---
id: norma-y-distancias
titulo: Normas y distancias
fase: 1
nivel: intermedio
rutas: [core, ds, alg]
prerequisitos: [producto-punto-y-similitud]
tags: [algebra-lineal, distancia, metricas, knn]
resumen: Una norma mide el tamaño de un vector y una distancia, la separación entre dos puntos; elegir L1, L2, L∞ o Mahalanobis decide qué significa «cerca».
fuentes: ["Deisenroth, Faisal y Ong (2020), 'Mathematics for Machine Learning'", "Hastie, Tibshirani y Friedman (2009), 'The Elements of Statistical Learning'"]
---

## En una frase

Una **norma** asigna un tamaño a un vector y una **distancia** mide la separación entre dos
puntos, normalmente como la norma de su diferencia; cambiar de L1 a L2, a L∞ o a Mahalanobis
no es un detalle técnico: cambia qué puntos consideras vecinos, y con ellos el resultado de un
[[knn|KNN]], un [[k-means|K-means]] o un [[clustering-jerarquico|clustering jerárquico]].

## La idea

Estás en el centro de una ciudad y quieres saber a qué punto puedes llegar antes. Si puedes
volar, la distancia es la recta: la **distancia euclídea** o L2. Si solo puedes caminar por
calles que forman una cuadrícula perfecta, tienes que sumar las manzanas horizontales y las
verticales: eso es la **distancia Manhattan** o L1. Si lo que mides es el tiempo hasta el
punto más lejano, solo te importa la peor coordenada: eso es la norma **infinito** (L∞).

Las tres son distancias legítimas, y las tres dan respuestas distintas. El rombo de L1 y el
círculo de L2 no coinciden: un punto con diferencia `(3, 4)` está a distancia 7 en L1 y a 5 en
L2. Además, L2 es la única que no cambia si giras los ejes; L1 y L∞ dependen de cómo estén
orientadas las coordenadas. Eso importa cuando tus ejes son arbitrarios (¿por qué el eje 1 y
no una combinación de los dos?).

La cuestión de fondo es que **distancia es una decisión de modelado**, no una verdad. Si mides
personas por altura en centímetros y peso en gramos, la distancia euclídea estará dominada por
el peso: una diferencia de 2 kg son 2.000 unidades frente a los 2 de una diferencia de 2 cm.
Estandarizar las variables lo arregla
a medias; la **distancia de Mahalanobis** lo arregla del todo, porque no solo corrige la escala
de cada variable sino también su correlación. Si dos variables se mueven siempre juntas, un
punto que se sale de esa pauta es raro aunque esté cerca en línea recta.

:::figura
fichero: normas-y-mahalanobis
pie: A la izquierda, las tres bolas de radio 1 (rombo, círculo y cuadrado): el mismo radio encierra conjuntos distintos, y ese conjunto es lo que cada norma llama «vecinos». A la derecha, dos variables con correlación 0,9: en línea recta (1, 1) es el punto más lejano, pero es el más normal de los tres; los raros son (1, 0) y (0, 1), que en Euclídea parecían cercanos.
fuente: figuras/norma-y-distancias-1.py
:::

## Definición formal

**Norma.** Una función `‖·‖ : ℝⁿ → ℝ` es una norma si cumple: `‖x‖ ≥ 0` y `‖x‖ = 0` solo si
`x = 0`; `‖c·x‖ = /c/ · ‖x‖` para todo escalar `c`; y `‖x + y‖ ≤ ‖x‖ + ‖y‖` (desigualdad
triangular). Las normas `p` se definen así, con `/xᵢ/` el valor absoluto de la componente `i`:

:::formula
‖x‖ₚ = ( Σᵢ₌₁ⁿ /xᵢ/ᵖ )^(1/p)      para p ≥ 1
:::

- `p = 1` → **L1** o Manhattan: `‖x‖₁ = Σᵢ /xᵢ/`. Suma de los valores absolutos.
- `p = 2` → **L2** o euclídea: `‖x‖₂ = √(Σᵢ xᵢ²)`. La de uso diario.
- `p → ∞` → **L∞** o máximo: `‖x‖∞ = maxᵢ /xᵢ/`. Solo cuenta la coordenada mayor.
- `p < 1` no es una norma: incumple la desigualdad triangular.

