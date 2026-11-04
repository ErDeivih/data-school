---
id: deteccion-de-anomalias
titulo: Detección de anomalías
fase: 6
nivel: avanzado
rutas: [ds, de]
prerequisitos: [outliers-y-deteccion, distribuciones-en-datos-reales, precision-recall-y-pr]
tags: [anomalias, no-supervisado, isolation-forest, calidad]
resumen: Encontrar lo raro cuando nadie te ha dicho qué es raro: puntuaciones de rareza, umbrales que son una decisión de negocio y validación con muy pocos positivos.
fuentes: ["Liu, Ting y Zhou (2008), 'Isolation Forest'", "Breunig, Kriegel, Ng y Sander (2000), 'LOF: Identifying Density-Based Local Outliers'"]
---

## En una frase

La detección de anomalías ordena las observaciones de más rara a más normal con un modelo
ajustado sin etiquetas, y deja en tus manos la única decisión que importa: a partir de qué
puntuación se actúa.

## La idea

Un sensor de una fábrica mide temperatura, presión y caudal cada minuto. Un día la presión sube
un 3 % por encima de lo habitual durante veinte minutos. ¿Es una anomalía o es una tarde
calurosa? No hay ninguna etiqueta que diga «esto fue un fallo». Y ahí está la dificultad real
del problema: no es tanto calcular una puntuación de rareza, que es la parte fácil, como
**definir qué es raro**, que es una decisión sobre el negocio.

Los métodos se reparten en dos familias:

1. **Modelar lo normal y medir la desviación.** Se aprende la forma de la mayoría de los datos
   (una gaussiana, una densidad, un subespacio, un autoencoder) y se puntúa cada punto por lo
   mal que encaja. La distancia de Mahalanobis y los autoencoders están aquí.
2. **Aislar en vez de modelar.** Un Isolation Forest construye árboles con cortes aleatorios: un
   punto raro se queda solo con muy pocos cortes porque está en una zona vacía, mientras que un
   punto normal necesita muchos cortes para separarse de sus vecinos. No hace falta saber cómo
   es «lo normal»: basta con que lo raro esté apartado.

La primera familia sufre cuando la normalidad tiene varias formas (dos turnos de producción, por
ejemplo): una sola gaussiana tapa un turno con el otro. La segunda es más robusta a eso, pero
pierde sensibilidad cuando la anomalía está *dentro* de la nube, como un valor extremo en una
sola dirección. La tercera vía, la más útil en la práctica, es **supervisar un poco**: si tienes
200 casos revisados, entrena un clasificador normal y desbalanceado en lugar de fingir que no
sabes nada.

Hay una asimetría que nunca se puede olvidar: cuando una anomalía es un fraude o un fallo, el
coste de dejarla pasar suele ser enorme comparado con el de revisar una falsa alarma. Eso no se
resuelve con un algoritmo, se resuelve eligiendo el umbral con los dos costes sobre la mesa.

## Definición formal

**Distancia de Mahalanobis.** Con `μ` el vector de medias y `Σ` la matriz de covarianzas de los
datos:

:::formula
d²(x) = (x − μ)ᵗ · Σ⁻¹ · (x − μ)
:::

- `x` — el punto a puntuar, de dimensión `p`.
- `Σ⁻¹` — la inversa de la matriz de covarianzas; corrige la escala y la correlación entre
  variables. Con `Σ = I` la fórmula se reduce a la distancia euclídea al cuadrado.
- Si los datos son normales multivariantes, `d²` sigue una distribución chi-cuadrado con `p`
  grados de libertad, así que el umbral sale de un cuantil: por ejemplo, el percentil 99,9 de
  `χ²_p`. Eso convierte «raro» en una probabilidad, no en una corazonada.

**Z-score modificado (robusto).** Como la media y la desviación se contaminan con el propio
outlier, se usan la mediana y la desviación absoluta mediana:

:::formula
MAD = mediana( |x_i − mediana(x)| )        z_mod = 0,6745 · (x_i − mediana) / MAD
:::

- `MAD` — desviación absoluta mediana: la mediana de las distancias a la mediana.
- `0,6745` — el cuantil 0,75 de la normal estándar; sirve para que, en datos normales, `z_mod`
  sea comparable al z-score clásico.
- Regla habitual: por encima de `3,5` se revisa el punto.

