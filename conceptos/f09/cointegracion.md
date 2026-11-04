---
id: cointegracion
titulo: Cointegración
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [estacionariedad, test-adf-kpss, regresion-lineal, autocorrelacion-acf-pacf]
tags: [series-temporales, pares, arbitraje]
resumen: Dos series que vagan sin rumbo pero mantienen una combinación lineal estacionaria: la base estadística del trading de pares y del arbitraje estadístico.
fuentes: ["Engle y Granger (1987), 'Co-integration and Error Correction: Representation, Estimation, and Testing'", "Johansen (1991), 'Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models'"]
---

## En una frase

Dos series están cointegradas cuando cada una por separado es no estacionaria pero existe una
combinación lineal de ambas que sí es estacionaria: se separan, pero una fuerza económica las
empuja de vuelta a una relación de largo plazo.

## La idea

Todos los días alguien descubre que dos activos «están correlacionados» y monta una estrategia
con la diferencia. Casi siempre es un espejismo. Dos paseos aleatorios **independientes**
(generados por separado, sin ninguna relación económica) pueden mostrar en una muestra de 250
días una correlación de 0,9 y un R² de regresión altísimo, y aun así separarse para siempre a
partir de mañana. Es la regresión espuria: con series integradas, los estadísticos habituales
dejan de tener sus distribuciones y el R² se convierte en un número decorativo.

La cointegración es una condición mucho más fuerte y mucho más útil, y no habla de
correlación, habla de **equilibrio**. Dos series están cointegradas si existe una resta
ponderada de las dos que se comporta como una serie estable: oscila alrededor de una media
constante, cruza el cero, y cuando se aleja tiene tendencia a volver. La intuición económica
es que ambas están atadas por algo real: dos clases de acciones de la misma empresa, un ETF y
la cesta de valores que lo componen, dos barriles de crudo de calidades vecinas, una acción y
su sector. Mientras ese vínculo exista (el arbitraje, la convertibilidad, la ley), la
diferencia no puede crecer sin límite: si se abre, alguien la cierra y gana dinero haciéndolo.

Ese matiz es importante para no vender humo: la cointegración no es una propiedad estadística
abstracta, es un mecanismo. Si no puedes nombrar quién cierra la brecha y por qué le pagan por
hacerlo, probablemente estás mirando una regresión espuria que funcionó en el pasado.

El procedimiento clásico de Engle-Granger tiene dos pasos y es muy fácil de recordar. Primero
estimas por mínimos cuadrados ordinarios la relación de largo plazo entre las dos series
(regresas una sobre la otra). Segundo, te quedas con los residuos de esa regresión y les pasas
un contraste de raíz unitaria: si los residuos son estacionarios, la combinación lineal es
estable y las series están cointegradas. Hay dos detalles que casi todo el mundo pasa por
alto. El primero, que los valores críticos **no** son los del ADF normal: como los residuos se
han estimado, la distribución del estadístico cambia y hay que usar las tablas de
Engle-Granger y MacKinnon, cuyos umbrales son más exigentes (del orden de −3,3 al 5 % con un
solo regresor, frente a unos −2,9 del ADF estándar). El segundo, que la regresión es
asimétrica: regresar `y` sobre `x` y `x` sobre `y` da estimaciones distintas en muestra
pequeña, aunque ambas convergen.

Johansen ataca el problema de otra forma y resuelve varias limitaciones del anterior. En lugar
de estimar una ecuación y contrastar sus residuos, plantea un sistema vectorial de corrección
de error (VECM) y estima el **rango** de la matriz que multiplica a los niveles. Ese rango es
el número de relaciones de cointegración: 0 significa ninguna, 1 significa una relación
(lo típico en un par), y un rango igual al número de series significaría que todas son
estacionarias y no hay nada que cointegrar. Se contrasta con el test de la traza y el del
máximo autovalor. Johansen es el camino natural con tres o más series y cuando no tienes
claro cuál es la variable dependiente.

El premio gordo de la cointegración es el **teorema de representación de Granger**: si dos
series están cointegradas, entonces existe una representación de corrección de error, es
decir, los cambios de hoy dependen del desequilibrio de ayer. Traducido: la cointegración
**implica predictibilidad** en los retornos. Una de las dos series (o las dos) tiene que
reaccionar cuando la brecha se abre. Eso es lo que convierte una relación estadística en una
señal operables, y es también la razón de que haya que comprobar la velocidad de esa vuelta:
una vida media de 60 días en un diferencial del 1 % no paga comisiones ni coste de préstamo.
El uso práctico es el de [[pairs-trading|trading de pares]] y, en versión cartera,
[[arbitraje-estadistico|arbitraje estadístico]]: se calcula el z-score del diferencial y se
opera la vuelta a la media, con la cointegración como filtro previo de qué pares merecen
mirarse.

