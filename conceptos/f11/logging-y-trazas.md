---
id: logging-y-trazas
titulo: Registro y trazas
fase: 11
nivel: intermedio
rutas: [alg, de]
prerequisitos: [apis-rest, rendimiento-y-perfilado]
tags: [logging, trazas, observabilidad, depuracion]
resumen: Registrar para poder depurar: niveles con contrato, mensajes estructurados, identificadores de correlación y trazas que enseñan dónde se fue el tiempo.
fuentes: ["Beyer y otros (2016), 'Site Reliability Engineering'", "Majors, Fong-Jones, Miranda (2022), 'Observability Engineering'"]
---

## En una frase

Un registro es una línea con contexto que sobrevive al proceso, y una traza es el árbol de
tiempos de una petición repartida entre servicios; las dos cosas solo sirven si se pueden
buscar por identificador y correlacionar entre sí.

## La idea

Cuando alguien dice «a veces va lento», tienes tres herramientas y cada una responde a una
pregunta distinta:

- **Métrica:** ¿está pasando y desde cuándo? Un número agregado por minuto, barato de guardar y
  de consultar, pero sin detalle.
- **Traza:** ¿dónde se fue el tiempo en esa petición concreta? El árbol de llamadas con la
  duración de cada tramo.
- **Registro:** ¿por qué pasó? La línea con los datos del caso concreto.

Con las tres, la investigación es una secuencia: la métrica dice que el percentil 99 subió de
200 a 900 ms a las 10:14; una traza lenta de esa franja muestra que 700 ms se van en una
consulta; y las líneas de registro de esa petición, encontradas por su identificador, dicen con
qué parámetros se ejecutó la consulta. Sin el identificador que une las tres, cada herramienta
es un compartimento estanco y la investigación se convierte en adivinación.

**Registro estructurado.** La diferencia entre estas dos formas de escribir lo mismo es enorme:

- `logger.info(f"cobro aceptado pedido={pedido} importe={importe}")`
- `logger.info("cobro aceptado", extra={"campos": {"pedido": pedido, "importe": importe}})`

La primera genera un texto distinto para cada pedido: para agrupar o contar hay que escribir
expresiones regulares y rezar. La segunda deja un mensaje **fijo** y unos campos aparte, así
que puedes contar cuántos «cobro aceptado» hay por minuto, filtrar por `importe > 1000` o
construir un panel sin tocar el código. Regla práctica: **el mensaje es una constante y los
datos variables van en campos**.

**Niveles con contrato.** Un nivel no describe cómo se siente el programador, describe qué
debería hacer quien lo lee:

- `DEBUG` — detalle para reproducir un problema. En producción, apagado o encendido a demanda.
- `INFO` — lo que hizo el sistema: petición servida, trabajo terminado, mensaje consumido. Una
  línea por unidad de trabajo.
- `WARNING` — algo raro que se resolvió solo: un reintento que funcionó, un valor por defecto
  aplicado. No requiere que nadie se levante.
- `ERROR` — una operación falló y alguien debería mirarlo. Si tu sistema reintenta y casi
  siempre acierta, eso no es un error: es un aviso.
- `CRITICAL` — el proceso no puede seguir.

Cuando se marca todo como error, el nivel deja de significar nada y las alertas se ignoran.
Es el fallo más común y el más caro.

**Correlación.** Un identificador por petición, generado en el borde del sistema y propagado a
todo lo que toque esa petición: llamadas HTTP, mensajes de cola, tareas en segundo plano,
trabajos por lotes. Ese identificador va en cada línea de registro. Si cada servicio se inventa
el suyo, no hay forma de reconstruir el recorrido. Con trazas, además, se propaga el
identificador de traza y el de la traza padre, así que los tramos se pueden unir aunque
atraviesen cinco servicios.

**Y una cuenta que casi nadie hace: el registro cuesta dinero.** Cada línea se escribe, se
transporta, se indexa y se guarda. Activar el nivel de depuración en producción sin pensar
multiplica el volumen por decenas y la factura con él. La solución no es registrar menos
siempre, es muestrear: guardar el 100 % de los errores y una fracción de los casos que salen
bien.

