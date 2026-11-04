---
id: bfs-y-dfs
titulo: Recorridos BFS y DFS
fase: 10
nivel: intermedio
rutas: [alg]
prerequisitos: [grafos-representacion, pilas-y-colas, complejidad-asintotica]
tags: [grafos, recorridos, bfs, dfs]
resumen: Dos formas de visitar todos los vértices de un grafo; la primera explora por capas y da distancias, la segunda se hunde y descubre ciclos, caminos y componentes.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 22", "Moore (1959), 'The shortest path through a maze'"]
---

## En una frase

BFS visita el grafo por capas —primero todo lo que está a un paso, luego a dos— y por eso
calcula distancias mínimas en grafos sin pesos; DFS se hunde todo lo que puede antes de
retroceder y por eso descubre ciclos, caminos y órdenes topológicos.

## La idea

Imagina que tiras una piedra en un estanque. Las ondas se expanden en círculos: primero el
anillo a un metro, luego el de dos, luego el de tres. Nunca aparece agua a tres metros antes de
que haya aparecido a dos. Ese es el recorrido en anchura (**BFS**, *breadth-first search*): se
explora por capas, y el número de capa es exactamente la distancia mínima al origen contada en
aristas.

Ahora imagina que recorres un laberinto con la mano pegada a la pared derecha: avanzas todo lo
que puedes por el primer pasillo, y solo cuando te bloqueas retrocedes hasta la última
bifurcación y pruebas la otra rama. Ese es el recorrido en profundidad (**DFS**,
*depth-first search*): se hunde antes de ensanchar.

Los dos visitan todos los vértices y cuestan lo mismo, O(n + m) con lista de adyacencia. La
diferencia está en **qué información producen por el camino**:

- **BFS produce distancias en número de aristas.** Es el algoritmo correcto para «el camino más
  corto» cuando todas las aristas valen lo mismo: menos saltos. Si las aristas tienen pesos
  distintos, BFS da el camino con menos paradas, que no es el más barato; eso es trabajo de
  [[caminos-minimos]].
- **BFS produce el árbol de caminos mínimos**, del que se reconstruye la ruta concreta hacia
  cualquier vértice.
- **DFS produce un bosque de árboles de profundidad** y, sobre todo, marcas de entrada y salida
  por vértice. Esas marcas son la base para detectar ciclos, ordenar tareas por dependencias
  (orden topológico), encontrar componentes fuertemente conexas y resolver laberintos con
  retroceso.
- **DFS es lo que usas cuando el grafo es enorme y solo quieres saber si hay camino.** Se hunde
  hacia el objetivo sin explorar las capas enteras que BFS necesita guardar en memoria.

La elección de la estructura es lo único que cambia entre los dos: BFS usa una **cola** (primero
en entrar, primero en salir) y DFS usa una **pila** (último en entrar, primero en salir) o la
propia pila de llamadas con recursión. Ambas están en [[pilas-y-colas]]. Esa es la lección que
hace clic: los dos recorridos son el mismo bucle con distinto contenedor.

## Definición formal

Sea `G = (V, E)` con `n = |V|` vértices y `m = |E|` aristas, representado con
[[grafos-representacion|lista de adyacencia]]. Un recorrido parte de un vértice `s` y visita
cada vértice alcanzable exactamente una vez.

**BFS.** Usa una cola `Q` y un array `dist` donde `dist[v]` es la distancia mínima en aristas
de `s` a `v`, con `dist[s] = 0`.

1. Marca `s` como visitado y encólalo con `dist[s] = 0`.
2. Mientras `Q` no esté vacía: saca `u` del principio, y para cada vecino `v` sin visitar,
   márcalo, asígnale `dist[v] = dist[u] + 1` y encólalo.

Propiedades:

- `dist[v]` es el **mínimo** número de aristas de `s` a `v`. Es la razón de que BFS resuelva
  «menos saltos».
- Los vértices salen de la cola en orden no decreciente de `dist`: nunca sale uno de capa 3
  antes de que hayan salido todos los de capa 2.
- Complejidad: O(n + m) con lista de adyacencia; O(n²) con matriz.
- Memoria: O(n) para la cola. En un grafo ancho, la cola puede contener casi todos los vértices
  a la vez; en eso DFS le gana.

**DFS.** Usa una pila (o recursión) y dos marcas por vértice: `entrada[v]` y `salida[v]`, que
son el instante en que se descubre y el instante en que se termina de explorar.

1. Para cada vértice `u`: si no está visitado, márcalo con `entrada[u] = t`, incrementa `t`, y
   recorre cada vecino `v` sin visitar llamando a DFS sobre `v`.
2. Al volver de todos los vecinos, marca `salida[u] = t` e incrementa `t`.

