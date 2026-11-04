---
id: grafos-computacionales-y-autograd
titulo: Grafos computacionales y autograd
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [regla-de-la-cadena, retropropagacion, optimizadores]
tags: [autograd, gradiente, pytorch, retropropagacion]
resumen: Cada operación con tensores construye un grafo; backward lo recorre al revés con la regla de la cadena y deja la derivada de la pérdida en cada parámetro.
fuentes: ["Baydin et al. (2018), 'Automatic Differentiation in Machine Learning: a Survey'", "Paszke et al. (2019), 'PyTorch: An Imperative Style, High-Performance Deep Learning Library'"]
---

## En una frase

Cada operación que haces con tensores va apuntando en un grafo dirigido qué se calculó y con
qué; `backward()` recorre ese grafo en orden inverso aplicando la regla de la cadena y deja en
`.grad` la derivada de la pérdida respecto a cada parámetro.

## La idea

Escribir a mano el gradiente de una red de 50 capas es inviable: son cientos de derivadas
encadenadas y cualquier cambio en la arquitectura obliga a rehacerlas. La **diferenciación
automática** resuelve eso sin hacer álgebra simbólica ni aproximar con diferencias finitas:
cada operación elemental (suma, producto, `exp`, `relu`, `matmul`…) sabe cuál es su derivada
local, y el framework encadena esas derivadas locales por la regla de la cadena.

Hay dos maneras de encadenar, y la diferencia importa mucho:

- **Modo directo (forward):** se propaga la derivada desde las entradas hacia la salida. Para
  obtener la derivada respecto a los `N` parámetros hay que hacer `N` pasadas, una por
  parámetro. Con millones de parámetros, imposible.
- **Modo inverso (reverse):** se propaga desde la salida hacia las entradas. Con una salida
  escalar (la pérdida) basta **una** pasada para obtener las derivadas respecto a **todos** los
  parámetros, a un coste parecido al doble de la pasada hacia delante, independientemente de
  cuántos parámetros haya. Es lo que usa todo el deep learning, y es exactamente lo que
  llamamos [[retropropagacion|retropropagación]].

El grafo se construye **mientras se ejecuta el código** (`define-by-run`). No hay una fase de
compilación: si escribes un `if` sobre el valor de un tensor, el grafo toma una rama u otra
según el caso, y eso es una ventaja enorme para depurar. Cada nodo guarda dos cosas: la
operación que lo produjo y, si hace falta, los valores intermedios que necesitará la vuelta
atrás. Esa memorización es la razón de que el entrenamiento consuma tanta memoria: las
activaciones de todas las capas tienen que seguir vivas hasta que se usa su derivada.

De ahí salen las dos técnicas que conviene conocer. El **checkpointing de gradientes** no guarda
las activaciones intermedias: las recalcula en la vuelta atrás. Cambias cómputo por memoria, y
permite entrenar modelos que de otra forma no caben. Y `torch.no_grad()` en la evaluación evita
construir el grafo entero, porque no vas a necesitar ninguna derivada.

Una última idea que sorprende a quien viene del cálculo simbólico: autograd no **simplifica**
nada. No obtiene `dy/dw = 2·(x·w + b)·x` como haría un programa de álgebra; calcula el producto
de las derivadas locales en el punto concreto, numéricamente. Por eso el resultado es exacto
(salvo el redondeo en coma flotante) y por eso el coste depende de la estructura del grafo y no
de la longitud de la expresión.

## Definición formal

Sea una composición de funciones `y = f_L(f_{L−1}(… f_1(x) …))`, con `z_l` la salida de la capa
`l` y `J_l = ∂z_l / ∂z_{l−1}` su jacobiano. La regla de la cadena dice:

:::formula
∂y/∂x = J_L · J_{L−1} · … · J_1
:::

- `z_l` — activación intermedia, salida de la capa `l`; `z_0 = x`.
- `J_l` — matriz de derivadas parciales de la capa `l`, de tamaño `dim(z_l) × dim(z_{l−1})`.
- `L` — número de operaciones encadenadas.

