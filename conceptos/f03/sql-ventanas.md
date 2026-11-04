---
id: sql-ventanas
titulo: "SQL: funciones de ventana"
fase: 3
nivel: avanzado
rutas: [de, ds]
prerequisitos: [sql-agregaciones-y-group-by, sql-subconsultas-y-cte]
tags: [sql, ventanas, ranking, series-temporales]
resumen: Calcular un valor por fila mirando sus vecinas -ranking, diferencias, acumulados y medias móviles- sin colapsar la tabla como hace GROUP BY.
fuentes: ["Garcia-Molina, Ullman y Widom (2008), 'Database Systems: The Complete Book'", "Winand (2012), 'SQL Performance Explained'"]
---

## En una frase

Una función de ventana calcula un valor para cada fila mirando un conjunto de filas vecinas —su
ventana— sin agrupar: la tabla conserva todas sus filas y gana una columna con el cálculo.

## La idea

`GROUP BY` responde «¿cuál es la facturación media por ciudad?» y devuelve una fila por ciudad.
Pero muchas preguntas reales no son así: «para cada pedido, ¿cuánto llevo facturado hoy acumulado
en esta ciudad?», «¿cuánto facturó el pedido anterior de este cliente?», «¿en qué puesto queda
este producto dentro de su categoría?». En todas ellas quieres el detalle **y** el resumen en la
misma fila. `GROUP BY` no puede: al agrupar destruye las filas de detalle.

La ventana sí. La imagen útil es una clase de alumnos: `GROUP BY clase` te da la nota media de
cada clase en una fila; con una ventana pones junto a cada alumno la media de *su* clase, la nota
del alumno anterior en la lista y su puesto en el ranking, y el alumno sigue ahí. En pandas el
equivalente mental es `groupby(...).transform(...)` frente a `groupby(...).agg(...)`: `agg`
colapsa, `transform` devuelve algo del tamaño del original (ver
[[pandas-agrupaciones-y-joins|pandas: agrupaciones y uniones]]).

Toda ventana tiene tres piezas, y cada una responde a una pregunta distinta:

1. **`PARTITION BY`** — ¿entre quiénes compito? Corta la tabla en grupos independientes. Sin
   partición, la ventana es la tabla entera.
2. **`ORDER BY`** — ¿en qué orden? Define qué significa «anterior», «acumulado» o «primero».
   Donde no hay orden no hay vecinos.
3. **El marco** — ¿qué filas exactas entran en el cálculo? Por defecto, con `ORDER BY`, el marco
   es «desde el principio de la partición hasta la fila actual, incluidos sus empates».

Los usos que aparecen una y otra vez:

- **Ranking:** `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`.
- **Comparación con vecinos:** `LAG` (fila anterior), `LEAD` (siguiente), diferencias y variaciones
  porcentuales.
- **Acumulados:** total corrido por día, mes o cliente.
- **Medias móviles:** ventanas de 3, 7 o 30 filas, la base de cualquier suavizado.
- **Cuota sobre el total:** la parte dividida entre el total de su partición, sin necesidad de
  una segunda consulta.
- **Deduplicar:** `ROW_NUMBER() OVER (PARTITION BY clave ORDER BY fecha DESC)` y quedarse con
  `rn = 1` es el idioma estándar para «la última versión de cada fila».

La pega es el coste. Una ventana casi siempre obliga al motor a **ordenar** por las claves de
partición y orden: es trabajo en memoria y, si el conjunto no cabe, en disco (ver
[[sql-indices-y-planes|índices y planes]]). Un `ORDER BY` dentro de la ventana que no aprovecha
ningún índice puede ser la diferencia entre un informe que tarda un segundo y otro que tarda un
minuto, aunque la consulta devuelva las mismas 500 filas.

## Definición formal

La forma general es:

```
funcion(args) OVER (PARTITION BY p ORDER BY o [marco])
```

- **Sin `OVER`**, la función es un agregado normal y colapsa filas. **Con `OVER`**, se calcula sin
  colapsar: el resultado tiene exactamente las mismas filas que la entrada.
- `PARTITION BY p`: se evalúa de forma independiente en cada grupo definido por `p`. Si se omite,
  la partición es toda la tabla. `OVER ()` es una ventana vacía, válida para totales globales.
- `ORDER BY o`: orden dentro de cada partición. Es obligatorio para las funciones de ranking y
  para `LAG`/`LEAD`; sin él, el resultado de una acumulativa depende de un orden no especificado.
