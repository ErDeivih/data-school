---
id: metricas-y-alertas
titulo: Métricas, SLO y alertas
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [logging-y-trazas, apis-rest, cache-y-redis, observabilidad-de-datos]
tags: [observabilidad, slo, alertas, metricas]
resumen: SLI, SLO y presupuesto de error: alertar por lo que sufre el usuario y no por causas, con etiquetas de cardinalidad baja o el sistema de métricas se cae.
fuentes: ["Beyer y otros (2016), 'Site Reliability Engineering'", "Beyer y otros (2018), 'The Site Reliability Workbook'"]
---

## En una frase

Una métrica es un número agregado por etiquetas, un SLI es la proporción de peticiones buenas, un
SLO es el mínimo de esa proporción que prometes y el presupuesto de error es lo que puedes gastar
incumpliéndolo; la alerta se dispara cuando el presupuesto **se agota rápido**, no cuando una
causa concreta se pone rara.

## La idea

Todo empieza con una distinción que decide si tus alertas sirven o solo hacen ruido:

- **Síntoma:** lo que sufre quien usa el sistema. «El 4 % de las peticiones de pago devuelven
  error 500», «el 95 % de las búsquedas tarda menos de 400 ms». Se mide en el borde, donde está
  el usuario.
- **Causa:** lo que explica el síntoma por dentro. «La CPU del servicio está al 92 %», «la cola de
  trabajos tiene 40.000 mensajes pendientes», «la réplica va 3 s por detrás».

La tentación es alertar por causas, porque son fáciles de medir y están a mano. Y es un error, por
dos motivos que se ven en cuanto se escriben:

- **La CPU al 92 % no es un problema si nadie lo nota.** Un servicio con caché caliente puede ir
  al 92 % de CPU sirviendo todo en 20 ms. Esa alerta despierta a alguien a las tres de la mañana
  para que no haga nada. Tres de esas y las alertas de verdad se silencian todas.
- **El problema que sí importa puede no tener causa visible.** Una consulta que se volvió lenta por
  un plan de ejecución distinto, un proveedor externo que responde mal, un despliegue que devuelve
  datos equivocados sin gastar más CPU: ninguno de esos enciende la alerta de CPU, y todos se ven
  en la tasa de error.

Regla práctica: **se alerta por síntomas y se diagnostica por causas**. La causa va al panel y al
runbook; la alerta va al síntoma. Hay una excepción legítima: las causas que anuncian un fallo
**inevitable y próximo**, como «el disco se llena en 4 horas». Ahí la alerta es una predicción, no
una causa cualquiera.

**El SLI es una proporción, no un promedio.** Un SLI bien puesto tiene esta forma:

:::formula
SLI = eventos_buenos / eventos_totales
:::

Y la clave está en la palabra **eventos**: el denominador son sucesos contables, no tiempo. «El
99,9 % de las peticiones se sirvieron bien» es un SLI. «El servicio estuvo disponible el 99,9 %
del tiempo» es una promesa que nadie sabe medir y que además es mentira: un servicio que devuelve
error 500 en todas las peticiones está «disponible» (el proceso responde) y no sirve para nada.

**El SLO es el listón.** Es el valor mínimo del SLI que te comprometes a cumplir en una ventana,
normalmente 28 o 30 días. Y de él sale el número que de verdad gobierna la operación: el
**presupuesto de error**, que es lo que puedes incumplir.

:::formula
presupuesto_de_error = 1 − SLO
:::

Con un SLO del 99,9 % en una ventana de 30 días, el presupuesto es del 0,1 % de los eventos, o
43,2 minutos si lo mides en tiempo. Ese presupuesto cambia la conversación por completo. Ya no se
discute «¿podemos desplegar el viernes?»: se mira el presupuesto que queda. Si queda entero, se
despliega sin drama. Si está agotado, la prioridad del equipo es la fiabilidad y las funciones
nuevas esperan. Es la única forma conocida de que «vamos con prisa» deje de ser una opinión.

