# Backlog — Data School

Ordenado **por valor para el producto**, no por facilidad. La regla del protocolo: nunca menos de cinco tareas listas; una tarea bloqueada se marca y se sigue con la siguiente.

**Estado (2026-11-04, sesión 2)**: la consolidación está hecha y las 7 tareas que quedaron en el backlog se han cerrado. Detalle en `CONSOLIDACION.md` y `DECISIONES.md` (D-020 a D-025).

## Hecho en esta sesión

| # | Tarea | Resultado |
|---|---|---|
| 1 | Comprobador periódico de enlaces | `tools/comprobar-enlaces.ps1` (puerta que falla con caídos) + `tools/programar-enlaces.ps1` (tarea semanal de Windows, sin GitHub Actions). Verificado: 82 enlaces, 0 caídos. |
| 2 | Plantilla de resumen de fuentes | `fuentes/PLANTILLA-RESUMEN.md` con campos y puerta, y `fuentes/RESUMENES-EJEMPLO.md` con 10 fuentes reescritas. |
| 3 | Fichas de datasets | `datasets/FICHAS.md` (10 fichas con licencia, procedencia, dificultad, uso y proyectos) y `datasets/VERIFICACION.md` con `data_profile` real: 10/10 cargan, 63/63 columnas y tipos, 0 nulos, 0 duplicados. Comprobador reproducible `datasets/_verificar-fichas.ps1` (85 criterios, verde). |
| 4 | Fichas de los 4 CSV nuevos | `proyectos/fichas/` con 4 fichas que cubren los 12 proyectos P11–P22, con criterios de terminado y rúbrica. |
| 5 | Cierre de `CONSOLIDACION.md` | Anexos A y B con descartes, rutas y tamaños; corrección 18→10 fichas pendientes; hallazgos del portal anotados (ventas-mensuales no es panel; verificación desfasada). |
| 6 | Orden de lectura por fase | `conceptos/INDICE-LECTURA.md`: 459 filas, 0 ciclos, 0 prerequisitos inexistentes. |
| 7 | Decisión sobre figuras de apoyo | `conceptos/figuras/LEEME.md`: 370 SVG = 349 en uso + 21 variantes/sonda; 3 módulos base documentados y conservados. |

## Listas ahora

| # | Tarea | Por qué vale | Nivel | Estado |
|---|---|---|---|---|
| 1 | Escribir las 10 fichas de proyecto que faltan (P01–P10) | Cierra la cobertura de los 22 proyectos; las 4 fichas actuales ya cubren P11–P22 | 2 | lista |
| 2 | Revisión trimestral de fuentes: licencias, precios y enlaces redirigidos | Las licencias y los precios cambian; el comprobador automático no los lee por ti | 1 | lista |
| 3 | Mapa concepto ↔ fuente del catálogo | Saber qué fuente del catálogo respalda cada concepto evita altas improvisadas y enlaza las dos carpetas | 2 | lista |
| 4 | Ampliar la cobertura en español | 30 de las 32 fuentes son en inglés; falta una cantera verificada en español para F y DS | 2 | lista |
| 5 | Ficha de 3 datasets externos con licencia (Kaggle, datos.gob.es, UCI) | Demuestra el criterio de admisión con material ajeno: enlazar, no copiar, y comprobar la licencia por ítem | 2 | lista |
| 6 | Unificar las puertas en `npm run verify` (tests + datasets + enlaces) | Una sola orden para la puerta previa al commit; hoy son tres comandos | 1 | lista |
| 7 | Revisar con el portal los 3 matices de los datasets (ventas no es panel; 3 columnas booleanas; `resultado` mixed) | Son datos del portal: aquí solo se documentan; si el portal los describe mal, hay que corregirlo allí | 2 | lista |

**Tareas listas ahora**: 1–7 (siete, cumple la regla de cinco).

## Esperando decisión (Nivel 3)

1. **¿Cómo se sincroniza este archivo con el portal Muestra?** ¿El portal consume esta carpeta como fuente o se sigue copiando a mano? Afecta al flujo entre dos proyectos. Mientras no se responda, la copia canónica es esta carpeta y el portal no se toca.
2. **¿Se publica este archivo tal cual** (conceptos completos, con código) o el portal es el único que publica? Es una decisión de alcance y de producto.
3. **Regenerar la verificación del portal** (`generar.mjs --ejemplos` + `verificar-ejemplos.ps1`) para que su `.verificacion` cubra los 459: aquí se ejecutaron los 16 huecos, pero la carpeta del portal sigue desfasada y no se toca desde esta sesión.
4. Las **4 decisiones de producto** de `ESPECIFICACION.md` (progreso, apuntes, datasets enlazados o locales, catálogo público o privado) son de la otra sesión; este archivo las resuelve solo para sí mismo.

## Cómo se genera trabajo cuando el backlog baja de cinco

Tres fuentes, en este orden: **huecos del catálogo** (fuentes sin resumen propio, datasets sin uso, proyectos sin criterios), **calidad del archivo** (enlaces caídos, evidencia de ejecución desfasada, figuras sin referencia) y **competencia** (lo que hace bien el sector y aquí falta). Toda investigación termina en fichero con propuesta ejecutable de nivel 1 o 2; si cambia el alcance, es nivel 3 y se anota.