**Isolation Forest.** Para cada punto se mide la longitud del camino `h(x)` hasta aislarlo,
promediada sobre `t` árboles aleatorios:

:::formula
s(x, n) = 2^( −E[h(x)] / c(n) )        c(n) = 2·H(n − 1) − 2·(n − 1)/n
:::

- `E[h(x)]` — longitud media del camino, en número de cortes, hasta quedarse solo.
- `n` — número de observaciones; `H(i) ≈ ln(i) + 0,5772` es el número armónico.
- `c(n)` — longitud media esperada en un árbol aleatorio; sirve para normalizar.
- `s` cercano a 1 indica anomalía, alrededor de 0,5 es normal y por debajo de 0,5 son puntos
  especialmente fáciles de aislar (el centro de una nube densa).

**LOF (Local Outlier Factor).** Compara la densidad local de un punto con la de sus `k` vecinos:

:::formula
LOF_k(x) = (1/k) · Σ_{o ∈ vecinos} lrd_k(o) / lrd_k(x)
:::

- `lrd_k` — densidad de alcanzabilidad local: la inversa de la distancia media a los `k` vecinos,
  contando la distancia de cada vecino a `x` si es mayor que su propia distancia al `k`-ésimo.
- `LOF ≈ 1` significa «igual de denso que mi entorno»; `LOF > 1`, más aislado que él. Es la
  herramienta cuando la densidad del conjunto varía por zonas: un punto en una zona rala no es
  anómalo si todos sus vecinos también están ralos.

**Evaluación.** Sin etiquetas no hay métrica, así que se etiqueta una muestra y se mide
`precision@k` (de los `k` puntos con mayor puntuación, cuántos son anomalías confirmadas) o el
área bajo la curva precisión-exhaustividad. La exactitud no se usa nunca: con un 0,5 % de
anomalías, decir «todo es normal» da un 99,5 % de acierto y no detecta nada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Σ` (covarianzas) | Matriz que corrige la escala y la correlación entre variables en Mahalanobis | unidades² | Con covarianzas grandes, `Σ⁻¹` encoge y `d²` baja: el mismo punto se considera menos raro |
| `MAD` | Desviación absoluta mediana: la mediana de las distancias a la mediana | las de la variable | El denominador del z modificado crece, así que la puntuación de todos los puntos **baja** y se marcan menos |
| `z_mod` | Puntuación robusta: `0,6745 · (x − mediana) / MAD` | desviaciones (adimensional) | Es la puntuación que ordena la lista; por encima de 3,5 se revisa el punto. Cuanto más alto, más raro |
| `E[h(x)]` | Longitud media del camino hasta aislar el punto, promediada sobre los árboles | cortes | Es el numerador del exponente con signo menos: al subir, `s(x, n)` **baja** y el punto parece normal |
| `n` | Número de observaciones con las que se ajusta el modelo | observaciones | `c(n)` crece como `ln(n)`, así que el mismo camino vale relativamente menos y el umbral se vuelve más exigente |
| `c(n)` | Longitud media esperada del camino en un árbol aleatorio: normaliza `E[h(x)]` | cortes | Al subir, divide más y `s` baja: es lo que hace comparables conjuntos de tamaños distintos |
| `s(x, n)` | Puntuación de aislamiento de Isolation Forest | adimensional (0 a 1) | Cerca de 1 es anomalía, alrededor de 0,5 es normal y por debajo de 0,5 son puntos del centro de una nube densa |
| `k` (en LOF) | Número de vecinos con los que se compara la densidad local | vecinos | Vecindarios más amplios: menos sensible a rarezas muy locales, y una anomalía dentro de una zona densa se diluye |
| `LOF_k` | Cociente entre la densidad de los vecinos y la del punto | adimensional | Alrededor de 1 es «igual de denso que mi entorno»; por encima, más aislado. Sirve cuando la densidad varía por zonas |
| `contamination` | Proporción de puntos que esperas marcar como anómalos | fracción (0-1) | El umbral se relaja y entran más puntos normales: sube el recall y baja la precisión. No se estima, se decide |
| `k` (en precision@k) | Cuántas alertas estás dispuesto a revisar | alertas | Al subir, la precisión baja (el ranking se va agotando) y el recall sube: es el presupuesto de revisión, no una métrica neutra |
:::

## Ejemplo

Nueve medidas de consumo diario: `10, 11, 12, 12, 13, 13, 14, 15, 100`. El último valor es el
que nos huele mal, y estos son los números:

- **Vía clásica.** Media `= 22,22` y desviación típica `= 29,21`. El z-score del 100 es
  `(100 − 22,22) / 29,21 = 2,66`. Con el umbral habitual de 3, **no lo marcarías**.
- **Por qué.** El propio valor extremo infla la media (de 12,5 a 22,22) y la desviación (de 1,60 a
  29,21), mientras que la mediana no se mueve y sigue en 13. Ese fenómeno se llama
  **enmascaramiento**: el outlier se esconde dentro de la estadística que debería delatarlo.
- **Vía robusta.** Mediana `= 13` y `MAD = 1`. El z-score modificado del 100 es
  `0,6745 · (100 − 13) / 1 = 58,68`, y el del valor 15 es `1,35`. Ahora el 100 está a años luz y
  el 15, que es el máximo legítimo, no se toca.

Ese contraste es la lección de la página: para detectar extremos, las estadísticas que usas para
medirlos no pueden depender de ellos.

:::figura
fichero: anomalias-anillo-y-z-robusto
pie: El panel izquierdo enseña por qué el problema se plantea sin etiquetas y por qué el umbral es una decisión: 300 puntos normales y 15 en un anillo lejano se separan a ojo, y esos 15 (el 4,8 %) son los que el negocio puede revisar. En dos dimensiones basta mirar; con cuarenta variables, esa misma separación hay que ordenarla con una puntuación, y ahí empieza el problema de verdad. El panel derecho es el que cambia la práctica. Al crecer el valor extremo, el z-score clásico se queda pegado a su techo —con nueve datos, 2,67, que sale de (n − 1)/√n— y no llega nunca al umbral de 3, mientras que el z modificado cruza el umbral de 3,5 ya con un valor de 18,2. La causa no es una casualidad de esos nueve números: la media y la desviación se calculan con el outlier dentro y él mismo las infla. Es el enmascaramiento del ejemplo visto como lo que es, una propiedad de la fórmula. La consecuencia para el trabajo diario es que un z-score por encima de 3 no demuestra que no haya anomalías: con pocos datos, puede ser imposible de alcanzar.
fuente: figuras/deteccion-de-anomalias-1.py
:::

## Código

```python verificable
import numpy as np

