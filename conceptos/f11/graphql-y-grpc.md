---
id: graphql-y-grpc
titulo: GraphQL y gRPC
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [apis-rest, apis-y-peticiones-http]
tags: [http, contratos, esquemas, rendimiento]
resumen: Consultar por esquema frente a protocolos binarios: cuándo conviene cada uno y qué precio se paga por elegir mal.
fuentes: ["gRPC Authors, 'Introduction to gRPC' (documentación oficial)", "GraphQL Foundation, 'GraphQL Specification'"]
---

## En una frase

GraphQL deja que el cliente pida los campos que necesita contra un único endpoint
descrito por un esquema, y gRPC sustituye el texto por mensajes binarios con contrato
generado, a cambio de perder la legibilidad y la caché que te daba HTTP.

## La idea

Con [[apis-rest|REST]] el servidor decide qué hay en cada respuesta. Eso funciona hasta que
tienes una pantalla móvil que solo necesita el nombre del cliente y el total del pedido, y le
llegan dos kilobytes de direcciones, líneas y metadatos que nadie va a pintar.

La salida
clásica es inventar un endpoint a medida (`/pedidos/42/resumen`), y a la tercera pantalla
distinta tienes siete endpoints que devuelven casi lo mismo.

GraphQL le da la vuelta: **un solo endpoint y el cliente elige los campos**. El contrato está
en un esquema tipado que dice qué se puede pedir, y el servidor rellena solo lo pedido. A
cambio, el servidor ya no puede cachear la respuesta por URL (todas las peticiones van al
mismo sitio), hay que defenderse de consultas carísimas y aparece un problema nuevo: resolver
el mismo campo en veinte elementos de una lista veinte veces.

gRPC es otra cosa. No va de elegir campos, va de **hablar rápido entre servicios que se
conocen**. Defines los mensajes en un fichero `.proto`, se generan las clases en el idioma que
uses y el transporte es HTTP/2 con mensajes binarios. Un mensaje de 6 campos ocupa decenas de
bytes en vez de un JSON lleno de nombres repetidos, y se pueden hacer llamadas en streaming en
los dos sentidos.

La regla práctica que resume el tema: **GraphQL es para clientes variados sobre la misma API
pública; gRPC es para servicios internos que se llaman mucho y no cambian a menudo.** Para una
API sencilla que devuelve un objeto y no crece, [[apis-rest|REST]] sigue siendo la opción más
barata de mantener.

## Definición formal

**GraphQL.** El servicio publica un esquema con tres bloques: `Query` para lecturas,
`Mutation` para escrituras y `Subscription` para flujos. Cada campo declara su tipo y si puede
ser nulo:

```text
type Pedido { id: ID!  total: Float!  cliente: Cliente!  lineas: [Linea!]! }
type Cliente { id: ID!  nombre: String!  email: String }
type Query { pedido(id: ID!): Pedido  pedidos(limite: Int = 20): [Pedido!]! }
```

El cliente manda una consulta y recibe la forma que ha pedido:

```text
{ pedido(id: 42) { total  cliente { nombre } } }   ->   {"data": {"pedido": {"total": 412.5, ...}}}
```

Todos los detalles van a `POST /graphql`, y el tipo de operación (`query` o `mutation`) viaja
en el cuerpo, no en la URL.

**gRPC.** El contrato es un `.proto` con mensajes y servicios. En proto3 cada campo lleva un
número que es lo que viaja por el cable, no el nombre:

```text
syntax = "proto3";
message Pedido { int64 id = 1;  double total = 2;  string cliente = 3; }
service Pedidos { rpc Obtener (PedidoRequest) returns (Pedido); }
```

Ese entero de posición es un *tag*: si renumeras un campo, rompes a todos los clientes
desplegados. Los modos de comunicación son cuatro: unaria (petición y respuesta), respuesta en
stream, petición en stream y bidireccional.

Comparación honesta de los tres estilos:

- **Tamaño y velocidad.** REST con JSON repite los nombres de los campos en cada objeto. gRPC
  manda solo tags y valores, y comprime con HTTP/2, así que suele ocupar bastante menos.
- **Contrato.** gRPC y GraphQL lo tienen explícito y verificable; REST lo tiene en una
  convención que solo existe si alguien la documenta.
- **Depuración.** Un `curl` contra REST se lee de un vistazo. gRPC necesita herramientas que
  entiendan el `.proto`, y GraphQL necesita ver la consulta y los resolvers, no solo la
  respuesta.
- **Caché.** REST se cachea por URL en cualquier CDN sin hacer nada. GraphQL casi nunca, y
  gRPC necesita caché a nivel de aplicación.
- **Navegador.** REST y GraphQL funcionan con `fetch`. gRPC puro no: en web se usa gRPC-Web o
  un proxy que traduzca.

:::formula
coste de una consulta = coste de recorrer los nodos + coste de resolver cada campo
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `coste de una consulta` | Lo que el servidor tarda en resolver una petición del cliente, de principio a fin | ms o consultas a la base de datos | Es lo que hay que limitar antes de exponer el endpoint: profundidad máxima, análisis de coste y tiempo tope por consulta |
| `coste de recorrer los nodos` | Resolver la lista de nivel superior: una consulta que devuelve N elementos | consultas | Crece una sola vez, con el tamaño de la lista: 100 pedidos siguen siendo 1 consulta |
| `coste de resolver cada campo` | Resolver un campo anidado dentro de cada nodo | consultas por nodo | Es el término que se dispara: sin batching son N consultas (el N+1) y con DataLoader son 1 más |
| `nodos` | Elementos que devuelve la lista padre | elementos | Multiplica solo el segundo sumando; por eso una lista larga con campos anidados caros es el peor caso |
| `campos` | Campos anidados que se piden dentro de cada nodo | campos | Cada campo nuevo se resuelve por nodo: pedir diez campos anidados multiplica el trabajo por diez |
:::

## Ejemplo

Supón que el pedido 42 tiene dos líneas. Con `GET /pedidos/42` la respuesta incluye
identificador, fecha, estado, total, el cliente entero con su dirección y las dos líneas, y el
cliente solo quería el total. La consulta GraphQL `{ pedido(id: 42) { total } }` devuelve un
único campo.

Ahora el problema del N+1, que es el error clásico de GraphQL. Pides cien pedidos con su
cliente. Si el resolver de `cliente` hace una consulta a la base de datos por cada pedido,
tienes **1 consulta para la lista más 100 para los clientes: 101**. Con REST, si el endpoint de
pedidos trae ya el nombre del cliente, es 1. La solución se llama *DataLoader* o *batching*:
agrupar las cien claves, hacer una sola consulta con un `WHERE id IN (...)` y repartir los
resultados. De 101 consultas a 2.

Y una medida del formato binario: un identificador pequeño en un mensaje protobuf ocupa 1 byte
de clave más 1 de valor, mientras que en JSON es el nombre del campo entre comillas, el valor y
los separadores.

## Código

```python verificable
# Cuanto se desperdicia mandando el objeto entero cuando solo hace falta un campo.
consulta_rest = {                  # /pedidos/42 trae todo, aunque solo quieras el total
    "id": 42, "fecha": "2026-01-05", "estado": "enviado", "total": 412.5,
    "cliente": {"id": 7, "nombre": "Ana", "email": "ana@ejemplo.com", "direccion": "Calle Mayor 3"},
    "lineas": [{"producto": "A", "cantidad": 2, "precio": 12.5},
               {"producto": "B", "cantidad": 1, "precio": 30.0}],
}

def tamano(objeto):
    if isinstance(objeto, dict):
        # suma recursiva de claves y valores; no cuenta llaves, comas ni dos puntos
        return sum(tamano(k) + tamano(v) for k, v in objeto.items())
    if isinstance(objeto, list):
        return sum(tamano(x) for x in objeto)     # en una lista no hay claves, solo valores
    return len(str(objeto))                       # una hoja se mide por su texto: 412.5 son 5

pedido_graphql = {"total": 412.5}   # la consulta pide exactamente un campo

print("tamano REST:", tamano(consulta_rest), "caracteres")      # -> 165 caracteres
print("tamano GraphQL:", tamano(pedido_graphql), "caracteres")  # -> 10 caracteres
print("sobra:", round(tamano(consulta_rest) / tamano(pedido_graphql), 1), "veces mas datos")
# la division con / siempre devuelve float; round lo deja en un decimal para leerlo
```

