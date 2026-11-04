---
id: priorizar-y-planificar
titulo: "Priorizar: qué se hace, qué se aplaza y qué se descarta"
fase: 12
nivel: intermedio
rutas: [core, alg]
prerequisitos: [dashboards, storytelling-con-datos, escribir-un-informe]
tags: [priorizacion, planificacion, producto, roadmap, foco]
resumen: Cómo decidir en qué se trabaja cuando todo parece urgente: coste del retraso entre tamaño, capacidad real, trabajo en curso limitado y qué se descarta por escrito.
fuentes: ["Reinertsen (2009), 'The Principles of Product Development Flow'", "Cohn (2005), 'Agile Estimating and Planning'", "Doerr (2018), 'Measure What Matters'"]
---

## En una frase

Priorizar es decidir tres cosas a la vez —qué se hace ahora, qué se aplaza con una condición y qué
se descarta— comparando lo que cuesta retrasar cada cosa con lo que cuesta hacerla, y dejando por
escrito lo descartado para no volver a discutirlo cada mes.

## La idea

Cuando alguien dice «todo es prioritario», lo que está diciendo es que no hay prioridades. Y el
síntoma se ve en la forma de trabajar: cinco cosas abiertas por persona, ninguna terminada, y una
reunión semanal para decidir cuál se empuja esta semana. El problema rara vez es falta de
esfuerzo: **el trabajo pendiente es una cola**, y las colas tienen leyes que no se negocian.

La primera ley dice que el tiempo que tarda algo en terminarse no depende de lo mucho que se
empuje, sino de cuánto trabajo hay por delante. Si el equipo tiene doce cosas en curso y termina
tres y media por semana, cada cosa tarda unas tres semanas y media en salir, por rápida que sea
individualmente. Con seis en curso, tardan la mitad. El mismo equipo, la misma gente, el mismo
esfuerzo: la diferencia es cuántas cosas se empezaron a la vez. Por eso empezar más trabajo no
acelera nada; retrasa todo.

La segunda ley explica por qué planificar al cien por cien de la capacidad es imposible. Cuando un
recurso está casi ocupado, cualquier cosa que llega espera; y la espera no crece de forma
proporcional a la ocupación, crece mucho más rápido. Al 50 % de ocupación, una tarea espera de
media lo que tarda en hacerse; al 90 %, nueve veces más; al 95 %, diecinueve. Ese es el motivo real
por el que conviene dejar aire en el plan: es la única forma de
que el trabajo urgente no arrastre a todo lo demás. Un equipo al 100 % es una cola larga.

**El coste del retraso no es el mismo para todo.** Hay tres formas típicas:

- **Lineal:** cada semana que no está cuesta lo mismo. Mejorar un proceso interno, reducir el
  tiempo de carga de una página.
- **Con fecha límite:** hasta una fecha vale mucho y después vale cero o negativo. Una campaña de
  Navidad, una obligación legal, una ventana de mercado. Aquí no se prioriza por valor total, sino
  por no llegar tarde, y a menudo la pieza más pequeña es la que hay que hacer ya.
- **Con decaimiento:** vale menos cada semana porque el mercado se enfría o el competidor llega
  antes. Es la forma de casi todo lo que tiene que ver con oportunidades.

**Priorizar es dividir.** La prioridad no sale del valor, sale del cociente entre el coste del
retraso y lo que cuesta hacerlo. Una mejora pequeña con mucho valor se hace ya; una iniciativa
enorme y valiosa espera, se trocea y se entrega por partes que ya dan valor.

Dividir por tamaño da
el coste de ocupar la cola; dividir por duración da el coste de esperar. No son lo mismo: una cosa
grande que se paraleliza tiene mucho tamaño y poca duración, y su valor llega antes.

**Decidir es descartar.** Si nada se descarta, la lista de pendientes crece cada mes y la palabra
prioridad pierde sentido: todo está dentro y todo espera. Descartar de verdad significa dejar algo
fuera y **escribirlo** con su condición de revisión: «esto no se hace hasta que la migración esté
cerrada, y lo revisamos en septiembre». Guardar una lista de «algún día» sin condición de revisión
es aplazar el problema, no decidirlo. Y descartar una idea no significa rechazar a
quien la propuso: la decisión va sobre el trabajo.

