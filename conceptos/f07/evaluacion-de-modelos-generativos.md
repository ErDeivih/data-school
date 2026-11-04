---
id: evaluacion-de-modelos-generativos
titulo: Evaluar un modelo generativo
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [gan, modelos-de-difusion, metricas-de-clasificacion]
tags: [generativos, metricas, evaluacion, diversidad, fidelidad]
resumen: Fidelidad frente a diversidad: por qué ninguna métrica sola dice si un modelo generativo es bueno, qué mide cada número y cómo evaluar sin engañarse.
fuentes: ["Heusel et al. (2017), 'GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium'", "Sajjadi et al. (2018), 'Assessing Generative Models via Precision and Recall'", "Borji (2019), 'Pros and Cons of GAN Evaluation Measures'"]
---

## En una frase

Un modelo generativo puede fallar de dos maneras opuestas —no parecerse a los datos o no cubrirlos—
y una sola métrica no distingue una de otra: hay que medir fidelidad y diversidad por separado.

## La idea

Piensa en un falsificador de billetes. Uno copia un billete de diez con una perfección
insultante, pero solo sabe hacer ese. Otro produce manchas de colores variados que no se parecen
a ningún billete. El primero tiene una fidelidad perfecta y una diversidad nula; el segundo, lo
contrario. Ninguno de los dos te sirve para pagar el café, y sin embargo un solo número puede
puntuar mejor al segundo.

Entrenar un modelo generativo tiene exactamente ese problema. Una [[gan|red generativa adversaria]]
cuyo generador ha colapsado en un modo produce imágenes nítidas y creíbles de una sola clase; un
[[modelos-de-difusion|modelo de difusión]] mal entrenado produce variedad de manchas borrosas.
Los dos son malos, por motivos distintos, y se arreglan de formas distintas. Por eso la
evaluación se organiza alrededor de tres preguntas separadas:

1. **¿Se parece cada muestra a algo real?** Es la *fidelidad*, y en la literatura de modelos
   generativos se llama *precision*.
2. **¿El modelo cubre todo lo que hay en los datos?** Es la *diversidad* o *cobertura*, y se
   llama *recall*.
3. **¿Sirve para la tarea?** Un modelo puede ganar en las dos anteriores y no ayudar en nada: si
   las muestras no mejoran un clasificador, no aportan información nueva, o un experto no las
   acepta, el número da igual.

Las métricas que se citan, y lo que mide cada una:

- **Inception Score (IS).** Aplica un clasificador preentrenado a las muestras generadas y premia
  que las predicciones sean **seguras** (poca entropía por muestra) y **variadas** (mucha entropía
  en el promedio). Su fallo de diseño es que **nunca mira los datos reales**: un modelo que
  produce imágenes nítidas de una clase que no existe en el conjunto puede sacar una puntuación
  alta. Solo es comparable contra otros modelos evaluados con la misma red y el mismo número de
  clases.
- **FID.** Compara la distribución de las activaciones de una red preentrenada sobre datos reales
  con la de las muestras generadas, ajustando una gaussiana a cada conjunto y midiendo la
  distancia entre ellas. Sí mira los datos reales, y por eso se convirtió en el estándar de facto.
  Pero comprime dos ejes en un número, da por supuesto que las activaciones son gaussianas y
  depende de la red, de la capa, de la resolución y del número de muestras: dos FID calculados
  con distinto preprocesado no son comparables, ni siquiera en el mismo conjunto de datos.
- **Precisión y exhaustividad para modelos generativos.** Se incrusta cada muestra con una red (o
  unas features hechas a mano) y se define el «manantial» de un conjunto como la unión de bolas
  alrededor de sus puntos, con radio igual a la distancia al k-ésimo vecino. La precisión es la
  fracción de muestras generadas que caen en el manantial de los datos reales; la exhaustividad,
  la fracción de datos reales cubiertos por el manantial de las muestras. Son dos números en vez
  de uno, y esa es precisamente la virtud: separan los dos modos de fallo.
- **Perplejidad**, en modelos de lenguaje, mide lo bien que el modelo predice el texto real, no lo
  buenos que son sus textos generados. Un modelo puede tener una perplejidad excelente y generar
  siempre la misma frase. Se completa con métricas de diversidad (distinct-n, auto-BLEU) y, sobre
  todo, con evaluación humana; el detalle está en [[evaluacion-de-llms]].
