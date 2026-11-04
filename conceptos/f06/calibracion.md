---
id: calibracion
titulo: Calibración de probabilidades
fase: 6
nivel: avanzado
rutas: [ds]
prerequisitos: [metricas-de-clasificacion, glm-y-logistica]
tags: [probabilidad, evaluacion, brier, incertidumbre]
resumen: Que un 0,7 sea de verdad un 70 por ciento: cómo se mide la calibración, cómo se arregla y por qué el AUC no la ve.
fuentes: ["Brier (1950), 'Verification of forecasts expressed in terms of probability'", "Niculescu-Mizil y Caruana (2005), 'Predicting good probabilities with supervised learning'", "Guo et al. (2017), 'On Calibration of Modern Neural Networks'"]
---

## En una frase

Un clasificador está calibrado cuando, de todos los casos a los que puso un 0,7, acierta
realmente el 70 %; la discriminación dice quién es más probable, la calibración dice cuánto.

## La idea

Dos modelos pueden ordenar a los clientes exactamente igual —mismo AUC, mismas posiciones en
la lista— y uno de ellos mentir en los números. El primero dice 0,9 para un impago y acierta
9 de cada 10 veces; el segundo dice 0,9 y acierta 6 de cada 10. Para decidir a quién llamas
primero dan igual. Para decidir **cuánto** vale cada caso, no.

Y casi todas las decisiones de negocio son de ese segundo tipo. Si conceder un crédito deja un
beneficio esperado de 200 € y una pérdida esperada de 2.000 €, la decisión correcta es conceder
cuando `p · 200 > (1 − p) · 2.000`, es decir, cuando `p < 0,909`. Esa cuenta solo funciona si
`p` es una probabilidad de verdad. Con un modelo que dice 0,9 cuando en realidad es 0,6, la
misma fórmula te hace firmar créditos que no deberías. Toda la maquinaria de decisión por coste
de [[umbrales-y-coste]] se apoya en este supuesto.

¿Por qué se descalibran los modelos? Cada familia tiene su vicio:

- Una máquina de vectores soporte no devuelve probabilidades: devuelve una distancia a la
  frontera. Convertirla en probabilidad con un sigmoide mal ajustado da números con sentido del
  orden y sin sentido de la escala.
- Naive Bayes multiplica probabilidades como si las variables fueran independientes. Cuando no
  lo son, el producto se dispara hacia 0 y hacia 1: es el modelo con **exceso de confianza**
  clásico.
- Un árbol de decisión con hojas puras devuelve 0 y 1 exactos, y 0 y 1 nunca son ciertos.
- Un bosque aleatorio promedio de votos tiende a quedarse corto: dice 0,6 cuando la frecuencia
  real es 0,8, porque el promedio tira hacia el centro.
- Las redes neuronales modernas, entrenadas mucho y con regularización, suelen ser
  **demasiado confiadas** en la zona alta ([[sobreajuste-en-redes]]).

Diagnosticarlo es fácil y visual: se agrupan las predicciones en tramos, se calcula la
probabilidad media que dijo el modelo y la frecuencia real de positivos en cada tramo, y se
dibuja. Es el **diagrama de fiabilidad**. Si el modelo está calibrado, los puntos caen sobre la
diagonal. Arreglarlo es también fácil, pero tiene una regla que no se puede saltar: **la
corrección se ajusta sobre datos que el modelo no ha visto** (un conjunto de calibración, o el
de validación). Ajustarla sobre el entrenamiento produce una curva que encaja perfectamente y
no corrige nada.

:::figura
fichero: calibracion-fiabilidad-y-brier
pie: A la izquierda, el diagrama de fiabilidad de los cinco tramos del ejemplo: cada punto es un tramo, su tamaño es el número de casos y la diagonal es la calibración perfecta. Los cuatro tramos bajos van casi pegados a la diagonal, pero el de arriba promete 0,88 y cumple 0,74, y ahí está casi todo el error. A la derecha, dos modelos que ordenan igual (mismo AUC, 0,816): elevar al cuadrado conserva el orden y rompe la escala, así que el Brier sube de 0,175 a 0,210. Conclusión: mira el diagrama por tramos y no el promedio; un ECE global pequeño puede esconder todo el desvío justo en la zona donde decides.
fuente: figuras/calibracion-1.py
:::

