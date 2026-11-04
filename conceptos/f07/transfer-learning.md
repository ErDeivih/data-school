---
id: transfer-learning
titulo: Aprendizaje por transferencia
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [sesgo-varianza, perceptron-y-mlp, train-val-test, funciones-de-perdida]
tags: [transferencia, fine-tuning, representaciones, practica]
resumen: Reutilizar un modelo ya entrenado en otra tarea y adaptarlo a la tuya con pocas etiquetas, en vez de empezar de cero cada vez.
fuentes: ["Yosinski et al. (2014), 'How transferable are features in deep neural networks?'", "Pan y Yang (2010), 'A Survey on Transfer Learning'"]
---

## En una frase

En lugar de entrenar una red desde cero con los datos que tienes, partes de un modelo ya
entrenado en una tarea parecida, reutilizas sus capas como extractor de características y solo
adaptas una parte a tu problema.

## La idea

Aprender a conducir un coche te sirve para conducir una furgoneta. No empiezas de cero: el
volante, los pedales y la idea de mirar por el retrovisor se transfieren. Lo que tienes que
ajustar es lo específico: la altura, el tamaño y la distancia de frenado. Cuanto más parecida
sea la tarea nueva a la vieja, menos tienes que reaprender; y el conocimiento que se transfiere
casi siempre es el de los niveles bajos (bordes, formas, ritmos) y no el de las decisiones
finales.

En redes ocurre lo mismo. Los primeros filtros de una CNN entrenada con imágenes aprenden
detectores de bordes y texturas que sirven para casi cualquier problema visual; las últimas
capas se especializan en las clases concretas que se entrenaron. Por eso existen tres regímenes
distintos, y elegir mal es el error más caro de este tema:

- **Extractor congelado.** Se usa la red preentrenada tal cual y se entrena solo una cabeza
  nueva (una regresión logística o un MLP pequeño) sobre la salida de una capa intermedia. Es
  lo más barato y lo más robusto cuando tienes muy pocas etiquetas.
- **Ajuste fino (fine-tuning).** Se sigue entrenando el modelo completo (o parte de él) con tus
  datos y una [[tasas-de-aprendizaje-y-schedulers|tasa de aprendizaje]] pequeña. Necesita más
  datos y más cuidado, pero permite que las características se adapten a tu dominio.
- **Desde cero.** Sin modelo previo. Solo tiene sentido cuando tu dominio se parece poco a todo
  lo que existe publicado o cuando tienes muchísimos datos etiquetados.

La intuición cuantitativa es simple: el número de **parámetros que puedes permitirte entrenar**
es proporcional a la cantidad de etiquetas que tienes. Con 20 etiquetas y 2.000 parámetros, el
modelo memoriza; con 20 etiquetas y 10 parámetros en una cabeza nueva sobre una representación
buena, aprende. Transferir es, en el fondo, comprar representaciones con datos de otro.

:::figura
fichero: transfer-learning-etiquetas-y-ancla
pie: Dos preguntas distintas, una por panel. A la izquierda, ¿cuánto gana la transferencia? Con 12 etiquetas de destino, la red entrenada desde cero se queda en 0,657 y la que parte del modelo de origen llega a 0,910: 25 puntos de diferencia. Fíjate en que la banda de color se estrecha a medida que hay más etiquetas: con pocas, el resultado depende mucho de la semilla, y esa es la razón de que una sola corrida no demuestre nada. Hacia las 300 etiquetas las dos curvas se juntan, porque con datos suficientes la representación se aprende sola y el atajo deja de aportar. La transferencia no sube el techo del modelo: te hace llegar antes. A la derecha está el precio de moverse demasiado, con el anclaje L2. Cada punto es un valor de `λ`. Con `λ = 0` el ajuste es libre: el error en la tarea nueva es cero y el de la tarea vieja se dispara a 1,386, que es el olvido catastrófico medido. Con `λ = 5` ocurre lo contrario. El compromiso útil está en medio (`λ = 0,05` conserva bastante de los dos), y se elige con un conjunto de validación de la tarea nueva, nunca a ojo.
fuente: figuras/transfer-learning-1.py
:::

## Definición formal

