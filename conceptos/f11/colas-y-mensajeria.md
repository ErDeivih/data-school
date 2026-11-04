---
id: colas-y-mensajeria
titulo: Colas y mensajería
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [apis-rest, idempotencia-en-apis, batch-vs-streaming]
tags: [asincronia, desacoplamiento, reintentos, fiabilidad]
resumen: Desacoplar productor y consumidor, reintentar sin duplicar y aceptar que ordenar cuesta dinero.
fuentes: ["Hohpe y Woolf (2003), 'Enterprise Integration Patterns'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11"]
---

## En una frase

Una cola es un buzón entre dos programas: el productor deja el mensaje y sigue a lo suyo, el
consumidor lo recoge cuando puede, y en medio hay que decidir qué pasa si el consumidor falla,
si el mensaje llega dos veces o si el orden importa.

## La idea

Sin cola, cuando alguien hace un pedido en tu tienda, la petición HTTP tiene que generar la
factura, avisar al almacén, mandar el correo y actualizar las recomendaciones. Son cuatro
cosas, y si el servidor de correo tarda tres segundos, el cliente está esperando tres segundos
mirando un botón girando. Peor: si el correo falla, ¿se pierde el pedido?

Con cola, la petición solo escribe «pedido 251 creado» en el buzón y responde en 20 ms. Cada
consumidor recoge el mensaje y hace su parte. El servidor de correo puede estar caído media
hora sin que nadie deje de comprar: los mensajes se acumulan y se procesan cuando vuelva.

Ese desacoplamiento trae tres problemas nuevos que son el verdadero contenido del tema:

1. **¿Y si el consumidor se cae a mitad?** El mensaje no se puede borrar antes de terminar el
   trabajo. Se confirma (*ack*) al final. Si el consumidor muere antes de confirmar, la cola
   vuelve a entregar el mensaje: **entrega al menos una vez**. Y eso significa que tu consumidor
   tiene que aguantar el mismo mensaje dos veces, es decir, ser idempotente.
2. **¿Y si el mensaje es veneno?** Un mensaje con un formato que tu código no sabe procesar
   fallará siempre. Si se reintenta indefinidamente, bloquea la cola para todos los mensajes que
   van detrás. Después de N intentos se manda a una **cola de mensajes muertos** y se investiga
   a mano.
3. **¿Y el orden?** Una cola con un solo consumidor mantiene el orden de llegada. En cuanto hay
   varios consumidores leyendo de la misma cola, el orden se pierde: dos pedidos del mismo
   cliente pueden procesarse al revés. Para eso están las **claves de partición**: todos los
   mensajes con la misma clave van a la misma partición y ahí sí se respetan el orden, aunque
   el orden entre particiones distintas no signifique nada.

La decisión importante es qué garantía necesitas. **Como mucho una vez** (se envía y se olvida)
pierde mensajes y es aceptable para métricas y registros. **Al menos una vez** es lo que dan
casi todas las colas y lo que obliga a la idempotencia del consumidor. **Exactamente una vez**
de verdad es muy caro y en la práctica significa «al menos una vez más un consumidor
idempotente con deduplicación».

## Definición formal

Términos que conviene fijar, porque cada tecnología les cambia el nombre:

- **Productor:** quien publica. **Consumidor:** quien procesa. **Mensaje:** la unidad que viaja,
  con su cuerpo y sus metadatos.
- **Cola (queue):** muchos consumidores compiten por cada mensaje y cada mensaje lo procesa uno
  solo. Es el modelo de reparto de trabajo.
- **Tema con suscriptores (topic, pub/sub):** cada suscriptor recibe su propia copia del
  mensaje. Es el modelo de difusión.
- **Confirmación (ack):** señal de que el mensaje se ha procesado y se puede borrar.
  **Visibilidad:** mientras un consumidor lo tiene sin confirmar, el mensaje queda invisible
  para los demás; si no confirma en ese plazo, vuelve a la cola.
- **Cola de mensajes muertos (DLQ):** destino de los mensajes que han agotado sus reintentos.
- **Partición:** división ordenada de un tema. La clave de partición determina a cuál va cada
  mensaje, y el orden solo se garantiza dentro de una partición.
- **Compensación (offset):** la posición hasta la que un consumidor ha leído en su partición.
  Si vuelve a una posición anterior, reprocesa; es la herramienta del reproceso.

**Reintentos con espera creciente.** Reintentar de inmediato contra un servicio caído es
contraproducente: multiplica la carga justo cuando el servicio está peor. La espera crece:

:::formula
espera(n) = min(espera_max, base · 2^(n−1)) + aleatorio
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `espera(n)` | Lo que se espera antes de lanzar el reintento número n | s | Es el resultado: sin tope crece sin límite y el mensaje se queda atascado más que la propia caída |
| `n` | Número del intento, empezando en 1 | — | Cada intento duplica la espera anterior hasta el tope; después todas las esperas son iguales |
| `base` | Espera del primer reintento (0,5 o 1 s en la práctica) | s | Desplaza toda la curva hacia arriba y hace que se alcance el tope antes: con base 2 s, el tope de 30 s se toca en el quinto intento |
| `espera_max` | Tope de la espera para no acabar esperando horas | s | Alarga la rama creciente: con 300 s, el mensaje puede tardar cinco minutos en volver a intentarse |
| `aleatorio` | El *jitter* que se suma a cada reintento | s | No cambia la media, reparte a miles de clientes para que no coincidan en el mismo instante; sin él, todos los que fallaron a la vez vuelven a la vez |
:::

- `n` — número del intento, empezando en 1.
- `base` — espera del primer reintento, típicamente 0,5 o 1 segundo.
- `espera_max` — tope, por ejemplo 30 segundos, para no acabar esperando horas.
- `aleatorio` — jitter: reparte los reintentos de muchos clientes para que no lleguen todos a
  la vez.

Que un consumidor sea **idempotente** significa que procesar el mismo mensaje dos veces deja el
sistema igual que procesarlo una. Se consigue con una clave de operación única y una tabla de
«ya procesados», o escribiendo de forma naturalmente idempotente (un `INSERT ... ON CONFLICT DO
NOTHING`, un `SET estado = 'enviado'` sin incrementos).

## Ejemplo

Un pico de 1.000 pedidos en un minuto. El productor publica en la cola `pedidos.creados` y
responde; cuatro consumidores procesan unos 250 cada uno. Si un consumidor se cae en el mensaje
300, ese mensaje no se confirma, su visibilidad caduca a los 30 segundos y vuelve a la cola: lo
recoge otro. El pedido 300 se procesa una vez, pero **el consumidor puede verlo dos veces** si
el fallo ocurrió después de escribir en la base de datos y antes de confirmar. De ahí que el
consumidor compruebe antes de escribir.

Con la espera creciente y base de 1 segundo, los reintentos de un mismo mensaje esperan 1, 2, 4,
8, 16 y luego 30 segundos indefinidamente si no se pone tope de intentos. Con un tope de 5
intentos, las esperas acumuladas son 1 + 2 + 4 + 8 = **15 segundos** antes de mandarlo a la cola
de muertos; con 6 intentos serían 31. La cuenta es la que hay que tener clara antes de elegir el
tope: cada intento de más duplica casi todo el tiempo que el mensaje lleva esperando.

Y el orden: si los mensajes de un mismo cliente deben procesarse en orden, se publican con
`clave = cliente_id`. Todos los de la clienta 7 van a la misma partición y se leen en orden;
los de la clienta 7 y los del cliente 9 pueden ir en cualquier orden relativo, y eso casi nunca
importa.

## Código

```python verificable
# Tres formas de entregar el mismo mensaje y lo que pasa cuando el consumidor falla.
def intento_entrega(exito):
    return exito                    # el parametro simula el resultado: True funciona, False falla

def at_most_once(exito):
    intento_entrega(exito)          # se envia una vez y se olvida
    return "perdido" if not exito else "procesado"
    # expresion condicional: primero el valor de la izquierda, que es el de la condicion cierta

def at_least_once(exito, max_reintentos=3):
    for _ in range(max_reintentos):     # _ es la variable de usar y tirar: no se lee la vuelta
        if intento_entrega(exito):
            return "procesado"          # sale en el primer intento que funcione
    return "a la cola de muertos"       # agoto los reintentos: el mensaje es veneno

print("at-most-once, fallo  ->", at_most_once(False))            # -> perdido
print("at-least-once, fallo ->", at_least_once(False))           # -> a la cola de muertos
print("at-least-once, exito ->", at_least_once(True))            # -> procesado

# Backoff exponencial con tope: el reintento 3 espera 4 s y del 6 en adelante, 30 s.
for intento in range(1, 8):
    espera = min(30, 2 ** (intento - 1))     # el tope es lo que aplana la curva
    print(f"reintento {intento}: espera {espera:>2} s")     # :>2 alinea los numeros de dos cifras
```

