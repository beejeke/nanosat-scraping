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
import requests


class SatelliteScraper:

    def __init__(self):
        self.url = 'https://spacefund.com/launch-database/'
        self.data = []

    def get_html(self, url):
        """
        Método para obtener la URL a scrapear y parsearla a HTML.
        :param url: URL a scrapear.
        :return: Contenido de la respuesta en HTML.
        """
        response = requests.get(url)
        html = BeautifulSoup(response.content, 'html.parser')

        return html

    def get_headers(self, html):
        """
        Método para obtener las cabeceras del dataset.
        :param html: Estructura HTML de la página previamente recogida.
        :return: Headers para el futuro dataset.
        """
        hdrs = html.find_all('th', class_='wdtheader')

        headers = []
        for h in hdrs:
            headers.append(h.text)

        return headers

    def scrap(self):
        html = self.get_html(self.url)
        headers = self.get_headers(html)
        print(headers)