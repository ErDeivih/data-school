---
id: regimenes-de-mercado
titulo: Regímenes de mercado
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [volatilidad-realizada, hmm-regimenes, validacion-temporal]
tags: [regimenes, volatilidad, markov, exposicion]
resumen: Detectar el clima antes de elegir modelo o exposición, sabiendo que el estado no se observa, que la detección llega tarde y que el suavizado mira al futuro.
fuentes: ["Hamilton (1989), 'A New Approach to the Economic Analysis of Nonstationary Time Series'", "Ang y Timmermann (2012), 'Regime Changes and Financial Markets'"]
---

## En una frase

Un régimen de mercado es un estado persistente en el que la volatilidad, las correlaciones y a
veces la dirección se comportan de forma distinta, y detectarlo sirve para cambiar de modelo o
de exposición, no para adivinar la dirección.

## La idea

El clima y el tiempo no son lo mismo. En verano puede llover un día, y en invierno puede hacer
una tarde espléndida. Si quieres decidir qué ropa llevar de viaje, miras la estación, no la
predicción de mañana. Los regímenes de mercado son la estación: un estado que dura semanas o
meses, en el que las reglas del juego cambian respecto al anterior.

Lo que cambia entre regímenes es concreto y medible:

- **La volatilidad.** En los episodios de tensión, la volatilidad diaria puede multiplicarse
  por dos o por tres, y la distribución de los retornos gana colas.
- **Las correlaciones.** En calma, las acciones se mueven por sus propias razones; en tensión,
  casi todo cae a la vez y la diversificación que tenías desaparece justo cuando la necesitas.
- **La persistencia.** Los regímenes duran: no se cambia de calma a tensión y vuelta en dos
  días. Esa persistencia es lo que hace posible detectarlos con retraso y seguir ganando algo.
- **A veces la dirección.** No siempre. Un régimen puede ser de volatilidad alta con dirección
  plana, o de tendencia suave con volatilidad baja. Confundir régimen con dirección es el
  primer error de la lista.

Hay dos familias de detección y conviene conocer las dos:

1. **Reglas sobre variables observables.** Un umbral sobre la volatilidad realizada, sobre la
   caída desde el máximo, sobre la dispersión de retornos entre sectores o sobre la correlación
   media. Son transparentes, fáciles de auditar y no prometen más de lo que dan.
2. **Modelos de estado latente.** Una [[hmm-regimenes|cadena de Markov oculta]] o un modelo de
   cambio de régimen estiman la probabilidad de estar en cada estado. Son más elegantes y
   también más peligrosos: introducen parámetros, necesitan datos para estimarse y su
   resultado depende del periodo con el que los ajustes.

El uso sensato es siempre el mismo: **cambiar la exposición o el modelo, no la dirección**. Si
detectas tensión, reduces tamaño, subes el umbral de entrada o cambias a un modelo entrenado
en volatilidad alta. Lo que no funciona es usar el régimen como señal de compra o venta: los
regímenes se detectan con retraso y con ruido, y cuando el estado es evidente ya está en el
precio.

## Definición formal

Un modelo de regímenes es una cadena de Markov con `K` estados. La matriz de transición `P`
recoge la probabilidad de pasar de un estado a otro:

:::formula
P_jk = Pr( S_t+1 = k  dado  S_t = j )  ,  con Σ_k P_jk = 1 para cada j
:::

- `S_t` — el estado (no observado) en el instante `t`. Por ejemplo 0 = calma, 1 = tensión.
- `P_jk` — probabilidad de que, estando en `j`, el siguiente periodo sea `k`.
- La diagonal mide la persistencia: `P_jj` alto significa que el estado dura.
- **Duración esperada** de un estado: `1 / (1 − P_jj)` periodos.

La **distribución estacionaria** `π` es la fracción del tiempo que el sistema pasa en cada
estado a largo plazo, y se obtiene resolviendo `π = π · P` con `Σ π_j = 1`.

Cada estado tiene su propia distribución de retornos:

:::formula
r_t en el estado j  ∼  Normal(μ_j , σ_j²)
:::

