---
id: derivadas-parciales-y-gradiente
titulo: Derivadas parciales y gradiente
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [derivadas-y-reglas, escalares-vectores-matrices, producto-punto-y-similitud, regla-de-la-cadena]
tags: [calculo, optimizacion, gradiente]
resumen: La derivada parcial mide como cambia una función al mover una sola variable; el gradiente las junta en un vector que apunta al maximo crecimiento.
fuentes: ["Stewart (2015), 'Calculus: Early Transcendentals'", "Boyd y Vandenberghe (2004), 'Convex Optimization'"]
---

## En una frase

La derivada parcial dice cuánto cambia una función cuando mueves **una sola** de sus variables
dejando el resto quietas, y el gradiente es el vector que reúne todas esas derivadas: apunta en
la dirección de máximo crecimiento y su longitud es la pendiente en esa dirección.

## La idea

Imagina que estás en una ladera con niebla y solo tienes un altímetro. No ves el paisaje, pero
puedes dar un paso al norte y ver cuánto sube el altímetro, luego volver y dar un paso al este.
Esas dos medidas son las derivadas parciales: cada una mide la pendiente en una dirección,
manteniendo la otra congelada. El gradiente es el vector que combina ambas y responde a la
pregunta útil: **¿hacia dónde doy el paso para subir lo más rápido posible, y cuánto subo por
metro?** Camina en dirección contraria al gradiente y bajas lo más rápido posible. Eso es
literalmente el descenso de gradiente, el algoritmo que entrena casi todo modelo de machine
learning.

Hay un detalle que se pasa por alto: el gradiente **no** es una dirección universal, es una
dirección concreta en el punto donde lo evalúas. En cada punto de la ladera el gradiente apunta
a otro sitio. Y su longitud depende de las unidades: si mides altura en metros y distancia en
kilómetros, el número cambia aunque la montaña sea la misma. Por eso en machine learning se
escalan las variables: el descenso de gradiente avanza con un paso fijo y, si una variable
tiene un rango mil veces mayor que otra, el paso será enorme en una dirección y ridículo en la
otra. Esa es la razón práctica de estandarizar antes de entrenar.

## Definición formal

Sea `f(x₁, x₂, …, xₙ)` una función de `n` variables. La **derivada parcial** respecto de `xⱼ`
en un punto es la derivada ordinaria tratando el resto como constantes:

:::formula
∂f/∂xⱼ = lím_{h→0} [ f(…, xⱼ + h, …) − f(…, xⱼ, …) ] / h
:::

- `∂` — símbolo de derivada parcial (una d redondeada); se usa para dejar claro que hay más
  variables y que no todas se mueven.
- `xⱼ` — la variable que se mueve; el resto permanece fijo.
- `h` — incremento infinitesimal que tiende a cero.

El **gradiente** es el vector con todas las parciales:

:::formula
∇f(x) = ( ∂f/∂x₁ , ∂f/∂x₂ , … , ∂f/∂xₙ )
:::

- `∇` — operador nabla; `∇f` se lee «gradiente de f».
- `x` — el punto (un vector de `n` coordenadas) donde se evalúa.

Tres propiedades que se usan constantemente:

- **Derivada direccional.** Con `u` un vector unitario, la tasa de cambio de `f` al moverse en
  la dirección `u` es `∇f(x) · u`, el producto escalar. Por la desigualdad de Cauchy-Schwarz,
  ese producto es máximo cuando `u` apunta en la misma dirección que `∇f` y vale `‖∇f‖`. De ahí
  la afirmación «el gradiente apunta al máximo crecimiento».
- **Condición de punto crítico.** En un mínimo o máximo interior de una función derivable,
  `∇f(x) = 0` (todas las parciales se anulan). Es condición necesaria, no suficiente: un punto
  de silla también la cumple.
- **Regla de la cadena multivariante.** Si `f` depende de `u` y `u` depende de `x`, entonces
  `∂f/∂xⱼ = Σᵢ (∂f/∂uᵢ)·(∂uᵢ/∂xⱼ)`. Es la misma regla de la cadena, sumando por todos los
  caminos.

