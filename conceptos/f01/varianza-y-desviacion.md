---
id: varianza-y-desviacion
titulo: Varianza y desviación típica
fase: 1
nivel: básico
rutas: [core, ds, quant]
prerequisitos: [valor-esperado, medidas-de-dispersion]
tags: [probabilidad, dispersion, riesgo]
resumen: Cuanto se aleja una variable de su media, por qué se mide en unidades al cuadrado y cómo se combinan las varianzas al sumar variables.
fuentes: ["Casella y Berger (2002), 'Statistical Inference'", "DeGroot y Schervish (2012), 'Probability and Statistics'"]
---

## En una frase

La varianza es el promedio de las distancias al cuadrado a la media, y la desviación típica es
su raíz cuadrada: la misma información, pero en las unidades originales.

## La idea

Dos empresas de mensajería prometen entregar en 30 minutos de media. En la primera, los
repartos tardan entre 29 y 31 minutos; en la segunda, unos tardan 10 y otros 50. La media es
idéntica y las dos empresas no se parecen en nada: para prometer un plazo, planificar turnos o
decidir a cuál contratas, lo que importa es la **dispersión**.

La forma natural de medirla sería promediar las distancias a la media, pero esas distancias se
cancelan (unas son positivas y otras negativas) y el promedio da cero siempre. Hay dos salidas:
usar el valor absoluto o elevar al cuadrado. Se eligió el cuadrado, y no por capricho:

- es derivable en todas partes, así que se puede optimizar y aparece en fórmulas cerradas;
- **se descompone de forma aditiva**: la varianza de una suma de variables independientes es
  la suma de las varianzas. Esa propiedad es la que sostiene los mínimos cuadrados, la
  anualización de la volatilidad, el ANOVA y media estadística aplicada.

El precio de elevar al cuadrado es que la varianza vive en **unidades al cuadrado**: si mides
alturas en metros, la varianza va en metros cuadrados, y comparar una varianza en m² con otra
en cm² es comparar peras con manzanas. La **desviación típica** arregla eso tomando la raíz:
vuelve a metros y se puede leer en la misma escala que los datos. Por eso casi todo el mundo
comunica desviaciones típicas (la volatilidad de un activo, la precisión de un instrumento) y
casi todos los teoremas se escriben con varianzas.

Un aviso para cuando llegues a finanzas: la desviación típica mide dispersión simétrica. Un
activo que sube un 40 % y otro que baja un 40 % contribuyen igual a la volatilidad, aunque no
sean la misma noticia. Para eso existen la asimetría y el CVaR.

## Definición formal

Para una variable aleatoria `X` con media `μ = E[X]`:

:::formula
Var(X) = E[(X − μ)²] = E[X²] − μ²
:::

- `Var(X)` — varianza de `X`; se escribe también `σ²` o `σ²_X`.
- `σ = √Var(X)` — desviación típica de `X`, en las mismas unidades que `X`.
- `E[·]` — valor esperado; `μ²` es la media elevada al cuadrado, no `E[X²]`.

:::figura
fichero: varianza-dispersion-y-suma
pie: Arriba, dos empresas con la misma media de 30 minutos: la azul entrega siempre entre 25 y 35, la naranja reparte entre 10 y 50. La media no distingue una de otra; la desviación típica si. Abajo a la izquierda, multiplicar por 3 sube la desviación a 5,12 (x3) y la varianza a 26,25 (x9). Abajo a la derecha, la desviación de la suma de dos dados es 2,4152, no la suma de las desviaciones (3,4157): lo que se suma son las varianzas.
fuente: figuras/varianza-y-desviacion-1.py
:::

**Propiedades.**

- `Var(c) = 0` para cualquier constante `c`.
- `Var(aX + b) = a²·Var(X)`. Sumar `b` no cambia nada (traslada la distribución) y multiplicar
  por `a` multiplica la desviación típica por `a`, pero la varianza por `a²`.
- `Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y)`. Si `X` e `Y` son independientes, el término de
  covarianza desaparece y las varianzas se suman.
- `Var(X − Y) = Var(X) + Var(Y) − 2·Cov(X, Y)`. Restar **no** reduce el riesgo si las variables
  son independientes: siguen sumándose las varianzas.

**Versión muestral.** Con `n` datos `x₁, …, xₙ` y media muestral `x̄`:

`s² = (1/(n−1)) · Σᵢ (xᵢ − x̄)²`

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Var(X)`, `sigma^2` | Dispersión media al cuadrado respecto a la media | las de `X` al cuadrado | Es el resultado de la formula. Crece con el cuadrado de cualquier cambio de escala, y siempre es mayor o igual que 0 |
| `sigma` | Desviación típica: la raíz de la varianza | las de `X` | Vuelve a las unidades originales y es lo que se comunica. Se multiplica por `a` cuando los datos se multiplican por `a`, no por `a^2` |
| `mu` | La media de `X`, `E[X]` | las de `X` | Desplaza la distribución sin cambiar la dispersión: `Var(X + b) = Var(X)`. Sumar una constante no reduce el riesgo |
| `E[X^2]` | Media de los cuadrados | las de `X` al cuadrado | Entra en la versión corta `Var = E[X^2] - mu^2`. Es mayor o igual que `mu^2`, y la diferencia es justo la varianza |
| `a`, `b` | Constantes de un cambio de escala y un desplazamiento | adimensionales | `Var(aX + b) = a^2 · Var(X)`. Duplicar `a` cuadruplica la varianza y solo duplica la desviación. Si `a` es negativo, la varianza no cambia de signo |
| `Cov(X, Y)` | Covarianza entre las dos variables que se suman | producto de las unidades de las dos | Con covarianza positiva, `Var(X + Y)` sube por encima de la suma de varianzas; con covarianza negativa, baja. Es lo que hace que diversificar funcione |
| `s^2` | Varianza muestral, calculada con `n - 1` | las de los datos al cuadrado | Con `ddof=0` (dividir por `n`) sale sistematicamente mas pequeña; con seis datos, un 17 % menos. El divisor correcto al estimar de una muestra es `n - 1` |
| `n` | Numero de datos de la muestra | observaciones | Mas datos no cambian el valor esperado del estimador, solo su precisión: la varianza muestral sigue fluctuando alrededor de `sigma^2`, pero cada vez menos |
:::

El divisor es `n − 1` porque la media se estima con los propios datos y eso consume un grado de
libertad; dividir por `n` da una estimación sesgada hacia abajo. Dividir por `n` se usa cuando
los datos son la población completa y no una muestra (por ejemplo, en la varianza de un dado
justo, que se calcula con las seis caras).

## Ejemplo

**Un dado.** `E[X] = 3,5` y `E[X²] = (1 + 4 + 9 + 16 + 25 + 36)/6 = 91/6 = 15,1667`. Entonces
`Var(X) = 15,1667 − 12,25 = 2,9167` y `σ = √2,9167 = 1,7078`. La desviación típica es más
pequeña que el rango (5) y más grande que la mitad del rango típico, que es lo esperable en una
distribución con masa en los seis valores.

**Cambio de escala.** Si `Y = 3X + 10`, `Var(Y) = 9 · 2,9167 = 26,25` y `σ_Y = 5,1235`. El
`+10` no ha cambiado la dispersión; el `×3` ha triplicado la desviación típica.

**Dos dados.** La suma de dos dados independientes tiene
`Var = 2,9167 + 2,9167 = 5,8333`, y `σ = 2,4152`. Fíjate en que la desviación de la suma
**no** es la suma de las desviaciones: `1,7078 + 1,7078 = 3,4156` es un número demasiado
grande. Las desviaciones típicas no se suman; las varianzas sí.

**Datos reales.** Alturas de seis personas, en metros: 1,62 · 1,71 · 1,68 · 1,75 · 1,80 · 1,66.
La media es 1,7033 m, la varianza muestral 0,00419 m² y la desviación típica 0,0647 m. Decir
«la varianza es 0,004» sin unidades no informa de nada; decir «la desviación típica es 6,5 cm»
sí.

## Código

```python verificable
import numpy as np

x = np.arange(1, 7, dtype=float)          # un dado justo, valores equiprobables
var = (x ** 2).mean() - x.mean() ** 2     # E[X^2] - (E[X])^2

print(f"E[X^2]       = {(x ** 2).mean():.4f}")   # -> 15.1667
print(f"Var(X)       = {var:.4f}")               # -> 2.9167
print(f"Desv. tipica = {np.sqrt(var):.4f}")      # -> 1.7078
print(f"Var(3X + 10) = {(3 * x + 10).var():.4f}")  # -> 26.2500
```
:::claves
- `x = np.arange(1, 7, dtype=float)` importa: sin `dtype=float` el array sería de enteros, `x ** 2` seguiria siendo exacto pero `x.mean()` también devolveria un `float`, y en un array de enteros una división entera te daria un resultado truncado sin avisar.
- `(3 * x + 10).var()` no lleva `ddof`: NumPy divide por `n` por defecto. Aqui da igual porque los seis valores son la población entera del dado, pero en el bloque siguiente, con las alturas de seis personas, la diferencia entre `ddof=0` y `ddof=1` es el 17 % que la página senala.
- `alturas.var(ddof=1)` y `alturas.std(ddof=1)` son métodos del array y **no** modifican nada: devuelven un número nuevo. `sort()` si modifica en el sitio; `var` no. Para comprobarlo, imprime `alturas` después y veras el mismo orden.
- `np.array([a + b for a, b in product(range(1, 7), repeat=2)], dtype=float)` construye los 36 resultados con una lista intermedia de Python. NumPy tiene formas sin bucle (`np.add.outer`), pero esta deja claro que hay 36 sumas y no un modelo.
- `suma.var()` sale 5,8333 y `dado.var()` 2,9167, el doble. Al sumar variables independientes las varianzas se suman. La prueba de que no se suman las desviaciones es que `1,7078 + 1,7078 = 3,4156` no es `2,4152`.
- Los `print` con `:.5f` y `:.4f` muestran decimales distintos a proposito: con `ddof=0` y `ddof=1` los dos valores difieren en el tercer decimal, así que redondear a dos los igualaria y ocultaria el sesgo que se quiere ensenar.
:::


```python verificable
import numpy as np
from itertools import product

