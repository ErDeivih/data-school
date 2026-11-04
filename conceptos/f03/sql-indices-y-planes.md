---
id: sql-indices-y-planes
titulo: "SQL: índices y planes"
fase: 3
nivel: avanzado
rutas: [de, ds]
prerequisitos: [sql-select-y-filtros, sql-joins]
tags: [sql, indices, rendimiento, explain]
resumen: Por qué una consulta que devuelve 20 filas tarda un minuto: qué hace un índice, cuándo el motor lo ignora y cómo leer el plan de ejecución.
fuentes: ["Winand (2012), 'SQL Performance Explained'", "Garcia-Molina, Ullman y Widom (2008), 'Database Systems: The Complete Book'"]
---

## En una frase

Un índice es una estructura ordenada que el motor mantiene junto a la tabla para encontrar filas
sin leerlas todas, y el plan de ejecución (`EXPLAIN`) es la única forma fiable de comprobar si de
verdad lo ha usado.

## La idea

Piensa en un libro de 800 páginas y en su índice alfabético. Si buscas todas las menciones de
«transacción», sin índice te toca hojear las 800 páginas. Con índice vas a la T, lees tres
números de página y saltas directo a ellos. Nadie discute que el índice es mejor **para esa
pregunta**. Pero si lo que quieres es leerte el libro entero, el índice no solo no ayuda: estorba.
Y hay un precio oculto: cada vez que se añade o se corrige una página, alguien tiene que rehacer
el índice. En una base de datos ese alguien es el motor, en cada `INSERT`, `UPDATE` y `DELETE`.

Eso resume las tres verdades de los índices:

1. **Aceleran las lecturas selectivas.** Poco porcentaje de filas, mucha ganancia.
2. **No ayudan cuando hay que leer casi todo.** Si tu filtro deja pasar el 40 % de la tabla,
   recorrer la tabla de principio a fin suele ser más barato que saltar de índice en índice.
3. **Cuestan en cada escritura y ocupan espacio.** Diez índices sobre una tabla de movimientos
   pueden doblar el tiempo de carga sin que nadie sepa por qué.

El motor decide entre los dos caminos con un **optimizador basado en coste**: consulta sus
estadísticas (cuántas filas hay, cuántos valores distintos, cómo se reparten) y estima cuántas
páginas tendrá que tocar cada alternativa. Esa decisión no es una opinión: queda escrita en el
plan de ejecución. Por eso `EXPLAIN` es la herramienta central de este tema y por eso mirar
«cuánto tarda» sin mirar el plan es adivinar.

La parte contraintuitiva es que **un índice puede existir y no usarse**. Las causas típicas:

- Hay una **función o una operación sobre la columna**: `WHERE YEAR(fecha) = 2024` o
  `WHERE cliente_id + 0 = 123`. El índice está ordenado por `fecha`, no por `YEAR(fecha)`; el
  motor tendría que calcular la función para cada fila y eso es un recorrido completo.
- El patrón empieza por comodín: `LIKE '%gomez'` no puede buscar por el principio del texto.
- La columna tiene **poca selectividad**: un índice sobre un booleano donde el 90 % de las filas
  valen `true` no ahorra nada, porque hay que leer el 90 % de la tabla igualmente.
- El índice es **compuesto y no se usa su prefijo**: un índice `(cliente_id, fecha)` sirve para
  filtrar por `cliente_id` y por `(cliente_id, fecha)`, pero no por `fecha` sola.
- Las **estadísticas están desactualizadas** y el optimizador cree que va a devolver 1 fila cuando
  devuelve un millón.

Y la trampa final: el plan puede decir «índice» y ser un desastre. Un recorrido de índice que
devuelve 200.000 filas obliga a 200.000 lecturas aleatorias de la tabla, y un recorrido
secuencial de esas mismas 200.000 filas puede ser mucho más rápido porque lee en orden. Ver
`SEARCH ... USING INDEX` no es el final de la investigación: hay que mirar cuántas filas estima y
cuántas devuelve de verdad.

## Definición formal

- **Selectividad de una columna:** `s = valores distintos / filas totales`. Vale 1 en un
  identificador único y 0,000002 en un booleano. Cuanto más cerca de 1, más útil es un índice
  para igualdades. Ojo: en la literatura también se llama selectividad a la fracción de filas que
  devuelve un predicado (`filas que cumplen / filas totales`), que es justo lo contrario. Cuando
  alguien dice «esta columna es muy selectiva», pregunta cuál de las dos definiciones usa.
- **Índice B-tree:** árbol equilibrado con las claves ordenadas. Con `N` claves y un abanico de
  `m` punteros por nodo, la altura es `h ≈ log_m(N)`. Con `N` = 1.000.000 y `m` = 200,
  `200³ = 8.000.000`, así que la altura es 3: tres lecturas de nodo para llegar a la clave. Un
  recorrido completo de esas mismas filas toca todas las páginas de la tabla.
