# Los seis informes de NotebookLM: qué hay, qué falta y cómo entra en el temario

**Fecha:** 2026-11-02 · **Fuente:** seis PDF en `Descargas`, generados con NotebookLM sobre un
corpus de ~300 vídeos de canales de datos y quant · **Destino:** `contenido/f00…f12/`

---

## 1. Qué son exactamente estos seis ficheros

No son seis temarios: son **seis cortes del mismo corpus**, con el mismo esqueleto y distinto
énfasis. Leídos los seis enteros, el material nuevo que aportan cabe en dos bloques.

| Fichero | Título real | Págs. | Módulos | Aporta | Redundante con |
| --- | --- | --- | --- | --- | --- |
| `p1` | Compendio maestro de ingeniería cuantitativa | 15 | 6 | Visión de conjunto: finanzas, sesgos, procesos, estadística, álgebra, arquitectura | p3, p6 |
| `p2` | Guía maestra: derivación estocástica y multi-greek | 15 | 5 | Backtesting, **portafolio de proyectos**, procesos, **griegas**, filosofía | p5 |
| `p3` | Manual maestro: procesos estocásticos | 14 | 5 | Versión corta de p2 con más peso en ABM/GBM y KL | p2 |
| `p4` | **Guía estructural y temario: mapeo a fuentes de vídeo** | 22 | 6 | **El más útil**: 17 secciones con el mapeo concepto→vídeo | — |
| `p5` | Tratado completo: simulación, álgebra, trading algorítmico | 25 | 6 | **Aceptación-rechazo**, Euler-Maruyama, griegas, indicadores, genética | p2 |
| `p6` | Guía maestra de finanzas cuantitativas | 17 | 5 | Cálculo de Itô, Bachelier, griegas, mitos | p4, p5 |

**La fuente canónica por bloque:** inferencia → `p4` §1; procesos estocásticos → `p5` §1 y `p6`
§3; valoración y griegas → `p5` §3; Markov → `p4` §3.2; backtesting → `p6` §1 y `p5` §5;
portafolio y carrera → `p2` §2 y `p4` §6.1. El resto se puede ignorar sin perder nada.

**Aviso de calidad, porque condiciona todo lo demás.** Los informes están generados a partir de
transcripciones de vídeo y se nota: LaTeX roto dentro del texto (`$dS_t = \mu$`, `$EV$`), tablas
convertidas en párrafos con barras verticales, y cifras de ejemplo sin fuente (rentabilidades de
2021-2022, «Sharpe entre 1,5 y 3,0»). **Ninguna cifra de estos PDFs entra en una página sin una
fuente citable detrás.** Lo que sí entra es la estructura conceptual, que es buena.

---

## 2. Los seis bloques temáticos reales

| Bloque | Qué dice el corpus | Dónde vive hoy | Destino |
| --- | --- | --- | --- |
| B1 · Inferencia aplicada | LLN frente a CLT, intervalos de confianza, media acumulada frente a ventana, no estacionariedad del rendimiento | F02 y F05, bien cubiertos | **Enriquecer 4 páginas** + 1 página nueva |
| B2 · Procesos estocásticos | ABM frente a GBM, EDE, Euler-Maruyama, lema de Itô, Karhunen-Loève, puente browniano | **No existe nada** | **4 páginas nuevas** |
| B3 · Valoración y griegas | Bachelier, Black-Scholes, delta-gamma-vega, cobertura con álgebra lineal, *volatility drag* | Solo existe `curva-de-tipos-y-descuento` | **3 páginas nuevas** + 1 enriquecimiento |
| B4 · Markov y crédito | Matriz de transición, Chapman-Kolmogorov, estados absorbentes, MLE, migración de crédito | **No existe** | **1 página nueva** |
| B5 · Backtesting y edge | Los tres sesgos, EG, decaimiento del edge, criterio de retiro, modelo casino | F09 lo cubre mejor que los PDFs | **Enriquecer 3 páginas** |
| B6 · Portafolio, operación y carrera | Los 5 proyectos que «te hacen quant», riesgo operativo de cola, crítica a la EMH, honestidad temporal del dato | Parcial (`alpha-y-beta`, `incidentes-y-postmortem`, `sesgo-de-supervivencia`) | **Enriquecer 2**, **1 página nueva** (point-in-time) y alimentar `02-PROYECTOS.md` |
| B7 · Trading algorítmico e indicadores | VWAP intradía, pin bar, EMA, RSI, HMA, robustez Monte Carlo, programación genética | `algoritmos-de-ejecucion` y `generacion-de-senales`, sin página de indicadores | **1 página nueva** + 2 enriquecimientos |

Conclusión operativa: **el corpus no mejora lo que ya hay de data engineering** (F03, F04, F11
están por delante). Su valor real es abrir la mitad matemática de la ruta quant, que hoy empieza
en «qué es un mercado» y salta a métricas de riesgo sin pasar por cómo se mueve un precio.

---

## 3. Mapa concepto → página existente o hueco

Ids copiados literalmente del temario. «Existe» significa que la página cubre el concepto de
verdad; «incompleto» significa que lo toca de refilón.

