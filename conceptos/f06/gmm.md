---
id: gmm
titulo: Mezclas gaussianas
fase: 6
nivel: avanzado
rutas: [ds, core]
prerequisitos: [distribuciones-continuas, maxima-verosimilitud, k-means]
tags: [clustering, probabilidad, em, no-supervisado]
resumen: Cada punto pertenece a cada grupo con una probabilidad, y el algoritmo EM alterna asignar esas probabilidades y reajustar las gaussianas de cada grupo.
fuentes: ["Dempster, Laird y Rubin (1977), 'Maximum Likelihood from Incomplete Data via the EM Algorithm'", "Bishop (2006), 'Pattern Recognition and Machine Learning', cap. 9"]
---

## En una frase

Una mezcla gaussiana supone que los datos salen de varias campanas superpuestas —primero se
elige grupo, luego se sortea el valor— y el algoritmo EM estima a la vez las campanas y la
probabilidad de que cada punto venga de cada una.

## La idea

Imagina una sala con dos grupos de gente hablando y un micrófono que graba el volumen total. No
sabes quién habla en cada momento, pero sí que hay dos maneras de hablar: una con voz grave y
otra aguda. Cada medición de volumen es una mezcla de ambas. Si supieras quién habló, calcular
la voz media de cada grupo sería trivial (una media); si supieras las voces medias, asignar cada
medición a un grupo también sería trivial (comparar). No sabes ninguna de las dos cosas, y ahí
está la gracia: puedes **alternar**. Supón unas voces, reparte las mediciones según lo bien que
encajen, recalcula las voces con ese reparto y repite. Eso es EM.

La diferencia con [[k-means]] es que aquí el reparto no es «este punto es del grupo 2», sino
«este punto es del grupo 2 con probabilidad 0,85 y del grupo 1 con 0,15». Esa **pertenencia
blanda** (en inglés, *soft assignment*) es lo que hace que un punto en la frontera no decida el
resultado: contribuye a las dos medias, ponderado. También es lo que permite que los grupos
tengan forma de elipse, cada uno con su propia orientación, en vez de la esfera implícita de
k-means.

El modelo es **generativo**: describe cómo se producirían los datos. Con probabilidad `π_k` se
elige la componente `k`, y después se sortea un punto de una normal con media `μ_k` y matriz de
covarianzas `Σ_k`. Ajustar el modelo es encontrar los `π`, los `μ` y las `Σ` que hacen los datos
observados más probables.

