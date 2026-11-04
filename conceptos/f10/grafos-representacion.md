---
id: grafos-representacion
titulo: "Grafos: representación"
fase: 10
nivel: intermedio
rutas: [alg, de]
prerequisitos: [complejidad-asintotica, arrays-y-listas, tablas-hash]
tags: [grafos, estructuras, memoria, modelado]
resumen: Lista o matriz de adyacencia cambian el coste de casi todo algoritmo de grafos; elegir mal la estructura arruina un recorrido que estaba bien pensado.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 22", "Sedgewick y Wayne (2011), 'Algorithms', 4.ª ed., cap. 4"]
---

## En una frase

Un grafo se guarda como lista de vecinos por vértice o como matriz de síes y noes, y esa
elección decide el coste de cada operación posterior: consultar una arista concreta, recorrer
todos los vecinos o preguntar si dos vértices están conectados.

## La idea

Un grafo es lo más parecido a un mapa que hay en informática: un conjunto de puntos (los
**vértices** o nodos) y un conjunto de conexiones entre ellos (las **aristas**). Una red de
carreteras, una red social, las dependencias entre tareas de un pipeline, las conexiones entre
cuentas bancarias: todo eso son grafos, y en todos esos casos lo primero que hay que decidir no
es el algoritmo, sino **cómo se guarda**.

Piensa en una ciudad con 5 plazas y 7 calles que las unen. Tienes dos formas de dibujarlo en
una hoja de cálculo:

1. **Matriz de adyacencia:** una tabla de 5 × 5 donde la celda de la fila A y la columna B dice
   si hay calle de A a B (y cuánto mide, si es ponderado). Es una foto completa: para saber si
   existe una calle concreta, miras una celda. El problema es que la tabla tiene 25 celdas y
   solo 7 calles: 18 celdas dicen «no hay nada». Con 1.000 plazas, la tabla tendría un millón de
   celdas para representar unas pocas miles de calles.
2. **Lista de adyacencia:** para cada plaza, una lista con las plazas a las que llega una calle.
   Solo se guarda lo que existe. Con 5 plazas y 7 calles, se guardan 14 entradas en un grafo no
   dirigido (7, si es dirigido). Y recorrer «todas las calles que salen de A» es leer su lista,
   sin mirar nada más.

La regla práctica que sale de ahí: **casi todos los grafos del mundo real son dispersos** (cada
vértice conecta con unos pocos), así que casi siempre se usa lista de adyacencia. La matriz se
reserva para cuando el grafo es denso (cerca de todos los pares posibles conectados) o cuando
necesitas preguntar «¿existe la arista A–B?» millones de veces y quieres que esa consulta sea
O(1) sin discusión.

Lo que hace que esta decisión sea más importante de lo que parece es que cambia el coste de
**todos** los algoritmos que vienen después. Un recorrido [[bfs-y-dfs]] sobre una lista de
adyacencia cuesta O(V + E); sobre una matriz, O(V²), porque para cada vértice hay que mirar la
fila entera para encontrar sus vecinos. Y el algoritmo de [[caminos-minimos]] de Dijkstra cambia
de O((V + E) log V) a O(V²) por el mismo motivo. La estructura no es un detalle de
implementación: es la mitad del análisis.

## Definición formal

Un grafo es un par `G = (V, E)` donde:

- `V` — conjunto de vértices (o nodos). Se escribe `n = |V|` para su número.
- `E` — conjunto de aristas. Se escribe `m = |E|` para su número. En esta página se usa `m` y
  no `E` a secas para no confundir el conjunto con su tamaño.
- Si las aristas son pares **no ordenados** `{u, v}`, el grafo es **no dirigido** y la arista se
  puede recorrer en los dos sentidos.
- Si son pares **ordenados** `(u, v)`, el grafo es **dirigido** y `(u, v)` es distinto de
  `(v, u)`.
- **Ponderado** significa que cada arista lleva un número asociado (un coste, una distancia, un
  tiempo). Sin pesos, todas las aristas valen lo mismo.
- Un **bucle** es una arista de un vértice consigo mismo; una **arista múltiple** es más de una
  arista entre el mismo par. Un grafo que las admite se llama multigrafo.
- El **grado** de un vértice es su número de aristas incidentes. En un grafo no dirigido, la
  suma de todos los grados es 2m.

**Matriz de adyacencia.** Una matriz `A` de tamaño n × n con `A[u][v]` igual al peso de la
arista de `u` a `v` (o 1 si no hay pesos), y 0 o infinito cuando no hay arista. En un grafo no
dirigido, `A[u][v] = A[v][u]`: la matriz es simétrica y se guarda la mitad.

