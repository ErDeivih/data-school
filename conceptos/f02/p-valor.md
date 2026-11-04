---
id: p-valor
titulo: El p-valor
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, probabilidad-condicional, distribuciones-continuas]
tags: [inferencia, p-valor, replicacion]
resumen: La probabilidad de ver un resultado al menos tan extremo como el observado si la nula fuera cierta; no es la probabilidad de que la nula sea verdadera.
fuentes: ["Wasserstein y Lazar (2016), 'The ASA Statement on p-Values: Context, Process, and Purpose'", "Colquhoun (2014), 'An Investigation of the False Discovery Rate and the Misinterpretation of p-values'"]
---

## En una frase

El p-valor es la probabilidad de observar un resultado al menos tan extremo como el tuyo **si la
hipótesis nula fuera cierta**; mide cómo de raros son tus datos bajo esa hipótesis, y no dice nada
sobre la probabilidad de que la hipótesis sea verdadera.

## La idea

Imagina que llegas a casa y la puerta está abierta. «La puerta abierta es rarísima si nadie ha
entrado», piensas, y llamas a la policía. Ese razonamiento es un p-valor: has evaluado la
probabilidad de la evidencia **suponiendo** que no pasó nada. Lo que no has calculado es la
probabilidad de que realmente haya entrado alguien, porque para eso hacen falta más cosas: cuánta
gente pasa por tu calle, si tienes gatos, si ayer te dejaste la puerta mal cerrada. El p-valor es
la primera mitad de la historia, y es la mitad que no responde a la pregunta que te interesa.

Esa inversión —confundir «probabilidad de los datos dada la hipótesis» con «probabilidad de la
hipótesis dados los datos»— tiene nombre, falacia del fiscal, y sale directamente del
[[teorema-de-bayes]]. Para pasar de una a otra necesitas la probabilidad previa de la hipótesis, y
el p-valor no la contiene.

La segunda pieza que hay que entender es que **un p-valor pequeño no es raro**. Si la nula fuera
cierta y el estadístico fuera continuo, el p-valor se reparte uniforme entre 0 y 1: un 5 % de las
veces será menor que 0,05 y un 1 % menor que 0,01, con o sin efecto real. Por eso la
frase «p < 0,05, luego hay algo» solo es defendible si el contraste era uno, estaba preinscrito y
no has mirado los datos antes de elegirlo.

La tercera pieza es la que explica la crisis de replicación, y no es una sola causa sino cuatro que
se refuerzan:

- **Multiplicidad.** Si pruebas 20 relaciones y ninguna existe, la probabilidad de que alguna salga
  con `p < 0,05` es `1 − 0,95²⁰ = 0,64`. Casi dos de cada tres.
- **Bifurcaciones de análisis.** Excluir un outlier aquí, añadir una covariable allá, cambiar la
  ventana temporal. Cada decisión razonable por separado multiplica los caminos posibles, y basta
  con quedarse con el que da `p < 0,05`.
- **Sesgo de publicación.** Un resultado con `p = 0,04` se publica; el mismo estudio con `p = 0,12`
  se queda en un cajón. Lo que lees es una muestra
  sesgada hacia los positivos, no una muestra aleatoria de los estudios.
- **Potencia baja.** En un estudio con poca potencia, los pocos resultados que alcanzan
  significación son precisamente los que más exageran el efecto. Es la maldición del ganador
  ([[errores-tipo-i-ii-y-potencia]]).

Lo que toca no es dejar de usar p-valores. Es usarlos sabiendo qué son. Reporta el
tamaño del efecto con su intervalo, di cuántos contrastes hiciste y decide el análisis antes de ver
el resultado.

:::figura
fichero: p-valor-cola-y-uniformidad
pie: A la izquierda, las 20 tiradas del ejemplo: el p-valor es la suma de las barras rojas, es decir, la probabilidad de todo lo que es al menos tan extremo como 15 caras (0,0207 por cola y 0,0414 en bilateral). A la derecha están los mismos contrastes repetidos 5.000 veces: bajo `H₀` los p-valores son planos y un 5,1 % cae por debajo de 0,05 sin que exista ningún efecto, mientras que con un efecto real (curva verde) el 47,5 % se apila a la izquierda del umbral. Compara las dos formas: la altura de la barra roja no es una probabilidad de que la nula sea cierta, es la frecuencia esperada de resultados así cuando la nula lo explica todo.
fuente: figuras/p-valor-1.py
:::

## Definición formal

Para un contraste con estadístico `T`, valor observado `t_obs` e hipótesis nula `H₀`:

- `T` — estadístico de contraste, función de los datos.
- `t_obs` — el valor que toma `T` con los datos que tienes.
- `H₀` — hipótesis nula, con un valor concreto del parámetro.
- `α` — nivel de significación elegido antes de ver los datos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `T` | Estadístico de contraste (una t, una z, un chi-cuadrado) | adimensional si es un cociente | Su valor no decide nada por sí solo: hay que ver cuánto se aleja de lo que se espera bajo `H₀` y con qué dispersión |
| `t_obs` | El valor que toma `T` con tus datos | las de `T` | Cuanto más extremo, menor p. Duplicar la distancia al centro no divide el p-valor entre dos: la cola decrece mucho más deprisa que eso |
| `H₀` | Hipótesis nula, siempre con un valor concreto del parámetro | las del parámetro | Es la única suposición que entra en el cálculo. Si la nula está mal planteada, el p-valor mide con precisión la cosa equivocada |
| `p` | Probabilidad de un resultado al menos tan extremo como el observado, si `H₀` es cierta | entre 0 y 1 | Bajo `H₀` es uniforme, así que un 5 % de los contrastes da p < 0,05 por puro azar. No es la probabilidad de que `H₀` sea verdadera ni la de replicar |
| `α` | Umbral de decisión, fijado antes de ver los datos | tanto por uno (0,05 por costumbre) | Sube → rechazas más y cometes más falsos positivos; baja → rechazas menos y necesitas más muestra para el mismo efecto |
| `n` | Número de observaciones | observaciones | Sube → el mismo efecto produce p-valores más pequeños. Con n enorme, una diferencia irrelevante acaba con p < 0,001 |
| `β`, `1 − β` | Probabilidad de no detectar un efecto real y su complementaria, la potencia | tanto por uno | No salen del p-valor: se calculan en el diseño. Un p-valor de 0,20 no significa «80 % de probabilidad de que no haya efecto» |
:::

:::formula
p = P( T al menos tan extremo como t_obs | H₀ )
:::

«Tan extremo» se define por la alternativa. Si `H₁` es `θ > θ₀`, entonces `p = P(T ≥ t_obs | H₀)`.
Si es bilateral, `p = P( /T/ ≥ /t_obs/ | H₀ )`, es decir, las dos colas.

Un p-valor es **válido** si cumple, para todo `α` entre 0 y 1:

:::formula
P( p ≤ α | H₀ ) ≤ α
:::

De ese reparto sale la propiedad que más cuesta creer y más útil es: con un estadístico continuo y `H₀`
cierta, la desigualdad es una igualdad y el p-valor se distribuye uniforme en `[0, 1]`:

:::formula
p ~ Uniforme(0, 1)   cuando H₀ es cierta
:::

Lo que **no** es el p-valor, en forma de definición:

- No es `P(H₀ | datos)`. Eso es una probabilidad posterior y necesita un prior.
- No es `1 − β`, la probabilidad de detectar un efecto real: eso es la potencia, donde `β` es la
  probabilidad de no detectarlo cuando existe ([[errores-tipo-i-ii-y-potencia]]).
- No es la probabilidad de que el resultado se replique.
- No es el tamaño del efecto ni su importancia práctica.

## Ejemplo

Lanzo una moneda 20 veces y salen 15 caras. La nula es «la moneda es justa», `P(cara) = 0,5`.

- Solo hay 20 tiradas, así que puedo enumerar: `P(X ≥ 15)` suma las probabilidades de 15, 16, 17,
  18, 19 y 20 caras.
- Los coeficientes binomiales son 15.504, 4.845, 1.140, 190, 20 y 1. Suman 21.700 casos favorables
  de los 2²⁰ = 1.048.576 posibles.
- `P(X ≥ 15) = 21.700 / 1.048.576 = 0,0207` (una cola).
- El contraste bilateral duplica esa cola: `p = 0,0414`.

Con `α = 0,05` se rechaza que la moneda sea justa. Pero mira la letra pequeña: he elegido la moneda
**después** de lanzarla, solo tengo 20 tiradas y 15 caras es justo el borde. Si hubiera probado
también un dado, dos barajas y una ruleta, el hallazgo no valdría nada. Y si repitieras el
experimento, la estimación de la probabilidad de cara sería muy inestable: el intervalo del 95 %
para 15 de 20 va de 0,51 a 0,91, un rango enorme.

El segundo cálculo es el que desmonta la lectura ingenua de «p < 0,05, luego es verdad». Supón un
cribado de 200 candidatos: 20 tienen un efecto real y 180 son ruido. El contraste tiene una
potencia del 80 % y usas `α = 0,05`.

