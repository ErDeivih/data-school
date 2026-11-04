---
id: maxima-verosimilitud
titulo: Máxima verosimilitud (MLE)
fase: 2
nivel: avanzado
rutas: [ds, core]
prerequisitos: [estimadores-y-propiedades, probabilidad-condicional, distribuciones-continuas]
tags: [inferencia, estimacion, verosimilitud]
resumen: Elegir los parámetros que hacen más probables los datos observados; de ahí salen el MLE de una moneda y la pérdida de la regresión logística.
fuentes: ["Fisher (1922), 'On the Mathematical Foundations of Theoretical Statistics'", "Casella y Berger (2002), 'Statistical Inference', cap. 7"]
---

## En una frase

El **MLE** elige el valor del parámetro que hace que los datos que has visto sean lo más probables
posible: en vez de preguntar «¿qué valor tiene `p`?», pregunta «¿qué `p` haría más verosímil esta
muestra?» y devuelve ese.

## La idea

Tienes una moneda y no sabes si está trucada. La lanzas 10 veces y salen 7 caras. Cualquier valor
de `p` entre 0 y 1 es compatible con ese resultado, pero no todos igual de bien: si `p = 0,5`, ver
7 caras de 10 es bastante normal; si `p = 0,9`, ver 7 de 10 es raro (esperarías 9); si `p = 0,1`,
ver 7 caras es casi imposible. La **verosimilitud** convierte esa intuición en un número: la
probabilidad de los datos observados, calculada para cada valor posible de `p`. El MLE es el `p`
que la hace máxima, y con 7 de 10 sale 0,7.

El cambio de mentalidad que trae el MLE es sutil pero enorme: **los datos están fijos y el
parámetro se mueve**. En probabilidad clásica fijas `p = 0,5` y calculas la probabilidad de cada
resultado; en verosimilitud fijas el resultado «7 caras» y recorres todos los `p` posibles. La
función es la misma, la incógnita es la otra. Por eso se llama *verosimilitud* y no probabilidad:
no es una probabilidad sobre `p` (para eso hace falta un prior, como en
[[estimacion-bayesiana-map]]), es una función de `p` que no tiene por qué integrar 1.

¿Por qué se usa tanto? Por tres motivos concretos:

1. **Tiene receta.** Se escribe la verosimilitud, se toma el logaritmo (que convierte productos en
   sumas) y se deriva. Los candidatos a máximo salen de igualar a cero esa derivada.
2. **Tiene garantías.** Bajo condiciones suaves, el MLE es consistente, asintóticamente insesgado y
   asintóticamente eficiente: con muchos datos no hay estimador insesgado que le gane en varianza.
3. **Produce las pérdidas que ya usas.** Si los datos son normales, el MLE es la recta de mínimos
   cuadrados. Si son Bernoulli, el MLE es la [[glm-y-logistica|regresión logística]] con su pérdida
   de entropía cruzada. La `log-loss` que optimizas en un clasificador **es** una log-verosimilitud
   negativa. No hay dos conceptos ahí: son la misma cosa con otro nombre.

El precio es que el MLE puede portarse mal con pocos datos y con parámetros en el borde. Con 10
lanzamientos y 0 caras, el MLE de `p` es 0: afirma que es imposible sacar cara, con 10
datos. Ese es el problema que arreglan los priors y la regularización.

:::figura
fichero: verosimilitud-maximo-e-informacion
pie: A la izquierda, cada valor de p es una hipótesis y el máximo de la curva es el MLE; en p = 0,5 la log-verosimilitud baja solo 1,01, así que los datos son 2,7 veces más probables con 0,6: hay indicio, no prueba. A la derecha, la misma proporción observada con n = 10, 50 y 200 afila el máximo como manda la información de Fisher, y esa curvatura es exactamente lo que hace que la estimación varíe menos.
fuente: figuras/maxima-verosimilitud-1.py
:::

## Definición formal

Sea `x = (x₁, …, xₙ)` una muestra observada, generada por un modelo con parámetro `θ` (uno solo o
un vector). Su **función de verosimilitud** es:

:::formula
L(θ) = P(X = x ; θ)   si X es discreta    ·    L(θ) = ∏ᵢ f(xᵢ ; θ)
:::

