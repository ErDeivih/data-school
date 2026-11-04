---
id: airflow-dagster-prefect
titulo: Airflow, Dagster y Prefect
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [orquestacion-y-dag, etl-vs-elt]
tags: [airflow, dagster, prefect, orquestacion, herramientas]
resumen: Los tres orquestadores que aparecen en las ofertas de empleo, en qué se parecen y qué forma distinta de pensar propone cada uno.
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering', cap. 8", "Apache Airflow documentation, 'DAGs'", "Dagster documentation, 'Software-defined assets'"]
---

## En una frase

Airflow, Dagster y Prefect resuelven el mismo problema —decidir qué se ejecuta, cuándo y en qué
orden— con tres formas distintas de pensarlo: Airflow organiza tareas, Dagster organiza los datos
que esas tareas producen, y Prefect convierte tu propio código Python en el pipeline sin escribir
un grafo aparte.

## La idea

Los tres son orquestadores: un planificador que lanza trabajos según un calendario y unas
dependencias, más una interfaz que dice qué pasó anoche. Ninguno te da una capacidad que los otros
no tengan; lo que cambia es **lo que te cuesta hacer cada cosa** y el vocabulario con el que
piensas.

**Airflow** nació en 2014 y se popularizó primero, así que es el que más te vas a encontrar. Escribes
un fichero de DAG en Python con operadores (`PythonOperator`, `BashOperator`, y un catálogo enorme
de integraciones) y encadenas dependencias con el operador `>>`. Su ventaja es la comunidad: lleva
una década acumulando conectores para cualquier sistema que se te ocurra. Su precio es que arrastra
decisiones de diseño propias: el planificador **lee y evalúa tu fichero de DAG cada pocos segundos**,
así que meter lógica pesada ahí dentro (una consulta a base de datos, un bucle grande) degrada el
orquestador entero; y la fecha lógica tiene la semántica de intervalo que se explica más abajo.

**Dagster** propone invertir el punto de vista. En lugar de describir tareas, describes **activos**
(*assets*): la tabla `ventas_por_provincia`, el fichero `clientes.parquet`, el modelo entrenado. De
cada activo declaras de qué depende y el grafo de ejecución se deduce solo. La ventaja es que el
catálogo y el linaje salen gratis, porque el orquestador ya sabe qué existe, quién lo produce y
quién lo consume ([[catalogo-y-linaje]]). Trae además tipado de entradas y salidas y una forma de
ejecutar el grafo en tu portátil sin levantar nada, lo que hace las pruebas mucho menos dolorosas.

**Prefect** nació de la frustración con Airflow: en vez de mantener un fichero de grafo separado del
código, decoras tus funciones con `@flow` y `@task` y ya tienes un pipeline. El grafo se construye
en tiempo de ejecución, lo que permite ramas dinámicas de verdad (decidir sobre la marcha cuántas
tareas lanzar). Su modelo de ejecución separa el planificador de los trabajadores, así que no
necesitas operar una base de datos de metadatos propia si no quieres.

Donde te los vas a encontrar:

- **Airflow** domina en empresas grandes y es el que más aparece en las ofertas de empleo. Es el que
  conviene saber leer aunque acabes trabajando con otro.
- **Dagster** está creciendo en equipos que ya tienen un problema serio de catálogo, linaje y
  calidad del dato.
- **Prefect** se usa en equipos pequeños, en proyectos nuevos y donde el pipeline es, sobre todo,
  código Python con bastante lógica propia.

Y lo que comparten los tres, que es lo que de verdad importa aprender: programación por calendario o
por evento, reintentos con espera, reproceso por rango de fechas ([[backfill-y-reproceso]]),
alertas, y una interfaz donde mirar duraciones y fallos. Cambiar de orquestador es un trabajo de
meses que **no arregla** que tus tareas no sean idempotentes ni que nadie mire las alertas
([[idempotencia-y-reintentos]]).

## Definición formal

Conviene fijar el vocabulario, porque cada herramienta usa el suyo para lo mismo:

- **Unidad de trabajo:** `task` en Airflow, `op` o `asset` en Dagster, `task` (una función decorada)
  en Prefect.
- **Ejecución:** una instancia del grafo para una fecha o partición concreta. Su identidad es el par
  formado por el grafo y su clave lógica:
  - Airflow: `(dag_id, logical_date)`, con `data_interval = [logical_date, logical_date + schedule)`.
  - Dagster: `(job, partition_key)`, por ejemplo `ventas_por_provincia` con `partition_key = "2024-03-14"`.
  - Prefect: `flow_run_id`, con los parámetros que le pases.
- **Partición:** en Dagster es un concepto de primer nivel. `DailyPartitionsDefinition(start_date=...)`
  parte un activo por día y `StaticPartitionsDefinition([...])` por una lista fija de valores, como
  países o tiendas. Reprocesar es «materializar la partición del 14 de marzo», y nada más.
