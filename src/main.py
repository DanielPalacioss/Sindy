from scraping import setup_selenium, procesar_urls
from data_processing import calcular_desviacion_estandar_y_datos, crear_y_retornar_dataframes
from model_training import entrenar_modelo_clasificacion, entrenar_modelo_regresion, evaluar_modelo
from config import (
    torneos_dict, alineaciones_dict, Alineacion_local, Alineacion_visitante,
    equipo_objetivo_1, equipo_objetivo_2, urls_equipo_1, urls_equipo_2, stats,
    equipos_dict, estadisticas_excluidas
)
from sklearn.model_selection import train_test_split
import pandas as pd

def main():
    # Configuración de Selenium
    driver = setup_selenium()
    
    # Procesar URLs para obtener estadísticas de los partidos
    stats[equipo_objetivo_1] = procesar_urls(urls_equipo_1, equipo_objetivo_1, driver)
    stats[equipo_objetivo_2] = procesar_urls(urls_equipo_2, equipo_objetivo_2, driver)
    
    # Cerrar el navegador
    driver.quit()
    
    # Crear y retornar DataFrames con las estadísticas de los partidos
    equipos_dataframes = crear_y_retornar_dataframes(stats)
    df_equipo1 = equipos_dataframes[equipo_objetivo_1]
    df_equipo2 = equipos_dataframes[equipo_objetivo_2]
    
    # Definir las columnas para las características (X) y las etiquetas (Y)
    valores_x = [
        'Remates', 'Remates al arco', 'Pases', 'Faltas', 'Tarjetas amarillas', 'Tarjetas rojas',
        'goles_primera_mitad', 'goles_segunda_mitad', 'Posesión', 'Precisión de los pases',
        'visitante', 'local', 'Torneo', 'Alineacion', 'equipo', 'equipo_contrincante',
        'goles_totales', 'Alineacion_contrincante'
    ]
    valores_y = ['gano', 'Tiros de esquina', 'perdio', 'empato']
    valores_y_categoricas = ['gano', 'perdio', 'empato']  # Variables categóricas
    valores_y_continuas = ['Tiros de esquina']  # Variables continuas
    
    # Preparar los datos para el entrenamiento
    x = df_equipo1[valores_x]
    y = df_equipo1[valores_y]
    
    y_categoricas = y[valores_y_categoricas]
    y_continuas = y[valores_y_continuas]
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    x_train, x_test, y_train_categoricas, y_test_categoricas = train_test_split(
        x, y_categoricas, test_size=0.2, random_state=42
    )
    _, _, y_train_continuas, y_test_continuas = train_test_split(
        x, y_continuas, test_size=0.2, random_state=42
    )
    
    # Entrenar modelos
    model_clasificacion = entrenar_modelo_clasificacion(x_train, y_train_categoricas)
    model_regresion = entrenar_modelo_regresion(x_train, y_train_continuas)
    
    # Evaluar modelos
    evaluar_modelo(model_clasificacion, x_test, y_test_categoricas, tipo='clasificacion')
    evaluar_modelo(model_regresion, x_test, y_test_continuas, tipo='regresion')
    
    # Realizar predicciones
    predicciones_categoricas = model_clasificacion.predict(x_test)
    predicciones_continuas = model_regresion.predict(x_test)
    
    # Mostrar resultados
    print("Predicciones categóricas:", predicciones_categoricas)
    print("Predicciones continuas:", predicciones_continuas)

if __name__ == "__main__":
    main()