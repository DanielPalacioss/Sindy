#Como la regresion logistica necesita mas de 1 variable para predecir el futuro, necesitamos que ya sea en los partidos del local o el visitante alla al un partido donde gane y otro donde pierda. si no da error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from xgboost import XGBRegressor, plot_importance
import matplotlib.pyplot as plt
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import math
import pandas as pd
import os
from RecoleccionEquipos import EquipmentCollection
from selenium.webdriver.chrome.options import Options
from getMatch import getMatch
import sys
import numpy as np
from datetime import datetime, timedelta
from getAlineacion import getAlineacion
import re
from unidecode import unidecode
from xgboost import XGBClassifier
from sklearn.multioutput import MultiOutputClassifier

options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-blink-features=AutomationControlled")  # Evita detección
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-extensions")  # Sin extensiones
options.add_argument("--disable-popup-blocking")  # Bloquea pop-ups
options.add_argument("--disable-gpu")  # Mejora rendimiento en Windows
options.add_argument("--disable-dev-shm-usage")  # Previene problemas de memoria



# Ingreso de datos por parte del usuario
equipo_objetivo_1 = "Valencia C. F."#input("Ingresa el primer equipo objetivo: ")
equipo_objetivo_2 = "RCD Espanyol"#input("Ingresa el segundo equipo objetivo: ")

# Estadísticas a excluir (fijas como en el código original)
estadisticas_excluidas = ["Posición adelantada"]
urls_equipo_1 = []
urls_equipo_2 = []

if os.path.exists(f"{equipo_objetivo_1}.csv"):
    opcion = input(f"Desea cargar nuevos datos del {equipo_objetivo_1}?  SI/NO ")
    if(opcion.strip().lower() == "si"):
        if os.path.exists("equipos_links.csv"):
            # Cargar el CSV en un DataFrame
            df = pd.read_csv("equipos_links.csv")
            if equipo_objetivo_1 in df["Equipo"].values:
                matchsNumber = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_1}? "))

                #Buscar link de lista de partidos
                url = df.loc[df["Equipo"] == equipo_objetivo_1, "Link_Lista_Partidos"].values[0]
                
                #Buscar link de un partido x del equipo
                defaultLink = df.loc[df["Equipo"] == equipo_objetivo_1, "Link_Partido_X"].values[0]
                
                #Ejecutar para recolectar link
                urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)
            
            else:
                matchsNumber = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_1}? "))
                url = input(f"Ingrese la url de la lista de partidos de {equipo_objetivo_1} ")
                defaultLink = input(f"Ingrese la url de un partido x de {equipo_objetivo_1} ")
                urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)
                
                # Crear nueva fila como diccionario
                nueva_fila = {"Equipo": equipo_objetivo_1, "Link_Lista_Partidos": url, "Link_Partido_X": defaultLink}

                # Agregar la fila al DataFrame
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

                # Guardar el DataFrame actualizado en el CSV
                df.to_csv("equipos_links.csv", index=False)
        else:
            # Si el archivo no existe, creamos el DataFrame desde cero
            matchsNumber = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_1}? "))
            url = input(f"Ingrese la URL de la lista de partidos de {equipo_objetivo_1}: ")
            defaultLink = input(f"Ingrese la URL de un partido X de {equipo_objetivo_1}: ")

            # Crear DataFrame con la nueva fila
            df = pd.DataFrame([{
                "Equipo": equipo_objetivo_1, 
                "Link_Lista_Partidos": url, 
                "Link_Partido_X": defaultLink
            }])

            # Guardar el DataFrame en un nuevo CSV
            df.to_csv("equipos_links.csv", index=False)
            urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)
else:
    if os.path.exists("equipos_links.csv"):
        # Cargar el CSV en un DataFrame
        df = pd.read_csv("equipos_links.csv")
        if equipo_objetivo_1 in df["Equipo"].values:
            matchsNumber = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_1}? "))

            #Buscar link de lista de partidos
            url = df.loc[df["Equipo"] == equipo_objetivo_1, "Link_Lista_Partidos"].values[0]
            
            #Buscar link de un partido x del equipo
            defaultLink = df.loc[df["Equipo"] == equipo_objetivo_1, "Link_Partido_X"].values[0]
            
            #Ejecutar para recolectar link
            urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)
        
        else:
            matchsNumber = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_1}? "))
            url = input(f"Ingrese la url de la lista de partidos de {equipo_objetivo_1} ")
            defaultLink = input(f"Ingrese la url de un partido x de {equipo_objetivo_1} ")
            urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)
            
            # Crear nueva fila como diccionario
            nueva_fila = {"Equipo": equipo_objetivo_1, "Link_Lista_Partidos": url, "Link_Partido_X": defaultLink}

            # Agregar la fila al DataFrame
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

            # Guardar el DataFrame actualizado en el CSV
            df.to_csv("equipos_links.csv", index=False)
    else:
        # Si el archivo no existe, creamos el DataFrame desde cero
        matchsNumber = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_1}? "))
        url = input(f"Ingrese la URL de la lista de partidos de {equipo_objetivo_1}: ")
        defaultLink = input(f"Ingrese la URL de un partido X de {equipo_objetivo_1}: ")

        # Crear DataFrame con la nueva fila
        df = pd.DataFrame([{
            "Equipo": equipo_objetivo_1, 
            "Link_Lista_Partidos": url, 
            "Link_Partido_X": defaultLink
        }])

        # Guardar el DataFrame en un nuevo CSV
        df.to_csv("equipos_links.csv", index=False)
        urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)

if os.path.exists(f"{equipo_objetivo_2}.csv"):
    opcion = input(f"Desea cargar nuevos datos del {equipo_objetivo_2}?  SI/NO ")
    if(opcion.strip().lower() == "si"):
        if os.path.exists("equipos_links.csv"):
            # Cargar el CSV en un DataFrame
            df = pd.read_csv("equipos_links.csv")
            if equipo_objetivo_2 in df["Equipo"].values:
                matchsNumber2 = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_2}? "))

                #Buscar link de lista de partidos
                url2 = df.loc[df["Equipo"] == equipo_objetivo_2, "Link_Lista_Partidos"].values[0]
                
                #Buscar link de un partido x del equipo
                defaultLink2 = df.loc[df["Equipo"] == equipo_objetivo_2, "Link_Partido_X"].values[0]
                
                #Ejecutar para recolectar link
                urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)
            
            else:
                matchsNumber2 = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_2}? "))
                url2 = input(f"Ingrese la url de la lista de partidos de {equipo_objetivo_2} ")
                defaultLink2 = input(f"Ingrese la url de un partido x de {equipo_objetivo_2} ")
                urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)
                
                # Crear nueva fila como diccionario
                nueva_fila = {"Equipo": equipo_objetivo_2, "Link_Lista_Partidos": url2, "Link_Partido_X": defaultLink2}

                # Agregar la fila al DataFrame
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

                # Guardar el DataFrame actualizado en el CSV
                df.to_csv("equipos_links.csv", index=False)
        else:
            # Si el archivo no existe, creamos el DataFrame desde cero
            matchsNumber2 = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_2}? "))
            url2 = input(f"Ingrese la URL de la lista de partidos de {equipo_objetivo_2}: ")
            defaultLink2 = input(f"Ingrese la URL de un partido X de {equipo_objetivo_2}: ")

            # Crear DataFrame con la nueva fila
            df = pd.DataFrame([{
                "Equipo": equipo_objetivo_2, 
                "Link_Lista_Partidos": url2, 
                "Link_Partido_X": defaultLink2
            }])

            # Guardar el DataFrame en un nuevo CSV
            df.to_csv("equipos_links.csv", index=False)
            urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)

else:
    if os.path.exists("equipos_links.csv"):
        # Cargar el CSV en un DataFrame
        df = pd.read_csv("equipos_links.csv")
        if equipo_objetivo_2 in df["Equipo"].values:
            matchsNumber2 = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_2}? "))

            #Buscar link de lista de partidos
            url2 = df.loc[df["Equipo"] == equipo_objetivo_2, "Link_Lista_Partidos"].values[0]
            
            #Buscar link de un partido x del equipo
            defaultLink2 = df.loc[df["Equipo"] == equipo_objetivo_2, "Link_Partido_X"].values[0]
            
            #Ejecutar para recolectar link
            urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)
        
        else:
            matchsNumber2 = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_2}? "))
            url2 = input(f"Ingrese la url de la lista de partidos de {equipo_objetivo_2} ")
            defaultLink2 = input(f"Ingrese la url de un partido x de {equipo_objetivo_2} ")
            urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)
            
            # Crear nueva fila como diccionario
            nueva_fila = {"Equipo": equipo_objetivo_2, "Link_Lista_Partidos": url2, "Link_Partido_X": defaultLink2}

            # Agregar la fila al DataFrame
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

            # Guardar el DataFrame actualizado en el CSV
            df.to_csv("equipos_links.csv", index=False)
    else:
        # Si el archivo no existe, creamos el DataFrame desde cero
        matchsNumber2 = int(input(f"¿Cuántas URLs deseas ingresar del equipo {equipo_objetivo_2}? "))
        url2 = input(f"Ingrese la URL de la lista de partidos de {equipo_objetivo_2}: ")
        defaultLink2 = input(f"Ingrese la URL de un partido X de {equipo_objetivo_2}: ")

        # Crear DataFrame con la nueva fila
        df = pd.DataFrame([{
            "Equipo": equipo_objetivo_2, 
            "Link_Lista_Partidos": url2, 
            "Link_Partido_X": defaultLink2
        }])

        # Guardar el DataFrame en un nuevo CSV
        df.to_csv("equipos_links.csv", index=False)
        urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)

