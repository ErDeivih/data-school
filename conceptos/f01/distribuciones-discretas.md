---
id: distribuciones-discretas
titulo: Distribuciones discretas
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [variable-aleatoria, valor-esperado, varianza-y-desviacion]
tags: [probabilidad, distribuciones, conteo]
resumen: Bernoulli, binomial, geométrica, Poisson y multinomial: qué mecanismo genera cada una y cómo elegir la correcta según lo que estés contando.
fuentes: ["Ross (2014), 'Introduction to Probability Models'", "DeGroot y Schervish (2012), 'Probability and Statistics'"]
---

## En una frase

Cada distribución discreta nace de un mecanismo concreto —un sí o no, contar éxitos en `n`
intentos, esperar al primero, contar sucesos raros en un intervalo— y reconocer el mecanismo
es toda la batalla.

## La idea

No hay que memorizar fórmulas: hay que reconocer la historia. Cada distribución discreta
responde a una pregunta distinta, y si te equivocas de historia, la fórmula da números con
buena pinta y mal significado.

- **«Sí o no, una vez.»** Un cliente convierte o no; un correo es spam o no. Es una
  **Bernoulli**: un solo ensayo con probabilidad `p` de éxito.
- **«Sí o no, `n` veces, siempre con la misma `p` y sin que un ensayo afecte al siguiente.»**
  Cuántos de los 10 correos son spam. Es una **binomial**, que es la suma de `n` Bernoullis
  independientes e idénticas.
- **«¿Cuántos intentos hasta que salga?»** Cuántas llamadas hasta que me contestan, cuántos
  intentos hasta que un anuncio recibe un clic. Es una **geométrica**.
- **«¿Cuántos sucesos raros ocurren en un intervalo fijo?»** Llamadas que llegan a un centro de
  atención en una hora, errores de un servidor al día, coches que cruzan un peaje. Es una
  **Poisson**, y aparece como límite de la binomial cuando `n` es enorme y `p` diminuta pero
  `n·p` se mantiene constante.
- **«¿Cómo se reparten `n` ensayos entre `k` categorías?»** Los 12 clientes que eligen entre
  tres planes. Es una **multinomial**.

El detalle que decide si puedes usar la binomial es el supuesto de **independencia y `p`
constante**. Si muestreas sin reemplazo (extraes 5 piezas de un lote de 50 y las que salen no
vuelven), los ensayos no son independientes y la distribución correcta es la **hipergeométrica**.
Si el número de intentos no es fijo sino que esperas a acumular `r` éxitos, es la **binomial
negativa**. Confundir estas cuatro es el error más habitual en control de calidad y en análisis
de embudos.

Un aviso sobre la Poisson: su rasgo definitorio es que la media y la varianza son iguales a
`λ`. Si con tus datos la varianza muestral es mucho mayor que la media (sobredispersión), el
modelo Poisson no se sostiene: hay agrupamiento, heterogeneidad o dependencia, y lo normal es
pasar a una binomial negativa o a un modelo con sobredispersión explícita.

## Definición formal

Todas son variables discretas con función de masa `p(x) = P(X = x)`:

- **Bernoulli(p).** `P(X = 1) = p`, `P(X = 0) = 1 − p`. Media `p`; varianza `p(1 − p)`.
- **Binomial(n, p).** `P(X = k) = C(n, k) · p^k · (1 − p)^(n − k)` para `k = 0, …, n`, donde
  `C(n, k) = n!/(k!(n − k)!)` es «n sobre k», el número de formas de elegir qué intentos
  salen bien. Media `n·p`; varianza `n·p·(1 − p)`.
- **Geométrica(p).** `P(X = k) = (1 − p)^(k − 1) · p` para `k = 1, 2, 3, …`, contando el número
  de intentos **incluido** el acierto. Media `1/p`; varianza `(1 − p)/p²`. Es
  «sin memoria»: saber que han fallado 4 veces no cambia la probabilidad de acertar a la
  quinta.
- **Poisson(λ).** `P(N = k) = e^(−λ) · λ^k / k!` para `k = 0, 1, 2, …`, donde `λ > 0` es el
  número medio de sucesos por intervalo. Media `λ` y varianza `λ`.
