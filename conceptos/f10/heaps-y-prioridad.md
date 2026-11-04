---
id: heaps-y-prioridad
titulo: Montículos y colas de prioridad
fase: 10
nivel: intermedio
rutas: [alg]
prerequisitos: [complejidad-asintotica, arrays-y-listas, arboles-binarios]
tags: [estructuras, heap, prioridad, top-k]
resumen: Un montículo guarda el mínimo o el máximo en la raíz y lo mantiene ahí con dos operaciones de O(log n), sin llegar a ordenar el resto de los elementos.
fuentes: ["Williams (1964), 'Algorithm 232: Heapsort'", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 6"]
---

## En una frase

Un montículo es un árbol binario casi completo guardado en un array donde cada padre es menor
(o mayor) que sus hijos, de forma que el extremo que te interesa siempre está en la primera
posición y sacarlo cuesta O(log n).

## La idea

Imagina la sala de urgencias de un hospital. No atiendes por orden de llegada, sino por
gravedad: en cada momento quieres saber quién es el más grave de todos los que esperan. Podrías
mantener la lista ordenada por gravedad, pero cada vez que llega un paciente tendrías que
insertarlo en su sitio moviendo media lista. Y no necesitas la lista ordenada: **solo
necesitas el primero**.

Un montículo (en inglés, *heap*) hace exactamente eso: renuncia al orden total para poder
mantener el extremo accesible a coste mínimo. La regla es débil y fácil de reparar: cada padre
es menor o igual que sus hijos. No dice nada sobre el orden entre hermanos ni entre primos. Esa
debilidad es justo lo que abarata las operaciones.

Dos detalles hacen que sea tan práctico:

1. **Se guarda en un array, sin punteros.** El árbol es «casi completo» (todas las filas llenas
   salvo la última, que se llena de izquierda a derecha), y esa forma se corresponde exactamente
   con un array: el nodo de la posición `i` tiene sus hijos en `2i+1` y `2i+2`, y su padre en
   `(i−1)/2`. Cero memoria de estructura, todo localidad de caché.
2. **Reparar es bajar o subir por una sola rama.** Cuando insertas, el elemento nuevo sube hasta
   donde le toca comparándose con su padre. Cuando sacas la raíz, pones el último elemento
   arriba y lo hundes comparándose con sus hijos. Cada paso baja un nivel, y la altura es
   ⌊log₂ n⌋.

Con eso, la cola de prioridad resuelve en O(log n) lo que con una lista ordenada costaría O(n).
Y aparece un patrón que se repite muchísimo: **los k mejores**. Si quieres los 10 precios más
altos de un flujo de un millón de valores, no ordenas el millón ni mantienes un montículo con
él: mantienes un montículo de **10** elementos, el más pequeño arriba, y cada valor nuevo que
supera al mínimo de esos 10 entra y el mínimo sale. Al final tienes los 10 mayores, en O(n log
k) y con O(k) de memoria, sin haber guardado el resto.

Ojo con una confusión habitual: un montículo **no es un array ordenado**. Recorrer el array de
un montículo no devuelve nada ordenado, y no se puede hacer [[busqueda-binaria]] sobre él. Solo
el extremo está garantizado. Si necesitas todo ordenado, hay que sacar los elementos uno a uno
(eso es *heapsort*, O(n log n)) o usar [[ordenacion]] directamente.

## Definición formal

Un montículo binario es un array `A` de `n` elementos con dos propiedades:

- **De forma:** el árbol es completo salvo la última fila, que se llena de izquierda a derecha.
  Equivalentemente, las posiciones 0…n−1 están todas ocupadas, sin huecos.
- **De montículo (min-heap):** para todo `i` con hijo, `A[i] ≤ A[hijo]`. En un max-heap la
  desigualdad va al revés. Se elige una y se respeta en todo el código.

Relaciones de índices con la raíz en la posición 0:

- `padre(i) = (i − 1) / 2` con división entera.
- `hijo_izquierdo(i) = 2i + 1`.
- `hijo_derecho(i) = 2i + 2`.
- Último nodo interno: `n/2 − 1` con división entera. De ahí en adelante, todo son hojas.

Operaciones y costes:

| Operación | Qué hace | Coste |
| --- | --- | --- |
| `min()` o `max()` | consulta la raíz sin sacarla | O(1) |
| `insertar(x)` | añade al final y sube (sift-up) | O(log n) |
| `extraer_extremo()` | mueve el último a la raíz y hunde (sift-down) | O(log n) |
| `construir(A)` | convierte un array cualquiera en montículo | O(n) |
| `heapify` desde vacío insertando uno a uno | lo mismo, peor | O(n log n) |
| `cambiar_prioridad(i)` | sube o baja el elemento `i` | O(log n) |
| `heapsort` | extraer el extremo n veces | O(n log n) |

Dos hechos que sorprenden y conviene entender:

1. **Construir un montículo es O(n), no O(n log n).** El truco es hundir a los nodos internos
   de abajo hacia arriba. Los nodos de la última fila no se hunden (coste 0), los de la
   penúltima se hunden 1 nivel, los de la antepenúltima 2… La suma total está acotada por 2n,
   no por n log n. Insertar uno a uno, en cambio, es peor porque cada inserción va por la ruta
   larga desde abajo.
2. **La altura de un montículo con n nodos es ⌊log₂ n⌋.** Como el árbol es completo, no hay
   margen: el número de niveles lo fija `n`. Es la razón de que el montículo no necesite
   balancearse, a diferencia de los [[arboles-balanceados]].

:::figura
fichero: heaps-array-siftdown-y-los-k-mejores
pie: Arriba, el árbol y su array: los hijos de la posición i viven en 2i+1 y 2i+2, así que la estructura no guarda un solo puntero. Abajo a la izquierda, la bajada (sift-down) al extraer el máximo: el último elemento pasa a la raíz y se hunde por el camino largo, tres comparaciones dobles para ocho elementos. Abajo a la derecha, lo que cuesta sacar los k mejores de n: con un montículo de tamaño k es n log k (casi lineal cuando k es pequeño) y ordenando todo antes es n log n, veinte veces más trabajo con k = 1.000.
fuente: figuras/heaps-y-prioridad-1.py
:::

## Ejemplo

Partimos del array `[50, 30, 70, 20, 40, 60, 80]` y lo convertimos en un min-heap hundiendo a
los nodos internos de abajo hacia arriba. El array tiene 7 elementos, así que el último nodo
interno es `7/2 − 1 = 2`:

```
indice:   0    1    2    3    4    5    6
valor:   50   30   70   20   40   60   80

indice 2 (70): hijos en 5 (60) y 6 (80). 60 < 70 -> se cambia.
              [50, 30, 60, 20, 40, 70, 80]
indice 1 (30): hijos en 3 (20) y 4 (40). 20 < 30 -> se cambia.
              [50, 20, 60, 30, 40, 70, 80]
indice 0 (50): hijos en 1 (20) y 2 (60). 20 < 50 -> se cambia.
              [20, 50, 60, 30, 40, 70, 80]
              sigue en el indice 1: hijos 3 (30) y 4 (40). 30 < 50 -> se cambia.
              [20, 30, 60, 50, 40, 70, 80]
```

Resultado: `[20, 30, 60, 50, 40, 70, 80]`. Compruébalo padre a padre:

| Índice | Valor | Hijos | ¿Cumple? |
| --- | --- | --- | --- |
| 0 | 20 | 30 y 60 | sí |
| 1 | 30 | 50 y 40 | sí |
| 2 | 60 | 70 y 80 | sí |

Y fíjate en lo que **no** se cumple: el array no está ordenado. El 50 está antes que el 40, y el
60 antes que el 50. Un montículo no ordena; solo garantiza que la raíz es el mínimo de todo.

Ahora extraemos el mínimo tres veces:

- Sale 20. El último (80) sube a la raíz y se hunde: 80 → cambia con 30 → cambia con 40.
  Queda `[30, 40, 60, 50, 80, 70]`.
- Sale 30. Sube 70, cambia con 40 y se para. Queda `[40, 50, 60, 70, 80]`.
- Sale 40. Queda `[50, 70, 60, 80]`.

Los tres primeros extraídos son 20, 30 y 40: los tres menores, en orden creciente, sin haber
ordenado el array entero en ningún momento.

## Código

```python verificable
import heapq

# heapq mantiene un MIN-heap: el menor siempre en la posicion 0.
datos = [50, 30, 70, 20, 40, 60, 80]
heapq.heapify(datos)                     # O(n): reordena in situ, sin crear otra lista
print("heap tras heapify:", datos)        # -> heap tras heapify: [20, 30, 60, 50, 40, 70, 80]
print("minimo:", datos[0])                # -> minimo: 20
print("no esta ordenado:", datos[1:])     # -> no esta ordenado: [30, 60, 50, 40, 70, 80]

print("los tres menores, extraidos uno a uno:", [heapq.heappop(datos) for _ in range(3)])  # -> los tres menores, extraidos uno a uno: [20, 30, 40]
print("lo que queda:", datos)             # -> lo que queda: [50, 70, 60, 80]
```

:::claves
- `heapq.heapify(datos)` reordena **in situ** y devuelve `None`: si escribes `datos = heapq.heapify(datos)` te quedas sin lista. Es O(n), no O(n log n).
- `heapq` mantiene un **min-heap**: la raíz es el menor. Para una cola de prioridad donde interesa el mayor, se guardan las claves negadas o se envuelven en tuplas `(-prioridad, dato)`.
- `heapq.heappop(datos)` saca la raíz y la devuelve; `datos[0]` la consulta sin sacarla y es O(1). Confundirlos desordena cualquier bucle que solo quería mirar el extremo.
- `heapq.heapreplace(monton, x)` saca la raíz y mete `x` **en una sola operación**; equivale a `heappop` seguido de `heappush`, pero con una sola bajada en vez de dos. En el bucle del top-k, esa diferencia es la mitad del trabajo.
- `heapq.nlargest(k, iterable)` no necesita que el iterable esté en un montículo: por dentro mantiene uno de tamaño k. Para k pequeño es mejor que `sorted(...)[-k:]`, que ordena los n elementos.
- Un montículo **no está ordenado**: `datos[1:]` sale en un orden cualquiera que solo cumple padre ≤ hijos. Para obtener los elementos en orden hay que extraerlos uno a uno, y eso es O(n log n).
:::

```python verificable
import heapq

# Los 3 precios mas altos de un flujo de 1.000.000 de valores, con 3 huecos de memoria.
# El truco: un MIN-heap de tamano k; la raiz es el peor de los que llevas.
def top_k(flujo, k):
    monton = []
    for x in flujo:
        if len(monton) < k:
            heapq.heappush(monton, x)
        elif x > monton[0]:          # solo entra si mejora al peor de los elegidos
            heapq.heapreplace(monton, x)
    return sorted(monton, reverse=True)

import random
rng = random.Random(0)               # semilla fija: el resultado es reproducible
flujo = [rng.randrange(1_000_000) for _ in range(1_000_000)]
print("top 3:", top_k(flujo, 3))     # -> top 3: [999999, 999997, 999996]
```

```python verificable
# Por que construir un monticulo es O(n) y no O(n log n): contar comparaciones.
def sift_down(a, i, n, cont):
    while True:
        izq, der = 2 * i + 1, 2 * i + 2
        menor = i
        if izq < n:
            cont[0] += 1
            if a[izq] < a[menor]:
                menor = izq
        if der < n:
            cont[0] += 1
            if a[der] < a[menor]:
                menor = der
        if menor == i:
            return
        a[i], a[menor] = a[menor], a[i]
        i = menor

def construir_heap(valores):
    cont = [0]
    a = list(valores)
    for i in range(len(a) // 2 - 1, -1, -1):   # de abajo hacia arriba, solo nodos internos
        sift_down(a, i, len(a), cont)
    return cont[0]

def insertar_uno_a_uno(valores):
    h, cont = [], [0]
    for x in valores:
        h.append(x)
        i = len(h) - 1
        while i > 0:                            # sift-up: sube hasta que el padre es menor
            padre = (i - 1) // 2
            cont[0] += 1
            if h[padre] <= h[i]:
                break
            h[padre], h[i] = h[i], h[padre]
            i = padre
    return cont[0]

valores = list(range(1000, 0, -1))              # descendente: el peor caso para sift-up
print("n =", len(valores))                                        # -> n = 1000
print("comparaciones con build-heap:", construir_heap(valores))    # -> comparaciones con build-heap: 1982
print("comparaciones insertando uno a uno:", insertar_uno_a_uno(valores))  # -> comparaciones insertando uno a uno: 7987
```

Con `n = 1000`, construir el montículo de golpe cuesta 1.982 comparaciones (unas 2n) frente a
7.987 (unas 8n) insertando uno a uno. Para `n` grande, la diferencia tiende a un factor log n.

```python ilustrativo
# Max-heap en Python: heapq es un min-heap, asi que se niega la clave.
# Patron util para planificadores: (prioridad_negada, tarea).
import heapq

cola = []
heapq.heappush(cola, (-5, "reentrenar modelo"))
heapq.heappush(cola, (-9, "caida de la API"))
heapq.heappush(cola, (-1, "actualizar documentacion"))
while cola:
    prioridad, tarea = heapq.heappop(cola)
    print(-prioridad, tarea)      # sale 9, luego 5, luego 1
```

## Errores típicos

- **Suponer que el array del montículo está ordenado.** `[20, 30, 60, 50, 40]` es un min-heap
  perfectamente válido y no está ordenado. Hacer `for x in heap:` no da los elementos en orden;
  hay que extraerlos con `heappop` uno a uno.
- **Usar un max-heap para «los k mayores».** Si mantienes los k mayores en un max-heap, la raíz
  es el mayor de los elegidos y no te sirve para decidir si un valor nuevo entra: necesitas
  comparar contra el **peor** de los seleccionados, que es el mínimo. El montículo correcto para
  top-k es el contrario al que la intuición pide.
- **Construir un montículo insertando elemento a elemento cuando ya tienes el array.** Basta
  `heapify`, que es O(n). Insertar 1.000 elementos uno a uno hace unas 4 veces más
  comparaciones.
- **Cambiar la prioridad de un elemento sin rehacer el montículo.** Modificar `fila[3] = nuevo`
  directamente rompe la propiedad y no da error: el montículo queda silenciosamente inválido y
  las extracciones devuelven un orden incorrecto. Hay que subir o hundir ese elemento, o usar
  `heapq.heapreplace` si lo que quieres es sustituir el extremo.
- **Usar el montículo como si fuera una cola de prioridad con borrado arbitrario.** `heapq` no
  ofrece «borra esta tarea concreta»; el patrón habitual es marcar la entrada como cancelada y
  comprobarlo al extraer (borrado perezoso), o usar una estructura indexada.
- **Elegir un montículo cuando necesitas búsquedas por clave.** Para «dame el valor de este
  identificador» el montículo no sirve: recorrerlo es O(n). Eso es trabajo de [[tablas-hash]] o
  de [[arboles-balanceados]].

:::practica
enunciado: Convierte el array [9, 4, 7, 1, 8] en un min-heap hundiendo los nodos internos de abajo hacia arriba y di la altura del montículo resultante.
pista: Con n = 5, el último nodo interno es 5/2 − 1 = 1; los hijos de la posición i están en 2i+1 y 2i+2.
solucion: Índice 1 (valor 4): hijos en 3 (1) y 4 (8); 1 < 4, se cambia y queda [9, 1, 7, 4, 8]. Índice 0 (valor 9): hijos en 1 (1) y 2 (7); 1 < 9, se cambia y queda [1, 9, 7, 4, 8], y sigue en el índice 1: hijos 3 (4) y 4 (8); 4 < 9, se cambia y queda [1, 4, 7, 9, 8]. La altura es ⌊log₂ 5⌋ = 2. Conclusión: el mínimo queda en la raíz y el array no está ordenado.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes el array [20, 30, 60, 50, 40, 70, 80], que es un min-heap válido. ¿Cuál es el resultado de recorrerlo de izquierda a derecha?
o: Los valores en orden creciente, porque es un montículo
o: 20, 30, 60, 50, 40, 70, 80: el montículo solo garantiza que cada padre es menor que sus hijos
o: Los valores en orden decreciente, porque es un min-heap
a: 2
e: La propiedad de montículo solo relaciona cada nodo con sus hijos, no con sus hermanos ni con los nodos de otras ramas. Por eso el 50 puede aparecer después del 60. Para obtener el orden hay que extraer los elementos uno a uno con heappop.
:::

:::quiz
p: Quieres los 5 valores mayores de un flujo de 10 millones de números sin guardarlos todos. ¿Qué montículo usas y por qué?
o: Un max-heap de 5 elementos, porque busco los mayores
o: Un min-heap de 5 elementos, porque su raíz es el peor de los 5 elegidos y basta comparar con ella
o: Un max-heap de 10 millones de elementos, y luego se extraen 5
a: 2
e: Un min-heap de tamaño k deja arriba el menor de los seleccionados. Cada valor nuevo se compara con esa raíz: si es mayor, desplaza al peor y entra. Así el coste es O(n log k) y la memoria O(k). Un max-heap de tamaño k no serviría para decidir; el de 10 millones contradice la premisa de no guardarlo todo.
:::

:::truco
`heapq` solo da min-heaps, así que para un max-heap se niega la clave: se guardan `-x` y se
recupera `-heappop(...)`. Y `heapq.heapreplace(h, x)` es más eficiente que `heappop` seguido de
`heappush` cuando lo que quieres es sustituir el extremo, como en el patrón top-k.
:::
