---
id: observabilidad-de-llms
titulo: Observabilidad de una aplicación con LLM
fase: 8
nivel: avanzado
rutas: [ds, alg]
prerequisitos: [coste-y-latencia, evaluacion-de-llms, structured-output]
tags: [trazas, metricas, coste, depuracion]
resumen: Qué grabar de cada consulta, en qué forma y para qué: sin trazas por paso ni tokens medidos, un sistema con LLM no se puede depurar ni presupuestar.
fuentes: ["Beyer et al. (2016), 'Site Reliability Engineering: How Google Runs Production Systems'", "Sculley et al. (2015), 'Hidden Technical Debt in Machine Learning Systems'", "OpenTelemetry (2024), 'Specification: Traces, Spans and Context Propagation'"]
---

## En una frase

Observar una aplicación con LLM es guardar, por cada consulta, **lo que entró, lo que salió, cuántos
tokens costó, cuánto tardó y qué pasos intermedios hubo**, y tenerlo agregado por versión: es lo
único que permite responder «¿por qué esta respuesta es peor que la de la semana pasada?» sin
adivinar.

## La idea

Un sistema con LLM se parece peligrosamente a un sistema normal, y por eso se opera mal. Tiene una
entrada, una salida y una latencia, así que parece que basta con el registro de siempre. Pero se
diferencia en cuatro cosas, y cada una tiene su consecuencia:

1. **No es determinista.** La misma entrada puede dar salidas distintas. Un fallo no se reproduce
   ejecutando el mismo caso otra vez: hay que haber guardado la traza exacta.
2. **Una consulta es varios pasos.** Recuperar documentos, llamar al modelo, validar el esquema,
   reintentar, llamar a una herramienta. Un registro con una sola línea de «petición completada» no
   dice en qué paso se fue el tiempo ni el dinero.
3. **El coste es una variable de la consulta.** No es como una consulta a una base de datos, donde el
   precio es fijo. Diez documentos recuperados en vez de tres multiplican la factura y el registro no
   lo nota si nadie apunta los tokens.
4. **La calidad no se ve en el código de estado.** Un `200 OK` con una respuesta mala es un éxito para
   la infraestructura y un desastre para el negocio. Sin una medición de calidad ligada a la traza, no
   hay forma de saber si el sistema empeoró.

De ahí sale la definición de trabajo: una **traza** por consulta, con un **span** por paso, y en cada
span los atributos que importan (tokens de entrada, tokens de salida, coste, modelo, versión del
prompt, documentos recuperados, resultado de la validación). Eso es exactamente lo que hace
OpenTelemetry con cualquier sistema distribuido; aquí solo se añaden atributos nuevos.

Lo que casi nadie instrumenta y es donde está el dinero: **el coste por traza no se reparte igual
que las peticiones**. La mediana de las consultas es barata y la cola no: un 5 % de trazas con
contexto enorme y varios reintentos se puede llevar la mitad de la factura. Si solo miras el coste
medio, no ves nada; si miras el p95 de coste por traza, ves el problema entero.

Y queda la pieza que convierte esto en algo útil de verdad: **todo se agrupa por versión** (del
modelo, del prompt y del índice de recuperación). Una métrica sin versión es una anécdota: si el
acierto baja del 82 % al 71 %, lo primero que hay que poder contestar es si cambió el prompt, el
modelo o los documentos. Sin ese etiquetado, la comparación es entre manzanas y manzanas de la
semana pasada.

:::figura
fichero: observabilidad-que-mirar-en-produccion
pie: Arriba a la izquierda, la distribución de latencia por consulta: la mediana está en 2,6 segundos, pero el 5 % de las trazas pasa de 5,3 segundos, y casi todas las lentas son reintentos. Arriba a la derecha, el coste acumulado del mes ordenando las consultas de más barata a más cara: pasar del 60 % de las consultas al 95 % solo añade el 21 % del gasto, así que el dinero está repartido y el sitio donde recortar no es la cola. Abajo a la izquierda, los fallos de validación de esquema contados por su causa: dos entradas solapadas del catálogo de herramientas bastan para que el modelo elija mal. Abajo a la derecha, cómo se reparte el gasto de tokens entre entrada, caché y salida: la entrada se lleva el 80 % y la caché, que parecía la palanca, aporta el 2 %.
fuente: figuras/observabilidad-de-llms-1.py
:::

