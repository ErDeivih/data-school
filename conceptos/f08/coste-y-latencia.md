---
id: coste-y-latencia
titulo: Coste y latencia
fase: 8
nivel: intermedio
rutas: [ds, de]
prerequisitos: [tokenizacion, ventanas-de-contexto, como-funciona-un-llm]
tags: [llm, coste, latencia, produccion]
resumen: El presupuesto de una consulta se decide con tres números (tokens de entrada, de salida y aciertos de caché) y la latencia se reparte entre el primer token y el resto.
fuentes: ["Pope et al. (2023), 'Efficiently Scaling Transformer Inference'"]
---

## En una frase

Cada consulta a un modelo de lenguaje se paga en **tokens** (los que envías y los que genera)
y se espera en **dos tiempos distintos**: lo que tarda en salir la primera palabra y lo que
tarda en terminar, y esos dos tiempos se sienten de forma muy diferente.

## La idea

Un modelo de lenguaje no cobra por pregunta, cobra por
[[tokenizacion|token]]: por cada trozo de texto que le entra y por cada trozo que produce. Y
no cuestan lo mismo: el token de salida se factura bastante más caro que el de entrada,
porque se genera de uno en uno mientras que la entrada se procesa en paralelo.

Eso crea una asimetría que sorprende a casi todo el mundo la primera vez. Un sistema con un
prompt de 3.000 tokens, veinte turnos de conversación y 120.000 tokens de documentos adjuntos
paga casi todo en la **entrada**. Un sistema que pide al modelo que escriba un informe de
2.000 palabras paga casi todo en la **salida**. Son dos problemas de optimización distintos.

Hay tres palancas, y ninguna es magia:

1. **Enviar menos tokens.** Recuperar 5 fragmentos en vez de 20, resumir el historial en vez de
   arrastrarlo entero, usar modelos pequeños para tareas fáciles y grandes solo donde haga
   falta. Es la palanca más eficaz y la que más veces se ignora.
2. **Caché de prompt.** Muchos proveedores permiten marcar el prefijo estable de la
   conversación (el prompt del sistema, las instrucciones largas, el manual de la empresa)
   para que no se vuelva a procesar ni se cobre a precio completo. Como el prefijo no cambia
   entre consultas, el ahorro es directo.
3. **Comprimir la salida.** Pedir «responde en un párrafo» en vez de «explica en detalle»
   reduce el coste y casi siempre mejora la respuesta. Los tokens de salida son los caros.

La latencia, en cambio, se mide con dos números. El **tiempo hasta el primer token** (*time to
first token*) es lo que tarda el modelo en procesar toda la entrada y producir la primera
palabra: depende sobre todo del tamaño de la entrada, y es lo que hace que una consulta con
120.000 tokens de contexto parezca colgada. El **tiempo total** es el primer token más el
tiempo de generar el resto, que depende del número de tokens de salida.

De ahí sale la regla práctica: **para que un sistema se sienta rápido, lo que hay que
arreglar es el primer token** (menos contexto, caché, o un modelo más pequeño); para que
termine antes, hay que acortar la salida. Y el **streaming** no reduce el tiempo total: mejora
la percepción porque el usuario ve texto mientras se genera. Un informe de 2.000 palabras que
tarda 40 segundos es insufrible sin streaming y aceptable con él.

## Definición formal

Sea una consulta con `n_in` tokens de entrada, de los cuales `n_cache` están ya en caché (un
subconjunto del prefijo estable), y `n_out` tokens generados. Con los precios por token del
proveedor:

:::formula
coste = p_in · (n_in − n_cache) + p_cache · n_cache + p_out · n_out
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `p_in` | Precio de un token de entrada que no está en caché | euros por millón de tokens | Sube el coste de todo lo que no sea prefijo estable: es la palanca de los documentos recuperados |
| `p_cache` | Precio de un token de entrada servido desde caché | euros por millón de tokens | Aunque suba, sigue siendo la parte barata: el ahorro de cachear el prefijo se encoge, pero no desaparece |
| `p_out` | Precio de un token generado | euros por millón de tokens | Es el precio más alto de los tres: sube el coste de todo lo que el modelo escribe, incluso lo que luego descartas |
| `n_in` | Tokens que se envían en el prompt | tokens | Sube el coste de entrada y también el tiempo hasta el primer token |
| `n_cache` | De esos, los que ya estaban en caché | tokens | Baja el coste (se pagan a `p_cache`) y baja el primer token; no puede pasar de `n_in` |
| `n_out` | Tokens que genera el modelo | tokens | Sube el coste más deprisa que ningún otro término y alarga el tiempo total, pero no toca el primer token |
:::