**El burn rate gobierna las alertas.** El presupuesto se gasta; la pregunta es a qué velocidad. Si
lo gastas repartido por igual durante toda la ventana, a ese ritmo se le llama 1. Si lo gastas al
doble de velocidad, es un burn rate de 2. La gracia es que un burn rate alto **en una ventana
corta** es una señal de incendio:

:::formula
burn_rate = (tasa_de_error_observada / tasa_de_error_permitida)
:::

Un burn rate de 14,4 sostenido durante una hora consume 14,4 / 720 = el 2 % del presupuesto
mensual en una hora. Y dos umbrales bastan para cubrir los dos escenarios: un incendio rápido que
hay que apagar ya (ventana corta, umbral alto) y una hemorragia lenta que se come el mes gota a
gota (ventana larga, umbral más bajo). Los números concretos están en el ejemplo.

**Cardinalidad: cómo tumbar el sistema de métricas en una tarde.** Una métrica con etiquetas no es
una serie temporal; es **una serie por cada combinación de valores de sus etiquetas**. Con 20
métricas base, 5 rutas, 3 regiones y 4 métodos salen 20 · 5 · 3 · 4 = 1.200 series: eso lo aguanta
cualquier sistema. Ahora añade la etiqueta `usuario_id`, que en un día tiene 100.000 valores
distintos: 20 · 5 · 3 · 4 · 100.000 = **120 millones de series**. El sistema de métricas no falla
con un error elegante: deja de aceptar escrituras, las consultas se agotan por tiempo de espera y
te quedas sin observabilidad justo el día que la necesitas.

La regla es tajante: **el identificador de usuario, la URL con parámetros y el identificador de
petición no son etiquetas de métrica**. La cardinalidad alta vive en los registros y en las trazas
([[logging-y-trazas]]), que están hechos para eso. Y si necesitas saltar de un panel a un caso
concreto, se usan ejemplos enlazados: la métrica guarda unos pocos identificadores de muestra por
cubo, no todos.

## Definición formal

**SLI.** Sea `buenos` el número de eventos que cumplen el criterio y `total` el número de eventos
contables de la misma clase:

:::formula
SLI = buenos / total
:::

Criterios típicos, uno por tipo de servicio:

- **Disponibilidad:** la petición se sirvió con un código que no es 5xx.
- **Latencia:** la petición se sirvió en menos del umbral acordado. Se mide con percentiles, no con
  la media: la media esconde el 1 % que sufre.
- **Corrección:** el dato devuelto es el correcto (el más difícil de medir y el más importante).
- **Frescura:** el dato más reciente tiene menos de X minutos (clave en un sistema de datos).

**SLO y presupuesto.** Con `SLO` expresado en tanto por uno:

:::formula
presupuesto = 1 − SLO
consumido = 1 − SLI_acumulado
restante = SLO − SLI_acumulado
:::

**Ventana.** La media móvil sobre una ventana `W`:

:::formula
SLI_W = buenos_en_W / total_en_W
:::

La media móvil es la que se alerta; la ventana **calendario** (el mes natural) es la que se usa
para el informe y para decidir prioridades. Confundirlas hace que el mismo sistema parezca sano en
un sitio y enfermo en el otro.

**Burn rate.** Con `E` la tasa de error permitida (`1 − SLO`):

