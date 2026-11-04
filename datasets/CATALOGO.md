# Catálogo de datasets — Data School

Fecha de generación: **2026-11-04**. Generado a partir de [`datasets.json`](datasets.json)
(manifiesto `version: 1`, `generadoPor: datos/generar-datasets.mjs`, semilla fija por conjunto,
licencia `CC0-1.0 (datos sinteticos)`).

Cada conjunto lleva: **id**, **título**, **fichero**, **filas**, **columnas con tipo y unidad**,
**licencia**, **origen** y **checksum**. Los 10 CSV están en [`csv/`](csv/).

Nota de rutas: el campo `fichero` del manifiesto apunta a `datos/datasets/<id>.csv`, la ruta del
proyecto de origen (`aprender`); en este repositorio los CSV se copiaron a `datasets/csv/`. El
manifiesto se conserva tal cual, sin reescribir sus rutas.

## Verificación de integridad (sha256)

Se recalculó el SHA-256 de los bytes de cada CSV y se comparó con el `checksum` que declara el
manifiesto (mismo prefijo `sha256:`). Resultado de la comprobación del 2026-11-04:

| # | Conjunto | Fichero | Filas | Cols. | sha256 del manifiesto | sha256 del fichero | sha256 coincide (sí/no) |
|---|---|---|---|---|---|---|---|
| 1 | `ventas-mensuales` | `csv/ventas-mensuales.csv` | 180 | 4 | `sha256:afa71a0b0ae0189e863247ff5a25f4ebe1836742ac7686f929d6a42565ecf7f6` | `sha256:afa71a0b0ae0189e863247ff5a25f4ebe1836742ac7686f929d6a42565ecf7f6` | **sí** |
| 2 | `clientes-churn` | `csv/clientes-churn.csv` | 200 | 5 | `sha256:5290b89e3ecf746e378b01af2e73bb9e39a4297541e5ccbedae19bfc97a9839c` | `sha256:5290b89e3ecf746e378b01af2e73bb9e39a4297541e5ccbedae19bfc97a9839c` | **sí** |
| 3 | `precios-accion` | `csv/precios-accion.csv` | 250 | 6 | `sha256:15c9d071f65b8e34061f757405bb3a74021bd4cb7d8b333364fe215038911de7` | `sha256:15c9d071f65b8e34061f757405bb3a74021bd4cb7d8b333364fe215038911de7` | **sí** |
| 4 | `sensores-planta` | `csv/sensores-planta.csv` | 240 | 4 | `sha256:151ed407852ef5ae874afeb18302fa9300a58f090f1302c876422f30732617aa` | `sha256:151ed407852ef5ae874afeb18302fa9300a58f090f1302c876422f30732617aa` | **sí** |
| 5 | `encuestas-satisfaccion` | `csv/encuestas-satisfaccion.csv` | 160 | 4 | `sha256:da16c0e54b3c37555f51947ff9d605aeb07a8051495d23aa708859a12f2e63db` | `sha256:da16c0e54b3c37555f51947ff9d605aeb07a8051495d23aa708859a12f2e63db` | **sí** |
| 6 | `algoritmos-tiempos` | `csv/algoritmos-tiempos.csv` | 180 | 3 | `sha256:b1965e63ca0a4987ded90cc2d71cb22167c11fa2041673de9484f5f3cdc8cbe7` | `sha256:b1965e63ca0a4987ded90cc2d71cb22167c11fa2041673de9484f5f3cdc8cbe7` | **sí** |
| 7 | `telemetria-f1` | `csv/telemetria-f1.csv` | 180 | 10 | `sha256:c232e767dc95184fddeb329f6a7c4c72ccb13423a2961bea717cd464150c2c3b` | `sha256:c232e767dc95184fddeb329f6a7c4c72ccb13423a2961bea717cd464150c2c3b` | **sí** |
| 8 | `cartera-acciones` | `csv/cartera-acciones.csv` | 360 | 3 | `sha256:62ccc9a7355a27559024f7e4b725792d2be58a379fad4b4740a8a6fd25eacd51` | `sha256:62ccc9a7355a27559024f7e4b725792d2be58a379fad4b4740a8a6fd25eacd51` | **sí** |
| 9 | `f1-clasificacion` | `csv/f1-clasificacion.csv` | 400 | 12 | `sha256:2cd5b45e02b14ad12bae786880bf4a175cfc8d2a2ea13d286e28384779054a93` | `sha256:2cd5b45e02b14ad12bae786880bf4a175cfc8d2a2ea13d286e28384779054a93` | **sí** |
| 10 | `futbol-partidos` | `csv/futbol-partidos.csv` | 380 | 12 | `sha256:5cbc8977b6c9d4f7ae66bfcc7642c93a6655faf7b6e6524a6d40480e2e66a12e` | `sha256:5cbc8977b6c9d4f7ae66bfcc7642c93a6655faf7b6e6524a6d40480e2e66a12e` | **sí** |

