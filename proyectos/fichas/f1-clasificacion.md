# Ficha · f1-clasificacion — ingesta, fuga temporal y puesto de carrera

**Estado:** ficha de enunciado. No hay implementación de este proyecto en la carpeta: aquí se fija
qué construir, con qué datos del catálogo y cómo se demuestra que está terminado. Las fichas
hermanas son [telemetria-f1](telemetria-f1.md), [cartera-acciones](cartera-acciones.md) y
[futbol-partidos](futbol-partidos.md).

## Datos asignados

- **CSV:** [`datasets/csv/f1-clasificacion.csv`](../../datasets/csv/f1-clasificacion.csv) — **400
  filas** y **12 columnas**; sintético, semilla fija y licencia CC0-1.0. Tamaño y checksum en
  [`datasets/CATALOGO.md`](../../datasets/CATALOGO.md).
- **Catálogo de proyectos:** [`proyectos/CATALOGO.md`](../CATALOGO.md) — cubre los proyectos P17, P18
  y P19.
- **Ficha del dataset:** [`datasets/FICHAS.md`](../../datasets/FICHAS.md) — procedencia, checksum y
  preguntas que permite responder.
- **Columnas:** `carrera`, `piloto`, `equipo`, `posicion_quali`, `vuelta_quali_s`, `sector1_s`,
  `sector2_s`, `sector3_s`, `compuesto`, `temperatura_c`, `posicion_final`, `puntos`.

## Proyectos del catálogo que cubre

| ID | Título del catálogo | Nivel |
| --- | --- | --- |
| P17 | Del API de F1 a un lago, sin romper nada | intermedio |
| P18 | Predecir la clasificación sin mirar la carrera | avanzado |
| P19 | ¿Merece la pena el undercut? | avanzado |

## Nivel y rutas

- **P17:** intermedio, ruta **DE**. Ingesta idempotente y capa de datos.
- **P18:** avanzado, ruta **DS**. Auditoría de fuga, partición por carrera e inferencia.
- **P19:** avanzado, ruta **DS**. Análisis de efecto con datos que no bastan: hay que decir qué falta.
- **Requisitos previos:** Python o SQL, validación de datos, regresión y validación cruzada por
  grupos, intervalos de confianza. P18 y P19 dependen de la tabla limpia de P17.

## Tiempo estimado

| Proyecto | Horas |
| --- | --- |
| P17 | 6–8 h |
| P18 | 8–10 h |
| P19 | 5–7 h |

Total de la ficha: **19–25 h**. P19 es corto en código y largo en criterio: la mitad del trabajo es
documentar por qué el CSV asignado no permite medir un undercut.

## Enunciado

El CSV es una temporada sintética de veinte carreras con veinte pilotos: tiempos de clasificación por
sectores, compuesto de neumático, temperatura, puesto final y puntos. Construye primero una ingesta
que guarde el bruto y deje un hecho por `(carrera, piloto)` que no se duplique al recargar (P17);
después, un análisis honesto del puesto (P18); y, por último, la pregunta del adelantamiento en
parada (P19), incluida la parte incómoda: con estas columnas no se puede medir.

La trampa central del dataset es que el puesto de clasificación es el **rango del tiempo de vuelta**,
y el tiempo de vuelta es la suma de los sectores. Un modelo que use los sectores para «predecir» el
puesto de clasificación no aprende nada: hace aritmética. El proyecto vale si se demuestra esa
equivalencia, se elige un objetivo que sí admita aprendizaje (el puesto final de carrera a partir de
la clasificación, sin usar el resultado como entrada) y se declara la fuga antes de mirar la métrica.

## Datos y preparación

- **Estructura:** 400 filas = 20 carreras (`r01`–`r20`) × 20 pilotos (`P01`–`P20`); clave natural
  `(carrera, piloto)`, sin nulos ni claves repetidas. Cinco equipos con cuatro pilotos fijos cada uno,
  así que equipo y piloto están confundidos: no se puede separar «buen coche» de «buen piloto».
