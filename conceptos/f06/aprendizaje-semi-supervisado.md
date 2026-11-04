---
id: aprendizaje-semi-supervisado
titulo: Aprendizaje semisupervisado
fase: 6
nivel: experto
rutas: [ds]
prerequisitos: [paradigmas-de-aprendizaje, metricas-de-clasificacion, train-val-test, clustering-jerarquico]
tags: [etiquetas, autosupervision, pseudoetiquetado, propagacion]
resumen: Aprovechar millones de filas sin etiquetar con autosupervisión, pseudoetiquetado y propagación de etiquetas cuando anotar es caro
fuentes: ["Zhu y Goldberg (2009), 'Introduction to Semi-Supervised Learning'", "Chapelle, Schölkopf y Zien (2006), 'Semi-Supervised Learning'", "Sohn et al. (2020), 'FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence'"]
---

## En una frase

El aprendizaje semisupervisado usa a la vez unas pocas filas etiquetadas y muchas sin
etiquetar, apoyándose en la idea de que la forma de la distribución de los datos —dónde están
los grupos, qué puntos se parecen— contiene información sobre la frontera que buscas.

## La idea

Etiquetar es caro y lento. Un radiólogo tarda minutos en marcar una imagen; un abogado, horas
en clasificar un contrato; un analista, días en decidir si una operación fue buena. Conseguir
10.000 filas etiquetadas puede costar más que todo el resto del proyecto. En cambio, datos sin
etiquetar suele haber millones: los tienes en el data lake, esperando.

El aprendizaje supervisado clásico ignora esos millones. El semisupervisado los usa, y la
hipótesis que lo justifica se puede enunciar sin matemáticas: **si dos puntos están muy cerca
en el espacio de variables, es probable que compartan etiqueta**. Es lo que se llama
supuesto de suavidad, y hay una segunda versión más específica: los puntos tienden a
agruparse en racimos, y cada racimo suele tener una sola etiqueta (supuesto de clúster).

Sobre esos supuestos se construyen cuatro familias de métodos:

1. **Autosupervisión.** En lugar de inventar etiquetas de clase, se inventa una tarea que solo
   necesita los propios datos: predecir una parte oculta, ordenar trozos, distinguir una
   transformación aplicada. El modelo resultante se ajusta después con las pocas etiquetas
   reales. Es lo que hacen los modelos de lenguaje.
2. **Pseudoetiquetado.** Se entrena con lo etiquetado, se predicen las filas sin etiquetar, se
   añaden las predicciones con más confianza y se repite.
3. **Propagación de etiquetas.** Se construye un grafo de similitud entre todos los puntos y
   las etiquetas conocidas se difunden por ese grafo.
4. **Entrenamiento con consistencia.** La misma imagen con dos aumentos distintos debe dar la
   misma predicción; la discrepancia se penaliza como pérdida.

Hay un requisito que muchos pasan por alto y que decide si el método funcionará: **los
supuestos tienen que ser ciertos en tus datos**. Si la frontera real cruza un racimo de
puntos, propagar etiquetas dentro de ese racimo introduce errores sistemáticos, no ruido
aleatorio. Y si las clases están tan mezcladas que la cercanía no dice nada, ningún método
semisupervisado ayuda: en el peor caso, como demuestra la literatura teórica, añadir datos sin
etiquetar puede empeorar el resultado frente a usar solo las etiquetas.

## Definición formal

Sea `L = {(xᵢ, yᵢ)}` el conjunto etiquetado, con `n` elementos, y `U = {xⱼ}` el conjunto sin
etiquetar, con `m` elementos, con `m ≫ n`. La pérdida de un método semisupervisado se escribe
como una suma de dos términos:

:::formula
L_total = Σ_{(x,y) ∈ L} ℓ(y, f(x))  +  λ · Σ_{x ∈ U} ℓ_u(f, x)
:::

- `f` — el modelo que se entrena; devuelve una predicción o una probabilidad por clase.
- `ℓ` — la pérdida supervisada habitual (entropía cruzada, por ejemplo), que solo se puede
  calcular en `L` porque es lo único con etiqueta.
