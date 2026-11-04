---
id: tasas-de-aprendizaje-y-schedulers
titulo: Tasa de aprendizaje y planificadores
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [optimizadores, derivadas-parciales-y-gradiente, convexidad]
tags: [hiperparametros, entrenamiento, aprendizaje, planificadores]
resumen: El hiperparámetro que más cambia el resultado, y cómo moverlo durante el entrenamiento con calentamiento, escalones o coseno.
fuentes: ["Smith (2017), 'Cyclical Learning Rates for Training Neural Networks'", "Loshchilov y Hutter (2017), 'SGDR: Stochastic Gradient Descent with Warm Restarts'", "Goyal et al. (2017), 'Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour'"]
---

## En una frase

La tasa de aprendizaje es el tamaño del paso que da el optimizador en cada actualización y un
planificador la va cambiando durante el entrenamiento —normalmente bajándola— para avanzar
rápido al principio y afinar al final.

## La idea

Todo lo que hace el optimizador se multiplica por `η`: si es demasiado grande, el paso se pasa
del mínimo, el error crece y en pocas iteraciones la pérdida es `nan`; si es demasiado pequeña,
el entrenamiento avanza tan despacio que parece atascado, y en un paisaje con zonas planas
puede quedarse dando pasitos en una región mala sin llegar nunca a la buena. Entre esos dos
extremos hay un rango amplio de valores que funcionan, y encontrar uno es la primera tarea de
cualquier ajuste.

Hay una forma muy eficaz de encontrarlo, propuesta por Leslie Smith: la **prueba de rango**. Se
entrena unas cuantas decenas o cientos de iteraciones subiendo `η` de forma exponencial desde un
valor minúsculo, y se dibuja la pérdida frente a `η`. La pérdida empieza bajando, llega a un
mínimo y luego se dispara. El valor bueno está un poco antes del punto donde empieza a subir: no
en el mínimo exacto, porque interesa margen para que el entrenamiento no se desestabilice en
cuanto cambien las circunstancias.

Con el valor encontrado, ¿por qué no dejarlo fijo? Porque lo que va bien al principio no va bien
al final. Al principio los pesos están lejos de cualquier solución y conviene avanzar a zancadas,
sin miedo a pasarse, porque cualquier dirección que baje sirve. Al final estás en un valle y
quieres pasos pequeños para no salirte. Un **planificador** (en inglés, *scheduler*) programa
esa transición:

- **Escalones:** bajar `η` por un factor (típicamente 10) cada cierto número de épocas.
- **Coseno:** seguir una curva de coseno desde `η_max` hasta un mínimo. Es suave, sin saltos, y
  el descenso se acelera justo en la segunda mitad, que es donde interesa.
- **Calentamiento y coseno:** subir linealmente durante los primeros cientos de pasos y luego
  bajar con coseno. Es el plan estándar en transformers y en casi todo lo que usa Adam.
- **`ReduceLROnPlateau`:** bajar solo cuando la métrica de validación deja de mejorar. Cómodo,
  pero reactivo: reacciona después de que el estancamiento ya ha ocurrido.
- **Ciclos y reinicios:** subir y bajar `η` varias veces dentro del mismo entrenamiento. Sirve
  para escapar de mínimos malos y para entrenar varios modelos en el mismo presupuesto.

El **calentamiento** merece una explicación porque parece una moda y no lo es. En los primeros
pasos, las estimaciones de la media del cuadrado del gradiente en Adam son pésimas (arrancan en
cero) y, además, las capas de normalización y de atención se comportan de forma inestable
cuando las activaciones son grandes. Subir `η` desde cero durante unos cientos de pasos evita
ese primer tramo peligroso.

Dos reglas prácticas para no perder el tiempo: la primera, ajusta `η` **antes** que la
arquitectura, porque un cambio de `η` de un factor 10 suele mover la métrica más que cambiar una
capa; la segunda, si multiplicas el tamaño del lote por `k`, multiplica `η` por `k` y alarga el
calentamiento (regla de escalado lineal). Con Adam el efecto es menos directo, pero el
calentamiento sigue haciendo falta.

:::trampa
Un `scheduler.step()` en el sitio equivocado es un error silencioso y caro. Si el planificador
está pensado para avanzar una vez por **época** y lo llamas una vez por **lote**, con 1000 lotes
por época la tasa de aprendizaje se desploma en la primera época y el resto del entrenamiento se
hace con pasos casi nulos. Decide la unidad (lote o época) y sé coherente con la que espera el
planificador.
:::