## Definición formal

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x` | Un punto de dimensión `d` | las de las variables | No es un mando. Al alejarse de todas las componentes, todas las densidades se hacen diminutas y la responsabilidad se reparte de forma cada vez más plana |
| `K` | Número de componentes de la mezcla | componentes (entero) | La log-verosimilitud no puede bajar al añadirlo, igual que la inercia no subía en K-means, así que no sirve para elegirlo. En la práctica puede quedarse igual de un `K` al siguiente si EM cae en un máximo local. Con `K` igual al número de puntos, cada punto tiene su propia campana y la varianza tiende a 0 |
| `π_k` | Peso de la componente `k` | probabilidad, entre 0 y 1 | Reparte la masa de probabilidad entre las componentes: los pesos suman 1. Si una componente toma un peso casi 1, las demás dejan de influir |
| `μ_k` | Vector de medias de la componente `k` | las de las variables | Es su centro. Al separarse dos medias, el valle entre ellas se hace más profundo y las responsabilidades se vuelven más tajantes, hasta parecerse a una etiqueta dura |
| `Σ_k` | Matriz de covarianzas de la componente `k` | unidades² | Decide la forma del grupo: esférica si es un número, alargada si es diagonal y girada si es completa. Al crecer la varianza, la campana se aplana y su responsabilidad se reparte entre más puntos |
| `N(x; μ, Σ)` | Densidad normal multivariante | 1 / (unidades^d) | Es la verosimilitud de cada componente. En dimensión alta es un número diminuto: se calcula en logaritmos para que no se desborde |
| `r_ik` | Responsabilidad: probabilidad de que el punto `i` venga de la componente `k` | probabilidad, entre 0 y 1 | Es el resultado blando del modelo y suma 1 en cada punto. Cuanto más cerca de 1, más se parece a una etiqueta dura; cerca de 0,5, el punto está en la frontera |
| `n` | Número de observaciones | observaciones | Es el divisor de los pesos y el que fija la penalización del BIC. Con pocas observaciones por componente, la matriz de covarianza completa no se puede estimar y conviene restringirla |
| `L` | Log-verosimilitud de los datos bajo la mezcla | log-probabilidad (sin unidades) | Nunca disminuye al aplicar un paso de EM: es lo que garantiza que el algoritmo converge. Solo sube hasta un máximo **local**, que depende del arranque |
| `q` | Número de parámetros libres del modelo | parámetros | Con covarianza completa y `d` dimensiones, `q = K·(d + d(d+1)/2 + 1) − 1`. Es lo que se penaliza en el BIC: al subir `q`, el criterio empeora |
| `BIC` | Criterio de selección: `−2·L + q·ln(n)` | adimensional | Con más componentes `L` sube y `q` también; el BIC tiene su mínimo en un `K` razonable, y ese mínimo es el que se elige. Menos es mejor, al contrario que la verosimilitud |
| `AIC` | Criterio alternativo: `−2·L + 2·q` | adimensional | Igual que el BIC pero con una penalización más floja, así que tiende a elegir más componentes. Con pocos datos, el BIC es más prudente |
:::

Con `K` componentes, `π_k` el peso de la componente `k` (cumplen `π_k ≥ 0` y `Σ_k π_k = 1`) y
`N(x; μ_k, Σ_k)` la densidad normal multivariante:

:::formula
p(x) = Σ_k π_k · N(x ; μ_k, Σ_k)
:::

- `x` — un punto de dimensión `d`.
- `π_k` — probabilidad *a priori* de que un punto salga de la componente `k`.
- `μ_k` — vector de medias de la componente `k`.
- `Σ_k` — matriz de covarianzas `d × d` de la componente `k`; su forma decide si el grupo es
  alargado, girado o esférico.

El algoritmo EM repite dos pasos hasta que la log-verosimilitud deja de mejorar:

:::formula
Paso E:  r_ik = π_k · N(x_i ; μ_k, Σ_k) / Σ_j π_j · N(x_i ; μ_j, Σ_j)
:::

:::formula
Paso M:  μ_k = Σ_i r_ik · x_i / Σ_i r_ik      π_k = (1/n) · Σ_i r_ik
:::

- `r_ik` — **responsabilidad**: probabilidad de que la observación `i` venga de la componente
  `k`. Para cada `i`, la suma sobre `k` vale 1.
- `n` — número de observaciones.
- La matriz de covarianzas se actualiza igual, ponderando cada punto por `r_ik`:
  `Σ_k = Σ_i r_ik (x_i − μ_k)(x_i − μ_k)ᵗ / Σ_i r_ik`.
- La log-verosimilitud que se vigila es `L = Σ_i log( Σ_k π_k N(x_i; μ_k, Σ_k) )`. **Nunca
  disminuye** al aplicar un paso: por eso EM converge, aunque solo a un máximo local.

Para elegir `K` no sirve la log-verosimilitud, que siempre sube al añadir componentes. Se usa un
criterio que penalice los parámetros de más:

:::formula
BIC = −2·L + q·ln(n)      AIC = −2·L + 2·q
:::

- `q` — número de parámetros libres. Con covarianza completa en `d` dimensiones,
  `q = K·(d + d(d+1)/2 + 1) − 1`; el `−1` es porque los pesos suman 1.
- La **estructura de covarianza** también es una decisión de modelo, y cambia `q`. *Completa*
  (`full`): cada grupo tiene su propia matriz, la más flexible y la que más parámetros gasta.
  *Compartida* (`tied`): todos los grupos usan la misma forma, solo cambian de centro.
  *Diagonal* (`diag`): las variables no se correlacionan dentro del grupo. *Esférica*
  (`spherical`): un único número por grupo, un radio. Con pocas observaciones por grupo,
  restringir compensa casi siempre.
- Cuanto menor sea el BIC, mejor. La penalización crece con `q`, así que el mínimo suele estar
  en un `K` razonable en lugar de en el mayor que pruebes.

## Ejemplo

Seis medidas en una dimensión: `−1, 0, 1, 4, 5, 6`. Se ven dos bloques, y arrancamos EM con
`μ₁ = 0`, `μ₂ = 4`, `σ₁² = σ₂² = 1` y pesos `π₁ = π₂ = 0,5`.

**Un paso E a mano, para el punto `x = 2,5`.** Las dos densidades comparten el factor
`1/√(2π)`, así que solo importa la exponencial:

- Componente 1: `exp(−(2,5 − 0)² / 2) = exp(−3,125) = 0,0439`.
- Componente 2: `exp(−(2,5 − 4)² / 2) = exp(−1,125) = 0,3247`.
- Responsabilidad de la componente 1: `0,0439 / (0,0439 + 0,3247) = 0,1192`, un 12 %.

El punto está mucho más cerca del centro 4, así que se lo queda la componente 2 con el 88 %…
pero no del todo: ese 12 % entra en la media de la componente 1 y la desplaza un poco hacia la
derecha.

**Tras 50 iteraciones**, los parámetros se estabilizan en:

- Medias: `μ₁ = 0,0000` y `μ₂ = 5,0000`.
- Varianzas: `σ₁² = σ₂² = 0,6667`.
- Pesos: `π₁ = π₂ = 0,5`.
- Log-verosimilitud: `L = −11,456`.

Compruébalo a mano: la varianza de `{−1, 0, 1}` es `2/3 = 0,6667`, y estos puntos quedan tan
lejos del centro 5 que su responsabilidad hacia la componente 2 es prácticamente cero. Cada
grupo se lleva tres puntos y el resultado coincide con lo que haría k-means, como era de
esperar cuando los grupos están tan separados. La diferencia aparece cuando los grupos se
solapan: ahí k-means corta por la mitad y la mezcla reparte.

## Código

:::figura
fichero: gmm-mezcla-y-pertenencia-blanda
pie: A la izquierda, lo que el modelo ajusta de verdad: dos campanas con el mismo peso y la misma forma, y la curva negra que es su suma. Las observaciones están abajo, sobre el eje, para no tapar las curvas: hay tres puntos bajo la primera campana, tres bajo la segunda y el valle entre ambas está prácticamente vacío, que es justo lo que hace que la mezcla funcione. En este dato la mezcla y K-means dan la misma partición, y eso es esperado cuando los grupos están separados. La diferencia está en el panel derecho, que es donde el ejemplo se rompe a mano: con los parámetros ya convergidos, el punto `x = 0,5` es 100 % de una componente, `x = 5,5` es 100 % de la otra y `x = 2,5` se reparte al 50 %. Ese punto medio no es un empate mal resuelto, es información: está exactamente en la frontera, donde el modelo no tiene motivo para preferir una campana, y una etiqueta dura lo escondería. Con los parámetros de arranque del ejemplo (centros en 0 y 4, varianza 1) ese mismo punto daba 12 % y 88 %, así que la responsabilidad también depende de dónde haya convergido EM.
fuente: figuras/gmm-1.py
:::

```python verificable
import numpy as np

