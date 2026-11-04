---
id: volatilidad-realizada
titulo: Volatilidad realizada
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [retornos-logaritmicos, varianza-y-desviacion, autocorrelacion-acf-pacf, series-temporales-componentes]
tags: [volatilidad, series-temporales, riesgo]
resumen: La raíz de la suma de los retornos intradía al cuadrado mide cuánto se movió el precio de verdad, y es la variable de entrada de casi todo modelo de volatilidad.
fuentes: ["Andersen, Bollerslev, Diebold y Labys (2003), 'Modeling and Forecasting Realized Volatility'", "Corsi (2009), 'A Simple Approximate Long-Memory Model of Realized Volatility'"]
---

## En una frase

La volatilidad realizada de un día es la raíz de la suma de los cuadrados de sus retornos
intradía: usa todo el camino que recorrió el precio, no solo la diferencia entre el cierre de
ayer y el de hoy, y por eso estima muchísimo mejor cuánto se movió el mercado.

## La idea

La forma clásica de estimar la volatilidad de un día es coger el retorno de cierre a cierre y
elevarlo al cuadrado. Es un estimador insesgado, pero malísimo: usa **una** observación por
día y no ve nada de lo que pasó dentro de la sesión. Dos días con el mismo retorno de cierre
pueden haber sido un paseo tranquilo o una montaña rusa, y ese estimador los trata igual.

Un ejemplo extremo: un día en el que el precio abre en 100, sube a 103, baja a 97 y cierra en
100 tiene un retorno de cierre de exactamente 0, así que el estimador clásico diría que la
volatilidad de ese día fue cero. La volatilidad realizada de ese día es enorme, porque hubo un
6 % de recorrido. Al revés, un día que sube en línea recta de 100 a 102 tiene un retorno de
cierre del 2 % y muy poca volatilidad realizada: se movió mucho en una dirección, pero de
forma ordenada.

La idea es sencilla: si tienes el precio cada cinco minutos, tienes 78 observaciones por
sesión en lugar de una. Elevas al cuadrado cada retorno intradía, los sumas y tienes la
varianza del día. La raíz cuadrada es la volatilidad realizada. La razón de que la suma de
cuadrados funcione es la misma por la que la varianza de una suma de incrementos
independientes es la suma de las varianzas: cada cuadrado estima la contribución de ese tramo
a la variación total del día.

Hay un compromiso que hay que entender bien, porque es la mitad práctica del concepto. Cuanto
más fino muestreas, más observaciones tienes… y más ruido de microestructura metes. Los
precios rebotan entre el bid y el ask, y ese rebote no es información: son dos precios para el
mismo activo. Cada rebote aporta un cuadrado pequeño pero constante, y con miles de retornos
de un segundo el sesgo se acumula y la volatilidad realizada sale inflada. Al alargar el
intervalo, el rebote se cancela dentro de cada barra y el sesgo desaparece, pero te quedas con
menos observaciones. En acciones, el compromiso habitual es **cinco minutos**; la herramienta
para elegirlo en tu caso concreto es el *volatility signature plot*, que dibuja la volatilidad
realizada media frente al intervalo de muestreo y muestra la zona en la que el estimador se
estabiliza. Con datos de un segundo, ese gráfico suele tener una pendiente muy clara hacia
arriba en el extremo fino.

Dos propiedades que se usan constantemente. La primera: **las varianzas se suman en el
tiempo**. La varianza realizada de una semana es la suma de las cinco varianzas diarias; la
varianza de un mes, la suma de las del mes. Las volatilidades, en cambio, no se suman: si
sumas cinco volatilidades diarias te sale un número sin sentido. Para agregar volatilidades se
suman varianzas y se hace la raíz al final (bajo el supuesto de incrementos independientes).

La segunda: **la volatilidad se agrupa**. Días de mucha volatilidad tienden a ir seguidos de
días de mucha volatilidad, y lo mismo con la calma. La volatilidad realizada muestra
autocorrelación alta y persistente, mucho más que los retornos, que son casi incorrelacionados.
Eso es lo que la hace útil como variable predictiva y lo que sostiene modelos como
[[garch-volatilidad|GARCH]] o el modelo HAR, que predice la volatilidad de mañana con la de
hoy, la media de la última semana y la del último mes.

