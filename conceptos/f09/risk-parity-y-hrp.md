---
id: risk-parity-y-hrp
titulo: Risk parity y HRP
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [construccion-de-carteras, markowitz-y-frontera, covarianza-y-correlacion, varianza-y-desviacion]
tags: [cartera, riesgo, correlacion, clustering]
resumen: Repartir el riesgo en vez del capital: pesos de igual contribución y la jerarquía de correlaciones que estabiliza la cartera cuando la matriz estimada no es fiable.
fuentes: ["López de Prado (2016), 'Building Diversified Portfolios that Outperform Out of Sample'", "Maillard, Roncalli y Teïletche (2010), 'The Properties of Equally Weighted Risk Contribution Portfolios'", "Markowitz (1952), 'Portfolio Selection'"]
---

## En una frase

En vez de repartir el dinero a partes iguales, se buscan pesos que hagan que cada activo aporte
la misma cantidad de riesgo a la cartera; HRP (Hierarchical Risk Parity) llega a un reparto
parecido sin invertir una matriz de covarianza estimada, que es la parte frágil de todo esto.

## La idea

Poner el mismo dinero en cada activo no reparte el riesgo: lo concentra donde más se mueve. Con
tres activos de volatilidad anual 10 %, 20 % y 30 % y correlaciones moderadas, una cartera a
partes iguales tiene unas contribuciones al riesgo del **7,5 %, 35,4 % y 57,1 %**. Es decir:
aparentemente estás diversificado en tres patas y en la práctica más de la mitad de tu riesgo
viene de una sola. La causa es doble: el activo se mueve más y, además, se mueve junto con otro
de la cartera. Un activo volátil y correlacionado con lo que ya tienes aporta mucho más que su
peso.

Risk parity ataca justo eso: se eligen los pesos de forma que cada activo contribuya lo mismo al
riesgo total. El caso más conocido es **ERC** (*equal risk contribution*), también llamado
*equal risk budget*. Nada de esto usa retornos esperados: es una cartera construida solo con la
matriz de covarianzas, y por eso se dice que es una apuesta a la diversificación, no a que un
activo lo vaya a hacer mejor que otro.

El problema aparece al estimar. La matriz de covarianzas de `n` activos tiene `n(n+1)/2` números
distintos; con 50 activos son 1.275 parámetros que estimas con datos ruidosos, y las
correlaciones son lo menos estable de todo. Tanto la cartera de mínima varianza como ERC (en su
versión numérica) miran dentro de esa matriz, y ahí un error pequeño se amplifica: en el ejemplo
de cuatro activos, mínima varianza pone el **0 %** en uno de ellos y el **73 %** en el que tiene
menos volatilidad. Un peso de cero no es una decisión de inversión, es un artefacto de la
estimación.

**HRP** propone otra cosa: en lugar de invertir la matriz, construir primero una **jerarquía** de
correlaciones (qué activos se parecen a cuáles), ordenar los activos según esa jerarquía y luego
repartir el riesgo por el árbol: primero entre los dos grandes grupos, después dentro de cada uno.
No pretende ser óptimo en la muestra; pretende que el resultado no salte cuando la estimación
cambie un poco. La jerarquía usa solo el *orden* de las distancias, no sus valores exactos, y por
eso es comparativamente robusta.

Hay dos advertencias que conviene tener presentes. La primera: ERC iguala riesgo, y eso maximiza
diversificación, no el Sharpe; en un universo con bonos y acciones, la cartera queda dominada por
los bonos (baja volatilidad) y su rentabilidad esperada es baja, por lo que las implementaciones
institucionales la apalancan. Ese apalancamiento es una decisión de financiación, con su coste y
su riesgo de margen, no una propiedad del método. La segunda: si mides el riesgo solo con
volatilidad, estás suponiendo que las subidas y las bajadas duelen igual y que las colas no
importan; con activos asimétricos conviene mirar además [[var-y-cvar]] y [[maximo-drawdown]].

## Definición formal

Sean `n` activos con vector de pesos `w` (habitualmente `wᵢ ≥ 0` y `Σ wᵢ = 1`), matriz de
covarianzas `Σ` y `σᵢ = √Σᵢᵢ` la volatilidad del activo `i`.

