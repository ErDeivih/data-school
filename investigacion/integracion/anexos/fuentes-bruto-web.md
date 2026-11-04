# Fuentes web de calidad para Data Engineer (con base DS y algo de quant)

**Para quién es esto:** alguien que ya tiene un temario de 450 conceptos en 13 fases (F00–F12) y quiere *material*, no otro temario. Cada entrada está mapeada a la fase que le toca y dice qué aporta que no aporte el resto.

**Cómo se ha construido:** todas las URLs de este documento se han comprobado con petición HTTP real (código 200) o se han leído en una página abierta durante la investigación. No hay enlaces "de memoria".

**Fecha de la investigación:** noviembre de 2026. Los precios de certificaciones y los datos de mercado cambian: verifica el importe en la web oficial antes de pagar.

**Regla de uso:** no consumas más de 6–8 fuentes de forma activa. El resto son de consulta puntual. El error caro aquí no es elegir mal el canal, es coleccionar canales.

---

## 1. Canales de vídeo (20)

Selección con criterio de "esto no lo cubre ningún otro". Mezcla inglés/español. Descartados a propósito: canales de "motivación data" sin código, canales de analista que se disfrazan de DE, y cuentas que solo suben reels de roadmap.

### 1.1 Ingeniería de datos, plataforma y arquitectura

| Canal | URL | Idioma | Fase | Nivel | Qué aporta que no aporte otro | Advertencia |
|---|---|---|---|---|---|---|
| **DataTalksClub** | https://www.youtube.com/@DataTalksClub | EN | F04, F03 | Principiante → intermedio | Es el único que da una **secuencia completa y gratuita** (Data Engineering Zoomcamp: Docker → Terraform → Airflow → dbt/BigQuery → Spark → Kafka) con cohortes reales y deberes. Currículo, no tutoriales sueltos. | El contenido va por campañas anuales: si ves la playlist de un año anterior, las versiones de herramientas están desfasadas. Sigue el repo del año en curso, no la playlist vieja. |
| **Seattle Data Guy** (Ben Rogojan) | https://www.youtube.com/@SeattleDataGuy | EN | F04, F12 | Principiante → intermedio | Perspectiva de **consultoría real**: por qué un pipeline se cae en producción, cómo se negocia con stakeholders, qué se paga. Es el que más se parece a "lo que pasa en una empresa el lunes". | Deriva creciente hacia el negocio del dato y su newsletter; poco código denso. No esperes aquí tu dosis de Spark. |
| **Andreas Kretz** | https://www.youtube.com/c/andreaskayy | EN | F04, F11 | Principiante → avanzado | **Arquitectura y porqués**: batch vs streaming, lambda/kappa, por qué existe el orquestador, separación compute/storage. Racionaliza decisiones, no solo botones. | Formato antiguo (URL /c/, vídeos largos y webcam), subidas irregulares y mucho empuje hacia su curso de pago y a Databricks. Filtra. |
| **Data with Zach** (Zach Wilson) | https://www.youtube.com/c/datawithzach | EN | F04, F12 | Intermedio → avanzado | El mejor en **fundamentos de entrevista DE + diseño de pipelines**: idempotencia, SCD, modelado, "cómo lo harías en producción". Nivel técnico alto. | Su contenido gratuito es ahora el escaparate de DataExpert.io (bootcamp de pago). Los vídeos buenos son de 2022–2023; algunos ejemplos usan versiones viejas de herramientas. |
| **Darshil Parmar** | https://www.youtube.com/@DarshilParmar | EN | F04, F03 | Principiante → intermedio | **Proyectos end-to-end con código**: AWS/GCP/Azure + Airflow + Spark + Kafka montados de principio a fin, repositorios públicos. Es la vía más rápida de pasar de "sé qué es S3" a "tengo un pipeline en S3". | Muy AWS-céntrico y a veces "copiar y pegar": los proyectos no siempre cubren idempotencia, tests ni coste. Úsalo como andamio, y luego rompe y arregla el pipeline tú. |
| **Kahan Data Solutions** | https://www.youtube.com/@KahanDataSolutions | EN | F04, F11 | Intermedio | **dbt y Airflow en serio**: incremental models, snapshots, tests, CI/CD de transformaciones, patrones de despliegue. Lo que ningún curso introductorio de dbt te cuenta. | Canal pequeño y muy focalizado en el modern data stack (dbt/Snowflake/Fivetran). Si tu objetivo es big data on-prem, no es tu canal. |
| **Start Data Engineering** (Joseph Machado) | https://www.youtube.com/@startdataengineering | EN | F04, F11 | Intermedio → avanzado | **Calidad de ingeniería aplicada a datos**: tests, data contracts, observabilidad, "cómo escribir un pipeline que otro pueda mantener". Nivel de detalle poco habitual en YouTube. | Producción escasa y el contenido vive sobre todo en su blog (ver bloque 2). Trátalo como blog con vídeo ocasional. |
| **Databricks** (oficial) | https://www.youtube.com/@Databricks | EN | F04, F07 | Intermedio | Fuente **autoritativa** de Spark, Delta Lake, lakehouse, Unity Catalog y lakehouse federation. Cuando un blog random contradice a Databricks sobre Delta, suele ganar Databricks. | Canal de marketing: mucho anuncio de producto y keynote. Ve a las sesiones técnicas (Data + AI Summit), no a los promo. |
| **E-Learning Bridge** (Shashank Mishra) | https://www.youtube.com/@shashank_mishra | EN/HI | F04, F10 | Intermedio | **Big data clásico**: Spark interno (particiones, shuffles, executors), Hadoop, Kafka, y preguntas de entrevista de big data. Explica *por qué* Spark hace lo que hace. | Mezcla hindi/inglés con acento marcado (subtítulos obligatorios) y varias series usan Spark 2.x/3.0. Verifica versiones. |
| **Data Engineering Latam** | https://www.youtube.com/@DataEngineeringLatam | ES | F03, F04 | Principiante → intermedio | La cobertura **en español** más ordenada del stack DE: playlists separadas de SQL, Airflow, Spark, Docker y AWS/Azure. Buen sustituto si tu inglés todavía no aguanta un curso de 10 horas. | Canal de comunidad: calidad desigual entre playlists, algunas con vídeos de hace 2–3 años y sin actualizar. Revisa fechas antes de seguir una serie. |

