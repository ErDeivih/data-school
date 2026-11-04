---
id: interpretabilidad-shap
titulo: Interpretabilidad y SHAP
fase: 6
nivel: avanzado
rutas: [ds]
prerequisitos: [importancia-de-variables, arboles-de-decision, gradient-boosting]
tags: [interpretabilidad, shapley, explicabilidad]
resumen: Que parte de una predicción concreta se atribuye a cada variable: valores de Shapley, curvas PDP e ICE y los límites de todo ello.
fuentes: ["Lundberg y Lee (2017), 'A Unified Approach to Interpreting Model Predictions'", "Molnar (2022), 'Interpretable Machine Learning'"]
---

## En una frase

SHAP reparte la predicción de un caso concreto entre sus variables, igual que se reparte un
premio entre las personas que cooperaron para ganarlo: cada variable recibe la parte que
aportó de media, y el reparto no dice qué variable *causa* el resultado, solo cómo se reparte
lo que el modelo ya había decidido.

## La idea

Cuatro personas construyen un producto y ganan un premio. ¿Cómo se reparte? A partes iguales
sería injusto si una no hizo nada. Por orden de llegada tampoco: depende del orden. La
respuesta de la teoría de juegos cooperativos (Shapley, 1953) es promediar: imagina todos los
órdenes posibles de llegada y, en cada uno, mira cuánto añade cada persona al equipo que ya
estaba. La media de esas aportaciones marginales es su parte.

Traducido a un modelo predictivo, el premio es la predicción de una fila menos la predicción
media, y los jugadores son las variables. En lugar de «cuánto añade esta persona al equipo»,
la pregunta es «cuánto cambia la predicción si conozco esta variable, dado lo que ya sabía de
las demás». El resultado son tantos números por variable como filas tengas: una explicación
**local**, fila a fila.

Eso es lo que SHAP añade a [[importancia-de-variables|la importancia de variables]] clásica.
La importancia por impureza o por permutación da un único número por variable para todo el
conjunto; SHAP da un número por variable y por observación. Con eso puedes ver que una
variable empuja hacia arriba en unos casos y hacia abajo en otros, en lugar de quedarte con un
promedio que no describe a nadie.

Las curvas **PDP** e **ICE** responden a una pregunta parecida pero no igual. La PDP fuerza
una variable a un valor para todas las filas y promedia las predicciones: «en promedio, ¿qué
pasa si esta variable vale t?». La ICE dibuja esa misma curva para una sola fila. Cuando las
curvas ICE se cruzan, la PDP puede salir plana mientras dentro hay dos efectos opuestos: una
variable que sube la predicción en unos casos y la baja en otros. Un promedio plano no
significa «esta variable no importa», significa «importa de dos maneras distintas y las he
mezclado».

## Definición formal

Sea `F` el conjunto de las `M` variables del modelo, `f` la función que predice y
`x` la fila que quieres explicar. Para un subconjunto `S` de variables define el valor de la
coalición:

:::formula
v(S) = E[ f(X) | X_S = x_S ]
:::

- `M` — número de variables del modelo.
- `S` — subconjunto de variables cuyos valores sí se conocen.
- `v(S)` — predicción esperada cuando las variables de `S` toman los valores de `x` y el
  resto se promedia sobre su distribución.
- `E[·]` — esperanza matemática; en la práctica se estima promediando sobre filas de datos.

El valor de Shapley de la variable `i` es su aportación marginal media sobre todos los
subconjuntos posibles:

:::formula
φ_i = Σ_{S ⊆ F∖{i}} ( |S|! · (M − |S| − 1)! / M! ) · ( v(S ∪ {i}) − v(S) )
:::

- `φ_i` — atribución de la variable `i` para esa fila concreta.
- `|S|` — tamaño del subconjunto `S`, es decir, cuántas variables se conocen ya.
- El factor `|S|! · (M − |S| − 1)! / M!` es un peso: cuántos órdenes de llegada corresponden a
  ese subconjunto.

Propiedades que se cumplen por construcción y conviene saber leer:

1. **Eficiencia:** `Σ_i φ_i = f(x) − E[f(X)]`. La suma de atribuciones es exactamente la
   diferencia entre la predicción de esa fila y la media. Ni más ni menos.
2. **Variable inútil:** si una variable no cambia nunca la predicción, su `φ_i` es 0.
3. **Simetría:** dos variables intercambiables reciben lo mismo.

Para un modelo de árboles, el algoritmo **TreeSHAP** calcula `φ_i` de forma exacta en tiempo
polinómico. Para cualquier otro modelo, **KernelSHAP** lo estima por muestreo: es una
aproximación con ruido, y con pocas muestras dos ejecuciones dan números distintos.

