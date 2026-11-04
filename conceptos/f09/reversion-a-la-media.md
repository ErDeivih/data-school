---
id: reversion-a-la-media
titulo: Reversión a la media
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [estacionariedad, z-score-y-estandarizacion, autocorrelacion-acf-pacf]
tags: [reversion, estacionariedad, senales, riesgo]
resumen: Si una serie vuelve a su nivel habitual, cada desviación es una oportunidad; si pasea, cada desviación es el principio de la siguiente. Distinguirlo es todo.
fuentes: ["Ornstein y Uhlenbeck (1930), 'On the theory of the Brownian motion'", "Poterba y Summers (1988), 'Mean Reversion in Stock Prices'"]
---

## En una frase

La reversión a la media dice que un valor que se ha alejado mucho de su nivel habitual
tiende a volver a él, y solo es cierta mientras ese nivel habitual siga existiendo.

## La idea

Piensa en un perro atado con una correa a una farola. El perro se aleja, olfatea, tira, pero
la correa lo devuelve una y otra vez cerca de la farola. Si ves al perro a diez metros de la
farola, apostar a que en un rato estará más cerca es razonable. Ahora cambia la escena por la
de un caminante borracho que sale de un bar: se aleja y no hay ninguna cuerda que lo traiga
de vuelta. Cada paso nuevo es el punto de partida del siguiente. Si confundes al perro con el
borracho, la misma apuesta que gana con uno te arruina con el otro.

Ese es el problema entero de la reversión a la media: **hay que decidir si la serie tiene
farola**. Los precios de las acciones, en niveles, se parecen mucho más al borracho que al
perro: una acción que cae de 100 a 60 no está «barata», está a 60. Lo que sí revierte, muchas
veces, es una **relación** entre dos series (el diferencial entre dos acciones parecidas, la
[[cointegracion|combinación lineal que es estacionaria]]), o la desviación de un precio
respecto a una referencia que se mueve despacio, como su propia media de 200 sesiones o el
valor razonable que estima un modelo de factores.

Hay tres ingredientes que convierten la intuición en una regla medible:

1. **Una referencia.** La media de la serie, o el valor que predice un modelo. Sin referencia
   no hay nada respecto a lo que estar desviado.
2. **Una medida de desviación** comparable entre series y entre épocas: el z-score, es decir,
   cuántas desviaciones típicas te has alejado. Así un 3 % de desviación en una serie nerviosa
   no se confunde con un 3 % en una serie tranquila.
3. **Una velocidad de retorno.** Cuánto tarda la desviación en corregirse. Es lo que decide si
   te da tiempo a ganar el movimiento después de pagar los costes.

El enemigo no es el ruido: es el **cambio de nivel**. Si la farola se muda, la correa sigue
tirando pero hacia otro sitio. Eso es lo que pasa cuando una empresa cambia de negocio, cuando
una fusión altera la relación entre dos acciones o cuando un régimen de mercado cambia las
correlaciones. La reversión a la media no avisa: simplemente deja de funcionar, y la posición
que tenías abierta se convierte en una apuesta direccional.

## Definición formal

El modelo mínimo de reversión es un proceso autorregresivo de orden 1:

:::formula
x_t = μ + ρ · (x_t−1 − μ) + ε_t ,  con −1 < ρ < 1
:::

- `x_t` — el valor de la serie (o de la desviación respecto a su referencia) en el instante `t`.
- `μ` — la media a la que la serie vuelve, el nivel de la farola.
- `ρ` (rho) — la persistencia: qué fracción de la desviación sobrevive de un periodo al
  siguiente. Cuanto más cerca de 1, más lenta es la vuelta.
- `1 − ρ` — la fracción de la desviación que se corrige en cada periodo. Con `ρ = 0,9`, cada
  periodo corrige el 10 % de lo que se había alejado.