**Resultado: 10/10 coinciden.** Los 10 CSV copiados son byte a byte los que declara el manifiesto: ningún fichero se alteró al copiarlo.

Totales del catálogo: **10 conjuntos**, **2530 filas** y **63 definiciones de columna** (algunas columnas comparten nombre entre conjuntos).

## Conjuntos

### 1. `ventas-mensuales` — Ventas mensuales por tienda

- **Fichero**: `datasets/csv/ventas-mensuales.csv`
- **Ruta en el manifiesto**: `datos/datasets/ventas-mensuales.csv`
- **Filas**: 180
- **Columnas**: 4
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:afa71a0b0ae0189e863247ff5a25f4ebe1836742ac7686f929d6a42565ecf7f6`
- **sha256 del fichero**: `sha256:afa71a0b0ae0189e863247ff5a25f4ebe1836742ac7686f929d6a42565ecf7f6` — coincide
- **Descripción**: Una serie de ventas diarias con estacionalidad semanal y una tendencia suave.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `fecha` | fecha | ISO 8601 |
| 2 | `tienda` | texto | — |
| 3 | `unidades` | entero | uds |
| 4 | `ingresos` | decimal | EUR |

### 2. `clientes-churn` — Clientes y baja

- **Fichero**: `datasets/csv/clientes-churn.csv`
- **Ruta en el manifiesto**: `datos/datasets/clientes-churn.csv`
- **Filas**: 200
- **Columnas**: 5
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:5290b89e3ecf746e378b01af2e73bb9e39a4297541e5ccbedae19bfc97a9839c`
- **sha256 del fichero**: `sha256:5290b89e3ecf746e378b01af2e73bb9e39a4297541e5ccbedae19bfc97a9839c` — coincide
- **Descripción**: Clientes sintéticos con antigüedad, uso mensual y si se dieron de baja.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `id_cliente` | texto | — |
| 2 | `antiguedad_meses` | entero | meses |
| 3 | `uso_mensual` | entero | sesiones |
| 4 | `reclamaciones` | entero | uds |
| 5 | `baja` | booleano | 0/1 |

### 3. `precios-accion` — Precios diarios de una acción