consumo = np.array([10.0, 11, 12, 12, 13, 13, 14, 15, 100])   # el ultimo es el raro

# Version clasica: media y desviacion. El propio outlier las infla y se esconde.
z = (consumo - consumo.mean()) / consumo.std(ddof=1)   # ddof=1: divide entre n-1
print("media:", round(consumo.mean(), 2), "desviacion:", round(consumo.std(ddof=1), 2))
# -> media: 22.22 desviacion: 29.21
print("z-score del 100:", round(z[-1], 2))        # -> 2.66

# Version robusta: mediana y desviacion absoluta mediana (MAD).
mediana = np.median(consumo)
mad = np.median(np.abs(consumo - mediana))        # MAD: distancias a la mediana, y su mediana
z_mod = 0.6745 * (consumo - mediana) / mad        # 0,6745 deja las dos escalas comparables
print("mediana:", mediana, "MAD:", mad)           # -> mediana: 13.0 MAD: 1.0
print("z modificado del 100:", round(z_mod[-1], 2))   # -> 58.68
print("z modificado del 15:", round(z_mod[-2], 2))    # -> 1.35
```

:::claves
- `consumo.std(ddof=1)` divide entre `n − 1`, la desviación **muestral**, la misma que estima la
  variabilidad de la población. El `ddof=0` que trae NumPy por defecto divide entre `n` y da un
  número algo menor; con nueve datos la diferencia se ve en la segunda cifra decimal, y con pocas
  observaciones puede cambiar si el punto pasa o no el umbral.
- `z = (consumo - consumo.mean()) / consumo.std(ddof=1)` es una operación **vectorizada**: el
  resultado tiene la misma forma que la entrada (nueve valores), no un número. `z[-1]` toma el del
  último elemento, que es el que interesa aquí; si te quedas con `z` entero e imprimes, verás los
  nueve z-scores.
- `np.median(np.abs(consumo - mediana))` calcula el MAD a mano porque NumPy no trae función
  propia. `scipy.stats.median_abs_deviation` existe, pero **no** aplica el factor 0,6745 salvo que
  le pidas `scale="normal"`: usarla por defecto y comparar con 3,5 mezcla dos escalas distintas.
- El MAD puede valer 0 (cuando más de la mitad de los datos son idénticos): entonces `z_mod` sale
  `inf` o `nan` y la puntuación deja de servir. No es un caso raro en datos discretos o con muchos
  ceros, y hay que decidir qué hacer antes de que reviente el informe.
- En el segundo bloque, `D.sort(axis=1)` ordena **cada fila** y devuelve `None`: ordena la matriz
  en el sitio, así que después hay que seguir usando `D` y no lo que devolvió la llamada. Un
  `puntuacion = D.sort(axis=1)` deja `puntuacion` a `None` y el error aparece dos líneas más abajo.
- `puntuacion = D[:, 5]` es la distancia al **quinto vecino**, no al sexto: la columna 0 de cada
  fila es la distancia del punto consigo mismo, que vale 0. Contar esa columna como un vecino más
  desplaza todo el cálculo y hace que la puntuación dependa de un cero.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(0)
normal = rng.normal(0, 1, size=(300, 2))
angulos = np.linspace(0, 2 * np.pi, 15, endpoint=False)
anomalos = 7 * np.column_stack([np.cos(angulos), np.sin(angulos)])   # 15 puntos en un anillo lejano
X = np.vstack([normal, anomalos])
es_anomalia = np.r_[np.zeros(300), np.ones(15)]

# Puntuacion sin modelo: la distancia al quinto vecino mas cercano. Cuanto mayor, mas raro.
D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)   # matriz 315x315 de distancias
D.sort(axis=1)                       # ordena cada fila en el sitio: devuelve None
puntuacion = D[:, 5]                 # la columna 0 es el propio punto; esta es el 5.o vecino
for k in (10, 20):
    elegidos = np.argsort(puntuacion)[::-1][:k]
    print(f"top{k}: {int(es_anomalia[elegidos].sum())} anomalias reales de {k}")
# -> top10: 10 anomalias reales de 10
# -> top20: 15 anomalias reales de 20
print("puntuacion media normal:", round(float(puntuacion[:300].mean()), 3),
      "anomala:", round(float(puntuacion[300:].mean()), 3))
# -> puntuacion media normal: 0.326 anomala: 4.68
```

