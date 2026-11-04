---
id: regresion-lineal
titulo: Regresión lineal
fase: 6
nivel: básico
rutas: [core, ds]
prerequisitos: [notacion-matematica, medidas-de-centralidad, covarianza-y-correlacion]
tags: [modelos, minimos-cuadrados, prediccion]
resumen: Ajustar la recta que minimiza la suma de errores al cuadrado, leer sus coeficientes con sentido y no confundirla con causalidad.
fuentes: ["Gauss (1809), 'Theoria motus corporum coelestium'", "James et al. (2021), 'An Introduction to Statistical Learning'"]
---

## En una frase

La regresión lineal busca la recta (o el plano, o el hiperplano) que pasa lo más cerca posible
de todos los puntos a la vez, midiendo «cerca» como la suma de los errores al cuadrado, y cada
coeficiente dice cuánto cambia la predicción al mover una variable manteniendo el resto quieto.

## La idea

Tienes cinco alumnos, sus horas de estudio y su nota. Pintas los puntos y quieres resumir la
relación con una recta para poder predecir a alguien nuevo. ¿Cuál es «la» recta? Cualquier
recta deja errores: unos puntos quedan por encima y otros por debajo. La idea de mínimos
cuadrados es elegir la recta que hace mínima la suma de esos errores elevados al cuadrado.

¿Por qué al cuadrado y no el valor absoluto, que parece más natural? Por tres motivos
prácticos. Primero, elevar al cuadrado castiga mucho los errores grandes, así que la recta se
pelea por no fallar escandalosamente en ningún punto. Segundo, esa suma tiene una solución
cerrada: no hace falta buscar a ciegas, se calcula con una fórmula. Y tercero, el error
cuadrático es el que aparece de forma natural cuando supones que los errores siguen una
distribución normal.

Una trampa mental que conviene desactivar desde el principio: la recta describe **asociación**,
no causa. Si ajustas el gasto en helados contra los ahogamientos, la pendiente será positiva,
y no porque los helados ahoguen a nadie: detrás está el calor del verano, que empuja las dos
cosas. Eso es [[causalidad-vs-correlacion|correlación sin causalidad]], y ningún coeficiente
de regresión lo arregla.

Tampoco es lo mismo la pendiente de la regresión que la correlación. La correlación está
siempre entre −1 y 1 y no depende de las unidades; la pendiente depende de las unidades
(mide notas por hora de estudio o gramos por segundo según cómo midas). La correlación te dice
si la relación es fuerte; la pendiente, cuánto cambia la predicción con una unidad más.

## Definición formal

Con una sola variable explicativa, el modelo es:

:::formula
y = β₀ + β₁ · x + ε
:::

- `y` — variable que quieres predecir (respuesta).
- `x` — variable explicativa (predictora).
- `β₀` — intercepto: el valor esperado de `y` cuando `x = 0`.
- `β₁` — pendiente: cuánto cambia `y` de media por cada unidad que sube `x`.
- `ε` — error o residuo: todo lo que influye en `y` y no está en `x`.

Los estimadores de mínimos cuadrados (OLS, *ordinary least squares*) minimizan la suma de
residuos al cuadrado, `Σᵢ (yᵢ − ŷᵢ)²`, donde `ŷᵢ = b₀ + b₁·xᵢ` es la predicción para la fila
`i`. La solución en forma cerrada es:

:::formula
b₁ = Σᵢ (xᵢ − x̄)(yᵢ − ȳ) / Σᵢ (xᵢ − x̄)²      b₀ = ȳ − b₁ · x̄
:::

- `x̄`, `ȳ` — medias de `x` y de `y`.
- `Σᵢ` — suma sobre todas las observaciones.

Con varias variables, el modelo es `y = β₀ + β₁x₁ + β₂x₂ + … + βₚxₚ + ε` y se escribe de forma
matricial. Si `X` es la matriz de datos con una columna de unos al principio (para el
intercepto) e `y` el vector de respuestas, los coeficientes son:

:::formula
β = (XᵀX)⁻¹ Xᵀ y
:::

- `X` — matriz de `n` filas y `p+1` columnas; la primera columna es todo unos.
- `Xᵀ` — traspuesta de `X`.
- `β` — vector de coeficientes estimados, con `β₀` en la primera posición.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `β₁` | Pendiente: cambio medio de `y` por unidad de `x` | unidades de `y` por unidad de `x` | La recta se empina: cada unidad de `x` mueve mas la predicción |
| `β₀` | Intercepto: predicción cuando `x = 0` | unidades de `y` | Toda la recta sube sin cambiar su inclinación |
| `n` | Numero de observaciones | filas | El ajuste es mas estable y `R²` mas creible: menos riesgo de que un punto mande |
| `p` | Numero de variables explicativas | columnas (sin contar el uno) | `R²` nunca baja en entrenamiento, pero la predicción empeora fuera de muestra si hay sobreajuste |
| `ε` | Error: lo que influye en `y` y no esta en `x` | unidades de `y` | Nada que puedas tocar: si crece, el ajuste explica menos y `R²` baja |
| `R²` | Proporción de la variabilidad de `y` que recoge el modelo | tanto por uno, de 0 a 1 | Mas cerca de 1, mejor ajuste en la muestra (no prueba que el modelo sea correcto) |
:::

Dos consecuencias directas de esa fórmula, que se ven en el ejemplo: los residuos suman cero
y son ortogonales a cada columna de `X`. La recta pasa siempre por el punto `(x̄, ȳ)`.

Para medir cuánto se explica, se usa el coeficiente de determinación `R² = 1 − SS_res / SS_tot`,
donde `SS_res` es la suma de residuos al cuadrado y `SS_tot = Σᵢ(yᵢ − ȳ)²`. `R²` es la
proporción de la variabilidad de `y` que recoge el modelo, entre 0 y 1 (en entrenamiento).

## Ejemplo

Cinco alumnos, horas de estudio y nota:

```
x (horas)  1   2   3   4   5
y (nota)   4   5   6   8   9
```

- `x̄ = 3,0` e `ȳ = 6,4`.
- `Σ(xᵢ − x̄)(yᵢ − ȳ) = 13,0` y `Σ(xᵢ − x̄)² = 10,0`, así que `b₁ = 13,0 / 10,0 = 1,3`.
- `b₀ = 6,4 − 1,3 · 3,0 = 2,5`.

La recta es `nota = 2,5 + 1,3 · horas`. Lectura del coeficiente: cada hora extra de estudio se
asocia a 1,3 puntos más de nota **en estos datos**. Predicciones: 3,8 / 5,1 / 6,4 / 7,7 / 9,0.
Residuos: +0,2 / −0,1 / −0,4 / +0,3 / 0,0, que suman 0. Para 6 horas, la predicción es 10,3,
que ya está fuera del rango observado: es una extrapolación y hay que desconfiar de ella.

:::figura
fichero: regresion-lineal-recta-y-residuos
pie: A la izquierda, la recta que minimiza la suma de errores al cuadrado, con cada residuo dibujado como un palo vertical: suman cero y la recta pasa por el punto de las medias. La banda naranja es territorio sin datos, y ahí cae la predicción de 10,3 para 6 horas: aritmética correcta, conclusión dudosa, porque nada garantiza que la relación siga siendo lineal fuera del rango observado. A la derecha, el residuo de cada alumno frente a su predicción, en orden de horas: sube y baja sin que los errores grandes se agrupen en un lado. Con cinco puntos eso es todo lo que se puede comprobar; el embudo o la curva solo aparecen con muchos más.
fuente: figuras/regresion-lineal-1.py
:::

## Código