Y el aviso final, que es donde se pierde el dinero: la cointegración se estima en una muestra
y se opera en otra. Las relaciones se rompen por fusiones, cambios regulatorios, quiebras o
simplemente porque el mecanismo de arbitraje se hizo tan competitivo que dejó de pagar. Si
pruebas 500 pares y te quedas con el que más cointegra en la muestra, el p-valor que lees está
sesgado: es el mismo problema de [[data-snooping-y-multiple-testing|pruebas múltiples]] de
siempre. La cointegración es una hipótesis sobre el futuro, no un certificado del pasado.

## Definición formal

Sean `y_t` y `x_t` dos series **integradas de orden 1**, es decir, no estacionarias pero cuya
primera diferencia sí lo es (`y_t ~ I(1)`, `x_t ~ I(1)`); [[estacionariedad|la
estacionariedad]] y [[test-adf-kpss|los contrastes de raíz unitaria]] definen exactamente qué
significa eso.

:::formula
y_t = α + β · x_t + z_t          z_t = y_t − α − β · x_t
:::

- `α` — nivel constante de la relación de largo plazo.
- `β` — pendiente de la relación de largo plazo; es el coeficiente de cointegración.
- `z_t` — desviación respecto al equilibrio, o diferencial.
- Si `z_t` es `I(0)` (estacionario, con media y varianza constantes), entonces `y_t` y `x_t`
  están **cointegradas** con vector de cointegración `(1, −β)`.

**Contraste de Engle-Granger.** Se estiman `α̂` y `β̂` por mínimos cuadrados y se aplica un
contraste de raíz unitaria a los residuos `ẑ_t = y_t − α̂ − β̂ · x_t`. La hipótesis nula es «no
hay cointegración» (los residuos tienen raíz unitaria). Se rechaza cuando el estadístico es
más negativo que el valor crítico de Engle-Granger, que **no** es el del ADF estándar.

**Representación VECM.** Con un vector `y_t` de `n` series:

:::formula
Δy_t = μ + Π · y_{t−1} + Σ_{i=1}^{p−1} Γ_i · Δy_{t−i} + ε_t ,   con  Π = α · β'
:::

- `Δy_t` — primeras diferencias de las series (estacionarias).
- `Π` — matriz de `n × n` que multiplica a los niveles; su rango `r` es el número de
  relaciones de cointegración.
- `β` — matriz de vectores de cointegración (`n × r`).
- `α` — matriz de velocidades de ajuste (`n × r`): cuánto corrige cada serie el desequilibrio.
- `Γ_i` — matrices de la dinámica de corto plazo.
- `μ` — vector de constantes.
- Si `r = 0`, no hay cointegración; si `r = n`, todas las series son estacionarias.

**Vida media del diferencial.** Si `z_t` sigue un proceso autorregresivo de orden 1:

:::formula
z_t = φ · z_{t−1} + ε_t     ⇒     vida_media = ln(0,5) / ln(φ)
:::

- `φ` — coeficiente de persistencia; debe cumplir `0 < φ < 1` para que el diferencial vuelva.
- `vida_media` — número de periodos que tarda el diferencial en recorrer la mitad del camino
  de vuelta al equilibrio. Con `φ = 0,9`, son unos 6,6 periodos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `y_t`, `x_t` | Las dos series de niveles que se sospecha que están atadas | las de la serie (euros, índices) | El nivel no cambia el diagnóstico: lo que se contrasta es el residuo, no el tamaño de las series. Comparar magnitudes muy distintas solo obliga a estimar `β` con más cuidado |
