---
id: algoritmos-de-streaming
titulo: Algoritmos de streaming
fase: 10
nivel: experto
rutas: [alg, de]
prerequisitos: [aleatoriedad-y-muestreo, tablas-hash, complejidad-asintotica]
tags: [streaming, probabilistico, memoria, estimacion]
resumen: Muestrear, contar y resumir un flujo que no cabe en memoria y que solo pasa una vez, con estructuras cuyo error está acotado por contrato.
fuentes: ["Vitter (1985), 'Random Sampling with a Reservoir'", "Cormode y Muthukrishnan (2005), 'An Improved Data Stream Summary: The Count-Min Sketch and its Applications'", "Flajolet, Fusy, Gandouet y Meunier (2007), 'HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm'"]
---

## En una frase

Un algoritmo de streaming procesa cada elemento **una sola vez**, en el orden en que llega y con
una memoria que no depende del número de elementos, y a cambio devuelve una estimación con un
error que puedes acotar de antemano.

## La idea

Guardar el flujo no es una opción. Diez mil millones de eventos de 100 bytes son un terabyte, y
aunque tuvieras el disco, la pregunta «¿cuántos usuarios distintos he visto hoy?» exige un
`COUNT(DISTINCT)` que no cabe en memoria. Los algoritmos de streaming responden a ese tipo de
preguntas gastando kilobytes.

Todos siguen la misma filosofía: **cambiar exactitud por espacio**, pero con una garantía
matemática, no con una aproximación de andar por casa. La garantía tiene siempre la misma forma:
«el resultado se desvía del verdadero como mucho en `ε` con probabilidad al menos `1 − δ`»,
donde `ε` es el error relativo que toleras y `δ` la probabilidad de pasarte. Tú eliges esos dos
números, y ellos determinan el tamaño de la estructura.

Las cuatro preguntas que resuelven las estructuras de este tema:

- **¿Qué frecuencias tienen los elementos?** El **count-min sketch** da una cota superior de la
  frecuencia real de cada clave con memoria fija.
- **¿Cuántos elementos distintos hay?** **HyperLogLog** estima la cardinalidad de un conjunto con
  un error del orden del 1 % usando unos pocos kilobytes.
- **¿Cuál es el percentil 99 de la latencia?** Los **sketches de cuantiles** (t-digest, GK)
  mantienen un resumen de la distribución con error relativo acotado.
- **¿Puedo tener una muestra uniforme del flujo?** El **reservoir sampling** guarda `k`
  elementos y garantiza que en todo momento son una muestra uniforme de los que han pasado.

Dos avisos que separan a quien ha leído el tema de quien lo ha usado en producción. El primero:
la mayoría de estos algoritmos **solo estiman**; no puedes pedirles que listen los elementos
vistos, porque no los guardan. El segundo: el error del count-min sketch crece con el **total**
de elementos procesados, no con la frecuencia de la clave que consultas; en un flujo que nunca
termina hay que introducir olvido (ventanas o decaimiento exponencial) o la estructura acaba
siendo inútil.

## Definición formal

**Reservoir sampling (algoritmo R de Vitter).** Se mantiene un array `R` de `k` huecos. Para el
elemento número `i` del flujo (con `i` empezando en 1):

- Si `i ≤ k`, se guarda en el hueco `i − 1`.
- Si `i > k`, se sortea un entero `j` uniforme en `{0, …, i − 1}`; si `j < k`, se sustituye
  `R[j]` por el elemento nuevo, y si no, se descarta.

Al terminar, cada uno de los `n` elementos que han pasado está en `R` con probabilidad
exactamente `k / n`. La prueba es por inducción: cuando llega el elemento `i`, cada hueco ya
ocupado lo está con probabilidad `k / (i − 1)`, y la probabilidad de que el nuevo lo reemplace
es `k / i` repartida entre los `k` huecos, así que la probabilidad de supervivencia es
`k/(i−1) · (1 − 1/i) = k/i`. **La probabilidad es `k / i`, no `k / n`**: usar `k / n` con el
total final, que además no conoces hasta el final, sesga la muestra hacia los primeros
elementos.

