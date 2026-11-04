---
id: series-temporales-en-pandas
titulo: Series temporales en Pandas
fase: 3
nivel: intermedio
rutas: [ds, de, quant]
prerequisitos: [pandas-fundamentos, fechas-y-horas, pandas-agrupaciones-y-joins]
tags: [pandas, tiempo, resample, rolling]
resumen: Con la fecha en el índice, Pandas agrega por ventanas, calcula medias móviles por tiempo, desplaza y une series de frecuencias distintas por el instante más cercano.
fuentes: ["McKinney (2017), 'Python for Data Analysis'", "Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice'"]
---

## En una frase

Poner la fecha en el **índice** convierte una columna en una coordenada temporal, y a partir de ahí
Pandas agrupa por intervalos (`resample`), calcula ventanas por tiempo (`rolling("7D")`), desplaza
(`shift`) y pega dos series de frecuencias distintas por el instante más cercano (`merge_asof`).

## La idea

Tienes tres relojes midiendo lo mismo: un sensor que escribe cada 5 minutos, el precio de un activo
que llega una vez al día y la nómina que sale una vez al mes. Compararlos exige decidir sobre qué
rejilla común se miran, y **cada decisión tiene consecuencias**:

- Subir de frecuencia (de mensual a diario) obliga a inventar los días que no existen. Se puede
  repetir el último valor (`ffill`) o dejarlos vacíos (`NaN`), pero nunca son datos observados.
- Bajar de frecuencia (de diario a mensual) descarta detalle. Ya no hay una respuesta única: ¿el
  precio del mes es el último, la media, el máximo? Cada una cuenta una historia distinta.

Pandas no decide por ti, pero te da la maquinaria. La pieza que lo hace posible es el **índice
temporal**: una fecha que no es una columna más, sino la coordenada por la que se alinean todas las
operaciones. Con las fechas en el índice, `df.loc["2024-03"]` selecciona marzo entero sin escribir
una máscara, `resample("W")` agrupa por semanas naturales y `rolling("7D")` cuenta días de verdad.

Ese es el cambio mental que hay que hacer: **una ventana de 7 filas no es una ventana de 7 días**.
Si faltan días (un festivo, un sensor caído), `rolling(7)` coge las siete filas anteriores, que
pueden abarcar doce días, y el resultado mezcla cosas de dos semanas. `rolling("7D")` coge las
observaciones de los últimos siete días, que pueden ser tres filas.

Y la segunda pieza es la **alineación**. Dos series de frecuencias distintas no se unen con
`merge`: se unen con `merge_asof`, que para cada instante de una busca la última observación
anterior de la otra, con una tolerancia máxima. Es exactamente lo que hace un `JOIN` en SQL
temporal, y es la operación diaria de cualquier analista: pegar operaciones a precios, pedidos a
tarifas, lecturas a calibraciones.

## Definición formal

- **`DatetimeIndex`** — un índice de marcas de tiempo, idealmente ordenado, sin duplicados y con
  `freq` declarada (`.index.freq`, por ejemplo `<Day>`). Es el requisito de `resample`, de
  `rolling` con ventana de texto y de `merge_asof` sobre fechas.
- **`asfreq(regla, method=None)`** — cambia la rejilla de muestreo **sin agregar**: construye un
  índice nuevo con esa frecuencia, pone `NaN` donde no había observación (o arrastra el anterior con
  `method="ffill"`) y **descarta** las observaciones que no caen en una etiqueta de la rejilla.
- **`resample(regla, closed=None, label=None)`** — agrupa por intervalos y calcula un agregado por
  intervalo. Reglas: `"D"` (día), `"h"` (hora), `"W"` (semana que termina en domingo), `"W-MON"`,
  `"MS"` / `"ME"` (principio y fin de mes), `"QS"` / `"QE"` (trimestre).
- **`rolling(ventana, min_periods=None, closed="right")`** — ventana móvil. Si `ventana` es un
  entero, cuenta **filas**; si es texto (`"7D"`, `"3h"`), cuenta **tiempo** y exige índice temporal.
  En ventanas de tiempo `min_periods` vale 1 por defecto, así que las primeras posiciones ya traen
  valores calculados con muy pocos puntos.
- **`shift(n)`** mueve los valores `n` filas; `shift(freq="D")` mueve las **etiquetas** dejando los
  valores. `diff()` es `x − x.shift(1)` y `pct_change()` es la variación relativa.
