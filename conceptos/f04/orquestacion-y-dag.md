---
id: orquestacion-y-dag
titulo: Orquestación y DAG
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [etl-vs-elt, batch-vs-streaming]
tags: [orquestacion, dag, planificacion, reintentos, dependencias]
resumen: Un grafo dirigido sin ciclos que dice qué tarea depende de cuál, cuándo se ejecuta cada una y qué hacer cuando una falla a las tres de la mañana.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering', cap. 8", "Apache Airflow documentation, 'DAGs'"]
---

## En una frase

Un orquestador es el programa que sabe en qué orden hay que ejecutar tus trabajos, qué hacer
cuando uno falla y cómo relanzar solo la parte que quedó a medias; el DAG es el grafo de
dependencias que se lo cuenta.

## La idea

Al principio todo el mundo lanza sus scripts con `cron`. Dos líneas y a dormir:

```text
0 3 * * * /opt/etl/extraer.sh
0 4 * * * /opt/etl/transformar.sh
```

Eso funciona exactamente hasta que pasa algo de esta lista:

- La extracción tarda 90 minutos en vez de 60, y la transformación arranca a las 4:00 con los
  datos a medias. **No había una dependencia, había una hora pactada.**
- La extracción falla y la transformación se ejecuta igual, produciendo una tabla vacía que nadie
  detecta hasta el informe de las 9:00.
- Hay que reprocesar el 14 de marzo y alguien tiene que lanzar los cinco scripts a mano, en orden,
  sin equivocarse.
- Nadie sabe qué se ejecutó anoche, cuánto tardó ni por qué falló el martes.

Un **DAG** (grafo dirigido acíclico) resuelve las tres primeras. Los nodos son tareas, las flechas
son dependencias, y «acíclico» significa que no hay bucles: por eso siempre existe al menos un
orden en el que se pueden ejecutar todas. Si hubiera un ciclo, la tarea A esperaría a la B y la B a
la A, y no habría forma de empezar.

Lo que aporta un orquestador, además de dibujar ese grafo:

1. **Dependencias reales.** La tarea B no arranca cuando son las 4:00, arranca cuando A ha
   terminado bien.
2. **Reintentos con espera.** Un fallo de red a las 3:00 no debería despertar a nadie: se reintenta
   tres veces con cinco minutos de espera y probablemente sale solo.
3. **Reproceso por rango de fechas.** Ejecutar el mismo grafo para días pasados sin tocar el
   presente ([[backfill-y-reproceso]]).
4. **Idempotencia por diseño.** Cada ejecución está parametrizada por su intervalo, así que
   relanzarla no duplica ([[idempotencia-y-reintentos]]).
5. **Observabilidad.** Qué se ejecutó, cuándo, cuánto tardó, con qué salida, quién lo relanzó y
   cuántas veces falló esta semana.

Hay dos conceptos que hay que interiorizar antes de tocar un orquestador, porque son el origen de
casi todos los sustos:

- **Ejecución lógica frente a ejecución física.** Una ejecución lanzada el 15 de marzo a las 3:00
  procesa los datos del 14 de marzo. En Airflow, además, la ejecución se nombra por el **inicio de
  su intervalo de datos**, no por el día en que se dispara. Si dentro de la tarea usas el reloj del
  sistema, el reproceso escribirá datos del día equivocado.
- **Camino crítico.** La duración de un DAG no es la suma de sus tareas: es la del camino más largo
  desde el principio hasta el final. Añadir máquinas a las ramas cortas no adelanta nada.

## Definición formal

Un DAG es un par `G = (V, A)` donde `V` son las tareas y `A ⊆ V × V` son las dependencias, sin
ningún ciclo. Para cada tarea `v`, `pred(v)` es el conjunto de sus predecesoras directas: `v` está
lista cuando **todas** las tareas de `pred(v)` han terminado con éxito.

- **Camino crítico:** el camino más largo de una tarea inicial a una final, medido en duración. La
  duración mínima del DAG es la longitud de ese camino. Ninguna cantidad de paralelismo baja de
  ahí.

:::formula
duración_mínima(DAG) = longitud del camino crítico
:::

