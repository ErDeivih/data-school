---
id: tsne-y-umap
titulo: t-SNE y UMAP
fase: 6
nivel: avanzado
rutas: [ds]
prerequisitos: [pca, maldicion-de-la-dimensionalidad, entropia-e-informacion]
tags: [visualizacion, dimensionalidad, vecindarios, no-lineal]
resumen: Dos formas de dibujar datos de muchas dimensiones en un plano que conservan los vecindarios y se inventan el resto: sirven para mirar, no para medir.
fuentes: ["van der Maaten y Hinton (2008), 'Visualizing Data using t-SNE'", "McInnes, Healy y Melville (2018), 'UMAP: Uniform Manifold Approximation and Projection'"]
---

## En una frase

t-SNE y UMAP colocan cada punto en dos dimensiones de forma que sus vecinos más cercanos sigan
siéndolo, a costa de deformar todo lo demás: el dibujo dice quién está cerca de quién, pero las
distancias entre grupos y sus tamaños no significan nada.

## La idea

Piensa en el plano de un metro dibujado a mano para que las estaciones de cada línea queden
juntas y las líneas no se crucen. Para orientarte sirve: ves qué estaciones son vecinas. Pero no
midas con una regla la distancia entre dos barrios del dibujo, porque el cartógrafo ha estirado
unas zonas y comprimido otras a propósito. Eso es exactamente lo que hace t-SNE.

El punto de partida es un problema geométrico inevitable: **no se puede meter un espacio de
muchas dimensiones en dos sin deformarlo**. Cuatro puntos que distan lo mismo entre sí (un
tetraedro) no caben en un plano: en el plano, de cada punto salen como mucho tres vecinos
equidistantes, y el cuarto tiene que acercarse a alguno. Así que cualquier método tiene que
elegir qué conservar, y [[pca]] elige las distancias globales (las direcciones de más varianza),
mientras que t-SNE y UMAP eligen los vecindarios locales.

Como lo consiguen, en tres pasos:

1. **Convertir distancias en probabilidades.** Para cada punto, la probabilidad de elegir a otro
   como vecino decae con la distancia según una gaussiana cuyo ancho `σ_i` se ajusta punto a
   punto. El ancho no es libre: se elige para que la distribución tenga una **perplejidad**
   concreta, que es aproximadamente «el número efectivo de vecinos» que ese punto considera.
2. **Repetir lo mismo en el plano.** Se colocan los puntos en 2D y se calcula, con una
   distribución de colas gordas (la t de Student), la probabilidad de que dos puntos sean
   vecinos en el dibujo.
3. **Mover los puntos para que ambas distribuciones se parezcan**, minimizando la divergencia
   KL. Eso es lo que hace el descenso de gradiente.

UMAP hace lo mismo con otra maquinaria —un grafo difuso y una entropía cruzada— y suele ser más
rápido y conservar algo mejor la estructura global, pero comparte la propiedad incómoda: sigue
sin ser una proyección con escala.

La perplejidad es el parámetro que decide qué se ve. Baja, cada punto solo mira a dos o tres
vecinos y el dibujo se rompe en islas; alta, mira a muchos y las islas se funden. Los valores
habituales van de 5 a 50, y **no hay uno correcto**: si dos perplejidades dan mensajes distintos,
la conclusión es que tus datos no tienen una estructura de grupos clara.

## Definición formal

t-SNE empieza definiendo, para cada par de puntos `x_i` y `x_j` del espacio original, una
similitud condicional:

:::formula
p_j|i = exp(−‖x_i − x_j‖² / (2 σ_i²)) / Σ_{k ≠ i} exp(−‖x_i − x_k‖² / (2 σ_i²))
:::

- `‖x_i − x_j‖` — distancia euclídea entre los dos puntos.
- `σ_i` — ancho de banda gaussiano del punto `i`. Se busca por bisección el valor que hace que
  la entropía `H(P_i) = −Σ_j p_j|i · log₂ p_j|i` cumpla `2^H = Perplejidad`, el valor que fijas tú.
- `p_j|i` no es simétrica, así que se simetriza: `p_ij = (p_j|i + p_i|j) / (2n)`, con `n` el
  número de puntos.

