# Investigación de producto — cómo presentan su catálogo seis plataformas

Comprobado el **2026-11-04**. Método: lectura de las páginas públicas de cada plataforma (catálogo, ficha de curso, ficha de ruta, precios) y, cuando el sitio bloquea el acceso automatizado, de su centro de ayuda o de una captura archivada, indicándolo en la fila. **Los datos marcados «no comprobado» no se usan para decidir nada.**

Objetivo: Data School no va a ser otro curso, sino **el índice maestro** que enlaza y resume recursos ajenos. Esta investigación busca qué decisiones de presentación de catálogo ya están resueltas en el sector y cuáles merecen adoptarse.

## Resumen por plataforma

| Plataforma | Cómo ordena el contenido | Prerrequisitos | Metadatos por recurso | Coste que declara | Lo que hace bien |
|---|---|---|---|---|---|
| [roadmap.sh](https://roadmap.sh/roadmaps) | Grafo: 97 mapas (31 de rol, 61 de habilidad, 5 de buenas prácticas). El orden lo da el grafo, no una numeración | Explícitos y **enlazados entre mapas** («Pre-requisites: SQL, Python»); también «Related roadmaps» | Nodos con tema y recursos; packs y cursos con lecciones, minutos, nivel, proyecto y certificado verificable | Los mapas se leen sin registro; precio de packs **no comprobado** | El mejor modelo de navegación del grupo: dependencias reales y proyectos separados del temario |
| [DataTalksClub — DE Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Curso de módulos numerados + workshops + proyecto final; 6 zoomcamps hermanos (ML, LLM, MLOps…) | Básicos de código y SQL; Python «útil, no obligatorio». Nivel único | Dos modalidades: cohorte en vivo (deadlines, leaderboard, peer review, certificado) o a tu ritmo (sin certificado) | Gratis ambas | Separa la mecánica de cohorte del contenido reutilizable; avisa de que «en vivo» no son clases en directo |
| [Kaggle Learn](https://www.kaggle.com/learn) | Dos capas: **Guides** (colecciones curadas de la comunidad) y **Courses** (propios, ~18). Sin rutas de rol | «Builds on» / «Preparation for»: relaciones declaradas, no orden inventado | Lecciones Tutorial + Exercise; horas estimadas de certificado; coste explícito; instructor | «No cost, like all Kaggle Learn Courses» | Es el patrón más cercano al catálogo curado: metadatos honestos y capa editorial separada del contenido |
| [DataCamp](https://support.datacamp.com/en-us/articles/17598982-tracks-choosing-the-right-path) | Career Tracks vs Skill Tracks vs Courses, Projects, Assessments; una track activa a la vez | Track sin prerrequisitos, FAQ que explica carrera vs habilidad | Duración de track, nº de aprendices, instructores | Suscripción; importe **no comprobado** (bloqueo Cloudflare; cifras de captura archivada) | Explica la diferencia carrera/habilidad en FAQ, no en marketing |
| [Dataquest](https://www.dataquest.io/path/data-analyst/) | 5 Career Paths, 6 Skill Paths, cursos, proyectos, temas | Path «de cero a empleable» con pasos ordenados | **Esfuerzo semanal** (8 meses a 5 h/semana), nº de cursos, nº de proyectos, inscritos, valoración | Precio **no comprobado** (carga por JS) | Vende esfuerzo real y certificado **comprobable con URL pública** |
| [Maven Analytics](https://mavenanalytics.io/online-data-analysis-learning-paths) | Siete formatos: cursos, talleres en vivo, learning paths, proyectos guiados, crash courses, credenciales, drills | Etiquetas de skill y de persona, no requisitos duros | Cada curso: horas, quizzes, skills assessments, nivel, certificación | Free 0 $ · Pro 34 $/mes o 399 $/año · Teams 39 $/asiento ([precios](https://mavenanalytics.io/pricing)) | **Precio por ítem desde la primera pantalla** y ficha homogénea y comparable |
| [Mode / ThoughtSpot](https://mode.com/sql-tutorial/) (contraste) | Tutorial SQL gratis, legible sin registro, en cuatro niveles con lecciones numeradas (15+20+8+9) | Niveles explícitos, sin prerrequisitos enlazados | Sin ficha de recurso: es contenido propio, no catálogo | Gratis | Claridad de niveles; pero no es un catálogo |

## Qué hacen bien (decisión de producto, no marketing)

1. **El orden no se inventa: se declara.** roadmap.sh y Kaggle Learn dicen explícitamente «esto requiere esto» y «esto prepara para esto». Ninguno numera lecciones como si el orden fuera obvio.
2. **Los proyectos son una capa aparte del contenido.** roadmap.sh tiene galería de proyectos filtrable por nivel, y no los mete dentro del temario. Dataquest y Maven los cuentan como parte del path.
3. **La ficha es comparable.** Maven y Kaggle declaran en el mismo sitio: coste, horas, nivel, certificado y evaluación. Sin eso, comparar dos recursos es imposible.
4. **El coste va por ítem y avisado.** Maven pone el precio en la ficha; Coursera/edX marcan «auditar gratis / certificado de pago». Ninguna de las consultadas esconde el muro de pago hasta después de registrarse.
5. **El certificado es un dato, no una promesa.** Dataquest y Maven declaran certificado con verificación pública; Kaggle declara las horas estimadas para obtenerlo. Un catálogo serio debe copiar esto: certificado sí/no/verificable, nunca «certificado» a secas.
6. **Metadatos de esfuerzo, no solo duración.** «3 horas para el certificado» (Kaggle) y «8 meses a 5 h/semana» (Dataquest) son decidibles; «36 horas» no lo es.
7. **Ninguna resuelve los enlaces muertos.** Mode migró a ThoughtSpot y no avisa en el tutorial. Nadie que enlace contenido ajeno mantiene hoy una fecha de comprobación visible. **Ese es nuestro hueco.**

## Qué adoptamos en Data School

| Adopción | De quién | Por qué encaja | Nivel |
|---|---|---|---|
| **Doble eje rol + habilidad** en la navegación: un recurso se etiqueta por ruta (DE/DS/AI) y por habilidad (SQL, orquestación, dbt…), sin duplicar la ficha | DataCamp, Dataquest | La especificación pide tres rutas y puntos de cruce: el eje de habilidad es justo lo que las cruza | 2 (esquema) |
| **Aristas `requiere` / `prepara para`** entre tramos y recursos, en vez de un orden numerado inventado | roadmap.sh, Kaggle Learn | Permite responder «¿qué me falta?» sin escribir un temario | 2 (esquema) |
| **Ficha normalizada obligatoria**: tipo, coste, idioma, nivel, horas estimadas, proyecto incluido, certificado (sí/no/verificable), autor, **licencia, estado y fecha de comprobación** | Maven, Kaggle, y añadido propio | Es el corazón del producto; sin ficha no hay catálogo | 2 |
| **Esfuerzo real**: horas semanales sugeridas, no solo duración total | Dataquest, Kaggle | Decidible; ayuda a elegir entre dos recursos parecidos | 2 |
| **Capa editorial tipo «Guides»**: colecciones propia con criterio y motivo («por qué esta secuencia»), enlazando al proveedor | Kaggle Learn | Permite curar sin copiar temario: es exactamente la regla de oro | 2 |
| **Coste y aviso de pago en la ficha**, con estado `pending` si el coste no está confirmado | Maven, Coursera, edX | Evita el recurso trampa: gratis hasta que no lo es | 1 (datos) |
| **Certificado como dato verificable** (URL pública o «no emitido») | Dataquest, Maven | Convierte una promesa de marketing en un campo comprobable | 2 |
| **Comprobador de enlaces propio con fecha visible** | nadie (hueco) | Es el riesgo nº 1 de la especificación y el único punto donde ninguna plataforma compite | 1 |

## Qué NO se copia

- **El grafo y el contenido de roadmap.sh**: su FAQ prohíbe redistribuir el contenido. Se puede aprender del modelo, no replicar el mapa. `/roadmaps` se enlaza, no se rehace.
- **Los temarios y vídeos de los Zoomcamps, Kaggle Learn, Coursera, DataCamp…**: se enlazan y se resumen en palabras propias. Nunca una lista de lecciones copiada, ni un PDF, ni un vídeo dentro del repositorio.
- **Sus taxonomías comerciales** (Career Track vs Skill Track de DataCamp, packs de Maven): se usa el concepto, no su catálogo ni sus textos.
- **Los rankings de «más inscritos»**: no son un criterio de calidad —lo dice la propia especificación—, así que no se convierten en etiqueta del catálogo.

## Consecuencia para el modelo (propuesta)

El modelo de datos debe soportar: **rutas** con **tramos** ordenados por aristas `requiere/prepara`; **recursos** con ficha normalizada y estado de licencia/enlace fechado; **proyectos** como capa aparte, ligados a tramos; **datasets** con licencia por conjunto; y **progreso** por recurso/tramo/proyecto, que es una de las decisiones pendientes. La investigación confirma que un recurso puede pertenecer a dos rutas y a varias habilidades; por eso la relación recurso↔tramo debe ser **de muchos a muchos**, no una columna.

## Tareas que salen de aquí

1. Modelo de datos mínimo con aristas `requiere/prepara` y ficha normalizada (**nivel 2**, reversible; ver `BACKLOG.md`).
2. Comprobador de enlaces con fecha visible por recurso (**nivel 1**; ver `BACKLOG.md`).
3. Ficha de recurso con los estados `verified` / `pending` / `broken` y la fecha de comprobación (**nivel 2**, ya está en la especificación).
4. Capa de «Guides» editoriales cuando exista catálogo (nivel 2, no antes de tener 20 recursos).

Ninguna de estas propuestas amplía el alcance de la especificación: todas caben en las pantallas ya prometidas, así que **no hay pregunta de nivel 3 nueva**. La única decisión de nivel 3 pendiente sigue siendo la de la especificación (¿tres rutas separadas o una con tres salidas?), que afecta al modelo y está anotada en `BACKLOG.md`.