Y una tercera propiedad, más técnica: la volatilidad realizada es **asimétrica a la derecha**
(nunca es negativa y tiene una cola larga hacia arriba), mientras que su logaritmo se parece
bastante más a una normal. Por eso casi todos los modelos de volatilidad trabajan con
`ln(RV)`: una regresión lineal sobre RV en niveles se deja arrastrar por los días de pánico.

Sus usos son muy concretos: medir riesgo de una cartera, dimensionar posiciones con
volatilidad objetivo ([[tamano-de-posicion|vol targeting]]), alimentar modelos de predicción
con una variable limpia y diaria, y comparar la volatilidad que el mercado esperaba con la que
ocurrió de verdad. Esa última comparación es la que da sentido a la prima de riesgo de
volatilidad: la [[metricas-de-riesgo|volatilidad implícita]] de las opciones y la realizada
son cosas distintas y su diferencia no es un error de nadie.

:::figura
fichero: volatilidad-realizada-camino-y-sesgo
pie: Arriba, un día que baja a 98,95 y vuelve a cerrar en 100: el retorno de cierre es cero, así que el estimador clásico diría que no pasó nada, mientras la varianza realizada del camino es 2,28 · 10⁻⁴. Abajo, el otro extremo: muestreando cada minuto, el rebote bid-ask infla la varianza un 32 %; cada cinco minutos el sesgo cae al 6 % y la curva se pega a la verdad. Mira lo rápido que se aplana la curva roja: ahí está el compromiso entre tener más observaciones y meter más ruido.
fuente: figuras/volatilidad-realizada-1.py
:::

## Definición formal

Para un día `t` con `M` intervalos intradía:

:::formula
RV_t = Σ_{i=1}^{M} r_{t,i}²          σ̂_t = √RV_t
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `RV_t` | Varianza realizada del día `t`: la suma de los cuadrados de los retornos intradía | retorno al cuadrado | Es lo que se agrega en el tiempo y lo que se mete en el modelo; no es una volatilidad y no se compara con una implícita sin hacerle la raíz |
| `σ̂_t` | Volatilidad realizada del día `t` | tanto por uno por día | Es `√RV_t`, la cifra que se enseña y con la que se dimensiona una posición |
| `r_{t,i}` | Retorno logarítmico del intervalo `i` del día `t` | tanto por uno | Al elevarlo al cuadrado da igual su signo: subir y bajar contribuyen igual, así que `RV` no dice la dirección |
| `P_{t,i}` | Precio al final del intervalo `i` | EUR o índice | Un precio mal ajustado por un dividendo o un split mete un cuadrado enorme que domina todo el día |
| `M` | Número de intervalos del día (78 con barras de 5 minutos en una sesión de 6,5 horas) | entero | Más intervalos es más información y también más ruido de rebote: `M` se elige con el gráfico de firma, no con el máximo que permitan los datos |
| `i` | Índice del intervalo dentro del día | entero de 1 a `M` | El primer retorno se calcula contra el precio de apertura, `P_{t,0}`, no contra el cierre de ayer: mezclar los dos añade el hueco nocturno |
| `RV_{t:t+k}` | Varianza realizada de `k + 1` días | retorno al cuadrado | Suma las varianzas diarias. Sumar las **volatilidades** daría un número sin interpretación |
| `σ̂_anual` | Volatilidad anualizada | % anual | Sale de `√(252 · media(RV))`, nunca de multiplicar la varianza por 252, que deja el resultado en unidades al cuadrado |
| `β₀, β_d, β_w, β_m` | Coeficientes del modelo HAR: constante, diario, semanal y mensual | adimensionales | Suelen salir positivos y sumar algo menos que 1; si suman más, el modelo implica una volatilidad que crece sola, que en una serie real es señal de sobreajuste |
| `RV^(w)_{t−1}`, `RV^(m)_{t−1}` | Medias de la varianza realizada de los últimos 5 y 22 días | retorno al cuadrado | Son las que dan memoria larga al modelo: con solo el término diario, el HAR se queda en un GARCH disfrazado |
| `ε_t` | Error del modelo HAR en el día `t` | retorno al cuadrado | Absorbe lo que no explican los tres plazos; si su varianza cambia por tramos, queda estructura sin recoger |
:::