**Lista de adyacencia.** Un array de `n` listas, donde la lista de `u` contiene los pares
`(v, peso)` de las aristas que salen de `u`. En un grafo no dirigido, cada arista aparece dos
veces, una en cada extremo.

Costes comparados:

| Operación | Matriz | Lista |
| --- | --- | --- |
| Memoria | O(n²) | O(n + m) |
| ¿Existe la arista u–v? | O(1) | O(grado(u)) |
| Recorrer los vecinos de u | O(n) | O(grado(u)) |
| Recorrido completo (BFS o DFS) | O(n²) | O(n + m) |
| Añadir una arista | O(1) | O(1) |
| Borrar una arista | O(1) | O(grado(u)) |
| Añadir un vértice | O(n²) para copiar la matriz | O(1) |

Cuándo cada una:

- **Denso**: m se acerca a n² (en no dirigido, el máximo es n(n−1)/2). La matriz no desperdicia
  tanto y la consulta O(1) decide.
- **Disperso**: m es del orden de n. La lista usa memoria proporcional a lo que hay, y el
  recorrido O(n + m) es muy inferior a O(n²).
- **Con pesos**, la lista guarda el peso junto al vecino y la matriz guarda el peso en la celda.
- Un caso intermedio útil: si necesitas consultas «¿existe?» rápidas **y** recorridos baratos,
  se combinan una [[tablas-hash]] de aristas con la lista de adyacencia.

## Ejemplo

Grafo **dirigido y ponderado** con 5 vértices y 7 aristas. Los vértices son A, B, C, D y E, y
las aristas son:

```
A -> B (4)    A -> C (2)    B -> C (5)    B -> D (10)
C -> E (3)    E -> D (4)    D -> A (11)
```

La lista de adyacencia es directa: una lista por vértice con sus salidas.

```
A: (B, 4)  (C, 2)
B: (C, 5)  (D, 10)
C: (E, 3)
D: (A, 11)
E: (D, 4)
```

Total de entradas: 7, exactamente una por arista. La matriz es de 5 × 5 = 25 celdas:

```
      A    B    C    D    E
A     -    4    2    -    -
B     -    -    5   10    -
C     -    -    -    -    3
D    11    -    -    -    -
E     -    -    -    4    -
```

Contamos la diferencia: 25 celdas frente a 7 entradas. El 72 % de la matriz está vacío. Si este
grafo tuviera 10.000 usuarios y cada uno siguiera a 20, la matriz tendría **100 millones** de
celdas y la lista 200.000 entradas: un factor de 500.

Ahora los costes concretos sobre este grafo:

- «¿Existe arista de A a D?» → matriz: mirar `A[D]` = vacío, **1 operación**. Lista: recorrer
  `(B,4)` y `(C,2)`, **2 operaciones**. Con grado 20, la lista costaría 20.
- «Vecinos de A» → lista: 2 operaciones. Matriz: recorrer la fila entera, **5 operaciones**
  (y 10.000 en el grafo grande).
- Recorrido completo desde A → lista: O(n + m) = O(5 + 7) = 12. Matriz: O(n²) = 25.
- Memoria → lista: 5 listas + 7 pares. Matriz: 25 celdas.

Para este grafo pequeño las dos valen. A partir de unos miles de vértices dispersos, la matriz
deja de ser una opción y la lista gana sin discusión.

:::figura
fichero: grafos-representacion-matriz-y-lista
pie: A la izquierda, lo que ocupa cada representación en un grafo no dirigido con 5 vecinos por vértice de media: con 10.000 vértices la matriz reserva 100 millones de celdas y la lista 60.000 entradas, y la distancia entre las dos curvas crece sin techo. Los puntos morados son doce grafos dispersos al azar, medidos con la misma fórmula, para que se vea que la recta azul describe lo corriente y no un caso de laboratorio. A la derecha, el desperdicio de la matriz: con 1.000 vértices, 5 vecinos por vértice ocupan el 0,5 % de las celdas, y solo un grafo denso, con cientos de vecinos por vértice, justifica la tabla. Ese es el número que decide: la matriz se paga cuando hay que preguntar «¿existe la arista?» millones de veces, no cuando hay que recorrer el grafo.
fuente: figuras/grafos-representacion-1.py
:::

## Código