#Validacion de link en equipo local
opcion = input(f"El link del {equipo_objetivo_1} quedo mal ingresado?  SI/NO ")
if(opcion.strip().lower() == "si"):
    # Cargar el CSV en un DataFrame
    df = pd.read_csv("equipos_links.csv")

    # Eliminar la fila del equipo incorrecto
    df = df[df["Equipo"] != equipo_objetivo_1]

    url = input(f"Ingrese la url de la lista de partidos de {equipo_objetivo_1} ")
    defaultLink = input(f"Ingrese la url de un partido x de {equipo_objetivo_1} ")

    # Crear DataFrame con la nueva fila
    nueva_fila = pd.DataFrame([{
        "Equipo": equipo_objetivo_1, 
        "Link_Lista_Partidos": url, 
        "Link_Partido_X": defaultLink
    }])

    # Agregar la nueva fila al DataFrame
    df = pd.concat([df, nueva_fila], ignore_index=True)

    # Guardar el DataFrame actualizado
    df.to_csv("equipos_links.csv", index=False)

#Validacion de link en equipo visitante
opcion2 = input(f"El link del {equipo_objetivo_2} quedo mal ingresado?  SI/NO ")
if(opcion2.strip().lower() == "si"):
    # Cargar el CSV en un DataFrame
    df = pd.read_csv("equipos_links.csv")

    # Eliminar la fila del equipo incorrecto
    df = df[df["Equipo"] != equipo_objetivo_2]

    url2 = input(f"Ingrese la url de la lista de partidos de {equipo_objetivo_2} ")
    defaultLink2 = input(f"Ingrese la url de un partido x de {equipo_objetivo_2} ")

    # Crear DataFrame con la nueva fila
    nueva_fila = pd.DataFrame([{
        "Equipo": equipo_objetivo_2, 
        "Link_Lista_Partidos": url2, 
        "Link_Partido_X": defaultLink2
    }])

    # Agregar la nueva fila al DataFrame
    df = pd.concat([df, nueva_fila], ignore_index=True)

    # Guardar el DataFrame actualizado
    df.to_csv("equipos_links.csv", index=False)

    print("♻️ Reiniciando el script...")
    os.execv(sys.executable, ["python"] + sys.argv)  # Reinicia el script
else:
    if opcion.strip().lower() == "si":
        print("♻️ Reiniciando el script...")
        os.execv(sys.executable, ["python"] + sys.argv)  # Reinicia el script


equipos_dict = EquipmentCollection().get_dict_of_csv()
if len(equipos_dict) == 1:
    raise Exception("No se ha agregado equipos, por favor agregarlos")

# Configuración de Selenium con ChromeDriver
service =  Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

Torneo = 1 #Torneo de partido a predecir, para saber que numero poner, vaya a bajo en el diccionario torneo

if equipos_dict.get(equipo_objetivo_1, -1) == -1:
    raise Exception(f"El equipo {equipo_objetivo_1} no existe en la base de datos, por favor agregarlo")
if equipos_dict.get(equipo_objetivo_2, -1) == -1:
    raise Exception(f"El equipo {equipo_objetivo_2} no existe  en la base de datos, por favor agregarlo")

equipo_objetivo_1_ID = equipos_dict.get(equipo_objetivo_1, -1)
equipo_objetivo_2_ID = equipos_dict.get(equipo_objetivo_2, -1)
# Diccionario de torneos
torneos_dict = {
    "Liga de Campeones de la UEFA": 0,
    "LaLiga": 1,
    "Ligue 1": 2,
    "Premier League": 3,
    "Serie A": 4,
    "Europa League":5,
    "Amistosos": 6,
    "Segunda División":7,
    "Conference League": 8,
    "Bundesliga": 9,
    "Brasileirão Serie A": 10,
    "Copa Libertadores": 11,
    "Copa de Brasil": 12,
    "Copa de Francia": 13,
    "EFL Cup": 14,
    "FA Cup": 15,
    "Championship": 16,
    "Supercopa de Europa": 17,
    "Supercopa de España": 18,
    "Copa del Rey": 19,
    "Mundial de Clubes": 20,
    "Liga Conferencia": 21,
    "Serie B": 22,
    "DFB Pokal": 23,
    "2. Bundesliga": 24,
    "Copa Emirates": 25,
    "Copa Sudamericana": 26,
    "Campeonato Paulista": 27,
    "Copa Paulista": 28,
    "Brasileirão Série B": 29,
    "Copa do Nordeste": 30,
    "Campeonato Cearense": 31,
    "Campeonato Mineiro": 32,
    "Supercopa de Brasil": 33,
    "Carioca Serie A": 34,
    "Copa Italia": 35,
    "Ligue Professionnelle 3": 36,
    "Championnat National": 37,
    "Championnat National 2": 38,
    "Ligue 2": 39,
    "Football League One": 40,
    "National League N / S": 41,
    "Football League Trophy": 42,
    "Non League Premier": 43,
    "Tercera División de España": 44,
    "3. Liga": 45,
    "Serie C": 46,
    "Supercopa de Alemania": 47,
    "Campeonato Gaúcho": 48,
    "SuperLiga Serbia": 49,
    "Prva Liga": 50,
    "Primera Liga de Croacia": 51,
    "Supercopa de Croacia": 52,
    "Torneo desconocido": -1
    # Agrega otros torneos según necesites
}

# Alineaciones
alineaciones_dict = {
    "4-3-3": 0,
    "4-4-2": 1,
    "3-5-2": 2,
    "4-2-3-1": 3,
    "5-3-2": 4,
    "4-5-1": 5,
    "3-4-3": 6,
    "4-1-4-1": 7,
    "4-4-1-1": 8,
    "5-4-1": 9,
    "5-3-1-1": 10,
    "5-2-3": 11,
    "6-3-1": 12,
    "4-2-2-2": 13,
    "4-1-3-2": 14,
    "3-6-1": 15,
    "3-3-3-1": 16,
    "3-4-2-1": 17,
    "2-3-5": 18,
    "4-2-4": 19,
    "4-3-2-1": 20,
    "3-2-5": 21,
    "4-1-2-1-2": 22,
    "3-5-1-1": 23,
    "3-3-1-3": 24,
    "4-2-1-3": 25,
    "5-2-2-1": 26,
    "3-2-2-3": 27,
    "4-3-1-2": 28,
    "3-4-1-2": 29,
    "3-1-4-2": 30,
    "3-2-4-1": 31,
    "No encontrado":-1
}

# Diccionario para almacenar las estadísticas de los partidos
stats = {equipo_objetivo_1: {}, equipo_objetivo_2: {}}

