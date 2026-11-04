---
id: metricas-de-clasificacion
titulo: Métricas de clasificación
fase: 6
nivel: básico
rutas: [core, ds]
prerequisitos: [matriz-de-confusion, train-val-test]
tags: [evaluacion, clasificacion, metricas]
resumen: Exactitud, precisión, exhaustividad, F1 y balanced accuracy: cuál elegir según lo que cueste cada tipo de error.
fuentes: ["Sokolova y Lapalme (2009), 'A systematic analysis of performance measures for classification tasks'", "Powers (2011), 'Evaluation: From Precision, Recall and F-Measure to ROC, Informedness, Markedness and Correlation'"]
---

## En una frase

Una métrica de clasificación resume los cuatro recuentos de la [[matriz-de-confusion]] en un
solo número, y cada una incorpora de antemano una opinión sobre qué error es peor.

## La idea

Un banco revisa 1.000 operaciones al día y 20 son fraudulentas de verdad. Un detector que
respondiera «ninguna es fraude» acertaría 980 veces: un 98 % de exactitud y una utilidad
nula. Ese contraste es el corazón del tema: **la exactitud mide con qué frecuencia aciertas,
no si aciertas en lo que importa**.

Clasificar tiene solo dos maneras de equivocarse y no cuestan lo mismo. Un **falso positivo**
(marcar como fraude una compra legítima) bloquea la tarjeta de un cliente inocente: una
llamada, una disculpa y a veces un cliente perdido. Un **falso negativo** (dejar pasar un
fraude) cuesta el importe entero. En un cribado médico la balanza se inclina al revés: un
falso positivo es una prueba extra, y un falso negativo es una enfermedad sin tratar.

Las métricas responden a dos preguntas distintas:

- **Precisión:** cuando el modelo dice «positivo», ¿cuántas veces tiene razón? Es la métrica
  de quien sufre las alertas, como el analista que revisa la cola de casos marcados.
- **Exhaustividad** (también *recall* o sensibilidad): de todos los positivos reales, ¿cuántos
  detecta? Es la métrica de quien sufre lo que se escapa.
- **F1:** un único número que combina las dos anteriores y se hunde si una de ellas es muy
  baja, aunque la otra sea perfecta.
- **Balanced accuracy:** la media de la exhaustividad de cada clase. Es la exactitud corregida
  para que la clase mayoritaria no aplaste a la minoritaria.

No hay una métrica «mejor»: hay una métrica alineada con lo que cuesta cada error, y eso se
decide antes de mirar el resultado. Ese paso es [[umbrales-y-coste]], y la curva que recorre
todos los umbrales posibles es [[roc-auc]].

## Definición formal

Sobre `N` casos evaluados, con estas cuatro casillas:

- `VP` (verdaderos positivos): casos positivos que el modelo marcó como positivos.
- `FP` (falsos positivos): casos negativos que el modelo marcó como positivos.
- `FN` (falsos negativos): casos positivos que el modelo marcó como negativos.
- `VN` (verdaderos negativos): casos negativos que el modelo marcó como negativos.
- `N = VP + FP + FN + VN`, el total de casos.

:::formula
Exactitud = (VP + VN) / N
:::

:::formula
Precisión = VP / (VP + FP)          Exhaustividad = VP / (VP + FN)
:::

- La precisión queda **indefinida** (0 dividido entre 0) si el modelo no predice ningún
  positivo: no es que valga 0, es que no hay nada que medir. Forzar un 0 falsea la comparación.
- La exhaustividad también se llama sensibilidad; su gemela para la clase negativa es la
  `Especificidad = VN / (VN + FP)`, que responde «de todos los sanos, ¿a cuántos dejo en paz?».

:::formula
F1 = 2 · Precisión · Exhaustividad / (Precisión + Exhaustividad) = 2·VP / (2·VP + FP + FN)
:::

Es la **media armónica**, no la aritmética: la media armónica de 1 y 0 es 0, y la aritmética
sería 0,5. Por eso F1 solo es alto cuando precisión y exhaustividad lo son a la vez.

:::formula
Balanced accuracy = (Exhaustividad + Especificidad) / 2
:::

Con clases de tamaño muy distinto, la balanced accuracy es mucho más informativa que la
exactitud, porque da el mismo peso a cada clase en lugar de dar más peso a la que más abunda.

## Ejemplo

1.000 operaciones, 20 fraudes reales. El modelo levanta 30 alertas y 18 de ellas son fraude:

- `VP = 18`, `FP = 12`, `FN = 2`, `VN = 968`. Comprobación: 18 + 12 + 2 + 968 = 1.000.
- Exactitud = (18 + 968) / 1.000 = **0,986**.
- Precisión = 18 / 30 = **0,60**: cuatro de cada diez alertas son falsas alarmas.
- Exhaustividad = 18 / 20 = **0,90**: se le escapan 2 de los 20 fraudes.
- Especificidad = 968 / 980 = **0,9878**.
- F1 = 2 · 0,60 · 0,90 / 1,50 = **0,72**.
- Balanced accuracy = (0,90 + 0,9878) / 2 = **0,9439**.

