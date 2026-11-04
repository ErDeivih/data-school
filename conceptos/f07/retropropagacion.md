---
id: retropropagacion
titulo: Retropropagación
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [perceptron-y-mlp, regla-de-la-cadena, derivadas-parciales-y-gradiente, funciones-de-activacion]
tags: [redes-neuronales, gradientes, autograd, entrenamiento]
resumen: La regla de la cadena aplicada capa a capa, con el grafo computacional, los deltas y una comprobación numérica del gradiente
fuentes: ["Rumelhart, Hinton y Williams (1986), 'Learning representations by back-propagating errors'", "Baydin et al. (2018), 'Automatic Differentiation in Machine Learning: a Survey'"]
---

## En una frase

La retropropagación es la regla de la cadena aplicada en orden inverso sobre el grafo de
operaciones de la red: se calcula cómo cambia la pérdida al mover cada peso, empezando por la
salida y reutilizando en cada capa el error que ya se calculó en la capa siguiente.

## La idea

Entrenar una red es un problema de optimización: hay una pérdida que mide cuánto se equivoca el
modelo y quieres saber, para cada uno de los millones de pesos, en qué dirección moverlo para
que la pérdida baje. Es decir, quieres el gradiente de la pérdida respecto a cada peso. El
problema es que la pérdida es una composición de decenas de operaciones, y calcular las
derivadas una por una a mano no es viable.

La observación que lo resuelve es que la derivada de una composición se puede encadenar:

:::formula
Si y = f(g(x)), entonces dy/dx = f'(g(x)) · g'(x)
:::

Y si en vez de una cadena piensas en un grafo, aparece la estructura útil: la pérdida se
calcula aplicando operaciones en orden (hacia delante), y cada operación conoce su propia
derivada local. Para obtener el gradiente respecto a cualquier nodo, basta con multiplicar las
derivadas locales del camino que va de ese nodo a la pérdida. La clave está en que **esos
productos se comparten**: si dos rutas pasan por el mismo nodo, el factor común se calcula una
vez. Esa reutilización es lo que separa la retropropagación de aplicar la regla de la cadena
a mano nodo por nodo.

Ejemplo mecánico. Supón `a = b·c`, `d = a + e`, `L = d²`. Hacia delante: `a`, luego `d`, luego
`L`. Hacia atrás: `dL/dd = 2d`, `dd/da = 1` (porque `d = a + e`), así que `dL/da = 2d·1 = 2d`;
y `da/db = c`, así que `dL/db = 2d·c` sin haber vuelto a derivar `L`. Cada nodo recibe el
gradiente de sus consumidores, lo multiplica por su derivada local y lo reparte entre sus
entradas. Eso es toda la retropropagación.

Con eso quedan tres hechos que hay que retener:

1. **La retropropagación es el algoritmo, no el optimizador.** Calcula gradientes; lo que
   decide cuánto moverse es el optimizador (SGD, momento, Adam). Confundirlos es como confundir
   el cuentakilómetros con el motor.
2. **Cada capa necesita guardar su preactivación.** Para aplicar `φ'(z)`, el paso hacia atrás
   necesita el `z` que se calculó hacia delante. Eso explica buena parte del consumo de
   memoria de entrenar una red, y también que los frameworks liberen esos valores a medida que
   ya no hacen falta.
3. **El mismo mecanismo funciona para cualquier grafo.** No hace falta que sea por capas:
   autograd graba las operaciones que ejecutas y las recorre al revés. Por eso puedes escribir
   bucles, condiciones y operaciones raras en PyTorch y el gradiente sigue calculándose solo.

## Definición formal

Con `L` la pérdida, `z^(ℓ)` las preactivaciones de la capa `ℓ` y `a^(ℓ) = φ(z^(ℓ))` las
activaciones, se define el delta de la capa `ℓ` como el gradiente de la pérdida respecto a sus
preactivaciones:

:::formula
δ^(L) = ∇_{a^(L)} L ⊙ φ'(z^(L))            δ^(ℓ) = (W^(ℓ+1))ᵀ · δ^(ℓ+1) ⊙ φ'(z^(ℓ))
:::

:::formula
∂L/∂W^(ℓ) = δ^(ℓ) · (a^(ℓ−1))ᵀ            ∂L/∂b^(ℓ) = δ^(ℓ)
:::

- `L` — la pérdida total, un escalar; con un lote de `n` ejemplos suele ser la media de las
  pérdidas individuales.
