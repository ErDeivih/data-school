---
id: k-means
titulo: K-means
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [norma-y-distancias, medidas-de-centralidad, escalado-y-transformacion]
tags: [clustering, centroides, inercia, no-supervisado]
resumen: Agrupar puntos alrededor de k centroides minimizando la suma de distancias al cuadrado, con el método del codo para elegir k y sus límites bien claros.
fuentes: ["Lloyd (1982), 'Least Squares Quantization in PCM'", "MacQueen (1967), 'Some Methods for Classification and Analysis of Multivariate Observations'", "Arthur y Vassilvitskii (2007), 'k-means++: The Advantages of Careful Seeding'"]
---

## En una frase

K-means coloca `k` centroides, asigna cada punto al más cercano, recoloca cada centroide en el
centro de su grupo y repite hasta que nada se mueve; el objetivo es que cada punto esté lo más
cerca posible de su centroide.

## La idea

Tienes las ventas de una tienda y quieres saber si hay «tipos de cliente». No tienes etiquetas,
así que no puedes entrenar un clasificador: tienes que buscar estructura. K-means es la
respuesta más directa.

Elige `k` puntos al azar como centros provisionales. Después alterna dos pasos:

1. **Asignar:** cada punto va al centro más cercano.
2. **Actualizar:** cada centro se mueve al promedio de los puntos que le han tocado.

Y repite. Cada paso reduce (o deja igual) la suma de distancias al cuadrado, así que el
algoritmo siempre termina: no puede dar vueltas indefinidamente porque solo hay un número
finito de agrupaciones posibles. Pero aquí está su carácter: **termina en un mínimo local, no
en el mínimo global**. Si empiezas con centros mal colocados, te quedas en una partición peor y
no te enteras.

De ahí que la inicialización importe tanto. La versión `k-means++`, que es la que usa sklearn
por defecto con `n_init=10`, elige los centros iniciales separados entre sí con una
probabilidad proporcional a su distancia al centro más cercano ya elegido. Con eso se evita el
caso clásico de dos centros cayendo en el mismo grupo y un tercero en tierra de nadie.

Y de ahí también la pregunta obvia: ¿cuánto vale `k`? K-means no lo decide; tú lo fijas. La
herramienta habitual es el **método del codo**: dibujar la inercia (la suma de distancias al
cuadrado de cada punto a su centroide) frente a `k` y buscar el punto donde la curva deja de
caer rápido. Es una heurística visual, no un test, y con datos ruidosos es más un consejo que
una respuesta. El criterio de la silueta o el gap statistic son alternativas algo más
formales.

El límite estructural de K-means es su forma: cada grupo es una **esfera** alrededor de su
centroide, porque la frontera entre dos centroides es siempre una recta perpendicular. Con
grupos alargados, anillos, o densidades muy distintas, K-means corta por donde no debe. Ahí
tocan [[clustering-jerarquico|clustering jerárquico]] o [[dbscan-y-hdbscan|DBSCAN]].

## Definición formal

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `xᵢ` | El punto `i` que se agrupa | las de las variables | No es un mando. Los puntos extremos arrastran su centroide porque la media no es robusta: un solo atípico mueve el grupo entero |
| `k` | Número de grupos que pides | grupos (entero) | La inercia baja siempre y llega a 0 con `k = n`. Subirlo mejora el ajuste a los datos y empeora la interpretación: pasados unos pocos grupos solo se parten los que ya había |
| `μ_j` | Centroide del grupo `j`: la media de sus puntos | las de las variables | Al desplazarse cambia qué puntos le quedan asignados. Su posición no es un mando, es el resultado: se recoloca en cada iteración |
| `c(i)` | El grupo asignado al punto `i` | etiqueta (entero) | Es una etiqueta, no una magnitud: la distancia entre el grupo 0 y el 2 no significa nada, y el número que le toca a un grupo cambia entre ejecuciones |
| `(xᵢ − μ_j)²` | Distancia euclídea al cuadrado del punto a su centro | unidades² | Es la magnitud que se minimiza, y al estar al cuadrado pesa mucho más un punto lejano que varios cerca: por eso K-means es sensible a los atípicos |
| `J` | Inercia: la suma de esas distancias al cuadrado | unidades² | Es lo que baja el algoritmo en cada paso: siempre decrece o se queda igual, y por eso termina. No es comparable entre valores de `k` |
| `d` | Número de variables | variables | Cada variable nueva añade una dimensión a la distancia: si no se escala antes, la de mayor rango domina y las demás dejan de influir |
| `n_j` | Número de puntos del grupo `j` | puntos | Los grupos grandes pesan más en la inercia, así que K-means prefiere partir un grupo grande antes que dejar uno pequeño mal ajustado |
| `n_init` | Cuántos arranques distintos se prueban | ejecuciones (entero) | Subirlo reduce la probabilidad de quedarse en un mínimo local: sklearn se queda con el arranque de menor inercia. Cuesta tiempo lineal en `n_init` |
:::

