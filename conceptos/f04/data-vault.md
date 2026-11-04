---
id: data-vault
titulo: Modelado Data Vault
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [modelado-dimensional, hechos-y-dimensiones, evolucion-de-esquema]
tags: [modelado, historico, auditoria, integracion]
resumen: Hub, enlace y satélite: un modelado que solo inserta filas y que aguanta que los orígenes cambien sin reescribir el histórico.
fuentes: ["Linstedt y Olschimke (2015), 'Building a Scalable Data Warehouse with Data Vault 2.0'", "Reis y Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

Data Vault guarda cada cosa por separado y sin borrar nada: el hub tiene una fila por clave de
negocio, el enlace una fila por relación y el satélite una fila por cada cambio de atributos, así que
un origen nuevo o un dato corregido se añaden sin tocar lo que ya había.

## La idea

Imagina que en vez de una ficha de cliente que reescribes cada vez que el cliente se muda —y donde
pierdes lo de antes— llevas tres cuadernos. En el primero apuntas cada cliente una sola vez, con su
identificador de negocio. En el segundo apuntas relaciones: «este cliente hizo este pedido el 3 de
mayo». En el tercero apuntas cambios: «el 10 de enero vivía en Madrid, el 2 de marzo en Barcelona, el
1 de septiembre en Valencia». Nadie borra ni corrige: si descubres que el dato de marzo estaba mal,
escribes una línea nueva con la fecha en que lo supiste, y el cuaderno sigue contando lo que creías
en cada momento.

Ese es el espíritu de las tres piezas:

- **Hub:** la clave de negocio, el identificador que usa el negocio (NIF, número de pedido), con su
  `load_date` y el sistema del que vino. Una fila por clave, para siempre.
- **Enlace:** la relación entre dos o más hubs (cliente con pedido, producto con almacén). Una fila
  por combinación de claves.
- **Satélite:** los atributos descriptivos de un hub o de un enlace, con la fecha de carga. Una fila
  por cambio, y nunca un `UPDATE`.

El problema que resuelve es de carga, no de consulta. En un modelo dimensional
([[modelado-dimensional]]) cada origen nuevo obliga a tocar la dimensión y a decidir cómo reescribir
su historia ([[scd-dimensiones-cambiantes]]). Con diez fuentes que cambian de formato cada año, eso
es un proyecto por trimestre. En Data Vault, un origen nuevo se traduce en un satélite nuevo que
cuelga del hub que ya existía: no se toca ni una fila de lo anterior.

Dos consecuencias que hay que tener claras antes de elegirlo:

1. **El raw vault no aplica reglas de negocio.** Guarda lo que dijo cada fuente, tal cual, sin
   unificar mayúsculas ni elegir una ciudad «buena». La limpieza y la reconciliación entre fuentes
   van en el **business vault** o directamente en los marts. Si metes la regla en la carga, el día
   que cambie no puedes reconstruir lo que la fuente decía de verdad.
2. **No es una capa para consultar.** Un informe sobre el raw vault acaba con ocho uniones. Encima
   se construyen las dimensiones y los hechos de siempre ([[hechos-y-dimensiones]]), y ahí es donde
   pregunta el negocio.

Y no siempre compensa. Con una sola fuente y tres informes estables, Data Vault es coste sin
beneficio: más tablas, más carga y más joins para el mismo resultado. Brilla cuando hay muchas
fuentes, requisitos de auditoría y orígenes que cambian a menudo.

:::figura
fichero: data-vault-satelite-append
pie: Arriba, las cuatro piezas: el hub guarda la clave una sola vez, los satélites cuelgan de él con los atributos (y uno por fuente, sin pisarse), y el enlace une hubs entre sí. Abajo, lo que pasa cuando el origen informa cuatro veces del mismo cliente: la ciudad cambia en enero, marzo y septiembre, así que hay tres filas; la llegada de junio repite Barcelona, su hash coincide con la de la fila anterior y no inserta nada. El histórico no se reescribe: la versión vigente es la de load_date más alta.
fuente: figuras/data-vault-1.py
:::

## Definición formal

La identidad de un hub y la detección de un cambio se hacen con dos funciones de hash:

:::formula
hub_key = hash(clave_de_negocio)   ·   cambio ⇔ hashdiff(atributos) ≠ hashdiff de la última fila
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `clave_de_negocio` | Identificador que el negocio reconoce (NIF, número de pedido) | texto o número | Si cambia de formato o de longitud, todas las claves hash del almacén cambian con ella |
| `hub_key` | Hash de la clave de negocio: la clave con la que se unen todas las tablas | hexadecimal | Da igual su valor; si cambias el algoritmo o recortas el número de caracteres, hay que recargar el almacén |
| `load_date` | Instante en que la fila entró en el almacén | fecha y hora UTC | Si sube la precisión (de día a milisegundo), dos cargas del mismo día dejan de chocar al deduplicar |
| `record_source` | Sistema del que salió la fila | texto | Cuantas más fuentes alimenten el mismo hub, más satélites cuelgan de él y más trabajo de unificación |
| `hashdiff` | Hash de todos los atributos descriptivos de una fila | hexadecimal | Si cambia respecto al de la fila anterior, el satélite inserta; si coincide, no inserta nada |
| `satélite` | Tabla de atributos con su historia, colgada de un hub o de un enlace | filas | Cuantos más atributos agrupes juntos, más filas por cambio y más ancho el histórico |
| `enlace` | Tabla que relaciona dos o más hubs | filas | Un enlace con más hubs encarece la carga, pero modela relaciones de muchos a muchos |
| `efectividad` | Satélite del enlace que marca si la relación sigue viva | estado | Permite saber si un cliente sigue asignado a un comercial sin borrar ni un enlace |
:::

Con eso, la versión vigente de un atributo es la fila del satélite con el `load_date` más alto, y la
validez de la anterior termina justo ahí. Mucha gente añade una columna `load_end_date` y la rellena
al insertar el cambio: se puede, pero esa columna se actualiza, y entonces la tabla ya no es
inmutable ni se puede recargar una partición sin miedo.

## Ejemplo

El CRM manda cuatro fotos del cliente 42 durante 2024:

| Fecha de carga | Ciudad que informa | ¿Fila nueva en el satélite? |
| --- | --- | --- |
| 10 de enero | Madrid | Sí: es la primera |
| 2 de marzo | Barcelona | Sí: el hashdiff cambió |
| 15 de junio | Barcelona | No: mismo hashdiff que la anterior |
| 1 de septiembre | Valencia | Sí: el hashdiff volvió a cambiar |

Cuatro llegadas producen **una fila en el hub** y **tres en el satélite**. Con una dimensión SCD de
tipo 2 tendrías las mismas tres versiones, pero además habrías tenido que decidir si actualizas la
columna `valido_hasta` de la fila anterior (una escritura en el histórico) o si la dejas abierta y la
calculas en cada consulta. Aquí no hay decisión: solo se inserta.

Y si mañana el ERP informa otra ciudad para el mismo cliente, no se pisa nada: nace
`SAT_CLIENTE_ERP` colgado del mismo hub, y la unificación se decide después, en la capa donde se
puede discutir con negocio. Ese aplazamiento es la diferencia de fondo: el conflicto entre fuentes
no se resuelve durante la carga.

## Código

```python verificable
import hashlib
import pandas as pd

# Lo que manda el origen: una foto por carga, con la ciudad que el CRM conoce ese dia
origen = pd.DataFrame({
    "load_date": ["2024-01-10", "2024-03-02", "2024-06-15", "2024-09-01"],
    "id_cliente": [42, 42, 42, 42],
    "ciudad": ["Madrid", "Barcelona", "Barcelona", "Valencia"],
})

def hashdiff(fila):
    return hashlib.md5("|".join(str(v) for v in fila).encode()).hexdigest()[:8]

satelite = []
for _, fila in origen.iterrows():
    h = hashdiff([fila.id_cliente, fila.ciudad])
    if not satelite or h != satelite[-1]["hashdiff"]:    # solo inserta si algo cambio
        satelite.append({"load_date": fila.load_date, "ciudad": fila.ciudad, "hashdiff": h})

print("llegadas:", len(origen), " filas del satelite:", len(satelite))
# -> llegadas: 4  filas del satelite: 3
for f in satelite:
    print(f["load_date"], f["ciudad"], f["hashdiff"])
# -> 2024-01-10 Madrid a280015e
# -> 2024-03-02 Barcelona 39e607fe
# -> 2024-09-01 Valencia 375ab662
```

:::claves
- `hashlib.md5(...)` necesita **bytes**: `.encode()` no es decorativo, sin él lanza `TypeError`. Y
  el hash es determinista entre máquinas, cosa que el `hash()` de Python no es: cambia en cada
  arranque del proceso y rompería las claves de una carga a la siguiente.
- `hashdiff` tiene que calcularse sobre columnas limpias, en un orden fijo y con un separador fijo.
  Si incluyes el `load_date` o el origen, el hash cambia en cada carga y el satélite inserta una
  fila cada día aunque no haya pasado nada. Y si un día reordenas las columnas, todas las filas
  parecen nuevas.
- `.hexdigest()[:8]` es md5 recortado a ocho caracteres, no un hash de ocho caracteres: son 32 bits,
  y con ese tamaño la probabilidad de que dos filas distintas compartan hash deja de ser despreciable
  a partir de unas decenas de miles de filas. En producción se usan 16 o 32 caracteres.
- `origen.iterrows()` devuelve cada fila como una `Series` copiada, y `fila.ciudad` funciona porque
  la columna se llama así. Para millones de filas es lento: `itertuples()` hace lo mismo mucho más
  rápido.
- `satelite[-1]["hashdiff"]` compara contra la **última fila insertada**, no contra la anterior del
  origen. Es lo que hace que dos llegadas idénticas seguidas no dupliquen la fila, que es justo lo
  que pasa el 15 de junio.
- `satelite.append({...})` crea una lista de diccionarios, no un DataFrame. Si lo conviertes con
  `pd.DataFrame(satelite)`, `load_date` queda como texto: aquí el orden alfabético coincide con el
  cronológico porque las fechas van en formato ISO, pero el día que alguien escriba `10/01/2024` el
  orden se rompe. Para eso está `pd.to_datetime`.
:::

Así se lee la versión vigente de cada cliente, sin actualizar nada:

```sql ilustrativo
-- La versión vigente es la fila del satélite con el load_date más alto
select hub_key, ciudad, load_date
from (
    select s.*, row_number() over (partition by hub_key order by load_date desc) as rn
    from sat_cliente s
) t
where rn = 1
```

## Errores típicos

- **Meter reglas de negocio en el raw vault.** Poner la ciudad en mayúsculas o descartar los
  teléfonos con formato raro durante la carga te deja sin poder reconstruir lo que la fuente decía.
  El raw guarda lo que llegó; la regla vive en el business vault y se puede cambiar.
- **Hacer `UPDATE` en el satélite.** Rellenar `load_end_date` al insertar el cambio parece cómodo y
  rompe lo único que hacía especial a este modelado: si la tabla ya no es inmutable, no puedes
  recargar una partición sin preguntarte qué se va a pisar ([[idempotencia-y-reintentos]]).
- **Cambiar la receta del hash a mitad de camino.** Añadir una columna al `hashdiff`, cambiar el
  separador o el número de caracteres hace que todas las filas parezcan distintas y el satélite se
  duplique entero en la siguiente carga. La definición va en un contrato ([[contratos-de-datos]]).
- **Consultar el raw vault desde el cuadro de mando.** Ocho uniones para leer una ciudad. Los marts
  dimensionales que se construyen encima existen justo para eso.
- **Mezclar atributos que cambian con frecuencias muy distintas.** Si la dirección cambia cada mes y
  el segmento cada año, un satélite único inserta una fila por cada cambio de dirección repitiendo
  el segmento: histórico ancho y difícil de leer. Sepáralos por frecuencia de cambio.
- **Montarlo sin necesidad.** Es un patrón de integración para muchas fuentes y mucha auditoría. Con
  un origen y dos informes, el coste de mantenerlo no se recupera.

:::practica
enunciado: Dos fuentes informan del mismo cliente: el CRM manda ciudad y teléfono, y el ERP manda ciudad y límite de crédito. La ciudad del CRM cambia a menudo y la del ERP casi nunca, y a veces no coinciden. Diseña los hubs, enlaces y satélites y di dónde se resuelve el conflicto de ciudad.
pista: Lo que cambia con distinta frecuencia va en satélites distintos, y el raw vault no decide quién tiene razón.
solucion: Un solo HUB_CLIENTE con la clave de negocio compartida (el NIF) y su hub_key. De él cuelgan SAT_CLIENTE_CRM (ciudad, teléfono) y SAT_CLIENTE_ERP (ciudad, límite de crédito), cada uno con su load_date, su hashdiff y su record_source, y cada uno cargado de forma independiente: si el CRM cambia un teléfono, el satélite del ERP no se toca. Si dentro del CRM la ciudad cambia cada mes y el teléfono casi nunca, sepáralos también en dos satélites por frecuencia de cambio. El conflicto de ciudad no se resuelve al cargar: se resuelve en el business vault o en el mart, con una regla explícita del tipo «el CRM manda para la dirección de contacto y el ERP para la de facturación». Y si además hay pedidos, un ENLACE_CLIENTE_PEDIDO une HUB_CLIENTE con HUB_PEDIDO, con su load_date, sin duplicar los atributos del cliente.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué guarda exactamente un hub?
o: Los atributos descriptivos del cliente con su historia
o: La clave de negocio, con su load_date y el sistema del que vino, una fila por clave
o: La relación entre el cliente y sus pedidos
a: 2
e: El hub solo identifica: clave de negocio, load_date y record_source. Los atributos van en el satélite y las relaciones en el enlace. Si metieras atributos en el hub, un cambio de ciudad obligaría a insertar filas que romperían la regla de una fila por clave.
:::

:::quiz
p: Llega una carga en la que el cliente 42 sigue viviendo en la misma ciudad que la última vez. ¿Qué se inserta?
o: Una fila nueva en el satélite, porque cada carga deja rastro
o: Nada: el hashdiff coincide con el de la última fila del satélite
o: Una fila nueva en el hub, porque ha habido una carga
a: 2
e: Si el hashdiff de los atributos coincide con el de la fila anterior, no hay cambio que registrar y no se inserta nada. El hub tampoco crece: su clave de negocio ya estaba. Para dejar rastro de que la carga se ejecutó se usa una tabla de auditoría de procesos, no el satélite.
:::

:::quiz
p: El CRM y el ERP dan ciudades distintas para el mismo cliente y no sabes cuál es la buena. ¿Dónde se decide?
o: En la carga, quedándose con el valor del CRM porque llega primero
o: En la carga, con un UPDATE que unifique las dos
o: Más adelante, en el business vault o el mart, con una regla explícita
a: 3
e: El raw vault conserva la versión de cada fuente y no elige. Decidir en la carga convierte una discusión de negocio en código escondido que no puedes reconstruir; además, elegir «el que llega primero» hace que el resultado dependa del orden de las cargas. La regla se aplica después y se puede cambiar sin recargar el histórico.
:::
