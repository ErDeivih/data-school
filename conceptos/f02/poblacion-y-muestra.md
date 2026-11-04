---
id: poblacion-y-muestra
titulo: Población y muestra
fase: 2
nivel: básico
rutas: [ds, core]
prerequisitos: [medidas-de-centralidad, variable-aleatoria]
tags: [muestreo, inferencia, sesgo]
resumen: La población es lo que quieres describir y la muestra lo que mides; de esa distancia nacen el error de muestreo y casi todos los sesgos.
fuentes: ["Cochran (1977), 'Sampling Techniques'", "Lohr (2019), 'Sampling: Design and Analysis'"]
---

## En una frase

La **población** es el conjunto completo sobre el que quieres afirmar algo, la **muestra** es el
trozo que de verdad puedes medir, y toda la estadística inferencial consiste en saltar de una a
otra sabiendo cuánto te puedes equivocar al hacerlo.

## La idea

Estás cocinando una sopa para doce personas. No te la bebes entera para saber si está salada:
remueves bien, coges una cucharada y la pruebas. Esa cucharada es la **muestra** y la olla entera
es la **población**. El truco funciona por dos condiciones: que hayas removido (que la cucharada
sea *representativa*) y que sepas que dos cucharadas distintas no saben exactamente igual (que
existe *variabilidad muestral*).

Las dos condiciones fallan continuamente en el trabajo real:

- **No siempre puedes remover.** Si haces una encuesta de satisfacción por correo electrónico, la
  muestra son los que contestan, no los clientes. Y los que contestan son justo los muy contentos
  y los muy enfadados: la cucharada se ha cogido de la superficie de la olla, donde flota la sal.
  Eso es **sesgo de selección**, y no se arregla con más datos: se arregla cambiando cómo eliges.
- **La variabilidad es inevitable.** Aunque la muestra sea perfecta, dos muestras aleatorias de la
  misma población dan medias distintas. Eso es el **error de muestreo**, y sí se reduce con `n`
  más grande.

La distinción que más cuesta interiorizar es la de los dos vocabularios. Sobre la población hablas
de **parámetros**: la media real de todos los clientes, la proporción real de piezas defectuosas.
Sobre la muestra hablas de **estadísticos**: la media de los 200 clientes que contestaron, el 3,1 %
de defectuosas que contaste. Los parámetros no los ves nunca, y son la respuesta a la pregunta que
te importa. Los estadísticos los calculas siempre, y son solo una pista. Toda la inferencia (los
[[intervalos-de-confianza]], el [[contraste-de-hipotesis]], el [[bootstrap]]) existe precisamente
para cuantificar qué relación hay entre la pista y la respuesta.

:::figura
fichero: muestra-parametro-y-diseno
pie: Cada punto es una muestra de n = 2 y el promedio de las 15 cae justo en μ, pero la muestra (1200, 1500) falla por 650 €: insesgado no significa acertado. A la derecha, con el mismo n = 5, forzar la representación de cada departamento baja la desviación de 377 € a 19 €, así que la representatividad se arregla con diseño y no con más datos.
fuente: figuras/poblacion-y-muestra-1.py
:::

## Definición formal

Sea una población de tamaño `N` y una muestra de tamaño `n`, con `n ≤ N`. La muestra se representa
como una variable aleatoria `(X₁, X₂, …, Xₙ)`: antes de extraerla no sabes qué valores saldrán.

- `N` — número de elementos de la población. Puede ser finito (los 48.000 clientes de una empresa)
  o conceptualmente infinito (todas las piezas que produciría una máquina en el futuro).
- `n` — número de elementos de la muestra; lo eliges tú.
- `θ` — **parámetro**: una característica numérica de la población, como la media `μ`, la
  proporción `p` o la desviación típica `σ`. Es un número fijo y desconocido.
- `θ̂` («theta sombrero») — **estadístico**: la misma característica calculada sobre la muestra,
  como `x̄` o `p̂ = k/n` con `k` el número de éxitos. Es una variable aleatoria: cambia con cada
  muestra.
- `θ̂ − θ` — **error de estimación** de una muestra concreta. Se descompone en sesgo, varianza y
  error de medición.

