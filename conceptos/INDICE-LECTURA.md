# Orden de lectura por fase — Data School

**Fecha:** 2026-11-04

**Total:** 459 conceptos repartidos en 13 fases (f00–f12).

**Qué es este documento.** El orden recomendado para leer los conceptos de cada fase, calculado a partir del campo `prerequisitos` del frontmatter de los 459 `.md`. No es una regla ni un requisito: es una recomendación derivada de los prerequisitos. Si un concepto se entiende sin haber leído los anteriores (o si ya los sabes), puedes leerlo antes; el orden solo evita empezar por el tejado.

## Cómo se ha calculado

1. Se lee el frontmatter (`id`, `titulo`, `fase`, `prerequisitos`) de los 459 `.md`; `prerequisitos` es una lista de `id` de otros conceptos.
2. Dentro de cada fase se construyen las aristas `prerequisito → concepto` usando **solo** prerequisitos que pertenecen a la misma fase.
3. Se aplica el **orden topológico de Kahn**: en cada paso se elige el concepto sin prerequisitos pendientes cuyo `id` es alfabéticamente menor (desempate determinista). El mismo conjunto de entrada produce siempre el mismo orden.
4. Los prerequisitos que están en **otra fase** no bloquean el orden dentro de la fase: se anotan como *prerequisitos externos* en la última columna, para que sepas qué conviene llevar leído de antes.
5. Se comprueba que cada `id` de `prerequisitos` existe como concepto y se buscan ciclos (conceptos que se esperan unos a otros).

## Comprobaciones

- Filas por fase: f00=14, f01=41, f02=26, f03=42, f04=61, f05=29, f06=49, f07=33, f08=22, f09=61, f10=32, f11=34, f12=15; suma **459**.
- Conceptos sin prerequisitos dentro de su fase (puntos de entrada): **66**.
- Conceptos con prerequisitos de otra fase: **229** (394 referencias externas en total).
- `id` de prerrequisito que no existe como concepto: **0**.
- Ciclos detectados: **0**.

## Resumen

| Fase | Nombre | Conceptos | Puntos de entrada | Con prereq. externos | Conceptos externos citados |
| --- | --- | ---: | ---: | ---: | ---: |
| f00 | Aprender a aprender | 14 | 2 | 0 | 0 |
| f01 | Fundamentos matemáticos | 41 | 6 | 9 | 2 |
| f02 | Inferencia y estadística | 26 | 1 | 20 | 11 |
| f03 | Python, SQL y herramientas | 42 | 1 | 2 | 4 |
| f04 | Ingeniería de datos | 61 | 6 | 33 | 22 |
| f05 | Exploración y series temporales | 29 | 9 | 21 | 26 |
| f06 | Machine learning clásico | 49 | 11 | 28 | 33 |
| f07 | Deep learning | 33 | 3 | 28 | 27 |
| f08 | LLMs e IA generativa | 22 | 2 | 14 | 16 |
| f09 | Finanzas cuantitativas | 61 | 11 | 37 | 38 |
| f10 | Algoritmos y estructuras | 32 | 3 | 8 | 11 |
| f11 | Ingeniería de software | 34 | 6 | 21 | 20 |
| f12 | Comunicación y carrera | 15 | 5 | 8 | 13 |
| **Total** | **13 fases** | **459** | **66** | **229** | — |

---

## f00 — Aprender a aprender (14 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `como-estudiar`, `notacion-matematica`.

**Prerequisitos externos:** ninguno.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `como-estudiar` | Cómo estudiar esto | — | — |
| 2 | `leer-documentacion-oficial` | Leer la documentación oficial | `como-estudiar` | — |
| 3 | `mapa-del-portal` | Cómo usar este portal | `como-estudiar` | — |
| 4 | `escribir-tarjetas-de-repaso` | Escribir tarjetas de repaso | `como-estudiar`, `mapa-del-portal` | — |
| 5 | `hacer-preguntas-buenas` | Formular buenas preguntas | `mapa-del-portal` | — |
| 6 | `como-leer-un-paper` | Cómo leer un paper | `como-estudiar`, `hacer-preguntas-buenas` | — |
| 7 | `medir-tu-progreso` | Medir tu progreso sin engañarte | `como-estudiar` | — |
| 8 | `notacion-matematica` | Notación matemática | — | — |
| 9 | `pedir-ayuda-tecnica` | Pedir ayuda técnica y que te la den | `hacer-preguntas-buenas` | — |
| 10 | `practicar-con-datos-reales` | Practicar con datos reales | `hacer-preguntas-buenas` | — |
| 11 | `fuentes-y-canales` | Fuentes, canales y datos | `como-estudiar`, `practicar-con-datos-reales` | — |
| 12 | `rutas-de-aprendizaje` | Rutas de aprendizaje | `como-estudiar`, `mapa-del-portal` | — |
| 13 | `tomar-notas-tecnicas` | Tomar notas técnicas | `como-estudiar` | — |
| 14 | `usar-ia-para-aprender` | Usar la IA para aprender sin engañarte | `como-estudiar`, `hacer-preguntas-buenas` | — |

## f01 — Fundamentos matemáticos (41 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `escalares-vectores-matrices`, `limites-y-continuidad`, `logaritmos-y-escalas-logaritmicas`, `medidas-de-centralidad`, `precision-y-error-numerico`, `probabilidad-axiomas`.

**Prerequisitos externos:** 9 conceptos dependen de 2 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `escalares-vectores-matrices` | Escalares, vectores y matrices | — | `notacion-matematica` (f00) |
| 2 | `limites-y-continuidad` | Límites y continuidad | — | `notacion-matematica` (f00) |
| 3 | `derivadas-y-reglas` | Derivadas y reglas de derivación | `limites-y-continuidad` | — |
| 4 | `integrales` | Integrales | `derivadas-y-reglas`, `limites-y-continuidad` | — |
| 5 | `logaritmos-y-escalas-logaritmicas` | Logaritmos y escalas logarítmicas | — | `notacion-matematica` (f00) |
| 6 | `medidas-de-centralidad` | Medidas de centralidad | — | `notacion-matematica` (f00) |
| 7 | `cuantiles-y-percentiles` | Cuantiles y percentiles | `medidas-de-centralidad` | `notacion-matematica` (f00) |
| 8 | `medidas-de-dispersion` | Medidas de dispersión | `medidas-de-centralidad` | `notacion-matematica` (f00) |
| 9 | `asimetria-y-curtosis` | Asimetría y curtosis | `medidas-de-centralidad`, `medidas-de-dispersion` | — |
| 10 | `operaciones-matriciales` | Operaciones con matrices | `escalares-vectores-matrices` | — |
| 11 | `determinante-rango-invertibilidad` | Determinante, rango e inversa | `operaciones-matriciales` | — |
| 12 | `precision-y-error-numerico` | Precisión y error numérico | — | `notacion-matematica` (f00) |
| 13 | `probabilidad-axiomas` | Axiomas de probabilidad | — | — |
| 14 | `probabilidad-condicional` | Probabilidad condicional | `probabilidad-axiomas` | — |
| 15 | `cadenas-de-markov` | Cadenas de Markov | `operaciones-matriciales`, `probabilidad-condicional` | — |
| 16 | `independencia-y-condicionamiento` | Independencia y condicionamiento | `probabilidad-axiomas`, `probabilidad-condicional` | — |
| 17 | `producto-punto-y-similitud` | Producto punto y similitud | `escalares-vectores-matrices` | — |
| 18 | `norma-y-distancias` | Normas y distancias | `producto-punto-y-similitud` | — |
| 19 | `regla-de-la-cadena` | Regla de la cadena | `derivadas-y-reglas`, `limites-y-continuidad` | — |
| 20 | `derivadas-parciales-y-gradiente` | Derivadas parciales y gradiente | `derivadas-y-reglas`, `escalares-vectores-matrices`, `producto-punto-y-similitud`, `regla-de-la-cadena` | — |
| 21 | `convexidad` | Convexidad | `derivadas-parciales-y-gradiente`, `derivadas-y-reglas` | — |
| 22 | `jacobiano-y-hessiano` | Jacobiano y Hessiano | `derivadas-parciales-y-gradiente`, `operaciones-matriciales` | — |
| 23 | `optimizacion-con-restricciones` | Optimización con restricciones | `convexidad`, `derivadas-parciales-y-gradiente`, `jacobiano-y-hessiano` | — |
| 24 | `teorema-de-bayes` | Teorema de Bayes | `probabilidad-axiomas`, `probabilidad-condicional` | — |
| 25 | `transformaciones-lineales` | Transformaciones lineales | `escalares-vectores-matrices`, `operaciones-matriciales` | — |
| 26 | `autovalores-y-autovectores` | Autovalores y autovectores | `determinante-rango-invertibilidad`, `transformaciones-lineales` | — |
| 27 | `descomposicion-svd` | Descomposición en valores singulares | `autovalores-y-autovectores`, `norma-y-distancias` | — |
| 28 | `variable-aleatoria` | Variable aleatoria | `probabilidad-axiomas` | `notacion-matematica` (f00) |
| 29 | `valor-esperado` | Valor esperado | `probabilidad-axiomas`, `variable-aleatoria` | — |
| 30 | `varianza-y-desviacion` | Varianza y desviación típica | `medidas-de-dispersion`, `valor-esperado` | — |
| 31 | `covarianza-y-correlacion` | Covarianza y correlación | `valor-esperado`, `varianza-y-desviacion` | — |
| 32 | `correlacion-pearson-spearman` | Correlación de Pearson y Spearman | `covarianza-y-correlacion`, `medidas-de-dispersion` | — |
| 33 | `distribuciones-discretas` | Distribuciones discretas | `valor-esperado`, `variable-aleatoria`, `varianza-y-desviacion` | — |
| 34 | `distribuciones-continuas` | Distribuciones continuas | `distribuciones-discretas`, `integrales`, `variable-aleatoria` | — |
| 35 | `distribucion-normal-multivariante` | Distribución normal multivariante | `covarianza-y-correlacion`, `distribuciones-continuas`, `operaciones-matriciales`, `variable-aleatoria` | — |
| 36 | `entropia-e-informacion` | Entropía e información | `distribuciones-discretas`, `valor-esperado` | `maxima-verosimilitud` (f02) |
| 37 | `expansion-karhunen-loeve` | Expansión de Karhunen-Loève | `autovalores-y-autovectores`, `covarianza-y-correlacion` | — |
| 38 | `ley-de-los-grandes-numeros` | Ley de los grandes números | `distribuciones-discretas`, `valor-esperado`, `varianza-y-desviacion` | — |
| 39 | `momentos-y-cumulantes` | Momentos y cumulantes | `asimetria-y-curtosis`, `valor-esperado`, `varianza-y-desviacion` | — |
| 40 | `teorema-central-del-limite` | Teorema central del límite | `distribuciones-continuas`, `ley-de-los-grandes-numeros`, `varianza-y-desviacion` | — |
| 41 | `z-score-y-estandarizacion` | Z-score y estandarización | `medidas-de-centralidad`, `medidas-de-dispersion` | — |