Compara ese 0,72 de F1 con el 0,986 de exactitud: la exactitud dice «casi perfecto» y el F1
dice «aceptable, con muchas falsas alarmas». Las dos son correctas, y solo una es útil para
decidir si merece la pena poner el detector en producción.

:::figura
fichero: clasificacion-metricas-y-umbral
pie: A la izquierda, los cinco números del detector de fraude del ejemplo, todos calculados sobre la misma matriz de confusión: exactitud 0,986, balanced accuracy 0,944, F1 0,720, precisión 0,600 y exhaustividad 0,900. La línea de puntos es un modelo que dice «no» a todo: 0,980 de exactitud y cero fraudes detectados, casi indistinguible del anterior por esa sola cifra. A la derecha, un ejemplo distinto, con un 25 % de positivos, muestra cómo se mueven precisión, exhaustividad y F1 al subir el umbral: precisión y exhaustividad tiran en direcciones opuestas y el F1 de ese ejemplo tiene su máximo (0,80) en el umbral 0,60. Conclusión: elige la métrica antes de entrenar, a partir del coste de cada error, y publica siempre el umbral con el número.
fuente: figuras/metricas-de-clasificacion-1.py
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `VP` | Verdaderos positivos: casos positivos marcados como positivos | número de casos | Sube la precisión (el numerador) y la exhaustividad. Solo puede subir si el modelo acierta más, o si bajas el umbral |
| `FP` | Falsos positivos: casos negativos marcados como positivos | número de casos | Sube el denominador de la precisión, así que la precisión baja; la exhaustividad no se mueve (no aparece en su fórmula). Es el error que sufre quien revisa las alertas |
| `FN` | Falsos negativos: casos positivos que se escapan | número de casos | Baja la exhaustividad y no toca la precisión. Es el error que sufre quien esperaba la detección |
| `N` | El total de casos evaluados | número de casos | Con `N` fijo, más casos solo cambian repartiendo los cuatro recuentos. La exactitud es la única que se calcula sobre `N` |
| `umbral` | El punto de corte de la puntuación para decidir «positivo» | las de la puntuación | Bajarlo sube la exhaustividad y baja la precisión, y al revés. Toda métrica de un clasificador binario depende de él: sin el umbral, el número no es reproducible |
| `prevalencia` | La proporción de positivos reales en la población | tanto por uno | Con el mismo modelo, la precisión baja al bajar la prevalencia (los falsos positivos se cuentan contra menos aciertos) y la exactitud sube. F1 y balanced accuracy también se mueven: compara siempre con prevalencias parecidas |
:::

## Código

```python verificable
# Detector de fraude: 1.000 operaciones, 20 fraudes reales, 30 alertas y 18 aciertos
vp, fp, fn, vn = 18, 12, 2, 968

exactitud = (vp + vn) / (vp + fp + fn + vn)
precision = vp / (vp + fp)
exhaustividad = vp / (vp + fn)
f1 = 2 * precision * exhaustividad / (precision + exhaustividad)
especificidad = vn / (vn + fp)
balanced = (exhaustividad + especificidad) / 2

print(f"exactitud     {exactitud:.4f}")      # -> 0.9860
print(f"precision     {precision:.4f}")      # -> 0.6000
print(f"exhaustividad {exhaustividad:.4f}")  # -> 0.9000
print(f"F1            {f1:.4f}")             # -> 0.7200
print(f"balanced acc  {balanced:.4f}")       # -> 0.9439
```

```python verificable
# El clasificador trivial que dice "no" a todo: exactitud alta y utilidad nula.
n, fraudes = 1000, 20
vp, fp, fn, vn = 0, 0, fraudes, n - fraudes

print(f"exactitud     {(vp + vn) / n:.4f}")   # -> 0.9800
print(f"exhaustividad {vp / (vp + fn):.4f}")   # -> 0.0000
print("alertas lanzadas:", vp + fp)           # -> 0
```

