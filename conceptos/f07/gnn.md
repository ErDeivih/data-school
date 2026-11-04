---
id: gnn
titulo: Redes sobre grafos
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [perceptron-y-mlp, operaciones-matriciales, retropropagacion]
tags: [grafos, mensajes, estructura, deep-learning]
resumen: Cada nodo se representa agregando información de sus vecinos, capa a capa: la estructura del grafo entra en el modelo en lugar de tratarse como columnas sueltas.
fuentes: ["Kipf y Welling (2017), 'Semi-Supervised Classification with Graph Convolutional Networks'", "Hamilton et al. (2017), 'Inductive Representation Learning on Large Graphs'"]
---

## En una frase

Una red sobre grafos (GNN) calcula la representación de cada nodo mezclando su información con
la de sus vecinos; apilando capas, cada nodo acaba resumiendo su vecindario de radio `k`, y la
misma matriz de pesos sirve para todos los nodos del grafo.

## La idea

Imagina que quieres saber la ideología de una persona a partir de sus amistades. Preguntas a
sus amigos, y a los amigos de sus amigos, y combinas lo que te dicen dando más peso a quien
tiene menos contactos (porque su opinión es más informativa que la de alguien que habla con
todo el mundo). Ese rumor que se propaga por la red de amistades y se promedia en cada paso es
exactamente lo que hace una GNN: **pasar mensajes por las aristas y agregarlos en cada nodo**.

La diferencia con lo que ya sabes está en cómo se usa la estructura:

- Una [[cnn|red convolucional]] explota una rejilla: cada píxel tiene vecinos fijos (arriba,
  abajo, izquierda, derecha) y el mismo filtro se desliza por todas las posiciones.
- Una RNN explota una secuencia: el vecino es el siguiente elemento en el tiempo.
- Un [[perceptron-y-mlp|MLP]] sobre las características de cada fila **ignora por completo**
  quién es vecino de quién. Si el grafo importa, ese MLP está tirando información a la basura.

:::figura
fichero: gnn-sobresuavizado-y-pesos
pie: El panel izquierdo es el límite práctico de las GNN y la razón de que casi todas tengan dos o tres capas. Al apilar capas, la representación de cada nodo se va pareciendo a la de sus vecinos hasta que todos convergen a la misma dirección: con 32 capas el coseno medio entre pares es 0,9999 y la red ya no distingue un nodo de otro, así que ninguna tarea por nodo puede funcionar. No es sobreajuste ni un problema de gradientes: es una propiedad del operador que se aplica una y otra vez. El panel derecho enseña por qué hace falta normalizar. Sin normalizar, el peso de cada vecino es 1 y un nodo con 400 vecinos aporta 400 veces más a la suma que uno con un vecino: su representación domina y el entrenamiento se desequilibra. La curva es la misma para la normalización por filas y para la simétrica, pero la simétrica reparte el peso entre los dos extremos de la arista, dividiendo por la raíz del grado de cada uno, y por eso mantiene el espectro acotado.
fuente: figuras/gnn-1.py
:::

Un grafo es la estructura correcta cuando las relaciones son irregulares: número de vecinos
distinto en cada nodo, sin orden entre ellos, y a menudo sin dirección clara. Moléculas
(átomos y enlaces), redes sociales, citas entre artículos, recomendación usuario-producto,
mallas de tráfico o grafos de dependencias. En todos esos casos no hay una rejilla que
deslizar, pero sí una noción de «vecindad» que se puede explotar.

La propiedad que hace que todo funcione es la **invariancia a la permutación**: si renumeras
los nodos del grafo, la representación que produce la red cambia de orden pero no de valor.
Para conseguirlo, la operación de agregación tiene que ser conmutativa (suma, media, máximo), y
no puede depender del índice del vecino. Si concatenas los vecinos en el orden en que aparecen
en la matriz, has roto esa propiedad y la red aprenderá cosas distintas según cómo numeres el
grafo: un error clásico y difícil de ver.

## Definición formal

