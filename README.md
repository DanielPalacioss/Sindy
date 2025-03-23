# Sindy
Software predictivo para apuestas de futbol usando Machine Learning.

1) Recordar que el chrome driver debe estar lo mas actualizado posible y el chrome igual, para que no hayan problemas de incompatibilidad o errores. O usar un chromeDriver compatible con la version que tengais de Chrome.

2) Se necesita instalar los requirements para un buen uso del software y evitar errores: pip install -r requirements.txt

3) Se ejecuta el python main.py

Estructura del proyecto:

/Sindy/
│
├── /config/                  # Carpeta para archivos de configuración
│   └── config.py             # Configuraciones globales (diccionarios, listas, etc.)
│
├── /scraping/                # Carpeta para el módulo de scraping
│   └── scraping.py           # Lógica de scraping y obtención de estadísticas
│
├── /data_processing/         # Carpeta para el módulo de procesamiento de datos
│   └── data_processing.py    # Lógica de procesamiento y cálculo de estadísticas
│
├── /model_training/          # Carpeta para el módulo de entrenamiento de modelos
│   └── model_training.py     # Lógica de entrenamiento y evaluación de modelos
│
├── /utils/                   # Carpeta para utilidades adicionales
│   └── utils.py            # Funciones auxiliares (opcional)
│
├── main.py                   # Punto de entrada del programa
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación del proyecto