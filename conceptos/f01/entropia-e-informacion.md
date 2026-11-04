---
id: entropia-e-informacion
titulo: Entropía e información
fase: 1
nivel: avanzado
rutas: [ds, alg]
prerequisitos: [distribuciones-discretas, valor-esperado, maxima-verosimilitud]
tags: [informacion, entropia, machine-learning]
resumen: Entropía, entropía cruzada, divergencia KL e información mutua: la moneda con la que se mide la incertidumbre y se entrena casi todo el machine learning.
fuentes: ["Cover y Thomas (2006), 'Elements of Information Theory'", "MacKay (2003), 'Information Theory, Inference, and Learning Algorithms'"]
---

## En una frase

La entropía mide en bits la sorpresa media de una variable aleatoria, la entropía cruzada mide
lo que cuesta describirla con un modelo equivocado y la información mutua mide cuánto reduce
una variable la incertidumbre sobre otra.

## La idea

Un mensaje que te cuenta algo que ya sabías no aporta información. «Mañana sale el sol» no vale
nada; «mañana hay un eclipse» vale mucho. La información es **sorpresa**, y la sorpresa de un
suceso se mide como `−log₂(p)`: si `p = 1/2` son 1 bit, si `p = 1/8` son 3 bits y si `p = 1`
son 0 bits. La **entropía** es el promedio de esa sorpresa, ponderado por la frecuencia de cada
suceso.

Esa definición no es arbitraria: la entropía es el mínimo número medio de preguntas de sí o no
que necesitas para identificar el resultado, y también el límite teórico de compresión. Una
moneda justa tiene 1 bit de entropía (una pregunta: ¿ha salido cara?); un dado de seis caras
tiene `log₂ 6 = 2,585` bits; una variable uniforme sobre 8 valores tiene 3 bits exactos.

Cuando el modelo no es el correcto aparece la **entropía cruzada**. Si los datos vienen de una
distribución `p` y tú los codificas con un código optimizado para `q`, gastas de media
`H(p) + KL(p‖q)` bits: la entropía de los datos más un sobrecoste por usar el modelo
equivocado. Ese sobrecoste es la **divergencia KL**, que nunca es negativa y solo vale cero
cuando `p` y `q` coinciden.

Esto no es teoría abstracta: es literalmente la función de pérdida de un clasificador. Con una
etiqueta correcta `y` y una probabilidad predicha `q(y)`, la pérdida es `−log q(y)`. Fíjate en
lo que implica: acertar con una probabilidad de 0,99 cuesta 0,0145 bits, dudar cuesta 1 bit y
equivocarse con confianza (predecir 0,01 para la clase correcta) cuesta 6,64 bits. El castigo
por la confianza mal puesta es enorme, y eso es una virtud: empuja al modelo a estar **bien
calibrado**, no solo a acertar.

La **información mutua** cierra el círculo: mide cuánta incertidumbre sobre `Y` desaparece al
conocer `X`. Es cero si y solo si las variables son independientes, lo que la hace más potente
que la correlación, que solo detecta relación lineal. Se usa para seleccionar variables, para
evaluar agrupamientos y para entender cuánta información comparten dos señales.

Dos avisos antes de bajarla al detalle. La entropía **no** mide dispersión: depende solo de las
probabilidades, no de la distancia entre los valores. Una variable que vale 0 o 1 con
probabilidad 1/2 y otra que vale 0 o 1.000 con probabilidad 1/2 tienen la misma entropía: 1 bit.
Y la divergencia KL **no es una distancia**: no es simétrica y no cumple la desigualdad
triangular, así que `KL(p‖q)` y `KL(q‖p)` son dos cantidades distintas con significados
distintos.

## Definición formal

Con `log₂` los resultados van en **bits**; con logaritmo neperiano, en **nats** (1 nat = 1,4427
bits). La convención `0 · log 0 = 0` es necesaria porque `p log p → 0`.

- **Entropía** de una variable discreta `X` con masa `p(x)`:
  `H(X) = −Σₓ p(x)·log₂ p(x)`. Cumple `0 ≤ H(X) ≤ log₂ k`, donde `k` es el número de valores
  con probabilidad positiva. El máximo se alcanza en la uniforme y el mínimo cuando un valor
  tiene probabilidad 1.
- **Entropía conjunta y condicional:** `H(X, Y) = −Σ p(x, y)·log₂ p(x, y)` y
  `H(Y|X) = H(X, Y) − H(X)`. Regla de la cadena: `H(X, Y) = H(X) + H(Y|X)`.
- **Entropía cruzada:** `H(p, q) = −Σₓ p(x)·log₂ q(x) = H(p) + KL(p‖q)`. Es la pérdida que se
  minimiza al entrenar un clasificador.
