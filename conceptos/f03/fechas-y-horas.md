---
id: fechas-y-horas
titulo: Fechas, horas y zonas horarias
fase: 3
nivel: intermedio
rutas: [core, de, ds]
prerequisitos: [tipos-y-estructuras-python, ficheros-y-encoding]
tags: [python, tiempo, zonas-horarias]
resumen: Un instante y una hora local no son lo mismo; datetime, timedelta, UTC y el horario de verano, que dos días al año rompe la cuenta de 24 horas.
fuentes: ["Python Software Foundation (2024), 'datetime — Basic date and time types'", "Eggert y Olson (2024), 'Sources for Time Zone and Daylight Saving Time Data'"]
---

## En una frase

Una fecha y hora puede ser un **instante** (un punto concreto de la línea del tiempo, que es el
mismo en todo el mundo) o una **hora de pared** (lo que marca el reloj de un sitio); `datetime`
maneja las dos, y confundirlas es la causa de casi todos los errores de tiempo.

## La idea

Una videollamada a las 09:00 en Madrid y a las 08:00 en Londres es la misma reunión. La hora de
pared es distinta; el instante es el mismo. Esa distinción, que en la vida diaria se resuelve con
sentido común, es exactamente lo que hay que decirle explícitamente a un programa.

El punto de referencia es **UTC** (la hora del meridiano de Greenwich, sin cambios de hora) y cada
zona horaria es un desfase respecto a él: Madrid va con UTC+1 en invierno y UTC+2 en verano. Con eso
ya tienes la primera regla: guarda los instantes en UTC y pasa a hora local solo para mostrarlos o
para agrupar por día local. Si guardas horas locales en una base de datos, dentro de dos años nadie
sabrá de qué zona eran, y el día en que cambia la hora tendrás dos horas distintas con la misma
etiqueta.

El **horario de verano** es la razón de que un desfase no sea un número fijo. En la Unión Europea el
reloj se adelanta el último domingo de marzo y se atrasa el último domingo de octubre, siempre a la
01:00 UTC. Eso significa tres cosas que se notan en los datos:

1. **Una hora local puede no existir.** El 29 de marzo de 2026, en Madrid, entre las 02:00 y las
   02:59 no hay ningún instante: el reloj saltó de las 02:00 a las 03:00.
2. **Una hora local puede repetirse.** El 25 de octubre de 2026, en Madrid, las 02:30 ocurren dos
   veces, una con UTC+2 y otra con UTC+1. Si guardas «02:30» sin zona, no sabes cuál de las dos es.
3. **Un día local no siempre dura 24 horas.** El 29 de marzo dura 23 horas reales y el 25 de octubre
   dura 25. Restar dos fechas locales que caen en días distintos del cambio de hora da 23 o 25 horas
   sin que nada avise.

Una idea parecida gobierna los **calendarios**, y es la fuente de los errores de facturación: un mes
no tiene una duración fija. Sumar 30 días no es sumar un mes, porque febrero tiene 28 o 29 días, y
un año no tiene 365 días. Por eso existe `timedelta`: representa una **duración** (una cantidad de
tiempo), no una fecha. Y por eso «un día» es ambiguo: puede ser un día de calendario o 24 horas.

Por último, `datetime` distingue entre objetos **ingenuos** (`naive`, sin zona) y **conscientes**
(`aware`, con zona). Un `datetime` sin zona no es un instante: es una hora de pared sin decir de
dónde. Puedes sumarle `timedelta` y formatearlo, pero no puedes convertirlo a otra zona ni
compararlo con uno consciente: Python lanza `TypeError` en lugar de adivinar, y hace bien.

## Definición formal

Un instante se representa con `t_utc`, y su hora de pared en la zona `z` se obtiene sumando el
desfase `Δ` que esa zona tiene **en ese instante**:

:::formula
t_local = t_utc + Δ(z, t_utc)      ·      Δt = t_utc2 − t_utc1
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `t_utc` | El instante, medido en UTC | fecha y hora | La hora local avanza lo mismo: es el mismo reloj con otro cero |
| `t_local` | Lo que marca el reloj en la zona `z` | fecha y hora de pared | No es un instante hasta que se le dice la zona |
| `Δ` | Desfase de la zona frente a UTC | horas, de −12 a +14 | Cada hora de más adelanta el reloj local una hora |
| `z` | La zona horaria, por ejemplo `Europe/Madrid` | nombre de la base tz | Cuanto más al este, mayor es su desfase |
| `Δt` | Duración entre dos instantes | horas o días | Es la única resta de fechas que no depende del calendario |
| `timedelta` | Una duración, no una fecha | días, segundos y microsegundos | Al sumarla a una hora local se avanza en hora de pared, no en tiempo real |
| `días` | Días de calendario | días | 1 día de calendario son 24 horas salvo en los dos días del cambio de hora |
:::

Dos consecuencias que conviene tener escritas:

- **Cambiar de zona no cambia el instante.** `instante.astimezone(madrid)` devuelve otro objeto con
  la misma marca de tiempo y otro `tzinfo`; la comparación `==` entre los dos sigue siendo `True`.
- **`+ timedelta(days=1)` sobre una hora local avanzan un día de calendario, no 24 horas.** Sobre un
  `datetime` consciente, Python mantiene la hora de pared y recalcula el desfase: por eso el 29 de
  marzo de 2026 en Madrid ese «día» son 23 horas reales.

## Ejemplo

El 29 de marzo de 2026 el reloj de Madrid se adelanta a la 01:00 UTC (las 02:00 locales):

```
00:30 UTC  ->  01:30 en Madrid      (todavía UTC+1)
00:59 UTC  ->  01:59 en Madrid
01:00 UTC  ->  03:00 en Madrid      (ya UTC+2; la hora local 02:00-02:59 no existe)
```

Y el 25 de octubre de 2026 se atrasa, también a la 01:00 UTC:

```
00:59 UTC  ->  02:59 en Madrid      (todavía UTC+2)
01:00 UTC  ->  02:00 en Madrid      (ya UTC+1; la hora local 02:00-02:59 ocurre dos veces)
```

Con números redondos: una medida tomada a las **08:00 de la mañana en Madrid en julio** está tomada
a las **06:00 UTC**, porque `Δ` vale 2 en verano. La misma hora de pared en enero son las 07:00 UTC
(`Δ` vale 1). Si tu pipeline guarda «08:00» sin zona y otro día compara con UTC, arrastra un error
de una o dos horas que cambia según el mes, el peor tipo de error posible: el que a veces acierta.

:::figura
fichero: fechas-y-horas-utc-y-horario-de-verano
pie: El panel izquierdo muestra que el desfase de Madrid no es un número fijo sino una escalera con dos saltos al año, así que cualquier conversión que uses un desfase constante se equivoca durante la mitad del año. El panel derecho mide cuánto dura de verdad un día local: 24 horas casi siempre, 23 el domingo de marzo y 25 el de octubre. De ahí salen las dos reglas prácticas: convierte siempre con la zona y nunca cuentes horas restando fechas locales.
fuente: figuras/fechas-y-horas-1.py
:::

## Código

```python verificable
import datetime as dt

inicio = dt.datetime(2026, 3, 1, 9, 0)      # datetime "ingenuo": no dice de que zona es
fin = inicio + dt.timedelta(days=10, hours=4, minutes=30)
print("fin:", fin)                                            # -> 2026-03-11 13:30:00
print("duracion:", fin - inicio)                              # -> 10 days, 4:30:00
print("fecha suelta:", fin.date(), " hora suelta:", fin.time())  # -> 2026-03-11 y 13:30:00
print("formateado:", fin.strftime("%d/%m/%Y %H:%M"))          # -> 11/03/2026 13:30
print("dias hasta el 20 de marzo:", (dt.datetime(2026, 3, 20) - fin).days)   # -> 8
```