Dos condiciones definen una **muestra aleatoria simple**: cada elemento de la población tiene la
misma probabilidad de salir, y las extracciones son independientes entre sí. Bajo ellas el valor
esperado de la media muestral es la media poblacional, `E[x̄] = μ`, y su desviación típica —el
**error típico**— vale:

:::formula
ET(x̄) = σ / √n    y, si n/N > 0,05,   ET(x̄) = (σ / √n) · √((N − n) / (N − 1))
:::

- `σ` — desviación típica de la población.
- `√((N − n) / (N − 1))` — **factor de corrección para población finita**: cuando muestreas una
  fracción apreciable de una población finita, hay menos incertidumbre de la que sugiere `σ/√n`,
  porque al medir un elemento ya no puede volver a salir.

Cuando la `n` es una fracción pequeña de `N` (menos del 5 %) el factor vale casi 1 y se ignora.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Elementos que mides: el tamaño de la muestra | elementos | El error típico cae como `1/√n`: cuadruplicar la muestra lo reduce a la mitad. No toca el sesgo, y por eso no arregla una muestra mal elegida |
| `N` | Elementos de la población | elementos | Con `N` mucho mayor que `n` el factor de corrección tiende a 1 y se ignora; cuando muestreas más del 20 % de una población finita, el error típico real es menor del que sugiere `σ/√n` |
| `σ` | Desviación típica de la población | las de la variable | Es el numerador del error típico: el doble de dispersión, el doble de incertidumbre. Si no la conoces se estima con `s` |
| `n/N` | Fracción de muestreo | proporción | Por debajo de 0,05 el factor vale casi 1; con 200 de 400 empleados (0,5) el error típico baja un 29 %. Ignorarlo te hace reportar más incertidumbre de la que tienes |
| `θ` | Parámetro de la población (media `μ`, proporción `p`, desviación `σ`) | las de la variable | Es fijo: no sube ni baja, y no lo observas nunca. Es la respuesta a la pregunta, no un resultado del estudio |
| `θ̂` | Estadístico calculado sobre la muestra (`x̄`, `p̂ = k/n`) | las de la variable | Es aleatorio: cambia con cada muestra. Su dispersión es el error típico y su centro es lo que decide si el estimador es insesgado |
:::

## Ejemplo

Los sueldos mensuales de los 6 empleados de una empresa pequeña, en euros:

```
1200   1500   1800   2100   2400   3000
```

- Media poblacional: (1200 + 1500 + 1800 + 2100 + 2400 + 3000) / 6 = 12.000 / 6 = **2.000 €**.
  Ese es el parámetro `μ`: no lo ves si solo tienes una nómina delante.
- Muestra de tamaño `n = 2`: hay 15 pares posibles. Sus medias van de **1.350 €** (el par
  1200 y 1500) a **2.700 €** (el par 2400 y 3000).
- Si tu muestra es el par (1200, 1500), tu estadístico es 1.350 € y tu error de estimación es
  1.350 − 2.000 = **−650 €**, un 32 % por debajo. Con `n = 2` eso es normal, no mala suerte.

Fíjate en lo importante: el estimador `x̄` es insesgado (promediando las 15 medias sale 2.000 €
exactos), pero *una* muestra concreta puede estar muy lejos. Insesgado no significa acertado.

## Código

```python verificable
import numpy as np
from itertools import combinations

# Los seis sueldos que forman la poblacion completa (N = 6)
poblacion = np.array([1200, 1500, 1800, 2100, 2400, 3000])
print(f"media poblacional: {poblacion.mean():.1f}")  # -> 2000.0

# Todas las muestras posibles de tamano 2: son 15
pares = np.array(list(combinations(poblacion, 2)))
medias = pares.mean(axis=1)
print(f"numero de muestras: {len(pares)}")       # -> 15
print(f"menor media muestral: {medias.min():.1f}")  # -> 1350.0
print(f"mayor media muestral: {medias.max():.1f}")  # -> 2700.0
print(f"media de las 15 medias: {medias.mean():.1f}")  # -> 2000.0
```

