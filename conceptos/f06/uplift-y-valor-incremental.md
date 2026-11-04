---
id: uplift-y-valor-incremental
titulo: Uplift y valor incremental
fase: 6
nivel: avanzado
rutas: [ds]
prerequisitos: [metricas-de-clasificacion, train-val-test, arboles-de-decision]
tags: [causalidad, marketing, clasificacion]
resumen: El efecto de intervenir frente a no hacerlo, medido sobre quien de verdad cambia de comportamiento y no sobre quien ya iba a comprar.
fuentes: ["Künzel et al. (2019), 'Metalearners for estimating heterogeneous treatment effects using machine learning'", "Athey y Imbens (2017), 'The State of Applied Econometrics: Causality and Policy Evaluation'"]
---

## En una frase

El uplift de un cliente es cuánto cambia su probabilidad de comprar **porque** le has intervenido, y
no se mide con su probabilidad de comprar, sino comparando clientes idénticos tratados y no
tratados.

## La idea

Una tienda manda un cupón a sus clientes y mide quién compra después. Los que compran son muchos,
pero parte de esa gente habría comprado igual sin cupón. Solo el **incremental** —los que compran
por el cupón y no habrían comprado sin él— es el valor que generó la campaña. El resto es gasto
disfrazado de éxito.

Pero hay un hueso duro: para un cliente concreto **nunca puedes observar las dos cosas**. O le
mandas el cupón, o no. El resultado que no ocurrió (el contrafactual) no está en tus datos. Por eso
el uplift no se aprende como una probabilidad: no tienes etiqueta por cliente, tienes un experimento
con dos grupos comparables. Comparando su conversión aparecen cuatro tipos de cliente:

- **Los que responden.** Compran con la campaña y no sin ella. Son el objetivo.
- **Los que siempre compran.** Convertirían igual: intervenirles cuesta dinero y no cambia nada.
- **Los que nunca compran.** No hay campaña que los mueva.
- **Los que empeoran.** Un correo insistente puede recordarle a alguien que quería darse de baja. Su
  uplift es **negativo** y, si no los detectas, tu campaña se los cobra a los que responden.

Tres formas de estimarlo:

1. **Dos modelos.** Uno con los tratados y otro con los controles; el uplift de un cliente es la
   diferencia de sus predicciones. Fácil de explicar, pero cada modelo ve la mitad de los datos y
   sus errores se restan sin cancelarse.
2. **Un modelo con el tratamiento como variable.** Añades la columna «fue tratado» y predices la
   conversión; el uplift es la predicción con tratamiento a 1 menos con tratamiento a 0. Usa todos
   los datos, pero el modelo se apoya en el efecto medio y aplana las diferencias entre clientes.
3. **Transformar la clase.** Conviertes el problema en una clasificación normal con una etiqueta
   inventada y predices directamente quién responde. Es la más limpia y la que menos código necesita.

## Definición formal

Con `T` la variable que dice si el cliente fue tratado (1) o no (0), e `Y` la que dice si compró
(1) o no (0), el efecto individual es:

:::formula
τ(x) = E[ Y(1) − Y(0) | X = x ]
:::

`Y(1)` es lo que habría pasado con tratamiento e `Y(0)` lo que habría pasado sin él. Los dos no se
observan a la vez: para cada cliente solo ves uno.

La transformación de clase convierte esto en una clasificación binaria normal. Se define una
etiqueta `J` que invierte el resultado de los controles, y una versión simétrica `z` que va de `−1`
a `+1`:

:::formula
J = T · Y + (1 − T) · (1 − Y)        z = 2Y − 1
:::

La etiqueta `z` sale del resultado observado, no de `J`: vale `+1` si el cliente convirtió y `−1`
si no, en los dos grupos. La `J` solo existe para poder usar un clasificador normal; todas las
cuentas de uplift se hacen con `z`.

Un clasificador entrenado para predecir `z` aprende, sin saberlo, a distinguir a quien responde del
que no. El uplift se recupera con una media de las predicciones del modelo en cada grupo:

:::formula
τ(x) ≈ ½ · E[z | T = 1, x] − ½ · E[z | T = 0, x]
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `T` | Tratamiento: 1 si el cliente recibió la intervención, 0 si no | 0 o 1 | Es la asignación; su media es la fracción tratada `u` |
| `Y` | Resultado observado: 1 si convirtió, 0 si no | 0 o 1 | — |
| `Y(1)`, `Y(0)` | Resultado potencial con y sin tratamiento (nunca se ven los dos) | 0 o 1 | — |
| `τ(x)` | Uplift: el efecto del tratamiento para un cliente con características `x` | probabilidad, −1 a 1 | Es lo que se quiere estimar y lo que ordena a quién intervenir |
| `J` | Etiqueta transformada: el resultado del tratado, y el resultado **contrario** del control | 0 o 1 | — |
| `z` | La misma etiqueta en escala simétrica: `+1` si convirtió, `−1` si no | −1 o +1 | — |
| `u` | Fracción de clientes tratados en el experimento | tanto por uno, 0 a 1 | Con `u` muy cerca de 0 o de 1, el grupo pequeño apenas informa y la estimación se vuelve ruidosa |
| `½` | El factor que devuelve la escala de `z` (de −1 a 1) a escala de probabilidad | adimensional | Olvidarlo duplica el uplift estimado |
| `π(x)` | Probabilidad de conversión estimada por el modelo | 0 a 1 | Se usa para comparar, pero no es la cantidad que decide a quién intervenir |
:::

Dos requisitos que **no** son opcionales:

1. **Los grupos tienen que ser comparables.** Si el cupón se envió a los clientes más fieles y el
   control son los que quedaban, la diferencia mide fidelidad, no efecto. Con datos observacionales
   hay que ajustar por las variables que explican la asignación y el resultado.
2. **Nada de fuga entre grupos.** Si las características de un cliente se calcularon usando el
   resultado de otros, la comparación se contamina ([[fuga-de-datos]]).

Y un detalle de vocabulario: el uplift **no** es la probabilidad de comprar. Un cliente con 80 % de
probabilidad y uplift 0 es un desperdicio; uno con 5 % de probabilidad y uplift 5 puntos es a quien
quieres. Ordenar por propensión y ordenar por uplift dan listas distintas, y la segunda es la que
genera ingresos. El corte para decidir a partir de qué uplift intervienes se elige por el coste de la
campaña, no por 0,5 ([[umbrales-y-coste]]).

:::figura
fichero: uplift-efecto-por-segmento
pie: La misma campaña sobre tres segmentos. En A va en contra (del 32 % al 6 %); en B y C sube. A la derecha, el efecto neto de cada uno frente al umbral donde dejar de compensar: el promedio de 13,3 puntos no describe a nadie, porque solo B lo supera con holgura.
fuente: figuras/uplift-y-valor-incremental-1.py
:::

## Ejemplo

Experimento con 8 clientes, cuatro tratados y cuatro de control, y la conversión observada. La
etiqueta `J` vale `Y` para los tratados y el resultado contrario para los controles:

| Cliente | T | Y | J |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 0 | 0 |
| 3 | 1 | 1 | 1 |
| 4 | 1 | 0 | 0 |
| 5 | 0 | 1 | 0 |
| 6 | 0 | 0 | 1 |
| 7 | 0 | 0 | 1 |
| 8 | 0 | 0 | 1 |

- Diferencia directa de tasas: `2/4 − 1/4 = 0,25`.
- `E[J | T = 1] = 2/4 = 0,50` y `E[J | T = 0] = 3/4 = 0,75`. La resta sale negativa (`−0,25`), con
  el signo cambiado respecto al efecto real (`+0,25`): la media de `J` no mide lo mismo en los dos
  grupos, porque en los controles está invertida, así que por sí sola no sirve para estimar el
  uplift. Por eso existe la escala `z`.
- En escala `z`: `E[z | T = 1] = 0` y `E[z | T = 0] = 0,25 − 0,75 = −0,50`, así que el uplift es
  `½ · (0 − (−0,50)) = 0,25` y cuadra con la diferencia directa. Con grupos desiguales hay que
  ponderar cada media por el peso de su grupo.

Ahora mira los dos subgrupos, que es donde está la gracia. Cada uno compara sus tratados con sus
controles: el grupo «fiel», clientes 1 y 2 frente a 5 y 6, y el grupo «frío», clientes 3 y 4 frente
a 7 y 8.

- Grupo fiel: en escala `z`, media `0,00` en tratados (uno de los dos convirtió) y `0,00` en
  controles (también uno de los dos); el uplift sale `0`. Dentro, el cliente 1 convierte con y sin
  campaña (uplift 0) y el cliente 2 no convierte en ninguno de los dos casos (uplift 0): a este
  grupo, la campaña no le hizo nada.
- Grupo frío: en escala `z`, `0,00` frente a `−1,00` (allí no convirtió nadie); el uplift sale
  `0,50`, y lo aporta entero el cliente 3 (convierte con campaña y sin ella no). El cliente 4 no
  convierte nunca.

