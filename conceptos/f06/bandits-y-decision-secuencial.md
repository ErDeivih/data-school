---
id: bandits-y-decision-secuencial
titulo: Bandits y decisión secuencial
fase: 6
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [valor-esperado, teorema-de-bayes, ab-testing]
tags: [decision, exploracion, secuencial, refuerzo]
resumen: Decidir y aprender a la vez: epsilon-greedy, UCB y Thompson sampling reparten las pruebas entre la opción que crees mejor y las que aún no conoces.
fuentes: ["Sutton y Barto (2018), 'Reinforcement Learning: An Introduction', cap. 2", "Auer, Cesa-Bianchi y Fischer (2002), 'Finite-time Analysis of the Multiarmed Bandit Problem'", "Chapelle y Li (2011), 'An Empirical Evaluation of Thompson Sampling'"]
---

## En una frase

Un bandit es el problema de decidir muchas veces seguidas cuando cada decisión te enseña algo pero
también te cuesta: hay que repartir el esfuerzo entre la opción que crees mejor y las que todavía no
conoces.

## La idea

Tienes cinco versiones del texto de un botón y 1.000 visitas al día. Si lo apuestas todo a la que
crees mejor, nunca sabrás si la cuarta era mejor todavía; si repartes las visitas a partes iguales,
durante semanas la mitad de tus visitantes verá una versión peor. Ese tira y afloja es **explorar
frente a explotar**, y su coste tiene nombre: **arrepentimiento** (regret), todo lo que dejarías de
ganar si conocieras de antemano la mejor opción.

Lo que hace especial a este problema es que decidir y aprender son el mismo acto. No hay una fase de
datos y otra de decisión, como en un [[ab-testing|test A/B]]: allí se fija un tamaño de muestra, se
aguanta la variante peor durante todo el experimento y se decide al final. Un bandit decide sobre la
marcha y va retirando lo que falla. A cambio paga dos precios que casi nadie menciona:

1. **El reparto queda desequilibrado.** La variante buena acumula miles de observaciones y la mala
   unas decenas, así que su [[intervalos-de-confianza|intervalo de confianza]] es enorme y no es una
   muestra aleatoria de nada: comparar las dos al final con un contraste clásico no vale.
2. **El contraste clásico deja de ser válido.** En un test A/B el reparto se decide antes de ver los
   resultados. Aquí se decide *con* los resultados ya vistos: los brazos con mejor suerte reciben
   más tráfico, y esa realimentación sesga cualquier comparación posterior.

Hay tres familias de solución:

- **Epsilon-greedy.** Con probabilidad `1 − ε` usa la opción de mejor media observada; con `ε`, una
  al azar. Con `ε` fijo nunca deja de pagar exploración: sigue gastando la misma fracción en brazos
  que ya sabe malos.
- **UCB (cota superior de confianza).** Suma a la media observada un bono que crece cuando el brazo
  se ha probado poco, y elige el índice más alto. Nadie decide «ahora toca explorar»: la exploración
  sale sola del bono del brazo olvidado.
- **Thompson sampling.** Mantiene una distribución sobre la media de cada brazo (la posterior de
  [[teorema-de-bayes|Bayes]]), sortea un valor de cada una y actúa según el sorteo. Un brazo con
  pocas tiradas tiene la distribución ancha y a veces gana; uno muy probado y bueno, casi siempre.
  Suele ser el que menos se arrepiente.

Un bandit así supone que la mejor opción es la misma para todo el mundo y para siempre. Cuando
depende del cliente (el titular que funciona a las nueve no funciona a las once de la noche), el
problema es un **bandit contextual**, ya de lleno en [[aprendizaje-por-refuerzo]].

## Definición formal

Con `K` brazos, cada uno con una recompensa esperada `μ_i` desconocida, y `T` rondas:

:::formula
R_T = T · μ* − Σ E[rₜ]        con  μ* = max μ_i   (la suma recorre las T rondas)
:::

- `μ_i` — recompensa esperada del brazo `i`: la probabilidad de éxito si la recompensa es binaria,
  o el ingreso medio por visita si es continua.
- `μ*` — la mejor de todas. Nadie la conoce; es una referencia para contar lo que pierdes.
- `r_t` — la recompensa que cobras en la ronda `t`.
- `R_T` — arrepentimiento acumulado tras `T` rondas, en la misma unidad que la recompensa: si la
  recompensa son euros, `R_T` son euros.

Y las dos reglas que más se usan:

:::formula
UCB1:  índice_i = μ̂_i + √(2 · ln t / n_i)
:::

