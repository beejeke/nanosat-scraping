"""
            Práctica 1 - Web Scraping

    Desarrollo de una herramienta para aplicar herramientas
    de web scraping sobre un sitio web, con el fin de extraer
    datos de interés y generar un dataset con dicha información.

    ==> Autores
        * Omar Mendo Mesa <@beejeke>
        * Guzmán Manuel Gómez Pérez <@GGP00>

    ==> Fichero
        * src/methods.py

    ==> Descripción
        Fichero principal donde se desarrollan los métodos necesarios para
        la extracción de datos a partir de un sitio web.
"""

import csv
import random
import re
import requests
import time
import pandas as pd

from bs4 import BeautifulSoup
from tqdm import tqdm

Y = '\033[1;33m'
B = '\033[1;36m'
G = '\033[1;32m'
P = '\033[1;35m'
W = '\033[1;37m'
NC = '\033[0m'

""" --- ACLARACIÓN ---

El siguiente diccionario se ha desarrollado para obtener unas cabeceras concretas para el futuro dataset
    - El nanosatélite 'deobitsail' tenía el mayor número de cabeceras útiles, por lo que se puede obtener
      la totalidad de los datos para todos los nanosatélites.
      
Lo mismo ocurre con los otros dos casos, que nos darán otro tipo de cabeceras para scrapear los datos en cuestión.
"""

HEADER_SAT = {'all': 'deorbitsail', 'launched': 'tubsat-n', 'not-launched': 'grbalpha'}


