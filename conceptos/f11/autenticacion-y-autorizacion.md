---
id: autenticacion-y-autorizacion
titulo: Autenticación y autorización
fase: 11
nivel: avanzado
rutas: [alg]
prerequisitos: [apis-rest]
tags: [seguridad, sesiones, tokens, permisos]
resumen: Quien eres y qué puedes hacer: sesiones, tokens, JWT, OAuth y los errores de seguridad que se repiten en cada proyecto.
fuentes: ["OWASP, 'Application Security Verification Standard'", "Jones, Bradley y Sakimura (2015), 'JSON Web Token (JWT)', RFC 7519"]
---

## En una frase

Autenticar es demostrar quién eres; autorizar es decidir qué puedes hacer con esa identidad, y
son dos comprobaciones distintas que se confunden constantemente.

## La idea

Imagina un edificio. En la puerta enseñas el carné y el vigilante comprueba que es auténtico:
eso es **autenticación**. Una vez dentro, tu tarjeta abre la sala de servidores pero no la caja
fuerte: eso es **autorización**. Si las confundes y solo compruebas el carné en la puerta,
cualquier empleado entra a la caja fuerte; si solo miras la tarjeta sin comprobar el carné,
cualquiera con una tarjeta falsa entra.

Con servicios web hay dos formas de mantener esa identidad a lo largo de las peticiones:

- **Sesión en el servidor.** Al iniciar sesión, el servidor crea un registro con el
  identificador del usuario y devuelve una cookie con un identificador de sesión opaco. En cada
  petición, el servidor busca esa sesión. Revocar el acceso es borrar la fila: inmediato. El
  precio es que todas las peticiones necesitan consultar el almacén de sesiones.
- **Token firmado (JWT).** El servidor entrega un token que contiene los datos del usuario y
  una firma. En cada petición, el servidor solo comprueba la firma, sin consultar nada. Es
  cómodo y escala, y a cambio **no se puede revocar**: el token vale hasta que caduca. Por eso
  los tokens son cortos (minutos) y van acompañados de un *refresh token* de vida más larga,
  que sí se guarda y se puede invalidar.

Hay un detalle del token que se malinterpreta siempre: **el contenido va firmado, no cifrado**.
Cualquiera que tenga el token puede leer lo que lleva dentro con cuatro líneas de código; lo que
no puede es cambiar nada sin invalidar la firma. Así que nada de meter datos sensibles ahí.

Encima de eso está **OAuth 2.0**, que no es un sistema de autenticación sino de autorización
delegada: permite que una aplicación acceda a tus datos en otro servicio sin darle tu
contraseña. Quien sí es un protocolo de autenticación es OpenID Connect, que va sobre OAuth y
añade un token de identidad verificable.

## Definición formal

**JWT.** Un token es tres bloques separados por puntos: `cabecera.carga.firma`. Los dos
primeros van en base64url y el tercero es la firma calculada sobre `cabecera.carga`:

:::formula
firma = HMAC-SHA256(clave_secreta, cabecera + "." + carga)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `firma` | El tercer bloque del token: el sello que demuestra que cabecera y carga no se han tocado | bytes en base64url (32 con SHA-256) | No crece: cambia entera si cambia un solo carácter del mensaje. Es lo que compara el servidor |
| `clave_secreta` | La clave con la que se firma y se verifica; vive en un gestor de secretos, nunca en el repositorio | bytes | Nada visible en el token; si se filtra, cualquiera puede firmar tokens válidos, y rotarla invalida todos los emitidos |
| `cabecera` | JSON con `alg` (el algoritmo) y `typ` (el tipo) | bytes en base64url | Nunca debe leerse del token: aceptar el `alg` que manda el cliente es el fallo que permite falsificar tokens. El algoritmo se fija en el servidor |
| `carga` | Los *claims*: `sub`, `rol`, `exp`, `iat`, `aud`, `iss` | bytes en base64url | Alarga cada petición (una cookie son unos bytes; un JWT con muchos claims, cientos) y **cualquiera la lee**: va firmada, no cifrada |
| `HMAC-SHA256` | La función que mezcla la clave con el mensaje | — | Cambiar de algoritmo cambia la longitud de la firma; el servidor debe pasar la lista de algoritmos permitidos al verificar |
:::

