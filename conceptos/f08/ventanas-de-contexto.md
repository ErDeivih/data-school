---
id: ventanas-de-contexto
titulo: Ventana de contexto
fase: 8
nivel: intermedio
rutas: [ds]
prerequisitos: [como-funciona-un-llm, tokenizacion, prompting]
tags: [llm, contexto, memoria, coste]
resumen: Cuantos tokens caben a la vez, por qué lo del medio se olvida y como trocear y ordenar la información para que el modelo la use de verdad.
fuentes: ["Liu et al. (2023), 'Lost in the Middle: How Language Models Use Long Contexts'", "Dai et al. (2019), 'Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context'"]
---

## En una frase

La ventana de contexto es el número máximo de tokens que el modelo puede tener delante a la
vez: lo que no cabe no existe para él, y lo que cabe no se usa igual de bien según dónde esté.

## La idea

Piensa en la ventana de contexto como la superficie de un escritorio. El modelo solo puede
trabajar con los papeles que están encima. Si te traes el archivo entero, la superficie se
llena y ya no cabe nada más; y aunque quepa todo, tener el documento importante
encima del montón no es lo mismo que tenerlo enterrado en el medio.

Tres propiedades que se derivan de esa imagen y que conviene tener claras:

**1. Es una restricción compartida entre entrada y salida.** La ventana es la suma de lo que
envías más lo que el modelo genera, no «cuánto texto puedo enviar». Si tu prompt ocupa
toda la ventana, no hay sitio para la respuesta. Por eso se reserva siempre un margen para la
salida antes de construir el prompt.

**2. El coste crece muy rápido con la longitud.** La autoatención compara cada token con todos
los anteriores: `n` tokens cuestan del orden de `n²` comparaciones. Además, cada token ocupa
memoria en la **caché KV** (las claves y valores que el modelo guarda para no recalcularlos), y
esa memoria se multiplica por las peticiones simultáneas. Un modelo que parece barato con 2.000
tokens puede ser inviable con 128.000 y veinte usuarios a la vez.

**3. La posición importa.** Los modelos usan mejor la información que está al principio y al
final del contexto que la que queda en el medio. El efecto es lo bastante sistemático como para
tener nombre: el problema de «perdido en el medio». No es un fallo del modelo, sino una
consecuencia de cómo se reparte la atención. Y hay una medida que sale gratis y resulta muy
poco intuitiva: **pon la pregunta después de los documentos, no antes**. Muchas veces basta con
reordenar el mismo prompt para pasar de fallar a acertar.

Así se llega a la diferencia entre **ventana anunciada** y **ventana útil**. Que un modelo acepte
200.000 tokens no significa que recupere con precisión un dato enterrado en el token 90.000: la
calidad de la recuperación decae al llenar el contexto, y decae de forma distinta según la
tarea. Encontrar una aguja es más fácil que razonar sobre veinte documentos a la vez.

Que hacer, en orden de rentabilidad:

1. **No meter todo.** Recuperar los fragmentos relevantes y meter solo esos
   ([[rag-arquitectura|RAG]]) gana casi siempre a llenar la ventana. Menos tokens es a la vez
   más barato, más rápido y más preciso.
2. **Ordenar por relevancia y colocar lo importante en los extremos.** Instrucción al
   principio, pregunta al final, y los documentos ordenados de más a menos relevante: así lo
   peor queda en el medio, que es donde el modelo atiende menos.
3. **Resumir el historial en lugar de arrastrarlo.** En una conversación larga, reenviar todos
   los turnos anteriores hace que el coste crezca de forma cuadrática y que las instrucciones
   iniciales se diluyan. Un resumen del estado de la conversación ocupa menos y se relee mejor.
4. **Contar tokens de verdad.** Caracteres divididos entre cuatro es una estimación de andar por
   casa. Con código, cifras o identificadores se queda corta. Usa el tokenizador del modelo.

## Definición formal

Sea `W` el tamaño de la ventana de contexto, medido en tokens. La restricción que se cumple en
cada petición es:

:::formula
tokens(sistema) + tokens(contexto) + tokens(historial) + tokens(pregunta) + tokens(respuesta) ≤ W
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `W` | Tamaño de la ventana: el máximo de tokens a la vez | tokens | Acepta más texto, pero no mejora la recuperación: la ventana útil no crece igual |
| `tokens(historial)` | Los turnos anteriores que reenvías | tokens | El coste crece de forma cuadrática y las instrucciones iniciales se diluyen |
| `tokens(respuesta)` | La reserva para la salida | tokens | Es lo único que **no** puedes recuperar después: si no se reserva, la generación se corta |
| `n` | Tokens de la secuencia en la fórmula de la atención | tokens | El trabajo crece con `n²`: duplicar la longitud multiplica por cuatro las comparaciones |
| `bytes` | Memoria de la caché KV | bytes | Lineal con `n`, pero se multiplica por cada petición simultánea |
| `L` | Número de capas del modelo | capas | Cada capa guarda su propio par de tensores: la caché crece en proporción |
| `H_kv` | Cabezas de clave y valor | cabezas | Con GQA es menor que el número de cabezas de consulta, y la caché baja en la misma proporción |
| `b` | Bytes por valor: 2 en 16 bits, 1 en 8 bits | bytes | Cuantizar a 8 bits divide la caché entre dos, a cambio de precisión |
| `s` | Factor de escala al ampliar la ventana | adimensional | Alargar sin reentrenar degrada la atención en posiciones relativas |
:::

- `W` — el máximo de tokens que el modelo admite **en total**, entrada más salida.
- `tokens(·)` — la cuenta que da el tokenizador del modelo, no una estimación por caracteres.
- `tokens(respuesta)` — la reserva que hay que dejar libre; si no se reserva, la generación se
  corta a mitad.

**Coste de la atención.** Para una secuencia de `n` tokens, la autoatención completa hace del
orden de `n²` comparaciones entre pares de posiciones. Duplicar la longitud del contexto
multiplica por cuatro ese trabajo, y por eso los contextos muy largos se pagan en tiempo y en
dinero.

**Memoria de la caché KV.** El modelo guarda las claves y los valores de todos los tokens ya
procesados para no recalcularlos en cada paso nuevo:

:::formula
bytes ≈ 2 · L · H_kv · d_cabeza · n · b
:::

- `L` — número de capas del modelo.
- `H_kv` — número de cabezas de clave y valor. Con atención multi-cabeza agrupada (GQA), este
  número es menor que el de cabezas de consulta, y esa es precisamente su ventaja: la caché se
  reduce en la misma proporción.
- `d_cabeza` — dimensión de cada cabeza.
- `n` — número de tokens en el contexto.
- `b` — bytes por valor: 2 en precisión de 16 bits, 1 en 8 bits.
- El `2` inicial es porque se guardan **dos** tensores por capa y cabeza: claves y valores.
- Esta memoria es **por secuencia**. Con `k` peticiones simultáneas, se multiplica por `k`.

**Ampliar la ventana.** Cuando un modelo se entrena con una longitud y se quiere usar con otra
mayor, se reescalan las codificaciones posicionales. Con interpolación posicional, se divide la
posición por un factor de escala `s = W_nueva / W_entrenamiento`. Alargar la ventana sin
reentrenar suele degradar la atención en las posiciones relativas, así que la ampliación se
acompaña de un ajuste fino con ejemplos largos.

:::figura
fichero: ventanas-cache-kv-y-coste-cuadratico
pie: A la izquierda, la memoria de la caché KV para un modelo de 32 capas, 8 cabezas de clave y valor, dimensión de cabeza 128 y 16 bits por valor. La línea azul es una sola petición: 2.048 MiB con 32.768 tokens. La roja son 32 peticiones simultáneas: 64 GiB solo de caché, sin contar los pesos del modelo. La banda sombreada es lo que añade la concurrencia, y es la razón de que servir contextos largos a muchos usuarios sea caro aunque el modelo acepte 200.000 tokens. A la derecha, el trabajo de atención en escala logarítmica: la pendiente es 2,00, así que pasar de 4.096 a 32.768 tokens multiplica por 8 la longitud y por 64 las comparaciones.
fuente: figuras/ventanas-de-contexto-1.py
:::

## Ejemplo

**Cuánta memoria ocupa el contexto.** Para un modelo de 32 capas, 8 cabezas de clave y valor,
dimensión de cabeza 128 y precisión de 16 bits:

```
  4096 tokens ->    256.0 MiB por secuencia
  8192 tokens ->    512.0 MiB por secuencia
 32768 tokens ->   2048.0 MiB por secuencia
32 secuencias de 8192 tokens: 16.0 GiB
```

La caché crece linealmente con los tokens, pero se multiplica por la concurrencia. Con 32
peticiones simultáneas de 8.192 tokens ya son 16 GiB solo de caché, sin contar los pesos del
modelo. Ese es el motivo real por el que servir contextos largos a muchos usuarios a la vez es
caro, por mucho que el modelo acepte 200.000 tokens.

