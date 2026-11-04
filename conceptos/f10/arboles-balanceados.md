---
id: arboles-balanceados
titulo: Árboles balanceados
fase: 10
nivel: avanzado
rutas: [alg]
prerequisitos: [arboles-binarios, complejidad-asintotica, recursion-y-backtracking]
tags: [estructuras, arboles, avl, rotaciones]
resumen: AVL, rojo-negro y B-árboles garantizan altura logarítmica con reglas locales de reequilibrio, y por eso sostienen los índices de las bases de datos.
fuentes: ["Adelson-Velsky y Landis (1962), 'An algorithm for the organization of information'", "Guibas y Sedgewick (1978), 'A dichromatic framework for balanced trees'", "Bayer y McCreight (1972), 'Organization and maintenance of large ordered indices'"]
---

## En una frase

Un árbol balanceado es un árbol de búsqueda que se reordena solo mediante reglas locales
—rotaciones y recoloreos— para que su altura nunca deje de ser logarítmica, y así la promesa
de O(log n) se cumple para cualquier orden de inserción, incluido el ya ordenado.

## La idea

En [[arboles-binarios]] quedó un problema abierto: la forma del árbol depende del orden en que
lleguen las claves. Si llegan ordenadas, el árbol degenera en una lista y buscar pasa de O(log
n) a O(n). Y el caso no es raro: los identificadores autoincrementales, las fechas y las series
temporales llegan ordenados casi siempre.

Los árboles balanceados resuelven eso con una idea que parece contradictoria: en vez de evitar
que el árbol se deforme, permiten que se deforme y lo arreglan inmediatamente, con operaciones
locales que no dependen del tamaño del árbol. La operación básica es la **rotación**, y consiste
en cambiar qué nodo hace de padre entre dos nodos que ya estaban uno encima del otro,
conservando la propiedad de orden. Una rotación mueve tres punteros y cuesta O(1).

Con esa pieza se construyen varias familias, y cada una elige dónde pone el listón:

- **AVL** exige que las alturas de los dos subárboles de cualquier nodo difieran como mucho en
  1. Es la condición más estricta, así que el árbol queda muy bajo (altura como mucho 1,44 ·
  log₂ n) y las búsquedas son rapidísimas; a cambio, cada inserción puede necesitar una o dos
  rotaciones más a menudo, y el borrado a veces encadena rotaciones hasta la raíz.
- **Rojo-negro** no exige nada sobre alturas, sino sobre colores. Es menos estricto: la altura
  puede llegar al doble del óptimo, así que busca algo más despacio que un AVL, pero **recolorea
  mucho y rota poco**. Por eso es la elección por defecto en las bibliotecas de propósito
  general: `std::map` de C++, `TreeMap` de Java y los mapas ordenados de la mayoría de los
  lenguajes son árboles rojo-negro.
- **B-árboles** (y su variante B+ para índices) abandonan la idea de dos hijos. Cada nodo guarda
  muchas claves y tiene muchos hijos, de forma que el árbol es anchísimo y bajísimo: con 100
  claves por nodo, un árbol de 4 niveles indexa hasta 100⁴ = 100 millones de claves. Están
  diseñados para el disco: cada nivel es una lectura de página, así que bajar 3 o 4 niveles
  cuesta 3 o 4 lecturas en vez de las ~20 de un árbol binario. Son la estructura de los índices
  de las bases de datos relacionales.
- **Treap** consigue el equilibrio por lotes: cada nodo lleva una prioridad aleatoria y el árbol
  se mantiene ordenado por clave y ordenado por prioridad a la vez. La altura esperada es
  O(log n) y no hay que guardar ni colores ni factores de equilibrio, lo que simplifica el
  código a cambio de depender de la calidad del generador aleatorio.
- **Splay** no garantiza nada por operación, pero mueve a la raíz lo que acabas de consultar; es
  el análisis amortizado aplicado a árboles, y brilla cuando los accesos están sesgados.

La consecuencia práctica de todo esto: **cuando usas un diccionario ordenado de la biblioteca
estándar, casi siempre estás usando un árbol rojo-negro sin saberlo**. Y cuando creas un índice
en una base de datos, estás creando un B-árbol. Escribir el tuyo casi nunca hace falta; saber
qué garantiza sí.

