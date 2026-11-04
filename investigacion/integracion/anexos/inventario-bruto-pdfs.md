# Análisis de los 6 informes de NotebookLM

Los seis textos son seis redacciones del **mismo temario**. No son seis fuentes: son un temario
y cinco variaciones. Los bloques se repiten en el mismo orden con los mismos ejemplos
(NVIDIA a 543, el balón del campo de fútbol, el cruce de medias 7/12 frente a 3/5, los
bombarderos de Abraham Wald, los 75 jugadores del casino, el Sharpe que pasa de 3,0 a 0,9–1,2,
el portafolio cubierto frente al beta puro en 2021–2022 y el sistema AMZN a 244 con IV del 41 %).
La diferencia entre ellos es de **extensión, orden y algún añadido aislado**, no de contenido.

Referencia usada para el mapeo: `CONTENIDO-TEMARIO.md` (438 conceptos, 13 fases, F00–F12).
Los 29 `id` propuestos se han verificado con búsqueda exacta sobre ese fichero: ninguno existe
ya. Todos los prerequisitos propuestos son `id` que ya están en el temario.

---

## 1. Qué es cada PDF

| Fichero | Título real (literal) | Módulos | Unicidad | Redundancia |
| --- | --- | --- | --- | --- |
| `p1.txt` | COMPENDIO MAESTRO DE INGENIERÍA CUANTITATIVA, MODELADO ESTOCÁSTICO Y ARQUITECTURA DE TRADING PARA AGENTES IA | 6 + conclusión | Único en el bloque de arquitectura defensiva para agentes (confianza cero, solo lectura y apéndice, disyuntores, límites de API) y en la tabla de especificación técnica con directivas de código. Añade la «teoría de las dos envolventes» como formalismo y el principio de irreducibilidad computacional | Alta con p2 y p3: mismos tres sesgos, mismo caso de cobertura NVIDIA, mismo caso del balón, misma regla del 72, misma simulación del casino. Es el más «de gestión» de los seis |
| `p2.txt` | GUÍA MAESTRA DE INGENIERÍA CUANTITATIVA: DESDE LA DERIVACIÓN ESTOCÁSTICA Y COBERTURA MULTI-GREEK HASTA LA ARQUITECTURA DE SISTEMAS Y MITIGACIÓN DE SESGOS DE MODELADO | 5 (12 subsecciones) | Único en la aplicación del puente browniano al **hueco nocturno** (cierre 16:00 a apertura 9:30) y en la derivación de la ecuación de Fredholm término a término con la regla de Leibniz. Es el más detallado en las derivaciones | Casi total con p3 en los bloques 3 y 4. La tabla de sesgos es la mejor construida de los seis (mecanismo, consecuencia, mitigación) |
| `p3.txt` | MANUAL MAESTRO DE INGENIERÍA CUANTITATIVA: DESDE LA TEORÍA DE PROCESOS ESTOCÁSTICOS HASTA EL ARQUITECTURA DE TRADING Y CONTROL DE RIESGO INSTITUCIONAL | 5 | Único en la **matriz fundamental N=(I−Q)^-1** para estados absorbentes, en el proceso de Ornstein-Uhlenbeck escrito para la tasa de acierto, en el consejo de redondear la matriz de griegas antes de invertirla, en el crudo WTI de abril de 2020 y en la regresión de alfa con SMB y HML | Calco de p2 en casi todo. Cambia el orden de los bloques (pone arquitectura antes que procesos estocásticos) y añade la cita de Fama-French |
| `p4.txt` | GUÍA ESTRUCTURAL Y TEMARIO MAESTRO DE FINANZAS CUANTITATIVAS: MAPEO INTEGRAL DE CONCEPTOS A FUENTES DE VIDEO | 6 | **La más importante y la única estructuralmente distinta**: cada apartado lleva su «Mapeo a Video de Origen». Es la única que contiene el modelo de Bachelier con su derivación, la interpretación frecuentista del intervalo de confianza, la fórmula del error de truncamiento espectral, el criterio objetivo de retiro EG ≤ coste de fricción, el decaimiento de Davies-Harte O(N log N) y el incidente del Discord | Alta en solapamiento temático, baja en contenido nuevo: repite ABM/GBM, Karhunen-Loève, PCA, cobertura multi-griega y sesgos. Pero es la única que sirve como **índice** del resto |
| `p5.txt` | TRATADO COMPLETO DE INGENIERÍA CUANTITATIVA: DESDE LA SIMULACIÓN ESTOCÁSTICA Y EL ÁLGEBRA LINEAL HASTA LA ARQUITECTURA DE TRADING ALGORÍTMICO Y LA GESTIÓN DE RIESGO REAL | 6 | Único en todo el bloque de **estrategias concretas**: VWAP intradía en 15 minutos, detección vectorizada de pin bar, HMA/RSI multitemporal, programación genética de indicadores, comparativa backtesting.py frente a VectorBT. Único también en el método de aceptación y rechazo, en el código de simulación espectral y en la ruptura de correlación | Sus secciones 2, 3 y 5 son copia de los otros cinco. Es el más largo y el que más relleno arrastra |
| `p6.txt` | GUÍA MAESTRA DE FINANZAS CUANTITATIVAS: CONCEPTOS FUNDAMENTALES, MODELADO ESTOCÁSTICO Y VALIDACIÓN DE ESTRATEGIAS | 5 | La más ordenada y la más honesta en dos matices que los demás no tienen: que un Sharpe degradado a 0,9–1,2 es **más peligroso** que uno negativo, y el detalle de la estrategia transversal long/short con deslistados. Añade el cálculo +50 % y −50 % igual a −25 % | Es un resumen de p1–p5. No aporta ninguna derivación nueva, pero es la mejor puerta de entrada |

**Veredicto:** p4 es la fuente canónica de estructura (es el único que declara de dónde sale cada
bloque). p2 y p5 son las fuentes canónicas de detalle matemático. p1 es la canónica de
arquitectura de sistemas. p3 es prescindible salvo por tres detalles. p6 es la canónica de
redacción y p5 la única con contenido operativo propio.

---

## 2. Mapa de módulos por PDF

### 2.1 `p1.txt` — Compendio maestro

| Módulo (título literal) | De qué trata |
| --- | --- |
| 1. Principios Fundamentales de Finanzas Cuantitativas y Análisis Crítico del Mercado | Crítica a la eficiencia de mercado, alfa como retorno ortogonal, interés compuesto frente a day trading, ausencia de contrafactuales |
| 2. Sesgos Críticos y Trampas Mortales en el Backtesting de Estrategias | Look-ahead (dos envolventes), data snooping y p-hacking (3/5 frente a 7/12), supervivencia (Abraham Wald) y los tres «cómplices» de fricción |
| 3. Procesos Estocásticos y Modelado Matemático: De la Teoría a la Simulación | SDE, comparativa ABM frente a GBM con derivación por lema de Itô, expansión de Karhunen-Loève del puente, Volterra, browniano fraccionario y Davies-Harte |
| 4. Estadística Aplicada, Inferencia y Métricas de Progresión Teórica | Ley de grandes números frente a teorema central del límite, insesgadez y corrección de Bessel, contraste t y Z con el caso del balón, edge EG y media móvil de 7 periodos |
| 5. Álgebra Lineal y Reducción de Dimensionalidad Aplicada al Mercado | Griegas de Black-Scholes, cobertura delta-gamma-vega con sistema 2x2 sobre NVIDIA, PCA con equivalencia SVD-covarianza y carga factorial por componente |
| 6. Arquitectura de Proyectos Cuantitativos y Especificaciones para Implementación en Agentes IA | Los cinco proyectos (Qfin, MBS, Gaussian Cookbook, sistema de volatilidad) y la matriz de especificación técnica con casos de uso, riesgo y directiva de código |
| Conclusión, Arquitectura de Seguridad y Hoja de Ruta de Desarrollo | Cuatro principios rectores con la arquitectura de confianza cero, registros inmutables y disyuntores |

### 2.2 `p2.txt` — Guía maestra de derivación estocástica

| Módulo (título literal) | De qué trata |
| --- | --- |
| 1. Metodología Rigurosa de Backtesting y Prevención de Trampas Matemáticas en Modelos Trading | Tabla de tres sesgos con mecanismo, consecuencia y mitigación; el look-ahead explicado con el decil superior e inferior que se normaliza con la semana siguiente; los «cómplices del crimen» |
| 2. Arquitectura de Proyectos Cuantitativos de Alto Impacto y Desarrollo de Sistemas | Cadena captura point-in-time a ejecución; los cinco proyectos con su fundamentación matemática, su implementación y su lección estratégica |
| 3. Modelado Matemático de Procesos Estocásticos: Movimiento Browniano Aritmético (ABM) vs. Geométrico (GBM) y Expansión Karhunen-Loève | Derivación paso a paso de ABM y de GBM, teoría espectral en L2, ecuación de Fredholm, EDO, normalización y truncamiento; aplicación al hueco nocturno |
| 4. Cobertura Algorítmica Multi-Greek y Métodos de Reducción de Dimensionalidad (PCA) | Caso numérico NVIDIA con protocolo de tres pasos, PCA con demostración SVD-covarianza e interpretación de cargas |
| 5. Inferencia Estadística Aplicada, Desmitificación del Trading Efímero y la Filosofía del Progreso Cuantitativo | Ley de grandes números frente a central del límite, contraste del balón, crítica a la eficiencia, alfa ortogonal, regla del 72, simulación del casino y media rodante |

### 2.3 `p3.txt` — Manual maestro

| Módulo (título literal) | De qué trata |
| --- | --- |
| 1. Trampas Fundamentales en el Backtesting y Diagnóstico de la Degradación de Estrategias | Tres sesgos con analogía de sobres, cruces y bombarderos; esperanza matemática EV y su degradación como proceso de Ornstein-Uhlenbeck |
| 2. Arquitectura de Proyectos Cuantitativos: Del Prototipado Teórico a Sistemas de Producción | Los cinco proyectos; aquí el de MBS llega a la matriz fundamental N=(I−Q)^-1 |
| 3. Teoría Avanzada de Procesos Estocásticos: Karhunen-Loève y Dinámica de ABM vs. GBM | Los seis pasos del algoritmo espectral, tabla continuo frente a discreto, ABM frente a GBM con la distinción entre media ensamblada y mediana de trayectoria |
| 4. Cobertura Algorítmica Multi-Griegos y Reducción de Dimensionalidad (PCA) | Sistema de griegas con redondeo previo a la inversión, condición de suficiencia de n−1 opciones para n−1 griegas, PCA y no estacionariedad |
| 5. Inferencia Estadística Aplicada, Demolición de Mitos Financieros y la Filosofía del Quant | Contraste t y Z, errores tipo I y II, día trading, regla del 72, casino, alfa con SMB y HML, portafolio cubierto y desigualdad de Paolucci |