- **Marco:** `ROWS` cuenta filas físicas, `RANGE` cuenta filas por su valor en el `ORDER BY`
  (los empates entran juntos) y `GROUPS` cuenta grupos de empate. Los límites son
  `UNBOUNDED PRECEDING`, `n PRECEDING`, `CURRENT ROW`, `n FOLLOWING` y `UNBOUNDED FOLLOWING`.
  El defecto con `ORDER BY` es `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; sin
  `ORDER BY` es toda la partición.

Funciones de ranking, con `n` filas empatadas en el mismo valor:

- `ROW_NUMBER()` numera 1, 2, 3, 4… sin repetir números: los empates se rompen por un criterio
  arbitrario si el `ORDER BY` no es único.
- `RANK()` da 1, 2, 2, 4: los empates comparten puesto y el siguiente salta.
- `DENSE_RANK()` da 1, 2, 2, 3: los empates comparten puesto y no hay huecos.

`LAG(x, k, defecto)` devuelve el valor de `x` en la fila `k` posiciones anterior dentro de la
partición (`k` = 1 si se omite) y `defecto` (nulo si se omite) cuando esa fila no existe.
`LEAD` hace lo mismo hacia delante.

**Las funciones de ventana se evalúan después de `WHERE`, `GROUP BY` y `HAVING`, y antes de
`ORDER BY` y `LIMIT`.** Eso tiene una consecuencia directa: no puedes filtrar por una función de
ventana en el `WHERE`, porque cuando el `WHERE` se evalúa la ventana aún no existe. Para filtrar
por `ROW_NUMBER` hay que envolver la consulta en una CTE o subconsulta y filtrar fuera.

## Ejemplo

Cuatro ventas con una fecha repetida, que es donde se ve el detalle importante:

```
fecha       importe
2024-01-01     10
2024-01-02     20
2024-01-02     30
2024-01-03     40
```

Calculando el acumulado de dos formas sobre la misma tabla:

| fecha | importe | acumulado con RANGE (defecto) | acumulado con ROWS |
| --- | --- | --- | --- |
| 2024-01-01 | 10 | 10 | 10 |
| 2024-01-02 | 20 | 60 | 30 |
| 2024-01-02 | 30 | 60 | 60 |
| 2024-01-03 | 40 | 100 | 100 |

La primera fila del 2 de enero vale 60 con el marco por defecto: `RANGE` incluye **todo el grupo
de empate**, es decir las dos ventas de ese día (10 + 20 + 30). Con `ROWS` vale 30, porque solo
suma las filas que ya han pasado una a una. Las dos cifras son «correctas» según lo que hayas
pedido, pero si comparas dos informes hechos por personas distintas y uno usó el defecto y otro
`ROWS`, la discrepancia del 2 de enero es exactamente esto. La media móvil de 3 filas da 10,00 /
15,00 / 20,00 / 30,00, y `LAG(importe)` da nulo en la primera fila porque ahí no hay venta
anterior.

## Código

```sql verificable
-- La misma ventana con RANGE (defecto) y con ROWS: solo cambia el marco.
CREATE TABLE ventas (fecha DATE, importe INTEGER);

INSERT INTO ventas VALUES
    ('2024-01-01', 10),
    ('2024-01-02', 20),
    ('2024-01-02', 30),
    ('2024-01-03', 40);