- **Programación:** una expresión cron (`"0 3 * * *"`), un intervalo (`timedelta`) o un disparador
  por evento.
- **Sensor o automatización:** una espera sobre algo externo (un fichero en un almacén de objetos,
  una tabla que aparezca) o sobre otra ejecución (que el activo anterior esté al día).

La semántica que más confunde, y que es igual en los tres aunque se llame distinto: **la clave
lógica marca el inicio del intervalo de datos, y la ejecución se dispara al cerrarlo**:

:::formula
ejecución con logical_date = t procesa [t, t + periodo) y se dispara en t + periodo
:::

Una programación diaria con `start_date` del 1 de marzo y `catchup` activo crea una ejecución por
día, identificada por el inicio de su intervalo. La ejecución lanzada el 15 de marzo a las 3:00 es
la de `logical_date = 14 de marzo a las 3:00`, y su intervalo de datos es
`[14 de marzo 3:00, 15 de marzo 3:00)`. De ahí sale el clásico «el informe del 15 lleva datos del
14», que no es un fallo: es la definición. La trampa está en que `{{ ds }}` es el inicio del
intervalo, no el día en que la ejecución arranca, así que la consulta que lo use lee el día
anterior al del reloj.

Comparación de los tres, sin entrar en gustos:

| Aspecto | Airflow | Dagster | Prefect |
| --- | --- | --- | --- |
| Unidad que describes | Tarea | Activo (dato producido) | Función decorada |
| Cómo se declara el grafo | Operadores encadenados con `>>` en un fichero de DAG | Dependencias tipadas entre funciones | Decoradores sobre tu propio código |
| Cuándo se construye el grafo | Al leer el fichero, en cada ciclo del planificador | Al cargar las definiciones | En tiempo de ejecución |
| Linaje y catálogo | Hay que añadirlos aparte | De serie, porque el activo declara qué produce | Parcial, según integraciones |
| Pruebas en local | Necesitan entorno y simulaciones | Ejecución del activo en proceso | Es Python normal, sin más |
| Dónde lo verás | Empresas grandes y muchas ofertas | Equipos con problema de gobierno del dato | Proyectos nuevos y equipos pequeños |

## Ejemplo

Mismo pipeline en los tres: extraer, limpiar y cargar, con programación diaria a las 3:00.

En **Airflow** escribes el grafo aparte y Airflow te da la fecha lógica en la plantilla `{{ ds }}`:

```text
dag_id       = ventas_diarias
schedule     = "0 3 * * *"
start_date   = 2024-03-01 03:00
catchup      = True
max_active_runs = 1

extraer >> limpiar >> cargar
```

En **Dagster** describes los activos y su partición diaria:

```text
activo ventas_crudas       particion diaria desde 2024-03-01
activo ventas_limpias      depende de ventas_crudas
activo ventas_por_provincia depende de ventas_limpias
```

Y reprocesar el 14 de marzo es materializar esa partición, sin lanzar el grafo entero.

En **Prefect** el grafo es tu código: `ventas_diarias("2024-03-14")` es una ejecución con ese
parámetro, y el registro vive en la API del propio Prefect.

En los tres casos, un reproceso del 8 al 14 de marzo son **7 ejecuciones**, una por día, cada una con
su clave lógica. Si tus tareas son idempotentes, esas 7 ejecuciones pueden correr en paralelo; si no
lo son, lanzarlas juntas duplica datos y el problema no es del orquestador.

## Código

```python verificable
from datetime import datetime, timedelta

# La fecha logica marca el INICIO del intervalo de datos, no el dia del disparo.
inicio_dag = datetime(2024, 3, 1, 3, 0)      # start_date de la programacion "0 3 * * *"

for desplazamiento in (0, 12, 13):
    logical_date = inicio_dag + timedelta(days=desplazamiento)
    fin_intervalo = logical_date + timedelta(days=1)
    print(f"logical_date {logical_date:%m-%d %H:%M} cubre "
          f"[{logical_date:%m-%d %H:%M}, {fin_intervalo:%m-%d %H:%M}) "
          f"y se dispara el {fin_intervalo:%m-%d %H:%M}")

desde, hasta = datetime(2024, 3, 8, 3, 0), datetime(2024, 3, 15, 3, 0)
print("ejecuciones del reproceso 8-14 de marzo:", (hasta - desde).days)   # -> ejecuciones del reproceso 8-14 de marzo: 7
```

