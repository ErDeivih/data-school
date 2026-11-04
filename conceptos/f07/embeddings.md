---
id: embeddings
titulo: Embeddings
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [producto-punto-y-similitud, norma-y-distancias, encoding-de-categoricas, pca]
tags: [representacion, vectores, similitud, texto]
resumen: Convertir palabras y categorías en vectores densos donde la distancia significa parecido: la base del texto, los recomendadores y la búsqueda semántica.
fuentes: ["Mikolov et al. (2013), 'Efficient Estimation of Word Representations in Vector Space'", "Mikolov et al. (2013), 'Distributed Representations of Words and Phrases and their Compositionality'", "Jurafsky y Martin (2024), 'Speech and Language Processing', cap. 6"]
---

## En una frase

Un embedding es una tabla que asigna a cada objeto (una palabra, un producto, un usuario) un
vector de números aprendidos, colocado de forma que dos objetos parecidos queden cerca y el
parecido se pueda medir con un producto punto o una distancia.

## La idea

Supón que quieres representar 50.000 palabras para un modelo. La forma obvia es el *one-hot*: un
vector de 50.000 ceros con un 1 en la posición de la palabra. Funciona y es fácil de generar,
pero tiene dos defectos graves.

El primero es el tamaño: 50.000 números por palabra, de los que 49.999 son ceros. El segundo es
peor: **todos los pares de palabras están igual de lejos**. El [[producto-punto-y-similitud|producto
punto]] entre «perro» y «cachorro» es 0, exactamente igual que entre «perro» y «helicóptero». Para
el modelo, todas las palabras son igual de distintas entre sí, y tiene que aprender desde cero
que son parecidas usando los ejemplos.

Un embedding da la vuelta a eso. En vez de un vector enorme y vacío, cada palabra recibe un
vector corto y **denso** —de 50 a 1.000 números, casi todos distintos de cero— que se aprende a
partir del uso. La idea que lo hace funcionar es la hipótesis distribucional: dos palabras que
aparecen en los mismos contextos tienden a significar cosas parecidas. Si el modelo ve
«el perro ladra» y «el cachorro ladra», acabará poniendo sus vectores cerca porque ambos
predicen «ladra».

Eso da la propiedad que buscábamos: **la distancia pasa a significar algo**. Puedes medirla,
ordenar vecinos, hacer búsquedas por similitud o alimentar un clasificador con esos vectores en
lugar de con texto.

Tres cosas que conviene tener claras desde el principio:

1. **El embedding no es un diccionario, es una función aprendida de la tarea.** Los vectores se
   ajustan para predecir algo concreto (la palabra del contexto, la siguiente palabra, si dos
   frases son equivalentes). Si cambias el objetivo, cambian los vectores.
2. **No hay un embedding universal.** Los vectores de dos modelos distintos viven en espacios
   distintos y **no son comparables** aunque tengan la misma dimensión. Mezclarlos sin más es un
   error clásico.
3. **Cerca no es sinónimo de parecido.** Los antónimos aparecen muy cerca porque aparecen en
   contextos casi idénticos («subió» y «bajó» se usan igual). La similitud captura
   distribución, no significado.

## Definición formal

Un embedding es una matriz `E` de forma `V × d`:

- `V` — tamaño del vocabulario o del catálogo: cuántos objetos distintos hay.
- `d` — dimensión del embedding: cuántos números tiene cada vector. Es un hiperparámetro.
- `E[i]` — la fila `i`, el vector del objeto `i`. Se llama *embedding lookup* porque consultar el
  embedding de un token es leer una fila, y equivale a multiplicar su one-hot por `E`:
  `e_i = onehot(i) · E`.

**Similitud.** La medida habitual es el coseno, que compara direcciones e ignora la longitud:

:::formula
cos(u, v) = (u · v) / (‖u‖ · ‖v‖) ∈ [−1, 1]
:::

- `u · v` — producto punto: `Σⱼ uⱼ vⱼ`.
- `‖u‖` — [[norma-y-distancias|norma euclídea]]: `√(Σⱼ uⱼ²)`.
- Vale 1 si apuntan en la misma dirección, 0 si son perpendiculares y −1 si son opuestos.
- La distancia euclídea `‖u − v‖` da un orden distinto si los vectores tienen longitudes muy
  diferentes; por eso, si el modelo se entrenó con coseno, normaliza antes de comparar.

