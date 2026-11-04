---
id: apis-rest
titulo: APIs REST
fase: 11
nivel: intermedio
rutas: [alg, de]
prerequisitos: [apis-y-peticiones-http]
tags: [http, backend, diseno, interfaces]
resumen: Recursos, verbos y códigos de estado bien elegidos: la API que cualquiera puede usar sin leer tu documentación entera.
fuentes: ["Fielding (2000), 'Architectural Styles and the Design of Network-based Software Architectures'", "Richardson y Ruby (2007), 'RESTful Web Services'"]
---

## En una frase

Una API REST organiza la información en recursos con URL propia y deja que el protocolo HTTP
ponga el resto: el verbo dice qué operación es, el código de estado dice qué ha pasado y la
respuesta solo contiene datos, no sobres con instrucciones.

## La idea

Piensa en una biblioteca. No le pides al bibliotecario «hazme el favor de darme el libro de
Cervantes y apúntalo en tu cuaderno»: le dices *qué* quieres y él decide *cómo* conseguirlo.
REST es exactamente ese trato. Tú nombras la cosa (`/libros/123`), eliges el verbo (quieres
leerlo, quieres añadirlo, quieres retirarlo) y el servidor responde con un resultado.

La consecuencia práctica es que **las URL nombran sustantivos, no acciones**. Si tu API tiene
`/crearPedido` o `/cancelarPedido`, no es REST: es un conjunto de funciones con cableado HTTP
encima. Lo correcto es tener `/pedidos` como colección y `/pedidos/42` como elemento, y dejar
que el verbo haga el trabajo.

La segunda idea es que **el código de estado es parte del contrato**. Un cliente que recibe un
404 sabe que el recurso no está; un cliente que recibe un 403 sabe que existe pero no puede
tocarlo; un cliente que recibe un 200 con `{"error": "no encontrado"}` no sabe nada sin leer
el cuerpo, y eso obliga a programar un `if` distinto por cada endpoint. Cuando un cliente
genérico (un navegador, un SDK, un monitor, un *proxy*) no puede interpretar tus respuestas,
has tirado la principal ventaja del estilo.

La tercera es que **la red no es fiable**. Una petición puede llegar, procesarse y perderse la
respuesta. Si el cliente reintenta, ¿se crea el pedido dos veces? Por eso los verbos de
consulta y de reemplazo son idempotentes —repetirlos no cambia el resultado— y por eso las
creaciones necesitan una [[idempotencia-en-apis|clave de idempotencia]] si quieres poder
reintentarlas sin miedo.

## Definición formal

Un servicio REST se caracteriza por:

- **Recursos identificados por URL.** Cada recurso tiene un identificador estable:
  `/clientes/7`, `/clientes/7/pedidos?estado=pendiente`. Las barras expresan jerarquía de
  contención, no rutas de sistema de ficheros.
- **Verbos con significado fijo.** GET lee, POST crea, PUT reemplaza el recurso entero, PATCH
  modifica una parte, DELETE elimina. El significado no lo eliges tú.
- **Representaciones.** El servidor no devuelve el objeto, devuelve una representación suya
  (JSON, normalmente). El cliente negocia el formato con la cabecera `Accept` y el servidor
  contesta con `Content-Type`.
- **Sin estado en el servidor.** Cada petición lleva toda la información necesaria para
  atenderla: la sesión va en una cabecera o en un token, no en la memoria del proceso. Esto es
  lo que permite repartir peticiones entre varios servidores sin sesiones pegajosas.
- **Interfaz uniforme.** Los mismos verbos, los mismos códigos y las mismas convenciones en
  todos los recursos.

Tabla de verbos y su efecto:

| Verbo | Efecto | Idempotente | Cuerpo de la respuesta |
| --- | --- | --- | --- |
| GET | Lee una representación | Sí | El recurso |
| POST | Crea un recurso nuevo | No | El recurso creado, con su URL |
| PUT | Reemplaza el recurso entero | Sí | El recurso resultante |
| PATCH | Modifica parte del recurso | No por defecto | El recurso resultante |
| DELETE | Elimina el recurso | Sí | Vacío |

Códigos que de verdad vas a usar, y qué significa cada uno:

- **200** correcto con cuerpo; **201** creado, con la cabecera `Location` hacia el recurso
  nuevo; **204** correcto sin cuerpo, típico de un DELETE.
- **400** la petición está mal formada (JSON roto); **422** el JSON es válido pero los datos no
  cumplen las reglas; **401** no sé quién eres; **403** sé quién eres y no puedes; **404** no
  existe; **405** ese verbo no vale para esa URL; **409** choca con el estado actual (un
  duplicado, una versión desactualizada); **429** vas demasiado rápido.
- **500** fallo tuyo; **502** el servicio de detrás contestó mal; **503** ahora mismo no puedo;
  **504** el servicio de detrás no contesta.

**Paginación.** Una colección no se devuelve entera nunca. Hay dos familias:

- Por desplazamiento: `?limite=100&offset=200`. Sencilla y saltable a cualquier página, pero
  cada página cuesta más que la anterior y las inserciones desplazan elementos entre páginas.
- Por cursor: `?limite=100&cursor=eyJpZCI6MjAwfQ`. Estable y rápida, pero solo avanzas hacia
  delante.

**Versionado.** El más común es la versión en la ruta (`/v1/pedidos`), porque es visible y se
enruta sin trucos. La alternativa es negociar por cabecera (`Accept: application/vnd.api+json;version=2`).
Cualquiera de las dos vale; lo imperdonable es cambiar el significado de un campo sin cambiar
la versión.

## Ejemplo

Tienes 250 pedidos y devuelves 100 por página como máximo:

- Petición 1: `GET /v1/pedidos?limite=100&offset=0` devuelve los identificadores del 1 al 100.
- Petición 2: `GET /v1/pedidos?limite=100&offset=100` devuelve del 101 al 200.
- Petición 3: `GET /v1/pedidos?limite=100&offset=200` devuelve del 201 al 250, es decir 50.

Tres peticiones y ya está. Si el cliente pide `?limite=1000`, el servidor no debe devolver
1000: debe responder 422 con un mensaje que diga cuál es el máximo, porque un límite abierto
es una invitación a tumbar tu base de datos.

Sigamos con la idempotencia. `PATCH /pedidos/42` con `{"estado": "enviado"}` sobre un pedido
que ya está en `enviado` no debería incrementar la versión del recurso ni disparar un correo:
el resultado tiene que ser el mismo que la primera vez. `DELETE /pedidos/42` repetido debe
responder 204 las dos veces, aunque la segunda no borre nada.

## Código

```python verificable
ids = list(range(1, 251))          # 250 pedidos
LIMITE_MAX = 100
offset, total_peticiones = 0, 0

while offset < len(ids):
    pedir = min(100, len(ids) - offset)      # la ultima pagina pide 50, no 100
    if pedir > LIMITE_MAX:
        raise ValueError("422: limite fuera de rango")    # el servidor no sirve 1000: corta
    pagina = ids[offset:offset + pedir]      # rebanada semiabierta: entra el offset, no el final
    total_peticiones += 1
    print(f"GET /v1/pedidos?limite={pedir}&offset={offset} -> {len(pagina):>3} items, "
          # :>3 es un ancho minimo de 3 alineado a la derecha: la columna cuadra al leerla
          f"desde el id {pagina[0]} hasta el {pagina[-1]}")
    offset += pedir

print("peticiones necesarias:", total_peticiones)   # -> 3
```

