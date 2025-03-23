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

def reemplazar_texto(texto, nuevo_valor):
    return re.sub(r";/g.*?;", f';{nuevo_valor};', texto)

# Configuración de Selenium con ChromeDriver
service =  Service(executable_path= 'chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
url = 'https://www.google.com/search?q=real+madrid&rlz=1C1ALOY_esCO1035CO1035&oq=real&gs_lcrp=EgZjaHJvbWUqFAgAECMYJxhGGP0BGOMCGIAEGIoFMhQIABAjGCcYRhj9ARjjAhiABBiKBTIMCAEQLhgnGIAEGIoFMgYIAhBFGDkyBggDEEUYQDIGCAQQRRg7MgwIBRAuGEMYgAQYigUyBggGEEUYPDIGCAcQRRg90gEIMTM1N2owajmoAgCwAgE&sourceid=chrome&ie=UTF-8#sie=t;/m/06l22;2;/m/09gqx;bbbs;hd;;;;2025-06-27T01:00:00Z&wptab=si:APYL9btp3RF4rMteeKUUGnuEThopwi3n8zDPOUD_15eeNqymofjNp8Ggx03jTIB85JK2xfZX-PN_WHJ87reP5LTehwdvvpHWqUIShAMRBH0NlhoWnBaeEyQqXqVwveDRKb-hXLnQjhPkLs5mAmJzxKJK7FN7UDNYhFyCjhrD9D0h41TmJ0xMxpEaJAmM21muoVPeZGVO_psENF4ab__kC6R0N0AcZK9iSKeXlaOvisBNagbzFVd4Plc%3D'
matchsNumber = 100
defaultLink = 'https://www.google.com/search?q=real+madrid&rlz=1C1ALOY_esCO1035CO1035&oq=real&gs_lcrp=EgZjaHJvbWUqFAgAECMYJxhGGP0BGOMCGIAEGIoFMhQIABAjGCcYRhj9ARjjAhiABBiKBTIMCAEQLhgnGIAEGIoFMgYIAhBFGDkyBggDEEUYQDIGCAQQRRg7MgwIBRAuGEMYgAQYigUyBggGEEUYPDIGCAcQRRg90gEIMTM1N2owajmoAgCwAgE&sourceid=chrome&ie=UTF-8#sie=m;/g/11vwk39h16;2;/g/11b6xyz746;dt;fp;1;;;&wptab=si:APYL9btp3RF4rMteeKUUGnuEThopwi3n8zDPOUD_15eeNqymofjNp8Ggx03jTIB85JK2xfZX-PN_WHJ87reP5LTehwdvvpHWqUIShAMRBH0NlhoWnBaeEyQqXqVwveDRKb-hXLnQjhPkLs5mAmJzxKJK7FN7UDNYhFyCjhrD9D0h41TmJ0xMxpEaJAmM21muoVPeZGVO_psENF4ab__kC6R0N0AcZK9iSKeXlaOvisBNagbzFVd4Plc%3D'
try:
    driver.get(url)
    time.sleep(6)
    # Esperar a que el modal se cargue
    wait = WebDriverWait(driver, 0)  # Aumenta el tiempo de espera
    modal = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sZmt3b"]/div[2]/div[2]/div/div[2]/div')))
    cont = 0
    tableNumber = math.ceil(matchsNumber/40)+1
    while(cont < tableNumber):
        time.sleep(4)
        # Hacer scroll dentro del div con scroll
        driver.execute_script("arguments[0].scrollTop = 0;", modal)
        cont +=1 

    # Obtener la fecha y hora actual en UTC
    now = datetime.now(timezone.utc)
    
    time.sleep(5)

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
                modifiedLink = reemplazar_texto(defaultLink, div.get_attribute("data-df-match-mid"))
                filtered_matchesLink.append(modifiedLink)
except Exception as e:
    print(f"Error obteniendo Ids de la URL {e}")