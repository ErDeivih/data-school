# Ficha · cartera-acciones — retorno, riesgo y alpha de cinco acciones

**Estado:** ficha de enunciado. No hay implementación de este proyecto en la carpeta: aquí se fija
qué construir, con qué datos del catálogo y cómo se demuestra que está terminado. Las fichas
hermanas son [telemetria-f1](telemetria-f1.md), [f1-clasificacion](f1-clasificacion.md) y
[futbol-partidos](futbol-partidos.md).

## Datos asignados

- **CSV:** [`datasets/csv/cartera-acciones.csv`](../../datasets/csv/cartera-acciones.csv) — **360
  filas** y **3 columnas**; sintético, semilla fija y licencia CC0-1.0. Tamaño y checksum en
  [`datasets/CATALOGO.md`](../../datasets/CATALOGO.md).
- **Catálogo de proyectos:** [`proyectos/CATALOGO.md`](../CATALOGO.md) — cubre los proyectos P14, P15,
  P16 y P22.
- **Ficha del dataset:** [`datasets/FICHAS.md`](../../datasets/FICHAS.md) — procedencia, checksum y
  preguntas que permite responder.
- **Columnas:** `mes` (fecha ISO), `activo` (texto) y `retorno` (decimal, tanto por uno).

## Proyectos del catálogo que cubre

| ID | Título del catálogo | Nivel |
| --- | --- | --- |
| P14 | El riesgo de una cartera, medido | avanzado |
| P15 | ¿Batir al indice o asumir mas riesgo? | avanzado |
| P16 | Un memo de inversion con supuestos y sensibilidad | intermedio |
| P22 | Finanzas desde cero: interés, inflación y riesgo | básico |

## Nivel y rutas

- **P22:** básico, ruta **DS**. Es la puerta de entrada: interés, retorno nominal y real, y una
  primera medida de riesgo.
- **P16:** intermedio, ruta **DS**. Comunicación: convertir los cálculos en un memo con supuestos.
- **P14 y P15:** avanzado, ruta **QT**. Métricas de riesgo y separación de beta y alpha con
  inferencia.
- **Requisitos previos:** álgebra básica, media y desviación típica, regresión lineal simple. Los
  cuatro proyectos comparten la misma tabla; conviene hacerlos en orden P22 → P16 → P14 → P15.

## Tiempo estimado

| Proyecto | Horas |
| --- | --- |
| P22 | 3–4 h |
| P16 | 4–6 h |
| P14 | 6–8 h |
| P15 | 8–10 h |

Total de la ficha: **21–28 h**. P14 y P15 reutilizan la tabla de retornos y las métricas de riesgo.

## Enunciado

El CSV es un panel mensual con sesenta meses de retornos de cinco acciones y un índice. Construye una
base de análisis que convierta ese panel en una serie de riqueza por activo y, sobre ella, cuatro
piezas: la medida del riesgo de cada acción y de una cartera (P14), la separación entre el retorno
que se explica por el mercado y el que no (P15), un memo de inversión de una página con supuestos,
dos escenarios y sensibilidad (P16), y la versión desde cero que explica interés, inflación y riesgo
sin jerga (P22).

La dificultad no está en multiplicar retornos: está en no anualizar mal, en calcular la caída máxima
sobre la riqueza y no sobre la media, en separar beta de alpha sin confundir correlación con
causalidad y en no inventar una tasa libre de riesgo ni una inflación que el CSV no trae. Todo
supuesto que no salga del fichero se declara como supuesto.

## Datos y preparación

- **Formato panel:** 360 filas = 60 meses × 6 activos (`indice`, `accion-a` … `accion-e`). La clave
  natural es `(mes, activo)`; no hay nulos ni claves repetidas, pero se comprueba en el pipeline. Para
  operar hay que **pivotar** a una matriz 60 × 6 y verificar que no quedan huecos.
- **`retorno` está en tanto por uno**, no en porcentaje ni en euros. Un `-0.03` es −3 %. No hay
  columna de precios: la serie de riqueza se construye como producto acumulado de `(1 + retorno)`.
- **Frecuencia mensual:** anualizar un retorno medio mensual no es multiplicar por 12 y ya está; la
  forma correcta es componer, `(1 + r)^12 − 1`, y la volatilidad anual se obtiene multiplicando la
  mensual por `√12`. Hay que declarar qué convención se usa en cada tabla.
- **Caída máxima (drawdown):** se calcula sobre la riqueza acumulada, no sobre la serie de retornos.
  Con datos mensuales, la caída real dentro del mes no se ve: es una cota, no el máximo verdadero.
- **Sharpe:** necesita una tasa libre de riesgo que **no está en el CSV**. Se usa una tasa declarada
  (por ejemplo, 0) y se justifica; sin esa declaración el Sharpe no es una cifra defendible.
- **Beta y alpha:** el índice es el proxy de mercado. Beta = covarianza con el índice / varianza del
  índice; alpha = retorno medio − beta × retorno medio del mercado. Con 60 observaciones y
  correlaciones bajas, los betas salen con error estándar grande: el intervalo importa más que el
  punto.
- **Lo que no hay:** inflación, tipos, dividendos, comisiones, pesos de cartera ni capital inicial. El
  P22 pide hablar de inflación: se hace con una tasa **asumida y declarada**, nunca presentándola como
  dato del CSV. El P16 pide supuestos: son eso, supuestos, y van escritos.

## Pasos

1. **Validar el panel (P14).** Cargar, comprobar 360 filas, 60 meses, 6 activos y la clave
   `(mes, activo)`; pivotar a 60 × 6 y demostrar que no hay celdas vacías ni meses duplicados.
