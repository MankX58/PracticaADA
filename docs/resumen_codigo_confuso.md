# 🧠 Guía Rápida: Entendiendo el Código y la Sintaxis del Proyecto

Este documento está diseñado para cualquier persona (incluso si no conoce a fondo el proyecto o de algoritmos avanzados) que quiera entender **qué hace el código** y **cómo funcionan las partes más confusas de la sintaxis** de Python que utilizamos.

---

## 1. Resumen: ¿De qué trata el código?

Este proyecto es esencialmente un "Google Maps" a pequeña escala. 
Tenemos un montón de puntos de la ciudad (nodos) y calles (aristas) que los conectan. El objetivo del código es calcular cuál es el camino más rápido (o más seguro) para ir de un punto A a un punto B, usando dos algoritmos famosos: **Dijkstra** y **A*** (A-Estrella).

Para lograr esto, el programa hace lo siguiente:
1. **Carga los datos:** Lee las calles y coordenadas de Medellín.
2. **Construye el Grafo:** Arma un mapa virtual en la memoria del computador.
3. **Explora Caminos:** Usa matemática y comparaciones lógicas para encontrar la ruta más óptima.
4. **Dibuja la Interfaz:** Muestra los resultados en un mapa web interactivo que el usuario puede controlar.

---

## 2. Las 5 Partes de Código (Sintaxis) Más Confusas Explicadas Fácilmente

A lo largo del proyecto, usamos herramientas avanzadas de Python para asegurar que los cálculos tomen milisegundos y no horas. Aquí explicamos las partes que al leer el código pueden resultar extrañas:

### 1. El uso de `float("inf")` (Infinito)
**Dónde lo usamos:** Al iniciar los algoritmos.
```python
distancias = {}
nuevo_costo = distancias.get(actual, float("inf"))
```
**¿Qué significa?**
En Python, `float("inf")` representa el número "infinito". Lo usamos como nuestro valor por defecto. Al inicio, como el algoritmo no sabe a qué distancia está el destino, asume que está a una distancia infinita. A medida que explora las calles y descubre una ruta (ej. 500 metros), reemplaza ese infinito por el número real.

### 2. La función `.get()` de los Diccionarios
**Dónde lo usamos:** Para evitar que el programa se caiga.
```python
parent = predecesores.get(actual)
```
**¿Qué significa?**
Un diccionario en Python guarda pares de datos (ej: `{"Poblado": "Aranjuez"}`). 
Si intentamos buscar una clave usando corchetes tradicionales (`predecesores["Bello"]`) y esa clave no existe en el diccionario, **el programa se detendrá abruptamente con un error llamado `KeyError`**.
Al usar la función `.get()`, le decimos a Python: *"Busca la clave. Si no existe, no te asustes ni congeles el programa, simplemente devuélveme `None` (nada) y sigue trabajando"*. Esto hace el código extremadamente robusto y a prueba de fallos.

### 3. La estructura `heapq` (Cola de Prioridad)
**Dónde lo usamos:** Es el "motor" de búsqueda de los algoritmos.
```python
import heapq
heapq.heappush(cola, (prioridad, vecino))
_, actual = heapq.heappop(cola)
```
**¿Qué significa?**
Piensa en `heapq` como la sala de triaje de urgencias de un hospital. Los pacientes no se atienden en orden de llegada (como en una fila normal), sino por **gravedad** (prioridad).
Al guardar lugares en esta cola, usamos una tupla de dos valores: `(prioridad, vecino)`. Cuando ejecutamos `heappop()`, Python nos garantiza matemáticamente que siempre sacará el elemento con el **número más pequeño en la prioridad** (es decir, el camino más corto o barato). Esto evita tener que ordenar la lista manualmente cada vez, lo cual tomaría muchísimo tiempo.

