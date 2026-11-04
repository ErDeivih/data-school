---
id: reformar-tablas-ancho-y-largo
titulo: Reformar tablas: ancho y largo
fase: 3
nivel: intermedio
rutas: [core, ds, de]
prerequisitos: [pandas-fundamentos, pandas-agrupaciones-y-joins]
tags: [pandas, melt, pivot, tidy]
resumen: melt, pivot y stack cambian de sitio la información sin sumar nada; es el paso obligatorio para convertir doce columnas de meses en una serie temporal.
fuentes: ["Wickham (2014), 'Tidy Data'", "McKinney (2017), 'Python for Data Analysis'"]
---

## En una frase

Reformar una tabla es mover la información entre los **nombres de las columnas** y las **celdas**
sin calcular nada: `melt` la estira, `pivot` y `stack` la vuelven a ensanchar, y ni una fila se
suma por el camino.

## La idea

Coge la hoja de cálculo que todo el mundo usa para las ventas mensuales: una fila por cliente y
doce columnas, de enero a diciembre. Para mirarla con el dedo es cómoda. Para casi todo lo demás es
un estorbo:

- No puedes dibujar una línea: una gráfica de líneas necesita **una** columna de fechas y **una**
  columna de valores, y ahí tienes doce columnas de valores sueltos.
- No puedes agrupar por mes ni ordenar por importe: la fecha no es un dato, es el **nombre de una
  columna** (metadato del esquema). No se puede filtrar por `mes > 6` algo que no existe como
  columna.
- No puedes añadir un año más sin tocar el esquema: el año 2024 tiene que ser `ene_2024`, y entonces
  los nombres se lían.

`melt` arregla eso: cada nombre de columna se convierte en un **valor** de una columna nueva
(`mes`) y cada celda pasa a ser una fila. La tabla resultante tiene una fila por observación
—cliente, mes, ventas— y eso es lo que se llama una tabla **larga** o *tidy*. La tabla de partida,
con una columna por variable, se llama **ancha**.

Y aquí está lo importante: **reformar no cambia ni un número**. No hay suma, ni media, ni
agrupación. Los mismos 12 valores siguen ahí; solo cambia el sitio donde están escritos. Es un
cambio de forma, no de contenido, y por eso la comprobación de que lo has hecho bien es que la suma
total no se mueva. Si se mueve, has hecho un `pivot_table` o un `groupby` sin querer.

El camino de vuelta (largo a ancho) se hace con `pivot` o con `unstack`, y ahí aparece la única
trampa de verdad del asunto: la tabla ancha es el **producto cartesiano** de los identificadores por
las variables. Si en la tabla larga falta una combinación —un cliente sin ventas en febrero—, esa
celda no desaparece: vuelve como `NaN`. El pivote no pierde datos, pero **rellena huecos**.

## Definición formal

- **Tabla ancha** (*wide*): una fila por entidad y una columna por variable. `n` filas y `m + k`
  columnas, donde `m` son los identificadores y `k` las variables que se repiten (los meses).
- **Tabla larga** (*long* o *tidy*): una fila por observación, con las columnas
  `identificadores… , variable, valor`. `n · k` filas y `m + 2` columnas.
- `melt(id_vars, value_vars, var_name="variable", value_name="value")` — de ancho a largo. Si no
  pasas `value_vars`, toma **todas** las columnas que no estén en `id_vars`.
- `pivot(index, columns, values)` — de largo a ancho. Exige que cada par `(index, columns)` aparezca
  **una sola vez**; con duplicados lanza `ValueError` en lugar de agregar.
- `pivot_table(...)` — la versión que **sí** agrega cuando hay duplicados (`aggfunc`, media por
  defecto; ver [[pandas-agrupaciones-y-joins]]).
- `stack()` / `unstack()` — lo mismo pero usando el índice: `stack` mueve el último nivel de
  columnas al índice de filas y devuelve una `Series` con `MultiIndex`; `unstack` deshace el camino.
- `wide_to_long(stubnames, i, j, sep)` — para familias de columnas con nombre repetido
  (`v2023`, `v2024`).

La cuenta que gobierna todo:

:::formula
filas_largas = filas_anchas · k          filas_anchas = filas_largas / k
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Filas de la tabla ancha | filas | La tabla larga crece igual de rápido: cada cliente nuevo añade `k` filas |
| `k` | Columnas de valor (los meses) | columnas | La tabla larga crece proporcionalmente, y los identificadores se repiten `k` veces más |
| `m` | Columnas identificadoras que se mantienen | columnas | Cada una se copia en las `n · k` filas largas: más ancho de tabla, más memoria |
| celdas | Celdas del pivote de vuelta | celdas | Es `n · k`: los huecos que no existían en la tabla larga vuelven como `NaN` |
:::

## Ejemplo

Tres clientes y tres meses de ventas:

```
cliente   ene   feb   mar
      A    10    20    30
      B    40    50    60
      C    70    80    90
```

- La forma ancha tiene `3 × 4 = 12` celdas y `n = 3` filas.
- Con `melt`, la forma larga tiene `n · k = 3 · 3 = 9` filas y 3 columnas (cliente, mes, ventas).
- La suma de los nueve valores es **450**, y en la tabla ancha también: `(10+20+30) + (40+50+60) +
  (70+80+90) = 60 + 150 + 240 = 450`. Reformar no movió ni un número.
- `melt` va **columna a columna**, no fila a fila: las tres primeras filas de la tabla larga son
  los tres clientes de enero (A, B, C), después los tres de febrero y luego los de marzo.

Ahora la vuelta con huecos. Una tabla larga con cinco observaciones de las seis posibles
(A-ene 1, A-feb 2, A-mar 3, B-ene 4, B-mar 6; falta B-feb):

- El pivote tiene 2 filas y 3 columnas: 6 celdas.
- Cinco llevan datos y **una** (B-feb) queda a `NaN`: el 16,7 % de la tabla.
- La suma de la tabla ancha (saltando el `NaN`) sigue siendo 16, exactamente la suma de la tabla
  larga. No se perdió nada: se añadió un hueco.

:::figura
fichero: reformar-tablas-ancho-y-largo-celdas
pie: Arriba, el precio de reformar: con 500 clientes, la tabla ancha se queda en 500 filas con cualquier número de meses, mientras que la larga paga una fila por cliente y mes (6.000 filas con doce meses). Abajo, la vuelta: el pivote siempre devuelve el producto cartesiano de identificadores por variables, así que si a la tabla larga le faltan tres pares de los doce, esas tres celdas reaparecen vacías en lugar de desaparecer. El pivote no pierde ningún número, pero rellena huecos, y esos huecos hay que decidir si son cero, nulos o un error de los datos.
fuente: figuras/reformar-tablas-ancho-y-largo-1.py
:::

## Código

```python verificable
import pandas as pd

ancho = pd.DataFrame({
    "cliente": ["A", "B", "C"],
    "ene": [10, 20, 30],
    "feb": [40, 50, 60],
    "mar": [70, 80, 90],
})
largo = ancho.melt(id_vars="cliente", var_name="mes", value_name="ventas")

print(ancho.shape, largo.shape)          # -> (3, 4) (9, 3)
print(largo["mes"].tolist())             # -> ['ene', 'ene', 'ene', 'feb', 'feb', 'feb', 'mar', 'mar', 'mar']
print(largo["ventas"].sum())             # -> 450  la misma suma que en la tabla ancha
print(ancho[["ene", "feb", "mar"]].to_numpy().sum())   # -> 450
print(largo.dtypes["ventas"])            # -> int64  el tipo de los valores se conserva
```

```python verificable
import pandas as pd

largo = pd.DataFrame({
    "cliente": ["A", "A", "A", "B", "B"],
    "mes": ["ene", "feb", "mar", "ene", "mar"],
    "ventas": [1, 2, 3, 4, 6],
})
ancho = largo.pivot(index="cliente", columns="mes", values="ventas")

print(ancho.shape)                          # -> (2, 3)
print(ancho.loc["B"].tolist())              # -> [4.0, nan, 6.0]  falta B-feb
print(int(ancho.isna().sum().sum()), ancho.size)   # -> 1 6

# pivot NO agrega: con un par (cliente, mes) repetido lanza un error en vez de sumar
repetido = pd.concat([largo, largo.iloc[[0]]])
try:
    repetido.pivot(index="cliente", columns="mes", values="ventas")
except ValueError as e:
    print(str(e))                           # -> Index contains duplicate entries, cannot reshape

# pivot_table es la que agrega; aqui se le dice explicitamente que sume
print(repetido.pivot_table(index="cliente", columns="mes", values="ventas",
                           aggfunc="sum").loc["A"].tolist())   # -> [2.0, 2.0, 3.0]
```

