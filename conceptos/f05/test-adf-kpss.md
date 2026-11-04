---
id: test-adf-kpss
titulo: Tests de raíz unitaria: ADF y KPSS
fase: 5
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [estacionariedad, contraste-de-hipotesis, autocorrelacion-acf-pacf]
tags: [series-temporales, contrastes, raiz-unitaria]
resumen: Dos contrastes con hipótesis nulas opuestas para decidir si una serie necesita diferenciarse, y por qué hay que usarlos juntos.
fuentes: ["Dickey y Fuller (1979), 'Distribution of the Estimators for Autoregressive Time Series with a Unit Root'", "Kwiatkowski, Phillips, Schmidt y Shin (1992), 'Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root'", "Hamilton (1994), 'Time Series Analysis', cap. 17"]
---

## En una frase

El contraste ADF plantea como hipótesis nula que la serie tiene una raíz unitaria y el KPSS
plantea justo lo contrario, que es estacionaria; como sus hipótesis nulas son opuestas, se aplican
los dos y se interpretan juntos.

## La idea

El ojo engaña. Mira el precio de una acción durante dos años: sube, baja, se recupera. ¿Es un
paseo aleatorio o una serie que oscila alrededor de una tendencia? Con 500 datos y una raíz
cercana a la unidad, las dos cosas se parecen muchísimo, y las consecuencias de confundirlas son
graves: si diferencias una serie estacionaria, le metes ruido y una autocorrelación artificial; si
no diferencias una que tenía raíz unitaria, tus intervalos de predicción se quedan cortos y el
modelo pronostica con una media que ya no existe.

Para decidir hace falta un contraste, y aquí aparece una dificultad incómoda: en un contraste
clásico la hipótesis nula es lo que quieres refutar, y **no rechazar no es lo mismo que aceptar**.
Si solo tienes un contraste, un resultado "no significativo" te deja sin saber si la serie es
estacionaria o si simplemente tienes pocos datos. La solución práctica es usar dos contrastes
cuyas hipótesis nulas son opuestas:

- **ADF** (Augmented Dickey-Fuller). Hipótesis nula: la serie tiene una raíz unitaria, es decir,
  no es estacionaria. Si rechazas, tienes evidencia a favor de la estacionariedad.
- **KPSS** (Kwiatkowski, Phillips, Schmidt y Shin). Hipótesis nula: la serie es estacionaria
  (alrededor de una constante o de una tendencia determinista). Si rechazas, tienes evidencia a
  favor de la raíz unitaria.

El ADF es un contraste de raíz unitaria; el KPSS es un contraste de estacionariedad. Ninguno es
"mejor": el ADF tiene poca potencia cuando la raíz está cerca de 1 (le cuesta distinguir 0,98 de
1) y el KPSS tiene poca potencia cuando la raíz está lejos de 1. Por eso se cruzan los resultados,
y de ahí salen cuatro situaciones con lecturas muy distintas:

| ADF | KPSS | Lectura |
| --- | --- | --- |
| rechaza | no rechaza | Estacionaria. Modela el nivel (ARMA) o la tendencia más un ARMA. |
| no rechaza | rechaza | Raíz unitaria. Diferencia y vuelve a contrastar. |
| rechaza | rechaza | Contradicción. Sospecha de un cambio estructural, de integración fraccionaria o de una serie muy persistente. |
| no rechaza | no rechaza | No hay información suficiente. Con muestras cortas es lo más habitual. |

El caso "los dos rechazan" merece un comentario, porque es el que más confunde. Un cambio
estructural —una crisis, un cambio de regulación, un cambio de metodología— hace que los dos
contrastes vean algo raro: el ADF se queda sin potencia porque la serie parece tener una raíz, y
el KPSS detecta que la media no es constante en todo el periodo. La respuesta correcta no es
elegir el test que te da la razón, sino mirar la serie, buscar el punto de ruptura y, si lo hay,
contrastar permitiéndolo explícitamente.

## Definición formal

**ADF.** Se estima por mínimos cuadrados la regresión

:::formula
Δy_t = α + β·t + γ·y_{t−1} + Σ_{i=1}^{p} δ_i·Δy_{t−i} + ε_t
:::

y el estadístico es `ADF = γ̂ / SE(γ̂)`, el cociente entre el coeficiente estimado de `y_{t−1}` y
su error típico.

