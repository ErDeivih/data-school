---
id: arboles-de-decision
titulo: Árboles de decisión
fase: 6
nivel: básico
rutas: [ds]
prerequisitos: [paradigmas-de-aprendizaje, metricas-de-clasificacion]
tags: [arboles, gini, sobreajuste, interpretabilidad]
resumen: Dividir los datos con preguntas binarias eligiendo el corte que más reduce la impureza: potente, interpretable y adicto al sobreajuste.
fuentes: ["Breiman et al. (1984), 'Classification and Regression Trees'", "Quinlan (1986), 'Induction of Decision Trees'"]
---

## En una frase

Un árbol de decisión predice haciendo preguntas de sí o no sobre las variables y bajando por la
rama correspondiente, y en cada paso elige la pregunta que deja los grupos resultantes lo más
«puros» posible, es decir, con la mayor proporción de una sola clase.

## La idea

Es el modelo de machine learning que se explica sin pizarra. Para saber si un correo es spam
preguntas: ¿contiene la palabra «gratis»? Si sí, ¿tiene adjunto? Y así hasta llegar a una hoja,
donde el árbol da su respuesta. Cada pregunta es una comparación: `x ≤ 3,5`, `ciudad = Madrid`,
`sí` o `no`.

El árbol se construye de arriba abajo y de forma **glotona**: en cada nodo prueba todos los
cortes posibles de todas las variables y se queda con el que mejor separa las clases *ahora*,
sin mirar si ese corte será útil tres niveles más abajo. No busca el árbol óptimo global (eso
es un problema computacionalmente intratable); busca el mejor corte local y sigue. Funciona
sorprendentemente bien, y a cambio puede quedarse atrapado en decisiones tempranas mejorables.

La pregunta operativa es qué significa «mejor separa». Ahí entran las medidas de **impureza**:
Gini y entropía. Ambas valen 0 cuando un nodo tiene una sola clase (puro) y son máximas cuando
las clases están a partes iguales. Para elegir el corte, el árbol calcula la impureza del nodo
padre, la compara con la media ponderada de la impureza de los dos hijos y elige el corte que
más reduce esa diferencia. Gini y entropía casi siempre eligen el mismo corte; la diferencia
importa poco en la práctica.

El defecto estructural del árbol es que puede seguir preguntando hasta que cada hoja tenga un
único ejemplo. Si lo dejas crecer sin límite, acierta el 100 % de los datos de entrenamiento y
falla más fuera de muestra: ha memorizado en lugar de aprender. Eso es sobreajuste en estado
puro, y se controla de dos formas:

- **Podando antes** (pre-poda): limitar la profundidad máxima, exigir un número mínimo de
  ejemplos por hoja o un mínimo de ejemplos para dividir un nodo.
- **Podando después** (post-poda): dejar crecer el árbol y recortar las ramas que no aportan
  mejora suficiente en un conjunto de validación. En scikit-learn se hace con el parámetro
  `ccp_alpha`: a mayor valor, más agresiva la poda.

Otra limitación que conviene tener presente: los cortes son **perpendiculares a los ejes**.
Una frontera diagonal entre dos clases obliga al árbol a dibujar una escalera con muchos
escalones, mientras que un modelo lineal la resuelve con una sola recta. Y el árbol es
**inestable**: cambia tres ejemplos del conjunto de entrenamiento y la primera división puede
ser otra, con un árbol completamente distinto. Esa inestabilidad es justamente lo que arreglan
[[bagging-y-random-forest|los ensembles de árboles]].

## Definición formal

Sea un nodo con `n` observaciones y `K` clases, y `p_k` la proporción de observaciones de la
clase `k` en ese nodo (por lo tanto, `Σ_k p_k = 1`).

:::formula
Gini = 1 − Σ_k p_k²          Entropía = − Σ_k p_k · log₂(p_k)
:::

- `K` — número de clases.
- `p_k` — proporción de ejemplos de la clase `k` en el nodo.
- `log₂` — logaritmo en base 2, para medir la entropía en bits.

Un corte candidato divide el nodo en dos hijos, izquierdo (`izq`) y derecho (`der`), de tamaños
`n_izq` y `n_der`. La **ganancia** del corte es la reducción de impureza ponderada:

:::formula
Ganancia = Impureza(padre) − ( n_izq/n · Impureza(izq) + n_der/n · Impureza(der) )
:::

El árbol evalúa esa ganancia para cada variable y cada punto de corte posible, y se queda con
el máximo. En un **árbol de regresión** la impureza es la varianza (o el error cuadrático medio)
y la predicción de cada hoja es la media de los valores que caen en ella.

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa con la ganancia si sube |
| --- | --- | --- | --- |
| `n` | Observaciones que han llegado al nodo | casos | No la cambia por sí sola: solo reparte el peso de la media ponderada |
| `K` | Número de clases del problema | clases | La impureza máxima sube (la entropía llega a `log₂K`): hay más que separar y los cortes ganan valor |
| `p_k` | Proporción de la clase `k` dentro del nodo | tanto por uno, suman 1 | Cuanto más se acerca a 1 en una sola clase, más puro es el nodo y menos queda por ganar |
| `Impureza(padre)` | Gini o entropía del nodo que se quiere partir | bits (entropía) o adimensional (Gini) | Es el techo de la ganancia: no se puede ganar más de lo que hay |
| `n_izq/n` | Fracción de casos que se van al hijo izquierdo | tanto por uno | Pesa a ese hijo en la media; como los dos pesos suman 1, subir uno baja el otro |
| `Impureza(izq)`, `Impureza(der)` | Impureza de cada hijo tras el corte | igual que la del padre | Si sube la de un hijo, la ganancia baja: el corte deja un grupo más mezclado |
| `max_depth` | Profundidad máxima que se le permite al árbol | niveles | La ganancia de entrenamiento sube, pero deja de servir fuera de muestra |
| `ccp_alpha` | Fuerza de la poda posterior | adimensional | Recorta ramas: baja la ganancia en entrenamiento y sube el acierto en datos nuevos |
:::

:::figura
fichero: arboles-impureza-y-sobreajuste
pie: A la izquierda, Gini y entropía dibujan casi la misma curva, y por eso da igual cuál elijas para buscar el corte; el error de la clase mayoritaria, en cambio, es plano a tramos y no distingue matices. Las dos primeras caen a cero en los nodos puros, que es justo lo que persigue el árbol. A la derecha está el precio de no podar: el acierto de entrenamiento llega al 100 % en cuanto el árbol crece sin límite, mientras el acierto en datos que no ha visto se queda en 0,68 y no mejora. La distancia entre las dos curvas es el sobreajuste, y la conclusión práctica es que la profundidad se elige con un conjunto de validación, nunca con el de entrenamiento.
fuente: figuras/arboles-de-decision-1.py
:::

## Ejemplo

Doce correos: 6 spam y 6 normales. El nodo raíz tiene impureza de Gini
`1 − (0,5² + 0,5²) = 0,5`. Dos cortes candidatos:

- **Corte A, «contiene la palabra gratis»:** deja 6 correos con 1 spam y 5 normales, y otros 6
  con 5 spam y 1 normal. La impureza de cada hijo es `1 − (1/6)² − (5/6)² = 0,2778`. Ganancia:
  `0,5 − 0,2778 = 0,2222`.
- **Corte B, «contiene la palabra hola»:** deja 6 con 2 spam y 4 normales, y 6 con 4 spam y 2
  normales. Impureza `1 − (2/6)² − (4/6)² = 0,4444`. Ganancia: `0,5 − 0,4444 = 0,0556`.

Gana el corte A, cuatro veces más ganancia que el B. Ojo con el detalle de que la impureza de
los hijos es la misma en las dos ramas del corte A: lo que importa no es que un hijo quede muy
puro, sino que los dos queden puros, porque un hijo puro y otro muy mezclado apenas reducen la
impureza total.

Y aquí aparece el sobreajuste. Si sigues cortando, puedes llegar a hojas con un solo correo:
impureza 0 en todas, ganancia total 0,5, y acierto del 100 % en entrenamiento. Basta con que uno
de esos correos sea raro (un correo normal que dice «gratis») para que el árbol tenga una regla
absurda y la aplique con total confianza.

## Código