**Count-min sketch.** Una matriz de `d` filas y `w` columnas de contadores, con una función hash
distinta por fila. Para contar la clave `x`, se incrementan las `d` celdas `(fila, h_fila(x))`.
La estimación es el **mínimo** de esas `d` celdas:

:::formula
est(x) = min sobre f = 1…d de contador[f][h_f(x)]
:::

- `a(x)` — frecuencia real de `x` en el flujo.
- `N` — número total de elementos procesados hasta ahora.
- `ε` — error relativo máximo que toleras, en fracción de `N`.
- `δ` — probabilidad de superar ese error.

Con `w = ⌈e/ε⌉` y `d = ⌈ln(1/δ)⌉` columnas y filas, se cumple
`a(x) ≤ est(x) ≤ a(x) + ε·N` con probabilidad al menos `1 − δ`. Las colisiones solo pueden
**sumar**, nunca restar: la estimación es siempre una cota superior. `e` es la base de los
logaritmos naturales. Nótese que el error absoluto es `ε·N`, proporcional al flujo total: por eso
un count-min sin ventana empeora sin remedio con el tiempo.

**HyperLogLog.** Se usan `m = 2^b` registros, cada uno de `b` bits de índice. Para cada elemento
se calcula un hash; con sus primeros `b` bits se elige el registro y con el resto se cuenta
`ρ`, el número de ceros iniciales. El registro guarda el máximo `M[j]` de los `ρ` que le han
tocado. La estimación de la cardinalidad es:

:::formula
E ≈ α_m · m² / Σⱼ 2^(−M[j])
:::

donde `α_m` es una constante de corrección (`α_m ≈ 0,7213 / (1 + 1,079/m)` para `m` grande) y
`Σⱼ` suma sobre los `m` registros. El error típico relativo es aproximadamente
`1,04 / √m`. Despejando: para un error del 1 % hacen falta `m ≈ (1,04 / 0,01)² ≈ 10.816`
registros, unos 8 kB. Compara eso con guardar los 1.000 millones de identificadores.

**Sketches de cuantiles.** Mantienen una lista comprimida de intervalos cuyo número crece como
`O((1/ε) · log(ε·N))` y garantizan que el cuantil devuelto no se desvía más de `ε·N` posiciones
del verdadero. Un `p99` exacto exige ordenar; con `ε = 0,001` y mil millones de eventos, el
resumen ocupa unos pocos miles de intervalos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `a(x)` | Frecuencia real de la clave `x` en el flujo | apariciones | Crece lo que crezca el flujo; no se puede consultar sin guardar la clave |
| `N` | Total de elementos procesados | elementos | El error absoluto del count-min sube con él (`ε·N`), aunque la clave que consultas no haya crecido |
| `ε` | Error relativo máximo tolerado en el count-min | fracción de `N` | Más tolerancia, menos columnas: `w = ⌈e/ε⌉` |
| `δ` | Probabilidad de superar ese error | probabilidad | Más exigencia, más filas: `d = ⌈ln(1/δ)⌉` |
| `w`, `d` | Columnas y filas del count-min | celdas | Más celdas, menos colisiones y menos error, a cambio de memoria |
| `m` | Registros de HyperLogLog (`m = 2^b`) | registros | El error típico baja como `1,04/√m`: para la mitad de error hacen falta cuatro veces más registros |
| `k` | Huecos del reservoir | elementos | Más huecos, muestra más grande y menos varianza, pero nunca más de lo que cabe en memoria |
:::