- `ρᵢⱼ = Σᵢⱼ / (σᵢ · σⱼ)` — correlación entre los activos `i` y `j`.
- `σ(w) = √(wᵀ Σ w)` — volatilidad de la cartera.
- `MRCᵢ = (Σw)ᵢ / σ(w)` — contribución marginal: cuánto sube la volatilidad de la cartera al
  añadir un poco de peso al activo `i`. Es la derivada parcial `∂σ/∂wᵢ`.
- `RCᵢ = wᵢ · MRCᵢ = wᵢ (Σw)ᵢ / σ(w)` — contribución total al riesgo. Como `σ(w)` es homogénea
  de grado 1 en los pesos, el teorema de Euler garantiza `Σᵢ RCᵢ = σ(w)`.
- **Contribución relativa:** `RCᵢ / σ(w)`. Es el número que se compara con `1/n`.

**Cartera ERC:** los pesos que cumplen, para todo `i` y todo `j`,

:::formula
ERC:  wᵢ (Σw)ᵢ = wⱼ (Σw)ⱼ  para todo i, j   ⇔   RCᵢ = σ(w) / n
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `wᵢ` | Peso del activo `i` en la cartera | tanto por uno, suman 1 | Sube su aportación al riesgo en proporción directa, aunque también mueve la de los demás |
| `Σ` | Matriz de covarianzas de los activos | % al cuadrado | Con más covarianza general, la cartera se concentra en los activos de menos riesgo |
| `σᵢ` | Volatilidad del activo `i`, `√Σᵢᵢ` | % anual | En la inversa de volatilidad, ese activo pesa menos; en ERC el efecto depende de las correlaciones |
| `σ(w)` | Volatilidad de la cartera, `√(wᵀΣw)` | % anual | Sube el riesgo total, pero las aportaciones relativas no tienen por qué cambiar |
| `RCᵢ` | Aportación del activo `i` al riesgo total | % al cuadrado, y suman `σ(w)` | Su activo manda más en la cartera: es lo que ERC obliga a igualar |
| `MRCᵢ` | Contribución marginal, `(Σw)ᵢ / σ(w)` | % | Mide cuánto sube la volatilidad al añadir un poco de peso, antes de ponderar por el peso |
| `ρᵢⱼ` | Correlación entre los activos `i` y `j` | adimensional, entre −1 y 1 | Con correlaciones altas, la inversa de volatilidad deja de igualar las aportaciones |
| `dᵢⱼ` | Distancia de HRP, `√(½(1 − ρᵢⱼ))` | adimensional, entre 0 y 1 | Los activos se separan en el árbol: primero se agrupan los más parecidos |
| `α` | Peso que la bisección de HRP da al primer grupo | tanto por uno | Se reparte según la varianza de cada mitad: la mitad más tranquila recibe más peso |
:::

No hay fórmula cerrada en general: se resuelve numéricamente. Un caso particular sí la tiene: si
la correlación entre todos los pares es cero, `Σ` es diagonal y la solución es la **inversa de
volatilidad**, `wᵢ ∝ 1/σᵢ`. Ese es el error más frecuente del tema: usar `1/σᵢ` y llamarlo risk
parity cuando las correlaciones no son cero (con dos activos sí coinciden: el término cruzado se
cancela).

**HRP** se construye en tres pasos:

1. **Distancia a partir de la correlación:** `dᵢⱼ = √(½ (1 − ρᵢⱼ))`. Va de 0 (correlación 1,
   activos indistinguibles) a 1 (correlación −1). Cumple las propiedades de una distancia, así
   que se puede agrupar con ella.
2. **Agrupación jerárquica:** se enlazan los dos grupos más cercanos repetidamente (enlace simple
   en la formulación original: la distancia entre dos grupos es la mínima entre sus elementos)
   hasta que todo queda en un árbol. El resultado es un dendrograma, y sus **hojas** dan un orden
   de los activos en el que los parecidos quedan juntos: la *cuasi-diagonalización*.
