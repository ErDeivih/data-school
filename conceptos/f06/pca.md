---
id: pca
titulo: Análisis de componentes principales
fase: 6
nivel: intermedio
rutas: [ds, core]
prerequisitos: [escalado-y-transformacion, covarianza-y-correlacion, autovalores-y-autovectores]
tags: [dimensionalidad, algebra-lineal, visualizacion, preprocesado]
resumen: Sustituye variables correlacionadas por unas pocas direcciones que concentran la varianza, y deja claro qué información se tira al hacerlo.
fuentes: ["Jolliffe (2002), 'Principal Component Analysis'", "Hastie, Tibshirani y Friedman (2009), 'The Elements of Statistical Learning', cap. 14"]
---

## En una frase

El análisis de componentes principales (PCA) busca las direcciones del espacio donde los datos
están más abiertos y las usa como ejes nuevos: con dos variables muy correlacionadas, una sola
dirección recoge casi toda la información y la segunda se puede tirar.

## La idea

Pon una nube de puntos en el aire y proyecta su sombra sobre el suelo. Si la nube es alargada y
la lámpara está encima, la sombra es un borrón redondo y no se distingue nada. Si mueves la
lámpara hasta que la sombra sea lo más larga posible, la silueta revela la forma del objeto.
PCA hace exactamente eso, pero eligiendo la dirección en lugar de mover la lámpara: la primera
componente es la dirección en la que los datos se estiran más, la segunda es la dirección
perpendicular que más se estira de lo que queda, y así sucesivamente.

¿Para qué sirve? Tres problemas muy concretos:

1. **Demasiadas columnas correlacionadas.** Si tienes la altura en centímetros, en pulgadas y
   el perímetro de la muñeca, tres columnas cuentan casi lo mismo. Los modelos que miden
   distancias, como [[knn]] o [[k-means]], se dejan confundir por esa redundancia. PCA las
   funde en una sola dirección.
2. **Ruido.** Las últimas componentes recogen variaciones diminutas, muchas veces de medición.
   Quedarse con las primeras es una forma barata de suavizar.
3. **Ver.** Cuarenta columnas no se pueden dibujar. Dos componentes sí, y a menudo enseñan
   grupos y valores atípicos que ninguna tabla mostraba.

El precio está en la interpretación. Una componente es una mezcla con pesos de todas las
variables originales, así que «la componente 2 sube» no significa nada para el negocio hasta
que miras qué variables pesan en ella. Y si las variables tienen escalas distintas, la
componente 1 será simplemente la que venga medida en unidades más grandes.

## Definición formal

Sea `X` la matriz de datos de `n` filas (observaciones) y `p` columnas (variables), ya
**centrada** restando a cada columna su media.

:::formula
S = (1 / (n − 1)) · Xᵗ X
:::

- `Xᵗ` — la traspuesta de `X`, de tamaño `p × n`.
- `S` — la matriz de covarianzas, de tamaño `p × p`. El elemento de la diagonal `S_jj` es la
  varianza de la variable `j` y el de fuera de la diagonal `S_jk` es la covarianza entre `j` y `k`.

Las componentes son los autovectores de `S`, ordenados por su autovalor de mayor a menor:

:::formula
S · v_k = λ_k · v_k ,   λ₁ ≥ λ₂ ≥ … ≥ λ_p ≥ 0
:::

- `v_k` — el `k`-ésimo autovector (o *loading*): los pesos con los que se combinan las variables
  originales. Se normaliza a longitud 1, así que `v_kᵗ v_k = 1`.
- `λ_k` — el `k`-ésimo autovalor: la varianza de los datos a lo largo de la dirección `v_k`.
- `λ_k / Σ_j λ_j` — la **proporción de varianza explicada** por esa componente.
- `Z = X · V` — las puntuaciones (*scores*), donde `V` es la matriz con las `k` primeras
  columnas `v_1 … v_k`. `Z` tiene `n` filas y `k` columnas: esa es tu tabla reducida.
- Reconstrucción con `k` componentes: `X̂ = Z · Vᵗ`. La varianza que se pierde es exactamente
  `Σ` de los autovalores descartados.