**Cuánto ocupa un documento.** Un informe de 40 páginas ronda los 25.000 tokens; si mandas diez
informes así son 250.000 tokens, más de lo que admite casi cualquier modelo corriente. Con 40
documentos de 1.500 tokens cada uno (60.000 tokens) tampoco cabe en una ventana de 32.768: hace
falta seleccionar antes de enviar.

**Seleccionar por presupuesto.** Con 2.000 tokens disponibles para el contexto recuperado y
cinco fragmentos candidatos ordenados por relevancia (950, 400, 1.200, 300 y 600 tokens):

```
elegidos: doc3#12, doc1#04, doc2#09
tokens usados 1650 de 2000  descartados 2
```

Entran los tres mejor puntuados que caben: el fragmento de 1.200 tokens queda fuera porque
después de los dos primeros solo quedaban 650. Fíjate en que la selección no es «los tres
mejores», sino «los mejores que caben». Un fragmento excelente que no cabe no aporta nada, y en su
lugar entran dos mediocres que sí caben.

## Código

```python verificable
# Memoria de la cache KV: 2 (claves y valores) * capas * cabezas * dimension * tokens * bytes
def cache_mib(tokens, capas=32, cabezas=8, dim=128, bytes_por_valor=2):
    return 2 * capas * cabezas * dim * tokens * bytes_por_valor / 1024 ** 2   # 1024**2 pasa de bytes a MiB

for tokens in (4096, 8192, 32768):
    print(f"{tokens:>6} tokens -> {cache_mib(tokens):8.1f} MiB por secuencia")
# -> 256.0, 512.0 y 2048.0 MiB

# Y esa memoria se multiplica por el numero de peticiones simultaneas
print(f"32 secuencias de 8192 tokens: {cache_mib(8192) * 32 / 1024:.1f} GiB")   # -> 16.0 GiB
```

:::claves
- Los valores por defecto de la función (`capas=32`, `cabezas=8`, …) son los del ejemplo: si llamas a `cache_mib(4096)` sin más argumentos, usa esos. Cambiar un solo valor por defecto cambia todas las llamadas siguientes sin avisar.
- `bytes_por_valor=2` es la precisión de 16 bits. Si pones `1` (8 bits), la caché se divide exactamente entre dos: es la palanca más directa para servir contextos largos.
- El `2 *` del principio son **dos tensores** por capa y cabeza: claves y valores. Olvidarlo da la mitad de la memoria real, que es el error más habitual al dimensionar un servidor.
- `/ 1024 ** 2` convierte bytes a **MiB** (potencias de 1024), no a MB (potencias de 1000). La diferencia es del 5 %, y en cifras de decenas de GiB se nota.
- `{tokens:>6}` alinea el número a la derecha en seis caracteres para que las tres líneas queden en columna. Sin el `>6` la salida es correcta pero ilegible.
- La última línea multiplica por 32 **después** de calcular una secuencia: la caché no se comparte entre peticiones. Si en vez de multiplicar sumaras, subestimarías el coste del servicio en un factor de 32.
:::

```python verificable
# Elegir que fragmentos entran en la ventana: los mejor puntuados que quepan en el presupuesto.
fragmentos = [
    ("doc3#12", 950, 0.89),
    ("doc1#04", 400, 0.81),
    ("doc7#01", 1200, 0.77),
    ("doc2#09", 300, 0.74),
    ("doc5#03", 600, 0.70),
]
presupuesto = 2000          # tokens disponibles para el contexto recuperado

elegidos, usado = [], 0     # dos variables de golpe: la lista de elegidos y el contador de tokens
for nombre, tokens, score in sorted(fragmentos, key=lambda f: -f[2]):   # el menos delante ordena de mayor a menor
    if usado + tokens <= presupuesto:    # cabe entero: no se parte un fragmento
        elegidos.append(nombre)
        usado += tokens                  # se acumula para la siguiente decision

print("elegidos:", ", ".join(elegidos))          # -> doc3#12, doc1#04, doc2#09
print(f"tokens usados {usado} de {presupuesto}  descartados {len(fragmentos) - len(elegidos)}")
# -> 1650 de 2000  descartados 2
```

