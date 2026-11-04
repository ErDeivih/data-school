---
id: desbalanceo-de-clases
titulo: Desbalanceo de clases
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [metricas-de-clasificacion, matriz-de-confusion, precision-recall-y-pr]
tags: [clasificacion, metricas, remuestreo]
resumen: Cuando el 1 % de los casos son positivos, el accuracy engaña; lo que hay que ajustar es la métrica, el peso de las clases y el umbral de decisión.
fuentes: ["Chawla et al. (2002), 'SMOTE: Synthetic Minority Over-sampling Technique'", "King y Zeng (2001), 'Logistic Regression in Rare Events Data'"]
---

## En una frase

Con clases muy desequilibradas, un modelo que diga siempre «no» acierta el 99 % de las veces y
es inútil: lo que importa no es cuántas aciertas, sino cuántos positivos encuentras y a qué
precio en falsas alarmas.

## La idea

Piensa en la alarma de incendios de un edificio. Si la ajustas para que no suene nunca, tendrás
cero falsas alarmas y un edificio quemado. Si la ajustas para que suene con cualquier olor a
humo, detectarás todos los fuegos y también todas las tostadas. Ninguna de las dos es «la
correcta»: la elección depende de cuánto te cuesta un incendio no detectado frente a cuánto te
cuesta una evacuación innecesaria.

El desbalanceo de clases es exactamente eso, y el error habitual es tratarlo como un problema de
datos cuando casi siempre es un problema de **métrica y de umbral**. Tres escenarios reales
donde aparece: fraude (menos del 1 % de las transacciones), abandono de clientes (unos pocos
puntos), y en finanzas, un movimiento grande del precio en la próxima hora.

El daño empieza por la métrica. Con un 1 % de positivos, el **accuracy** (proporción de
aciertos) es inútil: predecir siempre la clase mayoritaria da 0,99. Hay que pasar a métricas que
miren la clase minoritaria: [[precision-recall-y-pr|precisión y exhaustividad]] con su curva PR,
[[roc-auc|el AUC]] como resumen del orden, o directamente el coste esperado si conoces el precio
de cada error.

El segundo daño es el entrenamiento. La mayoría de los algoritmos minimizan una suma de errores
sobre todas las filas. Con 1.000.000 de negativos y 10.000 positivos, cada fila pesa lo mismo:
acertar 10.000 negativos más baja la pérdida exactamente igual que acertar los 10.000 positivos,
así que el modelo aprende a ignorar la clase rara porque por ahí ya baja la pérdida. Las
soluciones se agrupan en tres familias:

1. **Pesos.** Multiplicar el error de la clase rara por un factor. Es la opción más limpia: no
   tocas los datos, solo la función de pérdida. `class_weight="balanced"` reparte el peso
   inversamente a la frecuencia.
2. **Remuestreo.** Duplicar positivos (sobremuestreo), tirar negativos (submuestreo) o generar
   positivos sintéticos interpolando entre vecinos (SMOTE). Funcionan, pero submuestrear tira
   información y el sobremuestreo ingenuo favorece el sobreajuste por repetición.
3. **Umbral.** Dejar el modelo probabilístico tranquilo y mover el punto de corte. Es la palanca
   más barata y la que casi nadie usa.

:::figura
fichero: desbalanceo-accuracy-y-umbral
pie: A la izquierda, el modelo que predice siempre «no» sobre 10.000 casos con 100 fraudes: acierta 9.900 y no señala ni uno, así que su accuracy es 0,9900 y su exhaustividad 0,0000. El 99 % de acierto es exactamente lo que da no hacer nada, y por eso el accuracy no sirve como criterio con clases raras. A la derecha, el mismo modelo sobre 100 casos con 20 positivos y tres umbrales: con 0,9 señala 2 y acierta los dos (precisión 1,00, exhaustividad 0,10); con 0,5 señala 24, encuentra 10 (precisión 0,42); con 0,1 señala 85 y encuentra 18 de los 20 (exhaustividad 0,90, precisión 0,21). Pasar de 0,5 a 0,1 recupera 8 fraudes a cambio de 53 falsas alarmas más: la decisión es de coste, no de estadística.
fuente: figuras/desbalanceo-de-clases-1.py
:::

## Definición formal

Sea `π = P(y = 1)` la prevalencia de la clase positiva. En un problema sano `π` ronda 0,5; aquí
hablamos de valores como 0,001 o 0,01.

Con `TP`, `FP`, `FN` y `TN` las cuatro casillas de la
[[matriz-de-confusion|matriz de confusión]]:

- **Exhaustividad (recall):** `TP / (TP + FN)`. De todos los positivos reales, cuántos pillo.
- **Precisión:** `TP / (TP + FP)`. De todos los que señalo, cuántos lo son de verdad.
- **F1:** media armónica de ambas, `2 · P · R / (P + R)`. Solo tiene sentido si las dos importan
  por igual, cosa que rara vez ocurre.
- **Acierto (accuracy):** `(TP + TN) / n`. Con `π` pequeño, predecir siempre 0 da `1 − π`.

:::formula
peso de la clase c:  w(c) = n / (2 · n(c))   ·   decisión:  ŷ = 1 si p ≥ t
:::

En la primera fórmula `n` es el número total de filas y `n(c)` las de la clase `c`; con dos
clases, esto es lo que hace `class_weight="balanced"`. En la segunda, `p` es la probabilidad
estimada y `t` el umbral, que por defecto es 0,5 pero **no tiene por qué serlo**. Elegir `t` es
un problema de decisión, no de estadística: si un falso negativo cuesta 10 veces más que un
falso positivo, el umbral óptimo baja, no sube.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `π` | Prevalencia de la clase positiva: `P(y = 1)` | tanto por uno, 0 a 1 | Cuanto más baja, más engaña el accuracy: predecir siempre 0 da `1 − π`, que con 0,01 es 0,99. Por debajo de 0,1 hay que cambiar de métrica |
| `n` | Número total de filas | filas | No cambia el reparto, pero con pocas filas de la clase rara las métricas de esa clase son muy inestables |
| `n(c)` | Filas de la clase `c` | filas | Es el denominador del peso: cuanto más rara es la clase, más peso recibe cada uno de sus errores |
| `w(c)` | Peso de la clase `c`: `n / (2 · n(c))` | adimensional | Con 9.900 y 100, cada fila positiva pesa 50 y cada negativa 0,51: casi cien veces más por fila. Es `class_weight="balanced"`: no toca los datos, solo la pérdida |
| `p` | Probabilidad estimada de la clase positiva | tanto por uno, 0 a 1 | Es la salida del modelo. Con `π = 0,01`, un `p = 0,3` puede ser una señal fortísima (30 veces la tasa base), así que no lo interpretes como probabilidad real sin calibrar |
| `t` | Umbral de decisión: se predice 1 si `p ≥ t` | tanto por uno, 0 a 1 | Bajarlo sube la exhaustividad y baja la precisión. Con `t = 0,1` y 100 casos con 20 positivos se señalan 85 y se pillan 18 de los 20; el óptimo se calcula con el coste de cada error, no con la intuición |
| `TP`, `FP`, `FN`, `TN` | Las cuatro casillas de la matriz de confusión | casos | Son las piezas de todas las métricas: `TP / (TP + FN)` es la exhaustividad y `TP / (TP + FP)` la precisión. Con números absolutos se ve el desbalanceo; con proporciones, no |
| `(TP + TN) / n` | El accuracy o acierto | tanto por uno, 0 a 1 | Es la métrica que engaña: solo cuenta aciertos totales, así que sube cuando el modelo ignora la clase rara. Con `π` bajo, no la uses como criterio |
:::

## Ejemplo

**El engaño del accuracy.** 10.000 casos, 100 positivos (π = 1 %). Un modelo que predice siempre
«no»:

- Acierto: 9.900 / 10.000 = **0,9900**.
- Exhaustividad: 0 / 100 = **0,0000**.
- Precisión: 0 / 0, indefinida; con `zero_division=0` se reporta **0,0000**.

Un 99 % de acierto y cero capacidad de detección. Cualquier informe que solo publique el
accuracy está ocultando esto.

**El efecto de los pesos.** 4.000 filas sintéticas con unas 200 positivas (5 %), divididas en
entrenamiento y prueba con estratificación. Una regresión logística sin pesos encuentra el
**18 %** de los positivos en la prueba; la misma con `class_weight="balanced"` encuentra el
**68 %**. Ninguna variable ha cambiado, ni una fila añadida: solo ha cambiado cuánto duele
equivocarse en la clase rara.

**El umbral.** 100 casos con 20 positivos y puntuaciones que se solapan:

- Umbral 0,9: 2 positivos señalados, exhaustividad **0,10**, precisión **1,00**.
- Umbral 0,5: 24 señalados, exhaustividad **0,50**, precisión **0,42**.
- Umbral 0,1: 85 señalados, exhaustividad **0,90**, precisión **0,21**.

