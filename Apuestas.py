#Como la regresion logistica necesita mas de 1 variable para predecir el futuro, necesitamos que ya sea en los partidos del local o el visitante alla al un partido donde gane y otro donde pierda. si no da error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import math
import pandas as pd
import os
from RecoleccionEquipos import EquipmentCollection
from selenium.webdriver.chrome.options import Options
from getMatch import getMatch
import sys
from datetime import datetime, timedelta

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
equipo_objetivo_1 = "Racing de Estrasburgo"#input("Ingresa el primer equipo objetivo: ")
equipo_objetivo_2 = "Lyon"#input("Ingresa el segundo equipo objetivo: ")

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

Torneo = 2 #Torneo de partido a predecir, para saber que numero poner, vaya a bajo en el diccionario torneo

if equipos_dict.get(equipo_objetivo_1, -1) == -1:
    raise Exception(f"El equipo {equipo_objetivo_1} no existe en la base de datos, por favor agregarlo")
if equipos_dict.get(equipo_objetivo_2, -1) == -1:
    raise Exception(f"El equipo {equipo_objetivo_2} no existe  en la base de datos, por favor agregarlo")

equipo_objetivo_1_ID = equipos_dict.get(equipo_objetivo_1, -1)
equipo_objetivo_2_ID = equipos_dict.get(equipo_objetivo_2, -1)
# Diccionario de torneos
torneos_dict = {
    "Champions League": 0,
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

#Alineacion de partido a predecir, para saber que numero poner, vaya al metodo obtener estadisticas en el diccionario Alineaciones
Alineacion_local = 17
Alineacion_visitante = 3
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
        rows = stats_table.select('tr.MzWkAb')
        for row in rows:
            stat_name = row.find('th').text
            if stat_name not in estadisticas_excluidas:
                stat_value = int(row.find_all('td')[equipo_objetivo_columna].text.strip().replace('%', ''))
                partido_stats[stat_name] = stat_value        

        formacion_local_div = soup.find('div', class_= 'lrvl-tlt lrvl-tl lrvl-btrc')
        formacion_visitante_div = soup.find('div', class_= 'lrvl-tlt lrvl-tl lrvl-bbrc')
        jugadores_formacion_local_div = formacion_local_div.find_all('div', class_= 'A9ad7e imso-loa')
        jugadores_formacion_visitante_div = formacion_visitante_div.find_all('div', class_= 'A9ad7e imso-loa')
        
        if local == 0:
            for i, jugador_span in enumerate(jugadores_formacion_local_div, start= 1):
                jugador = jugador_span.find_all('span')
                partido_stats[f"jugador {i}"] = jugador[1].get('aria-label')
                partido_stats[f"posicion jugador {i}"] = jugador[2].get('aria-label')
        else:
            for i, jugador_span in enumerate(jugadores_formacion_visitante_div[::-1], start=1):
                jugador = jugador_span.find_all('span')
                partido_stats[f"jugador {i}"] = jugador[1].get('aria-label')
                partido_stats[f"posicion jugador {i}"] = jugador[2].get('aria-label')

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
    df = pd.read_csv(f"{equipo_objetivo_1}.csv", parse_dates=['Fecha'], dayfirst=True, sep=";", encoding="utf-8")

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
    df = pd.read_csv(f"{equipo_objetivo_2}.csv", parse_dates=['Fecha'], dayfirst=True, sep=";", encoding="utf-8")

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
            df_existente = pd.read_csv(nombre_archivo, parse_dates=['Fecha'], dayfirst=True, sep=';', quotechar='"')

            # Crear un nuevo DataFrame con los nuevos datos
            datos = [estadisticas for estadisticas in partidos.values()]
            df_nuevo = pd.DataFrame(datos)

            # Concatenar los DataFrames
            df_stats = pd.concat([df_existente, df_nuevo], ignore_index=True)
            df_stats = df_stats.drop_duplicates(subset=["Fecha", "Equipo_name"], keep="first")

            # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
            df_stats = df_stats.sort_values(by="Fecha", ascending=False)

            # Guardar el DataFrame actualizado en el archivo CSV
            df_stats.to_csv(nombre_archivo, sep=';', index=False)
        else:
            # Si no existe, crear el archivo con los datos nuevos
            datos = [estadisticas for estadisticas in partidos.values()]
            df_stats = pd.DataFrame(datos)

            # Ordenar el DataFrame en orden descendente (fecha más reciente primero)
            df_stats = df_stats.sort_values(by="Fecha", ascending=False)
            df_stats.to_csv(nombre_archivo, sep=';', index=False)

        # Guardar el DataFrame en el diccionario
        equipos_dataframes[equipo] = df_stats

    return equipos_dataframes

equipos_dataframes = crear_y_retornar_dataframes(stats)

# Acceder al DataFrame de un equipo
df_equipo1 = equipos_dataframes[equipo_objetivo_1]
df_equipo2 = equipos_dataframes[equipo_objetivo_2]

valores_x = ['Remates', 'Remates al arco', 'Pases', 'Faltas', 'Tarjetas amarillas', 'Tarjetas rojas', 'goles_primera_mitad', 'goles_segunda_mitad', 'Posesión', 'Precisión de los pases', 'visitante', 'local', 'Torneo', 'Alineacion', 'equipo', 'equipo_contrincante', 'goles_totales', 'Alineacion_contrincante']
valores_y = ['gano', 'Tiros de esquina', 'perdio', 'empato']
valores_y_categoricas = ['gano', 'perdio', 'empato']
valores_y_continuas = ['Tiros de esquina']
#--------------------------------------------------------------------------------Equipo local modelo predictivo
# 2. Preparar los datos para el modelo del equipo local
# Seleccionamos las columnas con estadísticas y el objetivo
x = df_equipo1[valores_x]
y = df_equipo1[valores_y]

# Dividir las variables de salida (Y)
y_categoricas = y[valores_y_categoricas]
y_continuas = y[valores_y_continuas]

# Dividir los datos en conjunto de entrenamiento y prueba
x_train, x_test, y_train_categoricas, y_test_categoricas = train_test_split(x, y_categoricas, test_size=0.2, random_state=42)
_, _, y_train_continuas, y_test_continuas = train_test_split(x, y_continuas, test_size=0.2, random_state=42)

param_grid = {
    'criterion':['gini', 'entropy'],
    'n_estimators': [100, 250, 500],
    'min_samples_leaf':[5, 15, 25],
    'max_features': [3,5, 7,9]
}

# 1. Entrenar el modelo de clasificación para las variables categóricas

etc = ExtraTreesClassifier(random_state=21)
etc.fit(x_train, y_train_categoricas)

model_clasificacion = GridSearchCV(etc, param_grid, cv=3, n_jobs=-1)
model_clasificacion.fit(x_train, y_train_categoricas)
print("\nthe best ", model_clasificacion.best_estimator_, " the best scors ", model_clasificacion.best_score_)

# 2. Entrenar el modelo de regresión para las variables continuas
regresor = ExtraTreesRegressor(n_estimators=150, random_state=42)
model_regresion = MultiOutputRegressor(regresor)
model_regresion.fit(x_train, y_train_continuas)

#--------------------------------------------------------------------------------Equipo visitante modelo predictivo
# 2. Preparar los datos para el modelo del equipo local
# Seleccionamos las columnas con estadísticas y el objetivo
x2 = df_equipo2[valores_x]
y2 = df_equipo2[valores_y]

# Dividir las variables de salida (Y)
y_categoricas2 = y2[valores_y_categoricas]
y_continuas2 = y2[valores_y_continuas]

# Dividir los datos en conjunto de entrenamiento y prueba
x_train2, x_test2, y_train_categoricas2, y_test_categoricas2 = train_test_split(x2, y_categoricas2, test_size=0.2, random_state=42)
_, _, y_train_continuas2, y_test_continuas2 = train_test_split(x2, y_continuas2, test_size=0.2, random_state=42)

# 1. Entrenar el modelo de clasificación para las variables categóricas

etc2 = ExtraTreesClassifier(random_state=21)
etc2.fit(x_train2, y_train_categoricas2)

model_clasificacion2 = GridSearchCV(etc2, param_grid, cv=3, n_jobs=-1)
model_clasificacion2.fit(x_train2, y_train_categoricas2)
print("\nthe best2 ", model_clasificacion2.best_estimator_, " the best scors2 ", model_clasificacion2.best_score_)

# 2. Entrenar el modelo de regresión para las variables continuas
regresor2 = ExtraTreesRegressor(n_estimators=150, random_state=42)
model_regresion2 = MultiOutputRegressor(regresor2)
model_regresion2.fit(x_train2, y_train_continuas2)



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
    'Alineacion_contrincante': Alineacion_visitante
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
    'Alineacion_contrincante': Alineacion_local
}

