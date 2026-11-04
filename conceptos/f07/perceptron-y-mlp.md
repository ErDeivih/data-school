---
id: perceptron-y-mlp
titulo: Perceptrón y perceptrón multicapa
fase: 7
nivel: básico
rutas: [ds]
prerequisitos: [regresion-lineal, glm-y-logistica, producto-punto-y-similitud]
tags: [redes-neuronales, neurona, capas, xor]
resumen: La neurona, el sesgo, las capas y el teorema que explica por qué una capa oculta ya resuelve lo que una recta no puede
fuentes: ["Rosenblatt (1958), 'The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain'", "Rumelhart, Hinton y Williams (1986), 'Learning representations by back-propagating errors'", "Cybenko (1989), 'Approximation by superpositions of a sigmoidal function'"]
---

## En una frase

Una neurona combina sus entradas con unos pesos, les suma un sesgo y decide con ese número; una
red las apila en capas, y con eso dibuja fronteras curvas que una sola neurona no puede.

## La idea

Empieza por la pieza mínima. Una neurona recibe `p` números, los multiplica por `p` pesos, los
suma, le añade un término constante (el sesgo) y pasa el resultado por una función de
activación. Eso es todo. La suma `w·x + b` es una [[regresion-lineal|combinación lineal]]: si
la activación fuera la identidad, la neurona sería un modelo lineal.

El sesgo es la pieza que más gente olvida. Sin `b`, la frontera de decisión tiene que pasar por
el origen; con `b`, la mueves a donde quieras. En dos dimensiones la neurona dibuja una recta;
en `p` dimensiones, un hiperplano.

De ahí sale el límite famoso: una sola neurona solo separa lo que una recta separa, y hay
problemas minúsculos que no lo son. El ejemplo clásico es XOR, con dos entradas binarias y la
etiqueta «una u otra pero no las dos»: los positivos (0,1) y (1,0) están en una diagonal y los
negativos (0,0) y (1,1) en la otra, así que **ninguna recta los separa**. Minsky y Papert lo
demostraron en 1969.

La salida es añadir una capa oculta. Con dos neuronas ocultas basta para resolver XOR: cada una
reconoce media condición y la salida combina las dos. Eso es un perceptrón multicapa: una capa
de entrada, una o más capas ocultas y una capa de salida. Y aquí está el resultado que justifica
todo el campo: una red con una sola capa oculta, suficientemente ancha, puede aproximar
cualquier función continua con la precisión que quieras (teorema de aproximación universal). No
dice cuántas neuronas hacen falta ni cómo encontrarlas.

Una forma útil de leer una capa oculta: **cada neurona recorta el espacio con un hiperplano y
la capa siguiente combina esos recortes**. Con muchas neuronas, la red va tallando el espacio
en trozos y etiquetando cada trozo. Por eso más neuronas permiten fronteras más retorcidas, y
por eso también sobreajustan antes cuando hay pocos datos.

## Definición formal

Una neurona con `p` entradas y activación `φ` calcula:

:::formula
z = Σ_{i=1..p} wᵢ·xᵢ + b = w·x + b          a = φ(z)
:::

- `xᵢ` — la entrada `i`; en la primera capa son las variables del problema.
- `wᵢ` — el peso de la entrada `i`; su signo indica si empuja hacia la clase positiva.
- `b` — el sesgo; desplaza la frontera y no depende de ninguna entrada.
- `z` — la preactivación, una combinación lineal de las entradas.
- `φ` — la activación, típicamente no lineal: sigmoide, `tanh`, ReLU o GELU.
- `a` — la salida de la neurona, que será una entrada de la capa siguiente.

Una red con `L` capas se escribe por composición, con `W^(ℓ)`, `b^(ℓ)` los pesos y sesgos de la
capa `ℓ`:

:::formula
h^(0) = x     h^(ℓ) = φ(W^(ℓ)·h^(ℓ−1) + b^(ℓ))     ŷ = h^(L)
:::

- `W^(ℓ)` — matriz de pesos de la capa `ℓ`; su forma es (nº de neuronas de la capa, nº de
  entradas que recibe).
