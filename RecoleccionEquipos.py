from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options


class EquipmentCollection:
    if __name__ == "__main__":

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


        # Configuración de Selenium con ChromeDriver
        service =  Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)

        urls_torneos = []

        equipos_dict = {"Desconocido": -1}


    def getTeams(self, soup):
        self.equipos_dict = self.get_dict_of_csv()
        try:
            campeonato = soup.find('div', class_='PZPZlf ssJ7i')
            team_tables = soup.find_all('table', class_='Jzru1c')  # Encuentra todas las tablas

            for team_table in team_tables:  # Itera sobre cada tabla encontrada
                rows = team_table.select('tr.imso-loa.imso-hov')  # Selecciona las filas dentro de cada tabla
                for row in rows:
                    team_name = row.get("aria-label")
                    if team_name and team_name not in self.equipos_dict:
                        self.equipos_dict[team_name] = len(self.equipos_dict)

        except Exception as e:
            print(f"Error al obtener estadísticas para {campeonato}: {e}")

    # Función para procesar las URLs
    def procesar_urls(self, urls):
        for url in urls:
            try:
                self.driver.delete_all_cookies()
                self.driver.get(url)
                time.sleep(3)
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                self.getTeams(soup)
                
            except Exception as e:
                print(f"Error procesando la URL {url}: {e}")

        # Cerrar el navegador
        self.driver.quit()

        return pd.DataFrame(list(self.equipos_dict.items()), columns=["Equipo", "ID"])

    def get_dict_of_csv(self):
        if os.path.isfile('teams.csv'):
            df = pd.read_csv('teams.csv', sep=';', quotechar='"')
            return dict(zip(df["Equipo"], df["ID"]))
        else:
            return self.equipos_dict
        
    def save_csv(self, df):

        # Verificar si el archivo existe
        if os.path.isfile('teams.csv'):
            df.to_csv('teams.csv', sep=';', index=False)
        else:
            df.to_csv('teams.csv', sep=';', index=False)
            # Si no existe, se crea desde 0
            
if __name__ == "__main__":
    equipment_collection = EquipmentCollection()
    df = equipment_collection.procesar_urls(equipment_collection.urls_torneos)
    equipment_collection.save_csv(df)