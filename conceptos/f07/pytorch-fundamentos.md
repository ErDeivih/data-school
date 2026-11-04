---
id: pytorch-fundamentos
titulo: PyTorch: fundamentos
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [numpy-fundamentos, perceptron-y-mlp, funciones-de-perdida, grafos-computacionales-y-autograd]
tags: [pytorch, entrenamiento, tensores, dataloader]
resumen: Tensores que recuerdan cómo se calcularon, un módulo con sus parámetros, un cargador de lotes y un bucle de cinco pasos que se repite.
fuentes: ["Paszke et al. (2019), 'PyTorch: An Imperative Style, High-Performance Deep Learning Library'", "Stevens, Antiga y Viehmann (2020), 'Deep Learning with PyTorch'"]
---

## En una frase

PyTorch es NumPy con dos añadidos —los tensores saben en qué dispositivo viven y recuerdan cómo
se calcularon— más tres piezas de fontanería: el módulo que agrupa los parámetros, el cargador
que sirve los lotes y el bucle de cinco pasos que los entrena.

## La idea

El **tensor** es la estructura básica: un array de `n` dimensiones con un tipo (`float32` por
defecto) y un dispositivo (`cpu` o `cuda`). Las operaciones son las de
[[numpy-fundamentos|NumPy]] y siguen las mismas reglas de [[numpy-broadcasting|broadcasting]],
así que casi todo lo que sabes de NumPy se traslada. Lo que no se traslada es el dispositivo:
si el modelo está en la GPU y los datos en la CPU, la operación falla. Es un error de una línea
y de media hora de búsqueda la primera vez.

El **módulo** (`nn.Module`) es una clase con dos métodos. En `__init__` declaras las capas; el
simple hecho de asignarlas como atributos hace que PyTorch registre sus parámetros y los
devuelva en `modelo.parameters()`, que es lo que le pasas al optimizador. En `forward` describes
el cálculo. Se llama al modelo como si fuera una función (`modelo(x)`), no `modelo.forward(x)`:
la llamada pasa por unos enganches internos que gestionan modos y otras cosas que acabarás
usando.

El **cargador** (`DataLoader`) envuelve un `Dataset` —una clase con `__len__` y `__getitem__`—
y se encarga de agrupar en lotes, barajar el orden en cada época y, si le dices
`num_workers > 0`, de preparar los lotes en procesos paralelos. Barajar importa: si el conjunto
está ordenado por clase, los lotes llegan todos de la misma clase y el gradiente va oscilando
sin motivo.

Y el **bucle de entrenamiento** son siempre las mismas cinco operaciones: limpiar gradientes,
pasar hacia delante, calcular la pérdida, retropropagar y actualizar. Todo lo demás —métricas,
guardado, parada temprana— se cuelga alrededor.

Dos detalles que ahorran disgustos. El primero: `modelo.train()` y `modelo.eval()` no son
decoración. Cambian el comportamiento de capas como
[[dropout-y-regularizacion|dropout]] y [[normalizacion-por-lotes|normalización por lotes]], y
olvidarse de `eval()` al medir da métricas que no significan nada. El segundo: guarda el
`state_dict` (un diccionario de tensores), no el objeto del modelo. Guardar el objeto entero
serializa la ruta de la clase; el día que muevas el fichero o renombres la clase, el modelo ya
no carga.

:::aviso
En Windows, `DataLoader` con `num_workers > 0` arranca procesos con `spawn`: el script se vuelve
a ejecutar en cada uno. Si el código de entrenamiento está en el nivel superior del fichero sin
protección, cada trabajador intentará entrenar otra vez y verás errores raros o un bucle sin
fin. Envuelve el arranque en `if __name__ == "__main__":`. Es la causa número uno de que un
`DataLoader` «no funcione» en Windows y funcione igual en Linux.
:::

## Definición formal

El entrenamiento con descenso de gradiente por minilotes actualiza los parámetros `θ` con una
estimación del gradiente calculada sobre un lote `B`:

:::formula
θ ← θ − η · (1/|B|) · Σ_{i ∈ B} ∇_θ L(xᵢ, yᵢ; θ)
:::

- `θ` — todos los parámetros del modelo (`modelo.parameters()`).
- `B` — el lote; `|B|` su tamaño.
- `η` — la tasa de aprendizaje.
- `L` — la pérdida, calculada por el criterio.
- `∇_θ L` — el gradiente que produce `backward()`; los gradientes se acumulan en `.grad`.