- `cabecera` — JSON con el algoritmo (`alg`) y el tipo (`typ`). `alg` debe fijarse en el
  servidor y nunca tomarse del propio token: aceptar `alg: none` o dejar que el cliente elija
  es el fallo clásico que permite falsificar tokens.
- `carga` — los *claims*. Los habituales: `sub` (a quién identifica), `exp` (caducidad, en
  segundos desde epoch), `iat` (emisión), `aud` (para quién es), `iss` (quién lo emitió).
- `firma` — el sello. Sin la clave secreta no se puede recalcular, así que modificar la carga
  invalida el token. La comparación debe hacerse en tiempo constante.

**Contraseñas.** Nunca se guardan, se guardan derivaciones lentas con sal:

- `sal` — valor aleatorio distinto por usuario, guardado junto al hash. Impide que dos usuarios
  con la misma contraseña tengan el mismo hash y anula las tablas precalculadas.
- Función de derivación lenta: `bcrypt`, `scrypt` o `argon2`. Se les llama funciones
  deliberadamente caras: tardar 100 ms en verificar una contraseña es invisible para un usuario
  y arruina a quien intente probar mil millones de candidatas.
- Un `sha256` simple no vale para contraseñas: está diseñado para ser rapidísimo.

**Autorización.** Dos modelos que cubren casi todo:

- **RBAC (por roles).** El usuario tiene roles y cada rol tiene permisos. Fácil de auditar:
  «quién puede borrar facturas» se responde mirando la matriz.
- **ABAC o por propiedad.** La decisión depende del recurso concreto: puedes ver *este* pedido
  porque es tuyo. RBAC solo no basta aquí, y olvidarlo produce la vulnerabilidad más común de
  las APIs: cambiar el identificador de la URL y ver los datos de otro.

**Sesiones frente a tokens, en corto:**

- Revocación inmediata: sesión sí, token no.
- Estado en el servidor: sesión sí, token no.
- Funciona entre servicios sin consultar nada: token sí, sesión no.
- Tamaño de cada petición: la cookie son unos pocos bytes, un JWT con muchos claims puede ser
  de cientos.

## Ejemplo

Un usuario inicia sesión y el servicio emite un JWT con `{"sub": "42", "rol": "lector",
"exp": 1900000000}`. En la siguiente petición, `GET /v1/facturas/9`, el servidor:

1. Comprueba la firma. Si no cuadra, **401**.
2. Comprueba `exp`. Si ha caducado, **401** (y el cliente debe usar el refresh token).
3. Lee el rol y decide. `lector` puede ver la factura 9 solo si es suya; si es de otro cliente,
   **403** (o 404 si no quieres revelar que existe).

Cambiemos un carácter de la carga: si el atacante reescribe el rol como `admin`, la firma deja
de coincidir y la petición se rechaza. Ese es todo el mecanismo de integridad, y por eso la
clave de firma tiene que ser larga y vivir fuera del repositorio, en un gestor de secretos.

Sobre lo que cuesta una contraseña: un `sha256` tarda microsegundos, así que un atacante con una
tarjeta gráfica prueba miles de millones de combinaciones por segundo. Una función lenta tarda
del orden de decenas de milisegundos, y esa diferencia de varios órdenes de magnitud es todo el
diseño: no protege contra una contraseña débil para siempre, la hace tan cara de romper que
deja de merecer la pena.

## Código

