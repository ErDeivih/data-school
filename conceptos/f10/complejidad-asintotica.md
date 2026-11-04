---
id: complejidad-asintotica
titulo: Complejidad asintótica
fase: 10
nivel: básico
rutas: [alg, de]
prerequisitos: [notacion-matematica]
tags: [algoritmos, coste, analisis, rendimiento]
resumen: Como crece el trabajo de un algoritmo cuando crece la entrada: O, Ω y Θ sirven para comparar dos soluciones sin cronómetro y sin depender de la máquina.
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 3", "Sedgewick y Wayne (2011), 'Algorithms'"]
---

## En una frase

La complejidad asintótica describe cómo crece el trabajo de un algoritmo al crecer el tamaño de
la entrada, ignorando a propósito las constantes y los detalles de la máquina: es la forma de
decidir cuál de dos soluciones aguanta cuando los datos se multiplican por mil.

## La idea

Imagina que tienes que encontrar un nombre en una guía de teléfonos de papel con un millón de
entradas. Si las entradas estuvieran en orden alfabético, abres por la mitad, miras si el nombre
que buscas va antes o después, y descartas media guía de golpe. Repites la jugada y en cada paso
te queda la mitad: 1.000.000 → 500.000 → 250.000 → … En 20 pasos has llegado a una sola entrada,
porque 2²⁰ es algo más de un millón. Si la guía estuviera desordenada, no habría más remedio que
leer nombres uno a uno: 500.000 comparaciones de media. Mismo problema, mismo ordenador, factor
25.000 de diferencia.

Lo que acabas de comparar no son dos programas concretos ni dos lenguajes: son dos **formas de
crecer**. La búsqueda lineal hace un trabajo proporcional al número de elementos; la binaria hace
un trabajo proporcional a cuántas veces puedes partir el problema por la mitad, que es el
logaritmo en base 2. Cuando el orden de magnitud es distinto, ninguna constante te salva: si
multiplicas la lista por mil, la lineal tarda mil veces más y la binaria solo necesita diez pasos
más.

La notación asintótica escribe esa idea con tres letras, y cada una responde a una pregunta
distinta. **O** (o grande) pone un techo: «este algoritmo no hace más trabajo que esto». **Ω**
pone un suelo: «no puede hacer menos que esto». **Θ** (theta) pone las dos cosas a la vez: «hace
exactamente esto, salvo constantes». Cuando alguien dice «esto es O(n²)» casi siempre quiere
decir Θ(n²), pero la distinción importa cuando el algoritmo tiene un caso bueno y uno malo.

:::figura
fichero: complejidad-crecimientos-y-pendientes
pie: Arriba están los cinco crecimientos habituales juntos, y el eje vertical va en escala logarítmica: sin ella no cabrían en el mismo dibujo, porque entre el logarítmico y el cuadrático hay seis órdenes de magnitud con n = 1.000. Lo que hay que mirar es la separación entre curvas, no el valor de cada una: con n = 100 el cuadrático hace 10.000 operaciones y el logarítmico 7, y esa distancia crece sin parar. Abajo, las dos curvas del ejemplo de la página en escala log-log: cada orden de crecimiento es una pendiente distinta, y con un millón de elementos la distancia entre `n log₂ n` y `n²` es de un factor 75.000. Ese factor es la razón de que una prueba con datos pequeños no distinga un algoritmo bueno de uno malo, y de que el orden manda sobre la constante en cuanto n crece.
fuente: figuras/complejidad-asintotica-1.py
:::

Hay dos consecuencias que se olvidan todo el rato. La primera: O no son segundos. Una función
O(n²) con una constante diminuta puede ganar a una O(n log n) con una constante enorme mientras
la entrada sea pequeña; la asintótica habla de qué pasa **cuando n crece**, y siempre hay un
umbral a partir del cual manda el orden. La segunda: hay que decir **de qué** se mide el coste
(comparaciones, accesos a memoria, bytes leídos) y **en qué caso** (el mejor, el peor, el
promedio). Un mismo algoritmo puede ser O(1) en el mejor caso y O(n) en el peor.

## Definición formal

Sea `T(n)` el número de operaciones elementales que ejecuta un algoritmo con una entrada de
tamaño `n`.

- **O(f(n))** — «T crece como mucho como f». Existen una constante `c > 0` y un umbral `n₀` tales
  que `T(n) ≤ c · f(n)` para todo `n ≥ n₀`. Es una cota **superior**.
- **Ω(f(n))** — «T crece al menos como f». Existen `c > 0` y `n₀` tales que `T(n) ≥ c · f(n)`
  para todo `n ≥ n₀`. Es una cota **inferior**.
