---
id: distribucion-normal-multivariante
titulo: Distribución normal multivariante
fase: 1
nivel: intermedio
rutas: [ds, core]
prerequisitos: [distribuciones-continuas, covarianza-y-correlacion, operaciones-matriciales, variable-aleatoria]
tags: [probabilidad, multivariante, covarianza, mahalanobis]
resumen: Modela varias variables que se mueven juntas cuando cada una es normal, y explica por qué la correlación cambia la probabilidad conjunta sin tocar las marginales.
fuentes: ["Anderson (1958), 'An Introduction to Multivariate Statistical Analysis'", "DeGroot y Schervish (2012), 'Probability and Statistics', 4ª ed.", "NIST/SEMATECH, 'e-Handbook of Statistical Methods', sección 1.3.5.4"]
---

## En una frase

La distribución normal multivariante describe cómo se comportan varias variables normales a la
vez, y guarda toda la información sobre su dependencia en una sola matriz: la de covarianzas.

## La idea

Una normal de una variable se describe con dos números: dónde está el centro y cuánto se abre.
Con varias variables, esos dos números no bastan. Imagina que mides la altura y el peso de mil
personas. Cada una por separado es más o menos normal: alturas alrededor de 170 cm, pesos
alrededor de 70 kg. Pero si solo guardas esas dos campanas no has guardado nada del hecho de que
la gente alta pesa más. La probabilidad de encontrar a alguien de 195 cm y 45 kg no es el
producto de dos campanas: es muchísimo más pequeña, porque esa combinación casi no existe.

La normal multivariante resuelve exactamente eso: es la campana de una variable, pero en varias
dimensiones, y con una pieza extra que dice **cómo se inclina** la nube. Esa pieza es la matriz
de covarianzas `Σ`. En dos dimensiones se ve como una elipse inclinada: si la correlación es
positiva, la elipse se tumba hacia arriba a la derecha; si es cero, los ejes de la elipse están
alineados con los ejes de coordenadas; y si es 1 o −1, la elipse se aplasta hasta convertirse en
una línea recta, porque una variable es función exacta de la otra.

Hay una forma de mirarlo que vale para cualquier número de dimensiones. En una normal de una
variable, medir «cuán lejos del centro está un punto» se hace con el z-score:
`(x − μ) / σ`. En varias dimensiones no puedes dividir por una desviación típica porque hay
muchas direcciones, y cada dirección tiene su propia anchura. La normal multivariante usa la
**distancia de Mahalanobis**: primero rota el espacio para alinear los ejes de la elipse con los
ejes de coordenadas y luego divide cada eje por su anchura. En ese espacio rotado y escalado, la
nube vuelve a ser una esfera de radio 1 y el problema se ha convertido otra vez en el de una
variable. Ese es el truco que hace que la fórmula de la densidad sea tan compacta.

Las consecuencias prácticas son tres, y las tres sorprenden a quien llega de la estadística de
una variable:

- Cada variable por separado sigue siendo normal, con su media y su varianza. A eso se le llama
  **marginal**, y no depende de las correlaciones: sales de la normal multivariante mirando solo
  una coordenada.
- Cualquier combinación lineal de las variables es también normal. En particular, la suma sigue
  siendo normal, y su varianza no es la suma de varianzas: lleva un término extra por cada par,
  `2·cov`. Si dos activos están muy correlacionados, la cartera no reduce riesgo, lo multiplica.
- Si condicionas una variable a que las demás tomen un valor concreto, la distribución que queda
  vuelve a ser normal, con una media que se desplaza y una varianza que **encoge**. Cuanto más
  correlacionadas estén, más encoge: ver el peso de alguien te dice mucho de su altura.

Y una advertencia desde el principio: normal cada una no implica normal conjunta. Puedes tener
dos variables marginales perfectamente normales cuya nube tenga forma de plátano, de ocho o de
dos montones. La normal multivariante es una hipótesis más fuerte que «cada una es normal», y esa
hipótesis es la que hace que funciones todo lo que viene después.

## Definición formal

Un vector aleatorio `X` de `p` componentes sigue una normal multivariante con vector de medias
`μ` y matriz de covarianzas `Σ` si su función de densidad es

