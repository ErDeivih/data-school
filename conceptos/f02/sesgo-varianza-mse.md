---
id: sesgo-varianza-mse
titulo: Sesgo, varianza y ECM
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [poblacion-y-muestra, valor-esperado]
tags: [machine-learning, error, regularizacion]
resumen: El error que puedes esperar se descompone en ruido irreducible, sesgo al cuadrado y varianza; por eso un modelo algo sesgado puede predecir mejor.
fuentes: ["Geman, Bienenstock y Doursat (1992), 'Neural Networks and the Bias/Variance Dilemma'", "Hastie, Tibshirani y Friedman (2009), 'The Elements of Statistical Learning', cap. 7"]
---

## En una frase

El error esperado de un modelo se descompone en tres piezas que se pelean entre sí: el ruido de
los datos, que no se puede tocar; el sesgo, que baja al complicar el modelo; y la varianza, que
sube al complicarlo. El mejor modelo no es el que menos se equivoca en tus datos, sino el que
equilibra las tres.

## La idea

Imagina que quieres predecir el precio de un piso a partir de los metros cuadrados. Tienes 60
pisos con precios ruidosos: dos pisos idénticos pueden haberse vendido con 15.000 € de diferencia
porque uno tenía mejor orientación, o porque el vendedor tenía prisa. Ese ruido está en los datos
y **ninguna función puede eliminarlo**.

Ahora ajustas dos modelos:

- Una **recta**. Con los datos que tienes, la recta siempre sale parecida: cambia poco si repites
  el muestreo. Pero es rígida, y el precio real por metro cuadrado no es constante (los pisos
  grandes suelen ser más baratos por metro). Se equivoca de forma sistemática: **sesgo alto,
  varianza baja**.
- Una **curva flexible que pasa por los 60 puntos exactos**. En tus datos su error es cero, pero
  si cambias 5 pisos de la muestra la curva se retuerce y predice disparates en los extremos. Ha
  memorizado el ruido: **sesgo bajo, varianza altísima**.

La imagen mental más útil es la del tirador. El **sesgo** es que la diana esté mal centrada; la
**varianza** es que la mano tiemble. Puedes fallar por cualquiera de los dos motivos, y la diana
no te dice cuál de ellos es. Lo que se mide al final es la distancia al centro: el **error
cuadrático medio** (ECM).

El resultado central es que ese ECM esperado es exactamente la suma de las tres piezas. Por eso
existe la [[regularizacion-l1-l2|regularización]]: aceptar un poco de sesgo a cambio de mucha
menos varianza suele salir a cuenta. Y por eso «mi modelo acierta el 100 % en entrenamiento» es
una mala noticia, no una buena.

:::nota
Los libros de estadística clásica llaman a esto **error cuadrático medio de un estimador** y lo
escriben `ECM(θ̂) = Sesgo(θ̂)² + Var(θ̂)`. En machine learning se añade el término del ruido y se
habla de **error esperado de predicción**. Es la misma descomposición con otro envoltorio.
:::

:::figura
fichero: sesgo-varianza-diana-y-descomposicion
pie: En cada diana, la cruz roja es el promedio de los disparos y el centro es el valor verdadero: fallar puede ser apuntar mal (sesgo) o temblar (varianza), y la diana sola no distingue los dos casos. Abajo, la descomposición del ejemplo de k-NN: con k = 1 casi todo el error es varianza, con k = 200 casi todo es sesgo, y el mínimo está en k = 60, no en el extremo más flexible.
fuente: figuras/sesgo-varianza-mse-1.py
:::

## Definición formal

Sea `Y = f(X) + ε` el proceso que genera los datos: `f` es la función verdadera, `X` las
variables de entrada, e `Y` la respuesta observada.

- `f(X)` — valor esperado de `Y` dado `X`, es decir `f(x) = E[Y / X = x]`.
- `ε` — ruido aleatorio con media cero y varianza `σ²`. Es lo que hace que dos observaciones con
  la misma `X` tengan distinta `Y`.
- `D` — el conjunto de entrenamiento, que tratamos como aleatorio: otra muestra daría otro modelo.
- `f̂_D(x)` — la predicción del modelo entrenado con `D` en el punto `x`.
- `E_D[·]` — esperanza sobre todas las muestras de entrenamiento posibles de tamaño `n`.

Para un punto de prueba `x` cualquiera, el error cuadrático medio esperado se descompone así:

:::formula
E_D[(Y − f̂_D(x))²] = σ² + (E_D[f̂_D(x)] − f(x))² + E_D[(f̂_D(x) − E_D[f̂_D(x)])²]
:::

Con nombres, que es como se cita siempre:

:::formula
Error esperado = Ruido + Sesgo² + Varianza
:::