### 1.2 Fundamentos, código y sistema (transversal)

| Canal | URL | Idioma | Fase | Nivel | Qué aporta | Advertencia |
|---|---|---|---|---|---|---|
| **codebasics** | https://www.youtube.com/@codebasics | EN | F03 | Principiante | Python y SQL desde cero con **ritmo de principiante real**, sin saltos. Bueno para F03 si vienes de cero absoluto. | Orientado a analista, no a DE: no entra en Spark, orquestación ni infra. Y tiene mucho curso patrocinado. |
| **Datademia** | https://www.youtube.com/@datademia | ES | F03, F04 | Principiante | **DE en español con laboratorios**: línea de comandos, Git, Docker, estadística, Airflow. Es de los pocos en español que enseña *a montar* en vez de a definir conceptos. | Canal de una academia de pago: parte del contenido acaba en CTA a sus cursos. Ritmo lento para quien ya programa. |
| **MoureDev by Brais Moure** | https://www.youtube.com/@mouredev | ES | F03, F11 | Principiante → intermedio | **Español de España, didáctica excelente** en Python, Git, testing, backend y roadmaps. Es el mejor sitio en español para arreglar los agujeros de F03/F11 sin pagar. | Es desarrollo de software general, no datos. Contenido de 2–4 años de antigüedad en algunas series (frameworks). |
| **Pelado Nerd** | https://www.youtube.com/@peladonerd | ES (Río de la Plata) | F11 | Intermedio | **Docker, Kubernetes, Linux, self-hosting, redes**. Es lo que te falta cuando tu DAG funciona en local y muere en el contenedor. | Tono informal y contenido muy largo; no es un curso estructurado. Nada de datos. |
| **StatQuest with Josh Starmer** | https://www.youtube.com/@statquest | EN | F02, F06 | Principiante → intermedio | **Intuición visual de estadística y ML** (PCA, regresión, árboles, boosting, MLE). Es el atajo para entender *qué hace* un modelo antes de usarlo. | Deliberadamente ligero en matemáticas formales: no sustituye a F01/F02 con demostraciones. Y el ritmo "BAM!" no es para todos. |
| **Codificando Bits** | https://www.youtube.com/@codificandobits | ES | F02, F05, F06 | Intermedio | **Series temporales y ML en español con rigor**: estacionariedad, ARIMA, validación temporal, feature engineering. Raro y valioso. | Canal pequeño; producción pausada. Mira las playlists, no el feed. |

### 1.3 Quant y finanzas (F09)

| Canal | URL | Idioma | Fase | Nivel | Qué aporta | Advertencia |
|---|---|---|---|---|---|---|
| **QuantPy** | https://www.youtube.com/@QuantPy | EN | F09 | Intermedio | **Código quant real**: valoración de opciones, Monte Carlo, optimización de carteras, backtesting en Python. Junta F09 con F03. | Adquirido por ThetaData: parte del contenido nuevo es promo de datos de mercado. Nivel matemático asume derivadas y probabilidad. |
| **PyQuant News** (Jason Strimpel) | https://www.youtube.com/@PyQuantNews | EN | F09 | Intermedio | Puente **data engineering ↔ trading**: ingesta de precios, almacenamiento de ticks, pipelines de datos de mercado. Justo el ángulo que ningún canal de DE cubre. | Formato corto y a menudo promocional de su newsletter/curso. Poca profundidad por vídeo. |
| **Dimitri Bianco** | https://www.youtube.com/@DimitriBianco | EN | F09, F12 | Intermedio → avanzado | **Carrera y realidad del quant** (risk, model validation, entrevistas, matemáticas que se usan de verdad) desde dentro de banca. Corrige expectativas del "quant de película". | Mucho vídeo de opinión y de carrera; el código es minoritario. |
| **El podcast de Value School** | https://www.youtube.com/@ValueSchool | ES | F09, F12 | Principiante | **Finanzas en español de España, con conferenciantes serios** (gestión, Historia de los mercados, sesgos). Contexto económico y vocabulario que necesitas para hablar con negocio. | Es value investing, **no quant**: cero estadística, cero código. Úsalo solo como cultura financiera, nunca como fuente cuantitativa. |

**Nota de honestidad sobre este bloque:** en español ya hay fundamentos decentes (Data Engineering Latam, Datademia, MoureDev, Codificando Bits), pero **sigue faltando un canal de referencia en español sobre data engineering moderno a nivel intermedio-avanzado** (dbt, Iceberg, streaming real, coste en el warehouse). En español hay mucho "qué es un data lake" y poco "cómo hago un merge incremental idempotente con particiones". Ahí tira de Kahan, Start Data Engineering y la documentación oficial.

---

## 2. Sitios, blogs y newsletters

### 2.1 Documentación oficial imprescindible (consulta, no lectura)