:::formula
f(x) = (2π)^(−p/2) · det(Σ)^(−1/2) · exp( −½ · (x − μ)ᵀ Σ⁻¹ (x − μ) )
:::

- `X` — el vector de las `p` variables que mides juntas, `X = (X₁, …, X_p)`.
- `p` — número de variables del vector, la dimensión del problema.
- `x` — un punto concreto del espacio, el valor del que quieres la densidad.
- `μ` — vector de medias, `E[X]`. Marca el centro de la nube; sus unidades son las de cada
  variable.
- `Σ` — matriz de covarianzas, de tamaño `p × p`. En la diagonal lleva las varianzas
  `Var(Xᵢ)` y fuera de la diagonal las covarianzas `Cov(Xᵢ, Xⱼ)`. Es simétrica y
  semidefinida positiva; para que la densidad exista tiene que ser **invertible**
  (`det(Σ) > 0`).
- `(x − μ)ᵀ Σ⁻¹ (x − μ)` — la distancia de Mahalanobis al cuadrado. Es un número sin unidades:
  mide cuántas «desviaciones típicas conjuntas» está el punto del centro, en la dirección en la
  que se mida.
- `det(Σ)` — determinante de la matriz de covarianzas. Es el **volumen** de la nube al cuadrado:
  cuanto más grande, más dispersa y más plana es la densidad, y su altura máxima baja.
- `Σ⁻¹` — matriz inversa. Existe solo si ninguna variable es combinación lineal exacta de las
  demás y ninguna tiene varianza cero.

**Notación:** `X ~ N_p(μ, Σ)`.

Dos propiedades que se usan constantemente y conviene tener a mano:

:::formula
aᵀX ~ N(aᵀμ, aᵀΣa)   para cualquier vector a de constantes
:::

Es decir: cualquier combinación lineal es normal, y su varianza se calcula con la forma
cuadrática `aᵀΣa`. Con `p = 2` y `a = (1, 1)ᵀ` sale `Var(X₁ + X₂) = σ₁² + σ₂² + 2·σ₁₂`, donde
`σ₁₂` es la covarianza. Si es positiva, sumar variables **aumenta** la varianza por encima de la
suma de varianzas.

La otra propiedad es el condicionamiento. Partiendo el vector en dos bloques, `X₁` y `X₂`:

:::formula
X₁ dado X₂ = x₂ sigue una normal con media μ₁ + Σ₁₂ Σ₂₂⁻¹ (x₂ − μ₂) y covarianza Σ₁₁ − Σ₁₂ Σ₂₂⁻¹ Σ₂₁
:::

- `Σ₁₂` — bloque de covarianzas entre el primer grupo de variables y el segundo.
- `Σ₂₂` — matriz de covarianzas del bloque que condiciona.
- `Σ₁₂ Σ₂₂⁻¹ (x₂ − μ₂)` — el ajuste de la media: lo que aprendes del bloque `x₂` y repartes
  hacia `x₁` según la correlación.
- `Σ₁₁ − Σ₁₂ Σ₂₂⁻¹ Σ₂₁` — la covarianza condicional, que siempre es menor o igual que `Σ₁₁`.
  Observar algo nunca aumenta la incertidumbre sobre otra cosa que está correlacionada con ello.

