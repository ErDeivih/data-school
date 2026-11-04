---
id: seleccion-de-hiperparametros
titulo: Búsqueda de hiperparámetros
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [train-val-test, validacion-cruzada, sesgo-varianza, regularizacion-l1-l2]
tags: [optimizacion, validacion, presupuesto, practica]
resumen: Rejilla, búsqueda aleatoria, bayesiana y Hyperband: cómo repartir el presupuesto de entrenamientos sin sobreajustar la validación.
fuentes: ["Bergstra y Bengio (2012), 'Random Search for Hyper-Parameter Optimization'", "Snoek et al. (2012), 'Practical Bayesian Optimization of Machine Learning Algorithms'"]
---

## En una frase

Los hiperparámetros son las decisiones que tomas tú antes de entrenar (profundidad del
árbol, `C` de la SVM, tasa de aprendizaje) y buscarlos consiste en probar combinaciones,
medirlas con [[validacion-cruzada|validación cruzada]] y quedarte con la mejor, gastando el
menor número de entrenamientos posible.

## La idea

Entrenar un modelo es barato de describir y caro de repetir. Cada vez que cambias un
hiperparámetro hay que volver a ajustar los pesos y volver a validar. Si tienes 5
hiperparámetros y quieres probar 10 valores de cada uno, la rejilla tiene 10⁵ = 100.000
combinaciones: con 30 segundos por entrenamiento son 35 días de cómputo. Nadie hace eso.

La primera intuición (y la equivocada) es «cuanto más fina la rejilla, mejor». El problema
es que la rejilla crece de forma exponencial con el número de dimensiones: en 10 dimensiones
una rejilla de solo 2 valores por eje ya son 1.024 entrenamientos, y cada eje queda sondeado
en **dos únicos puntos**. Ese es el argumento de la búsqueda aleatoria: con el mismo
presupuesto, cada intento aleatorio es un punto nuevo en todas las dimensiones a la vez, así
que ningún eje se queda sin explorar. Y en la práctica solo unos pocos hiperparámetros
importan de verdad; los demás se pueden dejar en un valor razonable.

La segunda intuición es que se puede aprender del historial. Si ya has probado 20
combinaciones, sabes dónde estuvo bien y dónde mal: la búsqueda bayesiana construye un
modelo sustituto (habitualmente un proceso gaussiano) de la función
«hiperparámetros → puntuación» y elige el siguiente punto donde ese sustituto cree que hay
mejora. Con evaluaciones caras (minutos u horas) ahorra muchos entrenamientos; con
evaluaciones de un segundo, el coste de decidir supera al de entrenar y no compensa.

La tercera es rendirse a tiempo. Hyperband y ASHA no eligen mejores puntos: asignan a cada
configuración un presupuesto pequeño (pocas épocas), tiran la mitad de las peores, doblan el
presupuesto de las supervivientes y repiten. Es el mismo principio que un torneo: es mucho
más barato descubrir que una configuración es mala con 5 épocas que con 200.

## Definición formal

Sea `f(θ)` la puntuación media en validación cruzada de una configuración `θ = (θ₁, …, θ_d)`,
donde `d` es el número de hiperparámetros. Buscar es resolver:

:::formula
θ* = argmax f(θ)   con   θ ∈ Θ = Θ₁ × Θ₂ × … × Θ_d
:::

- `θ` — una configuración concreta; cada `θᵢ` es un hiperparámetro (por ejemplo `C = 1,0`).
- `Θᵢ` — el conjunto de valores permitidos para ese hiperparámetro; puede ser discreto
  (`[16, 32, 64]`), continuo (`[0, 1]`) o logarítmico (`10^[-3, 3]`).
- `f(θ)` — la métrica que eliges (exactitud, AUC, RMSE) promediada sobre los pliegues. Es
  ruidosa: dos ejecuciones con la misma `θ` pueden dar puntuaciones distintas.
