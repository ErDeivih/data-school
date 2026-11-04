---
id: metricas-de-clustering
titulo: Métricas de clustering
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [k-means, clustering-jerarquico, dbscan-y-hdbscan]
tags: [clustering, metricas, no-supervisado, validacion]
resumen: Sin etiquetas no hay exactitud que calcular, así que un agrupamiento se juzga por su geometría con silueta, Davies-Bouldin, Calinski-Harabasz, gap y DBCV.
fuentes: ["Rousseeuw (1987), 'Silhouettes: A graphical aid to the interpretation and validation of cluster analysis'", "Kaufman y Rousseeuw (1990), 'Finding Groups in Data: An Introduction to Cluster Analysis'", "Davies y Bouldin (1979), 'A Cluster Separation Measure'", "Caliński y Harabasz (1974), 'A Dendrite Method for Cluster Analysis'", "Tibshirani, Walther y Hastie (2001), 'Estimating the number of clusters in a data set via the gap statistic'", "Moulavi et al. (2014), 'Density-Based Clustering Validation'"]
---

## En una frase

Sin etiquetas no hay exactitud que calcular, así que un agrupamiento se juzga por su geometría: la
silueta mira cada punto, Davies-Bouldin y Calinski-Harabasz resumen compacidad y separación en un
número, el estadístico de gap compara tu compacidad con la del ruido uniforme y DBCV hace lo mismo
con densidades.

## La idea

Tienes que repartir a 300 alumnos en grupos de trabajo y nadie te ha dicho quién es amigo de
quién. Un reparto es bueno si cada alumno queda rodeado de gente parecida a él, y es malo si a
alguien le ha tocado un grupo en el que no encaja con nadie. No puedes comprobar si acertaste,
pero sí puedes medir eso: **cuánto se parece cada punto a los de su grupo comparado con los del
grupo de al lado**. Esa medida, promediada, es la silueta.

La silueta se calcula **punto a punto**, y de ahí salen dos lecturas distintas: el promedio dice
si la partición entera es defendible, y el gráfico de barras dice **qué puntos concretos** están
en el grupo equivocado. Un promedio decente puede esconder un grupo entero en negativo, y ese
grupo suele ser el más interesante: o es un grupo real que el algoritmo no ha sabido separar, o
es un cajón de sastre donde han caído los puntos que no encajan en ningún sitio.

Davies-Bouldin y Calinski-Harabasz resumen lo mismo en un solo número, para comparar de un vistazo
muchos valores de `k`, pero se apoyan en el centroide y en la distancia euclídea: premian los
grupos redondos y mienten con las formas alargadas o anidadas.

Y hay una pregunta que las tres esquivan: **¿existe más de un grupo?**. Como dividir siempre
aumenta la compacidad, siempre habrá un `k` con mejor nota, y si tus datos son una nube uniforme
sin estructura la silueta no te avisará: te dará un máximo y tú lo interpretarás. Para eso está el
**estadístico de gap** (Tibshirani, Walther y Hastie, 2001), que compara tu compacidad con la que
conseguirías agrupando ruido uniforme con el mismo `k`. Si tus datos no son más compactos que el
ruido, el gap se queda plano o negativo y la conclusión honesta es que no había grupos.

Queda el caso de los grupos que no son bolas: dos lunas entrelazadas, un anillo con un núcleo, una
banda alargada. Ahí [[dbscan-y-hdbscan|DBSCAN]] o el
[[clustering-jerarquico|clustering jerárquico]] encuentran lo que [[k-means|K-means]] no ve, pero
las métricas basadas en centroides castigarán esa solución correcta. Para eso existe **DBCV**
(Moulavi y coautores, 2014): mide la densidad dentro de cada grupo y la separación a través de las
zonas vacías, sin suponer ninguna forma.

Las cinco métricas miden **geometría**, no utilidad: sirven para descartar particiones y para
detectar puntos mal colocados, no para justificar una decisión. Un agrupamiento con silueta 0,7
puede ser inútil para tu pregunta de negocio.

