# Fuentes para aprender datos: lo que falta en `RECURSOS.md`

**Fecha:** 2026-11-02 · **Comprobación:** abrí y leí ese día las dos fuentes de mercado (§6), el
roadmap en español, el libro de patrones y los enlaces de Instagram. El resto de URLs procede de
la investigación y no las he abierto una a una: si alguna falla, busca el recurso por su nombre.
Antes de fiarte de un enlace, pruébalo; cuesta dos segundos.

`RECURSOS.md` ya tiene lo esencial: SharpeEdge, StatQuest, 3Blue1Brown, Kaggle, roadmap.sh,
el Zoomcamp, `Use the Index Luke`, FRED, datos.gob.es. **Esta página no lo repite.** Añade lo que
falta para data engineering —que es mucho— y dice qué fuentes son de consulta y cuáles de
estudio.

**Regla que gobierna todo lo demás:** no más de **6-8 fuentes activas** a la vez. El error caro
no es elegir mal el canal; es coleccionar canales. Marca las tuyas en la última sección y no las
cambies hasta cerrar un proyecto.

---

## 1. Canales de vídeo que no están en `RECURSOS.md`

### 1.1 Ingeniería de datos (lo que de verdad hace un DE)

| Canal | URL | Idioma | Fase | Qué aporta | Advertencia |
| --- | --- | --- | --- | --- | --- |
| DataTalksClub | `youtube.com/@DataTalksClub` | EN | F03, F04 | La única **secuencia completa y gratuita** (Docker → Terraform → Airflow → dbt/BigQuery → Spark → Kafka) con deberes y cohortes | Las playlists de años anteriores están desfasadas; sigue el repo del año en curso |
| Seattle Data Guy | `youtube.com/@SeattleDataGuy` | EN | F04, F12 | Consultoría real: por qué se cae un pipeline, cómo se negocia con negocio, cuánto se paga | Deriva a negocio del dato; poco código denso |
| Andreas Kretz | `youtube.com/c/andreaskayy` | EN | F04, F11 | Arquitectura y **porqués**: batch frente a streaming, lambda/kappa, separar cómputo y almacenamiento | Formato antiguo y empuje a su curso de pago; filtra |
| Data with Zach | `youtube.com/c/datawithzach` | EN | F04, F12 | Lo mejor en **entrevista DE**: idempotencia, SCD, modelado, «cómo lo harías en producción» | Su gratis es escaparate de su bootcamp; los vídeos buenos son de 2022-2023 |
| Darshil Parmar | `youtube.com/@DarshilParmar` | EN | F04, F03 | Proyectos **end-to-end** con AWS/GCP/Azure, Airflow, Spark y Kafka, con repositorio público | Muy AWS-céntrico y a veces copiar y pegar; los proyectos no siempre cubren tests ni coste |
| Kahan Data Solutions | `youtube.com/@KahanDataSolutions` | EN | F04, F11 | **dbt y Airflow en serio**: incremental models, snapshots, tests, CI/CD de transformaciones | Canal pequeño y muy centrado en el modern data stack |
| Start Data Engineering | `youtube.com/@startdataengineering` | EN | F04, F11 | **Calidad de ingeniería aplicada a datos**: tests, contratos, observabilidad, código mantenible | Produce poco vídeo; el contenido vive en su blog (§2) |
| Databricks (oficial) | `youtube.com/@Databricks` | EN | F04, F07 | Fuente **autoritativa** de Spark, Delta Lake y lakehouse | Marketing: ve a las sesiones técnicas, no a los keynotes |
| Snowflake (oficial) | `youtube.com/@SnowflakeInc` | EN | F04 | Almacén cloud: micro-particiones, clustering, *zero-copy*, coste | También es marketing, y su forma de hacer las cosas no se traduce a otros almacenes |
| E-Learning Bridge | `youtube.com/@shashank_mishra` | EN/HI | F04, F10 | **Big data clásico**: particiones, shuffles, executors, Kafka, preguntas de entrevista | Acento marcado (subtítulos) y series con Spark antiguo: verifica versiones |

### 1.2 Transversal: código, sistema y español