- **Regla del prefijo:** un índice compuesto `(c₁, c₂, …, cₖ)` es utilizable para predicados que
  fijan `c₁`, o `c₁` y `c₂`, y así sucesivamente. No sirve para `c₂` sola.
- **Índice cubriente:** contiene todas las columnas que la consulta necesita (`SELECT` incluido),
  así que el motor responde solo con el índice y no va a la tabla. Es lo que en algunos motores se
  llama *index-only scan*.
- **Coste de una búsqueda:** `h` lecturas del árbol más una lectura por fila devuelta. Si no es
  cubriente, esas lecturas son aleatorias y son la parte cara.
- **`EXPLAIN` frente a `EXPLAIN ANALYZE`:** el primero muestra el plan **estimado** y no ejecuta la
  consulta; el segundo la ejecuta de verdad y añade filas reales, tiempo por nodo y número de
  repeticiones. Las estimaciones se comparan con los datos reales: una desviación grande es la
  pista de que faltan estadísticas o de que el predicado no es el que crees.

Como se lee un plan, en orden:

1. ¿Dónde está el coste más alto? Se lee de dentro hacia fuera, no de arriba abajo.
2. ¿Recorrido completo o búsqueda por índice? Busca `SCAN` o `SEARCH` (o `Seq Scan` e `Index
   Scan`, según el motor).
3. ¿Hay ordenaciones explícitas? Un `SORT` grande suele ser el verdadero culpable.
4. ¿Cuántas filas estima cada nodo y cuántas devuelve?
5. ¿El algoritmo de unión es bucle anidado, hash o combinación ordenada?

## Ejemplo

Una tabla `pedidos` con 1.000.000 de filas y 500 clientes, así que cada cliente tiene 2.000
pedidos de media y `WHERE cliente_id = 123` devuelve unas 2.000 filas:

- **Sin índice:** el motor lee las 1.000.000 de filas (~10.000 páginas a 100 filas por página) y
  descarta todas menos 2.000.
- **Con índice B-tree sobre `cliente_id`:** altura 3, más las 2.000 filas encontradas. El trabajo
  pasa de orden «todas las páginas» a orden «una constante más el resultado».
- **Con `WHERE cliente_id + 0 = 123`:** la misma respuesta, pero vuelve al recorrido completo: la
  suma impide usar el orden del índice.
- **Con `WHERE activo = 1`** y el 90 % de las filas activas: el índice no aporta. El motor lee el
  índice, descubre que casi todas las filas cumplen y acaba recorriendo la tabla; los optimizadores
  modernos eligen directamente el recorrido completo y aciertan.

Mira la diferencia entre las dos primeras listas: no es de milisegundos, es de **cantidad de
trabajo**. Esa es la cifra que se puede razonar sin medir, y la que explica por qué una consulta
que funcionaba en desarrollo con 10.000 filas se arrastra en producción con 50 millones.

## Código

```python verificable
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pedidos (id INTEGER PRIMARY KEY, cliente_id INTEGER, fecha TEXT, importe REAL)")
con.executemany("INSERT INTO pedidos VALUES (?, ?, ?, ?)",
                [(i, i % 500, f"2024-01-{i % 28 + 1:02d}", 10.0 + i % 90) for i in range(20000)])

def plan(sql):
    return [fila[-1] for fila in con.execute("EXPLAIN QUERY PLAN " + sql)][0]

consulta = "SELECT SUM(importe) FROM pedidos WHERE cliente_id = 123"
print("sin indice  :", plan(consulta))   # -> sin indice  : SCAN pedidos

con.execute("CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id)")
print("con indice  :", plan(consulta))
# -> con indice  : SEARCH pedidos USING INDEX idx_pedidos_cliente (cliente_id=?)

# La operacion sobre la columna y el comodin inicial devuelven el plan a un recorrido completo.
print("con funcion :", plan("SELECT SUM(importe) FROM pedidos WHERE cliente_id + 0 = 123"))
# -> con funcion : SCAN pedidos
print("comodin     :", plan("SELECT SUM(importe) FROM pedidos WHERE fecha LIKE '%01-15'"))
# -> comodin     : SCAN pedidos
```

```python verificable
import numpy as np

# Selectividad = valores distintos / filas. Un indice sobre una columna con dos
# valores no ahorra lecturas: la consulta devuelve media tabla de todas formas.
rng = np.random.default_rng(0)
activo = rng.integers(0, 2, size=100_000)          # columna booleana
factura = rng.integers(1, 100_001, size=100_000)   # identificador de factura

print(f"activo   distintos {np.unique(activo).size:>6}  selectividad {np.unique(activo).size / activo.size:.7f}")
# -> activo   distintos      2  selectividad 0.0000200
print(f"factura  distintos {np.unique(factura).size:>6}  selectividad {np.unique(factura).size / factura.size:.1f}")
# -> factura  distintos  63232  selectividad 0.6
```

## Errores típicos

- **Indexarlo todo «por si acaso».** Cada índice se actualiza en cada escritura y ocupa espacio.
  Una tabla de ingesta con doce índices puede cargar cuatro veces más lento que con dos, y el
  optimizador tarda más en elegir. Índice solo para las consultas que existen de verdad.
