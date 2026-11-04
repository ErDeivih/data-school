---
id: pairs-trading
titulo: Trading de pares
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [cointegracion, z-score-y-estandarizacion, correlacion-pearson-spearman]
tags: [pairs, cointegracion, reversion, costes]
resumen: Dos activos, un diferencial y un z-score: cómo elegir el par, estimar el ratio de cobertura y decidir la salida sin engañarte con la muestra.
fuentes: ["Gatev, Goetzmann y Rouwenhorst (2006), 'Pairs Trading: Performance of a Relative-Value Arbitrage Rule'", "Vidyamurthy (2004), 'Pairs Trading: Quantitative Methods and Analysis'"]
---

## En una frase

El trading de pares compra el activo que se ha quedado barato respecto a su pareja y vende el
caro, apostando a que la relación entre los dos se restablece.

## La idea

Dos supermercados de la misma cadena, uno en un barrio caro y otro en uno humilde. Sus ventas
no son iguales, pero se mueven juntas: si un mes sube el consumo en toda la ciudad, suben las
dos. Un día observas que la tienda del barrio humilde vende mucho menos de lo que le
correspondería por cómo va la del barrio caro. Antes de concluir que hay una oportunidad,
compruebas que la relación es real: misma cadena, mismos proveedores, misma política de
precios. Si lo es, apuestas a que la diferencia se cierra, y para eso **compras la que se ha
quedado atrás y vendes la que se ha adelantado**. Da igual si el consumo global sube o baja:
lo que te importa es el diferencial.

Ese es el trading de pares, y tiene dos trampas que se llevan por delante a la mayoría:

1. **Correlación no es cointegración.** Dos series pueden correlacionarse un 0,9 en una muestra
   y separarse para siempre. La correlación mide si se mueven juntas en los cambios; la
   cointegración mide si la **diferencia** entre ellas es estable. Puedes tener la primera sin
   la segunda, y la primera no sirve para operar un diferencial.
2. **La relación puede romperse de verdad.** Una fusión, un cambio de regulación, un escándalo
   contable o la entrada de un competidor cambian la relación entre las dos empresas. En ese
   caso el diferencial no se cierra porque ya no hay relación que cerrar, y la posición que
   tenías abierta se convierte en dos apuestas direccionales.

El oficio está en elegir el par por una razón económica (mismo sector, misma cadena de valor,
mismos clientes) y en usar el z-score del diferencial como regla objetiva de entrada y salida.
El par se elige con la cabeza; la operación, con el número.

:::figura
fichero: pairs-trading-diferencial-y-stop
pie: Arriba, los dos precios en logaritmos: comparten el paseo común y por eso su diferencia tiene nivel al que volver. En medio, el diferencial con la banda de ±1,5 desviaciones y las 12 operaciones sombreadas (verde comprando el diferencial, rosa vendiéndolo). Abajo está la decisión que no se puede tomar por opinión: el stop cuesta 0,027 de resultado bruto pero reduce la peor racha de −0,023 a −0,012, y esa peor racha es la cifra con la que se dimensiona la posición.
fuente: figuras/pairs-trading-1.py
:::

## Definición formal

Trabaja siempre con **logaritmos** de los precios, para que el diferencial sea comparable en
el tiempo y entre niveles de precio. Con los precios de dos activos, `P_A` y `P_B`:

:::formula
diferencial_t = ln(P_A,t) − β · ln(P_B,t)
:::

- `ln(P_A,t)`, `ln(P_B,t)` — logaritmo del precio de cada activo en `t`. Se usan logaritmos
  porque un 1 % de subida es siempre 0,01, valga la acción 10 o 500.
- `β` (beta) — el **ratio de cobertura**: cuántas unidades de `B` hacen falta para compensar
  una unidad de `A`. Se estima regresando `ln(P_A)` sobre `ln(P_B)` con datos anteriores al
  periodo que vas a operar. Si `β = 1,25`, por cada euro largo en `A` vendes 1,25 euros de `B`.