### 2.4 `p4.txt` — Guía estructural y temario (la más importante)

| Módulo (título literal) | De qué trata |
| --- | --- |
| 1. MÓDULO 1: ESTADÍSTICA APLICADA, INFERENCIA Y ANÁLISIS DE PROGRESO EN TRADING | 1.1 Ley de grandes números y central del límite con tabla de formulaciones y vídeo; 1.2 media acumulada frente a media rodante con bandas de ±1σ; 1.3 interpretación frecuentista del intervalo de confianza y falacias tipo Craig Percoco |
| 2. MÓDULO 2: MODELADO DE PROCESOS ESTOCÁSTICOS Y DERIVACIÓN ANALÍTICA DE PRECIOS | 2.1 ABM frente a GBM; 2.2 los seis pasos de Karhunen-Loève con decaimiento O(k^-2) y error de truncamiento; 2.3 derivación del modelo de Bachelier y su uso en derivados de tipos |
| 3. MÓDULO 3: REDUCCIÓN DE DIMENSIONALIDAD, CADENAS DE MARKOV Y LIBRERÍAS CUANTITATIVAS | 3.1 PCA; 3.2 cadenas de Markov para morosidad con estados absorbentes, MLE y Chapman-Kolmogorov; 3.3 Gaussian Cookbook, Davies-Harte con Toeplitz incrustado en circulante y parámetro de Hurst |
| 4. MÓDULO 4: INGENIERÍA DE PORTAFOLIOS, COBERTURA MULTI-GREEK Y GESTIÓN DE RIESGO | 4.1 cobertura delta-gamma-vega con tabla paso a paso; 4.2 portafolio cubierto frente a beta pasiva y demostración del arrastre de volatilidad |
| 5. MÓDULO 5: VALIDACIÓN DE ESTRATEGIAS, EVALUACIÓN DE EDGE Y ERRORES EN BACKTESTING | 5.1 tres trampas más la ficción de costes; 5.2 ecuación del edge y criterio objetivo de desconexión EG ≤ coste de fricción; 5.3 lotería, regla del 72, casino y ausencia de contrafácticos |
| 6. MÓDULO 6: PROYECTOS INTEGRALES Y REFLEXIONES DEL DOMINIO PROFESIONAL | 6.1 los cinco proyectos con valor en entrevistas; 6.2 riesgo operativo con el caso del Discord de Quant Guild; 6.3 crítica a la eficiencia, alfa y límites de la IA |

### 2.5 `p5.txt` — Tratado completo

| Módulo (título literal) | De qué trata |
| --- | --- |
| 1. Fundamentos Matemáticos: Métodos de Simulación Estocástica y Análisis Espectral | 1.1 generador uniforme como base; 1.2 método de aceptación y rechazo con tasa analítica (normal 31,33 % frente a triangular 50 %); 1.3 derivación completa de Karhunen-Loève; 1.4 discretización Q Λ^(1/2) Z con código, conservación de covarianza y opciones dependientes de trayectoria |
| 2. Modelado Estadístico, Reducción de Dimensionalidad e Inferencia | 2.2 PCA con ruptura de correlación en estrés; 2.3 ley de grandes números frente a central del límite, simulación Poisson frente a uniforme y contraste Z del balón |
| 3. Cobertura Algorítmica Multi-Griega (Multi-Greek Hedging) en Opciones | Fórmulas cerradas de las cinco griegas, restricción del subyacente, sistema matricial, código y tabla de etapas |
| 4. Arquitectura, Inferencia y Métodos Evolutivos en Trading Algorítmico | 4.2 estrategia VWAP de 15 minutos con ATR y cierre forzado, y el colapso por comisión del 0,1 %; 4.3 pin bar vectorizado en XAU/USD con filtro EMA; 4.4 HMA y RSI multitemporal en BTC con Monte Carlo de 500 perturbaciones; 4.5 programación genética de indicadores y zona muerta |
| 5. Trampas Críticas en el Backtesting y Gestión de Riesgo Cuantitativo | Los tres sesgos y el «Trading Egg» con ventanas móviles |
| 6. Filosofía Práctica de Mercados, Crítica Académica y Resiliencia Cuantitativa | Crítica a la eficiencia, alfa, day trading, casino, reconciliación aritmética del portafolio cubierto, irreducibilidad computacional y analogía del jardín |

### 2.6 `p6.txt` — Guía maestra de finanzas cuantitativas

| Módulo (título literal) | De qué trata |
| --- | --- |
| 1. Desmitificación del Backtesting: Análisis de Sesgos Críticos y Rigor Estadístico | Los tres sesgos, el matiz de que degradarse a 0,9–1,2 es peor que degradarse a negativo, el long/short transversal con deslistados y la tabla de fricciones |
| 2. Proyectos Fundamentales para la Construcción de un Portafolio Cuantitativo de Alto Nivel | Los cinco proyectos con matriz comparativa de concepto, reto técnico e impacto |
| 3. Procesos Estocásticos y Cálculo de Itô: Movimiento Browniano Aritmético (ABM) vs. Geométrico (GBM) | SDE, dinámica sumativa frente a multiplicativa, arrastre de volatilidad, lema de Itô completo, Karhunen-Loève y truncamiento |
| 4. Desmitificación de Mitos del Mercado: Trading Intradía, Eficiencia y Falacias Académicas | Lotería y arrastre, ausencia de contrafácticos con la tasa de acierto 57 % a 46 %, casino, eficiencia, alfa frente a CAPM y Fama-French, cobertura activa |
| 5. Algoritmos y Estadística Aplicada en Python: Cobertura Multi-Greek, PCA y Análisis Temporal | Cobertura con código NumPy, PCA con SVD, ley de grandes números y central del límite, contraste Z, errores tipo I y II y decaimiento del EV |

### 2.7 Fuente canónica por bloque temático

| Bloque temático | Canónico | Por qué | Redundantes |
| --- | --- | --- | --- |
| Sesgos de backtesting y fricciones | p2 §1 | La única tabla con mecanismo, consecuencia y mitigación en las tres columnas, más el ejemplo del decil con datos alternativos | p1 §2, p3 §1, p4 §5.1, p5 §5.2, p6 §1 |
| Proyectos y arquitectura de portafolio | p4 §6.1 | Añade el «valor en entrevistas» y el stack concreto de cada proyecto | p1 §6, p2 §2.2, p3 §2, p5 §2, p6 §2 |
| ABM, GBM y lema de Itô | p2 §3.3 | Derivación más completa, con la regla cuadrática de Itô explícita | p1 §3, p3 §3, p4 §2.1, p6 §3 |
| Karhunen-Loève del puente browniano | p5 §1.3 | Derivación término a término de la regla de Leibniz y conservación de covarianza | p1 §3, p2 §3.4, p3 §3, p4 §2.2, p6 §3 |
| Browniano fraccionario, Volterra y Davies-Harte | p4 §3.3 | Única con la función de covarianza del fBm y la complejidad O(N log N) frente a O(N³) de Cholesky | p1 §3, p2 §2.2, p3 §2, p6 §2 |
| Modelo de Bachelier | p4 §2.3 | Único que lo trata | ninguno |
| Griegas y cobertura multi-griega | p5 §3 | Fórmulas cerradas de las cinco griegas y código ejecutable | p1 §5, p2 §4.2, p3 §4, p4 §4.1, p6 §5 |
| PCA y equivalencia con SVD | p5 §2.2 | Añade la ruptura de correlación con límite ρ→1 | p1 §5, p2 §4.3, p3 §4, p4 §3.1, p6 §5 |
| Cadenas de Markov para morosidad | p4 §3.2 | Estados completos, tabla numérica de transición y discusión de la ventana de calibración | p1 §6, p2 §2.2, p3 §2, p6 §2 |
| Inferencia (ley de grandes números, central del límite, t, potencia) | p4 §1.1 | Única que justifica el pivote de t a normal con n mayor que 30 y mapea a vídeo | p1 §4, p2 §5.2, p3 §5, p5 §2.3, p6 §5 |
| Intervalos de confianza | p4 §1.3 | Único que lo trata | ninguno |
| Edge, valor esperado y criterio de retiro | p4 §5.2 | Única con la desigualdad EG ≤ coste de fricción como regla de desconexión | p1 §4, p3 §1, p5 §5.3, p6 §5 |
| Day trading, regla del 72 y casino | p5 §6.3 | La única con la reconciliación aritmética explícita del ejemplo 2021–2022 | p1 §1, p2 §5.3, p3 §5, p4 §5.3, p6 §4 |
| Simulación de variables aleatorias | p5 §1.2 | Único que lo trata | ninguno |
| Estrategias concretas y motores de backtest | p5 §4 | Único que lo trata | ninguno |
| Arquitectura defensiva y seguridad operativa | p1 (conclusión) | Único con confianza cero, apéndice inmutable, disyuntores y límites de API | p4 §6.2, p5 §6.5 |

---

## 3. Inventario de conceptos

Convención: `X` = tratado con desarrollo propio; `m` = solo mención o uso de pasada; `·` = no
aparece. La primera columna es solo un contador de filas, para poder decir «93 conceptos» sin
discusión; las referencias cruzadas entre secciones se hacen siempre por `id`, nunca por número.
Un mismo `id` puede aparecer como existente en unas filas y como hueco en otras: son conceptos
distintos que caen en la misma página.

### 3.1 Backtesting, sesgos y validación

