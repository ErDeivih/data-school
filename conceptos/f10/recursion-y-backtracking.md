---
id: recursion-y-backtracking
titulo: Recursión y backtracking
fase: 10
nivel: intermedio
rutas: [alg, core]
prerequisitos: [complejidad-asintotica, pilas-y-colas]
tags: [algoritmos, recursion, backtracking, busqueda]
resumen: Una función que se llama a sí misma con un problema más pequeño, y la técnica de deshacer pasos para explorar todas las posibilidades sin repetir trabajo.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 4", "Sedgewick y Wayne (2011), 'Algorithms', 4.ª ed., cap. 2"]
---

## En una frase

La recursión resuelve un problema resolviendo copias más pequeñas de sí mismo hasta llegar a un
caso que se sabe contestar directamente, y el backtracking usa esa misma recursión para explorar
decisiones —qué colocar aquí, por dónde ir— deshaciendo cada intento fallido para probar el
siguiente.

## La idea

Tienes tres cajas chinas y quieres saber qué hay dentro de la última. La respuesta no es
«abre las tres a la vez»: es «abre la primera, y lo que hay dentro es el mismo problema con una
caja menos». Cuando llegas a una caja que no contiene otra, tienes la respuesta y vas cerrando.
Eso es recursión: **resolver el problema de tamaño `n` suponiendo resuelto el de tamaño `n − 1`**,
con un caso base que corta la cadena.

La recursión es cómoda porque el problema de la Torre de Hanói, el recorrido de un árbol o el
producto de matrices se describen en dos líneas en vez de en un bucle con índices. Pero no es
gratis, y el precio tiene dos partes:

1. **Cada llamada ocupa un marco en la pila.** Guardar argumentos, variables locales y la
   dirección de vuelta no es gratis, y la profundidad máxima está limitada (en CPython, por
   defecto, 1.000 marcos; al pasarse salta `RecursionError`). Una recursión que baja un elemento
   por llamada sobre 100.000 elementos no cabe, por muy correcta que sea.
2. **La recursión ingenua repite trabajo.** El ejemplo canónico es Fibonacci:
   `fib(n) = fib(n−1) + fib(n−2)` llama a `fib(n−2)` dos veces, a `fib(n−3)` tres veces y así
   hasta que el número de llamadas crece como la sucesión de Fibonacci: `fib(35)` hace unos 30
   millones de llamadas para calcular un número de nueve cifras. La solución se llama
   [[programacion-dinamica|memoización]]: guardar el resultado de cada subproblema la primera vez
   y devolverlo después.

**Backtracking** es recursión con marcha atrás. La idea es construir la solución por partes: se
elige una opción, se comprueba si esa elección puede llegar a alguna parte, se sigue explorando,
y si no hay salida se **deshace** la elección y se prueba la siguiente. Es una búsqueda en
profundidad sobre el árbol de decisiones, con dos ingredientes:

- **Deshacer el paso** (de ahí el nombre: *backtrack*). Si has marcado la casilla como visitada y
  la rama no lleva a ningún sitio, hay que desmarcarla al volver. Olvidar esto es el error más
  común: el programa termina antes de tiempo o da resultados de menos.
- **Podar.** Antes de seguir, comprobar si la rama puede dar una solución válida. En el problema
  de las ocho reinas, colocar dos reinas en la misma columna hace inútil explorar todo lo que
  cuelga de ahí: la poda convierte un árbol de millones de nodos en uno de miles.

La combinación de las dos cosas es lo que hace que el backtracking resuelva de verdad problemas
como sudokus, laberintos, planificación de horarios y asignación de recursos. No cambia la
naturaleza exponencial del problema: solo evita explorar el trozo del árbol que ya se sabe que no
sirve.

:::figura
fichero: recursion-llamadas-y-poda
pie: Izquierda: llamadas de Fibonacci contadas de verdad, con y sin memoria, en escala logarítmica. La curva roja (recursión ingenua) crece como φⁿ: fib(30) hace 2.692.537 llamadas para devolver un número de seis cifras, y el mismo valor con la tabla se calcula en 59 llamadas, un 99,998 % menos. La distancia entre las dos curvas mide el trabajo repetido, y es la razón de que exista la [[programacion-dinamica|memoización]]. Derecha: nodos que explora el backtracking de las n reinas (azul) frente a las nⁿ hojas del árbol de decisiones completo (rojo). Con 8 reinas la poda deja 2.057 nodos de 16.777.216, un factor de 8.000, pero las dos barras siguen creciendo: la poda recorta el árbol, no lo aplana, y el problema sigue siendo exponencial en el peor caso.
fuente: figuras/recursion-y-backtracking-1.py
:::

## Definición formal

Una función es **recursiva** si en su cuerpo aparece una llamada a sí misma. Toda recursión bien
formada tiene tres partes:

- **Caso base:** la condición bajo la que se devuelve un resultado sin volver a llamar. Sin caso
  base, la recursión no termina y el programa muere por desbordamiento de pila.
- **Paso recursivo:** la llamada con un problema estrictamente más pequeño. «Más pequeño» hay que
  demostrarlo: si el tamaño no decrece, tampoco termina.
- **Combinación:** cómo se construye el resultado del tamaño `n` a partir del resultado del
  tamaño menor.

El coste se describe con una **relación de recurrencia**. Los dos ejemplos de referencia:

:::formula
Fibonacci:  T(n) = T(n−1) + T(n−2) + Θ(1)  ⇒  T(n) = Θ(φⁿ),  con φ = (1 + √5)/2 ≈ 1,618
Búsqueda binaria recursiva:  T(n) = T(n/2) + Θ(1)  ⇒  T(n) = Θ(log₂ n)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T(n)` | trabajo total de la función con una entrada de tamaño n | operaciones (llamadas o comparaciones) | sigue la recurrencia: puede quedarse en logarítmico o dispararse |
| `n` | tamaño del problema: discos, elementos, filas del tablero | unidades del problema | en Fibonacci multiplica las llamadas por φ; en la binaria solo suma una |
| `φ` | proporción áurea, (1 + √5) / 2 ≈ 1,618 | adimensional | es la base de la exponencial: cuanto mayor, antes se hace intratable |
| `Θ(1)` | trabajo constante de combinar los resultados | operaciones | no cambia el orden del coste |
:::

donde `φ` es la proporción áurea, `n` el tamaño del problema y `Θ(1)` el trabajo constante de
combinar. La diferencia entre las dos es enorme: `1,618ⁿ` explota, `log₂ n` apenas crece.

**Backtracking.** Sea un problema cuyas soluciones se construyen tomando una secuencia de
decisiones `x₁, x₂, …, xₘ`, cada una elegida de un conjunto `Sᵢ` de candidatos. El esquema
general es:

:::formula
explorar(k): si k > m y la solución es válida → anótala
             si no, para cada candidato c en S(k): si es viable → aplica c, explorar(k+1), deshaz c
:::

- `k` — índice de la decisión que se está tomando.
- `S(k)` — candidatos posibles en el paso `k`.
- **viable** — comprobación que descarta ramas que no pueden dar solución. Es la poda.
- **deshaz `c`** — devolver el estado a como estaba antes de aplicar `c`. Es la parte que se
  olvida.

El coste del esquema sin poda es el tamaño del árbol de decisiones, `O(∏ /Sᵢ/)`; con poda, el
número de nodos que sobreviven. En el peor caso (sudoku mal planteado, laberinto sin salida) no
hay atajo: el backtracking puro es exponencial y por eso existe la
[[np-completitud|dificultad intrínseca]] de estos problemas.

## Ejemplo

**Fibonacci, coste de la recursión ingenua.** Contando llamadas:

| n | Llamadas a fib | fib(n) |
| --- | --- | --- |
| 10 | 177 | 55 |
| 20 | 21.891 | 6.765 |
| 30 | 2.692.537 | 832.040 |
| 35 | 29.860.703 | 9.227.465 |

Entre `n = 30` y `n = 35`, cinco unidades de tamaño multiplican por once el trabajo. Con
memoización, cada `n` se calcula una sola vez y el coste baja a `Θ(n)` llamadas: 36 en lugar de
casi 30 millones.

**Cuatro reinas.** Hay que colocar 4 reinas en un tablero de 4×4 sin que se amenacen entre ellas
(ni en la misma fila, ni en la misma columna, ni en la misma diagonal). Se coloca una reina por
fila, de arriba abajo, y se prueban columnas:

- Fila 0, columna 0. Válida.
- Fila 1: columna 0 amenazada (misma columna), columna 1 amenazada (diagonal). Columna 2:
  válida.
- Fila 2: columnas 0, 1 y 2 amenazadas; columna 3 amenazada por la reina de la fila 1 (diagonal
  que baja de (1,2) a (2,3)). **No hay candidata: se deshace** el paso de la fila 1.
- Fila 1, columna 3: válida. Fila 2, columna 1: válida. Fila 3: columnas 0 y 2 amenazadas,
  columna 1 amenazada por la reina de la fila 2, columna 3 amenazada por la de la fila 1.
  **No hay candidata: se deshace.**
- Se agotan las opciones y se retrocede hasta la fila 0: columna 0 no lleva a ninguna solución.
- Fila 0, columna 1. Y así hasta encontrar la primera solución: reinas en (0,1), (1,3), (2,0),
  (3,2).

El árbol completo sin poda tendría `4⁴ = 256` hojas; con la poda de columnas y diagonales, el
programa explora 17 nodos. Ese factor es exactamente el valor del backtracking.

## Código

```python verificable
import sys

