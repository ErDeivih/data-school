# Fuentes verificadas — Data School

Comprobación hecha el **2026-11-04 (UTC)**. Método: petición HTTP real a cada sitio (código de estado y redirección final), lectura de su página de licencia o del `LICENSE` del repositorio, y comprobación de la página de precio cuando aplica. Cada fila lleva el enlace a la evidencia de la licencia.

Informe automático de esta misma comprobación: [`INFORMES/enlaces-2026-11-04.md`](INFORMES/enlaces-2026-11-04.md) — 60 enlaces comprobados: 57 vivos, 3 redirigen (sin caídos). Se regenera con `npm run check:links`.

Las fuentes de la especificación entran como **candidatas**; aquí se quedan solo las que se han podido comprobar. Ninguna se da por buena «porque es famosa».

## Cómo se lee la tabla

- **Licencia**: la que consta por escrito. «Sin licencia explícita» = no hay `LICENSE` ni términos de reutilización publicados: se enlaza y se resume con palabras propias, no se reutiliza texto, figuras ni temario.
- **Coste**: gratis · gratis con cuenta · mixto (parte gratis y parte de pago, avisada) · de pago.
- **Idioma**: el del contenido, no el de la interfaz.
- **Estado**: `viva` (responde y publica hoy) · `viva (rebrand)` (cambió de nombre o dominio y redirige) · `muerta` (cerró o redirige fuera del servicio).
- **Tramo**: F = fundamentos · DE = data engineer · DS = data scientist · AI = AI engineer · T = transversal.

## Reglas de entrada al catálogo (salidas de la verificación)

1. Todo recurso entra **enlazado**, con URL oficial, licencia declarada y **fecha de última comprobación**.
2. Licencia clara y enlace vivo → estado `verified`. Sin licencia explícita, o licencia que solo permite uso personal → estado `pending` y **solo enlace**: no se copia texto, figura, temario ni PDF ajeno.
3. De pago **que avisa** → se enlaza con la marca «de pago». De pago que no avisa → fuera del catálogo.
4. El resumen es propio y corto (una o dos líneas): se describe qué enseña y a quién sirve, nunca se reproduce el temario.
5. Un principal y dos alternativas por tramo. Más de eso no ayuda, aturde.

## 1. Itinerarios (rutas y cursos estructurados)

