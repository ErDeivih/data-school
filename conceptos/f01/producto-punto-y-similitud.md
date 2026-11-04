---
id: producto-punto-y-similitud
titulo: Producto punto y similitud
fase: 1
nivel: básico
rutas: [core, ds, quant]
prerequisitos: [escalares-vectores-matrices]
tags: [algebra-lineal, similitud, embeddings, proyeccion]
resumen: El producto punto mide cuánto apuntan dos vectores en la misma dirección; normalizado da la similitud del coseno, la base de los embeddings.
fuentes: ["Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval'", "Deisenroth, Faisal y Ong (2020), 'Mathematics for Machine Learning'"]
---

## En una frase

El **producto punto** multiplica dos vectores componente a componente, suma los resultados y
devuelve un solo número: positivo si apuntan en la misma dirección, cero si son
perpendiculares y negativo si van en sentidos opuestos; dividido entre las dos longitudes se
convierte en el **coseno del ángulo**, la medida de parecido que usan los sistemas de
recomendación y los [[embeddings|embeddings]].

## La idea

Imagina que dos personas puntúan las mismas cinco películas del 1 al 5. Ana da
`(5, 4, 1, 2, 4)` y Luis da `(4, 5, 1, 3, 4)`. Los dos vectores apuntan casi en la misma
dirección: les gustan y les disgustan las mismas películas. El producto punto te da un número
que crece cuando las puntuaciones altas coinciden, pero tiene una trampa: si multiplicas el
vector de Luis por 10 (un usuario que puntúa del 10 al 50), el producto se multiplica por 10
sin que la opinión haya cambiado. Por eso se normaliza y se usa el coseno.

:::figura
fichero: producto-punto-coseno-y-proyeccion
pie: El producto punto se lee como la sombra de un vector sobre el otro (aquí, la de `y` sobre `x` cae en (2, 0)) y el coseno es esa sombra dividida entre las dos longitudes. Los dos paneles de la derecha enseñan la trampa que justifica normalizar: al doblar `y`, el producto punto pasa de 6 a 12 mientras el coseno se queda clavado en 0,7071.
fuente: figuras/producto-punto-y-similitud-1.py
:::

La otra lectura del producto punto es la **proyección**: `(x · y) / ‖x‖` dice cuánto de `y`
cae en la dirección de `x`. Es la respuesta a «¿cuánto de esta señal explica aquella
dirección?», y es la misma cuenta que hay detrás de la descomposición de una serie en
componentes, de la ortogonalización y de los coeficientes de una [[regresion-lineal|regresión]]
múltiple.

Y la tercera lectura es la geométrica: el producto punto es la forma más barata de detectar
**ortogonalidad**. Si vale cero, los vectores no comparten nada en esa dirección. En dimensión
alta, además, casi todos los pares de vectores aleatorios son casi ortogonales, y eso explica
por qué las distancias se vuelven poco informativas al añadir variables.

## Definición formal

Para `x, y ∈ ℝⁿ`:

:::formula
x · y = Σᵢ₌₁ⁿ xᵢ · yᵢ = x₁y₁ + x₂y₂ + … + xₙyₙ
:::

- `x, y` — dos vectores con el mismo número de componentes `n`.
- `xᵢ`, `yᵢ` — la componente `i` de cada vector.
- `Σᵢ₌₁ⁿ` — suma de todos los términos desde `i = 1` hasta `i = n`.
- El resultado es un **escalar**, no un vector.

:::formula
x · y = ‖x‖ · ‖y‖ · cos θ      ⇔      cos θ = (x · y) / (‖x‖ · ‖y‖)
:::

- `‖x‖ = √(x · x)` — la **norma euclídea** o longitud del vector.
- `θ` — el ángulo entre los dos vectores, en radianes o grados.
- `cos θ ∈ [−1, 1]` — la **similitud del coseno**. Vale 1 si van en la misma dirección, 0 si
  son perpendiculares y −1 si van en sentidos opuestos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `x`, `y` | Los dos vectores que se comparan | las de la variable que miden (puntuaciones, frecuencias de palabras…) | multiplicar uno por un número positivo no cambia el coseno pero multiplica el producto punto: es la diferencia entre medir dirección y medir tamaño |
| `n` | Número de componentes: la dimensión | entero ≥ 1 | cada componente añade un sumando. En dimensión alta casi todos los cosenos se acercan a 0 y las diferencias entre el más parecido y el menos parecido se estrechan |
| `xᵢ`, `yᵢ` | La componente `i` de cada vector | las de la variable | una sola componente enorme domina el producto punto y puede decidir toda la similitud |
| `Σᵢ₌₁ⁿ` | La suma de los `n` productos | — | es una suma, no un vector: el resultado es un único número |
| `x · y` | El producto punto: un escalar | las de las variables, al cuadrado | positivo si apuntan en la misma dirección, 0 si son perpendiculares, negativo si van en sentido contrario. Crece sin límite al agrandar cualquiera de los dos vectores |
| `‖x‖ = √(x · x)` | La longitud euclídea del vector | las de la variable | con el mismo producto punto, una norma mayor hace bajar el coseno: por eso el documento largo no gana por ser largo |
| `θ` | El ángulo entre los dos vectores | radianes o grados | está entre 0° y 180°; a 90° el producto punto es exactamente cero |
| `cos θ` | La similitud del coseno | adimensional, entre −1 y 1 | no tiene sentido fuera de ese rango (lo garantiza Cauchy-Schwarz). Es la medida que se usa para comparar y `1 − cos θ` la que se usa como distancia |
:::

