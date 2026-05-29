import streamlit as st
import streamlit.components.v1 as components
import json
import heapq
import time
from datos import distancia_haversine

def obtener_pasos_animacion(grafo_obj, inicio, fin, w_dist, w_riesgo, usar_heuristica=False):
    distancias = {n: float("inf") for n in grafo_obj.obtener_nodos()}
    distancias[inicio] = 0
    predecesores = {n: None for n in grafo_obj.obtener_nodos()}
    visitados = set()
    cola = [(0, inicio)]
    coord_fin = grafo_obj.obtener_coordenadas(fin) if usar_heuristica else None
    
    pasos = []
    
    while cola:
        _, actual = heapq.heappop(cola)
        if actual in visitados: continue
        visitados.add(actual)
        
        parent = predecesores[actual]
        pasos.append({"node": actual, "parent": parent})
        
        if actual == fin:
            break
            
        for a in grafo_obj.obtener_vecinos(actual):
            v = a["vecino"]
            if v not in visitados:
                nuevo_costo = distancias[actual] + (w_dist * a["longitud"] + w_riesgo * a["riesgo"])
                if nuevo_costo < distancias[v]:
                    distancias[v] = nuevo_costo
                    predecesores[v] = actual
                    prioridad = nuevo_costo
                    if usar_heuristica:
                        coord_v = grafo_obj.obtener_coordenadas(v)
                        h = distancia_haversine(coord_v[0], coord_v[1], coord_fin[0], coord_fin[1]) * w_dist
                        prioridad += h
                    heapq.heappush(cola, (prioridad, v))
                    
    ruta = []
    if distancias[fin] != float("inf"):
        actual = fin
        while actual:
            ruta.append(actual)
            actual = predecesores[actual]
        ruta.reverse()
        
    return pasos, ruta