:::figura
fichero: algoritmos-de-streaming-countmin-y-hll
pie: A la izquierda, la frecuencia de una clave pesada a lo largo de un flujo de 50.000 elementos: la línea negra es el recuento exacto y las otras dos son las estimaciones de un count-min sketch con 256 y con 4.096 columnas. Fíjate en dos cosas: ninguna estimación baja del valor real (las colisiones solo pueden sumar) y el hueco entre la estimación pequeña y el valor real se ensancha a medida que pasa el flujo, aunque la clave no crezca más rápido. A la derecha, el error relativo de HyperLogLog frente al número de registros, en escala doble logarítmica: los puntos medidos siguen la pendiente de la teoría, 1,04/√m, así que cada vez que cuadruplicas los registros el error se reduce a la mitad. Con 65.536 registros, algo más de 8 kB, el error medido baja al entorno del medio por ciento.
fuente: figuras/algoritmos-de-streaming-1.py
:::

## Ejemplo

**Reservoir.** Flujo de los enteros del 1 al 500, `k = 10`. Cada elemento debe acabar en la
muestra con probabilidad `10 / 500 = 0,02`, es decir un 2 %. Repitiendo el experimento 1.000
veces con semilla fija, las frecuencias observadas de cada entero van del 0,8 % al 3,5 %, con
media 2,0 %. Las variaciones son ruido binomial: con 1.000 repeticiones, el error típico de una
probabilidad del 2 % es `√(0,02 · 0,98 / 1000) ≈ 0,0044`, algo más de cuatro décimas.

**Count-min.** Matriz de 4 filas por 64 columnas, 256 contadores en total. Se insertan las
claves `b` 300 veces, `a` 50 veces y `c` 7 veces, y después 1.000 claves de ruido distintas.
Las estimaciones salen 323, 64 y 19 frente a los valores reales 300, 50 y 7. Fíjate en dos
cosas: las tres estimaciones son mayores o iguales que el valor real (nunca menores), y el
error absoluto es parecido en las tres, en torno a 12-20, porque proviene de las colisiones con
las claves de ruido y no de la frecuencia de la clave consultada.

**HyperLogLog.** Con `m = 10.816` registros el error típico es del 1 %. Si el flujo tiene
1.000 millones de identificadores distintos, guardarlos como enteros de 8 bytes son 8 GB; el
resumen son 8 kB. Seis órdenes de magnitud a cambio de un 1 % de error.

## Código

```python verificable
import numpy as np


def reservoir(flujo, k, rng):
    """Devuelve una muestra uniforme de k elementos viendo el flujo una sola vez."""
    muestra = []
    for i, elemento in enumerate(flujo, start=1):
        if i <= k:
            muestra.append(elemento)
        else:
            j = rng.integers(0, i)        # entero uniforme en [0, i)
            if j < k:
                muestra[j] = elemento     # k / i, nunca k / n
    return muestra


rng = np.random.default_rng(0)
k, n, repeticiones = 10, 500, 1000
veces = np.zeros(n, dtype=int)
for _ in range(repeticiones):
    for elemento in reservoir(range(n), k, rng):
        veces[elemento] += 1

frecuencia = veces / repeticiones
print("probabilidad esperada: {:.3f}".format(k / n))    # -> 0.020
print("minima observada: {:.3f}".format(frecuencia.min()))   # -> 0.008
print("maxima observada: {:.3f}".format(frecuencia.max()))   # -> 0.035
print("media observada:  {:.3f}".format(frecuencia.mean()))  # -> 0.020
```

