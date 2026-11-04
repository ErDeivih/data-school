---
id: optimizadores
titulo: Optimizadores
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [derivadas-parciales-y-gradiente, retropropagacion, funciones-de-perdida]
tags: [optimizacion, entrenamiento, gradiente, adam]
resumen: La regla que convierte el gradiente en un paso sobre los pesos; SGD, momento, RMSprop, Adam y AdamW hacen cosas distintas con la misma información.
fuentes: ["Kingma y Ba (2015), 'Adam: A Method for Stochastic Optimization'", "Loshchilov y Hutter (2019), 'Decoupled Weight Decay Regularization'", "Wilson et al. (2017), 'The Marginal Value of Adaptive Gradient Methods in Machine Learning'"]
---

## En una frase

El optimizador es la regla que decide cuánto y en qué dirección mover cada peso a partir del
gradiente: SGD da un paso proporcional al gradiente, el momento acumula velocidad para
atravesar valles estrechos y Adam ajusta el tamaño del paso parámetro a parámetro según cómo de
grande haya sido su gradiente últimamente.

## La idea

Estás en una ladera con niebla y solo notas la pendiente bajo tus pies. Para bajar, das un paso
en la dirección de máxima bajada; ese paso es la **tasa de aprendizaje** (`η`). En una ladera
redonda funciona. En un valle estrecho y alargado, no: la pared te obliga a dar pasos
diminutos para no subir por el otro lado, y con esos pasos tardas una eternidad en avanzar por
el fondo del valle. Ese es el problema real de entrenar redes: la curvatura de la pérdida es
muy distinta según la dirección.

El **momento** lo arregla en parte con física de instituto: en vez de dar el paso solo con la
pendiente actual, mantienes una velocidad `v` que se va acumulando, y das el paso con ella. Las
oscilaciones laterales se cancelan entre sí (van y vienen, se restan) mientras que el avance
constante por el fondo se suma. Es una bola pesada rodando: se ignora el temblor y se conserva
la inercia. El precio: el paso efectivo se multiplica por `1 / (1 − β)`, así que con `β = 0,9`
es diez veces mayor y hay que bajar `η` para no desestabilizar el entrenamiento.

**RMSprop** ataca el problema por otro lado: guarda una media de los gradientes al cuadrado de
cada parámetro y divide el paso por su raíz. Un parámetro que lleva muchos pasos con gradientes
grandes recibe pasos pequeños, y uno con gradientes pequeños recibe pasos relativamente
grandes. Es un tamaño de paso **por parámetro**, no uno global. **Adam** es la combinación de
los dos: momento (media del gradiente) más RMSprop (media del cuadrado), con una corrección
para que las medias que arrancan en cero no desvirtúen los primeros pasos. Por eso es el
optimizador por defecto.

La memoria es la factura que pagas por esa comodidad: SGD no guarda nada, el momento guarda un
vector del tamaño de los pesos, y Adam guarda dos (la media del gradiente y la del cuadrado).
En un modelo con miles de millones de parámetros, eso es la diferencia entre que quepa o no
quepa. Y no todo son ventajas: Adam converge rápido al principio, pero varios trabajos —entre
ellos el de Wilson y colaboradores de 2017— muestran que en algunos problemas de clasificación
de imágenes un SGD con momento bien ajustado generaliza mejor. No es una ley, es un aviso:
prueba los dos y compara en validación, no en entrenamiento.

:::nota
`AdamW` no es un optimizador nuevo: es Adam con el decaimiento de pesos **desacoplado**. En
Adam, si metes la penalización L2 dentro del gradiente, ese término también se divide por la
raíz de la media de cuadrados, así que los parámetros con gradientes grandes reciben menos
regularización efectiva de la que crees. `AdamW` resta `η · λ · θ` aparte y recupera el
comportamiento de SGD.
:::

## Definición formal

Con `θ` el vector de parámetros, `L` la pérdida, `g = ∇_θ L` su gradiente y `η` la tasa de
aprendizaje:

:::formula
SGD:  θ ← θ − η · g
:::

- `θ` — todos los pesos y sesgos del modelo, aplanados en un vector.
- `g` — gradiente de la pérdida respecto a `θ`, calculado por
  [[retropropagacion|retropropagación]] sobre el lote actual.
