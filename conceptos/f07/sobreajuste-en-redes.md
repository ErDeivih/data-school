---
id: sobreajuste-en-redes
titulo: Sobreajuste en redes
fase: 7
nivel: intermedio
rutas: [ds]
prerequisitos: [perceptron-y-mlp, sesgo-varianza, train-val-test]
tags: [deep-learning, regularizacion, entrenamiento]
resumen: Aprender a leer las dos curvas de un entrenamiento para detectar sobreajuste y decidir en que orden tocar datos, regularización y capacidad.
fuentes: ["Goodfellow, Bengio y Courville (2016), 'Deep Learning', cap. 7", "Prechelt (1998), 'Early Stopping - But When?'"]
---

## En una frase

Una red sobreajusta cuando aprende de memoria el ruido de los ejemplos de entrenamiento: la
pérdida de entrenamiento sigue bajando, pero la de validación toca fondo y empieza a subir, y
la diferencia entre las dos es la señal de alarma.

## La idea

Piensa en alguien que prepara una oposición memorizando las respuestas de los exámenes de los
cinco años anteriores. En esos exámenes saca un 10. Le cambias una cifra a un problema y
falla. No ha aprendido el método, ha aprendido las respuestas. Una red neuronal hace
exactamente eso si le das suficiente capacidad y pocos ejemplos: con millones de pesos puede
memorizar etiquetas aleatorias.

Lo importante es que **el sobreajuste se detecta comparando dos números, no mirando uno**. La
pérdida de entrenamiento casi siempre baja: es lo que el optimizador está minimizando
directamente, y con capacidad suficiente acaba cerca de cero aunque las etiquetas sean ruido
puro. La pregunta útil es qué hace mientras tanto la pérdida de un conjunto que la red no ha
visto.

Al principio las dos curvas bajan juntas: la red aprende el patrón que comparten los dos
conjuntos. Llega un punto en el que ese patrón ya está aprendido y lo único que queda en el
conjunto de entrenamiento es su ruido particular: el píxel concreto de esa foto, la fluctuación
de ese día. Ahí la curva de entrenamiento sigue bajando y la de validación se aplana y sube. Ese
punto de inflexión responde a «¿cuándo paro y qué toco?».

El orden en que se tocan las cosas importa más que la lista de remedios:

1. **Comprueba que la partición es limpia.** Si hay fuga de datos entre entrenamiento y
   validación, el sobreajuste que crees ver (o que no ves) es mentira. Antes de regularizar,
   revisa que ninguna variable se calculó con información del futuro ni con estadísticos de
   todo el conjunto.
2. **Consigue más datos o aumenta los que tienes.** Es lo único que ataca la causa. Voltear,
   recortar, añadir ruido o mezclar ejemplos cuando el problema lo permite vale más que
   cualquier truco de regularización.
3. **Regulariza.** Penalización L2 sobre los pesos, [[dropout-y-regularizacion|dropout]],
   parada temprana y, si el modelo es grande, aumento de datos. Es barato y suele bastar.
4. **Reduce capacidad o complica la tarea.** Menos capas, menos unidades, menos variables de
   entrada. O al contrario: si el problema admite más datos etiquetados, invierte el esfuerzo
   ahí en vez de recortar el modelo.
5. **Ajusta el entrenamiento.** Menos épocas (parada temprana), una
   [[tasas-de-aprendizaje-y-schedulers|tasa de aprendizaje]] con decaimiento y una selección de
   hiperparámetros honesta.

El error de orden más común es empezar por el punto 5. Bajar la tasa de aprendizaje hace que
las dos curvas bajen más despacio: no arregla el sobreajuste, solo retrasa el momento en que
aparece.

:::figura
fichero: sobreajuste-curvas-y-capacidad
pie: A la izquierda, por qué el sobreajuste se lee y no se mide: la curva azul de entrenamiento baja en todas las épocas, y la roja de validación toca fondo hacia la época 600 y de ahí en adelante sube. El mínimo de la curva roja es la época que se guarda; si te quedas con el modelo del final, la validación es un 8 % peor habiendo entrenado 2.400 épocas de más. La línea de puntos marca el ruido irreducible (0,3² = 0,09): todo lo que la curva de entrenamiento baja por debajo de ahí es memorización, no aprendizaje. A la derecha, el mismo fenómeno visto por capacidad: hasta 16 unidades la validación mejora, y a partir de ahí empeora mientras el entrenamiento sigue bajando. Ese es el motivo de que «más capacidad» no sea la respuesta y de que contar parámetros no decida nada.
fuente: figuras/sobreajuste-en-redes-1.py
:::