| Canal | URL | Idioma | Fase | Qué aporta | Advertencia |
| --- | --- | --- | --- | --- | --- |
| MoureDev (Brais Moure) | `youtube.com/@mouredev` | ES | F03, F11 | El mejor sitio **en español** para arreglar Python, Git, testing y backend sin pagar | Es desarrollo general, no datos; algunas series tienen 2-4 años |
| Pelado Nerd | `youtube.com/@peladonerd` | ES | F11 | Docker, Kubernetes, Linux, redes: lo que te falta cuando el DAG muere en el contenedor | Informal y muy largo; no es curso estructurado |
| Codificando Bits | `youtube.com/@codificandobits` | ES | F02, F05, F06 | **Series temporales y ML en español con rigor**: estacionariedad, ARIMA, validación temporal | Canal pequeño y producción pausada |
| codebasics | `youtube.com/@codebasics` | EN | F03 | Python y SQL desde cero con ritmo de principiante real | Orientado a analista; mucho curso patrocinado |
| Alex The Analyst | `youtube.com/@AlexTheAnalyst` | EN | F03, F12 | Cómo consume los datos el usuario final: BI, portfolio, entrevistas de analista | No es DE; como canal principal te haría perder meses en Power BI |
| PyQuant News | `youtube.com/@PyQuantNews` | EN | F09 | Puente **data engineering ↔ trading**: ingesta de precios, ticks, pipelines de mercado | Formato corto y promocional de su newsletter |
| Value School (podcast) | `youtube.com/@ValueSchool` | ES | F09, F12 | Cultura financiera en español con conferenciantes serios | Es *value investing*, cero estadística: nunca como fuente cuantitativa |

### 1.3 Canales en español que sí existen (y de qué sirven)

Decir que «no hay nada en español» es falso: hay una comunidad de ingeniería de datos latina
bastante activa. Lo que falta es profundidad en la parte difícil.

| Canal | URL | Fase | Qué aporta | Advertencia |
| --- | --- | --- | --- | --- |
| Data Engineering LATAM | `youtube.com/@DataEngineeringLatam` | F03, F04 | SQL, Spark, Airflow, Azure y AWS **en español**, por playlists temáticas | Nivel introductorio-intermedio; poca cosa de producción o coste |
| CodinEric | `youtube.com/@CodinEric` | F04, F11 | Testing de datos y buenas prácticas (incluida una charla de Great Expectations en PyConAr) | Producción irregular |
| The LATAM Engineer | `youtube.com/@TheLATAMEngineer` | F11 | Mentalidad DevOps aplicada a datos: de local a producción | Pocos vídeos y muy largos |
| Dateneo | `youtube.com/@Dateneo` | F04 | Conceptos de plataforma y ecosistema, en español neutro | Divulgación, no implementación |
| Datademia | `youtube.com/@datademia` | F03 | Fundamentos de programación, línea de comandos y estadística | Muy básico |
| Dot CSV | `youtube.com/@DotCSV` | F06, F07 | Divulgación de IA con rigor y entusiasmo | No es formación técnica sistemática |
| AprendeIA (Ligdi Gonzalez) | `youtube.com/@aprendeIA` | F06, F07 | ML y deep learning en español, con cuadernos | Orientado a DS, no a DE |

**El hueco real:** data engineering moderno a nivel intermedio-avanzado (dbt, Iceberg, streaming
de verdad, idempotencia con particiones, coste). En español hay mucho «qué es un data lake» y
poco «cómo hago un merge incremental que no duplique». Ahí tiras de Kahan, Start Data Engineering
y la documentación oficial.

---

## 2. Blogs y newsletters (consulta semanal, no lectura)

