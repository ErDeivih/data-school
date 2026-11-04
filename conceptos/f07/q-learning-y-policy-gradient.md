---
id: q-learning-y-policy-gradient
titulo: Q-learning y gradiente de política
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [aprendizaje-por-refuerzo, derivadas-parciales-y-gradiente, valor-esperado, optimizadores]
tags: [refuerzo, q-learning, policy-gradient, bellman]
resumen: Las dos familias del refuerzo profundo: aprender el valor de cada accion y actuar con avaricia, o parametrizar la política y subir su retorno esperado con gradiente.
fuentes: ["Watkins y Dayan (1992), 'Q-learning'", "Williams (1992), 'Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning'", "Sutton et al. (2000), 'Policy Gradient Methods for Reinforcement Learning with Function Approximation'"]
---

## En una frase

El Q-learning aprende cuánto vale cada acción en cada estado y luego actúa eligiendo la de más
valor; el gradiente de política no aprende valores, aprende directamente los parámetros de la
política empujándola en la dirección de las acciones que dieron buen retorno.

## La idea

Hay dos formas de decidir bien en una situación repetida.

La primera es **tomar notas**. Cada vez que estás en una situación y pruebas una acción, apuntas
lo que crees que vas a ganar con ella: «en el pasillo, girar a la derecha: −3,4; girar a la
izquierda: −4,1». Con esas notas, decidir es trivial: elige el número más alto. Eso es
Q-learning: aprender una tabla `Q(s, a)` de valores y actuar con avaricia sobre ella. La nota se
actualiza con lo que ganas ahora más lo que crees que ganarás después, y esa mezcla entre lo
observado y lo estimado es la esencia de las ecuaciones de
[[aprendizaje-por-refuerzo|Bellman]].

La segunda es **ajustar la receta**. No llevas notas de cada acción: tienes una política
parametrizada (por ejemplo, una red que devuelve `π(a|s)`) y, cada vez que una acción sale bien,
subes un poco su probabilidad; cuando sale mal, la bajas. No necesitas saber cuánto vale cada
acción, solo en qué dirección mover los parámetros para que el retorno esperado crezca. Eso es
el gradiente de política.

Las diferencias prácticas entre las dos familias explican por qué existen ambas:

- **Q-learning es off-policy.** Puede aprender de datos generados por cualquier política,
  incluida una antigua o aleatoria, porque su objetivo es estimar el valor óptimo, no el de la
  política que actúa. Eso permite guardar experiencias en un búfer y reutilizarlas.
- **REINFORCE es on-policy.** Su estimación del gradiente usa el retorno de la política actual;
  si reciclas trayectorias viejas, estás estimando el gradiente de otra política. Hay correcciones
  (importancia) pero añaden varianza.
- **Q-learning solo actúa bien con acciones discretas y pocas**, porque necesita calcular el
  máximo sobre todas las acciones. Con un brazo robótico de 7 articulaciones continuas, ese
  máximo es un problema de optimización dentro del bucle de aprendizaje.
- **El gradiente de política maneja acciones continuas y políticas estocásticas** de forma
  natural, y es lo que se usa en los modelos de lenguaje modernos con RLHF, donde la «acción» es
  elegir un token entre decenas de miles.

En la práctica, el gradiente de política puro tiene una varianza enorme, y por eso casi todo lo
que se usa hoy es **actor-crítico**: un actor (la política) y un crítico (una red que estima el
valor) que se ayudan mutuamente. Eso une las dos ideas de esta página.

## Definición formal

**Q-learning.** Con una tabla `Q(s, a)` y una transición observada `(s, a, r, s')`, la
actualización es