SELECT fecha,
       importe,
       SUM(importe) OVER (ORDER BY fecha) AS acumulado_rango,
       SUM(importe) OVER (ORDER BY fecha
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado_filas,
       ROUND(AVG(importe) OVER (ORDER BY fecha
                                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS media_movil_3,
       LAG(importe) OVER (ORDER BY fecha) AS importe_anterior
FROM ventas
ORDER BY fecha, importe;
```

```text
fecha | importe | acumulado_rango | acumulado_filas | media_movil_3 | importe_anterior
2024-01-01 | 10 | 10 | 10 | 10.0 | None
2024-01-02 | 20 | 60 | 30 | 15.0 | 10
2024-01-02 | 30 | 60 | 60 | 20.0 | 20
2024-01-03 | 40 | 100 | 100 | 30.0 | 30
```

```python verificable
import duckdb

con = duckdb.connect()
con.sql("""
    CREATE TABLE estados (cliente VARCHAR, fecha DATE, plan VARCHAR);
    INSERT INTO estados VALUES
        ('Ana',   DATE '2024-01-10', 'basico'),
        ('Ana',   DATE '2024-02-01', 'pro'),
        ('Luis',  DATE '2024-01-05', 'pro'),
        ('Luis',  DATE '2024-01-20', 'basico'),
        ('Marta', DATE '2024-03-02', 'pro');
""")

# ROW_NUMBER numera dentro de cada particion y no colapsa nada: se filtra fuera.
# Es el idioma estandar para quedarse con la ultima fila de cada clave.
ultimo = con.sql("""
    SELECT cliente, plan FROM (
        SELECT cliente, plan,
               ROW_NUMBER() OVER (PARTITION BY cliente ORDER BY fecha DESC) AS rn
        FROM estados
    )
    WHERE rn = 1
    ORDER BY cliente
""").fetchall()

print(" ".join(f"{cliente}:{plan}" for cliente, plan in ultimo))
# -> Ana:pro Luis:basico Marta:pro
```

## Errores típicos

- **Filtrar por una función de ventana en el `WHERE`.** `WHERE ROW_NUMBER() OVER (...) = 1` da
  error porque la ventana se calcula después del `WHERE`. Envuélvela en una CTE y filtra en la
  consulta de fuera, como en el ejemplo de código.
- **Confundir `RANK`, `DENSE_RANK` y `ROW_NUMBER`.** Con dos empates en cabeza, `RANK` da 1, 1, 3
  y `DENSE_RANK` da 1, 1, 2. Si después filtras por «el puesto 2», obtienes cosas distintas.
  `ROW_NUMBER` además rompe los empates de forma arbitraria: si usas `rn = 1` para deduplicar y no
  ordenas por una clave única, la fila elegida puede cambiar entre ejecuciones.
- **Olvidar `PARTITION BY`.** Sin partición, el acumulado o el ranking se calculan sobre toda la
  tabla. Es un error silencioso: la consulta corre, devuelve números plausibles y el total
  acumulado de cada cliente incluye a todos los demás.
- **Dar por hecho `ROWS` cuando el defecto es `RANGE`.** Con fechas repetidas (varias ventas el
  mismo día) los acumulados no coinciden, y con `ORDER BY` no único el resultado depende del
  criterio de desempate. Escribe el marco explícito siempre que el resultado vaya a un informe.
- **Usar `LAG` sin `ORDER BY` o con un orden no determinista.** «La fila anterior» solo significa
  algo si el orden está fijado; con empates, el motor puede devolver cualquiera de las dos filas y
  el resultado cambia de una ejecución a otra.
- **Calcular la media móvil con `AVG` sobre la partición entera.** `AVG(x) OVER (PARTITION BY ...)`
  da la media de todo el grupo en cada fila, no una media móvil. Para que se mueva hace falta el
  marco de filas; para ventanas de tiempo real (30 días) la cuenta de filas no es lo mismo que la
  cuenta de días, y faltarán filas en los huecos.

:::practica
enunciado: En `pagos(cliente, fecha, importe)`: Ana pagó 10 el 2024-01-01 y 30 el 2024-01-15; Luis, 20 el 2024-01-03 y 5 el 2024-01-20. Escribe la consulta que devuelva, para cada pago, el importe del pago anterior del mismo cliente y la diferencia entre ambos, ordenada por cliente y fecha.
pista: Es un `LAG(importe)` con `PARTITION BY cliente` y `ORDER BY fecha`; en el primer pago de cada cliente el resultado es nulo.
solucion: `SELECT cliente, fecha, importe, LAG(importe) OVER (PARTITION BY cliente ORDER BY fecha) AS anterior, importe - LAG(importe) OVER (PARTITION BY cliente ORDER BY fecha) AS diferencia FROM pagos ORDER BY cliente, fecha`. Salen cuatro filas: Ana 10 y nulo, luego 30 con anterior 10 y diferencia 20; Luis 20 y nulo, luego 5 con anterior 20 y diferencia -15. La partición reinicia la cuenta en cada cliente.
:::

## Comprueba que lo sabes

:::quiz
p: Con las cuatro ventas del ejemplo, ¿por qué el acumulado del primer 2 de enero vale 60 con el marco por defecto y 30 con ROWS?
o: Porque con RANGE los empates del ORDER BY entran juntos y con ROWS solo entran las filas ya recorridas
o: Porque ROWS ignora la primera fila de la partición
o: Porque el marco por defecto es el total de la partición
a: 1
e: El marco por defecto con ORDER BY es RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, y RANGE trata como iguales todas las filas con el mismo valor de orden: las dos del 2 de enero. ROWS avanza fila a fila. El defecto no es la partición entera; eso ocurre solo cuando no hay ORDER BY.
:::

:::quiz
p: Quieres quedarte con la última fila de cada cliente según la fecha. ¿Dónde va el filtro rn = 1?
o: En el WHERE de la misma consulta, junto al ROW_NUMBER
o: En una consulta externa (CTE o subconsulta) que envuelva el cálculo de la ventana
o: En el HAVING, porque rn es un agregado
a: 2
e: Las funciones de ventana se evalúan después del WHERE y del HAVING, así que no puedes filtrar por ellas en ese nivel. Se calculan en una consulta interna y se filtran en la externa. rn tampoco es un agregado: cada fila conserva su número.
:::

:::aviso
Las ventanas obligan a ordenar. Si la consulta va sobre millones de filas, comprueba el plan: un
`ORDER BY` que no se apoya en un índice puede dominar el tiempo total aunque el `SELECT` solo
devuelva cien filas. Y si la tabla está particionada por fecha, añade la fecha como primera
columna de `PARTITION BY` para que el motor pueda trabajar por particiones en lugar de reordenar
todo.
:::
