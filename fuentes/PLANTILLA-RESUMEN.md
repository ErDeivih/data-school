# Plantilla de resumen de fuentes

Para añadir una fuente nueva al catálogo **sin improvisar** cada vez. Toda alta pasa por esta
plantilla y por las reglas de [`README.md`](README.md); el resultado se añade a [`FUENTES.md`](FUENTES.md)
y, si toca, a [`POR-TRAMO.md`](POR-TRAMO.md).

## La regla que no se negocia

**Se enlaza y se resume; no se copia.** El resumen es tuyo: describe qué enseña y a quién sirve,
nunca reproduce el temario, la descripción oficial, los módulos ni los textos de la página. Si no
puedes resumir sin copiar, la fuente no entra.

## Campos obligatorios de una alta

| Campo | Cómo se rellena | Ejemplo |
|---|---|---|
| **Fuente** | Enlace oficial canónico, no un agregador ni un acortador | `https://docs.python.org/3/` |
| **Qué es** | Una frase: qué es el recurso, sin adjetivos de marketing | «La documentación oficial del lenguaje Python y su biblioteca estándar.» |
| **Qué enseña / para qué sirve** | Una frase: qué se aprende o qué se resuelve con él | «Es la referencia primaria para consultar sintaxis, módulos y comportamiento del lenguaje.» |
| **Para quién** | Tramo y perfil: F, DE, DS, AI o T; y si es principal, alternativa o apoyo | «F · apoyo permanente, no un curso.» |
| **Qué no cubre** | Límite honesto: lo que no vas a encontrar ahí | «No enseña estadística ni proyectos guiados.» |
| **Licencia** | Clase medida y enlace a la evidencia (LICENSE o página legal) | «PSF-2.0 · reutilizable con atribución.» |
| **Coste** | Gratis · gratis con cuenta · mixto (avisado) · de pago | «Gratis.» |
| **Idioma** | El del contenido, no el de la interfaz | «Inglés (traducción parcial al español).» |
| **Estado y fecha** | `viva` / `viva (rebrand)` / `muerta` + fecha `AAAA-MM-DD` de la comprobación | «viva · 2026-11-04.» |
| **Por qué entra** | Una frase de criterio: cobertura, calidad, coste o hueco que cubre | «No hay otra fuente primaria del lenguaje; es la que se consulta a diario.» |
| **Clase de licencia** | Solo enlace · por ítem · reutilizable con atribución (ver README) | «Reutilizable con atribución.» |

## Fórmula del resumen (dos frases, máximo)

1. **Qué es y qué enseña**: una frase sin adjetivos vacíos («increíble», «el mejor», «líder»).
2. **Para quién y qué no cubre**: una frase que ayude a descartarla cuando no toca.

Nada de listas de módulos, ni de «temario completo», ni de «certificación oficial» si no se ha
verificado la certificación. Los datos que no se han comprobado se marcan **«no comprobado»** y no
se usan para recomendar.

## Puerta antes de publicar una alta

- [ ] El enlace responde y se ha apuntado la redirección final si la hay.
- [ ] La licencia se ha leído en su fuente, no se ha supuesto por el dominio.
- [ ] La clase de licencia está asignada (solo enlace / por ítem / reutilizable).
- [ ] El resumen está en palabras propias y no reproduce la descripción oficial.
- [ ] Se ha pasado `npm run check:links` (o `tools/comprobar-enlaces.ps1`) y no hay caídos nuevos.
- [ ] No se ha copiado ningún fichero de la fuente al repositorio.

## Ejemplo correcto

> **Docs de SQLite** — La documentación oficial del motor SQL embebido más desplegado. Enseña el
> dialecto SQL de SQLite, sus tipos y su API desde el propio proyecto; sirve como referencia de
> consulta, no como curso guiado. Para F (SQL) y como apoyo de DE. No cubre SQL de servidor
> (PostgreSQL, MySQL) ni modelado. Licencia: dominio público. Gratis, inglés, viva (2026-11-04).
> Entra porque es la fuente primaria y la licencia permite citar sus ejemplos con atribución.

## Contraejemplo (lo que no se hace)

> **Mal:** «Curso con 12 módulos: introducción, instalación, variables, funciones, bucles, listas,
> diccionarios, ficheros, errores, clases, módulos y proyecto final. ¡El más completo!»

Eso es el temario copiado y una promesa de marketing: no dice qué se aprende a hacer, no dice a
quién sirve y no se puede comprobar. Si no hay forma de resumirlo sin copiar, se enlaza sin resumen
y se marca `pending`… o no entra.
