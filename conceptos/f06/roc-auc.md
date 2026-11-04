---
id: roc-auc
titulo: Curva ROC y AUC
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [matriz-de-confusion, metricas-de-clasificacion]
tags: [evaluacion, umbral, clasificacion, roc]
resumen: El rastro que deja un clasificador al mover su umbral y el área bajo esa curva, con el sesgo que esconde cuando el positivo es raro.
fuentes: ["Fawcett (2006), 'An introduction to ROC analysis'", "Provost, Fawcett y Kohavi (1998), 'The Case Against Accuracy Estimation for Comparing Induction Algorithms'"]
---

## En una frase

La curva ROC dibuja, para todos los umbrales posibles, qué proporción de positivos capturas
frente a qué proporción de negativos molestas; el AUC resume esa curva en un solo número: la
probabilidad de que un positivo elegido al azar puntúe más alto que un negativo elegido al azar.

## La idea

Casi ningún clasificador devuelve un «sí» o un «no»: devuelve una puntuación. El 0,83 de un
modelo de riesgo, los 12 puntos de un scoring de crédito, la distancia a la frontera de una
máquina de vectores. La decisión final la tomas tú cuando eliges un **umbral**: a partir de qué
puntuación actúas. Y ahí está el problema: cada umbral es un clasificador distinto, con su
propia precisión y su propia exhaustividad.

Podrías probar 20 umbrales y hacer 20 tablas de [[matriz-de-confusion]]. La curva ROC hace algo
más inteligente: recorre todos los umbrales de una vez y dibuja el compromiso. En el eje
vertical, la **tasa de verdaderos positivos** (TPR, que es la exhaustividad o sensibilidad): de
todos los positivos reales, cuántos capturas. En el horizontal, la **tasa de falsos positivos**
(FPR): de todos los negativos reales, a cuántos molestas. El punto ideal es la esquina superior
izquierda; la diagonal es el comportamiento de una moneda al aire.

Una forma de leer el AUC sin fórmulas: coge un positivo y un negativo al azar, mira sus
puntuaciones y apuesta a que el positivo tiene la puntuación más alta. El AUC es la probabilidad
de ganar esa apuesta. Un AUC de 0,8 significa que ganas 8 de cada 10 apuestas de ese tipo. No
significa «clasificas bien el 80 % de los casos»: eso es la exactitud, otra métrica distinta, y
esa confusión es la fuente de la mitad de los malentendidos.

El AUC tiene una virtud y un defecto que son el mismo hecho: **no depende de la prevalencia**.
Eso lo hace cómodo para comparar modelos entre poblaciones distintas, y a la vez peligrosísimo
cuando el positivo es raro, porque el FPR se mide sobre una masa enorme de negativos. Con
10.000 casos y un 1 % de positivos, un FPR del 5 % son 495 falsas alarmas contra 90 aciertos:
la curva está preciosa y la precisión real es del 15 %. Cuando lo positivo escasea, la curva
que hay que mirar es la de [[precision-recall-y-pr]].

## Definición formal

Sea `s(x)` la puntuación que el modelo asigna al caso `x` (más alta = más probable positivo), y
`τ` el umbral a partir del cual se decide «positivo»:

:::formula
TPR(τ) = VP(τ) / (VP(τ) + FN(τ))          FPR(τ) = FP(τ) / (FP(τ) + VN(τ))
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `s(x)` | Puntuación que el modelo da al caso `x`; más alta, más probable es que sea positivo | las de la puntuación | No mueve el AUC por sí sola: solo cuenta el orden entre casos, no el tamaño |
| `τ` | Umbral a partir del cual se decide «positivo» | las de la puntuación | La curva se va a la esquina de abajo a la izquierda, el origen: caen a la vez el TPR y el FPR |
| `TPR(τ)` | Positivos reales capturados o exhaustividad, la altura del punto en la curva | adimensional, entre 0 y 1 | Es lo que quieres alto; sube al bajar `τ`, a cambio de más falsas alarmas |
| `FPR(τ)` | Negativos reales molestados, `1 − especificidad`; la posición horizontal | adimensional, entre 0 y 1 | Es lo que quieres bajo; sube al bajar `τ` |
| `AUC` | Área bajo toda la curva: probabilidad de que un positivo al azar puntúe más alto que un negativo al azar | adimensional, entre 0 y 1 | Cuanto más alto, mejor ordena; 0,5 es ordenar al azar y no cambia con la prevalencia |
| `x⁺`, `x⁻` | Un positivo y un negativo elegidos al azar, independientes entre sí | — | No se «mueven»: son la definición probabilística del AUC |
| `π` | Prevalencia de la población donde aplicas el modelo | adimensional, entre 0 y 1 | El AUC se queda igual; la precisión del mismo umbral se hunde |
:::