La última línea es la definición de insesgadez en acción: el promedio de todos los estadísticos
posibles devuelve el parámetro.

:::claves
- `np.array(list(combinations(poblacion, 2)))` construye las 15 parejas de golpe. `combinations` no repite elementos ni el orden, así que no hay duplicados que quitar; con `permutations` tendrías 30 y cada pareja contada dos veces.
- `pares.mean(axis=1)` promedia **cada fila**, es decir cada pareja, y devuelve 15 medias. Con `axis=0` promediaría las dos columnas y saldría un único número: la diferencia entre las dos llamadas es todo el ejemplo.
- `poblacion.mean()` se calcula sobre los seis sueldos, no sobre las muestras: ese 2.000 € es el parámetro `μ`. Que `medias.mean()` dé exactamente lo mismo es la insesgadez, y es una propiedad del procedimiento, no de ninguna muestra.
- `combinations` solo es correcto porque todas las parejas son igual de probables: enumera el espacio muestral completo del muestreo aleatorio simple. Si el diseño fuera estratificado o por conglomerados, esta lista de 15 no representaría el experimento.
- El sesgo y el error no son el mismo número: `medias.mean() - poblacion.mean()` vale 0, mientras que una muestra concreta se equivoca 650 €. Confundir la propiedad del estimador con el resultado de una estimación es el error que la página entera intenta desactivar.
- Cambia el `2` de `combinations(poblacion, 2)` por `3` y vuelve a mirar `medias.min()` y `medias.max()`: pasan de 1.350-2.700 a 1.500-2.500. Esa horquilla que se estrecha es el único efecto de aumentar `n`, y se comprueba en una línea.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)

# Sueldos por departamento: dentro de cada grupo son parecidos, pero los grupos
# tienen medias muy distintas. 6 tecnicos y 4 directivos.
tecnicos = np.array([1800.0, 1900, 1850, 1950, 1820, 1880])
directivos = np.array([4100.0, 4200, 4150, 4250])
poblacion = np.concatenate([tecnicos, directivos])
print(f"media poblacional      {poblacion.mean():.0f}")  # -> 2790

# Muestreo aleatorio simple: 5 personas de las 10 al azar
simple = np.array([rng.choice(poblacion, size=5, replace=False).mean()
                   for _ in range(2000)])

# Muestreo estratificado: 3 tecnicos y 2 directivos (la mitad de cada grupo)
estrat = np.array([0.6 * rng.choice(tecnicos, size=3, replace=False).mean()
                   + 0.4 * rng.choice(directivos, size=2, replace=False).mean()
                   for _ in range(2000)])

