#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from datetime import datetime


def process(df, content):
    data_pattern = re.compile('[\w]+: ([\w]+)')
    hora, data = [tag.get_text().strip() for tag in contents[0].find_all('td') if re.match(data_pattern, tag.get_text())]
    hora = data_pattern.search(hora).group(1)
    data = data_pattern.search(data).group(1)
    full_date = datetime.strptime(' '.join([data, hora]), '%d/%m/%Y %Hh%M')
    new_content = {'Sumário': content.find('div', id='txSumarioID').get_text(),
                  'Discurso': content.find('p').get_text(),
                  'Sessão': re.search(re.compile("Sessão: ([\w.]+)"),
                      content.find('td', text=re.compile('Sessão:')).get_text().strip()).group(1),
                  'Data': full_date}
    df = df.append(new_content, ignore_index=True)
    return df

def main():
    base_url = 'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?txIndexacao=&CurrentPage={page_number}&BasePesq=plenario&txOrador=&txPartido=&dtInicio=01/01/2019&dtFim=31/12/2019&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=DESC&PageSize=50&txTexto=&txSumario='
    base_link = 'https://www.camara.leg.br/internet/sitaqweb/'
    links = list()
    df = pd.DataFrame({'Sumário': [], 'Discurso': []})
    
    for page_number in range(1, 408):
        site_data = requests.get(base_url.format(page_number=page_number))
        soup = BeautifulSoup(site_data.content, 'html.parser')
        link_tags = soup.find_all('a', href=re.compile('TextoHTML'))
        for tag in link_tags:
            links.append(re.sub(r"\s", "", tag['href']))
            
    for link in links:
        link_data = requests.get(base_link+link)
        link_soup = BeautifulSoup(link_data.content, 'html.parser')
        content = link_soup.find('div', id='content')
        df = process(df, content)
        
    return df
            
if __name__ == '__main__':
    df = main()
    df.to_csv('camara.csv')

