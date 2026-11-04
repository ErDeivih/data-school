---
id: escalado-y-transformacion
titulo: Escalado y transformación
fase: 5
nivel: intermedio
rutas: [ds, core]
prerequisitos: [medidas-de-dispersion, z-score-y-estandarizacion, distribuciones-en-datos-reales]
tags: [escalado, transformacion, preprocesamiento]
resumen: Poner las variables en unidades comparables y acercar su forma a la normal: imprescindible en unos modelos, indiferente en otros y una fuente de fuga si se hace mal.
fuentes: ["Box y Cox (1964), 'An Analysis of Transformations'", "Yeo y Johnson (2000), 'A New Family of Power Transformations to Improve Normality or Symmetry'"]
---

## En una frase

Escalar cambia las unidades de una variable para que todas pesen lo mismo en una distancia o en
una penalización, y transformar cambia la forma de su distribución; ninguna de las dos cosas
añade información, pero las dos cambian lo que el modelo aprende.

## La idea

Imagina que quieres agrupar pisos por lo deseables que son y usas dos variables: superficie en
metros cuadrados (de 40 a 200) y precio en euros (de 90.000 a 800.000). Si calculas la distancia
euclídea tal cual, el precio aporta cifras miles de veces mayores y la superficie deja de contar
por completo. No es que el precio importe más: es que está en otra unidad. **Escalar es quitar
la unidad de en medio** para que la distancia mida parecido en todas las direcciones.

Ese problema solo existe en los modelos que comparan distancias o que reparten una penalización
entre los coeficientes:

- **Les afecta mucho:** KNN, SVM, k-means y cualquier agrupamiento, PCA, regresión con
  regularización (ridge, lasso), redes neuronales. En todos ellos la escala de entrada entra
  directamente en la cuenta.
- **No les afecta:** los árboles de decisión y sus conjuntos, como
  [[gradient-boosting|el boosting]] o los bosques. Un árbol parte por umbrales y da igual que la
  variable vaya de 0 a 1 o de 0 a 1.000.000: el orden es el mismo.

La segunda mitad del concepto es la **transformación de la forma**. Muchas variables reales son
multiplicativas y con cola a la derecha: el salario, el precio de la vivienda, el número de
visitas. Aplicar un logaritmo convierte «multiplicar por 2» en «sumar una constante», comprime
la cola y acerca la distribución a una normal, que es lo que los modelos lineales y los
intervalos de confianza agradecen. Es la diferencia entre modelar «el precio sube un 10 %» y
modelar «el precio sube 20.000 €»: lo primero suele ser lo que de verdad ocurre.

:::figura
fichero: escalado-a-quien-aplasta-cada-metodo
pie: Los seis valores del ejemplo (1, 2, 3, 4, 5 y 100) bajo los cuatro escalados, cada uno dibujado en su propio rango de 0 a 1 para poder compararlos. Fíjate en dónde caen los cinco valores normales: con min-max ocupan el 4 % de la escala y el 100 se lleva el otro 96 %, así que en la práctica se han vuelto indistinguibles; con z-score se quedan casi pegados y el 100 se va a +2,04; con el escalado robusto el grupo respira (de −1,0 a 0,6) y el 100 se dispara a 38,6. Solo el logaritmo reparte los cinco entre 0,69 y 1,79 conservando las distancias. Ninguna escala arregla el extremo: lo único que se elige es a quién aplasta.
fuente: figuras/escalado-y-transformacion-1.py
:::

## Definición formal

Con `x` una variable y `x₁, …, xₙ` sus valores observados:

- **Normalización min-max:** `x' = (x − min(x)) / (max(x) − min(x))`. Deja todo en `[0, 1]`.
- **Estandarización (z-score):** `z = (x − μ) / σ`, con `μ` la media y `σ` la desviación típica.
  No tiene límites y no garantiza simetría.
- **Escalado robusto:** `x' = (x − mediana(x)) / IQR`, con `IQR` el rango intercuartílico, es
  decir el percentil 75 menos el percentil 25.
- **Logaritmo:** `x' = ln(1 + x)`, escrito `log1p`. El `+1` permite el cero sin ir a menos
  infinito. Solo sirve para valores no negativos.
- **Box-Cox:** para `x > 0` y un parámetro `λ`, `x^(λ) = (x^λ − 1) / λ` si `λ ≠ 0`, y
  `x^(λ) = ln(x)` si `λ = 0`. `λ` se estima por máxima verosimilitud; `λ = 1` es no hacer nada,
  `λ = 0,5` es una raíz cuadrada y `λ = 0` es el logaritmo.
