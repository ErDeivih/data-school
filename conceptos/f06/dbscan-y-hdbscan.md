---
id: dbscan-y-hdbscan
titulo: DBSCAN y HDBSCAN
fase: 6
nivel: avanzado
rutas: [ds, alg]
prerequisitos: [norma-y-distancias, k-means, clustering-jerarquico, escalado-y-transformacion]
tags: [clustering, densidad, ruido, no-supervisado]
resumen: Agrupar por densidad en vez de por distancia al centro: encuentra formas arbitrarias, marca el ruido y no obliga a fijar el número de grupos de antemano.
fuentes: ["Ester et al. (1996), 'A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise'", "Campello, Moulavi y Sander (2013), 'Density-Based Clustering Based on Hierarchical Density Estimates'", "Schubert et al. (2017), 'DBSCAN Revisited, Revisited: Why and How You Should (Still) Use DBSCAN'"]
---

## En una frase

DBSCAN agrupa los puntos que están densamente apiñados y declara **ruido** a los que están
aislados, así que puede encontrar grupos con forma de media luna o de anillo sin que le digas
cuántos hay; HDBSCAN hace lo mismo eligiendo la densidad de corte a partir de los datos.

## La idea

[[k-means|K-means]] y el [[clustering-jerarquico|clustering jerárquico]] comparten una
obsesión: la distancia a un centro o entre grupos. Eso funciona cuando los grupos son
compactos, pero falla con dos lunas entrelazadas, que son el ejemplo de manual: los dos grupos
están pegados y k-means los corta por la mitad.

DBSCAN cambia la pregunta. En vez de «¿a qué centro perteneces?», pregunta «¿tienes suficientes
vecinos cerca?». Y de ahí salen tres tipos de punto:

- **Punto central (core):** tiene al menos `minPts` vecinos dentro de un radio `eps`. Está en
  zona densa.
- **Punto fronterizo:** no es central, pero está dentro del radio de algún punto central.
- **Ruido:** no es central ni está cerca de uno. Se queda sin grupo.

La agrupación crece por contagio: dos puntos centrales que estén a menos de `eps` pertenecen al
mismo grupo, y arrastran a sus fronterizos. Como el crecimiento sigue la cadena de densidad y
no la distancia a un centro, el grupo puede tomar cualquier forma: una media luna, un anillo,
una letra. Y nada obliga a que todos los puntos pertenezcan a un grupo: lo que no está en zona
densa es ruido, con la etiqueta `-1`.

El precio es que `eps` y `minPts` hay que elegirlos, y `eps` es delicado. Con `eps` demasiado
pequeño, casi todo es ruido y los grupos se fragmentan; con `eps` demasiado grande, todos los
grupos se funden en uno. No hay un valor «correcto» universal: depende de la escala de los
datos, y por eso hay que **escalar** las variables antes.

HDBSCAN responde a eso. En lugar de ejecutar DBSCAN con un `eps` fijo, construye la jerarquía
de agrupaciones para todos los valores de `eps` a la vez (sobre el árbol de expansión mínima
mutua) y luego elige la agrupación más **estable**, es decir, la que sobrevive en un rango
amplio de densidades. El único parámetro que queda es `min_cluster_size`, que es mucho más
fácil de razonar: «un grupo es un grupo si tiene al menos 15 puntos». Además da a cada punto
una probabilidad de pertenencia (`probabilities_`), que es más honesta que la etiqueta dura.