El efecto agregado de 0,25 no describe a ninguno de los dos: uno no responde nada y el otro responde
`0,50`. El promedio cae justo en medio (la media de `0` y `0,50` es `0,25`) y por eso no sirve para
decidir a quién intervenir. Esa heterogeneidad invisible en el promedio —y el hecho de que aquí los
clientes «fieles» sean justo los que no responden— es lo que hace falta mirar antes de gastar.

## Código

```python verificable
import numpy as np

T = np.array([1, 1, 1, 1, 0, 0, 0, 0])     # tratado / control
Y = np.array([1, 0, 1, 0, 1, 0, 0, 0])     # convirtio / no convirtio
z = 2 * Y - 1                               # +1 si convirtio, -1 si no
J = T * Y + (1 - T) * (1 - Y)               # etiqueta con los controles invertidos

# Con los dos grupos del mismo tamano, el uplift es la mitad de la diferencia de sus medias de z
tau = 0.5 * (z[T == 1].mean() - z[T == 0].mean())

print(f"tasa tratados {Y[T == 1].mean():.2f}  tasa control {Y[T == 0].mean():.2f}")
print(f"diferencia directa  {Y[T == 1].mean() - Y[T == 0].mean():.2f}")   # -> 0.25
print(f"media de z          {np.round([z[T == 1].mean(), z[T == 0].mean()], 2)}")
print(f"uplift              {tau:.2f}")                                   # -> 0.25
print(f"J por subgrupo      {np.round([J[:2].mean(), J[2:].mean()], 2)}")  # -> [0.5  0.67]
print(f"uplift subgrupo frio {0.5 * (z[2:4].mean() - z[6:8].mean()):.2f}")  # -> 0.50
```

:::claves
- `T * Y` y `(1 - T) * (1 - Y)` son productos **elemento a elemento**, no `@`. Con `@` obtendrías un escalar (el producto escalar de los dos vectores) y la etiqueta `J` saldría mal sin dar ningún error.
- `(1 - T)` con `T` entero da enteros: `1` donde no hubo tratamiento y `0` donde sí. Eso hace que los controles se queden con `1 - Y`, es decir, con el resultado invertido.
- `Y[T == 1]` es **indexado booleano**: devuelve solo las posiciones donde la condición es cierta, en un array nuevo. La máscara `T == 1` tiene `True` y `False`, no unos y ceros; si escribieras `Y[T]` con `T` valiendo 1 y 0, NumPy lo interpretaría como **posiciones** (la 1 y la 0) y te devolvería dos elementos en vez de cuatro.
- `(T == 1).mean()` sobre un array de booleanos devuelve la **fracción** de `True` (0,5 aquí), porque `True` cuenta como 1. Ese número es lo que decide si la fórmula simple vale: con grupos del mismo tamaño sí; si un grupo es el doble que el otro, hay que ponderar cada media por el peso de su grupo.
- El `0,5` de delante traduce de la escala `z` (que va de `−1` a `+1`) a escala de probabilidad. Si lo quitas, con estos datos obtienes `0,50` en vez de `0,25` (la diferencia entre las dos medias de `z`, `0,00 − (−0,50)`, sin dividir): el doble del efecto real, y suficientes decisiones equivocadas para arruinar el presupuesto de la campaña.
- `J[:2]` y `J[2:]` son **vistas**, no copias: aquí solo las lees, pero escribir dentro cambiaría `J`. Y fíjate en que la media de `J` de los cuatro controles (`J[4:]`) es `0,75`, mayor que la de los tratados (`0,50`), aunque en esos controles solo convirtió una cuarta parte: `J` no mide conversión, mide conversión invertida, así que compararla entre grupos es lo único que la hace útil. Nunca la interpretes como una probabilidad.
:::

## Errores típicos

- **Optimizar la probabilidad de conversión y llamarlo uplift.** El modelo que mejor predice quién
  compra suele seleccionar a los que ya iban a comprar. Un ranking por propensión y otro por uplift
  pueden ser casi opuestos; mide siempre el efecto en un grupo de control que no recibe la campaña.
- **No tener grupo de control.** Sin control, cualquier subida de ventas se atribuye a la campaña,
  incluida la que venía de la estacionalidad, de una promoción de la competencia o del simple paso
  del tiempo ([[validacion-temporal]]).
- **Comparar grupos que no son comparables.** Si el cupón se envió primero a los clientes más
  activos, la diferencia mide quién era activo, no el efecto del cupón. Aleatoriza la asignación, y
  comprueba que las características de los dos grupos se parecen antes de mirar el resultado.