- `⊙` — producto elemento a elemento; `δ^(ℓ)` tiene la forma de las preactivaciones de la capa
  `ℓ`.
- `W^(ℓ)`, `b^(ℓ)` — los pesos y sesgos de la capa `ℓ`; `W^(ℓ+1)` es la matriz de la capa
  siguiente, la que está más cerca de la salida.
- `a^(ℓ−1)` — las activaciones de la capa anterior; en la primera capa son las entradas `x`.
- `φ'` — la derivada de la
  [[funciones-de-activacion|función de activación]], evaluada en cada preactivación.
- `(W^(ℓ+1))ᵀ` — la transpuesta, que reparte el error hacia atrás por los mismos caminos por
  los que la señal fue hacia delante.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L` | pérdida total del lote, un escalar | las del objetivo al cuadrado si la pérdida es cuadrática | Todos los gradientes crecen en la misma proporción: la pérdida es la escala global del entrenamiento. Cambiar de `mean` a `sum` multiplica el paso efectivo por el tamaño del lote |
| `δ^(ℓ)` | gradiente de la pérdida respecto a las preactivaciones de la capa `ℓ` | las de `z^(ℓ)` | Es el error que se reparte hacia atrás. Si se encoge capa a capa, las primeras dejan de aprender; si crece, el paso se dispara y la pérdida acaba en `nan` |
| `W^(ℓ)` | matriz de pesos de la capa `ℓ` | adimensional | Sube la norma del gradiente de esa capa: los pesos grandes amplifican la señal en la ida y el error en la vuelta, y son la vía habitual del gradiente que explota |
| `b^(ℓ)` | sesgos de la capa `ℓ` | las de la preactivación | Su gradiente es exactamente `δ^(ℓ)`, sin multiplicar por ninguna activación: los sesgos aprenden más rápido que los pesos cuando las activaciones son pequeñas |
| `a^(ℓ−1)` | activaciones de la capa anterior; en la primera capa son las entradas `x` | las de la activación | Multiplica al delta en `∂L/∂W`: si las activaciones son diminutas, el gradiente de los pesos de esa capa también lo es, aunque el delta sea grande |
| `φ'` | derivada de la activación, evaluada en cada preactivación | adimensional | Es el factor que decide si el gradiente sobrevive. En sigmoide y `tanh` vale entre 0 y 1 (0,25 como máximo la sigmoide): al encadenarse, el producto se desvanece. En `ReLU` vale 1 o 0, sin término medio |
| `(W^(ℓ+1))ᵀ` | transpuesta de la matriz de la capa siguiente | adimensional | No se ajusta: reparte el error por los mismos caminos por los que fue la señal. Sin transponer, las formas pueden cuadrar por casualidad y el modelo entrena mal sin dar ningún error |
| `n` | número de ejemplos del lote | ejemplos | El delta de la salida lleva un `1/n` dentro: al subir el lote cada ejemplo pesa menos y el paso es más suave, pero hay menos actualizaciones por época |
:::

La estructura recursiva es el punto clave: para calcular `δ^(ℓ)` solo hacen falta `δ^(ℓ+1)`,
la matriz de pesos siguiente y la derivada local. **El coste total es del mismo orden que el
paso hacia delante**, no del orden del número de pesos al cuadrado. Eso es lo que hace viable
entrenar redes grandes.

Y como el gradiente que se propaga es un producto de matrices y derivadas, el resultado puede
desvanecerse (si los factores son menores que 1, típicamente con sigmoide y `tanh`) o
explotar (si son mayores, típicamente con pesos mal inicializados). Ese es el diagnóstico
detrás de las inicializaciones de Xavier y He y de las conexiones residuales.

## Ejemplo

Red mínima: 3 entradas, una capa oculta de 2 neuronas con activación sigmoide, una salida con
sigmoide y pérdida cuadrática media. Cuatro filas:

```
entradas              etiqueta
(0, 0, 0)             0
(0, 1, 1)             1
(1, 0, 1)             1
(1, 1, 0)             0
```

Con pesos concretos (`W¹` de 3x2, `b¹ = (0,1; −0,1)`, `W²` de 2x1, `b² = 0,2`) el cálculo da:

```
perdida inicial            0,251452
gradiente dW2              0,022698   0,023830
diferencias finitas dW2    0,022698   0,023830
perdida tras un paso       0,250920
```

