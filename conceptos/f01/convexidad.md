---
id: convexidad
titulo: Convexidad
fase: 1
nivel: avanzado
rutas: [core, ds, quant]
prerequisitos: [derivadas-parciales-y-gradiente, derivadas-y-reglas]
tags: [optimizacion, minimos, teoria]
resumen: Una función convexa tiene un único valle: cualquier mínimo local es el global, y eso convierte un problema de optimización en un problema resuelto.
fuentes: ["Boyd y Vandenberghe (2004), 'Convex Optimization'"]
---

## En una frase

Una función convexa se curva siempre «hacia arriba», como un cuenco: eso garantiza que cualquier
mínimo local que encuentres es el mínimo global, que es exactamente lo que necesitas para
confiar en un algoritmo de optimización.

## La idea

Imagina que estás buscando el punto más bajo de un terreno con los ojos vendados y solo puedes
notar la pendiente bajo tus pies. Si el terreno es una única hoya, caminar siempre cuesta abajo
te lleva al fondo: no hay forma de quedarte atrapado en un hoyo lateral porque no existen. Si el
terreno es una cordillera con muchos valles, la misma estrategia te deja en el primer hoyo que
encuentres, y no tienes manera de saber si hay uno más profundo al otro lado. La convexidad es
la propiedad que distingue los dos paisajes.

Formalmente, convexo significa que el segmento que une dos puntos cualesquiera de la gráfica
**nunca pasa por debajo** de la curva. Dicho de otra forma: si mezclas dos soluciones con
cualquier peso, el resultado no es peor que la mezcla de sus valores. Esa propiedad es la que
hace que la optimización convexa sea una tecnología madura: existen algoritmos que garantizan
encontrar la solución óptima en tiempo polinómico, y se puede certificar cuándo has terminado.

Esto importa mucho más de lo que parece en datos. La regresión lineal por mínimos cuadrados es
un problema convexo (tiene solución cerrada); la regresión con regularización L1 o L2 también;
la regresión logística, también, aunque no tenga fórmula cerrada. En cambio, entrenar una red
neuronal no lo es: su paisaje está lleno de sillas y de mínimos locales, y por eso se aceptan
soluciones «suficientemente buenas» en vez de óptimas. Saber en qué lado de esa línea está tu
problema decide cuánto puedes confiar en el resultado.

## Definición formal

Un conjunto `C ⊆ ℝⁿ` es **convexo** si para todo `x, y ∈ C` y todo `θ ∈ [0, 1]` se cumple que
`θx + (1 − θ)y ∈ C`: el segmento entre dos puntos del conjunto se queda dentro.

Una función `f: C → ℝ` (con `C` convexo) es **convexa** si para todo `x, y ∈ C` y todo
`θ ∈ [0, 1]`:

:::formula
f(θx + (1 − θ)y) ≤ θ f(x) + (1 − θ) f(y)
:::

- `x`, `y` — dos puntos cualesquiera del dominio.
- `θ` — peso entre 0 y 1; `θx + (1 − θ)y` es un punto del segmento que los une.
- El lado izquierdo es el valor real de `f` en el punto intermedio; el derecho es la
  interpolación lineal de los valores extremos. Convexo significa «la cuerda va por encima».
- Si la desigualdad es estricta para `x ≠ y`, la función es **estrictamente convexa**.

:::figura
fichero: convexidad-cuerda-y-tangente
pie: Los tres paneles son el mismo criterio mirado de tres maneras. En los dos primeros la cuerda y la tangente cumplen su papel, y por eso el punto crítico es fiable; en el tercero la cuerda corta la gráfica y ni siquiera existe un mínimo global. Si tu función se parece al tercer dibujo, ningún algoritmo te garantiza nada.
fuente: figuras/convexidad-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `f` | La función que estas minimizando | las de la magnitud que mides | Si deja de ser convexa, un mínimo local puede no ser el global: se pierde la garantia |
| `x`, `y` | Dos puntos cualesquiera del dominio | las de la variable de entrada | Nada: la desigualdad tiene que cumplirse para todos los pares, no solo para los comodos |
| `θ` | Peso del punto intermedio, dentro de `[0, 1]` | adimensional | Recorre el segmento entero; fuera de ese rango ya no es una mezcla y la desigualdad no dice nada |
| `f''(x)` | Segunda derivada: la curvatura en una variable | unidades de `f` partido por las de `x` al cuadrado | Si se hace negativa en algun tramo, la función deja de ser convexa ahi |
| `H` | Matriz hessiana: la curvatura en cada dirección | las de las segundas derivadas | Si algun autovalor se vuelve negativo, hay una dirección que baja: silla o maximo |
| `v` | Una dirección cualquiera donde probar la curvatura | la de las variables | `vᵀHv` debe ser mayor o igual que cero en TODAS las direcciones, no solo en los ejes |
| `∇f(x)` | Gradiente: la pendiente en el punto | unidades de `f` por unidad de `x` | Con convexidad, anularlo ya es suficiente para el mínimo global; sin ella, es solo necesario |
:::

