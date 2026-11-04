---
id: aprendizaje-activo
titulo: Aprendizaje activo
fase: 6
nivel: experto
rutas: [ds]
prerequisitos: [paradigmas-de-aprendizaje, metricas-de-clasificacion, calibracion, train-val-test]
tags: [etiquetado, incertidumbre, presupuesto, anotacion]
resumen: Elegir que filas etiquetar para aprender mas con menos anotaciones: incertidumbre, comite, diversidad y criterios de parada
fuentes: ["Settles (2012), 'Active Learning'", "Lewis y Gale (1994), 'A Sequential Algorithm for Training Text Classifiers'"]
---

## En una frase

El aprendizaje activo no espera a que le lleguen etiquetas: elige de una en una (o de pocas en
pocas) las filas que más le van a enseñar, se las manda a un anotador humano y repite, con el
objetivo de alcanzar la misma precisión con muchas menos anotaciones.

## La idea

Si etiquetar cuesta dinero, la pregunta interesante no es «¿cómo aprendo con estas
etiquetas?» sino «¿qué etiqueto con el presupuesto que tengo?». Y no todas las filas enseñan
lo mismo.

Imagina un clasificador que separa correos en «consulta» y «queja». La mayoría de los correos
son evidentes: cualquiera los etiquetaría igual y el modelo ya los acierta. Hay unos pocos,
sin embargo, que están justo en la frontera: hablan de un problema, piden algo y no está claro
qué pesa más. Etiquetar cien correos evidentes aporta cien confirmaciones de lo que el modelo
ya sabía. Etiquetar veinte correos de la frontera aporta veinte correcciones que mueven la
frontera.

Esa es la intuición del aprendizaje activo, y se concreta en cuatro formas de elegir la
siguiente fila:

1. **Incertidumbre.** Se pide la etiqueta del punto donde el modelo está menos seguro: la
   probabilidad más cercana a 0,5 en clasificación binaria, o la entropía más alta con varias
   clases.
2. **Comité.** Se entrenan varios modelos distintos (o el mismo con distintas semillas) y se
   pide la etiqueta del punto donde más discrepan.
3. **Cambio esperado del modelo.** Se estima cuánto cambiaría el modelo si conocieras esa
   etiqueta y se elige la que más lo cambiaría. Es caro de calcular y se usa poco.
4. **Diversidad.** Se pide un lote de puntos que sean distintos entre sí, no diez variantes del
   mismo caso raro. Sin diversidad, el lote se llena de duplicados cercanos y se desperdicia.

Hay un problema práctico que decide si esto funciona en la vida real: **la incertidumbre solo
es útil si el modelo está calibrado**. Un modelo sobreconfiado dirá 0,99 en puntos donde se
equivoca, y la estrategia de incertidumbre no los verá nunca. Y hay una trampa estadística al
final: si eliges qué etiquetar con el mismo conjunto con el que luego evalúas, la métrica
final deja de ser una estimación insesgada, porque has enriquecido artificialmente el conjunto
con los casos difíciles.

## Definición formal

Un problema de aprendizaje activo es una tupla `(L, U, A, Q, h)`, donde `L` son las filas ya
etiquetadas, `U` las candidatas sin etiquetar, `A` el anotador (el oráculo), `Q` la estrategia
de consulta y `h` el modelo. El bucle es:

:::formula
x* = argmax_{x ∈ U}  Q(x)     →     L ← L ∪ {(x*, A(x*))}     →     h ← entrenar(L)
:::

- `U` — el conjunto de candidatas sin etiquetar del que se puede elegir.
- `Q(x)` — la puntuación de informatividad de la fila `x`, según la estrategia elegida.
- `A(x*)` — la etiqueta verdadera que devuelve el anotador para la fila elegida.
- `L` — el conjunto etiquetado, que crece una consulta (o un lote) por iteración.
- `h` — el modelo reentrenado al final de cada iteración.

La estrategia de incertidumbre para clasificación binaria, con `p(x)` la probabilidad que el
modelo asigna a la clase positiva, es:

:::formula
Q_incertidumbre(x) = 1 − |2·p(x) − 1|     o bien     Q_entropía(x) = −Σ_c p_c(x)·log p_c(x)
:::

- `p(x)` — probabilidad de la clase positiva para la fila `x`; `|2·p(x) − 1|` vale 1 cuando el
  modelo está seguro y 0 cuando `p(x) = 0,5`.
- `p_c(x)` — probabilidad de la clase `c` en el caso multiclase; la suma recorre todas las
  clases.
