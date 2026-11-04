---
id: bases-de-datos-vectoriales
titulo: Bases de datos vectoriales
fase: 8
nivel: avanzado
rutas: [ds, de]
prerequisitos: [embeddings, producto-punto-y-similitud, norma-y-distancias, maldicion-de-la-dimensionalidad, knn]
tags: [rag, recuperacion, indices, latencia]
resumen: Índices para buscar el vecino más cercano entre millones de vectores: qué hacen HNSW e IVF, qué recall sacrifican y cómo se combina con filtros.
fuentes: ["Malkov y Yashunin (2018), 'Efficient and Robust Approximate Nearest Neighbor Search Using HNSW Graphs'", "Jégou, Douze y Schmid (2011), 'Product Quantization for Nearest Neighbor Search'"]
---

## En una frase

Una base de datos vectorial guarda los [[embeddings|embeddings]] y responde a «dame los
vectores más parecidos a este», pero como comparar contra millones de vectores uno por uno es
demasiado lento, usa un índice aproximado (HNSW, IVF) que encuentra casi siempre los mismos
vecinos mirando una fracción pequeña de los datos.

## La idea

Buscar el vecino más cercano es fácil de describir y caro de ejecutar. Con 10.000 vectores,
comparar la consulta contra todos es instantáneo. Con 50 millones de vectores de 768
dimensiones, cada comparación cuesta 768 multiplicaciones y el barrido completo son unos
38.000 millones de operaciones por consulta: segundos, no milisegundos, y eso sin contar que
los 50 millones de vectores ocupan unos 150 GB en memoria.

La salida es dejar de buscar el vecino *exacto* y conformarse con el *casi exacto*. Es una
decisión de ingeniería, no un atajo sucio: si el noveno resultado de tu búsqueda aparece en
segundo lugar, al generador le da igual. Lo que importa es que los verdaderamente buenos
entren en la lista.

Dos familias de índice resuelven esto:

**HNSW** (*Hierarchical Navigable Small World*) construye un grafo por capas. La capa de
arriba tiene pocos nodos y conexiones largas —como los vuelos intercontinentales—; las capas
de abajo van teniendo más nodos y conexiones cortas —como los vuelos regionales—. La búsqueda
empieza arriba, salta rápido a la región correcta y va bajando para afinar. Cada nodo guarda
una lista de vecinos de tamaño `M`, y la búsqueda explora una cola de candidatos de tamaño
`efSearch`. Es rápido, con recall alto y sin entrenamiento previo, pero el grafo ocupa memoria
extra (del orden de `M` enlaces por vector) y las inserciones son más caras que las lecturas.

**IVF** (*Inverted File*) hace lo contrario: primero agrupa los vectores en `nlist` grupos con
k-means y guarda, para cada grupo, la lista de vectores que contiene. En una consulta compara
solo contra los `nlist` centroides, elige los `nprobe` más cercanos y busca dentro de ellos.
Es sencillo, ocupa poco más que los propios vectores y se puede combinar con **cuantización
de producto** para comprimir cada vector a unos pocos bytes, a costa de perder precisión en
las distancias. Su debilidad es la frontera: un vector se asigna a un solo grupo, y si su
vecino más cercano cayó en el grupo de al lado, no lo encontrarás salvo que subas `nprobe`.

Hay un tercer factor que se lleva por delante más sistemas que los dos anteriores: **el
filtrado**. Casi nunca quieres buscar en todo el corpus, sino en los documentos de un cliente,
de un idioma o de los últimos 30 días. Filtrar *después* de buscar es un error clásico: pides
el top 10 y te quedas con los que cumplen el filtro, que pueden ser cero. La solución es
filtrar dentro del índice (el motor recorre el grafo o los grupos saltando lo que no cumple),
y para eso el índice tiene que conocer los metadatos del filtro.

## Definición formal

Sea una base de `n` vectores `v₁, …, vₙ ∈ ℝ^d` y una consulta `q`. La búsqueda exacta devuelve:

:::formula
NN_k(q) = los k vectores con menor d(q, vᵢ)
:::

donde `d(·,·)` es la distancia (euclídea, o `1 − coseno` si los vectores están normalizados).
La búsqueda aproximada devuelve `Â_k(q)` y su calidad se mide con **recall@k**:

:::formula
recall@k = | Â_k(q) ∩ NN_k(q) | / k
:::

- `recall@k = 1` significa que el índice devolvió exactamente los mismos `k` vecinos que el
  barrido completo. En la práctica se trabaja entre 0,90 y 0,99.
- Un recall del 0,95 con 10 resultados significa que, de media, uno de cada dos consultas
  pierde un vecino relevante por el camino.

Los parámetros que se tocan:

- **HNSW:** `M` (enlaces por nodo, típicamente 16-48) y `efSearch` (tamaño de la cola de
  exploración). Subir `efSearch` mejora el recall de forma monótona y encarece cada consulta
  de forma casi lineal; `M` mejora el recall sobre todo en datos con grupos muy densos, a
  cambio de más memoria.
- **IVF:** `nlist` (número de grupos) y `nprobe` (grupos que se visitan). La fracción de base
  que se examina es aproximadamente `nprobe / nlist`; con `nlist = 4096` y `nprobe = 64` se
  mira el 1,6 % de los datos, y por eso es tan rápido.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Vectores guardados en el índice | vectores | El barrido exacto crece de forma lineal, y el índice aproximado es el que deja de notarlo |
| `d` | Dimensiones de cada vector (las del modelo de embeddings) | dimensiones | El coste por comparación y la memoria suben a la vez: `float32` son `4 · d` bytes por vector. No se puede cambiar sin revectorizar todo |
| `q` | La consulta, vectorizada con el **mismo** modelo que el corpus | vector de `d` dimensiones | Nada: la consulta es una sola. Pero si viene de otro modelo, las distancias no significan nada |
| `recall@k` | Fracción de los `k` vecinos verdaderos que devuelve el índice | entre 0 y 1 | Sube `efSearch` (HNSW) o `nprobe` (IVF). Es la palanca que se paga en latencia, no en precisión del vector |
| `M` | Enlaces por nodo en el grafo HNSW | enlaces | Más memoria (del orden de `4 · M` bytes por vector) y mejor recall en datos con grupos densos |
| `efSearch` | Tamaño de la cola de exploración de HNSW | candidatos | Recall monótonamente mejor y consulta casi proporcionalmente más cara |
| `nlist` | Número de grupos del IVF (centroides del k-means) | grupos | Grupos más finos: cada consulta mira menos datos y hay más fronteras donde perder un vecino |
| `nprobe` | Grupos que se visitan en una consulta | grupos | `nprobe / nlist` es la fracción de base examinada: con 4096 y 64 se mira el 1,6 %. Doblar `nprobe` dobla el tiempo |
| `k` | Resultados que se piden | vecinos | Fija el techo y también el trabajo del índice: `recall@10` no es lo mismo que `recall@100` |
:::

Coste de memoria, como orden de magnitud: los vectores en `float32` ocupan `4 · d` bytes por
vector (3.072 bytes con `d = 768`), y HNSW añade del orden de `4 · M` bytes más por vector
para los enlaces.

## Ejemplo

Base de 1.000.000 de vectores de 768 dimensiones:

- Vectores en crudo: 1.000.000 · 768 · 4 bytes ≈ **2,9 GB**.
- Barrido completo por consulta: 768 millones de multiplicaciones ≈ **decenas de
  milisegundos** en CPU, cientos de veces más de lo aceptable en una interfaz con streaming.
- IVF con `nlist = 4096`, `nprobe = 64`: se examinan unos 15.600 vectores, el **1,6 %** de la
  base. El coste por consulta baja en un factor cercano a 60.
- HNSW con `M = 32`: los enlaces añaden del orden de 128 bytes por vector, unos **128 MB**
  extra, y cada consulta visita unos pocos miles de nodos.

El efecto de la frontera, medido en una base de juguete de 600 vectores en 32 dimensiones
dividida en 8 grupos, con 30 consultas y `k = 10`:

| nprobe | Base examinada | recall@10 |
| --- | --- | --- |
| 1 | 12 % | 0,60 |
| 2 | 25 % | 0,80 |
| 4 | 50 % | 0,95 |

Con `nprobe = 1` se pierde el 40 % de los vecinos verdaderos: los que están cerca de la
frontera entre dos grupos. Doblar `nprobe` recupera la mayor parte. En una base real de
millones de vectores el recall a igual `nprobe` es mejor (más datos por grupo), pero el patrón
se mantiene: **el recall se compra con tiempo de consulta**, y hay que medirlo con tus datos.

## Código

El primer bloque hace la búsqueda exacta sobre una base pequeña de juguete: es el patrón
mental contra el que se compara todo lo demás. El segundo construye un IVF de verdad
(k-means incluido) y mide cuánto recall se pierde al visitar solo una parte de los grupos.

```python verificable
import numpy as np

rng = np.random.default_rng(0)
base = rng.normal(0, 1, size=(2000, 64))
base /= np.linalg.norm(base, axis=1, keepdims=True)      # normalizar = comparar por coseno
consulta = rng.normal(0, 1, size=64)
consulta /= np.linalg.norm(consulta)

# Producto escalar = similitud del coseno cuando los vectores son unitarios
similitudes = base @ consulta
# argsort ordena de menor a mayor: el menos delante lo da la vuelta para quedarse con el top
mejores = np.argsort(-similitudes)[:5]

print("mejores indices:", mejores.tolist())
print("sus similitudes:", np.round(similitudes[mejores], 3).tolist())
print("coste: 1 producto matriz-vector,", base.shape[0] * base.shape[1], "multiplicaciones")
```

