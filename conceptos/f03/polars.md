---
id: polars
titulo: Polars
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [pandas-fundamentos, pandas-agrupaciones-y-joins]
tags: [polars, expresiones, pereza]
resumen: API de expresiones, plan perezoso y ejecución en paralelo sobre memoria de Arrow: la alternativa a Pandas cuando la tabla deja de ser cómoda.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

Polars describe las transformaciones como **expresiones** sobre columnas y las ejecuta con un
motor en paralelo que puede analizar el plan antes de tocar los datos; es la alternativa a Pandas
cuando el tamaño, la memoria o el número de núcleos empiezan a importar.

## La idea

En Pandas escribes una secuencia de órdenes: filtra esto, añade aquella columna, agrupa, ordena.
Cada línea se ejecuta cuando la escribes y produce una tabla nueva. En Polars escribes una
**consulta**: describes lo que quieres («para cada ciudad, la suma de importes, ordenado de mayor
a menor») y el motor decide cómo hacerlo. La diferencia es la misma que entre dar instrucciones
paso a paso a un taxista y decirle «llévame al aeropuerto por la ruta más rápida»: en el segundo
caso quien conduce puede aprovechar información que tú no tienes.

Ese «puede analizar el plan» es la **evaluación perezosa**. Con un `LazyFrame` no has leído nada
todavía: tienes un plan. Cuando llamas a `.collect()`, el optimizador reordena el trabajo y, entre
otras cosas:

- **Empuja los filtros hacia abajo** (*predicate pushdown*): si al final solo quieres 2024, no
  lee los años anteriores.
- **Empuja la selección de columnas** (*projection pushdown*): si usas 3 de 40 columnas de un
  Parquet, lee solo esas 3 (ver [[arrow-y-formatos-columnares]]).
- **Elimina trabajo repetido** y reparte las operaciones entre todos los núcleos disponibles, sin
  que tú escribas una línea de paralelismo.

Y hay una decisión de diseño que cambia la forma de programar: **Polars no tiene índice**. En
Pandas el índice es a la vez etiqueta y fuente de bugs (`loc` frente a `iloc`, alineaciones
inesperadas). Aquí cada fila es una fila y punto: para identificar algo, tienes una columna con
el identificador. A cambio, desaparecen `reset_index`, `set_index` y toda la familia de errores
asociada.

¿Cuándo sustituye a Pandas? Cuando alguna de estas es verdad: la tabla no cabe cómoda en memoria,
la operación es pesada (agrupaciones y uniones grandes), lees Parquet y quieres aprovechar el
optimizador, o necesitas exprimir varios núcleos. ¿Cuándo **no**? Con tablas de unos miles de
filas la diferencia es ruido, y el ecosistema de Pandas (scikit-learn, Matplotlib, Seaborn,
muchas librerías de negocio) sigue siendo más ancho. La conversión entre ambos es barata y se
puede hacer en los dos sentidos, así que la pregunta no es cuál es mejor, sino dónde está el
cuello de botella.

## Definición formal

- **`DataFrame`** — tabla en memoria, ya calculada (*eager*). Tiene columnas con nombre y tipo,
  sin índice.
- **`LazyFrame`** — un **plan** sin ejecutar. Se construye con `pl.LazyFrame(...)`, con
  `pl.scan_parquet(...)` o convirtiendo con `.lazy()`, y se ejecuta con `.collect()`.
- **`Expr`** — una expresión: una receta que se aplica a columnas y devuelve columnas. `pl.col("x")`
  es la columna `x`; `pl.col("x") * 2` es esa columna multiplicada; `pl.lit(1)` es un valor
  constante; `.alias("nombre")` renombra el resultado y `cast(pl.Int64)` cambia el tipo.
- **Contextos** donde se evalúa una expresión: `select` (elegir y calcular columnas),
  `with_columns` (añadir sin quitar), `filter` (filtrar filas), `group_by(...).agg(...)`
  (agregar por grupo) y `sort`.
- **`pl.when(condición).then(a).otherwise(b)`** — el `if` de expresiones, equivalente al
  `CASE WHEN` de SQL.
- **Semántica inmutable**: casi todos los métodos devuelven un objeto nuevo. No hay
  `inplace=True`; si quieres conservar el resultado, asígnalo (`df = df.with_columns(...)`).