:::claves
- `tamano` **no cuenta llaves, comas ni dos puntos**: suma los nombres y los valores recursivamente. Los 165 caracteres son una estimación por abajo; el `json.dumps` del mismo objeto ocupa más. Si en el `sum` te dejaras fuera `tamano(k)`, estarías midiendo solo los valores y el resultado cambiaría por completo.
- `isinstance(objeto, dict)` y `isinstance(objeto, list)` son los dos casos recursivos y el `return len(str(objeto))` es el caso base: números y textos. En Python `True` es un `int`, así que `len(str(True))` son 4 caracteres.
- `{"total": 412.5}` no es lo que devuelve GraphQL por el cable: la respuesta real va envuelta en `{"data": {"pedido": ...}}`, así que esos 10 caracteres son del campo, no del mensaje entero. La comparación es honesta como *forma*, no como tamaño final.
- `varint` devuelve una **lista de enteros**, no bytes, y por eso `varint(tag) + varint(valor)` concatena listas: `[8] + [42]` da `[8, 42]`. Si los valores fueran enteros, el `+` los sumaría y el mensaje saldría mal sin dar ningún error.
- `byte | (0x80 if n else 0)` pone el bit alto a 1 mientras queden bytes: así el decodificador sabe si tiene que seguir leyendo. El último byte va sin ese bit, y un varint mal terminado hace que el receptor se coma los bytes del campo siguiente.
- `tag = (campo << 3)` mete el número de campo en los bits altos y deja los 3 bajos para el tipo (0 es varint). Con `campo = 1` el tag vale 8. Cambiar el número de un campo en el `.proto` cambia el tag y rompe a los clientes ya desplegados, aunque el nombre siga igual.
:::

:::figura
fichero: graphql-y-grpc-consultas-y-bytes
pie: Izquierda, lo que cuesta de verdad la misma pantalla de 100 pedidos: REST con el cliente ya incluido gasta 1 consulta, GraphQL con batching (DataLoader) gasta 2 y GraphQL sin batching gasta 101, porque el resolver del campo anidado se ejecuta una vez por elemento. Derecha, el mismo mensaje —id 42, total 412,5 y cliente «Ana»— en JSON y en protobuf: los valores ocupan 12 bytes en los dos formatos, así que toda la diferencia (44 frente a 16 bytes) está en la estructura. En JSON el nombre de cada campo, las llaves y las comas son 32 de los 44 bytes; en protobuf solo hay un tag de un byte por campo. Esa es la razón de que gRPC sea más barato entre servicios y de que GraphQL necesite medir el coste por consulta, no solo los bytes que viajan.
fuente: figuras/graphql-y-grpc-1.py
:::

```python verificable
# Como codifica protobuf un entero: tag en los bits bajos, varint para el valor.
def varint(n):
    bytes_salida = []
    while True:
        byte = n & 0x7F            # los 7 bits bajos del numero
        n >>= 7                    # el resto se desplaza: sera el byte siguiente del varint
        bytes_salida.append(byte | (0x80 if n else 0))   # 0x80 = "hay mas bytes"; el ultimo va sin el
        if not n:
            return bytes_salida    # devuelve una lista de enteros, no bytes

for campo, valor in [(1, 42), (2, 40000), (3, 9000000)]:
    tag = (campo << 3)              # 3 bits de tipo (0 = varint) + n. de campo
    codificado = varint(tag) + varint(valor)    # concatenar listas: primero el tag, luego el valor
    print(f"campo {campo} valor {valor:>7} -> {len(codificado)} bytes: {codificado}")
print("el mismo numero en JSON ocupa tambien el nombre del campo y las comillas")
```