- `θ*` — la configuración que se lleva a producción.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `θ` | Una configuración concreta de hiperparámetros (por ejemplo `C = 1,0` y `gamma = 0,1`) | las de cada hiperparámetro | No es algo que «suba»: mover `θ` mueve la puntuación, y eso es justo lo que se explora |
| `Θᵢ` | El conjunto de valores permitidos para el hiperparámetro `i` | las de ese hiperparámetro | Un rango más ancho multiplica el trabajo y, con presupuesto fijo, deja cada zona menos sondeada |
| `d` | Número de hiperparámetros que se buscan a la vez | dimensiones | Cada dimensión nueva multiplica el tamaño de la rejilla: con `d = 5` y 10 valores por eje son 100.000 entrenamientos |
| `f(θ)` | Puntuación media en validación cruzada de esa configuración | unidades de la métrica (exactitud, AUC, R²) | Es la señal que guía la búsqueda, y es ruidosa: la misma `θ` repetida puede dar números distintos |
| `N` | Número de configuraciones evaluadas, es decir el presupuesto | intentos | El máximo de `N` mediciones ruidosas crece con `N` aunque ninguna configuración sea mejor: el resultado se vuelve más optimista |
| `θ*` | La configuración que se lleva a producción | las de cada hiperparámetro | Se elige como el máximo de `f`, así que su puntuación no es una estimación insesgada de lo que rendirá |
:::

Los cuatro esquemas se distinguen por cómo eligen la secuencia de puntos:

| Esquema | Cómo elige el siguiente punto | Coste típico | Cuándo usarlo |
| --- | --- | --- | --- |
| Rejilla | En orden, todos los de un producto cartesiano | `Πᵢ nᵢ` entrenamientos | 1-2 hiperparámetros y valores ya acotados |
| Aleatoria | Uniforme (o log-uniforme) dentro de cada `Θᵢ` | El presupuesto que fijes | Punto de partida por defecto |
| Bayesiana | Maximiza una utilidad sobre un sustituto de `f` | 20-100 evaluaciones caras | Cada evaluación cuesta minutos u horas |
| Hyperband / ASHA | Elimina las malas con poco presupuesto y dobla a las buenas | Presupuesto total repartido en rondas | Modelos iterativos: redes, boosting |

Dos detalles que se olvidan y arruinan la búsqueda:

1. **Muestrea en escala logarítmica** los hiperparámetros multiplicativos. Un `C` de SVM
   entre 0,001 y 1.000 muestreado uniforme deja el 99,9 % de los puntos por encima de 1.
2. **El máximo de `N` intentos no es una estimación insesgada** de `f(θ*)`: es el máximo de
   `N` variables ruidosas, y su esperanza crece con `N` aunque todas las configuraciones sean
   igual de buenas. Ese sesgo se corrige con un conjunto externo que la búsqueda no haya
   tocado, o con [[validacion-cruzada|validación anidada]].

## Ejemplo

Una SVM de núcleo RBF con 60 muestras, 6 variables y 5 pliegues. Buscamos `C` y `gamma`:

```
rejilla:  C en {0,1; 1; 10}  x  gamma en {scale; 0,1; 1}  ->  9 combinaciones
mejor resultado: C = 1, gamma = scale  ->  exactitud media en validación 0,850
```

Ahora cuatro intentos aleatorios con el mismo rango para `C`, en escala logarítmica (`gamma`
va de 0,01 a 1), y una quinta parte del presupuesto (4 entrenamientos contra 9): el mejor de
los cuatro da **0,833** con `C = 1,63` y `gamma = 0,288`. Está a 0,017 del óptimo de la
rejilla habiendo gastado menos de la mitad. En dos dimensiones eso es suerte; en diez
dimensiones es la diferencia entre explorar cada eje o no explorarlo:

```
rejilla de 2 valores por eje en 4 dimensiones: 16 puntos, 2 valores distintos por eje
9 puntos aleatorios en 4 dimensiones:           9 puntos, 9 valores distintos por eje
```

La rejilla gasta 16 entrenamientos y solo prueba dos valores de cada hiperparámetro. Nueve
puntos aleatorios prueban nueve valores distintos de cada uno.

:::figura
fichero: seleccion-de-hiperparametros-rejilla-vs-aleatoria
pie: A la izquierda, los dos diseños con el mismo presupuesto de nueve intentos. La rejilla (cuadrados) cae siempre sobre las mismas tres rectas de puntos: por muchos entrenamientos que gaste, cada eje queda sondeado en tres valores. Los nueve puntos de la aleatoria no comparten coordenada, así que cada intento es información nueva en las dos dimensiones a la vez; con dos ejes la diferencia es pequeña, pero con diez es la diferencia entre explorar o no explorar. A la derecha, sesenta configuraciones idénticas en calidad: la línea de puntos es el nivel real y la roja sube sola. Ese crecimiento es el sesgo del máximo de `N`, y es la razón de que el mejor resultado de una búsqueda no se pueda reportar como rendimiento esperado. Cuanto más grande sea el presupuesto, más alta será la cifra que devuelve el buscador sin que el modelo haya mejorado nada.
fuente: figuras/seleccion-de-hiperparametros-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score