- `ℓ_u` — la pérdida no supervisada: en pseudoetiquetado, la entropía cruzada contra la
  etiqueta inventada; en consistencia, la distancia entre dos predicciones del mismo punto.
- `λ` — cuánto pesa el término no supervisado frente al supervisado. Es el hiperparámetro
  crítico del método.
- `n` y `m` — tamaños de `L` y `U`; la relación `m/n` determina cuánta información puede
  aportar `U`, y también cuánto daño puede hacer si el supuesto es falso.

En propagación de etiquetas, la formulación es distinta: se construye una matriz de pesos `W`
con `Wᵢⱼ` grande cuando los puntos `i` y `j` son parecidos (por ejemplo, un núcleo gaussiano
o los `k` vecinos más próximos) y se resuelve:

:::formula
F* = (I − α·S)⁻¹ · Y     con S = D^(−1/2) · W · D^(−1/2)
:::

- `W` — matriz de similitud entre los `n + m` puntos; `D` es su matriz diagonal de grados,
  con `Dᵢᵢ = Σⱼ Wᵢⱼ`.
- `Y` — matriz de etiquetas conocidas; las filas de los puntos sin etiquetar son cero.
- `α ∈ (0, 1)` — cuánto se difunde la información en cada iteración.
- `F*` — puntuaciones por clase para todos los puntos; la clase predicha es el mayor valor de
  cada fila.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `L` | El conjunto de filas con etiqueta observada: lo único que se sabe de verdad | filas | Con más filas etiquetadas el método se apoya menos en los supuestos y el resultado se parece al del aprendizaje supervisado |
| `U` | El conjunto de filas sin etiquetar | filas | Más filas sin etiquetar dan más geometría que aprovechar y también más daño que hacer si el supuesto es falso |
| `m/n` | Cuántas filas sin etiquetar hay por cada fila etiquetada | cociente | Al subir, pesa más la estructura de los datos; el modelo hereda los sesgos del conjunto grande aunque las 20 etiquetas digan otra cosa |
| `λ` | Cuánto pesa la pérdida no supervisada frente a la supervisada | adimensional | Si sube, el modelo prioriza la forma de los datos y desatiende las etiquetas; si se pasa, las ignora del todo |
| `ℓ_u` | La pérdida no supervisada: contra la pseudoetiqueta, o entre dos aumentos del mismo punto | las de la pérdida | Si sube, el modelo está peor en la parte no supervisada; es lo que empuja la frontera hacia donde están los puntos |
| `α` | Cuánto se difunde la etiqueta en cada iteración de la propagación, entre 0 y 1 | adimensional | Cerca de 0 las etiquetas apenas salen de su punto; cerca de 1 se difunden mucho y el resultado se suaviza de más |
| `W` | La matriz de similitud entre los `n + m` puntos (núcleo gaussiano o `k` vecinos) | adimensional | Con `k` vecinos: si `k` sube, todo se conecta con todo y las etiquetas se difuminan; con `k = 1` no se difunde nada |
:::

## Ejemplo

200 puntos en dos lunas entrelazadas, con solo 12 etiquetas (el 6 %). El resto va marcado como
sin etiquetar. Con 150 filas de entrenamiento y 50 de prueba:

```
solo con las 12 etiquetas : 0,72    <- la recta no puede seguir las lunas
pseudoetiquetado          : 0,44    <- empeora: hereda los errores de esa recta
propagacion de etiquetas  : 0,84    <- iguala al modelo entrenado con las 150 etiquetas
MLP con las 150 etiquetas  : 0,84
```

Tres lecturas de esta tabla:

- **La geometría es información.** La propagación no ve ni una etiqueta más que la regresión,
  pero conoce la posición relativa de los 150 puntos y con eso reconstruye la frontera
  curva. Los supuestos de suavidad y de racimo se cumplen aquí, y por eso funciona.
- **El pseudoetiquetado se atasca.** Con 12 etiquetas, el modelo base tiene una frontera
  mala; las pseudoetiquetas heredan esa frontera mala y el proceso se refuerza a sí mismo. El
  umbral de confianza 0,75 no lo salva.
