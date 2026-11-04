# Certificaciones por nivel: qué sacar, cuándo y qué hay que aprender

**Fecha:** 2026-11-02 · **Regla que gobierna todo:** una certificación no arregla la falta de
proyectos. Si tienes que elegir entre pagar un examen y terminar PF-01, termina PF-01.

Los precios son aproximados y cambian: confirma el importe en la web oficial antes de pagar. Lo que
no cambia es el orden: primero lo gratis, después lo básico, y solo cuando hay proyecto, lo medio.

---

## 1. Los cuatro niveles

| Nivel | Qué es | Coste | Requisito para empezar | Para qué sirve |
| --- | --- | --- | --- | --- |
| 0 · Gratis | Cursos y badges sin examen de pago | 0 € | Ninguno | Vocabulario y primer currículo |
| 1 · Básicas | Fundamentos de nube, BI o analista | 90-170 USD | F03 y F04 iniciales | Primer filtro de RR. HH. y vocabulario |
| 2 · Medias | Data engineer de plataforma | 150-250 USD | Un proyecto terminado | El filtro real de las ofertas DE |
| 3 · Altas | Diseño, streaming y rendimiento | 200-375 USD | Dos años de práctica o un año intenso | Diferenciarte y subir de nivel |

**Ningún nivel se salta.** Sacar la de nivel 3 sin la 2 y sin proyecto es pagar por un examen que
no vas a aprobar o que no te va a servir.

---

## 2. Nivel 0 · Gratis (semanas 0-8)

No son certificaciones que se paguen, pero sí credenciales que se ponen en LinkedIn y, sobre todo,
el vocabulario mínimo para que el nivel 2 no te pille en blanco.

