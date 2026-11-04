---
id: glm-y-logistica
titulo: Modelos lineales generalizados y regresión logística
fase: 6
nivel: intermedio
rutas: [ds, core]
prerequisitos: [regresion-lineal, maxima-verosimilitud, probabilidad-condicional]
tags: [glm, clasificacion, probabilidad, enlace]
resumen: Cuando la respuesta no es continua: función de enlace, odds, logit y por qué la regresión logística es el GLM más usado del oficio.
fuentes: ["Nelder y Wedderburn (1972), 'Generalized Linear Models'", "McCullagh y Nelder (1989), 'Generalized Linear Models'"]
---

## En una frase

Un modelo lineal generalizado mantiene la parte lineal `β₀ + β₁x₁ + …` pero le pone delante una
transformación (la función de enlace) que adapta el resultado al tipo de respuesta: en la
logística, esa transformación convierte la probabilidad en algo que va de menos infinito a más
infinito y se llama logit.

## La idea

La regresión lineal funciona porque la respuesta puede valer cualquier número real. ¿Qué pasa
si lo que quieres predecir es «¿se cancela este cliente?», es decir, un 0 o un 1? Puedes ajustar
una recta a los ceros y unos, pero el resultado es malo por tres motivos concretos: la recta
predice 1,3 o −0,2 (probabilidades imposibles), trata igual un error cerca de 0,5 que cerca de
los extremos, y la varianza de una variable 0/1 depende de su media, así que nunca es constante.

El truco del GLM es no forzar la linealidad sobre la probabilidad `p`, sino sobre una función de
`p`. En la regresión logística se elige el **logit**, que es el logaritmo de las *odds*:

:::formula
logit(p) = ln( p / (1 − p) )
:::

- `p` — probabilidad del suceso, entre 0 y 1.
- `p / (1 − p)` — las *odds* o ventaja: cuántas veces es más probable que ocurra frente a que no.
- `ln` — logaritmo natural.

Mira lo que hace esa transformación. Si `p = 0,5`, las odds son 1 y el logit vale 0. Si
`p = 0,9`, las odds son 9 y el logit 2,20. Si `p = 0,99`, las odds son 99 y el logit 4,60. El
logit estira los extremos hacia más y menos infinito y deja la zona central casi lineal. Eso
resuelve el problema de las predicciones imposibles: la parte lineal puede valer cualquier
número, y al deshacer la transformación siempre cae entre 0 y 1.

Por eso las *odds* son el idioma natural de la logística: un coeficiente de 0,8 significa «cada
unidad de `x` multiplica las odds por `e^0,8 = 2,23`», no «suma 0,8 a la probabilidad». La
probabilidad sube mucho cuando partes de 0,1 y casi nada cuando partes de 0,9, y las odds
capturan exactamente eso.

## Definición formal

Un GLM tiene tres piezas: una distribución para la respuesta, un predictor lineal y una función
de enlace que los conecta.

1. **Componente aleatorio:** `y` sigue una distribución de la familia exponencial (normal,
   Bernoulli, Poisson, gamma…).
2. **Predictor lineal:** `η = β₀ + β₁x₁ + … + βₚxₚ`.
3. **Función de enlace:** `g(μ) = η`, donde `μ = E[y]` es la media de la respuesta.

En la regresión logística, `y` es Bernoulli con `μ = p` y el enlace es el logit:

:::formula
ln( p / (1 − p) ) = β₀ + β₁ x₁ + … + βₚ xₚ
:::

Despejando `p` aparece la función logística o sigmoide, que es la inversa del enlace:

:::formula
p = 1 / (1 + e^(−η))      con η = β₀ + β₁ x₁ + … + βₚ xₚ
:::