:::claves
- `vp / (vp + fp)` con `vp + fp == 0` lanza `ZeroDivisionError`, no devuelve 0. sklearn devuelve 0 con un aviso en ese caso: son dos comportamientos distintos para la misma situación, y por eso la precisión «indefinida» hay que tratarla a mano.
- `f"{(vp + vn) / n:.4f}"` redondea al imprimir; el valor guardado en la variable sigue siendo el exacto. La exactitud del ejemplo es `986/1000 = 0,986` exacto, pero `0,9439` de balanced accuracy es un redondeo de `0,94387...`.
- `2 * precision * exhaustividad / (precision + exhaustividad)` es la media armónica. La aritmética, `(precision + exhaustividad) / 2`, daría 0,75 en vez de 0,72: F1 castiga que una de las dos sea baja, y esa es toda su razón de ser.
- `balanced = (exhaustividad + especificidad) / 2` necesita la especificidad, que se calcula con `VN` y `FP`. Una balanced accuracy alta con una precisión de 0,60 no es contradicción: está midiendo las dos clases por igual, no las alertas.
- En el segundo bloque, `vp = 0` deja `vp / (vp + fn)` en 0,0 sin error porque `fn = 20`. Cambia el ejemplo a un problema sin positivos reales (`fraudes = 0`) y esa misma línea revienta con `ZeroDivisionError`.
- `n - fraudes` es el número de negativos. Si escribes `fraudes` por error, `vn` pasa a valer 20, los cuatro recuentos suman 40 en vez de 1.000 y la exactitud que imprime el bloque pasa a ser 0,5: el ejemplo entero deja de enseñar lo que quiere enseñar.
:::

## Errores típicos

- **Presumir de exactitud con clases desbalanceadas.** Si el 98 % de los casos son negativos,
  un modelo que siempre dice «no» ya tiene 98 %. Publica además balanced accuracy, F1 o la
  matriz completa.
- **Confundir precisión con exhaustividad.** «El modelo acierta el 90 % de los fraudes» es
  exhaustividad; «el 90 % de las alertas son fraude» es precisión. Son números distintos y
  cuentan historias opuestas. Míralas siempre juntas.
- **Optimizar F1 sin preguntarse si FP y FN cuestan lo mismo.** F1 da el mismo peso a los dos
  errores. Si bloquear una compra legítima cuesta 3 € y un fraude no detectado cuesta 200 €,
  F1 no es tu métrica: la que lo es se construye en [[umbrales-y-coste]].
- **Comparar F1 entre conjuntos con prevalencias distintas.** Con la misma calidad del modelo,
  F1 baja cuando el positivo es más raro. Un F1 de 0,7 en un problema con 1 % de positivos y
  otro de 0,7 con 40 % de positivos no significan lo mismo.
- **Medir sobre el conjunto de entrenamiento.** Un árbol profundo saca 1,0 en entrenamiento y
  la mitad en prueba. Las métricas se calculan sobre datos que el modelo no ha visto
  ([[train-val-test]]).
- **Reportar una sola cifra sin el umbral.** Toda métrica de un clasificador binario depende
  del punto de corte elegido. Sin decir cuál, el número no es reproducible.

:::practica
enunciado: Un filtro de spam marca 80 de 500 correos; 50 eran spam y 45 de los marcados lo eran. Calcula exactitud, precisión, exhaustividad, F1 y balanced accuracy.
pista: VP = 45 y los otros tres recuentos salen de restar. La balanced accuracy es la media de exhaustividad y especificidad.
solucion: VP = 45, FP = 35, FN = 5, VN = 415. Exactitud = 460/500 = 0,92. Precisión = 45/80 = 0,5625. Exhaustividad = 45/50 = 0,90. F1 = 2 · 0,5625 · 0,90 / 1,4625 = 0,692. Balanced = (0,90 + 415/450) / 2 = 0,911. El 0,92 de exactitud esconde que 35 de cada 80 alertas son correos legítimos: publica el F1 o la matriz.
:::

## Comprueba que lo sabes

:::quiz
p: Un detector marca 30 operaciones como fraude y 18 lo son; en total había 20 fraudes entre 1.000 operaciones. ¿Cuál es su exhaustividad?
o: 18 / 30 = 0,60
o: 18 / 20 = 0,90
o: 986 / 1.000 = 0,986
a: 2
e: La exhaustividad divide los aciertos positivos entre todos los positivos reales: 18 de 20. La primera opción es la precisión (aciertos entre las alertas) y la tercera es la exactitud.
:::

:::quiz
p: ¿Por qué la exactitud es una mala métrica cuando el 98 % de los casos son negativos?
o: Porque no está definida si no hay predicciones positivas
o: Porque un modelo que siempre predice negativo ya obtiene un 98 % y no detecta nada
o: Porque solo funciona con variables continuas
a: 2
e: La exactitud suma los dos tipos de acierto y la clase mayoritaria domina la cuenta. Balanced accuracy o F1 reparten el peso entre clases y dejan al descubierto a ese modelo trivial. La indefinición por división entre cero afecta a la precisión, no a la exactitud.
:::

:::trampa
Cambiar de métrica después de ver los resultados es hacer trampa. Si pruebas exactitud,
precisión, F1 y AUC y publicas la que salió mejor, el número que publicas está sesgado al
alza: con cuatro métricas sobre el mismo conjunto siempre hay una que suena bien. Elige la
métrica antes de entrenar, a partir del coste de cada error.
:::
