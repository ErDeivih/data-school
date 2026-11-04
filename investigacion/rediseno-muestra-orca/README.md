# rediseno-muestra-orca · registro de decisión del rediseño del portal Muestra

**Qué es.** El **único material exclusivo del archivo de Orca**
(`E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia\docs\diseno`) que se conserva en Data
School: el **registro de decisión del rediseño del portal Muestra**, fechado en **2026-11** y
contratado como `muestra:redesign-20261101-v1`. No es una copia del portal ni documentación del
producto: es la evidencia de qué se cambió, por qué, y qué fuentes lo justifican.

**10 ficheros, ~84 KB**, copiados el **2026-11-04** del archivo de solo lectura, respetando sus
subcarpetas `manifiestos/`, `origen/` y `recorridos/`.

---

## 1. Qué hay dentro

| Fichero | Qué es | Para qué sirve |
| --- | --- | --- |
| `REDISENO.json` | El registro completo ya fusionado (67 KB): contrato, sistema de diseño, alcance, fuentes, 39 páginas inventariadas, 3 recorridos, revisión y bloqueos | La evidencia entera en un solo fichero; es el que se cita |
| `REDISENO.base.json` | Los metadatos **autorados a mano** (14 KB), sin hashes: es la entrada de la fusión | Editar el registro sin regenerar la evidencia |
| `.rediseno-aplicado` | Marcador que dice que el rediseño está **aplicado en sitio** (`app.js`, `estilo.css`, `generar.mjs`) y que las capturas «after» son las vigentes | Que el arnés de capturas sepa qué fase fotografiar |
| `manifiestos/recorridos.json` | El manifiesto de los tres recorridos con los resultados observados paso a paso | reproducir qué se comprobó |
| `recorridos/J1.json` | Recorrido 1 · localizar un concepto y comprobar prerrequisitos — `passed` | Prueba de navegación, no de impresión |
| `recorridos/J2.json` | Recorrido 2 — `passed` | Ídem |
| `recorridos/J3.json` | Recorrido 3 — `passed` | Ídem |
| `origen/app.diff` | Diff aplicado a `sitio/app.js` | El cambio de código, legible línea a línea |
| `origen/estilo.diff` | Diff aplicado a `sitio/estilo.css` | El cambio visual, legible línea a línea |
| `origen/generar.diff` | Diff aplicado a `generar.mjs` | El cambio en el generador del portal |

**Los `.diff` son el registro de los cambios aplicados**: no hace falta el repositorio original para
saber qué se tocó. Los tres recorridos (`J1`–`J3`) pasaron, y las 39 páginas del inventario están
marcadas `kept`: el rediseño no elimina ninguna.

## 2. El contrato y en qué consiste el rediseño

`contract_id: muestra:redesign-20261101-v1` · `data_scope: synthetic` · `inventory_complete: true`.
Seis decisiones de alcance, todas en la capa de presentación:

1. **Cabecera con cinco destinos primarios** (Hoy, Ruta, Repaso, Progreso, Buscar); Método, Glosario
   y Pendientes bajan al pie en vez de competir con nueve enlaces de la misma jerarquía.
2. **Barra inferior móvil** de cinco destinos con icono y etiqueta, conservando los `href` que
   exigen las pruebas de armazón y navegación.
3. **Sección actual anunciada** con `aria-current="page"` en cabecera, barra y pie.
4. **Foco visible de 3 px** en los enlaces de navegación y **objetivos táctiles de 44 px** sin
   cambios.
5. **Lectura**: párrafos limitados a **72ch**, filete de 2 px en las tarjetas en lugar de sombra.
6. **Movimiento desactivado** con `prefers-reduced-motion: reduce`.

## 3. Las fuentes del diseño (no son opiniones)

El registro declara cuatro fuentes y qué se aplicó de cada una:

| Fuente | Qué se aplicó |
| --- | --- |
| **WCAG 2.2 · Target Size (Minimum) 2.5.8** | Mantener 44 px en barra inferior y enlaces: el mínimo legal es 24 px, el sistema ya usaba 44 |
| **MDN · `prefers-reduced-motion`** | Desactivar transiciones de navegación y tarjetas cuando el sistema pide menos movimiento |
| **Nielsen Norman Group · Progressive disclosure** | Cinco destinos primarios en la cabecera y el resto en el pie |
| **Practical Typography · Summary of key rules** | Longitud de línea de 60–75 caracteres; se fija 72ch |

## 4. Lo que NO se copia: las 156 capturas PNG (15,9 MB)

El archivo de Orca contiene `capturas/before/` y `capturas/after/` con **156 PNG, 15,88 MB**. **Se
quedan allí y no se copian**, por tres motivos:

1. **No son contenido de datos e IA.** Son capturas de la interfaz del portal Muestra; este archivo
   documenta *decisiones*, no sirve como fototeca de pantallas.
2. **El archivo de Orca es de solo lectura y no se toca.** No se mueve, ni se reduce, ni se
   reorganiza; su valor es ser el original intacto.
3. **Se pueden regenerar.** El marcador `.rediseno-aplicado` y el arnés
   `_probar-rediseno-capturas.mjs` existen justamente para volver a capturarlas cuando haga falta;
   copiar 16 MB de derivados no añade evidencia.

Por el mismo criterio tampoco se copian `manifiestos/capturas-before.json` ni
`manifiestos/capturas-after.json`: son los índices con `sha256` de esas 156 capturas que no están
aquí. Si algún día se necesitan, se leen del archivo original.

## 5. Límite conocido, dicho a propósito

`redesign_review` está marcado **incompleto**: `visual_reviewed: false` y `manifest_sha256: null`.
El bloqueo `b-visual-review` (severidad baja) lo explica: no hubo revisión visual humana ni
herramienta de comparación de imágenes operativa en ese entorno, así que la evidencia disponible son
los PNG con `sha256` y las métricas objetivas del manifiesto. Queda dicho aquí y no se disimula: el
registro documenta lo que se verificó, no lo que se deseaba haber verificado.
