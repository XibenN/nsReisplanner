import requests
import xmltodict
import json
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def reisplanner(request):
    jsonData = {}

    if 'beginstation' in request.GET and 'eindstation' in request.GET:
        beginstation = request.GET['beginstation']
        eindstation = request.GET['eindstation']
        auth_details = ('xibennguyen@gmail.com', '-asP1nMTjIeMl7RCfbHdxsNPGPphXY-QS7O_Q0gTBgK3apOBtXec5w')
        api_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={}&toStation={}&departure=true'.format(
            beginstation, eindstation)
        response = requests.get(api_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)
        nsDump = json.dumps(vertrekXML)
        jsonLoads = json.loads(nsDump)
        jsonData = jsonLoads['ReisMogelijkheden']['ReisMogelijkheid']

        for reis in jsonData:
            reis.update({'SpoorNummer': reis['ReisDeel'][0]['ReisStop'][0]['Spoor']['#text']})

        for date in jsonData:
            date.update({'VertrekTijdFormat': date['GeplandeVertrekTijd'][11:16]})
            date.update({'AankomstTijdFormat': date['GeplandeAankomstTijd'][11:16]})

        print(json.dumps(jsonData, indent=4))

    return render(request, 'reisplanner.html', {
        'jsonData': jsonData
    })