## f02 — Inferencia y estadística (26 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `poblacion-y-muestra`.

**Prerequisitos externos:** 20 conceptos dependen de 11 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `poblacion-y-muestra` | Población y muestra | — | `medidas-de-centralidad` (f01), `variable-aleatoria` (f01) |
| 2 | `causalidad-vs-correlacion` | Causalidad frente a correlación | `poblacion-y-muestra` | `correlacion-pearson-spearman` (f01), `valor-esperado` (f01) |
| 3 | `confusores-y-dag` | Confusores, mediadores y DAG | `causalidad-vs-correlacion` | `correlacion-pearson-spearman` (f01) |
| 4 | `datos-agrupados-y-errores-tipicos` | Datos agrupados y errores típicos | `poblacion-y-muestra` | `medidas-de-centralidad` (f01), `medidas-de-dispersion` (f01), `varianza-y-desviacion` (f01) |
| 5 | `intervalos-de-confianza` | Intervalos de confianza | `poblacion-y-muestra` | `distribuciones-continuas` (f01), `teorema-central-del-limite` (f01) |
| 6 | `contraste-de-hipotesis` | Contraste de hipótesis | `intervalos-de-confianza`, `poblacion-y-muestra` | `distribuciones-continuas` (f01) |
| 7 | `missing-data` | Datos ausentes | `poblacion-y-muestra` | `medidas-de-centralidad` (f01), `probabilidad-condicional` (f01) |
| 8 | `p-valor` | El p-valor | `contraste-de-hipotesis` | `distribuciones-continuas` (f01), `probabilidad-condicional` (f01) |
| 9 | `errores-tipo-i-ii-y-potencia` | Errores tipo I y II, potencia | `contraste-de-hipotesis`, `p-valor` | `distribuciones-continuas` (f01) |
| 10 | `sesgo-varianza-mse` | Sesgo, varianza y ECM | `poblacion-y-muestra` | `valor-esperado` (f01) |
| 11 | `estimadores-y-propiedades` | Estimadores y sus propiedades | `poblacion-y-muestra`, `sesgo-varianza-mse` | `valor-esperado` (f01) |
| 12 | `bootstrap` | Bootstrap y remuestreo | `estimadores-y-propiedades`, `intervalos-de-confianza` | `medidas-de-dispersion` (f01) |
| 13 | `inferencia-causal-metodos` | Métodos de inferencia causal | `causalidad-vs-correlacion`, `confusores-y-dag`, `estimadores-y-propiedades` | — |
| 14 | `maxima-verosimilitud` | Máxima verosimilitud (MLE) | `estimadores-y-propiedades` | `distribuciones-continuas` (f01), `probabilidad-condicional` (f01) |
| 15 | `estimacion-bayesiana-map` | Estimación bayesiana y MAP | `maxima-verosimilitud` | `distribuciones-continuas` (f01), `teorema-de-bayes` (f01) |
| 16 | `remuestreo-y-permutacion` | Tests de permutación | `bootstrap`, `contraste-de-hipotesis`, `p-valor` | `distribuciones-continuas` (f01) |
| 17 | `tamano-del-efecto` | Tamaño del efecto | `contraste-de-hipotesis`, `p-valor` | `medidas-de-dispersion` (f01) |
| 18 | `multiplicidad-y-fdr` | Multiplicidad y FDR | `contraste-de-hipotesis`, `errores-tipo-i-ii-y-potencia`, `p-valor`, `tamano-del-efecto` | — |
| 19 | `test-t` | Test t | `contraste-de-hipotesis`, `p-valor`, `tamano-del-efecto` | `distribuciones-continuas` (f01) |
| 20 | `anova` | ANOVA | `contraste-de-hipotesis`, `test-t` | `distribuciones-continuas` (f01), `varianza-y-desviacion` (f01) |
| 21 | `chi-cuadrado` | Test chi-cuadrado | `contraste-de-hipotesis`, `p-valor`, `test-t` | `distribuciones-discretas` (f01) |
| 22 | `disenos-factoriales-e-interacciones` | Diseños factoriales e interacciones | `anova`, `contraste-de-hipotesis`, `errores-tipo-i-ii-y-potencia`, `test-t` | — |
| 23 | `tamano-muestral` | Cálculo de tamaño muestral | `errores-tipo-i-ii-y-potencia`, `intervalos-de-confianza`, `tamano-del-efecto`, `test-t` | — |
| 24 | `ab-testing` | Tests A/B | `contraste-de-hipotesis`, `errores-tipo-i-ii-y-potencia`, `p-valor`, `tamano-muestral`, `test-t` | — |
| 25 | `pruebas-de-equivalencia-y-no-inferioridad` | Pruebas de equivalencia y no inferioridad | `contraste-de-hipotesis`, `errores-tipo-i-ii-y-potencia`, `intervalos-de-confianza`, `tamano-muestral`, `test-t` | — |
| 26 | `tests-no-parametricos` | Tests no paramétricos | `anova`, `contraste-de-hipotesis`, `test-t` | `medidas-de-centralidad` (f01) |

## f03 — Python, SQL y herramientas (42 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `entorno-python`.

**Prerequisitos externos:** 2 conceptos dependen de 4 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `entorno-python` | Entorno de Python | — | — |
| 2 | `tipos-y-estructuras-python` | Tipos y estructuras de Python | `entorno-python` | — |
| 3 | `ficheros-y-encoding` | Ficheros y codificaciones | `entorno-python`, `tipos-y-estructuras-python` | — |
| 4 | `apis-y-peticiones-http` | APIs y peticiones HTTP | `ficheros-y-encoding`, `tipos-y-estructuras-python` | — |
| 5 | `fechas-y-horas` | Fechas, horas y zonas horarias | `ficheros-y-encoding`, `tipos-y-estructuras-python` | — |
| 6 | `funciones-y-modulos` | Funciones, módulos y paquetes | `entorno-python`, `tipos-y-estructuras-python` | — |
| 7 | `comprensiones-y-generadores` | Comprensiones y generadores | `funciones-y-modulos`, `tipos-y-estructuras-python` | — |
| 8 | `errores-y-depuracion` | Errores y depuración | `entorno-python`, `funciones-y-modulos` | — |
| 9 | `gestores-de-contexto` | Gestores de contexto y liberación de recursos | `errores-y-depuracion`, `funciones-y-modulos` | — |
| 10 | `git-para-datos` | Git para datos | `entorno-python`, `ficheros-y-encoding` | — |
| 11 | `json-y-datos-anidados` | JSON y datos anidados | `ficheros-y-encoding`, `tipos-y-estructuras-python` | — |
| 12 | `notebooks-vs-scripts` | Notebooks frente a scripts | `entorno-python`, `tipos-y-estructuras-python` | — |
| 13 | `numpy-fundamentos` | NumPy: fundamentos | `entorno-python`, `tipos-y-estructuras-python` | — |
| 14 | `numpy-broadcasting` | Broadcasting de NumPy | `numpy-fundamentos` | `escalares-vectores-matrices` (f01) |
| 15 | `pandas-fundamentos` | Pandas: fundamentos | `numpy-fundamentos`, `tipos-y-estructuras-python` | — |
| 16 | `arrow-y-formatos-columnares` | Arrow y formatos columnares | `numpy-fundamentos`, `pandas-fundamentos` | — |
| 17 | `datos-que-no-caben-en-memoria` | Datos que no caben en memoria | `arrow-y-formatos-columnares`, `ficheros-y-encoding`, `pandas-fundamentos` | — |
| 18 | `regex-y-limpieza-de-texto` | Expresiones regulares | `ficheros-y-encoding`, `tipos-y-estructuras-python` | — |
| 19 | `scraping-etico` | Web scraping responsable | `apis-y-peticiones-http`, `regex-y-limpieza-de-texto` | — |
| 20 | `scripts-ejecutables-y-argumentos` | Scripts ejecutables y argumentos | `entorno-python`, `funciones-y-modulos` | — |
| 21 | `sql-select-y-filtros` | SQL: consultas y filtros | `ficheros-y-encoding`, `tipos-y-estructuras-python` | — |
| 22 | `sql-agregaciones-y-group-by` | SQL: agregaciones y GROUP BY | `sql-select-y-filtros` | — |
| 23 | `calidad-de-datos` | Calidad de datos | `pandas-fundamentos`, `sql-agregaciones-y-group-by` | — |
| 24 | `perfilado-de-datos` | Perfilado y EDA automático | `calidad-de-datos`, `pandas-fundamentos` | — |
| 25 | `sql-joins` | SQL: uniones | `sql-select-y-filtros` | — |
| 26 | `pandas-agrupaciones-y-joins` | Pandas: agrupaciones y uniones | `pandas-fundamentos`, `sql-agregaciones-y-group-by`, `sql-joins` | — |
| 27 | `polars` | Polars | `pandas-agrupaciones-y-joins`, `pandas-fundamentos` | — |
| 28 | `reformar-tablas-ancho-y-largo` | Reformar tablas: ancho y largo | `pandas-agrupaciones-y-joins`, `pandas-fundamentos` | — |
| 29 | `series-temporales-en-pandas` | Series temporales en Pandas | `fechas-y-horas`, `pandas-agrupaciones-y-joins`, `pandas-fundamentos` | — |
| 30 | `sql-indices-y-planes` | SQL: índices y planes | `sql-joins`, `sql-select-y-filtros` | — |
| 31 | `sql-modelado-y-normalizacion` | SQL: modelado y normalización | `sql-agregaciones-y-group-by`, `sql-joins` | — |
| 32 | `sql-subconsultas-y-cte` | SQL: subconsultas y CTE | `sql-agregaciones-y-group-by`, `sql-select-y-filtros` | — |
| 33 | `sql-ventanas` | SQL: funciones de ventana | `sql-agregaciones-y-group-by`, `sql-subconsultas-y-cte` | — |
| 34 | `terminal-y-shell` | Terminal y shell | `entorno-python`, `ficheros-y-encoding` | — |
| 35 | `testing-con-pytest` | Tests con pytest | `entorno-python`, `pandas-fundamentos`, `tipos-y-estructuras-python` | — |
| 36 | `tipado-y-linters` | Tipado y linters | `entorno-python`, `testing-con-pytest`, `tipos-y-estructuras-python` | — |
| 37 | `transacciones-y-bloqueos` | Transacciones, aislamiento y bloqueos | `sql-modelado-y-normalizacion`, `sql-select-y-filtros` | — |
| 38 | `vectorizacion` | Vectorización | `numpy-broadcasting`, `numpy-fundamentos` | — |
| 39 | `vistas-y-copias` | Vistas, copias y aliasing | `numpy-fundamentos`, `tipos-y-estructuras-python` | — |
| 40 | `clases-y-objetos` | Clases y objetos | `tipos-y-estructuras-python`, `vistas-y-copias` | — |
| 41 | `visualizacion-matplotlib` | Visualización con Matplotlib | `numpy-fundamentos`, `pandas-fundamentos` | — |
| 42 | `visualizacion-estadistica` | Visualización estadística | `visualizacion-matplotlib` | `cuantiles-y-percentiles` (f01), `medidas-de-centralidad` (f01), `medidas-de-dispersion` (f01) |