def obtener_estadisticas(soup, equipo_objetivo):
    try:
        fecha_div = soup.find('div', class_= 'imso_mh__pst-m-stts-l')
        fecha = fecha_div.find('div', class_= 'imso-hide-overflow').find_all('span')[4].text.strip()
        stats_table = soup.find('div', class_='lr-imso-ss-wdm')
        partido_stats = {}
        fecha_actual = datetime.now()
        year = fecha_actual.year
        fecha = fecha.split(",")
        if(len(fecha) > 1):
            fecha = fecha[1].replace(' ', '')+f"/{year}" #Esto debe modificarse segun el año en el que estemos
            fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
        elif(len(fecha[0].replace(' ', '')) <= 5):
            fecha = fecha[0].replace(' ', '')+f"/{year}"
            if(fecha == f"Hoy/{year}"): 
                fecha = fecha_actual.strftime("%d/%m/%Y")
            elif(fecha == f"Ayer/{year}"):
                fecha = (fecha_actual - timedelta(days=1)).strftime("%d/%m/%Y") #restamos un dia
            fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
        else:
            fecha = fecha[0]
            fecha = datetime.strptime(fecha, "%d/%m/%y").date()
            
        partido_stats["Fecha"] = fecha
        partido_stats["Equipo_name"] = equipo_objetivo

        alineacion = ""
        alineacionContrincante = ""
        local = 0
        # Obtener el nombre del torneo
        torneo_div = soup.find('div', class_='imso-hide-overflow')
        torneo_span = torneo_div.find('span', class_='imso-loa imso-ln')
        torneo_nombre = torneo_span.text.strip() if torneo_span else "Torneo desconocido"
        # Obtener la alineacion del equipo objetivo
        alineacion_div = soup.find('div', class_='lr-imso-lineups-container')
        local_div = alineacion_div.find('div', class_='lr-vl-hf lrvl-btrc')
        visitante_div = alineacion_div.find('div', class_='lr-vl-hf lrvl-bbrc')
        local_all_span = local_div.find_all('span')
        visitante_all_span = visitante_div.find_all('span')

        if(local_all_span[0].text.strip() == equipo_objetivo):
            alineacion = local_all_span[1].text.strip()
            alineacionContrincante = visitante_all_span[1].text.strip()
        else:
            alineacion = visitante_all_span[1].text.strip()
            alineacionContrincante = local_all_span[1].text.strip()
            local = 1

        # Buscar el torneo en el diccionario y agregar el valor numérico
        torneo_valor = torneos_dict.get(torneo_nombre, -1)  # Si no lo encuentra, asigna -1

        # Agregar el valor numérico del torneo a las estadísticas del partido
        partido_stats["Torneo"] = torneo_valor

        # Buscar la alineacion en el diccionario y agregar el valor numérico
        alineacion_valor = alineaciones_dict.get(alineacion, -1)
        alineacion_contrincante_valor = alineaciones_dict.get(alineacionContrincante, -1)
        partido_stats["Alineacion"] = alineacion_valor
        partido_stats["Alineacion_contrincante"] = alineacion_contrincante_valor
        headers = stats_table.find_all('th', class_='jqZdce')
        
        if local == 0:
            equipo_objetivo_columna = 0
            equipo_contrincante = headers[1].find('img')['alt']
        else:
            equipo_objetivo_columna = 1
            equipo_contrincante = headers[0].find('img')['alt']

        partido_stats["equipo"] = equipos_dict.get(equipo_objetivo, -1)
        partido_stats["equipo_contrincante"] = equipos_dict.get(equipo_contrincante, -1)
        partido_stats["equipo_contrincante_name"] = equipo_contrincante
        partido_stats["tarjetas"] = 0
        partido_stats["tarjetas_contrincante"] = 0
        rows = stats_table.select('tr.MzWkAb')
        columna_contrincante = 1 - equipo_objetivo_columna
        
        for row in rows:
            stat_name = row.find('th').text
            if stat_name not in estadisticas_excluidas:
                stat_value = int(row.find_all('td')[equipo_objetivo_columna].text.strip().replace('%', ''))
                partido_stats[stat_name] = stat_value
                if stat_name in ["Tarjetas amarillas", "Tarjetas rojas"]:
                    partido_stats["tarjetas"] += stat_value
                    
            if stat_name in ["Remates","Remates al arco","Posesión", "Faltas","Tarjetas amarillas","Tarjetas rojas","Tiros de esquina"]:
                stat_value = int(row.find_all('td')[columna_contrincante].text.strip().replace('%', ''))
                partido_stats[f"{stat_name}_contrincante"] = stat_value
                if stat_name in ["Tarjetas amarillas", "Tarjetas rojas"]:
                    partido_stats["tarjetas_contrincante"] += stat_value

        formacion_local_div = soup.find('div', class_= 'lrvl-tlt lrvl-tl lrvl-btrc')
        formacion_visitante_div = soup.find('div', class_= 'lrvl-tlt lrvl-tl lrvl-bbrc')
        jugadores_formacion_local_div = formacion_local_div.find_all('div', class_= 'A9ad7e imso-loa')
        jugadores_formacion_visitante_div = formacion_visitante_div.find_all('div', class_= 'A9ad7e imso-loa')
        
        if local == 0:
            for i, jugador_span in enumerate(jugadores_formacion_local_div, start= 1):
                jugador = jugador_span.find_all('span')
                partido_stats[f"{jugador[1].get('aria-label')}-{equipo_objetivo}"] = 1
            
        else:
            for i, jugador_span in enumerate(jugadores_formacion_visitante_div[::-1], start=1):
                jugador = jugador_span.find_all('span')
                partido_stats[f"{jugador[1].get('aria-label')}-{equipo_objetivo}"] = 1
        
        partido_stats['Tiros de esquina_concedidos'] = partido_stats['Tiros de esquina_contrincante']
        del partido_stats['Tiros de esquina_contrincante']
        partido_stats["Posesión"] = partido_stats["Posesión"]/100
        partido_stats["Posesión_contrincante"] = partido_stats["Posesión_contrincante"]/100
        partido_stats["Precisión de los pases"] = partido_stats["Precisión de los pases"]/100
        partido_stats["Posesión_contra_por_remate"] = np.nan if partido_stats["Remates_contrincante"] == 0 else partido_stats["Posesión_contrincante"] / partido_stats["Remates_contrincante"]
        #partido_stats["Posesión_contra_por_remate"] = partido_stats["Posesión_contrincante"]/partido_stats["Remates_contrincante"].replace(0, np.nan)
        #partido_stats["tarjetas_por_falta"] = partido_stats["tarjetas"]/partido_stats["Faltas"].replace(0, np.nan)
        partido_stats["tarjetas_por_falta"] = np.nan if partido_stats["Faltas"] == 0 else partido_stats["tarjetas"] / partido_stats["Faltas"]
        partido_stats["pases_completados"] = round((partido_stats["Pases"] * partido_stats["Precisión de los pases"]))
        partido_stats["faltas_por_pases"] = np.nan if partido_stats["pases_completados"] == 0 else partido_stats["Faltas"] / partido_stats["pases_completados"]
        #partido_stats["faltas_por_pases"] = partido_stats["Faltas"]/partido_stats["pases_completados"].replace(0, np.nan)
        partido_stats["pases_por_posesion"] = partido_stats["pases_completados"]/partido_stats["Posesión"]
        partido_stats["tirosEsquina_por_remate"] = np.nan if partido_stats["Remates"] == 0 else partido_stats["Tiros de esquina"] / partido_stats["Remates"]
        partido_stats["tirosEsquina_por_posesion"] = np.nan if partido_stats["Posesión"] == 0 else partido_stats["Tiros de esquina"] / partido_stats["Posesión"]
        partido_stats["diff_remates"] = partido_stats["Remates"] - partido_stats["Remates_contrincante"]

        #partido_stats["tirosEsquina_por_remate"] = partido_stats["Tiros de esquina"]/partido_stats["Remates"].replace(0, np.nan)
        #partido_stats["tirosEsquina_por_posesion"] = partido_stats["Tiros de esquina"]/partido_stats["Posesión"].replace(0, np.nan)
        #partido_stats["diff_remates"] = partido_stats["Remates"] - partido_stats["Remates_contrincante"].replace(0, np.nan)
        partido_stats["diff_posesion"] = partido_stats["Posesión"] - partido_stats["Posesión_contrincante"]
        partido_stats["diff_Tiros de esquina"] = partido_stats["Tiros de esquina"] - partido_stats["Tiros de esquina_concedidos"]
        partido_stats["diff_tarjetas"] = partido_stats["tarjetas"] - partido_stats["tarjetas_contrincante"]
        #partido_stats["diff_Tiros de esquina"] = partido_stats["Tiros de esquina"] - partido_stats["Tiros de esquina_concedidos"].replace(0, np.nan)
        #partido_stats["diff_tarjetas"] = partido_stats["tarjetas"] - partido_stats["tarjetas_contrincante"].replace(0, np.nan)
        partido_stats["diff_faltas"] = partido_stats["Faltas"] - partido_stats["Faltas_contrincante"]
        partido_stats["remates_por_pase"] = partido_stats["Remates"]/partido_stats["Pases"]
        return partido_stats
    except Exception as e:
        print(f"Error al obtener estadísticas para {equipo_objetivo}: {e}")
        return None

def obtener_goles_por_tiempo(soup, equipo_objetivo):
    goles_por_tiempo = {
        'goles_primera_mitad': 0, 
        'goles_segunda_mitad': 0,
        'goles_totales': 0,  # Campo para goles totales
        'gano': 0,  # Nuevo campo booleano para indicar si ganó o no
        'empato': 0,
        'perdio': 0,
        'visitante': 0,
        'local': 0
    }

    try:
        # Encontrar la sección de resultados
        equipo_local = soup.find('div', class_='imso_mh__first-tn-ed').find('span').text
        equipo_visitante = soup.find('div', class_='imso_mh__second-tn-ed').find('span').text
        # Buscar los goles en el marcador principal
        marcador_local = int(soup.find('div', class_='imso_mh__l-tm-sc').text.strip())
        
        marcador_visitante = int(soup.find('div', class_='imso_mh__r-tm-sc').text.strip())
        
        # Si ambos equipos tienen 0 goles, retornar directamente
        if marcador_local == 0 and marcador_visitante == 0:
            print(f"Ambos equipos no tienen goles en el partido actual ({equipo_local} vs {equipo_visitante}).")
                # Determinar si el equipo objetivo ganó o no
            if equipo_objetivo == equipo_local:
                goles_objetivo = marcador_local
                goles_rival = marcador_visitante
                goles_por_tiempo['local'] = 1
            else:
                goles_por_tiempo['visitante'] = 1
                goles_objetivo = marcador_visitante
                goles_rival = marcador_local

            # Si el equipo objetivo tiene más goles que el rival, ganó (1), si no, perdió o empató (0)
            if goles_objetivo > goles_rival:
                goles_por_tiempo['gano'] = 1
            elif goles_objetivo == goles_rival:
                goles_por_tiempo['empato'] = 1
            else:
                goles_por_tiempo['perdio'] = 1
            return goles_por_tiempo

        if equipo_objetivo == equipo_local:
            goles_objetivo = marcador_local
            goles_rival = marcador_visitante
            goles_por_tiempo['local'] = 1
        else:
            goles_por_tiempo['visitante'] = 1
            goles_objetivo = marcador_visitante
            goles_rival = marcador_local

        # Si el equipo objetivo tiene más goles que el rival, ganó (1), si no, perdió o empató (0)
        if goles_objetivo > goles_rival:
            goles_por_tiempo['gano'] = 1
        elif goles_objetivo == goles_rival:
            goles_por_tiempo['empato'] = 1
        else:
            goles_por_tiempo['perdio'] = 1
                
        # Buscar todos los eventos de goles directamente desde los spans
        eventos_goles = soup.find_all('span', class_='liveresults-sports-immersive__game-minute')

        # Limitar el recorrido solo a la cantidad de goles marcados
        goles_totales_en_partido = marcador_local + marcador_visitante
        eventos_goles = eventos_goles[:goles_totales_en_partido]  # Solo tomar el número exacto de eventos de goles

        # Procesar los eventos de goles
        for minuto_tag in eventos_goles:
            # Extraer el minuto del primer span hijo
            minuto = int(minuto_tag.find('span').text.strip())
            
            # Determinar a qué equipo pertenece el gol
            equipo_goleador = equipo_local if minuto_tag.find_parent('div', class_='imso_gs__left-team') else equipo_visitante
            
            if equipo_goleador == equipo_objetivo:
                if minuto <= 45:
                    goles_por_tiempo['goles_primera_mitad'] += 1
                else:
                    goles_por_tiempo['goles_segunda_mitad'] += 1

        # Calcular la cantidad total de goles
        goles_por_tiempo['goles_totales'] = goles_por_tiempo['goles_primera_mitad'] + goles_por_tiempo['goles_segunda_mitad']
        #goles_por_tiempo['goles_totales'] = goles_por_tiempo['goles_primera_mitad'] + goles_por_tiempo['goles_segunda_mitad']
        return goles_por_tiempo

    except Exception as e:
        print(f"Error al obtener goles para {equipo_objetivo}: {e}")
        return None

