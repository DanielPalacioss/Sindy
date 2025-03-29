#Como la regresion logistica necesita mas de 1 variable para predecir el futuro, necesitamos que ya sea en los partidos del local o el visitante alla al un partido donde gane y otro donde pierda. si no da error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.multioutput import MultiOutputRegressor, MultiOutputClassifier
from sklearn.metrics import  root_mean_squared_error, mean_absolute_error, r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import math
import pandas as pd
import os
from RecoleccionEquipos import EquipmentCollection
from selenium.webdriver.chrome.options import Options
from getMatch import getMatch
from xgboost import XGBClassifier, XGBRegressor

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

# Ingreso de URLs
#num_urls = int(input("¿Cuántas URLs deseas ingresar? "))
matchsNumber = 10
url = 'https://www.google.com/search?sca_esv=4ad496d1768baf99&rlz=1C1ALOY_esCO1035CO1035&cs=1&sxsrf=AHTn8zolV7G8aX6c1SUQSHNUlE4RUGOXXQ:1742790043735&q=Racing+Club+de+Estrasburgo&stick=H4sIAAAAAAAAAONgVuLUz9U3MMktsKh4xGjCLfDyxz1hKe1Ja05eY1Tl4grOyC93zSvJLKkUEudig7J4pbi5ELp4FrFKBSUmZ-alKzjnlCYppKQquBaXFCUWJ5UWpecDAA7-TgdhAAAA&ved=2ahUKEwiL-srr7qGMAxXnSTABHVR3B24Qukt6BAgCEBU#sie=t;/m/04mp8x;2;/m/044hxl;bbbs;hd;;;;2025-05-18T12:00:00Z&wptab=si:APYL9bsdvePlUvFpoma5fMvhOQ6bvXM76DvGLQOhfQo6Zp3kxNoH6BKiFU3NUK-DDCMYUl50O50je6Y_pgRm3IpRsSlYbsKls-YEcu9yYUL2YnmVQ4YudYQ4Y_xxEGvPHR77C-QcPNH5WvlitVIR5ZYdbAZV9xP_zzdIbZpUuqdXX0L0MjyeLBSxTVRMXo1hQYBq8VA0LGOtL2d-BSB5BD3HHsGWRyMSC-5ZHoDOn0FAaFKYI36KwaY%3D'
defaultLink = 'https://www.google.com/search?sca_esv=4ad496d1768baf99&rlz=1C1ALOY_esCO1035CO1035&cs=1&sxsrf=AHTn8zolV7G8aX6c1SUQSHNUlE4RUGOXXQ:1742790043735&q=Racing+Club+de+Estrasburgo&stick=H4sIAAAAAAAAAONgVuLUz9U3MMktsKh4xGjCLfDyxz1hKe1Ja05eY1Tl4grOyC93zSvJLKkUEudig7J4pbi5ELp4FrFKBSUmZ-alKzjnlCYppKQquBaXFCUWJ5UWpecDAA7-TgdhAAAA&ved=2ahUKEwiL-srr7qGMAxXnSTABHVR3B24Qukt6BAgCEBU#sie=m;/g/11y6hmcdl6;2;/m/044hxl;dt;fp;1;;;&wptab=si:APYL9bsdvePlUvFpoma5fMvhOQ6bvXM76DvGLQOhfQo6Zp3kxNoH6BKiFU3NUK-DDCMYUl50O50je6Y_pgRm3IpRsSlYbsKls-YEcu9yYUL2YnmVQ4YudYQ4Y_xxEGvPHR77C-QcPNH5WvlitVIR5ZYdbAZV9xP_zzdIbZpUuqdXX0L0MjyeLBSxTVRMXo1hQYBq8VA0LGOtL2d-BSB5BD3HHsGWRyMSC-5ZHoDOn0FAaFKYI36KwaY%3D'
urls_equipo_1 = getMatch().getMatchs(matchsNumber, url, defaultLink)