- **Evaluación humana.** Es el patrón de referencia y también la más fácil de hacer mal. Necesita
  un protocolo: elección forzada entre dos opciones, instrucciones idénticas, orden aleatorizado,
  evaluadores ciegos al método, un número suficiente de ellos y una medida del acuerdo entre
  evaluadores. Sin acuerdo medido, «el 70 % de los humanos prefirió A» puede ser el ruido de una
  docena de personas cansadas.

Quedan dos comprobaciones que se olvidan y que son baratas:

- **Memorización.** Calcula la distancia de cada muestra generada al ejemplo de entrenamiento más
  cercano. Un modelo que gana en FID copiando el conjunto de entrenamiento no ha aprendido una
  distribución: ha aprendido una lista. Si las distancias se acumulan cerca de cero, tienes una
  tabla de búsqueda con pasos extra.
- **Utilidad aguas abajo.** Usa las muestras para entrenar un clasificador y mide sobre datos
  reales. Es la única métrica que responde a «¿para qué sirve esto?», y la que decide en la
  práctica cuando el modelo se usa para aumentar datos.

:::trampa
Comparar tu FID con el de un artículo publicado. El número depende de la red, de la capa, de la
resolución, del interpolado y del número de muestras. Dos implementaciones del «mismo» FID dan
valores distintos sobre el mismo modelo. Solo son comparables los FID que has calculado tú, con
tu script, sobre el mismo conjunto y con el mismo número de muestras.
:::

:::figura
fichero: evaluacion-generativos-fidelidad-y-cobertura
pie: A la izquierda, dos formas de fallar sobre los mismos datos de juguete, que son dos nubes separadas: el modelo A se ha quedado con un solo modo y nunca genera la mitad izquierda, y el modelo B cubre todo pero la mayoría de sus muestras caen donde no hay datos. Son fallos opuestos y se arreglan de formas distintas. A la derecha, las dos cifras que sí los separan: A tiene una fidelidad perfecta y la mitad de la cobertura; B, al contrario. Debajo de cada modelo aparece su FID calculado con la fórmula de la sección anterior sobre las mismas muestras: 2,53 para A y 1,54 para B. El número único prefiere al modelo que ha olvidado la mitad del problema, porque está dominado por la diferencia de medias y A se ha ido a un lado. Por eso la evaluación se reporta con las dos cifras.
fuente: figuras/evaluacion-de-modelos-generativos-1.py
:::

## Definición formal

**FID.** Con `φ` la red de características, `μ_r` y `Σ_r` la media y la covarianza de `φ` sobre
los datos reales y `μ_g` y `Σ_g` las mismas sobre las muestras generadas:

:::formula
FID = ‖μ_r − μ_g‖² + Tr( Σ_r + Σ_g − 2 · (Σ_r · Σ_g)^(1/2) )
:::

El primer término castiga que las medias estén lejos; el segundo, que las formas de las dos
nubes no coincidan. La raíz cuadrada es matricial, no elemento a elemento.

**Inception Score.**

:::formula
IS = exp( E_x [ KL( p(y / x) ‖ p(y) ) ] )
:::

donde `p(y / x)` es la distribución de clases que el clasificador preentrenado asigna a la
muestra `x`, y `p(y)` la media de esas distribuciones sobre todas las muestras generadas. La
divergencia es alta cuando cada muestra se clasifica con seguridad en una clase y el conjunto
toca muchas clases.

**Precisión y exhaustividad.** Se define el manantial de un conjunto de puntos `S` como la unión
de bolas centradas en sus elementos, con radio `r_k` igual a la distancia al k-ésimo vecino más
cercano dentro de `S`. Con `G` las muestras generadas y `X` los datos reales:

:::formula
precision = (1/M) · Σ_j 1[ g_j ∈ manantial(X) ]
recall    = (1/N) · Σ_i 1[ x_i ∈ manantial(G) ]
:::