:::claves
- `min(100, len(ids) - offset)` es lo que hace que la última petición pida 50 y no 100. Si el servidor devolviera siempre 100, la última página traería 50 elementos y 50 huecos. `total_peticiones` cuenta **peticiones**, no filas: son 3, no 250.
- La rebanada `ids[offset:offset + pedir]` es semiabierta: con `offset=0` y `pedir=100` devuelve los elementos 0 a 99. Por eso el paso del bucle (`offset += pedir`) tiene que avanzar **exactamente** el mismo ancho que la rebanada: si el ancho y el paso se separan, la página siguiente repite filas o se salta un tramo entero.
- El bucle avanza con `offset += pedir` y termina cuando el offset alcanza la longitud: `ceil(250 / 100) = 3` vueltas. Con `range` y un número fijo de páginas no haría falta la condición, pero entonces una colección que crece entre peticiones se cortaría.
- `raise ValueError("422...")` solo simula la respuesta: en un servicio real el 422 se devuelve como estado HTTP y el cliente lo lee en la primera línea, no dentro del cuerpo.
- En el segundo bloque, `put` y `delete` **modifican el diccionario en el sitio** y devuelven una tupla o un código. Los dos `print` con dos llamadas seguidas enseñan las dos respuestas idénticas, y eso es la idempotencia: la segunda llamada no cambia nada porque la primera ya dejó el estado ahí.
- `put` no incrementa la versión si el estado es el mismo: quitar ese `if` haría que reintentar un PUT subiera la versión sin que el recurso hubiera cambiado, y el cliente creería que alguien lo ha modificado.
:::

:::figura
fichero: apis-rest-coste-paginacion
pie: Izquierda, las filas que hay que leer para servir una página según se pagine. Por desplazamiento el coste crece con la profundidad —la página 20 exige leer 2.000 filas para devolver 100— mientras que el cursor se queda plano en 100 por página. Derecha, el otro problema del desplazamiento: si entre la página 1 y la 2 entra un pedido nuevo por delante, el id 4, que ya viajó en la primera, vuelve a salir en la segunda y el cliente lo ve duplicado; con un borrado en medio, en lugar de repetir se saltaría uno. El cursor evita las dos cosas porque recuerda por dónde ibas en vez de contar posiciones.
fuente: figuras/apis-rest-1.py
:::

```python verificable
pedido = {"estado": "pendiente", "version": 1}

def get(recurso):                       # GET no cambia nada
    return recurso["estado"], recurso["version"]      # devuelve una tupla (estado, version)

def put(recurso, estado):               # PUT es idempotente: mismo cuerpo, mismo resultado
    if recurso["estado"] != estado:     # solo sube la version si el estado cambia de verdad
        recurso["estado"] = estado
        recurso["version"] += 1
    return recurso["estado"], recurso["version"]

def delete(recurso):                    # DELETE es idempotente: la segunda vez tampoco pasa nada
    if recurso["estado"] != "cancelado":
        recurso["estado"] = "cancelado"
        recurso["version"] += 1
    return 204                          # un codigo, no un cuerpo: DELETE no devuelve nada

print("GET   x2 ->", get(pedido), get(pedido))          # -> ('pendiente', 1) ('pendiente', 1)
print("PUT   x2 ->", put(pedido, "enviado"), put(pedido, "enviado"))   # -> ('enviado', 2) ('enviado', 2)
print("DELETE x2 ->", delete(pedido), delete(pedido))   # -> 204 204
print("version final:", pedido["version"])              # -> 3 (la subio el PUT y la subio el DELETE)
```

```text
GET /v1/pedidos?limite=2&offset=0 HTTP/1.1
Host: api.tienda.example
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{"datos": [{"id": 1, "estado": "pendiente"}, {"id": 2, "estado": "enviado"}],
 "siguiente": "/v1/pedidos?limite=2&offset=2"}

POST /v1/pedidos HTTP/1.1
Idempotency-Key: 8f14e45f-ceea-467a-9a3e-1c0f2a9b7d21
Content-Type: application/json

{"cliente": 7}

HTTP/1.1 201 Created
Location: /v1/pedidos/251
```

## Errores típicos

- **Devolver 200 para todo y poner el error en el cuerpo.** `200 {"ok": false, "error": "no existe"}`
  rompe a cualquier cliente genérico: los reintentos, la caché y la monitorización dejan de
  funcionar. Usa el código que toca y deja el cuerpo para el detalle.
- **Poner verbos en la URL.** `/borrarPedido/42` o `/getUsuarios` convierten la API en un
  catálogo de funciones. Es `/pedidos/42` con DELETE, o `/usuarios` con GET.
- **Confundir 401 y 403.** El 401 significa «falta autenticación o es inválida» y debe traer
  `WWW-Authenticate`; el 403 significa «estás autenticado y no te corresponde». Devolver 403 a
  quien no ha iniciado sesión hace que el cliente no sepa que tiene que pedir credenciales.