:::parametros
| Símbolo | Qué es | Unidades | Si sube |
| --- | --- | --- | --- |
| `μ` | Centro de la nube, una media por variable | las de cada variable | La nube entera se desplaza; la forma, el volumen y todas las probabilidades relativas quedan igual. Un test sobre `μ` cambia de resultado, la densidad en un punto relativo no |
| `Σ` | Matriz de covarianzas `p × p`: varianzas en la diagonal, covarianzas fuera | las de las variables al cuadrado | La nube se ensancha y `det(Σ)` crece, así que la altura máxima de la densidad baja: la probabilidad se reparte por más volumen. Los contornos se estiran y se inclinan según qué celdas suban |
| `det(Σ)` | Volumen de la nube al cuadrado, dentro de la constante de normalización | las de las variables elevadas a `p` | Sube la constante `det(Σ)^(−1/2)`, que divide: la densidad es más baja y más plana, porque el mismo 1 de probabilidad ocupa más sitio |
| `Σ⁻¹` | Matriz de precisión: cómo se convierte una diferencia en distancia | inversa de las unidades de `Σ` | Con la misma diferencia `x − μ`, un valor más alto en la dirección del punto da una Mahalanobis mayor y una densidad exponencialmente menor: castiga más alejarse por donde la nube es estrecha |
| `ρ` | Correlación entre dos variables, `σ₁₂ / (σ₁·σ₂)`, de −1 a 1 | adimensional | La elipse se inclina y se estrecha. Las marginales no cambian, pero cambia la probabilidad conjunta: sube la de «las dos altas a la vez» y la de «una alta y otra baja». En el límite, `ρ = ±1` aplasta la nube a una recta y `det(Σ) = 0`: la densidad no existe |
| `p` | Número de variables del vector | variables | Los grados de libertad de la chi-cuadrado de la Mahalanobis al cuadrado suben con `p`, así que un mismo valor de distancia es menos extremo. El número de parámetros de `Σ` crece como `p(p+1)/2` y se come los datos: con `p = 100` son 5050 números que estimar |
:::

Una consecuencia que se usa muchísimo: si `X ~ N_p(μ, Σ)` y `Σ` es invertible, entonces la
distancia de Mahalanobis al cuadrado sigue una ji-cuadrado con `p` grados de libertad.

:::formula
(x − μ)ᵀ Σ⁻¹ (x − μ) ~ χ²_p
:::

Eso es lo que permite dibujar los contornos de la elipse a un nivel de confianza dado y detectar
puntos atípicos **teniendo en cuenta la correlación**: un peso de 95 kg no es raro en alguien de
190 cm, pero es rarísimo en alguien de 160 cm.

:::figura
fichero: normal-multivariante-elipse-y-conjunta
pie: A la izquierda, los contornos de la nube con varianzas 4 y 9 y correlación 0,70. Los puntos (2, 3) y (−2, −3) caen sobre la misma elipse, así que tienen la misma distancia de Mahalanobis (1,176) y exactamente la misma densidad (0,0206); el punto (4, 6) está en la misma dirección pero más lejos, y su densidad cae a 0,0035: unas seis veces menos que en (2, 3) y diez veces menos que en el centro. La línea roja discontinua es la dirección principal de la nube. A la derecha, con las mismas marginales en los tres casos, la probabilidad de que las dos variables se queden por debajo de 2 pasa de 0,629 a 0,741 solo cambiando la correlación de 0 a 0,95.
fuente: figuras/distribucion-normal-multivariante-1.py
:::

## Ejemplo

Dos variables, `X₁` (por ejemplo, la nota de un examen práctico) y `X₂` (la del teórico), con

```text
μ = (0, 0)        Σ = [ 4,0   4,2 ]
                      [ 4,2   9,0 ]
```

La primera variable tiene desviación típica 2, la segunda 3, y la covarianza es 4,2, así que la
correlación es `ρ = 4,2 / (2 · 3) = 0,70`. El determinante es
`det(Σ) = 4,0 · 9,0 − 4,2² = 36,00 − 17,64 = 18,36`, luego `Σ` es invertible y la densidad
existe. La constante de normalización vale

`(2π)^(−2/2) · det(Σ)^(−1/2) = 1 / (2π · √18,36) = 1 / (6,2832 · 4,2849) = 0,037144`.

Ahora tres puntos, para ver qué hace la Mahalanobis:

- **El centro, `x = (0, 0)`.** La Mahalanobis es 0 y la densidad es la constante: **0,037144**,
  el máximo.
- **`x = (2, 3)`.** El punto está a una desviación típica de cada media, en la dirección
  correcta. La distancia de Mahalanobis al cuadrado es 1,176, así que la densidad es
  `0,037144 · e^(−1,176/2)` = **0,020626**. Menos de la mitad que en el centro, y eso que el
  punto no parece lejos.
- **`x = (4, 6)`.** Dos desviaciones típicas de cada media, otra vez en la dirección de la
  correlación. Mahalanobis al cuadrado 4,706 y densidad **0,003532**: una décima parte del
  centro.

