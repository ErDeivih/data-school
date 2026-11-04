---
id: sesgo-varianza
titulo: Compromiso sesgo-varianza
fase: 6
nivel: intermedio
rutas: [core, ds]
prerequisitos: [sesgo-varianza-mse, metricas-de-regresion]
tags: [machine-learning, sobreajuste, generalizacion]
resumen: El error al predecir datos nuevos se reparte entre ruido irreducible, sesgo y varianza; la curva que explica por qué más complejo no siempre es mejor.
fuentes: ["Geman, Bienenstock y Doursat (1992), 'Neural Networks and the Bias/Variance Dilemma'", "Hastie, Tibshirani y Friedman (2009), 'The Elements of Statistical Learning', cap. 7"]
---

## En una frase

El error de un modelo sobre datos nuevos se descompone en tres piezas que se suman: el ruido
irreducible de los datos, el sesgo (lo que el modelo se equivoca siempre en la misma dirección) y la
varianza (lo que cambian sus predicciones al cambiar la muestra de entrenamiento), y aumentar la
complejidad baja el sesgo pero sube la varianza.

## La idea

Dos tiradores de dardos. El primero agrupa todos sus tiros en un círculo pequeño, pero el círculo
está desplazado del centro: tiene mucha precisión y **sesgo**. El segundo acierta de media en el
centro, pero sus tiros se reparten por toda la diana: no tiene sesgo y tiene mucha **varianza**. Un
modelo de machine learning es ambos tiradores a la vez, y la diana es el conjunto de datos nuevos.

Se ve muy bien con dos extremos:

- Un modelo que **siempre predice la media** de la variable objetivo (complejidad mínima) tiene un
  sesgo enorme y una varianza casi nula: cambia la muestra de entrenamiento y su predicción apenas
  se mueve, pero se equivoca siempre en la misma dirección en cuanto la relación no es constante.
- Un **polinomio de grado 20** que pasa por los 21 puntos de entrenamiento tiene un sesgo nulo *en
  esos puntos* y una varianza enorme: cambia un solo valor y la curva entera se retuerce, incluidas
  las zonas donde no había datos.

La consecuencia práctica es la curva en forma de U que aparece en el ejemplo: el error sobre datos
nuevos baja al principio (el sesgo cae más deprisa de lo que sube la varianza), llega a un mínimo y
luego sube. Ese mínimo no está en el modelo más complejo ni en el más simple. Y explica por qué cada
palanca actúa sobre una pieza distinta:

- **Más datos** reducen la varianza, no el sesgo. Si tu modelo no puede representar la relación, mil
  filas más no arreglan nada.
- **Regularizar** ([[regularizacion-l1-l2]]) sube el sesgo a cambio de bajar la varianza: es un
  intercambio explícito, no una mejora gratuita.
- **Promediar modelos** (bagging, bosques aleatorios) reduce la varianza sin tocar el sesgo.
- **Mejores variables** ([[ingenieria-de-features]]) reducen el sesgo, porque acercan el modelo a la
  relación real.

Dos matices que conviene tener presentes. El primero: la descomposición exacta es del error
cuadrático; para la exactitud o el AUC es una guía, no una igualdad. El segundo: con modelos muy
sobreparametrizados (redes grandes, bosques profundos) se ha observado que el error puede volver a
bajar después de subir, el fenómeno de la *doble bajada*; la curva en U describe el régimen clásico,
no una ley universal.

## Definición formal

Sea `y = f(x) + ε`, con `f` la función de regresión verdadera, `ε` un ruido con media 0 y varianza
`σ²`, e independiente de `x`. Sea `f̂` el modelo estimado con una muestra de entrenamiento `D`, y
`x₀` un punto nuevo. Entonces:

:::formula
E[ (y₀ − f̂(x₀))² ] = σ²  +  ( E[f̂(x₀)] − f(x₀) )²  +  E[ ( f̂(x₀) − E[f̂(x₀)] )² ]
:::

- `y₀` — la observación nueva en `x₀`, es decir `f(x₀) + ε`.
- `E[·]` — la esperanza sobre **todas** las muestras de entrenamiento posibles y sobre el ruido de
  `y₀`. Es la parte que se olvida: el sesgo y la varianza no son propiedades de un modelo concreto,
  son propiedades del procedimiento de ajuste.
- `σ²` — el **ruido irreducible**: la varianza del error de los datos. No se puede bajar con ningún
  modelo, porque no depende de él.
