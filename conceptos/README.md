# conceptos — contenido del portal Data School

## Qué es esta carpeta

Esta carpeta es el **archivo de solo lectura** del contenido didáctico del portal vivo de Data
School. Se importó el **2026-11-04** desde `F:\Proyectos\ProyectoServidor\aprender` (que no se
modificó: se leyó y se copió). Aquí no se genera contenido nuevo ni se sirve nada: es la copia de
consulta del temario, sus figuras y la evidencia de que los ejemplos se ejecutan.

Todo lo que hay dentro es **contenido propio del proyecto Data School**, escrito en el portal vivo.
No se copia material de terceros: cuando un concepto cita a alguien, la cita está en su campo
`fuentes` como referencia bibliográfica, no como texto reproducido.

El índice navegable, con una tabla por fase y las 459 filas de conceptos, está en
[INDICE.md](INDICE.md).

## Las 13 fases y sus 459 conceptos

| Fase | Nombre de la fase | Conceptos |
| --- | --- | ---: |
| f00 | Aprender a aprender | 14 |
| f01 | Fundamentos matemáticos | 41 |
| f02 | Inferencia y estadística | 26 |
| f03 | Python, SQL y herramientas | 42 |
| f04 | Ingeniería de datos | 61 |
| f05 | Exploración y series temporales | 29 |
| f06 | Machine learning clásico | 49 |
| f07 | Deep learning | 33 |
| f08 | LLMs e IA generativa | 22 |
| f09 | Finanzas cuantitativas | 61 |
| f10 | Algoritmos y estructuras | 32 |
| f11 | Ingeniería de software | 34 |
| f12 | Comunicación y carrera | 15 |
| **Total** | **13 fases** | **459** |

Los nombres de fase son los del portal (los declara `generar.mjs`). Dentro de cada concepto, el
campo `fase` del frontmatter es el número de fase (0–12), y la carpeta es `f00`–`f12`.

Por nivel: 81 conceptos básicos, 183 intermedios, 155 avanzados y 40 expertos. Por ruta, el
temario se clasifica con cinco códigos: `core` (núcleo), `de` (data engineering), `ds` (data
science), `quant` (quant / trading) y `alg` (algoritmos y software); un concepto puede pertenecer a
varias rutas.

## Estructura de ficheros

```
conceptos/
├── f00/ … f12/            459 ficheros .md (el temario, uno por concepto)
├── figuras/               370 ficheros .svg (las figuras ya renderizadas)
├── figuras-fuente/        350 ficheros .py (los scripts que generan esas figuras)
├── verificacion/          929 .py + 33 .sql + 1 .json (los ejemplos ejecutables)
│   └── salidas/           962 ficheros .txt (la salida real de cada ejemplo)
├── INDICE.md              tabla por fase: id | título | nivel | rutas | resumen
└── README.md              este fichero
```

Recuentos exactos medidos sobre esta carpeta:

| Zona | Ficheros | Detalle |
| --- | ---: | --- |
| `f00/` … `f12/` | 459 | 13 carpetas, solo `.md` |
| `figuras/` | 370 | plano, solo `.svg` |
| `figuras-fuente/` | 350 | plano, solo `.py` (sin `__pycache__` ni `.pyc`) |
| `verificacion/` | 1.925 | 929 `.py` + 33 `.sql` + 1 `.json` + 962 `.txt` en `salidas/` |

En `verificacion/`, la raíz guarda los 962 scripts y el manifiesto, y la subcarpeta `salidas/` los
962 volcados de texto. El total ocupa ~1,15 MB.

## Esquema del frontmatter

Cada `.md` empieza con un bloque YAML delimitado por `---` en la primera línea y otra línea `---`
que lo cierra. Los 459 ficheros lo tienen completo: no hay ninguno sin frontmatter. Los campos son:

| Campo | Tipo | Qué guarda |
| --- | --- | --- |
| `id` | texto | Identificador del concepto; coincide con el nombre del fichero sin `.md` |
| `titulo` | texto | Título legible del concepto |
| `fase` | entero | Número de fase, 0–12 (la carpeta es `f00`–`f12`) |
| `nivel` | texto | `básico`, `intermedio`, `avanzado` o `experto` |
| `rutas` | lista | Rutas a las que sirve: `core`, `de`, `ds`, `quant`, `alg` |
| `prerequisitos` | lista | `id` de los conceptos que conviene saber antes (vacía si no hay) |
| `tags` | lista | Etiquetas temáticas para buscar y repasar |
| `resumen` | texto | Una sola línea con la idea del concepto (el que usa INDICE.md) |
| `fuentes` | lista | Referencias bibliográficas citadas, como atribución; no es material copiado |

Ejemplo real (recortado) de `f00/como-estudiar.md`:

```yaml
---
id: como-estudiar
titulo: Cómo estudiar esto
fase: 0
nivel: básico
rutas: [core]
prerequisitos: []
tags: [estudio, metodo, memoria, habito]
resumen: Recuperar de memoria, repartir los repasos en el tiempo e intercalar temas: eso es estudiar.
fuentes: ["Ebbinghaus (1885), 'Über das Gedächtnis'", "Roediger y Karpicke (2006), ..."]
---
```

## Cómo se leen los bloques

El cuerpo de un concepto usa Markdown normal y, además, bloques propios del portal: una línea
`:::nombre`, contenido y una línea `:::` que cierra. Los que importan para leer el temario son
estos.

### `:::figura` — una figura, su pie y el script que la genera

