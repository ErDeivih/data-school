---
id: caminos-minimos
titulo: Caminos mínimos
fase: 10
nivel: avanzado
rutas: [alg]
prerequisitos: [bfs-y-dfs, grafos-representacion, heaps-y-prioridad, programacion-dinamica]
tags: [grafos, rutas, dijkstra, optimizacion]
resumen: Dijkstra, Bellman-Ford, Floyd-Warshall y A* resuelven el mismo problema con supuestos distintos; elegir el que no toca da respuestas seguras y equivocadas.
fuentes: ["Dijkstra (1959), 'A note on two problems in connexion with graphs'", "Bellman (1958), 'On a routing problem'", "Floyd (1962), 'Algorithm 97: Shortest path'", "Hart, Nilsson y Raphael (1968), 'A formal basis for the heuristic determination of minimum cost paths'"]
---

## En una frase

Dado un grafo con pesos y dos vértices, encontrar la ruta de coste total mínimo; el algoritmo
que se usa depende de si los pesos pueden ser negativos, de si necesitas un origen o todos los
pares, y de si tienes una estimación que te permita no explorar el grafo entero.

## La idea

Tienes un mapa con distancias entre ciudades y quieres ir de A a B gastando lo menos posible. La
solución es una versión con precios de la onda del estanque de [[bfs-y-dfs]]: en vez de expandir
por número de saltos, expandes **siempre por el nodo pendiente más barato conocido**. Así, la
primera vez que alcanzas un nodo, lo has alcanzado por la ruta más barata. Eso es Dijkstra.

La idea funciona porque los pesos no son negativos: si todo lo que sumas es mayor o igual que
cero, el camino más barato a un nodo `u` no puede pasar por un nodo cuyo coste ya es mayor que
el de `u`. Esa monotonía es la que permite «cerrar» un nodo y no volver a mirarlo. Y también es
la que se rompe en cuanto aparece **una arista negativa**: puede existir un atajo hacia algo que
ya diste por cerrado, y Dijkstra no lo verá porque no vuelve sobre sus pasos. Por eso ese caso
se resuelve con Bellman-Ford, que relaja **todas** las aristas n−1 veces y no cierra nada hasta
el final.

Cambia también cuántos pares quieres resolver:

- **Un origen, un destino** (o un origen y todos los destinos): Dijkstra y A*.
- **Un origen con pesos negativos**: Bellman-Ford.
- **Todos los pares a la vez**: Floyd-Warshall, que resuelve el problema con una tabla n × n y
  tres bucles anidados. Es el enfoque de [[programacion-dinamica]] aplicado a grafos.

Y por último, A* es la variante de Dijkstra que se usa cuando tienes una pista: si estás en
Madrid y quieres ir a Zaragoza, no exploras Galicia primero, por muy barata que sea la autopista.
A* ordena la cola de prioridad por `coste_real_hasta_aquí + estimación_de_lo_que_falta`, de
forma que se dirige hacia el destino. Si la estimación nunca se pasa (nunca dice que falta menos
de lo que falta), A* devuelve exactamente el mismo camino mínimo que Dijkstra explorando muchos
menos nodos. Si se pasa, devuelve un camino más corto de lo posible: un error silencioso.

## Definición formal

Sea `G = (V, E)` un grafo dirigido o no dirigido con `n = |V|` vértices y una función de peso
`w(u, v)` definida para cada arista. El **coste** de un camino es la suma de los pesos de sus
aristas.

- `dist(s, v)` — el coste mínimo de `s` a `v`. Es `∞` si no hay camino.
- **Relajación** de la arista `(u, v)` — si `dist[u] + w(u, v) < dist[v]`, se actualiza
  `dist[v] = dist[u] + w(u, v)` y se guarda `previo[v] = u`. Relajar es la operación básica de
  los cuatro algoritmos; cambian el orden y cuántas veces la hacen.
- `π(v)` — en A*, la estimación del coste que falta de `v` al destino. Es una **heurística**.
- **Heurística admisible** — `π(v) ≤ dist(v, destino)` para todo `v`: nunca sobreestima. Es la
  condición que hace que A* siga siendo exacto.
- **Heurística consistente** — `π(u) ≤ w(u, v) + π(v)`: además cumple la desigualdad triangular.
  Es más fuerte que la admisibilidad y garantiza que A* cierra cada nodo una sola vez.

Algoritmos, supuestos y costes (con `m = |E|`):

