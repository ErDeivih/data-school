---
id: atencion
titulo: Mecanismos de atención
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [embeddings, rnn-lstm-gru, producto-punto-y-similitud, funciones-de-activacion]
tags: [atencion, secuencias, consultas, transformers]
resumen: En vez de comprimir toda la secuencia en un estado fijo, cada posición consulta a todas las demás y se queda con lo relevante: la idea que desbloqueó los transformers.
fuentes: ["Bahdanau, Cho y Bengio (2015), 'Neural Machine Translation by Jointly Learning to Align and Translate'", "Vaswani et al. (2017), 'Attention Is All You Need'", "Luong, Pham y Manning (2015), 'Effective Approaches to Attention-based Neural Machine Translation'"]
---

## En una frase

La atención es una búsqueda blanda: cada posición formula una pregunta (consulta), la compara
con las etiquetas de todas las posiciones disponibles (claves) y se lleva una mezcla ponderada
de sus contenidos (valores), en vez de depender de un único vector de resumen.

## La idea

Piensa en un traductor secuencia a secuencia de la generación anterior. Un codificador
recurrente lee la frase entera en inglés y produce un estado final `h`. El decodificador empieza
a generar la traducción **solo con ese vector**. Para la frase «The cat that chased the mouse
that stole the cheese was black», ese vector tiene que contener el sujeto, el tiempo verbal, el
género, las dos subordinadas... y no cabe. Lo que se olvida es precisamente la primera palabra,
que es la que decide cómo se traduce el verbo del final.

La atención rompe el cuello de botella con una idea que se entiende sin matemáticas: en vez de
obligar al decodificador a mirar un resumen, deja que **mire todos los estados del codificador**
y que decida en cada paso a cuáles prestar atención. Cuando va a generar «era», mira con fuerza
a «cat» y apenas a «mouse».

La analogía que mejor funciona es la de un buscador. Tienes:

- una **consulta** (*query*): lo que estoy buscando ahora mismo;
- un conjunto de **claves** (*keys*): el índice, una etiqueta por cada elemento disponible;
- un conjunto de **valores** (*values*): el contenido de cada elemento.

El buscador compara la consulta con cada clave y da una puntuación de parecido. Esas
puntuaciones se convierten en pesos que suman 1 (con la función softmax) y el resultado es la
mezcla ponderada de los valores. No hay una decisión dura («usa el elemento 3 y olvida los
demás»): hay una mezcla. Por eso se dice que es **blanda** y por eso es diferenciable, que es lo
que permite entrenarla con descenso de gradiente.

Dos detalles que separan la idea de la implementación que funciona:

1. **El parecido se mide con un producto punto.** No hace falta una red para comparar consulta y
   clave: basta multiplicarlas. Es barato y además se puede calcular para todas las parejas a la
   vez con una única multiplicación de matrices, que es justo lo que una GPU hace rápido.
2. **Hay que dividir por la raíz de la dimensión.** Si no, cuando las dimensiones crecen los
   productos punto crecen y el softmax se satura: un peso vale casi 1, el resto casi 0, y el
   gradiente se muere. Ese `1/√d_k` parece un detalle y es la mitad del truco.

Y una consecuencia que suele sorprender: la atención, tal cual, **no sabe nada del orden**. Si
permutas las posiciones de la entrada, la salida se permuta igual y ningún número cambia. Por eso
los [[transformers]] necesitan codificaciones posicionales: la atención aporta el «quién se
relaciona con quién», y la posición hay que dársela aparte.

## Definición formal

Sean `n` posiciones de consulta y `m` posiciones de clave y valor. Se construyen tres matrices
proyectando la entrada `X` (de forma `n × d_model`):

:::formula
Q = X W_Q ,  K = X W_K ,  V = X W_V
:::

- `X` — la secuencia de entrada, una fila por posición y `d_model` columnas por fila.
- `W_Q`, `W_K` — matrices aprendidas de forma `d_model × d_k`.
- `W_V` — matriz aprendida de forma `d_model × d_v`.
- `Q` — consultas, forma `n × d_k`. `K` — claves, forma `m × d_k`. `V` — valores, forma `m × d_v`.
- `n` — número de posiciones que preguntan; `m` — número de posiciones que responden.
- `d_k` — dimensión de consultas y claves; deben coincidir para poder multiplicarlas.
- `d_v` — dimensión de los valores; puede ser distinta de `d_k`.

**Atención de producto punto escalada** (la que usan los transformers):

:::formula
Atención(Q, K, V) = softmax( Q Kᵀ / √d_k ) V
:::

