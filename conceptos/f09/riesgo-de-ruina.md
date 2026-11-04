---
id: riesgo-de-ruina
titulo: Riesgo de ruina
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [criterio-de-kelly, valor-esperado, probabilidad-axiomas]
tags: [riesgo, ruina, rachas, capital]
resumen: La probabilidad de perder el capital, o de llegar a un nivel del que ya no puedes seguir, antes de que la ventaja de tu sistema tenga tiempo de imponerse.
fuentes: ["Feller (1968), 'An Introduction to Probability Theory and Its Applications, Vol. 1'", "MacLean, Thorp y Ziemba (2011), 'The Kelly Capital Growth Investment Criterion'"]
---

## En una frase

El riesgo de ruina es la probabilidad de quedarte sin capital antes de que la ventaja de tu
sistema se note, y depende casi por completo de una sola decisión: cuánto arriesgas en cada
operación.

## La idea

Hay un resultado clásico de probabilidad que se llama ruina del jugador. Imagina que apuestas
un euro a cara o cruz, con una moneda justa, contra alguien que tiene una fortuna enorme. Da
igual con cuánto empieces: si juegas el tiempo suficiente, acabarás sin dinero. Es aritmética,
no mala suerte. Con esperanza cero y un rival con más capital que tú, la ruina es
cuestión de tiempo.

Ahora cambia la moneda por una con ventaja: ganas el 55 % de las veces. ¿Te salva eso? Solo en
parte. Te salva **si el tamaño de tus apuestas es pequeño respecto a tu capital**.

Si arriesgas
mucho, puedes tener cinco pérdidas seguidas en la primera hora y quedarte fuera de juego, y da lo
mismo que tu sistema «a la larga» gane dinero: a la larga no vas a llegar.

La intuición central es que la probabilidad de ruina baja **exponencialmente** con el número de
unidades de riesgo que tienes. Y el número de unidades de riesgo es, precisamente, lo contrario
del tamaño de tus apuestas: si arriesgas un 2 % del capital en cada operación, tienes 50
unidades; si arriesgas un 10 %, tienes 10. Pasar de 2 % a 10 % no multiplica el riesgo de ruina
por cinco, lo multiplica por miles.

Hay una trampa de vocabulario que conviene deshacer. En este modelo, «ruina» significa llegar a
cero. En la vida real, la ruina llega mucho antes: cuando el bróker te cierra la posición, cuando
tocas el límite de pérdida diaria de una [[prueba-de-fondeo]], o cuando decides que ya no
aguantas más y cierras la cuenta. Todas esas son barreras, y la probabilidad de tocarlas se
calcula con la misma lógica: cambia el cero por el nivel que no puedes cruzar.

## Definición formal

**Modelo clásico.** Apuestas una unidad fija en cada ronda: ganas una unidad con probabilidad
`p` y pierdes una unidad con probabilidad `q = 1 − p`. Empiezas con `N` unidades y la ruina es
llegar a 0 unidades.

:::formula
P(ruina) = (q / p)^N        si p > q
:::

:::formula
P(ruina) = 1               si p ≤ q
:::

- `p` — probabilidad de ganar una unidad en una ronda.
- `q` — probabilidad de perderla, `q = 1 − p`.
- `N` — capital medido en unidades de riesgo, no en euros. Si arriesgas una fracción `r` del
  capital en cada operación y el tamaño de la apuesta no se reajusta, `N = 1 / r`.
- `q / p` — el «precio» de tu desventaja por unidad. Con `p = 0,55` vale 0,818; con `p = 0,51`
  vale 0,961, y fíjate en lo rápido que se acerca a 1: cuanto menor es la ventaja, más capital
  necesitas para el mismo riesgo.

Si el rival no es infinito sino que tiene `N_total − i` unidades y tú empiezas con `i`, la
probabilidad de arruinarte antes de dejarlo seco es:

:::formula
P = ( (q/p)^i − (q/p)^N_total ) / ( 1 − (q/p)^N_total )
:::

