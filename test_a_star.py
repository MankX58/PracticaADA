import time
from datos import cargar_red_vial, NODOS_MEDELLIN, obtener_nodo_real_cercano
from grafo import construir_grafo, dijkstra, a_estrella

print("Loading data...")
df = cargar_red_vial("data/calles_de_medellin_con_acoso.csv")
print("Building graph...")
g = construir_grafo(df)

inicio_str = "Poblado"
fin_str = "Aranjuez"
alfa = 1.0
beta = 0.0

inicio_real = obtener_nodo_real_cercano(inicio_str, g.coordenadas)
fin_real = obtener_nodo_real_cercano(fin_str, g.coordenadas)

print("Running Dijkstra...")
rd = dijkstra(g, inicio_real, fin_real, alfa, beta)
print(f"Dijkstra explored: {rd['nodos_explorados']}")

print("Running A*...")
ra = a_estrella(g, inicio_real, fin_real, alfa, beta)
print(f"A* explored: {ra['nodos_explorados']}")