- `TPR(τ)` — tasa de verdaderos positivos, o sensibilidad: fracción de positivos reales con
  `s(x) ≥ τ`. Es la altura de la curva.
- `FPR(τ)` — tasa de falsos positivos: fracción de negativos reales con `s(x) ≥ τ`. Es la
  posición horizontal. Equivale a `1 − Especificidad`.
- Al subir `τ` te vuelves más exigente: caen las dos tasas. Al bajarlo, suben las dos.
- La pareja `(FPR(τ), TPR(τ))` es un punto de la curva ROC; la curva entera es el conjunto de
  puntos que se obtiene al recorrer `τ` desde `+∞` hasta `−∞`.

:::formula
AUC = ∫₀¹ TPR d(FPR) = P(s(x⁺) > s(x⁻)) + ½ · P(s(x⁺) = s(x⁻))
:::

- `x⁺` y `x⁻` — un caso positivo y uno negativo elegidos al azar, de forma independiente.
- La segunda igualdad es la interpretación probabilística (estadístico U de Mann-Whitney).
  Los **empates** cuentan como medio acierto, pero solo cuando empatan un positivo y un
  negativo: si el orden separa las clases, el AUC sigue siendo 1 aunque el modelo use muy
  pocos valores distintos.
- `AUC = 0,5` es ordenar al azar. `AUC = 1` es separar perfectamente.
- El AUC es invariante a cualquier transformación **estrictamente creciente** de `s`: si
  multiplicas todas las puntuaciones por 3 o les aplicas un logaritmo, el AUC no cambia. Solo
  importa el orden, no los valores.

:::figura
fichero: roc-escalera-y-prevalencia
pie: A la izquierda, los ocho casos del ejemplo: al bajar el umbral la curva sube a escalones y el área que queda debajo es el AUC (0,80, o 12 de las 15 parejas). Fíjate en el tramo del umbral 0,85 al 0,60: capturas un positivo más sin molestar a ningún negativo nuevo, y ese regalo es justo lo que el AUC mide. A la derecha está lo que el AUC no mide: con el mismo punto de trabajo (90 % capturado, 5 % de negativos molestados) la precisión es 0,15 si el positivo es el 1 % de la población y 0,95 si es la mitad. Conclusión: usa el AUC para comparar modelos, pero decide con la precisión y el coste de tu población real.
fuente: figuras/roc-auc-1.py
:::

## Ejemplo

Ocho casos, tres positivos y cinco negativos, ordenados por la puntuación del modelo:

```
y     1     1     1     0     0     0     0     0
s  0,95  0,60  0,40  0,85  0,55  0,35  0,20  0,10
```

**AUC a mano.** Hay 3 · 5 = 15 parejas (positivo, negativo). Cuenta en cuántas gana el positivo:
el 0,95 gana a los cinco negativos; el 0,60 gana a 0,55, 0,35, 0,20 y 0,10 (cuatro, porque
pierde con 0,85); el 0,40 gana a 0,35, 0,20 y 0,10 (tres). Total: 5 + 4 + 3 = 12 de 15, y
`AUC = 12/15 = 0,8`.

**Recorrido de umbrales.** Mirando solo un par de puntos se ve el compromiso:

| Umbral | TPR | FPR | Lectura |
| --- | --- | --- | --- |
| 0,95 | 0,333 | 0,000 | Solo la apuesta más segura: ningún inocente molestado |
| 0,85 | 0,333 | 0,200 | Igual de exhaustivo, pero ya has molestado a un negativo |
| 0,60 | 0,667 | 0,200 | Capturas uno más sin coste adicional de FPR |
| 0,40 | 1,000 | 0,400 | Capturas los tres, a cambio de molestar a dos negativos |

Ese salto del umbral 0,85 al 0,60 no cuesta nada: el punto (0,2 · 0,333) y el (0,2 · 0,667)
tienen el mismo FPR. La curva ROC es, en el fondo, un catálogo de esos intercambios.

**Dónde falla.** Con 100 positivos y 9.900 negativos, un modelo con `AUC = 0,92` que trabaja en
un punto con `TPR = 0,90` y `FPR = 0,05` produce 90 aciertos y 495 falsas alarmas. La precisión
es `90 / 585 = 0,1538`: menos de una de cada seis alertas es real. El AUC no engaña, pero
tampoco te cuenta eso.

## Código