Dos consecuencias que conviene tener presentes desde el principio: las componentes no están
correlacionadas entre sí (la matriz de covarianzas de `Z` es diagonal), y `Σ_k λ_k` es la
varianza total, o sea la suma de las varianzas de las `p` variables originales.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `X` | Matriz de datos: `n` filas (observaciones) y `p` columnas (variables) | las de cada variable | Con más columnas y las mismas filas, las direcciones se estiman peor: hacen falta más datos para el mismo número de variables |
| `n` | Número de observaciones (filas) | observaciones | Los autovectores se estabilizan y la proporción explicada de cada componente deja de bailar entre muestras |
| `p` | Número de variables (columnas) | variables | La varianza total es la suma de las `p` varianzas, así que cada componente se lleva una proporción menor y hacen falta más componentes para el mismo porcentaje |
| `S` | Matriz de covarianzas `p × p` de la `X` centrada | unidades² (las de las variables al cuadrado) | No «sube»: es la tabla de la que salen los autovalores; su diagonal son las varianzas y lo de fuera de la diagonal, las covarianzas |
| `λ_k` | Autovalor de la componente `k`: la varianza de los datos en esa dirección | unidades² | Esa componente gana peso en la proporción explicada `λ_k / Σλ` y sube puestos en el orden |
| `v_k` | Autovector de la componente `k`: los pesos de cada variable original | adimensional | Los pesos se reajustan para seguir siendo perpendiculares a los demás; cambia su interpretación, no su longitud (siempre vale 1) |
| `k` | Número de componentes que conservas | componentes | Se conserva más varianza (la suma de los `λ` que te quedas) y se reduce menos: con `k = p` no has reducido nada |
| `X̂ = Z · Vᵗ` | Reconstrucción de los datos con `k` componentes | las de las variables | Cuanto más alto `k`, más se parece `X̂` a `X`; la varianza que queda fuera es exactamente la suma de los autovalores descartados |
:::

## Ejemplo

Seis observaciones de dos variables que se mueven casi juntas:

```
x:  1  2  3  4  5  6
y:  2  3  5  4  6  7
```

- Medias: `x̄ = 3,5` e `ȳ = 4,5`. Se centran las dos columnas.
- Matriz de covarianzas: `S = [[3,5, 3,3], [3,3, 3,5]]`. Cada variable tiene varianza 3,5 y
  comparten 3,3: van muy juntas.
- Autovalores: `λ₁ = 6,8` y `λ₂ = 0,2`. Como `6,8 + 0,2 = 7,0`, la primera componente explica
  `6,8 / 7,0 = 0,971`, es decir el **97,1 %**, y la segunda solo el 2,9 %.
- Autovectores: `v₁ = (0,707, 0,707)` y `v₂ = (0,707, −0,707)`. La primera dirección es «las
  dos variables suben a la vez»; la segunda es «una sube y la otra baja», y apenas tiene
  recorrido en estos datos.
- Puntuaciones sobre la primera componente: −3,54; −2,12; 0,00; 0,00; 2,12; 3,54.

Con dos columnas has pasado de dos números por fila a uno, conservando el 97,1 % de la
varianza. La observación 1 tiene la puntuación más baja y la 6 la más alta: la componente 1 es
un «nivel general» de las dos variables. Si te quedaras con una sola dimensión, perderías lo
poco que distingue a las observaciones 3 y 4 entre sí: tienen la misma media `x + y = 8`, pero
la primera está en `(3, 5)` y la segunda en `(4, 4)`.

:::figura
fichero: pca-varianza-y-proyeccion
pie: El panel izquierdo es el gráfico que decide cuántas componentes conservar. Con ocho variables construidas a partir de tres factores ocultos, la primera dirección se lleva el 57 % de la varianza y las tres primeras el 94 %; a partir de ahí la línea se aplana y cada componente nueva aporta menos de lo que cuesta en interpretación. Ese codo es el argumento, no un umbral mágico: quedarse con dos o con tres es una decisión del problema, y las cinco últimas se pueden tirar sin perder apenas nada. El panel derecho pone precio a la reducción con las seis observaciones del ejemplo: cada punto se sustituye por su sombra sobre la recta roja —la primera componente— y la distancia a esa recta se pierde. Conservas el 97,1 % de la varianza, pero el 2,9 % que tiras es justo lo que distinguía a las observaciones 3 y 4 entre sí. Reducir dimensión es siempre elegir qué se deja fuera, y esa elección no la hace el algoritmo.
fuente: figuras/pca-1.py
:::

## Código