| Recurso | URL | Fase | Qué cubre | Por qué merece la pena |
|---|---|---|---|---|
| PostgreSQL Docs | https://www.postgresql.org/docs/current/ | F03, F04 | SQL, índices, MVCC, EXPLAIN, ventanas, tipos, extensiones | La referencia SQL más honesta que existe. Si tu SQL solo viene de tutoriales, aquí descubres por qué tu consulta tarda 40 s. |
| dbt Docs | https://docs.getdbt.com/ | F04 | Modelos, incremental, snapshots, tests, macros, contratos | Documentación que enseña la **disciplina de transformación**: materializaciones, linaje, tests. Es el estándar de facto del transform moderno. |
| Apache Airflow Docs | https://airflow.apache.org/docs/ | F04 | DAGs, operadores, scheduling, idempotencia, backfills | Aquí están los conceptos que separan un DAG de juguete (cron + script) de uno de producción (retries, catchup, SLA, XComs con criterio). |
| Apache Spark Docs | https://spark.apache.org/docs/latest/ | F04 | RDD/DataFrame, tuning, joins, AQE, structured streaming | La guía de *performance tuning* sola justifica el enlace. Es donde entiendes particiones y shuffles de verdad. |
| Delta Lake Docs | https://docs.delta.io/ | F04 | ACID en lakehouse, time travel, MERGE, optimización | Complemento imprescindible de Spark si trabajas con tablas: sin esto, tu "data lake" es una carpeta de Parquet. |
| Apache Iceberg Docs | https://iceberg.apache.org/docs/latest/ | F04 | Especificación de tablas, evolución de esquema, hidden partitioning | El formato que ha ganado la guerra de tablas abiertas. Si en 2026 no sabes qué es un catálogo Iceberg, se nota en entrevistas. |
| Apache Kafka Docs | https://kafka.apache.org/documentation/ | F04 | Particiones, offsets, garantías de entrega, compactación, Kafka Connect | Streaming sin esto es copiar código. La sección de *delivery semantics* es la que te preguntan. |
| Databricks Docs | https://docs.databricks.com/ | F04 | Lakehouse, Unity Catalog, workflows, Delta Live Tables | Referencia cuando el entorno es Databricks (muy habitual en empresas grandes). |
| Snowflake Docs | https://docs.snowflake.com/ | F04 | Micro-particiones, clustering, warehouses, gobernanza, coste | El mejor sitio para aprender a razonar sobre **coste de cómputo**, algo que casi nadie domina en junior. |
| BigQuery Docs | https://cloud.google.com/bigquery/docs | F04 | Particionado, clustering, slots, coste por bytes | Si tu nube es GCP, la sección de optimización de coste/consulta es obligatoria. |
| AWS Glue Docs | https://docs.aws.amazon.com/glue/ | F04 | Catálogo, crawlers, jobs, Spark serverless | Ruta de entrada más común a DE en la nube en España (y en consultoría). |
| Azure Data Factory Docs | https://learn.microsoft.com/en-us/azure/data-factory/ | F04 | Pipelines, linked services, integration runtime | Sigue siendo el ETL más pedido en banca/seguros/administración en España, aunque Microsoft empuje Fabric. |
| pandas Docs | https://pandas.pydata.org/docs/ | F03, F05 | DataFrames, groupby, merges, time series, IO | La guía de *10 minutes to pandas* y la de *cookbook* resuelven el 80 % del día a día. |
| Polars Docs | https://docs.pola.rs/ | F03, F05 | DataFrames con API perezosa, expresiones, streaming | Alternativa moderna a pandas: más rápida y con semántica de expresiones. Buen diferenciador de portfolio. |
| DuckDB Docs | https://duckdb.org/docs/ | F03, F05 | SQL analítico embebido, lectura de Parquet, extensiones | La herramienta que más ha cambiado el trabajo local de un DE: SQL sobre Parquet sin montar clúster. |
| Astronomer Docs | https://docs.astronomer.io/ | F04 | Airflow en producción, buenas prácticas de DAGs, despliegue | Mejor documentación *práctica* de Airflow que la oficial en varios puntos (guías de patrones). |

### 2.2 Blogs de referencia

| Recurso | URL | Fase | Qué cubre | Por qué merece la pena |
|---|---|---|---|---|
| Start Data Engineering | https://www.startdataengineering.com/ | F04, F11 | Proyectos paso a paso, tests, CI/CD de datos, data quality | El blog que trata pipelines como **software**: tests, entornos, despliegue. Calidad de escritura muy por encima de la media. |
| Seattle Data Guy (blog) | https://blog.dataengineer.io/ | F04, F12 | Arquitectura real, entrevistas, carrera, consultoría | Casos concretos de empresas y salarios. Bueno para calibrar expectativas y para preparar "cuéntame un proyecto". |
| Data Engineering Weekly | https://www.dataengineeringweekly.com/ | F04, F08 | Curación semanal: Iceberg, lakehouse, plataformas, IA en datos | La mejor relación señal/ruido del sector. Una lectura semanal cubre "estar al día" sin Twitter. |
| Simon Späti (ssp.sh) | https://ssp.sh/ | F04, F12 | Ensayos técnicos, entrevistas a ingenieros, fundamentos de DE | Escritura reflexiva, no clickbait. Ideal para F12 (comunicar decisiones técnicas). |
| The Analytics Engineering Roundup (dbt) | https://roundup.getdbt.com/ | F04, F12 | Analítica moderna, casos de analytics engineering, cultura de datos | Buen antídoto contra el "tool-first": habla de organización, contratos y propiedad del dato. |
| Databricks Blog | https://www.databricks.com/blog | F04, F07 | Spark, lakehouse, ingeniería de rendimiento, MLOps | Artículos técnicos profundos (a veces demasiado). Fuente fiable de benchmarks y de cómo funciona Delta por dentro. |
| Dagster Blog | https://dagster.io/blog | F04, F11 | Orquestación con activos (assets), testing de pipelines, data quality | La mejor explicación conceptual de la diferencia entre *tarea* y *activo de datos*. Cambia cómo diseñas. |
| Spotify Engineering | https://engineering.atspotify.com/ | F04, F11, F12 | Plataformas de datos a escala, backstage, equipos | Casos de ingeniería de empresas que sí publican detalle. Útil para F11 (sistemas) y para hablar de escala con criterio. |
| Martin Fowler | https://martinfowler.com/ | F11 | Arquitectura, patrones, testing, refactoring, CI | Aunque no es de datos, es la fuente que evita que escribas pipelines como scripts de 800 líneas. F11 puro. |
| Locally Optimistic | https://www.locallyoptimistic.com/ | F04, F12 | Analítica, organización de equipos de datos, carrera | Ensayos con experiencia real de equipos pequeños. Bueno para F12 (producto y carrera). |
| Benn Stancil (benn.substack) | https://benn.substack.com/ | F12, F08 | Opinión lúcida sobre el stack, BI, IA y el futuro del dato | No enseña herramientas; enseña a pensar. Lectura crítica, no tutorial. |
| El podcast de Data Engineering | https://www.dataengineeringpodcast.com/ | F04, F12 | Entrevistas a ingenieros y fundadores del ecosistema | Casi 700 episodios: buscas la herramienta y escuchas a quien la construyó. Formato entrevista, no curso. |
| QuantDare | https://www.quantdare.com/ | F09, F02 | Quant en **español**: estadística aplicada a mercados, backtesting, riesgo | Prácticamente el único blog quant en español con rigor y continuidad. Une F02 y F09. |
| Quantocracy | https://www.quantocracy.com/ | F09 | Agregador diario de blogs quant | Curación del ecosistema quant (mucho ruido, pero es el radar). Úsalo para descubrir, no para leer todo. |
| Robot Wealth | https://robotwealth.com/ | F09, F05 | Trading sistemático, investigación cuantitativa honesta, series temporales | De los pocos que publica **resultados que no funcionan** y por qué. Antídoto al overfitting. |
| Ernie Chan (blog) | https://epchan.blogspot.com/ | F09 | Mean reversion, execution, ideas de estrategias con código | Clásico del sector, muy directo. Contenido antiguo (formatos y mercados de otra época): lee los conceptos, no los tickers. |
| Aprende Machine Learning | https://www.aprendemachinelearning.com/ | F02, F06 | ML en **español** desde cero, con código y teoría | Referencia hispanohablante consolidada. Bueno para F02/F06 si el inglés te frena al principio. |