- **Devolver un array pelado como colección.** `[{"id": 1}, {"id": 2}]` no deja sitio para el
  total, el cursor ni los avisos; añadirlos después rompe a todos los clientes. Envuelve
  siempre: `{"datos": [...], "siguiente": ...}`.
- **Exponer las claves de la base de datos.** `/pedidos/1042` donde 1042 es el `AUTO_INCREMENT`
  revela cuántos pedidos tienes y permite enumerar los de otros. Mejor un identificador público
  opaco, o al menos un control de acceso en cada lectura.
- **PUT para cambios parciales.** Si `PUT /clientes/7` espera el objeto completo y tú mandas
  solo el teléfono, o borras los demás campos o tienes que inventarte una lógica de fusión. Un
  cambio parcial es `PATCH`; `PUT` es un reemplazo y debe ser idempotente.
- **Paginación sin límite máximo ni orden estable.** Sin `ORDER BY` fijo, dos peticiones con el
  mismo `offset` pueden devolver filas distintas y el cliente se salta registros o los repite.

## Comprueba que lo sabes

:::quiz
p: Un cliente reintenta un POST porque se le perdió la respuesta. ¿Qué mecanismo evita que se creen dos pedidos?
o: Cambiar el POST por un PUT a la colección
o: Enviar una clave de idempotencia en la petición y que el servidor recuerde su resultado
o: Subir el código de estado a 201 para que el cliente sepa que se ha creado
a: 2
e: El POST no es idempotente por naturaleza, así que reintentarlo duplica. La clave de idempotencia deja que el servidor reconozca el reintento y devuelva el mismo resultado sin volver a crear. Cambiar a PUT no arregla nada si el servidor genera el identificador, y el 201 solo informa de lo que ya ha pasado.
:::

:::quiz
p: Un usuario ha iniciado sesión pero intenta borrar un pedido de otra tienda. ¿Qué código corresponde?
o: 401, porque no se le permite la operación
o: 403, porque está autenticado pero no autorizado
o: 404, porque su pedido no existe en esa tienda
a: 2
e: El 401 es para quien no ha demostrado quién es. Aquí sí lo ha demostrado, simplemente no le corresponde, y eso es 403. El 404 es una decisión de diseño legítima para no revelar que el recurso existe, pero como respuesta genérica a un problema de permisos es incorrecta.
:::

:::quiz
p: ¿Por qué se recomienda limitar y acotar la paginación por desplazamiento?
o: Porque el offset obliga a recorrer y descartar filas, así que las páginas profundas son más caras, y sin límite máximo una petición puede tumbar la base de datos
o: Porque el offset no funciona con más de mil registros
o: Porque los cursores son obligatorios en HTTP
a: 1
e: Con `offset=100000` el motor tiene que leer y tirar cien mil filas antes de devolver las siguientes, y ese coste crece con la profundidad. El cursor evita ese recorrido porque recuerda por dónde ibas. El offset funciona con cualquier tamaño; simplemente se vuelve lento.
:::

:::practica
enunciado: Diseña los endpoints para gestionar comentarios de un artículo: listar con paginación, leer uno, crear, editar el texto y borrar. Indica verbo, URL y código de éxito de cada uno.
pista: Los comentarios viven dentro de un artículo, así que la URL refleja esa contención.
solucion: GET /v1/articulos/9/comentarios?límite=50&cursor=abc (200, colección envuelta con el siguiente cursor). GET /v1/comentarios/1234 (200). POST /v1/articulos/9/comentarios con el cuerpo del comentario (201 y cabecera Location hacia /v1/comentarios/1234). PATCH /v1/comentarios/1234 con el texto nuevo (200, y si el cliente manda una versión antigua, 409). DELETE /v1/comentarios/1234 (204, e idempotente: repetirlo sigue dando 204). Los identificadores de comentario son públicos, no la clave primaria de la tabla.
:::

:::nota
REST es un estilo arquitectónico descrito por Roy Fielding en su tesis doctoral, no un estándar
con certificado. Casi ninguna API real cumple los seis principios a rajatabla; lo que importa
es que las decisiones sean coherentes y que un cliente pueda predecir el resto de la API
después de aprender dos endpoints.
:::