## Definición formal

Con `n` puntos, `k` grupos, `n_i` puntos en el grupo `i` y `d(a, b)` la distancia euclídea entre
dos puntos:

:::formula
s(i) = (b(i) − a(i)) / max(a(i), b(i))          silueta = (1/n) · Σ s(i)
:::

- `a(i)` — distancia media del punto `i` a los demás de su propio grupo (cohesión).
- `b(i)` — distancia media del punto `i` a los del grupo ajeno más cercano (separación).
- `s(i)` — entre −1 y 1: vale 1 si está mucho más cerca de los suyos, ronda 0 en la frontera y es
  negativo si estaría mejor en el grupo de al lado. Un grupo de un solo punto tiene silueta 0.

:::formula
Davies-Bouldin = (1/k) · Σ_i max_{j≠i} (S_i + S_j) / M_ij
:::

- `S_i` — dispersión del grupo `i`: distancia media de sus puntos a su centroide.
- `M_ij` — distancia entre los centroides de los grupos `i` y `j`.
- Cuanto **más bajo**, mejor; 0 es el mínimo teórico y no tiene unidades.

:::formula
Calinski-Harabasz = [ tr(B) / (k − 1) ] / [ tr(W) / (n − k) ]
:::

- `tr(B)` — dispersión **entre** grupos: distancias al cuadrado de cada centroide al centroide
  global, ponderadas por el tamaño del grupo.
- `tr(W)` — dispersión **dentro** de los grupos: distancias al cuadrado de cada punto a su
  centroide.
- Cuanto **más alto**, mejor, y sin cota superior: solo se compara dentro del mismo conjunto de
  datos.

:::formula
Gap(k) = (1/B) · Σ_b log(W_k^b) − log(W_k)
:::

- `W_k` — dispersión interna agrupada de tus datos con `k` grupos.
- `W_k^b` — la misma cantidad en el conjunto de referencia `b`, hecho de puntos uniformes en la caja
  que ocupan tus datos; `B` es cuántos de esos conjuntos se generan.
- Se elige el `k` **más pequeño** que cumple `Gap(k) ≥ Gap(k+1) − s_{k+1}`, con `s_{k+1}` la
  desviación típica de los `log(W_{k+1}^b)`: el primer `k` en el que añadir un grupo más ya no
  aporta una mejora clara.

:::formula
DBCV = Σ_i (n_i / n) · (DSPC_i − DSC_i) / max(DSPC_i, DSC_i)
:::

- `DSC_i` — densidad interna del grupo `i`: la arista más larga de su árbol de recubrimiento
  mínimo, calculado con **distancias de alcanzabilidad mutua**, que nunca son menores que la
  distancia de cada punto a su vecino número `k`.
- `DSPC_i` — separación: la arista más corta que conectaría el grupo `i` con el ajeno más cercano
  en ese mismo árbol.
- Cada grupo aporta `(DSPC_i − DSC_i) / max(DSPC_i, DSC_i)`, entre −1 y 1, y DBCV es la media
  ponderada por el tamaño. Vale 1 cuando los grupos son densos por dentro y están separados por
  zonas vacías.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `a(i)` | Distancia media del punto `i` a los de su propio grupo | las de las variables | Sube cuando el grupo es ancho o alargado, y con ella baja la silueta de ese punto. Un grupo de un solo punto tiene `a = 0` por convenio y silueta 0 |
