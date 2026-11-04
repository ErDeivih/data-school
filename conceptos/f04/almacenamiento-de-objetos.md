---
id: almacenamiento-de-objetos
titulo: Almacenamiento de objetos
fase: 4
nivel: básico
rutas: [de]
prerequisitos: [ciclo-de-vida-del-dato, ficheros-y-encoding]
tags: [almacenamiento, nube, coste, s3]
resumen: Un disco remoto al que se accede por HTTP con objetos enteros; el prefijo hace de carpeta, la clase decide el coste y la frecuencia de lectura decide la clase.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering', cap. 6", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 3"]
---

## En una frase

El almacenamiento de objetos no se monta como un disco: se le piden objetos enteros por HTTP,
y cada objeto se identifica por una clave que es toda su ruta (`ventas/2026/01/parte-0001.parquet`).
No hay carpetas de verdad, solo nombres que empiezan igual, y eso cambia cómo organizas los
datos y cuánto pagas.

## La idea

Imagina un guardamuebles enorme. Alquilas un espacio con un nombre único (el *bucket*), metes
cajas y cada caja lleva escrita su dirección completa. Para coger algo no buscas en estanterías:
das la dirección exacta y te traen la caja entera. No puedes abrirla y cambiar un calcetín: la
sacas, la modificas y la vuelves a guardar entera.

Ese es el modelo. Sin sistema de ficheros, sin `rename`, sin `append`: **los objetos son
inmutables**, y actualizar uno significa reescribirlo completo. A cambio obtienes tres cosas que
ningún disco te da igual de barato: capacidad sin límite práctico, once nueves de durabilidad
-anunciada por los proveedores- y un precio por GB que es el más bajo del mercado.

El detalle que más confunde al principio es la barra. En la clave `ventas/2026/01/parte.parquet`
la barra es un carácter más del nombre, no un separador de carpetas. `ventas/2026` como *prefijo*
coincide también con la clave `ventas/2026-antiguo/resumen.csv`, porque solo compara texto. De
ahí salen los tres reflejos que hay que cambiar:

- Listar un prefijo es una operación de texto, no un recorrido de directorio. Lista y compara.
- Renombrar una "carpeta" es renombrar clave a clave: no existe un `mv` de directorios.
- El orden de la clave decide la lectura. Se escribe de lo más general a lo más concreto
  (fecha, entidad, partición) para que el sufijo identifique una única parte.

Los tres grandes coinciden en el concepto con nombres distintos: **S3** (AWS), **Cloud Storage**
(GCP) y **Blob Storage** (Azure). Bucket y container son lo mismo; la API y los permisos cambian,
las ideas no. Lo que aprendas de uno se traslada, y la sintaxis se consulta.

Y una propiedad que importa más de lo que parece: la **consistencia fuerte de lectura tras
escritura**. Cuando un `PUT` responde con éxito, cualquier `GET` o `LIST` posterior ve el objeto
nuevo. Sin eso, un trabajo que escribe un Parquet a las 03:00 y otro que lo lee a las 03:01
fallaría de forma intermitente. No confundas consistencia con durabilidad: la durabilidad dice
que el dato no se pierde; la consistencia, que se lee lo último escrito aunque el `PUT` acabe de
responder.

## Definición formal

El coste mensual de guardar datos en un bucket tiene tres sumandos y un posible castigo:

:::formula
coste = GB · p_almacén + n · p_lectura + peticiones · p_petición + penalización por borrado temprano
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `GB` | Volumen guardado, medido en GB | GB | Sube el primer sumando: el almacenamiento se paga siempre, se lea o no |
| `p_almacén` | Precio por GB y mes de la clase elegida | moneda por GB y mes | Sube el coste aunque no leas nada; es el único término que pagas con el sistema parado |
| `n` | Número de veces que lees cada GB en el mes | lecturas por GB y mes | Al subir, las clases frías dejan de compensar y la clase caliente vuelve a ganar |
| `p_lectura` | Precio por GB servido y por operación de `GET` | moneda por GB y moneda por operación | Sube el segundo sumando: castiga el acceso frecuente a datos fríos |
| `peticiones` | Número de llamadas a la API del mes | operaciones | Importa con ficheros diminutos: millones de objetos pequeños cuestan más en peticiones que en almacén |
| `p_petición` | Precio por cada 1000 o 10 000 operaciones | moneda por millar | Sube el tercer sumando; `PUT`, `GET` y `LIST` no siempre valen lo mismo |
| `penalización` | Cargo por borrar o sobrescribir antes del mínimo de la clase | moneda por GB | Solo existe en clases frías, que exigen conservar el objeto entre 30 y 180 días |
:::

