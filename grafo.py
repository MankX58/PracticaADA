import heapq
import math
import time
from datos import distancia_haversine


def calcular_costo(longitud, riesgo, alfa, beta):
    return alfa * longitud + beta * riesgo

class Grafo:
    def __init__(self):
        self.adyacencia = {}
        self.coordenadas = {}

    def agregar_nodo(self, nombre, latitud, longitud):
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = []
        self.coordenadas[nombre] = (latitud, longitud)

    def agregar_arista(self, origen, destino, longitud_metros, riesgo, nombre_calle, es_una_via=False):
        for n in (origen, destino):
            if n not in self.adyacencia: self.adyacencia[n] = []
            
        arista = {"vecino": destino, "longitud": longitud_metros, "riesgo": riesgo, "calle": nombre_calle}
        self.adyacencia[origen].append(arista)

        if not es_una_via:
            arista_inv = {"vecino": origen, "longitud": longitud_metros, "riesgo": riesgo, "calle": nombre_calle}
            self.adyacencia[destino].append(arista_inv)

    def obtener_vecinos(self, nodo): return self.adyacencia.get(nodo, [])
    def obtener_nodos(self): return list(self.adyacencia.keys())
    def obtener_coordenadas(self, nodo): return self.coordenadas.get(nodo)
    def cantidad_nodos(self): return len(self.adyacencia)
    def cantidad_aristas(self): return sum(len(v) for v in self.adyacencia.values())

def construir_grafo(datos):
    import pandas as pd
    from datos import parse_coord_string
    grafo = Grafo()
    for _, fila in datos.iterrows():
        origen_id = str(fila["origin"])
        destino_id = str(fila["destination"])
        
        lat_o, lon_o = parse_coord_string(origen_id)
        lat_d, lon_d = parse_coord_string(destino_id)
        
        grafo.agregar_nodo(origen_id, lat_o, lon_o)
        grafo.agregar_nodo(destino_id, lat_d, lon_d)
        
        riesgo = fila["harassmentRisk"]
        if pd.isna(riesgo): 
            riesgo = 0.5
            
        nombre_calle = str(fila["name"]) if not pd.isna(fila["name"]) else "Desconocida"
        
        grafo.agregar_arista(
            origen_id, destino_id, fila["length"],
            riesgo, nombre_calle, fila["oneway"]
        )
    return grafo

def _reconstruir_ruta(fin, distancias, predecesores, aristas_usadas, tiempo_ms, nodos_explorados):
    if distancias.get(fin, float("inf")) == float("inf"):
        return {"ruta": [], "costo": float("inf"), "nodos_explorados": nodos_explorados, 
                "tiempo_ms": tiempo_ms, "distancia_total": 0, "riesgo_promedio": 0, 
                "detalles_aristas": [], "encontrada": False}

    ruta, actual = [], fin
    while actual:
        ruta.append(actual)
        actual = predecesores[actual]
    ruta.reverse()

    distancia_total, riesgo_total, detalles = 0, 0, []
    for i in range(1, len(ruta)):
        a = aristas_usadas[ruta[i]]
        distancia_total += a["longitud"]
        riesgo_total += a["riesgo"]
        detalles.append({"desde": ruta[i-1], "hasta": ruta[i], "calle": a["calle"], 
                         "longitud": a["longitud"], "riesgo": a["riesgo"]})

    num = len(ruta) - 1
    riesgo_promedio = riesgo_total / num if num > 0 else 0

    return {"ruta": ruta, "costo": distancias[fin], "nodos_explorados": nodos_explorados, 
            "tiempo_ms": tiempo_ms, "distancia_total": distancia_total, 
            "riesgo_promedio": round(riesgo_promedio, 4), "detalles_aristas": detalles, "encontrada": True}

def algoritmo_base(grafo, inicio, fin, alfa, beta, usar_heuristica=False):
    t0 = time.perf_counter()
    distancias = {n: float("inf") for n in grafo.obtener_nodos()}
    distancias[inicio] = 0
    predecesores, aristas_usadas = {n: None for n in grafo.obtener_nodos()}, {}
    visitados, nodos_explorados = set(), 0
    cola = [(0, inicio)]

    coord_fin = grafo.obtener_coordenadas(fin) if usar_heuristica else None

    while cola:
        _, actual = heapq.heappop(cola)
        if actual in visitados: continue
        visitados.add(actual)
        nodos_explorados += 1
        if actual == fin: break

        for a in grafo.obtener_vecinos(actual):
            v = a["vecino"]
            if v not in visitados:
                nuevo_costo = distancias[actual] + calcular_costo(a["longitud"], a["riesgo"], alfa, beta)
                if nuevo_costo < distancias[v]:
                    distancias[v] = nuevo_costo
                    predecesores[v] = actual
                    aristas_usadas[v] = a
                    
                    prioridad = nuevo_costo
                    if usar_heuristica:
                        coord_v = grafo.obtener_coordenadas(v)
                        h = distancia_haversine(coord_v[0], coord_v[1], coord_fin[0], coord_fin[1]) * alfa
                        prioridad += h
                        
                    heapq.heappush(cola, (prioridad, v))

    return _reconstruir_ruta(fin, distancias, predecesores, aristas_usadas, (time.perf_counter() - t0)*1000, nodos_explorados)

def dijkstra(grafo, inicio, fin, alfa=1.0, beta=0.0):
    """
    Algoritmo de Dijkstra para encontrar la ruta de costo mínimo.
    
    Análisis de Complejidad:
    - Temporal: O(N log N), donde N es el número de nodos.
      Insertar y extraer del min-heap toma O(log N), y en el peor caso se hace 
      para cada calle o intersección.
    - Espacial: O(N) para la representación del grafo en lista de adyacencia,
      y estructuras auxiliares.
    """
    return algoritmo_base(grafo, inicio, fin, alfa, beta, usar_heuristica=False)

def a_estrella(grafo, inicio, fin, alfa=1.0, beta=0.0):
    """
    Algoritmo A* (A-Estrella) utilizando Distancia Haversine como heurística.
    
    Análisis de Complejidad:
    - Temporal: O(N log N) en el peor caso teórico. Sin embargo, en la 
      práctica explora significativamente menos nodos que Dijkstra gracias a la 
      heurística espacial que dirige la búsqueda hacia el destino.
    - Espacial: O(N) idéntico a Dijkstra.
    """
    return algoritmo_base(grafo, inicio, fin, alfa, beta, usar_heuristica=True)
