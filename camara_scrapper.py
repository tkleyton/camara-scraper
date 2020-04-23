#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re


def process(content):
    print(content)
    return

def main():
    base_url = 'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?txIndexacao=&CurrentPage={page_number}&BasePesq=plenario&txOrador=&txPartido=&dtInicio=01/01/2019&dtFim=31/12/2019&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=DESC&PageSize=50&txTexto=&txSumario='
    base_link = 'https://www.camara.leg.br/internet/sitaqweb/'
    links = list()

    for page_number in range(1, 408):
    site_data = requests.get(base_url.format(page_number=1))
    soup = BeautifulSoup(site_data.content)
    link_tags = soup.find_all('a', href=re.compile('TextoHTML'))
    for tag in link_tags:
        links.append(re.sub(r"\s", "", tag['href']))

    for link in links:
    link_data = requests.get(base_link+link)
    link_soup = BeautifulSoup(link_data.content)
    content = link_soup.find('div', id='content')
    process(content)

if __name__ == '__main__':
    main()