## f04 — Ingeniería de datos (61 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `ciclo-de-vida-del-dato`, `compresion-y-codificacion`, `feature-store`, `mlops-y-cicd-de-modelos`, `normalizacion-vs-desnormalizacion`, `parquet-avro-orc`.

**Prerequisitos externos:** 33 conceptos dependen de 22 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `ciclo-de-vida-del-dato` | Ciclo de vida del dato | — | `calidad-de-datos` (f03), `ficheros-y-encoding` (f03) |
| 2 | `almacenamiento-de-objetos` | Almacenamiento de objetos | `ciclo-de-vida-del-dato` | `ficheros-y-encoding` (f03) |
| 3 | `compresion-y-codificacion` | Compresión y codificación | — | `arrow-y-formatos-columnares` (f03), `ficheros-y-encoding` (f03) |
| 4 | `data-lake` | Data lake | `ciclo-de-vida-del-dato` | `ficheros-y-encoding` (f03) |
| 5 | `docker-para-datos` | Docker para datos | `ciclo-de-vida-del-dato` | `entorno-python` (f03) |
| 6 | `feature-store` | Feature store | — | `fuga-de-datos` (f05), `ingenieria-de-features` (f05), `pipelines-de-ml` (f06) |
| 7 | `mlops-y-cicd-de-modelos` | MLOps y CI/CD de modelos | — | `pipelines-de-ml` (f06), `train-val-test` (f06) |
| 8 | `normalizacion-vs-desnormalizacion` | Normalización frente a desnormalización | — | `sql-joins` (f03), `sql-modelado-y-normalizacion` (f03) |
| 9 | `oltp-vs-olap` | OLTP frente a OLAP | `ciclo-de-vida-del-dato` | `sql-modelado-y-normalizacion` (f03), `sql-select-y-filtros` (f03) |
| 10 | `etl-vs-elt` | ETL frente a ELT | `ciclo-de-vida-del-dato`, `oltp-vs-olap` | — |
| 11 | `batch-vs-streaming` | Procesamiento por lotes y en flujo | `ciclo-de-vida-del-dato`, `etl-vs-elt` | — |
| 12 | `dbt-y-transformacion` | dbt y transformación | `etl-vs-elt` | `sql-joins` (f03), `sql-select-y-filtros` (f03), `sql-subconsultas-y-cte` (f03) |
| 13 | `ingesta-incremental-y-cdc` | Ingesta incremental y CDC | `batch-vs-streaming`, `etl-vs-elt`, `oltp-vs-olap` | `sql-ventanas` (f03) |
| 14 | `datos-de-mercado-y-acciones-corporativas` | Datos de mercado y acciones corporativas | `ingesta-incremental-y-cdc` | `fechas-y-horas` (f03), `pandas-fundamentos` (f03) |
| 15 | `kafka-y-colas` | Kafka y colas de mensajes | `batch-vs-streaming`, `ingesta-incremental-y-cdc` | — |
| 16 | `lambda-y-kappa` | Arquitecturas lambda y kappa | `batch-vs-streaming`, `data-lake`, `kafka-y-colas` | — |
| 17 | `modelado-dimensional` | Modelado dimensional | `oltp-vs-olap` | `sql-joins` (f03), `sql-modelado-y-normalizacion` (f03) |
| 18 | `bi-y-consumo` | BI y capa de consumo | `modelado-dimensional`, `oltp-vs-olap` | — |
| 19 | `data-warehouse` | Data warehouse | `etl-vs-elt`, `modelado-dimensional`, `oltp-vs-olap` | — |
| 20 | `arquitectura-medallion` | Arquitectura medallion | `data-lake`, `data-warehouse`, `etl-vs-elt` | — |
| 21 | `catalogo-y-linaje` | Catálogo y linaje | `data-warehouse` | — |
| 22 | `capa-semantica-y-metricas` | Capa semántica y métricas | `arquitectura-medallion`, `catalogo-y-linaje`, `dbt-y-transformacion` | — |
| 23 | `esquema-estrella-y-copo` | Esquema en estrella y copo de nieve | `modelado-dimensional`, `normalizacion-vs-desnormalizacion` | `sql-joins` (f03) |
| 24 | `gobierno-y-privacidad` | Gobierno y privacidad del dato | `catalogo-y-linaje`, `ciclo-de-vida-del-dato` | `calidad-de-datos` (f03) |
| 25 | `control-de-acceso-por-fila-y-columna` | Control de acceso por fila y por columna | `gobierno-y-privacidad` | `sql-select-y-filtros` (f03) |
| 26 | `data-mesh` | Data mesh | `catalogo-y-linaje`, `data-lake`, `gobierno-y-privacidad` | — |
| 27 | `enmascarado-y-retencion` | Enmascarado y retención | `gobierno-y-privacidad` | `privacidad-y-gdpr` (f11) |
| 28 | `hechos-y-dimensiones` | Tablas de hechos y dimensiones | `esquema-estrella-y-copo`, `modelado-dimensional` | `sql-agregaciones-y-group-by` (f03) |
| 29 | `orquestacion-y-dag` | Orquestación y DAG | `batch-vs-streaming`, `etl-vs-elt` | — |
| 30 | `airflow-dagster-prefect` | Airflow, Dagster y Prefect | `etl-vs-elt`, `orquestacion-y-dag` | — |
| 31 | `calidad-y-slas` | Calidad y acuerdos de nivel de servicio | `orquestacion-y-dag` | `calidad-de-datos` (f03) |
| 32 | `contratos-de-datos` | Contratos de datos | `calidad-y-slas` | `calidad-de-datos` (f03) |
| 33 | `idempotencia-y-reintentos` | Idempotencia y reintentos | `orquestacion-y-dag` | `apis-y-peticiones-http` (f03) |
| 34 | `eventos-push-y-webhooks` | Eventos push y webhooks | `idempotencia-y-reintentos` | `apis-rest` (f11) |
| 35 | `kubernetes-basico` | Kubernetes básico | `docker-para-datos`, `orquestacion-y-dag` | — |
| 36 | `iac-y-terraform` | Infraestructura como código | `docker-para-datos`, `kubernetes-basico` | `git-para-datos` (f03) |
| 37 | `observabilidad-de-datos` | Observabilidad de datos | `calidad-y-slas`, `contratos-de-datos` | — |
| 38 | `monitorizacion-de-drift` | Deriva de datos y de concepto | `mlops-y-cicd-de-modelos`, `observabilidad-de-datos` | `calidad-de-datos` (f03) |
| 39 | `parquet-avro-orc` | Parquet, Avro y ORC | — | `arrow-y-formatos-columnares` (f03), `ficheros-y-encoding` (f03) |
| 40 | `duckdb-y-analitica-local` | DuckDB y analítica local | `parquet-avro-orc` | `pandas-fundamentos` (f03), `sql-agregaciones-y-group-by` (f03) |
| 41 | `evolucion-de-esquema` | Evolución de esquema | `almacenamiento-de-objetos`, `data-lake`, `parquet-avro-orc` | — |
| 42 | `data-vault` | Modelado Data Vault | `evolucion-de-esquema`, `hechos-y-dimensiones`, `modelado-dimensional` | — |
| 43 | `particionado-y-clustering` | Particionado y clustering | `data-lake`, `parquet-avro-orc` | — |
| 44 | `backfill-y-reproceso` | Backfill y reproceso | `idempotencia-y-reintentos`, `orquestacion-y-dag`, `particionado-y-clustering` | — |
| 45 | `coste-y-optimizacion` | Coste y optimización | `compresion-y-codificacion`, `parquet-avro-orc`, `particionado-y-clustering` | — |
| 46 | `lakehouse-y-table-formats` | Lakehouse y formatos de tabla | `data-lake`, `parquet-avro-orc`, `particionado-y-clustering` | — |
| 47 | `nubes-y-servicios-gestionados` | Nubes y servicios gestionados | `almacenamiento-de-objetos`, `coste-y-optimizacion`, `data-warehouse` | — |
| 48 | `iam-y-permisos-cloud` | Identidad y permisos en la nube | `nubes-y-servicios-gestionados` | `autenticacion-y-autorizacion` (f11) |
| 49 | `problema-de-ficheros-pequenos` | El problema de los ficheros pequeños | `parquet-avro-orc`, `particionado-y-clustering` | — |
| 50 | `reconciliacion-y-pruebas` | Reconciliación y pruebas de datos | `calidad-y-slas`, `dbt-y-transformacion` | `sql-agregaciones-y-group-by` (f03) |
| 51 | `registro-de-esquemas` | Registro de esquemas | `evolucion-de-esquema`, `kafka-y-colas` | — |
| 52 | `registros-rechazados-y-cuarentena` | Registros rechazados, cuarentena y parada del pipeline | `contratos-de-datos` | `calidad-de-datos` (f03) |
| 53 | `reverse-etl` | Reverse ETL | `contratos-de-datos`, `data-warehouse`, `idempotencia-y-reintentos` | — |
| 54 | `scd-dimensiones-cambiantes` | Dimensiones que cambian (SCD) | `hechos-y-dimensiones`, `modelado-dimensional` | `sql-joins` (f03) |
| 55 | `correccion-point-in-time` | Corrección point-in-time | `datos-de-mercado-y-acciones-corporativas`, `scd-dimensiones-cambiantes` | `sesgo-de-mirar-al-futuro` (f09) |
| 56 | `spark-fundamentos` | Spark: fundamentos | `data-lake`, `parquet-avro-orc` | `pandas-fundamentos` (f03) |
| 57 | `spark-particiones-y-shuffle` | Spark: particiones y shuffle | `parquet-avro-orc`, `particionado-y-clustering`, `spark-fundamentos` | — |
| 58 | `spark-joins-y-skew` | Spark: uniones y asimetría | `spark-fundamentos`, `spark-particiones-y-shuffle` | `sql-joins` (f03) |
| 59 | `streaming-tiempo-real` | Streaming: ventanas y marcas de agua | `batch-vs-streaming`, `ingesta-incremental-y-cdc`, `kafka-y-colas` | — |
| 60 | `ventanas-y-watermarks` | Ventanas y marcas de agua | `ingesta-incremental-y-cdc`, `kafka-y-colas`, `streaming-tiempo-real` | — |
| 61 | `flink-y-procesamiento-de-eventos` | Flink y procesamiento de eventos | `streaming-tiempo-real`, `ventanas-y-watermarks` | — |