:::formula
Thompson:  θ_i ~ Beta(α_i, β_i)   ·   elige el mayor θ_i   ·   α_i += r,  β_i += 1 − r
:::

- `μ̂_i` — media observada del brazo `i`: premios acumulados dividido entre tiradas.
- `n_i` — veces que has tirado del brazo `i`. Va en el denominador: cuanto más probado, menos bono.
- `t` — tiradas acumuladas en total. Va en el numerador: el bono crece con el tiempo, porque un
  brazo sin probar es cada vez más sospechoso.
- `θ_i` — una media sorteada de la creencia sobre el brazo `i`; se compara ella, no `μ̂_i`.
- `α_i`, `β_i` — aciertos y fallos del brazo `i`, más uno de prior. `Beta(1, 1)` es no saber nada:
  cualquier media entre 0 y 1 es igual de creíble. Su media es `α_i / (α_i + β_i)` y su anchura
  depende de la suma ([[distribuciones-continuas]]).

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `K` | Número de opciones entre las que elegir | brazos | Más brazos que explorar: el arrepentimiento crece, y con `ε` fijo lo hace de forma lineal |
| `T` | Número de decisiones que vas a tomar | rondas | El arrepentimiento total sube, pero el medio por ronda baja: explorar se amortiza |
| `μ_i` | Recompensa esperada real del brazo `i` | la de la recompensa | Si el mejor brazo destaca mucho sobre el segundo, cualquier política acierta antes |
| `μ*` | La mejor recompensa esperada | la de la recompensa | Es la referencia: cuanto más alta, más caro es cada tiro a un brazo peor |
| `R_T` | Arrepentimiento acumulado | la de la recompensa | Es lo que se minimiza; su forma dice si la política aprende o solo prueba |
| `ε` | Probabilidad de tirar al azar en epsilon-greedy | adimensional, de 0 a 1 | Más exploración y menos explotación: con `ε` fijo, arrepentimiento lineal |
| `μ̂_i` | Media observada del brazo `i` | la de la recompensa | Con muchas tiradas se acerca a `μ_i`; con pocas es casi ruido |
| `n_i` | Tiradas del brazo `i` | rondas | Baja el bono de UCB y estrecha la creencia de Thompson |
| `α_i`, `β_i` | Aciertos y fallos contados del brazo `i` | rondas | Su suma controla la anchura de la posterior, y esa anchura es la exploración |
:::

:::figura
fichero: bandits-y-decision-secuencial-arrepentimiento
pie: A la izquierda, la línea negra del codicioso se va a unos 140 premios perdidos en 2.000 tiradas y su recta no se dobla: se queda con el primer brazo que le sonríe y no vuelve a mirar. UCB y Thompson se aplanan a partir de la tirada 500, y Thompson es el que menos paga de los cuatro. El panel derecho explica ese aplanamiento: el bono de un brazo cae como 1/√n, y cuando baja del hueco real que lo separa del mejor (0,30 en este ejemplo, línea roja discontinua) ya no compensa volver a probarlo. Con pocas tiradas acumuladas el bono es más alto y se explora más; por eso la curva morada está por encima de la azul.
fuente: figuras/bandits-y-decision-secuencial-1.py
:::

## Ejemplo

Tres brazos con recompensa binaria y UCB1, con las primeras rondas seguidas a mano. Hay que tirar
una vez de cada brazo antes de poder calcular índices (con `n_i = 0` el bono se va a infinito):

| Tirada | `n` (A, B, C) | Medias | Bono | Índices | Elige |
| --- | --- | --- | --- | --- | --- |
| 1 a 3 | 1, 1, 1 | 1,00 · 0,00 · 1,00 | — | — | uno de cada |
| 4 | 1, 1, 1 | 1,00 · 0,00 · 1,00 | 1,482 · 1,482 · 1,482 | 2,482 · 1,482 · 2,482 | A (empate) |
| 5 | 2, 1, 1 | 1,00 · 0,00 · 1,00 | 1,177 · 1,665 · 1,665 | 2,177 · 1,665 · 2,665 | C |
| 6 | 2, 1, 2 | 1,00 · 0,00 · 0,50 | 1,269 · 1,794 · 1,269 | 2,269 · 1,794 · 1,769 | A |

Los bonos salen de `√(2 · ln t / n_i)`. En la tirada 4, `t = 3` y `n_i = 1`, así que
`√(2 · 1,099 / 1) = 1,482`. En la 6, `t = 5`, y el bono de A, ya probado dos veces, cae a
`√(2 · 1,609 / 2) = 1,269` mientras el de B, probado una sola vez, sube a `√(2 · 1,609 / 1) = 1,794`.

