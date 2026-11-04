---
id: cache-y-redis
titulo: Caché y Redis
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [apis-rest, gestion-de-memoria]
tags: [rendimiento, memoria, invalidacion, latencia]
resumen: Guardar el resultado caro para no repetirlo: qué cachear, cuándo invalidar y por qué el TTL es solo una parte del problema.
fuentes: ["Redis, 'Documentación oficial'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 5"]
---

## En una frase

Una caché es una copia de un dato caro de calcular, guardada cerca para responder rápido la
próxima vez; el problema interesante no es guardarla, es saber cuándo deja de ser válida.

## La idea

Un panel de ventas pide cada cinco segundos el mismo agregado: sumar 40 millones de filas de
pedidos para obtener el total del mes. La consulta tarda dos segundos y el número cambia, como
mucho, una vez por hora. Estás pagando dos segundos cada cinco segundos para recalcular algo
que casi nunca cambia: eso es lo que arregla una caché.

Guardas el resultado con una clave (`ventas:mes:2026-01`) y un tiempo de vida de 60 segundos.
La primera petición paga los dos segundos; las once siguientes del minuto responden en un
milisegundo. La base de datos respira y el panel va rápido.

Pero aparece el problema de verdad: **la invalidación**. Alguien registra una venta nueva y el
total cacheado miente durante hasta 60 segundos. Ese es el compromiso central: cuanto más
tiempo vive la entrada, más ahorras y más tiempo mientes. Hay tres estrategias y no son
excluyentes:

- **Tiempo de vida (TTL).** La entrada caduca sola. Es la red de seguridad, no la estrategia:
  garantiza que ningún dato viejo se quede para siempre.
- **Invalidación explícita.** Cuando el dato cambia, se borra la clave. Es lo correcto, y es
  fácil de olvidar en el sitio menos pensado: la venta se registra por tres caminos y solo uno
  borra la caché.
- **Clave versionada.** La clave incluye algo que cambia con el dato (`ventas:mes:2026-01:v7`).
  No hay que borrar nada: la clave vieja deja de consultarse y caduca por TTL. Cuesta más
  memoria durante un rato.

Y hay dos peligros clásicos que se cobran caros en producción. El primero es la **estampida**
(*thundering herd*): una clave muy consultada caduca y, en ese instante, cien procesos van a la
base de datos a la vez a recalcular lo mismo. El segundo es **cachear lo que no se repite**:
guardar resultados distintos por usuario cuando cada uno consulta una vez solo llena memoria y
no ahorra nada.

## Definición formal

**Patrón caché-aside** (el más común, y el que conviene saber de memoria):

1. Busca la clave en la caché. Si está, devuélvela: **acierto**.
2. Si no está, calcula el valor con la fuente lenta: **fallo**.
3. Guarda el valor con un TTL y devuélvelo.

Las métricas que se vigilan son tres:

:::formula
tasa de aciertos = aciertos / (aciertos + fallos)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `tasa de aciertos` | Proporción de lecturas que se resuelven sin tocar la fuente lenta | de 0 a 1 (se lee en %) | Por encima de 0,8 en una caché de lectura caliente se considera sana; por debajo, o el TTL es corto o el conjunto de claves no cabe |
| `aciertos` | Lecturas que encuentran la clave en la caché y vuelven en un milisegundo | peticiones | Sube la tasa y no toca la fuente; cada acierto sigue costando un viaje de red, que es lo que hay que vigilar si tarda 20 ms |
| `fallos` | Lecturas que no la encuentran y van a la fuente lenta | peticiones | Es el término que manda en la latencia media: cada fallo cuesta la consulta entera (200 ms en el ejemplo) |
| `aciertos + fallos` | Total de lecturas del periodo que se mide | peticiones | Con los mismos aciertos, más fallos bajan la tasa; la métrica solo es comparable entre ventanas de tamaño parecido |
| `TTL` (no está en la fórmula) | Segundos que vive cada entrada antes de caducar | s | Sube la tasa (menos fallos) y sube el tiempo que puedes estar sirviendo un dato viejo: es el compromiso central de la página |
:::