## Definición formal

**Una entrada de registro** es una tupla:

:::formula
(timestamp, nivel, logger, mensaje, campos, trace_id, span_id)
:::

- `timestamp` — instante del suceso, en UTC y en formato ISO 8601 con zona. En hora local, un
  cambio de horario desordena el historial.
- `nivel` — uno de los cinco anteriores.
- `logger` — de dónde viene (módulo, servicio).
- `mensaje` — texto fijo, de **cardinalidad baja**: unos cientos de mensajes distintos en todo
  el sistema.
- `campos` — pares clave-valor de **cardinalidad alta**: identificadores, importes, duraciones.
- `trace_id`, `span_id` — identificadores que permiten unir la línea con su traza.

**Cardinalidad.** Es la clave para no arruinarte. Si el mensaje lleva datos dentro, su
cardinalidad se dispara:

:::formula
cardinalidad(mensaje) ≈ cardinalidad(campos)   ← lo que NO hay que hacer
:::

Con el mensaje fijo, `cardinalidad(mensaje)` se queda en cientos y el índice es pequeño; los
identificadores viven en los campos, que se indexan aparte o se buscan bajo demanda.

**Una traza** es un árbol de tramos (*spans*). Cada tramo tiene:

- `trace_id` — común a toda la traza.
- `span_id` y `parent_span_id` — posición en el árbol.
- `nombre`, `inicio`, `duración`, `estado` y atributos.

**Descomposición del tiempo.** Para un tramo padre con duración `D` y el conjunto de sus tramos
hijo `H`:

:::formula
tiempo_propio(padre) = D − (unión de los intervalos de H)
:::

Se usa la **unión**, no la suma, porque los hijos pueden solaparse (llamadas en paralelo): dos
consultas simultáneas de 100 ms ocupan 100 ms del padre, no 200. Si el tiempo propio sale
negativo, la instrumentación está mal o los relojes de las máquinas están desfasados
([[sistemas-distribuidos-bases]]).

**Volumen de registro.** El presupuesto diario es:

:::formula
bytes_por_día = rps × líneas_por_petición × bytes_por_línea × 86400
:::

- `rps` — peticiones por segundo.
- `líneas_por_petición` — cuántas líneas escribe el sistema por cada petición.
- `86400` — segundos de un día.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `bytes_por_día` | Lo que hay que escribir, transportar, indexar y guardar cada día | bytes | Es lo que se paga: entra en la factura del sistema de registro, no en la del servicio |
| `rps` | Peticiones por segundo que atiende el sistema | peticiones/s | Sube el volumen en línea recta: el doble de tráfico es el doble de registro |
| `líneas_por_petición` | Líneas que escribe el código por cada petición | líneas | Es la palanca barata: pasar de 3 a 40 multiplica por 13 sin tocar el tráfico |
| `bytes_por_línea` | Tamaño medio de una línea ya formateada | bytes | Sube con cada campo que añades; un cuerpo de petición entero lo dispara |
| `86400` | Segundos de un día | s | Es la constante que convierte el ritmo por segundo en presupuesto diario |
:::

**Tasa de error.** `tasa = errores / total`. Es la métrica que se alerta; el registro es lo que
se mira después para entenderla.

## Ejemplo

**La traza que resuelve el caso.** Una petición `GET /checkout` tarda 240 ms. El árbol de
tramos es:

| Tramo | Padre | Inicio | Duración |
| --- | --- | --- | --- |
| GET /checkout | — | 0 ms | 240 ms |
| autenticar | GET /checkout | 5 ms | 30 ms |
| leer carrito | GET /checkout | 40 ms | 180 ms |
| consulta SQL | leer carrito | 45 ms | 170 ms |
| calcular total | GET /checkout | 225 ms | 10 ms |

Los hijos directos ocupan 220 ms, así que el tiempo propio del padre es de 20 ms: el código de
la petición no es el problema. El hijo más lento es «leer carrito», con 180 ms, y dentro de él
la consulta se lleva 170 ms. La conclusión —hay que mirar esa consulta— sale del árbol, no de
una corazonada. Es exactamente lo que hace un perfilador ([[rendimiento-y-perfilado]]), pero
entre servicios y sin necesidad de reproducir el caso.