- **Yeo-Johnson:** la misma idea pero definida también para valores negativos, con una rama
  distinta a cada lado del cero.

:::formula
min-max: x' = (x − min) / (max − min)   ·   z-score: z = (x − μ) / σ   ·   robusto: x' = (x − mediana) / IQR
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x` | El valor que se transforma | las de la variable | No cambia la transformación: cambia dónde cae el resultado dentro del rango |
| `min`, `max` | Mínimo y máximo **del conjunto de entrenamiento** | las de `x` | El rango `max − min` es el denominador. Un solo extremo grande lo infla y aplasta al resto: con 100 en el ejemplo, los valores 1 a 5 quedan por debajo de 0,04 |
| `μ` | Media del conjunto de entrenamiento | las de `x` | Centra el z-score; la arrastra cualquier extremo, así que con cola larga el cero deja de estar en el centro real |
| `σ` | Desviación típica del conjunto de entrenamiento | las de `x` | Es el denominador del z-score. Con `ddof=1` (muestral, pandas) sale algo mayor que con `ddof=0` (poblacional, scikit-learn): con `n` grande da igual, con 20 filas no |
| `mediana` | Mediana del conjunto de entrenamiento | las de `x` | Centro del escalado robusto; no la mueve un extremo, por eso el grupo de valores normales conserva su separación |
| `IQR` | Rango intercuartílico: percentil 75 menos percentil 25 | las de `x` | Anchura de la caja del escalado robusto. Si es 0 (más de la mitad de los datos repetidos) la división se va a infinito |
| `λ` | Parámetro de Box-Cox, estimado por máxima verosimilitud | adimensional | Es la potencia que se aplica: `λ = 1` no hace nada, `λ = 0,5` es una raíz cuadrada, `λ = 0` es el logaritmo. Solo se estima con `x > 0`; con ceros o negativos hay que pasar a Yeo-Johnson |
| `c` | Desplazamiento en `ln(x + c)`, cuando hay ceros | las de `x` | Con `c = 1` es `log1p` y el cero se queda en 0. Un `c` grande acerca la transformación a una recta y pierde el efecto sobre la cola: elígelo a conciencia, no por comodidad |
:::

Tres reglas que no se pueden saltar:

1. **Los parámetros se estiman solo con el conjunto de entrenamiento.** `min`, `max`, `μ`, `σ`,
   la mediana, el IQR y `λ` son números aprendidos de los datos; si los calculas con todo el
   conjunto antes de dividir, el conjunto de prueba ha participado en el preprocesamiento. Eso
   es [[fuga-de-datos|fuga de datos]], y es de las que no se ven.
2. **Se aplica la misma transformación a entrenamiento, validación, prueba y producción.** Se
   guarda el objeto entrenado (por ejemplo un `StandardScaler`) y se reutiliza. Nunca se
   recalcula sobre datos nuevos.
3. **Las variables binarias y las categóricas codificadas con one-hot no se escalan.** Un 0 y
   un 1 ya están en la misma escala; estandarizarlos destruye su lectura.

## Ejemplo

Seis valores: cinco normales y uno enorme.

```
1   2   3   4   5   100
```

- **Min-max.** El rango es 99. El 2 se convierte en (2 − 1) / 99 = **0,0101** y el 4 en
  **0,0303**. Los cinco valores normales quedan apretados entre 0 y 0,04: el extremo se ha
  comido el intervalo entero.
- **Z-score con desviación muestral (`ddof=1`).** La media es 19,17 y la desviación 39,63, así
  que el 2 queda en **−0,43** y el 100 en **+2,04**.
- **Z-score de scikit-learn (`ddof=0`).** La misma operación con la desviación poblacional da
  **−0,50** para el 1 y **+2,23** para el 100. El 100 no cambia de interpretación, pero los
  números no coinciden con los de la fórmula muestral: hay que saber cuál usa cada herramienta.
- **Escalado robusto.** Mediana 3,5 e IQR 2,5. Los cinco valores normales se reparten entre
  **−1,0** y **0,6** y el 100 se va a **38,6**. Ninguna escala arregla un valor extremo; lo
  único que cambia es a quién aplasta.

Y para la forma, con una variable claramente asimétrica:

- Asimetría original: **1,38**.
- Asimetría tras `log1p`: **0,31**.
- Asimetría tras Box-Cox (con `λ = −0,07` estimado): **0,04**.

El logaritmo ya arregla la mayor parte; Box-Cox afina el resto eligiendo la potencia que mejor
simetriza.

## Código

```python verificable
import numpy as np

