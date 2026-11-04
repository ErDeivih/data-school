---
id: recomendadores
titulo: Sistemas de recomendación
fase: 6
nivel: avanzado
rutas: [ds, alg]
prerequisitos: [producto-punto-y-similitud, descomposicion-svd, metricas-de-ranking]
tags: [recomendacion, factorizacion, ranking, filtrado]
resumen: Filtrado colaborativo, basado en contenido y factorización de matrices, con la parte que casi nadie hace bien: evaluar el orden de la lista, no el error de la nota.
fuentes: ["Koren, Bell y Volinsky (2009), 'Matrix Factorization Techniques for Recommender Systems'", "Ricci, Rokach y Shapira (2011), 'Recommender Systems Handbook'"]
---

## En una frase

Un recomendador predice qué le va a gustar a alguien comparándolo con gente de gustos
parecidos, con la descripción de los productos, o con ambas cosas a la vez, y se evalúa por el
orden en que acierta, no por el error de la nota estimada.

## La idea

Tienes una matriz con usuarios en las filas y productos en las columnas, y dentro las notas de
lo que cada uno ha valorado. Casi todas las casillas están vacías: un usuario típico puntúa 30
películas de un catálogo de 10.000. El objetivo es rellenar las casillas vacías que le
interesan, que no son todas: solo la primera fila de la lista que le vas a enseñar.

Hay tres familias de soluciones y conviene saber cuándo va cada una:

1. **Filtrado colaborativo.** «A ti te gusta lo que le gusta a gente parecida a ti.» Se parece a
   los usuarios (user-user) o a los productos (item-item) midiendo similitud entre filas o
   columnas de la matriz. No necesita saber nada de los productos, y por eso descubre relaciones
   inesperadas. Su límite es el arranque en frío: un usuario nuevo no se parece a nadie todavía.
2. **Basado en contenido.** «Te gustan las de ciencia ficción, así que te recomiendo esta de
   ciencia ficción.» Necesita atributos de los productos (género, marca, texto) y funciona desde
   el primer día, pero no descubre gusto por cosas que nunca has visto.
3. **Factorización de matrices.** Se aprende un vector corto (de 20 a 200 números) para cada
   usuario y cada producto de forma que su producto escalar aproxime la nota. Es lo que ganó el
   concurso de Netflix y es la base de casi todo lo que se usa hoy en producción.

En un sistema industrial se combinan las tres y se añade contexto: hora, dispositivo, estación
del año. Y hay un detalle que decide si el sistema sirve: la mayoría de las recomendaciones
buenas consisten en **ordenar bien** entre cientos de candidatos, no en acertar la nota con dos
decimales.

## Definición formal

Sea `R` la matriz de valoraciones, con `r_ui` la nota del usuario `u` al producto `i` y vacío
cuando no existe. Sea `O` el conjunto de pares observados.

**Similitud entre productos (item-item).** Con los vectores de valoraciones centrados por
usuario, `v_i` (columna `i`):

:::formula
sim(i, j) = (v_i · v_j) / (‖v_i‖ · ‖v_j‖) = cos(θ)
:::

- `v_i · v_j` — producto escalar: suma de los productos de las notas coincidentes.
- `‖v_i‖` — norma euclídea del vector, `√(Σ_k v_ki²)`.
- El resultado está en `[−1, 1]`; solo se compara sobre los usuarios que han valorado **ambos**
  productos. Con notas de 1 a 5 (todas positivas) el coseno nunca baja de 0, así que en la
  práctica va de 0 a 1. Aquí no hay que hacer nada especial porque la matriz es densa: los tres
  usuarios han valorado las tres columnas, así que el coseno del vector entero coincide con el
  del solape. En una matriz dispersa de verdad, en cambio, la columna lleva un cero donde el
  usuario no votó y ese coseno mide otra cosa: mezcla usuarios que no comparan y sale sistemáticamente
  más bajo que el del solape (nunca más alto). Mide solo sobre los usuarios que han valorado los dos
  productos, y si no hay ninguno en común el parecido no está definido y hay que decidir qué hacer
  con ese par, porque dejarlo tal cual te devuelve un `nan`.

