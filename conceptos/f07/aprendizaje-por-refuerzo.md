---
id: aprendizaje-por-refuerzo
titulo: Aprendizaje por refuerzo
fase: 7
nivel: experto
rutas: [ds]
prerequisitos: [paradigmas-de-aprendizaje, valor-esperado, probabilidad-condicional]
tags: [refuerzo, decision, recompensa, exploracion]
resumen: Un agente actua sobre un entorno, recibe recompensas y aprende una política que maximiza el retorno acumulado a base de probar y equivocarse.
fuentes: ["Sutton y Barto (2018), 'Reinforcement Learning: An Introduction'", "Bellman (1957), 'A Markovian Decision Process'"]
---

## En una frase

Un agente observa el estado del entorno, elige una acción, recibe una recompensa y un estado
nuevo, y su objetivo es aprender una política (qué hacer en cada estado) que maximice la
recompensa **acumulada a lo largo del tiempo**, no la de este paso.

## La idea

Piensa en enseñar a un perro con premios. No le das la respuesta correcta en cada situación: le
das un premio cuando hace algo bueno, y el perro tiene que averiguar **qué parte de lo que hizo**
provocó el premio. Si se sienta, te da la pata y luego ladra, y solo entonces llega el premio,
¿qué aprendió? Ese es el problema central del refuerzo: el **reparto de crédito** entre acciones
cuando la recompensa llega tarde.

En el aprendizaje supervisado tienes `(x, y)`: la respuesta correcta para cada entrada. Aquí no
hay respuesta correcta; hay una señal escalar que puede llegar cien pasos después de la decisión
que la causó, y puede llegar mezclada con el azar. Tres diferencias que cambian todo:

1. **No hay etiquetas, hay recompensa.** No sabes cuál era la acción óptima en ese estado, solo
   cuánto has ganado.
2. **Los datos los generas tú.** La distribución de lo que ves depende de la política que estás
   usando ahora mismo. Si tu política nunca va por una zona del entorno, nunca aprenderás nada
   de esa zona. En supervisado el conjunto de datos está fijo; aquí se mueve mientras aprendes.
3. **Los objetivos son a largo plazo.** Un agente que maximiza la recompensa inmediata se queda
   atrapado cobrando calderilla; a veces hay que sacrificar ahora para ganar después.

De ahí sale la tensión que define la disciplina: **explorar o explotar**. Exploras cuando pruebas
un restaurante nuevo y explotas cuando vuelves al que ya sabes que está bien. Si solo explotas,
te quedas con la primera opción aceptable que encontraste y nunca descubres la buena; si solo
exploras, nunca aprovechas lo que has aprendido. En el ejemplo del bandido con tres brazos, la
política que nunca explora se queda con una recompensa media de `0,289` cuando existe un brazo
que da `0,5`, y la que explora el 10 % de las veces llega a `0,486`.

El descuento `γ` es la otra pieza clave: convierte el futuro en algo comparable con el presente.
Con `γ = 0,9`, una recompensa a 10 pasos vale `0,9^10 ≈ 0,35` de lo que valdría ahora; con
`γ = 0,99`, vale `0,90`. Elegir `γ` es, en la práctica, elegir el **horizonte** del agente, y no
es un detalle: es la diferencia entre un agente que planifica y uno que reacciona.

:::figura
fichero: refuerzo-explorar-y-descontar
pie: A la izquierda, el premio medio por tirada de una política ε-greedy según cuánto explora, sobre el bandido de tres brazos de más abajo. La línea gris es elegir siempre al azar (0,40) y la roja punteada, el mejor brazo (0,50): con ε = 0 el agente se queda en 0,29, por debajo del azar, porque un empate inicial lo deja pegado al brazo malo para siempre. Basta explorar el 1 % para superar al azar, y el 10 % se acerca al techo. A la derecha, el otro parámetro que hay que elegir a mano: con γ = 0,9 una recompensa deja de contar a los siete pasos, y con γ = 0,99 el mismo premio aún vale 0,74 a treinta pasos. Ese es el horizonte del agente, y explica por qué subir γ hace el entrenamiento mucho más difícil: el retorno acumula más términos y tiene mucha más varianza.
fuente: figuras/aprendizaje-por-refuerzo-1.py
:::

## Definición formal

Un proceso de decisión de Markov (MDP) se define con la tupla `(S, A, P, R, γ)`:

- `S` — el conjunto de estados; `s_t` es el estado en el paso `t`.
- `A` — el conjunto de acciones disponibles; `a_t` es la acción elegida en `t`.
- `P(s' | s, a)` — la probabilidad de transición: dado el estado `s` y la acción `a`, qué estado
  viene después. Es la parte que no controlas.
