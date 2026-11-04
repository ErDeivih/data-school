---
id: idempotencia-en-apis
titulo: Idempotencia en APIs
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [apis-rest, autenticacion-y-autorizacion]
tags: [http, reintentos, backend, fiabilidad]
resumen: Repetir una petición no debe repetir el efecto: claves de idempotencia, respuestas guardadas y los detalles que deciden si un reintento te salva o te duplica el cobro.
fuentes: ["Fielding, Nottingham y Reschke (2022), 'HTTP Semantics', RFC 9110, seccion 9.2.2", "Stripe, 'Idempotent requests' (documentacion oficial)"]
---

## En una frase

Una operación es idempotente cuando aplicarla dos veces deja el sistema igual que aplicarla
una, y en una API eso no se consigue prohibiendo los reintentos (que son inevitables), sino
haciendo que el segundo intento devuelva la misma respuesta que el primero.

## La idea

El cliente manda un `POST /pagos` con 250 EUR. El servidor cobra, guarda el pago y empieza a
escribir la respuesta. Se corta la conexión. El cliente ve un error de red, que es
exactamente lo que vería si la petición no hubiera llegado nunca. Tiene dos opciones y las dos
son malas si el servidor no le ayuda: reintentar y arriesgarse a cobrar dos veces, o no
reintentar y arriesgarse a que el cliente se quede sin pagar.

Ese dilema no se resuelve en el cliente. Se resuelve en el servidor, aceptando que la misma
petición puede llegar varias veces y recordando qué hizo la primera. La pieza que lo hace
posible es la **clave de idempotencia**: un identificador que el cliente genera una vez y
manda en todas las repeticiones de esa operación. El servidor lo guarda junto con la
respuesta y, si vuelve a verlo, devuelve lo que respondió antes sin volver a ejecutar nada.

Conviene separar dos cosas que se mezclan todo el tiempo:

1. **Idempotencia del verbo HTTP.** `GET`, `PUT` y `DELETE` son idempotentes por definición en
   HTTP: dos `PUT` con el mismo cuerpo sobre el mismo recurso dejan el recurso en el mismo
   estado, y dos `DELETE` dejan el recurso borrado. `POST` **no** es idempotente: cada envío
   crea un recurso nuevo. Esto es una propiedad del protocolo y del diseño del recurso, no
   una característica que el servidor active.
2. **Idempotencia de la operación de negocio.** Un cobro, un envío de correo o una
   transferencia son irreversibles y no son idempotentes por naturaleza. Aquí hace falta el
   mecanismo explícito: la clave y el registro de respuestas.

La analogía útil es la del resguardo de la tintorería. Si vuelves a pedir «mi pedido» con el
mismo número de resguardo, te dan el mismo pedido, no uno nuevo. El número de resguardo es la
clave de idempotencia; el mostrador es el servidor. Lo importante: **el cliente elige la
clave**, porque solo él sabe que dos intentos son el mismo encargo y no dos encargos iguales.

Hay tres diseños que la gente intenta antes de llegar a este, y los tres fallan:

- **Filtrar por el cuerpo de la petición.** «Si ya hay un pago de 250 EUR de este usuario hoy,
  no lo repito». Falla con dos compras legítimas iguales y no protege de nada si dos
  peticiones llegan a la vez.
- **Un `SELECT` antes del `INSERT`.** Es una carrera: dos entregas simultáneas ven la tabla
  vacía y las dos insertan. La garantía de verdad es la **restricción de unicidad** en la base
  de datos.
- **Guardar solo el identificador del pago creado, sin la respuesta.** El reintento recibe un
  `200` con un cuerpo distinto al original y el cliente cree que la operación cambió. Hay que
  guardar el **estado HTTP, las cabeceras relevantes y el cuerpo**.

:::nota
La clave de idempotencia no es un candado contra el abuso ni un mecanismo de autenticación.
Es un registro de «esto ya lo hice y esto contesté». Un atacante que adivine la clave de otro
usuario no debe poder leer su respuesta: la clave se guarda **con el ámbito del usuario y del
endpoint**, y se busca siempre acotada a ese ámbito.
:::