Propiedades:

- **Clasificación de aristas** con `entrada` y `salida`: una arista `(u, v)` es de **árbol** si
  `v` estaba sin visitar; de **retroceso** si `v` es un ancestro de `u` (lo que demuestra un
  ciclo); de **avance** o de **cruce** en el resto de los casos.
- **Hay ciclo** en un grafo dirigido si y solo si DFS encuentra una arista de retroceso.
- **Orden topológico:** el orden decreciente de `salida` de un grafo dirigido acíclico es un
  orden válido de dependencias.
- Complejidad: O(n + m) con lista de adyacencia.
- Memoria: O(n) para las marcas más O(profundidad) para la pila, que puede llegar a n.

**Comparación directa:**

| Aspecto | BFS | DFS |
| --- | --- | --- |
| Contenedor | cola (FIFO) | pila (LIFO) o recursión |
| Orden de visita | por capas, en anchura | por ramas, en profundidad |
| Distancias sin pesos | sí, mínimas | no |
| Camino más corto con pesos | no | no: eso es Dijkstra |
| Detectar ciclos | con conteo de grados entrantes | con marcas de entrada y salida |
| Orden topológico | con el algoritmo de Kahn | con el orden de salida |
| Memoria en grafo ancho | alta, la cola crece | baja, solo la pila actual |
| Memoria en grafo profundo | baja | alta, riesgo de desbordar la pila |

## Ejemplo

Grafo no dirigido con 7 vértices y 7 aristas:

```
aristas: 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 4-5
```

La 4-5 cierra un ciclo: 1 → 2 → 4 → 5 → 2. Las listas de adyacencia, con los vecinos en orden
creciente, son:

```
1: 2, 3
2: 1, 4, 5
3: 1, 6
4: 2, 5
5: 2, 4
6: 3, 7
7: 6
```

**BFS desde el vértice 1**, con cola:

| Paso | Cola al empezar | Se saca | Se encolan | dist |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 2, 3 | dist[1]=0 |
| 2 | [2, 3] | 2 | 4, 5 | dist[2]=1 |
| 3 | [3, 4, 5] | 3 | 6 | dist[3]=1 |
| 4 | [4, 5, 6] | 4 | nada nuevo | dist[4]=2 |
| 5 | [5, 6] | 5 | nada nuevo | dist[5]=2 |
| 6 | [6] | 6 | 7 | dist[6]=2 |
| 7 | [7] | 7 | nada nuevo | dist[7]=3 |

- Orden de visita: **1, 2, 3, 4, 5, 6, 7**.
- Distancias: 1 → 0; 2 y 3 → 1; 4, 5 y 6 → 2; 7 → 3. Fíjate en que la 7 sale la última porque
  está a tres saltos pasando por 3 y 6. No hay forma de llegar en menos: el único vecino de 7 es
  6, y 6 solo conecta con 3, que está a un salto de 1.
- El camino mínimo de 1 a 7 es 1 → 3 → 6 → 7, con 3 aristas.

**DFS desde el vértice 1**, con recursión y vecinos en orden creciente:

```
1 -> 2 -> 4 -> 5 -> (2 ya visitado, 4 ya visitado) -> vuelve a 4 -> vuelve a 2
   -> 5 ya visitado -> vuelve a 1
   -> 3 -> 6 -> 7 -> vuelve a 6 -> vuelve a 3 -> vuelve a 1
```

- Orden de visita (entrada): **1, 2, 4, 5, 3, 6, 7**.
- Fíjate en la diferencia: el vértice 5 está a 2 aristas de 1 y el vértice 4 también, pero DFS
  entra en la rama 2 → 4 → 5 y solo después vuelve a mirar el 3. BFS, en cambio, tiene claras
  las capas: 2 y 3 en la primera, 4, 5 y 6 en la segunda, 7 en la tercera. Con el 7 el contraste
  es máximo: DFS lo alcanza al final de una rama larga, mientras BFS sabe que está exactamente a
  3 saltos y lo demuestra.

Ese contraste es el resumen de todo: **mismo grafo, mismos vértices, información distinta según
el contenedor**.

:::figura
fichero: bfs-y-dfs-capas-y-ramas
pie: El mismo grafo de 7 vértices y 7 aristas, con el mismo orden de vecinos, recorrido de las dos formas. A la izquierda, BFS: cada vértice lleva su capa escrita dentro, que es la distancia mínima en aristas al 1, y el aro se colorea por capa; las aristas gruesas son el árbol de caminos mínimos. A la derecha, DFS: el número con º es el orden de entrada y las aristas gruesas son su árbol de profundidad, que no es el mismo (el 5 entra desde el 4 y no desde el 2, así que la arista que sobra cambia de panel). Lo que hay que comparar es el vértice 3: BFS lo visita tercero porque está a un salto de distancia; DFS lo visita quinto, porque antes se hundió en la rama 2 → 4 → 5. Los dos visitan los siete vértices y cuestan O(n + m), pero solo BFS produce la distancia mínima.
fuente: figuras/bfs-y-dfs-1.py
:::