- `diferencial_t` — la serie que se supone estacionaria. Es la que se opera.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P_A,t`, `P_B,t` | Precio de cada activo en `t` | EUR | No se usan en crudo: se toman logaritmos para que un 1 % sea 0,01 valga la acción 10 o 500 |
| `β` | Ratio de cobertura: log-unidades de `B` por cada log-unidad de `A` | adimensional | Con `β = 1,25`, por cada euro largo en `A` se venden 1,25 de `B`. Si se estima en un periodo tranquilo y la volatilidad relativa cambia después, `β` deja de ser el ratio correcto y el diferencial se desplaza sin que ninguna empresa haya hecho nada |
| `diferencial_t` | `ln(P_A) − β·ln(P_B)`, la serie que se opera | log-unidades | Es la serie cuya estacionariedad hay que contrastar antes de operar; si pasea, un z-score de 2,5 solo describe el nivel actual |
| `m` | Media del diferencial en la ventana de estimación | log-unidades | Desplaza el centro de la banda. Estimarla con el periodo que vas a operar es mirar al futuro y hace que todos los pares funcionen |
| `s` | Desviación típica del diferencial en esa misma ventana | log-unidades | Es el ancho de la banda. Cuanto más pequeña, más señales y más falsas: con `s` pequeño el ruido cruza el umbral constantemente |
| `z_t` | z-score: `(diferencial − m) / s` | desviaciones típicas | Es la señal. Entradas típicas en ±1,5 o ±2, salidas en 0 y stop en ±2,5 o ±3,5: alejar el umbral de entrada reduce operaciones y también la muestra con la que juzgas la regla |
| `φ` | Coeficiente del AR(1) ajustado al diferencial | entre 0 y 1 | Más cerca de 1 = vuelve más despacio. La vida media es `−ln(2)/ln(φ)`: 11 periodos con 0,94, 34 con 0,98. Si supera tu horizonte de paciencia, no hay operación |
| `vida media` | Periodos que tarda el diferencial en recorrer la mitad de su desviación | periodos | Es el presupuesto de tiempo de la operación: con él se decide cuánto se aguanta antes de cerrar por tiempo |
| `stop` | Umbral de z que cierra la posición perdiendo | desviaciones típicas | Cuanto más lejos, más bruto se conserva y más grande es la peor excursión adversa. Es un intercambio, no una mejora gratis: se elige por la peor racha que toleras |
:::

El z-score del diferencial respecto a su comportamiento histórico es la señal:

:::formula
z_t = (diferencial_t − m) / s
:::

- `m` — media del diferencial en la ventana de estimación.
- `s` — desviación típica del diferencial en esa misma ventana.
- Regla típica: entrar cuando `z` supera +1,5 o 2 vendiendo el diferencial (corto en `A`,
  largo en `B`) y cuando baja de −1,5 o −2 comprándolo. Salir cuando `z` cruza 0, y cerrar por
  stop cuando `z` supera ±2,5 o ±3,5, o por tiempo si la operación no se resuelve.
- La **vida media** del diferencial sale de ajustar un AR(1) sobre él:
  `vida media = −ln(2) / ln(φ)`, con `φ` el coeficiente estimado. Si la vida media es mayor que
  tu horizonte de paciencia, no hay operación.

Las tres condiciones que hacen que el esquema sea honesto:

1. **`β`, `m` y `s` se estiman con una parte de la muestra y se operan con la otra.** Nunca con
   todo el histórico: eso es [[sesgo-de-mirar-al-futuro|mirar al futuro]].
2. **El diferencial tiene que ser estacionario.** Contrasta la cointegración antes de operar;
   un z-score de 2,5 sobre una serie que pasea es solo el nivel actual.
3. **La neutralidad es por importe, no por sensibilidad.** Igualar el valor de las dos patas no
   iguala sus betas al mercado; eso se corrige con el `β` estimado y se comprueba después.

## Ejemplo

Dos series de precios construidas con un factor común y una desviación que revierte con
`φ = 0,94`. La primera mitad de los datos (450 observaciones) sirve para estimar; la segunda,
para operar.

- Ratio de cobertura estimado: `β = 1,271`.
- En la segunda mitad, el z-score del diferencial va de **−2,27 a +3,38**, y pasa 88 de 450
  días fuera de la banda de ±1,5.
- Con entrada cuando `z` supera 1,5 o baja de −1,5, salida en `z = 0`, stop cuando `z` supera
  2,5 o baja de −2,5, y una regla de espera que impide volver a entrar hasta que `z` regrese a
  la zona central: **12 operaciones** en 450 días.

Los resultados de esas 12 operaciones, en unidades del diferencial y con una unidad de
exposición por operación:

```
con stop 2,5   operaciones  12   bruto +0,2128   neto +0,2080   peor racha -0,0122
sin stop       operaciones  12   bruto +0,2395   neto +0,2347   peor racha -0,0229
```

Aquí está la decisión que hay que tomar con números y no con opiniones. El stop **cuesta**
0,0267 de resultado bruto (de 0,2395 a 0,2128) y a cambio **reduce casi a la mitad** la peor
excursión adversa (de −0,0229 a −0,0122). Si tu tamaño de posición se fija por la peor
excursión, el stop te permite doblar el tamaño y compensar de sobra lo que pagas. Si no lo
haces, el stop solo te ha costado dinero. Y el coste de las dos patas, a 2 puntos básicos por
pata y operación (0,0004 por operación), se lleva 0,0048 del bruto: poco en este ejemplo,
porque el diferencial se mueve mucho. Cuando el diferencial se mueve poco, ese mismo coste se
come la operación entera.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(7)
n = 900
comun = np.cumsum(rng.normal(0, 0.01, n))        # paseo comun: el "mercado"
desv = np.zeros(n)
for t in range(1, n):
    desv[t] = 0.94 * desv[t - 1] + rng.normal(0, 0.008)   # diferencial que revierte
log_a = 4.0 + comun + 0.5 * desv
log_b = 3.5 + 0.8 * comun + rng.normal(0, 0.003, n)

m = n // 2
beta = np.polyfit(log_b[:m], log_a[:m], 1)[0]    # ratio de cobertura, solo con la primera mitad
spread = log_a - beta * log_b
mu, sd = spread[:m].mean(), spread[:m].std(ddof=1)
z = (spread - mu) / sd

print("beta estimada %.3f" % beta)
print("z fuera de muestra: min %+.2f  max %+.2f" % (z[m:].min(), z[m:].max()))
print("dias con z fuera de +-1,5: %d de %d" % (int(np.sum(np.abs(z[m:]) > 1.5)), n - m))
# -> beta estimada 1.271
# -> z fuera de muestra: min -2.27  max +3.38
# -> dias con z fuera de +-1,5: 88 de 450
```