| nº | Concepto | p1 | p2 | p3 | p4 | p5 | p6 | Id existente o estado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sesgo de mirar al futuro con filtración F_t | X | X | X | X | X | X | `sesgo-de-mirar-al-futuro` | Existe. El temario lo enuncia pero no da el formalismo de filtración ni la alineación temporal |
| 2 | Teoría de las dos envolventes o de los dos sobres | X | X | X | X | X | X | Existe pero incompleto en `sesgo-de-mirar-al-futuro` | Es una analogía pedagógica, no un formalismo; falta en la página del temario |
| 3 | Alineación point-in-time de datos alternativos (tráfico web, sentimiento, publicación de resultados) | X | X | X | X | X | X | **HUECO `correccion-point-in-time`** | Es la idea más repetida de los seis textos y no tiene id propio en F04 ni en F09 |
| 4 | Data snooping y p-hacking paramétrico (3/5 frente a 7/12) | X | X | X | X | X | X | `data-snooping-y-multiple-testing` | Existe. La página debería incorporar el ejemplo de las medias móviles |
| 5 | Estabilidad paramétrica local (7/12 frente a 8/12) y mesetas de rendimiento | X | X | X | X | X | X | Existe pero incompleto en `validacion-temporal` | Falta el criterio de sensibilidad: pequeña perturbación no debe colapsar la métrica |
| 6 | Validación walk-forward con ventanas rodantes | X | X | X | X | X | X | Existe pero incompleto en `validacion-temporal` | El temario lo cita como validación temporal; falta el procedimiento in-sample y out-of-sample desplazado |
| 7 | Sesgo de supervivencia y analogía de Abraham Wald | X | X | X | X | X | X | `sesgo-de-supervivencia` | Existe. La analogía de los bombarderos no está en el temario y es la mejor explicación disponible |
| 8 | Reconstrucción del universo point-in-time con empresas deslistadas | X | X | X | X | X | X | **HUECO `universo-de-inversion-point-in-time`** | Distinto del sesgo: aquí se trata de construir el universo, que es trabajo de ingeniería de datos |
| 9 | Universo transversal long/short con deslistados | · | · | · | · | · | X | Existe pero incompleto en `sesgo-de-supervivencia` | Solo p6 explica cómo afecta a las ponderaciones de una cartera long/short |
| 10 | Costes de transacción, comisiones y cánones | X | X | X | X | X | X | `slippage-y-comisiones` | Existe |
| 11 | Horquilla bid-ask y error de asumir precios medios | X | X | X | X | X | X | `order-book-y-spread` | Existe |
| 12 | Deslizamiento e impacto de mercado por latencia y profundidad | X | X | X | X | X | X | `slippage-y-comisiones` | Existe |
| 13 | Regla de descarte: sin edge en un mundo sin fricción, la fricción no lo crea | · | · | · | · | · | X | Existe pero incompleto en `slippage-y-comisiones` | Criterio de orden previo al backtest; solo p6 lo formula |
| 14 | Sharpe de 3,0 como síntoma de error y no como logro | X | X | X | X | X | X | `ratio-de-sharpe` | Existe pero incompleto: el umbral del 3,0 y la degradación a 0,9–1,2 son contenido nuevo |
| 15 | Deflactación del Sharpe por número de intentos | · | · | · | · | · | · | `sharpe-deflactado` | **Hueco de los PDFs, no del temario**: ninguno de los seis menciona la deflactación ni a López de Prado |

### 3.2 Procesos estocásticos

| nº | Concepto | p1 | p2 | p3 | p4 | p5 | p6 | Id existente o estado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | Proceso de Wiener y sus incrementos independientes | X | X | X | X | m | X | **HUECO `proceso-de-wiener`** | Se define en cinco de los seis, siempre como base de lo demás; no tiene id |
| 17 | Movimiento browniano aritmético | X | X | X | X | m | X | **HUECO `movimiento-browniano-aritmetico`** | Con solución cerrada, distribución normal y admisión de precios negativos |
| 18 | Movimiento browniano geométrico | X | X | X | X | m | X | **HUECO `movimiento-browniano-geometrico`** | Es la pieza central de los seis textos y no existe en el temario |
| 19 | Lema de Itô y reglas cuadráticas (dt al cuadrado igual a 0, dW al cuadrado igual a dt) | X | X | X | X | · | X | **HUECO `lema-de-ito`** | p5 no lo deriva, solo lo usa en la descripción de Qfin |
| 20 | Ecuación diferencial estocástica como objeto formal | X | X | X | X | m | X | **HUECO `ecuaciones-diferenciales-estocasticas`** | Sin id en todo F01 y F09 |
| 21 | Discretización de Euler-Maruyama | X | X | X | X | m | X | **HUECO `simulacion-euler-maruyama`** | Aparece en los cinco como esquema de simulación de Qfin |
| 22 | Arrastre de volatilidad y término menos media sigma al cuadrado | X | X | X | X | X | X | **HUECO `arrastre-de-volatilidad`** | Todos lo citan; nadie da el enlace con la media geométrica de forma completa |
| 23 | Media aritmética del precio frente a mediana de la trayectoria | m | X | X | X | · | X | Incluido en `arrastre-de-volatilidad` | La esperanza crece a mu y la mediana a mu menos media varianza |
| 24 | Puente browniano y covarianza mínimo menos producto | X | X | X | X | X | X | **HUECO `puente-browniano`** | También usado para interpolar, no solo para simular |
| 25 | Expansión de Karhunen-Loève del puente | X | X | X | X | X | X | **HUECO `expansion-karhunen-loeve`** | Derivación por ecuación de Fredholm y regla de Leibniz |
| 26 | Decaimiento espectral O(k^-2) y error de truncamiento | m | X | X | X | X | X | Incluido en `expansion-karhunen-loeve` | Solo p4 da la fórmula cerrada del error cuadrático medio de truncamiento |
| 27 | Simulación espectral discreta Q Λ^(1/2) Z y conservación de covarianza | X | X | X | X | X | X | **HUECO `simulacion-normal-multivariante`** | Es la versión matricial del puente; p5 demuestra que la covarianza se conserva |
| 28 | Movimiento browniano fraccionario y parámetro de Hurst | X | X | X | X | m | X | **HUECO `movimiento-browniano-fraccionario`**, solapa con `hurst-y-memoria` | El id existente mide memoria; faltan el proceso, su covarianza y su simulación |
| 29 | Algoritmo de Davies-Harte con FFT y matriz circulante de 2N | X | X | X | X | · | X | **HUECO `davies-harte-y-fft`** | Solo p4 da la complejidad O(N log N) frente a O(N³) de Cholesky |
| 30 | Procesos de Volterra y volatilidad rugosa (Rough Bergomi) | X | X | X | X | · | X | **HUECO `procesos-de-volterra`** | Solo mención del modelo en todos; Volterra se define con la integral de núcleo |
| 31 | Modelo de Bachelier para opciones | · | · | · | X | · | · | **HUECO `modelo-de-bachelier`** | Exclusivo de p4, con derivación completa y justificación por tipos negativos |
| 32 | Método de aceptación y rechazo | · | · | · | · | X | · | **HUECO `metodo-de-aceptacion-rechazo`** | Exclusivo de p5, con tasa de aceptación analítica y comparativa normal frente a triangular |
| 33 | Método de la transformada inversa | · | · | · | · | m | · | Solo mención | Se cita como alternativa inabordable cuando la CDF no es invertible |
| 34 | Valoración Monte Carlo de opciones dependientes de trayectoria | m | X | X | X | X | X | Existe pero incompleto en `simulacion-de-monte-carlo` | Falta el sesgo por truncar la covarianza en asiáticas y con barrera |

### 3.3 Álgebra lineal, derivados y PCA

| nº | Concepto | p1 | p2 | p3 | p4 | p5 | p6 | Id existente o estado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 35 | Modelo de Black-Scholes como marco de valoración | m | X | X | X | X | X | **HUECO `modelo-de-black-scholes`** | Se usa como caja negra en los seis; ninguno deriva la prima |
| 36 | Volatilidad implícita y suelo de volatilidad | X | X | X | X | · | X | **HUECO `volatilidad-implicita`** | Se invierte numéricamente para fijar reglas de reversión a la media |
| 37 | Griegas de Black-Scholes (delta, gamma, vega, theta, rho) | X | X | X | X | X | X | **HUECO `griegas-black-scholes`** | p5 es el único que da las cinco fórmulas cerradas |
| 38 | Cobertura simultánea delta-gamma-vega por sistema lineal | X | X | X | X | X | X | **HUECO `cobertura-delta-gamma-vega`** | Incluye la regla de n−1 opciones para n−1 griegas no lineales |
| 39 | Mal condicionamiento de la matriz de griegas y redondeo previo a invertir | X | · | X | · | · | · | Existe pero incompleto en `determinante-rango-invertibilidad` | Falta el número de condición y el umbral 1e5 que cita p1 |
| 40 | Delta unitario del subyacente con gamma y vega nulas | X | X | X | X | X | X | Incluido en `cobertura-delta-gamma-vega` | Es la razón por la que hacen falta opciones auxiliares |
| 41 | PCA como eliminación de colinealidad en retornos | X | X | X | X | X | X | `pca` | Existe |
| 42 | Equivalencia entre SVD y diagonalización de covarianza (lambda igual a sigma al cuadrado entre n−1) | X | X | X | X | X | X | Existe pero incompleto en `pca` y `descomposicion-svd` | La identidad concreta no está en el temario |
| 43 | Interpretación económica de las cargas (mercado 55 %, sector 27 %, idiosincrásico) | X | X | X | X | X | X | Existe pero incompleto en `pca` | Falta el ejemplo con AAPL, AMZN, MSFT y GM |
| 44 | No estacionariedad de las cargas en ventanas rodantes de 60 días | X | X | X | X | X | X | Existe pero incompleto en `pca` | El temario cita el PCA estático |
| 45 | Ruptura de correlación en estrés y límite rho hacia 1 | X | X | X | X | X | X | Existe pero incompleto en `pca` | Solo p5 escribe el límite y la consecuencia sobre la diversificación |
| 46 | Cadena de Markov discreta con estados absorbentes aplicada a morosidad | X | X | X | X | · | X | **HUECO `cadenas-de-markov-y-estados-absorbentes`** | `hmm-regimenes` es otra cosa: estados ocultos, no transiciones observadas |
| 47 | Estimación por máxima verosimilitud de la matriz de transición | X | X | X | X | · | X | Existe pero incompleto en `maxima-verosimilitud` | Falta el caso concreto de contar transiciones y normalizar filas |
| 48 | Ecuaciones de Chapman-Kolmogorov como potencia de la matriz | X | X | X | X | · | X | Incluido en `cadenas-de-markov-y-estados-absorbentes` | P a la n |
| 49 | Matriz fundamental N igual a (I−Q)^-1 | · | · | X | · | · | · | Incluido en `cadenas-de-markov-y-estados-absorbentes` | Exclusivo de p3; da el tiempo esperado en estados transitorios |
| 50 | Cobertura de cola y portafolio cubierto frente a beta puro | X | X | X | X | X | X | **HUECO `cobertura-de-cola`** | Con el ejemplo 2021–2022, cuyos números se contradicen entre PDFs |