## Definición formal

Una traza `T` es un árbol de spans. Cada span `s` lleva nombre, instante de inicio, duración y un
conjunto de atributos. La agregación que se mira en producción es siempre la misma:

:::formula
coste(traza) = Σ_span ( tokens_entrada · p_entrada + tokens_cache · p_cache + tokens_salida · p_salida )
:::

:::formula
éxito = nº de trazas válidas / nº de trazas totales        latencia_p95 = percentil 95 de la duración total
:::

Y para saber si el sistema sirve o solo funciona, hace falta una medida de calidad unida a la traza:

:::formula
acierto = nº de trazas correctas / nº de trazas evaluadas        por versión (modelo, prompt, índice)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `traza` | Todo lo que ocurrió en una consulta, con sus spans y sus atributos | una por consulta | Es la unidad de depuración. Si dos consultas se mezclan en la misma traza, deja de servir para reproducir nada |
| `span` | Un paso de la traza: recuperación, llamada al modelo, validación, herramienta | milisegundos y atributos | Cuantos más pasos se instrumenten, más fino el diagnóstico. Instrumentar solo la llamada al modelo deja invisible el tiempo de recuperación y el de los reintentos |
| `tokens_entrada` | Tokens de contexto que se envían, incluido el prompt de sistema y los documentos | tokens | Es la partida que más crece en un sistema con RAG: cada documento recuperado se paga en **cada** llamada de la traza, no una vez |
| `tokens_cache` | Los de la parte del prefijo que no cambia y se cobra a precio reducido | tokens | Subirlos es ahorro puro, siempre que el prefijo sea idéntico entre peticiones. Un cambio de prompt al principio de todo invalida la caché entera |
| `tokens_salida` | Tokens generados | tokens | Cuestan varias veces más que los de entrada y se generan de uno en uno, así que mandan en la latencia total tanto como en la factura |
| `coste(traza)` | Lo que costó esa consulta, sumando todos sus spans | euros | Mirar la media esconde el problema: el p95 y la contribución del 5 % más caro son los números que deciden el diseño |
| `latencia_p95` | Duración total por debajo de la cual está el 95 % de las consultas | milisegundos | Es la latencia que percibe la gente. La media se la lleva por delante un puñado de trazas con reintentos |
| `acierto` | Fracción de trazas correctas según el conjunto de evaluación | proporción | Sin `acierto` medido no hay mejora posible: optimizar coste y latencia en un sistema que responde mal es acelerar el error |
| `versión` | Etiqueta de modelo, prompt e índice de recuperación de cada traza | cadena | Sin ella no se puede comparar nada. Es el atributo que convierte una métrica en una decisión |
:::

El error que hay que medir antes de tocar nada: comparar dos versiones con el **mismo** conjunto de
evaluación. Si el conjunto cambia entre medidas, la diferencia que ves no es del sistema.

:::formula
Δ_acierto = acierto(v2) − acierto(v1)      medido sobre el mismo conjunto y con el mismo juez
:::

## Ejemplo

Un asistente de soporte con RAG atiende 500 consultas al día. Desde que se instrumentó bien, la
tabla de agregados es esta:

| Métrica | Valor | Qué significa |
| --- | --- | --- |
| Consultas al día | 500 | Volumen estable |
| Latencia mediana | 2.643 ms | La mitad de las consultas tardan menos |
| Latencia p95 | 5.312 ms | Una de cada veinte pasa de cinco segundos |
| Tasa de éxito | 91,8 % | El 8,2 % acaba en reintento o en error visible |
| Tokens de entrada por consulta | 3.600 | Prompt de sistema, historial y documentos |
| Tokens de salida por consulta | 250 | Respuesta corta |
| Coste mediano por consulta | 0,0206 € | `3.600 · 3,00 + 1.200 · 0,30 + 250 · 15,00` por millón |
| Coste del p95 | 0,0346 € | 1,68 veces la mediana: la cola existe, pero no es donde está el grueso |
| Reparto de la factura | 80 % entrada, 18 % salida, 2 % caché | La partida que decide no es la caché, es el volumen de entrada |