equipo1, equipo2 = list(stats.keys())
# Calcular estadísticas para el equipo 1
for partido, stats_partido in stats[equipo1].items():
    estadisticas_equipo1['Remates'] += stats_partido['Remates']
    estadisticas_equipo1['Remates al arco'] += stats_partido['Remates al arco']
    estadisticas_equipo1['Pases'] += stats_partido['Pases']
    estadisticas_equipo1['Faltas'] += stats_partido['Faltas']
    estadisticas_equipo1['Tarjetas amarillas'] += stats_partido['Tarjetas amarillas']
    estadisticas_equipo1['Tarjetas rojas'] += stats_partido['Tarjetas rojas']
    estadisticas_equipo1['goles_primera_mitad'] += stats_partido['goles_primera_mitad']
    estadisticas_equipo1['goles_segunda_mitad'] += stats_partido['goles_segunda_mitad']
    estadisticas_equipo1['Posesión'] += stats_partido['Posesión']
    estadisticas_equipo1['Precisión de los pases'] += stats_partido['Precisión de los pases']
    estadisticas_equipo1['goles_totales'] += stats_partido['goles_totales']

# Calcular estadísticas para el equipo 2
for partido, stats_partido in stats[equipo2].items():
    estadisticas_equipo2['Remates'] += stats_partido['Remates']
    estadisticas_equipo2['Remates al arco'] += stats_partido['Remates al arco']
    estadisticas_equipo2['Pases'] += stats_partido['Pases']
    estadisticas_equipo2['Faltas'] += stats_partido['Faltas']
    estadisticas_equipo2['Tarjetas amarillas'] += stats_partido['Tarjetas amarillas']
    estadisticas_equipo2['Tarjetas rojas'] += stats_partido['Tarjetas rojas']
    estadisticas_equipo2['goles_primera_mitad'] += stats_partido['goles_primera_mitad']
    estadisticas_equipo2['goles_segunda_mitad'] += stats_partido['goles_segunda_mitad']
    estadisticas_equipo2['Posesión'] += stats_partido['Posesión']
    estadisticas_equipo2['Precisión de los pases'] += stats_partido['Precisión de los pases']
    estadisticas_equipo2['goles_totales'] += stats_partido['goles_totales']
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

