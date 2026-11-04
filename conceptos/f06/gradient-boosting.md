---
id: gradient-boosting
titulo: Gradient boosting
fase: 6
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [arboles-de-decision, sesgo-varianza, derivadas-parciales-y-gradiente]
tags: [boosting, ensembles, optimizacion, tabular]
resumen: Sumar árboles pequeños que corrigen el error del anterior: la receta que domina los datos tabulares y en la que cada pieza cuenta.
fuentes: ["Friedman (2001), 'Greedy Function Approximation: A Gradient Boosting Machine'", "Chen y Guestrin (2016), 'XGBoost: A Scalable Tree Boosting System'"]
---

## En una frase

Gradient boosting construye el modelo poco a poco: empieza con una predicción constante y en
cada paso entrena un árbol pequeño para corregir lo que el modelo actual se equivoca, sumándolo
con un peso pequeño para no pasarse.

## La idea

Un árbol profundo entrenado de una vez falla por varianza: memoriza. Un bosque promedia muchos
árboles independientes para bajar esa varianza. Gradient boosting ataca el problema desde el
otro lado: en lugar de promediar modelos completos, construye **un solo modelo** con muchos
trozos pequeños, cada uno entrenado para arreglar el error que queda.

Piensa en alguien que aprende a lanzar dardos. La primera tirada cae lejos. El entrenador no le
dice «tira otra vez», le dice «estás 20 centímetros a la izquierda»: el segundo lanzamiento
corrige ese error, no empieza de cero. Después corrige el error que queda, y así. El modelo
final es la suma de todos los lanzamientos, no el último.

Ese «error que queda» se llama **residuo**, y con la pérdida cuadrática es literalmente
`y − ŷ`. Con otras pérdidas (logística, Poisson, ranking) ya no es el residuo, sino el
**gradiente negativo** de la pérdida respecto a la predicción actual: la dirección en la que hay
que mover la predicción para reducir el error. De ahí el nombre: boosting por gradiente. En
lugar de calcular el gradiente analíticamente y dar un paso, se entrena un árbol para predecir
ese gradiente y se suma. El árbol es el que aprende la forma del paso.

Dos detalles cambian todo el comportamiento:

- **La tasa de aprendizaje** `ν` (nu o *learning rate*) encoge cada árbol antes de sumarlo. Con
  `ν = 0,1` cada árbol aporta el 10 % de lo que predijo. Cuanto menor es, más árboles hacen
  falta y mejor suele ser el resultado: es un intercambio entre tiempo de cómputo y calidad.
- **La profundidad** se mantiene pequeña (entre 2 y 8 niveles, a menudo 3). El boosting no
  necesita árboles listos; necesita árboles que corrijan un poquito. Un árbol profundo se come
  los datos y provoca el sobreajuste que el método intenta evitar.

## Definición formal

El modelo es una suma de funciones, construida de forma aditiva y por etapas:

:::formula
F_m(x) = F_(m−1)(x) + ν · h_m(x)
:::

- `F_m` — modelo después de añadir el árbol `m`.
- `h_m` — árbol pequeño entrenado en la etapa `m`.
- `ν` — tasa de aprendizaje, entre 0 y 1; encoge la aportación de cada árbol.
- `F_0` — predicción inicial constante: la media de `y` con pérdida cuadrática, o el log-odds
  base con pérdida logística.

En cada etapa, el árbol `h_m` se entrena sobre los **pseudo-residuos**, que son el gradiente
negativo de la pérdida `L` respecto a la predicción actual:

:::formula
r_i = − ∂L(y_i, F(x_i)) / ∂F(x_i)      evaluado en F = F_(m−1)
:::

- `L(y, F)` — función de pérdida; con la cuadrática, `L = ½(y − F)²` y `r_i = y_i − F(x_i)`.
- `∂` — derivada parcial.
- `r_i` — valor objetivo que el árbol `h_m` intenta predecir para la fila `i`.

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa con el error de prueba si sube |
| --- | --- | --- | --- |
| `ν` | Tasa de aprendizaje: cuánto aporta cada árbol | entre 0 y 1 | Hace falta menos árboles para ajustar, pero el modelo llega antes al ruido: el error de prueba baja y luego sube, y el mínimo se adelanta |
| `M` | Número de árboles que se suman | etapas | El error de entrenamiento baja siempre; el de prueba baja hasta un punto y después empeora. Ese punto es la parada temprana |
| `max_depth` | Profundidad de cada árbol | niveles | Cada árbol capta interacciones más complejas y el conjunto sobreajusta antes; con 2 o 3 suele bastar |
| `F_0` | Predicción inicial constante | las de `y` | Marca de dónde se parte (la media con pérdida cuadrática); no cambia el techo, solo los primeros pasos |
| `γ` | Coste fijo por crear una hoja | las de la pérdida | Con valores altos no se aceptan divisiones y el árbol se queda en una hoja: poda previa, menos capacidad |
| `λ` | Penalización L2 sobre el valor de las hojas | adimensional | Encoge las ganancias y los pesos de las hojas: menos sobreajuste y más sesgo |
| `T` | Número de hojas del árbol | hojas | Sube la capacidad del modelo y el coste `γ·T` que paga por ella |
| `w_j` | Valor que el árbol asigna a la hoja `j` | las de `y` | Es la corrección que se suma; en la versión regularizada vale `−Σg_i / (Σh_i + λ)` |
:::