- **`merge_asof(izq, der, on, by=None, direction="backward", tolerance=None)`** — para cada fila de
  la izquierda busca la última observación de la derecha cuyo instante sea anterior
  (`backward`), del mismo grupo si se pasa `by`, y deja `NaN` si no hay ninguna dentro de
  `tolerance`. Las dos claves tienen que estar **ordenadas**.

Y las dos cuentas que más se confunden, la simple y la compuesta:

:::formula
r_periodo = Π (1 + r_i) − 1          frente a          Σ r_i
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `label` | Extremo del intervalo que pone la fecha en `resample` | `"left"` o `"right"` | Con `"right"` (por defecto en `"W"`) el agregado cuelga del domingo; con `"left"`, del lunes. Cambia a qué fecha se une luego |
| `closed` | Extremo del intervalo que entra en el grupo | `"left"` o `"right"` | Con `"right"` (por defecto) el día de la etiqueta entra en su propio grupo; con `"left"` se va al anterior |
| `min_periods` | Puntos mínimos para dar un resultado | observaciones | Si sube, hay más `NaN` al principio (menos ruido y menos datos); en ventanas de tiempo vale 1 por defecto |
| `ventana` | Ancho de la ventana móvil | filas o tiempo | Si es tiempo, el número de filas que entran cambia con los huecos; si son filas, la duración en días cambia |
| `tolerance` | Distancia máxima permitida en `merge_asof` | tiempo | Si baja, más operaciones se quedan sin pareja (`NaN`) en vez de arrastrar un precio viejo |
:::

## Ejemplo

Dos observaciones de una serie: **10** el 1 de enero y **30** el 5 de enero.

- `asfreq("D")` devuelve cinco etiquetas —del 1 al 5— con valores `[10, NaN, NaN, NaN, 30]`. La
  rejilla tiene un valor por día y los huecos están vacíos. La suma sigue siendo 40: no se ha
  agregado nada.
- `resample("D").sum()` devuelve `[10, 0, 0, 0, 30]`. Aquí sí hay un cálculo: los días sin datos
  suman **0**. Mismo número de filas, información distinta: un hueco y un cero no son lo mismo.

Ventanas, con una serie irregular de cuatro puntos: 10 (1 de enero), 20 (2 de enero), 30 (5 de
enero) y 40 (6 de enero).

- `rolling("3D").sum()` da `[10, 30, 30, 70]`. En el 5 de enero solo entra ese punto, porque el del
  día 2 queda fuera de los tres días anteriores.
- `rolling(3).sum()` da `[NaN, NaN, 60, 90]`. Las tres filas anteriores al 5 de enero son el 1, el 2
  y el 5: **cinco días de calendario** contados como si fueran tres días seguidos.

Reagregar a frecuencia mensual, con diez retornos diarios del 1,0 %, 2,0 %, −1,0 %, 3,0 %, 0 %, 2,0 %,
1,0 %, −2,0 %, 1,0 % y 1,0 %:

- La suma es **0,08** y la media mensual **0,008**, pero la rentabilidad del mes, componiendo, es
  `1,01 · 1,02 · 0,99 · 1,03 · 1,00 · 1,02 · 1,01 · 0,98 · 1,01 · 1,01 − 1 = `**0,081893**`.
- Sumar retornos simples solo es exacto para variaciones muy pequeñas; con un −2 % y un +3 % en el
  mismo mes el error ya se ve en la cuarta cifra.

Y la alineación: tres operaciones (1 de enero a las 09:00, 1 de enero a las 12:00 y 3 de enero a las
10:00) contra dos precios (1 de enero a las 08:59 y a las 11:30). Con `direction="backward"` y
`tolerance=1 día`, las dos primeras operaciones encuentran precio (1,5 y 1,7) y la del 3 de enero
queda a **`NaN`**, porque el precio más cercano está a más de un día. Sin `tolerance` habría
arrastrado el precio del día 1 como si fuera del día 3.

:::figura
fichero: series-temporales-ventanas-y-etiquetas
pie: Arriba, la misma serie con un hueco de dos días. En el día 5 la ventana de tres días solo ve esa observación (30) y la ventana de tres filas arrastra la del día 2 (60): las dos son correctas y miden cosas distintas, y el hueco de en medio es lo que las separa. Abajo, los totales semanales del 1 al 10 de enero colocados en su fecha: con la etiqueta por defecto la semana del 1 al 7 cuelga del domingo 7 (28) y con label='left' cuelga del lunes 31 de diciembre (21). Si después unes esa tabla con otra por fecha, la misma semana se alinea con días distintos.
fuente: figuras/series-temporales-en-pandas-1.py
:::

## Código

```python verificable
import pandas as pd

