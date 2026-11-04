---
id: sesgo-de-mirar-al-futuro
titulo: Sesgo de mirar al futuro
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [fuga-de-datos, validacion-temporal, train-val-test]
tags: [fuga-de-datos, backtest, validacion, sesgo]
resumen: Usar en la decisión de hoy información que solo existía después: el error que convierte cualquier backtest en una máquina de imprimir dinero.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 7"]
---

## En una frase

Hay sesgo de mirar al futuro cuando una decisión del backtest usa información que en ese momento
todavía no existía: la posición que tomas el martes no puede depender del cierre del miércoles, ni
de la media de todo el año, ni del dato macro que se publicó dos meses después.

## La idea

En un backtest todo ocurre a la vez, porque el ordenador tiene el fichero entero delante. Eso, que
es la mayor comodidad del mundo, es también la fuente de casi todos los resultados demasiado
buenos. En la realidad, el martes por la mañana solo sabes lo que había pasado hasta el lunes por
la tarde. Nada más.

La trampa más famosa es la de ejecución: construyes una señal con el cierre de hoy y luego calculas
el beneficio de hoy. Si tu señal dice «hoy ha subido, así que hoy estoy comprado», acabas cobrando
todas las subidas y evitando todas las bajadas, y el backtest se dispara. En la vida real, cuando
tienes el cierre de hoy ya no puedes operar a ese precio: operas mañana, al precio de mañana. Ese
desplazamiento de una sola barra vale, en el ejemplo de abajo, más de quince puntos porcentuales de
diferencia.

:::figura
fichero: sesgo-de-mirar-al-futuro-una-barra
pie: Las tres curvas salen del mismo precio y de la misma regla; lo único que cambia es en qué barra se cobra la posición. La versión que decide y cobra en la misma barra sube sin una sola barra perdedora, y ésa es precisamente la señal de alarma: ninguna estrategia real gana en todas.
fuente: figuras/sesgo-de-mirar-al-futuro-1.py
:::

Pero el sesgo no solo vive en la ejecución. Se cuela en el preprocesado, que es donde menos se
mira:

- **Estandarizar con la media y la desviación de toda la muestra.** La primera observación queda
  expresada en unidades que dependen de datos de dentro de tres años.
- **Imputar nulos con la mediana global**, o rellenar hacia atrás los huecos con el valor
  siguiente.
- **Seleccionar variables mirando la correlación con el objetivo en todo el histórico**, o hacer
  un análisis de componentes principales sobre el conjunto completo.
- **Codificar variables categóricas con la media del objetivo** (target encoding) calculada con
  todas las filas.
- **Decidir qué activos entran en el universo** usando la capitalización o la liquidez actuales: es
  el [[sesgo-de-supervivencia|sesgo de supervivencia]], un primo hermano de este.

Y hay una familia de casos con datos reales que no tiene nada que ver con el código: los datos
**revisados**. Muchas series macroeconómicas se publican con una primera estimación y se revisan
varias veces durante meses y años. Si usas la serie final, estás usando la versión corregida con
información posterior a la publicación, que en el momento de decidir no existía. Lo mismo con los
resultados trimestrales: la fecha que importa es la de publicación, no la del cierre del
trimestre.

Como se detecta, en orden de eficacia:

1. **Desplaza todo una barra más hacia el pasado y vuelve a medir.** Si el rendimiento se hunde, tu
   ventaja era el sesgo. Es la prueba más rápida y la que más veces da la respuesta.
2. **Dibuja el rendimiento por año del backtest y compáralo con el de un experimento honesto.** Los
   sesgos de futuro son especialmente generosos en los periodos de crisis, cuando la volatilidad es
   alta y una señal que «ya sabe» el resultado acierta mucho.
3. **Pregunta por cada variable: ¿este número estaba disponible el día que decido?** Con nombre,
   fecha y hora. Si la respuesta es «creo que sí», probablemente no.

Dos cosas que conviene separar con claridad, porque se confunden constantemente: **la etiqueta sí
mira al futuro** (por definición: es lo que quieres predecir) y **las variables nunca**. Mezclar
los dos papeles es el origen del [[fuga-de-datos|fuga de datos]] clásica en problemas de
clasificación.

