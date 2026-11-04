---
id: naive-bayes
titulo: Naive Bayes
fase: 6
nivel: intermedio
rutas: [ds]
prerequisitos: [teorema-de-bayes, independencia-y-condicionamiento, maxima-verosimilitud]
tags: [clasificacion, probabilidad, texto, spam]
resumen: Clasificador probabilístico que supone que las variables son independientes dada la clase; el supuesto es falso y aun así gana en texto por rápido y por honesto.
fuentes: ["Lewis (1998), 'Naive (Bayes) at Forty: The Independence Assumption in Information Retrieval'", "Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval', cap. 13"]
---

## En una frase

Naive Bayes aplica el [[teorema-de-bayes|teorema de Bayes]] suponiendo que, sabida la clase,
todas las variables son independientes entre sí; esa suposición es casi siempre falsa, pero
hace que el cálculo sea una multiplicación barata y funciona muy bien cuando las variables son
palabras.

## La idea

Quieres saber si un correo es spam. Usas la regla de Bayes: la probabilidad de spam dado el
texto es proporcional a la probabilidad previa de spam multiplicada por la probabilidad de
observar ese texto si es spam. El problema es que «ese texto» es una secuencia concreta de
palabras y jamás has visto esa secuencia exacta. Estimar la probabilidad conjunta de 100
palabras exige una tabla con `2^100` combinaciones.

Aquí entra el supuesto ingenuo: **supón que cada palabra aparece de forma independiente de las
demás, una vez sabido si el correo es spam o no**. Entonces la probabilidad conjunta se
factoriza en un producto de probabilidades por palabra, y cada una se estima contando cuántas
veces aparece esa palabra en los correos de cada clase. De `2^100` parámetros pasas a dos
números por palabra. Eso es todo el truco, y explica el nombre.

Es ingenuo porque es falso de forma evidente: en un correo real, «gratis» y «oferta» aparecen
juntos muchísimo más de lo que predice la independencia. Y sin embargo el clasificador
funciona. ¿Por qué? Por dos razones prácticas: para **decidir** solo importa qué clase queda
con mayor puntuación, no que las probabilidades sean exactas, y los errores de la
factorización se reparten de forma parecida entre las clases. Además, con muchas variables
correlacionadas, el voto repetido de un mismo indicio empuja la decisión en la dirección
correcta aunque exagere la confianza.

De ahí su segunda virtud: es **rapidísimo**. Entrenar es contar palabras; predecir es sumar
logaritmos. En un corpus de un millón de documentos, un multinomial Naive Bayes entrena en
segundos. Y su tercera virtud: funciona con pocos datos por clase, porque cada palabra aporta
su propio parámetro.

El precio es que sus probabilidades están **mal calibradas**: suele dar 0,9999 cuando la
confianza real es 0,8. Si lo que necesitas es una probabilidad para decidir un umbral de
negocio, tendrás que calibrarlo.

