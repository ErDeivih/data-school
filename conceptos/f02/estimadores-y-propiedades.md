---
id: estimadores-y-propiedades
titulo: Estimadores y sus propiedades
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [poblacion-y-muestra, sesgo-varianza-mse, valor-esperado]
tags: [inferencia, estimacion, propiedades]
resumen: Insesgado, consistente, eficiente y suficiente: lo que hace útil a un estimador y por qué el mejor no siempre es el insesgado.
fuentes: ["Lehmann y Casella (1998), 'Theory of Point Estimation'", "Casella y Berger (2002), 'Statistical Inference', cap. 7"]
---

## En una frase

Un **estimador** es la receta que convierte tu muestra en un número; sus propiedades —insesgadez,
consistencia, eficiencia y suficiencia— dicen cómo se comporta esa receta si la repitieras mil
veces, y ninguna de ellas se puede comprobar mirando una sola estimación.

## La idea

Piensa en una báscula. La **estimación** es lo que marca hoy con tu saco de patatas encima: un
número, 10,3 kg. El **estimador** es la báscula entera: el aparato que, con cualquier saco, te da
un número. Que hoy marque 10,3 kg no te dice nada sobre si la báscula es buena; para eso hay que
pesar diez sacos de peso conocido y ver qué hace.

Con los estimadores pasa igual, y de ahí salen las cuatro propiedades que importan:

- **Insesgado**: si repitieras el muestreo infinitas veces, el promedio de tus estimaciones sería
  el parámetro. Una báscula insesgada no se desvía siempre hacia arriba; puede fallar hoy arriba y
  mañana abajo, pero no tiene un sesgo fijo.
- **Consistente**: al crecer la muestra, la estimación se pega al parámetro. Es lo mínimo
  exigible: una báscula que sigue desviándose igual con 10 sacos que con 10.000 no sirve.
- **Eficiente**: entre los estimadores insesgados, el que tiene menos varianza. Dos básculas
  insesgadas, pero una tiembla el doble: la que tiembla menos es más eficiente.
- **Suficiente**: el estimador aprovecha toda la información relevante de la muestra sobre el
  parámetro. Si te doy la media de 100 observaciones normales, saber los 100 valores uno a uno no
  te añade nada sobre `μ`.

La jerarquía práctica es esta: un estimador sesgado pero consistente suele ser útil (el sesgo se
va con `n`, como en el [[sesgo-varianza-mse|MLE de la varianza]]); un estimador eficiente con
pocos datos puede ser peor en la práctica que uno algo sesgado con menos varianza; y un estimador
sesgado pero consistente que además tiene menos ECM es lo que usamos todos los días cuando
regularizamos.

Hay un matiz que separa a quien entiende esto de quien lo recita: **insesgado no es una propiedad
del número que tienes delante**. Es una propiedad de la distribución del estimador sobre todas las
muestras posibles. Cuando alguien dice «mi estimación es insesgada», está diciendo algo sobre su
procedimiento, no sobre su resultado.

:::figura
fichero: estimadores-media-y-mediana
pie: Con datos normales las dos distribuciones están centradas en 0 —las dos son insesgadas— pero la de la mediana es más ancha: la media tiene menos varianza, o sea es más eficiente. Con una Cauchy se invierte: la media se escapa del dibujo en un 17 % de las muestras y la mediana sigue concentrada. La forma de la población decide qué estimador conviene, no basta con que sea insesgado.
fuente: figuras/estimadores-y-propiedades-1.py
:::

## Definición formal

Sea `X = (X₁, …, Xₙ)` una muestra aleatoria de una población con parámetro `θ`.

- `θ` — el **parámetro**: un número fijo y desconocido de la población (una media `μ`, una
  proporción `p`, una varianza `σ²`).
- `θ̂ = T(X₁, …, Xₙ)` — el **estimador**: una función de la muestra. Es una variable aleatoria,
  porque la muestra lo es.
- `θ̂(x₁, …, xₙ)` — la **estimación**: el valor concreto que sale con tus datos. Es un número.
- `E[θ̂]` y `Var(θ̂)` — media y varianza del estimador sobre todas las muestras posibles.
- `ECM(θ̂) = E[(θ̂ − θ)²]` — error cuadrático medio, definido en [[sesgo-varianza-mse]].

Las cuatro propiedades, en fórmula:

:::formula
Insesgado: E[θ̂] = θ    ·    ECM(θ̂) = Sesgo(θ̂)² + Var(θ̂)
:::

:::formula
Consistente: θ̂ → θ en probabilidad cuando n → ∞
:::

