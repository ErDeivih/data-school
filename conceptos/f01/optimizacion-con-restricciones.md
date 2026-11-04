---
id: optimizacion-con-restricciones
titulo: Optimización con restricciones
fase: 1
nivel: avanzado
rutas: [core, quant, ds]
prerequisitos: [derivadas-parciales-y-gradiente, jacobiano-y-hessiano, convexidad]
tags: [optimizacion, lagrange, carteras, kkt]
resumen: Multiplicadores de Lagrange y condiciones KKT: como maximizar o minimizar cuando hay restricciones, y por qué la cartera de maximo Sharpe sale de ahi.
fuentes: ["Boyd y Vandenberghe (2004), 'Convex Optimization'", "Markowitz (1952), 'Portfolio Selection'"]
---

## En una frase

Cuando optimizas con restricciones, los multiplicadores de Lagrange convierten el problema
restringido en uno sin restricciones y, de paso, te dicen cuánto mejora el objetivo si relajas
cada restricción una unidad; las condiciones KKT son el criterio que debe cumplir la solución
cuando las restricciones son desigualdades.

## La idea

Sin restricciones, optimizar es buscar donde el gradiente se anula: si puedes moverte en
cualquier dirección, en el óptimo ninguna dirección mejora. Con restricciones cambia el
argumento. Si estás obligado a moverte sobre una curva o dentro de una región, puede que en el
óptimo el gradiente **no** sea cero: lo que ocurre es que la dirección de mejora está bloqueada
por la restricción.

Piensa en una montaña y una valla circular dentro de la cual debes quedarte. Si el pico está
dentro de la valla, el problema es el de siempre. Pero si el pico está fuera, te pegas a la valla
y el mejor punto es aquel donde caminar a lo largo de la valla ya no te hace subir. En ese punto
el gradiente de la altura apunta directamente hacia fuera de la valla, es decir, es paralelo al
gradiente de la restricción. Esa proporcionalidad es exactamente el multiplicador de Lagrange.

La interpretación económica es la parte que más se usa: el multiplicador mide el **precio
sombra** de la restricción. Si el multiplicador de «riesgo total ≤ 2 %» vale 0,8, significa que
relajar esa restricción en una unidad mejoraría tu objetivo en 0,8 unidades (por ejemplo, 0,8
puntos de Sharpe por cada punto porcentual de riesgo extra). Eso te dice cuánto vale negociar el
límite. En gestión de carteras, la restricción presupuestaria (los pesos suman 1) siempre está
activa, y de ahí sale la conocida fórmula de la cartera de máximo Sharpe.

## Definición formal

**Problema general:**

:::formula
minimizar f(x)   sujeto a   gᵢ(x) ≤ 0   y   hⱼ(x) = 0
:::

- `f` — función objetivo; `x` — vector de variables de decisión.
- `gᵢ(x) ≤ 0` — restricciones de desigualdad (`m` de ellas).
- `hⱼ(x) = 0` — restricciones de igualdad (`p` de ellas).

**Lagrangiano.** Con multiplicadores `λᵢ ≥ 0` para las desigualdades y `νⱼ` de signo libre para
las igualdades:

:::formula
L(x, λ, ν) = f(x) + Σᵢ λᵢ gᵢ(x) + Σⱼ νⱼ hⱼ(x)
:::

- `λᵢ` — multiplicador de la i-ésima desigualdad; debe ser **no negativo**.
- `νⱼ` — multiplicador de la j-ésima igualdad; puede ser positivo o negativo.
- `L` — función auxiliar sin restricciones cuyos puntos estacionarios coinciden con los
  candidatos del problema original.

**Condiciones KKT** (Karush-Kuhn-Tucker). Son necesarias para la optimalidad bajo ciertas
condiciones de regularidad y, si `f` y las `gᵢ` son convexas y las `hⱼ` afines, también son
**suficientes**:

1. **Estacionariedad:** `∇f(x*) + Σᵢ λᵢ ∇gᵢ(x*) + Σⱼ νⱼ ∇hⱼ(x*) = 0`.
2. **Factibilidad primal:** `gᵢ(x*) ≤ 0` y `hⱼ(x*) = 0`.
3. **Factibilidad dual:** `λᵢ ≥ 0`.
4. **Holgura complementaria:** `λᵢ · gᵢ(x*) = 0` para todo `i`.

La cuarta condición es la que se usa en la práctica: dice que si una restricción **no** está
activa (`gᵢ(x*) < 0`, te sobra margen), su multiplicador es cero y no influye; y si el
multiplicador es positivo, la restricción está activa (`gᵢ(x*) = 0`, estás pegado al límite). No
hay término medio.