- `ε_t` — el shock aleatorio del periodo, con media cero.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x_t` | El valor de la serie (o de la desviación respecto a su referencia) en el instante `t` | las de la serie | El nivel en sí no cambia el diagnóstico: lo que decide es si existe una referencia a la que volver. Si la serie es un paseo, `x_t` es el punto de partida de todo lo que venga después y no hay nada a lo que regresar |
| `μ` | La media a la que la serie vuelve: el nivel de la farola | las de la serie | Desplaza la serie entera sin cambiar su persistencia. Es la referencia, y por eso si `μ` se mueve (fusión, cambio de negocio, cambio de régimen) la reversión deja de funcionar aunque `ρ` siga siendo 0,9 |
| `ρ` | Persistencia: qué fracción de la desviación sobrevive de un periodo al siguiente | adimensional, entre −1 y 1 | Cuanto más cerca de 1, más lenta es la vuelta y más se parece a un paseo: `ρ = 0,9` da 6,6 periodos de vida media y `ρ = 0,99` da 69. Por encima de 0,98 el intervalo de confianza de `ρ` suele incluir el 1, y entonces no tienes una estrategia, tienes una duda |
| `1 − ρ` | La fracción de la desviación que se corrige en cada periodo | adimensional | Es la velocidad de la vuelta. Con `ρ = 0,9` se corrige el 10 % por periodo; con `ρ = 0,99`, el 1 % diario, que es lentísimo para una operación que paga coste cada vez que entra y sale |
| `d = 1 − ρ` (velocidad) | La misma corrección, escrita como la usan los modelos continuos | por periodo | En el proceso de Ornstein-Uhlenbeck, la vida media es `ln(2)/d`: con `d = 0,1`, 6,9 periodos. Es útil para comparar series de distinta frecuencia, pero sigue siendo el mismo número que `1 − ρ` |
| `ε_t` | El shock aleatorio del periodo, con media cero | las de la serie | Su desviación típica fija el tamaño de las desviaciones, no su duración. Con shocks más grandes la serie se aleja más de `μ` y hay más ocasiones de operar, pero también más riesgo de que un shock sea en realidad un cambio de nivel |
| `vida media` | El tiempo que tarda una desviación en reducirse a la mitad: `−ln(2)/ln(ρ)` | periodos (los de los datos: si son días, días) | Crece muy rápido al acercarse `ρ` a 1: pasa de 6,6 periodos con 0,9 a 69 con 0,99. Es el parámetro que decide si la operación cubre costes: una vuelta de 60 días con una brecha del 1 % no paga comisiones ni préstamo |
| `z_t = (x_t − m_t)/s_t` | La desviación medida en desviaciones típicas de una ventana móvil | adimensional | Es la señal. Un umbral de 2 en una serie nerviosa se alcanza constantemente y en una tranquila casi nunca; esa es la razón de estandarizar. Si `s_t` es casi cero, el cociente se dispara y entra una operación por ruido |
| `m_t`, `s_t` | Media y desviación típica de `x` en la ventana que termina en `t` | las de la serie | Cuanto más larga la ventana, más lenta es la referencia y menos señales; cuanto más corta, más veces el z-score supera el umbral. Con 20 días casi todo parece extremo; con 250, una desviación de 2 es un acontecimiento |
| Umbral de entrada | El valor de `z` a partir del cual se abre la posición (±2 habitualmente) | desviaciones típicas | Bajarlo multiplica las operaciones y los costes, y mete operaciones en desviaciones que aún pueden crecer; subirlo deja pocas entradas, pero cada una es más extrema. No lo elijas mirando qué valor daba mejor resultado en tu histórico |
| Stop | El valor de `z` al que se cierra la posición con pérdida (±3,5 habitualmente) | desviaciones típicas | Es el precio de reconocer que la farola se ha mudado. Cuanto más lejos, menos veces salta y más duele cada vez que salta; con reversión a la media, las pérdidas son pequeñas casi siempre y catastróficas cuando el nivel cambia |
:::

De ahí sale la **vida media** de una desviación, que es el tiempo que tarda en reducirse a la
mitad:

:::formula
vida media = −ln(2) / ln(ρ)
:::

Con `ρ = 0,9` el resultado es 6,6 periodos; con `ρ = 0,99`, 69 periodos. La vida media se mide
en las mismas unidades que los datos: si trabajas con días, son días.

La regla de operación usa el z-score de la desviación respecto a una media y una desviación
típica estimadas en una ventana móvil:

:::formula
z_t = (x_t − m_t) / s_t
:::

- `m_t` — media de `x` en la ventana que termina en `t` (por ejemplo, los últimos 60 días).
- `s_t` — desviación típica de `x` en esa misma ventana.
- Regla típica: entrar cuando `z` supera +2 (vendiendo) o baja de −2 (comprando), salir cuando
  `z` vuelve a 0, y cerrar por stop si `z` llega a ±3,5.

El umbral de entrada y la ventana son parámetros, no constantes de la naturaleza. Lo que **no**
es negociable es que `m_t` y `s_t` se calculen solo con datos anteriores a `t`.

:::figura
fichero: reversion-farola-y-paseo
pie: Las dos series de la izquierda bajan en el mismo tramo y las dos están por debajo de su media de 60 días, así que la regla las trata igual. La diferencia es que la azul tiene a donde volver y la roja no: su «media» es solo el sitio por donde pasó hace poco. A la derecha se ve la consecuencia con la misma regla en las dos: en la que revierte el resultado sube hasta +1,42 y se mantiene; en la que pasea acaba en +0,03 y lo poco que gana es la suerte de una racha concreta. Un z-score extremo no es una señal si no hay farola.
fuente: figuras/reversion-a-la-media-1.py
:::

## Ejemplo

Una serie que revierte con `ρ = 0,8978` estimado sobre 3000 observaciones. Aplicando la
fórmula de la vida media: −ln(2) / ln(0,8978) = 0,6931 / 0,1078 = **6,43 periodos**. Cada
periodo corrige el 1 − 0,8978 = **10,2 %** de la desviación.

Eso significa que si la serie está a dos desviaciones típicas de su media y nada más la
empuja, después de 6,43 periodos la mitad de esa desviación habrá desaparecido, y en unos 20
periodos quedará alrededor de un 12 %. Traducido a una operación: entras con `z = −2` en una
serie cuya desviación típica es 0,032 y sales con `z = 0`. El recorrido completo que buscas es
2 · 0,032 = 0,064 en unidades de la serie; capturar la mitad ya es un buen resultado.

Ahora el contraste que importa. Con la misma regla sobre dos series —una que revierte y otra
que pasea— durante 2000 periodos:

```
revierte   pnl +1,1429   operaciones  43   pnl por operación +0,02658
pasea      pnl +0,0870   operaciones  36   pnl por operación +0,00242
```

Las dos series tienen la misma volatilidad de shocks, y la misma regla gana en las dos… pero
no gana lo mismo: en la que revierte el resultado por operación es **once veces** mayor. En la
serie que pasea, lo que se gana no es reversión, es casualidad acumulada: el algoritmo entra
en un movimiento aleatorio y a veces sale bien. Y todo esto es antes de costes.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
n = 3000
rho, sigma = 0.9, 0.01
x = np.zeros(n)
for t in range(1, n):
    x[t] = rho * x[t - 1] + rng.normal(0, sigma)

# Estimacion de x_t = a + rho * x_{t-1} por minimos cuadrados
X = np.column_stack([np.ones(n - 1), x[:-1]])
coef, *_ = np.linalg.lstsq(X, x[1:], rcond=None)
rho_hat = coef[1]
vida_media = -np.log(2) / np.log(rho_hat)

print("rho estimado    %.4f" % rho_hat)
print("vida media      %.2f periodos" % vida_media)
print("mitad en 1 paso %.4f" % (1 - rho_hat))
# -> rho estimado    0.8978
# -> vida media      6.43 periodos
# -> mitad en 1 paso 0.1022
```

