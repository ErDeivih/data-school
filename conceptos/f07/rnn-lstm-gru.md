---
id: rnn-lstm-gru
titulo: RNN, LSTM y GRU
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [perceptron-y-mlp, retropropagacion, funciones-de-activacion, regla-de-la-cadena]
tags: [secuencias, recurrencia, puertas, gradiente]
resumen: Una red que se pasa su propio estado de un paso al siguiente, y las puertas que añaden LSTM y GRU para que el gradiente no se desvanezca por el camino.
fuentes: ["Rumelhart, Hinton y Williams (1986), 'Learning Representations by Back-Propagating Errors'", "Hochreiter y Schmidhuber (1997), 'Long Short-Term Memory'", "Cho et al. (2014), 'Learning Phrase Representations using RNN Encoder-Decoder'"]
---

## En una frase

Una red recurrente lee la secuencia elemento a elemento y va arrastrando un estado —un vector de
memoria— que resume lo leído hasta ahora; LSTM y GRU añaden puertas que deciden qué olvidar y
qué guardar para que esa memoria aguante muchos pasos.

## La idea

Lee esta frase: «El gato que perseguía el ratón que había robado el queso era negro». Para
saber que el sujeto de «era» es el gato y no el ratón, tienes que recordar la primera palabra
después de nueve. Una red hacia delante normal, con una ventana fija de palabras, no puede
hacerlo: o le das toda la frase de golpe (y entonces la longitud es fija y el número de
parámetros se dispara con ella) o pierdes la información.

La solución recurrente es sencilla de contar: lee la frase palabra a palabra y mantén un
cuaderno. Al llegar a la palabra `t`, miras la palabra y el cuaderno, escribes un cuaderno
nuevo y produces una salida. El cuaderno es el **estado oculto** `h_t`. Las tres claves son:

1. **Los pesos son los mismos en todos los pasos.** La celda que procesa la palabra 1 es
   exactamente la misma que procesa la palabra 20. Por eso la red funciona con frases de
   cualquier longitud y no crece en parámetros.
2. **El estado es un vector de tamaño fijo.** No es una cinta infinita: es un resumen con
   pérdida. Cuanto más largo el texto, más se olvida del principio.
3. **El entrenamiento es una red muy profunda con pesos atados.** Al desplegar la recurrencia
   en el tiempo, 50 palabras son 50 capas, todas con la misma matriz. Y ahí está el problema.

Ese problema es el **gradiente que se desvanece**. Al retropropagar por el tiempo, el gradiente
de la pérdida respecto al estado inicial es un producto de 50 factores, uno por paso. Si cada
factor vale 0,25, el producto es 7,9 · 10⁻³¹: el estado inicial no recibe ninguna señal y la red
no puede aprender dependencias largas. Si cada factor vale 1,5, el producto es 6,4 · 10⁸ y el
entrenamiento explota. Solo cuando el factor ronda 1 sobrevive la información.

La LSTM (1997) resuelve esto con una idea concreta: además del estado oculto, mantiene un
**estado de celda** `c_t` que se actualiza **sumando**, no multiplicando por una matriz. Esa
suma crea una autopista por la que el gradiente viaja sin multiplicarse por `W_h` en cada paso.
Las **puertas** son capas con activación sigmoide que producen números entre 0 y 1 y deciden
cuánto dejar pasar: qué olvidar del estado anterior, qué escribir de la entrada nueva y qué
sacar hacia fuera. La GRU (2014) simplifica: fusiona el estado de celda con el oculto y usa tres
juegos de matrices en vez de cuatro, con un rendimiento parecido en la práctica.

## Definición formal

**Celda recurrente simple.** Con entrada `x_t ∈ ℝ^d`, estado `h_t ∈ ℝ^m` y sesgo `b_h`:

:::formula
h_t = tanh(W_x x_t + W_h h_{t−1} + b_h) ,  ŷ_t = softmax(W_y h_t + b_y)
:::

- `x_t` — vector de entrada en el paso `t` (por ejemplo, el [[embeddings|embedding]] del token).
- `h_t` — estado oculto en `t`; resume la secuencia hasta `t`. También es la salida de la celda.
- `W_x` — matriz de pesos entrada → estado, de forma `d × m`.
- `W_h` — matriz recurrente estado → estado, de forma `m × m`. **Es la misma en todos los pasos.**
- `b_h` — sesgo del estado, de tamaño `m`.
- `h_0` — estado inicial, normalmente el vector de ceros.
- `tanh` — [[funciones-de-activacion|tangente hiperbólica]], que acota la salida a (−1, 1).
- `W_y`, `b_y` — capa de salida que convierte el estado en predicción.