**Cómo se aprenden.** En *skip-gram* con muestreo negativo, para cada par (centro `c`, contexto
`o`) que aparece junto en el corpus se maximiza:

:::formula
log σ(u_o · v_c) + Σ_{k=1}^{K} E_{w_k ∼ P_n} [ log σ(−u_{w_k} · v_c) ]
:::

- `v_c` — vector de la palabra centro; `u_o` — vector de una palabra del contexto. Son dos
  matrices distintas (`V` y `U`) que se aprenden a la vez.
- `σ(x) = 1/(1+e^{−x})` — sigmoide.
- `K` — número de negativos por ejemplo positivo.
- `P_n` — distribución de la que se extraen palabras que **no** aparecen en el contexto. Sin
  negativos, el objetivo exigiría normalizar sobre todo el vocabulario en cada paso, que con
  50.000 palabras es carísimo.
- Al maximizar, el producto punto de los pares reales sube y el de los falsos baja: exactamente
  el efecto que queremos.

**Dimensión.** Valores típicos: 50-100 para vocabularios pequeños, 300 para word2vec clásico,
768-1.536 para embeddings de frases de modelos grandes. Más dimensión separa más matices pero
necesita más datos por objeto; con un catálogo de 200 productos, 300 dimensiones solo pueden
sobreajustar.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `E` | la tabla de embeddings: una fila por objeto | adimensional | Es lo que se aprende. Su tamaño es `V · d` números: crece en línea recta con el vocabulario y con la dimensión, y no cambia según la tarea |
| `V` | tamaño del vocabulario o del catálogo | objetos | Cada objeto nuevo son `d` números más que aprender. Con `V` grande y pocos datos por objeto, los vectores de los objetos raros apenas se entrenan y quedan casi en su inicialización aleatoria |
| `d` | dimensión del embedding | números por objeto | Más dimensión separa más matices y necesita más datos por objeto. Con un catálogo de 200 productos, pasar de 64 a 300 dimensiones no añade información: añade memoria y sobreajuste |
| `u`, `v` | dos vectores del espacio | adimensional | Lo que importa no son sus módulos, sino el ángulo: el coseno no cambia si multiplicas uno de los dos por 10. Si el modelo se entrenó con coseno, normaliza antes de comparar |
| `u · v` | producto punto entre los dos vectores | adimensional | Crece con la dimensión y con los módulos, no solo con el parecido. Con vectores sin normalizar, un vector «largo» se parece a todo |
| `‖u‖` | norma euclídea del vector | las del vector | Escala el coseno: es el divisor que quita el efecto del tamaño. Con `‖u‖` o `‖v‖` iguales a cero, el coseno es indefinido y sale `nan` |
| `σ` | sigmoide, que convierte la puntuación en probabilidad | entre 0 y 1 | Aplasta todo lo que esté por encima de 6 o por debajo de −6: con productos punto grandes la sigmoide se satura y el gradiente del par se apaga |
| `K` | número de negativos por ejemplo positivo | negativos | Más negativos por par dan un gradiente menos ruidoso y un entrenamiento más lento y más caro. Los valores habituales van de 5 a 20 |
| `P_n` | distribución de la que salen los negativos | adimensional | Si muestrea demasiado las palabras muy frecuentes, el modelo solo aprende a separar lo trivial; la corrección habitual es elevar la frecuencia a 3/4 |
:::

## Ejemplo

Un vocabulario de 50.000 palabras con vectores de 300 números en float32:

- Tabla de embeddings: 50.000 · 300 · 4 = **60 MB**. Es un tensor normal y corriente.
- La misma información en one-hot denso: 50.000 · 4 = 200.000 bytes = **195 KiB por palabra**,
  y **10 GB** si guardaras las 50.000.
- Y con el one-hot, el coseno entre «perro» y «cachorro» es **0**, exactamente igual que entre
  «perro» y «helicóptero».

Con una tabla diminuta de cuatro filas y cuatro dimensiones se ve el efecto completo:

| objeto | dim 1 | dim 2 | dim 3 | dim 4 |
| --- | --- | --- | --- | --- |
| gato | 0,9 | 0,1 | 0,0 | 0,0 |
| perro | 0,8 | 0,2 | 0,1 | 0,0 |
| coche | 0,0 | 0,1 | 0,9 | 0,2 |
| moto | 0,1 | 0,0 | 0,8 | 0,3 |

- Coseno entre gato y perro: **0,984**.
- Coseno entre coche y moto: **0,978**.
- Coseno entre gato y coche: **0,012**.

El modelo no «sabe» qué es un gato: ha colocado los dos animales en una zona del espacio y los
dos vehículos en otra porque en el corpus aparecían en contextos parecidos.

:::figura
fichero: embeddings-geometria-y-coseno
pie: La izquierda dibuja cuatro palabras como flechas desde el origen. Es un espacio de dos dimensiones, pero la idea es la misma que en 300: lo que se compara es la dirección, no el largo de la flecha, y por eso la medida es el coseno. Los dos animales apuntan casi igual (coseno 0,99) y los dos vehículos también (0,99), mientras que un animal y un vehículo quedan casi perpendiculares (0,06). Esa es toda la propiedad que buscábamos cuando cambiamos el one-hot por embeddings: ahora se puede medir el parecido, ordenar vecinos y hacer búsquedas por similitud. La derecha pone las dos representaciones frente a frente con las mismas palabras. Con one-hot el coseno es 0 en todos los pares, da igual que sean «perro» y «cachorro» o «perro» y «helicóptero»: el modelo no recibe ninguna pista y tiene que aprender el parecido a base de ejemplos. Con embeddings, el par que aparece en contextos parecidos queda en 0,99 y el que no tiene nada que ver, en 0,06. Dos avisos que la figura no puede enseñar y conviene tener presentes: un coseno alto significa «aparece en contextos parecidos», no «significa lo mismo» (los antónimos salen pegados), y los vectores de dos entrenamientos distintos no son comparables aunque tengan la misma dimensión: cada uno vive en su propio sistema de coordenadas.
fuente: figuras/embeddings-1.py
:::

## Código

```python verificable
import numpy as np

# Una tabla de embeddings es una matriz V x d: cada fila es un objeto.
V, d = 50000, 300
# Los 4 son los bytes de un float32; /1e6 pasa a MB decimales y /1024 a KiB binarios.
print("tabla densa:", V * d * 4 / 1e6, "MB")          # -> 60.0 MB
print("one-hot por palabra:", V * 4 / 1024, "KiB")    # -> 195.3125 KiB
print("todas one-hot:", V * V * 4 / 1e9, "GB")        # -> 10.0 GB

# Consultar un embedding es multiplicar el one-hot por la tabla: devuelve la fila.
E = np.array([[0.9, 0.1, 0.0, 0.0],    # gato
              [0.8, 0.2, 0.1, 0.0],    # perro
              [0.0, 0.1, 0.9, 0.2],    # coche
              [0.1, 0.0, 0.8, 0.3]])   # moto
# El one-hot por la matriz devuelve una fila NUEVA; E[1] seria una vista sobre la tabla.
print("fila recuperada:", (np.array([0.0, 1.0, 0.0, 0.0]) @ E).tolist())
# -> [0.8, 0.2, 0.1, 0.0]

def cos(u, v):
    # Sin axis, np.linalg.norm devuelve la norma de todo el vector aplanado, no la de cada
    # fila: con matrices de varios vectores habria que pasar axis=-1.
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))

print("coseno one-hot:", cos(np.array([1.0, 0, 0, 0]), np.array([0.0, 1, 0, 0])))  # -> 0.0
print("coseno denso  :", round(cos(E[0], E[1]), 3))                               # -> 0.984
print("coseno ajeno  :", round(cos(E[0], E[2]), 3))                               # -> 0.012
```

:::claves
- `np.array([0.0, 1.0, 0.0, 0.0]) @ E` equivale a `E[1]`, pero **no** es lo mismo por dentro:
  `E[1]` es una **vista** de la fila de la tabla (escribir en ella cambiaría el embedding),
  mientras que el producto devuelve un array nuevo. Por eso una capa de embeddings real es una
  consulta por índice, no una multiplicación por un one-hot de 50.000 ceros.