- **`posicion_quali` es derivada:** coincide con el rango de `vuelta_quali_s`, salvo dos parejas con
  tiempo idéntico (carrera r01 y carrera r05) donde el desempate es arbitrario. Ordenar por tiempo y
  comparar con la columna es una comprobación obligatoria.
- **Sectores:** `sector1_s + sector2_s + sector3_s ≈ vuelta_quali_s` (diferencia de milésimas por
  redondeo). Son un desglose del mismo dato, no tres predictores independientes.
- **`posicion_final` no es una permutación:** hay puestos repetidos dentro de una carrera (hasta siete
  puestos duplicados en algunas). En 11 carreras hay un único primero y en 9 no: seis no tienen
  ninguna fila en el puesto 1 y tres tienen dos o tres filas empatadas en el primero. Cualquier
  métrica de ranking debe tratar los empates.
- **`puntos` es una función determinista de `posicion_final`** (25-18-15-12-10-8-6-4-2-1, cero a
  partir del 11.º). No es una variable independiente: usarla como feature del puesto final es fuga.
- **Compuesto y temperatura:** solo hay `blando` y `medio`; el compuesto es el de la clasificación, no
  el de carrera. La temperatura se mueve en una franja estrecha (24–32 °C). Poca señal, y la poca que
  hay está mezclada con el equipo.
- **Lo que no hay:** paradas, vueltas de carrera, edad del neumático ni tiempos por vuelta. Por eso el
  **undercut de P19 no se puede medir con este CSV**; ver la ficha
  [telemetria-f1](telemetria-f1.md), que sí tiene parada y edad de neumático.
- **P17 y el «API»:** en esta carpeta no hay API. El CSV se trata como un snapshot de la fuente: se
  guarda el bruto con fecha y `sha256`, se carga a staging tipado y se publica el hecho. La versión
  real con OpenF1 ya existe en [`pf-02-openf1`](../pf-02-openf1/README.md); esta ficha usa el dataset
  asignado y no descarga nada.

## Pasos

1. **Ingesta idempotente (P17).** Copiar el CSV a `data/raw/` con fecha y `sha256`, tipar columnas en
   staging y cargar un hecho con clave `(carrera, piloto)`. Recargar dos veces y demostrar 400 filas
   únicas, 20 carreras y 20 pilotos.
2. **Auditoría del dato (P17/P18).** Comprobar rangos 1–20, unicidad de la clave, empates de vuelta,
   puestos finales repetidos y coherencia de `puntos` con `posicion_final`. Dejar la auditoría escrita.
3. **Auditoría de fuga (P18).** Declarar la lista de columnas prohibidas como entrada
   (`posicion_final`, `puntos`) y comprobar en el código que no entran en la matriz de features.
4. **Control de tautología (P18).** Ordenar por `vuelta_quali_s` y comparar con `posicion_quali`;
   documentar las dos parejas empatadas y concluir que usar sectores para predecir el puesto de
   clasificación es aritmética. Calcular la línea base «puesto final = puesto de clasificación».
5. **Modelo aprendible (P18).** Predecir `posicion_final` con features de clasificación (puesto,
   tiempo, sectores, compuesto, temperatura, equipo), con validación **dejando una carrera fuera**
   cada vez. Reportar MAE y correlación de rangos frente a la línea base.
6. **Incertidumbre y errores (P18).** Bootstrap agrupado por carrera para la diferencia con la línea
   base; concluir si la mejora supera el ruido. Analizar los errores (¿carreras con más empates?).
7. **P19 con lo que hay.** Documentar las columnas que exigiría un undercut (parada, edad, tiempo de
   vuelta) y demostrar que faltan. Medir como proxy el cambio de puestos entre clasificación y
   carrera, estratificado por compuesto y temperatura, con intervalo; concluir que no es un undercut.
8. **Verificar y documentar.** `verificar.py` con recuentos, unicidad e idempotencia; `README.md` con
   comandos, resultados y límites; reejecutar y comparar.

## Criterios de terminado