- `Q` — cuanto mayor, más informativa es la fila.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Q(x)` | Puntuación de informatividad de la fila `x`, según la estrategia elegida | las de la estrategia (probabilidad, entropía o votos) | Cuanto mayor, más arriba queda la fila en la cola; cambiar `Q` cambia por completo qué se etiqueta |
| `p(x)` | Probabilidad que el modelo asigna a la clase positiva | de 0 a 1 | Cerca de 0,5 la fila es más informativa; cerca de 0 o de 1 el modelo ya la tiene clara y etiquetarla confirma lo que sabía |
| `x*` | La fila elegida para anotar en esta ronda | una fila de `U` | Es el máximo de `Q` sobre `U`; con la estrategia de incertidumbre es la `p(x)` más próxima a 0,5 |
| `U` | Las filas candidatas, todavía sin etiquetar | filas | Al encogerse con cada consulta, el criterio va quedándose sin puntos fáciles que descartar y las rondas se vuelven más caras |
| `L` | Las filas ya etiquetadas; crece una por consulta, o un lote entero | filas | Es el presupuesto gastado: su tamaño es el eje de la curva de rendimiento y de la decisión de parar |
| `A(x*)` | La etiqueta verdadera que devuelve el anotador para la fila elegida | las de `y` | Es el único dato nuevo que entra en el sistema; un anotador que se equivoca enseña el error, y con más fuerza si la fila es ambigua |
| `h` | El modelo reentrenado al final de cada ronda | no tiene unidades | Reentrenarlo es el coste dominante cuando el modelo es grande, y es lo que decide el tamaño del lote |
:::

Tres parámetros que hay que fijar antes de empezar y que casi nunca se fijan bien: el tamaño
del lote por ronda (1 es lo más eficiente y lo más caro en reentrenamientos), el presupuesto
total de etiquetas y el criterio de parada. El criterio de parada honesto es doble: o se acaba
el dinero, o la curva de rendimiento frente a número de etiquetas deja de subir. Sin esa curva
no hay forma de saber si el aprendizaje activo estaba sirviendo.

## Ejemplo

100 puntos en dos lunas entrelazadas, ruido 0,25, y un presupuesto de 12 etiquetas. Se empieza
con 4 filas etiquetadas al azar y se añade una por ronda; al final se mide la exactitud sobre
los 100 puntos, promediando 5 ejecuciones con semillas distintas:

```
estrategia aleatoria      : 0,776
estrategia de incertidumbre: 0,850
```

Mismo modelo, mismo número de etiquetas, misma métrica. La única diferencia es **cuáles** se
etiquetaron. Con 12 etiquetas de 100, elegir los puntos de la frontera vale 7,4 puntos de
exactitud más que elegirlos al azar. Ese es todo el negocio del aprendizaje activo: no mejorar
el modelo, sino mejorar la elección de los datos.

Y la letra pequeña: la comparación se ha hecho midiendo sobre los mismos 100 puntos. Si esos
100 puntos fueran el conjunto de evaluación final, el número estaría inflado, porque el bucle
activo eligió precisamente los casos difíciles de ese conjunto. En un proyecto real, la
evaluación se hace sobre un conjunto aparte que la estrategia nunca vio.

:::figura
fichero: aprendizaje-activo-incertidumbre-vs-azar
pie: A la izquierda, dónde caen las ocho primeras consultas de cada estrategia sobre los 100 puntos del problema. Los cuadrados naranjas son la estrategia aleatoria: se reparten por todas partes, incluidas zonas donde el modelo ya acierta. Los círculos verdes son la incertidumbre, y se concentran en la franja entre las dos lunas, que es exactamente donde la frontera está mal puesta. A la derecha, la curva que decide si esto sirve: con 12 etiquetas la diferencia es de 0,074 a favor de la incertidumbre, y esa ventaja se mantiene hasta el final del gráfico (unas 0,04 con 24 etiquetas). Con esa forma se ve el criterio de parada honesto: cuando la curva deja de subir, cada etiqueta nueva cuesta dinero y no aporta. La comparación es generosa con el método, porque se mide sobre los mismos 100 puntos de los que salen las consultas; en un proyecto real, un conjunto aparte daría una ventaja menor.
fuente: figuras/aprendizaje-activo-1.py
:::

## Código

```python verificable
import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = make_moons(n_samples=100, noise=0.25, random_state=0)