- `xᵢ` — el punto `i`, un vector de `d` variables.
- `c(i)` — el grupo asignado al punto `i`, un número entre 1 y `k`.
- `μ_j` — el centroide del grupo `j`; su posición es la media de los puntos asignados a `j`.
- `(xᵢ − μ_{c(i)})²` — distancia euclídea al cuadrado del punto a su centroide.
- `J` — la inercia: siempre disminuye al aumentar `k`, y vale 0 cuando `k = n`.

El algoritmo de Lloyd alterna dos pasos que minimizan `J` manteniendo fijo el otro:

1. `c(i) = argmin_j (xᵢ − μ_j)²` (asignar al más cercano).
2. `μ_j = (1/n_j) Σ_{i: c(i)=j} xᵢ` (mover al promedio), con `n_j` el número de puntos del
   grupo `j`.

Detalle que casi nadie tiene en cuenta: **la inercia no es comparable entre valores de `k`**.
Siempre baja al subir `k`; con `k = n` es exactamente 0. Por eso el codo se lee como un cambio
de pendiente y por eso no puedes elegir `k` «minimizando» la inercia sin más: con más grupos
siempre baja, así que ese criterio te llevaría a `k = n`.

## Ejemplo

Seis clientes con una sola variable, el gasto mensual en euros:

```
1   2   3   10   11   12
```

Con `k = 2` y centros iniciales en 1 y 10:

- **Asignar:** {1, 2, 3} al centro 1; {10, 11, 12} al centro 10.
- **Actualizar:** el centro 1 pasa a (1+2+3)/3 = 2; el centro 10 pasa a (10+11+12)/3 = 11.
- **Asignar otra vez:** nadie cambia de grupo. El algoritmo termina en dos iteraciones.

La inercia final es `(1−2)² + (2−2)² + (3−2)² + (10−11)² + (11−11)² + (12−11)² = 1+0+1+1+0+1 = 4`.

La curva del codo para estos datos: `k=1` da 125,5; `k=2` da 4,0; `k=3` da 2,5; `k=4` da 1,0.
El salto brutal está entre 1 y 2 (de 125,5 a 4,0), y a partir de ahí cada grupo extra apenas
rasca: eso es un codo clarísimo en `k = 2`. Con 6 puntos y 2 grupos, cada centroide es la media
de un grupo de 3.

## Código

:::figura
fichero: k-means-anillos-y-arranque
pie: La fila de arriba ataca el límite geométrico. Con un núcleo dentro de un anillo la estructura natural son dos grupos, pero la frontera entre ellos tendría que ser un círculo: K-means solo sabe poner rectas, así que con `k = 2` reparte el anillo en dos mitades por ángulo y deja el núcleo partido. Subir a `k = 4` no arregla la forma, solo trocea el anillo en más trozos: el error se queda en torno al 30 %, y solo baja al 5 % con `k = 10`. Eso es lo que significa «el modelo tiene la forma equivocada». La fila de abajo ataca el otro límite: cuarenta arranques al azar del mismo dato con el mismo `k` dan inercias entre 465 y 716, un 54 % de diferencia, y la partición que sale de un mal arranque no es un poco peor: es otra distinta. Ese es el motivo de `n_init = 10` y de `k-means++`.
fuente: figuras/k-means-2.py
:::

:::figura
fichero: k-means-codo-y-centroides
pie: El panel izquierdo lleva las dos curvas a la misma escala 0-100 para poder compararlas, porque la inercia se mide en unidades al cuadrado y la silueta no tiene unidades. La azul baja siempre, con o sin estructura: con `k` igual al número de puntos valdría 0, así que «menor inercia» nunca es un criterio. Lo que se lee es la pendiente: al pasar de 3 a 4 grupos la inercia cae un 76 % y al añadir el quinto solo un 11 %, y ahí está el codo. La verde confirma lo mismo por otro camino y desciende en cuanto se pasa de 4. El panel derecho recuerda el motivo de fondo: la frontera entre dos centroides es siempre la recta que los separa por la mitad, de modo que cada grupo es una esfera alrededor de su centro. Fíjate en el grupo de 25 puntos: K-means no sabe que es pequeño ni que está junto a otro, solo mide distancias al cuadrado, y por eso el grupo con más puntos pesa más en la inercia.
fuente: figuras/k-means-1.py
:::