Un grafo es `G = (V, E)`: `V` es el conjunto de nodos y `E` el de aristas. Se representa con la
matriz de adyacencia `A`, de tamaño `n × n` (`n` = número de nodos), donde `A_uv = 1` si hay
arista entre `u` y `v`. El **grado** de un nodo es `d_v = Σ_u A_vu`, el número de vecinos.
`N(v)` es el conjunto de vecinos de `v` y `h_v^(k)` es el vector de características del nodo
`v` en la capa `k` (con `h_v^(0)` las características de entrada).

La forma general de una capa de paso de mensajes es:

:::formula
h_v^(k+1) = φ( h_v^(k) , AGG_{u ∈ N(v)} ψ( h_u^(k) ) )
:::

- `ψ` — función que transforma el mensaje de cada vecino; casi siempre una multiplicación por
  una matriz de pesos aprendida `W`.
- `AGG` — agregación **conmutativa** sobre los vecinos: suma, media o máximo.
- `φ` — función que combina el nodo consigo mismo y con lo agregado; normalmente una
  transformación lineal seguida de una no linealidad.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Número de nodos del grafo | nodos | El número de parámetros **no cambia**, porque `W` es la misma para todos: lo que crece es el coste de agregar mensajes, que es lineal en el número de aristas |
| `d_v` | Grado del nodo `v`: cuántos vecinos tiene | vecinos | Sin normalizar, el nodo pesa más en todas las sumas de sus vecinos y su representación domina; con normalización simétrica, cada arista suya aporta menos |
| `k` | Número de capas: el radio del vecindario que resume cada nodo | capas | Cada capa amplía el alcance, pero hacia la octava el coseno medio entre nodos ronda 0,8 y todos empiezan a parecerse: el sobre-suavizado borra la información |
| `W^(k)` | Matriz de pesos de la capa `k`, compartida por todos los nodos | adimensional | Más capacidad de transformar los mensajes, con el mismo número de parámetros para cualquier tamaño de grafo |
| `h_v^(k)` | Vector de características del nodo `v` en la capa `k` | las de las características | Con más capas va mezclando más vecindario y perdiendo lo que lo hacía distinto: es el efecto que mide el panel izquierdo de la figura |
| `AGG` | Agregación conmutativa sobre los vecinos (suma, media o máximo) | las de los mensajes | Elegir suma en vez de media hace que los nodos con más vecinos acumulen valores más grandes; el máximo se fija en el vecino más extremo y no promedia |
:::

La versión más usada es la capa convolucional de grafos (GCN), que se escribe directamente en
forma matricial:

:::formula
H^(k+1) = σ( D̃^(−1/2) Ã D̃^(−1/2) H^(k) W^(k) ) ,   con Ã = A + I
:::

- `H^(k)` — matriz de `n × F` con las características de todos los nodos apiladas por filas.
- `W^(k)` — matriz de pesos de `F × F'`, **la misma para todos los nodos**; es lo que hace que
  el número de parámetros no dependa del tamaño del grafo.
- `Ã = A + I` — la adyacencia más la identidad, es decir, **con autoenlaces**: cada nodo se
  envía un mensaje a sí mismo para no perder su propia información al agregar.
- `D̃` — matriz diagonal con `D̃_vv = Σ_u Ã_vu`, el grado contando el autoenlace.
- `D̃^(−1/2) Ã D̃^(−1/2)` — normalización simétrica: divide cada arista por la raíz del grado de
  sus dos extremos, para que un nodo con 500 vecinos no domine la suma.
- `σ` — no linealidad, por ejemplo ReLU.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `A` | Matriz de adyacencia: `A_uv = 1` si hay arista entre `u` y `v` | adimensional | Más aristas densifican el grafo: cada nodo mezcla más vecinos por capa y el sobre-suavizado llega antes |
| `Ã` | La adyacencia más la identidad, `A + I` | adimensional | Añade los autoenlaces: cada nodo se envía un mensaje a sí mismo y conserva su información. Quitarlos hace que un nodo aislado quede a ceros |
| `D̃` | Matriz diagonal con el grado contando el autoenlace | vecinos | Al subir el grado, cada arista pesa menos en la normalización simétrica y las sumas no crecen con el número de vecinos |
| `F` | Número de características de entrada por nodo | características | Sube el coste de `W` (que es `F × F'`) y también la información que cada nodo puede propagar |
| `H^(k)` | Matriz `n × F` con las características de todos los nodos | las de las características | Es lo que se propaga: cada capa mezcla el vecindario y acerca las filas entre sí |
| `σ` | No linealidad que se aplica al final de la capa (por ejemplo ReLU) | la de la preactivación | No es un parámetro que se mueva, es una elección. Sin ella, apilar capas equivale a una sola transformación lineal |
| `READOUT` | Operación que resume el grafo entero en un vector | las de las características | Tiene que ser conmutativa (media, suma o pooling con atención) para que el resultado no dependa de cómo numeres los nodos |
:::

