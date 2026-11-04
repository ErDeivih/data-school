---
id: medidas-de-dispersion
titulo: Medidas de dispersión
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [medidas-de-centralidad, notacion-matematica]
tags: [estadistica, descriptiva, dispersion, varianza]
resumen: Rango, IQR, varianza, desviación típica y coeficiente de variación miden cuánto se alejan los datos; sin ellos, una media no describe nada.
fuentes: ["Fisher (1925), 'Statistical Methods for Research Workers'"]
---

## En una frase

La dispersión mide cuánto se alejan los datos de su centro: sin ella, «media 50» describe igual
a un grupo en el que todos sacan 50 que a otro en el que la mitad saca 10 y la mitad 90.

## La idea

Reparte 250.000 euros entre cinco personas de dos maneras. En la primera, cada una recibe
50.000. En la segunda, una recibe 250.000 y las otras cuatro nada. La media es idéntica (50.000
euros) y los dos repartos no se parecen en nada. Cualquier resumen que solo dé la media está
escondiendo la única información que importa.

La **desviación típica** es la respuesta más usada: cuánto se separa, por término medio, un dato
de la media. Se mide en las mismas unidades que los datos, así que una desviación de 3 kg se
entiende; la **varianza** es su cuadrado y se mide en kg², y por eso no se compara nunca con una
media ni con un rango. El **rango** (máximo menos mínimo) es la medida más barata y la peor: la
deciden dos observaciones, así que un solo error de medición lo destroza y siempre crece al
añadir datos. El **IQR** solo mira el 50 % central y por eso aguanta los valores extremos
([[cuantiles-y-percentiles]]). La **desviación absoluta mediana** (MAD) es el IQR llevado al
extremo: la mediana de las distancias a la mediana.

:::figura
fichero: dispersion-misma-media-dos-equipos
pie: Arriba, los dos equipos: los dos tienen media 50 y no hay forma de distinguirlos con ella, pero en el B el rango es de 80 horas y en el A de 4. Abajo, la misma información como desviaciones respecto a la media: las rayas del equipo B miden 31,62 y las del A 1,58, veinte veces menos en términos relativos (63,2 % frente a 3,2 % de coeficiente de variación). La media sola esconde la única información que importa.
fuente: figuras/medidas-de-dispersion-1.py
:::

Ninguna medida de dispersión dice nada sobre la **forma**. Dos conjuntos pueden tener la misma
media y la misma desviación típica y ser opuestos: dos valores extremos frente a dos grupos
separados. Y con distribuciones muy asimétricas, «media ± 2 desviaciones» sugiere un rango que
no existe ([[asimetria-y-curtosis]]). La regla práctica: con datos limpios y razonablemente
simétricos, media y desviación típica; con colas largas o valores extremos, mediana e IQR.

Para comparar la dispersión de cosas medidas en escalas distintas está el **coeficiente de
variación**, que es la desviación típica dividida entre la media. Al dividir, las unidades se
cancelan y queda un número adimensional: 0,03 o 3 %. Es la forma de decir «esta máquina es
mucho más regular que aquella» aunque una mida milisegundos y la otra euros.

## Definición formal

Con `n` observaciones `x₁, x₂, …, xₙ` y su media muestral `x̄`:

- **Rango:** `R = máx(x) − mín(x)`.
- **Rango intercuartílico:** `IQR = Q(0,75) − Q(0,25)`, con `Q` los cuartiles.
- **Varianza muestral:** `s² = (1/(n − 1)) · Σᵢ (xᵢ − x̄)²`.
- **Varianza poblacional:** `σ² = (1/N) · Σᵢ (xᵢ − μ)²`.
- **Desviación típica muestral:** `s = √(s²)`.
- **Coeficiente de variación:** `CV = s / x̄`.
- **Desviación absoluta mediana:** `MAD = mediana( /xᵢ − mediana(x)/ )`, donde `/·/` es el valor
  absoluto.

