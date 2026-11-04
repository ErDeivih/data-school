---
id: incidentes-y-postmortem
titulo: Incidentes y postmortem
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [logging-y-trazas, metricas-y-alertas, errores-y-depuracion, git-avanzado]
tags: [operacion, incidentes, postmortem, fiabilidad]
resumen: Qué hacer cuando algo se rompe en producción: severidades, runbook, mitigar antes de diagnosticar y un postmortem sin culpa con acciones que se cierran.
fuentes: ["Beyer y otros (2016), 'Site Reliability Engineering'", "Limoncelli y otros (2014), 'The Practice of Cloud System Administration'"]
---

## En una frase

Un incidente no se arregla pensando más rápido: se arregla con un nivel de gravedad que decide
quién manda, un runbook que dice qué tocar, la disciplina de **restaurar el servicio antes de
entender qué pasó** y un postmortem sin culpa cuyas acciones se cierran o se borran.

## La idea

A las 03:40 la tasa de error de la pasarela de pagos pasa del 0,4 % al 38 %. Hay dos
comportamientos posibles y solo uno sirve.

El primero es el del detective: abrir el editor, leer los registros, formar una hipótesis sobre
qué consulta SQL se ha degradado, escribir un parche, probarlo en local. A las 05:20, con suerte,
hay una hipótesis y ninguna certeza. Mientras tanto, cada minuto entran pedidos que fallan.

El segundo es el del bombero: **primero apagar el fuego, después buscar la cerilla**. A las 03:43
se revierte el despliegue de la tarde y la tasa de error vuelve al 0,5 %. A las 03:44 el servicio
funciona y el sistema deja de sangrar. A las 10:00, con calma y con café, se investiga si la
causa era aquel despliegue, un cambio de configuración en la base de datos o un proveedor externo.
Si resulta que no era el despliegue, se vuelve a poner y se sigue buscando; el tiempo perdido han
sido cuarenta minutos de una hipótesis, no dos horas de servicio caído.

La razón de que esto casi nunca se haga bien no es técnica, sino de incentivos: **diagnosticar es más
divertido que mitigar**. Un ingeniero con curiosidad prefiere entender el fallo, y en ese momento
el sistema está pidiendo otra cosa. La organización lo arregla con una regla explícita en el
runbook: durante un incidente de gravedad alta, revertir o aislar es la primera acción, y la
investigación se abre después, en frío, cuando ya no hay nadie perdiendo dinero.

**Severidades.** La gravedad no mide lo interesante que es el problema, mide cuánto duele. Sirve
para decidir tres cosas en treinta segundos: a quién se despierta, quién tiene la autoridad para
decidir y cuánto puede durar antes de escalar a la persona de guardia de más arriba.

- **SEV1** — el servicio principal está caído o se están corrompiendo datos. Se despierta a quien
  haga falta, incluido el responsable técnico. Comunicación cada 30 minutos.
- **SEV2** — una función importante no funciona o hay degradación severa, y hay clientes
  afectados. Se avisa a quien está de guardia; comunicación cada hora.
- **SEV3** — degradación menor o molestia con solución conocida. Se arregla en horario laboral.
- **SEV4** — cosmético, documentación, deuda técnica. Es una tarea, no un incidente.

La regla es que **quien está de guardia declara la gravedad, y equivocarse por arriba es barato**.
Subir un SEV3 a SEV2 cuesta una llamada de más; bajarlo cuesta una hora de caída que nadie estaba
mirando. Y una vez declarada, la severidad solo la baja quien la subió.

**Papeles.** En un incidente serio hacen falta tres sombreros. En un equipo pequeño la misma
persona lleva dos, pero nunca los dos que se estorban:

- **Comandante del incidente** — decide y coordina. No toca el teclado ni depura: su trabajo es
  que haya una sola persona cambiando cosas en producción y que la información fluya.
- **Operador** — ejecuta los cambios, sigue el runbook y dice en voz alta lo que va a hacer antes
  de hacerlo.
