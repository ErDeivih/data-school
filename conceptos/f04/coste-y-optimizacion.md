---
id: coste-y-optimizacion
titulo: Coste y optimización
fase: 4
nivel: avanzado
rutas: [de, ds]
prerequisitos: [particionado-y-clustering, parquet-avro-orc, compresion-y-codificacion]
tags: [coste, rendimiento, almacenamiento, finops]
resumen: En analítica se paga sobre todo por bytes leídos, bytes guardados y horas de cómputo, así que optimizar es leer menos, archivar antes y no repetir trabajo.
fuentes: ["Documentación oficial de DuckDB, 'Parquet'"]
---

## En una frase

La factura de una plataforma de datos sale casi siempre de tres contadores —bytes leídos,
bytes almacenados y horas de cómputo—, y optimizarla consiste en tocar esos tres números:
leer menos datos por consulta, guardar lo viejo en un almacenamiento más barato y dejar de
repetir el mismo trabajo.

## La idea

La factura sorpresa casi nunca viene de un recurso caro y visible, como una máquina enorme. Viene
de mil consultas pequeñas que leen una tabla entera para usar tres columnas. La analogía es la
fotocopiadora: no pagas por tenerla enchufada, pagas por copia. Un `SELECT *` sobre una tabla de
dos terabytes es fotocopiar el archivador completo para leer una página.

Tres contadores, tres palancas:

1. **Leer menos.** Leer solo las columnas que usas (los formatos columnares como Parquet lo
   permiten de verdad, no es una metáfora), leer solo las filas que el filtro necesita
   (particionado y *pruning*), y comprimir para que cada byte leído cueste menos.
2. **Guardar distinto.** No todos los datos valen lo mismo: los de ayer se consultan cada hora,
   los de 2021 casi nunca. Mover lo antiguo a almacenamiento frío o a un formato más compacto
   reduce la partida de almacenamiento, que suele ser la más grande y la que menos se revisa.
3. **No repetir.** Un informe que se recalcula veinte veces al día desde los datos crudos se
   calcula una vez y se materializa. Un *job* que corre cada noche y produce lo mismo que el de
   la noche anterior es dinero tirado sin que nadie lo note.

Y una palanca organizativa que va antes que las técnicas: **atribuir el gasto**. Si cada recurso
lleva etiquetas de equipo y proyecto, el coste se puede repartir y cada equipo puede verlo. Sin
atribución, nadie sabe cuánto gasta y por tanto nadie optimiza: la factura es de todos y de
nadie.

:::aviso
Optimizar coste sin medir el valor es la forma más rápida de destruir un producto. Ahorrar 200
euros al mes leyendo los datos con un día de retraso puede costar ventas que valen doscientas
veces más. El coste se optimiza **sujeto a un nivel de servicio**: frescura, latencia y
exactitud se fijan primero, y después se busca la forma más barata de cumplirlos.
:::

## Definición formal

El modelo mental de coste de una consulta analítica:

:::formula
coste ≈ bytes_leídos · tarifa_lectura + horas_cómputo · tarifa_cómputo
:::

:::formula
coste_almacenamiento ≈ bytes_guardados · tarifa_mensual · meses
:::

- `bytes_leídos` — bytes que el motor tiene que abrir para responder. No es el tamaño de la
  tabla: es el de las columnas que tocas y las particiones que el filtro necesita.
- `tarifa_lectura` — precio por unidad de datos leídos, distinto según el servicio y la región.
- `horas_cómputo` — tiempo de clúster o de motor consumido, medido en horas o en unidades de
  cómputo por hora.
- `bytes_guardados` — lo que ocupa la tabla, ya comprimida, multiplicado por el tiempo que la
  guardas.

Las dos técnicas que mueven `bytes_leídos` de verdad:

- **Poda de columnas** (*column pruning*): en un formato columnar, cada columna vive en sus
  propios bloques. Si la tabla tiene 40 columnas y la consulta usa 3, se leen esas 3. En un CSV
  se leen las 40, porque el formato está orientado a fila.
