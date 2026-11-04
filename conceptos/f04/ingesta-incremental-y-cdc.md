---
id: ingesta-incremental-y-cdc
titulo: Ingesta incremental y CDC
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [etl-vs-elt, batch-vs-streaming, oltp-vs-olap, sql-ventanas]
tags: [cdc, ingesta, incremental, replicacion, borrados]
resumen: Leer solo lo que ha cambiado en vez de copiar la tabla entera: tres formas de hacerlo y por qué la más fiable es leer el registro de transacciones.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11", "Reis & Housley (2022), 'Fundamentals of Data Engineering', cap. 7"]
---

## En una frase

La ingesta incremental copia de la fuente solo las filas que han cambiado desde la última vez;
CDC es la técnica más fiable para conseguirlo, porque en lugar de adivinar comparando tablas lee
el registro de transacciones de la base de datos, donde cada inserción, modificación y borrado ya
está anotado por el propio motor.

## La idea

No vuelves a fotocopiar el archivador entero cada mañana: apuntas las fichas que han cambiado. Eso
es la ingesta incremental, y suena obvio hasta que aparece el primer problema real.

La alternativa ingenua es el **reemplazo completo**: `SELECT *` de la tabla entera cada noche y a
correr. Con 300.000 filas funciona. Con 200 millones tienes tres problemas a la vez: la ventana de
tiempo se hace insoportable, la consulta compite por recursos con la aplicación que factura
([[oltp-vs-olap]]) y, sobre todo, **los borrados desaparecen sin dejar rastro**. Si una fila ya no
está, un `SELECT *` no te dice si se borró o si tu filtro la excluyó.

Hay tres formas de hacerlo incremental, y conviene conocer las tres porque te las vas a encontrar
en ese orden:

**1. Columna de marca de tiempo (`updated_at`).** Lees `WHERE updated_at > ultimo_valor`. Es la
más común y la más frágil. Falla si la aplicación no actualiza esa columna en todos los caminos de
escritura (basta un `UPDATE` manual de un compañero de soporte), si los relojes de los servidores
no están sincronizados, o si una transacción larga que empezó antes se confirma después con una
marca anterior a la que ya leíste. Por eso siempre se deja un margen de solapamiento y se
deduplica al aplicar. Y no captura borrados: una fila eliminada no tiene marca nueva que leer.

**2. Columna autoincremental (`id`).** Lees `WHERE id > ultimo_id`. Es el más barato y el más
seguro de los dos primeros, pero solo sirve para tablas de solo-añadir: eventos, registros de
auditoría, líneas de un log. En cuanto la tabla admite modificaciones, un `UPDATE` no cambia el
`id` y esa fila no vuelve a aparecer nunca.

**3. CDC (change data capture).** Lees el registro de transacciones del motor —el write-ahead log
en PostgreSQL, el binlog en MySQL, el redo log en Oracle—. Ese registro existe ya, porque el motor
lo necesita para recuperarse de un fallo, así que leerlo no añade ninguna consulta sobre las
tablas de producción. Y trae lo que los otros dos no pueden traer: la operación. Cada entrada dice
si fue una inserción, una modificación o un borrado, con el valor anterior y el nuevo.

El precio de CDC es de operación, no de concepto: necesitas permisos de replicación, el formato
del log es propio de cada motor y cambia entre versiones mayores, y hay que resolver la transición
entre la foto inicial de la tabla (el *snapshot*) y el flujo de cambios que empieza a llegar. Esa
transición es la parte donde se pierden o se duplican filas en la mayoría de las implantaciones.

En todas las variantes, el destino se actualiza con un `MERGE` por clave primaria, no con un
`INSERT`. Esa es la diferencia entre un pipeline que aguanta un reintento y uno que duplica filas
([[idempotencia-y-reintentos]]).

## Definición formal

Sea `S` la tabla origen, `D` la tabla destino, `K` su clave primaria y `L` la posición dentro del
registro de transacciones (en PostgreSQL se llama LSN, en Oracle SCN; la idea es la misma: un
número que crece y ordena todos los cambios).

Un flujo CDC es una secuencia ordenada de registros, cada uno con la forma
`(L, op, K, antes, despues)`, donde `op` toma los valores `I` (inserción), `U` (modificación),
`D` (borrado) y `R` (lectura del snapshot inicial).

- **Reemplazo completo:** `D ← S`. Simple, caro y ciego a los borrados.
- **Incremental por marca de tiempo:** `D ← D ∪ { s ∈ S : s.updated_at > u }`, con `u` el mayor
  `updated_at` ya procesado. Requiere que `updated_at` crezca de forma monótona, cosa que no está
  garantizada.
