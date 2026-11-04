---
id: analisis-amortizado
titulo: Análisis amortizado
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [complejidad-asintotica, arrays-y-listas]
tags: [algoritmos, coste, estructuras, rendimiento]
resumen: Repartir el coste de una secuencia entre sus operaciones: por qué añadir al final de una lista sale a O(1) aunque alguna inserción concreta cueste O(n).
fuentes: ["Cormen, Leiserson, Rivest y Stein (2009), 'Introduction to Algorithms', cap. 17", "Tarjan (1985), 'Amortized Computational Complexity'"]
---

## En una frase

El análisis amortizado demuestra que el coste **total** de una secuencia de `m` operaciones
está acotado, aunque algunas operaciones concretas sean carísimas, y de ahí deduce el coste
medio por operación sin suponer nada sobre los datos ni sobre la probabilidad de cada caso.

## La idea

Piensa en una estantería con un solo hueco que vas llenando. Cuando se llena, no compras un
hueco más: compras una estantería del **doble** de tamaño y trasladas todos los libros. La
primera colocación es gratis de traslado, la segunda obliga a mover 1 libro, la tercera 2, la
quinta 4, la novena 8… Colocar 1.024 libros uno a uno mueve 1.023 libros en total, no 1.024 ·
(algo grande). El traslado caro ocurre muy de vez en cuando y, cuando ocurre, la estantería
recién comprada tiene sitio de sobra para rato.

Eso es todo el concepto. Ahora la parte que se malinterpreta: **amortizado no es el caso
medio**. El caso medio promedia sobre una distribución de entradas posibles; el amortizado no
usa ninguna probabilidad, es una garantía sobre la peor secuencia de operaciones que se te
pueda ocurrir. Si alguien encadena las operaciones que más daño hacen, el coste total sigue
estando acotado. Esa es la fuerza del argumento: no depende de la suerte.

Tampoco es un «a veces va rápido y a veces lento, y de media bien». El análisis amortizado
reparte el coste de forma explícita: asigna a cada operación barata un poco más de lo que
realmente cuesta y guarda la diferencia como **crédito** que gastan las operaciones caras. Si
el crédito nunca se queda en negativo, la cuenta cuadra. Hay tres formas estándar de hacer esa
contabilidad y las tres llegan al mismo resultado: el método agregado (sumar todo y dividir),
el método contable (créditos) y el método del potencial (una función del estado).

De ahí salen los costes que usas a diario sin pensarlo: añadir al final de una lista de Python,
insertar en un diccionario, `append` a un `deque` o a un `vector` de C++ son O(1) **amortizado**,
no O(1) en el peor caso. La diferencia importa en tres escenarios concretos:

1. **Sistemas de tiempo real.** Si cada operación tiene un plazo máximo de respuesta, una
   inserción que de pronto copia 10 millones de elementos te hace perder el plazo. Ahí no vale
   el amortizado: hace falta una estructura con peor caso garantizado o un crecimiento
   incremental (copiar un bloque por operación).
2. **Estructuras persistentes.** Cuando cada versión anterior debe seguir siendo consultable,
   una operación amortizada barata puede volverse caro por versión, porque el trabajo que se
   ahorraba en el estado compartido ya no se puede reaprovechar igual.
3. **Cuando el patrón de uso rompe el argumento.** Un array dinámico que se encoge en cuanto
   baja de la mitad del tamaño puede entrar en un ciclo de ampliar y encoger si el uso alterna
   inserción y borrado justo en el umbral. La solución clásica es encoger solo cuando el
   tamaño baja de un cuarto de la capacidad, y así las ampliaciones quedan separadas por
   suficientes operaciones baratas.

## Definición formal

Sean `m` operaciones aplicadas en orden y `cᵢ` el coste real de la operación `i` (medido en
operaciones elementales). Sea `C = c₁ + c₂ + … + c_m` el coste total de la secuencia.

- **Coste amortizado por operación** — un valor `â` tal que existen costes asignados `ĉᵢ` con
  `ĉᵢ ≤ â` para todo `i` y `Σ ĉᵢ ≥ Σ cᵢ`. Si existe, la secuencia entera cuesta como mucho
  `m · â`, aunque alguna `cᵢ` suelta sea mucho mayor.