## Definición formal

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `c` | Una de las clases posibles (spam, no spam) | ninguna | No es una magnitud que se mueva: es una de las opciones entre las que decides |
| `xⱼ` | La variable `j`; en texto, la palabra `j` | apariciones o presencia | Más apariciones de una palabra que favorece a una clase empujan la decisión hacia ella, y lo hacen de forma multiplicativa |
| `P(c)` | Previa de la clase: su frecuencia en el entrenamiento | probabilidad, entre 0 y 1 | Arrastra el resultado en la misma dirección. Con clases muy desbalanceadas, una previa de 0,99 decide casi sola; si vale 0, esa clase es imposible para siempre |
| `P(xⱼ / c)` | Verosimilitud de la palabra `j` dentro de la clase `c` | probabilidad, entre 0 y 1 | Sube la puntuación de esa clase en `log P`, y como se suman logaritmos, el efecto crece con el número de apariciones. Un valor de 0 anula el producto entero |
| `Πⱼ` | Producto sobre todas las variables | ninguna | Cuantas más palabras tenga el documento, más factores y más pequeño el producto: con 300 palabras y probabilidades de 0,01 el resultado cae por debajo de lo que representa un `float` de 64 bits. Por eso se trabaja en logaritmos |
| `Σⱼ log P(xⱼ / c)` | La misma cuenta en logaritmos | log-probabilidad (sin unidades) | Es lo que se compara de verdad. Las diferencias se leen como cocientes de verosimilitud: 2,655 en log es un factor 14 |
| `α` | Suavizado de Laplace: pseudo-cuentas que se suman a cada palabra | cuentas (número, no entero) | Reparte la probabilidad entre todas las palabras del vocabulario: las verosimilitudes se acercan entre sí y la decisión se vuelve menos extrema. Con `α` enorme, todas las palabras pesan igual y decide solo la previa |
| `V` | Tamaño del vocabulario | palabras | El suavizado reparte `α·V` pseudo-cuentas entre todas: con vocabularios muy grandes hace falta `α` más pequeño para no borrar las diferencias entre palabras |
| `n` | Número de documentos de la clase | documentos | Es el denominador de la verosimilitud y el que da o quita peso al suavizado: con pocos documentos por clase, `α = 1` domina y las verosimilitudes se aplanan |
:::

Con una clase `c` y un vector de variables `x = (x₁, …, x_d)`, la regla de decisión es

:::formula
ŷ = argmax_c  P(c) · Πⱼ P(xⱼ | c)
:::

- `c` — una de las clases posibles (por ejemplo, `spam` o `no spam`).
- `P(c)` — probabilidad previa de la clase, estimada con su frecuencia en el entrenamiento.
- `xⱼ` — la variable `j`; en texto, la presencia de la palabra `j` o su número de apariciones.
- `P(xⱼ | c)` — verosimilitud de esa variable dentro de la clase `c`.
- `Πⱼ` — producto sobre todas las variables; es la factorización que introduce el supuesto
  ingenuo.

Para evitar que un producto de muchos números pequeños se convierta en cero en coma flotante,
se trabaja en logaritmos:

:::formula
ŷ = argmax_c [ log P(c) + Σⱼ log P(xⱼ | c) ]
:::

Tres variantes según el tipo de variable:

| Variante | Variable | Verosimilitud |
| --- | --- | --- |
| Bernoulli | Presencia o ausencia | `pⱼ^1 · (1 − pⱼ)^0` si la palabra aparece y `pⱼ^0 · (1 − pⱼ)^1` si no aparece, así que penaliza la ausencia explícitamente |
| Multinomial | Conteo de apariciones | Producto de potencias según el número de veces |
| Gaussiana | Variable continua | Densidad normal con media y varianza por clase |

El **suavizado de Laplace** añade una pseudo-cuenta para que una palabra nunca vista en una
clase no anule todo el producto: `P(xⱼ = 1) = (nⱼ + α) / (n + α·V)`, con `nⱼ` el número de
documentos de la clase que contienen la palabra, `n` el total de documentos de la clase, `V`
el tamaño del vocabulario y `α` normalmente 1.

## Ejemplo

Seis correos ya etiquetados y solo dos palabras, «gratis» y «premio». Contamos cuántos correos
de cada clase contienen cada palabra:

| Palabra | Aparece en spam (de 4) | Aparece en no spam (de 2) |
| --- | --- | --- |
| gratis | 3 | 0 |
| premio | 2 | 1 |

Con `α = 1` y `V = 2` (el vocabulario son esas dos palabras), las verosimilitudes salen de la
fórmula de Laplace `(nⱼ + α) / (n + α·V)`, donde `nⱼ` es la cuenta de la tabla y `n` el número
de documentos de la clase:

- `P(gratis | spam) = (3+1)/(4+2) = 0,667`
- `P(gratis | no spam) = (0+1)/(2+2) = 0,250`
- `P(premio | spam) = (2+1)/(4+2) = 0,500`; `P(premio | no spam) = (1+1)/(2+2) = 0,500`