**La factura del registro.** Con 200 peticiones por segundo, líneas de 250 bytes y el nivel de
información en 3 líneas por petición, salen 13,0 GB al día. Con el nivel de depuración en 40
líneas por petición, **172,8 GB al día**, unos 5,2 TB al mes. La diferencia entre esas dos
cifras no es un ajuste fino: es la mitad del presupuesto de observabilidad. Y de esas 40 líneas,
en un día normal, probablemente no se lee ninguna.

:::figura
fichero: logging-volumen-y-muestreo
pie: Izquierda, lo que cuesta cada nivel de registro con 200 peticiones por segundo y líneas de 250 bytes: apagado no cuesta nada, `INFO` con 3 líneas por petición son 13,0 GB al día y `DEBUG` con 40 líneas son 172,8 GB, trece veces más por la misma petición. Derecha, la salida que no es apagar sino muestrear: de esas 40 líneas, 2 son de un caso interesante y 38 son detalle rutinario, así que guardar el 100 % de lo interesante y una décima parte del resto baja de 172,8 GB a 25,1 GB al día. El detalle del caso raro sigue estando y el presupuesto vuelve a caber.
fuente: figuras/logging-y-trazas-1.py
:::

## Código

```python verificable
import io
import json
import logging

class FormatoJSON(logging.Formatter):
    """Registro estructurado: mensaje fijo y datos variables en campos aparte."""
    def format(self, record):
        # Formatter se hereda y se sobrescribe format(): cada linea sale como un JSON de una
        # sola linea. Lo que devuelvas aqui es lo que acaba escrito, tal cual.
        return json.dumps({
            "nivel": record.levelname,                  # el nombre del nivel, no el numero
            "logger": record.name,                      # el nombre que se le dio en getLogger
            "mensaje": record.getMessage(),             # interpola el mensaje con sus argumentos
            # getattr con valor por defecto: casi todos los registros no traen "campos", y
            # record.campos directo lanzaria AttributeError; aqui sale un diccionario vacio.
            "campos": getattr(record, "campos", {}),
        }, ensure_ascii=False, sort_keys=True)           # sin escapar tildes y claves ordenadas

flujo = io.StringIO()                          # en produccion, la salida estandar del proceso
manejador = logging.StreamHandler(flujo)       # el "handler" decide DONDE se escribe
manejador.setFormatter(FormatoJSON())          # y el formatter, CON QUE FORMA

logger = logging.getLogger("pagos")            # getLogger devuelve siempre el mismo objeto
logger.setLevel(logging.INFO)                  # por debajo de INFO, el registro ni se crea
logger.propagate = False                       # que no se duplique por el logger raiz
logger.handlers = [manejador]                  # asignar la lista BORRA los handlers heredados

logger.info("cobro aceptado", extra={"campos": {"pedido": 8412, "importe": 19.99}})
logger.warning("reintento de pasarela", extra={"campos": {"pedido": 8412, "intento": 2}})
logger.debug("esta no se escribe: el nivel es INFO")     # el filtro va antes de formatear

registros = [json.loads(linea) for linea in flujo.getvalue().splitlines()]
# getvalue() devuelve el texto acumulado (el StringIO no se vacia al leer); splitlines() lo
# parte por saltos de linea y json.loads() reconstruye cada objeto: el registro se consulta.
print("lineas emitidas:", len(registros))                # -> 2
print("niveles:", [r["nivel"] for r in registros])       # -> ['INFO', 'WARNING']
print("mensajes:", [r["mensaje"] for r in registros])    # -> ['cobro aceptado', 'reintento de pasarela']
print("campos del segundo:", registros[1]["campos"])     # -> {'intento': 2, 'pedido': 8412}
```

:::claves
- El `debug` **no llega a formatearse**: el filtro por nivel se aplica antes, así que esa línea
  no cuesta ni una llamada a `json.dumps`. Por eso el volumen se controla desde `setLevel`.
