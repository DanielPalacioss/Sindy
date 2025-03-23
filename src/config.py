# Diccionario de equipos (puede ser generado dinámicamente o definido manualmente)
equipos_dict = {
    "FC Union Berlin": 1,
    "Mönchengladbach": 2,
    # Agrega más equipos según sea necesario
}

# Estadísticas a excluir
estadisticas_excluidas = ["Posición adelantada"]

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
}

# Diccionario de alineaciones
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

# Configuración de equipos objetivo (pueden ser ingresados por el usuario)
equipo_objetivo_1 = "FC Union Berlin"
equipo_objetivo_2 = "Mönchengladbach"

# URLs de los partidos (pueden ser ingresados por el usuario)
urls_equipo_1 = [...]  # Lista de URLs para el equipo 1
urls_equipo_2 = [...]  # Lista de URLs para el equipo 2

# Validación de equipos
if equipos_dict.get(equipo_objetivo_1, -1) == -1:
    raise Exception(f"El equipo {equipo_objetivo_1} no existe en la base de datos, por favor agregarlo")
if equipos_dict.get(equipo_objetivo_2, -1) == -1:
    raise Exception(f"El equipo {equipo_objetivo_2} no existe en la base de datos, por favor agregarlo")

# IDs de los equipos objetivo
equipo_objetivo_1_ID = equipos_dict.get(equipo_objetivo_1, -1)
equipo_objetivo_2_ID = equipos_dict.get(equipo_objetivo_2, -1)

# Configuración de torneo y alineaciones para el partido a predecir
Torneo = 9  # Torneo de partido a predecir (Bundesliga)
Alineacion_local = 3  # Alineación del equipo local (4-2-3-1)
Alineacion_visitante = 3  # Alineación del equipo visitante (4-2-3-1)

# Diccionario para almacenar las estadísticas de los partidos
stats = {equipo_objetivo_1: {}, equipo_objetivo_2: {}}