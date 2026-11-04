---
id: calidad-y-slas
titulo: Calidad y acuerdos de nivel de servicio
fase: 4
nivel: avanzado
rutas: [de]
prerequisitos: [calidad-de-datos, orquestacion-y-dag]
tags: [calidad, alertas, frescura, slo]
resumen: El SLI es cómo mides la calidad, el SLO el umbral que te exiges y el SLA el acuerdo con consecuencia; sin un número medible no hay promesa que valga.
fuentes: ["Moses, Gavish & Vorwerck (2022), 'Data Quality Fundamentals'", "Reis & Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

Un acuerdo de nivel de servicio en datos es una promesa medible —a qué hora, con cuántas filas,
con qué exactitud— más la forma de comprobarla; sin esa parte, «los datos están mal» es una
opinión que no se puede priorizar ni discutir.

## La idea

«El dato llega tarde» es una queja. «La tabla `fact_ventas` debe estar completa a las 06:30 y en
los últimos 30 días lo ha estado 29 veces» es un hecho sobre el que se puede decidir: se puede
priorizar, se puede asignar a alguien y se puede comprobar si la semana que viene ha mejorado.

Todo el concepto consiste en convertir la calidad en números con umbral y dueño. Los cinco ejes
que de verdad se miden en un pipeline:

1. **Frescura.** Cuánto tiempo pasa desde que el dato se produce hasta que está disponible.
   `ahora − max(fecha_evento)`. Detecta el pipeline parado.
2. **Completitud.** Cuántas filas o claves faltan. `filas_cargadas ÷ filas_esperadas`. Detecta la
   pérdida parcial, que es más traicionera que la caída total porque no hace ruido.
3. **Exactitud.** Si el valor es correcto. Casi nunca se puede comprobar directamente; se
   aproxima con **reconciliación** contra el origen: `suma(origen) = suma(destino)`.
4. **Unicidad.** Que no haya duplicados en la clave que define el grano.
5. **Validez y coherencia.** Tipos, rangos, dominios permitidos y consistencia entre tablas
   relacionadas (toda venta tiene un cliente que existe).

Y el vocabulario, tomado prestado de la ingeniería de fiabilidad:

- **SLI** (indicador): lo que mides. «Retraso de la partición diaria, en minutos».
- **SLO** (objetivo): el valor que te propones. «El 99 % de los días con un retraso de 30 minutos
  o menos».
- **SLA** (acuerdo): el SLO con consecuencia. Penalización económica, escalado a guardia,
  prioridad sobre otras tareas. No todo necesita SLA; casi todo necesita SLO.
- **Presupuesto de error**: lo que te puedes permitir incumplir. Con un SLO del 99 % sobre 30
  días, el presupuesto es 0,3 días al mes. Cuando se agota, se paran las funcionalidades nuevas y
  se arregla el pipeline.

La parte que casi todo el mundo hace mal son las **alertas**. Tres reglas que cambian por
completo su utilidad:

- **Alertar por síntoma, no por causa.** Al consumidor le da igual que el paso `extract_3` haya
  fallado; lo que necesita saber es «la tabla de ventas no estará lista». Una alerta por tablas y
  día, no cuarenta alertas por tareas.
- **Umbrales relativos a la historia.** La tabla tiene 1,2 millones de filas los martes con una
  variación del 8 %. Alertar por debajo de un millón fijo salta todos los domingos; lo que sirve
  es comparar con el mismo día de la semana.
- **Cada alerta con dueño y contexto.** Tabla, partición, valor observado, valor esperado, dueño y
  enlace a la ejecución. Una alerta sin dueño se archiva sola.

:::trampa
Confundir frescura con exactitud. Un dato puede llegar puntual y estar mal, y puede llegar tarde
y estar bien. Son dos SLI distintos, se rompen por causas distintas y se arreglan en sitios
distintos. Si sólo mides la hora de llegada, tu tabla puede estar siempre a tiempo y llevar tres
semanas sumando mal.
:::

## Definición formal

Para una tabla con particiones diarias, tres indicadores calculables sin ambigüedad:

:::formula
frescura(p) = max(fecha_evento en p) − inicio de p
:::

:::formula
completitud(p) = filas_cargadas(p) ÷ filas_esperadas(p)
:::

:::formula
cumplimiento_SLO = días con retraso ≤ umbral ÷ días observados
:::

Símbolos:

- `p` — la partición, normalmente un día natural.
- `fecha_evento` — la columna que dice cuándo ocurrió el hecho, no cuándo se cargó. Si no la
  tienes, no puedes medir frescura: sólo puedes medir hora de carga.
- `filas_esperadas` — lo que el origen declara que hay. Sin un recuento del origen, la
  completitud se estima con la mediana histórica del mismo día de la semana.
- `retraso` — minutos entre la hora prometida y la hora real en que la partición quedó completa.
- `umbral` — el retraso máximo que el SLO considera aceptable (30 minutos en el ejemplo).

El **presupuesto de error** se deriva del SLO:

:::formula
presupuesto = (1 − SLO) · días observados
:::

## Ejemplo

`fact_ventas` debe estar completa a las 06:30. Retrasos de los últimos 30 días, en minutos sobre
esa hora:

```text
0  2  0  5  0  0  3  0  12 0  0  4  0  0  8  0
0  0  6  0  0  2  0  0  40 0  0  3  0  0
```

- 29 de 30 días dentro del umbral de 30 minutos: **96,7 %** de cumplimiento. El SLO del 99 % no
  se cumple.
- Retraso mediano: **0 minutos**. Percentil 95: **10,2 minutos**. Peor día: **40 minutos**.
- Presupuesto de error con SLO del 99 %: (1 − 0,99) · 30 = **0,3 días**. Se ha gastado 1 día,
  **3,3 veces** el presupuesto del mes.

Fíjate en la trampa de la mediana: «la mediana es 0, o sea que va perfecto» es exactamente lo que
diría alguien que no ha mirado el percentil 95 ni el peor caso. La mediana dice que la mayoría de
los días van bien; el SLO se juzga con la cola.

Y la completitud, que es otro SLI y ese día también falló. El 14 de marzo:

| Canal | Filas cargadas | Filas esperadas | Completitud |
| --- | --- | --- | --- |
| web | 610.000 | 610.000 | 100,0 % |
| app | 300.000 | 300.000 | 100,0 % |
| marketplace | 74.000 | 110.000 | 67,3 % |
| Total | 984.000 | 1.020.000 | 96,5 % |

El total parece casi bien; el desglose por canal dice la verdad: faltan 36.000 filas y todas son
de `marketplace`. Un SLO de completitud global del 95 % habría dado el día por bueno. Por eso los
indicadores se definen sobre la dimensión que puede romperse, no sólo sobre el total.

## Código

```python verificable
import numpy as np

# Retraso en minutos sobre las 06:30 de la particion diaria, ultimos 30 dias.
retrasos = np.array([0, 2, 0, 5, 0, 0, 3, 0, 12, 0, 0, 4, 0, 0, 8, 0,
                     0, 0, 6, 0, 0, 2, 0, 0, 40, 0, 0, 3, 0, 0])

umbral, slo = 30, 0.99
cumplimiento = (retrasos <= umbral).mean()
presupuesto = (1 - slo) * retrasos.size
print(f"cumplimiento {cumplimiento:.1%}")                       # -> cumplimiento 96.7%
print(f"dias observados {retrasos.size}  fuera {int((retrasos > umbral).sum())}")  # -> dias observados 30  fuera 1
print(f"presupuesto de error {presupuesto:.1f} dias")           # -> presupuesto de error 0.3 dias
print(f"mediana {np.median(retrasos):.1f} min  p95 {np.percentile(retrasos, 95):.1f} min")
# -> mediana 0.0 min  p95 10.2 min
```

```python verificable
# Completitud por canal: el total puede cuadrar y el desglose no.
esperadas = {"web": 610_000, "app": 300_000, "marketplace": 110_000}
cargadas = {"web": 610_000, "app": 300_000, "marketplace": 74_000}

for canal in esperadas:
    print(canal, cargadas[canal], "de", esperadas[canal],
          f"{cargadas[canal] / esperadas[canal]:.1%}")
# -> web 610000 de 610000 100.0%
# -> app 300000 de 300000 100.0%
# -> marketplace 74000 de 110000 67.3%

total_cargado, total_esperado = sum(cargadas.values()), sum(esperadas.values())
print("total", total_cargado, "de", total_esperado, f"{total_cargado / total_esperado:.1%}")
# -> total 984000 de 1020000 96.5%
```

## Errores típicos

- **Prometer «los datos estarán bien» sin número.** Sin SLI no hay SLO, sin SLO no hay umbral y
  sin umbral no hay alerta. La conversación se queda en una discusión de percepciones.
- **Medir la calidad sólo en el destino final.** Si mides la completitud únicamente en la tabla
  que consume el negocio, sabes que falta algo pero no en qué capa se perdió. Hay que medir en
  cada frontera: origen contra ingesta, ingesta contra transformación, transformación contra
  consumo.
- **Umbrales absolutos fijos.** «Alertar si hay menos de un millón de filas» dispara todos los
  domingos y no dispara el domingo en el que de verdad falta la mitad. Los umbrales se calculan
  contra la misma estacionalidad.
- **Alertar por causa y no por síntoma.** Un fallo de red genera cuarenta alertas de tareas y
  ninguna dice «la tabla de ventas no está lista». Las cuarenta se silencian y con ellas la que
  importaba.
- **Definir un SLA sin dueño ni consecuencia.** Un documento que dice «la tabla debe estar a las
  06:30» y no tiene a quién reclamar no cambia ningún comportamiento. El SLA lleva nombre y
  efecto.
- **Perseguir el 100 % de frescura.** Un SLO del 100 % es imposible y hace que el equipo deje de
  mirar las alertas en cuanto se incumple (que será siempre). Los objetivos se ponen donde el
  coste de mejorarlos deja de compensar.

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre un SLI, un SLO y un SLA?
o: Son tres nombres para lo mismo según el tamaño de la empresa
o: El SLI es lo que mides, el SLO el umbral que te exiges y el SLA el acuerdo con consecuencia si no se cumple
o: El SLI lo define el consumidor, el SLO el productor y el SLA el proveedor de la nube
a: 2
e: El indicador es una medida (minutos de retraso), el objetivo es un valor con un porcentaje (99 % de los días por debajo de 30 minutos) y el acuerdo añade una consecuencia: penalización, escalado o prioridad. Se puede tener SLO sin SLA, y es lo normal.
:::

:::quiz
p: La tabla tiene un retraso mediano de 0 minutos pero un percentil 95 de 10,2 y un peor día de 40. Con un SLO de «99 % de los días con 30 minutos o menos», ¿qué conclusión es correcta?
o: El SLO se cumple, porque la mediana es 0
o: El SLO no se cumple: ha habido 1 día de 30 en el que el retraso superó el umbral
o: No se puede saber sin conocer la media
a: 2
e: 1 día de cada 30 es un 96,7 % de cumplimiento, por debajo del 99 %. La mediana dice que la mayoría de los días van bien, y es justo la trampa: un SLO se juzga por la cola, no por el caso típico. La media no aporta nada aquí porque un valor extremo la desplaza.
:::

:::practica
enunciado: Quieres definir el SLO de frescura de la tabla `fact_pedidos`, que alimenta el cuadro de mando de operaciones. Hoy nadie ha medido nada. Propón el indicador, el objetivo y la alerta, con los números que usarías para empezar.
pista: Piensa en quién consume la tabla y a qué hora, y en cómo varía el volumen según el día de la semana.
solucion: Indicador (SLI): minutos de retraso entre las 07:00 y el momento en que la partición del día anterior está completa y con el 100 % de las filas esperadas; se mide por partición diaria. Objetivo (SLO): el 99 % de los días con retraso menor o igual a 30 minutos, sobre una ventana móvil de 30 días. Alerta: una sola por tabla y día, disparada cuando la partición no está completa a las 07:45 (media hora después del umbral, para no despertar a nadie por un retraso de dos minutos), con la tabla, la partición, las filas cargadas frente a las esperadas y el enlace a la ejecución. Para la completitud se usa una banda relativa: alertar si las filas caen más de un 15 % respecto a la mediana de los cuatro mismos días de la semana anteriores, y además si el porcentaje de nulos de la clave sube del 0,1 %. Todo esto se revisa al mes: si el SLO se cumple siempre, está flojo; si nunca se cumple, o el objetivo es irreal o el pipeline necesita trabajo de verdad.
:::