- [ ] La ingesta deja 400 filas, 20 carreras y 20 pilotos, con clave `(carrera, piloto)` única; el
      bruto guarda fecha y `sha256`, y una segunda ejecución deja exactamente las mismas 400 filas.
- [ ] La auditoría documenta empates de `vuelta_quali_s`, puestos finales repetidos y la relación
      `puntos = f(posicion_final)`; ninguna fila se descarta sin motivo escrito.
- [ ] El código demuestra que `posicion_final` y `puntos` no entran como features del modelo de P18
      (lista explícita o comprobación en `verificar.py`).
- [ ] El control de tautología reproduce `posicion_quali` ordenando por tiempo, documenta las dos
      parejas empatadas y dice con claridad que predecir el puesto de clasificación con sectores no es
      aprendizaje.
- [ ] El modelo de P18 se evalúa dejando carreras fuera (sin filas de la misma carrera en train y
      test) y se compara con la línea base «puesto final = puesto de clasificación» en la misma tabla.
- [ ] La métrica va con incertidumbre (bootstrap por carrera) y los empates de `posicion_final` se
      tratan de forma declarada, sin forzar una permutación perfecta; el informe explica el efecto de
      los empates y concluye si la mejora sobre la línea base puede ser ruido.
- [ ] P19 enumera las columnas que faltan para medir un undercut, no las inventa, mide un proxy
      declarado y concluye que el CSV asignado no permite responder la pregunta original.
- [ ] `README.md` reproduce los resultados y las comprobaciones con comandos; reejecutar da lo mismo.

## Entregables

- Código: `ingerir.py` (snapshot + staging + hecho), `auditar.py`, `modelo.py`, `verificar.py`.
- `data/raw/f1-clasificacion-<fecha>.csv` (bruto inmutable) y `data/hecho-clasificacion.csv`.
- Resultados: auditoría de datos, tabla de línea base vs modelo, intervalos y análisis de errores.
- Informe corto de P19 con la lista de columnas ausentes y el proxy medido.
- `README.md` con comandos, recuentos, decisiones de fuga y límites.
- Registro de comprobaciones de `verificar.py`.

## Qué demuestra y cómo se evalúa

Demuestra que sabes montar una ingesta idempotente sobre una fuente que no es una API, que auditas la
fuga antes de modelar y que reconoces una tautología: el puesto de clasificación no se «predice» con
los sectores, se reconstruye. También demuestra que puedes decir que un dataset no permite responder
una pregunta, en lugar de fabricar una respuesta.

| Criterio | Peso |
| --- | --- |
| Ingesta idempotente, bruto y recuentos | 20 % |
| Auditoría del dato y de la fuga (columnas prohibidas) | 20 % |
| Control de tautología y línea base | 20 % |
| Modelo con partición por carrera y métricas de puesto | 20 % |
| Incertidumbre, empates y análisis de errores | 10 % |
| P19: límites de datos y proxy declarado | 10 % |

## Riesgos típicos

- **Fuga por `posicion_final` o `puntos`:** usarlos como entrada y obtener una métrica excelente que
  no significa nada. La comprobación debe estar en el código, no en la memoria.
- **Mezclar carreras:** partir filas al azar reparte condiciones de la misma carrera entre train y
  test. La partición correcta es por carrera.
- **Tautología:** incluir la vuelta o los sectores y llamar «modelo» al ranking. Si el objetivo es el
  puesto de clasificación, la línea base aritmética ya es perfecta (salvo empates).
- **Empates silenciados:** forzar puestos únicos o descartar filas empatadas para que la métrica
  cuadre. El dataset tiene empates; se documentan.
- **Confusor equipo–piloto:** cuatro pilotos por equipo y veinte carreras no separan coche de piloto.
- **P19 mal planteado:** construir un «undercut» sin paradas ni edad de neumático. El CSV no lo
  permite; se dice y se enlaza la ficha de telemetría.
- **Suponer una API que no existe:** P17 se resuelve con un snapshot del CSV; si se quiere la versión
  real, está en PF-02.
