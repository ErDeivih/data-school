# Verificación de los 10 datasets — carga real y contraste con el manifiesto

**Fecha**: 2026-11-04. **Alcance**: los 10 CSV de [`csv/`](csv/) perfilados uno a uno y contrastados
con [`datasets.json`](datasets.json) (filas, columnas, nombres, tipos y unidad declarada), más la
comprobación de integridad `sha256` que ya recoge [`CATALOGO.md`](CATALOGO.md).

**Resultado global: 10/10 perfiles ejecutados, 10/10 ficheros cargan, 10/10 coinciden en filas y
columnas, 63/63 definiciones de columna con nombre y tipo coherentes con el mapeo declarado, 0 celdas
vacías y 0 filas duplicadas.** Los matices (3 columnas booleanas y 1 columna de texto con inferencia
mixta) se detallan abajo: no se esconden.

## Método

1. **Perfilado.** Una ejecución de `data_profile` por fichero, con ruta relativa a esta carpeta
   (`datasets/csv/<id>.csv`). Sin `sample`: los 10 conjuntos tienen entre 160 y 400 filas, el perfil
   cubre todas las filas. De cada informe se toman: `rowCount`, `columnCount`, tipo inferido por
   columna, recuento de nulos (vía completitud), duplicados de fila completa (detección `sha256`) y
   outliers por rango intercuartílico.
2. **Contraste.** Se compara con `datasets.json` y se aplica el mapeo de tipos del manifiesto al
   vocabulario del perfilador:

   | Tipo del manifiesto | Tipo esperado en el perfil | Nota |
   |---|---|---|
   | `fecha` | `date` | ISO 8601 |
   | `texto` | `string` | — |
   | `entero` | `number` | el perfilador no distingue entero de decimal |
   | `decimal` | `number` | idem |
   | `booleano` | `number` | 0/1; el perfilador no tiene tipo booleano (ver nota 2) |

