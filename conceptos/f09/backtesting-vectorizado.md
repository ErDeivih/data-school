---
id: backtesting-vectorizado
titulo: Backtesting vectorizado
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [vectorizacion, retornos-logaritmicos, sesgo-de-mirar-al-futuro]
tags: [backtest, vectorizacion, numpy, rendimiento]
resumen: Calcular la posición y el resultado de toda la serie de golpe con arrays: rapidísimo para explorar ideas y muy fácil de contaminar sin que salte ningún error.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 8", "McKinney (2022), 'Python for Data Analysis'"]
---

## En una frase

El backtesting vectorizado convierte la regla de trading en operaciones sobre arrays —señal,
posición, desplazamiento, rendimiento— y calcula la serie entera de una vez, en lugar de
recorrer barra a barra; es mil veces más rápido para explorar y no avisa cuando la has liado.

## La idea

Un backtest por eventos es un reloj: en cada instante pasa algo, el mercado publica un precio, la
estrategia decide, el bróker confirma, la posición cambia. Un backtest vectorizado es una
calculadora de nóminas: tienes una columna con lo que se cobra y otra con el IRPF, las restas de
golpe y ya está. Nada de relojes.

La traducción de la idea a tres columnas es siempre la misma:

1. **Señal:** un número por barra que dice lo que *quieres* hacer. Por ejemplo, `+1` si el cierre
   de ayer superó su media de 20 días, `0` si no.
2. **Posición:** la señal convertida en exposición, desplazada una barra. Si la señal se calcula
   con el cierre de hoy, la posición solo puede estar viva **a partir de mañana**. Ese
   desplazamiento es la frontera entre un backtest y una fantasía.
3. **Rendimiento:** la posición multiplicada por el retorno de la barra, más los costes de la
   rotación.

La ventaja es enorme y no es solo de velocidad: como todo es un array, puedes añadir una
dimensión con el parámetro de la media móvil y obtener 200 variantes de la estrategia en la misma
operación. Eso es exactamente lo que hace [[vectorbt-backtrader-zipline|VectorBT]], y es lo que
convierte al backtesting vectorizado en la herramienta natural para la fase de exploración.

El problema es simétrico y más peligroso: **no hay ningún punto del proceso en el que el código
se queje**. Un bucle que intenta leer una fila que no existe lanza un `IndexError` y te enteras.
Un array desplazado al revés, un `NaN` en la primera posición o un retorno calculado con el
mismo precio que la señal producen un resultado perfectamente plausible, con una curva suave y un
Sharpe estupendo. En un backtest vectorizado, los errores no se ven en los logs: se ven en el
bróker, meses después.

:::figura
fichero: backtesting-vectorizado-cuatro-curvas
pie: Arriba, la señal y la posición que de verdad se mantiene: el array no distingue una de otra y no avisa de nada. Abajo, el capital final de la misma regla sobre el mismo precio según la línea que se cambie: sin desplazar la señal el resultado se dispara, y sin costes o sumando en vez de componer también se desvía, cada una en su dirección.
fuente: figuras/backtesting-vectorizado-1.py
:::

## Definición formal

Sea `r_t` el retorno de la barra `t` (por ejemplo, el retorno simple `P_t / P_{t-1} − 1`) y
`g` la regla que convierte la información disponible al final de `t` en una posición objetivo:

:::formula
s_t = g(I_t)            pos_t = s_{t-1}            pnl_t = pos_t · r_t − c · /pos_t − pos_{t-1}/
:::

- `I_t` — información disponible al terminar la barra `t`: precios hasta `t`, indicadores
  calculados con datos hasta `t`. Nunca incluye `t+1`.
- `s_t` — señal calculada al final de `t`. Es una decisión, no una posición todavía.
- `pos_t` — posición **mantenida durante** la barra `t`. Por eso vale `s_{t-1}`: es el
  desplazamiento de una barra (`shift(1)`), la línea que separa un backtest honesto de uno que
  mira al futuro.
- `r_t` — retorno de la barra `t`, el que se cobra.
- `c` — coste por unidad de rotación, en tanto por uno: comisión más deslizamiento
  ([[slippage-y-comisiones]]).
- `/pos_t − pos_{t-1}/` — rotación: cuánto cambia la posición de una barra a la siguiente, en
  valor absoluto. Es lo que se paga aunque la estrategia no gane nada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `s_t` | Señal calculada al final de la barra `t`: una decisión, todavía no una posición | exposición objetivo (0 a 1) | No es la posición que cobra: si la usas directamente como `pos_t`, estás cobrando el retorno con la información que lo generó |