```python verificable
import numpy as np

# Horas de estudio (x) y nota (y) de 5 alumnos.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([4.0, 5.0, 6.0, 8.0, 9.0])

# Minimos cuadrados en forma cerrada: b1 = Sxy / Sxx
xm, ym = x.mean(), y.mean()
b1 = ((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()
b0 = ym - b1 * xm

residuos = y - (b0 + b1 * x)
r2 = 1 - (residuos ** 2).sum() / ((y - ym) ** 2).sum()

print(f"pendiente  {b1:.3f}")
print(f"intercepto {b0:.3f}")
print(f"R2         {r2:.4f}")
print(f"suma de residuos {residuos.sum():.1e}")
print(f"prediccion para x=6: {b0 + b1 * 6:.1f}")
# -> pendiente  1.300
# -> intercepto 2.500
# -> R2         0.9826
# -> suma de residuos 0.0e+00
# -> prediccion para x=6: 10.3
```

:::claves
- `x.mean()` y `y.mean()` se calculan sobre todo el `np.array` de una vez, en C. La resta
  `x - xm` devuelve un array **nuevo**: `x` sigue intacto. Si en vez de `x - xm` escribieras
  `x -= xm`, modificarias los datos originales y el resto de las cuentas saldria mal.
- `((x - xm) * (y - ym)).sum()` es un **producto elemento a elemento** seguido de una suma, no
  un producto escalar escrito raro. Si usaramos `x * y` sin restar las medias, el resultado no
  sería la covarianza sino algo que depende de donde este el origen.
- `b1` sale de dividir dos sumas, y las dos son del orden de 1: por eso el resultado no se te
  va de las manos. Con `x` en horas y `y` en euros, en cambio, `b1` tendria unidades de
  euros por hora: el número cambia aunque la relación sea la misma.
- `residuos = y - (b0 + b1 * x)` se calcula **después** de tener `b0` y `b1`. Si cambiaras el
  orden y calcularas los residuos con `b1` a medias, seguirian sumando algo parecido a cero y no
  te enterarias del error: la comprobación `residuos.sum()` no detecta un ajuste mal hecho.
- `f"..."` con `{b1:.3f}` redondea **solo al imprimir**; `b1` sigue guardando todos los
  decimales. Y `:.1e` en la suma de residuos escribe `0.0e+00`: la suma no es cero exacto, es
  cero hasta el error de redondeo de la coma flotante.
- Cambia `x` por `x + 1000`: `b1` no se mueve (la pendiente no depende del origen), pero `b0`
  se hunde a −1297,5. Es la misma recta descrita con otro cero de referencia.
:::

```python verificable
import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([4.0, 5.0, 6.0, 8.0, 9.0])

# Version matricial: la primera columna de unos es el intercepto.
X = np.column_stack([np.ones_like(x), x])
beta = np.linalg.solve(X.T @ X, X.T @ y)      # ecuaciones normales
print("beta (b0, b1):", np.round(beta, 3))

# Los residuos son ortogonales a las columnas de X; de ahi salen las ecuaciones normales.
residuos = y - X @ beta
print("X^T e:", np.round(X.T @ residuos, 12) + 0.0)
print(f"media de y {y.mean():.3f}  media de las predicciones {(X @ beta).mean():.3f}")
# -> beta (b0, b1): [2.5 1.3]
# -> X^T e: [0. 0.]
# -> media de y 6.400  media de las predicciones 6.400
```

## Errores típicos

- **Contar la pendiente como si fuera causal.** «Por cada hora extra, la nota sube 1,3
  puntos» es una descripción del ajuste, no una promesa de intervención. Puede haber una
  tercera variable (motivación, nivel previo) empujando las dos. Para afirmaciones causales
  hace falta un diseño experimental o métodos causales, no una regresión.
- **Extrapolar fuera del rango de los datos.** Con notas de 1 a 5 horas, predecir 10,3 para
  6 horas es aritmética correcta y conclusión dudosa: nada garantiza que la relación siga
  siendo lineal ahí. Los modelos lineales no avisan cuando se salen de su terreno.