| `b(i)` | Distancia media del punto `i` al grupo ajeno más cercano | las de las variables | Sube cuando los grupos están lejos entre sí y empuja la silueta hacia 1. Si el grupo vecino está pegado, `b` baja y la barra de ese punto se hunde |
| `s(i)` | Silueta del punto: cuánto mejor está en su grupo que en el vecino | adimensional, entre −1 y 1 | Es el resultado. Por debajo de 0 ese punto está mal asignado. El promedio resume la partición, pero solo es comparable entre particiones del mismo dato y la misma escala |
| `k` | Número de grupos que se piden | grupos (entero) | La silueta no baja ni sube por sistema: tiene un máximo, casi siempre en 2 o 3, porque dividir siempre aumenta la compacidad. Davies-Bouldin tiene un mínimo y Calinski-Harabasz un máximo, y no siempre coinciden |
| `S_i` | Dispersión del grupo `i`: distancia media de sus puntos a su centroide | las de las variables | Entra sumando en Davies-Bouldin, así que un grupo ancho empeora el índice. La media no es robusta: un solo atípico alejado infla `S_i` y hunde la nota de un grupo que estaba bien |
| `M_ij` | Distancia entre los centroides de los grupos `i` y `j` | las de las variables | Está en el denominador: si dos grupos están pegados, `M_ij` es pequeño y Davies-Bouldin se dispara. Es la señal de que sobra un grupo, o de que los dos que tienes son en realidad uno |
| `tr(B)` y `tr(W)` | Dispersión entre grupos y dentro de los grupos | unidades² | Calinski-Harabasz es su cociente corregido por grados de libertad. Al añadir variables que no informan, `tr(W)` crece y el índice baja: es una forma cómoda de detectar ruido mal escalado |
| `W_k` | Dispersión interna agrupada con `k` grupos | unidades² | Baja siempre al subir `k` y vale 0 con `k = n`, por eso el gap no la minimiza: la compara en escala logarítmica con la del ruido uniforme |
| `B` | Cuántos conjuntos de ruido uniforme se generan | conjuntos (entero) | Más referencias dan un gap y una `s` más estables a cambio de tiempo de cómputo: con 10 el resultado ya orienta, con 50 apenas se mueve |
| `DSC_i` y `DSPC_i` | Densidad interna y separación del grupo `i` según DBCV | las de las variables | Si `DSC_i` supera a `DSPC_i`, el grupo es más ancho que la distancia al vecino y su validez es negativa: DBCV está diciendo que ese grupo no está separado de nada |
:::

:::figura
fichero: metricas-de-clustering-silueta
pie: El mismo dato de tres grupos bien separados, agrupado con el número de grupos correcto (izquierda) y con el doble (derecha). Cada barra es un punto: su longitud es la silueta de ese punto y el color, el grupo al que ha ido a parar; la línea de puntos es la media de todo el conjunto. Con k = 3 no hay ni una barra a la izquierda del cero y la media es 0,711. Con k = 6 la media cae a 0,404 y dos barras cruzan el cero: esos dos puntos están más cerca del grupo de al lado que del suyo. Ese es el uso principal de la silueta, encontrar los puntos que el algoritmo ha colocado mal, y por eso se mira el gráfico y no solo el promedio.
fuente: figuras/metricas-de-clustering-1.py
:::

## Ejemplo

Cuatro puntos en las esquinas de un rectángulo: `(0,0)`, `(0,2)`, `(10,0)` y `(10,2)`. Hay dos
particiones posibles, cortar por la vertical (izquierda y derecha) o por la horizontal (arriba y
abajo). Los números se pueden seguir a mano.

**Cortando por x**: los grupos son `{(0,0), (0,2)}` y `{(10,0), (10,2)}`.

- Para `(0,0)`: `a = 2` (la distancia a su compañero) y `b = (10 + 10,198)/2 = 10,099` (la media a
  los dos puntos del otro grupo; una distancia es 10 y la otra `√(10² + 2²) = 10,198`). Entonces
  `s = (10,099 − 2)/10,099 = 0,802`.
- `S_A = S_B = 1`, porque cada punto está a distancia 1 de su centroide, y `M = 10`. Davies-Bouldin
  `= (1/2) · [(1+1)/10 + (1+1)/10] = 0,2`.