## Definición formal

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `D` | El conjunto de puntos que se agrupa | las de las variables | No es un mando. Al crecer, la densidad típica cambia y el `eps` que funcionaba deja de valer |
| `d(p, q)` | Distancia entre dos puntos | las de las variables | Es el criterio de vecindad. Sin escalar, la variable de mayor rango decide quién está cerca de quién |
| `eps` | Radio de la vecindad | las de las variables | El hiperparámetro crítico. Al subirlo entran más vecinos en cada radio: los grupos se funden y baja el ruido; con `eps` muy pequeño ningún punto es central y todo queda como ruido |
| `minPts` | Vecinos mínimos para ser punto central, contando el propio punto | puntos (entero) | Al subirlo, más exigente: menos puntos centrales, más ruido y grupos más pequeños y densos. Un valor habitual de partida es `2 · d`, con `d` el número de variables |
| `N_eps(p)` | La vecindad de `p`: todos los puntos a distancia `eps` o menos | conjunto de puntos | Su tamaño es lo que se compara con `minPts`. Cuenta el propio punto, porque `d(p, p) = 0`: confundirlo desplaza el resultado |
| `core_k(a)` (HDBSCAN) | Distancia de `a` a su `k`-ésimo vecino: mide cómo de densa es su zona | las de las variables | Sustituye a `eps`: en vez de un radio fijo, cada punto lleva su propia escala de densidad. Zonas densas toleran distancias cortas y zonas dispersas, largas |
| `d_mreach(a, b)` (HDBSCAN) | Distancia de alcance mutua: el máximo entre las densidades de los dos y su distancia | las de las variables | Es la distancia corregida sobre la que trabajo HDBSCAN. Al subir la densidad de una zona, sus distancias de alcance se acortan y el grupo se separa mejor |
| `min_cluster_size` (HDBSCAN) | Tamaño mínimo para considerar algo un grupo | puntos | Es el único mando que queda y es mucho más fácil de razonar: al subirlo desaparecen los grupos pequeños y crece el porcentaje marcado como ruido |
| `k` o `min_samples` (HDBSCAN) | Vecinos que definen la densidad local | puntos | Al subirlo, la densidad se mide en un entorno más amplio: los grupos se vuelven más conservadores y solo sobreviven los que aguantan en varias escalas |
:::

Fija `eps > 0` (radio) y `minPts ∈ ℕ` (número mínimo de vecinos). La vecindad de un punto `p`
es `N_eps(p) = { q ∈ D : d(p, q) ≤ eps }`.

- **Punto central:** `/N_eps(p)/ ≥ minPts`, es decir, `p` tiene al menos `minPts` puntos a
  distancia `eps` o menos, contándose él mismo.
- **Alcanzable por densidad:** `q` es alcanzable desde `p` si existe una cadena
  `p = p₁, p₂, …, pₘ = q` donde cada `pᵢ₊₁` está en `N_eps(pᵢ)` y todos los `p₁ … p_{m−1}` son
  centrales.
- **Conectados por densidad:** `p` y `q` están en el mismo grupo si existe un punto `o` desde
  el que ambos son alcanzables.
- **Ruido:** un punto que no es central y no es alcanzable desde ningún central.

:::formula
N_eps(p) = { q ∈ D : d(p, q) ≤ eps },   p es central si /N_eps(p)/ ≥ minPts
:::

- `D` — el conjunto de puntos.
- `d(p, q)` — la distancia entre dos puntos, normalmente la euclídea.
- `eps` — el radio de la vecindad; el hiperparámetro crítico.
- `minPts` — cuántos vecinos hacen falta para considerar una zona densa. Con `d` dimensiones,
  un valor habitual de partida es `2 · d`.

En HDBSCAN, en vez de un `eps` fijo se usa la **distancia de alcance mutua** y la **core
distance**:

:::formula
d_mreach(a, b) = max{ core_k(a), core_k(b), d(a, b) }
:::

- `core_k(a)` — la distancia del punto `a` a su `k`-ésimo vecino más cercano; mide cómo de
  densa es su zona.
- `d_mreach(a, b)` — distancia corregida entre dos puntos, que nunca es menor que la densidad
  de la zona más dispersa de las dos.
- Sobre esa distancia se construye un árbol de expansión mínima, se poda por estabilidad y
  sale la jerarquía de grupos.

Detalle práctico: `minPts` en DBSCAN incluye el propio punto. Es decir, `minPts = 5` significa
«el punto más cuatro vecinos». sklearn lo aplica así, y confundirlo desplaza el resultado.

## Ejemplo

Nueve puntos en una recta, etiquetados A a I, con `eps = 1,5` y `minPts = 3`:

```
A    B    C              D    E    F         G         H         I
0    1    2              7    8    9        20        21        22
```

Vecindades (contando el propio punto, porque `d(p, p) = 0 ≤ eps`):

- A: {A, B} → 2 puntos. **No es central.**
- B: {A, B, C} → 3 puntos. **Central.**
- C: {B, C} → 2 puntos. No es central.
- D: {D, E} → 2. E: {D, E, F} → 3. F: {E, F} → 2. Así que **E es central**.
- G: {G, H} → 2. H: {G, H, I} → 3. I: {H, I} → 2. **H es central.**

Conectividad: B no está a menos de 1,5 de E (distancia 5), así que los dos primeros tríos son
grupos distintos. Resultado: **grupo 1 = {A, B, C}**, **grupo 2 = {D, E, F}**, **grupo 3 =
{G, H, I}**, y **ningún punto de ruido**, porque todos los puntos no centrales están a menos de
`eps` de un central.

