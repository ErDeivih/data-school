---
id: validacion-cruzada
titulo: Validación cruzada
fase: 6
nivel: intermedio
rutas: [core, ds]
prerequisitos: [train-val-test, desbalanceo-de-clases, sesgo-varianza]
tags: [evaluacion, k-fold, hiperparametros]
resumen: Partir los datos en k pliegues para estimar y elegir sin gastar un conjunto de prueba, con variantes para clases raras, grupos y series temporales.
fuentes: ["Stone (1974), 'Cross-Validatory Choice and Assessment of Statistical Predictions'", "Kohavi (1995), 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection'"]
---

## En una frase

La validación cruzada reparte los datos en `k` pliegues y repite el entrenamiento `k` veces, dejando
cada vez un pliegue distinto fuera, de forma que todas las observaciones se usan para validar
exactamente una vez y para entrenar `k − 1` veces.

## La idea

Con una sola partición de validación hay dos problemas: se desperdicia una parte de los datos que no
se usa para entrenar, y el resultado depende de qué filas hayan caído en cada lado. Si el 20 % de
validación es una muestra afortunada, el modelo parece mejor de lo que es; si es desafortunada, al
revés.

La validación cruzada resuelve las dos cosas rotando el papel de cada trozo. Es como corregir
exámenes haciendo que cada alumno sea examinador de los demás por turnos: cada fila participa en el
entrenamiento y también sirve de control, y al final tienes `k` medidas en lugar de una. Con esas `k`
medidas haces dos cosas distintas, y conviene no confundirlas:

- **Estimar**: la media de los `k` errores es tu estimación del rendimiento.
- **Decidir**: comparar configuraciones por su error medio y quedarte con la mejor.

La elección de `k` es un compromiso estadístico, no una costumbre:

- `k` pequeño (3 o 5): cada pliegue de entrenamiento es más pequeño (`(k−1)/k` de los datos) y la
  estimación tiene más sesgo pesimista, pero el cómputo es menor y la varianza entre pliegues se ve
  mejor.
- `k` grande (10, 20): cada modelo entrena con casi todos los datos, así que la estimación es menos
  pesimista, pero los `k` entrenamientos son caros y sus resultados están muy correlacionados.
- `k = n` (dejar uno fuera): entrena `n` veces con `n − 1` datos. Casi insesgado, carísimo, y con
  varianza alta, porque los `n` modelos son casi idénticos entre sí.

El estudio clásico de Kohavi sobre conjuntos de datos reales encontró que 10 pliegues era un buen
compromiso entre sesgo y varianza; por eso 5 y 10 son los valores que verás por defecto. Pero la
regla que importa más que el valor de `k` es otra: **lo que se hace con los datos tiene que ocurrir
dentro del pliegue**. Si escalas, imputas o seleccionas variables usando el conjunto completo antes
de partir, la validación cruzada mide una cosa y tú crees que mide otra.

Las variantes existen porque `KFold` puro asume algo que casi nunca se cumple: que las filas son
intercambiables.

## Definición formal

Sea `D` una muestra de `n` observaciones y `κ` un reparto en `k` subconjuntos disjuntos
`P_1, …, P_k` del mismo tamaño aproximado. Para cada pliegue `j`, sea `f̂^{−j}` el modelo entrenado con
`D \ P_j`. El error de validación cruzada es:

:::formula
CV = (1/k) · Σ_{j=1}^{k} ( 1/n_j ) · Σ_{i ∈ P_j} L( y_i , f̂^{−j}(x_i) )
:::

- `P_j` — el pliegue de prueba `j`; `n_j` — su número de observaciones.
- `f̂^{−j}` — el modelo ajustado **sin** el pliegue `j`. El superíndice `−j` significa «sin `j`».
- `L` — la función de pérdida: error cuadrático para regresión, exactitud o log-loss para
  clasificación.
- Si los pliegues tienen tamaños distintos, el `1/n_j` normaliza cada uno: cada pliegue pesa lo
  mismo en la media. La pérdida sobre todas las predicciones juntas sería otra cosa (ponderar cada
  pliegue por `n_j`).

**Incertidumbre.** Con `e_1, …, e_k` los errores de cada pliegue:

:::formula
error_típico ≈ desviación_típica(e_1, …, e_k) / √k
:::

Es una **cota inferior** de la incertidumbre real: los `k` modelos comparten `k − 2` pliegues de
entrenamiento entre sí, así que sus errores están correlacionados y no son `k` medidas
independientes. Comparar dos modelos por una diferencia menor que ese error típico no es concluyente.

Variantes y qué cambia en cada una:

- **Estratificada (`StratifiedKFold`).** Se reparte respetando la proporción de cada clase:
  `n_j^c / n_j ≈ n^c / n` para cada clase `c`. Con clases raras evita pliegues sin positivos
  ([[desbalanceo-de-clases]]).
