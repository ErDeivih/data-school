# Integración de fuentes externas en Muestra — paquete de trabajo

**Fecha:** 2026-11-02 · **Rama de trabajo:** `codex/regresion-navegadores` · **Estado:** parte ya integrada y validada el 2026-11-02: las doce páginas previstas están escritas y el temario en 450 conceptos.

Este paquete responde a un encargo concreto: meter en la academia el conocimiento que ya
existe fuera de ella (seis informes de NotebookLM sobre un corpus de ~300 vídeos, doce
publicaciones de Instagram con proyectos y teoría, y fuentes nuevas de datos) **sin romper el
contrato de contenido** del repositorio.

No es un resumen de los PDFs. Es el trabajo previo que hace falta para que cada idea acabe en
un `id` del temario, en una página que cumpla el contrato, o en un proyecto con rúbrica — y
para que nada entre dos veces ni se quede en un cajón.

---

## 1. Los documentos

| Documento | Qué contiene | Cuándo se usa |
| --- | --- | --- |
| [`01-NOTEBOOKLM.md`](01-NOTEBOOKLM.md) | Qué hay de verdad en los seis informes, qué ya cubre el temario, qué falta y la ficha de cada concepto nuevo | Antes de escribir cualquier página de la ruta quant |
| [`02-PROYECTOS.md`](02-PROYECTOS.md) | Catorce proyectos en dos capas: ocho micro-proyectos para la app y seis de portfolio con arquitectura y rúbrica | Al planificar el trimestre |
| [`03-FUENTES.md`](03-FUENTES.md) | Canales, webs, cursos y datos que no están en `RECURSOS.md`, con la fase a la que sirven | Cuando te aburras de tu propia lista |
| [`04-PLAN.md`](04-PLAN.md) | El orden de ejecución en tandas, con esfuerzo, criterio de cierre y comandos | Al empezar cada sesión de trabajo |
| [`05-TRAZABILIDAD.md`](05-TRAZABILIDAD.md) | Una fila por fuente y destino: de dónde sale cada cosa y en qué estado está | Para no perder el hilo entre semanas |
| [`06-COBERTURA.md`](06-COBERTURA.md) | Qué áreas cubre el temario, qué falta de verdad y qué no hace falta aprender | Cuando dudes si te falta algo |
| [`07-CERTIFICACIONES.md`](07-CERTIFICACIONES.md) | Certificaciones por nivel (gratis, básicas, medias, altas), con qué aprender en cada una | Antes de pagar un examen |
| [`08-PROYECTOS-DEL-MUNDO.md`](08-PROYECTOS-DEL-MUNDO.md) | Qué proyectos existen de verdad (foros, repos, documentación) y cuáles de los nuestros tienen precedente | Antes de empezar uno nuevo |
| [`09-APIS-GRATUITAS.md`](09-APIS-GRATUITAS.md) | APIs y datos abiertos sin suscripción, con estado de la prueba del 2026-11-02 | Al elegir fuente para un proyecto |
| [`10-F1-PREDICCION.md`](10-F1-PREDICCION.md) | Cómo predecir clasificación y carrera de F1 sin hacer trampa: datos, variables, métricas y plan | Antes de tocar P18 o P19 |
| [`11-LEER-CODIGO.md`](11-LEER-CODIGO.md) | Lectura paso a paso del código de PF-01 y P17 y el vocabulario de empresa con su página | Cuando quieras entender lo que ya está hecho |
| [`anexos/`](anexos/LEEME.md) | El inventario bruto de los PDFs (93 conceptos) y la investigación de fuentes sin curar | Cuando quieras el detalle que el resumen no recoge |

---

## 2. El estado real de la escuela (lo que he comprobado, no lo que promete la documentación)

| Dato | Valor comprobado |
| --- | --- |
| Conceptos en el temario | **458** (438 + las 20 páginas nuevas), todos con fichero |
| Fases | 13 (`f00` a `f12`), la fase del fichero tiene que coincidir con el `fase:` del frontmatter |
| Ruta quant (F09) | **54 conceptos**, centrados en trading sistemático, ejecución, riesgo y validación |
| Itinerarios | 10, dos por ruta, con su proyecto y entregable declarados |
| Proyectos implementados | **22** (`P01`–`P22`): 10 de currículo + 12 de F1, fútbol y cartera |
| Paquetes de datos | **10**: los 6 de siempre más F1, cartera, clasificación y fútbol |
| Contrato de página | frontmatter de 8 campos y 7 secciones fijas, validadas por `generar.mjs` |

La consecuencia importante: **la escuela no está vacía, está desequilibrada**. La ingeniería de
datos (F04, 54 conceptos) y la estadística (F02) están bien cubiertas; la mitad matemática de
la ruta quant no existe. Los seis informes de NotebookLM no rellenan huecos de data
engineering: rellenan un bloque entero que falta, el de **derivados y cálculo estocástico**.

---

## 3. Tres decisiones que he tomado y por qué

**1. Los PDFs no se copian, se convierten en fichas de página.**
Un informe de NotebookLM es un texto continuo con `$...$` de LaTeX, tablas rotas y código
suelto. Pegarlo en `contenido/` rompe el validador (no admite LaTeX ni HTML) y, peor, enseña
menos que una página escrita con el contrato delante. Por eso `01-NOTEBOOKLM.md` no transcribe:
extrae el concepto, decide si ya existe, y si no existe, redacta la ficha que hay que escribir.