:::claves
- `at_most_once` **no reintenta nunca**: si el primer intento falla, devuelve "perdido" y ahí acaba. Es la garantía barata (métricas, registros) y la única que pierde mensajes; para un cobro no sirve.
- `at_least_once(False)` reintenta 3 veces y las 3 falla, así que va a la cola de muertos: el ejemplo es un mensaje veneno. Con un parámetro que fallara solo las dos primeras veces, el tercer intento devolvería "procesado" y el mensaje no se perdería.
- `max_reintentos=3` es el número de **intentos totales**, no de reintentos: `range(3)` da tres vueltas, es decir 1 intento original más 2 reintentos. El off-by-one clásico es confundir «5 reintentos» con «5 intentos» y quedarse corto justo cuando la caída dura.
- `min(30, 2 ** (intento - 1))` da 1, 2, 4, 8, 16, 30, 30, 30: sin el `min`, el reintento 20 esperaría 2^19 = 524.288 segundos, casi seis días, y el mensaje quedaría bloqueado más tiempo que la caída que intenta superar.
- La clave de deduplicación es la **tupla** `(clave, version)`: con solo el identificador del pedido, una versión corregida del mismo pedido se tomaría por duplicada y se perdería el cambio. Y sin `version`, cualquier reenvío legítimo con datos nuevos se ignoraría en silencio.
- `procesados` es un `set` **en memoria**: al reiniciar el proceso se vacía y el mismo mensaje vuelve a contarse. En producción esa tabla vive en la base de datos con una restricción de unicidad, que es la única defensa que sobrevive a un reinicio y a dos consumidores a la vez.
:::

:::figura
fichero: colas-espera-creciente
pie: Izquierda, la espera antes de cada reintento con `base = 1 s` y tope de 30: crece al doble hasta el sexto y a partir de ahí se aplana. La banda azul es el jitter, el poco de azar que se suma a cada espera; sin el tope, el reintento 20 esperaría casi seis días. Derecha, para qué sirve ese azar: quinientos clientes que reintentan tras el mismo fallo. Sin jitter coinciden todos en el mismo instante y el servicio que intenta recuperarse recibe un pico de 500 peticiones justo cuando está peor; con jitter repartido por medio segundo, cada décima de segundo llegan unas 50. La espera creciente le da aire al servicio y el jitter reparte a los clientes: las dos cosas juntas, no una.
fuente: figuras/colas-y-mensajeria-1.py
:::

```python verificable
# Por que el consumidor tiene que ser idempotente: la misma clave, dos entregas.
pedidos = {}
procesados = set()                  # set: la pertenencia es inmediata y no admite repetidos

def consumir(mensaje):
    clave = (mensaje["clave"], mensaje["version"])   # operacion + version, y tiene que ser tupla
    if clave in procesados:                          # esta es la comprobacion que da idempotencia
        return "duplicado ignorado"
    procesados.add(clave)
    pedidos[mensaje["pedido"]] = pedidos.get(mensaje["pedido"], 0) + 1
    # .get con 0 por defecto: la primera vez la clave no existe y un pedidos[...] daria KeyError
    return "procesado"

entrega = {"clave": "pedido-251", "version": 1, "pedido": 251}
print("primera entrega:", consumir(entrega))     # -> procesado
print("reintento:     ", consumir(entrega))      # -> duplicado ignorado
print("veces contabilizado el pedido 251:", pedidos[251])   # -> 1
print("mensajes vistos:", len(procesados))       # -> 1
```

```python ilustrativo
import pika

conexion = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
# la conexion TCP con el broker se abre una vez y se reutiliza para todos los mensajes
canal = conexion.channel()
canal.queue_declare(queue="pedidos.creados", durable=True)          # sobrevive al reinicio
canal.queue_declare(queue="pedidos.muertos", durable=True)

def procesar(cuerpo: bytes) -> None:
    escribir_factura(cuerpo)        # tiene que ser idempotente: puede repetirse

def al_recibir(canal, metodo, propiedades, cuerpo):
    try:
        procesar(cuerpo)
    except Exception as exc:
        intentos = (propiedades.headers or {}).get("x-intentos", 0) + 1
        # headers puede ser None: el "or {}" lo cambia por un diccionario vacio antes del .get
        if intentos >= 5:
            canal.basic_publish(exchange="", routing_key="pedidos.muertos", body=cuerpo,
                                properties=pika.BasicProperties(headers={"x-intentos": intentos}))
            # exchange vacio = publicar directo en esa cola; el reenvio lleva el contador subido
        else:
            canal.basic_publish(exchange="", routing_key="pedidos.creados", body=cuerpo,
                                properties=pika.BasicProperties(headers={"x-intentos": intentos}))
    finally:
        canal.basic_ack(metodo.delivery_tag)     # se confirma siempre: el reintento ya esta decidido

canal.basic_qos(prefetch_count=10)               # no acaparar mensajes sin procesar
canal.basic_consume(queue="pedidos.creados", on_message_callback=al_recibir)
# basic_consume solo registra el callback; el consumo empieza de verdad en start_consuming
canal.start_consuming()
```

## Errores típicos

- **Confirmar el mensaje antes de terminar el trabajo.** `basic_ack` al principio es perder
  mensajes cuando algo falla a mitad. Se confirma al final, cuando el efecto ya está guardado.
- **Suponer que un mensaje llega una sola vez.** La garantía real es al menos una vez, así que
  el mismo mensaje puede procesarse dos veces. Si tu consumidor incrementa un contador o envía
  un correo, necesitas una clave de operación o una tabla de deduplicación.