La versión que usan XGBoost y compañía añade dos regularizaciones y usa la expansión de Taylor
de segundo orden de la pérdida. Con `g_i` la primera derivada y `h_i` la segunda,
`g_i = ∂L/∂F` y `h_i = ∂²L/∂F²`, la función objetivo de cada árbol es:

:::formula
Obj = Σ_i [ g_i · f(x_i) + ½ · h_i · f(x_i)² ] + γ · T + ½ · λ · Σ_j w_j²
:::

- `f(x_i)` — predicción que el árbol asigna a la fila `i`, que es el valor `w_j` de la hoja
  donde cae.
- `g_i` — primera derivada de la pérdida respecto a la predicción actual, para la fila `i`.
- `h_i` — segunda derivada de esa misma pérdida.
- `T` — número de hojas del árbol; `w_j` — valor asignado a la hoja `j`.
- `γ` (gamma) — coste fijo por crear una hoja nueva: subirlo poda el árbol.
- `λ` (lambda) — penalización L2 sobre los valores de las hojas.
- El peso óptimo de una hoja es `w_j = − Σ_{i∈I_j} g_i / (Σ_{i∈I_j} h_i + λ)`, donde `I_j` es el
  conjunto de filas que caen en la hoja `j`. La ganancia de una división se calcula con esos
  pesos: si no supera `γ`, no se hace.

Cuatro implementaciones y sus rasgos distintivos: **scikit-learn** es la más simple y lenta;
**XGBoost** crece nivel a nivel con el objetivo regularizado anterior; **LightGBM** crece hoja a
hoja (elige la hoja que más reduce la pérdida) y agrupa los valores continuos en histogramas,
lo que lo hace muy rápido en datasets grandes; **CatBoost** trata las variables categóricas con
estadísticas ordenadas que evitan el sesgo del *target encoding* clásico.

## Ejemplo

Cuatro observaciones con `y = [10, 12, 14, 16]`, árboles de un solo corte y `ν = 0,1`.

- `F_0 = 13` (la media). Residuos: `[−3, −1, +1, +3]`.
- Primer corte: el árbol separa las dos primeras filas (residuo medio `−2`) de las dos últimas
  (`+2`). Predicción del árbol: `[−2, −2, +2, +2]`.
- `F_1 = 13 + 0,1 · [−2, −2, +2, +2] = [12,8, 12,8, 13,2, 13,2]`. Nuevos residuos:
  `[−2,8, −0,8, +0,8, +2,8]`.
- Segundo corte: medias `−1,8` y `+1,8`.
  `F_2 = [12,8 − 0,18, 12,8 − 0,18, 13,2 + 0,18, 13,2 + 0,18] = [12,62, 12,62, 13,38, 13,38]`.

Los residuos bajan en valor absoluto en cada paso (`3,0 → 2,8 → 2,62`) pero muy despacio,
porque `ν = 0,1` recorta cada corrección a la décima parte. Ese es el precio de la tasa pequeña:
convergencia lenta a cambio de estabilidad. Con `ν = 1` el primer paso ya pondría
`F_1 = [11, 11, 15, 15]`, más cerca de los datos de entrenamiento y más expuesto al ruido.

Con datos reales, un boosting implementado a mano con 50 tocones y `ν = 0,1` sobre
`y = sen(x) + ruido` deja el RMSE en 0,262, frente a 0,723 de predecir siempre la media. Y el
efecto de la tasa, con 60 árboles de profundidad 2 sobre una muestra con ruido:

```
lr=0.05 train 0.286  test 0.327
lr=0.3  train 0.109  test 0.245
lr=1.0  train 0.038  test 0.458
```

Con `lr = 0,05` el modelo aún no ha aprovechado los 60 árboles (error alto en las dos partes).
Con `lr = 0,3` está en su punto: mucho mejor en entrenamiento (0,109) y mejor en prueba (0,245).
Con `lr = 1,0` el entrenamiento es casi perfecto (0,038) y la prueba empeora claramente (0,458):
sobreajuste. La conclusión práctica es que `ν` y el número de árboles no se eligen por separado;
se eligen juntos, mirando una curva de validación.