- **Aplicar una función a la columna indexada.** `WHERE YEAR(fecha) = 2024`, `WHERE UPPER(email) =
  'A@B.COM'` o `WHERE id + 0 = 7` impiden usar el orden del índice. Reescribe como rango
  (`fecha >= '2024-01-01' AND fecha < '2025-01-01'`), normaliza el dato al guardarlo o usa un
  índice funcional si tu motor lo permite.
- **Confiar en `LIKE '%texto'`.** Un comodín al principio no puede usar el orden del índice. Si
  necesitas buscar dentro del texto, usa búsqueda de texto completo o un índice trigrama.
- **Crear el índice compuesto en el orden equivocado.** Un índice `(fecha, cliente_id)` no sirve
  para filtrar solo por `cliente_id`: manda la regla del prefijo. Piensa primero qué columna
  aparece en igualdades y ponla delante.
- **Comparar columnas de tipos distintos.** Si la fecha está guardada como texto y la comparas con
  un número, el motor convierte y el índice deja de aplicarse (o la consulta falla directamente,
  según el motor). Los tipos de la tabla tienen que coincidir con los del predicado.
- **Mirar el plan estimado y creerlo.** Un `EXPLAIN` que estima 1 fila y un `EXPLAIN ANALYZE` que
  devuelve 900.000 significan estadísticas desactualizadas, un predicado con una correlación que el
  optimizador no conoce o una expresión opaca. Ejecuta `ANALYZE` sobre la tabla antes de tocar
  índices.

:::practica
enunciado: La tabla pedidos tiene 4.000.000 de filas (100 por página: 40.000 páginas) y 50.000 clientes. Su índice B-tree sobre cliente_id tiene abanico 200. Calcula cuántas lecturas cuesta WHERE cliente_id = 7 frente al recorrido completo y cuántas quedarían con un índice cubriente (cliente_id, fecha, importe) para sumar el importe.
pista: La altura sale de m^h ≥ N; el coste es esa altura más una lectura por fila devuelta, y un índice cubriente evita las lecturas aleatorias de la tabla.
solucion: 200² = 40.000 es menor que 4.000.000 y 200³ = 8.000.000 lo supera, luego la altura es 3. Cada cliente tiene 4.000.000 / 50.000 = 80 pedidos. Sin índice: 40.000 páginas. Con índice no cubriente: 3 lecturas del árbol más 80 lecturas aleatorias de la tabla, 83. Con índice cubriente: solo las 3 del árbol, porque el importe ya viaja en el índice. La ganancia son esas 80 lecturas aleatorias.
:::

## Comprueba que lo sabes

:::quiz
p: Un índice existe sobre cliente_id, pero la consulta WHERE cliente_id + 0 = 123 no lo usa. ¿Por qué?
o: Porque el índice solo se usa en consultas con ORDER BY
o: Porque el índice está ordenado por cliente_id, no por el resultado de sumarle cero a cliente_id
o: Porque sumar cero cambia el tipo de la columna a texto
a: 2
e: Para usar el orden del índice el motor tendría que calcular cliente_id + 0 en cada fila, y eso equivale a un recorrido completo. Reescribe el predicado sin la operación. No tiene nada que ver con ORDER BY (aunque un índice también puede ahorrar esa ordenación) ni con conversiones de tipo en este caso.
:::

:::quiz
p: ¿Cuándo un recorrido completo de la tabla es mejor que usar un índice?
o: Nunca: si hay índice, el motor siempre debe usarlo
o: Cuando el predicado deja pasar una fracción grande de la tabla, porque las lecturas aleatorias por índice cuestan más que leer en orden
o: Cuando la tabla tiene menos de un millón de filas
a: 2
e: El índice paga una lectura del árbol más una lectura por fila devuelta, y esas lecturas son aleatorias. Si hay que devolver el 40 % de la tabla, leerla entera en orden suele ganar, y el optimizador lo elige. No es cuestión de un umbral fijo de filas: depende de la fracción devuelta, del tamaño de fila y del almacenamiento.
:::

:::quiz
p: Tienes un índice compuesto (cliente_id, fecha). ¿Para cuál de estas consultas NO sirve?
o: WHERE cliente_id = 12
o: WHERE cliente_id = 12 AND fecha >= '2024-01-01'
o: WHERE fecha >= '2024-01-01'
a: 3
e: La regla del prefijo exige que las columnas se usen de izquierda a derecha: cliente_id sola o acompañada de fecha aprovechan el índice; fecha sola no, porque el árbol está ordenado primero por cliente_id. Para esa consulta haría falta otro índice que empiece por fecha.
:::

:::trampa
`EXPLAIN` no ejecuta la consulta; `EXPLAIN ANALYZE` sí, y en un `UPDATE` o un `DELETE` eso
significa que **modifica datos**. Comprueba siempre si el `ANALYZE` va dentro de una transacción
que puedas deshacer antes de lanzarlo sobre producción.
:::