**Predicción item-item** para el usuario `u` y el producto `i`, con `N(i)` los `k` productos
más parecidos a `i` que `u` ya ha valorado:

:::formula
r̂_ui = μ_i + Σ_{j ∈ N(i)} sim(i, j) · (r_uj − μ_j) / Σ_{j ∈ N(i)} sim(i, j)
:::

- `μ_i` — media de las notas del producto `i`; `μ_j`, la del producto `j`.
- `r_uj − μ_j` — lo que este usuario puntuó al producto `j` **por encima o por debajo de lo
  normal**. Es la corrección que evita que un usuario generoso arrastre la predicción hacia
  arriba. Sin centrar, la fórmula es la misma pero con `μ = 0`.

**Factorización** con sesgos, que es el modelo de referencia en la práctica:

:::formula
r̂_ui = μ + b_u + b_i + p_uᵗ · q_i
:::

- `μ` — media global de todas las notas.
- `b_u` — sesgo del usuario: cuánto puntúa de más o de menos en general.
- `b_i` — sesgo del producto: cuánto recibe de más o de menos en general.
- `p_u`, `q_i` — vectores latentes de dimensión `f`; su producto escalar recoge la afinidad que
  no explican los sesgos.
- Se ajustan minimizando el error cuadrático con regularización:
  `Σ_{(u,i) ∈ O} (r_ui − r̂_ui)² + λ(b_u² + b_i² + ‖p_u‖² + ‖q_i‖²)`. La `λ` evita que un
  usuario con tres valoraciones reciba un sesgo enorme.

**Evaluación de ranking.** Con `k` el tamaño de la lista, `rel_i` la relevancia del producto en
la posición `i` (1 si es relevante, 0 si no; o la nota) y `DCG` la ganancia descontada:

:::formula
DCG@k = Σ_{i=1..k} (2^rel_i − 1) / log₂(i + 1)        NDCG@k = DCG@k / IDCG@k
:::

- `IDCG@k` — el DCG que se obtendría con el mejor orden posible: es la normalización, así que
  `NDCG@k` va de 0 a 1.
- `precision@k` — fracción de los `k` primeros que son relevantes. Solo es comparable con el
  mismo `k`.
- `recall@k` — fracción de todos los relevantes que aparecen en los `k` primeros.
- El denominador `log₂(i + 1)` hace que bajar un producto relevante de la posición 1 a la 2
  cueste mucho menos que bajarlo de la 1 a la 10.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `μ` | Media global de todas las valoraciones observadas | puntos de la escala | Todas las predicciones suben lo mismo: es un desplazamiento común y no cambia el orden de la lista |