En el plano, con las posiciones `y_i` que se están optimizando, la similitud usa una t de
Student de un grado de libertad, cuyas colas gordas evitan que los puntos se apelotonen:

:::formula
q_ij = (1 + ‖y_i − y_j‖²)⁻¹ / Σ_{k ≠ l} (1 + ‖y_k − y_l‖²)⁻¹
:::

Y el objetivo es acercar ambas distribuciones:

:::formula
C = KL(P ‖ Q) = Σ_{i ≠ j} p_ij · log(p_ij / q_ij)
:::

- `p_ij` — similitud en el espacio original (constante durante la optimización).
- `q_ij` — similitud en el plano (cambia en cada paso).
- La divergencia KL no es simétrica: penaliza mucho más usar una `q_ij` pequeña donde `p_ij` es
  grande que al revés. Por eso t-SNE prefiere juntar puntos que estaban lejos antes que separar
  vecinos verdaderos, y por eso los grupos aparecen como islas compactas.

En UMAP, los dos parámetros que se tocan son `n_neighbors` (cuántos vecinos definen la
estructura local, equivalente funcional de la perplejidad) y `min_dist` (la distancia mínima a
la que se permite apelotonar puntos en el dibujo; bajo, los grupos salen más compactos).

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de puntos que se proyectan | puntos | El mapa tarda más (el coste crece al cuadrado) y las islas se reparten entre más puntos: la figura se vuelve una mancha |
| `σ_i` | Ancho de banda gaussiano del punto `i`, el que se ajusta para cada punto | las de las variables originales | Cada punto mira más lejos, así que aumentan los «vecinos» que considera y el vecindario pierde detalle local |
| `Perplejidad` | Número efectivo de vecinos que cada punto tiene en cuenta | vecinos (adimensional) | Vecindarios más anchos: las islas pequeñas se funden y las distancias entre grupos cambian por completo, como en el ejemplo |
| `p(j dado i)` | Probabilidad de que `i` elija a `j` como vecino en el espacio original | probabilidad (0-1) | No se interpreta sola: lo que importa es la distribución completa de cada punto; una probabilidad alta de un vecino lejano arrastra el mapa |
| `p_ij` | La versión simetrizada, la que se compara con el plano | probabilidad (0-1) | Es constante durante toda la optimización: no cambia mientras se mueven los puntos |
| `q_ij` | Probabilidad de que dos puntos sean vecinos en el plano | probabilidad (0-1) | Cambia en cada paso del descenso de gradiente; es lo único que se mueve |
| `KL(P ‖ Q)` | Divergencia que se minimiza entre las dos distribuciones | nats (adimensional) | No es un parámetro que se suba: es la función de coste. Cuanto mayor, peor está el dibujo |
| `n_neighbors` (UMAP) | Cuántos vecinos definen la estructura local | vecinos | El equivalente de la perplejidad: alto conserva mejor la estructura global y difumina la local |
| `min_dist` (UMAP) | Distancia mínima a la que se dejan apelotonar los puntos en el plano | las del plano (2D) | Grupos menos compactos y más repartidos; bajo, las islas quedan más apretadas y separadas entre sí |
:::

## Ejemplo

**Por qué hay que deformar algo.** Cuatro puntos en tres dimensiones que forman un tetraedro
regular de arista `20·√2 = 28,28` (los vértices son las cuatro combinaciones de `+10` y `−10` con
un número par de signos negativos). Los seis pares distan exactamente lo mismo: `28,28`. Proyectados a dos dimensiones con la mejor
transformación lineal posible (las dos primeras componentes principales), las distancias desde
el primer vértice pasan a ser `28,28`, `20,00` y `20,00`. Es decir: la mejor proyección posible
ya encoge dos de las aristas un 29 %. No es un fallo del método, es geometría.

**Qué decide la perplejidad.** Tres grupos de 60 puntos en 10 dimensiones, centrados en `(0,…,0)`,
`(4,0,…,0)` y `(0,4,0,…,0)`, con desviación 0,7 dentro de cada grupo. Las distancias entre los
centros de los grupos en el dibujo salen así:

