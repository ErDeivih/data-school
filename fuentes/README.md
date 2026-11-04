# Fuentes — qué es este catálogo y cómo se lee

Esta carpeta guarda el **catálogo de fuentes** de Data School: una lista de recursos externos
(cursos, libros, documentación oficial, datasets y papers) que se han comprobado uno a uno para
poder **enlazarlos y resumirlos con palabras propias**. No es una biblioteca ni un repositorio de
material ajeno: aquí no se copia ni se aloja nada de terceros.

Ficheros:

| Fichero | Qué contiene |
|---|---|
| [`FUENTES.md`](FUENTES.md) | El catálogo verificado: 32 fuentes con licencia, coste, idioma, estado y tramo, más descartes y recuento. |
| [`POR-TRAMO.md`](POR-TRAMO.md) | Un principal y dos alternativas por tramo (F, DE, DS, AI), con el motivo de cada elección. |
| [`PLANTILLA-RESUMEN.md`](PLANTILLA-RESUMEN.md) | La plantilla obligatoria para dar de alta una fuente: campos, fórmula del resumen y puerta de entrada. |
| [`RESUMENES-EJEMPLO.md`](RESUMENES-EJEMPLO.md) | Diez fuentes reescritas con la plantilla, para ver el tono y el nivel de detalle. |
| `README.md` | Este documento: leyenda, reglas de entrada, clases de licencia y método de comprobación. |

Comprobación hecha el **2026-11-04 (UTC)**. Cada fila del catálogo lleva su fecha, su enlace y la
evidencia de la licencia; una fuente sin esa evidencia no entra.

## Cómo se lee la tabla de FUENTES.md

Cada columna responde a una pregunta distinta y no se mezclan:

- **Fuente**: enlace oficial. Es el único destino que se publica; el nombre va enlazado, no se
  reproduce el logotipo ni la portada.
- **Qué es y qué enseña**: resumen propio de una o dos líneas. Dice qué enseña y a quién sirve,
  nunca reproduce el temario.
- **Licencia**: la que consta por escrito, con enlace a la página o al `LICENSE` que lo prueba.
  «Sin licencia explícita» significa que no hay `LICENSE` ni términos de reutilización publicados:
  se puede recomendar y enlazar, no reutilizar. «Solo enlace» significa que el titular se reserva
  la copia y la redistribución.
- **Coste**: `gratis` · `gratis con cuenta` · `mixto, avisado` (parte gratis y parte de pago, y lo
  avisa antes de cobrar) · `de pago`. El coste no decide la licencia, pero sí la recomendación.
- **Idioma**: el del contenido, no el de la interfaz. Casi todo el catálogo está en inglés; lo que
  tiene traducción se anota.
- **Estado**: `viva` (responde y publica hoy) · `viva (rebrand)` (cambió de nombre o dominio y
  redirige) · `muerta` (cerró o redirige fuera del servicio).
- **Tramo**: `F` fundamentos · `DE` data engineer · `DS` data scientist · `AI` AI engineer ·
  `T` transversal.

## Reglas de entrada

1. **Enlace, licencia y fecha.** Todo recurso entra enlazado, con su URL oficial, su licencia
   declarada y la **fecha de última comprobación**. Sin fecha no hay fuente: caduca.
2. **Sin licencia o solo uso personal → `pending` y solo enlace.** Si no hay licencia explícita, o
   la licencia solo permite uso personal, la fuente se queda como enlace con resumen propio. No se
   copia texto, figura, temario ni PDF ajeno a este repositorio.
3. **De pago que avisa → se enlaza marcado.** Si el sitio deja claro el coste antes de cobrar
   (auditar gratis, plan Pro, suscripción), se enlaza con la marca «de pago» o «mixto, avisado».
   **De pago que no avisa → fuera del catálogo.** No se anuncia como gratis algo que no lo es.
4. **Un principal y dos alternativas por tramo.** Más de eso no ayuda, aturde. El principal es la
   recomendación por cobertura, calidad y coste; las alternativas cubren otro enfoque o son de
   pago. La licencia no decide si una fuente se recomienda, solo qué se puede hacer con su
   contenido (ver [`POR-TRAMO.md`](POR-TRAMO.md)).
5. **El resumen es propio.** Se describe qué enseña y a quién sirve, con palabras propias y sin
   reproducir el temario.

## Clases de licencia (medidas el 2026-11-04)

Las 32 fuentes se agrupan en tres clases según lo que permiten hacer con su contenido:

| Clase | Nº | Qué permite | Fuentes |
|---|---|---|---|
| **Solo enlace + resumen propio** | **15** | Recomendar y enlazar; no copiar texto, figuras, temario ni PDF | roadmap.sh, DataTalksClub, Kaggle Learn, dbt Learn, Google Skills, Coursera, edX, DeepLearning.AI, fast.ai, YouTube, Docs de dbt, Python Data Science Handbook, ISLR, Mathematics for ML, IMDb |
| **Licencia por ítem** | **7** | Depende de cada dataset/paper: hay que leer la ficha antes de usarlo | Kaggle Datasets, Hugging Face Datasets, data.gov, datos.gob.es, UCI ML Repository, arXiv, Hugging Face Papers |
| **Reutilizables con atribución** | **9** | Citar o reutilizar respetando la licencia y la atribución | MIT OCW (CC BY-NC-SA), freeCodeCamp (solo su código, BSD-3), Docs de Python (PSF-2.0), PostgreSQL License, SQLite (dominio público), Apache Spark (Apache-2.0), Apache Airflow (Apache-2.0), DuckDB (MIT), Dive into Deep Learning (texto CC BY-SA + código MIT) |
| **Muerta** | **1** | — (descartada y sustituida) | Papers with Code |

Suma: 15 + 7 + 9 = **31 fuentes vivas** + 1 muerta = **32 comprobadas** (31 vivas + 1 muerta).

Matices que importan dentro de la tercera clase: MIT OCW es **no comercial** y compartir igual;
freeCodeCamp libera **solo el código**, no el currículo; Dive into Deep Learning separa texto
(CC BY-SA) de código; SQLite y arXiv no son «lo mismo»: SQLite es dominio público y cada paper de
arXiv lleva la licencia que eligió su autor.

## Corrección de recuento: la cifra «11» es errónea; la medida es 15

El apartado «Recuento» de `FUENTES.md` (línea final) dice **«11 fuentes con licencia restrictiva o
sin licencia explícita»**, pero su propia lista enumera **14**: DataTalksClub, roadmap.sh, Kaggle
Learn, dbt Learn, Coursera, edX, DeepLearning.AI, fast.ai, Docs de dbt, PDSH, ISLR, Mathematics for
ML, IMDb y YouTube. La medición hecha en esta carpeta da **15**: las 14 listadas más **Google
Skills**, que la tabla del propio `FUENTES.md` describe como «Contenido © Google: solo enlace» y que
la lista del recuento omite.

La cifra operativa es **15** (clase «solo enlace + resumen propio»). `FUENTES.md` ya se ha corregido
en la cabecera de esta sesión, pero su apartado «Recuento» sigue diciendo 11 y enumerando 14: la
discrepancia queda registrada y reportada, no escondida. Las otras dos clases sí cuadran con su
lista: 7 por ítem y 9 reutilizables.

## Cómo se comprueba

La comprobación es mixta: automática para los enlaces y manual para licencias y precios.

- **Enlaces**: `npm run check:links` (o `tools/comprobar-enlaces.ps1`, que además falla si hay
  caídos) recorre las URLs del catálogo con una petición HTTP real (código de estado, redirección
  final) y deja el informe en [`INFORMES/enlaces-2026-11-04.md`](../INFORMES/enlaces-2026-11-04.md).
  Resultado de la última pasada: **82 enlaces comprobados, 79 vivos y 3 redirigen, 0 caídos,
  0 bloqueados**. Un «redirige» no es un fallo: se anota el destino nuevo y se actualiza la URL.
- **Periódicamente**, sin GitHub Actions: `tools/comprobar-enlaces.ps1` es la puerta y
  `tools/programar-enlaces.ps1` registra una tarea semanal de Windows que la ejecuta sola (se lanza
  una vez; se quita con `-Quitar`). El informe fechado se sobrescribe cada día de ejecución.
- **Licencia y precio**: se leen a mano, por fuente, en su página de licencia o en el `LICENSE` del
  repositorio y en su página de precios. Esa lectura queda como enlace de evidencia en cada fila.
  El chequeo automático no puede decidir si una licencia permite reutilizar: eso se lee.
- **Altas nuevas**: pasan por [`PLANTILLA-RESUMEN.md`](PLANTILLA-RESUMEN.md) y su puerta; hay diez
  ejemplos hechos en [`RESUMENES-EJEMPLO.md`](RESUMENES-EJEMPLO.md).

## Material de terceros

El material de terceros **nunca se copia**. En este repositorio no hay temario, PDFs, figuras,
transcripciones ni capturas de las fuentes: solo enlaces y resúmenes propios. La clase de licencia
sirve para saber si algún día se puede citar algo (y cómo), pero la regla de trabajo es no hacerlo:
la fuente vive en su sitio, y aquí se enlaza.
