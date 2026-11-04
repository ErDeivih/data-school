---
id: pilas-y-colas
titulo: Pilas, colas y deques
fase: 10
nivel: básico
rutas: [alg, de]
prerequisitos: [arrays-y-listas, complejidad-asintotica]
tags: [estructuras, lifo, fifo, recorridos]
resumen: Dos formas de guardar y sacar: la pila devuelve lo último que entró y la cola lo primero; con ellas se resuelven paréntesis, recorridos por niveles y planificadores.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 10", "Knuth (1997), 'The Art of Computer Programming, vol. 1'"]
---

## En una frase

Una **pila** solo deja sacar el último elemento que entró (LIFO, *last in, first out*) y una
**cola** solo deja sacar el primero que entró (FIFO, *first in, first out*); esa única diferencia
decide si un recorrido va en profundidad o por niveles.

## La idea

Una pila es la bandeja de platos de un bar: el último plato que se pone encima es el primero que
se coge. Nadie intenta sacar el de abajo. Eso es una limitación y a la vez su superpoder: cuando
solo te interesa lo más reciente, la pila es la estructura perfecta. Un paréntesis de apertura
espera a su cierre; si aparece otro paréntesis antes, el nuevo es el que hay que cerrar primero.
Un «deshacer» tiene que revertir el último cambio, no el primero. Y cuando una función llama a
otra, la que está a medias se queda esperando encima de la pila mientras la nueva trabaja: eso es
la **pila de llamadas**, la misma idea metida en el lenguaje.

Una cola es la fila del supermercado: el primero que llegó es el primero que paga. Sirve para todo
lo que exige orden de llegada. Un planificador de tareas reparte el procesador por turnos; un
servidor de mensajes entrega en el orden en que se recibieron (si quieres eso, una cola; si
quieres prioridad, cambia de estructura y mira [[heaps-y-prioridad]]); un recorrido de un grafo
**por niveles** necesita visitar antes todos los vecinos de la distancia 1 que cualquiera de
distancia 2, y eso es exactamente una cola.

El detalle práctico está en cómo se implementan. Una pila encaja sin esfuerzo en una lista de
Python: `append` y `pop` trabajan en el mismo extremo, y ese extremo es O(1). Una cola **no**
encaja: si usas una lista y sacas por delante con `pop(0)`, cada extracción desplaza todos los
elementos que quedan, así que vaciar una cola de 10.000 elementos cuesta casi 50 millones de
desplazamientos. La estructura correcta es `collections.deque` (*double-ended queue*), que
permite añadir y quitar por los dos extremos en O(1) porque no guarda los elementos pegados en
memoria, sino enlazados en bloques.

Un **deque** es, de hecho, la estructura más versátil de las tres: sirve como pila
(`append` + `pop`), como cola (`append` + `popleft`) y como cola de doble entrada, que es lo que
necesita una ventana deslizante cuando hay que descartar por el principio y por el final. Su
punto débil es el acceso por índice en el medio: para llegar al elemento 500.000 de un deque hay
que recorrer, así que es O(n), mientras que en una lista es O(1).

## Definición formal

**Pila (stack).** Estructura con tres operaciones, todas sobre el mismo extremo, llamado cima:

- `push(x)` — apila `x` en la cima.
- `pop()` — devuelve y elimina el elemento de la cima.
- `peek()` o `top()` — devuelve la cima sin eliminarla.

**Cola (queue).** Estructura con dos extremos:

- `enqueue(x)` — añade `x` por el final.
- `dequeue()` — devuelve y elimina el elemento del principio.
- `front()` — consulta el principio sin eliminarlo.

**Deque.** Generaliza las dos: `append`, `appendleft`, `pop`, `popleft`, todas O(1).

Costes con las implementaciones de Python:

| Operación | Lista | Deque |
| --- | --- | --- |
| Añadir por el final | O(1) amortizado | O(1) |
| Quitar por el final | O(1) | O(1) |
| Añadir por el principio | O(n) | O(1) |
| Quitar por el principio | O(n) | O(1) |
| Acceder por índice | O(1) | O(n) |
| Buscar un valor | O(n) | O(n) |