La primera lectura, la obvia: 2,6 segundos de mediana es mucho para un chat. La segunda lectura, la
que da la observabilidad: si se separa por número de reintentos, casi todo el tiempo extra está en
las trazas que reintentaron. Los números de abajo salen de las 500 trazas de ejemplo del código, y
el detalle importa más que el total.

La factura del día son 10,37 € y está repartida: la mitad del gasto se acumula en 321 de las 500
consultas. Eso descarta la hipótesis cómoda de «hay unas pocas consultas carísimas que rompen el
presupuesto»: el p95 cuesta 1,68 veces la mediana, no diez. Si de verdad quieres bajar la factura,
el sitio no es la cola, es la partida que domina el total: la **entrada**, con el 80,2 % del gasto.
La caché, que parecía la gran palanca, aporta el 1,7 % del ahorro de este sistema. Los tres números
completos salen de las 500 trazas de ejemplo del código, y están calculados en el panel de coste de
la figura.

Y la tercera lectura, la que casi nunca se hace: **la tasa de éxito del 91,8 % no es la calidad**.
Una traza puede terminar con un esquema válido y una respuesta equivocada. El acierto se mide con el
conjunto de evaluación de [[evaluacion-de-llms|evaluación de LLMs]], y lo que aporta la observabilidad
es poder decir **en qué trazas** falló: con el identificador de la traza se va al prompt exacto, a los
documentos que se recuperaron y a la respuesta que se dio. Sin ese hilo, un fallo de calidad es un
número sin caso.

Los tres fallos que aparecen una y otra vez en el registro, por orden de frecuencia:

| Causa | Síntoma | Dónde se ve |
| --- | --- | --- |
| Esquema inválido | La respuesta no valida y se reintenta | El span de validación, no el del modelo |
| Documentos irrelevantes | Respuesta correcta de forma y vacía de contenido | La lista de documentos recuperados en el span de recuperación |
| Herramienta con dos entradas solapadas | El modelo elige la equivocada | El nombre de la herramienta en el span de la llamada |

Fíjate en que los tres se diagnostican en spans **distintos** del span del modelo. Un sistema que
solo instrumenta la llamada al modelo ve el síntoma —tarda, cuesta, falla— y no ve ninguna de las
tres causas.

## Código

```python verificable
# Agregados de una traza: lo minimo que hay que grabar para poder depurar y presupuestar.
import numpy as np

rng = np.random.default_rng(7)
N = 500

# Reintentos de cada consulta: la causa principal de la cola de latencia.
reintentos = rng.binomial(2, 0.30, size=N)
# El exito depende del numero de reintentos: mas intentos, sistema mas nervioso.
exito = rng.random(N) < np.where(reintentos == 0, 0.96, np.where(reintentos == 1, 0.90, 0.75))
# La latencia base de una llamada, con cola (lognormal), mas el coste de cada reintento.
latencia = rng.lognormal(mean=np.log(1100.0), sigma=0.35, size=N) + reintentos * 1900 \
           + np.where(exito, 0.0, 2500.0)

print("traza   exito   reintentos   latencia_ms")
for i in (0, 1, 2):
    print(f"{i:5d}   {str(bool(exito[i])):5s}   {reintentos[i]:10d}   {latencia[i]:11.0f}")
print("p50 de latencia:", round(float(np.percentile(latencia, 50))), "ms")
print("p95 de latencia:", round(float(np.percentile(latencia, 95))), "ms")
print("exito:", round(float(exito.mean()), 4))
# -> traza   exito   reintentos   latencia_ms
# ->     0   True             1          2536
# ->     1   True             1          2990
# ->     2   True             1          3209
# -> p50 de latencia: 2643 ms
# -> p95 de latencia: 5312 ms
# -> exito: 0.918

# La media de latencia no describe a nadie: mira la distancia entre la mediana y el p95.
print("media", round(float(latencia.mean())), "ms   p95 - p50:",
      round(float(np.percentile(latencia, 95) - np.percentile(latencia, 50))), "ms")
# -> media 2559 ms   p95 - p50: 2668 ms
```