Un modelo con precisión alta y exhaustividad baja ha colapsado: todo lo que genera es creíble,
pero solo cubre una parte de los datos. Uno con precisión baja y exhaustividad alta reparte
demasiado: cubre todo y además mucho que no existe.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `μ_r` | Media de las características de los datos reales | las de `φ` | No se interpreta sola: lo que cuenta es su distancia a `μ_g`. Al separarse las dos medias, el primer término del FID crece al cuadrado de la distancia |
| `μ_g` | Media de las características de las muestras generadas | las de `φ` | Al desplazarse respecto a `μ_r`, el FID empeora muy rápido. Un desplazamiento pequeño pesa más que una dispersión moderada, y ese sesgo del FID no siempre coincide con lo que ve el ojo |
| `Σ_r` | Covarianza de las características reales | las de `φ` al cuadrado | Fija la forma que hay que reproducir. Si el modelo genera con menos varianza que `Σ_r`, el segundo término del FID lo penaliza: es el término que detecta el colapso de modos, aunque de forma indirecta |
| `Σ_g` | Covarianza de las características generadas | las de `φ` al cuadrado | Al crecer mucho más que `Σ_r`, el FID empeora por el término de traza, pero de forma más suave que un desplazamiento de la media. Un modelo que reparte de más puede tener mejor FID que uno que se ha desviado |
| `Tr` | Traza: suma de la diagonal de una matriz | las de su argumento | Es el término que mide la discrepancia de forma. Si el modelo tuviera exactamente la misma covarianza que los datos, `Tr(Σ_r + Σ_g − 2(Σ_rΣ_g)^(1/2))` valdría cero |
| `p(y / x)` | Probabilidad que el clasificador asigna a cada clase para la muestra `x` | probabilidad | En el IS, cuanto más concentrada esté (más segura), mayor la divergencia. Un generador que produce basura con mucha confianza sube el IS sin mejorar nada |
| `p(y)` | Distribución media de clases sobre las muestras generadas | probabilidad | Cuanto más repartida, mayor el IS. Pero solo cuenta las clases del clasificador preentrenado y puede subir produciendo muestras irreales que caen en clases variadas |
| `manantial(X)` | Unión de bolas de radio `r_k` alrededor de los puntos de `X` | — | Es la definición de «zona donde hay datos». Al subir el radio, la precisión sube y la exhaustividad sube también: las dos cifras solo son comparables con el mismo `k` y la misma métrica de distancia |
| `k` | Vecinos usados para fijar el radio de las bolas | recuento | Al subir `k`, el radio crece y las dos métricas se vuelven más indulgentes. Es un hiperparámetro del evaluador, no del modelo, y hay que fijarlo y reportarlo |
| `1[·]` | Indicador: vale 1 si la condición se cumple y 0 si no | 0 o 1 | Es lo que convierte cada muestra en un voto. Al promediar sobre todas, se obtiene la fracción del conjunto que cumple la condición |
:::

## Ejemplo

**1. Un desplazamiento pesa más que una dispersión.** Con la misma gaussiana de referencia,
`μ_r = (0, 0)` y `Σ_r = I`, dos modelos bidimensionales calculados con la fórmula del FID:

```
desplazado 0,5 en un eje     0.2500
con un 50 % mas de varianza  0.1010
las dos cosas a la vez       0.3510
```

El modelo que se ha desplazado media unidad empeora el FID **más del doble** que el que reparte
un 50 % de más en todas las direcciones, aunque el segundo está claramente peor si lo miras. La
lección no es que el FID esté roto: es que es una métrica con sesgo propio y hay que saber cuál.

**2. Precisión y exhaustividad a mano.** Cuatro datos reales en las esquinas de un cuadrado
unitario y tres muestras generadas: `(0,05; 0,05)`, `(0,95; 0,05)` y `(0,5; 0,9)`, con bolas de
radio 0,35:

```
precision 0.6667
recall    0.5000
puntos generados fuera: 1
puntos reales sin cubrir: 2
```

La precisión es 2 de 3 porque una muestra cae en zona vacía; la exhaustividad es 2 de 4 porque dos
esquinas no están cubiertas. Con un solo número no habrías sabido cuál de los dos problemas
tienes, ni cuánto.

**3. El caso que lo resume todo.** Dos modelos sobre los mismos datos, con dos modos bien
separados:

```
modelo A (colapsado)   precision 1.0000   recall 0.5000   FID 2.5267
modelo B (disperso)    precision 0.4542   recall 1.0000   FID 1.5434
```

