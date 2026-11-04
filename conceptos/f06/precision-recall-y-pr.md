---
id: precision-recall-y-pr
titulo: Curva precisión-exhaustividad
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [metricas-de-clasificacion, matriz-de-confusion]
tags: [evaluacion, umbral, desbalanceo, recuperacion]
resumen: La curva que mide lo que de verdad importa cuando el positivo es raro, con una línea base que es la prevalencia y no el 0,5.
fuentes: ["Saito y Rehmsmeier (2015), 'The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets'", "Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval', cap. 8"]
---

## En una frase

La curva precisión-exhaustividad dibuja, para cada umbral, cuántas de tus alertas son correctas
frente a cuántos de los positivos reales capturas, y su área se compara contra la prevalencia,
no contra 0,5.

## La idea

Vuelve al detector de fraude: 20 fraudes entre 1.000 operaciones, un 2 % de prevalencia. El
modelo levanta 30 alertas y 18 son fraude. La [[matriz-de-confusion]] dice: 18 aciertos, 12
falsas alarmas, 2 fugas. La curva [[roc-auc]] diría que el FPR es `12/980 = 0,012`, un 1,2 %:
sobre el papel, casi perfecto. Pero el analista que abre la cola ve 30 casos y solo 18 son
fraude: trabaja con un 40 % de ruido. **La ROC mide el ruido relativo a los negativos; la curva
PR lo mide relativo a tus alertas.** Cuando los negativos son el 99 % de la muestra, esas dos
cosas no se parecen en nada.

La curva precisión-exhaustividad (curva PR) es la misma idea que la ROC con otros ejes: se
recorren todos los umbrales y se dibuja la precisión frente a la exhaustividad. Su ventaja es
que la línea base es evidente y honesta. Un clasificador que ordena al azar tiene, en cualquier
punto, una precisión igual a la **prevalencia**: si el 1 % de los casos son positivos y disparas
al azar, el 1 % de tus alertas serán aciertos. Por eso el área bajo la curva PR (AP, *average
precisión*) se lee siempre contra ese número: un AP de 0,15 con una prevalencia del 1 % es un
modelo 15 veces mejor que el azar, aunque el número parezca pequeño. Un AP de 0,15 con una
prevalencia del 40 % es un desastre.

Ese es el precio de la curva PR: **depende de la prevalencia**. Si mañana la proporción de
fraude cambia, el mismo modelo da otra AP. La ROC no se mueve. No es un defecto: es exactamente
el motivo por el que la PR dice la verdad sobre tu operación. Si tu problema real tiene un
positivo raro, evalúa en condiciones de positivo raro.

## Definición formal

Con `τ` el umbral, y recordando que la exhaustividad es la TPR:

:::formula
Precisión(τ) = VP(τ) / (VP(τ) + FP(τ))          Exhaustividad(τ) = VP(τ) / (VP(τ) + FN(τ))
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `VP(τ)`, `FP(τ)`, `FN(τ)` | Los recuentos de la matriz de confusión cuando se predice positivo todo lo que supera `τ` | casos | Más `FP` con el mismo `VP` baja la precisión; más `FN` baja la exhaustividad |
| `Precisión(τ)` | De las alertas que has emitido, cuántas eran reales | adimensional, entre 0 y 1 | Sube al subir el umbral; el azar daría la prevalencia |
| `Exhaustividad(τ)` | De los positivos reales, cuántos capturas; es la TPR | adimensional, entre 0 y 1 | Baja al subir el umbral |
| `τ` | Umbral a partir del cual se emite la alerta | las de la puntuación | Sube: la precisión sube y la exhaustividad cae |
| `AP` | Área bajo la curva PR, sumando escalones de exhaustividad | adimensional, entre 0 y 1 | Sube si el modelo ordena mejor; se compara con la prevalencia, no con 0,5 |
| `Pₙ`, `Rₙ` | Precisión y exhaustividad en el umbral `n`, ordenados por exhaustividad creciente | adimensional | Cada punto se pondera por lo que aporta de exhaustividad |
| `Rₙ − Rₙ₋₁` | El trozo de exhaustividad que gana ese umbral | adimensional, entre 0 y 1 | Si un tramo pesa más, la AP se parece más a la precisión de ese punto |
| `π` | Prevalencia: la línea base de la curva y de la AP | adimensional, entre 0 y 1 | Suben la AP y la precisión de todos los puntos, sin que el modelo cambie |
:::

- `VP(τ)`, `FP(τ)`, `FN(τ)` — los recuentos de la matriz de confusión cuando se predice positivo
  todo lo que puntúa por encima de `τ`.
- La curva PR es el conjunto de puntos `(Exhaustividad(τ), Precisión(τ))` al recorrer `τ`. La
  exhaustividad crece de 0 a 1 y la precisión, en general, baja.
- Si el modelo no predice ningún positivo, la precisión queda indefinida; el punto no se dibuja.

:::formula
AP = Σₙ (Rₙ − Rₙ₋₁) · Pₙ
:::

- `Pₙ` y `Rₙ` — precisión y exhaustividad en el umbral `n`, ordenados por exhaustividad
  creciente.