| Concepto del corpus | Estado | Id o propuesta |
| --- | --- | --- |
| Ley de los grandes números y TCL aplicados a un edge | Existe | `ley-de-los-grandes-numeros`, `teorema-central-del-limite` |
| Interpretación frecuentista del intervalo de confianza | Existe | `intervalos-de-confianza` |
| Media acumulada frente a ventana móvil | Incompleto | `estacionariedad` + página nueva `medir-tu-progreso` |
| Ventanas de varianza y cambio de régimen en el rendimiento | Existe | `regimenes-de-mercado`, `hmm-regimenes` |
| Movimiento browniano aritmético y geométrico | **Hueco** | `movimiento-browniano` |
| EDE y esquema de Euler-Maruyama | **Hueco** | `ecuaciones-diferenciales-estocasticas` |
| Lema de Itô y término de segundo orden | **Hueco** | `lema-de-ito` |
| Expansión de Karhunen-Loève del puente browniano | **Hueco** | `expansion-karhunen-loeve` |
| Modelo de Bachelier | **Hueco** | `valoracion-de-opciones` |
| Black-Scholes y paridad put-call | **Hueco** | `valoracion-de-opciones` |
| Griegas delta, gamma, vega, theta, rho | **Hueco** | `griegas-y-cobertura` |
| Cobertura multi-greek como sistema lineal | **Hueco** | `griegas-y-cobertura` |
| *Volatility drag* y rentabilidad geométrica | **Hueco** | `volatility-drag` |
| Cadenas de Markov con estados absorbentes | **Hueco** | `cadenas-de-markov` |
| Estimación MLE de una matriz de transición | Incompleto | `maxima-verosimilitud` + `cadenas-de-markov` |
| PCA sobre retornos y multicolinealidad | Existe | `pca` |
| Aceptación-rechazo para generar distribuciones | Incompleto | `simulacion-de-monte-carlo`, `aleatoriedad-y-muestreo` |
| Look-ahead, data snooping y supervivencia | Existe | `sesgo-de-mirar-al-futuro`, `data-snooping-y-multiple-testing`, `sesgo-de-supervivencia` |
| Sharpe deflactado por número de pruebas | Existe | `sharpe-deflactado` |
| Edge por operación y criterio de retiro | Incompleto | `alpha-decay` + `generacion-de-senales` |
| El día trading como casino | Incompleto | `psicologia-del-trading`, `paper-trading` |
| Indicadores: VWAP, EMA, RSI, HMA, pin bar | **Hueco** | `indicadores-tecnicos` |
| Programación genética de indicadores | **Hueco** | solo mención, no merece página propia |
| Beta pasiva frente a cartera cubierta | Incompleto | `alpha-y-beta`, `volatility-drag` |
| Crítica a la EMH y naturaleza del alpha | Incompleto | `alpha-y-beta`, `factores-y-fama-french` |
| Riesgo operativo de cola e infraestructura | Existe | `incidentes-y-postmortem`, `copias-de-seguridad-y-recuperacion` |
| Fecha de disponibilidad frente a fecha del hecho (point-in-time) | **Hueco** | `correccion-point-in-time` |
| Universo de inversión histórico: altas, bajas y cambios de ticker | Incompleto | `sesgo-de-supervivencia` (enriquecer) |
| Los cinco proyectos de portfolio quant | — | va a `02-PROYECTOS.md` (PF-06) |

**Resultado:** 11 páginas nuevas, 13 enriquecimientos y 1 concepto descartado.

---

## 4. Fichas de las once páginas nuevas

> **Estado a 2026-11-02.** Las once fichas de este apartado están escritas y validadas en el
> portal. Cada una se puede abrir en `#/c/<id>`. Lo que queda por escribir ya no sale de estos
> informes: son los huecos del temario que recoge [`06-COBERTURA.md`](06-COBERTURA.md).

Cada ficha trae el frontmatter listo para pegar, el guion de las siete secciones, un ejemplo
numérico ya calculado, el quiz y los errores típicos. El código es un esbozo: al escribirlo,
respeta la regla de que `verificable` se ejecuta sin red en menos de 15 s y que los `print`
sueltan solo ASCII.

### N1 · `movimiento-browniano`

```markdown
id: movimiento-browniano
titulo: Movimiento browniano
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [variable-aleatoria, distribuciones-continuas, ley-de-los-grandes-numeros]
tags: [procesos, estocastico, precios]
resumen: El paseo aleatorio en tiempo continuo que sostiene casi todo modelo de precio, y por qué su varianza crece con el tiempo.
fuentes: ["Bachelier (1900), 'Théorie de la spéculation'", "Karatzas y Shreve (1991), 'Brownian Motion and Stochastic Calculus'"]
```

- **En una frase:** un proceso cuyo valor cambia por sumas de shocks independientes, de forma que
  su desviación típica crece con la raíz del tiempo y su camino no tiene derivada en ningún punto.
- **La idea:** el grano de polen en el agua. Cada empujón es independiente y del mismo tamaño
  típico; sumar muchos no estabiliza el valor, estabiliza la *forma* de la distribución. De ahí
  que la incertidumbre a un año sea √252 veces la de un día, y no 252 veces.
- **Definición formal:** W con W₀=0, incrementos independientes y estacionarios
  W_t − W_s ~ N(0, t−s), caminos continuos. ABM: dS = μ dt + σ dW. GBM: dS = μ S dt + σ S dW, con
  solución S_t = S₀ · exp((μ − σ²/2)t + σW_t). Cada símbolo, definido: μ deriva anual, σ
  volatilidad anual, W movimiento browniano estándar.
- **Ejemplo:** S₀ = 100, μ = 0, σ = 0,20, un año, y un camino con W₁ = 0,5. En ABM:
  100 + 0,20 · 0,5 = 110. En GBM: 100 · exp(−0,02 + 0,10) = 108,33. La diferencia de 1,67 no es
  ruido: es el término −σ²/2.