**LSTM.** Cuatro puertas, todas con activación `σ` (sigmoide, que devuelve valores en (0, 1)) y
`⊙` el producto elemento a elemento:

:::formula
f_t = σ(W_f [h_{t−1}, x_t] + b_f)      i_t = σ(W_i [h_{t−1}, x_t] + b_i)
g_t = tanh(W_g [h_{t−1}, x_t] + b_g)   o_t = σ(W_o [h_{t−1}, x_t] + b_o)
c_t = f_t ⊙ c_{t−1} + i_t ⊙ g_t        h_t = o_t ⊙ tanh(c_t)
:::

- `f_t` — puerta de olvido: cuánto del estado de celda anterior se conserva.
- `i_t` — puerta de entrada: cuánto del candidato se escribe.
- `g_t` — candidato: la información nueva, en el rango (−1, 1).
- `o_t` — puerta de salida: cuánto del estado de celda se expone como estado oculto.
- `c_t` — estado de celda, el que se actualiza con una suma. Es la autopista del gradiente.
- `[h_{t−1}, x_t]` — concatenación de los dos vectores.

**GRU.** Dos puertas y sin estado de celda separado:

:::formula
z_t = σ(W_z [h_{t−1}, x_t] + b_z)   r_t = σ(W_r [h_{t−1}, x_t] + b_r)
h_t = (1 − z_t) ⊙ h_{t−1} + z_t ⊙ tanh(W [r_t ⊙ h_{t−1}, x_t] + b)
:::

- `z_t` — puerta de actualización: cuánto se reemplaza el estado anterior.
- `r_t` — puerta de reinicio: cuánto del estado anterior se tiene en cuenta para proponer el
  candidato. `(1 − z_t)` es la parte que se conserva tal cual.