- `L(θ)` — verosimilitud: la probabilidad (o densidad) conjunta de los datos observados, vista
  como función de `θ`. Con datos independientes es el producto de las densidades individuales.
- `f(xᵢ ; θ)` — densidad (o función de masa) de una observación, evaluada en el valor observado.
- `θ` — el parámetro o vector de parámetros que se quiere estimar.
- `θ̂_MLE` — el **estimador de máxima verosimilitud**: el valor de `θ` que maximiza `L(θ)`.

Como el logaritmo es monótono, maximizar `L` es maximizar `ℓ = log L`, y eso convierte productos
en sumas:

:::formula
ℓ(θ) = Σᵢ log f(xᵢ ; θ)    ·    ∂ℓ/∂θ = 0  (ecuación de verosimilitud)
:::

- `ℓ(θ)` — **log-verosimilitud**. Se usa ella porque las sumas son más fáciles de derivar y porque
  los productos de muchos números pequeños desbordan el rango de coma flotante.
- `∂ℓ/∂θ` — **función de puntuación** (*score*). Sus raíces son los candidatos a máximo; se
  comprueba que son máximos con la segunda derivada.
- `I(θ) = −E[∂²ℓ/∂θ²]` — **información de Fisher**: cuánta información aporta la muestra sobre
  `θ`. Cuanto mayor, más afilado es el máximo y menos varía la estimación.

Eso produce los dos resultados que se citan siempre, para muestras grandes:

:::formula
θ̂_MLE ≈ Normal(θ, 1 / I(θ))    ·    Var(θ̂) ≥ 1 / I(θ)   (cota de Cramér-Rao)
:::

El primero dice que el MLE es aproximadamente normal y centrado, con varianza la inversa de la
información. El segundo dice que **ningún** estimador insesgado puede tener menos varianza que
`1/I(θ)`: el MLE alcanza esa cota en el límite, y por eso se dice que es asintóticamente eficiente.

Dos propiedades de invarianza que conviene tener a mano:

- **Invarianza funcional:** si `θ̂` es el MLE de `θ`, entonces `g(θ̂)` es el MLE de `g(θ)` para
  cualquier función `g`. Esto es cierto y muy cómodo, pero **no** significa que `g(θ̂)` sea
  insesgado.
- **El MLE de la varianza divide por `n`, no por `n − 1`.** Maximizar la verosimilitud normal da
  `σ̂² = (1/n)·Σ(xᵢ − x̄)²`, que está sesgado hacia abajo. El estimador insesgado de Bessel no es el
  MLE: es una corrección posterior.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L(θ)` | Verosimilitud: probabilidad conjunta de los datos vista como función de `θ` | probabilidad o densidad | No es una probabilidad sobre `θ`: no integra 1 y no admite «hay un 70 % de que `p` sea 0,6». Con datos independientes es un producto, y con muchos datos se va a cero |
| `ℓ(θ)` | Log-verosimilitud, `log L` | log de probabilidad | Se usa ella porque convierte productos en sumas y porque un producto de 10.000 densidades pequeñas desborda la coma flotante. Maximizar `ℓ` es maximizar `L`: el logaritmo es monótono |
| `f(xᵢ ; θ)` | Densidad o función de masa de una observación | densidad o probabilidad | Es el supuesto del modelo: si los datos tienen colas gruesas y usas una normal, `ℓ` es la función equivocada y el máximo cae lejos |
| `θ` | Parámetro o vector de parámetros a estimar | los del modelo | Su dominio importa: `log p` con `p ≤ 0` o `log(1 − p)` con `p ≥ 1` valen −infinito y rompen la suma. Es el error más caro al escribir la verosimilitud |
| `θ̂_MLE` | Valor de `θ` que maximiza `L(θ)` | las de `θ` | Con 0 caras en 10 lanzamientos vale exactamente 0, y con separación perfecta en clasificación no existe como número finito: por eso la logística regulariza siempre |
| `∂ℓ/∂θ` | Función de puntuación (*score*) | — | Sus raíces son los candidatos a máximo, pero una raíz puede ser un mínimo: hay que comprobar la segunda derivada antes de dar el valor por bueno |
| `I(θ)` | Información de Fisher: `−E[∂²ℓ/∂θ²]` | — | Cuanto mayor, más afilado el máximo y menos varía la estimación. En una Bernoulli vale `n/(p(1 − p))`, así que sube con `n` y se dispara cuando `p` se acerca a 0 o a 1 |
| `n` | Número de observaciones | observaciones | Sube la información de forma lineal y baja el error típico como `1/√n`: con `p = 0,6`, 50 lanzamientos dan 0,069 y 200 dan 0,035 |
| `1 / I(θ)` | Varianza asintótica del MLE | (unidades de `θ`)² | Es también la cota de Cramér-Rao: ningún estimador insesgado puede bajar de ahí. El MLE la alcanza en el límite, y por eso se dice que es asintóticamente eficiente |
:::

## Ejemplo

Moneda lanzada `n = 50` veces, con `k = 30` caras. La verosimilitud es
`L(p) = p³⁰·(1 − p)²⁰` y la log-verosimilitud `ℓ(p) = 30·log p + 20·log(1 − p)`.

- Derivando: `ℓ'(p) = 30/p − 20/(1 − p) = 0` → `30(1 − p) = 20p` → `p = 30/50 = 0,6`.
- En `p = 0,6`, `ℓ(0,6) = 30·log(0,6) + 20·log(0,4) = −33,651`.
- En `p = 0,5`, `ℓ(0,5) = 50·log(0,5) = −34,657`. La diferencia, 1,006, es el logaritmo del cociente
  de verosimilitudes: la probabilidad de esta muestra bajo `p = 0,5` es `e^−1,006 ≈ 0,37` veces la
  que tiene bajo `p = 0,6`. Los datos son 2,7 veces más probables con `p = 0,6` que con `p = 0,5`.
  No es una prueba aplastante, y con 50 lanzamientos tampoco debería serlo.