alturas = np.array([1.62, 1.71, 1.68, 1.75, 1.80, 1.66])

# ddof=1 divide por n-1: estimamos la media y gastamos un grado de libertad.
print(f"media          = {alturas.mean():.4f} m")        # -> 1.7033 m
print(f"varianza ddof0 = {alturas.var(ddof=0):.5f} m^2")  # -> 0.00349 m^2
print(f"varianza ddof1 = {alturas.var(ddof=1):.5f} m^2")  # -> 0.00419 m^2
print(f"desv. tipica   = {alturas.std(ddof=1):.4f} m")    # -> 0.0647 m

# Dos dados independientes: las varianzas se suman, las desviaciones no.
suma = np.array([a + b for a, b in product(range(1, 7), repeat=2)], dtype=float)
dado = np.arange(1, 7, dtype=float)
print(f"Var(suma) = {suma.var():.4f}  = 2 * {dado.var():.4f}")   # -> 5.8333  = 2 * 2.9167
```

## Errores típicos

- **Sumar desviaciones típicas.** La desviación de una suma independiente es la raíz de la suma
  de varianzas: `√(2,9167 + 2,9167) = 2,4152`, no `1,7078 + 1,7078 = 3,4156`. Sumar sigmas
  infla el riesgo (o la precisión) de forma sistemática.
- **Comparar varianzas en unidades distintas.** Si pasas de metros a centímetros, la varianza
  se multiplica por 10.000 y la desviación típica solo por 100. Convierte las dos cosas a la
  misma unidad antes de comparar.
- **Dividir por n al estimar de una muestra.** Da una varianza sistemáticamente menor que la
  real; con seis datos, 0,00349 frente a 0,00419, un 17 % menos. El divisor correcto con datos
  muestrales es `n − 1`.
- **Creer que restar variables reduce el riesgo.** Si `X` e `Y` son independientes,
  `Var(X − Y) = Var(X) + Var(Y)`: restar suma varianzas igual que sumar. Solo la covarianza
  negativa hace que una resta (o una cartera con pesos opuestos) reduzca la dispersión.
- **Usar la regla del 68 % sin comprobar la forma.** Que el 68 % de los datos caiga dentro de
  `μ ± σ` es cierto para la normal. En una distribución de colas gordas ese porcentaje cambia,
  y hay datos a más de cinco desviaciones típicas con una frecuencia que la normal considera
  imposible.
- **Interpretar la desviación típica como un rango.** `σ` no dice el máximo ni el mínimo, ni
  cuánto puede perder una estrategia. Es una medida de dispersión media, no una cota.

:::practica
enunciado: La duración en minutos de un servicio tiene media 20 y desviación típica 4. Se factura segun Y = 2X + 5. Calcula Var(Y), la desviación típica de Y y explica que aporta el sumando 5.
pista: La varianza de un cambio de escala aplica Var(aX + b) = a² · Var(X).
solucion: Var(X) = 4² = 16. Var(Y) = 2² · 16 = 64, así que sigma_Y = 8 minutos. El factor 2 duplica la desviación típica (de 4 a 8) pero cuadruplica la varianza; el sumando 5 solo desplaza la media a 45 minutos y no cambia nada la dispersión. La varianza va en minutos al cuadrado.
:::

## Comprueba que lo sabes

:::quiz
p: Si multiplicas todos los datos por 3 y les sumas 10, ¿qué le pasa a la varianza?
o: Se multiplica por 3 y se le suma 10
o: Se multiplica por 9, porque la varianza va en unidades al cuadrado
o: No cambia, porque la forma de la distribución es la misma
a: 2
e: Var(aX + b) = a²·Var(X). El desplazamiento b no afecta a la dispersión, y el factor 3 se eleva al cuadrado porque la varianza mide distancias al cuadrado. La desviación típica se multiplica por 3, no por 9.
:::

:::quiz
p: X e Y son independientes, con Var(X) = 4 y Var(Y) = 9. ¿Cuánto vale Var(X − Y)?
o: 13, porque las varianzas se suman
o: 5, porque se restan
o: 1, porque 3 − 2 = 1
a: 1
e: Al restar, el término de covarianza sería −2·Cov(X, Y), y con independencia la covarianza es cero, así que queda 4 + 9 = 13. La desviación típica de la diferencia es √13 ≈ 3,61, mayor que cada una por separado.
:::

:::quiz
p: ¿Por qué se usa el cuadrado de las distancias y no su valor absoluto?
o: Porque el cuadrado se descompone de forma aditiva y permite sumar varianzas
o: Porque el valor absoluto da siempre cero
o: Porque el cuadrado es más fácil de interpretar en las unidades originales
a: 1
e: La varianza de una suma independiente es la suma de varianzas, y esa propiedad sostiene los mínimos cuadrados, el ANOVA y la anualización de la volatilidad. El valor absoluto también evita la cancelación (la desviación absoluta media existe), pero no se descompone igual de bien. El cuadrado, además, obliga a tomar la raíz para volver a las unidades originales.
:::