- **Insesgado** significa que el centro de la distribución del estimador cae sobre el parámetro.
- **Consistente** se cumple, por la [[ley-de-los-grandes-numeros|ley de los grandes números]], si
  el sesgo y la varianza tienden a cero con `n`. Un estimador insesgado con varianza que no baja
  no es consistente.
- **Eficiente** se define por comparación: `θ̂₁` es más eficiente que `θ̂₂` si ambos son insesgados
  y `Var(θ̂₁) < Var(θ̂₂)` para todo `θ`. La **cota de Cramér-Rao** da el mínimo alcanzable por
  cualquier estimador insesgado, `1 / (n · I(θ))`, donde `I(θ)` es la información de Fisher de una
  observación.
- **Suficiente**: `T` lo es si la distribución condicional de la muestra dado `T` no depende de
  `θ`. En la práctica, el criterio de factorización de Fisher-Neyman: la verosimilitud se puede
  escribir como `L(θ) = g(T, θ) · h(x)`.

Un detalle que se olvida: **la insesgadez no se conserva al transformar**. Si `θ̂` es insesgado
para `θ`, entonces `1/θ̂` no es insesgado para `1/θ`, ni `θ̂²` lo es para `θ²`. Y por eso la
desviación típica muestral `s` (raíz de la varianza insesgada) es ligeramente sesgada hacia abajo
como estimador de `σ`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `θ` | Parámetro de la población: media, proporción o varianza | las de la variable | Es fijo y desconocido, así que no sube ni baja. Todo lo que se predica de insesgadez o eficiencia es del estimador, nunca de él |
| `θ̂ = T(X₁, …, Xₙ)` | El estimador: una función de la muestra | las de `θ` | Cambiar `T` lo cambia todo. Dos estimadores distintos sobre los mismos datos dan números distintos, y esa elección es la que se discute en esta página |
| `θ̂(x₁, …, xₙ)` | La estimación: el número que sale con tus datos | las de `θ` | Es un valor, no una propiedad: `x̄ = 3,2` no es insesgado ni deja de serlo. Solo el procedimiento que lo produjo lo es |
| `E[θ̂]` | Media del estimador sobre todas las muestras posibles | las de `θ` | Si coincide con `θ` el estimador es insesgado. La diferencia es el sesgo, y con 20.000 réplicas del ejemplo se estima bien porque el error de Monte Carlo baja como `1/√repeticiones` |
| `Var(θ̂)` | Dispersión del estimador entre muestras | (unidades de `θ`)² | Baja como `1/n`. Entre dos insesgados, el de menos varianza es el más eficiente; con colas gruesas puede ser infinita y entonces la insesgadez no vale nada |
| `ECM(θ̂)` | `E[(θ̂ − θ)²]`, el error cuadrático medio | (unidades de `θ`)² | Es `sesgo² + varianza` y es lo que se compara de verdad: en el ejemplo, el insesgado tiene ECM 3,530 y el sesgado 3,010, así que gana el sesgado |
| `n` | Tamaño de la muestra | observaciones | Es lo que da la consistencia: al crecer, sesgo y varianza tienden a cero y `θ̂` se pega a `θ`. Con `n = 10` el sesgo de dividir entre `n` es un 10 % de `σ²`; con `n = 5`, un 20 % |
| `I(θ)` | Información de Fisher de una observación | — | La cota de Cramér-Rao es `1/(n·I(θ))`: cuanto más información, menos varianza puede tener cualquier estimador insesgado. Es un suelo, no una garantía de alcanzarlo |
:::

## Ejemplo

El estimador de la varianza con `n` en el denominador tiene un sesgo exacto y calculable:
`E[s²ₙ] = σ²·(n − 1)/n`, es decir `Sesgo = −σ²/n`.

Con `n = 10` y `σ² = 4`:

- El estimador sesgado promedia `4 · 9/10 = 3,6`. Su sesgo es `−0,4`.
- El de Bessel (dividir por `n − 1`) promedia exactamente 4. Su sesgo es 0.
- Simulando 20.000 muestras con esos parámetros salen medias de **3,612** y **4,013**: coinciden
  con la teoría dentro del error de Monte Carlo.

Y aquí viene lo interesante: en esas mismas 20.000 réplicas, el estimador **sesgado** tiene un ECM
de **3,010** y el insesgado de **3,530**. El sesgado gana como estimador puntual porque su varianza
es menor. Que sea insesgado no lo hace preferible para todos los usos: si vas a sumar 10.000
varianzas, quieres el insesgado; si vas a estimar una sola, el ECM manda.

Segundo ejemplo, la eficiencia. Con 4.000 muestras de 25 observaciones:

- Población normal: varianza de la media **0,1654** y de la mediana **0,2548**. La media es más
  eficiente, como predice la teoría (la media tiene varianza `σ²/n = 4/25 = 0,16`).
- Población de Cauchy (cola larguísima): varianza de la media **6.170** y de la mediana **0,11**.
  La mediana destroza a la media. La media sigue siendo insesgada para el centro de simetría,
  pero su varianza es infinita: insesgadez sin eficiencia no vale nada.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)

# Verdadera varianza poblacional: 4. Se mira que estimador se acerca mas de media.
verdadera_var, repeticiones, tam = 4.0, 20000, 10
sesgados, insesgados = [], []
for _ in range(repeticiones):
    x = rng.normal(0, np.sqrt(verdadera_var), size=tam)
    sesgados.append(x.var())            # divide por n
    insesgados.append(x.var(ddof=1))    # divide por n-1

print(f"dividir por n    media {np.mean(sesgados):.3f}  error {np.mean(sesgados) - verdadera_var:+.3f}")
print(f"dividir por n-1  media {np.mean(insesgados):.3f}  error {np.mean(insesgados) - verdadera_var:+.3f}")

# La correccion de Bessel no sale de la nada: el sesgo exacto es -sigma^2 / n.
print(f"sesgo teorico    {-verdadera_var / tam:.3f}")
```

:::claves
- `x.var()` divide entre `n` y `x.var(ddof=1)` entre `n − 1`: son dos estimadores distintos, no dos formas de escribir lo mismo. El primero subestima `σ²` un `σ²/n` de media, y esa es justo la magnitud que el bloque intenta mostrar.
- En `rng.normal(0, np.sqrt(verdadera_var), size=tam)` el segundo argumento es la **desviación**, no la varianza. Pasar `verdadera_var` sin la raíz convertiría el ejemplo en `σ² = 16` sin dar ningún error: seguiría imprimiendo medias y sesgos, todos mal.
- `sesgados` e `insesgados` son listas de Python; `np.mean(sesgados)` las convierte por dentro. Si las construyeras con `np.append` dentro del bucle, el resultado sería idéntico y tardaría muchísimo más: añadir a una lista y convertir al final es lo barato.
- Lo que se imprime es `np.mean(sesgados) - verdadera_var`, la media de 20.000 réplicas menos el parámetro. Sale 3,612 frente a los 3,6 teóricos: esa diferencia no es sesgo, es ruido de Monte Carlo, y encoge como `1/√20000`.
- `-verdadera_var / tam` es el sesgo teórico exacto `−σ²/n`. Comparar el número medido con el teórico es la única forma de distinguir «la simulación confirma la teoría» de «la simulación tiene un error de signo o de escala».
- Los dos bloques de la página arrancan con `np.random.default_rng(0)`: la misma semilla. Eso hace que el segundo bloque repita la misma secuencia de números que el primero, lo cual es cómodo para comparar y una trampa si esperabas dos experimentos independientes.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)

# Dos predictores casi identicos (correlacion 0,99) y 20 observaciones:
# el diseno esta mal condicionado y OLS paga por ello con enorme varianza.
n = 20
z = rng.normal(0, 1, size=n)
X = np.column_stack([z, z + 0.2 * rng.normal(0, 1, size=n)])
X = (X - X.mean(axis=0)) / X.std(axis=0)      # centradas y con suma de cuadrados 1

beta_real = np.array([1.5, -0.8])
XtX = X.T @ X
lam = 0.5

ols, ridge = [], []
for _ in range(2000):
    y = X @ beta_real + rng.normal(0, 1.0, size=n)
    Xty = X.T @ y
    ols.append(np.linalg.solve(XtX, Xty))
    ridge.append(np.linalg.solve(XtX + lam * np.eye(2), Xty))
ols, ridge = np.array(ols), np.array(ridge)

print(f"correlacion entre predictores {np.corrcoef(X[:, 0], X[:, 1])[0, 1]:.2f}")
print(f"OLS    media {np.round(ols.mean(axis=0), 3)}  desv tipica {np.round(ols.std(axis=0), 3)}")
print(f"ridge  media {np.round(ridge.mean(axis=0), 3)}  desv tipica {np.round(ridge.std(axis=0), 3)}")
print(f"OLS    ECM {np.mean(np.sum((ols - beta_real) ** 2, axis=1)):.4f}")
print(f"ridge  ECM {np.mean(np.sum((ridge - beta_real) ** 2, axis=1)):.4f}")
```

Los dos estimadores son consistentes, pero solo OLS es insesgado: promedia 1,472 y −0,772 frente
a los valores reales 1,5 y −0,8. El precio de esa insesgadez es una desviación típica de 1,348
frente a 0,474 del estimador con penalización. El resultado final es que el sesgado tiene menos de
la mitad de ECM: **1,6200 frente a 3,6481**. Sin [[regularizacion-l1-l2|regularización]], con
predictores correlacionados, la insesgadez es un lujo caro.