- **Multinomial(n, p₁, …, p_k).** Con `n` ensayos independientes y `k` categorías mutuamente
  excluyentes cuyas probabilidades suman 1:
  `P(n₁, …, n_k) = (n!/(n₁!···n_k!)) · p₁^n₁ ⋯ p_k^n_k`, con `n₁ + ⋯ + n_k = n`. Cada categoría
  por separado es una binomial de parámetros `n` y `p_i`.

Dos familias de apoyo que aparecen cuando fallan los supuestos:

- **Hipergeométrica.** Muestreo sin reemplazo de una población finita de tamaño `N` con `K`
  éxitos. La media es `n·K/N`, pero la varianza es menor que la de la binomial equivalente,
  porque cada extracción informa sobre las siguientes.
- **Binomial negativa.** Número de intentos hasta acumular `r` éxitos. Con `r = 1` es la
  geométrica, y su varianza puede superar holgadamente la media, lo que la hace útil cuando hay
  sobredispersión.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p` | La probabilidad de éxito de un ensayo | adimensional, entre 0 y 1 | La media de la binomial sube (`n·p`); la varianza sube y luego baja, con máximo en `p = 0,5` |
| `n` | El número de ensayos, fijo de antemano | ensayos | La media sube proporcionalmente y la desviación típica solo con `√n`: el resultado se vuelve más predecible en términos relativos |
| `k` | El número de éxitos que estás contando | éxitos | Solo tiene sentido entre 0 y `n`; por encima de `n` la probabilidad es 0 |
| `λ` | La tasa media de sucesos por intervalo, con `λ = n·p` | sucesos por intervalo | La media y la varianza suben a la vez: si tus datos tienen varianza muy por encima de la media, la Poisson no vale |
| `N`, `K` | Tamaño de la población y cuántos éxitos hay en ella | elementos | Con `K/N` fijo, la media de la hipergeométrica no cambia, pero su varianza baja al reducir `N`: cada extracción informa más de las siguientes |
| `r` | Éxitos que hay que acumular en la binomial negativa | éxitos | La media sube (`r/p`) y la varianza también; con `r` grande la distribución se parece cada vez más a una Poisson |
:::

La figura enseña las dos caras del mismo mecanismo: en el centro, dos modelos distintos que dan
casi el mismo número; en la cola, la diferencia que decide cuál hay que usar.

:::figura
fichero: discretas-binomial-pn-limite-y-cola
pie: A la izquierda, la binomial con `n = 10.000` y `p = 0,00025` y la Poisson con `λ = n·p = 2,5` dan la misma altura en cada barra: por eso se puede sustituir una por otra. A la derecha, la misma media con la varianza multiplicada por 3,5 cambia la cola en un factor 16. Compara las dos curvas de la derecha a partir de 8 sucesos: ahí es donde una Poisson mal elegida subestima los incidentes del año.
fuente: figuras/distribuciones-discretas-1.py
:::

## Ejemplo

**Binomial.** `n = 10` correos, probabilidad de spam `p = 0,3`. `P(X = 3) = 0,2668` y
`P(X ≤ 3) = 0,6496`. La media es 3 y la varianza 2,1, así que la desviación típica es
`√2,1 = 1,449`: ver 1 o 5 spams en una bandeja de 10 no es nada raro. Ver 8 o más sí:
`P(X ≥ 8) = 0,0016`.

**Geométrica.** Con `p = 0,2`, `P(X = 5) = 0,8⁴ · 0,2 = 0,0819` y la media son 5 intentos.
Fíjate en que la media es 5 y que los primeros cinco intentos solo acumulan
`1 − 0,8⁵ = 0,6723` de probabilidad: la cola es larga.

**Poisson y su límite.** Un servidor recibe 2,5 peticiones por segundo de media. Con
`λ = 2,5`, `P(N = 2) = 0,2565`. Para comprobar de dónde sale, toma la binomial con
`n = 10.000` y `p = 0,00025` (mismo `λ = n·p = 2,5`): da `P(X = 0) = 0,08206` frente a
`0,08208` de la Poisson, y `P(X = 2) = 0,25654` frente a `0,25652`. La diferencia está en la
cuarta cifra decimal. Y aunque `P(N ≥ 8) = 0,0042` parezca despreciable, en un sistema que
atiende un millón de segundos al año son unas 4.200 rachas de ese tipo: la cola importa.

**Multinomial.** 12 clientes eligen entre tres planes con probabilidades 0,5, 0,3 y 0,2. La
probabilidad de que queden 6, 4 y 2 es `0,0702`. Si solo te interesara «cuántos eligen el plan
A», sería una binomial de `n = 12` y `p = 0,5`.

## Código

```python verificable
from scipy import stats