### 4. Comprensión de Diccionarios (Dictionary Comprehension)
**Dónde lo usamos:** Para crear grandes estructuras de datos en 1 sola línea.
```python
nodos_json = {n: grafo.obtener_coordenadas(n) for n in grafo.obtener_nodos()}
```
**¿Qué significa?**
Es una forma súper comprimida y elegante de hacer un ciclo repetitivo `for`. En español simple, esta línea dice:
*"Créame un nuevo diccionario. Donde la Clave será el nombre del nodo (`n`) y el Valor serán las coordenadas de ese nodo, y repite este proceso para cada nodo que exista en la lista total"*.
Python procesa estas líneas comprimidas mucho más rápido que si escribiéramos el bloque clásico de 4 líneas.

### 5. La estructura `set()` (Conjuntos Matemáticos)
**Dónde lo usamos:** Para recordar por dónde ya pasamos.
```python
visitados = set()
visitados.add(actual)
if actual in visitados: continue
```
**¿Qué significa?**
Un `set()` es como una lista, pero con dos superpoderes:
1. **No permite elementos repetidos** (si intentas agregar "Parque Berrío" dos veces, solo queda uno).
2. **Las búsquedas son instantáneas (Velocidad O(1)).** Cuando preguntamos `if actual in visitados:`, Python sabe la respuesta de inmediato, sin importar si hay 5 lugares o 10 millones guardados allí. Si usáramos una lista normal `[]`, el computador tendría que revisar la lista completa desde el primer elemento hasta el último, volviendo al programa muy ineficiente.

---

## 3. ¿Cómo funciona la "Magia" de la Interfaz Web?

Si abres `interfaz.py`, verás que armamos una página web sin escribir ni una sola línea de HTML o CSS. Eso es gracias a la librería **Streamlit**.

### El truco del "Re-run" (Re-ejecución)
En Streamlit, la página web funciona como un script que corre **de arriba hacia abajo repetitivamente**. Cada vez que el usuario mueve una barra deslizante (slider) o presiona un botón, Streamlit detecta la interacción, detiene el proceso y **vuelve a ejecutar todo el código desde la línea 1** usando los nuevos valores.

### El Decorador salvavidas: `@st.cache_data`
```python
@st.cache_data
def cargar_datos(): 
    return cargar_red_vial()
```
**¿Por qué es vital?**
Dado que Streamlit re-ejecuta todo con cada clic del usuario, si nuestro archivo de datos de las calles de Medellín pesara mucho, la página se congelaría varios segundos cada vez que mueves el slider.
Al ponerle la "etiqueta" `@st.cache_data` justo arriba de la función, le ordenamos a Python: *"Ejecuta esto solo una vez en la vida. Guarda el archivo resultante en la Memoria RAM (caché) y la próxima vez que pase por aquí, entrega el archivo directamente desde la memoria en cero segundos"*.

---

## 4. Explicando la Lógica del Algoritmo en Palabras Mortales

Si necesitas explicarle a alguien (sin tecnicismos) cómo funciona verdaderamente el corazón de nuestro código para encontrar la ruta óptima:

1. El explorador (algoritmo) se para en el **nodo inicial** (ej. Poblado).
2. Mira a todos sus **vecinos conectados directamente** y calcula el "esfuerzo" (distancia o riesgo) para llegar a ellos.
3. Anota a todos esos vecinos en su libreta (`heapq`) junto con el costo de llegar allí.
4. Revisa su libreta completa y elige al vecino anotado que represente el **menor costo histórico**, y "viaja" mentalmente hasta él.
5. Al llegar, marca ese lugar con una X (`visitados`) para jamás volver a pisarlo y entrar en círculos infinitos. Desde ahí, repite el paso 2.
6. A medida que avanza, va dejando un rastro de "migas de pan" (variable `predecesores`) anotando *"llegué aquí gracias a que venía de allá"*.
7. Al momento de pisar el **destino final** (ej. Aranjuez), se detiene, sigue las migas de pan en reversa, y así obtiene la línea perfecta que dibuja en el mapa.