## f05 — Exploración y series temporales (29 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `analisis-de-supervivencia`, `desbalanceo-de-clases`, `distribuciones-en-datos-reales`, `eda-pasos`, `fuga-de-datos`, `imputacion-de-datos`, `outliers-y-deteccion`, `seleccion-de-features`, `series-temporales-componentes`.

**Prerequisitos externos:** 21 conceptos dependen de 26 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `analisis-de-supervivencia` | Análisis de supervivencia | — | `distribuciones-continuas` (f01), `maxima-verosimilitud` (f02), `variable-aleatoria` (f01) |
| 2 | `desbalanceo-de-clases` | Desbalanceo de clases | — | `matriz-de-confusion` (f06), `metricas-de-clasificacion` (f06), `precision-recall-y-pr` (f06) |
| 3 | `distribuciones-en-datos-reales` | Distribuciones en datos reales | — | `asimetria-y-curtosis` (f01), `distribuciones-continuas` (f01), `medidas-de-dispersion` (f01) |
| 4 | `eda-pasos` | Análisis exploratorio: el método | — | `calidad-de-datos` (f03), `pandas-fundamentos` (f03), `perfilado-de-datos` (f03) |
| 5 | `encoding-de-categoricas` | Codificación de categóricas | `eda-pasos` | `pandas-fundamentos` (f03) |
| 6 | `escalado-y-transformacion` | Escalado y transformación | `distribuciones-en-datos-reales` | `medidas-de-dispersion` (f01), `z-score-y-estandarizacion` (f01) |
| 7 | `fuga-de-datos` | Fuga de datos (data leakage) | — | `train-val-test` (f06), `validacion-cruzada` (f06) |
| 8 | `imputacion-de-datos` | Imputación de datos | — | `missing-data` (f02), `pandas-fundamentos` (f03) |
| 9 | `outliers-y-deteccion` | Valores atípicos | — | `cuantiles-y-percentiles` (f01), `medidas-de-dispersion` (f01), `z-score-y-estandarizacion` (f01) |
| 10 | `seleccion-de-features` | Selección de variables | — | `correlacion-pearson-spearman` (f01), `validacion-cruzada` (f06) |
| 11 | `series-temporales-componentes` | Componentes de una serie temporal | — | `medidas-de-centralidad` (f01), `notacion-matematica` (f00) |
| 12 | `estacionariedad` | Estacionariedad | `series-temporales-componentes` | `varianza-y-desviacion` (f01) |
| 13 | `anomalias-en-series-temporales` | Anomalías en series temporales | `estacionariedad`, `outliers-y-deteccion`, `series-temporales-componentes` | — |
| 14 | `autocorrelacion-acf-pacf` | Autocorrelación, ACF y PACF | `estacionariedad` | `covarianza-y-correlacion` (f01) |
| 15 | `descomposicion-stl` | Descomposición STL | `estacionariedad`, `series-temporales-componentes` | — |
| 16 | `frecuencia-y-agregacion-temporal` | Frecuencia, granularidad y agregación | `series-temporales-componentes` | `fechas-y-horas` (f03), `pandas-agrupaciones-y-joins` (f03) |
| 17 | `garch-volatilidad` | GARCH y volatilidad | `autocorrelacion-acf-pacf`, `estacionariedad` | `varianza-y-desviacion` (f01) |
| 18 | `hmm-regimenes` | Cadenas de Markov ocultas | `estacionariedad`, `garch-volatilidad` | `maxima-verosimilitud` (f02) |
| 19 | `ingenieria-de-features` | Ingeniería de variables | `series-temporales-componentes` | `pandas-agrupaciones-y-joins` (f03), `pandas-fundamentos` (f03) |
| 20 | `pronosticos-de-referencia-y-mase` | Pronósticos de referencia y MASE | `series-temporales-componentes` | `metricas-de-regresion` (f06) |
| 21 | `suavizado-exponencial` | Suavizado exponencial | `estacionariedad`, `series-temporales-componentes` | — |
| 22 | `prophet-y-modelos-modernos` | Prophet y modelos modernos | `series-temporales-componentes`, `suavizado-exponencial` | — |
| 23 | `test-adf-kpss` | Tests de raíz unitaria: ADF y KPSS | `autocorrelacion-acf-pacf`, `estacionariedad` | `contraste-de-hipotesis` (f02) |
| 24 | `arima-sarima` | ARIMA y SARIMA | `autocorrelacion-acf-pacf`, `estacionariedad`, `test-adf-kpss` | — |
| 25 | `diagnostico-de-residuos` | Diagnóstico de residuos | `arima-sarima`, `autocorrelacion-acf-pacf` | `supuestos-de-la-regresion` (f06) |
| 26 | `validacion-temporal` | Validación temporal | `autocorrelacion-acf-pacf`, `estacionariedad`, `fuga-de-datos` | — |
| 27 | `prediccion-con-incertidumbre` | Predicción con incertidumbre | `series-temporales-componentes`, `validacion-temporal` | `metricas-de-regresion` (f06) |
| 28 | `prevision-a-varios-pasos` | Previsión a varios pasos | `autocorrelacion-acf-pacf`, `series-temporales-componentes`, `validacion-temporal` | — |
| 29 | `series-jerarquicas` | Series jerárquicas y reconciliación | `series-temporales-componentes`, `suavizado-exponencial`, `validacion-temporal` | — |

## f06 — Machine learning clásico (49 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `bandits-y-decision-secuencial`, `datos-geoespaciales`, `k-means`, `metricas-de-regresion`, `naive-bayes`, `paradigmas-de-aprendizaje`, `pca`, `reglas-de-asociacion`, `regresion-lineal`, `svm`, `train-val-test`.