# Binomial: 10 ensayos independientes con la misma p = 0,3
n, p = 10, 0.3
print(f"P(X = 3)   = {stats.binom.pmf(3, n, p):.4f}")   # -> 0.2668
print(f"P(X <= 3)  = {stats.binom.cdf(3, n, p):.4f}")  # -> 0.6496
print(f"media bin  = {stats.binom.mean(n, p):.4f}")    # -> 3.0000
print(f"varianza   = {stats.binom.var(n, p):.4f}")     # -> 2.1000
print(f"P(X >= 8)  = {stats.binom.sf(7, n, p):.5f}")   # -> 0.00159

# Geometrica: numero de intentos hasta el primer exito, incluido el acierto
print(f"P(G = 5)   = {stats.geom.pmf(5, 0.2):.4f}")    # -> 0.0819
print(f"media geom = {stats.geom.mean(0.2):.4f}")      # -> 5.0000
```

:::claves
- `stats.binom.pmf(3, n, p)` recibe primero el valor de la variable y después los parámetros. Cambiar el orden no da un error inmediato y a veces devuelve un número con buena pinta: si esa llamada fuera `pmf(n, 3, p)` estarías pidiendo la probabilidad de 10 éxitos en 3 ensayos.
- `stats.binom.sf(7, n, p)` es la función de supervivencia `P(X > 7)`, no `P(X ≥ 7)`. Por eso el ejemplo escribe `sf(7, ...)` para obtener `P(X ≥ 8)`: el off-by-one clásico. `1 - cdf(8, n, p)` da otro número, y es el equivocado.
- `stats.geom.pmf(5, 0.2)` cuenta el número de intentos **incluido** el acierto, empezando en 1. Existe la variante que cuenta los fracasos previos y empieza en 0: si la usas, todas las probabilidades se desplazan una posición y `P(X = 5)` pasa a ser `P(X = 4)` en tu hoja de cálculo.
- `stats.poisson.pmf(0, n * p)` acepta `n * p` como tasa sin avisar de que el resultado es una media: la función no sabe si `λ` viene de contar sucesos o de multiplicar dos parámetros, así que el error de usar `p` en lugar de `n·p` solo se nota en las cuentas.
- `stats.multinomial.pmf([6, 4, 2], 12, [0.5, 0.3, 0.2])` quiere las probabilidades en el mismo orden que los conteos y que sumen 1. Si suman 0,9999 por redondeo devuelve un valor absurdo o un cero, sin decir nada.
- `stats.binom.var(n, p)` devuelve la varianza teórica `n·p·(1 − p)`, no la varianza de unos datos. Si lo que quieres es la dispersión de tu muestra, esa función no la calcula, y el número puede parecer razonable aunque tus datos no sean binomiales.
:::

```python verificable
from scipy import stats

# Binomial con n grande y p pequena: el limite es la Poisson con lambda = n * p.
n, p = 10000, 0.00025
print(f"binomial P(X = 0) = {stats.binom.pmf(0, n, p):.5f}")   # -> 0.08206
print(f"Poisson  P(N = 0) = {stats.poisson.pmf(0, n * p):.5f}")   # -> 0.08208
print(f"binomial P(X = 2) = {stats.binom.pmf(2, n, p):.5f}")   # -> 0.25654
print(f"Poisson  P(N = 2) = {stats.poisson.pmf(2, n * p):.5f}")   # -> 0.25652
print(f"lambda = n * p    = {n * p}")                          # -> 2.5

# La cola de la Poisson: sucesos raros que en volumen anual dejan de serlo.
print(f"Poisson P(N >= 8) = {stats.poisson.sf(7, n * p):.4f}")   # -> 0.0042