El modelo A no genera **nunca** la mitad izquierda de los datos: para cualquier uso que necesite
esa mitad, A es inútil. Y sin embargo el FID prefiere claramente a B, cuyas muestras se reparten
de más y en su mayoría no se parecen a nada. La razón es que el FID está dominado por la
diferencia de medias: A se ha ido a un lado y B se ha quedado en el centro. Si el informe lleva
un solo número, lleva la conclusión equivocada.

## Código

```python verificable
import numpy as np


def fid(mu_r, S_r, mu_g, S_g):
    # Tr((S_r S_g)^(1/2)) sale de los autovalores de S_r^(1/2) S_g S_r^(1/2), que si es simetrica
    vals, vecs = np.linalg.eigh(S_r)
    raiz = vecs @ np.diag(np.sqrt(vals)) @ vecs.T
    A = raiz @ S_g @ raiz
    return float(((mu_r - mu_g) ** 2).sum() + np.trace(S_r) + np.trace(S_g)
                 - 2 * np.sqrt(np.linalg.eigvalsh(A)).sum())


I = np.eye(2)
print(f"desplazado 0,5 en un eje     {fid(np.zeros(2), I, np.array([0.5, 0.0]), I):.4f}")   # -> 0.2500
print(f"con un 50 % mas de varianza  {fid(np.zeros(2), I, np.zeros(2), 1.5 * I):.4f}")     # -> 0.1010
print(f"las dos cosas a la vez       {fid(np.zeros(2), I, np.array([0.5, 0.0]), 1.5 * I):.4f}")  # -> 0.3510
```

:::claves
- `Tr((S_r · S_g)^(1/2))` no se calcula con `np.sqrt` sobre el producto, porque `S_r · S_g` no es simétrica y su raíz cuadrada no está bien definida por esa vía. El truco es `S_r^(1/2) · S_g · S_r^(1/2)`, que sí es simétrica y tiene los mismos autovalores: la traza de su raíz es la suma de las raíces de sus autovalores.
- Hay que usar solo la **traza**, no la matriz. Por eso basta `np.linalg.eigvalsh`, que devuelve autovalores ordenados y sin partes imaginarias; calcular `sqrtm` entera con `scipy.linalg` costaría más y no cambiaría el resultado.
- `np.linalg.eigh(S_r)` reconstruye `S_r^(1/2)` como `V · diag(√λ) · Vᵀ`. `eigh` es la versión para matrices simétricas: usa solo el triángulo inferior y devuelve autovalores reales, que es justo lo que hace falta con una covarianza.
- `((mu_r - mu_g) ** 2).sum()` es el cuadrado de la distancia euclídea, no la distancia. Elevar al cuadrado es intencionado: un desplazamiento del doble de tamaño cuesta cuatro veces más FID.
- `float(...)` al final es porque `np.trace` y `np.sqrt(...).sum()` devuelven `np.float64`. Da igual para imprimir con formato, pero si el valor va a un `json` o a una comparación de tipos, conviene el `float` de Python.
- Compara las tres salidas: 0,25 por desplazarse medio; 0,10 por repartir un 50 % de más; 0,35 por las dos cosas. Con eso ya sabes que un FID de 0,3 puede venir de un desplazamiento pequeño o de un desastre de forma, y el número no te lo dice.
:::

```python verificable
import numpy as np

real = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
gen = np.array([[0.05, 0.05], [0.95, 0.05], [0.5, 0.9]])
radio = 0.35

d_gen_real = np.linalg.norm(gen[:, None, :] - real[None, :, :], axis=2)
precision = (d_gen_real.min(axis=1) <= radio).mean()

d_real_gen = np.linalg.norm(real[:, None, :] - gen[None, :, :], axis=2)
recall = (d_real_gen.min(axis=1) <= radio).mean()

print(f"precision {precision:.4f}")                          # -> 0.6667
print(f"recall    {recall:.4f}")                             # -> 0.5000
print("puntos generados fuera:", int((d_gen_real.min(axis=1) > radio).sum()))    # -> 1
print("puntos reales sin cubrir:", int((d_real_gen.min(axis=1) > radio).sum()))  # -> 2
```

