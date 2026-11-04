---
id: ventanas-y-watermarks
titulo: Ventanas y marcas de agua
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [streaming-tiempo-real, kafka-y-colas, ingesta-incremental-y-cdc]
tags: [streaming, ventanas, watermarks, tardanzas, tiempo-de-evento]
resumen: Cuándo cerrar una ventana de agregación, cuánto esperar a los datos que llegan tarde y qué hacer con los que aparecen después del cierre.
fuentes: ["Akidau et al. (2015), 'The Dataflow Model'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 11"]
---

## En una frase

Una ventana agrupa los eventos por el momento en que ocurrieron, y la marca de agua es el reloj que
dice hasta dónde ha llegado ese tiempo de evento: cuando la marca de agua sobrepasa el final de una
ventana, la ventana se cierra y su recuento se publica.

## La idea

Piensa en el recuento de maletas de un aeropuerto. Cada maleta se escanea en la cinta en el momento
en que pasa, pero el parte se sube a la central cuando el lector encuentra red. Si cierras la cuenta
de la hora 8:00-9:00 a las 9:00 en punto, las maletas de esa hora que subieron su parte a las 9:04
se pierden o se cuelan en la hora siguiente. El dato trae su propia fecha y esa fecha no coincide
con la de llegada: es el problema que resuelve todo el tiempo de evento, y aquí se decide la parte
que duele, **cuándo dejas de esperar**.

Antes de cerrar nada hay que elegir la ventana, y hay tres formas que se usan a diario:

- **Fija** (tumbling): intervalos que ni se solapan ni dejan hueco, `[08:00, 08:05)`,
  `[08:05, 08:10)`. Es la que alimenta informes y cuadros de mando.
- **Deslizante** (sliding): ventanas solapadas que se recalculan cada cierto paso. Una media móvil
  de diez minutos recalculada cada minuto son diez ventanas vivas a la vez.
- **De sesión**: no se corta por reloj, sino por inactividad. Un hueco de treinta minutos sin
  eventos cierra la sesión y el siguiente evento abre otra.

El tamaño y el paso son decisiones de negocio, no técnicas: un minuto para alertas, una hora para el
informe diario. En SQL, estas agregaciones se escriben con funciones de ventana ([[sql-ventanas]]).

Ahora la marca de agua, que es una **apuesta, no un hecho**: «doy por hecho que ya no va a llegar
nada con tiempo de evento anterior a W». Se calcula con el mayor tiempo de evento visto hasta ahora
menos un margen `R`, y tiene una propiedad que no se puede romper: **nunca retrocede**. Si
retrocediera, reabriría ventanas ya publicadas y el consumidor vería dos resultados distintos para
el mismo intervalo, que es la forma más rápida de perder la confianza en un dato.

La marca de agua es lo que convierte «esperar un poco más» en una regla: cuando `W` alcanza el final
de la ventana, se cierra y se publica. El margen `R` es el parámetro que se negocia: subirlo reduce
los datos perdidos y aumenta la latencia, y bajarlo da resultados antes y descarta más. No se elige a
ojo.

Queda la decisión que casi nadie documenta: qué hacer con el evento que llega **después** del
cierre. Hay dos políticas:

1. **Descartarlo**, mandándolo a un flujo aparte de tardíos o a una tabla de cuarentena. Es simple y
   el resultado publicado no cambia nunca. A cambio, el recuento se queda corto para siempre.
2. **Reemitir el resultado corregido**, y entonces el consumidor necesita **retractación**: la
   emisión nueva no se suma a la anterior, la sustituye. Sin retractación, el total sale contado dos
   veces y el error es más caro que el dato perdido.

Y un detalle que sorprende: no decide el retraso del evento, decide cuánto había avanzado la marca de
agua cuando llegó. Un evento con ocho minutos de retraso entra si el flujo no había visto nada más
nuevo; otro con cuatro se queda fuera si por medio llegó algo que la empujó más allá de su ventana.

