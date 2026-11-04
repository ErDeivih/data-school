# Backlog — Data School

Ordenado **por valor para el producto**, no por facilidad. La regla del protocolo: nunca menos de cinco tareas listas; una tarea bloqueada se marca y se sigue con la siguiente.

**Estado de la sesión (2026-11-04)**: la consolidación está hecha. Las tareas 1, 2, 3, 6, 7, 8 y 9 del backlog anterior se cerraron al importar el material; quedan las de abajo.

## Hecho en esta sesión

- Medición de los cinco orígenes con números (`INVENTARIO.md`) y plan de consolidación (`CONSOLIDACION.md`).
- Importados **459 conceptos** en 13 fases, **370 SVG** + **350 fuentes** de figura y **1.925 ficheros** de verificación (la evidencia del portal cubría 438 conceptos; se ejecutaron los 16 que faltaban, 0 fallos).
- Catálogo de **32 fuentes** con clases de licencia medidas y **principal + 2 alternativas por tramo** (`fuentes/POR-TRAMO.md`).
- **10 datasets** sintéticos CC0-1.0 con checksum verificado 10/10, manifiesto y generador; catálogo de los externos que solo se enlazan.
- **2 proyectos completos** y **catálogo de 22 proyectos + 8 laboratorios** (`proyectos/`).
- Investigación (`investigacion/`): estudio de plataformas, 23 ficheros de integración del portal y el registro de rediseño exclusivo de Orca.
- Puerta de enlaces: **82 comprobados, 79 vivos, 3 redirigen, 0 caídos**.
- Corregida la cifra de fuentes «solo enlace»: de 11 a **15** (D-016).

## Listas ahora

| # | Tarea | Por qué vale | Nivel | Estado |
|---|---|---|---|---|
| 1 | Repetir `npm run check:links` y `tools/medir-origenes.ps1` cuando cambien los orígenes | El catálogo se pudre si no se comprueba; la medición debe seguir siendo reproducible | 1 | lista |
| 2 | Plantilla de resumen propio para las 32 fuentes y reescribir 10 con ella | Evita copiar temarios por accidente: la regla de oro necesita forma | 2 | lista |
| 3 | Ficha de dificultad y uso para cada uno de los 10 datasets (filas, columnas, preguntas que permite) | El dataset sin «para qué sirve» no ayuda a elegir proyecto | 2 | lista |
| 4 | Cuatro fichas de proyecto para los 4 CSV nuevos de la viva (`cartera-acciones`, `f1-clasificacion`, `futbol-partidos`, `telemetria-f1`) | El catálogo tiene proyectos P11–P22 para ellos, pero faltan criterios de terminado escritos | 2 | lista |
| 5 | Decidir qué hacer con los 21 SVG que ningún `:::figura` enlaza y con `comun.py`/`_medir.py`/`_tanteo.py` | Material de apoyo sin dueño: o se documenta para qué está o se retira | 2 | lista |
| 6 | Índice de lectura por fase (orden recomendado dentro de f00–f12) a partir de `prerequisitos` | El temario existe, pero no dice por dónde empezar dentro de cada fase | 1 | lista |
| 7 | Comprobar con `data_profile` que los 10 CSV cargan y que sus tipos coinciden con `datasets.json` | La puerta de datos del protocolo; una ingesta que no se ha probado es una hipótesis | 1 | lista |

**Tareas listas ahora**: 1–7 (siete, cumple la regla de cinco).

## Esperando decisión (Nivel 3)

1. **¿Cómo se sincroniza este archivo con el portal Muestra?** ¿El portal consume esta carpeta como fuente o se sigue copiando a mano? Afecta al flujo entre dos proyectos y a quién manda cuando cambian. Mientras no se responda, la copia canónica del contenido es esta carpeta y el portal no se toca.
2. **¿Se publica este archivo tal cual** (conceptos completos, con código) o el portal es el único que publica? Es una decisión de alcance y de producto.
3. **¿Cómo se regenera la verificación del portal** (`generar.mjs --ejemplos` + `verificar-ejemplos.ps1`) para que su `.verificacion` cubra los 459? Aquí se ejecutaron los 16 huecos, pero la carpeta del portal sigue desfasada y no se toca desde esta sesión.
4. Las **4 decisiones de producto** que siguen abiertas en `ESPECIFICACION.md` (progreso, apuntes, datasets enlazados o locales, catálogo público o privado) son de la otra sesión; este archivo las resuelve solo para sí mismo.

## Cómo se genera trabajo cuando el backlog baja de cinco

Tres fuentes, en este orden: **huecos del catálogo** (fuentes sin resumen propio, datasets sin uso, proyectos sin criterios), **calidad del archivo** (enlaces caídos, evidencia de ejecución desfasada, figuras sin referencia) y **competencia** (lo que hace bien el sector y aquí falta). Toda investigación termina en fichero con propuesta ejecutable de nivel 1 o 2; si cambia el alcance, es nivel 3 y se anota.