Fíjate en que el punto `(4, 6)` está «fuera» de la nube pero no es imposible: la densidad ha
caído un factor 10, no a cero. Lo que sí sería casi imposible es `(4, −6)`, con la misma
distancia a los ejes pero en la dirección contraria a la correlación.

Y el efecto de la correlación en una probabilidad conjunta, que es donde de verdad se nota.
Todos estos casos tienen las **mismas** marginales (`σ₁ = 2`, `σ₂ = 3`); lo único que cambia es
`ρ`:

```text
ρ = 0,00   densidad en (3; 4,5) = 0,002796   P(X₁ < 2 y X₂ < 2) = 0,6289
ρ = 0,70   densidad en (3; 4,5) = 0,009887   P(X₁ < 2 y X₂ < 2) = 0,6989
ρ = 0,95   densidad en (3; 4,5) = 0,026795   P(X₁ < 2 y X₂ < 2) = 0,7408
```

Con `ρ = 0,95` la densidad en un punto bastante alejado es **casi diez veces** la del caso
independiente. La correlación no mueve las campanas de cada variable: mueve la probabilidad de
que las dos se muevan a la vez. Quien modele dos variables como independientes cuando tienen
`ρ = 0,95` va a asignar a los escenarios conjuntos probabilidades equivocadas por un factor 10.

## Código

```python verificable
import numpy as np
from scipy import stats

mu = np.array([0.0, 0.0])
S = np.array([[4.0, 4.2], [4.2, 9.0]])          # varianzas 4 y 9, covarianza 4,2
d = stats.multivariate_normal(mean=mu, cov=S)

print(f"det {np.linalg.det(S):.2f}  rho {S[0, 1] / np.sqrt(S[0, 0] * S[1, 1]):.2f}")
# -> det 18.36  rho 0.70
for x in ([0.0, 0.0], [2.0, 3.0], [4.0, 6.0]):
    m2 = float(np.array(x) @ np.linalg.inv(S) @ np.array(x))   # Mahalanobis al cuadrado
    print(f"{x}  mahalanobis2 {m2:.3f}  densidad {d.pdf(x):.6f}")
# -> [0.0, 0.0]  mahalanobis2 0.000  densidad 0.037144
# -> [2.0, 3.0]  mahalanobis2 1.176  densidad 0.020626
# -> [4.0, 6.0]  mahalanobis2 4.706  densidad 0.003532
```

:::claves
- `stats.multivariate_normal(mean=..., cov=...)` devuelve un **objeto** con métodos `.pdf(x)`,
  `.cdf(x)` y `.rvs(size=n)`. No es una función suelta como `stats.norm.pdf`. `.pdf` acepta una
  lista de Python y la convierte en array, así que `d.pdf(x)` y `d.pdf(np.array(x))` dan lo
  mismo; pero el orden de las coordenadas es el de `mean`, y equivocarse de orden no da ningún
  error, solo un número distinto.
- La covarianza va en **unidades al cuadrado**, no en correlaciones: `[[4.0, 4.2], [4.2, 9.0]]`
  no es `[[1, 0.7], [0.7, 1]]`. Si pasas la matriz de correlaciones, la densidad sale mal y no
  avisa. Para convertir: `S = np.outer(sd, sd) * R`, con `sd = np.sqrt(np.diag(S))`.
- `x @ np.linalg.inv(S) @ x` escribe la forma cuadrática a mano y sirve para comprobar que la
  densidad es la constante por la exponencial. `np.linalg.solve(S, x)` es mejor que
  `np.linalg.inv(S) @ x` cuando solo necesitas el producto: no calcula la inversa entera y con
  matrices mal condicionadas comete menos error.
- `.cdf` en dimensión mayor que 2 no tiene fórmula cerrada: SciPy lo calcula por integración
  numérica y se vuelve lento y frágil. Con `p = 2` y la identidad, `d.cdf([0.0, 0.0])` da
  exactamente 0,25, que es el producto de dos normales estándar (comprobado). Con `p = 10` el
  mismo cálculo puede tardar segundos y avisar por falta de precisión. Si necesitas
  probabilidades conjuntas en dimensión alta, usa Monte Carlo, no `.cdf`.