- `η` — tasa de aprendizaje: el tamaño del paso.

:::formula
Momento:  v ← β · v + g        θ ← θ − η · v
:::

- `v` — velocidad acumulada, un vector del mismo tamaño que `θ`, inicializado a cero.
- `β` — coeficiente de momento (0,9 es el valor habitual); la fracción de velocidad que
  sobrevive a cada paso. `β = 0` deja el SGD puro.
- Es la convención de `torch.optim.SGD(momentum=β)` sin amortiguación: el paso efectivo en
  régimen estacionario es `η / (1 − β)`.

:::formula
RMSprop:  s ← ρ · s + (1 − ρ) · g²        θ ← θ − η · g / (√s + ε)
:::

- `s` — media exponencial del gradiente al cuadrado, elemento a elemento.
- `g²` — el gradiente elevado al cuadrado, no el gradiente de `g²`.
- `ρ` — factor de decaimiento de esa media; 0,9 en la formulación original y valores como 0,99
  en algunas implementaciones.
- `ε` — constante pequeña (1e-8) que evita dividir por cero.

:::formula
Adam:  m ← β₁·m + (1−β₁)·g        v ← β₂·v + (1−β₂)·g²
:::

:::formula
m̂ = m / (1 − β₁ᵗ)        v̂ = v / (1 − β₂ᵗ)        θ ← θ − η · m̂ / (√v̂ + ε)
:::

- `m` — media exponencial del gradiente: el momento.
- `v` — media exponencial del gradiente al cuadrado: la escala.
- `β₁ = 0,9`, `β₂ = 0,999` — decaimientos por defecto; `t` — número de paso, empezando en 1.
- `m̂`, `v̂` — las mismas medias corregidas de sesgo, porque arrancan en cero.
- `1 − β₁ᵗ` y `1 − β₂ᵗ` — el factor de corrección; en `t = 1` valen 0,1 y 0,001.

:::formula
AdamW:  θ ← θ − η · m̂ / (√v̂ + ε) − η · λ · θ
:::

- `λ` — coeficiente de decaimiento de pesos, aplicado como un encogimiento aparte y no dentro
  de `g`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `θ` | todos los pesos y sesgos del modelo, aplanados en un vector | las del parámetro | Al crecer sus valores, crece también el término de decaimiento `η·λ·θ`: el mismo `λ` regulariza más a los pesos que ya son grandes |
| `g` | gradiente de la pérdida respecto a `θ`, calculado por retropropagación | las de la pérdida partido por las de `θ` | Es la única información que reciben todas las reglas. Si sube, todos dan pasos mayores, cada uno con su propia fórmula |
| `η` | tasa de aprendizaje: el tamaño del paso | las de `θ` partido por las de `g` | Escala **todo** el entrenamiento. En una cuadrática el error se multiplica por `(1 − η·curvatura)` en cada paso: cuando ese factor supera 1 en valor absoluto, el entrenamiento diverge |
| `v` (momento) | velocidad acumulada del gradiente | las de `g` | Al subir, el paso se hace mayor. En régimen estacionario tiende a `η/(1 − β)`, así que activar el momento multiplica el paso efectivo por diez sin tocar `η` |
| `β` | fracción de velocidad que sobrevive a cada paso | adimensional, entre 0 y 1 | Cuanto más cerca de 1, más memoria y mayor el paso efectivo `η/(1 − β)`. Con `β = 0` queda el SGD puro, así que subirlo obliga a bajar `η` |
| `s` / `v` (RMSprop y Adam) | media exponencial del gradiente al cuadrado | las de `g²` | Al subir, el paso `g/(√v̂ + ε)` se hace más pequeño: un parámetro con gradientes grandes se frena solo. Es el mecanismo que iguala escalas muy distintas |
| `ρ` | factor de decaimiento de esa media en RMSprop | adimensional, entre 0 y 1 | Memoria más larga de la escala: el optimizador reacciona más despacio a un cambio de curvatura y suaviza más el ruido |
| `β₁`, `β₂` | decaimientos de las medias de `g` y de `g²` en Adam | adimensionales, entre 0 y 1 | `β₂` alto (0,999) mide la escala sobre muchos pasos y `β₁` alto da más inercia. Tocarlos cambia el paso efectivo: hay que reajustar `η` a la vez |
| `t` | número de paso, empezando en 1 | iteraciones | Solo entra en la corrección de sesgo: en `t = 1` los factores valen 0,1 y 0,001, y enseguida se acercan a 1. La corrección solo importa en el arranque |
| `m̂`, `v̂` | las medias de Adam corregidas de sesgo | las de `g` y de `g²` | Sin corregir, el primer paso sale 3,16·`η` sin que nadie lo haya pedido; corregido mide exactamente `η` en valor absoluto en cualquier dirección |
| `ε` | constante pequeña que evita dividir por cero | las de `√v̂` | Con el valor por defecto (1e-8) es irrelevante. Al subirlo (1e-4) deja de normalizar en los parámetros con gradientes diminutos y el paso vuelve a ser proporcional al gradiente |
| `λ` | coeficiente de decaimiento de pesos en AdamW | 1 partido por las de `θ` | Encoge los pesos un `η·λ·θ` por paso, aparte del gradiente: al subirlo hay más regularización y menos capacidad efectiva del modelo |
:::