:::formula
burn_rate(W) = tasa_de_error_en_W / E
tiempo_para_agotar = tiempo_restante_de_ventana / burn_rate
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `buenos` | Eventos que cumplen el criterio (petición sin 5xx, respuesta bajo el umbral) | eventos | Sube el `SLI` en línea recta. Es la parte que se puede mejorar sin tocar nada más: un caché bien puesto ([[cache-y-redis]]) sube `buenos` sin bajar `total` |
| `total` | Eventos contables de esa clase en la ventana | eventos | Sube el `SLI` si los nuevos eventos son buenos y lo baja si son malos. Ojo: si `total` es 0, el `SLI` es indefinido, no 1 |
| `SLI` | La proporción de eventos buenos | tanto por uno (0,999 = 99,9 %) | Es lo que se mide. Un `SLI` de 1 sostenido suele significar que el criterio es demasiado blando o que `total` solo cuenta lo que funciona |
| `SLO` | El listón que prometes para el `SLI` en la ventana | tanto por uno | Al subirlo, el presupuesto se encoge: del 99,9 % al 99,99 % pasas de 43,2 minutos a 4,3 al mes, y cada despliegue se vuelve una apuesta |
| `presupuesto` (`E`) | Lo que puedes incumplir: `1 − SLO` | tanto por uno o minutos | Es el presupuesto de la operación. Si sube, caben más fallos y más despliegues arriesgados; si se agota, se congelan las funciones nuevas |
| `W` | La ventana sobre la que se mide el `SLI` | minutos, horas o días | Es el parámetro que más se olvida y el que decide la alerta: una ventana de 5 minutos da alertas nerviosas; una de 30 días tarda una eternidad en enterarse de un incendio |
| `burn_rate` | A qué múltiplo del ritmo permitido se gasta el presupuesto | adimensional (1 = ritmo justo) | Por encima de 1 se agota antes del final de la ventana. Es la magnitud de las alertas: 14,4 en una hora es un incendio, 1,1 durante un mes es una deriva |
| Etiquetas | Cada clave cuyo valor multiplica las series | — | Cada etiqueta nueva **multiplica** series, no las suma. Una etiqueta de cardinalidad 100.000 sobre 1.200 series da 120 millones y tumba el sistema de métricas |
:::

**Alertas multiventana.** Un solo umbral obliga a elegir entre ser nervioso o ser lento. Se usan dos
condiciones a la vez, y solo alerta si **las dos** se cumplen:

:::formula
alerta_rapida: burn_rate(5 min) > 14,4  Y  burn_rate(1 h) > 14,4
alerta_lenta:  burn_rate(30 min) > 6    Y  burn_rate(6 h) > 6
:::

- La ventana **larga** confirma que no es un pico de treinta segundos (evita el falso positivo).
- La ventana **corta** hace que la alerta se resuelva rápido cuando el problema se arregla, en vez
  de quedarse encendida horas porque la media de 6 horas sigue sucia.

## Ejemplo

Un servicio de pagos con `SLO = 99,9 %` en una ventana de 30 días, con 10 peticiones por segundo.
Los eventos totales de la ventana son 10 · 86.400 · 30 = **25.920.000**. El presupuesto de error es
del 0,1 %: **25.920 peticiones** fallidas, o **43,2 minutos** si se mira en tiempo.

Incidente: durante 40 minutos, la tasa de error es del 4 %.

- Error permitido: `E = 1 − 0,999 = 0,001` (una de cada mil peticiones).
- `burn_rate` en esos 40 minutos: 0,04 / 0,001 = **40**.
- Presupuesto consumido: 40 · (40 / 43.200) = **3,7 %** del mes en 40 minutos.
- A ese ritmo, el presupuesto entero dura 43.200 / 40 = **1.080 minutos**: 18 horas. Un solo día
  malo cierra el mes.

Ahora la comparación que enseña por qué se alerta con ventanas: la misma tasa de error del 4 %
durante **5 minutos** consume el 0,46 % del presupuesto y no merece despertar a nadie; durante
**6 horas** consume el 33 % y es un incendio declarado. Sin ventana, la misma cifra significa las
dos cosas a la vez.

Y la otra cara: una tasa de error del **0,15 %** (burn rate 1,5) no enciende ninguna alerta de
incendio, pero si se sostiene todo el mes agota el presupuesto en 20 días. Ese es el caso que
justifica la alerta lenta.

:::figura
fichero: metricas-presupuesto-y-cardinalidad
pie: Izquierda, el presupuesto de error de un mes al 99,9 %: la línea gris es el ritmo que lo gasta justo al final de la ventana y la escalera azul es el consumo real, con un incidente de 6 horas que se lleva el 33 % del presupuesto de golpe. Cuando se cruza la banda roja, quedan menos de tres días de presupuesto y lo que toca no es desplegar. Derecha, la explosión de cardinalidad: añadir el identificador de usuario como etiqueta multiplica las series por cien mil y el sistema de métricas deja de aceptar escrituras, justo el día que hace falta.
fuente: figuras/metricas-y-alertas-1.py
:::

