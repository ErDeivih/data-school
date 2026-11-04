---
id: fuentes-y-canales
titulo: Fuentes, canales y datos
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar, practicar-con-datos-reales]
tags: [recursos, canales, datos]
resumen: Dónde aprender cada fase, qué fuente sirve para qué y por qué seis activas bastan: el mapa de recursos con enlaces directos.
fuentes: ["DataTalksClub (2020), 'Data Engineering Zoomcamp'", "Start Data Engineering (2021), 'Start Data Engineering blog'"]
---

## En una frase

Cada fase del portal tiene una o dos fuentes que la cubren de verdad; el trabajo no es
coleccionarlas, es elegir seis, dejarlas fijas un trimestre y volver a ellas.

## La idea

Existen miles de horas de vídeo sobre datos. Casi todas repiten lo mismo con distinto acento, y
una minoría cubre lo que de verdad cuesta: idempotencia, modelado con grano, coste, calidad y
diagnóstico de fallos. El problema del que empieza no es la falta de material, es la abundancia:
veinte canales abiertos y ningún proyecto terminado.

Este mapa está organizado por fase, no por popularidad. Una fuente entra si cumple tres cosas:
cubre una fase que el portal no cubre con su propia página, **enseña con código o con un caso
real**, y tiene una advertencia honesta (vende algo, está desfasada o es superficial). Lo que no
cumple las tres no está.

Y una regla que gobierna el resto: **seis fuentes activas como máximo**. Una para el currículo,
una de práctica diaria, una de referencia, una de fondo, una de actualidad y una que alimente tu
proyecto. Cambiar una exige una razón escrita; «he visto un canal nuevo» no es una razón.

:::trampa
Ver un vídeo no es estudiar. El vídeo entra por los ojos y se olvida en dos días si no se
convierte en una pregunta escrita, un ejemplo ejecutado o una tarjeta de repaso. La regla es la
misma que en [[como-estudiar]]: una idea por vídeo, apuntada como pregunta, y el concepto abierto
en el portal después.
:::

## Definición formal

Una fuente se elige por cuatro criterios y se descarta si falla el tercero:

:::parametros
| Criterio | Qué mide | Cómo se comprueba en cinco minutos | Si falla |
| --- | --- | --- | --- |
| Cobertura | Cubre una fase del portal y no repite otra fuente | Busca tres temas difíciles de F04 o F11 y comprueba si están | Es una fuente de repaso, no de estudio |
| Código o caso real | Hay un repositorio, una consulta ejecutable o un caso con números | Abre dos vídeos al azar y busca código en pantalla | Es divulgación: sirve para motivarse, no para aprender |
| Honestidad | Dice qué no funciona, qué está desfasado y qué vende | Lee la descripción y los comentarios fijados | Si solo hay promesas, fuera |
| Densidad | Aporta algo que no tengas ya en el temario | Compara con las páginas de la fase | Es coleccionismo |
:::

La **ficha de una fuente** tiene cinco campos: qué cubre, a qué fase sirve, qué aporta que no
aporte otra, qué le falta y con qué se complementa. Sin los dos últimos campos, una lista de
recursos es publicidad.

## Ejemplo

Así se eligen las seis de un primer trimestre, con el criterio de arriba aplicado:

| Puesto | Fuente | Fase | Por qué esa y no otra |
| --- | --- | --- | --- |
| Currículo | [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) | F03, F04 | Es la única secuencia gratuita completa: Docker, Terraform, Airflow, dbt, Spark y Kafka con deberes |
| Práctica | [PostgreSQL Exercises](https://pgexercises.com/) | F03 | 80 ejercicios con solución y sin registro; el SQL se aprende tecleando |
| Referencia | [Documentación de Airflow](https://airflow.apache.org/docs/) | F04 | Idempotencia, backfill y reintentos explicados por quien los implementa |
| Fondo | [StatQuest](https://www.youtube.com/@statquest) | F02, F06 | La intuición de estadística y ML en vídeos de diez minutos |
| Actualidad | [Data Engineering Weekly](https://www.dataengineeringweekly.com/) | F04, F08 | Una hora a la semana cubre «estar al día» sin redes sociales |
| Proyecto | [NYC TLC Trip Records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | F04, F05 | Datos reales y sucios, con licencia limpia, para el primer pipeline serio |

Las seis caben en una tarde de configuración y cubren F03, F04, F02 y F06. La ruta quant no
aparece a propósito: en el primer trimestre no toca.

## Código

```text
FICHA DE FUENTE (rellenar antes de añadirla a la lista activa)

  nombre:       Data with Zach
  enlace:       https://www.youtube.com/c/datawithzach
  fase:         F04, F12
  cubre:        entrevista tecnica de data engineering e idempotencia
  aporta:       el "como lo harias en produccion", con casos reales
  le falta:     los videos buenos son de 2022 y usa versiones antiguas
  complemento:  la documentacion oficial para las versiones actuales
  fecha:        2026-11-02
```

Ese bloque es el formato que se guarda en el registro de fuentes. Un recurso sin ficha es un
marcador que no vas a volver a abrir.

## Las fuentes, por fase

**F03 · Python y SQL**

| Fuente | Qué aporta | Advertencia |
| --- | --- | --- |
| [PostgreSQL Exercises](https://pgexercises.com/) | La mejor progresión de SQL con solución explicada | Nada de modelado, solo consultas |
| [DataLemur](https://datalemur.com/) | Preguntas SQL de entrevista real | Formato entrevista, no fundamentos |
| [8 Week SQL Challenge](https://8weeksqlchallenge.com/) | Ocho casos de negocio completos | Requiere saber SQL antes de empezar |
| [MoureDev](https://www.youtube.com/@mouredev) | Python, Git y testing en español de España | Es desarrollo general, no datos |

**F04 · Ingeniería de datos**

| Fuente | Qué aporta | Advertencia |
| --- | --- | --- |
| [DataTalksClub](https://www.youtube.com/@DataTalksClub) | Currículo completo y gratuito | Las playlists viejas están desfasadas |
| [Seattle Data Guy](https://www.youtube.com/@SeattleDataGuy) | Cómo se rompe un pipeline en producción | Poco código denso |
| [Andreas Kretz](https://www.youtube.com/c/andreaskayy) | Arquitectura y porqués: batch frente a streaming | Formato antiguo y empuja su curso |
| [Kahan Data Solutions](https://www.youtube.com/@KahanDataSolutions) | dbt y Airflow en serio | Muy centrado en el modern data stack |
| [Start Data Engineering](https://www.startdataengineering.com/) | Tests, contratos y observabilidad | Publica poco, pero muy bueno |
| [Data Engineering LATAM](https://www.youtube.com/@DataEngineeringLatam) | Lo mismo en español, por playlists | Nivel introductorio |
| [Documentación de dbt](https://docs.getdbt.com/) | Materializaciones, tests y contratos | Es referencia, no curso |

**F11 · Software y sistemas**

| Fuente | Qué aporta | Advertencia |
| --- | --- | --- |
| [Martin Fowler](https://martinfowler.com/) | Arquitectura, patrones y testing | No es de datos: es el criterio de diseño |
| [Pelado Nerd](https://www.youtube.com/@peladonerd) | Docker, Linux y redes en español | Informal y muy largo |

**F02, F05 y F06 · Estadística, series y ML**

| Fuente | Qué aporta | Advertencia |
| --- | --- | --- |
| [StatQuest](https://www.youtube.com/@statquest) | Intuición visual de estadística y ML | Ligero en matemáticas formales |
| [Codificando Bits](https://www.youtube.com/@codificandobits) | Series temporales y ML en español | Producción pausada |

**F09 · Quant**

| Fuente | Qué aporta | Advertencia |
| --- | --- | --- |
| [QuantPy](https://www.youtube.com/@QuantPy) | Opciones, Monte Carlo y carteras con código | Parte del contenido nuevo es promoción |
| [Robot Wealth](https://robotwealth.com/) | Resultados que no funcionan, y por qué | Blog, no curso |
| [QuantDare](https://www.quantdare.com/) | Quant en español con rigor | Menos actualizado que los blogs grandes |

**Datos para los proyectos de [[portfolio-y-proyectos]]**

| Fuente | Qué permite | Aviso |
| --- | --- | --- |
| [NYC TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | Pipeline por lotes con Parquet y particiones | Decenas de GB el histórico |
| [Chicago Crimes](https://data.cityofchicago.org/) | Ingesta incremental y datos sucios | ~8 millones de filas |
| [GH Archive](https://gharchive.org/) | Eventos por hora para streaming | 1-3 GB al día |
| [Open-Meteo](https://open-meteo.com/) | Enriquecer con meteorología, sin clave | Gratis para uso no comercial |
| [INE](https://www.ine.es/) | Datos españoles con API | Documentación árida |
| [AEMET](https://opendata.aemet.es/) | API con clave y límite de peticiones | Requiere registro |
| [CityBikes](https://api.citybik.es/v2/) | Kafka sin infraestructura | API pública y pequeña |

## Errores típicos

- **Coleccionar fuentes en vez de terminar una.** Veinte canales abiertos y ningún proyecto
  cerrado es el estado natural de quien empieza. La lista activa es de seis.
- **Ver vídeos sin libreta.** Sin una pregunta escrita o un ejemplo ejecutado, el vídeo no deja
  nada. La prueba es simple: al día siguiente, ¿puedes explicarlo sin mirar?
- **Confundir divulgación con formación.** Un canal que resume un paper en diez minutos sirve para
  saber que existe, no para implementarlo.
- **Usar solo una fuente para todo.** Ninguna cubre F03, F04 y F11 bien. Si tu única fuente es un
  canal de YouTube, tu formación tiene la forma de ese canal.
- **Cambiar de fuente cuando algo se pone difícil.** El aburrimiento en la fase 4 es parte del
  proceso; cambiar de canal no lo resuelve, lo pospone.
- **No comprobar la licencia de los datos.** Publicar un portfolio con datos que no puedes
  redistribuir es un problema legal, no un detalle. Comprueba la licencia antes de subir nada.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el criterio que descarta una fuente aunque sea popular?
o: Que no enseñe con código ni con un caso real, o que no admita sus propios límites
o: Que tenga pocos suscriptores
o: Que esté en inglés
a: 1
e: La popularidad no dice nada sobre la densidad. Una fuente entra si cubre una fase, enseña con código o con un caso real y dice qué le falta. Sin lo tercero, es publicidad con buena edición.
:::

:::quiz
p: Ya tienes seis fuentes activas y descubres un canal nuevo que parece mejor que uno de los seis. ¿Qué haces?
o: Sustituir la que peor esté funcionando, después de comprobar los cuatro criterios y escribir el motivo
o: Añadirlo: siete no es tanto
o: Dejarlo para más adelante y no volver a mirarlo
a: 1
e: La regla de seis existe para forzar la comparación. Si el canal nuevo cubre mejor una fase, entra y sale el que peor cumple; si no, se apunta y no se consume. Acumular sin sustituir es la forma más común de no aprender nada.
:::
