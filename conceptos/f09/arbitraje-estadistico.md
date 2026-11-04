---
id: arbitraje-estadistico
titulo: Arbitraje estadístico
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [cointegracion, regresion-lineal, construccion-de-carteras, z-score-y-estandarizacion]
tags: [stat-arb, factores, neutralidad, costes]
resumen: Cientos de posiciones pequeñas para explotar la reversión de lo que los factores no explican, con una sensibilidad al coste que decide si existe negocio.
fuentes: ["Avellaneda y Lee (2010), 'Statistical Arbitrage in the US Equities Market'", "Pole (2007), 'Statistical Arbitrage: Algorithmic Trading Insights and Techniques'"]
---

## En una frase

El arbitraje estadístico apuesta a que, después de quitar a cada activo la parte que explican
los factores comunes, lo que sobra vuelve a su sitio.

## La idea

Piensa en una regata con quinientos barcos. Si te preguntas quién va a llegar antes a la
boya, la respuesta depende sobre todo de la marea y del viento: eso es el mercado, y no lo
predices. Pero si te preguntas qué barco va mejor de lo que le correspondería por su
tripulación, el viento deja de importar: comparas cada barco con lo que predicen sus
condiciones y te fijas en la sorpresa. El arbitraje estadístico vive de las sorpresas.

Formalmente, cada activo tiene una parte de su retorno que se explica por factores comunes
(el mercado, el sector, el tamaño, el valor, la volatilidad) y una parte que no. Esa parte que
sobra es el **residuo**, y hay buenas razones para pensar que los residuos de cientos de
activos se comportan mejor que sus precios: son más estacionarios, no tienen deriva de largo
plazo y su desviación respecto a su nivel habitual tiende a corregirse. La estrategia es
sencilla de enunciar: estima el residuo de cada activo, mide cuánto se ha desviado de su
nivel normal, y apuesta en contra de la desviación, en pequeñas cantidades y en muchos
activos a la vez.

Lo que hace que esto sea un oficio y no una receta son tres cosas:

1. **La neutralidad no es gratis.** Si compras los residuos negativos y vendes los positivos
   sin más, tu cartera tendrá una beta al mercado distinta de cero y, sin querer, estarás
   apostando direccionalmente. Hay que imponer la neutralidad como restricción: suma de pesos
   cero y exposición a cada factor cero.
2. **La escala es minúscula y el coste es brutal.** Cada posición individual es pequeña y el
   residuo medio se mueve muy poco. La rentabilidad bruta se mide en puntos básicos por
   operación, y el diferencial, el impacto y el coste de préstamo de los cortos se la comen
   si el giro es alto.
3. **El crowding.** Cuando una estrategia de este tipo funciona durante años, el capital
   acude. Los residuos que todo el mundo vigila se arbitran más rápido, la rentabilidad cae y,
   peor, las posiciones de todos se parecen: en una liquidación, todo el mundo sale por la
   misma puerta y la caída es común, no diversificada.

Esto no es un pariente lejano de [[pairs-trading|el trading de pares]]: es la versión
industrial. En lugar de un par, cientos de activos; en lugar de una relación económica
elegida a mano, un modelo de factores estimado; en lugar de un diferencial, una cartera de
residuos.

:::figura
fichero: arbitraje-estadistico-coste-se-come-el-bruto
pie: Arriba, el nivel del residuo de un activo y su media móvil: lo que revierte es esa desviación, y con ella se opera. En medio, el s-score que la mide. Abajo está la conclusión de la página: la misma señal, con el mismo acierto, pasa de +0,44 bruto a +0,16 neto con 5 puntos básicos y a −0,11 con 10. El coste de equilibrio de esta señal es 8 pb por unidad de giro, así que todo lo que se pague por encima de esa cifra convierte una estrategia ganadora en perdedora sin tocar el modelo.
fuente: figuras/arbitraje-estadistico-1.py
:::

## Definición formal

Para cada activo `i` y periodo `t`, el modelo de factores descompone el retorno:

:::formula
r_i,t = Σ_k β_i,k · F_k,t + ε_i,t
:::