## Código

```python verificable
# --- inicio formula 1 ---
# De un SLO salen DOS presupuestos distintos y no son intercambiables.
slo = 0.999
ventana_dias = 30
rps = 10

error_permitido = 1 - slo
segundos_ventana = ventana_dias * 86400
eventos_totales = rps * segundos_ventana
# El presupuesto en tiempo es la fraccion del mes que puedes estar fallando: 0,001 * 30 dias.
minutos_presupuesto = error_permitido * ventana_dias * 24 * 60
# El presupuesto en peticiones es esa misma fraccion sobre el trafico.
peticiones_presupuesto = error_permitido * eventos_totales
# --- fin formula 1 ---

print("error permitido: %.4f" % error_permitido)               # -> 0.0010
print("eventos en la ventana:", eventos_totales)               # -> 25920000
print("presupuesto en minutos: %.1f" % minutos_presupuesto)    # -> 43.2
print("presupuesto en peticiones: %.0f" % peticiones_presupuesto)  # -> 25920
```

:::claves
- `1 - slo` con `slo = 0.999` da `0.0009999999999998899`, no `0.001`: es el error de redondeo
  binario de siempre. Al imprimir con `%.4f` sale bien y al comparar con `== 0.001` daría `False`.
  Para comparar decimales exactos, redondea antes o usa `decimal.Decimal`.
- El presupuesto **en tiempo** y el **en peticiones** se calculan de dos formas distintas: el de
  tiempo reparte los minutos de la ventana y el de peticiones reparte el tráfico. Solo coinciden si
  el tráfico es constante; con un pico de tráfico nocturno, el mismo minuto de caída cuesta mucho
  más presupuesto en peticiones que en tiempo.
- El presupuesto en tiempo sale de `error_permitido * ventana_dias * 24 * 60` = 43,2 minutos al
  mes, que es la cifra que se cita en las conversaciones. No es «el servicio puede estar caído 43
  minutos seguidos»: es la suma de todo lo que falles, repartido como sea.
- Este bloque no usa pandas ni NumPy a propósito: son cuatro multiplicaciones y traer una librería
  para eso solo hace el ejemplo más difícil de leer y más lento de arrancar.
:::

```python verificable
# --- inicio formula 2 ---
# El burn rate decide si una alerta es un incendio o una deriva. Mismo SLO, traficos distintos.
def burn_rate(tasa_de_error, slo):
    # Cuantas veces mas rapido se gasta el presupuesto que al ritmo permitido.
    return tasa_de_error / (1 - slo)

casos = [
    ("pico de 5 minutos al 4 %", 0.04, 5),
    ("incidente de 40 minutos al 4 %", 0.04, 40),
    ("incidente de 6 horas al 4 %", 0.04, 360),
    ("deriva del 0,15 % todo el mes", 0.0015, 43200),
]
ventana_minutos = 30 * 24 * 60

for nombre, tasa, minutos in casos:
    br = burn_rate(tasa, 0.999)
    # Lo gastado es el burn rate por la fraccion de la ventana que duro el fallo: quemar al
    # cuadruple durante una hora de un mes de 720 horas gasta 4/720 del presupuesto.
    consumido = br * minutos / ventana_minutos
    # El presupuesto no se puede gastar dos veces: al 100 % esta agotado y el resto es dano
    # que ya no cabe. El burn rate baja a 1 cuando se topa, no sigue subiendo.
    print("%-32s burn %5.1f  presupuesto %6.2f%%  se agota en %s"
          % (nombre, br, 100 * consumido,
             "no aplica" if br <= 1 else "%.0f h" % (ventana_minutos / br / 60)))
# --- fin formula 2 ---
# -> pico de 5 minutos al 4 %        burn  40.0  presupuesto   0.46%  se agota en  18 h
# -> incidente de 40 minutos al 4 %  burn  40.0  presupuesto   3.70%  se agota en  18 h
# -> incidente de 6 horas al 4 %     burn  40.0  presupuesto  33.33%  se agota en  18 h
# -> deriva del 0,15 % todo el mes   burn   1.5  presupuesto 150.00%  se agota en 480 h
# Ojo: el burn rate es el MISMO en los tres primeros casos porque la tasa de error es la misma.
# Lo que cambia el dano no es el burn rate, es cuanto tiempo se sostiene. La deriva es al reves:
# un burn rate modesto (1,5) que dura el mes entero agota el presupuesto en 20 dias, y eso no lo
# detecta ninguna alerta de incendio.
```

