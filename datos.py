import pandas as pd
import os
import math

def distancia_haversine(lat1, lon1, lat2, lon2):
    RADIO_TIERRA = 6_371_000
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dlat, dlon = lat2 - lat1, math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return RADIO_TIERRA * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

NODOS_MEDELLIN = {
    "Parque Berrio": (6.2518, -75.5636), "Parque Bolivar": (6.2540, -75.5680),
    "Alpujarra": (6.2450, -75.5700), "San Antonio": (6.2470, -75.5680),
    "Poblado": (6.2100, -75.5740), "Aguacatala": (6.2180, -75.5720),
    "Industriales": (6.2310, -75.5710), "Exposiciones": (6.2370, -75.5680),
    "Universidad": (6.2680, -75.5680), "Hospital": (6.2620, -75.5760),
    "Caribe": (6.2750, -75.5760), "Estadio": (6.2560, -75.5900),
    "Suramericana": (6.2500, -75.5850), "Floresta": (6.2460, -75.5960),
    "San Javier": (6.2580, -75.6120), "Laureles": (6.2450, -75.5920),
    "Belen": (6.2320, -75.5910), "Buenos Aires": (6.2390, -75.5540),
    "Aranjuez": (6.2730, -75.5580), "Castilla": (6.2830, -75.5790),
    "Envigado": (6.1740, -75.5920), "Itagui": (6.1850, -75.5990),
    "Manrique": (6.2720, -75.5480), "Robledo": (6.2740, -75.5970),
    "La America": (6.2480, -75.5980),
    "Tricentenario": (6.2904, -75.5647),
    "Pilarica": (6.2750, -75.5850),
    "Universidad de Medellin": (6.2311, -75.6115),
}