### 2.3 Sitios de práctica (aprender haciendo)

| Recurso | URL | Fase | Qué cubre | Por qué merece la pena |
|---|---|---|---|---|
| PostgreSQL Exercises | https://pgexercises.com/ | F03 | 80+ ejercicios SQL con solución explicada | La mejor progresión de SQL que existe: de SELECT a agregaciones y ventanas, con feedback inmediato y sin registro. |
| SQLBolt | https://sqlbolt.com/ | F03 | SQL interactivo básico-intermedio | 20 minutos al día y sales sabiendo JOINs. Perfecto si partes de cero absoluto. |
| SQLZoo | https://sqlzoo.net/ | F03 | Tutoriales interactivos con evaluación automática | Antiguo pero funcional; bueno para drills de GROUP BY y subconsultas. |
| DataLemur | https://datalemur.com/ | F03, F12 | Preguntas SQL de entrevista reales (FAANG) | Entrena el formato exacto de la prueba técnica, no el SQL de manual. |
| StrataScratch | https://www.stratascratch.com/ | F03 | Problemas SQL y Python de entrevistas reales | Base grande de problemas con soluciones de la comunidad. El plan gratuito es limitado. |
| 8 Week SQL Challenge | https://8weeksqlchallenge.com/ | F03, F04 | 8 casos de negocio completos (restaurante, suscripciones, etc.) | Te obliga a **modelar y responder preguntas de negocio**, no a resolver juguetes. Salen proyectos de portfolio decentes. |
| Mode SQL Tutorial | https://mode.com/sql-tutorial/ | F03 | SQL para analítica con datos reales | Explicaciones muy claras de agregaciones y ventanas. Contenido algo antiguo pero los conceptos no caducan. |
| HackerRank SQL | https://www.hackerrank.com/domains/sql | F03, F10 | Ejercicios SQL y algoritmos por niveles | Útil para práctica diaria y para F10 (estructuras). Interfaz anticuada y problemas a veces tramposos. |
| NeetCode | https://neetcode.io/ | F10 | 150 problemas de algoritmos con vídeo y ruta | Para F10 sin perderte: ruta ordenada por patrones. No es de datos, es el gimnasio de algoritmos. |
| Kaggle Learn | https://www.kaggle.com/learn | F03, F05, F06 | Microcursos de pandas, SQL, visualización, ML | Gratis, corto y con entorno incluido. La vía más rápida de tocar pandas con datos reales el primer día. |
| Data Engineering Handbook (Zach Wilson) | https://github.com/DataExpert-io/data-engineer-handbook | F00, F12 | Mapa completo de recursos, entrevistas y temas por nivel | Úsalo como **índice** para contrastar tu temario, no como plan. Enorme y desordenado, pero cubre huecos. |
| Roadmap.sh — Data Engineer | https://roadmap.sh/data-engineer | F00, F04 | Mapa visual de tecnologías por área | Sirve para ver dependencias ("¿qué necesito antes de Kafka?"). No es un temario serio, es un mapa mental. |
| Design Patterns for Data Engineering (DEDP) | https://www.dedp.online/ | F04, F11 | Patrones de diseño de sistemas de datos en abierto | Libro/curso online gratuito sobre patrones (ingesta, modelado, serving). Muy alineado con F04 y F11. |
| Roadmap DE en español (natayadev) | https://natayadev.github.io/dataengineering-roadmap/ | F00 | Recursos gratuitos en español, ordenados por nivel | Curación honesta y actualizada de material en español. Bueno para no duplicar y para tirar de subtítulos. |
| awesome-public-datasets | https://github.com/awesomedata/awesome-public-datasets | F05, F12 | Catálogo curado de datasets abiertos por dominio | Punto de partida cuando no sabes qué datos usar. Licencias dispares: verifica cada uno. |

---

## 3. Cursos gratuitos y certificaciones (empleabilidad real 2026)

### 3.1 Gratis de verdad (sin truco)