- `η` — predictor lineal, la combinación de variables con sus coeficientes.
- `e` — base de los logaritmos naturales, aproximadamente 2,71828.
- `p` — probabilidad estimada del suceso, siempre entre 0 y 1.
- `βⱼ` — cambio en el **log-odds** por unidad de `xⱼ`, manteniendo el resto constante.
- `e^(βⱼ)` — *odds ratio*: cuánto se multiplican las odds por unidad de `xⱼ`.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `βⱼ` | Cambio en el log-odds por unidad de `xⱼ` | log-odds por unidad de `xⱼ` | Las odds se multiplican por `e^βⱼ`; el efecto sobre la probabilidad depende de donde estes de la curva |
| `η` | Predictor lineal: la combinación `β₀ + β₁x₁ + …` | log-odds | La sigmoide lo aplasta al intervalo [0, 1]: en el centro mueve mucho la probabilidad y en los extremos casi nada |
| `p` | Probabilidad estimada del suceso | tanto por uno, de 0 a 1 | Al acercarse a 0 o a 1 la varianza `p(1 − p)` se hace pequeña: el modelo tiene menos margen para distinguir |
| `e^(βⱼ)` | Odds ratio: cuanto se multiplican las odds por unidad | adimensional | Por encima de 1 aumenta las odds; solo se parece al riesgo relativo cuando el suceso es raro |
| `D` | Desvianza: menos dos veces la log-verosimilitud | adimensional | Cuanto menor, mejor ajuste; la diferencia entre dos modelos anidados se contrasta con una ji-cuadrado |
| `L` | Verosimilitud del modelo en los datos | adimensional, entre 0 y 1 | Crece cuando el modelo da mas probabilidad a lo que paso; se maximiza con un algoritmo iterativo, no con una formula |
:::

Los coeficientes no se estiman con una fórmula cerrada como en mínimos cuadrados, porque la
verosimilitud de Bernoulli no la tiene. Se maximiza por [[maxima-verosimilitud|máxima
verosimilitud]] con un algoritmo iterativo (mínimos cuadrados reponderados, IRLS), que en cada
paso resuelve una regresión ponderada por `p(1 − p)`.

Otros GLM que conviene reconocer: **Poisson** con enlace logarítmico para conteos (llamadas por
hora, defectos por metro), **gamma** con enlace inverso o logarítmico para cantidades positivas
y asimétricas (importes de siniestros) y **binomial** con enlace logit o probit para
proporciones. La estructura es siempre la misma; cambia la distribución y el enlace.

Para comparar y contrastar modelos se usa la **desvianza**, que es menos dos veces la
log-verosimilitud más una constante: `D = −2 · ln L`. Cuanto menor, mejor ajuste, y la
diferencia de desvianzas entre dos modelos anidados se contrasta con una ji-cuadrado.

## Ejemplo

Partimos de `p = 0,25`. Las odds son `0,25 / 0,75 = 1/3 ≈ 0,3333` y el logit vale
`ln(0,3333) = −1,0986`. Ahora supón un modelo con `β₀ = −1,0986` y `β₁ = 0,8`, y mira qué pasa
al subir `x` una unidad:

- `η = −1,0986 + 0,8 = −0,2986`.
- `p = 1 / (1 + e^(0,2986)) = 1 / 2,3481 = 0,4259`.
- Las odds pasan de 0,3333 a 0,3333 · e^0,8 = 0,3333 · 2,2255 = 0,7418. Y, en efecto,
  `0,7418 = 0,4259 / 0,5741`.

La probabilidad sube 0,176 (de 0,250 a 0,426) mientras que el *odds ratio* es constante, 2,23.
Ese es el motivo de que nunca se diga «un coeficiente de 0,8 sube la probabilidad un 80 %».

:::figura
fichero: glm-sigmoide-y-logit
pie: El primer panel es la función de enlace invertida: por mucho que el predictor lineal η se vaya a más o menos infinito, la probabilidad se queda entre 0 y 1. Lo que importa es la forma: en el centro la curva es casi una recta, así que una unidad más de η mueve mucho la probabilidad, y en los extremos está tan aplastada que casi no la mueve. El segundo panel pone los doce alumnos del ejemplo sobre la curva ajustada: la frontera del 0,5 cae en 3,76 horas y con 4 horas la probabilidad ya es 0,576. El tercero muestra por qué se trabaja en logit: la zona central es casi lineal, pero de 0,9 a 0,99 el logit pasa de 2,20 a 4,60. Un mismo coeficiente suma lo mismo en logit y mueve la probabilidad de forma muy distinta según dónde estés.
fuente: figuras/glm-y-logistica-1.py
:::

Con datos reales de horas de estudio y resultado de examen, doce alumnos:

```
b0 -4.774  b1 1.271
odds ratio por hora extra 3.563
h=4.0  sigmoide 0.576  sklearn 0.576
h=6.0  sigmoide 0.945  sklearn 0.945
```

Cada hora extra multiplica las odds de aprobar por 3,56. Para 4 horas la probabilidad estimada
es 0,576; para 6 horas, 0,945. La sigmoide calculada a mano coincide con la de la librería, que
es la comprobación de que has entendido el enlace.

## Código

