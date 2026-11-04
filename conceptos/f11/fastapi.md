---
id: fastapi
titulo: FastAPI
fase: 11
nivel: intermedio
rutas: [alg, ds]
prerequisitos: [apis-rest, tipado-y-linters, concurrencia-async-hilos-procesos]
tags: [python, http, validacion, backend]
resumen: Rutas, validación con Pydantic, inyección de dependencias y documentación automática: el marco para servir un modelo en Python.
fuentes: ["FastAPI, 'Documentación oficial'", "Pydantic, 'Documentación oficial'"]
---

## En una frase

FastAPI es el marco que convierte anotaciones de tipo de Python en validación de datos,
documentación interactiva y servidor HTTP, de forma que la mayor parte de las peticiones mal
formadas mueren antes de llegar a tu código.

## La idea

Escribir un servicio HTTP a mano tiene una parte aburrida y repetitiva: comprobar que llega un
campo, que es un número, que está en rango, que el JSON es válido, y devolver un error con
sentido cuando no lo es. Si esa comprobación se olvida en un endpoint, ya tienes un 500 en
producción por un campo nulo.

FastAPI parte de una idea muy concreta: **el tipo que ya habrías escrito para el editor puede
validar la petición**. Declaras una clase Pydantic con sus campos y sus restricciones, la usas
como anotación del parámetro, y el marco hace el resto: si el cuerpo no encaja, responde él
mismo con un 422 y una lista de qué campo ha fallado y por qué, sin que tú escribas un solo
`if`.

Lo segundo que aporta es **cero documentación desincronizada**. Del mismo esquema de Pydantic
se genera el documento OpenAPI, y de ahí una página interactiva donde cualquiera puede probar
tu API sin abrir Postman. La documentación no es un fichero aparte que se queda viejo: se
deriva del código que se ejecuta.

Lo tercero es **inyección de dependencias**. Cosas que toda petición necesita —la conexión a
base de datos, el usuario autenticado, los parámetros de paginación— se declaran una vez como
funciones y el marco las resuelve y las cierra al terminar. Y aquí está el matiz asíncrono: si
tu función es `def` normal, FastAPI la ejecuta en un grupo de hilos, así que **no bloqueas el
bucle de eventos** aunque uses bibliotecas síncronas. Si es `async def`, se ejecuta en el
bucle, y entonces cualquier llamada bloqueante que hagas dentro sí para a todos los demás. Ese
detalle es la causa número uno de servicios que se atascan.

## Definición formal

Piezas del marco:

- **Aplicación.** `app = FastAPI()` es el objeto que agrupa rutas y configuración. Se arranca
  con un servidor ASGI (`uvicorn app:app`).
- **Decorador de ruta.** `@app.get("/pedidos/{pedido_id}")` registra una función para el método
  HTTP y la ruta. Existen `get`, `post`, `put`, `patch`, `delete`. El orden de declaración
  importa: una ruta dinámica declarada antes se come a las fijas que vengan después.
- **Validación de entrada.** Tres orígenes distintos, y conviene no confundirlos:
  - Parámetros de ruta: aparecen en la URL entre llaves y llegan como argumentos.
  - Parámetros de consulta: argumentos con valor por defecto (`limite: int = 20`).
  - Cuerpo: un modelo Pydantic anotado. Lo que no esté declarado en el modelo **se ignora**,
    no se copia al objeto.
- **Códigos.** Por defecto un POST responde 200; para crear de verdad se declara
  `status_code=201`. Un error de validación responde 422 con la lista de fallos. Un fallo de
  negocio se lanza con `HTTPException(status_code=404, detail="...")`.
- **Dependencias.** `Depends(funcion)` resuelve el parámetro antes de llamar a la ruta. Si la
  misma dependencia se pide varias veces **dentro de la misma petición**, se calcula una sola
  vez (caché por petición); entre peticiones distintas se recalcula.
- **Modelos.** Pydantic valida y convierte: `int`, `float`, `str`, `bool`, `datetime`, listas,
  modelos anidados. `Field(ge=, le=, max_length=)` añade restricciones. Los validadores con
  `@field_validator` normalizan valores (recortar espacios, pasar a minúsculas).
- **Modelos separados para entrada y salida.** Es la práctica habitual: `UsuarioEntrada` con lo
  que el cliente puede mandar y `UsuarioSalida` con lo que puede ver. Así la contraseña no se
  escapa en la respuesta por despiste.