datos = np.array([-1.0, 0.0, 1.0, 4.0, 5.0, 6.0])   # dos grupos evidentes
mu = np.array([0.0, 4.0])                            # arranque: dos centros distintos
var = np.array([1.0, 1.0])
pi = np.array([0.5, 0.5])

# Densidad normal escrita a mano (no hace falta scipy): una fila por componente y
# una columna por observacion. Ya lleva multiplicado el peso pi[k].
def densidades(datos, mu, var, pi):
    return np.array([pi[k] * np.exp(-(datos - mu[k]) ** 2 / (2 * var[k]))
                     / np.sqrt(2 * np.pi * var[k]) for k in range(2)])

for _ in range(50):
    # Paso E: responsabilidad de cada componente en cada punto.
    r = densidades(datos, mu, var, pi)
    # axis=0 suma sobre las componentes: en cada punto las responsabilidades suman 1.
    r = r / r.sum(axis=0)
    # Paso M: con esas responsabilidades, reestimar pesos, medias y varianzas.
    nk = r.sum(axis=1)                 # peso total de cada componente
    pi = nk / datos.size
    mu = (r * datos).sum(axis=1) / nk
    # mu[:, None] pasa mu de (2,) a (2,1) para poder restarlo a los 6 datos.
    # La division es entre nk (suma de responsabilidades), no entre el numero de puntos.
    var = (r * (datos - mu[:, None]) ** 2).sum(axis=1) / nk

