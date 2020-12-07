"""
Autor: Felipe David Navarro Pecci
Fecha: 07/12/2020
Descripción: Código para recopilar los PDFs y XMLs del Borme de un día concreto

"""

## Import librerías
import requests
import csv
import re
import time

from bs4 import BeautifulSoup
from os import makedirs
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

## Definición de funciones

def descargar_archivos(links_archivos):
    """
    Función para descargar los archivos de los links indicados
    Se descarga el pdf y el xml

    Args:
        links_archivos (list): Lista de links de descarga de archivos
    """
    try:
        for link in links_archivos:

            # Cargar la URL
            response = requests.get(link)
            soup = BeautifulSoup(response.content,"html.parser")

            # Extraer el nombre de la cabecera y los links de los archivos
            metadatos = soup.find("div", class_="metadatos")
            cabecera = metadatos.find_all("dd")[2].get_text()
            cabecera = cabecera.lower().replace(" ","_")
        
            nombre_archivo = metadatos.find_all("dd")[3].get_text()
            nombre_archivo = nombre_archivo.lower().replace("-","_")
            
            links_descarga = soup.find("ul", class_="enlaces-doc sin-fondo")
            link_pdf = links_descarga.find("li", class_="puntoPDF")
            link_pdf = link_pdf.find("a")["href"]
            link_pdf = "https://www.boe.es" + link_pdf

            link_xml = links_descarga.find("li", class_="puntoXML")
            link_xml = link_xml.find("a")["href"]
            link_xml = "https://www.boe.es" + link_xml

            # Hacer una petición a los links para descargar a la carpeta correspondiente
            path_archivos = 'C:\\Users\\fdnav\\borme_adq\\files\\' + cabecera + '\\'

            response_pdf = requests.get(link_pdf)
            response_xml = requests.get(link_xml)       

            if not exists(path_archivos):
                makedirs(path_archivos)

            # Guardar PDF
            with open(path_archivos + nombre_archivo + ".pdf", "wb") as output_file:
                output_file.write(response_pdf.content)

            # Guardar XML
            with open(path_archivos + nombre_archivo + ".xml", "wb") as output_file:
                output_file.write(response_xml.content)


            time.sleep(3)

    except Exception as e:
        print("Error: " + e)


def get_links(seccion_segunda):
    """
    Función para extraer los links a los archivos de la sección segunda del BORME

    Args:
        seccion_segunda (BS4 HTML): HTML de la sección segunda

    Returns:
        links_html (list): lista con los links de la sección segunda
    """
    try:
        links_html = []
        response = requests.get(seccion_segunda)
        soup = BeautifulSoup(response.content,"html.parser")
        sumario = soup.find("div", class_="sumario")
        links = sumario.find_all("li", class_="puntoHTML")
        for i in links:
            tag = i.find("a")
            link = tag["href"]
            links_html.append("https://www.boe.es" + link)
            
    except Exception as e:
        print("Error: " + e)

    return links_html


def montar_url(url_boletin):
    """
    Función para añadir el querystring que lleva a la sección segunda del BORME

    Args:
        url_boletin (string): url del boletín
    Returns:
        url_boletin + querystring (string): url completa para ir a la sección segunda del BORME
    """

    return(url_boletin + "index.php?s=C")



def check_link(url,link_buscado):
    """
    Función para comprobar si el link pasado coincide con el que se busca

    Args:
        url (string): url a comprobar
        link_buscado (string): url que se busca

    Returns:
        match (bool): Ture/False dependiendo de si hay coincidencia o no
    """
    match = False
    if url != None:
        check = re.findall(link_buscado,url)
        if len(check) > 0:
            match = True
        else:
            pass
    return match

def get_boletin(fecha):
    """
    Función para obtener el link del boletín para la fecha indicada, en caso de que exista

    Args:
        fecha (string): Fecha para la que se busca el boletin

    Returns:
        url_boletin(string): Link del boletin para el dia indicado
    """
    url_boletin = "N/A"

    try:
        url_borme = "https://www.boe.es/diario_borme/index.php?m={}&a={}".format(fecha[0:4],fecha[4:6])
        response = requests.get(url_borme)
        soup = BeautifulSoup(response.content,"html.parser")

        target_table = soup.find("table", class_="BoeCalen")
        target_links = target_table.find_all("a")
        for link in target_links:
            url = link["href"]
            link_buscado = "/borme/dias/{}/{}/{}/".format(fecha[0:4],fecha[4:6],fecha[6:])
            if check_link(url,link_buscado):
                print("Borme disponible para la fecha {}/{}/{}/".format(fecha[0:4],fecha[4:6],fecha[6:]))
                url_boletin = "https://www.boe.es"+url
            else:
                pass

    except Exception as e:
        print("Error: "+ e)

    if url_boletin != "N/A":
        print("Boletín encontrado")
    else:
        print("Boletín no encontrado")

    return url_boletin


fecha = "20201202"
url_boletin = get_boletin(fecha)
if url_boletin != "N/A":
    seccion_segunda = montar_url(url_boletin)
    links_archivos = get_links(seccion_segunda)
    descargar_archivos(links_archivos)