- **Divergencia KL:** `KL(p‖q) = Σₓ p(x)·log₂ (p(x)/q(x)) ≥ 0`, con igualdad si y solo si
  `p = q`. Vale `+∞` si existe algún `x` con `p(x) > 0` y `q(x) = 0`.
- **Información mutua:** `I(X; Y) = KL(p(x, y) ‖ p(x)·p(y)) = H(X) + H(Y) − H(X, Y)`. Es cero
  si y solo si `X` e `Y` son independientes, capta cualquier tipo de dependencia y es simétrica.
- **Entropía diferencial** (caso continuo): `h(X) = −∫ f(x)·log₂ f(x) dx`. A diferencia de la
  discreta, **puede ser negativa** y cambia con las unidades: una uniforme en `[0; 0,5]` tiene
  `h = −1` bit.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p(x)` | La probabilidad de cada valor según los datos | adimensional, suma 1 | Al concentrarse en pocos valores, `H(p)` baja: el máximo es `log₂ k` con `k` valores equiprobables |
| `q(x)` | La probabilidad que asigna el modelo | adimensional, suma 1 | No cambia `H(p)`; solo mueve el sobrecoste `KL(p‖q)`, que es 0 cuando `q = p` |
| `H(p)` | La entropía de los datos: la sorpresa media | bits (o nats) | Es el suelo de la pérdida: ningún modelo puede bajar de ahí |
| `H(p, q)` | La entropía cruzada: `H(p) + KL(p‖q)` | bits (o nats) | Coincide con `H(p)` solo si el modelo es perfecto; es la pérdida que se minimiza al entrenar |
| `KL(p‖q)` | El sobrecoste de codificar con `q` lo que viene de `p` | bits (o nats) | Nunca es negativa; vale `+∞` si el modelo da probabilidad 0 a algo que ocurre |
| `I(X; Y)` | La información mutua: lo que saber `X` reduce la incertidumbre sobre `Y` | bits (o nats) | Sube con cualquier dependencia, lineal o no; vale 0 si y solo si son independientes |
| `k` | Número de valores con probabilidad positiva | valores | La entropía máxima sube como `log₂ k`: pasar de 8 a 16 valores solo añade 1 bit |
| `base` | Base del logaritmo: 2 para bits, `e` para nats | — | Cambia la unidad, no la información: 1 nat equivale a 1,4427 bits |
:::

:::figura
fichero: entropia-bits-y-kl-no-simetrica
pie: A la izquierda, la entropía de una moneda según su sesgo: máxima en `p = 0,5` con 1 bit y casi nula cuando el resultado es predecible, porque la entropía mide sorpresa y no número de resultados. A la derecha, dos distribuciones que se parecen mucho: la KL en un sentido vale 0,1398 bits y en el contrario 0,1573. Esa diferencia es la prueba de que la KL no es una distancia y de que el orden de los argumentos cambia el resultado.
fuente: figuras/entropia-e-informacion-1.py
:::

## Ejemplo

**Moneda sesgada.** Justa: `H = 1` bit. Con `p = 0,9` de caras: `H = 0,4690` bits. Con
`p = 0,99`: `H = 0,0808` bits. Cuanto más predecible, menos información aporta cada tirada, y
en el límite (`p = 1`) la entropía es cero.

**Entropía cruzada con un modelo plano.** La distribución real es `p = (0,7; 0,3)` y el modelo
`q = (0,5; 0,5)`. Entonces `H(p) = 0,8813` bits y `KL(p‖q) = 0,1187` bits, así que
`H(p, q) = 0,8813 + 0,1187 = 1,0000` bits exactos (el modelo plano siempre cuesta `log₂ 2 = 1`
bit). En la otra dirección, `KL(q‖p) = 0,1258`, distinto: la KL no es simétrica.

**Coste de una predicción.** Con la clase correcta: predecir 0,99 cuesta 0,0145 bits, predecir
0,5 cuesta 1,0000 bit y predecir 0,01 cuesta 6,6439 bits. La diferencia entre acertar con
seguridad y equivocarse con seguridad es de casi 6,6 bits por observación: por eso la entropía
cruzada domina el entrenamiento de clasificadores.

**Información mutua.** Tabla conjunta de dos sucesos: llueve (sí o no) y llevas paraguas (sí o
no), con probabilidades `[[0,40; 0,05]; [0,10; 0,45]]`. Las marginales son `P(llueve) = 0,45` y
`P(paraguas) = 0,50`, `H(llueve) = 0,9928`, `H(paraguas) = 1,0000` y la información mutua es
0,3973 bits. Con la fórmula `H(X) + H(Y) − I = 1,5955 = H(X, Y)`, todo cuadra.

**Entropía máxima.** Con 8 resultados equiprobables, `H = 3,0000` bits exactos, el máximo
posible para 8 valores. Si alguno tuviera más probabilidad que otro, la entropía bajaría.

## Código

```python verificable
import numpy as np
from scipy import stats

