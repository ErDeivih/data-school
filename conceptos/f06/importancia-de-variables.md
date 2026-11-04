---
id: importancia-de-variables
titulo: Importancia de variables
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [arboles-de-decision, bagging-y-random-forest, validacion-cruzada]
tags: [interpretabilidad, seleccion-de-variables, sesgo, modelos]
resumen: La importancia no es una propiedad de la variable sino del modelo y de las demás variables; impureza, permutación y reajuste miden cosas distintas.
fuentes: ["Breiman (2001), 'Random Forests'", "Fisher, Rudin y Dominici (2019), 'All Models are Wrong, but Many are Useful: Learning a Variable's Importance by Studying an Entire Class of Prediction Models Simultaneously'"]
---

## En una frase

«¿Qué variable es más importante?» no tiene respuesta sin decir para qué modelo, con qué datos
y junto a qué otras variables: importancia por impureza, por permutación y por reajuste miden
tres cosas distintas y dan respuestas distintas.

## La idea

Imagina que preguntas quién es el jugador más importante de un equipo. La pregunta no tiene
respuesta hasta que concretas el deporte y las reglas: en baloncesto, quien más canastas mete;
en fútbol, quizá quien más pases completa o quien menos goles encaja. Con las variables pasa lo
mismo. La importancia es una medida de **cuánto ayuda esta variable al modelo que has entrenado
con las demás variables que tienes**. Cambia el modelo, cambian las otras variables, cambia la
métrica y cambia la respuesta.

Hay tres formas de medirla, y cada una responde a una pregunta distinta:

1. **Importancia por impureza (MDI).** Un árbol divide eligiendo la variable que más limpia la
   mezcla de clases. Suma cuánto limpió cada variable en todas sus divisiones y reparte el
   mérito. Es gratis (sale del modelo ya entrenado) y por eso es la que traen todas las
   librerías por defecto. También es la más engañosa: favorece variables continuas y con muchos
   valores distintos, y **nunca da cero**, ni siquiera a columnas de ruido puro.
2. **Importancia por permutación.** Rompe la relación entre una variable y la etiqueta
   desordenando esa columna y mide cuánto empeora el modelo. Es agnóstica al modelo, pero mide
   en la práctica y depende del conjunto donde la calcules. Si dos variables están
   correlacionadas, al romper una dejas a la otra cubriendo el hueco y ambas parecen poco
   importantes.
3. **Reajuste sin la variable (leave-one-out).** Entrena el modelo otra vez sin esa variable y
   compara. Es la medida más honesta —«¿qué pasa si no tengo este dato?»— y la más cara: `p + 1`
   entrenamientos en lugar de uno.

Ninguna es «la correcta». Elige según la pregunta: si quieres entender el modelo, permutación; si
quieres decidir qué datos recoger, reajuste; si quieres un ranking rápido para tantear, MDI, pero
sin creértelo.

## Definición formal

Sea `f` el modelo entrenado, `D` un conjunto de datos (de validación o prueba), `s` una métrica
cuanto más alta mejor y `F` el conjunto de las `p` variables.

**Importancia por impureza (MDI).** Para cada variable `j`:

:::formula
MDI_j = (1 / N) · Σ_{nodos t que dividen por j} n_t · Δimpureza(t)
:::

- `n_t` — número de observaciones que llegan al nodo `t`; `N` el total de la muestra de
  entrenamiento.
- `Δimpureza(t)` — la impureza del nodo menos la media de la impureza de sus dos hijos, ponderada
  por el número de observaciones que caen en cada uno. Con Gini o con entropía.
- Las librerías normalizan al final para que `Σ_j MDI_j = 1`, así que cada valor se lee como
  «proporción del total», no como una cantidad absoluta.

**Importancia por permutación.** Se repite `R` veces:

:::formula
PI_j = s(f, D) − (1/R) · Σ_{r=1..R} s( f, D^{(j, r)} )
:::