3. **Bisección recursiva:** con la lista ordenada, se parte por la mitad. La varianza de cada
   mitad, `V(g)`, se calcula con pesos de inversa de varianza **dentro** del grupo. Se reparte el
   peso entre las dos mitades con `α = 1 − V₁/(V₁ + V₂)` para la primera y `1 − α` para la
   segunda, y se repite el proceso dentro de cada mitad hasta llegar a activos sueltos.

:::figura
fichero: risk-parity-aportes-y-jerarquia
pie: A la izquierda, cuánto riesgo aporta cada activo en cuatro carteras construidas con la misma matriz de covarianzas. Con los pesos a partes iguales (primera barra) el activo 3 se lleva el 57 % del riesgo aunque tenga un tercio del dinero; ERC (tercera barra) lo deja en el 33 % exacto para los tres; y la mínima varianza baja todavía más la volatilidad a costa de concentrar el riesgo: le da al activo 3 solo un 2 % del peso, pero ese 2 % de peso aporta el 86 % del riesgo de la cartera, que es justo lo contrario de diversificar. A la derecha, la matriz de correlaciones de otros cuatro activos reordenada por el dendrograma de HRP: los dos bloques que se mueven juntos (0,8 y 0,7) quedan pegados a la diagonal, que es lo que permite repartir el riesgo por el árbol sin invertir la matriz.
fuente: figuras/risk-parity-y-hrp-1.py
:::

## Ejemplo

**Tres activos:** volatilidades 10 %, 20 % y 30 %; correlaciones `ρ₁₂ = 0,2`, `ρ₁₃ = 0,1`,
`ρ₂₃ = 0,6`.

| Cartera | Pesos | Contribuciones al riesgo | Volatilidad |
| --- | --- | --- | --- |
| Partes iguales | 33,3 / 33,3 / 33,3 | 7,5 % / 35,4 % / 57,1 % | 15,85 % |
| Inversa de volatilidad | 54,6 / 27,3 / 18,2 | 27,1 % / 37,5 % / 35,4 % | 11,95 % |
| ERC | 59,0 / 24,1 / 16,9 | 33,3 % / 33,3 % / 33,3 % | 11,42 % |
| Mínima varianza | 85,5 / 12,0 / 2,5 | 85,6 % / 12,0 % / 2,5 % | 9,54 % |

Tres lecturas. La inversa de volatilidad **no** iguala las contribuciones (27,1 contra 37,5)
porque hay correlación. ERC sí las iguala, y aun así baja la volatilidad desde el 15,85 % de las
partes iguales al 11,42 %. Y mínima varianza consigue menos volatilidad todavía (9,54 %) pero
concentrando el 85,6 % del riesgo en un solo activo: menos temblor, menos diversificación.

**Cuatro activos:** volatilidades 10 %, 12 %, 25 % y 28 %, con `ρ₁₂ = 0,7`, `ρ₃₄ = 0,8` y
correlaciones cruzadas del 0,1 al 0,2. El dendrograma empareja primero los activos 3 y 4 y luego
el 1 y el 2, así que el orden cuasi-diagonal es `[3, 4, 1, 2]`.

| Cartera | Pesos (1, 2, 3, 4) | Volatilidad |
| --- | --- | --- |
| Partes iguales | 25,0 / 25,0 / 25,0 / 25,0 | 14,33 % |
| Inversa de volatilidad | 38,6 / 32,2 / 15,4 / 13,8 | 11,05 % |
| HRP | 50,9 / 35,3 / 7,7 / 6,1 | 9,81 % |
| Mínima varianza | 73,5 / 18,2 / 0,0 / 8,3 | 9,54 % |

Mínima varianza vuelve a dejar un activo en cero. HRP concentra más que la inversa de volatilidad
(porque penaliza el grupo correlacionado 3-4) y no llega a la volatilidad de mínima varianza,
pero no depende de invertir la matriz: si mañana cambia la correlación entre 3 y 4, sus pesos se
mueven mucho menos.

## Código