# Moneda sesgada: la entropia es la sorpresa media, en bits.
for p in (0.5, 0.9, 0.99):
    print(f"moneda p={p:<5} H = {stats.entropy([p, 1 - p], base=2):.4f} bits")

# scipy.stats.entropy(p, q) devuelve la divergencia KL; la cruzada es H(p) + KL(p; q).
p = np.array([0.7, 0.3])     # distribucion real
q = np.array([0.5, 0.5])     # modelo, plano
print(f"H(p)    = {stats.entropy(p, base=2):.4f}")                                # -> 0.8813
print(f"KL(p;q) = {stats.entropy(p, q, base=2):.4f}")                            # -> 0.1187
print(f"CE(p;q) = {stats.entropy(p, base=2) + stats.entropy(p, q, base=2):.4f}")  # -> 1.0000
print(f"KL(q;p) = {stats.entropy(q, p, base=2):.4f}")                            # -> 0.1258
```

:::claves
- `stats.entropy(p)` con un solo argumento calcula la entropía `H(p)`; con dos, `stats.entropy(p, q)` calcula la **divergencia KL**, no la entropía cruzada. La cruzada hay que sumarla a mano: `H(p) + KL(p‖q)`. Es la confusión más habitual porque el nombre de la función sugiere lo contrario, y el resultado (0,1187 frente a 1,0000) tiene el mismo aspecto de número razonable.
- El orden de los argumentos importa y no da error: `stats.entropy(p, q)` da 0,1187 y `stats.entropy(q, p)` da 0,1258. Si intercambias las variables del modelo y de los datos, la pérdida cambia sin ningún aviso.
- `stats.entropy(p, base=2)` devuelve bits; sin `base`, devuelve nats. La misma distribución da 0,8813 en bits y 0,6108 en nats, y ninguna de las dos es incorrecta: mezclarlas al comparar dos modelos sí lo es.
- `stats.entropy` normaliza por defecto: si le pasas conteos como `[7, 3]` los divide entre su suma y calcula la entropía de `[0,7; 0,3]`. Cómodo para histogramas, peligroso si creías que estaba sumando logaritmos de los valores originales.
- `stats.entropy([0.5, 0.5], [1.0, 0.0], base=2)` devuelve `inf`, no un error. El modelo da probabilidad cero a algo que ocurre, y por eso la pérdida se va al infinito: es el motivo real del suavizado de etiquetas en un clasificador.
- La entropía no distingue valores: `stats.entropy([0.5, 0.5], base=2)` vale 1 bit tanto si los dos resultados son 0 y 1 como si son 0 y 1.000. La varianza de esos dos casos es incomparable, así que entropía y dispersión no miden lo mismo.
:::

```python verificable
import numpy as np
from scipy import stats

# Tabla conjunta: filas llueve (si, no), columnas paraguas (si, no).
conjunta = np.array([[0.40, 0.05],
                     [0.10, 0.45]])
px = conjunta.sum(axis=1, keepdims=True)
py = conjunta.sum(axis=0, keepdims=True)
mi = (conjunta * np.log2(conjunta / (px * py))).sum()

print(f"P(llueve) = {px[0, 0]:.2f}  P(paraguas) = {py[0, 0]:.2f}")   # -> P(llueve) = 0.45  P(paraguas) = 0.50
print(f"informacion mutua = {mi:.4f} bits")                          # -> 0.3973 bits

hx = -(conjunta.sum(axis=1) * np.log2(conjunta.sum(axis=1))).sum()
hy = -(conjunta.sum(axis=0) * np.log2(conjunta.sum(axis=0))).sum()
print(f"H(X) = {hx:.4f}  H(Y) = {hy:.4f}")                           # -> H(X) = 0.9928  H(Y) = 1.0000
print(f"H(X) + H(Y) - MI = {hx + hy - mi:.4f}")                      # -> 1.5955

# La entropia maxima con 8 resultados posibles es log2(8) = 3 bits.
print(f"uniforme 8 simbolos = {stats.entropy(np.full(8, 1 / 8), base=2):.4f} bits")  # -> 3.0000 bits
```

```python verificable
import numpy as np

# Entropia cruzada de una etiqueta correcta segun la probabilidad que le asigna el modelo.
for q in (0.99, 0.5, 0.01):
    print(f"q(correcta) = {q:<5} coste = {-np.log2(q):.4f} bits")