- `D^{(j, r)}` — el conjunto `D` con la columna `j` desordenada al azar en la repetición `r`
  (los valores se barajan entre filas, rompiendo la relación con la etiqueta).
- `PI_j > 0` significa que la variable aporta; alrededor de 0, que el modelo funciona igual sin
  ella; **negativo** es normal y significa que el modelo mejora por casualidad al romperla.
- Se debe calcular sobre datos que el modelo no ha visto. En entrenamiento, un modelo
  sobreajustado usa hasta las variables de ruido y todas parecen importantes.

**Reajuste (leave-one-out).**

:::formula
Δ_j = s(f, D) − s( f_{−j}, D )
:::

- `f_{−j}` — el mismo algoritmo entrenado sin la variable `j`.
- Con `p` variables hacen falta `p + 1` entrenamientos (y repetirlos con validación cruzada si
  quieres una estimación estable). Mide el efecto **marginal** de tener la variable, no el
  efecto de perturbarla.

**Valores de Shapley (SHAP).** Reparten la predicción de cada instancia entre las variables,
promediando su contribución marginal sobre todos los subconjuntos posibles:

:::formula
φ_j = Σ_{S ⊆ F \ {j}} ( |S|! · (p − |S| − 1)! / p! ) · ( v(S ∪ {j}) − v(S) )
:::

- `S` — un subconjunto de variables que no incluye a `j`; `v(S)` la predicción del modelo usando
  solo las variables de `S`.
- El peso combinatorio reparte el mérito de forma que se cumpla la aditividad:
  `Σ_j φ_j = f(x) − E[f]`.
- Es exacto pero caro: se aproxima con muestreo, y su interpretación sigue siendo «para este
  modelo», no «para el mundo». Ver [[interpretabilidad-shap]].

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `MDI_j` | Importancia de la variable `j` por impureza, sumada en todos los nodos que dividen por ella | proporción del total: `Σ_j MDI_j = 1` | Sube con el número de valores distintos de la columna aunque no informe de nada: es el sesgo de cardinalidad |
| `PI_j` | Importancia por permutación: cuánto empeora la métrica al desordenar la columna `j` | unidades de la métrica `s` | Si sube, la variable aporta más. Puede salir negativa, y eso solo significa que al romperla el modelo mejoró por casualidad |
| `R` | Número de veces que se repite la permutación para promediarla | repeticiones | Más repeticiones dan una estimación más estable y cuestan más. Con `R = 1` el número es casi todo ruido |
| `Δ_j` | Importancia por reajuste: lo que cae la métrica al entrenar sin la variable `j` | unidades de `s` | Si sube, la variable es más necesaria. Mide el efecto de no tenerla, no el de perturbarla |
| `φ_j` | Valor de Shapley de la variable `j`: su parte del reparto de la predicción | unidades de la predicción | Los `φ_j` de todas las variables suman exactamente `f(x) − E[f]`; ninguna sube sin que otra baje |
| `p` | Número de variables del modelo | columnas | Con `p` grande el reajuste cuesta `p + 1` entrenamientos y la impureza reparte el mismo total entre más candidatas |
:::

## Ejemplo

**Ruido puro que parece importante.** Un random forest con 700 observaciones y 8 variables, de
las cuales solo 3 informan sobre la etiqueta (accuracy en prueba: 0,914). Las importancias por
impureza de las 8 variables son:

```
0,148  0,370  0,117  0,073  0,069  0,070  0,072  0,081
```

Las cinco últimas son ruido y, aun así, todas superan el 0,05. Si ordenaras por MDI y te
quedaras con las seis primeras, incluirías tres columnas que no aportan nada.

Las importancias por permutación de las mismas variables:

```
0,163  0,331  0,106  -0,001  -0,007  0,004  0,005  -0,001
```

Las cinco de ruido quedan en torno a cero (dos en negativo), y las tres informativas se
mantienen. La conclusión práctica: **MDI nunca da cero y hay que leerla en relación con el
número de variables**, mientras que la permutación sí distingue el ruido.

