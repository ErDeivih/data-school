---
id: supuestos-de-la-regresion
titulo: Supuestos de la regresión
fase: 6
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [regresion-lineal, varianza-y-desviacion, contraste-de-hipotesis]
tags: [diagnostico, supuestos, inferencia]
resumen: Linealidad, independencia, homocedasticidad y normalidad: qué rompe cada supuesto, qué sigue funcionando y cómo se diagnostica.
fuentes: ["White (1980), 'A Heteroskedasticity-Consistent Covariance Matrix Estimator'", "Wooldridge (2020), 'Introductory Econometrics'"]
---

## En una frase

Los supuestos de la regresión no son un ritual: cada uno sostiene una promesa distinta, y
saber cuál falla te dice si el problema está en los coeficientes (que salen sesgados) o solo en
los errores estándar y los contrastes (que dejan de ser válidos aunque el coeficiente siga
siendo razonable).

## La idea

Cuando ajustas una regresión por mínimos cuadrados, la fórmula `β = (XᵀX)⁻¹Xᵀy` devuelve
siempre un número, con datos buenos y con datos malos. Los supuestos existen para responder a
la pregunta: ¿ese número se parece a lo que quieres estimar?

Piensa en una báscula. Si está bien calibrada, el peso que marca es el peso real. Si el muelle
está vencido, marca siempre 2 kilos de más: ese es el **sesgo**, un error sistemático que no
desaparece por tomar más medidas. Y si la aguja tiembla mucho, el peso medio puede estar bien
pero cada lectura individual es poco fiable: eso es la **varianza**, y se combate con más
datos o con mejores estimadores.

Los supuestos de la regresión se reparten justo entre esas dos cosas:

- Los que garantizan que los coeficientes son **insesgados**: linealidad en los parámetros,
  error con media cero y no correlacionado con las predictoras, y ausencia de colinealidad
  perfecta.
- Los que garantizan que los errores estándar y los contrastes son **correctos**: varianza
  constante del error (homocedasticidad) e independencia entre observaciones.
- El que solo hace falta para que los contrastes sean exactos en muestras pequeñas:
  normalidad de los residuos.

Esta distinción es la que casi nadie hace y la que más tiempo ahorra. Si tus residuos son
heterocedásticos, el coeficiente estimado sigue siendo insesgado y consistente; lo que está
mal es el error estándar clásico, y con él el `t` y el `p`. La solución no es tirar el modelo,
es cambiar la fórmula del error estándar. En cambio, si el error está correlacionado con una
variable que te has dejado fuera, el coeficiente está sesgado y ninguna corrección de errores
estándar te salva.

## Definición formal

El modelo es `y = Xβ + ε`. Los supuestos habituales (condiciones de Gauss-Markov, más el
extra de normalidad) son:

| Supuesto | Qué afirma | Si falla |
| --- | --- | --- |
| Linealidad | `y` es una función lineal de los parámetros más un error | Sesgo por especificación: el modelo estima otra cosa |
| Exogeneidad | El error tiene media cero y no está correlacionado con las predictoras | Sesgo e inconsistencia en los coeficientes |
| Homocedasticidad | La varianza del error es la misma para toda observación | Coeficientes válidos, errores estándar clásicos incorrectos |
| Independencia | Los errores de dos observaciones no están correlacionados | Con series temporales, errores estándar muy subestimados |
| Normalidad de los residuos | Los errores siguen una normal | Los contrastes `t` y `F` dejan de ser exactos en muestras pequeñas |
| Sin colinealidad perfecta | Ninguna predictora es combinación lineal exacta de otras | `XᵀX` no es invertible y no hay solución única |

Con `n` el número de observaciones y `k` el número de predictoras, el error estándar clásico
del coeficiente `j` es `SE(b_j) = √( σ̂² · [(XᵀX)⁻¹]_jj )`, donde `σ̂²` es la varianza residual
estimada y `[(XᵀX)⁻¹]_jj` el elemento `j` de la diagonal de esa matriz inversa. Si la varianza
del error no es constante, esa `σ̂²` única no representa a nadie y el `SE` sale mal.

La alternativa es el estimador robusto de White (también llamado HC), que estima la varianza
usando los residuos al cuadrado de cada observación en lugar de una varianza común:

:::formula
Var_HC(b) = (XᵀX)⁻¹ · ( Σᵢ eᵢ² · xᵢ xᵢᵀ ) · (XᵀX)⁻¹
:::

- `eᵢ` — residuo de la observación `i`.
- `xᵢ` — vector de predictoras de la observación `i` (con el uno del intercepto).
- `Σᵢ eᵢ² xᵢxᵢᵀ` — suma exterior de los residuos al cuadrado, que recoge la heterocedasticidad.
- La variante HC3, la más usada con muestras pequeñas, corrige además cada `eᵢ²` por el apalancamiento
  (`eᵢ² / (1 − hᵢ)²`, con `hᵢ` el apalancamiento de esa observación).

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `eᵢ` | Residuo de la observación `i` | unidades de `y` | Al cuadrado pesa mas en la varianza robusta: una observación mal ajustada infla el error estandar |
| `xᵢ` | Vector de predictoras de la observación `i`, con el uno del intercepto | las de cada variable | Con heterocedasticidad, las filas con `x` grande dominan el calculo del error robusto |
| `σ̂²` | Varianza residual estimada, un solo número | unidades de `y` al cuadrado | El error estandar clasico sube con ella; si la varianza real no es constante, ese único número no representa a nadie |
| `hᵢ` | Apalancamiento: cuanto puede tirar esa fila de la recta | tanto por uno, de 0 a 1 | El residuo se divide entre `(1 − hᵢ)²`, así que las filas muy influyentes pesan mucho mas en HC3 |
| `n` | Numero de observaciones | filas | Los errores estandar bajan (mas información) y los contrastes ganan potencia |
| `k` | Numero de predictoras | columnas sin el intercepto | Cada variable de mas consume un grado de libertad y ensancha un poco los intervalos |
:::

## Ejemplo

Doscientos datos generados con `y = 2 + 0,8·x + ε`, donde la desviación típica de `ε` crece
como `0,02·x²`: para `x = 2` el error típico es 0,08 y para `x = 10` es 2,0. Veinticinco veces
más dispersión en un extremo que en el otro.

```
beta1   clasico 0.7435   robusto 0.7435
SE      clasico 0.0288   robusto 0.0316
t       clasico 25.83    robusto 23.50
```

El coeficiente es idéntico, como manda la teoría: la heterocedasticidad no sesga la pendiente.
Lo que cambia es el error estándar, y con él la confianza del contraste. El clásico, 0,0288, es
menor que el robusto, 0,0316: subestima la incertidumbre porque promedia una varianza que en
realidad depende de `x`. El `t` baja de 25,83 a 23,50. Aquí la conclusión no cambia, pero con
un efecto más pequeño y una heterocedasticidad más fuerte, ese cambio decide entre significativo
y no significativo.

Los contrastes formales sobre esos mismos datos:

```
Breusch-Pagan p 0.000007
Jarque-Bera  p 0.0000
```

El contraste de Breusch-Pagan rechaza varianza constante (`p` casi cero) y el de Jarque-Bera
rechaza normalidad. Y aquí está el matiz interesante: los errores que generé **sí** eran
normales, pero con varianzas distintas. Al mezclar normales de distinta varianza, los residuos
agregados salen con colas más gruesas y el contraste de normalidad lo detecta. Un
Jarque-Bera significativo no siempre significa «los datos no son normales», a veces significa
«hay heterocedasticidad».

:::figura
fichero: supuestos-embudo-y-error-estandar
pie: Los dos primeros paneles llevan la misma escala a propósito. En el primero, los residuos forman una nube sin forma y respetan las bandas punteadas: la varianza es constante. En el segundo, las mismas bandas fijas dejarían puntos fuera y la dispersión crece con x, veinticinco veces de un extremo al otro: ese embudo es la heterocedasticidad. El tercer panel es la consecuencia práctica: el coeficiente estimado es idéntico en los dos métodos, pero el intervalo del 95 % calculado con errores robustos HC3 es más ancho que el clásico. Como el coeficiente no se mueve y el error estándar sí, lo que estaba mal no era el ajuste sino la promesa de precisión.
fuente: figuras/supuestos-de-la-regresion-1.py
:::

## Código