- `Rₙ − Rₙ₋₁` — el trozo de exhaustividad que gana ese umbral. La suma pondera cada precisión
  por lo que aporta, y es la definición que usa `average_precision_score` de `scikit-learn`
  (interpolación escalonada, no trapezoidal).
- La línea base de la AP es la prevalencia `π = (VP + FN) / N`.

Las dos curvas son la misma información con distinto eje, y se pasa de una a otra con la
prevalencia `π`:

:::formula
Precisión = TPR · π / (TPR · π + FPR · (1 − π))
:::

Con `π` pequeño, el término `FPR · (1 − π)` domina el denominador y la precisión se hunde
aunque el FPR sea minúsculo. Ahí está, en una línea, todo el asunto del desbalanceo.

:::figura
fichero: pr-curva-y-linea-base
pie: A la izquierda, la curva PR del ejemplo de 10.000 casos con 100 positivos: la meseta se queda en 0,15 (más de ocho de cada diez alertas son falsas) y el área bajo la curva es la AP, que se compara contra la prevalencia (0,01), no contra 0,5. A la derecha, la misma cuenta mirada desde el otro eje: con un TPR fijo del 90 %, bajar el FPR del 5 % al 1 % sube la precisión de 0,15 a 0,48 si el positivo es el 1 %, y la deja en 0,99 si es la mitad. Conclusión: la ROC es cómoda para comparar modelos, pero cuando el positivo escasea la curva que describe tu operación es esta.
fuente: figuras/precision-recall-y-pr-1.py
:::

## Ejemplo

Un buscador devuelve 10 resultados ordenados por relevancia. Solo 3 son relevantes, y aparecen
en las posiciones 1, 3 y 6:

```
posicion   1  2  3  4  5  6  7  8  9  10
relevante  s  n  s  n  n  s  n  n  n   n
```

Cada vez que aparece un relevante, mira la precisión en ese corte:

- Posición 1: 1 acierto de 1 → precisión 1, exhaustividad 1/3 = 0,333.
- Posición 3: 2 aciertos de 3 → precisión 0,667, exhaustividad 2/3 = 0,667.
- Posición 6: 3 aciertos de 6 → precisión 0,5, exhaustividad 3/3 = 1.

La AP es la media de esas precisiones (aquí cada relevante aporta `1/3` de exhaustividad):

```
AP = (1/3)·1 + (1/3)·0,667 + (1/3)·0,5 = 0,333 + 0,222 + 0,167 = 0,722
```

La prevalencia del conjunto es `3/10 = 0,3`. Un orden aleatorio daría AP ≈ 0,3, así que este
0,722 es claramente mejor que el azar, sin ser perfecto: hay un relevante en la posición 6.

Y el contraste que justifica la curva: con 100 positivos entre 10.000 casos (1 %), un modelo
con `AUC = 0,92` puede tener `AP = 0,148`. En la ROC parece casi redondo; en la PR se ve que
solo una de cada siete alertas es real.

## Código

```python verificable
# 10 resultados de un buscador, ya ordenados de mas a menos relevante
# Una lista de Python, no un np.array: aqui solo hace falta recorrerla.
relevancias = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]

aciertos, suma = 0, 0.0
# enumerate(..., start=1) devuelve (posicion, valor) empezando a contar en 1: asi `posicion`
# es el numero de resultados que llevas vistos, que es el denominador de la precision.
for posicion, rel in enumerate(relevancias, start=1):
    if rel == 1:
        aciertos += 1
        suma += aciertos / posicion     # precision en el punto en que aparece el relevante

total = sum(relevancias)                # cuantos relevantes hay en total
ap = suma / total                       # media de las precisiones en cada relevante
azar = total / len(relevancias)         # la prevalencia: la linea base de la curva PR

print(f"AP          {ap:.4f}")                      # -> 0.7222
print(f"prevalencia {azar:.4f}")                    # -> 0.3000
print(f"veces mejor que el azar {ap / azar:.1f}")   # -> 2.4

# sklearn.metrics.average_precision_score hace esta misma suma escalonada.
```

:::claves
- `enumerate(relevancias, start=1)` empieza a contar en 1 a propósito: la posición del resultado y el número de resultados vistos son el mismo número, y sin ese `start=1` la precisión del primer acierto saldría `1/0`, un error de división.
- `aciertos, suma = 0, 0.0` es un desempaquetado de tupla, no dos asignaciones distintas. El `0.0` mantiene `suma` en coma flotante desde el principio; en Python 3 la división ya daría float igualmente.
- `average_precision_score` **suma escalones**, no interpola trapecios: pondera cada precisión por el trozo de exhaustividad que aporta. `auc(recall, precision)` de `sklearn.metrics` hace la interpolación trapezoidal y da otro número con los mismos datos. Elige una y di cuál usas.
- `y.mean()` sobre un array de ceros y unos es directamente la prevalencia (0,01 en el ejemplo), porque la media de unos y ceros es la proporción de unos. Es la línea base contra la que se lee la AP.
- La AP **depende de la prevalencia**: si cambias la proporción de positivos del conjunto, el mismo modelo da otra AP. La ROC no se mueve. No es un defecto de la PR: es lo que la hace útil cuando el positivo es raro.
- En el primer bloque, un resultado relevante en la posición 1 aporta una precisión de 1,0 y solo `1/3` de exhaustividad: la AP es una media ponderada, así que un acierto muy arriba pesa mucho más que uno al final de la lista.
:::