| Algoritmo | Pesos | Resuelve | Coste |
| --- | --- | --- | --- |
| Dijkstra con montículo | no negativos | un origen, todos los destinos | O((n + m) log n) |
| Dijkstra con matriz y búsqueda lineal | no negativos | un origen, todos los destinos | O(n²) |
| Bellman-Ford | cualesquiera, detecta ciclos negativos | un origen, todos los destinos | O(n · m) |
| Floyd-Warshall | cualesquiera, detecta ciclos negativos | todos los pares | O(n³) |
| A* | no negativos, con heurística | un origen, un destino | O((n + m) log n) en el peor caso, mucho menos en la práctica |

Detalles que importan:

1. **Dijkstra con montículo** extrae el nodo de menor `dist` pendiente. La cola de prioridad es
   la de [[heaps-y-prioridad]], y la variante perezosa (reinsertar cuando mejora la distancia y
   descartar las entradas viejas) es la que se escribe en la práctica.
2. **Bellman-Ford** hace n−1 pasadas sobre todas las aristas. Al terminar, una pasada extra en la
   que todavía se pueda relajar demuestra que existe un **ciclo de peso negativo alcanzable**, y
   entonces el problema no tiene solución: se puede dar vueltas al ciclo indefinidamente bajando
   el coste.
3. **Floyd-Warshall** mantiene `D[i][j]` y prueba a mejorar cada par permitiendo que los nodos
   intermedios sean 0, 1, 2… hasta n−1. Es el mismo patrón de subproblemas solapados que usan
   otros problemas de [[programacion-dinamica]].
4. **A*** con `π(v) = 0` para todo `v` es exactamente Dijkstra. La heurística es una
   generalización, no un algoritmo distinto.
5. El **camino** se recupera con el array `previo`: se va de `previo[v]` hacia atrás hasta el
   origen y se invierte la lista. Sin ese array solo se obtiene el coste.

## Ejemplo

Grafo **no dirigido y ponderado** con 5 vértices: `V = {0, 1, 2, 3, 4}` y aristas

```
0-1 (4)   0-2 (1)   2-1 (2)   1-3 (5)
2-3 (8)   3-4 (3)   2-4 (10)
```

Dijkstra desde el vértice 0, extrayendo siempre el nodo pendiente de menor distancia:

| Paso | Nodo extraído | dist al extraer | Relajaciones | Distancias tras el paso |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 → 4; 2 → 1 | [0, 4, 1, ∞, ∞] |
| 2 | 2 | 1 | 1 → 1 + 2 = 3 mejora 4; 3 → 9; 4 → 11 | [0, 3, 1, 9, 11] |
| 3 | 1 | 3 | 3 → 3 + 5 = 8 mejora 9; ya tiene 0 y 2 | [0, 3, 1, 8, 11] |
| 4 | 3 | 8 | 4 → 8 + 3 = 11, empata con 11 | [0, 3, 1, 8, 11] |
| 5 | 4 | 11 | nada nuevo | [0, 3, 1, 8, 11] |

Resultado: `dist = [0, 3, 1, 8, 11]`. Distancias mínimas desde el 0.

El detalle interesante está en el vértice 1. En el paso 1 su distancia es 4, y en el paso 2 baja
a 3 al descubrir la ruta 0 → 2 → 1. Si el algoritmo hubiera «cerrado» el 1 con su primer valor,
la respuesta final habría sido 4 y el camino 0 → 1; con la relajación correcta, el camino es
0 → 2 → 1. **Ese es el mecanismo que Dijkstra explota y el que se rompe con pesos negativos.**

Ahora el caso con pesos negativos. El grafo `(0,1,3), (0,2,1), (2,3,2), (3,1,−4), (1,4,5),
(3,4,7)` no tiene ciclos negativos (el único ciclo es 1 → 4 → 3 → 1, con peso 5 + 7 − 4 = 8,
positivo) y sus distancias mínimas desde el 0 son `[0, −1, 1, 3, 4]`. Fíjate en el vértice 1: el
camino barato no es la arista directa de peso 3, sino 0 → 2 → 3 → 1, que cuesta 1 + 2 − 4 = −1.
Con pesos negativos, el orden de llegada deja de ser una guía: una arista negativa puede
convertir un camino que parecía largo en el más barato, y ya no se puede dar por bueno un
vértice solo porque hayas llegado antes a él.