La PDP y la ICE se definen así, con `j` la variable que se mueve, `t` el valor que se le
impone y `X_{−j}` el resto de variables:

:::formula
PDP_j(t) = E_{X_{−j}}[ f(t, X_{−j}) ]      ICE_j^(i)(t) = f(t, x_{−j}^(i))
:::

- `t` — valor impuesto a la variable `j`.
- `X_{−j}` — todas las variables menos la `j`, promediadas sobre los datos.
- `x_{−j}^(i)` — los valores reales de la fila `i` en el resto de variables.
- La PDP es la media de las ICE sobre todas las filas.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `M` | Numero de variables del modelo | variables | El calculo exacto se dispara: hay `2^M` coaliciones, y por eso hacen falta TreeSHAP o muestreo |
| `S` | Subconjunto de variables cuyo valor ya se conoce | variables | Cada variable nueva que entra reduce la incertidumbre y cambia el valor de la coalición |
| `φ_i` | Atribución de la variable `i` en esa fila | unidades de la predicción | Empuja la predicción de esa fila hacia arriba (o hacia abajo, si es negativa); la suma de todas es fija |
| `E[f(X)]` | Predicción media del modelo sobre los datos | unidades de la predicción | Sube el liston: las atribuciones se reparten la distancia entre la fila y esa media, no la predicción entera |
| `t` | Valor impuesto a la variable en la PDP | unidades de esa variable | Recorre la rejilla elegida; fuera del rango observado la respuesta es una extrapolación del modelo |
| `n` de muestras | Numero de filas usadas para estimar `v(S)` con KernelSHAP | filas | Menos ruido entre ejecuciones, a cambio de mas tiempo; TreeSHAP no depende de esto |
:::

## Ejemplo

Un modelo de tres variables `a`, `b` y `c` con estas predicciones por coalición (los valores
`v(S)` ya están promediados sobre los datos):

```
v(vacío) = 0,0    v(a) = 1,0    v(b) = 2,0    v(c) = 3,0
v(a,b) = 4,0      v(a,c) = 5,5  v(b,c) = 6,0  v(a,b,c) = 8,0
```

Aplicando la fórmula salen las atribuciones: `φ_a = 1,75`, `φ_b = 2,50`, `φ_c = 3,75`. La
suma es 8,0, exactamente `v(a,b,c) − v(vacío)`. La variable más determinante es `c`, la que
menos `a`.

Fíjate en un detalle que se escapa a simple vista: en solitario, `a` aporta 1,0
(`v(a) − v(vacío)`), pero su atribución es 1,75. La diferencia viene de que `a` aporta más
cuando `b` y `c` ya están dentro: `v(a,b,c) − v(b,c) = 2,0`. SHAP promedia esas dos situaciones
en vez de quedarse con una. Eso es exactamente lo que hace la fórmula con los pesos.

Para la PDP, con las predicciones medias al fijar la primera variable en una rejilla:

```
x1 = 0,00  ->  PDP = 1,436
x1 = 0,50  ->  PDP = 2,593
x1 = 1,00  ->  PDP = 3,688
```

El efecto medio crece 2,25 puntos de 0 a 1. La curva ICE de una observación concreta
(la número 0) va de 0,395 a 2,645, un salto parecido. Si otra observación tuviera un salto muy
distinto o de signo contrario, la media estaría escondiendo una interacción.

:::figura
fichero: shap-reparto-y-pdp-ice
pie: A la izquierda, la predicción de una fila repartida entre sus tres variables: cada barra arranca donde acabó la anterior y la barra gris de abajo mide el total, así que se ve de un vistazo que la suma de las atribuciones es exactamente la predicción menos la media (la propiedad de eficiencia). Fíjate en que la variable a aporta más dentro del reparto que en solitario: eso es lo que promedian los pesos de la fórmula. A la derecha, la trampa de la PDP: cada línea morada es la curva ICE de una observación y la roja es su promedio. Las individuales se mueven con fuerza y en direcciones opuestas, y la media sale casi plana. Una PDP plana con ICE inclinadas no significa «esta variable no importa», significa «importa de dos maneras y las he promediado».
fuente: figuras/interpretabilidad-shap-1.py
:::

## Código