El modo inverso no construye esos jacobianos. Para una pérdida escalar `L`, define
`v = ∂L/∂z_L = 1` y va multiplicando por la izquierda:

:::formula
∂L/∂z_{l−1} = (∂L/∂z_l) · J_l        (producto vector-jacobiano)
:::

- `∂L/∂z_l` — vector de derivadas de la pérdida respecto a la activación de la capa `l`.
- Cada nodo del grafo implementa su propio producto vector-jacobiano, que es lo que se llama la
  función `backward` de esa operación.
- El coste total es del orden de dos veces la pasada hacia delante, con independencia del número
  de parámetros. Ese es el motivo de que el modo inverso sea el estándar.

Los **tensores hoja** (*leaf*) son los que se crean directamente (`torch.randn(..., requires_grad=True)`
o los parámetros de un módulo). Solo ellos acumulan gradiente en `.grad` de forma predeterminada;
los intermedios se descartan al terminar la pasada, salvo que pidas `retain_grad()`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x` | entrada del grafo | las de la entrada | No es un parámetro: es un dato. Con `requires_grad=True` también acumula gradiente, pero el optimizador no lo toca |
| `w`, `b` | peso y sesgo del ejemplo | adimensional y las de `z` | Son los tensores **hoja** que sí se entrenan: su `.grad` es lo que lee el optimizador para dar el paso |
| `z` | activación intermedia de cada operación | las de la salida de esa operación | Cada valor intermedio que se guarda sigue vivo en memoria hasta que se usa su derivada; al crecer el grafo o el lote, ahí se va la VRAM |
| `y` | salida del grafo, la pérdida | las del objetivo | El modo inverso necesita que sea **escalar**: `backward()` sin argumento solo funciona sobre un tensor de un elemento |
| `J_l` | jacobiano de la operación `l` | adimensional | No se construye nunca: cada nodo implementa el producto vector-jacobiano. Materializarlo costaría `dim(z_l) × dim(z_{l−1})` números por operación |
| `∂L/∂z_l` | derivada de la pérdida respecto a la activación de la capa `l` | las de `y` partido por las de `z_l` | Es el vector que viaja hacia atrás: cada nodo lo multiplica por su jacobiano y lo entrega al anterior. Su tamaño no depende del número de parámetros |
| `L` (mayúscula) | número de operaciones encadenadas del grafo | operaciones | Más operaciones alargan la ida y la vuelta en la misma proporción: el coste sigue siendo del orden del doble de la ida, no un múltiplo del número de parámetros |
| `∂L/∂z_L` | semilla de la pasada inversa | las de `y` partido por las de `z_L` | Vale 1 cuando la pérdida es escalar. Si la salida tuviera varios elementos habría que pasar un vector como argumento de `backward()` |
| acumulación | número de `backward()` sin limpiar entre medias | llamadas | Los gradientes se **suman** en `.grad`. Al subir, el paso efectivo del optimizador crece sin control aunque la tasa de aprendizaje no haya cambiado |
:::

## Ejemplo

Un grafo diminuto que se puede seguir a mano: `z = x · w + b`, `y = z²`, con `x = 2`, `w = 3` y
`b = 1`. Hacia delante: `z = 2 · 3 + 1 = 7` e `y = 7² = 49`. Hacia atrás, la regla de la cadena
aplica las derivadas locales en orden inverso:

- `∂y/∂z = 2z = 14`.
- `∂y/∂w = (∂y/∂z) · (∂z/∂w) = 14 · x = 14 · 2 = 28`.
- `∂y/∂b = (∂y/∂z) · 1 = 14`.
- `∂y/∂x = (∂y/∂z) · w = 14 · 3 = 42`.

Comprobación numérica de la derivada respecto a `w` con diferencias finitas hacia delante:
`y(3,000001) = (2 · 3,000001 + 1)² = 7,000002² = 49,000028`, y
`(49,000028 − 49) / 0,000001 = 28,0000`. Coincide con el valor analítico hasta el cuarto
decimal: es lo que hace que la diferenciación automática sea útil y las diferencias finitas no
(una diferencia finita arrastra errores de cancelación y necesita una evaluación por parámetro).

**Acumulación de gradientes.** Si tu lote no cabe en memoria, divides el lote en trozos y
acumulas el gradiente de cada trozo antes de actualizar. El bloque de código comprueba que la
suma ponderada de los gradientes por trozo es exactamente el gradiente del lote completo:
`[−2,5, −2,75]` en los dos casos. Los gradientes que calcula autograd se **suman**; por eso hay
que ponderar cada trozo por su tamaño relativo, y por eso hay que limpiar el gradiente
(`zero_grad`) antes de cada paso, o se irá acumulando lo de todos los pasos anteriores.

:::figura
fichero: grafos-computacionales-y-autograd-grafo-y-acumulacion
pie: En el panel izquierdo, lo que hay que mirar son las etiquetas de las flechas rojas. Cada nodo no calcula la derivada de toda la expresión: solo multiplica la derivada que le llega desde arriba por su derivada local (×2z en el cuadrado, ×1 en la suma, ×x y ×w en el producto). Encadenando esas cuatro multiplicaciones salen los tres gradientes —∂y/∂b = 14, ∂y/∂w = 28 y ∂y/∂x = 42— con una sola pasada de derecha a izquierda, y ese es el motivo de que entrenar una red de cincuenta capas sea viable: el coste no depende de cuántos parámetros haya, solo de la forma del grafo. El panel derecho muestra el error silencioso más frecuente de PyTorch. La curva azul es la norma del gradiente que usa el optimizador cuando se llama a zero_grad() en cada lote: oscila alrededor de 0,5, que es lo que mide el lote actual. La roja es la misma ejecución sin limpiar: como .grad es un acumulador, en el lote t lleva la suma de los t gradientes anteriores y crece de forma sostenida. Al final el paso efectivo es decenas de veces mayor que el que crees haber configurado, y el síntoma —una pérdida que baja muy rápido y luego se vuelve errática— se atribuye casi siempre a la tasa de aprendizaje o a los datos.
fuente: figuras/grafos-computacionales-y-autograd-1.py
:::

## Código

```python verificable
import numpy as np

