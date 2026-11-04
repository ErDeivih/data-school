---
id: flink-y-procesamiento-de-eventos
titulo: Flink y procesamiento de eventos
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [streaming-tiempo-real, ventanas-y-watermarks]
tags: [flink, streaming, estado]
resumen: Un motor que procesa evento a evento con estado y watermarks, en lugar de micro-lotes: qué gana, qué complica y cuándo no compensa.
fuentes: ["Apache Flink (2024), 'Documentation: Time and Watermarks'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11"]
---

## En una frase

Flink trata cada evento como un dato que ocurre en su propio instante: mantiene estado por clave,
avanza un reloj lógico con los propios eventos y guarda puntos de recuperación para poder
reanudar sin perder ni duplicar.

## La idea

Spark Structured Streaming procesa micro-lotes: agrupa unos segundos de eventos y los trata como
una tabla pequeña. Funciona muy bien y es fácil de razonar. Flink hace otra cosa: cada evento entra
en un operador que puede recordar cosas —un contador, una media, el último valor— y ese estado
vive en el motor, no en tu base de datos.

Recordar cosas es lo que permite detectar patrones que un lote no ve: dos eventos del mismo
usuario separados por 90 segundos, un pico que empieza y no termina, una sesión que se cierra por
inactividad. También es lo que complica la operación: hay que decidir cuánto estado se guarda,
dónde vive y qué pasa si el proceso muere.

La tercera pieza es el **tiempo de evento**. Los eventos llegan desordenados y tarde; el motor
avanza un reloj lógico —el watermark— que dice «ya no espero nada anterior a este instante». Lo
que llega después es tarde, y tú decides si se descarta, se actualiza o se manda a una cola
aparte.

:::aviso
Un watermark no es una garantía de que no lleguen eventos antiguos: es una apuesta con retraso
configurable. Cuanto más tolerante, más esperas y más estado acumulas. Cuanto más agresivo, más
eventos tardíos descartas. No hay configuración que elimine la decisión.
:::

## Definición formal

El modelo se apoya en tres conceptos que se configuran juntos:

:::formula
watermark(t) = max(event_time) − retraso        ventana [inicio, fin) se cierra cuando watermark ≥ fin
:::

- **event_time** — el instante en que ocurrió el hecho, dentro del propio evento.
- **processing_time** — el reloj de la máquina que procesa; no sirve para reproducir.
- **retraso (allowed lateness)** — cuánto se espera antes de dar una ventana por cerrada.
- **estado** — lo que el operador recuerda entre eventos, indexado por clave.
- **checkpoint** — copia periódica del estado para reanudar; el **savepoint** es una copia manual
  con nombre, para migrar o cambiar el código.
- **exactly-once** — se consigue con checkpoints y un sink transaccional o idempotente; el motor
  no lo regala por sí solo.

## Ejemplo

Siete eventos con su marca de tiempo, llegando en este orden:
`(1,100) (2,103) (3,105) (4,101) (5,106) (6,104) (7,102)`. Retraso configurado: 2.

Tras el evento 5, el máximo es 106 y el watermark vale 104. Los eventos 4 (101) y 7 (102) llegan
por debajo de esa marca: son tardíos. Los otros cinco se procesan en su ventana. El resultado es
5 procesados y 2 tardíos, que es exactamente la cuenta que hay que vigilar en producción.

## Código

```python verificable
# Watermark con retraso fijo: cuántos eventos llegan tarde y cuáles
eventos = [(1, 100), (2, 103), (3, 105), (4, 101), (5, 106), (6, 104), (7, 102)]
retraso = 2

maximo = 0
procesados = 0
tardios = []
for i, t in eventos:
    maximo = max(maximo, t)
    marca = maximo - retraso
    if t < marca:
        tardios.append(i)
    else:
        procesados += 1

print(f"procesados {procesados}")        # -> procesados 5
print(f"tardios {len(tardios)}")          # -> tardios 2
print(f"ids tardios {tardios}")           # -> ids tardios [4, 7]
print(f"marca final {maximo - retraso}")  # -> marca final 104
```

