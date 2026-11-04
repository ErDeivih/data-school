---
id: lema-de-ito
titulo: Lema de Itô
fase: 9
nivel: experto
rutas: [quant]
prerequisitos: [ecuaciones-diferenciales-estocasticas, regla-de-la-cadena, retornos-logaritmicos]
tags: [ito, calculo, derivacion]
resumen: La regla de la cadena del cálculo estocástico: el término de segundo orden que aparece al derivar y que explica el menos sigma al cuadrado partido por dos.
fuentes: ["Itô (1951), 'On stochastic differential equations'", "Hull (2018), 'Options, Futures and Other Derivatives'"]
---

## En una frase

Si `X` sigue una ecuación diferencial estocástica y `f` es una función suave, entonces `f(X)`
sigue otra ecuación con un término extra `½·b²·f''` que en el cálculo normal no existe.

## La idea

En el cálculo de siempre, cuando derivas una función compuesta aplicas la regla de la cadena y
listo. El término de segundo orden de la expansión de Taylor se desprecia porque, al pasar al
límite, `(dx)²` es infinitamente más pequeño que `dx`.

Con un browniano eso deja de ser cierto. El incremento `dW` tiene un tamaño típico de `√dt`, así
que su cuadrado es del orden de `dt`: no es despreciable, es del mismo orden que el término
principal. El cálculo estocástico consiste, en el fondo, en no tirar ese cuadrado.

La consecuencia práctica es que derivar un precio no es derivar una función normal. Al pasar de
`S` a `ln S` aparece un término `−σ²/2` que reduce la media del logaritmo respecto a la deriva
`μ`. Ese término es la razón de que la rentabilidad compuesta de un activo sea menor que su
rentabilidad media, y es la pieza que faltaba en el capítulo anterior:
[[ecuaciones-diferenciales-estocasticas]] describe cómo se mueve `S`, y el lema de Itô dice cómo
se mueve cualquier función de `S`.

:::trampa
Aplicar la regla de la cadena normal a un proceso estocástico no da un error de redondeo: da un
resultado sistemáticamente equivocado. Si derivas `ln S` sin el término de Itô, tu media del
logaritmo crece como `μ` y tu simulación acaba por encima de la realidad en cualquier horizonte
largo. El error es pequeño al principio y crece con el tiempo, que es la peor forma de
equivocarse.
:::

## Definición formal

Sea `X_t` una EDE `dX = a dt + b dW` y `f(x, t)` una función con derivadas segundas continuas.
Entonces:

:::formula
df = ( f_t + a·f_x + ½·b²·f_xx ) dt + b·f_x·dW
:::

- `f_t`, `f_x`, `f_xx` — derivadas parciales de `f` respecto al tiempo, a `x` y segunda respecto a
  `x`.
- `a` y `b` — deriva y difusión del proceso, como en la página anterior.
- `½·b²·f_xx·dt` — el término de segundo orden; es lo que distingue a Itô de la regla de la
  cadena ordinaria.
- `b·f_x·dW` — la parte aleatoria, que se comporta como en el cálculo normal.

La regla mnemotécnica es la tabla de multiplicación del cálculo estocástico: `dt·dt = 0`,
`dt·dW = 0` y `dW·dW = dt`. Con ella, la expansión de Taylor a segundo orden se calcula sin
ambigüedad.

**El caso del logaritmo.** Con `f(x) = ln x`, `f_x = 1/x` y `f_xx = −1/x²`. Sustituyendo en el
GBM (`a = μS`, `b = σS`):

:::formula
d ln S = ( μ − σ²/2 ) dt + σ dW
:::

Ese `−σ²/2` es exactamente el que aparece en la solución del GBM y el que hace que la media
geométrica quede por debajo de la aritmética.

## Ejemplo

`μ = 8 %` y `σ = 30 %`. La media del logaritmo crece a `0,08 − 0,045 = 0,035` al año, no a 0,08.

En 10 años, la media de `ln(S_T/S_0)` es `0,35`, mientras que `μ·T = 0,80`. La diferencia, `0,45`,
es `σ²/2 · T`: no es ruido, es una corrección determinista que se acumula.

Traducido a riqueza: con `μ = 8 %`, la riqueza mediana crece como `e^{0,035·10} = 1,42` veces,
mientras que la riqueza media crece como `e^{0,08·10} = 2,23`. La media la empujan unas pocas
trayectorias que se disparan; la mediana describe a la persona típica. Ese hueco es el
[[volatility-drag]], y su origen es este término.

## Código