def precision_al_etiquetar(estrategia, semilla):
    rng = np.random.default_rng(semilla)
    idx = np.arange(len(y))
    rng.shuffle(idx)                        # el orden de llegada de los datos es aleatorio
    etiquetados = [int(i) for i in idx[:4]]
    sin_etiquetar = [int(i) for i in idx[4:]]
    modelo = LogisticRegression(max_iter=1000)

    while len(etiquetados) < 12:            # presupuesto: 12 etiquetas en total
        # Se reentrena con lo etiquetado hasta ahora: la incertidumbre se mide con este modelo
        modelo.fit(X[etiquetados], y[etiquetados])
        if estrategia == "aleatorio":
            # choice con size=1 devuelve un array de un elemento: de ahi el [0]
            elegido = int(rng.choice(sin_etiquetar, size=1, replace=False)[0])
        else:
            # Incertidumbre: la probabilidad mas cercana a 0,5 esta en la frontera
            # [:, 1] es la columna de la clase positiva; con [:, 0] se elegiria lo contrario
            p = modelo.predict_proba(X[sin_etiquetar])[:, 1]
            elegido = sin_etiquetar[int(np.argmin(np.abs(p - 0.5)))]
        etiquetados.append(elegido)
        sin_etiquetar.remove(elegido)       # remove borra por valor y recorre la lista entera

    modelo.fit(X[etiquetados], y[etiquetados])
    return accuracy_score(y, modelo.predict(X))

for est in ("aleatorio", "incertidumbre"):
    puntuaciones = [precision_al_etiquetar(est, s) for s in range(5)]
    print(f"{est:>14}: accuracy con 12 etiquetas = {np.mean(puntuaciones):.3f}")
# ->      aleatorio: accuracy con 12 etiquetas = 0.776
# -> incertidumbre: accuracy con 12 etiquetas = 0.850
```

:::claves
- `rng.choice(sin_etiquetar, size=1, replace=False)` devuelve un **array** de un elemento, no un número: de ahí el `[0]` del final. Y `sin_etiquetar.remove(elegido)` borra por **valor**, no por posición, recorriendo la lista entera: con 96 elementos da igual, pero con un banco de un millón de filas hay que llevar una máscara booleana en vez de tocar la lista.
- La rama aleatoria consume números del generador y la de incertidumbre no, así que las dos no son comparables semilla a semilla. Se comparan promediando varias, que es lo que hace el `range(5)`.
- `modelo.predict_proba(X[sin_etiquetar])[:, 1]` toma la columna de la clase positiva. Con `[:, 0]` el programa no falla, pero `np.argmin(np.abs(p - 0.5))` elige el punto **menos** incierto y la estrategia se vuelve lo contrario de lo que dice.
- `X[etiquetados]` con una lista de enteros devuelve una **copia** reordenada, no una vista: reordenar `etiquetados` no altera `X`. Lo mismo vale para `X[sin_etiquetar]`, que se recalcula entero en cada ronda.
- La exactitud final se mide con `accuracy_score(y, modelo.predict(X))` sobre los mismos 100 puntos de los que salen las consultas. Es lo más cómodo y lo más engañoso del bucle: la estrategia ha ido a buscar justo los casos difíciles de ese conjunto. Si esos 100 puntos fueran la evaluación final, el 0,850 estaría inflado.
- Cambia `while len(etiquetados) < 12` por `< 50` y la ventaja de la incertidumbre se estrecha: cuando hay etiquetas de sobra, elegir bien importa menos y la línea base aleatoria acaba alcanzándote.
:::

```python ilustrativo
# La estrategia de incertidumbre sin diversidad puede pedir diez veces el mismo caso raro.
# Ilustrativo: usa modAL y un estimador ya entrenado que no estan en el bloque.
from modAL.uncertainty import uncertainty_sampling
from modAL.batch import uncertainty_batch_sampling
from modAL.density import information_density

# Incertidumbre pura: el lote se llena de puntos casi duplicados
selector = uncertainty_batch_sampling    # es una funcion, no un objeto: se llama como la otra
# Combinada con densidad: penaliza los puntos aislados, que son raros y poco representativos
def puntuacion(estimador, X_pool):
    return uncertainty_sampling(estimador, X_pool) * information_density(X_pool)

for _ in range(20):                       # 20 rondas de anotacion humana real
    fila, _ = selector(estimador, X_pool)
    etiqueta = oraculo.etiquetar(fila)    # la persona tarda minutos: el bucle es lento
    estimador.teach(fila, etiqueta)       # teach reentrena el modelo con la fila nueva