s = pd.Series([10.0, 30.0], index=pd.to_datetime(["2024-01-01", "2024-01-05"]))

print(s.asfreq("D").tolist())            # -> [10.0, nan, nan, nan, 30.0]
print(s.asfreq("D").index.freq)          # -> <Day>
print(s.resample("D").sum().tolist())    # -> [10.0, 0.0, 0.0, 0.0, 30.0]
print(s.loc["2024-01-01":"2024-01-02"].tolist())   # -> [10.0]  trocear por texto

# asfreq cambia la rejilla y DESCARTA lo que no cae en ella: aqui se pierden los tres datos
meses = pd.Series([1.0, 2.0, 3.0],
                  index=pd.to_datetime(["2024-01-05", "2024-02-10", "2024-03-20"]))
print(meses.asfreq("MS").tolist())       # -> [nan, nan]

# Una frecuencia anclada al calendario da las mismas etiquetas a dos series distintas...
primera = pd.Series(1.0, index=pd.date_range("2024-01-01", periods=10, freq="D"))
segunda = pd.Series(1.0, index=pd.date_range("2024-01-03", periods=10, freq="D"))
print([d.strftime("%m-%d") for d in primera.resample("W").sum().index])   # -> ['01-07', '01-14']
print([d.strftime("%m-%d") for d in segunda.resample("W").sum().index])   # -> ['01-07', '01-14']
# ...pero una de varios dias empieza a contar en el primer dato de cada serie
print([d.strftime("%m-%d") for d in primera.resample("7D").sum().index])  # -> ['01-01', '01-08']
print([d.strftime("%m-%d") for d in segunda.resample("7D").sum().index])  # -> ['01-03', '01-10']
```

```python verificable
import pandas as pd