`f` es **cóncava** si `−f` es convexa, y entonces la cuerda va por debajo.

**Criterios prácticos**, de más útil a menos:

1. **Segunda derivada:** en una variable, `f` es convexa en un intervalo si `f''(x) ≥ 0` en todo
   él. Con `f'' > 0` es estrictamente convexa.
2. **Hessiano:** en varias variables, `f` es convexa si su [[jacobiano-y-hessiano|hessiano]] es
   semidefinido positivo en todo el dominio (`vᵀHv ≥ 0` para todo vector `v`). Si es definido
   positivo, es estrictamente convexa.
3. **Tangente por debajo:** `f` es convexa si y solo si `f(y) ≥ f(x) + ∇f(x)·(y − x)` para
   todos `x, y`. Es decir, la recta tangente en cualquier punto queda por debajo de la gráfica.
4. **Reglas de composición:** suma de convexas es convexa; multiplicar por un escalar positivo
   conserva la convexidad; el máximo de varias funciones convexas es convexo; una norma es
   convexa.

**Consecuencias para la optimización:**

- Todo mínimo local de una función convexa es un **mínimo global**; si es estrictamente convexa,
  el mínimo es único.
- El conjunto de minimizadores `{x : f(x) ≤ α}` es convexo (los conjuntos de subnivel no tienen
  agujeros separados).
- `∇f(x*) = 0` es condición **necesaria y suficiente** para que `x*` sea mínimo global. Con
  funciones no convexas era solo necesaria.

## Ejemplo

Tres funciones, mismo punto crítico, tres historias distintas. En todas, `x = 0` anula la
primera derivada.

- `f(x) = 3x² + 6x + 11`. `f'(x) = 6x + 6`, se anula en `x = −1`. `f''(x) = 6 > 0` en todas
  partes, así que es estrictamente convexa y `(−1, 8)` es el mínimo **global**. Se puede
  comprobar con la desigualdad de la cuerda: con `x = −2` y `y = 0`, `f(−2) = 11`, `f(0) = 11`, el
  punto medio es `−1` y `f(−1) = 8 ≤ (11 + 11)/2 = 11`. La cuerda va por encima.
- `g(x) = −3x² + 6x + 11`. `g'(x) = −6x + 6`, se anula en `x = 1`, y `g''(x) = −6 < 0`: es
  cóncava, y `(1, 14)` es un máximo. Intentar minimizarla con descenso de gradiente no lleva a
  ninguna parte: la función baja indefinidamente cuando `x → ±∞`.
- `h(x) = x³ − 3x`. `h'(x) = 3x² − 3`, se anula en `x = ±1`. `h''(x) = 6x`: negativa en `x = −1`
  (máximo local, `h(−1) = 2`) y positiva en `x = 1` (mínimo local, `h(1) = −2`). No es convexa ni
  cóncava: tiene los dos tipos de punto crítico, y el mínimo global no existe porque
  `h(x) → −∞` cuando `x → −∞`.

En varias variables, `q(x, y) = x² + 4xy + 5y²` tiene hessiano `[[2, 4], [4, 10]]`, cuyos
autovalores son `6 ± √32 ≈ 0,34` y `11,66`: ambos positivos, luego el hessiano es definido
positivo, `q` es estrictamente convexa y su único punto crítico `(0, 0)` es el mínimo global. Los
menores principales dan la misma conclusión sin calcular autovalores: `2 > 0` y
`2·10 − 4·4 = 4 > 0`.

