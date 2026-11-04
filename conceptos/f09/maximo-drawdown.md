---
id: maximo-drawdown
titulo: Caída máxima (max drawdown)
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [retornos-logaritmicos, metricas-de-riesgo, ratio-de-sharpe]
tags: [riesgo, drawdown, backtest, metricas]
resumen: La mayor caída desde un pico de tu curva de capital hasta el mínimo anterior a recuperarlo: cuánto duele, cuánto dura y por qué decide si aguantas.
fuentes: ["Magdon-Ismail y Atiya (2004), 'Maximum Drawdown'", "Bacon (2008), 'Practical Portfolio Performance Measurement and Attribution'"]
---

## En una frase

La caída máxima es la mayor pérdida porcentual que ha sufrido tu curva de capital desde un
máximo hasta el mínimo anterior a recuperarlo, y no basta con saber cuánto cayó: hay que saber
cuánto tardó en volver.

## La idea

Imagina que dos conductores llegan al mismo destino. Uno aparca con el depósito lleno; al otro
se le encendió la reserva hace ochenta kilómetros. Han recorrido exactamente lo mismo, pero solo
uno podría haber seguido viaje. Con una estrategia pasa igual: dos sistemas que acaban el año con
un +20 % no son comparables si uno pasó por un −5 % y el otro por un −40 %, porque el segundo te
habría obligado a decidir si seguías justo en el peor momento posible.

La caída máxima (max drawdown) responde a la pregunta «¿cuánto llegué a perder desde el último
máximo?». No es el riesgo de una operación concreta ni la volatilidad: es el recorrido de la
curva de capital de arriba abajo. Es la métrica que más se nota en la cuenta y en la cabeza, y
la que menos aparece en los folletos comerciales.

Conviene separar dos cantidades que se confunden todo el tiempo:

- **Profundidad:** cuánto cayó, en porcentaje sobre el pico. Un 20 % significa que llegaste a
  tener un 20 % menos que tu máximo.
- **Duración:** cuánto tiempo estuvo la curva por debajo de ese pico. Una caída del 20 % que se
  recupera en dos meses es un problema muy distinto de una del 20 % que tarda cuatro años.

Y hay una asimetría que se olvida siempre: caídas y subidas no son simétricas. Si pierdes un
50 %, necesitas un 100 % para volver al punto de partida. Por eso las rachas malas pesan mucho
más de lo que sugiere su porcentaje, y por eso un drawdown grande es tan difícil de digerir: no
solo te quita dinero, te quita la capacidad de recuperarlo con el mismo esfuerzo.

El drawdown es también la métrica más útil para decidir el tamaño de tus posiciones, porque es
lo que un inversor (o un bróker) mira para decidir si te deja seguir. Un sistema con una
rentabilidad excelente y un drawdown del 60 % es, en la práctica, un sistema que casi nadie
ejecuta hasta el final.

## Definición formal

Con `C(t)` el valor de la curva de capital (o del patrimonio) en el instante `t`:

:::formula
DD(t) = ( max_{s ≤ t} C(s) − C(t) ) / max_{s ≤ t} C(s)
:::

:::formula
MDD = max sobre t de DD(t)
:::

- `C(t)` — capital en el instante `t`. Puede ser el valor de una cartera, de una cuenta o de una
  estrategia normalizada a 100.
- `max_{s ≤ t} C(s)` — el máximo alcanzado **hasta** `t`, llamado pico móvil. Es un máximo
  acumulado, no el máximo de toda la serie: en cada instante solo se mira hacia atrás.
- `DD(t)` — caída en ese instante, en tanto por uno (0,2 equivale al 20 %). Vale 0 cuando la
  curva está en su máximo histórico de la muestra.
- `MDD` — la mayor de todas las `DD(t)`. Se calcula sobre la curva de capital, nunca sobre la
  serie de retornos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `C(t)` | El capital (o el valor de la cartera) en el instante `t` | dinero o índice (base 100) | No es una palanca: es lo que mides. La escala da igual, porque la caída va en porcentaje: 10.000 € o 100 dan el mismo 15,18 % |