t = pd.Series([10.0, 20.0, 30.0, 40.0],
              index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-05", "2024-01-06"]))

print(t.rolling("3D").sum().tolist())     # -> [10.0, 30.0, 30.0, 70.0]  ventana de tiempo
print(t.rolling(3).sum().tolist())        # -> [nan, nan, 60.0, 90.0]    ventana de filas
print(t.rolling("3D").count().tolist())   # -> [1.0, 2.0, 1.0, 2.0]
print(t.rolling("3D", min_periods=2).sum().tolist())   # -> [nan, 30.0, nan, 70.0]

print(t.shift(1).tolist())                # -> [nan, 10.0, 20.0, 30.0]  fila anterior
print(t.shift(freq="D").index.tolist()[:2])   # -> [2024-01-02, 2024-01-03]  mueve la etiqueta
print(t.diff().tolist())                  # -> [nan, 10.0, 10.0, 10.0]
```

```python verificable
import pandas as pd

retornos = pd.Series([0.01, 0.02, -0.01, 0.03, 0.0, 0.02, 0.01, -0.02, 0.01, 0.01],
                     index=pd.date_range("2024-01-01", periods=10, freq="B"))
print(round(float(retornos.sum()), 6))                                      # -> 0.08
print(round(float((1 + retornos).resample("ME").prod().iloc[0] - 1), 6))    # -> 0.081893
print(round(float(retornos.resample("ME").mean().iloc[0]), 6))              # -> 0.008

# Semanas naturales: la etiqueta por defecto es el domingo que cierra la semana
semanas = pd.Series(range(1, 11), index=pd.date_range("2024-01-01", periods=10, freq="D"))
print(semanas.resample("W").sum().tolist())                       # -> [28, 27]
print([d.strftime("%a") for d in semanas.resample("W").sum().index])   # -> ['Sun', 'Sun']
print(semanas.resample("W", label="left", closed="left").sum().tolist())   # -> [21, 34]

# Alinear por el instante mas cercano: merge_asof, no merge
operaciones = pd.DataFrame({
    "hora": pd.to_datetime(["2024-01-01 09:00", "2024-01-01 12:00", "2024-01-03 10:00"]),
    "importe": [100, 50, 30]})
precios = pd.DataFrame({"hora": pd.to_datetime(["2024-01-01 08:59", "2024-01-01 11:30"]),
                        "precio": [1.5, 1.7]})
unido = pd.merge_asof(operaciones, precios, on="hora", direction="backward",
                      tolerance=pd.Timedelta("1D"))
print(unido["precio"].tolist())           # -> [1.5, 1.7, nan]
print(int(unido["precio"].isna().sum()))  # -> 1
```

:::claves
- `resample` **exige** que la fecha esté en el índice. Con la fecha en una columna, lo primero es
  `df.set_index("fecha")`; si no, no existe el método.
- `asfreq` y `resample` no son lo mismo: `asfreq` reindexa sin calcular (huecos a `NaN` o arrastre
  con `method="ffill"`), `resample` agrupa y calcula (los huecos pasan a ser 0 en una suma).
- `rolling("3D")` trabaja con `closed="right"`: la ventana es `(t − 3 días, t]`, sin incluir el
  extremo izquierdo. Por eso el 5 de enero solo suma su propio valor.
- En ventanas de **tiempo**, `min_periods` vale 1 por defecto: la primera fila ya tiene resultado
  calculado con un único punto. `min_periods=2` deja `NaN` donde no hay al menos dos observaciones.
- `shift(1)` mueve los valores manteniendo las etiquetas (la primera fila queda a `NaN`);
  `shift(freq="D")` hace lo contrario: conserva los valores y mueve las fechas un día.
- `pd.date_range(...)` y `pd.to_datetime(...)` devuelven un `DatetimeIndex` que sabe su frecuencia
  (`index.freq` es `<Day>`); esa información sobrevive al filtrar y a un `loc` por texto, pero se
  pierde al concatenar (`index.freq` pasa a `None`). No cambia ningún resultado, pero delata que el
  índice ya no es homogéneo.
:::

## Errores típicos

- **Llamar a `resample` con la fecha en una columna.** Da
  `TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex`, porque el método vive
  en el índice y no mira las columnas. Se arregla con `set_index("fecha")`, y de paso el `slice` por
  texto (`df.loc["2024-03"]`) empieza a funcionar.
- **Índice desordenado o con duplicados.** `merge_asof` lanza `ValueError: left keys must be sorted`
  y `asfreq` lanza `cannot reindex on an axis with duplicate labels`. `resample` con duplicados no
  se queja: suma las dos observaciones de la misma etiqueta en silencio. Antes de nada,
  `sort_index()` y una comprobación de `index.is_unique`.
- **Usar `resample("M")`.** En Pandas 3 esa frecuencia está eliminada (`Invalid frequency: M`) y hay
  que elegir `"ME"` (fin de mes) o `"MS"` (principio de mes). Es un cambio que rompe código escrito
  con Pandas 1 y que aparece en cuanto actualizas.
- **Suponer que la etiqueta de `resample("W")` es el lunes.** Por defecto la semana se cierra por la
  derecha y se etiqueta con el **domingo**: el total del 1 al 7 de enero cuelga del 7 de enero. Con
  `label="left", closed="left"` la misma semana cuelga del lunes anterior (31 de diciembre) y los
  números cambian de grupo (21 y 34 en vez de 28 y 27).
- **Confundir la media de los retornos con la rentabilidad del periodo.** `resample("ME").mean()`
  sobre retornos diarios da 0,008, que no es la rentabilidad del mes (0,081893). Para componer,
  `(1 + r).resample("ME").prod() - 1`.
- **Usar `rolling(7)` en una serie con huecos.** Cuenta siete filas, no siete días: si faltan tres
  días, esas siete filas abarcan diez días y la media mezcla dos regímenes. Para eso está
  `rolling("7D")`, que además deja claro en el código que la ventana es temporal.
- **Unir dos series temporales con `merge`.** `merge` empareja claves iguales, no cercanas: si las
  horas no coinciden exactamente al segundo, el resultado se queda sin filas. La herramienta es
  `merge_asof`, con `direction` y `tolerance` explícitos.

:::aviso
No todas las reglas anclan los intervalos al calendario. `"W"`, `"ME"` o `"QE"` sí: dos series
distintas producen las mismas etiquetas aunque empiecen en días distintos. Pero una frecuencia de
varios días como `"7D"` empieza a contar en la **primera observación de cada serie**: una que
arranca el 1 de enero da los intervalos del 1 y del 8, y otra que arranca el 3 de enero los da del
3 y del 10. `origin` no lo arregla (solo actúa en frecuencias de horas o menores, y avisa por
pantalla si lo intentas). Además, en cualquier frecuencia el primer y el último intervalo suelen
estar incompletos: una serie horaria resampleada a `"2h"` puede dar 1, 2, 2 y 1 observaciones por
intervalo. Mira siempre `res.index[:3]`, `res.index[-2:]` y `res.count()` antes de unir ese
resultado con otra fuente.
:::

:::practica
enunciado: Tienes precios diarios con huecos (faltan festivos) y una lista de operaciones con hora exacta. Escribe el código que (a) pone la serie de precios en rejilla diaria sin inventar valores, (b) calcula la media móvil de 7 días por tiempo y (c) pega a cada operación el último precio conocido con una tolerancia de 2 días, diciendo cuántas operaciones se quedan sin precio.
pista: Para (a), `asfreq("D")` deja `NaN` y `method="ffill"` arrastra el último valor; para (b), `rolling("7D")`; para (c), `merge_asof` con `direction="backward"` y `tolerance=pd.Timedelta("2D")`.
solucion: `precios = precios.sort_index()` y después `precios.asfreq("D", method="ffill")` deja un valor por día natural arrastrando el último precio conocido (no interpola: no inventa precios, repite el último). La media móvil es `precios.rolling("7D").mean()`, que solo usa las observaciones de los últimos siete días. La unión es `pd.merge_asof(operaciones.sort_values("hora"), precios.reset_index(), left_on="hora", right_on="index", direction="backward", tolerance=pd.Timedelta("2D"))`, y las operaciones sin precio se cuentan con `unido["precio"].isna().sum()`. Si en vez de `asfreq` usaras `resample("D").mean()`, los festivos tendrían un valor calculado (la media del día, que es el propio precio si solo hay uno) y estarías tratando igual un dato observado y un día vacío.
:::

## Comprueba que lo sabes

:::quiz
p: Una serie tiene observaciones el 1, el 2, el 5 y el 6 de enero. ¿Qué devuelve `rolling(3).sum()` frente a `rolling("3D").sum()` en el 5 de enero?
o: Lo mismo en las dos: la suma de las tres observaciones anteriores
o: `rolling(3)` suma 60 (las filas 1, 2 y 5) y `rolling("3D")` suma 30 (solo el día 5)
o: `rolling("3D")` suma 60 y `rolling(3)` suma 30
a: 2
e: `rolling(3)` cuenta filas: coge las tres anteriores, que son el 1, el 2 y el 5 de enero y suman 60. `rolling("3D")` cuenta tiempo: la ventana es el intervalo de tres días que termina en el 5 de enero, así que el dato del día 2 queda fuera y solo entra el 30. Las dos son correctas; miden cosas distintas.
:::

:::quiz
p: `s.asfreq("D")` sobre una serie con datos solo el 1 y el 5 de enero, ¿qué hace con los días 2, 3 y 4?
o: Les pone `NaN` y deja la serie con cinco filas
o: Los rellena repitiendo el último valor conocido
o: Los elimina y deja la serie con dos filas
a: 1
e: `asfreq` cambia la rejilla y no agrega: crea las etiquetas que faltan con `NaN`. Solo arrastra el valor anterior si le pasas `method="ffill"`, y solo interpola si usas `method="bfill"` u otra estrategia explícita.
:::

:::quiz
p: `resample("W").sum()` sobre los días 1 a 10 de enero de 2024, ¿qué etiquetas produce?
o: El 1 y el 8 de enero, porque la semana empieza en lunes
o: El 7 y el 14 de enero, porque la semana se cierra por la derecha y se etiqueta con el domingo
o: El 31 de diciembre y el 7 de enero, porque `closed="left"` por defecto
a: 2
e: En `resample("W")` la etiqueta es el final del intervalo (domingo) y el intervalo se cierra por la derecha, así que el total del 1 al 7 cuelga del 7 y el del 8 al 10, del 14. Con `label="left", closed="left"` las etiquetas serían el 31 de diciembre y el 7 de enero, y los grupos cambiarían.
:::

:::quiz
p: Tienes operaciones con hora exacta y precios diarios. ¿Qué usas para pegar a cada operación el último precio anterior con un límite de un día?
o: `merge(operaciones, precios, on="hora", how="left")`
o: `merge_asof(operaciones, precios, on="hora", direction="backward", tolerance=pd.Timedelta("1D"))`
o: `operaciones.join(precios, on="hora")`
a: 2
e: `merge` y `join` emparejan claves iguales: como las horas no coinciden, no habría filas o saldrían `NaN` en todas. `merge_asof` busca la observación más cercana en el tiempo, y con `direction="backward"` coge la última anterior; `tolerance` impide que arrastre un precio demasiado viejo y deja `NaN` cuando no hay ninguno cerca.
:::

:::nota
Antes de modelar nada de una serie temporal conviene responder a tres preguntas: ¿cuál es la
frecuencia real de los datos (no la que crees), cuántos huecos hay y con qué criterio se rellenan, y
qué ventana temporal tiene sentido para el negocio. La aritmética de `resample` es fácil; decidir
qué significa un cero, un hueco y un valor arrastrado es lo que cambia el resultado (ver
[[estacionariedad]] y [[validacion-temporal]]).
:::
