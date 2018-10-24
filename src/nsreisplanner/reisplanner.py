from __future__ import print_function
import requests
from .forms import reisplannerForm
import xmltodict
import json

beginstation = ''
eindstation = ''

def createForm(request):
    global beginstation
    global eindstation

    if request.method == 'POST':
        form = reisplannerForm(request.POST)
        if form.is_valid():
            beginstation = form.cleaned_data['beginstation']
            eindstation = form.cleaned_data['eindstation']

    print(beginstation, eindstation)
    form = reisplannerForm()

    return form

def apiLinkGenerator():
    auth_details = ('xibennguyen@gmail.com', '-asP1nMTjIeMl7RCfbHdxsNPGPphXY-QS7O_Q0gTBgK3apOBtXec5w')
    api_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={}&toStation={}&departure=true'.format(
        beginstation, eindstation)
    response = requests.get(api_url, auth=auth_details)
    vertrekXML = xmltodict.parse(response.text)
    nsDump = json.dumps(vertrekXML)
    jsonLoads = json.loads(nsDump)
    jsonData = jsonLoads['ReisMogelijkheden']['ReisMogelijkheid']

    return jsonData

def main():
    data = apiLinkGenerator()

    print('Dit zijn de vertrekkende treinen naar {}: '.format(eindstation))
    for data in data:
        # Reis informatie
        vertrekTijd = data['GeplandeVertrekTijd']
        actueleReisTijd = data['ActueleReisTijd']
        status = data['Status']
        aantalOverstappen = data['AantalOverstappen']

        # Reis Deel
        reisDeel = data['ReisDeel']
        vervoerder = reisDeel[0]['Vervoerder']
        vervoerType = reisDeel[0]['VervoerType']
        reisStops = []

        print('Om {} vertrekt er een trein naar {} met de vervoerder {} {}'.format(vertrekTijd[11:16], eindstation, vervoerder, vervoerType))
        print('De actuele reistijd naar {} is {}, de status is {}. Overstappen: {}'.format(eindstation, actueleReisTijd, status, aantalOverstappen))

        for stops in reisDeel[0]['ReisStop']:
            stopNaam = stops['Naam']
            reisStops.append(stopNaam)

        print(*reisStops, sep=', ')
