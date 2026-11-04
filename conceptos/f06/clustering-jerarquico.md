---
id: clustering-jerarquico
titulo: Clustering jerárquico
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [norma-y-distancias, k-means, correlacion-pearson-spearman]
tags: [clustering, dendrograma, enlace, no-supervisado]
resumen: Construir un árbol de agrupaciones de abajo arriba, elegir el criterio de enlace y decidir el número de grupos cortando el dendrograma a la altura adecuada.
fuentes: ["Sneath y Sokal (1973), 'Numerical Taxonomy'", "Murtagh y Contreras (2012), 'Algorithms for Hierarchical Clustering'", "Ward (1963), 'Hierarchical Grouping to Optimize an Objective Function'"]
---

## En una frase

El clustering jerárquico no te da una partición, te da **todas**: empieza con cada punto en su
propio grupo, va fusionando los dos grupos más parecidos hasta que queda uno, y guarda el
historial completo en un dendrograma que puedes cortar a la altura que quieras.

## La idea

Con [[k-means|K-means]] tienes que decidir `k` antes de empezar y el resultado cambia por
completo con esa decisión. El clustering jerárquico invierte el orden: construye **todo** el
árbol de agrupaciones y decides después dónde cortarlo. Si al mirar el gráfico ves que hay una
frontera natural en 3 grupos, cortas ahí; y si el negocio pide 5 segmentos, vuelves a cortar el
mismo dendrograma sin recalcular nada.

El proceso es mecánico. Tienes `n` puntos, cada uno su propio grupo. Calculas la distancia
entre todos los pares de grupos, fusionas los dos más cercanos y repites. Cada fusión queda
registrada con la altura a la que ocurrió, que es exactamente la distancia entre los dos
grupos que se unieron. Ese historial dibujado como árbol es el **dendrograma**.

La clave está en la primera pregunta: ¿qué es «la distancia entre dos grupos»? Ahí es donde
entra el **criterio de enlace**, y cambiar de criterio cambia el resultado por completo:

- **Enlace simple (single):** la distancia entre dos grupos es la del par de puntos más
  cercanos, uno de cada grupo. Tiende a encadenar grupos alargados y puede unir dos conjuntos
  muy separados a través de un puente de puntos intermedios.
- **Enlace completo (complete):** la distancia es la del par más lejano. Produce grupos
  compactos y de tamaño parecido, y es muy sensible a los atípicos.
- **Enlace promedio (average, UPGMA):** la media de todas las distancias entre pares. Es el
  compromiso entre los dos anteriores y el más usado como opción por defecto.
- **Ward:** en vez de una distancia entre puntos, mide cuánto aumenta la inercia interna al
  fusionar dos grupos. Minimizar eso equivale a buscar grupos lo más compactos y esféricos
  posible; es el criterio que más se parece a K-means y el que suele dar los resultados más
  interpretables con variables continuas escaladas.

El coste es la letra pequeña: hay que calcular la matriz de distancias completa, `n(n−1)/2`
valores, y guardarla. Con 10.000 puntos son casi 50 millones de distancias, unos 400 MB en
coma flotante de 64 bits. Con 100.000 puntos, el planteamiento se cae. Para eso hay variantes
sobre vecinos más cercanos o métodos pensados para muchas filas.

## Definición formal

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `D` | Matriz de distancias entre los `n` puntos | las de las variables | Es la entrada del método. Ocupa `n(n−1)/2` valores: con 10.000 puntos son unos 400 MB, y por eso el método se cae en conjuntos grandes |
| `d(a, b)` | Distancia entre dos puntos concretos | las de las variables | Es el ladrillo con el que se mide todo lo demás. Si las variables no están escaladas, la de mayor rango decide la distancia |
| `A`, `B` | Dos grupos ya formados que se plantean fusionar | conjuntos de puntos | Según crecen, su distancia mutua tiende a crecer y la fusión se hace a más altura. Ese crecimiento es lo que da forma al dendrograma |
| `nA`, `nB` | Número de puntos de cada grupo | puntos | Aparecen en el enlace promedio y en Ward: un grupo grande arrastra la media y puede fusionarse antes de lo que parece |
| `d(A, B)` enlace simple | Distancia entre grupos medida por el par más cercano | las de las variables | Da las fusiones más bajas y provoca encadenamiento: basta un puente de puntos para unir dos nubes separadas |
| `d(A, B)` enlace completo | Distancia entre grupos medida por el par más lejano | las de las variables | Da las fusiones más altas y grupos compactos, pero parte grupos alargados y es sensible a un solo punto lejano |
| `d(A, B)` enlace promedio | Media de todas las distancias entre los dos grupos | las de las variables | Queda en medio de los otros dos y suaviza los extremos: ni encadena tanto como el simple ni se rompe con un atípico como el completo |
| `Δ(A, B)` (Ward) | Cuánto empeora la compacidad global al fusionar `A` y `B` | unidades² | Se elige la fusión de `Δ` más pequeño, así que los grupos salen compactos y de tamaño parecido. Con grupos de tamaños muy distintos tiende a igualarlos |
| `/μA − μB/²` | Distancia al cuadrado entre los centroides de los dos grupos | unidades² | Es el motor de Ward: cuanto más lejos están los centros, más cuesta fusionarlos y más alta queda la unión |
| `h` | Altura a la que se corta el dendrograma | las de las variables | Subirlo reduce el número de grupos: cada fusión que queda por debajo del corte une dos grupos en uno. Es el mando para elegir cuántos grupos quieres |
:::