El bucle, con la estructura que repiten todos los proyectos:

```text
for epoca in range(num_epocas):
    modelo.train()                       # dropout y normalizacion en modo entrenamiento
    for x, y in cargador:                # un lote por iteracion
        optimizador.zero_grad()          # 1. limpiar los gradientes anteriores
        prediccion = modelo(x)           # 2. hacia delante
        perdida = criterio(prediccion, y)  # 3. la perdida
        perdida.backward()               # 4. hacia atras: llena los .grad
        optimizador.step()               # 5. actualizar los parametros

    modelo.eval()                        # modo evaluacion
    with torch.no_grad():                # sin construir el grafo
        validar(modelo, val)
```

Los elementos que intervienen en el bucle:

- `modelo` — instancia de `nn.Module` con sus parámetros registrados.
- `criterio` — la función de pérdida; `nn.CrossEntropyLoss` o `nn.MSELoss`, entre otras.
- `optimizador` — construido **después** del modelo, con `modelo.parameters()`.
- `cargador` — `DataLoader` que produce tuplas `(x, y)` ya agrupadas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `θ` | todos los parámetros del modelo (`modelo.parameters()`) | las del parámetro | Es lo único que se mueve. El optimizador recorre la lista de tensores que le pasaste al construirlo: si creas capas después, esas se quedan sin entrenar y sin avisar |
| `B` | el lote de ejemplos que se usa en cada paso | ejemplos | Lotes más grandes dan un gradiente menos ruidoso y menos pasos por época. Con SGD hay que subir `η` en la misma proporción o el entrenamiento cambia de ritmo |
| tamaño del lote | número de ejemplos del lote, `abs(B)` en la fórmula | ejemplos | Entra **dividiendo** el gradiente: la pérdida se promedia sobre el lote, así que ni la pérdida ni el gradiente dependen de cuántos ejemplos haya, solo de su media |
| `η` | tasa de aprendizaje | las de `θ` partido por las de `g` | Escala el paso. En la versión de un solo parámetro (sin sesgo) el error se multiplica por `1 − 2·η·media(x²)`; con estos cuatro puntos eso da `1 − 15·η`. En el modelo completo, que además tiene sesgo, la condición de estabilidad es más estrecha: con `η = 0,13` la pérdida acaba en 10²⁸ |
| `L` | la pérdida que devuelve el criterio | las del objetivo | Es el número del que sale todo el gradiente. Con `reduction="sum"` en vez de `"mean"`, tanto su valor como su gradiente se multiplican por el tamaño del lote |
| `∇_θ L` | gradiente que produce `backward()` | las de `L` partido por las de `θ` | Se **acumula** en `.grad`: sube con cada `backward()` que no vaya precedido de `zero_grad()`, y el paso del optimizador crece con él |
| `xᵢ`, `yᵢ` | entrada y etiqueta de cada ejemplo del lote | las de las variables | La escala de `x` entra directamente en el límite de estabilidad: multiplicar las entradas por 10 sin tocar `η` hace que el mismo entrenamiento explote |
| `num_epocas` | pasadas completas por el conjunto de entrenamiento | épocas | Más épocas entrenan más y sobreajustan antes. Lo que decide cuándo parar es la métrica de validación, nunca la de entrenamiento |
| `batch_size` | ejemplos por lote que sirve el cargador | ejemplos | Es un argumento del `DataLoader`, no del optimizador. Al subirlo hay menos lotes por época y, por tanto, menos llamadas a `step()` por época |
| `num_workers` | procesos que preparan los lotes en paralelo | procesos | Con 0 los lotes se preparan en el proceso principal. Al subirlo hay más paralelismo, pero en Windows cada trabajador reimporta el script: sin `if __name__ == "__main__":` se reejecuta el entrenamiento entero |
:::

## Ejemplo

Ajustamos `y = 2x` con cuatro puntos (`x = [1, 2, 3, 4]`, `y = [2, 4, 6, 8]`) usando solo
NumPy, para ver qué hace el bucle por dentro. Con `η = 0,1` y empezando en `w = 0`, `b = 0`:

- El gradiente inicial es `2 · media(x · (0 − y)) = 2 · (−60)/4 = −30`, así que el primer paso
  deja `w = 0 − 0,1 · (−30) = 3` y `b = 0 − 0,1 · (−10) = 1`. La pérdida arranca en 30,0.