- **Θ(f(n))** — las dos anteriores a la vez: `c₁ · f(n) ≤ T(n) ≤ c₂ · f(n)` desde cierto `n₀`.
- **c** — constante positiva que absorbe el coste de una operación, el lenguaje y la máquina.
- **n₀** — tamaño de entrada a partir del cual la comparación es válida. Antes de `n₀` puede
  pasar cualquier cosa y la notación no dice nada.
- **n** — tamaño de la entrada: elementos de una lista, nodos de un grafo, filas de una tabla.

Como se calcula, en cuatro reglas:

1. **Fuera constantes.** `5n + 20` es Θ(n): el 5 y el 20 no cambian la forma de la curva.
2. **Fuera términos menores.** `3n² + 50n + 1.000` es Θ(n²): a partir de `n = 100`, el término
   cuadrático ya pesa más que los otros dos juntos.
3. **En secuencia se suma y gana el mayor.** Recorrer la lista (Θ(n)) y luego ordenarla
   (Θ(n log n)) es Θ(n log n).
4. **Anidado se multiplica.** Un bucle de `n` iteraciones que dentro recorre `n` elementos es
   Θ(n²).

Crecimientos habituales, con números concretos:

| n | n log₂ n | n² | n² dividido entre n log₂ n |
| --- | --- | --- | --- |
| 100 | 664 | 10.000 | 15,1 |
| 1.000 | 9.966 | 1.000.000 | 100,3 |
| 10.000 | 132.877 | 100.000.000 | 752,6 |
| 100.000 | 1.660.964 | 10.000.000.000 | 6.020,6 |

La última columna es la trampa: para `n = 100` los dos crecimientos se parecen (factor 15) y para
`n = 100.000` no se parecen en nada (factor 6.020). Por eso una prueba con datos pequeños no
distingue un algoritmo bueno de uno malo.

También hay complejidad **espacial**: la memoria extra que consume el algoritmo, sin contar la
entrada. Un recorrido iterativo de una lista usa Θ(1) de espacio extra; el mismo recorrido escrito
con recursión usa Θ(n) de pila, y con `n = 100.000` eso puede agotar el límite de recursión antes
que el tiempo.

## Ejemplo

Lista ordenada con los 524.288 primeros números pares (de 0 a 1.048.574) y buscamos el valor
900.000, que ocupa la posición 450.000 contando desde cero.

- **Búsqueda lineal:** compara desde el principio; encuentra el valor en la comparación 450.001.
- **Búsqueda binaria:** `log₂(524.288) = 19`, así que hace 19 comparaciones.
- Cociente: 450.001 / 19 ≈ 23.684. El mismo trabajo, 23.000 veces menos.

Y el efecto del crecimiento cuadrático: recorrer una tabla de 10.000 elementos y compararlos
todos contra todos son 10.000² = 100.000.000 de operaciones. Si aceptamos como supuesto de trabajo
que la máquina hace 100 millones de operaciones elementales por segundo (es un supuesto de orden
de magnitud, no una medida de tu ordenador), ese algoritmo tarda alrededor de un segundo, mientras
que la versión Θ(n log₂ n) del mismo problema hace 132.877 operaciones, unas 750 veces menos.

## Código

```python verificable
# Contamos comparaciones en vez de segundos: el cronometro depende de la maquina,
# el conteo de operaciones no.
datos = list(range(0, 2 ** 20, 2))          # 524288 numeros pares ordenados
objetivo = 900000                            # esta en la posicion 450000

def lineal(v, x):
    for i, y in enumerate(v):                # recorre hasta encontrarlo
        if y == x:
            return i, i + 1
    return -1, len(v)

def binaria(v, x):
    lo, hi, comps = 0, len(v) - 1, 0
    while lo <= hi:
        medio = (lo + hi) // 2               # parte el espacio de busqueda por la mitad
        comps += 1
        if v[medio] == x:
            return medio, comps
        if v[medio] < x:
            lo = medio + 1
        else:
            hi = medio - 1
    return -1, comps

print("elementos en la lista ", len(datos))               # -> elementos en la lista  524288
print("comparaciones lineal  ", lineal(datos, objetivo)[1])   # -> comparaciones lineal   450001
print("comparaciones binaria ", binaria(datos, objetivo)[1])  # -> comparaciones binaria  19
```

