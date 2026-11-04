---
id: evolucion-de-esquema
titulo: Evolución de esquema
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [almacenamiento-de-objetos, parquet-avro-orc, data-lake]
tags: [esquema, compatibilidad, parquet, contratos]
resumen: Cambiar el esquema de una tabla sin romper a quien la lee: qué operaciones son seguras, cuáles exigen coordinación y por qué renombrar es la peor de todas.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 4", "Reis y Housley (2022), 'Fundamentals of Data Engineering', cap. 6"]
---

## En una frase

Evolucionar un esquema es cambiar las columnas de una tabla mientras otros la siguen leyendo: se
puede añadir, renombrar y quitar, pero cada cambio tiene un precio distinto y el único que se paga
siempre es la compatibilidad hacia atrás, porque los datos ya escritos no se pueden reescribir a
la ligera.

## La idea

Piensa en un formulario de almacén. Al principio tiene casillas para `id`, `importe` y `ciudad`.
Al año siguiente el negocio quiere registrar también el canal de venta:

- **Añadir una casilla al final** es barato. Los envíos de antes simplemente no la traen; quien
  rellena formularios nuevos la usa y quien lee los viejos no se entera.
- **Cambiar el nombre de `ciudad` por `localidad`** es caro. Todos los formularios archivados
  dicen `ciudad`, y el lector que busca `localidad` no la encuentra en ninguna caja antigua. No
  hay renombrado de datos ya escritos: el nombre está dentro del fichero.
- **Quitar una casilla** solo funciona cuando compruebas que nadie la sigue rellenando ni leyendo.
  Mientras un solo informe la use, quitarla le rompe el mes.

La clave, y lo que casi nadie explica, es que la compatibilidad depende de **cómo lee el
consumidor**, no solo del cambio. Un lector que accede por **nombre** (`SELECT id, importe, ciudad`)
sobrevive a que le añadan columnas nuevas y a que las reordenen: pide las que conoce y las
encuentra. Un lector que accede por **posición** (`SELECT *` guardado en una tabla con las columnas
en un orden concreto, o un `INSERT INTO ... SELECT *`) se rompe en cuanto el orden cambia o
aparece una columna nueva en medio. En columnar, `SELECT *` no es una comodidad: es un contrato
implícito con el orden de las columnas, y ese contrato no está escrito en ningún sitio.

Hay dos direcciones, y conviene no mezclarlas:

- **Compatibilidad hacia atrás:** el esquema nuevo puede leer los datos escritos con el viejo.
  Es la que necesitas siempre, porque tu tabla acumula meses de ficheros antiguos.
- **Compatibilidad hacia delante:** el esquema viejo puede leer los datos escritos con el nuevo.
  Es la que permite que un consumidor que no ha actualizado su código siga funcionando. Añadir
  una columna opcional la cumple; quitar una columna, no.

Un esquema que cumple las dos se llama **totalmente compatible**, y es el objetivo razonable de
cualquier tabla de la que dependan varios equipos. Los formatos de tabla modernos
-[[lakehouse-y-table-formats|Delta, Iceberg, Hudi]]- permiten declarar el esquema y consultarlo en
un momento del pasado, lo que reduce el riesgo, pero no cambia la lógica: el problema no es la
tecnología, son los lectores que ya existen.

## Definición formal

Sea `S_v` el esquema de la versión `v` de la tabla y `D_v` los datos escritos con él. Se dice que
`S_2` es compatible hacia atrás con `S_1` si toda consulta válida contra `S_1` se puede ejecutar
sobre `D_1` leído con `S_2` y devuelve los mismos valores en las columnas comunes.

:::formula
compatible_hacia_atrás(S_2, S_1)  ⇔  S_2 contiene todas las columnas de S_1, con el mismo tipo
(o uno que admita todos sus valores) y sin volver obligatoria ninguna que fuera opcional
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `S_1` | Esquema con el que se escribieron los datos que ya están en el lago | lista de columnas | Cuantas más columnas tenga, más difícil es que un esquema nuevo las cubra todas |
| `S_2` | Esquema nuevo que quieres publicar | lista de columnas | Si es un superconjunto de `S_1`, la compatibilidad hacia atrás sale gratis |
| `columnas(S)` | Conjunto de nombres de columna del esquema | nombres | Es lo que se compara: los nombres, no las posiciones ni el orden |
| `valor por defecto` | Valor que el motor devuelve cuando la columna no existe en el fichero | del tipo de la columna | Si existe, el nulo o el valor se rellena y el lector antiguo no se entera |
| `nulos añadidos` | Celdas que el motor rellena al unir ficheros de esquemas distintos | número de celdas | Un nulo por columna nueva y por fila antigua; por eso ya no distingues «no había dato» de «no existía la columna» |
| `ventana de lectura` | Tiempo desde el último uso conocido de una columna hasta que te atreves a quitarla | días | Cuanto mayor, más seguro el borrado y más tiempo cargas con la columna; con informes anuales se mide en meses |
:::

Con esto, las operaciones quedan clasificadas sin ambigüedad. `+` significa compatible, `?` que
depende de si el lector accede por nombre o por posición, y `−` que rompe:

| Cambio | Lector v1 (código viejo) | Lector v2 (lee por nombre) | Lector v3 (lee por posición) |
| --- | --- | --- | --- |
| Añadir columna opcional | + | + | + si va al final, − si va en medio |
| Añadir columna con valor por defecto | + | + | + si va al final, − si va en medio |
| Hacer opcional una columna obligatoria | + | + | + |
| Reordenar columnas | + | + | − |
| Ampliar el tipo (entero a decimal) | ? | + | ? |
| Renombrar una columna | − | ? | − |
| Quitar una columna | − | − | − |

:::figura
fichero: evolucion-de-esquema-compatibilidad
pie: Los dos paneles responden a las dos preguntas que hay que hacerse antes de tocar nada. A la izquierda, qué hace cada cambio: casi todo lo que rompe lo hace contra el lector antiguo, y el renombrado rompe incluso al lector nuevo si este accede por posición. A la derecha, que el formato columnar no reescribe el pasado: la columna añadida en marzo no existe en los ficheros de enero y febrero, y quien los lee recibe nulos indistinguibles de un dato ausente.
fuente: figuras/evolucion-de-esquema-1.py
:::

## Ejemplo

Una tabla de ventas con `id`, `importe` y `fecha` recibe un cambio cada trimestre:

| Fecha | Cambio | Qué pasa al leer los ficheros anteriores |
| --- | --- | --- |
| Marzo | Añadir `canal` (opcional) | Los ficheros de enero y febrero devuelven nulo en `canal` |
| Junio | Añadir `descuento` con valor por defecto 0 | Los ficheros antiguos devuelven 0, no nulo: la suma no cambia de significado |
| Septiembre | Renombrar `canal` a `origen` | El informe que lee `canal` deja de ver la columna: se rompe el mismo día |
| Diciembre | Quitar `descuento` | Solo es seguro si ningún informe la lee desde septiembre |

Fíjate en la diferencia entre marzo y junio. El nulo de marzo es ambiguo: no sabes si el cliente no
tenía canal o si el fichero es tan antiguo que la columna no existía. El valor por defecto de
junio evita esa ambigüedad, y por eso es la forma preferida de añadir una columna que luego se
vaya a sumar o a agrupar. Y para el renombrado de septiembre, si de verdad quieres hacerlo, la
secuencia segura es: añadir `origen`, escribir las dos durante un ciclo completo, migrar a los
lectores, y solo entonces quitar `canal`.

## Código

```python verificable
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Enero: el esquema original. Marzo: el mismo esquema mas una columna nueva.
enero = pd.DataFrame({"id": [1, 2], "importe": [10.5, 20.0]})
marzo = pd.DataFrame({"id": [3], "importe": [7.25], "canal": ["web"]})

# El productor no reescribe el fichero viejo: escribe el nuevo con una columna mas.
pq.write_table(pa.Table.from_pandas(enero, preserve_index=False), "enero.parquet")
pq.write_table(pa.Table.from_pandas(marzo, preserve_index=False), "marzo.parquet")

print("columnas de enero:", pq.read_schema("enero.parquet").names)
print("columnas de marzo:", pq.read_schema("marzo.parquet").names)
# La columna nueva no existe en lo ya escrito: no aparece sola al leer un fichero suelto.
try:
    pq.read_table("enero.parquet").column("canal")
except KeyError as exc:
    print("enero.parquet no trae canal:", type(exc).__name__)

# Al unir esquemas distintos, pandas decide por version: o rellena con nulo o se queja.
try:
    print("pandas concatena con nulos:", pd.concat([enero, marzo], ignore_index=True)
          .to_dict(orient="list"))
except Exception as exc:
    print("pandas no concatena:", type(exc).__name__)
# -> columnas de enero: ['id', 'importe']
# -> columnas de marzo: ['id', 'importe', 'canal']
# -> enero.parquet no trae canal: KeyError
# -> pandas concatena con nulos: {'id': [1, 2, 3], 'importe': [10.5, 20.0, 7.25], 'canal': [nan, nan, 'web']}

# Arrow si garantiza el relleno: unir por nombre y poner nulo donde falta la columna.
unido = pa.concat_tables([pa.Table.from_pandas(enero, preserve_index=False),
                          pa.Table.from_pandas(marzo, preserve_index=False)],
                         promote_options="default")
print("arrow si puede:", unido.to_pydict())
# -> arrow si puede: {'id': [1, 2, 3], 'importe': [10.5, 20.0, 7.25], 'canal': [None, None, 'web']}
```

:::claves
- `pq.write_table` escribe **un fichero por tabla** y guarda el esquema dentro del propio
  fichero. No hay catálogo que valide nada: por eso puedes escribir dos ficheros con columnas
  distintas en la misma "tabla" y no te enteras hasta que alguien los lee juntos.
- `pq.read_schema(...).names` devuelve solo los **nombres**, en el orden en que se escribieron.
  Es lo que hay que comparar antes de publicar un cambio: si `names` del esquema nuevo no
  contiene todos los del viejo, la compatibilidad hacia atrás está rota.