- De los 20 reales, detectas el 80 %: **16 aciertos**.
- De los 180 de ruido, se cuelan el 5 %: **9 falsos positivos**.
- Total: 25 hallazgos «significativos», de los cuales 9 son falsos. **El 36 % de tus hallazgos son
  basura**, aunque todos tengan `p < 0,05`.

## Código

```python verificable
from scipy import stats

# 15 caras en 20 lanzamientos: cuanto de raro es si la moneda fuera justa
dos_colas = stats.binomtest(15, 20, p=0.5, alternative="two-sided")
una_cola = stats.binomtest(15, 20, p=0.5, alternative="greater")

print(f"p bilateral  {dos_colas.pvalue:.4f}")   # -> 0.0414
print(f"p unilateral {una_cola.pvalue:.4f}")    # -> 0.0207
print(f"casos con 15 o mas caras: {stats.binom.sf(14, 20, 0.5) * 2**20:.0f} de {2**20}")  # -> 21700 de 1048576
```

:::claves
- `stats.binomtest(15, 20, p=0.5)` tiene un argumento llamado `p` que es la probabilidad de cara bajo `H₀`, no el p-valor. El p-valor está en `.pvalue`. El nombre invita a confundirlos y el código no se queja.
- `alternative="two-sided"` no es siempre el doble de `"greater"`. Aquí lo es porque la binomial con p = 0,5 es simétrica; en una distribución asimétrica, el método de dos colas suma las probabilidades menores o iguales que la observada y el resultado no es 2 × la cola.
- `stats.binom.sf(14, 20, 0.5)` es P(X > 14), o sea P(X ≥ 15). `sf` es siempre estricta por la derecha, así que para incluir el 15 hay que pasarle 14. Ese desplazamiento de uno es el error clásico al usar `sf` en vez de `1 - cdf`.
- `dos_colas` y `una_cola` no son números: son objetos con métodos (`.pvalue`, `.proportion_ci()`). Por eso hay que escribir `.pvalue` para operar con ellos, y por eso `dos_colas < 0.05` lanza un `TypeError` en vez de comparar nada.
- `stats.binomtest` (contraste) y `stats.binom` (distribución) son dos objetos distintos de la misma librería: el primero devuelve el p-valor con su propio criterio de «al menos tan extremo», el segundo da la cola exacta con `sf`, `cdf` o `pmf`. Aquí coinciden (0,0207) porque la binomial con p = 0,5 es simétrica, pero no son intercambiables.
- `stats.binom.sf(14, 20, 0.5) * 2**20` mezcla un `np.float64` con un entero de Python y el resultado sigue siendo flotante: el `:.0f` del `print` es lo que lo muestra como un recuento. Ese 21.700 se puede comprobar a mano con los coeficientes binomiales (15.504 + 4.845 + 1.140 + 190 + 20 + 1); si tu suma no cuadra, el error está en los coeficientes, no en `sf`.
:::

```python verificable
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
reps, n = 5000, 30

# Bajo H0 (los dos grupos salen de la misma normal) el p-valor es uniforme:
# con 5000 contrastes, alrededor del 5 % dan p < 0,05 sin que exista ningun efecto.
a = rng.normal(0, 1, size=(reps, n))
b = rng.normal(0, 1, size=(reps, n))
p_nulo = stats.ttest_ind(a, b, axis=1).pvalue

# Bajo H1 (media 0,5 mas alta) los p-valores se apiñan cerca de cero
c = rng.normal(0.5, 1, size=(reps, n))
p_real = stats.ttest_ind(c, b, axis=1).pvalue

print(f"P(p < 0,05) sin efecto:  {np.mean(p_nulo < 0.05):.3f}")   # -> 0.051
print(f"P(p < 0,10) sin efecto:  {np.mean(p_nulo < 0.10):.3f}")   # -> 0.105
print(f"P(p < 0,05) con efecto:  {np.mean(p_real < 0.05):.3f}")   # -> 0.475
```

```python verificable
# Lo que un p < 0,05 no te dice: la proporcion de hallazgos que son falsos.
# 200 candidatos, 20 con efecto real, potencia 80 %, alpha 5 %.
verdaderos, ruido = 20, 180
aciertos = 0.80 * verdaderos
falsos = 0.05 * ruido
hallazgos = aciertos + falsos

print(f"hallazgos con p < 0,05  {hallazgos:.0f}")          # -> 25
print(f"de ellos, falsos        {falsos:.0f}")            # -> 9
print(f"proporcion de falsos    {falsos / hallazgos:.0%}")  # -> 36%
```

