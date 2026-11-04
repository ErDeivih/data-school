---
id: programacion-dinamica
titulo: Programación dinámica
fase: 10
nivel: avanzado
rutas: [alg, core]
prerequisitos: [recursion-y-backtracking, complejidad-asintotica, divide-y-venceras]
tags: [algoritmos, optimizacion, memoizacion, tabulacion]
resumen: Cuando la recursión repite los mismos subproblemas, guardar sus resultados convierte un coste exponencial en uno polinómico sin cambiar el razonamiento.
fuentes: ["Bellman (1957), 'Dynamic Programming'", "Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 15", "Sedgewick y Wayne (2011), 'Algorithms', 4.ª ed., cap. 6"]
---

## En una frase

La programación dinámica resuelve problemas que se descomponen en subproblemas **solapados**
—el mismo subproblema aparece en muchas ramas— calculando cada uno una sola vez y guardándolo en
una tabla, con lo que un coste exponencial se convierte en polinómico.

## La idea

El nombre engaña. «Programación» aquí no significa escribir código, sino **planificar por
etapas** (como en programación lineal); Bellman lo eligió en los años cincuenta, entre otras
cosas, porque sonaba lo bastante aburrido para que un jefe no intentara recortarle el
presupuesto. Lo que hace la técnica es otra cosa: **no repetir trabajo**.

Volvamos a la recursión ingenua del Fibonacci que aparece en [[recursion-y-backtracking]]:
`fib(5)` llama a `fib(4)` y `fib(3)`; `fib(4)` a su vez llama a `fib(3)` y `fib(2)`. El `fib(3)`
se calcula dos veces, el `fib(2)` tres veces, y con `n = 30` el mismo valor se recalcula millones
de veces para producir un número de nueve cifras. Todas esas llamadas hacen exactamente lo mismo:
es trabajo duplicado, no dificultad del problema.

La programación dinámica se apoya en dos propiedades que hay que comprobar **antes** de usarla:

- **Subestructura óptima:** la solución óptima del problema se construye a partir de soluciones
  óptimas de sus subproblemas. Si la mejor forma de resolver un trozo dependiera de cómo se
  resolvieron los demás, no se podría componer.
- **Subproblemas solapados:** el mismo subproblema se necesita muchas veces. Si cada subproblema
  apareciera una sola vez, la recursión normal ya sería eficiente y esto no aportaría nada: ese
  es el caso de [[divide-y-venceras]], donde las mitades son disjuntas (mergesort no repite ni un
  cálculo).

Hay dos formas de implementarlo, y la elección es sobre todo de estilo:

1. **Memoización (de arriba abajo):** se escribe la recursión natural y, antes de calcular, se
   mira en un diccionario si ese subproblema ya se resolvió. Es un cambio de cinco líneas y
   conserva la legibilidad del razonamiento recursivo. El coste es el de la recursión: profundidad
   de pila y el diccionario.
2. **Tabulación (de abajo arriba):** se identifican los estados, se ordenan por tamaño creciente
   y se rellenan en un array o una matriz. Suele ser más rápida (sin llamadas ni diccionario) y
   permite ahorrar memoria si cada fila solo depende de la anterior, pero exige tener claro el
   orden de dependencias antes de empezar.

El resultado de cualquiera de las dos es el mismo: el número de operaciones pasa de exponencial a
proporcional al **número de estados distintos** multiplicado por el trabajo de cada transición.
Ese es el intercambio central: se paga memoria para no pagar tiempo.

