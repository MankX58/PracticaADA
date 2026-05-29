# 🎤 Guía de Preparación para la Sustentación Oral (ADA)

Este documento está diseñado específicamente para asegurar que obtengas el **60% de la nota** correspondiente a la presentación y sustentación técnica, basado en la rúbrica de evaluación oficial.

---

## 1. Explicación de los Algoritmos (15%)

**Objetivo:** Demostrar que entienden cómo funciona cada paso internamente sin depender de código.

### Algoritmo de Dijkstra
* **Qué es:** Es un algoritmo voraz de búsqueda de caminos más cortos para grafos con pesos no negativos.
* **Cómo funciona paso a paso:**
  1. Iniciamos asignando un costo (distancia) de 0 al nodo de inicio y de "infinito" a todos los demás.
  2. Usamos una **cola de prioridad** (`heapq`) para extraer en cada ciclo el nodo con el menor costo acumulado conocido.
  3. Al extraer un nodo, revisamos todas sus aristas conectadas (vecinos).
  4. Hacemos el proceso de **relajación**: si el costo de llegar al vecino pasando por el nodo actual es MENOR que el costo que conocíamos previamente, actualizamos su costo y metemos ese vecino a la cola.
  5. Repetimos hasta que extraemos el nodo de destino de la cola.
* **Por qué garantiza el óptimo:** Porque asume que los pesos son $\ge 0$. Una vez que extraes un nodo de la cola, es matemáticamente imposible encontrar un camino más corto hacia él en el futuro (cualquier otra ruta tendría que sumar valores positivos a un número que ya era mayor).

### Algoritmo A* (A-Estrella)
* **Qué es:** Es una mejora sobre Dijkstra que usa "inteligencia" espacial para no buscar a ciegas.
* **Cómo funciona paso a paso:**
  1. Igual que Dijkstra, pero la cola de prioridad no se ordena por el costo acumulado $g(n)$, sino por la función de costo total estimado $f(n) = g(n) + h(n)$.
  2. $g(n)$ es el costo real acumulado desde el inicio (lo mismo de Dijkstra).
  3. $h(n)$ es la **heurística** (nuestra estimación de cuánto falta para llegar). Usamos la distancia **Haversine** (distancia en línea recta).
  4. Al usar $f(n)$, el algoritmo prefiere explorar nodos que geográficamente apuntan hacia el destino, reduciendo dramáticamente la expansión radial (en todas direcciones).
* **Por qué garantiza el óptimo:** Porque nuestra heurística (línea recta) es estrictamente **admisible**: por las leyes de la geometría, nunca sobreestima el costo real (la distancia en auto por calles siempre será igual o mayor a la línea recta, jamás menor).

---

## 2. Uso de Técnicas de Diseño (10%)

**Objetivo:** Conectar el código práctico con la teoría algorítmica vista en clase.

* **Técnica Voraz (Greedy):** 
  * *Justificación:* Ambos algoritmos son inherentemente voraces porque en CADA paso toman la mejor decisión local disponible (sacar el nodo con el menor costo de la cola de prioridad). Esperan que esta serie de decisiones locales los conduzcan a la solución global óptima.
* **Programación Dinámica (Subestructura Óptima):**
  * *Justificación:* El arreglo/diccionario de `distancias` actúa como una **tabla de memoización**. El problema cumple con la propiedad de subestructura óptima: "El camino más corto de A hasta C pasando por B contiene obligatoriamente el camino más corto de A hasta B". Guardamos estas soluciones parciales óptimas para no recalcularlas, que es el núcleo del proceso de relajación de aristas.

---

## 3. Análisis de Complejidad (10%)

**Objetivo:** Justificar matemáticamente la eficiencia temporal y espacial.

