---
id: criterio-de-kelly
titulo: Criterio de Kelly
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [valor-esperado, retornos-logaritmicos, varianza-y-desviacion]
tags: [posicion, capital, crecimiento, apuestas]
resumen: La fracción del capital que maximiza el crecimiento esperado a largo plazo: ni tan poca que desaprovechas la ventaja, ni tanta que una racha te saque de la ecuación.
fuentes: ["Kelly (1956), 'A New Interpretation of Information Rate'", "MacLean, Thorp y Ziemba (2011), 'The Kelly Capital Growth Investment Criterion'"]
---

## En una frase

El criterio de Kelly calcula qué fracción del capital conviene arriesgar en cada apuesta para
que el capital crezca lo más rápido posible a la larga, y su resultado sorprende a todo el mundo:
existe un óptimo, y pasarse de ese óptimo es tan malo como quedarse corto.

## La idea

Imagina una moneda cargada que sale cara el 55 % de las veces y cruz el 45 %, y que te pagan lo
mismo que apuestas. Es un juego con ventaja clara. Ahora la pregunta interesante: ¿cuánto
apuestas en cada tirada?

- Si apuestas 1 € siempre, tu capital crece en línea recta y tardarás una eternidad.
- Si apuestas todo el capital, aciertas muchas veces seguidas y multiplicas, pero basta una cruz
  para quedarte a cero. Con un 45 % de cruces, esa cruz llega pronto.
- Si apuestas una fracción fija del capital, hay un valor concreto que maximiza el crecimiento.

El razonamiento de Kelly es que lo que importa a largo plazo no es la media aritmética de los
resultados, sino la **media del logaritmo** del capital. La razón es que el capital se
multiplica: si ganas un 10 % y luego pierdes un 10 %, no vuelves al punto de partida, acabas un
1 % por debajo. El logaritmo convierte productos en sumas, y maximizar la suma esperada de
logaritmos es maximizar la tasa de crecimiento por operación. Esa tasa se llama **crecimiento
logarítmico** y es la que manda cuando juegas miles de veces.

De ahí sale la consecuencia más contraintuitiva de todo esto: si apuestas demasiado, tu
crecimiento esperado se vuelve **negativo** aunque cada apuesta tenga esperanza positiva. A eso
se le llama sobreapuesta o «variance drag»: la volatilidad te come el beneficio. En el ejemplo
de la moneda, con un 20 % del capital por tirada el crecimiento ya es negativo, y con un 30 %
pierdes dinero de forma sistemática.

Kelly maximiza el crecimiento, pero **no** maximiza la riqueza esperada (eso lo hace apostarlo
todo) y **no** controla el drawdown. Con Kelly completo la curva de capital es muy violenta, y
por eso en la práctica se usa medio Kelly o un cuarto de Kelly: se renuncia a un poco de
crecimiento a cambio de la mitad de volatilidad.

## Definición formal

**Apuesta binaria.** Ganas con probabilidad `p` una cantidad `b` por cada unidad arriesgada, y
pierdes la unidad con probabilidad `q = 1 − p`. La fracción óptima del capital es:

:::formula
f* = (p · b − q) / b = p − q / b
:::

:::formula
g(f) = p · ln(1 + f · b) + q · ln(1 − f)
:::

- `p` — probabilidad de ganar la apuesta.
- `q` — probabilidad de perder, `q = 1 − p`.
- `b` — ganancia por unidad arriesgada (con cuota 1:1, `b = 1`).
- `f` — fracción del capital que se apuesta en cada operación (0 ≤ `f` < 1).
- `g(f)` — tasa de crecimiento esperada por apuesta, en logaritmo natural. Es la media de
  `ln(1 + resultado)`.
- `f*` — la fracción que maximiza `g(f)`. Se obtiene igualando a cero la derivada.

**Versión continua.** Si los retornos siguen una normal con media `μ` y desviación típica `σ`
(por ejemplo, mensuales), el resultado es:

:::formula
f* = μ / σ²          g(f*) = μ² / (2 σ²) = S² / 2
:::