class SatelliteScraper:

    def __init__(self):
        self.url = 'https://www.nanosats.eu'
        self.subdomain = '/database'
        self.headers = []
        self.hdrs_data = []
        self.td_data = []
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

    def get_nanosats_names_links(self, html):
        """
        Método para obtener el nombre de cada nanosatélite mediante su link correspondiente.
        :param html: Estructura HTML de la página previamente recogida.
        :return: Lista con los nombres de cada nanosatélite.
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

    def get_nanosats_images_links(self, html):
        """
        Método para obtener las imagenes de cada nanosatélite mediante su link correspondiente.
        :param html: Estructura HTML de la página previamente recogida.
        :return: Lista con los enlaces de las imagenes de cada nanosatélite.
        """
        img_tags = html.findAll("a", {"class": "fancybox-1"})
        return [img['href'] for img in img_tags]

    def get_headers(self, html):
        """
        Método para obtener las cabeceras para el fichero CSV y determinar la estructura que deseamos.
        :param html: Estructura HTML de la página previamente recogida.
        :return: Lista con los nombres de las columnas que queremos tener en el dataset.
        """
        b_tags = html.find_all('b')

        hdrs = []
        for b in b_tags:
            hdrs.append(b.text)

        return hdrs

    def data_scraper(self, html):
        """
        Método que obtiene los datos de cada nanosatélite por estado.
        :param html: Estructura HTML de la página previamente recogida.
        """
        td_tags = html.find_all('td')

        extracted_data = []
        for td in td_tags:
            extracted_data.append(td.text)
        extracted_data.append(self.get_nanosats_images_links(html))

        self.data.append(extracted_data)

    def data_scraper_all(self, html):
        """
        Método que obtiene los datos de cada nanosatélite del total.
        :param html: Estructura HTML de la página previamente recogida.
        """
        table = html.find('table', class_='tcomp')
        td_tags = table.find_all(lambda tag: tag.name == 'td')
        header = self.get_headers(table)

        data = []
        for hdrs, td in zip(header, td_tags):
            data.append([hdrs, td.text])

        # Creamos una lista de listas con las cabeceras y los datos de las etiquetas 'td'
        self.hdrs_data = [item[0] for item in data]
        self.td_data = [item[1] for item in data]

        # Muchos nanosatélites no tienen cabecera 'Nation', si no 'Nation (HQ) y Nation (AIT), por lo que
        # solo queremos conservar el valor de Nation (HQ) y llamarlo 'Nation'.

        if 'Nation (HQ)' in self.hdrs_data:
            self.hdrs_data = ['Nation' if 'Nation (HQ)' in hdr else hdr for hdr in self.hdrs_data]

        extracted_data = []
        cnt = 0
        for hdr in self.headers[0]:
            # Si tenemos cabeceras coincidentes, añadimos los datos correspondientes por posición (índice)
            if hdr in self.hdrs_data:
                ind = self.hdrs_data.index(hdr)
                extracted_data.append(self.td_data[ind].rstrip().replace('"', ' '))
                cnt += 1
            else:
                # Si no son coincidentes, añadimos '?' como contenido
                extracted_data.append('?')
        extracted_data.append(self.get_nanosats_images_links(html))

        self.data.append(extracted_data)

    def scraper(self, nanosats_n, status):
        """
        Método principal donde se ejecutarán los métodos desarrollados previamente para scrapear los datos.
        """
        print(f"\n===> 🚀 {P}Web Scraping of nanosatellites launch missions data from{NC} " + "'" +
              f'{B}{self.url}{NC}' + f"' 🚀 <===\n")

        html = self.get_html(self.url + self.subdomain)
        nanosats_names = self.get_nanosats_names_links(html)

        # Number of nanosats to scrape passed by CLI ==> (src/main.py)
        nanosats_number = [nanosats_names[nano_number] for nano_number in range(nanosats_n)]

        print(f"===> {W}Number of nanosats to scrape: {Y}{len(nanosats_number)}/{len(nanosats_names)}{NC}\n\n")

        # En función del valor que hayamos introducido en el CLI, las cabeceras tendran unos valores u otros
        # como se ha comentado al comienzo del fichero  ==> HEADER_SAT
        html = self.get_html(self.url + f'/sat/{HEADER_SAT[status]}')
        self.headers.append(self.get_headers(html))

        cnt = 0
        for i, name in zip(nanosats_number, tqdm(nanosats_number)):
            tqdm.write("==> Adding nanosatellite name to his link: " + f'{B}{self.url}' + '/sat' + f'{name}{NC}')
            html = self.get_html(self.url + '/sat' + name)
            #time.sleep(random.randint(0, 2))

            # Si el valor del flag que pasamos por el CLI es -a/--all, coge las cabeceras del nanosat 'deorbitsail'
            if HEADER_SAT[status] == 'deorbitsail':
                tqdm.write(f'==> {G}Scraping data{NC} for ' + name + ' nanosatellite...')
                self.data_scraper_all(html)
                tqdm.write(f'==> {G}Data scraped:{NC} {W}{self.data[cnt]}{NC}\n\n')
                cnt += 1
            else:
                if self.headers == self.hdrs_data:
                    tqdm.write(f'==> {G}Scraping data{NC} for ' + name + ' nanosatellite...')
                    self.data_scraper(html)
                    tqdm.write(f'==> {G}Data scraped:{NC} {W}{self.data[cnt]}{NC}\n\n')
                    cnt += 1
                else:
                    tqdm.write(f'{B}[INFO]{NC} Invalid headers, discarding data [...]\n')
        self.df = pd.DataFrame(self.data, columns=[*self.headers[0], 'Images'])
        self.df = self.df.drop(labels='Sources', axis=1)

    def save_data_csv(self, nanosats_n, status):
        """
        Método principal para guardar los datos obtenidos en un dataset.
        """
        self.df.to_csv(f'datasets/nanosat_info-{nanosats_n}_{status}.csv', header=True, sep=';',
                       index=False, quoting=csv.QUOTE_NONE, escapechar=' ', encoding='utf-8')
        print(f'\n\n{G}Datos descargados con éxito:{NC}', '\n', f'{W}{self.df.head()}{NC}\n',
              '\n', f'\n{G}Guardados en:{NC} {W}/datasets{NC}\n')