# 60 muestras, 6 variables: una rejilla pequena cabe entera y se puede leer
X, y = make_classification(n_samples=60, n_features=6, n_informative=3,
                           n_redundant=0, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)   # baraja antes de partir, con semilla fija
rejilla = {"C": [0.1, 1.0, 10.0], "gamma": ["scale", 0.1, 1.0]}   # 9 combinaciones

# SVC va SIN ajustar: el buscador clona el modelo en cada pliegue y en cada combinacion
busqueda = GridSearchCV(SVC(kernel="rbf"), rejilla, cv=cv, scoring="accuracy").fit(X, y)
print("combinaciones evaluadas:", len(busqueda.cv_results_["params"]))   # -> 9
print("mejor C y gamma        :", busqueda.best_params_)                 # -> {'C': 1.0, 'gamma': 'scale'}
print("mejor accuracy en CV   :", round(busqueda.best_score_, 3))       # -> 0.85

# La aleatoria gasta 4 intentos en vez de 9 y muestrea en escala logaritmica
rng = np.random.default_rng(0)
mejores = []
for _ in range(4):
    C = float(10 ** rng.uniform(-1, 1))    # de 0,1 a 10
    g = float(10 ** rng.uniform(-2, 0))    # de 0,01 a 1
    s = cross_val_score(SVC(kernel="rbf", C=C, gamma=g), X, y, cv=cv).mean()
    mejores.append((round(float(s), 3), round(C, 2), round(g, 3)))
print("mejor de 4 aleatorias  :", max(mejores))   # -> (0.833, 1.63, 0.288)
```

:::claves
- `GridSearchCV(...).fit(X, y)` devuelve el propio buscador, no el modelo. Para predecir se usa `busqueda.best_estimator_` o `busqueda.predict`, que delega en él. `best_params_` y `best_score_` llevan guion bajo final porque no existen hasta después de ajustar.
- `busqueda.cv_results_["params"]` es una lista con un diccionario por combinación, y su longitud (9) es el número de entrenamientos, no el de hiperparámetros. `cv_results_` trae además la media y la desviación de cada combinación, que es lo que hace falta para saber si la diferencia entre dos candidatas es ruido.
- `gamma="scale"` es una cadena, no un número: scikit-learn la sustituye por `1 / (n_variables · X.var())`. Por eso la rejilla mezcla texto y números sin fallar, y por eso dos conjuntos con distinta escala dan `gamma` distinto con la misma rejilla.
- `cross_val_score(...).mean()` devuelve un `np.float64`, y `float(s)` lo convierte a un `float` de Python. Sin esa conversión el `max(mejores)` sigue funcionando, pero al imprimir sale `np.float64(0.833)` en NumPy 2 y las comparaciones con `==` contra un `float` corriente se vuelven frágiles.
- `10 ** rng.uniform(-1, 1)` muestrea `C` en escala logarítmica: la mitad de los intentos cae por debajo de 1 y la otra mitad por encima. Con `rng.uniform(0.1, 10)` el 91 % de los puntos quedaría por encima de 1 y el rango pequeño no se exploraría.
- Cambia `range(4)` por `range(100)`: el mejor de los intentos sube aunque el modelo no mejore nada. Es exactamente el sesgo del máximo de la figura, y la razón de que la búsqueda tenga que reservar un conjunto externo.
:::

```python ilustrativo
# Busqueda bayesiana con Optuna: el sustituto decide el siguiente punto
# (necesita la libreria optuna, fuera de las permitidas en un bloque verificable)
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

def objetivo(trial):
    C = trial.suggest_float("C", 1e-3, 1e3, log=True)       # log=True: uniforme en el exponente
    gamma = trial.suggest_float("gamma", 1e-4, 1e0, log=True)
    return cross_val_score(SVC(kernel="rbf", C=C, gamma=gamma), X, y, cv=cv).mean()