Sea una tarea de origen con datos `(X_s, y_s)` y una tarea de destino con `(X_t, y_t)`, donde
`|y_t|` es mucho menor que `|y_s|`. Un modelo preentrenado se descompone en dos partes:

:::formula
f_θ(x) = g_φ( h_ψ(x) )
:::

- `h_ψ` — el **extractor**: convierte la entrada `x` en un vector de características `h_ψ(x)`.
- `g_φ` — la **cabeza**: convierte esas características en la predicción.
- `ψ`, `φ` — los pesos de cada parte; en el preentrenamiento se aprendieron con `(X_s, y_s)`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `h_ψ(x)` | Vector de características que el extractor saca de la entrada | las de las características | No es un parámetro que se mueva: es lo que se reutiliza. Cuanto mejor sea esa representación, menos datos necesita la cabeza |
| `g_φ` | La cabeza que convierte las características en la predicción | las de la salida | Con más capacidad aprende tareas más difíciles sobre la misma representación, pero también memoriza antes si hay pocas etiquetas |
| `ψ` | Pesos del extractor | adimensionales | Si se congelan, solo entrena `φ` y el modelo no puede adaptarse al dominio nuevo; si se descongelan con una tasa alta, los pesos preentrenados se destruyen en las primeras decenas de pasos |
| `φ` | Pesos de la cabeza | adimensionales | Es lo único que se entrena en el régimen congelado: el número de parámetros entrenables decide cuántas etiquetas necesitas |
| `λ` | Peso del anclaje L2 hacia los pesos preentrenados | adimensional | Con `λ = 0` el ajuste es libre y olvida el origen (error en origen 1,386); con `λ = 5` apenas se mueve y no aprende el destino (error 1,260). El valor útil está en medio |
| `w_origen` | Los pesos preentrenados, el punto de partida | adimensionales | No se mueve: son la referencia del anclaje. Con `λ` grande, `w` se queda pegado a `w_origen` |
| `L_destino` | Pérdida en la tarea nueva | las de la tarea | Es lo que se minimiza. Bajarla sin mirar `L_origen` es exactamente lo que produce el olvido catastrófico |
:::

Los tres regímenes son tres problemas de optimización distintos sobre esa descomposición:

1. **Extractor congelado:** `ψ` queda fijo y se minimiza la pérdida solo sobre `φ`. El número de
   parámetros entrenables es el de la cabeza.
2. **Ajuste fino:** se minimiza sobre `ψ` y `φ` a la vez, partiendo de los valores
   preentrenados y con una tasa de aprendizaje pequeña.
3. **Desde cero:** se inicializa `ψ` al azar (o con una inicialización diseñada, véase
   [[inicializacion-de-pesos]]) y se optimiza todo con `(X_t, y_t)`.

Una variante muy usada cuando el destino es pequeño pero no idéntico al origen es el anclaje
L2 hacia los pesos de partida (a veces llamado L2-SP): se añade a la pérdida un término

:::formula
L_total = L_destino(w) + (λ/2) · ‖ w − w_origen ‖²
:::

- `w_origen` — los pesos preentrenados, el punto del que se parte.
- `λ` — cuánto se penaliza alejarse de ellos; `λ = 0` es ajuste fino libre y `λ` muy grande es
  dejar el modelo congelado.
- `‖·‖²` — norma euclídea al cuadrado, la suma de los cuadrados de todas las diferencias.

## Ejemplo

Tarea de origen: clasificar puntos del plano según la regla XOR (positivo si las dos coordenadas
tienen el mismo signo), con 400 ejemplos. Tarea de destino: la misma regla, con la nube de
puntos desplazada, y **solo 12 etiquetas**. Red pequeña de 2 entradas, 8 neuronas ReLU y una
salida:

```
red de origen en su propia tarea   0.975
desde cero con 12 etiquetas        0.657
partiendo del modelo de origen     0.910
```

La regla XOR **no se puede separar con una recta**, así que con 12 puntos un modelo desde cero
se queda cerca del azar-más-un-poco (0,657). La representación que aprendió el modelo de origen
ya contiene la no linealidad necesaria, y una cabeza entrenada sobre ella acierta el 91 % de
los 400 puntos de prueba. Es el efecto típico: la transferencia no mejora el techo del modelo,
mejora la **velocidad a la que llegas** con pocos datos.

