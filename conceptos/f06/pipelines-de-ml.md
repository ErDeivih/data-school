---
id: pipelines-de-ml
titulo: Pipelines de machine learning
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [fuga-de-datos, validacion-cruzada, escalado-y-transformacion, train-val-test]
tags: [practica, fuga-de-datos, sklearn, reproducibilidad]
resumen: Encadenar imputación, escalado y modelo en un solo objeto: la forma practica de que ninguna transformación se ajuste con datos de prueba
fuentes: ["Buitinck et al. (2013), 'API design for machine learning software: experiences from the scikit-learn project'"]
---

## En una frase

Un pipeline es una cadena de pasos —imputar, escalar, seleccionar variables, codificar
categóricas— que termina en un modelo, se ajusta y se evalúa como si fuera un solo
estimador, de manera que cada transformación aprende únicamente de los datos de
entrenamiento de su pliegue.

## La idea

Un modelo casi nunca se come los datos en crudo. Antes hay que rellenar nulos, estandarizar,
crear variables, codificar categorías y quedarse con las columnas útiles. Todo eso son
**transformaciones que aprenden algo de los datos**: la mediana con la que imputas, la media y
la desviación con las que estandarizas, las categorías que has visto, las variables que has
seleccionado.

Y ahí está el problema. Si calculas esas cosas una vez sobre el conjunto completo y luego
haces validación cruzada, cada pliegue de entrenamiento ya sabe algo del pliegue de prueba:
la media, la mediana o la selección de variables se han calculado mirando también las filas
que se supone que no has visto. Eso es [[fuga-de-datos|fuga de datos]], y su síntoma típico
es una puntuación de validación estupenda que no se repite en producción.

Un pipeline resuelve esto por construcción. Cuando llamas a `fit` sobre un pipeline con
validación cruzada, el estimador se replica en cada pliegue y **cada paso se ajusta solo con
las filas de entrenamiento de ese pliegue**. Al predecir, las transformaciones ya ajustadas
se aplican al conjunto de prueba. No tienes que acordarte de nada: la estructura te obliga.

Tiene tres ventajas más, y las tres se notan en el día a día. La primera es que el
preprocesamiento viaja con el modelo: si guardas el pipeline, guardas la media, la
desviación, la lista de columnas y el orden exacto de las operaciones, así que servir una
predicción nueva es una línea. La segunda es que elimina el error de aplicar el mismo
tratamiento dos veces con criterios distintos en entrenamiento y en producción. La tercera es
la búsqueda de hiperparámetros: puedes buscar a la vez el número de componentes de un PCA y
la profundidad de un árbol con la misma rejilla, porque los nombres de los pasos se pueden
usar como prefijo (`reducir__n_components`).

## Definición formal

Un pipeline es una tupla ordenada de `k` pasos:

:::formula
P = (T₁, T₂, …, T_{k−1}, M)     ŷ = M(T_{k−1}(… T₂(T₁(X))))
:::

- `Tᵢ` — transformadores; cada uno implementa `fit(X, y)` y `transform(X)`. Ejemplos:
  `SimpleImputer`, `StandardScaler`, `OneHotEncoder`, `PCA`, `SelectKBest`.
- `M` — el estimador final; implementa `fit` y `predict` (o `predict_proba`).
- `X` — la matriz de variables de entrada, con `n` filas y `p` columnas.
- `ŷ` — la predicción; para predecir, las transformaciones **no se vuelven a ajustar**, solo
  se aplican.
- `X_fit` — en `P.fit(X_fit, y_fit)`, todos los `Tᵢ` aprenden solo de `X_fit`.

Regla que resume todo lo anterior: **cualquier cosa que mire `y` o que resuma `X` es un paso
del pipeline, nunca una operación previa sobre el conjunto completo**. Si una transformación
se ajusta fuera del pipeline y dentro de la validación cruzada, hay fuga.

Dos precisiones que separan a quien lo entiende de quien solo lo copia:

1. **Transformaciones sin estado** (aplicar un logaritmo, restar una constante conocida) son
   seguras fuera del pipeline porque no aprenden nada de los datos. El peligro empieza cuando
   aparece un `fit`.
