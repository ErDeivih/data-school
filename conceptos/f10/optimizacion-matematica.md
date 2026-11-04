---
id: optimizacion-matematica
titulo: Optimización matemática
fase: 10
nivel: avanzado
rutas: [alg, quant]
prerequisitos: [derivadas-parciales-y-gradiente, convexidad, optimizacion-con-restricciones]
tags: [optimizacion, programacion-lineal, gradiente, metaheuristicas]
resumen: Programación lineal, entera, descenso de gradiente y metaheurísticas: cómo elegir el método según la forma del problema y qué garantía da cada uno.
fuentes: ["Boyd y Vandenberghe (2004), 'Convex Optimization'", "Nocedal y Wright (2006), 'Numerical Optimization'", "Wolsey (1998), 'Integer Programming'"]
---

## En una frase

Optimizar es encontrar el mejor valor posible de unas variables dentro de unas restricciones, y
la primera decisión —la que determina todo lo demás— no es qué solver usar, sino **de qué tipo
es el problema**: lineal, entero, convexo o ninguno de los anteriores.

## La idea

Imagina que tienes que asignar 200 turnos de trabajo entre 60 personas respetando descansos,
convenios y preferencias. Podrías escribir una función de coste y bajar por su pendiente hasta
que ya no baje más. Mal camino: ese problema tiene restricciones duras (un turno no puede
quedarse sin cubrir) y variables enteras (media persona no existe), y la función de coste está
llena de valles del tamaño de una mosca. El descenso de gradiente te dejará en el fondo de
cualquiera de ellos.

La clasificación correcta es la que decide el método:

1. **Programación lineal (LP).** Tanto la función objetivo como todas las restricciones son
   lineales, y las variables son continuas. Es el caso fácil: existe un algoritmo —el
   **simplex**, o los métodos de punto interior— que encuentra el **óptimo global** en un tiempo
   que en la práctica crece de forma casi lineal con el tamaño, aunque su peor caso teórico sea
   exponencial (el cubo de Klee-Minty lo demuestra). Problemas con millones de variables y
   restricciones se resuelven en segundos. La razón profunda es geométrica: el
   conjunto factible es un poliedro y el óptimo está siempre en un vértice, así que no hay
   valles interiores donde quedarse atrapado.
2. **Programación entera (IP/MIP).** Algunas o todas las variables deben ser enteras. Es
   **NP-duro**. El método estándar, **branch and bound**, resuelve relajaciones lineales y va
   partiendo el problema en subproblemas. Funciona sorprendentemente bien en la práctica, pero
   no hay garantía de rapidez, y la diferencia entre la mejor solución entera y la cota que da
   la relajación —el **gap de integralidad**— es lo que decide si el problema es tratable.
3. **Optimización convexa no lineal.** La función objetivo es convexa y el conjunto factible
   también. Aquí los métodos de gradiente, Newton o punto interior encuentran el óptimo global
   porque **todo mínimo local es global**. Es la frontera práctica: si puedes reformular tu
   problema como convexo, dejas de tener un problema de optimización y pasas a tener uno de
   cálculo.
4. **No convexo.** Redes neuronales, carteras con cardinalidad, rutas. Aquí no hay garantías:
   descenso de gradiente estocástico con muchos reinicios, o **metaheurísticas** (recocido
   simulado, algoritmos genéticos, búsqueda tabú) que exploran el espacio aceptando a veces
   movimientos que empeoran. Devuelven una buena solución, nunca un certificado de que sea la
   mejor.

La regla de oro: **antes de optimizar, clasifica**. Un problema lineal resuelto con descenso de
gradiente es un problema mal resuelto a propósito.

## Definición formal

**Forma estándar de un problema lineal.**

:::formula
minimizar cᵀx  sujeto a  A·x ≤ b,  x ≥ 0
:::

- `x` — vector de `n` variables de decisión.
- `c` — vector de `n` coeficientes de coste; `cᵀx` es el producto escalar, la función objetivo.
- `A` — matriz de `m` filas y `n` columnas con los coeficientes de las restricciones.
- `b` — vector de `m` términos independientes.
- `A·x ≤ b` — las `m` restricciones; `x ≥ 0` son las de no negatividad.

El conjunto `{x : A·x ≤ b, x ≥ 0}` es un poliedro convexo. El teorema fundamental de la
programación lineal dice que si el óptimo existe y el problema es acotado, **existe un vértice
del poliedro que es óptimo**. Un vértice se corresponde con una **solución básica factible**: se
fijan `n − m` variables a cero y se resuelven las `m` restantes. El número de vértices está
acotado por `C(n, m)`, el número de combinaciones, que crece exponencialmente; el simplex los
recorre de forma inteligente sin visitarlos todos.