que tiende a `(q/p)^i` cuando `N_total` crece. Es la versión útil cuando tienes un objetivo
concreto («duplicar antes de arruinarme»), no solo una barrera.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p` | Probabilidad de ganar una unidad en una ronda | tanto por uno | Sube el denominador de `q/p`, así que la ruina baja en picado: la curva es exponencial en `N` y también en la ventaja. Un punto más de acierto multiplica el capital que necesitas para el mismo riesgo |
| `q` | Probabilidad de perderla, `q = 1 − p` | tanto por uno | Sube `q/p`, el «precio» de tu desventaja. Cuando `q/p` se acerca a 1 el exponente tiene que ser enorme para compensar: con `p = 0,51` la base es 0,961 y la ruina tarda muchísimo más en bajar |
| `N` | Capital medido en **unidades de riesgo**, no en euros: con un riesgo del 2 % por operación, `N = 50` | unidades de riesgo | Es el exponente de `(q/p)^N` y por eso domina todo: pasar de 50 unidades a 10 no multiplica la ruina por 5, la multiplica por miles. En la práctica `N = 1 / riesgo` |
| `riesgo` | Fracción del capital que arriesgas en cada operación | tanto por uno | Es el inverso de `N`: doblar el riesgo a la mitad de unidades deja el riesgo de ruina elevado al cuadrado. Es la única palanca que se toca de verdad en el día a día |
| `q / p` | El «precio» de la desventaja por unidad, siempre menor que 1 si tienes ventaja | adimensional | Al acercarse a 1 la curva se aplana y hace falta mucho más capital para el mismo riesgo. Con `p = 0,55` vale 0,818; con `p = 0,51`, 0,961 |
| `P(ruina)` | Probabilidad de tocar cero en algún momento, con tiempo ilimitado | tanto por uno | Es una probabilidad de **toda la vida** de la cuenta, no de las próximas 200 operaciones: por eso la simulación de la página da cifras algo más bajas que la fórmula |
| `N_total` | Capital total del rival o del mercado, en unidades | unidades de riesgo | Solo aparece en la versión con objetivo: al crecer, el término se desvanece y la probabilidad tiende a `(q/p)^i`. Con un rival muy grande, esa versión y la clásica coinciden |
:::

:::aviso
Dos supuestos del modelo que en la práctica se rompen: las operaciones son **independientes** y
el tamaño de la apuesta es **constante** en unidades. Si tus posiciones están correlacionadas
(cinco apuestas al mismo sector son casi una), el número efectivo de unidades es mucho menor que
el que crees. Y con tamaño proporcional al capital (riesgo fijo porcentual) el capital nunca
llega a cero en el modelo, así que la ruina hay que definirla contra una barrera.
:::

:::figura
fichero: riesgo-ruina-tamano-y-acantilado
pie: A la izquierda, la probabilidad de arruinarse en algún momento según lo que arriesgues por operación, con la misma ventaja del 55 %: baja de forma exponencial, no lineal. Con el 2 % por operación es del 0,0044 % y con el 10 % sube al 13,44 %, unas 3.000 veces más, sin que la estrategia haya cambiado en nada. A la derecha, la simulación de 20.000 caminos de 200 operaciones: con el 2 % no se arruina ninguno y solo el 0,31 % llega a perder la mitad; con el 10 % se arruina el 11,83 % y el 35,11 % pasa por una caída del 50 %. La diferencia entre el 13,44 % de la fórmula y el 11,83 % de la simulación es el tiempo: la fórmula juega para siempre y la simulación solo 200 operaciones.
fuente: figuras/riesgo-de-ruina-1.py
:::

## Ejemplo

Con `p = 0,55` (ventaja del 10 % sobre una moneda justa) y apuestas de una unidad, la
probabilidad de arruinarse según cuánto arriesgues por operación es esta:

| Riesgo por operación | Unidades de capital | P(ruina) |
| --- | --- | --- |
| 1 % | 100 | 0,0000002 % |
| 2 % | 50 | 0,0044 % |
| 5 % | 20 | 1,81 % |
| 10 % | 10 | 13,44 % |
| 20 % | 5 | 36,66 % |

(Los valores salen de `(0,45 / 0,55)^N`. Con 100 unidades el exponente es −20 y el número es
diminuto; con 5 unidades es −1 y queda un tercio.)

Lee la tabla despacio, porque es la lección entera de este concepto:

- Con la **misma ventaja** del 55 %, arriesgar el 2 % te da un riesgo de ruina de 0,0044 % y
  arriesgar el 10 % te da un 13,44 %. El segundo riesgo es **unas 3.000 veces mayor**.
- La diferencia no está en la estrategia, está en el tamaño. Dos personas con el mismo sistema y
  distinto tamaño de posición no están jugando al mismo juego.
- Incluso con un 20 % por operación, que parece una barbaridad, el sistema sigue teniendo
  esperanza positiva. El problema no está en la esperanza, sino en que no vas a llegar a cobrarla.

La simulación con 20.000 caminos de 200 operaciones confirma el orden de magnitud: con un 2 %
por operación no se arruina ningún camino y solo el 0,31 % sufre una caída del 50 %; con un 10 %
se arruina el 11,83 % y más de un tercio (35,11 %) pasa por una caída del 50 %. La simulación da
cifras algo más bajas que la fórmula porque solo juega 200 operaciones, mientras que la fórmula
calcula la probabilidad de arruinarse en algún momento, con tiempo ilimitado.

## Código

```python verificable
import numpy as np