**Lo que se promete con fecha es lo que ya está casi hecho.** Prometer una fecha para algo que no
se ha empezado es adivinar, y la falacia de la planificación es universal: todo el mundo tarda más
de lo que cree, incluso cuando ya le ha pasado antes. Para lo demás se promete orden y resultado,
no fecha, y se revisa cuando hay datos nuevos. El compromiso se hace contra un percentil alto del
rango, no contra la media.

**La deuda técnica también se prioriza, y pierde siempre.** Comparada con una funcionalidad nueva,
una tarea de mantenimiento nunca tiene un defensor con la misma energía. Por eso se reserva un
porcentaje fijo de cada iteración, decidido una vez, en lugar de discutirlo cada dos semanas
([[coste-y-optimizacion]]).

## Definición formal

**Ley de Little.** Relaciona el trabajo en curso, el ritmo de entrega y el tiempo de ciclo:

:::formula
WIP = Θ · CT
:::

**La espera crece con la ocupación.** En un sistema con llegadas aleatorias y servicio variable,
la espera media en cola, medida en múltiplos del tiempo de servicio, es:

:::formula
W = (1/μ) · ρ / (1 − ρ)
:::

**Coste del retraso.** Se estima en unidades relativas y se compone de cuatro sumandos:

:::formula
CD = valor_de_negocio + criticidad_temporal + reducción_de_riesgo + valor_de_habilitación
:::

**Las dos formas de priorizar con él.** Dividir por tamaño mide lo que la iniciativa ocupa en la
cola; dividir por duración mide cuándo llega su valor:

:::formula
WSJF = CD / tamaño        CD3 = CD / duración
:::

**Capacidad planificable.** De la capacidad nominal hay que descontar lo que se come el trabajo no
planificado:

:::formula
capacidad_planificable = capacidad_nominal · (1 − interrupción)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `WIP` | Trabajo empezado y no terminado | elementos | Al subir, sube el tiempo de ciclo en la misma proporción. Es la variable que más se puede tocar y la que menos se toca: limitar el trabajo en curso es gratis y casi nadie lo hace |
| `Θ` | Ritmo de entrega del equipo, medido en elementos terminados | elementos por semana | Al subir, baja el tiempo de ciclo. Pero es la variable lenta: mejorar el ritmo real cuesta meses y sube de golpe solo si se reduce el trabajo a medias |
| `CT` | Tiempo de ciclo: de empezar algo a terminarlo | semanas | Al subir, el valor llega más tarde y las estimaciones envejecen. Con `CT` alto, decidir «qué se hace primero» importa menos que decidir «cuántas cosas a la vez» |
| `ρ` | Ocupación del recurso: fracción del tiempo que está trabajando | tanto por uno | Al subir, la espera crece como `ρ / (1 − ρ)`: al 50 % es 1 vez el tiempo de servicio, al 90 % es 9 y al 95 % es 19. Es la razón matemática de planificar con holgura |
| `μ` | Ritmo de servicio del recurso | tareas por semana | Al subir, cada tarea tarda menos y la espera baja en la misma proporción. Duplicar la capacidad reduce la espera a la mitad, pero no arregla una cola descontrolada |
| `CD` | Coste del retraso: lo que se pierde por cada unidad de tiempo que algo no está | euros por semana, o relativo | Al subir, la iniciativa sube en la lista. Antes de comparar, comprueba que todos los `CD` están en la misma unidad y en el mismo horizonte |
| `tamaño` | Esfuerzo total estimado de la iniciativa | personas-semana, puntos | Al subir, baja el `WSJF`: una iniciativa grande ocupa más cola y retrasa a las demás. Un tamaño mal estimado cambia el orden entero, así que se estima en rango |
| `duración` | Tiempo de calendario hasta que la iniciativa entrega valor | semanas | Al subir, baja el `CD3`. Es lo que distingue una iniciativa grande y paralelizable (tamaño alto, duración corta) de una secuencial |
| `interrupción` | Fracción de la capacidad que se va en soporte, incidencias y trabajo no planificado | tanto por uno | Al subir, baja la capacidad planificable y todas las fechas se mueven. Es la partida que más se ignora al planificar y la que más se cumple |
| `valor_de_habilitación` | Cuánto valor futuro desbloquea esta iniciativa | relativo | Al subir, adelanta a otras aunque no dé valor directo hoy. Es el sumando que hace que la migración aburrida gane a la funcionalidad lucida |
:::

