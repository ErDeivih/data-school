# Cobertura del temario: qué falta de verdad y qué no hace falta

**Fecha:** 2026-11-02 · **Base:** 450 conceptos y 13 fases, contrastados con cuatro modelos de
referencia y con el corpus de 300 vídeos del que salieron los seis informes.

La pregunta que responde este documento es incómoda y hay que contestarla sin vender humo:
**¿está todo el mundo de los datos en la escuela?** No. Ningún temario lo está, y el que dice
estarlo miente. Lo que sí se puede medir es qué falta y si eso falta importa para el trabajo al
que apuntas.

---

## 1. Método

| Referencia | Qué aporta | Cómo se ha usado |
| --- | --- | --- |
| Data Engineering Zoomcamp (DataTalksClub) | El currículo gratuito más completo: Docker, SQL, Terraform, Airflow, dbt/BigQuery, Spark, Kafka | Comprobar que cada módulo tiene al menos un concepto que lo cubra |
| AWS Certified Data Engineer – Associate (DEA-C01) | Cuatro dominios: ingesta y transformación, almacenamiento, operaciones, seguridad y gobierno | Buscar los temas del examen que no aparecen en ningún id |
| *Fundamentals of Data Engineering* (Reis y Housley) | Ciclo de vida (generación, almacenamiento, ingesta, transformación, servicio) y seis corrientes subterráneas: seguridad, gestión del dato, DataOps, arquitectura, ingeniería de software y orquestación | Comprobar que las corrientes están representadas, no solo las etapas |
| Ofertas 2025-2026 de [`03-FUENTES.md`](03-FUENTES.md) §6 | SQL, Python, pipelines, una nube, orquestador, modelado y calidad | Verificar que lo que más se pide tiene página |
| Corpus de los 300 vídeos | Quant y finanzas cuantitativas | Delimitar qué parte del temario **no** puede venir de ahí |

Criterio de estado: **cubierto** si hay al menos un concepto cuyo título y resumen tratan el tema
de verdad; **parcial** si se toca dentro de otra página; **ausente** si no hay nada.

---

## 2. Cobertura por área