| Recurso | URL | Fase | Por qué |
| --- | --- | --- | --- |
| Start Data Engineering | `startdataengineering.com` | F04, F11 | Pipelines como **software**: tests, entornos, CI/CD, calidad. La mejor escritura del sector |
| Data Engineering Weekly | `dataengineeringweekly.com` | F04, F08 | Mejor relación señal/ruido para «estar al día» sin Twitter |
| Seattle Data Guy (blog) | `blog.dataengineer.io` | F04, F12 | Casos de empresa y salarios; prepara «cuéntame un proyecto» |
| Simon Späti | `ssp.sh` | F04, F12 | Ensayos técnicos y entrevistas; entrena F12 (comunicar decisiones) |
| The Analytics Engineering Roundup | `roundup.getdbt.com` | F04, F12 | Antídoto contra el «tool-first»: organización, contratos, propiedad del dato |
| Dagster Blog | `dagster.io/blog` | F04, F11 | La mejor explicación de la diferencia entre *tarea* y *activo de datos* |
| Databricks Blog | `databricks.com/blog` | F04, F07 | Artículos profundos de Spark y Delta; benchmarks y funcionamiento interno |
| Spotify Engineering | `engineering.atspotify.com` | F04, F11, F12 | Plataformas de datos a escala, publicadas con detalle |
| Martin Fowler | `martinfowler.com` | F11 | Arquitectura, patrones, testing, refactoring. Evita que escribas pipelines como scripts de 800 líneas |
| Locally Optimistic | `locallyoptimistic.com` | F04, F12 | Equipos pequeños de datos, con experiencia real |
| Benn Stancil | `benn.substack.com` | F12, F08 | No enseña herramientas: enseña a pensar el stack y el BI |
| The Data Engineering Podcast | `dataengineeringpodcast.com` | F04, F12 | Casi 700 episodios: buscas la herramienta y escuchas a quien la construyó |
| QuantDare | `quantdare.com` | F09, F02 | Prácticamente el único blog quant **en español** con rigor y continuidad |
| Robot Wealth | `robotwealth.com` | F09, F05 | De los pocos que publica resultados que **no** funcionan, y por qué |
| Quantocracy | `quantocracy.com` | F09 | Agregador diario del ecosistema quant; radar, no lectura |

---

## 3. Práctica (aquí se aprende, no se mira)

| Recurso | URL | Fase | Qué entrena |
| --- | --- | --- | --- |
| PostgreSQL Exercises | `pgexercises.com` | F03 | 80+ ejercicios de SQL con solución explicada y sin registro. La mejor progresión que existe |
| SQLBolt | `sqlbolt.com` | F03 | SQL interactivo desde cero; 20 minutos al día y sabes `JOIN` |
| SQLZoo | `sqlzoo.net` | F03 | Drills de `GROUP BY` y subconsultas con evaluación automática |
| DataLemur | `datalemur.com` | F03, F12 | Preguntas SQL de entrevista real; entrena el formato de la prueba |
| StrataScratch | `stratascratch.com` | F03 | Problemas SQL y Python de entrevistas; plan gratuito limitado |
| 8 Week SQL Challenge | `8weeksqlchallenge.com` | F03, F04 | 8 casos de negocio completos: obliga a modelar y responder preguntas, no a resolver juguetes |
| NeetCode | `neetcode.io` | F10 | 150 problemas con ruta por patrones; el gimnasio de algoritmos |
| DEDP (Design Patterns for Data Engineering) | `dedp.online` | F04, F11 | Libro gratuito de patrones de sistemas de datos (ingesta, modelado, serving) |
| Data Engineering Handbook | `github.com/DataExpert-io/data-engineer-handbook` | F00, F12 | Índice enorme de recursos; úsalo para contrastar el temario, no como plan |
| Roadmap DE en español | `natayadev.github.io/dataengineering-roadmap` | F00 | Curación de material gratuito en español, ordenado por nivel |

---

## 4. Cursos y certificaciones: qué pesa y qué no

### Gratis de verdad

| Recurso | URL | Fase | Veredicto |
| --- | --- | --- | --- |
| Data Engineering Zoomcamp | `github.com/DataTalksClub/data-engineering-zoomcamp` | F03, F04 | **El mejor retorno por hora del documento.** 9 semanas, pipeline completo. El certificado no vale; el repositorio final, sí |
| dbt Fundamentals | `learn.getdbt.com/courses/dbt-fundamentals` | F04 | Curso oficial de ~5 h con certificado gratis. El vocabulario mínimo del transform moderno |
| Confluent Developer | `developer.confluent.io/courses` | F04 | El mejor material gratuito de Kafka: vídeo, código y ejercicios |
| freeCodeCamp Relational Database | `freecodecamp.org/learn/relational-database` | F03 | Bash + PostgreSQL + Git con certificación gratuita y verificable |
| CS50x | `cs50.harvard.edu/x` | F03, F10, F11 | Fundamentos de verdad; duro si vienes de cero, pero elimina lagunas que frenan F10/F11 |
| Microsoft Learn (ruta DE) | `learn.microsoft.com/en-us/training/career-paths/data-engineer` | F04 | Formación oficial gratuita de Fabric/Azure; el examen se paga aparte |
| Astronomer Academy | `academy.astronomer.io` | F04 | Cursos gratuitos de Airflow y buenas prácticas; la certificación se paga |
| DeepLearning.AI short courses | `deeplearning.ai/short-courses` | F07, F08 | Cursos de 1-2 h de RAG y embeddings; útiles y superficiales |