- **Responsable de comunicación** — escribe el estado para quien no está en la llamada: qué
  sabemos, qué hemos hecho, qué no sabemos y cuándo daremos la siguiente actualización.

**El runbook.** Es el documento que convierte «sé arreglarlo» en «cualquiera de guardia lo
arregla a las cuatro de la mañana». Es una receta con comandos exactos, el resultado que se espera de cada uno y el camino de
vuelta, y no un manual de arquitectura.

- Cómo se confirma que el problema es eso y no otra cosa.
- La mitigación, paso a paso, con el comando literal y pegable.
- Cómo se sabe que ha funcionado (qué panel, qué métrica, qué valor).
- Cómo se revierte la mitigación si empeora.
- A quién se avisa y con qué texto, ya redactado.

Un runbook que no se ha recorrido en una prueba sigue siendo un borrador. La forma de
mantenerlo vivo es obligatorio: **ninguna alerta se cierra sin que su runbook se haya seguido**,
y cada vez que un paso no cuadra con la realidad se corrige en ese momento, no después.

## Definición formal

Un incidente es un intervalo temporal con hitos. Con `t_i` el instante de cada hito:

:::formula
MTTD = t_deteccion − t_inicio        (tiempo hasta detectar)
MTTM = t_mitigacion − t_deteccion    (tiempo hasta mitigar)
MTTR = t_restauracion − t_deteccion  (tiempo hasta restaurar)
:::

Y la duración que sufre el usuario, que es la única cifra que ve quien paga:

:::formula
impacto = t_restauracion − t_inicio = MTTD + (t_restauracion − t_deteccion)
:::

- `t_inicio` — instante en que el sistema empezó a comportarse mal. Casi nunca se conoce con
  precisión: se estima a partir de la primera petición afectada en los registros.
- `t_deteccion` — instante en que un humano lo supo. Si lo dice un cliente, `MTTD` incluye todo
  el rato que el sistema estuvo roto sin que nadie mirara.
- `t_mitigacion` — instante en que el impacto sobre los usuarios deja de crecer. No es que esté
  arreglado: es que ya no hace daño.
- `t_restauracion` — instante en que el servicio recupera su comportamiento normal, con la causa
  entendida o no.
- `MTTR` — medio tiempo de reparación. Se mide **desde la detección**: lo que no se ve, no se
  puede arreglar. Un `MTTD` grande se corrige con mejores alertas ([[metricas-y-alertas]]), no
  con más manos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `t_inicio` | Instante en que el sistema empezó a fallar de verdad | marca de tiempo | No es una palanca: es el dato que hay que reconstruir después con los registros. Si lo estimas mal, todas las duraciones salen mal |
| `t_deteccion` | Instante en que un humano se enteró | marca de tiempo | Es la palanca más rentable: pasar de 40 minutos a 2 es bajar el impacto sin tocar el código. Lo que se rompe y no se alerta ([[metricas-y-alertas]]) se descubre por el cliente |
| `t_mitigacion` | Instante en que el daño deja de crecer | marca de tiempo | Depende de la decisión de mitigar antes de entender. Un equipo que diagnostica primero tiene este hito una o dos horas más tarde con el mismo arreglo final |
| `t_restauracion` | Instante en que el servicio vuelve a la normalidad | marca de tiempo | Puede llegar días después si la causa es de fondo. Baja el `MTTR` publicado, pero para el usuario el incidente acabó en la mitigación |
| `MTTD` | Lo que tarda el sistema en avisar | minutos u horas | Es el tramo más barato de recortar y el que más impacto tiene: reduce el `impacto` en la misma cantidad |
| `MTTM` | Lo que tarda el equipo en parar el daño desde que lo sabe | minutos | Se recorta con runbooks y con revertir sin miedo, no con más gente en la llamada |
| `MTTR` | Lo que tarda el servicio en volver, contado desde la detección | minutos u horas | Es la cifra que se publica. Se puede mejorar por dos caminos distintos: detectar antes (baja el impacto) o mitigar antes (baja el impacto, no el `MTTR`) |
| `impacto` | Tiempo total que el usuario estuvo sufriendo el fallo | minutos u horas | Es la cifra honesta cuando alguien pregunta «¿cuánto estuvimos caídos?»: incluye el rato en que nadie sabía nada |
:::