```python verificable
# Las dos representaciones del mismo grafo dirigido y ponderado.
aristas = [("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10),
           ("C", "E", 3), ("E", "D", 4), ("D", "A", 11)]

vertices = ["A", "B", "C", "D", "E"]
indice = {v: i for i, v in enumerate(vertices)}      # nombre -> posicion en la matriz

# Lista de adyacencia: solo se guarda lo que existe
adyacencia = {v: [] for v in vertices}
for u, v, w in aristas:
    adyacencia[u].append((v, w))

# Matriz de adyacencia: n x n celdas, casi todas vacias
n = len(vertices)
matriz = [[0] * n for _ in range(n)]
for u, v, w in aristas:
    matriz[indice[u]][indice[v]] = w

print("lista de A:", adyacencia["A"])                     # -> lista de A: [('B', 4), ('C', 2)]
print("celdas de la matriz:", n * n)                      # -> celdas de la matriz: 25
print("entradas de la lista:", sum(len(x) for x in adyacencia.values()))  # -> entradas de la lista: 7
print("peso de B a D por matriz:", matriz[indice["B"]][indice["D"]])      # -> peso de B a D por matriz: 10
print("peso de D a B (no existe):", matriz[indice["D"]][indice["B"]])     # -> peso de D a B (no existe): 0
```

:::claves
- `adyacencia = {v: [] for v in vertices}` crea **una lista nueva por vértice**. Con `[[]] * n` las n entradas apuntarían a la misma lista y añadir un vecino a una lo añadiría a todas; es el error de identidad clásico de Python y no da ningún error, solo un grafo imposible.
- `matriz = [[0] * n for _ in range(n)]` necesita la comprensión por el mismo motivo: `[[0] * n] * n` repite la **misma fila** n veces, y escribir una celda cambiaría la columna entera.
- La lista se indexa por el nombre del vértice y la matriz por una **posición entera**: `matriz[indice[u]][indice[v]]`. Ese mapa nombre → índice hay que construirlo aparte (aquí es el diccionario `indice`) y también cuesta.
- `adyacencia["A"]` devuelve la lista de verdad, no una copia: `adyacencia["A"].append(("D", 3))` modifica el grafo. En la matriz, `matriz[0][1]` devuelve un número, y con 0 como «no hay arista» ese 0 no distingue «no existe» de «existe con coste 0».
- `sum(len(x) for x in adyacencia.values())` cuenta 7 entradas porque el grafo del ejemplo es dirigido. En un grafo no dirigido ese número sería 2m, el doble de aristas, y confundirlo descoloca todas las cuentas de memoria.
- Cambiar `matriz = [[0] * n for _ in range(n)]` por una matriz llena de `float("inf")` cambia lo que significa una celda vacía y es lo que hace falta en cuanto hay pesos negativos: Dijkstra y Floyd-Warshall necesitan distinguir «no hay arista» de «arista de coste 0».
:::

```python verificable
# No dirigido: cada arista aparece dos veces. El grado sale de la lista.
aristas = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]

adyacencia = {}
for u, v in aristas:                 # al no ser dirigido, se anota en los dos sentidos
    adyacencia.setdefault(u, []).append(v)
    adyacencia.setdefault(v, []).append(u)

grados = {v: len(vecinos) for v, vecinos in adyacencia.items()}
print("vecinos de C:", sorted(adyacencia["C"]))            # -> vecinos de C: ['A', 'B', 'D']
print("grados:", grados)                                   # -> grados: {'A': 2, 'B': 2, 'C': 3, 'D': 1}
print("suma de grados:", sum(grados.values()))             # -> suma de grados: 8
print("2 x aristas:", 2 * len(aristas))                    # -> 2 x aristas: 8
```

```python verificable
# Cuidado con las aristas repetidas: el mismo par anotado dos veces rompe la identidad.
aristas = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("A", "B")]  # (A,B) esta dos veces

adyacencia = {}
for u, v in aristas:
    adyacencia.setdefault(u, []).append(v)
    adyacencia.setdefault(v, []).append(u)

grados = {v: len(vecinos) for v, vecinos in adyacencia.items()}
print("vecinos de A:", sorted(adyacencia["A"]))            # -> vecinos de A: ['B', 'B', 'C']
print("suma de grados:", sum(grados.values()))             # -> suma de grados: 10
print("aristas distintas:", len(set(map(frozenset, aristas))))  # -> aristas distintas: 4
```

Si tu modelo admite varias aristas entre el mismo par (vuelos entre dos ciudades, transferencias
entre dos cuentas), el multigrafo es correcto y la lista guardará las dos entradas. Si no las
admite, esa arista duplicada es un error de datos que hay que detectar antes de analizar el
grafo.

