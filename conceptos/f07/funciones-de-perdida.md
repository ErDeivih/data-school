---
id: funciones-de-perdida
titulo: Funciones de pérdida
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [perceptron-y-mlp, maxima-verosimilitud, entropia-e-informacion]
tags: [perdidas, entrenamiento, entropia, clasificacion]
resumen: El número que el entrenamiento empuja hacia abajo en cada paso; elegir la pérdida es decidir qué error te importa y cuál puedes ignorar.
fuentes: ["Goodfellow, Bengio y Courville (2016), 'Deep Learning', cap. 6", "Lin et al. (2017), 'Focal Loss for Dense Object Detection'"]
---

## En una frase

La función de pérdida es el número que el optimizador intenta hacer pequeño en cada paso:
resume en un solo escalar qué significa «equivocarse» y, con ello, decide qué aprende la red y
qué se le perdona.

## La idea

Imagina dos alumnos que hacen un examen de 100 preguntas. El primero acierta 90 y falla 10
seguidas; el segundo acierta 90 y falla 10 repartidas, pero en tres de ellas escribe una
barbaridad. Si solo miras el número de fallos, los dos empatan. Si el profesor penaliza más
las respuestas seguras y equivocadas —las que iba diciendo en voz alta que eran correctas—,
el segundo suspende. La función de pérdida es ese criterio de corrección: no mide el número de
errores, mide **cómo de malos** son.

De ahí que existan varias. El error cuadrático medio (MSE) eleva al cuadrado cada desviación,
así que un error de 10 pesa 100 veces más que uno de 1: es la elección natural en regresión.
La entropía cruzada castiga el logaritmo de la probabilidad que le das a la clase verdadera,
y ese logaritmo crece sin límite cerca de cero: decir «0,01» cuando la respuesta era «sí»
cuesta 4,61, mientras que decir «0,60» cuesta 0,51. La penalización explota justo donde el
modelo está **seguro y equivocado**, que es exactamente el caso que quieres corregir.

Hay un segundo motivo, más profundo, para estas fórmulas y no otras: casi todas las pérdidas
habituales son **verosimilitudes negativas**. Minimizar el MSE equivale a suponer ruido
gaussiano de varianza constante; minimizar la entropía cruzada binaria equivale a suponer que
cada etiqueta sale de una Bernoulli cuyo parámetro predice la red; la entropía cruzada de
varias clases es la verosimilitud de una distribución categórica. Minimizar la pérdida es hacer
[[maxima-verosimilitud|máxima verosimilitud]] con una distribución distinta cada vez, y esa es
la razón de que las fórmulas tengan logaritmos y cuadrados y no otras formas raras.

Dos consecuencias prácticas antes de seguir. La primera: la pérdida es un **sustituto** de lo
que de verdad te importa (exactitud, AUC, dinero ganado). Solo se puede entrenar una función
derivable, así que a veces optimizas algo distinto de tu métrica y las dos curvas se separan.
La segunda: la pérdida tiene **escala**. Si usas `sum` en vez de `mean`, multiplicas el valor
por el tamaño del lote y, con él, el tamaño efectivo del paso de tu optimizador.

## Definición formal

Para `n` ejemplos de un lote, con `yᵢ` el valor u objetivo real e `ŷᵢ` la predicción:

:::formula
MSE = (1/n) · Σᵢ (yᵢ − ŷᵢ)²
:::

- `n` — número de ejemplos del lote.
- `yᵢ` — valor real del ejemplo `i`.
- `ŷᵢ` — valor que predice el modelo para el ejemplo `i`.
- `Σᵢ` — suma sobre todos los ejemplos del lote.

En clasificación binaria, con `p̂ᵢ` la probabilidad que la red asigna a la clase 1 e `yᵢ ∈ {0, 1}`:

:::formula
BCE = −(1/n) · Σᵢ [ yᵢ · log(p̂ᵢ) + (1 − yᵢ) · log(1 − p̂ᵢ) ]
:::

- `p̂ᵢ` — probabilidad de la clase positiva, salida de una sigmoide.
- `log` — logaritmo natural; `log(1) = 0` y `log(x) → −∞` cuando `x → 0`.
- En cada ejemplo solo sobrevive uno de los dos sumandos: el que corresponde a la etiqueta.

Con `K` clases y `zᵢ` el vector de logits (puntuaciones sin normalizar) del ejemplo `i`:

:::formula
CE = −(1/n) · Σᵢ log( softmax(zᵢ)[yᵢ] )
:::