- `( E[f̂(x₀)] − f(x₀) )²` — el **sesgo al cuadrado**: cuánto se desvía, de media, la predicción del
  valor verdadero.
- `E[ ( f̂(x₀) − E[f̂(x₀)] )² ]` — la **varianza**: cuánto oscila la predicción alrededor de su propia
  media al cambiar la muestra.

Tres consecuencias que se usan a diario:

1. **La suma es el error esperado de predicción.** Con `σ² = 0,09`, un sesgo al cuadrado de 0,0056 y
   una varianza de 0,0120, el error esperado es `0,09 + 0,0056 + 0,0120 = 0,1076`; su raíz es 0,33,
   el orden de magnitud del ruido.
2. **La varianza crece con el número de parámetros.** En el modelo lineal con columnas ortogonales,
   la varianza media del ajuste es `σ² · p / n`, con `p` el número de parámetros y `n` el número de
   observaciones. Duplicar variables sin duplicar datos duplica la varianza.
3. **La desviación típica del error estimado no es la del ruido.** Comparar el error de un modelo
   con `σ` solo tiene sentido si `σ` se ha estimado aparte; si no, estás comparando el total con una
   de sus partes.

:::figura
fichero: sesgo-varianza-descomposicion-y-ajuste
pie: A la izquierda, los tres sumandos del error esperado, medidos con 300 muestras de 30 puntos cada una. El sesgo al cuadrado (azul) se desploma del grado 0 al 5 y a partir de ahí ya no baja; la varianza (roja) sube sin parar, y la suma (morada) tiene su mínimo en el grado 3, no en el 9. A la derecha, la misma muestra con dos ajustes: el grado 3 sigue la curva verdadera, y el grado 9 se retuerce para pasar por los puntos y falla en los huecos. Conclusión: el modelo se elige en el mínimo del error de validación, y pasarse de complejidad cuesta varianza sin comprar nada de sesgo.
fuente: figuras/sesgo-varianza-1.py
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `σ²` | El ruido irreducible: la varianza del error de los datos | unidades de `y` al cuadrado | Sube el suelo del error y nada lo baja: no depende del modelo. Si tu error ya está pegado a `σ`, el problema es de datos o de medida, no de algoritmo |
| `p` | El número de parámetros del modelo | adimensional | La varianza media del ajuste crece como `σ² · p / n`. Duplicar variables sin duplicar filas duplica la varianza: ahí nace el sobreajuste |
| `n` | El número de observaciones de entrenamiento | adimensional | Baja la varianza (como `1/n`) y no toca el sesgo. Con un modelo que no representa la relación, mil filas más no arreglan nada |
| `x₀` | El punto nuevo donde se predice | las de la variable de entrada | El sesgo y la varianza se miden punto a punto: en los extremos del rango la varianza es mayor, porque hay menos datos que sujeten la curva |
| `complejidad` | Cuántos grados de libertad das al modelo | grados del polinomio o parámetros efectivos | Baja el sesgo y sube la varianza. El error total tiene forma de U: el mejor punto está en el medio, y a partir de ahí solo se memoriza ruido |
:::

## Ejemplo

Se ajustan polinomios de varios grados a `f(x) = sen(2πx)` en 30 puntos de `[0, 1]`, con ruido de
desviación 0,3. Se repite el experimento 300 veces con muestras distintas y se mide, en cada punto,
la media y la varianza de las predicciones sobre las 300 réplicas:

```text
grado   sesgo²   varianza   error del estimador
  0      0,4833    0,0029         0,4862
  1      0,2197    0,0061         0,2258
  3      0,0056    0,0120         0,0176
  5      0,0001    0,0178         0,0179
  9      0,0002    0,0296         0,0298
```

- Del grado 0 al 3, el sesgo cae de 0,4833 a 0,0056 y la varianza apenas sube de 0,0029 a 0,0120: el
  error total se desploma de 0,4862 a 0,0176.
- Del grado 5 al 9, el sesgo ya no baja (0,0001 → 0,0002) y la varianza sube un 66 %: el error total
  empeora. Ahí ya no estás aprendiendo la curva, estás memorizando el ruido.
- El mínimo está en los grados 3-5, con 0,0176 y 0,0179. La diferencia entre ambos es ruido; lo que
  importa es que existe un rango razonable y que salirse por arriba se paga.
- Súmale la varianza irreducible: `σ² = 0,09`. El error esperado de predicción en el mejor grado es
  `0,09 + 0,0176 = 0,1076`. Casi todo lo que queda por bajar es ruido, no modelo.