- `Q Kᵀ` — matriz de puntuaciones de forma `n × m`; la celda `(i, j)` es el producto punto entre
  la consulta `i` y la clave `j`.
- `√d_k` — el escalado. **Por qué:** si las componentes de `q` y `k` son independientes con media
  0 y varianza 1, entonces `q · k = Σᵢ qᵢ kᵢ` tiene media 0 y **varianza `d_k`**, así que su
  desviación típica es `√d_k`. Dividir devuelve las puntuaciones a una escala con desviación
  típica 1, independientemente de la dimensión.
- `softmax` — se aplica **por filas**: cada fila de `n` puntuaciones se convierte en `m` pesos
  positivos que suman 1. La fila `i` dice con qué se queda la consulta `i`.
- `V` — multiplicar los pesos por `V` devuelve una matriz `n × d_v` con la mezcla de valores.

**Atención aditiva** (Bahdanau), para cuando no quieres imponer que las dimensiones coincidan:

:::formula
e_{ij} = vᵀ tanh( W_q q_i + W_k k_j )
:::

- `W_q`, `W_k` — proyectan consulta y clave a una dimensión común.
- `v` — vector aprendido que colapsa el resultado a un único número `e_{ij}`.
- Es más cara (una red pequeña por cada pareja) y hoy se usa poco, pero fue la formulación
  original y funciona mejor con dimensiones pequeñas.

**Multi-cabeza.** En vez de una sola atención sobre `d_model` dimensiones, se hacen `h`
atenciones en paralelo sobre subespacios de tamaño `d_k = d_model / h` y se concatenan:

:::formula
MultiCabeza(X) = Concat(cabeza_1, …, cabeza_h) W_O
:::

- `cabeza_i = Atención(X W_Q^i, X W_K^i, X W_V^i)` — cada cabeza tiene sus propias proyecciones.
- `W_O` — matriz de salida de forma `d_model × d_model`.
- La gracia: cada cabeza puede especializarse en un tipo de relación (una en la sintaxis local,
  otra en la correferencia) porque trabaja en un subespacio distinto.

**Máscaras.** Se suman a las puntuaciones **antes** del softmax, con `−∞` en las posiciones que
se quieren prohibir (un `−∞` se convierte en peso 0 después del softmax):

- **Máscara de relleno:** prohíbe las posiciones de relleno (`padding`), que no son datos.
- **Máscara causal:** prohíbe mirar al futuro (`j > i`). Es la que hace posible generar texto
  token a token sin que el modelo vea lo que todavía no ha escrito.