El segundo experimento mide el precio de moverse demasiado. Modelo de origen con pesos
`w = [1,5; −0,5]` y tarea de destino con solución `w = [0,2; 1,8]`. Se ajusta con el anclaje L2
y se miran los dos errores a la vez:

```
ancla lambda   error en origen   error en destino
        0.00            1.386             0.000
        0.05            1.256             0.136
        0.50            0.687             0.720
        5.00            0.128             1.260
```

Con `λ = 0` el modelo aprende la tarea nueva a la perfección y **destruye** lo que sabía: el
error en la tarea de origen pasa de 0 a `1,386`. Con `λ = 5` ocurre lo contrario, conserva el
origen (`0,128`) y no aprende el destino (`1,260`). El valor útil está en el medio, y se elige
con un conjunto de validación de la tarea nueva, no a ojo. Eso es el compromiso
[[sesgo-varianza|sesgo-varianza]] trasladado al punto de partida.

## Código

```python verificable
import numpy as np


def entrena(X, y, epocas, params=None, semilla=0):
    """Red 2-8-1 con ReLU y entropia cruzada, por lotes. Devuelve W1, b1, w2, b2."""
    rng = np.random.default_rng(semilla)
    if params is None:
        W1, b1 = rng.normal(0, 0.7, (2, 8)), np.zeros(8)
        w2, b2 = rng.normal(0, 0.35, 8), 0.0
    else:
        # .copy() en las matrices y los vectores: sin el, el descenso de gradiente escribe
        # sobre los pesos del modelo de origen y la segunda llamada empezaria de otro sitio.
        W1, b1, w2, b2 = params[0].copy(), params[1].copy(), params[2].copy(), params[3]

    for _ in range(epocas):
        orden = rng.permutation(len(y))          # barajar una vez por epoca, no por lote
        for inicio in range(0, len(y), 32):
            idx = orden[inicio:inicio + 32]
            H = np.maximum(0.0, X[idx] @ W1 + b1)
            # [:, None] convierte el error en columna (lote, 1): asi el broadcasting alinea
            # las filas de H con las filas del error en vez de con las columnas.
            dz = (1 / (1 + np.exp(-(H @ w2 + b2))) - y[idx])[:, None] / len(idx)
            g = dz * w2 * (H > 0)                 # (H > 0) es la derivada de ReLU
            W1 -= 0.05 * (X[idx].T @ g)
            b1 -= 0.05 * g.sum(0)
            w2 -= 0.05 * (H * dz).sum(0)
            b2 -= 0.05 * float(dz.sum())
    return W1, b1, w2, b2


def precision(X, y, params):
    W1, b1, w2, b2 = params
    p = 1 / (1 + np.exp(-(np.maximum(0.0, X @ W1 + b1) @ w2 + b2)))
    return float(((p > 0.5) == y).mean())


def datos(rng, n, centro, escala):
    X = rng.normal(centro, escala, size=(n, 2))
    return X, (X[:, 0] * X[:, 1] > 0).astype(float)   # regla XOR: no hay recta que la separe


X_origen, y_origen = datos(np.random.default_rng(0), 400, 0.0, 1.0)
X_destino, y_destino = datos(np.random.default_rng(2), 12, 0.4, 0.7)   # solo 12 etiquetas
X_test, y_test = datos(np.random.default_rng(1), 400, 0.4, 0.7)

origen = entrena(X_origen, y_origen, 200)
desde_cero = entrena(X_destino, y_destino, 200)
transferido = entrena(X_destino, y_destino, 200, params=origen)

print(f"red de origen en su propia tarea   {precision(X_origen, y_origen, origen):.3f}")
print(f"desde cero con 12 etiquetas        {precision(X_test, y_test, desde_cero):.3f}")
print(f"partiendo del modelo de origen     {precision(X_test, y_test, transferido):.3f}")
# -> red de origen en su propia tarea   0.975
# -> desde cero con 12 etiquetas        0.657
# -> partiendo del modelo de origen     0.910
```

:::claves
- `params[0].copy()` copia el **array**, no el nombre. Si te olvidas del `.copy()` en cualquiera
  de las cuatro piezas, el descenso de gradiente modifica el modelo de origen en su sitio: la
  siguiente llamada partiría de otro sitio y el experimento dejaría de ser comparable.