- La información de Fisher es `I(p) = n / (p(1 − p)) = 50 / 0,24 = 208,3`, así que el error típico
  asintótico es `√(p(1 − p)/n) = √(0,24/50) = 0,0693`.
- Simulando 20.000 monedas con `p = 0,6` y `n = 50`, la desviación típica del MLE sale 0,0691 y su
  media 0,5995: la teoría asintótica acierta ya con `n = 50`.

Segundo caso, la regresión. Con 60 puntos de `y = 0,5·x + ruido(0; 1)`, el MLE de la pendiente es
**0,3385** en la muestra simulada, idéntico al de mínimos cuadrados. Y el MLE de `σ²` es **0,9130**
frente a **0,9445** del insesgado: el MLE divide por `n` y paga el sesgo de siempre.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(0, 1, size=40)
y = 0.5 * x + rng.normal(0, 1, size=40)

# Verosimilitud de una Bernoulli: n = 50 lanzamientos con 30 caras
n, exitos = 50, 30
p_mle = exitos / n
log_ver = exitos * np.log(p_mle) + (n - exitos) * np.log(1 - p_mle)
print(f"p MLE                  {p_mle:.4f}")        # -> 0.6000
print(f"log-verosimilitud      {log_ver:.3f}")      # -> -33.651

# La derivada de la log-verosimilitud en el maximo debe ser cero
h = 1e-6
def lv(p):
    return exitos * np.log(p) + (n - exitos) * np.log(1 - p)
print(f"derivada en el maximo  {(lv(p_mle + h) - lv(p_mle - h)) / (2 * h):.6f}")  # -> 0.000000

# Error tipico asintotico a partir de la informacion de Fisher: I(p) = n / (p(1-p))
error_tipico = np.sqrt(p_mle * (1 - p_mle) / n)
print(f"error tipico asintotico {error_tipico:.4f}")  # -> 0.0693