- **Código (verificable):** simular 20 000 caminos con `rng = np.random.default_rng(7)`, 252
  pasos, imprimir la media y la desviación de log(S₁/S₀) y compararlas con (μ−σ²/2) y σ.
- **Errores típicos:** usar ABM para precios (permite valores negativos); confundir σ anual con
  diaria (hay que dividir por √252, no por 252); olvidar el −σ²/2 y creer que el retorno
  esperado es μ; suponer que un camino de precio se puede derivar.
- **Quiz:** «¿Por qué la desviación de un browniano a un año es √252 veces la de un día y no
  252?» con opciones que incluyan «porque las varianzas se suman, no las desviaciones».

### N2 · `ecuaciones-diferenciales-estocasticas`

```markdown
id: ecuaciones-diferenciales-estocasticas
titulo: Ecuaciones diferenciales estocásticas
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [movimiento-browniano, derivadas-y-reglas, integrales]
tags: [sde, euler-maruyama, simulacion]
resumen: Cómo se escribe un modelo de precio como deriva más ruido, y cómo se simula sin que el paso temporal mienta.
fuentes: ["Kloeden y Platen (1992), 'Numerical Solution of Stochastic Differential Equations'"]
```

- **En una frase:** una ecuación dX = a(X,t) dt + b(X,t) dW que dice cuánto cambia X por unidad de
  tiempo (deriva) y cuánto por unidad de ruido (difusión).
- **La idea:** dos fuerzas. La deriva empuja siempre en la misma dirección; la difusión empuja
  hacia un lado o el otro con magnitud √Δt. Esa raíz es la que rompe la intuición: al dividir el
  tiempo en trozos, el ruido no se reduce proporcionalmente.
- **Definición formal:** Euler-Maruyama: X_{k+1} = X_k + a(X_k,t_k)Δt + b(X_k,t_k)√Δt · Z, con
  Z ~ N(0,1). Error fuerte (trayectoria) de orden ½; error débil (esperanza) de orden 1.
- **Ejemplo:** GBM con μ = 0,05, σ = 0,25, S₀ = 100, 4 pasos de 0,25 años y Z = (0,3; −1,1; 0,2;
  0,8). Primer paso: 100 + 0,05·100·0,25 + 0,25·100·0,5·0,3 = 100 + 1,25 + 3,75 = 105,0.
- **Código (verificable):** Euler-Maruyama con 1 000 pasos frente a la solución exacta, imprimir
  el error absoluto medio y comprobar que baja al dividir Δt por 4.
- **Errores típicos:** usar Δt en el término estocástico; elegir pasos tan grandes que la
  trayectoria se vuelva negativa; confundir deriva con retorno esperado; olvidar que el error
  fuerte y el débil se miden distinto.
- **Quiz:** «Si reduces Δt a la cuarta parte, ¿qué le pasa al término de ruido de cada paso?»
  (se multiplica por ½, no por ¼).

### N3 · `lema-de-ito`

```markdown
id: lema-de-ito
titulo: Lema de Itô
fase: 9
nivel: experto
rutas: [quant]
prerequisitos: [ecuaciones-diferenciales-estocasticas, regla-de-la-cadena, retornos-logaritmicos]
tags: [ito, calculo, derivacion]
resumen: La regla de la cadena del cálculo estocástico: aparece un término de segundo orden que cambia el resultado y explica el −σ²/2.
fuentes: ["Itô (1951), 'On stochastic differential equations'", "Hull (2018), 'Options, Futures and Other Derivatives'"]
```

- **En una frase:** si X sigue una EDE y f es una función suave, f(X) sigue otra EDE con un
  término extra ½b²f'' que en el cálculo normal no existe.
- **La idea:** en el cálculo de siempre, (dW)² se desprecia porque es de orden(dt)². Con un
  browniano, (dW)² es de orden dt: no se puede despreciar y aparece la curvatura de f.
- **Definición formal:** df = (f_t + a f_x + ½ b² f_xx) dt + b f_x dW. Aplicado a f = ln S con
  GBM: d ln S = (μ − σ²/2) dt + σ dW.
- **Ejemplo:** μ = 0,08, σ = 0,30. La media del logaritmo crece a 0,08 − 0,045 = 0,035 al año,
  no a 0,08: en 10 años la diferencia es 0,45 de log-rentabilidad, un 56 % del 0,80 que se
  esperaría ignorando el término de segundo orden.
- **Código (verificable):** simular 50 000 GBM a un año, imprimir la media de log(S₁/S₀) y
  compararla con (μ − σ²/2); el error debe quedar por debajo de 0,01.
- **Errores típicos:** aplicar la regla de la cadena sin el término ½σ²; usar retornos simples
  donde el lema pide logarítmicos; derivar f como si W fuera derivable; confundir el signo.
- **Quiz:** «¿De dónde sale el −σ²/2?» con opciones que incluyan «de la curvatura del logaritmo
  multiplicada por la varianza del ruido».

### N4 · `valoracion-de-opciones`

```markdown
id: valoracion-de-opciones
titulo: Valoración de opciones
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [movimiento-browniano, valor-esperado, curva-de-tipos-y-descuento]
tags: [opciones, black-scholes, derivados]
resumen: Por qué una opción tiene un precio único aunque nadie sepa a dónde va el activo: replicación, medida neutral al riesgo y la fórmula de Black-Scholes.
fuentes: ["Black y Scholes (1973), 'The Pricing of Options and Corporate Liabilities'", "Bachelier (1900), 'Théorie de la spéculation'"]
```

- **En una frase:** el precio de una opción no sale de predecir el activo, sino de construir una
  cartera que la copie y obligar a que las dos cuesten lo mismo.