- Calinski-Harabasz: entre grupos `2·(0−5)² + 2·(10−5)² = 100`; dentro, `4 · 1² = 4`. El índice es
  `(100/1) / (4/2) = 50`.

**Cortando por y**: los grupos son `{(0,0), (10,0)}` y `{(0,2), (10,2)}`.

- Para `(0,0)`: `a = 10` y `b = (2 + 10,198)/2 = 6,099`, luego `s = (6,099 − 10)/max(10; 6,099) = −0,390`:
  negativo, porque ese punto está más cerca de los dos de arriba que de su propio compañero.
- `S_A = S_B = 5` y `M = 2`, luego Davies-Bouldin `= (1/2) · [(5+5)/2 + (5+5)/2] = 5`.
- Calinski-Harabasz: centroides `(5,0)` y `(5,2)`, global `(5,1)`; entre grupos `2·1 + 2·1 = 4` y
  dentro `4 · 25 = 100`, luego `(4/1) / (100/2) = 0,08`.

Las tres métricas eligen la partición por x. Fíjate en las escalas: Davies-Bouldin pasa de 0,2 a 5
y Calinski-Harabasz de 50 a 0,08, pero esos números no significan nada por sí solos, solo valen
comparados con los de otra partición **del mismo dato**. La silueta es la única con lectura
absoluta: por encima de 0 el punto está donde debe. Como orientación muy gruesa se suele decir que
una silueta media por encima de 0,7 indica estructura clara, entre 0,5 y 0,7 es razonable, entre
0,25 y 0,5 es débil y por debajo de 0,25 no hay nada que sostener; son bandas prácticas, no un
contraste de hipótesis.

## Código

```python verificable
import numpy as np
from sklearn import metrics

# Cuatro puntos en las esquinas de un rectangulo: dos particiones posibles.
X = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0]])
por_x = np.array([0, 0, 1, 1])          # {(0,0),(0,2)} y {(10,0),(10,2)}
por_y = np.array([0, 1, 0, 1])          # {(0,0),(10,0)} y {(0,2),(10,2)}

for nombre, et in (("cortando por x", por_x), ("cortando por y", por_y)):
    print(nombre,
          "silueta", round(metrics.silhouette_score(X, et), 3),
          "davies", round(metrics.davies_bouldin_score(X, et), 3),
          "calinski", round(metrics.calinski_harabasz_score(X, et), 3))
# -> cortando por x silueta 0.802 davies 0.2 calinski 50.0
# -> cortando por y silueta -0.39 davies 5.0 calinski 0.08
print("silueta punto a punto:", np.round(metrics.silhouette_samples(X, por_y), 4))
# -> silueta punto a punto: [-0.3901 -0.3901 -0.3901 -0.3901]
```

:::claves
- `silhouette_score` devuelve **un float**, no una Serie ni un array: la media de las siluetas de todos los puntos. Si quieres las de cada punto, la función es `silhouette_samples`, con la misma firma, y devuelve un array de longitud `n` en el mismo orden que las filas de `X`.
- Las tres funciones devuelven valores con **escalas incomparables**: la silueta está entre −1 y 1, Davies-Bouldin no tiene cota (0 es el mínimo y solo se alcanza con grupos de un punto o perfectamente compactos) y Calinski-Harabasz no tiene cota superior. Nunca compares un 0,4 de una con un 0,4 de otra.
- `davies_bouldin_score` y `calinski_harabasz_score` lanzan `ValueError` si solo hay un grupo, y `silhouette_score` también: no tienen sentido con `k = 1`. Si estás recorriendo valores de `k` en un bucle, empieza en 2.
- `silhouette_score(X, et)` recibe las etiquetas como segundo argumento y **no** un modelo ajustado. El orden de las etiquetas importa: la fila `i` de `X` tiene que corresponder a `et[i]`. Un `DataFrame` con el índice barajado y las etiquetas en otro orden da un número perfectamente plausible y completamente falso.
- Las tres usan distancia euclídea sobre `X` tal cual. Si una variable está en euros y otra en metros, la de rango mayor decide todo el cálculo: hay que [[escalado-y-transformacion|escalar antes]], exactamente igual que antes de agrupar.
- `silhouette_score` con `metric="precomputed"` acepta una matriz de distancias en lugar de los datos. Es la vía para usar distancias que no sean euclídeas, pero entonces `X` tiene que ser la matriz de distancias completa, no los puntos.
:::

