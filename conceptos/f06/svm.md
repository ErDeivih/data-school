---
id: svm
titulo: Máquinas de vectores de soporte
fase: 6
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [producto-punto-y-similitud, norma-y-distancias, optimizacion-con-restricciones, escalado-y-transformacion]
tags: [clasificacion, margen, kernels, regularizacion]
resumen: Separar dos clases con el hiperplano que deja el mayor margen posible, usando solo los puntos fronterizos y un núcleo cuando la frontera no es recta.
fuentes: ["Cortes y Vapnik (1995), 'Support-Vector Networks'", "Boser, Guyon y Vapnik (1992), 'A Training Algorithm for Optimal Margin Classifiers'"]
---

## En una frase

Una máquina de vectores de soporte busca la frontera que separa dos clases dejando el mayor
hueco posible a cada lado, y solo depende de los puntos que están en el borde de ese hueco:
los vectores de soporte. Con un *núcleo* puede trazar fronteras curvas sin calcular
explícitamente las coordenadas de un espacio de dimensión mucho mayor.

## La idea

Imagina que separas dos grupos de puntos con una regla recta sobre una hoja de papel. Hay
infinitas rectas que los separan, y todas aciertan en los datos que tienes. ¿Cuál eliges? La
que pase **lo más lejos posible de los dos grupos**. La intuición es que una frontera que
roza un punto es frágil: un pequeño error de medida y ese punto cruza al otro lado.

Eso es todo el SVM lineal: maximizar el **margen**, la distancia entre la frontera y los
puntos más cercanos de cada clase. Es una idea geométrica, no probabilística: el SVM no te da
una probabilidad, te da una distancia con signo a la frontera. Y tiene una consecuencia
elegante: la solución solo depende de los puntos que tocan el borde del margen. Los del
interior podrían moverse mientras no crucen ese borde sin cambiar la frontera. Esos puntos
fronterizos son los **vectores de soporte**, y de ahí el nombre.

El segundo ingrediente aparece cuando las clases no se separan con una recta. Un truco
conocido: si los puntos están en un círculo interior (clase A) rodeado de un anillo (clase B),
no hay recta que los separe, pero el círculo `x² + y² = r²` sí. Elevar las variables al
cuadrado convierte el problema en linealmente separable en un espacio de más dimensiones. El
SVM lleva esa idea al extremo con el **truco del núcleo**: en toda la formulación los datos
aparecen únicamente como productos punto `xᵢ·xⱼ`, así que se puede sustituir ese producto por
una función de núcleo `K(xᵢ, xⱼ)` que equivale a un producto punto en un espacio de dimensión
altísima. Nunca se calculan esas coordenadas: se calcula directamente el parecido. Y queda una
frontera curva en el espacio original, con el mismo coste que una recta.

El precio: hay que **escalar las variables**. El SVM mide distancias, y una variable que se
mueve entre 0 y 1 pesa lo mismo que otra que se mueve entre 0 y 100.000 si no se estandarizan.
Es su supuesto más frágil en la práctica.

## Definición formal

Con datos `(xᵢ, yᵢ)`, `i = 1 … n`, donde `yᵢ ∈ {−1, +1}`, el SVM lineal con margen duro busca

:::formula
min ½ · /w/²   sujeto a   yᵢ (w·xᵢ + b) ≥ 1 para todo i
:::

- `w` — vector normal al hiperplano; su dirección es perpendicular a la frontera.
- `b` — sesgo (término independiente); desplaza el hiperplano del origen.
- `w·xᵢ + b = 0` — la frontera de decisión.
- `yᵢ (w·xᵢ + b) ≥ 1` — cada punto cae al menos una unidad del lado correcto.
- `/w/` — la norma euclídea de `w`; el margen total entre las dos clases vale `2 / /w/`, así
  que minimizar `½ /w/²` es maximizar el margen.

Con margen **blando** —el que se usa siempre, porque los datos reales se solapan— se añaden
holguras `ξᵢ ≥ 0` y un coste `C`:

:::formula
min ½ · /w/² + C · Σᵢ ξᵢ   sujeto a   yᵢ (w·xᵢ + b) ≥ 1 − ξᵢ,  ξᵢ ≥ 0
:::

- `ξᵢ` — cuánto se permite que el punto `i` invada el margen o caiga del lado equivocado.
- `C` — cuánto pesa cada violación frente al tamaño del margen. `C` grande = margen estrecho
  y pocos errores en entrenamiento (sobreajuste); `C` pequeño = margen ancho y más errores
  tolerados (sesgo).