```python verificable
import numpy as np
from sklearn.linear_model import LogisticRegression

# Horas de estudio (x) y resultado del examen (1 aprueba, 0 suspende).
x = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0]).reshape(-1, 1)
y = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1])

# reshape(-1, 1) convierte los 12 numeros en una matriz de 12 filas y 1 columna:
# sklearn espera una tabla de variables, no una lista plana.
modelo = LogisticRegression().fit(x, y)
b0, b1 = modelo.intercept_[0], modelo.coef_[0, 0]

print(f"b0 {b0:.3f}  b1 {b1:.3f}")
print(f"odds ratio por hora extra {np.exp(b1):.3f}")
for horas in (4.0, 6.0):
    p = 1 / (1 + np.exp(-(b0 + b1 * horas)))          # funcion logistica
    # predict_proba devuelve dos columnas (clase 0 y clase 1): el [0, 1] toma la segunda.
    print(f"h={horas:.1f}  sigmoide {p:.3f}  sklearn {modelo.predict_proba([[horas]])[0, 1]:.3f}")
# -> b0 -4.774  b1 1.271
# -> odds ratio por hora extra 3.563
# -> h=4.0  sigmoide 0.576  sklearn 0.576
# -> h=6.0  sigmoide 0.945  sklearn 0.945
```

:::claves
- `x` tiene que ser una matriz de una columna, y por eso esta el `.reshape(-1, 1)`. El `-1`
  significa «calcula tu esa dimensión»: con 12 números sale una matriz de 12 filas. Si le pasas
  la forma plana `(12,)`, sklearn lanza un error de dimensiones en vez de adivinar.
- `modelo.intercept_` y `modelo.coef_` son **arrays**, no números: `[0]` y `[0, 0]` los sacan de
  dentro. Si imprimes `modelo.coef_` tal cual veras `[[1.27...]]` con corchetes de mas, y si la
  operación siguiente espera un número, fallara.
- `print("b0", b0)` imprime los decimales completos; el redondeo a tres cifras es cosa del
  formato `f"{b0:.3f}"`. Lo que se ve en pantalla no es lo que hay guardado: las cuentas
  siguientes usan el valor completo.
- `modelo.predict_proba([[horas]])` devuelve una matriz de dos columnas: la probabilidad de la
  clase 0 y la de la clase 1. El `[0, 1]` toma la segunda. Elegir `[0, 0]` no da un error, da la
  probabilidad **contraria**: es un fallo que pasa desapercibido si no miras los números.
- `1 / (1 + np.exp(-(b0 + b1 * horas)))` escrito a mano da exactamente lo mismo que la libreria
  porque la logistica no tiene truco. La comprobación sirve cuando el signo se te va: un
  `np.exp(+(b0 + b1 * horas))` produce una curva decreciente y dos números que no cuadran.
- `LogisticRegression()` aplica **penalización L2 por defecto** (`C=1.0`), así que no es
  exactamente el modelo de maxima verosimilitud de la formula. Con estos 12 datos ya se nota:
  sin penalizar, `b1` vale 2,61 en vez de 1,271. Con muchas variables correlacionadas, la
  diferencia es grande.
- `np.log(p)` en el segundo bloque se va a **menos** infinito si algun `p` valiera 0: numpy
  devuelve `-inf` y un aviso en vez de un error, pero la suma deja de servir. Y `predict_proba`
  si puede dar un 0 o un 1 exactos: `sklearn` no los recorta, calcula su perdida con una forma
  estable de `log(1 + e^z)`.
:::

```python verificable
import numpy as np

# 100 casos: el modelo da 0,8 a los 30 positivos y 0,3 a los 70 negativos.
y = np.array([1.0] * 30 + [0.0] * 70)
p = np.concatenate([np.full(30, 0.8), np.full(70, 0.3)])

# Log-verosimilitud de Bernoulli: suma de y*log(p) + (1-y)*log(1-p).
ll = (y * np.log(p) + (1 - y) * np.log(1 - p)).sum()
base = y.mean()
ll_base = (y * np.log(base) + (1 - y) * np.log(1 - base)).sum()

print(f"log-verosimilitud modelo {ll:.3f}")
print(f"log-verosimilitud base   {ll_base:.3f}")
print(f"2*(ll - ll_base)         {2 * (ll - ll_base):.3f}")
# -> log-verosimilitud modelo -31.662
# -> log-verosimilitud base   -61.086
# -> 2*(ll - ll_base)         58.850
```

## Errores típicos