**El postmortem sin culpa.** Un postmortem es un documento escrito en los días siguientes, no un
juicio. El criterio para saber si es sin culpa es mecánico: **si el documento contiene el nombre
de una persona como causa, está mal escrito**. Las personas no son causas, sino el punto donde un
sistema con incentivos, prisas y controles flojos deja pasar un error. «Juan desplegó el cambio
sin probar» no sirve para nada, porque Juan sigue ahí y mañana desplegará otro cambio. «El
despliegue no exigía prueba previa y el botón de revertir estaba detrás de dos menús» sí sirve:
son dos cosas que se pueden cambiar hoy.

La estructura mínima de un postmortem útil, en este orden: **impacto** (quién y cuánto), **línea
de tiempo** (con marcas de tiempo reales, incluidos los callejones sin salida), **qué lo
contribuyó** (en plural: casi nunca hay una sola causa), **qué funcionó bien** (para no
desmontarlo en el siguiente cambio), **qué nos engañó** (la hipótesis falsa que se persiguió) y
**acciones**.

**Las acciones son el único apartado que vale algo.** Un postmortem con buenas intenciones y sin
acciones cerradas es un ejercicio de terapia. Cada acción tiene que cumplir cuatro condiciones:

- **Concreta**: «mejorar la monitorización» no es una acción; «añadir alerta de tasa de error
  por encima del 2 % durante 5 minutos en la pasarela» lo es.
- **Con dueño**: una persona, no un equipo. «El equipo de plataforma» es un buzón donde nadie
  responde.
- **Con fecha**: una fecha límite, aunque sea provisional.
- **Verificable**: se puede comprobar si está hecha sin preguntarle a nadie.

Y la condición que se olvida: **una acción sin cerrar caduca**. Si a los treinta días no se ha
hecho, hay dos salidas honestas: reprogramarla con una razón, o borrarla y admitir que no se va a
hacer. Lo que no vale es dejarla en la lista para siempre. Un tablero con 300 acciones abiertas de
los últimos tres años es igual que un tablero sin acciones: nadie lo mira.

:::formula
ratio_de_cierre = acciones_cerradas / acciones_totales
:::

Hay un caso aparte que merece mención: **el incidente que ya ocurrió antes**. Si dos incidentes
comparten el mismo factor contribuyente, forman un patrón y no dos incidentes, y el postmortem
del segundo es en realidad una pregunta incómoda sobre por qué la acción del primero no se cerró.
Ese es el motivo real de llevar acciones con fecha.

## Ejemplo

Un incidente real, con los tiempos tal como se reconstruyeron después:

| Hora | Qué pasa |
| --- | --- |
| 02:55 | Se despliega la versión 412 del servicio de pagos |
| 03:02 | La tasa de error de pagos sube del 0,4 % al 38 % (`t_inicio`) |
| 03:05 | La alerta de tasa de error se dispara; alguien de guardia la ve (`t_deteccion`) |
| 03:08 | Se declara SEV2 y se abre la llamada |
| 03:40 | Se revierte a la versión 411; la tasa de error vuelve al 0,5 % (`t_mitigacion`) |
| 04:10 | Se confirma con métricas y registros que el servicio está estable (`t_restauracion`) |

Los números de la fórmula:

- `MTTD` = 03:02 → 03:05 = **3 minutos**.
- `MTTM` = 03:05 → 03:40 = **35 minutos**.
- `MTTR` = 03:05 → 04:10 = **65 minutos**.
- `impacto` = 03:02 → 04:10 = **68 minutos** de peticiones fallando.

