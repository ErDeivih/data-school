---
id: lakehouse-y-table-formats
titulo: Lakehouse y formatos de tabla
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [data-lake, parquet-avro-orc, particionado-y-clustering]
tags: [formatos, transacciones, iceberg, delta]
resumen: Una capa de metadatos sobre Parquet que aporta transacciones, viaje en el tiempo y esquema evolutivo: Delta Lake, Iceberg y Hudi sobre el mismo lago.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

Un **formato de tabla abierto** (Delta Lake, Apache Iceberg, Apache Hudi) es una capa de
metadatos que se apoya en ficheros Parquet y añade lo que un lago de ficheros no tiene:
publicación atómica de cambios, lecturas consistentes, viaje en el tiempo y evolución del
esquema; un **lakehouse** es un lago con esa capa encima y consultas tipo almacén.

## La idea

Un [[data-lake|lago]] de ficheros Parquet tiene un problema de fondo: **no hay transacciones**.
Un proceso escribe 300 ficheros y falla en el 214. ¿Qué ve el analista que consulta esa carpeta
a las 3 de la mañana? Ve 213 ficheros de la partición de hoy y los 300 de ayer: datos
duplicados y una partición a medias que parece completa. Nadie ha roto nada y, sin embargo, el
informe miente.

Los tres problemas concretos:

1. **Publicación no atómica.** «Ya está cargado» no es un estado que el sistema de ficheros
   sepa representar; solo hay bytes escritos o no escritos.
2. **Corregir una fila cuesta reescribir.** Un `UPDATE` sobre 40 filas obliga a reescribir el
   fichero entero donde vivían, y con él la partición, y hay que avisar a todo el mundo de que
   el fichero cambió.
3. **Cada lector improvisa.** El esquema, las particiones y las estadísticas viven en la cabeza
   de quien escribió el proceso, no en un sitio que las herramientas puedan leer.

La solución es la misma que usan las bases de datos desde hace décadas: **separar los datos del
catálogo**. Los ficheros Parquet siguen siendo inmutables y estúpidos; al lado se mantiene un
registro de transacciones que dice qué ficheros forman la tabla ahora mismo, con qué esquema y
con qué particiones.

La analogía es una biblioteca. En un lago de ficheros, cada bibliotecario deja los libros en la
estantería que le parece y avisa a quien puede. En un lakehouse hay un **catálogo central**: se
colocan los libros y, en una sola operación, se actualiza el catálogo. Quien consulta mira el
catálogo, no las estanterías. Y como el catálogo guarda las versiones anteriores, puedes
preguntar «cómo era la biblioteca el martes pasado».

Lo que aporta la capa de metadatos:

- **Commits atómicos.** Un cambio se publica de golpe: o está entero o no está.
- **Aislamiento entre lectores y escritores.** Quien lee ve una *instantánea* coherente, no
  ficheros a medio escribir.
- **Viaje en el tiempo.** Cada instantánea es consultable mientras se conserve en el registro y
  los ficheros no se hayan borrado.
- **Evolución de esquema.** Añadir una columna, renombrarla o ampliar un tipo sin reescribir el
  histórico; los ficheros viejos se leen con nulo en la columna nueva.
- **Particionado oculto y estadísticas.** Las particiones pueden derivarse de la columna (por
  ejemplo `mes(fecha)`) sin que el usuario escriba el valor, y el registro guarda mínimos y
  máximos por fichero para descartar lo que no hace falta leer.
- **Borrados y actualizaciones.** Vía reescritura de ficheros afectados (*copy-on-write*) o vía
  ficheros de borrado (*merge-on-read*).

Los tres formatos resuelven lo mismo con diseños distintos. Delta Lake guarda un registro de
transacciones JSON con puntos de control periódicos en Parquet. Iceberg organiza los metadatos
en un fichero de tabla, una lista de manifiestos y los manifiestos, con particionado oculto y
una especificación independiente del motor. Hudi se apoya en una línea temporal de acciones y
está muy orientado a *upserts* y a ingestas de cambio ([[ingesta-incremental-y-cdc|CDC]]) con
elección entre copy-on-write y merge-on-read. Las diferencias prácticas están en el ecosistema
de motores que los leen, en cómo gestionan la concurrencia y en qué operaciones son más
eficientes; para elegir, mira qué motores usas y quién mantiene el catálogo, no la pegatina.

## Definición formal

Una tabla de este tipo es, formalmente, un **registro de instantáneas**:

- **Instantánea (snapshot) `v`:** el conjunto de ficheros de datos que forman la tabla en la
  versión `v`, más el esquema, la especificación de particiones y las estadísticas.
- **Commit:** una operación atómica que crea la instantánea `v+1` a partir de la `v`, añadiendo
  y quitando ficheros. Es la única forma de modificar la tabla.
- **Fichero vivo:** el referenciado por la instantánea actual. Un fichero que no está en ninguna
  instantánea viva es basura y se puede borrar (*vacuum*).
- **Viaje en el tiempo:** consultar una instantánea anterior `v' < v`, mientras siga existiendo
  y sus ficheros no se hayan eliminado.

:::formula
instantánea v = ficheros_vivos(v) · leer(v) no ve ningún cambio posterior a v
:::

Dos invariantes que hay que respetar para que la magia funcione:

1. **Ningún lector mira los ficheros directamente.** Si un proceso lista la carpeta con el
   sistema de ficheros en vez de leer el registro, verá ficheros a medio publicar y datos
   duplicados. Toda lectura pasa por el formato de tabla.
2. **La retención define el viaje en el tiempo.** El registro guarda versiones durante un
   tiempo limitado (típicamente unos días, configurable). Pasado ese plazo, la compactación de
   metadatos borra las versiones viejas y sus ficheros: el viaje en el tiempo **no** es una
   copia de seguridad.

## Ejemplo

Una tabla con tres instantáneas y ficheros de 100 filas:

| Instantánea | Operación | Añade | Quita | Ficheros vivos | Filas |
| --- | --- | --- | --- | --- | --- |
| v1 | carga inicial | f1, f2, f3 | — | 3 | 300 |
| v2 | actualiza importes de las filas 1 a 100 | f4 | f1 | 3 | 300 |
| v3 | borra los identificadores menores o iguales a 50 | f5 | f4 | 3 | 250 |

Lo importante es lo que **no** cambia: en v2 el número de filas sigue siendo 300, porque una
actualización no añade ni quita registros, solo cambia el contenido de 100 de ellos. Y lo que sí
cambia: `SELECT sum(importe) FROM tabla VERSION AS OF 1` devuelve la suma con los importes
viejos y `VERSION AS OF 2` con los nuevos, sobre la misma tabla física y sin copias.

En v3, el borrado de 50 filas no toca f2 ni f3: solo se reescribe el fichero f4, que contenía
las filas afectadas. Ese es el motivo de que los ficheros deban ser razonablemente grandes: si
tuvieras ficheros de 5 filas, cada operación reescribiría cientos de ellos.

## Código

```python verificable
# Registro de transacciones: cada version anade y quita ficheros, nada se edita en el sitio
snapshots = [
    {"v": 1, "anade": ["f1", "f2", "f3"], "quita": []},
    {"v": 2, "anade": ["f4"], "quita": ["f1"]},   # actualiza las filas 1..100
    {"v": 3, "anade": ["f5"], "quita": ["f4"]},   # borra las filas 1..50
]
# Cada fichero guarda pares (id, importe); f4 es la version actualizada de f1
ficheros = {
    "f1": [(i, i * 10.0) for i in range(1, 101)],
    "f2": [(i, i * 10.0) for i in range(101, 201)],
    "f3": [(i, i * 10.0) for i in range(201, 301)],
    "f4": [(i, i * 12.0) for i in range(1, 101)],
    "f5": [(i, i * 12.0) for i in range(51, 101)],
}

def vivos(version):
    conjunto = set()
    for s in snapshots:
        if s["v"] > version:
            break
        conjunto |= set(s["anade"])       # un commit solo anade y quita referencias
        conjunto -= set(s["quita"])
    return sorted(conjunto)

for v in (1, 2, 3):
    filas = [fila for f in vivos(v) for fila in ficheros[f]]
    total = sum(imp for _, imp in filas)
    print(f"v{v}: {len(vivos(v))} ficheros, {len(filas)} filas, importe {total:.0f}")
# -> v1: 3 ficheros, 300 filas, importe 451500
# -> v2: 3 ficheros, 300 filas, importe 461600
# -> v3: 3 ficheros, 250 filas, importe 446300
```