**Programación entera y relajación.** Si se exige `x ∈ ℤⁿ` (o `xⱼ ∈ {0, 1}` en el caso binario),
el problema deja de ser convexo en el sentido útil: el conjunto factible son puntos sueltos. La
**relajación lineal** es el mismo problema sin la exigencia de integralidad. Su valor óptimo
`z_LP` siempre es una **cota** del óptimo entero `z_IP` en un problema de minimización
(`z_LP ≤ z_IP`), y el cociente `z_IP / z_LP` se llama **gap de integralidad**. El gap depende de
la formulación, no solo del problema: la misma mochila con una formulación más apretada puede
tener un gap mucho menor.

**Descenso de gradiente.** Para una función diferenciable `f`:

:::formula
x_{t+1} = x_t − η · ∇f(x_t)
:::

- `x_t` — el punto en la iteración `t`.
- `∇f(x_t)` — el gradiente, el vector de derivadas parciales; apunta hacia donde `f` crece más
  deprisa, así que se resta para bajar.
- `η` — el **paso** o tasa de aprendizaje, un número positivo que decide cuánto se avanza.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x` | Vector de variables de decisión | las de la variable (euros, turnos, unidades) | Mueve el objetivo: cuánto, lo dice `c` |
| `c` | Coeficientes de coste de la función objetivo | coste por unidad de variable | El objetivo cambia en `c` por cada unidad de `x`; reordena los vértices por calidad |
| `A`, `b` | Coeficientes y términos independientes de las restricciones | según la restricción | Añadir una restricción solo puede empeorar el óptimo: recorta la región factible |
| `z_LP` | Óptimo de la relajación lineal de un problema entero | las del objetivo | Es una cota, no la respuesta: en minimización siempre queda por debajo de `z_IP` |
| `η` | Paso del descenso de gradiente | unidades de `x` por unidad de gradiente | Converge más rápido hasta que se pasa: con `η ≥ 2/L` el método oscila o diverge |
| `L` | Curvatura máxima de la función (constante de Lipschitz del gradiente) | 1/unidades de `x` | Obliga a pasos más pequeños: la condición práctica es `η < 2/L` |
:::

:::figura
fichero: optimizacion-matematica-poliedro-y-paso
pie: A la izquierda, la región factible del ejemplo de la página con el valor del objetivo en cada vértice (0, 6, 8 y 9): el máximo está en (3, 1), un vértice, no en el interior. La trayectoria verde es el descenso de gradiente sobre la misma función objetivo: sube en la dirección (2, 3) y se sale del polígono en cuatro pasos, porque no sabe que existen restricciones. A la derecha, la distancia al mínimo a lo largo de las iteraciones para cuatro pasos: con η = 0,05 la recta baja despacio (un factor 0,9 por iteración), con η = 0,40 se planta en el mínimo en pocas vueltas, con η = 0,95 la curva va en zigzag y se acerca alternando, y con η = 1,05 se dispara hacia arriba hasta salirse del recuadro. El umbral está en `η < 2/L`, y con `L = 2` eso significa `η < 1`: por eso 0,95 aún converge y 1,05 no.
fuente: figuras/optimizacion-matematica-1.py
:::

Con `η` demasiado pequeño la convergencia es lentísima; con `η` demasiado grande el método
**diverge**: los iterados se alejan del mínimo en zigzag. Para funciones convexas y con paso
adecuado, la convergencia está garantizada.

**Convexidad.** `f` es convexa si para todo `a`, `b` y todo `λ ∈ [0, 1]`:

:::formula
f(λ·a + (1 − λ)·b) ≤ λ·f(a) + (1 − λ)·f(b)
:::

La gráfica entre dos puntos queda por debajo de la cuerda que los une. La consecuencia práctica
es la que importa: **cualquier mínimo local es un mínimo global**, así que puedes parar cuando
el gradiente se anula sin miedo a haberte equivocado de valle.

## Ejemplo

**Un programa lineal a mano.** Maximizar `2x + 3y` sujeto a `x + y ≤ 4`, `x + 3y ≤ 6`, `x ≥ 0`,
`y ≥ 0`. Los vértices se obtienen cortando rectas:

- `(0, 0)` → objetivo 0.
- `(4, 0)` → `2·4 + 3·0 = 8`.
- `(0, 2)` → `2·0 + 3·2 = 6`.
- `(3, 1)`, la intersección de `x + y = 4` con `x + 3y = 6` (restando: `2y = 2`, luego `y = 1`
  y `x = 3`) → `2·3 + 3·1 = 9`.

El óptimo es 9 en `(3, 1)`. Ninguna solución del interior puede superarlo: moverse desde un
vértice hacia dentro solo puede empeorar alguna restricción.

**Descenso de gradiente paso a paso.** Minimizar `f(x) = x² − 4x + 1`, cuya derivada es
`2x − 4` y cuyo mínimo está en `x = 2` con `f(2) = −3`. Empezando en `x = 0` con paso `η = 0,3`:

- Paso 1: gradiente `−4`, nuevo `x = 0 − 0,3·(−4) = 1,2`, `f(1,2) = −2,36`.
- Paso 2: gradiente `2·1,2 − 4 = −1,6`, nuevo `x = 1,2 + 0,48 = 1,68`, `f = −2,8976`.
- Paso 5: `x = 1,97952`, `f = −2,999581`.
- Paso 20: `x ≈ 2,000000`, `f ≈ −3,000000`.

Con paso `η = 1,5` el mismo problema oscila entre valores cada vez mayores y no converge: el
paso tiene que ser menor que `2/L`, donde `L` es la curvatura máxima de la función (aquí
`f'' = 2`, así que `η < 1`).

**El gap de integralidad de una mochila.** Tres objetos con pesos `6, 5, 5` y valores `9, 5, 5`,
mochila de capacidad 10. La mejor selección entera es el objeto 1, con valor 9; o los objetos 2
y 3, con valor 10. Óptimo entero: **10**. La relajación lineal puede coger el objeto 1 entero
(peso 6, valor 9) y cuatro quintas partes del objeto 2 (peso 4, valor 4), llegando a **13**. El
gap es `13 / 10 = 1,3`: el solver entero sabe que su solución no puede estar a más de un 30 %
del óptimo, y ese certificado es lo que le permite parar con tranquilidad cuando el gap se
cierra.

## Código

```python verificable
import numpy as np
from scipy.optimize import linprog