Ahora cambia solo `eps` a `0,5`:

- A: {A} → 1; B: {B} → 1; C: {C} → 1. Ningún punto tiene 3 vecinos, así que **ninguno es
  central** y todos los puntos quedan como **ruido** (etiqueta `-1`). Con `eps` demasiado
  pequeño, DBSCAN no encuentra nada.

Y con `eps = 6`, B está a distancia 5 de E, así que las vecindades se encadenan y los seis
primeros puntos caen en **un solo grupo**: {A, B, C, D, E, F}. El tercer trío sobrevive
aparte, porque de F a G hay 11. Resultado: **dos grupos en vez de tres**. Al subir el radio,
DBSCAN funde racimos que no tienen nada que ver, y ese es el error clásico al elegir `eps`.

## Código

:::figura
fichero: dbscan-lunas-frente-a-k-means
pie: Dos lunas entrelazadas y una frontera recta son incompatibles, y eso es todo lo que hay que ver: K-means acierta el 73 % y falla justo donde está la información, porque cada luna queda partida por la mitad en lugar de quedar entera. El porcentaje no es catastrófico y ahí está la trampa: en un problema desbalanceado, un modelo que corta por el medio puede tener una exactitud aceptable y ser inservible. Abajo, DBSCAN con `eps = 0,16` y `minPts = 8` recupera las dos lunas sin que nadie le diga cuántos grupos hay, y además marca seis puntos como ruido. Esos seis puntos son los atípicos que en la versión de arriba estaban dentro de un grupo y ensuciando su centroide; aquí quedan fuera y con una etiqueta explícita. Ese `eps` todavía deja 45 puntos de una luna convertidos en una tercera etiqueta: el grupo se termina de fundir con `eps ≈ 0,18`, y ahí se ve lo fino que hay que hilar el radio.
fuente: figuras/dbscan-y-hdbscan-2.py
:::

:::figura
fichero: dbscan-tipos-de-punto-y-eleccion-de-eps
pie: A la izquierda están las tres categorías que introduce DBSCAN y que ningún método de centroides tiene. Los círculos azules son puntos centrales: dentro del círculo cian caben `minPts = 5` puntos contando el propio, y ese es el único requisito para serlo. Los cuadrados naranjas son puntos de borde: no llegan al umbral por sí solos pero caen dentro del radio de uno central, así que pertenecen al grupo sin poder fundar uno. Las aspas rojas son ruido, y aquí está la diferencia importante: son puntos que se quedan **sin grupo**, no puntos mal asignados a uno. Con `k = 2` en K-means todos estarían en alguna parte. A la derecha, la misma información en forma de curva: cada punto ordenado por la distancia a su cuarto vecino. Las zonas densas son la parte plana de la izquierda y los puntos aislados el tramo empinado de la derecha; el codo entre ambos es el `eps` razonable. Con el valor dibujado quedan fuera 32 de 190 puntos, que es una cantidad de ruido creíble, no un desastre.
fuente: figuras/dbscan-y-hdbscan-1.py
:::

```python verificable
import numpy as np
from sklearn.cluster import DBSCAN

# Nueve puntos en una recta: el mismo dato, tres valores de eps, tres respuestas.
# reshape(-1, 1): nueve puntos en una recta, como matriz de 9 filas y 1 columna.
X = np.array([0, 1, 2, 7, 8, 9, 20, 21, 22.0]).reshape(-1, 1)
for eps in (0.5, 1.5, 6.0):
    d = DBSCAN(eps=eps, min_samples=3).fit(X)
    # labels_ es un array de enteros; -1 significa ruido, no "sin clasificar".
    etiquetas = [int(e) for e in d.labels_]
    n_ruido = int((d.labels_ == -1).sum())
    print(f"eps={eps:<4} etiquetas {etiquetas}  ruido {n_ruido}")
# -> eps=0.5  etiquetas [-1, -1, -1, -1, -1, -1, -1, -1, -1]  ruido 9
# -> eps=1.5  etiquetas [0, 0, 0, 1, 1, 1, 2, 2, 2]  ruido 0
# -> eps=6.0  etiquetas [0, 0, 0, 0, 0, 0, 1, 1, 1]  ruido 0

# Cuales son puntos centrales con eps=1.5: los que tienen 3 vecinos o mas.
d = DBSCAN(eps=1.5, min_samples=3).fit(X)
# X es (9,1) y X.T es (1,9): la resta da una matriz 9x9 de distancias, y se
# cuentan las que no pasan de 1.5. Incluye el propio punto, d(p,p)=0.
vecinos = (np.abs(X - X.T) <= 1.5).sum(axis=1)
print("vecinos por punto (incluyendo el propio):", [int(v) for v in vecinos])
# -> vecinos por punto (incluyendo el propio): [2, 3, 2, 2, 3, 2, 2, 3, 2]
```