def fib_llamadas(n, contador):
    contador[0] += 1
    if n < 2:
        return n
    return fib_llamadas(n - 1, contador) + fib_llamadas(n - 2, contador)

for n in (10, 20, 30):
    contador = [0]
    valor = fib_llamadas(n, contador)
    print(f"fib({n:>2}) = {valor:>8}  llamadas = {contador[0]:>9}")

# La pila de llamadas es finita: pasarse de profundidad es un error, no una lentitud.
print("limite de recursion:", sys.getrecursionlimit())   # -> limite de recursion: 1000
try:
    fib_llamadas(2000, [0])
except RecursionError:
    print("RecursionError a profundidad 2000")          # -> RecursionError a profundidad 2000
```

:::claves
- `contador` es una **lista de un elemento** y no un entero: los `int` de Python son inmutables, así que `contador += 1` dentro de la función crearía una variable local y el recuento de fuera no cambiaría. Con la lista se modifica el objeto compartido, y por eso el código no necesita `nonlocal`.
- `fib_llamadas` devuelve `n` cuando `n < 2` y no comprueba si es negativo: llamarla con `-1` devuelve −1 en lugar de avisar, y la serie seguiría bajando en cada paso recursivo.
- Las cifras del bucle son el dato del tema: `fib(30)` hace 2.692.537 llamadas para devolver 832.040. Entre `n = 20` y `n = 30` las llamadas se multiplican por 123, que es φ¹⁰ ≈ 122,99: el trabajo se multiplica por φ **cada vez que n sube una unidad**.
- `sys.getrecursionlimit()` devuelve 1000, el valor por defecto de CPython. Es el número de marcos que caben en la pila, no el de llamadas: en `fib` cada nivel de profundidad deja una llamada pendiente de terminar.
- `fib_llamadas(2000, [0])` no se hace lenta: salta `RecursionError` antes de calcular nada. Subir el límite con `setrecursionlimit` no añade memoria a la pila, solo retrasa el fallo hasta que el proceso se cae sin excepción que lo capture.
:::

```python verificable
def resolver_n_reinas(n):
    """Devuelve todas las soluciones y cuantos nodos del arbol ha explorado."""
    soluciones, nodos = [], 0

    def viable(fila, col, colocadas):
        # Solo hay que comprobar contra las reinas ya puestas: misma columna o misma diagonal.
        for f, c in colocadas:
            if c == col or abs(f - fila) == abs(c - col):
                return False
        return True

    def explorar(fila, colocadas):
        nonlocal nodos
        nodos += 1
        if fila == n:
            soluciones.append(list(colocadas))
            return
        for col in range(n):
            if viable(fila, col, colocadas):     # poda antes de seguir
                colocadas.append((fila, col))
                explorar(fila + 1, colocadas)
                colocadas.pop()                  # deshacer: el paso clave del backtracking

    explorar(0, [])
    return soluciones, nodos

for n in (4, 6):
    soluciones, nodos = resolver_n_reinas(n)
    print(f"n={n}: soluciones={len(soluciones):>3}  nodos explorados={nodos:>6}  hojas sin poda={n**n}")
# -> n=4: soluciones=  2  nodos explorados=    17  hojas sin poda=256
# -> n=6: soluciones=  4  nodos explorados=   153  hojas sin poda=46656

tablero = resolver_n_reinas(6)[0][0]
for fila, col in tablero:
    print("." * col + "R" + "." * (6 - col - 1))
# -> .R....
# -> ...R..
# -> .....R
# -> R.....
# -> ..R...
# -> ....R.
```

```python verificable
# Backtracking con deshacer sobre un laberinto: 0 = libre, 1 = muro.
laberinto = [
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
]
inicio, fin = (0, 0), (3, 4)

def buscar(celda, camino, visitadas):
    if celda == fin:
        return list(camino)
    fila, col = celda
    for df, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        f, c = fila + df, col + dc
        if 0 <= f < len(laberinto) and 0 <= c < len(laberinto[0]):
            if laberinto[f][c] == 0 and (f, c) not in visitadas:
                visitadas.add((f, c))
                camino.append((f, c))
                resultado = buscar((f, c), camino, visitadas)
                if resultado:
                    return resultado
                camino.pop()          # callejon sin salida: se deshace
    return None