#COMIENZO DEL DATAFRAME
estadisticas_equipo1_df = pd.DataFrame([estadisticas_equipo1])
estadisticas_equipo2_df = pd.DataFrame([estadisticas_equipo2])

# Predicciones categóricas (gano, perdio, empato)
predicciones_categoricas_equipo1 = model_clasificacion.predict(estadisticas_equipo1_df)
predicciones_probabilidades_equipo1 = model_clasificacion.predict_proba(estadisticas_equipo1_df)

predicciones_categoricas_equipo2 = model_clasificacion2.predict(estadisticas_equipo2_df)
predicciones_probabilidades_equipo2 = model_clasificacion2.predict_proba(estadisticas_equipo2_df)

# Predicciones continuas (Tiros de esquina, goles_totales)
predicciones_continuas_equipo1 = model_regresion.predict(estadisticas_equipo1_df)
predicciones_continuas_equipo2 = model_regresion2.predict(estadisticas_equipo2_df)

#Predicción local
y_pred_categoricas = model_clasificacion.predict(x_test)
y_pred_continuas = model_regresion.predict(x_test)

#Predicción visitante
y_pred_categoricas2 = model_clasificacion2.predict(x_test2)
y_pred_continuas2 = model_regresion2.predict(x_test2)

# Evaluación de las variables continuas (regresión) local 
mse_continuas = root_mean_squared_error(y_test_continuas, y_pred_continuas)
mae_continuas = mean_absolute_error(y_test_continuas, y_pred_continuas)
r2_continuas = r2_score(y_test_continuas, y_pred_continuas)

