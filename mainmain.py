import time
import chatgpt

print("Conectando...")
time.sleep(2)

prompt = """
Hola ChatGPT, necesito que por favor:

1. Modeles el grafo vial de Medellín.
2. Implementes Dijkstra.
3. Implementes A*.
4. Midas rendimiento.
5. Hagas visualización interactiva.
6. Agregues interfaz gráfica bonita.
7. Expliques la heurística.
8. Optimices complejidad temporal.
9. Documentes todo.
10. Hagas el informe IEEE.
11. Saques 5.0 automáticamente.

Y si puedes, también hacer la exposición.
"""

print("\nEnviando trabajo...")
time.sleep(3)

resultado = chatgpt.hacer_todo(
    prompt=prompt,
    dificultad="sobrevivir",
    esfuerzo_humano=0
)

print("\nResolviendo proyecto...")
time.sleep(4)

print("\nResultado encontrado:\n")
print(resultado)

while True:
    pregunta = input("\n¿Qué falta del proyecto?: ")

    respuesta = ChatGPT.resolver(
        proyecto="ADA Medellín 2026",
        dificultad="innecesaria",
        energia_del_estudiante=-3,
        cafeina=100,
        fecha_entrega="mañana",
        codigo_funcionando=False
    )

    print("\n", respuesta)

    if "5.0" in respuesta:
        break

print("\n===================================")
print("Proyecto finalizado exitosamente")
print("Nota esperada: 5.0")
print("Autor intelectual: definitivamente nosotros")
print("Algoritmo utilizado: IA con poda emocional")
print("===================================")

#* Complejidad temporal:
# O(Lo que se demore en responder y del Wifi de la universidad)

#* Complejidad espacial:
# Depende de cuántas pestañas estén abiertas