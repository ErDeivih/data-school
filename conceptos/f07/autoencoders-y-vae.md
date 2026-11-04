---
id: autoencoders-y-vae
titulo: Autoencoders y VAE
fase: 7
nivel: avanzado
rutas: [ds]
prerequisitos: [perceptron-y-mlp, pca, funciones-de-perdida, optimizadores, deteccion-de-anomalias]
tags: [latente, compresion, generativo, anomalias]
resumen: Comprimir la entrada en un cuello de botella y reconstruirla: sirve para reducir dimensión, detectar anomalías y, con un VAE, generar muestras nuevas.
fuentes: ["Bourlard y Kamp (1988), 'Auto-association by Multilayer Perceptrons and Singular Value Decomposition'", "Kingma y Welling (2014), 'Auto-Encoding Variational Bayes'", "Hinton y Salakhutdinov (2006), 'Reducing the Dimensionality of Data with Neural Networks'"]
---

## En una frase

Un autoencoder es una red que aprende a copiar su entrada pasando por un cuello de botella
estrecho: si consigue reconstruirla bien, es que ese cuello de botella ha conservado lo
esencial, y ese resumen comprimido sirve para reducir dimensión, detectar rarezas o generar
datos nuevos.

## La idea

Imagina que tienes que resumir un libro en una sola página y luego reconstruir el libro a partir
de esa página. Si lo consigues, la página contiene lo esencial. Si no, o el resumen era
demasiado corto o no supiste elegir qué guardar. Un autoencoder es ese ejercicio,
hecho con números y entrenado por descenso de gradiente.

La estructura son dos redes en espejo:

- El **codificador** lleva la entrada (por ejemplo, 784 píxeles de un dígito escrito a mano) a un
  vector corto, de 32 números. Ese vector es el **código latente** `z`.
- El **decodificador** hace el camino inverso: recibe `z` y produce una reconstrucción de 784
  píxeles.

Se entrena para que la reconstrucción se parezca a la entrada. No hay etiquetas: es aprendizaje
autosupervisado, la respuesta es la propia pregunta. Y el cuello de botella es lo que obliga a
que el código sea útil: si le das 784 dimensiones latentes, la red aprende a copiar sin comprimir
nada y no has conseguido nada.

Lo interesante es **qué** acaba guardando el cuello de botella. Si la entrada son dígitos
escritos a mano, no guarda los píxeles: guarda el trazo, la inclinación, el grosor, la curva del
«3». Es decir, descubre por su cuenta los factores que varían en los datos. Eso conecta con
[[pca]]: si el codificador y el decodificador son lineales y el error es cuadrático, el
autoencoder aprende el mismo subespacio que PCA. La ventaja del autoencoder es que
con capas no lineales puede aprender variedades curvas que PCA no ve.

Tres usos concretos, y son usos distintos:

1. **Reducción de dimensión y representación.** El código latente alimenta un clasificador, un
   buscador de similitud o una visualización. Es una alternativa no lineal a PCA.
2. **Detección de anomalías.** Un autoencoder entrenado solo con datos normales reconstruye bien
   lo normal y mal lo raro. El **error de reconstrucción** es la puntuación de anomalía. Es la
   aplicación más útil y la más fácil de hacer mal (ver los errores típicos).
3. **Generación.** Aquí el autoencoder normal no sirve: su espacio latente no tiene estructura, y
   coger un punto al azar entre dos códigos aprendidos suele producir basura. El **VAE**
   (*variational autoencoder*) resuelve eso obligando a que los códigos sigan una distribución
   conocida, normalmente una normal estándar.

El VAE cambia una cosa pequeña con consecuencias grandes: en vez de asignar a cada entrada un
punto `z`, el codificador emite los parámetros de una distribución —una media y una varianza por
dimensión— y se **muestrea** `z` de ella. Para que el muestreo no rompa el descenso de gradiente
se usa el truco de la reparametrización: `z = μ + σ ⊙ ε`, con `ε` ruido normal. Así `z` es una
función determinista y derivable de `μ` y `σ`, y el ruido entra por fuera. A la pérdida se le
suma un término que empuja esas distribuciones hacia la normal estándar: es el término `KL`. El
resultado es un espacio latente continuo y relleno, donde moverse un poco cambia la salida un
poco, que es lo que hace falta para generar.