- **Método agregado** — se acota `C` directamente y se divide: si `C = O(f(m))`, entonces cada
  operación cuesta `O(f(m)/m)` amortizado. Con `C ≤ 2m` sale `â = O(1)`.
- **Método contable** — se cobra a cada operación un importe distinto de su coste real y la
  diferencia se guarda como crédito asociado a un elemento concreto de la estructura. La regla
  de oro: el crédito total nunca puede ser negativo. Las ampliaciones lo consumen.
- **Método del potencial** — se define una función `Φ` sobre los estados de la estructura, con
  `Φ` no negativa y `Φ(estado inicial) = 0`, y se define el coste amortizado de la operación `i`
  como `ĉᵢ = cᵢ + Φ(Sᵢ) − Φ(Sᵢ₋₁)`. Sumando telescópicamente, `Σ ĉᵢ = Σ cᵢ + Φ(S_m) − Φ(S₀) ≥ Σ cᵢ`,
  así que `Σ cᵢ ≤ Σ ĉᵢ`. Para un array dinámico que duplica, `Φ = 2 · tamaño − capacidad` y con
  ese potencial resulta `ĉᵢ ≤ 3` para toda inserción.
- **`tamaño`** — número de elementos guardados. **`capacidad`** — huecos reservados.

Coste real de las primeras inserciones en un array que duplica (copias más la inserción):

| Inserción | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Coste real | 1 | 2 | 3 | 1 | 5 | 1 | 1 | 1 | 9 |

Suma de las nueve: 24. Media: 2,67. Ninguna operación pasa de 9 y sin embargo el **peor** de la
secuencia no crece con `n`: es exactamente el tamaño en el momento de duplicar, y eso solo pasa
en las potencias de 2, separadas cada vez por más operaciones baratas.

:::figura
fichero: amortizado-copias-y-picos
pie: A la izquierda, las copias acumuladas al insertar n elementos, en escala logarítmica. Duplicar la capacidad (azul) suma 262.143 copias para 262.144 inserciones, que es n − 1: una por inserción y ninguna más. Crecer sumando un hueco cada vez (rojo) suma 34.359.607.296 copias, 131.072 veces más, y la recta tiene pendiente 2 porque el total crece con el cuadrado de n. A la derecha, el coste real de cada una de las primeras 40 inserciones: las ampliaciones (en rojo) cuestan 3, 5, 9, 17 y 33, y caen en 2, 4, 8, 16 y 32. Los picos son reales, pero cada vez están más separados: la media de las 40 inserciones es 2,58 y ninguna operación supera la cota amortizada de 3.
fuente: figuras/analisis-amortizado-1.py
:::

## Ejemplo

Insertar 1.024 elementos al final de un array vacío:

- **Duplicando la capacidad:** las copias ocurren en los tamaños 1, 2, 4, …, 512 y suman
  1 + 2 + 4 + … + 512 = 1.023 elementos copiados, que es `n − 1`. El coste real total (copias
  más las 1.024 inserciones) es 2.047, así que cada inserción sale a 2,0 de media. El peor caso
  puntual fue copiar 512 elementos, pero eso ocurrió una sola vez.
- **Creciendo de uno en uno:** las copias suman 0 + 1 + 2 + … + 1.023 = 523.776, y la media por
  inserción es 511,5. Con 100.000 inserciones el crecimiento constante hace 4.999.950.000 copias
  (casi 5.000 millones) frente a 131.071 con duplicación.

La diferencia no está en el lenguaje ni en la máquina: está en la política de crecimiento. Y
tiene una lectura práctica: si ves un bucle que construye una lista con `lista = lista + [x]`,
estás pagando la versión de crecimiento constante, porque cada `+` crea una lista nueva y copia
todo lo anterior.

## Código

```python verificable
# Dos politicas de crecimiento del mismo array: duplicar o sumar un hueco.
def copias_totales(n, politica):
    capacidad, tam, copias = 1, 0, 0
    for _ in range(n):
        if tam == capacidad:                  # no cabe: hay que ampliar
            copias += tam                     # se traslada todo lo guardado
            capacidad = capacidad * 2 if politica == "doble" else capacidad + 1
        tam += 1
    return copias

for n in (8, 16, 32, 1024):
    print(f"n={n:>5}  duplicando {copias_totales(n, 'doble'):>8}  "
          f"sumando uno {copias_totales(n, 'uno'):>8}")

# La comprobacion que importa: con duplicacion las copias son n-1, muy por debajo de 2n
print("copias con n=1024 y duplicacion:", copias_totales(1024, "doble"))   # -> 1023
print("copias con n=100000 y duplicacion:", copias_totales(100000, "doble"))  # -> 131071
```