- `y_t` — la serie que se contrasta.
- `Δy_t = y_t − y_{t−1}` — la primera diferencia.
- `α` — la constante de la regresión (el nivel).
- `β·t` — la tendencia determinista; se incluye o no según la especificación (`sin constante`,
  `con constante`, `con constante y tendencia`).
- `γ` — el coeficiente clave: si `γ = 0` hay raíz unitaria y la serie no es estacionaria; si
  `γ < 0`, la serie tira hacia su media y es estacionaria.
- `δ_i` — los coeficientes de los `p` retardos de la diferencia, que limpian la autocorrelación
  del error.
- `p` — el número de retardos; se elige con un criterio de información (AIC o BIC) o con la regla
  de Schwert `p_max = parte entera de 12·(T/100)^(1/4)`, con `T` el número de observaciones.

**Lo importante:** `ADF` no se compara con los valores críticos de una t de Student. La
distribución de `γ̂/SE(γ̂)` bajo la hipótesis nula no es la normal estándar, porque bajo una raíz
unitaria la serie no es estacionaria y la teoría asintótica habitual no aplica. Los valores
críticos son mucho más negativos: con constante y muestra grande, **−3,43 al 1 %, −2,86 al 5 % y
−2,57 al 10 %**. Hay que rechazar cuando el estadístico es *más pequeño* que el valor crítico.

**KPSS.** Se estima la regresión de `y_t` sobre una constante (caso "nivel") o sobre una constante
y una tendencia (caso "tendencia"), se toman los residuos `ê_t` y se calcula

:::formula
S_t = Σ_{i=1}^{t} ê_i   ·   LM = (1/T²) · Σ_{t=1}^{T} S_t² / σ̂²
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `y_t` | La serie que se contrasta | las de la serie | Es el dato. Ojo con la escala: el ADF es invariante a multiplicar la serie por una constante, pero el KPSS no cambia tampoco, así que da igual medir en euros o en miles |
| `Δy_t` | La primera diferencia, `y_t − y_{t−1}` | las de la serie | Es la variable que se explica. Si la serie ya venía diferenciada y la vuelves a diferenciar, metes una raíz unitaria artificial y los dos contrastes se vuelven difíciles de leer |
| `γ` | El coeficiente de `y_{t−1}` en la regresión del ADF | 1/periodo (adimensional si el paso es 1) | Es la pieza clave: con `γ = 0` hay raíz unitaria; cuanto más negativo, más tira la serie hacia su media. El estadístico `ADF = γ̂/SE(γ̂)` crece en valor absoluto al alejarse de cero |
| `ADF` | El estadístico del contraste | adimensional | Se compara con valores críticos **muy negativos**: −3,43 (1 %), −2,86 (5 %) y −2,57 (10 %) con constante. Hay que rechazar cuando es más pequeño que el umbral, y no se compara con una t de Student |
| `α` (ADF) | La constante de la regresión | las de la serie | Recoge el nivel. Incluirla o no es una decisión de especificación: con una serie que tiene tendencia determinista, la constante sola no basta y el contraste se equivoca |
| `β·t` | La tendencia determinista | las de la serie por periodo | Si la serie tiene una dirección clara y no la incluyes, el ADF pierde potencia y el KPSS rechaza: en el ejemplo de la página el ADF pasa de −0,55 a −12,83 al añadirla |
| `p` | Número de retardos de la diferencia que se incluyen | retardos | Con pocos, el error queda autocorrelacionado y el contraste rechaza demasiado; con muchos, pierdes potencia. La regla de Schwert da `12 · (T/100)^0,25` como máximo: 12 con `T = 100` y 16 con `T = 400` |
| `T` | Número de observaciones | observaciones | Con `T` pequeño los dos contrastes casi nunca rechazan y el resultado es «no hay información». Por debajo de 50 observaciones no esperes un veredicto |
| `ê_t` | Los residuos de la regresión del KPSS sobre la constante (o sobre constante y tendencia) | las de la serie | Si la serie tiene raíz unitaria, los residuos se acumulan y la suma siguiente crece sin freno |
| `S_t` | La suma acumulada de los residuos hasta `t` | las de la serie | Es un paseo aleatorio de los residuos. Si la serie fuese estacionaria, `S_t` oscilaría alrededor de cero; con raíz unitaria se va |
| `σ̂²` | La varianza de largo plazo de los residuos (kernel de Bartlett, ancho `l`) | las de la serie, al cuadrado | Está en el denominador: si la estimas grande, el `LM` baja y te cuesta rechazar. Su ancho de banda es `l = 4 · (T/100)^0,25` |
| `LM` | El estadístico del KPSS | adimensional | Al contrario que el ADF, se rechaza cuando es **grande**. Umbrales en el caso «nivel»: 0,739 (1 %), 0,463 (5 %), 0,347 (10 %); en el caso «tendencia» son 0,216, 0,146 y 0,119 |
:::