:::claves
- `np.polyfit(log_b[:m], log_a[:m], 1)` devuelve los coeficientes **de mayor a menor grado**: `[pendiente, ordenada]`. Por eso se toma `[0]`, que es la pendiente; si tomas `[1]` obtienes la ordenada en el origen (un número alrededor de 1) y el diferencial sale con un desplazamiento constante que el z-score no absorbe, porque `mu` se estima después. Y el orden de los argumentos importa: es `(x, y)`, así que `polyfit(log_b, log_a)` estima `A` en función de `B`. Invertirlos da la beta recíproca (1/1,271 = 0,787) y compra y vende las patas al revés, sin ningún error.
- `spread = log_a - beta * log_b` trabaja con dos series de la **misma longitud**, elemento a elemento. Si una de las dos viniera de un `diff` tendría una fila menos y NumPy fallaría al restar, pero si viniera de un `cumsum` con un elemento de más, la resta daría un array de longitud distinta sin avisar hasta mucho después. Merece la pena comprobar `log_a.shape == log_b.shape` antes de operar.
- `spread[:m].mean()` y `spread[:m].std(ddof=1)` son la línea que separa un backtest de una fantasía. Con `spread.mean()` y `spread.std()` sobre las 900 observaciones, la media y la desviación ya saben lo que va a pasar en los 450 días que luego se operan: el z-score se vuelve más extremo justo en los sitios donde después hay corrección y el número de operaciones y su resultado mejoran sin que la regla haya mejorado.
- `ddof=1` divide entre `n−1` y `ddof=0` entre `n`. Sobre 450 observaciones la diferencia es del 0,1 % y no cambia nada; sobre ventanas cortas (30 días) el z-score sale hasta un 1,7 % más ancho con `ddof=0` y las entradas se adelantan. NumPy usa `ddof=0` por defecto, así que `np.std(spread[:m])` **no** es lo que quieres aquí: hay que pedir `ddof=1`. pandas, en cambio, ya usa `ddof=1` en `Series.std()`, igual que la estadística de manual.
- `z = (spread - mu) / sd` se calcula para las 900 filas, pero solo se usa desde `m`. Calcularlo entero es cómodo para dibujar; usarlo entero para decidir sería el error anterior. Si el código que opera leyera `z[t]` para `t < m`, estaría operando dentro de la muestra de estimación, que es donde la regla se eligió.
- `np.sum(np.abs(z[m:]) > 1.5)` suma una máscara booleana: `True` vale 1 y `False` vale 0, así que cuenta los días fuera de banda. Funciona, pero solo si se envuelve en `int()` al imprimir con `%d`, porque el resultado de `np.sum` es un entero de NumPy y no un `int` de Python. Con `(z[m:] > 1.5).sum()` se cuenta solo un lado, que es la mitad de la historia.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(7)
n = 900
comun = np.cumsum(rng.normal(0, 0.01, n))
desv = np.zeros(n)
for t in range(1, n):
    desv[t] = 0.94 * desv[t - 1] + rng.normal(0, 0.008)
