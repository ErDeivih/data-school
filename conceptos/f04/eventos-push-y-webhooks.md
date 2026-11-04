---
id: eventos-push-y-webhooks
titulo: Eventos push y webhooks
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [apis-rest, idempotencia-y-reintentos]
tags: [webhooks, eventos, idempotencia]
resumen: Cuando el origen empuja en vez de esperar a que lo consultes: cómo verificar la firma, por qué llegan duplicados y qué hace falta para no inundar la tabla.
fuentes: ["Stripe (2024), 'Webhooks best practices'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11"]
---

## En una frase

Un webhook es una llamada HTTP que el proveedor hace a tu servidor cuando ocurre algo, y llega
al menos una vez, desordenado y a veces repetido: tu trabajo es que eso no importe.

## La idea

Sondear una API cada cinco minutos funciona hasta que no: gastas peticiones, llegas tarde y te
pierdes lo que ocurrió entre dos consultas. El modelo push lo invierte: tú publicas una URL y el
proveedor te avisa. Es más eficiente y más frágil, porque ahora el que decide cuándo llega el dato
es otro.

La fragilidad tiene tres formas. **Llega dos veces**: si tu servidor tarda o devuelve un error, el
proveedor reintenta, y un reintento no significa que el primer intento no se procesara.
**Llega desordenado**: dos eventos del mismo objeto pueden llegar invertidos. **Llega sin
autenticar**: cualquiera puede llamar a tu URL, así que hay que verificar que viene de quien dice.

La respuesta a las tres es la misma que en cualquier ingesta: una clave de evento única, una
operación idempotente y una firma que verifique el origen. Con eso, un reintento es inofensivo y un
duplicado se descarta.

:::aviso
El webhook no es una fuente de verdad, es una notificación. Si te importa el estado final del
objeto, además de guardar el evento pide el objeto por la API y guarda esa versión. Así un evento
perdido no deja un hueco permanente: el siguiente lo corrige.
:::

## Definición formal

Un webhook es una petición `POST` con un cuerpo y dos cabeceras que hay que comprobar:

:::formula
firma = HMAC_SHA256( secreto, timestamp + "." + cuerpo )        y rechaza si |ahora − timestamp| > 5 min
:::

- **cuerpo** — el evento en JSON, con un identificador único (`id` o `event_id`).
- **firma** — el hash calculado con un secreto compartido; se compara en tiempo constante.
- **timestamp** — evita que alguien reenvíe una petición antigua capturada (ataque de repetición).
- **clave de idempotencia** — el `event_id`; se guarda una sola vez y se descarta el resto.

**Garantía real: entrega al menos una vez.** Nadie promete exactamente una. Por eso el consumidor
tiene que ser idempotente: procesar dos veces el mismo evento debe dejar el mismo estado que
procesarlo una.

## Ejemplo

Mil pedidos, cada uno con su evento, y un 7,7 % de reintentos por el motivo que sea:

- Entregas recibidas: 1.077.
- Eventos únicos: 1.000.
- Duplicados: 77.

Sin idempotencia, la tabla de pedidos tendría 1.077 filas y la facturación cobraría 77 pedidos dos
veces. Con una clave única y un `MERGE`, las 1.077 entregas dejan 1.000 filas y el reintento es
inofensivo.

## Código

```python verificable
# 1.000 eventos y 77 reintentos: qué pasa con y sin clave de idempotencia
ids = list(range(1000))
entregas = ids + [i for i in ids if i % 13 == 0]

vistos = set()
duplicados = 0
for i in entregas:
    if i in vistos:
        duplicados += 1
    else:
        vistos.add(i)

print(f"entregas {len(entregas)}")          # -> entregas 1077
print(f"unicos {len(vistos)}")               # -> unicos 1000
print(f"duplicados {duplicados}")            # -> duplicados 77
print(f"cobertura {len(vistos) / 1000:.1%}")  # -> cobertura 100.0%
```

La última línea demuestra que no se pierde nada: todos los eventos llegaron al menos una vez. El
reintento no es un problema de pérdida, es un problema de repetición.

:::claves
- `if i in vistos` sobre un `set` es O(1) de media; con una lista sería O(n) y se notaría con
  millones de eventos.
- La clave es el `id` del evento, no el `id` del pedido: dos eventos distintos del mismo pedido son
  legítimos y hay que procesarlos los dos.
- Aquí se guarda en memoria; en producción va una restricción `UNIQUE` en la base de datos, que es
  la única forma de que la idempotencia sobreviva a dos procesos en paralelo.
- `len(vistos) / 1000` compara con el número de eventos esperado, no con las entregas. Comparar con
  las entregas daría 92,8 % y parecería que faltan datos.
- El 13 es arbitrario: sirve para simular reintentos. En el mundo real el reintento sigue una
  política de espera creciente y suele acabar en una cola de mensajes muertos.
:::

## Errores típicos

- **Procesar sin clave de idempotencia.** Un reintento duplica filas y, si hay dinero de por medio,
  cobra dos veces. Es el fallo más caro y el más frecuente.
- **No verificar la firma.** Cualquiera puede llamar a tu URL y meter datos falsos. Se verifica
  siempre, incluso en desarrollo.
- **Comparar la firma con `==`.** La comparación normal filtra información por tiempo de respuesta.
  Usa una comparación en tiempo constante.
- **Responder tarde.** El proveedor tiene un tiempo máximo de espera; si procesas antes de
  responder, los reintentos llegarán mientras aún trabajas. Responde rápido con un 2xx y procesa en
  una cola.
- **Asumir orden.** Dos eventos del mismo objeto pueden llegar invertidos. Si el orden importa,
  guarda la marca de tiempo del evento y aplica el último estado, no el último que llegó.
- **Depender solo del webhook.** Un evento perdido deja un hueco para siempre. Complementa con una
  reconciliación periódica contra la API.

:::practica
enunciado: Recibes 10.000 entregas de webhook y esperas 9.200 eventos únicos. ¿Qué dos comprobaciones haces antes de dar la ingesta por buena y qué harías si la diferencia no cuadra?
pista: Una es de identidad (duplicados esperados), otra de cobertura (eventos que faltan).
solucion: Primero, contar cuántas entregas se descartan como duplicadas por `event_id`; segundo, comparar los eventos únicos con los 9.200 esperados. Si faltan, no es un problema de duplicados: hay eventos que nunca llegaron, así que se lanza una reconciliación contra la API para el periodo afectado y se revisa la cola de mensajes muertos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un webhook obliga a que el consumidor sea idempotente?
o: Porque la garantía real es entrega al menos una vez, así que habrá reintentos
o: Porque los webhooks llegan siempre dos veces por diseño
o: Porque el proveedor no permite responder con 200
a: 1
e: Nadie garantiza exactamente una entrega: si tu respuesta se pierde o llega tarde, el proveedor reintenta. La idempotencia convierte ese reintento en inofensivo.
:::

:::quiz
p: ¿Qué dos cosas comprueba la firma de un webhook?
o: Que la petición la envió quien tiene el secreto y que no es una repetición antigua
o: Que el JSON es válido y que el evento existe
o: Que el servidor está disponible y que hay red
a: 1
e: El HMAC demuestra el origen porque solo quien tiene el secreto puede calcularlo; el timestamp dentro de la firma limita la ventana de validez y bloquea el reenvío de una petición capturada.
:::
