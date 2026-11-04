---
id: evaluacion-de-llms
titulo: Evaluación de LLMs
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [train-val-test, metricas-de-clasificacion, metricas-de-ranking, prompting, contraste-de-hipotesis]
tags: [evaluacion, metricas, jueces, regresion]
resumen: Como se mide si un sistema con modelos de lenguaje funciona: conjuntos de prueba propios, métricas automáticas, jueces que hay que validar y regresiones que no se cuelan.
fuentes: ["Zheng et al. (2023), 'Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena'", "Papineni et al. (2002), 'BLEU: a Method for Automatic Evaluation of Machine Translation'"]
---

## En una frase

Evaluar un sistema con modelos de lenguaje es construir un conjunto de casos con respuesta
conocida, decidir qué métrica mide lo que te importa, y repetir la misma medición en cada
cambio para detectar cuándo has mejorado una cosa y roto otra.

## La idea

Con un modelo clásico de machine learning sabes exactamente qué hacer: separas un conjunto de
prueba, calculas una métrica y comparas. Con un sistema generativo el problema es que «bien»
no es un número único. Si el sistema responde a «¿cuál es el plazo de devolución?», la
respuesta «30 días naturales» y «treinta días» son ambas correctas, y «30 días laborables» es
una respuesta fluida, segura y falsa.

Hay tres formas de medir, y ninguna basta sola:

**Métricas automáticas contra una referencia.** Exactitud (la respuesta coincide carácter a
carácter) y `F1` por solapamiento de palabras. Son baratas, reproducibles y tontas: castigan
«París» frente a «paris» y premian una respuesta que repite palabras de la referencia sin
responder nada. Sirven para vigilar formatos, extracción de campos y preguntas con respuesta
corta y única.

**Jueces automáticos.** Otro modelo lee la pregunta, la respuesta y a veces una referencia, y
puntúa. Escalan a miles de casos y capturan matices que el `F1` no ve. Su problema es que
introducen un sesgo sistemático: tienden a preferir respuestas largas, a colocarse del lado de
la primera opción que leen y a valorarse mejor a sí mismos que a otros modelos. Por eso un
juez **hay que validarlo** contra anotaciones humanas (con acuerdo medido, por ejemplo con
kappa) antes de usarlo como termómetro.

**Evaluación humana.** Es el patrón de referencia, pero cara y lenta. Se reserva para calibrar
el juez, para decidir entre dos versiones finales y para los casos donde el error es caro.

Y una cuarta pieza que se olvida siempre: **el conjunto de prueba tiene que ser tuyo**. Los
conjuntos públicos acaban contaminados: si el corpus de entrenamiento del modelo incluyó las
preguntas y sus respuestas, tu medición mide memoria, no capacidad. Un conjunto de 200 casos
escritos por tu equipo, con las respuestas revisadas, vale más que diez conjuntos públicos de
10.000 preguntas.

Por último, la parte que convierte la evaluación en algo útil: **las regresiones**. Cada fallo
real que detectes en producción se convierte en un caso del conjunto. A partir de ahí, ningún
cambio de prompt, de modelo o de recuperador puede volver a introducirlo sin que salte la
alarma. Sin ese bucle, la evaluación es un examen que se hace una vez y se abandona.

## Definición formal

Sea un conjunto de evaluación `E = {(x₁, y₁), …, (x_N, y_N)}` con `x_i` la entrada y `y_i` la
respuesta de referencia, y sea `ŷ_i` la salida del sistema. Las métricas básicas:

- **Exactitud** (*exact match*): proporción de casos en los que, tras normalizar, la predicción
  y la referencia coinciden **palabra a palabra**. La normalización habitual pasa a minúsculas y
  quita la puntuación, pero **no los acentos**: «París» y «paris» siguen siendo distintos. Elige
  la normalización, escríbela y congélala.
- **`F1` por solapamiento de tokens**, con `P` la proporción de tokens de `ŷ` que aparecen en
  `y` y `R` la proporción de tokens de `y` que aparecen en `ŷ`:

:::formula
F1 = 2 · P · R / (P + R)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x_i` | La entrada del caso `i` del conjunto de evaluación | texto | El conjunto es tuyo o no es una medición: los públicos acaban dentro del entrenamiento del modelo y miden memoria |
| `y_i` | La respuesta de referencia, escrita y revisada por tu equipo | texto | Es el patrón contra el que se compara todo. Si es ambigua, el `F1` mide tu redacción, no el sistema |
| `ŷ_i` | Lo que responde el sistema | texto | Una respuesta puede ser correcta y no coincidir con la referencia: de ahí que haga falta más de una métrica |
| `P` | Precisión: proporción de tokens de la predicción que están en la referencia | entre 0 y 1 | Sube cuando el sistema añade poco texto de más. Una respuesta larga y correcta baja la precisión por todo lo que añade |
| `R` | Exhaustividad: proporción de tokens de la referencia que aparecen en la predicción | entre 0 y 1 | Sube cuando el sistema no se deja palabras. Responder «1789» a «¿en qué año…?» da `R = 1` y `P = 1` con una palabra |
| `F1` | Media **armónica** de `P` y `R` | entre 0 y 1 | Es alta solo si las dos lo son: si `P = 0`, el `F1` es 0 aunque `R = 1`. Con la media normal, una respuesta larguísima saldría bien parada |
| `N` | Número de casos del conjunto | casos | Con `N = 30` el intervalo de confianza es enorme: dos aciertos de diferencia no significan nada. Es el motivo de que se pidan cientos de casos propios |
| `κ` | Kappa de Cohen: acuerdo corregido por el azar | entre −1 y 1 | Por debajo de 0,4 el juez no sirve para decidir entre versiones; a partir de 0,6-0,8 el acuerdo es sustancial |
:::

- **Precisión y exhaustividad de recuperación** cuando el sistema produce un ranking de
  fragmentos citables: [[metricas-de-ranking|precision@k, recall@k, MRR y NDCG]].

Para validar un juez automático se mide el acuerdo con las etiquetas humanas. El **kappa de
Cohen** corrige el acuerdo que se produciría por azar:

:::formula
κ = (P_o − P_e) / (1 − P_e)
:::

- `P_o` — acuerdo observado: fracción de casos en los que el juez y el humano coinciden.
- `P_e` — acuerdo esperado por azar, calculado con las proporciones marginales de cada
  etiquetador: `P_e = p_juez(1) · p_humano(1) + p_juez(0) · p_humano(0)`.
- `κ = 0` significa «como el azar»; `κ = 1`, acuerdo perfecto. Como orientación, por debajo de
  0,4 el juez no es fiable para decidir entre versiones; entre 0,6 y 0,8 hay acuerdo
  sustancial y ya se puede usar para detectar cambios grandes.

Un detalle que decide la utilidad de la métrica: la **normalización**. Un `F1` sin normalizar
mide mayúsculas y comas. Si normalizas acentos y puntuación, el número baja de forma más
lenta cuando empeora el sistema. Elige una normalización y **congélala**: si cambia entre dos
mediciones, no estás comparando versiones del sistema, estás comparando versiones de la
métrica.

## Ejemplo

Seis preguntas con respuesta corta, con la predicción y la referencia:

| Predicción | Referencia | ¿Exacta? | F1 |
| --- | --- | --- | --- |
| Paris | Paris | sí | 1,00 |
| Paris | paris | sí | 1,00 |
| Paris | Lyon | no | 0,00 |
| 1789 | en 1789 | no | 0,67 |
| 1789 | 1799 | no | 0,00 |
| vatio | el vatio | no | 0,67 |

Resultado: exactitud **2/6 = 0,33**, `F1` medio **0,556**. Las dos métricas cuentan historias
distintas y las dos son correctas: el sistema acierta un tercio de las respuestas palabra por
palabra, pero se acerca en dos casos más que el `F1` sí reconoce. Si tu métrica principal es
la exactitud, el 0,33 parece un desastre; el `F1` dice que el sistema acierta el contenido en
cuatro de seis. **Elegir la métrica es elegir qué historia cuentas.**

Validación de un juez sobre 50 respuestas, con etiquetas binarias (1 = correcta):

```
juez   : 30 unos, 20 ceros
humano : 28 unos, 2 ceros, 2 unos, 18 ceros
```

- Acuerdo observado `P_o = 46/50 = 0,92`.
- Acuerdo por azar `P_e = 0,6 · 0,6 + 0,4 · 0,4 = 0,52`.
- `κ = (0,92 − 0,52) / (1 − 0,52) = 0,83`.

El 0,92 suena a juez excelente, pero un 52 % de acuerdo saldría por puro azar; el kappa 0,83
dice que el acuerdo real es sustancial. Con este juez ya puedes comparar dos versiones del
sistema, siempre que la diferencia que detectes sea mayor que su ruido (4 desacuerdos en 50).

## Código

```python verificable
import re
from collections import Counter

