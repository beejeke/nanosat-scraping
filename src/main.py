"""
            Práctica 1 - Web Scraping

    Desarrollo de una herramienta para aplicar herramientas
    de web scraping sobre un sitio web, con el fin de extraer
    datos de interés y generar un dataset con dicha información.

    ==> Autores
        * Omar Mendo Mesa <@beejeke>
        * Guzmán Manuel Gómez Pérez <@GGP00>

    ==> Fichero
        * src/main.py

    ==> Descripción
        Fichero principal donde se ejecuta el scraper desarrollado.
"""

from methods import SatelliteScraper

if __name__ == '__main__':

    scraper = SatelliteScraper()
    scraper.scraper()
    scraper.save_data_csv()