```python verificable
import numpy as np

# Seis observaciones de dos variables que se mueven casi juntas.
x = np.array([1.0, 2, 3, 4, 5, 6])
y = np.array([2.0, 3, 5, 4, 6, 7])
X = np.column_stack([x, y])
Xc = X - X.mean(axis=0)                     # centrar: PCA mide dispersion, no posicion

# Matriz de covarianzas con n-1: cada variable consigo misma y con la otra.
S = Xc.T @ Xc / (X.shape[0] - 1)
print("covarianzas:", np.round(S, 2).ravel().tolist())   # -> [3.5, 3.3, 3.3, 3.5]

valores, vectores = np.linalg.eigh(S)       # eigh: solo matrices simetricas, y sin ordenar
orden = np.argsort(valores)[::-1]           # de mayor a menor varianza
valores, vectores = valores[orden], vectores[:, orden]
print("varianza por componente:", np.round(valores, 4).tolist())     # -> [6.8, 0.2]
print("proporcion explicada:", np.round(valores / valores.sum(), 3).tolist())  # -> [0.971, 0.029]
print("direccion de PC1:", np.round(vectores[:, 0], 3).tolist())     # -> [0.707, 0.707]

puntuaciones = Xc @ vectores                # una columna por componente: aun estan las dos
print("proyeccion sobre PC1:", np.round(puntuaciones[:, 0], 2).tolist())
# -> [-3.54, -2.12, 0.0, 0.0, 2.12, 3.54]
```

:::claves
- `np.linalg.eigh(S)` devuelve los autovalores **sin ordenar** y solo vale para matrices
  simétricas, que es el caso de `S`. De ahí el `np.argsort(valores)[::-1]` de la línea siguiente;
  `np.linalg.eig` también resolvería, pero devuelve números complejos y habría que quedarse con la
  parte real.
- `vectores[:, orden]` ordena las **columnas**. En `eigh` los autovectores vienen en columnas, así
  que `vectores[:, 0]` es la primera componente. Escribir `vectores[orden]` ordena las filas, mezcla
  todas las direcciones entre sí y no da ningún error: el resultado simplemente es otro.
- `X - X.mean(axis=0)` centra **por columnas**: `axis=0` recorre las filas y deja una media por
  variable. Con `axis=1` restarías la media de cada observación y el PCA respondería a otra
  pregunta. Y `S = Xc.T @ Xc / (n − 1)` divide entre `n − 1`, la covarianza muestral, la misma que
  `np.cov(Xc, rowvar=False)`; con `n` los autovalores se multiplican por `(n−1)/n`, aunque la
  proporción explicada no cambia.
- El signo de cada autovector es arbitrario: `v` y `−v` son la misma dirección, así que PC1 puede
  imprimirse como `[0.707, 0.707]` o como `[-0.707, -0.707]` según la versión de la librería. Lo
  que no cambia nunca es la varianza ni el valor absoluto de los pesos: interpreta la dirección,
  no el signo.
- `puntuaciones = Xc @ vectores` devuelve una columna por componente, **incluidas las que vas a
  tirar**: la reducción de verdad es `Xc @ vectores[:, :k]`. La varianza que se pierde al quedarte
  con `k` es exactamente la suma de los autovalores descartados, no una aproximación.
- `Mc.std(axis=0, ddof=1)` usa `ddof=1` para que cada columna estandarizada tenga varianza 1, la
  misma convención que la covarianza de arriba. Con el `ddof=0` que trae NumPy por defecto, las
  columnas se quedan con varianza ligeramente mayor que 1 —por el factor `n / (n − 1)`, que con 500
  filas es 1,002— y la proporción explicada no cambia en absoluto, porque ese factor es el mismo en
  todas las columnas.
:::

```python verificable
import numpy as np

# Las mismas 500 personas: salario en euros y edad en anyos.
rng = np.random.default_rng(0)
salario = rng.normal(30000, 8000, 500)
edad = rng.normal(40, 10, 500)
M = np.column_stack([salario, edad])
Mc = M - M.mean(axis=0)

valores = np.linalg.eigvalsh(Mc.T @ Mc / (M.shape[0] - 1))[::-1]
print("sin escalar:", np.round(valores / valores.sum(), 4).tolist())    # -> [1.0, 0.0]

Z = Mc / Mc.std(axis=0, ddof=1)             # varianza 1 por columna, con la misma ddof que S
valores_z = np.linalg.eigvalsh(Z.T @ Z / (Z.shape[0] - 1))[::-1]
print("estandarizado:", np.round(valores_z / valores_z.sum(), 4).tolist())
# -> [0.5026, 0.4974]
```

El segundo bloque es la advertencia en números: sin estandarizar, la primera componente explica
el 100 % de la varianza y no habla de las personas, solo de que los euros son números más
grandes que los años. Después de estandarizar, las dos variables aportan la mitad cada una.

## Errores típicos

- **No estandarizar cuando las escalas son distintas.** Es el error número uno. PCA maximiza
  varianza, y la varianza se mide en las unidades de cada columna: la variable con números más
  grandes gana siempre. Si las unidades no son comparables, estandariza antes (media 0,
  desviación 1).
- **Poner nombre a las componentes como si fueran variables.** «La componente 1 es el poder
  adquisitivo» solo se sostiene si miras los pesos y tienen sentido. Una componente con pesos
  parecidos y de signos opuestos es una *diferencia*, no un nivel, y se interpreta al revés.
