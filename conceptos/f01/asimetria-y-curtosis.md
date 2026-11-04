---
id: asimetria-y-curtosis
titulo: Asimetría y curtosis
fase: 1
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [medidas-de-centralidad, medidas-de-dispersion]
tags: [estadistica, colas, riesgo, momentos]
resumen: La asimetría dice hacia qué lado se estira la cola y la curtosis cuánto pesan los extremos; son los dos números que delatan que unos datos no son normales.
fuentes: ["Pearson (1895), 'Contributions to the Mathematical Theory of Evolution. II. Skew Variation in Homogeneous Material'", "Mandelbrot (1963), 'The Variation of Certain Speculative Prices'"]
---

## En una frase

La asimetría mide si la cola se estira hacia la derecha o hacia la izquierda, y la curtosis
cuánto peso tienen las colas; la normal tiene cero en las dos, y casi ningún dato del mundo real
también.

## La idea

Tienes dos muestras con la misma media y la misma desviación típica. En la primera, los valores
se reparten de forma más o menos regular a los dos lados del centro. En la segunda, casi todos
los valores están apelotonados cerca de la media y unos pocos se van muy lejos. La media y la
desviación típica no distinguen una de otra; el histograma, sí. La **curtosis** es el número que
resume esa diferencia: cuánto peso hay en las colas (y, como la desviación ya fija la escala, ese
peso se le quita al centro y a los hombros).

La **asimetría** responde a otra pregunta: ¿la cola larga está a la derecha o a la izquierda? Los
salarios, los precios de la vivienda y los tiempos de espera tienen asimetría positiva: muchos
valores bajos y unos pocos altísimos que estiran la media hacia arriba. Los retornos de una
cartera suelen tener asimetría negativa: la mayoría de los días son planos o ligeramente
positivos y unos pocos días de pánico se llevan por delante meses de ganancias. Ese patrón
—mucha calma y sustos concentrados— es exactamente lo que hace que la campana de Gauss no sirva
para describir el riesgo.

Dos consecuencias prácticas. La primera: **los momentos no ven nada que no sea un promedio de
potencias**. Un par de valores extremos manda sobre el tercer y el cuarto momento, así que la
asimetría y la curtosis muestrales son estimadores ruidosos y necesitan bastantes datos. La
segunda: cuando la curtosis es alta, la regla de «media ± 2 desviaciones cubre el 95 %» deja de
ser cierta. Con colas gordas, los sucesos extremos son mucho más frecuentes de lo que predice la
normal, y están precisamente donde duele: en el VaR, en la caída máxima y en cualquier métrica
de riesgo que asuma normalidad.

La curtosis **no** mide lo puntiaguda que es una distribución, aunque se repita hasta la
saciedad. Mide el peso de las colas. Dos distribuciones con la misma curtosis pueden tener picos
completamente distintos.

:::figura
fichero: asimetria-y-curtosis-misma-media-distinta-forma
pie: Arriba, los dos primeros conjuntos estandarizados contra la campana de Gauss de referencia: la normal la sigue casi perfectamente, y en la cola derecha los datos se salen de la curva por el lado derecho mientras la curva ya ha caído a cero. Abajo, las tres muestras enteras: la misma media y la misma desviación, y sin embargo los ingresos llegan a z = +11,2 y los dos días de pánico a z = −14,5. Mientras la curtosis se aleje de cero, «media ± 2 desviaciones» no cubre el 95 % de nada.
fuente: figuras/asimetria-y-curtosis-1.py
:::

## Definición formal

Con `X` una variable aleatoria, `μ = E[X]` su media y `σ` su desviación típica:

:::formula
γ₁ = E[(X − μ)³] / σ³        γ₂ = E[(X − μ)⁴] / σ⁴ − 3
:::

- `E[·]` — esperanza matemática (la media teórica).
- `μ` — media de la distribución; `σ` — su desviación típica.
- `γ₁` — **asimetría** (sesgo). Vale 0 en toda distribución simétrica; positiva si la cola larga
  está a la derecha; negativa si está a la izquierda.