| `α` | Ordenada de la relación de largo plazo: dónde está el diferencial cuando `x_t = 0` | las de `y_t` | Desplaza el diferencial en paralelo y no afecta a que sea estacionario. En el contraste solo molesta si se omite: sin constante, una media distinta de cero se confunde con raíz unitaria |
| `β` | Pendiente de la relación: el coeficiente de cointegración | cociente entre las unidades de `y` y de `x` | Es lo que hay que estimar bien. Si `β` se estima con error, el residuo arrastra parte de la tendencia de las series y el contraste rechaza menos: por eso la regresión es asimétrica en muestra pequeña y `β` debe ser estable en subperiodos |
| `z_t` | El diferencial o desviación respecto al equilibrio | las de `y_t` | Es lo que se vigila. Lo que decide la cointegración no es su tamaño en un momento dado, sino que su varianza y su media no dependan de `t` |
| `Π` | Matriz `n × n` que multiplica a los niveles en el VECM | adimensional | Su rango `r` es el número de relaciones de cointegración. Con `r = 0` no hay ninguna; con `r = n` todas las series son estacionarias y no hay nada que cointegrar |
| `Γ_i` | Matrices de la dinámica de corto plazo (retardos de las diferencias) | adimensional | Añadir retardos absorbe autocorrelación de corto plazo y deja el contraste más limpio, pero cada retardo consume observaciones y con ventanas cortas el test pierde potencia |
| `φ` | Persistencia del diferencial: qué fracción de la desviación sobrevive de un periodo al siguiente | adimensional, entre 0 y 1 | Cuanto más cerca de 1, más lenta es la vuelta: `φ = 0,9` da 6,6 periodos de vida media y `φ = 0,99` da 69. Por encima de 0,98 en datos diarios la operación deja de cubrir costes y el intervalo de confianza de `φ` suele incluir el 1 |
| `n` | Número de observaciones de la ventana de estimación | observaciones | Con 250 a 1.000 observaciones el contraste tiene potencia; por debajo de 100 el resultado es esencialmente ruido y el `β` estimado cambia mucho de una submuestra a otra |
:::

:::figura
fichero: cointegracion-diferencial-estacionario
pie: Arriba están los dos pares separados en el eje solo para poder dibujarlos: los dos «van juntos» y la regresión ajusta en los dos. La diferencia aparece abajo, en la resta. El residuo del par independiente se instala lejos de cero y no vuelve, así que ninguna resta lo hace estacionario; el del par atado oscila alrededor de cero y vuelve. Esa es la única pregunta que responde Engle-Granger: no si las series se parecen, sino si su diferencia tiene un nivel al que regresar.
fuente: figuras/cointegracion-1.py
:::

## Ejemplo

Seis observaciones de dos series, para ver el primer paso a mano:

| t | x | y |
| --- | --- | --- |
| 1 | 10,0 | 20,4 |
| 2 | 11,0 | 22,1 |
| 3 | 10,5 | 21,4 |
| 4 | 11,5 | 23,6 |
| 5 | 12,0 | 24,2 |
| 6 | 11,0 | 22,0 |

Medias: `x̄ = 11,0` e `ȳ = 22,283`. Las desviaciones del producto y los cuadrados dan
`Σ(x − x̄)(y − ȳ) = 4,90` y `Σ(x − x̄)² = 2,50`, así que:

- `β̂ = 4,90 / 2,50 = 1,96`.
- `α̂ = 22,283 − 1,96 · 11,0 = 0,723`.

Los residuos `ẑ_t = y_t − 0,723 − 1,96 · x_t` valen, en orden: **+0,077, −0,183, +0,097,
+0,337, −0,043 y −0,283**. Suman cero (propiedad de los residuos de mínimos cuadrados),
pequeños, y cambian de signo cuatro veces en seis observaciones: eso es lo que se espera de un
diferencial estacionario alrededor de cero.

Compáralo con lo que saldría si `y` fuese un paseo aleatorio independiente: los residuos
tendrían el mismo aspecto durante unas cuantas observaciones —una regresión siempre ajusta
algo— y luego se irían acumulando hacia un lado sin volver. Un contraste de raíz unitaria
sobre seis puntos no decide nada, y por eso en la práctica se usan ventanas de 250 a 1.000
observaciones; pero el patrón que buscas ya se ve aquí: oscilación rápida alrededor de cero,
sin tendencia.

## Código

```python verificable
import numpy as np
from statsmodels.tsa.stattools import coint

rng = np.random.default_rng(7)
n = 250
x = np.cumsum(rng.normal(0, 1, n)) + 100          # paseo aleatorio: I(1)
z = np.zeros(n)
for t in range(1, n):                             # desvio estacionario AR(1)
    z[t] = 0.85 * z[t - 1] + rng.normal(0, 0.5)
y = 2.0 * x + 5 + z                               # I(1) pero atado a x

beta = np.polyfit(x, y, 1)[0]
residuo = y - beta * x
rho = np.polyfit(residuo[:-1], np.diff(residuo), 1)[0]   # raiz del residuo, estilo Dickey-Fuller
t_eg, p_eg, _ = coint(y, x)

print(f"beta estimada por MCO   {beta:.3f}")        # -> 2.033
print(f"raiz del residuo (DF)   {rho:.3f}")         # -> -0.239
print(f"Engle-Granger  t {t_eg:.3f}  p {p_eg:.4f}")  # -> Engle-Granger  t -5.814  p 0.0000

x2 = np.cumsum(rng.normal(0, 1, n)) + 100
y2 = np.cumsum(rng.normal(0, 1, n)) + 200         # paseo independiente: sin relacion
t2, p2, _ = coint(y2, x2)
print(f"par sin relacion  t {t2:.3f}  p {p2:.4f}")   # -> par sin relacion  t -1.752  p 0.6525
print(f"beta espuria        {np.polyfit(x2, y2, 1)[0]:.3f}")   # -> 0.899
```