- `r_i,t` — retorno del activo `i` en el periodo `t`.
- `F_k,t` — retorno del factor común `k` en el periodo `t` (puede ser un factor observable o un
  componente principal extraído de la matriz de retornos).
- `β_i,k` — exposición del activo `i` al factor `k`, estimada por regresión con datos hasta
  `t` (nunca con toda la muestra).
- `ε_i,t` — el residuo: la sorpresa del activo una vez descontados los factores.
- `K` — número de factores. Con `K` factores el riesgo sistemático queda descrito por esas `K`
  direcciones y todo lo demás se trata como idiosincrásico.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `r_i,t` | Retorno del activo `i` en el periodo `t` | tanto por uno por periodo | No es un parámetro que se elija: es el dato. Si se mide en exceso sobre el tipo libre de riesgo, la constante desaparece de la regresión |
| `F_k,t` | Retorno del factor común `k` en el periodo `t` | tanto por uno por periodo | Con factores observables (mercado, sector, tamaño) son datos; con componentes principales hay que elegir cuántos se usan, y esa decisión se toma mirando solo el pasado |
| `β_i,k` | Exposición del activo `i` al factor `k`, estimada por regresión | adimensional | Si el activo tiene beta 1,3, un 1 % del factor le mueve un 1,3 %: por eso la neutralidad se impone sobre `Σ w_i · β_i,k` y no sobre la suma de importes |
| `ε_i,t` | Residuo: la parte del retorno que los factores no explican | tanto por uno por periodo | Es lo único que se opera. Si el modelo de factores explica mucho, el residuo es pequeño y el coste pesa más en proporción |
| `K` | Número de factores comunes | entero | Cada factor añadido recorta el residuo y sube los grados de libertad gastados: con 500 periodos y 12 activos, `K` grande deja el residuo casi vacío y el resultado, sobreajustado |
| `X_i,t` | Nivel acumulado del residuo, `Σ ε_i,s` | unidades de retorno sumadas | **Lo que revierte es este nivel, no `ε`.** Un `X` muy alejado de su media es la señal; confundir uno con otro invierte el signo de la posición |
| `φ` | Persistencia del nivel del residuo (coeficiente del AR(1)) | adimensional, entre 0 y 1 | Más cerca de 1 = vuelve más despacio: la vida media `−ln(2)/ln(φ)` pasa de 8,7 periodos con 0,92 a 34 con 0,98, y con ella el tiempo que hay que aguantar la posición |
| `η_t` | Innovación del nivel del residuo | tanto por uno | Es el ruido que mueve el nivel: si su volatilidad sube, las desviaciones son mayores y también lo es el riesgo de que no vuelvan |
| `s_i` | s-score: `(X_i − media(X_i)) / desv(X_i)` sobre ventana móvil | desviaciones típicas | Es el número que dispara todo. Valores de ±2 son entrada habitual; por encima de ±3 el clip corta el peso para que una sola serie no domine la cartera |
| `w_i` | Peso del activo `i` en la cartera, normalizado a exposición bruta 1 | fracción del bruto | Es proporcional a `−s_i`: cambiar el signo es apostar **a favor** de la desviación, que es justo lo contrario de la idea |
| `Σ w_i` | Suma de los pesos (neutralidad en dólares) | fracción del bruto | Se impone igual a cero. Sin esta restricción la cartera tiene beta 1 al mercado y has dejado de hacer arbitraje |
| `Σ w_i · β_i,k` | Exposición neta al factor `k` | adimensional | Se impone igual a cero para cada `k`. Es la restricción que casi todo el mundo olvida: se puede ser neutral en dólares y tener beta 0,3 |
| `giro` | Exposición recolocada cada periodo, `Σ abs(Δw_i)` | fracción de la exposición bruta | Es el multiplicador del coste: con 5 pb por unidad, un giro medio de 0,43 cuesta el 5,4 % del capital al año. El coste de equilibrio es `alpha bruto / giro` |
:::