log_a = 4.0 + comun + 0.5 * desv
log_b = 3.5 + 0.8 * comun + rng.normal(0, 0.003, n)

m = n // 2
beta = np.polyfit(log_b[:m], log_a[:m], 1)[0]
spread = log_a - beta * log_b
mu, sd = spread[:m].mean(), spread[:m].std(ddof=1)

def simula(stop, espera=0.5, entrada=1.5, salida=0.0):
    """Tras cerrar no se vuelve a entrar hasta que el z vuelve a la zona de espera."""
    pos, pnl, bloqueado = 0, 0.0, False
    ops, peor = [], []
    for t in range(m, n - 1):
        z = (spread[t] - mu) / sd
        if bloqueado and abs(z) < espera:
            bloqueado = False
        if pos == 0 and not bloqueado:
            if z > entrada:
                pos, ops, peor = -1, ops + [0.0], peor + [0.0]
            elif z < -entrada:
                pos, ops, peor = 1, ops + [0.0], peor + [0.0]
        if pos != 0:
            cambio = pos * (spread[t + 1] - spread[t])
            ops[-1] += cambio
            peor[-1] = min(peor[-1], ops[-1])
            pnl += cambio
            if (pos == 1 and (z >= salida or z <= -stop)) or (pos == -1 and (z <= salida or z >= stop)):
                pos, bloqueado = 0, True
    return pnl, ops, peor

coste = 0.0004          # dos patas, 2 pb por pata y operacion
for etiqueta, stop in (("con stop 2,5", 2.5), ("sin stop", 99.0)):
    pnl, ops, peor = simula(stop)
    print("%-12s operaciones %3d  bruto %+7.4f  neto %+7.4f  peor racha %+.4f"
          % (etiqueta, len(ops), pnl, pnl - coste * len(ops), min(peor)))