:::claves
- `np.polyfit(x, y, 1)` devuelve los coeficientes **de mayor a menor potencia**, no en el orden en que se escriben en una ecuación: el primero es la pendiente y el segundo la ordenada. Con `3` devolvería tres números y con `deg=0` uno solo. El código se queda con `[0]` porque solo usa la pendiente, y luego calcula a mano `residuo = y - beta * x`: eso deja fuera la constante de la relación, así que ese «residuo» está desplazado y **no es el que contrasta `coint`**, que sí estima la ordenada. Es un atajo para mirar la raíz del residuo, no el contraste bueno.
- `coint(y, x)` **no** es un contraste de raíz unitaria corriente sobre los residuos a mano: aplica internamente la regresión de Engle-Granger y usa los valores críticos de MacKinnon ajustados al número de variables. Devuelve tres cosas y el código descarta la tercera con `_`: el estadístico `t`, el p-valor y el valor crítico. Ojo con el orden de los argumentos: `coint(x, y)` da un estadístico distinto del de `coint(y, x)`, porque la regresión de partida es asimétrica.
- Ese `t` viene con su signo, y la hipótesis nula es «no hay cointegración», así que **cuanto más negativo, mejor**. El p-valor que devuelve no es el de una `t` de Student con `n − 2` grados de libertad: sale de la distribución propia de Engle-Granger, y por eso `coint` da p = 0,0000 para un `t` de −5,8 cuando a ojo uno esperaría compararlo con −1,96.
- En el segundo bloque, `np.polyfit(z[:-1], z[1:], 1)` estima un AR(1) sin constante: el `0` de `z[:-1]` se empareja con `z[1]`, y el último elemento de `z` no participa. Por eso la serie se acorta un elemento y `z` y `z[1:]` no tienen la misma longitud: si los pasas a una función que exige vectores iguales, tienes que recortarlos tú.
- La vida media se calcula con `-np.log(2) / np.log(phi)` y **no** con `np.log(0.5)/np.log(phi)` mal escrito: `np.log` es el logaritmo neperiano, y `ln(0,5)` es negativo, así que el resultado sale positivo porque el numerador y el denominador lo son. Si `phi` sale mayor o igual que 1, el cociente se vuelve negativo o se va a infinito: eso no es una vida media, es la señal de que la serie no revierte.
- Con 250 puntos, `coint` elige los retardos por su cuenta y el resultado cambia si le pasas `maxlag`; si necesitas reproducir exactamente las cifras de la página, fija ese argumento en lugar de dejarlo automático.
:::

```python verificable
import numpy as np

# Vida media del diferencial: cuanto tarda en recorrer la mitad del camino de vuelta
rng = np.random.default_rng(3)
n = 400
z = np.zeros(n)
for t in range(1, n):
    z[t] = 0.9 * z[t - 1] + rng.normal(0, 1)

phi = np.polyfit(z[:-1], z[1:], 1)[0]
print(f"phi estimado          {phi:.4f}")                    # -> 0.8917
print(f"vida media (periodos) {-np.log(2) / np.log(phi):.2f}")  # -> 6.05
```

El segundo ejemplo enseña el detalle importante: el `φ` estimado (0,892) no es el verdadero
(0,9) y la vida media sale 6,05 periodos en lugar de los 6,58 teóricos. Con 400 observaciones
la estimación es razonable; con 60, no lo sería.

## Errores típicos

- **Confundir correlación alta con cointegración.** Dos paseos aleatorios independientes
  pueden dar una correlación de 0,9 y un R² de 0,8 en la muestra sin ninguna relación real.
  Cointegración es que una combinación lineal sea estacionaria, no que las series se muevan
  juntas durante un tramo, y tampoco es lo mismo que la reversión a la media de un solo activo:
  lo que vuelve es el **diferencial**, y ninguna de las dos series tiene por qué hacerlo por
  separado.