La relación con SQL es directa, y ayuda a leer el código:

| SQL | Polars |
| --- | --- |
| `SELECT a, b * 2 AS c` | `select("a", (pl.col("b") * 2).alias("c"))` |
| `WHERE x > 0` | `filter(pl.col("x") > 0)` |
| `GROUP BY g` con `SUM(v)` | `group_by("g").agg(pl.col("v").sum())` |
| `CASE WHEN x > 0 THEN 1 ELSE 0 END` | `pl.when(pl.col("x") > 0).then(1).otherwise(0)` |
| `ORDER BY v DESC` | `sort("v", descending=True)` |

## Ejemplo

Un `LazyFrame` con dos columnas, `x = [1, 2, 3, 4]` e `y = [10, 20, 30, 40]`, y este plan: quédate
con las filas donde `x > 1`, calcula `ratio = y / x` y devuelve solo `x` y `ratio`.

- Primero se filtra: quedan las filas con `x = 2, 3, 4` e `y = 20, 30, 40`.
- Después se calcula el ratio fila a fila: 20/2 = **10**, 30/3 = **10**, 40/4 = **10**.
- Resultado: `x = [2, 3, 4]`, `ratio = [10.0, 10.0, 10.0]`.

Nada de eso se ha ejecutado hasta el `.collect()`. Si el mismo plan se leyera de un Parquet de
500 GB, el filtro `x > 1` se aplicaría **mientras se lee**, descartando bloques enteros antes de
construir la tabla.

Para una agrupación, con ciudades `Madrid, Madrid, Sevilla` e importes `10, 30, 5`, la suma por
ciudad da Madrid **40,0** y Sevilla **5,0**. Es el mismo resultado que en Pandas (ver
[[pandas-agrupaciones-y-joins]]) con una diferencia de forma: aquí no hay índice, el resultado
tiene exactamente las columnas que pides.

## Código

```python verificable
import polars as pl

df = pl.DataFrame({
    "ciudad": ["Madrid", "Madrid", "Sevilla"],
    "importe": [10.0, 30.0, 5.0],
})

# group_by + agg: una fila por grupo, y el resultado se ordena como parte de la consulta
print(df.group_by("ciudad").agg(pl.col("importe").sum().alias("total")).sort("ciudad").to_dicts())
# -> [{'ciudad': 'Madrid', 'total': 40.0}, {'ciudad': 'Sevilla', 'total': 5.0}]
print(df["importe"].sum())   # -> 45.0
```

```python verificable
import polars as pl

lf = pl.LazyFrame({"x": [1, 2, 3, 4], "y": [10.0, 20.0, 30.0, 40.0]})

# Esto NO ha ejecutado nada: es un plan con filtro, columna calculada y seleccion
plan = (lf.filter(pl.col("x") > 1)
          .with_columns((pl.col("y") / pl.col("x")).alias("ratio"))
          .select("x", "ratio"))

print(plan.collect().to_dict(as_series=False))
# -> {'x': [2, 3, 4], 'ratio': [10.0, 10.0, 10.0]}

# El if/else de las expresiones, sin bucles ni apply
print(pl.LazyFrame({"v": [-1, 0, 2]})
      .select(pl.when(pl.col("v") > 0).then(pl.lit("pos")).otherwise(pl.lit("no")).alias("s"))
      .collect()["s"].to_list())
# -> ['no', 'no', 'pos']
```

```python verificable
import polars as pl
import pyarrow as pa

tabla = pa.table({"x": [1, 2, 3]})
df = pl.from_arrow(tabla)          # comparte los buffers de Arrow, sin convertirlos
print(df["x"].to_list())           # -> [1, 2, 3]
print(df.to_arrow().equals(tabla)) # -> True

# Convertir a pandas es una operacion explicita: util para pasar el resultado a otra libreria
print(df.to_pandas()["x"].tolist())   # -> [1, 2, 3]
```

## Errores típicos

- **Llamar a `.collect()` después de cada paso.** Es el error que anula la ventaja principal: si
  recoges el resultado en cada línea, el optimizador solo ve una operación cada vez y no puede
  empujar filtros ni eliminar trabajo. Encadena todo el plan y recoge una vez al final.