## Definición formal

Con `η₀` o `η_max` la tasa inicial o máxima, `t` el paso o la época actual, `T` la duración del
ciclo y `γ` el factor de decaimiento:

:::formula
escalones:  η_t = η₀ · γ^⌊t / T⌋
:::

- `γ` — factor por el que se multiplica la tasa cada `T` pasos (0,1 es lo típico).
- `⌊·⌋` — parte entera, para que la tasa solo cambie al final de cada tramo.

:::formula
coseno:  η_t = η_min + ½ · (η_max − η_min) · (1 + cos(π · t / T))
:::

- `η_min` — suelo al que tiende la tasa al final del ciclo; puede ser 0 o un valor pequeño.
- `cos(π · t / T)` — vale 1 en `t = 0` y −1 en `t = T`, con lo que la tasa va de `η_max` a
  `η_min` suavemente.

:::formula
calentamiento:  η_t = η_max · t / T_calentamiento     para t < T_calentamiento
:::

- `T_calentamiento` — número de pasos de la subida lineal; después empieza la fase de descenso
  (coseno o escalones).

También se usan el decaimiento exponencial `η_t = η₀ · γ^t` y el inverso `η_t = η₀/(1 + γ·t)`.
`ReduceLROnPlateau` no es una fórmula sino una regla: si la métrica vigilada no mejora en
`patience` épocas, `η ← η · factor`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `η` | tasa de aprendizaje: el tamaño del paso | las de `θ` partido por las de `g` | Escala todo el entrenamiento. En una cuadrática el error se multiplica por `(1 − η·curvatura)` en cada paso: si ese factor supera 1 en valor absoluto, la pérdida crece hasta `nan` |
| `η₀`, `η_max` | tasa inicial o máxima del plan | las de `η` | Con un plan de coseno, subirla multiplica toda la curva. Es el parámetro que más mueve el resultado y el primero que hay que ajustar |
| `η_min` | suelo al que tiende el coseno al final del ciclo | las de `η` | Con 0 la tasa acaba en cero y los últimos pasos no aprenden nada; al subirlo, el afino final sigue moviendo los pesos y el plan nunca se apaga del todo |
| `t` | paso o época actual | iteraciones o épocas | Solo entra en el plan: al avanzar, la tasa baja. Lo que importa es que la unidad de `t` coincida con la que espera el planificador |
| `T` | duración del ciclo o de cada tramo | pasos o épocas | Un `T` mayor reparte el mismo descenso en más tiempo y el entrenamiento pasa más rato con tasas altas; con `T` pequeño el plan se agota antes de que el modelo aprenda |
| `γ` | factor por el que se multiplica la tasa cada `T` pasos | adimensional, menor que 1 | Con 0,1 la tasa cae un orden de magnitud por tramo. Cuanto más cerca de 1, más suave el plan; con `γ = 1` no hay decaimiento ninguno |
| `T_calentamiento` | pasos de subida lineal antes del descenso | pasos | Alargarlo protege más el arranque inestable, pero gasta presupuesto en tasas bajas. Un 1-5 % del total es lo habitual; con 10 pasos no protege de nada |
| `patience` | épocas sin mejora que aguanta `ReduceLROnPlateau` antes de bajar la tasa | épocas | Al subirlo, el planificador tarda más en reaccionar y el modelo pasa más tiempo estancado con la tasa vieja; al bajarlo, reacciona a cualquier ruido de validación |
| `factor` | cuánto se multiplica la tasa cuando el planificador la baja | adimensional, menor que 1 | Con 0,1 la tasa cae a la décima parte de golpe. Es un cambio mucho más brusco que el de un coseno, y por eso convive mal con tasas ya pequeñas |
:::

## Ejemplo

**Coseno a mano.** `η_max = 0,1`, `η_min = 0`, `T = 100` pasos:

- `t = 0`: `η = 0,05 · (1 + cos 0) = 0,05 · 2 = 0,1`.
- `t = 25`: `η = 0,05 · (1 + cos(π/4)) = 0,05 · (1 + 0,7071) = 0,0854`.
- `t = 50`: `η = 0,05 · (1 + cos(π/2)) = 0,05 · 1 = 0,05`.
- `t = 75`: `η = 0,05 · (1 + cos(3π/4)) = 0,05 · (1 − 0,7071) = 0,0146`.
- `t = 100`: `η = 0,05 · (1 + cos π) = 0`.

Fíjate en que la mitad del presupuesto se gasta entre 0,1 y 0,05 —la fase de exploración— y la
otra mitad entre 0,05 y 0: el afino se concentra al final, que es lo que se busca.