## Definición formal

Sea `p̂ᵢ` la probabilidad que el modelo asigna al caso `i` y `yᵢ ∈ {0, 1}` su etiqueta real.
Calibración perfecta significa:

:::formula
P(y = 1 | p̂ = p) = p    para todo p en [0, 1]
:::

- Es una afirmación sobre **grupos**, no sobre individuos: de todos los casos con `p̂ = 0,7`,
  el 70 % serán positivos. Nunca podrás comprobar que un caso concreto «tenía» un 70 %.
- `p̂ = 0,7` con un 60 % real es **exceso de confianza** (overconfident); con un 85 % real es
  **defecto de confianza**.

**Puntuación de Brier.** Es el error cuadrático medio de las probabilidades, y es una regla
estrictamente propia (premia decir la verdad, no solo acertar):

:::formula
Brier = (1/N) · Σᵢ (p̂ᵢ − yᵢ)²
:::

- `N` — número de casos. El Brier está en `[0, 1]`: 0 es perfecto, 0,25 es lo que saca un modelo
  que siempre dice 0,5 con la mitad de positivos.
- Se descompone en `Brier = fiabilidad − resolución + incertidumbre`. La **fiabilidad** mide el
  error de calibración; la **resolución** premia separar los grupos en zonas extremas; la
  **incertidumbre** es la varianza de la etiqueta y no depende del modelo.

**Error de calibración esperado (ECE).** Divide el rango en `B` tramos (típicamente 10) y
compara, en cada uno, la confianza media con la frecuencia observada:

:::formula
ECE = Σ_b (n_b / N) · |frecuencia(b) − confianza(b)|
:::

- `n_b` — número de casos en el tramo `b`; `N`, el total.
- Un ECE de 0,05 significa que, en promedio, las probabilidades están 5 puntos porcentuales
  desviadas. Cuidado con los tramos de pocos casos: su frecuencia observada es muy ruidosa.

**Las dos correcciones habituales.** Platt ajusta un sigmoide sobre la puntuación `s` del
modelo, con dos parámetros `A` y `B` estimados por máxima verosimilitud sobre el conjunto de
calibración:

:::formula
p̂ = 1 / (1 + exp(A · s + B))
:::

Es paramétrica, suave y funciona con pocos cientos de casos. No arregla una curva de
calibración con forma rara, porque solo puede estirar y desplazar el sigmoide.

La **regresión isotónica** ajusta una función escalonada no decreciente que minimiza el error
cuadrático bajo esa restricción de monotonía. Es mucho más flexible, pero necesita bastantes más
datos —y cuantos más positivos reales haya, mejor— porque cada escalón se estima con las
observaciones que caen en él; con pocos casos tiende a producir escalones planos en los
extremos, con probabilidades exactamente 0 o 1. Para redes neuronales hay una tercera vía,
la **escalación por temperatura**: dividir los *logits* entre un único parámetro `T > 0`
ajustado sobre validación.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p̂ᵢ` | La probabilidad que el modelo asigna al caso `i` | adimensional, entre 0 y 1 | No cambia nada por sí sola: la calibración compara el conjunto de los casos con ese mismo valor |
| `yᵢ` | La etiqueta real del caso `i` | 0 o 1 | Es el dato, no un parámetro: cambiarlo cambia el Brier y el ECE |
| `N` | Número de casos evaluados | casos | Estabiliza las estimaciones: con pocos casos el ECE y el Brier son muy ruidosos |
| `Brier` | Error cuadrático medio de las probabilidades, `(1/N) · Σ (p̂ᵢ − yᵢ)²` | adimensional, entre 0 y 1 | Cuanto más alto, peor: castiga decir 0,9 cuando la frecuencia real es 0,6 |
| `ECE` | Error de calibración esperado: media de los desvíos por tramo, ponderada por casos | adimensional, entre 0 y 1 | Cuanto más alto, más mienten las probabilidades de media; 0,05 son cinco puntos porcentuales |
| `B` | Número de tramos en que se parte el rango de `p̂` para el ECE | tramos | Con muchos tramos cada uno tiene pocos casos y la frecuencia observada es ruidosa; con pocos, el desvío se diluye |
| `n_b` | Casos que caen en el tramo `b` | casos | Pesa ese tramo en el ECE; un tramo con 5 casos apenas cuenta |
| `A`, `B` | Los dos parámetros del sigmoide de Platt, ajustados por máxima verosimilitud | adimensionales | `A` estira o encoge la curva (y con ella la confianza); `B` la desplaza hacia arriba o hacia abajo |
| `T` | Temperatura: divide los *logits* antes de pasarlos por la sigmoide | positiva, adimensional | Por encima de 1 suaviza las probabilidades (menos confianza); por debajo, las agudiza |
:::

## Ejemplo

Un modelo de impago sobre 1.000 clientes, agrupado en cinco tramos:

| Tramo de p̂ | Casos | Confianza media | Frecuencia observada | Desvío |
| --- | --- | --- | --- | --- |
| 0,0 a 0,2 | 300 | 0,12 | 0,10 | 0,02 |
| 0,2 a 0,4 | 250 | 0,31 | 0,28 | 0,03 |
| 0,4 a 0,6 | 200 | 0,52 | 0,55 | 0,03 |
| 0,6 a 0,8 | 150 | 0,71 | 0,62 | 0,09 |
| 0,8 a 1,0 | 100 | 0,88 | 0,74 | 0,14 |

El ECE es la media de los desvíos ponderada por el tamaño del tramo:

```
ECE = (300·0,02 + 250·0,03 + 200·0,03 + 150·0,09 + 100·0,14) / 1.000
    = (6 + 7,5 + 6 + 13,5 + 14) / 1.000 = 47 / 1.000 = 0,047