- `γ₂` — **curtosis en exceso**. Vale 0 en la normal, porque se le resta 3. La «curtosis de
  Pearson» (sin restar) vale 3 en la normal; cuidado con la convención que uses.
- El 3 se resta porque la normal tiene `E[(X − μ)⁴]/σ⁴ = 3`: es una simple comodidad para que
  comparar contra la normal sea leer un cero.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `X` | La variable aleatoria que estás describiendo | las de la variable (retornos, salarios) | No es una palanca: es lo que mides. Lo que importa es su forma, no su escala: multiplicar `X` por 100 no cambia ni `γ₁` ni `γ₂` |
| `μ` | Media de la distribución, `E[X]` | las de la variable | Es el centro del que se miden las potencias. Desplazar la variable no cambia la asimetría ni la curtosis: sumar una constante a todos los datos no hace nada a estos dos números |
| `σ` | Desviación típica de la distribución | las de la variable | Es el divisor de las dos fórmulas y la unidad de medida: al subir `σ`, cada desviación pesa menos en unidades típicas. Es lo que hace que `γ₁` y `γ₂` sean adimensionales |
| `E[·]` | Esperanza matemática: el promedio teórico ponderado por la probabilidad | las de lo que haya dentro | No se «sube»: es el operador. La diferencia entre `E[(X − μ)³]` y `(E[X − μ])³` es toda la diferencia entre la asimetría y un cero |
| `γ₁` | Asimetría (sesgo): tercer momento estandarizado | adimensional | Al subir, la cola larga se va a la derecha. Cero en toda distribución simétrica; negativo si la cola tira a la izquierda, como en los retornos con días de pánico |
| `γ₂` | Curtosis **en exceso**: cuarto momento estandarizado menos 3 | adimensional | Al subir, los extremos pesan más que en la normal. Tiene un suelo de −2 (una moneda) y no techo: una cola muy pesada da valores de decenas. Ojo con la convención: la curtosis de Pearson vale 3 en la normal |
| `m_k` | Momento central muestral de orden `k`, `(1/n) · Σᵢ (xᵢ − x̄)^k` | las de la variable elevadas a `k` | Al subir `k`, el momento depende de menos datos y de más extremos: `m₄` lo deciden casi por completo los dos o tres valores más alejados de la media |
| `n` | Número de observaciones de la muestra | ninguna (recuento) | No cambia los valores teóricos, pero sí la fiabilidad: con `n = 20` una asimetría de ±2 aparece por azar, con `n = 2.000` la variación es de unas décimas. Los momentos de orden 3 y 4 necesitan muchos datos |
| `G₁` | Asimetría muestral con corrección de sesgo: `(√(n(n − 1))/(n − 2)) · m₃ / m₂^(3/2)` | adimensional | Es `γ₁` estimada con datos. Con `n` pequeño el factor de corrección se separa de 1 (con `n = 5` multiplica por 1,49; con `n = 100`, por 1,02) y por eso el estimador sin corregir se queda corto en valor absoluto |
| `Q(0,25)`, `Q(0,50)`, `Q(0,75)` | Los cuartiles primero, segundo (la mediana) y tercero | las de la variable | Son la alternativa robusta: el coeficiente de Bowley usa solo estas tres posiciones, está acotado entre −1 y 1 y un solo valor extremo no lo mueve. `γ₁`, en cambio, se lo lleva detrás |
:::

En una muestra de `n` valores, con `m_k = (1/n) · Σᵢ (xᵢ − x̄)^k` el momento central de orden `k`:

:::formula
G₁ = (√(n(n − 1)) / (n − 2)) · m₃ / m₂^(3/2)
:::

Ese factor corrige el sesgo del estimador. `pandas.Series.skew()` y `scipy.stats.skew(bias=False)`
usan esta versión; `scipy.stats.skew` con su opción por defecto devuelve el momento sin corregir,
que con pocos datos es bastante menor en valor absoluto. `pandas.Series.kurt()` y
`scipy.stats.kurtosis(fisher=True)` devuelven curtosis **en exceso**.

Valores teóricos que conviene reconocer:

| Distribución | Asimetría | Curtosis en exceso |
| --- | --- | --- |
| Normal | 0 | 0 |
| Uniforme continua | 0 | −1,2 |
| Bernoulli(0,5) | 0 | −2 |
| Exponencial | 2 | 6 |
| t de Student con ν grados | 0 | 6 / (ν − 4) |

La curtosis en exceso tiene un suelo: **−2**, que alcanza la Bernoulli con probabilidad 0,5 (una
moneda). Es la distribución con las colas más finas posibles. La distribución uniforme se queda
en −1,2 porque no tiene ninguna cola. Los valores positivos indican colas más pesadas que la
normal.

Como alternativa robusta a los momentos está el coeficiente de asimetría de cuartiles de Bowley,
que solo usa posiciones y no potencias:

:::formula
Bowley = (Q(0,75) + Q(0,25) − 2 · Q(0,50)) / (Q(0,75) − Q(0,25))
:::

Está acotado entre −1 y 1 y no se deja arrastrar por un valor extremo, a diferencia de `γ₁`.

## Ejemplo

Tres conjuntos pequeños, con sus números calculados:

```text
Simétrico:   2  3  4  5  6  7  8
Con extremo: 1  1  1  2  2  3  5  9  20
Retornos:    +0,4 % durante 19 días y un día de −8 %
```

Resultados (`scipy`, con la corrección de sesgo):

| Conjunto | n | Media | Desviación | Asimetría | Curtosis en exceso |
| --- | --- | --- | --- | --- | --- |
| Simétrico | 7 | 5,0000 | 2,1602 | 0,0000 | −1,2000 |
| Con extremo | 9 | 4,8889 | 6,2339 | +2,1817 | +4,8761 |
| Retornos | 20 | −0,0002 | 0,0188 | −4,4721 | +20,0000 |

Lectura de cada uno:

- El **simétrico** tiene asimetría 0 (es simétrico) y curtosis −1,2000, exactamente la de una
  uniforme: siete valores equiespaciados no tienen colas. Si te fías del «±2 desviaciones», aquí
  te sobra la regla: ningún valor se aleja más de 3 unidades de la media, que con `s = 2,1602`
  son 1,39 desviaciones.
- El **con extremo** tiene la media en 4,89, por encima de 6 de sus 9 valores. La asimetría es
  +2,18 y la curtosis +4,88: un solo valor de 20 produce las dos cosas.
- Los **retornos** son el caso realista: 19 días casi planos y un día de −8 %. Media
  prácticamente cero, desviación 1,88 % y, sobre todo, asimetría −4,47 y curtosis +20. Una
  distribución normal no produce una curtosis de 20 con 20 datos: ese número es la firma de que
  el riesgo no es simétrico y de que los modelos que asumen normalidad van a infravalorar la
  probabilidad de los días malos ([[metricas-de-riesgo]]).

## Código

```python verificable
import numpy as np
from scipy import stats

simetrico = np.array([2, 3, 4, 5, 6, 7, 8], dtype=float)
con_extremo = np.array([1, 1, 1, 2, 2, 3, 5, 9, 20], dtype=float)
# 19 dias planos y un dia de panico: el patron tipico de los retornos reales
retornos = np.array([0.004] * 19 + [-0.08])

# bias=False aplica la correccion de sesgo: es lo mismo que pandas .skew() y .kurt()
print("simetrico", round(float(stats.skew(simetrico, bias=False)), 4),
      round(float(stats.kurtosis(simetrico, bias=False)), 4))         # -> 0.0 -1.2
print("extremo  ", round(float(stats.skew(con_extremo, bias=False)), 4),
      round(float(stats.kurtosis(con_extremo, bias=False)), 4))       # -> 2.1817 4.8761
print("retornos ", round(float(stats.skew(retornos, bias=False)), 4),
      round(float(stats.kurtosis(retornos, bias=False)), 4))          # -> -4.4721 20.0
```

