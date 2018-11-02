import requests
import xmltodict
import json
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def reisplanner(request):
    # Make jsonData global because it is being used on the detail page
    global jsonData
    jsonData = {}
    ErrorMessage = ''

    # If there is an error when inputting something, display a error message
    try:
        # Check if beginstation and eindstation exists in the request
        if 'beginstation' in request.GET and 'eindstation' in request.GET:
            # Get the values of the form and strip the extra spaces if there is any
            beginstation = request.GET['beginstation'].strip()
            eindstation = request.GET['eindstation'].strip()
            # To use the API you have to have an account, username:password
            auth_details = ('xibennguyen@gmail.com', '-asP1nMTjIeMl7RCfbHdxsNPGPphXY-QS7O_Q0gTBgK3apOBtXec5w')
            # Get the api url and insert the inputted data beginstation and eindstation
            api_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={}&toStation={}&departure=true'.format(
                beginstation, eindstation)
            # Get the response
            response = requests.get(api_url, auth=auth_details)
            # Convert to a dictionary
            vertrekXML = xmltodict.parse(response.text)

            # Write to a file
            with open('nsreisplanner.json', 'w') as nsAPI:
                nsAPI.write(json.dumps(vertrekXML, indent=4))

            # Open the file as read
            nsFile = open('nsreisplanner.json', 'r')
            nsDump = nsFile.read()

            # Convert to JSON
            jsonLoads = json.loads(nsDump)
            # The data is a Dictionary and in the dictionary is a list, we load that
            jsonData = jsonLoads['ReisMogelijkheden']['ReisMogelijkheid']

            # There are multiple dictionaries in dictionaries so we loop in the data
            for reis in jsonData:
                # We get all the planned times, format them with [11:16] and...
                # ...insert them in the first level of the dictionary
                reis.update({'VertrekTijdFormat': reis['GeplandeVertrekTijd'][11:16], 'AankomstTijdFormat': reis['GeplandeAankomstTijd'][11:16]})
                # We check if this gives an error because some stations...
                # ...just have one result of "ReisDeel", the [0] gives an error.
                try:
                    # Check if there is a "ReisDeel" because not every "Reis" has multiple "Reisdelen"
                    if 'Spoor' in reis['ReisDeel'][0]['ReisStop'][0]:
                        # Insert all the data where there are multiple 'ReisDelen' so we can access it in Django
                        reis.update({'SpoorNummer': reis['ReisDeel'][0]['ReisStop'][0]['Spoor']['#text'], 'Bestemming': reis['ReisDeel'][-1]['ReisStop'][-1]['Naam'], 'Vervoerder': reis['ReisDeel'][0]['Vervoerder'], 'RitNummer': reis['ReisDeel'][0]['RitNummer']})

                # When the error shows up, run this:
                except:
                    # Insert the data where there are just one 'ReisDeel' so we can access it in Django
                    reis.update({'SpoorNummer': reis['ReisDeel']['ReisStop'][0]['Spoor']['#text'], 'Bestemming': reis['ReisDeel']['ReisStop'][-1]['Naam'], 'Vervoerder': reis['ReisDeel']['Vervoerder'], 'RitNummer': reis['ReisDeel']['RitNummer']})
    except:
        # Display the Error Message when the input is wrong,
        # Put it in a variable so we can use it in the Django template
        ErrorMessage = 'Ongeldige station ingevoerd.'

    return render(request, 'reisplanner.html', {
        'jsonData': jsonData,
        'ErrorMessage': ErrorMessage
    })

def details(request):
    treinData = {}

    # Get the ritnummer in the URL
    ritNummer = request.GET.get('ritnummer', '')

    for data in jsonData:
        # Get the data associated with the ritnummer
        if data['RitNummer'] == ritNummer:
            # Put the data in the dictionary treinData
            treinData = data

    return render(request, 'details.html', {
        'treinData': treinData
    })

def vertrekTijden(request):
    jsonData = {}

    # Check if submitted 'station' is in the request
    if 'station' in request.GET:
        # Get the value of station
        station = request.GET['station']
        # Authenticate ourselves for the NS API
        auth_details = ('xibennguyen@gmail.com', '-asP1nMTjIeMl7RCfbHdxsNPGPphXY-QS7O_Q0gTBgK3apOBtXec5w')
        # Get the API url and insert the station value
        api_url = 'https://webservices.ns.nl/ns-api-avt?station={}'.format(
            station)
        # Get the response, convert it into a dictionary
        response = requests.get(api_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)

        # Write to a file
        with open('vertrektijden.json', 'w') as nsAPI:
            nsAPI.write(json.dumps(vertrekXML, indent=4))

        # Open the file as read
        nsFile = open('vertrektijden.json', 'r')
        nsDump = nsFile.read()

        # Convert to JSON
        jsonLoads = json.loads(nsDump)
        jsonData = jsonLoads['ActueleVertrekTijden']['VertrekkendeTrein']

        for reis in jsonData:
            # Format the vertrektijd and insert it into the dictionary JSON
            reis.update({'VertrekTijdFormat': reis['VertrekTijd'][11:16]})
            # Get the Spoornummer and insert it into the dictionary JSON
            # This is needed because there is no way to get the '#text' data in Django
            # Django does not accept the '#' so we are actually renaming it.
            reis.update({'SpoorNummer': reis['VertrekSpoor']['#text']})

    return render(request, 'vertrektijden.html', {
        'jsonData': jsonData
    })