casos = [
    ("capital de Francia", "Paris", "Paris"),
    ("capital de Francia", "Paris", "paris"),
    ("capital de Francia", "Paris", "Lyon"),
    ("ano de la Revolucion Francesa", "1789", "en 1789"),
    ("ano de la Revolucion Francesa", "1789", "1799"),
    ("unidad de potencia", "vatio", "el vatio"),
]

def normalizar(t):
    # [^\w\s] es "todo lo que no sea letra ni espacio": asi "París" y "paris" se comparan
    # igual. \w incluye las vocales acentuadas, ojo: no las quita, solo quita la puntuacion.
    return re.sub(r"[^\w\s]", "", t.lower()).split()   # minusculas y sin puntuacion

def f1(pred, ref):
    p, r = Counter(normalizar(pred)), Counter(normalizar(ref))
    # p & r es la interseccion de multiconjuntos: cuenta las palabras comunes
    # el minimo de repeticiones, no una vez por aparicion en cualquiera de los dos
    comunes = sum((p & r).values())                    # interseccion multiconjunto
    if comunes == 0:
        return 0.0
    # P y R por separado: el F1 es su media armonica, no la media normal
    precision = comunes / sum(p.values())
    recall = comunes / sum(r.values())
    return 2 * precision * recall / (precision + recall)

# una sola pasada por los casos: la tupla guarda la referencia y las dos metricas
filas = [(p, g, normalizar(p) == normalizar(g), f1(p, g)) for _, p, g in casos]
for p, g, exacta, f in filas:
    # {p!r} imprime el valor con sus comillas: se ve que "paris" y "Paris" son distintos
    print(f"pred {p!r}  ref {g!r}  exacta {exacta}  F1 {f:.2f}")

# sum() de booleanos = numero de aciertos; len(filas) = numero de casos
print("exactas:", sum(e for _, _, e, _ in filas), "de", len(filas))
print("F1 medio:", round(sum(f for _, _, _, f in filas) / len(filas), 3))
```

:::claves
- La normalización decide el resultado. `re.sub(r"[^\w\s]", ...)` borra la puntuación, las comas y los puntos, pero **no los acentos**: la `í` de «París» es una letra (`\w`) y sobrevive al filtro, así que «París» y «paris» no coinciden. Si quieres unificar acentos hay que quitarlos aparte.
- `Counter` cuenta repeticiones y `p & r` es la intersección de **multiconjuntos**: de cada palabra se queda con el mínimo de veces que aparece en los dos textos. Es lo que distingue este `F1` del solapamiento simple, que contaría una vez una palabra repetida.
- `2 * precision * recall / (precision + recall)` es la **media armónica**: si una de las dos es cero, el `F1` es cero por bueno que sea el otro valor. Con `comunes == 0` la división daría `ZeroDivisionError`, y por eso el `if` devuelve 0,0 antes.
- `lambda` y comprensiones no: aquí la lista `filas` **se calcula una vez** y luego se recorre dos veces (una para imprimir y otra para las medias). Si `f1()` fuese un modelo caro, ese cálculo se pagaría dos veces.
- `sum(e for _, _, e, _ in filas)` funciona porque `True` vale 1 y `False` vale 0. Es exactitud, no `F1`: las dos métricas del mismo conjunto dan 0,33 y 0,556, y las dos son correctas.
:::

```python verificable
import numpy as np