:::figura
fichero: ventanas-y-watermarks-cierre
pie: A la izquierda, cada evento por su tiempo de evento y su retraso de llegada. La línea discontinua es el retraso permitido, pero no separa a los que entran de los que se quedan fuera: por encima de ella hay puntos azules, que entraron, y cruces rojas, que no, porque lo que decide es la marca de agua del sistema y no el retraso de cada evento. A la derecha, el recuento que se publicó al cerrar cada ventana: los tramos rojos son eventos que llegaron después del cierre y nunca entraron en el número publicado, y el tramo gris es la última ventana, que todavía no se ha cerrado.
fuente: figuras/ventanas-y-watermarks-1.py
:::

## Definición formal

En el instante de proceso `t`, la marca de agua es el mayor tiempo de evento ya visto menos el
retraso permitido:

:::formula
W(t) = max{ e_i : ya vistos en t } − R
:::

Con eso, el cierre es una comparación: la ventana `[a, b)` se cierra, y su resultado se publica, en
cuanto `W(t) ≥ b`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `W(t)` | Marca de agua: hasta dónde se da por completo el tiempo de evento | instante de tiempo de evento | Si avanza más rápido, cierras antes: ganas frescura y descartas más eventos tardíos |
| `e_i` | Tiempo de evento del evento i-ésimo que el sistema ya ha visto | instante de tiempo de evento | Es el que manda: la marca de agua es su máximo menos el margen |
| `R` | Retraso permitido o tolerancia a tardanzas | minutos o segundos | Al subir, esperas más: entran más eventos correctos y el resultado llega más tarde |
| `[a, b)` | La ventana: `a` incluido, `b` excluido | instantes | Una ventana más ancha agrupa más eventos y tarda más en poder cerrarse |
| `b − a` | Tamaño de la ventana | minutos u horas | Al subir, menos filas de salida y menos resolución para ver picos |
| `p99` | Percentil 99 del retraso de llegada medido en producción | minutos | Es el valor con el que se elige `R`; si sube, `R` tiene que subir con él |
| `tardíos` | Eventos que llegan con su ventana ya cerrada | eventos | Al subir, más recuentos publicados que se quedan cortos o más reemisiones que corregir |
:::

## Ejemplo

Ventana fija de cinco minutos y margen `R = 3`. Llegan seis eventos, y la tabla muestra qué pasa con
cada uno al procesarlo:

| Llega a las | Tiempo de evento | Retraso | Marca de agua | Ventanas abiertas |
| --- | --- | --- | --- | --- |
| 08:01 | 08:00 | 1 | 07:57 | 08:00 |
| 08:04 | 08:04 | 0 | 08:01 | 08:00 |
| 08:07 | 08:06 | 1 | 08:03 | 08:00 y 08:05 |
| 08:09 | 08:03 | 6 | 08:03 | 08:00 y 08:05 |
| 08:12 | 08:11 | 1 | 08:08 | 08:05 y 08:10 |
| 08:15 | 08:02 | 13 | 08:08 | 08:05 y 08:10 |

Cuando llega el de las 08:12, la marca de agua salta a 08:08 y la ventana `[08:00, 08:05)` se cierra
con **3 eventos** (08:00, 08:04 y 08:03). Ese tercero llegó con seis minutos de retraso, más que el
margen de tres, y entró igual: cuando apareció, la marca de agua estaba en 08:03 y su ventana seguía
abierta. El de las 08:15, en cambio, se queda fuera con trece minutos de retraso: su ventana ya se
había publicado. Si la política es descartar, va a la tabla de tardíos y el recuento publicado se
queda en 3; si la política es reemitir, hay que publicar un 4 que **sustituye** al 3 anterior.

## Código