## Código

```python verificable
from collections import deque

grafo = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6],
    4: [2, 5],
    5: [2, 4],
    6: [3, 7],
    7: [6],
}

def bfs(grafo, inicio):
    """Devuelve el orden de visita y las distancias en aristas."""
    visitado = {inicio}
    cola = deque([inicio])          # FIFO: lo que entra primero sale primero
    orden, dist = [], {inicio: 0}
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in grafo[u]:
            if v not in visitado:
                visitado.add(v)     # se marca AL ENCOLAR, no al desencolar
                dist[v] = dist[u] + 1
                cola.append(v)
    return orden, dist

orden, dist = bfs(grafo, 1)
print("orden BFS:", orden)                      # -> orden BFS: [1, 2, 3, 4, 5, 6, 7]
print("distancias:", dist)                      # -> distancias: {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3}
print("distancia a 7:", dist[7])                # -> distancia a 7: 3
```

:::claves
- `cola.popleft()` cuesta O(1); con una lista normal, `lista.pop(0)` cuesta O(n) porque desplaza todos los elementos hacia la izquierda, y el recorrido entero se vuelve O(n²) sin que el código lo diga.
- `visitado.add(v)` va dentro del `if` y **antes** de `cola.append(v)`: se marca al encolar, no al desencolar. Si se marcara al desencolar, el mismo vértice entraría varias veces en la cola y `dist` podría quedar mal.
- `dist` es un diccionario que se construye a la vez que el recorrido, y el primer valor escrito para un vértice es el definitivo: BFS saca los vértices en orden no decreciente de distancia, y esa es toda la garantía.
- `orden` es una lista (el orden de visita) y `visitado` un conjunto: comprobar `v in visitado` cuesta O(1) de media, mientras que buscar en `orden` costaría O(n). Cambiar `visitado` por una lista multiplica el coste sin cambiar el resultado.
- `deque([inicio])` se construye con una lista de un elemento: `deque(inicio)` lanzaría `TypeError: 'int' object is not iterable`, porque el constructor espera un iterable y `inicio` es un entero.
- Cambiar `popleft()` por `pop()` convierte este BFS en un DFS sin tocar nada más. El contenedor es lo único que decide el orden de visita.
:::

```python verificable
grafo = {
    1: [2, 3],
    2: [1, 4, 5],
    3: [1, 6],
    4: [2, 5],
    5: [2, 4],
    6: [3, 7],
    7: [6],
}

def dfs_iterativo(grafo, inicio):
    """DFS con pila explicita: sin recursion, sin riesgo de desbordar."""
    visitado = {inicio}
    pila = [inicio]                 # LIFO: lo ultimo que entro sale primero
    orden = []
    while pila:
        u = pila.pop()
        orden.append(u)
        for v in reversed(grafo[u]):   # reversed para respetar el orden de los vecinos
            if v not in visitado:
                visitado.add(v)
                pila.append(v)
    return orden

def dfs_recursivo(grafo, u, visitado, orden):
    visitado.add(u)
    orden.append(u)
    for v in grafo[u]:
        if v not in visitado:
            dfs_recursivo(grafo, v, visitado, orden)

orden, visitado = [], set()
dfs_recursivo(grafo, 1, visitado, orden)

print("DFS recursivo:", orden)                      # -> DFS recursivo: [1, 2, 4, 5, 3, 6, 7]
print("DFS iterativo:", dfs_iterativo(grafo, 1))    # -> DFS iterativo: [1, 2, 4, 5, 3, 6, 7]
print("componentes alcanzables desde 1:", len(visitado))  # -> componentes alcanzables desde 1: 7
```

```python verificable
# Deteccion de ciclos: BFS por grados de entrada (Kahn) frente a DFS con marcas.
aristas = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]     # DAG: sin ciclos
aristas_ciclicas = [(1, 2), (2, 3), (3, 1), (3, 4)]

def orden_topologico(n, aristas):
    """Kahn: si al final no se han sacado todos, hay ciclo."""
    from collections import deque
    entrantes = {i: 0 for i in range(1, n + 1)}
    salidas = {i: [] for i in range(1, n + 1)}
    for u, v in aristas:
        salidas[u].append(v)
        entrantes[v] += 1
    cola = deque(sorted(i for i in entrantes if entrantes[i] == 0))
    orden = []
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in salidas[u]:
            entrantes[v] -= 1
            if entrantes[v] == 0:
                cola.append(v)
    return orden if len(orden) == n else None

print("DAG ordenado:", orden_topologico(5, aristas))              # -> DAG ordenado: [1, 2, 3, 4, 5]
print("con ciclo:", orden_topologico(4, aristas_ciclicas))        # -> con ciclo: None
```

