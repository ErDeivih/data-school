---
id: hmm-regimenes
titulo: Cadenas de Markov ocultas
fase: 5
nivel: experto
rutas: [quant, ds]
prerequisitos: [estacionariedad, maxima-verosimilitud, garch-volatilidad]
tags: [regimenes, series-temporales, estados-latentes]
resumen: Un modelo de estados ocultos que cambian con una cadena de Markov: estima en qué régimen estas, cuanto dura y cuando es probable que cambie.
fuentes: ["Hamilton (1989), 'A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle'", "Rabiner (1989), 'A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition'", "Tsay (2010), 'Analysis of Financial Time Series', cap. 4"]
---

## En una frase

Un modelo de Markov oculto supone que la serie la genera un número pequeño de estados que no ves
—tranquilo, agitado, alcista, bajista—, que cada estado produce valores con su propia
distribución, y que el estado de hoy depende solo del de ayer; con eso calcula la probabilidad de
estar en cada estado en cada instante.

## La idea

Casi todos los modelos de series temporales suponen que las reglas del juego son las mismas
durante todo el periodo. Eso es cómodo y, en mercados, falso: hay tramos en los que la volatilidad
es del 8 % anual y tramos en los que es del 40 %, hay mercados alcistas que duran años y desplomes
que duran semanas. Ajustar un único modelo a todo el histórico mezcla regímenes y produce un
promedio que no describe ninguno.

La solución más antigua y más usada para esto es suponer que existe un **estado latente** —no
observado— que cambia de vez en cuando, y que lo que observamos son datos generados por ese estado.
Un modelo de Markov oculto (HMM, *hidden Markov model*) tiene dos piezas:

1. **La cadena de estados.** El estado `S_t` toma uno de `K` valores (dos o tres en la práctica) y
   evoluciona de forma markoviana: la probabilidad de pasar a cada estado depende **solo** del
   estado actual, no de toda la historia. Esa matriz de transición es la que codifica la
   persistencia: si la probabilidad de seguir en el estado 1 es 0,95, los regímenes duran.
2. **Las emisiones.** En cada estado, el valor observado sale de una distribución propia. Lo
   habitual en finanzas es una normal con media y varianza distintas por estado: un régimen de
   calma con media cercana a cero y volatilidad baja, y un régimen de tensión con más volatilidad
   y, muchas veces, media negativa. Aquí está la conexión con [[garch-volatilidad|GARCH]]: los dos
   modelos describen la volatilidad cambiante, pero el HMM la hace saltar entre niveles discretos
   y el GARCH la mueve de forma continua.

Del modelo salen tres cosas muy útiles:

- Una **probabilidad** de estar en cada estado en cada instante, no una etiqueta rígida. Eso
  permite decir «hay un 70 % de probabilidad de que estemos en el régimen agitado», que es mucho
  más honesto que «estamos en crisis».
- La **duración esperada** de cada régimen, que se calcula con una sola división:
  `1/(1 − p_kk)`. Si la probabilidad de seguir en el estado es 0,95, dura 20 periodos de media.
- La **probabilidad de cambio**, que es lo que se usa para reaccionar antes de que el cambio sea
  obvio.

El precio que se paga es que el estado no se observa: hay que estimarlo, y eso se hace con el
algoritmo de **Baum-Welch**, que es una versión del algoritmo EM. Su funcionamiento es fácil de
describir: se parte de unos parámetros, se calcula la probabilidad de cada estado en cada instante
(paso E, que usa las recursiones *forward* y *backward*) y con esas probabilidades se reestiman
medias, varianzas y transiciones (paso M, con fórmulas cerradas). Se repite hasta que la
verosimilitud deja de subir. Tres propiedades que hay que tener presentes:

1. **La verosimilitud nunca baja** en cada iteración. Eso es garantía de que el algoritmo no se
   descontrola, no de que llegue al máximo global.
2. **Puede quedarse en un máximo local**, y no es raro. Dos inicializaciones distintas pueden
   acabar en soluciones distintas, con ajustes parecidos. Por eso se reinicia muchas veces desde
   puntos distintos y se conserva el mejor resultado.