Despejando `n` en el momento en que dos clases cuestan lo mismo, `n = (p_almacén_A − p_almacén_B) / (p_lectura_B − p_lectura_A)`,
se obtiene el umbral de lecturas al mes que justifica cada clase. Ese número, y no el precio por
GB, es el que decide.

:::figura
fichero: almacenamiento-de-objetos-clase-segun-acceso
pie: Cada línea es una clase; la línea gruesa azul es, en cada punto, la más barata. Lee el cruce y no el mínimo: si tu tabla se lee menos de 111 veces por GB al mes, la clase fría gana a la caliente aunque su precio por GB parezca peor, y por debajo de 20 la que gana es el archivo; si se lee más de 1000 veces, ninguna clase fría compensa y el acceso frecuente vuelve a ser la única opción sensata.
fuente: figuras/almacenamiento-de-objetos-1.py
:::

## Ejemplo

Una tabla de 200 GB que se consulta dos veces por semana. Son 200 · 8,7 = 1740 lecturas al mes,
es decir 8,7 lecturas por GB. Aplicando el despeje con `p_almacén` de 1,00, 0,50 y 0,20 y
`p_lectura` de 0,0005, 0,005 y 0,020 por lectura y GB:

- El primer cruce está en (1,00 − 0,50) / (0,005 − 0,0005) = **111 lecturas por GB al mes**: por
  debajo de esa frecuencia, la clase fría sale más barata que la caliente.
- Con 8,7, la clase fría cuesta 0,50 + 0,005 · 8,7 = **0,54** por GB y mes, frente a
  1,00 + 0,0005 · 8,7 = **1,00** de la caliente.
- Pero todavía no es la más barata de las tres. El segundo cruce, en
  (0,50 − 0,20) / (0,020 − 0,005) = **20 lecturas por GB al mes**, separa la clase fría del
  archivo: por debajo de 20 lecturas gana el archivo, que a esta frecuencia cuesta
  0,20 + 0,020 · 8,7 = **0,37**.
- En los 200 GB: 200,9 unidades al mes en caliente, 108,7 en frío y **74,8 en archivo**. A esta
  frecuencia lo que toca es bajar a archivo.

El mismo cálculo con 500 GB que se leen cuatro veces al día (120 lecturas por GB al mes) da lo
contrario: estás por encima de 111, así que la clase caliente recupera el primer puesto (1,06
frente a 1,10 de la fría y 2,60 del archivo).

## Código

```python verificable
import numpy as np

# Modelo de coste por GB y mes: almacen fijo + precio por operacion de lectura.
# Cifras de ejemplo en unidades relativas: la forma de las curvas es lo que se traslada
# a cualquier proveedor, no los numeros exactos.
almacen = {"caliente": 1.00, "frio": 0.50, "archivo": 0.20}
lectura = {"caliente": 0.0005, "frio": 0.005, "archivo": 0.020}

# Cuantas lecturas al mes hacen que dejar de usar la clase caliente salga a cuenta:
# se igualan los dos costes y se despeja n.
cruce1 = (almacen["caliente"] - almacen["frio"]) / (lectura["frio"] - lectura["caliente"])
cruce2 = (almacen["frio"] - almacen["archivo"]) / (lectura["archivo"] - lectura["frio"])
print(f"caliente = frio a las {cruce1:.0f} lecturas por GB al mes")   # -> 111
print(f"frio = archivo a las {cruce2:.0f} lecturas por GB al mes")    # -> 20

for n in (10, 200, 5000):
    coste = {k: almacen[k] + lectura[k] * n for k in almacen}
    print(f"{n:>5} lecturas/GB  " + "  ".join(f"{k} {v:.2f}" for k, v in coste.items())
          + f"  -> {min(coste, key=coste.get)}")
# -> 10 lecturas/GB  caliente 1.00  frio 0.55  archivo 0.40  -> archivo
# -> 200 lecturas/GB  caliente 1.10  frio 1.50  archivo 4.20  -> caliente
# -> 5000 lecturas/GB  caliente 3.50  frio 25.50  archivo 100.20  -> caliente
```