## Definición formal

En todo árbol de búsqueda, para cualquier nodo `x`, `h(x)` es la altura del subárbol que cuelga
de `x`: el número de aristas del camino más largo de `x` a una hoja, con `h(nulo) = −1` por
convenio.

**Rotación.** Con `y` el hijo izquierdo de `x`, una rotación a la derecha convierte el par en
`y` como padre y `x` como hijo derecho, reasignando el subárbol que estaba «en medio»:

- antes: `x.izq = y`, `y.der = B`
- después: `y.der = x`, `x.izq = B`

El recorrido en orden del subárbol no cambia: la rotación conserva la propiedad de orden y
cambia solo las alturas. La rotación a la izquierda es la operación simétrica.

**Factor de equilibrio** de un nodo `x`:

:::formula
FE(x) = h(x.izq) − h(x.der)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `h(x)` | Altura del subárbol que cuelga de `x` | aristas (enteros) | Alarga el camino más largo desde ese nodo: las operaciones que pasen por él cuestan más |
| `FE(x)` | Factor de equilibrio del nodo: altura izquierda menos altura derecha | entero, negativo si pesa la derecha | Al pasar de ±1 el nodo está desequilibrado y hay que rotar; en un AVL el valor absoluto nunca supera 1 |
| `n` | Número de claves guardadas | claves | La altura garantizada crece como log₂ n: multiplicar las claves por mil añade unos diez niveles |
| `t` | Orden de un B-árbol: número máximo de hijos por nodo | hijos por nodo | Cada nodo guarda más claves y el árbol se aplana; con t = 32, cuatro niveles pasan del millón de claves |
| Rotaciones | Recolocaciones locales por inserción | operaciones | Más trabajo por inserción a cambio de mantener la altura; en un AVL son como mucho 2 y no se propagan hacia arriba |
:::

donde `h(·)` es la altura del subárbol y `FE` es un entero. Las reglas de cada estructura:

| Estructura | Invariante | Altura garantizada | Rotaciones por inserción |
| --- | --- | --- | --- |
| AVL | el valor absoluto de FE es como mucho 1 en todo nodo | ≤ 1,44 · log₂(n+2) | hasta 2 |
| Rojo-negro | sin dos rojos seguidos y misma altura negra en todos los caminos | ≤ 2 · log₂(n+1) | hasta 2, más recoloreos |
| B-árbol de orden t | cada nodo salvo la raíz tiene entre t−1 y 2t−1 claves | ≤ log_t((n+1)/2) | divisiones de nodo, no rotaciones |
| Treap | clave ordenada y prioridad ordenada a la vez | O(log n) esperada | O(log n) esperadas |

**Por qué una rotación basta para reparar un AVL.** Una inserción sube la altura de un subárbol
como mucho en 1, así que el primer ancestro desequilibrado tiene FE = +2 o −2 exactamente.
Los cuatro casos posibles (izquierda-izquierda, izquierda-derecha, derecha-derecha,
derecha-izquierda) se arreglan con una o dos rotaciones, y tras el arreglo las alturas vuelven
a coincidir con las de antes de insertar: por eso **no hace falta seguir subiendo y se para**.
Ese argumento es el que convierte «reparar» en O(1) y la inserción completa en O(log n).

## Ejemplo

Partimos de un BST que ya degeneró insertando 10, 20, 30 en orden:

```
10
  \
   20
     \
      30
```

Todos los FE son −1, −1 y 0… hasta que calculamos el del nodo 10: su subárbol izquierdo está
vacío (h = −1) y el derecho tiene altura 1, así que FE(10) = −1 − 1 = −2. Está desequilibrado en
el caso «derecha-derecha», que se arregla con **una rotación a la izquierda** sobre el nodo 10:

```
      20
     /  \
   10    30
```

- Recorrido antes: 10, 20, 30. Recorrido después: 10, 20, 30. El orden no cambió.
- Altura antes: 2. Altura después: 1.
- FE(20) = 0: equilibrado.

Ahora el caso «izquierda-derecha», que necesita **dos** rotaciones. Insertamos 10, 30, 20 en
este orden:

```
10
  \
   30
  /
20
```