La comparación es `< marca` y no `<=`: un evento exactamente en la marca todavía se puede procesar.
Cambiar el signo mueve la frontera un evento y, en un flujo denso, cambia el recuento de tardíos en
miles.

:::claves
- `maximo` recuerda el mayor instante visto, no el último. Si usaras el último, un evento antiguo
  retrasaría el watermark y el motor esperaría para siempre.
- `maximo - retraso` es el watermark. El retraso es una decisión de negocio: cuánto estás dispuesto
  a esperar a cambio de procesar mejor.
- `t < marca` significa estrictamente anterior; `t == marca` aún entra. Es la misma convención que
  usa Flink para cerrar una ventana cuando `watermark >= fin`.
- `tardios.append(i)` guarda el identificador, no la marca: en producción lo que se manda a la cola
  de tardíos es el evento completo, para reprocesarlo si hace falta.
- El bucle no ordena nada: el orden de llegada es el del flujo real. Ordenar antes de procesar
  convertiría un problema de streaming en uno de lote y cambiaría el resultado.
:::

## Errores típicos

- **Usar el reloj de proceso en vez del de evento.** El resultado depende de cuándo se ejecutó el
  proceso, así que no se puede reproducir ni comparar entre ejecuciones.
- **Confiar en que el watermark garantiza orden.** No lo garantiza: solo acota la espera. Los
  eventos tardíos existen y hay que decidir qué hacer con ellos.
- **No acotar el estado.** Una clave por usuario con histórico completo crece hasta tumbar el
  proceso. Hay que poner caducidad (TTL) y medir el tamaño.
- **Creer que Flink da exactly-once por usarlo.** Se consigue con checkpoint y un sink que lo
  soporte; un `INSERT` a una tabla sin clave única sigue duplicando.
- **Comparar con Spark por velocidad sin mirar la latencia.** Flink gana en latencia por evento;
  Spark gana en simplicidad operativa y en reutilizar el mismo motor que el lote.
- **No probar la recuperación.** Un checkpoint que nunca se ha restaurado no está probado. Se
  ensaya: matar el proceso, reanudar desde el savepoint y comprobar el recuento.

:::practica
enunciado: Con los mismos siete eventos y retraso 2, ¿qué pasa si el evento 7 llega con marca 104 en vez de 102? ¿Y si el retraso fuera 0?
pista: El watermark depende del máximo y del retraso, no del orden.
solucion: Con 104, el máximo sigue siendo 106 y la marca 104: el evento 7 cae justo en la marca y se procesa, así que solo el 4 es tardío (1 tardío). Con retraso 0, la marca es el propio máximo y cualquier evento que no sea el máximo es tardío: solo se procesan los que baten el récord, y el resto cae. Es el caso extremo de «no espero nada».
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué decide el retraso configurado en un watermark?
o: Cuánto se espera antes de cerrar una ventana, a cambio de acumular estado
o: Cuántos eventos se pueden guardar en memoria
o: La velocidad del disco
a: 1
e: El retraso es una apuesta entre latencia y completitud: más retraso procesa mejor los eventos desordenados y mantiene estado y ventanas abiertas más tiempo; menos retraso responde antes y descarta más.
:::

:::quiz
p: Usas tiempo de procesamiento en lugar de tiempo de evento. ¿Qué pierdes?
o: La posibilidad de reproducir el resultado, porque depende de cuándo se ejecutó el proceso
o: Nada, es más rápido y equivalente
o: Solo la zona horaria
a: 1
e: Con tiempo de proceso, dos ejecuciones del mismo histórico dan resultados distintos. El tiempo de evento está en el dato y permite reprocesar y comparar, que es lo que hace auditable un pipeline.
:::