- `p_in` — precio por token de entrada no cacheado.
- `p_cache` — precio por token de entrada servido desde caché; suele ser entre 5 y 20 veces
  menor que `p_in`.
- `p_out` — precio por token generado. Se aplica a **todo** el texto que produce el modelo,
  incluido el que luego descartas.
- `n_cache ≤ n_in`: solo se puede cachear un prefijo idéntico entre consultas, no cualquier
  parte del prompt.

La latencia se modela con dos términos:

:::formula
TTFT ≈ t₀ + a · (n_in − n_cache) + a_c · n_cache        T_total = TTFT + b · n_out
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `TTFT` | Tiempo hasta el primer token: lo que el usuario espera mirando una pantalla vacía | milisegundos | Es el número que decide si el sistema «parece» rápido, aunque el total no cambie |
| `t₀` | Coste fijo de red y arranque, independiente del tamaño del prompt | milisegundos | Suma a todos los casos por igual: es el suelo por debajo del cual no baja ninguna consulta |
| `a` | Tiempo por token de entrada que hay que procesar | milisegundos por token | Con 120.000 tokens, unas centésimas por token ya son cientos de milisegundos |
| `a_c` | Tiempo por token servido desde caché | milisegundos por token | Como `a_c < a`, sube menos el TTFT que el mismo token sin cachear; si se acercara a `a`, la caché dejaría de servir para latencia |
| `b` | Tiempo por token generado; su inversa es la velocidad de generación | milisegundos por token | Sube el tiempo **total** y no toca el primer token: es el parámetro de la salida, no de la entrada |
| `T_total` | Tiempo hasta la última palabra | milisegundos | Es `TTFT + b · n_out`: con salidas largas, el término de generación se come al de entrada |
:::

- `TTFT` — tiempo hasta el primer token. `t₀` es el coste fijo de red y arranque; `a` es el
  tiempo por token de entrada procesado y `a_c` el de un token servido desde caché (`a_c < a`).
- `b` — tiempo por token generado; su inversa es la velocidad de generación.
- Fíjate en que `n_in` aparece en `TTFT` pero no en el término de generación, y `n_out` solo
  aparece en el segundo. Son dos cuellos de botella independientes.

Un concepto que conviene tener claro para presupuestar: el **coste por consulta** no es el
coste del sistema. Multiplica por el número de consultas al día y por los días del mes, y
súmale los reintentos, las llamadas de herramientas y las evaluaciones automáticas. Un agente
que da 6 pasos por tarea hace 6 llamadas al modelo, no una.

:::figura
fichero: coste-y-latencia-factura-y-espera
pie: A la izquierda, el coste por consulta según cuántos tokens de documentos se recuperan, con y sin caché del prefijo. Las dos rectas suben casi en paralelo: la distancia entre ellas es el ahorro de la caché (0,409 € frente a 0,369 € con el mismo prompt), mientras que bajar de 120.000 a 30.000 tokens de documentos deja la consulta en 0,099 €. La palanca grande está en la pendiente, no en la separación. A la derecha, el tiempo hasta la primera palabra de los tres casos: 58, 290 y 83 ms. Los tres terminan alrededor de los 6 s porque el tiempo total lo domina la generación, así que de nada sirve mirar solo el total: hay que mirar el primer token, que es el número que el usuario percibe como «esto funciona».
fuente: figuras/coste-y-latencia-1.py
:::

## Ejemplo

Sistema de preguntas sobre documentación con estos números por consulta:

- Prompt del sistema: 3.000 tokens.
- Historial de conversación: 12.000 tokens.
- Documentos recuperados: 120.000 tokens.
- Respuesta generada: 300 tokens.
- Precios de trabajo: 3 €, 0,30 € y 15 € por millón de tokens de entrada, caché y salida.

**Sin caché:** `(3.000 + 12.000 + 120.000) · 3 / 10⁶ + 300 · 15 / 10⁶ = 0,405 + 0,0045 =
0,4095 €` por consulta. Con 1.000 consultas al día, unos **2.565 € al mes** solo en el modelo.

**Con caché del prefijo estable** (sistema + historial: 15.000 tokens cacheados, 120.000
normales): `15.000 · 0,30 / 10⁶ + 120.000 · 3 / 10⁶ + 300 · 15 / 10⁶ = 0,0045 + 0,36 + 0,0045
= 0,369 €`. El ahorro es del 10 %: los documentos, que son lo que domina el gasto, **no se
pueden cachear** porque cambian en cada consulta según la pregunta.

**Reduciendo los documentos a 5 fragmentos** (unos 30.000 tokens), con caché:
`0,0045 + 0,09 + 0,0045 = 0,099 €`, un **73 % menos** que el caso con caché y un 76 % menos que
el original. La lección es que la palanca grande no es la caché, es recuperar menos.