# Multinomial: 12 clientes entre 3 planes con probabilidades 0,5 / 0,3 / 0,2
print(f"P(6, 4, 2) = {stats.multinomial.pmf([6, 4, 2], 12, [0.5, 0.3, 0.2]):.4f}")  # -> 0.0702
```

## Errores típicos

- **Usar la binomial cuando se muestrea sin reemplazo.** Si extraes 5 piezas de un lote de 50 y
  no devuelves las que salen, los ensayos son dependientes: la distribución es la
  hipergeométrica, con menos varianza. La binomial solo es correcta si el lote es enorme en
  comparación con la muestra.
- **Confundir la geométrica con su variante desplazada.** `P(X = k) = (1 − p)^(k−1)·p` cuenta
  el número de intentos empezando en 1; hay libros y funciones que cuentan los fracasos previos
  y empiezan en 0. Todo el cálculo se desplaza una unidad, y ese desajuste arruina las cuentas.
- **Ajustar una Poisson con datos sobredispersos.** Si la varianza muestral es mucho mayor que
  la media, hay agrupamiento o heterogeneidad y la Poisson subestima las colas. Comprueba
  siempre la relación media-varianza antes de usarla.
- **Leer la media como un pronóstico exacto.** «`n·p = 3`, luego saldrán 3» ignora la varianza
  2,1 y su desviación 1,45. Obtener 1 o 5 es lo normal; el 3 es solo el centro de gravedad.
- **Olvidar la cola en el dimensionado.** `P(N ≥ 8) = 0,0042` por segundo puede convertirse en
  miles de incidentes al año. El error no es el número, es no multiplicarlo por el volumen.
- **Confundir masa con acumulada al calcular «al menos».** `P(X ≥ 8)` no es `1 − P(X ≤ 8)`, sino
  `1 − P(X ≤ 7)`. El off-by-one es el error más frecuente en los contrastes de calidad, y en
  la práctica decide si rechazas un lote que estaba bien.

:::practica
enunciado: Un lote tiene 50 piezas y 8 son defectuosas. Extraes 5 sin devolverlas al lote. Calcula la probabilidad de que ninguna sea defectuosa con el modelo correcto y di qué daría la binomial mal aplicada con p = 0,84.
pista: Sin reemplazo los ensayos son dependientes: toca la hipergeométrica, con N = 50, K = 8 y n = 5. La binomial supondría una p fija en las cinco extracciones.
solucion: P(ninguna defectuosa) = C(42,5)/C(50,5) = 850.668/2.118.760 = 0,4015. La binomial daría 0,84⁵ = 0,4182, unos 1,7 puntos más. La diferencia es pequeña porque la muestra es el 10 % del lote, pero el error tiene signo fijo: la hipergeométrica siempre tiene menos varianza, así que la binomial exagera los resultados extremos.
:::

## Comprueba que lo sabes

:::quiz
p: Estás contando cuántas llamadas recibes en una hora y tu media es 12, con varianza muestral 45. ¿Qué modelo encaja mejor?
o: Poisson de lambda 12, porque los sucesos son raros
o: Una binomial negativa, porque la varianza es mucho mayor que la media
o: Geométrica, porque esperas a que llegue la primera llamada
a: 2
e: En una Poisson la media y la varianza coinciden en lambda, y aquí 45 está muy por encima de 12: hay sobredispersión, típica de llegadas agrupadas o de una mezcla de clientes con tasas distintas. La binomial negativa permite esa varianza extra. La geométrica modela el tiempo hasta la primera llamada, no el número de llamadas en una hora.
:::

:::quiz
p: ¿Cuál es la diferencia entre la binomial y la geométrica?
o: La binomial cuenta éxitos en un número fijo de ensayos; la geométrica cuenta ensayos hasta el primer éxito
o: La binomial es para sucesos raros y la geométrica para sucesos frecuentes
o: La geométrica es la binomial con n = 1
a: 1
e: En la binomial el número de ensayos es fijo y la variable es cuántos salen bien. En la geométrica el número de ensayos es lo que varía y el éxito es único. La binomial con n = 1 sí es una Bernoulli, no una geométrica.
:::

:::quiz
p: Con n = 10 y p = 0,3, ¿qué significa que la varianza sea 2,1?
o: Que el número de éxitos se aleja de la media 3 con una desviación típica de 1,45, así que ver 1 o 5 éxitos es normal
o: Que el máximo de éxitos posibles es 2,1
o: Que la media cambia con cada muestra en 2,1 unidades
a: 1
e: La varianza mide dispersión: su raíz, 1,45, es la distancia típica a la media de 3. Ver 1,45 o más éxitos de diferencia respecto al 3 es corriente, y hasta cierto punto esperable; no hay ningún tope en 2,1.
:::