- **La idea:** si puedo fabricar el pago de la opción comprando y vendiendo el subyacente, su
  precio queda clavado por el coste de esa réplica. La deriva del activo desaparece de la fórmula:
  solo quedan volatilidad, plazo, tipos y strike.
- **Definición formal:** C = S₀Φ(d₁) − K e^{−rT}Φ(d₂), con
  d₁ = (ln(S₀/K) + (r + σ²/2)T) / (σ√T) y d₂ = d₁ − σ√T. Paridad: C − P = S₀ − K e^{−rT}.
  Bachelier sustituye el GBM por un browniano aritmético y da una normal en vez de una lognormal.
- **Ejemplo:** S₀ = 100, K = 100, r = 3 %, σ = 25 %, T = 1. d₁ = 0,245, d₂ = −0,005;
  C = 100·0,5968 − 100·0,9704·0,4980 = 11,35. La put por paridad: 11,35 − 100 + 97,04 = 8,39.
- **Código (verificable):** `scipy.stats.norm.cdf` para calcular C y P, y comprobar la paridad
  con una tolerancia de 0,01.
- **Errores típicos:** meter la rentabilidad esperada del activo en la fórmula; usar volatilidad
  diaria con T en años; olvidar descontar el strike; creer que el precio de la opción es una
  probabilidad de que suba; comparar opciones con distintos vencimientos sin anualizar.
- **Quiz:** «Si sube la volatilidad, ¿qué le pasa a una call y a una put?» (suben las dos, porque
  la opción es un derecho, no una obligación).

### N5 · `griegas-y-cobertura`

```markdown
id: griegas-y-cobertura
titulo: Griegas y cobertura
fase: 9
nivel: experto
rutas: [quant]
prerequisitos: [valoracion-de-opciones, optimizacion-con-restricciones, operaciones-matriciales]
tags: [griegas, cobertura, riesgo]
resumen: Las derivadas del precio de una opción y cómo se resuelve la cartera que deja la exposición a cero sin apostar a la dirección.
fuentes: ["Hull (2018), 'Options, Futures and Other Derivatives', cap. 19", "Taleb (1997), 'Dynamic Hedging'"]
```

- **En una frase:** delta, gamma, vega, theta y rho miden cuánto cambia el precio de la opción
  cuando cambia una cosa; cubrir es elegir posiciones que sumen cero en esas derivadas.
- **La idea:** una cartera puede ser insensible al precio y seguir expuesta a que el precio se
  mueva mucho (gamma) o a que la volatilidad cambie (vega). Cubrir todo a la vez es resolver un
  sistema de ecuaciones, no comprar «un poco de todo».
- **Definición formal:** Δ = ∂C/∂S, Γ = ∂²C/∂S², ν = ∂C/∂σ, Θ = ∂C/∂t, ρ = ∂C/∂r. Cobertura de
  dos instrumentos: G · w = −exposición, con G la matriz de griegas por contrato y w los pesos.
  Después se ajusta la delta con el subyacente: w_S = −(Δ_cartera + Σ w_i Δ_i).
- **Ejemplo:** exposición objetivo Γ = 60, ν = 100. Call A: Γ = 2, ν = 10. Call B: Γ = 5, ν = 18.
  Determinante 2·18 − 5·10 = −14. Pesos: w_A = (18·60 − 5·100)/(−14) = −41,4 y
  w_B = (−10·60 + 2·100)/(−14) = 28,6. El signo negativo no es un error: hay que vender A.
- **Código (verificable):** `np.linalg.solve` con la matriz 2×2 y el vector, imprimir los pesos y
  la delta residual.
- **Errores típicos:** cubrir una vez y no rebalancear; ignorar la gamma cruzada entre
  instrumentos; rebalancear cada minuto y comerse la cobertura en comisiones; creer que
  delta-neutral es «sin riesgo»; confundir vega por contrato con vega por acción.
- **Quiz:** «Si el determinante de la matriz de griegas es cero, ¿qué significa?» (los dos
  instrumentos cubren exactamente lo mismo; no se puede resolver el sistema).

### N6 · `volatility-drag`

```markdown
id: volatility-drag
titulo: Volatility drag
fase: 9
nivel: intermedio
rutas: [quant, core]
prerequisitos: [retornos-logaritmicos, varianza-y-desviacion, ratio-de-sharpe]
tags: [volatilidad, rentabilidad, apalancamiento]
resumen: Por qué dos carteras con la misma media pueden acabar en sitios distintos, y cómo la volatilidad se come el interés compuesto.
fuentes: ["Hull (2018), 'Options, Futures and Other Derivatives'", "Thorp (2017), 'A Man for All Markets'"]
```

- **En una frase:** la rentabilidad que de verdad acumulas es aproximadamente la media menos la
  mitad de la varianza; subir la volatilidad sin subir la media te empobrece.
- **La idea:** una caída del 50 % exige una subida del 100 % para volver. Cuanto más grandes son
  los saltos, más caro sale recuperarse, aunque la media aritmética no cambie.
- **Definición formal:** R_g ≈ R_a − σ²/2 (por periodo, con retornos logarítmicos). En forma
  exacta: el crecimiento por periodo es la media de ln(1 + r).
- **Ejemplo:** un activo que hace +10 % y −10 % alternos tiene media aritmética 0 y, tras dos
  periodos, 1,10 · 0,90 = 0,99: un −1 %. Con ±20 %: 1,20 · 0,80 = 0,96, un −4 %.