- `(H @ w2 + b2)` devuelve un vector de forma `(lote,)` y `y[idx]` también. La resta es elemento a
  elemento; el `[:, None]` añade un eje para pasar de `(lote,)` a `(lote, 1)` y que después
  `dz * w2` multiplique bien por la matriz `H`.
- `(H > 0)` es una matriz de booleanos, y multiplicarla por `dz * w2` la convierte en 0 y 1: es la
  derivada de ReLU escrita de la forma más corta. Un `np.maximum(0, ...)` a mano daría lo mismo
  pero más largo.
- `X[idx]` es una **copia** hecha con indexación avanzada (un array de índices), no una vista: se
  puede leer sin miedo, pero modificar `X[idx]` **no** cambiaría `X`.
- `rng.permutation(len(y))` baraja los índices una vez por época. Si en lugar de eso usaras
  `rng.shuffle(y)`, estarías reordenando las etiquetas y desalineándolas de `X`.
- `b2 -= 0.05 * float(dz.sum())`: `dz.sum()` es un array de un elemento y `float()` lo convierte
  en un número de Python. Sin esa conversión `b2` acabaría siendo un array de NumPy y el tipo se
  contagiaría a todo lo que se calcule después.
- `precision(X, y, params)` devuelve un `float` con `float(((p > 0.5) == y).mean())`: `p > 0.5` ya
  es una comparación elemento a elemento, y compararla con `y` (que viene en 0.0 y 1.0) funciona
  porque NumPy compara `True == 1.0`. Cambiar las etiquetas a `-1` y `1` rompería esa línea.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
w_origen = np.array([1.5, -0.5])      # modelo ya entrenado en la tarea de origen
w_destino = np.array([0.2, 1.8])      # solucion buena para la tarea nueva
X = rng.normal(0, 1, size=(24, 2))
y_origen, y_destino = X @ w_origen, X @ w_destino

print("ancla lambda   error en origen   error en destino")
for lam in (0.0, 0.05, 0.5, 5.0):
    w = w_origen.copy()          # cada lambda parte del mismo punto de origen
    for _ in range(200):
        # El segundo sumando es el gradiente del anclaje L2: lam * (w - w_origen).
        grad = X.T @ (X @ w - y_destino) / len(X) + lam * (w - w_origen)
        w -= 0.1 * grad          # descenso de gradiente con tasa fija
    print(f"{lam:>11}   {np.abs(X @ w - y_origen).mean():14.3f}"
          f"   {np.abs(X @ w - y_destino).mean():15.3f}")
# -> ancla lambda   error en origen   error en destino
# ->         0.0            1.386             0.000
# ->        0.05            1.256             0.136
# ->         0.5            0.687             0.720
# ->         5.0            0.128             1.260
```

```python ilustrativo
# El patron habitual con un modelo de vision preentrenado: congelar y cambiar la cabeza.
# Necesita pesos descargados, por eso no se ejecuta aqui.
import torch
from torch import nn
from torchvision import models

modelo = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
for p in modelo.parameters():
    p.requires_grad = False                      # extractor congelado

modelo.fc = nn.Linear(modelo.fc.in_features, 3)  # 3 clases nuevas: esta capa si entrena
optimizador = torch.optim.AdamW(modelo.fc.parameters(), lr=1e-3)