## Código

```python verificable
import numpy as np

# f(x) = 3x^2 + 6x + 11 es convexa: todo punto que anula la derivada es el mínimo global.
f = lambda x: 3 * x**2 + 6 * x + 11
df = lambda x: 6 * x + 6

# Comprobación de la desigualdad de la cuerda en muchos pares de puntos
rng = np.random.default_rng(0)
x = rng.uniform(-5, 5, size=200)
y = rng.uniform(-5, 5, size=200)
theta = rng.uniform(0, 1, size=200)
cuerda = f(theta * x + (1 - theta) * y) - (theta * f(x) + (1 - theta) * f(y))

print("se cumple la desigualdad de la cuerda:", bool(cuerda.max() <= 1e-6))   # salida: True
print("minimo de la funcion                 :", round(float(f(-1.0)), 4))    # salida: 8.0
print("derivada en x=-1                     :", round(float(df(-1.0)), 8))   # salida: 0.0
```

:::claves
- `rng.uniform(-5, 5, size=200)` devuelve un array de 200 números, pero `rng.uniform(-5, 5)` sin `size` devolveria **un solo número**, no un array de uno. Ese detalle cambia el tipo de todo lo que venga después.
- Las tres líneas de `rng.uniform` se llaman una detras de otra sobre el **mismo generador**, así que consumen números distintos: `x`, `y` y `theta` no se repiten. Si necesitas reproducir la figura, no cambies el orden de esas tres líneas.
- La comparación es `cuerda.max() <= 1e-6`, con tolerancia, y no `cuerda.max() <= 0`. La diferencia siempre sale con error de redondeo del orden de `1e-14`, así que exigir cero exacto haría fallar una función que si es convexa.
- `bool(...)` esta ahi porque `cuerda.max() <= 1e-6` devuelve un `numpy.bool_`, no un `bool` de Python. Al imprimirlo se ve igual, pero si lo usas en un `if` con arrays de mas de un elemento, NumPy lanza un error de ambiguedad.
- Cambia `size=200` por `size=1`: el código sigue funcionando y la comprobación sigue diciendo `True`, porque has probado un solo par de puntos. La convexidad se comprueba con muchos pares justamente por eso: un par que cumple no demuestra nada.
:::

```python verificable
import numpy as np

# La convexidad también se ve en la segunda derivada: positiva en todo el dominio.
f = lambda x: 3 * x**2 + 6 * x + 11
theta = np.random.default_rng(1).uniform(-5, 5, size=200)   # 200 puntos del dominio

h = 1e-3    # con h más pequeño, el error de redondeo de la diferencia se come el resultado
segunda = (f(theta + h) - 2 * f(theta) + f(theta - h)) / h**2

print("segunda derivada numerica:", round(float(segunda.mean()), 4))    # salida: 6.0
print("todas positivas          :", bool(np.all(segunda > 0)))          # salida: True
```

```python verificable
import numpy as np

# El hessiano decide: definido positivo -> convexa -> el punto crítico es mínimo global.
H = np.array([[2.0, 4.0], [4.0, 10.0]])
autovalores = np.linalg.eigvalsh(H)

q = lambda v: v[0] ** 2 + 4 * v[0] * v[1] + 5 * v[1] ** 2

print("autovalores del hessiano:", np.round(autovalores, 4))            # salida: [ 0.3431 11.6569]
print("todos positivos        :", bool(np.all(autovalores > 0)))        # salida: True
print("q en el punto critico  :", round(float(q([0.0, 0.0])), 8))       # salida: 0.0

# No es solo el origen: cualquier punto tiene un valor mayor (es el mínimo global)
print("q en (1, -1)           :", round(float(q([1.0, -1.0])), 4))       # salida: 2.0
print("q en (-2, 1)           :", round(float(q([-2.0, 1.0])), 4))       # salida: 1.0
```

## Errores típicos

- **Dar por hecho que el mínimo encontrado es el global.** Salvo que demuestres convexidad (o
  que el problema tenga estructura), un mínimo local no dice nada del global. En redes
  neuronales y en problemas de agrupamiento esto no está garantizado.
