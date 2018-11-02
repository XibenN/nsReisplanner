import requests
import xmltodict
import json
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def reisplanner(request):
    global jsonData
    jsonData = {}
    ErrorMessage = ''

    try:
        if 'beginstation' in request.GET and 'eindstation' in request.GET:
            beginstation = request.GET['beginstation'].strip()
            eindstation = request.GET['eindstation'].strip()
            auth_details = ('xibennguyen@gmail.com', '-asP1nMTjIeMl7RCfbHdxsNPGPphXY-QS7O_Q0gTBgK3apOBtXec5w')
            api_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={}&toStation={}&departure=true'.format(
                beginstation, eindstation)
            response = requests.get(api_url, auth=auth_details)
            vertrekXML = xmltodict.parse(response.text)
            nsDump = json.dumps(vertrekXML)
            jsonLoads = json.loads(nsDump)
            jsonData = jsonLoads['ReisMogelijkheden']['ReisMogelijkheid']

            for reis in jsonData:
                reis.update({'VertrekTijdFormat': reis['GeplandeVertrekTijd'][11:16], 'AankomstTijdFormat': reis['GeplandeAankomstTijd'][11:16]})
                try:
                    if 'Spoor' in reis['ReisDeel'][0]['ReisStop'][0]:
                        reis.update({'SpoorNummer': reis['ReisDeel'][0]['ReisStop'][0]['Spoor']['#text'], 'Bestemming': reis['ReisDeel'][-1]['ReisStop'][-1]['Naam'], 'Vervoerder': reis['ReisDeel'][0]['Vervoerder'], 'RitNummer': reis['ReisDeel'][0]['RitNummer']})

                except:
                    reis.update({'SpoorNummer': reis['ReisDeel']['ReisStop'][0]['Spoor']['#text'], 'Bestemming': reis['ReisDeel']['ReisStop'][-1]['Naam'], 'Vervoerder': reis['ReisDeel']['Vervoerder'], 'RitNummer': reis['ReisDeel']['RitNummer']})
    except:
        ErrorMessage = 'Ongeldige station ingevoerd.'

    print(json.dumps(jsonData, indent=4))

    return render(request, 'reisplanner.html', {
        'jsonData': jsonData,
        'ErrorMessage': ErrorMessage
    })

def details(request):
    treinData = {}
    ritNummer = request.GET.get('ritnummer', '')

    for data in jsonData:
        if data['RitNummer'] == ritNummer:
            treinData = data

    return render(request, 'details.html', {
        'treinData': treinData
    })

def vertrekTijden(request):
    jsonData = {}

    if 'station' in request.GET:
        station = request.GET['station']
        auth_details = ('xibennguyen@gmail.com', '-asP1nMTjIeMl7RCfbHdxsNPGPphXY-QS7O_Q0gTBgK3apOBtXec5w')
        api_url = 'https://webservices.ns.nl/ns-api-avt?station={}'.format(
            station)
        response = requests.get(api_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)
        nsDump = json.dumps(vertrekXML)
        jsonLoads = json.loads(nsDump)
        jsonData = jsonLoads['ActueleVertrekTijden']['VertrekkendeTrein']

        for reis in jsonData:
            reis.update({'VertrekTijdFormat': reis['VertrekTijd'][11:16]})
            reis.update({'SpoorNummer': reis['VertrekSpoor']['#text']})

    return render(request, 'vertrektijden.html', {
        'jsonData': jsonData
    })