Ese es el resultado que hay que saber leer: la cuarta fila es la comprobación. El gradiente
analítico que ha salido de encadenar deltas coincide dígito a dígito con el que se obtiene
perturbando un peso 0,000001 arriba y abajo y midiendo cómo cambia la pérdida. **Siempre que
implementes retropropagación a mano, haz esa comprobación antes de dar nada por bueno**: un
error de signo o un `W` sin transponer producen un modelo que entrena «un poco» y es
sorprendentemente difícil de detectar mirando la curva de pérdida.

Y el paso final: con los pesos nuevos, la pérdida baja de 0,251452 a 0,250920. Un descenso de
0,0005 en un solo paso con tasa de aprendizaje 0,5. El entrenamiento es exactamente esto,
repetido unas cuantas mil veces.

:::figura
fichero: retropropagacion-coste-y-desvanecimiento
pie: El panel izquierdo compara lo que cuesta obtener el gradiente de tres maneras y está en escala logarítmica en los dos ejes. El paso hacia atrás corre en paralelo al de ida, con un factor constante pequeño: esa es la razón de que entrenar una red de millones de pesos sea viable. La curva roja es la comprobación por diferencias finitas, que necesita dos pasadas hacia delante por cada parámetro: con 10⁸ pesos son 10¹⁶ pasadas, un millón de veces más que la retropropagación. Por eso las diferencias finitas se usan para verificar un gradiente, nunca para calcularlo en el entrenamiento. El panel derecho es la consecuencia práctica de todo lo anterior: mide la norma del gradiente en cada capa de una red de cinco y la compara con la de la última. Con sigmoide, la primera capa recibe 0,001 de lo que recibe la última, es decir, mil veces menos: esas capas apenas cambian por mucho que se entrene. Con ReLU, la primera recibe 0,23, cuatro veces menos y perfectamente entrenable. Ese cociente, medido por capa, es el diagnóstico que dice si el problema es la inicialización o la activación, antes de tocar la tasa de aprendizaje.
fuente: figuras/retropropagacion-1.py
:::

## Código

```python verificable
import numpy as np

# Red minima: 3 entradas -> 2 neuronas ocultas (sigmoide) -> 1 salida (sigmoide)
X = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
y = np.array([[0.0], [1.0], [1.0], [0.0]])
W1 = np.array([[0.4, -0.6], [-0.2, 0.8], [0.5, 0.1]])
b1 = np.array([0.1, -0.1])
W2 = np.array([[1.2], [-0.9]])
b2 = np.array([0.2])

def sigmoide(z):
    return 1.0 / (1.0 + np.exp(-z))

def perdida(W1, b1, W2, b2):
    a1 = sigmoide(X @ W1 + b1)          # @ es producto matricial: (4x3) @ (3x2) -> (4x2)
    yg = sigmoide(a1 @ W2 + b2)
    return float(np.mean((yg - y) ** 2))   # float() saca el escalar de numpy a Python

# Paso hacia delante guardando lo que la regla de la cadena necesita despues
a1 = sigmoide(X @ W1 + b1)
yg = sigmoide(a1 @ W2 + b2)

# Paso hacia atras: delta de la salida y delta de la capa oculta
# El 2 y el 1/len(y) salen de derivar la media del cuadrado; yg*(1-yg) es la derivada de la sigmoide
d_salida = 2 * (yg - y) / len(y) * yg * (1 - yg)
gW2 = a1.T @ d_salida                   # la activacion anterior TRANSPUESTA por el delta
d_oculta = (d_salida @ W2.T) * a1 * (1 - a1)     # (W2)^T reparte el error hacia atras
gW1 = X.T @ d_oculta

print("perdida inicial          ", round(perdida(W1, b1, W2, b2), 6))   # -> 0.251452
print("gradiente dW2            ", np.round(gW2.ravel(), 6))           # -> [0.022698 0.02383 ]
```

:::claves
- `d_salida = 2 * (yg - y) / len(y) * yg * (1 - yg)` mete **todo** en una línea: el `2` y el
  `1/len(y)` vienen de derivar la media del cuadrado, y `yg * (1 - yg)` es la derivada de la
  sigmoide evaluada en la salida. Si te olvidas de ese último factor, el gradiente es el de una
  red lineal: parece que entrena, pero el modelo no aprende lo que debería.
