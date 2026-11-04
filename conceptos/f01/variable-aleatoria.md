---
id: variable-aleatoria
titulo: Variable aleatoria
fase: 1
nivel: básico
rutas: [core, ds, quant]
prerequisitos: [probabilidad-axiomas, notacion-matematica]
tags: [probabilidad, fundamentos, distribuciones]
resumen: Una función que asigna un número a cada resultado de un experimento, con su masa o densidad y su función de distribución asociadas.
fuentes: ["Ross (2014), 'Introduction to Probability Models'", "Casella y Berger (2002), 'Statistical Inference'"]
---

## En una frase

Una variable aleatoria es una regla que asigna un número a cada resultado posible de un
experimento, y su distribución dice qué valores puede tomar y con qué probabilidad.

## La idea

Tirar dos dados no te devuelve un número, te devuelve un par: (3, 5). Si lo que te importa es
la puntuación de una partida, esa información se resume en un 8. La **variable aleatoria** es
exactamente esa traducción: una función que convierte resultados del mundo en números, para
poder sumarlos, promediarlos y compararlos. Al número que sale en una tirada concreta se le
llama **realización**, y a la lista de valores posibles con sus probabilidades, **distribución**.

Hay dos sabores, y la diferencia es práctica, no estética.

- **Discreta:** los valores posibles se pueden listar uno a uno (el número de coches que pasan
  por delante de tu casa en una hora, el número de caras en diez lanzamientos). Cada valor
  tiene su probabilidad concreta, dada por la **función de masa**.
- **Continua:** la variable puede tomar cualquier valor de un intervalo (el tiempo hasta que
  falla un servidor, la altura de una persona, la temperatura de mañana). Aquí no hay lista
  posible, y aparece la trampa conceptual más grande del tema: **la probabilidad de un valor
  exacto es cero**. Preguntar «¿cuál es la probabilidad de que el servidor tarde exactamente
  2,000000 horas?» no tiene respuesta útil; lo que sí la tiene es un intervalo, y esa
  probabilidad es el área bajo la curva de **densidad**.

Por eso la densidad no es una probabilidad: es «probabilidad por unidad de x», y solo significa
algo cuando la multiplicas por un trozo de eje. Una uniforme entre 0 y 0,5 tiene densidad 2 en
todo su soporte, y 2 no es ninguna probabilidad.

La tercera pieza, la **función de distribución**, sirve para las dos: F(x) = P(X ≤ x), la
probabilidad acumulada hasta x. Es la que se usa para calcular cualquier intervalo y la que
devuelven las funciones de Python.

Una última idea: la X mayúscula es la variable, con su distribución; la x minúscula es un valor
concreto ya observado. Mezclarlas es la fuente de la mitad de las confusiones al leer fórmulas.

## Definición formal

Sea un experimento con espacio muestral `Ω` (el conjunto de todos los resultados posibles) y
una probabilidad `P` definida sobre sus sucesos. Una **variable aleatoria** es una función
`X: Ω → ℝ` que asigna un número real a cada resultado `ω ∈ Ω`. Se escribe `X` en mayúscula
para la función y `x` en minúscula para un valor concreto.

- **Variable discreta.** Su soporte es numerable: `x₁, x₂, x₃, …`. Su **función de masa**
  (o de probabilidad) es `p(x) = P(X = x)`, con `p(x) ≥ 0` y `Σₓ p(x) = 1`. La suma recorre
  todos los valores del soporte.
- **Variable continua.** Existe una **función de densidad** `f(x) ≥ 0` con `∫ f(x) dx = 1`
  (la integral recorre toda la recta real) tal que, para cualquier intervalo,
  `P(a < X ≤ b) = ∫ₐᵇ f(x) dx`. La densidad puede ser mayor que 1; no es una probabilidad.
- **Función de distribución.** `F(x) = P(X ≤ x)`, igual para discretas y continuas. Cumple
  tres cosas: no decrece, tiende a 0 por la izquierda y a 1 por la derecha, y es continua por
  la derecha. En el caso continuo, `F` es la integral de `f` y `f` es la derivada de `F`.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `X` | La variable aleatoria: la función que traduce un resultado a un número | las del número que devuelve | No es un parámetro que se mueva: es mayuscula porque es la función, no un dato |