:::claves
- `base /= np.linalg.norm(base, axis=1, keepdims=True)` divide cada fila por su propia norma. `axis=1` suma «a lo largo de las columnas» (una norma por vector) y `keepdims=True` mantiene la forma `(2000, 1)` para que NumPy pueda repartir la división fila a fila. Sin `keepdims` la norma sale con forma `(2000,)` y **no hay error**: NumPy la alinea por la última dimensión y divide cada columna por la norma del vector equivocado.
- Normalizar no es cosmético: **cambia el resultado**. Sin normalizar, `base @ consulta` es producto escalar puro y los vectores de norma grande ganan siempre, aunque apunten en dirección distinta. Con los vectores unitarios, ese producto es exactamente el coseno que se quiere medir.
- `base @ consulta` es álgebra lineal en C: recorre las 128.000 casillas sin un bucle de Python, y devuelve un array de 2000 similitudes. `np.argsort(-similitudes)` no ordena los valores, devuelve **las posiciones**; el menos delante invierte el orden porque `argsort` siempre va de menor a mayor.
- `similitudes[mejores]` usa indexación por array: coge los cinco valores en el orden de `mejores`. Y `np.round(..., 3)` devuelve un array de NumPy, así que sin el `.tolist()` el `print` enseña `np.float64(...)` en vez de números limpios.
- La búsqueda exacta de este bloque es el patrón mental contra el que se compara todo lo demás: cuesta 2000 · 64 = 128.000 multiplicaciones por consulta. Con un millón de vectores de 768 dimensiones serían 768 millones, y ese es el número que justifica los índices aproximados.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
centros = rng.normal(0, 1, size=(8, 32))
# Ruido alto a proposito: los grupos se solapan y la frontera del IVF se nota.
base = np.vstack([c + rng.normal(0, 2.0, size=(75, 32)) for c in centros])
base /= np.linalg.norm(base, axis=1, keepdims=True)

def dist2(X, Y):
    """Distancias al cuadrado de todos los pares, sin bucles: (n, m)."""
    # ||x||^2 + ||y||^2 - 2·x·y: la identidad que evita restar matrices de formas distintas
    return (X ** 2).sum(1)[:, None] + (Y ** 2).sum(1)[None, :] - 2 * X @ Y.T

def kmeans(X, k, semilla=0, iteraciones=50):
    """k-means basico: devuelve los k centroides, sin devolver la asignacion."""
    r = np.random.default_rng(semilla)
    # centros iniciales = k vectores reales elegidos al azar (sin reemplazo)
    C = X[r.choice(len(X), k, replace=False)].copy()
    for _ in range(iteraciones):
        # cada vector se asigna al centroide mas cercano (argmin devuelve el indice)
        etiquetas = np.argmin(dist2(X, C), axis=1)
        # .mean(0) promedia las filas del grupo; el if evita el nan de un grupo vacio
        C = np.array([X[etiquetas == j].mean(0) if np.any(etiquetas == j) else C[j]
                      for j in range(k)])
    return C

C = kmeans(base, 8)
asignacion = np.argmin(dist2(base, C), axis=1)          # a que grupo va cada vector

def exactos(q, k=10):
    """Los k indices verdaderamente mas cercanos: el barrido completo, sin indice."""
    return set(np.argsort(dist2(q[None, :], base)[0])[:k])

consultas = base[rng.choice(len(base), 30, replace=False)] + rng.normal(0, 0.1, (30, 32))
for nprobe in (1, 2, 4):
    aciertos = 0.0
    for q in consultas:
        # solo se comparan los centroides: elegir los nprobe grupos mas cercanos a la consulta
        cercanos = np.argsort(dist2(q[None, :], C)[0])[:nprobe]   # grupos a visitar
        # isin da una mascara; flatnonzero la convierte en los indices de esos vectores
        cand = np.flatnonzero(np.isin(asignacion, cercanos))
        d = dist2(base[cand], q[None, :])[:, 0]
        encontrados = set(cand[np.argsort(d)[:10]])
        # interseccion de conjuntos: cuantos de los 10 verdaderos recupero el IVF
        aciertos += len(encontrados & exactos(q, 10)) / 10
    print(f"nprobe={nprobe}  visitados {100 * nprobe // 8}%  recall@10 {aciertos / 30:.3f}")
