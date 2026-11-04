---
id: transformers
titulo: Transformers
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [atencion, embeddings, normalizacion-por-lotes, retropropagacion, tokenizacion]
tags: [transformers, atencion, arquitectura, secuencias]
resumen: Autoatención multi-cabeza, sin recurrencia y en paralelo: el bloque que compone casi todos los modelos de lenguaje actuales, con su coste y sus límites.
fuentes: ["Vaswani et al. (2017), 'Attention Is All You Need'", "Xiong et al. (2020), 'On Layer Normalization in the Transformer Architecture'", "Su et al. (2021), 'RoFormer: Enhanced Transformer with Rotary Position Embedding'"]
---

## En una frase

Un transformer es una pila de bloques idénticos donde cada posición se reconstruye mirando a
todas las demás con [[atencion|atención multi-cabeza]], sin recurrencia y sin convolución: toda
la secuencia se procesa a la vez y el orden se inyecta aparte, con codificaciones posicionales.

## La idea

La [[rnn-lstm-gru|recurrencia]] tiene un problema estructural además del gradiente: es
**secuencial por naturaleza**. Para calcular el estado de la palabra 50 necesitas el de la 49,
que necesita el de la 48. Por muchas GPU que pongas, no puedes calcular las 50 a la vez. El
trabajo es en cadena.

El transformer ataca justo eso. En un bloque transformer, **todas las posiciones se calculan
simultáneamente**: la palabra 50 mira a la 1 directamente, sin pasar por las 49 intermedias.
Esa es la razón por la que el modelo se puede entrenar con secuencias larguísimas y por la que
aprovecha las GPU, que están hechas para multiplicar matrices grandes.

¿Y cómo sustituye la recurrencia sin perder el orden? Con dos piezas:

1. **Autoatención multi-cabeza.** Cada posición produce una consulta y compara con las claves de
   todas las posiciones, incluidas las de delante y las de detrás. Así la palabra «era» puede
   recoger información de «gato» aunque esté a nueve posiciones. Y como hay varias cabezas, cada
   una puede especializarse: una mira la palabra anterior, otra busca el sujeto, otra la
   puntuación.
2. **Una red hacia delante por posición.** Después de mezclar información entre posiciones, cada
   posición pasa por la misma red de dos capas, aplicada **de forma independiente** a cada una.
   Aquí es donde el modelo transforma la información que ha recogido; la atención solo la mueve.

Eso es todo el bloque, y el modelo es ese bloque repetido 12, 24, 96 veces. Dentro, lo único que
cambia entre capas son los pesos.

Hay un matiz de diseño que conviene entender porque explica por qué los transformers modernos
son más fáciles de entrenar: **dónde va la normalización**. En el artículo original iba *después*
de sumar la conexión residual (post-LN) y eso obligaba a un calentamiento lento de la tasa de
aprendizaje para no explotar. Poniéndola *antes* de cada subcapa (pre-LN) el entrenamiento es
mucho más estable y permite tasas más altas, y es lo que se usa hoy. Las dos versiones se ven en
código, así que hay que saber reconocerlas.

Y una advertencia sobre la fama: el transformer no es mágico. Sin datos suficientes, una red
recurrente bien ajustada compite con él en secuencias cortas. Su ventaja aparece cuando hay
muchos datos y secuencias largas; su precio es que **la atención crece con el cuadrado de la
longitud**.

## Definición formal

Un bloque transformer recibe una matriz `X` de forma `n × d_model`: `n` posiciones (tokens), cada
una un vector de `d_model` números. Versión **pre-LN**, la habitual hoy:

:::formula
Z = X + MultiCabeza(LN(X)) ,  Y = Z + FFN(LN(Z))
:::

- `LN` — normalización por capa: [[normalizacion-por-lotes|LayerNorm]]. Normaliza cada fila por
  separado (media 0 y varianza 1 sobre las `d_model` componentes) y aplica una escala y un sesgo
  aprendidos. Se usa LayerNorm y no BatchNorm porque no depende del lote: cada posición se
  normaliza con sus propios números.
- `X + …` — conexión residual. Suma la entrada a la salida de la subcapa para que el gradiente
  tenga un camino directo y no tenga que atravesar toda la transformación.
- `MultiCabeza(·)` — la [[atencion|atención multi-cabeza]] con `h` cabezas de tamaño
  `d_k = d_model / h`, concatenadas y proyectadas con `W_O`.
- `FFN` — red hacia delante aplicada a cada posición de forma independiente.
- `Y` — salida del bloque, misma forma `n × d_model` que la entrada. Por eso se pueden apilar.