:::claves
- `capacidad = capacidad * 2 if politica == "doble" else capacidad + 1` es una expresión condicional dentro de una asignación: se evalúa una sola de las dos ramas. Con `n = 1024` la política de duplicar da 1.023 copias; con `n = 100.000` da 131.071, que **no** es `n − 1` (esa igualdad solo vale cuando `n` es una potencia de dos). Elegir el ejemplo en una potencia de dos es lo que hace que la cuenta salga redonda.
- La función devuelve el número de **copias**, no el coste: falta sumar las `n` inserciones. Con 1.024 elementos el coste real es 1.023 + 1.024 = 2.047 y la media por inserción es 2,0, no 1,0.
- `capacidad` empieza en 1 y `tam` en 0, así que la primera inserción **no** copia nada. Si cambiaras `capacidad` a 0, la primera ampliación tendría que copiar una lista vacía y el total de copias bajaría en 1 en todos los casos: el orden de complejidad no cambia, pero los números de la tabla sí.
- El bucle es O(n) porque recorre las inserciones una a una, aunque el número total de copias también sea O(n): son dos cosas distintas. La función que mide el coste no se libra de pagar el coste de medirlo.
- `coste_amortizado` devuelve `(peor, total)` y el código imprime `[0]` y `[1]` por posición. Si cambiaras el `return` para devolver `(total, peor)`, las dos líneas seguirían ejecutándose sin error y con los números cambiados de sitio: en Python nada avisa de que has intercambiado el orden de una tupla.
:::

```python verificable
# Metodo del potencial: Phi = 2*tamano - capacidad. Si el coste asignado
# (copias + insercion + cambio de Phi) no pasa de 3, el total es 3n como mucho.
def coste_amortizado(n):
    capacidad, tam, total, peor = 0, 0, 0, 0
    for _ in range(n):
        phi_antes = 2 * tam - capacidad
        if tam == capacidad:                  # ampliacion: se copia lo que habia
            copias = tam
            capacidad = capacidad * 2 if capacidad else 1
        else:
            copias = 0
        tam += 1
        phi_despues = 2 * tam - capacidad
        asignado = copias + 1 + phi_despues - phi_antes   # +1 por la propia insercion
        total += asignado
        peor = max(peor, asignado)
    return peor, total

print("peor coste amortizado con n=1024:", coste_amortizado(1024)[0])      # -> 3
print("suma de costes con n=1024:", coste_amortizado(1024)[1])             # -> 3071
print("suma de costes con n=100000:", coste_amortizado(100000)[1])         # -> 299999
```

```python ilustrativo
from collections import deque

# Operaciones que SI son O(1) amortizado y operaciones que NO lo son nunca.
lista = list(range(1000000))
lista.append(7)          # O(1) amortizado: si no cabe, se duplica la capacidad
lista.pop()              # O(1)
lista.insert(0, 7)       # O(n) siempre: desplaza el millon de elementos
lista.pop(0)             # O(n) siempre
del lista[500000]        # O(n) siempre

cola = deque(range(1000000))
cola.append(7)           # O(1)
cola.popleft()           # O(1): la cola doblemente enlazada no desplaza nada
cola[500000]             # O(n): el acceso por indice en medio de un deque recorre
```

## Errores típicos

- **Confundir amortizado con caso medio.** El caso medio necesita una distribución de
  probabilidad sobre las entradas; el amortizado no necesita ninguna y vale para la peor
  secuencia. Decir «de media es O(1)» cuando has demostrado un amortizado es perder el
  argumento que tenías.
- **Creer que amortizado O(1) significa que cada operación es O(1).** No lo es: la inserción que
  provoca la ampliación cuesta O(n) de verdad. Si tienes un plazo por operación (tiempo real,
  audio, control), mira el peor caso, no el amortizado.
- **Aplicar el argumento a operaciones que nunca fueron amortizadas.** `insert(0, x)` y
  `pop(0)` sobre una lista son Θ(n) en todas y cada una de las llamadas; no hay crédito que
  repartir porque no hay ninguna operación barata que lo acumule. Usa un `deque` o cambia el
  diseño. Está desarrollado en [[arrays-y-listas]] y en [[pilas-y-colas]].