| `pos_t` | Posición mantenida **durante** la barra `t` | fracción del capital | Vale `s_{t-1}`. Un desplazamiento de una barra es la diferencia entre un backtest y una fantasía: aquí es donde más se destruye el resultado al arreglarlo |
| `r_t` | Retorno de la barra `t`, el que se cobra | tanto por uno | Es el único término que puede hacer perder dinero. Con retornos grandes, `pnl_t` deja de ser pequeño y la aproximación por suma se rompe |
| `c` | Coste por unidad de rotación: comisión más deslizamiento | tanto por uno de lo operado | Con `c` mayor el resultado neto baja proporcionalmente a la rotación. La estrategia que más rota es la que antes se vuelve inviable |
| `abs(pos_t − pos_{t-1})` | Rotación entre dos barras consecutivas | unidades de posición | Se paga al entrar y al salir: una ida y vuelta cuesta dos unidades, no una. Con rotación diaria y `0,10 %` por cambio son más de un 25 % anual |
| `C_0` | Capital inicial | unidades monetarias | Es una escala, no un parámetro del modelo: multiplica toda la curva y no cambia ninguna métrica relativa |
:::

La curva de capital se obtiene componiendo, no sumando, cuando los pesos son fraccionarios:

:::formula
C_t = C_0 · Π (1 + pnl_s)        frente a        C_t ≈ C_0 · (1 + Σ pnl_s)
:::

La suma de retornos y el producto solo coinciden cuando los `pnl` son pequeños (menos del 1 %).
Con variaciones diarias de dos cifras, la diferencia entre las dos curvas es material: sumar
sobreestima la capitalización final.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `pnl_s` | Resultado de la barra `s`: posición por retorno menos coste | tanto por uno | Con `pnl_s` pequeños (menos del 1 %) componer y sumar dan casi lo mismo. A partir de ahí el producto se separa y la suma se queda corta |
| `Π (1 + pnl_s)` | Capitalización: el capital se multiplica barra a barra | factor acumulado | Es la curva correcta cuando los pesos son fraccionarios. Cada barra opera sobre el capital que quedaba, no sobre el inicial |
| `Σ pnl_s` | Suma aritmética de los resultados | tanto por uno | Sobreestima el capital final. El error crece con la volatilidad y con el número de barras, y siempre en la misma dirección |
:::

## Ejemplo

Siete cierres diarios: `100,0  102,0  101,0  105,0  103,0  106,0  108,0`. Los seis retornos son
`+2,00 %`, `−0,98 %`, `+3,96 %`, `−1,90 %`, `+2,91 %` y `+1,89 %`.

La regla es «estar comprado si el retorno de ayer fue positivo». Aplicada a las seis barras, la
posición de cada barra es `1` si el retorno anterior fue positivo y `0` si fue negativo:

```
posicion:      0    1    0    1    0    1
retorno:   +2,00  -0,98  +3,96  -1,90  +2,91  +1,89   (%)
pnl:         0   -0,98    0    -1,90    0    +1,89   (%)
```

- Total honesto: `−1,00 %` (si sumas los tres retornos ya redondeados a dos decimales te sale
  `−0,99 %`; la diferencia es el redondeo, y por eso conviene calcular con la serie completa).
- La misma regla **sin desplazar** (aplicada al retorno de su propia barra):
  `+2,00 + 3,96 + 2,91 + 1,89 = +10,76 %`. La única diferencia es en qué barra se aplica la
  señal, y el resultado pasa de perder un uno por ciento a ganar casi un once. Eso es
  [[sesgo-de-mirar-al-futuro]] en estado puro.
- Con costes de `0,10 %` por unidad de rotación: la posición recorre `0→1→0→1→0→1`, cinco
  unidades de rotación, `0,50 %` de coste. El resultado neto se queda en `−1,50 %`.

Un detalle que arruina más backtests de los que parece: el `shift(1)` deja un `NaN` en la
primera posición. Si lo dejas y acumulas con `cumsum`, el `NaN` se propaga a **toda** la serie y
la curva de capital sale vacía. Si lo rellenas «hacia atrás» (`bfill`) para que no moleste, has
metido el futuro en el pasado. Se rellena con cero: el primer día no estabas en el mercado.

## Código

