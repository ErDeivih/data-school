---
id: oltp-vs-olap
titulo: OLTP frente a OLAP
fase: 4
nivel: básico
rutas: [de, core]
prerequisitos: [ciclo-de-vida-del-dato, sql-select-y-filtros, sql-modelado-y-normalizacion]
tags: [bases-de-datos, analitica, transaccional, almacenamiento]
resumen: La base que atiende a la aplicación y la que responde preguntas de negocio tienen formas opuestas; usar una para lo otro acaba en bloqueos y consultas eternas.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit', cap. 1", "Documentación de DuckDB sobre almacenamiento columnar"]
---

## En una frase

OLTP es la base que aguanta miles de operaciones pequeñas por segundo sin perder ninguna;
OLAP es la que resume millones de filas en una consulta enorme, y son dos diseños distintos a
propósito.

## La idea

Imagina la caja de un supermercado y el despacho del jefe de compras. En la caja, cada segundo
importa: pasar un producto, cobrar, imprimir, descontar del inventario, todo en milisegundos. El
jefe de compras hace otra cosa: quiere saber cuánto se vendió de cada familia de producto por
semana durante los últimos tres años, para decidir qué comprar.

Son dos preguntas opuestas. La caja escribe **poco y muchas veces**, siempre sobre una fila
concreta. El despacho lee **muchísimo y pocas veces**, y le da igual tocar un millón de filas
con tal de obtener el resumen. Si pones las dos en la misma base, la consulta del jefe compite
por el disco con las cajas y, en el peor momento, aparecen bloqueos: la caja espera a que
termine un `GROUP BY` de tres años.

Esa es la razón de que existan dos mundos:

- **OLTP** (*Online Transaction Processing*): el sistema de la aplicación. Muchas escrituras y
  lecturas pequeñas, por identificador, con transacciones cortas. Se diseña **normalizado**
  para que cada hecho se guarde una sola vez y no haya contradicciones. Se almacena **por
  filas**, porque al insertar un pedido escribes todas sus columnas de golpe.
- **OLAP** (*Online Analytical Processing*): el sistema analítico. Pocas consultas, enormes,
  con agregaciones y filtros por fecha y categoría. Se diseña **desnormalizado** (esquema en
  estrella) para que la consulta toque pocas tablas y las uniones sean sencillas. Se almacena
  **por columnas**, porque una consulta que suma una sola columna no necesita leer las demás.

El ejemplo clásico de la diferencia está en una consulta concreta: «ventas por mes y tienda del
último año». En OLTP, esa consulta toca una tabla de pedidos con sus líneas, necesita unir
varias tablas normalizadas y compite con las cajas. En un almacén columnar, lee solo tres
columnas (fecha, tienda, importe) y descarta el resto del ancho de la tabla antes de mirarlo.

Y no es solo velocidad: es aislamiento. Analizar sobre la base de producción significa que un
informe pesado puede degradar el servicio que están usando los clientes, y que quien consulta
puede ver datos personales que no necesita. Separar los dos mundos resuelve las dos cosas a la
vez.

Ojo con el matiz: no todo lo que no es OLTP es un almacén enorme. Hay un punto intermedio que
hoy se usa muchísimo: una base **columnar dentro de un solo proceso**, como DuckDB, que
responde consultas analíticas sobre ficheros Parquet en tu portátil sin montar ningún clúster.
Para muchos análisis, eso es todo lo que hace falta.

## Definición formal

| Rasgo | OLTP | OLAP |
| --- | --- | --- |
| Propósito | Operar el negocio | Entender el negocio |
| Operaciones | `INSERT`, `UPDATE`, `DELETE` por clave | `SELECT` con agregación sobre rangos |
| Filas por operación | 1 a decenas | Millones a miles de millones |
| Latencia objetivo | 1 a 50 milisegundos | Segundos a minutos |
| Modelo | Normalizado (3FN) | Estrella o copo de nieve |
| Organización física | Por filas | Por columnas |
| Índices | Muchos, por clave y búsqueda | Pocos: particionado y ordenación |
| Concurrencia | Miles de usuarios a la vez | Decenas de analistas |
| Historicidad | Estado actual (o poco más) | Serie histórica completa |
| Actualización | Constante y en caliente | Por lotes, en ventanas planificadas |