:::trampa
Un backtest con Sharpe por encima de 3 en datos diarios casi nunca es un hallazgo: es un sesgo de
futuro, o costes que no has puesto, o un universo elegido a toro pasado. Antes de celebrarlo, busca
el error. Y si no lo encuentras, busca otra vez.
:::

## Definición formal

Sea `I_t` el conjunto de información disponible al terminar la barra `t`: precios y volúmenes
hasta `t`, más cualquier dato externo **publicado** hasta ese momento. Una regla de decisión es
válida si la posición de la barra siguiente depende solo de `I_t`:

:::formula
posicion_{t+1} = g(I_t)        y_t = f(precios de t+1 a t+h)
:::

- `I_t` — la información disponible en `t`. Incluye el cierre de `t`, pero no el de `t+1`.
- `g` — la regla que convierte información en posición: una media móvil, un modelo, un umbral.
- `posicion_{t+1}` — la exposición que se mantiene durante `t+1`, que es la que captura el retorno
  de `t+1`.
- `y_t` — la etiqueta, que por construcción usa `t+1 … t+h`. Es lo único de todo el proceso que
  tiene permiso para mirar al futuro, porque es el objetivo del aprendizaje.
- `h` — horizonte de predicción, en barras.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `I_t` | Información disponible al terminar la barra `t`: precios y volúmenes hasta `t` y datos publicados hasta `t` | conjunto de datos con fecha y hora | Si metes dentro cualquier dato posterior a `t`, deja de ser información y el backtest entero deja de valer |
| `g` | La regla que convierte información en posición: una media, un umbral, un modelo | función de `I_t` a exposición | Cuanto más estadístico use `g` calculado sobre toda la muestra, más global es la contaminación: pasa de una barra a todas |
| `posicion_{t+1}` | Exposición que se mantiene **durante** `t+1` | fracción del capital (0 a 1) | Es la que captura el retorno de `t+1`. Si la decides con información de `t+1` en vez de `t`, ganas todas las barras y el resultado es ficción |
| `y_t` | La etiqueta que quieres predecir, calculada de `t+1` a `t+h` | retorno o clase | Es lo único que tiene permiso para mirar al futuro: subir `h` la aleja más, y no contamina nada |
| `h` | Horizonte de predicción | barras | Con `h` mayor la etiqueta se solapa más consigo misma en el tiempo, y hay que purgar la validación por eso, no por fuga de variables |
| `t` | La barra en la que se decide | índice temporal | Desplazar todo una barra hacia el pasado es la prueba más rápida: si el resultado se hunde, la ventaja era el sesgo |
:::

La versión contaminada es la que usa el mismo instante en los dos lados: `posicion_t = g(I_t)` y
luego se cobra el retorno de `t`, que ya forma parte de `I_t`. En cuanto `g` contiene una media,
un umbral o cualquier estadístico calculado sobre toda la muestra, la contaminación deja de ser de
una barra y pasa a ser global.

## Ejemplo

Cinco cierres: `100,0`, `102,0`, `101,0`, `105,0`, `103,0`. Los retornos diarios son `+2,00 %`,
`−0,98 %`, `+3,96 %` y `−1,90 %`.

- **Estrategia tramposa:** estar comprado si el retorno de hoy es positivo («el signo de hoy»), y
  cobrar el retorno de hoy. El resultado es la suma de los valores absolutos:
  `2,00 + 0,98 + 3,96 + 1,90 = +8,85 %`. Ni una pérdida.
- **Estrategia honesta:** la posición de hoy la decide el retorno de ayer, y se cobra el retorno de
  hoy. Resultado: `−0,98 % − 3,96 % − 1,90 % = −6,85 %`. La señal «compra cuando ayer subió» se
  come las tres caídas.
- **Comprar y mantener:** `103,0 / 100,0 − 1 = +3,00 %`.

La trampa no está en la regla, está en cuándo se aplica. Y fíjate en el detalle que la delata: la
versión tramposa gana en **todas** las barras. Ninguna estrategia real gana siempre.

El mismo problema aparece en la gestión del riesgo. Si dimensionas la posición con la volatilidad
de **toda** la muestra, el tamaño que pones el décimo día ya sabe que en el día 120 llega una
crisis. Con una serie de 120 días tranquilos y 40 de pánico, el tamaño calculado con la volatilidad
total es 7,6 veces el objetivo, mientras que el calculado solo con el pasado hasta ese día es 25,6:
una diferencia de más del triple, y en 134 de los 160 días el tamaño difiere en más de un 20 %. La
versión con la volatilidad total **parece** más prudente al principio, pero lo es por haber visto
el futuro.

