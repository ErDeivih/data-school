---
id: knn
titulo: K vecinos más cercanos
fase: 6
nivel: básico
rutas: [ds, alg]
prerequisitos: [norma-y-distancias, escalado-y-transformacion, train-val-test]
tags: [clasificacion, distancia, no-parametrico, vecinos]
resumen: Guardar los datos y decidir por mayoría entre los k vecinos más parecidos: el modelo más simple que existe y el que peor envejece al crecer la dimensión.
fuentes: ["Fix y Hodges (1951), 'Discriminatory Analysis: Nonparametric Discrimination'", "Cover y Hart (1967), 'Nearest Neighbor Pattern Classification'"]
---

## En una frase

K vecinos más cercanos no aprende nada en el entrenamiento: guarda todos los ejemplos y, para
predecir uno nuevo, busca los `k` más parecidos y decide por votación (o por su media, si es
regresión).

## La idea

Tienes una lista de pisos vendidos con sus características y su precio. Llega un piso nuevo y
quieres estimar cuánto vale. Lo más natural del mundo: busca los pisos más parecidos que
conozcas y mira a cuánto se vendieron. Si los tres más parecidos se vendieron a 210.000,
225.000 y 240.000 euros, tu estimación es 225.000. Eso es todo KNN, sin ecuaciones.

La consecuencia interesante es que **no hay entrenamiento**. Guardar los datos es instantáneo;
todo el trabajo ocurre en la predicción, donde hay que calcular la distancia del punto nuevo a
todos los del conjunto de entrenamiento. Es lo contrario de un [[regresion-lineal|modelo
lineal]] o de un [[gradient-boosting|gradient boosting]], que se toman su tiempo al aprender y
luego predicen en microsegundos. A esto se le llama modelo *perezoso* o basado en instancias.

El parámetro `k` es el que decide el equilibrio. Con `k = 1` cada predicción copia la etiqueta
del punto más cercano: el error de entrenamiento es exactamente cero (cada punto es su propio
vecino a distancia 0) y el modelo dibuja islas alrededor de cada observación, incluidos los
errores de etiquetado. Con `k` grande la frontera es suave pero se diluyen los detalles
locales. La teoría dice que con `k = 1` y muchos datos el error es como mucho el doble del
error óptimo (el llamado «error de Bayes»), y que al ir creciendo `k` ese error se acerca al
óptimo; en la práctica, `k` se elige con
[[validacion-cruzada|validación cruzada]].

Dos advertencias que se cobran caras. La primera: KNN se basa en distancias, así que
**hay que escalar las variables**. Si el precio del piso se mide en euros (200.000) y el número
de habitaciones en unidades (3), la distancia estará dominada por el precio y las habitaciones
no influirán nada. La segunda: en espacios de muchas dimensiones todas las distancias se
parecen entre sí y «el más cercano» deja de ser informativo. Es la
[[maldicion-de-la-dimensionalidad|maldición de la dimensionalidad]].