Como se lee `∇f(x) · u`: es el [[producto-punto-y-similitud|producto punto]] entre el vector
gradiente y el vector dirección `u`, es decir `Σⱼ (∂f/∂xⱼ)·uⱼ`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `∂f/∂xⱼ` | Cuánto cambia `f` al mover solo la variable `xⱼ` | salida por unidad de `xⱼ` | Cada parcial hereda la escala de su variable: si `xⱼ` se mide en unidades mil veces mayores, su parcial es mil veces mayor y domina el gradiente |
| `∇f(x)` | El vector con todas las parciales, evaluado en el punto `x` | salida por unidad de distancia | Al alejarte del mínimo su longitud crece y el paso avanza mucho; cerca del mínimo se hace diminuta y el descenso se arrastra. Si todas las componentes son cero, el punto es crítico |
| `x` | El punto (un vector de `n` coordenadas) donde se evalúa | las de las variables | No es una dirección universal: en cada punto el gradiente apunta a otro sitio, y en el mínimo vale cero |
| `u` | La dirección en la que te mueves, de norma 1 | adimensional | La derivada direccional es `∇f · u` y es máxima cuando `u` apunta como el gradiente, donde vale `‖∇f‖`; si `u` es perpendicular, vale cero |
| `h` | El paso de la aproximación numérica de la parcial | las de la variable | Entre `10⁻⁸` y `10⁻⁴` hay un compromiso óptimo; por debajo de `10⁻¹⁰` el redondeo de la resta se come el resultado, igual que en una variable |
| `lr` | La tasa de aprendizaje del descenso de gradiente | las de la distancia por unidad de gradiente | Si es demasiado grande, el método oscila o diverge; si es muy pequeña, avanza tan poco que parece no hacer nada. Con la curvatura de este ejemplo, el límite está cerca de `2 / λ_max` |
:::

## Ejemplo

Sea `f(x, y) = x² + 2xy + 3y²`.

**Derivadas parciales.** Tratando `y` como constante: `∂f/∂x = 2x + 2y`. Tratando `x` como
constante: `∂f/∂y = 2x + 6y`. Por tanto `∇f(x, y) = (2x + 2y, 2x + 6y)`.

**En el punto (1, 2):** `∇f(1, 2) = (2·1 + 2·2, 2·1 + 6·2) = (6, 14)`. La longitud es
`√(36 + 196) = √232 ≈ 15,23`: moviéndose en la dirección `(6, 14)/15,23` la función crece a razón
de 15,23 por unidad de distancia.

**Comprobación numérica.**

:::figura
fichero: gradiente-campo-y-descenso
pie: A la izquierda, las curvas de nivel de `f(x, y) = x² + 2xy + 3y²` y, en cada punto, una flecha con la dirección del gradiente. Las flechas siempre cruzan las líneas grises en ángulo recto, y en el centro (0, 0) no hay flecha: allí el gradiente vale cero y la función tiene su mínimo. Mira que la dirección cambia de un punto a otro: el gradiente no es una dirección única. A la derecha, el descenso de gradiente sobre ese mismo mapa: los primeros pasos, con el gradiente grande, avanzan mucho; los últimos, cerca del mínimo, apenas se mueven. Esa desigualdad de ritmos es lo que se arregla escalando las variables antes de entrenar.
fuente: figuras/derivadas-parciales-y-gradiente-1.py
:::

`f(1, 2) = 1 + 4 + 12 = 17`. Con un paso de 0,001 en la dirección
del gradiente normalizado, el punto es `(1,0004, 2,0009)` y
`f ≈ 17,01523`, es decir un aumento de 0,01523 ≈ 15,23 · 0,001. Coincide con `‖∇f‖` por el
tamaño del paso.

**Comprobación de un mínimo.** `∇f = 0` exige `2x + 2y = 0` y `2x + 6y = 0`, cuya única solución
es `(0, 0)`. Ahí `f = 0`, y como `f(x,y) = (x + y)² + 2y²` es suma de cuadrados, es el mínimo
global (la función es convexa).