Lo que revierte no es el residuo del periodo, sino el **nivel acumulado** del residuo, que es
la desviación de precio que el modelo no explica:

:::formula
X_i,t = Σ (s ≤ t) ε_i,s
:::

`X_i,t` es el precio del residuo, una serie que se modela como un proceso de reversión:

:::formula
X_t = φ · X_t−1 + η_t ,  vida media = −ln(2) / ln(φ)
:::

- `φ` (phi) — persistencia del nivel del residuo. Cuanto más cerca de 1, más lento vuelve.
- `η_t` — innovación del nivel, con media cero.
- El **s-score** es el z-score de ese nivel: `s_i = (X_i − media(X_i)) / desv(X_i)`, calculado
  sobre una ventana móvil.

Y la cartera se construye apostando contra la desviación, con dos restricciones explícitas:

:::formula
w_i ∝ −s_i ,  sujeto a  Σ w_i = 0  y  Σ w_i · β_i,k = 0 para todo k
:::

- `w_i` — peso del activo `i` en la cartera, normalmente con exposición bruta (la suma de los
  valores absolutos de los pesos) normalizada a 1.
- `Σ w_i = 0` — neutralidad en dólares: lo que compras lo financias con lo que vendes. Sin
  esto, tu cartera tiene beta 1 al mercado y has dejado de hacer arbitraje.
- `Σ w_i · β_i,k = 0` — neutralidad a cada factor. Es la restricción que casi todo el mundo
  olvida: se puede ser neutral en dólares y tener una beta de 0,3 al mercado.

## Ejemplo

Doce activos, dos factores comunes y un residuo que revierte con `φ = 0,92`. La exposición
bruta se normaliza a 1, se estiman las betas con una ventana móvil de 60 periodos y se impone
la neutralidad en dólares. Durante 540 periodos fuera de la ventana de estimación:

- Suma de pesos media: −0,000000. La neutralidad en dólares es exacta por construcción.
- Exposición bruta media: 0,9435 (algo menos de 1 porque al restar la media se pierde un poco).
- Beta neta al primer factor: +0,006. Con esto, la parte del mercado que te llega es
  despreciable.
- PnL bruto acumulado: **+0,1765** en unidades de retorno de la cartera.
- Giro medio por periodo: 0,433, es decir, se recoloca el 43 % de la exposición bruta cada
  periodo.
- Coste acumulado con 5 puntos básicos por unidad de girada: **+0,1165**.
- PnL neto: **+0,0600**.

Lee esos números en orden porque cuentan una historia incómoda. El bruto es +0,1765 y el
coste, +0,1165: **dos tercios de la rentabilidad bruta se van en costes**, y eso con un coste
de 5 pb, que en muchos activos es optimista. El dato que de verdad decide es el último: el
**coste de equilibrio es 7,58 pb por unidad de giro**. Por encima de ese coste, la estrategia
pierde dinero aunque el modelo sea perfecto. Ese número se calcula antes de construir nada; si
tu coste real es 10 pb, no hay estrategia que discutir.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(0)
T, N, K = 600, 12, 2
F = rng.normal(0, 0.01, (T, K))                                    # dos factores comunes
B = np.column_stack([rng.normal(0.9, 0.2, N),
                     np.r_[np.full(6, -0.6), np.full(6, 0.6)]])    # exposiciones

# Lo que revierte es el PRECIO del residuo (una desviacion acumulada), no su retorno
X = np.zeros((T, N))
for t in range(1, T):
    X[t] = 0.92 * X[t - 1] + rng.normal(0, 0.003, N)
dX = np.diff(X, axis=0, prepend=np.zeros((1, N)))
R = F @ B.T + dX

ventana = 60
pesos = np.zeros((T, N))
for t in range(ventana, T - 1):
    X_reg = np.column_stack([np.ones(ventana), F[t - ventana:t]])
    beta = np.linalg.lstsq(X_reg, R[t - ventana:t], rcond=None)[0][1:]
    resid = R[t - ventana:t] - F[t - ventana:t] @ beta     # retorno del residuo
    nivel = np.cumsum(resid, axis=0)                       # nivel acumulado del residuo
    s = (nivel[-1] - nivel.mean(axis=0)) / nivel.std(axis=0, ddof=1)
    w = -np.clip(s, -3.0, 3.0)                             # apostamos contra la desviacion
    w = w / np.abs(w).sum()
    pesos[t] = w - w.mean()                                # neutralidad en dolares