Llega un correo que contiene «gratis» **dos veces** y ninguna vez «premio». Con las previas
`P(spam) = 4/6 = 0,667` y `P(no spam) = 2/6 = 0,333`, y la variante multinomial, que solo suma
los términos de las palabras que aparecen (con su número de apariciones):

- Spam: `log(0,667) + 2 · log(0,667) = −0,405 − 0,810 = −1,216`
- No spam: `log(0,333) + 2 · log(0,250) = −1,099 − 2,773 = −3,871`

Gana **spam** con una diferencia de 2,655 en logaritmos, que equivale a un cociente de
verosimilitudes de `e^2,655 ≈ 14,2`. Fíjate en que la palabra «premio» no discrimina (0,5 en
las dos clases) y no aporta nada al cálculo; «gratis» sí. Ojo con la variante: si usaras
`BernoulliNB`, el modelo sumaría también el término de las palabras **ausentes**, `log(1 − p)`,
y las puntuaciones serían distintas. Sin suavizado, cualquier correo de «no spam» tendría
`P(gratis | no spam) = 0` y el producto se anularía: ese es exactamente el motivo de Laplace.

El bloque de código hace la misma cuenta sobre un corpus algo mayor (6 correos y unas cuantas
palabras más), así que los números no coinciden dígito a dígito con este ejemplo de dos
palabras: lo que importa es que el procedimiento es idéntico.

## Código

:::figura
fichero: naive-bayes-previa-y-suavizado
pie: El panel izquierdo explica por qué Naive Bayes acierta tanto y engaña tanto: con una sola palabra decisiva (razón de verosimilitud 20) el posterior ya pasa del 50 % cuando la previa llega al 5 %, y con tres indicios contados por separado la curva se vuelve casi un escalón, que es la forma que tienen sus probabilidades: 0,9999 cuando la confianza real es 0,8. La lectura práctica es que en este modelo la frecuencia de spam del corpus manda más de lo que parece. El panel derecho muestra el efecto del suavizado de Laplace sobre el caso de la página: la palabra «gratis» aparece en 3 de 4 spam y en 0 de 2 correos legítimos, así que sin pseudo-cuentas su verosimilitud en la clase legítima vale 0 y el producto entero se anula; al subir `alpha`, las verosimilitudes se acercan entre sí y la decisión se vuelve menos extrema. El valor por defecto, `alpha = 1`, es el que deja la probabilidad en torno a 0,70.
fuente: figuras/naive-bayes-1.py
:::

```python verificable
import numpy as np

# Naive Bayes multinomial desde cero sobre conteos escritos a mano.
# Filas: 4 correos de spam y 2 de no spam. Columnas: "gratis", "premio".
conteos = {"spam": np.array([3.0, 2.0]), "no spam": np.array([0.0, 1.0])}
n_docs = {"spam": 4.0, "no spam": 2.0}
alpha, V = 1.0, 2   # suavizado de Laplace, vocabulario de 2 palabras

# Suavizado de Laplace: (n_j + alpha) / (n + alpha * V). Se hace de una vez para
# las dos palabras porque conteos[c] es un array; alpha y V son escalares.
log_verosimilitud = {
    c: np.log((conteos[c] + alpha) / (n_docs[c] + alpha * V)) for c in conteos
}
log_previa = {c: np.log(n_docs[c] / 6.0) for c in conteos}

# Correo nuevo: aparece "gratis" (2 veces) y no aparece "premio".
x = np.array([2.0, 0.0])
for c in conteos:
    # x tiene un 0 en las palabras ausentes, asi que no restan nada: es la
    # diferencia con BernoulliNB, que si penaliza las ausencias.
    puntuacion = log_previa[c] + float((x * log_verosimilitud[c]).sum())
    print(f"{c:<8} log P(clase) {log_previa[c]:+.3f}  puntuacion total {puntuacion:+.3f}")
# -> spam     log P(clase) -0.405  puntuacion total -1.216
# -> no spam  log P(clase) -1.099  puntuacion total -3.871

print("prediccion:", max(conteos, key=lambda c: (x * log_verosimilitud[c]).sum() + log_previa[c]))
# -> spam
```