| `max_{s ≤ t} C(s)` | El pico móvil: el máximo alcanzado **hasta** `t`, mirando solo hacia atrás | igual que `C(t)` | Cuanto más alto quede el pico, mayor sale la caída porcentual desde él. No es el máximo de toda la serie: si el máximo llega después del fondo, no entra en la cuenta |
| `DD(t)` | La caída en ese instante: cuánto has perdido desde el pico | tanto por uno (0,2 equivale al 20 %) | Vale 0 justo cuando la curva marca un máximo nuevo, sube al alejarte de él y solo vuelve a cero cuando lo recuperas |
| `MDD` | La mayor de todas las `DD(t)`: el número que se publica | tanto por uno | Solo puede crecer cuando añades historia, porque hay más ocasiones de encontrar una caída peor. El `MDD` histórico no es una cota de lo que puede pasar |
| Duración | Periodos entre el pico que inicia el `MDD` y el momento en que la curva lo recupera | periodos (meses, sesiones) | No entra en la fórmula y es la otra mitad de la historia: un 15 % que se recupera en tres meses y otro que tarda tres años tienen el mismo número y efectos psicológicos opuestos |
| Frecuencia de medida | Cada cuánto se muestrea la curva: diaria, mensual | — | No es un parámetro de la fórmula y es el que más cambia el resultado: con datos diarios el `MDD` sale siempre mayor o igual que con mensuales, porque la vela mensual no ve el mínimo de dentro del mes |
:::

Definiciones que van de la mano:

- **Duración de la caída** (underwater period): desde el pico que inicia el `MDD` hasta el
  primer instante en que `C(t)` vuelve a ese pico.
- **Factor de recuperación:** rentabilidad total del periodo dividida entre el `MDD`.
- **Calmar:** rentabilidad anualizada dividida entre el `MDD`. Es el «cuánto gano por cada punto
  de caída» y lo tienes desarrollado en [[sortino-y-calmar]].

:::figura
fichero: drawdown-profundidad-y-duracion
pie: Arriba, la curva del ejemplo: el pico de 11.200 € en el mes 3, el fondo de 9.500 € en el mes 6 y la zona roja, que es todo el tiempo que la cuenta estuvo por debajo de su máximo. Abajo está esa misma distancia mes a mes: su altura es lo que se publica (15,18 %) y su anchura es la duración (seis meses hasta volver al pico en el mes 9). Quédate con el detalle que decide si aguantas: recuperar un 15,18 % exige subir un 17,89 %, porque el porcentaje se mide sobre el capital ya reducido.
fuente: figuras/maximo-drawdown-1.py
:::

:::aviso
El `MDD` depende de la frecuencia de los datos. Con datos diarios sale siempre mayor o igual que
con datos mensuales, porque la vela mensual esconde mínimos que sí ocurrieron. Si comparas dos
estrategias, calcula el `MDD` a la misma frecuencia y dilo en voz alta.
:::

## Ejemplo

Estos son los doce valores mensuales de una cuenta que empieza con 10.000 €:

```
10.000  10.500  11.200  10.800  10.100   9.500
10.200  11.000  11.600  11.400  12.100  12.400
```

- El pico antes de la caída está en el tercer mes: **11.200 €**.
- El mínimo llega en el sexto mes: **9.500 €**.
- Caída máxima: (11.200 − 9.500) / 11.200 = 0,1518, es decir **15,18 %**.
- La curva vuelve a 11.200 € en el noveno mes, cuando marca 11.600 €. Duración: **6 meses** por
  debajo del pico.
- Para pasar de 9.500 € a 11.200 € hace falta un **+17,89 %**, no un 15,18 %.

Fíjate en el último detalle: la caída fue del 15,18 % y la subida necesaria para repararla es
del 17,89 %, porque el porcentaje de recuperación se mide sobre el capital ya reducido. La
cuenta acaba el año con 12.400 €, un +24 % sobre el inicio, y sin embargo pasó medio año por
debajo de su máximo. Ese medio año es la parte de la historia que decide si alguien aguanta.

## Código