camino = buscar(inicio, [inicio], {inicio})
print("pasos del camino:", len(camino))     # -> pasos del camino: 8
print("camino:", camino)
# -> camino: [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4)]
```

## Errores típicos

- **Olvidar el caso base o escribirlo mal.** Sin caso base la recursión no termina; con un caso
  base que no cubre todas las ramas (por ejemplo, tratar `n == 0` pero no `n < 0`), el error
  aparece solo con ciertas entradas. Escribe el caso base como la condición más restrictiva que
  corta todas las ramas.
- **No deshacer el paso.** Si marcas una casilla, un índice o un contador y no lo restauras al
  volver de la llamada recursiva, el estado queda sucio para las siguientes ramas. El síntoma
  habitual es «encuentra soluciones pero se salta algunas» o «devuelve un camino que no existe».
- **Mutar una lista compartida y devolverla.** `soluciones.append(colocadas)` guarda una
  **referencia** a la lista, que sigue cambiando después. Hay que copiar:
  `soluciones.append(list(colocadas))`.
- **Confundir poda con corrección.** La poda no puede descartar soluciones válidas: si la
  comprobación de viabilidad es demasiado agresiva, el backtracking devuelve «no hay solución»
  para problemas que sí la tienen. La poda es una optimización y hay que probarla aparte, con
  instancias pequeñas donde se conozca la respuesta.
- **Usar recursión donde la profundidad es lineal en los datos.** Recorrer una lista enlazada de
  un millón de nodos o un árbol degenerado con recursión revienta la pila. La versión iterativa
  con una pila explícita hace el mismo trabajo con memoria en el montón, como se ve en
  [[bfs-y-dfs|los recorridos con pila explícita]].
- **Recursión sin memoización cuando hay subproblemas repetidos.** Si el árbol de llamadas tiene
  ramas idénticas (Fibonacci, mochila, cambio de monedas), el coste exponencial es un desperdicio
  evitable: [[programacion-dinamica|la programación dinámica]] reduce el mismo cálculo a tiempo
  polinómico añadiendo una tabla.

:::trampa
`sys.setrecursionlimit(100000)` no arregla una recursión profunda: solo retrasa el fallo hasta
que el proceso se cae por desbordamiento real de la pila del sistema, sin `RecursionError` que lo
capture. Si tu algoritmo necesita profundidad proporcional a los datos, conviértelo a iterativo.
:::

:::practica
enunciado: La función hanoi(n, a, c, b) mueve un disco y se llama dos veces con n − 1 más una vez por nivel. Para 3 discos, escribe los 7 movimientos de la varilla A a la C y cuenta las llamadas totales, incluidas las del caso base n = 0.
pista: Cada llamada con n > 0 genera dos llamadas con n − 1, así que el número de llamadas cumple T(n) = 2 · T(n−1) + 1 con T(0) = 1.
solucion: Movimientos: A→C, A→B, C→B, A→C, B→A, B→C, A→C (7 = 2³ − 1). Llamadas: T(1) = 3, T(2) = 7, T(3) = 15, de las cuales 8 son del caso base. La pila llega a 4 marcos (n = 3, 2, 1, 0) y el coste crece exponencialmente con el número de discos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el Fibonacci recursivo sin memoización hace unos 2,7 millones de llamadas para n = 30?
o: Porque cada llamada crea dos nuevas y el número de llamadas crece como φⁿ
o: Porque Python es lento ejecutando llamadas a funciones
o: Porque hay que recorrer los 30 números dos veces
a: 1
e: El árbol de llamadas tiene ramas repetidas: fib(n−2) se recalcula desde cero una y otra vez, y el número total de llamadas sigue la sucesión de Fibonacci, que crece exponencialmente con base φ ≈ 1,618. No es un problema de velocidad del lenguaje: con memoización el mismo cálculo baja a 31 llamadas.
:::

:::quiz
p: En un backtracking que marca celdas visitadas, ¿qué pasa si te olvidas de desmarcarlas al volver de la llamada recursiva?
o: Nada, porque el conjunto de visitadas se recrea en cada llamada
o: El programa explora menos ramas de las que debería y puede no encontrar soluciones que existen
o: El programa entra en un bucle infinito siempre
a: 2
e: Si una celda queda marcada de una rama que falló, las ramas siguientes la verán como ya visitada y no podrán pasar por ella, aunque pertenezca a su camino. El resultado es que se pierden soluciones válidas. La marca tiene que ser parte del estado que se deshace, igual que el camino.
:::

:::quiz
p: ¿Para qué sirve la poda en el problema de las n reinas?
o: Para garantizar que se encuentran todas las soluciones en tiempo polinómico
o: Para no explorar ramas que ya violan las reglas, reduciendo el árbol de decisiones de nⁿ hojas a unos pocos nodos
o: Para deshacer los pasos que no funcionan
a: 2
e: La poda evita bajar por ramas donde dos reinas ya se amenazan: en 6 reinas, el árbol completo tendría 46.656 hojas y la poda lo deja en 153 nodos explorados. Deshacer los pasos es la otra mitad del backtracking, y el problema sigue siendo exponencial en el peor caso: la poda reduce, no elimina, la dificultad.
:::
