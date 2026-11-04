# Plan de ejecución en tandas

**Fecha:** 2026-11-02 · Cada tanda se cierra con una puerta ejecutable, no con una sensación.

El orden de abajo es el orden **temático**: primero la cadena matemática, después los proyectos.
Si tu prioridad es encontrar trabajo de data engineer, empieza por la tanda **T5** y deja T1–T3
para cuando tengas un proyecto en GitHub; el razonamiento está en §3.

---

## 1. Las seis tandas

### T1 · La cadena estocástica (4 páginas) — **hecha**

| | |
| --- | --- |
| Páginas | `movimiento-browniano` → `ecuaciones-diferenciales-estocasticas` → `lema-de-ito` → `valoracion-de-opciones` |
| Por qué en este orden | Cada una necesita la anterior: sin browniano no hay EDE, sin EDE no hay Itô, sin Itô no se entiende de dónde sale el −σ²/2 de la valoración |
| Ficheros | 4 ficheros en `contenido/f09/` + 4 filas en `CONTENIDO-TEMARIO.md` + recuento de la fase |
| Esfuerzo | 4 sesiones de 90 min (una página por sesión, con el código ejecutado) |
| Puerta | `node generar.mjs --validar` en verde y las cuatro páginas visibles en el portal con sus enlaces |
| Riesgo | Que la página de Itô se convierta en un tratado. Si pasa de 1 400 palabras de prosa, se recorta el ejemplo, no la definición |

### T2 · Griegas, volatilidad e indicadores (3 páginas + 3 enriquecimientos) — **páginas hechas, enriquecimientos pendientes**

| | |
| --- | --- |
| Páginas | `griegas-y-cobertura`, `volatility-drag`, `indicadores-tecnicos` |
| Enriquecer | `ratio-de-sharpe` (el umbral de sospecha), `alpha-decay` (edge y retirada), `generacion-de-senales` (indicadores como features, no como señales) |
| Esfuerzo | 3 sesiones de 90 min |
| Puerta | Las tres páginas validan; el ejemplo de cobertura resuelve el sistema con `np.linalg.solve` y el residuo de delta se imprime |
| Riesgo | Que `indicadores-tecnicos` parezca una apología. El tono tiene que ser el de «esto es lo que calcula, esto es lo que no puede saber» |

### T3 · Markov, Karhunen-Loève y la página de método (3 páginas) — **hecha**

| | |
| --- | --- |
| Páginas | `cadenas-de-markov` (F01), `expansion-karhunen-loeve` (F01), `medir-tu-progreso` (F00) |
| Esfuerzo | 3 sesiones de 90 min |
| Puerta | Validan; `medir-tu-progreso` aparece en el itinerario de entrada de `core` si se regenera |
| Riesgo | `expansion-karhunen-loeve` es la más difícil de las diez. Si no sale con un ejemplo numérico que se pueda seguir a mano, se deja en `avanzado` sin ejemplo y se marca como pendiente, en vez de rellenarla |

### T4 · Enriquecimientos y teoría de Instagram (0 páginas nuevas)

| | |
| --- | --- |
| Enriquecer | Los 13 de `01-NOTEBOOKLM.md` §5 + `entrevistas-de-datos` y `portfolio-y-proyectos` con el contraste junior/senior |
| Esfuerzo | 2 sesiones de 90 min (los enriquecimientos son párrafos, no páginas) |
| Puerta | `node generar.mjs --validar` y `node _comprobar-tildes.mjs` |
| Riesgo | El clásico: aprovechar para «reescribir» la página entera y romper lo que ya funcionaba. Se añade, no se sustituye |

### T5 · Honestidad temporal y capa A de proyectos (1 página + 3 datasets + 8 proyectos)

