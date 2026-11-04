---
id: streaming-tiempo-real
titulo: "Streaming: ventanas y marcas de agua"
fase: 4
nivel: experto
rutas: [de]
prerequisitos: [kafka-y-colas, batch-vs-streaming, ingesta-incremental-y-cdc]
tags: [streaming, ventanas, tiempo-de-evento, marcas-de-agua, tardanzas]
resumen: Cuándo ocurrió un evento no es cuándo llegó: ventanas, marcas de agua, tolerancia a tardanzas y la letra pequeña de exactamente una vez.
fuentes: ["Akidau et al. (2015), 'The Dataflow Model'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11"]
---

## En una frase

En un flujo, el instante en que un evento ocurrió y el instante en que tu proceso lo vio son dos
cosas distintas, y casi todo el trabajo difícil del streaming consiste en decidir cuánto tiempo
esperas a los que llegan tarde antes de dar una ventana por cerrada.

## La idea

Piensa en un peaje que quiere contar cuántos coches pasan por hora. El coche cruzó a las 8:59, pero
la cámara envía la foto al servidor central y la foto llega a las 9:01 y medio. Si cierras la
cuenta de la hora 8:00 a 9:00 a las 9:00 en punto, ese coche se ha perdido o se ha contado en la
hora equivocada. Ese es todo el problema del streaming en una frase: **el dato lleva su propia
fecha, y esa fecha no coincide con la de llegada**.

Hay tres relojes en juego y conviene no mezclarlos:

1. **Tiempo de evento:** cuándo ocurrió de verdad. Viene dentro del propio dato, puesto por el
   sistema que lo originó.
2. **Tiempo de ingesta:** cuándo lo recibió el intermediario. Es el que estampa Kafka al guardar
   el registro. Sirve para saber cuánto tarda un productor en publicar, nada más.
3. **Tiempo de proceso:** cuándo lo ve la máquina que lo está tratando. Lo pone el reloj local de
   esa máquina.

La regla que resuelve el 90 % de las dudas: **para calcular, usa tiempo de evento; para operar,
usa tiempo de proceso**. Los resultados por hora natural se agrupan por tiempo de evento, porque
si no, un pico de tráfico o un reinicio mueven los datos de una ventana a otra y los mismos datos
dan resultados distintos en cada ejecución. Las alertas de «el pipeline lleva veinte minutos
atascado» se miden en tiempo de proceso, porque el retraso es un hecho sobre tu sistema, no sobre
el dato.

El problema de fondo es que **nunca puedes saber si has visto ya todos los eventos de un instante**.
Puede aparecer uno más viejo en cualquier momento. Como no hay certeza, lo único que puedes hacer
es tomar una decisión: dejar de esperar. Esa decisión se llama **marca de agua** (*watermark*) y es
una promesa, no un hecho: «no voy a volver a aceptar eventos anteriores a esta hora». Se calcula
como el tiempo de evento más nuevo que has visto menos un margen de retraso permitido.

Con esa promesa ya se puede cerrar y emitir una ventana. Un evento que llega con tiempo de evento
por detrás de la marca de agua es un **evento tardío**, y tienes que decidir explícitamente qué
hacer con él, porque las tres opciones son legítimas y significan cosas distintas:

- **Descartarlo**, contándolo en una métrica. Es lo correcto cuando el resultado se publica y ya
  nadie va a corregirlo.
- **Emitir una corrección.** Se vuelve a emitir el resultado de la ventana con el dato nuevo y el
  consumidor reemplaza el anterior. Es lo correcto cuando el número final importa más que la
  inmediatez, y obliga a que el consumidor sepa hacer actualizaciones, no solo inserciones.
- **Ampliar el margen** (`allowed lateness`). Se sigue aceptando tardíos hasta un límite y después
  se descartan. Cada minuto de margen es un minuto más de estado guardado y de latencia.

Sobre las **ventanas**, hay cuatro formas y se eligen por la pregunta, no por gusto:

- **Fijas (tumbling):** no solapan. 10:00-10:05, 10:05-10:10. Cada evento cae en exactamente una.
- **Deslizantes (hopping/sliding):** se solapan. Una ventana de cinco minutos que avanza cada
  minuto genera cinco ventanas simultáneas sobre cada evento. Sirven para medias móviles.