FE(10) = −2, pero el hijo derecho (30) tiene FE = +1, es decir que el desequilibrio «entra» por
la izquierda de un hijo derecho. La solución es rotar primero a la derecha sobre 30 y después a
la izquierda sobre 10:

```
      20
     /  \
   10    30
```

Otra vez el mismo árbol, y otra vez el orden intacto. Con esas dos piezas, cualquier secuencia
de inserciones deja el árbol con altura O(log n). Las cuentas concretas se ven en el código: con
las 720 permutaciones de las claves 1 a 6, un BST sin equilibrar acaba con altura 5 en 32 de
ellas y con altura media 3,27; el AVL, en cambio, termina con altura 2 en todas.

:::figura
fichero: arboles-balanceados-altura-y-b-arbol
pie: A la izquierda, la altura máxima que garantiza cada regla de equilibrado: el árbol perfecto (log₂ n), un AVL (hasta un 44 % más) y un rojo-negro (hasta el doble). Las tres crecen igual de despacio, así que la diferencia entre 20 y 40 niveles es una constante, no un cambio de régimen. A la derecha, por qué las bases de datos usan B-árboles: con 31 claves por nodo, tres niveles guardan 30.780 claves y cuatro llegan a 954.300, mientras que un árbol binario necesitaría veinte niveles para pasar del millón.
fuente: figuras/arboles-balanceados-1.py
:::

## Código

```python verificable
import sys
from itertools import permutations

sys.setrecursionlimit(20000)   # la recursion baja por la altura, pero conviene no ir justo

class Nodo:
    __slots__ = ("clave", "izq", "der", "altura")

    def __init__(self, clave):
        self.clave, self.izq, self.der, self.altura = clave, None, None, 0

def altura(n):
    return -1 if n is None else n.altura   # el arbol vacio mide -1, por convenio

def actualizar(n):
    n.altura = 1 + max(altura(n.izq), altura(n.der))
    return n

def rotar_derecha(y):
    """El hijo izquierdo sube; el subarbol intermedio cambia de padre."""
    x = y.izq
    y.izq = x.der
    x.der = y
    actualizar(y)
    return actualizar(x)

def rotar_izquierda(x):
    y = x.der
    x.der = y.izq
    y.izq = x
    actualizar(x)
    return actualizar(y)

def factor(n):
    return altura(n.izq) - altura(n.der)

def insertar_avl(nodo, clave):
    if nodo is None:
        return Nodo(clave)
    if clave < nodo.clave:
        nodo.izq = insertar_avl(nodo.izq, clave)
    elif clave > nodo.clave:
        nodo.der = insertar_avl(nodo.der, clave)
    else:
        return nodo
    actualizar(nodo)
    f = factor(nodo)
    if f > 1 and clave < nodo.izq.clave:        # izquierda-izquierda
        return rotar_derecha(nodo)
    if f < -1 and clave > nodo.der.clave:       # derecha-derecha
        return rotar_izquierda(nodo)
    if f > 1 and clave > nodo.izq.clave:        # izquierda-derecha: dos rotaciones
        nodo.izq = rotar_izquierda(nodo.izq)
        return rotar_derecha(nodo)
    if f < -1 and clave < nodo.der.clave:       # derecha-izquierda: dos rotaciones
        nodo.der = rotar_derecha(nodo.der)
        return rotar_izquierda(nodo)
    return nodo

def en_orden(nodo):
    if nodo is None:
        return []
    return en_orden(nodo.izq) + [nodo.clave] + en_orden(nodo.der)

avl = None
for k in (10, 20, 30):
    avl = insertar_avl(avl, k)
print("AVL tras 10,20,30:", en_orden(avl), "altura", avl.altura)   # -> AVL tras 10,20,30: [10, 20, 30] altura 1

avl = None
for k in (10, 30, 20):
    avl = insertar_avl(avl, k)
print("AVL tras 10,30,20:", en_orden(avl), "altura", avl.altura)   # -> AVL tras 10,30,20: [10, 20, 30] altura 1

avl = None
for k in range(1, 7):                  # claves ya ordenadas: el peor caso de un BST
    avl = insertar_avl(avl, k)
print("AVL con 1..6 ordenadas: altura", avl.altura)                # -> AVL con 1..6 ordenadas: altura 2
```

