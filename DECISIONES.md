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

## Decisiones que **no** toma el agente (nivel 3, esperando)

Las cinco de la especificación. La primera decide el modelo entero:

1. ¿Tres rutas separadas o una sola con tres salidas?
2. ¿El progreso es por recurso, por tramo o por proyecto?
3. ¿Los apuntes son texto propio dentro de la plataforma, o enlaces a un cuaderno externo?
4. ¿Los datasets se enlazan o se descargan a un almacén local?
5. ¿El catálogo es privado o público?

Propuesta del agente si no hay respuesta: 2) progreso por tramo demostrado con proyecto; 3) enlace externo con nota corta propia; 4) enlazar, nunca alojar; 5) privado en la primera versión. La 1 queda abierta.

## Descartado de momento (y por qué)

- **Copiar temarios, lecciones, PDFs o vídeos**: prohibido por la regla de oro y por las licencias verificadas en `FUENTES.md`.
- **Replicar el mapa de roadmap.sh**: su FAQ prohíbe redistribuir el contenido; se enlaza como referencia, no se rehace.
- **Usar las cifras de «más inscritos»** como criterio de calidad: la especificación lo prohíbe expresamente.
- **Alojar datasets en el repositorio**: licencias y tamaño; la especificación lo deja como pregunta, y la propuesta es enlazar.