:::figura
fichero: programacion-dinamica-arbol-y-tabla
pie: Izquierda: el árbol de llamadas de fib(5) tal como lo genera la recursión ingenua. Son 15 llamadas para 6 valores distintos; en rojo quedan los subproblemas repetidos (fib(2) se recalcula tres veces, fib(1) cinco) y en azul los que aparecen una sola vez. Ese solapamiento es la condición que tiene que cumplirse para que guardar resultados sirva de algo: donde no hay nodos repetidos, como en [[divide-y-venceras|mergesort]], la tabla solo añade memoria. Derecha: la tabla de la mochila 0/1 del ejemplo, con cada celda rellenada una sola vez a partir de la de arriba; el tono indica el valor y el camino rojo reconstruye la solución óptima hacia atrás desde la esquina de abajo (7, con los objetos A y B). Aquí la tabla rellena 24 estados frente a las 2⁴ = 16 combinaciones de la fuerza bruta: la ventaja no está en este juguete, sino en cuanto n crece.
fuente: figuras/programacion-dinamica-1.py
:::

## Definición formal

Un problema admite una formulación en programación dinámica si su solución se puede escribir como
una función `F` sobre un conjunto finito de **estados** `s`, con una **transición** que relaciona
un estado con estados más pequeños:

:::formula
F(s) = óptimo sobre las decisiones d de [ coste(s, d) + F(siguiente(s, d)) ],   con F(caso base) fijado
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `F(s)` | mejor valor alcanzable desde el estado s | la unidad del objetivo (euros, valor, distancia) | se calcula una sola vez por estado y se guarda |
| `s` | estado: lo que resume el subproblema (peso disponible, objetos considerados) | adimensional, pero tiene que ser un valor comparable | más estados distintos, más coste: O(estados × decisiones) |
| `d` | decisión posible en ese estado (coger el objeto, no cogerlo) | adimensional | más decisiones por estado, más transiciones que probar |
| `coste(s, d)` | lo que aporta esa decisión | la unidad del objetivo | entra en el máximo (o el mínimo) que define F(s) |
| `siguiente(s, d)` | estado al que lleva la decisión | el mismo tipo que s | tiene que ser estrictamente más pequeño, o la recursión no termina |
| `n` | número de objetos de la mochila | objetos | el coste es Θ(n · W): sube proporcionalmente |
| `W` | capacidad de la mochila | kilos o unidades de capacidad | pseudopolinómico: W entra como valor, no como número de bits |
| `wᵢ`, `vᵢ` | peso y valor del objeto i | kilos y unidades de valor | el objeto solo entra en la tabla si wᵢ ≤ c |
:::

- `s` — estado: lo que resume toda la información relevante del subproblema (por ejemplo, «peso
  disponible» y «número de objetos considerados»).
- `d` — decisión posible en ese estado.
- `coste(s, d)` — lo que aporta esa decisión.
- `siguiente(s, d)` — el estado al que se pasa, estrictamente «más pequeño» en el orden de
  dependencias.
- `F(caso base)` — el valor conocido de los estados mínimos.

El coste del algoritmo es `O(número de estados × decisiones por estado)`. Comparado con el coste
exponencial de explorar todas las combinaciones, esa es toda la ganancia.

**Dos ejemplos canónicos.**

*Fibonacci.* Estado = el índice `n`. Transición `F(n) = F(n−1) + F(n−2)`, con `F(0) = 0` y
`F(1) = 1`. Estados distintos: `n + 1`. Coste: `Θ(n)` frente al `Θ(φⁿ)` de la recursión pura
(con `φ ≈ 1,618`, la proporción áurea).

*Mochila 0/1.* Objetos `1..n` con peso `wᵢ` y valor `vᵢ`, y una mochila de capacidad `W`. El
estado es `(i, c)`: los primeros `i` objetos y capacidad disponible `c`. La transición es:

:::formula
F(i, c) = max( F(i−1, c),  vᵢ + F(i−1, c − wᵢ) )   si wᵢ ≤ c
:::

donde `F(i, c)` es el valor máximo alcanzable usando los primeros `i` objetos con capacidad `c`.
El primer término es «no coger el objeto `i`» y el segundo «cogerlo». Con `F(0, c) = 0` y
`F(i, c) = 0` si `c < 0`. Estados: `n · W`. Coste: `Θ(n · W)`, que es **pseudopolinómico**
(polinómico en el valor `W`, no en el número de cifras de `W`); con capacidades astronómicas deja
de ser viable, y de ahí que la mochila sea [[np-completitud|NP-dura]].

