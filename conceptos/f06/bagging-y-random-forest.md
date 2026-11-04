---
id: bagging-y-random-forest
titulo: Bagging y Random Forest
fase: 6
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [arboles-de-decision, sesgo-varianza, bootstrap]
tags: [ensembles, bagging, varianza, bosques]
resumen: Entrenar muchos árboles sobre muestras bootstrap y promediar: baja la varianza, y el submuestreo de variables evita que todos se equivoquen igual.
fuentes: ["Breiman (1996), 'Bagging Predictors'", "Breiman (2001), 'Random Forests'"]
---

## En una frase

Bagging entrena muchos modelos parecidos sobre remuestras aleatorias de los datos y promedia
sus predicciones; Random Forest hace lo mismo con árboles y añade una dosis extra de azar
(dejar que cada corte mire solo un subconjunto de variables) para que los árboles no se
equivoquen todos en lo mismo.

## La idea

Un árbol de decisión tiene poca tendencia a equivocarse de forma sistemática (sesgo bajo) y
mucha a cambiar si le tocas los datos (varianza alta). Cambia tres ejemplos y la primera
división puede ser otra, y el árbol entero cambia con ella. Es el perfil exacto de modelo que
se arregla promediando.

La receta es la del [[bootstrap]]: en lugar de entrenar un árbol con tus `n` filas, sortea `n`
filas **con reemplazo** (algunas salen repetidas, otras no salen) y entrena un árbol con cada
remuestra. Repite 100 veces y tendrás 100 árboles distintos. Para predecir, vota el conjunto (en
clasificación) o promedia (en regresión).

¿Por qué funciona? Porque los errores aleatorios de los árboles se cancelan al promediar. Pero
hay un límite que casi nadie menciona: si los árboles están **correlacionados**, promediar no
sirve de mucho. Imagina 100 personas que copian del mismo compañero: la media de sus respuestas
tiene la misma probabilidad de error que la del compañero copiado. La fórmula de la varianza de
la media de `n` modelos con correlación `ρ` lo deja claro:

:::formula
Var(media) = ρ · σ² + (1 − ρ) · σ² / n
:::

- `σ²` — varianza de un modelo individual.
- `ρ` — correlación media entre los errores de dos modelos distintos.
- `n` — número de modelos que promedias.

El segundo término desaparece con muchos modelos, pero el primero, `ρσ²`, se queda: es el
**suelo** por debajo del cual no puedes bajar por muchos árboles que añadas. Aquí es donde
entra Random Forest. Un árbol con datos ruidosos tiende a elegir la variable más predictiva
para el primer corte, así que todos los árboles se parecen en la cima. La solución de Breiman
es obligar a cada corte a considerar solo una muestra aleatoria de variables: en clasificación,
la raíz cuadrada del número de variables (por ejemplo, 3 de 10); en regresión, un tercio. Con
eso los árboles siguen siendo buenos, pero dejan de estar de acuerdo, y `ρ` baja.

El regalo adicional es la estimación **out-of-bag** (OOB). Como cada árbol se entrena con una
remuestra con reemplazo, alrededor del 37 % de las filas no entra en ese árbol
(`1 − 1/e ≈ 0,368`). Para cada fila puedes predecir solo con los árboles que no la vieron y
comparar con su etiqueta real: eso es un conjunto de validación gratis, del tamaño de tu
muestra, sin sacrificar datos de entrenamiento.

## Definición formal

Con `B` remuestras bootstrap y `T_b` el modelo entrenado con la remuestra `b`:

- **Clasificación:** la predicción es la clase más votada,
  `ŷ = argmax_k Σ_b 1[T_b(x) = k]`. También se puede promediar la probabilidad estimada de cada
  árbol, que suele dar una probabilidad mejor calibrada que el voto.
- **Regresión:** la predicción es la media, `ŷ = (1/B) · Σ_b T_b(x)`.

- `B` — número de árboles. No es un parámetro que provoque sobreajuste al subirlo: la curva de
  error se aplana, no empeora.
- `T_b` — árbol entrenado con la remuestra `b`.
- `1[·]` — función indicadora: vale 1 si la condición se cumple y 0 si no.