:::claves
- `list(range(0, 2 ** 20, 2))` construye la lista entera en memoria: 524.288 enteros. No es una vista ni un generador, es una lista de verdad, y por eso `list(...)` es necesario aquí: sin él, `range` también funcionaría en los bucles pero `len(datos)` fallaría.
- `binaria` devuelve una **tupla** `(posición, comparaciones)` y el código solo usa el segundo elemento con `[1]`. La posición se calcula igual, así que si el valor no estuviera en la lista la función devolvería `-1` en el primer hueco: la tupla siempre tiene la misma forma, haya éxito o no.
- El `while lo <= hi` con `medio = (lo + hi) // 2` usa división **entera**: con `lo = 0` y `hi = 5`, `medio` vale 2. Si escribieras `/`, `v[medio]` daría error de tipo porque las listas de Python no admiten índices decimales (a diferencia de NumPy, que los redondearía). El `//` es obligatorio.
- `comparaciones lineal 450001` es el dato que enseña: con la lista de 524.288 elementos, la búsqueda lineal hace 450.001 comparaciones y la binaria 19. Esa cifra no es una estimación, es el conteo exacto de ejecuciones del cuerpo, y es la razón de medir así y no con un cronómetro: el conteo no depende de la máquina.
- Cambiar el `return i, i + 1` de `lineal` por `return i` haría que `lineal(datos, objetivo)[1]` fallara con `TypeError: 'int' object is not subscriptable`. El `i + 1` es el número de comparaciones contando desde 1 (la posición es `i`, que empieza en 0), y por eso el resultado es 450.001 y no 450.000.
- En `binaria`, `comps += 1` va **después** de calcular `medio` y **antes** de comparar: cada vuelta del bucle gasta exactamente una comparación. Si lo movieras dentro del `if`, la última vuelta (la que no encuentra) no contaría y el total saldría 18 en lugar de 19.
:::

```python verificable
import math

# Los tres crecimientos clasicos, con numeros en vez de dibujos.
print("n".rjust(8), "n*log2(n)".rjust(12), "n^2".rjust(16), "n^2/(n*log2 n)".rjust(17))
for n in (100, 1000, 10000, 100000):
    print(f"{n:>8d} {n * math.log2(n):>12.0f} {n * n:>16d} {n / math.log2(n):>17.1f}")

# Duplicar la entrada cuesta una comparacion mas en la busqueda binaria:
print("2^19 elementos:", math.ceil(math.log2(2 ** 19)), "comparaciones")  # -> 2^19 elementos: 19 comparaciones
print("2^20 elementos:", math.ceil(math.log2(2 ** 20)), "comparaciones")  # -> 2^20 elementos: 20 comparaciones
```

:::claves
- `print("n".rjust(8), "n*log2(n)".rjust(12), ...)` usa `rjust` en vez de una f-string a propósito: los encabezados son cadenas y `rjust` las alinea a la derecha al ancho que le pidas. En las filas de datos sí se usa f-string con `:>8d`, que es lo mismo pero aplicado a un número.
- `f"{n:>8d}"` solo funciona con un **entero**: la `d` de `d`ecimal entero lanza `ValueError` si `n` fuera un `float`. Y `n * n` con `n` entero de Python no desborda nunca, así que `100000 ** 2` sale exacto y no como un número en notación científica.
- `n / math.log2(n)` es una división normal, así que el resultado es `float` incluso con `n` entero. Ese cociente es la columna que se lee mal: no es un porcentaje, es «cuántas veces cabe el logarítmico en el cuadrático», y por eso crece con `n` en lugar de estabilizarse.
- `math.ceil(math.log2(2 ** 20))` devuelve 20 exacto, y el `ceil` está ahí por los tamaños que no son potencia de dos: `math.log2(1000)` vale 9,9657 y en coma flotante puede salir 9,999999999999998, así que redondear hacia arriba evita quedarse una comparación corto. Para 1.000 elementos el número real de comparaciones en el peor caso es 10.
- `math.log2` es más preciso que `math.log(x, 2)` para potencias de dos, y más rápido. Con `1000` los dos coinciden; con `2 ** 29` la diferencia se ve en los últimos decimales, que es justo donde el `ceil` decide entre 29 y 30.
:::

```python ilustrativo
# Coste escondido de operaciones que parecen de una linea.
lista = list(range(100000))

len(lista)            # O(1): la longitud esta guardada, no se cuenta
99999 in lista        # O(n): recorre comparando uno a uno
lista[50000]          # O(1): acceso por indice
conjunto = set(lista)
99999 in conjunto     # O(1) de media: calcula el hash y mira en un cubo
lista.insert(0, -1)   # O(n): desplaza los 100000 elementos a la derecha
```

## Errores típicos

- **Leer O(n) como «tarda poco» o «tarda lo mismo».** La notación no dice nada del tiempo
  absoluto. Un algoritmo Θ(n) con `n = 10⁹` y una operación de 100 ns por elemento tarda 100
  segundos; otro Θ(n²) con `n = 1.000` tarda milisegundos. El orden manda solo cuando `n` crece.