3. **Las etiquetas son arbitrarias.** Si intercambias el nombre de los estados, la verosimilitud no
   cambia ni un decimal. El «estado 0» no significa nada por sí mismo: hay que identificar cada
   régimen por sus parámetros (el de varianza baja, el de media negativa), no por su índice.

Para etiquetar cada instante hay dos salidas distintas y confundirlas es una fuente clásica de
autoengaño. La probabilidad **filtrada** en `t` usa solo la información hasta `t`: es la que
podrías haber calculado en tiempo real. La probabilidad **suavizada** usa toda la muestra, incluido
el futuro: es mejor estimación y es inutilizable como señal de trading, porque mira hacia delante.
El camino más probable (algoritmo de Viterbi) es una tercera salida, que da una secuencia de
etiquetas coherente pero oculta que también es una estimación retrospectiva.

:::figura
fichero: hmm-regimenes-probabilidad-suavizada
pie: Arriba, una serie generada por dos regímenes, tranquilo en azul y agitado en rojo, con la sombra marcando cuál estaba activo: eso es lo que el modelo no ve. Abajo, la probabilidad suavizada de estar en el agitado, que es la única salida del modelo. Nótese que no es una etiqueta rígida sino una probabilidad, y que acierta el 95 % de los días: en los días 147 y 148 baja al 50 %, justo cuando el régimen vuelve al tranquilo, porque los datos de ese tramo se parecen a los dos estados. La incertidumbre es del problema, no del algoritmo.
fuente: figuras/hmm-regimenes-1.py
:::

## Definición formal

Sea `y_1, …, y_T` la serie observada y `S_t ∈ {1, …, K}` el estado latente.

**Cadena de estados.** La transición entre estados es

:::formula
p_ij = P(S_t = j | S_{t−1} = i)   ·   Σ_{j=1}^{K} p_ij = 1   ·   π_j = P(S_1 = j)
:::

- `p_ij` — probabilidad de pasar del estado `i` al `j` en un paso. Forman la matriz `P`, cuyas
  filas suman 1.
- `π_j` — la distribución inicial; muchas veces se toma la estacionaria, que es el vector `π` que
  cumple `π = π·P`, o simplemente `1/K`.
- **Duración esperada** del estado `k`: `1 / (1 − p_kk)` periodos. Es la media de una geométrica
  con parámetro `1 − p_kk`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `S_t` | El estado latente en el instante `t`: no se observa | una etiqueta de `1` a `K` | — |
| `K` | El número de estados | entero, 2 o 3 en la práctica | Más estados ajustan mejor dentro de la muestra y casi siempre peor fuera. Con `K = T` la verosimilitud es infinita y el modelo no dice nada: decide `K` con BIC o con validación |
| `y_t` | El valor observado en `t`, generado por el estado | las de la serie (retornos, %) | — |
| `p_ij` | Probabilidad de pasar del estado `i` al `j` en un paso | adimensional, entre 0 y 1 | Si suben las de la diagonal, los regímenes duran más y el modelo cambia menos de opinión; si suben las de fuera, el estado salta cada dos por tres y deja de ser un régimen |
| `p_kk` | La probabilidad de **seguir** en el estado `k` | adimensional, entre 0 y 1 | Alarga la duración esperada `1 / (1 − p_kk)`: con 0,95 son 20 periodos; con 0,99, cien. Es el parámetro que decide si el modelo ve regímenes o solo ruido |
| `π_j` | La probabilidad de que el primer instante esté en el estado `j` | adimensional, las `K` suman 1 | Reparte el tiempo entre estados en la primera observación; en series largas deja de notarse, en series cortas manda |
| `μ_k` | La media de los valores que produce el estado `k` | las de la serie | Separa los regímenes por nivel: un estado con media negativa será el de las caídas. Con dos medias casi iguales el modelo solo está distinguiendo volatilidad |
| `σ²_k` | La varianza de ese estado | las de la serie, al cuadrado | Es lo que de verdad distingue los regímenes en finanzas: calma frente a tensión. Es la conexión con GARCH, que mueve esa volatilidad de forma continua en vez de a saltos |
| `f_k(y)` | La densidad de observar `y` si el estado es `k` | 1 / (unidades de la serie) | Es la pieza que traduce «cuánto se parece este dato a cada régimen»; si la distribución está mal elegida (normal con colas gordas), un dato extremo se lleva toda la probabilidad de un estado imposible |
| `α_t(k)` | Peso no normalizado del estado `k` en `t` en la recursión forward | adimensional, se normaliza en cada paso | No se interpreta: se normaliza para que no desborde el ordenador. Lo que se dibuja es `γ` |
| `γ_t(k)` | La probabilidad **suavizada** de estar en el estado `k` en `t` con toda la muestra | adimensional, entre 0 y 1 | Es la salida que se dibuja, y también la que engaña: usa datos posteriores a `t`, así que en un backtest parece adivinar el cambio antes de que ocurra |
| `ξ_t(i, j)` | Probabilidad conjunta de estar en `i` en `t−1` y en `j` en `t`, con toda la muestra | adimensional | Es lo que se acumula en el paso M para reestimar la matriz de transición |
| `1 / (1 − p_kk)` | Duración esperada del estado `k` | periodos | Cuanto más cerca de 1 está `p_kk`, más larga: 10 periodos con 0,9, veinte con 0,95. Si el modelo da duraciones de uno o dos periodos, lo que ha encontrado no son regímenes |
:::