- **Fichero**: `datasets/csv/precios-accion.csv`
- **Ruta en el manifiesto**: `datos/datasets/precios-accion.csv`
- **Filas**: 250
- **Columnas**: 6
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:15c9d071f65b8e34061f757405bb3a74021bd4cb7d8b333364fe215038911de7`
- **sha256 del fichero**: `sha256:15c9d071f65b8e34061f757405bb3a74021bd4cb7d8b333364fe215038911de7` — coincide
- **Descripción**: Paseo aleatorio con deriva, apertura, cierre, máximo, mínimo y volumen.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `fecha` | fecha | ISO 8601 |
| 2 | `apertura` | decimal | EUR |
| 3 | `cierre` | decimal | EUR |
| 4 | `maximo` | decimal | EUR |
| 5 | `minimo` | decimal | EUR |
| 6 | `volumen` | entero | acciones |

### 4. `sensores-planta` — Sensores de planta

- **Fichero**: `datasets/csv/sensores-planta.csv`
- **Ruta en el manifiesto**: `datos/datasets/sensores-planta.csv`
- **Filas**: 240
- **Columnas**: 4
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:151ed407852ef5ae874afeb18302fa9300a58f090f1302c876422f30732617aa`
- **sha256 del fichero**: `sha256:151ed407852ef5ae874afeb18302fa9300a58f090f1302c876422f30732617aa` — coincide
- **Descripción**: Lecturas de temperatura y presión con un episodio de avería.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `hora` | entero | h desde el inicio |
| 2 | `temperatura` | decimal | °C |
| 3 | `presion` | decimal | bar |
| 4 | `estado` | texto | — |

### 5. `encuestas-satisfaccion` — Encuestas de satisfacción

- **Fichero**: `datasets/csv/encuestas-satisfaccion.csv`
- **Ruta en el manifiesto**: `datos/datasets/encuestas-satisfaccion.csv`
- **Filas**: 160
- **Columnas**: 4
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:da16c0e54b3c37555f51947ff9d605aeb07a8051495d23aa708859a12f2e63db`
- **sha256 del fichero**: `sha256:da16c0e54b3c37555f51947ff9d605aeb07a8051495d23aa708859a12f2e63db` — coincide
- **Descripción**: Puntuaciones de 0 a 10 por segmento, con una cola de insatisfechos.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `id` | texto | — |
| 2 | `segmento` | texto | — |
| 3 | `puntuacion` | entero | 0-10 |
| 4 | `recomienda` | booleano | 0/1 |

### 6. `algoritmos-tiempos` — Tiempos de algoritmos

- **Fichero**: `datasets/csv/algoritmos-tiempos.csv`
- **Ruta en el manifiesto**: `datos/datasets/algoritmos-tiempos.csv`
- **Filas**: 180
- **Columnas**: 3
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:b1965e63ca0a4987ded90cc2d71cb22167c11fa2041673de9484f5f3cdc8cbe7`
- **sha256 del fichero**: `sha256:b1965e63ca0a4987ded90cc2d71cb22167c11fa2041673de9484f5f3cdc8cbe7` — coincide
- **Descripción**: Tiempo de ejecución de seis algoritmos de ordenación con tamaños crecientes.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `algoritmo` | texto | — |
| 2 | `n` | entero | elementos |
| 3 | `milisegundos` | decimal | ms |

### 7. `telemetria-f1` — Telemetria de una carrera

- **Fichero**: `datasets/csv/telemetria-f1.csv`
- **Ruta en el manifiesto**: `datos/datasets/telemetria-f1.csv`
- **Filas**: 180
- **Columnas**: 10
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:c232e767dc95184fddeb329f6a7c4c72ccb13423a2961bea717cd464150c2c3b`
- **sha256 del fichero**: `sha256:c232e767dc95184fddeb329f6a7c4c72ccb13423a2961bea717cd464150c2c3b` — coincide
- **Descripción**: Tres carreras, dos pilotos y treinta vueltas por piloto, con compuesto, desgaste y una parada por piloto y carrera.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `carrera` | texto | — |
| 2 | `piloto` | texto | — |
| 3 | `vuelta` | entero | vueltas |
| 4 | `compuesto` | texto | — |
| 5 | `edad_neumatico` | entero | vueltas |
| 6 | `sector1_s` | decimal | s |
| 7 | `sector2_s` | decimal | s |
| 8 | `sector3_s` | decimal | s |
| 9 | `tiempo_vuelta_s` | decimal | s |
| 10 | `parada` | booleano | 0/1 |

### 8. `cartera-acciones` — Cartera de acciones frente a un indice

- **Fichero**: `datasets/csv/cartera-acciones.csv`
- **Ruta en el manifiesto**: `datos/datasets/cartera-acciones.csv`
- **Filas**: 360
- **Columnas**: 3
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:62ccc9a7355a27559024f7e4b725792d2be58a379fad4b4740a8a6fd25eacd51`
- **sha256 del fichero**: `sha256:62ccc9a7355a27559024f7e4b725792d2be58a379fad4b4740a8a6fd25eacd51` — coincide
- **Descripción**: Sesenta meses de retornos de cinco acciones y un indice, con un factor de mercado comun y ruido propio.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `mes` | fecha | ISO 8601 |
| 2 | `activo` | texto | — |
| 3 | `retorno` | decimal | tanto por uno |