:::claves
- `almacen` y `lectura` son diccionarios, no arrays: aquí no se calcula nada con NumPy, se
  consultan precios por nombre. `np` solo aparece porque el ejemplo es el mismo modelo que la
  figura, y se podría borrar el `import` sin cambiar el resultado.
- `cruce1` y `cruce2` salen de despejar a mano, no de buscar el mínimo en una rejilla: si el
  precio de lectura de la clase fría baja, su cruce con la caliente **se aleja hacia la derecha**,
  así que la franja de lecturas en la que la clase fría gana se ensancha y más gente debería
  usarla.
- `min(coste, key=coste.get)` devuelve la **clave** del diccionario (el nombre de la clase), no
  el valor más pequeño. Es el error más habitual al leer esta línea: si quieres el importe hay
  que añadir `coste[mejor]`.
- `{n:>5}` alinea el número a la derecha en cinco caracteres y `{v:.2f}` lo redondea a dos
  decimales. Cambiar `.2f` por `.0f` cambia la salida, no el cálculo.
- `100.20` es un número con punto decimal de Python; el portal escribe los decimales con coma en
  la prosa, pero la salida de un `print` sale siempre con punto.
:::

```python verificable
import json

# Respuesta tipica de un listado de objetos (formato de S3 y compatibles).
# Fijate en IsTruncated y NextContinuationToken: el listado NO devuelve todo el prefijo.
respuesta = json.dumps({
    "Name": "datos-ventas",
    "Prefix": "ventas/2026/",
    "KeyCount": 2,
    "IsTruncated": True,
    "NextContinuationToken": "1ueGcxLPRx1Tr/XYExHnhbYLgveDs2J/wm36Hy4vbOwM=",
    "Contents": [
        {"Key": "ventas/2026/01/parte-0001.parquet", "Size": 134217728,
         "StorageClass": "STANDARD", "ETag": "9b2cf535f27731c974343645a3985328"},
        {"Key": "ventas/2026/01/parte-0002.parquet", "Size": 131072000,
         "StorageClass": "STANDARD", "ETag": "5f363e0e58a95f06cbe9bbc662c5dfb6"},
    ],
}, indent=2)
print(respuesta)

# Con IsTruncated en True hay que repetir la llamada pasando el token; sin ese bucle
# te quedas con las primeras claves y crees que el prefijo esta vacio o incompleto.
peticion = {"Bucket": "datos-ventas", "Prefix": "ventas/2026/",
            "ContinuationToken": "1ueGcxLPRx1Tr/XYExHnhbYLgveDs2J/wm36Hy4vbOwM="}
print("siguiente llamada:", peticion["ContinuationToken"][:12] + "...")  # -> 1ueGcxLPRx1T...
```

## Errores típicos

- **Creer que el prefijo es una carpeta.** `ventas/2026` coincide con `ventas/2026-antiguo/`
  porque es comparación de texto. Si filtras el prefijo sin la barra final, entran datos de otro
  periodo y el informe sale mal sin dar ningún error.
- **Elegir la clase de almacenamiento por el precio por GB.** La clase fría es la más barata en
  reposo y la más cara en cada lectura. Elige con el número de lecturas al mes, no con la tarifa.