La trampa concreta de Dijkstra es esta: cierra cada vértice con la primera distancia con la que
sale de la cola, y ese cierre se apoya en que todas las aristas suman. Con una arista negativa,
puede existir un atajo hacia un vértice ya cerrado; el algoritmo o lo ignora o llega tarde a él,
y la respuesta final queda por encima de la real. Es un fallo silencioso, sin excepción y sin
aviso: devuelve números plausibles. Bellman-Ford no cierra nada hasta el final y por eso no
tiene ese punto débil.

Floyd-Warshall sobre el grafo dirigido de 4 vértices con aristas `(0,1,3), (1,2,1), (0,2,7),
(2,3,2)` da esta tabla de distancias mínimas entre todos los pares:

```
       a 0    a 1    a 2    a 3
desde 0   0      3      4      6
desde 1   inf    0      1      3
desde 2   inf    inf    0      2
desde 3   inf    inf    inf    0
```

El 4 de la fila 0 es la clave: aunque existe la arista directa 0 → 2 de peso 7, la ruta
0 → 1 → 2 cuesta 3 + 1 = 4. Floyd-Warshall encuentra ese atajo sin que nadie se lo indique,
porque en la pasada con `k = 1` prueba a meter el vértice 1 como intermedio en todos los pares.

:::figura
fichero: caminos-minimos-dijkstra-y-negativos
pie: A la izquierda, el grafo no dirigido del ejemplo con las distancias que da Dijkstra desde el 0: [0, 3, 1, 8, 11]. Las aristas azules son el árbol de caminos mínimos. Fíjate en el vértice 1: se cierra en 3 y no en 4, porque el atajo 0 → 2 → 1 es más barato que la arista directa. Y fíjate en el 4: empata, con dos rutas de coste 11 (0 → 2 → 4 y 0 → 2 → 1 → 3 → 4) y el algoritmo se queda con la primera. A la derecha, el mismo algoritmo sobre un grafo dirigido con una arista de peso −4: el 1 sale de la cola con 3 y queda cerrado, así que ya no se vuelve a mirar y Dijkstra devuelve 3 donde el coste real es −1; el error se propaga al 4, que sale 8 en vez de 4. Los valores en verde son los de Bellman-Ford, que no cierra nada hasta el final. Lo peligroso es que no hay excepción ni aviso: son números plausibles. El panel dibuja la versión de libro, la que cierra cada vértice al sacarlo de la cola; la variante perezosa que reinserta la distancia cuando mejora se comporta como un algoritmo de corrección de etiquetas y en este ejemplo acabaría acertando, pero deja de ser Dijkstra y pierde su coste.
fuente: figuras/caminos-minimos-1.py
:::

## Código

```python verificable
import heapq

aristas = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3), (2, 4, 10)]
n = 5

# El grafo es no dirigido: cada arista se guarda en los dos sentidos.
adyacencia = {i: [] for i in range(n)}
for u, v, w in aristas:
    adyacencia[u].append((v, w))
    adyacencia[v].append((u, w))

def dijkstra(adyacencia, origen, n):
    """Distancias minimas desde el origen. Exige pesos no negativos."""
    dist = [float("inf")] * n
    previo = [None] * n
    dist[origen] = 0
    cola = [(0, origen)]                 # (distancia, vertice): el monticulo ordena por distancia
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue                     # entrada vieja: ya se mejoro por otra ruta
        for v, w in adyacencia[u]:
            if d + w < dist[v]:          # relajacion de la arista (u, v)
                dist[v] = d + w
                previo[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, previo

def camino(previo, origen, destino):
    ruta, actual = [], destino
    while actual is not None:
        ruta.append(actual)
        actual = previo[actual]
    ruta.reverse()
    return ruta if ruta and ruta[0] == origen else None

dist, previo = dijkstra(adyacencia, 0, n)
print("distancias desde 0:", dist)          # -> distancias desde 0: [0, 3, 1, 8, 11]
print("camino al 4:", camino(previo, 0, 4)) # -> camino al 4: [0, 2, 4]
print("camino al 3:", camino(previo, 0, 3)) # -> camino al 3: [0, 2, 1, 3]
```