- **Decir que un coeficiente sube la probabilidad en esa cantidad.** El coeficiente vive en
  escala de log-odds: su efecto sobre `p` depende del punto de partida. `β₁ = 0,8` sube la
  probabilidad 0,176 si partes de 0,25, y bastante menos si partes de 0,8. Para comunicar el
  efecto, da probabilidades en puntos concretos o el *odds ratio*.
- **Leer el *odds ratio* como riesgo relativo.** Un OR de 3,56 no significa «3,56 veces más
  probable». Solo se parecen cuando el suceso es raro (probabilidades pequeñas). Con sucesos
  frecuentes, el OR exagera el efecto respecto al riesgo relativo.
- **Ajustar mínimos cuadrados a una respuesta 0/1 y reportar el `R²`.** Las predicciones se
  salen del intervalo [0,1], los residuos no pueden ser normales ni homocedásticos y el `R²`
  pierde su interpretación. Usa un GLM con la distribución correcta.
- **Ignorar la separación perfecta.** Si una variable separa perfectamente las clases, la
  verosimilitud se maximiza empujando el coeficiente a infinito: la librería avisa o devuelve
  números enormes. La solución habitual es regularizar (penalización L2, activada por defecto
  en la mayoría de implementaciones) o replantear el problema.
- **Quedarse con el umbral 0,5.** La logística devuelve probabilidades, no decisiones. El corte
  óptimo depende de lo que cuesta cada tipo de error; con clases desbalanceadas, 0,5 suele ser
  malísimo. Eso es [[umbrales-y-coste]].
- **Comparar modelos GLM por RMSE o por exactitud en vez de por desvianza.** La desvianza es la
  medida de ajuste coherente con la verosimilitud del modelo. La exactitud mezcla el modelo con
  el umbral que hayas elegido y no distingue un 0,51 de un 0,99.

:::practica
enunciado: Un modelo logístico da a un cliente una probabilidad de fuga de 0,20. Cada mes de contrato multiplica las odds por 1,5. Calcula la probabilidad tras dos meses más, con el resto de variables igual.
pista: Pasa la probabilidad a odds con p/(1 − p), multiplica por el odds ratio elevado al número de unidades y deshaz el cambio dividiendo entre uno más las odds.
solucion: Con p = 0,20, las odds son 0,20/0,80 = 0,25. Dos meses las multiplican por 1,5² = 2,25: 0,25 · 2,25 = 0,5625. La probabilidad es 0,5625/1,5625 = 0,36. No sale 0,20 · 1,5² = 0,45: el odds ratio multiplica las odds, no la probabilidad, y por eso el efecto sobre p es menor.
:::

## Comprueba que lo sabes

:::quiz
p: En una regresión logística, ¿qué mide el coeficiente β₁ de una variable continua?
o: El cambio en la probabilidad estimada por cada unidad de la variable
o: El cambio en el logaritmo de las odds por cada unidad de la variable
o: Cuantas veces más probable es el suceso por cada unidad de la variable
a: 2
e: El modelo es lineal en el logit, no en la probabilidad. β1 es el cambio en log-odds; exp(β1) es el odds ratio, que multiplica las odds. Ninguno de los dos es un cambio directo ni constante en la probabilidad.
:::

:::quiz
p: Con odds de 1/3, ¿cuál es el logit y qué probabilidad le corresponde tras sumar 0,8 al logit?
o: Logit 0,333 y probabilidad 0,426
o: Logit −1,099 y probabilidad 0,426
o: Logit −1,099 y probabilidad 0,176
a: 2
e: El logit es ln(1/3) = -1,0986. Sumando 0,8 queda -0,2986, y la sigmoide da 1/(1+e^0,2986) = 0,426. La probabilidad sube 0,176, pero ese incremento es lo que cambia, no el logit.
:::

:::quiz
p: ¿Por qué no se ajusta una regresión lineal normal a una respuesta binaria 0/1?
o: Porque las predicciones pueden salirse de [0,1] y el error no tiene varianza constante
o: Porque los coeficientes no se pueden estimar con matrices
o: Porque la respuesta binaria no tiene media
a: 1
e: La recta puede predecir 1,3 o -0,2, que no son probabilidades, y la varianza de una Bernoulli es p(1-p), que depende de la media y por tanto nunca es constante. La media de una variable 0/1 sí existe: es la proporción de unos.
:::

:::trampa
La regresión logística es lineal en el logit, no en las probabilidades. Eso significa que un
mismo coeficiente produce efectos muy distintos según dónde estés de la curva: fuerte en la
zona central, casi nulo en los extremos. Cualquier frase del tipo «esta variable aumenta el
riesgo un X %» está mal si no dice en qué punto se evalúa.
:::