- **Contar líneas de código en vez de operaciones.** Un `for` de tres líneas puede esconder un
  recorrido completo de la lista dentro; lo que cuenta es cuántas veces se ejecuta el cuerpo.
  Antes de asignar un coste, pregúntate qué hace cada línea por dentro.
- **Confundir bucles anidados (multiplicar) con bucles seguidos (sumar).** Dos bucles de `n` uno
  detrás del otro son Θ(n); uno dentro de otro son Θ(n²). Es el error que más cambia la
  conclusión de un análisis.
- **Olvidar el coste de las operaciones de biblioteca.** `x in lista`, `lista.insert(0, x)`,
  `lista.pop(0)` y concatenar cadenas dentro de un bucle son O(n) cada una. Metidas en un bucle
  de `n` iteraciones convierten un algoritmo lineal en cuadrático sin que se vea ningún bucle
  anidado. En [[arrays-y-listas]] y en [[pilas-y-colas]] están las alternativas.
- **Comparar el mejor caso de uno con el peor del otro.** La búsqueda lineal encuentra el primer
  elemento en una comparación y el último en `n`. Si no dices qué caso estás midiendo, la
  comparación no significa nada. Di siempre «en el peor caso» o «de media».

:::practica
enunciado: Dos algoritmos resuelven el mismo problema con n = 2.048 elementos: uno hace n² operaciones y otro n · log₂ n. Calcula las operaciones de cada uno, su cociente, y cuántas haría el cuadrático si n se duplicara a 4.096.
pista: log₂ 2.048 = 11 porque 2¹¹ = 2.048; al duplicar n, n² se multiplica por 4 y n log₂ n casi por 2.
solucion: Cuadrático: 2.048² = 4.194.304 operaciones. Logarítmico: 2.048 · 11 = 22.528. Cociente: 4.194.304 / 22.528 ≈ 186. Al duplicar n, el cuadrático pasa a 4.096² = 16.777.216 (cuatro veces más) y el logarítmico a 4.096 · 12 = 49.152 (algo más del doble). Conclusión: con n pequeño la diferencia ya es de dos órdenes, y crece con n.
:::

## Comprueba que lo sabes

:::quiz
p: Un algoritmo hace 3n² + 50n + 1.000 operaciones. ¿Cuál es su complejidad?
o: Θ(n²), porque el término cuadrático domina cuando n crece
o: Θ(3n² + 50n), porque la constante 1.000 es despreciable
o: Θ(n³), porque hay un término cuadrático y otro lineal
a: 1
e: Al crecer n, el término n² acaba pesando más que los otros dos juntos, así que el crecimiento es cuadrático. Los términos menores y las constantes se descartan: 3n² y n² son la misma clase. Sumar exponentes no tiene ningún sentido aquí.
:::

:::quiz
p: ¿Por qué una búsqueda binaria en una lista ordenada de un millón de elementos necesita unas 20 comparaciones?
o: Porque divide el espacio de búsqueda por la mitad en cada paso y 2 elevado a 20 supera un millón
o: Porque recorre la lista en bloques de 50.000 elementos
o: Porque compara solo los elementos de las posiciones pares
a: 1
e: Cada comparación descarta la mitad de los candidatos: 1.000.000, 500.000, 250.000 y así hasta 1. El número de mitades que caben es log₂(n), que para un millón es algo menos de 20. No hay bloques ni se saltan posiciones: la lista entera sigue siendo candidata hasta que se descarta.
:::

:::quiz
p: Dentro de un bucle que recorre 10.000 elementos ejecutas `if x in lista` sobre esa misma lista. ¿Qué complejidad tiene el conjunto?
o: Θ(n), porque solo hay un bucle
o: Θ(n²), porque cada pertenencia recorre la lista entera
o: Θ(log n), porque la lista está ordenada
a: 2
e: El bucle exterior hace n iteraciones y cada `in` sobre una lista hace hasta n comparaciones, así que se multiplican: n². Con un `set` la pertenencia es O(1) de media y el conjunto vuelve a ser Θ(n). Que la lista esté ordenada no sirve: `in` no usa búsqueda binaria.
:::

:::trampa
Medir con `time.perf_counter` para decidir qué algoritmo es mejor lleva a conclusiones falsas
con entradas pequeñas: ahí manda la constante del lenguaje y lo que tarde en calentarse la caché.
Compara primero de forma asintótica y usa el cronómetro solo para comprobar el orden de magnitud
con el tamaño de datos que vas a tener de verdad.
:::