**2. Los doce posts de Instagram no son doce proyectos.**
De los doce enlaces, **tres estaban rotos** (la publicación ya no existe) y **tres no tenían
contenido recuperable** (una línea de texto o un carrusel sin descripción). Los seis restantes sí
aportan: una lista de cinco proyectos de analista financiero, un criterio de diseño de paneles,
una fuente de datasets y tres listas de teoría. He separado lo que el post **dice de verdad** de
lo que es mi interpretación, y cada uno está fichado en `05-TRAZABILIDAD.md` con su estado.

**3. Primero el material, después las páginas… y luego las páginas.**
La primera entrega fue solo documentación: añadir 11 conceptos y 8 proyectos de golpe dejaba el
repositorio en rojo hasta que estuvieran las páginas y las rúbricas. Después se integraron las seis
que más valor tienen (ver §6), escritas con el contrato delante y validadas con
`node generar.mjs --validar`. Las otras cinco siguen como fichas listas para pegar, y los ocho
micro-proyectos esperan sus datasets y sus rúbricas.

---

## 4. Cómo se usa este paquete en la práctica

1. Abre [`04-PLAN.md`](04-PLAN.md) y elige la tanda. Cada tanda tiene un criterio de cierre
   medible, no una lista de deseos.
2. Si la tanda es de teoría, abre la ficha del concepto en [`01-NOTEBOOKLM.md`](01-NOTEBOOKLM.md),
   escribe la página con `COMO-ESCRIBIR-CONTENIDO.md` al lado y añade la fila al temario en el
   mismo cambio.
3. Si la tanda es de proyecto, abre [`02-PROYECTOS.md`](02-PROYECTOS.md), copia el objeto y
   ajusta datos e hitos a lo que de verdad puedas entregar esa semana.
4. Marca el avance en [`05-TRAZABILIDAD.md`](05-TRAZABILIDAD.md). Si un concepto se cae o se
   parte en dos, se anota ahí; el temario no se toca a mano sin pasar por ese registro.

---

## 5. Lo que este paquete no hace

- No decide por ti qué estudiar primero: eso ya lo hacen los itinerarios y la agenda.
- No sustituye a `RECURSOS.md` ni a `BIBLIOGRAFIA.md`; los complementa donde se quedan cortos.
- No valida los PDFs como fuente académica. Son apuntes de vídeo con notación irregular
  (`$EV$`, `$\sigma_B$`, tablas incrustadas). Todo lo que entra en una página se contrasta con
  una fuente citable antes de escribir la sección «Definición formal».

---

## 6. Qué está integrado ya en la escuela (2026-11-02)

Veinte páginas nuevas, validadas con `node generar.mjs --validar` y con las competencias y el
temario actualizados. Cada una se abre en el portal con su enlace, y desde ahí se llega a las
demás por los enlaces internos.

| Página | Fase | Enlace en el portal |
| --- | --- | --- |
| Fuentes, canales y datos | F00 | `#/c/fuentes-y-canales` |
| Medir tu progreso sin engañarte | F00 | `#/c/medir-tu-progreso` |
| Cadenas de Markov | F01 | `#/c/cadenas-de-markov` |
| Expansión de Karhunen-Loève | F01 | `#/c/expansion-karhunen-loeve` |
| Corrección point-in-time | F04 | `#/c/correccion-point-in-time` |
| Movimiento browniano | F09 | `#/c/movimiento-browniano` |
| Ecuaciones diferenciales estocásticas | F09 | `#/c/ecuaciones-diferenciales-estocasticas` |
| Lema de Itô | F09 | `#/c/lema-de-ito` |
| Valoración de opciones | F09 | `#/c/valoracion-de-opciones` |
| Griegas y cobertura | F09 | `#/c/griegas-y-cobertura` |
| Volatility drag | F09 | `#/c/volatility-drag` |
| Indicadores técnicos | F09 | `#/c/indicadores-tecnicos` |
| Terminal y shell | F03 | `#/c/terminal-y-shell` |
| Identidad y permisos en la nube | F04 | `#/c/iam-y-permisos-cloud` |
| El problema de los ficheros pequeños | F04 | `#/c/problema-de-ficheros-pequenos` |
| Eventos push y webhooks | F04 | `#/c/eventos-push-y-webhooks` |
| Enmascarado y retención | F04 | `#/c/enmascarado-y-retencion` |
| Registro de esquemas | F04 | `#/c/registro-de-esquemas` |
| Flink y procesamiento de eventos | F04 | `#/c/flink-y-procesamiento-de-eventos` |
| Certificaciones de datos | F12 | `#/c/certificaciones-de-datos` |

`fuentes-y-canales` es la puerta de entrada al material externo: nueve canales, siete fuentes de
datos y las webs de práctica y referencia, cada una con enlace directo y su advertencia. Las cinco
de la cadena estocástica cierran el bloque matemático de la ruta quant, y `correccion-point-in-time`
trae a F04 la disciplina de fechas que faltaba.

**No queda ninguna ficha del corpus por escribir.** Lo que falta no es teoría del corpus:
son los proyectos con rúbrica y el análisis de huecos del temario, en
[`06-COBERTURA.md`](06-COBERTURA.md).

**Cómo verlas.** Arranca el portal (`npm run dev`, en `http://127.0.0.1:8788`) y abre cualquiera
de las rutas de la tabla. Si el servidor ya estaba corriendo, reinícialo: sirve el `web/` que se
generó la última vez que se construyó, y las páginas nuevas no aparecen hasta que se reconstruye.

Evidencia de la comprobación: `node generar.mjs --validar` en verde, `npm run check:cloud` con 142
comprobaciones y 0 fallos, `_comprobar-prerequisitos.mjs` sin problemas de grafo y capturas en
[`capturas/`](capturas/). El temario pasa de 438 a 458 conceptos y las competencias ganan 27 pares
ficha-competencia.