:::claves
- `np.column_stack([np.ones(n - 1), x[:-1]])` **desplaza las series para emparejarlas**: `x[:-1]` son los valores de ayer y `x[1:]` los de hoy, así que la regresión explica cada valor por el anterior. Si te equivocas y pasas `x[1:]` como regresor, el modelo se explica a sí mismo y `rho_hat` sale 1,0: el código no avisa, solo da una vida media infinita.
- `coef, *_ = np.linalg.lstsq(X, x[1:], rcond=None)` devuelve la solución en primer lugar, y `rho_hat = coef[1]` toma la **pendiente**, no la ordenada, porque la columna de unos va la primera de la matriz de diseño. El bloque se queda con la pendiente y descarta la constante estimada: esa constante es la media del proceso y, como `x` se generó con media cero, sale cerca de cero, pero no exactamente cero. Por eso `rho_hat` no coincide con el `ρ = 0,9` con el que se generaron los datos.
- `-np.log(2) / np.log(rho_hat)` divide dos números negativos y por eso da positivo. Si `rho_hat` saliera exactamente 1, `np.log(1)` es 0 y Python lanzaría una división entre cero; si saliera mayor que 1 (posible con muestras cortas o con datos no estacionarios), el resultado sería un número negativo que no significa nada. Ninguna de las dos cosas lanza un error por sí sola hasta que divides.
- En `pnl_reversion`, la ventana se escribe `x[t - ventana:t]`, que **excluye** el instante `t`: el z-score se calcula con los 60 días anteriores y se compara con `x[t]`, el precio de hoy. Es exactamente lo que evita mirar al futuro. Cambiar ese corte por `x[t - ventana:t + 1]` metería el dato de hoy en su propia media y el resultado mejoraría de forma artificial.
- `v.std(ddof=1)` divide entre `ventana − 1`: es la desviación típica **muestral**, la que se usa cuando la ventana es una muestra y no la población. NumPy usa `ddof=0` por defecto, así que sin ese argumento todos los z-scores saldrían un poco mayores y la estrategia operaría más.
- El bucle va `for t in range(ventana, len(x) - 1)` y suma `pos * (x[t + 1] - x[t])`: la posición se decide con información hasta `t` y se cobra el movimiento de `t` a `t + 1`. Y ojo con `pnl` y `curva`: `curva[t] = pnl` escribe el acumulado, así que el último elemento de `curva` siempre es cero (el bucle no llega ahí) y **el resultado final es `curva[-2]`**, no `curva[-1]`. Mirar el último valor de la curva da 0,00 y parece que la estrategia no gana nada.
- El coste no aparece en ninguna línea: el `pnl` es bruto. Con 42 operaciones y un recorrido de ida y vuelta que cuesta 0,2 %, la diferencia entre +1,42 bruto y el neto puede ser la mitad del resultado. Añadir el coste es tan sencillo como restar una cantidad fija por cambio de posición (`ops`), pero entonces los números de la página dejan de cuadrar.
:::

