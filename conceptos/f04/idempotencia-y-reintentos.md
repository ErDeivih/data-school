---
id: idempotencia-y-reintentos
titulo: Idempotencia y reintentos
fase: 4
nivel: avanzado
rutas: [de, alg]
prerequisitos: [orquestacion-y-dag, apis-y-peticiones-http]
tags: [pipelines, fiabilidad, reintentos, consistencia]
resumen: Una tarea idempotente se puede repetir sin duplicar ni corromper nada; es lo que convierte un reintento en una red de seguridad en vez de en un problema.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications'", "Reis & Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

Un reintento consiste en volver a ejecutar una tarea que **puede que ya se ejecutara**, y la
idempotencia es la propiedad que hace que esa segunda ejecución deje el sistema exactamente
igual que la primera.

## La idea

Estás pagando en una tienda con tarjeta. El datáfono dice «error de comunicación» y el cajero
vuelve a pasarla. Si el sistema del banco no es idempotente, pagas dos veces. El cajero no
tiene forma de saber si el primer intento llegó a aplicarse, y esa duda es exactamente el
problema que resuelve este concepto.

En un pipeline pasa lo mismo. Un timeout, un 502 de la API de origen, un worker que muere a
mitad del `INSERT`: en todos esos casos el orquestador (ver [[orquestacion-y-dag]]) sólo sabe
que **no recibió confirmación**. No puede distinguir «no se hizo» de «se hizo y no me
enteré». Y la única respuesta segura es reintentar, porque no reintentar deja el dato
incompleto para siempre. Reintentar sin idempotencia, en cambio, duplica.

La diferencia entre una operación idempotente y una que no lo es se ve en una línea de SQL:

- `UPDATE saldos SET importe = importe + 100` **no** es idempotente: cada ejecución suma cien.
- `UPDATE saldos SET importe = 350` **sí** lo es: da igual ejecutarla una, dos o cinco veces.

Los cuatro patrones que se usan en la práctica:

1. **Reemplazo de partición.** La tarea escribe la partición entera del día D y, si ya existía,
   la tira antes (`INSERT OVERWRITE`, `CREATE OR REPLACE TABLE`, o escribir a una ruta temporal
   y renombrar). Ejecutar dos veces deja el mismo contenido. Es el patrón de referencia en
   [[batch-vs-streaming|procesamiento por lotes]].
2. **Upsert o MERGE por clave natural.** Si la fila ya existe con esa clave se actualiza; si no,
   se inserta. La clave (`pedido_id`, `evento_id`) tiene que ser única y estable.
3. **Clave de idempotencia explícita.** El productor genera un identificador por operación y lo
   manda con ella; el destino guarda los identificadores ya vistos y rechaza los repetidos
   (`INSERT ... ON CONFLICT DO NOTHING`, o una clave primaria cuya violación se ignora).
4. **Diseño acumulativo evitado.** Guardar el estado en lugar de sumar deltas:
   `SET estado = 'enviado'` en vez de `SET contador = contador + 1`.

La garantía que se persigue no es «exactamente una vez» en el transporte —eso es imposible en
un sistema distribuido, porque el acuse de recibo también se puede perder—, sino
**efectivamente una vez**: entrega al menos una vez más un destino idempotente. Si el mismo
mensaje puede llegar dos veces y aplicarlo dos veces no cambia nada, el resultado es el de una
sola entrega.

:::trampa
«Mi tarea sólo lee, así que reintentar es gratis». Casi nunca es cierto: la tarea escribe en un
destino, manda un correo, abre un ticket, incrementa un contador o publica en una cola. Antes de
activar reintentos automáticos, haz la lista de efectos secundarios y comprueba uno por uno si
repetirlo molesta.
:::

## Definición formal

En matemáticas, una función `f` es idempotente si aplicarla dos veces da lo mismo que aplicarla
una:

:::formula
f(f(x)) = f(x)
:::

Trasladado a un pipeline, el estado del destino después de `n` ejecuciones de la tarea `T` sobre
la misma entrada `x` no depende de `n`:

:::formula
T(T(…T(x))) = T(x)   para todo n ≥ 1
:::

Símbolos:

- `x` — la entrada de la tarea: la partición de origen, el fichero, el lote de eventos.
- `T` — la transformación completa, **incluida la escritura en el destino**.
- `n` — el número de veces que el orquestador ha lanzado la tarea (1, 2, 3…).
- `f(f(x)) = f(x)` — la definición matemática; `SET importe = 350` la cumple y
  `importe = importe + 100` no.

Hay tres condiciones que se tienen que cumplir a la vez para poder afirmar que una tarea es
idempotente:

1. **Clave estable.** Existe un identificador de negocio —no un autoincremental, no un
   `now()`— que identifica la unidad de trabajo. Sin él, dos ejecuciones producen dos filas
   distintas y nada las puede reconocer como la misma.
2. **Resultado determinista.** La misma entrada produce la misma salida. Si metes `now()` o un
   número aleatorio en una columna del resultado, dos ejecuciones se diferencian aunque no
   dupliquen.
3. **Atomicidad de la unidad.** La escritura de la partición es una transacción o un renombrado
   atómico. Si el proceso muere a mitad, el destino queda a medias, y el reintento tiene que
   poder rehacerlo desde cero.

:::nota
Idempotencia y determinismo son cosas distintas. Un `SET contador = contador + 1` es
determinista y no idempotente. Un `INSERT ... ON CONFLICT (clave) DO NOTHING` que grabe `now()`
es idempotente y no determinista: la segunda ejecución no cambia nada, pero el valor que quedó
depende de cuándo corrió la primera. Y un `SET actualizado_en = now()` no es ni lo uno ni lo otro:
no acumula, pero el estado después de dos ejecuciones no es el mismo que después de una, así que
incumple la definición de idempotencia. Lo sería si el valor saliera de la entrada —la fecha
lógica del intervalo— en lugar del reloj. Para reproducir un resultado necesitas las dos
propiedades; para sobrevivir a un reintento basta la idempotencia.
:::

## Ejemplo

La tabla de pedidos tiene dos pedidos reales: `P1` con importe 100 y `P2` con importe 250. El
total correcto es 350. La tarea se lanza tres veces porque un timeout hizo que el orquestador
reintentara dos veces.

| Estrategia | Filas tras 3 ejecuciones | Suma de importes | ¿Correcto? |
| --- | --- | --- | --- |
| Append puro | 6 | 1.050 | No |
| MERGE por pedido_id | 2 | 350 | Sí |
| ON CONFLICT DO NOTHING | 2 | 350 | Sí |

El append puro ha triplicado la cifra y ningún test de esquema lo detecta: los tipos son
correctos, no hay nulos y la clave primaria —si no existe— no se queja. El error sólo se ve
comparando el total con el origen.

De ahí sale la segunda mitad de la práctica: **reconciliación**. Después de un reintento,
comprobar el invariante (`filas_destino = filas_origen`, `suma_destino = suma_origen`) y hacer
fallar la tarea si no cuadra. Un pipeline que reintenta sin reconciliar cambia un problema de
disponibilidad por uno de corrección, que es peor porque no hace ruido.

## Código

```python verificable
import pandas as pd

# Dos pedidos reales; el orquestador lanza la tarea 3 veces por un timeout.
pedidos = pd.DataFrame({"pedido_id": ["P1", "P2"], "importe": [100, 250]})

# Append puro: cada reintento vuelve a insertar las mismas filas.
append = pd.concat([pedidos] * 3, ignore_index=True)
print(f"append  filas {len(append)}  suma {append['importe'].sum()}")   # -> append  filas 6  suma 1050

# Upsert por clave natural: el destino indexa por pedido_id y sobreescribe.
destino = {}
for _ in range(3):
    for fila in pedidos.itertuples(index=False):
        destino[fila.pedido_id] = fila.importe
print(f"upsert  filas {len(destino)}  suma {sum(destino.values())}")    # -> upsert  filas 2  suma 350
```

```sql verificable
CREATE TABLE destino (pedido_id VARCHAR PRIMARY KEY, importe INTEGER);

-- Primer intento
INSERT INTO destino VALUES ('P1', 100), ('P2', 250);
-- El orquestador no recibe respuesta y reintenta: mismas filas, misma clave
INSERT INTO destino VALUES ('P1', 100), ('P2', 250) ON CONFLICT (pedido_id) DO NOTHING;
-- Y un tercer intento
INSERT INTO destino VALUES ('P1', 100), ('P2', 250) ON CONFLICT (pedido_id) DO NOTHING;

SELECT count(*) AS filas, sum(importe) AS suma FROM destino;
```