- `r_{t,i}` — retorno logarítmico del intervalo `i` del día `t`:
  `r_{t,i} = ln(P_{t,i} / P_{t,i−1})`.
- `P_{t,i}` — precio al final del intervalo `i` del día `t`; `P_{t,0}` es el precio de apertura.
- `M` — número de intervalos del día (con barras de 5 minutos en una sesión de 6,5 horas,
  `M = 78`).
- `RV_t` — varianza realizada del día `t`; está en unidades de retorno al cuadrado.
- `σ̂_t` — volatilidad realizada del día `t`, en las mismas unidades que los retornos (tanto
  por uno por día).

**Agregación y anualización.** Bajo incrementos independientes:

:::formula
RV_{t:t+k} = Σ_{j=0}^{k} RV_{t+j}          σ̂_anual = √(252 · media(RV_diaria))
:::

- `RV_{t:t+k}` — varianza realizada del periodo de `k + 1` días.
- La anualización correcta es `√252 · √(media de RV)`. Multiplicar la volatilidad diaria media
  por `√252` es equivalente, pero multiplicar la **varianza** por 252 te deja en unidades al
  cuadrado.

**Modelo HAR.** Con la volatilidad realizada diaria y sus medias de 5 y 22 días (semana y mes):

:::formula
RV_t = β₀ + β_d · RV^(d)_{t−1} + β_w · RV^(w)_{t−1} + β_m · RV^(m)_{t−1} + ε_t
:::

- `RV^(d)_{t−1}` — varianza realizada de ayer.
- `RV^(w)_{t−1}` — media de la varianza realizada de los últimos 5 días.
- `RV^(m)_{t−1}` — media de los últimos 22 días.
- `β₀, β_d, β_w, β_m` — coeficientes a estimar; suelen salir positivos y sumar algo menos
  que 1, lo que refleja la persistencia de la volatilidad.

## Ejemplo

Seis retornos logarítmicos de cinco minutos dentro de una sesión, en tanto por uno:

| Intervalo | Retorno | Retorno al cuadrado |
| --- | --- | --- |
| 1 | +0,0010 | 0,00000100 |
| 2 | −0,0020 | 0,00000400 |
| 3 | +0,0015 | 0,00000225 |
| 4 | −0,0005 | 0,00000025 |
| 5 | +0,0020 | 0,00000400 |
| 6 | −0,0010 | 0,00000100 |
| Suma | +0,0010 | 0,00001250 |

- Varianza realizada del día: `RV = 1,25 · 10⁻⁵`.
- Volatilidad realizada del día: `σ̂ = √(1,25 · 10⁻⁵) = 0,003536`, es decir un **0,354 %**
  diario.
- Anualizada: `0,003536 · √252 = 0,0561`, un **5,61 %** anual.
- Estimador clásico de cierre a cierre: el retorno del día es +0,0010 y su cuadrado es
  `1,00 · 10⁻⁶`, **doce veces y media más pequeño** que la varianza realizada. Y fíjate en que
  el precio acabó donde empezó más un 0,1 %: el día se movió de verdad y el estimador clásico
  casi no lo vio.

Con seis barras el ejemplo es una caricatura; con 78 barras de cinco minutos en una sesión real
el estimador es muchísimo más estable. Lo que no cambia es la lección: la información está en
el camino, no en los extremos.

## Código

```python verificable
import numpy as np

# Seis retornos logaritmicos de 5 minutos dentro de una sesion
r = np.array([0.0010, -0.0020, 0.0015, -0.0005, 0.0020, -0.0010])

rv = np.sum(r ** 2)                 # varianza realizada del dia
vol_dia = np.sqrt(rv)
vol_anual = vol_dia * np.sqrt(252)

print(f"varianza realizada  {rv:.3e}")            # -> 1.250e-05
print(f"volatilidad diaria  {vol_dia:.6f}")       # -> 0.003536
print(f"volatilidad anual   {vol_anual:.4f}")     # -> 0.0561
print(f"retorno del dia     {r.sum():+.4f}")      # -> +0.0010
print(f"ese retorno al cuadrado {r.sum() ** 2:.3e}")  # -> 1.000e-06
```