- `ê_t` — los residuos de esa regresión.
- `S_t` — la suma acumulada de los residuos hasta `t`; es una especie de paseo aleatorio de los
  residuos, y si la serie fuera un paseo aleatorio crecería mucho.
- `σ̂²` — la varianza de largo plazo de los residuos, estimada con un kernel de Bartlett
  (Newey-West) y un ancho de banda `l = parte entera de 4·(T/100)^(1/4)`.
- `LM` — el estadístico; se rechaza la estacionariedad cuando es **grande**. Valores críticos en
  el caso "nivel": 0,739 (1 %), 0,463 (5 %), 0,347 (10 %). En el caso "tendencia" son mucho
  menores: 0,216, 0,146 y 0,119.

:::figura
fichero: adf-kpss-cuatro-casillas
pie: Los cuatro contrastes sobre 300 días simulados, cada panel con su lectura en una línea. Con el ruido, ADF y KPSS coinciden en que la serie es estacionaria; con el paseo, coinciden en que hay raíz unitaria. El panel de abajo a la derecha es el que enseña: una serie con tendencia determinista da «raíz unitaria» con los dos tests mientras el contraste lleve solo constante, y al permitir la tendencia pasa a −11,49 y 0,058, es decir, estacionaria. La especificación importa tanto como los datos.
fuente: figuras/test-adf-kpss-1.py
:::

## Ejemplo

**Cuántos retardos meter (regla de Schwert).** Con `T = 100`: `12 · 1^0,25 = 12` retardos como
máximo. Con `T = 400`: `12 · 4^0,25 = 12 · 1,414 = 16,97`, es decir 16. La regla crece muy
despacio: cuadruplicar la muestra solo añade cuatro retardos.

**El cálculo del KPSS a mano.** Cuatro residuos `ê = (1, −1, 1, −1)`, supongamos `σ̂² = 1` (no hay
autocorrelación que sumar). Las sumas acumuladas son `S = (1, 0, 1, 0)` y su suma de cuadrados es
`1 + 0 + 1 + 0 = 2`. Entonces

```
LM = (1/16) · 2 / 1 = 0,125
```

Como 0,125 está muy por debajo de 0,463, no se rechaza la estacionariedad. Fíjate en que los
residuos van alternando: no se acumulan, y esa es exactamente la señal de que no hay raíz
unitaria.

**Las dos series de siempre.** Sobre 300 observaciones simuladas:

- Un paseo aleatorio da `ADF = −0,81` (mayor que −2,86: no se rechaza la raíz unitaria) y
  `KPSS = 1,450` (muy por encima de 0,463: se rechaza la estacionariedad). Los dos coinciden.
- Ruido blanco da `ADF = −11,78` (rechazo clarísimo) y `KPSS = 0,279` (por debajo de 0,463: no se
  rechaza). Los dos coinciden otra vez.

**La trampa de la tendencia.** Cuatro series de 300 datos, contrastadas solo con constante:

```
ruido              ADF -12,05   KPSS 0,166   -> estacionaria
paseo              ADF  -0,22   KPSS 4,750   -> raiz unitaria
paseo con deriva   ADF  -2,69   KPSS 1,768   -> raiz unitaria
tendencia + ruido  ADF  -0,55   KPSS 5,092   -> ¿raiz unitaria?
```

La última serie es `0,1·t + ruido`: tiene una tendencia determinista perfectamente predecible y
**es estacionaria alrededor de esa tendencia**. Pero contrastada solo con constante, los dos
tests dicen que hay raíz unitaria, porque la constante no puede recoger una media que crece. Al
repetir el contraste permitiendo tendencia, el resultado se da la vuelta: `ADF = −12,83` y
`KPSS = 0,029`, es decir, estacionaria. La especificación del contraste importa tanto como los
datos.