| Recurso | URL | Fase | Coste | Peso en CV | Veredicto |
|---|---|---|---|---|---|
| Data Engineering Zoomcamp (DataTalksClub) | https://github.com/DataTalksClub/data-engineering-zoomcamp | F03, F04 | 0 € | Alto (proyecto) | **El mejor retorno por hora de todo el documento.** 9 semanas, pipeline completo con Docker, Terraform, Airflow, dbt, Spark, Kafka. El certificado en sí no vale mucho; el repositorio con el proyecto final, sí. |
| dbt Fundamentals | https://learn.getdbt.com/courses/dbt-fundamentals | F04 | 0 € | Medio-alto | Curso oficial, ~5 h, certificado gratuito. Es el vocabulario mínimo del transform moderno (modelos, tests, incremental, linaje). Hazlo y luego rompe un incremental model a propósito. |
| freeCodeCamp — Relational Database | https://www.freecodecamp.org/learn/relational-database/ | F03 | 0 € | Medio | Bash + PostgreSQL + Git en proyectos guiados. Certificación gratuita y verificable. Buen sustituto de un curso de SQL de pago. |
| CS50x (Harvard) | https://cs50.harvard.edu/x/ | F03, F10, F11 | 0 € | Medio-alto | Fundamentos de verdad (memoria, estructuras, Python, SQL). Duro si vienes de cero, pero elimina lagunas que luego te frenan en F10/F11. |
| MIT OpenCourseWare | https://ocw.mit.edu/ | F01, F02, F11 | 0 € | Bajo (sin certificado) | Para F01/F02 con demostraciones serias y F11 (sistemas distribuidos). No da credencial, da conocimiento. Elige cursos concretos, no "explores". |
| Microsoft Learn — ruta Data Engineer | https://learn.microsoft.com/en-us/training/career-paths/data-engineer | F04 | 0 € | Medio | Formación oficial gratuita y muy completa de Fabric/Azure. El examen se paga aparte. Útil si tu mercado es banca/administración en España. |
| AWS Skill Builder (plan gratuito) | https://skillbuilder.aws/ | F04 | 0 € (plan free) | Medio | Cursos y labs básicos de Glue, Redshift, S3. El plan gratuito no incluye los labs avanzados ni los exámenes de práctica completos. |
| Google Cloud Skills Boost | https://www.cloudskillsboost.google/ | F04 | 0 € parcial / suscripción | Medio | Hay rutas gratuitas de BigQuery y Dataflow. El "learning path" completo con labs suele requerir suscripción o créditos. Comprueba qué es gratis antes de meter tarjeta. |
| Confluent Developer (Kafka) | https://developer.confluent.io/courses/ | F04 | 0 € | Medio | El mejor material gratuito de Kafka: cursos con vídeo, código y ejercicios. Streaming explicado por quien lo construyó. |
| Astronomer Academy | https://academy.astronomer.io/ | F04 | 0 € (cursos) / pago (certificación) | Medio | Cursos gratuitos de Airflow 3 y buenas prácticas. La certificación oficial de Airflow se paga. |
| Kaggle Learn | https://www.kaggle.com/learn | F02, F03, F05, F06 | 0 € | Bajo-medio | Microcursos con certificado nominal. Sirve para arrancar pandas/SQL/ML, no para acreditar nivel. |
| DeepLearning.AI short courses | https://www.deeplearning.ai/short-courses/ | F07, F08 | 0 € | Bajo-medio | Cursos de 1–2 h sobre RAG, embeddings, agentes. Buenos para F08 y para entender qué te van a pedir en pipelines de IA. Muy superficiales. |

### 3.2 De pago, y cuándo sí

| Recurso | URL | Fase | Coste aproximado | Peso en CV | Veredicto |
|---|---|---|---|---|---|
| AWS Certified Data Engineer – Associate (DEA-C01) | https://aws.amazon.com/certification/certified-data-engineer-associate/ | F04 | ~150 USD examen | **Alto** en consultoría/cloud | La certificación cloud con mejor relación señal/precio para DE ahora mismo. Vale sobre todo si tu empresa o los clientes son AWS. No sustituye a un proyecto. |
| Google Cloud Professional Data Engineer | https://cloud.google.com/learn/certification/data-engineer | F04 | ~200 USD examen | Alto (si el mercado es GCP) | Más dura que la de AWS y más orientada a diseño. Buena, pero inútil si no hay ofertas GCP en tu zona. |
| Microsoft DP-700 (Fabric Data Engineer) | https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/ | F04 | ~165 USD examen | Medio-alto (España, banca) | Sustituye a DP-203 (retirado). Si tu objetivo es banca/seguros/administración española, es la más rentable. Ojo: está muy atada al producto Fabric. |
| Databricks Certified Data Engineer Associate | https://www.databricks.com/learn/certification/data-engineer-associate | F04 | ~200 USD examen | Alto en entorno Databricks | Examen práctico y respetado. Tiene sentido si ya trabajas con Databricks o quieres entrar en consultoría de datos. |
| Snowflake SnowPro Core | https://www.snowflake.com/en/learn/certification/ | F04 | ~175 USD examen | Medio | Vale si el stack objetivo es Snowflake. Es más "producto" que "ingeniería": no te enseña a diseñar, te acredita en la plataforma. |
| Astronomer Airflow Certification | https://academy.astronomer.io/ | F04 | ~250 USD | Bajo-medio | Solo si tu trabajo es explícitamente Airflow. Nadie contrata por esto; el repo con DAGs de producción pesa más. |
| IBM Data Engineering Professional Certificate (Coursera) | https://www.coursera.org/professional-certificates/ibm-data-engineer | F03, F04 | Suscripción mensual (~40–60 €/mes) | Bajo-medio | Muy extenso y muy lento, con ejercicios superficiales. Sirve si necesitas estructura y no sabes por dónde empezar; no para conseguir trabajo por sí solo. |
| Google Data Analytics Certificate (Coursera) | https://www.coursera.org/professional-certificates/google-data-analytics | F03 | Suscripción mensual | Bajo para DE | Certificado de **analista**, no de ingeniero. Útil si vienes de cero absoluto y necesitas un primer título, pero no te hace DE. |

### 3.3 Lo que NO merece la pena (y por qué)

- **Bootcamps de DE de 3.000–8.000 € con "empleabilidad garantizada".** La garantía suele ser una bolsa de empleo o una devolución condicionada. Con el Zoomcamp gratuito + 2 proyectos serios + una certificación cloud, cubres el mismo temario.
- **Certificaciones de "Big Data" de plataformas de cursos genéricas** (Hadoop, "data science con Excel"). Nadie las pide en 2026 y Hadoop está en declive claro en ofertas.
- **Certificados de finalización de cursos de 3 horas** (Kaggle, DeepLearning.AI, Coursera sueltos). No van en la sección de formación del CV; van —como mucho— en "otros".
- **Cualquier certificación de un proveedor que no aparezca en las ofertas de tu ciudad.** Revisa 30 ofertas reales antes de pagar 200 USD.
- **Cursos de "IA para data engineers" de 2026 que solo enseñan prompts.** El valor está en RAG/embeddings/pipelines de datos para IA (F08), no en "ChatGPT para tu DAG".