- **Elegir una política de crecimiento constante.** Ampliar sumando un hueco cada vez convierte
  `n` inserciones en Θ(n²) copias, como muestran los 523.776 traslados de 1.024 elementos.
  Duplicar (o multiplicar por 1,5) es lo que hace que el amortizado sea O(1).
- **Encoger demasiado pronto.** Si reduces la capacidad en cuanto el tamaño baja de la mitad,
  alternar inserción y borrado justo en el umbral provoca una ampliación (y una copia completa)
  en cada operación: el amortizado se va a Θ(n) por operación. Encoge solo cuando el tamaño baje
  de un cuarto de la capacidad, o no encojas.
- **Olvidar que el argumento vale para una secuencia, no para un estado.** En estructuras
  persistentes o con referencias externas (iteradores, punteros a elementos) una ampliación
  invalida el trabajo ahorrado y el reparto deja de cuadrar. Si guardas iteradores mientras
  modificas la estructura, el problema ya no es de coste sino de corrección.

:::practica
enunciado: Insertas 4.096 elementos al final de un array dinámico vacío que duplica su capacidad al llenarse. ¿Cuántos elementos se copian en total, cuál es el coste real sumando copias e inserciones y cuánto sale por inserción? Compáralo con crecer sumando un hueco cada vez.
pista: Las copias ocurren en los tamaños 1, 2, 4, 8… y suman n − 1; con crecimiento constante la suma es 0 + 1 + … + (n − 1).
solucion: Con duplicación las copias son 1 + 2 + 4 + … + 2.048 = 4.095 = n − 1. El coste total es 4.095 + 4.096 = 8.191, unos 2 por inserción: O(1) amortizado. Creciendo de uno en uno las copias son 0 + 1 + … + 4.095 = 8.386.560, una media de 2.047,5 por inserción. Conclusión: la política de crecimiento decide entre Θ(n) y Θ(n²).
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre decir que `append` es O(1) amortizado y decir que es O(1) de media?
o: Ninguna, son dos formas de decir lo mismo con palabras distintas
o: El amortizado es una garantía sobre el peor caso de una secuencia de operaciones; el de media supone una distribución de probabilidad sobre las entradas
o: El amortizado se aplica solo a estructuras persistentes y el de media a las mutables
a: 2
e: El análisis amortizado no usa probabilidad: reparte el coste de las operaciones caras entre las baratas y garantiza una cota para cualquier secuencia. El caso medio, en cambio, promedia sobre una distribución de entradas posibles, que en la práctica casi nunca conoces.
:::

:::quiz
p: Un array dinámico duplica su capacidad cuando se llena. ¿Cuántos elementos se copian en total al insertar 1.024 elementos empezando de cero?
o: 1.023, porque las copias son 1 + 2 + 4 + ... + 512
o: 1.024, uno por inserción
o: 523.776, porque cada inserción copia todo lo anterior
a: 1
e: Las copias solo ocurren al llenarse, en los tamaños potencia de 2: 1, 2, 4, ..., 512, que suman 1.023. La opción de 523.776 es el resultado de crecer un hueco cada vez, con coste cuadrático. Que cada inserción copie todo lo anterior ocurre solo en la política de crecimiento constante.
:::

:::quiz
p: En un sistema que debe responder a cada operación en menos de un milisegundo, ¿basta con saber que una inserción es O(1) amortizado?
o: Sí, porque el coste total está acotado y por tanto cada operación cabe en el plazo
o: No, porque la operación que provoca la ampliación cuesta O(n) y puede superar el plazo
o: Sí, siempre que la capacidad se duplique en vez de sumar un hueco
a: 2
e: El amortizado acota la suma de costes, no el máximo. La inserción que dispara la ampliación copia todos los elementos y es la que rompe el plazo. Para eso hacen falta estructuras con peor caso garantizado o ampliaciones incrementales que copien un bloque por operación.
:::

:::aviso
El coste amortizado describe el coste de una **secuencia**, no el de una operación aislada. Si tu
sistema tiene plazos por operación, mide el peor caso; si solo te importa el total de un proceso
por lotes, el amortizado es la herramienta correcta.
:::
