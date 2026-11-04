# Fuentes externas de datasets

Catálogos ajenos de donde se pueden sacar datos para practicar. **No se copian ni se alojan en este
repositorio: se enlazan.** La licencia es **por ítem** y hay que comprobarla en la ficha de cada
dataset concreto antes de usarlo: la del catálogo no se hereda.

Esta página resume la sección 4 de [`../fuentes/FUENTES.md`](../fuentes/FUENTES.md) con palabras
propias, sin copiar texto de los catálogos. Comprobación de enlaces y licencias: **2026-11-04**.

## Regla de uso

> **Solo enlace. Comprobar la licencia de cada dataset antes de usarlo.**

Consecuencias prácticas:

1. Se enlaza la ficha oficial del dataset, no se descarga el fichero al repositorio.
2. Se lee la licencia **de ese ítem** (no la del catálogo, no la del autor de la lista).
3. Se anota en el ejercicio: URL, licencia y fecha de consulta. Sin esos tres datos no hay dataset.
4. Se respeta lo que pida la licencia: atribución, no comercial, compartir igual, sin derivadas…
5. Si la licencia no está clara o dice «Other»/«Unknown», no se usa. Sin licencia clara no entra.

## Catálogos

| Catálogo | Qué es | Licencia | Coste | Idioma | Estado |
|---|---|---|---|---|---|
| [Kaggle Datasets](https://www.kaggle.com/datasets) | Miles de conjuntos reales con API y cuadernos; para practicar SQL, joins, EDA y modelos. | **Una por dataset**, la elige el autor: hay CC0, CC BY 4.0, Apache-2.0, MIT, «Other» y «Unknown». | Gratis con cuenta | Metadatos en inglés; los datos, en muchos idiomas | Viva |
| [Hugging Face Datasets](https://huggingface.co/datasets) | Catálogo con filtro por licencia, idioma y tarea; fuerte en texto e IA. | **Una por dataset**; cada ficha declara la suya y el Hub permite filtrar por licencia. | Gratis (cuenta para lo privado) | Multilingüe | Viva |
| [data.gov](https://data.gov) | Catálogo federal de datos abiertos de EE. UU.: economía, clima, transporte, salud. | **Una por conjunto**, fijada por la agencia que publica (la mayoría, dominio público federal): hay que leer la ficha. | Gratis | Inglés | Viva |
| [datos.gob.es](https://datos.gob.es) | Catálogo español de datos abiertos; la licencia consta en los metadatos del dataset (p. ej. `CC_BY_4_0`). | **Una por dataset**, declarada en metadatos (comprobado CC BY 4.0 en un caso). | Gratis | Español (descripciones también en inglés) | Viva |
| [UCI Machine Learning Repository](https://archive.ics.uci.edu/) | Datasets clásicos de ML y estadística, referencia académica (el iris, por ejemplo). | **Una por dataset** (iris: CC BY 4.0). | Gratis | Inglés | Viva |
| [IMDb non-commercial datasets](https://data.imdb.com/non-commercial-datasets/) | Ficheros TSV de películas, series y personas para practicar SQL y joins; refresco diario. | **Solo uso personal y no comercial** ([términos](https://data.imdb.com/non-commercial-datasets/)); no permite redistribuir. | Gratis | Inglés | Viva (URL nueva; la descarga vive en [datasets.imdbws.com](https://datasets.imdbws.com/)) |

## Aviso de IMDb

IMDb es el caso más restrictivo de la lista: sus datasets son **solo para uso personal y no
comercial**. Eso significa:

- no se publica el fichero, ni entero ni troceado, ni se redistribuye;
- no se usa como base de un dataset que se vaya a publicar;
- si se usa para practicar en local, se cita la fuente y se comprueba que el uso sigue siendo
  personal y no comercial.

Si un ejercicio necesita datos de cine para publicarse, se buscan antes en data.gov, datos.gob.es o
Kaggle con licencia compatible; IMDb no se copia.

## Cuándo usar cada uno

- **Practicar SQL y joins con datos variados**: Kaggle (con cuenta) o UCI.
- **Datos reales de España**: datos.gob.es, con licencia declarada en metadatos.
- **Datos reales de EE. UU.**: data.gov, leyendo la ficha de la agencia.
- **Texto e IA**: Hugging Face, filtrando por licencia e idioma.
- **Ejercicios de cine**: IMDb solo en local y para uso personal; nunca publicado.

Ninguno se copia al repositorio: los 10 CSV que hay en [`csv/`](csv/) son propios, sintéticos y
CC0-1.0. El criterio de admisión está en [`README.md`](README.md).