## Código

```python verificable
import numpy as np

# f(x, y) = x**2 + 2xy + 3y**2 -> gradiente (2x + 2y, 2x + 6y)
def f(p):
    x, y = p
    return x**2 + 2 * x * y + 3 * y**2

def grad(p):
    x, y = p
    return np.array([2 * x + 2 * y, 2 * x + 6 * y])

# Descenso de gradiente: caminar en dirección contraria al gradiente.
# Con lr = 0.1 y una función con número de condición ~5.8, hacen falta unos cientos de pasos
# para acercarse al mínimo: la convergencia depende de la curvatura, no solo de la dirección.
p, lr = np.array([4.0, -3.0]), 0.1
for _ in range(250):
    p = p - lr * grad(p)

print("gradiente en (1,2):", grad(np.array([1.0, 2.0])))   # -> [ 6. 14.]
print("norma             :", round(float(np.linalg.norm(grad([1.0, 2.0]))), 2))  # -> 15.23
print("mínimo encontrado :", np.round(p, 8), "f =", round(float(f(p)), 8))       # salida: [ 0. -0.] f = 0.0
```

:::claves
- `p = p - lr * grad(p)` **no** modifica el array original en el sitio: crea uno nuevo y vuelve a etiquetar `p`. Funciona igual en este bucle, pero la diferencia importa en cuanto haya otra variable apuntando al mismo array; para modificar de verdad hay que usar `p -= lr * grad(p)`.
- `grad(p)` devuelve un `np.array` de dos elementos y `lr * grad(p)` lo escala entero. Si `grad` devolviera una tupla, la resta de un array y una tupla seguiría funcionando por conversión, pero cualquier operación con formas distintas se rompería: el tipo de retorno de la función es parte del contrato.
- `x, y = p` **desempaqueta** el array, y es lo que permite escribir `def grad(p): x, y = p`. Si `p` tuviera tres componentes, esa línea lanzaría `ValueError`; es la forma de que el código avise cuando el problema cambia de tamaño.
- `np.linalg.norm(grad([1.0, 2.0]))` calcula la **norma euclídea** (raíz de la suma de los cuadrados) y devuelve un `np.float64`. Al pasarlo a `round` y a `float` se convierte en un `float` de Python: sin ese paso, algunos `print` y formatos muestran `np.float64(15.23)` en lugar de `15.23`.
- `f = lambda x, y: x**2 + 2 * x * y + 3 * y**2` define la misma función que `def f(...)` del bloque anterior, pero **sin nombre interno**. Con una `lambda` no se pueden añadir comentarios ni trazas dentro, y si se queda sin asignar a una variable no se puede depurar.
- `grad_numerico` devuelve `round(fx, 4), round(fy, 4)`: una **tupla** de dos números redondeados, no un array. Por eso se imprime como `(6.0, 14.0)` con paréntesis y no como `[6. 14.]` con corchetes, que es lo que devuelve la versión analítica. Comparar las dos salidas exige fijarse en el tipo, no solo en los números.
:::

```python verificable
import numpy as np

# El gradiente no es una dirección universal: cambia de punto en punto.
f = lambda x, y: x**2 + 2 * x * y + 3 * y**2

def grad_numerico(x, y, h=1e-6):
    fx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    fy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return round(fx, 4), round(fy, 4)

for punto in [(1.0, 2.0), (0.0, 0.0), (-2.0, 1.0)]:
    print("punto", punto, "gradiente", grad_numerico(*punto))
# salida:
# punto (1.0, 2.0) gradiente (6.0, 14.0)
# punto (0.0, 0.0) gradiente (0.0, 0.0)
# punto (-2.0, 1.0) gradiente (-2.0, 2.0)
```

## Errores típicos

- **Olivdar que las demás variables son constantes.** Al derivar `x²y³` respecto de `x`, `y³` es
  una constante y el resultado es `2xy³`. Tratar `y` como variable y aplicar la regla del
  producto cuando no toca es el fallo más habitual al empezar.
