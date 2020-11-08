# 🚀 Nanosat Scraper 🚀

<p align="center">
  <img width="580" height="413" src="https://media.giphy.com/media/NXuqvtn9kp2smltRXc/giphy.gif">
</p>

## Práctica 1: Web scraping
### Descripción
Esta práctica ha sido desarrollada para la asignatura *Tipología y ciclo de vida de los datos*,
perteneciente al Máster Universitario en Ciencia de Datos, por la *Universitat Oberta de Catalunya* [UOC](https://www.uoc.edu/portal/es/index.html).
<br/>

El objetivo principal de dicha práctica es la aplicación de técnicas de [*web scraping*](https://es.wikipedia.org/wiki/Web_scraping),
usando el lenguaje de programación **Python** para la extracción de datos de un sitio web y generar posteriormente
un *dataset* con dicha información.

### Legalidad
El [sitio web](https://www.nanosats.eu/) no contiene un [recurso robots.txt](https://www.nanosats.eu/robots.txt). A continuación se cita al autor y el sitio web, acorde a las especificaciones de los términos y condiciones de uso: "Erik Kulu, Nanosats Database, www.nanostar.eu"

### Uso de la herramienta
Para poder hacer uso de la herramienta, hay que realizar una serie de pasos.
*   Creamos un entorno virtual de Python y lo activamos.
```
python3 -m venv <nombre_env>
```
*   Instalamos las dependencias, tanto del ```requirements.txt``` como del ```setup.py```
```
pip install -r requirements.txt
pip install -e .
```
*   Hacemos uso del CLI con el comando ```web-scraping```
```
# Por ejemplo, queremos obtener la información de todos los nanosatélites del sitio web
# con variantes:

$ web-scraping scrape
$ web-scraping -a
$ web-scraping --all
```

Además, podemos obtener los datos del número de nanosatélites que queramos.
```
# Por ejemplo, queremos obtener la información de los primeros 75 nanosatélites del sitio web
# con variantes:

$ web-scraping scrape -n 75
$ web-scraping --number 75

```

O también, en función del estado de la misión que queremos obtener datos, podemos elegir entre ```launched```,
```not-launched``` o ```all```

```
# Por ejemplo, queremos obtener la información de los primeros 850 nanosatélites del sitio web
# pero que hayan sido lanzados con éxito:

$ web-scraping scape -n 850 -s launched
$ web-scraping scape -n 850 --status launched
```
### Integrantes del equipo

*   [Omar Mendo Mesa](https://github.com/beejeke)
*   [Guzmán Manuel Gómez Pérez](https://github.com/GGP00)