- Tras 100 pasos, la pérdida es 0,0002 con `w = 1,9901` y `b = 0,0292`.
- Tras 200 pasos, la pérdida es 0,0000 con `w = 1,9995` y `b = 0,0014`: ha recuperado la
  relación exacta `y = 2x`.

La tasa de aprendizaje tiene un límite concreto en este problema. Si te quedas con un solo
parámetro (sin sesgo) y la pérdida `media((w·x − y)²)`, el error se multiplica en cada paso por
`1 − 2·η·media(x²) = 1 − 15·η`:

- Con `η = 0,1`, el factor es `−0,5`: el error se divide por 2 en cada paso y en 20 pasos ya es
  prácticamente cero.
- Con `η = 0,2`, el factor es `−2`: el error se duplica (con signo alterno) en cada paso y el
  entrenamiento diverge. En el ejemplo completo con sesgo, basta con `η = 0,13` para que la
  pérdida acabe en 10²⁸.

Ese «límite» depende de la escala de los datos: si multiplicas `x` por 10 sin tocar `η`, el
factor pasa a ser `1 − 1500·η` y el entrenamiento explota. Es la razón de que se normalicen las
entradas.

:::figura
fichero: pytorch-fundamentos-bucle-y-lotes
pie: El panel izquierdo ejecuta exactamente el bucle de cinco pasos sobre el mismo problema, con dos tasas de aprendizaje, y dibuja la pérdida de cada iteración en escala logarítmica. Con η = 0,1 la curva baja de 30 a 3·10⁻⁷ de forma monótona: el modelo recupera la relación exacta y = 2x. Con η = 0,13, solo tres centésimas más, la pérdida crece sin parar hasta 10²⁸: el error se multiplica en cada paso por 1 − 2·η·media(x²), y en cuanto ese factor supera 1 en valor absoluto no hay forma de volver. No es un fallo del optimizador ni de los datos: es el mismo código con otro número, y de ahí que la primera comprobación ante una pérdida que se dispara sea bajar η, no revisar el modelo. El panel derecho hace visible una cuenta que casi nadie hace a mano: con 1000 muestras y batch_size = 32 salen 32 lotes, no 31. Los 31 primeros van llenos y el último lleva solo 8 muestras, pero también se procesa y también da su llamada a step(). Descartarlo con drop_last=True tira esas 8 muestras en cada época, y en un conjunto pequeño eso es información que el modelo nunca ve.
fuente: figuras/pytorch-fundamentos-1.py
:::

## Código

```python verificable
import numpy as np

# El bucle de entrenamiento, a mano y con NumPy, para ver que no hay magia.
x = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([[2.0], [4.0], [6.0], [8.0]])      # la relacion exacta es y = 2x
w, b, lr = np.zeros((1, 1)), 0.0, 0.1           # w se declara (1, 1) para que x @ w de (4, 1)

for paso in range(200):
    prediccion = x @ w + b                      # 1. hacia delante
    perdida = np.mean((prediccion - y) ** 2)    # 2. la perdida
    error = prediccion - y                      # 3. hacia atras, a mano
    # w -= ... modifica el array EN EL SITIO; w = w - ... crearia uno nuevo cada paso
    w -= lr * (2 * x.T @ error / len(x))        # 4. paso del optimizador
    b -= lr * (2 * error.mean())                # b es un float: aqui -= es solo reasignar
    if paso in (0, 99, 199):
        # :>3 alinea el numero del paso a la derecha y :8.4f reserva 8 caracteres para la perdida
        print(f"paso {paso:>3}  perdida {perdida:8.4f}  w {w[0, 0]:.4f}  b {b:+.4f}")
# -> paso   0  perdida  30.0000  w 3.0000  b +1.0000
# -> paso  99  perdida   0.0002  w 1.9901  b +0.0292
# -> paso 199  perdida   0.0000  w 1.9995  b +0.0014
```

:::claves
- `w` se declara con forma `(1, 1)` y no como `np.zeros(1)`: `x @ w` con `x` de forma `(4, 1)`
  necesita que `w` sea `(1, 1)` para dar `(4, 1)`. Con `w` de forma `(1,)` el producto sale `(4,)`
  y la resta `prediccion - y` contra una columna `(4, 1)` dispara el *broadcasting* y devuelve una
  matriz `(4, 4)` sin ningún error a la vista.