2. **Construir riqueza (P14).** Calcular la serie acumulada por activo con `prod(1 + retorno)`;
   comprobar que el retorno total coincide con riqueza final − 1 y que la suma de retornos mensuales
   **no** es el retorno total.
3. **Medir riesgo (P14).** Volatilidad mensual y anualizada, caída máxima desde la riqueza y Sharpe
   con tasa declarada, para las cinco acciones y el índice. Tabla con unidades y convención.
4. **Regresión contra el índice (P14/P15).** Estimar beta, alpha mensual, R² y error estándar por
   acción; reportar intervalos de confianza y separar la parte de retorno explicada por el mercado de
   la residual.
5. **Contrastar el alpha (P15).** Calcular t del alpha y un bootstrap, corregir por comparar cinco
   activos y concluir si el alpha estimado puede ser suerte. La conclusión se escribe como
   «no distinguible de cero» o «evidencia insuficiente», no como una recomendación.
6. **Cartera (P14/P16).** Definir una cartera (por ejemplo, equiponderada), calcular su beta, su
   volatilidad, su caída máxima y su Sharpe, y compararla con el índice con la misma convención.
7. **Nominal, real y escenarios (P22/P16).** Separar retorno nominal de real con una inflación
   declarada, calcular el efecto de dos escenarios y una sensibilidad a tres variables (tasa,
   inflación, pesos). Escribir el memo de una página con supuestos, cifras y límites.
8. **Verificar y documentar.** Un `verificar.py` con los recuentos y las identidades (riqueza,
   beta/alpha, suma de pesos); `README.md` con comandos, convenciones y supuestos; reejecutar y
   comprobar que las tablas salen iguales.

## Criterios de terminado

- [ ] El pipeline valida 360 filas, 60 meses, 6 activos y la clave `(mes, activo)`, y el pivote
      produce una matriz 60 × 6 sin huecos.
- [ ] La riqueza acumulada es reproducible desde `retorno`; el README muestra que el retorno total es
      `prod(1 + r) − 1` y no la suma de los retornos mensuales.
- [ ] La caída máxima se calcula sobre la riqueza y se declara que, con frecuencia mensual, es una
      cota inferior de la caída real.
- [ ] La volatilidad y el Sharpe llevan la convención de anualización escrita y una tasa libre de
      riesgo declarada; ninguna tabla publica un Sharpe sin esas dos piezas.
- [ ] Beta y alpha están estimados contra el índice con su error estándar o intervalo, y el informe
      separa explícitamente el retorno de mercado del residual.
- [ ] El alpha se contrasta (t y bootstrap), se corrige por las cinco comparaciones y la conclusión
      dice si puede ser suerte; no se presenta un alpha puntual como prueba de habilidad.
- [ ] P22 calcula el retorno real con una inflación asumida y explícita; el memo de P16 cabe en una
      página, declara supuestos, presenta dos escenarios, una sensibilidad y una recomendación
      condicionada con sus límites. En ambos, lo que sale del CSV está separado de lo que es supuesto.
- [ ] `README.md` reproduce todas las tablas con comandos; reejecutar produce los mismos resultados.

## Entregables

- Código: `cargar.py`, `metricas.py` (riqueza, vol, drawdown, Sharpe), `regresion.py` (beta/alpha),
  `verificar.py`.
- `data/retornos-limpio.csv` (panel validado) y `data/riqueza.csv` (serie acumulada por activo).
- Resultados en `resultados/`: tabla de riesgo, tabla de beta/alpha con intervalos, tabla de la
  cartera y comparación con el índice.
- `memo.md` de una página (P16) con supuestos, escenarios y sensibilidad.
- `README.md` con comandos, convenciones de anualización, tasa libre de riesgo e inflación asumidas.
- Registro de comprobaciones de `verificar.py`.

## Qué demuestra y cómo se evalúa

Demuestra que distingues retorno de riesgo, que sabes anualizar sin inventar, que calculas la caída
sobre riqueza y que separas beta de alpha con su incertidumbre. En la parte de comunicación,
demuestra que puedes escribir una recomendación condicionada en lugar de una predicción.

| Criterio | Peso |
| --- | --- |
| Datos y preparación: panel, clave, pivote y unidades | 15 % |
| Métricas de riesgo: riqueza, volatilidad, drawdown y Sharpe con convención | 20 % |
| Separación beta/alpha y lectura económica de la regresión | 25 % |
| Incertidumbre y contraste del alpha (t, bootstrap, multiplicidad) | 15 % |
| P22 y memo P16: supuestos, escenarios, sensibilidad y lenguaje | 15 % |
| Reproducibilidad y verificación | 10 % |

## Riesgos típicos

- **Anualizar mal:** multiplicar el retorno medio mensual por 12 y presentarlo como retorno anual, o
  sumar retornos mensuales como si fueran aditivos.
- **Drawdown sobre retornos:** calcular la caída máxima sobre la media o sobre el retorno mensual en
  vez de sobre la riqueza acumulada.
- **Fuga de información:** estimar beta y alpha con toda la muestra y luego presentar el alpha como
  si fuera una predicción. Es una estimación in-sample y hay que decirlo.
- **Alpha = suerte:** con 60 meses y cinco acciones, un alpha positivo puede ser ruido; sin intervalo
  ni corrección por multiplicidad, la conclusión no se sostiene.
- **Supuestos disfrazados de datos:** inventar una inflación, una tasa libre de riesgo o unos pesos y
  no declararlos. El CSV no los trae.
- **Denominadores y pesos:** comparar carteras con pesos distintos sin decirlo; una cartera
  equiponderada no es «el mercado».
- **Correlación baja:** el índice explica poco de cada acción en estos datos; betas con error
  estándar grande y R² bajo son el resultado esperado, no un fallo del cálculo.