:::figura
fichero: boosting-tasa-de-aprendizaje-y-parada
pie: El panel izquierdo es la curva que hay que mirar siempre en boosting: el error en datos no vistos según se suman árboles. Con ν = 0,6 el mínimo llega a los 4 árboles y a partir de ahí solo empeora, porque cada corrección es tan grande que el modelo se ajusta al ruido; con ν = 0,05 sigue bajando mucho después, hasta pasar el árbol 70. La tasa no cambia el destino, cambia cuándo llegas: con tasas altas necesitas parada temprana. El panel derecho explica por qué el error de entrenamiento no sirve como criterio: baja siempre, hasta casi cero, aunque el modelo esté empeorando fuera de muestra. La referencia es la línea de puntos, el error de predecir siempre la media (0,791).
fuente: figuras/gradient-boosting-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(0)
X = rng.uniform(-3, 3, size=(200, 1))
y = np.sin(X[:, 0]) + rng.normal(scale=0.2, size=200)

F = np.full(y.shape, y.mean())      # arranque: la constante que minimiza el error cuadratico
for _ in range(50):
    residuo = y - F                 # con perdida cuadratica el gradiente negativo es el residuo
    h = DecisionTreeRegressor(max_depth=1, random_state=0).fit(X, residuo)
    F = F + 0.1 * h.predict(X)      # 0,1 es la tasa de aprendizaje

print(f"RMSE final        {np.sqrt(((y - F) ** 2).mean()):.3f}")
print(f"RMSE de la media  {np.sqrt(((y - y.mean()) ** 2).mean()):.3f}")
# -> RMSE final        0.262
# -> RMSE de la media  0.723
```

:::claves
- `np.full(y.shape, y.mean())` crea un array **nuevo** con la forma de `y` y ese valor repetido: es
  la predicción constante de arranque. `F = y.mean()` sería un número suelto: NumPy difunde el
  escalar contra el array de predicciones y el bucle funcionaría igual, pero así queda claro que `F`
  es la predicción de cada fila.
- `DecisionTreeRegressor(max_depth=1)` es un **tocón**: una sola pregunta, dos hojas. El boosting no
  quiere un árbol listo, quiere uno que corrija un poquito; con `max_depth=None` cada árbol se
  memoriza los residuos que le tocan y el conjunto deja de corregir para pasar a copiar.
- `h.predict(X)` devuelve las predicciones del árbol **sobre las mismas filas** con las que se
  acaba de entrenar. Aquí es lo correcto, porque lo que se suma es la corrección que el árbol
  aprendió para esas filas; en un modelo de producción no lo sería.
- `F = F + 0.1 * h.predict(X)` **crea un array nuevo** cada vuelta: no modifica `F` en el sitio.
  Con `F += ...` el resultado es idéntico, pero deja de quedar claro que se está sumando una etapa.
- La línea `F = F + 0.1 * h.predict(X)` es la única que lleva la tasa de aprendizaje. Cámbiala por
  `F = F + h.predict(X)` (tasa 1) y el RMSE de entrenamiento baja de 0,262 a 0,18: con 50 tocones de
  una sola pregunta el modelo todavía no tiene capacidad para sobreajustar. Ese sobreajuste, el del
  ejemplo con `lr = 1,0`, necesita árboles de profundidad 2.
- El bucle no guarda ninguna historia: al terminar solo tienes el `F` final y no puedes dibujar la
  curva de validación. Para eso está `staged_predict()`, que devuelve la predicción tras cada árbol
  (es lo que usa la figura de esta página).
:::

```python verificable
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
X = rng.uniform(-3, 3, size=(240, 2))
y = np.sin(X[:, 0]) + 0.5 * X[:, 1] + rng.normal(scale=0.2, size=240)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

for lr in (0.05, 0.3, 1.0):
    m = GradientBoostingRegressor(n_estimators=60, learning_rate=lr,
                                  max_depth=2, random_state=0).fit(X_tr, y_tr)
    rmse_tr = np.sqrt(((y_tr - m.predict(X_tr)) ** 2).mean())
    rmse_te = np.sqrt(((y_te - m.predict(X_te)) ** 2).mean())
    print(f"lr={lr:<4} train {rmse_tr:.3f}  test {rmse_te:.3f}")