**Emisiones.** En el caso gaussiano, `y_t` condicionado al estado es normal:

:::formula
y_t | S_t = k  ~  N(μ_k, σ²_k)   ·   f_k(y) = (1/√(2πσ²_k))·exp(−(y − μ_k)² / (2σ²_k))
:::

- `μ_k` — la media de los valores que produce el estado `k` (el retorno medio del régimen).
- `σ²_k` — la varianza de ese estado; en finanzas es la diferencia más informativa entre regímenes.
- `f_k(y)` — la densidad de probabilidad de observar `y` si el estado es `k`. Es la pieza que
  traduce «cuánto se parece este dato a cada régimen».
- El número de parámetros libres es `K(K − 1)` transiciones, más `2K` medias y varianzas.

**Recursión forward (filtrado).** La probabilidad conjunta de estar en el estado `k` y haber visto
los datos hasta `t` se actualiza así:

:::formula
α_t(k) ∝ f_k(y_t) · Σ_{i=1}^{K} α_{t−1}(i)·p_ik   ·   γ_t(k) = P(S_t = k | y_1…y_T)
:::

- `α_t(k)` — peso no normalizado de cada estado en `t`; se normaliza en cada paso para evitar
  desbordamientos numéricos.
- `γ_t(k)` — la probabilidad **suavizada** de estar en el estado `k` en `t` con toda la muestra;
  es la salida que se dibuja.
- La recursión *backward* es la simétrica hacia atrás; su producto con la forward, normalizado, da
  `γ_t(k)`.
- La verosimilitud total de la serie se obtiene acumulando los factores de normalización de la
  recursión forward: `log P(y_1…y_T) = Σ_t log c_t`.

**Paso M de Baum-Welch.** Con `ξ_t(i, j) = P(S_{t−1} = i, S_t = j | y_1…y_T)`:

:::formula
p̂_ij = Σ_t ξ_t(i,j) / Σ_t γ_{t−1}(i)   ·   μ̂_k = Σ_t γ_t(k)·y_t / Σ_t γ_t(k)   ·   σ̂²_k = Σ_t γ_t(k)·(y_t − μ̂_k)² / Σ_t γ_t(k)
:::

Es decir: cada estado se reestima como una media ponderada por la probabilidad de pertenecer a él,
y cada transición como la frecuencia con la que se ha recorrido esa arista, también ponderada. De
ahí que el algoritmo se lea como «estimar las etiquetas y, con ellas, reestimar los parámetros».

## Ejemplo

**Duración y proporción de cada régimen, a mano.** Con `P = [[0,9; 0,1], [0,2; 0,8]]`:

- Duración esperada del estado 1: `1/(1 − 0,9) = 10` periodos.
- Duración esperada del estado 2: `1/(1 − 0,8) = 5` periodos.
- Proporción del tiempo en cada estado (distribución estacionaria): `π₁ = (1 − p₂₂) / ((1 − p₁₁) +
  (1 − p₂₂)) = 0,2 / 0,3 = 0,667` y `π₂ = 0,333`. El estado tranquilo ocupa dos tercios del
  tiempo.

