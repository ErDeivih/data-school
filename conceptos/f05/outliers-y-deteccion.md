---
id: outliers-y-deteccion
titulo: Valores atípicos
fase: 5
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [z-score-y-estandarizacion, cuantiles-y-percentiles, medidas-de-dispersion]
tags: [outliers, deteccion, calidad, robustez]
resumen: Detectar un valor que se aleja del resto es fácil; decidir si es un error de medición, un dato mal tecleado o el fenómeno que buscas es el trabajo que de verdad importa.
fuentes: ["Tukey (1977), 'Exploratory Data Analysis'"]
---

## En una frase

Un valor atípico es una observación que no encaja con el patrón del resto, y detectarlo es la
parte fácil: lo difícil es decidir si es un error que hay que corregir o el caso extremo real
que da valor al análisis.

## La idea

Imagina una mancha en una radiografía. Puede ser suciedad en el escáner o un tumor. La
estadística te dice que la mancha está ahí; solo el radiólogo sabe qué es. Con los datos pasa lo
mismo: un importe de 1 200 000 euros en una tabla de compras puede ser un pedido corporativo
perfectamente real o un error de tecleo donde alguien añadió tres ceros. La decisión **no se
toma con una fórmula, se toma preguntando cómo se generó ese dato**.

Esa es la razón de que la detección de atípicos tenga dos fases y casi todo el mundo se salte la
segunda:

1. **Detectar**: aplicar una regla y obtener una lista de candidatos.
2. **Interpretar**: para cada candidato, buscar el mecanismo. ¿Un sensor saturado? ¿Una unidad
   equivocada (céntimos en una columna de euros)? ¿Un cliente distinto? ¿Un día con una campaña?

Y hay un detalle técnico que cambia todo: **los métodos clásicos se enmascaran entre sí**. La
media y la desviación típica se calculan con todos los datos, incluidos los extremos, así que un
valor enorme infla la desviación y acaba pareciendo «normal» a ojos del propio z-score. Con 12
observaciones y un único valor extremo, el z-score máximo posible es (n − 1) / √n ≈ 3,18 por
mucho que el valor crezca. Los métodos basados en la mediana no tienen ese problema, porque la
mediana no se mueve cuando mueves el extremo.

:::figura
fichero: outliers-enmascaramiento-z-frente-a-mad
pie: El eje horizontal es el valor del extremo, en escala logarítmica, y los mismos once valores normales. A la izquierda, el z-score clásico pasa de 3,08 a 3,18 cuando el extremo crece de 45 a 1.000: es prácticamente plano y se queda por debajo del umbral, mientras el z modificado sube de 11 a 333. A la derecha se ve la causa: la desviación típica del denominador crece con el extremo al mismo ritmo que el numerador. La conclusión práctica es que el umbral 3,5 con media y desviación **no** detecta un valor mil veces mayor; hay que usar mediana y MAD.
fuente: figuras/outliers-y-deteccion-1.py
:::

:::nota
Ojo con la palabra «atípico» en datos con dos poblaciones. Si mezclas clientes particulares y
empresas en la misma columna de facturación, el grupo de empresas enteras será «atípico» para
cualquier regla. No son errores: es que hay dos grupos, y lo que toca es separarlos con una
variable, no borrarlos.
:::

## Definición formal

Cuatro reglas, de la más simple a la más general:

**Vallas de Tukey (IQR).** Con `Q1` y `Q3` el primer y tercer cuartil:

:::formula
IQR = Q3 − Q1          vallas: [ Q1 − 1,5 · IQR , Q3 + 1,5 · IQR ]
:::

- `Q1` — valor que deja el 25 % de los datos por debajo; `Q3`, el 75 %.
- `IQR` — rango intercuartílico, la anchura del 50 % central.
- El factor 1,5 es una convención de Tukey: en una distribución normal, deja fuera
  aproximadamente el **0,7 %** de las observaciones. En datos sesgados deja fuera más, y a
  menudo de forma legítima.

**Z-score.** Con `x̄` la media muestral y `s` la desviación típica muestral:

:::formula
z = (x − x̄) / s          se marca si |z| > 3
:::

**Z-score modificado (robusto).** Con `MAD` la desviación absoluta mediana:

:::formula
MAD = mediana( |x − mediana(x)| )          M = 0,6745 · (x − mediana) / MAD          se marca si |M| > 3,5
:::

- `MAD` — mediana de las distancias a la mediana. Es la versión robusta de la desviación típica.
- `0,6745` — constante que hace que, en una distribución normal, `MAD / 0,6745` estime la
  desviación típica. Sin ella, el umbral 3,5 no sería comparable con el 3 del z-score.