```python verificable
import itertools
from math import factorial
import numpy as np

# Juego cooperativo de 3 variables: v(S) es lo que predice el modelo usando solo S.
# Con 3 variables hay 8 coaliciones, asi que el valor de Shapley se calcula exacto.
v = {(): 0.0, ("a",): 1.0, ("b",): 2.0, ("c",): 3.0,
     ("a", "b"): 4.0, ("a", "c"): 5.5, ("b", "c"): 6.0, ("a", "b", "c"): 8.0}
todos = ("a", "b", "c")

def shapley(j, v, todos):
    total = 0.0
    for r in range(len(todos)):
        for S in itertools.combinations([k for k in todos if k != j], r):
            peso = factorial(r) * factorial(len(todos) - r - 1) / factorial(len(todos))
            total += peso * (v[tuple(sorted(S + (j,)))] - v[tuple(sorted(S))])
    return total

phi = {j: shapley(j, v, todos) for j in todos}
for j in todos:
    print(f"phi_{j} = {phi[j]:+.3f}")
print("suma =", round(sum(phi.values()), 3), " v(todos) =", v[todos])
# -> phi_a = +1.750
# -> phi_b = +2.500
# -> phi_c = +3.750
# -> suma = 8.0  v(todos) = 8.0
```

:::claves
- La clave del diccionario `v` es una **tupla** `("a", "b")` y no una lista: las listas no se
  pueden usar como clave porque no son hashables. Y `tuple(sorted(...))` esta ahi porque
  `("b", "a")` y `("a", "b")` serian claves distintas apuntando a la misma coalición.
- `v[()]` funciona: la tupla vacia es una clave valida y representa la coalición sin ninguna
  variable, que es `E[f(X)]`. Si te olvidas de esa entrada, el calculo lanza `KeyError` en la
  primera vuelta del bucle.
- `itertools.combinations(..., r)` con `r = 0` devuelve **una** tupla vacia, no nada. Ese
  detalle es lo que hace que la variable entre sola en el equipo vacio y su aportación marginal
  sea `v({i}) − v(vacio)`: la primera de las cuatro que se promedian.
- `factorial(r) * factorial(M - r - 1) / factorial(M)` es una división de enteros en Python 3:
  da un `float`. Si esto fuera Python 2, la división sería entera y todos los pesos saldrian 0 o
  1: los valores de Shapley serian basura sin ningun aviso.
- `phi` es un diccionario, pero el bucle imprime recorriendo `todos`, no `phi`: el orden de las
  líneas (`a`, `b`, `c`) es siempre el mismo y puedes comparar dos salidas línea a línea.
- Cambia `v[("a", "b")]` de 4,0 a 3,0: `φ_a` y `φ_b` bajan 1/6 cada uno y `φ_c` sube 1/3, porque
  esa coalición también aparece restando en el término `v(a,b,c) − v(a,b)`. La suma sigue
  siendo 8,0: la eficiencia es una propiedad de la formula, no del reparto concreto.
:::

```python verificable
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(0)
X = rng.uniform(0, 1, size=(300, 2))
y = 3 * X[:, 0] + 2 * (X[:, 1] > 0.5)

arbol = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)

# PDP de x1: prediccion media al fijar x1 = t y dejar x2 tal como esta en la muestra.
for t in (0.0, 0.25, 0.5, 0.75, 1.0):
    Xm = X.copy()        # copia, no vista: si no, machacarias la columna de X
    Xm[:, 0] = t
    print(f"x1={t:.2f}  PDP={arbol.predict(Xm).mean():.3f}")

# ICE del individuo 0: su curva sola, de x1=0 a x1=1.
Xm = X.copy()
Xm[:, 0] = 0.0
# El extremo izquierdo de SU curva es su prediccion con x1 forzado a 0, no su x1 real.
izq = arbol.predict(Xm)[0]
Xm[:, 0] = 1.0
print(f"ICE obs 0: {izq:.3f} -> {arbol.predict(Xm)[0]:.3f}")
# -> x1=0.00  PDP=1.436
# -> x1=0.25  PDP=1.436
# -> x1=0.50  PDP=2.593
# -> x1=0.75  PDP=2.934
# -> x1=1.00  PDP=3.688
# -> ICE obs 0: 0.395 -> 2.645
```

```python ilustrativo
import shap
from sklearn.ensemble import GradientBoostingRegressor

# X_entrenamiento y X_test vienen de tu propio pipeline, ya sin fuga de datos.
modelo = GradientBoostingRegressor(random_state=0).fit(X_entrenamiento, y_entrenamiento)

# TreeSHAP: exacto para arboles y rapido aunque haya muchas filas.
explicador = shap.TreeExplainer(modelo)
valores = explicador.shap_values(X_test)     # una fila por observacion, una columna por variable

# Importancia global = media del valor absoluto de las atribuciones.
shap.summary_plot(valores, X_test)
```

## Errores típicos

- **Leer SHAP como causalidad.** SHAP explica cómo reparte el modelo lo que ya ha decidido,
  ni más ni menos. Si dos variables están correlacionadas, el reparto entre ellas es en parte
  arbitrario: con la referencia marginal cada una se lleva la mitad del efecto, con la
  condicional una se lo lleva casi todo. El modelo no sabe cuál de las dos causa nada; para
  eso hace falta [[causalidad-vs-correlacion|diseño causal]], no un explicador.
