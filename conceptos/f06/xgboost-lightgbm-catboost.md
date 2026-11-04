---
id: xgboost-lightgbm-catboost
titulo: XGBoost, LightGBM y CatBoost
fase: 6
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [gradient-boosting, arboles-de-decision, regularizacion-l1-l2, validacion-cruzada]
tags: [boosting, tabular, hiperparametros, categoricas]
resumen: Los tres motores de boosting que dominan los datos tabulares: en qué se diferencian al crecer los árboles y cuándo conviene elegir cada uno.
fuentes: ["Chen y Guestrin (2016), 'XGBoost: A Scalable Tree Boosting System'", "Ke et al. (2017), 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree'", "Prokhorenkova et al. (2018), 'CatBoost: unbiased boosting with categorical features'"]
---

## En una frase

Los tres implementan el mismo algoritmo —[[gradient-boosting|boosting de gradiente]] sobre
árboles de decisión— y se diferencian en tres decisiones de ingeniería: cómo crecen los
árboles, cómo tratan las variables categóricas y cómo se protegen del sobreajuste.

## La idea

El boosting construye árboles en secuencia: cada árbol se entrena sobre el error que dejaron
los anteriores. Esa receta es común a los tres. Lo que cambia, y cambia mucho en la práctica,
es el **cómo**.

Piensa en tres albañiles construyendo el mismo muro. El primero (XGBoost) coloca los
ladrillos **fila a fila**: nunca empieza la fila 4 hasta terminar la 3. Eso da árboles
equilibrados y predecibles, pero gasta trabajo en ramas que apenas aportan. El segundo
(LightGBM) coloca el ladrillo **donde más falta hace**, aunque quede un torreón torcido: crece
siempre por la hoja que más reduce el error. Escribe menos árboles para el mismo error, con el
riesgo de hacer ramas muy profundas y de sobreajustar si no se le pone freno. El tercero
(CatBoost) construye **por niveles simétricos** —la misma división en todo un nivel, lo que
hace del árbol un objeto muy regular y barato de evaluar— y, sobre todo, resuelve el problema
que los otros dos dejan al usuario: qué hacer con las variables categóricas.

Ese es el segundo eje. Codificar «ciudad» con 3.000 valores mediante one-hot dispara la
dimensionalidad; codificarla por la media del objetivo es eficaz pero **filtra la etiqueta de
la propia fila**, que es una forma clásica de [[fuga-de-datos|fuga de datos]]. CatBoost usa
*estadísticas ordenadas*: para cada fila calcula la media del objetivo usando solo las filas
anteriores en una permutación aleatoria, así que el dato de esa fila nunca entra en su propio
codificador.

El tercer eje es la velocidad. LightGBM y el XGBoost moderno agrupan cada variable continua en
unos cientos de intervalos (*histogramas*, `max_bin`), de modo que buscar el mejor corte
cuesta recorrer intervalos y no valores únicos. En tablas de millones de filas, esa es la
diferencia entre minutos y horas. Y el cuarto, silencioso: LightGBM es muy sensible a pocas
filas por hoja (`min_data_in_leaf`) y CatBoost es el que mejor se porta *de fábrica* cuando no
tienes tiempo de afinar nada.

## Definición formal

Los tres ajustan un modelo aditivo de `K` árboles:

:::formula
ŷᵢ = Σₖ₌₁ᴷ fₖ(xᵢ),  con  fₖ ∈ ℱ (el espacio de los árboles)
:::

- `xᵢ` — vector de variables de la observación `i`.
- `fₖ` — el árbol número `k`; cada árbol devuelve un valor constante por hoja.
- `ŷᵢ` — la predicción final, la suma de las contribuciones de todos los árboles.
- `ℱ` — el conjunto de todas las particiones posibles del espacio de variables.

El entrenamiento es voraz y por etapas. En el paso `t`, con la pérdida
`L = Σᵢ l(yᵢ, ŷᵢ⁽ᵗ⁻¹⁾ + fₜ(xᵢ))`, se elige el árbol que maximiza

:::formula
Ganancia = ½ · [ G_L²/(H_L + λ) + G_R²/(H_R + λ) − G²/(H + λ) ] − γ
:::

- `G_L`, `G_R` — suma de gradientes (primeras derivadas de la pérdida) en el hijo izquierdo y
  el derecho.