- **CDC:** `D ← merge(D, { c : c.L > u })`, con `u` el mayor `L` aplicado.

:::formula
D ← merge(D, { c : c.L > u })   con   u = max(L aplicado)
:::

Propiedades que hay que exigirle al `merge`:

- **Idempotencia:** aplicar dos veces un cambio con la misma `L` deja `D` igual. Se consigue con
  `MERGE` o `UPSERT` por `K`; nunca con `INSERT`.
- **Orden por clave:** los cambios de una misma `K` se aplican en orden creciente de `L`. Si dos
  actualizaciones de la misma fila se aplican al revés, el destino se queda con el valor antiguo.
  Puedes paralelizar entre claves, jamás dentro de una clave.
- **Borrados explícitos:** un registro con `op = D` se traduce en `DELETE` sobre `D`, o en una
  marca `_deleted = true` si necesitas conservar la historia. Ignorarlo deja filas fantasma que
  siguen sumando en los informes.

Y una restricción física que decide si el sistema es recuperable: la **retención del log**
(`log_retention`). Es cuánto tiempo conserva el motor los segmentos del registro de transacciones.
Si tu conector está caído más que eso, los cambios se han perdido y la única salida honrada es
rehacer el snapshot completo.

## Ejemplo

Una tabla `clientes` con tres filas se copia el 1 de marzo:

```
id  nombre  ciudad   updated_at
1   ana     madrid   2024-03-01 08:00
2   luis    sevilla  2024-03-01 08:00
3   marta   bilbao   2024-03-01 08:00
```

Durante el día, la aplicación hace cinco operaciones:

```
hora   operacion
09:12  inserta id=4 (pablo, valencia)
10:40  modifica id=2 -> ciudad = granada
11:05  borra id=3
11:30  modifica id=1 -> nombre = ana maria
11:31  modifica id=4 -> ciudad = alicante
```

El registro de transacciones queda así:

```
LSN   op  id  antes                 despues
1004  I   4   -                     (pablo, valencia)
1017  U   2   ciudad=sevilla        ciudad=granada
1022  D   3   (marta, bilbao)       -
1040  U   1   nombre=ana            nombre=ana maria
1041  U   4   ciudad=valencia       ciudad=alicante
```

- **Con `updated_at > '2024-03-01 08:00'`:** aparecen las filas 1, 2 y 4. La fila 3 no aparece
  porque ya no existe. El destino se queda con **marta en bilbao para siempre**, y ese cliente
  fantasma seguirá contando en los informes hasta que alguien lo note.
- **Con CDC:** se aplican las cinco operaciones en orden de `LSN`. El destino acaba con tres
  filas: id 1 (ana maria, madrid), id 2 (luis, granada) e id 4 (pablo, alicante). La fila 3
  desaparece, que es lo correcto.

Resumen de qué captura cada técnica:

| Técnica | Inserciones | Modificaciones | Borrados | Carga sobre producción |
| --- | --- | --- | --- | --- |
| Marca de tiempo | Sí | Sí, si la aplicación la mantiene | No | Una consulta con filtro |
| Columna autoincremental | Sí | No | No | Una consulta con filtro |
| CDC | Sí | Sí | Sí | Ninguna consulta: lee el log que el motor ya escribe |

## Código

```python verificable
# El mismo cambio real aplicado con marca de tiempo y con CDC.
destino = {1: ("ana", "madrid"), 2: ("luis", "sevilla"), 3: ("marta", "bilbao")}
cambios = [("I", 4, ("pablo", "valencia")),
           ("U", 2, ("luis", "granada")),
           ("D", 3, None),
           ("U", 1, ("ana maria", "madrid"))]

# 1) Con updated_at, el borrado de la fila 3 no genera ninguna marca nueva que leer.
vistos_por_marca = [1, 2, 4]
print("filas que ve updated_at:", len(vistos_por_marca))   # -> filas que ve updated_at: 3
print("la fila 3 sigue en el destino:", 3 in destino)      # -> la fila 3 sigue en el destino: True

# 2) Con CDC, el log trae la operacion y el borrado tambien se aplica.
for op, clave, valor in cambios:
    if op == "D":
        destino.pop(clave, None)
    else:
        destino[clave] = valor

print("filas tras CDC:", len(destino))                     # -> filas tras CDC: 3
print("la fila 3 sigue en el destino:", 3 in destino)      # -> la fila 3 sigue en el destino: False
print("ciudad de la fila 2:", destino[2][1])               # -> ciudad de la fila 2: granada
```

