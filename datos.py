import pandas as pd
import os
import math
import ast

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

# Cache de nodos para no recalcular
_cache_nodos_cercanos = {}

def cargar_red_vial(ruta_archivo="data/calles_de_medellin_con_acoso.csv"):
    # Carga el dataset real gigante
    if os.path.exists(ruta_archivo):
        return pd.read_csv(ruta_archivo, sep=';')
    raise FileNotFoundError(f"No se encontró el dataset {ruta_archivo}")

def obtener_nombres_nodos():
    return sorted(NODOS_MEDELLIN.keys())

def obtener_coordenadas(nombre_nodo):
    return NODOS_MEDELLIN.get(nombre_nodo)

def parse_coord_string(coord_str):
    # La coord viene como '(-75.5728593, 6.2115169)' -> (lon, lat)
    # Devolvemos (lat, lon)
    try:
        tup = ast.literal_eval(coord_str)
        return (tup[1], tup[0])
    except:
        return (0, 0)

def obtener_nodo_real_cercano(nombre_poi, coordenadas_grafo):
    """
    Dado un nombre amigable (Ej: 'Poblado'), busca en todas las coordenadas del grafo
    cuál es el ID del nodo más cercano físicamente usando distancia Haversine.
    """
    if nombre_poi in _cache_nodos_cercanos:
        return _cache_nodos_cercanos[nombre_poi]
        
    lat_poi, lon_poi = NODOS_MEDELLIN[nombre_poi]
    nodo_mas_cercano = None
    distancia_minima = float('inf')
    
    for nodo_id, (lat_real, lon_real) in coordenadas_grafo.items():
        d = distancia_haversine(lat_poi, lon_poi, lat_real, lon_real)
        if d < distancia_minima:
            distancia_minima = d
            nodo_mas_cercano = nodo_id
            
    _cache_nodos_cercanos[nombre_poi] = nodo_mas_cercano
    return nodo_mas_cercano