- **Confundir convexo con «curvado hacia arriba en algún punto».** La convexidad es una
  propiedad **global** del dominio: `h(x) = x³ − 3x` tiene un tramo donde `h'' > 0` pero no es
  convexa en todo `ℝ`.
- **Comprobar el hessiano solo en un punto.** `H` definido positivo en `x₀` no implica que `f`
  sea convexa en todo el dominio; solo implica que `x₀` es un mínimo local. Para convexidad hay
  que comprobar todo el dominio (o usar reglas de composición).
- **Creer que convexo implica derivable.** `f(x) = /x/` es convexa y no es derivable en cero.
  Existe subgradiente, y los algoritmos de optimización convexa funcionan igual; lo que se pierde
  es la condición `∇f = 0`.
- **Confundir estrictamente convexa con fuertemente convexa.** La primera da unicidad del
  mínimo; la segunda, además, garantiza una velocidad de convergencia. `x⁴` es estrictamente
  convexa pero su hessiano es cero en el origen, y el descenso de gradiente allí converge
  lentísimo.
- **Sumar funciones convexas sin mirar los signos.** La suma de convexas es convexa, pero restar
  una convexa destruye la garantía: `f(x) − g(x)` con ambas convexas no es convexa en general.
  Y multiplicar por una constante negativa convierte convexa en cóncava.

:::practica
enunciado: Para q(x) = 2x² − 8x + 7, decide si es convexa, encuentra su punto crítico y di si ese punto es el mínimo global. Comprueba la desigualdad de la cuerda con x = 1 e y = 3 tomando θ = 0,5.
pista: Con q''(x) constante y positiva, la estricta convexidad decide por ti.
solucion: q'(x) = 4x − 8 se anula en x = 2, y q''(x) = 4 > 0 en todo el dominio, así que es estrictamente convexa y x = 2 es el mínimo global, con q(2) = 8 − 16 + 7 = −1. La cuerda con θ = 0,5: el punto medio es 2, y q(1) = 1 y q(3) = 1 dan (1 + 1)/2 = 1; se cumple −1 ≤ 1, que es la desigualdad de convexidad.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué garantiza que una función sea convexa en todo su dominio?
o: Que cualquier mínimo local es el mínimo global
o: Que la función es derivable
o: Que tiene un máximo y un mínimo
a: 1
e: La convexidad implica que no hay valles secundarios: si el gradiente se anula, estás en el fondo. No implica derivabilidad (el valor absoluto es convexo y no es derivable en cero) ni la existencia de máximo, porque una convexa puede crecer indefinidamente.
:::

:::quiz
p: En el intervalo [-1, 1], f(x) = x³ tiene f''(x) = 6x, que es negativa para x < 0 y positiva para x > 0. ¿Qué se concluye?
o: Que f es convexa porque f'' > 0 en la mitad del intervalo
o: Que f no es convexa en el intervalo completo, aunque lo sea en cada mitad por separado
o: Que f'' no sirve para estudiar convexidad
a: 2
e: La convexidad exige f'' >= 0 en todo el intervalo. x³ es cóncava en [-1, 0] y convexa en [0, 1], pero en el intervalo completo la cuerda entre -1 y 1 corta la gráfica, así que no es convexa ahí.
:::

:::quiz
p: La regresión lineal por mínimos cuadrados es un problema convexo. ¿Qué consecuencia práctica tiene?
o: Que la solución de mínimos cuadrados es el óptimo global y no hay mínimos locales en los que quedarse atrapado
o: Que el modelo no puede sobreajustar
o: Que los residuos son siempre cero
a: 1
e: La función de pérdida cuadrática es convexa, así que cualquier algoritmo que la minimice converge al óptimo global. Eso no dice nada sobre sobreajuste (que depende del número de variables y de la regularización) ni implica residuos nulos, solo que no se pueden mejorar.
:::

:::trampa
«Uso descenso de gradiente, así que encuentro el mínimo» solo es cierto si el problema es
convexo o si has encontrado el mínimo por varios caminos. Con una red neuronal, dos semillas
distintas dan soluciones distintas con la misma pérdida: eso no es un bug, es el paisaje no
convexo. Si necesitas una garantía, cambia de modelo o demuestra convexidad.
:::