# Cinco valores normales y uno extremo: el mismo dato, dos escalados.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 100.0])

minmax = (x - x.min()) / (x.max() - x.min())
z = (x - x.mean()) / x.std(ddof=1)      # ddof=1: estimamos la media de la muestra

print(f"min-max de 2.0   {minmax[1]:.4f}")   # -> 0.0101
print(f"min-max de 4.0   {minmax[3]:.4f}")   # -> 0.0303
print(f"z-score de 2.0   {z[1]:+.2f}")       # -> -0.43
print(f"z-score de 100   {z[5]:+.2f}")       # -> +2.04
```

:::claves
- `x - x.min()` es una resta **elemento a elemento** sobre el array entero: devuelve un array nuevo de seis elementos, no un número. Lo mismo con `x / x.std(ddof=1)`. Python no tiene quejas de formas porque las tres piezas (array, array, escalar) encajan; si en vez de `x.mean()` escribieras `np.mean` (sin paréntesis) obtendrías una función y NumPy intentaría difundirla como si fuera un número.
- `ddof=1` divide entre `n − 1` y `ddof=0` (el valor por defecto) entre `n`. Con estos seis valores la diferencia es visible: `x.std(ddof=1)` vale 39,63 y `x.std(ddof=0)` vale 36,17, así que el z-score del 100 es +2,04 o +2,23 según cuál uses. `StandardScaler` de scikit-learn usa `ddof=0`; pandas `.std()` usa `ddof=1`. Si comparas sus salidas sin saber esto, creerás que una está mal.
- `minmax[1]` y `z[1]` son **el mismo índice**, el del valor 2, no el segundo valor distinto. La numeración empieza en 0, así que el 2 está en la posición 1 y el 100 en la 5. Si el array tuviera un índice de fechas en pandas, `minmax[1]` sería un error o una columna, y habría que usar `.iloc[1]`.
- `x.std()` devuelve un `np.float64`, y `(x - x.mean()) / x.std(ddof=1)` devuelve un array de `np.float64`. El f-string con `:+.2f` solo formatea la salida; el array sigue ahí. Si guardas `z` en un DataFrame, la columna será `float64`, no un objeto de Python.
- El min-max de este bloque no tiene un valor fijo: el 0,0101 del valor 2 sale de dividir entre
  `max − min = 99`, y con otro máximo el mismo 2 daría otro número. Recalculado sobre datos
  nuevos da otra cosa, y por eso el escalador se ajusta solo con entrenamiento y se reutiliza.
- El `.round(2).tolist()` del bloque con `StandardScaler` existe **solo para imprimir**: convierte el array de NumPy en una lista de Python. Si te quedas con la lista y sigues operando, pierdes el álgebra de NumPy, porque `lista * 2` repite los elementos en vez de multiplicarlos. Compruébalo con `np.round(a, 2) * 2` frente a `np.round(a, 2).tolist() * 2`.
:::

```python verificable
import numpy as np
from scipy import stats

# Una cola larga de verdad: cada valor es casi el doble que el anterior.
x = np.array([1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0])
print(f"asimetria original  {stats.skew(x):.2f}")           # -> 1.38
print(f"asimetria con log1p {stats.skew(np.log1p(x)):.2f}")  # -> 0.31

# Box-Cox estima la potencia por maxima verosimilitud; lambda=0 seria el logaritmo.
ajustado, lam = stats.boxcox(x)
print(f"asimetria Box-Cox   {stats.skew(ajustado):.2f}")     # -> 0.04
print(f"lambda estimada     {lam:.2f}")                      # -> -0.07
```

```python verificable
import numpy as np
from sklearn.preprocessing import RobustScaler, StandardScaler

x = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [100.0]])

# StandardScaler usa la desviacion poblacional (ddof=0); comprime el grupo normal.
print("standard", np.round(StandardScaler().fit_transform(x).ravel(), 2).tolist())
# -> [-0.5, -0.47, -0.45, -0.42, -0.39, 2.23]