p, q = 0.55, 0.45            # probabilidad de ganar y de perder, pago 1:1

def ruina(riesgo_por_operacion):
    """Capital medido en unidades de riesgo: N = 1 / riesgo."""
    return (q / p) ** (1 / riesgo_por_operacion)

for r in (0.01, 0.02, 0.05, 0.10, 0.20):
    print(f"riesgo {r:>5.0%}  unidades {1 / r:>4.0f}  ruina {ruina(r):.2e}")
# -> riesgo    2%  unidades   50  ruina 4.39e-05
# -> riesgo   10%  unidades   10  ruina 1.34e-01

print(f"el 10% arriesga {ruina(0.10) / ruina(0.02):.0f} veces mas que el 2%")   # -> 3062
```

:::claves
- `ruina()` devuelve una probabilidad en tanto por uno: `ruina(0.10)` es 0,1344, no 13,44. Multiplicar por 100 para leerla en porcentaje es cosa de quien la usa, y el `:.2e` del `print` la deja en notación científica, que es lo que hace falta para ver de un vistazo que el 1 % y el 10 % no están en la misma escala.
- `1 / riesgo` es el número de unidades `N`, así que el argumento va en tanto por uno. Llamar a `ruina(2)` «con un riesgo del 2 %» da `(0,45/0,55)^0,5 = 0,90`: un 90 % de ruina en vez de un 0,0044 %. La función no comprueba el rango y el resultado sigue siendo un número plausible.
- La fórmula solo vale con `p > q`. Con `p = 0,45` y `q = 0,55` devuelve un número **mayor que 1**, que no es una probabilidad; y con `p = q = 0,5` devuelve exactamente 1,0. El caso sin ventaja es una línea aparte en la página y el código no la implementa.
- `(q/p) ** N` se va a cero tan rápido que en coma flotante acaba siendo `0.0` exacto: con `r = 0,001` el exponente es 1.000 y el resultado ya ronda 10⁻⁸⁸, y con riesgos más pequeños se pierde por completo. Es la razón de que la tabla se corte en el 1 %.
- La razón entre las dos probabilidades, 3.062, es un cociente de riesgos de ruina y no de riesgos por operación: el segundo se multiplica por 5 y el primero por miles. Ese cociente es la lección entera del concepto.
:::

```python verificable
import numpy as np

# Simulacion con apuesta de tamano fijo: cada operacion suma o resta `riesgo`
# unidades del capital inicial (no se reajusta el tamano al capital actual).
rng = np.random.default_rng(7)
n_ops, n_caminos = 200, 20_000
resultados = rng.choice([1.0, -1.0], size=(n_caminos, n_ops), p=[0.55, 0.45])

for riesgo in (0.02, 0.10):
    capital = 1 + riesgo * np.cumsum(resultados, axis=1)
    ruina_total = (capital <= 0).any(axis=1)
    caida_mitad = (capital <= 0.5).any(axis=1)
    print(f"riesgo {riesgo:>4.0%}  ruina {ruina_total.mean():6.2%}  caida del 50% {caida_mitad.mean():6.2%}")