**Prerequisitos externos:** 28 conceptos dependen de 33 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `bandits-y-decision-secuencial` | Bandits y decisión secuencial | — | `ab-testing` (f02), `teorema-de-bayes` (f01), `valor-esperado` (f01) |
| 2 | `datos-geoespaciales` | Datos geoespaciales | — | `norma-y-distancias` (f01), `pandas-agrupaciones-y-joins` (f03), `sql-joins` (f03) |
| 3 | `k-means` | K-means | — | `escalado-y-transformacion` (f05), `medidas-de-centralidad` (f01), `norma-y-distancias` (f01) |
| 4 | `clustering-jerarquico` | Clustering jerárquico | `k-means` | `correlacion-pearson-spearman` (f01), `norma-y-distancias` (f01) |
| 5 | `dbscan-y-hdbscan` | DBSCAN y HDBSCAN | `clustering-jerarquico`, `k-means` | `escalado-y-transformacion` (f05), `norma-y-distancias` (f01) |
| 6 | `gmm` | Mezclas gaussianas | `k-means` | `distribuciones-continuas` (f01), `maxima-verosimilitud` (f02) |
| 7 | `metricas-de-clustering` | Métricas de clustering | `clustering-jerarquico`, `dbscan-y-hdbscan`, `k-means` | — |
| 8 | `metricas-de-regresion` | Métricas de regresión | — | `medidas-de-centralidad` (f01), `medidas-de-dispersion` (f01) |
| 9 | `naive-bayes` | Naive Bayes | — | `independencia-y-condicionamiento` (f01), `maxima-verosimilitud` (f02), `teorema-de-bayes` (f01) |
| 10 | `paradigmas-de-aprendizaje` | Paradigmas de aprendizaje | — | — |
| 11 | `pca` | Análisis de componentes principales | — | `autovalores-y-autovectores` (f01), `covarianza-y-correlacion` (f01), `escalado-y-transformacion` (f05) |
| 12 | `procesamiento-de-texto-clasico` | Procesamiento de texto clásico | `naive-bayes` | `regex-y-limpieza-de-texto` (f03) |
| 13 | `reglas-de-asociacion` | Reglas de asociación | — | `probabilidad-condicional` (f01), `sql-agregaciones-y-group-by` (f03) |
| 14 | `regresion-lineal` | Regresión lineal | — | `covarianza-y-correlacion` (f01), `medidas-de-centralidad` (f01), `notacion-matematica` (f00) |
| 15 | `glm-y-logistica` | Modelos lineales generalizados y regresión logística | `regresion-lineal` | `maxima-verosimilitud` (f02), `probabilidad-condicional` (f01) |
| 16 | `sesgo-varianza` | Compromiso sesgo-varianza | `metricas-de-regresion` | `sesgo-varianza-mse` (f02) |
| 17 | `regularizacion-l1-l2` | Regularización L1 y L2 | `regresion-lineal`, `sesgo-varianza` | `escalado-y-transformacion` (f05) |
| 18 | `supuestos-de-la-regresion` | Supuestos de la regresión | `regresion-lineal` | `contraste-de-hipotesis` (f02), `varianza-y-desviacion` (f01) |
| 19 | `svm` | Máquinas de vectores de soporte | — | `escalado-y-transformacion` (f05), `norma-y-distancias` (f01), `optimizacion-con-restricciones` (f01), `producto-punto-y-similitud` (f01) |
| 20 | `train-val-test` | Conjuntos de entrenamiento, validación y prueba | — | — |
| 21 | `knn` | K vecinos más cercanos | `train-val-test` | `escalado-y-transformacion` (f05), `norma-y-distancias` (f01) |
| 22 | `maldicion-de-la-dimensionalidad` | Maldición de la dimensionalidad | `knn` | `norma-y-distancias` (f01) |
| 23 | `matriz-de-confusion` | Matriz de confusión | `train-val-test` | — |
| 24 | `metricas-de-clasificacion` | Métricas de clasificación | `matriz-de-confusion`, `train-val-test` | — |
| 25 | `aprendizaje-semi-supervisado` | Aprendizaje semisupervisado | `clustering-jerarquico`, `metricas-de-clasificacion`, `paradigmas-de-aprendizaje`, `train-val-test` | — |
| 26 | `arboles-de-decision` | Árboles de decisión | `metricas-de-clasificacion`, `paradigmas-de-aprendizaje` | — |
| 27 | `bagging-y-random-forest` | Bagging y Random Forest | `arboles-de-decision`, `sesgo-varianza` | `bootstrap` (f02) |
| 28 | `calibracion` | Calibración de probabilidades | `glm-y-logistica`, `metricas-de-clasificacion` | — |
| 29 | `aprendizaje-activo` | Aprendizaje activo | `calibracion`, `metricas-de-clasificacion`, `paradigmas-de-aprendizaje`, `train-val-test` | — |
| 30 | `etiquetas-y-techo-del-modelo` | Calidad de las etiquetas y techo del modelo | `metricas-de-clasificacion`, `sesgo-varianza`, `train-val-test` | — |
| 31 | `gradient-boosting` | Gradient boosting | `arboles-de-decision`, `sesgo-varianza` | `derivadas-parciales-y-gradiente` (f01) |
| 32 | `precision-recall-y-pr` | Curva precisión-exhaustividad | `matriz-de-confusion`, `metricas-de-clasificacion` | — |
| 33 | `deteccion-de-anomalias` | Detección de anomalías | `precision-recall-y-pr` | `distribuciones-en-datos-reales` (f05), `outliers-y-deteccion` (f05) |
| 34 | `roc-auc` | Curva ROC y AUC | `matriz-de-confusion`, `metricas-de-clasificacion` | — |
| 35 | `metricas-de-ranking` | Métricas de ranking | `metricas-de-clasificacion`, `roc-auc` | — |
| 36 | `recomendadores` | Sistemas de recomendación | `metricas-de-ranking` | `descomposicion-svd` (f01), `producto-punto-y-similitud` (f01) |
| 37 | `tsne-y-umap` | t-SNE y UMAP | `maldicion-de-la-dimensionalidad`, `pca` | `entropia-e-informacion` (f01) |
| 38 | `umbrales-y-coste` | Umbrales y coste del error | `matriz-de-confusion`, `metricas-de-clasificacion`, `roc-auc` | — |
| 39 | `fairness-y-equidad` | Equidad y métricas de fairness | `matriz-de-confusion`, `metricas-de-clasificacion`, `umbrales-y-coste` | — |
| 40 | `uplift-y-valor-incremental` | Uplift y valor incremental | `arboles-de-decision`, `metricas-de-clasificacion`, `train-val-test` | — |
| 41 | `validacion-cruzada` | Validación cruzada | `sesgo-varianza`, `train-val-test` | `desbalanceo-de-clases` (f05) |
| 42 | `importancia-de-variables` | Importancia de variables | `arboles-de-decision`, `bagging-y-random-forest`, `validacion-cruzada` | — |
| 43 | `interpretabilidad-shap` | Interpretabilidad y SHAP | `arboles-de-decision`, `gradient-boosting`, `importancia-de-variables` | — |
| 44 | `pipelines-de-ml` | Pipelines de machine learning | `train-val-test`, `validacion-cruzada` | `escalado-y-transformacion` (f05), `fuga-de-datos` (f05) |
| 45 | `entrenamiento-frente-a-inferencia` | Coherencia entre entrenamiento e inferencia | `pipelines-de-ml`, `train-val-test` | `fuga-de-datos` (f05), `monitorizacion-de-drift` (f04) |
| 46 | `seleccion-de-hiperparametros` | Búsqueda de hiperparámetros | `regularizacion-l1-l2`, `sesgo-varianza`, `train-val-test`, `validacion-cruzada` | — |
| 47 | `automl` | AutoML | `pipelines-de-ml`, `seleccion-de-hiperparametros`, `validacion-cruzada` | `fuga-de-datos` (f05) |
| 48 | `stacking-y-blending` | Stacking y blending | `bagging-y-random-forest`, `gradient-boosting`, `metricas-de-clasificacion`, `validacion-cruzada` | — |
| 49 | `xgboost-lightgbm-catboost` | XGBoost, LightGBM y CatBoost | `arboles-de-decision`, `gradient-boosting`, `regularizacion-l1-l2`, `validacion-cruzada` | — |

## f07 — Deep learning (33 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `aprendizaje-por-refuerzo`, `embeddings`, `perceptron-y-mlp`.

**Prerequisitos externos:** 28 conceptos dependen de 27 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `aprendizaje-por-refuerzo` | Aprendizaje por refuerzo | — | `paradigmas-de-aprendizaje` (f06), `probabilidad-condicional` (f01), `valor-esperado` (f01) |
| 2 | `embeddings` | Embeddings | — | `encoding-de-categoricas` (f05), `norma-y-distancias` (f01), `pca` (f06), `producto-punto-y-similitud` (f01) |
| 3 | `perceptron-y-mlp` | Perceptrón y perceptrón multicapa | — | `glm-y-logistica` (f06), `producto-punto-y-similitud` (f01), `regresion-lineal` (f06) |
| 4 | `funciones-de-activacion` | Funciones de activación | `perceptron-y-mlp` | `derivadas-y-reglas` (f01), `regla-de-la-cadena` (f01) |
| 5 | `cnn` | Redes convolucionales | `funciones-de-activacion`, `perceptron-y-mlp` | `operaciones-matriciales` (f01) |
| 6 | `funciones-de-perdida` | Funciones de pérdida | `perceptron-y-mlp` | `entropia-e-informacion` (f01), `maxima-verosimilitud` (f02) |
| 7 | `retropropagacion` | Retropropagación | `funciones-de-activacion`, `perceptron-y-mlp` | `derivadas-parciales-y-gradiente` (f01), `regla-de-la-cadena` (f01) |
| 8 | `gan` | Redes generativas adversarias | `funciones-de-perdida`, `perceptron-y-mlp`, `retropropagacion` | `entropia-e-informacion` (f01) |
| 9 | `gnn` | Redes sobre grafos | `perceptron-y-mlp`, `retropropagacion` | `operaciones-matriciales` (f01) |
| 10 | `inicializacion-de-pesos` | Inicialización de pesos | `funciones-de-activacion`, `retropropagacion` | `varianza-y-desviacion` (f01) |
| 11 | `normalizacion-por-lotes` | Normalización por lotes | `inicializacion-de-pesos`, `retropropagacion` | `escalado-y-transformacion` (f05) |
| 12 | `optimizadores` | Optimizadores | `funciones-de-perdida`, `retropropagacion` | `derivadas-parciales-y-gradiente` (f01) |
| 13 | `autoencoders-y-vae` | Autoencoders y VAE | `funciones-de-perdida`, `optimizadores`, `perceptron-y-mlp` | `deteccion-de-anomalias` (f06), `pca` (f06) |
| 14 | `grafos-computacionales-y-autograd` | Grafos computacionales y autograd | `optimizadores`, `retropropagacion` | `regla-de-la-cadena` (f01) |
| 15 | `modelos-de-difusion` | Modelos de difusión | `autoencoders-y-vae`, `funciones-de-perdida`, `optimizadores`, `retropropagacion` | — |
| 16 | `evaluacion-de-modelos-generativos` | Evaluar un modelo generativo | `gan`, `modelos-de-difusion` | `metricas-de-clasificacion` (f06) |
| 17 | `pytorch-fundamentos` | PyTorch: fundamentos | `funciones-de-perdida`, `grafos-computacionales-y-autograd`, `perceptron-y-mlp` | `numpy-fundamentos` (f03) |
| 18 | `gpu-y-rendimiento` | GPU y rendimiento | `pytorch-fundamentos`, `retropropagacion` | `operaciones-matriciales` (f01) |
| 19 | `cuantizacion-y-destilacion` | Cuantización y destilación | `funciones-de-perdida`, `gpu-y-rendimiento`, `optimizadores` | `entropia-e-informacion` (f01) |
| 20 | `exportar-y-servir-modelos` | Exportar y servir modelos | `cuantizacion-y-destilacion`, `gpu-y-rendimiento`, `pytorch-fundamentos` | — |
| 21 | `q-learning-y-policy-gradient` | Q-learning y gradiente de política | `aprendizaje-por-refuerzo`, `optimizadores` | `derivadas-parciales-y-gradiente` (f01), `valor-esperado` (f01) |
| 22 | `reproducibilidad-del-entrenamiento` | Reproducibilidad del entrenamiento | `inicializacion-de-pesos`, `pytorch-fundamentos` | — |
| 23 | `rnn-lstm-gru` | RNN, LSTM y GRU | `funciones-de-activacion`, `perceptron-y-mlp`, `retropropagacion` | `regla-de-la-cadena` (f01) |
| 24 | `atencion` | Mecanismos de atención | `embeddings`, `funciones-de-activacion`, `rnn-lstm-gru` | `producto-punto-y-similitud` (f01) |
| 25 | `seguimiento-de-experimentos` | Seguimiento de experimentos | `pytorch-fundamentos` | `seleccion-de-hiperparametros` (f06) |
| 26 | `sobreajuste-en-redes` | Sobreajuste en redes | `perceptron-y-mlp` | `sesgo-varianza` (f06), `train-val-test` (f06) |
| 27 | `dropout-y-regularizacion` | Dropout y regularización | `sobreajuste-en-redes` | `regularizacion-l1-l2` (f06), `sesgo-varianza` (f06) |
| 28 | `tasas-de-aprendizaje-y-schedulers` | Tasa de aprendizaje y planificadores | `optimizadores` | `convexidad` (f01), `derivadas-parciales-y-gradiente` (f01) |
| 29 | `depuracion-de-redes` | Depurar el entrenamiento | `funciones-de-perdida`, `retropropagacion`, `sobreajuste-en-redes`, `tasas-de-aprendizaje-y-schedulers` | — |
| 30 | `tokenizacion` | Tokenización | `embeddings` | `procesamiento-de-texto-clasico` (f06), `regex-y-limpieza-de-texto` (f03) |
| 31 | `transfer-learning` | Aprendizaje por transferencia | `funciones-de-perdida`, `perceptron-y-mlp` | `sesgo-varianza` (f06), `train-val-test` (f06) |
| 32 | `fine-tuning-y-lora` | Ajuste fino y LoRA | `optimizadores`, `tasas-de-aprendizaje-y-schedulers`, `transfer-learning` | `operaciones-matriciales` (f01) |
| 33 | `transformers` | Transformers | `atencion`, `embeddings`, `normalizacion-por-lotes`, `retropropagacion`, `tokenizacion` | — |

