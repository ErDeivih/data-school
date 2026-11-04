# APIs gratuitas sin suscripción (probadas el 2026-11-02)

**Para qué:** datos reales para los proyectos sin tarjeta, sin registro y sin sorpresas. Cada fila
dice si necesita clave, qué límite tiene y para qué proyecto sirve.

**Estado de la prueba:** «200» significa que respondió desde este equipo ese día. «Limitada» o
«429» significa que existe pero hay que espaciar las peticiones.

---

## 1. Probadas y funcionando

| API | URL | Clave | Límite | Para qué |
| --- | --- | --- | --- | --- |
| Banco Mundial | `https://api.worldbank.org/v2/` | No | Sin límite publicado; responde lento a veces | PF-01 (población, PIB, esperanza de vida), series por país y año |
| OpenF1 | `https://api.openf1.org/v1/` | No | Límite no publicado; histórico desde 2023 | F1 real: sesiones, pilotos, posiciones, vueltas, radios (P17-P19) |
| GitHub | `https://api.github.com/` | No (60/h sin token, 5.000 con token gratis) | 60 peticiones por hora por IP | Ingesta paginada, eventos, repos; buen ejercicio de rate limit |
| CoinGecko | `https://api.coingecko.com/api/v3/` | No (plan demo) | ~30 peticiones por minuto | Series de precios de cripto, ingesta periódica e idempotencia |
| CityBikes | `https://api.citybik.es/v2/` | No | Sin límite publicado | Estado por estación cada minuto: streaming simulado con Kafka |
| Rest Countries | `https://restcountries.com/v3.1/` | No | Sin límite publicado | Dimensión de países para cualquier modelo en estrella |

## 2. Funcionan pero piden clave gratuita

| API | URL | Clave | Por qué merece la pena |
| --- | --- | --- | --- |
| AEMET OpenData | `https://opendata.aemet.es/` | Gratis, por correo | Meteorología de España: practica gestión de claves y caché |
| ESIOS / Red Eléctrica | `https://www.ree.es/es/datos` | Token gratuito | Series de 10 minutos: estacionalidad, anomalías, pronóstico |
| Alpha Vantage | `https://www.alphavantage.co/` | Gratis | 25 peticiones al día: precios diarios y fundamentales para F09 |
| football-data.org | `https://www.football-data.org/` | Gratis | Resultados y clasificaciones de fútbol, con plan gratuito |
| NASA | `https://api.nasa.gov/` | `DEMO_KEY` | Imágenes y datos científicos; límite muy bajo pero suficiente para practicar |
| USGS | `https://earthquake.usgs.gov/fdsnws/event/1/` | No | Terremotos en tiempo casi real: eventos con geolocalización |
| INE | `https://www.ine.es/dyngs/INEbase/` | No (API JSON `tempus3`) | Datos españoles oficiales: paro, IPC, padrón |

## 3. Existen pero hoy no respondieron desde aquí

| API | URL | Qué pasó | Qué hacer |
| --- | --- | --- | --- |
| Open-Meteo | `https://api.open-meteo.com/v1/forecast` | 503 el 2026-11-02 | Reintentar otro día; el archivo histórico está en `archive-api.open-meteo.com`. Si insiste, usar AEMET |
| GDELT | `https://api.gdeltproject.org/api/v2/doc/doc` | 429 (demasiadas peticiones) | Espaciar peticiones; el proyecto de eventos globales aguanta un ritmo lento |

## 4. Sin API, pero con datos abiertos que se descargan

| Fuente | URL | Formato | Proyecto |
| --- | --- | --- | --- |
| NYC TLC | `https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page` | Parquet por mes | El clásico de pipeline batch |
| StatsBomb Open Data | `https://github.com/statsbomb/open-data` | JSON de eventos | xG y redes de pases (P21) |
| GH Archive | `https://gharchive.org/` | JSON.gz por hora | Streaming con Kafka |
| datos.gob.es | `https://datos.gob.es/` | CSV y JSON | Cualquier proyecto con datos españoles |
| INE (descargas) | `https://www.ine.es/` | CSV y PC-Axis | Series oficiales sin API |

---

## 5. Reglas para usar APIs en un proyecto

1. **Guarda el bruto antes de transformar.** Si la API cambia, el fichero viejo es tu única prueba.
2. **Comprueba el límite en la cabecera**, no en la documentación: `X-RateLimit-Remaining` dice la
   verdad del momento.
3. **Reintenta con espera creciente**, no en bucle cerrado. Un 429 no se arregla insistiendo.
4. **Cachea por clave y fecha.** Una segunda ejecución del mismo día no debe pedir lo mismo.
5. **Documenta la licencia y la fecha de descarga** en el README. Sin eso, el proyecto no es
   reproducible.
6. **No publiques datos que no puedas redistribuir.** Guarda el script y documenta la fuente.

## 6. Cuáles usar según el proyecto

| Proyecto | API | Por qué |
| --- | --- | --- |
| PF-01 (pulso económico) | Banco Mundial | Sin clave, series largas, licencia clara |
| P17 (ingesta F1) | OpenF1 | Gratis, sin clave y con datos desde 2023 |
| P18-P19 (F1 con datos reales) | OpenF1 + FastF1 | OpenF1 para ingesta; FastF1 pide F1TV Access desde v3.9 |
| P20-P21 (fútbol) | football-data.org + StatsBomb | Resultados y eventos con licencia de uso no comercial |
| PF-03 (streaming) | CityBikes o GH Archive | Flujo continuo y pequeño, sin infraestructura |
| PF-05 (servicio) | CoinGecko o GitHub | Datos que cambian y permiten cachear |