**Plan completo.** Con 1000 pasos totales, `η_max = 3·10⁻⁴` y calentamiento lineal de 100
pasos: el paso 0 arranca en 0, el 50 en `1,5·10⁻⁴` (justo la mitad), el 100 en `3·10⁻⁴` (el
máximo) y a partir de ahí el coseno baja: `2,65·10⁻⁴` en el paso 300, `1,24·10⁻⁴` en el 600 y 0
en el 1000. Ese perfil —subir rápido, bajar despacio— es el que verás en casi todos los
entrenamientos de transformers.

**Cuándo diverge.** Minimizando `f(θ) = θ²` con `θ₀ = 1` y el paso `θ ← θ − η · 2θ`, el error se
multiplica por `(1 − 2η)` en cada iteración. Tras 10 pasos:

- `η = 0,1`: factor `0,8` → `θ = 0,107`.
- `η = 0,5`: factor `0` → `θ = 0` en un solo paso. Convergencia instantánea, pero ojo: el
  factor es exactamente cero, cualquier curvatura distinta y el paso se queda corto o se pasa.
- `η = 1,1`: factor `−1,2` → `θ = 6,19`. El signo alterna y la magnitud crece: esto es una
  divergencia, y en una red real es un `nan`.

Ese ejemplo muestra por qué la primera comprobación ante un `nan` es bajar `η` a la décima
parte. El límite de estabilidad depende de la curvatura (aquí, `η < 1`), así que no hay un
número universal: hay que buscarlo por problema.

:::figura
fichero: tasas-de-aprendizaje-y-schedulers-planes-y-divergencia
pie: El panel izquierdo pone los cuatro planes sobre el mismo presupuesto de 1000 pasos y con la tasa normalizada, para que se comparen entre sí. Los escalones son la opción más brusca: cuatro tramos con saltos de factor 10, y en el último cuarto la tasa es prácticamente cero. El coseno recorre el mismo descenso sin ningún salto, y merece la pena mirar dónde se desploma: la primera mitad del presupuesto se gasta entre 1,0 y 0,5 y la segunda entre 0,5 y 0, que es el afino. El calentamiento es idéntico al coseno salvo en los 100 primeros pasos, que se reservan para subir desde cero; esa rampa es la que protege del arranque en el que las medias de Adam todavía son malas. El panel derecho explica por qué la tasa hay que elegirla con cuidado: con f(θ) = θ² el error se multiplica por (1 − 2η) en cada paso, así que el eje vertical es el error acumulado y su forma la decide ese factor. Con η = 0,1 el factor es 0,8 y en diez pasos el error ya está en 0,107. Con η = 0,5 el factor vale exactamente cero y acierta el mínimo en un solo paso, pero precisamente por eso es frágil: cualquier curvatura distinta hace que el paso se quede corto o se pase. Con η = 1,1 el factor es −1,2: el signo alterna mientras la magnitud crece hasta 6,19, y ese crecimiento alterno es el `nan` de un entrenamiento real. De ahí la primera comprobación ante un `nan`: bajar η a la décima parte antes de tocar nada más.
fuente: figuras/tasas-de-aprendizaje-y-schedulers-1.py
:::

## Código

```python verificable
import numpy as np

# Calentamiento lineal + coseno, el plan tipico de un transformer pequeno.
def lr(paso, total=1000, calentamiento=100, lr_max=3e-4):
    if paso < calentamiento:
        return lr_max * paso / calentamiento          # subida lineal
    # El progreso se mide solo sobre lo que queda DESPUES del calentamiento, no sobre total
    progreso = (paso - calentamiento) / (total - calentamiento)
    return 0.5 * lr_max * (1 + np.cos(np.pi * progreso))

for paso in (0, 50, 100, 300, 600, 1000):
    # :>4 alinea a la derecha en 4 caracteres para que la columna no baile
    print(f"paso {paso:>4}  lr {lr(paso):.6f}")
# -> paso    0  lr 0.000000
# -> paso   50  lr 0.000150
# -> paso  100  lr 0.000300
# -> paso  300  lr 0.000265
# -> paso  600  lr 0.000124
# -> paso 1000  lr 0.000000
```

:::claves
- El plan devuelve la tasa **absoluta**, no un multiplicador. En PyTorch, `LambdaLR` espera una
  función que devuelva un factor sobre la `lr` base del optimizador, y el bloque ilustrativo de
  abajo lo hace así (`paso / 100`). Pasarle esta función multiplicaría la tasa por sí misma y el
  plan quedaría escalado al cuadrado, con el calentamiento convertido en una curva cuadrática.
