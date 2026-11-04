---
id: z-score-y-estandarizacion
titulo: Z-score y estandarización
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [medidas-de-centralidad, medidas-de-dispersion]
tags: [estadistica, escalado, outliers]
resumen: El z-score dice a cuántas desviaciones típicas está un valor de la media; sirve para comparar escalas distintas y para detectar valores atípicos.
---

## En una frase

El z-score de un valor es cuántas desviaciones típicas le separan de la media: convierte
cualquier medida en «cuánto se sale de lo normal en su propio grupo» y permite comparar cosas
medidas en escalas que no tienen nada que ver.

## La idea

Dos estudiantes sacan un 8,9 y un 7,5. ¿Quién lo ha hecho mejor? Sin más datos, no se puede
decir. Si el primero estaba en un examen con media 6,5 y desviación típica 1,2, su nota está
2,00 desviaciones por encima de la media de su clase. Si el segundo estaba en un examen con
media 5,0 y desviación 0,8, la suya está 3,12 desviaciones por encima de la media de la suya. El
7,5 es mejor resultado **en su contexto**. El z-score es exactamente esa cuenta: cuántas
desviaciones típicas.

Es un cambio de unidades, como pasar de euros a «euros típicos». Nada más. Y de ahí salen sus
dos virtudes: puedes poner en la misma escala una altura en centímetros y un peso en kilos, y
puedes decir si un valor es raro sin conocer la escala original. Un z-score de 3 en un tiempo de
respuesta, en un salario o en un error de medida significa lo mismo: ese valor está muy lejos del
comportamiento habitual de su grupo.

Lo que el z-score **no** hace es cambiar la forma de los datos. Si la distribución era asimétrica
y con colas gordas, sigue siéndolo: la asimetría y la curtosis son idénticas antes y después
([[asimetria-y-curtosis]]). Estandarizar no normaliza nada. Y hay un detalle que se cobra caro en
machine learning: si calculas la media y la desviación con **todos** los datos y luego divides en
entrenamiento y prueba, la información del conjunto de prueba se ha colado en el entrenamiento
([[fuga-de-datos]]). La media y la desviación se calculan solo con el entrenamiento y se aplican
al resto.

La versión robusta cambia la media por la mediana y la desviación por el MAD multiplicado por
1,4826, el factor que hace que en una distribución normal dé lo mismo que la desviación típica.
Con datos muy asimétricos funciona mejor, porque un solo valor enorme no infla el denominador
hasta esconder a los demás.

## Definición formal

Con una observación `x`, la media `μ` (o `x̄` en una muestra) y la desviación típica `σ` (o `s`):

:::formula
z = (x − μ) / σ        z_robusto = (x − mediana) / (1,4826 · MAD)
:::