La **red hacia delante** (FFN) es una expansión y una contracción:

:::formula
FFN(z) = W₂ · GELU(W₁ z + b₁) + b₂
:::

- `z` — una fila de `Z`, de tamaño `d_model`.
- `W₁` — matriz de forma `d_ff × d_model`; `W₂` — de forma `d_model × d_ff`.
- `d_ff` — dimensión interna, típicamente `4 · d_model` (2.048 cuando `d_model` es 512).
- `GELU` — activación suave parecida a ReLU, definida para la documentación como
  `GELU(x) = x · Φ(x)`, con `Φ` la función de distribución de la normal estándar.

**Codificación posicional.** Como la atención es equivariante a permutaciones, hay que dar la
posición explícitamente. La versión sinusoidal del artículo original suma a cada embedding:

:::formula
PE(pos, 2i) = sin( pos / 10000^(2i/d_model) ) ,  PE(pos, 2i+1) = cos( pos / 10000^(2i/d_model) )
:::

- `pos` — la posición en la secuencia (0, 1, 2, …).
- `i` — el índice de la pareja de dimensiones (0 ≤ i < d_model/2).
- Frecuencias distintas por dimensión: las primeras oscilan rápido y distinguen posiciones
  vecinas, las últimas oscilan despacio y codifican la posición absoluta.
- Alternativas habituales en modelos modernos: posiciones aprendidas (GPT-2 original) y **RoPE**,
  que rota las consultas y las claves un ángulo proporcional a la posición en lugar de sumar
  nada a la entrada.

**Máscara causal.** En un decodificador que genera texto, la puntuación de la posición `i`
contra la `j` se prohíbe cuando `j > i`. Se implementa sumando `−∞` antes del softmax.

**Contabilidad.** Parámetros de un bloque: `4 · d_model²` en la atención (las cuatro matrices
`W_Q`, `W_K`, `W_V`, `W_O`), `2 · d_model · d_ff` en la FFN y `4 · d_model` en los dos LayerNorm.
Coste de cálculo por capa: `O(n² · d_model)` la atención y `O(n · d_model · d_ff)` la FFN, con
`2` delante de cada uno si se cuentan multiplicaciones y sumas por separado.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | número de tokens de la secuencia | tokens | Es la variable cara: la atención crece con `n²` en coste y en memoria, y la FFN solo con `n`. Duplicar el contexto cuadruplica las matrices de atención de cada cabeza y cada capa |
| `d_model` | anchura del vector de cada posición | unidades | Sube el coste de todo y los parámetros del bloque con `d_model²` en la atención y `d_model · d_ff` en la FFN. Es la palanca de capacidad, no la de contexto |
| `h` | número de cabezas | cabezas | Con `d_model` fijo no cambia los parámetros (`d_k = d_model / h`), pero multiplica por `h` la memoria de las matrices de puntuaciones. Menos cabezas y más grandes es más barato en memoria |
| `d_k` | dimensión de cada cabeza: `d_model / h` | unidades | Si baja, cada cabeza compara menos matices y el coste por cabeza baja; si sube, las puntuaciones crecen con `√d_k` y el escalado se vuelve más crítico |
| `d_ff` | dimensión interna de la FFN | unidades | Fija los parámetros de la FFN (`2 · d_model · d_ff`) y el punto donde la FFN deja de mandar: el cruce con la atención está exactamente en `n = d_ff` |
| `W_Q`, `W_K`, `W_V`, `W_O` | las cuatro matrices de la atención multi-cabeza | adimensional | Son `4 · d_model²` parámetros, la mitad del bloque. No dependen de `n`: los mismos pesos procesan 10 tokens o 10.000 |
| `W₁`, `W₂` | las dos matrices de la FFN | adimensional | `2 · d_model · d_ff` parámetros, la otra mitad del bloque. Aquí es donde el modelo transforma lo que la atención solo mueve |
| `pos` | posición del token en la secuencia | índice | Con la codificación sinusoidal cambia la frecuencia de cada dimensión; no añade parámetros, pero sin ella el modelo es ciego al orden |
| `LN` | normalización por capa, por posición | adimensional | Normaliza cada fila por separado, así que no depende del tamaño del lote. Puesta antes de cada subcapa (pre-LN) el entrenamiento es estable con tasas altas |
:::

## Ejemplo

`d_model = 512`, `h = 8` cabezas y `d_ff = 2048`:

- Dimensión de cada cabeza: 512 / 8 = **64**.
- Parámetros de atención: 4 · 512² = **1.048.576**.
- Parámetros de la FFN: 2 · 512 · 2048 = **2.097.152**.
- LayerNorm: 2 · 2 · 512 = **2.048**.
- Total del bloque: **3.147.776**. Un modelo de 12 bloques tiene unos 37,8 millones de
  parámetros en los bloques, más los embeddings y la capa de salida.

**Cuándo manda cada subcapa.** Con `2n²d` para la atención y `2n·d·d_ff` para la FFN, se igualan
cuando `n = d_ff = 2048`:

- Con `n = 512`: atención 2·512²·512 = 0,27 GFLOP, FFN 2·512·512·2048 = 1,07 GFLOP. Manda la FFN.
- Con `n = 2048`: las dos cuestan 4,3 GFLOP.
- Con `n = 8192`: atención 68,7 GFLOP, FFN 17,2 GFLOP. Manda la atención, y por goleada.

**Memoria de la matriz de atención**, con 8 cabezas y float32 (4 bytes por número), por capa:
`8 · n² · 4` bytes. Con `n = 512` son 8 MiB; con 1.024, 32 MiB; con 2.048, 128 MiB. Y eso **por
capa**: con 24 capas y 2.048 tokens, 3 GB solo en matrices de atención.

:::figura
fichero: transformers-coste-y-memoria
pie: Los dos paneles cuentan la misma propiedad desde dos sitios distintos: la atención crece con el cuadrado de la longitud. A la izquierda están las dos subcapas del bloque enfrentadas. La red hacia delante sube en línea recta con n y la atención sube en parábola, así que hay un punto donde se cruzan y ese punto es exactamente n = d_ff = 2.048: por debajo, la mayor parte del cálculo está en la FFN; por encima, la atención se come el presupuesto y con 16.384 tokens cuesta cien veces más. Traducido a decisiones: si tus secuencias son cortas, optimizar la FFN tiene sentido; si son largas, el problema es la atención y la solución pasa por ventanas, dispersión o aproximaciones, no por tocar la FFN. A la derecha está el precio que no se ve en los FLOP: la memoria de las matrices de puntuaciones, que también va con n². Cada punto de la curva azul es una capa (8 MiB con 512 tokens, 32 con 1.024, 128 con 2.048) y la curva roja es el total del modelo de 24 capas, que llega a 3 GB con 2.048 tokens solo para guardar esos pesos intermedios de la pasada hacia delante. Ese es el motivo real de que subir el contexto sea caro y de que existan las técnicas de atención eficiente: no es el número de parámetros, que no cambia con la longitud, es todo lo que hay que retener en memoria.
fuente: figuras/transformers-1.py
:::

## Código

```python verificable
import numpy as np

def softmax(z, axis=-1):
    e = np.exp(z - z.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

rng = np.random.default_rng(0)
n, d_model = 4, 6
X = rng.normal(0, 1, (n, d_model))
# Esto es un GENERADOR, no una lista: el desempaquetado lo recorre tres veces y se agota.
Wq, Wk, Wv = (rng.normal(0, 0.5, (d_model, d_model)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv

# Mascara causal: -infinito por encima de la diagonal, antes del softmax.
# k=1 salta la diagonal principal: cada token SI puede mirarse a si mismo.
causal = np.triu(np.full((n, n), -np.inf), k=1)
# Aqui d_model hace de d_k porque las proyecciones son cuadradas; con varias cabezas el
# divisor seria d_k = d_model / h.
pesos = softmax(Q @ K.T / np.sqrt(d_model) + causal)
print(pesos.round(3).tolist())
# -> [[1.0, 0.0, 0.0, 0.0], [0.475, 0.525, 0.0, 0.0],
#     [0.198, 0.369, 0.433, 0.0], [0.217, 0.299, 0.347, 0.136]]
# Si cada fila suma 1, la mascara se aplico antes del softmax y no lo descompenso.
print("cada fila suma:", pesos.sum(axis=1).round(3).tolist())   # -> [1.0, 1.0, 1.0, 1.0]
```

:::claves
- `Wq, Wk, Wv = (rng.normal(...) for _ in range(3))` funciona porque el desempaquetado consume
  el generador justo tres veces. No es una lista: si guardas el generador en una variable y
  luego intentas `matrices[0]`, falla. Y si lo recorrieras dos veces, la segunda vendría vacío.
- La máscara se **suma antes** del softmax y vale `-np.inf`, no un número muy negativo. Sumada
  después, la fila ya está normalizada y anular términos la deja por debajo de 1: la mezcla sale
  reescalada. Y `np.triu(..., k=1)` empieza en la diagonal de arriba, así que la diagonal
  principal queda a 0: cada token sí puede mirarse a sí mismo.