- `μ_j` — retorno medio del estado `j`.
- `σ_j` — volatilidad del estado `j`.
- En tensión lo habitual es `σ` mayor y `μ` menor, pero los dos parámetros se estiman, no se
  imponen.

Y la pieza que decide si el modelo es utilizable o es una máquina de mirar al futuro es la
diferencia entre probabilidad filtrada y suavizada:

:::formula
filtrada:   ξ_t(j) = Pr( S_t = j  dado  r_1 … r_t )
suavizada:  Pr( S_t = j  dado  r_1 … r_T )   ← usa también el futuro
:::

- `ξ_t(j)` **filtrada** usa solo la información hasta `t`. Es la única que puedes usar para
  decidir en `t`.
- La **suavizada** usa toda la muestra, incluido el futuro. Sirve para describir el pasado en
  un artículo y para nada más: si asignas la exposición con ella, el backtest es una ficción.
- Con la probabilidad filtrada, la regla de exposición es una media ponderada de las
  exposiciones por estado: `w_t = Σ_j ξ_t(j) · g_j`, con `g_j` la exposición deseada en el
  estado `j`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `K` | Número de estados que le pides al modelo | estados | Más estados describen mejor el pasado y se estiman con menos datos cada uno: con 3 o 4, las transiciones se vuelven inestables y acabas con dos modelos mal ajustados |
| `P_jj` | Probabilidad de seguir en el mismo estado (`P_calma,calma` = 0,95) | probabilidad por periodo | Alarga los episodios y por tanto la detección llega con menos falsos positivos; por encima de 0,99 el estado dura tanto que el cambio casi no se ve |
| `1 − P_jj` | Probabilidad de salir del estado; su inversa es la duración esperada | probabilidad por periodo | Con 0,05 la calma dura 20 periodos; con 0,15 la tensión dura 6,7, y una ventana de 20 días medirá un pasado que ya terminó |
| `π_j` | Fracción del tiempo que el sistema pasa en el estado `j` a largo plazo | tanto por uno | Determina cuántos episodios verás y con qué clase mayoritaria: con π_tensión = 0,333, decir siempre «calma» acierta el 70 % de los días |
| `μ_j`, `σ_j` | Retorno medio y volatilidad de cada estado | % por periodo | La σ es lo único que un detector de volatilidad ve de verdad; la μ cambia entre estados, pero un filtro de volatilidad no la detecta |
| `ξ_t(j)` filtrada | Probabilidad del estado `j` con los datos hasta `t` | probabilidad | Es la única utilizable para decidir. La suavizada usa el futuro: sirve para escribir un artículo, no para operar |
:::

:::figura
fichero: regimenes-de-mercado-detector-y-retardo
pie: Arriba a la izquierda, la volatilidad móvil de 20 días que tú ves y las bandas rojas del estado real que no ves: el filtro cruza el umbral unos días después de cada inicio. Arriba a la derecha, las dos métricas del detector: acierta el 68,1 % de los días, pero decir siempre «calma» acierta el 70,5 %, así que el número que importa es la precisión en tensión, 0,473. Abajo, las dos lecturas que deciden el uso: con 108 episodios el aviso llega 2 días tarde, y el retorno medio de los cuatro primeros días de tensión es casi igual al del resto del episodio, así que el régimen avisa de volatilidad, no de caída.
fuente: figuras/regimenes-de-mercado-1.py
:::

## Ejemplo

Dos estados, calma y tensión, con esta matriz de transición:

```
P = [ 0,95  0,05 ]      fila 0: estando en calma
    [ 0,10  0,90 ]      fila 1: estando en tensión
```

- Duración esperada en calma: 1 / (1 − 0,95) = **20 periodos**. En tensión:
  1 / (1 − 0,90) = **10 periodos**.
- Distribución estacionaria: hay que resolver `π = πP`. De la segunda ecuación,
  `π_tensión = 0,05 · π_calma + 0,90 · π_tensión`, es decir `0,10 · π_tensión = 0,05 · π_calma`,
  o sea `π_tensión = 0,5 · π_calma`. Con la suma igual a 1: `π_calma = 0,667` y
  `π_tensión = 0,333`. Es decir, se pasa un tercio del tiempo en tensión, aunque cada episodio
  dure solo diez periodos.