- `b_z`, `b_r`, `b` — los tres sesgos de la celda, de tamaño `m`. Son los que hacen que la cuenta
  de parámetros sea `3 · ((d + m) · m + m)` y no `3 · (d + m) · m`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x_t` | vector de entrada en el paso `t`: el embedding del token | las de la entrada | Más dimensión de entrada son más pesos en `W_x`, pero no alarga la memoria: la celda sigue teniendo el mismo estado |
| `h_t` | estado oculto: el resumen de todo lo leído hasta `t` | adimensional | Es la memoria de la red. Un estado mayor guarda más matices y multiplica los parámetros con `m²`, que es el término dominante |
| `c_t` | estado de celda de la LSTM: el que se actualiza sumando | adimensional | Es la autopista del gradiente. No añade parámetros propios; los añaden las puertas que lo escriben |
| `W_h` | matriz recurrente estado → estado, **la misma en todos los pasos** | adimensional | Su norma decide el factor por paso. Alta, el producto de cincuenta matrices explota; baja, se desvanece. No crece con la longitud de la secuencia |
| `W_x` | matriz entrada → estado | adimensional | Es el término `d · m`: sube si usas embeddings más largos, no si alargas la secuencia |
| `f_t` | puerta de olvido: cuánto del estado de celda anterior se conserva | adimensional, entre 0 y 1 | Es el factor que multiplica al gradiente que vuelve por `c_t`. Cerca de 1 la memoria aguanta muchos pasos; cerca de 0 se corta en seco |
| `i_t`, `o_t` | puertas de entrada y de salida de la LSTM | entre 0 y 1 | Deciden cuánto se escribe y cuánto se expone en cada paso. No cambian el número de parámetros, cambian lo que pasa por la celda |
| `g_t` | candidato: la información nueva, acotada a (−1, 1) | adimensional | Es el contenido que se propone; se queda en el estado solo en la medida en que `i_t` lo deje pasar |
| `z_t`, `r_t` | puertas de actualización y reinicio de la GRU | entre 0 y 1 | Sustituyen a las tres puertas de la LSTM con dos. `(1 − z_t)` es la parte del estado anterior que se conserva tal cual |
| `m` | tamaño del estado oculto | unidades | Es la palanca grande: los parámetros crecen con `m²` y el coste por paso también. Doblar `m` casi cuadruplica la parte recurrente |
| `d` | tamaño de la entrada en cada paso | unidades | Crece en línea recta en `W_x`. Alargar la secuencia no lo cambia: es el mismo vector de pesos en los cincuenta pasos |
:::

**Parámetros.** Una celda simple gasta `d·m + m² + m`. Cada puerta de una LSTM o GRU añade un
juego de matrices de tamaño `(d + m) × m` y un sesgo de tamaño `m`. Con `d = 10` y `m = 20`:
RNN 620, LSTM 2.480 (cuatro puertas) y GRU 1.860 (tres). La GRU usa un **25 % menos** que la
LSTM con el mismo estado.

## Ejemplo

Con un factor de retropropagación de 0,25 por paso (el valor típico con `tanh`, cuya derivada
máxima es 1 y vale 0,25 en el punto de trabajo habitual), tras 50 pasos el gradiente que llega
al primer paso es 0,25⁵⁰ ≈ **7,9 · 10⁻³¹**: cero en cualquier precisión finita. Con 0,9 por paso
es 5,2 · 10⁻³, pequeño pero vivo. Con 1,5 por paso es **6,4 · 10⁸** y el entrenamiento revienta.

Por eso la solución práctica tiene tres piezas, y las tres se usan juntas:

- Celdas con puertas (LSTM o GRU), que crean el camino aditivo del estado de celda.
- **Recorte del gradiente** (*gradient clipping*): si la norma del gradiente global supera un
  umbral, se reescala. Con umbral 1,0, un gradiente de norma 47 se convierte en uno de norma
  1,0 sin cambiar su dirección. Es la defensa estándar contra la explosión.
- **Truncar la retropropagación en el tiempo** (TBPTT): se corta el grafo cada `k` pasos (por
  ejemplo 35) y se desprenden los estados. Limita el coste y la longitud del producto.

:::figura
fichero: rnn-lstm-gru-gradiente-y-pesos
pie: La curva de la izquierda es el producto que aparece al retropropagar por el tiempo: un factor por paso, elevado al número de pasos. Léela al revés de como se lee una gráfica normal, porque el eje horizontal son los pasos que retrocedes. Con 0,25 por paso, a los veinte pasos ya se ha perdido todo y a los cincuenta quedan 8·10⁻³¹: la primera palabra de la frase no recibe ninguna señal apreciable por mucho que entrenes, porque ese número es diez millones de veces más pequeño que el peso al que tendría que sumarse. Con 0,90 el producto baja, pero sigue siendo un número utilizable: la información del principio llega. Y con 1,50 el mismo producto se dispara hasta 6·10⁸ y la pérdida se va a `nan` en el primer lote malo. La conclusión práctica es que el factor ronda 1 o no hay nada que hacer, y de ahí salen las tres piezas que se usan juntas: puertas que crean un camino aditivo, recorte del gradiente para cortar la explosión y truncado en el tiempo para limitar el producto. El panel derecho explica por qué mucha gente elige GRU: con 10 entradas y 20 unidades de estado, la RNN gasta 620 parámetros, la LSTM 2.480 y la GRU 1.860, un 25 % menos, porque fusiona el estado de celda con el oculto y usa tres juegos de matrices en vez de cuatro. El ahorro no es solo de memoria: menos parámetros es también menos sobreajuste cuando los datos son pocos.
fuente: figuras/rnn-lstm-gru-1.py
:::

## Código

```python verificable
# BPTT multiplica un factor por cada paso hacia atras: el producto decide todo.
# .3e es notacion cientifica con tres decimales: con .3f los dos ultimos casos saldrian
# 0.000 y no se veria ni que uno se apaga ni que el otro explota.
print(f"0.25^50 = {0.25 ** 50:.3e}")   # -> 7.889e-31  (desvanecido)
print(f"0.90^50 = {0.90 ** 50:.3e}")   # -> 5.154e-03  (vivo)
print(f"1.50^50 = {1.50 ** 50:.3e}")   # -> 6.376e+08  (explosivo)
```

:::claves
- `0.25 ** 50` es una potencia, no una multiplicación encadenada: Python la calcula con
  exponenciación y por eso el resultado es exacto hasta donde llega el `float` de 64 bits. En
  `float32`, que es lo que usa la GPU, los tres números siguen siendo representables: el más
  pequeño de los normales es 1,18·10⁻³⁸ y el mayor, 3,4·10³⁸. Lo que mata al gradiente en la
  práctica no es que el producto se vuelva cero de golpe, sino que sea tan diminuto que la
  actualización de las primeras capas se pierda al sumarse a pesos de tamaño normal.
- `:.3e` es notación científica con tres decimales. Si lo cambias por `:.3f`, las dos últimas
  líneas imprimen `0.000` y `6376215002.142`, y la primera sale `0.000`: el formato esconde
  justo lo que quieres ver.
- En la segunda pieza, `rng.normal(0, 0.1, (d, m))` recibe la **forma** como una tupla
  `(filas, columnas)`, y aquí filas son las entradas y columnas las unidades de estado. Si
  inviertes el orden, `x[t] @ Wx` falla al multiplicar o, peor, cuadra por casualidad cuando
  `d = m` y la red aprende otra cosa.
- `h = np.tanh(x[t] @ Wx + h @ Wh + b)` funciona porque el lado derecho se evalúa **entero**
  antes de asignar: la `h` que aparece a la derecha es la del paso anterior. Si lo partieras en
  dos líneas reutilizando `h` a medias, estarías metiendo el estado nuevo en su propia entrada.
- `h = np.zeros(m)` es el estado inicial, un vector **plano** de `m` números. Con
  `np.zeros((1, m))` el producto `h @ Wh` sigue funcionando (una fila por la matriz), pero la
  forma del estado cambia y el resto del código deja de cuadrar sin dar un error claro.
- `round(float(np.linalg.norm(h)), 4)`: `np.linalg.norm` devuelve un `numpy.float64` y el
  `float()` lo pasa a `float` de Python. Sin esa conversión, `round` mantiene el tipo de numpy y
  el texto que se imprime cambia de formato según la versión.
:::

```python verificable
import numpy as np