```

Un ECE de 4,7 puntos. Y el detalle importante: en los tramos bajos el modelo está casi bien,
mientras que en el tramo 0,8 a 1,0 promete 0,88 y cumple 0,74. Si tu decisión vive en ese
tramo (por ejemplo, solo actúas a partir de 0,8), ese desvío de 14 puntos es el único que te
importa, y el ECE global de 0,047 lo diluye entre 900 casos que no te afectan.

**Brier de un caso diminuto.** Con `p̂ = [0,9, 0,7, 0,3, 0,2, 0,6]` e `y = [1, 1, 0, 0, 1]`:

```
Brier = ((0,9-1)² + (0,7-1)² + (0,3-0)² + (0,2-0)² + (0,6-1)²) / 5
      = (0,01 + 0,09 + 0,09 + 0,04 + 0,16) / 5 = 0,39 / 5 = 0,078
```

## Código

```python verificable
import numpy as np

# Los cinco tramos de la tabla del ejemplo: el clasico exceso de confianza arriba
confianza = np.array([0.12, 0.31, 0.52, 0.71, 0.88])
casos = np.array([300, 250, 200, 150, 100])
observada = np.array([0.10, 0.28, 0.55, 0.62, 0.74])

# ECE: media de los desvios ponderada por el tamano de cada tramo
# casos / casos.sum() divide elemento a elemento: cada tramo se lleva su peso y los cinco
# pesos suman 1. No hace falta ningun bucle.
desvios = np.abs(observada - confianza)
ece = float((casos / casos.sum() * desvios).sum())
# np.round devuelve otro array; .tolist() lo convierte en lista de Python para que se
# imprima como [0.02, 0.03, ...] y no como array([0.02, 0.03, ...]).
print("desvios por tramo", np.round(desvios, 2).tolist())  # -> [0.02, 0.03, 0.03, 0.09, 0.14]
print(f"ECE {ece:.4f}")                                    # -> 0.0470
```

:::claves
- `casos / casos.sum() * desvios` es aritmética **elemento a elemento**, sin bucles: la división reparte los pesos y la multiplicación los aplica tramo a tramo. El `.sum()` final es lo que convierte los cinco números en el ECE.
- `float(...)` al final no es decoración: `(array).sum()` devuelve un escalar de NumPy, que se imprime como `np.float64(0.047)` en las versiones nuevas. `float()` lo deja en un número normal.
- `np.round(desvios, 2)` redondea solo para imprimir; el ECE se calcula con los desvíos sin redondear. Si redondeas antes, el resultado sale con otro último decimal.
- `np.abs` es el valor absoluto elemento a elemento, no la función `abs` de Python: `abs(array)` funciona por casualidad para un array de una dimensión, pero `np.abs` es lo correcto y lo que funciona con cualquier forma.
- `np.repeat(valores, 100)` del segundo bloque repite cada valor 100 veces: construye 1.900 casos con la probabilidad exacta que se quiere comprobar. `p ** 2` es una transformación creciente, así que el orden no cambia (el AUC se queda igual) y la escala sí (el Brier empeora).
- `p_base = base.predict_proba(X_te)[:, 1]` toma la **segunda columna**, la de la clase positiva. `predict_proba` devuelve una columna por clase y en orden alfabético: si algún día las clases son texto, comprueba `base.classes_` antes de cortar por la columna 1.
:::

```python verificable
import numpy as np
from sklearn.metrics import brier_score_loss, roc_auc_score