## Ejemplo

Supón un endpoint de alta de usuario con `email` y `edad`. Tres peticiones y tres respuestas:

- `POST /v1/usuarios` con `{"email": "ana@ejemplo.com", "edad": 30}` → **201** y el usuario
  creado sin el campo de contraseña.
- `POST /v1/usuarios` con `{"email": "ana@ejemplo.com", "edad": 15}` → **422**, con
  `loc: ["body", "edad"]` y el mensaje «debe ser mayor o igual que 18».
- `POST /v1/usuarios` con `{"email": "ana@ejemplo.com", "edad": "treinta"}` → **422**, porque
  el valor no se puede convertir a entero.

Fíjate en que la tercera es un problema de *conversión* y la segunda de *regla de negocio*, pero
las dos acaban en el mismo código 422 con distinto detalle. Ese es el comportamiento por
defecto de FastAPI y es lo que quieres: el cliente recibe siempre la misma forma de error.

Para la consulta, `GET /v1/pedidos?limite=100&offset=200` declara `limite: int = 20` y
`offset: int = 0`. Si el cliente manda `?limite=cien`, el parámetro no se puede convertir y la
respuesta es 422; si manda 5000 y tú has puesto `le=100` con `Query`, también.

## Código

```python verificable
from pydantic import BaseModel, Field, ValidationError, field_validator

class AltaUsuario(BaseModel):
    email: str
    edad: int = Field(ge=18, le=120)      # cotas incluidas: 18 y 120 pasan, 17 y 121 no

    @field_validator("email")             # se ejecuta al validar ese campo, no al leer la clase
    @classmethod                          # Pydantic v2 exige este decorador DEBAJO del validador
    def normalizar(cls, v: str) -> str:
        return v.strip().lower()           # normaliza antes de guardar: sin espacios y en minusculas

print(AltaUsuario(email="  Ana@Ejemplo.COM ", edad=30))   # -> email='ana@ejemplo.com' edad=30

# Lo que el usuario manda como texto y FastAPI convierte a int: si no puede, responde 422.
try:
    edad = int("treinta")
except ValueError as exc:
    print("422 Unprocessable Entity:", exc)               # -> 422 Unprocessable Entity: invalid literal for int() with base 10: 'treinta'

try:
    AltaUsuario(email="ana@ejemplo.com", edad=15)
except ValidationError as exc:            # hereda de ValueError: capturarlo por su nombre lo distingue
    print("422:", exc.errors()[0]["msg"])                 # -> 422: Input should be greater than or equal to 18
# errors() devuelve una lista con un fallo por campo; [0] es el primero, el de la edad
```

:::claves
- `Field(ge=18, le=120)` son cotas **incluidas**: 18 y 120 son válidos. Cambiar `ge` por `gt` haría que 18 fallara, y el mensaje de error seguiría hablando de 18, así que el despiste no se ve hasta que un cliente manda justo el valor del borde.
- `@classmethod` tiene que ir **debajo** de `@field_validator`, no encima: en Pydantic v2 el orden contrario lanza un error al definir la clase, no al validar. `cls` es la clase (no una instancia) y `v` el valor del campo tal como llegó.
- `AltaUsuario(...)` devuelve un objeto, no un diccionario: se lee con `usuario.email`, y `usuario["email"]` falla con `TypeError`. El `print` se ve ordenado porque Pydantic redefine el `__repr__`.
- `ValidationError` **hereda de `ValueError`**, así que un `except ValueError` genérico lo captura igual y te deja sin distinguir un dato inválido de un fallo tuyo. `errors()` da un diccionario por campo con `loc`, `msg` y `type`; `[0]` es solo el primero.
- Por defecto Pydantic **ignora los campos que no están declarados** en el modelo: `AltaUsuario(emial="...")` no da error y el campo se pierde. Si eso importa, el modelo se declara con `model_config = ConfigDict(extra="forbid")`.
- En el segundo bloque, `global llamadas` no es decorativo: sin él, `llamadas += 1` crearía una variable local y la de fuera se quedaría en 0 (Python lanza `UnboundLocalError`, porque la asignación convierte el nombre en local en toda la función).
- `db1 is db2 is db3` compara **identidad**, no igualdad: es la comprobación correcta para la caché de dependencias. La caché vive en el diccionario que se crea dentro de `manejar_peticion`, así que dura lo que dura la petición; la segunda petición vuelve a abrir la conexión.
:::

