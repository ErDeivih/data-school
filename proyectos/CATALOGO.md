# Catálogo de proyectos y laboratorios del portal

**Qué es.** Los 22 proyectos (P01–P22) y los 8 laboratorios (L01–L08) que el portal vivo
(`aprender`) presenta como catálogo de trabajo práctico, con su nivel, sus rutas de estudio y
el conjunto de datos asignado. Es contenido propio del proyecto Data School: no se copian
enunciados de terceros.

**Procedencia.** Extraído con Node el **2026-11-04** de `web/datos/portal.js`
(`window.PORTAL.recursos`, el bloque que alimenta el catálogo del portal), y contrastado con el
índice de búsqueda `web/datos/busqueda.js` (`window.BUSQUEDA`), que contiene las mismas 30 claves
`proj:P01`–`proj:P22` y `lab:L01`–`lab:L08`. Los títulos, resúmenes y niveles son literales del
portal; aquí solo se tabulan. Algunas entradas del portal están escritas sin tildes en el origen: se
respetan tal cual, sin corregirlas.

**Recuento.** 30 recursos: 22 proyectos y 8 laboratorios. Por nivel: 
básico 7 · intermedio 16 · avanzado 7.

---

## 1. Proyectos (22)

Ordenados por id. `Rutas` usa las siglas del portal: NUC = Núcleo, DE = Data engineering,
DS = Data science, QT = Quant / trading, ALG = Algoritmos y software.

### Nivel básico (3)

| ID | Título | Resumen | Rutas | Dataset |
| --- | --- | --- | --- | --- |
| proj:P01 | Comparar dos algoritmos de ordenación | Medir burbuja y mezcla con tamaños crecientes y explicar cuál crece más deprisa. | NUC/ALG | `algoritmos-tiempos` |
| proj:P02 | Contar duplicados en una lista | Detectar repetidos y decir cuántos hay y cuáles, con un método que se pueda repetir. | NUC/ALG | `clientes-churn` |
| proj:P22 | Finanzas desde cero: interés, inflación y riesgo | Calcular la rentabilidad real de una cartera, separar nominal de inflación y medir el riesgo sin adelantar la conclusión. | DS | `cartera-acciones` |

### Nivel intermedio (12)

| ID | Título | Resumen | Rutas | Dataset |
| --- | --- | --- | --- | --- |
| proj:P03 | Buscar un valor en una lista ordenada | Comparar búsqueda lineal y binaria, y explicar por qué una es más rápida. | NUC/ALG | `algoritmos-tiempos` |
| proj:P04 | Sumar una matriz por filas y por columnas | Recorrer una matriz, sumar por filas y por columnas, y comprobar que los totales coinciden. | NUC/ALG | `ventas-mensuales` |
| proj:P05 | Cargar una tabla sin duplicarla | Deduplicar por clave y demostrar que repetir la carga no cambia el resultado. | DE | `clientes-churn` |
| proj:P06 | Controles de calidad que fallan cuando deben | Escribir controles que detecten vacíos, repetidos y valores fuera de rango, y probarlos con un caso sucio y otro limpio. | DE | `encuestas-satisfaccion` |
| proj:P07 | Predecir sin mirar el futuro | Partir por fechas, entrenar con el pasado y medir con el futuro, demostrando que no hay fuga. | DS | `precios-accion` |
| proj:P08 | Una métrica que aguante la revisión | Calcular exactitud, sensibilidad y precisión desde la matriz, y detectar una declarada que no sale de las cuentas. | DS | `clientes-churn` |
| proj:P11 | Limpiar y unir la telemetria de una carrera | Ordenar las vueltas de dos pilotos en tres carreras, separar las paradas y dejar un ritmo por compuesto que se pueda comparar. | DE | `telemetria-f1` |
| proj:P12 | Un panel de carrera con una sola pregunta | Elegir una pregunta que se pueda responder con la telemetria, agregar por stint y dejar un panel con su fuente y su limite. | DE | `telemetria-f1` |
| proj:P13 | ¿Le costo la carrera la parada? | Comparar el ritmo antes y despues de la parada controlando el compuesto, y decir cuanto de la diferencia puede ser ruido. | DS | `telemetria-f1` |
| proj:P16 | Un memo de inversion con supuestos y sensibilidad | Escribir una recomendacion de una pagina con supuestos explicitos, dos escenarios y una sensibilidad que se pueda discutir. | DS | `cartera-acciones` |
| proj:P17 | Del API de F1 a un lago, sin romper nada | Ingerir clasificaciones de carrera desde una API, guardar el bruto y dejar una tabla que no se duplique al repetir la carga. | DE | `f1-clasificacion` |
| proj:P20 | Fútbol: ingesta y modelo en estrella | Convertir una tabla de partidos en un hecho por partido con dimensiones de equipo y jornada, comprobando que los totales cuadran. | DE | `futbol-partidos` |

### Nivel avanzado (7)

