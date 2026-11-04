# Ficha del agente — Data School

**Id en el panel**: `data-school`
**Ruta**: `F:\Proyectos\data-school`
**Rama de trabajo**: `main`
**Familia de interfaz**: F (documentación) + A (panel)

## Misión

**Reunir en un solo sitio todo el material de datos e IA** —conceptos, fuentes, proyectos, datasets— cogiendo lo mejor de cada origen, y dejarlo de forma que sirva para aprender y para construir.

Data School dejó de ser un producto aparte: el portal es **Muestra**. Esta carpeta es **la casa del contenido**: el catálogo que alimenta al portal y el archivo del que se tira.

## Qué hay aquí y qué se hace

| Carpeta | Qué va | Estado 2026-11-04 |
|---|---|---|
| `fuentes/` | catálogo de fuentes con licencia, coste, idioma y estado, trío principal + alternativas por tramo y plantilla de alta | **32 fuentes** (31 vivas, 1 muerta) + plantilla y 10 ejemplos |
| `conceptos/` | conceptos de datos e IA, con definición, código ejecutado, figuras, evidencia de ejecución e índices de consulta y lectura | **459 conceptos** en 13 fases, 2 índices |
| `proyectos/` | proyectos prácticos con enunciado, nivel y criterio de terminado | **2 completos + 22 de catálogo + 8 labs + 4 fichas** (12 proyectos) |
| `datasets/` | conjuntos de datos con licencia y procedencia, ficha de uso y perfil verificado; los externos, enlazados | **10 CSV CC0-1.0** con ficha y verificación |
| `investigacion/` | cómo lo hacen otros, APIs gratuitas, qué adoptamos y qué no | 1 estudio + 23 ficheros + registro de diseño |
| `tools/` | comprobador de enlaces, puerta y programador periódico, medidor de orígenes y verificador de conceptos | 6 herramientas |

## La tarea de consolidar: hecha (2026-11-04)

**Medir los cinco orígenes, comparar con números e importar aquí lo que falte.** Lo medido está en
`INVENTARIO.md`; lo que se trae, de dónde y lo que se descarta, en `CONSOLIDACION.md`.

1. `F:\Proyectos\ProyectoServidor\aprender` — el portal vivo: **459 conceptos**, 13 fases, 13 CSV (10 de portal + 3 de proyectos), 22 proyectos.
2. `...\aprender\docs\data-school-import` — lo importado de Data School: **32 fuentes**, comprobador de enlaces, sistema de diseño.
3. `E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia` — el archivo de Orca: **438 conceptos** idénticos a 438 de la viva, 6 CSV idénticos, **0 salidas de ejecución**; solo aporta el registro del rediseño del portal.
4. `C:\Users\David\orca\preview-data` — vista previa de **otro** servicio (`opofuente`): 76 tablas y **0 filas de contenido**; no aporta nada.
5. `F:\Proyectos\data-school` — esta carpeta: estructura, catálogo de fuentes, sistema de diseño y comprobador.

Confirmado con números: **la viva va por delante** (459 vs 438 conceptos, +21; 22 vs 10 proyectos; 946 vs 0 salidas) y **los 6 CSV de Orca ya están en la viva** (6/6 con SHA-256 idéntico). No hay dos versiones de contenido entre las que elegir.

## Reglas

- **Los orígenes son de solo lectura.** No se escribe en el portal ni en el archivo de Orca: se lee y se trae aquí.
- Hay **otra sesión trabajando en el portal (Muestra)**. Si algo hay que cambiar allí, se anota en `CONSOLIDACION.md`; no se toca.
- **Se enlaza y se resume, no se copia**: **15** de las 32 fuentes solo admiten enlace (la cifra «11» de la primera sesión estaba mal medida; corregida en D-016).
- Todo concepto lleva **código ejecutado**, no código de ejemplo sin probar.
- Todo dataset lleva **licencia y procedencia**.
- Sin GitHub Actions. Commit local; push selectivo.

## Cómo trabajas

Lee y sigue `F:\EspacioCodigo\_flujo-dsh\PROTOCOLO-AUTONOMIA.md` y `DOCTRINA-CALIDAD.md`.
Nivel 1 decides solo, nivel 2 anotas en `DECISIONES.md`, nivel 3 preguntas y sigues con otra tarea.

## Estado de la sesión (2026-11-04, sesión 2)

Consolidación cerrada (`INVENTARIO.md`, `CONSOLIDACION.md`) y las 7 tareas del backlog ejecutadas:
comprobador periódico de enlaces, plantilla de fuentes, fichas y verificación de datasets, fichas
de proyecto de los CSV nuevos, cierre de descartes, orden de lectura por fase y figuras de apoyo.
Queda pendiente lo de nivel 3 (sincronización archivo ↔ portal) y las 10 fichas de proyecto P01–P10.
Mantenimiento: `tools/programar-enlaces.ps1` (semanal) y `tools/medir-origenes.ps1` al cambiar los
orígenes.

## Al terminar cada sesión

`ESTADO-AGENTE.md` con el formato del protocolo, incluida la línea `resumen:` en lenguaje llano.