2. **Dentro de un pliegue, el pipeline se ajusta solo con el entrenamiento de ese pliegue**;
   el conjunto de prueba del pliegue se transforma con lo aprendido. Por eso el mismo
   pipeline da resultados distintos si lo metes en `cross_val_score` que si lo ajustas una vez
   sobre todo el conjunto.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Tᵢ` | Un transformador del pipeline: imputar, escalar, codificar, reducir o seleccionar | lo que devuelva ese paso | Cada paso que añades se reajusta en cada pliegue; más pasos, más sitios donde puede colarse una fuga si alguno se queda fuera |
| `M` | El estimador final, el único que predice | las unidades de `y` | Es lo único que cambia si cambias de modelo; la cadena de transformaciones de delante sigue igual |
| `k` | Número de pasos del pipeline: los `k − 1` transformadores más el modelo | pasos | Más pasos no es mejor: cada uno puede fallar y el orden importa, porque `PCA` antes de escalar no es lo mismo que después |
| `X` | La matriz de variables de entrada, con `n` filas y `p` columnas | las de cada variable | Con columnas en escalas muy distintas (edad en años, ingresos en euros) el modelo lo nota: sin escalar, la columna grande manda |
| `ŷ` | La predicción del pipeline ya ajustado | las unidades de `y` | Para predecir, las transformaciones NO se vuelven a ajustar: solo se aplican, y ese es el motivo de que dos predicciones iguales den el mismo resultado |
| `X_fit` | Las filas con las que se ajusta el pipeline | filas | Cuanto más pequeño sea `X_fit` (el trozo de un pliegue), más se separa la media de ese trozo de la media global y más se nota la diferencia entre ajustar dentro y fuera |
:::

## Ejemplo

120 clientes con edad (años, media 40, desviación 10) e ingresos (euros, media
30.000, desviación 8.000). Comparación de dos formas de hacer lo mismo:

```
sin pipeline: escalar con la media y la desviacion de TODO el conjunto -> 0,967
con pipeline: el escalador se ajusta dentro de cada pliegue           -> 0,975
```

La diferencia aquí es pequeña porque los datos son homogéneos: la media de todo el conjunto y
la de cada pliegue de entrenamiento se parecen mucho. Pero el mecanismo de la fuga ya está
ahí, y con datos donde el reparto no es aleatorio (por fecha, por cliente, por tramo de
ingresos) la brecha se abre de golpe. El caso extremo es una transformación supervisada:

```
60 filas, 500 columnas casi todas ruido, 20 variables elegidas con SelectKBest
seleccion hecha con todas las filas antes de validar -> 0,867 de exactitud
misma seleccion dentro del pipeline                  -> 0,417
```

0,867 contra 0,417 sobre el mismo modelo y los mismos datos. La diferencia no es el modelo:
es que la primera versión eligió las variables mirando el conjunto de prueba.

:::figura
fichero: pipelines-de-ml-fuga-segun-transformacion
pie: A la izquierda, los dos pares del ejemplo. Con el escalado la brecha es de ocho milésimas (0,967 contra 0,975): la fuga existe, pero la media de cada pliegue se parece tanto a la media global que no se nota. Con una selección supervisada la brecha es de cuatro décimas y media (0,867 contra 0,417), y ahí no hay nada sutil: el selector usa la etiqueta, así que al mirar todas las filas elige columnas que separan también el conjunto de prueba. Moraleja: la fuga no es un matiz de estilo, y su tamaño depende de si la transformación mira la etiqueta. La curva de la derecha lleva el mismo experimento a varios tamaños de selección, promediando cinco conjuntos: cuanto más grande es `k`, más alto parece el resultado falso, mientras la versión honesta se queda plana. Si tu validación mejora al ampliar la selección, sospecha antes de celebrar.
fuente: figuras/pipelines-de-ml-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

# 120 filas con dos columnas en escalas muy distintas: anos e ingresos en euros
rng = np.random.default_rng(0)
X = np.column_stack([rng.normal(40, 10, 120), rng.normal(30000, 8000, 120)])
# La comparacion contra 0 da un booleano; .astype(int) lo convierte en las clases 0 y 1
y = (X[:, 0] - 40 + (X[:, 1] - 30000) / 8000 + rng.normal(0, 1, 120) > 0).astype(int)

# MAL: escalar con la media y la desviacion de todo el conjunto, prueba incluida
print("sin pipeline:", round(cross_val_score(LogisticRegression(),
      StandardScaler().fit_transform(X), y, cv=5).mean(), 3))               # -> 0.967

# BIEN: el escalador se ajusta dentro de cada pliegue, con sus 96 filas
print("con pipeline:", round(cross_val_score(make_pipeline(StandardScaler(),
      LogisticRegression()), X, y, cv=5).mean(), 3))                        # -> 0.975

# Un pipeline con nombre en cada paso se lee y se depura mucho mejor
modelo = Pipeline([
    ("imputar", SimpleImputer(strategy="median")),   # primero los nulos
    ("escalar", StandardScaler()),                   # luego la escala
    ("reducir", PCA(n_components=2)),                # luego la dimension
    ("modelo", RandomForestClassifier(n_estimators=50, random_state=0)),
]).fit(X, y)
# steps es una lista de tuplas (nombre, objeto): se recorre con dos variables, no con una
print("pasos:", [nombre for nombre, _ in modelo.steps])   # -> ['imputar', 'escalar', 'reducir', 'modelo']
print("accuracy en entrenamiento:", round(modelo.score(X, y), 3))   # -> 1.0
```

