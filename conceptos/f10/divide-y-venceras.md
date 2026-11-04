---
id: divide-y-venceras
titulo: Divide y vencerás
fase: 10
nivel: intermedio
rutas: [alg, core]
prerequisitos: [recursion-y-backtracking, complejidad-asintotica, ordenacion]
tags: [algoritmos, recursion, recurrencias, mergesort]
resumen: Partir el problema en subproblemas independientes del mismo tipo, resolverlos por separado y combinar; el teorema maestro dice cuánto cuesta.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 4", "Karatsuba y Ofman (1962), 'Multiplication of multidigit numbers on automata'", "Cooley y Tukey (1965), 'An algorithm for the machine calculation of complex Fourier series'"]
---

## En una frase

Divide y vencerás es la receta de tres pasos —partir la entrada en trozos más pequeños del mismo
problema, resolver cada trozo por separado y combinar los resultados— y su interés está en que
el coste total depende casi por completo de **cuánto cuesta combinar**, no de la recursión.

## La idea

Imagina que tienes que contar 4.000 monedas. Contarlas de una en una es lineal: 4.000 pasos.
Ahora reparte el montón entre cuatro personas, que cada una cuente el suyo por separado y suma
los cuatro resultados al final. El trabajo de contar no baja (sigue siendo una moneda por paso),
pero el tiempo de pared sí, porque el trabajo es paralelizable. Eso es la parte «divide».

Lo interesante llega cuando el reparto **reduce el trabajo total**. Sumar cuatro números es
lineal; multiplicar dos números de `n` cifras con el algoritmo de la escuela cuesta `n²`
operaciones: cada cifra de un número se multiplica por cada cifra del otro. Karatsuba observó en
1962 que puedes multiplicar partiendo cada número en dos mitades y hacer tres multiplicaciones
más pequeñas en vez de cuatro, y combinarlas con sumas. Tres multiplicaciones de tamaño `n/2`
cuestan menos que cuatro, así que el coste total baja de `n²` a `n^1.585`. Nadie diría que
multiplicar es «recursivo» hasta que ve que conviene partirlo.

Los tres ejemplos clásicos, con sus costes:

- **Mergesort:** partir en dos, ordenar cada mitad, fusionar. Fusionar dos listas ordenadas
  cuesta `Θ(n)` y hay `log₂ n` niveles, así que `Θ(n log n)`. Es el mismo coste que quicksort
  pero garantizado en el peor caso, a cambio de `n` de memoria extra.
- **Multiplicación de Karatsuba:** partir, tres productos recursivos, combinar con sumas.
  `Θ(n^1.585)` frente al `Θ(n²)` del método escolar.
- **Transformada rápida de Fourier (FFT):** evaluar un polinomio de grado `n` en las `n` raíces
  `n`-ésimas de la unidad evaluándolo en las raíces pares e impares y recombinando.
  `Θ(n log n)` frente al `Θ(n²)` de evaluar en cada punto.

La lección común es la que da nombre al patrón: en los tres casos, la parte recursiva no es la
que domina el coste, sino **el paso de combinar**. En mergesort, fusionar. En Karatsuba, sumar y
restar las mitades. En la FFT, la «mariposa» que mezcla las dos evaluaciones. Si el paso de
combinar fuese cuadrático, dividir no serviría de nada.

Y una condición que se salta con frecuencia: **los subproblemas tienen que ser independientes**.
Dividir un array en dos mitades que no se tocan es correcto; dividir una serie temporal por la
mitad y entrenar un modelo con cada trozo no lo es, porque la mitad derecha depende de la
izquierda. [[purged-kfold|La validación cruzada con purga]] existe precisamente porque dividir
datos que no son independientes da estimaciones falsas.