:::claves
- La cola de prioridad guarda tuplas `(distancia, vértice)`: el montículo compara primero por distancia y solo usa el vértice para desempatar. Si se invirtiera el orden, `heapq` ordenaría por número de vértice y el algoritmo dejaría de ser Dijkstra.
- `if d > dist[u]: continue` descarta las entradas viejas del montículo. Sin esa línea el resultado sigue siendo correcto, pero se reprocesan vértices ya mejorados: el montículo se llena de copias y el trabajo crece.
- `dist = [float("inf")] * n` es correcto porque los `float` son inmutables; la trampa de `[[0] * n] * n` no aparece aquí. La misma línea con objetos mutables compartiría el mismo objeto en las n posiciones.
- `previo` no interviene en el cálculo de las distancias: solo sirve para reconstruir el camino. Sin ese array se obtiene el coste y no la ruta, y la función `camino` devuelve `None` cuando el destino no se alcanzó.
- El grafo no dirigido necesita las dos líneas, `adyacencia[u].append((v, w))` y `adyacencia[v].append((u, w))`. Si se olvida la segunda, Dijkstra devuelve `inf` para medio grafo sin lanzar ningún error.
- Cambiar `if d + w < dist[v]` por `<=` no altera las distancias finales y sí puede empeorar el tiempo: encola actualizaciones que no mejoran nada y el montículo crece de más.
:::

```python verificable
def bellman_ford(n, aristas, origen):
    """Admite pesos negativos. Devuelve None si hay un ciclo de peso negativo alcanzable."""
    dist = [float("inf")] * n
    dist[origen] = 0
    for _ in range(n - 1):               # n-1 pasadas bastan para cualquier camino simple
        for u, v, w in aristas:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in aristas:              # una pasada mas: si algo mejora, hay ciclo negativo
        if dist[u] + w < dist[v]:
            return None
    return dist

# Camino barato que pasa por dos aristas negativas seguidas
sin_ciclo = [(0, 1, 3), (0, 2, 1), (2, 3, 2), (3, 1, -4), (1, 4, 5), (3, 4, 7)]
print("pesos negativos:", bellman_ford(5, sin_ciclo, 0))   # -> pesos negativos: [0, -1, 1, 3, 4]

# Un ciclo cuyo peso total es negativo: no existe el camino minimo
ciclo_negativo = [(0, 1, 1), (1, 2, -3), (2, 1, 1)]
print("ciclo negativo:", bellman_ford(3, ciclo_negativo, 0))  # -> ciclo negativo: None
```

```python verificable
def floyd_warshall(n, aristas):
    """Todos los pares: programacion dinamica sobre los vertices intermedios."""
    INF = float("inf")
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0                      # la distancia de un vertice a si mismo es 0
    for u, v, w in aristas:
        D[u][v] = min(D[u][v], w)        # min() porque puede haber aristas repetidas
    for k in range(n):                   # k: el vertice que se permite como intermedio
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    return D

D = floyd_warshall(4, [(0, 1, 3), (1, 2, 1), (0, 2, 7), (2, 3, 2)])
print("de 0 a 2:", D[0][2])       # -> de 0 a 2: 4
print("de 0 a 3:", D[0][3])       # -> de 0 a 3: 6
print("de 1 a 3:", D[1][3])       # -> de 1 a 3: 3
print("de 3 a 0:", D[3][0])       # -> de 3 a 0: inf
```

Fíjate en la última línea: `D[3][0]` es `inf` porque el grafo del ejemplo es **dirigido** y no
hay ninguna arista que salga del vértice 3. La matriz de Floyd-Warshall no es simétrica salvo
que el grafo lo sea.

```python ilustrativo
# A* con heuristica: ordena la cola por coste_real + estimacion_restante.
# Con una heuristica admisible (que nunca sobreestima) devuelve el mismo camino que Dijkstra.
import heapq

def a_estrella(adyacencia, origen, destino, heuristica):
    cola = [(heuristica[origen], 0, origen)]   # (f = g + h, g = coste real, vertice)
    mejor = {origen: 0}
    while cola:
        f, g, u = heapq.heappop(cola)
        if u == destino:
            return g
        for v, w in adyacencia[u]:
            nuevo = g + w
            if nuevo < mejor.get(v, float("inf")):
                mejor[v] = nuevo
                heapq.heappush(cola, (nuevo + heuristica[v], nuevo, v))
    return float("inf")
```

## Errores típicos

- **Usar Dijkstra con pesos negativos.** El algoritmo cierra cada nodo con su primera distancia
  y no vuelve. Si más adelante aparece un atajo con peso negativo que llega a ese nodo, la
  respuesta final es mayor que la real y el camino devuelto no es el barato. El fallo no avisa:
  devuelve números plausibles. Con pesos negativos, Bellman-Ford o Floyd-Warshall.