Los tres modelos son el mismo. Lo único que cambia es dónde pones el listón, y ese listón se
elige con el coste de cada error sobre la mesa.

## Código

```python verificable
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 10.000 casos con un 1 % de positivos: el modelo "todo negativo" triunfa en accuracy.
y = np.zeros(10000, dtype=int)
y[:100] = 1
pred = np.zeros(10000, dtype=int)   # prediccion perezosa: nunca senala un positivo

print(f"accuracy  {accuracy_score(y, pred):.4f}")   # -> 0.9900
print(f"recall    {recall_score(y, pred):.4f}")     # -> 0.0000
print(f"precision {precision_score(y, pred, zero_division=0):.4f}")  # -> 0.0000
```

:::claves
- `precision_score` con un modelo que no señala nada da una división `0 / 0`. Sin `zero_division=0` scikit-learn lanza un aviso y devuelve 0,0 igualmente, pero el aviso es fácil de perder entre cientos de líneas de un informe. Ponlo explícito y decide qué quieres que salga: 0,0, 1,0 o un error.
- `y[:100] = 1` modifica el array **en el sitio**: es una asignación sobre una porción, no una función. Después de esa línea, `y` ya tiene 100 unos y 9.900 ceros, y no hay ningún array nuevo. Lo contrario ocurre con `pred = np.zeros(10000, dtype=int)`, que sí crea uno. La regla práctica: si la línea empieza por el nombre del array y un corchete, modifica; si empieza por `np.` o por el nombre de otro array, crea. Comprueba con `y is y[:100]` (devuelve `False` aunque el segundo sea una vista del primero: la vista es un objeto distinto que comparte los datos).
- `np.zeros(10000, dtype=int)` crea enteros. Si quitas el `dtype`, serían `float64` y las tres métricas seguirían dando lo mismo, porque `1.0 == 1` es verdadero. Pero no mezcles tipos por accidente: `precision_score` cuenta `TP` comparando etiqueta con predicción, y con etiquetas de texto (`"fraude"` / `"no fraude"`) necesitas declarar `pos_label` para que sepa cuál es la clase positiva. En un problema con clases 0/1 la positiva es 1 por defecto; con textos, no hay defecto.
- Las tres métricas se calculan sobre los mismos dos arrays y solo se diferencian en la fórmula. `accuracy_score` mira las cuatro casillas, `recall_score` solo mira la fila de los positivos reales y `precision_score` solo la columna de los señalados. Por eso el mismo modelo da 0,99 en una y 0,00 en las otras dos.
- `pred = np.zeros(10000, dtype=int)` no es un «modelo tonto» de juguete: es exactamente lo que hace cualquier clasificador mal calibrado cuando la clase rara es tan rara que el umbral 0,5 nunca se alcanza. Antes de culpar al modelo, mira cuántos positivos predice: si son cero, el problema es el umbral.
- Los tres `print` usan f-strings con `:.4f`, que **redondea solo el texto**. `accuracy_score` devuelve 0.99 exacto (9.900/10.000); si la proporción fuera 2/3, el f-string mostraría 0,6667 y el valor guardado seguiría siendo 0,6666666. No compares cifras formateadas entre modelos: compara los números.
:::

```python verificable
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split

# Dos nubes de puntos solapadas: la clase rara son 200 filas de 4.000.
rng = np.random.default_rng(0)
n_may, n_min = 3800, 200
X = np.vstack([rng.normal(0.0, 1.0, (n_may, 2)), rng.normal(1.2, 1.0, (n_min, 2))])
y = np.array([0] * n_may + [1] * n_min)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
sin_peso = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
con_peso = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_tr, y_tr)

print(f"positivos en prueba {int(y_te.sum())} de {y_te.size}")   # -> 60 de 1200
print(f"recall sin pesos                 {recall_score(y_te, sin_peso.predict(X_te)):.2f}")   # -> 0.18
print(f"recall con class_weight balanced {recall_score(y_te, con_peso.predict(X_te)):.2f}")   # -> 0.68
```

```python verificable
import numpy as np
from sklearn.metrics import precision_score, recall_score

# 100 casos: 20 positivos (los primeros) y 80 negativos, con puntuaciones que se solapan.
y = np.array([1] * 20 + [0] * 80)
p = np.concatenate([np.linspace(0.95, 0.05, 20), np.linspace(0.6, 0.01, 80)])

# El umbral 0.5 no es sagrado: moverlo reparte de otra forma recall y precision.
for t in (0.9, 0.5, 0.1):
    pred = (p >= t).astype(int)
    print(f"umbral {t:.1f}  positivos {int(pred.sum()):>3}  "
          f"recall {recall_score(y, pred):.2f}  precision {precision_score(y, pred, zero_division=0):.2f}")
# -> umbral 0.9  positivos   2  recall 0.10  precision 1.00
# -> umbral 0.5  positivos  24  recall 0.50  precision 0.42
# -> umbral 0.1  positivos  85  recall 0.90  precision 0.21
```