## Ejemplo

**Fibonacci con memoización, contando llamadas.** Para `n = 30`, cada valor se calcula una vez:

| n | Llamadas sin memoria | Llamadas con memoria | fib(n) |
| --- | --- | --- | --- |
| 10 | 177 | 19 | 55 |
| 20 | 21.891 | 39 | 6.765 |
| 30 | 2.692.537 | 59 | 832.040 |

Con memoización, el número de llamadas es `2n − 1` (cada valor genera una llamada que calcula y
otra que consulta la tabla), así que crece linealmente. A partir de `n = 30`, la diferencia entre
2,7 millones y 59 es el 99,998 %.

**Mochila 0/1 a mano.** Objetos con `(peso, valor)`: A = (2, 3), B = (3, 4), C = (4, 5), D = (5,
6). Capacidad `W = 5`. Recorremos los estados `F(i, c)` por filas (objetos) y columnas
(capacidad de 0 a 5):

| Objetos | c=0 | c=1 | c=2 | c=3 | c=4 | c=5 |
| --- | --- | --- | --- | --- | --- | --- |
| ninguno | 0 | 0 | 0 | 0 | 0 | 0 |
| A (2,3) | 0 | 0 | 3 | 3 | 3 | 3 |
| B (3,4) | 0 | 0 | 3 | 4 | 4 | 7 |
| C (4,5) | 0 | 0 | 3 | 4 | 5 | 7 |
| D (5,6) | 0 | 0 | 3 | 4 | 5 | 7 |

El valor óptimo es 7, y se alcanza con los objetos A y B (peso 2 + 3 = 5, valor 3 + 4 = 7). La
elección voraz por densidad —[[algoritmos-greedy|el algoritmo voraz]]— habría cogido B (densidad
4/3) y luego A (3/2), y también llega a 7 en este caso; con otros datos no, y ese es justo el
ejemplo del concepto de voraces. La tabla tiene `4 · 6 = 24` estados, y cada uno cuesta una
comparación: 24 operaciones frente a las `2⁴ = 16` combinaciones de este caso diminuto (aquí la
fuerza bruta gana; la ventaja aparece cuando hay 30 objetos, con 1.073 millones de combinaciones
frente a 30 · 6 = 180 estados).

## Código

```python verificable
from functools import lru_cache

# Version con memoizacion: se escribe la recursion natural y se envuelve.
@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)

# Version con tabulacion: se rellena de abajo arriba, sin recursion.
def fib_tabla(n):
    a, b = 0, 1                    # F(0) y F(1)
    for _ in range(n):
        a, b = b, a + b
    return a

print("fib_memo(30):", fib_memo(30))                  # -> fib_memo(30): 832040
print("fib_tabla(30):", fib_tabla(30))                # -> fib_tabla(30): 832040
print("llamadas distintas:", fib_memo.cache_info().currsize)   # -> llamadas distintas: 31
print("aciertos en cache:", fib_memo.cache_info().hits)       # -> aciertos en cache: 28
```

:::claves
- `@lru_cache(maxsize=None)` guarda el resultado **por argumento** y va contando lo que hace: `cache_info().currsize` son los 31 valores distintos que ha memorizado (de 0 a 30) y `hits` los 28 aciertos, es decir, las veces que se evitó recalcular.
- `currsize` es 31 y no 30 porque la caché guarda también `fib_memo(0)`: los estados son `n + 1`, no `n`. Y `hits` no cuenta la primera llamada de cada valor, solo las repeticiones.
- `fib_memo(30)` y `fib_tabla(30)` devuelven el mismo 832.040: la memoria no cambia el resultado, solo el número de operaciones. La diferencia entre memoización y tabulación es de estilo y de consumo, no de valor.
- `a, b = b, a + b` es una **asignación múltiple**: la parte derecha se evalúa entera antes de asignar nada, así que `a` no se pisa a mitad de camino. Escrito en dos líneas haría falta una variable temporal.
- `range(n)` da exactamente n vueltas, así que `fib_tabla(0)` devuelve 0 y `fib_tabla(1)` devuelve 1: los dos valores de arranque son F(0) y F(1), ya guardados en `a` y `b`.
- Los enteros de Python son **exactos**: `fib_memo(100)` devuelve el número completo, sin el redondeo que aparecería al pasar por coma flotante.
:::