Dos propiedades que se deducen de la definición y que casi nadie enuncia:

1. **Una pila no permite consultar el elemento del medio.** No es un descuido del diseño: si lo
   permitieras, la estructura dejaría de garantizar que solo lo reciente importa y los algoritmos
   que se apoyan en ella (paréntesis, evaluación de expresiones, retroceso) perderían su
   invariante. Si necesitas acceso arbitrario, quieres un array.
2. **El orden de salida determina el recorrido.** Con una pila, un recorrido de grafo explora en
   profundidad; con una cola, por niveles. Es la única línea que cambia entre DFS y BFS, y está
   desarrollado en [[bfs-y-dfs]].

:::figura
fichero: pilas-y-colas-vaciar-y-recorrido
pie: A la izquierda, lo que cuesta vaciar una cola entera: con una lista y pop(0) los desplazamientos suman n²/2 (49.995.000 con 10.000 elementos) y con un deque son n. A la derecha, el mismo grafo recorrido con una cola y con una pila: la cola visita por niveles (A, B, C, D, E, F) y la pila baja hasta el fondo antes de mirar al siguiente hermano (A, B, D, F, E, C). El color de cada nodo marca su nivel, y se ve que la pila se salta el orden.
fuente: figuras/pilas-y-colas-1.py
:::

## Ejemplo

Comprobar si los paréntesis de `{[()]}` están bien equilibrados, con una pila:

1. `{` → apilar. Pila: `{`.
2. `[` → apilar. Pila: `{ [`.
3. `(` → apilar. Pila: `{ [ (`.
4. `)` → es un cierre: desapilar y comprobar que la cima es `(`. Coincide. Pila: `{ [`.
5. `]` → desapilar: la cima es `[`. Coincide. Pila: `{`.
6. `}` → desapilar: la cima es `{`. Coincide. Pila vacía.
7. Al final la pila está vacía → equilibrado.

Con `([)]`, el paso 4 desapila `(` y el cierre `]` pide un `[`: no coincide → falso. Con `(((`,
la pila no se vacía al final → falso.

Y un recorrido por niveles sobre este grafo: `A` tiene como vecinos `B` y `C`; `B` y `C` llevan a
`D`; `C` y `D` llevan a `E`; `D` y `E` llevan a `F`. Con una cola, el orden de visita es
`A, B, C, D, E, F` y los niveles son `[A]`, `[B, C]`, `[D, E]`, `[F]`. Con una pila saldría
`A, C, E, F, D, B`, que es un recorrido en profundidad: mismos nodos, orden completamente
distinto.

El coste de sacar elementos por delante, con números: vaciar una cola de 10.000 elementos con
`pop(0)` sobre una lista desplaza 9.999 + 9.998 + … + 0 = 49.995.000 elementos. Con
`popleft()` sobre un deque, 10.000 movimientos de puntero. Mismo resultado, factor 5.000 de
diferencia.

## Código

```python verificable
# Una pila resuelve el equilibrio de parentesis en una sola pasada.
def equilibrado(texto):
    parejas = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in texto:
        if c in "([{":
            pila.append(c)                       # apilar la apertura
        elif c in parejas:
            if not pila or pila.pop() != parejas[c]:
                return False                     # cierre sin apertura o mal emparejado
    return not pila                              # si queda algo, hay aperturas sin cerrar

print(equilibrado("{[()]}"))   # -> True
print(equilibrado("([)]"))     # -> False
print(equilibrado("((("))      # -> False
print(equilibrado(""))         # -> True
```