## Errores típicos

- **Evaluar con accuracy.** Con `π = 1 %`, el 0,99 lo consigue un modelo que no hace nada. Usa
  exhaustividad, precisión, la curva PR y el AUC, o directamente la matriz de confusión con
  números absolutos.
- **Remuestrear antes de dividir en entrenamiento y prueba.** Si duplicas positivos y luego
  divides, la misma fila puede acabar en entrenamiento y en prueba: la puntuación se infla. El
  remuestreo se aplica **solo** al conjunto de entrenamiento.
- **Sobremuestrear duplicando sin control.** Copiar la misma fila 100 veces hace que el modelo
  la memorice. Si sobremuestreas, hazlo con datos sintéticos (SMOTE interpola entre vecinos) o,
  mejor, usa pesos, que logran el mismo efecto sin tocar las filas.
- **Submuestrear y no corregir la probabilidad.** Si entrenas con una prevalencia artificial del
  50 %, las probabilidades que salen ya no son probabilidades reales: hay que reescalarlas antes
  de interpretarlas o de calcular un beneficio esperado.
- **Quedarse con el umbral 0,5 por defecto.** Es el error más caro y el más fácil de arreglar.
  Si un falso negativo cuesta 20 veces más que un falso positivo, el umbral óptimo está muy por
  debajo de 0,5. Calcúlalo con el coste de cada error, no con la intuición.
- **Confundir desbalanceo con falta de señal.** Si las clases son inseparables porque las
  variables no informan, ningún remuestreo va a salvarte: solo conseguirás más falsos positivos.
  Comprueba primero si hay señal con una curva PR decente.

:::practica
enunciado: 10.000 transacciones con 100 fraudes. Con umbral 0,5 detectas 40 fraudes y señalas 50 inocentes; con umbral 0,2 detectas 80 y señalas 300. Si un fraude no detectado cuesta 200 € y una falsa alarma 5 €, calcula el coste de cada umbral y elige.
pista: Suma el coste de los falsos negativos y el de los falsos positivos: el umbral no se elige por precisión, sino por coste.
solucion: Umbral 0,5: falsos negativos 100 − 40 = 60, coste 60 · 200 = 12.000 €; falsos positivos 50 · 5 = 250 €; total 12.250 €. Umbral 0,2: falsos negativos 20, coste 4.000 €; falsos positivos 300 · 5 = 1.500 €; total 5.500 €. Gana el 0,2 y ahorra 6.750 € aunque su precisión sea peor: con un falso negativo 40 veces más caro que una falsa alarma, el listón baja.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo con un 99 % de accuracy sobre un problema con un 1 % de positivos, ¿qué te dice ese número?
o: Que el modelo es muy bueno y solo falla en un 1 % de los casos
o: Casi nada: predecir siempre la clase mayoritaria ya da ese 99 %
o: Que el modelo detecta el 99 % de los positivos
a: 2
e: Con una prevalencia del 1 %, la clase mayoritaria es el 99 % de las filas, así que el acierto trivial es 0,99. Para saber si hay detección de verdad hay que mirar la exhaustividad y la precisión de la clase minoritaria.
:::

:::quiz
p: Entrenas con submuestreo hasta dejar las clases al 50 %. ¿Qué hay que hacer antes de interpretar las probabilidades del modelo?
o: Nada, las probabilidades siguen siendo las del problema original
o: Reescalarlas, porque el modelo ha aprendido con una prevalencia distinta de la real
o: Volver a sobremuestrear hasta el 50 % y quedarse con la media de las dos predicciones
a: 2
e: La probabilidad que estima el modelo refleja la mezcla con la que entrenó. Si forzaste un 50 % de positivos cuando la realidad es un 1 %, el modelo sobreestima sistemáticamente el riesgo. Hay que corregir el sesgo con la razón de prevalencias antes de usarlas como probabilidades.
:::

:::aviso
En finanzas y en fraude, la clase positiva suele ser además la que más cambia con el tiempo: el
tipo de fraude de 2024 no se parece al de 2026. Un modelo con buena exhaustividad histórica
puede estar detectando un patrón que ya no existe. Revisa la deriva de la clase minoritaria
aparte de la del resto.
:::