# Función para procesar las URLs
def procesar_urls(urls, equipo_objetivo):
    partido_stats = {}
    driver.get(urls[0])
    time.sleep(2.5)
    for idx, url in enumerate(urls, start=1):
        try:
            
            driver.get(url)
            time.sleep(2.5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            stats = obtener_estadisticas(soup, equipo_objetivo)
            goles_por_tiempo = obtener_goles_por_tiempo(soup, equipo_objetivo)
            goles_totales = goles_por_tiempo['goles_totales']
            remates = stats['Remates']
            remates_arco = stats['Remates al arco']
            posesion = stats['Posesión']
            tiros_esquina = stats['Tiros de esquina']
            pases = stats['Pases']

            goles_por_tiempo["conversion_goles"] = np.nan if remates == 0 else goles_totales / remates
            goles_por_tiempo["conversion_arco"] = np.nan if remates_arco == 0 else goles_totales / remates_arco
            stats["posesion_por_remate"] = np.nan if remates == 0 else goles_totales / remates
            stats["posesion_por_gol"] = np.nan if goles_totales == 0 else posesion / goles_totales
            stats["tirosEsquina_por_gol"] = np.nan if goles_totales == 0 else tiros_esquina / goles_totales
            goles_por_tiempo["goles_por_pase"] = np.nan if pases == 0 else goles_totales / pases
            goles_por_tiempo["remates_al_arco_por_gol"] = np.nan if goles_totales == 0 else remates / goles_totales
            if stats and goles_por_tiempo:
                partido_key = f"Partido #{idx}"
                partido_stats[partido_key] = {**stats, **goles_por_tiempo}
            else:
                print(f"El equipo {equipo_objetivo} no se encontró en la URL: {url}")
        except Exception as e:
            print(f"Error procesando la URL {url} para {equipo_objetivo}: {e}")
    return partido_stats


if not urls_equipo_1:
    # Cargar el CSV en un DataFrame
    df = pd.read_csv(f"{equipo_objetivo_1}.csv", parse_dates=['Fecha'], sep=";", encoding="utf-8")

    # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
    df = df.sort_values(by="Fecha", ascending=False)

    # Recorrer las filas del DataFrame
    for i, row in df.iterrows():
        partido_key = f"Partido #{i+1}"  # Generar "Partido #1", "Partido #2", etc.
        stats[equipo_objetivo_1][partido_key] = row.to_dict()  # Convertir la fila a diccionario
else:
    stats[equipo_objetivo_1] = procesar_urls(urls_equipo_1, equipo_objetivo_1)

if not urls_equipo_2:
    # Cargar el CSV en un DataFrame
    df = pd.read_csv(f"{equipo_objetivo_2}.csv", parse_dates=['Fecha'], sep=";", encoding="utf-8")

    # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
    df = df.sort_values(by="Fecha", ascending=False)

    # Recorrer las filas del DataFrame
    for i, row in df.iterrows():
        partido_key = f"Partido #{i+1}"  # Generar "Partido #1", "Partido #2", etc.
        stats[equipo_objetivo_2][partido_key] = row.to_dict()  # Convertir la fila a diccionario
else:
    stats[equipo_objetivo_2] = procesar_urls(urls_equipo_2, equipo_objetivo_2)

# Cerrar el navegador
driver.quit()




def calcular_desviacion_estandar_y_datos(stats):
    # Obtener los nombres de los equipos (las claves del diccionario)
    equipo1, equipo2 = list(stats.keys())
    # Asignar los partidos de cada equipo desde el diccionario
    partidos_equipo1 = dict(list(stats[equipo1].items())[:6])
    partidos_equipo2 = dict(list(stats[equipo2].items())[:6])
    p = len(partidos_equipo1)  # Número de partidos

    # Variables acumulativas para el equipo 1
    Tgoles, Tcorner, TrematesAr, Tremates, TtarjetasA, Tfaltas, Tpases, TgolesPT, TgolesST = 0, 0, 0, 0, 0, 0, 0, 0, 0
    goles_equipo1, corner_equipo1 = [], []

    # Variables acumulativas para el equipo 2
    Tgoles2, Tcorner2, TrematesAr2, Tremates2, TtarjetasA2, Tfaltas2, Tpases2, TgolesPT2, TgolesST2 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    goles_equipo2, corner_equipo2 = [], []

    # Acumular datos del equipo 1 y 2
    for partidosN in partidos_equipo1:
        partido = partidos_equipo1[partidosN]
        goles = partido['goles_totales']
        corner = partido['Tiros de esquina']
        remates_arco = partido['Remates al arco']
        remates = partido['Remates']
        tarjetas_amarillas = partido['Tarjetas amarillas']
        faltas = partido['Faltas']
        pases = partido['Pases']
        goles_primera_mitad = partido['goles_primera_mitad']
        goles_segunda_mitad = partido['goles_segunda_mitad']

        # Sumar estadísticas
        Tgoles += goles
        Tcorner += corner
        TrematesAr += remates_arco
        Tremates += remates
        TtarjetasA += tarjetas_amarillas
        Tfaltas += faltas
        Tpases += pases
        TgolesPT += goles_primera_mitad
        TgolesST += goles_segunda_mitad

        goles_equipo1.append(goles)
        corner_equipo1.append(corner)

    for partidosN in partidos_equipo2:
        partido = partidos_equipo2[partidosN]
        goles = partido['goles_totales']
        corner = partido['Tiros de esquina']
        remates_arco = partido['Remates al arco']
        remates = partido['Remates']
        tarjetas_amarillas = partido['Tarjetas amarillas']
        faltas = partido['Faltas']
        pases = partido['Pases']
        goles_primera_mitad = partido['goles_primera_mitad']
        goles_segunda_mitad = partido['goles_segunda_mitad']

        # Sumar estadísticas
        Tgoles2 += goles
        Tcorner2 += corner
        TrematesAr2 += remates_arco
        Tremates2 += remates
        TtarjetasA2 += tarjetas_amarillas
        Tfaltas2 += faltas
        Tpases2 += pases
        TgolesPT2 += goles_primera_mitad
        TgolesST2 += goles_segunda_mitad

        goles_equipo2.append(goles)
        corner_equipo2.append(corner)

    # Promedios
    Mean = Tgoles / p if p != 0 else 0
    Mean2 = Tgoles2 / p if p != 0 else 0
    MeanC = Tcorner / p if p != 0 else 0
    MeanC2 = Tcorner2 / p if p != 0 else 0

    # Desviación estándar y rangos
    if p != 0:
        Ds = math.sqrt(sum([(x - Mean) ** 2 for x in goles_equipo1]) / p)
        UVs, UVr = Mean + Ds, Mean - Ds
    else:
        UVs, UVr = Mean + 0, Mean - 0

    if p != 0:
        DsC = math.sqrt(sum([(x - MeanC) ** 2 for x in corner_equipo1]) / p)
        UVsC, UVrC = MeanC + DsC, MeanC - DsC
    else:
        UVsC, UVrC = MeanC + 0, MeanC - 0

    if p != 0:
        Ds2 = math.sqrt(sum([(x - Mean2) ** 2 for x in goles_equipo2]) / p)
        UVs2, UVr2 = Mean2 + Ds2, Mean2 - Ds2
    else:
        UVs2, UVr2 = Mean2 + 0, Mean2 - 0

    if p != 0:
        DsC2 = math.sqrt(sum([(x - MeanC2) ** 2 for x in corner_equipo2]) / p)
        UVsC2, UVrC2 = MeanC2 + DsC2, MeanC2 - DsC2
    else:
        UVsC2, UVrC2 = MeanC2 + 0, MeanC2 - 0
    # Imprimir los resultados
    print(f"{'-' * 40} DATOS DEL {equipo1} {'-' * 40}")
    
    Pcorner = (Tcorner / p) - 1
    print(f"{equipo1}: Cantidad de tiros de esquina esperados >> {Pcorner:.2f}")
    print(f"Rango de la desviación estándar de corners: {UVrC:.2f} ---- {MeanC:.2f} ---- {UVsC:.2f}")
    
    Pgoles = (Tgoles / p) - 1
    print(f"{equipo1}: Cantidad de goles esperados >> {Pgoles:.2f}")
    print(f"Rango de la desviación estándar de goles: {UVr:.2f} ---- {Mean:.2f} ---- {UVs:.2f}")
    
    Pgoles_aciertos = (Tgoles * 100) / TrematesAr
    print(f"{equipo1}: Probabilidad de aciertos en remates >> {Pgoles_aciertos:.2f}%")
    print(f"Probabilidad de fallar >> {100 - Pgoles_aciertos:.2f}%")
    
    Premates = (TrematesAr * 100) / Tremates
    print(f"{equipo1}: Porcentaje de balones al arco >> {Premates:.2f}%")
    print(f"Porcentaje de balones fuera del arco >> {100 - Premates:.2f}%")
    
    PtarjetasA = (TtarjetasA * 100) / Tfaltas
    print(f"{equipo1}: Probabilidad de recibir tarjetas amarillas >> {PtarjetasA:.2f}%")
    
    PposesionB = (Tpases * 100) / (Tpases + Tpases2)
    print(f"{equipo1}: Promedio de posesión del balón >> {PposesionB:.2f}%")
    
    PgolesPT = (TgolesPT / p) - 1
    print(f"{equipo1}: Goles esperados en la primera mitad >> {PgolesPT:.2f}")
    
    PgolesST = (TgolesST / p) - 1
    print(f"{equipo1}: Goles esperados en la segunda mitad >> {PgolesST:.2f}")
    
    print(f"{'-' * 40} DATOS DEL {equipo2} {'-' * 40}")
    
    Pcorner2 = (Tcorner2 / p) - 1
    print(f"{equipo2}: Cantidad de tiros de esquina esperados >> {Pcorner2:.2f}")
    print(f"Rango de la desviación estándar de corners: {UVrC2:.2f} ---- {MeanC2:.2f} ---- {UVsC2:.2f}")
    
    Pgoles2 = (Tgoles2 / p) - 1
    print(f"{equipo2}: Cantidad de goles esperados >> {Pgoles2:.2f}")
    print(f"Rango de la desviación estándar de goles: {UVr2:.2f} ---- {Mean2:.2f} ---- {UVs2:.2f}")
    
    Pgoles2_aciertos = (Tgoles2 * 100) / TrematesAr2
    print(f"{equipo2}: Probabilidad de aciertos en remates >> {Pgoles2_aciertos:.2f}%")
    print(f"Probabilidad de fallar >> {100 - Pgoles2_aciertos:.2f}%")
    
    Premates2 = (TrematesAr2 * 100) / Tremates2
    print(f"{equipo2}: Porcentaje de balones al arco >> {Premates2:.2f}%")
    print(f"Porcentaje de balones fuera del arco >> {100 - Premates2:.2f}%")
    
    PtarjetasA2 = (TtarjetasA2 * 100) / Tfaltas2
    print(f"{equipo2}: Probabilidad de recibir tarjetas amarillas >> {PtarjetasA2:.2f}%")
    
    PposesionB2 = (Tpases2 * 100) / (Tpases + Tpases2)
    print(f"{equipo2}: Promedio de posesión del balón >> {PposesionB2:.2f}%")
    
    PgolesPT2 = (TgolesPT2 / p) - 1
    print(f"{equipo2}: Goles esperados en la primera mitad >> {PgolesPT2:.2f}")
    
    PgolesST2 = (TgolesST2 / p) - 1
    print(f"{equipo2}: Goles esperados en la segunda mitad >> {PgolesST2:.2f}")

    return Mean, Mean2

# 1. Convertir el diccionario de stats a DataFrame
def convertir_a_dataframes_por_equipo(stats):
    equipos_dataframes = {}
    for equipo, partidos in stats.items():
        datos = []
        for partido, estadisticas in partidos.items():
            fila = estadisticas
            datos.append(fila)
        equipos_dataframes[equipo] = pd.DataFrame(datos)  # Crear un DataFrame por equipo
    return equipos_dataframes

    #Manejo de csv
# Crear un DataFrame por equipo y devolver los DataFrames al final
def crear_y_retornar_dataframes(stats):
    equipos_dataframes = {}
    for equipo, partidos in stats.items():
        # Generar el nombre del archivo con el nombre del equipo
        nombre_archivo = f"{equipo}.csv"

        # Verificar si el archivo ya existe
        if os.path.isfile(nombre_archivo):
            # Leer el archivo existente
            df_existente = pd.read_csv(nombre_archivo, parse_dates=['Fecha'], sep=';', quotechar='"')
            df_existente["Fecha"] = pd.to_datetime(df_existente["Fecha"])
            df_all = pd.read_csv("historial.csv", parse_dates=['Fecha'], sep=';', quotechar='"')
            df_all["Fecha"] = pd.to_datetime(df_all["Fecha"])

            # Crear un nuevo DataFrame con los nuevos datos
            datos = [estadisticas for estadisticas in partidos.values()]
            df_nuevo = pd.DataFrame(datos)
            df_nuevo["Fecha"] = pd.to_datetime(df_nuevo["Fecha"])

            # Concatenar los DataFrames
            df_stats = pd.concat([df_existente, df_nuevo], ignore_index=True)

            df_stats = df_stats.drop_duplicates(subset=["Fecha", "Equipo_name"], keep="first")
            # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
            df_stats = df_stats.sort_values(by="Fecha", ascending=False)

            df_all = pd.concat([df_all, df_stats], ignore_index=True)
            df_all = df_all.drop_duplicates(subset=["Fecha", "Equipo_name"], keep="first")
            # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
            df_all = df_all.sort_values(by="Fecha", ascending=False)
            df_all.to_csv("historial.csv", sep=';', index=False)
            
            df_stats.fillna(0, inplace=True)
            # Guardar el DataFrame actualizado en el archivo CSV
            df_stats.to_csv(nombre_archivo, sep=';', index=False)
        else:
            # Si no existe, crear el archivo con los datos nuevos
            datos = [estadisticas for estadisticas in partidos.values()]
            df_stats = pd.DataFrame(datos)

            df_all = pd.read_csv("historial.csv", parse_dates=['Fecha'], sep=';', quotechar='"')
            df_all["Fecha"] = pd.to_datetime(df_all["Fecha"])

            df_stats["Fecha"] = pd.to_datetime(df_stats["Fecha"])
            # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
            df_stats = df_stats.sort_values(by="Fecha", ascending=False)
            df_stats = df_stats.drop_duplicates(subset=["Fecha", "Equipo_name"], keep="first")
            
            df_all = pd.concat([df_all, df_stats], ignore_index=True)
            df_all = df_all.drop_duplicates(subset=["Fecha", "Equipo_name"], keep="first")
            # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
            df_all = df_all.sort_values(by="Fecha", ascending=False)
            df_stats.fillna(0, inplace=True)
            df_all.to_csv("historial.csv", sep=';', index=False)
            df_stats.to_csv(nombre_archivo, sep=';', index=False)

        # Guardar el DataFrame en el diccionario
        equipos_dataframes[equipo] = df_stats

    return equipos_dataframes

# Crear un DataFrame por equipo y devolver los DataFrames al final
def crear_y_retornar_dataframes_all():
    # Generar el nombre del archivo con el nombre del equipo
    nombre_archivo = "historial.csv"

    # Verificar si el archivo ya existe
    if os.path.isfile(nombre_archivo):
        # Leer el archivo existente
        df_stats = pd.read_csv(nombre_archivo, parse_dates=['Fecha'], sep=';', quotechar='"')
        df_stats["Fecha"] = pd.to_datetime(df_stats["Fecha"])

        df_stats = df_stats.drop_duplicates(subset=["Fecha", "Equipo_name"], keep="first")
        # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
        df_stats = df_stats.sort_values(by="Fecha", ascending=False)
        df_stats.fillna(0, inplace=True)
        # Guardar el DataFrame actualizado en el archivo CSV
        df_stats.to_csv(nombre_archivo, sep=';', index=False)

    # Guardar el DataFrame en el diccionario
    return df_stats

equipos_dataframes = crear_y_retornar_dataframes(stats)
equipos_dataframes_all = crear_y_retornar_dataframes_all()
Alineacion_local = equipos_dataframes[equipo_objetivo_1].iloc[0]["Alineacion"] #se asignan alineacion mas reciente
Alineacion_visitante = equipos_dataframes[equipo_objetivo_2].iloc[0]["Alineacion"] #se asignan alineacion mas reciente

columnas_a_excluir = ['gano', 'Tiros de esquina', 'perdio', 'empato', 'Fecha', 'Equipo_name', 'equipo_contrincante_name']
valores_y = ['gano', 'Tiros de esquina', 'perdio', 'empato']
valores_y_categoricas = ['gano', 'perdio', 'empato']
valores_y_continuas = ['Tiros de esquina']
#--------------------------------------------------------------------------------Equipo local modelo predictivo
# 2. Preparar los datos para el modelo del equipo local
# Seleccionamos las columnas con estadísticas y el objetivo
x = equipos_dataframes_all.drop(columns=columnas_a_excluir)
y = equipos_dataframes_all[valores_y]

# Dividir las variables de salida (Y)
y_categoricas = y[valores_y_categoricas]
y_continuas = y[valores_y_continuas]

# Dividir los datos en conjunto de entrenamiento y prueba
x_train, x_test, y_train_categoricas, y_test_categoricas = train_test_split(x, y_categoricas, test_size=0.2, random_state=42)
_, _, y_train_continuas, y_test_continuas = train_test_split(x, y_continuas, test_size=0.2, random_state=42)

# Parámetros para XGBoost
param_grid_xgb = {
    'estimator__n_estimators': [150, 200, 300],
    'estimator__max_depth': [3, 5, 7],
    'estimator__learning_rate': [0.01, 0.1, 0.2],
    'estimator__subsample': [0.8, 1]
}

# Modelo base
xgb_base = XGBClassifier(random_state=21, eval_metric='logloss')
# MultiOutputClassifier para manejar múltiples salidas categóricas
multi_output_xgb = MultiOutputClassifier(xgb_base, n_jobs=-1)

# GridSearchCV con MultiOutputClassifier
model_clasificacion = GridSearchCV(multi_output_xgb, param_grid_xgb, cv=3, n_jobs=-1)
model_clasificacion.fit(x_train, y_train_categoricas)

print("\nMejor estimador:", model_clasificacion.best_estimator_)
print("Mejor score:", model_clasificacion.best_score_)

param_grid_regressor = {
    'n_estimators': [300],  # Menos valores
    'learning_rate': [0.05],  # Menos valores
    'max_depth': [3],  # Menos valores
    'subsample': [1.0],  # Menos valores
    'colsample_bytree': [1.0],  # Menos valores
    'reg_alpha': [0],  # Menos valores
    'reg_lambda': [0]  # Menos valores
}

xgb = XGBRegressor(random_state=42)
grid_search = GridSearchCV(xgb, param_grid_regressor, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
grid_search.fit(x_train, y_train_continuas)

# Mejor combinación de hiperparámetros
print("Mejores parámetros:", grid_search.best_params_)

# Modelo final con los mejores hiperparámetros
model_regresion = grid_search.best_estimator_
#plot_importance(model_regresion)
#plt.show()

#--------------------------------------Predecir si ganara con datos de un partido que ya ocurrio
# Predecir si ganará el próximo partido (usando nuevas estadísticas)
# Inicializar diccionarios para almacenar las estadísticas agregadas
estadisticas_equipo1 = {
    'Remates': 0,
    'Remates al arco': 0,
    'Pases': 0,
    'Faltas': 0,
    'Tarjetas amarillas': 0,
    'Tarjetas rojas': 0,
    'goles_primera_mitad': 0,
    'goles_segunda_mitad': 0,
    'Posesión': 0,
    'Precisión de los pases': 0, 
    'visitante': 0, 
    'local': 1, #Se inicializa en 1 porque el equipo 1 siempre va ser el local y el equipo 2 el visitante
    'Torneo': Torneo,
    'Alineacion': Alineacion_local,
    'equipo': equipo_objetivo_1_ID,
    'equipo_contrincante': equipo_objetivo_2_ID,
    'goles_totales': 0,
    'Alineacion_contrincante': Alineacion_visitante,
    'Tiros de esquina': 0,
    'Tiros de esquina_concedidos': 0
}

estadisticas_equipo2 = {
    'Remates': 0,
    'Remates al arco': 0,
    'Pases': 0,
    'Faltas': 0,
    'Tarjetas amarillas': 0,
    'Tarjetas rojas': 0,
    'goles_primera_mitad': 0,
    'goles_segunda_mitad': 0,
    'Posesión': 0,
    'Precisión de los pases': 0, 
    'visitante': 1, #Se inicializa en 1 porque el equipo 2 siempre va ser el visitante y el equipo 1 el local
    'local': 0, #Se inicializa en 1 porque el equipo 1 siempre va ser el local y el equipo 2 el visitante
    'Torneo': Torneo,
    'Alineacion': Alineacion_visitante,
    'equipo': equipo_objetivo_2_ID,
    'equipo_contrincante': equipo_objetivo_1_ID,
    'goles_totales': 0,
    'Alineacion_contrincante': Alineacion_local,
    'Tiros de esquina': 0,
    'Tiros de esquina_concedidos': 0
}

equipo1, equipo2 = list(stats.keys())
#Imprime probabilidad estadisticas de solo los primeros 6 partidos
calcular_desviacion_estandar_y_datos(stats)

# Función para calcular promedio ponderado
def weighted_average(values, weights):
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)

# Asignar pesos más altos a partidos recientes
pesos = [1.5, 1.3, 1.1, 0.9, 0.7, 0.5]  # Puedes ajustar según cuántos partidos quieras considerar

# Promedios ponderados para las estadísticas
estadisticas_equipo1['Remates'] = weighted_average(
    [stats_partido['Remates'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Remates al arco'] = weighted_average(
    [stats_partido['Remates al arco'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Pases'] = weighted_average(
    [stats_partido['Pases'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Faltas'] = weighted_average(
    [stats_partido['Faltas'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tarjetas amarillas'] = weighted_average(
    [stats_partido['Tarjetas amarillas'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tarjetas rojas'] = weighted_average(
    [stats_partido['Tarjetas rojas'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['goles_primera_mitad'] = weighted_average(
    [stats_partido['goles_primera_mitad'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['goles_segunda_mitad'] = weighted_average(
    [stats_partido['goles_segunda_mitad'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Posesión'] = weighted_average(
    [stats_partido['Posesión'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Precisión de los pases'] = weighted_average(
    [stats_partido['Precisión de los pases'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tiros de esquina'] = weighted_average(
    [stats_partido['Tiros de esquina'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tiros de esquina_concedidos'] = weighted_average(
    [stats_partido['Tiros de esquina_concedidos'] for stats_partido in stats[equipo1].values()],
    pesos
)


# Repetir para el equipo 2
estadisticas_equipo2['Remates'] = weighted_average(
    [stats_partido['Remates'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Remates al arco'] = weighted_average(
    [stats_partido['Remates al arco'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Pases'] = weighted_average(
    [stats_partido['Pases'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Faltas'] = weighted_average(
    [stats_partido['Faltas'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tarjetas amarillas'] = weighted_average(
    [stats_partido['Tarjetas amarillas'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tarjetas rojas'] = weighted_average(
    [stats_partido['Tarjetas rojas'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['goles_primera_mitad'] = weighted_average(
    [stats_partido['goles_primera_mitad'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['goles_segunda_mitad'] = weighted_average(
    [stats_partido['goles_segunda_mitad'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Posesión'] = weighted_average(
    [stats_partido['Posesión'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Precisión de los pases'] = weighted_average(
    [stats_partido['Precisión de los pases'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tiros de esquina'] = weighted_average(
    [stats_partido['Tiros de esquina'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tiros de esquina_concedidos'] = weighted_average(
    [stats_partido['Tiros de esquina_concedidos'] for stats_partido in stats[equipo2].values()],
    pesos
)

estadisticas_equipo1['Posesión_contrincante'] = estadisticas_equipo2["Posesión"]
estadisticas_equipo2['Posesión_contrincante'] = estadisticas_equipo1["Posesión"]
estadisticas_equipo1["Remates_contrincante"] = estadisticas_equipo2["Remates"]
estadisticas_equipo2["Remates_contrincante"] = estadisticas_equipo1["Remates"]
estadisticas_equipo1["Promedio_Tiros de esquina_contrincante"] = estadisticas_equipo2["Tiros de esquina"]
estadisticas_equipo2["Promedio_Tiros de esquina_contrincante"] = estadisticas_equipo1["Tiros de esquina"]
estadisticas_equipo1["tarjetas"] = estadisticas_equipo1["Tarjetas amarillas"] + estadisticas_equipo1["Tarjetas rojas"]
estadisticas_equipo2["tarjetas"] = estadisticas_equipo2["Tarjetas amarillas"] + estadisticas_equipo2["Tarjetas rojas"]
estadisticas_equipo1["tarjetas_contrincante"] = estadisticas_equipo2["tarjetas"]
estadisticas_equipo2["tarjetas_contrincante"] = estadisticas_equipo1["tarjetas"]
estadisticas_equipo1["Faltas_contrincante"] = estadisticas_equipo2["Faltas"]
estadisticas_equipo2["Faltas_contrincante"] = estadisticas_equipo1["Faltas"]

estadisticas_equipo1['Posesión_contra_por_remate'] = estadisticas_equipo1["Posesión_contrincante"] / estadisticas_equipo1["Remates_contrincante"]
estadisticas_equipo1["tarjetas_por_falta"] = estadisticas_equipo1["tarjetas"] / estadisticas_equipo1["Faltas"]
estadisticas_equipo1["pases_completados"] = round((estadisticas_equipo1["Pases"] * estadisticas_equipo1["Precisión de los pases"]))
estadisticas_equipo1["faltas_por_pases"] = estadisticas_equipo1["Faltas"]/estadisticas_equipo1["pases_completados"]
estadisticas_equipo1["pases_por_posesion"] = estadisticas_equipo1["pases_completados"]/estadisticas_equipo1["Posesión"]
estadisticas_equipo1["tirosEsquina_por_remate"] = estadisticas_equipo1["Tiros de esquina"]/estadisticas_equipo1["Remates"]
estadisticas_equipo1["tirosEsquina_por_posesion"] = estadisticas_equipo1["Tiros de esquina"]/estadisticas_equipo1["Posesión"]
estadisticas_equipo1["diff_remates"] = estadisticas_equipo1["Remates"] - estadisticas_equipo1["Remates_contrincante"]
estadisticas_equipo1["diff_posesion"] = estadisticas_equipo1["Posesión"] - estadisticas_equipo1["Posesión_contrincante"]
estadisticas_equipo1["diff_Tiros de esquina"] = estadisticas_equipo1["Tiros de esquina"] - estadisticas_equipo1["Promedio_Tiros de esquina_contrincante"]
estadisticas_equipo1["diff_tarjetas"] = estadisticas_equipo1["tarjetas"] - estadisticas_equipo1["tarjetas_contrincante"]
estadisticas_equipo1["diff_faltas"] = estadisticas_equipo1["Faltas"] - estadisticas_equipo1["Faltas_contrincante"]
estadisticas_equipo1["remates_por_pase"] = estadisticas_equipo1["Remates"]/estadisticas_equipo1["Pases"]
estadisticas_equipo1['goles_totales'] = estadisticas_equipo1['goles_primera_mitad'] + estadisticas_equipo1['goles_segunda_mitad']
estadisticas_equipo1['remates_al_arco_por_gol'] = estadisticas_equipo1["Remates"] / estadisticas_equipo1["goles_totales"]   
estadisticas_equipo1['goles_por_pase'] = estadisticas_equipo1["goles_totales"] /estadisticas_equipo1["Pases"]
estadisticas_equipo1['tirosEsquina_por_gol'] = estadisticas_equipo1["Tiros de esquina"]/estadisticas_equipo1["goles_totales"]
estadisticas_equipo1['posesion_por_gol'] = estadisticas_equipo1["Posesión"]/estadisticas_equipo1["goles_totales"]
estadisticas_equipo1['posesion_por_remate'] = estadisticas_equipo1["goles_totales"]/estadisticas_equipo1["Remates"]
estadisticas_equipo1['conversion_arco'] = estadisticas_equipo1["goles_totales"]/estadisticas_equipo1["Remates al arco"]
estadisticas_equipo1['conversion_goles'] = estadisticas_equipo1["goles_totales"]/estadisticas_equipo1["Remates"]


estadisticas_equipo2['Posesión_contra_por_remate'] = estadisticas_equipo2["Posesión_contrincante"] / estadisticas_equipo2["Remates_contrincante"]
estadisticas_equipo2["tarjetas_por_falta"] = estadisticas_equipo2["tarjetas"] / estadisticas_equipo2["Faltas"]
estadisticas_equipo2["pases_completados"] = round((estadisticas_equipo2["Pases"] * estadisticas_equipo2["Precisión de los pases"]))
estadisticas_equipo2["faltas_por_pases"] = estadisticas_equipo2["Faltas"]/estadisticas_equipo2["pases_completados"]
estadisticas_equipo2["pases_por_posesion"] = estadisticas_equipo2["pases_completados"]/estadisticas_equipo2["Posesión"]
estadisticas_equipo2["tirosEsquina_por_remate"] = estadisticas_equipo2["Tiros de esquina"]/estadisticas_equipo2["Remates"]
estadisticas_equipo2["tirosEsquina_por_posesion"] = estadisticas_equipo2["Tiros de esquina"]/estadisticas_equipo2["Posesión"]
estadisticas_equipo2["diff_remates"] = estadisticas_equipo2["Remates"] - estadisticas_equipo2["Remates_contrincante"]
estadisticas_equipo2["diff_posesion"] = estadisticas_equipo2["Posesión"] - estadisticas_equipo2["Posesión_contrincante"]
estadisticas_equipo2["diff_Tiros de esquina"] = estadisticas_equipo2["Tiros de esquina"] - estadisticas_equipo2["Promedio_Tiros de esquina_contrincante"]
estadisticas_equipo2["diff_tarjetas"] = estadisticas_equipo2["tarjetas"] - estadisticas_equipo2["tarjetas_contrincante"]
estadisticas_equipo2["diff_faltas"] = estadisticas_equipo2["Faltas"] - estadisticas_equipo2["Faltas_contrincante"]
estadisticas_equipo2["remates_por_pase"] = estadisticas_equipo2["Remates"]/estadisticas_equipo2["Pases"]          
estadisticas_equipo2['goles_totales'] = estadisticas_equipo2['goles_primera_mitad'] + estadisticas_equipo2['goles_segunda_mitad']
estadisticas_equipo2['remates_al_arco_por_gol'] = estadisticas_equipo2["Remates"] / estadisticas_equipo2["goles_totales"]
estadisticas_equipo2['goles_por_pase'] = estadisticas_equipo2["goles_totales"] /estadisticas_equipo2["Pases"]
estadisticas_equipo2['tirosEsquina_por_gol'] = estadisticas_equipo2["Tiros de esquina"]/estadisticas_equipo2["goles_totales"]
estadisticas_equipo2['posesion_por_gol'] = estadisticas_equipo2["Posesión"]/estadisticas_equipo2["goles_totales"]
estadisticas_equipo2['posesion_por_remate'] = estadisticas_equipo2["goles_totales"]/estadisticas_equipo2["Remates"]
estadisticas_equipo2['conversion_arco'] = estadisticas_equipo2["goles_totales"]/estadisticas_equipo2["Remates al arco"]
estadisticas_equipo2['conversion_goles'] = estadisticas_equipo2["goles_totales"]/estadisticas_equipo2["Remates"]

del estadisticas_equipo1['Tiros de esquina']
del estadisticas_equipo2['Tiros de esquina']
#COMIENZO DEL DATAFRAME
estadisticas_equipo1_df = pd.DataFrame([estadisticas_equipo1])
estadisticas_equipo2_df = pd.DataFrame([estadisticas_equipo2])

# Columnas a excluir
columnas_a_excluir = ['Fecha', 'Equipo_name', 'Torneo', 'Alineacion', 'Alineacion_contrincante', 'equipo', 'equipo_contrincante', 'equipo_contrincante_name', 
'Remates', 'Remates al arco', 'Posesión', 'Pases', 'Precisión de los pases', 'Faltas', 'Tarjetas amarillas', 'Tarjetas rojas', 'Tiros de esquina', 'goles_primera_mitad', 
'goles_segunda_mitad', 'goles_totales', 'gano', 'empato', 'perdio', 'visitante', 'local', 'Posesión_contrincante','Remates_contrincante','Tiros de esquina_concedidos',
'tarjetas','tarjetas_contrincante','Faltas_contrincante','Posesión_contra_por_remate','tarjetas_por_falta','pases_completados','faltas_por_pases','pases_por_posesion',
'tirosEsquina_por_remate','tirosEsquina_por_posesion','diff_remates','diff_posesion','diff_Tiros de esquina','diff_tarjetas','diff_faltas','remates_por_pase','Promedio_Tiros de esquina_contrincante'
'goles_totales','remates_al_arco_por_gol','goles_por_pase','tirosEsquina_por_gol','posesion_por_gol','posesion_por_remate','conversion_arco','conversion_goles']

# Obtener solo los nombres de las columnas que queremos (excluyendo algunas)
columnas_filtradas = [col for col in equipos_dataframes_all.columns if col not in columnas_a_excluir]

# Crear un DataFrame con una fila llena de ceros y las columnas filtradas
df_nuevas_columnas = pd.DataFrame([[0] * len(columnas_filtradas)], columns=columnas_filtradas)

# Unir los DataFrames
estadisticas_equipo1_df = pd.concat([estadisticas_equipo1_df, df_nuevas_columnas], axis=1)
# Unir los DataFrames
estadisticas_equipo2_df = pd.concat([estadisticas_equipo2_df, df_nuevas_columnas], axis=1)

torneo_name = next((k for k, v in torneos_dict.items() if v == Torneo), None)
alineaciones = getAlineacion().getAlineaciones({"name_equipo":equipo1,"name_visitante_equipo":equipo2,"torneo":torneo_name})

# Obtener jugadores del equipo local
jugadores_locales = alineaciones["local"]
jugadores_visitantes = alineaciones["visitante"]
#codigo que buscara los jugadores y le pondra 1 pensando en la alineacion: 
# Asignar 1 a los jugadores en la alineación
for jugador in jugadores_locales:
    if (estadisticas_equipo1_df['equipo'] == estadisticas_equipo1["equipo"]).any():
        if len(jugador.split()[0]) > 3:
            # Convertimos el nombre del jugador a ASCII (sin tildes) para la búsqueda
            nombre_jugador = unidecode(jugador.split()[0])
        else:
            nombre_jugador = unidecode(jugador.split()[1])
        
        # Regex modificada para buscar coincidencias sin importar tildes
        regex_busqueda = f"(?i)^.*{re.escape(nombre_jugador)}.*{re.escape(equipo1)}.*$"
        
        # Buscamos en todas las columnas (convertimos a ASCII para comparar)
        columnas_coincidentes = [
            col for col in estadisticas_equipo1_df.columns 
            if re.match(regex_busqueda, unidecode(col))
        ]
        
        if columnas_coincidentes:
            estadisticas_equipo1_df.loc[0, columnas_coincidentes] = 1

for jugador in jugadores_visitantes:
    if (estadisticas_equipo2_df['equipo'] == estadisticas_equipo2["equipo"]).any():
        if len(jugador.split()[0]) > 3:
            # Convertimos el nombre del jugador a ASCII (sin tildes) para la búsqueda
            nombre_jugador = unidecode(jugador.split()[0])
        else:
            nombre_jugador = unidecode(jugador.split()[1])
        
        # Regex modificada para buscar coincidencias sin importar tildes
        regex_busqueda = f"(?i)^.*{re.escape(nombre_jugador)}.*{re.escape(equipo2)}.*$"
        
        # Buscamos en todas las columnas (convertimos a ASCII para comparar)
        columnas_coincidentes = [
            col for col in estadisticas_equipo1_df.columns 
            if re.match(regex_busqueda, unidecode(col))
        ]
        
        if columnas_coincidentes:
            estadisticas_equipo2_df.loc[0, columnas_coincidentes] = 1

estadisticas_equipo1_df = estadisticas_equipo1_df[x_train.columns]
estadisticas_equipo2_df = estadisticas_equipo2_df[x_train.columns]


estadisticas_equipo1_df['Torneo'] = df['Torneo'].astype('category')
estadisticas_equipo1_df['Alineacion'] = df['Alineacion'].astype('category')
estadisticas_equipo1_df['Alineacion_contrincante'] = df['Alineacion_contrincante'].astype('category')
estadisticas_equipo1_df['equipo'] = df['equipo'].astype('category')
estadisticas_equipo1_df['equipo_contrincante'] = df['equipo_contrincante'].astype('category')

estadisticas_equipo2_df['Torneo'] = df['Torneo'].astype('category')
estadisticas_equipo2_df['Alineacion'] = df['Alineacion'].astype('category')
estadisticas_equipo2_df['Alineacion_contrincante'] = df['Alineacion_contrincante'].astype('category')
estadisticas_equipo2_df['equipo'] = df['equipo'].astype('category')
estadisticas_equipo2_df['equipo_contrincante'] = df['equipo_contrincante'].astype('category')

# Predicciones categóricas
predicciones_categoricas_equipo1 = model_clasificacion.predict(estadisticas_equipo1_df)
predicciones_probabilidades_equipo1 = model_clasificacion.predict_proba(estadisticas_equipo1_df)

predicciones_categoricas_equipo2 = model_clasificacion2.predict(estadisticas_equipo2_df)
predicciones_probabilidades_equipo2 = model_clasificacion2.predict_proba(estadisticas_equipo2_df)

# Predicciones continuas (Tiros de esquina, goles_totales)
predicciones_continuas_equipo1 = model_regresion.predict(estadisticas_equipo1_df)
predicciones_continuas_equipo2 = model_regresion2.predict(estadisticas_equipo2_df)

# Precisión del modelo
y_pred_categoricas = model_clasificacion.predict(x_test)
y_pred_continuas = model_regresion.predict(x_test)

# Precisión del modelo visitante
y_pred_categoricas2 = model_clasificacion2.predict(x_test2)
y_pred_continuas2 = model_regresion2.predict(x_test2)

# Evaluación de las variables continuas (regresión) local 
mse_continuas = root_mean_squared_error(y_test_continuas, y_pred_continuas)
mae_continuas = mean_absolute_error(y_test_continuas, y_pred_continuas)
r2_continuas = r2_score(y_test_continuas, y_pred_continuas)

# Evaluación de las variables continuas (regresión) visitante
mse_continuas2= root_mean_squared_error(y_test_continuas2, y_pred_continuas2)
mae_continuas2 = mean_absolute_error(y_test_continuas2, y_pred_continuas2)
r2_continuas2 = r2_score(y_test_continuas2, y_pred_continuas2)

print("\n\nEvaluacion del modelo y probabilidad de aciertos en datos de prueba\n")
#Evaluación del modelo
#categoricas
#local
accuracy_clasificacion = accuracy_score(y_test_categoricas, y_pred_categoricas)
print(f'\nPrecisión categoricas del local: {accuracy_clasificacion:.3f}')

#visitante
accuracy_clasificacion2 = accuracy_score(y_test_categoricas2, y_pred_categoricas2)
print(f'\nPrecisión categoricas del visitante: {accuracy_clasificacion2:.3f}')


#continuas local
print(f'\nError cuadrático medio (RMSE) continuas del local: {mse_continuas:.3f}')
print(f'Error cuadrático medio (MSE) continuas al cuadrado del local: {math.pow(mse_continuas,2):.3f}')
print(f'Error absoluto medio (MAE) continuas del local: {mae_continuas:.3f}')
print(f'Coeficiente de determinación (R2) continuas del local: {r2_continuas:.3f}')

#continuas visitante
print(f'\nError cuadrático medio (RMSE) continuas del visitante: {mse_continuas2:.3f}')
print(f'Error cuadrático medio (MSE) continuas al cuadrado del visitante: {math.pow(mse_continuas2,2):.3f}')
print(f'Error absoluto medio (MAE) continuas del visitante: {mae_continuas2:.3f}')
print(f'Coeficiente de determinación (R2) continuas del visitante: {r2_continuas2:.3f}')


print("\n-----------------PREDICCIONES DEL", equipo_objetivo_1, "-----------------")
for idx, variable in enumerate(y_categoricas.columns):
    probabilidad = predicciones_probabilidades_equipo1[idx]

    if len(probabilidad[0]) == 1:
        prob = probabilidad[0][0]
        print(f"{variable}: Predicción segura, Probabilidad: {prob:.2f}")
    else:
        prob_0 = probabilidad[0][0]
        prob_1 = probabilidad[0][1]
        print(f"{variable}: Predicción: {predicciones_categoricas_equipo1[0][idx]} "
              f"(Prob. clase 0: {prob_0:.2f}, Prob. clase 1: {prob_1:.2f})")

# Predicciones continuas sin tener en encuenta los jugadores (Tiros de esquina, goles_totales)
for idx, variable in enumerate(y_continuas.columns):
    prediccion = predicciones_continuas_equipo1[idx]
    prediccion_menos_mse = prediccion - mse_continuas
    prediccion_mas_mse = prediccion + mse_continuas
    print(f"{variable}: Predicción: {prediccion_menos_mse:.2f} ---- {prediccion:.2f} ---- {prediccion_mas_mse:.2f}")


print("\n-----------------PREDICCIONES DEL", equipo_objetivo_2, "-----------------")
for idx, variable in enumerate(y_categoricas2.columns):
    probabilidad = predicciones_probabilidades_equipo2[idx]

    if len(probabilidad[0]) == 1:
        prob = probabilidad[0][0]
        print(f"{variable}: Predicción segura, Probabilidad: {prob:.2f}")
    else:
        prob_0 = probabilidad[0][0]
        prob_1 = probabilidad[0][1]
        print(f"{variable}: Predicción: {predicciones_categoricas_equipo2[0][idx]} "
              f"(Prob. clase 0: {prob_0:.2f}, Prob. clase 1: {prob_1:.2f})")

# Predicciones continuas sin tener en encuenta los jugadores (Tiros de esquina, goles_totales)
for idx, variable in enumerate(y_continuas2.columns):
    prediccion2 = predicciones_continuas_equipo2[idx]
    prediccion_menos_mse2 = prediccion2 - mse_continuas2
    prediccion_mas_mse2 = prediccion2 + mse_continuas2
    print(f"{variable}: Predicción: {prediccion_menos_mse2:.2f} ---- {prediccion2:.2f} ---- {prediccion_mas_mse2:.2f}")
#-------------------------------------Predecir si ganara con datos de un partido que ya ocurrio
#local porcentajes
y_test_continuas = y_test_continuas.iloc[:, 0]
# Errores reales
errores = y_pred_continuas - y_test_continuas

# Porcentaje dentro del rango ±RMSE
porc_en_rango = np.mean(np.abs(errores) <= mse_continuas) * 100

# Porcentaje que se pasó por más de RMSE
porc_encima = np.mean(errores > mse_continuas) * 100

# Porcentaje que se quedó corto por más de RMSE
porc_debajo = np.mean(errores < -mse_continuas) * 100

# Mostrar resultados
print(f"\n\nPredicciones dentro del rango ±{mse_continuas:.2f}: {porc_en_rango:.2f}%")
print(f"Predicciones que sobreestimaron el valor real en más de {mse_continuas:.2f}: {porc_encima:.2f}%")
print(f"Predicciones que subestimaron el valor real en más de {mse_continuas:.2f}: {porc_debajo:.2f}%")

#Impresion de errores mas alto bajo y alto
# Índice de mayor sobreestimación
idx_max_sobre = np.argmax(errores)
# Índice de mayor subestimación
idx_max_sub = np.argmin(errores)

# Mostrar detalles
print("\n--- Mayor sobreestimación ---")
print(f"Valor real      : {y_test_continuas.iloc[idx_max_sobre]:.2f}")
print(f"Predicción      : {y_pred_continuas[idx_max_sobre]:.2f}")
print(f"Error (↑)       : {errores.iloc[idx_max_sobre]:.2f}")

print("\n--- Mayor subestimación ---")
print(f"Valor real      : {y_test_continuas.iloc[idx_max_sub]:.2f}")
print(f"Predicción      : {y_pred_continuas[idx_max_sub]:.2f}")
print(f"Error (↓)       : {errores.iloc[idx_max_sub]:.2f}")


#visitantes porcentajes
y_test_continuas2 = y_test_continuas2.iloc[:, 0]
# Errores reales
errores2 = y_pred_continuas2 - y_test_continuas2

# Porcentaje dentro del rango ±RMSE
porc_en_rango2 = np.mean(np.abs(errores2) <= mse_continuas2) * 100

# Porcentaje que se pasó por más de RMSE
porc_encima2 = np.mean(errores2 > mse_continuas2) * 100

# Porcentaje que se quedó corto por más de RMSE
porc_debajo2 = np.mean(errores2 < -mse_continuas2) * 100

# Mostrar resultados
print(f"\n\nPredicciones dentro del rango visitante ±{mse_continuas2:.2f}: {porc_en_rango2:.2f}%")
print(f"Predicciones que sobreestimaron el valor real en más de visitante {mse_continuas2:.2f}: {porc_encima2:.2f}%")
print(f"Predicciones que subestimaron el valor real en más de visitante {mse_continuas2:.2f}: {porc_debajo2:.2f}%")

#Impresion de errores mas alto bajo y alto
# Índice de mayor sobreestimación
idx_max_sobre2 = np.argmax(errores2)
# Índice de mayor subestimación
idx_max_sub2 = np.argmin(errores2)

# Mostrar detalles
print("\n--- Mayor sobreestimación visitante ---")
print(f"Valor real      : {y_test_continuas2.iloc[idx_max_sobre2]:.2f}")
print(f"Predicción      : {y_pred_continuas2[idx_max_sobre2]:.2f}")
print(f"Error (↑)       : {errores2.iloc[idx_max_sobre2]:.2f}")

print("\n--- Mayor subestimación visitante ---")
print(f"Valor real      : {y_test_continuas2.iloc[idx_max_sub2]:.2f}")
print(f"Predicción      : {y_pred_continuas2[idx_max_sub2]:.2f}")
print(f"Error (↓)       : {errores2.iloc[idx_max_sub2]:.2f}")