- **La última fila es un MLP con las 150 etiquetas, no un techo del problema.** La
  propagación llega a su altura usando el 6 % de las etiquetas, y eso ya es lo notable. Con
  esas mismas 150 etiquetas, un modelo supervisado más flexible (vecinos próximos, random
  forest) acierta más.

:::figura
fichero: semi-supervisado-frontera-con-12-etiquetas
pie: Las dos lunas del ejemplo, con los 150 puntos de entrenamiento y las 12 etiquetas marcadas con borde negro. A la izquierda, la frontera que aprende una regresión logística solo con esas 12 filas: una recta, y cae donde no toca, porque con doce ejemplos la recta que mejor los separa no tiene nada que ver con la que separa las lunas. A la derecha, la propagación de etiquetas sobre un grafo de 7 vecinos, que ve los mismos 12 puntos etiquetados más los 138 sin etiquetar y reconstruye la curva. La exactitud sobre los 50 puntos de prueba pasa de 0,72 a 0,84 con las mismas 12 etiquetas y las mismas 150 filas de entrenamiento. Lo que ha cambiado no es la cantidad de información etiquetada: es haber usado la posición de los puntos, que es exactamente el supuesto de suavidad que sostiene todo el método.
fuente: figuras/aprendizaje-semi-supervisado-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.semi_supervised import SelfTrainingClassifier, LabelSpreading
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Dos lunas: la geometria de los puntos SIN etiquetar tambien informa
X, y = make_moons(n_samples=200, noise=0.2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)

y_parcial = np.full_like(y_tr, -1)                 # -1 significa "sin etiquetar"
etiquetados = np.array([0, 1, 2, 3, 40, 41, 42, 43, 80, 81, 82, 83])
y_parcial[etiquetados] = y_tr[etiquetados]         # 12 etiquetas de 150 filas

def evalua(modelo, objetivo):
    # Se ajusta con las 150 filas: las marcadas con -1 son candidatas y no cuentan en la perdida
    modelo.fit(X_tr, objetivo)
    # score devuelve np.float64; float() lo deja en un numero de Python corriente
    return round(float(modelo.score(X_te, y_te)), 3)

base = LogisticRegression(max_iter=1000).fit(X_tr[etiquetados], y_tr[etiquetados])
print("solo con las 12 etiquetas:", round(float(base.score(X_te, y_te)), 3))              # -> 0.72
print("pseudoetiquetado         :", evalua(SelfTrainingClassifier(
      LogisticRegression(max_iter=1000), threshold=0.75, max_iter=10), y_parcial))        # -> 0.44
print("propagacion de etiquetas :", evalua(LabelSpreading(
      kernel="knn", n_neighbors=7), y_parcial))                                           # -> 0.84
print("MLP con las 150 etiquetas:", evalua(MLPClassifier(hidden_layer_sizes=(16,),
      max_iter=2000, early_stopping=False, random_state=0), y_tr))                        # -> 0.84
```

:::claves
- `np.full_like(y_tr, -1)` crea un array con la misma forma y el mismo tipo que `y_tr`, que es entero. La convención para «sin etiquetar» es `-1`, no `NaN`: como el array es entero, `np.full_like(y_tr, np.nan)` no guarda ningún `NaN`, sino el entero más negativo de 64 bits (-9223372036854775808), así que scikit-learn se queda sin filas sin etiquetar (avisa con «y contains no unlabeled samples») y acaba tratando ese número como una tercera clase.
- `LogisticRegression(max_iter=1000)`: el valor por defecto son 100 iteraciones, y cuando el modelo no converge el aviso sale por la salida de error, donde es fácil no verlo. En este ejemplo el límite no cambia nada (con 12 filas converge en 6 iteraciones), pero subirlo es lo primero que hay que probar cuando un resultado no cuadra.
- `LabelSpreading` no acepta `random_state` porque no muestrea nada: es determinista para un mismo grafo. Lo que cambia el resultado es `n_neighbors`, no la semilla. Con 7 vecinos el grafo es local; con 50, casi todos los puntos se conectan entre sí.
- La función `evalua` ajusta el modelo dentro: pasarle uno ya ajustado no da error, `fit` lo rehace desde cero y se pierde el ajuste anterior. Y `modelo.score(...)` sobre un clasificador devuelve exactitud, que solo significa algo si `y_te` trae etiquetas verdaderas: si metes filas con `-1` en el conjunto de evaluación, `score` las trata como una clase más y el número es basura.
- `SelfTrainingClassifier(..., threshold=0.75)` compara el umbral con la probabilidad **máxima** de cada fila, no con la de una clase concreta. En binario da igual; con cinco clases, una fila con 0,3 en la clase probable no llega al umbral.
- `auto.transduction_` es el vector de etiquetas final, con las observadas y las inventadas mezcladas. `auto.transduction_ >= 0` cuenta cuántas filas acabaron etiquetadas, y restarle `len(etiquetados)` da las pseudoetiquetas añadidas (138 en el ejemplo).
:::

```python verificable
import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.model_selection import train_test_split