### 3.4 Inferencia y estadística

| nº | Concepto | p1 | p2 | p3 | p4 | p5 | p6 | Id existente o estado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | Ley de los grandes números | X | X | X | X | X | X | `ley-de-los-grandes-numeros` | Existe; todos distinguen convergencia en probabilidad de convergencia casi segura |
| 52 | Teorema central del límite | X | X | X | X | X | X | `teorema-central-del-limite` | Existe |
| 53 | Insesgadez de la media muestral y varianza sigma al cuadrado entre n | X | X | X | X | X | m | `estimadores-y-propiedades` | Existe; falta la demostración explícita |
| 54 | Corrección de Bessel y parámetro ddof igual a 1 | X | m | · | X | X | · | Existe pero incompleto en `estimadores-y-propiedades` | Es un detalle de implementación con consecuencias reales; no está en el temario |
| 55 | Estadístico t frente a Z con varianza desconocida y pivote a normal | X | X | X | X | X | X | `test-t` | Existe; p4 justifica el pivote con n mayor que 30 |
| 56 | Interpretación frecuentista del intervalo de confianza | · | · | · | X | · | · | `intervalos-de-confianza` | Existe y el temario ya anuncia el error de interpretación; p4 lo desarrolla |
| 57 | p-valor como probabilidad condicional bajo la nula | m | m | X | X | · | X | `p-valor` | Existe |
| 58 | Errores tipo I y II, potencia 1 menos beta y efecto del tamaño muestral | X | X | X | X | X | X | `errores-tipo-i-ii-y-potencia` | Existe |
| 59 | Media acumulada frente a media rodante con bandas de más menos 1 sigma | X | X | m | X | X | · | Existe pero incompleto en `suavizado-exponencial` | En los PDFs es diagnóstico de progreso, no pronóstico |
| 60 | Simulación del teorema central del límite con Poisson y uniforme | · | · | · | · | X | · | Existe en `teorema-central-del-limite` y `distribuciones-discretas` | Solo p5 lo lleva a código |
| 61 | Ausencia de contrafactuales y ausencia de convergencia asintótica | X | X | X | X | X | X | **HUECO `ausencia-de-contrafactuales`** | Seis de seis; ninguno de los 438 ids lo cubre |
| 62 | Caso del balón de fútbol con n igual a 200 | X | X | X | X | X | X | No es concepto, es ejemplo | Se repite con cuatro juegos de números distintos (ver 6.5) |

### 3.5 Edge, riesgo y dinero

| nº | Concepto | p1 | p2 | p3 | p4 | p5 | p6 | Id existente o estado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 63 | Edge por operación igual a probabilidad por ganancia media menos probabilidad por pérdida media | X | X | X | X | X | X | **HUECO `esperanza-matematica-del-edge`** | En p5 aparece como «Trading Egg»; en p1 y p4 como EG |
| 64 | Degradación del edge como proceso de reversión a la media | X | · | X | X | · | X | **HUECO `proceso-de-ornstein-uhlenbeck`** | Solo p3 y p4 escriben la ecuación con theta y sigma |
| 65 | Criterio objetivo de retiro cuando el edge cae bajo el coste de fricción | · | · | m | X | m | X | Incluido en `esperanza-matematica-del-edge` | p4 es el único que lo formaliza como desigualdad |
| 66 | Regla del 72 | X | X | X | X | X | X | **HUECO `regla-del-72`** | Seis de seis; no tiene id |
| 67 | Efecto billete de lotería y asimetría de lotería | X | X | X | X | X | X | Existe pero incompleto en `psicologia-del-trading` | Es un sesgo de distribución, no de conducta |
| 68 | Simulación del casino con 75 de 75 arruinados | · | X | X | X | X | X | Existe pero incompleto en `riesgo-de-ruina` | El temario no recoge el experimento |
| 69 | Criterio de Kelly para dimensionar la apuesta | · | m | · | m | m | · | `criterio-de-kelly` | Solo mención: nunca se escribe la fórmula ni se resuelve un caso |
| 70 | Asimetría de la composición: menos 50 por ciento exige más 100 por ciento | X | X | X | X | X | X | Incluido en `arrastre-de-volatilidad` | p6 añade el caso más 50 y menos 50 igual a menos 25 por ciento |
| 71 | Crítica a la hipótesis de eficiencia de mercado | X | X | X | X | X | X | **HUECO `eficiencia-de-mercado-critica`** | Ningún id del temario la trata; es el marco de todo el bloque quant |
| 72 | Alfa como retorno ortogonal a todos los factores | X | X | X | X | X | X | Existe pero incompleto en `alpha-y-beta` | El id habla de alfa y beta frente al mercado, no de ortogonalidad frente a todos los factores |
| 73 | CAPM explica entre el 50 % y el 70 % de la varianza de retornos | X | · | · | · | · | X | Existe pero incompleto en `alpha-y-beta` | Cifra concreta que no está en el temario |
| 74 | Regresión de alfa con SMB y HML | · | · | X | X | · | X | `factores-y-fama-french` | Existe |
| 75 | Rendimiento geométrico compuesto del portafolio cubierto frente al beta puro | · | X | X | X | X | X | Ejemplo, no concepto | Los importes no cuadran entre PDFs (ver 6.5) |

### 3.6 Arquitectura, proyectos y herramientas

| nº | Concepto | p1 | p2 | p3 | p4 | p5 | p6 | Id existente o estado | Observación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 76 | Qfin: librería en PyPI con arquitectura orientada a objetos | X | X | X | X | X | X | Proyecto, no concepto | Sus piezas ya están en F03 y F11 (`clases-y-objetos`, `funciones-y-modulos`, `testing-con-pytest`) |
| 77 | The Gaussian Cookbook: repositorio de esquemas gaussianos | X | X | X | X | X | X | Referencia externa | Se cita con documentación en SSRN; no hay URL en ningún PDF |
| 78 | Cuadro de mando en Streamlit con microdatos de Fannie Mae | X | X | X | X | · | X | Referencia y herramienta | Fannie Mae es el único conjunto de datos institucional nombrado |
| 79 | Sistema de trading de volatilidad de extremo a extremo (AMZN a 244, IV del 41 %, suelo en 229, cinco niveles) | X | X | X | X | · | X | Proyecto, no concepto | Mapea a `tamano-de-posicion` y `algoritmos-de-ejecucion` |
| 80 | Blog técnico como auditoría de lagunas conceptuales | X | X | X | X | · | X | No es concepto técnico | Es una práctica de estudio: encaja en F00 |
| 81 | Arquitectura defensiva para agentes: confianza cero, registro de solo apéndice, disyuntores, límites de API | X | m | · | m | m | · | Existe pero disperso en `resiliencia-de-servicios`, `seguridad-owasp` y `copias-de-seguridad-y-recuperacion` | p1 es el único que lo desarrolla como diseño |
| 82 | Incidente del Discord de Quant Guild con seis años de datos perdidos | · | · | · | X | · | · | Mapea a `copias-de-seguridad-y-recuperacion` | Caso real, no concepto |
| 83 | Matriz de especificación técnica para un agente de IA (concepto, ecuación, riesgo, directiva de código) | X | · | · | · | · | · | No está en el temario | Formato pedagógico, no concepto; no se propone |
| 84 | Principio de irreducibilidad computacional | X | · | X | X | X | · | **No propuesto** (ver 7.4) | Argumento filosófico contra la IA predictiva; no es contenido técnico verificable |
| 85 | Desigualdad de Paolucci, Palooian o Palucci según el PDF | · | · | X | X | X | · | **No propuesto** (ver 7.4) | Consigna motivacional, no matemática; el nombre cambia en cada texto |
| 86 | Motor de backtest por eventos frente a vectorizado (backtesting.py frente a VectorBT) | · | · | · | · | X | · | `backtesting-por-eventos`, `backtesting-vectorizado`, `vectorbt-backtrader-zipline` | Los tres ids existen; p5 solo los compara por velocidad |
| 87 | Programación genética de indicadores con función de fitness exponencial | · | · | · | · | X | · | **HUECO `programacion-genetica-y-regresion-simbolica`** | Único en todo el corpus; hay crossover del 90 %, mutación del 15 % y zona muerta |
| 88 | Estrategia intradía sobre VWAP de 15 minutos con stop ATR y cierre forzado | · | · | · | · | X | · | **HUECO descartado** (ver 7.3) | El propio texto muestra tasa de acierto del 49 % y colapso al 0,1 % de comisión |
| 89 | Detección geométrica de velas pin bar | · | · | · | · | X | · | **HUECO descartado** (ver 7.3) | Regla de tres desigualdades sobre máximos, mínimos, apertura y cierre |
| 90 | Estrategia multitemporal HMA y RSI con perturbación Monte Carlo de 500 ejecuciones | · | · | · | · | X | · | **HUECO descartado** (ver 7.3) | La parte de robustez sí mapea a `validacion-temporal` |
| 91 | Zona muerta o deadband del 10 % contra el sobreoperado | · | · | · | · | X | · | **HUECO descartado** | Detalle de implementación de la señal; cabe en `generacion-de-senales` |
| 92 | Fricción en alta frecuencia: del más 713 % sin comisión al menos 97 % con 0,1 % | · | · | · | · | X | · | Existe pero incompleto en `slippage-y-comisiones` | Es el mejor ejemplo numérico del corpus sobre costes |
| 93 | Activos y conjuntos de datos citados (NVDA, AMZN, AAPL, MSFT, GM, XAU/USD, BTC/USDT, EUR/USD, Fannie Mae) | X | X | X | X | X | X | `datos-de-mercado-y-acciones-corporativas` | Existe, aunque el temario no recoge series de materias primas ni de cripto |

**Recuento:** 93 conceptos inventariados. 29 son huecos con propuesta, 4 son huecos descartados
por interés formativo, 2 no se proponen por no ser contenido técnico y los 58 restantes ya tienen
`id` en el temario, completo o incompleto.

---

## 4. Huecos propuestos

**Nota metodológica.** La regla de usar solo `id` ya existentes como prerequisito tiene una
consecuencia que conviene explicitar: varios huecos nuevos se apoyan pedagógicamente en otros
huecos nuevos (griegas antes de cobertura, movimiento browniano antes de Karhunen-Loève). En la
columna de prerequisitos se ponen los `id` **existentes** más cercanos; el orden real de lectura
se indica en la columna de contenido. Los 29 `id` se han comprobado por búsqueda exacta contra
`CONTENIDO-TEMARIO.md`: ninguno colisiona. Los resúmenes están entre 80 y 170 caracteres.