print(f"media del estratificado        {estrat.mean():.0f}")  # -> 2790
print(f"desviacion del muestreo simple {simple.std():.0f}")  # -> 376
print(f"desviacion del estratificado   {estrat.std():.0f}")  # -> 19
```

Mismo tamaño de muestra y misma población: las dos estrategias aciertan de media (2.790 €), pero
la aleatoria simple se desvía 376 € y la estratificada solo 19 €. Al forzar que cada estrato esté
representado, desaparece la varianza que venía de la diferencia entre departamentos. Eso es diseño
de muestreo, y no cuesta ni un dato más.

## Errores típicos

- **Decir «la muestra es grande, luego es representativa».** Representatividad y tamaño son cosas
  distintas. Una encuesta online con 100.000 respuestas sigue sesgada si solo la contesta gente
  con conexión y tiempo libre. Más `n` reduce el error de muestreo; no toca el sesgo.
- **Reportar el estadístico como si fuera el parámetro.** «El salario medio es 2.150 €» cuando eso
  es la media de tu muestra de 40 personas. Se escribe «2.150 € (media muestral, n = 40, error
  típico 90 €)». Sin `n` ni incertidumbre, el número no significa nada.
- **Confundir `N` con `n` al citar cifras.** «El 47 % de los españoles» con una muestra de 1.000
  personas es una estimación con un margen; el 47 % de la población no se ha medido.
- **Sesgo de supervivencia al construir la muestra.** Analizar el éxito de las empresas que
  siguen abiertas, o la rentabilidad de los fondos que no han cerrado. La población era «todas
  las que se crearon», y la muestra se ha autoseleccionado. Ver
  [[sesgo-de-supervivencia]].
- **Ignorar la no respuesta.** Si envías 1.000 encuestas y responden 120, tu `n` real es 120, no
  1.000, y además esos 120 no son una muestra aleatoria de los 1.000. La tasa de respuesta es un
  resultado del estudio, no un detalle administrativo.
- **Usar `σ/√n` cuando muestreas una fracción grande de la población.** Con 200 empleados de 400,
  `n/N = 0,5` y el factor de corrección reduce el error típico un 29 %. Ignorarlo te hace reportar
  más incertidumbre de la que tienes.

:::trampa
Cuando veas una muestra, la primera pregunta no es «¿cuántos son?» sino «¿quiénes son y quiénes
no están?». El sesgo de selección no se corrige con ninguna fórmula, ni con más datos, ni con
machine learning: solo se corrige cambiando el mecanismo de selección o reponderando con
información auxiliar conocida de toda la población.
:::

:::practica
enunciado: Una población de cinco pedidos tarda 4, 6, 8, 10 y 12 minutos. Enumera las diez muestras posibles de tamaño 2, calcula la media de sus diez medias y el error de estimación de la muestra (4, 6).
pista: Son las diez parejas sin orden; si el estimador es insesgado, la media de todas las medias coincide con el parámetro.
solucion: μ = 40/5 = 8 minutos. Medias de las diez parejas: 5, 6, 7, 8, 7, 8, 9, 9, 10, 11; suman 80, y 80/10 = 8 = μ: x̄ es insesgado. La muestra (4, 6) da x̄ = 5 y un error de estimación de 5 − 8 = −3 minutos, un 37,5 % por debajo. Con n = 2 eso no es mala suerte, es la variabilidad muestral.
:::

## Comprueba que lo sabes

:::quiz
p: En una población de seis sueldos con media 2.000 €, tomas la muestra (1200, 1500). ¿Qué afirmación es correcta?
o: El estimador está mal calculado, porque su valor no coincide con el parámetro
o: El estadístico vale 1.350 € y el error de estimación es de −650 €, algo normal con n = 2
o: La media poblacional también vale 1.350 €, porque las muestras son insesgadas
a: 2
e: El estadístico es la media de la muestra, 1.350 €, y el parámetro sigue siendo 2.000 €: el error es −650 €. Que el estimador sea insesgado quiere decir que el promedio de todas las muestras posibles da 2.000 €, no que cada muestra acierte.
:::

:::quiz
p: ¿Por qué aumentar el tamaño de la muestra no corrige un sesgo de selección?
o: Porque el sesgo depende de a quién incluyes, no de cuántos incluyes
o: Porque el error típico crece con la raíz de n
o: Porque con más datos siempre aparece multicolinealidad
a: 1
e: El sesgo viene del mecanismo de selección: si tu muestra son solo los que contestan un correo, medir a más personas así no arregla nada, solo estima con más precisión el valor equivocado. Lo que reduce el error de muestreo es n; lo que reduce el sesgo es el diseño.
:::

:::quiz
p: Muestreas 200 empleados de una plantilla de 3.000 y calculas el error típico. ¿Qué papel juega el factor de corrección para población finita?
o: Multiplica el error típico, porque la población es finita
o: Reduce ligeramente el error típico, porque 200/3.000 es pequeño y el efecto es menor del 4 %
o: Es imprescindible, porque sin él la media muestral estaría sesgada
a: 2
e: El factor vale √((N − n)/(N − 1)); con n/N = 0,067 sale aproximadamente 0,966, es decir un 3,4 % menos. Es un ajuste pequeño que en nada afecta al sesgo: la insesgadez de la media muestral no depende de él.
:::

:::truco
Antes de calcular nada, escribe en una frase la población y el parámetro. «Población: todos los
pedidos entregados en marzo. Parámetro: tiempo medio de entrega.» Si no puedes nombrar la
población, todavía no tienes un problema estadístico, tienes una consulta.
:::