:::claves
- `StandardScaler().fit_transform(X)` devuelve un array nuevo y tira el escalador: con él se pierden la media y la desviación que se usaron. Ese es el problema de fondo, no solo la fuga: en producción no tienes con qué reproducir la escala. Un pipeline guarda el escalador dentro del objeto y basta con guardar el objeto entero.
- `cross_val_score` recibe el pipeline **sin ajustar** y lo clona en cada pliegue. Si le pasaras uno ya ajustado, sklearn lo volvería a ajustar igualmente, así que no hay riesgo de reutilizar un ajuste viejo; simplemente no sirve de nada ajustarlo antes.
- `make_pipeline` nombra los pasos solo, en minúsculas y a partir de la clase (`standardscaler`, `logisticregression`). `Pipeline` con nombres explícitos es lo que permite pedir `reducir__n_components` en una rejilla de hiperparámetros: el prefijo del paso va seguido de **doble** guion bajo, y con uno solo sklearn no encuentra el parámetro.
- `Pipeline([...])` recibe una lista de tuplas `(nombre, objeto)` y los nombres no pueden repetirse ni contener doble guion bajo, porque esa sintaxis está reservada para direccionar parámetros dentro de los pasos.
- `modelo.score(X, y)` mide sobre los MISMOS datos del ajuste y devuelve exactitud, no error. Ese 1,0 es memorización, no calidad: con el bosque y el PCA dentro del pipeline no dice nada de lo que pasará con filas nuevas.
- `rng.normal(30000, 8000, 120)` genera los ingresos en euros mientras la edad va en años. Sin un paso de escalado, la penalización L2 de la regresión logística se aplica sobre coeficientes que se miden en unidades distintas, así que el resultado depende de las unidades que elijas. Cambia `SimpleImputer(strategy="median")` por `strategy="mean"` en el pipeline con el bosque y el resultado no se mueve: sin nulos, el imputador no tiene nada que hacer y su estrategia es indiferente.
:::

```python verificable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

# 500 columnas y solo 3 con senal: el escenario donde la fuga se ve a simple vista
# flip_y=0.15 mete ruido en la etiqueta, asi que ni el modelo perfecto pasa de ~0.85
X, y = make_classification(n_samples=60, n_features=500, n_informative=3,
                           n_redundant=0, flip_y=0.15, random_state=0)

# MAL: elegir las 20 variables "buenas" mirando TODAS las filas y luego validar
# get_support() devuelve una mascara booleana de 500 posiciones; con ella se indexan columnas
buenas = SelectKBest(f_classif, k=20).fit(X, y).get_support()
# max_iter alto por si acaso: el ajuste real es sobre las 20 columnas elegidas, no sobre las 500
print("antes de validar:", round(cross_val_score(LogisticRegression(max_iter=1000),
      X[:, buenas], y, cv=5).mean(), 3))                                   # -> 0.867

# BIEN: la seleccion vive dentro del pipeline y se reajusta en cada pliegue
limpio = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))
print("dentro del pipe :", round(cross_val_score(limpio, X, y,
      cv=StratifiedKFold(5, shuffle=True, random_state=0)).mean(), 3))      # -> 0.417
```

```python ilustrativo
# Los nombres de los pasos permiten buscar hiperparametros de toda la cadena a la vez
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

modelo = Pipeline([("escalar", StandardScaler()), ("reducir", PCA()), ("modelo", SVC())])
# El doble guion bajo separa el nombre del paso del nombre de su parametro interno
rejilla = {"reducir__n_components": [2, 5, 10], "modelo__C": [0.1, 1, 10]}
busqueda = GridSearchCV(modelo, rejilla, cv=5).fit(X_entrenamiento, y_entrenamiento)
print(busqueda.best_params_)
```