Fíjate en B: lleva un fallo, su media es 0,00, la peor de las tres, y aun así recibe su turno en la
tirada 5 porque tiene el bono más alto. Y en C: empezó con un acierto y una media de 1,00, pero al
fallar cae a 0,50 y pierde el liderato. Eso es UCB: el bono compra información sobre los brazos
dudosos y se apaga solo cuando ya no hacen falta. Con recompensas binarias, ocho tiradas bastan para
descartar un brazo, no para saber cuánto vale.

## Código

```python verificable
import numpy as np

# Cinco variantes con una tasa de exito real distinta. El algoritmo no la conoce.
medias = np.array([0.30, 0.60, 0.45, 0.35, 0.50])
T = 2000


def simula(explora, rng):
    n = np.zeros(medias.size)
    suma = np.zeros(medias.size)                    # premios acumulados por brazo
    perdido = 0.0
    for t in range(T):
        if n.min() == 0:
            i = int(np.argmin(n))                   # todos los brazos necesitan un tiro
        elif explora:
            i = int(np.argmax(suma / n + np.sqrt(2 * np.log(t) / n)))   # indice UCB1
        else:
            i = int(np.argmax(suma / n))            # codicioso: solo la media observada
        premio = 1.0 if rng.random() < medias[i] else 0.0
        n[i] += 1
        suma[i] += premio
        perdido += medias.max() - medias[i]         # lo que habrias ganado con el mejor
    return perdido, n


perdido_ucb, tiradas = simula(True, np.random.default_rng(7))
perdido_cod, _ = simula(False, np.random.default_rng(7))
print(f"UCB1      pierde {perdido_ucb:>4.0f} premios   tiradas {tiradas.astype(int)}")
# -> UCB1      pierde  126 premios   tiradas [ 102 1204  308   72  314]
print(f"codicioso pierde {perdido_cod:>4.0f} premios")   # -> codicioso pierde  201 premios
```

:::claves
- `np.argmax` devuelve la **posición** del máximo, no el valor. Por eso el brazo elegido se usa para indexar `n` y `suma`, y no como recompensa: confundir posición y valor es el error clásico con `argmax` y `argmin`.
- `suma / n` es una división de arrays elemento a elemento. Al principio vale `0/0`, que en NumPy es `nan` con un aviso, no un error: por eso el primer `if` fuerza una tirada por brazo antes de calcular nada. Sin ese arranque, `argmax` sobre un array con `nan` devuelve una posición arbitraria.
- `np.log(t)` con `t = 0` daría `-inf` y la raíz cuadrada, `nan`. El arranque evita también ese caso: cuando el bono se calcula, `t` vale como mínimo `K`.
- `rng.random() < medias[i]` compara un escalar con otro y devuelve un `bool` de Python, no un array: por eso `premio` se puede sumar directamente en `suma[i]`.
- El arrepentimiento se acumula con `medias.max() - medias[i]`, que es la diferencia con el mejor brazo *verdadero*. En un problema real no tienes `medias`, así que este número no se puede calcular: es una herramienta de laboratorio para comparar políticas, no una métrica de producción.
- Al cambiar `explora` por `False` solo se quita el término del bono; el resto del bucle es idéntico. Así se ve que la diferencia entre las dos políticas cabe en media línea de código.
:::

```python verificable
import numpy as np

# Tres brazos. Thompson no necesita arranque: empieza creyendo que todos valen 0,5.
medias = np.array([0.30, 0.60, 0.45])
rng = np.random.default_rng(7)
alfa, beta = np.ones(3), np.ones(3)     # prior Beta(1, 1): no sabe nada de ninguno
n = np.zeros(3)

for _ in range(2000):
    i = int(np.argmax(rng.beta(alfa, beta)))   # sortea una media de cada brazo y actua
    premio = 1.0 if rng.random() < medias[i] else 0.0
    alfa[i] += premio                          # acierto: la creencia sube
    beta[i] += 1.0 - premio                    # fallo: la creencia baja
    n[i] += 1

print("tiradas por brazo", n.astype(int))                    # -> [   8 1883  109]
print("media que cree   ", np.round(alfa / (alfa + beta), 2))  # -> [0.1  0.6  0.47]
print("confianza alfa+beta", (alfa + beta).astype(int))        # -> [  10 1885  111]
```

## Errores típicos