**El sesgo de cardinalidad.** Tres columnas generadas al azar, sin ninguna relación con la
etiqueta (que también es aleatoria):

| Variable | Valores distintos | Impureza | Permutación |
| --- | --- | --- | --- |
| Binaria | 2 | 0,008 | 0,0150 |
| Continua | cientos | 0,523 | −0,0023 |
| Identificador | 400 | 0,469 | −0,0097 |

Ninguna de las tres informa, y sin embargo la impureza reparte casi toda la importancia entre
las dos columnas con más valores distintos. El motivo es que una variable con muchos valores
posibles ofrece muchas formas de partir el nodo, así que alguna división «buena por casualidad»
siempre aparece. La permutación, en cambio, deja las tres en torno a cero. Si comparas
variables de naturaleza distinta con MDI, estás midiendo su cardinalidad tanto como su señal.

:::figura
fichero: importancia-de-variables-mdi-vs-permutacion
pie: A la izquierda, las ocho variables del ejemplo con las dos medidas. Las tres de arriba informan de la etiqueta y las cinco de abajo son ruido puro, y ahí está la lección: la barra azul del ruido se queda entre 0,07 y 0,08, porque la impureza se normaliza y siempre hay alguna división que mejora algo, mientras que la barra roja cae a cero o a negativo. Un ranking de impureza nunca dice «esta variable no aporta», y con muchas columnas eso es quedarse con ruido. A la derecha, las tres columnas aleatorias del segundo ejemplo: ninguna informa y, sin embargo, la impureza entrega 0,523 y 0,469 a la continua y al identificador, que son justo las de más valores distintos. Las tres permutaciones quedan en torno a cero. Conclusión: usa MDI para tantear y permutación o reajuste para decidir, y nunca compares por impureza variables de naturaleza distinta.
fuente: figuras/importancia-de-variables-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# 8 variables: solo 3 informan. Las otras 5 son ruido puro.
X, y = make_classification(n_samples=700, n_features=8, n_informative=3, n_redundant=0,
                           n_repeated=0, shuffle=False, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
bosque = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)

mdi = bosque.feature_importances_      # atributo con guion bajo final: existe solo tras fit
print("accuracy en test:", round(bosque.score(X_te, y_te), 3))       # -> 0.914
print("importancia por impureza:", mdi.round(3).tolist())
# -> [0.148, 0.37, 0.117, 0.073, 0.069, 0.07, 0.072, 0.081]
# mdi[3:] son las cinco ultimas columnas, que son las de ruido: se cuentan con un booleano
print("variables de ruido con impureza > 0.05:", int((mdi[3:] > 0.05).sum()), "de 5")   # -> 5 de 5