# El mismo grafo del ejemplo, con la pasada hacia atras escrita a mano.
def perdida(x, w, b):
    z = x * w + b
    return z ** 2, z                   # devuelve tambien z: la derivada local vale 2*z

x, w, b = 2.0, 3.0, 1.0
y, z = perdida(x, w, b)                # desempaqueta la tupla: y = z**2  y  z = z

dy_dz = 2 * z                       # derivada local de la ultima operacion
print(f"y          {y:.1f}")         # -> y          49.0
print(f"dy/dw      {dy_dz * x:.1f}")  # -> dy/dw      28.0
print(f"dy/db      {dy_dz:.1f}")     # -> dy/db      14.0
print(f"dy/dx      {dy_dz * w:.1f}")  # -> dy/dx      42.0

eps = 1e-6                          # diferencias finitas para comprobar
print(f"numerico    {(perdida(x, w + eps, b)[0] - y) / eps:.4f}")
# -> numerico    28.0000
```

:::claves
- `perdida` devuelve una **tupla** `(z ** 2, z)` y de ahí el `y, z = perdida(...)`. Devuelve `z`
  además del resultado porque la derivada local es `2 * z`: recalcularlo fuera sería repetir el
  trabajo que la función ya hizo.
- `perdida(x, w + eps, b)[0]` indexa el primer elemento de la tupla. `[0]` es `z ** 2` y `[1]` es
  `z`: confundirlos produce una «comprobación» que compara dos cosas distintas y un resultado que
  no cuadra con nada.
- `w + eps` crea un flotante **nuevo** y no toca `w`, que sigue valiendo 3,0. Si escribieras
  `w += eps`, la segunda llamada partiría de otro punto y la diferencia ya no estimaría la
  derivada en el punto original.
- `eps = 1e-6` es el compromiso clásico de las diferencias finitas hacia delante: más pequeño y
  la resta `y(w + eps) − y` pierde dígitos por cancelación; más grande y aparece el error de
  truncamiento del desarrollo de Taylor. Con `eps = 1e-8`, este ejemplo ya no imprime 28,0000.
- La comprobación numérica cuesta **una evaluación completa por parámetro**. Aquí solo se
  verifica `w`; con un millón de parámetros harían falta un millón de pasadas hacia delante, y de
  ahí que las diferencias finitas sirvan para verificar, no para entrenar.
- `dy_dz = 2 * z` es la derivada local **evaluada en el punto**, no una expresión simbólica:
  autograd encadena números igual que este bloque, y por eso el coste depende de la estructura
  del grafo y no de la longitud de la fórmula.
:::

```python verificable
import numpy as np