Para una tarea de grafo completo (predecir una propiedad de la molécula, no de un átomo), las
representaciones finales se resumen con una operación de lectura `READOUT`, que vuelve a ser
conmutativa: media, suma o un pooling con atención.

## Ejemplo

Camino de cuatro nodos `0—1—2—3`, con autoenlaces y normalización simétrica. Dos
características por nodo:

```
capa 0 (entrada)
nodo 0: [1, 0]
nodo 1: [0, 1]
nodo 2: [1, 1]
nodo 3: [2, 0]

capa 1, sin pesos (W = I) y sin no linealidad
nodo 0: [0.500, 0.408]
nodo 1: [0.742, 0.667]
nodo 2: [1.150, 0.667]
nodo 3: [1.408, 0.408]
```

El nodo 0 solo es vecino del 1 (y de sí mismo), así que su primera característica queda
`0,5·1 + 0,408·0 = 0,5` y la segunda `0,5·0 + 0,408·1 = 0,408`. El nodo 1 mezcla tres
contribuciones: su `[0,1]` con peso `1/3 = 0,333` y los vecinos 0 y 2 con peso
`1/√(3·2) = 0,408`. Fíjate en que el nodo 2, con más vecinos, reparte menos peso en cada uno.

El segundo fenómeno importante es el **sobre-suavizado**. Si aplicas la misma normalización
muchas veces, las representaciones de todos los nodos tienden a la misma dirección (el vector
propio asociado al mayor autovalor de la matriz normalizada). Con características aleatorias de
dimensión 3 en un camino de 6 nodos, la similitud por pares evoluciona así:

```
capas   coseno medio entre pares de nodos
   1            -0.0625
   2            -0.0415
   4             0.0979
   8             0.7973
  32             0.9999
```

Con 32 capas, todos los nodos son prácticamente el mismo vector: la red ha dejado de
distinguirlos y cualquier tarea por nodo se vuelve imposible. Por eso las GNN útiles tienen dos
o tres capas, o usan trucos (conexiones residuales, saltos desde la entrada, normalización por
pares) para poder apilar más.

## Código

```python verificable
import numpy as np

# Camino de 4 nodos con autoenlaces y normalizacion simetrica D^-1/2 A D^-1/2.
A = np.array([[1, 1, 0, 0],
              [1, 1, 1, 0],
              [0, 1, 1, 1],
              [0, 0, 1, 1]], float)
d = A.sum(axis=1)                # grado de cada nodo, contando el autoenlace de la diagonal
# np.outer(d, d) es la matriz d_u * d_v de todos los pares; la raiz de eso divide cada arista
# por la raiz del grado de sus dos extremos, que es la normalizacion simetrica.
A_hat = A / np.sqrt(np.outer(d, d))

H = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, 1.0],
              [2.0, 0.0]])

print("capa 0:")
print(H)
print("capa 1 (cada nodo agrega los mensajes de sus vecinos):")
# @ es el producto matricial: una capa entera de paso de mensajes en una sola operacion.
print(np.round(A_hat @ H, 3))
```

:::claves
- `A.sum(axis=1)` suma **cada fila**, que es exactamente el grado del nodo en esa fila. Con
  `axis=0` obtendrías lo mismo porque `A` es simétrica, pero en un grafo dirigido `axis=0` son
  las aristas que entran y `axis=1` las que salen: confundirlos cambia el modelo.
- `np.outer(d, d)` devuelve la matriz `d_u · d_v` de tamaño `n × n`, y la raíz se aplica a cada
  elemento. La división `A / ...` es elemento a elemento, no una inversión de matrices: no
  confundir con `np.linalg.inv`.
- La división `A / np.sqrt(np.outer(d, d))` solo es segura porque `A` tiene autoenlaces: si un
  nodo tuviera grado 0, la diagonal de `np.outer` sería 0 y saldría una división entre cero con
  su correspondiente aviso.