| Área | Estado | Dónde vive | Comentario |
| --- | --- | --- | --- |
| SQL: joins, ventanas, CTE, índices, planes | Cubierto | F03 (`sql-*`), F04 | Profundidad poco habitual: incluye algoritmos de join y transacciones |
| Modelado: normalización, estrella, copo, data vault, OBT | Cubierto | F04 (`modelado-dimensional`, `esquema-estrella-y-copo`, `data-vault`, `arquitectura-medallion`) | Con grano, SCD y reconciliación |
| Ingesta: batch, incremental, CDC, APIs, backfill | Cubierto | F04 (`ingesta-incremental-y-cdc`, `backfill-y-reproceso`, `apis-rest`) | Falta el detalle de eventos push (§3) |
| Formatos y almacenamiento | Cubierto | F04 (`parquet-avro-orc`, `lakehouse-y-table-formats`, `almacenamiento-de-objetos`, `particionado-y-clustering`) | Iceberg y Delta están dentro de `lakehouse`, sin página propia |
| Procesamiento: Spark, streaming, ventanas, exactly-once | Cubierto | F04 (`spark-*`, `streaming-tiempo-real`, `ventanas-y-watermarks`, `exactamente-una-vez`) | Bien; falta Flink como motor concreto |
| Orquestación | Cubierto | F04 (`orquestacion-y-dag`, `airflow-dagster-prefect`, `idempotencia-y-reintentos`) | Incluye el enfoque por activos |
| Transformación con dbt y capa semántica | Cubierto | F04 (`dbt-y-transformacion`, `capa-semantica-y-metricas`, `contratos-de-datos`) | |
| Calidad, observabilidad, linaje, catálogo | Cubierto | F04 (`calidad-de-datos`, `calidad-y-slas`, `observabilidad-de-datos`, `catalogo-y-linaje`) | |
| Fiabilidad: SLO, incidentes, postmortem, copias | Cubierto | F04, F11 (`incidentes-y-postmortem`, `resiliencia-de-servicios`) | |
| Seguridad y gobierno | Parcial | F11 (`gobierno-y-privacidad`, `privacidad-y-gdpr`, `control-de-acceso-por-fila-y-columna`, `secretos-y-configuracion`) | Falta identidad cloud (IAM) y enmascarado (§3) |
| Plataforma: Docker, Kubernetes, Terraform, CI/CD | Cubierto | F11 (`docker-para-datos`, `kubernetes-basico`, `iac-y-terraform`, `ci-cd`) | |
| Coste y rendimiento | Cubierto | F04, F11 (`coste-y-optimizacion`, `particionado-y-clustering`, `nubes-y-servicios-gestionados`) | |
| Sistemas: CAP, consenso, colas, caché | Cubierto | F11, F10 (`cap-y-consistencia`, `consenso-y-replicacion`, `colas-y-mensajeria`, `cache-y-redis`) | |
| Estadística e inferencia | Cubierto | F01, F02 | El bloque más sólido del temario |
| Machine learning clásico y validación | Cubierto | F06 | Con métricas, fuga y validación temporal |
| Deep learning y LLMs aplicados | Cubierto | F07, F08 | Con RAG, embeddings y evaluación |
| Series temporales | Cubierto | F05 | Estacionariedad, STL, ARIMA, validación temporal |
| Algoritmos y estructuras | Cubierto | F10 | Con medición de coste |
| Comunicación, producto y carrera | Cubierto | F12 | Entrevistas, portfolio, visualización honesta |
| **Terminal, shell y automatización con cron** | **Ausente** | — | No hay página de línea de comandos, pipes, permisos ni tareas programadas |
| **Identidad y permisos en la nube (IAM)** | **Ausente** | — | Hay acceso por fila y columna, pero no roles, políticas ni mínimo privilegio |
| **El problema de los ficheros pequeños** | **Ausente** | — | `particionado-y-clustering` no cubre compactación ni tamaño objetivo |
| **Eventos push y webhooks** | Parcial | F03 (`apis-y-peticiones-http`) | Solo el modelo de sondeo |
| Registro de esquemas y compatibilidad | Cubierto | F04 (`registro-de-esquemas`) | Con modos de compatibilidad y reglas de evolución |
| **Enmascarado, anonimización y retención** | Parcial | F11 (`gobierno-y-privacidad`, `privacidad-y-gdpr`) | Falta el cómo: técnicas y políticas de retención |
| Flink y procesamiento de eventos | Cubierto | F04 (`flink-y-procesamiento-de-eventos`) | Estado, watermarks y checkpoints |

**Resumen:** de las 26 áreas, **las 26 están cubiertas** con al menos una página propia, **5 de forma
parcial** y **3 ausentes**. De las parciales, dos merecen página (eventos push y enmascarado). Los
cinco huecos de §3 no son conceptualmente difíciles: son **oficio**.

---

## 3. Los cinco huecos que sí merecían una página (cerrados el 2026-11-02)

Ordenados por lo que se nota en un trabajo real, no por elegancia. **Las cinco páginas están
escritas y validadas:** `terminal-y-shell`, `iam-y-permisos-cloud`, `problema-de-ficheros-pequenos`,
`eventos-push-y-webhooks` y `enmascarado-y-retencion`.

### G1 · `terminal-y-shell` (F03, básico)

`prerequisitos: [entorno-python, ficheros-y-encoding]`

Pipes, redirecciones, permisos, `grep`, `find`, `awk`, `cron`, `ssh`, variables de entorno y
códigos de salida. Es la herramienta con la que se depura un pipeline a las tres de la mañana y
la que casi nadie enseña porque no es divertida. Un data engineer sin shell depende de que otro le
ejecute las cosas.

### G2 · `iam-y-permisos-cloud` (F04, intermedio)

`prerequisitos: [nubes-y-servicios-gestionados, autenticacion-y-autorizacion]`

Roles, políticas, cuentas de servicio, mínimo privilegio, credenciales de corta duración y el error
clásico de dar `*` sobre `*`. Es la mitad de la seguridad de un pipeline en la nube y la primera
pregunta de un auditor.

### G3 · `problema-de-ficheros-pequenos` (F04, avanzado)