**Coste.** La matriz de puntuaciones tiene `n · m` entradas por cabeza. El cálculo es
`O(n · m · d_k)` por cabeza y la memoria es `O(n · m)`. Duplicar la longitud de la secuencia
**cuadruplica** la memoria de atención.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Q` | consultas: lo que pregunta cada posición | adimensional | Más filas son más posiciones preguntando y más memoria de puntuaciones; no cambia ningún peso |
| `K` | claves: la etiqueta contra la que se compara cada consulta | adimensional | Más claves son más columnas en la matriz de puntuaciones y más coste, en línea recta |
| `V` | valores: el contenido que se mezcla | adimensional | El resultado tiene su misma anchura `d_v`. Cambiar `d_v` no toca las puntuaciones ni los pesos de atención: solo el tamaño de la salida |
| `W_Q`, `W_K` | proyecciones aprendidas de forma `d_model × d_k` | adimensional | Son parámetros: `2 · d_model · d_k`. Si `d_k` baja (menos cabezas o cabezas más pequeñas) hay menos pesos y puntuaciones menos ricas |
| `W_V` | proyección de los valores | adimensional | `d_model · d_v` parámetros. Es la única de las tres que no influye en el reparto de peso |
| `d_k` | dimensión de consultas y claves | unidades | Es la que obliga a dividir: la desviación típica del producto punto crece con `√d_k`, así que sin escalar el softmax se satura y el gradiente se muere |
| `d_v` | dimensión de los valores | unidades | Solo cambia la anchura de la salida; el coste de la mezcla crece con ella |
| `n` | posiciones que preguntan | posiciones | Multiplica el coste y la memoria de forma lineal en las puntuaciones y cuadrática si crece a la vez que `m`, como en la autoatención |
| `m` | posiciones que responden (claves y valores) | posiciones | Igual que `n`, pero la memoria de la matriz es `n · m` por cabeza: con 2.000 posiciones son 4 millones de números por cabeza y por capa |
| `h` | número de cabezas del multi-cabeza | cabezas | No cambia los parámetros totales (`d_k = d_model / h`), pero multiplica por `h` la memoria de las matrices de puntuaciones y reparte la capacidad en subespacios distintos |
:::

## Ejemplo

Tres posiciones con `d_k = 2`. La consulta es `q = [1, 0]` y las claves son `k₁ = [1, 0]`,
`k₂ = [0, 1]`, `k₃ = [1, 1]`. Las puntuaciones son los productos punto: 1, 0 y 1.

- **Sin escalar:** `softmax([1, 0, 1])` = **[0,4223  0,1554  0,4223]**. Las dos claves con
  puntuación 1 se reparten el 84 % del peso.
- **Escalado con `√d_k = √2 ≈ 1,4142`:** las puntuaciones pasan a 0,7071, 0 y 0,7071.
  `softmax` = **[0,4011  0,1978  0,4011]**.
- Si los valores fueran `v₁ = [1, 0]`, `v₂ = [0, 1]`, `v₃ = [1, 1]`, la salida escalada es
  0,4011 · [1, 0] + 0,1978 · [0, 1] + 0,4011 · [1, 1] = **[0,8022  0,5989]**.

Con `d_k = 2` el escalado cambia poco. Mira lo que pasa con una puntuación realista de `d_k = 64`,
donde la desviación típica de los productos punto es `√64 = 8`. Con puntuaciones `[8, 0, −8]`:

- **Sin escalar:** `softmax([8, 0, −8])` = **[0,9997  0,0003  0,0000]**. Toda la atención en una
  clave: el modelo ha dejado de mezclar y el gradiente respecto a las otras dos es prácticamente
  cero.
- **Escalado con `√64 = 8`:** puntuaciones `[1, 0, −1]`, `softmax` = **[0,6652  0,2447  0,0900]**.
  Sigue habiendo preferencia, pero las tres posiciones reciben señal.

Ese es el motivo exacto del `1/√d_k`: no es una constante de regularización misteriosa, es
devolver la escala que el softmax espera.

:::figura
fichero: atencion-escalado-de-puntuaciones
pie: El panel izquierdo es el caso extremo contado con números: tres claves, puntuaciones 8, 0 y −8, un softmax. Sin dividir, la primera clave se lleva 0,9997 del peso y las otras dos se quedan en 0,0003 y 0,0000. Eso no es «preferir» una clave: es dejar de mezclar. Y como el gradiente de la atención es proporcional al peso, las dos claves ignoradas reciben una señal prácticamente nula y no aprenden nada; el síntoma en la práctica es una pérdida que baja rápido al principio y luego se estanca, y subir o bajar la tasa de aprendizaje no lo arregla. Dividiendo entre √64 = 8 las puntuaciones quedan en 1, 0 y −1 y el reparto pasa a 0,67, 0,24 y 0,09: sigue habiendo preferencia clara, pero las tres posiciones reciben señal. El panel derecho demuestra que el caso de la izquierda no es un ejemplo amañado. Al crecer d_k, los productos punto de vectores aleatorios tienen desviación típica √d_k, así que sin dividir el peso máximo sube con la dimensión hasta pegarse a 1: con 512 dimensiones el modelo atiende a una sola clave de las 256 y las demás son invisibles. Con el escalado, la curva se queda plana cerca de 0,05 en todo el rango. Esa es la diferencia entre un mecanismo que mezcla y uno que solo copia.
fuente: figuras/atencion-1.py
:::

## Código

```python verificable
import numpy as np

def softmax(z):
    # Restar el maximo no cambia el resultado y evita desbordar exp() con puntuaciones grandes.
    # axis=-1 y keepdims=True: el softmax va POR FILAS y la suma conserva la forma (n, 1)
    # para que la division se reparta bien fila a fila.
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)

Q = np.array([[1.0, 0.0]])                     # una consulta
K = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
V = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
d_k = Q.shape[-1]                              # la ultima dimension de Q es d_k, no n

puntos = Q @ K.T            # K.T es (d_k, m): el producto da (n, m), consultas x claves
print("puntuaciones   ", puntos.round(4).tolist())                  # -> [[1.0, 0.0, 1.0]]
print("sin escalar    ", softmax(puntos).round(4).tolist())         # -> [[0.4223, 0.1554, 0.4223]]
pesos = softmax(puntos / np.sqrt(d_k))
print("con escalado   ", pesos.round(4).tolist())                  # -> [[0.4011, 0.1978, 0.4011]]
print("salida         ", (pesos @ V).round(4).tolist())             # -> [[0.8022, 0.5989]]

