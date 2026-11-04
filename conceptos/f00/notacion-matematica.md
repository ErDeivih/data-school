---
id: notacion-matematica
titulo: Notación matemática
fase: 0
nivel: básico
rutas: [core]
prerequisitos: []
tags: [matematicas, notacion, simbolos, formulario]
resumen: Σ, Π, ∈, ∂, ∇ y E[…] no son un idioma aparte: cada símbolo es una abreviatura de una frase. Apréndelos y las fórmulas dejan de dar miedo.
---

## En una frase

Una fórmula no es un jeroglífico, es una frase escrita con abreviaturas: `Σ` significa «suma
todo esto», `∈` significa «está dentro de», y `∂` significa «cómo cambia esto cuando muevo solo
esta variable».

## La idea

Piensa en una receta: «2 cdas de aceite, 180 °C, 20 min». Nadie necesita un máster para leerlo,
porque las abreviaturas (`cdas`, `°C`, `min`) se aprenden una vez y se usan siempre. La notación
matemática es exactamente eso. No hay un idioma secreto ni hace falta «ser de números»: hay unas
cuantas abreviaturas, y quien no te las ha presentado nunca te ha dejado creer que el problema
eras tú.

Aquí va la intuición de las tres que más asustan:

- `Σ` (sigma mayúscula) es un bucle: «coge cada elemento de la lista y súmalo». Si dentro pone
  `xᵢ`, se lee «cada x». Nada más. Si además lleva límites arriba y abajo, son el principio y el
  final del bucle.
- `∂` (la d redondeada) es una pregunta muy concreta: «si muevo esta variable un poquito y dejo
  las demás quietas, ¿cuánto cambia el resultado?». Esa es toda la idea de la
  [[derivadas-parciales-y-gradiente|derivada parcial]].
- `E[…]` es «el valor medio teórico a largo plazo». No es la media de tus datos: es la media que
  saldría con infinitos datos, y la media de los tuyos solo se le acerca. Su nombre formal es
  [[valor-esperado|valor esperado]].

Dos reglas de lectura que resuelven el 90 % de los atascos. Primera: **las fórmulas se leen de
dentro hacia fuera**, como las muñecas rusas; empieza por lo que está entre paréntesis y sigue la
operación de fuera. Segunda: **cada símbolo debe tener un nombre asignado antes de usarse**. Si
ves una `σ` y nadie ha dicho qué es, la fórmula no está mal: está incompleta.

## Definición formal

Las abreviaturas que aparecen una y otra vez en este portal, agrupadas según para qué sirven.

**Contar y operar**

| Símbolo | Se lee | Significa |
| --- | --- | --- |
| `Σ` | sumatorio | suma de una lista de términos |
| `Π` | productorio | producto de una lista de términos |
| `n` | ene | número de elementos o de observaciones |
| `i, j, k` | índices | posiciones dentro de una lista o una matriz |
| `xᵢ` | x sub i | el elemento que ocupa la posición i |
| `xᵢⱼ` | x sub i j | el elemento de la fila i y la columna j |
| `x̄` | x barra | la media de los valores observados |
| `√` | raíz | raíz cuadrada: el número que multiplicado por sí mismo da lo de dentro |
| `‖x‖` | norma | la longitud del vector x |

**Conjuntos, lógica y comparaciones**

| Símbolo | Se lee | Significa |
| --- | --- | --- |
| `∈` | pertenece a | el elemento está en el conjunto |
| `∀` | para todo | la afirmación vale en todos los casos |
| `∃` | existe | hay al menos un caso que cumple |
| `∪, ∩` | unión, intersección | los dos conjuntos juntos, o solo lo que comparten |
| `∅` | conjunto vacío | no hay ningún elemento |
| `ℝ, ℕ, ℤ` | reales, naturales, enteros | los conjuntos de números habituales |
| `≤, ≥, ≠` | menor o igual, mayor o igual, distinto | comparaciones |
| `≈` | aproximadamente igual | resultado redondeado o numérico |
| `∼` | se distribuye como | en estadística, la ley de probabilidad de una variable |
| `∝` | proporcional a | al doble de esto, el doble de aquello |
| `≪, ≫` | mucho menor, mucho mayor | diferencia de órdenes de magnitud |
| `⇒, ⇔` | implica, si y solo si | relación entre dos afirmaciones |