```

:::figura
fichero: vectorial-frontera-y-recall
pie: A la izquierda, los 600 vectores del ejemplo dibujados en dos dimensiones: se generaron en 8 grupos, pero el ruido los solapa y la nube no viene troceada. En el centro, los mismos puntos con los grupos que decide k-means: el corte es una frontera entre centroides y los 213 puntos marcados en rojo están casi a la misma distancia de dos grupos, así que una consulta que solo visite el grupo de su centroide más cercano los deja fuera. A la derecha, el recall medido en función de nprobe sobre este experimento: 0,60 con un solo grupo, 0,94 con cuatro y 1,00 con los ocho. Compara esa curva con la tabla del ejemplo: **el recall se compra con tiempo de consulta**, y el salto grande está en los primeros grupos. Si tu índice devuelve listas peores de lo esperado y el filtro por cliente está puesto, esta curva es lo primero que hay que medir.
fuente: figuras/bases-de-datos-vectoriales-1.py
:::

## Errores típicos

- **Creer que el índice devuelve los vecinos exactos.** HNSW e IVF son aproximados por
  diseño. Si tu evaluación de la recuperación da números peores de lo esperado, sube
  `efSearch` o `nprobe` antes de culpar al modelo de embeddings.
- **Filtrar después de buscar.** Pedir el top 10 global y quedarse con los que cumplen un
  filtro selectivo devuelve listas vacías o de un solo elemento. El filtro tiene que aplicarse
  dentro del recorrido del índice, y no todos los motores lo hacen igual de bien.
- **Comparar distancias de métricas distintas.** Un índice construido con distancia euclídea y
  consultado con coseno devuelve resultados sin sentido. Y si usas producto escalar con
  vectores no normalizados, los vectores largos ganan siempre: normaliza antes de indexar.
- **Reconstruir el índice con cada cambio de datos.** Con HNSW las inserciones son caras y las
  actualizaciones masivas degradan el grafo; con IVF, añadir vectores sin reentrenar los
  centroides desequilibra los grupos. Planifica una reconstrucción periódica o usa un motor
  que gestione el problema.
- **Ignorar el coste de memoria.** Los vectores en `float32` más los enlaces del grafo pueden
  no caber en la máquina que habías presupuestado. La cuantización (a `int8`, con
  cuantización de producto, o con binarios y distancia de Hamming) es la palanca habitual,
  siempre a cambio de recall.
- **Elegir el motor antes de conocer la escala y el filtro.** Con 50.000 vectores un índice
  plano en memoria va sobrado y es exacto. Añadir una base vectorial distribuida a ese tamaño
  solo añade un servicio que mantener.

:::aviso
El recall hay que medirlo con **tus** datos y **tus** consultas. Los valores que publican los
motores se obtienen con conjuntos de referencia que no se parecen a tu corpus: dimensión
distinta, distribución distinta y, sobre todo, ningún filtro de metadatos. Un índice con
recall 0,98 sin filtros puede bajar a 0,6 en cuanto filtras por cliente.
:::

## Comprueba que lo sabes

:::quiz
p: Un IVF con nlist = 4096 y nprobe = 32 devuelve listas peores de lo esperado. ¿Cuál es el primer ajuste razonable?
o: Cambiar el modelo de embeddings por uno de más dimensiones
o: Subir nprobe, porque se están visitando pocos grupos y los vecinos de la frontera quedan fuera
o: Reconstruir el índice sin normalizar los vectores
a: 2
e: Con 4096 grupos y 32 visitados se examina menos del 1 % de la base, así que es normal perder vecinos que cayeron en un grupo contiguo. Subir nprobe cambia recall por latencia de forma directa y medible. Cambiar de modelo no arregla un problema de índice, y quitar la normalización rompe la comparación por coseno.
:::

:::quiz
p: ¿Por qué filtrar por cliente después de pedir el top 10 global puede devolver una lista vacía?
o: Porque el motor no admite filtros después de la búsqueda
o: Porque los 10 vecinos globales pueden pertenecer todos a otros clientes, y el filtro se aplica sobre lo ya devuelto
o: Porque el filtro cambia la distancia entre vectores
a: 2
e: El top 10 se calcula sobre toda la base; si tus documentos son el 1 % del corpus, es perfectamente posible que ninguno entre en esos 10. La solución es filtrar durante el recorrido del índice, no después, para que el motor busque solo entre los candidatos que cumplen la condición.
:::

:::quiz
p: ¿Qué mide exactamente el recall@10 de un índice vectorial?
o: La fracción de consultas que terminan en menos de 10 ms
o: La fracción media de los 10 vecinos verdaderos que el índice consigue devolver
o: La fracción de vectores de la base que el índice visita en cada consulta
a: 2
e: Es una medida de calidad de la lista devuelta, comparada con el barrido exacto: si de los 10 vecinos reales solo devuelve 9, el recall es 0,9. El tiempo de respuesta y la fracción de base examinada son métricas distintas, y ambas se compran y se pagan por separado.
:::
