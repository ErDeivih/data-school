---
id: particionado-y-clustering
titulo: Particionado y clustering
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [parquet-avro-orc, data-lake]
tags: [rendimiento, almacenamiento, coste, poda]
resumen: Cortar la tabla por fecha o región para que cada consulta lea solo su trozo, elegir la cardinalidad correcta y ordenar las filas dentro del fichero.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications'"]
---

## En una frase

**Particionar** es separar físicamente las filas en grupos disjuntos por el valor de una
columna (una carpeta o un conjunto de ficheros por día, por país o por canal) para que una
consulta que filtra por esa columna ignore el resto; **agrupar** (*clustering*) es ordenar las
filas dentro de cada fichero para que las estadísticas permitan descartar trozos más pequeños y
los datos compriman mejor.

## La idea

Tienes 4 TB de ventas, 4 años de historia y una consulta que siempre filtra por un día concreto.
Sin ayuda, el motor tiene que abrir todos los ficheros y mirar las fechas una a una. Con el
particionado adecuado, la consulta abre **un** fichero: el del día que le interesa. No es una
optimización del 20 %, es leer `2,8 GB` en lugar de `4 TB`.

La analogía es un archivo de facturas. Si metes todas las facturas en una caja única, buscar una
de marzo de 2023 es abrir la caja y revisarlas todas. Si tienes una caja por año y mes, vas
directo. Y si además dentro de la caja los recibos están en orden, puedes buscar por importe sin
mirarlos todos.

Eso son las dos ideas, y son distintas:

- **Particionar** divide en ficheros separados. La poda es todo o nada por partición: la lees o
  no la lees.
- **Agrupar** decide el orden dentro del fichero. La poda es por bloque de filas, más fina, y
  además mejora la compresión porque los valores parecidos quedan juntos.

El error clásico es particionar por cualquier cosa. La clave está en **cuántas particiones**
generas y **de qué tamaño** quedan:

- Menos de 128 MB por partición: demasiados ficheros, sobrecarga de abrir y planificar.
- Más de 1 GB: poca poda, cada consulta lee un bloque enorme.
- La zona buena está entre **128 MB y 1 GB** por partición, y se ajusta con la granularidad
  (por día, por hora) y con el número de valores distintos de la clave.

Una columna es buena clave de partición si cumple tres cosas: se filtra casi siempre, tiene
cardinalidad moderada y reparte los datos de forma razonablemente uniforme. La fecha de un
evento cumple las tres; el identificador de cliente no cumple la segunda (millones de valores) y
el país no cumple la tercera si el 90 % de tus ventas son de un solo país.

Y hay una distinción que conviene no mezclar:

- **Partición:** conjunto disjunto de filas, con su propio prefijo de ruta. Podas ficheros
  enteros.
- **Orden / clustering:** las filas, dentro de cada fichero, se escriben ordenadas por una o
  varias columnas (o con un orden espacial tipo *Z-order* que entrelaza varias). Podas bloques
  de filas. En Iceberg se declara con columnas ordenadas; varios motores lo llaman *liquid
  clustering* cuando el motor lo reorganiza solo.
- **Bucket:** reparto por hash en un número fijo de cubos. Se usa sobre todo para que dos tablas
  se unan sin mover datos, no para filtrar por rango.

No son alternativas: lo habitual es **particionar por fecha y agrupar por la segunda columna
más filtrada** (por ejemplo, cliente o producto). Así la consulta poda por día y, dentro del
día, descarta bloques por rango de cliente.

## Definición formal

Sea una tabla `T` con `N` filas y `B` bytes totales. Una **especificación de partición** es una
función `p: fila → valor`, y la tabla se escribe en un fichero por cada valor distinto:

- `k = |{p(fila)}|` — número de particiones (cardinalidad de la clave).
- `tamaño_medio = B / k` — bytes por partición; es la cifra que hay que vigilar.
- Una consulta que filtra por la clave toca `m` particiones y lee aproximadamente `m · B / k`
  bytes (suponiendo reparto uniforme).

:::formula
bytes_leídos ≈ B · m / k  ·  con m = particiones que cumplen el filtro
:::

De ahí salen las dos reglas de diseño:

1. **Maximizar `k`** hasta que `B / k` baje de 128 MB; a partir de ahí solo ganas ficheros
   pequeños y sobrecarga.
2. **Minimizar `m`**: si la columna se filtra poco o el filtro es amplio, `m` se acerca a `k` y
   el particionado no aporta nada.

Y la tercera cifra que hay que mirar siempre: la **asimetría**. Si una partición concentra el
90 % de los bytes (un solo día con toda la campaña del año, o todos los nulos juntos), el
trabajo se reparte mal y una tarea tarda cien veces más que las demás. Se detecta midiendo el
tamaño por partición, no el total.

## Ejemplo

Ventas de 4 años en una tabla de 4.096 GB:

| Esquema | Particiones | Tamaño medio | Qué pasa |
| --- | --- | --- | --- |
| Sin particionar | 1 | 4.096 GB | Cada consulta lee 4 TB |
| Por fecha (4 años de 365 días) | 1.460 | 2,81 GB | Aún demasiado por partición |
| Por fecha y hora | 35.040 | 119,7 MB | En el rango recomendado |
| Por fecha y cliente | 7.300.000 | 0,57 MB | Desastre de ficheros pequeños |

Con el particionado por fecha y hora, una consulta de un día toca 24 particiones: lee unos
2,9 GB de los 4 TB, el **0,07 %**. A un precio hipotético de 5 dólares por TB leído, la consulta
pasa de 20 dólares a 1,4 céntimos. Ese es el motivo de que el particionado sea la primera
optimización de coste en la nube: no acelera el motor, hace que el motor lea menos.