```python verificable
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=60, centers=[(0, 0), (5, 0), (0, 5)], cluster_std=0.5, random_state=0)

def w_k(datos, k, arranques=1):
    """Dispersion interna agrupada: lo que K-means minimiza, sin el factor 2n."""
    et = KMeans(n_clusters=k, n_init=arranques, random_state=0).fit_predict(datos)
    return sum(((datos[et == g] - datos[et == g].mean(0)) ** 2).sum() / (2 * (et == g).sum())
               for g in range(k))

azar = np.random.default_rng(0)
minimo, maximo = X.min(0), X.max(0)          # la caja que ocupan los datos
ks = [1, 2, 3, 4, 5]
gap, s = {}, {}
for k in ks:
    real = np.log(w_k(X, k, 5))              # tus datos, con varios arranques
    ref = np.array([np.log(w_k(azar.uniform(minimo, maximo, X.shape), k)) for _ in range(10)])
    gap[k], s[k] = ref.mean() - real, ref.std(ddof=1) * np.sqrt(1 + 1 / len(ref))
    print(f"k={k}  logW {real:7.3f}  gap {gap[k]:6.3f}  s {s[k]:5.3f}")
# -> k=1  logW   1.746  gap -0.398  s 0.109
# -> k=2  logW   1.088  gap  0.455  s 0.141
# -> k=3  logW  -0.374  gap  1.763  s 0.129
# -> k=4  logW  -0.311  gap  1.549  s 0.131
# -> k=5  logW  -0.226  gap  1.468  s 0.079

# Regla de Tibshirani: el k mas pequeno que ya no mejora lo suficiente.
elegido = min(k for k in ks[:-1] if gap[k] >= gap[k + 1] - s[k + 1])
print("regla del gap: k =", elegido)              # -> regla del gap: k = 3
```

:::claves
- El gap de `k = 1` sale **negativo**, y no es un error: la caja que ocupan tres grupos separados es más ancha que los propios grupos, así que el ruido uniforme repartido por esa caja está más disperso que tus datos. El valor absoluto del gap no se interpreta; lo que se lee es dónde está el máximo y dónde se cumple la regla.
- `W_k` se define con el factor `1/(2·n_i)`, que es la mitad de la suma de cuadrados dentro del grupo. Ese factor se cancela en el cociente del gap, así que el código lo deja puesto solo para ser fiel a la fórmula; quitar el `2 *` no cambia ninguna conclusión.
- La regla se escribe con `s_{k+1}` en el lado derecho, no con `s_k`. Es el término que absorbe el ruido de la simulación: sin él, cualquier diferencia de milésimas elegiría un `k` distinto en cada ejecución.
- `azar.uniform(minimo, maximo, X.shape)` genera puntos uniformes en la **caja** definida por el mínimo y el máximo de cada variable. La implementación original gira antes los datos con un [[pca|análisis de componentes principales]] para que la caja no dependa de la orientación de los ejes; con datos ya centrados y sin correlación, da igual.
- El parámetro `arranques` es una concesión a la velocidad: `w_k` se llama decenas de veces, y las referencias de ruido no necesitan diez arranques porque no tienen estructura que encontrar. Con tus datos sí conviene subirlo, porque K-means no garantiza el óptimo: con 5 arranques, el `logW` de `k = 4` sale −0,311, y con 10 sale −0,358 (más bajo, mejor partición). Ese mínimo local que se cuela a veces es exactamente lo que mide `n_init`.
- `gap` y `s` son diccionarios y no listas porque se indexan por el valor de `k`, y así `gap[k + 1]` se lee igual que en la fórmula. Con listas habría que llevar la cuenta de la posición y el código se vuelve ilegible.
:::

