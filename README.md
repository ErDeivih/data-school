# Data School — la carpeta que aglutina todo

Aquí va **todo lo de datos e IA junto**: lo que había en Muestra, lo que era Data School,
y el material de Orca. Primero se reúne; después se decide qué se queda.

## Qué se trae aquí

| Origen | Qué aporta |
|---|---|
| `F:\Proyectos\ProyectoServidor\aprender` | el portal vivo: 438 conceptos en 13 fases, datasets, proyectos |
| `F:\Proyectos\ProyectoServidor\aprender\docs\data-school-import` | lo importado de Data School: 32 fuentes verificadas, comprobador de enlaces, sistema de diseño |
| `E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia` | el workspace archivado de Orca: 13 fases, 6 CSV, figuras |
| `C:\Users\David\orca\preview-data` | la vista previa de Orca |
| `F:\Proyectos\data-school` (esta carpeta) | el proyecto Data School original y esta consolidación |

## Estructura de esta carpeta

- `fuentes/` — el catálogo de fuentes con licencia, coste, idioma y estado (32 ya verificadas).
- `conceptos/` — los conceptos de datos e IA, con su definición, ejemplo, código y errores típicos.
- `proyectos/` — proyectos prácticos con su enunciado, nivel y criterio de terminado.
- `datasets/` — conjuntos de datos reales con licencia y para qué sirven.
- `investigacion/` — lo investigado: cómo lo hacen otros, APIs gratuitas, qué adoptamos.

## Reglas

- **Se enlaza y se resume, no se copia**: 11 de las 32 fuentes solo admiten enlace.
- Todo concepto lleva **código verificado** (ejecutado), no código de ejemplo sin probar.
- Todo dataset lleva **licencia** y **procedencia**.
- Nada de GitHub Actions. Commit local; push selectivo.

## Cómo arrancar

David pega el prompt de consolidación en un workspace con esta carpeta. El agente mide los cinco
orígenes, dice con números qué hay en cada uno, importa lo que falte y escribe `CONSOLIDACION.md`
con lo que se queda, lo que se descarta y por qué.