:::claves
- `dt.datetime(2026, 3, 1, 9, 0)` es **ingenuo**: no lleva zona. Puedes sumarle `timedelta` y formatearlo, pero no convertirlo a otra zona ni compararlo con un `datetime` consciente, porque Python lanza `TypeError` en vez de suponer que es UTC.
- `fin - inicio` devuelve un `timedelta`, no un número: `10 days, 4:30:00`. Si pides `.days` te da la parte entera de días (**10**, no 10,19) y descarta las horas sin avisar; para el total en segundos está `.total_seconds()`, y para el total en días, `total_seconds() / 86400`. Ojo con qué resta miras: en la última línea del bloque, `20 de marzo − fin`, `.days` vale 8 y el total en días, 8,44.
- `fin.date()` y `fin.time()` devuelven objetos nuevos de tipo `date` y `time`; no son texto. Al imprimirlos se ven en formato ISO (`2026-03-11`), que es el que ordena alfabéticamente igual que cronológicamente.
- `strftime("%d/%m/%Y")` escribe la fecha como texto en formato español. Ojo con la vuelta: `"%m/%d/%Y"` al leer interpretaría `03/11/2026` como el 3 de noviembre, y ese error no da ninguna excepción si el día es menor que 12.
- `dt.datetime(2026, 3, 20) - fin` compara dos fechas ingenuas, que es lo único que puedes hacer con ellas. El orden de los argumentos importa: al revés sale un `timedelta` negativo.
:::

```python verificable
import datetime as dt
from zoneinfo import ZoneInfo

madrid = ZoneInfo("Europe/Madrid")
utc = dt.timezone.utc

instante = dt.datetime(2026, 7, 15, 6, 0, tzinfo=utc)      # un punto del tiempo
en_madrid = instante.astimezone(madrid)                    # el mismo punto, otro reloj
print("UTC:   ", instante.strftime("%Y-%m-%d %H:%M %Z"))   # -> 2026-07-15 06:00 UTC
print("Madrid:", en_madrid.strftime("%Y-%m-%d %H:%M %Z"))  # -> 2026-07-15 08:00 CEST
print("desfase de Madrid en julio:", en_madrid.utcoffset())  # -> 2:00:00

medianoche = dt.datetime(2026, 3, 29, tzinfo=madrid)       # dia del cambio de hora
dia_siguiente = medianoche + dt.timedelta(days=1)          # +1 dia de calendario
print("horas reales del 29 de marzo:",
      dia_siguiente.astimezone(utc) - medianoche.astimezone(utc))          # -> 23:00:00
print("mismo instante con dos nombres:", medianoche == medianoche.astimezone(utc))  # -> True
```

```python ilustrativo
# Guardar y leer: el instante en UTC, la zona aparte
registro = {"medido_en": instante.astimezone(utc).isoformat(), "zona": "Europe/Madrid"}
# -> {"medido_en": "2026-07-15T06:00:00+00:00", "zona": "Europe/Madrid"}

# Un log o un CSV con este formato se puede volver a leer sin ambiguedad:
#   dt.datetime.fromisoformat("2026-07-15T06:00:00+00:00")
# Lo que NO se guarda es "2026-07-15 08:00" a secas: no dice de que reloj salio.
```

## Errores típicos

- **Restar una fecha local de una fecha UTC.** El resultado sale desplazado una o dos horas, según
  el mes, y ningún error te avisa. Pasa cuando una parte del pipeline trabaja en UTC y otra con
  `datetime.now()`, que devuelve la hora local de la máquina. Convierte todo a UTC antes de restar;
  restar horas locales mide tiempo de pared, no tiempo transcurrido, porque entre las dos fechas
  puede haber caído un cambio de hora.
- **Guardar horas locales sin zona.** «2026-10-25 02:30» en Madrid ocurre dos veces ese día y no hay
  forma de saber a cuál te refieres. Guarda el instante en UTC (o el texto ISO con el desfase,
  `2026-10-25T02:30:00+02:00`) y la zona solo si la necesitas para mostrar.