- `A_hat @ H` es la capa entera sin pesos ni no linealidad. En una GCN de verdad hay que
  multiplicar además por `W` por la derecha, y el orden importa: `A_hat @ H @ W`, porque `H` es
  `n × F` y `W` es `F × F'`.
- `np.linalg.matrix_power(A_hat, capas)` **multiplica la matriz por sí misma** `capas` veces, en
  vez de aplicar una capa con pesos nueva. Es una simplificación para medir el sobre-suavizado;
  una GNN real tendría una `W` distinta por capa.
- `Hk / np.linalg.norm(Hk, axis=1, keepdims=True)` normaliza **cada fila** a norma 1 y deja la
  forma intacta gracias a `keepdims=True`. Sin ese argumento la norma saldría con forma `(n,)` y
  el *broadcasting* dividiría mal.
- `np.triu_indices(n, 1)` da los índices de la parte de arriba de la matriz, es decir, los pares
  `i < j`. Así se cuenta cada par una sola vez y no se incluye la diagonal (un nodo consigo
  mismo), que es lo que interesa al hablar de similitud *entre* nodos.
:::

```python verificable
import numpy as np

# Sobre-suavizado: al apilar capas, todos los nodos acaban pareciendose.
n = 6
# np.eye(n, k=1) es la diagonal desplazada una posicion: sumando la identidad y las dos
# diagonales vecinas sale la matriz de adyacencia de un camino, con autoenlaces incluidos.
A = np.eye(n) + np.eye(n, k=1) + np.eye(n, k=-1)     # camino de 6 nodos
d = A.sum(axis=1)
A_hat = A / np.sqrt(np.outer(d, d))
rng = np.random.default_rng(0)
H = rng.normal(size=(n, 3))

for capas in (1, 2, 4, 8, 32):
    Hk = np.linalg.matrix_power(A_hat, capas) @ H
    Hn = Hk / np.linalg.norm(Hk, axis=1, keepdims=True)   # normalizamos para medir direccion
    # Hn @ Hn.T es la matriz de productos escalares entre todos los pares de nodos: con las
    # filas normalizadas, cada entrada ES el coseno del angulo entre esos dos nodos.
    S = Hn @ Hn.T
    iu = np.triu_indices(n, 1)                            # solo pares distintos
    print(f"capas={capas:>3}  coseno medio entre pares de nodos={S[iu].mean():.4f}")
# -> capas=  1  coseno medio entre pares de nodos=-0.0625
# -> capas=  2  coseno medio entre pares de nodos=-0.0415
# -> capas=  4  coseno medio entre pares de nodos=0.0979
# -> capas=  8  coseno medio entre pares de nodos=0.7973
# -> capas= 32  coseno medio entre pares de nodos=0.9999
```

```python ilustrativo
# Con PyTorch Geometric bastan unas pocas lineas; aqui no se ejecuta.
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class GCN(torch.nn.Module):
    def __init__(self, n_caracteristicas, n_clases):
        super().__init__()
        self.capa1 = GCNConv(n_caracteristicas, 16)   # ya incluye los autoenlaces
        self.capa2 = GCNConv(16, n_clases)

    def forward(self, x, aristas):
        x = F.relu(self.capa1(x, aristas))
        x = F.dropout(x, p=0.5, training=self.training)   # el dropout va sobre las features
        return F.log_softmax(self.capa2(x, aristas), dim=1)
```

## Errores típicos

- **Olvidar los autoenlaces (`Ã = A + I`).** Sin ellos, cada nodo **sustituye** su información
  por la de sus vecinos en lugar de mezclarla. Un nodo aislado (grado 0) se queda con el vector
  de ceros y su representación desaparece. Es el error número uno al implementar la capa a mano.
- **Normalizar con `A / suma` y creer que da igual que la simétrica.** La normalización por filas
  es válida (es la de GraphSAGE), pero cambia el operador y con él el comportamiento: la
  simétrica `D^(−1/2) A D^(−1/2)` mantiene el espectro acotado y reparte el peso entre los dos
  extremos de la arista. Si no normalizas nada, los nodos con grado alto acumulan sumas enormes
  y el entrenamiento explota.