```python verificable
import base64
import hashlib
import hmac
import json

CLAVE = b"secreto-de-firma"

def b64(datos: bytes) -> str:
    return base64.urlsafe_b64encode(datos).decode().rstrip("=")
    # base64url sin el relleno de "=": es el formato que exige un JWT; decode() pasa bytes a texto

def firmar(cabecera: dict, carga: dict) -> str:
    h = b64(json.dumps(cabecera, separators=(",", ":")).encode())
    c = b64(json.dumps(carga, separators=(",", ":")).encode())    # sin espacios: si cambian, cambia la firma
    firma = b64(hmac.new(CLAVE, f"{h}.{c}".encode(), hashlib.sha256).digest())
    # HMAC-SHA256 de "cabecera.carga" con la clave secreta; digest() devuelve los bytes
    return f"{h}.{c}.{firma}"

def verificar(token: str) -> bool:
    h, c, firma = token.split(".")                   # tres partes; si no son tres, el desempaquetado falla
    esperada = b64(hmac.new(CLAVE, f"{h}.{c}".encode(), hashlib.sha256).digest())
    return hmac.compare_digest(firma, esperada)      # comparacion en tiempo constante

token = firmar({"alg": "HS256", "typ": "JWT"}, {"sub": "42", "rol": "admin", "exp": 1900000000})
print("partes del token:", len(token.split(".")))    # -> 3 partes
print("firma valida:", verificar(token))             # -> True

# Nadie puede cambiar el rol sin la clave: la firma deja de cuadrar.
h, c, _ = token.split(".")
carga_falsa = b64(json.dumps({"sub": "42", "rol": "superadmin"}).encode())
print("token manipulado:", verificar(f"{h}.{carga_falsa}.{token.split('.')[2]}"))   # -> False
# la carga se lee y se reescribe sin ninguna clave (es texto); lo que no se puede es recalcular la firma
```

:::claves
- `b64` **no cifra nada**: base64url es una codificación, se revierte con cuatro líneas y sin clave. Cualquiera que tenga el token lee la carga entera; lo que no puede es cambiar nada sin la clave secreta.
- `separators=(",", ":")` quita los espacios que `json.dumps` pone por defecto. Si firmas con unos separadores y verificas con otros, el HMAC no coincide y todos los tokens fallan, aunque el contenido sea el mismo.
- `hmac.compare_digest` compara en **tiempo constante**: un `==` normal corta en el primer byte distinto y el tiempo que tarda filtra cuántos bytes has acertado. Es la diferencia entre comparar un sello y regalar la clave byte a byte.
- `token.split(".")` devuelve tres trozos y el desempaquetado falla con `ValueError` si hay más o menos: en el código real eso es un 401, no un 500.
- La carga falsa del ejemplo se construye **sin** `separators`: el token manipulado falla por el rol cambiado y también por el formato. En un ataque de verdad el atacante respeta el formato y solo cambia el valor; la firma lo rechaza igual.
- `hmac.new(CLAVE, mensaje, hashlib.sha256)`: la clave va **primero** y el mensaje después. Invertir esos dos argumentos compila y produce una firma válida, pero de un protocolo que no es JWT y que ningún otro servicio podrá verificar.
:::

```python verificable
# Matriz de permisos: que roles pueden hacer cada accion.
PERMISOS = {
    "ver":    {"lector", "editor", "admin"},     # conjuntos: la pertenencia es inmediata
    "editar": {"editor", "admin"},
    "borrar": {"admin"},
}

def autorizar(rol, accion):
    if rol is None:                              # is None, no == None: es el valor ausente
        return 401, "no se quien eres"
    if rol not in PERMISOS[accion]:
        # PERMISOS[accion] lanza KeyError si la accion no existe; en un servicio real, 404 o 405
        return 403, "se quien eres, pero no puedes"
    return 200, "adelante"                       # devuelve una tupla (codigo, motivo)

casos = [(None, "ver"), ("lector", "ver"), ("lector", "borrar"), ("admin", "borrar")]
for rol, accion in casos:
    estado, motivo = autorizar(rol, accion)      # desempaqueta la tupla que devuelve la funcion
    print(f"rol={str(rol):<7} accion={accion:<7} -> {estado} {motivo}")
    # :<7 alinea a la izquierda en 7 caracteres para que las columnas cuadren; str(None) es "None"
```