- **Trasladar los hábitos de índice de Pandas.** `df.loc`, `df.iloc` y `reset_index` no existen
  en Polars. Para trabajar con posiciones hay funciones explícitas (`with_row_index`,
  `gather`), y para identificar filas se usa una columna con el id.
- **Usar `map_elements` (o `apply`) para todo.** Ejecuta Python por elemento y rompe el
  paralelismo: es la versión Polars de `iterrows()`. Casi siempre existe una expresión nativa
  (`str.contains`, `dt.year`, `when/then`); búscala antes.
- **Suponer que Polars convierte tipos por ti.** Los dtypes son estrictos: restar un entero a una
  columna de texto lanza un error en vez de intentar adivinar. Es una buena noticia (los fallos
  aparecen al principio), pero obliga a escribir `cast` de forma explícita.
- **Creer que siempre es más rápido que Pandas.** Con pocas filas la diferencia es ruido y el
  ecosistema de Pandas juega a favor. Cambiar de librería sin medir es cambiar un problema por
  dos (ver [[rendimiento-y-perfilado]]).
- **Convertir a Pandas al principio del pipeline.** `pl.from_pandas(...)` al leer y
  `to_pandas()` al escribir está bien; hacerlo en medio de cada transformación copia los datos
  una y otra vez y pierdes lo que habías ganado.

:::practica
enunciado: Con `lf = pl.LazyFrame({"ciudad": ["Madrid", "Madrid", "Sevilla", "Bilbao"], "unidades": [3, 5, 2, 7]})`, escribe el plan perezoso que sume `unidades` por ciudad, descarte las que sumen menos de 5 y ordene de mayor a menor. ¿Qué filas devuelve `collect()`?
pista: La suma se calcula dentro de `group_by(...).agg(...)`; el filtro sobre el total es un `filter` posterior al `agg`, y todo sigue siendo un plan hasta `collect()`.
solucion: `lf.group_by("ciudad").agg(pl.col("unidades").sum().alias("total")).filter(pl.col("total") >= 5).sort("total", descending=True).collect()` devuelve `[{'ciudad': 'Madrid', 'total': 8}, {'ciudad': 'Bilbao', 'total': 7}]`. Paso a paso: la suma por grupo da Madrid 8, Sevilla 2 y Bilbao 7; el `filter` descarta Sevilla porque 2 < 5; el `sort` deja Madrid delante de Bilbao. Conclusión: dos filas, Madrid con 8 y Bilbao con 7.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué has leído del disco después de `lf = pl.scan_parquet("datos.parquet")` y añadir un `filter`?
o: Todo el fichero, porque `scan_parquet` lo carga en memoria
o: Nada: tienes un plan, y la lectura ocurre al llamar a `.collect()`
o: Solo la primera fila, para adivinar el esquema
a: 2
e: `scan_parquet` construye un `LazyFrame`: es un plan sin ejecutar. La lectura y el filtrado ocurren al recoger el resultado, y ahí el optimizador puede descartar columnas y bloques que no hacen falta.
:::

:::quiz
p: ¿Cuál es la diferencia entre `select` y `with_columns`?
o: `select` deja solo las columnas que le pides; `with_columns` añade o reemplaza y conserva las demás
o: Son sinónimos exactos
o: `with_columns` solo sirve para renombrar
a: 1
e: `select` define la lista final de columnas (lo que no nombras desaparece), mientras que `with_columns` añade las nuevas y mantiene las existentes. Confundirlas produce tablas a las que les faltan columnas justo antes de un `group_by`.
:::

:::quiz
p: En Polars, ¿cómo se identifica una fila concreta?
o: Con `df.loc[0]`, como en Pandas
o: Con una columna que contenga el identificador, porque no hay índice
o: Con `df.index[0]`
a: 2
e: Polars no tiene índice: `loc`, `iloc` e `index` no existen. La identidad de una fila es el valor de alguna de sus columnas, y si necesitas un número de orden se añade con `with_row_index`.
:::

:::truco
Si ya sabes SQL, la forma más rápida de aprender Polars es leer sus consultas como SQL: `select`
es el `SELECT PROJECT`, `filter` el `WHERE`, `group_by().agg()` el `GROUP BY` y `sort` el
`ORDER BY`. La diferencia es que en Polars las expresiones se pueden reutilizar y combinar como
variables de Python.
:::