* **Complejidad Temporal:** $O((V + E) \log V)$ para ambos algoritmos.
  * $V$ es el número de vértices y $E$ el número de aristas.
  * **¿De dónde sale?** Insertar y extraer todos los vértices del min-heap toma $O(V \log V)$. Relajar todas las aristas y hacer empujar (push) sus resultados al heap toma $O(E \log V)$. Sumando ambos queda $O((V + E) \log V)$.
  * *Aclaración sobre A\*:* En el peor caso absoluto, A* tiene la misma complejidad. Sin embargo, en el caso real gracias a nuestra heurística espacial, A* explora experimentalmente muchos menos vértices, volviéndose más rápido en tiempo de CPU (como se demuestra en los resultados de la interfaz).
* **Complejidad Espacial:** $O(V + E)$
  * Utilizamos una **lista de adyacencia** (implementada como diccionarios anidados de Python) que guarda $V$ nodos y $E$ aristas. Esto es inmensamente más eficiente que usar una Matriz de Adyacencia $O(V^2)$, ya que nuestro grafo de calles es extremadamente "disperso" (las calles no se conectan todas con todas).

---

## 4. Análisis de Trade-offs (15%)

**Objetivo:** Demostrar pensamiento crítico sobre decisiones de ingeniería tomadas.

* **Dijkstra vs A* (Complejidad vs Eficiencia):**
  * Ambos logran 100% de precisión.
  * El trade-off (sacrificio) de A* es que la implementación requiere conocer las coordenadas geográficas reales de cada nodo y calcular funciones trigonométricas complejas (Haversine) en cada iteración. A cambio de este ligero costo computacional (overhead), logramos una enorme ganancia en la reducción del número de nodos explorados.
* **Tiempo vs Seguridad (Parámetros Alfa y Beta):**
  * Es un trade-off social/urbano. Minimizar el riesgo ($\beta=1$) casi siempre obliga al algoritmo a dar grandes rodeos, sacrificando tiempo. Minimizar tiempo ($\alpha=1$) envía al ciudadano por la ruta más corta ignorando completamente que pueda atravesar las "zonas rojas" más peligrosas de Medellín. Nuestra función escalada ($0.5$ y $0.5$) brinda el punto medio exacto.
* **Memoria vs Búsqueda (Estructuras de Datos):**
  * Elegimos lista de adyacencia sacrificando el tiempo $O(1)$ constante que da una matriz para consultar si existe una arista directa (porque de todos modos los algoritmos iteran vecinos, no hacen consultas directas), a cambio de ahorrar enormes cantidades de memoria, haciéndolo escalable a toda la ciudad de Medellín.

---

## 5. Preguntas "Trampa" (Claridad y Dominio 10%)

* **Profesor:** *"Si A* siempre explora menos nodos y es más rápido, ¿por qué alguien seguiría usando Dijkstra?"*
  * **Respuesta:** Dijkstra no requiere que los nodos tengan atributos geográficos. Si estuviéramos buscando rutas en una topología de red de computadoras donde los "nodos" son routers sin coordenadas espaciales o GPS, A* sería inservible porque es imposible calcular una heurística geométrica admisible.
* **Profesor:** *"¿Por qué la heurística (h) tiene que multiplicarse por los pesos alfa y beta también?"*
  * **Respuesta:** Porque para que la heurística garantice ser admisible, no debe sobrepasar la función de costo real $g(n)$. Si nuestro costo real de distancia está escalado por $\alpha$ (0.5), la estimación de distancia lineal también debe reducirse al 0.5, de lo contrario la heurística estimaría un costo mayor al real, rompiendo la admisibilidad y haciendo que A* retorne rutas subóptimas.
* **Profesor:** *"Veo mapas y animaciones. ¿Usaron una librería de Machine Learning o Routing para resolver esto?"*
  * **Respuesta:** Absolutamente no. El 100% del motor lógico (Dijkstra, A*, relajación, colas de prioridad con `heapq`) fue construido analíticamente desde cero en Python puro (`grafo.py`). Librerías como `Folium` y `Streamlit` solo se utilizaron para pintar los resultados (el 5% de la rúbrica visual).