- **Tasa de aciertos:** qué proporción de lecturas se resuelven sin tocar la fuente. Por debajo
  del 80 % en una caché de lectura caliente, algo va mal: o el TTL es demasiado corto, o el
  conjunto de claves es enorme respecto a la memoria disponible.
- **Latencia de acierto y de fallo:** el acierto debe estar en el orden de un milisegundo. Si
  el acierto tarda 20 ms, el viaje de red se está comiendo el beneficio.
- **Tasa de expulsión:** cuántas entradas se tiran por falta de memoria antes de caducar. Si es
  alta, la caché es más pequeña que el conjunto de trabajo y estás expulsando datos que se
  volverán a pedir.

**Políticas de expulsión** cuando la memoria se llena: **LRU** tira lo usado hace más tiempo,
**LFU** tira lo usado menos veces, **aleatoria** tira cualquiera. Redis, además, permite poner
un TTL distinto por clave y expulsar primero las que tienen TTL próximo.

**Estructuras de datos útiles en Redis**, más allá de «clave que guarda un texto»:

- **String con TTL:** el caso básico, un contador o un fragmento de HTML.
- **Hash:** un objeto con campos (`usuario:7` con nombre, plan y última visita). Permite leer y
  escribir un campo sin traer todo el objeto.
- **Sorted set:** elementos ordenados por una puntuación. Es la base de las listas de
  clasificación y de las colas de prioridad.
- **Lista:** cola FIFO sencilla con inserción por un extremo y lectura por el otro.
- **Conjunto:** pertenencia y operaciones de unión e intersección (usuarios únicos por día).
- **Contador con expiración:** `INCR` más `EXPIRE` resuelve un límite de peticiones por minuto
  en dos comandos.

Dos detalles de operación que importan: Redis guarda todo en memoria, así que la memoria es el
límite duro y hay que decidir qué política de expulsión aplicar antes de llenarla; y las
claves deben nombrarse con una convención (`recurso:id:version`) porque en producción se
inspeccionan a mano y una clave sin estructura es un jeroglífico.

## Ejemplo

Supón un endpoint que lee el perfil de un usuario. La consulta a la base de datos tarda 200 ms
y el perfil cambia como mucho una vez al día.

- Sin caché: 1.000 peticiones por minuto son 1.000 × 200 ms = 200 segundos de trabajo de base
  de datos por minuto. Con una sola conexión, imposible.
- Con TTL de 60 segundos y 1.000 usuarios distintos: como mucho 1.000 fallos por minuto, uno por
  usuario, y el resto aciertos a 1 ms. El trabajo baja a 200 segundos por minuto... repartido
  entre usuarios, pero con la misma clave pedida diez veces, nueve se sirven de memoria.
- Con invalidación explícita al guardar: cuando el usuario cambia su perfil, se borra
  `perfil:7`. Cero mentiras y ningún fallo evitable.

Y la estampida: si `perfil:7` es la clave del usuario más activo y caduca en el momento de
máxima carga, los 50 procesos que atienden peticiones van a la vez a la base de datos. La
solución habitual es que solo uno recalcule y los demás esperen un poco, o servir el valor
caducado durante unos milisegundos mientras se refresca por detrás.

## Código

```python verificable
from collections import OrderedDict

CAPACIDAD = 3
cache = OrderedDict()                # hace falta el orden: hay que saber cual es el mas antiguo
aciertos = fallos = 0                # asignacion encadenada: los dos nombres empiezan en cero

def obtener(clave):
    global aciertos, fallos          # sin global, += crearia variables locales y no subiria el total
    if clave in cache:
        cache.move_to_end(clave)          # LRU: lo usado va al final
        aciertos += 1
        return cache[clave]
    fallos += 1
    valor = f"valor-de-{clave}"      # simula el calculo caro: aqui iria la consulta a la base
    cache[clave] = valor
    if len(cache) > CAPACIDAD:       # el desalojo se comprueba DESPUES de insertar
        cache.popitem(last=False)         # se desaloja el menos usado recientemente
    return valor

for clave in ["a", "b", "c", "a", "d", "a", "b"]:
    obtener(clave)
    print(f"pido {clave} -> cache {list(cache)}")   # list() muestra el orden: del mas viejo al mas nuevo

print("aciertos", aciertos, "fallos", fallos)
print("tasa de acierto", round(aciertos / (aciertos + fallos), 2))   # la division con / da float
```