```python verificable
import numpy as np

precios = np.array([100.0, 102.0, 101.0, 105.0, 103.0, 106.0, 108.0])
ret = np.diff(precios) / precios[:-1]

# Version tramposa: la senal de la barra t cobra el retorno de la barra t.
trampa = (ret > 0) * ret

# Version honesta: la posicion de hoy la decide el retorno de ayer (shift de una barra).
posicion = np.concatenate([[0.0], (ret[:-1] > 0).astype(float)])
honesto = posicion * ret

rotacion = np.abs(np.diff(posicion)).sum()
coste = rotacion * 0.001

print(f"retornos          {np.round(ret * 100, 2).tolist()}")
# -> [2.0, -0.98, 3.96, -1.9, 2.91, 1.89]
print(f"sin desplazar     {trampa.sum():+.2%}")     # -> +10.76%
print(f"desplazado        {honesto.sum():+.2%}")    # -> -1.00%
print(f"rotacion          {rotacion:.0f}  coste {coste:.2%}")  # -> rotacion 5  coste 0.50%
print(f"neto de costes    {honesto.sum() - coste:+.2%}")       # -> -1.50%
```

:::claves
- `np.diff(precios)` devuelve 6 diferencias con 7 precios, y `precios[:-1]` tiene 6 elementos: por
  eso `ret` tiene 6 y no 7. Todo el resto del bloque trabaja con 6 barras, así que `posicion` tiene
  que tener 6 también, y de ahí el `np.concatenate([[0.0], ...])`: el primer día no había posición.
- `(ret > 0)` es un array de **booleanos**; `* ret` lo convierte a 0/1 al vuelo. No hay `.astype`
  ni error, pero si `ret` llevara un `NaN` la comparación da `False` y ese día se trata como «no
  comprado»: el `NaN` desaparece sin que nadie lo mencione.
- `np.abs(np.diff(posicion)).sum()` calcula la rotación total. `np.diff` acorta el array una
  posición, así que este cálculo **no ve el cambio desde la posición inicial**: si empezaras con
  posición 1 en la primera barra, esa entrada no se cobraría. Se arregla con `prepend=0.0`, que es
  lo que hace la figura de este concepto.
- `honesto.sum()` suma retornos; `np.cumprod(1 + honesto)` capitaliza. El bloque imprime la suma
  porque el ejemplo la usa para hablar del neto, pero esa cifra **no es** el capital final: con
  seis barras y variaciones de varios puntos la diferencia ya se nota.
- `f"{coste:.2%}"` multiplica por 100 y añade el signo de porcentaje: `0.005` se imprime `0,50 %`.
  `np.round(ret * 100, 2)` hace lo mismo a mano pero redondeando antes, así que los dos números que
  ves en pantalla pueden discrepar en la última cifra.
- Cambiar `posicion` por `senal` en la línea de `honesto` es todo lo que hace falta para pasar de
  −1,00 % a +10,76 %: la trampa no necesita ninguna línea nueva, solo quitar el desplazamiento.
:::

```python verificable
import numpy as np

# El NaN del shift no da error: envenena la serie entera y la curva sale vacia.
# Aqui la posicion es larga-corta (+1 / -1), asi que la rotacion es el doble que en 0/1.
ret = np.array([0.02, -0.0098, 0.0396, -0.019, 0.0291, 0.0189])
posicion = np.array([np.nan, 1.0, -1.0, 1.0, -1.0, 1.0])

print("con NaN    ", np.round(np.cumsum(posicion * ret), 4).tolist())
# -> [nan, nan, nan, nan, nan, nan]

limpia = np.nan_to_num(posicion)      # NaN -> 0: el primer dia no estabas dentro
bruto = float((limpia * ret).sum())
rotacion = float(np.abs(np.diff(limpia)).sum())
coste = rotacion * 0.001

print(f"bruto      {bruto:+.2%}")                       # -> -7.86%
print(f"rotacion   {rotacion:.0f}  coste {coste:.2%}")  # -> rotacion 9  coste 0.90%
print(f"neto       {bruto - coste:+.2%}")               # -> -8.76%
```

## Errores típicos

- **No desplazar la señal.** Es el error número uno y el más caro: la señal calculada con el
  cierre de `t` solo puede operar en `t+1`. Si el resultado de tu versión sin desplazar es
  muchísimo mejor que la desplazada, no has encontrado una estrategia: has encontrado el
  [[sesgo-de-mirar-al-futuro]].
- **Dejar el `NaN` del `shift` o rellenarlo hacia atrás.** Un `NaN` en un `cumsum` o un
  `cumprod` contamina toda la serie y la curva aparece vacía; un `bfill` copia el futuro sobre el
  pasado. Rellena con cero, que es la verdad: antes de la primera señal no tenías posición.