Dos conceptos que explican por qué el diseño físico importa:

- **Localidad por fila**: los valores de una misma fila se guardan juntos. Insertar o leer una
  fila completa es una operación de disco. Es lo que quiere OLTP.
- **Localidad por columna**: los valores de una misma columna se guardan juntos. Leer una
  columna entera es secuencial y rápido, y además se comprime mejor (los valores de una columna
  se parecen entre sí). Es lo que quiere OLAP.

De ahí la regla práctica: **si tu consulta toca pocas columnas de muchas filas, quieres
columnar; si toca todas las columnas de una fila, quieres filas.**

Y de ahí también la razón de bloquear: en un motor por filas, un `UPDATE` de una celda
reescribe la fila entera y toma un bloqueo sobre ella; una consulta analítica que recorre toda
la tabla mantiene bloqueos durante mucho tiempo y hace esperar a las escrituras.

## Ejemplo

Una tienda con 5 millones de pedidos al año y una consulta: «importe total por mes en 2025».

- **En la base de la aplicación (OLTP)**, los importes están en `lineas_pedido` y la fecha en
  `pedidos`. La consulta necesita unir dos tablas y agregar 12 millones de líneas. Sin un
  índice que cubra el rango de fechas, el motor recorre la tabla entera y compite con las
  cajas. Tiempo típico: decenas de segundos, a veces minutos.
- **En el almacén analítico (OLAP)**, hay una tabla de hechos `ventas` particionada por mes con
  las columnas `fecha`, `tienda_id`, `producto_id`, `unidades`, `importe`. La misma pregunta
  lee tres columnas de 12 millones de filas, descarta las particiones de otros años antes de
  tocar datos y agrega en paralelo. Tiempo típico: menos de un segundo.

La diferencia no está en el hardware: está en cuántos bytes hay que leer. En el motor por filas
se leen todas las columnas de cada fila (digamos 120 bytes de ancho) para usar 24; en el
columnar se leen solo esos 24, y comprimidos. Un factor cinco en bytes leídos se convierte en
mucho más en tiempo, porque además el columnar puede paralelizar y usar operaciones vectorizadas.

## Código

```python verificable
# Diferencia medida en una base por filas (SQLite) con medio millon de lineas
import sqlite3
import time

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pedidos (pedido_id INTEGER PRIMARY KEY, estado TEXT)")
con.execute("CREATE TABLE lineas (pedido_id INTEGER, unidades INTEGER, importe REAL)")
con.executemany("INSERT INTO pedidos VALUES (?, ?)",
                [(p, "pagado") for p in range(1, 100001)])
con.executemany("INSERT INTO lineas VALUES (?, ?, ?)",
                [(p, 1 + k % 3, round(10.0 + 3 * k, 2))
                 for p in range(1, 100001) for k in range(5)])
con.commit()

# Lectura por clave: el caso para el que esta disenada una base transaccional
t0 = time.perf_counter()
for p in range(1, 2001):
    con.execute("SELECT estado FROM pedidos WHERE pedido_id = ?", (p,)).fetchone()
t_clave = (time.perf_counter() - t0) / 2000

# Agregacion sobre todo: el caso analitico, en el mismo motor
t0 = time.perf_counter()
total = con.execute("SELECT count(*), round(sum(importe), 2) FROM lineas "
                    "JOIN pedidos USING (pedido_id) WHERE estado = 'pagado'").fetchone()
t_agregado = time.perf_counter() - t0

print("filas en lineas   :", total[0])                       # -> 500000
print("lectura por clave :", round(t_clave * 1e6), "microsegundos")
# La lectura por clave tarda unos pocos microsegundos; la agregacion, unas cien veces mas.
print("agregado de todo  :", round(t_agregado * 1000, 1), "milisegundos")
print("importe total     :", total[1])                       # -> 8000000.0
```