- `softmax(z)[k] = exp(z[k]) / Σⱼ exp(z[j])` — convierte logits en probabilidades que suman 1.
- `softmax(zᵢ)[yᵢ]` — probabilidad asignada a la clase verdadera.

La pérdida focal añade un factor que apaga los ejemplos ya fáciles:

:::formula
focal = −(1/n) · Σᵢ α · (1 − p_tᵢ)^γ · log(p_tᵢ)
:::

- `p_tᵢ` — probabilidad que el modelo asigna a la clase verdadera del ejemplo `i`.
- `γ` — exponente de enfoque; con `γ = 0` la fórmula es la entropía cruzada otra vez, y `γ = 2`
  es el valor habitual. Cuanto mayor es `γ`, más se ignoran los ejemplos resueltos.
- `α` — peso de la clase (en el caso binario, el peso de la clase positiva), para el
  desbalanceo.

Para aprender representaciones (embeddings) se usan pérdidas **contrastivas**, que no comparan
con una etiqueta sino entre ejemplos. La de tripleta, con un ancla `a`, un positivo `p` de la
misma clase, un negativo `n` de otra, una distancia `d` y un margen `m > 0`:

:::formula
tripleta = max( 0, d(a, p) − d(a, n) + m )
:::

Si el positivo ya está más cerca que el negativo por un margen `m`, la pérdida es cero y no hay
gradiente. La variante InfoNCE generaliza esto a un positivo y muchos negativos dentro del
lote, y es la que usan los modelos de imagen y texto que se alinean entre sí.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | número de ejemplos del lote que entran en el promedio | ejemplos | Con `mean` el valor de la pérdida no cambia; con `sum` se multiplica por `n` y con él el paso efectivo del optimizador. Cambiar de lote sin cambiar la reducción es un cambio de tasa de aprendizaje encubierto |
| `yᵢ` | valor real u objetivo del ejemplo `i` | las del objetivo | Es el dato, no un mando: define qué significa acertar. Un error de escala aquí se paga al cuadrado con el MSE y linealmente con la entropía cruzada |
| `ŷᵢ` | valor que predice el modelo en regresión | las del objetivo | Al acercarse a `yᵢ` la pérdida baja al cuadrado de la distancia; al alejarse crece cuadráticamente, así que un error de 10 pesa 100 veces más que uno de 1 |
| `p̂ᵢ` | probabilidad que el modelo da a la clase positiva (salida de una sigmoide) | adimensional, entre 0 y 1 | Acercarse a la etiqueta correcta lleva la BCE a 0; alejarse la dispara. En 0,01 con etiqueta 1 la pérdida vale 4,6 y no tiene techo |
| `log` | logaritmo natural que usa la entropía cruzada | — | Es lo que hace que la penalización no tenga techo: `log(1) = 0` y `log(x) → −∞` cuando `x → 0`, justo en el caso del modelo seguro y equivocado |
| `zᵢ` | vector de logits (puntuaciones sin normalizar) del ejemplo `i` | adimensionales | Solo cuentan las **diferencias** entre logits, no su tamaño: sumar la misma constante a todos deja el `softmax` igual. Al crecer la diferencia a favor de la clase verdadera, la pérdida baja |
| `K` | número de clases | clases | Con más clases, la probabilidad de acertar por azar baja y la entropía cruzada de un modelo que reparte uniforme sube: vale `log K` |
| `γ` | exponente de enfoque de la pérdida focal | adimensional | Con `γ = 0` la focal es la entropía cruzada otra vez. Al subirlo, los ejemplos ya acertados pesan cada vez menos y el gradiente se concentra en los difíciles |
| `α` | peso de la clase positiva (o uno por clase) para el desbalanceo | adimensional | Reparte la culpa entre clases: al subirlo, los errores de esa clase pesan más. Ojo, el valor de la pérdida deja de ser comparable con experimentos que usen otro `α` |
| `p_tᵢ` | probabilidad que el modelo da a la clase verdadera del ejemplo `i` | adimensional, entre 0 y 1 | Al subir (más acierto), el factor `(1 − p_t)^γ` se hace pequeño y ese ejemplo deja de mandar en el gradiente: con `γ = 2`, un acierto al 95 % pesa 0,0025 |
| `m` | margen que se exige entre el positivo y el negativo en la pérdida de tripleta | las de la distancia `d` | Al subir, se exige más separación: más tripletas se quedan con pérdida positiva y el modelo empuja con más fuerza las representaciones |
:::

:::nota
La pérdida total casi nunca es solo la de los datos: se le suma un término de
regularización, `L_total = L_datos + λ · R(θ)`. En esa suma, `λ` es un hiperparámetro y `R` una
penalización sobre los pesos, como la norma L2 que se explica en
[[regularizacion-l1-l2|regularización L1 y L2]].
:::