Símbolos: `n` es el tamaño de la muestra; `N` el de la población; `x̄` la media muestral; `μ` la
media poblacional; `Σᵢ` la suma sobre todas las observaciones; `Q(0,25)` y `Q(0,75)` el primer y
el tercer cuartil; `√` la raíz cuadrada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Tamaño de la muestra | ninguna (recuento) | Al subir, el divisor `n − 1` deja de importar: con `n = 5` la corrección añade un 25 % a la varianza, con `n = 200` un 0,5 %. El rango, en cambio, siempre crece o se queda igual al añadir datos |
| `xᵢ` | Cada valor observado | las de la variable | Un solo valor extremo dispara `R`, `s²` y `s`, y apenas mueve el IQR y el MAD. Sumar una constante a todos los `xᵢ` no cambia ninguna de estas medidas |
| `x̄` | Media muestral de los datos | las de la variable | Es el centro del que se miden las distancias y el divisor del CV. Si se acerca a cero, el CV se dispara y deja de significar nada: por eso no se usa con temperaturas en grados Celsius |
| `s²` | Varianza muestral: media de las distancias al cuadrado, con `n − 1` | las de la variable **al cuadrado** (kg², ms²) | Al subir, los datos se alejan más del centro, pero el número no es comparable con la media ni con el rango: está en otra escala. Multiplicar los datos por `c` la multiplica por `c²` |
| `s` | Desviación típica muestral, `√(s²)` | las de la variable (kg, ms) | Es la varianza ya en unidades legibles. Se interpreta como «cuánto se aparta un dato típico». Las desviaciones **no** se suman: la de `X + Y` independientes es `√(σ₁² + σ₂²)`, no `σ₁ + σ₂` |
| `σ²`, `μ` | Varianza y media **poblacionales**, con `N` y no con `n − 1` | las mismas que `s²` y `x̄` | Son el valor de referencia que `s²` intenta estimar. Dividir entre `N` en lugar de `n − 1` sesga el resultado hacia abajo, y con pocos datos el error es grande |
| `CV` | Coeficiente de variación, `s / x̄` | adimensional (tanto por uno o %) | Al subir, hay más dispersión **relativa**: dos conjuntos con la misma `s` pero medias distintas pueden tener CVs muy distintos. Pierde todo el sentido si `x̄` está cerca de cero o si la escala no tiene cero absoluto |
| `IQR` | Anchura del 50 % central, `Q(0,75) − Q(0,25)` | las de la variable | Al subir, el centro de los datos está más repartido. Es la medida que no se inmuta cuando un valor extremo se dispara, y por eso se usa con colas largas |
| `MAD` | Mediana de las distancias a la mediana | las de la variable | Al subir, los datos se alejan del centro igual que con `s`, pero sin que un valor extremo la infle. Para compararla con `s` en datos normales se multiplica por 1,4826 |
| `k` | Número de desviaciones típicas en la desigualdad de Chebyshev | número puro, mayor que 1 | Al subir `k`, la garantía `1 − 1/k²` se acerca a 1: con `k = 2` cubre al menos el 75 %, con `k = 4` al menos el 93,75 %. Es un suelo válido para cualquier distribución, pero muy flojo comparado con el 95 % de la normal |
:::

**Por qué se divide entre `n − 1` y no entre `n`.** La media `x̄` se calcula con los mismos datos,
así que las desviaciones tienden a quedarse cortas: los datos están, por construcción, más cerca
de su propia media que de la media verdadera. Dividir entre `n − 1` (corrección de Bessel) hace
que el valor esperado de `s²` sea exactamente `σ²`. Con `n` grande la diferencia es despreciable;
con `n = 5` es de un 25 % y se nota.

Propiedades que conviene tener a mano:

- `s ≥ 0`, y `s = 0` solo si todos los valores son iguales.
- Sumar una constante a todos los datos no cambia ninguna medida de dispersión. Multiplicar por
  `c` multiplica el rango, el IQR y `s` por `c`, y la varianza por `c²`. El CV no cambia.
- Para variables **independientes**, las varianzas se suman: `σ²(X + Y) = σ²(X) + σ²(Y)`. Las
  desviaciones típicas **no** se suman: `σ(X + Y) = √(σ²(X) + σ²(Y))`.
- **Desigualdad de Chebyshev**, válida para cualquier distribución con varianza finita: al menos
  una fracción `1 − 1/k²` de los datos está a menos de `k` desviaciones típicas de la media. Con
  `k = 2`, al menos el 75 %.

:::formula
s² = (1/(n − 1)) · Σᵢ (xᵢ − x̄)²      s = √(s²)      CV = s / x̄
:::

## Ejemplo

Dos equipos de cinco personas con la misma media y comportamientos opuestos. Puntuaciones de
horas de conexión semanales:

```text
Equipo A:  48  49  50  51  52
Equipo B:  10  30  50  70  90
```

| Medida | Equipo A | Equipo B |
| --- | --- | --- |
| Media | 50 | 50 |
| Rango | 4 | 80 |
| IQR | 2 | 40 |
| Varianza muestral | 2,5 | 1.000 |
| Desviación típica | 1,58 | 31,62 |
| Coeficiente de variación | 3,2 % | 63,2 % |
| MAD | 1 | 20 |

La media es la misma y no hay forma de distinguir los equipos con ella. El equipo A es un grupo
homogéneo; el B tiene a alguien que casi no se conecta y a alguien que se conecta el doble que la
mediana. El coeficiente de variación deja la diferencia en un número comparable: el B es veinte
veces más disperso en términos relativos.

