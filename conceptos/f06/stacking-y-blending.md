---
id: stacking-y-blending
titulo: Stacking y blending
fase: 6
nivel: experto
rutas: [ds, quant]
prerequisitos: [validacion-cruzada, bagging-y-random-forest, gradient-boosting, metricas-de-clasificacion]
tags: [ensembles, metamodelo, overfitting, competiciones]
resumen: Combinar varios modelos con un metamodelo entrenado sobre predicciones fuera de muestra; la diferencia entre ganar y sobreajustar está en cómo se generan esas predicciones.
fuentes: ["Wolpert (1992), 'Stacked Generalization'", "Breiman (1996), 'Stacked Regressions'", "Van der Laan, Polley y Hubbard (2007), 'Super Learner'"]
---

## En una frase

El *stacking* entrena un modelo encima de las predicciones de varios modelos base, y solo
funciona si esas predicciones se generan **fuera de muestra**: si el metamodelo aprende sobre
predicciones hechas con los mismos datos con los que se entrenó cada base, aprende a confiar
en el modelo que más ha memorizado, no en el que mejor generaliza.

## La idea

Tienes tres modelos y quieres aprovechar lo mejor de cada uno. El promedio simple es la
primera idea: `(p₁ + p₂ + p₃)/3`. Funciona sorprendentemente bien y es difícil de batir. El
problema es que promedia a ciegas: si uno de los tres es malo o está sesgado, arrastra el
resultado, y si uno es excelente, su opinión vale lo mismo que la del mediocre.

El stacking sustituye el promedio por un **metamodelo**: un modelo pequeño que recibe las
predicciones de los base como variables de entrada y aprende a ponderarlas. Si un base es
mejor en una zona del espacio, el metamodelo puede darle más peso ahí. Es el mismo truco que
un comité de expertos con un coordinador que sabe a quién creer.

Y aquí está toda la dificultad. Para que el metamodelo aprenda **a quién creer de verdad**,
las predicciones que ve tienen que ser del mismo tipo que las que verá en producción: hechas
sobre datos que el base no ha visto. Si entrenas un Random Forest con todo el conjunto y le
pasas al metamodelo sus predicciones sobre esas mismas filas, el Random Forest dirá
«exactitud 99 %» porque ha memorizado, un KNN dirá «85 %», y el metamodelo aprenderá a
confiar casi en exclusiva en el Random Forest. En producción, donde el Random Forest ya no
memoriza, ese peso es una ruina. A esto se le llama a veces **fuga por predicciones
en muestra**, y es la razón por la que el stacking se hace con
[[validacion-cruzada|predicciones fuera de muestra]].

La variante pobre del stacking es el **blending**: en vez de K pliegues, se reserva un único
conjunto de validación (por ejemplo el 20 % de los datos), se entrenan los base con el 80 %
restante y el metamodelo aprende con las predicciones sobre ese 20 %. Es más simple y más
difícil de equivocar, pero desperdicia datos y da un metamodelo entrenado con menos filas.

## Definición formal

Sean `M` modelos base, un conjunto de entrenamiento `D` de `n` observaciones, y `K` pliegues.

1. **Predicciones fuera de muestra.** Para cada modelo `m` y cada pliegue `k`, se entrena
   `m` con `D \ D_k` y se predicen las filas de `D_k`. Se concatenan los `K` trozos y se
   obtiene la columna `zᵢₘ`, la predicción del modelo `m` para la fila `i` sin haberla visto.
   La matriz `Z` tiene `n` filas y `M` columnas.
2. **Metamodelo.** Se entrena un modelo `g` con entradas `Z` y la etiqueta original `y`:
   `ĝ = argmin_g Σᵢ L(yᵢ, g(zᵢ₁, …, zᵢ_M))`.
3. **Predicción final.** Para datos nuevos, `ŷ = g(m₁(x), …, m_M(x))`, donde cada `mⱼ` es el
   modelo base reentrenado con **todo** `D` (es el paso que casi todo el mundo olvida).

Símbolos: `zᵢₘ` es la predicción del modelo `m` sobre la fila `i` obtenida fuera de muestra;
`L` es la función de pérdida (error cuadrático en regresión, entropía cruzada en
clasificación); `K` es el número de pliegues, normalmente 5 o 10.

