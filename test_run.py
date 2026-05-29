import time
from datos import cargar_red_vial, obtener_nodo_real_cercano, NODOS_MEDELLIN
from grafo import construir_grafo, dijkstra

print("Cargando datos...")
df = cargar_red_vial()
print("Construyendo grafo...")
g = construir_grafo(df)

print("Nodos cargados:", len(g.obtener_nodos()))

n_poblado = obtener_nodo_real_cercano("Poblado", g.coordenadas)
n_aranjuez = obtener_nodo_real_cercano("Aranjuez", g.coordenadas)

print("Nodo Poblado:", n_poblado)
print("Nodo Aranjuez:", n_aranjuez)

t0 = time.time()
res = dijkstra(g, n_poblado, n_aranjuez)
print(f"Dijkstra finalizado en {time.time()-t0:.2f}s")
print("Encontrada:", res["encontrada"])
print("Distancia:", res["distancia_total"])
print("Nodos explorados:", res["nodos_explorados"])