```python verificable
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import make_moons

def mst(matriz):
    """Arbol de recubrimiento minimo, simetrizado (scipy lo guarda en un triangulo)."""
    m = minimum_spanning_tree(matriz).toarray()
    return np.maximum(m, m.T)

def dbcv(X, et, k=5):
    """Validez por densidad (Moulavi et al., 2014): 1 = grupos densos y separados."""
    D = squareform(pdist(X))
    nucleo = np.sort(D, axis=1)[:, min(k, len(X) - 1)]        # al vecino k-esimo
    mrd = np.maximum(D, np.maximum(nucleo[:, None], nucleo[None, :]))
    np.fill_diagonal(mrd, 0.0)
    grupos = np.unique(et)
    dsc = {g: mst(mrd[np.ix_(et == g, et == g)]).max() for g in grupos}
    dspc = {}
    for g in grupos:
        cortes = []
        for h in grupos:
            if h == g:
                continue
            idx = np.r_[np.where(et == g)[0], np.where(et == h)[0]]
            cruce = mst(mrd[np.ix_(idx, idx)])[:np.sum(et == g), np.sum(et == g):]
            cortes.append(cruce[cruce > 0].min())            # solo aristas que existen
        dspc[g] = min(cortes) if cortes else np.inf
    val = [(dspc[g] - dsc[g]) / max(dspc[g], dsc[g]) for g in grupos]
    return float(np.average(val, weights=[np.sum(et == g) for g in grupos]))

X4 = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0]])
print("rectangulo por x:", round(dbcv(X4, np.array([0, 0, 1, 1]), k=1), 3))   # -> 0.8
print("rectangulo por y:", round(dbcv(X4, np.array([0, 1, 0, 1]), k=1), 3))   # -> -0.8

X, verdad = make_moons(n_samples=400, noise=0.06, random_state=0)
kmeans = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X)
print("lunas de verdad  silueta %.3f  dbcv %.3f"
      % (metrics.silhouette_score(X, verdad), dbcv(X, verdad)))
# -> lunas de verdad  silueta 0.330  dbcv 0.330
print("lunas por k-means silueta %.3f  dbcv %.3f"
      % (metrics.silhouette_score(X, kmeans), dbcv(X, kmeans)))
# -> lunas por k-means silueta 0.489  dbcv -0.789
```

:::claves
- En el rectángulo, DBCV sale exactamente `+0,8` y `−0,8`: con dos puntos por grupo y `k = 1`, las distancias de alcanzabilidad mutua son 2 dentro de cada grupo y 10 entre grupos, así que `(10 − 2)/10 = 0,8`. Es la comprobación de que la implementación hace lo que dice la fórmula.
- `k=1` en la llamada a `dbcv` no es el número de grupos: es el vecino que define el **núcleo** de densidad. Con cuatro puntos, `min(k, n−1)` lo deja en 1 y el cálculo no revienta; con `k = 5` y cuatro puntos, `np.sort(D, axis=1)[:, 5]` daría `IndexError`.
- `np.fill_diagonal(mrd, 0.0)` es imprescindible: la distancia de un punto a sí mismo es 0, y `minimum_spanning_tree` interpreta los ceros como «no hay arista». Sin poner a cero la diagonal, `np.maximum` deja el núcleo en la diagonal y el árbol sale mal.
- `minimum_spanning_tree` devuelve el árbol con cada arista en **un solo triángulo** de la matriz. Por eso hace falta `np.maximum(m, m.T)` antes de buscar aristas: sin simetrizar, la mitad de las aristas se leen como 0 y el mínimo del cruce sale 0 siempre.
- `cruce[cruce > 0]` filtra las posiciones que no son aristas. Un `.min()` a secas incluiría esos ceros y devolvería 0, y entonces DBCV valdría 0 para cualquier partición: es el fallo más fácil de cometer y el más difícil de ver.
- La silueta prefiere el corte de K-means (0,489 frente a 0,330) y DBCV prefiere el correcto (0,330 frente a −0,789). Ninguna de las dos mira las etiquetas: la primera mide distancias a los vecinos y la segunda, densidad. Ese es el motivo de tener las dos en el cajón.
:::