matchsNumber2 = 10
url2 = 'https://www.google.com/search?cs=1&rlz=1C1ALOY_esCO1035CO1035&sca_esv=4ad496d1768baf99&sxsrf=AHTn8zra-g3LAPaLyjO_WqFLexIz1V5fSQ:1742790158233&q=Olympique+de+Lyon&stick=H4sIAAAAAAAAAONgVuLUz9U3MC43z654xGjCLfDyxz1hKe1Ja05eY1Tl4grOyC93zSvJLKkUEudig7J4pbi5ELp4FrEK-udU5hZkFpamKqSkKvhU5ucBAPQWM0lYAAAA&ved=2ahUKEwiV85-i76GMAxUMfDABHbmDLSkQukt6BAgCEBY#sie=t;/m/03w7kx;2;/m/044hxl;bbbs;hd;;;;2025-05-18T12:00:00Z&wptab=si:APYL9bsdvePlUvFpoma5fMvhOQ6bvXM76DvGLQOhfQo6Zp3kxNoH6BKiFU3NUK-DDCMYUl50O50je6Y_pgRm3IpRsSlYbsKls-YEcu9yYUL2YnmVQ4YudYQ4Y_xxEGvPHR77C-QcPNH5WvlitVIR5ZYdbAZVJmiZsK1To13Q_0mdZYXGr5SfsDO1NtOp88kgYf6twcoGZ2cUUrjh3b8oWBpjVa5abS0BbJyBwZ0KXSvtfjiijwZGLSY%3D'
defaultLink2 = 'https://www.google.com/search?cs=1&rlz=1C1ALOY_esCO1035CO1035&sca_esv=4ad496d1768baf99&sxsrf=AHTn8zra-g3LAPaLyjO_WqFLexIz1V5fSQ:1742790158233&q=Olympique+de+Lyon&stick=H4sIAAAAAAAAAONgVuLUz9U3MC43z654xGjCLfDyxz1hKe1Ja05eY1Tl4grOyC93zSvJLKkUEudig7J4pbi5ELp4FrEK-udU5hZkFpamKqSkKvhU5ucBAPQWM0lYAAAA&ved=2ahUKEwiV85-i76GMAxUMfDABHbmDLSkQukt6BAgCEBY#sie=m;/g/11w3vp_4dh;2;/m/044hxl;dt;fp;1;;;&wptab=si:APYL9bsdvePlUvFpoma5fMvhOQ6bvXM76DvGLQOhfQo6Zp3kxNoH6BKiFU3NUK-DDCMYUl50O50je6Y_pgRm3IpRsSlYbsKls-YEcu9yYUL2YnmVQ4YudYQ4Y_xxEGvPHR77C-QcPNH5WvlitVIR5ZYdbAZVJmiZsK1To13Q_0mdZYXGr5SfsDO1NtOp88kgYf6twcoGZ2cUUrjh3b8oWBpjVa5abS0BbJyBwZ0KXSvtfjiijwZGLSY%3D'
urls_equipo_2 = getMatch().getMatchs(matchsNumber2, url2, defaultLink2)

equipos_dict = EquipmentCollection().get_dict_of_csv()
if len(equipos_dict) == 1:
    raise Exception("No se ha agregado equipos, por favor agregarlos")

# Configuración de Selenium con ChromeDriver
service =  Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

Torneo = 9 #Torneo de partido a predecir, para saber que numero poner, vaya a bajo en el diccionario torneo

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
Alineacion_local = 3
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

        fecha = fecha.split(",")
        if(len(fecha) > 1):
            fecha = fecha[1].replace(' ', '')+"/24" #Esto debe modificarse segun el año en el que estemos
        elif(len(fecha[0]) <= 5):
            fecha = fecha[0]+"/24"
        else:
            fecha = fecha[0]
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