:::claves
- `stats.skew(x, bias=False)` y `stats.kurtosis(x, bias=False)` son las versiones corregidas (las mismas que `.skew()` y `.kurt()` de pandas). Con `bias=True`, que es el valor por defecto de `scipy.stats`, sale un número más pequeño en valor absoluto: con nueve datos, la diferencia se ve a simple vista.
- `stats.kurtosis` devuelve **curtosis en exceso** (la normal da 0), pero `stats.kurtosis(x, fisher=False)` devuelve la de Pearson (la normal da 3). Confundirlas es el error de lectura más común con este número.
- `np.array([0.004] * 19 + [-0.08])` mezcla una lista de Python con un `float` y sale un array de 20 elementos de tipo `float64`. Si el último valor fuera el entero `-8` en lugar de `-0.08`, el sesgo sería el mismo pero la escala cambiaría por completo: la curtosis es adimensional, así que no se entera, pero la desviación típica sí.
- `bias=False` divide por `n − 1` y aplica el factor `√(n(n − 1))/(n − 2)`. Con `n = 2` ese factor divide entre cero y scipy devuelve `nan` con un aviso; con `n = 3` el resultado existe pero no vale para nada.
- `stats.skew` y `stats.kurtosis` aceptan `nan_policy="omit"`, que descarta los huecos (por defecto un `nan` contamina el resultado y todo sale `nan`). Es cómodo y peligroso a la vez: cada estadístico puede acabar calculado con un número distinto de datos y nadie te avisa.
- El bloque siguiente usa una lista por comprensión con `rng.normal` dentro: dos mil muestras de veinte valores son 40.000 números y el resultado es un array de 2.000 asimetrías. Cada una se calcula con veinte datos, así que la dispersión de esas 2.000 asimetrías es justo lo que no se puede ver con una sola muestra: con `n = 20` la desviación típica del estimador ronda 0,5, y con `n = 200` baja a unas 0,16.
:::

```python verificable
import numpy as np
from scipy import stats

# Con pocos datos, la asimetria muestral de una normal ya se mueve muchisimo
rng = np.random.default_rng(0)

v20 = np.array([stats.skew(rng.normal(size=20), bias=False) for _ in range(2000)])
v200 = np.array([stats.skew(rng.normal(size=200), bias=False) for _ in range(2000)])
v2000 = np.array([stats.skew(rng.normal(size=2000), bias=False) for _ in range(2000)])

print(f"n   20: entre {v20.min():+.2f} y {v20.max():+.2f}")      # -> n   20: entre -2.01 y +2.04
print(f"n  200: entre {v200.min():+.2f} y {v200.max():+.2f}")    # -> n  200: entre -0.58 y +0.59
print(f"n 2000: entre {v2000.min():+.2f} y {v2000.max():+.2f}")  # -> n 2000: entre -0.19 y +0.18

retornos = np.array([0.004] * 19 + [-0.08])
print("ejemplo:", round(float(stats.skew(retornos, bias=False)), 2))   # -> -4.47
```

## Errores típicos

- **Decir que la curtosis mide lo puntiaguda que es una distribución.** Mide el peso de las
  colas: cuánta probabilidad hay en los extremos. Dos distribuciones con la misma curtosis pueden
  tener picos muy distintos, porque el pico lo fija la escala, no el cuarto momento.
- **Usar la asimetría o la curtosis muestrales con pocos datos.** Son potencias terceras y cuartas:
  un par de valores mandan sobre el resultado. Con 20 datos normales, la asimetría muestral puede
  pasar de +2 a −2 sin que haya nada raro; con 2.000 datos, su variación es de unas décimas. Si
  citas una curtosis, mira cuántas observaciones la sostienen.
- **Confundir las dos convenciones de curtosis.** Excel `CURT` y `scipy` con `fisher=True`
  devuelven exceso (normal = 0); otras herramientas devuelven curtosis de Pearson (normal = 3).
  Decir «curtosis 3» refiriéndose al exceso es un error de lectura de datos, no de matemáticas.
- **Seguir usando la regla 68-95-99,7 con colas gordas.** Con curtosis alta, la proporción de
  valores fuera de `±3σ` es bastante mayor que el 0,3 % de la normal, y el VaR calculado con esa
  regla subestima sistemáticamente las pérdidas.