usados = np.arange(ventana, T - 1)
bruto = np.array([pesos[t] @ R[t + 1] for t in usados])
giro = np.abs(np.diff(pesos[usados], axis=0)).sum(axis=1)
coste = giro * 0.0005

print("suma de pesos neta      %+.6f" % pesos[usados].sum(axis=1).mean())
print("exposicion bruta         %.4f" % np.abs(pesos[usados]).sum(axis=1).mean())
print("beta neta al factor 1   %+.3f" % (pesos[usados] @ B[:, 0]).mean())
print("pnl bruto acumulado    %+.4f" % bruto.sum())
print("giro medio por periodo   %.3f" % giro.mean())
print("coste acumulado (5 pb)  %+.4f" % coste.sum())
print("pnl neto de costes     %+.4f" % (bruto.sum() - coste.sum()))
print("coste de equilibrio     %.2f pb por unidad de giro" % (1e4 * bruto.sum() / giro.sum()))
# -> suma de pesos neta      +0.000000
# -> exposicion bruta         0.9435
# -> beta neta al factor 1   +0.006
# -> pnl bruto acumulado    +0.1765
# -> giro medio por periodo   0.433
# -> coste acumulado (5 pb)  +0.1165
# -> pnl neto de costes     +0.0600
# -> coste de equilibrio     7.58 pb por unidad de giro
```

El detalle que hace que este bloque sea correcto y no una fábrica de resultados falsos: el
residuo se acumula (`np.cumsum`) antes de calcular el s-score, porque **lo que revierte es el
nivel, no el retorno**. Un proceso AR(1) con coeficiente positivo en los retornos no es
reversión: es persistencia. Si te equivocas ahí, el signo de la posición se invierte y todo lo
demás sobra.

:::claves
- `np.column_stack([np.ones(ventana), F[t - ventana:t]])` pega una columna de unos delante de la matriz de factores. Ese `1` es la constante de la regresión: sin él, `lstsq` ajusta obligando a que la recta pase por el origen y las betas salen sesgadas. Y el índice importa: `[0][1:]` descarta la fila de la constante y se queda solo con las betas de los factores, que es lo que multiplica a `F` después.
- `np.linalg.lstsq(..., rcond=None)[0]` devuelve una **tupla de cuatro elementos** (solución, residuos, rango, valores singulares) y la solución es una matriz de forma `(K+1, N)`, una columna por activo. Desempaquetar mal (`beta = np.linalg.lstsq(...)` sin `[0]`) no da error: da una tupla que fallará más tarde y en otra línea. El rango de la solución es `(1 + K, N)` porque se resuelven los `N` activos de una sola vez.
- `np.diff(X, axis=0, prepend=np.zeros((1, N)))` tiene la misma longitud que `X` gracias a `prepend`: la primera fila queda a cero porque no hay periodo anterior con el que comparar. Sin `prepend`, devuelve `T-1` filas y todo lo que venga después se desalinea una fila respecto a `F` sin dar ningún error. Con `axis=0` se diferencia a lo largo del tiempo; con `axis=1` se restaría dentro de cada instante, que aquí no significa nada.
- `nivel.std(axis=0, ddof=1)` divide entre `n-1` y `nivel.std(axis=0)` entre `n`. Sobre 60 observaciones la diferencia es del 0,8 % y no se nota; con ventanas de 5 periodos el s-score sale hasta un 12 % más pequeño con `ddof=0` y las entradas se disparan antes de lo previsto. El `axis=0` también muerde: cada activo necesita su propia desviación, porque una desviación común a todos convertiría el s-score en una medida del tamaño del activo.
- `w = -np.clip(s, -3.0, 3.0)` hace dos cosas a la vez y las dos cambian el resultado. El `clip` limita el peso máximo: sin él, un s-score de 8 en un solo activo se lleva casi toda la cartera y con ella todo el riesgo. El signo menos es la esencia de la estrategia: si el nivel está por encima de su media, se vende. Quitar ese menos no da un error, da una estrategia direccional que apuesta a que la desviación sigue creciendo.
- `w = w / np.abs(w).sum()` normaliza por la suma de valores absolutos, no por la suma (que es cero). Es lo que fija la exposición bruta a 1 para que el resultado no dependa del número de activos. Y la línea siguiente, `pesos[t] = w - w.mean()`, impone la neutralidad en dólares exacta: después de restar la media, la suma de pesos vale cero por construcción. El precio es que la exposición bruta deja de ser 1 exacta (0,9435 en el ejemplo): se pierde un poco de tamaño para ganar neutralidad.
- El bucle `for t in range(ventana, T - 1)` termina en `T - 1`, no en `T`, porque dentro se usa `R[t + 1]`: la señal se construye con datos hasta `t` y se cobra el retorno de `t+1`. Cambiar ese límite por `T` da un `IndexError` que avisa, pero cambiar `R[t + 1]` por `R[t]` compila, se ejecuta y mide una estrategia que se compra a sí misma el mismo día que decide.
:::

```python verificable
import numpy as np