- `E` es de tipo `float64` porque todos los literales llevan decimales, y hay que conservarlos. No
  es una precaución contra la división entera: `u @ v` sí sería entero, pero `np.linalg.norm(u)`
  devuelve un `float64`, así que `/` es una división flotante y el coseno no se truncaría. Lo que
  cambia al quitar los `.0` son los valores del ejemplo —0,9 pasa a 0— y las filas se quedan a
  cero, con lo que el coseno sale `nan`.
- `np.linalg.norm(u)` sin `axis` calcula la norma del array **aplanado**. Con un vector va bien;
  con una matriz de 1.000 embeddings devuelve un solo número en lugar de 1.000 normas, y el
  cociente deja de ser un coseno. Hay que pasar `axis=-1` (o `axis=1`).
- El `float(...)` del final convierte el `numpy.float64` en un `float` de Python. Sin él,
  `round` mantiene el tipo de numpy y el formato impreso cambia según la versión.
- `E[0]` y `E[1]` son vistas, así que `cos` recibe la fila sin copiarla: no gasta memoria, pero
  tampoco la protege. Si una función modificara su argumento, estaría tocando la tabla.
- En la segunda pieza, `U[c] -= 0.5 * g * V[obj]` es una resta **en el sitio** sobre una vista:
  modifica `U` de verdad, no una copia. Y el `Uc = U[c].copy()` de la línea anterior es
  obligatorio porque la fila se usa dos veces: sin la copia, la actualización de `V[obj]` usaría
  el `U[c]` ya actualizado y el par se alejaría en vez de acercarse.
:::

```python verificable
import numpy as np

# Entrenar embeddings de juguete: acercar los pares que coocurren y alejar los negativos.
pares = [(0, 1), (1, 0), (2, 3), (3, 2)]      # gato-perro y coche-moto
rng = np.random.default_rng(0)
d = 8
U = rng.normal(0, 0.1, (4, d))                # vectores de centro
V = rng.normal(0, 0.1, (4, d))                # vectores de contexto
sig = lambda x: 1 / (1 + np.exp(-x))

for _ in range(3000):
    for c, o in pares:
        negs = [j for j in range(4) if j != c]
        negativos = [(negs[int(rng.integers(0, len(negs)))], 0.0) for _ in range(2)]
        for obj, etiqueta in [(o, 1.0)] + negativos:
            g = sig(float(U[c] @ V[obj])) - etiqueta
            Uc = U[c].copy()                  # copia antes de tocar la fila: se usa dos veces
            U[c] -= 0.5 * g * V[obj]
            V[obj] -= 0.5 * g * Uc

cos = lambda a, b: float(U[a] @ U[b] / (np.linalg.norm(U[a]) * np.linalg.norm(U[b])))
print("gato-perro:", round(cos(0, 1), 3))    # -> 0.998
print("coche-moto:", round(cos(2, 3), 3))    # -> 0.95
print("gato-coche:", round(cos(0, 2), 3))    # -> -0.038
```

```python ilustrativo
from sentence_transformers import SentenceTransformer
import numpy as np

# Un modelo preentrenado de frases: el mismo espacio para frases y para consultas.
modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
vectores = modelo.encode(["un perro ladra", "un cachorro ladra", "sube el precio del pan"],
                         normalize_embeddings=True)   # normalizar: el coseno es un producto punto

similitud = vectores @ vectores.T
for i in range(3):
    print(round(float(similitud[i, 0]), 3))
```

## Errores típicos

- **Comparar embeddings entrenados por separado.** Los vectores de dos modelos distintos no
  comparten sistema de coordenadas: la dimensión puede coincidir y el espacio no tener nada que
  ver. Si necesitas compararlos, entrena una proyección con pares de palabras alineadas o usa el
  mismo modelo para todo.
- **Usar distancia euclídea cuando el modelo se entrenó con coseno.** Un vector de norma 5 y otro
  de norma 0,5 pueden tener coseno 1 y estar «lejos» en distancia euclídea. Normaliza los
  vectores antes de calcular la distancia, o usa el producto punto directamente.
