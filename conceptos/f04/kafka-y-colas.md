---
id: kafka-y-colas
titulo: Kafka y colas de mensajes
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [batch-vs-streaming, ingesta-incremental-y-cdc]
tags: [kafka, colas, mensajeria, particiones, consumidores]
resumen: Un registro distribuido y ordenado por partición donde los productores escriben y cada consumidor lee a su ritmo; la pieza que desacopla dos sistemas.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11", "Narkhede, Shapira & Palino (2017), 'Kafka: The Definitive Guide'"]
---

## En una frase

Kafka es un registro de mensajes distribuido y persistente: los productores añaden eventos al
final de un tema, cada consumidor los lee a su propio ritmo guardando su posición, y el orden solo
está garantizado dentro de cada partición.

## La idea

Imagina una cinta transportadora de fábrica. Las piezas se colocan al final y avanzan; quien las
necesita las coge cuando puede, y la cinta no se detiene por él. Eso es Kafka, frente a la
bandeja de entrada que es una cola clásica: allí el mensaje se entrega y se borra, y si hay cinco
consumidores compitiendo, cada mensaje va a uno solo.

La diferencia importante es esta: **en Kafka el mensaje no se borra al entregarse**. Se queda en
disco el tiempo que dure la retención, y cada consumidor mantiene su propio puntero, llamado
compensación u *offset*. Diez grupos de consumidores distintos leen los mismos mensajes, cada uno
a su ritmo y sin estorbarse. Eso es lo que permite que el mismo flujo de eventos alimente al
equipo de fraude, al de analítica y al de recomendación sin montar tres tuberías.

Por qué se usa tanto:

1. **Desacopla productor y consumidor.** El sistema que genera 200.000 eventos por segundo no
   sabe ni le importa quién los lee. Si el consumidor está caído, la cinta sigue avanzando.
2. **Absorbe picos.** El registro hace de búfer. Un consumidor que se cae cuatro horas puede
   reanudar exactamente donde estaba, siempre que la retención conserve esos segmentos.
3. **Se puede rebobinar.** Mover la compensación hacia atrás y recalcular es la forma limpia de
   reprocesar un periodo sin volver a molestar a la fuente ([[backfill-y-reproceso]]).

El precio es de operación: hay que mantener los intermediarios, los discos y la retención, y hay
que entender bien tres mecanismos antes de poner nada en producción: **particiones**, **grupos de
consumidores** y **garantías de entrega**.

Sobre las particiones, la idea que más cuesta interiorizar es que **el orden es local**. Un tema
se divide en particiones, y cada partición es una secuencia ordenada independiente. No existe un
orden global del tema. Si necesitas que todos los eventos de un mismo cliente se procesen en
orden, el productor debe publicar con la clave del cliente: el mismo valor de clave cae siempre en
la misma partición. El efecto secundario es que un cliente enorme puede desequilibrar la
repartición, exactamente el mismo problema de asimetría que aparece en las uniones distribuidas
([[spark-joins-y-skew]]).

Sobre los grupos, la regla que hay que memorizar es que **una partición la lee un solo miembro del
grupo a la vez**. Por tanto el paralelismo máximo de un grupo es el número de particiones. Añadir
consumidores más allá de ese número no acelera nada: se quedan ociosos.

## Definición formal

- Un **tema** `T` se divide en `P` particiones. Cada partición es una secuencia de registros
  `(offset, clave, valor, marca_de_tiempo)` donde `offset` es un entero que empieza en 0 y solo
  crece. No se puede modificar un registro ya escrito.
- **Asignación por clave:** por defecto, el productor calcula la partición como
  `p = hash(clave) mod P`. Con clave nula, reparte por turnos entre las particiones, lo que
  destruye cualquier orden por entidad.
- **Grupo de consumidores** `G` con `C` miembros. Las `P` particiones se reparten entre los
  miembros: cada partición pertenece a un único miembro de `G`. De ahí:

:::formula
paralelismo_máximo = P        p = hash(clave) mod P
:::

- **Compensación (offset) confirmada:** la posición que el consumidor declara haber procesado. La
  diferencia con la última posición escrita por el productor es el **retraso**:

:::formula
lag = ultimo_offset_producido − ultimo_offset_confirmado
:::

El retraso es la métrica que se vigila en producción. Un sistema de mensajería que funciona
mientras el retraso crece sin que nadie lo mire es un sistema que fallará el día que la retención
borre los segmentos que el consumidor todavía necesitaba.

- **Retención:** `log_retention.ms` y `retention.bytes` deciden cuánto tiempo y cuánto espacio se
  conserva. Cuando se supera, se borran los segmentos más antiguos. Un consumidor parado más
  tiempo del que dura la retención no puede continuar desde su compensación: sus datos ya no
  están.

Garantías de entrega, que dependen de **cuándo** confirma el consumidor:

| Garantía | Cuándo confirma | Qué pasa si el proceso muere |
| --- | --- | --- |
| Como mucho una vez | Antes de procesar | El mensaje se pierde en silencio |
| Al menos una vez | Después de procesar | El mensaje se repite: el destino tiene que ser idempotente |
| Exactamente una vez | En una transacción que une el procesado y la confirmación | No se pierde ni se repite, pero solo dentro del circuito del propio Kafka |

## Ejemplo

Un tema `pedidos` con **6 particiones**. Llegan pedidos de cuatro clientes y el productor publica
con la clave `cliente_id`. Supongamos que el hash reparte así: `A` cae en la partición 1, `B` en la
5, `C` en la 5 y `D` en la 0.

```
particion 0:  D-1  D-2  D-3
particion 1:  A-1  A-2  A-3
particion 5:  B-1  C-1  B-2  C-2  B-3  C-3
```

- El orden **dentro de cada partición** es el orden de escritura. Los pedidos de `A` se procesan
  en orden, y los de `B` y `C` también, porque todos los eventos de una misma clave caen siempre
  en la misma partición. Aquí, además, `B` y `C` comparten la partición 5: se conserva el orden
  dentro de cada cliente, pero el orden relativo entre un pedido de `B` y uno de `C` lo fija la
  cinta, no el cliente.
- Un grupo con **3 consumidores** reparte las 6 particiones: dos cada uno. Pero el que reciba la
  partición 5 hace el doble de trabajo que los demás. Tienes tres consumidores y el trabajo está
  desequilibrado, porque la clave es lo que decide la partición y el productor no reparte las
  claves por ti.
- El **paralelismo máximo** de este grupo es 6. Si despliegas 8 consumidores, dos se quedan sin
  nada que leer: Kafka no crea particiones nuevas porque tú añadas procesos.
- Y el **retraso**: si el productor escribe 1.000.000 de eventos por hora y este consumidor
  procesa 200.000, el retraso crece 800.000 por hora. En cinco horas son 4.000.000 de eventos por
  detrás. Si la retención es de un día, hay margen; si es de dos horas, ese consumidor ya ha
  perdido datos.

## Código

```python verificable
import hashlib

# Kafka garantiza el orden DENTRO de cada particion, no en el tema entero.
def particion(clave, n):
    # Kafka usa murmur2; aqui md5 solo para ilustrar una asignacion determinista.
    return int(hashlib.md5(clave.encode()).hexdigest(), 16) % n

N = 6
pedidos = [("A", 1), ("A", 2), ("B", 1), ("C", 1), ("D", 1), ("A", 3), ("B", 2), ("C", 2)]

por_particion = {}
for clave, numero in pedidos:
    por_particion.setdefault(particion(clave, N), []).append(f"{clave}{numero}")

for p in sorted(por_particion):
    print(f"particion {p}: {' '.join(por_particion[p])}")

# Todos los pedidos de un mismo cliente caen siempre en la misma particion.
particiones_de_a = {particion(c, N) for c, _ in pedidos if c == "A"}
print("particiones de la clave A:", len(particiones_de_a))   # -> particiones de la clave A: 1
print("particiones usadas:", len(por_particion))            # -> particiones usadas: 2
```