- **Código (verificable):** generar 1 000 retornos normales con σ = 0,2, imprimir media
  aritmética, media de log(1+r) y el producto acumulado; la diferencia debe ser ≈ σ²/2.
- **Errores típicos:** comparar dos carteras por su media aritmética con volatilidades distintas;
  mantener apalancamiento constante en un activo volátil; olvidar el coste de financiar el
  apalancamiento; extrapolar el interés compuesto a partir del retorno medio.
- **Quiz:** «¿Qué cartera crece más: una con 8 % de media y 10 % de volatilidad, o una con 9 % y
  30 %?» (la primera: 0,08 − 0,005 = 0,075 frente a 0,09 − 0,045 = 0,045).

### N7 · `indicadores-tecnicos`

```markdown
id: indicadores-tecnicos
titulo: Indicadores técnicos
fase: 9
nivel: básico
rutas: [quant]
prerequisitos: [tick-data-y-ohlcv, retornos-logaritmicos]
tags: [indicadores, rsi, medias]
resumen: Qué calcula de verdad cada indicador clásico, para qué sirve y por qué optimizar sus parámetros es la forma más rápida de engañarte.
fuentes: ["Wilder (1978), 'New Concepts in Technical Trading Systems'", "Murphy (1999), 'Technical Analysis of the Financial Markets'"]
```

- **En una frase:** un indicador es una transformación de la serie de precios; no añade
  información que no estuviera ahí, solo la hace visible de otra forma.
- **La idea:** una media móvil suaviza; un RSI compara la magnitud de las subidas con la de las
  bajadas; un ATR mide cuánto se mueve el precio. Ninguno sabe nada del futuro, y todos comparten
  parámetros que se pueden ajustar hasta que el pasado queda perfecto.
- **Definición formal:** SMA_n = (1/n)·Σ P_{t−i}; EMA con α = 2/(n+1); RSI = 100 − 100/(1+RS),
  con RS = media de subidas / media de bajadas en n periodos; ATR = media del máximo entre
  (alto−bajo), (alto−cierre previo) y (cierre previo−bajo).
- **Ejemplo:** cierres 10, 11, 10, 12 con n = 3: SMA = (11+10+12)/3 = 11; subidas medias =
  (1+2)/3 = 1 y bajadas medias = 1/3, RS = 3, RSI = 75.
- **Código (verificable):** pandas con una serie de 8 cierres escritos a mano, `rolling(3).mean()`
  y una función RSI de 10 líneas, imprimir ambos.
- **Errores típicos:** optimizar el periodo sobre todo el histórico y llamarlo validación; usar el
  RSI como señal de compra sin definir el horizonte; olvidar que los indicadores usan precios ya
  conocidos (no hay magia); encadenar cinco indicadores y creer que se confirman entre sí.
- **Quiz:** «¿Qué información añade un RSI a la serie de cierres?» (ninguna nueva; reformula la
  serie para que la comparación de subidas y bajadas sea legible).

### N8 · `cadenas-de-markov`

```markdown
id: cadenas-de-markov
titulo: Cadenas de Markov
fase: 1
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [probabilidad-condicional, operaciones-matriciales]
tags: [markov, transiciones, credito]
resumen: Un sistema que salta entre estados sin memoria, y cómo su matriz de transición permite calcular a dónde irá y cuánto tardará en quedarse atrapado.
fuentes: ["Norris (1997), 'Markov Chains'", "Jarrow, Lando y Turnbull (1997), 'A Markov Model for the Term Structure of Credit Risk Spreads'"]
```

- **En una frase:** un proceso que en cada paso cambia de estado con probabilidades que solo
  dependen del estado actual, no de cómo llegó hasta él.
- **La idea:** un préstamo que pasa de «al día» a «30 días», a «60», a «90+» o a «impagado». La
  matriz de transición dice qué fracción de cada estado acaba en cada otro; elevarla al cuadrado
  da dos pasos, y al infinito dice dónde se queda todo el mundo.
- **Definición formal:** P con p_ij ≥ 0 y Σ_j p_ij = 1. Chapman-Kolmogorov: P^(n) = P^n.
  Estimación MLE: p̂_ij = n_ij / Σ_k n_ik. Un estado absorbente tiene p_ii = 1; el tiempo
  esperado hasta absorberlo sale de resolver (I − Q)⁻¹.
- **Ejemplo:** P = [[0,9; 0,1], [0; 1]]. Tras dos pasos la probabilidad de seguir en el primer
  estado es 0,81; el tiempo esperado hasta absorción es 1/(1−0,9) = 10 pasos.
- **Código (verificable):** `np.linalg.matrix_power(P, 12)` e inversa de (I − Q) con una matriz
  2×2, imprimir ambas.
- **Errores típicos:** estimar la matriz con cuatro transiciones y sacar conclusiones; olvidar que
  un estado absorbente no se abandona; suponer que las probabilidades no cambian con el tiempo
  (homogeneidad) sin comprobarlo; confundir la probabilidad de impago a un año con la de cinco.
- **Quiz:** «¿Qué significa que una fila de la matriz sume 1?» (que desde ese estado siempre se va
  a algún sitio; si no suma 1, falta un estado).

### N9 · `expansion-karhunen-loeve`

```markdown
id: expansion-karhunen-loeve
titulo: Expansión de Karhunen-Loève
fase: 1
nivel: experto
rutas: [quant, ds]
prerequisitos: [autovalores-y-autovectores, covarianza-y-correlacion]
tags: [kl, autovalores, procesos]
resumen: La versión continua del PCA: descomponer un proceso aleatorio en funciones propias de su covarianza, y simularlo con pocos términos.
fuentes: ["Karhunen (1947), 'Über lineare Methoden in der Wahrscheinlichkeitsrechnung'", "Loève (1948), 'Fonctions aléatoires du second ordre'"]
```