### 4.1 Prioridad alta (10)

| Id | Fase | Nivel | Prerequisitos | Resumen | Qué debe contener la página |
| --- | --- | --- | --- | --- | --- |
| `correccion-point-in-time` | F04 | avanzado | `sesgo-de-mirar-al-futuro`, `scd-dimensiones-cambiantes`, `datos-de-mercado-y-acciones-corporativas` | Guardar cada dato con la fecha en que estuvo disponible y no con la del evento: la disciplina que separa un pipeline honesto de un backtest inflado. | Fecha de evento frente a fecha de publicación y revisiones. Casos: resultados trimestrales publicados una semana después, tráfico web y sentimiento. Aserción en el pipeline que corta por `t` y prueba que falla si alguien la salta. |
| `movimiento-browniano-geometrico` | F09 | avanzado | `distribuciones-continuas`, `logaritmos-y-escalas-logaritmicas`, `derivadas-parciales-y-gradiente` | La ecuación multiplicativa del precio: se resuelve con el lema de Ito, da niveles lognormales siempre positivos y explica el arrastre de volatilidad. | SDE, cambio de variable a logaritmo, solución cerrada, distribución del nivel y del log-retorno, esperanza frente a mediana. Simulación exacta frente a Euler y por qué la exacta no tiene sesgo por paso. |
| `lema-de-ito` | F09 | avanzado | `derivadas-parciales-y-gradiente`, `regla-de-la-cadena`, `integrales` | La regla de la cadena del cálculo estocástico: el término de segundo orden que convierte dW al cuadrado en dt y hace aparecer menos media sigma al cuadrado. | Expansión de Taylor a segundo orden, tabla de las tres reglas cuadráticas, cálculo de la variación cuadrática y aplicación al logaritmo. Error típico: derivar como en cálculo ordinario y perder el término corrector. |
| `expansion-karhunen-loeve` | F09 | experto | `autovalores-y-autovectores`, `descomposicion-svd`, `distribucion-normal-multivariante` | Descomponer un proceso gaussiano en senos ponderados por normales independientes: la versión continua de diagonalizar la matriz de covarianza. | Ecuación integral de Fredholm, derivación con la regla de Leibniz hasta la EDO armónica, autovalores y autofunciones, truncamiento con decaimiento O(k^-2) y su error. Equivalencia con Q lambda medio Z. |
| `griegas-black-scholes` | F09 | avanzado | `derivadas-parciales-y-gradiente`, `distribuciones-continuas`, `jacobiano-y-hessiano` | Delta, gamma, vega, theta y rho como derivadas parciales del precio de la opción: qué mide cada una y por qué las de orden superior no se cubren con el spot. | Fórmulas cerradas de las cinco, signo e interpretación económica, unidades de vega y theta. Por qué el subyacente tiene delta uno, gamma cero y vega cero. |
| `cobertura-delta-gamma-vega` | F09 | experto | `operaciones-matriciales`, `determinante-rango-invertibilidad`, `microestructura-de-mercado` | Neutralizar varios riesgos a la vez resolviendo un sistema con las griegas: hacen falta n menos una opciones para n menos una sensibilidades no lineales. | Planteamiento matricial, resolución, delta residual y ajuste con el spot. Mal condicionamiento y redondeo previo. Requisito de lectura: `griegas-black-scholes`. |
| `esperanza-matematica-del-edge` | F09 | intermedio | `valor-esperado`, `generacion-de-senales`, `ratio-de-sharpe` | El valor esperado por operación, probabilidad por ganancia media menos probabilidad por pérdida media, y su uso como interruptor cuando cae bajo las fricciones. | Deducción por ley de la esperanza total, ejemplo numérico con y sin fricción y regla de desconexión cuando el edge rodante no supera el coste. Error típico: tratar la tasa de acierto como constante. |
| `eficiencia-de-mercado-critica` | F09 | intermedio | `que-es-un-mercado`, `microestructura-de-mercado`, `momentum` | Qué sostiene la hipótesis de eficiencia, en qué versiones se formula y por qué el precio es una expectativa temporal y no el valor justo inalterable. | Las tres formas débil, semifiuerte y fuerte, qué evidencia las apoya y qué las rompe. Choques de flujo, brechas de liquidez y expectativas rotas como origen del alfa. Postura del temario, sin convertirla en opinión. |
| `universo-de-inversion-point-in-time` | F04 | avanzado | `sesgo-de-supervivencia`, `datos-de-mercado-y-acciones-corporativas`, `scd-dimensiones-cambiantes` | Reconstruir qué empresas existían y cotizaban en cada fecha, incluidas las que quebraron: sin el cementerio bursátil el backtest transversal miente. | Fuentes de altas, bajas y cambios de ticker, pertenencia histórica a índice y capitalización flotante. Coste de mantenerlo y cómo probarlo contra un índice conocido. |
| `cadenas-de-markov-y-estados-absorbentes` | F09 | avanzado | `probabilidad-condicional`, `maxima-verosimilitud`, `operaciones-matriciales` | Modelar la morosidad como transiciones entre estados con uno absorbente: matriz estimada por máxima verosimilitud y potencias de Chapman-Kolmogorov. | Conteo de transiciones y normalización de filas, restricción de suma uno, estados absorbentes, matriz fundamental y tiempo esperado. No estacionariedad y sensibilidad a la ventana de calibración. |

### 4.2 Prioridad media (12)

| Id | Fase | Nivel | Prerequisitos | Resumen | Qué debe contener la página |
| --- | --- | --- | --- | --- | --- |
| `movimiento-browniano-aritmetico` | F09 | intermedio | `distribuciones-continuas`, `distribucion-normal-multivariante`, `valor-esperado` | El browniano aditivo y su hueco real: precios normales que admiten valores negativos, útiles en tipos de interés y en materias primas con almacenamiento caro. | SDE aditiva, solución por integración directa, distribución del nivel, esperanza y varianza lineales. Cuándo es aceptable un precio negativo: tipos y crudo con coste de almacenamiento. |
| `proceso-de-wiener` | F09 | intermedio | `distribuciones-continuas`, `independencia-y-condicionamiento` | El proceso gaussiano de incrementos independientes y varianza proporcional al tiempo: el ladrillo del que están hechos casi todos los modelos de precio. | Definición, propiedades de los incrementos, continuidad de trayectorias y no derivabilidad. Por qué no sirve como serie de precios tal cual. |
| `ecuaciones-diferenciales-estocasticas` | F09 | avanzado | `derivadas-parciales-y-gradiente`, `variable-aleatoria`, `distribucion-normal-multivariante` | Una ecuación que describe el cambio de una variable cuando parte del cambio es aleatorio: deriva, difusión y por qué la solución cerrada no siempre existe. | Forma diferencial, término de deriva y de difusión, condición de Lipschitz para existencia y unicidad, cuándo hay solución cerrada y cuándo solo numérica. |
| `simulacion-euler-maruyama` | F09 | avanzado | `simulacion-de-monte-carlo`, `numpy-fundamentos`, `vectorizacion` | Discretizar una ecuación estocástica para generar trayectorias: el esquema explícito, su error por paso y cuándo conviene la solución exacta en lugar del Euler. | Esquema, orden de convergencia, sesgo por paso grande, comparación con la solución exacta del geométrico y vectorización de N caminos por M pasos. |
| `puente-browniano` | F09 | avanzado | `distribuciones-continuas`, `covarianza-y-correlacion`, `autovalores-y-autovectores` | Un browniano atado a empezar y acabar en cero: covarianza mínimo menos producto, simulación espectral y uso para rellenar el hueco nocturno del precio. | Covarianza, condicionamiento en los extremos, simulación por KL y por interpolación gaussiana, y aplicación al tramo entre cierre y apertura. |
| `simulacion-normal-multivariante` | F09 | intermedio | `distribucion-normal-multivariante`, `autovalores-y-autovectores`, `numpy-fundamentos` | Generar vectores normales con una covarianza dada: Cholesky frente a diagonalización espectral, y qué pasa cuando la matriz no es definida positiva. | Cholesky, espectro, X igual a Q lambda medio Z y demostración de que la covarianza se conserva. Autovalores negativos por error numérico y qué hacer. |
| `arrastre-de-volatilidad` | F09 | intermedio | `retornos-logaritmicos`, `varianza-y-desviacion`, `maximo-drawdown` | Por qué la media geométrica cae bajo la aritmética en media varianza: una caída del 50 por ciento exige un 100 para volver y la varianza se come el compuesto. | Diferencia entre media aritmética y geométrica, fórmula aproximada, casos con números y efecto del tamaño de posición. Cómo se mitiga. |
| `regla-del-72` | F09 | básico | `logaritmos-y-escalas-logaritmicas`, `valor-esperado` | Duplicar capital a tanto por ciento anual: 72 entre la tasa da los años, y su reverso explica por qué una caída grande no se compensa con una subida igual. | Deducción a partir del logaritmo de dos, tabla de tasas, límites de la aproximación y enlace con la asimetría de la composición. |
| `ausencia-de-contrafactuales` | F09 | intermedio | `poblacion-y-muestra`, `estacionariedad`, `validacion-temporal` | El mercado ocurre una sola vez: sin repetición del experimento no hay convergencia asintótica y una racha ganadora no distingue modelo de suerte. | Qué exige un experimento repetible, por qué el mercado no lo permite, consecuencia sobre la inferencia y qué se puede hacer en su lugar: remuestreo, validación temporal y simulación. |
| `cobertura-de-cola` | F09 | avanzado | `var-y-cvar`, `maximo-drawdown`, `construccion-de-carteras` | Comprar protección frente al evento extremo aunque duela en los años buenos: coste anual frente a reducción de la caída máxima y su efecto en el compuesto. | Coste de la cobertura en años alcistas, ahorro en años de caída, cálculo del compuesto con y sin cobertura y condiciones en que deja de compensar. |
| `proceso-de-ornstein-uhlenbeck` | F09 | avanzado | `reversion-a-la-media`, `estacionariedad`, `distribuciones-continuas` | El proceso que revierte a una media con velocidad theta: modela desde el tipo de interés hasta el deterioro de la tasa de acierto de una estrategia. | Ecuación, solución, media y varianza de largo plazo y tiempo de reversión. Estimación por regresión y uso para decidir el retiro de una señal. |
| `modelo-de-black-scholes` | F09 | experto | `distribuciones-continuas`, `valor-esperado`, `curva-de-tipos-y-descuento` | El precio de una opción europea como esperanza descontada del pago bajo medida neutral al riesgo: de dónde sale y qué supuestos impone. | Cartera replicante, medida neutral, fórmula y sus cinco supuestos. Qué falla en la práctica: volatilidad no constante, colas y sonrisa. Es el prerrequisito lógico de `griegas-black-scholes` y de `volatilidad-implicita`. |