:::claves
- `pila.pop()` sin argumentos saca **el último** y es O(1); `pila.pop(0)` saca el primero y es O(n) porque desplaza todo. La misma lista sirve de pila o de cola lenta, y la diferencia entre las dos líneas es de un orden de complejidad.
- `deque.popleft()` no toca los demás elementos: mueve un puntero. Pero un deque **no admite rebanadas**: `d[:3]` lanza `TypeError` (pide un entero, no un `slice`). Si necesitas cortar por índice, ya no es la estructura adecuada.
- `not pila` es la condición correcta para «vacía»: una lista vacía es falsa en Python. Al terminar el recorrido de paréntesis, si quedan aperturas sin cerrar la pila no está vacía, y `not pila` lo detecta sin contar nada.
- En `bfs`, `visitados.add(vecino)` va **dentro del `if` y antes de `cola.append`**: marcar al encolar garantiza que cada nodo entra en la cola una sola vez y que su `dist` se fija con la primera capa que lo alcanza. Si en cambio marcas al desencolar, el mismo nodo entra varias veces en la cola (una por cada vecino que lo alcanza antes de procesarlo), el trabajo se multiplica en grafos con ciclos y la distancia se puede corregir hacia abajo más tarde.
- `len(cola)` se evalúa una vez al entrar en el `for` porque `range(len(cola))` se construye antes de iterar; por eso el bucle interior consume exactamente un nivel y la lista `nivel` sale completa.
- `collections.deque` acepta `maxlen`: al llenarse, descarta por el otro extremo solo. Es lo que se usa para «los últimos 100 eventos» sin ir borrando a mano.
:::

```python verificable
from collections import deque

# BFS: la cola garantiza que se visita por niveles y no en profundidad.
grafo = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}

def bfs(grafo, inicio):
    visitados = {inicio}
    cola = deque([inicio])
    orden, niveles = [], []
    while cola:
        nivel = []
        for _ in range(len(cola)):               # lo que hay en la cola es un nivel completo
            nodo = cola.popleft()
            orden.append(nodo)
            nivel.append(nodo)
            for vecino in grafo[nodo]:
                if vecino not in visitados:      # se marca al encolar, no al desencolar
                    visitados.add(vecino)
                    cola.append(vecino)
        niveles.append(nivel)
    return orden, niveles

print("orden:", bfs(grafo, "A")[0])     # -> orden: ['A', 'B', 'C', 'D', 'E', 'F']
print("niveles:", bfs(grafo, "A")[1])   # -> niveles: [['A'], ['B', 'C'], ['D', 'E'], ['F']]
print("nodos visitados:", len(bfs(grafo, "A")[0]))   # -> nodos visitados: 6
```

```python verificable
from collections import deque

# Sacar por delante: contamos desplazamientos en vez de cronometrar.
def desplazamientos_con_lista(cola):
    total = 0
    while cola:
        cola.pop(0)              # saca el primero y mueve todos los demas
        total += len(cola)       # lo que se ha desplazado en esa operacion
    return total

def desplazamientos_con_deque(cola):
    total = 0
    while cola:
        cola.popleft()           # no desplaza nada: actualiza un puntero
        total += 1
    return total

print("lista, 10000 elementos:", desplazamientos_con_lista(list(range(10000))))   # -> lista, 10000 elementos: 49995000
print("deque, 10000 elementos:", desplazamientos_con_deque(deque(range(10000))))  # -> deque, 10000 elementos: 10000
```

## Errores típicos

- **Usar una lista como cola.** `pop(0)` y `insert(0, x)` son O(n) cada vez: vaciar la cola sale
  a O(n²). Con 10.000 elementos son 49.995.000 desplazamientos en lugar de 10.000. Usa
  `collections.deque` o `queue.Queue` si hay hilos de por medio.
- **Confundir LIFO con FIFO al escribir un recorrido.** Cambiar la cola por una pila en un BFS
  no da un error de compilación ni un resultado vacío: da un DFS silencioso. Si tu «BFS» visita
  los nodos en un orden raro, mira la estructura que estás usando.
- **Marcar los nodos como visitados al desencolar en vez de al encolar.** En un grafo con
  ciclos, el mismo nodo entra varias veces en la cola antes de ser procesado y el trabajo se
  multiplica (en un grafo denso, de forma explosiva). La marca va en el momento de encolar.