Dos conjuntos con **la misma media y la misma desviación típica** y formas opuestas:

```text
Dos extremos:  -1        1
Dos grupos:    -1,2247  -1,2247   1,2247   1,2247
```

Ambos tienen media 0 y `s = 1,4142`. El primero son dos valores opuestos; el segundo son dos
grupos separados sin ningún valor central. Con la media y la desviación no se distinguen, y
tampoco ayuda el IQR (1,0 en el primero y 2,45 en el segundo): hace falta mirar la forma o el
gráfico.

## Código

```python verificable
import numpy as np
from scipy import stats

equipo_a = np.array([48, 49, 50, 51, 52], dtype=float)
equipo_b = np.array([10, 30, 50, 70, 90], dtype=float)

# La misma media en los dos equipos: sin dispersion serian indistinguibles
print("media   ", equipo_a.mean(), equipo_b.mean())                     # -> 50.0 50.0
print("rango   ", equipo_a.max() - equipo_a.min(),
      equipo_b.max() - equipo_b.min())                                  # -> 4.0 80.0
print("sd      ", round(float(equipo_a.std(ddof=1)), 2),
      round(float(equipo_b.std(ddof=1)), 2))                            # -> 1.58 31.62
print("varianza", equipo_a.var(ddof=1), equipo_b.var(ddof=1))           # -> 2.5 1000.0
print("CV %    ", round(100 * float(equipo_a.std(ddof=1) / equipo_a.mean()), 1),
      round(100 * float(equipo_b.std(ddof=1) / equipo_b.mean()), 1))    # -> 3.2 63.2
print("MAD     ", stats.median_abs_deviation(equipo_a),
      stats.median_abs_deviation(equipo_b))                             # -> 1.0 20.0
```

:::claves
- `equipo_a.std(ddof=1)` es un método del array y devuelve un `float`, pero **NumPy usa `ddof=0` por defecto** y `pandas` usa `1`. Esa es la razón de que la misma columna dé 1,58 en pandas y 1,4142 en NumPy sin `ddof`: no es un error de cálculo, son dos convenciones.
- `dtype=float` en el `np.array` no es cosmético. Con enteros, `var()` todavía devuelve decimales, pero cualquier división entera en el camino se trunca en silencio y te enteras tarde.
- `stats.median_abs_deviation` tiene `scale=1.0` por defecto y **no** aplica el factor 1,4826. Para que sea comparable con `std(ddof=1)` en datos normales hay que pedir `scale="normal"`; si no, sale siempre más pequeño.
- `equipo_a.max() - equipo_a.min()` es el rango, y como método devuelve un número suelto. Ni `max()` ni `min()` modifican el array; en cambio `np.sort` devuelve una copia ordenada y `array.sort()` ordena en el sitio.
- El bloque siguiente muestra el detalle que muerde: `muestras.var(axis=1, ddof=0)` calcula la varianza **de cada fila** porque `axis=1` recorre las columnas. Con `axis=0` repartiría las 200.000 muestras por columnas y el resultado sería el mismo número cinco veces.
- `round(float(x), 2)` convierte primero a `float` de Python: si no, `round` sobre un `np.float64` funciona, pero al imprimirlo junto a otros números la alineación de las columnas se descuadra.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
# 200.000 muestras de 5 valores de una normal con varianza real 4
muestras = rng.normal(loc=10.0, scale=2.0, size=(200_000, 5))

# Con ddof=0 dividimos entre n y la varianza sale sistematicamente baja:
# la varianza real de la normal es 4, asi que falta un 20 %
print(f"media con n   {muestras.var(axis=1, ddof=0).mean():.1f}")   # -> 3.2
print(f"media con n-1 {muestras.var(axis=1, ddof=1).mean():.1f}")   # -> 4.0
```

```python verificable
import numpy as np

# Misma media y misma desviacion tipica, dos formas distintas
dos_extremos = np.array([-1.0, 1.0])
dos_grupos = np.array([-1.224744871391589, -1.224744871391589,
                       1.224744871391589, 1.224744871391589])

print("media", round(float(dos_extremos.mean()), 4),
      round(float(dos_grupos.mean()), 4))                            # -> 0.0 0.0
print("sd   ", round(float(dos_extremos.std(ddof=1)), 4),
      round(float(dos_grupos.std(ddof=1)), 4))                       # -> 1.4142 1.4142
print("IQR  ", round(float(np.percentile(dos_extremos, 75) - np.percentile(dos_extremos, 25)), 4),
      round(float(np.percentile(dos_grupos, 75) - np.percentile(dos_grupos, 25)), 4))  # -> 1.0 2.4495
