# Rutas Óptimas y Seguras en Medellín

Proyecto para la materia Análisis y Diseño de Algoritmos (ADA).

Descripción
-----------
Este repositorio implementa una herramienta para calcular rutas óptimas en una red vial de Medellín combinando distancia y riesgo. Incluye implementación de Dijkstra y A* (con heurística Haversine), visualización interactiva con Streamlit y mapas con Folium.

Características
---------------
- Modelado del grafo con lista de adyacencia.
- Cálculo de costo lineal: `C = α·longitud + β·riesgo`.
- Algoritmos: Dijkstra y A*.
- Interfaz web interactiva con `streamlit` y `streamlit-folium`.
- Generación de mapas HTML con `folium`.

Requisitos
----------
- Python 3.8+
- Dependencias listadas en `requirements.txt`.

Instalación
-----------
1. Crear y activar un entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Ejecución
---------
- Interfaz web (Streamlit):

```powershell
streamlit run interfaz.py
```

- Interfaz de consola:

```powershell
python principal.py
```

Estructura de archivos
----------------------
- `datos.py` — Datos de nodos/aristas y utilidades.
- `grafo.py` — Construcción del grafo y algoritmos (Dijkstra, A*).
- `interfaz.py` — Interfaz web con Streamlit y funciones de visualización.
- `principal.py` — Punto de entrada en consola.
- `manual_estudiante.md` — Documentación y guía de uso.
- `mapa_rutas.html` — Ejemplo de mapa generado (salida).
- `requirements.txt` — Dependencias del proyecto.

Notas
-----
- Ajusta `α` y `β` en la interfaz para priorizar distancia o seguridad.
- La heurística Haversine garantiza que A* sea admisible con datos geográficos.

Licencia
-------
Código de ejemplo para uso académico. Añade una licencia si lo requieres.

Contacto
-------
Para dudas, usa el repositorio o contacta al autor del proyecto.