- **Orden topológico:** cualquier secuencia de las tareas que respeta todas las dependencias. Un
  DAG tiene siempre al menos uno y puede tener muchos; el orquestador no impone cuál, solo respeta
  las flechas.
- **Reintento con espera exponencial:** el intento `k` (contando desde 1) espera

:::formula
espera(k) = t_base · 2^(k−1)
:::

Con `t_base = 5 minutos`, los intentos esperan 5, 10 y 20 minutos. La idea es no machacar un
servicio que está caído: si el problema es de saturación, reintentar cada segundo lo empeora.
- **Ventana de ejecución:** el intervalo `[inicio, fin)` de datos que procesa una ejecución
  concreta. Toda tarea debería recibirlo como parámetro, nunca deducirlo del reloj.

## Ejemplo

Un DAG de siete tareas, con la duración en minutos de cada una:

```text
extraer_clientes (12) --> limpiar_clientes (4) --> cargar_dimension (3) --.
                                                                          '--> cargar_hechos (6) --> validar_totales (2)
extraer_pedidos (35) ---> limpiar_pedidos  (8) --------------------------'
```

Los dos caminos que llegan al final:

- `extraer_clientes → limpiar_clientes → cargar_dimension → cargar_hechos → validar_totales`
  = 12 + 4 + 3 + 6 + 2 = **27 minutos**.
- `extraer_pedidos → limpiar_pedidos → cargar_hechos → validar_totales`
  = 35 + 8 + 6 + 2 = **51 minutos**. Este es el camino crítico.

La suma de todas las tareas es 70 minutos, pero el DAG se completa en **51**: las dos
extracciones corren en paralelo. Y como el camino crítico pasa por `extraer_pedidos`, optimizar
`limpiar_clientes` no adelanta ni un minuto.

Ahora el caso que enseña por qué existen los reintentos. Programación diaria a las 3:00, y
`extraer_pedidos` falla por un corte de red:

```
03:00  arranca extraer_pedidos
03:35  falla                     -> espera 5 min
03:40  reintento 1
04:15  falla                     -> espera 10 min
04:25  reintento 2
05:00  falla                     -> espera 20 min
05:20  reintento 3
05:55  termina bien
06:03  termina limpiar_pedidos
06:09  termina cargar_hechos
06:11  termina validar_totales
```

El informe que debía estar listo a las 3:51 está listo a las 6:11. Un `cron` con horas fijas habría
producido datos incompletos a las 4:00 sin avisar a nadie.

## Código

```python verificable
from collections import deque

# Un DAG pequeno: duracion en minutos y predecesoras de cada tarea.
tareas = {
    "extraer_clientes": (12, []),
    "limpiar_clientes": (4, ["extraer_clientes"]),
    "cargar_dimension": (3, ["limpiar_clientes"]),
    "extraer_pedidos": (35, []),
    "limpiar_pedidos": (8, ["extraer_pedidos"]),
    "cargar_hechos": (6, ["cargar_dimension", "limpiar_pedidos"]),
    "validar_totales": (2, ["cargar_hechos"]),
}

grados = {t: len(pre) for t, (_, pre) in tareas.items()}
siguientes = {t: [] for t in tareas}
for t, (_, pre) in tareas.items():
    for p in pre:
        siguientes[p].append(t)

# Orden topologico: solo se encola una tarea cuando no le queda ninguna predecesora pendiente.
cola = deque(sorted(t for t, g in grados.items() if g == 0))
orden = []
while cola:
    t = cola.popleft()
    orden.append(t)
    for s in sorted(siguientes[t]):
        grados[s] -= 1
        if grados[s] == 0:
            cola.append(s)

inicio, fin = {}, {}
for t in orden:                       # el orden topologico garantiza que las predecesoras ya estan
    pre = tareas[t][1]
    inicio[t] = max((fin[p] for p in pre), default=0)
    fin[t] = inicio[t] + tareas[t][0]
    print(f"{t:<18} inicio {inicio[t]:>3}  fin {fin[t]:>3}")

print("tareas ordenadas:", len(orden))                                    # -> tareas ordenadas: 7
print("duracion sumando todo:", sum(d for d, _ in tareas.values()))       # -> duracion sumando todo: 70
print("duracion del DAG:", max(fin.values()))                             # -> duracion del DAG: 51
```