| Perplejidad | Distancias entre grupos en el plano | Cociente mayor/menor |
| --- | --- | --- |
| 5 | 41,9 — 43,3 — 41,9 | 1,03 |
| 30 | 20,9 — 15,3 — 24,0 | 1,56 |
| 50 | 9,3 — 7,0 — 16,3 | 2,31 |

Los tres grupos son los mismos en los tres casos y las distancias reales entre sus centros
también (`4`, `4` y `5,66`). Sin embargo, con perplejidad 5 los tres parecen igual de lejanos y
con perplejidad 30 el cociente mayor/menor pasa de 1,03 a 1,56. Si el mensaje de tu figura
depende de la perplejidad, el mensaje no está en los datos.

:::figura
fichero: tsne-perplejidad-y-distancias
pie: Los dos paneles son los mismos 180 puntos y los mismos tres grupos, dibujados con la misma semilla y cambiando solo la perplejidad. Lo que hay que mirar no es el dibujo, son los números de arriba: con perplejidad 5 los tres centros quedan a 41,9, 43,3 y 41,9, un cociente de 1,03, cuando en el espacio original distan 4,00, 4,00 y 5,66 (cociente 1,41). El par que de verdad está más lejos, el 2-3, sale en el mapa como el más corto. Con perplejidad 30 los mismos pares aparecen a 20,9, 15,3 y 24,0, cociente 1,56. Los grupos siguen siendo tres y las distancias reales no han cambiado: lo único que cambió fue un parámetro. La lectura práctica es que el mapa sirve para ver quién es vecino de quién y nunca para medir ni comparar distancias entre grupos; si dos perplejidades dan mensajes distintos, el mensaje no lo ponían los datos.
fuente: figuras/tsne-y-umap-1.py
:::

## Código

```python verificable
import numpy as np

# Cuanta atencion recibe una distancia segun el ancho de banda local (sigma).
for sigma in (1.0, 5.0):
    p1 = np.exp(-(1.0 ** 2) / (2 * sigma ** 2))    # similitud sin normalizar
    p2 = np.exp(-(2.0 ** 2) / (2 * sigma ** 2))
    print(f"sigma={sigma}  d=1 {p1:.4f}  d=2 {p2:.4f}  cociente {p1 / p2:.2f}")
# -> sigma=1.0  d=1 0.6065  d=2 0.1353  cociente 4.48
# -> sigma=5.0  d=1 0.9802  d=2 0.9231  cociente 1.06

# Perplejidad: el numero efectivo de vecinos de una distribucion de similitudes.
p = np.array([0.8, 0.1, 0.1])
H = -(p * np.log(p)).sum()                         # ojo: log neperiano, no log2
print("entropia:", round(H, 4), "perplejidad:", round(2 ** H, 2))
# -> entropia: 0.639 perplejidad: 1.56
```

:::claves
- `H = -(p * np.log(p)).sum()` mide la entropía en **nats**, porque `np.log` es el logaritmo
  neperiano. Con esa `H`, la perplejidad es `np.exp(H) = 1,895`. El bloque imprime `2 ** H = 1,56`
  porque mezcla las dos bases: elevar a 2 solo es correcto si la entropía está en bits, es decir
  calculada con `np.log2`. La fórmula `2^H = Perplejidad` del texto funciona porque t-SNE usa
  logaritmos en base 2; en código, comprueba siempre con qué logaritmo has medido `H`.
- `np.exp(-(d ** 2) / (2 * sigma ** 2))` es la similitud **sin normalizar**: falta dividir entre la
  suma de todas. Para comparar dos distancias del mismo punto no hace falta, porque el denominador
  se cancela en el cociente; para comparar dos puntos distintos, sí, y ahí es donde entra el
  `sigma` de cada uno.
- `np.linalg.norm(vertices[:, None, :] - vertices[None, :, :], axis=2)` es la matriz de distancias
  por *broadcasting*: los `None` añaden los ejes que faltan y la resta sale de forma `(4, 4, 3)`,
  una distancia por par y coordenada. El `axis=2` es lo que convierte esa resta en una norma y
  deja una matriz `4 × 4`; sin él obtendrías un único número.