```sql ilustrativo
-- La misma pregunta en un almacen columnar: se leen tres columnas, no la tabla entera
SELECT date_trunc('month', fecha) AS mes,
       tienda_id,
       sum(importe) AS importe,
       sum(unidades) AS unidades
FROM hechos_ventas
WHERE fecha >= DATE '2025-01-01' AND fecha < DATE '2026-01-01'
GROUP BY 1, 2
ORDER BY 1, 2;
```

## Errores típicos

- **Analizar en la base de producción.** El informe pesado bloquea o ralentiza el servicio, y el
  pico de tráfico coincide justo con la hora a la que se te ocurre lanzarlo. Copia a un sistema
  aparte, aunque sea una réplica de lectura.
- **Indexar para todo en OLTP.** Cada índice acelera las lecturas y frena cada `INSERT` y cada
  `UPDATE`. En una tabla con ocho índices, cada escritura mantiene ocho estructuras. Añade
  índices por consultas reales, no por si acaso.
- **Usar la tabla normalizada de la aplicación para BI y llamarlo «una sola fuente de verdad».**
  El analista acabará escribiendo uniones de siete tablas a mano en cada consulta. Ese trabajo
  se hace una vez, en el modelo (estrella), no en cada informe.
- **Creer que un motor columnar sirve para escribir.** Insertar una fila en un almacén columnar
  implica tocar muchas columnas y suele acabar en un fichero nuevo. Los almacenes analíticos se
  cargan por lotes, no a golpe de `INSERT` de la aplicación.
- **Pensar que «tiempo real» exige OLTP.** Muchos paneles «en tiempo real» solo necesitan
  actualizarse cada minuto, y eso se resuelve con micro-lotes. La arquitectura compleja de
  streaming se paga en mantenimiento, no en valor.
- **Medir la velocidad sin mirar los bytes.** Una consulta analítica tarda lo que tarda leer sus
  datos: si lee 40 GB para devolver 12 números, el problema es el diseño de la tabla, no la
  potencia del servidor.
- **Mezclar cargas y luego culpar a la base.** Si el mismo motor hace transacciones y
  analítica, el rendimiento es impredecible por definición, y depurar un incidente se vuelve
  imposible: no sabes qué carga causó qué.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué una consulta analítica es lenta en la base de la aplicación?
o: Porque los discos de la aplicación siempre son más lentos
o: Porque recorre muchas filas y bloquea recursos que necesitan las escrituras pequeñas y frecuentes
o: Porque SQL no permite agregaciones en bases transaccionales
a: 2
e: El problema no es el disco ni el lenguaje: es la carga. Una agregación sobre millones de filas mantiene lecturas y bloqueos durante mucho tiempo, y eso hace esperar a las transacciones cortas que sostienen la aplicación. Se separan las cargas, no se cambia el motor.
:::

:::quiz
p: ¿Qué gana un almacén columnar frente a uno por filas en una consulta que suma el importe de un año?
o: Lee solo la columna del importe (y las que use el filtro) en vez de todas las columnas de cada fila
o: Guarda menos filas, porque descarta las antiguas
o: Comprime las filas repetidas eliminándolas
a: 1
e: Al agrupar los valores por columna, la consulta lee únicamente las columnas que necesita y puede comprimirlas mejor porque los valores de una columna se parecen. No descarta filas ni elimina duplicados: el resultado es el mismo que en el motor por filas.
:::

:::quiz
p: Tienes que decidir el modelo de la tabla de hechos del almacén. ¿Qué eliges y por qué?
o: Normalizado en 3FN, para no repetir información
o: Desnormalizado en estrella, para que las consultas toquen pocas tablas y sean simples
o: Una copia exacta de las tablas de la aplicación, para no perder detalle
a: 2
e: En analítica se prioriza la lectura: el esquema en estrella une la tabla de hechos con dimensiones planas y evita cadenas de uniones. La normalización estricta es una virtud en OLTP (evita contradicciones al escribir) y un lastre al consultar. Copiar las tablas de la aplicación traslada el problema sin resolverlo.
:::

:::nota
«OLAP» no siempre significa un clúster. Una base columnar dentro de un proceso, sobre ficheros
Parquet, resuelve análisis de millones de filas en un portátil. Antes de montar
infraestructura, mide si tu problema cabe ahí.
:::
