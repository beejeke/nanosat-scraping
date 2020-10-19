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

import click
from .methods import SatelliteScraper


@click.group()
def cli():
    pass


def get_total_nanosats():
    scraper = SatelliteScraper()

    html = scraper.get_html('https://www.nanosats.eu/database')
    nanosats_names = scraper.get_nanosats_names_links(html)

    total = len(nanosats_names)

    return total


@cli.command(help='Ejecuta el scraper para obtener datos de los nanosatélites analizados.')
@click.option('--number', '-n', 'nanosats_n', default=get_total_nanosats(), show_default=True)
def scrape(nanosats_n):
    scraper = SatelliteScraper()
    scraper.scraper(int(nanosats_n))
    scraper.save_data_csv(nanosats_n)


if __name__ == '__main__':
    cli()