**Cálculo y probabilidad**

| Símbolo | Se lee | Significa |
| --- | --- | --- |
| `∂f/∂x` | parcial de f respecto de x | cómo cambia f al mover x, dejando el resto quieto |
| `∇f` | gradiente de f | el vector con todas las derivadas parciales |
| `df/dx` | derivada total | cómo cambia f contando que todo puede moverse |
| `∫` | integral | acumular el área bajo una curva |
| `Δ` | delta, incremento | la diferencia entre dos valores |
| `E[X]` | esperanza de X | el valor medio teórico de la variable X |
| `σ` | sigma | desviación típica: dispersión en las unidades de los datos |
| `σ²` | sigma cuadrado | varianza: la misma dispersión, en unidades al cuadrado |
| `μ` | mu | media teórica de una población |
| `θ` | theta | un parámetro desconocido que se estima |
| `argmax` | argumento que maximiza | el valor de la variable que hace máxima la función |

Tres convenios que conviene respetar al escribir: **mayúscula para la variable aleatoria y
minúscula para un valor concreto** (`X` es el resultado de tirar el dado y `x = 4` es un
resultado); **subíndice para la posición y superíndice para la potencia** (`x₂` es el segundo dato
y `x²` es x al cuadrado); y **los límites del sumatorio se escriben o se dicen** (`Σᵢ₌₁ⁿ xᵢ` está
completo, `Σ xᵢ` solo tiene sentido si el contexto ya fijó sobre qué se suma).

Dos símbolos que se escriben con barras: el valor absoluto `|x|`, que es el número sin su signo (va
en prosa y no en las tablas, porque la barra simple es el separador de columnas), y la norma
`‖x‖`, que es la longitud de un vector y sí está en la tabla de arriba. En código son `abs(x)` y
`np.linalg.norm(x)`.

## Ejemplo

Leamos cuatro fórmulas en alto, con números.

1. Con `x = (3, 5, 7, 9)`: `Σᵢ₌₁⁴ xᵢ = 3 + 5 + 7 + 9 = 24`. El productorio con los mismos
   números, `Πᵢ₌₁⁴ xᵢ = 3 · 5 · 7 · 9 = 945`.
2. La media de esos cuatro valores: `x̄ = (1/n) · Σᵢ₌₁ⁿ xᵢ = 24 / 4 = 6`. Se lee «x barra es igual
   a uno entre n por el sumatorio de las x».
3. `X ∼ N(10, 4)` se lee «X se distribuye como una normal de media 10 y varianza 4», la
   [[distribuciones-continuas|distribución normal]]. El segundo parámetro es la **varianza**, así
   que la desviación típica es `σ = √4 = 2`. Y `E[X] = 10`, que es la media teórica, no la de una
   muestra.
4. Con `f(x, y) = 3x²y`: `∂f/∂x = 6xy` y `∂f/∂y = 3x²`. En el punto `(2, 5)` el gradiente es
   `∇f = (6 · 2 · 5, 3 · 2²) = (60, 12)`: por cada unidad que muevas la x, f crece unas 60; por
   cada unidad que muevas la y, unas 12, cinco veces menos.

Fíjate en lo que ha pasado: ninguna de las cuatro líneas exigía saber matemáticas nuevas. Solo
leer las abreviaturas y hacer aritmética.

## Código