- **Poda de particiones** (*partition pruning*): si la tabla está particionada por fecha y
  filtras por un mes, el motor solo abre las particiones de ese mes. La condición es que el
  filtro use la columna de partición, tal cual y sin funciones encima.

Y una tercera que se olvida: **el coste de sacar los datos del almacenamiento frío**. Mover un
archivo a una capa barata reduce el almacenamiento y sube el coste y la latencia de lectura. Si
un dato se consulta una vez al mes, la capa fría sale a cuenta; si se consulta cada día, no.

## Ejemplo

Una tabla de ventas particionada por mes: 24 particiones de 8 GB cada una, 192 GB en total. Un
informe filtra los tres primeros meses.

- Sin poda: el motor abre las 24 particiones y lee **192 GB**.
- Con poda: abre 3 particiones y lee **24 GB**.
- Factor de reducción: **8 veces menos datos** por ejecución.

Si ese informe se ejecuta 30 veces al mes, la diferencia es de 5 760 GB a 720 GB leídos, es
decir **5 040 GB menos al mes**. Con una tarifa supuesta de 0,005 unidades monetarias por GB
leído, el ahorro son 25,2 unidades al mes; el número exacto da igual, lo que importa es la
forma: el ahorro escala con las ejecuciones, no con el tamaño de la tabla. El mismo informe
ejecutado 300 veces al mes multiplica el ahorro por diez.

El otro contador se ve mejor con números pequeños. La misma tabla de 200 000 filas guardada en
Parquet ocupa **615 KiB sin comprimir y 546 KiB con gzip**: comprimir un valor decimal por fila
no da casi nada, porque los números aleatorios no se repiten. Pero la columna de país, que tiene
cuatro valores repetidos, ocupa **50 KiB ella sola**, y la de importe **376 KiB**. De ahí salen
las dos lecciones: la compresión ayuda donde hay repetición, y leer una sola columna de un
formato columnar lee una fracción del fichero.

## Código

```sql verificable
-- Catalogo de particiones de una tabla: 24 meses de 8 GB cada uno.
CREATE TABLE particiones AS
SELECT m AS mes, 8.0 AS gb FROM generate_series(1, 24) AS t(m);

-- Una consulta que filtra tres meses: el motor solo abre esas particiones.
SELECT count(*) AS particiones,
       round(sum(gb), 1) AS gb_totales,
       round(sum(CASE WHEN mes <= 3 THEN gb ELSE 0 END), 1) AS gb_leidos
FROM particiones;
```

```text
particiones | gb_totales | gb_leidos
24          | 192.0      | 24.0
```

```python verificable
import io
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

rng = np.random.default_rng(7)
filas = 200_000
tabla = pa.table({
    "pais": pa.array(rng.choice(["ES", "FR", "DE", "IT"], filas)),
    "importe": pa.array(np.round(rng.lognormal(3.0, 0.8, filas), 2)),
    "unidades": pa.array(rng.integers(1, 20, filas)),
})

def tamano(t, **kw):
    destino = io.BytesIO()          # medimos en memoria: nada de ficheros externos
    pq.write_table(t, destino, **kw)
    return destino.tell()

print("todo, sin comprimir:", tamano(tabla, compression="none") // 1024, "KiB")  # -> 615 KiB
print("todo, gzip:         ", tamano(tabla, compression="gzip") // 1024, "KiB")  # -> 546 KiB
print("solo pais (gzip):   ", tamano(tabla.select(["pais"]), compression="gzip") // 1024, "KiB")     # -> 50 KiB
print("solo importe (gzip):", tamano(tabla.select(["importe"]), compression="gzip") // 1024, "KiB")  # -> 376 KiB
```