La formulación dual, que es la que se resuelve en la práctica, expresa la solución como
combinación de productos punto:

:::formula
f(x) = Σᵢ αᵢ yᵢ K(xᵢ, x) + b,  con αᵢ ≥ 0
:::

- `αᵢ` — multiplicadores de Lagrange; valen 0 para casi todos los puntos y son positivos
  exactamente en los vectores de soporte.
- `K(·, ·)` — el núcleo. Lineal `xᵢ·xⱼ`, polinómico `(γ xᵢ·xⱼ + r)^d`, o gaussiano (RBF)
  `exp(−γ /xᵢ − xⱼ/²)`.
- `γ` — en RBF, cuánto decae la influencia de un punto con la distancia; `γ` alto = frontera
  muy ajustada a cada punto.

El número de vectores de soporte es la medida de complejidad real del modelo: cuanto más
grande, más cerca está de sobreajustar.

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa con el margen si sube |
| --- | --- | --- | --- |
| `w` | Vector normal al hiperplano: su dirección es perpendicular a la frontera | las de las variables | El margen es `2 / ‖w‖`: al subir `‖w‖`, el pasillo se **estrecha** |
| `b` | Sesgo: desplaza el hiperplano sin girarlo | las de las variables | No cambia ni el ancho del margen ni su orientación, solo dónde cae la frontera |
| `C` | Cuánto pesa cada punto mal clasificado o dentro del margen | adimensional | Ancho si `C` es pequeño (tolera invadir) y estrecho si es grande; con `C` enorme el margen se pega a los datos y aparece el sobreajuste |
| `ξᵢ` | Holgura: cuánto se permite invadir el margen el punto `i` | las de las variables | Con `C` pequeño, las holguras compensan: es el precio de ensanchar el pasillo |
| `αᵢ` | Multiplicador de Lagrange de cada punto en la formulación dual | adimensional | Vale 0 en casi todos los puntos y es positivo solo en los vectores de soporte: subirlo implica que ese punto sujeta la frontera |
| `K(xᵢ, xⱼ)` | Núcleo: parecido entre dos puntos que equivale a un producto punto en otra dimensión | las derivadas del núcleo | Define el margen en ese espacio; la frontera puede ser curva |
| `γ` (núcleo RBF) | Cuánto decae la influencia de un punto al alejarse | 1 / (unidades²) | No cambia el margen del hiperplano, cambia su forma: `γ` alto ajusta cada punto y encoje la zona de influencia (sobreajuste) |
| `d` (núcleo polinómico) | Grado del polinomio | adimensional | Más combinaciones de variables: sube la capacidad y también el sobreajuste |
| Nº de vectores de soporte | Puntos que quedan justo en el borde o dentro del margen | puntos | Cuantos más, más puntos sujetan la frontera y más inestable es el modelo |
:::

## Ejemplo

Tres puntos en el plano:

```
clase -1:  A = (2, 3)   B = (2, 1)
clase +1:  C = (3, 3)
```

El hiperplano `w = (2, 0)`, `b = −5` da `w·x + b = 2x − 5`: vale `−1` en A y B y `+1` en C.
Todos cumplen `yᵢ(w·xᵢ + b) = 1`, es decir, están **sobre** el borde del margen. El margen
total es `2 / /w/ = 2/2 = 1`. Con `C` enorme, este es exactamente el clasificador que devuelve
un SVM lineal: los tres puntos son vectores de soporte.

Baja ahora `C` a 0,05 (mucha regularización) y la solución cambia de naturaleza: el modelo
prefiere un margen ancho antes que acertar. Con los mismos datos, sklearn devuelve
`w = (0,05, 0)` y `b = −1,10`; los valores de decisión pasan a ser `−1`, `−1` y `−0,95`, es
decir, **el punto C cae del lado equivocado**. Has ganado un margen de 40 a cambio de un error
de entrenamiento. Ese compromiso es el hiperparámetro `C`, y no hay forma de elegirlo sin
validación.

