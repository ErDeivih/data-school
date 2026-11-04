# Proyectos: la capa que entrena y la capa que demuestra

**Fecha:** 2026-11-02 · Complementa a `especificaciones/producto-v2/03-FUNCIONALIDADES.md` §F10
y a `RECURSOS.md` §6.

Hay dos tipos de proyecto y se confunden todo el tiempo. Los de la **capa A** viven dentro de
la academia, duran una sesión y tienen rúbrica automática: entrenan un gesto concreto. Los de
la **capa B** viven en GitHub, duran semanas y no los corrige nadie: son la prueba de que sabes
trabajar. Un portfolio lleno de capa A no impresiona a nadie; una persona que solo hace capa B
no aprende los gestos que la capa B exige.

Las dos capas de este documento están pensadas para encadenarse: cada proyecto de portfolio
declara qué micro-proyectos de la capa A lo preparan.

---

## 0. Lo que ya existe (comprobado en código)

- `sitio/proyectos.js` define **10 proyectos**: `P01`–`P04` de núcleo, `P05`–`P06` de datos,
  `P07`–`P08` de ciencia, `P09`–`P10` de quant.
- Cada proyecto declara `id`, `ruta`, `titulo`, `resumen`, `datos`, `starter`, `hitos` (3–5),
  `rubrica` (4–6 criterios con `peso` y `requiere`), `referencia`, `erronea`, `explicacionError`.
- `evaluar()` normaliza tildes, pasa a minúsculas y exige que aparezcan **todas** las piezas
  de `requiere` para dar nivel 3. `comparar()` comprueba que la rúbrica distingue la entrega
  de referencia de la errónea: si puntúan igual, la rúbrica no sirve.
- **Trampa real:** `CLASIFICACION` está indexado por id (`CLASIFICACION[p.id][0]`). Añadir un
  proyecto sin añadir su fila a `CLASIFICACION` rompe `META` en tiempo de carga. Todo alta
  necesita las dos cosas.
- Los datasets disponibles son seis: `ventas-mensuales`, `clientes-churn`, `precios-accion`,
  `sensores-planta`, `encuestas-satisfaccion`, `algoritmos-tiempos`.

### Qué NO demuestra hoy la capa A

| Hueco | Por qué importa para un data engineer |
| --- | --- |
| No hay ningún proyecto de ingesta incremental con eventos tardíos | Es el 80 % del trabajo real: llega tarde, llega dos veces, llega mal |
| No hay modelado dimensional a partir de un grano de pedido | Sin grano no hay tabla de hechos, y sin tabla de hechos no hay almacén |
| No hay idempotencia de un pipeline | Reejecutar sin duplicar es la primera pregunta de una entrevista técnica |
| No hay coste ni presupuesto de latencia | Un pipeline que funciona pero cuesta el triple no se despliega |
| No hay opciones ni griegas | La ruta quant se queda en trading direccional |

---

## 0. Lo que ya está dentro (2026-11-02)

**PF-01 completo:** `proyectos/pf-01-pulso-poblacion/` ingiere población y PIB per cápita de cinco
países (2000-2023) del Banco Mundial, guarda el bruto, construye un modelo en estrella con dbt
(`models/` + `schema.yml`) ejecutado con DuckDB, pasa 7 pruebas de modelo y 11 de ingesta, y
genera `panel.html` con dos gráficos y una tabla. Falta solo orquestación.

**P17 con datos reales:** `proyectos/pf-02-openf1/` descarga tres carreras de 2024 de OpenF1
(gratis, sin clave), guarda el bruto y deja 3.029 vueltas únicas con clave de idempotencia
(sesión, piloto, vuelta) y 8 comprobaciones en verde. Falta cruzar stints y orquestar.

Seis proyectos nuevos implementados en `sitio/proyectos.js`, con sus dos datasets y sus pruebas
en verde. Se abren en el portal con `#/proyectos/P11` y siguientes.

| Id | Ruta | Proyecto | Dataset |
| --- | --- | --- | --- |
| P11 | datos | Limpiar y unir la telemetría de una carrera | `telemetria-f1` |
| P12 | datos | Un panel de carrera con una sola pregunta | `telemetria-f1` |
| P13 | ciencia | ¿Le costó la carrera la parada? | `telemetria-f1` |
| P14 | quant | El riesgo de una cartera, medido | `cartera-acciones` |
| P15 | quant | ¿Batir al índice o asumir más riesgo? | `cartera-acciones` |
| P16 | ciencia | Un memo de inversión con supuestos y sensibilidad | `cartera-acciones` |
| P17 | datos | Del API de F1 a un lago, sin romper nada | `f1-clasificacion` |
| P18 | ciencia | Predecir la clasificación sin mirar la carrera | `f1-clasificacion` |
| P19 | ciencia | ¿Merece la pena el undercut? | `f1-clasificacion` |
| P20 | datos | Fútbol: ingesta y modelo en estrella | `futbol-partidos` |
| P21 | ciencia | Fútbol: el xG no es el marcador | `futbol-partidos` |
| P22 | ciencia | Finanzas desde cero: interés, inflación y riesgo | `cartera-acciones` |

Los cuatro datasets son sintéticos y deterministas, con manifiesto y checksum: 180 filas de telemetría (3 carreras, 2 pilotos, 30 vueltas cada uno, una parada por piloto) 360 filas de cartera (5 acciones y un índice, 60 meses), 400 de clasificación de F1 (20 carreras por 20 pilotos) y 380 partidos de fútbol con tiros y xG.