```python verificable
import hashlib
import time

sal = b"sal-aleatoria-por-usuario"
contrasena = b"correcta-caballo-bateria-grapadora"

inicio = time.perf_counter()          # reloj de pared con la mayor resolucion disponible
for _ in range(20_000):               # 20.000 vueltas para que sha256 sea medible
    hashlib.sha256(sal + contrasena).hexdigest()    # concatena sal y contrasena; devuelve texto hex
t_sha = time.perf_counter() - inicio  # segundos con decimales

inicio = time.perf_counter()
hashlib.scrypt(contrasena, salt=sal, n=2**14, r=8, p=1, dklen=32)
# n marca el coste (memoria y CPU) y dklen la longitud del hash; scrypt basta con un intento
t_scrypt = time.perf_counter() - inicio

print(f"sha256, 20000 intentos: {t_sha * 1000:7.1f} ms  ({t_sha / 20000 * 1000:.3f} ms por intento)")
# las dos cuentas son el mismo paso de segundos a milisegundos, una total y otra por intento
print(f"scrypt, 1 intento:      {t_scrypt * 1000:7.1f} ms  ({t_scrypt * 1000:.1f} ms por intento)")
print(f"un atacante prueba {t_scrypt / (t_sha / 20000):.0f} veces mas rapido con sha256")
# el cociente entre lo que cuesta un intento lento y uno rapido: esa es toda la defensa
```

:::figura
fichero: autenticacion-coste-de-la-contrasena
pie: Las dos caras del mismo diseño, con los órdenes de magnitud que mide el código de arriba. Izquierda, lo que cuesta probar una candidata: sha256 va a unos cinco millones de intentos por segundo y por núcleo porque está hecho para ser rapidísimo, mientras que scrypt con `n=2**14` baja a 17, porque cada intento gasta memoria y CPU a propósito. Derecha, el efecto sobre un atacante que quiera probar mil millones de candidatas: con sha256 son 200 segundos (un café) y con scrypt 58 millones de segundos, casi dos años. La defensa no es que el hash sea «más fuerte» ni que tenga más bits: es que cada intento sea caro, y ese coste lo pagas tú una vez por inicio de sesión.
fuente: figuras/autenticacion-y-autorizacion-1.py
:::

```python ilustrativo
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
esquema = HTTPBearer()                  # exige la cabecera Authorization: Bearer <token>
ALGORITMO = "HS256"                     # fijado en el servidor, jamas leido del token
# Con HS256 la clave es compartida: quien firma y quien verifica usan el MISMO secreto. Un
# servicio que solo verifica tokens de otro deberia usar un algoritmo asimetrico (RS256) y
# quedarse con la clave publica, que no le permite falsificar nada.

def usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(esquema)) -> dict:
    # dependencia: se ejecuta antes de la ruta y su resultado llega como argumento "usuario"
    try:
        carga = jwt.decode(credenciales.credentials, CLAVE_SECRETA, algorithms=[ALGORITMO],
                           audience="api.tienda.example", issuer="auth.tienda.example")
        # algorithms va como lista: PyJWT rechaza el token si su cabecera declara otro algoritmo
    except jwt.ExpiredSignatureError:
        # es subclase de InvalidTokenError, asi que tiene que ir ANTES que ella
        raise HTTPException(status_code=401, detail="token caducado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token invalido")
    return {"id": int(carga["sub"]), "rol": carga["rol"]}
    # los claims vuelven como JSON: sub es texto y hay que convertirlo a entero

@app.get("/v1/facturas/{factura_id}")
def leer_factura(factura_id: int, usuario: dict = Depends(usuario_actual)):
    factura = buscar_factura(factura_id)         # primero el recurso, despues los permisos
    if factura is None:
        raise HTTPException(status_code=404)     # 404 sin cuerpo: no revela si existe lo ajeno
    if factura["cliente_id"] != usuario["id"] and usuario["rol"] != "admin":
        # autorizacion por propiedad: el rol dice que puede leer facturas, no cuales
        raise HTTPException(status_code=403)
    return factura
```

## Errores típicos

- **Guardar contraseñas con un hash rápido o con un cifrado reversible.** `md5` o `sha256` sin
  sal se rompen con tablas precalculadas; el cifrado simétrico es peor todavía, porque un fallo
  de la base de datos entrega las contraseñas en claro. Usa bcrypt, scrypt o argon2 con sal por
  usuario.