# RobustScaler usa mediana e IQR: no lo mueve el extremo y mantiene separado el grupo.
print("robust  ", np.round(RobustScaler().fit_transform(x).ravel(), 2).tolist())
# -> [-1.0, -0.6, -0.2, 0.2, 0.6, 38.6]
```

## Errores típicos

- **Escalar con todo el conjunto antes de dividir.** `scaler.fit(X)` sobre la tabla completa
  mete la media y la desviación del conjunto de prueba en el entrenamiento. Ajusta solo con
  entrenamiento y aplica `transform` al resto, dentro de un
  [[pipelines-de-ml|pipeline]] para no olvidarlo.
- **Creer que hay que escalar siempre.** Si tu modelo es un bosque o un boosting de árboles
  ([[gradient-boosting|Gradient Boosting]]), escalar no cambia ni una predicción y añade un
  paso que hay que mantener. Mira primero qué modelo vas a usar.
- **No darse cuenta de que la desviación no es la misma en todas partes.**
  [[z-score-y-estandarizacion|El z-score]] se puede calcular con `ddof=0` (poblacional, lo que
  hace scikit-learn) o `ddof=1` (muestral, lo que hace pandas por defecto en `std`). Con `n`
  grande da igual; con 20 filas, no.
- **Aplicar logaritmo a valores negativos o a ceros.** `ln(0)` es menos infinito y la fila se
  pierde. Usa `log1p`, o un desplazamiento `ln(x + c)` con `c` elegido a conciencia, o
  Yeo-Johnson si hay negativos.
- **Escalar la variable objetivo sin deshacerlo después.** Si entrenas con el logaritmo del
  precio, las predicciones salen en escala logarítmica. Hay que aplicar la inversa
  (`expm1`) y, si el modelo minimiza error cuadrático, saber que la media de los logaritmos no
  es el logaritmo de la media.
- **Estandarizar columnas one-hot.** Una columna binaria estandarizada deja de ser «está o no
  está» y pasa a tener valores como −0,3. Además, con una categoría muy rara, la desviación
  típica es casi cero y la división dispara el valor. Deja las binarias en paz.

:::practica
enunciado: En una tabla de pisos la superficie va de 40 a 200 m² y el precio de 90.000 a 800.000 €. Calcula cuántas veces pesa más el precio que la superficie en una distancia euclídea y decide qué escalas y qué no para un KNN.
pista: El rango del precio es 710.000 y el de la superficie 160: la distancia la domina la variable con números grandes, no la más informativa.
solucion: Rango del precio = 800.000 − 90.000 = 710.000; rango de la superficie = 200 − 40 = 160. Cociente = 710.000 / 160 = 4.437,5: el precio recorre un rango 4.437,5 veces mayor, así que domina la distancia y la superficie deja de contar. Estandariza o normaliza las dos numéricas; la columna binaria de garaje (0/1) no se toca, porque un 0 y un 1 ya están en la misma escala.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el min-max deja los cinco valores normales del ejemplo apretados entre 0 y 0,04?
o: Porque el rango total lo fija el valor 100, así que cada unidad vale muy poco en la escala nueva
o: Porque el min-max siempre comprime los valores pequeños por definición
o: Porque la media de los datos es 19,17 y el 4 está por debajo
a: 1
e: El denominador es `max − min = 99`. Un valor que sube una unidad avanza 1/99 del intervalo, así que los valores de 1 a 5 ocupan menos del 5 % de la escala y el 100 se queda con el resto. No es una propiedad general del min-max: es consecuencia del valor extremo.
:::

:::quiz
p: Vas a entrenar un bosque aleatorio y una regresión con penalización ridge sobre las mismas variables. ¿Qué haces con el escalado?
o: Escalar en los dos casos, porque nunca hace daño
o: Escalar para el ridge y no escalar para el bosque
o: No escalar en ninguno, porque el ridge ya se encarga de la escala con la penalización
a: 2
e: Ridge penaliza la suma de coeficientes al cuadrado, y un coeficiente se mide en unidades de la variable: sin escalar, la penalización castiga mucho más a las variables con números grandes. El bosque parte por umbrales y el orden de los valores no cambia al escalarlos.
:::

:::trampa
Un `StandardScaler` guardado en un fichero y reutilizado en producción es correcto; uno
reentrenado cada día con los datos del día, no. Si la media se recalcula, la misma fila produce
una predicción distinta según el día en que llegue, y eso rompe cualquier comparación con el
backtest.
:::
