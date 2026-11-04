---
id: apis-y-peticiones-http
titulo: APIs y peticiones HTTP
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [ficheros-y-encoding, tipos-y-estructuras-python]
tags: [http, api, rest, paginacion, reintentos]
resumen: Una API es una promesa por escrito con método, ruta, código de estado y formato; aquí se aprende a leerla, paginarla y reintentarla sin abusar del servidor.
fuentes: ["RFC 9110, 'HTTP Semantics'", "RFC 8288, 'Web Linking'", "Documentación de MDN sobre códigos de estado HTTP"]
---

## En una frase

Una API HTTP es un contrato con cuatro piezas —método, ruta, cabeceras y código de estado— que
te dice a quién pides qué, si te lo dan, y por qué no te lo dan cuando te lo niegan.

## La idea

Cuando pides datos a un servicio web no estás llamando a una función: estás enviando un texto
por la red y esperando otro texto de vuelta. Ese intercambio tiene una gramática, y quien no la
lee acaba con un `JSONDecodeError` que en realidad era un «te has pasado de peticiones».

Piénsalo como pedir en una ventanilla. La **petición** lleva un método (qué quieres hacer), una
ruta (de qué), unas cabeceras (quién eres y en qué formato quieres la respuesta) y a veces un
cuerpo (los datos que mandas). La **respuesta** lleva un código de estado de tres cifras (qué ha
pasado), sus propias cabeceras y un cuerpo que suele ser JSON.

El código de estado es lo primero que hay que mirar, antes de tocar el cuerpo:

- **2xx: ha ido bien.** `200 OK` es lo normal; `201 Created` te dice que se creó algo;
  `202 Accepted` que se aceptó pero aún no está hecho; `204 No Content` que fue bien y no hay
  cuerpo.
- **3xx: mira la cabecera `Location`.** Una redirección no es un éxito: es un «está en otro
  sitio» que tu cliente debe seguir.
- **4xx: el error es tuyo, y reintentar tal cual no arregla nada.** `400` petición mal formada,
  `401` no te has identificado, `403` te has identificado y no tienes permiso, `404` no existe,
  `422` la petición está bien formada pero los datos no valen, `429` te has pasado de la cuota.
- **5xx: el error es suyo.** `500` fallo interno, `502` mal gateway, `503` no disponible,
  `504` el servidor de detrás no contestó a tiempo. Estos **sí** son los que se reintentan.

El problema práctico aparece con los conjuntos grandes: una API no te va a devolver un millón
de filas de golpe. Pagina. Hay tres estilos y conviene reconocerlos:

- **Por desplazamiento** (`?page=3&per_page=100` o `?offset=200&limit=100`): sencillo, pero si
  añades o borras filas mientras páginas, te saltas registros o los repites.
- **Por cursor** (`?cursor=abc123`): la respuesta trae un testigo opaco para la página
  siguiente. Estable aunque los datos cambien; es el que usan las APIs serias.
- **Por cabecera `Link`** (RFC 8288): la respuesta incluye la URL exacta de la página siguiente.
  Es el más limpio de todos porque no tienes que construir URLs.

Y luego está el límite de tasa: casi todas las APIs te dicen cuántas peticiones te quedan y
cuándo se reinicia el contador, normalmente en las cabeceras `X-RateLimit-Limit`,
`X-RateLimit-Remaining` y `X-RateLimit-Reset`, a veces en `Retry-After` cuando ya te han
bloqueado. Cuando llega un `429` o un `503`, la respuesta correcta no es insistir: es esperar un
poco y volver, **con espera exponencial** (1 s, 2 s, 4 s, 8 s…) y algo de azar añadido para que
mil clientes no reintenten en el mismo instante.

Las claves de API merecen un párrafo aparte porque es donde se filtran datos de verdad: van en
una cabecera (`Authorization: Bearer …`) o en una variable de entorno, **nunca** en el código,
nunca en un repositorio de Git y nunca en la URL, porque las URLs quedan registradas en los
logs de todos los intermediarios por los que pasan.

## Definición formal

Una petición HTTP/1.1 tiene esta forma:

```
METODO /ruta?consulta=valor HTTP/1.1
Host: api.ejemplo.com
Authorization: Bearer <clave>
Accept: application/json

cuerpo opcional
```

- **METODO** — `GET` lee (no debe cambiar nada), `POST` crea, `PUT` reemplaza, `PATCH` modifica
  en parte, `DELETE` borra. La propiedad que importa: `GET`, `PUT` y `DELETE` son
  **idempotentes** (repetirlos deja el mismo estado), `POST` no lo es.
- **Host** — el dominio al que va la petición. Obligatorio en HTTP/1.1.
- **`Authorization`** — la credencial. `Bearer` significa «un testigo opaco», que casi siempre
  es un token o una clave.
- **`Accept`** — el tipo de contenido que aceptas como respuesta (`application/json`,
  `text/csv`).

Códigos que vas a ver y qué hacer con cada uno:

| Código | Nombre | ¿Reintentar? | Qué suele pasar |
| --- | --- | --- | --- |
| 200 | OK | No hace falta | Respuesta normal |
| 301 / 302 | Movido permanentemente / temporalmente | Sí, siguiendo `Location` | Cambió la URL |
| 400 | Bad Request | No | Falta un parámetro o está mal formado |
| 401 | Unauthorized | No | Clave ausente, caducada o mal escrita |
| 403 | Forbidden | No | Clave válida sin permiso para ese recurso |
| 404 | Not Found | No | Ruta o identificador inexistente |
| 422 | Unprocessable Content | No | JSON válido pero valores inválidos |
| 429 | Too Many Requests | Sí, tras esperar `Retry-After` | Has superado la cuota |
| 500 / 502 / 503 / 504 | Errores de servidor | Sí, con espera exponencial | Fallo temporal del servicio |

**Espera exponencial con jitter**: el intento número `k` (empezando en 0) espera

:::formula
t_k = min(t_max, t_base · 2^k) · (1 + azar)
:::

donde `t_base` es la espera inicial (por ejemplo 0,5 s), `t_max` el techo (por ejemplo 30 s) y
`azar` un número aleatorio entre 0 y 1. Sin jitter, todos los clientes que fallaron a la vez
reintentan a la vez y tumban otra vez el servidor.

## Ejemplo

Petición paginada a `https://api.ejemplo.com/v1/pedidos?page=2&per_page=100`:

```
GET /v1/pedidos?page=2&per_page=100 HTTP/1.1
Host: api.ejemplo.com
Authorization: Bearer eyJhbGciOi...
Accept: application/json
```

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
X-RateLimit-Reset: 1735689600
Link: <https://api.ejemplo.com/v1/pedidos?page=3&per_page=100>; rel="next",
      <https://api.ejemplo.com/v1/pedidos?page=10&per_page=100>; rel="last"

{"total": 950, "page": 2, "pedidos": [ ... ]}
```

Que te está diciendo y en qué orden mirarlo:

1. `200`: bien. `total: 950` con `per_page=100` son 10 páginas, y `rel="last"` te lo confirma.
2. `X-RateLimit-Remaining: 58` de 60: vas sobrado, pero si tuvieras 0 tienes que parar hasta
   `X-RateLimit-Reset` (que es un instante Unix, en segundos).
3. `Link` con `rel="next"` es la URL exacta de la página siguiente: no la construyas tú,
   porque puede llevar un cursor que no sabes generar.

Si en vez de eso recibes:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

el plan es dormir 30 segundos y volver, no reducir el `per_page` y martillear. Y si recibes
`401` con `{"error": "token expired"}`, ninguna espera lo arregla: hay que renovar el token.

## Código

```python verificable
# Parsear cabeceras HTTP sin red: el bloque de cabeceras, tal cual llegaria
from email.parser import Parser

cabeceras = (
    "Content-Type: application/json\r\n"
    "X-RateLimit-Limit: 60\r\n"
    "X-RateLimit-Remaining: 58\r\n"
    'Link: <https://api.ejemplo.com/v1/pedidos?page=3>; rel="next", '
    '<https://api.ejemplo.com/v1/pedidos?page=10>; rel="last"\r\n'
)
m = Parser().parsestr(cabeceras)
print("restantes       :", m["X-RateLimit-Remaining"], "de", m["X-RateLimit-Limit"])  # -> 58 de 60

# La cabecera Link es una lista de URL con su relacion entre <> y rel=""
partes = [p.strip() for p in m["Link"].split(",")]
rel = {p.split('rel="')[1].rstrip('"'): p.split(">")[0].lstrip("<") for p in partes}
print("pagina siguiente:", rel["next"])
print("ultima pagina   :", rel["last"])
```

```python verificable
# Calculo de la espera entre reintentos: exponencial y con jitter
import random

random.seed(0)                      # semilla fija: el ejemplo es reproducible

t_base, t_max = 0.5, 30.0
for intento in range(5):
    espera = min(t_max, t_base * 2 ** intento)
    con_jitter = espera * (1 + random.random())
    print(f"intento {intento}: espera base {espera:>4.1f}s  con jitter {con_jitter:>5.2f}s")
```

```python verificable
# Que codigos merecen otro intento: la decision, escrita una sola vez
reintentables = {429, 500, 502, 503, 504}

def politica(codigo, intento, retry_after=None):
    if codigo in reintentables:
        return retry_after if retry_after is not None else min(30.0, 0.5 * 2 ** intento)
    return None                      # 4xx que no sea 429: reintentar no arregla nada

for codigo in (200, 401, 404, 429, 503):
    print(f"{codigo}: esperar {politica(codigo, 0)}")
```

```python ilustrativo
# El bucle real: red, cabeceras, paginacion y reintentos. Necesita red y una clave.
import os
import time
import requests

SESION = requests.Session()
SESION.headers["Authorization"] = f"Bearer {os.environ['API_TOKEN']}"  # nunca en el codigo

def pedir(url, intentos=5):
    for intento in range(intentos):
        r = SESION.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504) and intento < intentos - 1:
            espera = float(r.headers.get("Retry-After", 0.5 * 2 ** intento))
            time.sleep(espera)
            continue
        r.raise_for_status()          # 4xx: falla ya, con el cuerpo del error en el mensaje
    raise RuntimeError(f"agotados los reintentos en {url}")