Sea `D` una matriz de distancias entre `n` puntos, `d(i, j) ≥ 0`, con `d(i, i) = 0`. Un
algoritmo jerárquico aglomerativo produce una secuencia de `n − 1` fusiones. La **altura** de
la fusión `t` es la distancia entre los dos grupos `A` y `B` que se unen en ese paso, según el
criterio de enlace:

:::formula
simple:   d(A, B) = min { d(a, b) : a ∈ A, b ∈ B }
completo: d(A, B) = max { d(a, b) : a ∈ A, b ∈ B }
promedio: d(A, B) = (1 / (nA · nB)) · Σ_{a∈A} Σ_{b∈B} d(a, b)
:::

- `A`, `B` — dos grupos de puntos ya formados.
- `a`, `b` — puntos concretos de cada grupo.
- `nA`, `nB` — número de puntos de cada grupo.
- `d(a, b)` — distancia entre dos puntos, normalmente euclídea.
- La altura de la fusión es el valor `d(A, B)` en el momento de unirlos.

En Ward, la cantidad a minimizar al fusionar `A` y `B` es el incremento de la suma de
cuadrados dentro de los grupos:

:::formula
Δ(A, B) = (nA · nB / (nA + nB)) · /μA − μB/²
:::

- `μA`, `μB` — centroides (medias) de cada grupo.
- `/μA − μB/²` — distancia euclídea al cuadrado entre los dos centroides.
- `Δ(A, B)` — cuánto empeora la compacidad global si esos dos grupos se juntan.

Cortar el dendrograma a una altura `h` produce los grupos cuyas fusiones tienen altura mayor
que `h`. Como las alturas del dendrograma son monótonas no decrecientes en los tres primeros
enlaces, un corte horizontal está bien definido; con otros criterios, no siempre.

## Ejemplo

Cuatro puntos en una recta: `P1 = 0`, `P2 = 1`, `P3 = 4`, `P4 = 9`. Las distancias entre
pares son: `d(1,2) = 1`, `d(1,3) = 4`, `d(2,3) = 3`, `d(1,4) = 9`, `d(2,4) = 8`, `d(3,4) = 5`.

- **Enlace simple.** Se fusionan P1 y P2 (altura 1). La distancia del grupo {P1, P2} a P3 es
  `min(4, 3) = 3`, y a P4 es `min(9, 8) = 8`: se fusiona con P3 a altura 3. Después
  {P1, P2, P3} con P4 a `min(9, 8, 5) = 5`. Alturas: **1, 3, 5**.
- **Enlace completo.** Tras unir P1 y P2 (altura 1), la distancia a P3 es `max(4, 3) = 4` y a
  P4 es `max(9, 8) = 8`: se une con P3 a altura 4. Y el conjunto con P4 a
  `max(9, 8, 5) = 9`. Alturas: **1, 4, 9**.
- **Enlace promedio.** Tras unir P1 y P2 (altura 1), la distancia a P3 es `(4 + 3)/2 = 3,5` y a
  P4 es `(9 + 8)/2 = 8,5`: se une con P3 a 3,5. Después, `(9 + 8 + 5)/3 = 7,33`. Alturas:
  **1, 3,5, 7,33**.

Fíjate en lo que cambia el criterio. Si cortas pidiendo grupos separados al menos 3 unidades, el
enlace simple ya ha fusionado `{P1, P2}` con P3 (su altura es 3, justo en el límite) y deja dos
grupos: `{P1, P2, P3}` y `{P4}`. El completo y el promedio todavía no, porque sus alturas son
1, 4 y 9 en un caso y 1, 3,5 y 7,33 en el otro: el corte deja tres grupos sueltos. Sube el corte
a 4 y los tres criterios coinciden en dos grupos, `{P1, P2, P3}` y `{P4}`. Mismos datos, criterio
distinto, respuesta distinta en el corte de 3.

Y el enlace simple tiene su trampa conocida: ha metido a P3 en un grupo donde P1 y P2 están a
distancia 1 entre sí y P3 está a 4 de P1. Es el encadenamiento típico que une grupos separados a
través de un puente.