- `R(s, a)` — la recompensa esperada al tomar `a` en `s` (a veces se escribe `R(s, a, s')`).
- `γ ∈ [0, 1)` — el factor de descuento: cuánto vale una recompensa futura respecto a una de ahora.

La **política** `π(a | s)` es la probabilidad de elegir la acción `a` en el estado `s`. Es lo
único que se aprende. La **trayectoria** es la secuencia `s_0, a_0, r_1, s_1, a_1, r_2, …`. El
**retorno** desde el paso `t` es la suma descontada de las recompensas que vienen después:

:::formula
G_t = R_{t+1} + γ·R_{t+2} + γ²·R_{t+3} + … = Σ_{k=0..∞} γ^k · R_{t+k+1}
:::

El valor de un estado y el valor de un par estado-acción son las esperanzas de ese retorno:

:::formula
V^π(s) = E_π[ G_t | S_t = s ]        Q^π(s, a) = E_π[ G_t | S_t = s , A_t = a ]
:::

- `V^π(s)` — cuánto se espera ganar empezando en `s` y siguiendo la política `π` después.
- `Q^π(s, a)` — lo mismo, pero forzando la acción `a` en el primer paso.
- `E_π[·]` — esperanza sobre las transiciones del entorno y el azar de la propia política.

Sustituyendo la definición de `G_t` se obtienen las **ecuaciones de Bellman**, que expresan el
valor de hoy en función del valor de mañana (la misma idea que la recursión de la
[[programacion-dinamica|programación dinámica]]):