| Recurso | Qué da | Tiempo | Fases del portal |
| --- | --- | --- | --- |
| [dbt Fundamentals](https://learn.getdbt.com/courses/dbt-fundamentals) | Certificado gratuito de transformación | 5 h | F04: `dbt-y-transformacion` |
| [Confluent Developer](https://developer.confluent.io/courses/) | Cursos de Kafka con ejercicios | 8 h | F04: `kafka-y-colas` |
| [Astronomer Academy](https://academy.astronomer.io/) | Airflow práctico, cursos gratuitos | 6 h | F04: `airflow-dagster-prefect` |
| [Databricks Academy](https://www.databricks.com/learn/training/home) | Badge de fundamentos del lakehouse | 3 h | F04: `lakehouse-y-table-formats` |
| [Google Cloud Skills Boost](https://www.cloudskillsboost.google/) | Rutas gratuitas de BigQuery | 10 h | F04: `data-warehouse` |
| [AWS Skill Builder](https://skillbuilder.aws/) | Cursos básicos de Glue y S3 | 10 h | F04: `almacenamiento-de-objetos` |

**Qué hay que aprender antes de salir de aquí:** SQL con `JOIN` y ventanas, Python con `pandas`,
qué es un almacén, qué es un pipeline y qué es un fichero Parquet. Eso es F03 y la primera mitad
de F04.

---

## 3. Nivel 1 · Básicas (meses 1-4)

Son certificaciones de **contexto**, no de ingeniería. Sirven si vienes de cero, si tu CV no tiene
nada de datos o si tu mercado pide una credencial de entrada.

| Certificación | Coste | Qué evalúa | Qué hay que aprender | Cuándo no |
| --- | --- | --- | --- | --- |
| [AWS Certified Cloud Practitioner](https://aws.amazon.com/certification/certified-cloud-practitioner/) | ~100 USD | Servicios de AWS, facturación, seguridad básica | F03 y F04 inicial: qué es S3, una base de datos gestionada, IAM básico | Si ya vas a por la DEA-C01: sáltala |
| [Azure Fundamentals AZ-900](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) | ~99 USD | Nube, Azure, gobernanza y coste | Lo mismo en Azure; F04: `nubes-y-servicios-gestionados` | Si tu mercado es AWS |
| [Microsoft PL-300 (Power BI Data Analyst)](https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/) | ~165 USD | Modelado, DAX, visualización, seguridad | F03: SQL; F12: `visualizacion-honesta`, `dashboards` | Si tu objetivo no toca BI |
| [Databricks Lakehouse Fundamentals](https://www.databricks.com/learn/training/home) | Gratis (badge) | Conceptos de lakehouse y Delta | F04: `lakehouse-y-table-formats`, `parquet-avro-orc` | Es un badge, no un examen: no lo pongas como certificación |

**Qué se aprende de verdad en este nivel:** distinguir almacenamiento de cómputo, saber qué es un
rol y una política, entender una factura de nube y no confundir un panel con un pipeline. Si ya
tienes eso, salta al nivel 2.

---

## 4. Nivel 2 · Medias (meses 4-10)

Aquí está **la certificación que se pide en las ofertas**. Elige una, no tres.

| Certificación | Coste | Dominios que evalúa | Qué hay que aprender | Fases del portal |
| --- | --- | --- | --- | --- |
| [AWS Data Engineer – Associate (DEA-C01)](https://aws.amazon.com/certification/certified-data-engineer-associate/) | ~150 USD | Ingesta y transformación, almacén, operaciones, seguridad | Glue, S3, Athena, Redshift, IAM, KMS, coste | F04 completo + F11 (`iam-y-permisos-cloud`) |
| [Microsoft DP-700 (Fabric)](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/) | ~165 USD | Ingesta, lakehouse, warehouse, seguridad | Pipelines, Delta, Spark, RLS, OneLake | F04 + F11 (`control-de-acceso-por-fila-y-columna`) |
| [Databricks DE Associate](https://www.databricks.com/learn/certification/data-engineer-associate) | ~200 USD | Delta, PySpark, Auto Loader, workflows, Unity Catalog | `MERGE`, particiones, streaming, permisos | F04 (`spark-*`, `lakehouse-y-table-formats`) |
| [Snowflake SnowPro Core](https://www.snowflake.com/en/learn/certification/) | ~175 USD | Arquitectura, carga, clustering, seguridad | Micro-particiones, `COPY INTO`, roles, coste | F04 (`data-warehouse`, `particionado-y-clustering`) |
| [dbt Analytics Engineering](https://www.getdbt.com/certifications) | ~200 USD | Modelado, tests, incremental, documentación | dbt de verdad, no el tutorial | F04 (`dbt-y-transformacion`, `contratos-de-datos`) |

**Requisito real:** un pipeline propio funcionando, no un curso terminado. Si no puedes enseñar uno,
el examen te va a costar el doble porque estarás memorizando servicios que nunca has usado.

---

## 5. Nivel 3 · Altas (a partir del año 2)

Son exámenes de **diseño**, no de servicios: piden justificar arquitecturas, coste y rendimiento
con escenarios largos.

| Certificación | Coste | Qué añade | Qué hay que aprender |
| --- | --- | --- | --- |
| [Google Professional Data Engineer](https://cloud.google.com/learn/certification/data-engineer) | ~200 USD | Diseño de sistemas, Dataflow, BigQuery a escala | F04 avanzado, `streaming-tiempo-real`, `coste-y-optimizacion`, F11 |
| [Databricks DE Professional](https://www.databricks.com/learn/certification/data-engineer-professional) | ~200 USD | Rendimiento, streaming complejo, gobierno | `spark-joins-y-skew`, `flink-y-procesamiento-de-eventos`, `problema-de-ficheros-pequenos` |
| [SnowPro Advanced: Data Engineer](https://learn.snowflake.com/en/certifications/) | ~375 USD | Diseño, optimización, seguridad avanzada | `particionado-y-clustering`, `enmascarado-y-retencion`, `reconciliacion-y-pruebas` |
| [dbt Architect](https://www.getdbt.com/certifications) | ~300 USD | Arquitectura de transformación a escala | `modelado-dimensional`, `arquitectura-medallion`, `capa-semantica-y-metricas` |

Adyacentes que no son de data engineering pero suman: **AWS Machine Learning – Specialty** y
**Databricks ML Associate**. Solo si tu trabajo va a tocar modelos.

---

## 6. Ruta de 18 meses

| Meses | Nivel | Qué haces | Evidencia |
| --- | --- | --- | --- |
| 1-2 | 0 | Fundamentos gratuitos y primer proyecto | PF-01 en GitHub |
| 3-4 | 1 | Una básica (la de tu nube) y cerrar el proyecto | Badge + repo |
| 5-7 | 2 | Preparar la media y un segundo proyecto | PF-02 terminado |
| 8 | 2 | Examen de la media | Certificado |
| 9-12 | — | Tercer proyecto y portfolio | PF-03 o PF-04 |
| 13-16 | 3 | Preparar la alta (o la segunda media si cambias de plataforma) | PF-05 |
| 17-18 | 3 | Examen y postulación activa | Certificado + 3 repos |

Dos certificaciones y tres proyectos en 18 meses es un objetivo realista. Cinco certificaciones y
ningún proyecto es año y medio perdido con buena presentación.

---

## 7. Cómo se estudia cada nivel con el portal

| Dominio del examen | Nivel | Fase | Qué leer primero |
| --- | --- | --- | --- |
| SQL, Python, formatos | 1 | F03 | `sql-ventanas`, `sql-indices-y-planes`, `pandas-agrupaciones-y-joins` |
| Ingesta y transformación | 2 | F04 | `ingesta-incremental-y-cdc`, `dbt-y-transformacion` |
| Almacén y modelado | 2 | F04 | `modelado-dimensional`, `lakehouse-y-table-formats` |
| Operaciones y fiabilidad | 2-3 | F04, F11 | `calidad-y-slas`, `incidentes-y-postmortem` |
| Seguridad y gobierno | 2-3 | F11 | `iam-y-permisos-cloud`, `enmascarado-y-retencion` |
| Coste y rendimiento | 3 | F04 | `coste-y-optimizacion`, `problema-de-ficheros-pequenos` |
| Streaming | 3 | F04 | `kafka-y-colas`, `ventanas-y-watermarks`, `flink-y-procesamiento-de-eventos` |

El resto del examen es vocabulario de la plataforma: se estudia con la guía oficial y se fija con
un laboratorio propio, no con el portal.

---

## 8. Errores que cuestan dinero

- **Empezar por la de nivel 3.** Sin base y sin proyecto, el examen se aprueba memorizando y se
  olvida en un mes.
- **Sacar tres certificaciones del mismo nivel.** La segunda del mismo nivel no aporta señal.
- **Pagar el examen antes de un simulacro.** El intento fallido se paga igual.
- **Estudiar servicios que no vas a usar.** El examen pregunta por la solución al menor coste, no
  por la más moderna.
- **Dejar caducar sin renovar.** La renovación es más barata y más corta; el examen completo, no.
- **Poner la certificación como logro principal del CV.** Va en formación; el logro es el pipeline.

---

## 9. Todas las certificaciones, con su enlace

| Certificación | Nivel | Coste | Enlace oficial |
| --- | --- | --- | --- |
| dbt Fundamentals | 0 | Gratis | https://learn.getdbt.com/courses/dbt-fundamentals |
| Confluent Developer (Kafka) | 0 | Gratis | https://developer.confluent.io/courses/ |
| Astronomer Academy (Airflow) | 0 | Gratis | https://academy.astronomer.io/ |
| Databricks Lakehouse Fundamentals | 0 | Gratis (badge) | https://www.databricks.com/learn/training/home |
| Google Cloud Skills Boost | 0 | Gratis parcial | https://www.cloudskillsboost.google/ |
| AWS Skill Builder | 0 | Gratis parcial | https://skillbuilder.aws/ |
| AWS Cloud Practitioner | 1 | ~100 USD | https://aws.amazon.com/certification/certified-cloud-practitioner/ |
| Azure Fundamentals AZ-900 | 1 | ~99 USD | https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/ |
| Azure Data Fundamentals DP-900 | 1 | ~99 USD | https://learn.microsoft.com/en-us/credentials/certifications/azure-data-fundamentals/ |
| Microsoft PL-300 (Power BI) | 1 | ~165 USD | https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/ |
| AWS Data Engineer Associate (DEA-C01) | 2 | ~150 USD | https://aws.amazon.com/certification/certified-data-engineer-associate/ |
| Microsoft DP-700 (Fabric) | 2 | ~165 USD | https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/ |
| Databricks Data Engineer Associate | 2 | ~200 USD | https://www.databricks.com/learn/certification/data-engineer-associate |
| SnowPro Core | 2 | ~175 USD | https://www.snowflake.com/en/learn/certification/ |
| dbt Analytics Engineering | 2 | ~200 USD | https://www.getdbt.com/certifications |
| Confluent Certified Developer for Apache Kafka | 2 | ~150 USD | https://developer.confluent.io/certification/ |
| Astronomer Airflow Certification | 2 | ~250 USD | https://academy.astronomer.io/ |
| Google Professional Data Engineer | 3 | ~200 USD | https://cloud.google.com/learn/certification/data-engineer |
| Databricks Data Engineer Professional | 3 | ~200 USD | https://www.databricks.com/learn/certification/data-engineer-professional |
| SnowPro Advanced: Data Engineer | 3 | ~375 USD | https://learn.snowflake.com/en/certifications/ |
| dbt Architect | 3 | ~300 USD | https://www.getdbt.com/certifications |
| AWS Machine Learning – Specialty (adyacente) | 3 | ~300 USD | https://aws.amazon.com/certification/certified-machine-learning-specialty/ |
| Google Professional ML Engineer (adyacente) | 3 | ~200 USD | https://cloud.google.com/learn/certification/machine-learning-engineer |
| Databricks ML Associate (adyacente) | 3 | ~200 USD | https://www.databricks.com/learn/certification/machine-learning-associate |

Los precios son aproximados y cambian: confirma el importe en la página oficial antes de pagar.

---

## 10. Certificaciones de IA (las más demandadas en 2026)

No son de data engineering, pero el mercado ya pide «datos para IA»: pipelines de embeddings,
RAG, evaluación y despliegue. Si vas a tocar eso —y casi todo equipo lo toca—, una de estas suma.

| Certificación | Nivel | Coste | Qué evalúa | Qué hay que aprender |
| --- | --- | --- | --- | --- |
| [AWS AI Practitioner (AIF-C01)](https://aws.amazon.com/certification/certified-ai-practitioner/) | 1 | ~100 USD | Fundamentos de IA y generative AI en AWS | Vocabulario de modelos, Bedrock, SageMaker básico, IA responsable (F08) |
| [Azure AI Fundamentals (AI-900)](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/) | 1 | ~99 USD | Servicios de IA de Azure | Visión, lenguaje, IA generativa y sus límites (F08) |
| [Azure AI Engineer (AI-102)](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/) | 2 | ~165 USD | Diseñar e implementar soluciones de IA | Azure OpenAI, RAG con AI Search, agentes, seguridad y evaluación (F08) |
| [AWS ML Engineer – Associate (MLA-C01)](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) | 2 | ~150 USD | Pipelines de ML y despliegue | Feature engineering, entrenamiento, MLOps, monitorización (F06, F07) |
| [Databricks ML Associate](https://www.databricks.com/learn/certification/machine-learning-associate) | 2 | ~200 USD | ML en el lakehouse | MLflow, feature store, serving, evaluación (F06, F07) |
| [Google Professional ML Engineer](https://cloud.google.com/learn/certification/machine-learning-engineer) | 3 | ~200 USD | Diseño de sistemas de ML | Arquitectura, MLOps, BigQuery ML, coste (F06, F07, F11) |
| [Databricks ML Professional](https://www.databricks.com/learn/certification/machine-learning-professional) | 3 | ~200 USD | ML a escala | Serving, monitorización, gobierno de modelos (F07, F11) |

**Preparación gratis:** los cursos de [Hugging Face](https://huggingface.co/learn) y de
[DeepLearning.AI](https://www.deeplearning.ai/short-courses/) cubren el temario conceptual; el
examen se aprueba con el simulacro oficial y con un RAG propio funcionando.

**Cuándo sí:** si tu mercado pide «AI engineer», «ML engineer» o «data engineer para IA». **Cuándo
no:** si aún no tienes una certificación media de datos. La de IA sin la de datos te deja en tierra
de nadie: sabes de modelos y no sabes moverlos.

---

## 11. Certificaciones de IA gratuitas (sí, existen)

No tienen el peso de un examen de pago, pero dan credencial verificable, se ponen en LinkedIn y
sirven para lo que tú quieres: acreditar que empiezas y tener algo que enseñar mientras haces el
primer proyecto.

| Credencial | Coste | Qué acredita | Enlace |
| --- | --- | --- | --- |
| IBM SkillsBuild · AI Fundamentals | Gratis, con certificado | Fundamentos de IA, casos de uso y ética | https://skillsbuild.org/ |
| Cisco NetAcad · AI Fundamentals with IBM SkillsBuild | Gratis, con insignia | El mismo temario con plataforma de curso | https://www.netacad.com/courses/ai-fundamentals-with-ibm-skillsbuild |
| Google Cloud · Generative AI skill badges | Gratis (algunos con créditos) | Badges de IA generativa y Vertex AI | https://www.cloudskillsboost.google/ |
| Microsoft Learn · rutas de IA | Gratis (módulos y trofeos; el examen se paga) | Vocabulario de Azure AI y Copilot | https://learn.microsoft.com/en-us/training/ |
| Databricks Academy · badges | Gratis | Lakehouse, fundamentos de ML | https://www.databricks.com/learn/training/home |
| Hugging Face Course | Gratis (sin certificado oficial) | Transformers, datasets, despliegue | https://huggingface.co/learn |

**Cómo usarlas sin engañarte:** el badge no demuestra que sepas construir; demuestra que has hecho
el curso. Ponlo en formación y que el proyecto hable por ti. Y no pagues un examen de IA hasta
tener una media de datos: sin ella, sabes de modelos y no sabes moverlos.

---

## 12. Qué lecciones cubren cada certificación

La escuela cubre los **conceptos**; el examen pregunta además por **servicios con nombre**. Esta
tabla dice qué está cubierto y qué hay que estudiar aparte.

| Bloque del examen | ¿Cubierto? | Lecciones |
| --- | --- | --- |
| SQL y datos | Sí | `sql-ventanas`, `sql-indices-y-planes`, `sql-subconsultas-y-cte` |
| Ingesta y transformación | Sí | `ingesta-incremental-y-cdc`, `dbt-y-transformacion`, `eventos-push-y-webhooks` |
| Almacén y modelado | Sí | `modelado-dimensional`, `lakehouse-y-table-formats`, `data-warehouse` |
| Streaming | Sí | `kafka-y-colas`, `ventanas-y-watermarks`, `flink-y-procesamiento-de-eventos`, `registro-de-esquemas` |
| Operaciones y fiabilidad | Sí | `calidad-y-slas`, `incidentes-y-postmortem`, `backfill-y-reproceso` |
| Seguridad y gobierno | Sí | `iam-y-permisos-cloud`, `enmascarado-y-retencion`, `gobierno-y-privacidad` |
| Coste y rendimiento | Sí | `coste-y-optimizacion`, `problema-de-ficheros-pequenos`, `particionado-y-clustering` |
| Fundamentos de IA | Sí | `que-es-un-llm`, `prompting`, `alucinaciones-y-limites`, `sesgo-y-etica-en-datos` |
| RAG y embeddings | Sí | `rag-arquitectura`, `embeddings`, `chunking-y-embeddings`, `bases-de-datos-vectoriales` |
| Evaluación de modelos generativos | Sí | `evaluacion-de-llms`, `evaluacion-de-modelos-generativos`, `metricas-de-clasificacion` |
| MLOps y despliegue | Sí | `mlops-y-cicd-de-modelos`, `exportar-y-servir-modelos`, `monitorizacion-de-drift`, `feature-store` |
| Agentes y herramientas | Sí | `agentes-y-herramientas`, `seguridad-y-prompt-injection`, `idempotencia-en-apis` |
| Nombres de servicios (S3, Glue, Bedrock, Azure OpenAI…) | **No** | Se estudia con la guía oficial y el laboratorio |

**Conclusión honesta:** de los 13 bloques, 12 están cubiertos con páginas propias y solo falta el
vocabulario de servicios de cada plataforma. Eso no se aprende en una página: se aprende con la
guía del examen y con una cuenta real.