## Ejemplo

Tres ejemplos de clasificación binaria. Etiquetas reales `y = [1, 0, 1]` y probabilidades
predichas `p = [0.9, 0.2, 0.6]`. Calculamos la BCE término a término:

- Ejemplo 1 (`y = 1`, `p = 0.9`): `−log(0.9) = 0,105`.
- Ejemplo 2 (`y = 0`, `p = 0.2`): `−log(1 − 0.2) = −log(0.8) = 0,223`.
- Ejemplo 3 (`y = 1`, `p = 0.6`): `−log(0.6) = 0,511`.

BCE = (0,105 + 0,223 + 0,511) / 3 = **0,2798**. El MSE de las mismas predicciones es
((1−0,9)² + (0−0,2)² + (1−0,6)²) / 3 = (0,01 + 0,04 + 0,16) / 3 = **0,0700**.

Ahora supón que el tercer ejemplo, en vez de un tibio 0,6, fuera un 0,01 confiadísimo. Su
término pasa de 0,511 a `−log(0,01) = 4,605`, y la BCE sube a (0,105 + 0,223 + 4,605) / 3 =
**1,644**: multiplicar por 5,9 la pérdida por un solo ejemplo. Con la focal y `γ = 2`, el peso
de ese tercer ejemplo sería `(1 − 0,6)² = 0,16` si su probabilidad fuera 0,6, y el del primero
(`p = 0,95`) sería `(1 − 0,95)² = 0,0025`: los aciertos cómodos dejan de mandar en el
gradiente.

Fíjate además en la asimetría: el término del MSE pasa de 0,16 a (0,99)² = 0,98, es decir 0,82
más, mientras el de la BCE pasa de 0,51 a 4,61, o sea 4,09 más. En clasificación, esa
diferencia es la que hace que el modelo aprenda a no ser rotundamente incorrecto.

:::figura
fichero: perdidas-bce-mse-y-focal
pie: El eje horizontal es la probabilidad que el modelo da a la clase verdadera, así que a la izquierda están los errores y a la derecha los aciertos; el eje vertical va en escala logarítmica porque las diferencias son de órdenes de magnitud. La curva azul (entropía cruzada) se dispara cuando el modelo está seguro y equivocado: en `p = 0,01` cobra 4,6 y no tiene techo, y esa es exactamente la conducta que quieres castigar. La roja (error cuadrático) se aplana en 1 en ese mismo punto: castiga mucho menos al que se equivoca con confianza, y por eso el gradiente se desvanece justo cuando más falta hace. Comparar las dos curvas en `p = 0,01` es ver por qué en clasificación se usa entropía cruzada y no MSE. El panel derecho explica el otro problema, el del desbalanceo: con `γ = 2`, un ejemplo acertado con holgura (0,95) deja de aportar (0,0025), mientras que uno difícil conserva casi todo su peso. El resultado práctico es que el gradiente se concentra en los ejemplos que aún no se aciertan, en vez de gastarse en los miles de negativos fáciles que dominan un conjunto desbalanceado.
fuente: figuras/funciones-de-perdida-1.py
:::

## Código

```python verificable
import numpy as np

y = np.array([1.0, 0.0, 1.0])            # etiquetas reales
p = np.array([0.9, 0.2, 0.6])            # probabilidades predichas

# BCE: -log de la probabilidad que el modelo da a la clase verdadera
# En cada ejemplo solo sobrevive un sumando: el que corresponde a su etiqueta
bce = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
mse = np.mean((y - p) ** 2)

print(f"BCE {bce:.4f}")                   # -> BCE 0.2798
print(f"MSE {mse:.4f}")                   # -> MSE 0.0700

# Un error seguro y equivocado no se paga igual que uno tibio
print(f"-log(0.01) {-np.log(0.01):.3f}")  # -> -log(0.01) 4.605
print(f"-log(0.60) {-np.log(0.60):.3f}")  # -> -log(0.60) 0.511
```

:::claves
- `y * np.log(p) + (1 - y) * np.log(1 - p)` parece sumar dos términos, pero en cada fila uno de
  los dos vale cero: la etiqueta `y` es 0 o 1, y actúa de interruptor. Es la forma vectorizada de
  escribir «quédate solo con el logaritmo de la clase verdadera».
- `np.mean` divide entre el número de elementos, no entre `len(y)`: si `y` y `p` fueran matrices
  de dos dimensiones, el promedio sería de todas las celdas. Con vectores da igual, con
  probabilidades por clase es un error de escala silencioso.