# Si el modelo da probabilidad cero a algo que ocurre, la KL es infinita.
from scipy import stats
print(f"KL con soporte imposible = {stats.entropy([0.5, 0.5], [1.0, 0.0], base=2)}")  # -> inf
```

## Errores típicos

- **Confundir entropía con dispersión.** La entropía depende solo de las probabilidades, no de
  las distancias entre valores: una variable que toma 0 o 1 y otra que toma 0 o 1.000, ambas
  con probabilidad 1/2, tienen 1 bit cada una. La varianza, en cambio, es enorme en la segunda.
- **Mezclar bits y nats.** La misma distribución da 0,8813 en bits y 0,6108 en nats. Las
  pérdidas de las redes neuronales se publican casi siempre en nats y las comparaciones entre
  frameworks se tuercen cuando se mezclan. Di siempre la base.
- **Tratar la KL como una distancia.** No es simétrica (`0,1187` frente a `0,1258` en el
  ejemplo) y no cumple la desigualdad triangular. Las dos direcciones no son intercambiables:
  `KL(p‖q)` castiga que `q` se estire donde `p` tiene masa y es la que aparece en máxima
  verosimilitud.
- **Dar por bueno un modelo que asigna probabilidad cero.** Si `q(x) = 0` donde `p(x) > 0`, la
  KL es infinita y la entropía cruzada se va al infinito con una sola observación. Por eso en
  la práctica se suavizan las probabilidades (`label smoothing`, `epsilon` en los logaritmos).
- **Estimar la información mutua con pocas muestras.** El estimador está sesgado al alza: con
  pocos datos parece haber dependencia donde no la hay. Si comparas variables medidas con
  tamaños distintos, el sesgo decide el ranking.
- **Creer que minimizar la entropía cruzada es lo mismo que maximizar la exactitud.** Dos
  modelos con la misma exactitud pueden tener entropías cruzadas muy distintas: la pérdida
  premia la calibración, y un modelo con razón 60/40 para todos los casos acierta lo mismo que
  uno que acierta con 0,99 cuando está seguro y se equivoca con 0,6 cuando duda.

:::practica
enunciado: Un clasificador de tres clases tiene distribución real p = (0,5; 0,3; 0,2) y un modelo q = (0,4; 0,4; 0,2). Con log₂ 0,4 = 1,3219, log₂ 0,3 = 1,7370 y log₂ 0,2 = 2,3219, calcula H(p), la entropía cruzada y el sobrecoste.
pista: La entropía cruzada es la sorpresa media al codificar con q en lugar de con p, y su diferencia con H(p) es la divergencia KL.
solucion: H(p) = 0,5·1+0,3·1,7370+0,2·2,3219 = 0,5+0,5211+0,4644 = 1,4855 bits. H(p,q) = 0,5·1,3219+0,3·1,3219+0,2·2,3219 = 0,6610+0,3966+0,4644 = 1,5219 bits. KL = 1,5219−1,4855 = 0,0365. Conclusión: el error del modelo cuesta 0,0365 bits por observación y la pérdida nunca baja de 1,4855, la incertidumbre irreducible de las etiquetas.
:::

## Comprueba que lo sabes

:::quiz
p: Una moneda sale cara con probabilidad 0,99. ¿Cuál es su entropía en bits y qué significa?
o: 0,0808 bits: cada tirada aporta muy poca información porque el resultado es casi predecible
o: 0,99 bits, porque es la probabilidad de cara
o: 1 bit, porque sigue habiendo dos resultados posibles
a: 1
e: La entropía es la sorpresa media, no el número de resultados. Con p = 0,99, H = 0,0808 bits: acertar el resultado es tan fácil que cada tirada informa muy poco. Solo cuando p = 0,5 la entropía alcanza su máximo de 1 bit.
:::

:::quiz
p: Un modelo asigna probabilidad 0 a una clase que sí aparece en los datos. ¿Qué pasa con la entropía cruzada?
o: Se queda igual, porque esa observación es poco frecuente
o: Es infinita, porque el coste de esa observación es el logaritmo de cero
o: Baja, porque el modelo es más decidido
a: 2
e: La pérdida de una observación es −log q(clase correcta). Si q = 0, el logaritmo diverge y la pérdida es infinita: ninguna cantidad de aciertos en las demás compensa. Por eso se suavizan las probabilidades y se evita predecir ceros absolutos.
:::

:::quiz
p: ¿Por qué la información mutua detecta dependencias que la correlación no ve?
o: Porque está definida sobre las probabilidades conjuntas y vale cero si y solo si hay independencia, sin suponer linealidad
o: Porque siempre es mayor que la correlación
o: Porque se calcula con logaritmos, que capturan las curvas
a: 1
e: La correlación de Pearson mide asociación lineal: con y = x² es cero aunque la dependencia sea total. La información mutua compara la distribución conjunta con el producto de las marginales, así que cualquier dependencia la hace positiva, sea lineal o no.
:::