- **Medir el uplift con la métrica equivocada.** Un AUC alto sobre la etiqueta `Y` no dice nada del
  uplift, porque `Y` no es la variable de interés. La evaluación correcta es la curva de uplift
  ([[metricas-de-ranking]]): ordenar por uplift estimado y ver cuánto efecto real se acumula en el
  primer decil.
- **Ignorar a los que empeoran.** Si el 20 % de los clientes tiene uplift negativo, intervenirles
  destruye valor aunque el efecto medio sea positivo. El uplift existe para ponerlos al final de la
  lista, no para calcular una media.
- **Escribir la etiqueta `J` sin invertir los controles.** Es el fallo de una línea que arruina el
  ejercicio: `J = Y` convierte el problema en predecir conversión y el modelo aprende lo de siempre
  con un nombre nuevo. Comprueba que `J` vale `1 − Y` en las filas de control.

## Comprueba que lo sabes

:::quiz
p: Una campaña de correo se envía al 50 % de los clientes y la tasa de conversión es del 12 % en tratados y del 9 % en control. ¿Qué significa ese 3 %?
o: Que la campaña convierte al 3 % de los clientes y hay que ampliarla a todos
o: Que la campaña añade 3 puntos porcentuales de conversión frente a no hacer nada, siempre que los dos grupos sean comparables
o: Que el 3 % de los clientes que compraron lo hicieron por el correo
a: 2
e: La diferencia entre tratados y control estima el efecto de la campaña sobre el conjunto, no sobre cada comprador: no puedes saber cuáles de los 12 convertidos lo hicieron por el correo. Y «ampliarla a todos» exige que ese efecto se mantenga en escala, cosa que hay que comprobar, porque los clientes no tratados pueden responder distinto.
:::

:::quiz
p: ¿Por qué se necesita un experimento con grupo de control para estimar uplift?
o: Porque los datos históricos no registran la conversión de los clientes
o: Porque para cada cliente solo se observa un resultado: o el tratado o el no tratado, nunca los dos
o: Porque el modelo de uplift necesita el doble de filas para entrenar
a: 2
e: Es el problema fundamental de la inferencia causal: el resultado contrafactual no existe en los datos. El grupo de control te da, en agregado, la versión «sin tratamiento» de clientes comparables. Sin él, cualquier comparación mezcla el efecto con todo lo demás.
:::

:::quiz
p: En la transformación de clase, ¿qué hace la etiqueta J con los clientes del grupo de control?
o: Los deja como están, con su conversión original
o: Les pone su conversión invertida: 1 si no convirtieron y 0 si convirtieron
o: Los elimina del entrenamiento
a: 2
e: Invertir el resultado de los controles hace que la etiqueta J se comporte igual en los dos grupos, de modo que un clasificador normal pueda aprender a distinguir a quien responde. No se elimina a nadie, y dejarlos como están es el error que convierte todo el método en un modelo de conversión disfrazado.
:::

:::practica
enunciado: Un experimento tiene 1.000 clientes, 400 tratados y 600 de control. La tasa de conversión es del 14 % en tratados y del 8 % en control, así que el efecto directo son 6 puntos porcentuales. Calcula el uplift con la etiqueta simétrica z y explica por qué el resultado no coincide con 6 puntos si te olvidas del factor ½.
pista: z vale +1 cuando el cliente convierte y −1 cuando no. La media de z en un grupo es 2 por su tasa de conversión menos 1.
solucion: En los tratados, la media de z es 2 · 0,14 − 1 = −0,72. En los controles es 2 · 0,08 − 1 = −0,84. La diferencia es −0,72 − (−0,84) = +0,12 y, al multiplicar por ½, el uplift es 0,06: exactamente los 6 puntos porcentuales del cálculo directo. Si te saltas el ½, te quedas con 12 puntos porcentuales y crees que la campaña tiene el doble de efecto del que tiene. La razón de fondo es que la media de z está en una escala que va de −1 a +1 mientras que la conversión va de 0 a 1, así que pasar de una a otra siempre exige ese factor ½. El experimento está desequilibrado (400 tratados frente a 600 controles), pero eso no cambia el resultado mientras estimes las medias dentro de cada grupo; lo que sí importa es que los dos grupos sean comparables antes de mirar el resultado.
:::

:::aviso
El uplift se estima siempre sobre un experimento o sobre datos observacionales cuidadosamente
ajustados. Si tu única fuente es un histórico donde la campaña se mandó «a los buenos», ningún
modelo puede recuperar el efecto que habría tenido sobre los demás: no hay información sobre ese
contrafactual en los datos, por muy sofisticado que sea el algoritmo.
:::