Latencia, con `t₀ = 50 ms`, `a = 0,002 ms` por token de entrada, `a_c = 0,0002 ms` por token
cacheado y `b = 20 ms` por token de salida:

| Caso | Entrada | En caché | Primer token | Total |
| --- | --- | --- | --- | --- |
| Contexto corto | 4.000 | 0 | 58 ms | 6.058 ms |
| Contexto largo | 120.000 | 0 | 290 ms | 6.290 ms |
| Contexto largo con caché | 120.000 | 115.000 | 83 ms | 6.083 ms |

Los tres casos tardan casi lo mismo **en total** (unos 6 segundos, dominados por los 300
tokens de salida), pero el primer token pasa de 290 ms a 83 ms con caché. Si el sistema escribe
en streaming, el usuario ve texto casi al instante en el tercer caso y espera un tercio de
segundo en el segundo. La diferencia de sensación es enorme y el coste es el mismo.

## Código

```python verificable
# Precios de ejemplo en euros por millon de tokens: cámbialos por los de tu proveedor.
PRECIO_ENTRADA = 3.0     # tokens de entrada que no estan en cache
PRECIO_CACHE = 0.30      # tokens de entrada que si estan en cache
PRECIO_SALIDA = 15.0     # tokens generados

def coste(entrada_nueva, entrada_cache, salida):
    # los precios son por MILLON de tokens: el / 1e6 deja el resultado en euros por consulta
    return (entrada_nueva * PRECIO_ENTRADA + entrada_cache * PRECIO_CACHE
            + salida * PRECIO_SALIDA) / 1e6

# el orden de la tupla manda: sistema, historial, documentos y salida, en ese orden
sistema, historial, documentos, respuesta = 3000, 12000, 120000, 300

# sin cache: todo el prompt (prefijo + documentos) se paga a precio de entrada
sin_cache = coste(sistema + historial + documentos, 0, respuesta)
# con cache: el prefijo estable va en la ranura de cache; los documentos, que cambian
# en cada pregunta, van en la de entrada nueva
con_cache = coste(documentos, sistema + historial, respuesta)
# recortado: el mismo prefijo con 30.000 tokens de documentos en vez de 120.000
recortado = coste(30000, sistema + historial, respuesta)

print(f"sin cache            {sin_cache:.4f} EUR")
print(f"con cache            {con_cache:.4f} EUR")
print(f"con cache y 30k docs {recortado:.4f} EUR")
print(f"ahorro de la cache   {(1 - con_cache / sin_cache) * 100:.0f} %")
print(f"1000 consultas al dia con cache: {con_cache * 1000 * 30:.0f} EUR al mes")
```

:::claves
- `coste()` devuelve **euros por consulta**, no euros: los precios están por millón de tokens y por eso divide entre `1e6`. Si quitas ese `/ 1e6`, los números salen un millón de veces mayores (0,41 € se convierten en 409.500 €) y el error solo se nota al comparar con la factura.
- El **orden de los argumentos** decide qué se cobra a precio de caché: el primero es la parte que no está cacheada y el segundo la que sí lo está. En `coste(documentos, sistema + historial, respuesta)` los documentos van en la primera ranura a propósito, porque cambian en cada pregunta y no se pueden cachear; ponerlos en la segunda sería cobrar a precio de caché algo que nunca acierta.
- `sin_cache` pasa `0` como entrada cacheada: no es un descuento del 100 %, es el caso de control con el que se compara el ahorro.
- Los tres `print` con decimales no son cálculo: `{valor:.4f}` significa «cuatro decimales» y `{valor:.0f}` «ninguno». El último multiplica por 1.000 consultas y por 30 días; el mes se supone de 30 días, no de 31.
- Esta función es pura y estática: cambiar los tres `PRECIO_*` cambia los tres resultados a la vez. El porcentaje de la cuarta línea compara `con_cache` con `sin_cache`, no con `recortado`: cambiar de comparación cambia la historia que cuenta el número, aunque los euros sean los mismos.
:::