```python verificable
import numpy as np
from sklearn.metrics import roc_auc_score

# Ocho casos: y = 1 si era el caso que buscamos, score = puntuacion del modelo
y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
score = np.array([0.95, 0.60, 0.40, 0.85, 0.55, 0.35, 0.20, 0.10])

# AUC a mano: fraccion de parejas (positivo, negativo) en las que gana el positivo
# score[y == 1] no es un bucle: la comparacion produce una mascara de True y False y NumPy
# devuelve solo las puntuaciones marcadas con True (indexado booleano).
# La doble comprension es el producto cartesiano 3 x 5 = 15 parejas; cada p > n vale True o
# False y sum() los cuenta como 1 y 0, sin construir ninguna lista.
mejores = sum(p > n for p in score[y == 1] for n in score[y == 0])
# (y == 1).sum() cuenta los True: en una suma, True vale 1 y False vale 0.
parejas = (y == 1).sum() * (y == 0).sum()

print(f"parejas ganadas {mejores} de {parejas}")     # -> parejas ganadas 12 de 15
print(f"AUC a mano  {mejores / parejas:.3f}")        # -> 0.800
print(f"AUC sklearn {roc_auc_score(y, score):.3f}")  # -> 0.800
```

:::claves
- `score[y == 1]` es **indexado booleano**, no un filtro de pandas: devuelve un `np.array` nuevo con las puntuaciones de los positivos. El array original no se toca.
- `(y == 1).sum()` funciona porque `True` vale 1 al sumar. Pero `y.sum()` y `(y == 1).sum()` coinciden solo si las etiquetas son 0 y 1: con etiquetas −1 y +1, `y.sum()` daría un número sin sentido.
- `roc_auc_score(y, score)` espera las **etiquetas primero y las puntuaciones después** (al revés que `roc_curve`, que devuelve tres arrays). Si le pasas las puntuaciones en el primer argumento y las etiquetas en el segundo no da error: da un AUC bajo y falso.
- El segundo bloque repite el cálculo con `pred = score >= tau`: `>=` y no `>` decide si el caso que está justo en el umbral entra o no, y ese empate puede mover un escalón entero de la curva.
- `((pred == 1) & (y == 1))` lleva paréntesis obligatorios y usa `&`: con arrays de NumPy, `and` lanza «the truth value of an array is ambiguous», y sin paréntesis `&` se evalúa antes que `==`.
- `np.r_[a, b]` pega dos arrays uno detrás de otro (como `np.concatenate`). Se escribe con corchetes porque `np.r_` es un objeto de indexado, no una función.
:::

```python verificable
import numpy as np

y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
score = np.array([0.95, 0.60, 0.40, 0.85, 0.55, 0.35, 0.20, 0.10])
# int(...) convierte los enteros de NumPy en enteros de Python: la division da lo mismo,
# pero evita que se cuelen tipos raros al imprimir o al guardar.
positivos, negativos = int((y == 1).sum()), int((y == 0).sum())

# Cada umbral es un clasificador distinto; la curva ROC es el rastro que dejan
for tau in (0.95, 0.85, 0.60, 0.40):
    pred = score >= tau
    # Los parentesis de cada comparacion son obligatorios: & se evalua antes que == y
    # pred == 1 & (y == 1) se calcularia al reves. Con arrays se usa &, nunca `and`.
    tpr = int(((pred == 1) & (y == 1)).sum()) / positivos
    fpr = int(((pred == 1) & (y == 0)).sum()) / negativos
    print(f"umbral {tau:.2f}  TPR {tpr:.3f}  FPR {fpr:.3f}")
# -> umbral 0.95  TPR 0.333  FPR 0.000
# -> umbral 0.85  TPR 0.333  FPR 0.200
# -> umbral 0.60  TPR 0.667  FPR 0.200
# -> umbral 0.40  TPR 1.000  FPR 0.400
```

```python verificable
import numpy as np
from sklearn.metrics import roc_auc_score

# 100 positivos entre 10.000 casos: la clase rara es el 1 %
# np.linspace(a, b, n) da n valores equiespaciados entre a y b: 90 + 10 = 100 positivos
# y 495 + 9405 = 9.900 negativos.
pos = np.r_[np.linspace(0.80, 0.99, 90), np.linspace(0.10, 0.60, 10)]
neg = np.r_[np.linspace(0.80, 0.99, 495), np.linspace(0.00, 0.79, 9405)]
y = np.r_[np.ones(100), np.zeros(9900)]
score = np.r_[pos, neg]

pred = score >= 0.80
vp = int(((pred == 1) & (y == 1)).sum())
fp = int(((pred == 1) & (y == 0)).sum())

print(f"AUC       {roc_auc_score(y, score):.3f}")  # -> 0.920
print(f"TPR       {vp / (y == 1).sum():.3f}")      # -> 0.900
print(f"FPR       {fp / (y == 0).sum():.3f}")      # -> 0.050
print(f"precision {vp / (vp + fp):.4f}")           # -> 0.1538
```