# El coste de equilibrio se calcula ANTES de mirar la estrategia: es una condicion de viabilidad
for giro, bruto_por_giro in ((0.10, 0.0004), (0.25, 0.0004), (0.43, 0.0004), (0.43, 0.00015)):
    equilibrio_pb = 1e4 * bruto_por_giro
    coste_anual = giro * 252 * 0.0005
    print("giro %.2f  bruto por giro %.2f pb  equilibrio %.2f pb  coste anual a 5 pb %.2f%%"
          % (giro, 1e4 * bruto_por_giro, equilibrio_pb, 100 * coste_anual))
# -> giro 0.10  bruto por giro 4.00 pb  equilibrio 4.00 pb  coste anual a 5 pb 1.26%
# -> giro 0.25  bruto por giro 4.00 pb  equilibrio 4.00 pb  coste anual a 5 pb 3.15%
# -> giro 0.43  bruto por giro 4.00 pb  equilibrio 4.00 pb  coste anual a 5 pb 5.42%
# -> giro 0.43  bruto por giro 1.50 pb  equilibrio 1.50 pb  coste anual a 5 pb 5.42%
```

Ese cuadro es más útil que cualquier backtest: con un bruto de 4 pb por unidad de giro y un
coste de 5 pb, cada unidad que giras destruye 1 pb y la estrategia está muerta aunque el
modelo acierte. Y fíjate en la tercera y la cuarta fila: mismo giro, la mitad de bruto por
giro, y el coste anual idéntico. Lo que cambia entre las dos no es el coste: es si queda algo
después de pagarlo.

## Errores típicos

- **Creer que estar neutral en dólares es estar neutral al mercado.** La neutralidad en dólares
  solo iguala el valor de las posiciones largas y cortas. Si las largas tienen beta 1,3 y las
  cortas 0,9, tu cartera tiene beta 0,2 y en una caída del 10 % pierdes un 2 % sin haber
  apostado a nada. Impón la restricción sobre los factores, no solo sobre el importe.
- **Confundir el retorno del residuo con el nivel del residuo.** Es el error conceptual más
  frecuente y el que cambia el signo de la estrategia. La reversión a la media es una
  propiedad del **precio** del residuo; un AR(1) con coeficiente positivo en sus retornos
  describe persistencia, no reversión.
- **Estimar los factores o las betas con toda la muestra.** Si el componente principal sale de
  la matriz completa de retornos, cada beta que usas contiene información del futuro. Usa
  ventanas móviles, análisis recursivo o un modelo que solo mire hacia atrás. Y cuidado con los
  grados de libertad: número de factores, ventana de estimación, umbral de recorte del s-score
  y regla de salida. Con 500 periodos y 12 activos, cinco parámetros libres ya son demasiados
  para creerte el resultado.
- **Ignorar el coste de préstamo y la disponibilidad de los cortos.** Los residuos más
  negativos suelen estar en activos castigados, pequeños o con poca liquidez, y algunos no se
  pueden vender en corto. Un backtest que asume que sí puede está midiendo una cartera que no
  existe.
- **Analizar la sensibilidad al coste después de haber optimizado.** El orden correcto es:
  estima el bruto por unidad de giro, calcula el coste de equilibrio, y solo entonces mira si
  tu coste real está por debajo. Si empiezas por el backtest, acabarás eligiendo la versión
  con menos giro por casualidad, no por criterio.
- **Suponer que el residuo es estacionario para siempre.** La estacionariedad es un supuesto,
  no un hecho. Si una empresa cambia de negocio o entra en un índice distinto, su relación con
  los factores cambia y el residuo deja de tener nivel al que volver.

:::aviso
La diversificación de esta estrategia es engañosa: puedes tener 500 posiciones y un solo
factor de riesgo, el **riesgo de crowding**. Cuando muchos gestores han construido carteras
parecidas, las liquidaciones son simultáneas y correlacionadas, y una cartera con 500 nombres
se comporta como una sola apuesta. Mide la correlación de tus residuos con los del mercado, no
solo el número de posiciones.
:::

:::practica
enunciado: Tu cartera de residuos tiene un alpha bruto de 1,5 puntos básicos por periodo y un giro de 0,40 de la exposición bruta. Con un coste real de 3 pb por unidad girada, calcula el alpha neto por periodo, el anual (252 periodos) y el coste de equilibrio.
pista: El coste por periodo es giro por coste unitario; el coste de equilibrio, alpha bruto entre giro.
solucion: Coste = 0,40 · 3 = 1,2 pb = 0,00012. Neto = 1,5 − 1,2 = 0,3 pb por periodo, 0,00003; en 252 periodos, 0,00003 · 252 = 0,00756, un 0,76 % anual. Coste de equilibrio = 1,5 / 0,40 = 3,75 pb por unidad de giro: con 3 pb la estrategia sobrevive por poco, y con 5 pb cada unidad girada destruye 1,25 pb.
:::

## Comprueba que lo sabes

:::quiz
p: Normalizas pesos con suma cero y exposición bruta 1, pero las largas tienen beta media 1,4 y las cortas 1,0. ¿Qué has construido?
o: Una cartera neutral al mercado, porque la suma de pesos es cero
o: Una cartera con beta neta positiva, que pierde en las caídas del mercado aunque la selección de residuos sea correcta
o: Una cartera con beta negativa, porque las cortas compensan
a: 2
e: La neutralidad en dólares iguala importes, no sensibilidades. Con beta 1,4 en las largas y 1,0 en las cortas, la cartera tiene una beta neta positiva y sufre cuando el mercado cae. La restricción que falta es la exposición nula a cada factor, no la suma de pesos.
:::

:::quiz
p: El bruto por unidad de giro de tu estrategia es de 4 puntos básicos y tu coste real de ejecución, con diferencial e impacto, es de 6 pb. ¿Qué conclusión es correcta?
o: Hay que optimizar los parámetros hasta que el giro baje lo suficiente
o: La estrategia no es viable con ese coste: el coste de equilibrio está por debajo del coste real
o: Se puede seguir porque el bruto es positivo
a: 2
e: El coste de equilibrio es el bruto por unidad de giro, 4 pb: por encima de ese coste cada operación destruye valor. Bajar el giro cambia lo que pagas en total, pero no cambia que cada unidad girada cueste más de lo que produce. El bruto positivo no dice nada hasta restarle el coste.
:::

:::nota
El enfoque de Avellaneda y Lee usa componentes principales extraídos de la matriz de retornos
en lugar de factores observables, y mide la calidad de la estrategia con el ratio entre el
retorno del residuo y su volatilidad. La idea de fondo es la misma: quitar primero lo común y
operar después lo que queda.
:::