## f08 — LLMs e IA generativa (22 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `bases-de-datos-vectoriales`, `como-funciona-un-llm`.

**Prerequisitos externos:** 14 conceptos dependen de 16 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `bases-de-datos-vectoriales` | Bases de datos vectoriales | — | `embeddings` (f07), `knn` (f06), `maldicion-de-la-dimensionalidad` (f06), `norma-y-distancias` (f01), `producto-punto-y-similitud` (f01) |
| 2 | `como-funciona-un-llm` | Cómo funciona un LLM | — | `atencion` (f07), `tokenizacion` (f07), `transformers` (f07) |
| 3 | `preentrenamiento-y-escalado` | Preentrenamiento y escalado | `como-funciona-un-llm` | `funciones-de-perdida` (f07), `transformers` (f07) |
| 4 | `instruccion-y-alineamiento` | Instrucción y alineamiento | `preentrenamiento-y-escalado` | `fine-tuning-y-lora` (f07), `funciones-de-perdida` (f07) |
| 5 | `prompting` | Ingeniería de prompts | `como-funciona-un-llm` | `tokenizacion` (f07) |
| 6 | `evaluacion-de-llms` | Evaluación de LLMs | `prompting` | `contraste-de-hipotesis` (f02), `metricas-de-clasificacion` (f06), `metricas-de-ranking` (f06), `train-val-test` (f06) |
| 7 | `structured-output` | Salida estructurada | `como-funciona-un-llm`, `prompting` | `tipos-y-estructuras-python` (f03) |
| 8 | `ventanas-de-contexto` | Ventana de contexto | `como-funciona-un-llm`, `prompting` | `tokenizacion` (f07) |
| 9 | `coste-y-latencia` | Coste y latencia | `como-funciona-un-llm`, `ventanas-de-contexto` | `tokenizacion` (f07) |
| 10 | `economia-de-la-inferencia-propia` | Economía de la inferencia propia | `como-funciona-un-llm`, `coste-y-latencia` | `cuantizacion-y-destilacion` (f07) |
| 11 | `modelos-multimodales` | Modelos multimodales | `como-funciona-un-llm`, `ventanas-de-contexto` | `embeddings` (f07) |
| 12 | `motores-de-inferencia-para-llms` | Servir un LLM en abierto: motores y cuantización | `como-funciona-un-llm`, `coste-y-latencia`, `economia-de-la-inferencia-propia` | — |
| 13 | `observabilidad-de-llms` | Observabilidad de una aplicación con LLM | `coste-y-latencia`, `evaluacion-de-llms`, `structured-output` | — |
| 14 | `privacidad-y-datos-en-llms` | Privacidad de datos en LLMs | `bases-de-datos-vectoriales`, `coste-y-latencia` | — |
| 15 | `rag-arquitectura` | RAG: arquitectura | `como-funciona-un-llm`, `ventanas-de-contexto` | — |
| 16 | `agentes-y-herramientas` | Agentes y uso de herramientas | `como-funciona-un-llm`, `prompting`, `rag-arquitectura`, `structured-output` | — |
| 17 | `alucinaciones-y-limites` | Alucinaciones y límites | `como-funciona-un-llm`, `prompting`, `rag-arquitectura`, `ventanas-de-contexto` | — |
| 18 | `chunking-y-embeddings` | Troceado y embeddings | `rag-arquitectura` | `embeddings` (f07), `norma-y-distancias` (f01), `producto-punto-y-similitud` (f01), `tokenizacion` (f07) |
| 19 | `fine-tuning-vs-rag` | Ajuste fino frente a RAG | `alucinaciones-y-limites`, `prompting`, `rag-arquitectura` | `fine-tuning-y-lora` (f07) |
| 20 | `mcp-y-servidores-de-herramientas` | MCP y servidores de herramientas | `agentes-y-herramientas`, `structured-output` | — |
| 21 | `reranking` | Reordenación | `bases-de-datos-vectoriales`, `chunking-y-embeddings`, `rag-arquitectura` | `embeddings` (f07), `metricas-de-ranking` (f06) |
| 22 | `seguridad-y-prompt-injection` | Seguridad e inyección de prompts | `agentes-y-herramientas`, `como-funciona-un-llm`, `prompting` | — |

## f09 — Finanzas cuantitativas (61 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `alpha-y-beta`, `cointegracion`, `data-snooping-y-multiple-testing`, `generacion-de-senales`, `hurst-y-memoria`, `markowitz-y-frontera`, `movimiento-browniano`, `que-es-un-mercado`, `retornos-logaritmicos`, `reversion-a-la-media`, `sesgo-de-mirar-al-futuro`.