| `x` | Un valor concreto del soporte o una realización ya observada | las de `X` | Sustituir un valor por otro cambia la probabilidad, pero `x` no es un mando |
| `p(x)` | Función de masa (solo discreta): probabilidad de ese valor exacto | probabilidad, entre 0 y 1 | Todas las masas tienen que sumar exactamente 1. Con mas valores en el soporte, cada uno pesa menos |
| `f(x)` | Función de densidad (solo continua): probabilidad por unidad de `x` | inversa de las unidades de `X` | Puede pasar de 1 sin problema: no esta acotada, solo su integral lo esta. Si estrechas el soporte, la densidad sube aunque la probabilidad del intervalo no cambie |
| `F(x)` | Función de distribución: probabilidad acumulada hasta `x` | probabilidad, entre 0 y 1 | Nunca baja, empieza en 0 y termina en 1. Su pendiente es la densidad |
| `dx` | La anchura del intervalo con el que aproximas la integral | las de `X` | En la integral no es un parámetro; al calcularlo a mano con una suma, cuanto mas pequeño, mas exacto el área. Con `x = np.linspace(0, 2, 20001)` el paso ya es despreciable |
| `lam` | Tasa de la exponencial: sucesos por unidad de tiempo | inversa del tiempo (por hora) | Mas tasa, mas densidad cerca de 0 y menos cola: la media cae como `1 / lam`. `lam = 0,5` por hora da una media de 2 horas |
| `a`, `b` | Los extremos del intervalo cuya probabilidad quieres | las de `X` | `P(a < X <= b) = F(b) - F(a)`: al ensanchar el intervalo la probabilidad sube, y con `a = b` vale 0 exactamente |
:::

Con la función de distribución, cualquier probabilidad de un intervalo sale por resta:
`P(a < X ≤ b) = F(b) − F(a)`.

:::figura
fichero: variable-masa-densidad-y-acumulada
pie: A la izquierda, la suma de dos dados: solo once valores y en cada barra la altura es la probabilidad exacta. A la derecha, un tiempo continuo: la zona sombreada (un área) es P(X menor o igual que 2) y la línea roja es solo una altura, la densidad, que no es probabilidad de nada. La línea verde discontinua es F(x), que se lee en vertical y llega a 1.
fuente: figuras/variable-aleatoria-1.py
:::

## Ejemplo

**Caso discreto.** Lanzas dos dados y llamas `X` a la suma. Hay 36 resultados igual de
probables y la suma solo puede ir de 2 a 12:

- `P(X = 7) = 6/36 = 0,1667` (las seis parejas que suman 7).
- `P(X ≤ 4) = (1 + 2 + 3)/36 = 6/36 = 0,1667`.
- `P(X ≥ 11) = (2 + 1)/36 = 3/36 = 0,0833`.

Sumando las once probabilidades sale exactamente 1, como tiene que ser.

**Caso continuo.** El tiempo hasta el siguiente fallo de un servidor sigue una exponencial de
media 2 horas, con densidad `f(x) = 0,5 · e^(−0,5x)` para `x ≥ 0`. Entonces:

- `P(X ≤ 2) = 1 − e^(−1) = 0,6321`, calculado integrando la densidad de 0 a 2.
- `P(X = 2) = 0` exactamente.
- La densidad en `x = 2` vale `0,5 · e^(−1) = 0,1839`, que **no** es la probabilidad de nada:
  es la altura de la curva. La probabilidad de un intervalo de 0,01 horas alrededor de 2 es
  aproximadamente `0,1839 · 0,01 = 0,0018`.

## Código

```python verificable
from collections import Counter
from itertools import product

# X = suma de dos dados. Enumeramos los 36 resultados equiprobables, sin simular nada.
resultados = Counter(a + b for a, b in product(range(1, 7), repeat=2))
total = sum(resultados.values())

print(f"P(X = 7)   = {resultados[7] / total:.4f}")     # -> 0.1667
print(f"P(X <= 4)  = {sum(v for k, v in resultados.items() if k <= 4) / total:.4f}")  # -> 0.1667
print(f"P(X >= 11) = {sum(v for k, v in resultados.items() if k >= 11) / total:.4f}")  # -> 0.0833

# La masa suma 1: es la comprobacion de que la distribucion esta completa.
print("suma de la masa =", sum(resultados.values()) / total)   # -> 1.0
```
:::claves
- `Counter` no es un diccionario normal: cuando pides una clave que no existe devuelve `0` en vez de lanzar `KeyError`. Por eso `resultados[7]` funciona y también funcionaria `resultados[99]`. Y es una subclase de `dict`, así que conserva el orden de inserción al iterar.
- `Counter(a + b for a, b in product(range(1, 7), repeat=2))` recorre las 36 parejas **sin simular nada**: `product` genera el producto cartesiano y `repeat=2` es lo que hace que sean dos dados y no uno. Si cambiaras `repeat=2` por `repeat=3`, el soporte pasaria de 2..12 a 3..18 y todas las cuentas de abajo serian otras.
- `sum(resultados.values()) / total` vale 1,0 por construcción: `Counter` no normaliza nada. La comprobación útil es comparar el conteo de una rama concreta con el total, no confiar en que la suma de la masa sea 1.
- En el bloque de NumPy, `np.trapezoid` no es una integral simbolica: aproxima el área sumando trapecios sobre los puntos de `x`. Si reduces `np.linspace(0, 2, 20001)` a 20 puntos, el resultado cambia y el `# -> 0.6321` deja de cumplirse. La versión `np.trapz` es el nombre antiguo y esta en desuso.
- `lam * np.exp(-lam * x)` se calcula **elemento a elemento** porque `x` es un array: el resultado tiene la misma forma que `x`. Si `x` fuera una lista de Python, esa línea multiplicaria números por una lista y fallaria; el array es lo que hace que la operación vectorial funcione.
- El `print` con `f"P(X <= 2) por integral = {area:.4f}"` redondea al imprimir, no al calcular: `area` sigue siendo el número completo. Y `{0.0:.4f}` imprime `0.0000`, que es la forma de dejar claro que la probabilidad de un valor exacto es cero y no simplemente pequeña.
:::