# Procesar las URLs de ambos equipos
stats[equipo_objetivo_1] = procesar_urls(urls_equipo_1, equipo_objetivo_1)
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
            df_existente = pd.read_csv(nombre_archivo, sep=';', quotechar='"')

            # Crear un nuevo DataFrame con los nuevos datos
            datos = [estadisticas for estadisticas in partidos.values()]
            df_nuevo = pd.DataFrame(datos)

            # Concatenar los DataFrames
            df_stats = pd.concat([df_existente, df_nuevo], ignore_index=True)
            df_stats = df_stats.drop_duplicates()

            # Guardar el DataFrame actualizado en el archivo CSV
            df_stats.to_csv(nombre_archivo, sep=';', index=False)
        else:
            # Si no existe, crear el archivo con los datos nuevos
            datos = [estadisticas for estadisticas in partidos.values()]
            df_stats = pd.DataFrame(datos)
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

def preparar_datos(df):
    x = df[valores_x]
    y = df[valores_y]
    y_categoricas = y[valores_y_categoricas]
    y_continuas = y[valores_y_continuas]
    return x, y_categoricas, y_continuas

x1, y_cat1, y_cont1 = preparar_datos(df_equipo1)
x2, y_cat2, y_cont2 = preparar_datos(df_equipo2)

def dividir_datos(x, y_cat, y_cont):
    x_train, x_test, y_train_cat, y_test_cat = train_test_split(x, y_cat, test_size=0.2, random_state=42)
    _, _, y_train_cont, y_test_cont = train_test_split(x, y_cont, test_size=0.2, random_state=42)
    return x_train, x_test, y_train_cat, y_test_cat, y_train_cont, y_test_cont

x_train1, x_test1, y_train_cat1, y_test_cat1, y_train_cont1, y_test_cont1 = dividir_datos(x1, y_cat1, y_cont1)
x_train2, x_test2, y_train_cat2, y_test_cat2, y_train_cont2, y_test_cont2 = dividir_datos(x2, y_cat2, y_cont2)

# Crear una única columna categórica
def transformar_resultado(df):
    return df[['gano', 'empato', 'perdio']].idxmax(axis=1)

y_train_cat1 = transformar_resultado(y_train_cat1)
y_test_cat1 = transformar_resultado(y_test_cat1)

y_train_cat2 = transformar_resultado(y_train_cat2)
y_test_cat2 = transformar_resultado(y_test_cat2)

param_grid_xgb = {
    'n_estimators': [100, 250, 500],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0]
}