# n_repeats=4 promedia cuatro barajados de cada columna (el objeto trae tambien la desviacion)
perm = permutation_importance(bosque, X_te, y_te, n_repeats=4, random_state=0).importances_mean
print("importancia por permutacion:", perm.round(3).tolist())
# -> [0.163, 0.331, 0.106, -0.001, -0.007, 0.004, 0.005, -0.001]
print("variables de ruido con permutacion > 0.01:", int((perm[3:] > 0.01).sum()), "de 5")  # -> 0 de 5
```
:::claves
- `.fit()` devuelve el propio modelo ya entrenado, así que `RandomForestClassifier(...).fit(...)` es el bosque, no `None`. Por eso se puede encadenar sin asignar nada a una variable intermedia.
- `feature_importances_` viene **normalizado**: suma 1 entre todas las variables. Por eso una columna de ruido puro «tiene» 0,072 y no 0: no es una cantidad absoluta, es la parte del total que le tocó.
- `permutation_importance(...)` devuelve un objeto con tres arrays: `importances_mean`, `importances_std` e `importances` (matriz con una fila por variable y una columna por repetición). Si te quedas con el objeto en vez de con `.importances_mean`, no puedes compararlo con nada.
- `n_informative=3` con `n_redundant=0` y `n_repeated=0` es lo que garantiza que las otras cinco columnas sean ruido puro. Con los valores por defecto, `make_classification` añade variables que son combinaciones de las informativas y el ejemplo dejaría de significar lo que dice.
- `shuffle=False` en `make_classification` solo evita que se barajen las filas y las columnas al construir el conjunto: no afecta a la partición, que la decide `train_test_split`. Para repetir el 0,914 hacen falta las dos semillas: la de `make_classification` fija los datos y la de `train_test_split`, qué filas van a prueba.
- Cambia `X_te` por `X_tr` en `permutation_importance` y el ruido deja de quedar en cero: las cinco columnas de ruido pasan de estar en torno a cero a valer entre 0,005 y 0,019, mientras las informativas bajan (0,331 → 0,298, 0,163 → 0,102). Con las filas ya vistas, el bosque ha memorizado el ruido y la permutación mide otra cosa. Es el error que la página señala y aquí se reproduce en una línea.
:::

```python ilustrativo
# El sesgo de cardinalidad con las tres columnas del ejemplo: ninguna informa.
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(3)
y = rng.integers(0, 2, 2000)                     # la etiqueta es puro azar
X = np.column_stack([                            # tres vectores 1-D -> matriz (2000, 3)
    rng.integers(0, 2, 2000),        # binaria: 2 valores distintos
    rng.normal(0, 1, 2000),          # continua: cientos de valores distintos
    rng.integers(0, 400, 2000),      # identificador: 400 valores distintos
])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
bosque = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)

print("impureza:", bosque.feature_importances_.round(3).tolist())
# -> [0.008, 0.523, 0.469]
print("permutacion:", permutation_importance(
    bosque, X_te, y_te, n_repeats=5, random_state=0).importances_mean.round(4).tolist())
# -> [0.015, -0.0023, -0.0097]
```

```python ilustrativo
# El reajuste: la medida que responde a "que pasa si no tengo este dato".
# Cuesta p+1 entrenamientos, asi que se reserva para las variables que de verdad importan.
from sklearn.model_selection import cross_val_score

base = cross_val_score(modelo, X, y, cv=5, scoring="roc_auc").mean()
for j, nombre in enumerate(nombres):
    # axis=1 borra la COLUMNA j; con axis=0 borraria la fila j, que no es lo que queremos
    sin_j = cross_val_score(modelo, np.delete(X, j, axis=1), y, cv=5, scoring="roc_auc").mean()
    print(f"{nombre:20s} caida de AUC {base - sin_j:+.4f}")