# max 2x + 3y  ->  min -2x - 3y   (linprog siempre minimiza)
# x + y <= 4,  x + 3y <= 6,  x >= 0,  y >= 0
res = linprog([-2, -3], A_ub=[[1, 1], [1, 3]], b_ub=[4, 6],
              bounds=[(0, None), (0, None)], method="highs")

print("x, y =", np.round(res.x, 4))       # -> [3. 1.]
print("objetivo =", round(-res.fun, 4))   # -> 9.0
```

:::claves
- `linprog` **minimiza siempre**. Para maximizar hay que negar los coeficientes (`[-2, -3]`) y negar el resultado (`-res.fun`); olvidar el segundo signo da un óptimo correcto con el valor cambiado de signo.
- `res` es un objeto con campos, no una tupla: `res.x` es el vector solución, `res.fun` el valor del objetivo y `res.status` el código de salida. Comprueba `res.success` antes de usar `res.x`: si el problema es infactible, `res.x` es `None`.
- `bounds=[(0, None), (0, None)]` es lo que impone `x ≥ 0`. En `linprog` el valor por defecto de `bounds` ya es `(0, None)`, así que las restricciones de no negatividad van implícitas; una variable libre necesita `(None, None)`.
- `res.fun` puede salir como `np.float64`: al imprimirlo con `round(...)` o formatearlo sale un número normal, pero si lo comparas con `==` contra un `float` calculado a mano puedes llevarte una sorpresa por el redondeo binario.
- En el bucle del descenso de gradiente, `x` se reasigna a un `float` nuevo en cada vuelta (`x = x - paso * grad(x)`), no se modifica el original. Si en vez de un número fuera un `np.array`, `x = x - ...` crearía un array nuevo y `x -= ...` escribiría dentro del que ya tienes.
- El `range(1, 21)` hace **20 iteraciones** y el `if iteracion in (1, 2, 5, 20)` imprime solo cuatro. Cambiar el `range` por `range(1, 6)` deja el ejemplo en 5 pasos y el `print` del paso 20 no se ejecuta: el bucle no avisa, simplemente no llega.
:::

```python verificable
# Descenso de gradiente sobre f(x) = x^2 - 4x + 1, minimo en x = 2.
def f(x):
    return x**2 - 4*x + 1


def grad(x):
    return 2*x - 4


x, paso = 0.0, 0.3
for iteracion in range(1, 21):
    x = x - paso * grad(x)
    if iteracion in (1, 2, 5, 20):
        print("paso {:>2}: x = {:+.6f}  f(x) = {:+.6f}".format(iteracion, x, f(x)))

print("optimo teorico: x = 2, f(x) = -3")
# el paso 20 imprime: paso 20: x = +2.000000  f(x) = -3.000000
```

```python verificable
import itertools

pesos = [6, 5, 5]
valores = [9, 5, 5]
capacidad = 10

# Optimo entero por fuerza bruta: solo factible porque hay 3 objetos.
mejor = 0
for r in range(len(pesos) + 1):
    for combo in itertools.combinations(range(len(pesos)), r):
        if sum(pesos[i] for i in combo) <= capacidad:
            mejor = max(mejor, sum(valores[i] for i in combo))