- `a1.T @ d_salida` necesita la activación de la capa **anterior** y transpuesta: la forma es
  (2x4) @ (4x1) = (2x1), que es la forma de `W2`. El producto matricial no avisa si te equivocas
  de orden cuando las dimensiones cuadran por casualidad, y ese es el error silencioso clásico
  de implementar la retropropagación a mano.
- En `(d_salida @ W2.T) * a1 * (1 - a1)` conviven los dos productos: `@` es matricial (reparte
  el error entre las neuronas ocultas) y `*` es elemento a elemento (aplica la derivada neurona
  a neurona). Cambiar uno por otro no da error de formas, da un modelo que entrena mal.
- `gW2.ravel()` aplana la matriz (2x1) a un vector de dos elementos solo para imprimirla. No
  modifica `gW2` si se usa como método, pero `gW2.ravel()` devuelve una **vista**: si escribiras
  sobre el resultado, cambiarías el gradiente original.
- `float(np.mean(...))` no es cosmética: sin el `float`, la función devuelve un `numpy.float64` y
  `round` sobre él mantiene el tipo de numpy, con un formato que cambia según la versión.
- En el bloque de las diferencias finitas, `W2p, W2m = W2.copy(), W2.copy()` es obligatorio: sin
  el `copy()` las dos variables apuntan al mismo array, la perturbación de una se suma a la de
  la otra y la resta da cero. El gradiente numérico sale 0 y parece que el analítico está mal.
- La `eps` de las diferencias finitas tiene que estar entre `1e-5` y `1e-7`. Con `1e-2` el error
  de truncamiento domina; con `1e-12` domina el ruido de coma flotante y el cociente sale
  cualquier cosa.
:::

```python verificable
import numpy as np

# La misma red, ahora comprobando el gradiente por diferencias finitas
X = np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
y = np.array([[0.0], [1.0], [1.0], [0.0]])
W1 = np.array([[0.4, -0.6], [-0.2, 0.8], [0.5, 0.1]])
b1 = np.array([0.1, -0.1])
W2 = np.array([[1.2], [-0.9]])
b2 = np.array([0.2])

def sigmoide(z):
    return 1.0 / (1.0 + np.exp(-z))

def perdida(W1, b1, W2, b2):
    a1 = sigmoide(X @ W1 + b1)
    return float(np.mean((sigmoide(a1 @ W2 + b2) - y) ** 2))

a1 = sigmoide(X @ W1 + b1)
yg = sigmoide(a1 @ W2 + b2)
d_salida = 2 * (yg - y) / len(y) * yg * (1 - yg)
gW2 = a1.T @ d_salida

# Perturbamos cada peso de W2 y comparamos con el gradiente analitico
eps = 1e-6
num = np.zeros_like(W2)                 # misma forma y tipo que W2, rellena de ceros
for i in range(W2.shape[0]):
    W2p, W2m = W2.copy(), W2.copy()     # sin copy() las dos variables serian el mismo array
    W2p[i, 0] += eps
    W2m[i, 0] -= eps
    # Diferencia central: (f(x+h) - f(x-h)) / 2h, mas precisa que la hacia un solo lado
    num[i, 0] = (perdida(W1, b1, W2p, b2) - perdida(W1, b1, W2m, b2)) / (2 * eps)
print("diferencias finitas dW2  ", np.round(num.ravel(), 6))   # -> [0.022698 0.02383 ]

# Un paso de descenso de gradiente con tasa 0,5
print("perdida tras un paso     ", round(perdida(W1, b1, W2 - 0.5 * gW2, b2), 6))   # -> 0.25092
```

```python ilustrativo
# Lo mismo que hace autograd por debajo, en PyTorch
import torch

X = torch.tensor([[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])
# requires_grad=True es lo que hace que autograd grabe el grafo de operaciones
W1 = torch.tensor([[0.4, -0.6], [-0.2, 0.8], [0.5, 0.1]], requires_grad=True)
W2 = torch.tensor([[1.2], [-0.9]], requires_grad=True)

a1 = torch.sigmoid(X @ W1)
y_gorro = torch.sigmoid(a1 @ W2)
perdida = ((y_gorro - y) ** 2).mean()
perdida.backward()                     # recorre el grafo hacia atras y rellena los .grad
# W2.grad vale None hasta que se llama a backward(), y lo que escribe se ACUMULA
print(W2.grad)                         # identico al gW2 calculado a mano
```

## Errores típicos