## Definición formal

Sea una operación con efecto `f` y una clave `k` enviada por el cliente. El servidor mantiene
un registro `R` que asocia cada `k` con la respuesta que produjo.

- **Petición con clave nueva** (`k ∉ R`): se ejecuta el efecto, se guarda
  `R[k] = (código, cuerpo)` y se devuelve la respuesta. El registro y el efecto se escriben en
  la **misma transacción**.
- **Petición con clave repetida** (`k ∈ R`): no se ejecuta `f`; se devuelve `R[k]` tal cual,
  con el mismo código de estado.
- **Misma clave con cuerpo distinto:** conflicto. El cliente está reutilizando una clave para
  otra operación, así que la petición se rechaza (422 o 409). Comparar el cuerpo se hace sobre
  un **hash** del contenido, no sobre el texto original.
- **Clave en curso** (llegó una segunda petición mientras la primera se está ejecutando): se
  responde 409 *conflict* y el cliente reintenta más tarde. Es mejor decir «no sé todavía» que
  arriesgarse a ejecutar dos veces.

Símbolos: `f` es el efecto de negocio (cobrar, enviar, crear); `k` es la clave de idempotencia,
una cadena larga y aleatoria (UUID v4 o similar) generada por el cliente; `R` es el registro de
respuestas, con clave `k`; «misma transacción» significa que el efecto y la escritura en `R` se
confirman juntos o no se confirman ninguno.

:::truco
Guarda también un estado `en_curso` en `R` cuando empieces a procesar: así distingues «no lo he
visto nunca» de «lo estoy haciendo ahora mismo» y puedes devolver 409 en vez de ejecutar dos
veces. Con solo dos estados (existe / no existe) esa ventana queda abierta.
:::

La cabecera estándar para esto es `Idempotency-Key`. Ojo con un detalle: **caducar las claves
es parte del diseño**. Un TTL de 24 horas es habitual y suficiente para reintentos por red; si
lo pones de 30 segundos, un reintento con retroceso exponencial que llegue en el minuto 2
creará un duplicado.

## Ejemplo

Un cliente crea un pedido de 10,00 EUR con la clave `k-1` y la red falla antes de leer la
respuesta. Reintenta con la misma clave.

```
peticion 1  POST /pedidos  Idempotency-Key: k-1  {"lineas": [3.50, 6.50]}
            -> 201 {"id": 1000, "total": 10.0}
            (la respuesta se pierde en la red)

peticion 2  POST /pedidos  Idempotency-Key: k-1  {"lineas": [3.50, 6.50]}
            -> 201 {"id": 1000, "total": 10.0}     <- misma respuesta, ningun pedido nuevo

peticion 3  POST /pedidos  Idempotency-Key: k-2  {"lineas": [1.00]}
            -> 201 {"id": 1001, "total": 1.0}      <- operacion nueva, pedido nuevo
```

Tras las tres peticiones hay **dos** pedidos, no tres, y el cliente que solo vio el error de
red recibe exactamente la respuesta que se perdió. Eso es la idempotencia: el reintento es
gratis.

:::figura
fichero: idempotencia-clave-y-ttl
pie: Izquierda, el servidor y su registro de respuestas. La petición con `k-1` no encuentra la clave, crea el pedido 1000 y guarda la respuesta; la repetición con la misma clave devuelve exactamente la respuesta guardada y no crea nada; `k-2` es una operación nueva y crea el pedido 1001. Tres peticiones, dos pedidos. Derecha, por qué el TTL es parte del diseño: el reintento con retroceso exponencial (1, 2, 4, 8, 16 minutos) sigue llegando dentro de una ventana de 24 horas, pero si caducas la clave a los 10 minutos los intentos que llegan después vuelven a ejecutar el cobro.
fuente: figuras/idempotencia-en-apis-1.py
:::

## Código