- **Por grupos (`GroupKFold`).** Los pliegues son una partición de los **grupos**, no de las filas:
  ninguna entidad aparece a la vez en entrenamiento y prueba. Es imprescindible con datos de panel,
  pacientes repetidos o clientes con varias filas.
- **Repetida (`RepeatedKFold`).** Se repite el reparto `R` veces con barajados distintos y se
  promedian los `R · k` errores. Baja la varianza de la estimación, no el error del modelo.
- **Anidada.** El bucle interior elige hiperparámetros y el exterior estima. Es la única forma de
  obtener un número honesto cuando el modelo tiene hiperparámetros que se han buscado
  ([[seleccion-de-hiperparametros]]).
- **Temporal.** Pliegues consecutivos y ventanas hacia delante ([[validacion-temporal]]), con purga y
  embargo si las etiquetas se solapan ([[purged-kfold]]).

:::figura
fichero: validacion-cruzada-reparto-y-fuga
pie: A la izquierda, el porcentaje de positivos que cae en cada pliegue de prueba: barajando filas a lo bruto va del 8,3 % al 21,7 %, estratificando se queda entre el 13,3 % y el 15 % (la tasa real), y por grupos se dispersa otra vez porque no puede controlar las clases. A la derecha, la fuga que ninguna métrica enseña: con KFold, 140 veces un cliente queda con filas en entrenamiento y en prueba sumando los cinco pliegues; con GroupKFold, ninguna. Conclusión: elige el reparto por la estructura de los datos (clases raras, entidades repetidas, tiempo) y no por costumbre.
fuente: figuras/validacion-cruzada-1.py
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `k` | El número de pliegues | adimensional | Cada modelo entrena con `(k−1)/k` de los datos: la estimación es menos pesimista, pero cuesta `k` entrenamientos y los resultados están más correlacionados. Con `k = n` es casi insesgado y carísimo |
| `n` | El número de observaciones | adimensional | Con `k` fijo, más datos reducen el error típico de la estimación. Con 50 filas, `k = 10` deja 5 por pliegue y la métrica es ruido |
| `n_j` | El tamaño del pliegue `j` | adimensional | Pondera la pérdida del pliegue en la fórmula. Si los pliegues son iguales, el peso es el mismo para todos y la suma se simplifica |
| `L` | La función de pérdida | las de la métrica elegida | Cambia lo que se promedia, no el reparto: error cuadrático para regresión, exactitud o log-loss para clasificación. Dos modelos pueden ordenarse al revés según cuál uses |
| `R` | Las repeticiones del reparto (validación repetida) | adimensional | Baja la varianza de la ESTIMACIÓN (promedia `R · k` errores), no el error del modelo. Sirve para decidir empates, no para mejorar |
| `error_típico` | La incertidumbre de la estimación | las de la pérdida | Es una cota INFERIOR: los `k` modelos comparten `k − 2` pliegues y sus errores están correlacionados. Una diferencia menor que esta cifra no es concluyente |
:::

## Ejemplo

Trescientas filas con un 15 % de positivos, agrupadas en 30 clientes de 10 filas cada uno, con 5
pliegues:

```text
reparto         positivos por pliegue (%)
KFold           21,7 · 8,3 · 10,0 · 16,7 · 15,0
StratifiedKFold 13,3 · 13,3 · 15,0 · 15,0 · 15,0
GroupKFold      21,7 · 20,0 · 10,0 · 11,7 · 8,3
```

- `KFold` puro deja un pliegue con el 21,7 % de positivos y otro con el 8,3 %: un factor de 2,6 entre
  el mejor y el peor. La métrica global es una mezcla de escenarios muy distintos.
- `StratifiedKFold` los deja entre el 13,3 % y el 15 %, alrededor de la tasa real del 15 %. Las
  comparaciones entre pliegues pasan a tener sentido.
- `GroupKFold` no controla la proporción de clases (no puede: respeta los grupos), y de ahí su
  dispersión. A cambio, arregla la fuga que `KFold` no ve: con filas barajadas, **140 veces un
  cliente aparece a la vez en entrenamiento y prueba** (sumando los 5 pliegues); con `GroupKFold`,
  0. Si el modelo puede memorizar al cliente, esa fuga infla el resultado.

Y el efecto de elegir hiperparámetros en el mismo bucle donde se mide, con 80 observaciones y una
rejilla de cinco valores de `k` para un clasificador de vecinos:

- Mejor `k` según la búsqueda: 9.
- Nota de la validación cruzada interna (la que se usa para elegir): **0,700**.
- Nota de la validación cruzada anidada: **0,637**, con pliegues de 0,500 · 0,750 · 0,688 · 0,500 ·
  0,750.