# Dos lunas con muy pocas etiquetas: aqui el pseudoetiquetado hace dano
X, y = make_moons(n_samples=200, noise=0.2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)
y_parcial = np.full_like(y_tr, -1)                 # -1 significa "sin etiquetar"
etiquetados = np.array([0, 1, 2, 3, 40, 41, 42, 43, 80, 81, 82, 83])
y_parcial[etiquetados] = y_tr[etiquetados]

base = LogisticRegression(max_iter=1000).fit(X_tr[etiquetados], y_tr[etiquetados])
print("base con 12 etiquetas:", round(float(base.score(X_te, y_te)), 3))        # -> 0.72

auto = SelfTrainingClassifier(LogisticRegression(max_iter=1000), threshold=0.75, max_iter=10)
auto.fit(X_tr, y_parcial)        # las 150 filas: las de etiqueta -1 son las candidatas
print("tras el pseudoetiquetado:", round(float(auto.score(X_te, y_te)), 3))     # -> 0.44
print("pseudoetiquetas anadidas:", int((auto.transduction_ >= 0).sum()) - len(etiquetados))  # -> 138
# transduction_ trae la etiqueta final de cada fila; compararla con y_tr mide cuantas acerto
print("acuerdo (sobre 150 filas):", round(float((auto.transduction_ == y_tr).mean()), 3))   # -> 0.56
```

```python ilustrativo
# Autosupervision de verdad: preentrenar con tareas inventadas y ajustar despues.
# Ilustrativo: necesita torch, GPU y un corpus de imagenes que no esta en el bloque.
import torch
import torchvision

# 1) Preentrenamiento sin etiquetas: cada imagen con dos aumentos y una perdida de contraste
encoder = torchvision.models.resnet18(weights=None)
# .parameters() da un iterador sobre los pesos: el optimizador los referencia, no los copia
optimizador = torch.optim.Adam(encoder.parameters(), lr=1e-4)
for lote in cargador_sin_etiquetas:          # millones de imagenes, ninguna con clase
    v1, v2 = dos_aumentos_distintos(lote)
    perdida = perdida_contrastiva(encoder(v1), encoder(v2))
    perdida.backward()                       # calcula los gradientes
    optimizador.step()                       # y los aplica: hacen falta los dos, en ese orden