:::claves
- El primer bloque escribe la fórmula de Laplace a mano, así que la cuenta se puede seguir número a número. Ojo con `np.log((conteos[c] + alpha) / (n_docs[c] + alpha * V))`: aquí `conteos` y `n_docs` son diccionarios de **arrays**, uno por clase, y la división se hace elemento a elemento porque `alpha` y `V` son escalares.
- `log_previa` usa `n_docs[c] / 6.0` con la constante escrita a mano: es el total de documentos. Cambiar el corpus y olvidarse de ese 6 descuadra las previas sin dar ningún error. Con `6` en vez de `6.0`, en Python 3 el resultado sigue siendo `float`; la trampa era en Python 2.
- La puntuación se calcula como `(x * log_verosimilitud[c]).sum()`, y eso depende de que `x` tenga un **cero** en las palabras ausentes. El cero anula ese término, así que una palabra que no aparece no resta. Es justo la diferencia con `BernoulliNB`, que sí suma el término `log(1 − p)` de las palabras que faltan y por eso penaliza los documentos largos.
- `max(conteos, key=lambda c: ...)` devuelve la **clave** del diccionario, es decir, la cadena `"spam"`, no la puntuación ni una tupla. Si el empate importa, `max` devuelve el primero que encuentra y el orden de las claves de un `dict` es el de inserción.
- En el segundo bloque, `CountVectorizer` aprende el vocabulario en `fit_transform` y lo reutiliza en `transform`. Por eso `vec.transform(["gratis informe"])` produce una fila con las columnas de todas las palabras vistas en el corpus: una palabra nueva que no estuviera en el entrenamiento se **ignora en silencio**, sin aviso.
- `MultinomialNB(alpha=1e-9)` y `alpha=0` no son lo mismo, pero se parecen mucho: con `1e-9`, `log(1e-9) ≈ −20,7` y el número sigue siendo representable; con `0` exacto la verosimilitud es 0 y el logaritmo da `-inf`. El suavizado tampoco arregla la calibración: las probabilidades siguen siendo extremas, solo que menos.
- `m.predict_proba(nuevo)[0]` devuelve un array de dos probabilidades ordenadas por las clases **ordenadas**, no por su valor: la posición 0 es la clase 0. Si tu etiqueta fuese una cadena (`"spam"`, `"no spam"`), el orden sería alfabético, y ahí está el despiste habitual al leer la columna que no toca.
:::

```python verificable
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Corpus diminuto y escrito a mano: "informe" y "trimestral" solo salen en no spam.
textos = [
    "gratis premio gratis enhorabuena", "premio gratis reclama ahora",
    "gratis oferta premio gratis", "premio gratis dinero gratis",
    "informe adjunto trimestral", "adjunto el informe trimestral",
]
etiquetas = [1, 1, 1, 1, 0, 0]

vec = CountVectorizer()                     # aprende el vocabulario del corpus
X = vec.fit_transform(textos)               # matriz dispersa documentos x palabras
# transform (no fit_transform): usa el vocabulario ya aprendido. Una palabra que
# no estuviera en el corpus se ignoraria en silencio.
nuevo = vec.transform(["gratis informe"])   # mezcla de las dos clases

# Cuanto mayor es alpha, mas se suavizan las probabilidades extremas.
for alpha in (1e-9, 0.1, 1.0):
    m = MultinomialNB(alpha=alpha).fit(X, etiquetas)
    prob = m.predict_proba(nuevo)[0]
    print(f"alpha {alpha:<8g} P(spam) {prob[1]:.3f}  P(no spam) {prob[0]:.3f}  predice {int(m.predict(nuevo)[0])}")
# -> alpha 1e-09    P(spam) 0.573  P(no spam) 0.427  predice 1
# -> alpha 0.1      P(spam) 0.603  P(no spam) 0.397  predice 1
# -> alpha 1        P(spam) 0.703  P(no spam) 0.297  predice 1
```

## Errores típicos