Fíjate en la diferencia entre `MTTR` (65) e `impacto` (68): tres minutos. En este caso el equipo
detectó rápido. Ese mismo incidente con un `MTTD` de 40 minutos, que es lo normal cuando la
alerta no existe, habría dado un impacto de 105 minutos con el mismo trabajo técnico. **La
alerta valía más que cualquier optimización del código de pagos.**

Y en la línea de tiempo hay un detalle que casi siempre se omite en los postmortem: entre 03:08 y
03:40 alguien pasó veinte minutos leyendo registros buscando la consulta lenta. No la había.
Mitigar primero (revertir) a las 03:10 habría dejado el impacto en 8 minutos en vez de 68, y la
investigación posterior habría encontrado la causa igual, con la diferencia de que a las 03:10 ya
no había clientes perdiendo pagos. Ese es el aprendizaje que se escribe en el postmortem, y por
eso la acción no es «leer los registros más rápido» sino «en SEV1 y SEV2, revertir el último
cambio antes de abrir el editor».

:::figura
fichero: incidentes-linea-de-tiempo
pie: Arriba, la línea de tiempo del incidente: los 3 minutos que se tarda en detectar (MTTD), los 35 que se tarda en parar el daño desde que se sabe (MTTM) y los 68 minutos que estuvo el usuario sufriendo el fallo. La franja roja empieza en el fallo real, no en la alerta: ese trozo es el que paga el cliente. Abajo, el mismo fallo declarado SEV3, sin alerta y arreglado a lo largo de la mañana: el tramo oscuro, el que hace daño, pasa de 38 a 104 minutos, y el tramo claro es trabajo de fondo que ya no rompe nada.
fuente: figuras/incidentes-y-postmortem-1.py
:::

## Código

```python verificable
from datetime import datetime

# Hitos del incidente: se reconstruyen DESPUES, a partir de alertas y registros.
def t(hhmm):
    return datetime.strptime("2026-03-14 " + hhmm, "%Y-%m-%d %H:%M")

inicio, deteccion, mitigacion, restauracion = t("03:02"), t("03:05"), t("03:40"), t("04:10")

def minutos(a, b):
    # total_seconds() es un float con los segundos enteros y los microsegundos aparte: aqui no
    # hay microsegundos, pero dividir y convertir a int evita imprimir "65.0" mas adelante.
    return int((b - a).total_seconds() / 60)

print("MTTD  minutos:", minutos(inicio, deteccion))       # -> 3
print("MTTM  minutos:", minutos(deteccion, mitigacion))   # -> 35
print("MTTR  minutos:", minutos(deteccion, restauracion)) # -> 65
print("impacto usuarios:", minutos(inicio, restauracion), "minutos")  # -> 68
```

```python verificable
# Que se despierta a las cuatro de la manana depende de la gravedad, no de lo interesante
# que sea el fallo. Las reglas se escriben ANTES, para no discutirlas con el sistema caido.
ESCALADO = {
    #         a quien se avisa        comunicacion  plazo de escalada
    "SEV1": ("guardia + responsable", "30 min", "15 min"),
    "SEV2": ("guardia",               "1 h",    "1 h"),
    "SEV3": ("horario laboral",       "fin de dia", "no"),
    "SEV4": ("tarea",                 "no",     "no"),
}

def clasificar(servicio_principal, usuarios_afectados, hay_perdida_de_datos):
    # El orden de las comprobaciones importa: la primera condicion que se cumple manda.
    if servicio_principal or hay_perdida_de_datos:
        return "SEV1"
    if usuarios_afectados >= 100:
        return "SEV2"
    if usuarios_afectados > 0:
        return "SEV3"
    return "SEV4"

casos = [
    ("pagos caido", True, 5000, False),
    ("informes lentos", False, 300, False),
    ("un cliente sin acceso", False, 1, False),
    ("error de datos corregido", False, 0, True),
]
for nombre, principal, usuarios, datos in casos:
    sev = clasificar(principal, usuarios, datos)
    a_quien, cada, plazo = ESCALADO[sev]
    print(f"{nombre:28} {sev}  avisar: {a_quien:22} cada {cada}")
```