| Fuente | Qué es y qué enseña | Licencia | Coste | Idioma | Estado | Tramo |
|---|---|---|---|---|---|---|
| [roadmap.sh](https://roadmap.sh) | Mapas visuales de habilidades por rol (data engineer, data scientist, AI engineer…) con recursos en cada nodo, progreso e itinerarios; referencia de **estructura de ruta**, no de temario | Contenido **no redistribuible** (lo dice su [FAQ](https://roadmap.sh/about)); el código es open-core en GitHub | Mixto, **avisado**: plan gratis con límites + Pro de pago ([premium](https://roadmap.sh/premium)) | Inglés | viva | DE · DS · AI |
| [DataTalksClub — DE Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Curso gratis de 9 semanas de data engineering: Docker/Terraform, orquestación, warehouse, dbt, Spark, Kafka y proyecto final; cohorte en vivo con deberes corregidos o a tu ritmo | **Sin licencia explícita**: el repo no tiene `LICENSE` (GitHub la marca vacía) y su README dice «free and open-source» sin fijar términos | Gratis | Inglés | viva (cohorte enero 2027) | DE (principal) |
| [MIT OCW](https://ocw.mit.edu) | Más de 2.500 cursos del MIT liberados: matemáticas, estadística, programación, fundamentos de datos | [CC BY-NC-SA 4.0](https://ocw.mit.edu/pages/privacy-and-terms-of-use/) — no comercial, compartir igual, con atribución | Gratis | Inglés (algunos traducidos) | viva | F |
| [freeCodeCamp](https://www.freecodecamp.org) | Currículo interactivo de programación (Python, SQL, JavaScript) con certificaciones; base para entrar en la ruta | Código [BSD-3-Clause](https://github.com/freeCodeCamp/freeCodeCamp/blob/main/LICENSE.md); el **currículo es © freeCodeCamp** y no se redistribuye | Gratis | Inglés (hay parte traducida) | viva | F |
| [Kaggle Learn](https://www.kaggle.com/learn) | Micro-cursos prácticos de Python, pandas, SQL, visualización y ML, con cuadernos y certificado de Kaggle | Contenido © Kaggle: **solo enlace**; los datasets son aparte y llevan licencia propia | Gratis con cuenta | Inglés | viva | DS · DE (práctica) |
| [dbt Learn](https://learn.getdbt.com/catalog) | Cursos oficiales de dbt (fundamentos, modelado, tests, despliegue) con cuenta gratis; la certificación de dbt va aparte | Material de formación © dbt Labs; los [docs](https://docs.getdbt.com) tienen repo Apache-2.0, pero el sitio servido es «All Rights Reserved» | Gratis con cuenta (certificación de pago) | Inglés | viva (el catálogo vive en `/catalog`) | DE (analytics engineering) |
| [Google Skills](https://www.skills.google/) — antes Google Cloud Skills Boost | Labs guiados de Google Cloud, skill badges, rutas y certificaciones; complemento práctico de cloud, no un curso de datos completo | Contenido © Google: solo enlace | Mixto, **avisado**: cursos y créditos gratis + suscripciones ([suscripciones](https://www.skills.google/subscriptions)) | Inglés (interfaz localizada) | viva (rebrand: `cloudskillsboost.google` redirige) | DE (complemento) |

## 2. Cursos y vídeos

| Fuente | Qué es y qué enseña | Licencia | Coste | Idioma | Estado | Tramo |
|---|---|---|---|---|---|---|
| [Coursera](https://www.coursera.org) | Catálogo de cursos de universidades y empresas; auditoría gratuita en muchos cursos y certificado de pago | Contenido © Coursera y sus instructores: solo enlace | Mixto, **avisado**: auditar gratis, certificado de pago | Original en inglés; subtítulos y algunos cursos en español (33 idiomas en el curso comprobado) | viva | T (alternativa de pago) |
| [edX](https://www.edx.org) | Cursos de universidades con pista de auditoría gratuita y certificado verificado de pago | Contenido © edX y sus socios: solo enlace | Mixto, **avisado**: [auditar gratis](https://www.edx.org/learn/data-science), certificado de pago | Inglés (algunos cursos en español) | viva | T (alternativa de pago) |
| [DeepLearning.AI](https://www.deeplearning.ai) | Cursos cortos de IA generativa y LLMs, y especializaciones; enseña a construir aplicaciones con modelos | Contenido © DeepLearning.AI: solo enlace | Los cursos cortos están gratis **por tiempo limitado** en la beta de su plataforma ([ejemplo](https://www.deeplearning.ai/courses/chatgpt-prompt-eng)); las especializaciones son de pago | Inglés | viva | AI |
| [fast.ai](https://course.fast.ai/) | Curso práctico de deep learning en 9 lecciones, con libro gratis para leer en línea | Código **GPL-3.0**; la prosa **no permite redistribución** ([LICENSE del libro](https://raw.githubusercontent.com/fastai/fastbook/master/LICENSE)) | Gratis | Inglés | viva | AI (alternativa) |
| YouTube — canales técnicos ([StatQuest](https://www.youtube.com/@statquest), [Alex The Analyst](https://www.youtube.com/@AlexTheAnalyst), [DataTalksClub](https://www.youtube.com/@DataTalksClub), [3Blue1Brown](https://www.youtube.com/@3blue1brown)) | Vídeo de apoyo: estadística, SQL, análisis y matemáticas explicadas; complementa, no sustituye a una ruta | Licencia estándar de YouTube: **no reutilizable**; solo enlazar el vídeo (algunos canales publican vídeos CC BY) | Gratis | Inglés (mayoría); hay canales en español sin verificar | viva (4/4 canales responden) | F · DS · AI (apoyo) |

## 3. Libros y documentación oficial

| Fuente | Qué es y qué enseña | Licencia | Coste | Idioma | Estado | Tramo |
|---|---|---|---|---|---|---|
| [Docs de Python](https://docs.python.org/3/) | Referencia del lenguaje y la biblioteca estándar: la fuente primaria de Python | [PSF-2.0](https://docs.python.org/3/license.html) (ejemplos de código también en Zero-Clause BSD) | Gratis | Inglés + [traducción parcial al español](https://docs.python.org/es/3/) | viva (3.15) | F |
| [Docs de PostgreSQL](https://www.postgresql.org/docs/) | Manual oficial de SQL en PostgreSQL, por versión | [PostgreSQL License](https://www.postgresql.org/about/licence/) (permisiva, tipo BSD/MIT) | Gratis | Inglés | viva | F · DE |
| [Docs de SQLite](https://www.sqlite.org/docs.html) | Tutorial de SQL y referencia del motor más desplegado | [Dominio público](https://www.sqlite.org/copyright.html) | Gratis | Inglés | viva | F (SQL) |
| [Docs de dbt](https://docs.getdbt.com) | Guías y referencia de dbt Core y Cloud: modelado, tests, despliegue | Repo de docs [Apache-2.0](https://raw.githubusercontent.com/dbt-labs/docs.getdbt.com/current/License.md), pero el sitio servido dice «© dbt Labs. All Rights Reserved»: **solo enlace** | Gratis (dbt Cloud es de pago aparte) | Inglés | viva | DE |
| [Docs de Apache Spark](https://spark.apache.org/docs/latest/) | Guía de programación y referencia de API de Spark | [Apache-2.0](https://raw.githubusercontent.com/apache/spark/master/LICENSE) | Gratis | Inglés | viva (Spark 4.3) | DE |
| [Docs de Apache Airflow](https://airflow.apache.org/docs/) | Documentación por versión, tutoriales y referencia de operadores | [Apache-2.0](https://raw.githubusercontent.com/apache/airflow/main/LICENSE) | Gratis | Inglés | viva | DE |
| [Docs de DuckDB](https://duckdb.org/docs/) | Guía y referencia SQL de la base de datos analítica embebida | [MIT](https://raw.githubusercontent.com/duckdb/duckdb/main/LICENSE) | Gratis | Inglés | viva | F · DE |
| [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) | Manual de numpy, pandas, matplotlib y ML con cuadernos | Texto [CC BY-NC-ND 3.0](https://raw.githubusercontent.com/jakevdp/PythonDataScienceHandbook/master/LICENSE-TEXT) + código MIT: **no derivadas, no comercial** | Gratis | Inglés | viva | DS |
| [An Introduction to Statistical Learning](https://www.statlearning.com/) | El manual estándar de estadística y ML clásico (ISLR/ISLP), PDF gratis | **Sin licencia explícita**: «© 2021-2023 … All Rights Reserved» → leer sí, redistribuir no | Gratis el PDF (impresión de pago) | Inglés | viva | DS (principal de estadística) |
| [Dive into Deep Learning](https://d2l.ai/) | Libro interactivo de deep learning con código (PyTorch/JAX/TF) | Texto [CC BY-SA 4.0](https://raw.githubusercontent.com/d2l-ai/d2l-en/master/LICENSE) + código «modified MIT» | Gratis | Inglés (y chino) | viva | AI |
| [Mathematics for Machine Learning](https://mml-book.github.io/) | Matemáticas para ML: álgebra, cálculo, probabilidad y optimización | **No es open access**: [el PDF](https://mml-book.github.io/book/mml-book.pdf) permite solo visualización y descarga personal; prohíbe redistribuir y obras derivadas | Gratis para uso personal (impresión de pago) | Inglés | viva | F · AI |

## 4. Datasets

| Fuente | Qué es y qué enseña | Licencia | Coste | Idioma | Estado | Tramo |
|---|---|---|---|---|---|---|
| [Kaggle Datasets](https://www.kaggle.com/datasets) | Miles de conjuntos reales con API y cuadernos; para practicar SQL, joins, EDA y modelos | **Una licencia por dataset**, elegida por el autor: comprobado CC0, CC BY 4.0, Apache-2.0, MIT, «Other» y «Unknown» ([API de Kaggle](https://www.kaggle.com/api/v1/datasets/list?search=iris)) | Gratis con cuenta | Inglés (metadatos); datos en muchos idiomas | viva | DE · DS · AI |
| [Hugging Face Datasets](https://huggingface.co/datasets) | Catálogo de datasets con filtro por licencia, idioma y tarea; fuerte en texto e IA | Licencia **por dataset** (el Hub permite filtrar por licencia); cada ficha declara la suya | Gratis (cuenta para lo privado) | Multilingüe | viva | AI · DS |
| [data.gov](https://data.gov) | Catálogo federal de datos abiertos de EE. UU.: economía, clima, transporte, salud | Licencia **por conjunto**, fijada por la agencia que publica (mayoría dominio público federal); hay que leer la ficha de cada dataset | Gratis | Inglés | viva | DE · DS (datos reales) |
| [datos.gob.es](https://datos.gob.es) | Catálogo español de datos abiertos; licencia declarada en los metadatos del dataset ([API](https://datos.gob.es/apidata/catalog/dataset), p. ej. `CC_BY_4_0`) | **Una licencia por dataset**, declarada en metadatos (comprobado CC BY 4.0) | Gratis | Español (descripciones también en inglés) | viva | DE · DS (datos reales) |
| [UCI Machine Learning Repository](https://archive.ics.uci.edu/) | Datasets clásicos de ML y estadística, referencia académica | **Una licencia por dataset** ([iris: CC BY 4.0](https://archive.ics.uci.edu/dataset/53/iris)) | Gratis | Inglés | viva | F · DS |
| [IMDb non-commercial datasets](https://data.imdb.com/non-commercial-datasets/) | Ficheros TSV de películas, series y personas para práctica de SQL y joins; refresco diario | **Solo uso personal y no comercial** ([términos](https://data.imdb.com/non-commercial-datasets/)) | Gratis | Inglés | viva (URL cambiada: `imdb.com/interfaces` redirige aquí; descarga en [datasets.imdbws.com](https://datasets.imdbws.com/)) | DS · DE (ejercicios de SQL) |

## 5. Papers

| Fuente | Qué es y qué enseña | Licencia | Coste | Idioma | Estado | Tramo |
|---|---|---|---|---|---|---|
| [arXiv](https://arxiv.org) | Preprints de matemáticas, estadística, ML e IA; la fuente primaria para seguir el estado del arte | **Una licencia por paper**, elegida por el autor al enviar: CC0, CC BY 4.0, CC BY-SA 4.0, CC BY-NC-SA 4.0, CC BY-NC-ND 4.0 o licencia perpetua no exclusiva de arXiv ([info](https://info.arxiv.org/help/license/index.html)) | Gratis | Inglés | viva | AI · DS (avanzado) |
| [Hugging Face Papers](https://huggingface.co/papers) | Ranking diario de papers con enlace a código y demo; sustituto práctico de Papers with Code | Sin licencia propia: ToS de Hugging Face; cada paper conserva la licencia de arXiv | Gratis (cuenta para votar o suscribirse) | Inglés | viva | AI |
| [Papers with Code](https://paperswithcode.com) | — | — | — | — | **muerta**: el dominio redirige a `huggingface.co/papers/trending` | — (descartada) |

## Descartes y cambios de esta verificación

| Fuente | Qué pasó | Decisión |
|---|---|---|
| Papers with Code | El dominio entero (incluido `/about`) responde **302** a `https://huggingface.co/papers/trending`; cerró en 2025 sin aviso | **Fuera del catálogo.** Se sustituye por [Hugging Face Papers](https://huggingface.co/papers), con la advertencia de que sus rankings no son los de PwC |
| Google Cloud Skills Boost | `cloudskillsboost.google` redirige a [skills.google](https://www.skills.google/): la plataforma cambió de nombre | Entra como «Google Skills», marcada como complemento de pago |
| IMDb datos | `imdb.com/interfaces` ya no es la URL de descarga: redirige a `data.imdb.com/non-commercial-datasets/` | Se enlaza la URL nueva y se marca **solo uso no comercial** |
| dbt Learn | El catálogo responde en `learn.getdbt.com/catalog`, pero el curso y la certificación tienen costes distintos | Se enlaza el curso gratis; la certificación se marca aparte si entra |
| roadmap.sh | Su FAQ prohíbe redistribuir el contenido, y el plan gratis es limitado (Pro de pago) | Se enlaza como **referencia de estructura de rutas**; no se copia el contenido ni se toma su mapa como temario propio |

## Recuento

- **32 fuentes comprobadas**: 31 vivas y **1 muerta** (Papers with Code, sustituida).
- **0 descartadas por ser de pago sin avisar**: las de pago revisadas (roadmap.sh Pro, Coursera, edX, Google Skills) avisan del coste antes de pagar.
- **11 fuentes con licencia restrictiva o sin licencia explícita** (DataTalksClub, roadmap.sh, Kaggle Learn, dbt Learn, Coursera, edX, DeepLearning.AI, fast.ai, docs de dbt, PDSH, ISLR, MML, IMDb, YouTube): entran **solo enlace + resumen propio**, nunca material copiado.
- **Fuentes reutilizables con atribución** (útiles si algún día hace falta citar texto o figuras): MIT OCW (CC BY-NC-SA), d2l (CC BY-SA), freeCodeCamp (solo código BSD-3), Python (PSF-2.0), Spark/Airflow (Apache-2.0), DuckDB (MIT), PostgreSQL (PostgreSQL License), SQLite (dominio público), arXiv según paper.
- **Tramos cubiertos**: F y DE con principal y alternativas; DS con principal de estadística y práctica; AI con principal (DeepLearning.AI) y alternativas (fast.ai, d2l, arXiv). La ruta DE tiene el principal más fuerte (DE Zoomcamp, gratis y con proyecto final).