```python verificable
llegadas = [(1, 0), (4, 4), (7, 6), (9, 3), (12, 11), (15, 2)]   # (llega, tiempo de evento)
R, ANCHO = 3, 5                                                 # margen y tamano de ventana
max_visto, abiertas, publicadas, tardios = -99, {}, {}, []

for llega, evento in llegadas:
    max_visto = max(max_visto, evento)          # la marca de agua nunca retrocede
    marca = max_visto - R
    inicio = int(evento // ANCHO) * ANCHO       # a que ventana pertenece el evento
    if inicio in publicadas:                    # su ventana ya se publico: llega tarde
        tardios.append((llega, evento))
    else:
        abiertas[inicio] = abiertas.get(inicio, 0) + 1
    for w in sorted(abiertas):                  # cierra lo que la marca de agua ya dejo atras
        if w + ANCHO <= marca:
            publicadas[w] = abiertas.pop(w)
    print(f"llega {llega:2d}  evento {evento:2d}  marca {marca:3d}  abiertas {sorted(abiertas)}")

print("publicadas:", {f"8:{w:02d}": c for w, c in sorted(publicadas.items())})
print("abiertas al final:", {f"8:{w:02d}": c for w, c in sorted(abiertas.items())})
print("tardios:", tardios)
# -> publicadas: {'8:00': 3}
# -> abiertas al final: {'8:05': 1, '8:10': 1}
# -> tardios: [(15, 2)]
```

:::claves
- `max_visto = max(max_visto, evento)` es la línea que hace monótona la marca de agua. Si la
  escribieras como `marca = evento - R`, la marca de agua daría marcha atrás con cada evento
  desordenado y las ventanas ya publicadas se volverían a publicar.
- `abiertas.pop(w)` devuelve el valor **y** quita la clave del diccionario. Con `abiertas[w]` la
  ventana seguiría dentro y se volvería a publicar en cada iteración posterior, con el mismo
  recuento varias veces.
- El recuento de una ventana no se cierra al llegar el último evento de su intervalo, sino cuando
  otro evento posterior empuja la marca de agua: `[08:00, 08:05)` se publica a las 08:12, no a las
  08:05.
- `int(evento // ANCHO) * ANCHO` es la forma de saber a qué ventana fija pertenece un instante. El
  límite de la derecha no entra: 08:05 cae en la ventana que empieza en 08:05, no en la anterior.
- La lista `llegadas` está ordenada por instante de **llegada**, no por tiempo de evento. Si la
  ordenaras por tiempo de evento estarías simulando un mundo donde nada llega tarde y el ejemplo no
  enseñaría nada.
- `tardios` guarda los eventos descartados, pero eso es una decisión: si en vez de una lista fuera un
  contador que suma al recuento publicado, tendrías la política de reemitir, y el consumidor
  necesitaría saber que el 4 sustituye al 3.
:::

El margen `R` no se adivina: se mide el retraso con el que llegan los eventos de verdad y se toma un
percentil alto.

```python verificable
import numpy as np

# Retrasos de llegada de una semana, en minutos (semilla fija para que sea reproducible)
azar = np.random.default_rng(7)
retrasos = azar.gamma(shape=2.0, scale=1.5, size=20000)

print(f"p50 {np.percentile(retrasos, 50):.2f} min")     # -> p50 2.51 min
print(f"p90 {np.percentile(retrasos, 90):.2f} min")     # -> p90 5.82 min
print(f"p99 {np.percentile(retrasos, 99):.2f} min")     # -> p99 9.83 min
# Con R = 10 entra el 99 % de los eventos; con R = 3, la mitad se queda fuera.
```

## Errores típicos

- **Cerrar la ventana con el reloj de proceso** («a las 9:00 en punto cierro la hora de las 8»). Es
  el error de partida: todo lo que llegue tarde se pierde o se contabiliza en la hora equivocada.
  Las agregaciones por hora natural se cierran con la marca de agua, no con la hora del sistema.
- **Elegir `R` por lo que suena bien.** Un margen de cinco minutos porque es un número redondo deja
  fuera todo lo que supere ese retraso, y en una fuente con ráfagas eso es una parte del negocio.
  Mira el percentil 99 del retraso real y decide cuánto estás dispuesto a esperar.
- **Dejar que la marca de agua retroceda.** Pasa cuando se reinicia el proceso y vuelve a calcular
  el máximo desde cero, o cuando se usa el tiempo del último evento en vez del máximo. El resultado
  son dos cifras distintas para la misma hora y un consumidor que ya no sabe cuál creer.