## Errores típicos

- **Leer el AUC como un porcentaje de aciertos.** Un AUC de 0,9 no quiere decir que aciertes el
  90 % de los casos. Con un 1 % de positivos, ese mismo modelo puede tener una precisión del
  15 %. El AUC es una probabilidad de ordenación, no una tasa de acierto.
- **Usar el AUC con clases muy desbalanceadas y desplegar por umbral.** El FPR se calcula sobre
  una masa enorme de negativos: un 5 % parece pequeño y son cientos de falsas alarmas. Si lo que
  importa es la calidad de tus alertas, usa [[precision-recall-y-pr]].
- **Elegir el umbral por el punto que maximiza la distancia a la diagonal.** Ese criterio
  (el índice de Youden) da el mismo peso a un falso positivo que a un falso negativo, lo cual
  casi nunca es cierto. El umbral se elige por coste: [[umbrales-y-coste]].
- **Comparar AUC entre conjuntos con prevalencias muy distintas.** El AUC aguanta el cambio de
  prevalencia mejor que la precisión, pero los modelos no: una parte de la diferencia de AUC
  entre dos poblaciones puede ser del terreno, no del modelo.
- **Ignorar la zona de la curva que usas.** Un AUC alto puede venir de separar bien toda la
  cola, mientras que tu operación vive en el 1 % de alertas mejor puntuado. Mira la curva en esa
  región (o el *lift* en el top k), no solo el área total.
- **Olvidar los empates.** Si tu modelo entrega puntuaciones discretas con muchas repeticiones,
  cada empate **entre un positivo y un negativo** cuenta como medio acierto, así que el AUC
  baja aunque el orden sea bueno.

:::practica
enunciado: Dos positivos puntúan 0,9 y 0,5; cuatro negativos, 0,7, 0,5, 0,3 y 0,1. Calcula el AUC contando parejas y las tasas TPR y FPR con umbral 0,6 y con umbral 0,4.
pista: Cada pareja que gana el positivo cuenta 1 y cada empate 0,5; el TPR divide por los positivos y el FPR por los negativos.
solucion: Hay 2 · 4 = 8 parejas. El 0,9 gana a las cuatro; el 0,5 gana a 0,3 y 0,1, empata con 0,5 y pierde con 0,7: suma 2,5. AUC = (4 + 2,5)/8 = 0,8125. Con umbral 0,6 solo pasan 0,9 y 0,7, así que TPR = 1/2 = 0,5 y FPR = 1/4 = 0,25. Con umbral 0,4 pasan cuatro casos: TPR = 2/2 = 1 y FPR = 2/4 = 0,5. Bajar el umbral captura el segundo positivo a cambio de doblar las falsas alarmas.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa exactamente un AUC de 0,8?
o: Que el modelo acierta el 80 % de las clasificaciones
o: Que al coger un positivo y un negativo al azar, el positivo puntúa más alto el 80 % de las veces
o: Que el 80 % de las alertas del modelo son correctas
a: 2
e: El AUC es el área bajo la curva ROC, y equivale a la probabilidad de ordenar bien una pareja aleatoria de un positivo y un negativo. La primera opción describe la exactitud y la tercera la precisión; ninguna de las dos se deduce del AUC.
:::

:::quiz
p: Un modelo tiene AUC 0,92 sobre 10.000 casos con un 1 % de positivos. En el umbral elegido captura el 90 % de los positivos con un 5 % de falsos positivos. ¿Por qué la precisión es solo 0,15?
o: Porque el AUC está mal calculado
o: Porque el 5 % de FPR sobre 9.900 negativos son 495 falsas alarmas frente a 90 aciertos
o: Porque la precisión y el AUC miden lo mismo y deberían coincidir
o: Porque el modelo solo acierta el 15 % de los casos
a: 2
e: El FPR se mide sobre los negativos, que son el 99 % de la muestra: un 5 % de 9.900 es una cifra enorme en términos absolutos. La precisión divide los aciertos entre todas las alertas (90 / 585) y por eso se desploma. Ni el AUC está mal ni la precisión es una tasa de acierto global.
:::

:::nota
El AUC es invariante a cualquier transformación creciente de las puntuaciones. Es una ventaja
(no tienes que calibrar nada para comparar dos modelos con AUC) y a la vez la razón de que el
AUC no sirva para decidir nada por sí solo: para decidir necesitas probabilidades, y eso es
[[calibracion]]. Y si un AUC sale por debajo de 0,5, antes de dar el modelo por malo comprueba
que no haya una etiqueta invertida en algún paso del pipeline.
:::