### 4.3 Prioridad baja (7)

| Id | Fase | Nivel | Prerequisitos | Resumen | Qué debe contener la página |
| --- | --- | --- | --- | --- | --- |
| `movimiento-browniano-fraccionario` | F09 | experto | `hurst-y-memoria`, `covarianza-y-correlacion`, `distribuciones-continuas` | El proceso gaussiano cuyo parámetro de Hurst fija rugosidad y memoria: incrementos correlacionados que el browniano estándar no puede representar. | Función de covarianza con las potencias dos H, incrementos correlacionados, casos H menor, igual y mayor que 0,5 y por qué se usa en volatilidad rugosa. |
| `davies-harte-y-fft` | F09 | experto | `hurst-y-memoria`, `divide-y-venceras`, `autovalores-y-autovectores` | Simular un proceso gaussiano estacionario sin factorizar la covarianza: incrustar la matriz de Toeplitz en una circulante y diagonalizarla con la FFT. | Toeplitz incrustada en circulante de 2N, autovalores por transformada discreta, complejidad O(N log N) frente a O(N al cubo) de Cholesky y condiciones de definición positiva. |
| `procesos-de-volterra` | F09 | experto | `integrales`, `hurst-y-memoria`, `covarianza-y-correlacion` | Procesos definidos por una integral con núcleo dependiente del tiempo: la familia que contiene al browniano fraccionario y sostiene la volatilidad rugosa. | Integral con núcleo K de t y s, núcleos singulares, relación con el fraccionario y con Rough Bergomi. Solo mención en los PDFs: aquí hay que desarrollar de cero. |
| `metodo-de-aceptacion-rechazo` | F01 | intermedio | `variable-aleatoria`, `distribuciones-continuas`, `probabilidad-condicional` | Muestrear cualquier densidad acotada dibujando puntos en un rectángulo y descartando los de fuera: tasa de aceptación y coste disparado en las colas. | Algoritmo, cálculo de la constante de envolvente, tasa de aceptación analítica y comparativa normal frente a triangular. Cuándo la transformada inversa es mejor. |
| `modelo-de-bachelier` | F09 | experto | `distribuciones-continuas`, `valor-esperado`, `curva-de-tipos-y-descuento` | Valorar una opción suponiendo subyacente normal y no lognormal: la fórmula de 1900 que sigue siendo estándar cuando los tipos pueden ser negativos. | SDE sin deriva bajo medida neutral, derivación de la prima con la densidad normal, volatilidad en unidades absolutas y superioridad en swaptions y caplets. |
| `volatilidad-implicita` | F09 | avanzado | `volatilidad-realizada`, `distribuciones-continuas`, `busqueda-binaria` | La volatilidad que metida en Black-Scholes devuelve el precio de mercado: se invierte numéricamente y se usa como nivel de referencia y suelo. | Inversión numérica del precio, por qué no hay fórmula cerrada, sonrisa y estructura temporal, y el uso como suelo para reglas de reversión a la media. |
| `programacion-genetica-y-regresion-simbolica` | F06 | experto | `seleccion-de-hiperparametros`, `arboles-de-decision`, `seleccion-de-features` | Evolucionar fórmulas en vez de ajustar constantes: población de árboles, función de fitness, cruce y mutación, y el enorme riesgo de data snooping que introduce. | Representación en árbol, primitivas, fitness, selección del top 10 por ciento, cruce y mutación, zona muerta contra sobreoperado. Advertencia explícita: el fitness sobre retorno histórico es una fábrica de sobreajuste. |

**Distribución por fase:** F01 uno, F04 dos, F06 uno, F09 veinticinco. La concentración en F09 no
es un error de clasificación: el temario dedica 54 conceptos a lo quant y **ninguno a valoración
de derivados**, y de ese vacío salen cinco de los huecos (Bachelier, Black-Scholes, griegas,
cobertura y volatilidad implícita); otros cuatro (Karhunen-Loève, browniano fraccionario,
Volterra y Davies-Harte) salen de que el temario no tiene **ningún proceso estocástico de tiempo
continuo** más allá de `hurst-y-memoria` y `garch-volatilidad`.

---

## 5. Conceptos existentes que hay que enriquecer

| Id existente | Qué falta en la página | De qué PDF sale |
| --- | --- | --- |
| `sesgo-de-mirar-al-futuro` | El formalismo de la filtración y la teoría de las dos envolventes; el caso concreto del ranking por deciles normalizado con la semana siguiente; la alineación de datos alternativos por fecha de publicación | p1, p2, p3, p4, p5, p6 |
| `sesgo-de-supervivencia` | La analogía de Abraham Wald con su conclusión (blindar donde **no** hay impactos) y el efecto sobre las ponderaciones de una cartera long/short transversal | p3, p5, p6 |
| `data-snooping-y-multiple-testing` | El caso de las medias móviles 3/5 frente a 7/12 y la prueba de estabilidad local (7/12 frente a 8/12); la distinción entre memorizar ruido y capturar estructura | p1 a p6 |
| `validacion-temporal` | El procedimiento walk-forward explícito con tamaño de ventana, solape y criterio de aceptación; la meseta de rendimiento como test | p1 a p6 |
| `ratio-de-sharpe` | El uso diagnóstico del Sharpe anómalo como síntoma de fuga, con los dos umbrales que citan los textos (3,0 como alarma, 0,9 a 1,2 como resultado real) y el matiz de que 0,9 es más peligroso que negativo | p2, p6 |
| `slippage-y-comisiones` | La regla de descarte previo (sin edge teórico la fricción no lo crea) y el ejemplo del 713 % que pasa a menos 97 % con una comisión del 0,1 % | p5, p6 |
| `alpha-y-beta` | La definición de alfa como retorno ortogonal a todos los factores, la crítica al exceso sobre índice y la cifra de que el CAPM solo explica entre el 50 % y el 70 % | p1, p2, p3, p4, p5, p6 |
| `pca` | La equivalencia SVD-covarianza con lambda igual a sigma al cuadrado entre n menos uno, la interpretación de las cargas por componente y la no estacionariedad en ventanas de 60 días | p1 a p6 |
| `descomposicion-svd` | La demostración de que los vectores singulares derechos de la matriz de datos son los autovectores de la covarianza | p1 a p6 |
| `determinante-rango-invertibilidad` | El número de condición, el umbral práctico de 1e5 y el redondeo previo a invertir una matriz de griegas | p1, p3 |
| `estimadores-y-propiedades` | La corrección de Bessel y el detalle de `ddof=1`: sin él la varianza muestral está sesgada y todo contraste posterior hereda el sesgo | p1, p4, p5 |
| `intervalos-de-confianza` | El desarrollo completo: parámetro fijo, límites aleatorios, los tres muestreos y las tres falacias concretas del trading comercial | p4 |
| `test-t` | La justificación del pivote de t a normal con n mayor que 30 y el criterio para elegir Z o t según se conozca la varianza poblacional | p2, p3, p4 |
| `hurst-y-memoria` | El proceso fraccionario completo: función de covarianza, incrementos correlacionados y simulación | p1, p2, p3, p4, p6 |
| `maxima-verosimilitud` | El caso de la matriz de transición: contar transiciones, normalizar por filas y respetar la restricción de suma uno | p1, p2, p3, p4, p6 |
| `riesgo-de-ruina` | La simulación del casino con 75 jugadores y la idea de que el mercado cobra el papel de la casa | p2, p3, p4, p5, p6 |
| `criterio-de-kelly` | Prácticamente todo: los textos solo lo mencionan como la alternativa a no dimensionar; nunca escriben la fórmula ni un caso | p2, p4, p5 |
| `simulacion-de-monte-carlo` | La valoración de opciones dependientes de trayectoria y la perturbación aleatoria de parámetros como prueba de robustez frente al sobreajuste | p1 a p6 |
| `suavizado-exponencial` | El uso de la media rodante con bandas de más menos una desviación como diagnóstico de progreso, no como método de pronóstico | p1, p2, p4, p5 |
| `backtesting-por-eventos` y `backtesting-vectorizado` | La comparación práctica: fidelidad por evento frente a velocidad matricial, con el coste de las 15.000 evaluaciones de la programación genética | p5 |
| `fuga-de-datos` | El caso financiero del mismo error: la fuga vista desde un pipeline de machine learning y desde un backtest son la misma cosa con distinto nombre | p1 a p6 |
| `resiliencia-de-servicios` | El paquete completo de confianza cero, registro de solo apéndice, disyuntores y límites de API aplicado a un agente que opera capital | p1, p4 |

**Lo que el temario tiene y los PDFs ignoran.** Conviene decirlo porque afecta a la redacción de
las páginas: los seis informes **no mencionan** a López de Prado, ni el etiquetado por triple
barrera, ni el meta-etiquetado, ni los pesos por unicidad, ni la diferenciación fraccional, ni el
k-fold con purga y embargo, ni la validación combinatoria, ni el Sharpe deflactado. Es
exactamente el bloque «Etiquetado y validación» de F09 (8 conceptos), que ya está en el temario y
que los PDFs no cubren en absoluto. Tampoco cubren GARCH, ni las cadenas de Markov ocultas, ni
la cointegración, ni VaR y CVaR, ni Markowitz, ni FIX, ni la venta en corto, ni el protocolo de
ejecución más allá del VWAP como señal.

---

## 6. Fórmulas, trampas y referencias citadas

### 6.1 Fórmulas citadas

**Procesos estocásticos**