La estimación por mínimos cuadrados de `ρ` es la forma más directa de medir la vida media
sin suponer nada. Con `ρ` cerca de 1 la estimación se vuelve inestable, y ahí está el aviso:
si tu `ρ` estimado sale 0,995, la diferencia entre «revierte» y «pasea» cabe dentro del error
típico y no tienes una estrategia, tienes una duda.

```python verificable
import numpy as np

def pnl_reversion(x, ventana=60, entrada=2.0, salida=0.0, stop=3.5):
    """Compra cuando el z-score es muy negativo y vende cuando es muy positivo."""
    pos, pnl, ops = 0, 0.0, 0
    for t in range(ventana, len(x) - 1):
        v = x[t - ventana:t]
        z = (x[t] - v.mean()) / v.std(ddof=1)
        if pos == 0:
            if z > entrada:
                pos, ops = -1, ops + 1
            elif z < -entrada:
                pos, ops = 1, ops + 1
        elif pos == 1 and (z >= salida or z <= -stop):
            pos = 0
        elif pos == -1 and (z <= salida or z >= stop):
            pos = 0
        pnl += pos * (x[t + 1] - x[t])
    return pnl, ops

rng = np.random.default_rng(0)
n = 2000
rev = np.zeros(n)                       # serie que revierte: AR(1) con rho 0,95
for t in range(1, n):
    rev[t] = 0.95 * rev[t - 1] + rng.normal(0, 0.01)
paseo = np.cumsum(rng.normal(0, 0.01, n))   # serie que pasea: sin nivel al que volver

for nombre, serie in (("revierte", rev), ("pasea", paseo)):
    p, ops = pnl_reversion(serie)
    print("%-8s pnl %+7.4f  operaciones %3d  pnl/operacion %+.5f" % (nombre, p, ops, p / max(ops, 1)))
# -> revierte pnl +1.1429  operaciones  43  pnl/operacion +0.02658
# -> pasea    pnl +0.0870  operaciones  36  pnl/operacion +0.00242
```

El `z` se calcula con la ventana que termina en `t`, así que no hay nada de futuro en la
decisión; los resultados son antes de costes, y con 43 operaciones el error típico del
resultado por operación es lo bastante grande como para no sacar conclusiones fuertes.

## Errores típicos

- **Confundir un precio que baja con un precio barato.** Un precio que cae un 40 % no tiene
  ninguna obligación de volver. Si no puedes nombrar la referencia a la que debería volver,
  no hay reversión: hay una tendencia que estás intentando adivinar.