:::figura
fichero: autoencoders-y-vae-latente-y-anomalia
pie: El panel de la izquierda es la decisión de diseño del autoencoder: cuántas dimensiones latentes necesitas. Las dos curvas caen y luego se estancan en una línea roja que es el ruido de los datos. Ese estancamiento es la información útil: a partir de ahí, cada dimensión extra no resume nada, solo memoriza ruido, y un cuello de botella demasiado ancho (sobrecompleto) acaba copiando la entrada. Fíjate además en que la curva morada llega antes al suelo: con una variedad curva, seis dimensiones hacen lo mismo que veinte en el caso lineal. El panel derecho enseña el uso práctico más rentable, la detección de anomalías: se entrena solo con datos normales, se mide el error de reconstrucción y el umbral se fija en un percentil alto de esos normales. La separación no es perfecta y ahí está la lección: hay anomalías por debajo del umbral (se te escapan) y normales por encima (falsas alarmas), así que el umbral se elige por el coste de cada error, no por el porcentaje que te gustaría detectar.
fuente: figuras/autoencoders-y-vae-1.py
:::

## Definición formal

Un autoencoder son dos funciones parametrizadas y una pérdida:

:::formula
z = f_θ(x) ,  x̂ = g_φ(z) ,  L(x, x̂) = ‖x − x̂‖²
:::

- `x ∈ ℝ^d` — la entrada. `d` es el número de características (784 píxeles, 300 variables...).
- `f_θ` — el codificador, con parámetros `θ`. Devuelve el código latente.
- `z ∈ ℝ^k` — el código latente. `k` es la dimensión del cuello de botella.
- `g_φ` — el decodificador, con parámetros `φ`.
- `x̂` — la reconstrucción, de la misma forma que `x`.
- `L` — la pérdida. Es el error cuadrático medio, o entropía cruzada binaria si los píxeles
  están en [0, 1] (ver [[funciones-de-perdida|funciones de pérdida]]).
- **Infracompleto** si `k < d` (comprime de verdad) y **sobrecompleto** si `k ≥ d` (puede copiar).
  Un autoencoder sobrecompleto sin regularización aprende la identidad y no sirve para nada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `d` | Número de características de la entrada (píxeles, variables) | características | Con el mismo `k`, el cuello de botella comprime más: el error de reconstrucción sube, porque hay más que resumir con el mismo presupuesto |
| `k` | Dimensión del código latente, lo ancho que es el cuello de botella | dimensiones | El error baja y se estanca en el ruido de los datos. A partir de ahí deja de ganar y, si `k ≥ d` sin regularizar, memoriza la entrada y el código deja de resumir |
| `x` | La entrada de una observación | las de las características | No es un parámetro que se mueva: es el dato. Cambiarlo cambia `z` y `x̂` para esa fila |
| `θ` | Pesos del codificador | adimensionales | Más capacidad para comprimir: baja el error de entrenamiento, pero también la garantía de que el latente se generalice a datos no vistos |
| `φ` | Pesos del decodificador | adimensionales | Un decodificador más potente reconstruye mejor y puede llegar a ignorar `z`: es el camino al colapso del posterior en un VAE |
| `L` | Pérdida de reconstrucción (error cuadrático medio) | las de `x` al cuadrado | Es lo que se minimiza. Cuanto más baja, mejor reconstruye; pero un valor bajo en entrenamiento no dice nada sobre datos nuevos |
:::

**Equivalencia con PCA.** Si `f` y `g` son lineales y `L` es el error cuadrático, el óptimo
proyecta sobre el subespacio de las `k` primeras componentes principales. La varianza que se
pierde es la suma de los `d − k` autovalores descartados de la matriz de covarianza,
y coincide con el error de reconstrucción esperado.

**VAE.** El codificador emite `μ(x)` y `log σ²(x)` (se usa el logaritmo por estabilidad
numérica: la varianza debe ser positiva). El muestreo se hace con el truco de la
reparametrización:

:::formula
z = μ + σ ⊙ ε ,  ε ∼ N(0, I)
:::