- **En una frase:** cualquier proceso gaussiano centrado se puede escribir como una suma de
  funciones fijas multiplicadas por números aleatorios independientes, ordenadas por cuánta
  varianza aporta cada una.
- **La idea:** es un PCA, pero con infinitas columnas. El «peso» de cada dirección es una función
  del tiempo, no un vector; y la dirección se obtiene resolviendo una ecuación integral con el
  núcleo de covarianza. Para el puente browniano las funciones son senos y los pesos decaen como
  1/k².
- **Definición formal:** para el puente browniano en [0,1], con kernel K(s,t) = min(s,t) − st:
  λ_k = 1/(k²π²) y e_k(t) = √2 · sin(kπt), k = 1, 2, 3…
  Entonces B_t = Σ_k √λ_k · Z_k · e_k(t), con Z_k ~ N(0,1) independientes.
- **Ejemplo:** la varianza total del puente es ∫K(t,t)dt = ∫(t − t²)dt = 1/6 ≈ 0,1667. Los tres
  primeros autovalores suman (1 + 1/4 + 1/9)/π² = 0,1379, es decir el **82,7 %** de la varianza;
  con diez términos se llega al 94,2 %. Esa es la cuenta que justifica truncar la serie.
- **Código (verificable):** reconstruir 5 caminos con 3 y con 20 términos, imprimir la varianza
  media y compararla con 1/6.
- **Errores típicos:** confundirla con la serie de Fourier (aquí los coeficientes son aleatorios);
  usar demasiado pocos términos y concluir que el proceso es suave; olvidar normalizar las
  autofunciones; aplicarla a un proceso no gaussiano y creer que la truncación conserva la ley.
- **Quiz:** «¿Por qué los pesos decaen tan rápido en el puente browniano?» (porque su covarianza
  es muy suave; cuanto más suave el proceso, menos términos hacen falta).

### N10 · `medir-tu-progreso`

```markdown
id: medir-tu-progreso
titulo: Medir tu progreso sin engañarte
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar]
tags: [progreso, metricas, ventanas]
resumen: La media acumulada esconde los cambios: mide tu rendimiento por ventanas, compáralo contigo mismo y no conviertas la métrica en el objetivo.
fuentes: ["Heath y Starr (1999), 'Adaptive Spaced Repetition'", "Dweck (2006), 'Mindset'"]
```

- **En una frase:** si mides tu progreso con el total acumulado, nunca verás que has empeorado
  esta semana; con una ventana móvil, sí.
- **La idea:** la media de todo lo que has hecho arrastra el pasado y pesa igual una sesión de
  hace seis meses que la de ayer. El rendimiento, como una serie temporal, no es estacionario:
  cambia de régimen. Medirlo bien es mirar la ventana reciente y compararla con tu propia línea
  base, sabiendo que la métrica se puede convertir en el objetivo y estropearse.
- **Definición formal:** media acumulada x̄_t = (1/t)Σx_i; media por ventana
  m_t^(w) = (1/w)Σ_{i=t−w+1..t} x_i. La segunda reacciona; la primera no.
- **Ejemplo:** aciertos de 10 sesiones: 5, 6, 4, 5, 6, 4, 5, 3, 4, 3. La acumulada termina en 4,5
  y sugiere estabilidad; la ventana de 3 termina en 3,33, y la de 5 en 3,8: estás bajando.
- **Código (verificable):** pandas con `expanding().mean()` y `rolling(3).mean()` sobre la serie,
  imprimir las últimas tres filas de cada una.
- **Errores típicos:** medir minutos de estudio en vez de recuperación; comparar tu semana con la
  de otra persona; cambiar de métrica cuando baja; usar la racha como prueba de dominio.
- **Quiz:** «¿Qué ventaja tiene la ventana móvil sobre la media acumulada?» (detecta el cambio de
  tendencia; la acumulada lo diluye).

---

### N11 · `correccion-point-in-time`

```markdown
id: correccion-point-in-time
titulo: Corrección point-in-time
fase: 4
nivel: avanzado
rutas: [de, quant]
prerequisitos: [sesgo-de-mirar-al-futuro, scd-dimensiones-cambiantes, datos-de-mercado-y-acciones-corporativas]
tags: [point-in-time, linaje, backtest]
resumen: Guardar cada dato con la fecha en que estuvo disponible y no con la del evento: la disciplina que separa un pipeline honesto de un backtest inflado.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 4", "Hull (2018), 'Options, Futures and Other Derivatives'"]
```

- **En una frase:** cada fila lleva dos fechas, cuándo ocurrió y cuándo se supo; toda consulta
  histórica filtra por la segunda.
- **La idea:** un resultado trimestral se publica semanas después del cierre, y a veces se
  revisa. Si el pipeline guarda solo la fecha de cierre, cualquiera que consulte «qué se sabía
  el 15 de mayo» recibirá información que aún no existía. Es el mismo error que el sesgo de
  mirar al futuro, pero a nivel de almacén: no está en el modelo, está en la tabla.
- **Definición formal:** para cada entidad, `valid_from` y `as_of` (o `published_at`), con
  `as_of ≥ valid_from`. La vista histórica es la que filtra `as_of ≤ t`; la corrección retrasada
  entra como fila nueva que cierra la anterior, nunca como `UPDATE` destructivo.
