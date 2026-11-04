# Decisiones — Data School

Aquí se anotan las decisiones de **nivel 2** (el agente decide y lo deja escrito, con motivo) y los descartes de nivel 1 que conviene poder auditar. Las de nivel 3 no se toman: se preguntan y se anotan en `BACKLOG.md`.

Fecha de la sesión: **2026-11-04**.

| ID | Decisión | Motivo | Nivel | Reversible |
|---|---|---|---|---|
| D-001 | El sistema de diseño se crea **antes** de la primera pantalla, con dos temas (claro/oscuro), 13 colores semánticos + alias `link`, 8 estilos de texto en 3 familias del sistema, 6 espacios, 3 radios, 2 sombras y anillo de foco | No había marca previa y la especificación exige el sistema antes de cualquier pantalla; improvisar colores después cuesta más | 2 | sí (tokens) |
| D-002 | El sistema de diseño vive en `designs/data-school/` **dentro del repositorio**, no en un diseño externo | Es un entregable del proyecto y se versiona con el código; el visor genera sus ficheros de servidor y están ignorados por git | 2 | sí (mover carpeta) |
| D-003 | Se descarta **Papers with Code** y se sustituye por **Hugging Face Papers** | Comprobado el 2026-11-04: todo el dominio responde 302 a `huggingface.co/papers/trending`; mantenerlo sería un enlace muerto desde el día uno | 1 | sí (dato) |
| D-004 | Regla de licencias del catálogo: licencia clara → `verified`; sin licencia explícita o solo uso personal → `pending` y **solo enlace**; de pago que avisa → se enlaza marcado; de pago que no avisa → fuera | La regla de oro es «se enlaza y se resume, no se copia», y los derechos de autor no admiten «ya veremos»; `pending` permite publicar sin mentir | 2 | sí (dato) |
| D-005 | Se añaden `package.json` **sin dependencias** y `tools/check-links.mjs` con Node 20+ (fetch nativo) | El riesgo nº 1 de la especificación es que el catálogo se pudra; no existía comprobador y no hace falta instalar nada en el sistema | 2 | sí (borrar `tools/`) |
| D-006 | Un enlace `bloqueado` (401/403/429) **no** se declara caído | Kaggle, DataCamp y Coursera bloquean bots; marcarlo muerto sería inventar. Se deja para revisión manual con su código | 1 | sí |
| D-007 | Los datos no comprobados se marcan «no comprobado» y **no se usan para decidir**: precios de DataCamp, Dataquest y los packs de roadmap.sh, y las cifras de captura archivada | La investigación vale por lo verificado; un número de una captura de 2026 no es un dato de hoy | 1 | sí |
| D-008 | El sistema de diseño **no lleva componentes todavía**; el primer lote (LinkStatus, ResourceRow, TramoCard, ProgressBar) se construirá con la primera pantalla | Un sistema mínimo sin productos que lo consuman se llena de componentes inventados; mejor crecerlo con uso real | 2 | sí |
| D-009 | Se trabaja en `main`, sin abrir ramas | Lo pide el encargo de la sesión; abrir rama es nivel 3 (cambio de flujo de trabajo) | 1 | sí |
| D-010 | La carpeta se organiza en `fuentes/`, `conceptos/`, `proyectos/`, `datasets/` e `investigacion/`; los documentos de producto (`ESPECIFICACION`, `AGENTE`, `BACKLOG`, `DECISIONES`, `ESTADO`) se quedan en la raíz | Es la estructura que ya define `AGENTE.md`; separa catálogo de contenido de los documentos de gestión | 2 | sí (mover carpetas) |
| D-011 | Se importan los **459** conceptos de la viva, no los 438 de Orca | Superconjunto verificado con hash: 438/438 idénticos + 21 nuevos, 0 conceptos solo-en-Orca, y 459/459 con código | 2 | sí (borrar ficheros) |
| D-012 | Se versionan las **370 figuras SVG** (20,58 MB) además de sus **350 fuentes `.py`**; los 351 `.pyc` se descartan | 349 bloques `:::figura` referencian figuras; sin SVG el archivo queda ciego. Es material propio generado, no ajeno. Reversible con `git rm` | 2 | sí |
| D-013 | Se importa la evidencia de ejecución completa de `.verificacion/` (913 `.py`, 33 `.sql`, 946 salidas `.txt`; 1.893 ficheros) | Es la prueba de «todo concepto lleva código ejecutado»; sin las salidas no se puede auditar. Orca no las tiene | 2 | sí |
| D-014 | Los **10 datasets sintéticos propios** se alojan (CC0-1.0 con checksum SHA-256 y generador); los datasets externos (Kaggle, Hugging Face, data.gov, datos.gob.es, UCI, IMDb) se **enlazan**, nunca se copian | Licencia y procedencia verificables; los ajenos tienen licencia por ítem y no se redistribuyen | 2 | sí |
| D-015 | De Orca se trae **solo el registro de decisión del rediseño** (10 ficheros, ~90 KB: `REDISENO.json`, `REDISENO.base.json`, manifiestos, diffs y recorridos), no las 156 capturas (15,9 MB) | Es lo único exclusivo de Orca y no es contenido de datos e IA; las capturas son interfaz del portal y se quedan en el archivo | 2 | sí |
| D-016 | Se corrige de **11 a 15** el número de fuentes que solo admiten enlace | Conteo fila a fila de `FUENTES.md`: la clase «solo enlace» tiene 15; el propio documento enumeraba 14 y decía 11 | 1 | sí (dato) |
| D-017 | Una fuente «solo enlace» **puede** ser principal de un tramo; la licencia decide qué se puede copiar, no qué se puede recomendar | El producto enlaza; el criterio anterior («ninguna restringida como principal») confundía recomendación con copia. Se aplica en `fuentes/POR-TRAMO.md` | 2 | sí |
| D-018 | `C:\Users\David\orca\preview-data` no se importa | Medido: 4 ficheros, base SQLite de `opofuente` con 76 tablas y **0 filas de contenido**; no es el portal de datos | 1 | sí |
| D-019 | Se ejecutan aquí los **16 bloques `python verificable`** de los conceptos que el verificador del portal no cubría, y se guarda su salida en `conceptos/verificacion/` | La evidencia del portal cubría 438 de 459 conceptos (`.verificacion` desfasada tras añadir 21); sin este paso la regla «todo concepto lleva código ejecutado» no se cumpliría en 16. Ejecutado con el Python del sistema, 0 fallos. Reversible (borrar 32 ficheros) | 2 | sí |
| D-020 | La comprobación de enlaces pasa a ser **periódica en local**: `tools/comprobar-enlaces.ps1` (puerta, sale 1 si hay caídos) y `tools/programar-enlaces.ps1` (registra una tarea semanal de Windows, opcional, con `-Quitar`) | El riesgo nº 1 del catálogo es que se pudra; sin GitHub Actions la única vía es local. Se ofrece la tarea programada sin ejecutarla (cambiar el sistema es decisión de David) | 2 | sí |
| D-021 | Toda alta de fuente pasa por `fuentes/PLANTILLA-RESUMEN.md`, con sus campos y su puerta; se reescriben **10 fuentes** como muestra en `fuentes/RESUMENES-EJEMPLO.md` | Fija el tono y el nivel de detalle y evita copiar temarios por accidente; la plantilla incluye un contraejemplo de copia | 2 | sí |
| D-022 | Cada dataset tiene ficha homogénea de **licencia, procedencia, dificultad, uso y proyectos** (`datasets/FICHAS.md`) y una **verificación ejecutada** con `data_profile` (`datasets/VERIFICACION.md`) | La regla es «todo dataset lleva licencia y procedencia», y una ingesta sin probar es una hipótesis. Medido: 10/10 cargan, 63/63 columnas y tipos, 0 nulos, 0 duplicados. No se toca `datasets.json` (es del portal) | 2 | sí |
| D-023 | Se escriben las **4 fichas de proyecto** de los CSV nuevos (P11–P15, P17–P22); las **18 restantes** quedan en el backlog | Cierra el hueco de los CSV que no estaban en Orca sin inventar 18 fichas de golpe; las que hay tienen criterios de terminado verificables | 2 | sí |
| D-024 | Los **21 SVG sin `:::figura`** (20 variantes con tilde + `_probe_escalado.svg`) y los **3 módulos de apoyo** (`comun.py`, `_medir.py`, `_tanteo.py`) se conservan y se documentan en `conceptos/figuras/LEEME.md`; criterio de uso = tener bloque `:::figura` | Son variantes de figuras en uso y la base común de los 347 scripts; borrarlas rompería la regeneración. Coste pequeño, reversible | 2 | sí |
| D-025 | El **orden de lectura por fase** se deriva de `prerequisitos` con un orden topológico y desempate alfabético; es **recomendación**, no regla | 0 ciclos y 0 prerequisitos inexistentes, pero el orden no sustituye el criterio del que estudia. Se documenta el algoritmo para que sea reproducible | 2 | sí |