- `x` — el valor que quieres situar.
- `μ` — la media de la población de referencia; `x̄` si trabajas con una muestra.
- `σ` — la desviación típica de esa población; `s` si es una muestra.
- `z` — el resultado, en unidades de desviación típica. También se llama **puntuación típica**.
- `MAD` — la desviación absoluta mediana: la mediana de los valores absolutos de `xᵢ − mediana`.
- El factor `1,4826` es `1/Φ⁻¹(0,75)` y sirve para que la versión robusta coincida con `σ`
  cuando los datos son normales.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x` | El valor que quieres situar dentro de su grupo | las de la variable (notas, cm, euros) | Al subir `x`, el z-score sube en proporción: cada unidad de la variable suma `1/σ` al resultado. Es una transformación afín, así que el orden de los datos no cambia |
| `μ` | Media de la población de referencia; `x̄` si es una muestra | las de la variable | Al subir la media del grupo, el z-score del mismo `x` baja: el listón está más alto. Restar `μ` es lo que centra los datos en cero |
| `σ` | Desviación típica de la población; `s` si es una muestra | las de la variable | Al subir `σ`, todos los z-scores se acercan a cero: el grupo es tan disperso que casi nada llama la atención. Con `σ` inflada por unos pocos valores extremos, el z-score clásico deja de detectar lo que sí es raro |
| `z` | El resultado: cuántas desviaciones típicas separan `x` de la media | adimensional (desviaciones típicas) | Al subir, el dato está más lejos de su grupo: por convenio se marcan los que superan 3 en valor absoluto. No es una probabilidad: en una normal `z = 2` deja un 2,3 % por encima, pero con colas gordas ese porcentaje puede ser diez veces mayor |
| `x̄` | Media muestral, la que se usa cuando no tienes la población | las de la variable | Solo se puede calcular con datos; es el estimador de `μ`. En un modelo, calcularla con todo el conjunto antes de separar entrenamiento y prueba filtra información del test: eso es fuga de datos |
| `MAD` | Desviación absoluta mediana: la mediana de las distancias a la mediana | las de la variable | Al subir, los datos se alejan del centro, pero un valor extremo no la infla como infla a `σ`. Es la razón de que el z-score robusto siga discriminando con ingresos o latencias |
| `1,4826` | El factor que lleva el MAD a la escala de `σ` en una distribución normal | adimensional | Es una constante, no un parámetro. Si los datos no son normales, deja de haber equivalencia: el z-score robusto y el clásico miden cosas parecidas, pero no son el mismo número |
| `mín`, `máx` | El mínimo y el máximo de la variable (normalización min-max) | las de la variable | Aquí sí manda un valor extremo: si el máximo se dispara, todos los datos se apelotonan cerca de cero. Deja los datos en `[0, 1]`, pero depende por completo de dos observaciones |
:::

Propiedades:

- **Media 0 y desviación 1.** Si estandarizas un conjunto con su propia media y su propia
  desviación poblacional, el resultado tiene media 0 y desviación típica 1 exactas.
- **Invarianza a la escala.** Sumar una constante o multiplicar por una constante positiva no
  cambia el z-score: `x` y `100·x + 7` dan el mismo `z` para cada observación. Por eso el z-score
  es la forma correcta de comparar variables con unidades distintas.
- **No cambia la forma.** Asimetría, curtosis y orden de los datos se conservan.
- **Regla empírica** (solo si los datos son aproximadamente normales): alrededor del 68 % de los
  valores cae entre `z = −1` y `z = 1`, el 95 % entre −2 y 2, y el 99,7 % entre −3 y 3.
- **Desigualdad de Chebyshev** (válida siempre que exista la varianza): al menos una fracción
  `1 − 1/z²` de los datos está a menos de `z` desviaciones de la media. Para `z = 2`, al menos el
  75 %, sin suponer normalidad.
- **Normalización min-max** es otra cosa: `x' = (x − mín) / (máx − mín)` deja los datos en
  `[0, 1]` y depende por completo de los dos extremos. Se usa cuando el algoritmo necesita un
  rango acotado, no cuando quieres comparar con un grupo de referencia.

## Ejemplo

Comparar dos exámenes con dificultad distinta. El primer examen tiene media 6,5 y desviación
típica 1,2; el segundo, media 5,0 y desviación 0,8.

- Nota 8,9 en el primer examen: `z = (8,9 − 6,5) / 1,2 = 2,00`.
- Nota 7,5 en el segundo: `z = (7,5 − 5,0) / 0,8 = 3,125`.

El 7,5 está más lejos de su grupo que el 8,9 del suyo. Y al revés: una nota de 4,1 en el primer
examen da `z = (4,1 − 6,5) / 1,2 = −2,00`, igual de lejos por abajo que el 8,9 por arriba.

Otro caso, con alturas: una persona de 175 cm en un grupo con media 170 y desviación 10 tiene
`z = 0,50`; otra de 165 cm en un grupo con media 158 y desviación 6 tiene `z = 1,17`. La segunda
es más alta **para su grupo** aunque mida diez centímetros menos.

Y el caso en el que el z-score engaña: con ingresos mensuales muy asimétricos, un sueldo de
20.000 euros en un grupo con media 2.000 y desviación 3.000 da `z = 6,0`, mientras que en la
versión robusta (mediana 1.800 y MAD 500) da `(20.000 − 1.800) / (1,4826 · 500) = 24,5`. Los dos
números dicen «muy alto», pero el primero está artificialmente recortado porque unos pocos
sueldos altos inflaron la desviación típica. Con colas largas, la versión robusta discrimina
mejor.

:::figura
fichero: z-score-dos-examenes-en-un-eje
pie: Arriba, los dos exámenes con su propia regla: el 8,9 está a dos desviaciones de la media de un examen fácil, y el 7,5 se sale de donde llega casi nadie en uno difícil. Abajo, las dos notas pasadas a z, ya en el mismo eje: 2,00 frente a 3,12. La regla es que el z-score no cambia el dato, cambia la unidad en la que se lee, y por eso permite comparar un 7,5 con un 8,9 sin preguntar de qué examen salieron.
fuente: figuras/z-score-y-estandarizacion-1.py
:::