Propiedades y derivadas:

- **Cauchy-Schwarz:** el valor absoluto de `x · y` nunca supera `‖x‖ · ‖y‖`. Es lo que
  garantiza que `cos θ` no se salga de `[−1, 1]`.
- **Proyección de `y` sobre `x`:** el vector `((x · y) / (x · x)) · x`. Su longitud es
  `(x · y) / ‖x‖`.
- **Distancia del coseno:** `1 − cos θ`. Se usa como distancia porque `cos θ` no cumple la
  desigualdad triangular (ver [[norma-y-distancias|normas y distancias]]).
- **Relación con la correlación:** la [[correlacion-pearson-spearman|correlación de Pearson]]
  es exactamente el coseno entre los vectores **centrados** (restando a cada uno su media). Sin
  centrar, dos vectores con todos los valores positivos dan un coseno alto aunque no tengan
  ninguna relación.

## Ejemplo

Con `x = (1, 2, 2)` e `y = (2, 1, 0)`:

- Producto punto: `1·2 + 2·1 + 2·0 = 2 + 2 + 0 = 4`.
- Normas: `‖x‖ = √(1 + 4 + 4) = √9 = 3`; `‖y‖ = √(4 + 1 + 0) = √5 ≈ 2,2361`.
- Coseno: `4 / (3 · 2,2361) = 4 / 6,7082 ≈ 0,5963`.
- Ángulo: `arccos(0,5963) ≈ 53,4°`. Apuntan en direcciones parecidas, pero no iguales.
- Proyección de `y` sobre `x`: `(4 / 9) · (1, 2, 2) ≈ (0,4444, 0,8889, 0,8889)`. Es la parte
  de `y` que vive en la dirección de `x`.
- Si multiplicas `y` por 10, `y' = (20, 10, 0)`: el producto punto pasa a `40` (diez veces
  más) pero el coseno sigue siendo `0,5963`. La dirección no ha cambiado.
- Ortogonalidad: con `z = (2, −1, 0)`, `x · z = 2 − 2 + 0 = 0`. El ángulo es de 90°.

## Código

```python verificable
import numpy as np

x = np.array([1.0, 2.0, 2.0])
y = np.array([2.0, 1.0, 0.0])

producto = float(x @ y)
cos = producto / (np.linalg.norm(x) * np.linalg.norm(y))

print("producto punto:", producto)                        # -> 4.0
print("normas:", np.round([np.linalg.norm(x), np.linalg.norm(y)], 4).tolist())   # -> [3.0, 2.2361]
print("coseno:", round(cos, 4))                           # -> 0.5963
print("angulo en grados:", round(float(np.degrees(np.arccos(cos))), 1))          # -> 53.4

# Proyeccion de y sobre x: la parte de y que va en la direccion de x.
proyeccion = (producto / float(x @ x)) * x
print("proyeccion:", np.round(proyeccion, 4).tolist())    # -> [0.4444, 0.8889, 0.8889]
```

:::claves
- `x @ y` sobre dos arrays 1D devuelve un **escalar** de NumPy, no un array. Por eso el código lo envuelve en `float(...)`: así se imprime limpio y se comporta como un número de Python.
- `x * y` sería el **producto elemento a elemento** (un vector de tres componentes) y `x @ y` el producto punto (un número). Si esperabas un número y te sale un array, es exactamente esto.
- `np.linalg.norm(x)` calcula la L2 sin construir `x**2` en memoria; `np.linalg.norm(x, 1)` daría la L1 y `norm(x, np.inf)` la del máximo. El segundo argumento es el **orden** de la norma, no un eje.
- `np.round([...], 4)` devuelve un array de NumPy; `.tolist()` lo pasa a listas de Python. Sin el `.tolist()`, el `print` muestra la representación del array (con `array(` y los puntos decimales), no la lista limpia.
- `np.degrees(np.arccos(cos))` funciona en dos pasos: `arccos` devuelve **radianes** y `degrees` convierte a grados. `arccos` solo acepta valores en `[−1, 1]`, así que un coseno con error de redondeo de una milésima da `nan`: recortarlo con `np.clip(cos, -1, 1)` es la defensa habitual.
- `(producto / float(x @ x)) * x` multiplica el vector **entero** por un escalar; ese detalle es lo que convierte la cuenta en un vector (la proyección) y no en un número. `x @ x` es la norma al cuadrado, no la norma: dividir entre `np.linalg.norm(x)` daría la longitud de la proyección, que es otra cosa.
:::