## Código

:::figura
fichero: clustering-jerarquico-dendrograma-y-corte
pie: Los dos árboles son el mismo dato con la misma línea de corte a altura 2,5 y solo cambia el criterio de enlace. A la izquierda, el enlace simple mide la distancia entre grupos por el par de puntos **más cercano**, así que basta un puñado de puntos sueltos en medio para ir encadenando las dos nubes: el corte deja un solo grupo y las dos nubes han quedado fundidas. A la derecha, el enlace completo usa el par **más lejano** y ningún punto del puente puede entrar sin arrastrar a toda su nube: el mismo corte deja cuatro grupos. La última fusión está a 1,87 en un caso y a 7,64 en el otro, la misma distancia medida de dos maneras. Fíjate también en el eje vertical de la izquierda: está multiplicado por 4 solo para que el dibujo se vea, y esa es la pista de que el encadenamiento produce árboles aplastados, con casi todas las fusiones a alturas parecidas.
fuente: figuras/clustering-jerarquico-1.py
:::

```python verificable
import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

# Tres enlaces, tres historiales de fusion distintos con los mismos cuatro puntos.
X = np.array([0.0, 1.0, 4.0, 9.0]).reshape(-1, 1)
for metodo in ("single", "complete", "average"):
    Z = linkage(X, method=metodo)
    # Z tiene n-1 filas: (grupo A, grupo B, altura de la fusion, tamano).
    # La altura esta en la columna 2, no en la 3.
    print(f"{metodo:>9}  alturas de fusion {np.round(Z[:, 2], 3)}")
    print(f"           cortando a distancia 3 -> {[int(e) for e in fcluster(Z, t=3, criterion='distance')]}")
    print(f"           cortando a distancia 4 -> {[int(e) for e in fcluster(Z, t=4, criterion='distance')]}")
# ->    single  alturas de fusion [1. 3. 5.]
# ->            cortando a distancia 3 -> [1, 1, 1, 2]
# ->            cortando a distancia 4 -> [1, 1, 1, 2]
# ->  complete  alturas de fusion [1. 4. 9.]
# ->            cortando a distancia 3 -> [1, 1, 2, 3]
# ->            cortando a distancia 4 -> [1, 1, 1, 2]
# ->   average  alturas de fusion [1.    3.5   7.333]
# ->            cortando a distancia 3 -> [1, 1, 2, 3]
# ->            cortando a distancia 4 -> [1, 1, 1, 2]

print("distancias entre pares:", np.round(pdist(X), 3))
# -> distancias entre pares: [1. 4. 9. 3. 8. 5.]
```

:::claves
- `linkage(X, method=...)` acepta las observaciones directamente (como aquí) o una matriz de distancias ya calculada. Si le pasas una matriz de distancias hay que decírselo: la forma cómoda es `linkage(pdist(X), method="single")`, con la matriz **condensada** que devuelve `pdist`, no la matriz cuadrada completa.
- La matriz `Z` que devuelve `linkage` tiene `n − 1` filas y cuatro columnas: las dos primeras son los índices de los grupos que se fusionan (los puntos originales van de `0` a `n−1` y cada fusión nueva recibe el índice `n + i`), la tercera es la altura de la fusión y la cuarta el número de puntos del grupo resultante. La altura está en `Z[:, 2]`, y equivocarse de columna es el despiste más común al dibujar esto.
- `fcluster(Z, t=..., criterion="distance")` devuelve etiquetas de grupo que **no guardan relación con las alturas ni entre ejecuciones**: son enteros consecutivos asignados por orden de aparición. El grupo «1» de un enlace no es el mismo que el «1» de otro, así que comparar dos particiones mirando los números no significa nada.
- `dendrogram(...)` dibuja siempre el mismo árbol con independencia de `color_threshold`: ese parámetro **solo cambia el color**, no corta nada. Es la confusión que hace que alguien crea que ha elegido grupos cuando solo ha pintado ramas.
- Con enlace simple las alturas del dendrograma son monótonas no decrecientes y un corte horizontal deja grupos bien definidos. Con otros criterios (sobre todo con distancias que no cumplen la desigualdad triangular) puede haber inversiones y el corte horizontal deja de tener sentido.
- `no_labels=True` no es un detalle estético: con 69 puntos, las etiquetas de las hojas son los índices originales de cada fila y se solapan hasta ser ilegibles. Además, el orden de las hojas lo decide el árbol, **no** el orden del array: si necesitas saber qué punto es cuál, usa `dendrogram(Z, labels=...)` o mira `Z`.
- El enlace simple con `n` puntos tiene un coste de `O(n²)` en memoria para la matriz de distancias y de `O(n³)` en tiempo para el algoritmo aglomerativo clásico. Con 69 puntos no se nota; con 100.000 ni se intenta.
- Si cambias `method="single"` por `method="complete"` en la misma línea, no obtienes «el mismo árbol un poco distinto»: obtienes otro árbol, con otra última fusión (1,87 frente a 7,64) y otro número de grupos para el mismo corte. Es el parámetro que más cambia el resultado en todo el método.
:::