:::claves
- `rng.binomial(2, 0.30, size=N)` genera el número de reintentos de cada traza. Casi la mitad salen con cero, casi la otra mitad con uno, y unas pocas con dos. Esa mezcla es lo que hace que la mediana ya esté en la parte alta: con un 54 % de trazas reintentando, la mediana cae del lado de los reintentos.
- La latencia se construye **sumando** una base con cola (`lognormal`, nunca negativa y con valores altos ocasionales), el coste fijo de cada reintento y un extra cuando la consulta termina mal. Ese extra no es decoración: una traza que falla tarda más precisamente porque se agotó el tiempo.
- `str(bool(exito[i]))` imprime `True` o `False`. Sin el `bool`, NumPy imprimiría un valor de su propio tipo y el comentario de la salida no coincidiría.
- `np.percentile(latencia, 95)` interpola entre los dos valores centrales de la cola, así que puede devolver un número que no está en los datos. Es lo correcto para un percentil: no es «una traza concreta», es una posición.
- La semilla fija (`default_rng(7)`) es lo que hace que los comentarios `# ->` sean ciertos. Sin ella, el bloque sería verificable solo en apariencia: cada ejecución daría números distintos y ninguna comprobación serviría.
:::

```python verificable
# El coste por traza: lo que cuesta la cola y de que esta hecha la factura.
import numpy as np

rng = np.random.default_rng(7)
N = 500
reintentos = rng.binomial(2, 0.30, size=N)

P_ENTRADA, P_CACHE, P_SALIDA = 3.00, 0.30, 15.00        # euros por millon de tokens
TEXTO_ENTRADA = rng.integers(1_400, 2_200, size=N)      # instrucciones, historial y pregunta
DOCUMENTOS = rng.integers(0, 8, size=N)                 # recuperados por consulta
TOKENS_POR_DOCUMENTO, TOKENS_SALIDA = 420, 250

tokens_entrada = TEXTO_ENTRADA + DOCUMENTOS * TOKENS_POR_DOCUMENTO + reintentos * 3_600
# El prefijo estable (instrucciones mas catalogo) se cobra a precio de cache.
tokens_cache = np.full(N, 1_200)
coste = (tokens_entrada * P_ENTRADA + tokens_cache * P_CACHE
         + TOKENS_SALIDA * P_SALIDA) / 1e6

mediana = float(np.median(coste))
p95 = float(np.percentile(coste, 95))
print("coste mediano por consulta:", round(mediana, 4), "EUR")
print("coste del p95:", round(p95, 4), "EUR")
print("el p95 cuesta", round(p95 / mediana, 2), "veces la mediana")
print("factura del dia:", round(float(coste.sum()), 2), "EUR")
# -> coste mediano por consulta: 0.0206 EUR
# -> coste del p95: 0.0346 EUR
# -> el p95 cuesta 1.68 veces la mediana
# -> factura del dia: 10.37 EUR

# La cola no es un caso raro: es un grupo de consultas que se puede aislar y arreglar.
orden = np.argsort(coste)                                 # de mas barata a mas cara
cola = int(0.05 * N)
print("la cola del 5 % mas caro se lleva:",
      round(float(coste[orden][-cola:].sum() / coste.sum()), 4))
print("la cola del 5 % mas caro cuesta de media:",
      round(float(coste[orden][-cola:].mean()), 4), "EUR por consulta")
print("la mitad mas barata de la factura cabe en",
      int(np.searchsorted(np.cumsum(coste[orden]) / coste.sum(), 0.5)) + 1, "consultas")
# -> la cola del 5 % mas caro se lleva: 0.0917
# -> la cola del 5 % mas caro cuesta de media: 0.038 EUR por consulta
# -> la mitad mas barata de la factura cabe en 321 consultas

# Y el desglose por partida: que concepto se come el presupuesto.
total = (tokens_entrada * P_ENTRADA + tokens_cache * P_CACHE + TOKENS_SALIDA * P_SALIDA).sum() / 1e6
for nombre, euros in (("entrada", (tokens_entrada * P_ENTRADA).sum() / 1e6),
                      ("cache", (tokens_cache * P_CACHE).sum() / 1e6),
                      ("salida", (TOKENS_SALIDA * P_SALIDA * N) / 1e6)):
    print(f"{nombre:8s} {euros:6.2f} EUR al dia   {euros / total:5.1%}")
# -> entrada    8.31 EUR al dia   80.2%
# -> cache      0.18 EUR al dia    1.7%
# -> salida     1.88 EUR al dia   18.1%
```