:::claves
- `OrderedDict` y no un `dict`: aquí hacen falta `move_to_end` y `popitem(last=False)`. Un `dict` normal conserva el orden de inserción desde Python 3.7, pero no tiene esos dos métodos y el `AttributeError` salta en la primera llamada.
- `cache.popitem(last=False)` devuelve y **borra** la pareja más antigua. Con el valor por defecto (`last=True`) tiraría la última, que es justo la que acabas de meter: el argumento es lo único que separa una LRU de un absurdo, y el código sigue funcionando igual (sin fallar) si lo cambias.
- El desalojo se comprueba con `if len(cache) > CAPACIDAD` **después** de insertar, así que la caché llega a tener 4 entradas un instante y luego baja a 3. La secuencia `a, b, c, a, d, a, b` con capacidad 3 da **2 aciertos y 5 fallos**: la `a` repetida acierta, la `d` desaloja la `b` y la última `b` vuelve a fallar. Todo eso sin que el resultado diga nada de si la caché está bien dimensionada.
- Los contadores viven **fuera** de la función y por eso hace falta `global`: sin él, `aciertos += 1` crearía una variable local y el `print` final seguiría diciendo 0. Python no avisa, lanza `UnboundLocalError` en la primera suma.
- La clave del diccionario *es* la clave de caché. Si el valor dependiera del usuario —el perfil de Ana y el de Luis— y se guardara con la clave `perfil`, el segundo recibiría los datos del primero. Por eso las claves llevan ámbito: `perfil:7`, `ventas:mes:2026-01`.
- `round(aciertos / (aciertos + fallos), 2)` da la tasa con dos decimales, pero con **muy pocas** peticiones es ruido: en el ejemplo son 7 lecturas. La métrica se mira por ventanas de miles de lecturas, no por ejecución.
:::

:::figura
fichero: cache-aciertos-y-coste
pie: Izquierda, la tasa de aciertos de la misma caché LRU sobre 20.000 peticiones a un catálogo de 2.000 claves, cambiando solo cómo se reparte la demanda. Con la demanda concentrada (zipf 1,8) bastan 10 claves en memoria —el 0,5 % del catálogo— para pasar del 84 % de aciertos; con la demanda plana (zipf 1,1) hacen falta 500 claves, el 25 % del catálogo, para llegar al 82 %. El código es el mismo y la memoria es diez veces mayor: lo que decide es si unas pocas claves se llevan casi todas las visitas o si el tráfico se reparte. Derecha, por qué una caché puede empeorar el sistema: la latencia media es la mezcla de aciertos y fallos, así que con un 80 % de aciertos la media es 41 ms, no 1 ms, y el 20 % que falla manda. Antes de añadir caché hay que estimar la tasa de aciertos que se va a conseguir, no suponerla.
fuente: figuras/cache-y-redis-1.py
:::