- **Deducir la asimetría de la media menos la mediana y creerse el signo siempre.** En
  distribuciones unimodales y suaves, media > mediana sugiere asimetría positiva, pero con dos
  modas la relación se rompe. Además esa diferencia no tiene unidades comparables entre escalas:
  para eso está el coeficiente `3(x̄ − mediana)/s`.
- **Suponer que los momentos existen.** Hay distribuciones de cola tan pesada que la varianza es
  infinita (por ejemplo, las estables con exponente menor que 2) y la curtosis no está definida;
  con exponente menor o igual que 1 ni siquiera existe la media. Calcular `std()` sobre una
  muestra de esas no da un número estable: crece con el tamaño de la muestra.
- **Mirar solo los cuatro momentos.** Cuatro números no describen una distribución: dos datasets
  con la misma media, varianza, asimetría y curtosis pueden tener formas completamente distintas
  ([[eda-pasos]]).

:::aviso
En finanzas, la curtosis no es un detalle académico. Un modelo que asume normalidad y una
curtosis real de 8 comete errores grandes justo en la cola, que es la parte del riesgo que
importa. Antes de meter retornos en un optimizador de media-varianza, mira la curtosis y la
asimetría de la serie; si se alejan de cero, ese optimizador está resolviendo otro problema.
:::

:::practica
enunciado: Cinco salarios mensuales, en miles de euros: 18, 20, 22, 24 y 66. Calcula el coeficiente de asimetría 3·(media − mediana)/s y decide de qué lado está la cola larga.
pista: La mediana es el valor central con los datos ordenados; la desviación típica muestral divide la suma de cuadrados entre n − 1.
solucion: Media = 150/5 = 30; mediana = 22. Desviaciones: −12, −10, −8, −6, 36; cuadrados 144 + 100 + 64 + 36 + 1.296 = 1.640. s² = 1.640/4 = 410; s = 20,25. Coeficiente = 3·(30 − 22)/20,25 = 24/20,25 = +1,19. Es positivo y alto: un solo salario de 66 estira la cola hacia la derecha, así que la media no representa al empleado típico.
:::

## Comprueba que lo sabes

:::quiz
p: Un conjunto de retornos tiene curtosis en exceso de +12. ¿Qué implica?
o: Que la distribución es más puntiaguda que la normal y nada más
o: Que hay más probabilidad en las colas que en una normal y la varianza puede no describir bien el riesgo
o: Que la media está mal calculada
o: Que la distribución es simétrica
a: 2
e: La curtosis mide el peso de las colas: un exceso de +12 indica valores extremos mucho más frecuentes que en la normal. La lectura de «más puntiaguda» es incorrecta, y la curtosis no dice nada sobre la simetría (eso es la asimetría) ni sobre la media.
:::

:::quiz
p: ¿Por qué una asimetría muestral de −3,5 calculada con 15 observaciones hay que tomarla con pinzas?
o: Porque la asimetría solo se define para muestras de más de 100 datos
o: Porque el estimador usa potencias terceras y unas pocas observaciones deciden el resultado
o: Porque la asimetría negativa es imposible en muestras pequeñas
o: Porque el signo cambia al estandarizar los datos
a: 2
e: Con 15 datos normales, la asimetría muestral se mueve fácilmente entre −2 y +2 sin que haya nada anómalo, porque elevar al cubo da un peso enorme a uno o dos valores. El signo no cambia al estandarizar, y no hay ningún mínimo de 100 datos: simplemente hace falta bastante más muestra para que el número sea estable.
:::

:::quiz
p: ¿Qué distribución tiene la curtosis en exceso más baja posible, y cuánto vale?
o: La normal, con 0
o: La exponencial, con 6
o: Una Bernoulli con probabilidad 0,5, con −2
o: La uniforme continua, con −1,2
a: 3
e: El mínimo teórico del exceso de curtosis es −2, y lo alcanza una variable de dos valores equiprobables (una moneda). La uniforme continua se queda en −1,2 y la normal en 0. La exponencial tiene 6, es decir, colas mucho más pesadas que la normal.
:::