## Código

```python verificable
import numpy as np

def adf_stat(y, p=1, tendencia=False):
    """Estadistico t del coeficiente de y_{t-1} en la regresion de Dickey-Fuller."""
    dy = np.diff(y)
    X, objetivo = [], []
    for j in range(p, dy.size):
        fila = [y[j]]                                   # y_{t-1}
        if tendencia:
            fila.append(j + 1)                          # tendencia determinista
        fila.append(1.0)                                # constante
        fila += [dy[j - i] for i in range(1, p + 1)]    # retardos de la diferencia
        X.append(fila)
        objetivo.append(dy[j])
    X, d = np.array(X), np.array(objetivo)
    b, *_ = np.linalg.lstsq(X, d, rcond=None)
    resid = d - X @ b
    s2 = resid @ resid / (X.shape[0] - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    return b[0] / np.sqrt(cov[0, 0])

def kpss_stat(y, tendencia=False):
    """Estadistico LM: suma acumulada de residuos sobre la varianza de largo plazo."""
    T = y.size
    X = np.column_stack([np.ones(T), np.arange(1, T + 1)]) if tendencia else np.ones((T, 1))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    S = np.cumsum(e)
    nlags = int(4 * (T / 100) ** 0.25)                  # regla de Schwert
    s2 = (e @ e) / T
    for l in range(1, nlags + 1):
        s2 += 2 * (1 - l / (nlags + 1)) * (e[l:] @ e[:-l]) / T
    return (S @ S) / (T ** 2 * s2)

rng = np.random.default_rng(0)
n = 300
ruido = rng.normal(0, 1, n)
paseo = np.cumsum(ruido)
print("criticos ADF (constante): -3.43 (1%)  -2.86 (5%)  -2.57 (10%)")
print("criticos KPSS (nivel):     0.739 (1%)   0.463 (5%)   0.347 (10%)")
for nombre, s in (("paseo aleatorio", paseo), ("ruido blanco", ruido)):
    print(f"{nombre:>16}  ADF {adf_stat(s):+.2f}   KPSS {kpss_stat(s):.3f}")
# -> paseo aleatorio: ADF -0.81 y KPSS 1.450
# -> ruido blanco:    ADF -11.78 y KPSS 0.279
```

:::claves
- El orden de las columnas de `X` es una convención del código, no de la fórmula: la función construye `[y_{t-1}, tendencia?, constante, retardos...]` y después lee `b[0]` como el coeficiente de `y_{t-1}`. Si mueves la constante al principio, `b[0]` pasa a ser la constante y el estadístico sale sin sentido **sin dar ningún error**.
- `np.linalg.lstsq(X, d, rcond=None)` devuelve una tupla y el código se queda con el primer elemento (`b, *_ = ...`). El `rcond=None` no es decorativo: fija explícitamente el criterio de corte que NumPy 2 usa por defecto y evita el aviso de que el comportamiento cambiará. Con matrices mal condicionadas (una constante y una tendencia que crece hasta 300 son casi colineales) ese corte decide qué valores singulares se descartan.
- El estadístico no es `γ̂` sino `γ̂ / SE(γ̂)`, y el error típico sale de la matriz de covarianzas `s2 * inv(X.T @ X)`. El `s2` se divide entre `X.shape[0] - X.shape[1]` (filas menos columnas), no entre las filas: usar `n` en lugar de `n − k` infla el estadístico y te hace rechazar de más.
- `adf_stat` empieza el bucle en `j = p` y usa `y[j]` como `y_{t−1}`, mientras que `objetivo` es `dy[j]`. Ese desplazamiento de uno es el que empareja cada diferencia con su nivel anterior; si cambias `range(p, dy.size)` por `range(dy.size - p)`, la regresión sigue ejecutándose pero compara instantes que no se corresponden.
- El parámetro `p` (retardos) tiene un valor por defecto de 1 en esta función, no el que elige AIC. Con `p = 1` fijo, una serie con autocorrelación más larga deja el error correlacionado y el contraste rechaza demasiado. La regla de Schwert solo dice el máximo: `int(12 * (T / 100) ** 0.25)` con `T = 100` da 12 y con `T = 400` da 16.
- En `kpss_stat`, `S = np.cumsum(e)` se eleva al cuadrado ya sumado: `(S @ S)` es `Σ S_t²`. Y `nlags` se calcula con la misma regla de Schwert pero con coeficiente 4, no 12, así que para `T = 300` vale `int(4 · 3^0,25) = 5`. Cambiar ese 4 por 12 cambia el resultado sin que ninguna línea falle.
- `np.linalg.inv(X.T @ X)` calcula la inversa explícitamente. Con `X` mal condicionada (una constante y una tendencia que crece hasta 300) la inversa amplifica los errores de redondeo; `np.linalg.solve` o `lstsq` sobre el sistema completo son más estables. Aquí funciona porque la construcción es la misma en los dos bloques y las cifras son las de la página.
- El bloque compara con los valores críticos escritos a mano (`−2,86` y `0,463` al 5 %). Esos números son para muestras grandes con constante: con `T = 300` son una aproximación razonable, pero con 40 observaciones el umbral real del ADF es **más** negativo (−2,97 al 5 % simulando paseos aleatorios con esta misma función; la tabla de Fuller da −3,00 con `T = 25`), así que comparar contra −2,86 rechaza de más, no de menos. Lo que hace parecer que con pocos datos no se rechaza es la falta de potencia frente a alternativas cercanas a 1, no el umbral.
:::

