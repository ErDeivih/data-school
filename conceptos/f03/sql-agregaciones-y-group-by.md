---
id: sql-agregaciones-y-group-by
titulo: "SQL: agregaciones y GROUP BY"
fase: 3
nivel: básico
rutas: [de, ds]
prerequisitos: [sql-select-y-filtros]
tags: [sql, agregacion, group-by]
resumen: Partir la tabla en montones que comparten una clave y resumir cada montón en una fila; donde va cada filtro y por qué los nulos cambian la media.
fuentes: ["Garcia-Molina, Ullman y Widom (2008), 'Database Systems: The Complete Book'"]
---

## En una frase

Una agregación convierte muchas filas en una: `GROUP BY` decide qué filas van juntas, las
funciones de agregado (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) resumen cada montón y `HAVING`
descarta los montones que ya no te interesan.

## La idea

Imagina una caja de facturas. Si te piden «cuánto se ha facturado en total», sumas todas y ya
está. Si te piden «cuánto por ciudad», no puedes sumar en línea: primero **separas las facturas
en montones** —uno por ciudad— y después sumas cada montón por separado. Eso es exactamente
`GROUP BY ciudad`: partir la tabla en grupos que comparten el valor de esa columna y devolver
**una fila por grupo** en lugar de una fila por dato.

La consecuencia importante se ve en el grano de la salida: si `pedidos` tiene 6 filas y agrupas
por ciudad con 3 ciudades distintas, el resultado tiene 3 filas. Y cada columna del `SELECT` tiene
que ser una de las claves del grupo o un resumen del grupo: dentro de un grupo hay 2, 20 o 2.000
filas, así que `importe` sin agregar no es «el importe», son todos a la vez. PostgreSQL, SQL
Server y Oracle devuelven un error si la incluyes; MySQL solo la acepta si desactivas
`ONLY_FULL_GROUP_BY`, y entonces te da un valor cualquiera del grupo.

El orden en que el motor piensa la consulta explica dónde va cada filtro:

1. `FROM` y `JOIN`: se arma la tabla de trabajo.
2. `WHERE`: se descartan **filas** antes de agrupar. Aquí no puedes usar `SUM` ni `COUNT`,
   porque todavía no existen.
3. `GROUP BY`: se forman los montones.
4. Los agregados del `SELECT` resumen cada montón.
5. `HAVING`: se descartan **grupos** ya resumidos. Aquí sí puedes usar agregados.
6. `ORDER BY` y `LIMIT`.

Y un matiz que explica la mitad de las medias mal calculadas: **los agregados ignoran los
nulos**. `COUNT(*)` cuenta filas; `COUNT(importe)` cuenta filas donde `importe` no es nulo; `SUM`
y `AVG` se saltan los nulos. Por eso `AVG(importe)` no es `SUM(importe) / COUNT(*)` en cuanto hay
un hueco: un nulo significa «no lo sé», y sustituirlo por cero hunde la media.

## Definición formal

Sea una tabla de `n` filas y `k` expresiones de agrupación `c₁, …, cₖ` (columnas o funciones de
columnas). `GROUP BY c₁, …, cₖ` define una **partición** de las `n` filas: dos filas caen en el
mismo grupo si y solo si coinciden en *todas* las claves. El resultado tiene una fila por grupo.
Sin `GROUP BY`, toda la tabla es un único grupo y el resultado tiene una sola fila.

Con `G` un grupo y `x` una columna numérica:

- `COUNT(*)` = número de filas de `G`.
- `COUNT(x)` = número de filas de `G` en las que `x` no es nulo.
- `SUM(x)` = Σᵢ∈G xᵢ, sumando solo los valores no nulos.
- `AVG(x)` = `SUM(x) / COUNT(x)`: divide entre los valores presentes, no entre las filas.
- `MIN(x)` y `MAX(x)` = extremos del grupo, ignorando los nulos.
- `COUNT(DISTINCT x)` = número de valores distintos **no nulos** de `x` dentro del grupo.

`HAVING condición` filtra grupos: se evalúa después de agregar y su condición puede contener
agregados. `WHERE` es su hermano pequeño y se evalúa antes: filtra filas y no admite agregados.

Los agregados filtrados permiten resumir un subconjunto dentro del mismo grupo sin partir el
grupo en dos:

:::formula
SUM(x) FILTER (WHERE c)  ≡  SUM(CASE WHEN c THEN x END)
:::

Los nulos forman un único grupo entre ellos, cosa que choca con la intuición de `= NULL`, que
nunca es verdadero.

