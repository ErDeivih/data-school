# Data School — la casa del contenido de datos e IA

Aquí está **todo el material de datos e IA junto**: los 459 conceptos del portal, las 32 fuentes
verificadas, los datasets con su licencia, los proyectos con su criterio de terminado y la
investigación de la que salen las decisiones. El producto que lo publica es **Muestra**; esta
carpeta es el **catálogo y el archivo** del que se tira.

Consolidación hecha el **2026-11-04** a partir de cinco orígenes. Lo medido y lo descartado, con
números, está en [`INVENTARIO.md`](INVENTARIO.md) y [`CONSOLIDACION.md`](CONSOLIDACION.md).

## Estructura

| Carpeta | Qué hay | Cuánto |
|---|---|---|
| [`fuentes/`](fuentes/) | Catálogo de fuentes comprobadas: licencia, coste, idioma, estado y tramo; y el trío principal + dos alternativas por tramo | **32 fuentes** (31 vivas, 1 muerta) |
| [`conceptos/`](conceptos/) | Los 459 conceptos en 13 fases, con su definición, código ejecutado, figuras y la evidencia de ejecución | **459 conceptos**, 350 fuentes de figura, 370 SVG, 1.925 ficheros de verificación |
| [`proyectos/`](proyectos/) | Los 2 proyectos completos (código, datos, verificación y criterios) y el catálogo de práctica | **2 completos + 22 proyectos + 8 laboratorios** |
| [`datasets/`](datasets/) | 10 datasets sintéticos propios con licencia CC0-1.0, checksum y generador; catálogo de los externos que solo se enlazan | **10 CSV** |
| [`investigacion/`](investigacion/) | Cómo presentan su catálogo seis plataformas, investigación del portal (NotebookLM, APIs, certificaciones…) y el registro del rediseño de Muestra | **1 estudio + 23 ficheros + 10 de diseño** |
| [`tools/`](tools/) | Comprobador de enlaces con pruebas (sin dependencias), medidor reproducible de los orígenes y verificador del código de los conceptos | 4 herramientas |
| [`designs/`](designs/) | Sistema de diseño (tokens, tema claro/oscuro y preview de componente) | 1 sistema |

## Documentos de la raíz

- [`ESPECIFICACION.md`](ESPECIFICACION.md) — qué es el producto y qué pantallas promete.
- [`AGENTE.md`](AGENTE.md) — ficha del agente: misión, reglas y cómo se trabaja.
- [`BACKLOG.md`](BACKLOG.md) — qué toca ahora y qué está esperando decisión.
- [`DECISIONES.md`](DECISIONES.md) — lo decidido con su motivo y lo que no decide el agente.
- [`INVENTARIO.md`](INVENTARIO.md) — medición de los cinco orígenes, con números.
- [`CONSOLIDACION.md`](CONSOLIDACION.md) — qué se trae, de dónde y qué se descarta.
- [`ESTADO-AGENTE.md`](ESTADO-AGENTE.md) — estado de la sesión para el panel.

## Reglas

- **Se enlaza y se resume, no se copia.** Las fuentes de terceros se enlazan; su licencia decide
  qué se puede citar y qué no. **15** de las 32 fuentes solo admiten enlace + resumen propio.
- **Todo concepto lleva código ejecutado**, no código de ejemplo: la prueba está en
  `conceptos/verificacion/` (913 `.py`, 33 `.sql` y 946 salidas).
- **Todo dataset lleva licencia y procedencia**: los 10 propios son CC0-1.0, sintéticos, con
  checksum SHA-256 y generador; los externos se enlazan y se comprueba su licencia por ítem.
- **La viva es la fuente de verdad del contenido.** El archivo de Orca era una foto anterior
  (438 conceptos, 6 CSV, 0 salidas de ejecución); no se pierde nada al no duplicarlo.
- **Sin GitHub Actions.** Pruebas y comprobaciones en local.
- **Commit local y push selectivo**: un solo push al final de la sesión.

## Cómo se comprueba

```powershell
npm test                  # pruebas del comprobador de enlaces (Node 20+, sin instalar nada)
npm run check:links       # comprueba fuentes e investigación y escribe INFORMES/enlaces-<fecha>.md
powershell -NoProfile -ExecutionPolicy Bypass -File tools/medir-origenes.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verificar-conceptos.ps1   # ejecuta el código sin evidencia
```

La medición de los orígenes y el informe de enlaces de esta consolidación están en
[`INFORMES/`](INFORMES/).