:::figura
fichero: divide-y-venceras-comparaciones-y-exponentes
pie: Izquierda: comparaciones medidas ordenando arrays aleatorios con mergesort (azul) y con ordenación por inserción (rojo), en los dos ejes en escala logarítmica. Con 4.096 elementos el mergesort hace 43.954 comparaciones frente a 4.194.466 de la inserción, y la distancia se abre con n porque una curva es n log₂ n y la otra n²: la pendiente 2 de la recta roja significa que duplicar la entrada cuadruplica el trabajo. Derecha: el mismo efecto en el coste de multiplicar. El método escolar es n², Karatsuba baja el exponente a 1,585 y la FFT a n log₂ n; con cuatro cifras las tres curvas se confunden y dividir no aporta nada, mientras que con un millón de cifras la diferencia es de 10¹² operaciones frente a 3,2 · 10⁹. La conclusión es la del tema: lo que decide el coste no es partir, sino cuánto cuesta combinar.
fuente: figuras/divide-y-venceras-1.py
:::

## Definición formal

Un algoritmo sigue el patrón divide y vencerás si:

1. **Divide** la entrada de tamaño `n` en `a` subproblemas, cada uno de tamaño `n/b`.
2. **Vence** cada subproblema recursivamente, hasta que el tamaño es tan pequeño que se resuelve
   directamente (el caso base, habitualmente `n = 1`).
3. **Combina** las `a` soluciones en la solución del problema original, con coste `f(n)`.

Su coste `T(n)` cumple la recurrencia:

:::formula
T(n) = a · T(n / b) + f(n),   T(1) = Θ(1)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T(n)` | coste total del algoritmo con una entrada de tamaño n | operaciones | lo fija el teorema maestro a partir de a, b y f(n) |
| `n` | tamaño de la entrada | elementos, cifras o puntos de la muestra | el caso del teorema no cambia, pero el coste absoluto sí |
| `a` | número de subproblemas en que se divide | subproblemas (2 en mergesort, 3 en Karatsuba) | sube el exponente log_b a y con él el coste |
| `b` | factor por el que encoge cada subproblema | adimensional, mayor que 1 | baja el exponente: trozos más pequeños, menos trabajo |
| `f(n)` | coste de dividir y de combinar las soluciones | operaciones | si crece más rápido que n^(log_b a), acaba mandando él |
| `log_b a` | función crítica: exponente con el que se compara f(n) | exponente (1 en mergesort, 1,585 en Karatsuba) | es la frontera entre los tres casos del teorema |
:::

donde `n` es el tamaño de la entrada, `a ≥ 1` el número de subproblemas, `b > 1` el factor por el
que se reduce el tamaño y `f(n)` el coste de dividir y combinar.

**Teorema maestro.** Comparando `f(n)` con la función crítica `n^(log_b a)`:

| Caso | Condición | Resultado |
| --- | --- | --- |
| 1 | f(n) = O(n^(log_b a − ε)) con ε > 0 | T(n) = Θ(n^(log_b a)) |
| 2 | f(n) = Θ(n^(log_b a) · log^k n), con k igual a 0, 1, 2… | T(n) = Θ(n^(log_b a) · log^(k+1) n) |
| 3 | f(n) = Ω(n^(log_b a + ε)) y se cumple la condición de regularidad | T(n) = Θ(f(n)) |

Las tres recurencias que hay que reconocer de memoria:

:::formula
Mergesort:   a=2, b=2, f(n)=Θ(n)  ⇒  log_b a = 1  ⇒  T(n) = Θ(n · log₂ n)
Karatsuba:   a=3, b=2, f(n)=Θ(n)  ⇒  log_b a ≈ 1,585  ⇒  T(n) = Θ(n^1,585)
Búsqueda binaria:  a=1, b=2, f(n)=Θ(1)  ⇒  log_b a = 0  ⇒  T(n) = Θ(log₂ n)
:::

En el caso 3, la «condición de regularidad» exige que `a · f(n/b) ≤ c · f(n)` para alguna
constante `c < 1` y todo `n` suficientemente grande; sin ella, el teorema no se puede aplicar.

## Ejemplo

**Mergesort con 8 elementos:** `[38, 27, 43, 3, 9, 82, 10, 1]`. El árbol de particiones tiene
`log₂ 8 = 3` niveles:

- Nivel 0: 1 array de tamaño 8.
- Nivel 1: 2 arrays de tamaño 4.
- Nivel 2: 4 arrays de tamaño 2.
- Nivel 3: 8 arrays de tamaño 1 (caso base).

Fusionar todo el nivel cuesta `Θ(n)` en total, aunque esté repartido en trozos: en el nivel 2 hay
4 fusiones de 2 elementos, en el nivel 1 hay 2 fusiones de 4 elementos y en el nivel 0 una fusión
de 8. Con este array concreto salen 17 comparaciones en total, cómodamente por debajo del máximo
teórico de 24 (los `n − 1` de cada nivel, sumados), y muy lejos de las 28 comparaciones del peor
caso de la ordenación por inserción con 8 elementos. El trabajo total cabe en `3` niveles, que es
exactamente `log₂ 8`.

**Karatsuba con dos números de 4 cifras.** Multiplicamos `1234 · 5678` partiéndolos en mitades:

- `a = 12`, `b = 34`, `c = 56`, `d = 78`, todos de 2 cifras.
- `ac = 12 · 56 = 672`, `bd = 34 · 78 = 2652`, y `(a+b)(c+d) = 46 · 134 = 6164`.
- El término cruzado es `(a+b)(c+d) − ac − bd = 6164 − 672 − 2652 = 2840`.
- Resultado: `ac · 10⁴ + cruzado · 10² + bd = 6720000 + 284000 + 2652 = 7006652`.

Comprobación directa: `1234 · 5678 = 7006652`. El método escolar habría hecho `4 · 4 = 16`
multiplicaciones de una cifra; Karatsuba hace 3 multiplicaciones de 2 cifras (que a su vez se
parten) y unas pocas sumas. Con 4 cifras da igual; con un millón de cifras es la diferencia entre
`n²` y `n^1,585`.

## Código

```python verificable
def mergesort_contando(a):
    """Mergesort que devuelve (ordenado, comparaciones) y permite ver la recursion."""
    if len(a) <= 1:
        return a, 0
    medio = len(a) // 2
    izq, c1 = mergesort_contando(a[:medio])
    der, c2 = mergesort_contando(a[medio:])
    salida, i, j, c3 = [], 0, 0, 0
    while i < len(izq) and j < len(der):
        c3 += 1
        if izq[i] <= der[j]:
            salida.append(izq[i]); i += 1
        else:
            salida.append(der[j]); j += 1
    return salida + izq[i:] + der[j:], c1 + c2 + c3