## Ejemplo

Tabla `ventas` con 6 pedidos y su importe en euros:

```
id  ciudad   importe
1   Madrid    75,00
2   Madrid   150,00
3   Sevilla   25,00
4   Sevilla  400,00
5   Bilbao    30,00
6   Bilbao     NULL
```

Agrupando por `ciudad`:

| ciudad | COUNT(*) | COUNT(importe) | SUM(importe) | AVG(importe) |
| --- | --- | --- | --- | --- |
| Madrid | 2 | 2 | 225,00 | 112,50 |
| Sevilla | 2 | 2 | 425,00 | 212,50 |
| Bilbao | 2 | 1 | 30,00 | 30,00 |

Tres cosas que conviene mirar despacio:

- Bilbao tiene 2 filas, pero `COUNT(importe)` vale 1: el nulo no cuenta.
- El `AVG` de Bilbao es 30,00 / 1 = 30,00, no 30,00 / 2 = 15,00. Si el hueco fuera un cero, la
  media de esa ciudad sería 15,00 y la conclusión cambiaría por completo.
- En el total, `SUM(importe)` = 680,00 sobre 5 importes presentes da una media global de 136,00;
  680,00 / 6 = 113,33 es el importe medio **por pedido**. Son dos preguntas distintas.

Con `HAVING SUM(importe) > 100` se quedan Sevilla (425,00) y Madrid (225,00), y Bilbao
desaparece. Ese filtro no puede ir en el `WHERE`: `SUM` todavía no existe cuando se evalúa el
`WHERE`, y el motor te dará un error de agregado no permitido.

## Código

```sql verificable
-- Una agregacion minima: una fila por ciudad y solo los grupos que facturan mas de 100.
CREATE TABLE ventas (id INTEGER, ciudad VARCHAR, importe DECIMAL(10,2));

INSERT INTO ventas VALUES
    (1, 'Madrid',   75.00),
    (2, 'Madrid',  150.00),
    (3, 'Sevilla',  25.00),
    (4, 'Sevilla', 400.00),
    (5, 'Bilbao',   30.00),
    (6, 'Bilbao',   NULL);

SELECT ciudad,
       COUNT(*)               AS pedidos,
       COUNT(importe)         AS con_importe,
       SUM(importe)           AS facturado,
       ROUND(AVG(importe), 2) AS ticket_medio
FROM ventas
GROUP BY ciudad
HAVING SUM(importe) > 100
ORDER BY facturado DESC;
```

```text
ciudad | pedidos | con_importe | facturado | ticket_medio
Sevilla | 2 | 2 | 425.00 | 212.5
Madrid | 2 | 2 | 225.00 | 112.5
```

```python verificable
import duckdb

con = duckdb.connect()
con.sql("""
    CREATE TABLE ventas (ciudad VARCHAR, importe DECIMAL(10,2));
    INSERT INTO ventas VALUES
        ('Madrid',  75.00), ('Madrid', 150.00),
        ('Sevilla', 25.00), ('Sevilla', 400.00),
        ('Bilbao',  30.00), ('Bilbao',  NULL);
""")

filas, con_importe, total, media = con.sql(
    "SELECT COUNT(*), COUNT(importe), SUM(importe), AVG(importe) FROM ventas"
).fetchone()

# COUNT(*) cuenta filas; los agregados de importe se saltan el nulo.
print(f"filas {filas}  con_importe {con_importe}  total {total}  media {media:.2f}")
# -> filas 6  con_importe 5  total 680.00  media 136.00

# La media por pedido (todos) no es la media por importe presente.
por_pedido = con.sql("SELECT ROUND(SUM(importe) / COUNT(*), 2) FROM ventas").fetchone()[0]
print(f"media por pedido {por_pedido}")   # -> media por pedido 113.33
```

## Errores típicos

- **Poner en el `SELECT` una columna que no está en el `GROUP BY` ni dentro de un agregado.**
  En `SELECT ciudad, importe FROM ventas GROUP BY ciudad`, ¿qué importe sale si Madrid tiene dos?
  El motor no lo sabe: la columna va en el `GROUP BY` o dentro de un agregado, y si quieres todas
  las filas, no agrupes.
- **Filtrar agregados en el `WHERE`.** `WHERE SUM(importe) > 100` falla porque los agregados se
  calculan después. La condición sobre un agregado va en `HAVING`, y las condiciones sobre
  filas sueltas van en `WHERE`: ponerlas en `HAVING` funciona pero agrupa filas que luego
  descarta, y es más lento.