```python verificable
# Tiempo virtual: el reloj no aporta nada al ejemplo y asi el resultado es exacto.
reloj = {"t": 0.0}                  # un dict de un solo valor: asi se puede cambiar desde dentro
cache = {}
consultas = 0

def obtener_con_cache(clave, ttl=1.0):
    """Patron cache-aside: mira la cache, y solo si falla va al almacen."""
    global consultas
    entrada = cache.get(clave)      # .get devuelve None si no esta: no lanza KeyError
    if entrada and reloj["t"] - entrada[1] < ttl:
        # entrada[1] es la marca de tiempo; sin ella no se puede saber si ha caducado
        return entrada[0], "acierto"
    reloj["t"] += 0.2                       # la consulta a la base de datos tarda 200 ms
    consultas += 1
    cache[clave] = (f"fila-{clave}", reloj["t"])     # se guarda el valor CON su marca de tiempo
    return cache[clave][0], "fallo"                  # indice 0 = valor; el 1 es la marca

for clave in ["u1", "u1", "u1"]:
    _, estado = obtener_con_cache(clave)             # el guion bajo descarta el valor
    print(f"t={reloj['t']:.1f}s {clave} -> {estado}")

reloj["t"] = 2.0                            # pasa el tiempo de golpe: u1 ya ha caducado
print("tras el TTL:", obtener_con_cache("u1")[1])        # -> fallo
print("consultas al almacen:", consultas, "de 4 lecturas")
print("tiempo esperando al almacen:", round(0.2 * consultas, 1), "s")   # 0,2 s por consulta
```

```sql verificable
-- Que se cachea y que no se puede cachear: agregados frente a filas que cambian.
CREATE TABLE pedidos (id INTEGER, cliente INTEGER, importe DOUBLE, estado VARCHAR);
-- los tipos son una declaracion: SQLite guarda el valor que le llegue en cada columna

INSERT INTO pedidos VALUES
  (1, 7, 120.50, 'pagado'),
  (2, 7,  80.00, 'pagado'),
  (3, 9,  45.25, 'pendiente'),
  (4, 9, 200.00, 'pagado');

-- Clave de cache: el total pagado por cliente. Cambia poco y se repite mucho.
SELECT cliente, SUM(importe) AS total_pagado
FROM pedidos
WHERE estado = 'pagado'         -- el filtro va antes de agrupar: solo suman los pagados
GROUP BY cliente                -- una fila de salida por cliente
ORDER BY cliente;               -- sin un orden fijo, dos peticiones pueden devolver distinto orden
```

```python ilustrativo
import json
import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
# decode_responses=True devuelve str; sin el, cada get trae bytes y hay que decodificar a mano

def leer_perfil(usuario_id: int) -> dict:
    clave = f"perfil:{usuario_id}"                    # convencion: recurso:id
    guardado = r.get(clave)                           # None si no esta o si ya ha caducado
    if guardado is not None:                          # is not None: un valor vacio es acierto valido
        return json.loads(guardado)                   # acierto: un viaje de red y ya

    perfil = consultar_base_de_datos(usuario_id)      # fallo: la parte cara
    r.set(clave, json.dumps(perfil), ex=300, nx=False)  # TTL como red de seguridad
    # ex son los segundos de vida; con nx=True solo escribiria si la clave no existiera
    return perfil

def guardar_perfil(usuario_id: int, cambios: dict) -> None:
    escribir_en_base_de_datos(usuario_id, cambios)
    r.delete(f"perfil:{usuario_id}")                  # invalidacion explicita: sin mentiras

# Otras estructuras que ahorran codigo y viajes.
r.hset("coche:7", mapping={"marca": "A", "km": 32000})       # leer un campo sin traer el objeto
r.zadd("ranking:2026-01", {"ana": 1200, "luis": 980})        # lista ordenada por puntuacion
r.expire("ranking:2026-01", 60 * 60 * 24 * 30)              # y que caduque sola: 30 dias en segundos

# Limite de peticiones por minuto sin tablas ni bloqueos.
def permitido(ip: str, maximo: int = 100) -> bool:
    clave = f"limite:{ip}:{int(time.time() // 60)}"   # la clave lleva el minuto: la ventana rota sola
    usadas = r.incr(clave)                            # INCR crea la clave en 1 y devuelve el valor nuevo
    if usadas == 1:
        r.expire(clave, 60)                           # solo la primera peticion de la ventana pone el TTL
    return usadas <= maximo                           # la 101 devuelve False; el 429 lo pone quien llama
```

## Errores típicos

- **Confiar solo en el TTL para la coherencia.** Un TTL de una hora significa que durante una
  hora puedes servir un dato caducado. El TTL es la red de seguridad; la coherencia se consigue
  borrando la clave cuando el dato cambia.