- `H_L`, `H_R` — suma de hessianas (segundas derivadas) en cada hijo.
- `G`, `H` — las mismas sumas en el nodo padre.
- `λ` — regularización L2 sobre el valor de las hojas; encoge las ganancias dudosas.
- `γ` — umbral mínimo de ganancia para aceptar una división; es la poda previa.

Tres diferencias que sí cambian el resultado:

| Motor | Crecimiento | Categóricas | Frenos principales |
| --- | --- | --- | --- |
| XGBoost | Por niveles, profundidad fija | One-hot o codificación previa tuya | `max_depth`, `min_child_weight`, `lambda` |
| LightGBM | Por hoja, siempre la de mayor ganancia | Soporte nativo con `categorical_feature` | `num_leaves`, `min_data_in_leaf`, `feature_fraction` |
| CatBoost | Niveles simétricos (árboles *oblivious*) | Estadísticas ordenadas sobre el objetivo | `depth`, `l2_leaf_reg`, `one_hot_max_size` |

En LightGBM manda `num_leaves`: 31 equivale en capacidad a un árbol equilibrado de
profundidad 5, y subirlo a 255 da un modelo mucho más expresivo y mucho más fácil de
sobreajustar. En XGBoost el equivalente es `max_depth`.

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa con la ganancia del corte si sube |
| --- | --- | --- | --- |
| `G_L`, `G_R` | Suma de gradientes (primeras derivadas) en cada hijo | las de la pérdida | La ganancia crece con su cuadrado: separa mejor los residuos de cada lado |
| `H_L`, `H_R` | Suma de hessianas (segundas derivadas) en cada hijo | las de la pérdida | Va en el denominador: reparte el gradiente entre más peso y **baja** la ganancia de ese hijo |
| `G`, `H` | Las mismas sumas en el nodo padre | las de la pérdida | Es el término que se resta: si el padre ya está bien separado, dividirlo aporta menos |
| `λ` | Regularización L2 sobre el valor de las hojas | adimensional | Encoge todos los términos y la ganancia cae: con `λ = 16` el mejor corte baja de 8,0 a 0,9 |
| `γ` | Umbral mínimo de ganancia para aceptar la división | las de la pérdida | No cambia la ganancia calculada, cambia la decisión: por encima de ella no se divide nada |
| `T` | Número de hojas del árbol | hojas | Cada hoja nueva paga `γ`: subirlo deja el árbol más pequeño |
| `w_j` | Valor asignado a la hoja `j` | las de `y` | El peso óptimo es `−Σg_i / (Σh_i + λ)`, así que también se encoge al subir `λ` |
| `num_leaves` | Hojas máximas de LightGBM | hojas | Sube la capacidad y el riesgo de sobreajuste: 255 hojas es un árbol muy expresivo |
| `min_data_in_leaf` | Mínimo de filas en una hoja | filas | Con valores altos no se abren hojas pequeñas y se pierden cortes de ganancia alta pero con pocos casos |
:::

:::figura
fichero: boosting-ganancia-regularizada-y-crecimiento
pie: La fórmula de ganancia es la misma en los tres motores; lo que cambia es cómo la usan. A la izquierda se ve el efecto de λ: las tres curvas caen y la división deja de compensar cuando cruzan la línea de γ = 2, así que la regularización decide qué cortes sobreviven antes de mirar los datos. A la derecha, el esquema del segundo eje: XGBoost crece por niveles, así que sus cuatro hojas llegan a la vez; LightGBM crece por hoja y alarga solo la rama que más reduce la pérdida, con lo que llega al mismo error con menos divisiones pero con ramas muy desiguales. Esa desigualdad es la que obliga a frenarlo con `num_leaves` y `min_data_in_leaf`.
fuente: figuras/xgboost-lightgbm-catboost-1.py
:::

## Ejemplo

Cuatro observaciones con una sola variable `x` y el residuo que hay que ajustar en la primera
iteración (las primeras derivadas `g`), con hessianas `h = 1` en todas:

```
x       =   1     2     4     7
g       = -3.0  -1.0   1.0   3.0
```

Como `h = 1`, cada `H` es simplemente el número de filas. Con `λ = 0` y `γ = 0`, la ganancia
de cada corte es `½ · [G_L²/n_L + G_R²/n_R − G²/n]`:

- Corte entre 1 y 2: `G_L = −3`, `G_R = 3`; ganancia = ½ · [9/1 + 9/3 − 0/4] = **6,0**
- Corte entre 2 y 4: `G_L = −4`, `G_R = 4`; ganancia = ½ · [16/2 + 16/2 − 0/4] = **8,0**
- Corte entre 4 y 7: `G_L = −3`, `G_R = 3`; ganancia = ½ · [9/3 + 9/1 − 0/4] = **6,0**

