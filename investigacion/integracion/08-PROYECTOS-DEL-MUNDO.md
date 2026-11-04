# Proyectos que ya existen en el mundo (y cuáles de los nuestros son de verdad)

**Fecha:** 2026-11-02 · **Para qué:** no inventar proyectos que no tengan sentido. Si una idea no
aparece en ningún sitio, o es muy buena o es muy mala; casi siempre es lo segundo.

---

## 1. Criterio de «idea validada»

Una familia de proyectos entra en esta lista si cumple dos de tres:

1. Aparece en **dos fuentes independientes** (un repositorio y un curso, un foro y una
   documentación).
2. Tiene **datos públicos** con licencia clara.
3. Alguien ha publicado el resultado: un repositorio, un cuaderno o un artículo con cifras.

Lo que no cumple, no es que sea malo: es que no hay precedente y no sabrás si lo estás haciendo
bien.

---

## 2. Las familias que existen de verdad

| Familia | Dónde se ve | Qué demuestra | Nuestro equivalente | Estado |
| --- | --- | --- | --- | --- |
| **Pipeline batch con datos públicos** (NYC TLC, Chicago, INE) | Capstones del [Zoomcamp](https://github.com/topics/data-engineering-zoomcamp), blogs de consultoría | Ingesta, particiones, modelado, orquestación | PF-01 y PF-02 | Planificado, no hecho |
| **Transformación con dbt tipo Jaffle Shop** | [Guías oficiales de dbt](https://docs.getdbt.com/guides), cursos de analytics engineering | Modelado, tests, incremental, documentación | PF-02, P20 | Cubierto en ejercicios |
| **Streaming con Kafka y ventanas** | Módulo 6 del Zoomcamp, [Confluent Developer](https://developer.confluent.io/courses/), proyectos con GH Archive | Eventos tardíos, watermarks, idempotencia | PF-03, `P17` | Planificado |
| **CDC con Debezium** | Tutoriales de Debezium y charlas de data platform | Replicación lógica, SCD2, reconciliación | PF-04 | Planificado |
| **Servicio de datos con SLA** | Tutoriales de FastAPI, casos de plataformas internas | API, caché, límites, observabilidad | PF-05, `P14`-style | Planificado |
| **Calidad y observabilidad del dato** | [Great Expectations](https://greatexpectations.io/), OpenLineage, charlas de DataOps | Contratos, tests, linaje, alertas | `P06`, PF-04 | Cubierto en ejercicios |
| **Estrategia de neumáticos y ritmo en F1** | [Galería de FastF1](https://docs.fastf1.dev/gen_modules/examples_gallery/results_strategy/plot_strategy.html) | Stints, compuestos, degradación, comparación de pilotos | `P11`, `P12` | Implementado |
| **Predicción de clasificación o carrera en F1** | Proyectos de comunidad con FastF1 y OpenF1 | ML con fuga controlada, partición por carrera | `P18` | Implementado |
| **Análisis de undercut y ventana de parada** | Blogs de análisis de estrategia y cuentas de F1 data | Comparación con control, incertidumbre | `P19` | Implementado |
| **xG y análisis de fútbol** | [Football Analytics Dashboard](https://github.com/itzmore-mph/football-analytics-dashboard), [Football xG Predictor](https://github.com/bsobkowicz1096/Football-xG-Predictor) | xG, calibración, dashboards, redes de pases | `P21`, `P20` | Implementado |
| **Riesgo y factores de una cartera** | Cursos de finanzas cuantitativas, blogs de portfolio optimization | Beta, drawdown, Sharpe, alpha frente a índice | `P14`, `P15` | Implementado |
| **Memo de inversión con escenarios** | Casos de entrevista y cursos de valoración | Supuestos explícitos, sensibilidad, recomendación | `P16` | Implementado |
| **RAG sobre documentación propia** | [Hugging Face Course](https://huggingface.co/learn), tutoriales de LlamaIndex y LangChain | Embeddings, recuperación, evaluación | Ninguno | **Hueco real** |
| **Catálogo y linaje con OpenLineage/Marquez** | Demos de OpenLineage y charlas de plataforma | Linaje, impacto, gobierno | Ninguno | **Hueco real** |
| **Terraform para una plataforma de datos** | Repositorios de referencia de AWS/GCP, Zoomcamp módulo 1 | Infraestructura como código, entornos | Ninguno | **Hueco real** |

---

## 3. Veredicto sobre nuestros 22 proyectos

| Grupo | Ids | Veredicto |
| --- | --- | --- |
| Algoritmos y matrices | P01-P04 | **Validado**: es el ejercicio estándar de cualquier curso de algoritmos |
| Deduplicación y calidad | P05, P06 | **Validado**: aparece en el Zoomcamp y en toda introducción a data quality |
| Fuga y métrica | P07, P08 | **Validado**: es la primera lección de validación de cualquier curso de ML |
| Retornos y evento | P09, P10 | **Validado** en blogs de quant y cursos de series temporales |
| F1: limpieza, panel, parada | P11-P13 | **Validado** por la galería de FastF1 (stints, ritmo, posición) y por análisis de estrategia |
| Cartera y alpha | P14, P15 | **Validado**: riesgo, beta y alpha son el temario de cualquier curso de carteras |
| Memo de inversión | P16 | **Validado** en casos de entrevista y cursos de valoración |
| Ingesta desde API | P17 | **Validado**: es el módulo de ingesta de cualquier Zoomcamp |
| Clasificación F1 | P18 | **Validado** por proyectos de comunidad con FastF1 y OpenF1 |
| Undercut | P19 | **Adaptado**: menos común como proyecto cerrado, pero es análisis estándar de estrategia |
| Fútbol: estrella y xG | P20, P21 | **Validado** por repositorios públicos de xG y dashboards |
| Finanzas desde cero | P22 | **Validado**: interés compuesto, inflación y riesgo son el temario de cualquier curso básico |

**Ninguno es una invención sin precedente.** Los dos únicos «adaptados» son P19 (undercut) y la
parte de memo de P16; los dos son análisis reales de industria, solo que no suelen aparecer como
ejercicio cerrado.

---

## 4. Los tres huecos que sí merecen un proyecto

Por orden de valor para una candidatura de data engineer:

1. **RAG sobre documentación propia.** Un corpus de 200 documentos, embeddings, recuperación,
   evaluación con preguntas y respuestas. Existe en todas partes y no tenemos ninguno: es el
   proyecto que más se pide en ofertas que mezclan datos e IA. Fase que ejercita: F08.
2. **Linaje y catálogo.** Ingerir, transformar y registrar el linaje con OpenLineage para responder
   «si cambio esta columna, qué se rompe». Es el proyecto que demuestra que entiendes un equipo de
   datos y no solo un pipeline. Fase: F04 (`catalogo-y-linaje`).
3. **Terraform de una plataforma mínima.** Bucket, almacén, orquestador y permisos, con dos entornos
   y borrado seguro. Es el que separa «sé usar la consola» de «sé desplegar». Fase: F11
   (`iac-y-terraform`).

---

## 5. Lo que el mundo hace y no deberías hacer

| Proyecto | Por qué no |
| --- | --- |
| Titanic, Iris, prevalencia de diabetes | Saturados: el reclutador ha visto 300 iguales y no dicen nada de ti |
| Dashboard de COVID o de ventas genérico | No hay pregunta, solo gráficos |
| Predecir el precio de una acción con LSTM | Sin valor: si funcionara no lo publicarías, y todo el mundo sabe que no funciona |
| «Análisis de sentimiento de Twitter» sin caso | Datos que cambian, API de pago y ninguna decisión asociada |
| Un pipeline sin README | No existe para quien lo lee |
| Cinco proyectos a medias | Vale menos que uno terminado |

---

## 6. F1 con datos reales: lo que hay que saber antes

- **[FastF1](https://docs.fastf1.dev/)** es la librería de referencia: sesiones, vueltas, telemetría,
  stints, resultados. **Desde la versión 3.9 pide una suscripción F1TV Access para la mayoría de
  funciones**, así que no es gratis para el portfolio.
- **[OpenF1](https://openf1.org/)** es una API gratuita con sesiones, posiciones, radios y vueltas,
  pero su histórico empieza en 2023 y tiene límite de peticiones.
- **Consecuencia práctica:** los ejercicios de la app usan el paquete sintético para que la rúbrica
  sea reproducible; el proyecto de portfolio con datos reales se hace con OpenF1 o con FastF1 y
  suscripción, y se documenta la fuente y la fecha en el README.

## 7. Fútbol con datos reales

- **[StatsBomb Open Data](https://github.com/statsbomb/open-data)** es el estándar abierto: eventos
  de partidos con coordenadas, para xG y redes de pases. Licencia para uso no comercial con
  atribución.
- **Los dos repositorios de referencia** ([dashboard](https://github.com/itzmore-mph/football-analytics-dashboard),
  [xG](https://github.com/bsobkowicz1096/Football-xG-Predictor)) usan XGBoost, NetworkX y Streamlit:
  exactamente lo que pide el mercado para un proyecto de analítica deportiva.

## 8. Finanzas con datos reales

- **Riesgo y factores**: `yfinance` o Stooq para precios, y las series de FRED para tipos. Un
  proyecto de cartera con beta, drawdown y Sharpe es el clásico de cualquier blog de quant.
- **Aviso de licencia:** no redistribuyas precios de proveedores con condiciones restrictivas. Para
  portfolio, guarda el script y documenta la fuente, no los datos.

---

## 9. Qué hacer con esto

No hace falta inventar nada: el catálogo actual cubre las familias validadas salvo tres. La
decisión razonable es:

1. Hacer PF-01 y PF-02 (los dos clásicos indiscutibles).
2. Elegir **uno** de F1, fútbol o finanzas como proyecto de dominio, con datos reales y README.
3. Añadir el RAG si el mercado al que apuntas mezcla datos e IA.

Lo demás es coleccionar proyectos sin terminar.