```python verificable
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(0)
n = 200
x = rng.uniform(1, 10, size=n)
y = 2 + 0.8 * x + rng.normal(0, 0.02 * x ** 2)   # la varianza del error crece con x^2

X = sm.add_constant(x)                           # columna de unos para el intercepto
clasico = sm.OLS(y, X).fit()
# cov_type se pasa a fit(): el error estandar se calcula con los residuos al cuadrado
# de cada fila en vez de con una varianza comun.
robusto = sm.OLS(y, X).fit(cov_type="HC3")

print(f"beta1   clasico {clasico.params[1]:.4f}  robusto {robusto.params[1]:.4f}")
print(f"SE      clasico {clasico.bse[1]:.4f}  robusto {robusto.bse[1]:.4f}")
print(f"t       clasico {clasico.tvalues[1]:.2f}  robusto {robusto.tvalues[1]:.2f}")
# -> beta1   clasico 0.7435  robusto 0.7435
# -> SE      clasico 0.0288  robusto 0.0316
# -> t       clasico 25.83  robusto 23.50
```

:::claves
- `sm.OLS(y, X)` no añade el intercepto por su cuenta, a diferencia de casi todo lo demás. Sin
  `sm.add_constant(x)`, la recta se ve obligada a pasar por el origen y el coeficiente sale
  sesgado y mas grande. En `scikit-learn` es al revés: `LinearRegression` mete el intercepto
  salvo que le digas `fit_intercept=False`.
- `sm.add_constant(x)` devuelve un **array nuevo** con una columna de unos delante; `x` no se
  toca. Y si `x` ya tuviera una columna constante, por defecto la deja tal cual y no avisa
  nada: el `ValueError` por colinealidad perfecta solo salta con `has_constant="raise"`,
  porque dos columnas constantes hacen que `XᵀX` deje de ser invertible.
- `.fit()` devuelve un objeto de resultados y **no modifica** `y` ni `X`: puedes ajustar el
  mismo modelo con dos opciones distintas y comparar, como hace el ejemplo con `cov_type`.
- `clasico.params[1]` y `clasico.bse[1]` van por **posición**, no por nombre: el `0` es el
  intercepto y el `1` la primera predictora, porque `add_constant` la puso delante. Si cambiaras
  el orden de las columnas de `X`, el índice `1` pasaria a ser otra variable sin avisar.
- `cov_type="HC3"` es un argumento de `.fit()`, no del modelo: si lo pasas al constructor
  (`sm.OLS(y, X, cov_type="HC3")`) te lo ignora o falla. Es el error típico al copiar el ejemplo.
- `rng.normal(0, 0.02 * x ** 2)` genera un array de desviaciones **distintas por fila**, aunque
  `np.random.normal` también admita un solo número como desviación. Si escribieras
  `rng.normal(0, 0.02)`, la varianza sería constante y el ejemplo entero dejaria de tener sentido.
:::

```python verificable
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import jarque_bera

rng = np.random.default_rng(1)
n = 200
x = rng.uniform(1, 10, size=n)
y = 2 + 0.8 * x + rng.normal(0, 0.3 * x)     # error normal, pero de varianza creciente

X = sm.add_constant(x)
ajuste = sm.OLS(y, X).fit()

bp = het_breuschpagan(ajuste.resid, X)       # H0: varianza constante
jb = jarque_bera(ajuste.resid)               # H0: residuos normales
print(f"Breusch-Pagan p {bp[1]:.6f}")
print(f"Jarque-Bera  p {jb[1]:.4f}")
print(f"correlacion de los residuos con x: {np.corrcoef(ajuste.resid, x)[0, 1]:+.3f}")
# -> Breusch-Pagan p 0.000007
# -> Jarque-Bera  p 0.0000
# -> correlacion de los residuos con x: +0.000
```

## Errores típicos

- **Creer que sin normalidad los coeficientes están sesgados.** No lo están. La normalidad
  solo hace exactos los contrastes en muestras pequeñas; con `n` grande, el teorema central del
  límite hace que `t` y `F` funcionen igual. El supuesto que sí sesga es la exogeneidad.