```python verificable
import numpy as np
from scipy.cluster.hierarchy import linkage
from sklearn.datasets import make_blobs

# Ward sobre tres grupos bien separados: el salto de altura marca donde cortar.
X, verdad = make_blobs(n_samples=150, centers=3, cluster_std=0.5, random_state=0)
Z = linkage(X, method="ward")
print("tamano real de cada grupo:", np.bincount(verdad))
print("alturas de las 3 ultimas fusiones:", np.round(Z[-3:, 2], 3))
print("salto entre la 2.a y la 3.a por la cola:", round(Z[-2, 2] / Z[-3, 2], 2))
```

## Errores típicos

- **Mirar el dendrograma sin escalar las variables.** Si una variable está en euros y otra en
  unidades, la distancia la decide la primera y el árbol sale torcido. Estandariza antes, como
  en [[k-means|K-means]].
- **Leer el dendrograma como si las distancias horizontales fueran distancias entre puntos.**
  La única información fiable es la **altura** de cada fusión y qué ramas se unen. La posición
  horizontal de las hojas suele ser arbitraria y se reordena para que el dibujo no se cruce.
- **Elegir el enlace por costumbre.** El enlace simple encadena grupos a través de un puente
  de puntos, y el completo parte grupos grandes por culpa de un atípico. Si dudas, prueba
  varios y compara con lo que sabes del dominio.
- **Creer que Ward siempre es la mejor opción.** Ward minimiza el aumento de inercia, así que
  busca grupos compactos y de tamaño similar, como [[k-means|K-means]]. Con grupos alargados,
  anillos o densidades muy distintas, produce cortes artificiales.
- **Usarlo con muchas filas.** La matriz de distancias crece al cuadrado: 50.000 puntos son
  1.250 millones de pares. O usas una variante sobre vecinos, o [[dbscan-y-hdbscan|DBSCAN]]
  con un índice espacial, o agregas antes los datos.
- **Cortar en un punto donde la altura no salta.** Si las fusiones se suceden con alturas
  parecidas (datos sin estructura clara), cualquier corte es arbitrario. Que el dendrograma no
  muestre un salto grande es en sí mismo un resultado: no hay grupos naturales.

:::practica
enunciado: Con enlace de Ward: A tiene 8 puntos y media 0; B, 8 puntos y media 2; C, 1 punto en 10; D, 1 punto en 13. ¿Fusiona Ward primero A con B o C con D?
pista: Ward no mira solo la distancia entre centroides: el factor (nA · nB) / (nA + nB) pesa tanto como ella.
solucion: Δ(A, B) = (8 · 8 / 16) · (0 − 2)² = 4 · 4 = 16. Δ(C, D) = (1 · 1 / 2) · (10 − 13)² = 0,5 · 9 = 4,5. Ward fusiona primero C con D: aunque sus medias distan 3 unidades y las de A y B solo 2, el factor de tamaños (4 frente a 0,5) decide. Ward minimiza el aumento de inercia, no la cercanía de los centroides.
:::

## Comprueba que lo sabes

:::quiz
p: Cuatro puntos en una recta: 0, 1, 4 y 9. Con enlace simple, ¿cuál es la altura de la primera fusión y cuál la última?
o: 1 y 5
o: 1 y 9
o: 3 y 5
a: 1
e: Con enlace simple la primera fusión es el par más cercano, 0 y 1, a altura 1. Después {0, 1} se une a 4 con la distancia mínima `min(4, 3) = 3`, y el conjunto se une a 9 con `min(9, 8, 5) = 5`. Con enlace completo las alturas serían 1, 4 y 9: esa es justo la diferencia entre mirar el par más cercano o el más lejano.
:::

:::quiz
p: ¿Qué significa la altura a la que se fusionan dos ramas en un dendrograma?
o: El número de puntos que contiene cada grupo
o: La distancia entre esos dos grupos según el criterio de enlace elegido
o: La posición media de los puntos en el eje horizontal
a: 2
e: La altura es exactamente el valor de la distancia entre los dos grupos en el momento de unirlos, y depende del enlace: mínimo, máximo, media o incremento de inercia en Ward. El ancho de cada rama y su posición horizontal no codifican ninguna distancia.
:::

:::truco
Antes de cortar el dendrograma, mira las últimas alturas de fusión y busca el salto más grande.
Cortar justo por debajo de ese salto te da los grupos más estables. Si no hay ningún salto
destacado, la conclusión honesta es que los datos no tienen una estructura jerárquica clara.
:::