| `b_u` | Sesgo del usuario: cuánto puntúa de más o de menos en general | puntos de la escala | Un usuario generoso arrastra hacia arriba todas sus predicciones si no se centra por producto; es lo que separa «le gusta todo» de «este producto es bueno» |
| `b_i` | Sesgo del producto: cuánto recibe de más o de menos en general | puntos de la escala | Los productos populares suben en todas las listas y el recomendador se vuelve un ranking de popularidad |
| `p_u`, `q_i` | Vectores latentes de usuario y producto: la afinidad que no explican los sesgos | adimensional | Si crecen sin control, el modelo memoriza las pocas valoraciones que tiene cada usuario: por eso se regularizan |
| `f` | Dimensión de los vectores latentes | componentes | Más capacidad para captar gustos finos y más riesgo de sobreajuste, sobre todo con usuarios de pocas valoraciones |
| `λ` | Peso de la regularización sobre sesgos y factores | adimensional | Con `λ` alto los sesgos se encogen hacia 0 y el modelo se parece a predecir la media; con `λ` muy bajo, un usuario con tres notas recibe un sesgo enorme |
| `sim(i, j)` | Parecido entre dos productos, coseno de sus columnas centradas | adimensional (−1 a 1) | Pesos más altos dan más voz a ese vecino en la predicción; si la suma de similitudes es 0, la media ponderada se rompe |
| `k` (vecinos) | Cuántos productos parecidos entran en la predicción | vecinos | Más vecinos suavizan la predicción y meten productos cada vez menos parecidos: sube el sesgo y baja la varianza |
| `rel_i` | Relevancia del producto que está en la posición `i` | la de la etiqueta (0/1 o nota) | Sube la ganancia de ese puesto y el `DCG` con ella; al doblar `rel` la ganancia no se dobla, se multiplica por potencias de 2 |
| `DCG@k` | Ganancia acumulada de los `k` primeros puestos, descontada por la posición | ganancia | Al subir `k` siempre crece (o se queda igual): es una suma de términos no negativos |
| `NDCG@k` | `DCG@k` dividido entre el mejor `DCG@k` posible | adimensional (0 a 1) | Se acerca a 1 cuando lo más relevante está arriba. No tiene por qué crecer con `k`: con `k = 1` una lista con el mejor producto primero ya vale 1,00 |
:::

## Ejemplo

Tres usuarios que han puntuado tres productos (A, B, C) del 1 al 5, y un cuarto usuario nuevo
que solo ha puntuado A y C:

```
        A    B    C
u1      5    4    1
u2      4    3    2
u3      2    1    4
u4      5    ?    2
```

Similitudes entre columnas (coseno sobre las tres valoraciones observadas):

- `sim(A, B) = 0,994`. Casi idénticos: quien puntúa alto A puntúa alto B.
- `sim(A, C) = 0,683` y `sim(B, C) = 0,599`. Menos parecidos.

Queremos predecir la nota de `u4` en B. Los dos vecinos valorados por `u4` son A y C, con pesos
`0,994` y `0,599`:

- **Sin centrar**: `(0,994 · 5 + 0,599 · 2) / (0,994 + 0,599) = 3,872`. La predicción sale alta
  porque `u4` puntuó A con un 5, y ese 5 tira del resultado.
- **Centrando por producto** (medias: A = 3,667, B = 2,667, C = 2,333): las desviaciones de `u4`
  son `5 − 3,667 = +1,333` en A y `2 − 2,333 = −0,333` en C. Entonces
  `r̂ = 2,667 + (0,994 · 1,333 + 0,599 · (−0,333)) / 1,593 = 3,373`.

La diferencia entre 3,872 y 3,373 es de medio punto, y viene solo del sesgo: `u4` es un usuario
generoso (valora A con 5 cuando la media es 3,667) y el producto B recibe notas bajas. Centrar
separa «a este usuario le gusta todo» de «a este producto le gusta a todo el mundo», que es la
mitad del trabajo de un recomendador.

Para la evaluación, dos listas de cuatro productos con relevancias `3, 0, 2, 1` y `2, 0, 3, 1`
(3 = muy relevante, 0 = nada):

- Las dos tienen `precision@2 = 0,5`: en ambas, uno de los dos primeros es relevante.
- Pero `NDCG@4` vale `0,9508` en la primera y `0,7379` en la segunda, porque en la primera el
  producto más relevante está en el puesto 1 y en la segunda en el puesto 3. La precisión no ve
  la diferencia; NDCG sí.