:::claves
- `actualizar(nodo)` recalcula `nodo.altura` **después** de tocar los hijos, y `rotar_derecha`/`rotar_izquierda` la llaman en el orden correcto: primero el que baja y luego el que sube. Si actualizas antes de recolocar, las alturas quedan mal y el árbol deja de estar equilibrado sin que salte ningún error.
- `altura(None)` es −1 por convenio, así que un nodo hoja mide 0. Con el árbol vacío devolviendo 0, `factor()` daría ±1 de más y las rotaciones se dispararían antes de tiempo.
- Las cuatro ramas de `insertar_avl` se distinguen por el signo de `f` **y** por el lado por el que entró la clave. Comprobar solo `f` no basta: un caso izquierda-derecha y otro izquierda-izquierda dan el mismo `f = +2`.
- `if clave < nodo.izq.clave` mira la clave recién insertada, no el factor del hijo. Es la forma corta de decidir entre una y dos rotaciones; con el hijo `None` fallaría, pero esa rama no se alcanza porque `f > 1` implica que el hijo existe.
- Una inserción puede necesitar **dos rotaciones** (izquierda-derecha), pero ninguna se propaga más arriba: tras reparar el primer ancestro desequilibrado, las alturas vuelven a las de antes y la recursión termina. Eso es lo que deja la inserción en O(log n).
- Duplicados: `else: return nodo` los ignora **sin reequilibrar**, porque no se ha insertado nada. Cambiar ese `return` por una rama que cuente repeticiones exige decidir de qué lado viven los iguales y respetarlo en `en_orden`.
:::

```python verificable
from itertools import permutations

class NodoBST:
    __slots__ = ("clave", "izq", "der")

    def __init__(self, clave):
        self.clave, self.izq, self.der = clave, None, None

def altura_libre(n):
    if n is None:
        return -1
    return 1 + max(altura_libre(n.izq), altura_libre(n.der))

def altura_bst_ingenuo(claves):
    """BST sin reequilibrar: la altura depende del orden de llegada."""
    raiz = None
    for c in claves:
        nuevo = NodoBST(c)
        if raiz is None:
            raiz = nuevo
            continue
        actual = raiz
        while True:
            if c < actual.clave:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
    return altura_libre(raiz)

claves = list(range(1, 7))          # 720 ordenes de insercion distintos
alturas = [altura_bst_ingenuo(p) for p in permutations(claves)]

print("permutaciones:", len(alturas))                            # -> permutaciones: 720
print("altura minima:", min(alturas))                            # -> altura minima: 2
print("altura maxima:", max(alturas))                            # -> altura maxima: 5
print("altura media:", round(sum(alturas) / len(alturas), 2))     # -> altura media: 3.27
print("degenerados (altura 5):", sum(1 for h in alturas if h == 5))  # -> degenerados (altura 5): 32
```

El segundo bloque explica por qué existen los árboles balanceados: **incluso con claves
aleatorias**, la altura media (3,27) está muy por encima del mínimo teórico (2). Y en un 4,4 %
de los órdenes posibles el árbol degenera. Un AVL, un rojo-negro o un B-árbol ignoran el orden
de llegada y siempre acaban en altura 2 con esas seis claves.

```sql ilustrativo
-- Por que los indices son B-arboles y no arboles binarios: cada nivel es una lectura de pagina.
-- Con 100 claves por nodo, un arbol de 3 niveles cubre ~1.000.000 de claves.
CREATE INDEX idx_pedidos_fecha ON pedidos (fecha_creacion);
-- El indice es un B+arbol: buscar un rango de fechas es bajar por los niveles
-- y luego recorrer las hojas enlazadas, sin tocar la tabla hasta el final.
```

## Errores típicos

- **Actualizar las alturas antes de rotar, o no actualizarlas después.** Tras una rotación, los
  dos nodos implicados cambian de altura. Si se recalcula primero el que pasa a ser hijo y luego
  el que sube, todo cuadra; al revés, el padre se calcula con la altura vieja del hijo y el
  árbol queda con metadatos mentirosos que se propagan hacia arriba.