# Y el caso que rompe el softmax: dimension grande, puntuaciones grandes.
print("d_k=64 crudo   ", softmax(np.array([[8.0, 0.0, -8.0]])).round(4).tolist())
# -> [[0.9997, 0.0003, 0.0]]
print("d_k=64 escalado", softmax(np.array([[8.0, 0.0, -8.0]]) / 8).round(4).tolist())
# -> [[0.6652, 0.2447, 0.09]]
```

:::claves
- `keepdims=True` no es un adorno. Con una sola consulta el array es `(1, 3)` y la suma sin
  `keepdims` es `(1,)`: la división funciona por casualidad. En cuanto metas un lote de `n`
  consultas, la suma tendría forma `(n,)` y `(n, 3) / (n,)` no reparte nada: numpy alinea la
  última dimensión y divides cada columna por un número distinto. `keepdims` deja la suma en
  `(n, 1)` y siempre divide bien.
- `z - z.max(...)` es estabilidad numérica, no una resta inútil: el softmax es invariante a
  sumar una constante, y restar el máximo evita que `exp()` desborde. Con puntuaciones de 800,
  `np.exp(800)` es `inf` y el resultado sale `nan`.
- `K.T` transpone para que `Q @ K.T` dé `(n, m)`: consultas por claves. Si multiplicas al revés
  obtienes la traspuesta, y entonces el softmax reparte el peso de cada **clave** entre las
  consultas en vez de al contrario. No hay ningún error: sale otra cosa.
- `d_k = Q.shape[-1]` toma la **última** dimensión, que es `d_k`. Con `Q.shape[0]` cogerías `n`;
  con una sola consulta vale 1, dividir por `√1` no cambia nada y el ejemplo parece funcionar
  mientras el código está mal.
- `.round(4)` devuelve una **copia** redondeada: `puntos` sigue con todos sus decimales. Y
  `.tolist()` es lo que convierte el array en listas de Python para imprimirlo.
- En la segunda pieza, `(q * k).sum(axis=1)`: `*` es elemento a elemento y `sum(axis=1)` suma
  las `d` componentes de cada fila, que es el producto punto. Con `axis=0` sumarías las 2.000
  muestras entre sí y obtendrías dos números en lugar de 2.000.
:::

```python verificable
import numpy as np

# La varianza del producto punto crece con d_k: de ahi sale el 1/sqrt(d_k).
rng = np.random.default_rng(0)                 # semilla fija: siempre los mismos numeros
for d in (4, 16, 64, 256):
    q = rng.normal(0, 1, (2000, d))            # 2000 consultas de d dimensiones
    k = rng.normal(0, 1, (2000, d))
    # (q * k) es elemento a elemento; .sum(axis=1) es el producto punto de cada fila.
    print(f"d_k={d:>4}  desviacion tipica {float((q * k).sum(axis=1).std()):>5.2f}"
          f"  sqrt(d_k) {np.sqrt(d):>5.2f}")
    # -> 2.04 y 2.00 ; 3.95 y 4.00 ; 8.10 y 8.00 ; 15.80 y 16.00
```

```python ilustrativo
import torch
import torch.nn as nn

# MultiheadAttention ya hace las proyecciones, el escalado, las mascaras y la concatenacion.
atencion = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
# Sin mascara, todas las posiciones se ven entre si (codificador).
salida, pesos = atencion(x, x, x, need_weights=True)