- `extra={"campos": ...}` **crea atributos nuevos** en el registro y el `Formatter` los lee con
  `getattr(record, "campos", {})`; una clave de `extra` que se llame como un campo del registro
  (`msg`, `levelname`, `name`…) lanza `KeyError` al registrar la línea.
- `logger.handlers = [manejador]` **sustituye la lista entera**: los manejadores que hubiera
  heredados de la configuración por defecto desaparecen. Con `propagate = False`, además, nada
  sube al logger raíz y no hay líneas duplicadas.
- `record.getMessage()` es lo que interpola los argumentos del mensaje; si escribes
  `logger.info(f"... {pedido}")` la interpolación ocurre **antes** de la llamada, aunque el
  nivel esté apagado: pagas el formateo de todas formas.
- `ensure_ascii=False` conserva tildes y eñes en el JSON, y `sort_keys=True` ordena las claves:
  por eso el diccionario impreso del segundo registro sale como `{'intento': 2, 'pedido': 8412}`
  y no en el orden en que lo escribiste.
- Las cifras de volumen son **bytes decimales**: dividir entre `1e9` da GB y entre `1e12` TB, así
  que no van a coincidir con un gestor de ficheros que cuente GiB.
:::

```python verificable
# Arbol de tramos de una peticion: (nombre, id, padre, inicio_ms, duracion_ms)
spans = [
    ("GET /checkout", "a", None, 0, 240),
    ("autenticar", "b", "a", 5, 30),
    ("leer carrito", "c", "a", 40, 180),
    ("consulta SQL", "d", "c", 45, 170),
    ("calcular total", "e", "a", 225, 10),
]

hijos = {}
for nombre, sid, padre, inicio, duracion in spans:
    # Desempaquetado de la tupla en el propio for. setdefault agrupa por NOMBRE del padre:
    # crea la lista vacia la primera vez y luego siempre devuelve la misma.
    hijos.setdefault(padre, []).append((nombre, inicio, duracion))

raiz_nombre, raiz_id, _, _, raiz_duracion = spans[0]
directos = hijos[raiz_id]                    # los que cuelgan de la raiz; aqui no se solapan
ocupado = sum(duracion for _, _, duracion in directos)
# max con key: se queda con la TUPLA entera del tramo mas lento, no con la duracion.
mas_lento = max(directos, key=lambda s: s[2])

print("duracion de la peticion:", raiz_duracion, "ms")      # -> 240 ms
print("tiempo en hijos directos:", ocupado, "ms")           # -> 220 ms
print("tiempo propio del padre:", raiz_duracion - ocupado, "ms")   # -> 20 ms
# mas_lento[0] es el nombre y mas_lento[2] la duracion: el indice sale del orden de la tupla.
print(f"hijo mas lento: {mas_lento[0]} con {mas_lento[2]} ms")      # -> leer carrito con 180 ms
```

```python verificable
# Cuanto cuesta registrar: cada linea se escribe, se transporta, se indexa y se guarda.
rps, bytes_por_linea = 200, 250

def por_dia(lineas_por_peticion):
    # 86400 son los segundos del dia: la formula entera cabe en una linea.
    return rps * lineas_por_peticion * bytes_por_linea * 86400

info = por_dia(3)
debug = por_dia(40)

print(f"con INFO  {info / 1e9:6.1f} GB al dia")     # ->   13.0 GB al dia
print(f"con DEBUG {debug / 1e9:6.1f} GB al dia")    # ->  172.8 GB al dia
print(f"multiplicador {debug / info:.0f} x")        # -> 13 x
print(f"un mes en DEBUG: {debug * 30 / 1e12:.1f} TB")  # -> 5.2 TB
```

## Errores típicos

- **Construir el mensaje con datos dentro.** Un texto distinto por pedido es imposible de
  agrupar y obliga a indexar todo el contenido. Mensaje fijo y campos aparte: eso es el
  registro estructurado, y es lo que permite pasar de «leer líneas» a «consultar datos».