Fíjate en el contraste: los 10 puntos más raros de la lista son los 10 correctos, pero al pedir
20 hay que rellenar con 5 normales, porque solo existen 15 anomalías. Eso es lo que mide
`precision@k` y lo que decides tú al fijar cuántas alertas vas a revisar. Las librerías traen
detectores con ese umbral ya incorporado:

```python ilustrativo
# La version de biblioteca. `contamination` es el porcentaje que esperas marcar: no se
# estima, se decide, y sale directamente del presupuesto de revision.
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

bosque = IsolationForest(contamination=0.05, random_state=0, n_estimators=100).fit(X)
marcados = bosque.predict(X) == -1              # 5 % de 315 puntos: unos 16
lof = LocalOutlierFactor(n_neighbors=20)
marcados_lof = lof.fit_predict(X) == -1         # el umbral por defecto de LOF

# Bajo la alfombra de la puntuacion, siempre hay una decision de negocio.
print(int(marcados.sum()), int(marcados_lof.sum()))
```

## Errores típicos

- **Estandarizar con media y desviación que incluyen los outliers.** Es el enmascaramiento del
  ejemplo: la desviación inflada hace que el punto extremo parezca normal. Usa mediana y MAD, o
  ajusta el escalador solo con datos limpios.
- **Presumir de exactitud.** Con un 0,5 % de anomalías, un modelo que no marca nada acierta el
  99,5 %. La métrica correcta es `precision@k`, el área bajo la curva precisión-exhaustividad o
  el coste total de los errores.
- **Elegir el umbral por defecto y evaluarlo con las mismas etiquetas.** La `contamination` no
  se estima, se decide: «solo puedo revisar 20 casos al día» o «un fallo no detectado cuesta
  50.000 euros». Ponla con el equipo, no con el valor que trae la función. Y el umbral se elige
  dentro de la validación y se reporta en un conjunto que no se ha tocado, o mejor, en el
  siguiente periodo de tiempo: hacerlo sobre las etiquetas que usaste para ajustarlo es
  [[fuga-de-datos]] en estado puro.
