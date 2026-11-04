---
id: ley-de-los-grandes-numeros
titulo: Ley de los grandes números
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [valor-esperado, varianza-y-desviacion, distribuciones-discretas]
tags: [probabilidad, convergencia, muestreo]
resumen: Por qué la media muestral acaba pareciéndose al valor esperado, por qué tarda tanto en parecerse y por qué no significa que las rachas se compensen.
fuentes: ["Billingsley (1995), 'Probability and Measure'", "Casella y Berger (2002), 'Statistical Inference'"]
---

## En una frase

Si repites un experimento muchas veces de forma independiente, la media de los resultados se
acerca al valor esperado; la ley garantiza el límite, no la velocidad ni el camino.

## La idea

El casino no necesita ganar cada mano. Con la ventaja a su favor y miles de manos al día, la
ganancia media por mano se pega a su valor esperado como una lapa. Esa es toda la ley: la
**media de muchas observaciones independientes converge a la esperanza**. El casino no predice
la próxima tirada; se apoya en el promedio de un millón.

Y ahí empieza el malentendido más famoso de la probabilidad. Si han salido cinco caras
seguidas, mucha gente dice «ahora toca cruz». No toca nada: la moneda no tiene memoria. Lo que
ocurre es más sutil: la **proporción** de caras se acerca a 0,5 no porque las diferencias se
compensen, sino porque el denominador crece. De hecho, la diferencia entre el número de caras y
el de cruces tiende a **aumentar**, del orden de `√n`: tras 10.000 tiradas, una diferencia de
100 (un 1 % del total) es lo normal; tras 100 tiradas, sería una diferencia de 10 (un 10 %).
Las rachas no se compensan; se diluyen.

La segunda cosa que la ley no dice es **cuánto tarda**. La desviación típica de la media
muestral es `σ/√n`, así que el error baja con la raíz del tamaño: para reducir el error a la
mitad necesitas **cuatro veces** más datos, y para reducirlo diez veces, cien veces más datos.
Esa lentitud es la razón de que un test A/B con 200 visitas no distinga casi nada y de que
muchos backtests con pocas operaciones estén dominados por el ruido.

La tercera advertencia es el sesgo. La ley habla de la media de la muestra que tienes, no de la
población que te interesa. Si tu muestra está sesgada (encuestas solo por teléfono fijo, datos
solo de clientes que se quedaron, precios solo de operaciones ejecutadas), la media converge
con toda tranquilidad… al valor equivocado. Más datos no arreglan un sesgo de selección; lo
hacen más preciso y más difícil de discutir.

Por último, hay dos versiones de la ley. La **débil** dice que, para un tamaño `n` grande, es
muy improbable que la media esté lejos de `μ`. La **fuerte** dice algo más ambicioso: que la
sucesión completa converge a `μ` con probabilidad 1. Para trabajar, la débil suele bastar; la
fuerte es la que justifica frases como «a la larga, la media es `μ`».

## Definición formal

Sean `X₁, X₂, …, Xₙ` variables **iid** (independientes e idénticamente distribuidas), con media
`μ = E[Xᵢ]` y varianza finita `σ² = Var(Xᵢ)`. La media muestral es
`X̄ₙ = (1/n)·Σᵢ Xᵢ`.

- **Ley débil.** Para cualquier `ε > 0`, `P(|X̄ₙ − μ| ≥ ε) → 0` cuando `n → ∞`. Se dice que
  `X̄ₙ` converge **en probabilidad** a `μ`.
- **Ley fuerte.** `P(lim X̄ₙ = μ) = 1`. La sucesión entera converge a `μ` salvo en un conjunto
  de probabilidad cero.
- **Desigualdad de Chebyshev.** `P(|X̄ₙ − μ| ≥ ε) ≤ σ²/(n·ε²)`. Da una cota explícita y sin
  supuestos sobre la forma de la distribución, pero solo exige varianza finita, así que suele
  ser muy conservadora.