---

## 4. Fuentes de datos reales y abiertas para proyectos

| Fuente | URL | Licencia / condiciones | Tamaño aproximado | Proyecto que permite |
|---|---|---|---|---|
| **NYC TLC Trip Records** | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page | Datos públicos de la ciudad de NY (dominio público en la práctica) | ~30–60 GB el histórico completo; ~50–100 MB por mes en Parquet | Pipeline por lotes con Parquet + particionado por mes, join con meteorología, cálculo de demanda por zona. **El proyecto clásico de DE y sigue siendo el mejor.** |
| **Chicago Crimes** | https://data.cityofchicago.org/ | Datos abiertos del ayuntamiento (uso libre) | ~8 M filas, ~1,5 GB CSV | Ingesta incremental por fecha, modelado dimensional (hechos/dimensiones), calidad de datos (nulos, geocodificación sucia). Muy bueno para F04 (SCD y deduplicación). |
| **GH Archive** | https://gharchive.org/ | Datos públicos de eventos GitHub | ~1–3 GB por día (JSON.gz); particionado por hora | Streaming/batch con eventos semiestructurados: ingesta por horas, ventanas, top repos. Ideal para practicar Spark o Kafka con datos reales sucios. |
| **GDELT Project** | https://www.gdeltproject.org/ | Proyecto abierto, uso libre con atribución | Enorme (TB acumulados si vas a histórico) | Análisis de eventos globales, detección de tono, series temporales geopolíticas. Perfecto para F05 (series temporales) y NLP básico. |
| **World Bank Open Data** | https://data.worldbank.org/ | CC BY 4.0 | Cientos de MB en CSV vía API | Modelo en estrella de indicadores por país/año, comparativas, dashboards. Datos muy limpios: bueno para centrarte en el pipeline, no en la limpieza. |
| **Our World in Data** | https://ourworldindata.org/ | CC BY 4.0 (código abierto) | GBs en su catálogo; descargas por dataset | Proyecto de catálogo/linaje: ingesta de múltiples fuentes, normalización, documentación. Excelente para portfolio con storytelling (F12). |
| **Eurostat** | https://ec.europa.eu/eurostat | Reutilización libre con atribución | Cientos de MB | Comparativas europeas, armonización de códigos país, validación de esquemas. Combínalo con INE para un proyecto "España vs UE". |
| **INE (España)** | https://www.ine.es/ | Datos abiertos, reutilización con atribución | Decenas de MB por operación (API JSON) | Proyecto con datos **españoles** (paro, IPC, padrón) + visualización. Muy vendible en entrevistas en España. |
| **AEMET OpenData** | https://opendata.aemet.es/ | Datos abiertos del Gobierno de España (requiere API key gratuita) | Series históricas por estación; decenas de MB | Ingesta vía API con rate limits, climatología, join con datos de consumo o transporte. Practica gestión de claves y reintentos. |
| **ESIOS / Red Eléctrica (REE)** | https://www.ree.es/es/datos | Datos abiertos (token gratuito para la API) | Series de 10 min de generación y demanda; MBs | Series temporales de alta frecuencia: estacionalidad, agregación temporal, detección de anomalías, previsiones. F05 en estado puro. |
| **ENTSO-E Transparency Platform** | https://www.entsoe.eu/data/ | Registro gratuito, uso con atribución | GBs si bajas histórico de varios países | Proyecto energético multi-país: precios, generación, intercambios. Un clásico europeo con API incómoda (buena práctica de ingeniería). |
| **Open-Meteo** | https://open-meteo.com/ | Uso no comercial gratuito (CC BY 4.0 en los datos); API sin key para uso básico | Series horarias por coordenada; ligero | Join meteorológico con cualquier dataset (taxi, ventas, energía). Gratis y sin fricción: el complemento perfecto para enriquecer tu proyecto. |
| **Alpha Vantage** | https://www.alphavantage.co/ | API gratuita con límite (~25 peticiones/día); datos con condiciones de uso | Ligero (JSON/CSV) | Ingesta de precios y fundamentales, pipeline incremental diario, backtesting sencillo. Para F09 sin gastar dinero. |
| **yfinance (Yahoo Finance)** | https://github.com/ranaroussi/yfinance | Librería open source sobre datos de Yahoo (condiciones de Yahoo; no oficial) | Ligero | Prototipado rápido de precios y fundamentales. **Aviso:** no es una API oficial; no lo uses como fuente de producción ni redistribuyas datos. |
| **CoinGecko API** | https://www.coingecko.com/en/api | Plan demo gratuito con límite de llamadas; datos con atribución | Ligero | Proyecto de cripto con datos casi en tiempo real: ingesta periódica, almacenamiento, métricas. Buen ejercicio de idempotencia. |
| **StatsBomb Open Data** | https://github.com/statsbomb/open-data | Gratuito para investigación/uso no comercial con atribución | GBs de eventos de partidos | Modelado de eventos deportivos (xG, pases), JSON anidado → tablas. Excelente ejercicio de *aplanado* de JSON complejo. |
| **football-data.org** | https://www.football-data.org/ | API con plan gratuito (límite de peticiones) | Ligero | Pipeline de resultados y clasificaciones, scheduling diario, deduplicación. Muy fácil de montar en Airflow. |
| **CityBikes API** | https://api.citybik.es/v2/ | API pública abierta | Ligero | Streaming simulado de bicicletas compartidas; estado por estación cada minuto. Ideal para practicar Kafka sin infraestructura. |
| **Inside Airbnb** | https://insideairbnb.com/get-the-data/ | CC BY 4.0 | ~1–10 GB por ciudad | Proyecto de negocio: precios, ocupación, mapas. Datos sucios de verdad (tipos, nulos, geografía). |
| **OpenFDA** | https://open.fda.gov/ | Dominio público (EE. UU.) | GBs de informes de eventos adversos | Pipeline con API paginada y ficheros masivos; calidad de datos sanitaria. F04 + F05 sin datos personales. |
| **MIMIC-IV (PhysioNet)** | https://physionet.org/content/mimiciv/ | **Requiere acreditación**: formación en ética (CITI) y acuerdo de uso de datos | ~TB de datos clínicos | Proyecto sanitario serio (series temporales de UCI). La fricción de acceso es parte del aprendizaje: gobernanza y datos sensibles. |
| **AWS Open Data Registry** | https://registry.opendata.aws/ | Acceso libre; pagas el egress si procesas en tu cuenta | TBs (muchos datasets) | Practicar ingesta desde S3 real y controlar coste. Muy alineado con F04 en AWS. |
| **Google Cloud Public Datasets** | https://cloud.google.com/public-datasets | Acceso libre; BigQuery con 1 TB de consultas gratis al mes | TBs | Practicar SQL a gran escala sin descargar nada: particiones, coste por bytes, consultas caras. Perfecto para F04. |
| **Kaggle Datasets** | https://www.kaggle.com/datasets | Licencias **dispares** (verifica cada dataset) | MBs a GBs | Rápido para prototipos y competiciones. Evita datasets "limpios de tutorial" si quieres portfolio: elígelos sucios y documenta la limpieza. |
| **Hugging Face Datasets** | https://huggingface.co/datasets | Licencias dispares (muchas abiertas, algunas restringidas) | MBs a TBs | Datos para F08: texto, instrucciones, embeddings. Ojo con la licencia si publicas el proyecto. |