```python verificable
# Esquema evolutivo: un fichero nuevo anade una columna y los antiguos se leen con nulo
ficheros = {
    "f_antiguo": [{"id": 1, "ciudad": "Madrid"}, {"id": 2, "ciudad": "Sevilla"}],
    "f_nuevo": [{"id": 3, "ciudad": "Bilbao", "segmento": "premium"}],
}
columnas = ["id", "ciudad", "segmento"]      # el esquema de la tabla, no el de cada fichero

filas = [{c: fila.get(c) for c in columnas} for contenido in ficheros.values() for fila in contenido]
print("filas leidas:", len(filas))                                          # -> filas leidas: 3
print("filas sin segmento:", sum(f["segmento"] is None for f in filas))     # -> filas sin segmento: 2
print("columnas del esquema:", ",".join(columnas))                          # -> columnas del esquema: id,ciudad,segmento
```

## Errores típicos

- **Creer que el formato de tabla arregla los ficheros pequeños.** No los arregla: los hace
  visibles y los acumula en el registro. Sin una compactación periódica, el registro acaba con
  miles de ficheros diminutos y la planificación de la consulta se come el tiempo.
- **Confundir el viaje en el tiempo con una copia de seguridad.** La retención de versiones
  caduca y la compactación borra ficheros. Si necesitas recuperación ante desastres, mantén
  copias; el histórico de la tabla es para auditar y reproducir, no para restaurar.
- **Escribir con commits diminutos o con la estrategia equivocada.** Un commit por fila genera
  miles de instantáneas y degrada la planificación: agrupa las escrituras. Y reescribir ficheros
  enteros (copy-on-write) por cada actualización de una ingesta intensa multiplica la escritura;
  con muchos cambios, merge-on-read más compactación programada suele salir mejor.
- **Leer los ficheros saltándose el registro.** Un `ls` o un `spark.read.parquet(ruta)` sobre la
  carpeta de la tabla ve ficheros no publicados y filas borradas. Usa siempre la API del formato
  o del catálogo.
- **Mezclar particionado manual con particionado del formato.** Si un proceso escribe carpetas
  `fecha=2024-01-01/` y el formato deriva sus propias particiones de la columna, acabas con dos
  verdades y con una poda de particiones que no funciona. Elige una y documéntala.
- **Suponer que todos los motores soportan todo.** Cada formato y cada motor tienen coberturas
  distintas de operaciones (borrados, evolución de columnas, planificación). Comprueba las
  operaciones que usas antes de comprometerte.

## Comprueba que lo sabes

:::quiz
p: ¿Qué aporta un formato de tabla como Delta, Iceberg o Hudi sobre un lago de ficheros Parquet?
o: Comprime mejor los ficheros Parquet
o: Un registro de metadatos con instantáneas que permite commits atómicos, lecturas consistentes y viaje en el tiempo
o: Sustituye Parquet por un formato propietario más rápido
a: 2
e: Los ficheros de datos siguen siendo Parquet; lo que cambia es que existe un registro que dice qué ficheros forman la tabla en cada versión. De ahí salen las transacciones, el aislamiento y el histórico. La compresión depende del códec y del orden de los datos, no de la capa de tabla.
:::

:::quiz
p: En la tabla del ejemplo, la instantánea v2 actualiza los importes de 100 filas. ¿Por qué sigue teniendo 300 filas?
o: Porque el UPDATE se queda pendiente hasta la siguiente carga
o: Porque una actualización no cambia el número de filas: quita un fichero y pone otro con el mismo número de registros y valores nuevos
o: Porque el motor duplica las filas antiguas para no perderlas
a: 2
e: El commit quita la referencia a f1 y añade f4, que contiene las mismas 100 filas con importes nuevos. Cambia el contenido, no el cardinal. Las filas antiguas siguen visibles solo si consultas la instantánea v1.
:::

:::quiz
p: Tu tabla tiene 400.000 ficheros de 1 MB y las consultas tardan más en planificarse que en leer. ¿Qué corresponde hacer?
o: Añadir más particiones para que cada fichero corresponda a un cliente
o: Compactar los ficheros pequeños en ficheros de tamaño razonable y ajustar el particionado
o: Cambiar de formato de tabla, porque el actual no soporta ese volumen
a: 2
e: El formato de tabla no crea el problema: lo hace manejable al permitir compactar sin parar las lecturas. La causa suele ser un particionado demasiado fino o micro-lotes mal agrupados. Cambiar de formato no reduce el número de ficheros.
:::

:::aviso
El lakehouse no elimina el gobierno: añade metadatos que lo hacen posible. Necesitas decidir
quién escribe cada tabla, con qué motor, cada cuánto se compacta y cuánto se retiene. Un
lakehouse sin esas decisiones es el mismo pantano, ahora con un registro de transacciones más
grande.
:::