```

## Errores típicos

- **Usar el rango como medida de dispersión.** Lo fijan dos observaciones, crece siempre al
  añadir datos y un solo error de captura lo dispara. Sirve para describir un conjunto de tres
  números, no un dataset.
- **Comparar desviaciones típicas en unidades distintas sin el coeficiente de variación.** Una
  desviación de 2 kg y otra de 3 libras no se comparan a ojo: 3 libras son 1,36 kg. El CV quita
  las unidades de en medio.
- **Sumar desviaciones típicas.** La desviación de la suma de dos variables independientes es
  `√(σ₁² + σ₂²)`, no `σ₁ + σ₂`: con 3 y 4 sale 5, no 7. Es el error que hace que la volatilidad
  de una cartera parezca mayor de lo que es ([[construccion-de-carteras]]).
- **Calcular el coeficiente de variación con una media cercana a cero o en una escala sin cero
  absoluto.** El CV de unas temperaturas en grados Celsius cambia al pasarlas a Fahrenheit, que es
  la prueba de que ese número no significa nada.
- **Reportar «media ± desviación típica» con distribuciones muy asimétricas.** «Ingreso medio
  30.000 ± 5.000» sugiere un rango de 25.000 a 35.000 que no existe cuando la media está arrastrada
  por unos pocos sueldos altos. Con colas largas, mediana e IQR.
- **Confundir la desviación típica de los datos con el error típico de la media.** El error típico
  es `s/√n` y baja al crecer la muestra; lo que se encoge al medir más no es la dispersión de los
  datos, sino la incertidumbre sobre su media.

:::aviso
Con una sola observación, `std(ddof=1)` devuelve `nan` (no hay de qué restar) y `pandas` descarta
esa fila en `groupby().std()`. Es una fuente clásica de grupos que desaparecen de un informe sin
que salte ningún error.
:::

:::practica
enunciado: Cinco paquetes pesan 498, 502, 500, 504 y 496 gramos. Calcula la varianza muestral, la desviación típica y el coeficiente de variación, y decide si el proceso cumple la especificación de un CV por debajo del 1 %.
pista: Resta la media a cada valor, eleva al cuadrado y divide la suma entre n − 1; el CV es la desviación dividida entre la media.
solucion: Media = 2.500/5 = 500 g. Desviaciones: −2, 2, 0, 4, −4; cuadrados 4, 4, 0, 16, 16 = 40. s² = 40/4 = 10 g²; s = √10 = 3,16 g. CV = 3,16/500 = 0,0063 = 0,63 %, por debajo del 1 %: el proceso cumple.
:::

## Comprueba que lo sabes

:::quiz
p: Dos grupos tienen la misma media (50) y desviaciones típicas de 1,58 y 31,62. ¿Qué conclusión es correcta?
o: El segundo grupo tiene datos más dispersos; la media no distingue los dos grupos
o: El segundo grupo tiene una media distinta mal calculada
o: El primero tiene más datos porque su desviación es menor
o: Los dos grupos son equivalentes salvo por un valor extremo
a: 1
e: La media solo dice dónde está el centro: no distingue un grupo homogéneo de otro con valores opuestos. La desviación típica añade esa información, y el coeficiente de variación la hace comparable entre escalas distintas. Un valor extremo es una de las causas posibles de dispersión, no la única.
:::

:::quiz
p: ¿Por qué la varianza muestral divide entre n − 1 y no entre n?
o: Porque así el resultado queda siempre mayor y es más conservador
o: Porque las desviaciones respecto a la media muestral son, de media, demasiado pequeñas
o: Porque n − 1 es el número de grados de libertad de la desviación típica
o: Porque la media se calcula con n − 1 valores
a: 2
e: x̄ se estima con los propios datos, así que estos quedan más cerca de su media que de la media real y la suma de cuadrados sale corta. Dividir entre n − 1 corrige ese sesgo y hace que E[s²] = σ². No es una cuestión de grados de libertad «de la desviación», sino del sesgo del estimador.
:::

:::quiz
p: Una estrategia tiene retornos con desviación típica del 4 % y otra del 2 %. ¿Qué falta para poder decir cuál es más arriesgada en términos relativos?
o: Nada, la del 4 % es el doble de arriesgada
o: La media de los retornos, para calcular el coeficiente de variación
o: El número de operaciones, porque la desviación crece con la muestra
o: La curtosis, porque mide el riesgo de cola
a: 2
e: En términos relativos hay que dividir entre la media: un 4 % de desviación sobre un 20 % de rentabilidad es mucho menos relativo que un 2 % sobre un 1 %. La curtosis y el tamaño de muestra matizan el riesgo, pero lo que falta para el CV es la media.
:::