:::figura
fichero: svm-margen-y-parametro-c
pie: El panel izquierdo es el SVM tal y como se explica: la frontera se coloca donde deja el pasillo más ancho y solo los puntos que tocan ese pasillo (los tres anillados) la sujetan; los demás podrían moverse sin cambiar nada. Esa es la diferencia con la regresión logística, donde todas las observaciones empujan la frontera. El panel derecho muestra qué hace `C` con ese pasillo, en escala logarítmica: al subirlo, el margen se estrecha de más de 4 a 1,5 y el modelo se pega a los datos, hasta que dejarlo crecer ya no mejora el acierto. La lectura práctica es que `C` es el mando de sesgo-varianza del SVM y se elige con validación, no por defecto.
fuente: figuras/svm-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.svm import SVC

# El margen se ve a mano: w=(2,0), b=-5 deja los tres puntos justo en el borde.
X = np.array([[2.0, 3.0], [2.0, 1.0], [3.0, 3.0]])
y = np.array([-1, -1, 1])

for C in (1e6, 0.05):
    m = SVC(kernel="linear", C=C).fit(X, y)
    w = m.coef_[0]
    print(f"C={C:<9g} w=({w[0]:+.2f},{w[1]:+.2f}) b={m.intercept_[0]:+.2f} "
          f"margen={2 / np.linalg.norm(w):.2f} soporte={[int(i) for i in m.support_]}")
    print("   valores de decision:", np.round(m.decision_function(X), 2))
# -> C=1e+06     w=(+2.00,+0.00) b=-5.00 margen=1.00 soporte=[0, 1, 2]
# ->    valores de decision: [-1. -1.  1.]
# -> C=0.05      w=(+0.05,+0.00) b=-1.10 margen=40.00 soporte=[0, 1, 2]
# ->    valores de decision: [-1.   -1.   -0.95]
```

:::claves
- `m.coef_[0]` devuelve **una lista de vectores**, uno por clase, aunque el problema tenga dos
  clases: de ahí el `[0]` para quedarte con el `w`. `m.intercept_` es un array de un elemento, por
  eso el código pide `m.intercept_[0]` y no el array entero.
- `m.support_` son **índices** de las filas, no las filas. Para recuperar los puntos hay que
  indexar: `X[m.support_]`. Confundirlo es el error más habitual al dibujar un SVM.
- `2 / np.linalg.norm(w)` es el ancho del margen **solo** con núcleo lineal. Con RBF no existe
  `w` en el espacio original y `coef_` tiene otra forma: ese cálculo deja de tener sentido.
- `C=1e6` no es «margen duro» exacto, es la forma de pedirlo en la práctica: un castigo tan grande
  por cada violación que la solución es la de margen duro. Con datos que se solapan, valores así
  producen sobreajuste.
- `C=0.05` da `w = (0,05, 0)`: casi un vector nulo. El margen se dispara a 40 precisamente porque
  `2 / ‖w‖` divide entre una norma diminuta, y con él se cuela un punto mal clasificado. La métrica
  no es de fiar cuando el margen es enorme por esta razón.
- `f"C={C:<9g}"` usa el formato `g`, que elige solo la notación científica cuando hace falta: por eso
  el mismo `f-string` imprime `1e+06` y `0.05` sin que tengas que cambiar nada.
- En el segundo bloque, `y = np.where(X[:, 0] * X[:, 1] > 0, 1, -1)` construye el XOR: los puntos
  de los cuadrantes primero y tercero a un lado. Con núcleo lineal la exactitud es 0,540, es decir,
  azar; con un polinomio de grado 2 sube a 0,965. Ese salto es el truco del núcleo, no un cambio de
  optimizador.
:::

```python verificable
import numpy as np
from sklearn.svm import SVC

# El truco del nucleo: XOR no es separable con una recta, con un polinomio de grado 2 si.
rng = np.random.default_rng(0)
X = rng.normal(size=(200, 2))
y = np.where(X[:, 0] * X[:, 1] > 0, 1, -1)   # dos cuadrantes opuestos

for nombre, params in (("linear", {}),
                       ("poly", {"degree": 2, "gamma": 1.0, "coef0": 1.0}),
                       ("rbf", {"gamma": 1.0})):
    m = SVC(kernel=nombre, C=1.0, **params).fit(X, y)
    print(f"{nombre:>6}  exactitud {m.score(X, y):.3f}  vectores de soporte {len(m.support_)} de {X.shape[0]}")