- Simulando 20 000 periodos de la cadena: duración media observada 20,0 en calma y 9,9 en
  tensión, que es exactamente lo que predice la fórmula.

Esa aritmética es el presupuesto de tu detector. Si el régimen dura diez periodos y tu ventana
de detección es de veinte, la mitad de tus alertas llegarán cuando el episodio ya se ha
terminado. Eso es justo lo que se mide a continuación con 3000 días simulados, volatilidad
0,8 % en calma y 2 % en tensión, y un detector de volatilidad móvil a veinte días con umbral
0,012:

```
dias en tension 30%
acierto del filtro      0.681
acierto de decir calma  0.705
precision en tension    0.473
episodios 108  retardo mediano 2 dias
retorno medio primeros 4 dias -0.00043
retorno medio del resto       -0.00054
```

Tres lecturas, y las tres importan:

- **El filtro acierta menos que no hacer nada.** Un 68,1 % de acierto frente al 70,5 % de decir
  siempre «calma». Con clases desbalanceadas, el acierto es una métrica que engaña; hay que
  mirar la precisión en la clase minoritaria, que aquí es 0,473.
- **El retardo es corto (2 días) pero el filtro sigue disparando después.** Con episodios de
  diez días y una ventana de veinte, la volatilidad medida sigue alta cuando el régimen ya
  cambió: esas alertas son el 53 % de falsos positivos.
- **El golpe no está en los primeros días.** El retorno medio de los cuatro primeros días de
  tensión (−0,00043) es prácticamente igual al del resto del episodio (−0,00054). Este detector
  avisa de un cambio de **volatilidad**, no de una caída: el daño está repartido por todo el
  episodio y lo que evitas es exposición, no un desplome concreto.

## Código

```python verificable
import numpy as np

# Filas: estado en t. Columnas: estado en t+1. Estado 0 = calma, 1 = tension.
P = np.array([[0.95, 0.05],
              [0.10, 0.90]])

vals, vecs = np.linalg.eig(P.T)
est = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
est = est / est.sum()
print("probabilidad estacionaria  calma %.3f  tension %.3f" % (est[0], est[1]))
print("duracion esperada  calma %.1f  tension %.1f periodos" % (1 / 0.05, 1 / 0.10))

rng = np.random.default_rng(4)
n, estado, actual = 20000, 0, 0
duraciones = {0: [], 1: []}
for t in range(n):
    actual += 1
    if rng.random() < P[estado, 1 - estado]:
        duraciones[estado].append(actual)
        actual = 0
        estado = 1 - estado
print("duracion simulada  calma %.1f  tension %.1f periodos"
      % (np.mean(duraciones[0]), np.mean(duraciones[1])))
# -> probabilidad estacionaria  calma 0.667  tension 0.333
# -> duracion esperada  calma 20.0  tension 10.0 periodos
# -> duracion simulada  calma 20.0  tension 9.9 periodos
```

:::claves
- `np.linalg.eig(P.T)` devuelve autovalores y autovectores de la **traspuesta**: la estacionaria sale del autovector por la izquierda de `P`, y trasponer es la forma de pedírselo a `eig`. El autovector se elige con `argmin(np.abs(vals - 1))` porque en una matriz de transición el autovalor 1 siempre existe.
- Un autovector está definido salvo escala: por eso hay que dividir entre `est.sum()` para que las probabilidades sumen 1. Sin esa normalización el vector sale con números que no son probabilidades y el `print` no cuadra con la aritmética de la página.
- El bucle de la cadena usa una sola llamada al generador por periodo, `rng.random() < P[estado, 1 - estado]`. Poner dos `if` seguidos con dos llamadas gasta dos números aleatorios por paso, la secuencia cambia y las duraciones simuladas dejan de coincidir con 20 y 10.
- `duraciones` es un diccionario de listas y `actual` se reinicia a 0 en cada cambio: el último tramo de la simulación se pierde, y por eso la duración simulada de tensión sale 9,9 en vez de 10,0.
- `r[t - 19:t + 1].std(ddof=1)` es una desviación típica **móvil que termina en t**: la ventana incluye el día de hoy y ninguno posterior. Los 19 primeros días se quedan a cero porque no hay ventana completa, y un filtro centrado daría números mejores sin poder operarse.
- `alerta.sum()` en el denominador de la precisión cuenta los días en que el filtro dice «tensión», no el total de días. Cambiarlo por `len(alerta)` convierte la precisión en un porcentaje diminuto y sin sentido.
:::