:::claves
- La cola del 5 % más caro se lleva el **9,2 %** de la factura y cuesta casi el doble que la mediana. No es una concentración dramática, y eso también es información: en un sistema con RAG sano el gasto está repartido, así que buscar «la consulta que rompe el presupuesto» es perder el tiempo. Donde de verdad se ahorra es en la partida que domina el total.
- `np.argsort` devuelve las **posiciones** que ordenarían el vector, no el vector ordenado. De ahí `coste[orden]`: primero se obtiene el orden, después se reordena. Confundirlos es el fallo más común al construir una curva acumulada.
- `np.searchsorted` sobre la curva acumulada contesta a «¿cuántas consultas hacen falta para llegar a la mitad del gasto?»: 321 de 500. Es la forma de comprobar que el gasto está repartido, y el número con el que se compara si un cambio de prompt lo concentra.
- `tokens_cache` no se suma aparte: modela la parte fija del prefijo (1.200 tokens) que se cobra a 0,30 €/millón en lugar de a 3,00 €. Fíjate en su peso: el 1,7 % de la factura. La caché es un ahorro real, no la palanca principal de este sistema.
- La partida que manda es la **entrada**, con el 80,2 % del gasto, porque los documentos recuperados viajan en cada llamada de la traza. Ese es el número que decide si merece la pena recortar de tres documentos a dos, o si el problema es otro.
- `reintentos * 3_600` añade el contexto completo de nuevo en cada reintento. Es el multiplicador que convierte un problema de latencia en un problema de dinero: un reintento que se paga dos veces aparece en las dos métricas.
- `P_ENTRADA`, `P_CACHE` y `P_SALIDA` son números de trabajo para que la aritmética se pueda seguir. Con los precios de tu proveedor la proporción cambia; la estructura (la entrada manda en volumen, la salida en precio unitario) se mantiene en casi todos.
- `1e6` convierte de euros por millón a euros. Si lo quitas, los costes salen un millón de veces mayores y el panel de coste se vuelve absurdo: es el error de unidades más frecuente en este tipo de cuadro de mando.
:::

```python verificable
# Lo que se guarda de una traza: la lista de spans con sus atributos, que es lo que hace
# reproducible un fallo. Sin esto, la misma pregunta da respuestas distintas y no hay caso.
import json

TRAZA = {
    "trace_id": "3f9a1c",
    "consulta": "cuanto tarda el pedido A-4471",
    "version": {"modelo": "abierto-8b-v3", "prompt": "soporte-12", "indice": "docs-2026-10-01"},
    "spans": [
        {"nombre": "recuperar", "ms": 42, "atributos": {"documentos": 3, "tokens": 1260}},
        {"nombre": "modelo", "ms": 1180, "atributos": {"tokens_entrada": 3180,
                                                       "tokens_cache": 1200,
                                                       "tokens_salida": 246}},
        {"nombre": "validar", "ms": 3, "atributos": {"esquema": "respuesta_v2", "valido": True}},
        {"nombre": "reenviar", "ms": 1840, "atributos": {"motivo": "timeout del proveedor"}},
        {"nombre": "modelo", "ms": 1090, "atributos": {"tokens_entrada": 3180,
                                                       "tokens_cache": 1200,
                                                       "tokens_salida": 252}},
    ],
}

P_ENTRADA, P_CACHE, P_SALIDA = 3.00, 0.30, 15.00

def resumen(traza):
    coste = 0.0
    for span in traza["spans"]:
        a = span["atributos"]
        if span["nombre"] == "modelo":
            coste += (a["tokens_entrada"] * P_ENTRADA + a["tokens_cache"] * P_CACHE
                      + a["tokens_salida"] * P_SALIDA) / 1e6
    return {"span_mas_lento": max(traza["spans"], key=lambda s: s["ms"])["nombre"],
            "ms_total": sum(s["ms"] for s in traza["spans"]),
            "llamadas_al_modelo": sum(1 for s in traza["spans"] if s["nombre"] == "modelo"),
            "coste": round(coste, 6)}

resumen_traza = resumen(TRAZA)
print(json.dumps(resumen_traza, ensure_ascii=True, sort_keys=True))
# -> {"coste": 0.02727, "llamadas_al_modelo": 2, "ms_total": 4155, "span_mas_lento": "reenviar"}

# El span mas caro no es el mas lento: por eso hacen falta las dos metricas, no una.
for span in TRAZA["spans"]:
    print(f"{span['nombre']:10s} {span['ms']:5d} ms")
# -> recuperar     42 ms
# -> modelo      1180 ms
# -> validar        3 ms
# -> reenviar    1840 ms
# -> modelo      1090 ms
```