```python verificable
import numpy as np

x = np.array([1.0, 2.0, 2.0])
y = np.array([2.0, 1.0, 0.0])
y10 = 10 * y            # el mismo usuario puntuando en otra escala

cos = float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y)))
cos10 = float(x @ y10 / (np.linalg.norm(x) * np.linalg.norm(y10)))

print("producto con y y con 10y:", float(x @ y), float(x @ y10))   # -> 4.0 40.0
print("coseno con y y con 10y:", round(cos, 4), round(cos10, 4))   # -> 0.5963 0.5963

# Producto punto cero: direcciones perpendiculares.
z = np.array([2.0, -1.0, 0.0])
print("x . z:", float(x @ z))                                      # -> 0.0
```

## Errores típicos

- **Usar el producto punto crudo para comparar vectores de distinta magnitud.** Un documento largo tiene productos punto grandes con todo el mundo. Normaliza, usa el coseno, o aplica antes una [[z-score-y-estandarizacion|estandarización]].
- **Creer que un coseno de 1 significa «idénticos».** `(1, 1)` y `(100, 100)` tienen coseno 1 y magnitudes que no se parecen en nada. El coseno mide dirección, no tamaño.
- **Confundir el producto punto con el producto elemento a elemento.** `x · y` es un escalar (una suma de productos); `x * y` en numpy es otro vector. Si esperabas un número y te sale un array, esto es lo que ha pasado.
- **Tratar el coseno como si fuera una distancia.** La distancia del coseno `1 − cos θ` no cumple la desigualdad triangular: con `u = (1, 0)`, `w = (1, 1)/√2` y `v = (0, 1)`, entre `u` y `v` vale 1, pero las dos etapas `u → w` y `w → v` suman 0,586. Si necesitas una métrica de verdad, usa el ángulo `arccos(cos θ)`.
- **Comparar vectores de palabras sin centrar cuando buscas relación.** Dos textos que solo contienen palabras frecuentes tendrán coseno alto por el simple hecho de compartir el vocabulario común. Restar la media (o ponderar con tf-idf) cambia por completo el resultado.
- **Ignorar la maldición de la dimensionalidad.** En espacios de cientos de dimensiones, vectores aleatorios tienden a ser casi ortogonales entre sí: casi todos los cosenos se apiñan cerca de 0 y las diferencias entre el más parecido y el menos parecido se estrechan. Es la misma advertencia que aparece en [[knn|K vecinos más cercanos]] y en [[tsne-y-umap|t-SNE y UMAP]].

:::practica
enunciado: Marta puntúa tres películas con x = (4, 2, 4) y Pedro con y = (2, 4, 2). Calcula el producto punto y el coseno. ¿Cambia el coseno si Pedro puntúa en escala doble, y = (4, 8, 4)?
pista: El coseno divide el producto punto entre el producto de las normas; fíjate en qué le pasa a cada factor al doblar un vector.
solucion: x · y = 4·2 + 2·4 + 4·2 = 8 + 8 + 8 = 24. Normas: ‖x‖ = √(16 + 4 + 16) = √36 = 6 e ‖y‖ = √(4 + 16 + 4) = √24 ≈ 4,899. Coseno = 24 / (6 · 4,899) = 24 / 29,394 ≈ 0,8165, un ángulo de unos 35,3°. Al doblar y: producto 48 y norma √96 ≈ 9,798, luego 48 / 58,788 ≈ 0,8165. El coseno no cambia: solo mide dirección, no tamaño.
:::

## Comprueba que lo sabes

:::quiz
p: Con x = (1, 2, 2) e y = (2, 1, 0), ¿cuánto valen el producto punto y el coseno?
o: Producto 4 y coseno ≈ 0,5963, porque hay que dividir entre el producto de las normas 3 y 2,2361
o: Producto 4 y coseno 4, porque el producto punto ya es la similitud
o: Producto 8 y coseno ≈ 1,19, que es mayor que 1 porque los vectores no están normalizados
a: 1
e: El producto punto es 1·2 + 2·1 + 2·0 = 4. El coseno divide ese 4 entre el producto de las normas (3 y √5 ≈ 2,2361), y sale 0,5963. Un coseno mayor que 1 es imposible por la desigualdad de Cauchy-Schwarz.
:::

:::quiz
p: ¿Por qué se normaliza el producto punto para medir similitud entre documentos de longitudes distintas?
o: Porque el producto punto sin normalizar crece con la longitud del documento y favorece a los largos
o: Porque el producto punto solo funciona con vectores de norma 1
o: Porque normalizar convierte el producto punto en una probabilidad
a: 1
e: Un vector más largo (un documento con más palabras) tiene productos punto más grandes con todos los demás, así que el ranking se llena de documentos largos. Dividir entre las normas elimina ese efecto. El producto punto está definido para cualquier vector, y el coseno sigue siendo un número entre −1 y 1, no una probabilidad.
:::