**Un paso de filtrado, a mano.** Supón que tras ayer la probabilidad era `(0,6; 0,4)`. Con la
matriz anterior, la predicción de hoy antes de ver el dato es:

```
(0,6 · 0,9 + 0,4 · 0,2 ;  0,6 · 0,1 + 0,4 · 0,8) = (0,62 ; 0,38)
```

Ahora observas un retorno del 2 % (`y = 2`). Las densidades son las de una normal de media 0 y
varianza 1 para el estado tranquilo, y de media 0 y varianza 4 para el agitado:
`f₁(2) = 0,05399` y `f₂(2) = 0,12098`. Multiplicando y normalizando:

```
(0,62 · 0,05399 ; 0,38 · 0,12098) = (0,03347 ; 0,04597)   →   (0,421 ; 0,579)
```

Aunque la probabilidad previa favorecía al estado tranquilo (62 %), un dato de dos desviaciones
típicas del régimen tranquilo lo da la vuelta: la probabilidad del agitado pasa del 38 % al 58 %.
Así funciona el filtrado: la transición aporta la inercia y la emisión aporta la evidencia.

**Ajuste completo con datos simulados.** Con 600 observaciones generadas por dos estados gaussianos
—el tranquilo con media 0 y varianza 1, el agitado con media 2 y varianza 9— y una matriz de
transición real `[[0,95; 0,05], [0,10; 0,90]]`, el algoritmo de Baum-Welch arrancado desde una
separación por cuantiles recupera:

- Medias estimadas `0,00` y `1,98` (las reales, 0 y 2).
- Varianzas `0,95` y `9,63` (las reales, 1 y 9).
- Transiciones `[[0,951; 0,049], [0,124; 0,876]]`, con duraciones esperadas de 20,4 y 8,1 periodos.
- Acierto al etiquetar cada instante con el estado más probable: **93,3 %**.

Merece la pena fijarse en el detalle de que el acierto no es del 100 % aunque el modelo esté bien
estimado: cuando un dato está en la zona donde las dos distribuciones se solapan, ningún método
puede saber de qué estado viene. La incertidumbre es del problema, no del algoritmo.

**El etiquetado es arbitrario.** Si tomas cualquier conjunto de parámetros, calculas la
verosimilitud de una serie corta y luego repites el cálculo con los estados intercambiados (medias,
varianzas y matriz de transición con las filas y columnas permutadas), el resultado es idéntico:
`−14,0878` en los dos casos. Ese es el problema de intercambio de etiquetas (*label switching*), y
es la razón de que nunca debas referirte a los regímenes por su número.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(7)
n = 600
P = np.array([[0.95, 0.05], [0.10, 0.90]])        # matriz de transicion real
s = np.zeros(n, int)
for t in range(1, n):
    s[t] = rng.choice(2, p=P[s[t - 1]])
y = rng.normal(np.where(s == 0, 0.0, 2.0), np.where(s == 0, 1.0, 3.0))

def gauss(y, mu, var):
    return np.exp(-0.5 * (y - mu) ** 2 / var) / np.sqrt(2 * np.pi * var)

# Arranque por cuantiles: separa los periodos tranquilos de los agitados
mu = np.quantile(y, [0.25, 0.8])
var = np.array([y.var() / 4, y.var() * 2])
A = np.array([[0.9, 0.1], [0.1, 0.9]])
for _ in range(30):                                # Baum-Welch: con 30 iteraciones de EM basta
    B = np.column_stack([gauss(y, mu[k], var[k]) for k in range(2)])
    al = np.zeros((n, 2)); al[0] = 0.5 * B[0]
    for t in range(1, n):                          # paso forward (filtrado)
        al[t] = (al[t - 1] @ A) * B[t]
        al[t] /= al[t].sum()
    be = np.ones((n, 2))
    for t in range(n - 2, -1, -1):                 # paso backward
        be[t] = A @ (B[t + 1] * be[t + 1])
        be[t] /= be[t].sum()
    g = al * be; g /= g.sum(1, keepdims=True)      # gamma: probabilidad suavizada
    xi = np.array([al[t][:, None] * A * (B[t + 1] * be[t + 1])[None, :] for t in range(n - 1)])
    xi /= xi.sum((1, 2), keepdims=True)
    A = xi.sum(0) / g[:-1].sum(0)[:, None]         # paso M: transiciones, medias y varianzas
    mu = (g * y[:, None]).sum(0) / g.sum(0)
    var = (g * (y[:, None] - mu) ** 2).sum(0) / g.sum(0)