## Código

```python verificable
import numpy as np

precios = np.array([100.0, 102.0, 101.0, 105.0, 103.0])
ret = np.diff(precios) / precios[:-1]

pnl_trampa = np.sign(ret) * ret            # la senal de hoy opera el retorno de hoy
pnl_honesto = np.sign(ret[:-1]) * ret[1:]  # la senal de ayer opera el retorno de hoy

print("retornos:", np.round(ret * 100, 2).tolist())         # -> [2.0, -0.98, 3.96, -1.9]
print(f"acumulado con la trampa: {pnl_trampa.sum():+.2%}")  # -> +8.85%
print(f"acumulado honesto      : {pnl_honesto.sum():+.2%}") # -> -6.85%
print(f"comprar y mantener     : {precios[-1] / precios[0] - 1:+.2%}")   # -> +3.00%
```

:::claves
- `np.diff(precios)` devuelve un array **más corto**: con 5 precios da 4 diferencias. Por eso
  `precios[:-1]` tiene 4 elementos y la división encaja; si divides entre `precios` a secas, NumPy
  no puede emitir y lanza un error de formas.
- `np.sign(ret)` devuelve `-1,0`, `0,0` o `1,0` (float, no entero) y `np.sign(0)` es 0, no 1: en un
  retorno exactamente cero la posición se queda plana.
- `np.sign(ret) * ret` **no es la estrategia**: es el valor absoluto de cada retorno. La señal y el
  retorno son la misma cifra, así que el producto no puede salir negativo nunca. Ese «nunca» es la
  firma que buscamos: una estrategia real pierde barras.
- `np.sign(ret[:-1]) * ret[1:]` recorta los dos arrays para que casen: la señal viene de la barra
  anterior y el retorno se cobra en la siguiente. Si te equivocas de recorte y usas `ret[:-1]` otra
  vez, vuelves a la versión tramposa sin que nada avise.
- `pnl_trampa.sum()` suma retornos simples, y eso solo vale como aproximación para variaciones
  diminutas. Con cuatro barras es una ilustración, no una curva de capital: para capitalizar de
  verdad hay que componer con `np.cumprod(1 + ret)`.
- Los formatos `{:+.2%}` y `{:.2f}` no redondean igual: `+.2%` escribe el porcentaje con dos
  decimales y signo. `np.round(ret * 100, 2)` redondea a mano antes, así que los dos números que
  ves pueden diferir en la última cifra.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
ret = np.concatenate([rng.normal(0.0002, 0.005, size=120),   # 120 dias tranquilos
                      rng.normal(-0.0020, 0.025, size=40)])  # 40 dias de panico
objetivo = 0.10        # volatilidad objetivo, en tanto por uno

# Dimensionar con la volatilidad de toda la serie usa datos que en ese dia no existian.
vol_total = ret.std(ddof=1)
vol_pasado = np.array([ret[:t].std(ddof=1) if t >= 5 else np.nan
                       for t in range(ret.size)])

for t in (10, 150):
    print(f"t={t:>3}  tamano con vol total {objetivo / vol_total:.1f}  "
          f"con vol solo-pasado {objetivo / vol_pasado[t]:.1f}")
# en t=10 la vol total pide 7.6 y la informacion disponible pedia 25.6