**Distancia.** `d(x, y) = ‖x − y‖` con la norma que hayas elegido. Una distancia es una
**métrica** si cumple `d(x, y) = 0` solo cuando `x = y`, simetría `d(x, y) = d(y, x)` y
desigualdad triangular `d(x, z) ≤ d(x, y) + d(y, z)`.

**Distancia de Mahalanobis.** Con `Σ` la matriz de [[covarianza-y-correlacion|covarianza]]
de las variables (que debe ser invertible):

:::formula
d_M(x, y) = √( (x − y)ᵀ Σ⁻¹ (x − y) )
:::

- `Σ⁻¹` — inversa de la matriz de covarianza. Deshace la escala y la correlación.
- Si `Σ = I` (varianzas 1 y sin correlación), Mahalanobis coincide con la euclídea.
- Si `Σ` es diagonal, equivale a estandarizar cada variable y usar L2.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `‖x‖ₚ` | La norma `p` de un vector: su tamaño | las del vector | mide siempre lo mismo (el tamaño), pero **cuánto** mide depende de `p`: con `(3, 4)` da 7, 5 y 4 según la norma |
| `p` | El exponente de la norma | real ≥ 1 | con `p = 1` es la suma de valores absolutos (Manhattan), con `p = 2` la euclídea y al crecer se acerca al máximo de las componentes. Con `p < 1` deja de ser norma porque incumple la desigualdad triangular |
| `xᵢ` | La componente `i` del vector | las de la variable `i` | en L1 cada componente suma lo suyo; en L2 una sola componente grande domina la medida |
| `x − y` | El vector diferencia entre dos puntos | las de las variables | es la materia prima de la distancia: se mide la norma de este vector, no la de los puntos por separado |
| `d(x, y)` | La distancia entre dos puntos | las de las variables | para ser una **métrica** debe cumplir simetría y desigualdad triangular; L1, L2 y L∞ la cumplen, `cos θ` no |
| `Σ` | La matriz de covarianza de las variables | las de las variables, al cuadrado | si crece la varianza de una variable, esa dirección pesa menos en la distancia de Mahalanobis; si crece la correlación, la pauta diagonal se estrecha |
| `Σ⁻¹` | La inversa de la covarianza | 1/unidades al cuadrado | existe solo si `Σ` es invertible: con más variables que observaciones o con una columna duplicada no hay distancia de Mahalanobis que calcular |
| `d_M(x, y)` | La distancia de Mahalanobis | las de las variables | con `Σ = I` coincide con la euclídea; con correlación alta castiga salirse de la pauta y premia moverse en la dirección en que las variables van juntas |
:::

**Otras.** La **distancia del coseno** `1 − cos θ` se usa con [[producto-punto-y-similitud|vectores de texto]]; y la **distancia de Hamming** (número de posiciones distintas) aparece con variables categóricas.

## Ejemplo

**Las tres normas de un mismo vector.** Con `p = (3, 4)`: `‖p‖₁ = 3 + 4 = 7`,
`‖p‖₂ = √(9 + 16) = 5`, `‖p‖∞ = max(3, 4) = 4`.

**La distancia entre dos puntos.** De `(1, 1)` a `(4, 5)` la diferencia es `(3, 4)`, así que
`d₁ = 7`, `d₂ = 5` y `d∞ = 4`.

**Girar los ejes cambia L1 pero no L2.** Si giras el vector `(3, 4)` cuarenta y cinco grados
obtienes `(−0,7071, 4,9497)`. La norma L2 sigue siendo 5 (las rotaciones conservan las
longitudes) y la L1 pasa a `0,7071 + 4,9497 = 5,6569`. Conclusión: usar L1 en variables cuyas
unidades y ejes son arbitrarios es una decisión, no una neutralidad.

**Mahalanobis frente a Euclídea.** Dos variables con varianza 1 y correlación 0,9 tienen
`Σ = [[1; 0,9], [0,9; 1]]` y `Σ⁻¹ = [[5,2632; −4,7368], [−4,7368; 5,2632]]`. Comparando tres
diferencias respecto al origen:

| diferencia | Euclídea | Mahalanobis |
| --- | --- | --- |
| (1, 0) | 1,000 | 2,294 |
| (0, 1) | 1,000 | 2,294 |
| (1, 1) | 1,414 | 1,026 |

Euclídea dice que `(1, 1)` es el más lejano; Mahalanobis dice que es el **más cercano**,
porque con correlación 0,9 lo normal es que las dos variables se muevan juntas. Aquí no hay
un empate resuelto por la norma: son dos definiciones distintas de «cerca».

## Código

```python verificable
import numpy as np

p = np.array([3.0, 4.0])
print("L1   :", float(np.linalg.norm(p, 1)))       # -> 7.0
print("L2   :", float(np.linalg.norm(p, 2)))       # -> 5.0
print("Linf :", float(np.linalg.norm(p, np.inf)))  # -> 4.0

# Girar los ejes 45 grados conserva L2 (es invariante a rotaciones) pero no L1.
t = np.deg2rad(45)
R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
q = R @ p
print("p rotado:", np.round(q, 4).tolist())                  # -> [-0.7071, 4.9497]
print("L1 rotado:", round(float(np.linalg.norm(q, 1)), 4))   # -> 5.6569
print("L2 rotado:", round(float(np.linalg.norm(q, 2)), 4))   # -> 5.0
```

:::claves
- En `np.linalg.norm(p, 1)` el segundo argumento es el **orden** de la norma, no un eje: `norm(p)` es la L2, `norm(p, 1)` la suma de valores absolutos y `norm(p, np.inf)` el máximo. Escribir `axis=` ahí no significa lo mismo.
- `R @ p` (matriz por vector) devuelve un array de forma `(2,)`. Si lo escribes al revés, `p @ R`, **no salta ningún error**: NumPy trata el vector 1D como fila y el resultado es la rotación por el ángulo contrario, `Rᵀp`, que tiene toda la pinta de ser correcto. Cuando algo «se gira al revés», mira el orden.
- `np.deg2rad(45)` convierte a radianes porque `np.cos` y `np.sin` esperan radianes: pasarle `45` a secas calcula el coseno de 45 radianes. Además `cos(45°)` es 0,70710678…, que no se guarda exacto, así que `R @ p` conserva la norma solo hasta el error de redondeo (≈ 1e-16); por eso el código redondea antes de imprimir.
- `np.round(q, 4).tolist()` devuelve una lista de Python, pero `q` sigue siendo un array de `float64`. Redondear para imprimir no cambia los datos; redondear y seguir calculando sí acumula error.
- L2 es invariante a rotaciones y L1 no: el mismo vector da 5 con `norm(q, 2)` y 5,6569 con `norm(q, 1)`. Cambiar un solo número en esa línea enseña por qué elegir norma es una decisión de modelado y no un detalle.
- `q = R @ p` crea un array **nuevo**: la rotación no modifica `p`. En cambio `p *= 2` sí cambia `p` en el sitio, y si ese mismo `p` se usa más abajo con su valor original, el resultado deja de tener sentido.
:::

```python verificable
import numpy as np

# Dos variables con varianza 1 y correlacion 0,9: covarianza escrita a mano.
S = np.array([[1.0, 0.9], [0.9, 1.0]])
S_inv = np.linalg.inv(S)
dif = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])   # diferencias respecto al origen

euclidea = np.linalg.norm(dif, axis=1)
maha = np.sqrt(np.einsum("ij,jk,ik->i", dif, S_inv, dif))

print("S inversa:", np.round(S_inv, 4).tolist())      # -> [[5.2632, -4.7368], [-4.7368, 5.2632]]
print("euclidea :", np.round(euclidea, 3).tolist())   # -> [1.0, 1.0, 1.414]
print("Mahalanobis:", np.round(maha, 3).tolist())     # -> [2.294, 2.294, 1.026]
print("mas cercano euclidea:", int(np.argmin(euclidea)))       # -> 0
print("mas cercano Mahalanobis:", int(np.argmin(maha)))        # -> 2
```

## Errores típicos