## Errores típicos

- **Ajustar el escalador (o el imputador, o el PCA) antes de partir los datos.** Es la fuga
  más frecuente porque parece inofensiva: `scaler.fit_transform(X)` y después
  `train_test_split`. A partir de ahí, cada métrica está contaminada. Mete la transformación
  en el pipeline y no la toques fuera.
- **Olvidar que la selección de variables es supervisada.** `SelectKBest`, `RFE` y el
  *target encoding* usan `y`, así que también fugan. Este es el caso que más infla el
  resultado, porque el selector puede encontrar por azar las columnas que casualmente separan
  el conjunto de prueba.
- **Hacer el `fit_transform` de las variables categóricas una sola vez.** Si codificas
  categorías con las que aparecen en todo el conjunto, el modelo conoce categorías que en su
  pliegue de entrenamiento no existían. Con categorías raras el efecto es pequeño; con
  variables de alta cardinalidad, enorme.
- **Dejar huecos en el pipeline.** Un `StandardScaler` en el pipeline y una media móvil
  calculada antes, con `rolling` sobre toda la serie, siguen fugando: el pipeline solo
  protege lo que metes dentro. Lo que se calcula fuera, se calcula mal.
- **Guardar solo el modelo y no el pipeline.** Si en producción aplicas un escalado distinto
  del que usaste al entrenar, el modelo recibe datos con otra escala y predice mal sin dar
  ningún error. Guarda el objeto completo, con sus pasos y sus nombres de columna.
- **Reajustar el pipeline entero con cada predicción nueva.** Un pipeline ajustado no se
  vuelve a ajustar para predecir: se aplica. Reajustarlo con cada fila que llega hace que el
  modelo cambie solo con el tiempo y que dos predicciones idénticas den resultados distintos.

:::practica
enunciado: 100 clientes, edad media 40 y desviación 10. Un cliente de prueba tiene 65 años, así que el z-score correcto es (65 − 40)/10 = 2,5. Si escalas con la media y la desviación de todo el conjunto más 20 filas de prueba cuya media de edad es 45, ¿cuánto vale el z-score de ese mismo cliente y qué mide esa diferencia?
pista: Calcula la media conjunta con los dos tamaños y comprueba después cuánto cambia la desviación al añadir 20 filas tan parecidas.
solucion: Media conjunta = (100 · 40 + 20 · 45) / 120 = 4.900/120 = 40,83. La desviación típica conjunta sube de 10 a unos 10,17, así que el z-score pasa a (65 − 40,83)/10,17 = 2,38. El dato en sí no ha cambiado: lo que cambió es la escala, calculada con 20 filas que el modelo no debería haber visto. Por eso el escalador va dentro del pipeline y se ajusta solo con las 100 filas de entrenamiento de cada pliegue.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué gana un pipeline frente a hacer el preprocesamiento a mano antes de la validación cruzada?
o: Que entrena más rápido, porque reutiliza los cálculos entre pliegues
o: Que cada transformación se ajusta solo con el entrenamiento de su pliegue, y no hay fuga
o: Que no hace falta separar un conjunto de prueba
a: 2
e: El pipeline reajusta las transformaciones dentro de cada pliegue: eso es exactamente lo que evita la fuga. No es más rápido (reajusta más veces) y no elimina la necesidad de un conjunto de prueba o de validación bien hecha.
:::

:::quiz
p: Tienes 500 variables, seleccionas las 20 mejores con SelectKBest y validas el modelo con esas 20 columnas. ¿Por qué el resultado sale demasiado bueno?
o: Porque SelectKBest usa la etiqueta y, al haber mirado todas las filas, elige columnas que separan también el conjunto de prueba
o: Porque SelectKBest siempre sobreajusta y hay que evitarlo
o: Porque 20 variables son demasiadas para ese modelo
a: 1
e: La selección es supervisada: usa la etiqueta y, si se calcula antes de partir, aprovecha información del conjunto de prueba. Dentro de un pipeline se recalcula en cada pliegue y el resultado baja a lo que realmente vale el modelo.
:::

:::trampa
Ordenar el preprocesamiento con `fit_transform` sobre todo el conjunto y después hacer
`cross_val_score` es el error más común de un primer proyecto de machine learning, y no
produce ningún aviso: solo un número de validación que no se repite cuando el modelo llega a
producción. La regla es mecánica: si el objeto tiene `fit`, va dentro del pipeline.
:::