- `σ²` — **ruido irreducible**: varianza del término `ε`. No depende del modelo; solo se reduce
  midiendo mejor o añadiendo variables que expliquen parte de `ε`.
- `E_D[f̂_D(x)] − f(x)` — **sesgo**: cuánto se equivoca tu modelo *de media*, promediando sobre
  todos los entrenamientos posibles. Si vale cero, el modelo es insesgado en ese punto.
- `E_D[(f̂_D(x) − E_D[f̂_D(x)])²]` — **varianza**: cuánto cambia la predicción de un entrenamiento
  a otro. Mide la sensibilidad del modelo a la muestra concreta que le tocó.
- `E_D[(Y − f̂_D(x))²]` — **ECM** (error cuadrático medio): la cantidad que resume todo lo anterior.

La identidad se cumple cruzando los productos porque `ε` tiene media cero y es independiente de
`D`. Para pérdidas 0-1 (clasificación) la descomposición **no es aditiva** y se usa otra variante,
pero la conclusión cualitativa —más flexibilidad, menos sesgo y más varianza— se mantiene.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `f(x)` | Valor esperado de `Y` dado `x`: la función verdadera | las de `Y` | No se estima ni se conoce: es la referencia contra la que se mide el sesgo. En la práctica se sustituye por validación cruzada y muchas muestras |
| `ε` | Ruido aleatorio de los datos, de media cero | las de `Y` | Su varianza `σ²` es el suelo del error. Dos pisos idénticos pueden venderse con 15.000 € de diferencia y ninguna función lo evita |
| `σ²` | Ruido irreducible: la varianza de `ε` | las de `Y` al cuadrado | Sube el suelo del error y ningún modelo lo baja. Si tu error ya está pegado a `σ²`, el problema es de datos o de medida, no de algoritmo |
| `D` | Conjunto de entrenamiento, tratado como aleatorio | — | Al crecer `n` la varianza baja como `1/n` y el sesgo no se mueve. Es la única palanca que reduce las dos cosas sin elegir |
| `f̂_D(x)` | Predicción del modelo entrenado con `D` | las de `Y` | Cambiar `D` cambia la predicción: esa dispersión **es** la varianza. Un modelo flexible la dispara; uno rígido la mantiene pequeña |
| `E_D[·]` | Esperanza sobre todos los entrenamientos posibles | — | Es el promedio sobre modelos, no sobre puntos de datos. Sin ella no se puede separar sesgo de varianza: solo se ve el ECM total |
| `Sesgo²` | `(E_D[f̂_D(x)] − f(x))²`, cuánto falla de media | las de `Y` al cuadrado | Entra al cuadrado, así que un sesgo de 0,1 cuesta 0,01. Baja al complicar el modelo y es lo único que queda cuando el modelo es demasiado rígido |
| `Varianza` | `E_D[(f̂_D(x) − E_D[f̂_D(x)])²]`, cuánto oscila | las de `Y` al cuadrado | Sube con la flexibilidad, con predictores correlacionados y con pocos datos; baja con más filas y con regularización |
| `k` | Vecinos que promedia el modelo k-NN del ejemplo | vecinos | `k` pequeño deja varianza (con `k = 1`, 0,0956 de 0,0960); `k` grande deja sesgo (con `k = 200`, 0,0622 de 0,0626). El mínimo está en medio, cerca de 60 |
:::

## Ejemplo

Con un modelo de vecinos más cercanos (`k`-NN) sobre 200 puntos en `[0, 3]` con
`y = 2 + 0,5·x + ruido(0; 0,3)`, evaluado en `x = 1` (donde el valor verdadero es 2,5), se obtiene
promediando 400 entrenamientos simulados:

| k | error | sesgo² | varianza |
| --- | --- | --- | --- |
| 1 | 0,0960 | 0,0004 | 0,0956 |
| 5 | 0,0176 | 0,0000 | 0,0176 |
| 20 | 0,0047 | 0,0000 | 0,0047 |
| 60 | 0,0014 | 0,0000 | 0,0014 |
| 200 | 0,0626 | 0,0622 | 0,0004 |

Se lee de un vistazo: con `k = 1` el modelo copia el ruido del vecino más cercano y casi todo el
error es varianza (0,0956 de 0,0960). Con `k = 200` promedia toda la rejilla, así que la
predicción es siempre la misma —varianza prácticamente cero— pero se equivoca de forma sistemática
al ignorar que `y` crece con `x` (sesgo² = 0,0622). El mejor está en medio, alrededor de `k = 60`,
con un error de 0,0014: 45 veces menor que con `k = 200` y unas 69 veces menor que con `k = 1`.