:::claves
- `r ** 2` eleva al cuadrado **cada elemento** y devuelve un array nuevo; no confundir con `r * r`, que aquí da lo mismo, ni con `r ** 2` sobre una matriz, que en NumPy es elemento a elemento y no producto matricial.
- `np.sum(r ** 2)` suma todos los cuadrados y devuelve un **escalar**, no un array. Con `r.sum() ** 2` se eleva al cuadrado la suma, que es una cuenta distinta: 1,000 · 10⁻⁶ frente a 1,250 · 10⁻⁵, doce veces y media más pequeño. Las dos líneas se parecen mucho y responden a preguntas opuestas.
- `np.sqrt(rv)` y `rv * np.sqrt(252)` son la raíz y la anualización. La segunda multiplica la **volatilidad** por `√252`; si en su lugar pusieras `rv * 252` anualizarías la varianza y el número quedaría en unidades al cuadrado, sin sentido para compararlo con una volatilidad implícita.
- Los nombres no llevan tilde a propósito (`varianza realizada`, `volatilidad diaria`) porque son texto de consola; los comentarios `# -> 1.250e-05` están escritos a mano y dejan de ser ciertos en cuanto cambies un solo retorno de la lista.
- La notación `.3e` imprime en notación científica con tres decimales, que es la única forma legible de ver 1,25 · 10⁻⁵. Con `.2f` el resultado sería `0.00` y parecería que la varianza es cero.
- En el segundo bloque, `[...].reshape(-1, factor).sum(axis=1)` es lo que convierte 780 retornos de un minuto en retornos de cinco: `axis=1` suma **dentro** de cada bloque, y sin ese `axis` se sumaría todo el array y se perdería la estructura temporal.
:::

```python verificable
import numpy as np

# El ruido de microestructura (rebote bid-ask) infla la varianza realizada al afinar el muestreo
rng = np.random.default_rng(1)
n = 780                                    # barras de 1 minuto en una sesion
verdadero = rng.normal(0, 0.0005, n)       # volatilidad real: 5 pb por minuto
rebote = 0.0002 * rng.choice([-1.0, 1.0], n)   # ruido puro, sin informacion

for factor in (1, 5, 15):
    corte = n - n % factor
    limpio = verdadero[:corte].reshape(-1, factor).sum(axis=1)
    observado = (verdadero + rebote)[:corte].reshape(-1, factor).sum(axis=1)
    print(f"cada {factor:>2} min: RV limpia {np.sum(limpio ** 2):.3e}  "
          f"RV con rebote {np.sum(observado ** 2):.3e}  inflado x{np.sum(observado ** 2) / np.sum(limpio ** 2):.2f}")
```

El segundo bloque deja el sesgo a la vista: al minuto, la varianza realizada con rebote sale
alrededor de un 20 % por encima de la limpia; cada cinco minutos, un 14 %; cada quince, un 3 %.
Al agregar, el rebote se cancela dentro de cada barra y el estimador se acerca al valor real.
Ese es exactamente el compromiso que se resuelve con el gráfico de firma de volatilidad.

## Errores típicos

- **Muestrear lo más fino que permitan los datos.** Con retornos de un segundo, el rebote
  bid-ask domina la suma de cuadrados y la volatilidad realizada puede salir varias veces por
  encima de la real. Elige el intervalo con un gráfico de firma de volatilidad y quédate en la
  zona estable; cinco minutos es el punto de partida habitual en acciones.
- **Confundir varianza realizada con volatilidad realizada.** `RV` está en unidades al
  cuadrado; para anualizar y para comparar con una volatilidad implícita hay que hacer la raíz.
  Un `RV` de 1,25 · 10⁻⁵ no es «un 0,00125 %», es un 0,354 % diario.
- **Sumar volatilidades para agregar días.** Si quieres la volatilidad de la semana, suma las
  varianzas diarias y haz la raíz al final. Sumar las cinco volatilidades diarias da un número
  sin interpretación.
- **Meter `RV` en niveles como variable de un modelo lineal.** La distribución es asimétrica a
  la derecha y un solo día de pánico distorsiona la regresión. Usa `ln(RV)`, que es mucho más
  simétrica y además mantiene la positividad.
