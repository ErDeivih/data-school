---
id: problema-de-ficheros-pequenos
titulo: El problema de los ficheros pequeños
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [parquet-avro-orc, particionado-y-clustering]
tags: [lakehouse, compactacion, rendimiento]
resumen: Miles de ficheros diminutos hunden un lago porque listar cuesta más que leer: compactación, tamaño objetivo y por qué particionar de más es un error.
fuentes: ["Armbrust et al. (2020), 'Delta Lake: High-Performance ACID Table Storage'", "Apache Iceberg (2024), 'Table Maintenance'"]
---

## En una frase

Un lago con cien mil ficheros de diez kilobytes tarda más en **encontrar** los datos que en
leerlos, y arreglarlo es compactar: juntar ficheros pequeños en otros de tamaño razonable.

## La idea

Guardar cada micro-lote como un fichero parece inocente: el pipeline escribe rápido y no
sobrescribe nada. El problema aparece al leer. Un motor tiene que abrir el catálogo, listar los
objetos, pedir metadatos de cada uno y planificar; con cien mil ficheros, esa fase de planificación
cuesta segundos o minutos, y el trabajo útil es una fracción del tiempo total.

Hay un segundo efecto, peor: el almacenamiento de objetos cobra por petición. Cien mil `GET`
pequeños cuestan más que cien `GET` grandes con los mismos bytes. Y un tercero: cada fichero añade
su propia cabecera y su pie, así que la compresión pierde eficacia porque los diccionarios no se
comparten.

La solución tiene dos partes. **Escribir mejor**: agrupar por tamaño, no por evento, y usar
`COPY INTO`/`MERGE`/`append` en lotes razonables. **Mantener**: compactar periódicamente con la
operación del formato (`OPTIMIZE` en Delta, `rewrite_data_files` en Iceberg), que reescribe muchos
ficheros pequeños en pocos grandes.

Y una consecuencia contraintuitiva: **particionar de más también crea ficheros pequeños**. Si
particionas por hora y solo llegan tres eventos por hora, cada partición es un fichero de un
kilobyte. La regla práctica es que una partición tenga al menos cientos de megabytes; si no, se
particiona por día o por mes.

:::aviso
Compactar cuesta dinero y tiempo: reescribe datos. No lo hagas en cada ejecución ni sobre la tabla
entera. Se compacta lo que ha crecido y se mide antes y después: ficheros, tiempo de consulta y
bytes leídos.
:::

## Definición formal

El coste de leer una tabla crece con el número de ficheros por dos vías: la planificación y las
peticiones.

:::formula
ficheros_por_particion = bytes_particion / bytes_fichero        objetivo ≈ 128-512 MB por fichero
:::

- **bytes_particion** — lo que ocupa una partición (un día, un mes).
- **bytes_fichero** — el tamaño medio de los ficheros que escribe tu proceso.
- **Amplificación de metadatos** — cociente entre abrir todos los ficheros actuales y abrir los que
  harían falta con el tamaño objetivo.

Si una partición diaria tiene 1 GB y escribes ficheros de 10 KB, necesitas 104.857 aperturas para
leerla. Con ficheros de 128 MB, ocho. El trabajo útil es el mismo; la diferencia está en el
trabajo de coordinación.

## Ejemplo

Cien mil ficheros de 10 KB: 0,95 GB en total. Con un objetivo de 128 MB por fichero harían falta
ocho ficheros. La lectura útil es la misma —0,95 GB—, pero las aperturas pasan de 100.000 a 8.

Eso es una amplificación de metadatos de 13.107 veces. En un almacén local no se nota; en
almacenamiento de objetos, con latencia por petición, es la diferencia entre un panel que carga en
dos segundos y uno que tarda un minuto.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `bytes_fichero` | Tamaño medio de los ficheros escritos | MB | Baja el número de ficheros y el coste de planificar; demasiado grande penaliza la lectura selectiva |
| `bytes_particion` | Datos por partición | MB o GB | Con particiones pequeñas, cada una genera ficheros diminutos: es la causa más común |
| `ficheros_por_particion` | Cociente entre los dos anteriores | ficheros | Por encima de unos cientos por partición, el motor pierde más tiempo planificando que leyendo |
| `frecuencia_compactacion` | Cada cuánto se reescriben los ficheros | ejecuciones | Más frecuencia mejora la lectura y cuesta más escritura; se mide y se ajusta |
:::