Un único conjunto de datos, 40 puntos repartidos en 32 para entrenar y 8 para validar, muestra lo
mismo de forma más cruda: con grado 5, el error de entrenamiento es 0,222 y el de validación 0,276;
con grado 10, el de entrenamiento baja a 0,198 y el de validación se dispara a 1,040. La brecha entre
las dos columnas es la varianza, y es la señal de alarma que hay que mirar.

## Código

```python verificable
import numpy as np

def f(x):
    return np.sin(2 * np.pi * x)

rng = np.random.default_rng(1)
x = np.linspace(0, 1, 30)
sigma, replicas = 0.3, 300
grados = [0, 1, 2, 3, 4, 5, 6, 7, 9]

# 300 muestras distintas por grado: asi se ve la variabilidad del propio ajuste
pred = {g: np.zeros((replicas, x.size)) for g in grados}
for r in range(replicas):
    y = f(x) + rng.normal(0, sigma, x.size)
    for g in grados:
        pred[g][r] = np.polyval(np.polyfit(x, y, g), x)

print("grado  sesgo^2  varianza  error")
for g in grados:
    media = pred[g].mean(axis=0)
    sesgo2 = np.mean((media - f(x)) ** 2)
    var = np.mean(pred[g].var(axis=0))
    print("%5d  %7.4f  %8.4f  %7.4f" % (g, sesgo2, var, sesgo2 + var))
# ->     3   0.0056    0.0120   0.0176
# ->     9   0.0002    0.0296   0.0298
print("varianza irreducible %.4f" % sigma ** 2)      # -> varianza irreducible 0.0900
```

```python verificable
import numpy as np

# Un solo conjunto: la brecha entre entrenamiento y validacion es la varianza
rng = np.random.default_rng(5)
x = np.linspace(0, 1, 40)
y = np.sin(2 * np.pi * x) + rng.normal(0, 0.3, x.size)

# Validacion entrelazada: uno de cada cinco puntos, repartidos por todo el rango
validacion = np.arange(x.size) % 5 == 4
x_tr, y_tr = x[~validacion], y[~validacion]
x_va, y_va = x[validacion], y[validacion]

print("grado  error train  error validacion")
for g in range(1, 13):
    coef = np.polyfit(x_tr, y_tr, g)
    e_tr = np.sqrt(np.mean((y_tr - np.polyval(coef, x_tr)) ** 2))
    e_va = np.sqrt(np.mean((y_va - np.polyval(coef, x_va)) ** 2))
    print("%5d  %11.3f  %16.3f" % (g, e_tr, e_va))
# ->     5        0.222             0.276
# ->    10        0.198             1.040
# El minimo de validacion esta en los grados 5 y 6; a partir de ahi, la brecha crece
print("desviacion del ruido 0.30")
print("puntos: %d entrenamiento, %d validacion" % (x_tr.size, x_va.size))
# -> puntos: 32 entrenamiento, 8 validacion
```

:::claves
- `np.polyfit(x, y, g)` devuelve los coeficientes de MAYOR a menor grado, y `np.polyval` los espera en ese mismo orden. Si los das la vuelta, la curva sale mal sin dar ningún error.
- `np.polyfit` de grado `g` no valida nada: con 30 puntos admite grado 29 sin rechistar, y el polinomio que devuelve ni siquiera reproduce los 30 puntos, porque el sistema está mal condicionado. Ajustar y saber si el ajuste sirve son dos cosas distintas.
- `pred[g]` es una matriz de 300 filas (réplicas) por 30 columnas (puntos). `pred[g].mean(axis=0)` promedia **sobre las réplicas** y deja un valor por punto: ese es el `f̂` medio del que sale el sesgo. Con `axis=1` promediarías los puntos y el cálculo no significaría nada.
- `pred[g].var(axis=0)` de NumPy divide entre `n` (ddof=0); pandas divide entre `n − 1`. Con 300 réplicas la diferencia es del 0,3 % y no cambia ninguna conclusión, pero conviene saber de dónde sale.
- La varianza irreducible `σ²` **no** es la varianza de `y`: `0,3² = 0,09` es el suelo del error cuadrático medio, y por eso el error del mejor grado (0,0176) se compara con él y no con 1.
- `validacion = np.arange(x.size) % 5 == 4` reparte uno de cada cinco puntos por todo el rango. Cambiar esa línea por `x > 0,8` deja la validación en un extremo y el error de validación se dispara: no es el modelo, es dónde mides.
:::

## Errores típicos