- `D[D > 0]` filtra la diagonal antes de dividir. `D` incluye los ceros de cada punto consigo
  mismo, así que `D.min()` sería 0 y el cociente mayor/menor daría infinito. Es el mismo cuidado
  que hay que tener al calcular la distancia mínima entre vecinos.
- `np.linalg.eigh(centrado.T @ centrado)[1][:, ::-1][:, :2]` toma los autovectores, los invierte y
  se queda con dos columnas. Aquí no importa el orden por tamaño: los cuatro vértices del tetraedro
  son simétricos, y cualquier par de direcciones propias sirve para proyectar. En un caso real sí
  hay que ordenar por autovalor, como en [[pca]].
- El tercer bloque es `ilustrativo` y no se ejecuta en la verificación: importa `umap`, que **no**
  viene con scikit-learn. Y `TSNE` no tiene `transform()`: cada ejecución reajusta el mapa entero,
  así que las coordenadas de dos ejecuciones no son comparables ni se pueden usar como variables de
  un modelo.
:::

```python verificable
import numpy as np

# Cuatro puntos de un tetraedro regular: los seis pares distan exactamente lo mismo.
vertices = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) * 10
D = np.linalg.norm(vertices[:, None, :] - vertices[None, :, :], axis=2)   # los None dan los ejes

# La mejor proyeccion lineal a dos dimensiones: las dos primeras componentes principales.
centrado = vertices - vertices.mean(axis=0)
vectores = np.linalg.eigh(centrado.T @ centrado)[1][:, ::-1][:, :2]
plano = centrado @ vectores
D2 = np.linalg.norm(plano[:, None, :] - plano[None, :, :], axis=2)

print("distancias desde el primer vertice, original:", np.round(D[0, 1:], 2).tolist())
# -> [28.28, 28.28, 28.28]
print("las mismas distancias en el plano:", np.round(D2[0, 1:], 2).tolist())
# -> [28.28, 20.0, 20.0]
print("cociente mayor/menor original:", round(float(D[D > 0].max() / D[D > 0].min()), 2))
# -> 1.0
print("cociente mayor/menor en el plano:", round(float(D2[D2 > 0].max() / D2[D2 > 0].min()), 2))
# -> 1.41
```

```python ilustrativo
# El flujo real: escalar, reducir y dibujar. UMAP no viene con scikit-learn,
# asi que se instala aparte (paquete umap-learn).
import matplotlib
matplotlib.use("Agg")           # sin ventana: guardamos la figura a disco
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import umap                     # pip install umap-learn

Z = StandardScaler().fit_transform(X)                  # 2000 filas, 40 columnas
dos_d = TSNE(n_components=2, perplexity=30, random_state=0).fit_transform(Z)
dos_d_umap = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=0).fit_transform(Z)

fig, ejes = plt.subplots(1, 2, figsize=(10, 5))
ejes[0].scatter(dos_d[:, 0], dos_d[:, 1], s=4, c=etiquetas, cmap="tab10")   # color por grupo
ejes[1].scatter(dos_d_umap[:, 0], dos_d_umap[:, 1], s=4, c=etiquetas, cmap="tab10")
fig.savefig("mapa.png", dpi=150)
```

## Errores típicos

- **Medir distancias entre grupos.** El hueco blanco entre dos islas es un artefacto de la
  optimización, no una medida de parecido. Dos grupos pueden estar en extremos opuestos del
  dibujo y ser casi idénticos, y viceversa. Para comparar grupos, calcula distancias en el
  espacio original.
- **Interpretar el tamaño y la forma de las islas.** t-SNE reparte el plano entre los grupos de
  forma bastante uniforme, así que un grupo con el doble de área no tiene el doble de puntos ni
  de dispersión; y como los grupos salen redondeados y separados casi siempre, su silueta no
  reproduce la forma que tienen en el espacio original, ni siquiera cuando allí se solapan.
- **Usar la salida 2D como variables para un modelo.** Es una visualización, no una
  transformación estable: dos ejecuciones con datos ligeramente distintos dan coordenadas
  incomparables. Para reducir dimensión de verdad, usa [[pca]] o métodos con transformación
  aprendida.