## Código

```python verificable
# Coste de metadatos: cuántas aperturas necesita una tabla con un tamano de fichero dado
total_mb = 100_000 * 10 / 1024          # 100.000 ficheros de 10 KB
objetivo_mb = 128

print(f"tamano total {total_mb / 1024:.2f} GB")                      # -> tamano total 0.95 GB
print(f"ficheros objetivo {total_mb / objetivo_mb:.0f}")             # -> ficheros objetivo 8
print(f"amplificacion {100_000 / (total_mb / objetivo_mb):.0f}")     # -> amplificacion 13107
print(f"bytes por fichero {10 * 1024}")                              # -> bytes por fichero 10240
```

Con esos números, la decisión se toma sola: o se compacta o se deja de escribir por evento.

:::claves
- `total_mb / objetivo_mb` da cuántos ficheros harían falta con el tamaño objetivo. Es una división,
  no una medición: sirve para decidir, no para informar de lo que hay.
- `100_000 / 8` es la amplificación de metadatos, no de bytes. Confundirlas lleva a optimizar la
  compresión cuando el problema es el número de objetos.
- El tamaño objetivo no es universal: en un lago consultado con filtros de tiempo, 128-256 MB suele
  ir bien; en una tabla que se lee entera, más grande es mejor.
- `10 * 1024` bytes son 10 KB binarios, no 10.000. La diferencia es un 2,4 % y en estas cuentas no
  cambia la decisión, pero conviene saber cuál estás usando.
- La estimación ignora la compresión: si los datos comprimen 4 a 1, el fichero real es cuatro veces
  menor y la amplificación empeora en la misma proporción.
:::

## Errores típicos

- **Particionar por hora con poco volumen.** Es la causa número uno: cada partición es un fichero y
  el lago acaba con cien mil objetos. Particiona por día o por mes y filtra por columna.
- **Escribir un fichero por evento o por micro-lote.** El pipeline parece más simple y arruina la
  lectura de todos los demás.
- **Compactar toda la tabla cada noche.** Reescribe terabytes para arreglar unos megabytes. Compacta
  lo que ha crecido y mide el antes y el después.
- **Ignorar el coste por petición del almacenamiento de objetos.** Los bytes son baratos; las
  peticiones no. Un `LIST` de cien mil claves se paga.
- **Confundir compactación con `VACUUM`.** Compactar reescribe datos vivos; `VACUUM` borra lo que ya
  no se referencia. Son operaciones distintas y una no sustituye a la otra.
- **No medir.** Sin comparar ficheros, tiempo de consulta y bytes leídos antes y después, la
  compactación es un ritual.

:::practica
enunciado: Una tabla recibe 50 MB al día y se particiona por hora, con un fichero por micro-lote de 40 segundos. Calcula cuántos ficheros se generan al día y propone dos cambios concretos.
pista: Un día tiene 86.400 segundos; cada micro-lote es un fichero.
solucion: 86.400 / 40 = 2.160 ficheros al día, con 23 KB cada uno: el peor caso posible. Cambios: escribir en lotes de 5-10 minutos (288 ficheros al día) y compactar cada noche dejando 2-3 ficheros de 16-25 MB por hora, o directamente particionar por día y dejar 1 fichero de 50 MB.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué particionar por hora puede empeorar el rendimiento?
o: Porque crea muchas particiones con muy pocos datos, y cada una es al menos un fichero diminuto
o: Porque el motor no sabe leer particiones horarias
o: Porque la compresión no funciona en particiones
a: 1
e: Particionar reduce los datos a leer, pero cada partición es un objeto. Si el volumen por hora es pequeño, se multiplican los ficheros y el coste de planificación se come la ganancia del filtrado.
:::

:::quiz
p: La amplificación de metadatos es 13.000. ¿Qué mide exactamente?
o: Cuántas veces más ficheros hay que abrir respecto a una tabla con el tamaño objetivo
o: Cuántas veces se ha comprimido la tabla
o: El número de columnas que tiene la tabla
a: 1
e: Es el cociente entre aperturas actuales y aperturas con ficheros de tamaño objetivo. No dice nada de bytes ni de compresión: dice cuánto trabajo de coordinación estás pagando por tener objetos pequeños.
:::