**Prerequisitos externos:** 37 conceptos dependen de 38 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `alpha-y-beta` | Alpha y beta | — | `correlacion-pearson-spearman` (f01), `regresion-lineal` (f06), `valor-esperado` (f01), `varianza-y-desviacion` (f01) |
| 2 | `cointegracion` | Cointegración | — | `autocorrelacion-acf-pacf` (f05), `estacionariedad` (f05), `regresion-lineal` (f06), `test-adf-kpss` (f05) |
| 3 | `data-snooping-y-multiple-testing` | Data snooping y pruebas múltiples | — | `contraste-de-hipotesis` (f02), `multiplicidad-y-fdr` (f02), `p-valor` (f02) |
| 4 | `factores-y-fama-french` | Factores y Fama-French | `alpha-y-beta` | `correlacion-pearson-spearman` (f01), `regresion-lineal` (f06) |
| 5 | `generacion-de-senales` | Generación de señales | — | `fuga-de-datos` (f05), `ingenieria-de-features` (f05), `validacion-temporal` (f05) |
| 6 | `hurst-y-memoria` | Exponente de Hurst | — | `autocorrelacion-acf-pacf` (f05), `estacionariedad` (f05), `varianza-y-desviacion` (f01) |
| 7 | `markowitz-y-frontera` | Markowitz y la frontera eficiente | — | `covarianza-y-correlacion` (f01), `optimizacion-con-restricciones` (f01), `varianza-y-desviacion` (f01) |
| 8 | `movimiento-browniano` | Movimiento browniano | — | `distribuciones-continuas` (f01), `ley-de-los-grandes-numeros` (f01), `variable-aleatoria` (f01) |
| 9 | `ecuaciones-diferenciales-estocasticas` | Ecuaciones diferenciales estocásticas | `movimiento-browniano` | `derivadas-y-reglas` (f01), `integrales` (f01) |
| 10 | `pairs-trading` | Trading de pares | `cointegracion` | `correlacion-pearson-spearman` (f01), `z-score-y-estandarizacion` (f01) |
| 11 | `que-es-un-mercado` | Qué es un mercado | — | — |
| 12 | `microestructura-de-mercado` | Microestructura de mercado | `que-es-un-mercado` | — |
| 13 | `retornos-logaritmicos` | Retornos logarítmicos | — | `escalado-y-transformacion` (f05), `estacionariedad` (f05), `medidas-de-dispersion` (f01) |
| 14 | `criterio-de-kelly` | Criterio de Kelly | `retornos-logaritmicos` | `valor-esperado` (f01), `varianza-y-desviacion` (f01) |
| 15 | `curva-de-tipos-y-descuento` | Curva de tipos y descuento | `retornos-logaritmicos` | `notacion-matematica` (f00), `varianza-y-desviacion` (f01) |
| 16 | `diferenciacion-fraccional` | Diferenciación fraccional | `retornos-logaritmicos` | `autocorrelacion-acf-pacf` (f05), `estacionariedad` (f05), `test-adf-kpss` (f05) |
| 17 | `lema-de-ito` | Lema de Itô | `ecuaciones-diferenciales-estocasticas`, `retornos-logaritmicos` | `regla-de-la-cadena` (f01) |
| 18 | `ratio-de-sharpe` | Ratio de Sharpe | `retornos-logaritmicos` | `valor-esperado` (f01), `varianza-y-desviacion` (f01), `z-score-y-estandarizacion` (f01) |
| 19 | `reversion-a-la-media` | Reversión a la media | — | `autocorrelacion-acf-pacf` (f05), `estacionariedad` (f05), `z-score-y-estandarizacion` (f01) |
| 20 | `riesgo-de-ruina` | Riesgo de ruina | `criterio-de-kelly` | `probabilidad-axiomas` (f01), `valor-esperado` (f01) |
| 21 | `sesgo-de-mirar-al-futuro` | Sesgo de mirar al futuro | — | `fuga-de-datos` (f05), `train-val-test` (f06), `validacion-temporal` (f05) |
| 22 | `backtesting-vectorizado` | Backtesting vectorizado | `retornos-logaritmicos`, `sesgo-de-mirar-al-futuro` | `vectorizacion` (f03) |
| 23 | `alpha-decay` | Decaimiento del alpha | `backtesting-vectorizado`, `data-snooping-y-multiple-testing`, `generacion-de-senales` | — |
| 24 | `sesgo-de-supervivencia` | Sesgo de supervivencia | `retornos-logaritmicos`, `sesgo-de-mirar-al-futuro` | — |
| 25 | `sharpe-deflactado` | Sharpe deflactado | `data-snooping-y-multiple-testing`, `ratio-de-sharpe` | `asimetria-y-curtosis` (f01), `intervalos-de-confianza` (f02) |
| 26 | `tick-data-y-ohlcv` | Datos de transacción y velas | `que-es-un-mercado` | — |
| 27 | `indicadores-tecnicos` | Indicadores técnicos | `retornos-logaritmicos`, `tick-data-y-ohlcv` | — |
| 28 | `order-book-y-spread` | Libro de órdenes y diferencial | `microestructura-de-mercado`, `tick-data-y-ohlcv` | — |
| 29 | `slippage-y-comisiones` | Deslizamiento y comisiones | `microestructura-de-mercado`, `order-book-y-spread` | — |
| 30 | `backtesting-por-eventos` | Backtesting por eventos | `backtesting-vectorizado`, `order-book-y-spread`, `slippage-y-comisiones` | — |
| 31 | `latencia-y-ejecucion` | Latencia y ejecución | `microestructura-de-mercado`, `order-book-y-spread`, `que-es-un-mercado`, `slippage-y-comisiones` | — |
| 32 | `algoritmos-de-ejecucion` | Algoritmos de ejecución: VWAP, TWAP e iceberg | `latencia-y-ejecucion`, `microestructura-de-mercado`, `order-book-y-spread`, `slippage-y-comisiones` | — |
| 33 | `mql5-y-metatrader` | MQL5 y MetaTrader | `slippage-y-comisiones`, `tick-data-y-ohlcv` | — |
| 34 | `paper-trading` | Paper trading | `que-es-un-mercado`, `slippage-y-comisiones` | — |
| 35 | `protocolo-fix` | Protocolo FIX | `latencia-y-ejecucion`, `microestructura-de-mercado`, `order-book-y-spread` | — |
| 36 | `quantconnect-y-lean` | QuantConnect y LEAN | `backtesting-por-eventos`, `paper-trading` | — |
| 37 | `valoracion-de-opciones` | Valoración de opciones | `curva-de-tipos-y-descuento`, `movimiento-browniano` | `valor-esperado` (f01) |
| 38 | `griegas-y-cobertura` | Griegas y cobertura | `valoracion-de-opciones` | `operaciones-matriciales` (f01), `optimizacion-con-restricciones` (f01) |
| 39 | `vectorbt-backtrader-zipline` | VectorBT, Backtrader y Zipline | `backtesting-por-eventos`, `backtesting-vectorizado` | — |
| 40 | `volatilidad-realizada` | Volatilidad realizada | `retornos-logaritmicos` | `autocorrelacion-acf-pacf` (f05), `series-temporales-componentes` (f05), `varianza-y-desviacion` (f01) |
| 41 | `metricas-de-riesgo` | Métricas de riesgo: panorama | `ratio-de-sharpe`, `volatilidad-realizada` | — |
| 42 | `maximo-drawdown` | Caída máxima (max drawdown) | `metricas-de-riesgo`, `ratio-de-sharpe`, `retornos-logaritmicos` | — |
| 43 | `momentum` | Momentum | `retornos-logaritmicos`, `volatilidad-realizada` | `autocorrelacion-acf-pacf` (f05) |
| 44 | `psicologia-del-trading` | Psicología del trading | `maximo-drawdown` | `valor-esperado` (f01) |
| 45 | `regimenes-de-mercado` | Regímenes de mercado | `volatilidad-realizada` | `hmm-regimenes` (f05), `validacion-temporal` (f05) |
| 46 | `simulacion-de-monte-carlo` | Simulación de Monte Carlo | `maximo-drawdown` | `bootstrap` (f02), `variable-aleatoria` (f01) |
| 47 | `sortino-y-calmar` | Sortino y Calmar | `maximo-drawdown`, `metricas-de-riesgo`, `ratio-de-sharpe` | — |
| 48 | `tamano-de-posicion` | Tamaño de posición | `criterio-de-kelly`, `riesgo-de-ruina`, `volatilidad-realizada` | — |
| 49 | `construccion-de-carteras` | Construcción de carteras | `tamano-de-posicion` | `correlacion-pearson-spearman` (f01), `covarianza-y-correlacion` (f01) |
| 50 | `arbitraje-estadistico` | Arbitraje estadístico | `cointegracion`, `construccion-de-carteras` | `regresion-lineal` (f06), `z-score-y-estandarizacion` (f01) |
| 51 | `prueba-de-fondeo` | Pruebas de fondeo | `maximo-drawdown`, `metricas-de-riesgo`, `riesgo-de-ruina`, `tamano-de-posicion` | — |
| 52 | `rebalanceo` | Rebalanceo | `construccion-de-carteras`, `markowitz-y-frontera`, `retornos-logaritmicos` | — |
| 53 | `risk-parity-y-hrp` | Risk parity y HRP | `construccion-de-carteras`, `markowitz-y-frontera` | `covarianza-y-correlacion` (f01), `varianza-y-desviacion` (f01) |
| 54 | `triple-barrera` | Etiquetado por triple barrera | `retornos-logaritmicos`, `sesgo-de-mirar-al-futuro`, `tick-data-y-ohlcv`, `volatilidad-realizada` | — |
| 55 | `meta-labeling` | Meta-etiquetado | `triple-barrera` | `metricas-de-clasificacion` (f06), `umbrales-y-coste` (f06) |
| 56 | `purged-kfold` | K-fold con purga y embargo | `triple-barrera` | `autocorrelacion-acf-pacf` (f05), `fuga-de-datos` (f05), `validacion-cruzada` (f06) |
| 57 | `sample-weights` | Pesos de muestra | `triple-barrera` | `autocorrelacion-acf-pacf` (f05), `validacion-cruzada` (f06) |
| 58 | `validacion-combinatoria-cpcv` | Validación combinatoria (CPCV) | `purged-kfold`, `ratio-de-sharpe` | `validacion-cruzada` (f06) |
| 59 | `var-y-cvar` | VaR y CVaR | `maximo-drawdown`, `metricas-de-riesgo` | `cuantiles-y-percentiles` (f01) |
| 60 | `venta-en-corto-mecanica` | Vender en corto: préstamo, coste y recalls | `metricas-de-riesgo`, `order-book-y-spread`, `que-es-un-mercado` | — |
| 61 | `volatility-drag` | Volatility drag | `ratio-de-sharpe`, `retornos-logaritmicos` | `varianza-y-desviacion` (f01) |

## f10 — Algoritmos y estructuras (32 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `aleatoriedad-y-muestreo`, `complejidad-asintotica`, `optimizacion-matematica`.

**Prerequisitos externos:** 8 conceptos dependen de 11 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `aleatoriedad-y-muestreo` | Aleatoriedad y muestreo | — | `poblacion-y-muestra` (f02), `probabilidad-axiomas` (f01), `variable-aleatoria` (f01) |
| 2 | `complejidad-asintotica` | Complejidad asintótica | — | `notacion-matematica` (f00) |
| 3 | `arrays-y-listas` | Arrays y listas | `complejidad-asintotica` | `tipos-y-estructuras-python` (f03) |
| 4 | `analisis-amortizado` | Análisis amortizado | `arrays-y-listas`, `complejidad-asintotica` | — |
| 5 | `arreglos-de-cache-y-lineas-de-cache` | Jerarquía de memoria y localidad de caché | `arrays-y-listas`, `complejidad-asintotica` | `rendimiento-y-perfilado` (f11) |
| 6 | `optimizacion-matematica` | Optimización matemática | — | `convexidad` (f01), `derivadas-parciales-y-gradiente` (f01), `optimizacion-con-restricciones` (f01) |
| 7 | `ordenacion` | Algoritmos de ordenación | `arrays-y-listas`, `complejidad-asintotica` | — |
| 8 | `busqueda-binaria` | Búsqueda binaria | `arrays-y-listas`, `complejidad-asintotica`, `ordenacion` | — |
| 9 | `pilas-y-colas` | Pilas, colas y deques | `arrays-y-listas`, `complejidad-asintotica` | — |
| 10 | `recursion-y-backtracking` | Recursión y backtracking | `complejidad-asintotica`, `pilas-y-colas` | — |
| 11 | `arboles-binarios` | Árboles binarios y de búsqueda | `complejidad-asintotica`, `recursion-y-backtracking` | — |
| 12 | `arboles-balanceados` | Árboles balanceados | `arboles-binarios`, `complejidad-asintotica`, `recursion-y-backtracking` | — |
| 13 | `divide-y-venceras` | Divide y vencerás | `complejidad-asintotica`, `ordenacion`, `recursion-y-backtracking` | — |
| 14 | `heaps-y-prioridad` | Montículos y colas de prioridad | `arboles-binarios`, `arrays-y-listas`, `complejidad-asintotica` | — |
| 15 | `ordenacion-externa` | Ordenación externa | `complejidad-asintotica`, `heaps-y-prioridad`, `ordenacion` | — |
| 16 | `programacion-dinamica` | Programación dinámica | `complejidad-asintotica`, `divide-y-venceras`, `recursion-y-backtracking` | — |
| 17 | `algoritmos-greedy` | Algoritmos voraces | `complejidad-asintotica`, `ordenacion`, `programacion-dinamica` | — |
| 18 | `tablas-hash` | Tablas hash | `analisis-amortizado`, `arrays-y-listas`, `complejidad-asintotica` | — |
| 19 | `algoritmos-de-join` | Algoritmos de join | `ordenacion`, `tablas-hash` | — |
| 20 | `algoritmos-de-streaming` | Algoritmos de streaming | `aleatoriedad-y-muestreo`, `complejidad-asintotica`, `tablas-hash` | — |
| 21 | `bloom-filters` | Filtros de Bloom | `complejidad-asintotica`, `tablas-hash` | `probabilidad-axiomas` (f01) |
| 22 | `compresion` | Compresión | `arrays-y-listas`, `complejidad-asintotica`, `tablas-hash` | `entropia-e-informacion` (f01) |
| 23 | `concurrencia-algoritmica` | Concurrencia y paralelismo | `analisis-amortizado`, `complejidad-asintotica`, `tablas-hash` | — |
| 24 | `grafos-representacion` | Grafos: representación | `arrays-y-listas`, `complejidad-asintotica`, `tablas-hash` | — |
| 25 | `bfs-y-dfs` | Recorridos BFS y DFS | `complejidad-asintotica`, `grafos-representacion`, `pilas-y-colas` | — |
| 26 | `caminos-minimos` | Caminos mínimos | `bfs-y-dfs`, `grafos-representacion`, `heaps-y-prioridad`, `programacion-dinamica` | — |
| 27 | `map-reduce` | MapReduce y cómputo distribuido | `complejidad-asintotica`, `ordenacion`, `tablas-hash` | — |
| 28 | `np-completitud` | NP-completitud | `algoritmos-greedy`, `complejidad-asintotica`, `grafos-representacion`, `programacion-dinamica` | — |
| 29 | `algoritmos-de-aproximacion` | Algoritmos de aproximación | `algoritmos-greedy`, `complejidad-asintotica`, `np-completitud` | — |
| 30 | `tries` | Árboles de prefijos (tries) | `arboles-binarios`, `complejidad-asintotica`, `tablas-hash` | — |
| 31 | `indices-y-busqueda-en-texto` | Índices y búsqueda en texto | `ordenacion`, `tablas-hash`, `tries` | `procesamiento-de-texto-clasico` (f06) |
| 32 | `union-find` | Conjuntos disjuntos (union-find) | `analisis-amortizado`, `arboles-binarios`, `grafos-representacion` | — |