- **Usar la distancia euclídea con variables en unidades distintas.** Los gramos aplastan a los centímetros y el resultado lo decide una sola variable. Estandariza antes o usa Mahalanobis.
- **Sumar diferencias de variables correlacionadas como si fueran independientes.** L1 y L2 tratan los ejes como ortogonales; `Σ⁻¹` corrige precisamente eso. En el ejemplo, el punto `(1, 1)` pasa de ser el más lejano al más cercano.
- **Suponer que L1 y L2 dan el mismo vecindario.** En distancias cortas se parecen, pero en cuanto hay muchas coordenadas pequeñas L1 acumula y L2 no: el vecino más cercano puede cambiar y con él toda la predicción de un [[knn|KNN]].
- **Confundir norma con distancia.** La norma mide el tamaño de un vector respecto al origen; la distancia entre dos puntos es la norma de su **diferencia**. Es un error de una palabra que cambia todos los números.
- **Usar el coseno como distancia sin transformarlo.** `cos θ` vale entre −1 y 1 y no cumple la desigualdad triangular; si necesitas una métrica, usa `1 − cos θ`.
- **Aplicar Mahalanobis sin comprobar que `Σ` es invertible y estable.** Con menos observaciones que variables, o con variables duplicadas, `Σ` es singular; y con outliers, la covarianza estimada se dispara y la distancia deja de medir lo que crees. La distancia también hereda la maldición de la dimensionalidad: al añadir variables, todas las distancias relativas se parecen cada vez más (ver [[knn|K vecinos más cercanos]]).

:::practica
enunciado: Desde el origen, ¿qué punto está más cerca: B = (4, 3) o C = (5, 0)? Responde con L1, con L2 y con L∞ y comprueba si las tres coinciden.
pista: Con L1 sumas valores absolutos, con L2 la raíz de la suma de cuadrados y con L∞ te quedas con la coordenada mayor.
solucion: B = (4, 3): L1 = 4 + 3 = 7; L2 = √(16 + 9) = 5; L∞ = max(4, 3) = 4. C = (5, 0): L1 = 5 + 0 = 5; L2 = √25 = 5; L∞ = max(5, 0) = 5. En L2 hay empate a 5, en L1 gana C (5 frente a 7) y en L∞ gana B (4 frente a 5). La misma pregunta da dos ganadores distintos según la norma: elegir distancia es decidir qué significa «cerca».
:::

## Comprueba que lo sabes

:::quiz
p: Con Σ = [[1; 0,9], [0,9; 1]], ¿qué diferencia está más lejos del origen en distancia de Mahalanobis?
o: (1, 1), porque su distancia euclídea es la mayor
o: (1, 0), porque salirse de una pauta en la que las dos variables se mueven juntas es lo más improbable
o: Las tres están a la misma distancia de Mahalanobis
a: 2
e: Con correlación 0,9 lo esperable es que las dos variables suban a la vez, así que (1, 1) es lo menos sorprendente (d ≈ 1,03) y (1, 0) o (0, 1) lo más raro (d ≈ 2,29), justo al revés que en Euclídea. Este cálculo exige que Σ sea invertible.
:::

:::quiz
p: ¿Qué diferencia hay entre L1 y L2 para una diferencia de (3, 4)?
o: L1 = 7 y L2 = 5; L1 crece de forma lineal con cada coordenada y L2 castiga más las diferencias grandes
o: L1 = 5 y L2 = 7; L2 es más robusta frente a valores extremos
o: Las dos valen 7, porque ambas son normas
a: 1
e: L1 suma los valores absolutos (3 + 4 = 7) y L2 es la raíz de la suma de cuadrados (√25 = 5). Al elevar al cuadrado, L2 hace que una sola coordenada enorme domine la medida; por eso L1 es la opción robusta y L2 la sensible.
:::

:::trampa
Si tus distancias no discriminan (los vecinos más cercanos y más lejanos están casi a la misma
distancia), el problema casi nunca es la fórmula: es que tienes demasiadas variables
irrelevantes con la misma escala. Antes de cambiar de métrica, estandariza, elimina ruido y
mira cuántas dimensiones usas de verdad.
:::