# Acumular gradientes por trozos debe dar el gradiente del lote completo.
X = np.array([[1.0, 0.5], [2.0, -1.0], [3.0, 2.0], [0.5, 1.0]])
yt = np.array([1.0, -1.0, 2.0, 0.0])
w = np.zeros(2)

def gradiente(indices):                       # gradiente de la MSE media del trozo
    error = X[indices] @ w - yt[indices]      # X[indices] es indexado fancy: devuelve una COPIA
    return 2 * X[indices].T @ error / len(indices)   # @ multiplica matrices y .T transpone

g_completo = gradiente(np.arange(4))
g_acumulado = np.zeros(2)
for lote in ([0, 1], [2, 3]):                 # dos trozos de dos ejemplos
    g_acumulado += gradiente(lote) * len(lote) / 4   # ponderado por su tamano
print(f"lote completo {g_completo}")           # -> lote completo [-2.5  -2.75]
print(f"acumulado     {g_acumulado}")          # -> acumulado     [-2.5  -2.75]
```

```python ilustrativo
import torch

x = torch.tensor(2.0, requires_grad=True)
w = torch.tensor(3.0, requires_grad=True)
b = torch.tensor(1.0, requires_grad=True)

y = (x * w + b) ** 2
y.backward()                     # una sola pasada para los tres parametros

print(x.grad, w.grad, b.grad)    # tensor(42.) tensor(28.) tensor(14.)

# El grafo se libera al terminar la pasada inversa
try:
    y.backward()
except RuntimeError as e:
    print(e)                     # "Trying to backward through the graph a second time"

# Acumulacion de gradientes en un bucle real
for i, (entradas, etiquetas) in enumerate(cargador):
    salida = modelo(entradas)
    perdida = criterio(salida, etiquetas) / pasos_de_acumulacion
    perdida.backward()                       # los .grad se SUMAN en cada llamada
    if (i + 1) % pasos_de_acumulacion == 0:
        optimizador.step()
        optimizador.zero_grad()              # sin esto, el gradiente se acumula sin fin

# Evaluacion: sin grafo, menos memoria y mas rapido
with torch.no_grad():
    predicciones = modelo(x_test)

