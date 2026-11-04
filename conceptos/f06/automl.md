---
id: automl
titulo: AutoML
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [seleccion-de-hiperparametros, pipelines-de-ml, validacion-cruzada, fuga-de-datos]
tags: [practica, automatizacion, presupuesto, validacion]
resumen: Busqueda automática de modelos, variables e hiperparámetros: acelera el punto de partida y no sustituye a entender el problema
fuentes: ["Feurer et al. (2015), 'Efficient and Robust Automated Machine Learning'", "He et al. (2021), 'AutoML: A Survey of the State-of-the-Art'"]
---

## En una frase

AutoML es un programa que, dado un conjunto de datos y una métrica, prueba por ti
preprocesamientos, modelos e hiperparámetros, los evalúa con validación cruzada y devuelve el
mejor pipeline que ha encontrado dentro de un presupuesto de tiempo.

## La idea

Un proyecto de machine learning tiene una parte mecánica y una parte de criterio. La mecánica
es enumerable: ¿imputo con la mediana o con la media?, ¿estandarizo o dejo los datos como
están?, ¿un bosque de 200 árboles o un boosting con tasa 0,05? Son decisiones que se pueden
probar y medir. La parte de criterio no es enumerable: qué problema estás resolviendo, qué
métrica refleja ese problema, qué filas no deberían estar en el conjunto de datos, qué
significa un falso positivo en tu negocio.

AutoML automatiza la primera parte y es muy bueno en ella. Un buscador moderno encadena
[[pipelines-de-ml|pipelines]] completos y los compara con [[validacion-cruzada|validación
cruzada]]: en lugar de buscar solo `C` y `gamma`, busca a la vez el imputador, el escalador,
el selector de variables y el modelo. En unos minutos te da un punto de partida razonable, y
a veces te enseña algo: que un `RandomForest` con los valores por defecto rinde casi igual
que la red que ibas a construir a mano.

Lo que no hace es entender el problema. Si la métrica que le das es la exactitud y tus clases
están desbalanceadas al 2 %, optimizará una métrica que no distingue un modelo útil de uno que
predice siempre la clase mayoritaria. Si el conjunto tiene [[fuga-de-datos|fuga de datos]], la
encontrará y la explotará encantado, porque para el buscador la fuga es señal. Y si el
conjunto de validación es demasiado pequeño, el ganador de la búsqueda puede ser el que tuvo
suerte en el reparto.

Hay un segundo efecto, más sutil, que conviene tener presente: **cuantas más configuraciones
prueba un buscador, más alto es el mejor resultado, aunque ningún modelo sea mejor que otro**.
Es el mismo sesgo del máximo de `N` intentos que aparece en
[[seleccion-de-hiperparametros|la búsqueda de hiperparámetros]], pero amplificado, porque
AutoML prueba cientos o miles. Por eso el valor que devuelve el buscador es una estimación
optimista y hay que verificarlo con datos que la búsqueda no haya visto.

## Definición formal

Un problema de AutoML es una terna: un espacio de búsqueda `A`, una métrica `L` y un
presupuesto `B`. El buscador resuelve:

:::formula
A* = argmin_{A ∈ 𝒜}  L̂(A, D_val)     sujeto a  coste(A) ≤ B
:::

- `A` — un pipeline completo y configurado: imputador, transformaciones, modelo e
  hiperparámetros. Es el objeto que se busca.