diferencia = np.abs(objetivo / vol_total - objetivo / vol_pasado) / (objetivo / vol_pasado)
print(f"dias con tamano distinto mas del 20 %: {int((diferencia > 0.20).sum())} de {ret.size}")
# -> 134 de 160
```

## Errores típicos

- **Estandarizar, imputar o seleccionar variables con toda la muestra.** Cualquier transformación
  que aprenda parámetros (media, desviación, mediana, componentes, umbrales) se ajusta **solo con
  el entrenamiento** y se aplica después. Es exactamente lo que evita
  [[pipelines-de-ml|un pipeline bien construido]].
- **Operar al cierre de la barra que genera la señal.** Si la señal usa el cierre de hoy, la
  operación es de mañana. Ese desplazamiento hay que escribirlo en el código, no darlo por
  supuesto, y hay que comprobar en qué barra se aplica el retorno.
- **Rellenar los huecos con el valor siguiente.** «Rellenar hacia atrás» consiste literalmente en
  copiar el futuro sobre el pasado. Hacia delante (arrastrar el último valor conocido) es lo único
  defendible cuando el dato se publica con retraso.
- **Usar datos revisados como si fueran los originales.** Las series macro y los fundamentales se
  corrigen con el tiempo. Sin datos point-in-time (la foto exacta que se publicó cada día), el
  backtest está usando información que no existía.
- **Confundir el papel de la etiqueta con el de las variables.** Que `y` mire al futuro es el
  objetivo del problema; que una variable de entrada mire al futuro es el error. Si tu «variable»
  más predictiva es el retorno del mismo periodo que quieres predecir, no has encontrado nada.
- **Elegir el universo con criterios de hoy.** Incluir solo las empresas que siguen cotizando, o
  solo los fondos que existen ahora, selecciona a los ganadores después de saber quiénes ganaron.
  El universo se construye con lo que existía en cada fecha.

:::practica
enunciado: Con los cierres 200; 204; 202; 196; 200; 212, calcula el acumulado de una regla que toma +1 si el retorno previo fue positivo y −1 si fue negativo, en dos versiones: la que cobra el retorno de la misma barra que genera la señal y la que cobra el de la barra siguiente. Compara con comprar y mantener.
pista: La posición que aguanta la barra t solo puede decidirse con información de t−1; la versión tramposa usa el retorno de la propia barra.
solucion: Los retornos son +2,00; −0,98; −2,97; +2,04 y +6,00 (%). La versión tramposa cobra el valor absoluto de cada uno: 2,00 + 0,98 + 2,97 + 2,04 + 6,00 = +13,99 %. La honesta desplaza la señal: −0,98 + 2,97 − 2,04 + 6,00 = +5,95 %. Comprar y mantener da 212/200 − 1 = +6,00 %. Una sola barra de diferencia casi triplica el resultado.
:::

## Comprueba que lo sabes

:::quiz
p: Una regla dice «si el retorno de hoy es positivo, mantente comprado». ¿Dónde está el error si se aplica al retorno de hoy?
o: En que el signo del retorno de hoy no predice nada
o: Porque el cierre de hoy forma parte de la información que se usa para decidir, así que no se puede cobrar el retorno de la misma barra
o: En que habría que usar máximos y mínimos en lugar de cierres
a: 2
e: La posición que puedes mantener durante la barra t se decide con información disponible al final de t−1. Aplicar la señal de hoy al retorno de hoy equivale a comprar sabiendo el resultado, y por eso esa versión gana en todas las barras. El desplazamiento de una barra convierte el +8,85 % del ejemplo en −6,85 %.
:::

:::quiz
p: ¿Cuál de estas operaciones introduce sesgo de mirar al futuro?
o: Calcular la media y la desviación típica de las variables con el conjunto de entrenamiento y aplicarlas al de prueba
o: Calcular la media y la desviación típica de las variables con todo el conjunto, entrenamiento y prueba juntos
o: Usar la etiqueta para entrenar el modelo
a: 2
e: Ajustar cualquier transformación con datos de prueba filtra información del futuro hacia el entrenamiento y hace que la validación sea optimista. Se ajusta con entrenamiento y se aplica al resto. Usar la etiqueta para entrenar es lo normal: la etiqueta es el objetivo, no una variable de entrada.
:::

:::quiz
p: Tu backtest da un rendimiento excelente, pero al retrasar todas las variables una barra más se desploma. ¿Qué conclusión es correcta?
o: Que el retraso extra ha destruido la señal, así que conviene dejarlo como estaba
o: Que la ventaja venía de información contemporánea, es decir, de mirar al futuro, y el resultado original no es alcanzable en la realidad
o: Que el modelo necesita más datos para funcionar con retraso
a: 2
e: Si la estrategia solo funciona cuando la variable y el retorno que se cobra son simultáneos, entonces la variable contiene el resultado. En producción esa información no está disponible en el momento de decidir. El desplazamiento extra es el test más rápido para detectarlo.
:::

:::nota
El sesgo de mirar al futuro no se arregla con más datos ni con mejor hardware: se arregla
escribiendo, para cada columna de tu tabla, en qué fecha y a qué hora estaba disponible. Si no
puedes contestar esa pregunta, no sabes si la columna es utilizable.
:::