Detalle que se pasa por alto: en clasificación, `Z` debe contener **probabilidades**, no
etiquetas. La etiqueta dura convierte una variable continua y bien ordenada en una binaria
que tira casi toda la información, y el metamodelo pierde la capacidad de ponderar por
confianza.

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa con la métrica final si sube |
| --- | --- | --- | --- |
| `M` | Modelos base que se combinan | modelos | Más diversidad que aprovechar, pero más latencia y más formas de filtrar información si la matriz `Z` está mal hecha |
| `K` | Pliegues de la validación cruzada que generan `Z` | pliegues | Sube el coste de entrenamiento y baja el sesgo de `zᵢₘ`; con `K = n` (leave-one-out) cada columna es casi una predicción honesta, pero el metamodelo ve un reparto muy distinto del de producción |
| `n` | Filas disponibles | filas | Más filas para el metamodelo y para cada base: es lo que hace que `Z` sea fiable |
| `zᵢₘ` | Predicción del base `m` para la fila `i`, obtenida fuera de muestra | probabilidad o valor predicho | Es la única entrada del metamodelo: si es una predicción en muestra, el peso se va al base que más memoriza |
| `g` | Metamodelo de la segunda capa | — | Cuanto más flexible, antes aprende ruido de `Z`: con 2 o 3 columnas, la regresión regularizada suele ganar |
| `L` | Función de pérdida del metamodelo | las de la métrica | No cambia `Z`, pero decide qué se optimiza: entropía cruzada para clasificar, error cuadrático para predecir |
| `B` (blending) | Fracción reservada para el metamodelo en vez de usar `K` pliegues | tanto por uno | Sube la calidad de `Z` y baja las filas de entrenamiento de cada base: con el 20 % se desperdicia un quinto de los datos |
:::

## Ejemplo

Con 1.000 filas y tres modelos base, imagina estas exactitudes medidas de dos formas:

| Modelo base | En muestra (mal) | Fuera de muestra (bien) |
| --- | --- | --- |
| Árbol de decisión profundo | 1,00 | 0,71 |
| k-NN con k=5 | 0,88 | 0,78 |
| Regresión logística | 0,77 | 0,77 |

Con la columna «en muestra», el metamodelo aprende un peso cercano a 1 para el árbol, que es
justo el peor de los tres en datos nuevos: el ensemble acaba en torno a 0,70. Con la columna
«fuera de muestra», el metamodelo reparte el peso entre la logística y el k-NN y el resultado
sube a 0,81. **La misma receta, el mismo metamodelo y 11 puntos de diferencia** solo por cómo
se generó la matriz `Z`.

Regla práctica para la segunda capa: usa algo **simple**, una regresión logística con
regularización L2 o una regresión lineal no negativa. Con 3-10 columnas de entrada, un
gradient boosting en la segunda capa vuelve a sobreajustar casi siempre.

:::figura
fichero: stacking-pesos-en-muestra-y-fuera
pie: A la izquierda está el mecanismo del fallo: el peso que aprende el metamodelo depende por completo de cómo se midió cada base. Con predicciones en muestra, el peso se concentra en el que memoriza (0,58 frente a 0,42); medido fuera de muestra, el reparto se reparte entre los dos (0,57 y 0,43). A la derecha, el resultado en datos nuevos con dos base de AUC 0,87 y 0,78: el promedio simple llega a 0,825 y el stacking a 0,831. La lección es que la ganancia del stacking es de milésimas, no de puntos, y que depende de cómo se construya la primera capa.
fuente: figuras/stacking-y-blending-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier

X, y = make_classification(n_samples=600, n_features=12, n_informative=6,
                           class_sep=0.8, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

base = {"bosque": RandomForestClassifier(n_estimators=60, random_state=0),
        "knn": KNeighborsClassifier(n_neighbors=9),
        "logit": LogisticRegression(max_iter=2000)}

# 1) Predicciones FUERA DE MUESTRA: la columna que el metamodelo debe ver.
Z_oof = np.zeros((len(y_tr), len(base)))
for m, (nombre, modelo) in enumerate(base.items()):
    for itr, iva in StratifiedKFold(5, shuffle=True, random_state=0).split(X_tr, y_tr):
        modelo.fit(X_tr[itr], y_tr[itr])
        Z_oof[iva, m] = modelo.predict_proba(X_tr[iva])[:, 1]

# 2) La version tramposa: predicciones del modelo ya entrenado con esas mismas filas.
Z_insample = np.column_stack([m.fit(X_tr, y_tr).predict_proba(X_tr)[:, 1] for m in base.values()])

meta_oof = LogisticRegression(max_iter=2000).fit(Z_oof, y_tr)
meta_ins = LogisticRegression(max_iter=2000).fit(Z_insample, y_tr)

print(f"AUC del metamodelo sobre Z fuera de muestra {roc_auc_score(y_tr, meta_oof.predict_proba(Z_oof)[:, 1]):.3f}")
print(f"AUC del metamodelo sobre Z en muestra      {roc_auc_score(y_tr, meta_ins.predict_proba(Z_insample)[:, 1]):.3f}")
```

:::claves
- `Z_oof = np.zeros((len(y_tr), len(base)))` se rellena **por pliegues**: `Z_oof[iva, m]` escribe
  solo las filas del pliegue de validación. Si te equivocas de índice y escribes `Z_oof[:, m]`,
  cada pliegue pisa al anterior y al final `Z` contiene las predicciones de un solo modelo.
- `StratifiedKFold(5, shuffle=True, random_state=0).split(X_tr, y_tr)` devuelve **pares de índices**
  (`itr`, `iva`), no los datos. Todavía hay que indexar: `X_tr[itr]` para entrenar y `X_tr[iva]`
  para predecir. `shuffle=True` es imprescindible con datos ordenados, y la semilla hace que los
  pliegues sean los mismos cada vez que ejecutes el fichero.
- `predict_proba(...)[:, 1]` coge solo la columna de la clase positiva porque la otra es su
  complementaria: guardar las dos duplica la información y la logística de la segunda capa se
  vuelve inestable. Con `predict()` tendrías 0 y 1 en vez de probabilidades.
- `np.column_stack([...])` pega las columnas de los tres modelos en una matriz `(n, 3)`. Es
  equivalente a ir asignando `Z[:, m]`, pero más corto; lo que **no** es equivalente es que aquí no
  se rellena por pliegues: `m.fit(X_tr, y_tr)` reentrena cada modelo base con todo `X_tr` —`.fit`
  muta el objeto, así que los **tres** quedan reentrenados— y las tres columnas salen en muestra.
  El nombre `m` de la comprensión no escapa: en Python 3 tiene su propio ámbito.
- `meta_oof` y `meta_ins` son dos objetos distintos, pero el metamodelo es el mismo tipo de modelo:
  la única diferencia entre los dos números está en **qué matriz Z** recibió cada uno. Cambia
  `Z_insample` por `Z_oof` y la métrica baja: ese es todo el contenido de la página.
- Ojo con el detalle del final: los dos `roc_auc_score` se calculan sobre `y_tr` y sobre `Z` del
  mismo conjunto con el que se ajustó el metamodelo. Sirven para ver la diferencia entre las dos
  formas de construir `Z`, no como estimación honesta del rendimiento final.
:::

```python verificable
import copy

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Por que el metamodelo debe ser simple: con 600 filas y 2 columnas,
# un metamodelo muy flexible se ajusta al ruido de las predicciones.
X, y = make_classification(n_samples=600, n_features=12, n_informative=6,
                           class_sep=0.8, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

Z_tr = np.zeros((len(y_tr), 2))
Z_te = np.zeros((len(y_te), 2))
for m, modelo in enumerate([LogisticRegression(max_iter=2000), KNeighborsClassifier(n_neighbors=9)]):
    for itr, iva in StratifiedKFold(5, shuffle=True, random_state=0).split(X_tr, y_tr):
        mod = copy.deepcopy(modelo).fit(X_tr[itr], y_tr[itr])
        Z_tr[iva, m] = mod.predict_proba(X_tr[iva])[:, 1]
    mod = copy.deepcopy(modelo).fit(X_tr, y_tr)
    Z_te[:, m] = mod.predict_proba(X_te)[:, 1]

# Un metamodelo que memoriza la matriz Z saca 1.000 en entrenamiento y pierde en prueba.
for nombre, meta in (("logistica L2", LogisticRegression(max_iter=2000)),
                     ("knn k=1", KNeighborsClassifier(n_neighbors=1)),
                     ("knn k=3", KNeighborsClassifier(n_neighbors=3))):
    meta.fit(Z_tr, y_tr)
    auc_tr = roc_auc_score(y_tr, meta.predict_proba(Z_tr)[:, 1])
    auc_te = roc_auc_score(y_te, meta.predict_proba(Z_te)[:, 1])
    print(f"{nombre:<14} AUC entrenamiento {auc_tr:.3f}   AUC prueba {auc_te:.3f}   diferencia {auc_tr - auc_te:+.3f}")
# -> logistica L2   AUC entrenamiento 0.886   AUC prueba 0.900   diferencia -0.015
# -> knn k=1        AUC entrenamiento 1.000   AUC prueba 0.750   diferencia +0.250
# -> knn k=3        AUC entrenamiento 0.936   AUC prueba 0.836   diferencia +0.100
```

## Errores típicos

- **Entrenar el metamodelo con predicciones en muestra.** Es el fallo que destruye el
  stacking y el que más cuesta detectar, porque en validación cruzada interna *parece*
  funcionar: el metamodelo aprende a confiar en el modelo que más memoriza y en datos nuevos
  rinde peor que el mejor base por separado.
- **Reutilizar la misma partición para los base y para el metamodelo sin estratificar.** Si
  los pliegues quedan desbalanceados, un base puede aprender una tasa base distinta en cada
  pliegue y el metamodelo aprende a corregir por la partición, no por la señal. Usa
  [[validacion-cruzada|pliegues estratificados]] y, con series temporales, pliegues
  temporales consecutivos.
- **Pasar etiquetas duras en vez de probabilidades.** Con `predict()` en lugar de
  `predict_proba()` el metamodelo pierde la confianza de cada base y buena parte del
  beneficio del stacking desaparece.
- **Olvidar reentrenar los base con todos los datos.** La matriz `Z` sale de modelos
  entrenados con el 80 % de las filas, pero en producción quieres el base entrenado con el
  100 %. Si lo olvidas, dejas rendimiento sobre la mesa; si lo haces, ten presente que las
  predicciones de producción tendrán una distribución ligeramente distinta de las que vio el
  metamodelo.
- **Metamodelo complejo con pocas columnas.** Un gradient boosting en la segunda capa con
  tres variables de entrada encuentra interacciones donde solo hay ruido. Empieza por la
  regresión logística o lineal regularizada y solo sube de complejidad si la mejora se
  sostiene fuera de muestra.
- **Elegir el ensemble por su métrica en la misma muestra donde lo montaste.** Es
  [[data-snooping-y-multiple-testing|data snooping]]: si pruebas 40 combinaciones y te quedas
  con la mejor, el número está sesgado. Reserva un conjunto que no hayas tocado, o aplica el
  ajuste por pruebas múltiples.

:::practica
enunciado: Tres bases dan estas probabilidades fuera de muestra: con y = 1 → (0,9; 0,6; 0,2), con y = 0 → (0,3; 0,7; 0,6) y con y = 1 → (0,8; 0,7; 0,3). Con umbral 0,5, compara el promedio simple con el ponderado 0,6/0,3/0,1 y decide cuál acierta más.
pista: Aplica los pesos columna a columna; el promedio simple son pesos de un tercio para cada base.
solucion: Simple: (0,9+0,6+0,2)/3 = 0,567; (0,3+0,7+0,6)/3 = 0,533; (0,8+0,7+0,3)/3 = 0,600. Los tres superan 0,5, así que predice 1, 1, 1 y acierta dos de tres. Ponderado: 0,6·0,9 + 0,3·0,6 + 0,1·0,2 = 0,74; 0,6·0,3 + 0,3·0,7 + 0,1·0,6 = 0,45; 0,6·0,8 + 0,3·0,7 + 0,1·0,3 = 0,72. Predice 1, 0, 1 y acierta tres: el peso extra al base que separa mejor corrige la fila que el promedio simple falla.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué pasa si entrenas el metamodelo con las predicciones que cada modelo base hace sobre sus propios datos de entrenamiento?
o: Nada, el metamodelo converge igual porque solo aprende pesos
o: El metamodelo asigna casi todo el peso al base que más ha memorizado y el conjunto rinde peor en datos nuevos que ese mismo base
o: Los modelos base se reentrenan automáticamente con los pesos aprendidos
a: 2
e: Un base flexible con predicciones en muestra parece casi perfecto, así que el metamodelo concentra el peso en él. En datos nuevos ese modelo ya no memoriza y el ensemble se queda sin las virtudes de los demás. Con predicciones fuera de muestra, cada columna refleja lo que el modelo hace de verdad.
:::

:::quiz
p: ¿Qué ventaja tiene el stacking sobre un promedio simple de los mismos modelos?
o: Nunca necesita validación cruzada
o: Aprende cuánto vale cada modelo y puede dar más peso al que acierta más, en lugar de repartir a partes iguales
o: Garantiza una métrica mejor que el mejor de los modelos base
a: 2
e: El promedio da el mismo peso a un modelo excelente y a uno mediocre; el metamodelo estima los pesos a partir de datos fuera de muestra. No hay garantía de mejora: si los base son redundantes o el metamodelo se sobreajusta, el promedio simple gana.
:::

:::trampa
El stacking brilla en competiciones con métrica fija y datos etiquetados de sobra, y suele
desilusionar en producción: añade latencia (hay que servir todos los base), multiplica la
superficie de mantenimiento y gana décimas, no puntos. Antes de montarlo, comprueba cuánto
mejora sobre el simple promedio: si la diferencia es menor que el ruido de tu validación, no
compensa el coste.
:::