datos = [38, 27, 43, 3, 9, 82, 10, 1]
ordenado, comparaciones = mergesort_contando(datos)
print("ordenado:", ordenado)
# -> ordenado: [1, 3, 9, 10, 27, 38, 43, 82]
print("comparaciones:", comparaciones, "de un maximo teorico de", 8 * 3)   # -> comparaciones: 17 de un maximo teorico de 24
print("niveles de particion:", 3)                                          # -> niveles de particion: 3
```

:::claves
- `mergesort_contando` devuelve una **tupla** `(lista_ordenada, comparaciones)`, no una lista: `resultado = mergesort_contando(datos)` y luego `resultado[0]`, o desempaquetar en dos nombres. El contador viaja por el valor de retorno, así que no hace falta ninguna variable global ni `nonlocal`.
- El caso base es `len(a) <= 1` y no `== 1`: así una lista vacía también corta la recursión y devuelve cero comparaciones en vez de fallar al partirla.
- `a[:medio]` **copia** la mitad de la lista en cada llamada: el algoritmo ordena bien, pero gasta n log₂ n de memoria en copias en lugar de n. La versión eficiente trabaja con índices sobre el mismo array y un único buffer auxiliar.
- `return salida + izq[i:] + der[j:]` concatena tres listas y crea una nueva. Los trozos que sobran de un lado se pegan **sin comparar**, y por eso este array hace 17 comparaciones y no las 24 del máximo teórico: el `c3` solo cuenta las vueltas del `while`.
- `c1 + c2 + c3` suma las comparaciones de las dos mitades y las de la fusión. El contador es local a cada llamada, así que cada nivel devuelve su propio total y la suma se hace al volver.
- Con 8 elementos salen 3 niveles de partición, exactamente log₂ 8, y la lista final es la misma que devolvería `sorted`: contar comparaciones no cambia el resultado, solo lo hace medible.
:::

```python verificable
def karatsuba(x, y):
    """Multiplicacion de enteros por divide y venceras: 3 productos de n/2 cifras."""
    if x < 10 or y < 10:
        return x * y                      # caso base: una cifra
    n = max(len(str(x)), len(str(y)))
    mitad = n // 2
    potencia = 10 ** mitad
    a, b = divmod(x, potencia)
    c, d = divmod(y, potencia)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    cruzado = karatsuba(a + b, c + d) - ac - bd     # aqui esta el ahorro: un producto menos
    return ac * potencia * potencia + cruzado * potencia + bd