Para datos de F1 reales, la fuente es la API de [OpenF1](https://openf1.org/) y la librería
[FastF1](https://docs.fastf1.dev/): sirven para PF con datos verdaderos, pero cambian y tienen límite
de peticiones, así que los proyectos de la app usan el paquete sintético y el real se reserva para el
portfolio.

**Siguiente tanda propuesta:** los ocho micro-proyectos de §1 siguen siendo válidos, pero ahora
mismo valen más los seis de portfolio de §2.

## 1. Capa A — micro-proyectos (P11–P18): seis ya implementados, dos propuestos

Cada uno se pega en `sitio/proyectos.js` dentro de `PROYECTOS`, y su fila en `CLASIFICACION`.
Los textos de `referencia` y `erronea` están escritos para que la rúbrica **distinga**: la
referencia contiene todas las piezas de `requiere`, la errónea casi ninguna.

### Datasets que hay que añadir antes (3)

```text
pedidos-clientes   id_pedido, id_cliente, fecha_pedido, ciudad, importe, estado, canal
                   (600 filas, 40 clientes, 18 meses; incluye 12 pedidos duplicados por id_pedido
                    y 8 importes negativos de devoluciones que NO son errores)

eventos-pipeline   evento_id, pedido_id, tipo, ocurrido_en, recibido_en, importe
                   (2.000 eventos, 6 % con recibido_en > ocurrido_en + 2 h,
                    3 % repetidos con el mismo evento_id, 1 % sin pedido_id)

opciones-sinteticas fecha, subyacente, spot, strike, vencimiento, tipo, prima, delta, gamma, vega
                   (Black-Scholes con vol fija 0,25 y tipos 0,03; 4 vencimientos, 3 strikes)
```

Los tres son sintéticos y deterministas, como manda `datos/generar-datasets.mjs`. Ninguno lleva
datos personales. Se documentan en el manifest con su recuento de duplicados y ausencias
**esperadas**, porque medio ejercicio consiste en saber que están.

### `P11` · Ingesta incremental que no pierde eventos (datos)

```js
{
  id: "P11", ruta: "datos",
  titulo: "Cargar eventos tardíos sin perder ni duplicar",
  resumen: "Procesar un lote de eventos con retrasos y repetidos, y dejar una tabla donde cada evento aparece una sola vez.",
  datos: "eventos-pipeline",
  starter: "# Ingesta incremental\n\n## Regla de negocio\n\n## Deduplicación\n\n## Tardíos\n\n## Resultado\n",
  hitos: [
    { id: "H1", titulo: "Definir la clave del evento", criterio: "dice qué columna identifica un evento único y por qué" },
    { id: "H2", titulo: "Decidir qué es tarde", criterio: "fija un umbral de latencia en horas con un motivo" },
    { id: "H3", titulo: "Deduplicar sin perder el último estado", criterio: "conserva el registro con recibido_en más reciente" },
    { id: "H4", titulo: "Medir el descarte", criterio: "da el número de eventos descartados y su motivo" },
  ],
  rubrica: [
    { id: "R1", criterio: "nombra la clave de evento", peso: 2, requiere: ["evento_id"] },
    { id: "R2", criterio: "fija un umbral de latencia justificado", peso: 3, requiere: ["umbral", "horas"] },
    { id: "R3", criterio: "deduplica quedándose con el más reciente", peso: 3, requiere: ["recibido_en", "reciente"] },
    { id: "R4", criterio: "cuantifica lo descartado y por qué", peso: 2, requiere: ["descartad", "motivo"] },
  ],
  referencia: "# Ingesta incremental\n\n## Regla de negocio\nLa clave es evento_id, porque un pedido puede generar varios eventos.\n\n## Deduplicación\nOrdeno por recibido_en y me quedo con el último por evento_id: 60 repetidos menos.\n\n## Tardíos\nUn umbral de 2 horas separa el retraso normal del reintento: 120 eventos llegaron tarde.\n\n## Resultado\nQuedan 1.880 eventos, 120 tardíos aceptados y 60 duplicados descartados por ser el registro viejo del mismo evento_id.\n",
  erronea: "# Ingesta\n\nHe cargado el CSV y he quitado los repetidos con drop_duplicates. Ya está.\n",
  explicacionError: "No dice cuál es la clave ni con qué criterio se queda un registro: quitar duplicados sin definir qué es duplicado puede borrar el evento bueno y conservar el viejo.",
}
```

### `P12` · Tabla de hechos y dimensiones desde pedidos (datos)

```js
{
  id: "P12", ruta: "datos",
  titulo: "Modelar pedidos en estrella sin romper el grano",
  resumen: "Convertir una tabla plana de pedidos en un hecho por pedido y sus dimensiones, declarando el grano antes de escribir SQL.",
  datos: "pedidos-clientes",
  starter: "# Modelo en estrella\n\n## Grano\n\n## Dimensiones\n\n## Hecho\n\n## Comprobación\n",
  hitos: [
    { id: "H1", titulo: "Declarar el grano", criterio: "dice qué representa una fila del hecho, en una frase" },
    { id: "H2", titulo: "Separar dimensiones", criterio: "identifica cliente, fecha y canal como dimensiones" },
    { id: "H3", titulo: "Tratar devoluciones", criterio: "explica por qué un importe negativo no se descarta" },
    { id: "H4", titulo: "Comprobar que cuadra", criterio: "compara la suma del hecho con la suma del origen" },
  ],
  rubrica: [
    { id: "R1", criterio: "declara el grano por pedido", peso: 3, requiere: ["grano", "pedido"] },
    { id: "R2", criterio: "nombra las dimensiones", peso: 2, requiere: ["dimension", "cliente"] },
    { id: "R3", criterio: "justifica conservar los negativos", peso: 2, requiere: ["devoluc", "negativ"] },
    { id: "R4", criterio: "cuadra el total contra el origen", peso: 3, requiere: ["cuadra", "suma"] },
  ],
  referencia: "# Modelo en estrella\n\n## Grano\nUna fila del hecho es un pedido, identificado por id_pedido.\n\n## Dimensiones\ndim_cliente por id_cliente, dim_fecha por fecha_pedido y dim_canal por canal.\n\n## Hecho\nfact_pedidos con importe, estado y las claves de las tres dimensiones.\n\n## Comprobación\nLa suma del hecho cuadra con la suma del origen salvo 12 duplicados, que se colapsan: 240.318 frente a 240.318.\n\n## Devoluciones\nLos 8 importes negativos son devoluciones, no errores: quitarlos eliminaría ventas reales y la suma dejaría de cuadrar.\n",
  erronea: "# Modelo\n\nHe hecho una tabla con todo y he borrado los negativos porque un importe no puede ser negativo.\n",
  explicacionError: "No declara grano, confunde una devolución con un error y rompe el cuadre: el modelo no se puede auditar.",
}
```

### `P13` · Controles que distinguen nulo de cero (datos)

```js
{
  id: "P13", ruta: "datos",
  titulo: "Controles de calidad que no confunden nulo con cero",
  resumen: "Diseñar comprobaciones sobre sensores que fallen cuando deben y que no salten por un cero legítimo.",
  datos: "sensores-planta",
  starter: "# Controles\n\n## Qué es un fallo\n\n## Controles\n\n## Falsos positivos\n\n## Resultado\n",
  hitos: [
    { id: "H1", titulo: "Separar nulo de cero", criterio: "explica qué significa cada uno en un sensor" },
    { id: "H2", titulo: "Escribir tres controles", criterio: "incluye rango, nulos y monotonía del instante" },
    { id: "H3", titulo: "Provocar un fallo a propósito", criterio: "mete un valor imposible y comprueba que salta" },
    { id: "H4", titulo: "Contar falsos positivos", criterio: "da cuántas filas buenas marcó el control" },
  ],
  rubrica: [
    { id: "R1", criterio: "distingue nulo de cero", peso: 3, requiere: ["nulo", "cero"] },
    { id: "R2", criterio: "define controles con umbral", peso: 3, requiere: ["control", "rango"] },
    { id: "R3", criterio: "demuestra que el control falla cuando debe", peso: 3, requiere: ["provoc", "salta"] },
    { id: "R4", criterio: "mide falsos positivos", peso: 2, requiere: ["falso", "positivo"] },
  ],
  referencia: "# Controles\n\n## Qué es un fallo\nUn nulo en temperatura es una lectura perdida; un cero es una lectura de 0 grados y puede ser real.\n\n## Controles\nRango de temperatura entre -10 y 60, nulos en presion por encima del 2 %, y hora estrictamente creciente.\n\n## Prueba\nMeto temperatura 999 en una fila y el control de rango salta: la prueba provocada demuestra que el control no es decorativo.\n\n## Resultado\nNingún falso positivo en 500 filas; 11 nulos reales marcados y 2 ceros conservados.\n",
  erronea: "# Controles\n\nHe mirado los datos y están bien. He puesto un control que avisa si hay nulos.\n",
  explicacionError: "No define qué es un fallo, no demuestra que el control salta y no distingue un cero legítimo de una lectura perdida.",
}
```

### `P14` · Umbral elegido por coste, no por F1 (ciencia)

```js
{
  id: "P14", ruta: "ciencia",
  titulo: "Elegir el umbral por el coste de equivocarse",
  resumen: "Fijar el punto de corte de un clasificador a partir de lo que cuesta un falso positivo y un falso negativo.",
  datos: "clientes-churn",
  starter: "# Umbral\n\n## Costes\n\n## Barrido\n\n## Decisión\n\n## Límite\n",
  hitos: [
    { id: "H1", titulo: "Poner precio a cada error", criterio: "asigna un coste a falso positivo y a falso negativo" },
    { id: "H2", titulo: "Barrer umbrales", criterio: "prueba al menos cinco cortes y anota el coste total" },
    { id: "H3", titulo: "Elegir y justificar", criterio: "elige el corte de coste mínimo y lo explica" },
    { id: "H4", titulo: "Declarar el límite", criterio: "dice qué cambiaría si el coste estuviera mal estimado" },
  ],
  rubrica: [
    { id: "R1", criterio: "asigna coste a los dos errores", peso: 3, requiere: ["coste", "falso"] },
    { id: "R2", criterio: "barre varios umbrales con su coste", peso: 3, requiere: ["umbral", "barrido"] },
    { id: "R3", criterio: "elige el mínimo y lo justifica", peso: 3, requiere: ["minimo", "justific"] },
    { id: "R4", criterio: "declara la sensibilidad al coste", peso: 2, requiere: ["sensibilidad", "coste"] },
  ],
  referencia: "# Umbral\n\n## Costes\nUn falso negativo cuesta 120 euros de cliente perdido; un falso positivo, 15 euros de llamada.\n\n## Barrido\nPruebo cortes de 0,2 a 0,8: el coste total baja hasta 0,35 y vuelve a subir.\n\n## Decisión\nElijo 0,35 porque es el minimo de coste, no el máximo de exactitud.\n\n## Límite\nLa sensibilidad al coste es alta: si el falso negativo costara 40 en vez de 120, el corte óptimo se movería a 0,5.\n",
  erronea: "# Umbral\n\nUso 0,5 porque es el que viene por defecto y da buena accuracy.\n",
  explicacionError: "El umbral por defecto no tiene en cuenta el coste asimétrico de los errores, que es justo el problema del proyecto.",
}
```

### `P15` · Diagnóstico de fuga temporal (ciencia)

```js
{
  id: "P15", ruta: "ciencia",
  titulo: "Encontrar la fuga que hace perfecto al modelo",
  resumen: "Partir una serie con corte temporal, detectar por qué una métrica sospechosamente buena es una fuga y corregirla.",
  datos: "precios-accion",
  starter: "# Fuga temporal\n\n## Corte\n\n## Métrica sospechosa\n\n## Causa\n\n## Corrección\n",
  hitos: [
    { id: "H1", titulo: "Cortar por fecha", criterio: "usa un corte temporal, no aleatorio" },
    { id: "H2", titulo: "Detectar la sospecha", criterio: "identifica una métrica demasiado buena y lo dice" },
    { id: "H3", titulo: "Encontrar la causa", criterio: "nombra la variable que contiene el futuro" },
    { id: "H4", titulo: "Corregir y volver a medir", criterio: "da la métrica antes y después de quitar la variable" },
  ],
  rubrica: [
    { id: "R1", criterio: "corta por fecha", peso: 2, requiere: ["corte", "fecha"] },
    { id: "R2", criterio: "sospecha de la métrica perfecta", peso: 2, requiere: ["sospech", "metric"] },
    { id: "R3", criterio: "identifica la variable con futuro", peso: 3, requiere: ["futuro", "variable"] },
    { id: "R4", criterio: "compara antes y después", peso: 3, requiere: ["antes", "despues"] },
  ],
  referencia: "# Fuga temporal\n\n## Corte\nEntreno hasta 2023-12-31 y pruebo desde 2024-01-01, sin barajar.\n\n## Métrica sospechosa\nEl R2 sale 0,99 y eso no pasa con precios: sospecho de una variable que mira al futuro.\n\n## Causa\nLa variable cierre_manana usa el cierre del día siguiente; es la causa de la fuga.\n\n## Corrección\nAl quitar esa variable el R2 cae de 0,99 a 0,04 antes y despues del cambio, que es lo normal en una serie de precios.\n",
  erronea: "# Modelo\n\nHe entrenado y sale un R2 de 0,99, así que el modelo es buenísimo.\n",
  explicacionError: "Un R2 de 0,99 en precios diarios es la señal de alarma, no el resultado: falta comprobar qué variable contiene el futuro.",
}
```

### `P16` · Cobertura delta-gamma con álgebra (quant)

```js
{
  id: "P16", ruta: "quant",
  titulo: "Cubrir una cartera de opciones con álgebra",
  resumen: "Calcular la exposición de una cartera en griegas y resolver los pesos de cobertura con un sistema lineal, comprobando que la delta final queda a cero.",
  datos: "opciones-sinteticas",
  starter: "# Cobertura\n\n## Exposición\n\n## Sistema\n\n## Pesos\n\n## Comprobación\n",
  hitos: [
    { id: "H1", titulo: "Sumar la exposición", criterio: "calcula la exposición total en gamma y vega" },
    { id: "H2", titulo: "Plantear el sistema", criterio: "escribe la matriz de griegas y el vector objetivo" },
    { id: "H3", titulo: "Resolver los pesos", criterio: "invierte la matriz y da los pesos de cada opción" },
    { id: "H4", titulo: "Comprobar la delta", criterio: "calcula la delta residual y muestra que queda cerca de cero" },
  ],
  rubrica: [
    { id: "R1", criterio: "calcula la exposición total", peso: 2, requiere: ["exposicion", "gamma"] },
    { id: "R2", criterio: "plantea matriz y objetivo", peso: 3, requiere: ["matriz", "objetivo"] },
    { id: "R3", criterio: "resuelve e informa los pesos", peso: 3, requiere: ["pesos", "inversa"] },
    { id: "R4", criterio: "verifica la delta residual", peso: 3, requiere: ["residual", "cero"] },
  ],
  referencia: "# Cobertura\n\n## Exposición\nCorto 1.000 calls: gamma total -523,88 y vega total -815,54.\n\n## Sistema\nLa matriz de griegas G tiene en columnas gamma y vega de cada call de cobertura, y el objetivo es el negativo de mi exposición.\n\n## Pesos\nResuelvo con la inversa: 146 contratos de la call A y 62 de la call B.\n\n## Comprobación\nLa delta residual queda en 0,4 acciones, es decir practicamente cero frente al tamaño de la posición.\n",
  erronea: "# Cobertura\n\nCompro 100 calls para cubrirme y ya está, la delta se queda más o menos bien.\n",
  explicacionError: "Sin plantear el sistema no se sabe qué exposición queda: cubrir gamma y vega a ojo deja una delta residual que nadie ha medido.",
}
```

### `P17` · Idempotencia de un proceso de carga (datos)

```js
{
  id: "P17", ruta: "datos",
  titulo: "Reejecutar sin duplicar",
  resumen: "Hacer que un proceso de carga se pueda relanzar tres veces seguidas y deje exactamente las mismas filas.",
  datos: "eventos-pipeline",
  starter: "# Idempotencia\n\n## Clave\n\n## Estrategia\n\n## Prueba\n\n## Resultado\n",
  hitos: [
    { id: "H1", titulo: "Elegir la clave de idempotencia", criterio: "dice qué combinación de columnas identifica una carga" },
    { id: "H2", titulo: "Elegir la estrategia", criterio: "escoge entre upsert, borrar-y-reinsertar o partición, y lo motiva" },
    { id: "H3", titulo: "Probar tres ejecuciones", criterio: "lanza el proceso tres veces y cuenta las filas" },
    { id: "H4", titulo: "Probar el caso del reintento parcial", criterio: "corta la ejecución a la mitad y comprueba que no deja basura" },
  ],
  rubrica: [
    { id: "R1", criterio: "define la clave de idempotencia", peso: 3, requiere: ["clave", "idempotencia"] },
    { id: "R2", criterio: "justifica la estrategia elegida", peso: 2, requiere: ["estrategia", "upsert"] },
    { id: "R3", criterio: "demuestra el mismo resultado en tres ejecuciones", peso: 3, requiere: ["tres", "mismas"] },
    { id: "R4", criterio: "cubre el fallo a mitad de carga", peso: 3, requiere: ["mitad", "basura"] },
  ],
  referencia: "# Idempotencia\n\n## Clave\nLa clave de idempotencia es evento_id: dos cargas del mismo fichero traen los mismos ids.\n\n## Estrategia\nUso upsert por evento_id en vez de borrar y reinsertar: no pierdo el histórico si falla a mitad.\n\n## Prueba\nLanzo el proceso tres veces seguidas y quedan 1.880 filas las tres veces, las mismas.\n\n## Reintento parcial\nCorto la ejecución a la mitad y no queda basura: la transacción revierte y la tabla sigue en 1.880.\n",
  erronea: "# Carga\n\nCada vez que ejecuto borro la tabla y la vuelvo a llenar, así nunca hay duplicados.\n",
  explicacionError: "Borrar y reinsertar deja la tabla vacía si el proceso falla entre el borrado y la carga, y no responde a por qué dos ejecuciones darían lo mismo.",
}
```

### `P18` · Presupuesto de latencia y degradación (núcleo)

```js
{
  id: "P18", ruta: "nucleo",
  titulo: "Servir una consulta con presupuesto de latencia",
  resumen: "Medir cuánto tarda una consulta de un panel con datos crecientes, fijar un presupuesto y decidir qué se degrada cuando se supera.",
  datos: "pedidos-clientes",
  starter: "# Latencia\n\n## Medición\n\n## Presupuesto\n\n## Degradación\n\n## Resultado\n",
  hitos: [
    { id: "H1", titulo: "Medir con tamaños crecientes", criterio: "da tiempos para al menos tres tamaños" },
    { id: "H2", titulo: "Fijar el presupuesto", criterio: "declara un objetivo en milisegundos y de dónde sale" },
    { id: "H3", titulo: "Elegir qué degradar", criterio: "decide entre caché, límite de filas o preagregado, y lo motiva" },
    { id: "H4", titulo: "Comprobar la mejora", criterio: "compara el tiempo antes y después de la medida" },
  ],
  rubrica: [
    { id: "R1", criterio: "mide en varios tamaños", peso: 2, requiere: ["milisegundos", "tamanos"] },
    { id: "R2", criterio: "fija un presupuesto justificado", peso: 3, requiere: ["presupuesto", "objetivo"] },
    { id: "R3", criterio: "elige una degradación con motivo", peso: 3, requiere: ["degradacion", "cache"] },
    { id: "R4", criterio: "compara antes y después", peso: 3, requiere: ["antes", "despues"] },
  ],
  referencia: "# Latencia\n\n## Medición\nCon 10.000, 100.000 y 1.000.000 de filas la consulta tarda 40, 380 y 3.900 milisegundos.\n\n## Presupuesto\nEl objetivo es 300 milisegundos porque es el umbral en el que una persona deja de esperar una pantalla.\n\n## Degradación\nElijo cache de la agregación diaria: el limite de filas cambiaría la respuesta y el preagregado tarda en construirse.\n\n## Resultado\nTras la cache, la misma consulta tarda 22 milisegundos antes y despues de calentarla, un 94 % menos.\n",
  erronea: "# Latencia\n\nLa consulta va lenta, así que le pongo un limit 100 y ya carga rápido.\n",
  explicacionError: "Cambiar la respuesta no es optimizar: sin medir ni fijar presupuesto no se sabe si el limit oculta el problema o lo resuelve.",
}
```

**Fila obligatoria en `CLASIFICACION` para cada alta:**

```js
P11: [["de"], "intermedio"],   P12: [["de"], "intermedio"],
P13: [["de"], "intermedio"],   P14: [["ds"], "intermedio"],
P15: [["ds"], "avanzado"],     P16: [["quant"], "avanzado"],
P17: [["de"], "avanzado"],     P18: [["core", "alg"], "intermedio"],
```

**Criterio de cierre de la capa A:** `node _comprobar-proyectos-t35.mjs` y sus hermanos
`t36`–`t38` en verde, `comparar()` devolviendo `distingue: true` en los ocho, y la pantalla de
proyectos mostrando los 18 con su ruta y nivel.

---

## 2. Capa B — seis proyectos de portfolio, en orden de dificultad

Reglas comunes, porque son las que hacen que un repositorio se lea:

- **Un repositorio por proyecto.** Nada de una carpeta `proyectos/` con seis cuadernos sueltos.
- **README con ocho secciones fijas:** problema, pregunta que responde, datos y licencia,
  arquitectura (diagrama), cómo se ejecuta desde cero, decisiones y alternativas descartadas,
  qué falló y qué aprendiste, límites. Sin esto, el proyecto no existe para quien lo lee.
- **Se ejecuta con un comando.** `make up` o `docker compose up`. Si hay que adivinar, está a medias.
- **Pruebas de lo importante**, no del 100 %: la transformación, el contrato de datos y el caso raro.
- **Evidencia versionada:** captura del panel, salida de los tests, tiempo de ejecución.
- **Nada de datos personales ni claves.** Los `.env` van en `.env.example`.

### PF-01 · El pulso de tu ciudad (3 semanas · dificultad 2/5)

| | |
| --- | --- |
| Pregunta | ¿Qué tan frescos son los datos abiertos de mi ciudad y qué se puede responder con ellos? |
| Datos | AEMET (temperatura y precipitación por municipio), calidad del aire o GTFS de transporte. Todos con API o descarga abierta |
| Stack mínimo | Python + `httpx`, Parquet, DuckDB o PostgreSQL, dbt, Dagster o Airflow, Metabase |
| Arquitectura | API → bruto inmutable (`raw/fecha=…`) → normalizado → dbt (staging → marts) → panel |
| Fases que ejercita | F03, F04 (`ingesta-incremental-y-cdc`, `orquestacion-y-dag`, `dbt-y-transformacion`, `calidad-de-datos`), F12 |

**Hitos**

1. Ingesta que se pueda relanzar: guarda la respuesta cruda con su fecha y su `etag`; si no
   cambió, no vuelve a pedirla.
2. Modelo con un grano declarado por escrito (una fila = una estación y una hora).
3. Tres pruebas de datos: rango físico, unicidad de la clave, y frescura menor de 24 h.
4. Panel con dos preguntas y una nota al pie que diga de cuándo son los datos.
5. Informe de una página: qué se puede concluir y qué no.

**Criterio de aceptación**

- Dos ejecuciones seguidas dejan el mismo número de filas.
- El panel avisa visiblemente cuando los datos tienen más de 24 h.
- Existe una prueba que falla si se duplica una lectura.

**Defensa en entrevista**

- *«¿Cómo sabes que tu ingesta no pierde datos?»* → contar la clave, el recuento esperado y la
  prueba de frescura. No decir «porque funciona».
- *«¿Por qué Parquet y no CSV?»* → tipos, compresión por columna y que el fichero es inmutable.
- *«¿Qué harías si la API cambia de esquema?»* → validación de contrato en la ingesta, cuarentena
  de lo que no valida, y alerta.

**Preparado por:** `P11`, `P13`, `P18`.

---

### PF-02 · El almacén de una empresa que ya existe (4 semanas · dificultad 3/5)

| | |
| --- | --- |
| Pregunta | ¿Puede alguien de negocio responder sus preguntas sin pedirme SQL? |
| Datos | Un dataset público con grano de pedido o de transacción (ventas, alquiler de bicis, reservas). Si no existe, sintético documentado |
| Stack mínimo | PostgreSQL, dbt, tests de dbt, capa semántica (dbt metrics o MetricFlow), Metabase o Superset |
| Arquitectura | Origen → staging → intermedios → `dim_*` + `fact_*` → métricas → panel |
| Fases que ejercita | F04 (`modelado-dimensional`, `esquema-estrella-y-copo`, `scd-dimensiones-cambiantes`, `contratos-de-datos`, `capa-semantica-y-metricas`), F12 |

**Hitos**

1. Diccionario de datos escrito **antes** del SQL: grano, claves, tipos y qué significa cada métrica.
2. `dim_cliente` con SCD tipo 2 y una prueba que detecte dos versiones abiertas a la vez.
3. `fact_pedidos` que cuadre con el origen, y una consulta de reconciliación en el README.
4. Tres métricas en la capa semántica, con su definición y su margen de error.
5. Panel con una sola pantalla y un enlace a la definición de cada métrica.

**Criterio de aceptación**

- `dbt test` en verde y al menos una prueba propia por cada dimensión.
- La suma del hecho cuadra con el origen, y el descuadre está explicado (duplicados colapsados).
- Cualquier métrica del panel se puede rastrear hasta una tabla y una fórmula.

**Defensa en entrevista**

- *«¿Por qué estrella y no copo de nieve?»* → número de joins, legibilidad para negocio y coste
  de mantener dimensiones normalizadas que nadie consulta.
- *«Enséñame una decisión difícil.»* → SCD2 frente a sobrescribir: qué se pierde y por qué se eligió.

**Preparado por:** `P12`, `P14`.

---

### PF-03 · Eventos que llegan tarde (4 semanas · dificultad 4/5)

| | |
| --- | --- |
| Pregunta | ¿Cuánto se desvía un panel en tiempo real de la verdad que da el proceso por lotes? |
| Datos | Generador propio de eventos con retrasos, duplicados y huecos (documentado y con semilla) |
| Stack mínimo | Redpanda o Kafka, Python, Spark Structured Streaming o Polars con micro-lotes, Parquet/Iceberg, DuckDB |
| Arquitectura | Productor → cola → consumidor idempotente con watermark → tabla → comparación con lote |
| Fases que ejercita | F04 (`kafka-y-colas`, `streaming-tiempo-real`, `algoritmos-de-streaming`, `idempotencia-y-reintentos`, `lakehouse-y-table-formats`) |

**Hitos**

1. Productor que pueda inyectar un 5 % de eventos con 3 h de retraso a voluntad.
2. Consumidor idempotente: matar el proceso a mitad y relanzarlo no duplica.
3. Watermark explícito, y una decisión escrita sobre qué se hace con lo que llega después.
4. Tabla de reconciliación: lote frente a streaming, con la diferencia en unidades y en euros.
5. Panel con la diferencia y una alerta cuando supera el umbral.

**Criterio de aceptación**

- Tres caídas simuladas del consumidor y ninguna fila duplicada.
- La diferencia lote-streaming está cuantificada, no «es pequeña».
- El README explica qué se pierde al elegir el watermark.

**Defensa en entrevista**

- *«¿Exactly-once o at-least-once?»* → qué garantiza cada uno, qué cuesta, y por qué la
  idempotencia del consumidor es lo que de verdad salva el resultado.
- *«¿Qué pasa con un evento que llega dos días tarde?»* → política, dead letter, reproceso.

**Preparado por:** `P11`, `P17`.

---

### PF-04 · Cambios que llegan sin avisar (4 semanas · dificultad 4/5)

| | |
| --- | --- |
| Pregunta | ¿Cómo mantengo el almacén sincronizado con la base de datos de producción sin volver a copiarla entera cada noche? |
| Datos | PostgreSQL propio con carga continua (script que inserta, actualiza y borra) |
| Stack mínimo | PostgreSQL (WAL lógico), Debezium o `pgoutput`, Parquet, dbt, un reconciliador en Python |
| Arquitectura | Postgres → CDC → bruto → dbt (SCD2 + borrados lógicos) → reconciliación |
| Fases que ejercita | F04 (`ingesta-incremental-y-cdc`, `evolucion-de-esquema`, `scd-dimensiones-cambiantes`, `reconciliacion-y-pruebas`, `backfill-y-reproceso`) |

**Hitos**

1. Replicación lógica activa y un evento de `INSERT`, `UPDATE` y `DELETE` capturado y visible.
2. SCD2 generado desde el CDC, con `valid_from`, `valid_to` y `es_actual`.
3. Reconciliación automática: recuento y suma por tabla comparados con origen, tolerancia cero.
4. Un `backfill` de 24 h que no duplique ni pierda.
5. Informe del desfase medido en segundos, con percentiles.

**Criterio de aceptación**

- Borrar una fila en origen se refleja en el almacén y en el panel en menos de 60 s.
- La reconciliación falla a propósito cuando se inyecta una divergencia.
- El README explica qué pasa si el conector se para una hora.

**Defensa en entrevista**

- *«¿Por qué CDC y no una consulta cada 15 minutos?»* → coste, borrados y la carrera con las
  actualizaciones.
- *«¿Cómo gestionas un cambio de columna en origen?»* → `evolucion-de-esquema`, contrato y
  compatibilidad.

**Preparado por:** `P12`, `P17`.

---

### PF-05 · Un servicio de datos con SLA (3 semanas · dificultad 4/5)

| | |
| --- | --- |
| Pregunta | ¿Puede otra persona usar mis datos por HTTP sin leer mi código? |
| Datos | Cualquiera de los almacenes anteriores, servido por API |
| Stack mínimo | FastAPI, Redis, PostgreSQL, Docker, `k6` o `locust`, Prometheus + Grafana (o logs estructurados) |
| Arquitectura | Cliente → API (auth por clave, paginación, caché, límite) → almacén → métricas |
| Fases que ejercita | F11 (`fastapi`, `idempotencia-en-apis`, `autenticacion-y-autorizacion`, `resiliencia-de-servicios`, `incidentes-y-postmortem`, `ci-cd`) |

**Hitos**

1. OpenAPI publicado y un `curl` de ejemplo que funciona copiado tal cual.
2. Paginación por cursor, no por `offset`; explicado en el README.
3. `POST` idempotente con cabecera de clave; dos envíos iguales devuelven el mismo recurso.
4. Prueba de carga con percentiles p50/p95/p99 y un SLO declarado (por ejemplo p95 < 300 ms).
5. Un postmortem simulado: qué se rompió, cómo se detectó, qué se cambió.

**Criterio de aceptación**

- La prueba de carga genera un informe reproducible con el comando en el README.
- Cuando se supera el límite, la API responde 429 con `Retry-After`, no 500.
- Existe una prueba que verifica la idempotencia.

**Defensa en entrevista**

- *«¿Qué pasa si Redis se cae?»* → degradación a base de datos, qué se pierde y qué no.
- *«¿Cómo sabes que el SLO se cumple?»* → percentil, ventana y la fuente de la métrica.

**Preparado por:** `P17`, `P18`.

---

### PF-06 · Un backtest que sobrevive a la revisión (4 semanas · dificultad 5/5)

| | |
| --- | --- |
| Pregunta | ¿Cuánto de mi resultado es estrategia y cuánto es haber probado veinte ideas? |
| Datos | Precios diarios ajustados por acciones corporativas (o `opciones-sinteticas` para la parte de griegas) |
| Stack mínimo | Python, pandas/Polars, `vectorbt` o motor propio, DuckDB para el almacén de pruebas |
| Arquitectura | Bruto → ajuste → señales → carteras → validación (purga + embargo) → métricas con deflación |
| Fases que ejercita | F09 (`retornos-logaritmicos`, `purged-kfold`, `data-snooping-y-multiple-testing`, `sharpe-deflactado`, `sesgo-de-supervivencia`, `slippage-y-comisiones`), F02 |

**Hitos**

1. Serie ajustada por split y dividendo, con la figura que muestra qué cambia el ajuste.
2. Backtest con costes explícitos: comisión, `slippage` y capacidad declarada.
3. Validación con purga y embargo; y una segunda validación combinatoria si hay tiempo.
4. Sharpe deflactado por el número de pruebas, y la cuenta de cuántas ideas se probaron.
5. Informe de dos páginas con la parte que puede ser suerte, en porcentaje.

**Criterio de aceptación**

- La misma estrategia con y sin costes da resultados distintos y ambos están en el informe.
- El número de pruebas realizadas está registrado, no estimado a posteriori.
- El README dice explícitamente qué NO demuestra el backtest.

**Defensa en entrevista**

- *«¿Por qué el Sharpe no basta?»* → número de intentos, asimetría, colas y costes.
- *«¿Cómo evitas el look-ahead?»* → línea temporal de los datos, purga, y una prueba que lo
  detecta (por ejemplo, meter el precio de mañana y ver que la métrica se dispara).

**Preparado por:** `P15`, `P16`.

---

## 3. Qué proyecto hacer según el mes

| Mes | Capa A | Capa B | Resultado visible |
| --- | --- | --- | --- |
| 1 | `P05`, `P11`, `P13` | PF-01 | Primer repositorio con pipeline reproducible |
| 2 | `P12`, `P18` | PF-02 | Almacén dimensional con capa semántica |
| 3 | `P14`, `P15` | PF-06 (parte 1) | Rigor estadístico demostrable |
| 4 | `P17`, `P16` | PF-03 o PF-04 | Streaming o CDC, el diferenciador |
| 5 | `P08`, `P10` | PF-05 | Servicio con SLA y postmortem |
| 6 | repaso | PF-06 (cierre) o segundo proyecto de la ruta elegida | Portfolio con dos proyectos defendibles |

Dos proyectos defendidos de arriba abajo valen más que seis empezados. Si en el mes 3 no has
terminado PF-01, el problema no es el ritmo: es el alcance.

---

## 4. Cómo se conecta esto con el temario

| Proyecto | Conceptos que se leen antes | Conceptos que se practican |
| --- | --- | --- |
| PF-01 | `ingesta-incremental-y-cdc`, `orquestacion-y-dag`, `calidad-de-datos` | `dbt-y-transformacion`, `contratos-de-datos`, `metricas-y-alertas` |
| PF-02 | `modelado-dimensional`, `esquema-estrella-y-copo` | `scd-dimensiones-cambiantes`, `capa-semantica-y-metricas`, `reconciliacion-y-pruebas` |
| PF-03 | `kafka-y-colas`, `streaming-tiempo-real` | `algoritmos-de-streaming`, `idempotencia-y-reintentos`, `lakehouse-y-table-formats` |
| PF-04 | `ingesta-incremental-y-cdc`, `evolucion-de-esquema` | `scd-dimensiones-cambiantes`, `backfill-y-reproceso`, `reconciliacion-y-pruebas` |
| PF-05 | `fastapi`, `apis-rest` | `idempotencia-en-apis`, `resiliencia-de-servicios`, `incidentes-y-postmortem` |
| PF-06 | `retornos-logaritmicos`, `purged-kfold` | `sharpe-deflactado`, `sesgo-de-supervivencia`, `slippage-y-comisiones` |

Los ids están copiados del temario actual: si alguno cambia de nombre, `generar.mjs --validar`
lo dirá al enlazarlo desde una página, y esta tabla habrá que corregirla a mano.

---

## 3. Por qué engancha cada proyecto

Un ejercicio aburrido no se termina. Esta es la chispa de cada uno, en una línea.

| Id | Chispa |
| --- | --- |
| P01 | Ver con tus ojos que ordenar 10.000 números no cuesta lo mismo con dos algoritmos |
| P02 | Encontrar el duplicado que hizo que la factura saliera dos veces |
| P03 | Adivinar un número en 7 intentos de entre un millón |
| P04 | Descubrir que recorrer una matriz al revés tarda el doble |
| P05 | Relanzar la carga tres veces y que no se duplique nada |
| P06 | Meter un dato imposible y ver saltar el control que tú escribiste |
| P07 | Cazar la variable que miraba al futuro y hundía el modelo |
| P08 | Elegir el umbral que cuesta menos dinero, no el que da más exactitud |
| P09 | Comprobar cómo el coste de una comisión se come una estrategia ganadora |
| P10 | Distinguir «pasó después» de «pasó por» |
| P11 | Reconstruir una carrera desde las vueltas y encontrar la parada |
| P12 | Responder en una pantalla la pregunta que todos discuten en el bar |
| P13 | Decidir si la parada te costó la carrera o fue el tráfico |
| P14 | Ponerle número al «riesgo» que todos dicen asumir |
| P15 | Descubrir que tu genio era beta disfrazado |
| P16 | Escribir el memo que defenderías delante de un inversor |
| P17 | Construir una ingesta que aguanta que la API te ignore |
| P18 | Predecir la parrilla sin hacer trampa con la posición final |
| P19 | Comprobar si el undercut funciona de verdad o es una leyenda |
| P20 | Convertir 380 partidos en un modelo que responde preguntas |
| P21 | Explicar por qué el xG dice una cosa y el marcador otra |
| P22 | Calcular cuánto de tu «rentabilidad» se la comió la inflación |

Los seis de portfolio (PF-01 a PF-06) enganchan por otra razón: son los que alguien mira en una
entrevista. El detalle está en §2.