:::figura
fichero: recomendadores-ndcg-y-orden
pie: Las dos listas del ejemplo tienen el mismo contenido y el mismo acierto en los dos primeros puestos: precision@2 = 0,50 en ambas, como se ve en el panel izquierdo, donde el segundo puesto está vacío en las dos. El panel derecho enseña la única forma de distinguirlas: el NDCG acumulado, que descuenta cada puesto por su posición y lo compara con el mejor orden posible de esos mismos puestos. La lista A pone el producto más relevante (3) primero y termina en 0,95; la B lo pone tercero y se queda en 0,74. Fíjate además en la forma de la curva de la lista A: con k = 1 vale 1,00, porque para un solo puesto es perfecta, y al pedir dos puestos baja a 0,79, porque el segundo no aporta nada. Eso es exactamente lo que la precisión no puede contar, y la razón de fondo para no elegir el modelo con una sola métrica: la precisión premia acertar, el NDCG premia acertar pronto, y un recomendador se juzga por lo que se ve en los primeros puestos.
fuente: figuras/recomendadores-1.py
:::

## Código

```python verificable
import numpy as np

# Tres usuarios que han puntuado tres articulos (A, B, C) del 1 al 5.
train = np.array([(5.0, 4, 1),
                  (4.0, 3, 2),
                  (2.0, 1, 4)])
normas = np.linalg.norm(train, axis=0, keepdims=True)    # (1, 3): una norma por columna
similitud = (train.T @ train) / (normas.T @ normas)      # coseno entre columnas (articulos)
print("similitud A-B:", round(similitud[0, 1], 3),
      "A-C:", round(similitud[0, 2], 3),
      "B-C:", round(similitud[1, 2], 3))
# -> similitud A-B: 0.994 A-C: 0.683 B-C: 0.599

# Un cuarto usuario puntua A con 5 y C con 2. Queremos predecirle B.
medias = train.mean(axis=0)                              # una media por articulo
pesos = np.array([similitud[0, 1], similitud[2, 1]])     # parecido de A y C con B
valores = np.array([5.0, 2.0])
print("prediccion sin centrar:", round(float((pesos * valores).sum() / pesos.sum()), 3))
# -> prediccion sin centrar: 3.872
centrado = valores - np.array([medias[0], medias[2]])    # cada articulo respecto a su media
print("prediccion centrada:", round(float(medias[1] + (pesos * centrado).sum() / pesos.sum()), 3))
# -> prediccion centrada: 3.373
```

:::claves
- `np.linalg.norm(train, axis=0, keepdims=True)` calcula la norma de **cada columna**, y el
  `keepdims=True` deja la forma `(1, 3)` para que `normas.T @ normas` sea una matriz `3 × 3` que se
  divide elemento a elemento contra la de productos escalares. Sin `keepdims`, `normas` sería un
  vector `(3,)` y el producto de fuera ya no sería la matriz de normas.
- `train.T @ train` da los productos escalares **entre columnas**, es decir entre artículos: es el
  filtrado item-item. Quitando el `.T` se compararían usuarios (user-user), que es otro
  recomendador con los mismos datos y otra respuesta en el arranque en frío.
- La matriz `similitud` es simétrica, así que `similitud[0, 1]` y `similitud[1, 0]` valen lo mismo.
  El código usa solo la mitad de arriba; si en algún momento la rellenas a mano, no dupliques
  valores redondeados de formas distintas o dejarás de tener una matriz simétrica.
- `pesos.sum()` es la suma de los **pesos**, no de los valores: la predicción es una media
  ponderada. Si la suma de similitudes fuera 0 (vecinos que no se parecen en nada), la división
  daría `nan` y el `nan` se propagaría a toda la lista sin lanzar ningún error.
- En el bloque del NDCG, `np.log2(np.arange(2, r.size + 2))` genera los denominadores log₂(2),
  log₂(3), … en una sola línea, y `2 ** r - 1` es la ganancia. `ideal = np.sort(r)[::-1]` es el
  mejor orden posible: si te olvidas de invertir, el `IDCG` sale menor que el `DCG` y el NDCG puede
  pasar de 1 sin que nada falle. Y si quieres `NDCG@k` con `k` menor que la lista, recorta también el
  ideal a esos `k` puestos (`ideal[:k]`): el ideal entero mide otra cosa y da otro número (con
  `k = 4` las dos formas coinciden porque el cuarto puesto del ideal vale 0).