- **Reemitir sin retractar.** Si publicas el recuento corregido y el consumidor suma, el total crece
  sin que haya pasado nada. Reemitir exige un canal de retractación y consumidores que sepan
  aplicarlo; si no lo tienes, descarta y cuadra el hueco por otra vía.
- **No separar los tardíos.** Sin un flujo o una tabla de cuarentena, un evento tardío desaparece sin
  rastro: no puedes medir cuántos pierdes ni reprocesarlos cuando toque
  ([[backfill-y-reproceso]]).
- **Suponer que la ventana cerrada está completa.** Un fichero escrito para la ventana de las 9:00 no
  significa que a las 9:00 ya estuvieran todos los eventos. Si la latencia importa, publica con la
  marca de agua y deja claro hasta dónde llega ese dato ([[calidad-y-slas]]).

:::practica
enunciado: Con una ventana fija de diez minutos y un margen R = 2, llegan estos eventos (hora de llegada, tiempo de evento): 09:00 y 09:00, 09:03 y 09:08, 09:06 y 09:02, 09:11 y 09:12, 09:14 y 09:09. ¿En qué momento se cierra la ventana [09:00, 09:10) y con cuántos eventos? ¿Qué pasa con el evento de las 09:09?
pista: La marca de agua es el mayor tiempo de evento visto menos R, y la ventana se cierra cuando la marca de agua alcanza las 09:10.
solucion: Tras el de 09:00 la marca va en 08:58; tras el de 09:03, en 09:06 (el mayor es 09:08); tras el de 09:06 sigue en 09:06; y al llegar el de 09:11, el mayor visto es 09:12 y la marca salta a 09:10, así que la ventana se cierra con 3 eventos (09:00, 09:02 y 09:08). El de 09:09 llegó a las 09:14, con la ventana ya cerrada: con la política de descartar va a tardíos y el recuento publicado se queda en 3. Si subieras R a 5, la marca iría en 09:07 cuando llegó y la ventana seguiría abierta, así que el evento entraría; a cambio, la ventana no se cerraría hasta que llegara algo con tiempo de evento 09:15 o posterior, al menos cuatro minutos más tarde.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa exactamente que la marca de agua esté en 08:08 con un margen de 3 minutos?
o: Que el último evento visto tenía tiempo de evento 08:08
o: Que se da por hecho que ya no llegará nada con tiempo de evento anterior a 08:05
o: Que todos los eventos con tiempo de evento 08:08 ya han llegado y están contados
a: 2
e: La marca de agua es el mayor tiempo de evento visto (08:11) menos el margen (3), y expresa una apuesta: no esperar nada anterior a 08:05. No dice nada del instante de llegada ni garantiza que hayan llegado todos los eventos hasta ahí.
:::

:::quiz
p: Un evento con 8 minutos de retraso entra en su ventana y otro con 4 se queda fuera. ¿Cómo se explica?
o: Es un fallo del motor: con el mismo margen no puede pasar
o: Entra el que llegó cuando su ventana seguía abierta; la marca de agua no depende del retraso de cada evento
o: El de 8 minutos tenía un tiempo de evento más antiguo y por eso se admite siempre
a: 2
e: La marca de agua avanza con el mayor tiempo de evento visto, no con el retraso de cada evento. Si el flujo no había visto nada más nuevo, un evento muy retrasado encuentra su ventana abierta y entra; si por medio llegó algo que empujó la marca de agua, otro con menos retraso la encuentra cerrada. Ese es el motivo de que el retraso medido no sea la frontera exacta.
:::

:::quiz
p: Publicas por horas y llega un evento de las 08:59 a las 09:20, con la ventana ya cerrada. Tu política es reemitir. ¿Qué tiene que hacer el consumidor?
o: Sumar el nuevo recuento al que ya tenía
o: Sustituir el recuento anterior por el corregido, porque la reemisión lo retracta
o: Ignorarlo, porque un dato que llega tarde nunca es válido
a: 2
e: Reemitir sin retractar duplica el recuento: el consumidor se queda con la suma de las dos emisiones. La reemisión publica un resultado que sustituye al anterior, y el consumidor tiene que saber aplicarlo. Ignorarlo equivale a la política de descartar, pero sin dejar rastro del evento.
:::