```python verificable
# --- inicio formula 3 ---
# Cardinalidad: cada etiqueta MULTIPLICA las series, no las suma.
metricas_base = 20
endpoints, regiones, metodos = 5, 3, 4

sin_usuario = metricas_base * endpoints * regiones * metodos
con_cien_usuarios = sin_usuario * 100
con_cien_mil_usuarios = sin_usuario * 100_000
# --- fin formula 3 ---

print("series sin etiqueta de usuario:", sin_usuario)             # -> 1200
print("con 100 usuarios distintos:", con_cien_usuarios)           # -> 120000
print("con 100.000 usuarios:", f"{con_cien_mil_usuarios:,}")      # -> 120,000,000
print("factor de crecimiento:", con_cien_mil_usuarios // sin_usuario)  # -> 100000
```

## Errores típicos

- **Alertar por causas.** La CPU, la memoria, el número de conexiones y la profundidad de la cola
  son paneles, no alertas. Despiertan a gente que no puede hacer nada y, a fuerza de ruido, se
  acaban silenciando justo las que importan. La alerta va al síntoma; la causa, al runbook.
- **Usar la media como SLI de latencia.** Si el 99 % de las peticiones tarda 50 ms y el 1 % tarda
  8 segundos, la media sale por debajo de 130 ms y el panel dice que todo va bien. Se mide con
  percentiles, y el umbral del SLO se pone sobre el p95 o el p99, nunca sobre la media.
- **Poner `usuario_id`, la URL completa o el `request_id` como etiqueta.** Cada valor distinto de
  una etiqueta multiplica las series. Con 100.000 usuarios pasas de 1.200 series a 120 millones y
  el sistema de métricas deja de aceptar escrituras. Esos identificadores van en registros y trazas.
- **Definir el SLO pero no el presupuesto de error.** Sin presupuesto, el SLO es un adorno: no hay
  nada que gastar y por tanto ninguna decisión que tomar. El presupuesto es la herramienta de
  gestión; el SLO solo es el número del que sale.
- **Medir el SLI en un sitio que no es donde está el usuario.** Un SLI medido en el balanceador no
  ve los errores que el usuario recibe desde su red, y uno medido dentro del servicio puede contar
  como buenas las respuestas que se pierden de camino. Se mide lo más cerca posible del usuario.
- **Un `total` que solo cuenta lo que funciona.** Si el contador de peticiones se incrementa
  después de validar la petición, todas las peticiones inválidas desaparecen del denominador y el
  SLI sale del 100 % mientras los usuarios ven errores. El denominador se incrementa al **entrar**.
- **Alertas sin acción asociada.** Una alerta que no dice qué hacer obliga a quien la recibe a
  investigar desde cero a las cuatro de la mañana. Toda alerta enciende un runbook que empieza por
  «cómo se confirma que es esto» ([[incidentes-y-postmortem]]).
- **Silenciar en vez de arreglar.** Un silencio de alertas durante un despliegue tapa el problema
  real que aparezca en esa franja. Si el despliegue genera ruido, se ajusta la alerta para que el
  despliegue no la dispare; no se apaga el sistema de alertas.

## Comprueba que lo sabes