- **Registrar el mismo error en cada capa.** El servicio lanza, el repositorio registra, el
  caso de uso registra, el controlador registra y la pasarela registra: cinco líneas idénticas y
  ninguna con la información que falta. Se registra **una vez**, en el borde que decide qué
  hacer, con la traza de pila completa.
- **Usar `ERROR` para todo.** Si los reintentos que acaban bien se registran como error, la
  tasa de error deja de ser una señal y la alerta se silencia. Reserva `ERROR` para lo que
  requiere intervención.
- **Dejar el nivel de depuración encendido.** Multiplica el volumen por decenas y el coste con
  él, y entierra el aviso que importa entre millones de líneas. Si necesitas detalle en
  producción, actívalo por petición muestreada, no global.
- **No propagar el identificador de correlación.** Un identificador nuevo por servicio no sirve
  para nada: lo que hace falta es uno solo que atraviese HTTP, colas y tareas en segundo plano
  ([[colas-y-mensajeria]]). Sin él, reconstruir un caso entre cinco servicios es manual.
- **Registrar dentro de bucles.** Una línea por fila en un trabajo de diez millones de filas
  escribe más datos que el propio resultado. Se registra el progreso cada cierto número de
  elementos o cada cierto tiempo.
- **Escribir el registro en un fichero del contenedor.** El sistema de ficheros del contenedor
  es efímero y crece hasta llenar el disco. Se escribe a la salida estándar y la plataforma se
  encarga de recogerlo y rotarlo.
- **Poner identificadores en las etiquetas de una métrica.** Un identificador de usuario o una
  URL con parámetros como etiqueta multiplica las series temporales y tumba el sistema de
  métricas. La cardinalidad alta es para los registros y para las trazas; las métricas viven de
  la cardinalidad baja.

## Comprueba que lo sabes

:::quiz
p: Una métrica avisa de que el percentil 99 subió, pero necesitas saber en qué se fue el tiempo de una petición concreta. ¿Qué usas?
o: Un registro con nivel de depuración en todas las peticiones
o: Una traza: el árbol de tramos con la duración de cada uno
o: Otra métrica con más etiquetas
a: 2
e: La métrica dice que algo pasa y la traza dice dónde, porque descompone la duración total en los tramos que la componen y señala el más lento. El registro explica el porqué del caso concreto. Activar depuración en todas las peticiones genera un volumen enorme sin dar la estructura de tiempos.
:::

:::quiz
p: ¿Por qué se dice que el mensaje de una línea de registro debe ser fijo y los datos ir en campos?
o: Porque ocupa menos en disco
o: Porque así el número de mensajes distintos se mantiene bajo y se puede agrupar, contar y filtrar sin expresiones regulares
o: Porque los campos se cifran automáticamente
a: 2
e: Con datos interpolados en el texto, cada línea es única y cualquier análisis exige patrones frágiles. Separando mensaje y campos, el mensaje tiene cardinalidad baja (cientos de valores) y los identificadores viajan en campos indexables. El ahorro de disco es anecdótico al lado de poder consultar.
:::

:::quiz
p: Tu servicio reintenta una llamada y el segundo intento funciona. ¿Qué nivel corresponde?
o: `ERROR`, porque la primera llamada falló
o: `WARNING`, porque fue algo anómalo que se resolvió sin intervención
o: `INFO`, porque el resultado final fue correcto y no hay nada que mirar
a: 2
e: El nivel describe qué debe hacer quien lee. Un reintento que acaba bien merece que se pueda contar y alertar si se dispara, pero no que despierte a nadie: eso es un aviso. Marcarlo como error infla la tasa de error y acaba silenciando las alertas de verdad.
:::

:::truco
Si el registro es estructurado, un panel no necesita código nuevo: se construye con consultas
sobre los campos. Antes de añadir una línea, pregúntate qué consulta vas a escribir con ella.
Si no hay ninguna, probablemente no haga falta registrarla.
:::

:::aviso
Los registros son el sitio por donde más datos personales se escapan: correos, identificadores,
direcciones, cuerpos de petición completos. Seudonimiza antes de registrar y trata el
contenido de los registros como datos sujetos a las mismas reglas que la base de datos
([[privacidad-y-gdpr]]).
:::