```python verificable
llamadas = 0

def get_db():
    """Dependencia cara: abrir conexion. FastAPI la cachea dentro de la misma peticion."""
    global llamadas                       # sin global, llamadas += 1 seria una variable local
    llamadas += 1
    return {"conexion": llamadas}

def manejar_peticion(usar_cache=True):
    cache = {}                            # diccionario nuevo: la cache no sobrevive a la peticion
    def dep(nombre):
        if not usar_cache or nombre not in cache:
            cache[nombre] = get_db()      # solo se abre la conexion la primera vez que se pide
        return cache[nombre]
    return dep("db"), dep("db"), dep("db")   # las tres devuelven el MISMO objeto

antes = llamadas
db1, db2, db3 = manejar_peticion(usar_cache=True)
print("misma peticion, 3 usos:", db1 is db2 is db3, "->", llamadas - antes, "apertura")   # -> True -> 1 apertura
# is compara identidad (el mismo objeto), no igualdad: es justo lo que se quiere comprobar

antes = llamadas
manejar_peticion(usar_cache=False)
print("dependencia no cacheada:", llamadas - antes, "aperturas")                          # -> 3 aperturas
```

```python ilustrativo
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="API de pedidos")

class PedidoSalida(BaseModel):
    id: int
    total: float

def get_db():
    db = abrir_pool()                  # dependencia real: conexion a la base de datos
    try:
        yield db                       # FastAPI cierra el generador al acabar la peticion
    finally:
        db.close()

@app.get("/v1/pedidos/{pedido_id}", response_model=PedidoSalida)
def leer_pedido(pedido_id: int, db=Depends(get_db)):
    # pedido_id llega ya convertido a int por la anotacion; db lo resuelve FastAPI antes de llamar
    fila = db.buscar(pedido_id)
    if fila is None:
        raise HTTPException(status_code=404, detail="pedido no encontrado")   # corta y responde 404
    return fila                        # se valida contra PedidoSalida antes de salir

@app.get("/v1/pedidos")
def listar(limite: int = Query(20, ge=1, le=100), offset: int = 0, db=Depends(get_db)):
    # Query pone el valor por defecto y las cotas: ?limite=1000000 se rechaza con un 422
    # el enlace siguiente se calcula sumando; copiar el offset devolveria la misma pagina
    return {"datos": db.listar(limite, offset), "siguiente": f"?limite={limite}&offset={offset + limite}"}
```

:::figura
fichero: fastapi-bloqueo-del-bucle
pie: Ocho peticiones de 50 ms que llegan a la vez, con el mismo trabajo dentro de cada una. Arriba, la función está declarada `async def` y dentro hay una llamada bloqueante (un `requests.get`, un `time.sleep` o un driver de base de datos síncrono): el bucle de eventos no puede soltar la petición, así que las demás hacen cola y la última, la naranja, empieza a los 350 ms y acaba a los 400. Abajo, la misma función declarada `def` normal, que FastAPI manda a un grupo de hilos: las ocho acaban a los 50 ms. No es que los hilos sean más rápidos, es que ninguno espera a los otros. La regla que se deduce de la figura: dentro de `async def` solo puede haber esperas asíncronas; si la biblioteca es síncrona, se declara `def` y se deja que el marco use un hilo.
fuente: figuras/fastapi-1.py
:::

## Errores típicos

- **Declarar `async def` y hacer dentro una llamada bloqueante.** Un `requests.get`, un
  `time.sleep` o un driver de base de datos síncrono dentro de una corrutina paran el bucle
  entero: todas las peticiones concurrentes esperan. O usas `def` normal (FastAPI la manda a un
  hilo) o usas cliente asíncrono de verdad.
- **Confiar en el orden de las rutas dinámicas.** Si declaras `/pedidos/{pedido_id}` antes que
  `/pedidos/resumen`, la petición al resumen entra por la primera, intenta convertir «resumen» a
  entero y devuelve 422. Las rutas fijas van antes.
- **Devolver el modelo de entrada tal cual.** Si el modelo de alta lleva `password` o
  `es_admin`, acabas de publicarlos en la respuesta. Separa el modelo de salida y decláralo en
  `response_model`.