```python verificable
def crear_pedido(clave, lineas, cache):
    """Devuelve (respuesta, repetida). El cache hace de tabla con clave unica."""
    if clave in cache:                     # reintento: devolvemos la respuesta original
        return cache[clave], True
    # El identificador se deriva del numero de entradas del cache: en produccion lo asigna
    # la base de datos, no el codigo.
    respuesta = {"id": len(cache) + 1000, "total": sum(lineas)}
    cache[clave] = respuesta               # en produccion, en la misma transaccion
    return respuesta, False

cache = {}
# Cada llamada devuelve dos cosas: la respuesta y si era un reintento. En la tercera, el
# guion bajo descarta ese segundo valor porque no se va a usar.
primera, repetida = crear_pedido("k-1", [3.50, 6.50], cache)
segunda, repetida2 = crear_pedido("k-1", [3.50, 6.50], cache)
tercera, _ = crear_pedido("k-2", [1.00], cache)

print("primera llamada:", primera, "repetida:", repetida)      # -> repetida: False
print("mismo key      :", segunda, "repetida:", repetida2)     # -> el MISMO diccionario
print("otra key       :", tercera)
print("pedidos creados:", len(cache), "de 3 peticiones")       # -> 2 de 3
```

:::claves
- La respuesta repetida es **el mismo objeto**, no una copia: `segunda` y `primera` son el mismo
  diccionario, así que modificar uno cambia el otro. En producción lo que se devuelve es una
  respuesta reconstruida desde la base de datos, no una referencia compartida.
- El `id` se calcula con `len(cache) + 1000`: si se borrara una entrada del registro, el
  siguiente pedido reutilizaría un identificador ya entregado. Un contador o una secuencia de la
  base de datos no tienen ese problema.
- `sum(lineas)` suma la lista de importes y devuelve `0` con una lista vacía: un pedido sin
  líneas se crea con total 0 en vez de fallar. La validación del cuerpo es otra cosa.
- La clave se compara **tal cual llega**: `"k-1"` y `"K-1"` son claves distintas. Si el cliente
  genera UUID en minúsculas pero el servidor los normaliza, la deduplicación deja de funcionar.
- `cache[clave] = respuesta` ocurre **antes** de devolver, pero en este ejemplo no hay base de
  datos: si el proceso muriera justo después de esta línea, el pedido no existiría y el reintento
  lo crearía. Solo la transacción que abarca efecto y apunte cierra esa ventana.
- Cambiar el `return cache[clave], True` por `return None, True` rompe al cliente: el reintento
  recibiría un cuerpo vacío cuando el original traía el `id`, y es exactamente el fallo que
  describe «no guardar la respuesta completa».
:::

```sql verificable
-- La clave del cliente es la clave primaria: la base de datos, no el codigo, impide el duplicado.
CREATE TABLE pagos (clave VARCHAR PRIMARY KEY, importe DECIMAL(10,2));

INSERT INTO pagos VALUES ('pay-001', 250.00);
INSERT INTO pagos VALUES ('pay-002', 90.00);
-- El ON CONFLICT convierte el reintento en una operacion segura: no duplica ni falla.
INSERT INTO pagos VALUES ('pay-001', 250.00) ON CONFLICT DO NOTHING;

SELECT count(*) AS pagos, sum(importe) AS total FROM pagos;
```

```text
pagos  total
    2 340.00
```

```python ilustrativo
# La restriccion de unicidad es la unica proteccion real contra la carrera.
# Con SQLAlchemy, el patron completo seria asi.
from sqlalchemy.exc import IntegrityError

def cobrar(session, clave, importe):
    pago = Pago(clave=clave, importe=importe)
    session.add(pago)
    try:
        # El indice unico de la tabla decide quien gana: el segundo INSERT lanza IntegrityError
        # en vez de duplicar la fila.
        session.commit()
    except IntegrityError:
        # Hay que deshacer la transaccion fallida antes de seguir usando la sesion: si no,
        # cualquier consulta posterior falla con "current transaction is aborted".
        session.rollback()
        # El pago ya existia (lo creo la otra peticion): se devuelve el original, que es la
        # respuesta que hay que contestar al reintento.
        return session.get(Pago, clave)
    return pago
```

## Errores típicos

- **Usar `POST` y confiar en que el cliente no reintente.** Los clientes HTTP, las pasarelas y
  los balanceadores reintentan por su cuenta ante timeouts. Que tú no escribas un bucle de
  reintentos no significa que no haya repeticiones en la red.