- `precision2 = sum(1 for r in lista[:2] if r > 0) / 2` cuenta relevantes, no suma relevancia, y el
  `2` del denominador está escrito a mano. Si cambias el corte a 5 tienes que cambiar los dos
  sitios: `lista[:5]` y `/ 5`. Es el error clásico al comparar `precision@5` con `precision@20`.
:::

```python verificable
import numpy as np

def ndcg(relevancia):
    """Ganancia acumulada descontada, normalizada por el orden ideal."""
    r = np.asarray(relevancia, float)
    dcg = ((2 ** r - 1) / np.log2(np.arange(2, r.size + 2))).sum()   # descuento log2(2), log2(3)...
    ideal = np.sort(r)[::-1]                                        # el mejor orden posible
    idcg = ((2 ** ideal - 1) / np.log2(np.arange(2, ideal.size + 2))).sum()
    return dcg / idcg

# Dos ordenaciones de los mismos cuatro articulos. La relevancia va de 3 (perfecto) a 0.
for lista in ([3, 0, 2, 1], [2, 0, 3, 1]):
    precision2 = sum(1 for r in lista[:2] if r > 0) / 2
    print(lista, "precision@2", round(precision2, 2), "NDCG@4", round(float(ndcg(lista)), 4))
# -> [3, 0, 2, 1] precision@2 0.5 NDCG@4 0.9508
# -> [2, 0, 3, 1] precision@2 0.5 NDCG@4 0.7379
```

```python ilustrativo
# El modelo de factorizacion con sesgos, en la practica. En produccion se usa una
# libreria especializada (implicit, LightFM, Surprise) o un modelo de dos torres.
# Aqui solo se muestra el bucle de descenso de gradiente, sobre datos que no tenemos.
import numpy as np

def entrenar(R, f=20, epocas=30, lr=0.01, lam=0.05):
    mu = np.nanmean(R)                          # media de lo observado: los huecos no cuentan
    b_u = np.zeros(R.shape[0]); b_i = np.zeros(R.shape[1])
    P = np.random.default_rng(0).normal(0, 0.1, (R.shape[0], f))
    Q = np.random.default_rng(1).normal(0, 0.1, (R.shape[1], f))
    for _ in range(epocas):
        for u, i in zip(*np.where(~np.isnan(R))):    # cada par (usuario, producto) con nota
            e = R[u, i] - (mu + b_u[u] + b_i[i] + P[u] @ Q[i])
            b_u[u] += lr * (e - lam * b_u[u])
            b_i[i] += lr * (e - lam * b_i[i])
            P[u]  += lr * (e * Q[i] - lam * P[u])
            Q[i]  += lr * (e * P[u] - lam * Q[i])
    return mu, b_u, b_i, P, Q
```

## Errores típicos

- **Evaluar con RMSE y desplegar por ranking.** El error cuadrático premia acertar la nota media
  de los productos populares, que es justo lo que no quieres recomendar. Un modelo con mejor
  RMSE puede tener peor `NDCG@10`. Si el producto final es una lista ordenada, mide con métricas
  de ranking, como en [[metricas-de-ranking]], y con el mismo `k` y el mismo catálogo de
  candidatos: `precision@5` y `precision@20` no son comparables.
- **Barajar las interacciones al dividir.** Si eliges el 20 % de las valoraciones al azar para
  probar, estás usando datos del futuro para predecir el pasado en un sistema real. Divide por
  fecha: entrena con todo lo anterior a una fecha y prueba con lo posterior.
- **Ignorar el baseline de popularidad.** Recomendar los 10 productos más vendidos suele ser un
  rival sorprendentemente duro. Si tu modelo no lo supera, no hay modelo.