```python verificable
import numpy as np
from sklearn.cluster import KMeans

# Los centroides se mueven hasta que las asignaciones dejan de cambiar.
# reshape(-1, 1) convierte los 6 numeros en una matriz de 6 filas y 1 columna:
# sklearn espera siempre una matriz de observaciones x variables.
X = np.array([1, 2, 3, 10, 11, 12.0]).reshape(-1, 1)
m = KMeans(n_clusters=2, init=np.array([[1.0], [10.0]]), n_init=1, random_state=0).fit(X)
print("etiquetas:", m.labels_)
# cluster_centers_ tiene forma (2, 1); ravel() lo aplana a un array de 2 numeros.
print("centroides:", np.round(m.cluster_centers_.ravel(), 3))
print("inercia:", round(m.inertia_, 3), " iteraciones:", m.n_iter_)
# -> etiquetas: [0 0 0 1 1 1]
# -> centroides: [ 2. 11.]
# -> inercia: 4.0  iteraciones: 2

# El codo: la inercia baja siempre, la pregunta es donde deja de bajar en serio.
for k in (1, 2, 3, 4):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print(f"k={k}  inercia {km.inertia_:.3f}")
# -> k=1  inercia 125.500
# -> k=2  inercia 4.000
# -> k=3  inercia 2.500
# -> k=4  inercia 1.000
```

:::claves
- `m.labels_` no es una columna del DataFrame ni una Serie: es un array de NumPy de enteros, con la misma longitud que las filas y en el mismo orden. Y los números **no tienen significado ni orden**: el grupo «0» de una ejecución no tiene por qué ser el mismo que el «0» de la siguiente, ni el «0» significar «el primero por la izquierda».
- `m.cluster_centers_` es un array de forma `(k, d)`; de ahí el `.ravel()` del ejemplo para pasar de `[[2.], [11.]]` a `[2., 11.]`. `ravel()` devuelve una **vista** cuando puede: modificar el resultado puede tocar el original. Si quieres una copia, `np.array(...)` o `.copy()`.
- `m.inertia_` solo existe **después** de `fit`, y en scikit-learn los atributos aprendidos terminan en guion bajo por convención. Un `inertia_` suelto antes de ajustar lanza `AttributeError`, que es la señal de que el modelo aún no ha visto datos.
- `n_init=10` significa que el algoritmo se ejecuta diez veces con diez inicializaciones distintas y se queda con la de menor inercia. Con `n_init=1` el resultado depende de la semilla: en el mismo dato, cuarenta arranques al azar dan inercias que difieren un 54 %, y no son diferencias de redondeo, son particiones distintas.
- `KMeans(n_clusters=2, init=np.array([[1.0], [10.0]]))` pasa los centroides iniciales escritos a mano, y con eso `n_init` deja de tener sentido (sklearn avisa y hace una sola pasada). Es la forma de reproducir a mano el ejemplo de la página.
- `fit_predict(X)` es `fit(X)` más `predict(X)` y devuelve directamente las etiquetas. Cuidado: con datos de entrenamiento devuelve las etiquetas **memorizadas**, no una evaluación honesta.
- La silueta no está definida para `k = 1`: `silhouette_score` lanza un error si solo hay un grupo. En el código se calcula de `k = 2` en adelante y se deja un `nan` en la primera posición para que los índices sigan cuadrando.
:::

```python verificable
import numpy as np
from sklearn.cluster import KMeans

# K-means corta por rectas: con dos anillos concentricos parte cada anillo en dos.
rng = np.random.default_rng(0)
theta = rng.uniform(0, 2 * np.pi, 400)
radio = np.concatenate([rng.normal(1.0, 0.08, 200), rng.normal(3.0, 0.08, 200)])
X = np.column_stack([radio * np.cos(theta), radio * np.sin(theta)])

for k in (2, 3):
    # fit_predict es fit mas predict y devuelve las etiquetas directamente.
    etiquetas = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    # Cuanto del anillo interior (los 200 primeros puntos) cae en un solo grupo.
    # max sobre las dos hipotesis porque el numero de grupo es arbitrario.
    acuerdo = max((etiquetas[:200] == 0).mean(), (etiquetas[:200] == 1).mean())
    print(f"k={k}: el anillo interior cae en un unico grupo el {acuerdo:.0%} de las veces")
# -> k=2: el anillo interior cae en un unico grupo el 53% de las veces
# -> k=3: el anillo interior cae en un unico grupo el 34% de las veces
```