- `𝒜` — el espacio de todos los pipelines construibles con los bloques disponibles.
- `D_val` — los datos de validación; `L̂` es la métrica estimada ahí, no la real.
- `B` — el presupuesto: tiempo de reloj, número de configuraciones o número de épocas.
- `coste(A)` — lo que cuesta entrenar y evaluar `A` dentro del presupuesto.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `A` | Un pipeline completo y configurado: imputador, transformaciones, modelo e hiperparámetros | no tiene unidades: es un objeto | No es algo que suba; cambiar `A` cambia la puntuación, y el buscador prueba cientos o miles |
| `𝒜` | El espacio de todos los pipelines construibles con los bloques disponibles | número de configuraciones posibles | Cuanto más grande, más tarda la búsqueda y más probable es que el ganador deba su ventaja a la casualidad |
| `L̂(A, D_val)` | La pérdida estimada en validación: el error que se deriva de tu métrica (1 − exactitud, 1 − AUC, o el RMSE de un regresor) | las de la métrica | Es lo que el buscador minimiza. Al ser una estimación, el mínimo de muchas es optimista por construcción |
| `D_val` | Los datos de validación con los que se puntúa cada candidata | filas | Si es pequeño, el ganador cambia al cambiar la semilla: con 105 filas, una ventaja de una décima es casi toda casualidad |
| `B` | El presupuesto: tiempo de reloj, número de configuraciones o número de épocas | segundos, intentos o épocas | Más presupuesto sube el mejor resultado **y** su sesgo: lo que devuelve el buscador es un techo, no una promesa |
| `coste(A)` | Lo que cuesta entrenar y evaluar esa candidata | lo mismo que `B` | Si `coste(A)` supera `B`, la candidata se descarta aunque fuera la buena: el presupuesto decide qué se llega a probar |
:::

La optimización se hace casi siempre con búsqueda aleatoria, bayesiana o por bandidos, más un
mecanismo de parada temprana (Hyperband, ASHA) que asigna poco presupuesto a las malas
candidatas y lo dobla en las buenas. Los componentes típicos que se buscan a la vez son:

| Componente | Qué se prueba |
| --- | --- |
| Imputación | mediana, media, KNN, indicador de ausencia |
| Codificación | one-hot, ordinal, target encoding |
| Escalado | ninguno, estandarizar, normalizar, logaritmo |
| Selección | ninguna, por filtro, por modelo, PCA |
| Modelo | regresión, bosque, boosting, SVM, red pequeña |

Dos garantías que AutoML **no** da, y conviene decirlas en voz alta: no garantiza haber
encontrado el mejor modelo posible (el espacio es demasiado grande y la búsqueda es
incompleta), y no garantiza que `L̂` sea una buena estimación de lo que pasará en producción
(el buscador selecciona sobre `D_val`, así que `L̂` está sesgado al alza).

## Ejemplo

150 filas, 8 variables y mucha menos señal de la que parece: solo 2 variables informan y la
etiqueta tiene ruido. Un buscador prueba 100 configuraciones al azar de una regresión Ridge,
las puntúa con validación cruzada de 3 pliegues y elige la mejor.

```
split 0:  CV del ganador +0,033   R2 en test +0,166   mediana de las 100 -0,027
split 1:  CV del ganador +0,126   R2 en test +0,178   mediana de las 100 +0,097
split 2:  CV del ganador +0,040   R2 en test +0,152   mediana de las 100 +0,005
```

Léelo despacio, porque es la lección central de esta página. En los tres repartos, la
configuración ganadora saca entre 0,03 y 0,13 en validación mientras la mediana de las 100
configuraciones está en torno a 0, aunque se mueve de un reparto a otro: la búsqueda presenta
una ventaja de entre tres y seis centésimas sobre el montón. En datos nuevos los tres ganadores
rinden entre 0,15 y 0,18, en una horquilla de tres centésimas: la diferencia entre ellos es
ruido. Los dos números se miden sobre conjuntos distintos, así que no se comparan entre
sí: lo que se compara es la dispersión. La conclusión no es que buscar fuera inútil, sino que
**el tamaño de la mejora que anuncia la validación es optimista**: el máximo de 100 mediciones
ruidosas sobre 105 filas de entrenamiento recoge mucha casualidad. Para elegir, la validación
sirve; para cuantificar cuánto has mejorado, no.

Conclusión práctica: el valor que devuelve un buscador es un techo, no una promesa. Si te
ahorra tiempo para llegar a un punto de partida decente, perfecto; si la diferencia entre el
ganador y el resto es pequeña, no te la creas sin verificarla en datos que la búsqueda no haya
tocado.

:::figura
fichero: automl-el-mejor-de-n-engana
pie: A la izquierda, los tres repartos del ejemplo con sus 100 configuraciones cada uno. Los puntos azules son las candidatas, la raya morada es la mediana del montón y el punto rojo es el máximo, que es lo que el buscador devuelve. La distancia entre el rojo y la mediana es la «mejora» que anuncia la búsqueda, y fíjate en que la mediana se mueve de un reparto a otro mientras el ganador siempre está por encima: está eligiendo el mejor de 100 números ruidosos, no el mejor modelo. A la derecha, el número que el buscador va anunciando según gasta presupuesto: sube solo, porque solo puede quedarse con lo mejor que ha visto. Conclusión: compara siempre el ganador contra la mediana, mide el ganador en datos que la búsqueda no haya tocado, y si la ventaja se deshincha, quédate con el pipeline más simple.
fuente: figuras/automl-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, train_test_split

