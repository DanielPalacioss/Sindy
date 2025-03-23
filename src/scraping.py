from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from config import torneos_dict, alineaciones_dict, equipos_dict, estadisticas_excluidas, equipo_objetivo_1, equipo_objetivo_2


def setup_selenium():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def obtener_estadisticas(soup, equipo_objetivo):
    try:
        fecha_div = soup.find('div', class_='imso_mh__pst-m-stts-l')
        fecha = fecha_div.find('div', class_='imso-hide-overflow').find_all('span')[4].text.strip()
        stats_table = soup.find('div', class_='lr-imso-ss-wdm')
        partido_stats = {}

        fecha = fecha.split(",")
        if len(fecha) > 1:
            fecha = fecha[1].replace(' ', '') + "/24"
        elif len(fecha[0]) <= 5:
            fecha = fecha[0] + "/24"
        else:
            fecha = fecha[0]
        partido_stats["Fecha"] = fecha
        partido_stats["Equipo_name"] = equipo_objetivo

        alineacion = ""
        alineacionContrincante = ""
        local = 0
        torneo_div = soup.find('div', class_='imso-hide-overflow')
        torneo_span = torneo_div.find('span', class_='imso-loa imso-ln')
        torneo_nombre = torneo_span.text.strip() if torneo_span else "Torneo desconocido"
        alineacion_div = soup.find('div', class_='lr-imso-lineups-container')
        local_div = alineacion_div.find('div', class_='lr-vl-hf lrvl-btrc')
        visitante_div = alineacion_div.find('div', class_='lr-vl-hf lrvl-bbrc')
        local_all_span = local_div.find_all('span')
        visitante_all_span = visitante_div.find_all('span')

        if local_all_span[0].text.strip() == equipo_objetivo:
            alineacion = local_all_span[1].text.strip()
            alineacionContrincante = visitante_all_span[1].text.strip()
        else:
            alineacion = visitante_all_span[1].text.strip()
            alineacionContrincante = local_all_span[1].text.strip()
            local = 1

        torneo_valor = torneos_dict.get(torneo_nombre, -1)
        partido_stats["Torneo"] = torneo_valor

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

        formacion_local_div = soup.find('div', class_='lrvl-tlt lrvl-tl lrvl-btrc')
        formacion_visitante_div = soup.find('div', class_='lrvl-tlt lrvl-tl lrvl-bbrc')
        jugadores_formacion_local_div = formacion_local_div.find_all('div', class_='A9ad7e imso-loa')
        jugadores_formacion_visitante_div = formacion_visitante_div.find_all('div', class_='A9ad7e imso-loa')
        
        if local == 0:
            for i, jugador_span in enumerate(jugadores_formacion_local_div, start=1):
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
        'goles_totales': 0,
        'gano': 0,
        'empato': 0,
        'perdio': 0,
        'visitante': 0,
        'local': 0
    }

    try:
        equipo_local = soup.find('div', class_='imso_mh__first-tn-ed').find('span').text
        equipo_visitante = soup.find('div', class_='imso_mh__second-tn-ed').find('span').text
        marcador_local = int(soup.find('div', class_='imso_mh__l-tm-sc').text.strip())
        marcador_visitante = int(soup.find('div', class_='imso_mh__r-tm-sc').text.strip())
        
        if marcador_local == 0 and marcador_visitante == 0:
            print(f"Ambos equipos no tienen goles en el partido actual ({equipo_local} vs {equipo_visitante}).")
            if equipo_objetivo == equipo_local:
                goles_objetivo = marcador_local
                goles_rival = marcador_visitante
                goles_por_tiempo['local'] = 1
            else:
                goles_por_tiempo['visitante'] = 1
                goles_objetivo = marcador_visitante
                goles_rival = marcador_local

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

        if goles_objetivo > goles_rival:
            goles_por_tiempo['gano'] = 1
        elif goles_objetivo == goles_rival:
            goles_por_tiempo['empato'] = 1
        else:
            goles_por_tiempo['perdio'] = 1
                
        eventos_goles = soup.find_all('span', class_='liveresults-sports-immersive__game-minute')
        goles_totales_en_partido = marcador_local + marcador_visitante
        eventos_goles = eventos_goles[:goles_totales_en_partido]

        for minuto_tag in eventos_goles:
            minuto = int(minuto_tag.find('span').text.strip())
            equipo_goleador = equipo_local if minuto_tag.find_parent('div', class_='imso_gs__left-team') else equipo_visitante
            
            if equipo_goleador == equipo_objetivo:
                if minuto <= 45:
                    goles_por_tiempo['goles_primera_mitad'] += 1
                else:
                    goles_por_tiempo['goles_segunda_mitad'] += 1

        goles_por_tiempo['goles_totales'] = goles_por_tiempo['goles_primera_mitad'] + goles_por_tiempo['goles_segunda_mitad']
        return goles_por_tiempo

    except Exception as e:
        print(f"Error al obtener goles para {equipo_objetivo}: {e}")
        return None
    
def procesar_urls(urls, equipo_objetivo, driver):
    partido_stats = {}
    for idx, url in enumerate(urls, start=1):
        try:
            driver.get(url)
            time.sleep(5)
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