```python verificable
import numpy as np
from scipy.optimize import minimize

# Tres activos con volatilidad anual del 10 %, 20 % y 30 %.
vol = np.array([0.10, 0.20, 0.30])
corr = np.array([[1.0, 0.2, 0.1],
                 [0.2, 1.0, 0.6],
                 [0.1, 0.6, 1.0]])
cov = np.outer(vol, vol) * corr          # Sigma = D * C * D

def contribuciones(w):
    sigma = np.sqrt(w @ cov @ w)         # volatilidad de la cartera
    return w * (cov @ w) / sigma         # RC_i = w_i * (Sigma w)_i / sigma

def dispersion(w):
    rc = contribuciones(w)               # ERC = contribuciones iguales
    return float(((rc - rc.mean()) ** 2).sum() * 1e6)   # escala para el optimizador

inicio = np.array([1 / 3, 1 / 3, 1 / 3])
erc = minimize(dispersion, inicio, method="SLSQP", bounds=[(0, 1)] * 3,
               constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}]).x
inversa = (1 / vol) / (1 / vol).sum()

print("pesos ERC:", np.round(erc, 4).tolist())              # -> pesos ERC: [0.5901, 0.2406, 0.1694]
print("aportes ERC:", np.round(contribuciones(erc) / contribuciones(erc).sum(), 4).tolist())  # -> aportes ERC: [0.3333, 0.3333, 0.3333]
print("volatilidad ERC:", round(float(np.sqrt(erc @ cov @ erc)), 4))   # -> volatilidad ERC: 0.1142
print("pesos inversa de volatilidad:", np.round(inversa, 4).tolist())  # -> pesos inversa de volatilidad: [0.5455, 0.2727, 0.1818]
print("aportes inversa de volatilidad:", np.round(contribuciones(inversa) / contribuciones(inversa).sum(), 4).tolist())  # -> aportes inversa de volatilidad: [0.2708, 0.375, 0.3542]
print("aportes a partes iguales:", np.round(contribuciones(inicio) / contribuciones(inicio).sum(), 4).tolist())  # -> aportes a partes iguales: [0.0752, 0.354, 0.5708]
```

:::claves
- `minimize` no devuelve los pesos: devuelve un objeto `OptimizeResult` y los pesos están en `.x`. Y `.success = True` no significa que hayas encontrado nada: si el objetivo está mal escalado, el optimizador puede devolverte el punto de partida tal cual y decir que ha convergido. Compara siempre el resultado con el punto de partida.
- `1 / vol` funciona porque `vol` es un `np.array` y la división es elemento a elemento. Con una lista de Python, `1 / vol` es un `TypeError`: hay que envolverla antes con `np.array`.
- `np.outer(vol, vol) * corr` construye la covarianza con producto **elemento a elemento**; si lo escribes con `@` estás multiplicando matrices y el resultado no es `Σ`. El `*` y el `@` no son intercambiables en NumPy.
- `dendrogram(Z, no_plot=True)["leaves"]` devuelve los índices de los activos ya ordenados, y ese orden es el que hace la cuasi-diagonalización. El orden concreto puede salir invertido según la versión de SciPy, así que no fijes los pesos a mano a partir de él: recalcula.
- `squareform(distancia, checks=False)` convierte la matriz de distancias en el vector condensado que espera `linkage`, y `checks=False` desactiva la comprobación de simetría: si la matriz no es simétrica o la diagonal no es cero, el árbol sale mal sin ningún aviso.
:::

