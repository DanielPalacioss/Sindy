from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

class getAlineacion:
    
    def saveIdName365(self, parametros):
        name_equipo = parametros["name_equipo"]
        name_visitante_equipo = parametros["name_visitante_equipo"]
        torneo = parametros["torneo"]
        torneo_365 = ""
        name_365 = ""
        id_365 = ""
        name_visitante_365 = ""
        id_visitante_365 = ""
        
        df = pd.read_csv("league365.csv")

        if torneo not in df["name_google"].values:
            # Pedir al usuario el nombre real como aparece en 365
            torneo_365 = input("⚠️ Torneo no encontrado.\nIngresá el nombre EXACTO como aparece en 365, seguido de guion y el ID (ej: 'Premier-League-23'): ")

            # Agregar nueva fila
            nueva_fila = pd.DataFrame([{
                "name_google": torneo,
                "league": torneo_365
            }])

            df = pd.concat([df, nueva_fila], ignore_index=True)
            df.to_csv("league365.csv", index=False)
            print(f"✅ Torneo añadido: {torneo} -> {torneo_365}")

        else:
            # Extraer el valor de 'league' correspondiente
            torneo_365 = df.loc[df["name_google"] == torneo, "league"].values[0]
            print(f"✅ Torneo encontrado: {torneo} -> {torneo_365}")

        df_teams = pd.read_csv("teams.csv", sep=";", dtype={"ID_365": str, "Name365": str})
        
        # Verificamos si el equipo existe
        if name_equipo in df_teams["Equipo"].values:
            fila_equipo = df_teams.loc[df_teams["Equipo"] == name_equipo]

            id_365 = fila_equipo["ID_365"].values[0]
            name_365 = fila_equipo["Name365"].values[0]

            # Validamos si están vacíos (NaN o string vacío)
            if pd.isna(id_365) or id_365 == "":
                id_365 = input(f"🆔 Ingresá el ID_365 para el equipo '{name_equipo}': ")
                df_teams.loc[df_teams["Equipo"] == name_equipo, "ID_365"] = id_365

            if pd.isna(name_365) or name_365 == "":
                name_365 = input(f"🏷️ Ingresá el Name365 tal cual como aparece en 365 para el equipo '{name_equipo}': ")
                df_teams.loc[df_teams["Equipo"] == name_equipo, "Name365"] = name_365

            # Guardamos los cambios
            df_teams.to_csv("teams.csv", sep=";", index=False)

        else:
            print(f"❌ El equipo '{name_equipo}' no se encontró en teams.csv")
            
            
        # Verificamos si el equipo visitante existe
        if name_visitante_equipo in df_teams["Equipo"].values:
            fila_equipo = df_teams.loc[df_teams["Equipo"] == name_visitante_equipo]

            id_visitante_365 = fila_equipo["ID_365"].values[0]
            name_visitante_365 = fila_equipo["Name365"].values[0]

            # Validamos si están vacíos (NaN o string vacío)
            if pd.isna(id_visitante_365) or id_visitante_365 == "":
                id_visitante_365 = input(f"🆔 Ingresá el ID_365 para el equipo '{name_visitante_equipo}': ")
                df_teams.loc[df_teams["Equipo"] == name_visitante_equipo, "ID_365"] = id_visitante_365

            if pd.isna(name_visitante_365) or name_visitante_365 == "":
                name_visitante_365 = input(f"🏷️ Ingresá el Name365 tal cual como aparece en 365 para el equipo '{name_visitante_equipo}': ")
                df_teams.loc[df_teams["Equipo"] == name_visitante_equipo, "Name365"] = name_visitante_365

            # Guardamos los cambios
            df_teams.to_csv("teams.csv", sep=";", index=False)

        else:
            print(f"❌ El equipo '{name_visitante_equipo}' no se encontró en teams.csv")
        
        
        return {"torneo": torneo_365, "name": name_365, "name_id": id_365, "name_visitante": name_visitante_365, "name_visitante_id":id_visitante_365, "torneo_id_365":torneo_365.rsplit("-", 1)[-1]}
        
    def reemplazar_texto(self, parametros):
        parametros = self.saveIdName365(parametros)
        url = f'https://www.365scores.com/es/football/match/{parametros["torneo"]}/{parametros["name"]}-{parametros["name_visitante"]}-{parametros["name_id"]}-{parametros["name_visitante_id"]}-{parametros["torneo_id_365"]}'
        return url
    
    def getAlineaciones(self, parametros):
        options = Options()
        # Ruta al perfil de usuario (ajustá según tu usuario)
        #options.add_argument(r"--user-data-dir=C:\Users\shari\AppData\Local\Google\Chrome\User Data")
        #options.add_argument(r'--profile-directory=Profile 3')


        # Modo sin interfaz gráfica
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Recomendado en modo headless (especialmente en Windows)
        options.add_argument('--disable-dev-shm-usage')  # Previene errores en contenedores
        options.add_argument('--no-sandbox')  # Evita errores en algunos entornos Linux
        options.page_load_strategy = 'eager'
        
        # Opciones útiles
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('disable-blink-features=AutomationControlled')  # Evita detección
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")
        options.add_argument("--window-size=1280,720")

        url = self.reemplazar_texto(parametros)
        alineaciones = {"local":[],
                        "visitante":[]}
        # Configuración de Selenium con ChromeDriver
        service =  Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        # ahora navegamos sin esperar eternamente
        try:
            driver.get(url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 500);")
            boton_alineaciones = driver.find_element(By.CSS_SELECTOR, "#navigation-tabs_game-center_lineups")
            driver.execute_script("arguments[0].click();", boton_alineaciones)
            time.sleep(1)
            div = driver.find_element(By.CSS_SELECTOR, "div.website_main_content__U1P3B.website_sticky_main_content__GHju6.ps--active-y")
            driver.execute_script("arguments[0].scrollTop = 280;", div)
            alineacion_local = driver.find_element(By.CSS_SELECTOR, "div.field-formation_canvas_relative_container__izlE4")          
            jugadores_local = alineacion_local.find_elements(By.CSS_SELECTOR, "div.field-formation_player_name__6Ra-B")
            alineaciones["local"] = [j.text for j in jugadores_local]
            # Para seleccionar el que NO tiene la clase 'secondary-tabs_active__ubUlv'
            boton_visitante = driver.find_element(By.CSS_SELECTOR, "div.secondary-tabs_tab_button_container__NOfV7.secondary-tabs_tab_container__Rdwyg:not(.secondary-tabs_active__ubUlv)")
            time.sleep(1)
            driver.execute_script("arguments[0].click();", boton_visitante)
            time.sleep(1)
            alineacion_visitante = driver.find_element(By.CSS_SELECTOR, "div.field-formation_canvas_relative_container__izlE4")
            jugadores_visitante = alineacion_visitante.find_elements(By.CSS_SELECTOR, "div.field-formation_player_name__6Ra-B")
            alineaciones["visitante"] = [j.text for j in jugadores_visitante]
            return alineaciones
        except Exception as e:
            print(f"Error obteniendo Ids de la URL {e}")
            

if __name__ == "__main__":
    getAlineacion = getAlineacion()
    parametros = {"name_equipo":"Mirassol","name_visitante_equipo":"Corinthians","torneo":"Brasileirão Serie A"}
    alineaciones = getAlineacion.getAlineaciones(parametros)
    print(alineaciones)