- **Interpretar el intercepto cuando `x = 0` no existe.** `b₀ = 2,5` significa «nota esperada
  con cero horas», y con cero horas la nota real es 0. El intercepto es la altura de la recta
  en el origen, no siempre un valor con significado físico.
- **Usar `R²` como certificado de que el modelo es correcto.** Un `R²` de 0,98 puede convivir
  con una relación claramente curva o con un patrón en los residuos. Mira siempre los residuos
  frente a las predicciones antes de fiarte del número.
- **Meter variables muy correlacionadas y leer cada coeficiente.** Si dos variables contienen
  casi la misma información, la fórmula reparte el efecto de forma inestable: cambia una fila
  y los coeficientes saltan, a veces con signos absurdos. Es la multicolinealidad, y se detecta
  con [[covarianza-y-correlacion|la correlación]] entre predictoras y con el factor de inflación
  de la varianza.
- **Borrar los puntos que estropean el ajuste para subir el `R²`.** Un punto influyente puede
  cambiar la pendiente entera. Si es un error de medición, se corrige y se documenta; si es
  real, es parte del fenómeno y hay que decidir con criterio, no por conveniencia.

:::practica
enunciado: Cuatro días con temperatura 1, 2, 3 y 4 grados y ventas 3, 5, 7 y 8. Ajusta por mínimos cuadrados la recta de ventas sobre temperatura y predice un día a 3,5 grados.
pista: La pendiente es la suma de los productos de desviaciones entre la suma de las desviaciones de x al cuadrado; el intercepto sale de obligar a la recta a pasar por el punto de las medias.
solucion: x̄ = 2,5 e ȳ = 5,75. Las desviaciones de x son −1,5, −0,5, 0,5 y 1,5, con Σ(x−x̄)² = 5,0, y sus productos con las de y suman 8,5. Así b₁ = 8,5/5,0 = 1,7 y b₀ = 5,75 − 1,7 · 2,5 = 1,5. La recta es ventas = 1,5 + 1,7 · grados, y para 3,5 grados predice 1,5 + 5,95 = 7,45.
:::

## Comprueba que lo sabes

:::quiz
p: En el ejemplo, la recta es nota = 2,5 + 1,3 · horas. ¿Qué significa exactamente el 1,3?
o: Que la nota sube 1,3 puntos de media por cada hora extra de estudio en estos datos
o: Que el 1,3 % de la variación de la nota se explica por las horas
o: Que la correlación entre horas y nota es 1,3
a: 1
e: El coeficiente es la pendiente: cambio medio de la nota por unidad de horas. La proporción de variabilidad explicada es el R2 (0,9826) y la correlación no puede superar 1 en valor absoluto.
:::

:::quiz
p: ¿Por qué la suma de los residuos de una regresión con intercepto es exactamente cero?
o: Porque el intercepto absorbe la media y la recta pasa por el punto de las medias
o: Porque el modelo se ajusta hasta que no queda ningún error
o: Porque los residuos siempre son positivos y negativos a partes iguales por azar
a: 1
e: La ecuación normal del intercepto obliga a que la suma de residuos sea cero: la recta siempre pasa por (x̄, ȳ). Que la suma sea cero no significa que cada residuo sea cero ni que el ajuste sea bueno.
:::

:::quiz
p: Ajustas una regresión para predecir el precio de una vivienda y obtienes un coeficiente de 12.000 para los metros cuadrados. ¿Cuál es la lectura honesta?
o: Cada metro cuadrado extra se asocia a 12.000 euros más de precio medio, manteniendo el resto de variables del modelo
o: Cada metro cuadrado extra causa 12.000 euros de subida en el precio
o: Los metros cuadrados explican el 12 % de la variación del precio
a: 1
e: Un coeficiente es una asociación condicional al resto de variables del modelo, no un efecto causal. Y no dice nada sobre el porcentaje de variabilidad explicada: eso es el R2.
:::