```python verificable
# Registro de acciones de un postmortem: con dueño, con fecha y sin cierres regalados.
acciones = [
    {"id": 1, "que": "revertir el ultimo despliegue antes de depurar", "dueno": "ana", "abierta": 4},
    {"id": 2, "que": "alerta de tasa de error en la pasarela",          "dueno": "luis", "abierta": 12},
    {"id": 3, "que": "boton de revertir en el primer nivel del panel",  "dueno": "ana", "abierta": 45},
]

def estado(a, limite=30):
    # Una accion sin cerrar no se queda abierta para siempre: caduca.
    if not a["abierta"]:
        return "cerrada"
    return "caducada: reprogramar o borrar" if a["abierta"] > limite else "abierta"

abiertas = [a for a in acciones if not a["abierta"]]
# any() se para en el primer True: sirve para preguntar "¿hay alguna...?" sin recorrer todo.
sin_dueno = any(not a["dueno"] for a in acciones)

print("acciones totales:", len(acciones))          # -> 3
print("cerradas:", len(abiertas))                  # -> 0
print("hay acciones sin dueno:", sin_dueno)        # -> False
for a in acciones:
    print(f"  #{a['id']} {estado(a):32} {a['que']}")
# -> el #3 sale "caducada: reprogramar o borrar": 45 dias sin cerrar no es una accion, es una
#    intencion. Se reprograma con una fecha nueva o se borra y se dice en voz alta.
```

## Errores típicos

- **Diagnosticar antes de mitigar.** Es el error número uno y el más caro, porque es el que
  apetece. Con el servicio caído, revertir o aislar primero; la causa se busca después, en frío y
  sin nadie perdiendo dinero. Si la hipótesis era falsa, has perdido veinte minutos de
  diagnóstico, no dos horas de caída.
- **No declarar gravedad, o declararla a la baja.** Sin severidad no hay reglas de aviso ni
  autoridad para decidir, y el incidente se convierte en una conversación. Equivocarse por arriba
  cuesta una llamada; por abajo, una hora de caída silenciosa.
- **Confundir mitigar con arreglar.** Bajar la tasa de error al 0,5 % revirtiendo no es entender
  nada: es cerrar la hemorragia. Si el incidente se da por cerrado ahí, el mismo fallo vuelve a
  los dos meses. La causa se investiga **siempre**, aunque el servicio ya funcione.
- **Un postmortem con nombres propios.** «Fue un error humano de Juan» cierra el documento y no
  arregla nada: Juan sigue en el equipo y el sistema sigue dejando pasar el mismo error. Se
  escriben los factores contribuyentes del sistema: prueba que no se exige, botón de revertir
  escondido, alerta que no existe.
- **Acciones sin dueño o sin fecha.** Una acción que dice «mejorar la observabilidad» y la lleva
  «el equipo» es una acción que no se va a hacer. Persona concreta, texto concreto y fecha, o no
  es una acción.
- **Acumular acciones abiertas para siempre.** Una lista de 60 acciones abiertas desde hace dos
  años no es un plan: es un cementerio. Cada treinta días se revisa, se reprograma lo que sigue
  teniendo sentido y se borra lo que no, diciéndolo.
- **Escribir el runbook después del incidente y no probarlo nunca.** Un runbook sin recorrer es
  una hipótesis. Se valida en un ensayo o en el siguiente incidente, corrigiendo los pasos que no
  cuadran en el momento.
- **Investigar con los mismos datos que fallaron.** Si el problema fue una métrica mal calculada o
  un registro mal formado, mirar solo esa fuente lleva a la conclusión equivocada. Se contrasta
  con otra señal: registros de acceso, trazas ([[logging-y-trazas]]) o el propio panel de negocio.

## Comprueba que lo sabes