- **Confundir `COUNT(*)` con `COUNT(columna)`.** Con columnas que admiten nulos dan números
  distintos, y la diferencia es justo la información que buscabas. Para «cuántos pedidos hay»
  usa `COUNT(*)`; para «cuántos tienen importe informado», `COUNT(importe)`.
- **Suponer que `AVG(x)` es `SUM(x) / COUNT(*)`.** Solo coinciden si no hay nulos. Cuando
  compares medias de dos grupos, comprueba antes cuántos valores faltan en cada uno: un grupo
  con el 40 % de nulos puede tener una media preciosa calculada sobre muy pocos casos.
- **Tratar el nulo como cero.** `COALESCE(importe, 0)` cambia la media y el conteo. Si el nulo
  significa «no se informó», déjalo nulo y reporta `COUNT(x)` junto a `AVG(x)`; si significa
  «cero unidades», el problema está en el origen, que guarda dos cosas distintas en el mismo
  sitio.
- **Agrupar después de unir y multiplicar filas.** Un `JOIN` que no es 1:1 duplica filas y los
  `SUM` salen inflados, a veces al doble sin que se note. Es el error clásico de
  [[sql-joins|las uniones]]: agrupa por el grano correcto y comprueba el número de filas antes y
  después del `JOIN`.

:::practica
enunciado: Tabla `pedidos(id, cliente, ciudad, importe)` con (1, Ana, Madrid, 100), (2, Ana, Madrid, 50), (3, Luis, Sevilla, 200), (4, Luis, Sevilla, 300) y (5, Marta, Madrid, 80). Escribe la consulta que dé, por ciudad, pedidos, clientes distintos y total facturado, solo con las ciudades que pasan de 250 euros y ordenada por total descendente.
pista: Los resúmenes van en el `SELECT` con `COUNT(*)`, `COUNT(DISTINCT ...)` y `SUM(...)`; el filtro sobre el total es un `HAVING`, no un `WHERE`.
solucion: `SELECT ciudad, COUNT(*) AS pedidos, COUNT(DISTINCT cliente) AS clientes, SUM(importe) AS total FROM pedidos GROUP BY ciudad HAVING SUM(importe) > 250 ORDER BY total DESC`. Madrid suma 100 + 50 + 80 = 230 con dos clientes distintos, Ana y Marta; Sevilla, 200 + 300 = 500 con uno, Luis. El `HAVING` descarta Madrid y deja una sola fila: Sevilla, 2 pedidos, 1 cliente, 500 euros.
:::

## Comprueba que lo sabes

:::quiz
p: En la tabla de ventas del ejemplo, Bilbao tiene dos pedidos y uno de ellos con importe nulo. ¿Cuánto vale AVG(importe) para Bilbao?
o: 15,00, porque es 30,00 dividido entre las dos filas
o: 30,00, porque AVG divide entre los valores no nulos, que aquí es uno
o: NULL, porque en el grupo hay un nulo
a: 2
e: AVG ignora los nulos y divide entre los valores presentes: 30,00 / 1 = 30,00. La opción 1 describe SUM(x) / COUNT(*), que es otra pregunta. La opción 3 sería cierta solo si todos los valores del grupo fueran nulos.
:::

:::quiz
p: ¿Por qué WHERE SUM(importe) > 100 no funciona y HAVING SUM(importe) > 100 sí?
o: Porque WHERE solo admite comparaciones con comillas
o: Porque el WHERE se evalúa fila a fila antes de agrupar, cuando la suma del grupo todavía no existe
o: Porque HAVING es más rápido que WHERE en cualquier consulta
a: 2
e: El orden lógico es FROM, WHERE, GROUP BY, agregados, HAVING. Cuando se evalúa el WHERE aún no hay grupos ni sumas. La tercera opción es falsa: WHERE suele ser más barato porque descarta filas antes de agrupar, y por eso conviene poner ahí todo lo que no dependa de un agregado.
:::

:::trampa
Un `NULL` en la columna de agrupación no desaparece: todos los nulos forman un grupo propio en
la salida. Si agrupas 10.000 pedidos por provincia y 300 no tienen provincia informada, verás
una fila con la provincia vacía que se lleva el 3 % de los pedidos (y la facturación que sumen
esos 300, que no tiene por qué ser el 3 % del total). Ignorarla es fácil y es un error:
ese grupo suele ser el que revela un problema de captura en el formulario de origen.
:::