# Comprobacion por simulacion: el MLE de una moneda con p = 0,6 y n = 50
ps = rng.binomial(n, 0.6, size=20000) / n
print(f"desviacion simulada del MLE {ps.std(ddof=1):.4f}")  # -> 0.0691
print(f"media simulada del MLE      {ps.mean():.4f}")       # -> 0.5995
```

:::claves
- Las dos primeras líneas del bloque (`x = rng.normal(...)` y `y = 0.5 * x + ...`) no se usan después: el ejemplo continúa con la moneda. Además de sobrar, consumen números del generador, así que borrarlas cambiaría el valor de `ps` sin tocar ninguna línea de la parte de la moneda.
- `p_mle = exitos / n` con dos enteros da `0.6` en Python 3, pero `exitos // n` daría `0`: la barra doble es división entera. Con arrays de NumPy la diferencia es la misma y no avisa, así que conviene mirar el tipo del resultado cuando el número parece redondo.
- `(lv(p_mle + h) - lv(p_mle - h)) / (2 * h)` es una derivada numérica centrada: el error baja como `h²`, pero si `h` es demasiado pequeña la resta de dos números casi iguales se come los dígitos y sale ruido. Con `h = 1e-6` el resultado es 0,000000 porque el máximo está exactamente en 0,6; con `h = 1e-12` verías un valor arbitrario.
- `def lv(p)` usa `exitos` y `n` del ámbito global, no los recibe como argumento. Cambiar `n` en cualquier línea anterior cambia la función sin tocarla, y eso es cómodo aquí y una fuente de errores en un fichero largo.
- `rng.binomial(n, 0.6, size=20000) / n` produce los 20.000 MLE de una vez: la división convierte el array de enteros en `float` y `ps.std(ddof=1)` aplica la corrección de Bessel. Ese `ddof=1` está bien aquí (son réplicas de un experimento) y estaría mal si `ps` fuera la población completa.
- `ps.mean()` sale 0,5995 y no 0,6 exacto, aunque el MLE de una Bernoulli es insesgado: la media teórica de las réplicas es exactamente 0,6 y la diferencia es ruido de Monte Carlo. Compárala con el error típico asintótico `√(p(1−p)/n)`: 0,0691 medido frente a 0,0693 teórico, y esa coincidencia es lo que dice la teoría asintótica.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(2)
x = rng.normal(0, 1, size=60)
y = 0.5 * x + rng.normal(0, 1, size=60)
xc, yc = x - x.mean(), y - y.mean()

# El MLE de la pendiente coincide con el minimo cuadratico
pendiente = (xc @ yc) / (xc @ xc)
print(f"pendiente MLE/OLS {pendiente:.4f}")   # -> 0.3385
print(f"polyfit           {np.polyfit(x, y, 1)[0]:.4f}")  # -> 0.3385

# Con ruido normal, la log-verosimilitud depende solo del ECM de los residuos
residuos = yc - pendiente * xc
print(f"ECM               {(residuos ** 2).mean():.4f}")  # -> 0.9130

# El MLE de sigma^2 divide por n; el insesgado de Bessel por n-2
print(f"MLE de sigma^2    {(residuos ** 2).mean():.4f}")   # -> 0.9130
print(f"insesgado         {(residuos ** 2).sum() / (x.size - 2):.4f}")  # -> 0.9445
```

El segundo bloque muestra por qué «mínimos cuadrados» y «máxima verosimilitud con ruido
gaussiano» son la misma frase. `polyfit` y la fórmula del MLE dan 0,3385 con los mismos datos.

```python ilustrativo
# La perdida de la regresion logistica ES una log-verosimilitud negativa.
# Se escribe aqui como formula: no se ejecuta porque necesita datos reales.
#   L(beta)   = prod_i  p_i^y_i * (1 - p_i)^(1 - y_i)
#   -log L    = -sum_i [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]
#   con p_i   = 1 / (1 + exp(-x_i . beta))
# Minimizar -log L es lo que hace sklearn.linear_model.LogisticRegression.
```

## Errores típicos

- **Leer `L(θ)` como una probabilidad de `θ`.** La verosimilitud no es una distribución sobre el
  parámetro: no integra 1 y no se puede decir «hay un 70 % de probabilidad de que `p` sea 0,6». Eso
  exige un prior y da un posterior, que es el tema de [[estimacion-bayesiana-map]].
- **Confundir el MLE de la varianza con el insesgado.** `σ̂²` divide por `n`. Si copias la fórmula
  del MLE a un sitio donde esperabas insesgadez, subestimas la varianza un factor `(n − 1)/n`: con
  `n = 10` es un 10 % menos, y con `n = 5` un 20 %.
- **Aplicar la invarianza a la insesgadez.** `g(θ̂)` es el MLE de `g(θ)`, pero `E[g(θ̂)]` no tiene
  por qué ser `g(θ)`. El caso clásico: `s` (raíz de la varianza insesgada) es un estimador sesgado
  de `σ`.
- **Usar MLE con separación perfecta en clasificación.** Si una variable separa las clases por
  completo, la log-verosimilitud crece sin límite al empujar el coeficiente a infinito: el MLE **no
  existe** como número finito. Por eso la logística siempre lleva regularización.
- **Ignorar los supuestos del modelo al escribir la verosimilitud.** Toda la maquinaria depende de
  haber declarado bien la distribución: si los datos tienen colas gruesas y usas una normal, el MLE
  es el estimador equivocado para el problema correcto, y con datos extremos se va lejos.
- **Confundir el máximo de `ℓ` con un resultado significativo.** Que `p = 0,6` sea lo más
  verosímil con 50 lanzamientos no descarta `p = 0,5`: la muestra es solo 2,7 veces más probable
  bajo el primero, y eso es poco. El MLE da un punto, no una decisión; para decidir hacen falta
  [[intervalos-de-confianza]] o un [[contraste-de-hipotesis]].

:::truco
Antes de derivar, escribe la log-verosimilitud y **dónde** está definida. Los errores más caros
salen de olvidar el dominio: `log p` con `p ≤ 0`, o `log(1 − p)` con `p ≥ 1`. Y comprueba siempre
la segunda derivada: una raíz de `ℓ' = 0` puede ser un mínimo (con verosimilitudes multimodales,
pasa).
:::