```python verificable
# Reparto de particiones entre los miembros de un grupo y vigilancia del retraso.
n_particiones, n_consumidores = 6, 4
asignacion = {c: [] for c in range(n_consumidores)}
for p in range(n_particiones):
    asignacion[p % n_consumidores].append(p)

for consumidor, trozos in asignacion.items():
    print(f"consumidor {consumidor}: particiones {trozos}")

print("paralelismo maximo:", n_particiones)                       # -> paralelismo maximo: 6
print("consumidores sin particion con 8:", max(0, 8 - 6))         # -> consumidores sin particion con 8: 2

# Si el productor va mas rapido que el consumidor, el retraso crece sin freno.
lag = (1_000_000 - 200_000) * 5
print("retraso tras 5 horas:", lag)                               # -> retraso tras 5 horas: 4000000
```

## Errores típicos

- **Suponer que el orden es global.** Solo está garantizado dentro de una partición. Con seis
  particiones y varios consumidores en paralelo, dos eventos de claves distintas pueden procesarse
  en cualquier orden relativo. Si tu lógica depende de ese orden, la clave del mensaje tiene que
  reflejarlo.
- **Añadir consumidores esperando más velocidad.** El paralelismo máximo de un grupo es el número
  de particiones. El consumidor número 7 sobre un tema de 6 particiones no procesa nada. Si
  necesitas más paralelismo, hay que aumentar las particiones, y eso cambia el reparto por clave.
- **Confirmar la compensación antes de procesar.** Da la garantía de como mucho una vez: si el
  proceso muere entre la confirmación y el procesamiento, ese mensaje no se vuelve a leer nunca y
  desaparece sin que salte ninguna alerta.
- **Confirmar después de procesar sin ser idempotente.** Es la garantía habitual (al menos una
  vez) y significa que, tras cualquier reinicio, el último tramo se reprocesa. Si el destino es un
  `INSERT`, aparecen duplicados; tiene que ser un `MERGE` por clave
  ([[idempotencia-y-reintentos]]).
- **Elegir la clave por comodidad.** Con un campo de alta cardinalidad como `pedido_id`, cada
  mensaje va a una partición distinta y pierdes todo el orden por cliente. Con uno de baja
  cardinalidad, como el país, concentras el tráfico en dos particiones y desequilibras el grupo.
- **Dimensionar la retención por el disco y no por el consumidor más lento.** La retención debe
  cubrir la peor caída que estés dispuesto a tolerar. Si retienes siete días y un consumidor está
  parado ocho, sus compensaciones apuntan a segmentos que ya no existen y hay que empezar de cero.

## Comprueba que lo sabes

:::quiz
p: Un tema tiene 6 particiones y tu grupo de consumidores tiene 10 miembros. ¿Qué ocurre?
o: Los 10 se reparten el trabajo y el grupo va un 66 % más rápido
o: Cuatro miembros se quedan sin partición asignada y no procesan nada
o: Kafka crea 4 particiones nuevas de forma automática
a: 2
e: Cada partición la lee un único miembro del grupo a la vez, así que el paralelismo está limitado por el número de particiones. Kafka no crea particiones por su cuenta: hay que aumentarlas a mano, y eso cambia la asignación por clave de todos los mensajes futuros.
:::

:::quiz
p: ¿Por qué se dice que la garantía habitual es «al menos una vez»?
o: Porque el consumidor confirma después de procesar, así que un fallo entre esas dos cosas repite el mensaje
o: Porque Kafka pierde mensajes cuando se llena el disco
o: Porque el productor envía cada mensaje dos veces por seguridad
a: 1
e: Procesar y confirmar son dos operaciones distintas, y no hay forma de hacerlas atómicas sin transacciones. Si el proceso muere en medio, el mensaje se vuelve a entregar y hay que evitar que eso duplique el resultado. Por eso el destino tiene que ser idempotente.
:::

:::trampa
Vigila dos cosas a la vez: el retraso del consumidor y la antigüedad del mensaje más viejo sin
consumir. El retraso puede ser pequeño y aun así estar a punto de perder datos, si la retención
está a punto de borrar el segmento que ese consumidor todavía no ha leído.
:::