- **Leer la geometría como si fuera semántica.** Ni cada dimensión significa un concepto («animal»,
  «femenino») ni las analogías son una capacidad fiable: el ejemplo de rey menos hombre más mujer
  cae cerca de reina en algunos corpus y falla en muchos otros. El significado está repartido por
  todas las coordenadas, y el espacio refleja coocurrencia, no lógica. Si necesitas
  interpretabilidad, usa [[pca]] o un método de atribución; si necesitas razonamiento, no lo
  pidas a la distancia entre vectores.
- **Confundir cercanía con sinonimia.** Los antónimos y las palabras que solo comparten registro
  («bueno» y «malo», «subir» y «bajar») acaban muy cerca porque su contexto es casi idéntico. Si
  tu tarea depende de distinguirlos, la similitud de embeddings no es suficiente.
- **Aprender embeddings de categorías dentro del mismo conjunto de entrenamiento.** Es la versión
  vectorial del [[encoding-de-categoricas|target encoding]]: si los vectores se ajustan con las
  etiquetas que luego usas para evaluar, hay [[fuga-de-datos|fuga de datos]] y la métrica de
  validación sale inflada. Aprende los embeddings solo con el pliegue de entrenamiento.
- **Elegir la dimensión por costumbre.** Con pocos objetos por categoría, una dimensión alta
  memoriza: el modelo puede dar a cada objeto un vector casi único. Empieza bajo (16-64), mide en
  validación y sube solo si hace falta.

:::practica
enunciado: Un modelo da a «perro» el vector p = (0,8  0,2) y a «cachorro» el vector c = (1,4  0,2). Calcula el coseno entre los dos y la distancia euclídea entre los dos. ¿Cuál de las dos medidas dice que son parecidos, y por qué la otra engaña?
pista: El coseno ignora las longitudes; la distancia euclídea no.
solucion: p·c = 0,8·1,4 + 0,2·0,2 = 1,12 + 0,04 = 1,16. ‖p‖ = √0,68 = 0,825, ‖c‖ = √2,0 = 1,414. Coseno = 1,16 / (0,825 · 1,414) = 1,16 / 1,166 = 0,995. La distancia es √(0,6² + 0²) = 0,6. El coseno dice que son casi la misma dirección (0,995); la distancia sale grande solo porque c es más largo. Normaliza antes de comparar y las dos medidas coinciden.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia práctica más importante entre representar palabras con one-hot y con embeddings?
o: El one-hot ocupa más memoria, pero la similitud entre palabras es la misma
o: Con one-hot todas las palabras están a la misma distancia; con embeddings, la distancia refleja parecido aprendido del contexto
o: Los embeddings siempre dan mejores resultados en cualquier tarea
a: 2
e: El one-hot hace que el producto punto entre dos palabras distintas sea siempre 0, así que el modelo no tiene ninguna pista de parecido y debe aprenderlo de los ejemplos. Los embeddings colocan cerca lo que aparece en contextos parecidos. Lo de la memoria también es cierto (195 KiB por palabra frente a 1,2 KB con 300 dimensiones), pero lo que cambia el juego es la geometría, no el tamaño.
:::

:::quiz
p: Entrenas embeddings con un corpus y con otro distinto. ¿Puedes comparar directamente el vector de «gato» de uno con el del otro?
o: Sí, si los dos tienen la misma dimensión
o: No: cada entrenamiento define su propio sistema de coordenadas y los espacios no están alineados
o: Sí, si normalizas los dos vectores antes de comparar
a: 2
e: Que la dimensión coincida no alinea nada: cada modelo parte de inicializaciones aleatorias y llega a una solución distinta, con rotaciones y reflexiones arbitrarias del mismo espacio. Normalizar arregla longitudes, no orientaciones. Para comparar hace falta proyectar uno sobre el otro con pares de palabras alineadas, o usar el mismo modelo.
:::

:::trampa
Si un vecino más cercano de «excelente» en tu espacio de embeddings es «pésimo», no está roto: es
lo esperable. Los antónimos comparten contexto casi perfecto. Antes de montar un buscador o un
sistema de recomendación sobre similitud, inspecciona a mano los vecinos de veinte palabras
representativas de tu dominio: es la comprobación más barata y la que más sorpresas evita.
:::