```python verificable
# Modelo de latencia: los parametros ya estan en milisegundos por token.
# Los tres primeros argumentos son obligatorios (entrada, salida y tokens ya en cache);
# los que llevan valor por defecto son los t0, a, a_c y b de la formula de latencia.
def latencia(entrada, salida, cache_aciertos, ttft_base=50.0, ms_por_token_entrada=0.002,
             ms_por_token_cache=0.0002, ms_por_token_salida=20.0):
    # El primer token espera a que se procese toda la entrada; los demas salen a ritmo de salida.
    ttft = (ttft_base + (entrada - cache_aciertos) * ms_por_token_entrada
            + cache_aciertos * ms_por_token_cache)
    # devuelve DOS numeros en una tupla: quien llame tiene que desempaquetarlos
    return ttft, ttft + salida * ms_por_token_salida

# cada caso es una tupla (nombre, tokens de entrada, tokens servidos desde cache)
casos = [("contexto corto", 4000, 0), ("contexto largo", 120000, 0),
         ("contexto largo con cache", 120000, 115000)]
for nombre, entrada, cache in casos:
    ttft, total = latencia(entrada, 300, cache)   # 300 es la salida, igual en los tres casos
    print(f"{nombre:26s} primer token {ttft:>7.0f} ms   total {total:>7.0f} ms")
# el total lo domina la salida; la cache solo mueve el primer token
```

## Errores típicos

- **Presupuestar por el promedio y no por la cola.** La factura la deciden las consultas
  patológicas: la conversación de 40 turnos, el documento de 200 páginas, el agente que
  reintenta seis veces. Mide el percentil 95 y el 99 de tokens por consulta, no solo la media.
- **Arrastrar todo el historial en cada turno.** El turno 20 reenvía los 19 anteriores: el
  coste crece de forma cuadrática con la duración de la conversación. Resume, recorta por
  ventana o usa la caché del prefijo.
- **Creer que la caché arregla el gasto.** Solo se cachea el prefijo **idéntico** entre
  llamadas. Los documentos que cambian con cada pregunta, que suelen ser el grueso del gasto,
  no entran. Primero reduce el contexto, después optimiza la caché.
- **Optimizar el coste y no mirar la calidad.** Recortar el contexto de 120.000 a 30.000
  tokens abarata un 73 %, pero si los fragmentos que quitas contenían las respuestas, el
  sistema empeora. Cada recorte se mide con el conjunto de
  [[evaluacion-de-llms|evaluación]], no con la factura.
- **Usar el modelo más grande para todo.** Clasificar un correo en tres categorías, extraer un
  importe o reformatear una fecha son tareas que un modelo pequeño hace igual de bien por una
  fracción del precio y de la latencia. Reserva el modelo grande para el razonamiento y la
  redacción final.
- **Olvidar el coste oculto del agente.** Cada paso de un bucle de
  [[agentes-y-herramientas|agente]] es una llamada completa con todo el historial. Un agente de
  6 pasos no cuesta 6 veces una consulta: cuesta más, porque el historial crece en cada paso.
- **Medir la latencia solo de extremo a extremo.** Sin separar el primer token del total, no
  sabes si el problema es el contexto (arreglo: recuperar menos) o la generación (arreglo:
  pedir respuestas más cortas). Son dos arreglos opuestos.

:::truco
Antes de tocar el prompt, mide tres números: tokens de entrada por consulta, tokens de salida
por consulta y tiempo hasta el primer token. Con esos tres se sabe qué palanca mover, y sin
ellos cualquier optimización es una apuesta.
:::

## Comprueba que lo sabes

:::quiz
p: Tu primera consulta de cada conversación tarda 200 ms hasta el primer token y las siguientes tardan 1,5 s. ¿Qué pasa?
o: El modelo se está calentando y hay que esperar
o: El contexto crece con el historial y cada turno reenvía todo lo anterior, así que la entrada es cada vez mayor
o: La red se degrada con el uso
a: 2
e: El primer token depende sobre todo del tamaño de la entrada, y en una conversación la entrada es la suma de todos los turnos previos más el actual. La solución es recortar o resumir el historial y cachear el prefijo estable, no esperar: el efecto no desaparece solo.
:::

:::quiz
p: Cachear el prompt del sistema reduce la factura de un 3 % y cachear los documentos no es posible. ¿Qué palanca queda?
o: Subir la temperatura del modelo
o: Recuperar menos fragmentos y más relevantes, que es donde está el grueso de los tokens
o: Repetir la consulta para promediar
a: 2
e: Si los documentos dominan la entrada y no se pueden cachear porque cambian en cada consulta, la única palanca real es enviar menos y mejores fragmentos. Repetir la consulta multiplica el coste, y la temperatura no afecta al número de tokens de entrada.
:::

:::quiz
p: ¿Por qué el streaming mejora la experiencia si el tiempo total de generación no cambia?
o: Porque comprime los tokens antes de enviarlos
o: Porque el usuario empieza a leer antes, así que la espera percibida depende del primer token y no del total
o: Porque reduce el número de tokens de salida
a: 2
e: El streaming no altera ni el coste ni el tiempo total: cambia en qué momento hay algo en pantalla. La percepción pasa a depender del tiempo hasta el primer token, y por eso conviene optimizar ese número con menos contexto o con caché.
:::