# Etiquetas de un juez automatico y de un anotador humano sobre 50 respuestas.
juez = np.array([1] * 30 + [0] * 20)
humano = np.array([1] * 28 + [0] * 2 + [1] * 2 + [0] * 18)

# .mean() de un array de 0 y 1 es la proporcion de unos; comparar arrays da True/False
acuerdo = float((juez == humano).mean())
pj, ph = juez.mean(), humano.mean()
esperado = pj * ph + (1 - pj) * (1 - ph)      # acuerdo que daria el puro azar
kappa = (acuerdo - esperado) / (1 - esperado)

print("acuerdo observado:", round(acuerdo, 2))
print("acuerdo por azar :", round(float(esperado), 3))
print("kappa            :", round(float(kappa), 2))
# (juez != humano).sum() cuenta las posiciones donde discrepan: 4 de 50
print("desacuerdos      :", int((juez != humano).sum()), "de", juez.size)
```

:::figura
fichero: evaluacion-acuerdo-y-kappa
pie: A la izquierda, la matriz de coincidencias de los 50 casos: el juez y el humano coinciden en 46 (la diagonal) y discrepan en 4. Ese 92 % es el número que suena a juez excelente. A la derecha, el mismo acuerdo puesto en su sitio: la línea azul es la fórmula del kappa resuelta para el acuerdo observado, y la línea de puntos marca el 52 % que saldría por puro azar con estas proporciones de etiquetas. El punto rojo es este juez: está muy por encima del azar, y esa distancia es el kappa 0,83. Fíjate en que subir el acuerdo bruto de 0,92 a 0,96 no movería el punto en vertical tanto como parece: lo que decide es cuánto se separa de la línea de puntos.
fuente: figuras/evaluacion-de-llms-1.py
:::

:::claves
- `juez == humano` compara **elemento a elemento** y devuelve un array de booleanos; `.mean()` de ese array (donde `True` vale 1) es la proporción de coincidencias. Es el 92 % que suena tan bien y engaña.
- `esperado = pj * ph + (1 - pj) * (1 - ph)` estima el acuerdo **por azar** a partir de las proporciones marginales: con un 60 % de unos, dos etiquetadores que respondieran al azar coincidirían en el 52 % de los casos. El kappa resta esa parte antes de juzgar.
- `kappa = (acuerdo - esperado) / (1 - esperado)` divide por lo que **quedaba por ganar**: si el acuerdo por azar fuera 1, la división sería por cero. Con estos números sale 0,83 y ya se puede comparar versiones del sistema, siempre que la diferencia buscada sea mayor que el ruido (4 desacuerdos en 50).
- El `float(...)` de la primera y la última línea es para convertir el escalar de NumPy en un `float` de Python: sin él, el valor se imprime como `np.float64(0.92)` y no se puede meter en un JSON.
- Esta validación mide el acuerdo con **un** anotador humano. Un juez con kappa 0,83 frente a un humano sigue sin estar calibrado frente a otro: para decidir entre dos versiones casi idénticas hace falta más de una muestra y más de un anotador.
:::

## Errores típicos

- **Usar un conjunto de prueba público como si fuera tuyo.** Es casi seguro que estuvo en el
  corpus de entrenamiento de algún modelo, así que mide recuerdo. Conjunto propio, escrito
  para tu caso de uso, y revisado por alguien que sepa del dominio.
- **Medir con el mismo conjunto con el que ajustas.** Probar 40 variantes de prompt contra los
  mismos 200 casos y quedarte con la mejor infla el resultado igual que en cualquier
  [[seleccion-de-hiperparametros|búsqueda de hiperparámetros]]: reserva una parte que no
  toques hasta la decisión final.
- **Confiar en un juez sin validarlo.** Un juez que prefiere respuestas largas te empujará a
  prompts que generan párrafos, no respuestas. Antes de usarlo, mide el acuerdo con
  anotaciones humanas en una muestra de 50 a 100 casos y comprueba que supera el azar.
- **Evaluar con una sola métrica.** Exactitud, `F1`, fidelidad a las fuentes, latencia y coste
  se mueven en direcciones distintas. Un cambio que sube la calidad puede triplicar el coste
  por consulta.
- **No convertir los fallos reales en casos.** Si un usuario reporta una respuesta mala y no
  se añade al conjunto, el mismo fallo volverá con el siguiente cambio de prompt. La
  evaluación que crece con los fallos es la única que mejora el sistema de verdad.
- **Comparar ejecuciones con prompts o parámetros distintos y atribuir la diferencia al
  modelo.** Si cambias a la vez el prompt, la temperatura y la versión del modelo, no sabes
  qué causó la mejora. Un cambio por experimento.
- **Mirar solo la media.** Dos sistemas con `F1` medio 0,8 pueden ser muy distintos: uno falla
  un poco en todos los casos y el otro acierta el 80 % y destrozó el 20 %. Mira la
  distribución y, sobre todo, los casos peores.

:::aviso
Una evaluación con 30 casos tiene intervalos de confianza enormes: una diferencia de dos
aciertos no significa nada. Antes de declarar que una versión es mejor, comprueba cuántos
casos tendrías que cambiar para que la conclusión se diera la vuelta.
:::

## Comprueba que lo sabes

:::quiz
p: Un juez automático coincide con los anotadores humanos en el 92 % de los casos y el acuerdo esperado por azar es 0,52. ¿Qué conclusión es correcta?
o: El juez es bueno, porque el 92 % es un acuerdo altísimo
o: El kappa es 0,83, así que el acuerdo es sustancial y el juez sirve para comparar versiones con diferencias grandes
o: El kappa es 0,40 y el juez no es fiable
a: 2
e: La coincidencia bruta engaña cuando las clases están desequilibradas: hay que descontar el acuerdo que produciría el azar. Con esos números, kappa = (0,92 − 0,52) / 0,48 = 0,83, un acuerdo sustancial. Aun así, sirve para detectar diferencias mayores que su ruido, no para decidir entre dos versiones casi idénticas.
:::

:::quiz
p: Un sistema saca exactitud 0,33 y F1 medio 0,56 en el mismo conjunto. ¿Qué significa?
o: Que una de las dos métricas está mal calculada
o: Que el sistema rara vez coincide palabra por palabra, pero su contenido se solapa bastante con la referencia
o: Que el sistema acierta un tercio y falla dos tercios de forma equivalente en las dos métricas
a: 2
e: Las dos métricas son correctas y miden cosas distintas: la exactitud exige coincidencia exacta tras normalizar, y el F1 premia el solapamiento parcial de tokens. Elegir una u otra cambia la historia que cuentas, así que la decisión debe depender del caso de uso.
:::

:::quiz
p: ¿Por qué hay que reservar casos que no se usen para ajustar el prompt?
o: Porque el conjunto de prueba se gasta con el uso
o: Porque elegir la mejor variante sobre el mismo conjunto infla el resultado, igual que en cualquier búsqueda de hiperparámetros
o: Porque los modelos aprenden de las evaluaciones que haces
a: 2
e: Con 40 variantes probadas contra 200 casos, la mejor puntuación incluye una parte de suerte: es el mismo problema de selección múltiple que en machine learning clásico. La solución es una partición que solo se toque en la decisión final. Los modelos no aprenden de tus evaluaciones; tu criterio sí se contamina.
:::
