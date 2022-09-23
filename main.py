# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from utils.tools import Tools

def main():

    obj = Tools()

    mainURL = "https://www.portalbsd.com.br/tvterrestre.php"
    dictStatesURL = {}

    page = requests.get(mainURL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="dataTables-example")

    htmlTagLinkStates = results.find_all("a")
    for htmlTagLinkState in htmlTagLinkStates:
        UF = htmlTagLinkState.text[len(htmlTagLinkState.text) - 2:]
        dictStatesURL[UF] = "https://www.portalbsd.com.br/" + htmlTagLinkState['href']
    
    obj.converttoJson(dictStatesURL)

    keysDictStatesURL = list(dictStatesURL.keys())
    for key in keysDictStatesURL:
        linkURL = dictStatesURL.get(key)
        dictStatesURL[key] = obj.findAllCitiesState(linkURL)

    obj.converttoJson(dictStatesURL)

    keysDictStatesURL = list(dictStatesURL.keys())
    for key in keysDictStatesURL:
        citiesDictStatesURL = list(dictStatesURL[key].keys())
        for city in citiesDictStatesURL:
            linkURL = dictStatesURL[key].get(city)
            try:
                dictStatesURL[key][city] = obj.findAllChannelsCity(linkURL)
            except:
                dictStatesURL[key][city] = "Nenhum canal encontrado"
            print(city + " [COMPLETO]")
        print(key + " Completo")

    obj.converttoJson(dictStatesURL)

if __name__ == "__main__":
    main()