## Ejemplo

Cuatro iniciativas de un equipo, con el coste del retraso desglosado y dos formas de dividirlo:

```
iniciativa          valor  plazo  riesgo  habilita  CD  tamaño  duración   WSJF    CD3
arreglar el cobro       8      5       3         2  18       2         1    9,0  18,0
informes nuevos         5      0       1         1   7       5         3    1,4   2,3
migrar la base          3      1       5         3  12       8        10    1,5   1,2
buscador                5      0       0         1   6       3         4    2,0   1,5
```

Las dos columnas ordenan distinto y las dos tienen razón, según lo que se esté optimizando:

- **Por WSJF** (coste del retraso entre tamaño, que es coste de cola): cobro, buscador, migración,
  informes. El buscador es pequeño y adelanta a la migración, que ocupa mucho.
- **Por CD3** (coste del retraso entre duración, que es coste del reloj): cobro, informes,
  buscador, migración. Los informes se pueden paralelizar: mucho tamaño (5) pero poca duración
  (3 semanas), así que su valor llega antes que el del buscador, que depende de una sola persona
  durante 4 semanas.

Con Little, el mismo equipo con doce cosas en curso y tres y media terminadas por semana tarda
12 / 3,5 = **3,4 semanas** por elemento; limitando el trabajo en curso a seis, **1,7 semanas**. Sin
cambiar a nadie ni trabajar más horas.

Y la ocupación explica por qué el plan al 100 % no cabe: con una ocupación del 90 %, una tarea que
tarda tres días espera de media 9 · 3 = **27 días** antes de empezar, y el trabajo urgente que
aparece por el camino espera lo mismo que los demás. Al 70 % de ocupación la espera es 2,3 veces el
tiempo de servicio: unos 7 días para esa misma tarea. Ese aire es lo que hace que las fechas se
cumplan.

Capacidad del sprint: cinco personas y diez días laborables son 50 personas-día nominales; con un
30 % de interrupción quedan **35 planificables**. Si cada tarea tarda entre 3 y 9 días, cuatro
tareas caben prácticamente siempre (p80 = 27 personas-día), cinco caben el 89 % de las veces
(p80 = 34) y seis solo caben el 46 % (p80 = 40). Comprometer seis tareas porque la media son 36
personas-día es así como se promete lo que no cabe.

:::figura
fichero: priorizar-cola-y-coste-del-retraso
pie: Izquierda, la espera relativa en función de la ocupación: crece como el cociente entre la ocupación y lo que le falta para el 100 %, así que al 70 % una tarea espera 2,3 veces su tiempo de servicio y al 95 % espera 19. Ese es el motivo de dejar aire en el plan, no una concesión al descanso. Derecha, tres formas de coste del retraso acumulado: lineal, con fecha límite (el acantilado en el que el valor se desploma si se pasa la fecha) y con decaimiento. La pendiente decide el orden, y por eso dos iniciativas con el mismo valor total no se priorizan igual.
fuente: figuras/priorizar-y-planificar-1.py
:::

## Código

```python verificable
import pandas as pd

# Cuatro iniciativas: el coste del retraso son cuatro componentes que se suman,
# y el tamano (o la duracion) dividen. Todo en unidades relativas, como se hace de verdad.
iniciativas = pd.DataFrame({
    "iniciativa": ["arreglar el cobro", "informes nuevos", "migrar la base", "buscador"],
    "valor_negocio": [8, 5, 3, 5],
    "criticidad_temporal": [5, 0, 1, 0],
    "riesgo": [3, 1, 5, 0],
    "habilitacion": [2, 1, 3, 1],
    "tamano": [2, 5, 8, 3],
    "duracion_semanas": [1, 3, 10, 4],
})
componentes = ["valor_negocio", "criticidad_temporal", "riesgo", "habilitacion"]
iniciativas["coste_retraso"] = iniciativas[componentes].sum(axis=1)

# WSJF mide el coste de la cola (divide por tamano); CD3, el coste del reloj (por duracion).
iniciativas["wsjf"] = (iniciativas.coste_retraso / iniciativas.tamano).round(2)
iniciativas["cd3"] = (iniciativas.coste_retraso / iniciativas.duracion_semanas).round(2)
print(iniciativas[["iniciativa", "coste_retraso", "tamano", "wsjf", "cd3"]].to_string(index=False))
print("por WSJF:", list(iniciativas.sort_values("wsjf", ascending=False).iniciativa))
# -> por WSJF: ['arreglar el cobro', 'buscador', 'migrar la base', 'informes nuevos']
print("por CD3: ", list(iniciativas.sort_values("cd3", ascending=False).iniciativa))
# -> por CD3:  ['arreglar el cobro', 'informes nuevos', 'buscador', 'migrar la base']
```