**Forma matricial del caso clásico.** Para maximizar el [[ratio-de-sharpe|Sharpe]] con
`μ` el vector de retornos esperados y `Σ` la matriz de covarianzas, sujeto a `wᵀ1 = 1`
(la restricción presupuestaria), la solución es proporcional a `Σ⁻¹μ`:

:::formula
w* = Σ⁻¹μ / (1ᵀΣ⁻¹μ)
:::

- `w` — vector de pesos de la cartera; `1` — vector de unos.
- `Σ` — matriz de covarianzas de los retornos; debe ser invertible y definida positiva.
- `μ` — vector de retornos esperados por activo.

:::figura
fichero: restricciones-tangencia-y-precio-sombra
pie: En el panel izquierdo, el óptimo no es donde el gradiente del objetivo se anula, sino donde la curva de nivel roza la restricción: los dos gradientes quedan alineados, y esa proporción es el multiplicador. En el derecho se ve qué significa su valor: la pendiente de la recta tangente, 6, es exactamente lo que mejora el objetivo al relajar la restricción una unidad. Si esa pendiente fuera cero, el límite no te estaría costando nada.
fuente: figuras/optimizacion-con-restricciones-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `f` | Función objetivo que se minimiza | las de la magnitud objetivo | Si deja de ser convexa, KKT solo da candidatos y hay que compararlos todos |
| `x` | Vector de variables de decisión | las de cada variable | Cada variable nueva anade una componente a las condiciones de estacionariedad |
| `gᵢ(x) ≤ 0` | Restricciones de desigualdad | las de cada restricción | Cuantas mas haya, mas multiplicadores que deben salir no negativos |
| `hⱼ(x) = 0` | Restricciones de igualdad | las de cada restricción | Su multiplicador es de signo libre: puede ser positivo o negativo |
| `λᵢ` | Multiplicador de la i-esima desigualdad | unidades de `f` por unidad de la restricción | Es el precio sombra: cuanto vale relajar esa restricción una unidad; debe ser mayor o igual que cero |
| `νⱼ` | Multiplicador de la j-esima igualdad | unidades de `f` por unidad de la restricción | Mide lo que mejora `f` al aflojar la igualdad; sin signo obligado |
| `μ` | Vector de retornos esperados por activo | tanto por uno en el periodo | Al subir un activo, sube su peso relativo: entra mas cantidad de el |
| `Σ` | Matriz de covarianzas de los retornos | retorno al cuadrado | Al subir la covarianza entre dos activos, `Σ⁻¹` se acerca a singular y los pesos se disparan |
| `w` | Pesos de la cartera | fracción del capital, suman 1 | Sin la restricción `wᵀ1 = 1` el problema tiene infinitas soluciones equivalentes |
:::

## Ejemplo

**Caso con igualdad.** Maximiza `Q(x₁, x₂) = x₁ · x₂` sujeto a `x₁ + x₂ = 12`, con `x₁, x₂ ≥ 0`.
El lagrangiano es `L = x₁x₂ + ν(12 − x₁ − x₂)`. Las condiciones son `x₂ = ν`, `x₁ = ν`, luego
`x₁ = x₂` y con la restricción `x₁ = x₂ = 6`. El máximo vale `36`. En los extremos
`x₁ = 0` o `x₂ = 0` el producto es 0, así que el interior gana. El multiplicador vale `ν = 6`:
cada unidad extra de presupuesto (pasar de 12 a 13) aumentaría el producto en aproximadamente 6.

**Caso con desigualdad y KKT.** Minimiza `d(x, y) = x² + y²` (la distancia al origen al cuadrado)
sujeto a `x + y ≥ 4`. Escribimos la restricción como `g(x, y) = 4 − x − y ≤ 0`.

- Estacionariedad: `2x − λ = 0` y `2y − λ = 0`, luego `x = y`.
- Si la restricción no está activa (`x + y > 4`), entonces `λ = 0`, lo que da `x = y = 0`, pero
  `0 + 0 = 0 < 4` incumple la restricción. Contradicción: la restricción debe estar activa.
- Con `x + y = 4` y `x = y`: `x = y = 2`, `λ = 4`. El punto más cercano es `(2, 2)` a distancia
  `√8 ≈ 2,83`. El multiplicador `λ = 4` significa que relajar la restricción (bajar el 4 a 3)
  reduciría la distancia al cuadrado en unos 4 unidades.