- **Creer que las probabilidades son buenas.** Naive Bayes es un clasificador excelente y un
  estimador de probabilidad mediocre: empuja los valores hacia 0 y 1. Si vas a comparar la
  probabilidad con un umbral de coste, pásalo antes por
  [[calibracion|calibración de probabilidades]].
- **Activar la penalización de la ausencia sin pensar.** `BernoulliNB` incluye el término de
  las palabras que **no** aparecen, lo que en documentos largos domina la decisión; y
  `MultinomialNB` ignora las ausencias. Con textos cortos, Bernoulli suele ir mejor; con textos
  largos, multinomial. Pruébalos, no lo supongas.
- **Olvidar el suavizado.** Con `alpha = 0`, una sola palabra no vista en una clase anula el
  producto entero y el correo se clasifica siempre en la otra. Nunca uses cero.
- **Aplicar la variante gaussiana a variables que no son normales o están muy correlacionadas.**
  `GaussianNB` ajusta una normal por variable y por clase: con una variable sesgada o con dos
  variables casi idénticas sobreestima la confianza. Para datos tabulares continuos, los
  árboles suelen ganar.
- **Ignorar el desbalanceo de clases.** La previa `P(c)` sale directamente de las frecuencias y,
  con clases muy desbalanceadas, arrastra la decisión. Puedes ajustarla con
  `class_prior` en cualquiera de las variantes.
- **Usarlo para decidir cuando lo que importa es el orden.** En recuperación de información,
  las puntuaciones de Naive Bayes ordenan razonablemente bien pero no cumplen la propiedad de
  ranking de un modelo de relevancia; para eso están las métricas de
  [[metricas-de-ranking|ranking]].

:::practica
enunciado: De 10 correos, 6 son spam y 4 no spam. La palabra «factura» aparece en 1 de los 6 spam y en los 4 no spam. Con suavizado α = 1 y vocabulario V = 3, calcula en logaritmos la puntuación de un correo que contiene «factura» una vez y decide su clase.
pista: Aplica Laplace (n_j + α)/(n + α·V) a cada clase y suma el logaritmo de la previa con el de la verosimilitud.
solucion: Previas: 0,6 y 0,4. Verosimilitudes: factura en spam (1+1)/(6+3) = 0,222; en no spam (4+1)/(4+3) = 0,714. Spam: log 0,6 + log 0,222 = −0,511 − 1,504 = −2,015. No spam: log 0,4 + log 0,714 = −0,916 − 0,336 = −1,253. Gana no spam, con un cociente de verosimilitudes de e^0,762 ≈ 2,14 a su favor.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué supone exactamente el «supuesto ingenuo» de Naive Bayes?
o: Que todas las clases tienen la misma probabilidad previa
o: Que, una vez fijada la clase, las variables son condicionalmente independientes entre sí
o: Que las variables siguen una distribución normal
a: 2
e: El supuesto es de independencia condicional: `P(x₁, …, x_d | c) = Π P(xⱼ | c)`. No dice nada sobre las previas (que se estiman del entrenamiento) ni exige normalidad: eso solo ocurre en la variante `GaussianNB`.
:::

:::quiz
p: ¿Para qué sirve el suavizado de Laplace (`alpha > 0`)?
o: Para acelerar el entrenamiento
o: Para que una palabra no observada en una clase no anule el producto entero de verosimilitudes
o: Para convertir las puntuaciones en probabilidades calibradas
a: 2
e: Con conteo cero, la verosimilitud es cero y el producto completo se va a cero, así que esa clase queda descartada siempre. Añadir una pseudo-cuenta pequeña lo evita. No acelera nada y no arregla la calibración: las probabilidades siguen siendo extremas.
:::

:::nota
Naive Bayes sigue siendo la línea base obligatoria en clasificación de texto: aparece en
segundos, funciona con pocos datos etiquetados y sirve de referencia contra la que medir
cualquier modelo más caro. Si un transformer no le saca una diferencia clara en tu problema,
probablemente no necesitas el transformer.
:::