# Relajacion lineal de la mochila: se ordena por valor/peso y se parte el ultimo objeto.
orden = sorted(range(len(pesos)), key=lambda i: valores[i] / pesos[i], reverse=True)
restante, cota = capacidad, 0.0
for i in orden:
    if pesos[i] <= restante:
        restante -= pesos[i]
        cota += valores[i]
    else:
        cota += valores[i] * restante / pesos[i]   # fraccion del objeto que cabe
        break

print("optimo entero:", mejor)                          # -> 10
print("relajacion lineal:", round(cota, 2))             # -> 13.0
print("gap de integralidad:", round(cota / mejor, 2))   # -> 1.3
```

## Errores típicos

- **Usar descenso de gradiente en un problema lineal o entero.** Con `linprog` o un solver MIP
  obtienes el óptimo exacto en menos tiempo. El gradiente se reserva para funciones no lineales
  y, si son convexas, mejor con un método de segundo orden.
- **Redondear la solución de la relajación lineal.** Coger `x = 0,8` de la relajación y
  redondear a 1 puede violar una restricción (solución infactible) o dejar el resultado muy
  lejos del óptimo entero. Redondear no es un método: es una forma de perder la garantía sin
  darte cuenta.
- **Confundir el gap del solver con el gap de integralidad.** El *gap* que reporta un solver
  MIP es la distancia entre su mejor solución encontrada y su cota actual; el gap de
  integralidad es una propiedad de la formulación. Un solver puede reportar gap 0 % en un
  problema con gap de integralidad 1,3 simplemente porque ha cerrado el árbol.
- **Elegir el paso a ojo.** Un `η` fijo y mal elegido hace divergir o arrastrarse. Usa una
  búsqueda de línea, un esquema adaptativo (Adam, RMSProp) o al menos comprueba que `f(x_{t+1})`
  baja en cada iteración.
- **No escalar las variables.** Si una variable está en millones y otra entre 0 y 1, el problema
  está mal condicionado y el gradiente avanza como un borracho. Centra y escala antes de
  optimizar; es la diferencia entre converger en 50 iteraciones o en 50.000.
- **Pedirle a una metaheurística un certificado de optimalidad.** El recocido simulado y los
  algoritmos genéticos devuelven la mejor solución que han encontrado, no la mejor que existe.
  Sirven cuando no hay alternativa, y hay que reportarlos como heurística, con el presupuesto de
  tiempo que se les dio.

:::practica
enunciado: Minimiza f(x) = x² + 2x + 5 con descenso de gradiente desde x = 0 y paso η = 0,25. Calcula las tres primeras iteraciones con el valor de f en cada una y la distancia al óptimo al terminar.
pista: El gradiente es 2x + 2 y el óptimo está donde se anula, en x = −1. Cada iteración resta η multiplicado por el gradiente del punto actual.
solucion: Paso 1: gradiente 2, x = 0 − 0,25 · 2 = −0,5 y f = 4,25. Paso 2: gradiente 1, x = −0,75 y f = 4,0625. Paso 3: gradiente 0,5, x = −0,875 y f = 4,015625. El óptimo es x = −1 con f = 4, así que quedan 0,125 de distancia: con η = 0,25 la distancia se divide por dos en cada paso.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la programación lineal continua se considera «fácil» y la entera «difícil»?
o: Porque la lineal tiene menos variables y la entera más restricciones
o: Porque en la lineal el óptimo está en un vértice del poliedro y se alcanza con el simplex, mientras que exigir integralidad convierte el problema en NP-duro
o: Porque la entera necesita números decimales de más precisión
a: 2
e: La geometría del problema lineal garantiza un óptimo en un vértice y un algoritmo eficaz para encontrarlo. Al exigir valores enteros el conjunto factible deja de ser un poliedro continuo y el problema entra en la clase NP-duro, así que se resuelve con relajaciones y ramificación, sin garantía de tiempo.
:::

:::quiz
p: En una minimización, el óptimo de la relajación lineal de un problema entero es 13 y el mejor entero conocido es 15. ¿Qué significa?
o: Que la solución entera de 15 puede mejorarse como mucho hasta 13, y el gap actual es del 15 %
o: Que la solución entera de 15 es imposible y el óptimo es 13
o: Que la relajación lineal ha dado una solución infactible
a: 1
e: En minimización la relajación da una cota inferior: el óptimo entero está entre 13 y 15. El gap relativo es (15-13)/13, aproximadamente un 15 %, y mide cuánto puede mejorar todavía la mejor solución entera encontrada.
:::

:::trampa
Un descenso de gradiente que «funciona» en un problema no convexo puede estar devolviéndote el
fondo de un valle cualquiera. Antes de fiarte del resultado, repite desde 10 puntos iniciales
distintos: si los óptimos difieren, no tienes el mínimo, tienes un mínimo. Y en redes
neuronales eso es aceptable; en un problema de negocio, no.
:::