- `w -= ...` sobre un array de NumPy modifica el array **en el sitio**; `w = w - ...` crearía uno
  nuevo en cada iteración. Con `w` compartido con otra variable, la diferencia entre las dos
  formas es la diferencia entre un resultado correcto y uno inexplicable.
- `2 * x.T @ error / len(x)` mezcla dos operadores con precedencias distintas: `@` (producto
  matricial) se evalúa antes que `*` y `/`, así que la cuenta es `((2 * x.T) @ error) / 4`. La
  derivada de la MSE media lleva ese `2` delante y se divide entre el número de filas, no entre 4
  escrito a mano.
- `b` es un `float` de Python, no un array: `b -= ...` no modifica nada en el sitio, solo vuelve a
  asignar el nombre. El `+=`/`-=` significa cosas distintas según el tipo, y por eso conviene
  saber cuál tienes entre manos.
- `np.mean((prediccion - y) ** 2)` se calcula **antes** de actualizar los pesos, y por eso el paso
  0 imprime 30,0 y no el valor ya reducido: la pérdida que ves es la del modelo con el que has
  entrado a esa iteración. Es el mismo orden que sigue el bucle de PyTorch.
- `w[0, 0]` indexa la matriz con dos índices. Con `w` de forma `(1, 1)`, `w[0]` sería una fila
  entera (un array de un elemento) y saldría impreso como `[1.9901]` en vez del número.
:::

```python verificable
import numpy as np

# Lo que hace el DataLoader: barajar una vez por epoca y cortar en lotes.
datos = np.arange(10.0)                     # 10 muestras
rng = np.random.default_rng(0)
for epoca in range(2):
    orden = rng.permutation(datos.size)     # barajado distinto en cada epoca
    for inicio in range(0, datos.size, 4):
        idx = orden[inicio:inicio + 4]      # el ultimo lote es mas pequeno
        # inicio // 4 numera el lote: division entera, no la posicion de la muestra
        print(f"epoca {epoca}  lote {inicio // 4}  indices {idx}")
# -> epoca 0  lote 0  indices [4 6 2 7]
# -> epoca 0  lote 1  indices [3 5 9 0]
# -> epoca 0  lote 2  indices [8 1]
# -> epoca 1  lote 0  indices [2 9 3 6]
# -> epoca 1  lote 1  indices [0 4 8 7]
# -> epoca 1  lote 2  indices [5 1]
```

```python ilustrativo
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

class Datos(Dataset):
    def __init__(self, x, y):
        self.x, self.y = torch.as_tensor(x, dtype=torch.float32), torch.as_tensor(y)
    def __len__(self):
        return len(self.x)
    def __getitem__(self, i):
        return self.x[i], self.y[i]

class Red(nn.Module):
    def __init__(self, entradas, clases):
        super().__init__()
        self.capa = nn.Linear(entradas, 64)      # los parametros se registran solos
        self.salida = nn.Linear(64, clases)
    def forward(self, x):
        return self.salida(torch.relu(self.capa(x)))

modelo = Red(20, 3)
criterio = nn.CrossEntropyLoss()
optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4, weight_decay=0.01)
cargador = DataLoader(Datos(x_ent, y_ent), batch_size=32, shuffle=True, num_workers=0)

if __name__ == "__main__":                       # obligatorio con num_workers > 0 en Windows
    for epoca in range(10):
        modelo.train()
        for x, y in cargador:
            optimizador.zero_grad()
            perdida = criterio(modelo(x), y)
            perdida.backward()
            optimizador.step()
        modelo.eval()
        with torch.no_grad():
            correctas = (modelo(x_val).argmax(1) == y_val).sum().item()
        print(epoca, correctas / len(y_val))

    torch.save(modelo.state_dict(), "modelo.pt")               # solo los tensores
    modelo.load_state_dict(torch.load("modelo.pt", map_location="cpu"))
```

## Errores típicos

- **Olvidar `modelo.eval()` al evaluar.** Con dropout y normalización en modo entrenamiento, la
  validación usa máscaras aleatorias y estadísticas del lote: el resultado cambia entre
  ejecuciones y suele ser peor. Alterna `train()` y `eval()` en cada época, no una vez al
  principio: lo que decide si el modelo sirve es la métrica de validación
  ([[train-val-test|entrenamiento, validación y prueba]]), no la pérdida de entrenamiento.