:::practica
enunciado: Lanzas una moneda 20 veces y salen 8 caras. Calcula el MLE de p, compara la log-verosimilitud en ese valor y en p = 0,5, y da el error típico asintótico.
pista: El MLE de una Bernoulli es k/n, y el error típico sale de la información de Fisher, n/(p(1 − p)).
solucion: p̂ = 8/20 = 0,4. ℓ(0,4) = 8·ln 0,4 + 12·ln 0,6 = −7,330 − 6,130 = −13,460. ℓ(0,5) = 20·ln 0,5 = −13,863. La diferencia es 0,403, así que los datos son e^0,403 ≈ 1,50 veces más probables con p = 0,4 que con p = 0,5: hay indicio, no prueba. Error típico = √(0,4·0,6/20) = √0,012 = 0,110.
:::

## Comprueba que lo sabes

:::quiz
p: Lanzas una moneda 10 veces y salen 7 caras. ¿Cuál es el MLE de la probabilidad de cara?
o: 0,5, porque es la hipótesis por defecto de una moneda justa
o: 0,7, porque es la proporción observada
o: 0,636, porque hay que corregir con la regla de Laplace
a: 2
e: El MLE de una Bernoulli es la proporción de éxitos, 7/10 = 0,7. El 0,5 es una creencia previa, no un resultado de los datos, y 0,636 saldría de añadir pseudo-cuentas, que es una estimación bayesiana con prior, no el MLE.
:::

:::quiz
p: ¿Qué relación hay entre la pérdida de entropía cruzada de la regresión logística y la máxima verosimilitud?
o: Son dos criterios distintos que casualmente dan resultados parecidos
o: La entropía cruzada es exactamente el negativo de la log-verosimilitud de un modelo Bernoulli, así que minimizarla es maximizar la verosimilitud
o: La entropía cruzada solo se usa cuando el MLE no tiene solución
a: 2
e: Para cada observación con etiqueta y y probabilidad predicha p, la log-verosimilitud Bernoulli es y·log p + (1 − y)·log(1 − p), y su negativo es la entropía cruzada. No es una coincidencia: es el mismo problema escrito con otro nombre.
:::

:::quiz
p: Con n = 5 observaciones, ¿por qué el MLE de la varianza subestima σ² y por qué el estimador de Bessel lo arregla?
o: Porque el MLE divide por n y E[s²ₙ] = σ²(n − 1)/n; dividir por n − 1 elimina ese sesgo exacto
o: Porque el MLE no es consistente y hay que corregirlo a mano
o: Porque con pocos datos la varianza muestral es siempre cero
a: 1
e: El sesgo es exacto: (n−1)/n, un 20 % con n = 5. Dividir por n−1 lo cancela. El MLE sigue siendo consistente, y su ventaja es que también es el estimador de máxima verosimilitud de σ², con mejor ECM en muchos casos; sencillamente no es insesgado.
:::