:::claves
- `rng` se pasa como argumento a `reservoir` y se va consumiendo dentro: el generador avanza con cada sorteo, así que llamar dos veces a la función con el mismo `rng` da muestras **distintas**. Si dentro de la función hicieras `np.random.default_rng(0)`, las 1.000 repeticiones devolverían la misma muestra y las frecuencias saldrían todas 0 o 1.
- `veces[elemento] += 1` funciona porque `veces` es un `np.array` de enteros: el indexado devuelve una vista y el `+=` escribe en el array. Sobre una lista de Python también funciona, pero sobre una **tupla** daría error de tipo.
- La rama `if j < k` es la que decide si el elemento nuevo sustituye a uno de los que ya estaban. La comparación es `< k`, no `<= k`: con `<=` el hueco `k` no existe y saldría un `IndexError`.
- `frecuencia.min()` y `.max()` de las 500 probabilidades son valores extremos de 1.000 repeticiones, no la probabilidad real: con `k/n = 0,02` y 1.000 repeticiones el error típico es de unas cuatro milésimas, así que ver un 0,8 % o un 3,5 % es ruido esperado, no un fallo.
- En el count-min, `mult` y `suma` se guardan como **listas de `int` de Python**, no como arrays de NumPy. La razón es que `mult[fila] * h` con `h` de 64 bits desbordaría un entero de 64 bits; el `int` de Python crece sin límite y el módulo `% w` sale exacto.
- `estimar` recorre una **expresión generadora** dentro de `min(...)`, sin corchetes: no construye la lista de las `d` celdas, las va calculando. Con `min([...])` el resultado es el mismo y se reserva memoria para nada.
:::

```python verificable
import hashlib
import numpy as np

# Count-min sketch: 4 filas x 64 columnas. Solo puede sobreestimar.
d, w = 4, 64
rng = np.random.default_rng(7)
mult = rng.integers(1, 10**6, size=d).tolist()   # listas de int de Python: sin desbordar
suma = rng.integers(0, 10**6, size=d).tolist()
tabla = np.zeros((d, w), dtype=int)


def _hash(clave):
    return int.from_bytes(hashlib.blake2b(clave.encode(), digest_size=8).digest(), "big")


def anadir(clave, veces=1):
    h = _hash(clave)
    for fila in range(d):
        tabla[fila, (mult[fila] * h + suma[fila]) % w] += veces


def estimar(clave):
    h = _hash(clave)
    return min(tabla[fila, (mult[fila] * h + suma[fila]) % w] for fila in range(d))


for clave, veces in [("a", 50), ("b", 300), ("c", 7)]:
    anadir(clave, veces)
for i in range(1000):
    anadir("ruido-{}".format(i))          # otras claves del flujo, colisionan

print("real b=300  estimado b={}".format(estimar("b")))   # -> 323
print("real c=7    estimado c={}".format(estimar("c")))   # -> 19
print("real a=50   estimado a={}".format(estimar("a")))   # -> 64
print("contadores usados: {}".format(d * w))              # -> 256
```

```sql ilustrativo
-- En un motor de flujo el resumen vive dentro de la ventana: al cerrarla se emite
-- el resultado y el estado se descarta. Sintaxis de Flink SQL.
SELECT
    ventana_ini,
    COUNT(DISTINCT usuario_id) AS usuarios,     -- cardinalidad aproximada
    APPROX_COUNT_DISTINCT(usuario_id) AS usuarios_aprox,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latencia_ms) AS p99
FROM TABLE(TUMBLE(TABLE eventos, DESCRIPTOR(ts_evento), INTERVAL '5' MINUTE))
GROUP BY ventana_ini;
```

## Errores típicos

- **Usar `k / n` en lugar de `k / i` en el reservoir.** Es el fallo canónico: el total `n` no se
  conoce hasta el final y, si se usa, la muestra queda sesgada hacia los primeros elementos del
  flujo. La probabilidad correcta de reemplazo en el paso `i` es `k / i`.
- **Suponer que el count-min sketch puede quedarse corto.** Nunca subestima: los contadores solo
  reciben incrementos y las colisiones solo suman. Si obtienes un valor menor que el verdadero,
  tienes un error de implementación (por ejemplo, contar con la clave equivocada o reiniciar la
  matriz a mitad del flujo).