En las cinco filas se cumple `sesgo² + varianza = error`, que es la identidad de la definición
comprobada numéricamente. Y el mínimo error posible es el ruido `σ² = 0,09`, pero aquí se mide en
la *media* de `k` vecinos, así que la varianza del ruido baja como `σ²/k`: con `k = 60` el suelo del
error es 0,0015, y el modelo está justo ahí. No queda nada que rascar.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
x_grid = np.linspace(0, 3, 200)

# k vecinos mas cercanos a 1.0 sobre una rejilla densa: el diseno es fijo,
# asi que los vecinos no cambian entre muestras; lo que cambia es el ruido.
distancias = np.abs(x_grid - 1.0)
vecinos = np.argsort(distancias)

print("  k   error   sesgo^2   varianza")
for k in (1, 5, 20, 60, 200):
    predicciones = []
    for _ in range(400):
        y_ruidoso = 2.0 + 0.5 * x_grid + rng.normal(0, 0.3, size=x_grid.size)
        predicciones.append(y_ruidoso[vecinos[:k]].mean())
    predicciones = np.array(predicciones)
    verdadero = 2.0 + 0.5 * 1.0
    error = ((predicciones - verdadero) ** 2).mean()
    print(f"{k:>3}  {error:.4f}  {(predicciones.mean() - verdadero) ** 2:.4f}   {predicciones.var():.4f}")
```

Fíjate en la última fila: `sesgo² + varianza` clava el error en las cinco filas. Esa es la
identidad de la definición, comprobada numéricamente.

:::claves
- `np.argsort(distancias)` devuelve **posiciones**, no valores: por eso después se indexa `y_ruidoso[vecinos[:k]]`. Si indexaras con `np.sort(distancias)` estarías usando distancias como índices y el resultado sería un disparate o un `IndexError`.
- La rejilla `x_grid` es fija y solo se vuelve a sortear el ruido. Eso es lo que hace interpretable el experimento: si en cada réplica cambiaran también los vecinos, la varianza que mides mezclaría el diseño con el ruido.
- `predicciones` empieza siendo una lista de Python y no tiene `.var()` ni `.mean()`. Hasta que no se ejecuta `np.array(predicciones)` (o `np.mean`, que convierte por dentro) no hay vector: el orden de esas dos líneas importa.
- `predicciones.var()` divide entre 400 (ddof = 0). Aquí da igual porque son 400 réplicas de una simulación, pero la misma llamada sobre una muestra de datos es el estimador sesgado que aparece en el bloque siguiente: `.var()` y `.var(ddof=1)` no son dos formas de escribir lo mismo.
- `((predicciones - verdadero) ** 2).mean()` es el ECM de la definición escrito literalmente: media de los cuadrados de los errores. Cambiar `.mean()` por `.sum()` te da la suma de cuadrados, que crece con `k` y no sirve para comparar.
- Cambia el `0.3` de `rng.normal(0, 0.3, ...)` por `0.6` y el error de `k = 1` sube de 0,0960 a casi 0,36: el cuádruple exacto, porque `σ²` pasa de 0,09 a 0,36. Ningún modelo puede bajar de ahí, y esa es la comprobación de que `σ²` es el suelo.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
n, repeticiones, sigma2 = 10, 20000, 4.0

# Dos estimadores de la varianza: dividir por n (sesgado) y por n-1 (insesgado)
m1 = np.empty(repeticiones)
m2 = np.empty(repeticiones)
for i in range(repeticiones):
    muestra = rng.normal(0, np.sqrt(sigma2), size=n)
    m1[i] = muestra.var()             # ddof=0: el MLE, sesgado hacia abajo
    m2[i] = muestra.var(ddof=1)       # ddof=1: el insesgado de Bessel

for nombre, est in (("dividir por n  ", m1), ("dividir por n-1", m2)):
    sesgo = est.mean() - sigma2
    ecm = ((est - sigma2) ** 2).mean()
    print(f"{nombre}  media {est.mean():.3f}  sesgo {sesgo:+.3f}  ECM {ecm:.3f}")
```

El estimador insesgado tiene **más** ECM que el sesgado: 3,530 frente a 3,010, con una varianza
poblacional real de 4. El sesgo de −0,388 del primero se compensa con creces porque también tiene
menos varianza. Es el aviso más importante de esta página: insesgado no es sinónimo de mejor, y
verás esto otra vez en [[estimadores-y-propiedades]] y en la [[regularizacion-l1-l2|regularización]].

## Errores típicos

- **Elegir el modelo por su error de entrenamiento.** Un modelo lo bastante flexible memoriza el
  ruido y baja el error de entrenamiento hasta casi cero. Ese número no estima el error esperado
  de la definición, que incluye la varianza. Se evalúa siempre con datos que el modelo no ha visto.