### De pago, y cuándo sí

| Recurso | Coste | Veredicto |
| --- | --- | --- |
| AWS Certified Data Engineer – Associate (DEA-C01) | ~150 USD | La credencial cloud con mejor relación señal/precio para DE. Pasa filtros de RR. HH. en consultoría; no te hace ingeniero |
| Microsoft DP-700 (Fabric) | ~165 USD | La más rentable si tu mercado es banca, seguros o administración en España. Sustituye a DP-203 |
| Databricks Certified Data Engineer Associate | ~200 USD | Examen práctico y respetado, pero solo si ya trabajas con Databricks |
| Google Cloud Professional Data Engineer | ~200 USD | Más dura y más de diseño. Inútil si no hay ofertas GCP en tu zona |
| SnowPro Core | ~175 USD | Acredita plataforma, no ingeniería |

### Lo que no merece la pena

- **Bootcamps de 3.000-8.000 € con «empleabilidad garantizada».** Con el Zoomcamp gratis, dos
  proyectos serios y una certificación cloud cubres el mismo temario.
- **Certificaciones de «Big Data»** (Hadoop, «data science con Excel»): nadie las pide y Hadoop
  está en declive.
- **Certificados de cursos de 3 horas**: van en «otros», no en formación.
- **Cualquier certificación de un proveedor que no aparezca en 30 ofertas de tu ciudad.**

---

## 5. Datos reales para los proyectos

Los seis primeros son los que sostienen PF-01 a PF-04. El resto, para cuando quieras variar de
dominio.

| Fuente | URL | Qué permite | Aviso |
| --- | --- | --- | --- |
| NYC TLC Trip Records | `nyc.gov/site/tlc/about/tlc-trip-record-data.page` | El clásico: Parquet por mes, particionado, join con meteorología. **El mejor proyecto de DE que existe** | ~50-100 MB por mes; histórico completo, decenas de GB |
| Chicago Crimes | `data.cityofchicago.org` | Ingesta incremental por fecha, modelado dimensional, datos sucios de verdad | ~8 M filas; CSV de ~1,5 GB |
| GH Archive | `gharchive.org` | Eventos semiestructurados por hora: streaming y batch con JSON anidado | 1-3 GB por día comprimido |
| Open-Meteo | `open-meteo.com` | Enriquecer cualquier dataset con meteorología, sin clave | Gratis para uso no comercial |
| INE | `ine.es` | Datos españoles (paro, IPC, padrón) con API JSON: muy vendible en entrevistas en España | Documentación árida; paciencia con los códigos |
| AEMET OpenData | `opendata.aemet.es` | Ingesta con API key y límite de peticiones: practica reintentos y caché | Requiere registro gratuito |
| ESIOS / Red Eléctrica | `ree.es/es/datos` | Series de 10 minutos: estacionalidad, anomalías, pronóstico | Token gratuito |
| ENTSO-E | `entsoe.eu/data` | Energía multi-país; API incómoda, buena práctica de ingeniería | Registro gratuito |
| GDELT | `gdeltproject.org` | Eventos globales y series geopolíticas | Enorme si vas al histórico |
| World Bank Open Data | `data.worldbank.org` | Modelo en estrella limpio de indicadores por país y año | CC BY 4.0 |
| Our World in Data | `ourworldindata.org` | Catálogo y linaje de muchas fuentes; storytelling | CC BY 4.0 |
| StatsBomb Open Data | `github.com/statsbomb/open-data` | JSON anidado de eventos de fútbol: aplanar a tablas | Solo uso no comercial |
| CityBikes | `api.citybik.es/v2` | Estado por estación cada minuto: Kafka sin infraestructura | API pública |
| Inside Airbnb | `insideairbnb.com/get-the-data` | Precios y ocupación con datos sucios de verdad | CC BY 4.0; 1-10 GB por ciudad |
| OpenFDA | `open.fda.gov` | API paginada y ficheros masivos; calidad de datos sanitaria | Dominio público (EE. UU.) |
| MIMIC-IV | `physionet.org/content/mimiciv` | Series clínicas de UCI; gobernanza y datos sensibles | **Requiere acreditación y formación en ética** |
| AWS Open Data | `registry.opendata.aws` | Ingesta desde S3 real y control de coste | Pagas el *egress* |
| Google Cloud Public Datasets | `cloud.google.com/public-datasets` | SQL a gran escala sin descargar; coste por bytes | 1 TB de consultas gratis al mes |