- **Velocidad.** El error típico de la media es `σ/√n`. Para pasar de `n` a `4n` se reduce a la
  mitad; para dividirlo entre 10, `n` se multiplica por 100.

Los símbolos: `X̄ₙ` es la media de las primeras `n` observaciones, `μ` la esperanza (el límite),
`σ²` la varianza de cada observación, `ε` la distancia a `μ` que consideras «lejos», y `Σᵢ`
la suma desde `i = 1` hasta `n`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de observaciones independientes | observaciones | El error típico baja como `1/√n`: multiplicar `n` por 4 divide el error entre 2, y por 100 lo divide entre 10 |
| `μ` | La esperanza de cada observación: el límite al que tiende la media | las de `X` | Desplaza el destino de la media, pero no la velocidad a la que llega |
| `σ²` | La varianza de cada observación | las de `X`, al cuadrado | El error típico sube con `σ`, no con `σ²`: doblar la dispersión dobla el error |
| `X̄ₙ` | La media de las `n` primeras observaciones | las de `X` | Es lo que se mueve; con `n` pequeño puede alejarse de `μ` aunque la ley se cumpla |
| `ε` | La distancia a `μ` que consideras «lejos» | las de `X` | Chebyshev da una cota `σ²/(n·ε²)`: al doblar `ε` la cota se divide entre 4 |
| `σ/√n` | El error típico de la media | las de `X` | Es la unidad con la que se mide todo: comparar una media con `μ` sin dividir por `√n` exagera el error |
:::

Un aviso que la ley no incluye y que la figura deja ver: cada camino es irregular y hay rachas
en las que la media se aleja. Lo que converge es el conjunto, no cada paso.

:::figura
fichero: lgd-media-y-ritmo-de-convergencia
pie: A la izquierda, cinco series de tiradas de un dado: todas acaban pegadas a 3,5, pero ninguna baja de forma ordenada y con pocas tiradas hay medias entre 2 y 4, así que una racha no anticipa la siguiente. A la derecha, la desviación típica de la media en 400 réplicas se pega a la curva `σ/√n` (punteada): al pasar de 100 a 10.000 tiradas el error baja 10 veces, y ese factor 10 cuesta 100 veces más datos, que es la razón de que la precisión sea cara.
fuente: figuras/ley-de-los-grandes-numeros-1.py
:::

**Condiciones que no se pueden saltar.** Hace falta que la esperanza exista (la Cauchy no la
tiene) y que las observaciones no estén fuertemente correlacionadas. Con datos dependientes,
`X̄ₙ` puede no converger a `μ`, y aunque converja, su varianza no es `σ²/n`: con
autocorrelación positiva, la varianza efectiva es mayor y el error típico de `σ/√n` miente por
optimista.

## Ejemplo

Simulación de tiradas de un dado justo, donde `μ = 3,5` y `σ² = 35/12 ≈ 2,9167`:

```
n = 10       media = 2,8000    error = 0,7000
n = 100      media = 3,6700    error = 0,1700
n = 1000     media = 3,5740    error = 0,0740
n = 100000   media = 3,4985    error = 0,0015
```

Con estos datos el error baja de forma ordenada, pero eso no está garantizado: la convergencia es del límite, no de cada paso, y con otro camino perfectamente válido el error de `n = 100` puede salir mayor que el de `n = 10`.

**La cota frente a la realidad.** Un dado tiene `σ² = 2,9167`. Con `ε = 0,5` y `n = 100`,
Chebyshev dice que la probabilidad de que la media se aleje 0,5 o más no pasa de
`2,9167/(100·0,25) = 0,1167`. En 2.000 réplicas simuladas la frecuencia real fue 0,0030: la
cota es cierta, pero 39 veces más pesimista que la realidad. Sirve para demostrar la ley, no
para calcular probabilidades.