- **Confundir «hay pesos negativos» con «hay ciclo negativo».** Lo primero es un problema
  resoluble; lo segundo, no. Bellman-Ford distingue los dos casos con la pasada extra, y esa
  comprobación no es opcional: sin ella devuelve distancias que no existen.
- **Usar BFS para caminos mínimos con pesos.** BFS cuenta aristas, no suma pesos. Solo es
  correcto si todas las aristas valen lo mismo, y en ese caso es la opción más barata.
- **Implementar Floyd-Warshall con el bucle `k` en el sitio equivocado.** El vértice intermedio
  `k` tiene que ser el bucle **exterior**. Si se pone dentro, el algoritmo calcula otra cosa y
  da distancias demasiado grandes sin ningún error visible.
- **Dar una heurística inadmisible a A*.** Si la estimación sobreestima el coste que falta, A*
  puede devolver un camino que no es el mínimo. La condición no es «que se parezca», es «que
  nunca se pase»: la distancia en línea recta es admisible, una estimación optimista de tráfico
  no lo es.
- **Olvidar que Bellman-Ford relaja `m` aristas en cada pasada.** Con grafos grandes, O(n · m)
  puede ser millones de operaciones frente a las O(m log n) de Dijkstra. Antes de elegirlo,
  comprueba que de verdad hay pesos negativos: muchas veces el «peso negativo» es un error de
  signo en los datos.

:::practica
enunciado: Grafo dirigido con aristas 0→1 (2), 0→2 (5), 1→2 (1), 1→3 (4) y 2→3 (1). Ejecuta Dijkstra desde el vértice 0 y da las distancias finales y el camino mínimo hasta el 3.
pista: Extrae siempre el vértice pendiente de menor distancia y relaja sus aristas de salida; el vértice queda cerrado cuando sale de la cola.
solucion: Se extrae 0 y se relajan 1 (2) y 2 (5). Se extrae 1 con d = 2: 1→2 da 2 + 1 = 3, que mejora el 5, y 1→3 da 6. Se extrae 2 con d = 3: 2→3 da 3 + 1 = 4, que mejora el 6. Se extrae 3 con d = 4. Distancias: [0, 2, 3, 4] y camino 0 → 1 → 2 → 3. Conclusión: el atajo 1→2 rebajó el coste del 2 y, con él, el del 3.
:::

## Comprueba que lo sabes

:::quiz
p: En el grafo no dirigido con aristas 0-1 (4), 0-2 (1), 2-1 (2), 1-3 (5), 2-3 (8), 3-4 (3), ¿cuál es la distancia mínima de 0 a 3 y por qué camino?
o: 9, por el camino 0 → 2 → 3
o: 8, por el camino 0 → 2 → 1 → 3
o: 5, por el camino 0 → 1 → 3
a: 2
e: El camino directo 0 → 1 → 3 cuesta 4 + 5 = 9, y 0 → 2 → 3 cuesta 1 + 8 = 9. La ruta 0 → 2 → 1 → 3 cuesta 1 + 2 + 5 = 8, que es la menor. Dijkstra la encuentra porque relaja el vértice 1 (de 4 a 3) antes de cerrarlo.
:::

:::quiz
p: Un grafo tiene una arista de peso −4 pero ningún ciclo de peso negativo. ¿Qué algoritmo usas para las distancias desde un origen?
o: Dijkstra, porque el problema tiene solución
o: Bellman-Ford, porque admite pesos negativos y además comprueba que no haya ciclos negativos
o: BFS, porque cuenta saltos
a: 2
e: Que el problema tenga solución no salva a Dijkstra: su razonamiento se apoya en que los pesos no son negativos, y con una arista negativa puede cerrar un nodo con una distancia que luego deja de ser la mínima. Bellman-Ford no cierra nada, admite el signo y detecta el ciclo negativo si existiera.
:::

:::quiz
p: ¿Cuándo conviene Floyd-Warshall frente a ejecutar Dijkstra desde cada vértice?
o: Cuando el grafo es disperso y solo necesitas un origen
o: Cuando el grafo es denso y necesitas las distancias entre todos los pares, o cuando hay pesos negativos sin ciclos negativos
o: Siempre, porque es O(n³) y las potencias son rápidas
a: 2
e: Con n orígenes, Dijkstra cuesta O(n · (n + m) log n), que para grafos densos (m del orden de n²) es peor que el O(n³) de Floyd-Warshall, y este además admite pesos negativos y cabe en tres bucles. En un grafo disperso con un solo origen, Floyd-Warshall es un desperdicio de memoria y tiempo.
:::