```python verificable
import numpy as np

# Un ano, 50.000 trayectorias: media del logaritmo frente a la media simple
rng = np.random.default_rng(11)
mu, sigma, reps = 0.08, 0.30, 50_000

log_r = (mu - 0.5 * sigma ** 2) + sigma * rng.standard_normal(reps)
simple = np.exp(log_r) - 1

print(f"media log {log_r.mean():.4f}")          # -> media log 0.0346
print(f"teorica {mu - 0.5 * sigma ** 2:.4f}")   # -> teorica 0.0350
print(f"media simple {simple.mean():.4f}")      # -> media simple 0.0827
print(f"exp(mu)-1 {np.exp(mu) - 1:.4f}")        # -> exp(mu)-1 0.0833
```

Las dos primeras líneas comprueban el lema: la media del logaritmo es `μ − σ²/2`, con el error de
simulación de 50.000 réplicas. Las dos últimas comprueban la otra cara: la media del retorno
simple es `e^{μ} − 1`, no `μ − σ²/2`. Las dos cosas son ciertas a la vez y describen a personas
distintas.

:::claves
- `0.5 * sigma ** 2` se resta **antes** de generar el ruido, porque es parte de la media del
  logaritmo, no del shock. Restarlo después de generar sería equivalente solo si lo aplicaras a
  todas las réplicas por igual, y entonces ya no sería una corrección del modelo.
- `np.exp(log_r) - 1` convierte log-retornos en retornos simples. La media de una exponencial no es
  la exponencial de la media: por eso `simple.mean()` no coincide con `exp(log_r.mean()) - 1`.
- `sigma * rng.standard_normal(reps)` usa la desviación del logaritmo, que es `σ` para el retorno
  logarítmico anual. Si usaras la del retorno simple, la conversión no sería exacta.
- El error de la media cae con `√reps`: con 50.000 réplicas ronda 0,0013, y por eso la diferencia
  entre 0,0346 y 0,0350 es ruido y no un fallo del lema.
- La identidad `E[exp(X)] = exp(μ + σ²/2)` para `X` normal es la que cierra el círculo: aplicada a
  `log_r`, da `exp(μ − σ²/2 + σ²/2) = exp(μ)`, que es la media del nivel.
:::

## Errores típicos

- **Derivar como en el cálculo ordinario.** Es el error de origen: sin el término `½b²f_xx`, el
  resultado es plausible y está mal.
- **Olvidar que `dW² = dt`.** Sin esa regla no se puede expandir Taylor a segundo orden y no hay
  forma de decidir qué términos sobreviven.
- **Aplicar el lema a una función que no es suave.** Con una función con un pico (un pago de
  opción en el strike, por ejemplo) las derivadas no existen en ese punto y hay que tratarlo
  aparte.
- **Confundir el lema de Itô con el de Stratonovich.** Los dos existen y dan fórmulas distintas;
  la diferencia está en cómo se define la integral. En finanzas se usa Itô porque el límite
  izquierdo es el que se puede cubrir en la práctica.
- **Usar retornos simples donde el lema pide logarítmicos.** El término `−σ²/2` sale de derivar el
  logaritmo. Si tu variable es el retorno simple, la fórmula cambia.
- **Creer que el término de segundo orden es un error numérico.** No se elimina refinando la
  simulación: es parte de la dinámica.

:::practica
enunciado: Con μ = 0,12 y σ = 0,40, calcula la media anual del log-retorno y la media anual del retorno simple. Explica cuál de las dos es mayor y por qué.
pista: La media del simple sale de la identidad de la exponencial de una normal.
solucion: La media del logaritmo es 0,12 − 0,08 = 0,04. La media del simple es exp(0,12) − 1 = 0,1275, es decir, un 12,75 %. La media del simple es mayor porque la exponencial es convexa: las trayectorias que suben mucho pesan más en la media aritmética que en la del logaritmo, mientras que la mediana de la riqueza crece como exp(0,04) − 1 = 4,08 %.
:::

## Comprueba que lo sabes

:::quiz
p: ¿De dónde sale el término −σ²/2 al aplicar el lema de Itô al logaritmo?
o: De la curvatura del logaritmo multiplicada por la varianza del ruido
o: De descontar los tipos de interés
o: De la deriva del activo, que ya lo incluía
a: 1
e: La segunda derivada de ln x es −1/x², y al multiplicarla por ½·b² (con b = σS) y dividir por x² queda −σ²/2. No tiene nada que ver con los tipos ni con la deriva: es pura curvatura.
:::

:::quiz
p: Con μ = 6 % y σ = 50 %, ¿cuál es la media anual del log-retorno?
o: 0,06 − 0,125 = −0,065, es decir, negativa
o: 0,06, porque la deriva no cambia al cambiar de escala
o: 0,06 + 0,125 = 0,185
a: 1
e: σ²/2 = 0,25/2 = 0,125. La media del logaritmo es 0,06 − 0,125 = −0,065: con esa volatilidad, la riqueza mediana se encoge aunque la media aritmética sea positiva. Es el ejemplo clásico de que una media positiva no garantiza que la mayoría gane.
:::