- Movimiento browniano aritmético: `dS_t = μ dt + σ dW_t`, con solución `S_t = S_0 + μ t + σ W_t` y distribución `N(S_0 + μ t, σ² t)`.
- Movimiento browniano geométrico: `dS_t = μ S_t dt + σ S_t dW_t`, con solución `S_t = S_0 exp((μ − ½σ²) t + σ W_t)`.
- Lema de Itô para `f(t, S)`: `df = (∂f/∂t + μ S ∂f/∂S + ½ σ² S² ∂²f/∂S²) dt + σ S (∂f/∂S) dW`.
- Reglas cuadráticas: `(dt)² = 0`, `dt·dW_t = 0`, `(dW_t)² = dt`.
- Covarianza del puente browniano: `K_B(s,t) = min(s,t) − s·t` (general `min(s,t) − s·t/T`).
- Ecuación integral de Fredholm: `∫ K_B(s,t) e_k(s) ds = λ_k e_k(t)`.
- EDO del puente: `λ_k e''_k(t) + e_k(t) = 0`, con `λ_k = 1/(kπ)²` y `e_k(t) = √2 sin(kπ t)`.
- Serie de Karhunen-Loève: `B_t = √2 Σ Z_k sin(kπ t)/(kπ)` con `Z_k ~ N(0,1)` i.i.d.
- Error de truncamiento: `Error(K) = Σ_{k>K} 1/(kπ)²`, con decaimiento `λ_k = O(k⁻²)`.
- Versión discreta: `Σ = Q Λ Qᵀ` y `X_t = Q Λ^(1/2) Z_t`.
- Covarianza del browniano fraccionario: `E[B_H(s) B_H(t)] = ½ ( |s|^(2H) + |t|^(2H) − |s−t|^(2H) )`.
- Proceso de Volterra: `X_t = ∫₀ᵗ K(t,s) dW_s`.
- Esquema de Euler-Maruyama: `S_{t+Δt} = S_t + a(t,S_t) Δt + b(t,S_t) ΔW_t` con `ΔW_t ~ N(0, Δt)`.
- Arrastre de volatilidad: `R_g ≈ R_a − ½σ²`; y `−½σ²` como término corrector de la media geométrica.
- Proceso de Ornstein-Uhlenbeck para la tasa de acierto: `dP_win(t) = θ (P̄_win − P_win(t)) dt + σ_p dW_t`.

**Simulación**

- Aceptación y rechazo: `P(aceptar) = 1 / ((b−a)·M)`; normal estándar truncada a ±4σ: `M = 0,3989`, `A_rect = 3,1915`, aceptación `31,33 %`; triangular simétrica: `M = 2/(b−a)`, aceptación `50 %`.
- Conservación de covarianza: `Cov(Q Λ^(1/2) Z) = Q Λ Qᵀ = Σ`.
- Davies-Harte: Toeplitz incrustada en circulante de `2N`, diagonalizada por FFT, coste `O(N log N)` frente a `O(N³)` de Cholesky.

**Derivados**

- Modelo de Bachelier: `C = e^(−rT) [ (F_0 − K) Φ(d_B) + σ_B √T φ(d_B) ]` con `d_B = (F_0 − K)/(σ_B √T)`.
- Griegas de Black-Scholes: `Δ = Φ(d_1)`, `Γ = φ(d_1)/(S σ √τ)`, `V = S √τ φ(d_1)`, `Θ = −S φ(d_1) σ/(2√τ) − r K e^(−rτ) Φ(d_2)`, `ρ = K τ e^(−rτ) Φ(d_2)`.
- Cobertura multi-griega: `[Γ_A Γ_B ; V_A V_B] · [w_A ; w_B] = [−Γ_port ; −V_port]`, con `w_A = 8641`, `w_B = −8006`, delta residual `−46` y ajuste `+46` acciones.
- Condición de la matriz: `np.linalg.cond(G) < 1e5`, con redondeo previo `np.round(greeks, 2)`.

**Álgebra y estadística**

- Covarianza muestral: `S = XᵀX/(n−1)`; SVD `X = U Σ Vᵀ`; identidad `λ_i = σ_i²/(n−1)`.
- Ley de los grandes números: `X̄_n →P μ`; teorema central del límite: `Z = (X̄_n − μ)/(σ/√n) →d N(0,1)`.
- Insesgadez y varianza: `E[X̄_n] = μ`, `Var(X̄_n) = σ²/n`.
- Contraste: `t = (X̄ − μ_0)/(s/√n) ~ t_{n−1}`; `Z = (X̄ − μ_0)/(s/√n)`.
- Corrección de Bessel: `s² = Σ(X_i − X̄)²/(n−1)`, en código `ddof=1`.
- Media rodante: `Ȳ_roll(t,k) = (1/k) Σ_{i=t−k+1}^{t} Y_i` con banda `± σ_roll`.
- Edge: `EG = P(ganar)·W̄ − P(perder)·L̄`; retiro si `EG ≤ C_fricción`.
- Alfa ortogonal: `R_i − R_f = α + Σ β_k F_k + ε_i` con `E[ε_i · F_k] = 0`.
- Regresión con factores: `R_i − R_f = α + β_1(R_m − R_f) + β_2 SMB + β_3 HML + ε_i`.
- Ruptura de correlación: `lim (σ_mkt → ∞) ρ_ij → 1,0`.
- Cadenas de Markov: `P^(n) = P^n`; `p̂_ij = n_ij / Σ_l n_il`; matriz fundamental `N = (I − Q)⁻¹`.
- Regla del 72: `t ≈ 72 / r%`; composición `(1+r_1)(1+r_2) − 1`.
- Programación genética: `Fitness = exp(−Retorno total)`.

### 6.2 Trampas que los textos denuncian

1. **Look-ahead bias.** Abrir el «sobre 2». Variantes concretas que citan: normalizar con la media, el máximo o el mínimo de toda la muestra; cruzar datos alternativos por fecha de evento y no de publicación; usar estados financieros una semana antes de que existieran.
2. **Data snooping, overfitting y p-hacking.** Probar cientos de combinaciones y quedarse con la mejor. Síntoma: colapso al perturbar un parámetro.
3. **Sesgo de supervivencia.** El universo de hoy aplicado al pasado. El «cementerio bursátil».
4. **Ficción de costes.** Backtest sin comisiones, sin horquilla y sin deslizamiento.
5. **Mala interpretación del p-valor** (p3, p4, p6): confundir la probabilidad de los datos dado el modelo con la probabilidad del modelo dados los datos, y la tasa de acierto histórica con la probabilidad del siguiente trade.
6. **Mala interpretación del intervalo de confianza** (solo p4): creer que hay un 95 % de probabilidad de que el parámetro esté dentro de un intervalo ya calculado. El parámetro es fijo; los límites son aleatorios. Para un intervalo ya calculado la probabilidad es 1 o 0.
7. **Confundir convergencia asintótica con rentabilidad en muestras finitas.** Que la media converja no dice nada sobre los próximos veinte trades.
8. **Confundir alfa con exceso sobre un índice.** Sobrecargar tecnología no es alfa, es beta sectorial.
9. **Ignorar el arrastre de volatilidad.** Menos 50 % exige más 100 %; más 50 % y menos 50 % deja menos 25 %.
10. **Creer que más volatilidad es más rentabilidad.** Efecto billete de lotería.
11. **Asumir estacionariedad.** En la matriz de transición de crédito (ventana de 3 meses), en las cargas del PCA (ventana de 60 días) y en la tasa de acierto.
12. **Ignorar el mal condicionamiento** de una matriz de griegas antes de invertirla.
13. **Delegar privilegios de administración en componentes automatizados** (p1): el evento de cola izquierda administrativo.
14. **Confundir la IA con una bola de cristal.** Un modelo aproxima una esperanza condicional; no ejecuta el futuro.

### 6.3 Nombres propios, herramientas y repositorios

- **Personas:** Abraham Wald (sesgo de supervivencia), Craig Percoco (mencionado en p4 como ejemplo de mala interpretación estadística), «Paolucci», «Palooian» o «Palucci» según el PDF (la desigualdad de acción e iteración, con el apellido mal escrito de tres formas distintas).
- **Repositorios y librerías:** `qfin` (PyPI, `pip install qfin`), **The Gaussian Cookbook** (repositorio abierto con documentación en SSRN), `backtesting.py`, **VectorBT**, `numpy`, `scipy.linalg` (`eigh`), `Streamlit`, `pandas`, `sklearn.model_selection.TimeSeriesSplit`, `np.linalg.inv`, `np.linalg.cond`, `np.fft`.
- **Modelos y marcos citados:** Black-Scholes, Black-Scholes-Merton, Bachelier (1900), CAPM, Fama-French (SMB y HML), Rough Bergomi, Rough Volatility, Hull Moving Average, RSI, EMA, ATR, VWAP, regresión lineal de 50 periodos, programación genética.
- **Datos y activos:** microdatos hipotecarios de **Fannie Mae**; NVDA (543, K 545, IV 53 %, T 30/365, r 1,5 %); AMZN (244, IV 41 % a 42 %, suelo 229); AAPL en 15 minutos; XAU/USD en 1 hora durante 6 años; BTC/USDT en 4 horas y 1 día durante 9 años; EUR/USD, GBP/USD, AUD/USD y USD/JPY; crudo WTI de abril de 2020.
- **Comunidad:** el servidor de Discord de **Quant Guild**, con seis años de canales borrados por un moderador.
- **Fuentes de vídeo de p4** (18 títulos, sin URL ni canal): *Applied Statistics and Statistical Inference*; *A Quant's Visual Guide to Progress*; *Correcting the Interpretation of a Confidence Interval*; *Craig Percoco Doesn't Understand Statistics*; *Arithmetic and Geometric Brownian Motion Masterclass*; *Arithmetic Brownian Motion in Python*; *A Quant Derives the Karhunen–Loève Expansion of the Brownian Bridge in Continuous-Time*; *Bachelier Model Call Option Price Derivation*; *Analyzing Stock Returns with Principal Component Analysis in Python*; *5 Projects that Made me a Quant*; *Algorithmic Multi-Greek Hedging using Python*; *A REAL Quant Debunks the «Day Trading» Scam*; *3 Backtesting Pitfalls That Ruin Your Trading Strategy*; *Backtesting Quant Strats in Python*; *Analyzing Trading Strategy Performance Over Time*; *6 Years of Data, POOF, Gone.*; *Academia is wrong. Markets aren't efficient. Alpha is a homerun.*; *AI Isn't Killing Math. It's Exposing Mathematicians.*

### 6.4 Errores e inconsistencias **dentro** de los PDFs (hallazgo propio)

Esto no es lo que los textos denuncian: es lo que los textos hacen mal. Importa porque si estos
documentos se usan como fuente para las páginas del temario, los números se copiarían.