- El umbral habitual es **3,5**, no 3, precisamente porque el estimador es más conservador.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `Q1`, `Q3` | Primer y tercer cuartil | las de `x` | Mueven la valla: `Q3` más alto la aleja por arriba y `Q1` más bajo la aleja por abajo |
| `IQR` | Rango intercuartílico, la anchura del 50 % central | las de `x` | Ensancha las dos vallas a la vez; si los datos son muy dispersos, más casos quedan dentro |
| `1,5` | Constante de Tukey que multiplica al IQR | adimensional | Súbelo a 3 y en una normal no marcas prácticamente nada (queda fuera un 0,0002 %); bájalo a 1 y marcas de más. Con 1,5 se deja fuera ≈ 0,7 % de una normal |
| `x` | El valor que se está probando | las de la variable | Es la incógnita: lo que se pregunta es si es raro, no cuánto vale |
| `x̄` | Media muestral | las de `x` | Se calcula con el extremo dentro, así que un valor enorme la arrastra hacia él y lo disfraza |
| `s` | Desviación típica muestral (`ddof=1`) | las de `x` | Es el denominador del z-score y crece con el propio extremo: por eso el z-score se queda clavado cerca de 3,18 con `n = 12` |
| `z` | Puntuación del z-score | desviaciones típicas | Con umbral 3 marca pocos casos, pero en datos sesgados o con `n` pequeño esconde los extremos; úsalo solo si la distribución es aproximadamente simétrica |
| `MAD` | Mediana de las distancias a la mediana | las de `x` | Es la versión robusta de `s`: no la mueve el extremo. Si sale 0 (más de la mitad de los datos repetidos) el cociente se va a infinito y hay que cambiar de método |
| `0,6745` | Constante que hace que `MAD / 0,6745` estime la desviación típica en una normal | adimensional | Sin ella el umbral 3,5 no sería comparable con el 3 del z-score; no es un parámetro que se elija, se deja como está |
| `M` | z-score modificado | «desviaciones» robustas | Es el que crece de verdad con el extremo (de 11 a 333 en el ejemplo); el umbral habitual es 3,5 |
| `contamination` | Proporción de anomalías que Isolation Forest **debe** marcar | tanto por uno, 0 a 1 | No es un hallazgo: fija el número de marcas. Con 0,10 sobre datos limpios devuelve un 10 % de falsos positivos, así que empieza bajo y valida a mano |
:::

**Distancia de Mahalanobis.** Para varias variables a la vez, mide lo lejos que está un punto del
centro **teniendo en cuenta la correlación** entre variables y sus escalas. Un punto puede estar
dentro del rango de cada variable por separado y ser imposible en la combinación.

**Isolation Forest.** Método sin supuestos de distribución: construye árboles con cortes
aleatorios y mide cuántos cortes hacen falta para aislar un punto. Los extremos se aíslan con
pocos cortes. Devuelve una puntuación; cuanto más negativa, más raro es el punto. Su parámetro
`contamination` es **la proporción que esperas encontrar**, no un hallazgo.

## Ejemplo

Doce medidas, con un valor claramente separado:

```
8  9  10  10  11  12  12  13  14  15  16  45
```

Con las vallas de Tukey: `Q1 = 10`, `Q3 = 14,25`, `IQR = 4,25`. La valla superior queda en
`14,25 + 1,5 · 4,25 = 20,625`, así que **45 se marca** y ningún otro valor se acerca.

Con el z-score: media 14,583 y desviación 9,876, así que `z = (45 − 14,583) / 9,876 = 3,08`.
Se marca, pero por los pelos, y ese «por los pelos» es la pista de que algo va mal: la
desviación típica está inflada por el propio 45.

Con el z-score modificado: mediana 12 y `MAD = 2`, así que `M = 0,6745 · 33 / 2 = 11,13`. El
16, que es el mayor valor normal, da `M = 1,35` y no se marca. La separación entre 11,13 y 1,35
es enorme, y ahí está la diferencia: el método robusto no se deja arrastrar.

El enmascaramiento se ve mejor cambiando el extremo. Si en vez de 45 pones 200 o 1 000:

| Extremo | Media | Desviación | z | z modificado |
| --- | --- | --- | --- | --- |
| 45 | 14,58 | 9,88 | 3,08 | 11,13 |
| 200 | 27,50 | 54,38 | 3,17 | 63,40 |
| 1 000 | 94,17 | 285,27 | 3,18 | 333,20 |

El z-score **no sube**: pasa de 3,08 a 3,18, porque multiplicar el extremo por 20 multiplica
también la desviación típica. El z-score modificado pasa de 11 a 333. Si tu detector de atípicos
usara solo el z-score con umbral 3,5, un valor 1 000 veces mayor que el resto pasaría
desapercibido.

## Código