---

## 6. Qué se pide de verdad en las ofertas (2025-2026)

Dos fuentes independientes, con metodologías distintas, coinciden en la forma del stack.

| Skill | ITJobsWatch (UK, 6 meses a 2-nov-2026) | InterviewStack (6 877 ofertas, may-2026) |
| --- | --- | --- |
| SQL | 36,5 % | 71 % |
| Python | 32,7 % | 71 % |
| Pipelines / ETL | 31,9 % + 22,2 % | 74 % |
| Azure | 26,8 % | 33 % |
| Modelado de datos | 22,2 % | 38 % |
| Calidad de datos | 20,6 % | 43 % |
| AWS | 18,4 % | 44 % |
| CI/CD | 16,8 % | 30 % |
| Databricks | 15,2 % | 29 % |
| Spark / PySpark | 9,9 % (PySpark) | 33 % (Spark) |
| Airflow | — | 29 % |
| Snowflake | — | 31 % |
| dbt | 0,26 % (puesto 525) | 24 % |
| Kafka | — | 17 % |

**Cómo se leen estas dos columnas sin engañarse.** ITJobsWatch mide el **texto literal** del
anuncio en Reino Unido: infravalora lo que se da por supuesto. InterviewStack mide extracción de
skills sobre ofertas activas globales. De ahí que `dbt` salga 0,26 % en un sitio y 24 % en el
otro: en Reino Unido casi nadie escribe «dbt», pero se usa. Son rangos, no verdades.

**Lo que las dos dicen igual:** SQL + Python + pipelines + una nube + un orquestador + modelado y
calidad. Todo lo demás es especialización.

### Las tres cosas que separan a un junior contratable

1. **Un pipeline que se puede reejecutar sin romper nada.** El 74 % de las ofertas pide pipelines
   y el 43 % pide calidad explícitamente. El junior no contratable entrega un cuaderno que
   funciona una vez; el contratable entrega un DAG con reintentos, `MERGE`/upsert, tests de
   unicidad y de nulos, y sabe explicar qué pasa si se ejecuta dos veces el mismo día.
2. **Criterio de coste y de modelo, no de herramienta.** Por qué particionas por fecha, cuánto
   cuesta una consulta, por qué un `SELECT *` con `JOIN` sin filtro arruina la factura y qué
   esquema responde a la pregunta de negocio.
3. **Saber contar el proyecto en términos de negocio y de fiabilidad.** Solo el **3 % de las
   ofertas son de entrada** (frente al 8 % de analista): la puerta es estrechísima. El junior se
   contrata por señal de criterio, no por lista de tecnologías. Y la ruta realista suele ser
   *analytics engineer*, backend o analista durante 12-18 meses, no «DE junior» directo.

**Consecuencia para este repositorio:** si el objetivo es empleo, el peso debe estar en F03, F04,
F11 y los proyectos PF-01 a PF-05. La ruta quant (los diez conceptos de `01-NOTEBOOKLM.md`) es
diferenciador, no requisito.

### Fuentes de este apartado

- ITJobsWatch — Data Engineer, UK: `itjobswatch.co.uk/jobs/uk/data%20engineer.do`
- ITJobsWatch — dbt, evolución y skills co-ocurrentes: `itjobswatch.co.uk/jobs/uk/dbt.do`
- InterviewStack — Data Engineer skills 2026 (6 877 ofertas): `interviewstack.io/blog/data-engineer-skills-companies-want-2026`

---

## 7. Tus seis fuentes activas (rellenar a mano y no cambiar en tres meses)

| Puesto | Fuente | Para qué |
| --- | --- | --- |
| 1 · Currículo | Data Engineering Zoomcamp | La columna vertebral de F03-F04 |
| 2 · Práctica diaria | PostgreSQL Exercises | SQL, 20 min al día |
| 3 · Referencia | Documentación de Airflow y dbt | Lo que no se aprende en vídeo |
| 4 · Fondo | StatQuest o Codificando Bits | Estadística y series temporales |
| 5 · Actualidad | Data Engineering Weekly | Una hora a la semana, no más |
| 6 · Proyecto | NYC TLC u Open-Meteo | Los datos de PF-01 |

Cambiar una de estas seis exige una razón escrita. «He visto un canal nuevo» no es una razón.