- **Usar los valores críticos del ADF estándar para los residuos de Engle-Granger.** Los
  residuos se han estimado, y eso desplaza la distribución del estadístico hacia valores más
  negativos: hay que usar las tablas de Engle-Granger y MacKinnon. Si usas el umbral normal,
  rechazas «hay cointegración» demasiadas veces.
- **Leer el R², el t de la pendiente o el p-valor de la regresión de niveles.** Con series
  integradas esa regresión es espuria y sus estadísticos no tienen la distribución habitual.
  La única pregunta válida es si el residuo es estacionario, y se responde con su propio
  contraste.
- **Operar un par cointegrado sin mirar la vida media ni los costes.** Un diferencial que
  tarda 60 días en volver, con una brecha del 1 %, no cubre comisiones, diferencial y coste de
  préstamo del corto. La cointegración te dice que la relación existe; la vida media decide si
  es operables.
- **Buscar pares probando cientos y quedarte con el mejor.** Es
  [[data-snooping-y-multiple-testing|data snooping]] puro: el p-valor del elegido está sesgado
  y la cointegración desaparece fuera de la muestra. Reserva datos que no hayas mirado y
  exige estabilidad de `β` en subperiodos.
- **Ignorar los cambios estructurales.** Fusiones, cambios de índice, regulación o quiebras
  rompen la relación de largo plazo de un día para otro. Reestima la relación de forma
  periódica y define de antemano cuándo abandonas un par, en lugar de decidirlo con la pérdida
  ya en la cuenta.

:::practica
enunciado: Cinco observaciones de un par: x = 20, 22, 21, 24, 23 e y = 41, 45, 42, 49, 46. Estima la relación de largo plazo por mínimos cuadrados, calcula los residuos y di si el diferencial parece estacionario.
pista: Con las medias y las desviaciones se obtienen la pendiente y la ordenada; cada residuo es y menos la recta ajustada.
solucion: Medias: x̄ = 22 e ȳ = 44,6. Σ(x − x̄)(y − ȳ) = 20 y Σ(x − x̄)² = 10, luego β̂ = 2,0 y α̂ = 44,6 − 2,0 · 22 = 0,6. Residuos, en orden: +0,4; +0,4; −0,6; +0,4; −0,6. Suman cero, son pequeños y cambian de signo: el patrón de un diferencial estacionario. Con cinco puntos no se contrasta la raíz unitaria: hacen falta ventanas de 250 a 1.000 observaciones y los valores críticos de Engle-Granger, no los del ADF.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre que dos series estén correlacionadas y que estén cointegradas?
o: La correlación mide si se mueven juntas en la muestra; la cointegración exige que una combinación lineal sea estacionaria, lo que implica una relación estable en el tiempo
o: La cointegración es una correlación elevada al cuadrado
o: Son lo mismo, pero la cointegración se calcula con series diferenciadas
a: 1
e: La correlación es una medida de asociación lineal en la muestra y con series integradas puede ser altísima por puro azar. La cointegración exige que `y − βx` sea estacionaria, es decir, que la relación no se rompa, y por el teorema de representación de Granger implica que alguna serie corrige los desequilibrios.
:::

:::quiz
p: En Engle-Granger, ¿por qué no se pueden usar los valores críticos habituales del ADF sobre los residuos?
o: Porque los residuos tienen menos observaciones que las series originales
o: Porque los residuos se han estimado con los mismos datos, y eso sesga el estadístico hacia valores más negativos
o: Porque los residuos siempre son estacionarios por construcción
a: 2
e: Al estimar `α` y `β` se elige precisamente la combinación que hace los residuos lo más estacionarios posible, así que el contraste rechaza con demasiada facilidad si se compara con la distribución estándar. Las tablas de Engle-Granger y MacKinnon corrigen ese sesgo; las observaciones son casi las mismas que las de la serie original.
:::

:::quiz
p: Un diferencial cointegrado tiene `φ = 0,95` con datos diarios. ¿Qué implica para una estrategia de pares?
o: Que la vida media es de unos 13,5 días, así que la vuelta es lenta y hay que comprobar que cubre costes
o: Que la vida media es de 0,95 días y el par es ideal para intradía
o: Que el diferencial nunca vuelve, porque `φ` está cerca de 1
a: 1
e: La vida media es `ln(0,5) / ln(0,95) = 13,5` días. Con esa lentitud, la posición puede estar abierta semanas y los costes de comisión, diferencial y préstamo pesan mucho. Un `φ` cercano a 1 no anula la reversión, solo la hace lenta; solo `φ = 1` exacto significa que no hay vuelta.
:::