```python verificable
import numpy as np

valores = np.array([8, 9, 10, 10, 11, 12, 12, 13, 14, 15, 16, 45], dtype=float)
q1, q3 = np.percentile(valores, [25, 75])
iqr = q3 - q1
mediana = np.median(valores)
mad = np.median(np.abs(valores - mediana))

print(f"Q1 {q1}  Q3 {q3}  IQR {iqr}")                        # -> Q1 10.0  Q3 14.25  IQR 4.25
print(f"valla superior {q3 + 1.5 * iqr}")                   # -> valla superior 20.625
print(f"MAD {mad}")                                         # -> MAD 2.0
print(f"z de 45 {(45 - valores.mean()) / valores.std(ddof=1):.3f}")          # -> z de 45 3.080
print(f"z modificado de 45 {0.6745 * (45 - mediana) / mad:.3f}")             # -> z modificado de 45 11.129
print(f"z modificado de 16 {0.6745 * (16 - mediana) / mad:.3f}")             # -> z modificado de 16 1.349
```

:::claves
- `np.percentile(valores, [25, 75])` con una **lista** de niveles devuelve un array de dos elementos, y por eso se puede desempaquetar en `q1, q3 = ...`. Si le pasas un solo número (`np.percentile(v, 25)`) devuelve un escalar de NumPy y el desempaquetado falla con «cannot unpack non-iterable numpy.float64 object». Es la misma función con dos formas de llamada distintas.
- `np.percentile` interpola por defecto (`method="linear"`), así que no tiene por qué devolver un valor que exista en los datos: con los doce valores del ejemplo, `Q3 = 14,25` no está en la lista. Esa interpolación es la razón de que el IQR salga 4,25 y la valla 20,625 exactos. Con `method="lower"` o `"higher"` los cuartiles serían valores observados y la valla cambiaría.
- `np.median(x)` y `np.percentile(x, 50)` dan lo mismo, pero no son la misma función: `np.median` promedia los dos valores centrales cuando `n` es par. Los dos coinciden aquí porque `n = 12`.
- `valores.std(ddof=1)` usa la desviación **muestral** (divide entre `n − 1`), que es lo que hace la fórmula de la página. El valor por defecto de NumPy es `ddof=0`: si quitas ese argumento, el z de 45 pasa de 3,080 a 3,217 (con 12 valores la diferencia ya se ve en la segunda cifra). Con pocas filas, dos herramientas que usen `ddof` distinto dan z-scores distintos sobre los mismos datos.
- Los valores se declaran con `dtype=float` por claridad, no porque la resta lo necesite: `np.median` devuelve un `float`, así que `valores - mediana` promociona a `float64` aunque `valores` sea entero y aquí no hay ningún truncamiento que evitar. Compruébalo quitando `dtype=float`: `(valores - mediana).dtype` sigue siendo `float64` y el MAD sale igual.
- `mediana` y `mad` se calculan **una vez** y se reutilizan en las tres líneas siguientes. Fíjate en que no dependen de 45: por eso el z modificado cambia al mover el extremo y el z clásico no. Si recalcularas la media con el extremo dentro para el denominador robusto, el enmascaramiento volvería. Compruébalo sustituyendo `mad` por `valores.std(ddof=1)` en la última línea: el número pasa de 11,129 a 3,080 y deja de distinguir el extremo.
:::

```python verificable
import numpy as np

# Enmascaramiento: al crecer el extremo, la desviacion tipica crece con el y el
# z-score se queda clavado, mientras el z modificado (robusto) se dispara.
for extremo in (45.0, 200.0, 1000.0):
    v = np.array([8, 9, 10, 10, 11, 12, 12, 13, 14, 15, 16, extremo])
    mediana = np.median(v)
    mad = np.median(np.abs(v - mediana))
    z = (extremo - v.mean()) / v.std(ddof=1)
    z_mod = 0.6745 * (extremo - mediana) / mad
    print(f"extremo {extremo:>6.0f}  sd {v.std(ddof=1):>7.2f}  z {z:.2f}  z_mod {z_mod:>7.2f}")
```

```text
extremo     45  sd    9.88  z 3.08  z_mod   11.13
extremo    200  sd   54.38  z 3.17  z_mod   63.40
extremo   1000  sd  285.27  z 3.18  z_mod  333.20
```