- **Mirar el `R²` en lugar de los residuos.** Un `R²` alto es compatible con un patrón de
  embudo (heterocedasticidad) o con una curva (falta de linealidad). El diagnóstico se hace
  sobre los residuos frente a las predicciones y frente a cada predictora, no sobre el resumen.
- **Usar errores estándar clásicos con heterocedasticidad.** Es el error más caro y el más
  frecuente: el coeficiente está bien, el `p` está mal, y publicas una significación que no
  existe. Con datos heterocedásticos, usa errores robustos HC3 y dilo.
- **Ignorar la autocorrelación en series temporales.** Con datos ordenados en el tiempo, los
  residuos de meses consecutivos se parecen y el error estándar clásico puede quedar muy por
  debajo del real: aparecen `t` enormes de relaciones que no existen. Aquí hacen falta errores
  tipo Newey-West o directamente un modelo de series temporales.
- **Comprobar los supuestos sobre `y` en vez de sobre los residuos.** Lo que debe ser normal y
  homocedástico es el error, no la variable respuesta. Una `y` con distribución asimétrica es
  perfectamente compatible con una regresión correcta.
- **Eliminar puntos influyentes sin justificarlo.** Un solo punto con apalancamiento alto puede
  cambiar la pendiente. Hay que mirar medidas de influencia (distancia de Cook, apalancamiento)
  y decidir por criterio técnico: error de medición documentado o dato real que se queda.

:::practica
enunciado: Una regresión con 200 observaciones da β₁ = 0,15, con σ̂² = 0,25 y el elemento diagonal de (XᵀX)⁻¹ igual a 0,01. Un cálculo robusto HC3 da una varianza de 0,0064. ¿Sobrevive el efecto al contraste del 5 %, donde hace falta un t mayor que 1,96?
pista: El estadístico es el coeficiente entre su error estándar; compara las dos versiones y decide cuál vale cuando la varianza del error no es constante.
solucion: Clásico: SE = √(0,25 · 0,01) = 0,05, luego t = 0,15/0,05 = 3,0. Robusto: SE = √0,0064 = 0,08, luego t = 0,15/0,08 = 1,875, por debajo de 1,96. El coeficiente es idéntico, pero el error estándar clásico promediaba una varianza que no es constante y prometía una significación que no existe.
:::

## Comprueba que lo sabes

:::quiz
p: Tus residuos muestran un patrón de embudo claro y el contraste de Breusch-Pagan da p = 0,00001. ¿Qué está mal exactamente?
o: Los coeficientes estimados, que están sesgados
o: Los errores estándar clásicos y, con ellos, los contrastes de significación
o: Nada, porque la heterocedasticidad solo importa con muestras pequeñas
a: 2
e: La heterocedasticidad no sesga los coeficientes de mínimos cuadrados: siguen siendo insesgados y consistentes. Lo que invalida es el error estándar clásico, que supone una varianza común. Se corrige con errores robustos HC3 o con mínimos cuadrados ponderados.
:::

:::quiz
p: ¿Qué supuesto, si falla, hace que el coeficiente estime algo distinto de lo que quieres estimar?
o: La normalidad de los residuos
o: La homocedasticidad
o: La exogeneidad, es decir, que el error no esté correlacionado con las predictoras
a: 3
e: Si el error contiene una variable omitida que correlaciona con alguna predictora, el coeficiente recoge parte de ese efecto y está sesgado: más datos no lo arreglan. La normalidad y la homocedasticidad afectan a la inferencia, no al valor esperado del coeficiente.
:::

:::quiz
p: Ajustas una regresión con datos de 300 viviendas y los residuos no siguen una normal (Jarque-Bera con p = 0,01). ¿Qué haces?
o: Transformar la variable respuesta obligatoriamente, porque el modelo no vale
o: Seguir, porque con 300 observaciones el teorema central del límite sostiene los contrastes, y comprobar que no hay heterocedasticidad ni un patrón claro en los residuos
o: Pasar a un modelo no paramétrico, ya que la regresión exige normalidad exacta
a: 2
e: La normalidad de los residuos solo es necesaria para contrastes exactos con muestras pequeñas. Con n grande los contrastes son asintóticamente válidos. Lo que no se puede ignorar es un patrón en los residuos ni la heterocedasticidad, porque esos sí invalidan la inferencia.
:::