:::formula
Q(s, a) ← Q(s, a) + α · [ r + γ · max_{a'} Q(s', a') − Q(s, a) ]
:::

- `α` — la tasa de aprendizaje; cuánto se corrige la estimación con cada observación.
- `γ` — el factor de descuento, definido en [[aprendizaje-por-refuerzo|el MDP]].
- `r + γ · max_{a'} Q(s', a')` — el **objetivo**: la recompensa recibida más el mejor valor
  estimado del estado siguiente.
- `δ = r + γ · max_{a'} Q(s', a') − Q(s, a)` — el **error de diferencia temporal** (error TD).
  Si `δ = 0`, la tabla ya es coherente con las ecuaciones de Bellman.

La actualización es off-policy porque usa `max_{a'}`, la mejor acción, no la que ejecutará la
política que está explorando. Converge al óptimo `Q*` si todo par `(s, a)` se visita infinitas
veces y `α` cumple las condiciones habituales de decrecimiento (suma divergente, suma de
cuadrados convergente). Con `α` constante no converge a un punto: oscila alrededor.

**Gradiente de política.** Se parametriza `π_θ(a | s)` y se maximiza el retorno esperado
`J(θ) = E_{s∼d_π}[V^{π_θ}(s)]`. El teorema del gradiente de política dice que

:::formula
∇_θ J(θ) = E_{π_θ}[ ∇_θ log π_θ(a | s) · Q^{π_θ}(s, a) ]
:::

- `∇_θ log π_θ(a | s)` — la dirección en la que hay que mover `θ` para hacer esa acción `a` más
  probable en ese estado `s`.
- `Q^{π_θ}(s, a)` — el peso: si la acción valió mucho, el paso es grande en esa dirección; si
  valió poco o negativo, el paso va en contra.
- `E_{π_θ}[·]` — esperanza sobre estados visitados y acciones muestreadas **con la política actual**.

La versión más simple, **REINFORCE**, sustituye `Q^{π_θ}(s, a)` por el retorno muestreado `G_t`
de la trayectoria. El estimador es insesgado y de varianza alta. Para reducirla se resta una
**línea base** `b(s)` que no dependa de la acción:

:::formula
∇_θ J(θ) ≈ E[ ∇_θ log π_θ(a|s) · ( G_t − b(s) ) ]
:::

Como `E_{a∼π}[∇_θ log π_θ(a|s)] = 0`, restar `b(s)` no sesga el gradiente, solo cambia su
varianza. Lo habitual es `b(s) = V(s)`, y entonces `G_t − V(s)` se parece mucho a la **ventaja**
`A(s, a) = Q(s, a) − V(s)`: cuánto mejor es esta acción que lo normal en ese estado.

Con acciones discretas, la política se parametriza con un softmax sobre unas puntuaciones
`h_θ(s, a)` (el mismo softmax de [[funciones-de-activacion]]): `π_θ(a|s) = exp(h(s,a)) / Σ_{a'} exp(h(s,a'))`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Q(s, a)` | Valor estimado de tomar `a` en `s` y actuar bien después | las de la suma descontada de recompensas | No es una palanca: es lo que se aprende. Al subir, esa acción se vuelve más atractiva para la política avaricia. En el pasillo, el valor del estado 0 es −4,095 porque es la suma descontada de los cinco pasos hasta la meta, y todos son negativos porque cada paso cuesta −1 |
| `α` | Tasa de aprendizaje de la tabla | adimensional, entre 0 y 1 | Cada observación corrige más la estimación: con `α = 1` la tabla se queda con el último dato y olvida todo lo anterior; con `α` pequeño aprende despacio. Con `α` constante la tabla nunca se asienta del todo: oscila alrededor del valor verdadero. En tabular se usa `α_t = 1/n(s,a)` |
| `γ` | Factor de descuento del objetivo | adimensional, entre 0 y 1 | Alarga el horizonte: con `γ = 0,9` el valor de `Q(2, derecha)` sale de `−1 + 0,9·(−1)`, y con `γ = 1` el valor se propaga sin perder nada y la tabla tarda mucho más en estabilizarse. Con `γ = 0` el agente solo mira la recompensa del paso actual y no puede planificar |
| `δ` | Error de diferencia temporal: objetivo menos valor actual | las de la recompensa | Es lo que mueve la tabla: `Q ← Q + α·δ`. Al subir `δ` en valor absoluto, la corrección es mayor. Si `δ = 0` la tabla ya es coherente con las ecuaciones de Bellman y ese par `(s, a)` no cambia |
| `max_{a'}` | El mayor valor del estado siguiente sobre todas las acciones | las de `Q` | No es un parámetro, es el operador que hace off-policy al Q-learning. Al tomar el máximo de estimaciones **ruidosas**, el resultado está sesgado hacia arriba: por eso el agente cree que algunos estados malos son buenos, y por eso existe Double Q-learning |
| `J(θ)` | Retorno esperado de la política parametrizada | las de la recompensa acumulada por episodio | Es lo que se maximiza, no una recompensa concreta. Al subir, la política media mejora; el ruido de una sola trayectoria no lo mueve, hacen falta muchas |
| `∇_θ log π_θ(a dado s)` | Dirección en la que hay que mover `θ` para hacer `a` más probable en `s` | adimensional | Apunta siempre a **subir** la probabilidad de la acción elegida; el signo del paso lo decide el peso que lo multiplica. Con una política softmax su magnitud depende de las probabilidades: es máxima cuando `π` está cerca de 0,5 y casi nula cuando `π` ya es 0 o 1 |
| `b(s)` | Línea base: un valor que no depende de la acción | las de la recompensa | No cambia la **esperanza** del gradiente (porque la esperanza de `∇log π` es cero), solo su varianza. Al subirla, el gradiente se centra: sin línea base el estimador REINFORCE es insesgado pero de varianza enorme, y el ruido de la recompensa tapa la señal. Lo habitual es `b(s) = V(s)` |
| `A(s, a)` | Ventaja: cuánto mejor es `a` que lo normal en `s` | las de la recompensa | Es `Q(s, a) − V(s)`, la forma más usada del peso. Al subir, esa acción se refuerza más. Restar `V(s)` es lo que convierte «esta acción dio 10» en «esta acción dio 10, cuando lo normal era 9»: sin eso, en un problema donde todo da positivo, todas las acciones se refuerzan |
:::

## Ejemplo

Pasillo de 6 casillas con la meta en la 5. Acciones izquierda (0) y derecha (1), recompensa
`−1` por cada paso que no llega a la meta, `α = 0,5`, `γ = 0,9`, `ε = 0,2` y 500 episodios.
Tabla aprendida:

```
estado   Q(izquierda)   Q(derecha)
     0         -4.095      -3.439
     1         -4.095      -2.710
     2         -3.439      -1.900
     3         -2.710      -1.000
     4         -1.900       0.000
```

En todos los estados la acción «derecha» tiene más valor, que es la política correcta. El valor
de `Q(4, derecha)` es `0` porque desde la casilla 4 un paso a la derecha llega a la meta y no
hay penalización; `Q(3, derecha) = −1` porque cuesta un paso; `Q(2, derecha) = −1,9`, que es
`−1 + 0,9·(−1)`; y así hacia atrás, descontando un paso cada vez. Siguiendo la política avaricia
desde el estado 0 se llega a la meta en **5 pasos**, la distancia mínima. Fíjate en que el valor
de los estados lejanos (`−4,095` en el estado 0) es grande y negativo: es la suma descontada de
todas las penalizaciones hasta la meta.

Segundo ejemplo: comprobar el teorema del gradiente de política en un bandido de dos acciones
con política softmax de un solo parámetro `θ`. La acción buena da 2, la mala 0,5, y en `θ = 0,5`
la probabilidad de elegir la buena es `p = 0,6225`:

```
gradiente analitico   0.3525
gradiente numerico    0.3525
estimador REINFORCE   0.3539
```

El valor analítico es `p·(1−p)·(2 − 0,5) = 0,6225 · 0,3775 · 1,5 = 0,3525`. La derivada numérica
por diferencias finitas coincide hasta el cuarto decimal, y el estimador REINFORCE —el promedio
de `r·∇log π` sobre 200.000 muestras— da `0,3539`. Esa coincidencia es la demostración práctica
del teorema: **no hace falta conocer la derivada de la recompensa, solo muestrear acciones y
ponderar por lo que dieron**.

:::figura
fichero: q-learning-tabla-y-gradiente
pie: A la izquierda, la tabla `Q` que aprende Q-learning en el pasillo de seis casillas: en todos los estados la barra verde (derecha) es menos negativa que la azul, y de ese signo sale la política sin calcular nada más. El valor del estado 0 es −4,095 porque es la suma descontada de los cinco pasos hasta la meta, y el de la acción derecha en el estado 4 es exactamente 0: desde ahí un paso llega y no hay penalización. A la derecha, la otra familia: en vez de una tabla de valores, el retorno esperado en función del parámetro `θ` de una política softmax. El punto rojo es `θ = 0,5`, donde el teorema del gradiente da 0,3525 mezclando `p·(1−p)` con la diferencia de premios, y no ha hecho falta derivar la recompensa.
fuente: figuras/q-learning-y-policy-gradient-1.py
:::

## Código

```python verificable
import numpy as np

n_estados, meta = 6, 5          # pasillo 0..5; en 5 esta la meta
rng = np.random.default_rng(0)


def paso(s, a):
    s2 = min(max(s + (1 if a == 1 else -1), 0), n_estados - 1)   # 1 = derecha
    return s2, (0.0 if s2 == meta else -1.0)                     # -1 por cada paso


Q = np.zeros((n_estados, 2))
alpha, gamma, epsilon = 0.5, 0.9, 0.2
for _ in range(500):
    s = 0
    for _ in range(50):
        a = int(rng.integers(2)) if rng.random() < epsilon else int(np.argmax(Q[s]))
        s2, recompensa = paso(s, a)
        Q[s, a] += alpha * (recompensa + gamma * Q[s2].max() - Q[s, a])   # error TD
        s = s2
        if s == meta:
            break

print("estado   Q(izquierda)   Q(derecha)")
for s in range(meta):
    print(f"{s:>6}   {Q[s, 0]:12.3f}   {Q[s, 1]:9.3f}")
# -> estado   Q(izquierda)   Q(derecha)
# ->      0         -4.095      -3.439
# ->      1         -4.095      -2.710
# ->      2         -3.439      -1.900
# ->      3         -2.710      -1.000
# ->      4         -1.900       0.000

s, pasos = 0, 0
while s != meta and pasos < 20:
    s, _ = paso(s, int(np.argmax(Q[s])))
    pasos += 1
print(f"pasos desde el estado 0 con la politica greedy: {pasos}")
# -> pasos desde el estado 0 con la politica greedy: 5
```

:::claves
- `Q[s, a] += alpha * (...)` usa `Q[s2].max()`, que es el máximo sobre las dos acciones del estado siguiente. Ese `max` es lo que hace al algoritmo **off-policy**, y también lo que le permite aprender de trayectorias viejas. Fíjate en que `Q` es un array de NumPy y `Q[s, a] += ...` sí modifica el array en el sitio: no hay copia.
- `np.argmax(Q[s])` devuelve el índice del máximo y, con empate, el primero. Al arrancar, `Q = np.zeros((6, 2))` tiene los dos valores empatados a cero en cada estado, así que la política avaricia inicial elige siempre «izquierda» hasta que la primera actualización desempata.
- El `break` de `if s == meta` corta el episodio al llegar, y el `for _ in range(50)` es solo un tope de seguridad para que un agente que se quede dando vueltas no cuelgue el bucle. Sin el tope, un Q-learning mal inicializado puede no terminar nunca.
- `min(max(s + (1 if a == 1 else -1), 0), n_estados - 1)` recorta el movimiento a los extremos del pasillo: en el estado 0, ir a la izquierda deja al agente en el estado 0. Ese rebote es el que hace que los valores de `Q(0, izquierda)` y `Q(1, izquierda)` coincidan (−4,095 en los dos), y no es un error del entrenamiento.
- `Q[s2].max()` se evalúa **antes** de actualizar `Q[s, a]`, y da igual el orden aquí porque son filas distintas; en un entorno con bucles, donde `s2` puede ser `s`, el orden sí cambia el resultado. Es el mismo detalle que en la diferencia entre Q-learning y SARSA.
- El `alpha = 0.5` fijo explica por qué las cifras son −4,095 y no los valores exactos −4,0951…: con tasa constante la tabla oscila alrededor del valor verdadero y nunca se asienta. Con `alpha = 1/n(s, a)` convergería a los valores exactos de la serie descontada.
:::

```python verificable
import numpy as np

premios = np.array([2.0, 0.5])    # recompensa esperada de la accion buena y de la mala


def valor(theta):
    p = 1 / (1 + np.exp(-theta))  # probabilidad de elegir la accion buena
    return p * premios[0] + (1 - p) * premios[1]


theta, h = 0.5, 1e-6
p = 1 / (1 + np.exp(-theta))
analitica = p * (1 - p) * (premios[0] - premios[1])
numerica = (valor(theta + h) - valor(theta - h)) / (2 * h)

rng = np.random.default_rng(0)
muestras = 200000
a = np.where(rng.random(muestras) < p, 0, 1)   # 0 = accion buena, con probabilidad p
grad_log = np.where(a == 0, 1 - p, -p)         # d/dtheta log pi(a)
print(f"analitico {analitica:.4f}  numerico {numerica:.4f}"
      f"  REINFORCE {(premios[a] * grad_log).mean():.4f}")
# -> analitico 0.3525  numerico 0.3525  REINFORCE 0.3539
```

:::claves
- `np.where(rng.random(muestras) < p, 0, 1)` genera el array de acciones muestreadas de golpe: 200.000 tiradas de una vez en vez de un bucle. `rng.random(muestras)` devuelve 200.000 números en [0, 1) y la comparación es un array booleano, que `np.where` convierte en 0 y 1.
- `np.where(a == 0, 1 - p, -p)` es la derivada de `log π` respecto de `θ` para una política logística. No hay que derivar nada a mano en un caso general: en PyTorch esto lo hace `autograd`, pero aquí conviene ver que el gradiente depende **de la acción elegida**, no de todas.
- `(premios[a] * grad_log).mean()` es la media de `r · ∇log π` sobre las muestras, y por eso tiende al gradiente verdadero: es la esperanza que aparece en el teorema. `premios[a]` se llama indexado avanzado y devuelve un array de 200.000 premios, uno por acción muestreada.
- La estimación sale 0,3539 frente al valor exacto 0,3525 porque tiene varianza: con otra semilla daría otro número cercano. El error relativo de un 0,4 % es lo normal con 200.000 muestras; con 200 muestras la cifra bailaría en la segunda decimal.
- `numerica = (valor(theta + h) - valor(theta - h)) / (2 * h)` es la diferencia central, y el `2 * h` es lo que la hace de segundo orden: con `h = 1e-6` el resultado coincide con el analítico hasta el cuarto decimal. Con una diferencia hacia delante (`(valor(θ+h) - valor(θ)) / h`) el error sería de orden `h` y se vería en la cuarta decimal.
- Ni `theta` ni `p` se modifican en todo el bloque: son constantes de las que se calculan las tres estimaciones. Si quisieras comprobar la coincidencia en otro punto, cambia `theta` y recalcula las tres líneas a la vez, o compararás números de puntos distintos.
:::

```python ilustrativo
# REINFORCE con una red de politica. Necesita GPU y un entorno; no se ejecuta.
import torch
from torch.distributions import Categorical

politica = torch.nn.Sequential(
    torch.nn.Linear(4, 64), torch.nn.ReLU(), torch.nn.Linear(64, 2))
optimizador = torch.optim.Adam(politica.parameters(), lr=1e-2)

log_probs, recompensas = [], []
estado = entorno.reset()
while not terminado:
    dist = Categorical(logits=politica(torch.as_tensor(estado, dtype=torch.float32)))
    accion = dist.sample()
    log_probs.append(dist.log_prob(accion))
    estado, r, terminado, _ = entorno.step(accion.item())
    recompensas.append(r)

# El retorno se descuenta de atras hacia delante y se trata como una CONSTANTE.
G, retornos = 0.0, []
for r in reversed(recompensas):
    G = r + 0.99 * G
    retornos.append(G)
retornos = torch.tensor(list(reversed(retornos)))

perdida = -(torch.stack(log_probs) * retornos).sum()   # gradiente de politica x retorno
optimizador.zero_grad()
perdida.backward()
optimizador.step()
```

## Errores típicos

- **Hacer bootstrap desde estados terminales.** Cuando el episodio termina, no existe un estado
  siguiente: el objetivo debe ser solo `r`, sin sumar `γ · max Q(s', a')`. Si no enmascaras esa
  transición, la tabla aprende que después de la meta hay más futuro y el valor se propaga donde
  no debe. En código: multiplicar el término de bootstrap por `(1 − terminado)`.
- **Ignorar el sesgo de maximización.** `max_{a'} Q(s', a')` toma el máximo de estimaciones
  ruidosas, y el máximo de varios números ruidosos está sesgado hacia arriba. El agente acaba
  creyendo que estados malos son buenos. La solución clásica es Double Q-learning: dos tablas (o
  dos redes) y usar una para elegir la acción y la otra para valorarla.
- **Dejar `α` constante en un problema tabular.** Con `α` fijo, la tabla sigue moviéndose con
  cada recompensa aleatoria y nunca se asienta en los valores verdaderos. En tabular se usa
  `α_t = 1/n(s,a)` (media incremental) o un decaimiento; en aproximación con redes, una tasa
  decreciente cumple el mismo papel.
- **Mezclar on-policy y off-policy sin darse cuenta.** Guardar trayectorias de una política
  antigua y usarlas para estimar `∇_θ J` con REINFORCE introduce sesgo: estás evaluando
  acciones con la ponderación de otra distribución. Q-learning sí puede reutilizarlas porque su
  objetivo es `Q*`, independiente de la política que actúa. La corrección de importancia existe,
  pero dispara la varianza.
- **No tratar el retorno como constante al derivar.** En un framework con autograd, la pérdida
  `−G · log π_θ(a|s)` no debe derivar `G` respecto de `θ`: el retorno es un dato, no una función
  de los parámetros (si lo fuera, el gradiente sería otro y estarías optimizando algo distinto).
  Se corta con `detach()` o se construye con valores de la trayectoria ya cerrada.
- **No usar línea base en REINFORCE.** Sin restar `b(s)`, el estimador tiene una varianza enorme
  y el entrenamiento parece no aprender: el ruido de la recompensa domina la señal. Restar la
  media del retorno o `V(s)` no cambia la esperanza del gradiente y suele ser la diferencia
  entre aprender y no aprender.

:::practica
enunciado: En un estado s, Q(s, izquierda) = −1,5 y Q(s, derecha) = 0,3. Tomas «izquierda», recibes r = −2 y llegas a s', donde max Q(s') = −3. Con α = 0,4 y γ = 0,8, actualiza Q(s, izquierda) y di si el error TD es positivo o negativo.
pista: El objetivo es r + γ · max Q(s'); el error TD es ese objetivo menos el valor actual, y la corrección es α veces el error.
solucion: Objetivo = −2 + 0,8 · (−3) = −4,4. Error TD = −4,4 − (−1,5) = −2,9. Nueva Q = −1,5 + 0,4 · (−2,9) = −1,5 − 1,16 = −2,66. El error es negativo, así que la acción estaba sobrevalorada. Conclusión: Q(s, izquierda) baja de −1,5 a −2,66 y «derecha» sigue siendo la mejor acción del estado.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué se dice que Q-learning es off-policy?
o: Porque no necesita un entorno y puede entrenarse con datos guardados en disco
o: Porque su objetivo usa el máximo sobre las acciones siguientes, no la acción que ejecuta la política que explora
o: Porque actualiza la tabla sin usar recompensas
a: 2
e: La actualización usa `max_{a'} Q(s', a')`, que corresponde a la política óptima y no a la que está actuando con exploración. Eso permite aprender de experiencias generadas por cualquier política, incluida una aleatoria o antigua. Se sigue necesitando interactuar con el entorno (real o simulado) para obtener transiciones.
:::

:::quiz
p: En el pasillo del ejemplo, Q(2, derecha) = −1,900 y Q(3, derecha) = −1,000 con γ = 0,9. ¿De dónde sale ese −1,9?
o: De la suma de todas las penalizaciones del episodio
o: De −1 (el coste de este paso) más 0,9 veces el valor del estado siguiente, que es −1
o: De la media de las recompensas obtenidas en el estado 2
a: 2
e: La actualización de Bellman encadena el coste inmediato con el valor descontado del estado siguiente: −1 + 0,9·(−1) = −1,9. Ese encadenamiento hacia atrás es lo que hace que el valor del estado 0 sea −4,095, la suma descontada de los cinco pasos hasta la meta.
:::

:::quiz
p: ¿Por qué el teorema del gradiente de política permite aprender sin conocer la derivada de la recompensa?
o: Porque la recompensa se estima con una red auxiliar que se entrena aparte
o: Porque el gradiente del retorno esperado se escribe como la esperanza del gradiente de log π ponderado por el valor de la acción, y ese valor se puede muestrear
o: Porque las políticas softmax tienen derivada constante
a: 2
e: El teorema intercambia la derivada y la esperanza: aparece el gradiente del logaritmo de la probabilidad de la acción elegida multiplicado por Q(s,a), que se estima con el retorno observado. La verificación numérica del ejemplo lo confirma: analítico 0,3525, numérico 0,3525 y REINFORCE 0,3539. La derivada de un softmax no es constante: depende de las probabilidades.
:::