- **Usar el gradiente sin escalar las variables.** Si una variable va de 0 a 1 y otra de 0 a
  1.000.000, el gradiente está dominado por la segunda y el descenso de gradiente con paso fijo
  se comporta fatal. Estandariza o normaliza antes de optimizar.
- **Confundir gradiente con derivada direccional.** El gradiente es un vector; la derivada
  direccional es un número (la pendiente en una dirección concreta). Solo coinciden en valor
  cuando la dirección es la del propio gradiente.
- **Creer que `∇f = 0` garantiza un mínimo.** Un punto de silla también anula el gradiente. Hace
  falta mirar la curvatura (el [[jacobiano-y-hessiano|hessiano]]) o comprobar que la función es
  [[convexidad|convexa]].
- **Sumar mal los caminos en la regla de la cadena.** Cuando una variable intermedia influye en
  la salida por dos rutas, las dos contribuciones se **suman**. Omitir una da un gradiente
  incompleto: es el bug clásico de la retropropagación escrita a mano.
- **Olvidar que el gradiente se evalúa en un punto.** Decir «el gradiente de `f` es (6, 14)» sin
  decir dónde es una afirmación incompleta: `∇f` es una función que a cada punto le asigna un
  vector.

:::practica
enunciado: Para f(x, y) = x² + y² + 2x + 4y, calcula el gradiente en el punto (3, 1), su longitud y cuánto crece la función al avanzar 0,01 unidades en la dirección del gradiente.
pista: Trata la otra variable como constante en cada parcial y recuerda que la dirección de máximo crecimiento lleva la longitud del gradiente.
solucion: Las parciales son 2x + 2 y 2y + 4, así que ∇f(3, 1) = (8, 6). Su longitud es √(64 + 36) = √100 = 10: en esa dirección la función crece 10 por unidad de distancia, y con un paso de 0,01 crece unas 0,1 unidades. El gradiente se anula en (−1, −2), donde f vale −5, el mínimo global.
:::

## Comprueba que lo sabes

:::quiz
p: Con f(x, y) = x² + 2xy + 3y², ¿cuál es ∇f(1, 2)?
o: (3, 8)
o: (6, 14)
o: (2, 6)
a: 2
e: Las parciales son 2x+2y y 2x+6y. Evaluando en (1,2) sale (2+4, 2+12) = (6, 14). La opción (2,6) son los coeficientes sin evaluar; la otra no corresponde a ninguna parcial correcta.
:::

:::quiz
p: ¿Por qué se dice que el gradiente apunta a la dirección de máximo crecimiento?
o: Porque es perpendicular a la curva de nivel y el producto escalar con un vector unitario se maximiza cuando ambos apuntan igual
o: Porque siempre tiene coordenadas positivas
o: Porque su longitud es la derivada segunda
a: 1
e: La derivada direccional es el producto escalar del gradiente con la dirección. Ese producto es máximo cuando la dirección coincide con el gradiente, y entonces vale la norma del gradiente. Las curvas de nivel son perpendiculares al gradiente por la misma razón.
:::

:::quiz
p: Un modelo tiene una variable en euros (rango 10.000 a 500.000) y otra en tanto por uno (0 a 1). ¿Qué le pasa al descenso de gradiente con paso fijo?
o: Nada, el algoritmo se adapta solo al rango de cada variable
o: El gradiente queda dominado por la variable de mayor escala y el paso resulta inadecuado en las dos direcciones
o: Solo funciona si las dos variables son positivas
a: 2
e: Las derivadas parciales heredan la escala de su variable, así que la componente de la variable grande es enorme y la otra diminuta. Con un paso fijo, o te pasas en una dirección o no avanzas en la otra. Se arregla estandarizando o normalizando antes de optimizar.
:::

:::trampa
Un gradiente numérico mal calculado es un clásico: si usas `(f(x+h) − f(x))/h` con `h = 1e-15`,
el error de redondeo se come el resultado. La diferencia central
`(f(x+h) − f(x−h))/(2h)` con `h` entre 1e-6 y 1e-5 da muchos más dígitos correctos, y es la
forma de comprobar tu gradiente analítico.
:::