- `np.linalg.det(S)` con una matriz de covarianzas mal construida puede salir negativo o
  diminuto por error de redondeo, y ahí `multivariate_normal` lanza un aviso o falla. Si una
  variable es combinación lineal exacta de otra, la matriz no es invertible y la densidad no
  existe: eso no es un fallo del programa, es que el modelo está mal planteado.
- `d.pdf(x)` devuelve un `np.float64` y no comprueba que `x` esté en el soporte: fuera del rango
  devuelve números muy pequeños, nunca un error. Un valor de `1e-300` no significa «imposible»,
  significa «densidad muy baja».
:::

```python verificable
import numpy as np
from scipy import stats

# La Mahalanobis al cuadrado se comporta como una ji-cuadrado con p grados de libertad.
rng = np.random.default_rng(0)
mu = np.array([0.0, 0.0])
S = np.array([[4.0, 4.2], [4.2, 9.0]])
Sinv = np.linalg.inv(S)

X = rng.multivariate_normal(mu, S, size=200000)
m2 = np.einsum("ij,jk,ik->i", X, Sinv, X)        # una Mahalanobis por fila, sin bucle
corte = stats.chi2.ppf(0.95, df=2)
print(f"P(mahalanobis2 < {corte:.3f})  simulada {(m2 < corte).mean():.3f}  teorica 0.950")
# -> P(mahalanobis2 < 5.991)  simulada 0.950  teorica 0.950
print(f"proporcion de puntos fuera de la elipse del 95 %: {(m2 > corte).mean():.3f}")
# -> proporcion de puntos fuera de la elipse del 95 %: 0.050

# Sumar dos variables correlacionadas NO es sumar sus varianzas.
a = np.ones(2)
print(f"sd de la suma {np.sqrt(a @ S @ a):.4f}  suma de sd {np.sqrt(S[0, 0]) + np.sqrt(S[1, 1]):.4f}")
# -> sd de la suma 4.6260  suma de sd 5.0000
```

El último número es el que importa: la desviación típica de `X₁ + X₂` es 4,626 y no 5, porque la
covarianza entra en la cuenta. Ignorar la correlación aquí no es un matiz: es un error del 8 %
en la volatilidad, y del 16 % en la varianza.

## Errores típicos

- **Confundir la matriz de covarianzas con la de correlaciones.** `stats.multivariate_normal`
  no valida nada: si le pasas `[[1, 0.7], [0.7, 1]]` creyendo que son varianzas 4 y 9, te
  devuelve densidades perfectamente plausibles y equivocadas. Comprueba siempre que la diagonal
  sea lo que crees.
- **Creer que «cada variable es normal» implica normal multivariante.** No es cierto y es la
  fuente de la mitad de los problemas con cópulas y con datos financieros. Hay nubes con
  marginales normales y forma de plátano. Si vas a usar propiedades conjuntas (condicionar,
  simular, calcular intervalos elípticos), comprueba la normalidad conjunta, no la de cada eje.
- **Estimar `Σ` con `p` grande.** La matriz tiene `p(p+1)/2` parámetros libres: con 50 variables
  son 1275 números y necesitas bastantes más de 1275 observaciones para que `Σ` sea invertible.
  Más allá de eso, la inversa existe pero es basura numérica y la distancia de Mahalanobis se
  vuelve ruido. Alternativas: regularización (encoger la matriz hacia la diagonal), componentes
  principales o trabajar con la correlación en vez de la covarianza.
- **Usar Mahalanobis con `Σ` estimada en los mismos datos con los que detectas atípicos.** La
  media y la covarianza muestrales ya están tiradas hacia el punto raro que quieres encontrar.
  Con `n` pequeño, la distancia de un punto siempre parece menor de lo que es. Usa estimadores
  robustos (MCD) o reglas basadas en la mediana.
- **Olvidar que la correlación cero no es independencia.** En la normal multivariante, `Σ`
  diagonal sí implica independencia, y eso es una excepción cómoda del caso normal. Fuera de la
  normal, correlación cero no dice nada.