| | |
| --- | --- |
| Página | `correccion-point-in-time` en `contenido/f04/`: es el prerrequisito de PF-04 y de cualquier backtest honesto |
| Datos | `pedidos-clientes`, `eventos-pipeline`, `opciones-sinteticas` en `datos/generar-datasets.mjs`, con sus manifiestos |
| Código | `P11`–`P18` en `sitio/proyectos.js` **y** sus filas en `CLASIFICACION` (sin esto, `META` revienta) |
| Esfuerzo | 2 sesiones de 2 h |
| Puerta | `node _comprobar-proyectos-t35.mjs` y `t36`–`t38` en verde; `comparar()` devuelve `distingue: true` en los ocho; la pantalla muestra 18 proyectos |
| Riesgo | Que la rúbrica no distinga: si la entrega errónea puntúa casi igual que la de referencia, el criterio está mal escrito, no el proyecto |

### T6 · Capa B de portfolio (fuera del repositorio de la escuela)

| | |
| --- | --- |
| Proyecto | PF-01 completo, de la ingesta al panel, con README de ocho secciones |
| Esfuerzo | 3 semanas a 6-8 h por semana |
| Puerta | Alguien que no eres tú lo levanta desde cero siguiendo el README, sin preguntarte nada |
| Riesgo | El alcance. Si en la semana 2 no hay ingesta estable, se recorta el panel, no la ingesta |

---

## 2. Puertas comunes (copiar y pegar)

```sh
node generar.mjs --validar
node _comprobar-temario.mjs
node _comprobar-prerequisitos.mjs
node _comprobar-solapes.mjs
node _comprobar-tildes.mjs
node _generar-itinerarios.mjs && node _comprobar-itinerarios.mjs
```

Y si se toca `sitio/` o datos:

```sh
node _comprobar-proyectos-t35.mjs
node _comprobar-finalizacion.mjs
node _comprobar-file.mjs
npm run check:cloud
```

Las pruebas de navegador necesitan Chromium; las de `npm run check:cloud` no necesitan cuenta ni
secretos. No liberes el puerto 8788 matando procesos ajenos: los arneses usan puertos propios.

---

## 3. El orden alternativo (si tu prioridad es el empleo)

| Semanas | Qué | Por qué |
| --- | --- | --- |
| 1–3 | T5 + PF-01 | Un data engineer se contrata por un pipeline reproducible, no por saber Itô |
| 4–6 | PF-02 | El almacén dimensional es la segunda pregunta de toda entrevista |
| 7–8 | T4 (entrevistas y portfolio) | Con dos proyectos hechos, el contraste junior/senior se aprovecha de verdad |
| 9+ | T1–T3 | La matemática quant es un diferenciador, no un requisito del puesto |

Esta es la recomendación por defecto. La otra solo tiene sentido si tu objetivo real es quant
research o si el corpus de 300 vídeos es tu única fuente de motivación.

---

## 4. Qué significa «hecho» en cada tanda

No es que la página exista. Es que se cumplen las cuatro:

1. **Contrato:** la página valida y tiene las siete secciones.
2. **Comprensión:** puedes explicar el concepto sin leerlo, con el ejemplo numérico delante.
3. **Evidencia:** hay una prueba o una salida que demuestra lo que afirmas (un test, una captura,
   un `print` reproducible).
4. **Registro:** la fila de `05-TRAZABILIDAD.md` está en `cerrado` con la fecha.

Si falta la 2, has escrito una página, no has aprendido nada. El portal separa estado técnico de
progreso personal justo por esto: una lección marcada como leída no es una lección entendida.

---

## 5. Presupuesto total y qué se queda fuera

| Tanda | Sesiones | Horas |
| --- | --- | --- |
| T1 | 4 | 6 |
| T2 | 3 | 5 |
| T3 | 3 | 5 |
| T4 | 2 | 3 |
| T5 | 3 | 5 |
| T6 | 18 | 54 |
| **Total** | **33** | **≈ 78** |

Fuera del alcance de este plan, para que no se cuele por la puerta de atrás:

- Una fase F13 de derivados. Obliga a tocar generador, validador y navegación.
- Un motor de opciones en el portal. No es material de aprendizaje, es un producto.
- Traducir los seis PDFs. El material ya está en español; lo que falta es la página.
- Publicar el portfolio en abierto sin revisar datos y licencias. `03-FUENTES.md` marca cuáles
  permiten redistribución y cuáles solo uso personal.