La distribución estacionaria se saca del autovector de `P` traspuesta asociado al autovalor 1.
Es la forma compacta de resolver el sistema que en el ejemplo se hace a mano; para dos estados,
hacerlo a mano es más rápido y más claro.

```python verificable
import numpy as np

rng = np.random.default_rng(5)
n = 3000
P = np.array([[0.95, 0.05], [0.10, 0.90]])       # la misma cadena de la pagina
estado = np.zeros(n, dtype=int)
for t in range(1, n):
    if rng.random() < P[estado[t - 1], 1 - estado[t - 1]]:
        estado[t] = 1 - estado[t - 1]
    else:
        estado[t] = estado[t - 1]

media = np.where(estado == 0, 0.0005, -0.0008)
vol = np.where(estado == 0, 0.008, 0.020)
r = rng.normal(media, vol)

# Volatilidad movil de 20 dias: en t solo se usan datos hasta t (nada de futuro)
v = np.zeros(n)
for t in range(19, n):
    v[t] = r[t - 19:t + 1].std(ddof=1)
alerta = v > 0.012

print("dias en tension %.0f%%" % (100 * (estado == 1).mean()))
print("acierto del filtro      %.3f" % (alerta == (estado == 1)).mean())
print("acierto de decir calma  %.3f" % (estado == 0).mean())
print("precision en tension    %.3f" % ((alerta & (estado == 1)).sum() / alerta.sum()))

retardos = []
for t in range(1, n):
    if estado[t] == 1 and estado[t - 1] == 0 and alerta[t:].any():
        retardos.append(int(np.argmax(alerta[t:])))
print("episodios %d  retardo mediano %.0f dias" % (len(retardos), np.median(retardos)))

# Donde esta el golpe: retorno medio de los primeros cuatro dias frente al resto
primeros, resto = [], []
for t in range(1, n):
    if estado[t] == 1 and estado[t - 1] == 0:
        primeros.append(r[t:t + 4].mean())
        fin = t
        while fin < n and estado[fin] == 1:
            fin += 1
        if fin - t > 4:
            resto.append(r[t + 4:fin].mean())
print("retorno medio primeros 4 dias %+.5f" % np.mean(primeros))
print("retorno medio del resto       %+.5f" % np.mean(resto))
# -> dias en tension 30%
# -> acierto del filtro      0.681
# -> acierto de decir calma  0.705
# -> precision en tension    0.473
# -> episodios 108  retardo mediano 2 dias
# -> retorno medio primeros 4 dias -0.00043
# -> retorno medio del resto       -0.00054
```

Fíjate en que la cadena se simula con `estado[t]` dependiendo solo de `estado[t-1]`, y en que
la volatilidad móvil del día `t` usa la ventana que **termina** en `t`. Ese detalle es el que
separa un backtest honesto de uno que se mira el futuro: un filtro centrado en `t` daría
números mejores en el papel y no se podría operar.

## Errores típicos

- **Usar información de toda la muestra: probabilidades suavizadas o un umbral calibrado con
  el histórico completo.** La probabilidad suavizada sabe cuándo empezó y cuándo acabó la
  crisis, así que el backtest sale bonito y falso. Y «el percentil 70 de la volatilidad de los
  últimos diez años» es una decisión que en 2015 no podías tomar: calibra el umbral con datos
  anteriores y déjalo quieto.
- **Meter más estados de los que los datos sostienen.** Con tres o cuatro estados los
  parámetros se estiman con cada vez menos observaciones por estado y las transiciones se
  vuelven inestables. Empieza por dos y justifica el tercero con datos.
- **Usar una ventana más larga que el régimen, o dar por hecho que durará lo mismo que en la
  muestra.** Si el episodio dura diez días y mides con veinte, la mitad de tus alertas serán
  sobre un pasado que ya terminó. Y las duraciones estimadas son medias históricas: un episodio
  puede durar tres veces más, así que dimensiona la exposición para el caso largo, no para el
  medio.