## Definición formal

Con un conjunto de entrenamiento de `n` ejemplos `(xᵢ, yᵢ)` y un conjunto de validación de `m`
ejemplos `(x'ⱼ, y'ⱼ)`, y una red con parámetros `θ`:

:::formula
L_train(θ) = (1/n) · Σᵢ ℓ(f(xᵢ; θ), yᵢ)     L_val(θ) = (1/m) · Σⱼ ℓ(f(x'ⱼ; θ), y'ⱼ)
:::

- `f(x; θ)` — la salida de la red para la entrada `x` con los parámetros `θ`.
- `ℓ(·, ·)` — la pérdida de un ejemplo; por ejemplo la
  [[funciones-de-perdida|entropía cruzada]] en clasificación. La escribo como `ℓ` para no
  confundirla con la pérdida media `L`.
- `n`, `m` — número de ejemplos de entrenamiento y de validación.
- `L_train`, `L_val` — pérdida media sobre cada conjunto.
- **Hueco de generalización:** `G(θ) = L_val(θ) − L_train(θ)`. Mide cuánto peor va la red en
  datos que no ha visto.

Dos definiciones operativas, que son las que se usan de verdad:

- **Época óptima de parada:** `e* = argmin_e L_val(θ_e)`, donde `θ_e` son los parámetros
  después de `e` épocas. Se guarda el modelo de `e*`, no el del final.
- **Regularización L2 (weight decay):** se minimiza `L_train(θ) + (λ/2) · ‖θ‖²`, con `λ` el
  coeficiente de penalización (0 = sin regularizar) y `‖θ‖²` la suma de todos los pesos al
  cuadrado. Cuanto mayor es `λ`, más se sacrifica ajuste en entrenamiento a cambio de pesos
  más pequeños.

Tres matices que casi nunca se dicen:

1. **El hueco solo es interpretable si las dos pérdidas miden lo mismo.** Si tu conjunto de
   validación tiene otra distribución, otro ruido de etiquetado o está desbalanceado de otra
   forma, la diferencia entre las curvas mezcla el sobreajuste con esas diferencias.
2. **El criterio no es el signo del hueco, es la tendencia.** Un hueco negativo (validación
   mejor que entrenamiento) es perfectamente normal al principio, porque el conjunto de
   validación puede ser por azar algo más fácil. Lo que delata el sobreajuste es que la curva
   de validación **deje de bajar y suba** mientras la de entrenamiento sigue bajando.
3. **La capacidad efectiva no son los parámetros.** Una red muy grande con parada temprana,
   aumento de datos y penalización L2 puede generalizar mejor que una red pequeña entrenada
   hasta el final. Contar parámetros no decide nada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L_train` | Pérdida media sobre el conjunto de entrenamiento | las de la pérdida (adimensional si es entropía cruzada) | Es la curva que el optimizador minimiza directamente, así que casi siempre baja. Al subir mientras la validación también sube, el modelo está infraajustando: falta capacidad, épocas o mejores variables |
| `L_val` | La misma pérdida media, medida sobre ejemplos que el modelo no ha visto | las de la pérdida | Es la curva que informa. Sube por encima de su mínimo cuando la red empieza a memorizar: en el ejemplo pasa de 0,0936 en la época 600 a 0,1011 al final, un 8 % peor |
| `G` | Hueco de generalización: `L_val − L_train` | las de la pérdida | Cuanto mayor, más depende el modelo de haber visto el ejemplo. Ojo: el signo no decide nada (al principio puede ser negativo porque la validación es más fácil por azar); lo que decide es que la curva de validación **deje de bajar y suba** |
| `n`, `m` | Ejemplos de entrenamiento y de validación | recuento | Más `n` es lo único que ataca la causa del sobreajuste: reduce el hueco sin sacrificar ajuste. Más `m` no mejora el modelo, pero hace la estimación de `L_val` menos ruidosa y evita elegir la época de parada por una casualidad |
| `θ` | Todos los parámetros de la red (pesos y sesgos) | las de cada peso | Es lo que se aprende. Más parámetros dan más capacidad de memorizar: con suficientes pesos, una red ajusta etiquetas aleatorias hasta pérdida casi cero, que es justo el síntoma que hay que detectar |
| `e*` | Época de parada: el `e` que minimiza `L_val` | épocas (recuento) | Se elige **después** de mirar la curva, no antes. Si subes `e*` más allá del mínimo, mejoras el entrenamiento y empeoras la validación; el modelo que se guarda es el de `e*`, no el último |
| `λ` | Coeficiente de la penalización L2 sobre los pesos | adimensional (0 = sin regularizar) | Con `λ` mayor, los pesos se encogen y el modelo sacrifica ajuste en entrenamiento a cambio de generalizar mejor: en el ejemplo, `λ = 0,01` empeora el entrenamiento (0,0910 → 0,0938) y mejora la validación (0,0990 → 0,0947), y el hueco casi desaparece. Demasiado `λ` lleva al otro extremo, el infraajuste |
| `‖θ‖²` | La suma de todos los pesos al cuadrado | las de los pesos al cuadrado | Es lo que se penaliza. Al crecer, la penalización aprieta más fuerte. No incluye los sesgos, y esa omisión es deliberada: penalizar los sesgos estorba sin mejorar la generalización |
:::

## Ejemplo

Estas curvas son la salida real del primer bloque de código, redondeadas a cuatro decimales:
misma red (1 entrada, 16 unidades ocultas con `tanh`, 1 salida), 60 ejemplos de entrenamiento
y 60 de validación, ambos con el mismo ruido gaussiano de desviación 0,3.

```text
epoca  300  train 0.1361  validacion 0.1036
epoca  600  train 0.1011  validacion 0.0936
epoca  900  train 0.0942  validacion 0.0973
epoca 1200  train 0.0910  validacion 0.0990
epoca 1500  train 0.0886  validacion 0.0996
epoca 1800  train 0.0866  validacion 0.0999
epoca 2100  train 0.0849  validacion 0.1002
epoca 2400  train 0.0834  validacion 0.1005
epoca 2700  train 0.0821  validacion 0.1008
epoca 3000  train 0.0810  validacion 0.1011
```

Como se lee:

- La pérdida de entrenamiento baja en las diez comprobaciones: 0,1361 → 0,0810. Si solo mirases
  esa columna, concluirías que entrenar más siempre mejora.
- La de validación baja hasta la época 600 (0,0936) y a partir de ahí sube de forma monótona
  hasta 0,1011. El mínimo marca la época de parada.
- La pérdida de validación ya no baja del ruido irreducible: con ruido de desviación 0,3, el
  error cuadrático que no se puede evitar es 0,3² = 0,09. Todo lo que baja por debajo de 0,09
  en entrenamiento es memorización.
- Si paras en la época 600, te quedas con una validación de 0,0936; si entrenas hasta el final,
  acabas en 0,1011. Un 8 % peor por seguir entrenando 2.400 épocas de más.

Y fíjate en el detalle incómodo: en la época 600 el hueco es **negativo**
(0,0936 − 0,1011 = −0,0075). No pasa nada: el conjunto de validación es algo más fácil. Por eso
el criterio es la forma de la curva de validación, no el signo del hueco.

## Código

```python verificable
import numpy as np

# Curvas reales de un entrenamiento pequeno: 60 ejemplos de entrenamiento y 60 de validacion,
# la misma red (1 -> 16 -> 1) y el mismo ruido en los dos conjuntos.
rng = np.random.default_rng(0)
x = np.linspace(-3, 3, 60).reshape(-1, 1)
y = np.sin(x) + rng.normal(0, 0.3, x.shape)
xv = np.linspace(-3, 3, 60).reshape(-1, 1)
yv = np.sin(xv) + rng.normal(0, 0.3, xv.shape)

W1 = rng.normal(0, 1.0, (1, 16)) / 3; b1 = np.zeros(16)
W2 = rng.normal(0, 1.0, (16, 1)) / 4; b2 = np.zeros(1)

def mse(X, Y):
    return float(np.mean((np.tanh(X @ W1 + b1) @ W2 + b2 - Y) ** 2))

curva = []
for epoca in range(1, 3001):
    h = np.tanh(x @ W1 + b1)
    g = 2 * (h @ W2 + b2 - y) / x.size
    gh = (g @ W2.T) * (1 - h ** 2)
    W2 -= 0.02 * h.T @ g; b2 -= 0.02 * g.sum(0)
    W1 -= 0.02 * x.T @ gh; b1 -= 0.02 * gh.sum(0)
    if epoca % 300 == 0:
        curva.append((epoca, mse(x, y), mse(xv, yv)))

for epoca, tr, va in curva:
    print(f"epoca {epoca:>4}  train {tr:.4f}  validacion {va:.4f}")

mejor = min(curva, key=lambda c: c[2])
print(f"mejor validacion en la epoca {mejor[0]}  ({mejor[2]:.4f})")          # -> 600  (0.0936)
print(f"al final, train {curva[-1][1]:.4f}  validacion {curva[-1][2]:.4f}")  # -> 0.0810  0.1011
```

:::claves
- `x = np.linspace(-3, 3, 60).reshape(-1, 1)` tiene que ser **bidimensional** (60, 1) para que `x @ W1` funcione. El `reshape(-1, 1)` es el que añade la columna que falta: con un vector plano de 60 elementos, `x @ W1` sería producto matriz-vector y las formas de `gh` no cuadrarían. El `-1` le dice a NumPy que calcule esa dimensión sola.
- `rng.normal(0, 0.3, x.shape)` genera el ruido con la **misma forma** que `x`, no un vector plano. Si usaras `60` en lugar de `x.shape` saldría igual por casualidad, pero en cuanto cambies el número de ejemplos el array dejaría de encajar y el error aparecería en una resta, lejos de la línea que lo causó.
- El bucle actualiza los pesos **en el sitio** (`W2 -= 0.02 * h.T @ g`): `-=` sobre un array de NumPy modifica el array original, no crea uno nuevo. Por eso `W1`, `b1`, `W2` y `b2` conservan los cambios entre iteraciones, que es exactamente lo que se busca.
- `g = 2 * (h @ W2 + b2 - y) / x.size` divide entre `x.size`, que es 60, no entre `x.shape[0]`, que también es 60. Con una matriz de dos columnas `x.size` sería 120 y la pérdida media cambiaría de escala: es un detalle que muerde en cuanto el problema tiene más de una variable.
- `(1 - h ** 2)` es la derivada de `tanh` escrita como `1 - tanh²`. Si cambiaras `np.tanh` por otra activación y dejaras esta línea igual, el gradiente sería el de otra función y el entrenamiento no bajaría: es el error de copiar y pegar una red cambiando solo la activación del `forward`.
- La primera comprobación del bucle es `if epoca % 300 == 0`, así que se guardan 10 puntos de 3.000 épocas. La curva de validación tiene ruido de una época a otra, y mirar todos los pasos invita a parar en un mínimo local que es solo ruido: por eso se suele suavizar o muestrear antes de decidir `e*`.
:::

```python verificable
import numpy as np

# La validacion lleva su propio ruido independiente: asi las dos perdidas miden lo mismo
# y el hueco (val - train) significa algo.
def entrena(wd, lr=0.02, epochs=1200):
    rng = np.random.default_rng(0)
    x = np.linspace(-3, 3, 60).reshape(-1, 1)
    y = np.sin(x) + rng.normal(0, 0.3, x.shape)
    xv = np.linspace(-3, 3, 60).reshape(-1, 1)
    yv = np.sin(xv) + rng.normal(0, 0.3, xv.shape)

    W1 = rng.normal(0, 1.0, (1, 16)) / 3; b1 = np.zeros(16)
    W2 = rng.normal(0, 1.0, (16, 1)) / 4; b2 = np.zeros(1)

    for _ in range(epochs):
        h = np.tanh(x @ W1 + b1)
        g = 2 * (h @ W2 + b2 - y) / x.size
        gW2 = h.T @ g + wd * W2                      # wd * W2 es el gradiente de (wd/2) * ||W||^2
        gh = (g @ W2.T) * (1 - h ** 2)
        gW1 = x.T @ gh + wd * W1
        W1 -= lr * gW1; b1 -= lr * gh.sum(0)
        W2 -= lr * gW2; b2 -= lr * g.sum(0)

    htr = np.tanh(x @ W1 + b1); hva = np.tanh(xv @ W1 + b1)
    return float(np.mean((htr @ W2 + b2 - y) ** 2)), float(np.mean((hva @ W2 + b2 - yv) ** 2))

for wd in (0.0, 0.003, 0.01):
    tr, va = entrena(wd)
    print(f"weight decay {wd:.3f}  train {tr:.4f}  val {va:.4f}  hueco {va - tr:+.4f}")
# -> 0.000  train 0.0910  val 0.0990  hueco +0.0080
# -> 0.003  train 0.0916  val 0.0975  hueco +0.0059
# -> 0.010  train 0.0938  val 0.0947  hueco +0.0009
```

:::claves
- `wd * W2` es el gradiente de `(wd/2) * ‖W‖²` y por eso aparece sin el 2: la derivada de `(wd/2)·W²` es `wd·W`. El comentario de la línea lo dice porque es el sitio donde más se equivoca la gente: si pones `wd * W2 / 2` estás regularizando la mitad de lo que crees.
- `entrena` vuelve a llamar a `np.random.default_rng(0)` **dentro** de la función, así que las tres llamadas parten de los mismos datos y de la misma inicialización. Es lo que hace comparables las tres filas: sin eso, la diferencia entre `wd = 0` y `wd = 0,01` mezclaría el efecto de la regularización con el de otra semilla.
- La comparación entre las tres filas solo significa algo porque los tres entrenamientos son el mismo salvo `wd`: mismos datos, mismos pesos iniciales, mismas épocas y misma tasa. Si cambiaras `epochs` en una llamada, ya no podrías atribuir la diferencia al weight decay.
- Ni `b1` ni `b2` llevan término de penalización: los sesgos se dejan fuera del weight decay a propósito, porque encogerlos estorba sin mejorar la generalización. Si añadieras `wd * b2` a la actualización de `b2`, la validación empeoraría.
- El hueco se imprime con `{va - tr:+.4f}`, y ese `+` del formato fuerza a imprimir el signo aunque sea positivo; sin él, `+0.0080` saldría como `0.0080` y se perdería la lectura de si la validación va por encima o por debajo del entrenamiento.
- `return` devuelve una **tupla** de dos floats, no un array: `float(np.mean(...))` convierte el escalar de NumPy en un `float` de Python. El desempaquetado `tr, va = entrena(wd)` funciona por eso, y el `(tr, va)` es el orden en que se declaran, no alfabético: leerlo al revés cambia por completo la conclusión del bloque.
:::

La segunda tabla es la lección de «qué tocar primero»: penalizar los pesos **empeora** el
entrenamiento (0,0910 → 0,0938) y **mejora** la validación (0,0990 → 0,0947). El hueco pasa de
0,0080 a 0,0009, casi desaparece, sin tocar la arquitectura ni los datos. Y las tres cifras de
partida coinciden con la fila de 1.200 épocas de la tabla anterior: es el mismo entrenamiento.

## Errores típicos

- **Mirar solo la pérdida de entrenamiento.** Es la curva que siempre baja y la que menos
  información da. Si no tienes un conjunto de validación separado y congelado, no puedes
  detectar sobreajuste: solo puedes ver que la red aprende.
- **Usar la pérdida de validación como resultado final.** Si elegiste la época con ella, esa
  pérdida está sesgada a la baja: has seleccionado el mínimo de una curva ruidosa. El número
  que se reporta se mide en un tercer conjunto que no hayas tocado, o con
  [[validacion-cruzada|validación cruzada]] bien hecha.
- **Empezar por la tasa de aprendizaje.** Bajarla hace que las dos curvas vayan más despacio,
  no que se separen menos. El sobreajuste se combate con datos, regularización o menos
  capacidad; la tasa de aprendizaje se ajusta por otros motivos (inestabilidad, divergencia).
- **Regularizar un modelo que está infraajustando.** Si la pérdida de entrenamiento sigue alta
  y la de validación está pegada a ella, el problema es el contrario: más capacidad, más
  épocas, mejor tasa de aprendizaje o mejores variables. Añadir dropout ahí solo empeora las
  dos curvas.
- **Olvidar desactivar el dropout y el modo de entrenamiento al evaluar.** Si mides la
  validación con dropout activo y con las estadísticas de
  [[normalizacion-por-lotes|normalización por lotes]] actualizándose, la curva de validación es
  ruidosa y sistemáticamente peor; puedes concluir que sobreajusta cuando lo que pasa es que
  estás evaluando mal.
- **Confundir sobreajuste con desbalanceo.** Una exactitud de validación baja con pérdida
  estable no es sobreajuste: puede ser una métrica inadecuada para clases raras. Mira la
  [[metricas-de-clasificacion|matriz de confusión]] antes de tocar la regularización.

:::practica
enunciado: Un entrenamiento da estas pérdidas: época 500, train 0,200 y validación 0,180; época 1000, train 0,140 y validación 0,150; época 2000, train 0,080 y validación 0,190. ¿En qué época paras, cuánto vale ahí el hueco de generalización y qué porcentaje empeora la validación si llegas a la 2000?
pista: El hueco es validación menos entrenamiento; su signo no decide nada, lo que decide es la época en que la validación deja de bajar.
solucion: La validación mínima es 0,150 en la época 1000 (0,180 en la 500 y 0,190 en la 2000), así que paras ahí. El hueco es 0,150 − 0,140 = +0,010. Siguiendo hasta la 2000, la validación empeora (0,190 − 0,150) / 0,150 = 26,7 %, mientras el entrenamiento baja hasta 0,080. Conclusión: guarda el modelo de la época 1000.
:::

## Comprueba que lo sabes

:::quiz
p: Durante el entrenamiento, la pérdida de entrenamiento baja de 0,14 a 0,08 y la de validación baja de 0,10 a 0,09 y luego sube a 0,10. ¿Qué haces?
o: Seguir entrenando, porque la pérdida de entrenamiento todavía baja
o: Quedarte con el modelo de la época en que la validación fue mínima y, si el hueco sigue siendo grande, añadir regularización o más datos
o: Reducir la tasa de aprendizaje a la mitad para que las curvas se acerquen
a: 2
e: La curva de validación ya marcó su mínimo: lo que se aprende después es ruido del conjunto de entrenamiento. Bajar la tasa solo retrasa el problema, y seguir entrenando empeora la generalización aunque el entrenamiento mejore.
:::

:::quiz
p: ¿Por qué el hueco de generalización (validación menos entrenamiento) puede ser negativo sin que haya nada raro?
o: Porque el optimizador no converge en el conjunto de entrenamiento
o: Porque el conjunto de validación puede ser algo más fácil o tener menos ruido por azar
o: Porque la validación se calcula con el dropout activo
a: 2
e: El hueco compara dos muestras finitas y distintas: si la de validación tiene menos ruido efectivo o ejemplos más fáciles, sale mejor. El indicador fiable es la tendencia de la curva de validación, no el signo del hueco en un momento dado.
:::

:::quiz
p: Tienes un hueco grande y solo puedes hacer un cambio. ¿Cuál ataca la causa del sobreajuste?
o: Duplicar las épocas con un planificador de tasa de aprendizaje
o: Conseguir más datos etiquetados o aumentar los que ya tienes
o: Subir la tasa de aprendizaje para que el modelo explore más
a: 2
e: El sobreajuste es falta de información por parámetro: más datos es lo único que reduce el hueco sin sacrificar ajuste. Más épocas y una tasa mayor suelen empeorar la generalización, y la regularización solo alivia el síntoma a cambio de ajuste.
:::

:::trampa
Guardar el modelo al final del bucle de entrenamiento es el error más caro y más frecuente.
El modelo bueno es el de la época con mejor validación, no el último. Guarda una copia cada
vez que la validación mejore y quédate con esa.
:::