1. **Aritmética rota en p2.** Escribe que `1,288 × 0,800 − 1 = +1,88 %` (es `+3,04 %`) y que
   `1,143 × 0,980 − 1 = +6,00 %` (es `+12,01 %`). p5 corrige exactamente estos dos números y
   dedica un párrafo a la «nota de conciliación», pero sin citar a p2.
2. **El mismo caso del balón con tres juegos de datos y cuatro versiones.** p1 y p4 dan media 0,38
   con s 0,188 y Z igual a −9,0; p5 da media 0,375 con s 0,216 y Z igual a −8,185 (y un p-valor de
   1,34e−16); p6 da media 0,40 con s 0,20 y Z igual a −7,07. Tres «demostraciones» del mismo
   ejemplo con datos distintos y ninguna reproducible.
3. **La matriz de griegas no coincide entre PDFs y el resultado siempre es el mismo.** p1 usa
   Γ_A 0,0058 y V_A 0,28 con deltas 0,48 y 0,42; p2 usa Γ_A 0,00612 y V_A 0,7812; p5 usa Γ_A
   0,0125 y V_A 0,8540 con deltas 0,520 y 0,480; p6 usa una matriz de 0,0012 y 0,1050. Los cuatro
   llegan a `w_A = 8641` y `w_B = −8006` y a un delta residual de −46. Con esos insumos el
   resultado no puede ser el mismo: los pesos están copiados, no calculados. Peor: p5 presenta
   `w_A = +864,1` y `w_B = −800,6` (un orden de magnitud menos) manteniendo el delta residual de
   −46.
4. **Umbral de Sharpe contradictorio.** p2 y p1 consideran sospechoso un Sharpe entre 1,5 y 3,0;
   p6 considera sospechoso un Sharpe entre 1,5 y 1,7, que es un rango perfectamente normal.
5. **El Sharpe in-sample del ejemplo de sobreajuste cambia:** +2,2 y +2,1 en el mismo p2 (dos cifras
   para el mismo dato), +1,7 en p6 y «entre 1,5 y 3,0» en p1.
6. **Truncamiento espectral con tres cifras distintas:** `K ≈ 20 a 50` en p4, `K = 50 o 500` en
   p6, `K = 100 o 500` con fidelidad del 99,99 % en p5.
7. **Varianza explicada por PC2:** 25 % en p1, 27 % en p2, p3, p5 y p6. La de PC1 en estrés:
   «por debajo del 50 %» en p1, «más del 75 %» en p4, «más del 80 %» en p2 y p3, «75 % a 80 %» en p5.
8. **Caída que exige recuperación:** p5 dice que una caída del 50 % exige un 100 % para volver y
   p4 dice que una del 20 % exige un 25 %. Ambas son correctas, pero se presentan como si fueran
   el mismo argumento.
9. **Dictamen del Sharpe real:** «Sharpe real menor que 0 o mediocre 0,9 a 1,2» (p1) convive con
   «Sharpe de 0,9 a 1,2 polucionado e inviable» (p2) y con «niveles insignificantes 0,9, 1,2»
   (p3). Tres formas de decir lo mismo con tres conclusiones distintas.
10. **El nombre de la desigualdad final:** Paolucci en p3, Palooian en p4, Palucci en p5. En p1 ni
    se nombra. Un concepto con tres grafías no es un concepto.
11. **El Gaussian Cookbook cambia de naturaleza según el texto:** «recetario de procesos gaussianos»
    en p1, «plataforma interactiva» en p4, «repositorio y compilatorio técnico» en p6, y sin URL en
    ninguno de los seis. Un repositorio que se cita cuatro veces de cuatro formas no es verificable.

Ninguna de estas inconsistencias invalida el contenido conceptual, pero sí invalida el uso de sus
números como ejemplo verificado. Si una página del temario necesita un ejemplo numérico, hay que
recalcularlo.

---

## 7. Qué NO sirve para data engineering

El temario es «de cero a data engineer + data scientist» con una ruta `quant` dentro. Buena parte
de estos seis informes no pertenece a ese proyecto: pertenece al mundo de la mesa de derivados o
al del trading minorista. Conviene separarlo porque, si se mezcla, el alumno acaba aprendiendo a
invertir matrices de griegas antes de saber qué es una clave foránea.

### 7.1 Todo el bloque de valoración de derivados

Cobertura delta-gamma-vega, griegas de Black-Scholes, modelo de Bachelier, Black-Scholes y
volatilidad implícita. **Por qué no sirve:** ninguno de estos conceptos aparece en un pipeline de
datos. Requieren un modelo de valoración, una superficie de volatilidad y una cartera de opciones
reales; sin eso no hay nada que calcular. La única pieza transferible es el álgebra: montar un
sistema lineal, detectar que la matriz está mal condicionada y entender por qué invertir a ciegas
produce basura. Eso ya está cubierto por `determinante-rango-invertibilidad` y
`operaciones-matriciales`, y el resto es un nicho de mesa de opciones, no de ingeniería de datos.
Los cinco huecos de derivados se proponen porque el temario tiene una ruta `quant` declarada y
dejarla sin derivados es una laguna visible, pero **deberían marcarse como ruta `quant` opcional
y nunca como `core`**.

### 7.2 Los procesos gaussianos avanzados

Karhunen-Loève, movimiento browniano fraccionario, procesos de Volterra, Davies-Harte, puente
browniano aplicado al hueco nocturno. **Por qué no sirve:** es matemática seria y bien expuesta,
pero es cultura, no herramienta. Un data engineer no va a simular trayectorias con covarianza
exacta para entregar un pipeline. Lo que sí se aprovecha es la idea general —que simular con la
covarianza mal truncada sesga el resultado, y que una matriz con estructura (Toeplitz, circulante)
se resuelve con FFT en lugar de con factorización densa— y esa idea se explica en dos párrafos,
no en cuatro páginas. La aplicación del puente al hueco entre el cierre y la apertura (p2) es
ingeniosa y completamente inútil para el 99 % de los alumnos.

### 7.3 El bloque de técnica minorista (p5, sección 4)

VWAP intradía de 15 minutos, pin bar, HMA con RSI, zona muerta del 10 % y programación genética de
indicadores. **Por qué no sirve:** es el único bloque con contenido operativo original y es el que
peor envejece. Los propios números del texto lo desmienten: la estrategia de pin bar pura da
menos 2 % en seis años con una caída máxima del 43 % y una tasa de acierto del 38 %; la de VWAP da
una tasa de acierto del 49 % y pasa de más 713 % a menos 97 % al aplicar una comisión del 0,1 %.
Es decir, el documento demuestra que su propia sección 4 no funciona. Además contradice el resto
del corpus, que sostiene que los indicadores técnicos rezagados no tienen ventaja estadística.
Para el temario solo hay dos cosas rescatables: el ejemplo del colapso por comisiones (que
pertenece a `slippage-y-comisiones`) y la idea de perturbar parámetros para medir robustez (que
pertenece a `validacion-temporal`). El resto son cuatro «huecos descartados» del inventario. La
programación genética es la excepción: se propone en F06, pero no como técnica de trading sino
como ejemplo de búsqueda automática de fórmulas con un riesgo de sobreajuste enorme.

### 7.4 La retórica motivacional

La desigualdad de Paolucci, Palooian o Palucci, la analogía del jardín, el «jardín cuantitativo»,
el «escena de un crimen», el home run del béisbol, el casino con 75 jugadores y la crítica a la
academia. **Por qué no sirve:** no es contenido verificable. La analogía del béisbol es una forma
aceptable de introducir el alfa ortogonal y el casino ilustra bien el riesgo de ruina, pero
convertirlas en secciones propias es relleno. La «desigualdad» no es una desigualdad matemática:
es un eslogan, y además aparece con tres apellidos distintos, lo que la descalifica como
referencia. En el fichero no se propone `id` para ella ni para el «principio de irreducibilidad
computacional»: no son contenido técnico comprobable y una página sobre ellos no admitiría ni un
ejemplo con código ni una pregunta de comprobación con respuesta correcta.

### 7.5 Lo que sí transfiere, y conviene separar del ruido

| Bloque de los PDFs | A qué `id` del temario va | Por qué sirve fuera de las finanzas |
| --- | --- | --- |
| Alineación point-in-time de datos | `sesgo-de-mirar-al-futuro` y el hueco `correccion-point-in-time` | Es el mismo problema que el *point-in-time join* de un almacén: 90 % ingeniería, 10 % estadística |
| Reconstrucción del universo histórico | hueco `universo-de-inversion-point-in-time` | Es un problema de dimensiones que cambian en el tiempo, es decir, SCD de manual |
| Matriz de transición estimada por conteo | `maxima-verosimilitud` y el hueco de cadenas de Markov | Es un `groupby` con normalización por filas; el ejemplo perfecto de estadística que se implementa con SQL |
| Equivalencia SVD-covarianza | `pca` y `descomposicion-svd` | Explica de una vez por qué dos funciones distintas de la misma librería dan lo mismo |
| Ley de grandes números, central del límite, t, potencia | `ley-de-los-grandes-numeros`, `teorema-central-del-limite`, `test-t` | Base de cualquier test A/B |
| Walk-forward y estabilidad paramétrica | `validacion-temporal` | Es validación temporal aplicada a cualquier serie, no solo a precios |
| Modelado explícito de fricciones | `slippage-y-comisiones` | Enseña que un modelo sin costes no es un modelo, es una esperanza |
| Confianza cero, solo apéndice, disyuntores | `resiliencia-de-servicios` y `seguridad-owasp` | Es arquitectura de sistemas y aplica a cualquier servicio que mueva dinero o datos |
| Coste de la FFT frente a la factorización densa | `divide-y-venceras` | Razonamiento de complejidad aplicado, útil mucho más allá de la simulación |

### 7.6 Resumen de utilidad

De las 33 secciones que suman los seis PDFs, **sirven para el temario unas nueve**. El resto es
o repetición del mismo bloque, o matemática de nicho, o técnica minorista que los propios textos
refutan. La consecuencia práctica para la escuela es que **no hacen falta seis documentos**: hacen
falta tres extractos (p2 para derivaciones, p4 como índice y para inferencia, p1 para
arquitectura) y un cuarto con la sección de estrategias de p5, guardado como material de la ruta
`quant` y no como contenido `core`. Copiar los seis en el portal produciría 438 páginas con
ejemplos numéricos que se contradicen entre sí.