ll = np.log(densidades(datos, mu, var, pi).sum(axis=0)).sum()
print("medias:", np.round(mu, 4).tolist())        # -> [0.0, 5.0]
print("varianzas:", np.round(var, 4).tolist())    # -> [0.6667, 0.6667]
print("pesos:", np.round(pi, 4).tolist())         # -> [0.5, 0.5]
print("log-verosimilitud:", round(float(ll), 3))  # -> -11.456
```

:::claves
- El bloque calcula EM **a mano** y el paso M tiene una trampa de normalización: la varianza se divide entre `nk`, que es la suma de responsabilidades de la componente (`r.sum(axis=1)`), no entre el número de puntos. Dividir entre el número de puntos deja la varianza cuatro veces más grande y el resultado no cuadra con el `0,6667` de la página: es un error que no lanza ninguna excepción y solo se detecta comparando con la cuenta a mano.
- Los parámetros se quedan con el valor del **último** paso del bucle, que es el convergido: `mu = [0, 5]`, `var = [2/3, 2/3]` y una log-verosimilitud de `-11,456`, que es exactamente la del texto de la página. Si quieres los de un paso intermedio hay que guardarlos dentro del bucle, porque `mu`, `var` y `pi` se sobreescriben en cada vuelta.
- El 12 % / 88 % que da la página para `x = 2,5` sale de los parámetros **de arranque** (`μ = 0` y `4`, `σ² = 1`), no de los convergidos: con los centros ya en 0 y 5 y la misma varianza, ese punto está justo en medio y sale 50 % / 50 %. Los dos números son correctos, pero miden momentos distintos del algoritmo, y confundirlos es el despiste más fácil de cometer al leer el ejemplo.
- `densidades(datos, mu, var, pi)` devuelve `pi[k] · exp(−(x−μ)²/(2σ²)) / sqrt(2πσ²)` para cada componente, o sea la densidad normal escrita a mano: no hace falta `scipy.stats`. Con 1.000 observaciones y varias componentes, multiplicar cientos de densidades diminutas se va por debajo de lo que representa un `float`: de ahí que en la práctica se sume en logaritmos. Aquí hay seis puntos y no se nota.
- `np.array([... for k in range(2)])` construye una matriz de `2 × n`: cada fila es una componente, cada columna una observación. Por eso `r.sum(axis=0)` suma sobre las componentes (da 1 en cada punto) y `r.sum(axis=1)` suma sobre los puntos (da el peso de cada componente). Intercambiar los ejes rompe EM sin que salte ninguna excepción.
- Un detalle que muerde en este bloque: la log-verosimilitud se calcula **después** del bucle, con los parámetros ya actualizados, así que el `ll` impreso corresponde a la última estimación y no a la del paso anterior. Si se metiera dentro del bucle como última línea, el número que se leería sería el de antes de la última actualización, sistemáticamente un poco peor.
- `fill_between(malla, campana_2, campana_1 + campana_2, ...)` rellena la banda **entre** dos curvas, no debajo de una: sirve para apilar las dos aportaciones y que se vea la suma, que es la densidad de la mezcla. Con `fill_between(malla, 0, campana)` se obtendría solo el área de una campana.
- La pertenencia blanda es un array que se puede usar como peso: `(r * datos).sum(axis=1)` es la media ponderada y el mismo `r` sirve para la varianza. Eso es todo el paso M, y es también la diferencia práctica con K-means, donde cada punto vale 1 en un grupo y 0 en los demás.
- `GaussianMixture` de scikit-learn acepta `covariance_type` (`"full"`, `"tied"`, `"diag"`, `"spherical"`) y con `n_components = K` deja los resultados en `weights_`, `means_` y `covariances_`. `predict_proba` da las responsabilidades y `predict` la etiqueta dura, que no es más que el `argmax` de la responsabilidad: se calcula la blanda y luego se tira la información que sobra.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
X = np.concatenate([rng.normal(0, 1, 70), rng.normal(5, 1, 70), rng.normal(10, 1, 70)])

def em_1d(x, k, iters=200):
    """Mezcla de k gaussianas en una dimension: devuelve la log-verosimilitud y los parametros."""
    # arranque: k centros repartidos uniformemente por el rango de los datos.
    mu = np.linspace(x.min(), x.max(), k)
    var = np.full(k, x.var())
    pi = np.full(k, 1 / k)
    for _ in range(iters):
        d = pi * np.exp(-(x[:, None] - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
        # keepdims=True conserva la forma (n,1) y la division se emite por filas.
        r = d / d.sum(axis=1, keepdims=True)
        nk = r.sum(axis=0)
        pi = nk / x.size
        mu = (r * x[:, None]).sum(axis=0) / nk
        var = (r * (x[:, None] - mu) ** 2).sum(axis=0) / nk
    return np.log(d.sum(axis=1)).sum(), mu, var, pi

for k in range(1, 6):
    ll, mu, var, pi = em_1d(X, k)
    q = 3 * k - 1                              # media, varianza y peso por grupo, menos 1
    print(f"k={k}  log-verosimilitud {ll:8.1f}  BIC {-2 * ll + q * np.log(X.size):8.1f}")
# -> k=1  log-verosimilitud   -594.9  BIC   1200.4
# -> k=2  log-verosimilitud   -556.9  BIC   1140.5
# -> k=3  log-verosimilitud   -517.0  BIC   1076.8
# -> k=4  log-verosimilitud   -517.0  BIC   1092.9
# -> k=5  log-verosimilitud   -515.3  BIC   1105.5

ll, mu, var, pi = em_1d(X, 3)
punto = np.array([2.5])
d = pi * np.exp(-(punto[:, None] - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
print("medias ordenadas:", np.round(np.sort(mu), 2).tolist())          # -> [0.11, 5.11, 9.9]
print("pertenencia ordenada del punto 2.5:", np.round(np.sort((d / d.sum()).ravel()), 3).tolist())
# -> [0.0, 0.41, 0.59]
```