- **Aceptar el algoritmo que dice el token.** Si el servidor hace caso al campo `alg`, un
  atacante puede pedir `none` o cambiar de asimétrico a simétrico y firmar con la clave pública.
  El algoritmo se fija en el código y se pasa como lista permitida al verificar.
- **Meter datos sensibles dentro del JWT.** El token va firmado, no cifrado: cualquiera lo
  decodifica. Dentro solo el identificador, el rol y poco más.
- **Confiar solo en el rol.** Comprobar que el usuario es `lector` pero no que la factura sea
  suya es la vulnerabilidad de referencia de las APIs: cambiar el 9 por el 10 en la URL y leer
  datos ajenos. Cada lectura de un recurso necesita su comprobación de propiedad.
- **No expirar el token o no tener refresh token.** Un JWT sin `exp` es una contraseña
  permanente que no se puede revocar. La práctica habitual es un token de acceso de minutos y
  uno de refresco guardado y revocable.
- **Meter el token en la URL.** Las URL acaban en los registros del proxy, en el historial y en
  la cabecera `Referer`. El token va en la cabecera `Authorization: Bearer ...`, nunca en un
  parámetro de consulta.
- **Implementar OAuth a mano.** Es un protocolo con detalle suficiente (validación del
  `redirect_uri`, el parámetro `state`, PKCE) como para que la implementación casera sea un
  agujero. Usa una biblioteca o un proveedor de identidad.
- **Confundir 401 y 403 al depurar.** Devolver 403 a quien no ha mandado credenciales hace que
  el cliente no sepa que tiene que autenticarse, y a veces que reintente en bucle.

## Comprueba que lo sabes

:::quiz
p: ¿Qué impide que alguien cambie su rol dentro de un JWT?
o: Que la carga va cifrada con la clave del servidor
o: Que la firma cubre cabecera y carga, así que cualquier cambio obliga a recalcularla y no se puede sin la clave
o: Que los roles se comprueban contra la base de datos en cada petición
a: 2
e: La carga no va cifrada: se lee con base64url sin ninguna clave. Lo que la protege es la firma, que solo puede recalcular quien tiene la clave secreta o privada. Si el servidor consultara la base de datos en cada petición, estaríamos ante una sesión, no ante un token autocontenido.
:::

:::quiz
p: Un usuario autenticado con rol lector pide la factura de otro cliente. ¿Qué respuesta es la correcta?
o: 401, porque no tiene permiso para ese recurso
o: 200, si el rol lector permite leer facturas en general
o: 403, porque el rol le permite la acción pero no sobre ese recurso
a: 3
e: La autorización tiene dos capas: la acción (puede leer facturas) y la propiedad (esa factura es suya). Si la primera pasa y la segunda no, es un 403; si no ha demostrado identidad, es un 401. Devolver 200 porque el rol genérico lo permite es exactamente la fuga de datos entre clientes.
:::

:::quiz
p: ¿Por qué no vale sha256 para guardar contraseñas?
o: Porque produce colisiones con facilidad
o: Porque está diseñado para ser rapidísimo, así que probar candidatas sale muy barato al atacante
o: Porque no admite sal
a: 2
e: El problema no es que sea débil, es que es rápido: su velocidad es una virtud para verificar ficheros y un desastre para contraseñas. Las funciones de derivación como bcrypt, scrypt o argon2 son deliberadamente costosas, y ese coste se lo comes tú una vez por inicio de sesión y el atacante en cada intento.
:::

:::trampa
El error más frecuente al empezar con JWT es creer que «firmado» significa «secreto». Pega tu
token en cualquier decodificador web y verás el identificador de usuario, el rol y la fecha de
expiración en claro. Si algo no quieres que se lea, no lo metas ahí.
:::

:::aviso
OAuth 2.0 resuelve autorización delegada, no autenticación. Usarlo como sistema de login sin
OpenID Connect encima lleva a problemas sutiles: el token de acceso no está pensado para
identificar al usuario y su formato y duración no son tuyos. Si necesitas «entrar con Google»,
lo que quieres es OpenID Connect.
:::