- **No poner a cero los gradientes entre pasos.** En PyTorch los `.grad` se **acumulan**: si
  no llamas a `optimizer.zero_grad()`, el segundo paso usa la suma de los dos gradientes y el
  entrenamiento se va. Es el error número uno de quien empieza con PyTorch.
- **Transponer mal al repartir el error.** El paso hacia atrás usa `(W^(ℓ+1))ᵀ` para llevar el
  error de la capa siguiente a la actual. Con la matriz sin transponer, las formas pueden
  cuadrar por casualidad y el modelo entrena mal sin dar ningún error.
- **Olvidar la derivada de la activación.** Si al calcular `δ` se omite el factor `φ'(z)`, el
  gradiente que se propaga es el de una red lineal y el entrenamiento se degrada. La
  comprobación por diferencias finitas lo detecta de inmediato.
- **Confundir retropropagación con descenso de gradiente.** La primera calcula derivadas; el
  segundo decide el tamaño del paso. Un fallo de convergencia puede ser de cualquiera de los
  dos, y se diagnostican de forma distinta: mira la norma del gradiente antes de tocar la tasa
  de aprendizaje.
- **Guardar el grafo cuando no hace falta.** Dentro de un bucle de evaluación, no desactivar el
  cálculo de gradientes acumula grafos en memoria hasta agotarla. En PyTorch, envuelve la
  evaluación en `with torch.no_grad():`; es una línea y evita el error de memoria más común.
- **Comprobar el gradiente con una `eps` mal elegida.** Con `eps = 1e-2` la aproximación por
  diferencias finitas tiene un error enorme; con `eps = 1e-12`, el ruido de coma flotante se
  come el resultado. El rango razonable es `1e-5` a `1e-7`, y la tolerancia de comparación debe
  ser relativa, no exacta.

:::practica
enunciado: Una neurona con una entrada: x = 1,5, w = 0,4, b = 0,1, activación sigmoide y pérdida L = (a − y)² con y = 1. Calcula z, a y la pérdida; luego el delta δ = 2(a − y)·a·(1 − a) y los gradientes ∂L/∂w y ∂L/∂b. Da un paso con η = 0,5 y comprueba si la pérdida baja.
pista: El delta ya incluye la derivada de la sigmoide. El gradiente del peso es δ por la entrada, y el del sesgo es δ.
solucion: z = 0,4·1,5 + 0,1 = 0,7; a = 1/(1+e^−0,7) = 0,6682; L = (0,6682 − 1)² = 0,1101. δ = 2·(−0,3318)·0,6682·0,3318 = −0,1471, así que ∂L/∂w = −0,1471·1,5 = −0,2207 y ∂L/∂b = −0,1471. Con η = 0,5: w = 0,5104 y b = 0,1736. La pérdida pasa a 0,0790: ha bajado.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué calcula exactamente la retropropagación?
o: Los pesos óptimos de la red
o: El gradiente de la pérdida respecto a cada parámetro, reutilizando los deltas de las capas siguientes
o: El tamaño de paso que hay que dar en cada dirección
a: 2
e: La retropropagación solo calcula derivadas: aplica la regla de la cadena hacia atrás y reutiliza el delta ya calculado en la capa siguiente. Elegir el tamaño del paso es trabajo del optimizador (SGD, momento, Adam).
:::

:::quiz
p: El gradiente analítico de `W2` da (0,022698; 0,023830) y las diferencias finitas dan lo mismo. ¿Para qué sirve esa comprobación?
o: Para acelerar el entrenamiento, porque evita calcular el gradiente dos veces
o: Para detectar errores de implementación: un signo cambiado o una traspuesta mal puesta dan un gradiente parecido pero incorrecto
o: Para sustituir el paso hacia atrás por una aproximación numérica más barata
a: 2
e: Es una prueba de corrección, no un método de entrenamiento: las diferencias finitas cuestan un paso hacia delante por cada peso, así que solo se usan en la comprobación. Su valor está en que un gradiente mal calculado suele producir un modelo que entrena «regular», sin errores visibles.
:::

:::aviso
El producto de muchas matrices y derivadas es la razón de que el gradiente se desvanezca o
explote. Si ves que las primeras capas apenas cambian mientras las últimas aprenden, no
cambies la tasa de aprendizaje a ciegas: mide la norma del gradiente por capa. Ese dato te
dice si el problema está en la inicialización o en la activación.
:::