# -> con stop 2,5 operaciones  12  bruto +0.2128  neto +0.2080  peor racha -0.0122
# -> sin stop     operaciones  12  bruto +0.2395  neto +0.2347  peor racha -0.0229
```

El bloque de la regla de espera (`bloqueado`) no es un adorno: sin él, el algoritmo vuelve a
entrar en la misma dirección al día siguiente de saltar el stop, porque el z-score sigue
fuera de la banda. Ese bucle de reentradas es exactamente lo que convierte un stop razonable
en una sangría de comisiones.

## Errores típicos

- **Elegir el par por correlación.** Dos acciones del mismo sector suben y bajan juntas y
  pueden separarse un 40 % sin volver. Antes de operar, contrasta que el diferencial es
  estacionario; la correlación no te lo dice.
- **Estimar `β`, `m` y `s` con toda la muestra.** Es el error que hace que todos los pares
  funcionen. Si la media y la desviación del diferencial se calculan con el periodo que vas a
  operar, el z-score está mirando al futuro que dice predecir.
- **No poner stop, o peor, promediar a la baja.** Toda la tesis es que el diferencial vuelve, y
  el stop es la admisión de que a veces la tesis es falsa: sin él, una ruptura estructural se
  lleva la cuenta entera. Doblar la posición cuando `z` llega a 3 cambia la apuesta por «vuelve
  pronto y mucho», que es la forma más rápida de convertir una pérdida controlada en una
  catastrófica.
- **Olvidar la financiación y el préstamo.** Operar un par son dos posiciones, con dos
  comisiones, dos diferenciales y a menudo un coste por pedir prestado el activo que vendes en
  corto. Si ese activo es difícil de prestar, el coste puede superar el beneficio esperado.
- **Escoger el par con la prueba que más te gusta.** Si pruebas 200 pares y te quedas con el
  que da el p-valor más bajo, el resultado está sesgado. Ajusta por el número de pruebas con
  [[sharpe-deflactado|el Sharpe deflactado]] o reserva una muestra intacta.
- **Operar sobre precios en vez de logaritmos.** El ratio de cobertura y el diferencial dejan
  de ser comparables cuando los precios cambian de nivel, y el z-score de una diferencia de
  precios no es el mismo número que el de una diferencia de logaritmos.

:::trampa
El retroceso del diferencial no siempre es tesis: a veces es que `β` está mal estimada. Si la
regresión se hizo en un periodo tranquilo y luego la volatilidad relativa de las dos patas
cambia, `β` deja de ser el ratio correcto y el diferencial se desplaza sin que ninguna de las
dos empresas haya hecho nada. Reestima `β` en ventanas móviles o con un filtro de Kalman, y
mira si el desplazamiento aparece justo cuando reestimas.
:::

:::practica
enunciado: Con ln(P_A) = 4,30 y ln(P_B) = 3,45 has estimado un ratio de cobertura β = 1,25 con la primera mitad de la muestra. En esa ventana el diferencial tuvo media 0,004 y desviación típica 0,008. Calcula el diferencial actual, su z-score y decide si hay operación, con qué patas y dónde saldrías.
pista: El diferencial es ln(P_A) − β · ln(P_B), y el z-score es (diferencial − media) / desviación.
solucion: β · ln(P_B) = 1,25 · 3,45 = 4,3125, así que el diferencial vale 4,30 − 4,3125 = −0,0125. El z-score es (−0,0125 − 0,004) / 0,008 = −2,06, por debajo de −1,5: el diferencial está barato, así que compras A y vendes 1,25 euros de B por cada euro puesto en A. La salida es en z = 0, es decir, cuando el diferencial vuelva a 0,004.
:::

## Comprueba que lo sabes

:::quiz
p: Encuentras dos acciones con correlación de 0,95 durante tres años. ¿Es suficiente para operar el par?
o: Sí, una correlación de 0,95 significa que el diferencial vuelve siempre
o: No: la correlación mide co-movimiento en los cambios, y el diferencial puede no ser estacionario
o: Sí, siempre que las dos sean del mismo sector
a: 2
e: La correlación alta no garantiza que la diferencia entre las series tenga un nivel estable: dos paseos aleatorios independientes pueden correlacionarse mucho en una muestra concreta y separarse después. Lo que necesitas es cointegración, que es una propiedad del diferencial, y se contrasta aparte.
:::

:::quiz
p: Con un stop que salta cuando `z` llega a 2,5 o a −2,5, el resultado bruto es 0,2128 y la peor excursión −0,0122; sin stop, el bruto es 0,2395 y la peor excursión −0,0229. ¿Cómo se decide?
o: Quitando el stop, porque el bruto es mayor
o: Comparando lo que cuesta el stop con lo que permite ganar al poder dimensionar la posición con una peor excursión menor
o: Poniendo el stop más lejos, en 3,5, que siempre mejora las dos cifras
a: 2
e: El stop cuesta 0,0267 de bruto y a cambio reduce la peor excursión casi a la mitad. Si el tamaño se fija por la peor excursión tolerada, menos excursión significa más tamaño y más resultado sobre el capital. Comparar solo el bruto ignora precisamente lo que el stop aporta; y alejar el stop no mejora las dos cifras a la vez, solo desplaza el equilibrio.
:::

:::aviso
Un par puede dejar de ser un par por una fusión, un cambio en el índice, una ampliación de
capital o un cambio regulatorio. Revisa la relación cada cierto número de periodos y cierra la
posición si el diferencial se rompe acompañado de una noticia estructural, aunque el z-score
te diga que la desviación es enorme.
:::