El BIC baja hasta `k = 3` y vuelve a subir: la penalización `q·ln(n)` compensa la mejora de
log-verosimilitud a partir de ahí, que además se estanca (−517,0 con 3 y con 4). Y el punto
`2,5` no se asigna a un grupo: se reparte `0,59` y `0,41` entre los dos centros vecinos, que es
justo la información que k-means tira a la basura al decidir con un corte seco.

```python ilustrativo
# Con datos de verdad el flujo es: escalar, probar varias estructuras de covarianza
# y comparar por BIC. Aqui `datos` seria una matriz de n filas y d columnas ya cargada.
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

Z = StandardScaler().fit_transform(datos)      # el GMM tambien sufre con las escalas
for tipo in ("full", "tied", "diag", "spherical"):
    g = GaussianMixture(n_components=3, covariance_type=tipo, n_init=20, random_state=0).fit(Z)
    print(tipo, round(g.bic(Z), 1), round(g.aic(Z), 1))
```

## Errores típicos

- **Usarlo con grupos que no son elipses.** Una mezcla de gaussianas solo sabe de campanas
  giradas. Con dos lunas entrelazadas o un anillo, cada componente intentará tapar media figura
  y el resultado no significa nada. Si la forma es irregular, mira
  [[dbscan-y-hdbscan]] o [[clustering-jerarquico]].
- **No estandarizar.** La matriz de covarianzas se mide en las unidades de las variables; una
  columna en millones domina todas las direcciones y las demás componentes se ajustan a su
  ruido. Estandariza o, como mínimo, comprueba que las escalas son comparables.
- **Elegir `K` con la log-verosimilitud.** Añadir componentes siempre sube `L`: con `K = n` y
  una varianza diminuta por punto puedes acercarte al infinito. Usa BIC o AIC, o valida el
  número de grupos contra el uso que les vas a dar.