## Errores típicos

- **Adoptar GraphQL sin limitar la profundidad ni la complejidad.** Un cliente puede pedir una
  consulta anidada que recorre media base de datos. Hay que poner límite de profundidad,
  análisis de coste y tiempo máximo por consulta antes de exponer el endpoint.
- **Resolver campos de una lista uno a uno.** Es el N+1: cien pedidos se convierten en 101
  consultas. Se arregla con *batching* (DataLoader) o cargando los datos en el resolver padre.
- **Creer que GraphQL sustituye a la autorización.** El cliente elige la forma, no los permisos:
  cada resolver tiene que comprobar si el usuario puede ver ese campo. Ocultar un campo en el
  esquema no lo protege si sigue siendo resoluble.
- **Renumerar o reutilizar tags en un `.proto`.** El número es la identidad del campo en el
  cable; cambiar el 2 por otro nombre hace que los clientes viejos lean basura. Los campos se
  marcan como `reserved` y no se reutilizan.
- **Buscar en gRPC un navegador.** gRPC puro necesita HTTP/2 con tramas que el navegador no
  expone; hay que poner gRPC-Web y un proxy delante. Si el consumidor es una web, quizá REST o
  GraphQL salgan más baratos.
- **Elegir gRPC entre servicios que no se conocen.** El contrato rígido es una ventaja cuando
  ambos lados se despliegan juntos y una carga cuando el otro equipo publica cuando quiere. Para
  una API abierta a terceros, un `.proto` obligatorio es una barrera de entrada.
- **Cambiar la forma de las respuestas de REST sin versionar.** REST sin contrato explícito se
  rompe en silencio: el cliente no falla con un error de tipos, simplemente lee `undefined`.

## Comprueba que lo sabes

:::quiz
p: Pides cien pedidos con GraphQL y cada uno necesita su cliente. ¿Por qué pueden salir 101 consultas a la base de datos?
o: Porque GraphQL no permite hacer uniones
o: Porque el resolver del campo cliente se ejecuta una vez por elemento de la lista
o: Porque el esquema obliga a cargar el objeto completo
a: 2
e: Ese es el problema N+1: la lista se resuelve con una consulta y cada campo anidado lanza la suya. Se corrige agrupando las claves y resolviendo el campo con una sola consulta `IN`, que es lo que hacen las librerías de batching.
:::

:::quiz
p: ¿Qué se gana y qué se pierde al pasar de REST con JSON a gRPC entre dos servicios internos?
o: Se gana tamaño y velocidad de serialización, y se pierde la caché por URL y la facilidad de depurar con curl
o: Se gana caché por URL y se pierde el tipado
o: Se gana compatibilidad con el navegador y se pierde el streaming
a: 1
e: gRPC manda binario con tags en vez de nombres de campo, así que ocupa menos y serializa más rápido, y añade streaming. A cambio, todos los mensajes van a métodos, no a URL cacheables, y hace falta herramienta específica para inspeccionarlos.
:::

:::trampa
GraphQL promete que el cliente pide solo lo que necesita, y eso es cierto; lo que no promete es
que el servidor lo consiga barato. Una consulta de tres campos puede esconder veinte consultas
a la base de datos. Mide el coste por consulta, no la cantidad de datos que viaja.
:::

:::nota
Los esquemas de GraphQL admiten introspección, que es lo que permite generar documentación y
clientes automáticamente. En producción muchas empresas la desactivan total o parcialmente para
no publicar toda la superficie de su API a cualquiera que pregunte.
:::