- **Creer que se puede bajar sesgo y varianza a la vez con el mismo movimiento.** Agrandar el
  modelo o quitar regularización baja el sesgo y sube la varianza. Si las dos bajan, no es magia:
  has cambiado los datos (más muestra, mejores variables) o has dejado de estimar lo mismo.
- **Ignorar el ruido irreducible al comparar modelos.** Si `σ²` es grande, dos modelos con ECM
  0,31 y 0,32 pueden ser indistinguibles. Sin una estimación de `σ²`, esas diferencias son ruido.
- **Pensar que el sesgo se mide comparando con los datos.** El sesgo es `E_D[f̂_D(x)] − f(x)`, y
  `f` no la conoces: en la práctica se estima con validación cruzada y muchas muestras, o se
  razona sobre el modelo. Nadie ve el sesgo mirando una sola gráfica de residuos.
- **Extrapolar la descomposición 0-1 tal cual.** En clasificación con pérdida 0-1 el término de
  varianza puede ser negativo en la descomposición clásica, y lo que se usa es la variante
  «sesgo² + varianza + ruido» con una corrección. No mezcles la fórmula de regresión con
  exactitud de clasificación.
- **Aplicar la fórmula punto por punto sin promediar sobre `X`.** El resultado vale para cada `x`;
  el error global es el promedio sobre la distribución de `X`. Un modelo puede tener poco sesgo
  en el centro de los datos y muchísimo en los extremos, donde hay pocos puntos y mucha varianza.

:::truco
Cuando tu modelo va bien en validación y mal en test, o al revés, mira la curva de aprendizaje:
si el error de entrenamiento y el de validación son **ambos altos y cercanos**, tienes sesgo
(modelo demasiado simple); si el de entrenamiento es bajo y el de validación mucho más alto, tienes
varianza (modelo demasiado flexible o pocos datos).
:::

:::practica
enunciado: Tres modelos tienen el mismo ruido irreducible, 0,20, y estos pares (sesgo, varianza): A (0,50; 0,04), B (0,10; 0,25) y C (0; 0,49). Calcula el error esperado de cada uno y decide cuál elegir.
pista: El error esperado es ruido + sesgo² + varianza; el sesgo entra al cuadrado, así que uno pequeño cuesta poco.
solucion: A: 0,20 + 0,50² + 0,04 = 0,20 + 0,25 + 0,04 = 0,49. B: 0,20 + 0,10² + 0,25 = 0,20 + 0,01 + 0,25 = 0,46. C: 0,20 + 0 + 0,49 = 0,69. Gana B, que es el sesgado: el insesgado C paga una varianza mucho mayor. Aceptar un poco de sesgo a cambio de menos varianza es lo que hace la regularización.
:::

## Comprueba que lo sabes

:::quiz
p: El error esperado de predicción de un modelo se descompone en tres términos. ¿Cuáles?
o: Sesgo, varianza y ruido irreducible
o: Error de entrenamiento, error de validación y error de test
o: Precisión, exhaustividad y F1
a: 1
e: La descomposición es E[(Y − f̂(x))²] = σ² + sesgo² + varianza. Los otros dos conjuntos son formas de medir o repartir los datos, no componentes del error esperado.
:::

:::quiz
p: Un modelo de vecinos más cercanos con k = 1 da un error de entrenamiento casi nulo pero un error de test alto. ¿Qué componente domina?
o: El ruido irreducible, porque los datos son ruidosos
o: La varianza, porque la predicción depende de un solo punto y cambia mucho de una muestra a otra
o: El sesgo, porque el modelo es demasiado rígido
a: 2
e: Con k = 1 el modelo copia el ruido local: en cada muestra distinta los vecinos son otros y la predicción se mueve. El sesgo es casi nulo y el ruido irreducible es el mismo para todos los modelos; lo que se dispara es la varianza.
:::

:::quiz
p: ¿Por qué un estimador insesgado puede tener más error cuadrático medio que uno sesgado?
o: Porque el ECM solo depende del sesgo en muestras pequeñas
o: Porque ECM = sesgo² + varianza, y reducir sesgo a cero puede costar mucha más varianza de lo que se gana
o: Porque la insesgadez solo se define para muestras grandes
a: 2
e: El ECM suma las dos piezas. El estimador insesgado de la varianza tiene ECM 3,530 frente a 3,010 del sesgado con la misma varianza poblacional. Aceptar un poco de sesgo a cambio de menos varianza es exactamente lo que hace la regularización.
:::

:::aviso
El error de test que mides es **una** realización del error esperado, con su propia incertidumbre.
Con 200 observaciones de test, la diferencia entre dos modelos solo es creíble si supera varias
veces el error típico de la métrica. Comparar modelos por la tercera cifra decimal con un test
pequeño es leer ruido.
:::