- **Olvidar la invalidación en uno de los caminos de escritura.** La caché se borra en el panel
  de administración pero no en la importación nocturna, y a la mañana siguiente el informa
  miente. Lo robusto es invalidar en la capa que escribe el dato, no en el controlador HTTP.
- **Cachear datos por usuario sin límite.** Claves como `panel:usuario:12345` con 500.000
  usuarios llenan la memoria de cosas que se consultan una vez. Antes de cachear, estima el
  conjunto de claves y su frecuencia.
- **No protegerse de la estampida.** Una clave caliente que caduca y cien procesos que recalculan
  a la vez convierten la caché en amplificador de carga. Un bloqueo corto o servir el valor
  viejo mientras se refresca lo evita.
- **Guardar objetos enormes.** Una lista de un millón de elementos en una sola clave bloquea el
  servidor mientras se serializa y hace que cada lectura copie megabytes. Divide o página.
- **Usar Redis como base de datos principal sin decidir la durabilidad.** Redis es rápido porque
  vive en memoria; si no configuras persistencia y el proceso se reinicia, los datos que
  guardaste «para siempre» desaparecen. Para datos que no se pueden perder, la fuente de verdad
  es otra.
- **Cachear errores y respuestas vacías.** Un fallo momentáneo guardado con TTL de cinco minutos
  convierte un hipo en una caída de cinco minutos. No cacheados los errores, o cachea con TTL
  muy corto.

## Comprueba que lo sabes

:::quiz
p: Un panel muestra el total de ventas del mes y solo se actualiza cuando alguien registra una venta. ¿Qué combinación es correcta?
o: TTL de 24 horas, sin más
o: Invalidar la clave al registrar la venta y dejar un TTL razonable como red de seguridad
o: No cachear nunca, porque los agregados no se pueden cachear
a: 2
e: La invalidación explícita es lo que evita servir datos viejos, y el TTL garantiza que un fallo al borrar no deje el dato podrido para siempre. Un TTL largo sin invalidación miente hasta 24 horas; no cachear tira el ahorro, que es precisamente lo que buscas.
:::

:::quiz
p: ¿Qué mide la tasa de aciertos de una caché?
o: La proporción de lecturas que se resuelven sin consultar la fuente lenta
o: La proporción de entradas que caducan antes de ser expulsadas
o: El porcentaje de memoria libre del servidor de caché
a: 1
e: Aciertos entre aciertos más fallos: cuántas lecturas se ahorran el viaje a la fuente. Las entradas expulsadas antes de caducar miden otra cosa, la presión de memoria, y son la señal de que la caché es pequeña para el conjunto de trabajo.
:::

:::quiz
p: ¿Por qué una caché puede empeorar el sistema en lugar de mejorarlo?
o: Porque añade un viaje de red, y con una tasa de aciertos baja el coste total supera al de ir directo a la fuente
o: Porque ocupa memoria que necesita la base de datos
o: Porque las claves siempre crecen más rápido que los datos
a: 1
e: El acierto cuesta un viaje de red y hay que compararlo con el coste de la fuente. Si el 90 % de las consultas son de claves distintas que no se repiten, el 10 % de aciertos no compensa y la caché solo añade latencia y un sistema más que mantener. Además, sin protección, la estampida puede multiplicar la carga sobre la fuente.
:::

:::trampa
El `DEL` de invalidación casi nunca es el problema; el problema es que hay tres caminos que
escriben ese dato y solo uno borra la caché. Antes de añadir caché, enumera **todas** las rutas
de escritura; si no puedes, usa claves versionadas que cambian con el dato en lugar de borrar.
:::

:::aviso
Redis es un servidor compartido: una consulta lenta sobre una clave enorme bloquea a todos los
clientes, porque el modelo de ejecución es de un solo hilo para los comandos. Evita comandos
sobre colecciones gigantes y usa variantes incrementales o paginación.
:::