## Errores típicos

- **Leerlo como la probabilidad de que la nula sea cierta.** «p = 0,03, luego hay un 3 % de
  probabilidad de que no haya efecto» es la falacia del fiscal. Sin un prior no puedes
  calcular esa probabilidad, y con un prior fuerte puede ser altísima aunque p sea pequeño.
- **Usarlo como medida del tamaño del efecto.** Un p-valor bajísimo puede corresponder a una
  diferencia irrelevante si `n` es enorme; uno alto puede esconder un efecto grande con `n` pequeña.
  El p-valor mezcla efecto y tamaño de muestra.
- **Tratar 0,049 y 0,051 como categorías distintas.** La frontera del 5 % es una convención, no un
  acantilado. Un p = 0,049 y un p = 0,051 son prácticamente la misma evidencia y sin embargo uno se
  publica y el otro no.
- **Confundirlo con la probabilidad de replicar.** Que un estudio tenga `p = 0,01` no implica que el
  siguiente vaya a salir significativo: eso depende de la potencia, y con poca potencia la
  replicación es una moneda al aire.
- **Elegir el análisis después de ver los datos.** Probar tres filtros, dos recodificaciones y
  cuatro modelos, y publicar el que da `p < 0,05`, es p-hacking aunque no lo llames así. La solución
  es preinscribir el análisis o corregir por comparaciones múltiples ([[multiplicidad-y-fdr]]).
- **Creer que un p pequeño valida el experimento.** Un p-valor pequeño en un estudio con sesgo de
  selección, attrition o mala medición es un p-valor pequeño de algo que no querías medir. El
  p-valor no evalúa el diseño.

:::practica
enunciado: Un equipo contrasta 12 relaciones entre variables. Ninguna existe de verdad y cada contraste es independiente con α = 0,05. ¿Qué probabilidad hay de que al menos una salga con p < 0,05? ¿Y si probaran 30 relaciones?
pista: La probabilidad de que ninguna prueba dé un falso positivo es (1 − α) elevado al número de pruebas independientes.
solucion: La probabilidad de no dar falso positivo en una prueba es 0,95. Con 12 pruebas: 0,95¹² = 0,540, así que P(al menos un falso positivo) = 1 − 0,540 = 0,460. Con 30 pruebas: 0,95³⁰ = 0,215, y la probabilidad sube a 0,785. Conclusión: probando muchas relaciones sin corregir por multiplicidad, es más probable que improbable publicar un hallazgo que solo era ruido.
:::

## Comprueba que lo sabes

:::quiz
p: Un contraste da p = 0,03. ¿Cuál es la interpretación correcta?
o: Hay un 3 % de probabilidad de que la hipótesis nula sea verdadera
o: Si la hipótesis nula fuera cierta, la probabilidad de observar algo al menos tan extremo como esto sería del 3 %
o: El efecto medido es grande y relevante en la práctica
a: 2
e: El p-valor condiciona los datos a la hipótesis nula, nunca al contrario. No informa del tamaño del efecto ni de la probabilidad de que la nula sea cierta: para eso haría falta un prior y un intervalo con el tamaño del efecto.
:::

:::quiz
p: Si la hipótesis nula es cierta y el estadístico es continuo, ¿cómo se distribuye el p-valor?
o: Uniforme entre 0 y 1, así que un 5 % de los contrastes dan p < 0,05 por puro azar
o: Concentrado cerca de 1, porque no hay efecto real
o: Normal con media 0,5 y desviación 0,25
a: 1
e: La uniformidad es precisamente lo que hace del 5 % un umbral calibrado: bajo la nula, cada valor de p es igual de probable. Por eso un p < 0,05 aislado no es prueba de nada si no estaba preinscrito como contraste único. Si estuviera concentrado cerca de 1, el umbral del 5 % sería inútil.
:::

:::quiz
p: De 200 candidatos, 20 tienen efecto real. Con potencia 0,80 y α = 0,05, ¿qué proporción de los hallazgos significativos es falsa?
o: El 5 %, porque α = 0,05
o: El 36 %, porque los 9 falsos esperados sobre 25 hallazgos totales pesan más que el 5 %
o: El 80 %, porque la potencia es alta
a: 2
e: Se detectan 0,80 · 20 = 16 reales y se cuelan 0,05 · 180 = 9 falsos: 9 de 25 son el 36 %. El 5 % es la tasa de falsos positivos entre los que no tienen efecto, no entre los hallazgos, y esa distinción es justo la que explica el FDR.
:::