def mostrar_simulacion(grafo, inicio, fin, alfa, beta):
    st.markdown("Observa paso a paso cómo busca cada algoritmo sin interrupciones. La animación trazará las líneas de exploración formando el árbol de búsqueda.")
    
    col_btn, col_slider = st.columns([1, 2])
    with col_slider:
        velocidad = st.slider("Velocidad de la animación (ms por paso)", 10, 500, 50, step=10)
    
    with col_btn:
        st.write("") # Espaciador
        # Botón maestro en Streamlit para compilar la animación inicial
        if st.button("Iniciar Simulación", use_container_width=True, type="primary"):
            st.session_state["run_sim"] = True
            st.session_state["sim_key"] = time.time()  
        
    if st.session_state.get("run_sim", False):
        with st.spinner("Preparando animación..."):
            nodos_json = {n: grafo.obtener_coordenadas(n) for n in grafo.obtener_nodos()}
            aristas_json = []
            for n, vecinos in grafo.adyacencia.items():
                for v in vecinos:
                    aristas_json.append([n, v["vecino"]])
                    
            pasos_d, ruta_d = obtener_pasos_animacion(grafo, inicio, fin, alfa, beta, False)
            pasos_a, ruta_a = obtener_pasos_animacion(grafo, inicio, fin, alfa, beta, True)
            
            sim_key = st.session_state.get("sim_key", 0)
            
            html_code = f"""
            <!-- Animation Key: {sim_key} -->
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <style>
                    body {{ margin: 0; padding: 0; display: flex; font-family: sans-serif; position: relative; }}
                    .map-container {{ flex: 1; height: 100vh; position: relative; }}
                    #map-dijkstra {{ height: 100%; border-right: 2px solid #ccc; }}
                    #map-astar {{ height: 100%; }}
                    .title {{ position: absolute; top: 10px; left: 50px; z-index: 1000; background: white; padding: 5px 15px; border-radius: 8px; font-weight: bold; border: 2px solid #333; box-shadow: 2px 2px 5px rgba(0,0,0,0.3); }}
                    .stats {{ position: absolute; bottom: 20px; left: 50px; z-index: 1000; background: white; padding: 10px; border-radius: 8px; border: 2px solid #333; font-size: 14px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3); }}
                    .btn-reload {{ position: absolute; bottom: 20px; right: 20px; z-index: 2000; padding: 10px 20px; font-weight: bold; font-size: 14px; background: #34495e; color: white; border: 1px solid #2c3e50; border-radius: 8px; cursor: pointer; box-shadow: 2px 2px 8px rgba(0,0,0,0.3); transition: background 0.2s, transform 0.1s; }}
                    .btn-reload:hover {{ background: #2c3e50; transform: scale(1.02); }}
                    .btn-reload:active {{ transform: scale(0.98); }}
                </style>
            </head>
            <body>
                <button class="btn-reload" onclick="location.reload()">Reiniciar animación</button>
                <div class="map-container">
                    <div class="title" style="color: #c0392b;">Dijkstra (Explora radialmente)</div>
                    <div id="stats-d" class="stats">Nodos explorados: 0</div>
                    <div id="map-dijkstra"></div>
                </div>
                <div class="map-container">
                    <div class="title" style="color: #2980b9;">A* (Explora directo al destino)</div>
                    <div id="stats-a" class="stats">Nodos explorados: 0</div>
                    <div id="map-astar"></div>
                </div>
    
                <script>
                    const nodes = {json.dumps(nodos_json)};
                    const edges = {json.dumps(aristas_json)};
                    const stepsDijkstra = {json.dumps(pasos_d)};
                    const stepsAstar = {json.dumps(pasos_a)};
                    const routeDijkstra = {json.dumps(ruta_d)};
                    const routeAstar = {json.dumps(ruta_a)};
                    const speedMs = {velocidad};
    
                    function initMap(divId) {{
                        const m = L.map(divId, {{ zoomControl: false }}).setView([6.25, -75.58], 12);
                        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                            attribution: '&copy; OpenStreetMap'
                        }}).addTo(m);
                        
                        edges.forEach(e => {{
                            const p1 = nodes[e[0]];
                            const p2 = nodes[e[1]];
                            if(p1 && p2) {{
                                L.polyline([p1, p2], {{color: '#E0E0E0', weight: 2, opacity: 0.5}}).addTo(m);
                            }}
                        }});
                        
                        L.circleMarker(nodes["{inicio}"], {{radius: 8, color: "green", fillColor: "green", fillOpacity: 1}}).addTo(m);
                        L.circleMarker(nodes["{fin}"], {{radius: 8, color: "gold", fillColor: "gold", fillOpacity: 1}}).addTo(m);
                        
                        return m;
                    }}
    
                    const mapD = initMap('map-dijkstra');
                    const mapA = initMap('map-astar');
    
                    function animate(map, steps, route, color, statsId) {{
                        let i = 0;
                        const activeMarker = L.circleMarker([-90, 0], {{radius: 8, color: 'orange', fillColor: 'orange', fillOpacity: 1}}).addTo(map);
                        const statsDiv = document.getElementById(statsId);
                        
                        const interval = setInterval(() => {{
                            if (i >= steps.length) {{
                                clearInterval(interval);
                                map.removeLayer(activeMarker);
                                
                                for(let j=1; j<route.length; j++) {{
                                    const p1 = nodes[route[j-1]];
                                    const p2 = nodes[route[j]];
                                    L.polyline([p1, p2], {{color: '#00FF00', weight: 6, opacity: 0.9}}).addTo(map);
                                }}
                                statsDiv.innerHTML = `¡Completado! Nodos explorados: <b>${{steps.length}}</b>`;
                                return;
                            }}
                            
                            const step = steps[i];
                            const nodePos = nodes[step.node];
                            
                            activeMarker.setLatLng(nodePos);
                            
                            if (step.parent) {{
                                const parentPos = nodes[step.parent];
                                L.polyline([parentPos, nodePos], {{color: color, weight: 4, opacity: 0.6}}).addTo(map);
                            }}
                            
                            L.circleMarker(nodePos, {{radius: 4, color: color, fillColor: color, fillOpacity: 0.8}}).addTo(map);
                            
                            statsDiv.innerHTML = `Explorando: <b>${{step.node}}</b><br>Nodos analizados: ${{i+1}} / ${{steps.length}}`;
                            
                            i++;
                        }}, speedMs);
                    }}
    
                    animate(mapD, stepsDijkstra, routeDijkstra, 'red', 'stats-d');
                    animate(mapA, stepsAstar, routeAstar, 'blue', 'stats-a');
                </script>
            </body>
            </html>
            """
            
            # Truco infalible: alternar la altura por 1 pixel fuerza a Streamlit a destruir y recrear el iframe por completo
            altura = 620 if int(sim_key * 1000) % 2 == 0 else 621
            components.html(html_code, height=altura)
    else:
        st.info("👆 Selecciona tu configuración y haz clic en 'Generar Simulación'.")