_ARISTAS_SIMULADAS = [
    ("Av del Ferrocarril T1", "Caribe", "Hospital", 850, False, 0.35),
    ("Av del Ferrocarril T2", "Hospital", "Universidad", 720, False, 0.25),
    ("Av del Ferrocarril T3", "Universidad", "Parque Bolivar", 680, False, 0.30),
    ("Av del Ferrocarril T4", "Parque Bolivar", "San Antonio", 450, False, 0.40),
    ("Av del Ferrocarril T5", "San Antonio", "Alpujarra", 380, False, 0.45),
    ("Av del Ferrocarril T6", "Alpujarra", "Exposiciones", 520, False, 0.30),
    ("Av del Ferrocarril T7", "Exposiciones", "Industriales", 610, False, 0.20),
    ("Av del Ferrocarril T8", "Industriales", "Aguacatala", 780, False, 0.15),
    ("Av del Ferrocarril T9", "Aguacatala", "Poblado", 650, False, 0.10),
    ("Calle 50 T1", "San Antonio", "Suramericana", 920, False, 0.35),
    ("Calle 50 T2", "Suramericana", "Estadio", 750, False, 0.20),
    ("Calle 50 T3", "Estadio", "Floresta", 680, False, 0.25),
    ("Calle 50 T4", "Floresta", "San Javier", 890, False, 0.55),
    ("Calle Boyaca", "Parque Berrio", "Parque Bolivar", 520, False, 0.50),
    ("Carrera Junin", "Parque Berrio", "San Antonio", 430, True, 0.45),
    ("Calle Colombia", "Parque Bolivar", "Alpujarra", 600, False, 0.40),
    ("Av Oriental Sur", "Parque Berrio", "Buenos Aires", 1100, False, 0.55),
    ("Av Oriental Norte", "Parque Berrio", "Aranjuez", 1450, False, 0.50),
    ("Carrera 70", "Laureles", "Suramericana", 580, False, 0.15),
    ("Av Nutibara", "Laureles", "Belen", 820, False, 0.20),
    ("Calle 33", "Laureles", "Floresta", 650, False, 0.18),
    ("Transversal Inferior", "Belen", "Industriales", 950, False, 0.25),
    ("Carrera 76", "Belen", "Itagui", 1200, False, 0.30),
    ("Av 80 Sur", "La America", "Laureles", 450, False, 0.22),
    ("Av 80 Centro", "La America", "Floresta", 560, False, 0.28),
    ("Av 80 Norte", "La America", "Suramericana", 620, False, 0.25),
    ("Autopista Norte", "Caribe", "Castilla", 1100, False, 0.40),
    ("Carrera 52 Norte", "Caribe", "Aranjuez", 1050, False, 0.45),
    ("Calle Barranquilla", "Universidad", "Aranjuez", 780, False, 0.35),
    ("Carrera 45", "Aranjuez", "Manrique", 650, False, 0.60),
    ("Av del Rio Norte", "Castilla", "Robledo", 900, False, 0.35),
    ("Calle 80", "Robledo", "Hospital", 1050, False, 0.30),
    ("Av 80 Occidental", "Robledo", "Estadio", 1100, False, 0.32),
    ("Carrera 65", "Estadio", "Hospital", 850, False, 0.28),
    ("Calle San Juan", "San Javier", "La America", 780, False, 0.48),
    ("Av El Poblado", "Poblado", "Envigado", 1800, False, 0.08),
    ("Calle 10 Sur", "Envigado", "Itagui", 1400, False, 0.22),
    ("Av Las Vegas", "Aguacatala", "Envigado", 1500, False, 0.12),
    ("Loma El Tesoro", "Poblado", "Industriales", 1100, True, 0.10),
    ("Av 33", "Exposiciones", "Suramericana", 780, False, 0.30),
    ("Calle 30", "Industriales", "Belen", 900, False, 0.28),
    ("Diagonal 75", "Estadio", "Robledo", 950, False, 0.33),
    ("Carrera 46", "Universidad", "Hospital", 650, False, 0.30),
    ("Calle Gardel", "Manrique", "Universidad", 1100, False, 0.55),
    ("Av Los Industriales", "Industriales", "Exposiciones", 420, False, 0.18),
    ("Callejon del Centro", "San Antonio", "Parque Berrio", 350, False, 0.70),
    ("Paseo Carabobo", "Parque Bolivar", "San Antonio", 400, False, 0.55),
    ("Via Buenos Aires", "Exposiciones", "Buenos Aires", 950, False, 0.48),
    ("Calle 45", "Aranjuez", "Parque Berrio", 1200, False, 0.52),
    ("Av Regional", "Caribe", "Exposiciones", 2100, False, 0.32),
    ("Transversal Superior", "Buenos Aires", "San Antonio", 800, False, 0.42),
    
    # Nuevas conexiones con coordenadas reales
    ("Autopista Norte T2", "Tricentenario", "Caribe", 1800, False, 0.35),
    ("Calle 104", "Tricentenario", "Castilla", 1600, False, 0.40),
    ("Calle 80 T2", "Pilarica", "Robledo", 1300, False, 0.25),
    ("Puente del Mico", "Pilarica", "Caribe", 1000, False, 0.30),
    ("Calle 30 T2", "Universidad de Medellin", "Belen", 2200, False, 0.15),
    ("Carrera 87", "Universidad de Medellin", "La America", 2400, False, 0.20),
]

def generar_datos_simulados():
    filas = []
    for nombre, origen, destino, longitud, es_una_via, riesgo in _ARISTAS_SIMULADAS:
        lat_origen, lon_origen = NODOS_MEDELLIN[origen]
        lat_destino, lon_destino = NODOS_MEDELLIN[destino]
        h = distancia_haversine(lat_origen, lon_origen, lat_destino, lon_destino)
        longitud_real = max(longitud, h * 1.05) # Asegurar admisibilidad para A*
        filas.append({
            "nombre": nombre, "origen_nombre": origen, "destino_nombre": destino,
            "origen_lat": lat_origen, "origen_lon": lon_origen,
            "destino_lat": lat_destino, "destino_lon": lon_destino,
            "longitud": round(longitud_real, 2), "es_una_via": es_una_via, "riesgo_acoso": riesgo
        })
    return pd.DataFrame(filas)

def cargar_red_vial(ruta_archivo="red_vial_medellin.csv"):
    if ruta_archivo and os.path.exists(ruta_archivo):
        return pd.read_csv(ruta_archivo)
    
    datos = generar_datos_simulados()
    if ruta_archivo:
        datos.to_csv(ruta_archivo, index=False)
    return datos

def obtener_nombres_nodos():
    return sorted(NODOS_MEDELLIN.keys())

def obtener_coordenadas(nombre_nodo):
    return NODOS_MEDELLIN.get(nombre_nodo)