# Evaluación de las variables continuas (regresión) visitante 
mse_continuas2 = root_mean_squared_error(y_test_continuas2, y_pred_continuas2)
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


# Mostrar las predicciones de manera organizada
print("\n-----------------PREDICCIONES DEL", equipo_objetivo_1,"-----------------")
# Predicciones categóricas (gano, perdio, empato)
for idx, variable in enumerate(y_categoricas.columns):
    probabilidad = predicciones_probabilidades_equipo1[idx]

    # Comprobar cuántos elementos hay en la probabilidad
    if len(probabilidad[0]) == 1:
        # Solo hay una probabilidad (el modelo está seguro)
        prob = probabilidad[0][0]
        print(f"{variable}: Predicción segura, Probabilidad: {prob:.2f}")
    else:
        # Acceder a ambas probabilidades
        prob_0 = probabilidad[0][0]  # Probabilidad de la clase
        prob_1 = probabilidad[0][1]  # Probabilidad de la clase complementaria
        print(f"{variable}: Predicción: {predicciones_categoricas_equipo1[0][idx]} "
              f"(Probabilidad de clase 0: {prob_0:.2f}, Probabilidad de clase 1: {prob_1:.2f})")

# Predicciones continuas sin tener en encuenta los jugadores (Tiros de esquina, goles_totales)
for idx, variable in enumerate(y_continuas.columns):
    prediccion = predicciones_continuas_equipo1[0][idx]
    prediccion_menos_mse = prediccion - mse_continuas
    prediccion_mas_mse = prediccion + mse_continuas
    print(f"{variable}: Predicción: {prediccion_menos_mse:.2f} ---- {prediccion:.2f} ---- {prediccion_mas_mse:.2f}")

print("\n-----------------PREDICCIONES DEL", equipo_objetivo_2,"-----------------")
# Predicciones categóricas (gano, perdio, empato)
for idx, variable in enumerate(y_categoricas.columns):
    probabilidad = predicciones_probabilidades_equipo2[idx]

    # Comprobar cuántos elementos hay en la probabilidad
    if len(probabilidad[0]) == 1:
        # Solo hay una probabilidad (el modelo está seguro)
        prob = probabilidad[0][0]
        print(f"{variable}: Predicción segura, Probabilidad: {prob:.2f}")
    else:
        # Acceder a ambas probabilidades
        prob_0 = probabilidad[0][0]  # Probabilidad de la clase
        prob_1 = probabilidad[0][1]  # Probabilidad de la clase complementaria
        print(f"{variable}: Predicción: {predicciones_categoricas_equipo2[0][idx]} "
              f"(Probabilidad de clase 0: {prob_0:.2f}, Probabilidad de clase 1: {prob_1:.2f})")

# Predicciones continuas sin tener en encuenta los jugadores (Tiros de esquina, goles_totales)
for idx, variable in enumerate(y_continuas.columns):
    prediccion = predicciones_continuas_equipo2[0][idx]
    prediccion_menos_mse = prediccion - mse_continuas2
    prediccion_mas_mse = prediccion + mse_continuas2
    print(f"{variable}: Predicción: {prediccion_menos_mse:.2f} ---- {prediccion:.2f} ---- {prediccion_mas_mse:.2f}")
#-------------------------------------Predecir si ganara con datos de un partido que ya ocurrio

