from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Configuración de Selenium con ChromeDriver
service =  Service(executable_path= 'chromedriver.exe')
driver = webdriver.Chrome(service=service)

urls_torneos = []

equipos = {"Desconocido": -1}


def getTeams(soup):
    try:
        campeonato = soup.find('div', class_= 'PZPZlf ssJ7i B5dxMb')
        team_table = soup.find('table', class_= 'Jzru1c')

        rows = team_table.select('tr.imso-loa.imso-hov')
        for row in rows:
            team_name = row.get("aria-label")
            if not team_name in equipos:
                equipos[team_name] = (len(equipos)+1)-1

    except Exception as e:
        print(f"Error al obtener estadísticas para {campeonato}: {e}")

# Función para procesar las URLs
def procesar_urls(urls):
    for url in urls:
        try:
            driver.delete_all_cookies()
            driver.get(url)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            getTeams(soup)
            
        except Exception as e:
            print(f"Error procesando la URL {url}: {e}")

procesar_urls(urls_torneos)
print(equipos)