- **Usar solo la media del valor absoluto.** El resumen global por `mean(/φ_i/)` te dice
  cuánto pesa cada variable, pero no en qué dirección. Una variable puede tener atribuciones
  de +5 y −5 que se cancelan: media absoluta alta y efecto medio cero. Mira siempre la
  distribución, no solo el número.
- **Leer una PDP con interacciones fuertes como si fuera el efecto real.** Si las curvas ICE
  se cruzan, la PDP promedia efectos opuestos y puede salir plana. Dibuja siempre algunas ICE
  junto a la PDP, o mira las atribuciones por pares.
- **Calcular PDP sobre valores imposibles.** Si fuerzas una variable a 200 años de edad o a un
  precio negativo, estás preguntando al modelo por regiones donde no hay datos y la respuesta
  es una extrapolación de un árbol, que es constante y sin sentido. Limita la rejilla al rango
  observado.
- **Confundir KernelSHAP con un cálculo exacto.** Es una estimación por muestreo: con 100
  muestras los valores cambian de una ejecución a otra. Si necesitas estabilidad, usa un
  modelo de árboles con TreeSHAP o sube mucho el número de muestras y comprueba que converge.
- **Explicar con datos contaminados.** Si el modelo se entrenó con [[fuga-de-datos|fuga de
  datos]], la explicación será perfectamente coherente y describirá una mentira. La
  interpretabilidad documenta un modelo; no lo valida.

:::practica
enunciado: Un modelo de dos variables predice 7,2 para una fila y su predicción media es 3,0. Los valores de coalición son v(vacío) = 3,0, v(a) = 5,0, v(b) = 4,0 y v(a,b) = 7,2. Reparte la predicción con valores de Shapley.
pista: Cada variable recibe la media de sus dos aportaciones marginales: la de entrar en el equipo vacío y la de entrar cuando la otra ya estaba dentro.
solucion: φ_a = ½[(5,0 − 3,0) + (7,2 − 4,0)] = ½(2,0 + 3,2) = 2,6. φ_b = ½[(4,0 − 3,0) + (7,2 − 5,0)] = ½(1,0 + 2,2) = 1,6. La suma, 2,6 + 1,6 = 4,2, coincide con la predicción de la fila menos la media, 7,2 − 3,0: se cumple la eficiencia. La variable a explica 2,6 de los 4,2 puntos que esta fila está por encima de la media.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué garantiza la propiedad de eficiencia de los valores de Shapley?
o: Que la suma de las atribuciones es igual a la predicción de esa fila menos la predicción media
o: Que cada variable recibe la misma atribución en todas las filas
o: Que las variables correlacionadas se reparten el efecto a partes iguales
a: 1
e: La eficiencia dice que las atribuciones reparten exactamente el premio: la diferencia entre f(x) y E[f(X)]. No dice nada sobre filas distintas ni sobre variables correlacionadas, donde el reparto entre ellas sí depende de la referencia elegida.
:::

:::quiz
p: La PDP de una variable sale casi plana, pero sus curvas ICE tienen pendientes fuertes y de signo contrario. ¿Qué conclusión es correcta?
o: La variable no influye en la predicción
o: Hay interacción: la variable sube la predicción en unos casos y la baja en otros, y el promedio lo oculta
o: La PDP está mal calculada porque las ICE siempre deben ser paralelas
a: 2
e: La PDP es la media de las ICE. Si unas suben y otras bajan con fuerza, la media puede quedar plana sin que el efecto sea nulo. Una PDP plana con ICE inclinadas es la señal clásica de interacción.
:::

:::quiz
p: Para un modelo de gradient boosting con 5.000 filas quieres atribuciones por observación. ¿Qué camino es el razonable?
o: KernelSHAP con 50 muestras, porque es el método general
o: TreeSHAP, que es exacto para modelos de árboles
o: La importancia por impureza, que ya da un valor por fila
a: 2
e: TreeSHAP explota la estructura del árbol y calcula el valor exacto en tiempo polinómico. KernelSHAP sirve para cualquier modelo pero es una estimación con ruido, y con 50 muestras es muy inestable. La importancia por impureza da un único número por variable, no por fila.
:::

:::trampa
SHAP es aditivo por construcción: la suma de las atribuciones reconstruye la predicción. Eso
lo hace sonar como una descomposición única y definitiva, pero el reparto depende de la
distribución de referencia que uses para `v(S)`. Cambia de referencia y cambian los números,
sin que el modelo haya cambiado. Cita siempre qué referencia y qué implementación usaste.
:::