:::figura
fichero: metricas-de-clustering-densidad
pie: Dos lunas entrelazadas, el caso clásico en el que K-means no puede acertar porque su frontera es una recta. A la izquierda, la partición correcta: cada luna es un grupo. A la derecha, lo que corta K-means con k = 2: parte el plano por la mitad y trocea las dos lunas. La silueta prefiere el corte equivocado (0,489 frente a 0,330), porque ve dos manchas compactas en lugar de dos formas alargadas. DBCV, que mide densidad dentro y separación a través de las zonas vacías, prefiere la partición correcta (0,330 frente a −0,789). Si tu agrupamiento es de este tipo, mira DBCV y no la silueta.
fuente: figuras/metricas-de-clustering-2.py
:::

## Errores típicos

- **Elegir `k` con la métrica y creerte que ese es el número de grupos.** Todas devuelven un
  ganador para cada `k` que pruebes, así que la pregunta no es «¿cuál es el mejor `k`?» sino «¿la
  estructura que veo se sostiene?». Un máximo de la silueta en `k = 4` puede ser dos grupos reales
  partidos por la mitad.
- **Usar Davies-Bouldin o Calinski-Harabasz con grupos que no son bolas.** Las dos se calculan con
  centroides y distancias euclídeas, así que una agrupación por densidad correcta saca un
  Davies-Bouldin malísimo. Con formas raras, la métrica que corresponde es DBCV.
- **Comparar la misma métrica entre conjuntos de datos distintos.** Calinski-Harabasz no tiene
  unidades ni cota: un 250 en un dataset y un 90 en otro no dicen nada el uno del otro. Y la
  silueta se degrada sola al añadir dimensiones, porque en dimensión alta todas las distancias se
  parecen ([[maldicion-de-la-dimensionalidad|maldición de la dimensionalidad]]).
- **Mirar solo la media.** Un conjunto con silueta media 0,55 puede tener un grupo de 40 puntos con
  todas las barras en negativo: eso no es un grupo, es donde han ido a parar los puntos que no
  encajan. Dibuja el gráfico por punto y mira el grupo peor.
- **Calcular las métricas sin escalar.** Si una variable se mide en decenas de miles y otra entre 0
  y 1, todas las distancias las decide la primera y el resto no existe para la métrica. Es el mismo
  error que agrupar sin escalar, disfrazado de número objetivo.
- **Elegir `k` y valorar el resultado con los mismos datos.** La métrica se calcula sobre los datos
  que has usado para agrupar, así que siempre es optimista. Para una estimación honesta, mide la
  estabilidad agrupando submuestras, con la lógica de la [[validacion-cruzada|validación cruzada]].

:::trampa
Ordenar los grupos por su silueta media y quedarte con los buenos es una tentación, pero cambia la
pregunta: ya no estás validando una partición, estás construyendo otra. Si descartas el grupo malo,
las etiquetas del resto siguen siendo las mismas y los números que acabas de calcular dejan de
describir lo que tienes entre manos. Decide antes qué vas a hacer con los puntos que no encajan, y
si la respuesta es «dejarlos fuera», el modelo que buscas es [[dbscan-y-hdbscan|DBSCAN]], que tiene
una etiqueta de ruido explícita.
:::