- **De sesión:** agrupan eventos separados entre sí por menos de un hueco de inactividad. El
  tamaño de la ventana no se fija de antemano, lo decide el comportamiento.
- **Global:** una sola ventana para todo el flujo, que solo tiene sentido con un disparador
  (por ejemplo, emitir cada minuto el acumulado).

Y la letra pequeña de **exactamente una vez**: la garantía que ofrecen los motores cubre el
circuito de leer del intermediario, actualizar el estado interno y escribir en el intermediario,
todo dentro de transacciones. En cuanto el destino es un sistema externo sin transacciones —una
pasarela de pago, un fichero en un almacén de objetos—, lo que tienes es al menos una vez más
idempotencia en el destino ([[exactamente-una-vez]]).

## Definición formal

Sea `t_e` el tiempo de evento de un registro y `t_p` el tiempo de proceso en el que el sistema lo
trata. Sea `d` el **retraso permitido**, una constante de configuración expresada en unidades de
tiempo.

La **marca de agua** en un momento dado es:

:::formula
W = max(t_e vistos) − d
:::

`W` es monótona: nunca retrocede. Un registro es **puntual** si `t_e ≥ W` cuando llega, y
**tardío** si `t_e < W`.

Una ventana con intervalo `[inicio, fin)` acumula los registros cuyo `t_e` cae dentro. Se emite
cuando la marca de agua alcanza su final:

:::formula
ventana [inicio, fin) se emite cuando W ≥ fin
:::

Con un **límite de tardanza** `a`, se sigue aceptando un tardío mientras `W < fin + a`; a partir de
ahí se descarta y se cuenta. `a = 0` significa que en cuanto la ventana se emite, cualquier
corrección se tira.

Dos consecuencias que conviene tener escritas:

- **`d` decide el equilibrio entre latencia y corrección.** Con `d = 2 min`, un resultado puede
  tardar dos minutos más que el evento más nuevo; con `d = 30 min`, media hora.
- **`W` no avanza si el flujo se queda quieto.** Si una partición deja de recibir datos, su
  `max(t_e vistos)` se congela y la marca de agua con él: la última ventana de la noche no se
  emitiría hasta el día siguiente. Por eso los motores tienen un tiempo de inactividad que
  adelanta `W` al tiempo de proceso cuando no llega nada.

| Reloj | Quién lo pone | Para qué sirve |
| --- | --- | --- |
| Evento | El sistema que origina el dato | Agrupar, agregar y decidir el resultado |
| Ingesta | El intermediario, al almacenar | Diagnosticar cuánto tarda el productor en publicar |
| Proceso | La máquina que procesa | Operar: retraso, alertas, marcas de agua de emergencia |

## Ejemplo

Ventanas fijas de un minuto, retraso permitido `d = 2 minutos` y límite de tardanza `a = 3 minutos`.
Llegan siete eventos:

```
evento  t_evento  t_proceso  ventana          llega con retraso de
e1      10:00:30  10:00:31   [10:00, 10:01)   1 s
e2      10:01:10  10:01:12   [10:01, 10:02)   2 s
e4      10:02:05  10:02:06   [10:02, 10:03)   1 s
e3      10:00:45  10:04:20   [10:00, 10:01)   3 min 35 s
e5      10:01:50  10:06:40   [10:01, 10:02)   4 min 50 s
e6      10:08:00  10:08:01   [10:08, 10:09)   1 s
e7      10:00:10  10:09:00   [10:00, 10:01)   8 min 50 s
```

Recorrido paso a paso:

- Tras `e4`, el mayor `t_e` visto es 10:02:05, así que la marca de agua está en
  `10:02:05 − 2 min = 10:00:05`. Ninguna ventana se ha cerrado todavía.
- `e3` llega a las 10:04:20 con `t_e = 10:00:45`. Es mayor que la marca de agua (10:00:05), así que
  es puntual: entra en su ventana natural, `[10:00, 10:01)`. Fíjate en que llegó tres minutos y
  medio tarde y aun así se contó bien, porque el margen lo permitía.