```python verificable
import numpy as np
import pandas as pd

ancho = pd.DataFrame({"ene": [1, 4], "feb": [2, 5], "mar": [3, 6]}, index=["A", "B"])
larga = ancho.stack()                          # de columnas a filas: Series con dos niveles

print(type(larga).__name__, larga.index.nlevels)     # -> Series 2
print(larga.loc["A"].to_dict())                      # -> {'ene': 1, 'feb': 2, 'mar': 3}
print(larga.unstack().equals(ancho))                 # -> True  la vuelta es exacta

# Al desapilar, los huecos del producto cartesiano se rellenan con NaN...
parcial = pd.Series([1.0, np.nan, 3.0],
                    index=pd.MultiIndex.from_tuples([("A", "ene"), ("A", "feb"), ("B", "ene")]))
print(parcial.unstack().to_numpy().tolist())              # -> [[1.0, nan], [3.0, nan]]
# ...pero fill_value solo rellena los que faltaban por combinacion, no los que ya eran nulos
print(parcial.unstack(fill_value=0).to_numpy().tolist())  # -> [[1.0, nan], [3.0, 0.0]]
```

:::claves
- `melt` devuelve las filas **columna a columna**: primero todos los identificadores de `ene`,
  después los de `feb`. Si esperabas el orden de la tabla original, no es ese.
- `melt` **pierde el índice**: si la tabla tenía `set_index("cliente")`, hay que hacer
  `reset_index()` antes o el identificador desaparece de la tabla larga.
- `largo["mes"]` es de tipo texto (`str`), no numérico ni fecha: los nombres de columna son texto
  y así se quedan. `largo.dtypes["ventas"]` sí conserva el tipo original.
- `pivot` ordena las columnas del resultado alfabéticamente y devuelve `NaN` en las combinaciones
  que no existían; el número de celdas es siempre `n_identificadores · n_variables`.
- `stack()` devuelve una `Series` (no un `DataFrame`) con dos niveles de índice que **no tienen
  nombre** (`index.names` es `[None, None]`, no los nombres de la tabla). Con nombres, `unstack`
  tiene que decir con qué nivel trabaja.
- `wide_to_long` devuelve un `DataFrame` con `MultiIndex`, no una `Series`, y necesita
  `reset_index()` si quieres las columnas como columnas.
:::

## Errores típicos

- **Llamar a `melt` sin decir qué columnas son medidas.** Sin `value_vars`, `melt` se queda con
  todas las columnas que no estén en `id_vars`: si la tabla tiene un `total` o un `pais`, acaban
  dentro de la columna de valores, mezclados con los meses. Nombra las columnas de valor.
- **Esperar que `pivot` sume.** Con un par `(index, columns)` repetido lanza
  `ValueError: Index contains duplicate entries, cannot reshape`. Si el negocio pide agregar, la
  herramienta es `pivot_table` y hay que decidir `aggfunc` a conciencia.
- **Pasar `fill_value` a `pivot`.** Ese argumento existe en `pivot_table`, no en `pivot` (da
  `TypeError`). Y aunque lo tengas, `fill_value` solo rellena las combinaciones que faltaban: un
  valor que ya era `NaN` sigue siendo `NaN`.
- **Convertir `ene`, `feb`… en fechas con `pd.to_datetime`.** Con nombres de mes en español lanza
  `DateParseError`. Hay que traducir los nombres a números (`{"ene": 1, "feb": 2, …}`) y construir
  la fecha, o guardar directamente `2024-01`. Y ojo: en la tabla ancha el año no está en ninguna
  parte, así que si hay dos años, el nombre de la columna tiene que llevarlo (`ene-2023`).
- **Creer que la tabla larga ocupa menos.** Tiene `k` veces más filas y repite los identificadores
  en todas ellas; el número de medidas es el mismo, pero el fichero puede ser varias veces mayor.
  Reformar no es una optimización de almacenamiento, es un cambio de forma.
- **`stack` sobre columnas de tipos distintos.** Si mezclas importes y textos, la columna apilada
  acaba en `object` y los números dejan de ser números. Y en Pandas 3, `stack(dropna=False)` lanza
  `ValueError`: la implementación nueva no descarta ni introduce filas nulas, así que ese argumento
  ya no tiene sentido.

