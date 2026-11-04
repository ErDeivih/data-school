# Trazabilidad: de dónde sale cada cosa y en qué estado está

**Fecha:** 2026-11-02 · Una fila por fuente. Si algo no está aquí, no existe para el proyecto.

Estados posibles: `cerrado` (ya convertido en material del repositorio), `pendiente Tn` (tanda
n de `04-PLAN.md`), `descartado` (con motivo) y `roto` (el enlace ya no existe).

---

## 1. Los seis informes de NotebookLM

| Fuente | Qué contiene de verdad | Destino | Estado |
| --- | --- | --- | --- |
| `p1` Compendio maestro | 6 módulos generalistas; casi todo repetido | Bloques B1, B2, B4 | `cerrado` como material de contraste |
| `p2` Guía maestra (derivación y griegas) | Backtesting, portafolio de 5 proyectos, procesos, griegas, filosofía | B3, B5, B6 | `cerrado` |
| `p3` Manual maestro | Versión corta de `p2`, más ABM/GBM y KL | B2 | `descartado` como fuente (redundante; se conserva para el ejemplo de ABM) |
| `p4` Guía estructural | 17 secciones con el mapeo concepto→vídeo | B1, B2, B4, B6 | `cerrado` — fuente canónica |
| `p5` Tratado completo | Aceptación-rechazo, Euler-Maruyama, griegas, indicadores, genética | B2, B3, B7 | `cerrado` — fuente canónica de B3 |
| `p6` Guía maestra de finanzas | Itô, Bachelier, griegas, mitos | B2, B3 | `cerrado` |

Las once fichas están escritas y validadas en el portal. El detalle, en
[`01-NOTEBOOKLM.md`](01-NOTEBOOKLM.md).

---

## 2. Los doce enlaces de Instagram

Comprobado el 2026-11-02 recuperando la descripción de cada publicación desde el visor de
Instagram. «Recuperable» significa que había texto legible; tres enlaces estaban rotos.

### Proyectos

| # | Enlace | Autor | Qué dice de verdad | Destino | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | `instagram.com/p/DfKbcdggN9t/` | `@mr_.analyst` | Cinco proyectos de analista financiero: análisis de estados financieros, modelo y previsión, valoración por DCF y comparables con WACC, presupuesto frente a real, panel de KPIs | PF-02 (variación presupuesto/real y panel) y un anexo de finanzas corporativas | `cerrado` en `02-PROYECTOS.md` |
| 2 | `instagram.com/p/DfLqBLKqqt2/` | — | Enlace roto: la publicación ya no existe | — | `roto` |
| 3 | `instagram.com/p/Dd6jk0Ityx9/` | `@conesatrader` | Reel con una sola línea: «hemos implementado las fórmulas matemáticas de un fondo, machine learning y academia para los agentes». Sin detalle | Solo como referencia de tendencia (agentes + quant) | `descartado` por falta de contenido |
| 4 | `instagram.com/p/DfIifZRmk2K/` | `@astroannais` | Carrusel: telescopios, fútbol, satélites, proteínas y F1 «funcionan con datos»; ofrece cinco datasets gratuitos por comentario | [`03-FUENTES.md`](03-FUENTES.md) §4 (dominios de datos) | `cerrado` |
| 5 | `instagram.com/p/DfILruVsoSz/` | `@kyan.j.d` | Cómo el equipo de software de un GT3 dibuja el «circle of doom»: un mapa de circuito reducido a una sola pregunta (dónde acabas tras el boxeo) | PF-01 y PF-05 como criterio de diseño: una pregunta, una figura | `cerrado` |
| 6 | `instagram.com/p/DecfcaSGAHO/` | `@mar_antaya` | Una línea: «puede empezar como un proyecto para ti también». Sin contenido técnico | — | `descartado` |
| 7 | `instagram.com/p/DekHgCNqA2z/` | — | Enlace roto | — | `roto` |
| 8 | `instagram.com/p/DfAWwN8q0pz/` | — | Enlace roto | — | `roto` |

### Teoría