- `progreso` se calcula con `(paso - calentamiento) / (total - calentamiento)`, no con
  `paso / total`. Con `paso / total`, en el paso 100 el coseno ya valdría `cos(0,1π)` y el plan
  entero iría adelantado; el calentamiento dejaría de encadenar con el descenso.
- `np.cos(np.pi * progreso)` devuelve un `numpy.float64`, no un `float` de Python. Al imprimirlo
  con `:.6f` no se nota, pero si ese número se pasa a una función que exige `float` de verdad
  (o se serializa a JSON) hay que envolverlo en `float(...)`.
- `lr(1000)` da `0.000000` exacto: el plan acaba en **cero**, no en un mínimo pequeño. Los
  últimos pasos del entrenamiento se dan con tasa nula, así que no aprenden nada; muchos planes
  reales usan un `η_min` mayor que cero justo por esto.
- Los argumentos con valor por defecto permiten llamar `lr(300)` sin más. En Python esos valores
  se evalúan **una sola vez**, al definir la función: aquí son números y no pasa nada, pero si el
  valor por defecto fuera una lista o un array, todas las llamadas compartirían el mismo objeto.
- `f"paso {paso:>4}"` es formato de presentación y no cambia ningún número: solo rellena con
  espacios a la izquierda. Quitar el `:>4` deja la salida igual de correcta y las columnas
  desalineadas, que es lo que hace difícil comparar dos ejecuciones a ojo.
:::

```python verificable
import numpy as np

# En f(theta) = theta^2 con paso theta <- theta - eta*2*theta, el error se multiplica
# por (1 - 2*eta) en cada iteracion: con eta > 1 el factor supera 1 en valor absoluto.
for eta in (0.1, 0.5, 1.1):
    theta = 1.0
    for _ in range(10):
        theta = theta - eta * 2 * theta
    # {eta:<4} alinea a la izquierda y {:+.1f} fuerza el signo: asi se ve el factor 0.0 y el -1.2
    print(f"eta {eta:<4} factor por paso {1 - 2 * eta:+.1f}  theta tras 10 pasos {theta:+.6f}")
# -> eta 0.1  factor por paso +0.8  theta tras 10 pasos +0.107374
# -> eta 0.5  factor por paso +0.0  theta tras 10 pasos +0.000000
# -> eta 1.1  factor por paso -1.2  theta tras 10 pasos +6.191736
```

```python ilustrativo
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR, LambdaLR, ReduceLROnPlateau

optimizador = optim.AdamW(modelo.parameters(), lr=3e-4)

# Calentamiento de 100 pasos y luego coseno hasta el paso 10000
def plan(paso):
    if paso < 100:
        return paso / 100                      # multiplica la lr base
    progreso = (paso - 100) / (10000 - 100)
    # .item() saca el float de Python del tensor: LambdaLR espera un numero, no un tensor
    return 0.5 * (1 + torch.cos(torch.pi * torch.tensor(progreso))).item()

planificador = LambdaLR(optimizador, plan)
# En PyTorch los planificadores de paso por lote se llaman DESPUES de optimizer.step()
for paso, (x, y) in enumerate(cargador):
    optimizador.zero_grad()
    perdida = criterio(modelo(x), y)
    perdida.backward()
    optimizador.step()
    planificador.step()                        # una vez por lote, no por epoca

# El planificador por metrica se llama con la perdida de validacion, una vez por epoca
por_metrica = ReduceLROnPlateau(optimizador, mode="min", factor=0.1, patience=3)
por_metrica.step(perdida_validacion)

# Tasas distintas por grupo: el backbone preentrenado aprende mas despacio
optimizador = optim.SGD([
    {"params": modelo.backbone.parameters(), "lr": 1e-4},
    {"params": modelo.cabeza.parameters(), "lr": 1e-3},
], momentum=0.9)
coseno = CosineAnnealingLR(optimizador, T_max=50)
```

## Errores típicos

- **Llamar a `scheduler.step()` en el momento equivocado.** Son dos errores en uno. La unidad: el
  planificador que espera una llamada por época, llamado por lote, deja la tasa a casi cero en
  la primera época; el que espera una por lote, llamado por época, apenas cambia nada. Y el
  orden: en PyTorch se actualizan los pesos (`optimizer.step()`) y **después** avanza el
  planificador; al revés, todo el plan va un paso por delante de lo que crees (un desfase, no una
  catástrofe, pero cambia el entrenamiento).