- `b^(ℓ)` — vector de sesgos de la capa `ℓ`, uno por neurona.
- `h^(ℓ)` — vector de activaciones de la capa `ℓ`; `h^(0)` son los datos de entrada.
- `ŷ` — la salida de la red; con varias clases, un vector de probabilidades.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x` | vector de entradas de la neurona; en la primera capa, las variables del problema | las de las variables | No es un mando que se ajuste: son los datos. Lo que importa es su escala; si una variable entra en miles y otra en unidades, el descenso de gradiente se atasca o no converge |
| `w` | peso de cada entrada; su signo decide hacia qué clase empuja | adimensional | Sube la pendiente de la frontera: la misma entrada mueve mucho más la preactivación `z`, así que la decisión se vuelve más brusca y la red se satura antes |
| `b` | sesgo; desplaza la frontera sin girarla | las de la preactivación `z` | Mueve el corte en paralelo hacia el lado negativo: hace falta más señal para activar la neurona. Sin `b`, todas las fronteras pasan por el origen |
| `φ` | activación no lineal aplicada a `z` | adimensional | Si es la identidad, la red entera colapsa a un modelo lineal por muchas capas que tenga; cuanto más se satura (sigmoide, `tanh`), menos gradiente deja pasar |
| `W^(ℓ)` | matriz de pesos de la capa `ℓ`, de forma (neuronas de la capa, entradas que recibe) | adimensional | El número de parámetros crece con el **producto** de los tamaños: doblar a la vez la anchura y la entrada cuadruplica esa capa, no la duplica |
| `b^(ℓ)` | vector de sesgos de la capa `ℓ`, uno por neurona | las de la preactivación | Desplaza la frontera de cada neurona por separado; en redes modernas se inicializan a cero porque la simetría la rompen los pesos |
| `h^(ℓ)` | activaciones de la capa `ℓ`; `h^(0)` son los datos de entrada | las de la activación | Es la representación nueva que construye la red: cada neurona oculta recorta el espacio con un hiperplano y la capa siguiente combina esos recortes |
| `ŷ` | salida de la red | las del objetivo | Con un `softmax` de salida, las componentes suman 1; en regresión se deja sin activación para no destruir la escala del objetivo |
| nº de neuronas ocultas | anchura de la capa | neuronas | Sube la capacidad: la frontera admite más recortes y se vuelve más retorcida. Acierta más en entrenamiento y sobreajusta antes cuando hay pocos datos |
| `L` | número de capas de la red | capas | Con el mismo presupuesto de parámetros, la profundidad reutiliza representaciones y la anchura no: no son intercambiables, aunque ambas aproximen funciones parecidas |
:::

Dos consecuencias que conviene tener presentes:

1. **Si `φ` fuera lineal, apilar capas no serviría de nada**: la composición de funciones
   lineales es otra función lineal. Toda la potencia viene de la no linealidad, y por eso
   [[funciones-de-activacion|las funciones de activación]] tienen su propia página.
2. **El número de parámetros crece con el producto de los tamaños**, no con la suma: una capa
   de 256 neuronas que recibe 1.000 entradas aporta 256.000 pesos.

## Ejemplo

El XOR, con cuatro filas y dos variables. Una neurona no puede: cualquier recta deja un
positivo y un negativo del mismo lado.

```
entradas   etiqueta
(0, 0)     0
(0, 1)     1
(1, 0)     1
(1, 1)     0
```

Con dos entradas y un conjunto tan diminuto no hace falta ni entrenar: los pesos se pueden
razonar a mano. Sea `A` una neurona que detecta «al menos una entrada activa» con
`w = (1, 1)`, `b = −0,5`: da `A = 1` en (0,1), (1,0) y (1,1), y `A = 0` en (0,0). Sea `B` una
neurona que detecta «las dos activas» con `w = (1, 1)`, `b = −1,5`: da `B = 1` solo en (1,1).
La salida debe ser «una u otra pero no las dos», es decir `A` menos `B`:

```
suma ponderada de salida = A - 2·B   ->   (0,0) 0   (0,1) 1   (1,0) 1   (1,1) -1
umbral 0                             ->   (0,0) 0   (0,1) 1   (1,0) 1   (1,1) 0
```

La capa oculta ha construido dos variables nuevas (`A` y `B`) en las que el problema **sí** es
linealmente separable: eso es exactamente lo que hace una capa oculta, cambiar la
representación para que la última capa tenga un problema fácil.

En dos círculos concéntricos, ni dos neuronas bastan. El código de abajo lo mide: con dos
neuronas ocultas la red acierta el 77,5 % de un conjunto de prueba, con ocho acierta el 100 %,
y la regresión logística se queda en el 42,5 %. La diferencia entre fallar y acertar son 24
parámetros de más: 9 frente a 33.

:::figura
fichero: perceptron-mlp-recta-frente-a-capa-oculta
pie: Los dos paneles tienen los mismos 400 puntos: un disco azul rodeado por un anillo rojo, con la frontera de cada modelo dibujada en negro. Son un conjunto generado aparte, así que los porcentajes no coinciden con los del código de arriba: lo que se compara aquí es la forma de la frontera, no el decimal. La regresión logística solo puede trazar una recta y acierta el 57 %: parte el anillo y mete media clase roja dentro del disco. Ese es el mejor resultado posible con una frontera lineal, no un fallo de implementación, y por eso el porcentaje no sube por mucho que se entrene. Con ocho neuronas ocultas la frontera se cierra alrededor del disco y acierta el 100 %. Merece la pena mirar la forma del panel derecho: no es un círculo suave, es un polígono de ocho lados, porque cada neurona oculta aporta un recorte recto y la capa de salida los combina. Eso es exactamente lo que hace una capa oculta: cambiar la representación para que la última capa tenga un problema fácil.
fuente: figuras/perceptron-y-mlp-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_circles
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Clase 0 dentro del circulo, clase 1 en el anillo: ninguna recta las separa
X, y = make_circles(n_samples=400, factor=0.4, noise=0.08, random_state=0)
# factor=0.4 es el radio del circulo interior; noise añade ruido a las coordenadas
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

lineal = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
# score() devuelve la exactitud (aciertos partido por filas), no la perdida
print("regresion logistica:", round(float(lineal.score(X_te, y_te)), 3))    # -> 0.425

for capas in ((2,), (8,)):
    red = MLPClassifier(hidden_layer_sizes=capas, max_iter=3000,
                        early_stopping=False, random_state=0).fit(X_tr, y_tr)
    # coefs_ es una lista con la matriz de cada capa e intercepts_ la lista de sesgos
    n_par = red.coefs_[0].size + red.intercepts_[0].size + red.coefs_[1].size + 1
    # capas es una tupla: (8,) es una capa de 8 neuronas y (8, 4) serian dos capas
    print(f"una capa de {capas[0]} neuronas:", round(float(red.score(X_te, y_te)), 3),
          " parametros:", n_par)
# -> una capa de 2 neuronas: 0.775  parametros: 9
# -> una capa de 8 neuronas: 1.0  parametros: 33

# XOR: el caso minimo que una sola neurona nunca resuelve
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])
red = MLPClassifier(hidden_layer_sizes=(8,), max_iter=5000, early_stopping=False,
                    random_state=1).fit(X_xor, y_xor)
print("XOR con capa oculta:", red.predict(X_xor), " (esperado [0 1 1 0])")   # -> [0 1 1 0]
```