Más de seis puntos de diferencia. No es que la búsqueda esté mal hecha: es que el número que devuelve
la búsqueda es el máximo de cinco estimaciones ruidosas, y los máximos son optimistas
([[train-val-test]]).

## Código

```python verificable
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, GroupKFold

rng = np.random.default_rng(2)
n = 300
y = (rng.random(n) < 0.15).astype(int)          # 15 % de positivos
grupos = np.repeat(np.arange(30), 10)           # 30 clientes, 10 filas cada uno
X = rng.normal(size=(n, 4)) + y[:, None] * 0.8

# Proporcion de positivos que cae en cada pliegue de prueba
for nombre, divisor in (("KFold", KFold(5, shuffle=True, random_state=0)),
                        ("Stratified", StratifiedKFold(5, shuffle=True, random_state=0)),
                        ("GroupKFold", GroupKFold(5))):
    pliegues = (divisor.split(X, y, groups=grupos) if nombre == "GroupKFold"
                else divisor.split(X, y))
    print("%s: positivos por pliegue %s"
          % (nombre, " ".join("%.1f" % (100 * y[te].mean()) for _, te in pliegues)))
# -> KFold: positivos por pliegue 21.7 8.3 10.0 16.7 15.0
# -> Stratified: positivos por pliegue 13.3 13.3 15.0 15.0 15.0
# -> GroupKFold: positivos por pliegue 21.7 20.0 10.0 11.7 8.3

# Cuantos clientes aparecen a la vez en entrenamiento y prueba (sumando los 5 pliegues)
fugas = sum(len(set(grupos[tr]) & set(grupos[te]))
            for tr, te in KFold(5, shuffle=True, random_state=0).split(X))
sin_fugas = sum(len(set(grupos[tr]) & set(grupos[te]))
                for tr, te in GroupKFold(5).split(X, y, groups=grupos))
print("clientes compartidos con KFold: %d" % fugas)          # -> clientes compartidos con KFold: 140
print("clientes compartidos con GroupKFold: %d" % sin_fugas)  # -> clientes compartidos con GroupKFold: 0
```

```python verificable
import numpy as np
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

rng = np.random.default_rng(2)
n = 80
y = (rng.random(n) < 0.5).astype(int)
X = rng.normal(size=(n, 4)) + y[:, None] * 0.5
rejilla = {"n_neighbors": [3, 5, 9, 15, 25]}

# Lo habitual: elegir los hiperparametros y quedarse con la nota de esa misma busqueda
busqueda = GridSearchCV(KNeighborsClassifier(), rejilla, cv=5, scoring="accuracy").fit(X, y)

# Lo correcto: la busqueda va dentro de cada pliegue exterior
anidada = cross_val_score(GridSearchCV(KNeighborsClassifier(), rejilla, cv=5),
                          X, y, cv=5, scoring="accuracy")

print("mejor k %d" % busqueda.best_params_["n_neighbors"])   # -> mejor k 9
print("CV interno %.3f" % busqueda.best_score_)              # -> CV interno 0.700
print("CV anidado %.3f" % anidada.mean())                    # -> CV anidado 0.637
print("pliegues anidados", np.round(anidada, 3).tolist())
# -> pliegues anidados [0.5, 0.75, 0.688, 0.5, 0.75]
```

:::claves
- `KFold(5).split(X)` devuelve índices, no datos: hay que indexar (`X[tr]`, `y[te]`). Es el error número uno al empezar con validación cruzada.
- `GroupKFold` reparte grupos enteros y punto: no parte un grupo entre pliegues. Acepta `shuffle` y `random_state` desde scikit-learn 1.6; en 1.5 o anterior esos argumentos lanzan `TypeError`.
- `StratifiedKFold.split(X, y)` exige `y`; `KFold.split` lo ignora. Y `GroupKFold` necesita `groups=` siempre, aunque `y` sea opcional.
- `len(set(grupos[tr]) & set(grupos[te]))` es la intersección de conjuntos, no la de arrays: `np.intersect1d` haría lo mismo pero ordena y deduplica, y aquí solo se cuenta cuántos clientes aparecen a los dos lados.
- `cross_val_score(...)` devuelve un array con una nota por pliegue, no la media. La media hay que pedirla con `.mean()`, y la dispersión entre pliegues es información, no ruido que se descarta.
- `GridSearchCV(..., cv=5).best_score_` está sesgado al alza: es el máximo de 5 estimaciones. Poner el `GridSearchCV` **dentro** de `cross_val_score` (anidada) cambia el número de 0,700 a 0,637, que es la diferencia entre medir la búsqueda y medir el procedimiento.
- `GroupKFold(5)` con `n = 300` y 30 grupos deja 6 grupos (60 filas) fuera en cada pliegue; si los grupos no son divisibles, los pliegues salen de tamaños distintos y scikit-learn no avisa.
:::