- **Usar un desfase fijo.** `t_utc = t_local - 1` funciona en enero y falla en julio, y encima
  funciona en Londres y falla en Madrid. El desfase es una función de la zona y del instante: se
  pregunta a `zoneinfo`, no se escribe a mano.
- **Sumar `timedelta(days=30)` para «un mes».** Marzo tiene 31 días y febrero 28. Para sumar meses o
  años de calendario hay que decidir qué hacer con los días que no existen (el 31 de enero más un
  mes) y hacerlo explícitamente.
- **Comparar un `datetime` ingenuo con uno consciente.** Lanza
  `TypeError: can't compare offset-naive and offset-aware datetimes`. Es un favor: la alternativa
  sería un resultado silenciosamente equivocado.
- **Usar `datetime.utcnow()`.** Devuelve un `datetime` **ingenuo** con la hora UTC dentro, que es la
  peor combinación: parece UTC pero no lo dice. Usa `datetime.now(dt.timezone.utc)`.

:::practica
enunciado: Un log guarda la marca «2026-03-29 01:30:00» y se sabe que es hora local de Madrid. ¿A qué instante UTC corresponde? Y una medida tomada a las 08:00 locales del 15 de julio de 2026, ¿a qué instante UTC corresponde? Di también cuántas horas reales tiene el 25 de octubre de 2026 en Madrid.
pista: Mira si el instante cae antes o después de la 01:00 UTC del día del cambio, y usa el desfase que toca en cada caso.
solucion: El 29 de marzo de 2026 el cambio ocurre a la 01:00 UTC, así que la 01:30 local es todavía UTC+1: el instante es la 00:30 UTC de ese mismo día. Las 08:00 locales del 15 de julio llevan UTC+2, así que son las 06:00 UTC. El 25 de octubre de 2026 el día local dura 25 horas reales, porque a las 03:00 locales (01:00 UTC) el reloj se atrasa a las 02:00 y esa hora (02:00–02:59) se repite dos veces.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre un datetime ingenuo y uno consciente?
o: El ingenuo no guarda segundos, el consciente sí
o: El ingenuo no lleva zona, así que no es un instante y no se puede convertir a otra zona
o: El consciente solo existe en UTC, y el ingenuo en cualquier zona
a: 2
e: «Ingenuo» (naive) significa que el objeto no dice a qué zona pertenece: es una hora de pared sin dueño. Solo sirve para sumar duraciones y formatear. Un datetime consciente (aware) lleva su tzinfo y representa un instante, así que se puede convertir con astimezone y comparar con otros instantes. Los segundos los guardan los dos.
:::

:::quiz
p: Tienes marcas de tiempo en hora local de Madrid y quieres calcular cuánto tiempo pasa entre dos de ellas. ¿Qué haces?
o: Restarlas directamente y quedarte con los días
o: Convertir las dos a UTC y restar, porque entre ellas puede haber caído un cambio de hora
o: Sumar una hora a todas para que estén en UTC
a: 2
e: Restar horas locales mide tiempo de pared, no tiempo real: si entre las dos marcas cae el último domingo de marzo, el resultado se queda corto una hora, y si cae el de octubre, se pasa una hora. Convirtiendo a UTC con la zona correcta, la resta es tiempo transcurrido de verdad. Sumar una hora fija funciona solo en invierno.
:::

:::quiz
p: Para guardar en una base de datos la hora a la que un cliente hizo un pedido, ¿qué opción es la menos mala?
o: La hora local del servidor, que es la que ve el negocio
o: El instante en UTC, y la zona del cliente aparte si hace falta mostrarla
o: El instante convertido antes a la hora local del cliente, para no tener que convertir al leerlo
a: 2
e: El instante en UTC no es ambiguo y no depende de dónde esté el servidor ni de si ese día cambia la hora; la zona del cliente se guarda aparte como dato, no como parte de la fecha. Convertir a la hora local antes de guardar es justo lo que hay que evitar: esa hora puede existir dos veces cada octubre y no se puede reconstruir el instante a partir de ella.
:::