La corrección de sesgo es más importante de lo que parece. Sin ella, en el primer paso
`m = 0,1·g` y `v = 0,001·g²`, de modo que `m / √v = 0,1 / 0,0316 = 3,16`: el primer paso sale
3,16 veces más grande que `η` sin que nadie lo haya pedido. Con la corrección, `m̂ = g` y
`v̂ = g²`, y el primer paso mide exactamente `η` en valor absoluto.

## Ejemplo

Minimizamos `f(x, y) = 0,5 · (x² + 100·y²)` desde el punto `(1, 1)`. El gradiente es
`(x, 100·y)`: la dirección `y` tiene curvatura 100 y la `x` curvatura 1, así que es un valle
estrecho. Con SGD, el factor de contracción en `y` es `1 − 100·η`, y para que no crezca hace
falta `η < 0,02`.

- Primer paso con `η = 0,015` desde `(1, 1)`: `x = 1 − 0,015 = 0,985` e
  `y = 1 − 1,5 = −0,5`. Cada paso posterior multiplica `y` por `−0,5`, así que tras 20 pasos
  `y = 0,5²⁰ ≈ 9,5·10⁻⁷`. Y `x = 0,985²⁰ = 0,7391`.
- Con `η = 0,025`, el factor en `y` es `1 − 2,5 = −1,5`: cada paso multiplica por 1,5 y la
  pérdida acaba en `5,5·10⁸`. Dos milésimas por encima del límite y el entrenamiento está
  destruido.
- Con momento `β = 0,9` y el mismo `η = 0,015`, el paso efectivo es `η/(1 − β) = 0,15`, que
  multiplicado por la curvatura 100 da 15: el valle explota igual. El momento no es gratis, hay
  que bajar `η`.
- Con Adam y `η = 0,05`, tras 20 pasos las dos coordenadas valen `0,111`, aunque el gradiente
  de `y` sea 100 veces mayor que el de `x`. La normalización por `√v̂` iguala los pasos.

En la tabla del bloque de código, las cuatro configuraciones con sus pérdidas. La lección es
que el mismo gradiente, con cuatro reglas distintas, da cuatro resultados que no se parecen en
nada.

:::figura
fichero: optimizadores-valle-y-perdida
pie: El panel izquierdo dibuja las curvas de nivel de `0,5·(x² + 100·y²)`: elipses tan alargadas que el valle es una grieta, cien veces más curvoso en `y` que en `x`. Cada punto es un paso desde (1, 1) y la estrella marca el mínimo. SGD avanza en `x` y oscila en `y` sin poder bajar por la pared: llega al fondo del valle pero se queda a 0,74 del mínimo en la dirección que sí importa. Adam, con un paso cinco veces mayor, llega al entorno del centro con las dos coordenadas iguales (0,11) porque divide el paso por la raíz de la media de cuadrados y eso iguala escalas de curvatura muy distintas. El panel derecho es la misma historia contada con la pérdida, en escala logarítmica: las dos reglas de SGD se separan por dos milésimas de tasa de aprendizaje; con 0,015 el error se contrae y con 0,025 el factor por paso es `1 − 100·η = −1,5`, así que cada iteración multiplica el error por 1,5 hasta 5,5·10⁸. La curva del momento enseña el precio de la inercia: el paso efectivo se multiplica por `1/(1−β) = 10` y, sin bajar `η`, el valle se descontrola. Conclusión práctica: `η` no se elige por gusto, se elige comparando la curvatura mayor del problema con el paso efectivo de la regla.
fuente: figuras/optimizadores-1.py
:::