# -> lr=0.05 train 0.286  test 0.327
# -> lr=0.3  train 0.109  test 0.245
# -> lr=1.0  train 0.038  test 0.458
```

## Errores típicos

- **Subir `n_estimators` sin bajar `learning_rate`.** Los dos parámetros van juntos: `ν = 1` con
  500 árboles es una receta de sobreajuste, y `ν = 0,01` con 50 árboles es un modelo a medio
  entrenar. Ajusta primero `ν` (0,05-0,1 es un punto de partida razonable) y luego el número de
  árboles con parada temprana.
- **Usar árboles profundos.** El boosting aprende de correcciones pequeñas. Con `max_depth` de
  10 o más, cada árbol se ajusta al ruido y el conjunto sobreajusta enseguida. Empieza con
  profundidad 3 y sube solo si el problema lo pide.
- **Vigilar el error de entrenamiento.** Como el modelo se construye para reducir el error de
  entrenamiento paso a paso, ese número baja siempre y no informa de nada. La referencia es un
  conjunto de validación, con parada temprana (`early_stopping`) cuando deja de mejorar.
- **Esperar extrapolación en regresión.** Igual que un bosque, un boosting de árboles devuelve
  combinaciones de valores de hojas vistas: fuera del rango de los datos de entrenamiento la
  predicción se queda plana. Si la tendencia importa, un modelo lineal o una serie temporal
  harán mejor ese trabajo.
- **Confiar en la importancia por impureza para seleccionar variables.** Boosting y bosques
  comparten el sesgo hacia variables con muchos valores distintos. Para decidir qué variables
  entran, usa importancia por permutación con datos no vistos o selección hacia atrás con
  validación.
- **Validar sin respetar la estructura de los datos.** Con datos agrupados o series temporales,
  un `train_test_split` aleatorio filtra información del futuro. Ahí toca
  [[validacion-temporal|validación temporal]] o [[purged-kfold|purga y embargo]], sobre todo
  porque el boosting aprovecha cualquier fuga que le dejes.

:::practica
enunciado: Cuatro filas con y = [2, 4, 6, 8]. Arrancas con F₀ = 5 (la media) y un árbol de un solo corte que separa las dos primeras filas de las dos últimas, con ν = 0,5. Calcula la predicción del árbol, F₁ y el residuo máximo que queda.
pista: Cada hoja predice la media de los residuos que caen en ella, y la tasa de aprendizaje encoge esa aportación antes de sumarla.
solucion: Residuos iniciales: [−3, −1, +1, +3]. Medias por hoja: −2 y +2, así que el árbol predice [−2, −2, +2, +2]. F₁ = 5 + 0,5 · [−2, −2, +2, +2] = [4, 4, 6, 6]. Los residuos quedan en [−2, 0, 0, +2]: el máximo baja de 3 a 2. Con ν = 1 el mismo árbol dejaría F₁ = [3, 3, 7, 7] y el residuo máximo sería 1.
:::

## Comprueba que lo sabes

:::quiz
p: En gradient boosting con pérdida cuadrática, ¿qué aprende exactamente cada árbol nuevo?
o: Los residuos del modelo actual, que son el gradiente negativo de la pérdida
o: La variable respuesta original, con más profundidad que el árbol anterior
o: Una muestra aleatoria de los datos, como en bagging
a: 1
e: Con pérdida cuadrática ½(y-F)^2, el gradiente negativo respecto a F es exactamente y-F, el residuo. Con otras pérdidas se usa el gradiente negativo genérico, que es la dirección en la que hay que mover la predicción. La respuesta original se usa solo en el primer paso, para calcular la media inicial.
:::

:::quiz
p: Con 60 árboles, lr = 1,0 da error de prueba 0,458 y lr = 0,3 da 0,245. ¿Qué explica mejor la diferencia?
o: Que lr = 1,0 hace que cada árbol aporte su predicción completa y el conjunto se ajuste al ruido del entrenamiento
o: Que lr = 1,0 es demasiado lento y el modelo se queda sin entrenar
o: Que lr = 1,0 cambia la función de pérdida
a: 1
e: La tasa de aprendizaje encoge la aportación de cada árbol. Con lr = 1,0 el modelo llega antes al mínimo del entrenamiento (0,038) y con ello memoriza el ruido, como muestra el empeoramiento en prueba. No es un problema de lentitud ni cambia la pérdida.
:::

:::quiz
p: ¿Para qué sirven gamma y lambda en el objetivo regularizado de XGBoost?
o: Para acelerar el entrenamiento usando histogramas
o: Para penalizar, respectivamente, crear cada hoja nueva y el tamaño de los valores de las hojas
o: Para fijar la tasa de aprendizaje y el número de árboles
a: 2
e: Gamma es un coste fijo por hoja: si la ganancia de una división no lo supera, la división no se hace. Lambda es una penalización L2 sobre los pesos de las hojas, que los encoge. Son mecanismos de regularización estructural, no de velocidad ni de tasa de aprendizaje.
:::

:::trampa
El boosting reduce el error de entrenamiento en cada iteración por construcción: si dibujas esa
curva, siempre baja. Un informe que solo muestre «el error bajó de 0,50 a 0,02» no dice nada
sobre la calidad del modelo. Lo único que informa es la curva de un conjunto de validación que
el modelo no haya visto, con el punto donde empieza a subir.
:::