# Senal debil y mucho ruido: el escenario donde "el mejor de N" engana
X, y = make_regression(n_samples=150, n_features=8, n_informative=2,
                       noise=45.0, random_state=0)

for semilla in (0, 1, 2):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=semilla)
    rng = np.random.default_rng(semilla)
    alphas = 10 ** rng.uniform(-3, 3, size=100)          # 100 configuraciones al azar
    # np.array es lo que permite usar argmax y median despues; una lista no las tiene
    puntuaciones = np.array([cross_val_score(Ridge(alpha=a), X_tr, y_tr, cv=3,
                                             scoring="r2").mean() for a in alphas])
    mejor = int(np.argmax(puntuaciones))
    modelo = Ridge(alpha=alphas[mejor]).fit(X_tr, y_tr)  # se reentrena el ganador para medirlo
    print(f"split {semilla}: CV del ganador {puntuaciones[mejor]:+.3f}"
          f"   R2 en test {modelo.score(X_te, y_te):+.3f}"
          f"   mediana de las 100 {np.median(puntuaciones):+.3f}")
# -> split 0: CV del ganador +0.033   R2 en test +0.166   mediana de las 100 -0.027
# -> split 1: CV del ganador +0.126   R2 en test +0.178   mediana de las 100 +0.097
# -> split 2: CV del ganador +0.040   R2 en test +0.152   mediana de las 100 +0.005
```

:::claves
- `Ridge(alpha=a)` se crea **dentro** de la lista por comprensión: hay un modelo nuevo por cada valor de `alpha`. Reutilizar un mismo objeto y cambiarle `alpha` a mano entre iteraciones funciona, pero el objeto que guardas al final ya no es el que obtuvo cada puntuación.
- `scoring="r2"` se escribe aunque sea el valor por defecto de `cross_val_score` sobre un regresor. Explicitarlo evita que una versión distinta de scikit-learn te devuelva otra métrica y que compares peras con manzanas contra el `R2` de prueba.
- `np.argmax(puntuaciones)` devuelve la **posición** del máximo, no el valor, y un `np.int64`, no un `int` de Python. Por eso hacen falta las dos cosas: `alphas[mejor]` para recuperar el alpha y `int(...)` para que el número se pueda serializar, porque con NumPy 2 un `np.int64` suelto rompe más de un `json.dump`. Confundir el índice con la puntuación es un error silencioso que el programa no detecta.
- `10 ** rng.uniform(-3, 3, size=100)` muestrea el exponente, es decir, busca `alpha` en escala logarítmica. Con `rng.uniform(1e-3, 1e3, size=100)` el 99,9 % de los valores quedaría por encima de 1 y la zona pequeña no se exploraría.
- El formato `{puntuaciones[mejor]:+.3f}` obliga a que el número lleve signo. Sin el `+`, un R² de 0,033 y uno de −0,033 se leerían parecidos, y aquí el signo es justo lo que distingue «algo de señal» de «ruido».
- Cambia `size=100` por `size=5` en la lista de `alphas`: la mediana del montón casi no se mueve, pero el ganador baja varias centésimas. Su ventaja era el máximo de muchas tiradas, no una virtud de la configuración.
:::

```python ilustrativo
# AutoML de verdad: FLAML o AutoGluon buscan modelo y preprocesado a la vez.
# Va como ilustrativo porque necesita una libreria que no esta en la lista permitida.
from flaml import AutoML

automl = AutoML()
automl.fit(X_entrenamiento, y_entrenamiento, task="classification",
           metric="roc_auc", time_budget=300)      # 300 segundos: el presupuesto se fija antes
print(automl.best_loss, automl.best_config)

