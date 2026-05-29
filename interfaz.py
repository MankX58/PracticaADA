import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from datos import cargar_red_vial, obtener_nombres_nodos, NODOS_MEDELLIN, obtener_nodo_real_cercano
from grafo import construir_grafo, dijkstra, a_estrella
from animacion import mostrar_simulacion

st.set_page_config(page_title="Rutas Medellín", page_icon="🏙️", layout="wide")

@st.cache_data
def cargar_datos(): 
    return cargar_red_vial()

def crear_mapa(grafo, res_dijkstra, res_a_estrella, inicio_str, fin_str):
    mapa = folium.Map(location=[6.2442, -75.5812], zoom_start=13, tiles="CartoDB dark_matter")
    
    # NO dibujamos todas las aristas estáticas porque ahora son 68,000 y colapsaría el navegador.
    # El mapa base CartoDB ya muestra las calles grises.

    for res, color, w, dash in [(res_dijkstra, "#3498db", 6, None), (res_a_estrella, "#e67e22", 6, "10")]:
        if res and res["encontrada"]:
            folium.PolyLine([grafo.obtener_coordenadas(n) for n in res["ruta"]], color=color, weight=w, opacity=0.9, dash_array=dash).add_to(mapa)

    for nombre, (lat, lon) in NODOS_MEDELLIN.items():
        if nombre == inicio_str: folium.Marker([lat, lon], icon=folium.Icon(color="green")).add_to(mapa)
        elif nombre == fin_str: folium.Marker([lat, lon], icon=folium.Icon(color="red")).add_to(mapa)
        else: folium.CircleMarker([lat, lon], radius=5, color="#ecf0f1", fill=True).add_to(mapa)
    return mapa

def mostrar_metricas(etiqueta, valor, color="#f2d8c2"):
    st.markdown(
        f'<div style="margin-bottom:0.15rem;">{etiqueta}</div>'
        f'<div style="color:{color}; font-size:1.35rem; font-weight:600; margin-bottom:0.6rem;">{valor}</div>',
        unsafe_allow_html=True,
    )

def main():
    st.title("Rutas Óptimas y Seguras en Medellín")
    grafo = construir_grafo(cargar_datos())
    nodos = obtener_nombres_nodos()

    with st.sidebar:
        st.header("Configuración")
        inicio = st.selectbox("Inicio", nodos, index=nodos.index("Poblado"))
        fin = st.selectbox("Destino", nodos, index=nodos.index("Aranjuez"))
        st.markdown("### Prioridad de Ruta")
        preset = st.pills(
            "Estrategia:", 
            ["Ruta más Rápida", "Ruta más Segura", "Balance Perfecto", "Ajuste Manual"], 
            default="Balance Perfecto"
        )
        if preset is None: preset = "Balance Perfecto"
        
        if "Rápida" in preset: alfa, beta = 1.0, 0.0
        elif "Segura" in preset: alfa, beta = 0.0, 1.0
        elif "Balance" in preset: alfa, beta = 0.5, 0.5
        else:
            alfa = st.slider("Distancia (α)", 0.0, 1.0, 0.5)
            beta = st.slider("Seguridad (β)", 0.0, 1.0, 0.5)
 
    if inicio == fin:
        st.warning("Inicio y destino deben ser diferentes.")
        return

    tab1, tab2 = st.tabs(["Mapa de Rutas", "Simulación en Vivo (Dijkstra vs A*)"])

    with tab1:
        # Convertir nombre amigable a nodo real del CSV
        nodo_inicio = obtener_nodo_real_cercano(inicio, grafo.coordenadas)
        nodo_fin = obtener_nodo_real_cercano(fin, grafo.coordenadas)
        
        rd = dijkstra(grafo, nodo_inicio, nodo_fin, alfa, beta)
        ra = a_estrella(grafo, nodo_inicio, nodo_fin, alfa, beta)
    
        st_folium(crear_mapa(grafo, rd, ra, inicio, fin), width=None, height=500)
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<h3 style="color: #3498db;">Dijkstra</h3>', unsafe_allow_html=True)
            if rd["encontrada"]:
                mostrar_metricas("Costo", f"{rd['costo']:.2f}", "#7fb8ff")
                mostrar_metricas("Distancia", f"{rd['distancia_total']} m", "#7fb8ff")
                mostrar_metricas("Riesgo", f"{rd['riesgo_promedio']:.2%}", "#7fb8ff")
                mostrar_metricas("Nodos Exp", rd["nodos_explorados"], "#7fb8ff")
                mostrar_metricas("Tiempo", f"{rd['tiempo_ms']:.3f} ms", "#7fb8ff")
        with col2:
            st.markdown('<h3 style="color: #e67e22;">A*</h3>', unsafe_allow_html=True)
            if ra["encontrada"]:
                mostrar_metricas("Costo", f"{ra['costo']:.2f}", "#ffb870")
                mostrar_metricas("Distancia", f"{ra['distancia_total']} m", "#ffb870")
                mostrar_metricas("Riesgo", f"{ra['riesgo_promedio']:.2%}", "#ffb870")
                mostrar_metricas("Nodos Exp", ra["nodos_explorados"], "#ffb870")
                mostrar_metricas("Tiempo", f"{ra['tiempo_ms']:.3f} ms", "#ffb870")
        with col3:
            st.subheader("Comparación")
            if rd["encontrada"] and ra["encontrada"]:
                dn = rd["nodos_explorados"] - ra["nodos_explorados"]
                dt = rd["tiempo_ms"] - ra["tiempo_ms"]
                st.metric("Ahorro Nodos A*", f"{abs(dn)}", delta=f"{'menos' if dn>0 else 'más'}")
                st.metric("Ahorro Tiempo A*", f"{abs(dt):.3f} ms", delta=f"{'rápido' if dt>0 else 'lento'}")

    with tab2:
        # Aquí también debemos usar los nodos reales
        nodo_inicio = obtener_nodo_real_cercano(inicio, grafo.coordenadas)
        nodo_fin = obtener_nodo_real_cercano(fin, grafo.coordenadas)
        mostrar_simulacion(grafo, nodo_inicio, nodo_fin, alfa, beta)

if __name__ == "__main__":
    main()