- **Comparar volatilidades realizadas de sesiones o activos distintos sin normalizar.** Una
  sesión de tres horas, un día festivo con cierre temprano o un activo que cotiza 24 horas
  tienen distinto número de barras, así que sus `RV` no son comparables directamente: normaliza
  por barra y multiplica por las barras del día. Y dentro de una misma sesión, la volatilidad no
  se reparte uniformemente: se concentra en la apertura y en el cierre, de modo que la última
  hora no es comparable con la primera.
- **Tratar la volatilidad realizada como una medida de riesgo sin mirar la dirección.** Mide
  cuánto se movió el precio, no hacia dónde. Un día de subida del 5 % y uno de bajada del 5 %
  contribuyen igual a `RV`.

:::practica
enunciado: Cuatro sesiones seguidas tienen volatilidad realizada diaria del 1,2 %, 0,8 %, 1,5 % y 1,0 %. Calcula la volatilidad realizada de las cuatro sesiones juntas y su equivalente anual.
pista: Las volatilidades no se suman ni se promedian: pasa cada una a varianza, agrúpalas y haz la raíz al final.
solucion: Varianzas: 0,012² = 1,44 · 10⁻⁴; 0,008² = 0,64 · 10⁻⁴; 0,015² = 2,25 · 10⁻⁴; 0,010² = 1,00 · 10⁻⁴. Suma: 5,33 · 10⁻⁴. Raíz: √(5,33 · 10⁻⁴) = 0,02309, un 2,31 % en cuatro días. Anualizada: 0,02309 · √252 = 0,3665, un 36,65 % anual. Sumar las cuatro volatilidades daría 4,5 %, un número sin sentido: la agregación se hace con varianzas.
:::

## Comprueba que lo sabes

:::quiz
p: Un día el precio abre en 100, toca 103, baja a 97 y cierra en 100. ¿Qué dicen los dos estimadores?
o: Ambos dan volatilidad cero, porque el retorno de cierre es cero
o: El estimador de cierre a cierre da cero y la volatilidad realizada es alta, porque recorre todo el camino
o: La volatilidad realizada es cero y el estimador de cierre a cierre es alto
a: 2
e: El retorno de cierre a cierre es ln(100/100) = 0, así que su cuadrado es 0. La volatilidad realizada suma los cuadrados de los retornos intradía, que recogen la subida a 103 y la bajada a 97: el recorrido existió y el estimador clásico no lo ve.
:::

:::quiz
p: ¿Por qué no se usa el intervalo de muestreo más pequeño posible para calcular la volatilidad realizada?
o: Porque los datos de alta frecuencia son caros
o: Porque el rebote bid-ask introduce ruido que infla la suma de cuadrados al afinar el intervalo
o: Porque la fórmula de la varianza realizada exige exactamente 78 observaciones
a: 2
e: El ruido de microestructura aporta cuadrados pequeños pero constantes en cada retorno; con miles de retornos al día el sesgo se acumula y la estimación queda por encima de la volatilidad real. Por eso se busca el intervalo en el que el estimador se estabiliza, típicamente cinco minutos en acciones.
:::

:::quiz
p: Cuatro varianzas realizadas diarias consecutivas valen 4, 9, 16 y 25 (en las mismas unidades). ¿Cuál es la varianza realizada del periodo y la volatilidad media diaria?
o: La varianza del periodo es 54 y la volatilidad media diaria es √13,5, aproximadamente 3,67
o: La varianza del periodo es 13,5 y la volatilidad media diaria es 3,5
o: La varianza del periodo es 54 y la volatilidad media diaria es 3,5
a: 1
e: Las varianzas se suman: 4 + 9 + 16 + 25 = 54. La volatilidad media diaria se obtiene promediando varianzas y haciendo la raíz al final: √(54/4) = √13,5 ≈ 3,67. La opción 3 confunde promediar varianzas con promediar volatilidades: (2 + 3 + 4 + 5) / 4 = 3,5 subestima, porque la raíz cuadrada es cóncava y la media de las raíces es menor que la raíz de la media.
:::

:::aviso
La volatilidad realizada mide movimiento, no riesgo de pérdida. Una estrategia que gana un 3 %
todos los días con volatilidad realizada alta tiene menos riesgo de ruina que una que alterna
+10 % y −10 % con la misma volatilidad. Para riesgo de cola hacen falta
[[var-y-cvar|VaR, CVaR]] o la [[maximo-drawdown|caída máxima]].
:::