# 2) Ajuste final con las pocas etiquetas reales
cabeza = torch.nn.Linear(512, num_clases)
entrenar(cabeza, encoder, cargador_etiquetado)   # unas pocas miles de imagenes
```

## Errores típicos

- **Dar por hecho que añadir datos sin etiquetar siempre mejora.** Solo ayuda si se cumplen
  los supuestos (suavidad, racimos) y si el modelo base es mejor que el azar. Con una base
  mala, el pseudoetiquetado confirma sus propios errores y puede quedar peor que entrenar solo
  con lo etiquetado.
- **Validar mal cuando hay filas sin etiquetar.** En validación cruzada, los pliegues deben
  contener solo filas etiquetadas para medir; si metes filas con etiqueta `-1` en el pliegue
  de prueba, la métrica es basura. Separa la evaluación de lo que el método ve sin etiquetar.
- **Elegir el umbral de confianza por costumbre.** Un umbral alto apenas añade datos; uno bajo
  añade mucho y ensucia. En el ejemplo de arriba, con umbral 0,75 el modelo se quedó con 138
  pseudoetiquetas que solo coincidían con la realidad el 52 % de las veces, y la exactitud cayó
  de 0,72 a 0,44. El umbral correcto depende de la calibración de tus probabilidades: si el
  modelo está mal calibrado, un 0,9 no significa «acierto el 90 % de las veces».
- **Confundir semisupervisado con autosupervisado.** Autosupervisado significa inventarse la
  tarea a partir de los datos (sin ninguna etiqueta de clase); semisupervisado significa usar
  las pocas etiquetas de clase que tengas. Un modelo preentrenado de forma autosupervisada
  más un ajuste fino supervisado es el flujo habitual, y son dos fases distintas.
- **Aplicar propagación de etiquetas con una matriz de similitud mal escalada.** Con `k`
  vecinos hay que elegir `k`; con núcleo gaussiano, hay que elegir el ancho. Si `k` es enorme,
  todo se conecta con todo y las etiquetas se difuminan; si es 1, no se difunde nada.
- **Usar la etiqueta inventada como si fuera real en el informe final.** El modelo se entrenó
  con etiquetas predichas: la métrica de validación sigue siendo la referencia, y hay que
  dejar claro cuántas filas llevan etiqueta observada y cuántas, inferida.

:::practica
enunciado: Con 12 filas etiquetadas, un modelo acierta el 72 %. El pseudoetiquetado con umbral de confianza 0,75 añade 138 filas. Al comparar esas 138 pseudoetiquetas con la verdad, coinciden el 52 %. Calcula cuántas son erróneas y decide si conviene añadirlas, sabiendo que el modelo resultante baja al 44 %.
pista: Multiplica 138 por 0,52 para las correctas y por 0,48 para las erróneas, y compara ese 48 % de error con el 28 % que fallaba el modelo base.
solucion: Correctas = 138 · 0,52 = 71,8, unas 72; erróneas = 138 · 0,48 = 66,2, unas 66. Casi la mitad del material añadido lleva la etiqueta mal, y el modelo pasa de 0,72 a 0,44 de exactitud. No conviene: el proceso confirmó sus propios errores. Subir el umbral a 0,9 solo ayuda si las probabilidades están bien calibradas; con un modelo mal calibrado, un 0,9 no significa acertar el 90 % de las veces.
:::

## Comprueba que lo sabes

:::quiz
p: ¿En qué se apoya el aprendizaje semisupervisado para usar filas sin etiquetar?
o: En que los datos sin etiquetar contienen las etiquetas de otra fuente que hay que recuperar
o: En el supuesto de que puntos cercanos tienden a compartir etiqueta y de que los racimos suelen ser de una sola clase
o: En que el modelo puede adivinar la etiqueta al azar y quedarse con la mayoría
a: 2
e: Los dos supuestos clásicos son suavidad (puntos cercanos, misma etiqueta) y agrupamiento (un racimo, una clase). Si no se cumplen, los métodos dejan de ayudar e incluso pueden empeorar el resultado frente a usar solo lo etiquetado.
:::

:::quiz
p: Con 12 etiquetas, el pseudoetiquetado baja de 0,72 a 0,44 mientras la propagación llega a 0,84, lo mismo que un MLP entrenado con las 150 etiquetas. ¿Qué explica la diferencia?
o: Que la propagación usa la posición relativa de los 150 puntos y el pseudoetiquetado solo refuerza la frontera mala del modelo base
o: Que la propagación tiene más parámetros y por eso aprende más
o: Que el pseudoetiquetado no funciona nunca y no merece la pena probarlo
a: 1
e: La propagación construye un grafo de similitud con todos los puntos —etiquetados o no— y difunde las etiquetas por él, aprovechando la geometría. El pseudoetiquetado parte de una frontera aprendida con 12 ejemplos y la copia a escala. En otros problemas, con una base buena, el pseudoetiquetado sí aporta.
:::

:::aviso
Cuando el conjunto sin etiquetar no viene del mismo proceso que el etiquetado (por ejemplo,
texto de otro dominio o imágenes de otra cámara), el semisupervisado puede trasladar sesgos
del conjunto grande al modelo. Comprueba siempre en un conjunto de validación con la misma
distribución que producción, no en el conjunto sin etiquetar.
:::