## Código

```python verificable
# Dos examenes con dificultad distinta: el z-score los pone en la misma escala
facil = (6.5, 1.2)      # media y desviacion tipica del examen facil
dificil = (5.0, 0.8)    # y las del examen dificil

print("facil   8.9 -> z", round((8.9 - facil[0]) / facil[1], 4))       # -> 2.0
print("facil   4.1 -> z", round((4.1 - facil[0]) / facil[1], 4))       # -> -2.0
print("dificil 7.5 -> z", round((7.5 - dificil[0]) / dificil[1], 4))   # -> 3.125
print("dificil 8.9 -> z", round((8.9 - dificil[0]) / dificil[1], 4))   # -> 4.875
```

:::claves
- Aquí `facil = (6.5, 1.2)` es una **tupla**, no una lista: se puede leer por posición (`facil[0]`) pero no se puede modificar. Para un par de números que no van a cambiar es la opción correcta; si intentaras `facil[0] = 7.0` saltaría un `TypeError`.
- El paréntesis en `(8.9 - facil[0]) / facil[1]` no es decorativo: si lo quitas, la división se aplica solo a `facil[0]` y el resultado sale mal sin ningún aviso. La precedencia de `/` sobre `-` es la trampa clásica de esta fórmula.
- `round(x, 4)` en Python redondea al par más cercano (redondeo bancario): `round(2.00005, 4)` puede devolver `2.0` o `2.0001` según la representación binaria. Para comparar resultados con tests, usa `pytest.approx` o compara la diferencia, nunca la igualdad exacta.
- `StandardScaler` calcula la media y la desviación con `ddof=0`, igual que `np.std` sin argumentos. Por eso `z.std()` sale 1,0; en cambio `notas.std()` vale 1,4741 (el número que imprime el bloque) y `notas.std(ddof=1)` vale 1,5635, y `z.std(ddof=1)` daría algo mayor que 1: el escalador no usa la corrección de Bessel.
- `notas.reshape(-1, 1)` convierte el vector de nueve notas en una matriz de 9 filas y 1 columna, que es lo que espera sklearn. El `-1` significa «calcula tú esa dimensión»; si te equivocas de orden (`(1, -1)`), sklearn acepta la forma y escala **una sola fila**, que es un error silencioso.
- `fit_transform` aprende la media y la desviación y las aplica en la misma llamada. En un flujo real hay que usar `fit` con el entrenamiento y `transform` con la prueba: `fit_transform` sobre todo el conjunto es la fuga de datos que describe la página.
:::

```python verificable
import numpy as np
from sklearn.preprocessing import StandardScaler

notas = np.array([4.0, 5.5, 6.0, 6.5, 6.5, 7.0, 7.5, 8.0, 9.5]).reshape(-1, 1)
z = StandardScaler().fit_transform(notas).ravel()

# La media de las z es 0 y su desviacion 1: es el mismo dato en otras unidades
print("media notas", round(float(notas.mean()), 4))        # -> 6.7222
print("sd notas   ", round(float(notas.std()), 4))         # -> 1.4741
print("media z    ", abs(round(float(z.mean()), 12)))      # -> 0.0
print("sd z       ", round(float(z.std()), 4))             # -> 1.0
print("z de 9.5   ", round(float(z[-1]), 4))               # -> 1.8844
```

```python verificable
import numpy as np

# Ingresos con cola larga: el z-score clasico se queda corto porque sigma esta inflada
rng = np.random.default_rng(0)
ingresos = rng.lognormal(mean=10.0, sigma=0.6, size=5000)
valor = 100_000.0

z_clasico = (valor - ingresos.mean()) / ingresos.std()
mad = np.median(np.abs(ingresos - np.median(ingresos)))
z_robusto = (valor - np.median(ingresos)) / (1.4826 * mad)

print("media   ", round(float(ingresos.mean())))        # -> 26254
print("sd      ", round(float(ingresos.std())))         # -> 16934
print("mediana ", round(float(np.median(ingresos))))    # -> 21664
print("MAD     ", round(float(mad)))                    # -> 8464
print("z clasico", round(float(z_clasico), 2))          # -> 4.35
print("z robusto", round(float(z_robusto), 2))          # -> 6.24
```

## Errores típicos

- **Leer el z-score como una probabilidad.** `z = 2` no significa «el 2 %»: en una normal, deja
  un 2,3 % por encima, pero con colas gordas ese porcentaje puede ser diez veces mayor. El
  z-score da una distancia, no una probabilidad.