print("1234 * 5678  =", karatsuba(1234, 5678))    # -> 1234 * 5678  = 7006652
print("coincide con *:", karatsuba(1234, 5678) == 1234 * 5678)   # -> coincide con *: True
print("987654 * 3210 =", karatsuba(987654, 3210))  # -> 987654 * 3210 = 3170369340
```

```python verificable
import time

# La division solo compensa si los subproblemas son mas baratos: comparamos tamanos.
def maximo_dyv(a):
    """Maximo por divide y venceras: partir hasta 1 elemento y combinar comparando."""
    if len(a) == 1:
        return a[0]
    medio = len(a) // 2
    return max(maximo_dyv(a[:medio]), maximo_dyv(a[medio:]))

def maximo_lineal(a):
    mejor = a[0]
    for v in a[1:]:
        if v > mejor:
            mejor = v
    return mejor

datos = list(range(1000, 0, -1))          # 1000 numeros, el maximo esta al principio
print("maximo dyv:   ", maximo_dyv(datos))       # -> maximo dyv:    1000
print("maximo lineal: ", maximo_lineal(datos))   # -> maximo lineal:  1000

inicio = time.perf_counter()
for _ in range(100):
    maximo_dyv(datos)
t_dyv = (time.perf_counter() - inicio) / 100

inicio = time.perf_counter()
for _ in range(100):
    maximo_lineal(datos)
t_lineal = (time.perf_counter() - inicio) / 100