- **Usar la caché de dependencias para compartir estado entre peticiones.** La caché dura lo que
  dura la petición; un contador guardado ahí no se acumula y dos peticiones concurrentes no lo
  ven. El estado compartido va en la base de datos, en Redis o en un objeto de la aplicación.
- **Dejar que Pydantic ignore campos de más sin pensarlo.** El comportamiento por defecto
  descarta lo no declarado, lo cual está bien para no romper clientes, pero significa que un
  campo mal escrito (`emial`) no da error: la petición pasa y el dato falta. Si eso te importa,
  activa la prohibición de campos extra en el modelo.
- **Registrar datos sensibles en los errores de validación.** El 422 incluye el valor recibido en
  algunos casos; si el campo era una contraseña o un token, acabas de escribirlo en los registros
  y en el historial del navegador.
- **Servir con el servidor de desarrollo.** `uvicorn --reload` es para programar. En producción
  se usan varios procesos trabajadores y un proxy delante que corte las peticiones lentas.
- **No poner límite a los parámetros de consulta.** `limite: int = 20` sin cota deja que alguien
  pida `?limite=1000000`. La cota va en el propio tipo, con `Query(20, le=100)`.

## Comprueba que lo sabes

:::quiz
p: Declaras `def leer(pedido_id: int)` y llega la petición `/pedidos/abc`. ¿Qué contesta FastAPI?
o: Un 500, porque int("abc") lanza una excepción dentro de tu función
o: Un 422, porque el parámetro no se puede convertir al tipo declarado y la validación ocurre antes de llamar a tu función
o: Un 404, porque esa ruta no existe
a: 2
e: La conversión y la validación las hace el marco antes de ejecutar tu código, así que la excepción nunca llega a tu función. El 422 lleva el detalle de qué parámetro falló. Un 500 indicaría un fallo no controlado, y la ruta sí existe: lo que no encaja es el valor.
:::

:::quiz
p: ¿Qué pasa si dos dependencias de la misma petición piden la misma función con Depends?
o: Se ejecuta dos veces y abre dos conexiones
o: Se ejecuta una sola vez en esa petición y las dos reciben el mismo resultado
o: Da error de configuración por dependencia duplicada
a: 2
e: FastAPI cachea el resultado de cada dependencia durante la petición, así que la apertura cara se paga una vez. Esa caché no sobrevive a la petición: en la siguiente se vuelve a ejecutar. Si necesitas que no se reutilice, se desactiva la caché en el propio Depends.
:::

:::quiz
p: ¿Por qué una función `async def` puede ser peor que una `def` normal si usas una biblioteca síncrona?
o: Porque ocupa un hilo del grupo y ralentiza el arranque
o: Porque se ejecuta en el bucle de eventos y cualquier llamada bloqueante detiene a todas las demás peticiones
o: Porque FastAPI no admite bibliotecas síncronas en funciones async
a: 2
e: Una función `def` se envía a un grupo de hilos y bloquear un hilo no bloquea el servidor. Dentro de `async def` no hay hilo extra: una espera bloqueante congela el bucle y con él todas las peticiones en curso.
:::

:::practica
enunciado: Escribe el modelo Pydantic y la firma de un endpoint POST /v1/productos que reciba nombre (entre 3 y 60 caracteres), precio (mayor que 0) y etiquetas (lista, máximo 5), y que devuelva el producto con su id y su fecha de creación. Indica qué código de estado usar.
pista: El modelo de entrada y el de salida no tienen por qué ser el mismo.
solucion: `class ProductoEntrada(BaseModel): nombre: str = Field(min_length=3, max_length=60); precio: float = Field(gt=0); etiquetas: list[str] = Field(default_factory=list, max_length=5)` y `class ProductoSalida(ProductoEntrada): id: int; creado: datetime`. La firma sería `@app.post("/v1/productos", response_model=ProductoSalida, status_code=201)` con `def crear(datos: ProductoEntrada, db=Depends(get_db))`. El 201 es lo correcto porque se crea un recurso y conviene devolver la cabecera Location hacia `/v1/productos/{id}`. Una etiqueta repetida o un precio de 0 no llegan a la función: las corta la validación con un 422.
:::

:::truco
Abre `/docs` en cuanto levantes el servicio. La página interactiva se genera del esquema, y ver
los campos y los tipos que espera cada endpoint es la forma más rápida de detectar que has
declarado mal un modelo: si un campo no aparece ahí, FastAPI no lo está leyendo.
:::