- **Ejemplo:** ingresos de 2025-Q1 cerrados el 31-03 y publicados el 24-04; revisión al alza del
  3 % el 12-06. Una consulta a 15-05 debe devolver la cifra original; a 15-07, la revisada. Con
  una sola fecha, las dos consultas devuelven lo mismo y la primera es mentira.
- **Código (verificable):** dos tablas de tres filas con `as_of`, una consulta que devuelve el
  valor vigente en dos fechas distintas y un `print` con los dos resultados.
- **Errores típicos:** guardar solo la fecha del evento; corregir con `UPDATE` y perder el
  histórico; filtrar por `valid_from` creyendo que es lo mismo; olvidar las revisiones de datos
  macroeconómicos (el PIB se revisa tres veces); no probar el filtro con una fecha entre el
  cierre y la publicación.
- **Quiz:** «¿Qué dos fechas necesita una fila para ser honesta?» (la del hecho y la de su
  disponibilidad).

**Si una ficha crece demasiado, se parte.** El reparto natural, cuando llegue el momento, es:
`proceso-de-wiener` (el ladrillo), `movimiento-browniano-aritmetico` (por qué el aditivo tiene
hueco en tipos), `simulacion-euler-maruyama` (el esquema numérico), `puente-browniano` (la
condición de extremos), `modelo-de-black-scholes` (la fórmula) y `cobertura-delta-gamma-vega`
(el sistema). No lo hagas antes de tener la página compuesta escrita: partir un texto que no
existe solo multiplica los huecos.

---

## 5. Trece enriquecimientos de páginas que ya existen

No merecen página nueva: merecen un párrafo o un ejemplo mejor. El orden es el de impacto.

| Página | Qué añadir | De dónde sale |
| --- | --- | --- |
| `intervalos-de-confianza` | La confusión entre intervalo frecuentista y posterior, con el ejemplo de «el 95 % de qué» | p4 §1.3 |
| `ley-de-los-grandes-numeros` | Por qué un edge positivo no produce retornos estables en 20 operaciones | p4 §1.1 |
| `estacionariedad` | Media acumulada frente a ventana móvil, con una serie que cambia de régimen | p4 §1.2 |
| `simulacion-de-monte-carlo` | Aceptación-rechazo para generar de una distribución arbitraria; robustez de una estrategia | p5 §1.2, §4.4 |
| `alpha-decay` | Fórmula del edge por operación y criterio cuantitativo de retirada | p4 §5.2 |
| `sharpe-deflactado` | El umbral de sospecha: Sharpe entre 1,5 y 3,0 en un backtest bonito es una alarma, no un logro | p2 §1.1 |
| `pca` | PCA sobre retornos y el problema de multicolinealidad en los pesos de cartera | p4 §3.1 |
| `sesgo-de-supervivencia` | Los tres sesgos juntos, con la lista de comprobación antes de creerse un backtest | p5 §5.2 |
| `incidentes-y-postmortem` | Riesgo operativo de cola: el caso del servidor borrado y qué se hace antes de que pase | p4 §6.2 |
| `copias-de-seguridad-y-recuperacion` | La ley de los grandes números aplicada a la atención: crecer aumenta la cola de actores maliciosos | p4 §6.2 |
| `slippage-y-comisiones` | El caso VWAP del propio corpus: +713 % sin comisión y −97 % con 0,1 % en 6 072 operaciones; el coste por operación como variable dominante | p5 §4.2 |
| `psicologia-del-trading` | El modelo casino frente al jugador: por qué el día trading se parece más a la ruina que a un oficio | p5 §6.3 |
| `alpha-y-beta` | La crítica a la EMH y la definición de alpha ortogonal a los factores | p4 §6.3 |

Cada enriquecimiento sigue la misma regla: **no se pega el párrafo del PDF**. Se lee, se busca la
fuente citable, y se reescribe en el tono del portal con un ejemplo numérico propio.

---

## 6. Erratas dentro de los propios informes (por qué no se copia ni un número)

Esto no es lo que los informes denuncian: es lo que hacen mal. Importa porque una página escrita
copiando sus cifras heredaría el error y lo convertiría en doctrina del portal.

| Errata | Comprobación | Consecuencia |
| --- | --- | --- |
| `p2` calcula mal el interés compuesto: escribe 1,288 × 0,800 − 1 = +1,88 % y 1,143 × 0,980 − 1 = +6,00 % | Recalculado: +3,04 % y +12,01 % | `p5` corrige los dos números sin citar a `p2`: dos documentos del mismo corpus se contradicen |
| El «caso del balón» aparece con cuatro juegos de datos distintos (media 0,38 / 0,375 / 0,40; Z de −9,0 / −8,185 / −7,07) | Las cuatro versiones dicen demostrar lo mismo | Ningún ejemplo es reproducible; sirve la idea, no las cifras |
| La cobertura multi-greek llega **siempre** a los mismos pesos (8641 y −8006) con matrices de griegas distintas | Verificado por búsqueda: `p1`, `p3`, `p4` y `p6` repiten el par; `p5` da 864,1 y −800,6 con el mismo delta residual | Los pesos están copiados de una fuente, no calculados: el ejemplo no enseña el método |
| Umbral de Sharpe «sospechoso»: 1,5–3,0 en `p1`/`p2`, pero 1,5–1,7 en `p6` | 1,7 es un Sharpe normal | No se puede usar como regla sin decidir antes el criterio |
| Truncamiento espectral de Karhunen-Loève: K entre 20 y 50, K = 50 o 500, K = 100 o 500 «con 99,99 %» | Tres respuestas incompatibles | La página tiene que deducir el truncamiento con la varianza, no citar un número |
| Varianza explicada por PC1 en estrés: «por debajo del 50 %», «más del 75 %», «más del 80 %», «75–80 %» | Cuatro cifras para el mismo fenómeno | Igual que arriba: el método sí, la cifra no |
| Un concepto con tres grafías: Paolucci, Palooian, Palucci, y `p1` ni lo nombra | No aparece en literatura citable | Fuera del temario |
| El «Gaussian Cookbook» se describe como recetario en `p1` y como plataforma interactiva en `p4`, sin URL | No verificable | Se menciona como recurso, nunca como fuente |