```python verificable
# Coste real: matriz cuadratica frente a lista lineal, con un grafo disperso.
import random

def memoria_estimada(n, m):
    """Celdas de la matriz frente a entradas de la lista, en unidades de referencia."""
    return n * n, n + 2 * m      # la lista no dirigida guarda cada arista dos veces

for n in (100, 1_000, 10_000):
    m = 5 * n                    # grafo disperso: 5 vecinos por vertice de media
    celdas, entradas = memoria_estimada(n, m)
    print(f"n={n:>6}  m={m:>6}  matriz={celdas:>12}  lista={entradas:>8}  factor={celdas / entradas:.0f}")
```

## Errores típicos

- **Construir una matriz de adyacencia para un grafo disperso.** Con 100.000 usuarios y 20
  contactos cada uno, la matriz pide 10.000 millones de celdas y la lista, 2 millones de
  entradas. Es el error que más memoria desperdicia de toda la familia de estructuras.
- **Olvidar la segunda dirección en un grafo no dirigido.** Al insertar la arista `(u, v)` hay
  que añadirla en la lista de `u` y en la de `v`. Si solo se añade una, el recorrido funciona en
  un sentido y falla en el otro, y el fallo es silencioso: el grafo simplemente parece tener
  menos conexiones.
- **Confundir dirigido con no dirigido al modelar.** Las dependencias entre tareas, las
  jerarquías y las relaciones «sigue a» son dirigidas; las carreteras de doble sentido y las
  amistades suelen no serlo. Si el modelo se equivoca, cualquier algoritmo posterior dará
  resultados plausibles y falsos.
- **Usar 0 como «no hay arista» en un grafo ponderado con pesos cero o negativos.** El 0 deja
  de distinguir «no hay arista» de «hay arista con coste 0», y el algoritmo de turno se cree
  conectado lo que no lo está. Usa `inf` para ausencia, o una estructura aparte.
- **Elegir la representación antes de saber qué preguntas vas a hacer.** Si el algoritmo hace
  «¿existe esta arista?» un millón de veces, la matriz gana aunque gaste memoria. Si hace
  recorridos, la lista gana. La pregunta manda sobre la estructura, no al revés.
- **Indexar por el nombre del vértice en la matriz.** Las matrices se indexan por posiciones
  enteras 0…n−1. Si los identificadores son cadenas (nombres de usuario, IPs), hace falta un
  mapa nombre → índice, que es una [[tablas-hash]], y ese paso también cuesta.

:::practica
enunciado: Un grafo no dirigido tiene 2.000 vértices y 5.000 aristas. Calcula la memoria de la matriz y de la lista de adyacencia, y compara el coste de comprobar la existencia de las 5.000 aristas en cada representación.
pista: La matriz ocupa n² celdas pase lo que pase; la lista no dirigida guarda 2m entradas y cada consulta «¿existe u–v?» recorre el grado del vértice.
solucion: Matriz: 2.000² = 4.000.000 de celdas. Lista: n + 2m = 2.000 + 10.000 = 12.000 entradas, 333 veces menos. El grado medio es 2m/n = 5. Comprobar las 5.000 aristas cuesta 5.000 operaciones con la matriz (una celda cada una) y 5.000 · 5 = 25.000 con la lista. Conclusión: la lista gana en memoria sin discusión y la matriz solo compensa si las consultas de existencia dominan el trabajo.
:::

## Comprueba que lo sabes

:::quiz
p: Un grafo no dirigido tiene 1.000 vértices y 2.000 aristas. ¿Cuántas entradas guarda la lista de adyacencia y cuántas celdas la matriz?
o: 2.000 entradas y 1.000.000 de celdas
o: 4.000 entradas y 1.000.000 de celdas
o: 4.000 entradas y 2.000 celdas
a: 2
e: En un grafo no dirigido cada arista se anota en los dos extremos, así que la lista guarda 2m = 4.000 entradas. La matriz siempre es n² = 1.000.000 de celdas, independientemente de cuántas aristas haya: esa es justo la desventaja.
:::

:::quiz
p: ¿Cuál es el coste de recorrer todos los vecinos de un vértice en cada representación?
o: O(1) en la matriz y O(n) en la lista
o: O(n) en la matriz y O(grado del vértice) en la lista
o: O(grado del vértice) en las dos
a: 2
e: En la lista solo se leen las entradas que existen, así que cuesta lo que mide la lista. En la matriz hay que recorrer la fila entera de n celdas para descubrir cuáles no están vacías. Ese detalle es el que convierte un BFS de O(n + m) en O(n²).
:::

:::trampa
La matriz de adyacencia es simétrica en un grafo no dirigido, así que se puede guardar solo la
mitad triangular. Muchas implementaciones lo olvidan y pagan el doble de memoria. Si además el
grafo es disperso, guardar la mitad de una matriz enorme sigue siendo un desperdicio: lo que
corresponde es la lista de adyacencia.
:::