- **Ignorar los máximos locales y las componentes que colapsan.** EM solo garantiza que no
  empeora: con una mala inicialización se queda en una solución peor y estable, y si una
  gaussiana se centra en una sola observación su varianza tiende a cero, su densidad se dispara
  y la verosimilitud se va al infinito. Se arregla con `n_init` alto (20 o más, comparando las
  log-verosimilitudes y quedándote con la mejor) y con regularización de la covarianza
  (`reg_covar` en scikit-learn, típicamente `1e-6`).
- **Leer las responsabilidades como certezas.** Un `0,6` significa «bajo este modelo, con estos
  parámetros y esta forma de campana», no «hay un 60 % de probabilidad real de que este cliente
  sea de este tipo». Si el modelo está mal especificado, la probabilidad es tan falsa como el
  modelo.
- **Olvidar que la escala de la verosimilitud no es comparable entre transformaciones.** Cambiar
  unidades, quitar variables o imputar valores cambia `L` y el BIC, así que no compares BIC de
  modelos ajustados sobre conjuntos de columnas distintos.

:::practica
enunciado: Una mezcla gaussiana esférica en una dimensión, con n = 200, da estas log-verosimilitudes: K = 2 con L = −500, K = 3 con L = −470 y K = 4 con L = −468. Con q = 3K − 1 y BIC = −2L + q·ln(n), ¿qué K eliges?
pista: ln(200) = 5,3. Cada componente extra añade 3 parámetros, y el BIC los cobra a 5,3 puntos cada uno.
solucion: BIC(2) = 1000 + 5 · 5,3 = 1026,5. BIC(3) = 940 + 8 · 5,3 = 982,4. BIC(4) = 936 + 11 · 5,3 = 994,3. El mínimo está en K = 3: pasar a 4 mejora −2L en 4 puntos (de 940 a 936) pero sus 3 parámetros extra suman 15,9 de penalización, y el BIC sube 11,9. Eliges 3 componentes.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace exactamente el paso E de EM en una mezcla gaussiana?
o: Reestimar las medias y las covarianzas de cada componente
o: Calcular, para cada punto y cada componente, la probabilidad de que ese punto venga de esa componente
o: Elegir el número de componentes que mejor ajusta
a: 2
e: El paso E calcula las responsabilidades con las densidades actuales; el paso M reestima medias, covarianzas y pesos usando esas responsabilidades. Elegir el número de componentes no forma parte de EM: es una decisión previa que se resuelve con BIC, AIC o validación.
:::

:::quiz
p: ¿Por qué no se elige el número de componentes maximizando la log-verosimilitud?
o: Porque la log-verosimilitud no se puede calcular con más de tres componentes
o: Porque añadir componentes siempre la mejora, aunque sea a base de tapar ruido con campanas diminutas
o: Porque la log-verosimilitud solo vale para datos estandarizados
a: 2
e: Cada componente nueva añade parámetros y la verosimilitud no puede bajar: el modelo más complejo siempre encaja igual o mejor en la muestra. BIC y AIC restan una penalización proporcional al número de parámetros, y ese es el motivo de que puedan señalar un mínimo. La log-verosimilitud se calcula sin problema con cualquier número de componentes.
:::

:::quiz
p: Un punto tiene responsabilidades 0,6 y 0,4 sobre dos componentes. ¿Qué conclusión es correcta?
o: Que pertenece al primer grupo y el 0,4 es ruido de cálculo
o: Que el modelo lo sitúa en una zona ambigua, y ambas componentes se reparten su influencia en el paso M
o: Que hay un 60 % de probabilidad de que el punto pertenezca realmente al primer grupo, medida sobre la población
a: 2
e: La responsabilidad es una probabilidad a posteriori bajo el modelo ajustado, no una verdad sobre el mundo. Lo importante en la práctica es que ese punto entra ponderado en las dos componentes: no se descarta ni se asigna en bloque. Convertir esa cifra en una probabilidad poblacional exige creerse el modelo por completo.
:::

:::aviso
Las mezclas gaussianas escalan mal con la dimensión: con covarianza completa hay `d(d+1)/2`
parámetros por componente, y con `d = 50` son 1275 por grupo. Si tienes pocas observaciones por
grupo, restringe la covarianza (diagonal, esférica o compartida) o reduce la dimensión antes.
:::