:::claves
- `lineal.score(X_te, y_te)` devuelve la **exactitud**, no la pérdida ni las probabilidades: por
  dentro compara `predict` con las etiquetas verdaderas. Si quieres las probabilidades es
  `predict_proba`, y si quieres el error que se optimiza, `log_loss`.
- `MLPClassifier(...).fit(...)` **entrena y devuelve el propio modelo**, así que se puede
  encadenar dentro del `print`. No hay copia: `red` ya está entrenado y sus atributos
  (`coefs_`, `intercepts_`) solo existen después del `fit`.
- `red.coefs_` es una **lista con una matriz por capa**, no una matriz única: `coefs_[0]` son los
  pesos de la capa oculta y `coefs_[1]` los de la salida. `intercepts_` es la lista equivalente
  de sesgos, y el `+ 1` de la cuenta es el sesgo de la neurona de salida, que no aparece en
  `coefs_`.
- `hidden_layer_sizes` recibe una **tupla**: `(8,)` es una capa de 8 neuronas y `(8, 4)` serían
  dos capas. Escribir `(8)` en vez de `(8,)` no es una tupla, es el número 8, y sklearn lo
  rechaza con un error de tipos.
- `random_state=0` fija el sorteo de los pesos iniciales. Sin él, el mismo código da 0,775 o
  0,95 según la ejecución y parece que el método es inestable, cuando lo único que cambia es la
  semilla de la que arranca el descenso.
- `round(float(x), 3)` convierte antes el `numpy.float64` en un `float` de Python. No es
  decoración: `round` sobre un `numpy.float64` devuelve otro `numpy.float64` y el número de
  decimales que ves depende de cómo lo formatees después.
- `noise=0.08` en `make_circles` es lo que hace interesante el ejemplo. Con `noise=0` las dos
  clases están perfectamente separadas y la red saca 1,0 sin discusión; con ruido, un puñado de
  puntos del anillo caen dentro del disco y ninguna frontera los acierta todos.
:::

