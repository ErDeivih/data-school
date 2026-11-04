# investigacion · qué se investigó y para qué sirve

**Qué es esta carpeta.** La investigación de producto que sostiene las decisiones de Data School:
cómo presentan su catálogo otras plataformas, qué se adoptó, y todo el trabajo previo de integración
de fuentes externas del portal. No es documentación del producto ni material que se publique: es el
trabajo que hace que cada idea acabe en un `id` del temario, en una ficha o en un proyecto con
rúbrica, sin entrar dos veces ni quedarse en un cajón.

Fecha de esta importación: **2026-11-04**. Origen: portal vivo `aprender`, leído en solo lectura.

---

## (a) `INVESTIGACION.md` — cómo presentan su catálogo otras plataformas

Estudio comparado de **seis plataformas** —roadmap.sh, DataTalksClub (DE Zoomcamp), Kaggle Learn,
DataCamp, Dataquest y Maven Analytics— **más Mode/ThoughtSpot como contraste**: qué ordena cada una,
qué prerrequisitos declara, qué metadatos pone en la ficha y cuánto cuesta. Cierra con dos tablas
que son la decisión de producto: **qué se adopta** (doble eje rol + habilidad, aristas
`requiere`/`prepara`, ficha normalizada, esfuerzo real, certificado verificable, comprobador de
enlaces propio) y **qué no se copia** (temarios, grafos y taxonomías ajenas).

**Para qué sirve:** fijar cómo se presenta el catálogo de Data School sin inventar un orden ni
copiar el de nadie, y detectar el hueco que nadie cubre (enlaces muertos con fecha visible).

---

## (b) `integracion/` — 23 ficheros de investigación del portal

El paquete de trabajo para meter en la academia el conocimiento que ya existe fuera —seis informes
de NotebookLM sobre ~300 vídeos, publicaciones de Instagram con proyectos y teoría, y fuentes de
datos nuevas— **sin romper el contrato de contenido**. Recuento exacto: **12 documentos numerados
(`00`–`11`) + `anexos/` con 3 markdown + `capturas/` con 8 PNG = 23 ficheros**.

| Fichero | Qué contiene | Para qué sirve |
| --- | --- | --- |
| `00-LEEME.md` | El encargo completo: qué se integra, con qué reglas y en qué orden | Puerta de entrada al paquete; se lee antes que nada |
| `01-NOTEBOOKLM.md` | Los seis informes de NotebookLM: qué aporta cada uno, qué es redundante, cuánto es nuevo | Convertir 300 vídeos en material del temario sin duplicarlo |
| `02-PROYECTOS.md` | Las dos capas de proyecto —capa A (dentro de la academia, con rúbrica) y capa B (portfolio en GitHub)— y cómo se encadenan | Que un proyecto enseñe un gesto y a la vez demuestre que sabes trabajar |
| `03-FUENTES.md` | Fuentes que faltan para data engineering, con la regla de 6–8 fuentes activas como máximo | Elegir fuentes sin coleccionarlas |
| `04-PLAN.md` | Plan de ejecución en seis tandas, cada una cerrada con una puerta ejecutable | Ordenar el trabajo y saber cuándo una tanda está hecha |
| `05-TRAZABILIDAD.md` | Una fila por fuente con destino y estado (`cerrado`, `pendiente Tn`, `descartado`, `roto`) | Saber de dónde sale cada cosa y qué se descartó y por qué |
| `06-COBERTURA.md` | Medición de qué falta de verdad en los 450 conceptos y 13 fases, contrastado con modelos de referencia | Contestar «¿está todo el mundo de los datos?» sin vender humo |
| `07-CERTIFICACIONES.md` | Certificaciones por nivel: qué sacar, cuándo, coste aproximado y requisito | Ordenar el gasto: primero gratis, y el examen después del proyecto |
| `08-PROYECTOS-DEL-MUNDO.md` | Proyectos que ya existen en el mundo y el criterio de «idea validada» | No inventar proyectos que no tengan sentido |
| `09-APIS-GRATUITAS.md` | APIs sin suscripción probadas el 2026-11-02: clave, límite y proyecto al que sirven | Datos reales para los proyectos sin tarjeta ni sorpresas |
| `10-F1-PREDICCION.md` | Guía de los proyectos P18/P19: qué se puede predecir de F1, dónde se rompe la honestidad | Base de los proyectos de clasificación y undercut |
| `11-LEER-CODIGO.md` | Lectura paso a paso de PF-01 y PF-02, script a script | Aprender leyendo código terminado, no solo escribiéndolo |
| `anexos/` (3 md) | Material bruto del que salieron `01` y `03`: inventario de los seis PDFs (33 módulos, 93 conceptos, 29 huecos) y la investigación de fuentes completa | Consultar el detalle cuando la versión curada no basta |
| `capturas/` (8 PNG) | Capturas de apoyo (gráficos, paneles, pantallas del portal) citadas por los documentos | Ver la evidencia que los documentos referencian |

---

## (c) `rediseno-muestra-orca/` — registro de decisión del rediseño del portal Muestra

**El único material exclusivo del archivo de Orca** que se conserva aquí: 10 ficheros con el
contrato `muestra:redesign-20261101-v1` — alcance del rediseño, decisiones por página, recorridos
verificados, manifiestos y los `.diff` aplicados.

**Para qué sirve:** reconstruir por qué el portal Muestra se ve como se ve, qué se cambió en
`app.js` / `estilo.css` / `generar.mjs` y qué evidencia lo respalda. El detalle y el motivo de lo que
**no** se copia (las 156 capturas PNG) están en
[`rediseno-muestra-orca/README.md`](rediseno-muestra-orca/README.md).

---

## Reglas de esta carpeta

- **Orígenes en solo lectura.** Todo se copió del portal vivo `aprender` y del archivo de Orca sin
  escribir en ellos; aquí se conserva la estructura de origen (`anexos/`, `capturas/`,
  `manifiestos/`, `origen/`, `recorridos/`).
- **Sin texto de terceros.** Los documentos son propios del proyecto; las fuentes ajenas se enlazan
  y se resumen, no se redistribuyen.
- **Sin git.** La importación no toca el historial.