- `np.log(0)` es `-inf` y la pérdida se convierte en `nan` en un paso. Aquí no pasa porque las
  probabilidades del ejemplo son 0,9, 0,2 y 0,6, pero con una predicción exactamente 0 y
  etiqueta 1 el cálculo revienta. Por eso en PyTorch se usan las versiones con logits.
- `(1 - p_correcta) ** gamma * bce` es la focal entera: no es una pérdida nueva, es la entropía
  cruzada **ponderada** por un factor que depende de lo bien que lo hace el modelo en ese
  ejemplo. Cambiar `gamma` de 2 a 0 devuelve exactamente la BCE del bloque anterior.
- `for p_i, b, f in zip(p_correcta, bce, focal)` recorre los tres arrays **a la vez** y se para en
  el más corto. Si te equivocas de orden en el `zip`, imprime columnas cruzadas sin dar error:
  los tres tienen la misma longitud y el mismo tipo.
- `nn.BCEWithLogitsLoss()` espera **logits**, no probabilidades. Por dentro aplica el sigmoide y
  el logaritmo juntos con el truco log-sum-exp, que no desborda cuando la probabilidad se acerca
  a 0 o a 1. Si le pasas probabilidades ya recortadas con una sigmoide, calcula el sigmoide dos
  veces y la pérdida sale mal sin avisar.
- En `nn.CrossEntropyLoss(weight=...)`, el peso es un tensor **por clase** y va en el orden de
  las columnas de la salida. Con `weight=torch.tensor([1.0, 5.0])` los errores de la clase 1
  cuestan cinco veces más, y desde ese momento el valor numérico de la pérdida ya no se puede
  comparar con el de un experimento que use otros pesos.
:::

```python verificable
import numpy as np

# Focal: el factor (1 - p)^gamma apaga los ejemplos que ya se aciertan con holgura.
p_correcta = np.array([0.95, 0.60, 0.10])   # probabilidad de la clase verdadera
gamma = 2.0

bce = -np.log(p_correcta)
focal = (1 - p_correcta) ** gamma * bce

for p_i, b, f in zip(p_correcta, bce, focal):
    # zip recorre los tres arrays a la vez, en paralelo, y se para en el mas corto
    print(f"p={p_i:.2f}  BCE {b:.3f}  focal {f:.4f}")
# -> p=0.95  BCE 0.051  focal 0.0001
# -> p=0.60  BCE 0.511  focal 0.0817
# -> p=0.10  BCE 2.303  focal 1.8651
```

```python ilustrativo
import torch
import torch.nn as nn

# En PyTorch las perdidas de clasificacion esperan logits, no probabilidades: la version
# con logits aplica el sigmoide por dentro con el truco log-sum-exp y no desborda.
criterio = nn.BCEWithLogitsLoss()
logits = torch.tensor([2.0, -1.0, 0.5])
objetivo = torch.tensor([1.0, 0.0, 1.0])
print(criterio(logits, objetivo).item())     # 0.3048

# Multiclase: NO apliques softmax antes, CrossEntropyLoss ya lo hace por dentro
multiclase = nn.CrossEntropyLoss(weight=torch.tensor([1.0, 5.0]))   # peso por clase
salida = torch.randn(4, 2)                   # 4 ejemplos, 2 clases
etiquetas = torch.tensor([0, 1, 1, 0])       # etiquetas como indices de clase, no one-hot
print(multiclase(salida, etiquetas).item())
```

## Errores típicos

- **Aplicar softmax y luego `CrossEntropyLoss`.** La función ya lleva el softmax dentro, así
  que normalizas dos veces: las probabilidades se aplastan hacia 0,5, el gradiente se hace
  diminuto y el modelo aprende lentísimo. Pasa lo mismo con `Sigmoid` + `BCELoss` en binaria:
  usa `BCEWithLogitsLoss`.
- **Usar MSE con una sigmoide a la salida en clasificación.** El gradiente del MSE respecto al
  logit incluye el factor `p̂ · (1 − p̂)`, que tiende a cero cuando la predicción está saturada.
  Justo cuando el modelo está segurísimo y equivocado, el gradiente desaparece y no corrige
  nada. Con entropía cruzada ese término se cancela y el gradiente es `p̂ − y`.
- **Calcular `log(0)`.** Si una predicción es exactamente 0 y la etiqueta es 1, `log(0)` es
  `−inf` y la pérdida se convierte en `nan`, que contamina todos los pesos en un solo paso.
  Trabaja con logits o recorta las probabilidades con un épsilon.