- **Confundir dato sucio con anomalía.** Un sensor con el cable pelado produce valores
  imposibles (presión negativa, edad de 300 años). Eso se filtra en la validación de calidad
  antes de puntuar nada: si los mezclas, el detector gastará su presupuesto en errores de
  captura.
- **Entrenar el autoencoder con las anomalías dentro.** Si el modelo aprende a reconstruir
  también lo raro, deja de considerarlo raro. Entrena con datos que creas limpios (o con una
  pérdida que ignore el error grande) y comprueba que el error de reconstrucción es mayor en los
  casos revisados.
- **Olvidar la deriva.** Lo normal de hace un año no es lo normal de hoy: cambian los turnos,
  los precios, los clientes. Compara cada punto contra una ventana reciente y revisa el modelo
  con la misma periodicidad con la que revisas el negocio. [[monitorizacion-de-drift]] cubre ese
  seguimiento.

:::practica
enunciado: Nueve lecturas de un sensor: 20, 21, 21, 22, 22, 23, 23, 24 y 90. Calcula la mediana, el MAD y el z-score modificado del 90 y del 24 con z_mod = 0,6745 · (x − mediana) / MAD, y di cuáles marcas con el umbral de 3,5.
pista: El MAD es la mediana de las distancias a la mediana, así que primero ordena esas distancias.
solucion: Ordenadas, la mediana es 22. Las distancias a 22 son 2, 1, 1, 0, 0, 1, 1, 2 y 68; ordenadas, su mediana es 1, así que MAD = 1. z_mod(90) = 0,6745 · 68 / 1 = 45,9, muy por encima de 3,5: se marca. z_mod(24) = 0,6745 · 2 / 1 = 1,35, por debajo: no se marca. Solo el 90 es anómalo y el 24 es el máximo legítimo.
:::

## Comprueba que lo sabes

:::quiz
p: En la serie 10, 11, 12, 12, 13, 13, 14, 15, 100, el z-score clásico del 100 es 2,66. ¿Por qué no llega a 3?
o: Porque el 100 no es una anomalía real
o: Porque la media y la desviación se calculan incluyendo ese mismo valor y quedan infladas
o: Porque el z-score solo funciona con distribuciones uniformes
a: 2
e: El valor extremo arrastra la media de 12,5 a 22,22 y la desviación de 1,60 a 29,21, así que el punto se mide contra una escala que él mismo ha agrandado. La mediana (13) y el MAD (1) no se dejan mover por un solo punto, así que el z modificado es 58,68.
:::

:::quiz
p: Tienes 20.000 transacciones y 30 fraudes confirmados. ¿Qué métrica NO debes usar para elegir el umbral?
o: La exactitud, porque marcar nada ya da un 99,85 %
o: La precisión de los 100 primeros de la lista ordenada
o: El coste total, sumando el precio de cada fraude no detectado y de cada revisión
a: 1
e: La exactitud es inservible con clases tan desbalanceadas: la clase mayoritaria domina. precisión@k responde a la pregunta que importa («de los que voy a revisar, cuántos son fraude») y el coste total traduce el problema a dinero, que es lo que decide de verdad el umbral.
:::

:::quiz
p: ¿Qué ventaja tiene Isolation Forest frente a un método que modela la densidad de lo normal?
o: Que no necesita suponer una forma concreta para lo normal, porque aísla con cortes aleatorios
o: Que siempre obtiene mejor precisión que cualquier otro método
o: Que no necesita elegir ningún parámetro
a: 1
e: El bosque de aislamiento puntúa por facilidad de aislamiento, no por probabilidad bajo un modelo de densidad, así que aguanta bien datos con varias formas de «normalidad». No es siempre mejor: busca aleatoriamente y pierde sensibilidad en anomalías dentro de la nube. Y parámetros tiene, empezando por el número de árboles y la contaminación esperada.
:::

:::trampa
Si tu detector marca como anomalías justo los valores más grandes de una variable, comprueba
antes si tienes un problema de mezcla: dos turnos, dos países o dos versiones de la aplicación
en los mismos datos producen dos nubes, y el método señala a la minoritaria como rara. Segmenta
primero y detecta dentro de cada segmento.
:::