- **Acceder al elemento del medio.** Ni la pila ni la cola lo ofrecen como operación, y en un
  deque real cuesta O(n). Si necesitas mirar en medio, la estructura no es la adecuada: quieres
  un array o una lista.
- **Usar la recursión como pila sin límite.** Cada llamada ocupa un marco en la pila del
  programa; Python corta a los 1.000 niveles por defecto con `RecursionError`. Para recursiones
  profundas, escribe el algoritmo con una pila explícita, como se cuenta en
  [[recursion-y-backtracking]].
- **Elegir pila cuando el trabajo debe repartirse por turnos.** Con una pila, el último que
  llega se procesa primero, así que una tarea que no para de generar trabajo nuevo puede dejar
  a las demás sin turno (inanición). Los planificadores justos usan colas, y los que atienden
  prioridades, montículos.

:::practica
enunciado: Traza con una pila el equilibrio de la expresión `[{()]}` e indica en qué posición falla. Después, si la expresión fuera `([{`, di cuántos elementos quedan en la pila al terminar y por qué el resultado es falso.
pista: Cada cierre desapila y debe coincidir con la cima; al final la pila tiene que quedar vacía.
solucion: Se apilan `[`, `{` y `(`: pila `[ { (`. El `)` desapila `(` y coincide; queda `[ {`. El `]` desapila `{`, pero `]` empareja con `[`: no coincide, así que falla en la quinta posición. Con `([{` no llega ningún cierre: al terminar quedan 3 elementos y una pila no vacía significa aperturas sin cerrar, o sea falso. Conclusión: una pila y una sola pasada deciden la expresión.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué estructura usarías para comprobar que los paréntesis de una expresión están bien equilibrados, y por qué?
o: Una cola, porque hay que respetar el orden en que aparecen los símbolos
o: Una pila, porque cada cierre debe emparejarse con la apertura más reciente que sigue abierta
o: Un diccionario, porque hay tres tipos de paréntesis distintos
a: 2
e: El cierre corresponde siempre a la apertura más reciente, que es justo lo que devuelve una pila (LIFO). Una cola devolvería la primera apertura y fallaría con `([)]`. El diccionario sirve para saber qué cierre empareja con qué apertura, pero no para llevar el orden: eso lo hace la pila.
:::

:::quiz
p: Vaciar una cola de 10.000 elementos con `pop(0)` sobre una lista, ¿cuántos desplazamientos provoca?
o: 10.000, uno por cada extracción
o: Unos 50 millones, porque cada extracción mueve los que quedan
o: Ninguno, porque `pop(0)` solo actualiza un puntero
a: 2
e: Sacar el primero obliga a mover todos los siguientes: 9.999 + 9.998 + ... + 0 = 49.995.000. Con un deque son 10.000 actualizaciones de puntero. La opción de «solo un puntero» describe `popleft()` sobre un deque, no `pop(0)` sobre una lista.
:::

:::quiz
p: En un BFS, ¿dónde hay que marcar un nodo como visitado?
o: Al encolarlo, antes de que le llegue el turno
o: Al desencolarlo, justo antes de procesarlo
o: No hace falta marcarlo si el grafo no tiene ciclos
a: 1
e: Si marcas al desencolar, el mismo nodo puede entrar varias veces en la cola (una por cada vecino que lo alcanza antes de procesarlo) y el trabajo se multiplica. Marcándolo al encolar, cada nodo entra una sola vez. La marca también es necesaria sin ciclos, para no repetir nodos por caminos distintos.
:::

:::truco
Si dudas entre pila y cola, mira el orden en que quieres **sacar**: lo más reciente (pila), lo
más antiguo (cola) o ambos extremos (deque). Y si el trabajo tiene prioridades, ninguna de las
tres: eso es una cola de prioridad, que se implementa con un montículo.
:::