:::claves
- `version` va **dentro** de la traza y no en un fichero aparte. Es el atributo que permite agrupar métricas por versión de modelo, de prompt y de índice: sin él, dos periodos no se pueden comparar aunque el resto de los datos esté perfecto.
- El coste se calcula sumando **todas** las llamadas al modelo de la traza, incluida la del reintento. Una traza con dos llamadas cuesta casi el doble, y ese es el dato que explica por qué subir la tasa de éxito abarata más que bajar el precio del token.
- `max(..., key=lambda s: s["ms"])` devuelve el span más lento, que aquí es `reenviar` (1.840 ms), no el modelo. Es el hallazgo típico: el tiempo se va en la espera del reintento, no en el trabajo. Si solo instrumentas la llamada al modelo, este span no existe y la latencia no cuadra.
- `sort_keys=True` ordena las claves al serializar. Importa para que la salida sea siempre la misma cadena y el comentario `# ->` sea cierto; con diccionarios, el orden de inserción manda y un cambio de orden rompe la comprobación sin que el valor haya cambiado.
- `esquema: respuesta_v2` es un atributo del span de validación. Cuando la tasa de esquemas inválidos sube, lo primero que se mira es qué esquema y qué prompt estaban activos: son los dos únicos sospechosos, y los dos están en la traza.
- Los `trace_id` de este ejemplo son inventados, pero la forma es la de un identificador real: lo que importa es que sea único y que aparezca **en el mismo sitio** de todos los registros, para poder cruzar el log del servidor con la traza del modelo.
:::

## Errores típicos

- **Registrar solo la llamada al modelo.** El tiempo y el dinero de la recuperación, la validación y
  los reintentos quedan invisibles. El span del reintento suele ser el más lento de todos y es el que
  nunca se instrumenta.
- **Guardar el prompt solo cuando algo falla.** Para reproducir un fallo hace falta el prompt exacto,
  los documentos y la versión. Si el registro se escribe después de detectar el problema, ya no
  tienes ninguno de los tres.
- **Mirar la media de latencia y de coste.** La media se la llevan los valores extremos. La mediana
  dice cómo va el caso típico y el p95 cuánto sufre la gente: son dos pantallas distintas, no una.
- **No etiquetar la versión.** Un panel sin versión de modelo, prompt e índice no permite comparar
  nada. Cuando la calidad baja, no sabes si fue el prompt, el modelo o que los documentos cambiaron.
- **Loguear datos personales y secretos.** La traza es un registro que se copia, se envía a un
  servicio externo y se conserva. Todo lo que entre ahí hereda esa exposición: hay que decidir qué se
  guarda, qué se enmascara y cuánto tiempo se retiene, antes de encender el sistema.
- **Definir el éxito como «no hubo excepción».** Un `200 OK` con una respuesta vacía o inventada es
  un éxito técnico y un fallo de producto. La tasa de éxito técnica y la medida de calidad son dos
  métricas distintas y las dos hacen falta.