## Definición formal

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x` | El punto nuevo que quieres predecir | las de las variables | No es un mando: es el dato que llega. Al alejarse de la nube de entrenamiento, sus vecinos son peores y la predicción se vuelve arbitraria |
| `xᵢ` | Un ejemplo del conjunto de entrenamiento | las de las variables | Cuantos más ejemplos, mejor, pero cada predicción cuesta más: el trabajo crece con `n`, no con `k` |
| `d(x, xᵢ)` | Distancia entre el punto nuevo y el ejemplo `i` | las de las variables | Es el criterio de orden. Si una variable tiene un rango mucho mayor que las demás, la distancia la decide ella y las otras dejan de contar |
| `k` | Número de vecinos que votan | vecinos (entero) | Sube el sesgo y baja la varianza: la frontera se suaviza y se diluyen los detalles locales. Con `k = n` predice siempre la clase mayoritaria; con `k` par y dos clases, puede haber empate |
| `N_k(x)` | El conjunto de los `k` vecinos más cercanos | conjunto de ejemplos | Su tamaño es `k`. Es lo único que mira el modelo: el resto del conjunto de entrenamiento no influye en esta predicción |
| `1{yᵢ = c}` | Vale 1 si el vecino `i` es de la clase `c` y 0 si no | 0 o 1 | Al subir el número de vecinos de una clase, sube su suma y gana la votación. Es un indicador, no una magnitud que se ajuste |
| `wᵢ = 1 / d(x, xᵢ)` | Peso del vecino cuando se pondera por cercanía | 1 / (unidades) | Da más voz a los vecinos inmediatos y menos a los lejanos del corte. Con `d = 0` se va a infinito: ese caso hay que tratarlo aparte |
| `n` | Número de ejemplos guardados | ejemplos | El coste de cada predicción crece linealmente con `n` y la memoria también. El entrenamiento sigue siendo instantáneo |
| `d` | Número de variables (dimensiones) | variables | Es la maldición de la dimensionalidad: al subir `d`, todas las distancias se parecen y el cociente entre vecino y lejano tiende a 1 |
:::

Sea un conjunto de entrenamiento `D = {(x₁, y₁), …, (xₙ, yₙ)}` y una distancia `d(·, ·)`.

Para clasificación, con un punto nuevo `x`, se ordenan los puntos de `D` por `d(x, xᵢ)`
ascendente y se toman los `k` primeros, el conjunto `N_k(x)`. La predicción es la clase
mayoritaria:

:::formula
ŷ = argmax_c Σ_{i ∈ N_k(x)} 1{yᵢ = c}
:::

- `x` — vector de variables del punto a predecir.
- `d(x, xᵢ)` — distancia entre el punto nuevo y el ejemplo `i`; lo habitual es la euclídea
  `√Σⱼ (xⱼ − xᵢⱼ)²`, y también se usa Manhattan `Σⱼ /xⱼ − xᵢⱼ/` o Minkowski.
- `k` — número de vecinos; un entero positivo, típicamente entre 3 y 30.
- `N_k(x)` — el conjunto de los `k` vecinos más cercanos.
- `1{·}` — vale 1 si la condición se cumple y 0 si no.

En regresión se sustituye la votación por el promedio: `ŷ = (1/k) Σ_{i ∈ N_k(x)} yᵢ`. Y si
quieres dar más peso a los vecinos inmediatos, se pondera por el inverso de la distancia,
`wᵢ = 1 / d(x, xᵢ)`, con la precaución de tratar aparte el caso `d = 0`.

Detalles que cambian el resultado: con `k` par y dos clases, la votación puede empatar (usa
`k` impar o desempata por distancia); con distancias euclídeas y variables sin escalar, el
resultado lo decide la variable de mayor rango; y con muchos ceros (datos dispersos, texto),
la distancia euclídea pierde sentido y conviene el coseno.

## Ejemplo

Tres pisos conocidos, con dos variables: superficie en metros cuadrados y número de
habitaciones. El piso nuevo tiene 90 m² y 3 habitaciones.

| Piso | Superficie (m²) | Habitaciones | Precio (miles de €) |
| --- | --- | --- | --- |
| A | 80 | 3 | 200 |
| B | 100 | 4 | 260 |
| C | 85 | 2 | 185 |

Distancias euclídeas al piso nuevo (90, 3):

- A: `√((90−80)² + (3−3)²) = √100 = 10,0`
- B: `√((90−100)² + (3−4)²) = √101 = 10,05`
- C: `√((90−85)² + (3−2)²) = √26 = 5,10`

Con `k = 1` la predicción es el precio de C: 185.000 €. Con `k = 3`, la media de los tres:
(200 + 260 + 185) / 3 = **215.000 €**. Fíjate en lo frágil que es la distancia sin escalar: los
dos pisos casi empatados (10,0 y 10,05) se separan por 5 centésimas, mientras que la
diferencia de superficie (10 m²) pesa muchísimo más que la de habitaciones (1). Si
estandarizas ambas variables antes, las dos cuentan por igual y el orden de los vecinos puede
cambiar.

## Código

:::figura
fichero: knn-frontera-y-dimensionalidad
pie: A la izquierda, las dos fronteras del mismo modelo sobre los mismos 60 puntos: la azul (k = 1) acierta el 100 % del entrenamiento porque cada punto es su propio vecino a distancia cero, y esa perfección es memorización, no aprendizaje; la naranja (k = 15) es una sola curva que ignora el ruido. Fíjate en que las dos líneas se separan justo donde están los puntos mal etiquetados, que es el precio de suavizar. A la derecha está el otro problema, medido: con 2 dimensiones el vecino más cercano está unas 140 veces más cerca que el más lejano, y con 500 dimensiones el cociente sube a 0,84. Cuando el vecino más cercano casi da igual que el más lejano, «el más parecido» deja de ser un criterio y KNN se queda sin de dónde sacar información.
fuente: figuras/knn-1.py
:::

```python verificable
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# n_informative=4: solo 4 de las 8 columnas llevan senal; de las otras 4, dos son
# combinaciones de las informativas y dos son ruido, asi que la distancia se calcula
# en 8 dimensiones y esas 4 no aportan informacion nueva.
X, y = make_classification(n_samples=400, n_features=8, n_informative=4,
                           class_sep=1.0, random_state=0)