- **No separar el arranque en frío.** Un usuario con cero interacciones no tiene filtrado
  colaborativo posible: necesita popularidad, contenido o preguntas explícitas. Mézclalo en la
  misma métrica y el resultado global esconderá que a los nuevos les recomiendas ruido.
- **Sesgo de exposición.** El modelo solo aprende de lo que se mostró. Los productos que nunca
  salieron en la lista no tienen datos, así que nunca mejorarán: el sistema se cierra sobre sí
  mismo. Se corrige con exploración deliberada y con [[ab-testing]].
- **Recomendar lo que el usuario ya tiene.** Es el error más visible y el más frecuente al
  montar el primer prototipo: hay que filtrar lo ya consumido, y decidir explícitamente si se
  permite repetir en productos de compra recurrente.

:::practica
enunciado: Dos listas de cuatro productos tienen las mismas relevancias (3, 0, 2, 1) y (3, 0, 1, 2). Las dos dan precision@2 = 0,5. Calcula el NDCG@4 de cada una y decide cuál presentar.
pista: Usa (2^rel − 1) / log2(i + 1) en cada posición i y divide entre el DCG del orden ideal 3, 2, 1, 0, que vale 9,393.
solucion: Lista A: 7/1 + 0/1,585 + 3/2 + 1/2,322 = 7 + 0 + 1,5 + 0,431 = 8,931; NDCG@4 = 8,931/9,393 = 0,951. Lista B: 7/1 + 0 + 1/2 + 3/2,322 = 7 + 0,5 + 1,292 = 8,792; NDCG@4 = 8,792/9,393 = 0,936. Presenta la A: con la misma precisión@2 coloca el producto más relevante antes, y NDCG lo detecta.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué se centran las valoraciones por producto antes de predecir?
o: Para que todos los productos tengan la misma media y sea más fácil compararlos
o: Para separar el sesgo del producto del gusto del usuario, y que un usuario generoso no arrastre la predicción
o: Porque el coseno solo funciona con datos centrados
a: 2
e: Centrar mide cada nota como desviación respecto a la media del producto. Así un 5 en un producto que recibe 4,5 de media no cuenta como un 5 en uno que recibe 1,5. En el ejemplo, la predicción pasa de 3,872 a 3,373 por este motivo. El coseno funciona igual con datos sin centrar, pero mide otra cosa.
:::

:::quiz
p: Dos listas de recomendaciones tienen precisión@2 = 0,5. ¿Qué puede diferenciarlas?
o: Nada: si la precisión es la misma, son equivalentes
o: El NDCG, porque tiene en cuenta la posición y la relevancia de cada producto
o: El número de usuarios a los que se ha recomendado
a: 2
e: precisión@2 solo cuenta cuántos relevantes hay entre los dos primeros, no dónde está el más relevante. Con relevancias 3, 0, 2, 1 el NDCG@4 es 0,9508 y con 2, 0, 3, 1 es 0,7379: el producto muy relevante en el puesto 3 penaliza. El número de usuarios no forma parte de la métrica.
:::

:::quiz
p: Un usuario acaba de registrarse y no ha valorado nada. ¿Qué se le puede recomendar?
o: Nada hasta que valore al menos diez productos
o: Lo más popular, productos por contenido declarado en el registro, o pedirle unas preferencias explícitas
o: Productos aleatorios, para explorar sus gustos
a: 2
e: Sin interacciones no hay similitud con nadie, así que el filtrado colaborativo no tiene de dónde tirar. Las salidas son la popularidad segmentada, el contenido del perfil y las preguntas explícitas. El azar puro desperdicia las primeras impresiones, que son las que más pesan para que el usuario vuelva.
:::

:::nota
Los sistemas de recomendación se evalúan casi siempre con datos históricos, y los datos
históricos están sesgados por lo que el sistema anterior mostró. Un `NDCG` alto en histórico
significa «sé imitar al recomendador viejo», no «voy a gustar más». La única prueba de verdad es
un experimento en vivo con un grupo de control.
:::
