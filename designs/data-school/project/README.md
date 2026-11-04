# Data School — sistema de diseño

Academia de datos en una sola casa: **data engineer**, **data scientist** y **AI engineer**. El producto es un **índice maestro**: qué aprender, en qué orden, con qué recurso, con qué dataset y con qué proyecto demostrarlo. Este sistema cubre las tres familias de interfaz del proyecto (F documentación, A panel, B SaaS) con un solo vocabulario visual.

La marca es **editorial y técnica a la vez**: papel y serif para el catálogo, filas y filetes para la ficha de recurso, y un semáforo de estados propio del producto (vivo / caído / por revisar). Nada de degradados, nada de ilustraciones, nada de emoji.

## Principio de contenido

**Se enlaza y se resume, no se copia.** Cada recurso del catálogo muestra: qué es, quién lo hace, licencia, coste, idioma, estado del enlace y fecha de última comprobación. El texto que escribe Data School es propio y breve; el temario ajeno no se reproduce.

Estados, en las palabras del producto:

| Estado | Token | Cuándo |
|---|---|---|
| Comprobado | `verified` | El enlace responde y la licencia permite enlazarlo y resumirlo. Fecha visible. |
| Por revisar | `pending` | Vivo, pero falta confirmar licencia, idioma o coste. Se publica con la marca y una fecha de revisión. |
| Caído | `broken` | No responde, o la licencia prohíbe el uso previsto. **Se marca, no se oculta.** |

Un recurso de pago se enlaza solo si avisa de que es de pago; si no avisa, no entra. Un recurso sin licencia clara entra como `pending`, nunca como `verified`.

## Voz

- Frases cortas, en segunda persona y en presente: «este tramo demuestra que sabes orquestar».
- Do: nombrar el recurso, el tramo y el proyecto. Cifras concretas (semanas, horas, idioma, coste).
- Don't: superlativos de marketing, «aprende IA en 3 meses», mayúsculas de grito, emoji.
- Nombres propios tal como los escribe su dueño (dbt, DuckDB, Kaggle Learn, DataTalksClub); los títulos de recurso, en su idioma original.

## Fundamentos visuales

**Color.** Dos temas (claro y oscuro) y tokens semánticos, nunca colores sueltos. El fondo es papel (`surface`), la tarjeta sube un escalón (`surface-raised`) y los huecos (código, tabla, estado vacío) bajan a `surface-inset`. El azul `accent` marca acción, enlace y tramo activo; `accent-soft` es su fondo teñido. `on-accent` es el único color de texto sobre un relleno `accent`. El semáforo `verified` / `pending` / `broken` **solo** significa estado de fuente: no se usa como marca ni como decoración.

Contraste verificado (WCAG AA, calculado, no estimado): `ink` 15:1 claro / 16,4:1 oscuro sobre `surface`; `ink-muted` 5,96:1 / 8,6:1; `accent` como texto 6,19:1 / 8,68:1 y 5,54:1 sobre `accent-soft`; `on-accent` sobre `accent` 6,7:1 / 8,68:1; `verified` 6,97:1 / 10,5:1; `pending` 6,64:1 / 10,6:1; `broken` 7,09:1 / 9,14:1. `line-strong` pasa el 3:1 exigido a bordes de control (3,36:1 claro, 3,65:1 oscuro); `line` es decorativo y **no** debe usarse como borde de control.

**Tipografía.** Tres familias del sistema, sin ficheros de fuente: `serif` (Georgia) para los dos títulos (`display-xl`, `display`), `sans` para lectura e interfaz (`heading`, `body`, `small`, `label`) y `mono` para código y nombres de fichero. Ocho estilos en total. La etiqueta `label` va en MAYÚSCULAS con tracking 0,08em y solo para estados o cabeceras de tabla.

**Espacio.** Base 4px: `space-1` 4 · `space-2` 8 · `space-3` 12 · `space-4` 16 · `space-6` 24 · `space-8` 40. Relleno de tarjeta `space-4`; margen de página y separación de secciones `space-6`; portada `space-8`. Nada de valores intermedios inventados.

**Forma.** `radius-sm` 3px (etiquetas, inputs), `radius-md` 6px (tarjetas, botones, código), `radius-full` solo píldoras de filtro y discos de estado. Recto con una esquina suave: documentación técnica, no app de consumo.

**Elevación y foco.** Casi plano: el peso lo llevan los bordes. `shadow-sm` para tarjetas en reposo, `shadow-lg` para lo que flota (menú, diálogo, aviso de enlace caído). El foco de teclado es `focus-ring`: 2px del color del fondo y 2px de `accent` en `box-shadow`, nunca `outline` fino.

## Iconografía y activos

Todavía **no hay iconos ni logotipo**: el sistema se abre con la palabra «Data School» compuesta en `serif` con el estilo `display-xl`. Los iconos que se hagan irán en SVG de una sola tinta con `currentColor`, trazo 1,5px, retícula de 20px, y se subirán al grupo `Icons`. Hasta entonces: texto, nunca icono improvisado.

## Componentes

Aún **no hay componentes** en el bundle: este es el sistema mínimo que fija color, tipo, espacio, forma y estados antes de la primera pantalla. El primer lote que necesita el producto es: `LinkStatus` (píldora verified/pending/broken con fecha), `ResourceRow` (tipo · idioma · coste · licencia), `TramoCard` y `ProgressBar` (por ruta, por tramo, total). Se construirán como `window.DataSchool` cuando exista la primera pantalla.

## Cómo se consume

Los tokens se publican generados en `tokens.css` (tokens.css es del visor, no se edita a mano): `--surface`, `--surface-raised`, `--surface-inset`, `--line`, `--line-strong`, `--ink`, `--ink-muted`, `--accent`, `--accent-soft`, `--on-accent`, `--verified`, `--pending`, `--broken`, `--link`; familias `--font-serif`, `--font-sans`, `--font-mono`; `--space-*`, `--radius-*`, `--shadow-sm`, `--shadow-lg`, `--focus-ring`. El tema se cambia con el atributo de tema del visor (claro primero: es el fallback).

## Lo que el consumidor pone

El contenido del catálogo y sus estados. El sistema no decide qué recurso entra: decide cómo se ve un recurso vivo, uno por revisar y uno caído, y con qué contraste se lee su licencia y su fecha de comprobación.