:::practica
enunciado: Un incidente se detecta a las 09:12 por una alerta, se mitiga a las 09:47 revirtiendo un cambio de configuración y se restaura a las 11:30. Los registros muestran que las primeras peticiones afectadas son de las 08:55. Calcula `MTTD`, `MTTM`, `MTTR` e impacto, y di qué acción atacaría el mayor de los cuatro.
pista: El `MTTR` se cuenta desde la detección; el impacto, desde el inicio real del fallo.
solucion: `MTTD` = 08:55 → 09:12 = 17 minutos. `MTTM` = 09:12 → 09:47 = 35 minutos. `MTTR` = 09:12 → 11:30 = 138 minutos. Impacto = 08:55 → 11:30 = 155 minutos. El mayor es el `MTTR`, pero no se arregla con prisa: se descompone. Los 43 minutos entre mitigar (09:47) y restaurar (11:30) son trabajo de fondo, no daño nuevo: lo que sufría el usuario eran 52 minutos. La acción rentable es bajar el `MTTM`: si se hubiera revertido a las 09:20, el impacto habría sido de 25 minutos en vez de 155. Segunda acción: revisar por qué el sistema tardó 17 minutos en detectar un fallo que empezó a las 08:55.
:::

:::quiz
p: Son las 03:20, el servicio está caído y el despliegue de las 03:00 es el principal sospechoso. ¿Qué haces primero?
o: Revisar los registros del despliegue para confirmar que la causa es esa
o: Revertir el despliegue y comprobar si el servicio se recupera
o: Avisar a todo el equipo y esperar a que llegue alguien con más contexto
a: 2
e: Con el servicio caído, la primera acción es parar el daño. Revertir es rápido, reversible y comprueba la hipótesis al mismo tiempo: si el servicio se recupera, la causa era esa; si no, se vuelve a poner y se sigue buscando. Leer registros primero cambia minutos de diagnóstico por decenas de minutos de caída.
:::

:::quiz
p: Un postmortem concluye que la causa fue que una ingeniera aprobó un cambio sin revisar. ¿Qué falla en ese postmortem?
o: Nada, es una causa real y hay que documentarla
o: Que señala a una persona en vez de al sistema que permitió aprobar sin revisión
o: Que un postmortem nunca debe incluir líneas de tiempo
a: 2
e: Un postmortem sin culpa busca los factores del sistema, porque son los únicos que se pueden cambiar. Si se podía aprobar sin revisión y el proceso lo permitía, la acción es exigir revisión o automatizar la comprobación. Señalar a la persona deja el sistema intacto y garantiza que el fallo se repita, además de enseñar al equipo a no contar lo que pasa.
:::

:::quiz
p: En un incidente, `MTTD` es 2 minutos y `MTTM` es 50. ¿Qué conviene mejorar antes?
o: El `MTTD`, porque es la primera fase del incidente
o: El `MTTM`, porque es 25 veces mayor y es donde se pierde el tiempo
o: Ninguno de los dos: lo que importa es la causa raíz
a: 2
e: `MTTD` ya es excelente: la alerta funciona y alguien mira. El tiempo se va entre saberlo y parar el daño, que es justo lo que atacan un runbook con comandos pegables y la disciplina de revertir antes de depurar. Optimizar el `MTTD` de 2 minutos no da casi nada; bajar el `MTTM` de 50 a 15 recorta 35 minutos de impacto.
:::

:::trampa
Publicar solo el `MTTR` y llamarlo «tiempo de caída» maquilla el número por abajo: si el sistema
estuvo roto 40 minutos antes de que nadie lo notara, esos 40 minutos no aparecen en la cifra y
sin embargo son los que pagó el cliente. La cifra honesta es el impacto total, desde la primera
petición afectada.
:::

:::nota
Los postmortem de incidentes reales de empresas tecnológicas son material de lectura excelente y
público. Se lee la línea de tiempo para aprender a reconstruir una, y las acciones para ver cómo
se escribe una acción concreta de verdad. Lo que no se copia es el formato de la casa: lo que se
lleva uno es el método de preguntar «¿qué del sistema permitió esto?».
:::