**La lentitud.** La desviación típica de las medias fue 0,1750 con `n = 100`, frente al valor
teórico `√(2,9167/100) = 0,1708`. Para bajarla a 0,017 habría que multiplicar el tamaño de
muestra por 100, hasta `n = 10.000`. Diez veces menos error cuesta cien veces más datos.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)          # semilla fija: el resultado se repite igual
medias = {n: rng.integers(1, 7, size=n).mean() for n in (10, 100, 1000, 100000)}
for n, m in medias.items():
    print(f"n={n:>6}  media = {m:.4f}  error = {abs(m - 3.5):.4f}")

# El error baja con el tamano de la muestra, pero no de forma garantizada en cada camino:
# la ley habla del limite, no de cada paso.
print(f"error con n = 10     = {abs(medias[10] - 3.5):.4f}")      # -> 0.7000
print(f"error con n = 100000 = {abs(medias[100000] - 3.5):.4f}")  # -> 0.0015
```

:::claves
- `rng.integers(1, 7, size=n)` sortea enteros entre 1 y 6, **sin incluir el 7**: el límite superior de `integers` está excluido, igual que en `np.random.randint(1, 7)`. Escribir `integers(1, 6)` daría un dado trucado y el resultado del ejemplo ya no cuadraría.
- `rng.integers(1, 7, size=(2000, n))` construye una matriz de 2.000 filas por 100 columnas, y `.mean(axis=1)` promedia **cada fila**, es decir cada muestra. Con `axis=0` promediarías cada columna y obtendrías 100 medias de 2.000 tiradas: el error típico parecería mucho menor y la conclusión, falsa.
- `medias.std(ddof=1)` estima la dispersión de las medias muestrales a partir de las 2.000 réplicas. `np.std` sin `ddof` divide entre `n` y da un valor algo menor: con 2.000 réplicas la diferencia es pequeña, pero el argumento no es cosmético, es la diferencia entre estimar y describir.
- `np.abs(medias - 3.5) >= eps` devuelve un array de booleanos, y `.mean()` sobre booleanos cuenta la proporción de verdaderos. Funciona porque `True` vale 1: no hace falta ningún bucle ni `sum()/len()`.
- La cota de Chebyshev `2,9167/(100·0,25) = 0,1167` es 39 veces la frecuencia real del ejemplo (0,0030). La cota es cierta y no se puede mejorar sin supuestos: no sirve para calcular probabilidades, solo para demostrar la convergencia.
- El diccionario `{n: ... for n in (10, 100, 1000, 100000)}` reutiliza el mismo generador `rng` en las cuatro ramas, así que los datos de `n = 100` no son los mismos que los de `n = 1000` ni contienen a los anteriores. Si quieres series anidadas (la media de los primeros 10 dentro de la de 100), hay que generar una sola tirada larga y hacer medias acumuladas.
:::

```python verificable
import numpy as np

# Cota de Chebyshev para la media de 100 tiradas de un dado: sigma^2 / (n * eps^2)
sigma2, eps, n = 35 / 12, 0.5, 100
print(f"cota de Chebyshev = {sigma2 / (n * eps ** 2):.4f}")   # -> 0.1167

# Frecuencia real de alejarse 0,5 o mas, con 2000 muestras de tamano 100
rng = np.random.default_rng(1)
medias = rng.integers(1, 7, size=(2000, n)).mean(axis=1)
print(f"frecuencia real   = {(np.abs(medias - 3.5) >= eps).mean():.4f}")  # -> 0.0030