```python verificable
from datetime import datetime, timedelta

# Reintentos con espera exponencial: el fallo de red no deberia despertar a nadie.
base = timedelta(minutes=5)
t0 = datetime(2024, 3, 15, 3, 0)
minutos_extraccion = 35

for intento in range(1, 4):
    espera = base * (2 ** (intento - 1))
    print(f"reintento {intento}: espera {espera.seconds // 60} min")

espera_total = sum((base * (2 ** (k - 1))).seconds // 60 for k in range(1, 4))
print("espera acumulada:", espera_total, "min")     # -> espera acumulada: 35 min

# Tres intentos fallidos y el cuarto bueno, mas las esperas entre ellos.
fin_extraccion = t0 + timedelta(minutes=4 * minutos_extraccion + espera_total)
print("acaba la extraccion:", fin_extraccion.strftime("%H:%M"))   # -> acaba la extraccion: 05:55
print("acaba el DAG:", (fin_extraccion + timedelta(minutes=16)).strftime("%H:%M"))  # -> acaba el DAG: 06:11
```

## Errores típicos

- **Encadenar por hora en vez de por dependencia.** Poner la transformación a las 4:00 porque la
  extracción «suele tardar una hora» funciona hasta el día que tarda 90 minutos. Entonces la
  transformación lee datos incompletos y el informe sale mal sin que salte ningún error.
- **Usar el reloj del sistema dentro de una tarea.** `datetime.now()` rompe el reproceso: al
  relanzar el 14 de marzo, la tarea escribe datos del día en que la lanzas. La fecha lógica tiene
  que llegar como parámetro.
- **Confundir la fecha lógica con el día del disparo.** Es el origen del clásico «¿por qué el
  informe de ayer tiene datos de anteayer?». La ejecución con fecha lógica del 14 de marzo se lanza
  cuando termina su intervalo, es decir, el 15.
- **Tareas que no son idempotentes.** Si relanzar la tarea del 14 de marzo duplica filas, el
  reproceso es un arma cargada. Cada tarea debe poder ejecutarse dos veces sobre el mismo intervalo
  sin cambiar el resultado ([[idempotencia-y-reintentos]]).
- **No reintentar nada, o reintentar todo veinte veces.** Un fallo de red merece tres intentos con
  espera creciente; un esquema de tabla que alguien cambió va a fallar igual las veinte veces y solo
  llena el registro de ruido. Distingue errores recuperables de errores de programa.
- **Sensores que ocupan una ranura durante horas.** Un sensor que espera un fichero que aparece a
  las 18:00 mantiene un trabajador bloqueado todo el día. Usa modo diferido o reprograma la
  comprobación.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un DAG no puede tener ciclos?
o: Porque entonces no existiría ningún orden en el que se pudieran ejecutar las tareas
o: Porque los orquestadores no admiten más de cien tareas por grafo
o: Porque los ciclos hacen que el historial ocupe el doble
a: 1
e: La ejecución avanza por dependencias: para lanzar una tarea tienen que haber terminado todas sus predecesoras. Con un ciclo, cada tarea del bucle esperaría a otra del bucle y ninguna podría empezar nunca. El límite de tamaño y el historial son cuestiones aparte.
:::

:::quiz
p: La programación es diaria y reprocesas el 14 de marzo. ¿Qué datos debe procesar esa ejecución?
o: Los del 14 de marzo, identificados por su fecha lógica, no los del día en que la lanzas
o: Los del día en que la lanzas, porque es cuando se está ejecutando
o: Los de los últimos treinta días, para asegurar
a: 1
e: La fecha lógica es la identidad de la ejecución: es lo que permite relanzar cualquier día pasado y obtener el mismo resultado. Si la tarea lee el reloj del sistema, el reproceso escribe datos del presente en una partición del pasado y ya no puedes confiar en el histórico.
:::

:::truco
Antes de optimizar un DAG, calcula su camino crítico. La duración del grafo es la del camino más
largo, no la suma de las tareas: repartir máquinas entre las ramas cortas no adelanta ni un minuto.
:::