- **Instrumentar sin poder agregar.** Un registro que se puede leer pero no consultar por versión,
  latencia y coste es un vertedero, no un panel. Antes de escribir la primera traza, decide las tres
  o cuatro dimensiones por las que vas a cortar.

:::aviso
Guardar prompts y respuestas significa guardar **datos de tus usuarios**. Antes de activar el
registro: enmascara identificadores y secretos, limita la retención, restringe el acceso al servicio
de trazas y documenta qué se guarda. Un sistema de observabilidad bien montado es también una copia
de seguridad de todo lo que pasa por tu aplicación, y eso es una responsabilidad legal, no una
decisión técnica.
:::

:::trampa
El error que más caro sale es instrumentar solo en producción. Sin un entorno con trazas completas
donde reproducir un caso, cualquier cambio de prompt se prueba a ciegas y se detecta por el acierto,
es decir, tarde. Las trazas de la fase de pruebas son las que convierten una regresión de calidad en
un caso reproducible.
:::

## Comprueba que lo sabes

:::quiz
p: La latencia mediana de tu asistente es de 2,6 segundos y el p95 de 5,3. Al separar por número de reintentos, casi todas las trazas lentas habían reintentado una vez. ¿Qué haces con ese hallazgo?
o: Subir el tiempo de espera del proveedor, porque está tardando demasiado
o: Bajar la tasa de reintentos, por ejemplo validando o corrigiendo antes de reintentar, porque el reintento está pagando dos veces el mismo contexto
o: Cambiar el modelo por uno más rápido, que es la causa de la latencia
a: 2
e: El p95 se explica por el reintento, que además de duplicar el tiempo vuelve a enviar el contexto completo: es un problema de dinero y de latencia a la vez. Subir el tiempo de espera alarga el peor caso y cambiar de modelo no toca la causa. La pregunta correcta es por qué se reintenta tanto: esquema mal declarado, timeout demasiado bajo o herramientas solapadas.
:::

:::quiz
p: ¿Por qué hay que guardar la versión del prompt y del índice de recuperación dentro de cada traza?
o: Para cumplir con la normativa de auditoría
o: Para poder agrupar las métricas por versión y comparar dos periodos sin atribuir a un cambio lo que hizo otro
o: Para que la traza ocupe menos espacio al comprimirla
a: 2
e: Sin la etiqueta de versión, un cambio de prompt, de modelo y de documentos se mezclan en el mismo número y ninguna mejora se puede atribuir a nada. Con ella, el acierto del prompt 11 y el del prompt 12 se comparan sobre el mismo conjunto de evaluación. La auditoría es un motivo aparte y no tiene que ver con la utilidad diaria del dato.
:::

:::quiz
p: El coste medio por consulta es 0,0146 € y el 5 % más caro de las trazas se lleva el 24 % de la factura. ¿Qué decisión sale de ahí?
o: Ninguna: si la media es baja, el sistema es barato
o: Optimizar la cola: limitar los documentos recuperados por consulta, recortar el contexto de los reintentos y vigilar el p95 de coste, no la media
o: Subir el precio del servicio a todos los clientes para cubrir la cola
a: 2
e: Una factura concentrada en el 5 % de las trazas se controla actuando sobre esas trazas: menos documentos por consulta, contexto acotado y menos reintentos. El coste medio no mueve la aguja porque, por definición, la media esconde la concentración. Subir el precio reparte el problema en vez de resolverlo, y además castiga a los clientes baratos.
:::

:::quiz
p: Un despliegue termina con código de estado correcto en todas las consultas y la tasa de éxito técnica sube al 99 %. ¿Basta eso para saber que el sistema va bien?
o: Sí: si no hay errores, el sistema funciona
o: No: hace falta una medida de calidad ligada a la traza, porque una respuesta válida puede ser incorrecta o inventada
o: No, pero basta con revisar a mano diez respuestas al día
a: 2
e: La tasa de éxito técnica mide que el sistema no se rompió, no que acierte. Un esquema válido con datos inventados pasa todos los controles de infraestructura. Lo que falta es una medida de calidad con su conjunto de evaluación, agrupada por versión y enlazada al identificador de traza para poder abrir el caso concreto cuando el número baja.
:::