- **Culpar a los datos de un `nan`.** Un `nan` en la pérdida casi siempre empieza por una tasa
  demasiado alta. Bájala a la décima parte y repite antes de revisar el preprocesado. El ejemplo
  de arriba muestra lo rápido que se pierde el control: con `η = 1,1` el error se multiplica por
  −1,2 cada paso.
- **Ajustar la arquitectura antes que la tasa.** Probar cinco arquitecturas con una `η` mal
  elegida no informa sobre ninguna de las cinco. Encuentra el rango bueno con la prueba de rango
  y luego compara arquitecturas.
- **Usar la misma tasa para un backbone preentrenado y una cabeza nueva.** La cabeza parte de
  pesos aleatorios y necesita pasos grandes; el backbone ya está bien y con pasos grandes se
  destroza. Usa grupos de parámetros con tasas distintas y, si hace falta, descongela por capas.
- **Multiplicar el lote por 8 y no tocar nada más.** Con SGD, la regla de escalado lineal dice
  que la tasa suba en la misma proporción, y el calentamiento se alargue para no desestabilizar
  los primeros pasos. Si no lo haces, no estás comparando lo mismo.
- **Poner un calentamiento de 10 pasos en un transformer.** El calentamiento tiene que cubrir la
  fase en la que las estadísticas de Adam todavía son malas: unos cientos de pasos, o un 1-5 %
  del total. Con 10 pasos no protege de nada.

:::practica
enunciado: Entrenas 120 épocas con η₀ = 0,2 y un plan de escalones que multiplica la tasa por 0,1 cada 40 épocas. ¿Qué tasa usa la época 90 y cuántas épocas se entrenan con una tasa superior a 0,01?
pista: El exponente del decaimiento es la parte entera de t/T; cuenta cuántos tramos quedan todavía por encima del umbral.
solucion: Con T = 40, ⌊90/40⌋ = 2, así que η = 0,2 · 0,1² = 0,002. Los tramos son 0,2 (épocas 0-39), 0,02 (40-79) y 0,002 (80-119): por encima de 0,01 solo quedan los dos primeros, 80 épocas. Desde la época 80 la tasa es cien veces menor, que es justo el afino que busca el plan.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Para qué sirve el calentamiento en los primeros pasos de un entrenamiento con Adam?
o: Para que la pérdida baje más rápido al principio
o: Para evitar pasos demasiado grandes cuando las estimaciones del segundo momento de Adam son todavía malas y las activaciones inestables
o: Para que la tasa de aprendizaje acabe siendo más alta
a: 2
e: Las medias de Adam arrancan en cero y tardan unos pasos en ser representativas; si además el modelo es profundo y con normalización, las primeras actualizaciones son peligrosas. El calentamiento sube la tasa poco a poco y cubre ese tramo. No acelera la convergencia: la frena al principio a cambio de estabilidad.
:::

:::quiz
p: Con un plan de coseno de `η_max = 0,1` a `η_min = 0` durante 100 pasos, ¿qué tasa hay en el paso 50?
o: 0,1
o: 0,05
o: 0,0146
a: 2
e: En el punto medio del coseno, cos(π/2) = 0, así que η = 0,05 · (1 + 0) = 0,05: la mitad de la tasa máxima. En el paso 25 estaría en 0,0854 y en el 75 en 0,0146: la curva pasa mucho tiempo cerca del máximo y se desploma al final.
:::

:::quiz
p: Entrenas con 1000 lotes por época y un planificador pensado para avanzar una vez por época, pero lo llamas dentro del bucle de lotes. ¿Qué pasa?
o: Nada, el planificador lo detecta y se ajusta
o: La tasa de aprendizaje se reduce 1000 veces en la primera época y el entrenamiento se queda con pasos casi nulos
o: La tasa de aprendizaje se multiplica por 1000 y el entrenamiento diverge
a: 2
e: Cada llamada avanza un paso del plan, así que al final de la primera época has consumido el plan entero y la tasa queda en su suelo (o en cero). El entrenamiento no divergirá, pero se quedará parado y parecerá un problema de arquitectura o de datos.
:::

:::truco
Si no sabes por dónde empezar, prueba 10⁻³ con Adam y 10⁻¹ con SGD con momento, y ajusta con un
factor 3 arriba o abajo. Antes de gastar horas en arquitectura, gasta veinte minutos en una
prueba de rango: es el hiperparámetro que más mueve la aguja.
:::