```python verificable
def mochila_01(pesos, valores, capacidad):
    """Tabulacion de la mochila 0/1. Devuelve (valor optimo, objetos elegidos)."""
    n = len(pesos)
    # F[i][c] = mejor valor usando los i primeros objetos con capacidad c
    F = [[0] * (capacidad + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for c in range(capacidad + 1):
            F[i][c] = F[i - 1][c]                       # opcion: no coger el objeto i
            if pesos[i - 1] <= c:
                con = valores[i - 1] + F[i - 1][c - pesos[i - 1]]
                if con > F[i][c]:
                    F[i][c] = con                       # opcion: cogerlo
    # Reconstruccion hacia atras: si el valor cambio al anadir el objeto, se cogio
    elegidos, c = [], capacidad
    for i in range(n, 0, -1):
        if F[i][c] != F[i - 1][c]:
            elegidos.append(i - 1)
            c -= pesos[i - 1]
    return F[n][capacidad], sorted(elegidos)

pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
valor, elegidos = mochila_01(pesos, valores, 5)
print("valor optimo:", valor)                      # -> valor optimo: 7
print("objetos elegidos:", elegidos)               # -> objetos elegidos: [0, 1]
print("estados evaluados:", len(pesos) * 6)        # -> estados evaluados: 24
```

```python verificable
def distancia_edicion(a, b):
    """Distancia de Levenshtein por tabulacion: insertar, borrar o sustituir."""
    n, m = len(a), len(b)
    # D[i][j] = coste de convertir a[:i] en b[:j]
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i                  # borrar todo lo que sobra
    for j in range(m + 1):
        D[0][j] = j                  # insertar todo lo que falta
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            coste = 0 if a[i - 1] == b[j - 1] else 1
            D[i][j] = min(D[i - 1][j] + 1,        # borrar
                          D[i][j - 1] + 1,        # insertar
                          D[i - 1][j - 1] + coste)  # sustituir o dejar igual
    return D[n][m]

print("casa -> calle:", distancia_edicion("casa", "calle"))     # -> casa -> calle: 3
print("iguales:", distancia_edicion("datos", "datos"))          # -> iguales: 0
print("estados:", (4 + 1) * (5 + 1))                            # -> estados: 30
```

## Errores típicos

- **Usarla cuando los subproblemas no se solapan.** Si cada subproblema aparece una sola vez
  (mergesort, búsqueda binaria, recorrido de un árbol), la tabla no ahorra nada y solo añade
  memoria y complejidad. Comprueba el solapamiento antes: dibuja el árbol de llamadas de un caso
  pequeño y mira si hay nodos repetidos.
- **Confundir el número de estados con el tamaño de la entrada.** La mochila con capacidad `W`
  cuesta `Θ(n · W)`, que **no** es polinómico en el tamaño de la entrada (hacen falta `log₂ W`
  bits para escribir `W`). Por eso se dice pseudopolinómico, y por eso la mochila 0/1 sigue siendo
  NP-dura: no hay contradicción entre las dos afirmaciones.
- **Rellenar la tabla en el orden equivocado.** En la tabulación, cada celda usa celdas ya
  calculadas. Si el bucle recorre los estados antes de que estén sus dependencias, se leen ceros
  y el resultado sale mal sin dar ningún error. Antes de escribir los bucles, escribe la
  transición y deduce de ella el orden.
