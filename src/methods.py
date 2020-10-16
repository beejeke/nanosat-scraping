"""
            Práctica 1 - Web Scraping

    Desarrollo de una herramienta para aplicar herramientas
    de web scraping sobre un sitio web, con el fin de extraer
    datos de interés y generar un dataset con dicha información.

    ==> Autores
        * Omar Mendo Mesa <@beejeke>
        * Guzmán Manuel Gómez Pérez <@GGP00>

    ==> Fichero
        * src/scrapper.py

    ==> Descripción
        Fichero principal donde se desarrollan los métodos necesarios para
        la extracción de datos a partir de un sitio web.
"""

from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re
import pandas as pd
import time
import random
from tqdm import tqdm

Y = '\033[1;33m'
B = '\033[1;36m'
G = '\033[1;32m'
NC = '\033[0m'


class SatelliteScraper:

    def __init__(self):
        self.url = 'https://www.nanosats.eu'
        self.subdomain = '/database'
        self.headers = []
        self.data = []
        self.df = pd.DataFrame()

    def get_html(self, url):
        """
        Método para obtener la URL a scrapear y parsearla a HTML.
        :param url: URL a scrapear.
        :return: Contenido de la respuesta en HTML.
        """
        response = requests.get(url)
        html = BeautifulSoup(response.content, 'html.parser')

        return html

    def get_nanosats_database_links(self, html):
        """
        Método para obtener la información detallada de cada nanosatélite mediante su link correspondiente
        :param html: Estructura HTML de la página previamente recogida.
        :return:
        """
        td_tags = html.find_all('td')

        nanosats_links = []
        for td in td_tags:
            a = td.next_element
            if a.name == 'a':
                href = a['href']
                if re.match('sat', href):
                    nanosats_links.append(href)

        print(nanosats_links)

        return nanosats_links

    def get_nanosats_names_links(self, html):
        """
        Método para obtener el nombre de cada nanosatélite mediante su link correspondiente
        :param html: Estructura HTML de la página previamente recogida.
        :return:
        """
        td_tags = html.find_all('td')

        nanosats_names = []
        for td in td_tags:
            a = td.next_element
            if a.name == 'a':
                href = a['href']
                if re.match('sat', href):
                    href = href[3:]
                    nanosats_names.append(href)

        return nanosats_names

    def get_headers(self, html):
        b_tags = html.find_all('b')

        hdrs = []
        for b in b_tags:
            hdrs.append(b.text)
        return hdrs

    def data_scraper(self, html):
        td_tags = html.find_all('td')

        extracted_data = []
        for td in td_tags:
            extracted_data.append(td.text)

        self.data.append(extracted_data)

    def scraper_test(self):
        html = self.get_html(self.url + self.subdomain)

        name_links = self.get_nanosats_names_links(html)
        for name in tqdm(name_links):
            html = self.get_html(self.url + '/sat' + name)
            headers = self.get_headers(self.url + '/sat' + name)
            headers.append(name)
            self.data_scraper(html)
            print(self.data)

    def scraper(self):
        print("\n===> Web Scraping of nanosatellites launch missions data from " + "'" + self.url + "'... <===\n\n")

        # 1. Download HTML
        html = self.get_html(self.url + self.subdomain)

        # 2. Get links for each name
        nanosats_names = self.get_nanosats_names_links(html)

        html = self.get_html(self.url + '/sat/tubsat-n')
        hdrs = self.get_headers(html)
        self.headers.append(hdrs)

        cnt = 0
        for i, name in zip(range(250), tqdm(nanosats_names, total=250)):
            tqdm.write("==> Adding nanosatellite name to his link: " + self.url + '/sat' + name)
            html = self.get_html(self.url + '/sat' + name)
            time.sleep(random.randint(0, 3))
            hdrs_ = self.get_headers(html)

            if self.headers == [hdrs_]:
                tqdm.write(f'==> {G}Scraping data{NC} for ' + name + ' nanosatellite...\n')
                self.data_scraper(html)
                tqdm.write(f'==> {G}Data scraped:{NC} {self.data[cnt]}\n')
                cnt += 1
            else:
                tqdm.write(f'{B}[INFO]{NC} Invalid headers, discarding data [...]\n')

        self.df = pd.DataFrame(self.data, columns=self.headers)

    def save_data_csv(self):
        saving_path = f'datasets/'
        abs_path = Path(saving_path).resolve()
        self.df.to_csv(str(abs_path) + '/nanosat_info.csv', header=True, sep=';',
                       index=False, encoding='utf-8')
        print('==> Datos descargados con éxito:', '\n', self.df.head(), '\n')