# Devuelve cuatro arrays en este orden fijo: X e y de entrenamiento y de prueba.
# stratify=y reparte las clases en la misma proporcion en las dos partes.
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

# k=1 memoriza: acierta el 100 % del entrenamiento y generaliza peor.
print(f"{'k':>3}  {'exactitud train':>15}  {'exactitud test':>15}")
for k in (1, 3, 15, 45):
    m = KNeighborsClassifier(n_neighbors=k).fit(X_tr, y_tr)
    print(f"{k:>3}  {m.score(X_tr, y_tr):>15.3f}  {m.score(X_te, y_te):>15.3f}")
# ->   k  exactitud train   exactitud test
# ->   1            1.000            0.825
# ->   3            0.896            0.833
# ->  15            0.879            0.842
# ->  45            0.886            0.850
```

:::claves
- `train_test_split` devuelve **cuatro** objetos y se reparten siempre en el mismo orden: primero las variables y luego las etiquetas, en entrenamiento y en prueba. Si los intercambias, el modelo se ajusta con las etiquetas y no da ningún error: solo da resultados sin sentido.
- `m.score(X, y)` devuelve un `float` (la exactitud) y por dentro llama a `predict`; no te da las etiquetas ni las probabilidades. Para eso están `m.predict(X)` y `m.predict_proba(X)`, que devuelven arrays nuevos.
- Con `k = 1` la exactitud de entrenamiento es exactamente 1,000 siempre, con cualquier dato y cualquier ruido. No es una señal de que el modelo sea bueno: cada punto es su propio vecino a distancia 0. Comparar esa cifra entre modelos distintos es el error clásico.
- `flip_y=0.12` cambia a mano la etiqueta de ese porcentaje de puntos. Es lo que hace visible la diferencia entre las dos fronteras: con `flip_y=0.0` las dos líneas coincidirían y el panel no explicaría nada. Y `random_state=7` fija esos puntos: sin él, cada ejecución dibuja un ruido distinto.
- El cálculo de la maldición usa difusión (*broadcasting*): `X - q` resta un vector de `d` números a una matriz de `1000 × d` sin bucles, y `axis=1` suma **por filas**, es decir, las `d` coordenadas de cada punto. Con `axis=0` sumaría por columnas y el resultado sería una distancia por variable, no una por punto.
- `malla.ravel()` convierte la rejilla de `260 × 260` en una lista plana de 67.600 pares, que es lo que espera `predict`. Después hay que deshacer el cambio con `reshape(malla_x.shape)`: si te olvidas, `contour` recibe una lista plana y falla o dibuja mal.
:::

```python verificable
import numpy as np

# La maldicion de la dimensionalidad, medida: en muchas dimensiones
# el vecino mas cercano y el mas lejano estan casi a la misma distancia.
rng = np.random.default_rng(0)
print("dim  dist. al vecino mas cercano  al mas lejano  cociente")
for d in (2, 5, 20, 100, 500):
    X = rng.uniform(size=(1000, d))     # 1000 puntos en una caja de lado 1
    q = rng.uniform(size=d)             # el punto nuevo, tambien al azar
    # X - q resta el vector a las 1000 filas; axis=1 suma las d coordenadas de
    # cada punto, que es la distancia euclidea al cuadrado antes de la raiz.
    dist = np.sqrt(((X - q) ** 2).sum(axis=1))
    print(f"{d:>4}  {dist.min():>28.3f}  {dist.max():>12.3f}  {dist.min() / dist.max():>8.3f}")