## Código

```python verificable
import numpy as np

# Valle estrecho: curvatura 1 en x y 100 en y. Para SGD, el factor de contraccion
# en y es (1 - 100*eta), asi que el limite de estabilidad es eta < 0.02.
def valle(eta, beta=None, pasos=20):
    q = np.array([1.0, 1.0])
    v = np.zeros(2)                      # velocidad del momento, del tamano de q
    for _ in range(pasos):
        g = np.array([q[0], 100.0 * q[1]])
        if beta is None:                 # SGD puro
            q = q - eta * g
        else:                            # momento: la velocidad acumula el gradiente
            v = beta * v + g
            q = q - eta * v
    return q

def adam(eta, pasos=20):
    q = np.array([1.0, 1.0]); m = np.zeros(2); v = np.zeros(2)
    for t in range(1, pasos + 1):        # t empieza en 1: la correccion usa 0.9 ** t
        g = np.array([q[0], 100.0 * q[1]])
        m = 0.9 * m + 0.1 * g            # media del gradiente
        v = 0.999 * v + 0.001 * g ** 2   # media del gradiente al cuadrado
        q = q - eta * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
    return q

for nombre, q in [("sgd  eta=0.015", valle(0.015)),
                  ("sgd  eta=0.025", valle(0.025)),
                  ("mom  eta=0.015", valle(0.015, 0.9)),
                  ("adam eta=0.050", adam(0.05))]:
    perdida = 0.5 * (q[0] ** 2 + 100 * q[1] ** 2)
    # +.2e imprime con signo y en notacion cientifica: con .2f esta coordenada saldria 0.00
    print(f"{nombre}  x {q[0]:+.4f}  y {q[1]:+.2e}  perdida {perdida:.3e}")
# -> sgd  eta=0.015  x +0.7391  y +9.54e-07  perdida 2.732e-01
# -> sgd  eta=0.025  x +0.6027  y +3.33e+03  perdida 5.529e+08
# -> mom  eta=0.015  x -0.1247  y -3.91e-01  perdida 7.669e+00
# -> adam eta=0.050  x +0.1112  y +1.11e-01  perdida 6.247e-01
```

:::claves
- `q = q - eta * g` **no modifica** `q` en el sitio: crea un array nuevo y reasigna el nombre.
  Con `q -= eta * g` el resultado sería el mismo aquí, pero si `q` estuviera compartido con otra
  variable (algo muy fácil en un bucle) la modificarías sin querer.
- `beta=None` separa «sin momento» de «momento con `β = 0`». En la fórmula no son la misma rama:
  el `if` deja claro que son dos reglas distintas, y pasar `β = 0` cae por la del momento.
- `for t in range(1, pasos + 1)`: `t` empieza en **1**, no en 0, porque la corrección de sesgo
  usa `0.9 ** t` en el denominador y con `t = 0` quedaría una división por cero.
- El `1e-8` va **fuera** de la raíz y sumando al denominador: `np.sqrt(v / (1 - 0.999 ** t)) + 1e-8`.
  Es la convención de `torch.optim.Adam`. Meterlo dentro de la raíz cambia muy poco el resultado,
  pero deja de coincidir con la fórmula que se cita en el artículo.
- `f"{q[1]:+.2e}"` imprime con signo y en notación científica, y por eso se ve `+9.54e-07`. Con
  `:.2f` esa coordenada saldría `0.00` y parecería que no se ha movido, cuando es justo la que
  más ha bajado: elegir el formato es parte de leer bien el resultado.
- La pérdida se calcula **al final**, sobre el punto de llegada, y el bucle no la acumula. Para
  comparar configuraciones basta el punto final; para ver la curva de convergencia hay que
  guardar el valor en cada paso, y entonces la escala logarítmica es imprescindible porque los
  valores abarcan diez órdenes de magnitud.