# Cuantos parametros gasta cada celda con entrada 10 y estado oculto 20.
d, m = 10, 20                                  # d entradas por paso, m unidades de estado
rnn = d * m + m * m + m                        # una matriz de entrada, una recurrente, un sesgo
lstm = 4 * (d * m + m * m) + 4 * m             # 4 puertas
gru = 3 * (d * m + m * m) + 3 * m              # 3 puertas
print("RNN :", rnn)                 # -> 620
print("LSTM:", lstm)                # -> 2480
print("GRU :", gru)                 # -> 1860
print("GRU/LSTM:", round(gru / lstm, 3))   # -> 0.75

# Una celda RNN minima paso a paso: h_t = tanh(x_t Wx + h_(t-1) Wh + b).
rng = np.random.default_rng(0)                 # semilla fija: los mismos numeros siempre
Wx = rng.normal(0, 0.1, (d, m))                # (entradas, unidades): x[t] @ Wx -> (m,)
Wh = rng.normal(0, 0.1, (m, m))                # (unidades, unidades): h @ Wh -> (m,)
b = np.zeros(m)
x = rng.normal(0, 1, (5, d))                   # 5 pasos de tiempo, d entradas por paso

h = np.zeros(m)                                # estado inicial: un vector plano de ceros
for t in range(5):                             # la MISMA celda cinco veces: pesos atados
    h = np.tanh(x[t] @ Wx + h @ Wh + b)

# El estado final es todo lo que la red recuerda de los 5 pasos.
print("norma del estado:", round(float(np.linalg.norm(h)), 4))   # -> 1.3989
```

```python ilustrativo
import torch
import torch.nn as nn

modelo = nn.LSTM(input_size=128, hidden_size=256, num_layers=2,
                 batch_first=True, dropout=0.1)
# Las secuencias de un lote tienen longitudes distintas: se empaquetan para no
# procesar el relleno, que contaminaria el estado con ceros.
empaquetado = nn.utils.rnn.pack_padded_sequence(x, longitudes, batch_first=True,
                                                enforce_sorted=False)
salida, (h_n, c_n) = modelo(empaquetado)
salida, _ = nn.utils.rnn.pad_packed_sequence(salida, batch_first=True)