**Cómo convertir esto en portfolio (3 proyectos, no 10):**
1. **Batch idempotente con orquestación**: NYC TLC + Open-Meteo, Airflow + dbt + Parquet/Postgres, tests y re-ejecución segura.
2. **Streaming real**: CityBikes o GH Archive → Kafka → consumidor con ventanas → tabla agregada; documenta offsets y garantías.
3. **Caso de negocio con datos españoles**: INE + AEMET o ESIOS → modelo dimensional → dashboard → memo de 1 página con la decisión recomendada (F12).

---

## 5. Qué se pide hoy en ofertas de Data Engineer (2025–2026)

### 5.1 El stack que aparece de verdad

Dos análisis independientes con metodologías distintas coinciden en la forma del stack:

| Skill | % de ofertas (UK, ITJobsWatch, 6 meses a nov-2026) | % de ofertas (global/US, InterviewStack, 6.877 ofertas, may-2026) |
|---|---|---|
| SQL | 36,5 % (1ª) | 71 % |
| Python | 32,7 % (3ª) | 71 % |
| Pipelines / ETL | 31,9 % (pipeline) + 22,2 % (ETL) | 74 % |
| Azure | 26,8 % | 33 % |
| Data modelling | 22,2 % | 38 % |
| Data quality | 20,6 % | 43 % |
| AWS | 18,4 % | 44 % |
| CI/CD | 16,8 % | 30 % |
| Databricks | 15,2 % | 29 % |
| Spark / PySpark | 9,9 % (PySpark) | 33 % (Spark) |
| Airflow | ~26 % (entre las que citan dbt) | 29 % |
| dbt | 0,26 % de todas las ofertas TI (rank 525) | 24 % |
| Snowflake | no aparece en el top 30 de UK | 31 % |
| Kafka | no aparece en el top 30 de UK | 17 % |
| Terraform | 20,1 % (entre las que citan dbt) | 14 % |

*Nota metodológica importante:* ITJobsWatch mide **texto literal del anuncio en el Reino Unido**, así que infravalora herramientas que se dan por supuestas; InterviewStack mide **extracción de skills sobre 6.877 ofertas activas globales**. Por eso dbt sale 0,26 % en un sitio y 24 % en el otro: en el Reino Unido casi nadie escribe "dbt" en el anuncio, pero lo usa. Usa las dos tablas como rangos, no como verdad absoluta.

**Lectura práctica:** SQL + Python + pipelines + una nube + un orquestador + modelado y calidad. Todo lo demás es especialización.

### 5.2 Herramientas que suben y que bajan

**Suben (2024 → 2026):**
- **AI/LLM dentro de la oferta de DE**: 19,5 % de las ofertas UK de DE citan ya "AI"; en InterviewStack, LLM y Generative AI aparecen en el 9 % cada uno, "near zero hace un año". Se pide construir pipelines de datos para IA (RAG, embeddings, vector stores).
- **Data quality y observabilidad**: 43 % (calidad) y 14 % (observabilidad) en InterviewStack. Ya no se asume que el pipeline "funciona".
- **Ingeniería de plataforma aplicada a datos**: CI/CD 30 %, Terraform 14 %, Docker 14 %, Kubernetes 13 %, Git y entornos como requisito básico.
- **Formatos de tabla abiertos (Iceberg/Delta)**: Delta Lake ya aparece en el 7 % de las ofertas y el discurso de industria (AWS, Databricks y Snowflake convergiendo en Iceberg REST) lo empuja a estándar.
- **Databricks y lakehouse** como bloque: 15,2 % en UK, 29 % global.

**Bajan o se están comoditizando:**
- **dbt como palabra clave**: en UK pasa de rank 247 (2024) → 386 (2025) → 525 (2026) y del 1,07 % → 0,61 % → 0,26 % de las ofertas de TI. Interpretación correcta: **no está muriendo, se está convirtiendo en expectativa por defecto**, así que deja de diferenciar. Aprenderlo sigue siendo obligatorio; ponerlo como logro principal del CV, ya no.
- **Hadoop / MapReduce / ETL clásico con herramientas propietarias**: residual. Si tu formación es "Hadoop + Pentaho", vas tarde.
- **Scala**: 12 % de las ofertas; el mercado se ha movido a PySpark. Aprende Scala solo si entras en un equipo que ya lo tiene.
- **BI como competencia del DE**: Tableau 11 %, Power BI 14 %. Se espera que *habilites* dashboards, no que los construyas.
- **"Data science" como cajón de sastre en ofertas de DE**: 17 % estadística/experimentación. Se pide apoyar modelos, no construirlos.

### 5.3 Las tres cosas que separan a un junior contratable de uno que no