- `e5` llega a las 10:06:40 con `t_e = 10:01:50`, también por delante de la marca. Entra en
  `[10:01, 10:02)`.
- `e6` sí mueve el reloj: el mayor `t_e` pasa a 10:08:00 y la marca de agua salta a 10:06:00. En
  ese instante se cierran y emiten todas las ventanas cuyo final ya ha pasado: `[10:00, 10:01)` con
  2 eventos (`e1`, `e3`), `[10:01, 10:02)` con 2 (`e2`, `e5`) y `[10:02, 10:03)` con 1 (`e4`).
- `e7` llega a las 10:09:00 con `t_e = 10:00:10`, por detrás de la marca de agua de 10:06:00: es
  tardío. Como el límite de tardanza es de 3 minutos, la ventana `[10:00, 10:01)` quedó cerrada
  definitivamente a las 10:04:00 y el evento **se descarta**. Si `a` fuera de 10 minutos, se
  habría vuelto a emitir esa ventana con 3 eventos en lugar de 2.
- Y la ventana `[10:08, 10:09)`, que contiene `e6`, se queda abierta con 1 evento y no se emite: la
  marca de agua sigue en 10:06:00 porque no ha llegado nada más nuevo. Sin un tiempo de inactividad
  que adelante el reloj, esa ventana no se cierra.

## Código

```python verificable
from datetime import datetime, timedelta

def t(hhmmss):
    return datetime(2024, 3, 1, *map(int, hhmmss.split(":")))

RETRASO = timedelta(minutes=2)    # d: cuanto esperamos antes de cerrar una ventana
TARDANZA = timedelta(minutes=3)   # a: cuanto seguimos aceptando eventos tardios

# (t_evento, t_proceso, id), en el orden en que el flujo los entrega.
eventos = [(t("10:00:30"), t("10:00:31"), "e1"),
           (t("10:01:10"), t("10:01:12"), "e2"),
           (t("10:02:05"), t("10:02:06"), "e4"),
           (t("10:00:45"), t("10:04:20"), "e3"),
           (t("10:01:50"), t("10:06:40"), "e5"),
           (t("10:08:00"), t("10:08:01"), "e6"),
           (t("10:00:10"), t("10:09:00"), "e7")]

ventanas, descartados = {}, []
max_evento, marca = None, None

for te, tp, ident in eventos:
    max_evento = te if max_evento is None else max(max_evento, te)
    nueva = max_evento - RETRASO
    marca = nueva if marca is None else max(marca, nueva)   # la marca nunca retrocede

    inicio = te.replace(second=0, microsecond=0)
    if te < marca and marca > inicio + timedelta(minutes=1) + TARDANZA:
        descartados.append(ident)
    else:
        ventanas.setdefault(inicio, []).append(ident)

for inicio in sorted(ventanas):
    fin = inicio + timedelta(minutes=1)
    print(f"[{inicio:%H:%M}, {fin:%H:%M}) -> {len(ventanas[inicio])} eventos")

print("marca de agua final:", f"{marca:%H:%M:%S}")   # -> marca de agua final: 10:06:00
print("descartados:", descartados)                  # -> descartados: ['e7']
```

```python verificable
# Por que "al menos una vez" obliga a que el destino sea idempotente.
def insertar(destino, clave, valor):
    destino.append((clave, valor))

def merge(destino, clave, valor):
    destino[:] = [(k, v) for k, v in destino if k != clave]
    destino.append((clave, valor))

lote = [("a", 1), ("b", 2)]
reintento = [("b", 2), ("c", 3)]      # tras un fallo, el consumidor reprocesa desde su compensacion

con_insert = []
for par in lote + reintento:
    insertar(con_insert, *par)
print("con INSERT:", len(con_insert), "filas")        # -> con INSERT: 4 filas

con_merge = []
for par in lote + reintento:
    merge(con_merge, *par)
print("con MERGE:", len(con_merge), "filas")          # -> con MERGE: 3 filas
print("claves:", sorted(k for k, _ in con_merge))     # -> claves: ['a', 'b', 'c']
```