```python verificable
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

# 100 positivos entre 10.000 casos: la clase rara es el 1 %
pos = np.r_[np.linspace(0.80, 0.99, 90), np.linspace(0.10, 0.60, 10)]
neg = np.r_[np.linspace(0.80, 0.99, 495), np.linspace(0.00, 0.79, 9405)]
y = np.r_[np.ones(100), np.zeros(9900)]
score = np.r_[pos, neg]

# La ROC parece redonda; la PR ensena el ruido real de las alertas
print(f"AUC {roc_auc_score(y, score):.3f}")            # -> 0.920
print(f"AP  {average_precision_score(y, score):.4f}")  # -> 0.1483
# y.mean() sobre unos y ceros es la proporcion de positivos: la linea base de la PR.
print(f"azar (prevalencia) {y.mean():.4f}")             # -> 0.0100
```

## Errores típicos

- **Comparar una AP contra 0,5.** La línea base de la curva PR es la prevalencia del conjunto.
  Una AP de 0,15 con un 1 % de positivos es un buen resultado; con un 40 % de positivos sería
  un desastre. Di siempre la prevalencia al lado de la AP.
- **Usar la AP calculada con una prevalencia y desplegar con otra.** El modelo no cambia, pero
  la precisión sí. Si tu tráfico real tiene menos positivos que tu conjunto de prueba, la
  precisión en producción será peor que la del informe.
- **Mezclar AP escalonada con el área trapezoidal.** `average_precision_score` suma escalones;
  `auc(recall, precision)` interpola trapecios. Dan números distintos sobre los mismos datos.
  Elige una y di cuál.
- **Creer que la curva PR «corrige» el desbalanceo.** No corrige nada: solo lo hace visible.
  Un modelo malo sigue teniendo un AP malo por muy raro que sea el positivo.
- **Evaluar con precisión y exhaustividad de un solo umbral y llamarlo «la curva PR».** Un punto
  no es una curva. Si solo reportas uno, di cuál es el umbral y por qué lo elegiste
  ([[umbrales-y-coste]]).
- **Confundir el recall de la búsqueda con el recall@k.** El primero cuenta todos los relevantes
  del catálogo; el segundo solo los que caben en las primeras `k` posiciones. Son problemas
  distintos, y el segundo se estudia en [[metricas-de-ranking]].

:::practica
enunciado: Un buscador devuelve 12 resultados y solo 4 son relevantes, en las posiciones 2, 3, 7 y 10. Calcula la AP y compárala con la línea base del azar.
pista: Suma la precisión en cada posición relevante y divide entre el total de relevantes; la línea base es la prevalencia.
solucion: Precisiones en los cortes: 1/2 = 0,5; 2/3 = 0,667; 3/7 = 0,429; 4/10 = 0,4. AP = (0,5 + 0,667 + 0,429 + 0,4) / 4 = 1,995/4 = 0,499. La prevalencia es 4/12 = 0,333, así que un orden aleatorio daría AP ≈ 0,333: el 0,499 es una vez y media el azar, lastrado por los relevantes que aparecen en las posiciones 7 y 10.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo tiene AP = 0,15 sobre un conjunto donde solo el 1 % de los casos son positivos. ¿Cómo se interpreta?
o: Es un mal modelo, porque 0,15 está muy lejos de 1
o: Es bastante mejor que el azar, porque el azar daría una precisión del 1 %
o: No se puede interpretar sin conocer el AUC
a: 2
e: En la curva PR la referencia es la prevalencia. Un AP de 0,15 sobre una base del 1 % equivale a multiplicar por 15 la precisión de un orden aleatorio. Compararlo con 1 o con 0,5 es el error clásico.
:::

:::quiz
p: ¿Por qué la curva PR suele ser más informativa que la ROC cuando el positivo es muy raro?
o: Porque la precisión se mide sobre las alertas emitidas, y ahí las falsas alarmas pesan de verdad
o: Porque la ROC no se puede calcular con clases desbalanceadas
o: Porque la curva PR no depende de la prevalencia
a: 1
e: El eje vertical de la PR es la precisión, que divide los aciertos entre todas las alertas: cada falso positivo cuenta. En la ROC el eje es el FPR, que divide entre todos los negativos, y con millones de negativos unos cientos de falsas alarmas apenas mueven la aguja. Al contrario de lo que dice la tercera opción, la PR es la que sí depende de la prevalencia.
:::

:::aviso
Si tu conjunto de prueba está balanceado a propósito (por ejemplo, 50 % de positivos) y tu
población real tiene un 2 %, la curva PR que midas será mucho más optimista que la realidad.
Remuestrear para entrenar está bien; informar métricas calculadas sobre esa muestra como si
fueran de producción, no.
:::