- **Simular con `np.random.multivariate_normal` y una `Σ` que no es semidefinida positiva.**
  NumPy avisa (`covariance is not symmetric positive-semidefinite`) pero sigue devolviendo
  números si puede. Si la matriz la has estimado tú, comprueba
  `np.all(np.linalg.eigvalsh(S) > 0)` antes de simular nada.

:::aviso
La normal multivariante es cómoda pero muy restrictiva: impone que los contornos sean elipses y
que las colas decaigan como una exponencial del cuadrado. En datos financieros con colas gruesas
o en carteras con opciones, infravalora los sucesos conjuntos extremos justo cuando más importa.
Para eso se usan cópulas, que separan las marginales de la dependencia.
:::

:::practica
enunciado: Dos sensores miden la misma magnitud. Sus errores son conjuntamente normales con μ = (0, 0), varianzas 1,0 y 4,0 y covarianza 1,2. Calcula la correlación, la varianza de la media de los dos errores, y decide si promediar los sensores reduce el error respecto de usar solo el primero.
pista: La media es la combinación lineal con a = (0,5; 0,5), y su varianza es aᵀΣa, no la media de las varianzas.
solucion: ρ = 1,2 / (1,0 · 2,0) = 0,60. La varianza de la media es 0,25·1,0 + 0,25·4,0 + 2·0,25·1,2 = 0,25 + 1,00 + 0,60 = 1,85. Con un solo sensor la varianza es 1,0, así que promediar EMPEORA: 1,85 frente a 1,0. El segundo sensor es tan malo (varianza 4) que arrastra, y la correlación positiva impide que los errores se cancelen. La varianza de la media solo baja por debajo de 1,0 si la covarianza es menor que 0,5·(1,0 + 4,0) − 2·1,0 = −0,5, es decir, si los errores están correlacionados negativamente.
:::

## Comprueba que lo sabes

:::quiz
p: Dos variables tienen marginales normales estándar, con varianza 1 cada una y correlación 0,9. ¿Cuál es la varianza de su suma?
o: 2,0, porque las varianzas se suman
o: 3,8, porque 1 + 1 + 2 · 0,9
o: 1,0, porque la correlación reduce la varianza
a: 2
e: La varianza de una suma es σ₁² + σ₂² + 2·ρ·σ₁·σ₂ = 1 + 1 + 2·0,9 = 3,8. Sumar variables correlacionadas positivamente AUMENTA la varianza por encima de la suma de varianzas. La opción de 1,0 describe el caso de correlación −0,5, donde los términos cruzados cancelan parte de la suma.
:::

:::quiz
p: ¿Qué mide la distancia de Mahalanobis al cuadrado de un punto a la media?
o: La distancia euclídea al cuadrado, en unidades de la variable
o: Cuántas desviaciones típicas conjuntas está el punto, contando la dirección y la correlación entre variables
o: La probabilidad de que ese punto ocurra
a: 2
e: Mahalanobis rota el espacio según los ejes de la nube y luego divide cada dirección por su anchura, así que es una distancia en desviaciones típicas que tiene en cuenta la correlación. No es una probabilidad: para pasar de ella a una probabilidad hace falta la ji-cuadrado con p grados de libertad, y aun así eso da la probabilidad de la elipse, no la de un punto (que siempre es cero en una variable continua).
:::

:::quiz
p: Tienes tres variables con correlaciones altas y quieres probabilidades conjuntas del tipo P(X₁ < a, X₂ < b, X₃ < c). ¿Qué haces?
o: Multiplicar las tres probabilidades marginales
o: Usar stats.multivariate_normal(...).cdf y confiar en el resultado
o: Simular con rvs y contar la proporción de veces que se cumple la condición
a: 3
e: Multiplicar supone independencia y con correlaciones altas da un resultado muy equivocado. El .cdf de SciPy integra numéricamente y en dimensión mayor que 2 se vuelve lento y poco fiable (en dimensión 2 y con la identidad da exactamente 0,25, pero eso no se generaliza). Con Monte Carlo controlas el error por el número de simulaciones y funciona en cualquier dimensión.
:::