```python verificable
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

vol = np.array([0.10, 0.12, 0.25, 0.28])
corr = np.array([[1.0, 0.7, 0.2, 0.1],
                 [0.7, 1.0, 0.2, 0.1],
                 [0.2, 0.2, 1.0, 0.8],
                 [0.1, 0.1, 0.8, 1.0]])
cov = np.outer(vol, vol) * corr

def varianza_grupo(indices):
    """Varianza de un grupo con pesos de inversa de varianza dentro del grupo."""
    sub = cov[np.ix_(indices, indices)]
    inv = 1 / np.diag(sub)
    w = inv / inv.sum()
    return float(w @ sub @ w)

def hrp(cov):
    n = cov.shape[0]
    desv = np.sqrt(np.diag(cov))
    correl = cov / np.outer(desv, desv)
    distancia = np.sqrt(np.clip(0.5 * (1 - correl), 0, None))   # d = sqrt((1-rho)/2)
    np.fill_diagonal(distancia, 0.0)
    Z = linkage(squareform(distancia, checks=False), method="single")
    orden = list(dendrogram(Z, no_plot=True)["leaves"])         # cuasi-diagonalizacion
    pesos = np.ones(n)
    grupos = [orden]
    while grupos:                                               # biseccion recursiva
        siguientes = []
        for grupo in grupos:
            if len(grupo) <= 1:
                continue
            mitad = len(grupo) // 2
            izq, der = grupo[:mitad], grupo[mitad:]
            v_izq, v_der = varianza_grupo(izq), varianza_grupo(der)
            alfa = 1 - v_izq / (v_izq + v_der)                  # menos riesgo, mas peso
            for i in izq:
                pesos[i] *= alfa
            for i in der:
                pesos[i] *= 1 - alfa
            siguientes += [izq, der]
        grupos = [g for g in siguientes if len(g) > 1]
    return orden, pesos / pesos.sum()

orden, pesos = hrp(cov)
print("orden de las hojas:", orden)                       # -> orden de las hojas: [2, 3, 0, 1]
print("pesos HRP:", np.round(pesos, 4).tolist())          # -> pesos HRP: [0.5089, 0.3534, 0.0766, 0.0611]
print("volatilidad HRP:", round(float(np.sqrt(pesos @ cov @ pesos)), 4))   # -> volatilidad HRP: 0.0981
print("volatilidad a partes iguales:", round(float(np.sqrt(np.full(4, 0.25) @ cov @ np.full(4, 0.25))), 4))   # -> volatilidad a partes iguales: 0.1433
```

```python ilustrativo
import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf

# Con datos reales, Sigma se estima y ahi esta el problema. El estimador de
# Ledoit-Wolf encoge la matriz hacia una estructura simple y suele ser mas
# estable que la covarianza muestral cuando hay muchos activos y pocas filas.
retornos = pd.read_parquet("retornos_diarios.parquet")     # T filas x n columnas
lw = LedoitWolf().fit(retornos.to_numpy())
cov = lw.covariance_ * 252                                  # anualizar
print("intensidad de encogimiento:", lw.shrinkage_)
```

## Errores típicos

- **Confundir pesos iguales con riesgo igual.** El 60/40 y el 1/n son carteras de capital, no de
  riesgo: en el ejemplo de tres activos, partes iguales reparte el riesgo 7,5 / 35,4 / 57,1. Si
  querías diversificar, no lo has hecho.
- **Llamar risk parity a la inversa de la volatilidad.** `wᵢ ∝ 1/σᵢ` solo iguala las
  contribuciones cuando las correlaciones son cero (o cuando solo hay dos activos, donde el
  término cruzado se cancela). Con `ρ₂₃ = 0,6` en el ejemplo de tres activos da
  27,1 / 37,5 / 35,4, que está lejos de igualar nada. Es una cartera razonable, pero no es ERC.
- **Invertir una matriz de covarianza estimada con pocos datos.** Mínima varianza deja activos en
  cero y concentra el riesgo en uno; pequeñas variaciones de la muestra cambian los pesos por
  completo. Si vas a usar la matriz, encógela (Ledoit-Wolf) o usa una versión que no la invierta,
  como HRP.
- **Comparar volatilidades de carteras y creer que eso cierra el análisis.** Mínima varianza gana
  en volatilidad (9,54 % frente a 11,42 %) y a la vez concentra el 85,6 % del riesgo en un solo
  activo. Menos temblor con menos diversificación no es gratis: mira la cartera entera y su
  comportamiento en una caída, no un solo número.
- **Reestimar los pesos a diario sin mirar el coste.** Los pesos objetivo de ERC cambian cada vez
  que se reestima la volatilidad y la correlación, así que el turnover es mayor que en una cartera
  de pesos fijos. Con comisiones y deslizamiento realistas, la diferencia se come el efecto. Ver
  [[rebalanceo]] y [[slippage-y-comisiones]].
- **Usar correlaciones de Pearson sobre retornos con ceros y precios poco frecuentes.** Activos
  ilíquidos generan correlaciones artificialmente bajas (los ceros no son información), y la
  jerarquía se construye sobre ruido. Antes de agrupar, mira [[volatilidad-realizada]] y la
  calidad de los datos.

## Comprueba que lo sabes