- **Quedarte con una sola figura.** Si cambias la semilla, la perplejidad o el `n_neighbors` y
  la conclusión se mantiene, tienes algo. Si no, tenías un dibujo bonito. Enseña el rango, no
  la versión que más te gusta.
- **Proyectar datos nuevos con el modelo ya ajustado.** t-SNE clásico no tiene método para
  transformar puntos que no vio: hay que reajustar todo (y el dibujo cambia). UMAP sí tiene
  `transform`, pero sigue siendo una aproximación; si necesitas eso en producción, replantea el
  problema.
- **Aplicarlo antes de agrupar o de detectar anomalías.** Las coordenadas 2D conservan los
  vecinos, pero para [[k-means]], [[dbscan-y-hdbscan]] o [[deteccion-de-anomalias]] conviene
  trabajar en el espacio original reducido con PCA y no en un plano deformado.

:::practica
enunciado: Las similitudes normalizadas de un punto con sus vecinos son (0,5; 0,25; 0,25) para el punto A y (0,25; 0,25; 0,25; 0,25) para el B. Calcula la entropía y la perplejidad de cada uno y decide cuál está teniendo en cuenta a más vecinos.
pista: Perplejidad = 2^H si mides la entropía en bits; con logaritmos naturales es exp(H) y sale el mismo número.
solucion: A: H = −(0,5·log₂0,5 + 0,25·log₂0,25 + 0,25·log₂0,25) = 0,5·1 + 0,25·2 + 0,25·2 = 1,5 bits, y su perplejidad es 2^1,5 = 2,83. B: H = −4 · 0,25 · log₂0,25 = 2 bits, con perplejidad 2² = 4. El punto B mira a unos 4 vecinos efectivos y el A a unos 2,83: repartir la misma probabilidad entre más vecinos sube la perplejidad.
:::

## Comprueba que lo sabes

:::quiz
p: Dos grupos aparecen en tu figura t-SNE muy separados. ¿Qué puedes concluir?
o: Que los dos grupos son muy distintos entre sí, porque el hueco mide la distancia
o: Que el modelo considera que casi ningún punto de un grupo tiene vecinos en el otro
o: Que la distancia euclídea entre las medias de los grupos es grande en el espacio original
a: 2
e: t-SNE optimiza vecindarios: lo que garantiza es que los vecinos cercanos siguen cerca. La separación entre islas es en gran parte un efecto de la divergencia KL y de la perplejidad, y no conserva proporciones. Para afirmar que las medias están lejos hay que medirlo en el espacio original, no en el dibujo.
:::

:::quiz
p: ¿Qué controla la perplejidad en t-SNE?
o: El número de dimensiones de salida
o: El número efectivo de vecinos que cada punto tiene en cuenta al construirse el mapa
o: La fracción de varianza que se conserva, como en PCA
a: 2
e: La perplejidad se fija como objetivo de entropía de la distribución de vecinos de cada punto, así que regula el tamaño del vecindario. La salida sigue siendo bidimensional y t-SNE no reparte varianza explicada como PCA: no existe ese concepto aquí.
:::

:::quiz
p: ¿Por qué cuatro puntos equidistantes no se pueden representar en un plano sin deformar distancias?
o: Porque el plano solo admite tres puntos a la misma distancia de uno dado, así que el cuarto tiene que acercarse a alguno
o: Porque las distancias euclídeas solo existen en tres dimensiones
o: Porque los métodos no lineales no convergen con tan pocos puntos
a: 1
e: En un plano, la circunferencia de radio r alrededor de un punto admite infinitos puntos, pero solo tres pueden estar además a distancia r entre sí (el triángulo equilátero). El cuarto vértice del tetraedro no cabe y hay que deformar. No es un problema de algoritmo ni de convergencia: es geometría.
:::

:::aviso
t-SNE y UMAP no son intercambiables con PCA ni compiten en la misma liga. PCA es una
transformación reproducible que puedes aplicar a datos nuevos y cuyas componentes se
interpretan; t-SNE es una figura para mirar con los ojos. Si tu pipeline necesita coordenadas
estables, la respuesta casi siempre es PCA (o un autoencoder), no un mapa bidimensional.
:::