## Errores típicos

- **Marcar los vértices como visitados al desencolarlos en vez de al encolarlos.** En BFS, el
  mismo vértice puede entrar en la cola varias veces antes de ser procesado, y con ello se
  duplica el trabajo: el coste deja de ser O(n + m) y el `dist` puede quedar mal. Se marca en el
  momento de encolar.
- **Usar BFS para el camino más corto con pesos.** BFS cuenta aristas, no suma pesos. Si las
  aristas valen 1, 7 y 2, el camino con menos saltos puede ser el más caro. Eso lo resuelve
  [[caminos-minimos]] con Dijkstra o Bellman-Ford.
- **Implementar DFS con recursión sobre un grafo enorme y profundo.** La pila de llamadas tiene
  un límite (en Python, 1.000 marcos por defecto). Un grafo en cadena de 100.000 vértices revienta
  con `RecursionError`; la versión con pila explícita no tiene ese problema.
- **No reiniciar el recorrido para grafos desconectados.** Un solo BFS o DFS desde `s` solo
  alcanza la **componente conexa** de `s`. Para contar componentes, para saber si el grafo es
  conexo o para etiquetar grupos hay que lanzar el recorrido desde cada vértice no visitado.
- **Confundir «hay ciclo» con «hay arista repetida».** En un grafo no dirigido, encontrar un
  vecino ya visitado no siempre es un ciclo: puede ser la misma arista vista desde el otro
  extremo. Hay que excluir el vértice del que vienes, o comparar por identidad de arista.
- **Creer que DFS visita «lo más cercano primero».** DFS puede llegar al destino en 2 pasos o en
  100 según el orden de los vecinos en la lista. Si el resultado depende del orden de la lista
  de adyacencia, estás usando la herramienta equivocada para preguntar por distancias.

:::practica
enunciado: Grafo no dirigido con aristas 1-2, 1-3, 2-4, 2-5, 5-6 y 3-6. ¿Cuál es la distancia mínima de 1 a 6 con BFS? ¿Y cuántas aristas usa el árbol de DFS, con vecinos en orden creciente, para llegar a 6?
pista: BFS usa una cola y marca al encolar, así que el número de capa es la distancia; DFS se hunde por la primera rama.
solucion: BFS: sale 1 (distancia 0), entran 2 y 3 (1), luego 4 y 5 (2); al sacar el 3 entra el 6 con distancia 2, por el camino 1 → 3 → 6. DFS: 1 → 2 → 4 → 5 → 6 → 3, así que su camino a 6 es 1 → 2 → 5 → 6, tres aristas. Conclusión: los dos visitan los 6 vértices, pero solo BFS demuestra que 6 está a dos saltos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas afirmaciones distingue correctamente BFS de DFS en un grafo sin pesos?
o: BFS da la distancia mínima en aristas desde el origen; DFS da un camino, pero no necesariamente el más corto
o: BFS solo funciona en grafos dirigidos y DFS en no dirigidos
o: DFS recorre el grafo con una cola y BFS con una pila
a: 1
e: La cola obliga a BFS a explorar por capas, y por eso el número de capa es la distancia mínima en aristas. DFS se hunde por la primera rama que encuentra y puede dar un camino mucho más largo. Los contenedores son justo al revés de lo que dice la tercera opción: BFS usa una cola y DFS una pila (o la recursión), y los dos funcionan en grafos dirigidos y no dirigidos.
:::

:::quiz
p: Recorres un grafo no dirigido con BFS desde 1 y con DFS desde 1 y obtienes órdenes distintos. ¿Por qué?
o: Porque BFS usa una cola y DFS una pila, y eso cambia el orden en que se sacan los vértices pendientes
o: Porque BFS y DFS visitan conjuntos distintos de vértices
o: Porque DFS no visita los vértices ya visitados por otras ramas
a: 1
e: Los dos visitan exactamente los mismos vértices alcanzables, pero el contenedor decide cuál se procesa primero: la cola respeta el orden de llegada (capas) y la pila da prioridad al último que entró (profundidad). De ahí que los órdenes difieran sin que ninguno esté mal.
:::

:::trampa
En BFS, comprobar si el vértice ya está en la cola es distinto de comprobar si ya está visitado.
La forma robusta es marcar en el momento de encolar y usar esa marca como condición, porque
buscar dentro de la cola cuesta O(n) y convierte el algoritmo en O(n²) sin que se note en
grafos pequeños.
:::