## Sesión de consolidación (2026-11-04)

- La decisión 1 de la especificación (**un tronco común y tres salidas**) ya está cerrada por David el 2026-11-04 y recogida en `ESPECIFICACION.md`; deja de figurar como pendiente.
- Se corrige la lista de pendientes: quedan **4** decisiones de producto (progreso, apuntes, datasets enlazados o locales, catálogo público o privado), no 5.

## Decisiones que **no** toma el agente (nivel 3, esperando)

Decisiones de producto que siguen abiertas para el portal (no para este archivo):

1. ¿El progreso es por recurso, por tramo o por proyecto?
2. ¿Los apuntes son texto propio dentro de la plataforma, o enlaces a un cuaderno externo?
3. ¿Los datasets se enlazan o se descargan a un almacén local?
4. ¿El catálogo es privado o público?

Propuesta del agente si no hay respuesta: 1) progreso por tramo demostrado con proyecto; 2) enlace externo con nota corta propia; 3) enlazar, nunca alojar; 4) privado en la primera versión.

### Dudas de nivel 3 abiertas por la consolidación

5. **¿Cómo se sincroniza esta carpeta con el portal (Muestra)?** ¿El portal la consume como fuente, o se sigue copiando a mano? Afecta al flujo entre dos proyectos y a quién manda cuando cambian. **No se decide aquí**; mientras tanto, la copia canónica del contenido pasa a ser esta carpeta y el portal no se toca.
6. **¿Se publica este archivo tal cual** (conceptos completos, incluido el código) o el portal es el único que publica? Es una decisión de alcance y de producto, no de contenido.
7. **Diferencia de versiones entre viva y Orca en código de portal** (`app.js`, `estilo.css`, `proyectos.js`, `plan-hoy.js` difieren): no es contenido de datos y no se decide desde aquí; la otra sesión es la dueña del portal.

## Descartado de momento (y por qué)

- **Copiar temarios, lecciones, PDFs o vídeos**: prohibido por la regla de oro y por las licencias verificadas en `FUENTES.md`.
- **Replicar el mapa de roadmap.sh**: su FAQ prohíbe redistribuir el contenido; se enlaza como referencia, no se rehace.
- **Usar las cifras de «más inscritos»** como criterio de calidad: la especificación lo prohíbe expresamente.
- **Alojar datasets en el repositorio**: licencias y tamaño; la especificación lo deja como pregunta, y la propuesta es enlazar.