:::claves
- `sorted(fragmentos, key=lambda f: -f[2])` ordena por el tercer campo, la puntuación, con el signo cambiado para que salga de mayor a menor. `sorted` devuelve una **lista nueva**: la lista `fragmentos` original se queda como estaba.
- Cada elemento es una **tupla** `(nombre, tokens, score)` y el `for` la desempaqueta en tres variables. `f[2]` es el `score`; `f[1]` serían los tokens. Cambiar el índice cambia el criterio de orden sin que salte ningún error: es el fallo más silencioso de este bloque.
- La condición es `usado + tokens <= presupuesto`, no `< presupuesto`. Con `<` se perdería el fragmento que encaja justo, y con `<= usado + tokens` el resultado depende del orden.
- Este algoritmo es **voraz**: recorre una sola vez y nunca vuelve atrás. Por eso el fragmento de 1.200 tokens (tercero por puntuación) se queda fuera aunque sea mejor que los dos que entran después: cuando le llega el turno solo quedan 650 tokens.
- `len(fragmentos) - len(elegidos)` cuenta los descartados sin recorrer nada: `elegidos` tiene un elemento por cada fragmento aceptado. Si el bucle pudiera aceptar el mismo fragmento dos veces, esa resta mentiría.
- Cambia `sorted(...)` por `fragmentos` a secas y el resultado cambia por completo: entrarían los fragmentos en el orden del fichero (950, 400, 1200…) y el de 1.200 se colaría por delante de dos que ahora sí entran.
:::

## Errores típicos

- **Confundir la ventana anunciada con la útil.** Que el modelo acepte 128.000 tokens no
  significa que encuentre un dato concreto en el token 100.000 ni que razone bien sobre veinte
  documentos a la vez. Mide la recuperación en tu caso (`¿en qué posición está el dato que
  busco?`) antes de confiar en contextos enormes.
- **Poner la pregunta antes de los documentos.** Es el error de orden más caro y más fácil de
  arreglar. La información del medio del contexto se usa peor: deja los documentos en el centro
  y la pregunta al final, y las instrucciones del sistema al principio.
- **Rellenar la ventana «por si acaso».** Cada token extra cuesta dinero, tarda más y compite por
  la atención con lo que sí importa. Más contexto no es más información: muchas veces es más
  ruido.
- **Truncar por caracteres.** Cortar a 10.000 caracteres no corta a un número fijo de tokens: con
  código o cifras, la misma longitud en caracteres puede duplicar los tokens. Corta con el
  tokenizador del modelo o deja margen de sobra.
- **Ignorar la caché KV al planificar.** La memoria por secuencia se multiplica por la
  concurrencia, y además crece al generar. Un servicio con contextos largos y muchas peticiones
  simultáneas se queda sin memoria mucho antes de lo que sugiere el tamaño del modelo.
- **Creer que el historial completo es memoria.** Reenviar todos los turnos no es recordar: es
  volver a leer. Lo que no quepa se pierde sin aviso, y lo que quepa en medio de una
  conversación larga se usa peor. Resume el estado, guarda los hechos importantes en un sitio
  estructurado y no dependas de que el modelo «se acuerde».

## Comprueba que lo sabes

:::quiz
p: Un modelo admite 32.000 tokens. Envías un prompt de 31.500 tokens. ¿Qué esperas?
o: Que responda con normalidad porque todavía cabe
o: Que la respuesta se corte muy pronto o falle, porque la salida compite por el mismo límite
o: Que el modelo amplíe la ventana automáticamente
a: 2
e: El límite cubre entrada más salida. Si dejas 500 tokens libres, la respuesta se corta en cuanto los agota. Se reserva siempre un margen para la salida antes de construir el prompt.
:::

:::quiz
p: ¿Por qué importa el orden de los documentos dentro del contexto?
o: Porque el modelo los usa mejor al principio y al final que en el medio, así que conviene dejar lo peor en el centro
o: Porque el primero se procesa más rápido que los demás
o: Porque el modelo solo puede leer los tres primeros documentos
a: 1
e: La atención no reparte el peso de forma uniforme: la información del centro del contexto se recupera peor. Ordenar de más a menos relevante deja lo menos útil en la zona de menor atención y la pregunta al final, cerca de la generación.
:::

:::quiz
p: ¿Qué crece al duplicar la longitud del contexto?
o: Solo el coste de almacenar el texto de entrada
o: El trabajo de atención (del orden del cuadrado de la longitud) y la memoria de la caché KV, que se multiplica además por las peticiones simultáneas
o: Nada: el coste depende solo del número de parámetros
a: 2
e: La autoatención compara pares de posiciones, así que su coste crece con el cuadrado de `n`. La caché KV crece de forma lineal con los tokens, pero es memoria por secuencia: con muchas peticiones a la vez, el total se multiplica.
:::

:::trampa
Si tu respuesta correcta está en un documento del centro de un contexto lleno, el modelo puede
fallar aunque el dato esté ahí. Antes de cambiar de modelo o de prompt, prueba a mover ese
documento al principio o al final: es gratis y muchas veces resuelve el problema.
:::