:::formula
V^π(s) = Σ_a π(a|s) · [ R(s,a) + γ · Σ_{s'} P(s'|s,a) · V^π(s') ]
:::

La política óptima `π*` es la que maximiza `V^π` en todos los estados a la vez. Nótese la
dificultad: no se puede mejorar una acción sin evaluar las consecuencias, y las consecuencias
dependen de las acciones futuras, que a su vez dependen de la política. Las ecuaciones de
Bellman resuelven esa circularidad, y de ellas salen los dos grandes métodos:
[[q-learning-y-policy-gradient|Q-learning y el gradiente de política]].

Una política de exploración muy usada es la **ε-greedy**: con probabilidad `1 − ε` se elige la
acción de mayor valor estimado y con probabilidad `ε` una al azar. `ε = 0` es explotación pura.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `S` | El conjunto de estados del entorno | recuento (ninguna) | No se sube: es el problema que te dan. Lo que sí cambia con el número de estados es el coste de aprender: con miles de estados una tabla deja de caber y hace falta aproximar `V` con una función |
| `A` | El conjunto de acciones disponibles en cada estado | recuento (ninguna) | Más acciones dan más margen de mejora, pero el agente necesita más experiencia para descartar las malas: con 3 brazos y 2.000 tiradas basta, con 1.000 acciones no |
| `P(s' dado s, a)` | Probabilidad de acabar en `s'` al tomar `a` en `s` | probabilidad, entre 0 y 1 | Es la parte que no controlas. Si las transiciones son casi deterministas, el agente aprende rápido; cuanto más ruidosa es `P`, más experiencia hace falta para distinguir una acción buena de una con suerte |
| `R(s, a)` | Recompensa esperada al tomar `a` en `s` | las de la recompensa (puntos, euros) | Escalar todas las recompensas por una constante no cambia la política óptima; **sumar** una constante sí, porque altera el valor relativo del futuro. Si el agente cobra en cada paso, aprende a dar vueltas sin llegar a la meta |
| `γ` | Factor de descuento: cuánto vale una recompensa futura | adimensional, entre 0 y 1 | Al acercarse a 1 el horizonte se alarga: con `γ = 0,9` una recompensa a 10 pasos vale 0,35 y con `γ = 0,99` vale 0,90. Subirlo hace al agente previsor y también mucho más difícil de entrenar, porque el retorno tiene más varianza |
| `G_t` | Retorno: la suma descontada de las recompensas que vienen después | las de la recompensa | Es lo que se maximiza de verdad, no `R`. Al subir `γ`, el mismo premio futuro pesa más en `G_t`; y con recompensas grandes el retorno crece sin techo, así que conviene normalizarlo antes de meterlo en una red |
| `π(a dado s)` | La política: probabilidad de elegir `a` en `s` | probabilidad, entre 0 y 1 | Es lo único que se aprende. Una política con probabilidades repartidas explora por construcción; una política determinista solo explora si la modificas desde fuera (ε-greedy) |
| `V^π(s)` | Valor esperado de empezar en `s` siguiendo `π` | las de la recompensa acumulada | Es una estimación, no un dato. Cuanto más se visita un estado, menos se mueve su valor; los estados poco visitados tienen un `V` que es casi ruido y conviene no fiarse de él |
| `ε` | Fracción de acciones al azar en la política ε-greedy | probabilidad, entre 0 y 1 | Sube la exploración y con ella el descubrimiento de la acción buena, pero baja el rendimiento de la política que se está ejecutando. En el ejemplo, `ε = 0` se queda en 0,289 (peor que elegir al azar, 0,40) y `ε = 0,1` llega a 0,486. Se evalúa siempre con `ε = 0` |
:::

## Ejemplo

Bandido de tres brazos: cada brazo devuelve 1 con probabilidad `0,3`, `0,5` y `0,4`
respectivamente (el brazo 2 es el mejor). Dos mil tiradas, tres valores de `ε`:

```
epsilon      recompensa media   elige el mejor brazo
0.0                 0.289                 0.0%
0.01                0.417                59.0%
0.1                 0.486                89.9%
```

Con `ε = 0` el agente empata todos los valores al principio, empieza por el primer brazo y, como
cualquier recompensa que reciba lo confirma como «el mejor», ya no lo abandona nunca: cero por
ciento de elecciones al brazo bueno y `0,289` de recompensa media, que es exactamente la del
brazo malo. Es el fallo clásico de la explotación pura: **una casualidad se convierte en
certeza**. Con `ε = 0,1` explora lo suficiente para descubrir el brazo bueno y lo explota el
90 % de las veces.

Segundo ejemplo: el efecto del descuento sobre una secuencia de recompensas
`[0, 0, −1, 0, 10]` con `γ = 0,9`. El valor de cada instante mirando hacia delante:

```
t     r      retorno descontado G_t
0     0.0          5.7510
1     0.0          6.3900
2    -1.0          7.1000
3     0.0          9.0000
4    10.0         10.0000
```

Comprobación a mano de `G_0`: la penalización de `−1` en `t = 2` llega descontada dos pasos
(`−0,9² = −0,81`) y la recompensa de `10` en `t = 4`, cuatro pasos (`10 · 0,9⁴ = 6,561`). Suma:
`5,751`. Fíjate en lo que hace el descuento: la recompensa de 10 vale 6,561 al principio y 10 si
ya estás en `t = 4`. El agente prefiere llegar antes, aunque la recompensa sea la misma.

## Código

```python verificable
import numpy as np

medias = np.array([0.3, 0.5, 0.4])       # probabilidad real de exito de cada brazo
rng = np.random.default_rng(0)


def bandido(epsilon, pasos=2000):
    q = np.zeros(3)                      # valor estimado de cada brazo
    n = np.zeros(3)                      # veces que se ha tirado de cada brazo
    premio, optimo = 0.0, 0
    for _ in range(pasos):
        if rng.random() < epsilon:
            a = int(rng.integers(3))     # explorar
        else:
            a = int(np.argmax(q))        # explotar
        r = float(rng.random() < medias[a])
        n[a] += 1
        q[a] += (r - q[a]) / n[a]        # media incremental: no hace falta guardar todo
        premio += r
        optimo += int(a == 1)            # el brazo 1 es el mejor
    return premio / pasos, optimo / pasos


for eps in (0.0, 0.01, 0.1):
    media, opt = bandido(eps)
    print(f"epsilon={eps:<5} recompensa media={media:.3f}  elige el mejor brazo={opt:.1%}")
# -> epsilon=0.0   recompensa media=0.289  elige el mejor brazo=0.0%
# -> epsilon=0.01  recompensa media=0.417  elige el mejor brazo=59.0%
# -> epsilon=0.1   recompensa media=0.486  elige el mejor brazo=89.9%
```

:::claves
- `rng` se define **una sola vez, fuera** de la función. Eso hace que las tres llamadas a `bandido` no sean independientes: la segunda empieza donde acabó el generador de la primera. Si mueves `rng = np.random.default_rng(0)` dentro de la función, las tres pruebas arrancan de la misma semilla y los números cambian.
- `q[a] += (r - q[a]) / n[a]` es la media incremental y da exactamente el mismo resultado que guardar todas las recompensas y promediarlas, con memoria constante en vez de una lista que crece. Es la misma cuenta que hace NumPy al acumular una media, pero a mano porque el brazo elegido cambia en cada paso.
- `n[a] += 1` va **antes** de usar `n[a]`: si lo pusieras después, el primer premio se dividiría entre 0 y saldría `nan` (o `inf` con NumPy, porque en `float64` no lanza excepción).
- `int(np.argmax(q))` devuelve un entero de Python a partir del índice de NumPy, y con empate `argmax` se queda con el **primero**: eso es lo que decide el destino con `ε = 0`. `q = np.zeros(3)` arranca con los tres valores empatados a cero, así que el agente empieza por el brazo 0.
- `float(rng.random() < medias[a])` convierte un booleano en 0,0 o 1,0. La comparación es contra una probabilidad, no contra un umbral fijo: así el brazo 2 (0,5) da premio la mitad de las veces y el 0 (0,3), menos.
- `optimo += int(a == 1)` cuenta cuántas veces se elige el brazo bueno, que es información distinta de la recompensa: con `ε = 0` la recompensa media es 0,289 y el porcentaje de acierto 0,0 %, y las dos cifras hay que mirarlas juntas.
:::

```python verificable
import numpy as np

recompensas = np.array([0.0, 0.0, -1.0, 0.0, 10.0])
gamma = 0.9

# El retorno se calcula de atras hacia delante: G_t = r_t + gamma * G_{t+1}.
G = np.zeros_like(recompensas)
acumulado = 0.0
for t in range(len(recompensas) - 1, -1, -1):
    acumulado = recompensas[t] + gamma * acumulado
    G[t] = acumulado

for t in range(len(recompensas)):
    print(f"t={t}  r={recompensas[t]:>5}  retorno descontado G_t={G[t]:.4f}")
# -> t=0  r=  0.0  retorno descontado G_t=5.7510
# -> t=1  r=  0.0  retorno descontado G_t=6.3900
# -> t=2  r= -1.0  retorno descontado G_t=7.1000
# -> t=3  r=  0.0  retorno descontado G_t=9.0000
# -> t=4  r= 10.0  retorno descontado G_t=10.0000

print(f"G_0 a mano: -0.9^2 + 10 * 0.9^4 = {-0.9 ** 2 + 10 * 0.9 ** 4:.4f}")
# -> G_0 a mano: -0.9^2 + 10 * 0.9^4 = 5.7510
```

:::claves
- `np.zeros_like(recompensas)` crea un array de **la misma forma y el mismo tipo** que `recompensas`, es decir `float64`. Si lo hubieras escrito como `G = []` y hubieras hecho `G[t] = acumulado`, fallaría: una lista no admite asignar por índice una posición que todavía no existe.
- `range(len(recompensas) - 1, -1, -1)` es la forma de recorrer hacia atrás. El segundo argumento es el límite **excluido**, así que hay que llegar a `-1` para que el último índice sea 0. Es el error clásico de este bucle.
- `acumulado = recompensas[t] + gamma * acumulado` usa el valor del paso siguiente que se calculó en la vuelta anterior, no una variable nueva: por eso basta un acumulador y no hace falta guardar `G` entero para calcularlo. Y `gamma` multiplica al acumulado **ya descontado**, de modo que el descuento se aplica tantas veces como pasos falten.
- El retorno de este ejemplo es un número, no un gradiente: en un algoritmo de policy gradient se guarda como constante (`detach()` en PyTorch) y no se deriva respecto de los parámetros de la política.
- `{-0.9 ** 2 + 10 * 0.9 ** 4:.4f}` funciona porque `**` se evalúa antes que el menos unario, así que `-0.9 ** 2` es `-(0.9²)` = −0,81 y no `(-0.9)²` = +0,81. Es la misma precedencia que en matemáticas, y escribirlo al revés daría un número con el signo cambiado.
:::

```python ilustrativo
# El bucle agente-entorno tiene siempre la misma forma. Necesita instalar gymnasium
# y un entorno, por eso no se ejecuta aqui.
import gymnasium as gym

entorno = gym.make("CartPole-v1")
estado, _ = entorno.reset(seed=0)
retorno = 0.0

for paso in range(500):
    accion = politica(estado)              # aqui va lo que se aprende
    estado, recompensa, truncado, terminado, _ = entorno.step(accion)
    retorno += recompensa
    if terminado or truncado:
        break

entorno.close()
print("retorno del episodio:", retorno)    # se compara entre episodios, no dentro de uno
```

## Errores típicos

- **Evaluar con la política que explora.** El retorno que mides con `ε = 0,1` incluye un 10 % de
  acciones al azar, así que subestima el rendimiento del agente. Se evalúa con la política
  greedy (`ε = 0`) y, si el entorno es estocástico, sobre varios episodios con semillas
  distintas. Confundir ambas cosas lleva a elegir `ε` por el número equivocado.
- **Confundir recompensa con retorno.** Optimizar la recompensa inmediata no es lo mismo que
  maximizar `G_t`: en el ejemplo, la recompensa de 10 vale `6,561` cuando estás en `t = 0` y
  `10` cuando estás en `t = 4`. Un agente que solo mira el premio inmediato no aprende a
  anticiparse ni a pagar un coste pequeño hoy por un beneficio mayor mañana.
- **Diseñar mal la función de recompensa.** El agente optimiza exactamente lo que le pagas, no
  lo que querías. Si premias «tiempo en pie» en un robot, aprenderá a tambalearse sin avanzar;
  si premias la velocidad de un coche simulado, aprenderá a girar en círculos. La recompensa se
  revisa antes de entrenar y se comprueba el comportamiento con ejemplos concretos.
- **Sacar conclusiones de una sola semilla.** El resultado de un entrenamiento por refuerzo
  depende muchísimo de la semilla: en el bandido de arriba, `ε = 0` acaba en el brazo malo por
  un empate inicial, no por una propiedad profunda del algoritmo. Se repite con varias semillas
  y se comparan medianas y dispersión, nunca una curva suelta.
- **Ignorar el coste de obtener experiencia.** En muchos problemas reales cada interacción
  cuesta dinero o tiempo (un ensayo clínico, una compra, una máquina). Los algoritmos que
  aprenden en el entorno real sin simulación previa son peligrosos: primero se entrena en un
  simulador y se mide la brecha entre simulación y realidad.
- **Olvidar que los datos envejecen.** Si mejoras la política, los datos que recogiste con la
  política anterior describen un comportamiento que ya no sigues. Reutilizarlos sin más
  introduce un sesgo; los métodos que lo hacen (off-policy) necesitan correcciones de
  importancia o un control explícito de cuánto se desvía la política.

:::practica
enunciado: Con tres brazos, los valores estimados son Q(1) = 0,40, Q(2) = 0,45 y Q(3) = 0,30, y usas una política ε-greedy con ε = 0,1. Calcula la probabilidad de elegir cada brazo y la recompensa esperada del siguiente paso.
pista: La acción de más valor se elige con probabilidad 1 − ε; el presupuesto de exploración restante se reparte a partes iguales entre las demás.
solucion: La avaricia elige el brazo 2: P(2) = 0,9 + 0,1/3 = 0,9333 y P(1) = P(3) = 0,1/3 = 0,0333. La recompensa esperada es 0,9333 · 0,45 + 0,0333 · 0,40 + 0,0333 · 0,30 = 0,42 + 0,0133 + 0,01 = 0,4433. Conclusión: explorar el 10 % cuesta 0,0067 por paso frente a 0,45, el precio de no quedarse atrapado con la primera opción aceptable.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia esencial hay entre el aprendizaje supervisado y el aprendizaje por refuerzo?
o: En refuerzo no hay función de pérdida ni descenso de gradiente
o: En refuerzo no hay etiquetas correctas: solo una recompensa escalar, a menudo retrasada, y la distribución de datos depende de la política del agente
o: En refuerzo el entorno es siempre determinista, mientras que en supervisado hay ruido
a: 2
e: La clave es la ausencia de respuesta correcta por ejemplo y el hecho de que los datos los genera la propia política, lo que los mueve mientras se aprende. Sí hay pérdidas y gradientes (por ejemplo en el gradiente de política) y los entornos pueden ser estocásticos.
:::

:::quiz
p: Con γ = 0,9, ¿cuánto vale aproximadamente una recompensa de 10 que llega 4 pasos después?
o: 10, porque el descuento solo se aplica a las recompensas negativas
o: 6,561, porque se multiplica por 0,9⁴
o: 0, porque el descuento hace que el futuro no cuente
a: 2
e: Cada paso multiplica por γ: 0,9⁴ = 0,6561 y 10 · 0,6561 = 6,561, que es justo lo que aparece en G_0 del ejemplo. Cuanto menor es γ, más corto es el horizonte efectivo del agente.
:::

:::quiz
p: En el bandido con ε = 0, el agente acaba eligiendo el peor brazo el 100 % de las veces. ¿Por qué?
o: Porque el brazo bueno solo se puede encontrar con gradiente de política
o: Porque con todos los valores empatados a cero elige el primero, y la primera recompensa que recibe lo confirma en esa elección sin llegar a probar los demás
o: Porque los brazos con mayor probabilidad de premio tienen menor varianza y el agente los evita
a: 2
e: Es el fallo de la explotación pura: sin exploración no hay información nueva y un empate inicial se rompe por el orden, no por el valor. Con ε = 0,01 o 0,1 el agente prueba los otros brazos y la recompensa media sube a 0,417 y 0,486.
:::