**Cartera de máximo Sharpe.** Dos activos con retornos esperados `μ = (0,10; 0,20)`,
volatilidades `0,15` y `0,25` e independientes (covarianza cero). Entonces `Σ⁻¹μ` tiene
componentes `0,10/0,0225 = 4,4444` y `0,20/0,0625 = 3,2`, que suman `7,6444`. Normalizando,
`w = (0,5814; 0,4186)`. El retorno esperado de esa cartera es
`0,5814·0,10 + 0,4186·0,20 = 0,1419`, su volatilidad
`√(0,5814²·0,0225 + 0,4186²·0,0625) = 0,1362` y su Sharpe `0,1419/0,1362 = 1,0414`. El activo con
menos volatilidad recibe más peso aunque el otro tenga más retorno esperado: manda el cociente,
no el retorno.

## Código

```python verificable
import numpy as np

# Cartera de máximo Sharpe con restricción presupuestaria w1 + w2 = 1.
# Caso analítico: w* proporcional a Sigma^-1 mu, normalizado a suma 1.
mu = np.array([0.10, 0.20])
Sigma = np.array([[0.15**2, 0.0], [0.0, 0.25**2]])

z = np.linalg.solve(Sigma, mu)              # Sigma^-1 mu
w = z / z.sum()                             # normalizamos para que los pesos sumen 1

retorno = float(w @ mu)
riesgo = float(np.sqrt(w @ Sigma @ w))
print("pesos            ", np.round(w, 4).tolist())    # salida: [0.5814, 0.4186]
print("retorno cartera  ", round(retorno, 4))          # salida: 0.1419
print("volatilidad      ", round(riesgo, 4))           # salida: 0.1362
print("Sharpe           ", round(retorno / riesgo, 4)) # salida: 1.0414
```

:::claves
- `np.linalg.solve(Sigma, mu)` resuelve el sistema y **no** calcula la inversa. Es mas rapido y mas estable que `np.linalg.inv(Sigma) @ mu`, y da el mismo resultado hasta el ultimo decimal. Explicar la formula como `Σ⁻¹μ` no obliga a invertir nada en el código.
- El orden de los argumentos es `solve(A, b)` para `Ax = b`, es decir `solve(Sigma, mu)`. Si los intercambias, NumPy resuelve otro sistema distinto sin quejarse, y los pesos salen mal sin ningun error.
- `w @ mu` es el **producto escalar** y `w @ Sigma @ w` es la forma cuadrática de la varianza. El operador `@` no es `*`: con `*` NumPy multiplicaria elemento a elemento y la varianza saldria mal (o directamente fallaria por las formas).
- `z / z.sum()` es la restricción presupuestaria en una línea: normaliza para que los pesos sumen 1. Si quitas la normalización, los pesos no suman 1 pero el Sharpe es identico (1,0414), porque el cociente es invariante a escala. Ese es justo el motivo de que la restricción sea necesaria.
- Con covarianza cero, la componente `i` de `Σ⁻¹μ` vale `mu_i / sigma_i²`, es decir el cociente entre retorno y varianza. Por eso el activo de menos volatilidad (0,15) recibe mas peso que el de mas retorno (0,20): manda el cociente, no el retorno.
- `float(w @ mu)` convierte un `np.float64` en `float` de Python. No cambia el número, pero `round()` sobre un `np.float64` puede devolver otro `np.float64` en versiones antiguas, y al imprimirlo se nota.
:::

```python verificable
import numpy as np
from scipy.optimize import minimize

# El mismo problema resuelto con un optimizador numérico: comprobación cruzada.
def sharpe_negativo(w):
    mu = np.array([0.10, 0.20])
    Sigma = np.array([[0.15**2, 0.0], [0.0, 0.25**2]])
    return -float(w @ mu) / float(np.sqrt(w @ Sigma @ w))

restricciones = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
limites = [(0.0, 1.0), (0.0, 1.0)]
resultado = minimize(sharpe_negativo, x0=np.array([0.5, 0.5]),
                     constraints=restricciones, bounds=limites, method="SLSQP")

print("convergio        ", bool(resultado.success))       # salida: True
print("pesos SLSQP      ", np.round(resultado.x, 4).tolist())  # salida: [0.5814, 0.4186]
print("Sharpe SLSQP     ", round(-float(resultado.fun), 4))    # salida: 1.0414
```

## Errores típicos