# Probabilidades calibradas por construccion: de cada 100 casos con p = 0,30
# exactamente 30 son positivos.
valores = np.arange(5, 100, 5) / 100.0        # 0,05 ... 0,95
# np.repeat repite CADA valor 100 veces (1.900 casos); np.tile repetiria la lista entera.
p = np.repeat(valores, 100)
# La comprension construye 19 bloques de 100 etiquetas: los `int(v * 100)` primeros son 1
# y el resto 0, asi que la frecuencia real coincide con la probabilidad declarada.
y = np.concatenate([np.r_[np.ones(int(v * 100)), np.zeros(100 - int(v * 100))]
                    for v in valores])

# Una transformacion creciente (elevar al cuadrado) conserva el orden y rompe la escala
distorsionada = p ** 2

print(f"casos {p.size}  prevalencia {y.mean():.2f}")            # -> casos 1900  prevalencia 0.50
print(f"AUC   original {roc_auc_score(y, p):.3f}")             # -> 0.816
print(f"AUC   distorsionada {roc_auc_score(y, distorsionada):.3f}")  # -> 0.816
print(f"Brier original {brier_score_loss(y, p):.4f}")          # -> 0.1750
print(f"Brier distorsionada {brier_score_loss(y, distorsionada):.4f}")  # -> 0.2101
```

```python verificable
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Un arbol sin limite de profundidad deja hojas puras: solo sabe decir 0 y 1.
# flip_y=0.1 cambia el 10 % de las etiquetas a proposito: sin ese ruido el problema seria
# demasiado facil y el arbol acertaria sin despeinarse.
X, y = make_classification(n_samples=2000, n_features=10, n_informative=4,
                           n_redundant=2, flip_y=0.1, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

def brier(p, yv):
    # Media de los cuadrados: (p - yv) ** 2 se calcula elemento a elemento.
    return float(((p - yv) ** 2).mean())

base = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
# cv=5 no es «cinco modelos distintos»: CalibratedClassifierCV parte X_tr en cinco pliegues,
# entrena un arbol con cuatro y ajusta el calibrador con el que dejo fuera. Asi el calibrador
# nunca ve los datos con los que se entreno su arbol.
# El DecisionTreeClassifier se pasa SIN entrenar: la clase lo clona por dentro en cada pliegue.
calibrado = CalibratedClassifierCV(
    DecisionTreeClassifier(random_state=0), method="isotonic", cv=5
).fit(X_tr, y_tr)

# predict_proba devuelve una columna por clase, en el orden de `classes_`; la 1 es la positiva.
p_base = base.predict_proba(X_te)[:, 1]
p_cal = calibrado.predict_proba(X_te)[:, 1]

print(f"Brier sin calibrar {brier(p_base, y_te):.4f}")   # -> 0.2437
print(f"Brier calibrado    {brier(p_cal, y_te):.4f}")    # -> 0.1599
# (a == 0) | (a == 1) es la mascara de las probabilidades extremas y .mean() da su
# proporcion. El formato :.0% multiplica por 100 y anade el simbolo por su cuenta.
print(f"extremos 0 o 1     {((p_base == 0) | (p_base == 1)).mean():.0%}")  # -> 100%
print(f"confianza media    {p_base.mean():.3f}  frecuencia real {y_te.mean():.3f}")
```

## Errores típicos

- **Creer que discriminación y calibración son lo mismo.** El AUC solo mira el orden de las
  puntuaciones: es ciego a la calibración por construcción. Un modelo con AUC 0,95 puede estar
  diciendo 0,9 donde la realidad es 0,6; y al revés, un Brier bajo puede venir solo de acercar
  todas las probabilidades a la prevalencia, sin discriminar mejor. Mira las dos cosas.
- **Calibrar con el conjunto de entrenamiento.** El modelo ya está ajustado a esos datos, así
  que sus probabilidades salen demasiado afiladas y la corrección aprende ese afilado, no el
  error real. Se calibra sobre validación o con validación cruzada interna.
- **Usar isotónica con pocos datos.** Con unos cientos de casos produce escalones que copian el
  ruido de las muestras y devuelve 0 y 1 exactos en los extremos. Con pocos datos, Platt.
- **Mirar solo la media de la probabilidad predicha frente a la tasa real.** Dos errores que se
  compensan (sobreconfianza en un tramo, infraconfianza en otro) dan medias iguales y un
  diagrama destrozado. Mira el diagrama por tramos, no el promedio.
- **Corregir la calibración y no volver a comprobarla.** Cambiar de modelo, de variables o de
  población invalida el calibrador. Si reentrenas el modelo, recalibra.
- **Interpretar un 0,7 en un caso concreto como «este cliente tiene un 70 % de probabilidad».**
  La frecuencia es una propiedad de la cohorte. Nadie es «un 0,7»: es una forma de hablar.

:::practica
enunciado: En el tramo 0,6 a 0,8 hay 200 casos con confianza media 0,72 y 130 positivos; en el tramo 0,8 a 1,0, 50 casos con confianza 0,90 y 35 positivos. Calcula el ECE y decide si sirve para decidir por coste.
pista: El ECE pondera el desvío de cada tramo por su número de casos sobre el total de 250.
solucion: Frecuencias observadas: 130/200 = 0,65 y 35/50 = 0,70; desvíos 0,72 − 0,65 = 0,07 y 0,90 − 0,70 = 0,20. ECE = (200 · 0,07 + 50 · 0,20)/250 = (14 + 10)/250 = 0,096, casi diez puntos. El error vive en el tramo alto: si actúas por encima de 0,8 crees acertar el 90 % y aciertas el 70 %. Sin calibrar sobre validación no puedes multiplicar probabilidad por coste.
:::

## Comprueba que lo sabes

:::quiz
p: Dos modelos ordenan a los mismos clientes igual (mismo AUC) pero uno tiene Brier 0,15 y el otro 0,25. ¿Qué conclusión es correcta?
o: El de Brier 0,15 da mejores probabilidades y por eso sirve mejor para decidir por coste esperado
o: El de Brier 0,25 es mejor porque un Brier más alto indica más información
o: Los dos son equivalentes, porque ordenan igual
a: 1
e: El Brier es una regla propia: castiga decir 0,9 cuando la frecuencia real es 0,6. Con el mismo orden, el que tiene menos Brier está mejor calibrado y es el único de los dos que permite multiplicar probabilidad por coste y decidir.
:::

:::quiz
p: ¿Por qué la corrección de Platt o la isotónica no se ajustan sobre el conjunto de entrenamiento?
o: Porque el entrenamiento es demasiado grande para esos métodos
o: Porque el modelo ya está ajustado a esos datos y sus probabilidades allí son artificialmente afiladas
o: Porque Platt necesita que las etiquetas estén balanceadas
a: 2
e: Sobre entrenamiento el modelo tiende a parecer más seguro de lo que es, y el calibrador aprende ese vicio en lugar del error real. Sobre validación, la corrección mide el desvío que el modelo tendrá en datos nuevos.
:::

:::quiz
p: Un modelo dice 0,9 en 100 casos y en esos 100 acierta 74. ¿Qué está pasando y qué extremo de la tabla importa?
o: Está bien calibrado, la diferencia de 16 puntos es ruido
o: Tiene exceso de confianza y el desvío está concentrado en el tramo alto, que es justo donde suele decidir el umbral
o: Tiene defecto de confianza y debería subir sus probabilidades
a: 2
e: Promete 0,9 y cumple 0,74: sobreestima. El ECE global puede parecer pequeño si los tramos bajos están bien, pero el error vive en la zona alta, que es donde se eligen los umbrales de actuación.
:::

:::nota
La calibración no mejora la capacidad de discriminar: es una transformación monótona de las
puntuaciones, así que el AUC y todas las métricas de orden se quedan igual. Ganas la
interpretación y la posibilidad de decidir por valor esperado.
:::