# Mascara causal para el decodificador: cada posicion solo ve las anteriores.
n = x.size(1)
# triu con diagonal=1 deja True por ENCIMA de la diagonal, que es exactamente el futuro.
causal = torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)
salida, _ = atencion(x, x, x, attn_mask=causal)
```

## Errores típicos

- **Olvidar el `1/√d_k`.** Con dimensiones de 64 o más, el softmax se satura, los pesos se van a
  0 o 1 y el gradiente que llega a casi todas las posiciones es ~0. El síntoma típico es una
  pérdida que baja con rapidez y luego se estanca, y culpar a la tasa de aprendizaje no arregla
  nada. En [[transformers]], ese factor está dentro del bloque, pero si lo implementas a mano es
  el primer sitio donde mirar.
- **Aplicar el softmax por el eje equivocado.** La matriz de puntuaciones es `n × m` y el softmax
  va **por filas** (cada consulta reparte su peso entre las claves, suma 1). Si lo aplicas por
  columnas, cada clave reparte su peso entre las consultas y el resultado es otra cosa
  completamente distinta.
- **Meter la máscara multiplicando después del softmax, o confundir las dos máscaras.** Si
  multiplicas después, los pesos ya no suman 1 y la salida queda reescalada: la máscara se suma
  como `−∞` **antes** del softmax. Y hay dos máscaras que sirven para cosas distintas y se usan a
  la vez: la **causal** impide mirar al futuro durante la generación y la de **relleno** ignora
  las posiciones que no son datos reales. Poner solo una produce fuga de información en un caso y
  basura en el otro.
- **Creer que los pesos de atención son una explicación.** Un peso alto significa «esta posición
  se mezcla mucho en este resultado», no «esta posición causó la decisión». Hay cabezas cuyo
  trabajo es copiar el token anterior o ignorar todo; interpretar sus pesos como importancia
  lleva a conclusiones falsas.
- **Ignorar el coste cuadrático.** Pasar de 2.000 a 4.000 posiciones multiplica por cuatro la
  memoria de la matriz de atención de cada cabeza y de cada capa. Antes de subir la longitud,
  calcula: `n² · h · 4` bytes por capa en float32 es la cuenta mínima.
- **Usar atención sin información posicional y esperar que entienda el orden.** La atención es
  equivariante a permutaciones: sin posición, «el perro muerde al hombre» y «el hombre muerde al
  perro» le dan exactamente el mismo resultado agregado.

:::practica
enunciado: Con d_k = 2, la consulta q = [2, 0] y las claves k₁ = [1, 0], k₂ = [0, 1], k₃ = [1, 1]. Con los valores v₁ = [1, 0], v₂ = [0, 1] y v₃ = [1, 1], calcula los pesos de atención escalados y el vector de salida.
pista: Puntúa con el producto punto, divide entre √d_k = 1,4142 y pasa las tres puntuaciones por el softmax.
solucion: Las puntuaciones son 2, 0 y 2; escaladas quedan 1,4142, 0 y 1,4142. Las exponenciales son 4,1132, 1 y 4,1132, que suman 9,2264: los pesos son 0,4458, 0,1084 y 0,4458. La salida es 0,4458 · [1, 0] + 0,1084 · [0, 1] + 0,4458 · [1, 1] = [0,8916, 0,5542]. La clave con puntuación 0 conserva el 11 % del peso: el softmax no descarta del todo.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Para qué sirve exactamente dividir las puntuaciones entre √d_k?
o: Para que los pesos de atención sumen 1 después del softmax
o: Para devolver las puntuaciones a una desviación típica cercana a 1, porque el producto punto de vectores aleatorios de dimensión d_k tiene varianza d_k
o: Para reducir el número de parámetros de las proyecciones
a: 2
e: El softmax ya normaliza las filas por sí solo, así que los pesos suman 1 lo dividas o no. La división controla la escala de entrada al softmax: con puntuaciones de desviación típica 8 el softmax se satura (un peso 0,9997) y el gradiente desaparece. Los parámetros de W_Q, W_K y W_V no cambian con este factor.
:::

:::quiz
p: ¿Cuál es la diferencia entre aplicar la máscara antes y después del softmax?
o: Antes con −∞ hace que la posición reciba peso exactamente 0 y las filas sigan sumando 1; después, los pesos ya calculados quedan reescalados y la salida sale mal
o: Es equivalente, solo cambia el orden de las operaciones
o: Antes solo funciona con la máscara causal y después solo con la de relleno
a: 1
e: El softmax normaliza dividiendo entre la suma de las exponenciales. Si pones la máscara después, la fila ya está normalizada y al anular términos la suma baja de 1: estás reescalando la mezcla. Sumando −∞ antes, la exponencial de esa posición es 0 y el softmax reparte el peso solo entre las permitidas.
:::

:::quiz
p: ¿Por qué la atención sola no distingue «el perro muerde al hombre» de «el hombre muerde al perro»?
o: Porque el vocabulario es el mismo en las dos frases
o: Porque la operación es equivariante a permutaciones: reordenar las posiciones reordena la salida sin cambiar ningún número
o: Porque el softmax borra el orden al normalizar
a: 2
e: Las puntuaciones son productos punto entre pares de posiciones y la suma de valores no depende del orden en que se recorra. Necesitas información posicional explícita, ya sea sumada a las entradas (codificación sinusoidal) o inyectada en las proyecciones (RoPE), para que el orden entre en juego.
:::

:::trampa
Si tu modelo con atención da una pérdida sospechosamente baja en entrenamiento y mucho peor en
validación, revisa las máscaras antes que nada. Una máscara causal ausente o mal construida hacia
el lado equivocado deja al modelo leer el token que tiene que predecir, y eso se ve exactamente
como un modelo que aprende perfecto y no generaliza nada.
:::