# -> riesgo   2%  ruina  0.00%  caida del 50%  0.31%
# -> riesgo  10%  ruina 11.83%  caida del 50% 35.11%
```

## Errores típicos

- **Creer que un sistema con esperanza positiva no puede arruinarse.** Puede, y es lo más
  habitual. La esperanza es una propiedad de la estrategia; la ruina es una propiedad de la
  estrategia **y** del tamaño de las posiciones.
- **Confundir riesgo de ruina con la probabilidad de una racha perdedora.** La racha es un
  suceso observable; la ruina es el resultado de que esa racha llegue cuando tu capital ya está
  bajo. Puedes sobrevivir a diez pérdidas seguidas con un 1 % de riesgo y no sobrevivir a cuatro
  con un 25 %.
- **Calcular el riesgo de ruina con la racha más larga que has visto en tu histórico.** Es el
  error más peligroso. La racha futura puede ser más larga que la pasada, y el modelo no
  necesita conocerla: solo necesita el tamaño relativo de tus apuestas.
- **Ignorar la correlación entre posiciones.** Diez apuestas al mismo sector en el mismo día son,
  a efectos de ruina, casi una sola apuesta diez veces más grande. El número de unidades de
  riesgo que tienes es mucho menor que el que dice tu hoja de cálculo.
- **Usar la fórmula clásica con tamaño proporcional al capital.** Si tu riesgo es un porcentaje
  fijo del capital actual, tus apuestas se encogen cuando pierdes y el capital nunca llega a
  cero en el modelo. La ruina hay que definirla contra una barrera (un −30 %, un límite diario),
  y para eso lo correcto es simular ([[simulacion-de-monte-carlo]]).
- **Bajar el tamaño después de una racha, cuando ya estás en el mínimo.** Reducir el riesgo
  cuando el capital ha caído es matemáticamente correcto con riesgo fijo porcentual, pero
  muchas veces se hace justo al revés, subiéndolo para «recuperar lo perdido». Eso es
  lo que maximiza la probabilidad de ruina, y es el terreno de
  [[psicologia-del-trading]].

:::practica
enunciado: Un sistema gana el 53 % de las operaciones con pago 1:1 y apuestas de tamaño fijo. Calcula el riesgo de ruina si arriesgas el 4 % del capital por operación, y compáralo con arriesgar el 2 % y el 1 %.
pista: Con pago 1:1, N es el número de unidades de riesgo, N = 1 / riesgo, y la fórmula es (q/p)^N.
solucion: q/p = 0,47 / 0,53 = 0,8868. Con riesgo del 4 % hay N = 25 unidades: 0,8868^25 = 0,0496, un 4,96 %. Con el 2 %, N = 50: 0,8868^50 = 0,00246, un 0,25 %. Con el 1 %, N = 100: 0,8868^100 = 6,06 · 10^-6. La ventaja es la misma en los tres casos, pero bajar el riesgo a la mitad rebaja la ruina unas veinte veces: manda el tamaño.
:::

## Comprueba que lo sabes

:::quiz
p: Con una ventaja del 55 % y apuestas de una unidad, ¿por qué pasar de arriesgar el 2 % al 10 % por operación multiplica el riesgo de ruina por miles y no por cinco?
o: Porque el riesgo de ruina es exponencial en el número de unidades de capital, y ese número cae de 50 a 10
o: Porque con el 10 % la esperanza del sistema se vuelve negativa
o: Porque el 10 % provoca más comisiones
a: 1
e: La fórmula es (q/p)^N, con N = 1/riesgo. Al pasar de 50 a 10 unidades, el exponente baja de 50 a 10, y una base menor que 1 elevada a exponentes muy distintos da resultados incomparables: 4,39e-05 frente a 1,34e-01. La esperanza del sistema no cambia con el tamaño.
:::

:::quiz
p: ¿Qué significa «ruina» en la práctica si arriesgas un porcentaje fijo del capital en cada operación?
o: Que el capital llega exactamente a cero
o: Que el capital toca una barrera por debajo de la cual ya no puedes operar, porque con tamaño proporcional nunca llega a cero
o: Que pierdes más de diez operaciones seguidas
a: 2
e: Con riesgo fijo porcentual, cada pérdida encoge la apuesta, así que el capital se acerca a cero sin alcanzarlo en el modelo. Por eso la ruina se define contra una barrera real: el límite del bróker, la regla de una prueba de fondeo o tu propio umbral de abandono.
:::

:::quiz
p: ¿Cuál de estos dos sistemas tiene más riesgo de ruina, si los dos tienen la misma ventaja del 55 %?
o: El que arriesga el 5 % del capital por operación
o: El que arriesga el 1 % del capital por operación
o: Los dos igual, porque la ventaja es la misma
a: 1
e: La ventaja es idéntica, pero el riesgo de ruina depende del número de unidades de capital: (0,45/0,55)^20 = 1,81 % frente a (0,45/0,55)^100, que es del orden de 10^-9. El tamaño de la posición es la variable que domina.
:::