:::claves
- `gen[:, None, :] - real[None, :, :]` construye la tabla completa de diferencias con emisión: `gen` aporta la forma `(3, 1, 2)` y `real` la `(1, 4, 2)`, y el resultado es `(3, 4, 2)`. No hay bucle y no hay `for` anidado: las tres muestras contra los cuatro datos en una sola operación.
- El `None` de `[:, None, :]` es un eje nuevo, no un índice. Es la forma de decir «compara cada elemento de este eje con todos los del otro»; confundirlo con `np.newaxis` da exactamente lo mismo, pero escribirlo como `[:, 1, :]` seleccionaría una columna.
- La precisión se calcula sobre `min(axis=1)` —el vecino real más cercano de cada muestra generada— y la exhaustividad sobre `min(axis=1)` con los papeles cambiados. Fíjate en que son **dos** tablas de distancias: la segunda no es la traspuesta de la primera si los conjuntos tienen distinto tamaño, y aunque lo fuera las bolas se construyen alrededor de conjuntos distintos.
- En este ejemplo el radio está fijado a mano para poder seguirlo. En un caso real se fija con la distancia al k-ésimo vecino dentro del conjunto de referencia, y ese `k` hay que reportarlo: con otro radio las dos cifras cambian.
- `int(...)` convierte el recuento de NumPy en un entero de Python. Con `np.int64`, el `print` añadiría el tipo y el `# -> 1` de al lado dejaría de coincidir.
:::

```python ilustrativo
import torch
from torchmetrics.image.fid import FrechetInceptionDistance
from torchmetrics.image.inception import InceptionScore

# Las dos metricas que hay que reportar SIEMPRE juntas, y con el mismo numero de muestras
fid = FrechetInceptionDistance(feature=2048, normalize=True)
is_ = InceptionScore(normalize=True)

with torch.no_grad():
    for lote_reales in cargador_real:
        fid.update(lote_reales, real=True)
    for _ in range(n_muestras // 64):
        fid.update(generador.sample(64), real=False)
        is_.update(generador.sample(64))

print(f"FID {fid.compute():.3f}   IS {is_.compute()[0]:.3f}")
```

:::claves
- `fid.update(..., real=True)` y `real=False` alimentan las dos distribuciones. El orden no importa, pero **el número de muestras sí**: el FID se estima a partir de una covarianza muestral y su valor depende de cuántas muestras uses. Comparar dos modelos con 10.000 y con 50.000 muestras es comparar dos estimadores distintos.
- `FrechetInceptionDistance` guarda las características acumuladas hasta que llamas a `compute()`. En un bucle largo eso es memoria retenida: para muchas iteraciones conviene consultar el valor periódicamente en lugar de dejar crecer el acumulador.
- `is_.compute()` devuelve una tupla con la media y la desviación de las particiones. Si te quedas solo con el primer elemento estás ignorando la dispersión, que es la mitad del diagnóstico.
- Ni el FID ni el IS son comparables entre redes de características distintas. Si en el informe aparecen juntos resultados de dos scripts diferentes con `feature=2048` y `feature=64`, la tabla no significa nada.
- Fíjate en que este bloque no dice nada sobre precisión, exhaustividad, memorización ni utilidad. Es el mínimo, no la evaluación completa.
:::

## Errores típicos

- **Reportar un solo número.** El FID o el IS responden a «¿cuánto se parece esto?», no a «¿qué
  le falta?». Sin un par de métricas que separen fidelidad y cobertura, la conclusión va a ser
  equivocada en cuanto el modelo falle por el lado que la métrica no mira.
- **Comparar FID calculados con distinto preprocesado o distinta red.** El número no es una
  propiedad del modelo, es una propiedad del par (modelo, evaluador). Cambia la resolución, la
  capa o el interpolado y el ranking puede darse la vuelta.
- **Comparar con distinto número de muestras.** El FID se estima sobre una covarianza muestral, y
  esa estimación depende de cuántas muestras uses. Fija el número y usa el mismo en todas las
  filas de la tabla.
- **Usar el IS como métrica principal.** No mira los datos reales, así que no puede detectar que
  el modelo ha olvidado una clase entera, y un generador que produce basura con mucha confianza
  puntúa alto.
