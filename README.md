SINDY ⚽📊
Software predictivo para apuestas de fútbol

Sindy es una herramienta de machine learning diseñada para predecir resultados de partidos de fútbol y ayudar en la toma de decisiones para apuestas deportivas. Utiliza modelos avanzados de aprendizaje automático (XGBClassifier y XGBRegressor) junto con técnicas de web scraping (vía Selenium) para recopilar y analizar datos actualizados de equipos.

🔧 Requisitos y configuración

Dependencias:
ChromeDriver (compatible con tu versión de Chrome).
Python 3.8+.

Instalación

Clona el repositorio:
git clone [URL_del_repositorio]
cd Sindy

Crea y activa un entorno virtual:
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

Instala las dependencias:
pip install -r requirements.txt

🚨 Importante
Actualiza ChromeDriver:
Asegúrate de que tu versión de ChromeDriver sea compatible con tu navegador Chrome para evitar errores. Descarga la versión correcta [aquí](https://chromedriver.chromium.org/).

🛠 Funcionalidades clave
Web scraping automatizado: Extrae datos de rendimiento de equipos (goles, posesión, lesiones, etc.) usando Selenium.

Modelos de ML:

XGBClassifier: Predice resultados (victoria/empate/derrota).

XGBRegressor: Estima métricas continuas (ej. goles esperados).

Entrenamiento flexible: Los datos se actualizan automáticamente antes de cada predicción.

🔄 Mantenimiento
Si instalas nuevas dependencias, actualiza el archivo requirements.txt:
pip freeze > requirements.txt

📌 Notas
Este proyecto es un prototipo predictivo; los resultados no garantizan ganancias en apuestas.