- **Estimar la media y la desviación con toda la muestra.** Si `m` y `s` se calculan con el
  futuro, el z-score es impecable y la estrategia es inoperable. Usa ventanas móviles y, si
  usas la primera parte de la muestra para fijar los parámetros, no la vuelvas a usar para
  medir el resultado.
- **Promediar a la baja sin stop.** La reversión a la media tiene pérdidas acotadas la mayoría
  de las veces y catastróficas cuando el nivel cambia. El stop no es una falta de fe en la
  estrategia: es el reconocimiento de que a veces la farola se muda.
- **Suponer que `ρ` es constante.** Una vida media de 6 días en un mercado tranquilo puede
  convertirse en 60 en una crisis, justo cuando tienes la posición abierta. Mide `ρ` en
  ventanas y compara.
- **Operar reversión en series con raíz unitaria.** Antes de construir la estrategia, contrasta
  la estacionariedad. Si la serie es un paseo aleatorio, cualquier reversión que veas en la
  muestra es un artefacto de la muestra.
- **Olvidar los costes.** Una reversión del 0,3 % con un recorrido de ida y vuelta que cuesta
  0,2 % no es una estrategia, es una donación al bróker. Cuanto más corta es la vida media,
  más operaciones y más coste: la reversión rápida es la que peor soporta las comisiones.

:::trampa
El error más caro de esta familia es elegir la ventana y el umbral mirando qué combinación
daba mejor resultado en tu histórico. Con 20 ventanas y 10 umbrales tienes 200 estrategias
probadas, y la mejor de 200 siempre parece buena. Es
[[data-snooping-y-multiple-testing|data snooping]] con otro nombre.
:::

:::practica
enunciado: El diferencial de un par vale hoy 0,048; la media de 60 días es 0 y la desviación típica, 0,016. La regla entra en z = ±2, sale en 0 y cierra en ±3,5, y operar cuesta 0,020 de ida y vuelta. ¿Qué haces y cuánto esperas ganar?
pista: El z-score es la desviación respecto a la media dividida entre la desviación típica, y el recorrido que buscas es la vuelta a cero.
solucion: z = 0,048 / 0,016 = 3,0. Supera el umbral de 2 y no llega al stop de 3,5, así que vendes el diferencial. Si vuelve a la media capturas 0,048; descontando el coste de 0,020 quedan 0,028 netos, el 58 % del bruto. Con ρ = 0,9 la vida media es −ln(2) / ln(0,9) = 6,6 periodos: la posición dura semanas y el retraso se lo come el coste de préstamo.
:::

## Comprueba que lo sabes

:::quiz
p: Una serie tiene un ρ estimado de 0,99 en datos diarios. ¿Qué implica?
o: Que la serie revierte muy rápido y hay que operar intradía
o: Que la vida media de una desviación es de unos 69 días y que la estimación es tan frágil que podría ser un paseo aleatorio
o: Que la serie es estacionaria y se puede usar la media de toda la muestra sin problema
a: 2
e: La vida media es −ln(2) / ln(0,99) = 69 días, es decir, una corrección del 1 % diario: lentísima. Y un ρ de 0,99 está tan cerca de 1 que el intervalo de confianza suele incluir el 1, así que no puedes descartar que sea un paseo aleatorio. Reversión lenta y estacionariedad dudosa van juntas.
:::

:::quiz
p: ¿Por qué la misma regla de reversión gana once veces más por operación en la serie que revierte que en la que pasea?
o: Porque en la que pasea la regla entra menos veces y tiene menos muestra
o: Porque en la que revierte existe un nivel al que la desviación vuelve, y en la que pasea el movimiento es acumulativo y no tiene por qué corregirse
o: Porque la serie que pasea tiene menos volatilidad y por eso el z-score falla
a: 2
e: En la serie que revierte, la desviación se corrige y la posición captura esa corrección. En la que pasea, los incrementos son independientes: la desviación que detectas no es un desvío respecto a nada, es el nivel actual, y no hay motivo para que vuelva. Las dos series del ejemplo tienen la misma volatilidad de shocks, así que la tercera opción no explica nada.
:::

:::aviso
La reversión a la media y [[momentum|el momentum]] no son teorías rivales: operan en
horizontes distintos. La reversión domina en días o semanas; el momentum, en meses. Si tu
señal mezcla los dos sin separar los horizontes, las dos partes se cancelan y te quedas con
el giro, que es lo único que sí pagas seguro.
:::