donde `S = μ / σ` es el [[ratio-de-sharpe]] del activo sin apalancar y `f*` se interpreta como
el apalancamiento óptimo. Con un Sharpe de 0,5, la tasa de crecimiento máxima teórica es
0,5² / 2 = 0,125, es decir un 12,5 % por periodo, pero solo si puedes apalancarte hasta `f*` y
rebalancear de forma continua. Ese «solo si» es donde se cae la mitad de la teoría.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p` | Probabilidad de ganar la apuesta | tanto por uno | Sube `f*` en la misma proporción: dos puntos de acierto más mueven la fracción óptima mucho más de lo que parece. Es también el parámetro peor estimado de todos |
| `q` | Probabilidad de perder, `q = 1 − p` | tanto por uno | Es lo que se resta en `f* = p − q/b`. Un punto más de `q` baja la fracción en algo más de un punto, porque además encarece el denominador |
| `b` | Ganancia por unidad arriesgada: con cuota 2:1, `b = 2` | adimensional | Reduce el castigo de perder: `f* = p − q/b` sube al crecer `b`. Por eso la misma probabilidad de acierto pide fracciones muy distintas según lo que paguen |
| `f` | Fracción del capital apostada en cada operación, `0 ≤ f < 1` | tanto por uno | Es la decisión, no un dato. El crecimiento es máximo en `f*` y vuelve a bajar a los dos lados, así que pasarse es tan malo como quedarse corto |
| `g(f)` | Tasa de crecimiento esperada por apuesta: la media de `ln(1 + resultado)` | logaritmo natural por apuesta | Es la pendiente del capital en escala logarítmica. Con `g` negativo el capital mediano baja aunque la esperanza aritmética de cada apuesta sea positiva |
| `f*` | La fracción que maximiza `g(f)`, donde la derivada se anula | tanto por uno | En la versión continua vale `μ / σ²` y en la discreta `p − q/b`. Se calcula con estimaciones, así que hereda todo su error y conviene usar la mitad o un cuarto |
| `μ` | Retorno esperado por periodo del activo en la versión continua | tanto por uno por periodo | Entra en el numerador de `f* = μ / σ²`: doblar la rentabilidad esperada dobla el apalancamiento que pide la fórmula, con el mismo riesgo |
| `σ` | Desviación típica del retorno por periodo | tanto por uno por periodo | Entra **al cuadrado**, y por eso manda tanto: con la mitad de volatilidad la fracción óptima se multiplica por cuatro. Es también la magnitud que se estima con menos error |
| `S = μ / σ` | [[ratio-de-sharpe]] del activo sin apalancar | adimensional | La tasa de crecimiento máxima teórica es `S² / 2`: con `S = 0,5` son 0,125 por periodo. La relación es cuadrática, así que doblar el Sharpe cuadruplica el crecimiento disponible |
:::

:::nota
En tiempo continuo, con Kelly completo, la probabilidad de llegar a estar alguna vez un 50 %
por debajo del capital inicial es del 25 %, y la de caer al 10 % es del 1 %. No es una opinión:
sale de la fórmula de primera llegada de un movimiento browniano geométrico. Kelly protege el
crecimiento, no tu estómago.
:::

:::figura
fichero: kelly-crecimiento-y-sobreapuesta
pie: A la izquierda, el crecimiento esperado por tirada según la fracción que apuestes: sube hasta el máximo en `f* = 0,10` (+0,50 % por tirada) y a partir de ahí cae, cruza el cero en `f = 0,20` y se hunde. La zona roja es lo que casi nadie espera: con el 20 % del capital ya pierdes dinero en promedio aunque el 55 % de las tiradas ganen. A la derecha, la misma apuesta jugada 400 veces con cuatro tamaños, en escala logarítmica para que las pendientes se puedan comparar: el 0,10 multiplica el capital típico por 7,4, el 0,20 se queda plano y el 0,30 lo deja en 1,50 € de cada 1.000. Lo que decide no es acertar más, es cuánto arriesgas.
fuente: figuras/criterio-de-kelly-1.py
:::

## Ejemplo

La moneda del 55 % con cuota 1:1, capital inicial 1.000 €:

- `p = 0,55`, `q = 0,45`, `b = 1` → `f* = 0,55 − 0,45 = 0,10`. Apuesta el **10 %** del capital.
- Con 1.000 €, eso son 100 € en la primera tirada.

Y así se comporta el crecimiento según la fracción que arriesgues:

| Fracción f | Crecimiento por apuesta |
| --- | --- |
| 0,00 | 0,0000 % |
| 0,05 | +0,3753 % |
| 0,10 | +0,5008 % |
| 0,15 | +0,3736 % |
| 0,20 | −0,0138 % |
| 0,30 | −1,6203 % |

Mira las tres filas de en medio. Con `f = 0,15` arriesgas un 50 % más que con `f = 0,05` y
creces **menos**. Con `f = 0,20` ya pierdes dinero en promedio, aunque el 55 % de las tiradas
sean ganadoras. Y en el máximo, `f = 0,10`, el crecimiento es solo del 0,5 % por tirada: el
juego tiene ventaja, pero la ventaja es pequeña y no admite alegrías.

**Con la cuota cambia todo.** Si en vez de 1:1 te pagaran 2 por cada 1 arriesgado, con la misma
probabilidad del 55 %, la fracción óptima sube a `0,55 − 0,45 / 2 = 0,325`, casi un tercio del
capital. La lección: `f*` no depende solo de acertar más o menos, depende de **cuánto te pagan
cuando aciertas**.

**Caso continuo.** Una estrategia con un 1 % de exceso mensual y un 4 % de volatilidad mensual
tiene `f* = 0,01 / 0,04² = 6,25`, es decir, pide apalancarse 6,25 veces. Con esa palanca, la
volatilidad anual resultante sería del **86,6 %**. Ahí se ve por qué nadie usa Kelly completo:
las estimaciones de `μ` tienen mucho error y el resultado es una curva que casi nadie aguanta.

## Código

```python verificable
import numpy as np

