# Por tramo: un principal y dos alternativas

Cuatro tramos —**F** fundamentos, **DE** data engineer, **DS** data scientist, **AI** AI engineer—
con un principal y dos alternativas cada uno. Todo sale del catálogo de [`FUENTES.md`](FUENTES.md);
no se añade nada nuevo.

## Regla de esta página

**Todas las fuentes se enlazan y la licencia decide qué se puede citar, no si se recomienda.**

Esto **sustituye al criterio antiguo de «ninguna restringida como principal»**. El criterio viejo
usaba la licencia como puerta de la recomendación: una fuente con licencia restrictiva no podía ser
principal, aunque fuese el mejor recurso de su tramo. El resultado era peor catálogo —dejaba fuera
el DE Zoomcamp (sin `LICENSE` explícita) y el ISLR («All Rights Reserved»)— sin ganar nada legal,
porque **aquí no se copia nada de ninguna fuente**: se enlaza y se resume con palabras propias.
Recomendar no es reutilizar. Por eso ahora la recomendación se decide por cobertura, calidad de
enseñanza, coste y disponibilidad; la licencia solo marca lo que se puede hacer con el contenido
(citar, traducir, reutilizar), y eso se consulta en cada fila de `FUENTES.md`. Recomendar una fuente
«solo enlace» es tan seguro como recomendar una CC BY: en ambos casos el material se queda en su
sitio.

Corolario: el principal de un tramo no tiene que ser reutilizable, y una alternativa puede tener
mejor licencia que el principal sin desbancarlo.

## Tramo F — fundamentos

| Papel | Fuente | Motivo |
|---|---|---|
| **Principal** | [MIT OCW](https://ocw.mit.edu) | Más de 2.500 cursos del MIT liberados en abierto: matemáticas, estadística y programación con el rigor de una universidad, gratis y sin cuenta. |
| Alternativa | [freeCodeCamp](https://www.freecodecamp.org) | Currículo interactivo con certificaciones para aprender programando desde cero (Python, SQL, JavaScript). |
| Alternativa | [Docs de Python](https://docs.python.org/3/) | Referencia primaria del lenguaje y su biblioteca estándar, con traducción parcial al español; el sitio al que se vuelve mientras se aprende. |

## Tramo DE — data engineer

| Papel | Fuente | Motivo |
|---|---|---|
| **Principal** | [DataTalksClub — DE Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Ruta gratis de 9 semanas que cubre el oficio entero (Docker, orquestación, warehouse, dbt, Spark, Kafka) y termina en proyecto final con deberes corregidos. |
| Alternativa | [dbt Learn](https://learn.getdbt.com/catalog) | Cursos oficiales de dbt para analytics engineering: modelado, tests y despliegue con cuenta gratis. |
| Alternativa | [Docs de Apache Airflow](https://airflow.apache.org/docs/) | Documentación oficial de orquestación por versión: tutoriales y referencia de operadores para la parte de pipelines. |

## Tramo DS — data scientist

| Papel | Fuente | Motivo |
|---|---|---|
| **Principal** | [An Introduction to Statistical Learning](https://www.statlearning.com/) | El manual estándar de estadística y ML clásico, con PDF gratis; da la base teórica que el resto de recursos da por supuesta. |
| Alternativa | [Kaggle Learn](https://www.kaggle.com/learn) | Micro-cursos con cuaderno y certificado (pandas, SQL, visualización, ML): la práctica rápida que complementa la teoría. |
| Alternativa | [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) | Manual de numpy, pandas, matplotlib y ML con cuadernos ejecutables; el puente entre la estadística y el código. |

## Tramo AI — AI engineer

| Papel | Fuente | Motivo |
|---|---|---|
| **Principal** | [DeepLearning.AI](https://www.deeplearning.ai) | Cursos cortos de IA generativa y LLMs centrados en construir aplicaciones con modelos, con especializaciones para profundizar. |
| Alternativa | [fast.ai](https://course.fast.ai/) | Curso práctico de deep learning en 9 lecciones, con libro gratis: la vía de arriba abajo, de construir a entender. |
| Alternativa | [Dive into Deep Learning](https://d2l.ai/) | Libro interactivo con código en PyTorch/JAX/TF: la referencia que se puede leer, ejecutar y reutilizar con atribución. |

## Alternativa de pago transversal

[Coursera](https://www.coursera.org) y [edX](https://www.edx.org) son la alternativa de pago
transversal a los cuatro tramos: en muchos cursos se puede **auditar gratis** y el certificado se
paga. Sirven de plan B cuando hace falta un curso con instructor y fechas, no como sustituto del
principal de cada tramo. Están marcadas como «mixto, avisado» en el catálogo: el coste se avisa
antes de cobrar.

## Resumen

| Tramo | Principal | Alternativa 1 | Alternativa 2 |
|---|---|---|---|
| F | MIT OCW | freeCodeCamp | Docs de Python |
| DE | DE Zoomcamp | dbt Learn | Docs de Apache Airflow |
| DS | ISLR | Kaggle Learn | Python Data Science Handbook |
| AI | DeepLearning.AI | fast.ai | Dive into Deep Learning |

Los enlaces, licencias y estados de cada una están en [`FUENTES.md`](FUENTES.md); las clases de
licencia y las reglas de entrada, en [`README.md`](README.md).
