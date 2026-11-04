---
id: rutas-de-aprendizaje
titulo: Rutas de aprendizaje
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [mapa-del-portal, como-estudiar]
tags: [ruta, plan, orden]
resumen: Las cuatro rutas completas —data engineer, data scientist, IA y quant— con el orden de cada paso y lo que hay que saber antes de empezar cada uno.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering'", "DataTalksClub (2020), 'Data Engineering Zoomcamp'"]
---

## En una frase

Una ruta no es una lista de temas: es una secuencia de dependencias, y cada paso dice qué hace
falta tener resuelto antes de empezar.

## La idea

El portal ya avisa en cada ficha: arriba aparecen los requisitos y cuántos llevas. Esta página
explica **cómo se lee ese aviso** y da las cuatro rutas enteras, para que no tengas que adivinar
qué va antes de qué.

La regla que ordena todo es simple: no empieces un paso si el anterior no te sale sin mirar. Un
concepto que solo has leído se olvida; uno que has usado en un ejercicio se queda. Por eso cada
paso de las rutas lleva un ejercicio o un proyecto, no solo lecturas.

Y una advertencia: las rutas son cuatro, pero **no se hacen a la vez**. Elegir una y llegar al
final vale más que empezar las cuatro.

## Definición formal

Cada ruta se compone de cuatro tramos y cada tramo tiene una puerta de salida:

:::parametros
| Tramo | Qué se aprende | Antes necesitas | Puerta de salida |
| --- | --- | --- | --- |
| Base | Herramientas y matemáticas mínimas | Nada | Sabes leer un CSV, hacer un `JOIN` y calcular una media con su desviación |
| Oficio | Ingesta, modelado, calidad | Base | Un pipeline que se reejecuta sin duplicar |
| Análisis | Estadística y modelos | Oficio | Un modelo validado fuera de muestra con su métrica justificada |
| Sistema | Servir, operar y explicar | Análisis | Un servicio o panel que otra persona usa sin tu ayuda |
:::

- **Base** — F00 a F03: cómo estudiar, notación, Python, SQL, probabilidad y estadística descriptiva.
- **Oficio** — F04: el trabajo diario de un data engineer.
- **Análisis** — F02, F05, F06: inferencia, series temporales y machine learning.
- **Sistema** — F08, F11, F12: servir, operar y comunicar.

## Ejemplo

**Ruta de data engineer**, mes a mes, con lo que hay que aprender en cada tramo:

| Mes | Qué estudias | Qué necesitas antes | Qué entregas |
| --- | --- | --- | --- |
| 1 | [[entorno-python]], SQL básico, `practicar-con-datos-reales` | Nada | Un cuaderno que carga un CSV y lo describe |
| 2 | [[ingesta-incremental-y-cdc]], [[parquet-avro-orc]], [[calidad-de-datos]] | Python y SQL | P11: limpiar y unir la telemetría de una carrera |
| 3 | [[modelado-dimensional]], [[dbt-y-transformacion]] | Ingesta | P20: modelo en estrella de partidos |
| 4 | [[airflow-dagster-prefect]], [[idempotencia-y-reintentos]] | Modelado | P17: ingesta desde API que no duplica |
| 5 | [[kafka-y-colas]], [[ventanas-y-watermarks]] | Orquestación | PF-03 de [[portfolio-y-proyectos]] |
| 6 | [[iam-y-permisos-cloud]], [[coste-y-optimizacion]] | Todo lo anterior | Certificación media de [[certificaciones-de-datos]] |

**Ruta de data scientist:** base igual, después F02 (inferencia) y F05 (series) antes de F06. La
puerta de salida es un modelo con validación temporal y métrica elegida por el coste del error.

**Ruta de IA aplicada:** base igual, después F06 y F07 para entender qué hay dentro, y F08 para
construir con modelos. La puerta es un RAG con evaluación, no una demo.

**Ruta de quant:** base fuerte en F01 (probabilidad y cálculo) y F02, después F09. La puerta es un
backtest con costes y validación, no un gráfico bonito.

## Código

```text
COMO SE LEE EL AVISO DE REQUISITOS DE CADA FICHA

  Requisitos: 1 de 5        te falta casi todo: empieza por los enlazados
  Antes de este: 0 de 2     los prerrequisitos directos, los que de verdad hacen falta

  Regla practica:
    - Si te faltan mas de dos, no leas esta ficha entera: lee el prerrequisito y vuelve.
    - Si te falta uno y es de otra fase, leelo igual: son 20 minutos.
    - Si no te falta ninguno, haz el problema practico antes de marcarla.
```

## Errores típicos

- **Empezar por la fase 9 porque es la que suena interesante.** Sin base, la ruta quant se
  convierte en memorizar nombres de métricas.
- **Saltarse la base porque «ya sé Python».** Saber Python no es saber SQL, ni validar, ni modelar.
  La base incluye las tres cosas.
- **Hacer las cuatro rutas a la vez.** Ninguna llega al final. Elige una y usa las otras como
  cultura, no como plan.
- **Leer sin hacer el problema práctico.** La puerta de cada tramo es un entregable, no una
  lectura.
- **Cambiar de ruta cuando algo cuesta.** El tramo de oficio es cuesta arriba para todo el mundo;
  cambiar de ruta no lo evita, lo retrasa.
- **Ignorar el aviso de requisitos.** Está para ahorrarte el tiempo de leer algo que no vas a
  entender todavía.

:::practica
enunciado: Estás en el mes 2 de la ruta de data engineer y te apetece mirar opciones. ¿Qué dos fichas de F09 puedes leer sin romper el orden y cuáles no?
pista: Mira los prerrequisitos de las fichas de F09: algunas solo piden conceptos de F01.
solucion: Puedes leer las que dependen solo de probabilidad y estadística, como las de riesgo y métricas, porque F01 ya está cubierto. No deberías entrar en las de derivados ni en las de cobertura: piden cálculo estocástico y álgebra que aún no has hecho. La regla es mirar los prerrequisitos, no la fase.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa «Antes de este: 1 de 3» en una ficha?
o: Que de los tres prerrequisitos directos solo tienes uno hecho
o: Que la ficha está al 33 % de completarse
o: Que faltan tres fichas para terminar la fase
a: 1
e: El aviso cuenta los prerrequisitos directos que ya has marcado. No mide tu progreso en la ficha ni el de la fase: mide si puedes entender lo que viene.
:::

:::quiz
p: ¿Cuál es la puerta de salida del tramo de oficio en la ruta de data engineer?
o: Un pipeline que se reejecuta sin duplicar
o: Haber leído toda la fase F04
o: Un certificado de un curso
a: 1
e: El tramo se cierra con un entregable que demuestra el oficio: reejecutar sin duplicar, con tests y con una tabla final reproducible. Leer la fase entera no lo demuestra.
:::