- **Apilar 10 capas porque en una CNN funciona.** Aquí no: con 32 capas el coseno medio entre
  nodos es `0,9999` y la red ya no distingue unos de otros. Dos o tres capas es lo razonable;
  si necesitas más alcance, usa conexiones residuales o propaga de otra forma.
- **Romper la invariancia a la permutación.** Si concatenas las características de los vecinos
  en un orden concreto, o si usas una capa densa sobre `A` aplanada, la red depende de la
  numeración de los nodos. Agrega siempre con operaciones conmutativas.
- **Evaluar con enlaces que conectan entrenamiento y prueba.** En un grafo, las aristas son
  datos: si dejas pasar mensajes entre un nodo de entrenamiento y uno de prueba, el modelo ve
  la etiqueta del vecino y la métrica se infla. Esto es una fuga de datos
  ([[fuga-de-datos|fuga]]) con una forma propia: hay que enmascarar aristas, no solo filas.
- **No comparar con el MLP sobre las características del nodo.** En muchos conjuntos de datos
  reales, un MLP que ignora el grafo rinde casi igual, y a veces mejor si el grafo es ruidoso.
  Una GNN que no supera a ese MLP no está aportando nada y probablemente esté sobreajustando a
  la estructura.

:::practica
enunciado: Grafo 0—1—2—3. Características: nodo 0 = [1, 0], nodo 1 = [0, 1], nodo 2 = [1, 1], nodo 3 = [2, 0]. Aplica una capa que promedia los mensajes de los vecinos SIN autoenlaces. Da la nueva representación de 1, 0 y 3, y explica qué va mal.
pista: Cuenta los vecinos de cada nodo y divide la suma de sus vectores entre ese número.
solucion: Nodo 1 tiene vecinos {0, 2}: suma [1, 0] + [1, 1] = [2, 1], entre 2 → [1,0  0,5]. Nodo 0 solo tiene al 1: suma [0, 1] → [0, 1]. Nodo 3 no tiene vecinos: suma [0, 0], y sin autoenlace su representación queda [0, 0] y el nodo desaparece. Además el nodo 0 ha sustituido su [1, 0] por el del vecino. Los autoenlaces Ã = A + I evitan las dos cosas.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué se añade la identidad a la matriz de adyacencia (Ã = A + I)?
o: Para que la matriz sea invertible y se pueda calcular su inversa
o: Para que cada nodo incluya su propia información al agregar los mensajes de sus vecinos
o: Para duplicar el número de aristas y aumentar la capacidad del modelo
a: 2
e: Sin autoenlaces, la nueva representación de un nodo solo contiene información de sus vecinos y la suya se pierde; un nodo sin vecinos se queda a cero. Añadir la identidad no tiene nada que ver con la invertibilidad ni con la capacidad.
:::

:::quiz
p: Un nodo tiene grado 500 y otro grado 2. ¿Qué hace la normalización D^(−1/2) A D^(−1/2) en la agregación?
o: Dar más peso al nodo con 500 vecinos, porque tiene más información
o: Repartir el peso de cada arista dividiéndolo por la raíz del grado de sus dos extremos, de modo que las sumas no crezcan con el grado
o: Eliminar las aristas de los nodos con grado alto
a: 2
e: La normalización simétrica divide cada arista por √(d_u·d_v), así que un nodo con muchos vecinos aporta menos por cada uno y la magnitud de las representaciones se mantiene acotada. Sin normalizar, las sumas de los nodos populares dominarían el entrenamiento.
:::

:::quiz
p: ¿Qué es el sobre-suavizado en una GNN?
o: Que al apilar muchas capas las representaciones de todos los nodos convergen a la misma dirección y dejan de distinguirse
o: Que el modelo se sobreajusta al conjunto de entrenamiento porque hay demasiados parámetros
o: Que la función de pérdida deja de bajar porque los gradientes se desvanecen en los nodos hoja
a: 1
e: Aplicar repetidamente el operador normalizado lleva a todos los nodos hacia el mismo vector, el asociado al mayor autovalor: en el ejemplo, con 32 capas el coseno medio entre pares es 0,9999. No es sobreajuste ni un problema de gradientes, es una propiedad espectral del operador.
:::