- **Olvidar el signo de los multiplicadores.** Con restricciones escritas como `g ≤ 0`, el
  multiplicador debe ser `λ ≥ 0` y en el lagrangiano aparece **sumando** `λg`. Cambiar el signo
  da soluciones imposibles que nadie detecta porque el álgebra «sale».
- **Comprobar la holgura complementaria solo en un sentido.** Hay que verificar que
  `λᵢ · gᵢ(x*) = 0` para cada restricción: o la restricción está activa, o el multiplicador es
  cero. Una solución con las dos cosas positivas no es óptima, y es el error más común al
  resolver KKT a mano.
- **Suponer que KKT es suficiente siempre.** Lo es si el problema es convexo (objetivo convexo,
  restricciones de desigualdad convexas y de igualdad afines). Con un objetivo no convexo, KKT
  solo da candidatos: hay que comparar todos los puntos que cumplen las condiciones, incluidos
  los de la frontera.
- **Ignorar los límites del dominio.** Un problema con `w ≥ 0` tiene condiciones KKT extra por
  cada cota. Resolverlo como si no existieran da pesos negativos: matemáticamente válidos,
  financieramente imposibles sin vender en corto.
- **Buscar el máximo Sharpe sin la restricción presupuestaria.** Sin `wᵀ1 = 1`, el cociente es
  invariante a escala y el problema tiene infinitas soluciones equivalentes (o ninguna acotada).
  La restricción no es un adorno: es lo que fija la escala.
- **Usar `Σ` mal condicionada sin regularizar.** Si dos activos están casi perfectamente
  correlacionados, `Σ⁻¹` explota y los pesos salen enormes con signos alternos. En la práctica se
  añade una pequeña penalización (`Σ + εI`) o se imponen cotas.

:::practica
enunciado: Maximiza A(x, y) = x · y sujeto a 2x + y = 10, con x, y ≥ 0. Encuentra los valores de x e y, el máximo y el multiplicador de Lagrange, e interpreta ese multiplicador.
pista: Monta el lagrangiano con la restricción de igualdad y deriva respecto de x, de y y del multiplicador.
solucion: Con L = xy + ν(10 − 2x − y), las condiciones son y = 2ν y x = ν, luego y = 2x. Sustituyendo en 2x + y = 10: 2x + 2x = 10, de donde x = 2,5 e y = 5. El máximo es A = 12,5 y ν = 2,5: relajar la restricción en una unidad mejoraría el producto en unas 2,5 unidades. Como las esquinas (5, 0) y (0, 10) dan A = 0, el óptimo es interior.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa que el multiplicador de Lagrange de una restricción valga 0?
o: Que la restricción no está activa y relajarla no mejoraría el objetivo
o: Que la restricción es imposible de cumplir
o: Que el objetivo tiene un mínimo global en ese punto
a: 1
e: Por holgura complementaria, multiplicador cero y restricción inactiva van juntos: te sobra margen, así que el límite no influye en la solución. Un multiplicador positivo indicaría que la restricción aprieta y que relajarla mejoraría el objetivo.
:::

:::quiz
p: En el problema de minimizar x² + y² sujeto a x + y ≥ 4, ¿cuál es el punto óptimo y por qué?
o: (0, 0), porque es donde el gradiente se anula
o: (2, 2), porque la restricción está activa y por simetría x = y
o: (4, 0), porque está en el extremo de la restricción
a: 2
e: El gradiente se anula en (0,0) pero ese punto incumple la restricción, así que se descarta. Con la restricción activa, x + y = 4, y la estacionariedad obliga a x = y, de donde sale (2,2). En (4,0) la distancia es mayor, así que no es óptimo.
:::

:::quiz
p: ¿Por qué la cartera de máximo Sharpe es proporcional a Σ⁻¹μ y luego se normaliza?
o: Porque el cociente de Sharpe es invariante a escala: hay que fijar la escala con la restricción de que los pesos sumen 1
o: Porque los pesos deben ser siempre positivos
o: Porque Σ⁻¹ no existe si no se normaliza antes
a: 1
e: Multiplicar todos los pesos por una constante deja el Sharpe igual, ya que numerador y denominador escalan igual. La restricción presupuestaria fija la escala y permite hablar de una cartera concreta. La normalización no garantiza pesos positivos: eso requiere la restricción adicional w >= 0.
:::

:::aviso
Los multiplicadores son tan útiles como la solución: son el precio sombra de cada restricción.
Si el multiplicador de tu límite de riesgo es grande, ese límite te está costando rendimiento, y
ese es el argumento cuantitativo para negociar el mandato. Si es cero, el límite no te aprieta y
no tiene sentido pelearlo.
:::