- **Evaluar con las muestras que usaste para elegir el modelo.** Si comparas 40 checkpoints y te
  quedas con el de mejor FID, ese valor es el máximo de 40 medidas ruidosas y está sesgado hacia
  arriba. Reserva un conjunto de muestras o de semillas que no hayas usado para elegir, igual que
  en [[data-snooping-y-multiple-testing]].
- **Mirar solo la media de la métrica entre ejecuciones.** Un FID de 12,3 puede venir de cinco
  ejecuciones entre 11 y 14 o de una de 8 y otra de 20. La dispersión entre semillas es parte del
  resultado.
- **No comprobar la memorización.** Un modelo puede ganar en FID reproduciendo el conjunto de
  entrenamiento. Es la trampa más fácil de detectar (distancia al vecino más cercano) y la que
  más se ignora cuando el resultado es bueno.

:::practica
enunciado: Dos modelos sobre los mismos datos. El modelo A obtiene precisión 1,00 y exhaustividad 0,50; el modelo B, precisión 0,45 y exhaustividad 1,00. El FID de A es 2,53 y el de B, 1,54. El encargo es generar datos sintéticos para entrenar un clasificador que después se usará sobre datos reales, y las dos clases están igual de representadas en el problema. ¿Con cuál te quedas y qué comprobación haces antes de decidir?
pista: Piensa qué le falta a A y qué le sobra a B, y qué necesita un clasificador que va a verse con datos reales de las dos clases.
solucion: A no genera nunca la mitad de los datos, así que un clasificador entrenado solo con sus muestras no habrá visto la otra clase y fallará justo ahí: tiene una precisión perfecta y una cobertura inservible. B cubre todo, aunque con mucho ruido, y el ruido de más se puede filtrar o ponderar, mientras que la clase que falta no se puede inventar. Antes de decidir hay que comprobar dos cosas: la distancia de cada muestra al ejemplo de entrenamiento más cercano (para descartar que B esté copiando) y la utilidad aguas abajo, entrenando con muestras de cada modelo y midiendo sobre datos reales. Si las dos clases están igual de representadas, el recall de 0,50 de A es descalificante por sí solo.
:::

## Comprueba que lo sabes

:::quiz
p: Un generador obtiene precisión 0,95 y exhaustividad 0,30. ¿Qué le pasa?
o: Que ha colapsado: lo que genera es creíble, pero cubre solo una parte de los datos
o: Que produce muestras poco realistas
o: Que está memorizando el conjunto de entrenamiento
a: 1
e: La precisión mira si cada muestra generada cae en zona donde hay datos reales; la exhaustividad, si los datos reales quedan cubiertos. Precisión alta con exhaustividad baja es la firma del colapso de modos: el modelo hace bien una parte del problema y ha olvidado el resto. La memorización se detecta con la distancia al vecino más cercano del entrenamiento, no con estas dos cifras.
:::

:::quiz
p: ¿Por qué el Inception Score puede subir sin que el modelo mejore?
o: Porque promedia sobre demasiadas muestras
o: Porque solo mira las muestras generadas: premia predicciones seguras y variadas del clasificador, aunque las muestras no se parezcan a nada real
o: Porque usa una red preentrenada en otro conjunto de datos
a: 2
e: El IS no compara contra los datos reales en ningún momento. Un generador que produce imágenes nítidas de clases que no existen en el conjunto puede obtener una puntuación alta, porque el criterio es la confianza y la variedad de las predicciones, no la semejanza con los datos.
:::

:::quiz
p: Al calcular el FID de un modelo de difusión usas 5.000 muestras y para el modelo anterior tenías 50.000. ¿Qué haces?
o: Comparar los dos números directamente, la métrica ya está normalizada
o: Recalcular los dos con el mismo número de muestras antes de comparar
o: Usar el IS, que no depende del número de muestras
a: 2
e: El FID se estima a partir de la media y la covarianza de las características, y esa estimación depende de cuántas muestras entran. Con distinto número de muestras los dos valores no son comparables. El IS también depende de la muestra por el término de entropía media, aunque su dependencia sea menos directa.
:::

:::aviso
Si el modelo se va a usar para algo concreto —aumentar datos de entrenamiento, generar casos de
prueba, producir contenido—, la evaluación que decide es la de esa tarea, sobre datos reales. Las
métricas de distribución sirven para descartar modelos rápido, no para elegir el que se despliega.
:::