## Errores típicos

- **Decir que una estimación concreta es insesgada.** La insesgadez es una propiedad de la
  distribución del estimador, no del número. `x̄ = 3,2` no es insesgado ni deja de serlo: lo es el
  procedimiento que lo produjo.
- **Confundir consistente con insesgado.** Un estimador puede ser consistente y sesgado (el MLE de
  la varianza) o insesgado y no consistente. Son propiedades independientes y se demuestran por
  separado.
- **Elegir siempre el insesgado.** La insesgadez es una virtud entre varias. Si el insesgado tiene
  mucha más varianza, el sesgado gana en ECM, y en predicción lo que importa es el ECM.
- **Aplicar una transformación y suponer que la insesgadez se mantiene.** `s` no es insesgado para
  `σ` aunque `s²` lo sea para `σ²`; `1/x̄` no es insesgado para `1/μ`. Si necesitas insesgadez tras
  transformar, hay que corregirla (por ejemplo, el factor `c₄` para `s`).
- **Ignorar la eficiencia al comparar dos estimadores con datos escasos.** La media y la mediana
  son ambas insesgadas para el centro de una distribución simétrica, pero con 25 observaciones
  normales la mediana tiene un 54 % más de varianza. Con colas gruesas se invierte. La forma de la
  distribución decide.
- **Creer que el estimador insesgado de varianza mínima existe siempre.** Fuera de las familias
  exponenciales puede no existir, y muchas veces hay que elegir entre sesgo y varianza sin una
  respuesta única. La cota de Cramér-Rao da el suelo solo para insesgados y bajo condiciones de
  regularidad.

:::nota
La **suficiencia** es la propiedad más abstracta y la más útil cuando se entiende: dice cuándo
puedes tirar los datos originales sin perder información sobre el parámetro. Para una normal, `x̄`
y `s²` son conjuntamente suficientes para `(μ, σ²)`; para una Bernoulli, basta con el número de
éxitos. Si un estimador no es suficiente, está desperdiciando información de la muestra.
:::

:::practica
enunciado: Con 25 observaciones normales, la varianza de la media muestral es 0,1654 y la de la mediana 0,2548. Decide cuál es más eficiente, calcula la varianza extra de la otra y cuántas observaciones necesitaría para empatar.
pista: Entre estimadores insesgados, el más eficiente es el de menos varianza, y la varianza cae como 1/n.
solucion: La media, con 0,1654 < 0,2548. El cociente es 0,2548/0,1654 = 1,54: la mediana tiene un 54 % más de varianza, así que necesita 25 · 1,54 ≈ 39 observaciones para igualar lo que la media consigue con 25. Las dos son insesgadas para el centro de una normal; la eficiencia es lo que las separa.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia entre un estimador y una estimación?
o: El estimador es una función de la muestra (variable aleatoria) y la estimación es el valor concreto que sale con tus datos
o: Son sinónimos; solo cambia el contexto en el que se usa la palabra
o: El estimador se usa en poblaciones finitas y la estimación en infinitas
a: 1
e: El estimador es el procedimiento T(X) y tiene distribución, media y varianza; la estimación es T(x), un número. Las propiedades de insesgadez y eficiencia se predican del estimador, nunca de la estimación concreta.
:::

:::quiz
p: Un estimador insesgado tiene varianza 9 y otro sesgado tiene sesgo 1,5 y varianza 1. ¿Cuál tiene menor ECM?
o: El insesgado, porque su sesgo es cero
o: El sesgado, con ECM 3,25 frente a 9
o: Los dos igual, porque el sesgo se cancela con la varianza
a: 2
e: ECM = sesgo² + varianza: para el insesgado es 0 + 9 = 9; para el sesgado, 1,5² + 1 = 3,25. El sesgado gana con claridad, que es exactamente el argumento a favor de la regularización.
:::

:::quiz
p: Con una población de cola muy larga (Cauchy), ¿qué estimador del centro es preferible y por qué?
o: La media, porque siempre es insesgada
o: La mediana, porque la varianza de la media es enorme (o infinita) mientras la de la mediana se mantiene
o: Los dos son equivalentes en cualquier distribución simétrica
a: 2
e: En la simulación con 4.000 muestras de 25 observaciones, la varianza de la media fue 6.170 frente a 0,11 de la mediana. La media sigue siendo insesgada para el centro de simetría, pero su enorme varianza la hace inservible: la insesgadez sola no basta.
:::