```python verificable
import numpy as np

x = np.array([3.0, 5.0, 7.0, 9.0])

# Σ es un sumatorio y Π un productorio: en NumPy son dos funciones y nada más.
# Se imprimen los nombres en ASCII para que el ejemplo funcione en cualquier consola.
print("sumatorio  x_i =", x.sum())      # -> 24.0
print("producto   x_i =", x.prod())     # -> 945.0
print("media      x_i =", (1 / x.size) * x.sum())   # -> 6.0

# La derivada parcial ∂f/∂x, con una sola variable, se aproxima con diferencias
# finitas centradas.
f = lambda v: 3 * v**2 * 5          # f(x, 5) = 3x²·5
h = 1e-6
print("parcial en x=2 ~", round((f(2 + h) - f(2 - h)) / (2 * h), 1))   # -> 60.0
```

```python verificable
import numpy as np

# X ~ N(10, 4) usa la VARIANZA como segundo parámetro; np.random.normal pide la
# desviación típica (scale). Es el error de lectura más caro de esta página.
rng = np.random.default_rng(0)
media, varianza = 10.0, 4.0

muestra = rng.normal(loc=media, scale=np.sqrt(varianza), size=1_000_000)
print(f"E[X] = {media:.1f}   media muestral = {muestra.mean():.3f}")        # -> 10.0 y 10.002
print(f"sigma = {np.sqrt(varianza):.1f}   s = {muestra.std(ddof=1):.3f}")   # -> 2.0 y 2.001
```

## Errores típicos

- **Leer `∼` como «aproximadamente».** En estadística significa «se distribuye como»: `X ∼ N(0, 1)`
  no dice que X valga casi cero, dice qué forma tiene su distribución.
- **Confundir `σ` con `σ²`.** La normal se escribe `N(μ, σ²)` con la varianza, pero casi todas las
  funciones de Python piden la desviación. Poner el 4 de `N(10, 4)` como desviación duplica la
  dispersión real. La diferencia entre ambas está en
  [[varianza-y-desviacion|varianza y desviación típica]].
- **Usar un sumatorio sin decir sobre qué suma.** `Σ xᵢ` sin límites ni contexto no es una fórmula,
  es un hueco. Escribe siempre los límites o di en voz alta «sumando todos los elementos».
- **Confundir `∂` con `d`.** La derivada total `df/dx` cuenta que las demás variables cambian; la
  parcial `∂f/∂x` las deja quietas. En una función de una sola variable coinciden, y de ahí viene
  la confusión.
- **Confundir `argmax` con `max`.** `max` devuelve el valor más alto; `argmax`, la posición donde
  está. Si tienes `(3, 9, 4)`, el máximo es 9 y el argmax es 2.
- **Ignorar mayúsculas y subíndices.** `X` y `x` son cosas distintas, igual que `x₂` y `x²`. En
  notación matemática el tamaño y la posición de los símbolos llevan información.

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa exactamente `X ∼ N(10, 4)`?
o: Que X vale aproximadamente 10, con un error de 4
o: Que X se distribuye como una normal de media 10 y varianza 4, es decir, con desviación típica 2
o: Que X toma 4 valores distintos alrededor de 10
a: 2
e: El símbolo ∼ indica la ley de probabilidad, no una aproximación numérica. El segundo parámetro de la normal es la varianza, así que la desviación típica es la raíz de 4, o sea 2.
:::

:::quiz
p: Con `f(x, y) = 3x²y`, ¿qué es `∂f/∂x`?
o: `6xy`: la variación de f al mover x dejando y fija
o: `3x²`: la variación de f al mover y dejando x fija
o: `6xy + 3x²`: hay que sumar las dos derivadas parciales
a: 1
e: La derivada parcial respecto de x trata la y como una constante, y la derivada de x² es 2x, de donde sale 6xy. La opción 3x² es la parcial respecto de y; sumar las dos es el diferencial total, que es otra cosa.
:::

:::trampa
`≪` y `≫` no significan «algo menor»: significan «menor en órdenes de magnitud». Decir «2 ≪ 3» es
incorrecto; lo correcto es «1000 ≪ 1 000 000». Si quieres decir «un poco menos», usa `<`.
:::