print("medias     ", np.round(mu, 2), " (simuladas: 0.00 y 2.00)")     # -> [-0.    1.98]
print("varianzas  ", np.round(var, 2), " (simuladas: 1.00 y 9.00)")    # -> [0.95 9.63]
print("transicion ", np.round(A, 3).tolist())                          # -> [[0.951, 0.049], [0.124, 0.876]]
print("filas suman 1:", np.allclose(A.sum(1), 1))                      # -> True
print("duracion esperada", np.round(1 / (1 - np.diag(A)), 1))          # -> [20.4  8.1]
print("acuerdo con el estado simulado", round((g.argmax(1) == s).mean(), 3))   # -> 0.933
```

:::claves
- `P[s[t - 1]]` no es un índice raro: `P` es una matriz de 2×2 y `P[i]` devuelve su **fila** `i`, que es un array de dos probabilidades que suman 1. Eso es exactamente lo que espera `rng.choice(2, p=...)`. Si las filas no sumaran 1, NumPy lanza un `ValueError`; si las columnas sumaran 1 y las filas no, el resultado sería otro modelo.
- `rng.choice(2, p=...)` devuelve un `np.int64`, y `s = np.zeros(n, int)` fija el tipo del array para que todo encaje. Comparar después `g.argmax(1) == s` funciona porque ambos son arrays de enteros de la misma forma `(n,)`.
- `al[t] = (al[t - 1] @ A) * B[t]` mezcla un producto matriz-vector (`@`) con un producto elemento a elemento (`*`). Son cosas distintas: `@` combina los estados anteriores con la matriz de transición y `*` multiplica ese resultado por la verosimilitud del dato de hoy. Cambiar `@` por `*` no da error de tipos, da otro modelo.
- `al[t] /= al[t].sum()` **modifica el array en su sitio**, no crea uno nuevo. Es lo que evita que las probabilidades se vayan a cero tras unos cientos de pasos (desbordamiento inferior). El precio es que `al` deja de ser una probabilidad conjunta y pasa a ser condicional: por eso la verosimilitud total habría que recuperarla sumando los logaritmos de los factores de normalización, no mirando `al`.
- `be = np.ones((n, 2))` arranca el paso backward con unos. La última fila de `be` no se toca: el algoritmo empieza en `n - 2` y va hacia atrás. Si el bucle empezara en `n - 1`, leería `B[n]`, que no existe.
- `g = al * be; g /= g.sum(1, keepdims=True)`: `sum(1)` suma **por filas** (cada instante, sus dos estados) y `keepdims=True` conserva la forma `(n, 1)`, que es lo que hace que la división se reparta bien entre los dos estados. Sin `keepdims`, NumPy emitiría un aviso y difundiría la forma de otra manera.
- `xi = np.array([al[t][:, None] * A * (B[t + 1] * be[t + 1])[None, :] for t in range(n - 1)])` construye un array 3D con una lista por comprensión. `al[t][:, None]` convierte el vector de dos elementos en una columna de 2×1 y `[None, :]` convierte el otro en una fila de 1×2: así el producto exterior da la matriz 2×2 de cada instante. Es el truco de *broadcasting* que sustituye a dos bucles anidados.
- `A = xi.sum(0) / g[:-1].sum(0)[:, None]` reestima la transición sumando todos los instantes. El `sum(0)` suma sobre el **primer eje** (el tiempo) y `[:, None]` vuelve a poner el resultado en columna para que la división sea por filas. `g[:-1]` deja fuera el último instante porque no tiene transición hacia delante: si usaras `g` entero, las filas de `A` no sumarían 1.
- `g.argmax(1)` devuelve, para cada instante, el **índice** del estado más probable; `(g.argmax(1) == s).mean()` compara con el estado simulado y promedia los `True` como si fueran unos. El 0,933 no es un porcentaje redondeado: es la proporción exacta de aciertos.
- Nada de esto identifica los estados. `mu`, `var` y `A` podrían venir con los estados intercambiados y la verosimilitud sería idéntica: hay que mirar los valores para saber cuál es el tranquilo ([[maxima-verosimilitud|máxima verosimilitud]]).
:::

```python verificable
import numpy as np