- **Generar la clave en el servidor.** Si el servidor asigna un identificador nuevo a cada
  petición que recibe, dos entregas del mismo encargo obtienen identificadores distintos y la
  deduplicación es imposible. La clave la genera **quien conoce la intención**, que es el
  cliente.
- **Reutilizar una clave para operaciones distintas.** Muchos clientes generan la clave una vez
  por sesión y la usan en todas las peticiones: entonces el servidor devuelve la respuesta de
  la primera operación y el cliente cree que la segunda se hizo (y no se hizo nada). Detecta el
  caso con un hash del cuerpo y responde 422.
- **No guardar la respuesta completa.** Guardar solo «ok» y devolver un cuerpo genérico en el
  reintento rompe a los clientes que leen el `id` del recurso: reciben `null` y fallan al
  asignarlo. Guarda el código de estado, el cuerpo y las cabeceras que importen.
- **Caducar las claves antes de que termine la ventana de reintentos.** Si el cliente reintenta
  con retroceso exponencial durante 15 minutos y tu TTL es de 60 segundos, el reintento número
  7 crea un duplicado. El TTL debe cubrir la política de reintentos **del cliente**.
- **Aplicar la idempotencia solo al endpoint «importante».** El correo de confirmación, la
  llamada al webhook y la métrica de «pedidos creados» también se duplican. Si el contador de
  negocio se incrementa dos veces, el informe miente aunque la tabla de pedidos sea correcta.

:::trampa
Un `GET` que crea algo (por ejemplo `/enviar-recordatorio` o `/avanzar-estado`) rompe el
modelo entero: los navegadores, los *crawlers* y las herramientas de monitorización harán ese
`GET` cuando les apetezca, y cada uno ejecutará el efecto. Las lecturas se hacen con `GET` y
las mutaciones con `POST`, `PUT` o `PATCH`, sin excepciones.
:::

## Comprueba que lo sabes

:::quiz
p: Un cliente reintenta un `POST /pedidos` con la misma `Idempotency-Key`. ¿Qué debe hacer un servidor bien diseñado?
o: Crear otro pedido, porque el cliente lo ha pedido dos veces
o: Devolver la respuesta guardada de la primera petición, sin volver a crear nada
o: Responder 409 siempre, para que el cliente sepa que está repitiendo
a: 2
e: La clave significa «este es el mismo encargo», así que el segundo intento debe recibir la misma respuesta, con el mismo código de estado, y no crear un recurso nuevo. Responder 409 está reservado para la petición que llega **mientras** la primera sigue en curso; si ya terminó, se devuelve su respuesta.
:::

:::quiz
p: ¿Por qué comprobar con un `SELECT` antes de un `INSERT` no basta para evitar duplicados?
o: Porque el `SELECT` es más lento que el `INSERT` y merece la pena evitarlo
o: Porque dos peticiones simultáneas pueden leer las dos la tabla vacía e insertar las dos
o: Porque las bases de datos no permiten `SELECT` dentro de una transacción
a: 2
e: Es una condición de carrera clásica: entre la lectura y la escritura, la otra petición hace su propia lectura. La única garantía es una restricción de unicidad en la base de datos, que convierte el segundo `INSERT` en un error que tú interpretas como «ya estaba hecho».
:::

:::quiz
p: `PUT /usuarios/42 {"ciudad": "Sevilla"}` y `POST /usuarios` con ese mismo cuerpo. ¿Cuál es idempotente y por qué?
o: Las dos, porque las dos escriben el mismo dato
o: El `PUT`, porque aplicarlo dos veces deja el recurso 42 en el mismo estado; el `POST` crea un usuario nuevo cada vez
o: El `POST`, porque solo crea cuando el usuario no existe
a: 2
e: `PUT` es idempotente por definición: define el estado completo del recurso y repetirlo no cambia el resultado. `POST` se usa para crear dentro de una colección y cada envío produce un recurso nuevo, así que repetirlo duplica. La primera opción confunde «escribir lo mismo» con «no duplicar recursos».
:::