# El error tipico baja como 1/sqrt(n): 10 veces menos error cuesta 100 veces mas datos
print(f"sd de las medias  = {medias.std(ddof=1):.4f}")     # -> 0.1750
print(f"teorico sqrt(s2/n) = {np.sqrt(sigma2 / n):.4f}")   # -> 0.1708
```

## Errores típicos

- **Creer que las rachas se compensan.** «Han salido cinco caras, ahora toca cruz» es la
  falacia del jugador. La proporción converge porque crece el denominador; la diferencia
  absoluta entre caras y cruces tiende a crecer como `√n`.
- **Aplicarla a datos dependientes.** En una serie temporal con autocorrelación, la media no
  converge a la esperanza con error `σ/√n`. Si tu serie tiene memoria, el error típico real es
  mayor y hay que estimarlo con métodos específicos, no dividiendo entre `√n`.
- **Confundirla con el teorema central del límite.** La ley dice **a dónde** va la media (a `μ`);
  el [[teorema-central-del-limite|teorema central del límite]] dice **cómo se distribuye** la
  media alrededor de `μ` (aproximadamente normal). Son dos resultados distintos y
  complementarios.
- **Suponer que más datos es siempre más precisión.** La ganancia va con `√n`: pasar de 1.000 a
  100.000 registros reduce el error típico diez veces, no cien. Si el coste de los datos es
  alto, casi siempre compensa más mejorar la calidad o reducir el sesgo.
- **Olvidar el sesgo de selección.** La ley no distingue una muestra representativa de una
  sesgada: en la sesgada, la media converge al valor equivocado con toda la precisión del mundo.
- **Usar Chebyshev como si fuera la probabilidad real.** Es una cota superior válida para
  cualquier distribución con varianza finita, y en la práctica puede ser decenas de veces más
  grande que la probabilidad verdadera. Para cotas ajustadas hacen falta supuestos o el
  [[teorema-central-del-limite|TCL]].

:::practica
enunciado: El tiempo de espera de un servicio tiene σ = 3 minutos. Con 250 clientes medidos, calcula el error típico de la media muestral y decide cuántos clientes harían falta para dejarlo en 0,06 minutos.
pista: El error típico es σ/√n; para el tamaño necesario, despeja n de la igualdad 3/√n = 0,06.
solucion: Con n = 250, error típico = 3/√250 = 3/15,8114 = 0,1897 minutos. Para 0,06: √n = 3/0,06 = 50, luego n = 2.500. Conclusión: pasar de 0,1897 a 0,06 (algo más de tres veces menos error) exige multiplicar la muestra por 10, porque la precisión se paga con el cuadrado del tamaño; más datos no arreglan, además, un sesgo de selección en la muestra.
:::

## Comprueba que lo sabes

:::quiz
p: Han salido 5 caras seguidas con una moneda justa. ¿Qué dice la ley de los grandes números?
o: Que la probabilidad de cruz en la siguiente tirada es mayor para compensar
o: Que la proporción de caras se acercará a 0,5 al crecer el número de tiradas, sin que la moneda tenga memoria
o: Que en las próximas 5 tiradas saldrán 5 cruces
a: 2
e: La ley describe el comportamiento de la media de muchas tiradas, no de la siguiente. La proporción converge porque el número de tiradas crece, no porque las diferencias se cancelen: de hecho, la diferencia absoluta entre caras y cruces tiende a crecer con la raíz de n.
:::

:::quiz
p: Quieres reducir a la mitad el error típico de tu media muestral. ¿Cuántos datos necesitas?
o: El doble
o: Cuatro veces más
o: La mitad
a: 2
e: El error típico es sigma/raíz de n. Para que la raíz se reduzca a la mitad, n tiene que multiplicarse por 4. Es la razón de que mejorar la precisión sea tan caro y de que convenga más atacar el sesgo y la calidad del dato.
:::

:::quiz
p: ¿Cuál es la diferencia entre la ley de los grandes números y el teorema central del límite?
o: La ley dice a qué valor converge la media; el TCL describe cómo se distribuye alrededor de ese valor
o: La ley vale para variables discretas y el TCL para continuas
o: Son el mismo resultado con dos nombres
a: 1
e: La ley de los grandes números garantiza la convergencia de la media muestral a la esperanza. El teorema central del límite añade la forma de la distribución del error: al estandarizar la media, se parece a una normal, y de ahí salen los errores típicos y los intervalos de confianza.
:::