```python verificable
import numpy as np

# Una neurona es una recta: el sesgo la desplaza y el peso la gira
x = np.array([-6.0, -2.0, 0.0, 2.0, 6.0])
# np.exp se aplica al array entero: no hace falta recorrerlo con un bucle
sigmoide = 1.0 / (1.0 + np.exp(-x))
print("entradas ", x)                              # -> [-6. -2.  0.  2.  6.]
# np.round devuelve un array nuevo; `sigmoide` sigue con todos sus decimales
print("sigmoide ", np.round(sigmoide, 4))          # -> [0.0025 0.1192 0.5    0.8808 0.9975]

# El mismo peso con signo contrario niega la decision
print("w=-1, b=0:", np.round(1.0 / (1.0 + np.exp(-(-1.0 * x + 0.0))), 4))
# -> [0.9975 0.8808 0.5    0.1192 0.0025]

# Y el sesgo mueve la frontera: con w=1 y b=-2 el corte pasa por x=2
print("w=1, b=-2 :", np.round(1.0 / (1.0 + np.exp(-(1.0 * x - 2.0))), 4))
# -> [0.0003 0.018  0.1192 0.5    0.982 ]

# La sigmoide se satura: en los extremos su derivada es practicamente cero
# Se calcula en el mismo punto donde ya estaba evaluada: σ' = σ·(1 − σ)
print("derivada s(1-s):", np.round(sigmoide * (1 - sigmoide), 6))
# -> [0.002467 0.104994 0.25     0.104994 0.002467]
```

## Errores típicos

- **Olvidar el sesgo.** Sin `b`, todas las fronteras pasan por el origen y el modelo no puede
  representar ni un desplazamiento simple. Si ves que una red no aprende ni un problema
  trivial, revisa primero si has puesto sesgo.
- **Creer que apilar capas lineales sirve.** Dos capas sin activación (o con activación
  identidad) equivalen exactamente a una regresión lineal con otra matriz de pesos. Sin
  [[funciones-de-activacion|no linealidad]], más profundidad no añade capacidad.
- **Confundir el número de capas con la capacidad útil.** Una capa oculta muy ancha y una red
  profunda pueden aproximar funciones parecidas, pero no son intercambiables: con el mismo
  presupuesto de parámetros, la profundidad reutiliza representaciones y la anchura no.
- **Normalizar mal la entrada.** Una red con una variable en miles y otra en unidades tarda
  muchísimo en converger, o directamente no converge. Estandariza las entradas antes de
  entrenar, como harías con una SVM o una regresión con regularización fuerte.

:::practica
enunciado: Una neurona con tres entradas recibe x = (2, 1, 4), con pesos w = (0,5; −1,5; 0,25) y sesgo b = 0,3. Calcula la preactivación z y la salida a con sigmoide, y decide si la neurona se activa (a > 0,5). Repite el cálculo con b = −0,5 y di qué ha cambiado.
pista: z es la suma de cada entrada por su peso, más el sesgo; la sigmoide es 1/(1+e^−z), y e^−0,8 vale 0,449.
solucion: z = 0,5·2 + (−1,5)·1 + 0,25·4 + 0,3 = 1 − 1,5 + 1 + 0,3 = 0,8. Entonces a = 1/(1+0,449) = 0,690, mayor que 0,5: la neurona se activa. Con b = −0,5 queda z = 0 y a = 0,5 exacto. Los pesos no han cambiado; el sesgo solo desplaza la frontera de decisión hasta dejar la neurona justo en el límite.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué una sola neurona no puede resolver XOR?
o: Porque tiene pocos parámetros para cuatro filas
o: Porque su frontera de decisión es un hiperplano y ninguna recta separa (0,0) y (1,1) de (0,1) y (1,0)
o: Porque la función sigmoide no está definida en 0 y 1
a: 2
e: Una neurona suma pesos y sesgo: su frontera es lineal. En XOR las dos clases están en diagonales, así que cualquier recta deja un positivo y un negativo del mismo lado. Con una capa oculta, las neuronas intermedias crean variables nuevas donde el problema sí es separable.
:::

:::quiz
p: En el ejemplo de los círculos concéntricos, la red de 8 neuronas saca 1,0 en prueba y la logística 0,425. ¿Qué conclusión es correcta?
o: Que la red es mejor en cualquier problema, incluidas las tablas pequeñas
o: Que la capa oculta permite una frontera curva, y aquí la frontera real es un círculo
o: Que la regresión logística está mal implementada
a: 2
e: La logística solo puede dibujar una recta, y aquí la frontera verdadera es circular: su límite es de forma, no de implementación. Eso no implica que una red gane siempre; en datos tabulares pequeños con señal débil, el boosting suele rendir mejor con menos esfuerzo de ajuste.
:::

:::nota
El teorema de aproximación universal dice que existe una red suficientemente ancha que
aproxima cualquier función continua. No dice que el descenso de gradiente la encuentre, ni
cuántas neuronas hacen falta, ni que generalice con pocos datos. Es una garantía de capacidad,
no de aprendizaje.
:::