## Errores típicos

- **No escalar las variables.** K-means usa distancias euclídeas: una variable medida en
  euros domina sobre otra medida en unidades. Estandariza siempre, salvo que todas las
  variables estén ya en la misma escala y quieras que las de mayor rango pesen más.
- **Elegir `k` por la inercia más baja.** La inercia decrece siempre al subir `k` y llega a 0
  con `k = n`. El codo se lee en la pendiente, y si la curva es suave hay que apoyarse en
  silueta, en conocimiento del negocio o en la estabilidad de los grupos entre muestras.
- **Usar K-means con grupos de formas no esféricas o densidades muy distintas.** Un grupo
  alargado se parte en dos y dos grupos cercanos se funden. Si sospechas que la forma importa,
  mira el resultado de [[dbscan-y-hdbscan|DBSCAN]] antes de dar por bueno el tuyo.
- **Quedarse con una sola ejecución.** Con `n_init` bajo, dos ejecuciones pueden dar
  particiones distintas. Deja `n_init` en 10 o más y comprueba la estabilidad: si los grupos
  cambian mucho entre semillas, no hay estructura clara.
- **Tratar las etiquetas de grupo como si tuvieran orden o significado.** Los números 0, 1 y 2
  son nombres, no magnitudes: la distancia entre el grupo 0 y el 2 no significa nada. Y el
  grupo «1» de una ejecución no se corresponde con el «1» de otra.
- **Ignorar los valores atípicos.** La media que define cada centroide se deja arrastrar por
  un solo punto extremo, y eso mueve el grupo entero. Revisa atípicos antes, o usa una
  variante robusta como K-medoids.

:::practica
enunciado: Cuatro clientes con variables ya centradas: (0, 0), (0, 2), (10, 0) y (10, 2). Con k = 2, compara la inercia de partir por x (izquierda y derecha) con la de partir por y (abajo y arriba) y di cuál elige K-means.
pista: La inercia suma las distancias al cuadrado de cada punto a la media de su grupo; calcula antes los centroides.
solucion: Partiendo por x los centroides son (0, 1) y (10, 1), y cada punto dista 1 del suyo: J = 1 + 1 + 1 + 1 = 4. Partiendo por y son (5, 0) y (5, 2), y cada punto dista 5: J = 25 + 25 + 25 + 25 = 100. K-means elige la partición por x, la de menor inercia: optimiza distancias al cuadrado, no el criterio del negocio.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué K-means encuentra a veces una solución peor que la óptima?
o: Porque la inercia tiene varios mínimos locales y el algoritmo se queda en el primero al que llega desde la inicialización
o: Porque no está garantizado que termine
o: Porque solo funciona con datos en una dimensión
a: 1
e: Lloyd alterna dos pasos que nunca empeoran la inercia, así que siempre converge; el problema es que converge a un mínimo local que depende de dónde empezaron los centroides. De ahí `k-means++` y `n_init` alto. El algoritmo funciona en cualquier dimensión.
:::

:::quiz
p: Eliges `k` mirando la inercia y ves que baja de 125,5 a 4,0 entre `k=1` y `k=2`, y de 4,0 a 2,5 entre `k=2` y `k=3`. ¿Qué sugiere eso?
o: Que hay que usar `k=3` porque la inercia es menor
o: Que hay un codo claro en `k=2`, porque el segundo grupo explica casi toda la estructura y el tercero apenas añade nada
o: Que la inercia no sirve para nada y hay que usar otro método
a: 2
e: La caída de 121,5 puntos al pasar a 2 grupos indica que la estructura principal son dos grupos; el descenso de 1,5 al añadir el tercero es marginal. La inercia siempre baja, así que «menor inercia» nunca es el criterio por sí solo.
:::

:::trampa
K-means etiqueta **todos** los puntos, incluso el ruido: no existe la categoría «no
pertenece a ningún grupo». Un cliente atípico acabará asignado al grupo que le pille más
cerca, y eso puede deformar el centroide si el grupo es pequeño. Si necesitas detectar puntos
que no encajan, el modelo que buscas es [[dbscan-y-hdbscan|DBSCAN]] o un detector de
anomalías.
:::