- `pesos.sum(axis=1)` es la comprobación barata de que la máscara está en su sitio: con `-inf`
  dentro del softmax cada fila suma exactamente 1. Si te sale menos de 1, la has aplicado tarde.
- `np.sqrt(d_model)` hace aquí de `√d_k` porque las proyecciones del ejemplo son cuadradas
  (`d_model × d_model`). En un bloque con `h` cabezas el divisor es `d_k = d_model / h`, y ese
  es el error clásico al copiar este bloque a un modelo de verdad.
- `pesos.round(3)` devuelve una **copia** redondeada: `pesos` conserva todos sus decimales y
  sigue sumando 1 exacto. `.tolist()` solo cambia el formato de impresión.
- En la segunda pieza, `d_model // h` es división entera. Si `d_model` no es divisible entre `h`,
  se queda con la parte de abajo y las cabezas no cubren `d_model`: obtienes un aviso o un
  resultado silenciosamente mal. Y `2**20` son los bytes de un mebibyte (1.048.576), no un
  millón: con `/ 1e6` los mismos números saldrían un 5 % más grandes.
:::

```python verificable
# Contabilidad de un bloque transformer con d_model=512, 8 cabezas y d_ff=2048.
d_model, h, d_ff = 512, 8, 2048
qkvo = 4 * d_model * d_model        # W_Q, W_K, W_V y W_O
ffn = 2 * d_model * d_ff           # las dos lineales de la red hacia delante
normas = 2 * 2 * d_model           # dos LayerNorm, cada uno con escala y sesgo
# // es division entera: la dimension de cada cabeza tiene que ser exacta.
print("d_k por cabeza:", d_model // h)          # -> 64
print("atencion      :", qkvo)                  # -> 1048576
print("FFN           :", ffn)                   # -> 2097152
print("bloque entero :", qkvo + ffn + normas)   # -> 3147776

# Atencion y FFN cuestan lo mismo cuando n = d_ff.
print("n de cruce    :", d_ff)                  # -> 2048

# Memoria de la matriz de atencion, 8 cabezas, float32, por capa.
# 2**20 es un mebibyte en bytes (1.048.576); con 1e6 los numeros salen un 5 % mayores.
print(f"n= 512: {8 * 512 * 512 * 4 / 2**20:>6.1f} MiB")     # ->    8.0 MiB
print(f"n=1024: {8 * 1024 * 1024 * 4 / 2**20:>6.1f} MiB")   # ->   32.0 MiB
print(f"n=2048: {8 * 2048 * 2048 * 4 / 2**20:>6.1f} MiB")   # ->  128.0 MiB
```

```python ilustrativo
import torch
import torch.nn as nn

# Pre-LN: norm_first=True. Es la version estable y la que se usa hoy.
capa = nn.TransformerEncoderLayer(
    d_model=512, nhead=8, dim_feedforward=2048,
    activation="gelu", dropout=0.1, norm_first=True, batch_first=True,
)
codificador = nn.TransformerEncoder(capa, num_layers=12)

# La codificacion posicional se suma a los embeddings antes del primer bloque.
x = embeddings(tokens) + posicional[: tokens.size(1)]
salida = codificador(x, src_key_padding_mask=mascara_de_relleno)
```

## Errores típicos

- **Olvidar las codificaciones posicionales.** Sin ellas el modelo es invariante a
  permutaciones: «el perro muerde al hombre» y «el hombre muerde al perro» producen el mismo
  resultado agregado. Es el fallo más tonto y el más difícil de detectar, porque el modelo
  entrena, baja la pérdida y aprende algo peor de lo que debería sin dar ningún error.
- **Confundir la máscara causal con la de relleno.** La causal prohíbe mirar al futuro y solo se
  aplica cuando se genera; la de relleno ignora los tokens que no son datos. En un decodificador
  van las dos. Si te falta la causal, el modelo ve la respuesta y la pérdida de entrenamiento se
  vuelve sospechosamente baja mientras la validación no mejora.
- **Poner LayerNorm en el sitio equivocado y culpar a la inicialización.** Post-LN (el original)
  necesita calentamiento y es inestable con tasas altas; pre-LN es estable. Si copias un bloque
  post-LN y le pones una tasa alta sin calentamiento, la pérdida se va a NaN y el problema no son
  los pesos iniciales.