`prerequisitos: [parquet-avro-orc, particionado-y-clustering]`

Miles de ficheros de 10 KB en un lago destrozan el rendimiento: listar cuesta más que leer.
Compactación, tamaño objetivo por fichero, `OPTIMIZE`/`VACUUM` y por qué partitionar por hora es
peor que por día si el volumen es bajo. Es el problema que nadie documenta y todo el mundo sufre.

### G4 · `eventos-push-y-webhooks` (F04, intermedio)

`prerequisitos: [apis-rest, idempotencia-y-reintentos]`

Cuándo el origen empuja en vez de esperar a que lo consultes, cómo verificar la firma, qué hacer si
llegan duplicados o desordenados y por qué un webhook sin idempotencia es una fábrica de datos
duplicados.

### G5 · `enmascarado-y-retencion` (F04, avanzado)

`prerequisitos: [gobierno-y-privacidad, privacidad-y-gdpr]`

Hash, tokenización, seudonimización, k-anonimato, políticas de retención y derecho de supresión
aplicados a un almacén real. La teoría legal ya está en F11; lo que falta es el cómo técnico y su
coste.

Dos más, de prioridad baja: `registro-de-esquemas` (compatibilidad en streaming) y
`flink-y-procesamiento-de-eventos` (un motor más, no un concepto nuevo).

---

## 4. Lo que no se aprende con una página más

Esta es la parte que ningún temario dice y que decide más que el temario.

| Necesidad | Por qué no está en el portal | Cómo se cubre |
| --- | --- | --- |
| Una cuenta cloud real con permisos y factura | Exige una cuenta, tarjeta y decisiones que no se pueden documentar | Los proyectos PF-01 a PF-05, con presupuesto y borrado al terminar |
| Trabajar con datos de otras personas | Depende de un equipo que no tienes | Contribuir a un proyecto abierto, o simularlo con un contrato y un revisor |
| Inglés técnico de lectura rápida | Se aprende leyendo documentación, no una página | Leer la documentación oficial en inglés, no un resumen en español |
| Negociar requisitos con negocio | Requiere interlocutores | F12 da el marco; la práctica es hablar con alguien real |
| Depurar bajo presión | Se aprende rompiendo cosas | Los proyectos con incidentes provocados a propósito |

Y una advertencia que va en la línea del portal: **tener 450 páginas no te hace data engineer.**
Te hace alguien que puede explicar 450 conceptos. Lo que te contrata es un pipeline que se puede
reejecutar, con tests, y una explicación honesta de qué no cubre.

---

## 5. Qué se puede decir de los 300 vídeos

Los seis informes que salieron de ese corpus son **quant**: estadística, procesos estocásticos,
valoración, griegas, backtesting. De ahí salieron once páginas y trece enriquecimientos, y con eso
el corpus está exprimido: no hay más conceptos que extraer de él que merezcan una página.

Lo que el corpus **no** cubre, y por eso no puede ser la única fuente:

- Ingeniería de datos: ingesta, orquestación, modelado, calidad, coste. Cero.
- SQL en profundidad. Cero.
- Plataforma y fiabilidad. Casi nada.
- El bloque de validación de López de Prado, que la escuela ya tiene y el corpus no.

Conclusión: el corpus era una fuente excelente para una rama concreta y una mala guía general.
La escuela ya no depende de él.

---

## 6. Veredicto y siguiente paso

- **Cobertura:** 26 áreas cubiertas de 26, ninguna parcial y ninguna ausente. Los dos últimos
  parciales (`registro-de-esquemas` y `flink-y-procesamiento-de-eventos`) ya tienen página.
- **Lo que falta por escribir:** nada del corpus, nada de los cinco huecos y nada de proyectos:
  están los seis de F1 y cartera en el portal. Quedan dos conceptos parciales que no merecen
  página propia todavía.
- **Lo que falta por hacer:** los proyectos de portfolio. Sin ellos, el temario es una biblioteca;
  con ellos, es una candidatura.

Si hay que elegir un orden: **G1 (shell) y G3 (ficheros pequeños)** primero, porque son los que
más duelen en el primer trabajo; después G2 (IAM) y G4 (webhooks); G5 cuando haya datos personales
de por medio.