```python verificable
import numpy as np

capital = np.array([10000, 10500, 11200, 10800, 10100, 9500,
                    10200, 11000, 11600, 11400, 12100, 12400], dtype=float)
meses = np.arange(1, capital.size + 1)

picos = np.maximum.accumulate(capital)      # maximo alcanzado hasta cada mes
caidas = (picos - capital) / picos          # drawdown en cada mes
i_fondo = int(caidas.argmax())
i_pico = int(capital[:i_fondo + 1].argmax())
vuelta = np.flatnonzero(capital[i_fondo:] >= capital[i_pico])

print(f"pico         mes {meses[i_pico]:>2}  {capital[i_pico]:>7.0f}")   # -> mes  3    11200
print(f"fondo        mes {meses[i_fondo]:>2}  {capital[i_fondo]:>7.0f}")  # -> mes  6     9500
print(f"caida maxima {caidas[i_fondo]:.2%}")                              # -> 15.18%
print(f"duracion     {meses[i_fondo + vuelta[0]] - meses[i_pico]} meses")  # -> 6 meses
print(f"recuperacion {(capital[i_pico] / capital[i_fondo] - 1):.2%}")      # -> 17.89%
```

:::claves
- `dtype=float` en el `np.array` fija el tipo de todo el array: con enteros, cualquier división posterior crearía un array nuevo de decimales, pero asignar un resultado decimal dentro del array de enteros lo truncaría en silencio.
- `np.arange(1, capital.size + 1)` empieza en 1 y **no** incluye el final: es la forma cómoda de numerar los meses del 1 al 12. `capital.size` es el número de elementos, igual que `len(capital)` en un array de una dimensión.
- `np.maximum.accumulate(capital)` es el pico móvil, y `caidas.argmax()` devuelve la **posición** del fondo (5), no el valor: por eso el mes del fondo es `meses[i_fondo]`. El código lo envuelve en `int(...)` porque los índices de NumPy son `np.int64`: sirven para indexar, pero al guardarlos o compararlos se comportan de forma distinta a un `int` de Python.
- `capital[:i_fondo + 1].argmax()` busca el pico **solo hasta el fondo**, y ese `+1` está porque el corte no incluye el último índice. Si buscaras el máximo de toda la serie, cuando el máximo llega después de la caída señalarías un pico que no causó nada.
- `np.flatnonzero(capital[i_fondo:] >= capital[i_pico])` devuelve posiciones **relativas** al trozo recortado, y por eso el código suma `i_fondo` antes de convertirlas en meses. Con `np.where` obtendrías una tupla con un array dentro y todo el código de después tendría que cambiar.
- `f"{caidas[i_fondo]:.2%}"` imprime `15.18%` y `f"{capital[i_pico]:>7.0f}"` alinea a la derecha en 7 caracteres sin decimales: lo que ves en pantalla está redondeado. Comparar dos estrategias con los números redondeados puede darte un empate que en los datos no existe.
:::

```python verificable
import numpy as np

# Dos estrategias que acaban el ano igual (+20 %) con caminos muy distintos.
suave = np.array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120], dtype=float)
brusca = np.array([100, 130, 128, 150, 120, 145, 118, 140, 112, 118, 120], dtype=float)

def caida_maxima(curva):
    picos = np.maximum.accumulate(curva)
    return float(((picos - curva) / picos).max())

print(f"suave   final {suave[-1] / suave[0] - 1:+.0%}   caida {caida_maxima(suave):.2%}")
# -> suave   final +20%   caida 0.00%
print(f"brusca  final {brusca[-1] / brusca[0] - 1:+.0%}   caida {caida_maxima(brusca):.2%}")
# -> brusca  final +20%   caida 25.33%
# Bajar de 150 a 112 y volver arriba cuesta mas de lo que sugiere el 25 % de caida.
print(f"la brusca necesita {(150 / 112 - 1):+.2%} para volver al pico")
# -> la brusca necesita +33.93% para volver al pico
```

## Errores típicos