## Errores típicos

- **Agrupar por tiempo de proceso.** Si la ventana la decide el reloj de la máquina que procesa, un
  pico de tráfico, un despliegue o un reinicio mueven los datos de una ventana a otra, y el mismo
  flujo da resultados distintos según cuándo lo ejecutes. Agrupa por tiempo de evento y usa el de
  proceso solo para operar.
- **Creer que la marca de agua garantiza que no habrá más tardíos.** Es una apuesta configurable,
  no un teorema. Siempre puede aparecer un evento más viejo. Decide por escrito qué haces con él:
  descartarlo y contabilizarlo, o emitir una corrección.
- **Poner un retraso permitido enorme «para no perder nada».** Cada minuto de margen son minutos de
  latencia en el resultado y más estado que guardar y copiar en cada punto de control. Con 30
  minutos de margen, ningún panel enseña nada hasta media hora después del evento, y el tamaño del
  estado se multiplica por el número de ventanas abiertas y de claves distintas.
- **Olvidar que el reloj se congela cuando el flujo se queda quieto.** Sin un tiempo de inactividad
  que adelante la marca de agua al tiempo de proceso, la última ventana antes de un parón no se
  emite hasta que vuelva a llegar algo. Es el clásico «el panel de esta noche está vacío».
- **Confundir el exactamente una vez del motor con exactamente una vez de verdad.** La garantía
  cubre leer del intermediario, actualizar el estado y escribir en el intermediario. Si el destino
  final es una API externa o un fichero sin confirmación transaccional, sigues teniendo al menos
  una vez y necesitas idempotencia en el destino ([[exactamente-una-vez]]).
- **Elegir el hueco de sesión sin mirar el negocio.** Un hueco de 30 minutos sobre usuarios que
  navegan en ráfagas de 45 parte cada sesión en dos; uno de dos horas une la visita de la mañana
  con la de la tarde y produce sesiones que no existieron. El hueco no se deduce de los datos: se
  elige con quien va a usar el resultado delante.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia entre tiempo de evento y tiempo de proceso?
o: El de evento lo pone el sistema que origina el dato; el de proceso, la máquina que lo trata
o: El de evento siempre es posterior al de proceso
o: Son idénticos cuando los relojes de las máquinas están sincronizados
a: 1
e: El tiempo de evento viaja dentro del dato y describe cuándo ocurrió el hecho; el de proceso describe cuándo tu sistema lo tocó. Sincronizar los relojes reduce el retraso, pero con un intermediario, un reintento o un consumidor lento los dos valores siguen difiriendo.
:::

:::quiz
p: Con un retraso permitido de 2 minutos, ¿cuándo se emite la ventana [10:00, 10:01)?
o: En cuanto llega el primer evento que cae dentro de ella
o: Cuando la marca de agua alcanza las 10:01:00, lo que exige haber visto un evento con tiempo de evento igual o posterior a las 10:03:00
o: A las 10:01:00 del reloj de la máquina que procesa
a: 2
e: La marca de agua va dos minutos por detrás del tiempo de evento más nuevo visto, así que para llegar a 10:01:00 hace falta haber visto las 10:03:00. La tercera opción es usar tiempo de proceso para decidir el contenido de la ventana, que es justo el error que se comete al principio.
:::

:::quiz
p: ¿Qué significa exactamente que un evento sea «tardío»?
o: Que su tiempo de evento es anterior a la marca de agua cuando llega
o: Que su tiempo de proceso es anterior a su tiempo de evento
o: Que llegó más de un segundo después de producirse
a: 1
e: Un evento es tardío en relación con la marca de agua, no con un reloj de pared: llega después de que el sistema haya decidido no esperar más a esa parte del tiempo. Lo que hagas con él —descartarlo, corregir la ventana o ampliar el margen— es una decisión de diseño explícita.
:::

:::aviso
Elige el retraso permitido con el negocio delante, no con el miedo. Cada minuto de margen es
latencia en el resultado y estado que hay que guardar y copiar. Si el panel se mira a las 9:00 y
los datos son del día anterior, un margen de dos minutos sobra.
:::