El mejor corte es `x ≤ 3`: deja un hijo con {1, 2} y peso de hoja `+2` (`−G_L/H_L`) y otro con
{4, 7} y peso `−2`. La predicción sobre esas cuatro filas es exactamente `(+2, +2, −2, −2)`, que
baja el error cuadrático de 20 a 4 —la caída, 16, es el doble de la ganancia de 8 porque la
pérdida lleva el factor `½`—. Con `γ = 9` ninguna división superaría el umbral y el
árbol se quedaría en una sola hoja: así funciona la poda previa.

## Código

```python verificable
import numpy as np

# La ganancia de XGBoost, calculada a mano sobre cuatro residuos.
x = np.array([1.0, 2.0, 4.0, 7.0])
g = np.array([-3.0, -1.0, 1.0, 3.0])   # primeras derivadas (gradiente)
h = np.ones(4)                          # hessianas: 1 con perdida cuadratica
lam = 0.0

def ganancia(corte):
    izq, der = x <= corte, x > corte
    gl, hl = g[izq].sum(), h[izq].sum()
    gr, hr = g[der].sum(), h[der].sum()
    padre = g.sum() ** 2 / (h.sum() + lam)
    return 0.5 * (gl**2 / (hl + lam) + gr**2 / (hr + lam) - padre)

for corte in (1.5, 3.0, 5.5):
    print(f"corte x <= {corte:>3.1f}  ganancia {ganancia(corte):.1f}")
# -> corte x <= 1.5  ganancia 6.0
# -> corte x <= 3.0  ganancia 8.0
# -> corte x <= 5.5  ganancia 6.0
```

:::claves
- `izq, der = x <= corte, x > corte` no devuelve números: devuelve **máscaras booleanas** del mismo
  tamaño que `x`. Después, `g[izq]` selecciona las posiciones donde la máscara es `True`. Por eso
  los dos sumandos de la ganancia se calculan sin ningún `if`.
- `.sum()` sobre una máscara vacía devuelve `0.0`, no un error. Ese cero es la trampa del primer
  bloque: si un corte deja un hijo sin filas, `gl**2 / (hl + lam)` pasa a ser `0/0` cuando `lam = 0`
  y sale `nan`. En producción se descartan los cortes que dejan un hijo vacío.
- `h = np.ones(4)` con la pérdida cuadrática **no es una simplificación**: la segunda derivada de
  `½(y − F)²` respecto a `F` vale exactamente 1. Con pérdida logística `h` sería `p·(1 − p)` y cada
  fila pesaría distinto.
- `padre = g.sum() ** 2 / (h.sum() + lam)` usa el total del nodo, no un hijo. Es el término que se
  **resta**: la ganancia mide cuánto mejora dividir respecto a no dividir.
- `0.5 * (...)` es el `½` de la fórmula. Olvidarlo duplica todas las ganancias y hace que un `γ`
  ajustado deje de tener sentido: los umbrales y las ganancias tienen que estar en la misma escala.
- El segundo bloque reutiliza el nombre `ganancia` para **otra** función, con los sumandos ya hechos
  a mano. En un fichero de verdad conviene no repetir el nombre: la segunda definición tapa a la
  primera y quien lea el código puede llamar a la que no es.
:::

```python verificable
import numpy as np

# La regularizacion lambda encoge la ganancia: con lambda grande la division no compensa.
g = np.array([-3.0, -1.0, 1.0, 3.0])

def ganancia(gl, hl, gr, hr, lam):
    total = 0.5 * (gl**2 / (hl + lam) + gr**2 / (hr + lam) - g.sum() ** 2 / (4 + lam))
    return total

# El mejor corte separa {1, 2} de {4, 7}: G_L = -4, H_L = 2, G_R = 4, H_R = 2
for lam in (0.0, 4.0, 16.0):
    print(f"lambda {lam:>4.1f}  ganancia del mejor corte  {ganancia(-4.0, 2.0, 4.0, 2.0, lam):.2f}")
# -> lambda  0.0  ganancia del mejor corte  8.00
# -> lambda  4.0  ganancia del mejor corte  2.67
# -> lambda 16.0  ganancia del mejor corte  0.89
```

## Errores típicos