```python verificable
import numpy as np

def gini(conteos):
    p = np.asarray(conteos, dtype=float)
    p = p / p.sum()
    return 1 - (p ** 2).sum()

def entropia(conteos):
    c = np.asarray(conteos, dtype=float)
    p = c[c > 0] / c.sum()
    return -(p * np.log2(p)).sum() + 0.0

for conteos in ([6, 6], [2, 4], [1, 5], [0, 6]):
    print(f"nodo {str(conteos):<9} gini {gini(conteos):.4f}  entropia {entropia(conteos):.4f}")
# -> nodo [6, 6]    gini 0.5000  entropia 1.0000
# -> nodo [2, 4]    gini 0.4444  entropia 0.9183
# -> nodo [1, 5]    gini 0.2778  entropia 0.6500
# -> nodo [0, 6]    gini 0.0000  entropia 0.0000
```

:::claves
- `gini()` y `entropia()` **no imprimen nada**: devuelven un número. Lo que se ve en pantalla lo
  escribe el `print` del bucle. Si llamas a la función y no la metes en un `print`, no aparece nada.
- `np.asarray(conteos, dtype=float)` convierte la lista de Python en un array de NumPy y, de paso,
  en números con decimales. Ojo: la barra `/` de NumPy **siempre** divide de verdad, aunque el array
  sea de enteros; la que trunca es `//`. Aquí el `dtype=float` evita sorpresas como
  `np.asarray([1, 3, 5]) // 9`, que da `[0, 0, 0]` y deja el Gini en `nan`: al dividir entre una
  suma que vale 0, NumPy calcula `0/0` y avisa de la división inválida.
- `p = p / p.sum()` es una división de todo el array a la vez: NumPy reparte cada elemento entre la
  suma. El array original **no se toca**, porque `p / p.sum()` crea uno nuevo; solo `p /= p.sum()`
  lo modificaría en el sitio.
- `np.log2(0)` daría `-inf` y un aviso. Por eso `entropia()` se queda antes con `c[c > 0]`: quita
  los ceros. En `[6, 6]` no se nota, pero en `[0, 6]` es lo que hace que salga 0 en vez de `nan`.
- El `+ 0.0` del final **no** convierte el resultado en un `float` de Python: sigue siendo un
  `np.float64` (el `0.0` se suma como escalar de NumPy). Para tener un `float` de verdad hay que
  envolverlo: `float(entropia(conteos))`. En pantalla se imprimen igual, pero al guardar en un JSON
  o al comparar con `is` la diferencia aparece.
- Cambia `max_depth=None` por `max_depth=3` en el segundo bloque y el acierto de entrenamiento cae
  de 1,000 a 0,772 mientras el de prueba sube de 0,650 a 0,717: esa es toda la diferencia entre
  memorizar y aprender, y se ve en una sola línea.
:::

```python verificable
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(0)
X = rng.normal(size=(300, 4))
y = (X[:, 0] + X[:, 1] > 0).astype(int)
y = np.where(rng.random(300) < 0.15, 1 - y, y)      # 15 % de etiquetas cambiadas al azar

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

for prof in (1, 3, None):
    arbol = DecisionTreeClassifier(max_depth=prof, random_state=0).fit(X_tr, y_tr)
    print(f"profundidad {str(prof):>4}  train {arbol.score(X_tr, y_tr):.3f}  test {arbol.score(X_te, y_te):.3f}")
# -> profundidad    1  train 0.678  test 0.658
# -> profundidad    3  train 0.772  test 0.717
# -> profundidad None  train 1.000  test 0.650
```

## Errores típicos

- **Dejar crecer el árbol y reportar el acierto de entrenamiento.** Un árbol sin límite da
  1,000 en entrenamiento y rinde peor en prueba (0,650 frente a 0,717 con profundidad 3) porque
  ha memorizado el ruido. Fija `max_depth` o `min_samples_leaf`, o poda con `ccp_alpha`.
- **Podar mirando el conjunto de prueba.** La poda necesita un conjunto de validación propio;
  si eliges la profundidad con el test, ese test deja de ser una estimación honesta y el número
  que publiques estará inflado.
- **Leer la importancia por impureza como la verdad.** Esa medida favorece a las variables con
  más valores distintos (las continuas, y las categóricas con muchas categorías) porque tienen
  más cortes donde elegir. Para comparar variables, usa importancia por permutación sobre datos
  no vistos.