def todas_las_paginas(url):
    while url:
        datos = pedir(url)
        yield from datos["resultados"]
        url = datos.get("siguiente")  # o parsear la cabecera Link, segun la API
```

## Errores típicos

- **Mirar el cuerpo antes que el código de estado.** Un `500` con cuerpo HTML hace que
  `r.json()` lance `JSONDecodeError` y el mensaje real («el servicio está caído») se pierde.
  Comprueba `r.status_code` primero; casi todas las librerías tienen `raise_for_status()`.
- **Reintentar un 4xx.** Un `401`, `403` o `404` no mejora por insistir: si acaso empeora,
  porque algunos servicios bloquean a quien acumula errores. Solo se reintenta `429` y los
  `5xx`.
- **Reintentar sin espera creciente ni jitter.** Cinco reintentos inmediatos son cinco
  peticiones más en el peor momento. Con espera exponencial y un poco de azar, el servicio se
  recupera y tú también.
- **Un `POST` reintentado a ciegas.** `POST` no es idempotente: si la respuesta se perdió por
  la red, el reintento puede crear el pedido dos veces. O el servidor acepta una clave de
  idempotencia, o compruebas el estado antes de repetir.
- **Construir la URL de la página siguiente a mano.** Si la API usa cursores, `?page=3` no
  significa nada y te devuelve la primera página en bucle infinito. Sigue el `rel="next"` o el
  cursor que te den.
- **Guardar la clave en el repositorio.** Una clave en el código termina en Git, en una captura
  de pantalla o en un log de URLs. Va en variable de entorno o en un gestor de secretos, y si
  se filtra, se rota: no se «arregla» borrando el commit.
- **Ignorar la zona horaria de las fechas.** `1735689600` es un instante Unix (UTC), no una
  fecha local; y `"2025-01-01T00:00:00"` sin zona es ambiguo. Guarda siempre UTC y conviértelo
  al mostrarlo.

:::practica
enunciado: Una API responde {"total": 950} y acepta per_page=100, con X-RateLimit-Limit: 60 peticiones por minuto. Calcula cuántas páginas hacen falta y cuánto tarda la descarga respetando el límite. Después, con t_base = 0,5 s y t_max = 30 s, escribe las cuatro primeras esperas de la política exponencial.
pista: El número de páginas es ceil(total / per_page), y la espera del intento k vale min(t_max, t_base · 2^k).
solucion: 950/100 = 9,5, así que hacen falta 10 páginas. Con 60 peticiones por minuto, 10 peticiones caben de sobra en ese minuto y no hay que esperar entre páginas. Las esperas de los intentos k = 0, 1, 2 y 3 son 0,5 s, 1 s, 2 s y 4 s. Si en vez de eso llega un 429 con Retry-After: 30, ese valor manda: se esperan los 30 segundos indicados antes de reintentar.
:::

## Comprueba que lo sabes

:::quiz
p: Recibes un `429` con `Retry-After: 30` y un `X-RateLimit-Remaining: 0`. ¿Qué haces?
o: Reintentar inmediatamente con un `per_page` más pequeño
o: Esperar los 30 segundos indicados y volver a pedir; si se repite, esperar cada vez más
o: Cambiar el método de `GET` a `POST` y repetir la petición
a: 2
e: El 429 significa que has superado la cuota, así que insistir solo alarga el bloqueo; Retry-After es la espera mínima que te pide el servidor. Los 4xx que no sean 429 no se reintentan, y cambiar de método no esquiva el límite.
:::

:::quiz
p: ¿Por qué no conviene construir a mano la URL de la página siguiente cuando la API página con cursor?
o: Porque el cursor es un testigo opaco que solo el servidor sabe generar, y `?page=3` te devolvería otra vez la primera página
o: Porque las URLs con cursor caducan en un segundo
o: Porque el cursor solo funciona con el método POST
a: 1
e: El cursor no tiene estructura documentada: es una cadena que el servidor emite y entiende. Si la sustituyes por un número de página, o el servidor ignora el parámetro o devuelve un resultado distinto del que crees, y el bucle no termina nunca.
:::

:::quiz
p: ¿Qué diferencia hay entre `401` y `403`?
o: El 401 significa que no te has identificado y el 403 que te has identificado pero no tienes permiso
o: El 401 es un error del servidor y el 403 un error del cliente
o: El 401 se reintenta y el 403 no
a: 1
e: 401 es «falta autenticación o la credencial no vale» y 403 es «la credencial es válida pero este recurso no es para ti». Ninguno de los dos se arregla reintentando: en el primero hay que autenticarse o renovar el token, en el segundo pedir permisos.
:::

:::truco
Cuando integres una API nueva, guarda una respuesta de ejemplo en un fichero y escribe los
tests contra ese fichero, no contra el servicio. Así tus pruebas no dependen de la red, ni de
la cuota, ni de que el otro extremo esté de buen humor.
:::