:::claves
- `iniciativas[componentes].sum(axis=1)` suma **por filas**, que es lo que se quiere: el coste del
  retraso de cada iniciativa. Sin `axis=1`, pandas suma por columnas y devuelve cuatro números que
  no significan nada.
- Las dos ordenaciones salen del mismo `coste_retraso` y solo cambia el divisor. Que la lista se
  dé la vuelta según el divisor no es un fallo del método: es la señal de que hay que decidir qué
  se está optimizando, si el coste de la cola (tamaño) o el momento en que llega el valor
  (duración).
- Todos los números son relativos. La escala de 1 a 10 en cada componente y el consenso del equipo
  importan más que la precisión: lo que se discute al estimar es si el riesgo de la migración vale
  5 o 8, y esa discusión es el producto real del método.
- `round(2)` después de dividir solo afecta a la presentación. Si dos iniciativas quedan empatadas,
  el desempate se hace por criterio explícito (dependencias, una persona clave, compromiso externo)
  y se deja escrito, porque si no el orden lo decide el que más insiste.
:::

```python verificable
# Ley de Little: el tiempo de ciclo no lo fija el esfuerzo, lo fija el trabajo en curso.
TERMINADOS = 3.5
for wip in (4, 6, 12, 20):
    print("WIP %2d -> tiempo de ciclo %.1f semanas" % (wip, wip / TERMINADOS))
# -> WIP 12 -> tiempo de ciclo 3.4 semanas
# -> WIP  6 -> tiempo de ciclo 1.7 semanas

# Utilizacion: la espera crece como rho/(1-rho), no como rho. Por eso el 100 % no existe.
for rho in (0.5, 0.7, 0.8, 0.9, 0.95):
    print("utilizacion %.0f %% -> espera %.1f veces el tiempo de servicio" % (100 * rho, rho / (1 - rho)))
# -> utilizacion 70 % -> espera 2.3 veces el tiempo de servicio
# -> utilizacion 95 % -> espera 19.0 veces el tiempo de servicio
```

:::claves
- La ley de Little no dice que el trabajo en curso cause el tiempo de ciclo: es una identidad, y se
  cumple siempre. Lo que se decide con ella es qué variable se toca. Si no se puede subir el ritmo
  de entrega, lo único que queda para bajar el tiempo de ciclo es bajar el trabajo en curso, y eso
  es gratis.
- `ρ / (1 − ρ)` es la espera de un modelo de cola con llegadas aleatorias y un solo servidor
  (M/M/1). Exagera, porque un equipo no es un servidor único ni las llegadas son del todo
  aleatorias, pero la no linealidad es real: pasar del 80 % al 90 % de ocupación no empeora la
  espera un 12 %, la multiplica por 2,25. En la práctica, un equipo por encima del 85 % de
  ocupación efectiva empieza a perder fechas de forma sistemática.
- El `TERMINADOS = 3.5` es el ritmo real medido, no el deseado. Si se mide el ritmo con el trabajo
  a medias incluido, el número sale inflado y el tiempo de ciclo calculado miente a la baja.
- Esta cuenta se hace por equipo, no por persona. El trabajo en curso de una persona no se puede
  limitar a la mitad sin dejar de atender el soporte; el de un equipo, sí, y es la palanca que
  funciona.
:::