Y ojo con el otro extremo: con una partición por cliente y fecha, cada consulta abre 7,3
millones de ficheros, la planificación tarda más que la lectura y la factura por peticiones se
dispara. El particionado mal elegido es peor que no particionar.

## Código

```python verificable
# Tabla de 4 TB con 4 anos de 365 dias: cuanto se lee con y sin poda
tam_tabla_gb = 4096
dias = 4 * 365
tam_particion_gb = tam_tabla_gb / dias

print("particiones por fecha:", dias)                        # -> particiones por fecha: 1460
print("GB por particion:", round(tam_particion_gb, 2))       # -> GB por particion: 2.81
print("porcentaje leido en un dia:", round(100 / dias, 4))   # -> porcentaje leido en un dia: 0.0685

precio_tb = 5.0    # precio hipotetico por TB escaneado
print("coste sin podar:", round(tam_tabla_gb / 1024 * precio_tb, 2), "USD")    # -> coste sin podar: 20.0 USD
print("coste podando:", round(tam_particion_gb / 1024 * precio_tb, 3), "USD")  # -> coste podando: 0.014 USD
```

```python verificable
# Elegir la granularidad: el objetivo esta entre 128 MB y 1 GB por particion
tam_tabla_mb = 4096 * 1024

print("solo por fecha:", round(tam_tabla_mb / 1460, 1), "MB por particion")              # -> solo por fecha: 2872.8 MB por particion
print("por fecha y hora:", round(tam_tabla_mb / (1460 * 24), 1), "MB por particion")     # -> por fecha y hora: 119.7 MB por particion
print("por fecha y cliente:", round(tam_tabla_mb / (1460 * 5000), 2), "MB por particion")  # -> por fecha y cliente: 0.57 MB por particion
print("ficheros con fecha y cliente:", 1460 * 5000)                                      # -> ficheros con fecha y cliente: 7300000
```

## Errores típicos

- **Particionar por una columna de cardinalidad altísima.** `id_cliente`, `id_pedido` o un
  identificador de sesión generan millones de ficheros de pocos kilobytes. Si necesitas podar
  por cliente, agrupa u ordena por esa columna, no la uses como partición.
- **Particionar por una columna que nadie filtra o creer que acelera todas las consultas.** Si
  particionas por `canal_venta` y todas las consultas filtran por fecha, has multiplicado los
  ficheros sin podar nada; y una consulta que no filtra por la clave recorre todas las
  particiones igual que antes, ahora con más sobrecarga. La poda solo funciona si el filtro usa
  la clave (o una función de ella, con particionado oculto).
- **Confundir particionar con agrupar.** Particionar sin ordenar deja ficheros cuyo rango de
  fechas es amplio; las estadísticas no descartan nada dentro. Lo correcto es las dos cosas:
  partición por fecha y orden por la segunda columna más filtrada.
- **Ignorar la asimetría y los nulos.** Una partición mil veces mayor que las demás convierte un
  trabajo de 10 minutos en uno de 3 horas, porque no se puede repartir; se detecta midiendo el
  tamaño por partición, no el total. Y en muchos motores todos los nulos de la clave caen en una
  única partición enorme, así que fíltralos, imputa o trátalos antes de escribir.
- **Cambiar el esquema de particiones sin reescribir el histórico.** Si la tabla vieja está
  particionada por día y la nueva por hora, durante meses conviven dos disposiciones y las
  consultas leen ambas. Migra y compacta, no convivas con las dos.
- **Confundir bucket con partición.** El *bucketing* por hash reparte en un número fijo de cubos
  para poder unir dos tablas sin mover datos; no sirve para podar por rango de fechas.

## Comprueba que lo sabes

:::quiz
p: Tienes 4 TB y particionas por fecha: 1.461 particiones de 2,8 GB. ¿Cuál es el siguiente problema a resolver?
o: Que hay demasiadas particiones y sobra poda
o: Que cada partición sigue siendo grande y conviene una granularidad más fina, por ejemplo por hora
o: Que hay que añadir el identificador de cliente como segunda clave de partición
a: 2
e: Con 2,8 GB por partición cada consulta sigue leyendo bastante más de lo recomendable. Bajar a hora deja unas 24 particiones por día de unos 120 MB. Añadir el cliente multiplicaría los ficheros hasta el desastre de los kilobytes.
:::

:::quiz
p: ¿Qué diferencia hay entre particionar y agrupar (clustering)?
o: Son sinónimos: las dos separan filas en ficheros distintos
o: Particionar separa filas en ficheros distintos; agrupar ordena las filas dentro del fichero para podar bloques y comprimir mejor
o: Particionar sirve para leer y agrupar para escribir
a: 2
e: La partición es física y disjunta: una consulta abre o no abre el fichero. El orden dentro del fichero permite descartar bloques de filas mediante estadísticas y mejora la compresión al juntar valores parecidos. Se combinan: se particiona por fecha y se agrupa por la segunda columna más filtrada.
:::

:::quiz
p: Filtras por fecha pero particionaste por país, que tiene 40 valores con reparto uniforme. ¿Qué consigues?
o: Nada útil: la consulta tiene que leer las 40 particiones porque el filtro no usa la clave
o: Leer solo la partición del país que te interesa
o: La mitad de los datos, porque el reparto es uniforme
a: 1
e: La poda descarta particiones cuyo valor no puede cumplir el filtro. Si el filtro es por fecha y la partición es por país, ninguna de las 40 se puede descartar. El particionado debe hacerse por la columna que de verdad aparece en los filtros.
:::

:::trampa
Particionar no arregla un problema de datos pequeños: un volcado diario de 300 MB
particionado por hora produce 24 ficheros de 12 MB, y eso es peor que un único fichero de 300
MB. Antes de particionar, mide el volumen diario y calcula el tamaño de partición.
:::