```python ilustrativo
# Airflow: el grafo se declara en un fichero que el planificador lee cada pocos segundos,
# asi que aqui no va logica de negocio, solo la estructura y las llamadas.
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"retries": 3, "retry_delay": timedelta(minutes=5)}

with DAG(
    dag_id="ventas_diarias",
    start_date=datetime(2024, 3, 1, 3, 0),
    schedule="0 3 * * *",
    catchup=True,
    max_active_runs=1,
    default_args=default_args,
) as dag:
    # {{ ds }} es la fecha logica: lo que permite reprocesar sin tocar el presente.
    extraer = BashOperator(task_id="extraer", bash_command="python -m etl.extraer --ds {{ ds }}")
    limpiar = BashOperator(task_id="limpiar", bash_command="python -m etl.limpiar --ds {{ ds }}")
    cargar = BashOperator(task_id="cargar", bash_command="python -m etl.cargar --ds {{ ds }}")

    extraer >> limpiar >> cargar
```

```python ilustrativo
# Dagster: se declara lo que se PRODUCE y el grafo de tareas se deduce de ahi.
import dagster as dg

@dg.asset(partitions_def=dg.DailyPartitionsDefinition(start_date="2024-03-01"))
def ventas_crudas(context: dg.AssetExecutionContext) -> None:
    extraer(context.partition_key)          # "2024-03-14"

@dg.asset
def ventas_limpias(ventas_crudas: None) -> None:
    limpiar()

@dg.asset
def ventas_por_provincia(ventas_limpias: None) -> None:
    agregar()

# Prefect: el grafo es el propio codigo; nada de un fichero de DAG aparte.
from prefect import flow, task

@task(retries=3, retry_delay_seconds=300)
def extraer_prefect(dia: str) -> None:
    extraer(dia)

@flow
def ventas_diarias(dia: str) -> None:
    extraer_prefect(dia)

if __name__ == "__main__":
    ventas_diarias("2024-03-14")
```

## Errores típicos

- **Meter lógica de negocio en el fichero del DAG (Airflow).** El planificador evalúa ese fichero
  cada pocos segundos: si ahí consultas una base de datos o recorres una lista enorme, ralentizas el
  orquestador para todos los equipos. El fichero declara el grafo y llama a funciones de un paquete
  aparte.
- **Usar `datetime.now()` dentro de una tarea.** Rompe el reproceso: al relanzar el 14 de marzo, la
  tarea escribe datos del día en que la lanzas. Usa siempre la fecha lógica: `{{ ds }}` en Airflow,
  `context.partition_key` en Dagster, el parámetro del `@flow` en Prefect.
- **Reprocesar sin límite de ejecuciones simultáneas.** Un reproceso de 90 días sin control puede
  lanzar 90 ejecuciones a la vez y tumbar la base de datos de origen. Empieza con pocas y sube.
- **Elegir el orquestador por moda.** Migrar cuesta meses y casi nunca arregla el problema real, que
  suele ser que las tareas no son idempotentes, que no hay pruebas de calidad o que nadie mira las
  alertas. Arregla eso primero; luego, si hace falta, cambia de herramienta.
- **Dejar el orquestador sin alertas.** Un DAG que falla a las 3:00 y del que nadie se entera hasta
  que alguien pide el informe a las 10:00 no es un orquestador: es un registro de fallos con una
  interfaz bonita ([[observabilidad-de-datos]]).
- **Confundir el estado del orquestador con el estado del dato.** Que la tarea esté en verde
  significa que el proceso terminó sin error, no que la tabla tenga las filas correctas. Son dos
  cosas distintas y necesitan comprobaciones distintas ([[calidad-y-slas]]).

## Comprueba que lo sabes

:::quiz
p: ¿Qué cambia Dagster respecto a Airflow en la forma de describir un pipeline?
o: Describe los datos que se producen (activos) y el grafo de tareas se deduce de esas dependencias
o: No permite programar por calendario, solo por eventos
o: Ejecuta las tareas en orden aleatorio para probar la robustez
a: 1
e: El modelo de activos pone el foco en el resultado —la tabla, el fichero, el modelo— y de ahí salen el linaje y el catálogo sin trabajo extra. Dagster programa por calendario igual que los otros; lo que cambia es qué declaras primero.
:::

:::quiz
p: Una tarea de Airflow decide qué partición lee con `datetime.now()`. ¿Cuál es la consecuencia?
o: Ninguna, porque Airflow siempre ejecuta en tiempo real
o: Que el reproceso de una fecha pasada escribe datos del día en que se lanza, no de la fecha pedida
o: Que la tarea tarda más porque consulta el reloj del sistema
a: 2
e: La fecha lógica es la identidad de la ejecución y es lo único que hace reproducible un reproceso. Si la tarea mira el reloj del sistema, dos ejecuciones con la misma fecha lógica producen resultados distintos y el histórico deja de ser fiable.
:::

:::nota
Los tres orquestadores están en producción en empresas serias y los tres son buena elección.
Airflow es el que más aparece en las ofertas de empleo, así que merece la pena saber leer un DAG
aunque acabes trabajando con Dagster o con Prefect.
:::