## f11 — Ingeniería de software (34 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `apis-rest`, `contenedores`, `gestion-de-memoria`, `git-avanzado`, `principios-solid`, `testing-piramide`.

**Prerequisitos externos:** 21 conceptos dependen de 20 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `apis-rest` | APIs REST | — | `apis-y-peticiones-http` (f03) |
| 2 | `accesibilidad` | Accesibilidad | `apis-rest` | — |
| 3 | `autenticacion-y-autorizacion` | Autenticación y autorización | `apis-rest` | — |
| 4 | `contenedores` | Contenedores | — | `docker-para-datos` (f04), `entorno-python` (f03) |
| 5 | `gestion-de-memoria` | Gestión de memoria | — | `arrow-y-formatos-columnares` (f03), `tipos-y-estructuras-python` (f03), `vistas-y-copias` (f03) |
| 6 | `cache-y-redis` | Caché y Redis | `apis-rest`, `gestion-de-memoria` | — |
| 7 | `concurrencia-async-hilos-procesos` | Concurrencia, asincronía, hilos y procesos | `gestion-de-memoria` | `apis-y-peticiones-http` (f03), `concurrencia-algoritmica` (f10) |
| 8 | `fastapi` | FastAPI | `apis-rest`, `concurrencia-async-hilos-procesos` | `tipado-y-linters` (f03) |
| 9 | `git-avanzado` | Git avanzado | — | `git-para-datos` (f03) |
| 10 | `graphql-y-grpc` | GraphQL y gRPC | `apis-rest` | `apis-y-peticiones-http` (f03) |
| 11 | `idempotencia-en-apis` | Idempotencia en APIs | `apis-rest`, `autenticacion-y-autorizacion` | — |
| 12 | `colas-y-mensajeria` | Colas y mensajería | `apis-rest`, `idempotencia-en-apis` | `batch-vs-streaming` (f04) |
| 13 | `principios-solid` | Principios SOLID | — | `tipado-y-linters` (f03), `tipos-y-estructuras-python` (f03) |
| 14 | `patrones-de-diseno` | Patrones de diseño | `principios-solid` | `tipos-y-estructuras-python` (f03) |
| 15 | `rendimiento-y-perfilado` | Rendimiento y perfilado | `concurrencia-async-hilos-procesos`, `gestion-de-memoria` | `numpy-fundamentos` (f03) |
| 16 | `logging-y-trazas` | Registro y trazas | `apis-rest`, `rendimiento-y-perfilado` | — |
| 17 | `metricas-y-alertas` | Métricas, SLO y alertas | `apis-rest`, `cache-y-redis`, `logging-y-trazas` | `observabilidad-de-datos` (f04) |
| 18 | `incidentes-y-postmortem` | Incidentes y postmortem | `git-avanzado`, `logging-y-trazas`, `metricas-y-alertas` | `errores-y-depuracion` (f03) |
| 19 | `copias-de-seguridad-y-recuperacion` | Copias de seguridad y recuperación ante desastres | `incidentes-y-postmortem` | `almacenamiento-de-objetos` (f04), `gobierno-y-privacidad` (f04) |
| 20 | `resiliencia-de-servicios` | Resiliencia de servicios: cortacircuitos y degradación | `apis-rest`, `cache-y-redis`, `idempotencia-en-apis`, `metricas-y-alertas` | — |
| 21 | `secretos-y-configuracion` | Secretos y configuración | `autenticacion-y-autorizacion` | `entorno-python` (f03), `git-para-datos` (f03) |
| 22 | `seguridad-owasp` | Seguridad de aplicaciones | `apis-rest`, `autenticacion-y-autorizacion`, `secretos-y-configuracion` | — |
| 23 | `privacidad-y-gdpr` | Privacidad y RGPD | `seguridad-owasp` | `kafka-y-colas` (f04) |
| 24 | `sistemas-distribuidos-bases` | Sistemas distribuidos: bases | `cache-y-redis`, `colas-y-mensajeria` | `particionado-y-clustering` (f04) |
| 25 | `cap-y-consistencia` | CAP y modelos de consistencia | `cache-y-redis`, `sistemas-distribuidos-bases` | — |
| 26 | `consenso-y-replicacion` | Consenso y replicación | `cap-y-consistencia`, `sistemas-distribuidos-bases` | — |
| 27 | `exactamente-una-vez` | Entrega exactamente una vez | `cap-y-consistencia`, `colas-y-mensajeria`, `idempotencia-en-apis` | — |
| 28 | `sesgo-y-etica-en-datos` | Sesgo y ética en datos | `exactamente-una-vez` | `metricas-de-clasificacion` (f06), `train-val-test` (f06) |
| 29 | `testing-piramide` | La pirámide de pruebas | — | `testing-con-pytest` (f03) |
| 30 | `arquitectura-de-aplicaciones` | Arquitectura de aplicaciones: capas, límites y dependencias | `patrones-de-diseno`, `principios-solid`, `sistemas-distribuidos-bases`, `testing-piramide` | — |
| 31 | `ci-cd` | Integración y despliegue continuos | `testing-piramide` | `git-para-datos` (f03) |
| 32 | `code-review` | Revisión de código | `git-avanzado`, `testing-piramide` | — |
| 33 | `tdd` | Desarrollo guiado por pruebas | `testing-piramide` | `testing-con-pytest` (f03) |
| 34 | `refactorizacion` | Refactorización | `principios-solid`, `tdd`, `testing-piramide` | — |

## f12 — Comunicación y carrera (15 conceptos)

**Puntos de entrada (sin prerequisitos dentro de la fase):** `entrevistas-de-datos`, `especializacion-y-carrera`, `open-source`, `portfolio-y-proyectos`, `storytelling-con-datos`.

**Prerequisitos externos:** 8 conceptos dependen de 13 conceptos de otras fases; no bloquean el orden y se anotan en la última columna.

| orden | id | título | prerequisitos (en la fase) | prerequisitos externos |
| ---: | --- | --- | --- | --- |
| 1 | `entrevistas-de-datos` | Entrevistas técnicas de datos | — | `hacer-preguntas-buenas` (f00), `intervalos-de-confianza` (f02), `sql-ventanas` (f03) |
| 2 | `especializacion-y-carrera` | Especialización y carrera | — | `mapa-del-portal` (f00), `practicar-con-datos-reales` (f00) |
| 3 | `open-source` | Contribuir a código abierto | — | `code-review` (f11), `git-para-datos` (f03), `testing-con-pytest` (f03) |
| 4 | `portfolio-y-proyectos` | Portfolio y proyectos | — | `git-para-datos` (f03), `practicar-con-datos-reales` (f00) |
| 5 | `certificaciones-de-datos` | Certificaciones de datos | `especializacion-y-carrera`, `portfolio-y-proyectos` | — |
| 6 | `storytelling-con-datos` | Contar historias con datos | — | `metricas-de-clasificacion` (f06) |
| 7 | `escribir-un-informe` | Escribir un informe técnico | `storytelling-con-datos` | — |
| 8 | `documentacion-tecnica` | Documentación técnica | `escribir-un-informe` | — |
| 9 | `freelance-y-consultoria` | Freelance y consultoría | `escribir-un-informe`, `especializacion-y-carrera`, `portfolio-y-proyectos` | — |
| 10 | `presentaciones` | Presentar a audiencias distintas | `storytelling-con-datos` | — |
| 11 | `visualizacion-honesta` | Visualización honesta | `storytelling-con-datos` | `medidas-de-centralidad` (f01) |
| 12 | `dashboards` | Cuadros de mando | `storytelling-con-datos`, `visualizacion-honesta` | — |
| 13 | `etica-profesional` | Ética profesional | `escribir-un-informe`, `visualizacion-honesta` | `sesgo-y-etica-en-datos` (f11) |
| 14 | `metricas-de-producto` | Métricas de producto | `dashboards` | `ab-testing` (f02), `cuantiles-y-percentiles` (f01) |
| 15 | `priorizar-y-planificar` | Priorizar: qué se hace, qué se aplaza y qué se descarta | `dashboards`, `escribir-un-informe`, `storytelling-con-datos` | — |