- **Afinar hiperparámetros antes de tener una buena validación.** Con millones de filas,
  XGBoost con los valores por defecto ya es competitivo. Un
  [[validacion-cruzada|esquema de validación]] honesto (y temporal si hay fechas) mejora más
  el resultado que cualquier rejilla.
- **Usar `num_leaves` alto con pocos datos.** Es el error número uno de LightGBM: un
  `num_leaves` de 255 con 5.000 filas construye hojas con 20 observaciones que memorizan
  ruido. Si subes `num_leaves`, sube también `min_data_in_leaf` (por defecto 20) y el número
  de estimadores con una `learning_rate` más baja.
- **Codificar categóricas de cardinalidad alta a mano antes de LightGBM o CatBoost.** Si
  conviertes «producto» (10.000 valores) en 10.000 columnas one-hot, tiras la ventaja de
  ambos motores y además haces inviable la búsqueda de cortes. Pásalas como categóricas
  nativas o deja que CatBoost las ordene él.
- **Comparar los tres midiendo solo el tiempo de entrenamiento.** CatBoost suele entrenar más
  lento y predecir más rápido (árboles simétricos, muy vectorizables); LightGBM entrena
  rapidísimo y puede predecir más lento por hoja. Si el modelo va a servir en producción con
  mucho tráfico, mide también la latencia de inferencia.
- **Pensar que uno «gana» siempre.** Con datos tabulares, la diferencia entre los tres bien
  afinados es pequeña y depende de las variables, de la cardinalidad de las categóricas y del
  ruido. Lo correcto es probar los tres con la misma partición y quedarse con el que gane
  **fuera de la muestra**, no con el que tenga más fama.
- **Dar por bueno un `gain` de importancia de variables como verdad causal.** La importancia
  por ganancia favorece variables con muchos valores distintos. Para interpretar de verdad,
  mira [[interpretabilidad-shap|los valores de SHAP]].

:::practica
enunciado: Cuatro filas con gradientes g = [−2, −2, +2, +2] y hessianas h = 1. El corte que separa las dos primeras filas de las dos últimas deja G_L = −4, H_L = 2, G_R = +4 y H_R = 2, con G = 0 en el padre. Con λ = 4 y γ = 2, calcula la ganancia y decide si la división se hace.
pista: La ganancia bruta suma G²/(H+λ) de cada hijo, resta el término del padre y le quita γ.
solucion: Ganancia = ½ · [16/(2+4) + 16/(2+4) − 0/(4+4)] − 2 = ½ · 5,333 − 2 = 2,667 − 2 = 0,667, positiva: la división se acepta. Con λ = 0 daría 8 − 2 = 6; con λ = 16 la ganancia bruta cae a ½ · 1,778 = 0,889 y ya no supera γ = 2.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia práctica hay entre un árbol que crece por niveles y uno que crece por hoja?
o: El de por niveles siempre acierta más; el de por hoja es solo más rápido
o: El de por hoja elige siempre la hoja con mayor ganancia, así que llega al mismo error con menos árboles pero produce ramas desiguales y se sobreajusta antes si no se limita
o: El de por niveles no puede usar variables continuas
a: 2
e: La ganancia por hoja concentra el esfuerzo donde más se reduce la pérdida, lo que da eficiencia pero también profundidad descontrolada. Por eso LightGBM se regula con `num_leaves` y `min_data_in_leaf`, mientras que XGBoost corta con `max_depth`. Los dos usan variables continuas y ninguno es «más listo» en general.
:::

:::quiz
p: ¿Por qué CatBoost usa estadísticas ordenadas para las variables categóricas?
o: Para que el entrenamiento ocupe menos memoria
o: Porque codificar una categoría con la media del objetivo de todas las filas incluye la etiqueta de la propia fila y filtra información; el orden garantiza que cada fila se codifique solo con filas anteriores
o: Porque así no hace falta separar datos de entrenamiento y prueba
a: 2
e: La media del objetivo calculada sobre todo el conjunto mete la etiqueta de la fila en su propia variable: el modelo ve parte de la respuesta y la métrica de validación sale inflada. Las permutaciones con orden evitan ese filtro. CatBoost no elimina la necesidad de validar: solo arregla ese punto concreto.
:::

:::truco
Si tienes que elegir en cinco minutos: LightGBM para tablas grandes con variables numéricas,
CatBoost si abundan las categóricas de cardinalidad alta, y XGBoost si necesitas reproducir
un resultado publicado o ya tienes un pipeline afinado con él. Con los tres, empieza con una
`learning_rate` de 0,05 y muchos árboles antes de tocar la profundidad.
:::