# -> linear  exactitud 0.540  vectores de soporte 192 de 200
# ->   poly  exactitud 0.965  vectores de soporte 52 de 200
# ->    rbf  exactitud 0.980  vectores de soporte 82 de 200
```

## Errores típicos

- **No escalar las variables.** Es el error que más rendimiento destroza. Con RBF, una
  variable con rango 1.000 domina por completo el cálculo de distancias y las demás dejan de
  contar. Estandariza siempre antes, dentro del
  [[pipelines-de-ml|pipeline de machine learning]] para que el escalado se ajuste solo con el
  conjunto de entrenamiento.
- **Elegir `C` y `γ` con los valores por defecto.** `C = 1` y `gamma = 'scale'` son un punto de
  partida, no una respuesta. Con `C` demasiado grande el modelo hace islas alrededor de cada
  punto (memoriza); con `γ` demasiado grande, lo mismo en RBF. Busca en una rejilla
  logarítmica de `C` y `γ`.
- **Esperar probabilidades de `decision_function`.** Lo que devuelve el SVM es una distancia
  con signo, no una probabilidad calibrada. Si necesitas probabilidades, activa
  `probability=True` (que usa una calibración de Platt interna y encarece el entrenamiento) o
  calibra aparte. Un `0,3` de un SVM sin calibrar no significa «30 % de probabilidad».
- **Usar SVM con datasets muy grandes sin pensarlo.** El entrenamiento es entre cuadrático y
  cúbico en el número de filas en el caso general y no escala como los árboles. Con más de
  unas decenas de miles de filas, un [[gradient-boosting|gradient boosting]] o una regresión
  logística suelen dar resultados parecidos en una fracción del tiempo.
- **Ignorar el desbalanceo de clases.** El SVM con `C` simétrico trata igual los dos tipos de
  error. Si una clase es el 2 % de los datos, sube `class_weight='balanced'` o ajusta el
  umbral; si no, el modelo aprende a predecir siempre la clase mayoritaria.
- **Interpretar los vectores de soporte como «los datos importantes del negocio».** Son los
  puntos que definen la frontera de este modelo concreto, no los casos más relevantes ni los
  más difíciles de explicar.

:::practica
enunciado: Un SVM lineal ha aprendido w = (1, 2) y b = −4, con etiquetas en {−1, +1}. Calcula el valor de decisión del punto (3, 1), su clase y el margen total del modelo. ¿Ese punto es un vector de soporte?
pista: El valor de decisión es w·x + b, el signo da la clase y el margen es dos dividido entre la norma de w.
solucion: w·x + b = 1·3 + 2·1 − 4 = 1, positivo, luego la clase es +1. La norma es √(1² + 2²) = √5 = 2,236, así que el margen total vale 2/2,236 = 0,894. El valor de decisión es exactamente 1, el borde del margen, así que el punto es un vector de soporte: cualquier punto con un valor mayor en valor absoluto caería fuera y podría moverse sin alterar la frontera.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué son los vectores de soporte de un SVM entrenado?
o: Todos los puntos de entrenamiento que el modelo clasifica correctamente
o: Los puntos de entrenamiento que tocan o violan el borde del margen, y que son los únicos que determinan la frontera
o: Los dos puntos más alejados de cada clase
a: 2
e: La solución dual asigna `αᵢ = 0` a los puntos que quedan holgadamente dentro de su lado: podrías moverlos sin cambiar la frontera. Los vectores de soporte son los que tienen `αᵢ > 0`, es decir, los que están sobre el margen, dentro de él o mal clasificados.
:::

:::quiz
p: Un SVM con núcleo RBF clasifica perfectamente el entrenamiento pero falla en prueba. ¿Qué tocas primero?
o: Añadir más variables al modelo
o: Bajar `C` y bajar `γ`, porque la frontera se está ajustando a cada punto
o: Cambiar el núcleo a lineal, que siempre generaliza mejor
a: 2
e: `C` alto penaliza muchísimo cada error de entrenamiento y `γ` alto hace que la influencia de cada punto decaiga muy rápido: juntos producen islas alrededor de las observaciones. Bajando ambos, el margen se ensancha y la frontera se suaviza. El núcleo lineal no es siempre mejor: puede quedarse corto si la frontera es de verdad curva.
:::

:::aviso
El SVM fue durante los años noventa y dos mil el clasificador de referencia, y en datos
tabulares de tamaño medio sigue siendo competitivo. Pero no da importancia de variables
directamente, no da probabilidades sin calibración adicional y su coste de entrenamiento
crece muy rápido con las filas. Si tu problema es tabular, grande y con variables
heterogéneas, empieza por los árboles con boosting.
:::