```
:::figura
fichero: asimetria-y-curtosis-misma-media-distinta-forma
pie: Arriba, los dos primeros conjuntos estandarizados contra la campana de Gauss...
fuente: figuras/asimetria-y-curtosis-1.py
:::
```

- `fichero` es el nombre sin extensión de la figura: se lee en `figuras/<fichero>.svg`.
- `pie` es el pie de figura (una frase que explica qué mirar).
- `fuente` es la ruta del script que produjo la figura, relativa a la raíz del portal: el fichero
  correspondiente está en `figuras-fuente/`, con el mismo nombre base y extensión `.py`.

Hay **349 bloques `:::figura`** en los 459 conceptos. Los 349 `fichero` resuelven a un SVG de
`figuras/` (0 ausencias) y las fuentes resuelven a 347 scripts distintos de `figuras-fuente/`
(0 ausencias). Los 370 SVG incluyen 21 figuras que ningún bloque enlaza (variantes y material de
apoyo) y los 350 `.py` incluyen 3 módulos de apoyo que no son figuras (`comun.py`, `_medir.py`,
`_tanteo.py`).

### `:::parametros` — la tabla de variables de la fórmula

```
:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `X` | La variable aleatoria que estás describiendo | las de la variable | ... |
:::
```

Es una tabla Markdown de cuatro columnas: el símbolo, qué representa, en qué unidades va y qué
efecto tiene que suba. Sirve para leer una fórmula sin perderse en la notación. Hay **343 bloques
`:::parametros`**.

### `:::formula` — la fórmula en notación matemática

```
:::formula
γ₁ = E[(X − μ)³] / σ³        γ₂ = E[(X − μ)⁴] / σ⁴ − 3
:::
```

El contenido se escribe como líneas de notación matemática en texto plano. Hay **861 bloques
`:::formula`**.

### El código

Los ejemplos van en bloques de código cercados con tres acentos graves, con el lenguaje declarado
(`python` sobre todo, también `text`, `sql`, `bash`, `yaml`, `dockerfile`, `json` y `html`). Los
**459/459 conceptos** contienen al menos un bloque de código; en total hay **1.478 bloques**
(1.244 con lenguaje declarado: 1.037 `python`, 141 `text`, 47 `sql`, 7 `bash`, 6 `yaml`,
3 `dockerfile`, 2 `json` y 1 `html`; los otros 234 no declaran lenguaje). El código ejecutable de
cada concepto tiene su versión en `verificacion/`: el nombre del fichero es el `id` del concepto
seguido de `--NN` (`<concepto>--01.py`, `<concepto>--02.py`, …), y su salida real está en
`verificacion/salidas/<concepto>--NN.txt`. Son ejecutables 454 de los 459 conceptos (los otros 5 no
tienen bloque `python verificable`, ver «Cobertura»).

## Evidencia de ejecución: `verificacion/`

`verificacion/` es la prueba de que los ejemplos del temario se ejecutan y producen lo que dicen.
Contiene **1.925 ficheros** (~1,15 MB):

| Tipo | Ficheros | Qué es |
| --- | ---: | --- |
| `.py` | 929 | Los ejemplos de Python, uno por bloque ejecutable |
| `.sql` | 33 | Los ejemplos de SQL |
| `.json` | 1 | `manifiesto.json`, el índice de la verificación |
| `.txt` | 962 | La salida real de cada script, en `salidas/` |

Los scripts se nombran `<concepto>--NN.py` (o `.sql`) y cada uno tiene exactamente un volcado
`salidas/<concepto>--NN.txt`: 929 + 33 = 962 scripts y 962 salidas. No se copiaron `.pyc` ni
`__pycache__`; dentro de `conceptos/` no existe ninguno.

**Cobertura: 454 de 459 conceptos tienen código ejecutado con su salida.** La evidencia del portal
cubría **438** conceptos (913 scripts + 946 salidas): el verificador del portal no se había vuelto a
ejecutar después de añadir los 21 conceptos nuevos. Al consolidar se detectó el hueco y se ejecutaron
**los 16 conceptos nuevos que sí tenían bloque `python verificable`** (16 scripts y 16 salidas, 0
fallos) con el Python del sistema, el mismo que usa el portal. Los **5 conceptos sin bloque
ejecutable** son `fuentes-y-canales`, `rutas-de-aprendizaje`, `terminal-y-shell`,
`iam-y-permisos-cloud` y `certificaciones-de-datos`: su código es de shell, YAML o metadatos, que el
verificador del portal tampoco ejecuta por diseño.

La comprobación es reproducible (idempotente: solo ejecuta lo que no tiene evidencia):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/verificar-conceptos.ps1
```

## Procedencia y reglas

- **Origen:** contenido propio del proyecto Data School, escrito en el portal vivo
  (`F:\Proyectos\ProyectoServidor\aprender`). La fuente se trató como **solo lectura**: no se
  escribió ni se borró nada en ella.
- **Fecha de importación:** 2026-11-04.
- **Copia fiel:** los `.md`, `.svg`, `.py`, `.sql`, `.json` y `.txt` se copiaron byte a byte, sin
  reescribirlos. Solo `INDICE.md` y este `README.md` se generan a partir de ellos, y los 16 scripts
  y 16 salidas de los conceptos que el verificador del portal no cubría se ejecutaron aquí el
  2026-11-04 (ver «Cobertura» más arriba).
- **Sin material de terceros:** no se copia contenido de terceros. Las referencias del campo
  `fuentes` son citas de atribución, no texto reproducido.
- **Solo archivo:** esta carpeta no se usa para generar el portal; el portal se genera en su propio
  proyecto. Aquí se consulta.
