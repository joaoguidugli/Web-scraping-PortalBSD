#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json

class Tools ():

    def converttoJson(self, dict):
        """Converte um dicionário Python em JSON.

        Args:
            dict (dict): dicionário Python a ser convertido.
        """
        
        with open("wsportalbsd.json", "w") as outfile:
            json.dump(dict, outfile)

    def findAllChannelsCity(self, cityURL):
        """_summary_

        Args:
            cityURL (String): recebe a URL referente a cidade que serão buscado os canais.

        Returns:
            dict: retorna um dicionário com nome de todas os canais de uma cidade e as informações referentes.
                Exemplo:
                {
                    "RPC TV": {
                        "numberDigital": "12.1",
                        "numberPhysical": "42 UHF",
                        "frequencyChannel": "641.143 MHz",
                        "logoChannel": "https://www.portalbsd.com.br/images/tv/rpc.png",
                        "networkChannel": "Globo",
                        "audioChannel": "Estéreo",
                        "videoChannel ": "HDTV"
                    },
                    "Channel 2": {
                        [...]
                    }
                }
        """

        dictChannels = {}
        infoChannel = {}

        page = requests.get(cityURL)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find_all("table")
        table = table[0]

        trChannels = table.find_all("tr")
        for trChannel in trChannels:
            tdsChannel = trChannel.find_all("td")
            numberDigital = tdsChannel[0].text
            numberPhysical = ((tdsChannel[1].text).replace("UHF", " UHF")).replace("VHF", " VHF")
            frequencyChannel = tdsChannel[2].text
            logoChannel = "https://www.portalbsd.com.br/" + (tdsChannel[3].find("img"))['src']
            nameChannel = (tdsChannel[4].find("a")).text
            networkChannel = nameChannel[(nameChannel.find("("))+1:nameChannel.find(")")]
            nameChannel = nameChannel.replace((" (" + networkChannel + ")"), "")
            audioChannel = tdsChannel[5].text
            colorBackgound = ((tdsChannel[5])['style'])[13:19]
            if colorBackgound == "DA70D6":
                videoChannel = "HDTV"
            elif colorBackgound == "F68E56":
                videoChannel = "Standard"
            elif colorBackgound == "82CA9C":
                videoChannel = "Analógico"
            else:
                videoChannel = ""

            infoChannel = {'numberDigital': numberDigital, 'numberPhysical': numberPhysical, 'frequencyChannel': frequencyChannel, 'logoChannel': logoChannel, 'networkChannel': networkChannel, 'audioChannel': audioChannel, 'videoChannel ': videoChannel}
            dictChannels[nameChannel] = infoChannel

        return dictChannels

    def findAllCitiesState(self, stateURL):
        """_summary_

        Args:
            stateURL (String): recebe a URL referente ao estado em que buscarão as cidades.

        Returns:
            dict: retorna um dicionário com nome de todas as cidades e URLs referentes da tabela de um estado.
                Exemplo:
                {
                    "Catas Altas da Noruega": "https://www.portalbsd.com.br/terrestres_channels.php?cidade=4603",
                    "Monsenhor Paulo": "https://www.portalbsd.com.br/terrestres_channels.php?cidade=4602"
                }
        """

        dictCitiesURL = {}

        page = requests.get(stateURL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all(id="dataTables-example")
        results = results[1]

        htmlTagLinkCities = results.find_all("a")
        for htmlTagLinkCity in htmlTagLinkCities:
            cityName = htmlTagLinkCity.text[2:]
            dictCitiesURL[cityName] = "https://www.portalbsd.com.br/" + htmlTagLinkCity['href']

        return dictCitiesURL