:::claves
- `min_samples` **cuenta el propio punto**: con `min_samples=3` se pide «yo y dos vecinos más». Es distinto de lo que sugiere el nombre, y confundirlo desplaza todos los resultados sin dar ningún error. En el ejemplo de nueve puntos, con `eps = 1,5` los centrales son B, E y H, porque su vecindario tiene 3 puntos contándose a sí mismos.
- `DBSCAN` no recibe el número de grupos: lo deduce de la densidad. Por eso `fit_predict(X)` es lo normal, y por eso el resultado puede ser un solo grupo o ninguno.
- `fit_predict` devuelve `-1` para el ruido. Cualquier comparación con etiquetas reales tiene que **excluir** ese `-1` o contarlo como error: si no, un modelo que marca todo como ruido puntúa pésimo y uno que no marca nada puntúa bien. En el segundo bloque se ve la forma correcta: la máscara `d.labels_ != -1` filtra antes de comparar.
- `np.abs(X - X.T) <= 1.5` construye la matriz de distancias a mano: `X` tiene forma `(9, 1)` y `X.T` forma `(1, 9)`, así que la resta sale de `9 × 9` por difusión. Es exactamente lo que hace `pdist`, pero en versión cuadrada y sin salir del array.
- `NearestNeighbors.radius_neighbors` devuelve una lista de **arrays de longitud variable**, uno por punto, no una matriz rectangular: cada punto tiene un número distinto de vecinos. De ahí el `len(v)` punto por punto; un `.sum(axis=1)` directo no funciona.
- `kneighbors(X)` con los valores por defecto incluye al propio punto como primer vecino a distancia 0. La consecuencia práctica está en el código: para la curva de la k-ésima distancia se pide `n_neighbors=k + 1` y se toma la **última** columna, `[:, -1]`, porque la primera es el cero del propio punto.
- El orden de las filas sí influye en un caso concreto: cuando un punto de borde es alcanzable desde dos grupos distintos, DBSCAN lo asigna al primero que lo encuentra. Las etiquetas de los grupos tampoco son estables entre ejecuciones, así que el grupo «0» de una ejecución no es el «0» de la siguiente.
- Cuidado con mezclar ejemplos: en los nueve puntos de abajo, un `eps` de 0,2 deja los nueve como ruido y un `eps` de 1,5 da los tres grupos; el que funde los seis primeros puntos en un solo racimo es `eps = 6,0`. Los tres valores del primer bloque son el mismo dato con tres respuestas: nueve puntos de ruido, tres grupos, dos grupos. No hay un valor «correcto», se elige mirando la curva de la k-ésima distancia.
:::

```python verificable
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons

# Dos lunas entrelazadas: K-means tiene que cortarlas, DBSCAN las sigue enteras.
X, verdad = make_moons(n_samples=300, noise=0.06, random_state=0)

km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
print(f"k-means k=2  acuerdo con los grupos reales {max((km.labels_ == verdad).mean(), (km.labels_ != verdad).mean()):.3f}")

for eps in (0.1, 0.12, 0.3):
    d = DBSCAN(eps=eps, min_samples=5).fit(X)
    # Comparamos solo los puntos que DBSCAN asigna a algun grupo: el ruido no tiene etiqueta real.
    fuera_ruido = d.labels_ != -1
    acuerdo = max((d.labels_[fuera_ruido] == verdad[fuera_ruido]).mean(),
                  (d.labels_[fuera_ruido] != verdad[fuera_ruido]).mean())
    n_grupos = len(set(d.labels_[fuera_ruido])) if fuera_ruido.any() else 0
    print(f"DBSCAN eps={eps:<5} grupos {n_grupos}  ruido {int((~fuera_ruido).sum()):>3} de {len(X)}  "
          f"acuerdo {acuerdo:.3f}")
# -> k-means k=2  acuerdo con los grupos reales 0.743
# -> DBSCAN eps=0.1   grupos 11  ruido  15 de 300  acuerdo 0.937
# -> DBSCAN eps=0.12  grupos 2  ruido   5 de 300  acuerdo 1.000
# -> DBSCAN eps=0.3   grupos 1  ruido   0 de 300  acuerdo 0.500
```