:::practica
enunciado: Un servicio con 50 peticiones por segundo y `SLO = 99,95 %` en 30 días sufre un incidente de 12 minutos con el 8 % de errores. Calcula el error permitido, el presupuesto en peticiones y minutos, el burn rate y el porcentaje del presupuesto consumido. Después decide si conviene declarar incidente y congelar despliegues.
pista: El burn rate es la tasa observada dividida entre el error permitido; el consumido, esa misma cuenta por la fracción de ventana que duró el fallo.
solucion: Error permitido = 0,0005 (una de cada 2.000). Eventos en la ventana = 50 · 86.400 · 30 = 129.600.000; presupuesto = 64.800 peticiones, o 0,0005 · 43.200 = 21,6 minutos. Burn rate = 0,08 / 0,0005 = 160. Consumido = 160 · (12 / 43.200) = 4,4 % del presupuesto. Con un 95,6 % del presupuesto intacto, no hay motivo para congelar nada: se investiga la causa ([[incidentes-y-postmortem]]) y se sigue desplegando. Lo que sí hay que mirar es por qué una tasa de error de 160 veces lo permitido no disparó una alerta, y ese es un problema de umbrales, no de SLO.
:::

:::quiz
p: El panel de CPU de tu servicio lleva una semana al 88 % y nadie se ha quejado. ¿Qué haces con la alerta de CPU?
o: Bajarla al 80 % para enterarte antes
o: Quitarla como alerta y dejarla en el panel; la alerta debe ir al síntoma que sufre el usuario
o: Silenciarla solo por la noche
a: 2
e: La CPU alta sin impacto en el usuario no es un incidente, y una alerta que no requiere acción enseña al equipo a ignorar las alertas. La CPU se queda en el panel para el diagnóstico; la alerta se pone en la tasa de error o en la latencia del percentil alto. La excepción son las causas que anuncian un fallo inevitable, como un disco que se llena.
:::

:::quiz
p: Por qué no se debe usar el identificador de usuario como etiqueta de una métrica?
o: Porque ocupa más espacio en disco por serie
o: Porque cada valor distinto de la etiqueta multiplica las series temporales y el sistema de métricas deja de admitir escrituras
o: Porque las etiquetas solo admiten números
a: 2
e: Las etiquetas no suman series, las multiplican: con 1.200 series base y 100.000 usuarios salen 120 millones de series por métrica. El coste de disco es lo de menos: el sistema se queda sin memoria, rechaza escrituras y pierdes la observabilidad completa. Los identificadores van en registros y trazas, que están diseñados para cardinalidad alta.
:::

:::quiz
p: Un SLO del 99,9 % en 30 días equivale a cuánto presupuesto de error?
o: 43,2 minutos o el 0,1 % de los eventos
o: 8,6 horas, porque es el 1 % de un mes
o: 1 minuto, porque el 0,1 % de 30 días es menos de un minuto
a: 1
e: El presupuesto es 1 − 0,999 = 0,001, es decir el 0,1 %. Sobre 30 días son 0,001 · 43.200 = 43,2 minutos, o 0,1 de cada 1.000 peticiones. Las 8,6 horas corresponden a un SLO del 98,8 %, un listón mucho más flojo.
:::

:::trampa
Un SLI del 100 % casi siempre significa que la medición está mal, no que el sistema sea perfecto.
Suele ser un denominador que solo cuenta las peticiones que llegaron a completarse, un criterio tan
laxo que nada lo incumple, o una ventana tan corta que siempre está limpia. Antes de presumir de
disponibilidad, mira el `total`: si no cuadra con el tráfico que ves en el panel de negocio, el
número bueno es el del panel de negocio.
:::

:::nota
El SLO no es una promesa legal ni un acuerdo de nivel de servicio con un cliente: es una
herramienta interna para decidir en qué se trabaja. Se puede y se debe revisar cada trimestre. Un
SLO que nunca se incumple está demasiado flojo (y estás gastando de más en fiabilidad); uno que se
incumple todos los meses está demasiado alto y desmotiva.
:::