:::practica
enunciado: Con los cuatro puntos del rectángulo del ejemplo, calcula a mano la silueta del punto (10,0) en la partición por y, y explica por qué Davies-Bouldin vale 5 en esa partición y 0,2 en la partición por x.
pista: En la partición por y tu grupo es {(0,0),(10,0)} y el grupo ajeno {(0,2),(10,2)}. Para Davies-Bouldin, fíjate en la distancia que va en el denominador.
solucion: Para (10,0): a = 10, la distancia a su compañero (0,0); b = (10,198 + 2)/2 = 6,099, la media de las distancias a (0,2) y a (10,2). Entonces s = (6,099 − 10)/max(10, 6,099) = −0,390, negativo, porque (10,0) está más cerca del punto (10,2) de arriba que de su propio compañero. Los cuatro puntos dan lo mismo por simetría: es el −0,3901 que imprime scikit-learn. Davies-Bouldin usa la distancia entre centroides, no entre puntos: los centroides (5,0) y (5,2) distan 2 y las dispersiones internas valen 5 cada una, luego (5+5)/2 = 5. En la partición por x los centroides distan 10 y las dispersiones valen 1, luego (1+1)/10 = 0,2.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes una silueta media de 0,62 con k = 3 y de 0,58 con k = 4. ¿Qué concluyes?
o: Que el número de grupos es 3, porque es el que da la silueta más alta
o: Que 3 y 4 son prácticamente igual de defendibles y hay que mirar los dos gráficos por punto antes de decidir
o: Que hay exactamente 3 grupos en los datos
a: 2
e: Una diferencia de 0,04 está dentro del ruido de la propia métrica: no es un criterio para decidir. La silueta compara particiones que tú has construido, y si las dos son parecidas hay que mirar qué puntos cambian de grupo, si los grupos nuevos tienen sentido para el problema y si se repiten en submuestras. Lo que no puede hacer ninguna métrica es decirte cuántos grupos hay de verdad en los datos.
:::

:::quiz
p: Aplicas K-means con k = 2 a las dos lunas entrelazadas y obtienes silueta 0,489. Aplicas un método de densidad, que recupera las dos lunas de verdad, y esa partición correcta saca silueta 0,330. ¿Qué ha pasado?
o: Que el método de densidad ha agrupado mal y la silueta lo detecta
o: Que la silueta mide distancias euclídeas y premia las manchas redondeadas, así que el corte recto de K-means le parece mejor
o: Que la silueta solo funciona con K-means
a: 2
e: La silueta compara la distancia media dentro del grupo con la del grupo vecino. K-means parte las lunas en dos trozos compactos y la distancia entre esos trozos es grande, así que sale bien parada. La partición correcta son dos formas alargadas que se enganchan, y muchos de sus puntos tienen al grupo contrario cerca. Para formas no convexas hace falta una métrica de densidad como DBCV.
:::

:::quiz
p: El estadístico de gap para k = 1 vale −0,398. ¿Cómo se interpreta?
o: Que el ruido uniforme está más disperso que los datos con un solo grupo, y que el valor absoluto no significa nada: se lee dónde está el máximo y dónde se cumple la regla
o: Que hay un error en el cálculo, porque el gap no puede ser negativo
o: Que hay exactamente un grupo en los datos
a: 1
e: El gap compara la dispersión de tus datos con la de puntos uniformes repartidos en la caja que ocupan. Si tus grupos están separados y ocupan mucho espacio, la caja es más ancha que los grupos y el ruido sale más disperso: gap negativo. Lo que se interpreta es la forma de la curva y la regla Gap(k) ≥ Gap(k+1) − s(k+1), no el signo de cada valor.
:::

:::nota
Ninguna de estas métricas necesita etiquetas, pero todas necesitan una **decisión previa** que sí
es tuya: la escala de las variables y la distancia. Cambiar de euclídea a coseno, o estandarizar
en vez de normalizar, puede cambiar el ganador. Deja escritas esas dos decisiones junto al
resultado, porque sin ellas el número no es reproducible.
:::