## Errores típicos

- **No escalar las variables.** `eps` es un radio en las unidades de los datos: si una variable
  va de 0 a 1 y otra de 0 a 100.000, el radio solo tiene sentido para la segunda. Estandariza
  siempre y elige `eps` después.
- **Elegir `eps` a ojo.** Un método razonable: para cada punto, calcula la distancia a su
  `minPts`-ésimo vecino, ordena esas distancias y dibújalas. El «codo» de esa curva, donde
  deja de ser plana y empieza a subir, es un buen candidato a `eps`.
- **Confundir el ruido con un error que hay que limpiar.** La etiqueta `-1` es un resultado,
  no un fallo: esos puntos son atípicos o pertenecen a grupos demasiado pequeños. Cuéntalos y
  decide qué hacer con ellos. Borrarlos sin mirar puede eliminar justo los casos interesantes.
- **Esperar grupos de tamaño parecido.** DBSCAN no equilibra nada: un grupo puede tener 5.000
  puntos y otro 12. Si necesitas segmentos comparables, es la herramienta equivocada.
- **Usarlo en dimensión alta.** Las densidades se diluyen con las dimensiones (es la
  [[maldicion-de-la-dimensionalidad|maldición de la dimensionalidad]]): con 50 variables,
  cualquier `eps` razonable deja casi todo como ruido o lo funde todo. Reduce dimensión antes.
- **Quedarse con DBSCAN cuando `minPts` y `eps` os tienen locos.** Si pasas más tiempo
  ajustando `eps` que interpretando los grupos, cambia a HDBSCAN: solo pide `min_cluster_size`,
  que se traduce directamente a «cuántos puntos como mínimo forman un grupo».

:::practica
enunciado: Cinco puntos en una recta: 0, 2, 4, 5 y 30. Con eps = 2,5 y minPts = 3 (contando el propio punto), di qué puntos son centrales, en qué grupos quedan y cuál es ruido.
pista: La vecindad de un punto son los que están a distancia eps o menos, incluido él; hacen falta minPts para ser central.
solucion: Vecindades: 0 tiene {0, 2}, dos puntos, no es central; 2 tiene {0, 2, 4}, tres, sí es central; 4 tiene {2, 4, 5}, tres, también; 5 tiene {4, 5}, dos, no; 30 tiene {30}, uno, no. Como 2 y 4 son centrales y distan 2 ≤ eps, forman un grupo y arrastran a 0 y a 5: queda un solo grupo, {0, 2, 4, 5}, y el 30 se marca como ruido (−1).
:::

## Comprueba que lo sabes

:::quiz
p: Con `eps = 1,5` y `minPts = 3`, los puntos de una recta en 0, 1 y 2 forman un grupo. ¿Cuáles son puntos centrales?
o: Los tres, porque todos tienen vecinos
o: Solo el punto 1, porque es el único que tiene tres puntos a distancia 1,5 o menos (él mismo, el 0 y el 2)
o: Ninguno: hacen falta al menos 4 puntos
a: 2
e: La vecindad de 0 es {0, 1}: dos puntos, insuficiente. La de 1 es {0, 1, 2}: tres, suficiente. La de 2 es {1, 2}. Basta con que haya un punto central para que los otros dos se unan como fronterizos, así que el grupo existe aunque solo el 1 sea central.
:::

:::quiz
p: ¿Qué ventaja principal tiene HDBSCAN sobre DBSCAN?
o: Es siempre más rápido
o: No necesita fijar `eps`: construye la jerarquía para todas las densidades y elige la agrupación más estable, quedando solo `min_cluster_size` como parámetro de escala
o: Garantiza que todos los puntos se asignan a un grupo
a: 2
e: DBSCAN depende críticamente de `eps`, y un valor ligeramente distinto cambia por completo el resultado. HDBSCAN evita esa elección buscando la agrupación que persiste en un rango amplio de densidades. Sigue marcando ruido y no siempre es más rápido: construir la jerarquía cuesta más.
:::

:::aviso
DBSCAN con `eps` pequeño sobre datos reales suele devolver un montón de microgrupos y un 30 %
de ruido. Eso no significa que tus datos estén mal: significa que no forman cúmulos densos y
separados. Antes de seguir ajustando parámetros, pregúntate si el problema pide de verdad
agrupación por densidad o si lo que quieres es segmentar por reglas de negocio.
:::