1. **Un pipeline que se puede volver a ejecutar sin romper nada (idempotencia + tests + manejo de errores).** El 74 % de las ofertas pide pipelines y el 43 % pide calidad de datos explícitamente. El junior no contratable entrega un notebook que funciona una vez; el contratable entrega un DAG con reintentos, `MERGE`/upsert, tests de unicidad y nulos, y sabe explicar qué pasa si se ejecuta dos veces el mismo día. Esto es lo que separa "he hecho un curso" de "he construido algo".
2. **Criterio de coste y de modelo, no de herramienta.** Saber por qué particionas por fecha, cuánto cuesta una consulta en BigQuery/Snowflake, por qué un `SELECT *` con `JOIN` sin filtro arruina la factura, y qué esquema (estrella vs. normalizado) responde a la pregunta de negocio. En las ofertas aparece como "data modelling" (38 %) y "scalability" (21 %); en la entrevista aparece como "¿por qué lo hiciste así?".
3. **Saber contar el proyecto en términos de negocio y de fiabilidad.** El 45 % de las ofertas son senior o superior y solo el **3 % son entry-level** (frente al 8 % de analista): la puerta de entrada es estrechísima, así que el junior se contrata por señal de criterio, no por lista de tecnologías. Eso significa: repo legible, README con decisiones y trade-offs, un caso con datos reales (INE, AEMET, TLC) y una frase clara de impacto. Y la ruta de entrada realista suele ser **analytics engineer, backend o analista junior durante 12–18 meses**, no "DE junior" directo.

### 5.4 Fuentes de este bloque

- ITJobsWatch — Data Engineer (UK, 6 meses a 2-nov-2026): https://www.itjobswatch.co.uk/jobs/uk/data%20engineer.do
- ITJobsWatch — dbt (evolución 2024→2026 y skills co-ocurrentes): https://www.itjobswatch.co.uk/jobs/uk/dbt.do
- InterviewStack — Data Engineer Skills in 2026 (6.877 ofertas, mayo 2026): https://interviewstack.io/blog/data-engineer-skills-companies-want-2026
- DataQuest — Data engineering skills that actually matter in 2026: https://www.dataquest.io/newsletters/data-engineering-skills-that-actually-matter-in-2026/
- lakeFS — The State of Data and AI Engineering 2025: https://lakefs.io/blog/the-state-of-data-ai-engineering-2025/
- Microsoft Learn — DP-700 (sustituto de DP-203): https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/
- Guvi — Top YouTube Channels to Learn Data Engineering (2026), usado para el mapa de canales: https://www.guvi.in/blog/top-youtube-channels-to-learn-data-engineering/

---

## TOP 10 imprescindibles

Ordenados por utilidad real para alguien que empieza de cero en Data Engineering. Criterio: si solo tuvieras estas diez, ¿llegarías a un portfolio contratable en 9–12 meses?

| # | Fuente | Tipo | Fase | Por qué está aquí (y no otra) |
|---|---|---|---|---|
| 1 | Data Engineering Zoomcamp — https://github.com/DataTalksClub/data-engineering-zoomcamp | Curso gratuito | F03, F04 | Es el único currículo gratuito que te lleva de cero a pipeline completo con las herramientas que piden las ofertas. Sin él, montas piezas sueltas y sin orden. |
| 2 | PostgreSQL Exercises — https://pgexercises.com/ | Práctica | F03 | SQL es el skill nº 1 en ofertas (36,5 % UK / 71 % global) y aquí se aprende con feedback inmediato, gratis y sin registro. |
| 3 | dbt Fundamentals — https://learn.getdbt.com/courses/dbt-fundamentals | Curso gratuito | F04 | El vocabulario mínimo del transform moderno, gratis y oficial. Es la diferencia entre "sé SQL" y "sé construir una capa de transformación". |
| 4 | Documentación de Apache Airflow — https://airflow.apache.org/docs/ | Documentación | F04 | Orquestar es el núcleo del trabajo diario. Aquí están los conceptos (idempotencia, backfill, retries) que separan junior de junior contratable. |
| 5 | NYC TLC Trip Records — https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page | Datos | F04, F05 | El dataset que permite el proyecto de portfolio clásico y serio: batch, particiones, join, modelado. Datos reales y sucios, licencia limpia. |
| 6 | Documentación de Apache Spark — https://spark.apache.org/docs/latest/ | Documentación | F04 | Spark aparece en un tercio de las ofertas y es donde se cae en entrevistas. La guía de tuning es el atajo para entender particiones y shuffles. |
| 7 | AWS Certified Data Engineer – Associate — https://aws.amazon.com/certification/certified-data-engineer-associate/ | Certificación (pago) | F04 | La credencial cloud con mejor retorno real para DE. No te hace ingeniero, pero pasa filtros de RR. HH. en consultoría, que es donde están muchas de las ofertas junior. |
| 8 | Data Engineering Weekly — https://www.dataengineeringweekly.com/ | Newsletter | F04, F08 | Una hora a la semana te mantiene al día de Iceberg, lakehouse e IA en datos con la mejor relación señal/ruido. Evita el FOMO de Twitter. |
| 9 | StatQuest — https://www.youtube.com/@statquest | Canal | F02, F06 | La base estadística se te queda corta y aquí se arregla con intuición visual. Necesario porque el 35 % de las ofertas de DE tocan ML/IA de apoyo. |
| 10 | Start Data Engineering — https://www.startdataengineering.com/ | Blog | F04, F11 | Donde aprendes a escribir pipelines como software (tests, CI/CD, calidad). Es el salto de "funciona en mi portátil" a "aguanta producción". |

**Los tres huecos que este TOP 10 deja y tú tienes que cubrir con el temario:** (1) **streaming real** con Kafka (solo el 17 % de las ofertas, pero es diferenciador y no hay fuente gratuita buena: tira de Confluent Developer); (2) **coste y rendimiento en el almacén** (no hay curso, solo documentación de Snowflake/BigQuery y práctica); (3) **datos españoles y contexto regulatorio** (RGPD, gobernanza), que ninguna fuente internacional cubre y que sí se pregunta en entrevistas en España.