| ID | Título | Resumen | Rutas | Dataset |
| --- | --- | --- | --- | --- |
| proj:P09 | Retornos, drawdown y costes | Calcular el retorno acumulado de una serie, su mayor caída y lo que queda tras los costes. | QT | `precios-accion` |
| proj:P10 | Un evento y su efecto, con límites | Comparar la serie alrededor de un evento y decir qué se puede y qué no se puede concluir. | QT | `sensores-planta` |
| proj:P14 | El riesgo de una cartera, medido | Calcular beta, volatilidad, caida maxima y Sharpe de cinco acciones frente a un indice y explicar que mide cada cifra. | QT | `cartera-acciones` |
| proj:P15 | ¿Batir al indice o asumir mas riesgo? | Separar el retorno que se explica por el mercado del que no, y decir si el alpha estimado puede ser suerte. | QT | `cartera-acciones` |
| proj:P18 | Predecir la clasificación sin mirar la carrera | Estimar el puesto de clasificación con los sectores, el compuesto y la temperatura, sin colar la posición final ni mezclar carreras. | DS | `f1-clasificacion` |
| proj:P19 | ¿Merece la pena el undercut? | Comparar el efecto de adelantar la parada, controlando el compuesto y la edad del neumático, y decir cuánto puede ser ruido. | DS | `f1-clasificacion` |
| proj:P21 | Fútbol: el xG no es el marcador | Usar xG para estimar probabilidades de resultado, compararlo con una linea base y decir qué parte del marcador es azar. | DS | `futbol-partidos` |

## 2. Laboratorios (8)

| ID | Título | Resumen | Nivel | Rutas | Dataset |
| --- | --- | --- | --- | --- | --- |
| lab:L01 | Unidades y ingresos | Regresión e intervalo de confianza entre unidades vendidas e ingresos. | básico | NUC/DS | `ventas-mensuales` |
| lab:L02 | Veteranos frente a nuevos | Comparar dos medias de satisfacción y su incertidumbre. | básico | NUC/DS | `encuestas-satisfaccion` |
| lab:L03 | Quién se dará de baja | Clasificación, matriz de confusión y cambio de umbral para clientes. | intermedio | DS | `clientes-churn` |
| lab:L04 | Entrenar con una parte y medir con otra | Separar entrenamiento y prueba para observar el sobreajuste. | intermedio | DS | `clientes-churn` |
| lab:L05 | Bajar por la parábola | Descenso de gradiente: paso, convergencia y divergencia. | intermedio | NUC/ALG/DS | `algoritmos-tiempos` |
| lab:L06 | Juntar dos tablas sin perder filas | Joins SQL y multiplicación de filas con claves duplicadas. | básico | DE | `clientes-churn` |
| lab:L07 | Entrenar con el pasado y medir con el futuro | Partición temporal de precios y fuga de información futura. | intermedio | DS/QT | `precios-accion` |
| lab:L08 | Del bruto al neto | Medir costes fijos y variables sobre importes sintéticos. | básico | DE/QT | `ventas-mensuales` |

## 3. Datasets asignados (10)

Los 10 conjuntos sintéticos del portal a los que remiten los recursos, con tamaño y licencia.
Todos son CC0-1.0 y de origen sintético.

| Dataset | Conjunto | Filas | Licencia |
| --- | --- | --- | --- |
| `algoritmos-tiempos` | Tiempos de algoritmos | 180 | CC0-1.0 |
| `cartera-acciones` | Cartera de acciones frente a un indice | 360 | CC0-1.0 |
| `clientes-churn` | Clientes y baja | 200 | CC0-1.0 |
| `encuestas-satisfaccion` | Encuestas de satisfacción | 160 | CC0-1.0 |
| `f1-clasificacion` | Clasificacion y carrera de F1 | 400 | CC0-1.0 |
| `futbol-partidos` | Partidos de liga con tiros y xG | 380 | CC0-1.0 |
| `precios-accion` | Precios diarios de una acción | 250 | CC0-1.0 |
| `sensores-planta` | Sensores de planta | 240 | CC0-1.0 |
| `telemetria-f1` | Telemetria de una carrera | 180 | CC0-1.0 |
| `ventas-mensuales` | Ventas mensuales por tienda | 180 | CC0-1.0 |

## 4. Cómo se usa este catálogo

- Dos de los 22 proyectos están completos en esta carpeta, con código, datos y criterio de
  terminado verificable: **PF-01** (`pf-01-pulso-poblacion/`) y **PF-02** (`pf-02-openf1/`).
  Ver el [README](README.md) de `proyectos/`.
- Los 20 restantes y los 8 laboratorios son el catálogo del portal: sirven como mapa de qué
  practicar y con qué dataset, no como enunciados importados.
- Un laboratorio es una pieza corta sobre un dataset; un proyecto cruza varias capas
  (ingesta, modelo, verificación, panel) y termina con un criterio de terminado explícito.