P = np.array([[0.90, 0.10], [0.20, 0.80]])
print("duracion esperada", np.round(1 / (1 - np.diag(P)), 1), "periodos")   # -> [10.  5.]
val, vec = np.linalg.eig(P.T)                   # vector propio izquierdo de valor propio 1
pi = np.real(vec[:, np.argmin(np.abs(val - 1))])
print("proporcion del tiempo en cada regimen", np.round(pi / pi.sum(), 3))  # -> [0.667 0.333]

y = np.array([0.1, -0.3, 2.4, 1.9, 0.2, 3.1, -0.4])
def logver(mu, var, A):
    """Log-verosimilitud de la serie integrando todos los caminos de estados."""
    def f(v, m, s2):
        return np.exp(-0.5 * (v - m) ** 2 / s2) / np.sqrt(2 * np.pi * s2)
    al = 0.5 * np.array([f(y[0], mu[k], var[k]) for k in range(2)])
    for t in range(1, y.size):
        al = (al @ A) * np.array([f(y[t], mu[k], var[k]) for k in range(2)])
    return np.log(al.sum())

mu, var = np.array([0.0, 2.5]), np.array([1.0, 1.0])
print("log-verosimilitud original            %.4f" % logver(mu, var, P))          # -> -14.0878
print("log-verosimilitud con etiquetas al reves %.4f" % logver(mu[::-1], var[::-1], P[::-1, ::-1]))
# -> tambien -14.0878: los nombres de los estados son arbitrarios
```

```python ilustrativo
# statsmodels trae una version con regresores y varianza conmutada (Hamilton 1989).
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import statsmodels.api as sm