```

## Errores típicos

- **Evaluar en el mismo conjunto del que la estrategia elige.** Al principio hay que etiquetar
  algo para tener un modelo, y es tentador usar todo el conjunto pequeño como banco de prueba.
  Si ese conjunto es el de evaluación, la métrica final está sesgada: la estrategia ha ido a
  buscar justo los casos difíciles. Reserva un conjunto externo desde el minuto uno.
- **Pedir la incertidumbre a un modelo mal calibrado.** Un bosque con pocos árboles o una red
  sin temperaturas ajustadas dan probabilidades que no significan lo que dicen. Si el modelo
  dice 0,5 donde se equivoca el 20 % de las veces, la estrategia de incertidumbre ordena mal
  las filas. Comprueba la calibración antes de confiar en ella.
- **Elegir de uno en uno con un modelo caro.** Reentrenar una red grande después de cada
  etiqueta es económicamente absurdo: el coste de cómputo supera el de la anotación. Usa lotes
  de 20 a 100 filas, o estrategias baratas (comité de modelos pequeños), o reentrena cada
  varias rondas.
- **Ignorar la diversidad del lote.** Incertidumbre pura pide diez variantes del mismo caso
  ambiguo. Con lotes, combina incertidumbre con representatividad (densidad, agrupamiento) para
  que el lote cubra zonas distintas del espacio.
- **No comparar contra la línea base aleatoria.** El aprendizaje activo no siempre gana: si el
  modelo ya está muy bien, si los datos tienen mucho ruido de etiqueta o si el presupuesto es
  grande, etiquetar al azar rinde igual. Sin haber medido la línea base, no sabes si tu
  estrategia aporta algo.
- **Olvidar el coste real de la anotación.** Etiquetar una imagen médica, un contrato y un
  tuit no cuestan lo mismo, ni tardan lo mismo. Una estrategia que pide 50 filas carísimas
  puede salir peor que otra que pide 200 filas baratas: el presupuesto debe medirse en coste,
  no en número de filas.

:::practica
enunciado: Con 12 etiquetas, elegir las filas al azar da 0,776 de exactitud y elegirlas por incertidumbre da 0,850. Calcula la diferencia y estima cuántas etiquetas aleatorias harían falta para llegar a 0,850, suponiendo que cada etiqueta aleatoria aporta lo mismo. Decide si compensa.
pista: La ganancia es la diferencia entre las dos exactitudes; para el cociente, supón que las 12 etiquetas aleatorias aportan ese 0,776 de forma proporcional.
solucion: Ganancia = 0,850 − 0,776 = 0,074 de exactitud con el mismo presupuesto de 12 etiquetas. Bajo el supuesto de rendimiento constante por etiqueta, las 12 bien elegidas equivalen a 12 · (0,850/0,776) ≈ 13,1 etiquetas al azar: un 8 % menos de anotaciones. Ojo, ese supuesto de rendimiento constante es solo la regla de tres del enunciado y no se sostiene con presupuestos grandes, porque la curva se aplana. Compensa, pero poco en este caso, y recuerda que el 0,850 está medido sobre los mismos 100 puntos de los que salieron las consultas, así que hay que confirmarlo en un conjunto externo.
:::

## Comprueba que lo sabes

:::quiz
p: Con 12 etiquetas, elegir las filas por incertidumbre da 0,850 y elegirlas al azar da 0,776. ¿Qué ha cambiado?
o: El modelo es mejor, porque la incertidumbre mejora el algoritmo de entrenamiento
o: Nada del modelo: solo qué filas se han etiquetado, escogiendo las que están cerca de la frontera
o: La métrica, que se ha medido de otra forma en cada caso
a: 2
e: El modelo, los datos y la métrica son idénticos; lo único que cambia es la selección de las 12 filas que reciben etiqueta. La incertidumbre prioriza los puntos donde el modelo duda, y cada etiqueta mueve más la frontera.
:::

:::quiz
p: ¿Por qué la incertidumbre puede fallar como criterio de selección?
o: Porque solo funciona con regresión y no con clasificación
o: Porque depende de que las probabilidades estén calibradas: un modelo sobreconfiado nunca marca como dudosos sus propios errores
o: Porque los puntos inciertos siempre son errores de etiquetado
a: 2
e: Si el modelo asigna 0,99 a puntos que falla, la estrategia nunca los elegirá. La incertidumbre mide lo que el modelo cree saber, no lo que realmente ignora. Un modelo sobreconfiado ordena mal las filas. No es un problema exclusivo de la clasificación ni los puntos inciertos son errores.
:::

:::trampa
El aprendizaje activo introduce un sesgo de selección en la evaluación: el conjunto que usas
para decidir qué etiquetar se enriquece con los casos difíciles, así que medir ahí exagera el
resultado. Separa siempre el banco de consulta del conjunto de evaluación, y compara la curva
de rendimiento frente a etiquetas contra la línea base aleatoria.
:::