- **Reintentar sin espera creciente ni jitter.** Contra un servicio saturado, reintentar cada
  milisegundo añade leña al fuego y provoca tormentas de reintentos. Espera creciente con un
  poco de azar.
- **No tener cola de mensajes muertos.** Un mensaje veneno que falla siempre se reintenta para
  siempre y bloquea la cola. Con un tope de intentos y una cola aparte, el sistema sigue y tú
  puedes mirar el mensaje con calma.
- **Prometer orden sin particionar por clave.** Con varios consumidores sobre una misma cola,
  el orden de llegada no se conserva. Si de verdad importa, la clave de partición debe agrupar
  todo lo que tiene que ir en orden.
- **Hacer el mensaje gigante.** Mensajes de megabytes llenan los discos del bróker y obligan a
  copiar mucho en cada reintento. Lo grande va a un almacén de objetos y en el mensaje viaja la
  referencia.
- **Usar la cola como base de datos.** El bróker no está para consultas ni para búsquedas: los
  mensajes se consumen y desaparecen. El estado consultable vive en su base de datos.

## Comprueba que lo sabes

:::quiz
p: Tu consumidor cobra al cliente y después confirma el mensaje. Se cae entre las dos cosas. ¿Qué ocurre?
o: El mensaje se pierde y el cobro queda sin procesar
o: El mensaje vuelve a la cola y puede cobrarse dos veces, así que el consumidor debe ser idempotente
o: El bróker cancela el cobro automáticamente
a: 2
e: Como no hubo confirmación, el mensaje vuelve a entregarse: es la garantía al menos una vez. El bróker no sabe nada del cobro, así que la única defensa es que el consumidor detecte que ya lo hizo, con una clave de operación o una restricción de unicidad en la base de datos.
:::

:::quiz
p: ¿Para qué sirve una clave de partición en un sistema de mensajería?
o: Para repartir la carga entre los nodos del bróker y garantizar el orden dentro de cada partición
o: Para cifrar los mensajes con una clave distinta por cliente
o: Para que cada consumidor reciba una copia del mensaje
a: 1
e: La partición reparte el trabajo, y los mensajes con la misma clave caen siempre en la misma partición, donde se leen en orden. Lo que no garantiza es el orden entre particiones distintas. La copia para cada consumidor es el modelo de temas con suscriptores, no la partición.
:::

:::quiz
p: ¿Por qué los reintentos se espacian cada vez más y con algo de aleatoriedad?
o: Porque el bróker limita los reintentos por segundo y hay que esperar el turno
o: Porque un servicio caído o saturado no mejora si le llegan más peticiones, y el azar evita que todos los clientes reintenten en el mismo instante
o: Porque así el mensaje caduca antes y se descarta
a: 2
e: Reintentar de inmediato durante una caída empeora la situación del servicio que intentas recuperar. La espera creciente le da aire y el jitter reparte los reintentos de miles de clientes para que no coincidan. Los reintentos no cambian la caducidad del mensaje.
:::

:::practica
enunciado: Diseña el flujo de una tienda que confirma un pedido: qué mensajes se publican, qué consumidores hay, qué pasa si el de correo está caído y cómo evitas que un pedido se cobre dos veces.
pista: Un solo mensaje no tiene por qué generar todas las tareas; piensa en un tema con varios suscriptores.
solucion: La petición HTTP valida el pedido, lo guarda con estado `pendiente` y publica `pedido.creado` (con `clave = pedido_id`) en un tema. Tres suscriptores independientes lo consumen: facturación, almacén y notificaciones. Cada uno confirma al terminar su efecto. Si el de correo está caído, los mensajes se acumulan en su grupo de consumo y se procesan al volver, sin afectar a los otros dos. El cobro se protege con una clave de idempotencia (`cobro-<pedido_id>`) o con una restricción de unicidad en la tabla de cobros, porque el consumidor puede recibir el mismo mensaje dos veces. Los mensajes que fallen cinco veces van a `pedido.muerto` con su traza.
:::

:::nota
Cada tecnología cambia los nombres: en RabbitMQ se habla de colas, intercambios y enrutado por
clave; en Kafka, de temas, particiones y compensaciones que el consumidor gestiona. El modelo
mental es el mismo, y confundir «cola» con «tema» es la causa habitual de que un mensaje se
procese una vez cuando esperabas que llegara a tres servicios.
:::

:::trampa
Si tu consumidor no es idempotente y aumentas los reintentos, acabas de aumentar la probabilidad
de duplicar. La idempotencia no es un detalle de calidad: es el requisito que hace posible
reintentar. Antes de subir el número de reintentos, comprueba que procesar dos veces el mismo
mensaje no rompe nada.
:::