```python verificable
import numpy as np

# Variable continua: integramos la densidad para obtener probabilidades.
lam = 0.5                                  # tasa: 0,5 fallos por hora -> media 2 horas
x = np.linspace(0, 2, 20001)
area = np.trapezoid(lam * np.exp(-lam * x), x)

print(f"P(X <= 2) por integral = {area:.4f}")          # -> 0.6321
print(f"1 - exp(-lam * 2)      = {1 - np.exp(-lam * 2):.4f}")   # -> 0.6321
print(f"densidad en x = 2      = {lam * np.exp(-lam * 2):.4f}") # -> 0.1839
print(f"P(X = 2)               = {0.0:.4f}")            # -> 0.0000
```

## Errores típicos

- **Leer la densidad como una probabilidad.** `f(2) = 0,1839` no es `P(X = 2)`. La densidad
  es probabilidad por unidad de `x`, puede pasar de 1 y no está acotada por arriba.
- **Confundir masa con distribución acumulada.** `p(x) = P(X = x)` da la probabilidad de un
  valor; `F(x) = P(X ≤ x)` da la de todo lo que queda por debajo. Si mezclas las dos, calculas
  mal cualquier intervalo, sobre todo en el extremo superior (¿`P(X ≤ 7)` o `P(X < 7)`?).
- **Concluir que un suceso de probabilidad cero es imposible.** En una continua, `P(X = 2) = 0`
  y el servidor puede tardar exactamente 2,000000 horas. Probabilidad cero y suceso imposible
  solo coinciden cuando el espacio muestral es discreto y cada uno de sus resultados tiene
  probabilidad mayor que cero.
- **Suponer que todos los valores del soporte son igual de probables.** Repartir `1/n` entre
  los valores «porque no sabes nada» es una decisión que hay que justificar; en dos dados,
  el 7 es seis veces más probable que el 12.
- **Usar una densidad con datos de conteo (o una masa con datos continuos).** Si tu variable
  es «número de reintentos», tiene masa y no densidad; si es «peso del paquete», al revés.
- **Confundir la variable con el dato.** `X` es la variable con su distribución; `x = 3,7` es
  una observación. La mayúscula no es un número.

:::practica
enunciado: X es la suma de dos dados justos de seis caras. Calcula P(X ≤ 5) usando la función de distribución y comprueba que coincide con sumar la masa valor a valor.
pista: Enumera las 36 parejas equiprobables y cuenta las que suman 5 o menos; al sumar la masa hay que incluir el propio 5.
solucion: Con F(x) = P(X ≤ x): P(X ≤ 5) = (1 + 2 + 3 + 4)/36 = 10/36 = 0,2778. Sumando la masa, p(2) + p(3) + p(4) + p(5) = 1/36 + 2/36 + 3/36 + 4/36, el mismo resultado. Y P(X = 6) = 5/36 es otra cosa: la masa de un valor suelto no es F.
:::

## Comprueba que lo sabes

:::quiz
p: En una variable aleatoria continua, ¿cuánto vale P(X = 2)?
o: La densidad evaluada en 2
o: Cero, y la probabilidad solo tiene sentido sobre intervalos
o: Depende de la forma de la distribución
a: 2
e: En una continua la probabilidad es área bajo la densidad, y un punto no tiene área. La densidad en 2 es una altura (probabilidad por unidad de x), no un área, y por eso puede valer más de 1.
:::

:::quiz
p: ¿Qué diferencia hay entre la función de masa y la función de distribución?
o: La de masa da P(X = x); la de distribución da P(X ≤ x) y vale para discretas y continuas
o: La de masa es para datos continuos y la de distribución para discretos
o: Son lo mismo, solo cambia el nombre según el libro
a: 1
e: La masa solo existe en variables discretas y da la probabilidad de cada valor suelto. La función de distribución es acumulada, F(x) = P(X ≤ x), y en el caso continuo se obtiene integrando la densidad. Con ella, cualquier intervalo sale como F(b) − F(a).
:::

:::quiz
p: Lanzas dos dados y X es la suma. ¿Cuánto vale P(X ≤ 4)?
o: 4/12 = 0,3333
o: 6/36 = 0,1667
o: 3/36 = 0,0833
a: 2
e: Las parejas que suman 2, 3 o 4 son 1, 2 y 3, en total 6 de los 36 resultados. Coincide con P(X = 7) = 6/36, pero es casualidad: el 7 tiene seis parejas propias y la cola de 2 a 4 acumula otras seis.
:::