p = 0.55                     # probabilidad de ganar
b = 1.0                      # se gana 1 por cada 1 arriesgado
q = 1 - p
f_kelly = (p * b - q) / b    # fraccion optima del capital

def crecimiento(f):
    """Crecimiento esperado por apuesta: media de log(1 + resultado)."""
    return p * np.log(1 + f * b) + q * np.log(1 - f)

print(f"fraccion de Kelly {f_kelly:.2f}")            # -> fraccion de Kelly 0.10
for f in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30):
    print(f"f={f:.2f}  crecimiento {crecimiento(f):+.4%}")
# El maximo esta en f=0.10 (+0.5008 %), que es f*; en f=0.20 el crecimiento
# ya es negativo (-0.0138 %) aunque cada apuesta tenga esperanza positiva.
```

:::claves
- `np.log(1 - f)` con `f = 1` da `-inf` y con `f > 1` da `nan`, porque el logaritmo de un número negativo no existe. La función solo tiene sentido con `0 ≤ f < 1` y no lo comprueba: si le pasas un 1,2 el resultado es un `nan` que se propaga sin lanzar ninguna excepción.
- `q = 1 - p` no da exactamente 0,45 en coma flotante, sino 0,44999999999999996, así que `f_kelly` vale 0,10000000000000003. El `:.2f` del `print` lo disimula, pero comparar `f_kelly == 0.1` sería `False`. Redondear no es un adorno aquí.
- La función devuelve la media del logaritmo, no el logaritmo de la media. `p * np.log(1 + f*b) + q * np.log(1 - f)` y `np.log(p*(1 + f*b) + q*(1 - f))` se parecen en el código y son cosas distintas: la segunda es el logaritmo de la esperanza y su máximo está en apostarlo todo.
- El resultado es un `np.float64`, no un `float` de Python. Al imprimir con `%` da igual, pero al serializar a JSON o al comparar tipos hay que envolverlo en `float(...)`.
- En `f = 0.0` el crecimiento es exactamente 0,0 y `np.log(1)` no avisa de nada: es el único punto del bucle en el que la apuesta no cambia el capital, y por eso sirve de referencia contra la que leer los demás.
:::

```python verificable
import numpy as np

# Version continua: con retornos normales la fraccion de Kelly es mu / sigma^2.
mu_mensual, sigma_mensual = 0.01, 0.04      # 1 % de exceso y 4 % de volatilidad al mes
f_kelly = mu_mensual / sigma_mensual ** 2

print(f"Kelly completo {f_kelly:.2f}x")                          # -> 6.25x
print(f"medio Kelly    {f_kelly / 2:.2f}x")                      # -> 3.12x
print(f"volatilidad anual al Kelly completo {f_kelly * sigma_mensual * np.sqrt(12):.2%}")
# -> 86.60%

# La cuota cambia la fraccion: con la misma probabilidad, pagar 2 por 1 permite mas.
p = 0.55
print(f"con cuota 2:1 la fraccion seria {p - (1 - p) / 2:.2f}")   # -> 0.33
```

```python ilustrativo
import pandas as pd

# Kelly sobre los resultados de un backtest real: aqui esta el problema de verdad.
operaciones = pd.read_csv("resultados_backtest.csv")     # fichero externo
r = operaciones["r_multiplo"]

p = (r > 0).mean()                                  # tasa de acierto estimada
b = r[r > 0].mean() / abs(r[r < 0].mean())          # pago medio frente a perdida media
f = p - (1 - p) / b