```python verificable
import numpy as np

# Capacidad: la nominal no es la real. El soporte, las incidencias y las entrevistas
# se comen una parte fija del sprint y no desaparecen porque el plan este lleno.
capacidad_nominal = 5 * 10          # 5 personas, 10 dias laborables
interrupcion = 0.30
planificable = capacidad_nominal * (1 - interrupcion)
print("capacidad planificable: %.0f personas-dia de %d" % (planificable, capacidad_nominal))
# -> capacidad planificable: 35 personas-dia de 50

# Cada tarea tarda entre 3 y 9 dias. Lo que se promete no es la media: es un percentil.
rng = np.random.default_rng(7)
for tareas in (4, 5, 6):
    totales = rng.integers(3, 10, size=(20_000, tareas)).sum(axis=1)
    cabe = 100 * float((totales <= planificable).mean())
    print("%d tareas -> p50 %2.0f, p80 %2.0f personas-dia, cabe en el sprint el %.0f %% de las veces"
          % (tareas, np.percentile(totales, 50), np.percentile(totales, 80), cabe))
# -> 5 tareas -> p50 30, p80 34 personas-dia, cabe en el sprint el 89 % de las veces
# -> 6 tareas -> p50 36, p80 40 personas-dia, cabe en el sprint el 46 % de las veces
```

## Errores típicos

- **Planificar al 100 % de la capacidad.** Deja el sistema sin aire y convierte cualquier
  imprevisto en un retraso de todo lo demás. Planifica el 70-80 % y llama al resto «capacidad para
  lo que pasa», no «tiempo libre».
- **Empezar más de lo que se termina.** Es la causa directa del tiempo de ciclo largo: con doce
  cosas abiertas se tarda 3,4 semanas por cosa; con seis, 1,7. Limitar el trabajo en curso es la
  medida más barata y la que más resistencia genera, porque parece que frena al equipo.
- **Priorizar por quién grita más o por antigüedad de la petición.** El orden acaba decidiéndolo
  la persona con más poder de interrupción, no el coste del retraso. Si la prioridad se cambia
  cada semana, el trabajo a medias se acumula y ningún criterio sobrevive.
- **Prometer fechas para trabajo no empezado.** Es adivinar con seguridad. Se promete orden y
  resultado, y fecha solo para lo que ya está casi hecho o para lo que tiene una restricción
  externa real.
- **Estimar con un punto en vez de con un rango.** Un único número invita a comprometerse con él, y
  es el mejor de los casos disfrazado. El compromiso se hace contra el percentil 80 del rango.
- **Olvidar las interrupciones.** Si el plan no descuenta el soporte, las incidencias y las
  entrevistas, el equipo no va lento: está haciendo otro trabajo que nadie apuntó.
  Medirlo durante un mes suele dar entre el 20 % y el 40 % de la capacidad.
- **No descartar nada.** Un backlog que solo crece es una lista de deseos. Lo descartado se escribe
  con su condición de revisión y su dueño, y así no vuelve cada mes a la conversación.
- **Confundir esfuerzo con valor.** Una tarea difícil no es más importante que una fácil. El
  esfuerzo es el divisor; el valor, el numerador. Cambiarlos de sitio pone arriba lo que más cuesta
  hacer, que es casi siempre lo que menos valor da por semana de espera.
- **Tratar la deuda técnica y el mantenimiento como lo que se hace si sobra tiempo.** Nunca sobra,
  y la deuda se paga con intereses en el peor momento: en medio de un incidente o de una campaña
  ([[coste-y-optimizacion]]).
- **Medir la ocupación como señal de productividad.** Un equipo al 100 % con una cola larga no está
  trabajando mejor: está garantizando que lo urgente espere. Lo que se mide es el tiempo de ciclo y
  lo que se entrega, no lo ocupado que se está.

## Comprueba que lo sabes

:::practica
enunciado: Un equipo de cuatro personas tiene un sprint de dos semanas (10 días laborables) y dedica el 25 % de su tiempo a soporte e incidencias. Cada tarea tarda entre 4 y 8 días. Llegan tres iniciativas: A con coste del retraso 15 y tamaño 3, B con coste 9 y tamaño 9, y C con coste 6 y tamaño 2. Ordena por WSJF, calcula la capacidad planificable, decide cuántas tareas se pueden comprometer con una probabilidad razonable y explica qué haces con B.
pista: La capacidad planificable es la nominal menos la interrupción. Para el compromiso, mira el percentil 80 de la suma, no la media.
solucion: Capacidad nominal = 4 · 10 = 40 personas-día; planificable = 40 · 0,75 = 30 personas-día. WSJF: A = 15/3 = 5,0; B = 9/9 = 1,0; C = 6/2 = 3,0. El orden es A, C, B. Con tareas de 4 a 8 días (media 6, desviación de la suma unas 1,6 por tarea), tres tareas suman de media 18 personas-día y su p80 anda por 21, así que las tres caben con holgura dentro de 30; cuatro tareas (media 24, p80 unos 27) siguen cabiendo, y cinco ya se acercan al límite. Lo razonable es comprometer A y C con fecha y meter B solo si queda capacidad, porque B es la que menos valor da por unidad de esfuerzo. Y con B hay una decisión más importante que la de meterla o no: su tamaño 9 con coste 9 es una señal de que hay que trocearla, porque casi siempre existe una primera parte que ya entrega valor y ocupa mucho menos.
:::

