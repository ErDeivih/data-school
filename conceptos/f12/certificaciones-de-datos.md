---
id: certificaciones-de-datos
titulo: Certificaciones de datos
fase: 12
nivel: básico
rutas: [core, de]
prerequisitos: [especializacion-y-carrera, portfolio-y-proyectos]
tags: [certificacion, carrera, examen]
resumen: Qué certifica cada examen de datos, en qué orden sacarlas según el mercado y cómo se prepara una sin estudiar el doble de lo que pide.
fuentes: ["AWS (2026), 'Certified Data Engineer - Associate exam guide'", "Microsoft (2026), 'Study guide for Exam DP-700'"]
---

## En una frase

Una certificación no demuestra que sepas hacer el trabajo: demuestra que conoces el vocabulario y
los servicios de una plataforma concreta, y sirve para pasar el primer filtro de recursos humanos.

## La idea

Hay dos tipos de certificado y conviene no confundirlos. Los de **plataforma** (AWS, Azure, Google,
Databricks, Snowflake) evalúan servicios concretos: qué hace un servicio, cómo se conecta con otro,
cuánto cuesta y qué límite tiene. Los de **método** (dbt, Airflow) evalúan una herramienta que se
usa igual en cualquier nube.

Ninguno de los dos sustituye a un proyecto. Un examen se aprueba estudiando el temario oficial; un
puesto se consigue porque alguien puede enseñar un pipeline que se reejecuta. Pero la
certificación hace algo que el proyecto no: pasa el filtro automático de un portal de empleo y da
un vocabulario común en la entrevista.

El error caro es sacarlas en el orden equivocado. La primera debe ser la de la plataforma que
aparezca en las ofertas de tu ciudad; la segunda, la del almacén o el motor que use ese mercado. Y
ninguna antes de tener un proyecto que enseñar.

**Los cuatro niveles, y ninguno se salta.** Primero lo gratis (cursos y badges de dbt, Kafka,
Airflow y lakehouse), después una básica de nube o de BI, después la media de plataforma y solo al
final las altas, que son exámenes de diseño.

| Nivel | Qué es | Coste aproximado | Requisito para empezar |
| --- | --- | --- | --- |
| 0 | Cursos y badges gratuitos | 0 € | Ninguno |
| 1 | Básicas: nube o BI | 90-170 USD | F03 y F04 iniciales |
| 2 | Medias: data engineer de plataforma | 150-250 USD | Un proyecto terminado |
| 3 | Altas: diseño, streaming y rendimiento | 200-375 USD | Dos años de práctica o uno intenso |

:::trampa
Estudiar para el examen mirando vídeos de «trucos» no funciona: los exámenes de datos preguntan
por decisiones («qué servicio usarías para esto») y por límites. La forma eficaz es leer la guía
oficial del examen, marcar los dominios con su peso, y practicar con el simulador oficial, que
suele ser el único material con el formato real.
:::

## Definición formal

Cada examen publica una guía con dominios y pesos. Se prepara en cuatro pasos, en este orden:

:::formula
guía oficial → mapa de dominios a fases del portal → práctica con simulacro → examen
:::

- **Guía oficial** — el documento del proveedor con los dominios, su peso y las tareas evaluadas.
  Es la única fuente que hay que leer entera.
- **Mapa de dominios** — cada dominio se cruza con una fase: ingesta con F04, seguridad con F11,
  coste con F04. Lo que no tenga fase se estudia aparte y se anota.
- **Simulacro** — el examen de práctica oficial. Dos intentos por debajo del 80 % significan que
  falta estudio, no suerte.
- **Examen** — presencial o en remoto con vigilancia. El resultado suele ser inmediato; el
  certificado tarda unos días.

**Duración:** la mayoría caduca a los tres años y se renueva con un examen más corto o con créditos
de formación. **Coste:** entre 150 y 250 dólares el intento; el material gratuito de los propios
proveedores cubre casi todo el temario.

## Ejemplo

Mercado español, objetivo data engineer, sin certificaciones previas:

| Orden | Certificación | Por qué en ese puesto | Coste |
| --- | --- | --- | --- |
| 1 | [AWS Certified Data Engineer – Associate](https://aws.amazon.com/certification/certified-data-engineer-associate/) | Es la que más aparece en consultoría y la que mejor relación señal/precio tiene | ~150 USD |
| 2 | [Microsoft DP-700 (Fabric)](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/) | Banca, seguros y administración en España van por Azure; sustituye a DP-203 | ~165 USD |
| 3 | [Databricks Data Engineer Associate](https://www.databricks.com/learn/certification/data-engineer-associate) | Examinación práctica y muy respetada en equipos de datos grandes | ~200 USD |
| 4 | [Snowflake SnowPro Core](https://www.snowflake.com/en/learn/certification/) | Solo si el stack objetivo es Snowflake: acredita producto, no ingeniería | ~175 USD |
| — | [Google Professional Data Engineer](https://cloud.google.com/learn/certification/data-engineer) | Más difícil y más de diseño; solo si hay ofertas GCP en tu zona | ~200 USD |

La 3 y la 4 se saltan si no aparecen en las ofertas que estás mirando. Antes de pagar, cuenta
cuántas ofertas de tu ciudad nombran esa plataforma: si son menos de diez, no es tu certificación
todavía.

## Dónde se pide cada una

| Certificación | Nivel | Enlace oficial |
| --- | --- | --- |
| dbt Fundamentals | 0 | [learn.getdbt.com](https://learn.getdbt.com/courses/dbt-fundamentals) |
| Confluent Kafka | 0 | [developer.confluent.io](https://developer.confluent.io/courses/) |
| Astronomer Airflow | 0 | [academy.astronomer.io](https://academy.astronomer.io/) |
| AWS Cloud Practitioner | 1 | [aws.amazon.com](https://aws.amazon.com/certification/certified-cloud-practitioner/) |
| Azure AZ-900 | 1 | [learn.microsoft.com](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) |
| Microsoft PL-300 | 1 | [learn.microsoft.com](https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/) |
| AWS DEA-C01 | 2 | [aws.amazon.com](https://aws.amazon.com/certification/certified-data-engineer-associate/) |
| Microsoft DP-700 | 2 | [learn.microsoft.com](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/) |
| Databricks DE Associate | 2 | [databricks.com](https://www.databricks.com/learn/certification/data-engineer-associate) |
| SnowPro Core | 2 | [snowflake.com](https://www.snowflake.com/en/learn/certification/) |
| Google PDE | 3 | [cloud.google.com](https://cloud.google.com/learn/certification/data-engineer) |
| Databricks DE Professional | 3 | [databricks.com](https://www.databricks.com/learn/certification/data-engineer-professional) |
| AWS AI Practitioner | 1 | [aws.amazon.com](https://aws.amazon.com/certification/certified-ai-practitioner/) |
| Azure AI Engineer (AI-102) | 2 | [learn.microsoft.com](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/) |
| AWS ML Engineer Associate | 2 | [aws.amazon.com](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) |
| Google Professional ML Engineer | 3 | [cloud.google.com](https://cloud.google.com/learn/certification/machine-learning-engineer) |
| Databricks ML Professional | 3 | [databricks.com](https://www.databricks.com/learn/certification/machine-learning-professional) |
| IBM SkillsBuild AI Fundamentals (gratis) | 0 | [skillsbuild.org](https://skillsbuild.org/) |
| Cisco AI Fundamentals con IBM (gratis) | 0 | [netacad.com](https://www.netacad.com/courses/ai-fundamentals-with-ibm-skillsbuild) |
| Google Cloud Generative AI badges (gratis) | 0 | [cloudskillsboost.google](https://www.cloudskillsboost.google/) |
| Databricks Academy badges (gratis) | 0 | [databricks.com](https://www.databricks.com/learn/training/home) |

## Código

```text
PLAN DE SEIS SEMANAS PARA UNA CERTIFICACION DE PLATAFORMA

  Semana 1  Leer la guia oficial entera y anotar los dominios con su peso.
            Cruzar cada dominio con una fase del portal y marcar los huecos.
  Semana 2  Servicios del dominio con mas peso. Laboratorio propio: crear la cuenta,
            montar el minimo y romperlo a proposito.
  Semana 3  Dominio de ingesta y transformacion (F04). Un pipeline pequeno de punta a punta.
  Semana 4  Dominio de almacenamiento y modelo (F04). Coste y particiones con numeros.
  Semana 5  Dominio de seguridad y gobierno (F11). IAM, cifrado, auditoria y retencion.
  Semana 6  Dos simulacros oficiales. Repasar solo lo fallado. Examen.

  Regla: si un dominio pesa menos del 15 %, se estudia para reconocerlo, no para dominarlo.
```

## Errores típicos

- **Sacar la certificación antes de tener un proyecto.** El certificado abre la puerta; sin
  proyecto, la entrevista técnica la cierra.
- **Estudiar servicios que no vas a usar.** El examen pregunta por el servicio que resuelve el
  problema al menor coste, no por el que más te gusta.
- **Ignorar los pesos de los dominios.** Un dominio del 10 % no merece el mismo tiempo que uno del
  34 %, y mucha gente estudia en orden alfabético.
- **No hacer el simulacro oficial.** El formato (opción múltiple con escenarios largos) sorprende a
  quien solo ha leído documentación.
- **Dejar caducar la certificación sin enterarse.** Se renueva; si caduca, hay que repetir el
  examen completo.
- **Coleccionar certificados.** Tres certificaciones sin proyectos dicen menos que una con dos
  pipelines funcionando.

:::practica
enunciado: Tienes 90 euros y ocho semanas. ¿Qué haces: un curso de pago, un simulador o el intento de examen? Justifica con lo que sabes del proceso.
pista: El material oficial es gratuito; lo que no es gratis es el intento.
solucion: Estudiar con la guía y el material gratuito del proveedor, hacer dos simulacros oficiales (el primero suele ser gratuito o barato) y gastar el dinero en el intento del examen. Un curso de pago no aporta nada que la guía no tenga; el simulador sí, porque entrena el formato.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Para qué sirve de verdad una certificación de plataforma?
o: Para pasar el filtro de vocabulario y de recursos humanos, no para demostrar que sabes construir
o: Para demostrar que sabes construir un pipeline en producción
o: Para sustituir el portfolio
a: 1
e: El examen evalúa conocimiento de servicios y decisiones, no tu capacidad de operar un pipeline real. Su valor práctico está en el filtro inicial y en el vocabulario compartido; el portfolio demuestra lo otro.
:::

:::quiz
p: ¿Cuál es el primer paso para preparar un examen?
o: Leer la guía oficial del examen y anotar los dominios con su peso
o: Ver una playlist de trucos del examen
o: Comprar el curso más vendido de la plataforma
a: 1
e: La guía oficial dice exactamente qué se evalúa y cuánto pesa cada bloque. Cualquier plan que no empiece por ahí estudia de más en unas cosas y de menos en las que deciden el aprobado.
:::