```text
filas | suma
2 | 350
```

## Errores típicos

- **Generar la clave de idempotencia en el consumidor.** Si el UUID se crea dentro de la tarea,
  cada reintento trae una clave nueva y el destino no puede reconocer el duplicado. La clave la
  genera **el productor**, una sola vez, cuando el evento nace, y viaja con él.
- **Reintentar sin límite y sin espera creciente.** Cinco reintentos inmediatos contra un
  servicio saturado lo hunden más y consumen la cuota. Usa espera exponencial con algo de azar,
  un tope de intentos y una distinción explícita entre errores que merecen reintento (timeout,
  503, 429) y errores que no (400, 401, violación de esquema).
- **Confundir el reintento de la tarea con el del fragmento.** Si la tarea escribe 40
  particiones y falla en la 31, al reintentar tiene que rehacerla desde la 31 o ser idempotente
  en las 40. Lo segundo es más simple y no depende de que el orquestador recuerde el progreso.
- **Usar un autoincremental como clave natural.** El `id` de la tabla destino es distinto en
  cada ejecución; la clave natural es `pedido_id` o un hash del contenido del evento.
- **Suponer que el commit y el acuse de recibo son lo mismo.** El worker puede escribir en la
  base, morir antes de responder y ser reintentado. Esa ventana existe siempre; lo único que la
  hace inofensiva es que la escritura sea idempotente.
- **Deduplicar por una ventana de tiempo demasiado corta.** Un `MERGE` sobre los últimos cinco
  minutos no ve el duplicado que llega seis minutos tarde por un reintento de red. En streaming,
  la deduplicación se apoya en la marca de agua y en el identificador, no en el reloj de pared.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas operaciones NO es idempotente?
o: `INSERT INTO t VALUES (1) ON CONFLICT (id) DO NOTHING`
o: `UPDATE saldos SET importe = importe + 100 WHERE id = 7`
o: `CREATE OR REPLACE TABLE resumen AS SELECT ... FROM origen WHERE fecha = '2024-03-01'`
a: 2
e: Sumar cien es acumulativo: cada ejecución cambia el resultado, así que dos ejecuciones no dan lo mismo que una. Las otras dos dejan el destino igual se ejecuten una o cinco veces: la primera porque rechaza el duplicado y la tercera porque reconstruye la partición entera.
:::

:::quiz
p: ¿Por qué se dice que «al menos una vez más un destino idempotente» equivale en la práctica a «exactamente una vez»?
o: Porque el orquestador garantiza que sólo se ejecuta una vez
o: Porque si un mensaje se aplica dos veces el estado final es el mismo que aplicándolo una, así que el duplicado no tiene efecto
o: Porque los duplicados se borran automáticamente en el almacén
a: 2
e: El transporte puede repetir porque el acuse de recibo se pierde; no se puede evitar. Lo que sí se puede garantizar es que repetir no cambie el estado. Con esa propiedad, el efecto observable es el de una sola aplicación, aunque por debajo haya dos. Nadie borra nada automáticamente: es el diseño de la escritura el que lo hace inocuo.
:::

:::practica
enunciado: Una tarea carga cada noche el fichero de pedidos del día en la tabla `fact_pedidos` con un `INSERT`. El orquestador tiene 3 reintentos. El lunes el job falla a los 4 minutos con un timeout y se reintenta dos veces. ¿Qué encuentra el equipo el martes en la tabla y cómo lo arreglas?
pista: Piensa en qué pasa con las filas que ya se habían insertado antes del timeout.
solucion: El martes hay tres copias del mismo día de pedidos: el primer intento insertó la mayor parte antes de morir, y los dos reintentos volvieron a insertar todo. La cifra de ventas del lunes está triplicada y ningún test de esquema lo detecta. Se arregla cambiando el patrón: escribir cada noche en una tabla temporal y reemplazar la partición del día de forma atómica (INSERT OVERWRITE o CREATE OR REPLACE), o hacer MERGE por pedido_id si la tabla tiene que acumular. Después, borrar los duplicados del lunes con una deduplicación por pedido_id y añadir un test de reconciliación que compare filas y suma contra el origen.
:::