| # | Enlace | Autor | Qué dice de verdad | Destino | Estado |
| --- | --- | --- | --- | --- | --- |
| 9 | `instagram.com/p/Den0lqaRube/` | `@gauravgoyalai` | «20 fórmulas de matemáticas que todo el que aprende IA debería saber»: descenso de gradiente, softmax, retropropagación, similitud coseno, atención | Enriquecer `funciones-de-activacion`, `funciones-de-perdida`, `atencion`, `retropropagacion`; comprobar que el descenso de gradiente tiene sitio claro | `pendiente T4` |
| 10 | `instagram.com/p/Dd_7pTNjYFA/` | `@jyts__` | La entrevista técnica de data science: 10 preguntas (p-valor, sesgo-varianza, sobreajuste, fuga de datos, clases desbalanceadas, XGBoost frente a logística, SQL, producción, tu proyecto, tu debilidad) con respuesta junior y respuesta senior; insiste en llevar portfolio | Enriquecer `entrevistas-de-datos` y `portfolio-y-proyectos` con el contraste junior/senior | `pendiente T4` |
| 11 | `instagram.com/p/Dezah90llzf/` | `@kertutenso` | Carrusel de estadística sin texto en la descripción | — | `descartado` por falta de contenido |
| 12 | `instagram.com/p/De_tr9ikv6G/` | `@sanskartech` | Cinco proyectos de ML desde cero: regresión lineal, red neuronal, k-medias, Naive Bayes y PCA | Mapeado a `regresion-lineal`, `retropropagacion`, `k-means`, `naive-bayes`, `pca`; el PCA desde cero ya lo cubre `expansion-karhunen-loeve` por el lado continuo | `cerrado` como mapa |

**Resultado honesto:** de doce enlaces salen seis ideas utilizables, tres enlaces rotos y tres
publicaciones sin contenido. Ninguno de ellos es un temario; el valor está en la lista de
proyectos y en el contraste junior/senior de la entrevista.

---

## 3. Decisiones que afectan al temario

| Decisión | Alternativa descartada | Motivo |
| --- | --- | --- |
| 10 páginas nuevas, no 30 | Crear una fase F13 de «derivados» | El contrato fija fases 0–12; una F13 obliga a tocar generador, validador y navegación por una sola rama temática |
| Cadenas de Markov en F01 | Meterlas en F09 con el riesgo de crédito | Es un modelo de probabilidad; en F09 quedarían sin prerrequisitos matemáticos claros |
| Indicadores técnicos como página escéptica | No crear la página | El corpus insiste en ellos y el portal debe poder decir por qué no son una estrategia |
| `medir-tu-progreso` en F00 | Dejarlo como párrafo de `como-estudiar` | Es la única idea del corpus que sirve a cualquier ruta, no solo a quant |
| Los paneles y la ingesta de los posts van a PF-01/PF-02 | Crear proyectos nuevos por cada post | Los posts son bocetos; los proyectos ya cubren el mismo terreno con más rigor |

---

## 4. Cómo se mantiene este registro

1. Cada alta de concepto o proyecto empieza aquí: se añade la fila con estado `pendiente Tn`.
2. Cuando la página pasa las puertas de `04-PLAN.md`, se cambia a `cerrado` y se anota la fecha.
3. Si un concepto se parte en dos o se descarta, **no se borra la fila**: se anota el motivo.
   Un registro que solo crece no sirve; uno que se reescribe, tampoco.
4. Los enlaces externos se comprueban antes de cada tanda. Un enlace roto se marca `roto` y se
   busca el contenido por el nombre del autor; no se sustituye por otro inventado.

---

## 5. Lo que queda sin explotar (límites de este trabajo)

| Fuente | Estado | Por qué |
| --- | --- | --- |
| Los ~300 vídeos del corpus de NotebookLM | Sin revisar uno a uno | Solo se han leído los seis informes derivados. Un vídeo puede contener un ejemplo que ningún informe recogió |
| Los carruseles de Instagram | Solo la descripción | El visor de Instagram no expone el texto de las diapositivas; si alguna vez las ves, este registro se amplía |
| Los 438 conceptos del temario | No revisados | Este paquete añade y enriquece; no audita lo que ya había. Una auditoría de calidad página a página es otro encargo |

Escribir esto aquí no es una disculpa: es la lista de lo que **no** está hecho, para que nadie
confunda un paquete de integración con una revisión completa.