3. **Comprobaciones de apoyo** (PowerShell, solo lectura): recuento de filas de datos = líneas − 1,
   número de campos de la cabecera, BOM y fin de línea, unicidad de la clave natural de cada conjunto
   y recálculo del `sha256` de los bytes completos. Son reproducibles desde esta carpeta:

   ```powershell
   # Filas de datos y columnas de cabecera de los 10 ficheros
   Get-ChildItem csv/*.csv | ForEach-Object {
     $l = Get-Content $_.FullName; "$($_.Name): filas=$($l.Count-1) cols=$(($l[0] -split ',').Count)"
   }

   # Clave natural única por conjunto (0 duplicadas esperado)
   $v = Import-Csv csv/ventas-mensuales.csv
   ($v | ForEach-Object { "$($_.fecha)|$($_.tienda)" } | Sort-Object -Unique).Count   # 180
   ```

   Claves naturales comprobadas: `ventas-mensuales` → `(fecha, tienda)` · `clientes-churn` →
   `id_cliente` · `precios-accion` → `fecha` · `sensores-planta` → `hora` ·
   `encuestas-satisfaccion` → `id` · `algoritmos-tiempos` → `(algoritmo, n)` · `telemetria-f1` →
   `(carrera, piloto, vuelta)` · `cartera-acciones` → `(mes, activo)` · `f1-clasificacion` →
   `(carrera, piloto)` · `futbol-partidos` → `(jornada, local)`. En las 10: **0 claves repetidas**.

   Todo lo anterior está empaquetado en el comprobador [`_verificar-fichas.ps1`](_verificar-fichas.ps1),
   que además contrasta las cifras de este documento con `datasets.json`, cruza los proyectos citados
   en [`FICHAS.md`](FICHAS.md) con `../proyectos/CATALOGO.md` y valida los enlaces relativos. Devuelve
   `exit 0` solo si pasan todos, e imprime cuántos son:

   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File _verificar-fichas.ps1
   ```

4. **Integridad.** El `sha256` de los 10 ficheros se recalculó y **coincide con el `checksum` del
   manifiesto en los 10 casos** (`10/10`); la tabla con los dos hashes está en
   [`CATALOGO.md`](CATALOGO.md#verificación-de-integridad-sha256). La codificación de los 10 es UTF-8
   sin BOM y con fin de línea LF; ninguna cabecera tiene campos vacíos ni comillas.

## Tabla resumen

| # | Dataset | Filas esp./obs. | Cols. esp./obs. | Tipos coinciden | Nulos | Filas duplicadas | Veredicto |
|---|---|---|---|---|---|---|---|
| 1 | `ventas-mensuales` | 180 / 180 | 4 / 4 | sí | 0 % | 0 de 180 | correcto |
| 2 | `clientes-churn` | 200 / 200 | 5 / 5 | sí (1 booleana: nota 2) | 0 % | 0 de 200 | correcto |
| 3 | `precios-accion` | 250 / 250 | 6 / 6 | sí | 0 % | 0 de 250 | correcto |
| 4 | `sensores-planta` | 240 / 240 | 4 / 4 | sí | 0 % | 0 de 240 | correcto |
| 5 | `encuestas-satisfaccion` | 160 / 160 | 4 / 4 | sí (1 booleana: nota 2) | 0 % | 0 de 160 | correcto |
| 6 | `algoritmos-tiempos` | 180 / 180 | 3 / 3 | sí | 0 % | 0 de 180 | correcto |
| 7 | `telemetria-f1` | 180 / 180 | 10 / 10 | sí (1 booleana: nota 2) | 0 % | 0 de 180 | correcto |
| 8 | `cartera-acciones` | 360 / 360 | 3 / 3 | sí | 0 % | 0 de 360 | correcto |
| 9 | `f1-clasificacion` | 400 / 400 | 12 / 12 | sí | 0 % | 0 de 400 | correcto |
| 10 | `futbol-partidos` | 380 / 380 | 12 / 12 | sí, con 1 matiz (nota 1) | 0 % | 0 de 380 | correcto con matiz |
| — | **Total** | **2530 / 2530** | **63 / 63** | **63/63 por mapeo** | **0 %** | **0** | **10/10 cargan** |

Recuento de tipos: `fecha` 3 · `texto` 17 · `entero` 20 · `decimal` 20 · `booleano` 3 (total 63,
contado sobre las definiciones de `datasets.json`). Todos los nombres de columna coinciden uno a uno y
en el mismo orden que declara el manifiesto: no falta ni sobra ninguna.

## Desajustes y matices

**Ningún desajuste de datos.** Las cuatro observaciones siguientes no son filas perdidas ni valores
corruptos: son límites del perfilador, o estructura del conjunto que conviene tener escrita.

1. **`futbol-partidos.resultado`: el perfil lo clasifica como `mixed`, no como `string`.** La columna
   declara `texto` en el manifiesto y contiene los tres signos `1` (174 filas), `X` (114) y `2` (92).
   Como `1` y `2` también se leen como números, el perfilador marca 266 valores numéricos y 114
   textuales. Efecto visible: la puntuación de validez de ese fichero baja a **97,5 %** (4446/4560) y
   la de consistencia igual. Es un artefacto de inferencia de tipos, no un dato sucio: los recuentos
   de completitud son 4560/4560 y la columna es categórica de tres valores. Consecuencia práctica:
   al cargar el CSV hay que **forzar `resultado` a texto** o `1`/`2` acabarán como enteros y `X` como
   cadena, y cualquier agrupación partirá la categoría en dos.
2. **Las 3 columnas `booleano` se comprueban solo a medias.** `clientes-churn.baja`,
   `encuestas-satisfaccion.recomienda` y `telemetria-f1.parada` se infieren como `number` porque el
   perfilador no tiene tipo booleano. Lo que sí está verificado: contienen **exactamente dos valores
   distintos, 0 y 1**, sin nulos, así que son booleanas codificadas como entero. No pueden confirmarse
   como booleanas por etiqueta de tipo.
3. **`fichero` del manifiesto no coincide con la ruta real.** `datasets.json` apunta a
   `datos/datasets/<id>.csv` (la ruta del proyecto de origen) mientras los CSV viven en
   `datasets/csv/<id>.csv`. No es un fichero que falte: los 10 están, con el `sha256` declarado, y el
   desfase de rutas ya está explicado en [`README.md`](README.md) y
   [`CATALOGO.md`](CATALOGO.md). No se toca el manifiesto (es copia literal del origen).
4. **`ventas-mensuales` no es un panel tienda × día.** Hay **una fila por día** (180 fechas distintas,
   una por día natural de 2026-01-01 a 2026-06-29) y la tienda **rota**: `centro` 60 filas en los días
   1, 4, 7…, `norte` 60 en los días 2, 5, 8…, `sur` 60 en los días 3, 6, 9… Cada tienda cubre los
   mismos ~180 días pero solo un día de cada tres. Consecuencia: no se puede comparar una tienda con
   otra **el mismo día** (no hay día compartido); sí se puede agregar por tienda, por semana o por
   mes. Afecta a cómo se plantea `proj:P04` (sumar por filas y por columnas) y a `lab:L01`.

Otras repeticiones que son **estructura esperada, no duplicados**: `cartera-acciones` repite cada
`mes` 6 veces (6 activos × 60 meses = 360); `f1-clasificacion` repite cada `carrera` 20 veces (20
carreras × 20 pilotos = 400); `futbol-partidos` repite cada `jornada` 10 veces (38 jornadas × 10
partidos = 380); `telemetria-f1` repite cada `(carrera, piloto)` 30 veces (3 × 2 × 30 = 180). En los
10 conjuntos, la clave natural de cada apartado es única: **0 claves repetidas y 0 filas duplicadas**.

---

## Detalle por dataset

Para cada conjunto: columnas con el tipo del manifiesto, el tipo inferido y si coinciden; después,
las notas del perfil. «Outliers» son recuentos por rango intercuartílico del perfilador (`p25`/`p75`),
no errores: en varios conjuntos son justo el fenómeno que el dataset modela.

### 1. `ventas-mensuales` — Ventas mensuales por tienda

Fichero: [`csv/ventas-mensuales.csv`](csv/ventas-mensuales.csv). **180 filas × 4 columnas** (esperado
180 × 4). Todos los nulos 0 %. Clave natural `(fecha, tienda)` única: 180 de 180.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `fecha` | fecha | date | sí |
| `tienda` | texto | string | sí |
| `unidades` | entero | number | sí |
| `ingresos` | decimal | number | sí |

Notas: `fecha` 180 valores distintos (2026-01-01 a 2026-06-29); `tienda` 3 valores (60 filas cada
una). `unidades`: 49–121, mediana 80. `ingresos`: 603,31–1738,51 EUR, mediana 1074,93; **1 outlier
IQR**. Sin nulos, sin duplicados. Estructura: una fila por día con la tienda rotando (nota 4).

### 2. `clientes-churn` — Clientes y baja

Fichero: [`csv/clientes-churn.csv`](csv/clientes-churn.csv). **200 filas × 5 columnas** (esperado
200 × 5). Nulos 0 %. Clave natural `id_cliente` única: 200 de 200.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `id_cliente` | texto | string | sí |
| `antiguedad_meses` | entero | number | sí |
| `uso_mensual` | entero | number | sí |
| `reclamaciones` | entero | number | sí |
| `baja` | booleano | number | sí (0/1, nota 2) |

Notas: `antiguedad_meses` 1–48 meses; `uso_mensual` 4–42 sesiones; `reclamaciones` 0–3. `baja` toma
solo 0 y 1: **94 de 200 filas con baja (47 %)**, desbalanceo suave. Sin outliers IQR, sin nulos, sin
duplicados.

### 3. `precios-accion` — Precios diarios de una acción

Fichero: [`csv/precios-accion.csv`](csv/precios-accion.csv). **250 filas × 6 columnas** (esperado
250 × 6). Nulos 0 %. Clave natural `fecha` única: 250 de 250.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `fecha` | fecha | date | sí |
| `apertura` | decimal | number | sí |
| `cierre` | decimal | number | sí |
| `maximo` | decimal | number | sí |
| `minimo` | decimal | number | sí |
| `volumen` | entero | number | sí |

Notas: 250 fechas distintas (2026-01-01 a 2026-09-07). Precios entre 85,14 y 103,51 EUR; `volumen`
entre 502.797 y 1.492.120 acciones. Outliers IQR: **1 en `apertura`, 1 en `cierre`, 3 en `minimo`**.
Sin nulos, sin duplicados.

### 4. `sensores-planta` — Sensores de planta

Fichero: [`csv/sensores-planta.csv`](csv/sensores-planta.csv). **240 filas × 4 columnas** (esperado
240 × 4). Nulos 0 %. Clave natural `hora` única: 240 de 240.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `hora` | entero | number | sí |
| `temperatura` | decimal | number | sí |
| `presion` | decimal | number | sí |
| `estado` | texto | string | sí |

Notas: `hora` 0–239 sin huecos (240 horas). `estado` con 3 valores: `marcha` 144, `parada` 78,
`averia` 18. Outliers IQR: **18 en `temperatura` y 17 en `presion`**, coherentes con el episodio de
avería de 18 filas que describe el manifiesto: no son lecturas imposibles. Sin nulos, sin duplicados.

### 5. `encuestas-satisfaccion` — Encuestas de satisfacción

Fichero: [`csv/encuestas-satisfaccion.csv`](csv/encuestas-satisfaccion.csv). **160 filas × 4 columnas**
(esperado 160 × 4). Nulos 0 %. Clave natural `id` única: 160 de 160.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `id` | texto | string | sí |
| `segmento` | texto | string | sí |
| `puntuacion` | entero | number | sí |
| `recomienda` | booleano | number | sí (0/1, nota 2) |

Notas: `puntuacion` con 11 valores distintos, **0 a 10** (dentro del rango declarado 0-10; el perfil
no encuentra valores fuera de rango). Mediana 5, media 5,16. `segmento`: `nuevo` 54, `habitual` 53,
`veterano` 53. `recomienda`: **29 de 160 filas con 1 (18 %)**, cola de insatisfechos clara. Sin
outliers IQR, sin nulos, sin duplicados.

### 6. `algoritmos-tiempos` — Tiempos de algoritmos

Fichero: [`csv/algoritmos-tiempos.csv`](csv/algoritmos-tiempos.csv). **180 filas × 3 columnas**
(esperado 180 × 3). Nulos 0 %. Clave natural `(algoritmo, n)` única: 180 de 180.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `algoritmo` | texto | string | sí |
| `n` | entero | number | sí |
| `milisegundos` | decimal | number | sí |

Notas: 6 algoritmos (`burbuja`, `insercion`, `seleccion`, `mezcla`, `rapido`, `monticulo`), 30 filas
cada uno; 30 tamaños `n` distintos de 100 a 3000. `milisegundos` de 0,006 a 108,845: **18 outliers
IQR**, esperables porque los O(n²) se disparan y la distribución es muy asimétrica. Sin nulos, sin
duplicados.

### 7. `telemetria-f1` — Telemetria de una carrera

Fichero: [`csv/telemetria-f1.csv`](csv/telemetria-f1.csv). **180 filas × 10 columnas** (esperado
180 × 10). Nulos 0 %. Clave natural `(carrera, piloto, vuelta)` única: 180 de 180.

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `carrera` | texto | string | sí |
| `piloto` | texto | string | sí |
| `vuelta` | entero | number | sí |
| `compuesto` | texto | string | sí |
| `edad_neumatico` | entero | number | sí |
| `sector1_s` | decimal | number | sí |
| `sector2_s` | decimal | number | sí |
| `sector3_s` | decimal | number | sí |
| `tiempo_vuelta_s` | decimal | number | sí |
| `parada` | booleano | number | sí (0/1, nota 2) |

Notas: 3 carreras (`bahrein`, `monza`, `suzuka`) × 2 pilotos (`A`, `B`) × 30 vueltas = 180 filas.
`compuesto`: `medio` 120, `duro` 60. `parada` = 1 en **6 filas**: exactamente una por piloto y carrera
(vueltas 18 en A y 22 en B, en las tres carreras). Outliers IQR: **6 en cada uno de `sector1_s`,
`sector2_s`, `sector3_s` y `tiempo_vuelta_s`**, las mismas 6 vueltas con parada: son las vueltas
lentas, no errores. Sin nulos, sin duplicados.

### 8. `cartera-acciones` — Cartera de acciones frente a un indice

Fichero: [`csv/cartera-acciones.csv`](csv/cartera-acciones.csv). **360 filas × 3 columnas** (esperado
360 × 3). Nulos 0 %. Clave natural `(mes, activo)` única: 360 de 360 (panel balanceado 60 × 6).

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `mes` | fecha | date | sí |
| `activo` | texto | string | sí |
| `retorno` | decimal | number | sí |

Notas: 60 meses (2021-01-01 a 2025-12-01) × 6 activos (`accion-a` … `accion-e` + índice). `retorno`
en tanto por uno: **−0,1048 a 0,13475**, media −0,00054. Outliers IQR: **2**. `mes` se repite 6 veces
por diseño (no es duplicado). Sin nulos, sin duplicados.

### 9. `f1-clasificacion` — Clasificacion y carrera de F1

Fichero: [`csv/f1-clasificacion.csv`](csv/f1-clasificacion.csv). **400 filas × 12 columnas**
(esperado 400 × 12). Nulos 0 %. Clave natural `(carrera, piloto)` única: 400 de 400 (panel 20 × 20).

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `carrera` | texto | string | sí |
| `piloto` | texto | string | sí |
| `equipo` | texto | string | sí |
| `posicion_quali` | entero | number | sí |
| `vuelta_quali_s` | decimal | number | sí |
| `sector1_s` | decimal | number | sí |
| `sector2_s` | decimal | number | sí |
| `sector3_s` | decimal | number | sí |
| `compuesto` | texto | string | sí |
| `temperatura_c` | decimal | number | sí |
| `posicion_final` | entero | number | sí |
| `puntos` | entero | number | sí |

Notas: 20 carreras × 20 pilotos × 5 equipos (`alfa`, `beta`, `gamma`, `delta`, `epsilon`, 80 filas
por equipo). `posicion_quali` y `posicion_final`: 1–20. `vuelta_quali_s` 86,917–88,81 s.
`temperatura_c` 24–32 °C. `compuesto`: `blando` 206, `medio` 194. `puntos` 0–25. Sin outliers IQR, sin
nulos, sin duplicados.

### 10. `futbol-partidos` — Partidos de liga con tiros y xG

Fichero: [`csv/futbol-partidos.csv`](csv/futbol-partidos.csv). **380 filas × 12 columnas** (esperado
380 × 12). Nulos 0 %. Clave natural `(jornada, local)` única: 380 de 380 (38 jornadas × 10 partidos,
20 equipos).

| Columna | Tipo del manifiesto | Tipo inferido | ¿Coincide? |
|---|---|---|---|
| `jornada` | entero | number | sí |
| `local` | texto | string | sí |
| `visitante` | texto | string | sí |
| `goles_local` | entero | number | sí |
| `goles_visitante` | entero | number | sí |
| `tiros_local` | entero | number | sí |
| `tiros_visitante` | entero | number | sí |
| `xg_local` | decimal | number | sí |
| `xg_visitante` | decimal | number | sí |
| `posesion_local` | entero | number | sí |
| `amarillas` | entero | number | sí |
| `resultado` | texto | mixed | **con matiz** (nota 1) |

Notas: 38 jornadas × 10 partidos; 20 equipos como local y 20 como visitante. `goles_local` 0–3,
`goles_visitante` 0–2; `tiros_local` 2–22, `tiros_visitante` 2–16; `xg_local` 0,15–2,28,
`xg_visitante` 0,10–1,65; `posesion_local` 31–75 %; `amarillas` 0–6. `resultado`: `1` 174 filas,
`X` 114, `2` 92 — el perfil lo ve `mixed` porque `1` y `2` son numéricos y `X` no (nota 1). Sin
outliers IQR, sin nulos, sin duplicados.

---

## Qué queda cubierto y qué no

- **Cubierto**: que los 10 ficheros existen, tienen el número de filas y de columnas que declara el
  manifiesto, que los nombres y los tipos son coherentes con lo declarado (salvo los dos matices
  arriba, ambos explicados), que no hay celdas vacías ni filas repetidas, que la clave natural de cada
  conjunto es única, que la codificación es UTF-8 sin BOM y que los bytes son los que firma el
  `sha256` del manifiesto.
- **No cubierto**: la *exactitud* de los valores. Son datos sintéticos: el perfilador no puede
  compararlos con una verdad externa y así lo declara (`accuracy: undetermined`). Tampoco se valida
  que las fórmulas del generador sean las que su comentario dice; para eso está
  [`generar-datasets.mjs`](generar-datasets.mjs), que se conserva sin tocar.
- **Fichas de cada conjunto**: [`FICHAS.md`](FICHAS.md).