:::truco
El puente a serie temporal es siempre el mismo: `melt` → convertir la columna de meses en fechas
(el día 1 de cada mes) → `set_index` → `resample`. Sin el `melt` no hay nada que resamplear, porque
la fecha está en el nombre de las columnas (ver [[series-temporales-en-pandas]]).
:::

:::practica
enunciado: Tienes una tabla ancha con `cliente` y doce columnas (`ene` … `dic`) de ventas de 2024, con 500 clientes. Pásala a formato largo, calcula el total por mes y comprueba que el total del año coincide con el de la tabla ancha.
pista: `melt` con `id_vars="cliente"`; después `groupby("mes")`, pero para que los meses salgan en orden necesitas una columna de fecha, no texto.
solucion: `largo = ancha.melt(id_vars="cliente", var_name="mes", value_name="ventas")` da 500 · 12 = 6.000 filas. Con `meses = {"ene": 1, "feb": 2, …}` se construye `largo["fecha"] = pd.to_datetime({"year": 2024, "month": largo["mes"].map(meses), "day": 1})` y entonces `largo.groupby("fecha")["ventas"].sum()` sale en orden cronológico. La comprobación: `largo["ventas"].sum()` tiene que ser idéntica a `ancha.drop(columns="cliente").to_numpy().sum()`, porque reformar no agrega nada. Si no coincide, es que algún `NaN` se ha tratado distinto en los dos caminos.
:::

## Comprueba que lo sabes

:::quiz
p: Una tabla ancha tiene 200 filas y 12 columnas de meses. ¿Cuántas filas tiene después de `melt`?
o: 200, porque cambia el número de columnas, no el de filas
o: 2.400, porque cada fila se convierte en una fila por columna de valor
o: 212, porque se suman filas y columnas
a: 2
e: `melt` duplica la estructura: cada una de las 200 entidades aparece una vez por cada una de las 12 columnas de valor, así que quedan 200 · 12 = 2.400 filas largas con los identificadores repetidos. El número de medidas no cambia, pero el de filas sí.
:::

:::quiz
p: En la tabla larga hay dos filas con el mismo cliente y el mismo mes. ¿Qué pasa al hacer `pivot(index="cliente", columns="mes", values="ventas")`?
o: Suma los dos valores y deja uno
o: Lanza `ValueError: Index contains duplicate entries, cannot reshape`
o: Deja el primero y descarta el segundo en silencio
a: 2
e: `pivot` no agrega: solo recoloca. Como no sabe qué hacer con dos valores en la misma celda, se niega a continuar. Para agregar está `pivot_table`, con `aggfunc` explícito (su valor por defecto es la media, no la suma).
:::

:::quiz
p: Después de un `melt`, ¿qué contiene la columna nueva que antes era el nombre de las columnas (ene, feb, mar)?
o: Fechas reales del tipo `datetime64`
o: Texto: los nombres de columna son texto y así se quedan
o: Números de mes (1, 2, 3) puestos por Pandas
a: 2
e: `melt` copia los nombres de columna tal cual, como texto. Convertirlos en fechas es trabajo tuyo: con nombres en español `pd.to_datetime` lanza `DateParseError`, así que hay que traducir los nombres a números o haber nombrado las columnas como `2024-01`.
:::

:::quiz
p: ¿Cuál es la comprobación rápida de que has reformado bien una tabla?
o: Que el número de filas sea el que dice la fórmula `n · k`
o: Que la suma total de las medidas no haya cambiado
o: Que los tipos de las columnas sigan siendo los mismos
a: 2
e: Ninguna de las tres es mala, pero la suma es la que detecta el error grave: si reformando se te ha colado un `pivot_table` o un `groupby`, la suma cambia y las otras dos comprobaciones pueden pasar igualmente. La suma de la tabla ancha (ignorando los `NaN`) y la de la larga tienen que coincidir exactamente.
:::

:::nota
El nombre «tidy data» viene del paper de Hadley Wickham (2014): una fila por observación, una
columna por variable y una tabla por unidad de observación. Casi todas las herramientas de
gráficas, de agrupación y de series temporales esperan esa forma, y por eso `melt` aparece una y
otra vez en los pipelines, casi siempre justo antes de un `groupby` o de un `resample`.
:::