- **Usar los *loadings* para seleccionar variables.** Un peso alto en `v₁` no significa que esa
  variable sea importante para predecir nada; significa que contribuye a la dirección de más
  varianza. Si quieres seleccionar, usa [[seleccion-de-features]]; si quieres importancia para
  un modelo, mira [[importancia-de-variables]].
- **Ajustar el PCA con todos los datos antes de dividir.** Las medias, las desviaciones y las
  direcciones se calculan con el conjunto completo, así que el de prueba influye en la
  transformación que se aplica al de entrenamiento. Es [[fuga-de-datos]], y se evita metiendo
  el PCA dentro de un [[pipelines-de-ml|pipeline]].
- **Elegir componentes por el «90 % de varianza» y confundirlo con capacidad predictiva.** No
  hay ningún umbral mágico —para dibujar bastan dos, para quitar ruido sirve el codo del gráfico
  de varianza explicada y para predecir manda la validación—, y la dirección donde los datos más
  se abren no tiene por qué ser la que separa las clases: puedes conservar el 99 % de la varianza
  y haber tirado justo la dirección que distinguía a los grupos.
- **Aplicar PCA antes de un modelo de árboles.** Los árboles eligen una variable cada vez y no
  sufren con la redundancia ni con las escalas; darles componentes giradas solo les quita
  interpretabilidad y suele empeorar el resultado.

:::practica
enunciado: Dos variables tienen varianza 25 cada una y covarianza 15. Calcula los autovalores de la matriz de covarianzas, la proporción de varianza que explica la primera componente y decide si basta con una sola componente para conservar al menos el 75 % de la varianza.
pista: Con dos variables de varianza idéntica, los autovalores son varianza + covarianza y varianza − covarianza.
solucion: λ₁ = 25 + 15 = 40 y λ₂ = 25 − 15 = 10, así que la varianza total es 40 + 10 = 50. La primera componente explica 40 / 50 = 0,80, el 80 %, y la segunda el 20 %. Como 80 % ≥ 75 %, una sola componente basta; descartar la segunda tira 10 / 50 = 20 % de la varianza, la dirección en la que una variable sube y la otra baja.
:::

## Comprueba que lo sabes

:::quiz
p: Dos variables tienen varianza 3,5 cada una y covarianza 3,3. ¿Qué proporción de la varianza explica la primera componente?
o: El 50 %, porque hay dos variables
o: El 97,1 %, porque su autovalor es 6,8 y el total es 7,0
o: El 3,3 / 3,5 = 94,3 %, que es la correlación entre ambas
a: 2
e: Los autovalores de la matriz de covarianzas son 3,5 + 3,3 = 6,8 y 3,5 − 3,3 = 0,2; suman 7,0, la varianza total. La primera se lleva 6,8 / 7,0 = 97,1 %. El 94,3 % es la correlación (3,3 dividido entre 3,5), que es otra cosa; y el 50 % sería cierto solo si las variables no estuvieran correlacionadas.
:::

:::quiz
p: Tienes un modelo con una variable en euros (de 20.000 a 60.000) y otra en años (de 25 a 60). ¿Qué pasa si haces PCA sin estandarizar?
o: La primera componente será casi la variable en euros, porque su varianza es mucho mayor
o: Las dos variables pesarán lo mismo, porque PCA reparte la varianza
o: PCA fallará porque las unidades no coinciden
a: 1
e: PCA maximiza varianza y la varianza arrastra las unidades. La columna en euros tiene una desviación de miles y la de años de decenas, así que la dirección de más varianza es prácticamente la de los euros. Estandarizando, ambas entran en pie de igualdad. Las unidades distintas no provocan ningún error de cálculo: el problema es de interpretación y de resultado.
:::

:::quiz
p: ¿Por qué no conviene usar PCA antes de un random forest?
o: Porque los componentes principales no se pueden usar con árboles
o: Porque los árboles no necesitan ejes girados ni escalas comparables, y las componentes hacen que se pierda la lectura de cada variable
o: Porque PCA siempre destruye información
a: 2
e: Un árbol divide por umbrales sobre una variable cada vez, así que la redundancia y las escalas no le molestan. Girar los ejes no le aporta nada y además cada división pasa a hablar de una mezcla de variables, con lo que se pierde la interpretación. Y sí se puede usar técnicamente: solo que normalmente no compensa.
:::

:::trampa
Si tu PCA sobre datos sin estandarizar da una primera componente con el 99,9 % de la varianza,
casi nunca es un gran hallazgo: es una columna medida en unidades grandes. Repite el análisis
con las variables estandarizadas y compara. Si el resultado cambia por completo, el primer
resultado no significaba nada.
:::