Conclusión práctica, que ya está aplicada en las fichas de §4: **de estos informes se hereda la
estructura y el método; todos los ejemplos numéricos se recalculan**, y cuando una cifra no se
puede reconstruir, no entra.

---

## 7. Lo que NO entra (y por qué)

| Material | Decisión | Motivo |
| --- | --- | --- |
| Rentabilidades de 2021-2022 de dos carteras | Fuera | Cifras sin fuente, sin costes y sin fanqueo; no reproducibles |
| «qfin» como librería en PyPI | Fuera como hecho | No he podido verificar que exista; si existe, es un proyecto personal de un tercero |
| «Desigualdad de Palucci» | Fuera | Término no reconocible en la literatura; no se puede citar |
| Afirmaciones sobre manipulación del mercado | Fuera | Sin evidencia y sin utilidad para aprender |
| Programación genética de indicadores | Solo mención | Interesante, pero es un curso entero y no una página |
| Estrategias concretas (VWAP intradía, pin bar, HMA/RSI) | Solo como ejemplo, y con sus propios números delante | No hace falta desmontarlas: el corpus las desmonta. El pin bar puro da −2 % en 6 años de oro con un −43 % de caída máxima y un 38 % de acierto; la estrategia VWAP pasa de +713 % a −97 % al meter un 0,1 % de comisión |

Y una advertencia de encaje: **esto es quant, no data engineering.** Si tu prioridad es el puesto
de data engineer, este bloque es opcional y va después de F04 y F11. Si lo haces antes, aprenderás
matemáticas que no vas a usar en el trabajo y dejarás sin construir lo que sí te van a pedir.

---

## 8. Procedimiento exacto para dar de alta un concepto

1. **Comprobar que el id no existe:** busca el id en `CONTENIDO-TEMARIO.md`; si aparece, no es un
   alta, es un enriquecimiento.
2. **Escribir la página** en `contenido/fNN/<id>.md` con el contrato de
   `COMO-ESCRIBIR-CONTENIDO.md`: frontmatter de 8 campos, siete secciones en orden y, si hay
   código, etiqueta `verificable` o `ilustrativo`.
3. **Añadir la fila al temario** en la tabla de su fase, con id, título, nivel y una línea. Si la
   fase dice «Conceptos: N», actualiza N y el total de la cabecera.
4. **Resolver los prerrequisitos:** cada id de `prerequisitos` tiene que existir y leerse antes.
   Un ciclo rompe la ordenación de los itinerarios.
5. **Comprobar enlaces:** todos los `[[id]]` del cuerpo existen.
6. **Ejecutar las puertas:**
   ```sh
   node generar.mjs --validar
   node _comprobar-temario.mjs
   node _comprobar-prerequisitos.mjs
   node _comprobar-solapes.mjs
   ```
7. **Regenerar lo derivado:** `node _generar-itinerarios.mjs` y `node _detectar-dependencias.mjs`
   si la página usa una librería nueva.
8. **Anotar en `05-TRAZABILIDAD.md`** que el hueco está cerrado y con qué fuente.

**Trampa conocida:** el validador ejecuta cada bloque `verificable` y compara los comentarios
`# -> valor` con lo que se imprime. Un ejemplo con `scipy.stats` que tarde 6 s multiplicado por
once páginas hace insufrible la puerta; si el cálculo es solo ilustrativo, va en `ilustrativo`.

## 9. Cómo pedir el próximo informe a NotebookLM (para no repetir este trabajo)

Los seis informes se leen, pero se podrían haber pedido mejor. Si vuelves a generar uno sobre el
corpus de 300 vídeos, pide esto y ahorrarás la mitad del trabajo de curación:

1. **Un informe por módulo, no un compendio.** Un documento de 25 páginas con seis módulos se
   convierte en 40 KB de texto continuo que nadie relee. Seis documentos de 4 páginas se pueden
   asignar a seis páginas del temario.
2. **«No incluyas cifras que no puedas citar del vídeo.»** Todos los números de estos informes
   son inconsistentes entre sí (§6). Sin esta instrucción, el modelo rellena con ejemplos
   plausibles que luego hay que recalcular.
3. **«Para cada concepto: definición, fórmula, un ejemplo numérico resuelto y un error típico.»**
   Es exactamente la estructura de una página del portal, y evita el párrafo motivacional.
4. **«Cita el título del vídeo y el canal de cada concepto.»** Así se puede volver a la fuente
   cuando la fórmula no cuadre, y se puede poner en `fuentes`.
5. **«Dime qué NO cubre el corpus.»** Es la pregunta que descubre los huecos: en este caso, los
   informes no cubren nada del bloque de López de Prado que el temario ya tiene, y no dicen nada
   de ingeniería de datos.
6. **«Marca lo que sea opinión del autor del vídeo, no consenso.»** La crítica a la EMH, el modelo
   casino y las predicciones sobre IA son opinión; el lema de Itô no.

Con esto, el siguiente informe entra casi listo para convertirse en fichas como las de §4.
