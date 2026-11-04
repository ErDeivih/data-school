# Backlog — Data School

Ordenado **por valor para el producto**, no por facilidad. La regla del protocolo: nunca menos de cinco tareas listas; una tarea bloqueada se marca y se sigue con la siguiente.

**Estado de la sesión (2026-11-04)**: hechas 1, 2 y 3; en curso la 6. La 4 (nivel 3) queda esperando la respuesta de David; la 5 no se puede cerrar sin ella.

## Resumen

| # | Tarea | Por qué vale | Nivel | Depende de | Estado |
|---|---|---|---|---|---|
| 1 | Verificar fuentes y escribir `FUENTES.md` | Sin fuentes comprobadas no hay catálogo ni modelo; descarta 1 muerta y 11 de licencia restringida | 1 | — | **hecho** 2026-11-04 |
| 2 | Crear el sistema de diseño antes de la primera pantalla | Fija color, tipo, espacio y estados; sin él las pantallas se improvisan | 2 | — | **hecho** 2026-11-04 |
| 3 | Investigación de producto: cómo presentan el catálogo roadmap.sh, DataTalksClub, Kaggle Learn y academias | Decide el modelo y la ficha de recurso con criterio, no por imitación | 1 | — | **hecho** 2026-11-04 |
| 4 | Resolver las 5 decisiones de la especificación | La primera decide el modelo entero; las otras cuatro deciden pantallas | 3 | — | **esperando decisión** |
| 5 | Modelo de datos mínimo: rutas · tramos · recursos · proyectos · datasets · progreso | Desbloquea todas las pantallas y el comprobador | 2 | 4 | bloqueada por 4 |
| 6 | Comprobador de enlaces con fecha de comprobación | Es el riesgo nº 1 y el hueco que nadie cubre; entra en la puerta de toda pantalla | 1 | — | **en curso** |
| 7 | Asignar principal + dos alternativas por tramo en `FUENTES.md` | La especificación prohíbe veinte recursos por tramo: hay que decidir el trío | 1 | — | **lista** |
| 8 | Fichas de 3 datasets de muestra con licencia y uso | Los datasets son una de las cinco piezas y su licencia es un caso real | 2 | — | **lista** |
| 9 | Fichas de 6 proyectos de muestra con criterios de terminado | Es lo que demuestra un tramo; sin proyectos no hay progreso que medir | 2 | — | **lista** |
| 10 | Plantilla de resumen propio de recurso (voz y límites) | Evita copiar temarios por accidente: la regla de oro necesita forma | 2 | — | **lista** |
| 11 | Ficha de recurso (pantalla 4) con estados vivo/por revisar/caído | Primera pantalla con valor propio y con el estado «enlace caído» | 2 | 5, 6 | pendiente |
| 12 | Lista de rutas y ficha de ruta (pantallas 2 y 3) | El itinerario es el producto | 2 | 5 | pendiente |
| 13 | Portada (pantalla 1) con «qué toca hoy» y estado vacío | Puerta de entrada; depende del sistema de diseño | 2 | 5, 2 | pendiente |
| 14 | Catálogos de proyectos y datasets (pantallas 5 y 6) | Cierra las dos piezas de práctica | 2 | 5 | pendiente |
| 15 | Mi progreso (pantalla 7) | Cierra el ciclo: qué está pendiente y qué demostrado | 2 | 11-14 | pendiente |
| 16 | Auditoría de accesibilidad + gate de diseño por pantalla | La especificación exige puerta antes de dar una pantalla por buena | 1 | 11 | pendiente |

**Tareas listas ahora**: 6 (en curso), 7, 8, 9, 10 → cinco, cumple la regla del protocolo.

## Detalle de las tareas vivas

### 6. Comprobador de enlaces con fecha de comprobación (en curso)