- **Confundir la pérdida con la métrica.** La pérdida baja mientras la exactitud se estanca, o
  al revés. Además, si le pones pesos de clase, el valor de la pérdida deja de ser comparable
  entre experimentos: dos configuraciones con pérdidas 0,3 y 0,4 no están ordenadas por calidad
  si los pesos son distintos. Compara siempre la misma métrica, calculada igual.
- **Ignorar el desbalanceo con BCE.** Con un 1 % de positivos, predecir siempre «no» da una BCE
  de 0,045 y parece un éxito. Pasa a focal, a pesos por clase o a remuestreo, y mira
  [[desbalanceo-de-clases|las técnicas de desbalanceo]] y [[precision-recall-y-pr|la curva
  precisión-exhaustividad]] en vez de la exactitud.
- **Cambiar la reducción sin darte cuenta.** `reduction='sum'` multiplica la pérdida por el
  tamaño del lote y `reduction='none'` devuelve un vector con un valor por ejemplo. Si cambias
  de lote de 32 a 256 manteniendo la suma, el paso efectivo del optimizador se multiplica por
  8 y el entrenamiento se descontrola.

:::practica
enunciado: Un ejemplo de tres clases tiene logits z = (2, 1, 0) y la clase verdadera es la segunda, la del logit 1. Calcula las probabilidades con softmax y la entropía cruzada de ese ejemplo. Después di cuánto valdría la pérdida si el modelo hubiera puesto el logit mayor en la clase equivocada, con z = (2, 0, 1).
pista: softmax divide exp(z_k) entre la suma de las exponenciales; la pérdida es −log de la probabilidad de la clase verdadera.
solucion: Las exponenciales son (7,389; 2,718; 1) y suman 11,107, así que las probabilidades son (0,665; 0,245; 0,090). La pérdida es −log(0,245) = 1,406. Con z = (2, 0, 1) la probabilidad de la clase verdadera cae a 1/11,107 = 0,090 y la pérdida sube a 2,408: la entropía cruzada castiga mucho más estar seguro y equivocado.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo da probabilidad 0,9 a la clase correcta en un ejemplo y 0,1 en otro (ambos con etiqueta 1). ¿Cuánto aporta cada ejemplo a la entropía cruzada binaria?
o: 0,105 y 2,303
o: 0,9 y 0,1
o: 0,81 y 0,01
a: 1
e: La BCE usa el logaritmo de la probabilidad de la clase verdadera, con signo negativo: −log(0,9) = 0,105 y −log(0,1) = 2,303. Las otras dos opciones son la probabilidad en sí y su cuadrado, que son las cuentas del MSE: el error cuadrático medio daría 0,01 y 0,81, con lo que el ejemplo malo pesaría mucho menos de lo que pesa con la entropía cruzada.
:::

:::quiz
p: ¿Por qué se usa `BCEWithLogitsLoss` en vez de aplicar una sigmoide y luego `BCELoss`?
o: Porque es más rápido al no calcular la sigmoide
o: Porque calcula la pérdida directamente sobre los logits y evita el desbordamiento de `log(0)`
o: Porque permite usar varias clases a la vez
a: 2
e: Las dos versiones son matemáticamente equivalentes, pero la que trabaja con logits aplica internamente el truco log-sum-exp, que es numéricamente estable cuando la probabilidad se acerca a 0 o a 1. El problema no es la velocidad, y para varias clases la función es `CrossEntropyLoss`, no la binaria.
:::

:::quiz
p: Con un 99 % de ejemplos negativos, un modelo que siempre predice «negativo» obtiene una pérdida BCE de 0,045. ¿Qué conclusión es correcta?
o: El modelo es bueno porque la pérdida es casi cero
o: La pérdida es baja porque acierta la clase mayoritaria, y con este desbalanceo hay que mirar precisión, exhaustividad o usar pérdida focal
o: La BCE no se puede usar con clases desbalanceadas
a: 2
e: La BCE promedia por ejemplo, y el 99 % de las veces ese ejemplo es un negativo fácil: el promedio sale pequeño sin que el modelo haya aprendido nada útil sobre la clase que importa. La BCE sí se puede usar, pero con pesos por clase, con focal o mirando las métricas adecuadas.
:::

:::trampa
Si tu pérdida es `nan` después de unas iteraciones, casi nunca es la fórmula: es un `log(0)`,
una división por cero o una tasa de aprendizaje alta que hizo explotar los pesos. Mira primero
[[depuracion-de-redes|la guía de depuración]] antes de reescribir la pérdida.
:::