mod = sm.tsa.MarkovRegression(retornos, k_regimes=2, switching_variance=True)
res = mod.fit(search_reps=20)          # varios arranques: la verosimilitud es multimodal
print(res.params)
print(res.smoothed_marginal_probabilities.tail())
print(res.expected_durations)          # duracion esperada de cada regimen
```

## Errores típicos

- **Identificar los regímenes por el número de estado.** Las etiquetas son arbitrarias: cambiar el
  nombre de los estados deja la verosimilitud idéntica (`−14,0878` en los dos casos del bloque de
  arriba). Identifícalos siempre por sus parámetros (el de volatilidad alta, el de media negativa)
  y comprueba que el orden no cambia entre ejecuciones.
- **Confundir la probabilidad suavizada con la filtrada y usarla como señal.** La suavizada usa
  datos posteriores al instante que etiqueta, así que en un backtest parece adivinar los cambios
  justo el día antes. En producción solo tienes la filtrada, que reacciona con retraso. Usar la
  suavizada para decidir es [[sesgo-de-mirar-al-futuro|mirar al futuro]].
- **Quedarse con el primer ajuste.** La verosimilitud de un HMM tiene varios máximos locales. Si
  arrancas una sola vez, la solución depende del punto de partida. Reinicia desde varias
  inicializaciones (por ejemplo, separando por cuantiles) y quédate con la de mayor verosimilitud.
- **Elegir el número de estados por la verosimilitud.** Más estados ajustan siempre mejor dentro
  de la muestra: con `K = T` la verosimilitud es infinita y el modelo no dice nada. Decide `K` con
  BIC o con validación fuera de muestra, y sobre todo pregúntate si los regímenes tienen una
  interpretación económica. Dos o tres suelen ser suficientes.
- **Creer que los regímenes son la verdad del mercado.** Son una construcción del modelo: con otra
  `K` obtienes otra historia igual de convincente. Un HMM es una forma de resumir la persistencia
  de la volatilidad y de la media, no un detector de la naturaleza oculta del mercado.
- **Suponer normalidad en las emisiones.** Los retornos tienen colas gordas y asimetría
  ([[distribuciones-en-datos-reales|distribuciones en datos reales]]): una emisión gaussiana hace
  que los días extremos se lleven la probabilidad de un régimen «imposible» y el etiquetado se
  vuelva inestable. Usa una t de Student o una mezcla, o al menos comprueba cuántos datos caen en
  cada estado.

:::practica
enunciado: Con la matriz de transición P = [[0,8; 0,2], [0,3; 0,7]], ayer la probabilidad filtrada era (0,7; 0,3). Hoy observas un dato cuya densidad es 0,30 en el régimen tranquilo y 0,10 en el agitado. Calcula la probabilidad filtrada de hoy y la proporción del tiempo que pasa en cada régimen.
pista: Primero la transición (probabilidad previa), después multiplicar por la densidad de cada estado y normalizar para que las dos sumen 1.
solucion: Predicción: (0,7·0,8 + 0,3·0,3; 0,7·0,2 + 0,3·0,7) = (0,65; 0,35). Con el dato: (0,65·0,30; 0,35·0,10) = (0,195; 0,035), que suman 0,230; normalizando queda (0,848; 0,152). El dato empuja hacia el régimen tranquilo. Proporción del tiempo: π₁ = (1−0,7)/((1−0,8)+(1−0,7)) = 0,3/0,5 = 0,6 y π₂ = 0,4.
:::

## Comprueba que lo sabes

:::quiz
p: En un HMM de dos estados, la probabilidad de permanecer en el estado tranquilo es 0,96 y la de permanecer en el agitado es 0,85. ¿Cuánto dura cada régimen de media?
o: 0,96 y 0,85 periodos, porque son probabilidades
o: 25 periodos el tranquilo y 6,7 el agitado
o: No se puede saber sin la distribución inicial
a: 2
e: La duración esperada de un estado es 1/(1 - p_kk): 1/0,04 = 25 periodos para el tranquilo y 1/0,15 = 6,7 para el agitado. La distribución inicial solo reparte el tiempo entre estados, no cambia cuánto dura cada uno.
:::

:::quiz
p: Estimas la probabilidad de estar en el régimen agitado con suavizado y descubres que sube del 20 % al 80 % justo tres días antes de cada caída del mercado. ¿Qué haces?
o: Usarla como señal de venta: funciona en el backtest
o: Desconfiar: la probabilidad suavizada usa datos futuros, así que esa anticipación es un artefacto
o: Repetir el experimento con más regímenes hasta que la señal sea perfecta
a: 2
e: El suavizado usa toda la muestra para etiquetar cada instante, incluidos los datos posteriores, de modo que el cambio de régimen se detecta «antes» de forma artificial. Para decidir en tiempo real solo vale la probabilidad filtrada, que en el mejor de los casos confirma el cambio uno o dos días después.
:::

:::quiz
p: Ajustas un HMM con K = 2 y otro con K = 6 sobre los mismos datos. El de seis estados tiene una verosimilitud muy superior. ¿Qué modelo eliges?
o: El de seis, porque ajusta mejor
o: El de dos, salvo que el de seis se justifique con BIC, con una interpretación clara y con mejor comportamiento fuera de muestra
o: Ninguno: la verosimilitud de un HMM nunca es comparable entre modelos
a: 2
e: Añadir estados siempre sube la verosimilitud dentro de la muestra, porque el modelo gana grados de libertad para describir el ruido. La comparación honesta usa un criterio penalizado como el BIC y, sobre todo, la capacidad de generalizar con datos que el modelo no ha visto.
:::

:::trampa
Un HMM detecta regímenes con un retraso estructural: cuando el modelo tiene suficiente evidencia
para superar el 50 % de probabilidad, el movimiento ya ha ocurrido. Sirve para estimar riesgo y
para confirmar contexto, no para adivinar el cambio. Si tu backtest muestra que detecta el régimen
antes de que empiece, busca en el código: casi siempre estás usando la probabilidad suavizada o el
camino de Viterbi, y los dos miran al futuro.
:::