perdida.backward()
# Sin recorte, un solo paso malo puede hacer NaN toda la matriz de pesos.
torch.nn.utils.clip_grad_norm_(modelo.parameters(), max_norm=1.0)
optimizador.step()
optimizador.zero_grad()   # PyTorch ACUMULA el gradiente: sin esto se suma al del lote anterior
```

## Errores típicos

- **No recortar el gradiente.** Una recurrencia con 200 pasos multiplica 200 matrices por el
  camino recurrente. Basta con que la mayor parte de los factores sea algo mayor que 1 para que
  el gradiente se dispare y la pérdida pase a NaN sin avisar. Recorta con
  `clip_grad_norm_` y comprueba la norma del gradiente durante el entrenamiento.
- **Rellenar sin máscara.** Si juntas secuencias de distinta longitud con ceros y no usas
  `pack_padded_sequence` ni una máscara, el estado se contamina con el relleno y —peor— el
  modelo aprende a predecir relleno. El relleno debe quedar fuera de la pérdida y del estado.
- **Arrastrar el estado oculto entre lotes o barajar dentro de la secuencia.** Si no reinicias `h`
  en cada lote independiente, la red ve datos del lote anterior como si fueran pasado del actual;
  esto puede ser intencionado (entrenamiento con estado), pero entonces los lotes deben ser tramos
  consecutivos de la misma serie y hay que reiniciar al empezar cada época. Y dentro de una
  secuencia el orden *es* la información: puedes barajar qué secuencias forman cada lote, nunca
  los pasos de una secuencia.
- **Quedarte con la salida del último paso cuando la información está al principio.** Con un
  codificador unidireccional, el último estado es el que más pesa. Si necesitas mirar en las dos
  direcciones, usa una red bidireccional; si el problema es de alineación entre dos secuencias,
  lo que quieres es [[atencion|atención]].
- **Concluir que «la recurrencia es peor» con pocos datos.** Con secuencias cortas y un conjunto
  de entrenamiento pequeño, una GRU o una LSTM compiten perfectamente con un
  [[transformers|transformer]] y entrenan con menos recursos. La ventaja del transformer aparece
  cuando hay datos y cuando la secuencia es larga y paralelizable.
- **Saturar el `tanh` con entradas sin normalizar.** Si las entradas tienen magnitudes grandes,
  `tanh` se satura y su derivada se va a cero: vuelves al gradiente desvanecido por la puerta de
  atrás. Estandariza las entradas, como en cualquier red.

:::practica
enunciado: Al retropropagar por el tiempo, cada paso multiplica el gradiente por 0,6. ¿Qué fracción de la señal llega al primer estado tras 10 pasos y a partir de cuántos pasos queda por debajo de 10⁻³?
pista: La señal que sobrevive es el producto de un factor por paso, es decir 0,6 elevado al número de pasos.
solucion: 0,6¹⁰ = 6,0 · 10⁻³, menos del 1 % de la señal original. Como 0,6ⁿ < 10⁻³ exige n > ln(10⁻³) / ln(0,6) = 13,5, a partir de 14 pasos el primer estado no recibe prácticamente nada. Eso es el gradiente que se desvanece: no hay ningún error de cálculo, el producto se come la señal.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace exactamente la puerta de olvido de una LSTM?
o: Decide qué parte del estado de celda anterior se conserva, multiplicándolo por un valor entre 0 y 1
o: Borra las palabras que no aparecen en el vocabulario
o: Reinicia el estado oculto al empezar cada secuencia
a: 1
e: f_t sale de una sigmoide, así que está entre 0 y 1, y multiplica al estado de celda anterior: 0 lo borra del todo y 1 lo conserva entero. No tiene nada que ver con el vocabulario (eso es la tokenización) ni con el reinicio entre secuencias, que se hace fuera del modelo.
:::

:::quiz
p: ¿Por qué la actualización aditiva del estado de celda ayuda con el gradiente que se desvanece?
o: Porque elimina las multiplicaciones de la retropropagación
o: Porque el gradiente fluye por la suma sin multiplicarse por la matriz recurrente en cada paso, solo por las puertas de olvido
o: Porque usa float64 en lugar de float32
a: 2
e: c_t = f_t ⊙ c_(t−1) + i_t ⊙ g_t. Al derivar respecto a c_(t−1) queda solo f_t, no una matriz completa más una derivada de tanh. El producto de 50 factores se convierte en un producto de puertas de olvido que la red puede aprender a mantener cerca de 1. No se eliminan las multiplicaciones: se cambian por otras mucho más benignas.
:::

:::aviso
Enmascarar no es opcional cuando hay relleno. Y hay un detalle que se olvida: la pérdida debe
calcularse solo sobre las posiciones reales, dividiendo entre el número de elementos válidos y
no entre el número de elementos del tensor. Si divides por el total, el modelo con secuencias
largas parece mejor entrenado de lo que está.
:::