```

## Errores típicos

- **Comparar importancias por impureza entre variables de distinta cardinalidad.** Es el sesgo
  del segundo ejemplo: la continua y el identificador se llevan casi todo el peso aunque no
  informen. Si necesitas comparar, usa permutación o reajuste, o agrupa las variables
  categóricas con muchas categorías en una sola.
- **Calcular la permutación en el conjunto de entrenamiento.** El modelo ya ha memorizado esas
  filas, así que romper una columna apenas empeora la métrica y todo parece poco importante; o
  al revés, si el modelo sobreajusta, el ruido parece informativo. Se calcula siempre en
  validación o prueba.
- **Interpretar la importancia como causalidad.** Que el modelo se apoye en una variable no
  significa que cambiarla cambie el resultado. Para afirmar eso hacen falta experimentos o
  supuestos causales explícitos, como en [[confusores-y-dag]].
- **Leer la importancia de variables correlacionadas una a una.** Si dos variables miden casi lo
  mismo, la permutación rompe una y la otra sigue haciendo el trabajo: **las dos** parecen
  irrelevantes y acabas descartando información duplicada pero necesaria. Se corrige permutando
  el grupo entero a la vez.
- **Quedarse con el top 10 y reentrenar con esas variables.** La selección hecha sobre el mismo
  conjunto donde mediste la importancia está sesgada al alza: lo que parece una mejora es
  sobreajuste a la selección. Selecciona con validación dentro del entrenamiento, o comprueba la
  estabilidad con [[bootstrap|remuestreo]].
- **Comparar importancias entre modelos o mirar solo el ranking.** Un random forest y un gradient
  boosting reparten el mérito con reglas distintas, y dos semillas dan rankings distintos en las
  variables del medio, así que compara dentro del mismo modelo y mira la variabilidad entre
  repeticiones (`n_repeats`). Y no te quedes con el orden: que una variable sea la primera no
  significa que aporte, porque si todas las importancias por permutación están en 0,002 el orden
  es ruido.

:::practica
enunciado: Un modelo da estas importancias por permutación a cuatro columnas: 0,163 (informativa), 0,106 (informativa), 0,015 (ruido), 0,004 (ruido). Decides recoger datos nuevos solo para las columnas cuyo valor supere 0,01. ¿Con cuáles te quedas y qué falla en ese criterio?
pista: Compara primero cada valor con el umbral; después mira si el ruido que supera el umbral está lejos de cero.
solucion: Superan 0,01 las columnas de 0,163, 0,106 y 0,015. Las dos informativas quedan claras, pero la de 0,015 es ruido y entra igual. Si su desviación entre repeticiones es 0,012, un 0,015 está a poco más de una desviación de cero, mientras que la informativa de 0,106 está a más de ocho. Conclusión: el umbral fijo no basta; pide la variabilidad entre repeticiones y descarta lo que no se despegue de cero.
:::

## Comprueba que lo sabes

:::quiz
p: Cinco variables de ruido puro obtienen importancias por impureza entre 0,068 y 0,088. ¿Qué significa?
o: Que esas variables son importantes y el modelo las está aprovechando
o: Que la importancia por impureza reparte el total entre todas las variables y no llega a cero ni con ruido
o: Que la semilla del random forest está mal elegida
a: 2
e: La MDI se normaliza para sumar 1, así que cualquier variable que consiga alguna división se lleva una parte. Como un corte aleatorio siempre mejora algo la impureza, el ruido nunca sale a cero. La permutación de las mismas variables sí queda en torno a cero, y esa diferencia es la señal de alarma.
:::

:::quiz
p: Dos variables están correlacionadas entre sí y ambas son útiles. ¿Qué les hace la importancia por permutación calculada de una en una?
o: Les asigna a cada una la mitad de la importancia real
o: Les asigna una importancia baja a las dos, porque al romper una la otra sigue cubriendo la información
o: Les asigna una importancia inflada, porque se refuerzan
a: 2
e: Al desordenar una columna, el modelo sigue teniendo la información a través de su pareja correlacionada, así que la métrica apenas empeora y las dos parecen prescindibles. Es el fallo clásico de la permutación, y se arregla permutando el grupo completo de variables correlacionadas a la vez.
:::

:::quiz
p: ¿Cuál es la diferencia esencial entre la importancia por permutación y la de reajuste?
o: La permutación rompe la relación de la variable con la etiqueta; el reajuste entrena un modelo nuevo sin esa variable
o: La permutación es más cara de calcular
o: El reajuste solo funciona con árboles
a: 1
e: La permutación perturba una columna y evalúa el mismo modelo; el reajuste responde a «¿qué pasa si no tengo este dato?» entrenando de nuevo, lo que cuesta p+1 ajustes y obliga a repetir la validación. El reajuste es más caro y funciona con cualquier modelo, no solo con árboles.
:::

:::trampa
Si tu jefe pide «las cinco variables más importantes» para decidir qué datos recoger, la
respuesta útil no es un ranking de impureza: es el reajuste. La pregunta «¿cuánto empeora el
modelo si no tengo este dato?» es la que se traduce en dinero, y suele tener una respuesta
distinta a la del ranking que trae la librería por defecto.
:::