def entrenar_clasificacion_multioutput(x_train, y_train_cat, param_grid_xgb):
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_train_cat)  # Ahora solo una columna
    
    xgb_clf = XGBClassifier(
        random_state=21,
        objective='multi:softprob',
        eval_metric='mlogloss',
        num_class=len(le.classes_)  # Se asegura de que XGBoost reconozca las clases
    )

    grid_search = GridSearchCV(
        estimator=xgb_clf,
        param_grid=param_grid_xgb,
        cv=3,
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(x_train, y_encoded)
    
    return grid_search, le


def entrenar_regresion(x_train, y_train_cont):
    xgb_reg = XGBRegressor(n_estimators=150, random_state=42, objective='reg:squarederror')
    model = MultiOutputRegressor(xgb_reg)
    model.fit(x_train, y_train_cont)
    return model

# Entrenar modelos para equipo 1
modelos_clasificacion1, encoders1 = entrenar_clasificacion_multioutput(x_train1, y_train_cat1, param_grid_xgb)
model_regresion1 = entrenar_regresion(x_train1, y_train_cont1)

# Entrenar modelos para equipo 2
modelos_clasificacion2, encoders2 = entrenar_clasificacion_multioutput(x_train2, y_train_cat2, param_grid_xgb)
model_regresion2 = entrenar_regresion(x_train2, y_train_cont2)

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

# Corrección y optimización de predicciones

def hacer_predicciones_categoricas(modelo, estadisticas, label_encoder):
    predicciones_encoded = modelo.predict(estadisticas)
    predicciones_probabilidades = modelo.predict_proba(estadisticas)
    
    # Convertir la predicción numérica en la categoría original
    predicciones_categoricas = label_encoder.inverse_transform(predicciones_encoded)

    return predicciones_categoricas, predicciones_probabilidades

def evaluar_regresion(modelo, x_test, y_test):
    y_pred = modelo.predict(x_test)
    mse = root_mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, mae, r2, y_pred

def imprimir_evaluacion_regresion(mse, mae, r2, equipo):
    print(f'\nError cuadrático medio (RMSE) continuas del {equipo}: {mse:.3f}')
    print(f'Error cuadrático medio (MSE) continuas al cuadrado del {equipo}: {math.pow(mse,2):.3f}')
    print(f'Error absoluto medio (MAE) continuas del {equipo}: {mae:.3f}')
    print(f'Coeficiente de determinación (R2) continuas del {equipo}: {r2:.3f}')

# Predicciones categóricas
# Predicciones categóricas
predicciones_categoricas_equipo1, probabilidades_equipo1 = hacer_predicciones_categoricas(
    modelos_clasificacion1, estadisticas_equipo1_df, encoders1
)
predicciones_categoricas_equipo2, probabilidades_equipo2 = hacer_predicciones_categoricas(
    modelos_clasificacion2, estadisticas_equipo2_df, encoders2
)

# Predicciones continuas
predicciones_continuas_equipo1 = model_regresion1.predict(estadisticas_equipo1_df)
predicciones_continuas_equipo2 = model_regresion2.predict(estadisticas_equipo2_df)

# Predicciones continuas y evaluación
mse_continuas, mae_continuas, r2_continuas, predicciones_continuas_equipo1 = evaluar_regresion(
    model_regresion1, x_test1, y_test_cont1
)
mse_continuas2, mae_continuas2, r2_continuas2, predicciones_continuas_equipo2 = evaluar_regresion(
    model_regresion2, x_test2, y_test_cont2
)

print("\nEvaluación clasificación equipo 1:")
best_model = modelos_clasificacion1.best_estimator_  # Obtener el mejor modelo
pred_test = best_model.predict(x_test1)
acc = accuracy_score(y_test_cat1, pred_test)  # No es necesario usar y_test_cat1[col] ya que es solo una variable
print(f"Precisión: {acc:.3f}")


print("\nEvaluación clasificación equipo 2:")

best_model = modelos_clasificacion2.best_estimator_  # Extraer el mejor modelo
pred_test = best_model.predict(x_test2)
acc = accuracy_score(y_test_cat2, pred_test)
print(f"Precisión: {acc:.3f}")


def mostrar_predicciones(equipo, predicciones_categoricas, probabilidades, encoders, predicciones_continuas, mse_continuas):
    print(f"\n-----------------PREDICCIONES DEL {equipo}-----------------")
    for variable in valores_y_categoricas:
        clases_originales = encoders[variable].classes_
        proba = probabilidades[variable]
        print(f"\n{variable}:")
        for clase, prob in zip(clases_originales, proba):
            print(f"  Probabilidad {clase}: {prob:.2%}")
        print(f"  Predicción: {predicciones_categoricas[variable].iloc[0]}")

    for idx, variable in enumerate(valores_y_continuas):
        pred = predicciones_continuas[0][idx]
        print(f"\n{variable}:")
        print(f"  Rango probable: {pred - mse_continuas:.2f} a {pred + mse_continuas:.2f}")
        print(f"  Valor central: {pred:.2f}")

# Mostrar resultados
mostrar_predicciones(equipo_objetivo_1, predicciones_categoricas_equipo1, probabilidades_equipo1, encoders1, predicciones_continuas_equipo1, mse_continuas)
mostrar_predicciones(equipo_objetivo_2, predicciones_categoricas_equipo2, probabilidades_equipo2, encoders2, predicciones_continuas_equipo2, mse_continuas2)