- `μ` — vector de medias, de tamaño `k`.
- `σ = exp(log σ² / 2)` — vector de desviaciones típicas, positivo por construcción.
- `ε` — ruido normal estándar, del mismo tamaño que `z`. Es la única fuente de azar.
- `⊙` — producto elemento a elemento.

La pérdida del VAE suma reconstrucción y regularización, con `β` el peso del segundo término
(`β = 1` en el VAE original):

:::formula
L = reconstrucción + β · D_KL ,  D_KL = ½ Σⱼ ( μⱼ² + σⱼ² − 1 − log σⱼ² )
:::

- `D_KL` — divergencia de Kullback-Leibler entre la distribución que emite el codificador para
  esa entrada y la normal estándar `N(0, I)`. Mide cuánto se aparta.
- La suma recorre las `k` dimensiones latentes.
- El término vale 0 cuando `μⱼ = 0` y `σⱼ = 1` en todas las dimensiones, y crece al alejarse la
  media del origen o al desviarse la varianza de 1.
- `β` — cuánto pesa la regularización frente a la reconstrucción. Valores altos dan un latente más
  ordenado y reconstrucciones peores (**β-VAE**).

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `μ` | Media que el codificador da al código latente de cada entrada | las del espacio latente | El término `μ²` de la `KL` crece al cuadrado: alejarse del origen cuesta cada vez más y el latente se aprieta alrededor de cero |
| `log σ²` | Logaritmo de la varianza del código latente; se usa el logaritmo para que la varianza sea positiva | adimensional | Por debajo de 0 la `KL` sube y el codificador deja de «aparcar» cada entrada en un punto; por encima de 0 también sube, porque se reparte más de la cuenta |
| `σ` | Desviación típica del código, `exp(log σ² / 2)` | las del espacio latente | Es el tamaño del ruido que se muestrea: más `σ`, códigos más dispersos y reconstrucciones menos fieles |
| `ε` | Ruido normal estándar del truco de la reparametrización | adimensional | No es un parámetro del modelo: es la única fuente de azar. Cambiarlo cambia la muestra generada, no los pesos |
| `β` | Cuánto pesa la `KL` frente a la reconstrucción (`β = 1` en el VAE original) | adimensional | El latente queda más ordenado y continuo, pero la reconstrucción empeora: con `β` muy alto el decodificador deja de mirar `z` (colapso del posterior) |
| `D_KL` | Divergencia entre la distribución que el codificador da a esa entrada y la normal estándar | adimensional (nats) | Mide cuánto se aparta el latente de la normal: si sube, el espacio latente está menos relleno y muestrear puntos intermedios da peores resultados |
| `k` | Número de dimensiones latentes sobre las que se suma la `KL` | dimensiones | La `KL` total es una suma: con más dimensiones hay más términos que empujar hacia la normal estándar |
:::

**Puntuación de anomalía.** Con un autoencoder entrenado solo con datos normales, la puntuación
de una observación nueva es `s(x) = ‖x − x̂‖²`. El umbral no se inventa: se fija en un percentil
alto (por ejemplo el p99) de las puntuaciones de un conjunto de validación **normal**.

## Ejemplo

Diez observaciones con dos variables:

```
(2,5 2,4)  (0,5 0,7)  (2,2 2,9)  (1,9 2,2)  (3,1 3,0)
(2,3 2,7)  (2,0 1,6)  (1,0 1,1)  (1,5 1,6)  (1,1 0,9)
```

La media es (1,81  1,91). Al centrar cada columna restando su media, la primera observación
queda en (0,69  0,49) y la segunda en (−1,31  −1,21).

Las varianzas por componente (con `n − 1` en el denominador, porque estimamos la media) son
**1,284** y **0,0491**, y suman 1,333. La primera componente explica
1,284 / 1,333 = **96,3 %** de la variabilidad.

Comprimir a una sola dimensión y reconstruir da un error cuadrático medio por observación de
**0,0491**, que es **exactamente** la varianza de la segunda componente, la que se ha tirado. No
es casualidad: es la definición de PCA, y un autoencoder lineal entrenado con error cuadrático
llega al mismo sitio.

El término `KL` de un VAE, por dimensión, para varios valores de `μ` y `log σ²`:

| μ | log σ² | σ | D_KL |
| --- | --- | --- | --- |
| 0,0 | 0 | 1,000 | 0,0000 |
| 1,0 | 0 | 1,000 | 0,5000 |
| 2,0 | 0 | 1,000 | 2,0000 |
| 0,0 | −3 | 0,223 | 1,0249 |
| 0,0 | 3 | 4,482 | 8,0428 |

Se lee así: alejar la media del origen cuesta (0,5 por cada unidad al cuadrado, aquí 2,0 con
`μ = 2`), y una varianza muy pequeña también cuesta, porque el codificador está «aparcando» esa
entrada en un punto en vez de repartirla por el espacio latente. Ese castigo es lo que impide el
colapso del posterior y lo que rellena el espacio entre códigos.

## Código

```python verificable
import numpy as np

# Un autoencoder lineal con error cuadratico aprende el mismo subespacio que PCA.
X = np.array([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0],
              [2.3, 2.7], [2.0, 1.6], [1.0, 1.1], [1.5, 1.6], [1.1, 0.9]])
Xc = X - X.mean(axis=0)
n = X.shape[0]
# full_matrices=False porque solo hacen falta los min(n, d) vectores, no la matriz cuadrada
# completa: con 10 filas y 2 columnas, la version completa devolveria una U de 10x10.
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)

varianza = S ** 2 / (n - 1)                      # ddof=1: estimamos la media
print("varianza por componente:", varianza.round(3).tolist())   # -> [1.284, 0.049]
print("1a componente explica  :", round(float(varianza[0] / varianza.sum()), 3))  # -> 0.963

# Cuello de botella de 1 dimension: proyectar y reconstruir.
# Vt[:1] es la primera componente principal, como una fila de 1 x 2. Al proyectar y volver
# se tira la segunda componente, asi que el error esperado es exactamente su varianza.
rec = (Xc @ Vt[:1].T) @ Vt[:1]
error = float(((Xc - rec) ** 2).sum() / (n - 1))
print("error de reconstruccion:", round(error, 4))    # -> 0.0491
print("varianza descartada    :", round(float(varianza[1]), 4))   # -> 0.0491
```

```python verificable
import numpy as np

# Termino KL de un VAE gaussiano: 0.5 * (mu^2 + sigma^2 - 1 - log sigma^2), sumado por dimension.
def kl(mu, log_var):
    # El codificador devuelve log_var, no sigma: exp() lo convierte en la varianza. Se guarda
    # en logaritmo porque asi nunca puede salir negativa y el gradiente no se dispara.
    return float(0.5 * np.sum(mu ** 2 + np.exp(log_var) - 1.0 - log_var))

print("mu=0, log_var= 0:", round(kl(np.array([0.0]), np.array([0.0])), 4))    # -> 0.0
print("mu=1, log_var= 0:", round(kl(np.array([1.0]), np.array([0.0])), 4))    # -> 0.5
print("mu=2, log_var= 0:", round(kl(np.array([2.0]), np.array([0.0])), 4))    # -> 2.0
print("mu=0, log_var=-3:", round(kl(np.array([0.0]), np.array([-3.0])), 4))   # -> 1.0249
print("mu=0, log_var= 3:", round(kl(np.array([0.0]), np.array([3.0])), 4))    # -> 8.0428
print("sigma:", round(float(np.exp(-3.0 / 2)), 3), round(float(np.exp(3.0 / 2)), 3))  # -> 0.223 4.482
```

:::claves
- `np.linalg.svd(Xc, full_matrices=False)` devuelve tres cosas: `U`, los valores singulares `S` y
  `Vt`. `Vt` son las direcciones **por filas** (`Vt[0]` es la primera componente), no por columnas.
  Por eso la proyección se escribe `Xc @ Vt[:1].T`: hay que transponer para multiplicar.
- `X - X.mean(axis=0)` resta la media **de cada columna** porque `axis=0` recorre las filas. Con
  `axis=1` restarías la media de cada observación y el resultado no sería centrar las variables.
- En `varianza = S ** 2 / (n - 1)`, los valores singulares van al cuadrado para ser varianzas, y el
  denominador es `n - 1` porque la media se estima de los propios datos. NumPy usa `ddof=0` en
  `np.var`; aquí se escribe a mano para que coincida con la definición.