- **Creer que los cortes son la frontera real del problema.** Un árbol solo dibuja escalones
  paralelos a los ejes. Una frontera diagonal necesita muchos cortes, y con datos escasos el
  árbol la aproxima mal. Un modelo lineal, una [[svm]] con núcleo o una red resuelven ese caso
  con mucho menos.
- **Confundir los caminos del árbol con reglas causales.** Que un nodo diga «si el importe es
  mayor que 1.200, impaga» describe una regularidad en los datos de entrenamiento, no un
  mecanismo. Con variables correlacionadas, el árbol puede elegir cualquiera de las dos para el
  primer corte.
- **No fijar la semilla y no poder reproducirlo.** El árbol en sí es determinista, pero los
  empates entre cortes y el muestreo de datos se rompen con azar: sin `random_state` no puedes
  reproducir tu propio resultado, ni tú ni quien revise tu trabajo.

:::practica
enunciado: Un nodo con 10 solicitudes tiene 4 impagos y 6 clientes al día. El corte por «importe > 1.000 €» deja 4 impagos y 1 al día a un lado, y 0 impagos y 5 al día al otro. Calcula el Gini del padre y de los hijos, la ganancia del corte y decide si supera el umbral de 0,05.
pista: El Gini de un nodo es 1 menos la suma de las proporciones al cuadrado, y la ganancia resta al padre la media de los hijos ponderada por su tamaño.
solucion: Padre: 1 − (0,4² + 0,6²) = 1 − 0,52 = 0,48. Hijo izquierdo, 5 casos con 4 impagos: 1 − (0,8² + 0,2²) = 0,32. Hijo derecho, 5 casos puros: 0. Ganancia = 0,48 − (5/10 · 0,32 + 5/10 · 0) = 0,48 − 0,16 = 0,32, por encima de 0,05: el corte se acepta.
:::

## Comprueba que lo sabes

:::quiz
p: Un nodo tiene 6 casos de la clase A y 6 de la clase B. Un corte lo divide en 1A/5B y 5A/1B, y otro en 2A/4B y 4A/2B. ¿Cuál elige el árbol?
o: El primero, porque su ganancia de Gini es 0,2222 frente a 0,0556 del segundo
o: El segundo, porque reparte los datos de forma más equilibrada
o: Los dos son equivalentes, porque los dos dejan 12 casos en total
a: 1
e: El primero reduce la impureza de 0,5 a 0,2778 en los dos hijos (ganancia 0,2222); el segundo solo baja a 0,4444 (ganancia 0,0556). El árbol busca la mayor reducción de impureza, no el reparto más equilibrado.
:::

:::quiz
p: ¿Qué significa que un árbol de decisión haga divisiones «glotonas» (greedy)?
o: Que elige en cada nodo el mejor corte local sin garantizar el árbol óptimo global
o: Que usa todos los datos en cada nodo para no desperdiciar información
o: Que poda las ramas al final para quedarse con las mejores
a: 1
e: La elección es local: el mejor corte ahora, sin evaluar las consecuencias a más profundidad. Encontrar el árbol óptimo global es intratable, así que se acepta esta aproximación. La poda es un paso posterior y distinto.
:::

:::quiz
p: Tu árbol sin límite de profundidad da 0,99 de acierto en entrenamiento y 0,72 en prueba. ¿Qué es lo primero que pruebas?
o: Añadir más variables al modelo
o: Limitar la profundidad o exigir un mínimo de ejemplos por hoja
o: Cambiar la métrica de impureza de Gini a entropía
a: 2
e: La diferencia entre entrenamiento y prueba es la firma del sobreajuste, y el árbol creció hasta memorizar. Limitar la profundidad o el tamaño mínimo de hoja ataca directamente la causa. Cambiar Gini por entropía apenas mueve los cortes y no resuelve el problema.
:::

:::aviso
Un árbol de decisión se lee muy bien y por eso engaña: la facilidad para explicarlo no dice
nada sobre si es cierto. Antes de presentar un árbol como «las reglas del negocio», comprueba
su rendimiento en datos que no haya visto y cuánto cambian las reglas si reentrenas con una
muestra distinta.
:::