# Lo primero que hay que mirar no es el ganador, sino la linea base
from sklearn.dummy import DummyClassifier
linea_base = DummyClassifier(strategy="most_frequent").fit(X_entrenamiento, y_entrenamiento)
print(linea_base.score(X_validacion, y_validacion))
```

## Errores típicos

- **Darle a AutoML el conjunto de prueba.** Algunas herramientas parten los datos por su
  cuenta y otras no; si le pasas todo el conjunto, la búsqueda elige mirando el test y el
  número final no vale nada. Pásale solo entrenamiento y guarda el test para el final.
- **Confundir automatizar con resolver.** AutoML elige el modelo, no define el problema. Con
  la métrica equivocada (exactitud en clases desbalanceadas), el mejor pipeline según el
  buscador puede ser el que predice siempre la clase mayoritaria.
- **Creer que el pipeline ganador es el mejor posible.** La búsqueda es incompleta y depende
  de la semilla: dos ejecuciones del mismo buscador con la misma configuración pueden dar
  ganadores distintos con rendimiento casi idéntico. Si el ganador cambia según la semilla,
  la decisión no está tomada por los datos.
- **No comparar contra la línea base.** Antes de celebrar un AUC de 0,78, mira qué da
  predecir siempre la clase mayoritaria o la media. Sin esa referencia, el número no significa
  nada.
- **Ignorarlo cuando hay estructura que el buscador no puede adivinar.** Si el problema tiene
  grupos (varios registros por paciente, por cliente, por sensor), hay que particionar por
  grupo; si es una serie temporal, hay que validar hacia delante. Ninguna búsqueda automática
  adivina eso si se lo pasas como filas independientes.
- **Dejar que el buscador optimice sin control de coste.** Un presupuesto abierto puede
  gastar horas de cómputo para mejorar 0,002 en la métrica, y la factura la pagas tú. Fija
  presupuesto, métrica y criterio de parada antes de lanzarlo.

:::practica
enunciado: Un buscador ha probado 300 configuraciones. La ganadora da 0,82 en validación cruzada y la mediana de las 300 es 0,74. Mides la ganadora en un conjunto que la búsqueda no tocó y da 0,76. ¿Cuánto bajó la ventaja y qué modelo eliges, sabiendo que la tolerancia del conjunto externo es 0,02?
pista: Calcula primero la ventaja en validación, luego la ventaja en el conjunto externo, y compara esta última con la tolerancia.
solucion: En validación la ventaja era 0,82 − 0,74 = 0,08. En el conjunto externo queda 0,76 − 0,74 = 0,02, justo en el límite de la tolerancia. La ganadora no es falsa, pero casi toda la ventaja que anunciaba la búsqueda era el sesgo del máximo de 300 mediciones ruidosas. Si la diferencia con la segunda clasificada es menor que 0,02, elige el pipeline más simple y deja el número del buscador como techo, no como promesa.
:::

## Comprueba que lo sabes

:::quiz
p: Buscas 100 configuraciones con validación cruzada y la ganadora da 0,80 mientras la mediana es 0,78. ¿Qué concluyes?
o: Que la ganadora es claramente mejor: le saca dos puntos a las demás
o: Que la diferencia es pequeña y hay que comprobarla en datos que la búsqueda no haya visto antes de decidir
o: Que AutoML ha fallado y hay que repetir la búsqueda con más configuraciones
a: 2
e: Con muchas configuraciones y pocas filas, una ventaja de 0,02 puede ser ruido del conjunto de validación. El máximo de N mediciones ruidosas siempre parece bueno. Se verifica en un conjunto externo; si la ventaja desaparece, elige el modelo más simple.
:::

:::quiz
p: ¿Cuál de estas decisiones NO puede tomar AutoML por ti?
o: Que imputación funciona mejor con tus datos
o: Que significa un falso positivo en tu negocio y qué métrica refleja eso
o: Que modelo rinde mejor en validación cruzada
a: 2
e: El buscador solo optimiza la métrica que le das: si esa métrica no refleja el problema, optimizará otra cosa. Elegir la métrica y el coste de cada error es criterio humano y no sale de los datos.
:::

:::trampa
Un buscador encuentra pipelines que rinden de maravilla en validación porque explotan
cualquier fuga que exista en tus datos: una variable calculada con información del futuro, un
identificador correlacionado con la etiqueta, una fila duplicada entre entrenamiento y prueba.
Para el buscador es señal, no error. Limpia y parte los datos antes de lanzarlo, nunca
después.
:::