- `pd.concat` rellena con `nan` las columnas que faltan en alguno de los DataFrames, y ese
  comportamiento cambia entre versiones: en versiones antiguas lanza un error. El código lo
  captura y lo imprime, así que funciona en ambas.
- `pa.concat_tables(..., promote_options="default")` une por **nombre** y rellena con nulo. Sin
  ese argumento, Arrow exige esquemas idénticos y falla; es el error que aparece al leer una
  carpeta con ficheros de dos generaciones distintas.
- El `try` de `pq.read_table` captura `KeyError` porque pedir una columna que no está en el
  esquema es un error de clave, no un aviso. Es exactamente lo que le pasa a un informe cuando
  alguien quita o renombra una columna: falla en la primera línea, no a mitad del cálculo.
- `1`, `2` y `3` en `id` siguen siendo enteros tras la unión, pero `canal` es de tipo nulo: el
  tipo de una columna que solo existe en parte de los ficheros es el **más general** de los que
  aparecen, y eso puede cambiar el plan de una consulta.
:::

## Errores típicos

- **Renombrar una columna en producción sin avisar.** El nombre está dentro de cada fichero ya
  escrito y no se puede cambiar retroactivamente sin reescribirlo todo. El consumidor que pedía
  el nombre viejo se rompe en la primera línea, y para cuando lo notas ya hay informes a medias.
- **Confundir `SELECT *` con una lectura por nombre.** En columnar, `SELECT *` hereda el orden de
  columnas del esquema. Añadir una columna en medio o reordenar cambia lo que recibe el
  consumidor y puede escribir valores en la columna equivocada sin dar error.
- **Quitar una columna en cuanto dejas de escribirla.** La ventana de seguridad no depende de
  cuándo dejas de producirla, sino de cuándo deja de leerla el último consumidor. Con un informe
  anual, esa ventana se mide en meses, no en días.
- **No distinguir nulo de ausente.** Un nulo por columna nueva se mezcla con los nulos reales.
  Sin un valor por defecto declarado, cualquier media o agrupación posterior cambia de significado
  y nadie sabe por qué.
- **Cambiar el tipo de una columna para "arreglar" un problema de formato.** Pasar un entero a
  texto hace ilegibles las comparaciones numéricas anteriores; ampliar de entero a decimal es
  compatible hacia atrás en algunos motores y en otros no. Los tipos se amplían, no se
  reformatean.

:::practica
enunciado: Un informe mensual lee `id`, `importe`, `canal` y `descuento`. Quieres añadir una columna `origen` y eliminar `descuento`. ¿En qué orden haces los cambios y qué compruebas antes de cada uno?
pista: Añadir es compatible hacia atrás por definición; quitar exige demostrar que nadie lee la columna.
solucion: Primero añades `origen` como columna opcional o con valor por defecto -compatible hacia atrás, ningún lector se entera-. Después dejas pasar al menos un ciclo completo de escritura y actualizas los lectores para que usen `origen` si lo necesitan. Antes de quitar `descuento` consultas el historial de uso del catálogo o el registro de consultas y compruebas que no aparece en ninguna consulta desde hace al menos la ventana de lectura del informe -con un informe mensual, dos meses-. Solo entonces la eliminas, y no en el mismo despliegue que la escritura: si el informe falla, quieres saber cuál de los dos cambios fue.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estos cambios rompe a un consumidor que lee por nombre y solo pide las columnas que ya conocía?
o: Añadir una columna nueva con valor por defecto
o: Reordenar las columnas del esquema
o: Quitar una de las columnas que ese consumidor pide
a: 3
e: Añadir y reordenar son inocuos para quien lee por nombre: encuentra lo que pide donde esté. Quitar una columna que el consumidor pide es el único que lo rompe, porque deja de existir.
:::

:::quiz
p: Llevas dos meses sin escribir la columna `descuento` pero un informe anual la lee cada diciembre. ¿Puedes quitarla?
o: Sí, si llevas dos meses sin escribirla ya no la necesita nadie
o: No: mientras exista un lector que la use, quitarla lo rompe en su próxima ejecución
o: Sí, siempre que el formato de tabla soporte viaje en el tiempo
a: 2
e: La ventana de seguridad la marca el último lector, no el último escritor. El viaje en el tiempo permite consultar la versión antigua, pero no evita que el informe actual falle. Con un lector anual, hay que esperar a que migre.
:::

:::quiz
p: Lees una carpeta con ficheros Parquet de dos generaciones distintas y quieres tratarlos como una sola tabla. ¿Qué usas?
o: `pd.read_parquet` sobre toda la carpeta, que ya une por nombre
o: `pa.concat_tables(..., promote_options="default")`, que une por nombre y rellena con nulo
o: `pd.concat`, que rellena con nulo en todas las versiones
a: 2
e: Arrow garantiza la unión por nombre con relleno de nulos. `pd.concat` es de DataFrames en memoria y su comportamiento cambia entre versiones. Y hay motores que al leer una carpeta entera con esquemas distintos devuelven un tipo unión en vez de columnas, así que conviene comprobar el esquema antes.
:::