- **Entregable**: `tools/check-links.mjs` (extrae enlaces de Markdown, los comprueba, clasifica vivo/redirige/bloqueado/caído y escribe un informe fechado en `INFORMES/`) + pruebas de extracción y clasificación (`npm test`, sin dependencias) + primer informe sobre `FUENTES.md`.
- **Por qué ahora**: no necesita el modelo de datos, es Nivel 1 y desactiva el riesgo que la propia especificación llama «el catálogo se pudre en meses». Además sirve de puerta antes de cada pantalla (puerta nº 2).
- **Terminado cuando**: las pruebas pasan, el informe marca los caídos/redirigidos sin mentir y `FUENTES.md` gana su fecha de comprobación verificable.
- **Hallazgo ya conocido**: los sitios que bloquean bots (Cloudflare, reCAPTCHA) no se pueden declarar «vivos» ni «caídos» sin más; el informe los marca como `bloqueado` con su código y no se borra la fuente por eso.

### 7. Principal + dos alternativas por tramo

- **Entregable**: en `FUENTES.md`, una tabla por tramo (F, DE, DS, AI) con **un principal y dos alternativas**, y el motivo de cada elección en una línea.
- **Terminado cuando**: los 4 tramos tienen trío y ninguna fuente con licencia restringida aparece como principal.
- **Nivel**: 1 (es ordenar datos ya verificados; no cambia alcance).

### 8. Fichas de 3 datasets de muestra

- **Entregable**: `DATOS.md` o sección de muestra con licencia, tamaño, dominio, dificultad, para qué proyecto sirve y **criterio de admisión** (dataset con licencia «Unknown» no entra; IMDb solo uso no comercial).
- **Terminado cuando**: los 3 datasets elegidos tienen licencia comprobada y un proyecto asignado.
- **Nivel**: 2 (esquema/datos reversibles).

### 9. Fichas de 6 proyectos de muestra

- **Entregable**: enunciado, nivel, tramo, qué demuestra y criterios de terminado de 6 proyectos (2 por ruta), sin copiar enunciados ajenos.
- **Terminado cuando**: cada proyecto tiene sus criterios verificables y usa un dataset de la tarea 8.
- **Nivel**: 2.

### 10. Plantilla de resumen propio de recurso

- **Entregable**: una plantilla corta (qué es, qué enseña, para quién, qué no cubre, por qué entra) con un ejemplo hecho y un contraejemplo de copia. Va con el tono del sistema de diseño.
- **Terminado cuando**: 10 recursos de `FUENTES.md` se reescriben con la plantilla sin copiar una línea del original.
- **Nivel**: 2.

## Esperando decisión (Nivel 3)

**Tarea 4 — las cinco preguntas de la especificación.** Hace falta la respuesta de David, sobre todo la primera; no las decido yo porque cambian el producto:

1. ¿Tres rutas separadas o una sola con tres salidas? *(decide el modelo entero)*
2. ¿El progreso es por recurso, por tramo o por proyecto? *(decide la pantalla de progreso)*
3. ¿Los apuntes son texto propio dentro de la plataforma, o enlaces a un cuaderno externo? *(decide si hay editor)*
4. ¿Los datasets se enlazan o se descargan a un almacén local? *(decide coste de disco y mantenimiento)*
5. ¿El catálogo es privado o público? *(decide si hay cuentas)*

**Propuesta del agente** (se adopta si no hay respuesta, salvo en 1): 2) progreso por tramo demostrado con proyecto; 3) apuntes en enlace externo con nota corta propia; 4) enlazar, nunca alojar; 5) privado en la primera versión. La 1 no la puede decidir el agente porque define el producto.

- **Nivel**: 3 — se para y se pregunta. Mientras tanto, se sigue con la 6.

## Cómo se genera trabajo cuando el backlog baja de cinco

Tres fuentes, en este orden: **huecos de la especificación** (pantallas prometidas sin hacer, estados sin cubrir), **calidad del catálogo** (enlaces caídos, recursos sin licencia, tramos sin proyecto) y **competencia** (lo que hace bien el sector y aquí falta). Toda investigación termina en fichero con propuesta ejecutable de nivel 1 o 2; si cambia el alcance, es nivel 3 y se pregunta.