- **Bajar datos a la clase de archivo y borrarlos a la semana.** Las clases frías imponen un
  mínimo de conservación -típicamente 30 días, y más en archivo- y cobran la diferencia al
  borrar. Un proceso que escribe, lee y borra en el mismo día paga penalización tres veces.
- **Ignorar el coste por petición con millones de objetos pequeños.** Mil millones de ficheros
  de 1 KB se pagan casi enteros en `PUT` y `GET`. Compacta antes de subir.
- **Suponer que una lista pequeña de permisos amplía el acceso.** En S3, la política del bucket
  decide y la lista de control de acceso solo puede recortar; los proveedores modernos la tienen
  desactivada por defecto. Dos capas no se suman: se cruzan.

:::practica
enunciado: Guardas 4 TB de Parquet escrito a diario, con un año de historia, y lo lees en un informe mensual. Calcula cuántos GB-mes ahorras al mover los datos a una clase fría que cuesta la mitad, y decide si compensa sabiendo que relees 1 TB al mes.
pista: El ahorro se mide en GB-mes, y el sobrecoste de lectura es la diferencia de precio por GB leído multiplicada por lo que lees.
solucion: 4000 GB al mes con la mitad de precio son 4000 · 0,5 = 2000 unidades ahorradas cada mes solo en almacén. El sobrecoste de lectura es 1000 GB · (0,005 − 0,0005) = 4,5 unidades: dos mil veces menos. Compensa con holgura, porque relees 0,25 veces cada GB y el umbral está en 111. Lo que hay que mirar con lupa es la clase de archivo: en almacén sale aún más barata (0,205 por GB y mes frente a 0,501), pero su precio por GB leído es cuatro veces el de la clase fría y su mínimo de conservación castiga mover y borrar, así que ahí decide la política de retención, no la aritmética.
:::

:::trampa
Un borrado en un bucket puede seguir devolviendo error 404 durante un rato en algunos sistemas
con caché, aunque la consistencia de lectura tras escritura esté garantizada. Un `404` no
significa «el objeto nunca existió»: significa «esta lectura no lo ve». Si tu lógica de negocio
depende de esa distinción, guárdala en un registro, no la deduzcas del código HTTP.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué mover una "carpeta" dentro de un bucket no es instantáneo?
o: Porque el proveedor limita las operaciones de movimiento a una por minuto
o: Porque no hay carpetas: cada objeto se renombra por separado, y renombrar es copiar y borrar
o: Porque el prefijo está indexado y hay que reconstruir el índice al cambiarlo
a: 2
e: El prefijo es un trozo del nombre del objeto, no un directorio. Cambiarlo obliga a copiar cada objeto a la clave nueva y borrar la vieja, objeto a objeto. No hay límite por minuto ni reconstrucción de índice: simplemente no existe la operación.
:::

:::quiz
p: Tu tabla de 300 GB se lee 40 veces por GB al mes y el cruce entre clase caliente y fría está en 111. ¿Qué haces?
o: La dejo en la clase caliente: 40 está por debajo de 111, así que lo barato es la fría
o: La muevo a archivo, que siempre es lo más barato en reposo
o: La parto en trozos más pequeños para que el prefijo liste más rápido
a: 1
e: El cruce marca el número de lecturas a partir del cual la clase caliente compensa. Con 40 lecturas estás por debajo, así que el coste de almacenamiento manda y la clase fría sale más barata. Archivo no: su precio por lectura es mucho mayor y quedas por encima de su cruce. Partir en trozos no cambia la clase ni el coste por GB.
:::

:::quiz
p: Un proceso sube 1000 ficheros de 1 KB cada hora y los borra al día siguiente. ¿Qué coste domina?
o: El almacenamiento, porque son muchos ficheros
o: Las peticiones, porque cada objeto se paga por operación y son objetos diminutos
o: Ninguno: los objetos de menos de 1 MB no se cobran
a: 2
e: 24 000 operaciones al día frente a unos pocos MB almacenados: el precio por petición aplasta al de almacén. Por eso se compactan los ficheros pequeños antes de subirlos. No existe ninguna exención por tamaño pequeño.
:::