## Errores típicos

- **Preprocesar fuera del pliegue.** Escalar con la media global, imputar con la mediana de todo el
  conjunto, seleccionar variables con todos los datos o hacer codificación por objetivo antes de
  partir: todo eso mete información del pliegue de prueba en el entrenamiento. Se hace con
  [[pipelines-de-ml|pipelines]] que se ajustan pliegue a pliegue.
- **Reportar el mejor resultado de la búsqueda como rendimiento final.** El número que devuelve
  `GridSearchCV` está sesgado al alza porque es un máximo. Para reportar, validación anidada o un
  conjunto de prueba aparte.
- **Usar `KFold` cuando las filas no son intercambiables.** Con clases raras, un pliegue puede
  quedarse con dos positivos de 60 y su métrica no mide nada: estratifica. Y con datos agrupados o de
  panel, la misma entidad en entrenamiento y prueba convierte el problema en reconocimiento: ahí
  toca `GroupKFold` o una partición por entidad.
- **Barajar series temporales.** Con datos ordenados en el tiempo, `KFold(shuffle=True)` mide
  interpolación ([[validacion-temporal]]). Aquí se usan pliegues consecutivos, con purga si las
  etiquetas se solapan ([[purged-kfold]]).
- **Elegir `k` por costumbre, sin mirar la muestra ni la dispersión.** El error típico entre pliegues
  suele ser de varios puntos porcentuales y con `k = 5` es solo una cota inferior; si la diferencia
  entre dos modelos es más fina que eso, repite con varias semillas ([[bootstrap]]). Y con 50 filas,
  `k = 10` deja 5 observaciones por pliegue: la métrica es ruido puro.
- **Comparar modelos con particiones distintas.** Dos modelos evaluados con semillas distintas están
  midiendo, en parte, la diferencia entre los repartos. Usa el mismo objeto de partición o, mejor,
  validación cruzada repetida con pares emparejados.

:::practica
enunciado: Tienes 250 filas con 10 positivos (un 4 %). Calcula cuántos positivos caen en cada pliegue con validación cruzada estratificada de 5 y de 10 pliegues, y qué valores puede tomar la exhaustividad de un pliegue.
pista: Los positivos se reparten a partes iguales entre pliegues; la exhaustividad divide por los positivos que le tocan.
solucion: Estratificando, cada pliegue de 50 filas recibe 10/5 = 2 positivos con k = 5, y cada pliegue de 25 recibe 10/10 = 1 con k = 10. Con un solo positivo por pliegue la exhaustividad de ese pliegue solo puede valer 0 o 1, así que su media mide aciertos sueltos, no una tasa: con 10 positivos en total quédate en k = 5 y guarda k = 10 para conjuntos mayores.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la desviación entre pliegues dividida por la raíz de k no es el error típico real de la estimación?
o: Porque los pliegues tienen tamaños distintos y hay que ponderar
o: Porque los k modelos comparten k-2 pliegues de entrenamiento entre sí y sus errores están correlacionados
o: Porque la pérdida no se distribuye de forma normal
a: 2
e: La fórmula desviación / raíz de k supone medidas independientes. En validación cruzada cada modelo se entrena con casi los mismos datos que los demás, así que sus errores se parecen: la cifra resultante es una cota inferior. El tamaño de los pliegues y la forma de la distribución son cuestiones menores al lado de esa dependencia.
:::

:::quiz
p: Tienes 5.000 filas de 800 clientes, con unas 6 filas por cliente, y quieres estimar el rendimiento de un modelo que predice la baja del cliente. ¿Qué esquema usas?
o: KFold con 10 pliegues, barajando las filas
o: GroupKFold por cliente, para que ningún cliente esté en entrenamiento y prueba a la vez
o: StratifiedKFold, estratificando por la variable objetivo
a: 2
e: Con varias filas por cliente, barajar por fila deja al mismo cliente en los dos lados: el modelo puede reconocerlo y el resultado sale optimista. StratifiedKFold arregla el reparto de clases, que aquí no es el problema principal, y no evita la fuga por cliente.
:::

:::quiz
p: Una búsqueda de hiperparámetros con validación cruzada de 5 pliegues devuelve una exactitud de 0,86. La validación cruzada anidada del mismo procedimiento da 0,82. ¿Con qué número te quedas y por qué?
o: Con 0,86, porque es el resultado de la búsqueda y usa más información
o: Con 0,82, porque la búsqueda elige el máximo de varias estimaciones y eso lo hace optimista
o: Con la media de los dos, 0,84
a: 2
e: La búsqueda devuelve la mejor de varias estimaciones, así que incorpora la casualidad favorable del reparto; la anidada mide el procedimiento completo en datos que no han intervenido en la elección. Promediar dos estimaciones con sesgos distintos no arregla nada.
:::