```python verificable
import numpy as np

# (se repiten adf_stat y kpss_stat del bloque anterior)
def adf_stat(y, p=1, tendencia=False):
    dy = np.diff(y)
    X, objetivo = [], []
    for j in range(p, dy.size):
        fila = [y[j]]                                   # y_{t-1}
        if tendencia:
            fila.append(j + 1)                          # tendencia determinista
        fila.append(1.0)                                # constante
        fila += [dy[j - i] for i in range(1, p + 1)]    # retardos de la diferencia
        X.append(fila)
        objetivo.append(dy[j])
    X, d = np.array(X), np.array(objetivo)
    b, *_ = np.linalg.lstsq(X, d, rcond=None)
    resid = d - X @ b
    s2 = resid @ resid / (X.shape[0] - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    return b[0] / np.sqrt(cov[0, 0])

def kpss_stat(y, tendencia=False):
    T = y.size
    X = np.column_stack([np.ones(T), np.arange(1, T + 1)]) if tendencia else np.ones((T, 1))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    S = np.cumsum(e)
    nlags = int(4 * (T / 100) ** 0.25)
    s2 = (e @ e) / T
    for l in range(1, nlags + 1):
        s2 += 2 * (1 - l / (nlags + 1)) * (e[l:] @ e[:-l]) / T
    return (S @ S) / (T ** 2 * s2)

rng = np.random.default_rng(3)
n = 300
t = np.arange(n)
series = {
    "ruido": rng.normal(0, 1, n),
    "paseo": np.cumsum(rng.normal(0, 1, n)),
    "paseo con deriva": np.cumsum(rng.normal(0.1, 1, n)),
    "tendencia + ruido": 0.1 * t + rng.normal(0, 1, n),
}
for nombre, s in series.items():
    print(f"{nombre:>17}  ADF {adf_stat(s):+.2f}   KPSS {kpss_stat(s):.3f}")
# -> ruido -12.05 / 0.166;  paseo -0.22 / 4.750;  paseo con deriva -2.69 / 1.768
# -> tendencia + ruido -0.55 / 5.092 (los dos se equivocan por omitir la tendencia)

s = series["tendencia + ruido"]
print("con tendencia en el contraste: ADF %+.2f  KPSS %.3f"
      % (adf_stat(s, tendencia=True), kpss_stat(s, tendencia=True)))
# -> ADF -12.83 y KPSS 0.029: estacionaria alrededor de la tendencia
```

```python ilustrativo
# Las mismas cuentas con statsmodels. La importacion es lenta (varios segundos),
# por eso este bloque no es verificable.
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss

rng = np.random.default_rng(0)
paseo = np.cumsum(rng.normal(0, 1, 300))

print(adfuller(paseo, autolag="AIC")[0:2])        # estadistico y p-valor del ADF
print(kpss(paseo, regression="c", nlags="auto")[0:2])
```

## Errores típicos

- **Leer "no rechazo" como "hay raíz unitaria".** No rechazar solo significa que los datos no
  bastan para descartar la hipótesis nula. Con 40 observaciones, el ADF no rechaza ni cuando la
  serie es claramente estacionaria. Habla de "no hay evidencia en contra", no de "queda
  demostrado".