- **Comparar caídas medidas a frecuencias distintas.** Un `MDD` con datos diarios y otro con
  datos mensuales no son comparables: el diario ve mínimos que el mensual no. Elige una
  frecuencia y úsala para todo.
- **Confundir el drawdown con la peor operación.** Son cosas distintas: el drawdown es de la
  curva de capital y acumula varias operaciones perdedoras seguidas. Puedes tener un drawdown
  del 20 % con operaciones que individualmente nunca perdieron más del 1 %.
- **Mirar solo la profundidad e ignorar la duración.** Un 15 % que se recupera en tres meses y
  uno que tarda tres años tienen el mismo número y efectos psicológicos opuestos. Publica
  ambas cifras.
- **Medir el drawdown en la misma muestra donde elegiste la estrategia.** Si pruebas 200
  variantes y eliges la de menor drawdown, ese número está sesgado a la baja; es el mismo
  problema que describe [[data-snooping-y-multiple-testing]].
- **Creer que «ya ha caído bastante y no puede caer más».** El drawdown pasado no es una cota:
  es el mayor que ha ocurrido, no el mayor que puede ocurrir. Tratar un −20 % histórico como
  máximo garantizado es una falacia del jugador aplicada a tu cuenta.
- **Calcular el drawdown con la curva teórica sin costes.** Comisiones y deslizamiento
  ([[slippage-y-comisiones]]) hacen la caída más profunda y la recuperación más lenta. Un
  backtest sin costes siempre presume de un drawdown que no vas a vivir.

:::practica
enunciado: Doce capitales mensuales: 10.000, 11.000, 12.500, 14.000, 13.200, 12.000, 10.000, 11.500, 12.800, 13.400, 14.100, 14.600. Calcula el pico, el fondo, la caída máxima, cuánto hay que subir para recuperar y cuántos meses dura.
pista: El pico es el máximo alcanzado hasta el fondo, no el máximo de toda la serie.
solucion: Pico: 14.000 en el mes 4. Fondo: 10.000 en el mes 7. Caída: (14.000 − 10.000) / 14.000 = 28,57 %. Recuperación: 14.000 / 10.000 − 1 = +40 %, no un 28,57 %. La curva vuelve a superar 14.000 en el mes 11, con 14.100: seis meses por debajo del pico. Conclusión: la cuenta acaba con un +46 % y aun así pasó medio año sin recuperar su máximo.
:::

## Comprueba que lo sabes

:::quiz
p: Una cuenta va de 10.000 a 12.000, cae a 9.000 y luego sube a 13.000. ¿Cuál es la caída máxima?
o: El 25 %, porque (12.000 − 9.000) / 12.000 = 0,25
o: El 10 %, porque 9.000 es un 10 % menos que 10.000
o: El 33 %, porque hay que subir un 33 % desde 9.000 para volver a 12.000
a: 1
e: La caída se mide sobre el pico alcanzado hasta ese momento, que es 12.000, no sobre el capital inicial. (12.000 − 9.000) / 12.000 = 25 %. El 33 % es la subida necesaria para recuperar, que es otra cifra distinta y no mide la caída.
:::

:::quiz
p: ¿Por qué dos estrategias con la misma rentabilidad anual pueden tener drawdowns muy distintos?
o: Porque el drawdown no depende del resultado final, sino del orden y del tamaño de los retrocesos intermedios
o: Porque el drawdown se calcula con los retornos y no con el capital
o: Porque una de las dos tiene necesariamente más volatilidad y eso es lo único que importa
a: 1
e: El resultado final depende de la suma (o el producto) de los retornos, y el drawdown depende del camino: la misma secuencia de operaciones barajada da el mismo total y otro drawdown. La volatilidad influye, pero no es lo único: la racha y el orden importan.
:::

:::trampa
Si tu backtest tiene un drawdown del 8 % y crees que eso es poco, mira cuántos datos lo
sostienen y si el periodo incluyó alguna crisis. Un drawdown calculado sobre tres años tranquilos
no dice nada sobre lo que hará tu estrategia cuando el mercado cambie de régimen, y
[[regimenes-de-mercado]] existe precisamente porque ese cambio es lo normal, no la excepción.
:::
