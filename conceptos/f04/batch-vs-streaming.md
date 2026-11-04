---
id: batch-vs-streaming
titulo: Procesamiento por lotes y en flujo
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [etl-vs-elt, ciclo-de-vida-del-dato]
tags: [lotes, streaming, latencia, arquitectura, coste]
resumen: Procesar cada hora o procesar cada evento: la decisión se toma con la latencia que la decisión tolera, el coste y la complejidad, no con lo moderna que suene.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', caps. 10 y 11", "Reis & Housley (2022), 'Fundamentals of Data Engineering', cap. 8"]
---

## En una frase

Un proceso por lotes espera y trabaja con un bloque de datos acumulados; uno en flujo trata cada
evento cuando llega. La diferencia práctica es cuánto retraso aceptas, y el precio se paga en
complejidad.

## La idea

Piensa en la colada. Poner una lavadora cuando hay ropa suficiente es eficiente: un ciclo lleno,
poco detergente por camiseta y te puedes ir a hacer otra cosa. Lavar cada camiseta en cuanto te
la quitas da ropa limpia al instante, pero gastas un ciclo por prenda y tienes que estar
pendiente del aparato todo el día.

El procesamiento por lotes no es «lo antiguo»: es lo que hace la inmensa mayoría de las empresas.
Un informe de ventas que se calcula a las 3:00 y está listo a las 7:00 sirve para todas las
decisiones de esa jornada. Nadie va a tomar una decisión distinta porque el dato tenga tres horas
en vez de tres segundos.

La pregunta correcta, por tanto, no es «¿necesito tiempo real?» sino **«¿qué decisión cambia si
el dato llega quince minutos tarde?»**. Si la respuesta es «ninguna», el lote gana y no hay nada
que discutir. Si la respuesta es «bloqueamos la tarjeta del cliente», entonces sí, necesitas
flujo.

Lo que de verdad cuesta el flujo no es el motor, es todo lo que arrastra:

- **Estado permanente.** Un proceso por lotes arranca, lee, calcula, escribe y muere. Uno en
  flujo está vivo siempre: hay que desplegarlo, vigilarlo, actualizarlo sin perder datos y
  decidir qué pasa cuando se reinicia.
- **Orden y desorden.** En un lote, los datos ya están todos en la mesa. En flujo, los eventos
  llegan desordenados, con retrasos distintos y a veces dos veces ([[streaming-tiempo-real]]).
- **Reintentos.** Si el lote falla, lo vuelves a lanzar. Si el flujo falla a mitad, tienes que
  saber exactamente por dónde ibas ([[idempotencia-y-reintentos]]).
- **Un sistema de mensajería en medio.** Casi siempre un intermediario que hay que operar
  ([[kafka-y-colas]]).

Y hay una tercera opción que casi nadie considera antes de complicarse: **bajar la frecuencia del
lote**. Pasar de un proceso diario a uno cada quince minutos da la mayor parte del beneficio y
cuesta una fracción de lo que cuesta montar flujo. Es el primer experimento que hay que hacer,
no el último.

La frontera entre los dos mundos es difusa: los motores de flujo modernos trabajan con
micro-lotes (agrupan los eventos que han llegado en una fracción de segundo), así que en la
práctica hay un continuo entre «cada 24 horas» y «por evento». Las arquitecturas lambda y kappa
son dos formas conocidas de combinar ambos mundos ([[lambda-y-kappa]]).

## Definición formal

Sea `λ` la tasa de llegada de eventos, en eventos por segundo; `B` el tamaño del lote, en eventos
por ejecución; y `f` la frecuencia del lote, en ejecuciones por hora.

- **Rendimiento (throughput):** `B · f` eventos por hora. Tiene que ser mayor o igual que
  `λ · 3600` o el sistema se retrasa sin remedio.
- **Latencia máxima** de un evento, en horas:

:::formula
latencia_máxima = 1 / f
:::

Un evento que llega justo después de que arranque una ejecución espera un ciclo entero. Con
`f = 1` la latencia máxima es 1 hora; con `f = 12` (cada cinco minutos) es de 5 minutos.

- **Coste por hora**, con `c0` el coste fijo de cada ejecución (arrancar el motor, planificar,
  pagar el mínimo facturable) y `c1` el coste por evento procesado:

:::formula
coste_hora = f · c0 + c1 · λ · 3600
:::

Fíjate en lo importante: **el coste fijo se multiplica por `f`**, mientras que el variable no
depende de la frecuencia. Duplicar la frecuencia de ejecución duplica la parte fija, proceses los
datos que proceses.

- **Frescura** de una tabla: la antigüedad del dato más reciente que contiene. No es lo mismo que
  la latencia, que es lo que tarda un evento en aparecer. Una tabla puede tener latencia de un
  segundo y frescura de tres días si un reintento lleva tres días fallando en silencio.

## Ejemplo

Una tienda online recibe `λ = 3.000` eventos por segundo, es decir
`3.000 × 3.600 = 10.800.000` eventos por hora. El modelo de coste, con cifras inventadas pero
coherentes: `c0 = 0,05 €` por ejecución del trabajo y `c1 = 0,0000004 €` por evento, o sea
0,40 € por millón.

Coste variable por hora: `10.800.000 × 0,0000004 = 4,32 €`. Ese trozo no cambia con la
frecuencia. El coste fijo, sí:

```
frecuencia    latencia maxima    coste fijo/h    coste total/h
cada hora     60 min             0,05 €          4,37 €
cada 15 min   15 min             0,20 €          4,52 €
cada 5 min     5 min             0,60 €          4,92 €
cada minuto    1 min             3,00 €          7,32 €
```

La latencia mejora de 60 minutos a 1 minuto: un factor de 60. El coste sube de 4,37 € a 7,32 €:
un 67 %. Y eso sin contar la complejidad, que no aparece en la factura.

## Código

```python verificable
# La misma carga a distintas frecuencias: cuanto cuesta la frescura.
eventos_por_hora = 10_800_000        # 3.000 eventos por segundo
coste_arranque = 0.05                # euros por ejecucion del trabajo
coste_por_evento = 0.0000004         # euros por evento (0,40 EUR por millon)

variable = eventos_por_hora * coste_por_evento
print(f"{'frecuencia':>12} {'latencia':>9} {'coste/h':>8}")
for nombre, f in [("cada hora", 1), ("cada 15 min", 4), ("cada 5 min", 12), ("cada minuto", 60)]:
    print(f"{nombre:>12} {60 / f:>7.0f} m {f * coste_arranque + variable:>7.2f} EUR")

print("coste variable por hora:", round(variable, 2))   # -> coste variable por hora: 4.32
print("arranques al dia a 1 min:", 60 * 24)             # -> arranques al dia a 1 min: 1440
```

```python verificable
from datetime import datetime

# Por que el lote atribuye mal los eventos que llegan tarde: el corte es una frontera dura.
corte = datetime(2024, 3, 1, 10, 0)          # el lote de las 10:00 cierra a las 10:00 en punto
ocurridos = [datetime(2024, 3, 1, 9, 58), datetime(2024, 3, 1, 9, 59), datetime(2024, 3, 1, 9, 55)]
llegadas = [datetime(2024, 3, 1, 9, 59, 10), datetime(2024, 3, 1, 9, 59, 40), datetime(2024, 3, 1, 10, 3)]

en_el_lote = sum(1 for t in llegadas if t < corte)
print("eventos en el lote de las 10:00:", en_el_lote)                    # -> eventos en el lote de las 10:00: 2
print("eventos que van al lote siguiente:", len(llegadas) - en_el_lote)  # -> eventos que van al lote siguiente: 1

# El tercero ocurrio a las 9:55, pero llegara a las 10:03 y se contara en la hora siguiente.
retraso = (llegadas[2] - ocurridos[2]).total_seconds()
print("retraso en segundos:", int(retraso))                              # -> retraso en segundos: 480
```

## Errores típicos

- **Pedir flujo «porque es lo que se lleva».** La única pregunta válida es qué decisión cambia
  con el dato en la mano. Si la reunión donde se usa el dato es a las 9:00, un proceso a las 6:00
  es equivalente a uno en tiempo real y cuesta una fracción.
- **Creer que subir la frecuencia es gratis.** Cada ejecución paga un arranque: pasar de diario a
  cada minuto son 1.440 arranques al día en vez de 1, y la parte variable del coste no baja.
- **Confundir latencia con frescura.** Puedes tener un flujo que entrega cada evento en un segundo
  y una tabla con datos de hace tres días, porque un reintento lleva días fallando. La latencia
  mide la entrega; la frescura, lo que hay dentro.
- **Suponer que el flujo elimina el reproceso.** Tarde o temprano habrá que rehacer un periodo
  entero, así que necesitas el crudo guardado y un proceso que pueda ejecutarse dos veces sin
  duplicar ([[backfill-y-reproceso]]). Sin eso, el flujo solo sirve hasta el primer incidente.
- **Medir el éxito por la latencia y no por el uso.** Un panel que se refresca cada segundo y
  nadie mira consume más que el informe diario que sí se lee. Mide consultas y decisiones, no
  segundos.
- **Mantener dos tuberías con lógica distinta**, una por lotes y otra en flujo. Acaban dando dos
  números para la misma métrica y nadie sabe cuál es el bueno. Es exactamente el problema que
  atacan las arquitecturas lambda y kappa ([[lambda-y-kappa]]).

## Comprueba que lo sabes

:::quiz
p: ¿Qué decides primero al elegir entre proceso por lotes y proceso en flujo?
o: Que tecnología usa el resto de la empresa
o: Cuanto retraso puede tolerar la decisión que se va a tomar con el dato
o: Si el volumen supera el millón de eventos al día
a: 2
e: La latencia tolerable la fija el uso, no el volumen ni la moda. Con el requisito de latencia claro, el volumen solo decide si el motor elegido aguanta; sin él, cualquier discusión técnica es prematura.
:::

:::quiz
p: Pasas un proceso de diario a cada quince minutos. ¿Qué ocurre?
o: El coste fijo de arranque se multiplica por 96 y la latencia máxima baja de 24 horas a 15 minutos
o: No cambia el coste, solo la latencia
o: El coste baja, porque cada ejecución procesa menos datos
a: 1
e: Cada ejecución paga su arranque, así que multiplicar la frecuencia multiplica la parte fija. La parte variable depende del total de eventos, no de cómo los agrupes. Por eso conviene subir la frecuencia hasta donde haga falta y ni un paso más.
:::

:::aviso
Antes de montar un sistema de flujo, prueba a bajar la frecuencia del lote. Pasar de diario a cada
quince minutos da casi todo el beneficio de la frescura sin añadir un intermediario de mensajería,
sin estado permanente y sin eventos desordenados que resolver.
:::
