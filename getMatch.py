from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
from datetime import datetime, timezone
import re

class getMatch:

    @staticmethod
    def reemplazar_texto(texto, nuevo_valor):
        return re.sub(r";/g.*?;", f';{nuevo_valor};', texto)
    
    def getMatchs(self, matchsNumber, url, defaultLink):
        options = Options()
        # Modo sin interfaz gráfica
        options.add_argument('--headless')  
        options.add_argument('--disable-gpu')  # Recomendado en modo headless (especialmente en Windows)
        options.add_argument('--disable-dev-shm-usage')  # Previene errores en contenedores
        options.add_argument('--no-sandbox')  # Evita errores en algunos entornos Linux

        # Opciones útiles
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('disable-blink-features=AutomationControlled')  # Evita detección
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")

        #options.add_argument("--window-size=1920,1080")


        # Configuración de Selenium con ChromeDriver
        service =  Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        try:
            driver.get(url)
            time.sleep(1)
            driver.get(url)
            # Esperar a que el modal se cargue
            wait = WebDriverWait(driver, 6)  # Aumenta el tiempo de espera
            modal = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sZmt3b"]/div[2]/div[2]/div/div[2]/div')))
            cont = 0
            if(matchsNumber < 20):
                tableNumber = math.ceil(matchsNumber/40)
            else:
                tableNumber = math.ceil(matchsNumber/40)+1
                matchsNumber += 25
            while(cont < tableNumber):
                time.sleep(2.5)
                # Hacer scroll dentro del div con scroll
                driver.execute_script("arguments[0].scrollTop = 0;", modal)
                cont +=1 

            # Obtener la fecha y hora actual en UTC
            now = datetime.now(timezone.utc)
            
            time.sleep(1)

            # Buscar todos los divs con las clases 'imso-loa' o 'imso-ani' y filtrar por fecha
            filtered_matchesLink = []

            child_divs = driver.find_elements(By.CSS_SELECTOR, "div.OcbAbf[data-hveid='CAEQAA'] div.imso-loa.imso-ani")

            for div in reversed(child_divs):
                start_time_attr = div.get_attribute("data-start-time")

                if start_time_attr:
                    # Convertir la fecha de string a datetime
                    start_time = datetime.fromisoformat(start_time_attr.replace("Z", "+00:00"))

                    # Comparar con la fecha actual
                    if start_time < now:
                        modifiedLink = self.reemplazar_texto(defaultLink, div.get_attribute("data-df-match-mid"))
                        filtered_matchesLink.append(modifiedLink)
            driver.quit()
            return filtered_matchesLink[:matchsNumber] # Se agregan 15 porque a veces hay link sin estadisticas
        except Exception as e:
            print(f"Error obteniendo Ids de la URL {e}")