- **Usar un solo contraste.** Con el ADF solo, una serie con un cambio de nivel a mitad de la
  muestra parece tener raíz unitaria para siempre. El KPSS, que es sensible a la media no
  constante, lo detecta. Se ejecutan los dos y se leen las cuatro casillas.
- **Olvidar la tendencia determinista en la especificación.** Es el error más caro y el más
  fácil de cometer: contra una serie con tendencia limpia, el ADF con constante da `−0,55` (no
  rechaza) y el KPSS da `5,09` (rechaza); con tendencia incluida, los dos dan `−12,83` y `0,029`.
  Mira siempre el gráfico antes de elegir la especificación.
- **Comparar el estadístico con la t de Student.** Un ADF de −2,0 es "significativo" para una t
  normal y no lo es para el ADF, cuyo umbral al 5 % es −2,86. Toda la distribución cambia porque
  bajo la nula el estimador no es asintóticamente normal.
- **Elegir los retardos a ojo.** Con pocos retardos, el error de la regresión queda
  autocorrelacionado y el contraste rechaza demasiado (distorsión de tamaño); con demasiados,
  pierdes potencia. Deja que AIC o BIC los elijan, o aplica la regla de Schwert y comprueba los
  residuos con su [[autocorrelacion-acf-pacf|ACF]].
- **Aplicar los contrastes a series cortas o con estacionalidad fuerte.** Con menos de 50
  observaciones, casi nunca rechazan. Y con estacionalidad, la estacionalidad domina el
  estadístico: quita antes la parte estacional (diferencia estacional o
  [[descomposicion-stl|descomposición]]) y contrasta el residuo.

:::practica
enunciado: Con T = 200 observaciones aplicas la regla de Schwert para el número máximo de retardos del ADF. Después contrastas una serie con ADF = −2,10 y KPSS = 0,290, ambos con constante. ¿Cuántos retardos como máximo admites y qué conclusión sacas?
pista: Los umbrales al 5 % son −2,86 para el ADF (rechazas si es más negativo) y 0,463 para el KPSS de nivel (rechazas si es mayor).
solucion: Schwert: 12 · (200/100)^0,25 = 12 · 1,189 = 14,27, es decir 14 retardos como máximo. El ADF de −2,10 es mayor que −2,86, así que no rechaza la raíz unitaria; el KPSS de 0,290 no llega a 0,463, así que no rechaza la estacionariedad. Los dos no rechazan: no hay información suficiente, y con 200 datos toca mirar el gráfico o ampliar la muestra.
:::

## Comprueba que lo sabes

:::quiz
p: Un ADF con constante da −1,20 y un KPSS de nivel da 2,80. ¿Qué concluyes?
o: Que la serie es estacionaria, porque el ADF no rechaza
o: Que hay evidencia de raíz unitaria: el ADF no puede descartarla y el KPSS rechaza la estacionariedad
o: Que los tests se contradicen y no se puede decir nada
a: 2
e: El umbral del ADF al 5 % es -2,86, así que -1,20 no rechaza la raíz unitaria; el KPSS de 2,80 supera de largo el 0,463 y rechaza la estacionariedad. Los dos apuntan en la misma dirección: diferencia la serie y vuelve a contrastar.
:::

:::quiz
p: ¿Por qué una serie con tendencia determinista puede dar ADF no significativo si el contraste solo incluye una constante?
o: Porque el ADF no sirve para series con tendencia
o: Porque la constante no puede recoger una media que crece, así que el modelo se parece al de un paseo aleatorio con deriva
o: Porque la tendencia hace que la varianza deje de ser finita
a: 2
e: Si la media crece, una recta constante queda siempre por debajo o por encima y los residuos se acumulan igual que en un paseo aleatorio. Al añadir el término de tendencia, los residuos dejan de acumularse y el contraste detecta la estacionariedad: en el ejemplo de la página, el ADF pasa de -0,55 a -12,83.
:::

:::aviso
Ninguno de los dos contrastes detecta bien una raíz **cercana** a 1. Un proceso con coeficiente
0,97 es técnicamente estacionario, pero se comporta como un paseo aleatorio durante décadas. Si el
veredicto es ambiguo, la decisión práctica se toma por otro camino: cómo se comportan los
pronósticos fuera de muestra y qué errores cometes si diferencias de más o de menos.
:::