# -> dim  dist. al vecino mas cercano  al mas lejano  cociente
# ->    2                         0.010         1.334     0.007
# ->    5                         0.144         1.633     0.088
# ->   20                         1.047         2.267     0.462
# ->  100                         3.013         4.899     0.615
# ->  500                         8.198         9.755     0.840
```

## Errores típicos

- **No escalar las variables.** El error número uno. Una variable en euros y otra en unidades
  hacen que la distancia la decida la primera. Estandariza (o normaliza) siempre, y hazlo
  dentro de un [[pipelines-de-ml|pipeline]] para que la media y la desviación se calculen solo
  con el entrenamiento.
- **Usar `k = 1` porque la exactitud de entrenamiento es perfecta.** Ese 100 % no mide
  aprendizaje, mide memorización: cada punto es su propio vecino a distancia cero. Empieza con
  `k` impar entre 3 y 15 y ajústalo con validación.
- **Evaluar con muchas variables y sin reducir dimensión.** Si tienes 200 columnas y el
  vecino más cercano está a una distancia casi idéntica a la del más lejano, KNN no tiene de
  dónde sacar información. Reduce con [[pca|PCA]] o selecciona variables, o cambia de modelo.
- **Aplicar KNN a datos con escalas muy distintas por grupos (texto, conteos dispersos).** La
  distancia euclídea sobre vectores con muchos ceros da valores parecidos para documentos muy
  diferentes; ahí se usa similitud del coseno, y para texto suele ganar
  [[naive-bayes|Naive Bayes]] o un modelo lineal.
- **Ignorar el coste de predicción.** Con un millón de filas de entrenamiento, cada predicción
  recorre un millón de distancias. Para servir en producción en tiempo real, usa una estructura
  de índice (KD-tree, Ball-tree) o acepta que KNN no es la herramienta.
- **Tratar las variables categóricas como números.** Codificar «ciudad» como 1, 2, 3 hace que
  la ciudad 3 esté «más lejos» de la 1 que la 2, lo cual es falso. Usa
  [[encoding-de-categoricas|one-hot]] o una distancia específica.

:::practica
enunciado: Tres clientes con (edad, importe): A (30, 100) paga, B (40, 200) no paga y C (35, 150) paga. Llega uno nuevo (33, 130). Calcula las distancias euclídeas, la predicción con k = 1 y con k = 3, y qué sale ponderando por 1/d.
pista: La distancia es la raíz de la suma de las diferencias al cuadrado; sin escalar, el importe manda porque se mueve en decenas.
solucion: Distancias: A √(3² + 30²) = 30,15; B √(7² + 70²) = 70,35; C √(2² + 20²) = 20,10. Con k = 1 gana C y predice «paga». Con k = 3 votan los tres: dos pagas frente a una, predice «paga». Ponderando por 1/d: C 0,050, A 0,033 y B 0,014; la clase «paga» suma 0,083 frente a 0,014. El vecino más cercano es C en los tres casos porque la edad apenas pesa.
:::

## Comprueba que lo sabes

:::quiz
p: En KNN, ¿dónde está el coste computacional principal?
o: En el entrenamiento, que resuelve un sistema de ecuaciones
o: En la predicción, que calcula la distancia del punto nuevo a todos los ejemplos guardados
o: En ninguno de los dos: es un modelo instantáneo en ambos sentidos
a: 2
e: KNN no aprende parámetros: guardar el conjunto de entrenamiento es inmediato. El trabajo está en predecir, porque hay que comparar el punto nuevo con todos los ejemplos y ordenar. Por eso se le llama modelo perezoso y por eso no escala a millones de filas en producción.
:::

:::quiz
p: ¿Por qué la maldición de la dimensionalidad afecta especialmente a KNN?
o: Porque el modelo necesita más memoria para guardar los datos
o: Porque al añadir dimensiones las distancias entre puntos tienden a igualarse, y «el vecino más cercano» deja de ser significativamente más cercano que cualquier otro
o: Porque a partir de 10 dimensiones el algoritmo no converge
a: 2
e: En dimensión alta el cociente entre la distancia al vecino más cercano y al más lejano se acerca a 1, así que el criterio de vecindad pierde su poder discriminatorio. El modelo no falla por memoria ni por convergencia: falla porque la noción de «cerca» se vacía.
:::

:::truco
Para clasificación binaria usa `k` impar y evita los empates. Y antes de mirar el valor de
`k`, prueba con y sin estandarizar: la diferencia entre esas dos versiones suele ser mucho
mayor que la que hay entre dos valores razonables de `k`.
:::