# Tanto p como b son estimaciones con error, y el error se amplifica en f.
# Por eso se usa medio Kelly o un cuarto de Kelly, nunca el valor completo.
print(f"p={p:.3f}  b={b:.2f}  Kelly={f:.3f}  medio Kelly={f / 2:.3f}")
```

## Errores típicos

- **Aplicar Kelly completo con parámetros estimados.** `f*` depende de `p` y `b`, que son
  estimaciones. Un error de dos puntos en la probabilidad de acierto mueve la fracción óptima
  muchísimo, y el error casi siempre va en la dirección de sobreapostar. Usa medio Kelly o un
  cuarto, y comprueba cuánto cambia `f*` con un intervalo de confianza de `p`.
- **Usar `μ / σ²` con retornos que no son normales.** Con colas gruesas y asimetría, la fórmula
  continua se queda corta en el riesgo. Si tu estrategia vende opciones o tiene colas gruesas,
  la varianza no describe la pérdida mala.
- **Confundir Kelly con maximizar el beneficio esperado.** El beneficio esperado se maximiza
  apostándolo todo, y así es como se arruina uno. Kelly maximiza el crecimiento geométrico, que
  es otra cosa.
- **Ignorar los costes.** Las comisiones y el deslizamiento ([[slippage-y-comisiones]]) bajan
  `μ` y dejan `σ` igual, así que reducen `f*` sin que te enteres. Un Kelly calculado sobre un
  backtest sin costes está pidiendo demasiado tamaño.
- **Creer que Kelly elimina el riesgo de ruina.** Kelly completo significa una probabilidad del
  25 % de estar alguna vez un 50 % por debajo. No es un sistema conservador; es un sistema que
  maximiza el crecimiento y acepta el camino que haga falta. Mira [[riesgo-de-ruina]].
- **Recalcular el Kelly en cada operación con la ventana más corta posible.** Si `p` se estima
  con 20 operaciones, la fracción oscila sin sentido. Estima con una ventana larga y mueve el
  tamaño poco a poco.

:::practica
enunciado: Una apuesta gana el 60 % de las veces y paga 3 por cada unidad arriesgada. Calcula la fracción de Kelly y cuánto apostarías en la primera jugada con una cuenta de 20.000 €. Compara con el mismo 60 % pero cuota 1:1 y explica la diferencia.
pista: Con cuota b, la fórmula es f* = p − q / b, así que lo que te pagan también manda.
solucion: Con b = 3, q = 0,40: f* = 0,60 − 0,40 / 3 = 0,60 − 0,133 = 0,467. Sobre 20.000 € son 9.333 €. Con cuota 1:1 sería f* = 0,60 − 0,40 = 0,20, unos 4.000 €. La probabilidad de acertar es la misma, pero triplicar el pago más que duplica la fracción óptima: Kelly no solo mira cuántas veces ganas.
:::

## Comprueba que lo sabes

:::quiz
p: En la moneda del 55 % con cuota 1:1, apostar el 20 % del capital en cada tirada...
o: ...da más beneficio que el 10 %, porque arriesgas el doble en un juego con ventaja
o: ...da un crecimiento esperado ligeramente negativo, porque la volatilidad se come la ventaja
o: ...es imposible, porque el capital nunca llegaría a cero
a: 2
e: Con f = 0,20 la media de ln(1 + resultado) es −0,0138 % por tirada: la ventaja del 55 % no compensa la pérdida que produce la volatilidad. El crecimiento es máximo en f = 0,10, y a partir de ahí tanto da arriesgar más como menos: el 0,15 crece menos que el 0,05.
:::

:::quiz
p: Una estrategia tiene un exceso de rentabilidad del 1 % mensual y una volatilidad del 4 % mensual. ¿Qué fracción de Kelly pide la fórmula continua?
o: 0,25, porque es el ratio entre media y desviación
o: 6,25, porque es la media dividida entre la varianza
o: 0,16, porque hay que multiplicar la media por la desviación
a: 2
e: La fórmula continua es f = μ / σ², y 0,01 / 0,0016 = 6,25. Es decir, pide apalancarse 6,25 veces, lo que da una volatilidad anual del 86,6 %. Ese resultado absurdo en la práctica es la mejor prueba de que Kelly completo no se usa tal cual.
:::

:::quiz
p: ¿Por qué el criterio de Kelly maximiza el logaritmo del capital y no el capital esperado?
o: Porque el capital se multiplica entre operaciones y a largo plazo domina la tasa de crecimiento geométrico, no la media aritmética
o: Porque el logaritmo hace que las pérdidas no cuenten
o: Porque maximizar el capital esperado es imposible de calcular
a: 1
e: Al reinvertir, el capital final es un producto de factores, y el logaritmo lo convierte en una suma cuya media se puede maximizar. Maximizar el capital esperado llevaría a apostarlo todo, que arruina con probabilidad 1 en cualquier juego con pérdida posible.
:::

:::trampa
Kelly es muy sensible a la ventaja estimada. Si crees que tu tasa de acierto es del 55 % pero en
realidad es del 52 %, el 10 % de Kelly se convierte en una sobreapuesta. Antes de calcular una
fracción de Kelly, pregunta cuántas operaciones sostienen esa `p` y cuál es su intervalo de
confianza. Si la respuesta es «pocas», el número que salga no significa nada.
:::