"""
#--------------------------------------------------------------------------------Equipo local modelo predictivo teniendo en cuenta jugadores
# 2. Preparar los datos para el modelo del equipo local 
columnas_alineacion = ['jugador 1', 'posicion jugador 1','jugador 2', 'posicion jugador 2' ,'jugador 3', 'posicion jugador 3' ,'jugador 4', 'posicion jugador 4' ,'jugador 5', 'posicion jugador 5' ,'jugador 6', 'posicion jugador 6' ,'jugador 7', 'posicion jugador 7' ,'jugador 8', 'posicion jugador 8' ,'jugador 9', 'posicion jugador 9' ,'jugador 10', 'posicion jugador 10' ,'jugador 11', 'posicion jugador 11']

# Inicializar el LabelEncoder
label_encoder = LabelEncoder()
label_encoder2 = LabelEncoder()
# Aplicar el LabelEncoder a las columnas seleccionadas
for columna in columnas_alineacion:
    df_equipo1[columna] = label_encoder.fit_transform(df_equipo1[columna])
    df_equipo2[columna] = label_encoder2.fit_transform(df_equipo2[columna])

# Seleccionamos las columnas con estadísticas y el objetivo
x_categorica = df_equipo1[valores_x + ['Tiros de esquina']]
x_continuas = df_equipo1[valores_x + columnas_alineacion]
y_categorica = df_equipo1[columnas_alineacion]

# Dividir las variables de salida (Y)
y_continuas = y[valores_y_continuas]

# Dividir los datos en conjunto de entrenamiento y prueba
x_train_categorica, x_test_categorica, y_train_categoricas, y_test_categoricas = train_test_split(x_categorica, y_categorica, test_size=0.2, random_state=42)
x_train_continuas, x_test_continuas, y_train_continuas, y_test_continuas = train_test_split(x_continuas, y_continuas, test_size=0.2, random_state=42)

param_grid = {
    'estimator__criterion': ['gini', 'entropy'],  # Prefijo 'estimator__' para apuntar al modelo subyacente
    'estimator__n_estimators': [100, 250, 500],
    'estimator__min_samples_leaf': [5, 15, 25],
    'estimator__max_features': [3, 5, 7, 9],
}

# 1. Entrenar el modelo de clasificación para las variables categóricas
etc_classifier = ExtraTreesClassifier(random_state=21)
etc = MultiOutputClassifier(etc_classifier)

model_clasificacion = GridSearchCV(etc, param_grid, cv=3, n_jobs=-1)
model_clasificacion.fit(x_train_categorica, y_train_categoricas)
print("\nthe best scors teniendo en cuenta jugadores ", model_clasificacion.best_estimator_, " the best scors teniendo en cuenta jugadores ", model_clasificacion.best_score_)

# 2. Entrenar el modelo de regresión para las variables continuas
regresor = ExtraTreesRegressor(n_estimators=150, random_state=42)
model_regresion = MultiOutputRegressor(regresor)
model_regresion.fit(x_train_continuas, y_train_continuas)

#--------------------------------------------------------------------------------Equipo visitante modelo predictivo teniendo en cuenta jugadores
# 2. Preparar los datos para el modelo del equipo local
# Seleccionamos las columnas con estadísticas y el objetivo 

x_categorica2 = df_equipo2[valores_x + ['Tiros de esquina']]
x_continuas2 = df_equipo2[valores_x + ['jugador 1', 'posicion jugador 1','jugador 2', 'posicion jugador 2' ,'jugador 3', 'posicion jugador 3' ,'jugador 4', 'posicion jugador 4' ,'jugador 5', 'posicion jugador 5' ,'jugador 6', 'posicion jugador 6' ,'jugador 7', 'posicion jugador 7' ,'jugador 8', 'posicion jugador 8' ,'jugador 9', 'posicion jugador 9' ,'jugador 10', 'posicion jugador 10' ,'jugador 11', 'posicion jugador 11']]
y_categorica2 = df_equipo2[['jugador 1', 'posicion jugador 1','jugador 2', 'posicion jugador 2' ,'jugador 3', 'posicion jugador 3' ,'jugador 4', 'posicion jugador 4' ,'jugador 5', 'posicion jugador 5' ,'jugador 6', 'posicion jugador 6' ,'jugador 7', 'posicion jugador 7' ,'jugador 8', 'posicion jugador 8' ,'jugador 9', 'posicion jugador 9' ,'jugador 10', 'posicion jugador 10' ,'jugador 11', 'posicion jugador 11']]

# Dividir las variables de salida (Y)
y_continuas2 = y[valores_y_continuas]

# Dividir los datos en conjunto de entrenamiento y prueba
x_train_categorica, x_test_categorica2, y_train_categoricas, y_test_categoricas2 = train_test_split(x_categorica2, y_categorica2, test_size=0.2, random_state=42)
x_train_continuas, x_test_continuas2, y_train_continuas, y_test_continuas2 = train_test_split(x_continuas2, y_continuas2, test_size=0.2, random_state=42)

# 1. Entrenar el modelo de clasificación para las variables categóricas

etc2_classifier = ExtraTreesClassifier(random_state=21)
etc2 = MultiOutputClassifier(etc2_classifier)

model_clasificacion2 = GridSearchCV(etc2, param_grid, cv=3, n_jobs=-1)
model_clasificacion2.fit(x_train_categorica, y_train_categoricas)
print("\nthe best teniendo en cuenta jugadores ", model_clasificacion2.best_estimator_, " the best scors teniendo en cuenta jugadores ", model_clasificacion2.best_score_)

# 2. Entrenar el modelo de regresión para las variables continuas
regresor2 = ExtraTreesRegressor(n_estimators=150, random_state=42)
model_regresion2 = MultiOutputRegressor(regresor2)
model_regresion2.fit(x_train_continuas, y_train_continuas)


estadisticas_equipo1_df_categorica =  estadisticas_equipo1_df
estadisticas_equipo1_df_categorica['Tiros de esquina'] = predicciones_continuas_equipo1[0][idx]

estadisticas_equipo2_df_categorica =  estadisticas_equipo2_df
estadisticas_equipo2_df_categorica['Tiros de esquina'] = predicciones_continuas_equipo2[0][idx]

estadisticas_equipo1_df_continua =  estadisticas_equipo1_df
estadisticas_equipo2_df_continua =  estadisticas_equipo2_df

#----------------------------------------------Prediccion teniendo en cuenta jugadores 
# Predicciones categóricas jugadores

predicciones_categoricas_equipo1 = model_clasificacion.predict(estadisticas_equipo1_df_categorica)
predicciones_probabilidades_equipo1 = model_clasificacion.predict_proba(estadisticas_equipo1_df_categorica)

predicciones_categoricas_equipo2 = model_clasificacion2.predict(estadisticas_equipo2_df_categorica)
predicciones_probabilidades_equipo2 = model_clasificacion2.predict_proba(estadisticas_equipo2_df_categorica)

#Se elimina la columna tiros de esquina, ya que sera nuestra variable y en el siguiente modelo
estadisticas_equipo1_df_categorica.pop('Tiros de esquina')
estadisticas_equipo2_df_categorica.pop('Tiros de esquina')

# Decodificar las predicciones si el label_encoder es aplicable
predicciones_categoricas_equipo1_decodificada = []
for idx, variable in enumerate(columnas_alineacion):
    prediccion = predicciones_categoricas_equipo1[:, idx]
    pred_decodificada = label_encoder.inverse_transform(prediccion)
    predicciones_categoricas_equipo1_decodificada.append(pred_decodificada)

print("\nPredicciones Decodificadas Equipo 1:", predicciones_categoricas_equipo1_decodificada)

#Se añade la predicciones de jugadores


# Mostrar las predicciones de manera organizada
print("\n-----------------PREDICCIONES DEL", equipo_objetivo_1, "-----------------")

# Recorrer cada variable objetivo y sus probabilidades
for idx, variable in enumerate(columnas_alineacion):
    probabilidad = predicciones_probabilidades_equipo1[idx]  # Probabilidades para la salida `idx`
    prediccion = predicciones_categoricas_equipo1[:, idx]  # Predicción para la salida `idx`

    # Acceder a las probabilidades de todas las clases
    print(f"\nVariable: {variable}")
    for clase_idx, prob in enumerate(probabilidad[0]):
        print(f"Clase {clase_idx}: Probabilidad {prob:.2f}")
    print(f"Predicción final: {prediccion[0]}")  # Primera predicción para esta salida

"""    
"""
# Predicciones continuas (Tiros de esquina, goles_totales)
predicciones_continuas_equipo1 = model_regresion.predict(estadisticas_equipo1_df_categorica)
predicciones_continuas_equipo2 = model_regresion2.predict(estadisticas_equipo2_df_categorica)

#Predicción local
y_pred_categoricas = model_clasificacion.predict(x_test)
y_pred_continuas = model_regresion.predict(x_test)

#Predicción visitante
y_pred_categoricas2 = model_clasificacion2.predict(x_test2)
y_pred_continuas2 = model_regresion2.predict(x_test2)

# Evaluación de las variables continuas (regresión) local 
mse_continuas = root_mean_squared_error(y_test_continuas, y_pred_continuas)
mae_continuas = mean_absolute_error(y_test_continuas, y_pred_continuas)
r2_continuas = r2_score(y_test_continuas, y_pred_continuas)

# Evaluación de las variables continuas (regresión) visitante 
mse_continuas2 = root_mean_squared_error(y_test_continuas2, y_pred_continuas2)
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


# Mostrar las predicciones de manera organizada
print("\n-----------------PREDICCIONES DEL", equipo_objetivo_1,"-----------------")
# Predicciones categóricas (gano, perdio, empato)
for idx, variable in enumerate(y_categoricas.columns):
    probabilidad = predicciones_probabilidades_equipo1[idx]

    # Comprobar cuántos elementos hay en la probabilidad
    if len(probabilidad[0]) == 1:
        # Solo hay una probabilidad (el modelo está seguro)
        prob = probabilidad[0][0]
        print(f"{variable}: Predicción segura, Probabilidad: {prob:.2f}")
    else:
        # Acceder a ambas probabilidades
        prob_0 = probabilidad[0][0]  # Probabilidad de la clase
        prob_1 = probabilidad[0][1]  # Probabilidad de la clase complementaria
        print(f"{variable}: Predicción: {predicciones_categoricas_equipo1[0][idx]} "
              f"(Probabilidad de clase 0: {prob_0:.2f}, Probabilidad de clase 1: {prob_1:.2f})")

# Predicciones continuas sin tener en encuenta los jugadores (Tiros de esquina, goles_totales)
for idx, variable in enumerate(y_continuas.columns):
    prediccion = predicciones_continuas_equipo1[0][idx]
    prediccion_menos_mse = prediccion - mse_continuas
    prediccion_mas_mse = prediccion + mse_continuas
    print(f"{variable}: Predicción: {prediccion_menos_mse:.2f} ---- {prediccion:.2f} ---- {prediccion_mas_mse:.2f}")

print("\n-----------------PREDICCIONES DEL", equipo_objetivo_2,"-----------------")
# Predicciones categóricas (gano, perdio, empato)
for idx, variable in enumerate(y_categoricas.columns):
    probabilidad = predicciones_probabilidades_equipo2[idx]

    # Comprobar cuántos elementos hay en la probabilidad
    if len(probabilidad[0]) == 1:
        # Solo hay una probabilidad (el modelo está seguro)
        prob = probabilidad[0][0]
        print(f"{variable}: Predicción segura, Probabilidad: {prob:.2f}")
    else:
        # Acceder a ambas probabilidades
        prob_0 = probabilidad[0][0]  # Probabilidad de la clase
        prob_1 = probabilidad[0][1]  # Probabilidad de la clase complementaria
        print(f"{variable}: Predicción: {predicciones_categoricas_equipo2[0][idx]} "
              f"(Probabilidad de clase 0: {prob_0:.2f}, Probabilidad de clase 1: {prob_1:.2f})")

# Predicciones continuas sin tener en encuenta los jugadores (Tiros de esquina, goles_totales)
for idx, variable in enumerate(y_continuas.columns):
    prediccion = predicciones_continuas_equipo2[0][idx]
    prediccion_menos_mse = prediccion - mse_continuas2
    prediccion_mas_mse = prediccion + mse_continuas2
    print(f"{variable}: Predicción: {prediccion_menos_mse:.2f} ---- {prediccion:.2f} ---- {prediccion_mas_mse:.2f}")
#-------------------------------------Predecir si ganara con datos de un partido que ya ocurrio
"""