- **Guardar el modelo entero con `torch.save(modelo)`.** Además de ser más pesado, guarda una
  referencia a la clase: si mueves el fichero donde está definida o la renombras, el modelo deja
  de cargar. Guarda `modelo.state_dict()` y reconstruye la arquitectura en código. Al cargar,
  usa `map_location` si el `checkpoint` se guardó en GPU y ahora no la tienes.
- **Mover los datos a la GPU y no el modelo (o al revés).** El error
  «Expected all tensors to be on the same device» aparece en la primera operación que mezcle
  dispositivos. La receta: `modelo.to(dispositivo)` una vez y `x.to(dispositivo)` en cada lote.
- **Acumular la pérdida con `perdida` en vez de `perdida.item()`.** Guardar el tensor mantiene
  vivo el grafo de todo el lote, y al cabo de la época tienes cientos de grafos en memoria. Usa
  `.item()` para los números y `.detach().cpu().numpy()` para las predicciones que vayas a
  analizar con NumPy.
- **No llamar a `zero_grad()`.** Los gradientes se suman: sin limpiarlos, el paso del optimizador
  usa la suma de todos los anteriores. Mira
  [[grafos-computacionales-y-autograd|el grafo computacional]] para entender por qué.
- **Poner `num_workers > 0` en Windows sin proteger el arranque.** Los procesos trabajadores
  importan tu script otra vez; sin `if __name__ == "__main__":` se reejecuta el entrenamiento
  completo dentro de cada uno.

:::practica
enunciado: Tienes 1.000 muestras, un DataLoader con batch_size = 32 y shuffle activado, y entrenas 5 épocas. ¿Cuántas llamadas a optimizer.step() haces y cuántas muestras lleva el último lote de cada época?
pista: Cada época son lotes completos más un lote final con el resto; el barajado cambia qué muestras caen en él, no cuántas.
solucion: 1.000 / 32 = 31,25, así que cada época produce 32 lotes: 31 de 32 muestras y uno de 1.000 − 31 · 32 = 8. Con 5 épocas son 32 · 5 = 160 llamadas a step(), una por lote. El lote corto también cuenta: si lo descartas pierdes 8 muestras en cada época.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el orden correcto de las operaciones dentro del bucle de entrenamiento?
o: `backward()`, `zero_grad()`, `step()`
o: `zero_grad()`, `forward`, pérdida, `backward()`, `step()`
o: `step()`, `zero_grad()`, pérdida, `backward()`
a: 2
e: Primero se limpian los gradientes acumulados, luego se calcula la salida y la pérdida, después la retropropagación llena los `.grad` y por último el optimizador actualiza los pesos con ellos. Si limpias después de actualizar, el siguiente paso arrastra los gradientes viejos; si actualizas antes de retropropagar, usas los gradientes del paso anterior.
:::

:::quiz
p: ¿Por qué se guarda `modelo.state_dict()` y no el objeto del modelo?
o: Porque el `state_dict` ocupa menos y se puede editar
o: Porque guardar el objeto serializa la referencia a la clase y el modelo deja de cargar si cambia el código o la ruta
o: Porque `torch.save` no admite objetos
a: 2
e: El `state_dict` es un diccionario de tensores que se carga sobre una arquitectura construida en código: no depende de dónde esté definida la clase ni de cómo se llamara. Guardar el objeto entero usa `pickle` y guarda la ruta de la clase, así que renombrarla o mover el fichero rompe la carga. `torch.save` sí admite objetos, pero no es lo recomendable para modelos.
:::

:::quiz
p: En el ejemplo, con un solo parámetro y `x = [1, 2, 3, 4]`, el error se multiplica por `1 − 15·η` en cada paso. ¿Qué ocurre con `η = 0,2`?
o: Converge más rápido que con `η = 0,1`
o: Diverge, porque el factor vale −2 y el error se duplica en cada paso
o: Se queda igual, porque el factor es cero
a: 2
e: Con η = 0,2 el factor es 1 − 3 = −2: el error cambia de signo y se duplica en cada iteración, así que crece sin límite. Con η = 0,1 el factor es −0,5 y el error se reduce a la mitad por paso. El factor cero aparece con η = 1/15 ≈ 0,0667.
:::

:::trampa
Un `DataLoader` con `shuffle=False` sobre un conjunto ordenado por clase hace que cada lote
tenga una sola clase. El modelo no aprende mal por la arquitectura: el gradiente va dando saltos
porque cada lote empuja en una dirección distinta. Baraja siempre en entrenamiento, y **nunca**
en validación (da igual el orden, pero que sea reproducible).
:::