- Dentro de `adam()`, `m` y `v` se reinician en cada llamada: son **estado del optimizador**, no
  del modelo. En PyTorch viven dentro del objeto `optimizer`, y por eso `optimizer.zero_grad()`
  no los borra: lo que pone a cero son los `.grad`, que son otra cosa.
- El diccionario de grupos de `torch.optim.SGD([{...}, {...}], momentum=0.9)` define **tasa de
  aprendizaje por grupo**: el backbone con `1e-4` y la cabeza nueva con `1e-3`. Es la forma
  habitual de ajustar fino sin destruir lo que el modelo ya sabía.
:::

```python verificable
import numpy as np

# Correccion de sesgo de Adam: sin ella el primer paso es 3.16 veces eta, porque las
# medias arrancan en cero (0.1 / sqrt(0.001) = 3.16).
g = 2.0
m, v = 0.1 * g, 0.001 * g ** 2
print(f"sin corregir  {m / np.sqrt(v):.4f}")            # -> sin corregir  3.1623
mh, vh = m / (1 - 0.9), v / (1 - 0.999)                 # 1 - beta**t con t = 1
print(f"corregido     {mh / np.sqrt(vh):.4f}")          # -> corregido     1.0000

# Con la correccion, el primer paso mide eta en cualquier direccion: el gradiente
# se normaliza y solo importa su signo.
print(f"paso en x  {0.05 * mh / (np.sqrt(vh) + 1e-8):.4f}")   # -> paso en x  0.0500
```

```python ilustrativo
import torch

# El modelo y los datos ya estan definidos; aqui solo se elige la regla de actualizacion.
optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4, weight_decay=0.01)
# betas=(0.9, 0.999) y eps=1e-8 son los valores por defecto

for x, y in cargador:
    optimizador.zero_grad()              # sin esto los .grad se SUMAN a los del lote anterior
    perdida = criterio(modelo(x), y)
    perdida.backward()                   # calcula los gradientes, no mueve nada
    optimizador.step()                   # aquí es donde se aplica la regla del optimizador

# Tasas distintas para el backbone preentrenado y la cabeza nueva: dos grupos
optimizador = torch.optim.SGD([
    {"params": modelo.backbone.parameters(), "lr": 1e-4},
    {"params": modelo.cabeza.parameters(), "lr": 1e-3},
], momentum=0.9, nesterov=True)
```

## Errores típicos

- **Cambiar el tamaño del lote sin tocar la tasa de aprendizaje.** El gradiente de un lote es
  un promedio, así que pasar de 32 a 256 ejemplos reduce el ruido pero no la escala; lo que sí
  cambia es cuánta información usas por paso. La receta clásica es escalar `η` de forma
  proporcional al lote (con un calentamiento al principio) y no dejarla igual. Si no lo haces,
  el entrenamiento se vuelve lento o inestable según el caso.
- **Creer que Adam es siempre mejor.** Con gradientes muy dispares, Adam avanza donde SGD se
  atasca; pero su paso está acotado por `η`, así que en problemas suaves y bien escalados un
  SGD con momento y una `η` alta puede avanzar mucho más por época. Hay además trabajos que
  observan peor generalización de los métodos adaptativos en algunos problemas de visión. Mide
  en validación con los dos.
- **Poner decaimiento de pesos en Adam y esperar el comportamiento de SGD.** El término L2
  entra en `g`, y `g` se divide por `√v̂`: los parámetros con gradiente grande reciben menos
  encogimiento efectivo. Si quieres decaimiento de pesos de verdad, usa `AdamW` y no lo mezcles
  con `weight_decay` dentro del optimizador adaptativo.
- **Aplicar el momento y olvidar el factor `1/(1 − β)`.** El error del ejemplo: subir `β` de
  0 a 0,9 multiplica el paso efectivo por 10 sin tocar `η`. Si activas el momento y el
  entrenamiento diverge, lo primero que hay que bajar es `η`, no el momento.