:::quiz
p: Con tres activos, la cartera a partes iguales da contribuciones al riesgo del 7,5 %, 35,4 % y 57,1 %. ¿Qué significa?
o: Que el activo 3 aporta más de la mitad del riesgo de la cartera, aunque tenga el mismo dinero que los demás
o: Que el activo 3 tiene menos volatilidad que los otros dos
o: Que la cartera tiene una correlación media negativa
a: 1
e: La contribución al riesgo combina el peso con la volatilidad y con la correlación con el resto. Un activo volátil y correlacionado con los demás se lleva la mayor parte del riesgo aunque su peso sea un tercio. Que aporte más riesgo implica que es el más volátil, no el menos.
:::

:::quiz
p: ¿Cuándo coincide la cartera de inversa de volatilidad con la cartera ERC?
o: Cuando todos los activos tienen la misma volatilidad
o: Cuando las correlaciones entre todos los pares son cero
o: Siempre: son dos formas de calcular lo mismo
a: 2
e: Con Σ diagonal, `wᵢ (Σw)ᵢ = wᵢ²σᵢ²`, y las contribuciones iguales exigen `wᵢ ∝ 1/σᵢ`. En cuanto hay correlación, cada contribución incorpora términos cruzados distintos y la inversa de volatilidad deja de igualarlas. La excepción son dos activos: allí el término cruzado es el mismo en las dos contribuciones y se cancela. Que las volatilidades sean iguales llevaría a pesos iguales, que tampoco es ERC si hay correlación.
:::

:::quiz
p: ¿Qué hace HRP para no tener que invertir la matriz de covarianzas?
o: Usa solo las volatilidades individuales y descarta las correlaciones
o: Agrupa los activos por distancia de correlación, los ordena por el dendrograma y reparte el riesgo por el árbol con bisección recursiva
o: Estima la matriz con muchos más datos para que la inversa sea estable
a: 2
e: HRP sustituye la inversión por una jerarquía: la distancia `√((1−ρ)/2)` mide parecido, la agrupación construye el árbol, sus hojas dan el orden cuasi-diagonal y la bisección recursiva reparte el peso entre mitades usando varianzas de grupo. Sí usa las correlaciones, solo que a través de su orden, no de sus valores exactos.
:::

:::practica
enunciado: Dos activos con volatilidad anual del 15 % y del 25 % y correlación 0,5, con pesos 50/50. Calcula la volatilidad de la cartera y las contribuciones relativas al riesgo. Después mira los pesos de inversa de volatilidad (0,625 y 0,375) y explica por qué con dos activos sí igualan las contribuciones y con tres no.
pista: La contribución relativa de cada activo es wᵢ(Σw)ᵢ dividido entre la varianza de la cartera, y el término de covarianza se suma igual a las dos.
solucion: La covarianza es 0,5 · 0,15 · 0,25 = 0,01875. Σw con pesos 50/50 vale (0,020625, 0,040625) y la varianza de la cartera es 0,25 · 0,0225 + 0,25 · 0,0625 + 0,5 · 0,01875 = 0,030625, así que la volatilidad es 0,175. Las contribuciones relativas son 0,5 · 0,020625 / 0,030625 = 33,7 % y 0,5 · 0,040625 / 0,030625 = 66,3 %. Con los pesos de inversa de volatilidad (0,625 y 0,375), Σw vale (0,02109375, 0,03515625), la varianza baja a 0,02636719 y las dos contribuciones relativas valen exactamente 50 %. La razón es que el término cruzado w₁w₂ρσ₁σ₂ aparece sumando en las dos contribuciones, así que igualarlas exige w₁σ₁ = w₂σ₂, que es la inversa de volatilidad. Con tres o más activos cada contribución lleva términos cruzados distintos y esa coincidencia desaparece.
:::

:::aviso
Risk parity no usa retornos esperados: no promete más rentabilidad, promete un reparto de riesgo
concreto. Si tu universo son activos de volatilidad muy distinta, la cartera acabará dominada por
los de baja volatilidad, y subir la rentabilidad esperada exige apalancar. Ese apalancamiento
tiene coste, llamadas de margen y su propio riesgo de ruina, que se estudia en
[[riesgo-de-ruina]] y en [[criterio-de-kelly]].
:::