estudio = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=0))
estudio.optimize(objetivo, n_trials=60, timeout=3600)   # 60 evaluaciones o una hora
print(estudio.best_params, estudio.best_value)
```

## Errores típicos

- **Buscar hiperparámetros con el conjunto de prueba delante.** Si eliges la configuración
  comparando en el mismo conjunto con el que luego reportas el resultado, ese número está
  sesgado al alza. La búsqueda vive dentro de validación; el test se abre una sola vez.
- **Informar del mejor valor de validación como rendimiento esperado.** El máximo de 100
  intentos está sesgado al alza: cuanto más buscas, mejor parece y no mejor es. Para tener una
  estimación honesta necesitas un conjunto externo o validación anidada.
- **Explorar en escala lineal lo que es multiplicativo.** `C`, `gamma`, `alpha`, la tasa de
  aprendizaje y las profundidades se buscan en log. En escala lineal malgastas casi todo el
  presupuesto en el extremo grande del rango.
- **Rejilla con muchos hiperparámetros.** Cinco hiperparámetros y diez valores por eje son
  100.000 entrenamientos, y cada eje se sondea solo en diez puntos. Si quieres rejilla, que
  sea sobre los dos o tres hiperparámetros que importan.
- **Aleatorizar el orden y quedarse con la mejor de una única partición.** Con
  [[validacion-cruzada|K-fold]] y semilla fija, la diferencia entre dos configuraciones puede
  ser ruido del reparto. Repite con varias semillas antes de declarar un ganador.
- **Dejar el presupuesto abierto.** Sin límite de tiempo, de intentos o de épocas, una
  búsqueda puede consumir una semana de GPU para mejorar 0,002 en la métrica. Fija el
  presupuesto antes de empezar y anota cuánto has gastado.

:::practica
enunciado: Buscas el `C` de una SVM en el rango 0,001 a 1.000. Calcula qué fracción del rango cae por encima de 1 si muestreas uniforme en escala lineal y qué fracción si muestreas uniforme en escala logarítmica. Decide qué escala usar.
pista: En lineal, la fracción es (1000 − 1) / (1000 − 0,001). En logarítmica, cuenta la parte del exponente que supera 0 dentro de [−3, 3].
solucion: Lineal: (1000 − 1)/(1000 − 0,001) = 999/999,999 = 0,999, así que el 99,9 % de los puntos cae por encima de 1 y el rango pequeño queda prácticamente sin explorar. Logarítmica: el exponente va de −3 a 3, y C > 1 corresponde al exponente mayor que 0, es decir 3 de los 6 tramos: el 50 %. Muestrea en logarítmica, que reparte el presupuesto por décadas.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la búsqueda aleatoria suele batir a la rejilla con el mismo presupuesto?
o: Porque prueba valores que la rejilla no incluye y cada intento es un punto nuevo en todos los ejes a la vez
o: Porque evalúa más combinaciones que la rejilla para el mismo número de entrenamientos
o: Porque no necesita validación cruzada
a: 1
e: Con 9 intentos en 10 dimensiones la rejilla prueba 2 valores por eje, mientras que 9 puntos aleatorios prueban 9 valores distintos por eje. No evalúa más combinaciones: evalúa exactamente las mismas 9. Y la validación cruzada sigue siendo imprescindible.
:::

:::quiz
p: El mejor resultado de una búsqueda de 200 configuraciones es 0,91 en validación. ¿Qué significa?
o: Que el modelo acierta aproximadamente el 91 % en datos nuevos
o: Que 0,91 es el máximo de 200 mediciones ruidosas y probablemente esté por encima de lo que rendirá en datos nuevos
o: Que la configuración elegida es la mejor de todas las posibles
a: 2
e: El máximo de muchas mediciones ruidosas crece con el número de intentos aunque todas las configuraciones sean equivalentes. Por eso hay que estimar el rendimiento final con datos que la búsqueda no haya usado. Tampoco es la mejor de todas las posibles: solo es la mejor de las 200 probadas.
:::

:::trampa
Si tu búsqueda de hiperparámetros ha tocado 500 configuraciones y luego mides el resultado
final con el mismo K-fold que usaste para elegir, el número que sale no es una estimación:
es el mejor de 500. Reserva un conjunto externo desde el principio o haz validación anidada.
:::