```python verificable
# Aritmetica del ahorro: con tarifas redondas supuestas, lo que importa es la forma.
gb_particion = 8
particiones = 24
meses_consultados = 3
ejecuciones_mes = 30
tarifa_gb = 0.005        # unidades monetarias por GB leido (tarifa supuesta)

gb_antes = gb_particion * particiones * ejecuciones_mes
gb_despues = gb_particion * meses_consultados * ejecuciones_mes

print("GB al mes barriendo todo:  ", gb_antes)          # -> 5760
print("GB al mes leyendo 3 de 24:", gb_despues)         # -> 720
print("factor de reduccion:      ", gb_antes / gb_despues)   # -> 8.0
print("ahorro mensual:", round((gb_antes - gb_despues) * tarifa_gb, 2))  # -> 25.2
```

## Errores típicos

- **`SELECT *` en tablas anchas.** Es la causa número uno de facturas altas y se ve en cualquier
  revisión de consultas. En un formato columnar, nombrar las seis columnas que usas puede
  reducir lo leído en un orden de magnitud. Cuesta lo mismo escribirlas.
- **Filtrar por una columna que no es la de partición.** La tabla está particionada por fecha y
  la consulta filtra por cliente: el motor abre las 24 particiones y paga 192 GB. Si esa
  consulta es frecuente, el arreglo es una tabla agregada por cliente, no un índice mágico.
- **Particionar por una columna de altísima cardinalidad.** Un millón de particiones de dos
  filas cuesta más en metadatos y en listado de ficheros que el propio dato: el motor pierde el
  tiempo abriendo ficheros diminutos. Particiona por algo con decenas o cientos de valores
  (mes, región) y ordena o agrupa por el resto.
- **Guardar todo en crudo para siempre «por si acaso».** El almacenamiento es la partida que
  más crece y la que nadie revisa. Define retención por tabla: crudo 30 días, curado un año,
  histórico agregado en capa fría. Escribe la política antes de que la tabla tenga 40 TB.
- **Recalcular cada hora un informe que se lee una vez al día.** Materializa el agregado una
  vez y sirve las lecturas desde una tabla pequeña. Es el ahorro más fácil de conseguir y el
  que menos se hace, porque el trabajo redundante no se ve en ningún panel.
- **Tener el clúster encendido 24 horas para un proceso que dura 40 minutos.** El cómputo se
  factura por tiempo, no por trabajo. Apagado automático, instancias interrumpibles para las
  cargas que pueden reintentarse y colas para las que no son urgentes bajan la factura sin
  tocar una línea de SQL.

## Comprueba que lo sabes

:::quiz
p: Una tabla está particionada por mes. La consulta filtra por identificador de cliente y toca los 24 meses. ¿Qué ocurre con el coste?
o: El motor lee solo las filas del cliente, porque filtra por una columna muy selectiva
o: El motor abre las 24 particiones, porque el filtro no usa la columna de partición
o: El coste no cambia: el particionado solo afecta al almacenamiento
a: 2
e: La poda de particiones necesita que el filtro use la columna de partición. Filtrar por cliente no evita abrir todas las particiones, aunque descarte casi todas las filas después. La solución habitual es una tabla agregada por cliente o particionar también por esa dimensión.
:::

:::quiz
p: Guardas 200 000 filas en Parquet y la columna de importes apenas se comprime, mientras que la de país pasa de más de 100 KiB a 50 KiB. ¿Por qué?
o: Porque Parquet comprime solo las columnas de texto
o: Porque la compresión aprovecha la repetición, y los valores decimales aleatorios no se repiten
o: Porque los números en coma flotante ocupan menos que el texto
a: 2
e: Un compresor explota patrones repetidos. Cuatro valores de país repetidos 200 000 veces son un patrón ideal; importes con decimales aleatorios no tienen repetición que explotar. Por eso la compresión ayuda mucho en categóricas y fechas, y bastante menos en medidas continuas.
:::

:::truco
Antes de cambiar nada, ordena las consultas por bytes leídos durante una semana. Casi siempre
ocurre que el 5 % de las consultas hace el 80 % del gasto, y varias de ellas son el mismo
informe mal programado ejecutándose por un `cron` que nadie recuerda haber configurado.
:::