- `((Xc - rec) ** 2).sum() / (n - 1)`: el error de reconstrucción se divide entre `n - 1`, no entre
  `n` ni entre el número de elementos. Dividir entre `n` daría 0,0442 y dejaría de coincidir con la
  varianza descartada, que es justo la coincidencia que el ejemplo demuestra.
- `float(...)` alrededor de una reducción de NumPy es lo que deja el número limpio: `round` sobre un
  `np.float64` sigue devolviendo `np.float64`, y en NumPy 2.x su representación es `np.float64(0.963)`
  en vez de `0.963`. Con un array entero `round` no funciona en absoluto: lanza
  `TypeError: type numpy.ndarray doesn't define __round__ method`, así que el `float(...)` no sobra.
- En el VAE, `torch.randn_like(sigma)` genera ruido con la **misma forma** que `sigma`; si usaras una
  constante o un ruido de otra forma, la difusión de la reparametrización dejaría de ser válida y el
  gradiente que llega a `mu` y `sigma` no sería el correcto.
:::

```python ilustrativo
import torch
import torch.nn as nn

class VAE(nn.Module):
    def __init__(self, d=784, k=16):
        super().__init__()
        self.codificador = nn.Sequential(nn.Linear(d, 256), nn.ReLU(), nn.Linear(256, 2 * k))
        self.decodificador = nn.Sequential(nn.Linear(k, 256), nn.ReLU(), nn.Linear(256, d))
        self.k = k

    def forward(self, x):
        mu, log_var = self.codificador(x).chunk(2, dim=-1)
        sigma = torch.exp(0.5 * log_var)
        z = mu + sigma * torch.randn_like(sigma)      # reparametrizacion: el ruido entra por fuera
        return self.decodificador(z), mu, log_var

modelo = VAE()
optimizador = torch.optim.AdamW(modelo.parameters(), lr=1e-3)   # los parametros del MISMO modelo
for x, _ in cargador:                                 # solo se usan los datos, no las etiquetas
    x = x.view(x.size(0), -1)
    x_hat, mu, log_var = modelo(x)
    # El signo de dentro es el de la formula 0,5 * (mu^2 + sigma^2 - 1 - log_var)
    reconstruccion = nn.functional.binary_cross_entropy_with_logits(x_hat, x, reduction="sum")
    kl = 0.5 * torch.sum(mu.pow(2) + log_var.exp() - 1 - log_var)
    perdida = (reconstruccion + kl) / x.size(0)       # aqui es donde entraria el peso beta
    optimizador.zero_grad(); perdida.backward(); optimizador.step()
```

## Errores típicos

- **Usar un autoencoder para reducir dimensión cuando bastaba PCA.** Si necesitas interpretar las
  componentes, PCA te da direcciones con un significado algebraico claro y es determinista. El
  autoencoder gana cuando la variedad es claramente no lineal, y a cambio pierdes
  interpretabilidad y reproducibilidad: dos semillas dan dos latentes distintos.
- **Dejar el cuello de botella demasiado grande.** Si `k ≥ d` y no hay regularización, la red
  aprende a copiar la identidad: el error de reconstrucción es casi cero y el código no contiene
  estructura alguna. Si quieres un latente rico con `k` grande, usa ruido (denoising), dispersión
  o el término `KL` del VAE para que el cuello de botella sea informativo de verdad.
- **Evaluar con el error de reconstrucción de entrenamiento.** Un autoencoder puede memorizar el
  conjunto de entrenamiento y reconstruirlo casi perfecto. La calidad se mide sobre datos no
  vistos, y en detección de anomalías el umbral se calibra con datos normales de validación, no
  con el error de entrenamiento.
- **Creer que un error de reconstrucción bajo significa buena calidad visual.** La pérdida
  cuadrática promedia píxeles, y promediar píxeles produce imágenes borrosas. Un VAE con error
  bajo puede dar salidas desenfocadas: para calidad perceptiva hacen falta otros objetivos o
  arquitecturas distintas.