print(f"dyv {t_dyv * 1e6:.1f} us  lineal {t_lineal * 1e6:.1f} us")
print("dyv es mas lento:", t_dyv > t_lineal)     # -> dyv es mas lento: True
```

## Errores típicos

- **Dividir problemas cuyos subproblemas no son independientes.** Es el error que arruina
  análisis de datos: partir una serie temporal por la mitad o dividir clientes que comparten
  sesiones entre entrenamiento y prueba. Si las mitades se influyen, el resultado de cada una no
  es el del problema original restringido. En series temporales, la división tiene que respetar
  el orden, como en [[validacion-temporal|la validación walk-forward]].
- **Aplicar el teorema maestro sin comprobar la condición de regularidad.** El caso 3 exige
  `a · f(n/b) ≤ c · f(n)` con `c < 1`. Con `f(n)` que crece de forma extraña, el teorema no dice
  nada y hay que resolver la recurrencia por otro método (sustitución o árbol de recursión).
- **Elegir mal el tamaño del caso base.** Si bajas la recursión hasta un elemento, pagas
  muchísimas llamadas para trozos diminutos. Casi todas las bibliotecas cortan antes (Timsort usa
  tramos de 32 a 64 elementos y los ordena con inserción directa, que es más rápida en arrays
  pequeños). El caso base no es «tamaño 1» por obligación: es «el tamaño en que la versión
  directa es más rápida».
- **Olvidar el coste de memoria de las particiones.** Cada `a[:medio]` en Python **copia** la
  lista. Un mergesort escrito así reserva `n log n` de memoria en copias, no `n`. La versión
  eficiente trabaja con índices sobre el array original y un único buffer auxiliar.
- **Creer que divide y vencerás siempre es más rápido.** Repartir un problema lineal como
  encontrar el máximo añade llamadas, copias y marcos de pila para hacer las mismas `n − 1`
  comparaciones. Dividir solo compensa cuando el coste de combinar crece más despacio que el
  número de subproblemas: es lo que mide `log_b a`.
- **Combinar mal por no ordenar la salida del paso anterior.** En mergesort, la fusión exige que
  las dos mitades estén ordenadas; si la partición no cubre todo el array (un `<` en vez de `<=`,
  un rango mal cerrado), la fusión produce una lista que no está ordenada y el error aparece
  mucho más arriba, con un `sorted` que «a veces» falla.

:::nota
La FFT se puede leer como divide y vencerás puro: la transformada de tamaño `n` se calcula a
partir de dos transformadas de tamaño `n/2` (las de los índices pares e impares) y el paso de
combinar son `n/2` «mariposas» de coste constante. De ahí sale `Θ(n log n)`. La misma idea
sostiene la multiplicación rápida de polinomios.
:::

:::practica
enunciado: Ordena la lista [8, 7, 6, 5, 4, 3, 2, 1] con el mergesort de la página, que cuenta una comparación por cada vuelta del bucle de fusión. ¿Cuántas comparaciones hace en cada nivel del árbol de particiones y cuántas en total?
pista: El árbol tiene log₂ 8 = 3 niveles: cuatro fusiones de 2 elementos, dos de 4 y una de 8. Cuando el lado izquierdo siempre es mayor, el bucle consume entero el lado derecho.
solucion: Fusiones de tamaño 2: 4 fusiones × 1 comparación = 4. De tamaño 4: 2 × 2 = 4. De tamaño 8: 1 × 4 = 4. Total: 12 comparaciones, frente a las 24 del máximo teórico n · log₂ n y a las 28 del peor caso de la ordenación por inserción.
:::

## Comprueba que lo sabes

:::quiz
p: En la recurrencia T(n) = 2 · T(n/2) + Θ(n), ¿cuál es el coste total y por qué?
o: Θ(n), porque el caso base se alcanza rápido
o: Θ(n log n), porque hay log₂ n niveles y cada nivel cuesta Θ(n) en total
o: Θ(n²), porque hay que fusionar todos los pares
a: 2
e: El árbol de recursión tiene log₂ n niveles, tantos como divisiones por 2 hacen falta para llegar a un elemento, y en cada nivel el trabajo de dividir y fusionar suma Θ(n). Multiplicando, Θ(n log n). Decir Θ(n) olvida los niveles y decir Θ(n²) confunde el coste de una fusión con el de comparar todos los pares.
:::

:::quiz
p: ¿Por qué Karatsuba multiplica más rápido que el método escolar si hace lo mismo, partir en mitades?
o: Porque usa tres productos recursivos en vez de cuatro, y 3 · (n/2)^1,585 crece menos que 4 · (n/2)²
o: Porque aprovecha los ceros de los números
o: Porque suma en vez de multiplicar, y sumar es más rápido
a: 1
e: El método escolar necesita 4 productos de tamaño n/2 y da n². Karatsuba calcula ac, bd y (a+b)(c+d), y obtiene el término cruzado con restas, así que hace 3 productos. Con la recurrencia T(n) = 3T(n/2) + Θ(n) sale n^1,585, mejor que n². No hay ceros ni magia en las sumas: el ahorro es un producto menos por nivel.
:::

:::quiz
p: Divides un dataset de transacciones en dos mitades, entrenas un modelo con cada una y comparas los resultados. ¿Qué está mal?
o: Nada, es una forma válida de validar
o: Que las dos mitades no son independientes: si hay patrones temporales, cada mitad depende de la otra
o: Que hace falta entrenar con el dataset completo para que sea válido
a: 2
e: Dividir y vencerás exige subproblemas independientes. En datos con estructura temporal, la mitad derecha contiene el futuro de la izquierda y las dos comparten régimen de mercado, así que el resultado de cada mitad no estima el rendimiento del modelo. Para eso están la validación con purga y el walk-forward, que respetan el orden del tiempo.
:::