- **Mirar solo el error de entrenamiento.** Es la versión de manual: un modelo más flexible siempre
  lo baja, así que la elección por error de entrenamiento lleva al grado 20 o al árbol sin poda.
  Decide siempre con datos que el modelo no ha visto.
- **Confundir la varianza del modelo con la varianza de los datos.** El ruido irreducible `σ²` no
  baja con más datos ni con otro algoritmo. Si tu error ya está pegado a `σ`, el problema es de
  datos, no de modelo.
- **Creer que más datos reducen el sesgo.** Reducen la varianza. Un modelo lineal ajustado a una
  relación cuadrática seguirá fallando con un millón de filas; lo que hay que cambiar es el modelo o
  las variables.
- **Regularizar sin medir.** La penalización es un intercambio: si subes `λ` y el error de validación
  no mejora, solo has añadido sesgo. Se elige con validación cruzada, no por costumbre
  ([[validacion-cruzada]], [[seleccion-de-hiperparametros]]).
- **Interpretar la curva en U como una ley universal.** En modelos muy sobreparametrizados se observa
  la doble bajada: el error sube, alcanza un pico y vuelve a bajar al aumentar la complejidad. La
  curva clásica describe el régimen en el que el número de parámetros es menor que el de datos.
- **Aplicar la descomposición a métricas que no son el error cuadrático.** Para la exactitud o el AUC
  no hay suma de tres términos. Puedes razonar con sesgo y varianza, pero no citar la igualdad.

:::practica
enunciado: Dos modelos sobre el mismo problema, con ruido de varianza σ² = 0,04. El modelo A tiene sesgo² = 0,0100 y varianza 0,0225; el B, sesgo² = 0,0016 y varianza 0,0400. Calcula el error cuadrático esperado de cada uno, su raíz y el suelo que ninguno puede bajar. ¿Cuál eliges?
pista: El error esperado es la suma de los tres términos: ruido irreducible, sesgo al cuadrado y varianza. El ruido no depende del modelo.
solucion: A: 0,04 + 0,0100 + 0,0225 = 0,0725, con raíz 0,269. B: 0,04 + 0,0016 + 0,0400 = 0,0816, con raíz 0,286. El suelo es 0,04, es decir 0,2 de error, y ninguno lo baja: más de la mitad del error de A es ruido irreducible. Eliges A, con más sesgo y menos varianza; B complica el modelo y paga la varianza con creces.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo con 40 variables y 60 observaciones tiene mucho más error de validación que otro con 5 variables y las mismas 60 observaciones. ¿Qué pieza de la descomposición explica mejor la diferencia?
o: El sesgo, porque el modelo con más variables se equivoca de forma sistemática
o: La varianza, porque con 40 parámetros y 60 datos las predicciones cambian mucho al cambiar la muestra
o: El ruido irreducible, porque 40 variables introducen más ruido en los datos
a: 2
e: Con muchos parámetros para pocas observaciones, la varianza del ajuste crece como σ² · p / n: el modelo se pega a las peculiaridades de esa muestra concreta y cambia al cambiar la muestra. El sesgo suele ser menor cuando hay más variables, y el ruido irreducible depende de los datos, no del número de columnas.
:::

:::quiz
p: Tienes un modelo con error de validación 0,33 y sabes que la desviación típica del ruido de la variable objetivo es 0,30. ¿Qué conclusión es razonable?
o: Que el modelo es malo, porque su error debería ser menor que el ruido
o: Que casi todo el error que queda es ruido irreducible y que mejorar el modelo apenas bajará el error
o: Que el ruido de los datos hay que reducirlo antes de seguir con el modelo
a: 2
e: El error esperado incluye σ² como sumando: con σ = 0,30, el suelo del error cuadrático medio es 0,09 y su raíz, 0,30, así que el modelo está prácticamente ahí. El ruido irreducible no depende del modelo y no se puede reducir salvo midiendo mejor o cambiando de problema.
:::

:::quiz
p: ¿Por qué promediar muchos árboles entrenados con muestras bootstrap (bagging) suele mejorar la predicción?
o: Porque reduce el sesgo de cada árbol por separado
o: Porque reduce la varianza del predictor promediado, sin cambiar mucho su sesgo
o: Porque aumenta el número de parámetros efectivos del modelo
a: 2
e: Promediar predictores poco correlacionados reduce la varianza del resultado: los errores aleatorios de cada árbol se compensan. El sesgo de cada árbol se mantiene (los árboles siguen siendo igual de simples), y el número de parámetros no es lo que se busca.
:::