- **Sumar retornos donde hay que componer.** `(1 + pnl).prod()` y `1 + pnl.sum()` solo coinciden
  con variaciones diminutas. Con posiciones que cambian y retornos de varios puntos, la suma se
  desvía y siempre hacia arriba.
- **Comparar la posición objetivo con la posición real.** Vectorizar te deja el peso objetivo
  por barra, pero entre rebalanceos el peso **deriva** con los precios: si sube un activo, pesa
  más. Ignorar esa deriva es suponer un rebalanceo continuo y gratuito que no existe.
- **Olvidar costes y rotación.** El vectorizado hace tan fácil calcular la estrategia que se
  olvida lo que cuesta ejecutarla. Un sistema con rotación diaria y `0,10 %` por cambio paga más
  de un 25 % anual en costes: sin esa línea, cualquier idea parece viable.
- **Explorar 500 variantes y quedarte con la mejor.** El vectorizado está pensado para barrer
  parámetros, y ahí es donde entra el [[data-snooping-y-multiple-testing|data snooping]]: si el
  barrido se hace sobre todos tus datos, el mejor resultado es el máximo de 500 ruidos.

:::practica
enunciado: Con los cierres 100; 104; 102; 108; 105; 110; 107 aplica la regla «posición 1 durante la barra siguiente si el retorno de la anterior fue positivo, 0 si fue negativo», con la primera barra sin posición. Calcula el bruto, la rotación, el coste con 0,05 % por unidad y el neto.
pista: La posición de cada barra es el signo del retorno anterior; el coste se paga por cada cambio de posición, en valor absoluto.
solucion: Retornos: +4,00; −1,92; +5,88; −2,78; +4,76; −2,73 (%). Posiciones: 0, 1, 0, 1, 0, 1. Bruto = −1,92 − 2,78 − 2,73 = −7,43 %. Rotación = 1 + 1 + 1 + 1 + 1 = 5 unidades y coste 5 · 0,05 % = 0,25 %, así que el neto es −7,68 %. Comprar y mantener habría dado +7,00 %: el filtro compra siempre tarde.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la señal se desplaza una barra antes de convertirla en posición?
o: Porque el retorno de la barra t se cobra con una posición que solo puede decidirse con información disponible al final de t−1
o: Porque si no, el array tiene una longitud distinta y NumPy da error
o: Porque así se pagan menos comisiones al reducir la rotación
a: 1
e: La posición que mantienes durante la barra t se decide antes de que esa barra ocurra. Sin el desplazamiento estás comprando con el cierre que genera la señal y cobrando ese mismo movimiento: el backtest gana en casi todas las barras, que es la firma del sesgo de mirar al futuro. Los arrays se pueden recortar de muchas formas y las comisiones dependen del número de cambios de posición, no del desplazamiento.
:::

:::quiz
p: Tu curva de capital vectorizada sale entera a `NaN` después de la primera barra. ¿Qué ha pasado?
o: El `shift(1)` dejó un `NaN` en la primera posición y el acumulado lo arrastra hacia delante
o: Los precios tienen un valor nulo en el fichero original
o: El producto de retornos necesita números enteros
a: 1
e: `cumsum` y `cumprod` propagan el `NaN` a todas las posiciones siguientes, así que un solo valor ausente al principio deja la serie vacía. Se arregla rellenando esa posición con cero, que es la posición real antes de la primera señal. Rellenar hacia atrás copiaría el futuro y rellenar con la media es una invención.
:::

:::quiz
p: Estrategia con posición en `{0, 1}` que cambia de estado 9 veces en una serie de 6 barras y coste de 0,10 % por unidad de rotación. ¿Cuánto se lleva el coste?
o: 0,90 %, porque cada cambio de 0 a 1 o de 1 a 0 cuesta 0,10 % y hay nueve unidades de rotación
o: 0,10 %, porque el coste se paga una vez por operación abierta
o: Nada, porque el coste solo se aplica a las barras en las que estás dentro
a: 1
e: La rotación se mide como la suma de los valores absolutos de los cambios de posición, y aquí suman 9: se paga por entrar y por salir, y una ida y vuelta de `0→1→0` son dos unidades. Multiplicar por 0,10 % da 0,90 %. El coste no depende de si la operación gana o pierde: se paga igual.
:::

:::truco
Antes de mirar la rentabilidad de cualquier backtest vectorizado, imprime tres cosas: la longitud
de la serie, cuántos `NaN` quedan y la rotación total. Un backtest con muchos `NaN`, o con una
rotación anual superior a 30 veces el capital, está mal montado o es inviable por costes. Los dos
números se calculan en una línea y ahorran semanas.
:::