- **Dejar `ε` fijo y esperar que converja.** Con `ε = 0,1` y cinco brazos, un 2 % de las tiradas va
  para siempre a cada brazo malo: el arrepentimiento es una recta, no una curva que se aplana.
  Bájalo con el tiempo (`ε = 1/t`) o pasa a UCB o Thompson.
- **Comparar las medias de los brazos al final con un test clásico.** El reparto de tiradas depende
  de los resultados, así que el contraste no tiene la cobertura que promete. Si necesitas una
  comparación honesta, reserva un porcentaje fijo de tráfico aleatorio y mide solo ahí.
- **Confundir el objetivo.** Para *decidir* mientras aprendes, un bandit; para *estimar* el efecto de
  cada variante, un experimento aleatorio con tamaño calculado ([[ab-testing]], [[tamano-muestral]]).
  Un bandit para medir da estimaciones sesgadas, y un test A/B para decidir pierde dinero mientras
  dura.
- **Usar recompensa binaria cuando importa el ingreso.** Un clic que genera 3 € y otro que genera
  90 € no son el mismo éxito. Con recompensas continuas UCB se calcula igual, pero el prior de
  Thompson deja de ser Beta: para importes positivos se usa una Gamma.
- **Ignorar que el mundo cambia.** Si la mejor opción cambia con la temporada, un bandit que acumula
  todo el histórico se ancla en el pasado: usa una ventana deslizante o descuenta lo antiguo.

:::practica
enunciado: Un bandit con UCB1 lleva 100 tiradas repartidas así: A con 60 tiradas y media 0,42; B con 25 tiradas y media 0,35; C con 15 tiradas y media 0,30. Calcula los tres índices y decide de qué brazo tira ahora.
pista: El bono es √(2 · ln t / n_i) con t = 100, y ln 100 = 4,605.
solucion: 2 · ln 100 = 9,210. Bono de A = √(9,210 / 60) = 0,392, índice 0,812. Bono de B = √(9,210 / 25) = 0,607, índice 0,957. Bono de C = √(9,210 / 15) = 0,784, índice 1,084. Tira de C, aunque es el brazo con la peor media observada: 15 tiradas no bastan para descartarlo y su bono lo devuelve a la palestra.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el arrepentimiento de epsilon-greedy con ε fijo crece de forma lineal?
o: Porque el bono de cada brazo crece con el tiempo
o: Porque sigue gastando una fracción fija de las tiradas en brazos que ya sabe peores
o: Porque la media observada de un brazo nunca converge a su valor real
a: 2
e: Con ε fijo, cada ronda tiene una probabilidad constante de ir a un brazo malo, así que el error se acumula siempre al mismo ritmo: una recta. El bono que crece con el tiempo es de UCB; y las medias observadas sí convergen ([[ley-de-los-grandes-numeros]]), lo que pasa es que convergen a la vez que sigues pagando exploración.
:::

:::quiz
p: En UCB1, ¿de dónde sale la exploración si no hay ningún sorteo aleatorio?
o: De que el índice suma un bono que es grande cuando el brazo se ha probado poco
o: De que la media observada se calcula con una semilla aleatoria
o: De que el argmax elige otro brazo cuando hay empate
a: 1
e: El bono √(2 · ln t / n_i) hace que un brazo con pocas tiradas tenga un índice alto sin necesidad de suerte. La elección es determinista dado el histórico: la exploración está escrita en la fórmula, no en un dado.
:::

:::quiz
p: ¿Por qué Thompson sampling explora?
o: Porque suma un bono decreciente a la media observada
o: Porque sortea una media de la distribución de creencias de cada brazo, y esa distribución es ancha cuando hay pocas tiradas
o: Porque con probabilidad ε elige un brazo al azar
a: 2
e: Thompson es bayesiano: mantiene una posterior por brazo y decide con un sorteo de ella. Un brazo apenas probado tiene la posterior ancha y gana el sorteo de vez en cuando; según acumula datos, la posterior se estrecha y deja de tener oportunidades si es peor. El bono decreciente es UCB y el sorteo con probabilidad ε es epsilon-greedy.
:::

:::trampa
Es tentador lanzar un bandit, ver que gana la variante B y contar «B es un 12 % mejor». Ese número
no se sostiene: el tráfico se asignó en función de los resultados, así que B recibió más visitas
justo porque iba bien. Sin un grupo de control aleatorio no hay comparación válida. Si necesitas
las dos cosas, la solución estándar es reservar un 5-10 % fijo y aleatorio para medir.
:::