- **Estandarizar con la media y la desviación de todos los datos antes de separar entrenamiento y
  prueba.** La media del conjunto de prueba se ha metido en el modelo: es una fuga clásica. El
  escalador se ajusta con el entrenamiento y se aplica al resto.
- **Creer que estandarizar normaliza la distribución.** Solo cambia las unidades. Una distribución
  asimétrica sigue igual de asimétrica, y una variable bimodal sigue teniendo dos montañas.
- **Usar media y desviación con datos muy asimétricos.** Un solo valor extremo infla `s` y hace
  que los demás parezcan normales. Con ingresos, precios o latencias, mediana y MAD.
- **Estandarizar variables con desviación casi nula.** Si una columna es prácticamente constante,
  dividir entre `s ≈ 0` produce z-scores enormes a partir de ruido de redondeo. Hay que decidir
  qué hacer con esas columnas antes, no después.
- **Aplicar la regla 68-95-99,7 sin comprobar la forma.** Es una propiedad de la normal. Con
  retornos financieros, la proporción de días fuera de `±3σ` es bastante mayor que el 0,3 % que
  predice la regla ([[distribuciones-en-datos-reales]]).
- **Estandarizar variables binarias o categóricas codificadas con números.** Un indicador de
  0 y 1 ya está en una escala interpretable; estandarizarlo no aporta nada y complica la lectura
  de los coeficientes.

:::truco
Umbral de trabajo habitual para marcar valores atípicos: `/z/ > 3` con datos aproximadamente
simétricos, y `/z_robusto/ > 3,5` con datos de cola larga. Son reglas de triaje para mirar casos
uno a uno, no un veredicto: un valor atípico puede ser el fenómeno más interesante del dataset
([[outliers-y-deteccion]]).
:::

:::practica
enunciado: Un piso de 120 m² está en un barrio con media 95 m² y desviación 12,5; otro de 150 m², en uno con media 130 y desviación 25. Calcula los dos z-scores y decide cuál es más grande para su barrio.
pista: El z-score mide la distancia a la media en unidades de desviación típica; al dividir, las unidades se cancelan.
solucion: z₁ = (120 − 95)/12,5 = 25/12,5 = 2,00. z₂ = (150 − 130)/25 = 20/25 = 0,80. El piso de 120 m² está dos desviaciones por encima de su barrio y el de 150 solo 0,8: en términos relativos el pequeño es más atípico, aunque en metros sea menor. Con datos simétricos, un /z/ mayor que 2 ya es poco frecuente.
:::

## Comprueba que lo sabes

:::quiz
p: Un test tiene media 70 y desviación típica 8. ¿Qué vale el z-score de una puntuación de 86?
o: 1,0
o: 2,0
o: 16,0
o: 0,86
a: 2
e: z = (86 − 70) / 8 = 2,0, es decir, dos desviaciones típicas por encima de la media. La opción 16 es la diferencia sin dividir entre la desviación, y 0,86 es dividir la puntuación entre 100: un escalado que no resta la media y por eso no mide distancia a nada.
:::

:::quiz
p: ¿Qué le hace la estandarización a una distribución muy asimétrica?
o: La vuelve simétrica, porque centra los datos en cero
o: Nada: cambia las unidades, pero conserva la asimetría y la curtosis
o: Recorta los valores atípicos al rango de más menos 3
o: Reduce su varianza a 1 y su asimetría a 0
a: 2
e: Restar la media y dividir entre la desviación es una transformación lineal: el orden y la forma se conservan. La asimetría y la curtosis son invariantes ante un cambio de escala positivo, así que siguen ahí. Si los datos tienen cola larga, siguen teniéndola.
:::

:::quiz
p: ¿Por qué se calcula la media y la desviación del escalador solo con el conjunto de entrenamiento?
o: Porque así el escalado es más rápido de calcular
o: Porque usar todo el conjunto filtra información del conjunto de prueba al entrenamiento
o: Porque la media del conjunto de prueba suele ser cero
o: Porque el conjunto de prueba no tiene media definida
a: 2
e: Si la media y la desviación se calculan con todos los datos, cada predicción sobre el conjunto de prueba incorpora un resumen de ese conjunto: es fuga de datos y la métrica sale optimista. En producción, además, solo tendrás los datos de entrenamiento para fijar el escalado.
:::