# Detener el flujo del gradiente hacia una parte del grafo
caracteristicas = modelo.extractor(x).detach()   # el extractor no se entrena con esto
```

## Errores típicos

- **Olvidar `optimizador.zero_grad()`.** Los gradientes se **suman** en `.grad` en cada
  `backward()`. Si no los limpias, en el paso `n` estás aplicando la suma de los gradientes de
  los `n` pasos anteriores: el paso efectivo crece sin control y el entrenamiento se comporta de
  forma inexplicable. Es el error silencioso más frecuente de PyTorch.
- **Llamar a `backward()` dos veces sin `retain_graph=True`.** El grafo se libera al terminar la
  pasada inversa para ahorrar memoria; la segunda llamada lanza un `RuntimeError`. Si de verdad
  necesitas dos pasadas, pasa `retain_graph=True` y acuérdate de que la memoria no se libera.
- **Convertir a `numpy` o a `.item()` en medio del cálculo.** Esas conversiones cortan el grafo:
  lo que salga de ahí ya no tiene `requires_grad` y el `backward()` falla con «element 0 of
  tensors does not require grad». Para imprimir valores usa `.item()` solo en tensores que ya no
  van a participar en el gradiente (por ejemplo, la pérdida después del `backward`).
- **Modificar un tensor hoja en el sitio.** `w += 1` o `w[0] = 0` sobre un tensor con
  `requires_grad=True` rompe el grafo o da un gradiente incorrecto. Usa `with torch.no_grad():`
  para las actualizaciones manuales, o deja que lo haga el optimizador.
- **Evaluar sin `torch.no_grad()`.** Cada pasada de validación construye el grafo entero y
  guarda las activaciones para nada: la memoria se llena y la evaluación tarda el doble. No
  cambia el resultado, pero convierte una validación cómoda en un problema de memoria.
- **Suponer que el gradiente está promediado.** Para una pérdida con `reduction='sum'` el
  gradiente es la suma sobre el lote, no la media; y con acumulación de gradientes la escala
  depende de cuántos trozos sumas. Si divides la pérdida, divide también los gradientes
  (o divide la pérdida por el número de trozos, como en el bloque de arriba).

:::practica
enunciado: En el grafo z = 4x − 2, a = relu(z), L = a², con x = 0,5, calcula hacia delante z, a y L, y hacia atrás ∂L/∂x encadenando las derivadas locales.
pista: La derivada local de relu(z) vale 1 si z > 0 y 0 si z < 0; el valor exactamente cero deja el gradiente en cero.
solucion: z = 4 · 0,5 − 2 = 0; a = relu(0) = 0; L = 0² = 0. Hacia atrás, ∂L/∂a = 2a = 0 y ∂a/∂z = 0, porque z no es estrictamente positivo, así que ∂L/∂x = 0 · 4 = 0. En ese punto la unidad está muerta: con ese ejemplo no llega ninguna señal a x y el peso no se mueve.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el deep learning usa el modo inverso de la diferenciación automática y no el directo?
o: Porque el modo inverso es más preciso numéricamente
o: Porque con una salida escalar obtiene las derivadas respecto a todos los parámetros en una sola pasada, mientras el modo directo necesitaría una pasada por parámetro
o: Porque el modo directo solo funciona con funciones lineales
a: 2
e: Los dos modos son exactos; la diferencia es el coste. El modo directo propaga una dirección de derivada cada vez, así que con millones de parámetros harían falta millones de pasadas. El inverso aprovecha que la salida es escalar: una pasada, coste del orden del doble de la ida, y todos los gradientes a la vez.
:::

:::quiz
p: En el ejemplo, `y = (x·w + b)²` con `x = 2`, `w = 3` y `b = 1`. ¿Cuánto vale `∂y/∂w`?
o: 14
o: 28
o: 42
a: 2
e: Primero ∂y/∂z = 2z = 14 con z = 7, y después ∂z/∂w = x = 2, así que ∂y/∂w = 14 · 2 = 28. El 14 es la derivada respecto al sesgo (∂z/∂b = 1) y el 42 es la derivada respecto a la entrada x (∂z/∂x = w = 3).
:::

:::quiz
p: Entrenas con acumulación de gradientes en 4 trozos y olvidas llamar a `zero_grad()`. ¿Qué ocurre?
o: El gradiente se suma al de los pasos anteriores y el tamaño efectivo del paso crece con el tiempo
o: El gradiente se divide entre 4 y el entrenamiento se hace más lento, pero es correcto
o: PyTorch lanza un error al detectar el gradiente antiguo
a: 1
e: `.grad` es un acumulador: cada `backward()` suma. Sin limpiarlo, el paso que da el optimizador usa la suma de los gradientes de todos los pasos anteriores, que crece sin parar. PyTorch no avisa de nada porque acumular es precisamente lo que hace posible la acumulación de gradientes por trozos.
:::

:::trampa
Si tu pérdida baja muy rápido y luego se vuelve errática, revisa el orden de las tres líneas del
bucle: `zero_grad()`, `backward()`, `step()`. Un `step()` antes del `backward()` o un
`zero_grad()` después del `step()` producen exactamente ese síntoma, y no tiene nada que ver con
la tasa de aprendizaje.
:::