- **Aumentar el contexto sin mirar la memoria, y creer que más parámetros dan más contexto.** La
  atención escala con `n²` por cabeza y por capa: duplicar la longitud cuadruplica esa memoria.
  Antes de subir el contexto, calcula `h · n² · 4` bytes por capa y multiplícalo por el número de
  capas. Y recuerda que el número de parámetros no depende de la longitud de la entrada: los
  mismos pesos procesan 10 tokens o 10.000. Lo que cambia con la longitud es el coste, no el
  tamaño del modelo.
- **Esperar que gane a todo con pocos datos.** Con un conjunto de entrenamiento pequeño y
  secuencias cortas, una [[rnn-lstm-gru|LSTM o una GRU]] bien ajustadas compiten con un
  transformer de tamaño comparable y necesitan menos datos. Y sin aumento de datos ni
  regularización, un transformer grande cae en [[sobreajuste-en-redes|sobreajuste]] con facilidad.
- **Interpretar los pesos de atención como explicaciones.** Cada cabeza hace un trabajo distinto
  y muchas son casi redundantes o copian la posición anterior. Los pesos son pesos de mezcla, no
  importancias causales; si necesitas atribución, usa un método pensado para eso y valídalo.

:::practica
enunciado: Un transformer con d_model = 768, 12 cabezas, d_ff = 3072 y 12 bloques. ¿Cuántos parámetros tiene un bloque y cuántos suman los doce? Cuenta la atención (4 · d_model²), la FFN (2 · d_model · d_ff) y los dos LayerNorm.
pista: El número de parámetros de la atención no depende de las cabezas: las cuatro matrices siguen siendo de 768×768.
solucion: Atención 4 · 768² = 2.359.296; FFN 2 · 768 · 3072 = 4.718.592; LayerNorm 4 · 768 = 3.072. Cada bloque suma 7.080.960, unos 7,08 millones, y los 12 bloques 84.971.520, unos 85 millones, sin contar embeddings ni capa de salida. Las 12 cabezas bajan d_k a 64 y reducen el coste, no los pesos.
:::

## Comprueba que lo sabes

:::quiz
p: Con d_model = 512 y d_ff = 2048, ¿a partir de qué longitud de secuencia la atención cuesta más que la red hacia delante?
o: A partir de 512 tokens, porque es d_model
o: A partir de 2048 tokens, porque con 2n²d y 2n·d·d_ff el coste se iguala cuando n = d_ff
o: Nunca: la FFN siempre cuesta más porque tiene más parámetros
a: 2
e: 2n²d = 2n·d·d_ff se simplifica a n = d_ff = 2048. Por debajo, la FFN domina porque el término lineal en n es mayor; por encima, el término n² de la atención la supera rápidamente. Con n = 8192 la atención cuesta cuatro veces más que la FFN.
:::

:::quiz
p: ¿Por qué un transformer necesita codificaciones posicionales y una RNN no?
o: Porque el transformer procesa todas las posiciones a la vez y la atención es equivariante a permutaciones; la recurrencia ya lleva el orden en su propia secuencia de pasos
o: Porque el transformer no tiene sesgos y la RNN sí
o: Porque el softmax de la atención borra las posiciones al normalizar
a: 1
e: La recurrencia aplica la celda paso a paso, así que el orden está en la estructura del cálculo. La atención compara pares y suma valores, operaciones que no cambian si reordenas las posiciones: reordenar la entrada reordena la salida y nada más. La información posicional hay que añadirla (sumando una codificación o rotando consultas y claves).
:::

:::quiz
p: ¿Para qué sirve la conexión residual X + Subcapa(LN(X))?
o: Para duplicar el número de parámetros del bloque
o: Para que el gradiente tenga un camino directo hasta las capas anteriores y el bloque solo tenga que aprender la corrección
o: Para normalizar la salida del bloque antes de pasarla al siguiente
a: 2
e: La suma crea una identidad por la que el gradiente fluye sin atravesar la subcapa, así que una capa puede quedarse cerca de la identidad si no aporta nada. Es la misma idea que en las CNN profundas. No añade parámetros y no normaliza: de eso se encarga LayerNorm, que va antes de la subcapa en la variante pre-LN.
:::

:::aviso
Un transformer grande sobre pocos datos es la forma más rápida de obtener un modelo que parece
perfecto en entrenamiento. Si tu pérdida de entrenamiento baja a valores muy bajos mientras la de
validación deja de bajar, no añadas capas: añade datos, regularización y
[[dropout-y-regularizacion|dropout]], y comprueba que la máscara causal está donde debe.
:::