- **Juzgar el detector por su acierto.** Con clases desbalanceadas, decir siempre «calma»
  acierta la mayoría de los días. Mira la precisión y la exhaustividad de la clase minoritaria,
  y el coste de cada tipo de error.
- **Cambiar de modelo cada semana.** Si el detector cambia de estado a menudo, tendrás dos
  modelos mal estimados y un montón de giro. La persistencia es lo que hace que el cambio de
  modelo compense.
- **Confundir régimen con dirección.** Un filtro de volatilidad no predice si el mercado sube o
  baja. Úsalo para el tamaño y para la selección de modelo, no para ponerte corto.

:::trampa
El error más difícil de ver desde dentro es entrenar el modelo de regímenes en un periodo que
incluye la crisis que luego «predice». Si el modelo se ajustó con 2008 dentro, sus parámetros
ya saben cómo es un estado de tensión y suavizan el reconocimiento. Estima con datos
anteriores al episodio que quieres evaluar, o no estarás midiendo nada.
:::

:::practica
enunciado: Con dos estados, calma y tensión, la matriz de transición tiene P(calma→calma) = 0,97 y P(tensión→tensión) = 0,85. Calcula la duración esperada de cada estado, la fracción del tiempo en tensión y compara esa duración con una ventana de detección de 20 días.
pista: La duración esperada es 1/(1 − P_jj), y la distribución estacionaria sale de π = πP con las probabilidades sumando 1.
solucion: Duración en calma = 1/0,03 = 33,3 periodos y en tensión = 1/0,15 = 6,7. Para la estacionaria, π_tensión = 0,03 · π_calma + 0,85 · π_tensión, luego 0,15 · π_tensión = 0,03 · π_calma y π_tensión = 0,2 · π_calma. Con π_calma + π_tensión = 1 queda 0,833 y 0,167, un sexto del tiempo. Como los episodios duran 6,7 días y la ventana mide 20, casi todas las alertas llegan cuando el episodio ya terminó.
:::

## Comprueba que lo sabes

:::quiz
p: Con una matriz de transición en la que P(calma→calma) = 0,95 y P(tensión→tensión) = 0,90, ¿qué fracción del tiempo se pasa en tensión?
o: Un 10 %, porque la probabilidad de salir de tensión es 0,10
o: Un 33,3 %, porque los episodios son más cortos (10 periodos) pero la mitad de frecuentes que los de calma (20 periodos)
o: Un 50 %, porque la matriz es simétrica
a: 2
e: La distribución estacionaria sale de resolver pi = pi·P: pi_tension = 0,5·pi_calma con la suma igual a 1, lo que da 0,333 para tensión y 0,667 para calma. El 0,10 es la probabilidad de salir de tensión cada periodo, no la fracción del tiempo. Y la matriz no es simétrica: 0,05 frente a 0,10 en las transiciones.
:::

:::quiz
p: Un filtro de volatilidad acierta el 68 % de los días; decir siempre «calma» acierta el 70,5 %. ¿Qué se concluye?
o: Que el filtro es peor que no hacer nada y hay que descartarlo sin más
o: Que el acierto es una métrica inadecuada con clases desbalanceadas y hay que mirar la precisión y la exhaustividad de la clase de tensión, además de para qué se va a usar
o: Que el filtro funciona, porque un 68 % está cerca del 70,5 %
a: 2
e: El acierto queda dominado por la clase mayoritaria: con un 70 % de días en calma, acertar casi todo en calma da un porcentaje alto sin detectar nada. Eso no significa que el filtro sea inútil: sirve para reducir exposición, y su valor se juzga por la precisión en tensión (0,473 en el ejemplo) y por el uso que le des, no por el porcentaje global.
:::

:::nota
La volatilidad realizada y las correlaciones entre sectores son los indicadores de régimen más
sencillos de construir y de auditar. Un modelo de Markov oculto con dos estados suele ordenar
los mismos periodos que un umbral bien calibrado sobre volatilidad; la diferencia es que el
modelo da probabilidades y el umbral da un sí o un no. Empieza por el umbral.
:::