La varianza del promedio es la fórmula anterior. En Random Forest, el parámetro clave es
`max_features` (el número de variables que se consideran en cada corte): bajarlo reduce `ρ` pero
sube el sesgo de cada árbol individual. Ese es el compromiso que se ajusta por validación
cruzada.

El error OOB se calcula así: para cada fila `i`, sea `S_i` el conjunto de árboles en cuya
remuestra **no** entró. La predicción OOB de la fila `i` es el voto o media de `S_i`, y el error
OOB es el error de esas predicciones sobre todas las filas. Solo es válido si las filas son
intercambiables: con datos agrupados, duplicados o series temporales, deja de ser una
estimación honesta.

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa con la varianza del conjunto si sube |
| --- | --- | --- | --- |
| `σ²` | Varianza de un solo modelo de los que promedias | al cuadrado, en las unidades de la predicción | Sube la varianza del conjunto en la misma proporción: es un factor de escala |
| `ρ` | Correlación media entre los errores de dos modelos distintos | entre 0 y 1 | Sube el **suelo** `ρσ²` y promediar deja de servir: con `ρ = 0,8`, cien modelos se quedan en 0,80 |
| `n` (o `B`) | Número de modelos que promedias | modelos | Solo baja el término `(1 − ρ)σ²/n`: mucho al principio y casi nada a partir de unas decenas |
| `max_features` | Variables que puede mirar cada corte | variables por corte | Al bajarlo baja `ρ`, que es lo que de verdad mueve la varianza, pero sube el sesgo de cada árbol |
| `n_estimators` | Árboles del bosque | árboles | Nunca empeora, pero tampoco perfora el suelo `ρσ²`: pasado un punto solo cuesta tiempo |
| `min_samples_leaf` | Mínimo de filas por hoja | filas | Al subirlo, cada árbol es menos profundo: baja su varianza y sube su sesgo |
| OOB | Filas que quedan fuera de la remuestra bootstrap de un árbol | fracción de la muestra | No depende de nada que ajustes: con `n` filas tiende a `1 − 1/e ≈ 0,368` |
:::

:::figura
fichero: bagging-suelo-de-varianza-y-oob
pie: A la izquierda está el motivo de que exista Random Forest. Si los modelos no estuvieran correlacionados (ρ = 0), promediar cien bajaría la varianza cien veces; pero cada curva se aplana en su propio suelo, que es ρ, y con ρ = 0,8 cien árboles apenas mueven el resultado. Promediar más modelos no arregla la correlación: lo que la baja es el submuestreo de variables de cada corte. A la derecha, la consecuencia práctica: el error out-of-bag estima el error real sin reservar datos, aunque con muy pocos árboles es pesimista porque cada fila se predice con uno o dos. Pasados unos 30 árboles la curva OOB se aplana en 0,27-0,30 mientras la de prueba sigue bajando hasta 0,15: en este conjunto la OOB se queda más de diez puntos por encima del error real, o sea que es conservadora, y añadir más árboles ya solo cuesta tiempo.
fuente: figuras/bagging-y-random-forest-1.py
:::

## Ejemplo

Con `σ² = 1` (varianza de un árbol) y distintos valores de correlación, la varianza del
promedio es:

```
rho=0.0  n=1 1.000  n=10 0.100  n=100 0.010
rho=0.3  n=1 1.000  n=10 0.370  n=100 0.307
rho=0.8  n=1 1.000  n=10 0.820  n=100 0.802
```

Lee la primera fila: si los árboles no estuvieran correlacionados en absoluto, promediar 100
reduciría la varianza de 1,000 a 0,010, cien veces menos. En la fila `ρ = 0,8`, pasar de 1 a 100
árboles apenas baja de 1,000 a 0,802: los árboles son casi el mismo y promediar no aporta casi
nada. Con `ρ = 0,3`, un valor realista con submuestreo de variables, 100 árboles dejan la
varianza en 0,307, tres veces menos que uno solo, y añadir más árboles ya casi no mejora.

En la práctica, con 300 observaciones y ruido en las etiquetas:

```
un arbol train 1.000  test 0.792
bosque   train 1.000  test 0.833
OOB del bosque 0.844
```

El árbol solo acierta 0,792 fuera de muestra; el bosque de 60 árboles sube a 0,833, y su
estimación OOB, 0,844, es del mismo orden (ligeramente optimista porque cada fila se predice con
unos 22 árboles, no con los 60). Fíjate en que el acierto de entrenamiento es 1,000 en los dos:
el bosque no arregla el sobreajuste de cada árbol, lo compensa promediando.

## Código

```python verificable
import numpy as np

# Varianza de la media de n modelos con varianza 1 y correlacion rho entre ellos:
# Var = rho + (1 - rho) / n
for rho in (0.0, 0.3, 0.8):
    v = [rho + (1 - rho) / n for n in (1, 10, 100)]
    print(f"rho={rho:.1f}  n=1 {v[0]:.3f}  n=10 {v[1]:.3f}  n=100 {v[2]:.3f}")
# -> rho=0.0  n=1 1.000  n=10 0.100  n=100 0.010
# -> rho=0.3  n=1 1.000  n=10 0.370  n=100 0.307
# -> rho=0.8  n=1 1.000  n=10 0.820  n=100 0.802
```

:::claves
- En `v = [rho + (1 - rho) / n for n in (1, 10, 100)]` la variable `n` de la lista de comprensión
  **tapa** a cualquier otra `n` del programa mientras dura el bucle. Y ojo: aquí `n` es el número
  de modelos, no el de filas, aunque en Random Forest la letra se use para las dos cosas.
- `.oob_score_` solo existe si construyes el bosque con `oob_score=True`. Es una **propiedad** que
  se calcula durante el `fit`, no un método: si la llamas como `bosque.oob_score_()` da error.
  Viene dada como acierto (0,844), no como error: para el error hay que hacer `1 - oob_score_`.
- `n_jobs=1` es a propósito: el resultado se reproduce igual en cualquier máquina. Con `n_jobs=-1`
  (todos los núcleos) los árboles se reparten entre procesos y el orden de los votos cambia, así
  que el número final puede bailar en el tercer decimal.
- `flip_y=0.15` de `make_classification` cambia el 15 % de las etiquetas al azar. Sin ese ruido el
  problema sería separable y todo daría 1,000: el ruido es lo que hace visible la diferencia entre
  un árbol y un bosque.
- `train_test_split(..., test_size=0.4)` devuelve cuatro cosas y **en ese orden**:
  `X_tr, X_te, y_tr, y_te`. Si cruzas las dos últimas, el modelo se entrena con las etiquetas de
  prueba y no te enteras hasta que la métrica sale absurda.
- `max_features` no aparece en el código porque su valor por defecto en clasificación ya es
  `"sqrt"`: cada corte mira la raíz del número de variables (2 de 6 aquí). Ese valor por defecto es
  justamente lo que hace que los árboles no se parezcan entre sí, y por eso Random Forest no lo
  toca: bajarlo reduce todavía más la correlación `ρ` a cambio de subir el sesgo de cada árbol.
:::

```python verificable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           flip_y=0.15, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

arbol = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
bosque = RandomForestClassifier(n_estimators=60, oob_score=True,
                                random_state=0, n_jobs=1).fit(X_tr, y_tr)

print(f"un arbol train {arbol.score(X_tr, y_tr):.3f}  test {arbol.score(X_te, y_te):.3f}")
print(f"bosque   train {bosque.score(X_tr, y_tr):.3f}  test {bosque.score(X_te, y_te):.3f}")
print(f"OOB del bosque {bosque.oob_score_:.3f}")
# -> un arbol train 1.000  test 0.792
# -> bosque   train 1.000  test 0.833
# -> OOB del bosque 0.844
```

## Errores típicos

- **Creer que añadir árboles arregla cualquier cosa.** Más árboles nunca empeoran el resultado,
  pero tampoco bajan del suelo `ρσ²`. Si tus 500 árboles van mal, el problema es la correlación
  entre ellos o las variables, no el número.