```python verificable
import numpy as np
from sklearn.ensemble import IsolationForest

# Isolation Forest: no supone ninguna distribucion, aisla con cortes aleatorios.
rng = np.random.default_rng(3)
datos = np.vstack([rng.normal(0.0, 1.0, size=(200, 2)), [[6.0, 6.0], [-7.0, 5.0]]])

bosque = IsolationForest(n_estimators=100, random_state=0).fit(datos)
puntuacion = bosque.score_samples(datos)          # mas negativo = mas raro

print("los 4 mas raros:", np.argsort(puntuacion)[:4].tolist())        # -> [200, 201, 0, 168]
print("puntuacion mediana:", round(float(np.median(puntuacion)), 3))  # -> -0.398
print("marca con contamination=0.02:", int((bosque.set_params(contamination=0.02).fit_predict(datos) == -1).sum()))  # -> 5
print("marca con contamination=0.10:", int((bosque.set_params(contamination=0.10).fit_predict(datos) == -1).sum()))  # -> 21
```

## Errores típicos

- **Borrar los atípicos sin investigar el mecanismo.** Es el error más caro. Si el extremo era
  un pedido real o un fraude real, acabas de eliminar el fenómeno que querías estudiar. Antes de
  tocar nada, responde: ¿cómo se generó este valor?
- **Usar el z-score con datos sesgados.** La media y la desviación ya están contaminadas por el
  propio extremo: con 12 valores, el z-score se queda en 3,18 aunque el extremo sea mil veces
  mayor. Usa el z-score modificado o las vallas de Tukey.
- **Aplicar la regla del IQR a una distribución bimodal o con cola larga.** En una lognormal,
  el 10 % de los datos puede quedar fuera de las vallas sin que haya un solo error. En ese caso
  la pregunta correcta no es «qué borro» sino «qué transformación (logaritmo) o qué modelo
  describe esto».
- **Creer que `contamination` es un hallazgo.** Isolation Forest marca exactamente la proporción
  que le pides. Si pones 0,10, te devuelve un 10 % de «anomalías» aunque los datos sean ruido
  perfectamente normal. Empieza con un valor bajo, mira las puntuaciones y valida a mano los
  primeros casos.
- **Imputar el atípico con la media.** Inventa un dato que no existe y, si el valor era real,
  destruye la señal. Si decides recortarlo, usa *winsorizar* (llevarlo al percentil 1 o 99) y
  dilo explícitamente en el informe.
- **Confundir el error de medición con el valor extremo real.** Una edad de 250 años es un
  error, siempre. Un cliente que gasta cien veces más que la media es, casi siempre, un dato
  correcto y la parte más interesante del análisis.

:::practica
enunciado: Nueve medidas: 10, 11, 12, 12, 13, 14, 15, 16, 95. Calcula la valla superior de Tukey y el z-score modificado de 95 y de 16, y decide qué hacer con el valor extremo.
pista: La valla usa Q1, Q3 y 1,5 · IQR; el z modificado usa mediana y MAD, que no se mueven al cambiar el extremo.
solucion: Q1 = 12, Q3 = 15, IQR = 3, valla = 15 + 1,5 · 3 = 19,5, así que 95 queda fuera. Mediana 13 y MAD 2: M(95) = 0,6745 · (95 − 13) / 2 = 27,65, frente a M(16) = 0,6745 · 3 / 2 = 1,01. Los dos métodos lo separan sin ambigüedad, pero eso solo dice que es raro: antes de borrarlo hay que averiguar cómo se generó.
:::

## Comprueba que lo sabes

:::quiz
p: Con los 12 valores del ejemplo, el z-score del valor 45 es 3,08 y el z-score modificado es 11,13. ¿Por qué se parecen tan poco?
o: Porque el z-score modificado usa una fórmula distinta y más precisa
o: Porque el z-score divide por una desviación típica que el propio 45 ha inflado, y el modificado divide por el MAD, que no se mueve
o: Porque el z-score está mal calculado
a: 2
e: La media y la desviación típica se calculan con todos los valores, incluido el extremo, así que el extremo se enmascara a sí mismo. La mediana y el MAD solo dependen del orden y del centro, así que no cambian de forma apreciable al mover el extremo: por eso el z modificado crece con él.
:::

:::quiz
p: Ejecutas Isolation Forest con `contamination=0.10` sobre datos limpios y te devuelve un 10 % de anomalías. ¿Qué concluyes?
o: Que un 10 % de los datos son errores
o: Que el parámetro fija la proporción esperada y hay que validar los casos a mano antes de creerlos
o: Que hay que repetir con `contamination=0.5` para afinar
a: 2
e: `contamination` no es una detección, es una expectativa que le das al modelo: el umbral se coloca para marcar esa fracción. Con datos limpios, el resultado es un 10 % de falsos positivos. Se empieza con una proporción baja y se revisan los casos marcados con conocimiento del negocio.
:::

:::trampa
Estandarizar (restar la media y dividir por la desviación) **antes** de buscar atípicos no los
hace más fáciles de ver: es exactamente el mismo cálculo que el z-score, con el mismo problema de
enmascaramiento. La estandarización sirve para comparar escalas, no para detectar extremos.
:::