- **Poner `ε` grande.** Con `ε = 1e-4`, en los parámetros cuyos gradientes son diminutos
  —embeddings de palabras raras, por ejemplo— la división `g/(√v + ε)` deja de normalizar y el
  paso se vuelve proporcional al gradiente otra vez. Deja el valor por defecto salvo que sepas
  por qué lo cambias.
- **Meter los sesgos y los parámetros de normalización en el decaimiento de pesos.** Encoger
  `β` y `γ` de una capa de [[normalizacion-por-lotes|normalización]] o los sesgos hacia cero
  limita la capacidad del modelo sin ganar regularización útil. Lo habitual es excluirlos del
  grupo con decaimiento.

:::practica
enunciado: Con SGD y momento β = 0,9, tasa η = 0,01 y un gradiente constante g = 2, calcula la velocidad v y el desplazamiento acumulado del peso θ en los tres primeros pasos, partiendo de θ = 0. ¿Cuánto se ha movido en total y cuánto se habría movido con SGD puro?
pista: v ← β·v + g y θ ← θ − η·v. Con SGD puro el paso es siempre η·g, sin acumular nada.
solucion: Paso 1: v = 2, θ = −0,02. Paso 2: v = 0,9·2 + 2 = 3,8, θ = −0,058. Paso 3: v = 0,9·3,8 + 2 = 5,42, θ = −0,1122. Con SGD puro serían tres pasos de 0,02, o sea θ = −0,06. El momento casi duplica el avance porque la velocidad se acumula, y en régimen estacionario el paso efectivo tiende a η/(1 − β) = 0,1.
:::

## Comprueba que lo sabes

:::quiz
p: En el valle `f(x, y) = 0,5·(x² + 100·y²)`, con SGD y `η = 0,015` el entrenamiento va bien, pero con `η = 0,025` la pérdida llega a 5,5·10⁸. ¿Por qué?
o: Porque la pérdida tiene mínimos locales que atrapan al optimizador
o: Porque en la dirección de curvatura 100 el factor por paso es 1 − 100·η, y con η = 0,025 su valor absoluto es 1,5: cada paso multiplica el error por 1,5
o: Porque Adam y SGD no se pueden comparar en el mismo problema
a: 2
e: En una cuadrática el paso se repite multiplicando el error por (1 − η·curvatura). Con curvatura 100 y η = 0,025 ese factor vale −1,5, así que el error alterna de signo y crece un 50 % por paso: 20 pasos son un factor 3.325. Con η = 0,015 el factor es −0,5 y el error se desploma.
:::

:::quiz
p: ¿Qué aporta exactamente la corrección de sesgo de Adam?
o: Evita que el optimizador se quede atascado en un punto de silla
o: Corrige que `m` y `v` arranquen en cero, para que los primeros pasos no salgan 3,16 veces más grandes que `η`
o: Garantiza que la pérdida baje en cada iteración
a: 2
e: Las medias exponenciales necesitan unos cuantos pasos para acercarse a su valor real, y mientras tanto están sesgadas hacia cero. Dividir por (1 − β₁ᵗ) y (1 − β₂ᵗ) deshace ese sesgo: en t = 1, m/√v pasa de 3,16 a 1. Adam no garantiza que la pérdida baje en cada paso ni resuelve los puntos de silla por sí solo.
:::

:::quiz
p: Pasas de un lote de 32 a uno de 256 manteniendo la misma tasa de aprendizaje. ¿Qué esperas?
o: Que el entrenamiento sea más estable pero avance menos por época, y que haya que subir η o usar un calentamiento
o: Exactamente el mismo entrenamiento, solo más rápido en wall-clock
o: Que la pérdida se multiplique por 8
a: 1
e: El gradiente sigue siendo un promedio, no una suma, así que su escala no cambia; lo que cambia es el número de actualizaciones por época (8 veces menos) y el ruido, que se reduce. La regla práctica es escalar η con el lote y añadir un calentamiento corto para no desestabilizar las primeras iteraciones.
:::

:::trampa
Un `nan` en la pérdida a las pocas iteraciones casi nunca es «un dato malo»: es una tasa de
aprendizaje demasiado alta, un `log(0)` en la pérdida o una división por cero. Baja `η` a la
décima parte antes de tocar el modelo, y mira
[[depuracion-de-redes|las comprobaciones de depuración]] en orden.
:::