- **Ignorar que el error del count-min crece con el flujo.** La cota es `ε·N` y `N` no para de
  crecer. Un sketch que funcionaba bien con un millón de eventos da estimaciones inútiles con
  mil millones. La solución es ventanas deslizantes o decaimiento exponencial de los contadores.
- **Usar HyperLogLog con cardinalidades pequeñas sin corregir.** Con pocos elementos distintos
  la fórmula cruda es sesgada. Las implementaciones serias aplican **linear counting** por
  debajo de un umbral (`E < 2,5·m`) y corrigen el sesgo por encima. Si escribes el tuyo, copia
  esas correcciones o mide el sesgo antes de fiarte.
- **Aplicar medias y varianzas globales a un flujo no estacionario.** Un promedio acumulado desde
  el principio del tiempo mezcla regímenes distintos y describe a nadie. En flujos reales la
  pregunta correcta es sobre una ventana: última hora, últimos 5 minutos, con decaimiento.
- **Confundir tiempo de evento con tiempo de proceso.** Un evento ocurrido a las 10:00 puede
  llegar a las 10:07 por un reintento. Si agregas por hora de llegada, los totales de cada
  ventana se mueven según la red, no según la realidad. Necesitas **marcas de agua**
  (watermarks) que decidan cuándo una ventana está completa; el tema está en
  [[streaming-tiempo-real]].

:::practica
enunciado: Quieres un count-min sketch con error relativo ε = 0,001 sobre un flujo de N = 2.000.000 de elementos y una probabilidad de fallo δ = 0,05. Calcula las columnas w, las filas d y el número total de contadores, y di cuánto vale la cota de error absoluto.
pista: w = ⌈e/ε⌉ y d = ⌈ln(1/δ)⌉; el error absoluto es ε·N, no ε por la frecuencia de la clave.
solucion: w = ⌈2,71828/0,001⌉ = 2.719 y d = ⌈ln(1/0,05)⌉ = ⌈2,996⌉ = 3. Contadores: 2.719 · 3 = 8.157, unos 32 kB con enteros de 4 bytes. La cota es ε·N = 0,001 · 2.000.000 = 2.000: la estimación nunca se queda corta y puede pasarse en hasta 2.000 con probabilidad del 5 %.
:::

## Comprueba que lo sabes

:::quiz
p: En un reservoir sampling con k = 10 sobre un flujo de 500 elementos, ¿con qué probabilidad acaba un elemento concreto en la muestra?
o: Con probabilidad 10/500 = 2 %, sea cual sea el momento en que llega
o: Con probabilidad 10/500 solo si es de los primeros, y menor si llega tarde
o: Con probabilidad 1/500, porque solo hay un hueco libre
a: 1
e: El algoritmo R garantiza uniformidad: cada elemento del flujo acaba en la muestra con probabilidad k/n, independientemente de su posición. La probabilidad de reemplazo en el paso i es k/i, que decrece, pero la probabilidad acumulada de supervivencia hasta el final es exactamente k/n para todos.
:::

:::quiz
p: Tu count-min sketch estima 323 para una clave cuya frecuencia real es 300. ¿Qué conclusión es correcta?
o: Hay un error de implementación: el sketch debería dar exactamente 300
o: Es normal: las colisiones con otras claves solo suman, así que la estimación es una cota superior
o: El sketch ha perdido datos y hay que reconstruirlo con más columnas
a: 2
e: Todos los incrementos van a contadores compartidos, así que las claves ajenas pueden inflar la celda. El mínimo sobre las filas reduce ese ruido, pero nunca lo elimina del todo. Lo que sí sería un fallo es obtener menos de 300.
:::

:::aviso
Estos algoritmos estiman; no listan. Un HyperLogLog te dice que hay 4,1 millones de usuarios
distintos, pero no puede decirte cuáles. Si además de contar necesitas enumerar, hace falta
otra estructura (un índice, un muestreo aparte o una tabla de agregados), y su coste es
justamente lo que el sketch evitaba.
:::