- **Usar el error OOB con datos que no son intercambiables.** Con filas duplicadas, con varias
  filas por paciente o cliente, o con series temporales, una fila «no vista» por un árbol puede
  ser casi idéntica a otra que sí vio. El OOB sale entonces demasiado optimista. Para series
  temporales hace falta [[validacion-temporal|validación temporal]] o
  [[purged-kfold|purgar y embargar]].
- **Comparar dos bosques con distinto `max_features` y atribuir la diferencia a otra cosa.**
  `max_features` controla directamente `ρ`, y con él el rendimiento. Si no lo fijas igual en
  todas las pruebas, la comparación no significa nada.
- **Interpretar la importancia por impureza del bosque como una lista de causas.** Hereda el
  sesgo del árbol: favorece a las variables con más valores distintos. Además, con variables
  correlacionadas reparte la importancia entre ellas de forma inestable.
- **Aplicar el bosque a una regresión esperando extrapolación.** Un bosque predice promedios de
  hojas, así que nunca devuelve un valor mayor que el máximo visto en entrenamiento. Si la
  tendencia continúa fuera del rango, el bosque se queda plano y hay que usar otro modelo.
- **Olvidar que el bosque no es interpretable por sí mismo.** Pierdes el «si esto, entonces
  aquello» del árbol individual. Si necesitas reglas, o usas un árbol podado y pequeño, o pasas
  a [[importancia-de-variables|importancia por permutación]] y explicaciones por observación.

:::practica
enunciado: Un bosque tiene 25 árboles con varianza individual 4 y correlación media 0,5 entre sus errores. Calcula la varianza del promedio y decide cuánto se gana si el submuestreo de variables baja la correlación a 0,2 sin tocar el número de árboles.
pista: La varianza del promedio es ρσ² más el resto repartido entre el número de modelos; el primer término no depende de cuántos añadas.
solucion: Con ρ = 0,5: Var = 0,5 · 4 + 0,5 · 4/25 = 2 + 0,08 = 2,08. Con ρ = 0,2: 0,2 · 4 + 0,8 · 4/25 = 0,8 + 0,128 = 0,928. El suelo por correlación pasa de 2 a 0,8: bajar ρ reduce la varianza más de la mitad, mientras que multiplicar los árboles por cuatro solo recortaría el término pequeño.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué Random Forest usa un subconjunto aleatorio de variables en cada corte?
o: Para entrenar más rápido y ahorrar memoria
o: Para reducir la correlación entre árboles, que es el suelo que impide bajar la varianza al promediar
o: Para aumentar el sesgo de cada árbol y así regularizar
a: 2
e: El término rho*sigma^2 de la varianza del promedio no desaparece por muchos árboles que añadas. Al limitar las variables por corte, los árboles dejan de elegir todos la misma variable dominante y bajan su correlación. El ahorro de tiempo es un efecto secundario, no el motivo.
:::

:::quiz
p: Con varianza individual 1 y correlación 0,8 entre modelos, promediar 100 modelos deja la varianza en 0,802. ¿Qué conclusión sacas?
o: Que hay un error en la fórmula, porque promediar 100 siempre divide la varianza entre 100
o: Que la correlación impone un suelo y promediar más modelos apenas ayuda si están muy correlacionados
o: Que hay que usar 1.000 modelos para bajar de 0,5
a: 2
e: La fórmula rho + (1-rho)/n tiene un término fijo rho que no depende de n. Con rho=0,8 el suelo es 0,8, así que pasar de 1 a 100 modelos solo baja de 1,000 a 0,802. Solo el término (1-rho)/n se reparte con n.
:::

:::quiz
p: ¿Qué mide el error out-of-bag?
o: El error del bosque en las filas que quedaron fuera de la remuestra bootstrap de cada árbol
o: El error del bosque en un 20 % de datos reservado antes de entrenar
o: La diferencia entre el error de entrenamiento y el de prueba
a: 1
e: Cada árbol se entrena con una remuestra con reemplazo que deja fuera cerca del 37 % de las filas. Cada fila se predice con los árboles que no la vieron, y el error OOB es el de esas predicciones. No hay ningún conjunto reservado: es una validación interna, y solo vale si las filas son intercambiables.
:::