### 9. `f1-clasificacion` — Clasificacion y carrera de F1

- **Fichero**: `datasets/csv/f1-clasificacion.csv`
- **Ruta en el manifiesto**: `datos/datasets/f1-clasificacion.csv`
- **Filas**: 400
- **Columnas**: 12
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:2cd5b45e02b14ad12bae786880bf4a175cfc8d2a2ea13d286e28384779054a93`
- **sha256 del fichero**: `sha256:2cd5b45e02b14ad12bae786880bf4a175cfc8d2a2ea13d286e28384779054a93` — coincide
- **Descripción**: Veinte carreras con veinte pilotos: tiempos de clasificacion, compuesto, temperatura y posicion final.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `carrera` | texto | — |
| 2 | `piloto` | texto | — |
| 3 | `equipo` | texto | — |
| 4 | `posicion_quali` | entero | puesto |
| 5 | `vuelta_quali_s` | decimal | s |
| 6 | `sector1_s` | decimal | s |
| 7 | `sector2_s` | decimal | s |
| 8 | `sector3_s` | decimal | s |
| 9 | `compuesto` | texto | — |
| 10 | `temperatura_c` | decimal | C |
| 11 | `posicion_final` | entero | puesto |
| 12 | `puntos` | entero | puntos |

### 10. `futbol-partidos` — Partidos de liga con tiros y xG

- **Fichero**: `datasets/csv/futbol-partidos.csv`
- **Ruta en el manifiesto**: `datos/datasets/futbol-partidos.csv`
- **Filas**: 380
- **Columnas**: 12
- **Licencia**: CC0-1.0
- **Origen**: sintético (generado con semilla fija)
- **Checksum del manifiesto**: `sha256:5cbc8977b6c9d4f7ae66bfcc7642c93a6655faf7b6e6524a6d40480e2e66a12e`
- **sha256 del fichero**: `sha256:5cbc8977b6c9d4f7ae66bfcc7642c93a6655faf7b6e6524a6d40480e2e66a12e` — coincide
- **Descripción**: Una liga de veinte equipos: goles, tiros, xG, posesion y tarjetas por partido.

| # | Columna | Tipo | Unidad |
|---|---|---|---|
| 1 | `jornada` | entero | jornada |
| 2 | `local` | texto | — |
| 3 | `visitante` | texto | — |
| 4 | `goles_local` | entero | goles |
| 5 | `goles_visitante` | entero | goles |
| 6 | `tiros_local` | entero | tiros |
| 7 | `tiros_visitante` | entero | tiros |
| 8 | `xg_local` | decimal | goles esperados |
| 9 | `xg_visitante` | decimal | goles esperados |
| 10 | `posesion_local` | entero | % |
| 11 | `amarillas` | entero | tarjetas |
| 12 | `resultado` | texto | 1 X 2 |

## Notas

- Los datos son **sintéticos**: no proceden de personas reales ni de fuentes de terceros. Por eso
  se pueden alojar en este repositorio con licencia CC0-1.0.
- «Columnas» cuenta las definiciones del manifiesto (nombre, tipo y unidad), no las celdas.
- El checksum cubre el fichero completo, cabecera incluida: si se regenera con la misma semilla,
  los bytes y el SHA-256 vuelven a ser los mismos.
- Para rehacer esta verificación, ver [`README.md`](README.md#cómo-se-verifica).