- **Aplicar la doble rotación en el orden equivocado.** En el caso izquierda-derecha hay que
  rotar primero el hijo (a la izquierda) y después el abuelo (a la derecha). Invertir el orden
  deja el árbol tan desequilibrado como estaba, pero con los punteros ya movidos, así que el
  fallo aparece más tarde y confunde.
- **Creer que el árbol rojo-negro busca más rápido que un AVL.** Es al contrario: al permitir
  altura hasta el doble del óptimo, busca algo más despacio. Se elige porque escribe menos veces
  (menos rotaciones), no porque lea más rápido. Si tu carga es casi toda de lectura, un AVL
  suele salir mejor.
- **Creer que el factor de equilibrio se puede calcular en O(1) sin guardar la altura.** Si
  `factor` recorre el subárbol para medir su altura, cada inserción pasa a costar O(n) y todo el
  razonamiento se cae. La altura se guarda en el nodo y se actualiza en cada paso.
- **Usar un árbol binario para datos que viven en disco.** Un índice binario de un millón de
  claves tiene ~20 niveles; un B-árbol de orden 100 tiene 3. Con acceso a disco, veinte lecturas
  frente a tres no es un matiz, es la diferencia entre usable e inusable.
- **Reequilibrar en cada operación sin medir.** Si tu carga de trabajo borra y reinserta
  constantemente, el coste de mantenimiento puede superar el de las búsquedas que evita. Mide
  antes de elegir estructura, y considera un treap o un árbol de la biblioteca estándar.

:::practica
enunciado: Un índice guarda 1.000.000 de claves. Calcula la altura máxima garantizada de un AVL y de un rojo-negro, y cuántos niveles necesita un B-árbol con 100 claves por nodo.
pista: Usa las cotas de la tabla: 1,44 · log₂(n+2) para el AVL y 2 · log₂(n+1) para el rojo-negro, con log₂(1.000.000) ≈ 19,93.
solucion: log₂(1.000.002) ≈ 19,93. AVL: 1,44 · 19,93 = 28,7, así que como mucho 28 aristas. Rojo-negro: 2 · 19,93 = 39,9, hasta 39 aristas, un 40 % más de saltos. B-árbol: 100³ = 1.000.000, luego con 3 niveles de nodos ya cubre las claves. Conclusión: el B-árbol baja de unas 20 lecturas a 3 porque cada nivel es una página, no un solo nodo.
:::

## Comprueba que lo sabes

:::quiz
p: Insertas 10, 20 y 30 en un AVL vacío, en ese orden. ¿Cómo queda el árbol?
o: 10 como raíz, 20 a su derecha y 30 a la derecha de 20
o: 20 como raíz, con 10 a la izquierda y 30 a la derecha
o: 30 como raíz, con 20 a su izquierda y 10 a la izquierda de 20
a: 2
e: Tras insertar 20 y 30 sin reequilibrar quedaría una cadena con FE(10) = −2, el caso derecha-derecha. Una rotación a la izquierda sobre 10 sube el 20 a la raíz y deja 10 y 30 como hijos. La opción 1 es el estado previo al reequilibrio, y la 3 sería un árbol ordenado al revés.
:::

:::quiz
p: Un árbol rojo-negro permite altura hasta 2 · log₂(n+1), mientras que un AVL la limita a 1,44 · log₂(n+2). ¿Por qué se usa tanto el rojo-negro?
o: Porque sus búsquedas son más rápidas que las de un AVL
o: Porque reequilibrarlo cuesta menos escrituras, y esa es la operación dominante en inserciones y borrados
o: Porque un AVL no puede guardar claves duplicadas
a: 2
e: El AVL es más estricto, así que queda más bajo y busca igual o más rápido. La ventaja del rojo-negro está del lado de la escritura: sus reglas son más laxas y se repara con recoloreos, no con rotaciones. Los dos admiten claves duplicadas si se fija la convención.
:::

:::trampa
Un árbol balanceado no arregla un comparador incoherente. Si tu función de comparación no es un
orden total (por ejemplo, devuelve «iguales» para elementos que en realidad son distintos, o
depende de un campo que muta), el árbol se construye mal y las búsquedas fallan de forma
intermitente. Antes de sospechar del reequilibrio, comprueba el comparador.
:::