```python verificable
# El merge por clave es idempotente: reprocesar el mismo lote no cambia el resultado.
def aplicar(destino, lote):
    copia = dict(destino)
    for lsn, op, clave, valor in lote:
        if op == "D":
            copia.pop(clave, None)
        else:
            copia[clave] = valor
    return copia

destino = {1: "ana", 2: "luis"}
lote = [(1040, "U", 1, "ana maria"), (1041, "I", 5, "pablo")]

una = aplicar(destino, lote)
dos = aplicar(una, lote)                      # el mismo lote, otra vez

print("idempotente:", una == dos)             # -> idempotente: True
print("claves tras dos pasadas:", sorted(dos))  # -> claves tras dos pasadas: [1, 2, 5]
```

## Errores típicos

- **Confiar en `updated_at` sin margen de solapamiento.** Los relojes de las máquinas no van
  perfectamente sincronizados y una transacción larga puede confirmarse con una marca anterior a
  la última que leíste. Resta siempre un margen (cinco minutos es un punto de partida habitual) y
  deduplica al aplicar.
- **Creer que el incremental por `id` captura modificaciones.** Un `UPDATE` no toca la clave
  autoincremental, así que esa fila no volverá a salir en ningún `SELECT ... WHERE id > u`. Solo
  vale para tablas de solo-añadir.
- **No capturar borrados.** Es el error que hace que los informes no cuadren con la base de datos
  y nadie sepa por qué. O activas CDC, o cambias la aplicación a borrado lógico con una columna
  `deleted_at` que sí puedas leer.
- **Hacer `INSERT` en lugar de `MERGE`.** Con CDC, el mismo cambio puede llegar dos veces por un
  reintento, un reinicio del proceso o un reproceso. Un `INSERT` duplica la fila; un `UPSERT` por
  clave primaria, no ([[idempotencia-y-reintentos]]).
- **Ignorar la retención del log.** Si el conector está caído más tiempo del que el motor conserva
  sus segmentos, los cambios se han perdido de verdad. Hay que vigilar el retraso del conector
  como se vigila cualquier otro acuerdo de nivel de servicio ([[calidad-y-slas]]).
- **Aplicar cambios de la misma clave en paralelo.** El orden por `LSN` importa dentro de cada
  clave. Si dos actualizaciones de la misma fila se aplican desordenadas, el destino conserva el
  valor viejo y parece que el pipeline «a veces falla».

## Comprueba que lo sabes

:::quiz
p: ¿Qué captura CDC que un incremental por marca de tiempo no puede capturar?
o: Los borrados, porque el registro de transacciones anota la operación y el valor anterior
o: Las inserciones rápidas que duran menos de un segundo
o: Los cambios de esquema de la tabla
a: 1
e: El log anota la operación de cada cambio, así que un borrado llega como un registro con op = D y su valor previo. Una fila borrada no tiene marca de tiempo nueva que consultar, por eso se pierde para siempre con el enfoque de updated_at.
:::

:::quiz
p: ¿Por qué el incremental por columna autoincremental no sirve para una tabla que se modifica?
o: Porque los identificadores se reutilizan al borrar filas
o: Porque un UPDATE no cambia el identificador, así que esa fila nunca vuelve a leerse
o: Porque los identificadores grandes no caben en un entero de 32 bits
a: 2
e: El filtro «id mayor que el último visto» solo avanza: cualquier cambio sobre una fila ya leída queda por detrás de la frontera y no aparece nunca. Es un método excelente para tablas de solo-añadir y directamente incorrecto para el resto.
:::

:::quiz
p: ¿Para qué se deja un margen al leer por `updated_at`?
o: Para que la consulta tenga tiempo de ejecutarse
o: Porque una transacción que empezó antes puede confirmarse después con una marca anterior al último valor leído
o: Porque así se leen también las filas borradas
a: 2
e: La marca se asigna cuando la transacción escribe, no cuando se confirma, así que pueden aparecer filas «por detrás» de tu última lectura. El margen las recoge en la siguiente pasada; el precio es releer algunas filas, y por eso el paso de aplicación tiene que ser un UPSERT idempotente.
:::

:::trampa
Un incremental por `updated_at` sin borrados es la causa número uno del clásico «los informes no
cuadran con la base de datos». Comprueba siempre, con una consulta de recuento por día, que el
número de filas del destino sigue el mismo ritmo que el del origen.
:::