- **Olvidar el caso base.** Casi todos los fallos de la tabulación son una fila 0 o una columna 0
  mal inicializadas: la distancia de edición sin `D[i][0] = i` da resultados que parecen
  razonables y están mal.
- **Guardar la tabla entera cuando basta la última fila.** En la mochila y en la distancia de
  edición, cada fila depende solo de la anterior. Pasar de `Θ(n · W)` de memoria a `Θ(W)` es un
  cambio de dos líneas, y es la diferencia entre que el programa corra o se quede sin memoria con
  `W` grande. Si necesitas reconstruir la solución, entonces sí hace falta la tabla completa.
- **Memoizar con `lru_cache` sin pensar en los argumentos.** La caché se indexa por los
  argumentos tal cual: pasar una lista o un `DataFrame` como argumento hace que la memoización no
  acierte nunca (los objetos no son comparables por valor) o que la memoria crezca sin control.
  Los estados tienen que ser valores simples: enteros, tuplas, cadenas.

:::trampa
`functools.lru_cache` sobre una función que devuelve una lista guarda **la misma lista** para
todas las llamadas: si el que llama la modifica, corrompe la caché y los resultados siguientes
son incorrectos. Devuelve tuplas o copia al salir.
:::

:::practica
enunciado: Subes una escalera de 10 peldaños dando pasos de 1 o de 2. Escribe la recurrencia del número de caminos, calcula su valor para 10 peldaños y compara el coste de la tabulación con el de la recursión ingenua.
pista: El último paso fue de 1 o de 2, así que los caminos de n son los de n − 1 más los de n − 2, con F(1) = 1 y F(2) = 2. Sin memoria, el mismo subproblema se recalcula muchas veces.
solucion: F(3) = 3, F(4) = 5, F(5) = 8, F(6) = 13, F(7) = 21, F(8) = 34, F(9) = 55 y F(10) = 89 caminos. La tabulación rellena 10 estados con una suma cada uno: 10 operaciones. La recursión ingenua cumple T(n) = 1 + T(n−1) + T(n−2), que para n = 10 son 109 llamadas.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué dos propiedades tiene que cumplir un problema para que la programación dinámica aporte algo?
o: Subestructura óptima y subproblemas solapados
o: Coste lineal y datos ordenados
o: Recursión y memoria suficiente
a: 1
e: La subestructura óptima permite construir la solución con soluciones óptimas de los trozos, y el solapamiento es lo que hace que guardar resultados ahorre trabajo. Sin solapamiento, dividir el problema ya era suficiente (divide y vencerás) y la tabla no aporta nada.
:::

:::quiz
p: La mochila 0/1 se resuelve en tiempo Θ(n · W) con programación dinámica. ¿Por qué se dice que sigue siendo NP-dura?
o: Porque Θ(n · W) es demasiado lento en la práctica
o: Porque W entra en el coste como valor, no como número de bits, así que el algoritmo es pseudopolinómico
o: Porque la tabla ocupa demasiada memoria
a: 2
e: Para escribir W hacen falta log₂ W bits. Un algoritmo es polinómico si su coste está acotado por un polinomio en el tamaño de la entrada en bits; Θ(n · W) no lo está, porque duplicar los bits de W multiplica el coste por un número enorme. Es una familia de instancias con W astronómico lo que hace NP-duro al problema.
:::

:::quiz
p: ¿Qué diferencia práctica hay entre memoización y tabulación?
o: La memoización es de arriba abajo y solo calcula los estados que se necesitan; la tabulación rellena todos los estados de abajo arriba
o: La memoización es más rápida y usa menos memoria en todos los casos
o: La tabulación no sirve para problemas con subestructura óptima
a: 1
e: La memoización conserva la recursión natural y calcula solo lo alcanzable desde el estado inicial, a cambio de pila y de un diccionario. La tabulación evita llamadas y se puede optimizar la memoria a la última fila, pero paga el cálculo de estados que a lo mejor no hacían falta y exige fijar el orden de dependencias. Las dos calculan los mismos valores.
:::
