# Fichas de los 10 datasets

Una ficha por conjunto del catálogo. **Todos los campos son los mismos y en el mismo orden**, para
que se puedan comparar de un vistazo: `id`, `título`, `fichero`, `licencia`, `procedencia`, `tamaño`,
`columnas y tipos`, `checksum`, `dificultad`, `preguntas que permite responder`, `proyectos que lo
usan` y `limitaciones`.

**Base de los datos.** Cifras de filas, columnas, tipos y unidades: [`datasets.json`](datasets.json).
Comprobación de que esas cifras se cumplen en los CSV reales: [`VERIFICACION.md`](VERIFICACION.md)
(10/10 perfiles, 63/63 columnas coherentes, 0 nulos, 0 duplicados). Checksums: los declara el
manifiesto y se recalcularon y verificaron el 2026-11-04 en
[`CATALOGO.md`](CATALOGO.md#verificación-de-integridad-sha256) (10/10). Proyectos y niveles:
[`../proyectos/CATALOGO.md`](../proyectos/CATALOGO.md), cruzando por el campo `dataset`.
Aquí no se inventa ninguna cifra: lo que no está en el manifiesto o en el catálogo, no está.

**Totales del catálogo**: 10 conjuntos · **2530 filas** · **63 definiciones de columna** · todos
sintéticos y CC0-1.0.

---

### 1. `ventas-mensuales`

- **id**: `ventas-mensuales`
- **título**: Ventas mensuales por tienda
- **fichero**: [`csv/ventas-mensuales.csv`](csv/ventas-mensuales.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 180 filas × 4 columnas
- **columnas y tipos**: `fecha` (fecha, ISO 8601) · `tienda` (texto) · `unidades` (entero, uds) · `ingresos` (decimal, EUR)
- **checksum**: `sha256:afa71a0b0ae0189e863247ff5a25f4ebe1836742ac7686f929d6a42565ecf7f6` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **básico** — 4 columnas, cero nulos y una sola serie diaria: se resuelve agregando por tienda o por semana y comprobando una proporción.
- **preguntas que permite responder**:
  - ¿Cuántas unidades y cuántos ingresos suma cada tienda en el periodo?
  - ¿Cuánto ingresa de media cada unidad vendida, y cambia ese ingreso medio por tienda?
  - ¿Hay patrón semanal en unidades e ingresos? ¿Qué día de la semana es el más flojo?
  - ¿La serie crece porque se venden más unidades o porque se ingresa más por unidad?
- **proyectos que lo usan**:
  - `proj:P04` — Sumar una matriz por filas y por columnas (intermedio, NUC/ALG)
  - `lab:L01` — Unidades y ingresos (básico, NUC/DS)
  - `lab:L08` — Del bruto al neto (básico, DE/QT)
- **limitaciones**: es sintético: tendencia y estacionalidad las fija el script, no hay ni un día de venta real; no sirve para conclusiones del mundo real. Además hay **una fila por día con la tienda rotando**, así que no se pueden comparar dos tiendas el mismo día (ver [`VERIFICACION.md`](VERIFICACION.md), nota 4).

### 2. `clientes-churn`

- **id**: `clientes-churn`
- **título**: Clientes y baja
- **fichero**: [`csv/clientes-churn.csv`](csv/clientes-churn.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 200 filas × 5 columnas
- **columnas y tipos**: `id_cliente` (texto) · `antiguedad_meses` (entero, meses) · `uso_mensual` (entero, sesiones) · `reclamaciones` (entero, uds) · `baja` (booleano, 0/1)
- **checksum**: `sha256:5290b89e3ecf746e378b01af2e73bb9e39a4297541e5ccbedae19bfc97a9839c` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **intermedio** — hay una etiqueta binaria que además está bastante repartida (94 de 200), así que no basta describir: pide clasificar y leer una matriz de confusión.
- **preguntas que permite responder**:
  - ¿Qué proporción de clientes se da de baja y cómo se reparte por antigüedad?
  - ¿Los clientes con más reclamaciones se dan de baja más que los que no reclaman?
  - ¿El uso mensual separa a los que se van de los que se quedan, o se solapan?
  - ¿Con qué umbral de uso y reclamaciones se acierta mejor la baja, y a costa de cuántos falsos positivos?
- **proyectos que lo usan**:
  - `proj:P02` — Contar duplicados en una lista (básico, NUC/ALG)
  - `proj:P05` — Cargar una tabla sin duplicarla (intermedio, DE)
  - `proj:P08` — Una métrica que aguante la revisión (intermedio, DS)
  - `lab:L03` — Quién se dará de baja (intermedio, DS)
  - `lab:L04` — Entrenar con una parte y medir con otra (intermedio, DS)
  - `lab:L06` — Juntar dos tablas sin perder filas (básico, DE)
- **limitaciones**: es sintético: la relación entre reclamaciones, uso y baja la impone el generador, así que sirve para practicar el método, no para aprender cómo se comportan clientes reales. 200 filas dan para un ejercicio, no para un modelo con garantías.

### 3. `precios-accion`

- **id**: `precios-accion`
- **título**: Precios diarios de una acción
- **fichero**: [`csv/precios-accion.csv`](csv/precios-accion.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 250 filas × 6 columnas
- **columnas y tipos**: `fecha` (fecha, ISO 8601) · `apertura` (decimal, EUR) · `cierre` (decimal, EUR) · `maximo` (decimal, EUR) · `minimo` (decimal, EUR) · `volumen` (entero, acciones)
- **checksum**: `sha256:15c9d071f65b8e34061f757405bb3a74021bd4cb7d8b333364fe215038911de7` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **intermedio** — una serie temporal diaria obliga a partir por fechas antes de medir y a usar métricas de riesgo (volatilidad, caída), no un resumen de una tabla cualquiera.
- **preguntas que permite responder**:
  - ¿Cuál es el retorno diario medio y qué volatilidad tiene en el periodo?
  - ¿Cuál fue la mayor caída desde un máximo previo y en qué fechas ocurrió?
  - ¿Los días de mayor movimiento de precio van acompañados de más volumen?
  - ¿Se distingue una tendencia real o el retorno medio es compatible con cero?
- **proyectos que lo usan**:
  - `proj:P07` — Predecir sin mirar el futuro (intermedio, DS)
  - `proj:P09` — Retornos, drawdown y costes (avanzado, QT)
  - `lab:L07` — Entrenar con el pasado y medir con el futuro (intermedio, DS/QT)
- **limitaciones**: es sintético: un paseo aleatorio con deriva fijada por el script, no un activo real. No sirve para conclusiones de mercado ni para backtesting con validez externa; las fechas son inventadas (2026-01-01 a 2026-09-07) y el volumen no sale de ninguna bolsa.

### 4. `sensores-planta`

- **id**: `sensores-planta`
- **título**: Sensores de planta
- **fichero**: [`csv/sensores-planta.csv`](csv/sensores-planta.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 240 filas × 4 columnas
- **columnas y tipos**: `hora` (entero, horas desde el inicio) · `temperatura` (decimal, °C) · `presion` (decimal, bar) · `estado` (texto)
- **checksum**: `sha256:151ed407852ef5ae874afeb18302fa9300a58f090f1302c876422f30732617aa` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **intermedio** — el efecto que se busca (la avería) convive con lecturas extremas que también son normales, así que hay que definir una línea base antes de comparar.
- **preguntas que permite responder**:
  - ¿Cómo se desvían temperatura y presión durante el episodio de avería frente a la marcha normal?
  - ¿La parada de la planta precede a la avería o solo la acompaña?
  - ¿Qué umbral de temperatura separaría marcha de avería con menos falsos avisos?
  - ¿Cuánto tarda la lectura en volver a los valores de marcha después de la avería?
- **proyectos que lo usan**:
  - `proj:P10` — Un evento y su efecto, con límites (avanzado, QT)
- **limitaciones**: es sintético: el episodio de avería está fabricado y las temperaturas y presiones no corresponden a ningún equipo real. Sirve para practicar el antes/después con ruido, no para diagnosticar una planta.

### 5. `encuestas-satisfaccion`

- **id**: `encuestas-satisfaccion`
- **título**: Encuestas de satisfacción
- **fichero**: [`csv/encuestas-satisfaccion.csv`](csv/encuestas-satisfaccion.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 160 filas × 4 columnas
- **columnas y tipos**: `id` (texto) · `segmento` (texto) · `puntuacion` (entero, 0-10) · `recomienda` (booleano, 0/1)
- **checksum**: `sha256:da16c0e54b3c37555f51947ff9d605aeb07a8051495d23aa708859a12f2e63db` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **básico** — dos variables útiles y dos columnas que solo identifican: es comparar medias por segmento con su incertidumbre, sin más fontanería.
- **preguntas que permite responder**:
  - ¿Qué puntuación media da cada segmento y cuánta incertidumbre tiene esa media?
  - ¿Puntuación y recomendación dicen lo mismo, o hay quien puntúa alto y no recomienda?
  - ¿Qué proporción de insatisfechos (puntuación baja) hay en cada segmento?
  - ¿Cambiar el corte de «satisfecho» (7, 8 o 9) cambia la conclusión por segmento?
- **proyectos que lo usan**:
  - `proj:P06` — Controles de calidad que fallan cuando deben (intermedio, DE)
  - `lab:L02` — Veteranos frente a nuevos (básico, NUC/DS)
- **limitaciones**: es sintético: las puntuaciones están simuladas y los segmentos y la cola de insatisfechos los coloca el script, no se midieron a nadie. No sirve para conclusiones sobre satisfacción real.

### 6. `algoritmos-tiempos`

- **id**: `algoritmos-tiempos`
- **título**: Tiempos de algoritmos
- **fichero**: [`csv/algoritmos-tiempos.csv`](csv/algoritmos-tiempos.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 180 filas × 3 columnas
- **columnas y tipos**: `algoritmo` (texto) · `n` (entero, elementos) · `milisegundos` (decimal, ms)
- **checksum**: `sha256:b1965e63ca0a4987ded90cc2d71cb22167c11fa2041673de9484f5f3cdc8cbe7` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **intermedio** — los tiempos son muy asimétricos y hay que ajustar crecimiento (por ejemplo en escala logarítmica) en vez de comparar medias a ojo.
- **preguntas que permite responder**:
  - ¿Cuánto crece el tiempo de cada algoritmo al duplicar `n`, y qué exponente implica ese crecimiento?
  - ¿Qué algoritmo es más rápido con `n` pequeño y cuál con `n` grande: hay punto de cruce?
  - ¿La diferencia entre crecimiento lineal-logarítmico y cuadrático se ve en los datos o hay que forzar la escala?
  - ¿Qué algoritmo compensa a `n` grande y a partir de qué tamaño deja de compensar el más simple?
- **proyectos que lo usan**:
  - `proj:P01` — Comparar dos algoritmos de ordenación (básico, NUC/ALG)
  - `proj:P03` — Buscar un valor en una lista ordenada (intermedio, NUC/ALG)
  - `lab:L05` — Bajar por la parábola (intermedio, NUC/ALG/DS)
- **limitaciones**: es sintético: los milisegundos salen del modelo de coste del generador, no de medir una máquina real. No vale como benchmark ni para decidir qué algoritmo usar en producción; cada par `(algoritmo, n)` aparece una sola vez, así que no hay repeticiones para estimar dispersión.

### 7. `telemetria-f1`

- **id**: `telemetria-f1`
- **título**: Telemetria de una carrera
- **fichero**: [`csv/telemetria-f1.csv`](csv/telemetria-f1.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 180 filas × 10 columnas
- **columnas y tipos**: `carrera` (texto) · `piloto` (texto) · `vuelta` (entero, vueltas) · `compuesto` (texto) · `edad_neumatico` (entero, vueltas) · `sector1_s` (decimal, s) · `sector2_s` (decimal, s) · `sector3_s` (decimal, s) · `tiempo_vuelta_s` (decimal, s) · `parada` (booleano, 0/1)
- **checksum**: `sha256:c232e767dc95184fddeb329f6a7c4c72ccb13423a2961bea717cd464150c2c3b` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **intermedio** — 10 columnas en un panel carrera × piloto × vuelta: para comparar ritmos hay que controlar compuesto y edad del neumático, no basta agrupar.
- **preguntas que permite responder**:
  - ¿Cuánto se pierde en la vuelta de la parada frente al ritmo del mismo compuesto?
  - ¿El ritmo mejora o empeora a medida que el neumático envejece?
  - ¿Hay diferencia de ritmo entre los dos pilotos con el mismo compuesto y la misma edad de neumático?
  - ¿La pérdida de tiempo se reparte igual en los tres sectores o se concentra en uno?
  - ¿El ritmo antes y después de la parada cambia más de lo que cabe esperar por ruido?
- **proyectos que lo usan**:
  - `proj:P11` — Limpiar y unir la telemetria de una carrera (intermedio, DE)
  - `proj:P12` — Un panel de carrera con una sola pregunta (intermedio, DE)
  - `proj:P13` — ¿Le costo la carrera la parada? (intermedio, DS)
- **limitaciones**: es sintético: las vueltas son simuladas y no hay telemetría de ningún coche ni circuito real. Sirve para practicar el control por compuesto y la comparación antes/después, no para analizar una carrera de verdad.

### 8. `cartera-acciones`

- **id**: `cartera-acciones`
- **título**: Cartera de acciones frente a un indice
- **fichero**: [`csv/cartera-acciones.csv`](csv/cartera-acciones.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 360 filas × 3 columnas
- **columnas y tipos**: `mes` (fecha, ISO 8601) · `activo` (texto) · `retorno` (decimal, tanto por uno)
- **checksum**: `sha256:62ccc9a7355a27559024f7e4b725792d2be58a379fad4b4740a8a6fd25eacd51` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **avanzado** — con un panel de 60 meses × 6 activos se pueden calcular beta, alfa, volatilidad y Sharpe, y cada cifra exige declarar su supuesto y su error.
- **preguntas que permite responder**:
  - ¿Qué retorno medio y qué volatilidad tiene cada activo, y cuál da mejor relación riesgo-retorno?
  - ¿Qué parte del retorno de cada acción explica el índice (beta) y qué parte es propia del activo?
  - ¿El alfa estimado supera su error estándar o cabe dentro del ruido?
  - ¿Cómo se comporta la cartera completa frente al índice mes a mes?
- **proyectos que lo usan**:
  - `proj:P22` — Finanzas desde cero: interés, inflación y riesgo (básico, DS)
  - `proj:P16` — Un memo de inversion con supuestos y sensibilidad (intermedio, DS)
  - `proj:P14` — El riesgo de una cartera, medido (avanzado, QT)
  - `proj:P15` — ¿Batir al indice o asumir mas riesgo? (avanzado, QT)
- **limitaciones**: es sintético: los retornos salen de un factor de mercado común más ruido propio, no de series bursátiles reales. Con 60 meses las estimaciones de beta y alfa son ruidosas por diseño; no sirve para conclusiones de inversión.

### 9. `f1-clasificacion`

- **id**: `f1-clasificacion`
- **título**: Clasificacion y carrera de F1
- **fichero**: [`csv/f1-clasificacion.csv`](csv/f1-clasificacion.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 400 filas × 12 columnas
- **columnas y tipos**: `carrera` (texto) · `piloto` (texto) · `equipo` (texto) · `posicion_quali` (entero, puesto) · `vuelta_quali_s` (decimal, s) · `sector1_s` (decimal, s) · `sector2_s` (decimal, s) · `sector3_s` (decimal, s) · `compuesto` (texto) · `temperatura_c` (decimal, °C) · `posicion_final` (entero, puesto) · `puntos` (entero, puntos)
- **checksum**: `sha256:2cd5b45e02b14ad12bae786880bf4a175cfc8d2a2ea13d286e28384779054a93` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **avanzado** — 12 columnas y un riesgo de fuga dentro de la propia tabla: la posición final convive con la de clasificación y es fácil «predecir» con lo que ya es consecuencia.
- **preguntas que permite responder**:
  - ¿Cuánto pesa cada sector, el compuesto y la temperatura en el tiempo de vuelta de clasificación?
  - ¿La posición de clasificación predice la posición final, y cuánto se desvía en cada carrera?
  - ¿El compuesto elegido se relaciona con la temperatura de la sesión?
  - ¿Se puede estimar la posición de clasificación sin usar la posición final ni puntos, y sin mezclar carreras?
- **proyectos que lo usan**:
  - `proj:P17` — Del API de F1 a un lago, sin romper nada (intermedio, DE)
  - `proj:P18` — Predecir la clasificación sin mirar la carrera (avanzado, DS)
  - `proj:P19` — ¿Merece la pena el undercut? (avanzado, DS)
- **limitaciones**: es sintético: 20 pilotos y 5 equipos inventados, no una parrilla real. Las relaciones entre sectores, compuesto y posición final las fija el generador, así que un modelo que «funcione» aquí no demuestra nada sobre F1 real.

### 10. `futbol-partidos`

- **id**: `futbol-partidos`
- **título**: Partidos de liga con tiros y xG
- **fichero**: [`csv/futbol-partidos.csv`](csv/futbol-partidos.csv)
- **licencia**: CC0-1.0
- **procedencia**: sintético; generado por [`generar-datasets.mjs`](generar-datasets.mjs) con PRNG de semilla fija por conjunto y copiado byte a byte del proyecto de origen (`aprender`, `web/datos/datasets/`). No procede de personas ni de fuentes de terceros.
- **tamaño**: 380 filas × 12 columnas
- **columnas y tipos**: `jornada` (entero, jornada) · `local` (texto) · `visitante` (texto) · `goles_local` (entero, goles) · `goles_visitante` (entero, goles) · `tiros_local` (entero, tiros) · `tiros_visitante` (entero, tiros) · `xg_local` (decimal, goles esperados) · `xg_visitante` (decimal, goles esperados) · `posesion_local` (entero, %) · `amarillas` (entero, tarjetas) · `resultado` (texto, 1 X 2)
- **checksum**: `sha256:5cbc8977b6c9d4f7ae66bfcc7642c93a6655faf7b6e6524a6d40480e2e66a12e` — SHA-256 del manifiesto, calculado sobre los bytes completos del CSV; el del fichero coincide (10/10)
- **dificultad**: **avanzado** — exige montar un modelo en estrella (un hecho por partido con dimensiones de equipo y jornada) y tratar el marcador como variable aleatoria frente al xG, que son dos trabajos distintos.
- **preguntas que permite responder**:
  - ¿El xG de cada equipo se parece a sus goles a lo largo de la liga o se desvía?
  - ¿Qué equipos rinden por encima de su xG y cuánto de esa diferencia puede ser suerte?
  - ¿Los tiros explican el xG, y el xG explica el resultado del partido?
  - ¿La posesión se asocia a más tiros y a más goles, o no hay relación clara?
  - ¿Cuántos puntos saca cada equipo y cuadra con la suma de resultados de sus partidos?
- **proyectos que lo usan**:
  - `proj:P20` — Fútbol: ingesta y modelo en estrella (intermedio, DE)
  - `proj:P21` — Fútbol: el xG no es el marcador (avanzado, DS)
- **limitaciones**: es sintético: liga inventada de 20 equipos y 38 jornadas, no una competición real. El xG sale del generador, no de un modelo de tiro real, y `resultado` está escrito como `1`/`X`/`2`, así que al cargar el CSV hay que forzarlo a texto (ver [`VERIFICACION.md`](VERIFICACION.md), nota 1).

---

## Nota común a las 10 fichas

**Todos los conjuntos son sintéticos.** Los genera un PRNG de semilla fija y ninguno procede de
personas ni de fuentes de terceros; de ahí que se puedan alojar con licencia CC0-1.0. Consecuencia que
vale para los diez: **sirven para practicar el método y para comprobar que un resultado cuadra, no
para sacar conclusiones del mundo real.** Un hallazgo sobre estos datos no se traslada a ventas,
clientes, mercados, plantas, pilotos ni partidos de verdad, porque las relaciones entre variables son
las que impone el generador. Lo que sí es real es la reproducibilidad: mismo script y misma semilla,
mismos bytes y mismo SHA-256 (ver [`README.md`](README.md#cómo-se-regeneran)).

Otras piezas de esta carpeta: [`CATALOGO.md`](CATALOGO.md) (tabla generada desde el manifiesto),
[`VERIFICACION.md`](VERIFICACION.md) (perfiles y contraste con el manifiesto),
[`FUENTES-EXTERNAS.md`](FUENTES-EXTERNAS.md) (datasets ajenos que solo se enlazan).