# Si mas adelante quieres ajuste fino, descongela solo el ultimo bloque y baja la tasa:
# for p in modelo.layer4.parameters(): p.requires_grad = True
```

## Errores típicos

- **Descongelar todo desde el primer momento con una tasa de aprendizaje alta.** Los pesos
  preentrenados se destrozan en las primeras decenas de pasos y acabas con un modelo peor que
  uno entrenado desde cero. Empieza con la cabeza, luego descongela por bloques y usa una tasa
  entre 10 y 100 veces menor que la del preentrenamiento.
- **Cambiar el preprocesado de las entradas.** Un modelo preentrenado espera exactamente la
  misma normalización (media, desviación, tamaño, escala de color) con la que se entrenó. Si le
  pasas imágenes sin normalizar o en otro rango, las activaciones se salen de rango y las
  predicciones son basura. Se copia el preprocesado, no se reinventa.
- **Ajustar y evaluar sobre las mismas etiquetas de destino.** Con 12 o 20 etiquetas es
  tentador mirar la precisión en el mismo conjunto con el que se ajustó; ese número no dice
  nada. Separa validación desde el principio: el conjunto de destino es pequeño, y precisamente
  por eso hay que cuidarlo.
- **Ignorar la fuga del preentrenamiento.** Si el modelo base se entrenó con datos que incluyen
  tus ejemplos de prueba (habitual con modelos de lenguaje e imágenes públicas), tu evaluación
  está inflada y no hay forma de arreglarlo a posteriori. Comprueba la procedencia del corpus
  antes de creerte el resultado.
- **Transferir cuando los dominios no tienen nada que ver.** Las capas iniciales de un modelo
  de imágenes naturales no ayudan necesariamente con espectrogramas o señales médicas; a veces
  la transferencia es neutra y a veces es negativa (transferencia negativa: rinde peor que
  entrenar desde cero). Se comprueba con un experimento controlado, no se asume.
- **Elegir la profundidad a la que cortar por intuición.** ¿Congelo dos bloques o cuatro?
  ¿Reentreno la normalización? Son hiperparámetros y se deciden con validación. La regla
  práctica es empezar por lo más congelado y abrir solo si la validación lo pide.

:::practica
enunciado: Tres encargos, un solo régimen para cada uno: (A) congelar el extractor y entrenar una cabeza nueva; (B) ajuste fino completo con tasa pequeña; (C) entrenar desde cero. Encargo 1: 80 imágenes de un dominio parecido al preentrenado. Encargo 2: 8.000 imágenes de un dominio distinto. Encargo 3: 50 imágenes de un dominio que no se parece a nada publicado. Asigna uno a cada encargo y justifica.
pista: Lo que manda es cuántas etiquetas tienes frente a cuánto se parece tu dominio al del preentrenamiento.
solucion: 1 → A: con 80 etiquetas solo puedes permitirte la cabeza, y la representación sirve porque el dominio coincide. 2 → B: con 8.000 etiquetas sí puedes tocar el extractor, y el dominio distinto lo exige. 3 → C: sin parecido con nada publicado la transferencia puede ser negativa, y 50 etiquetas no ajustan nada.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes 200 imágenes etiquetadas de un dominio parecido a uno para el que existe un modelo preentrenado. ¿Por dónde empiezas?
o: Entrenando la red completa desde cero, para que no arrastre sesgos del preentrenamiento
o: Congelando el extractor y entrenando solo una cabeza nueva, y abriendo capas después si la validación lo pide
o: Ajustando todas las capas con la misma tasa de aprendizaje que usó el preentrenamiento
a: 2
e: Con pocas etiquetas, el extractor congelado es lo más robusto y barato; después se descongela por bloques con tasas pequeñas. Entrenar desde cero desaprovecha las representaciones y ajustar todo con la tasa original destruye los pesos preentrenados.
:::

:::quiz
p: En el ejemplo de XOR, el modelo desde cero acierta 0,657 y el transferido 0,910. ¿Cuál es la explicación?
o: El modelo de origen tiene más parámetros que el entrenado desde cero
o: La representación del modelo de origen ya contiene una no linealidad que separa la regla XOR, y con 12 etiquetas basta para ajustar la cabeza
o: El modelo transferido ha visto los 400 puntos de prueba durante el preentrenamiento
a: 2
e: Los dos modelos tienen exactamente la misma arquitectura y el de prueba es independiente del preentrenamiento. La diferencia es que XOR no es linealmente separable y 12 puntos no bastan para aprender la frontera desde cero, mientras que la capa oculta del modelo de origen ya la representa.
:::

:::quiz
p: ¿Qué controla el término de anclaje L2 con parámetro λ en el ajuste fino?
o: El número de capas que se descongelan
o: Cuanto se penaliza alejarse de los pesos preentrenados, es decir, cuánto se conserva del origen frente a cuánto se aprende del destino
o: La proporción de datos de origen que se mezclan con los del destino
a: 2
e: El anclaje es una penalización sobre la distancia a w_origen: con λ = 0 el modelo se mueve libre y olvida (error en origen 1,386), con λ = 5 apenas se mueve y no aprende el destino (error 1,260). No cambia qué capas se entrenan ni mezcla conjuntos de datos.
:::