:::quiz
p: Un equipo tiene 12 elementos empezados y sin terminar, y termina 3,5 por semana. ¿Qué pasa si empieza 6 elementos más de golpe, sin cambiar nada más?
o: El tiempo de ciclo baja porque hay más trabajo avanzando en paralelo
o: El tiempo de ciclo sube: los 18 elementos en curso tardarán unas 5,1 semanas cada uno con el mismo ritmo de entrega
o: El ritmo de entrega sube de forma proporcional al trabajo en curso
a: 2
e: Por la ley de Little, el tiempo de ciclo es el trabajo en curso dividido entre el ritmo de entrega: 12 / 3,5 = 3,4 semanas antes y 18 / 3,5 = 5,1 semanas después. Empezar más cosas no aumenta el ritmo de entrega, porque el ritmo lo limita la capacidad del equipo; lo único que cambia es que cada cosa tarda más en salir. El paralelismo solo ayuda cuando hay personas ociendas o cuellos de botella distintos, y aquí no es el caso.
:::

:::quiz
p: Dos iniciativas tienen el mismo coste del retraso total. Una puede tener un equipo de tres personas durante dos semanas y la otra necesita a una persona durante ocho semanas. ¿Cuál se hace antes y por qué?
o: La de ocho semanas, porque ocupa más tiempo el recurso y hay que empezarla antes
o: La de dos semanas con tres personas, porque su valor llega antes: es la que gana dividiendo por duración
o: Da igual, porque el valor total es el mismo
a: 2
e: Con el mismo coste del retraso, gana la que entrega antes, que es la de tres personas durante dos semanas: dividir por duración (CD3) mide cuándo llega el valor. La otra ocupa menos personas a la vez pero bloquea a una persona clave durante dos meses, y un recurso escaso bloqueado es la cola más cara que existe. Que el valor total sea el mismo no las hace equivalentes, porque el coste del retraso se acumula por semana.
:::

:::quiz
p: El equipo planifica el sprint al 100 % de su capacidad y todas las semanas termina con trabajo a medias y fechas incumplidas. ¿Cuál es la causa más probable?
o: El equipo rinde por debajo de lo esperado y hay que apretar más
o: Sin aire en el plan, cada imprevisto espera detrás de todo lo demás y la espera crece de forma no lineal con la ocupación
o: Las estimaciones están mal y hay que estimar con más detalle
a: 2
e: Con la ocupación cerca del 100 %, la espera crece como el cociente entre la ocupación y lo que le falta para el 100 %: al 90 % es nueve veces el tiempo de servicio. Por eso un plan sin holgura no falla por falta de esfuerzo, sino porque cualquier cosa que llegue tiene que esperar a que termine todo lo anterior. Estimar con más detalle reduce la incertidumbre de cada tarea pero no crea capacidad, y apretar más sube la ocupación y empeora la espera.
:::

:::trampa
El «sí, pero después». Un compromiso vago es peor que un no: la iniciativa se queda en la lista, se
vuelve a discutir cada mes y nadie la ha descartado de verdad. Si no se va a hacer, se dice y se
escribe con su condición de revisión; si se va a hacer, se le da un hueco que implica quitar otra
cosa del plan. Las dos respuestas son honestas; la ambigüedad no lo es.
:::

:::nota
Los métodos con nombre (WSJF, CD3, RICE, MoSCoW) no deciden nada por sí solos: son formas de
obligar a que las discusiones sean explícitas. El valor real está en las conversaciones que
provocan al estimar el coste del retraso y al justificar un tamaño, y en que la decisión queda
escrita con su contexto para poder revisarla cuando cambien los datos
([[escribir-un-informe]]).
:::