- **Muestrear un autoencoder normal como si fuera generativo, o dejar que el VAE ignore el
  latente.** El espacio latente de un autoencoder sin regularizar tiene huecos enormes entre
  códigos: un punto intermedio entre dos códigos aprendidos suele decodificar a algo sin sentido,
  y eso es lo que arregla el VAE. Pero el VAE tiene su propio modo de fallo: si el
  decodificador es demasiado potente, reconstruye sin mirar `z`, la `KL` se va a cero y el latente
  queda inútil (**colapso del posterior**). Se detecta midiendo la `KL` por dimensión durante el
  entrenamiento; si es casi cero, baja `β`, usa *free bits* o reduce la capacidad del
  decodificador.
- **Elegir el umbral de anomalía por porcentaje esperado de anomalías.** Si fijas el umbral en el
  p99 de los datos normales, estás decidiendo de antemano que el 1 % es anómalo. El umbral debe
  salir del coste de cada tipo de error: cuánto cuesta una falsa alarma frente a cuánto cuesta
  dejar pasar un caso real.

:::practica
enunciado: Entrenas un autoencoder con cuello de botella de 1 dimensión sobre datos centrados cuyas varianzas por componente son 2,50 y 0,10. En un conjunto de validación normal el error de reconstrucción por observación tiene media 0,10 y desviación 0,02. Fijas el umbral en el p99 (μ + 2,33σ) y llega una observación con error 0,15. ¿Es anómala?
pista: Con un latente de una dimensión, el error esperado es la varianza que se tira.
solucion: Al proyectar sobre la primera componente se descarta la segunda, así que el error esperado es 0,10 y coincide con la media de validación. El umbral queda en 0,10 + 2,33 · 0,02 = 0,10 + 0,047 = 0,147. La observación tiene 0,15 > 0,147: se marca como anómala, aunque por muy poco. Es un aviso de que un umbral ajustado con pocos datos de validación tiene poco margen.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes un autoencoder con 784 entradas y un latente de 784 dimensiones, sin ninguna regularización. ¿Qué va a pasar?
o: Aprenderá una representación más rica que PCA, con 784 factores independientes
o: Aprenderá a copiar la entrada: el error será casi cero y el código no tendrá estructura útil
o: No podrá entrenar porque el cuello de botella no comprime
a: 2
e: Sin cuello de botella ni regularización, la solución más fácil para minimizar la reconstrucción es la función identidad, que da error cero. Sí entrena, y precisamente por eso no sirve: el latente no resume nada. Para forzar estructura con k grande hay que añadir ruido, dispersión o el término KL del VAE.
:::

:::quiz
p: Con datos centrados, comprimes a 1 dimensión y el error de reconstrucción por observación es 0,0491. ¿Qué relación tiene ese número con PCA?
o: Es la suma de los dos autovalores de la covarianza
o: Es la varianza de la componente descartada, porque el error de reconstrucción de PCA es exactamente la varianza que no se retiene
o: Es la varianza de la primera componente
a: 2
e: Al proyectar sobre la primera componente se tira la segunda, y el error cuadrático medio por observación coincide con su varianza, 0,0491 frente a 1,284 de la primera. Por eso un autoencoder lineal con error cuadrático aprende el mismo subespacio: minimizar el error cuadrático es maximizar la varianza retenida.
:::

:::quiz
p: ¿Para qué sirve el término KL en la pérdida de un VAE?
o: Para que el decodificador tenga más parámetros
o: Para empujar la distribución que el codificador asigna a cada entrada hacia una normal estándar, de modo que el espacio latente quede continuo y se pueda muestrear
o: Para evitar que la reconstrucción sea demasiado buena y el modelo sobreajuste
a: 2
e: Sin ese término, cada entrada recibe un punto aislado del espacio y los huecos entre puntos decodifican a ruido. La KL empuja las medias hacia el origen y las varianzas hacia 1, con lo que las regiones se solapan y los puntos intermedios tienen sentido. Se pondera con beta, pero no es una herramienta contra el sobreajuste: la reconstrucción sigue siendo el término principal.
:::

:::trampa
El error de reconstrucción como detector de anomalías falla cuando el autoencoder es demasiado
expresivo: con suficientes parámetros puede reconstruir también lo raro, y la anomalía pasa
desapercibida. Si tus anomalías son reconstruidas con poco error, reduce la capacidad (menos
capas, `k` más pequeño), añade ruido al entrenamiento o cambia de enfoque: un detector que solo
ve datos normales rara vez basta con la capacidad de un autoencoder grande.
:::
