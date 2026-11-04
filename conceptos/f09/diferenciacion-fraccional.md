---
id: diferenciacion-fraccional
titulo: Diferenciación fraccional
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [estacionariedad, autocorrelacion-acf-pacf, test-adf-kpss, retornos-logaritmicos]
tags: [estacionariedad, memoria, series-temporales, lopez-de-prado]
resumen: Diferenciar con orden fraccionario hace estacionaria una serie conservando su memoria: gana el test de raíz unitaria sin perder la correlación con el pasado.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 5", "Hosking (1981), 'Fractional Differencing'"]
---

## En una frase

Diferenciar una serie con un orden `d` cualquiera entre 0 y 1 (no solo con 0 o con 1) permite
hacerla estacionaria perdiendo la mínima memoria posible: se elige el `d` más pequeño que pasa el
contraste de raíz unitaria y se conserva el resto de la información del nivel.

## La idea

Casi todo modelo estadístico exige que la serie sea estacionaria: que su media y su varianza no
se vayan a otra parte con el tiempo. Los precios no lo son, y la solución de manual es
diferenciar: pasar de precios a [[retornos-logaritmicos|retornos logarítmicos]]. La serie
resultante es estacionaria y cómoda, pero tiene un problema que se nota cuando intentas predecir
algo con ella: casi no queda nada del pasado. La autocorrelación del retorno diario a un día es
diminuta y a veinte días es prácticamente cero. Has tirado la memoria entera para quedarte con el
ruido.

Y la memoria valía algo. «El precio está un 15 % por encima de su media de 200 sesiones» es una
variable de nivel, y hay estrategias que viven justo de eso. Si tu única herramienta de
estacionariedad es diferenciar una vez, esa información no llega al modelo.

La diferenciación fraccional consiste en aplicar el operador de diferencias con exponente `d`
real, no entero. La idea matemática es vieja y sencilla: `(1 − B)^d`, con `B` el operador de
retardo, se puede desarrollar como una serie infinita de coeficientes para cualquier `d`. Con
`d = 1` los coeficientes son `1, −1` y poco más: diferenciación clásica, memoria cero. Con
`d = 0` el único coeficiente es `1`: no pasa nada, serie original, memoria entera y ninguna
estacionariedad. Con `d = 0,4` aparecen decenas de coeficientes que decaen despacio, y el
resultado es una serie que pasa el contraste de raíz unitaria pero sigue correlacionada consigo
misma a veinticinco rezagos.

La forma de elegir `d` es la parte importante y la que se hace mal: **no se elige por el
rendimiento de la estrategia**, se elige por el criterio de estacionariedad. Se baja `d` desde 1
en pasos pequeños y se toma el menor valor cuyo [[test-adf-kpss|contraste de raíz unitaria]]
rechace la hipótesis de raíz unitaria al nivel que hayas fijado (el 5 %, por ejemplo). Ese `d` es
el que conserva más memoria con la estacionariedad garantizada. Si lo eliges probando el que más
gana en el backtest, has convertido un parámetro estadístico en un ejercicio de
[[data-snooping-y-multiple-testing|búsqueda sobre ruido]].

:::aviso
La serie transformada no es un precio ni un retorno, y no se interpreta como tal. Sus valores son
combinaciones ponderadas de cotizaciones antiguas; sirven para alimentar un modelo, no para
leerlos en un titular.
:::

## Definición formal

Con `B` el operador de retardo (`B · X_t = X_{t−1}`) y `d` un número real:

:::formula
(1 − B)^d = Σ_{k=0}^{∞} ω_k B^k        ω_0 = 1,   ω_k = − ω_{k−1} · (d − k + 1) / k
:::

- `d` — orden de diferenciación. `d = 0` no transforma nada; `d = 1` es la primera diferencia.
- `ω_k` — peso del rezago `k`. La recurrencia es todo lo que hace falta para calcularlos; no hay
  que evaluar factoriales ni funciones gamma.
- `K` — número de pesos que se conservan. La serie es infinita, así que se trunca cuando
  `|ω_k| < τ`, con `τ` un umbral pequeño (`10⁻³` para series cortas, `10⁻⁵` para series largas).

La serie transformada es la convolución truncada:

:::formula
X̃_t = Σ_{k=0}^{K} ω_k · X_{t−k}        para t ≥ K
:::

- `X̃_t` — valor transformado. Solo existe a partir de `t = K`: las primeras `K` observaciones se
  pierden, y con `d` pequeño y series cortas eso puede ser un mordisco serio.
- `Σ ω_k` — la suma de los pesos es exactamente 0 para la serie infinita con cualquier `d > 0`, y
  eso es lo que elimina el nivel. Con la serie truncada queda un residuo positivo, y ese residuo
  es justamente la memoria que se conserva. Para `d = 0,4` con `τ = 10⁻³` (55 pesos) la suma vale
  0,136; para `d = 1` vale 0 exactamente, y de ahí que la primera diferencia no guarde nada del
  nivel.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `B` | El operador de retardo: `B · X_t = X_{t−1}` | — | No se elige, es notación: sirve para escribir el filtro como un polinomio |
| `d` | El orden de diferenciación | adimensional, en la práctica entre 0 y 1 | Con `d` pequeño se conserva más memoria y el filtro se alarga; `d = 1` es el retorno de siempre, estacionario y sin nada del nivel |
| `ω_k` | El peso del rezago `k` en el desarrollo de `(1 − B)^d` | adimensional | Alternan de signo y decaen despacio: el primero es 1, el segundo `−d`; esa cola larga es la memoria |
| `K` | Cuántos pesos se conservan antes de truncar | número de rezagos | Sube al bajar `τ` o al bajar `d`, y cada peso extra se come una observación del principio de la serie |
| `τ` | El umbral de truncamiento: se corta cuando el valor absoluto de `ω_k` baja de `τ` | adimensional | Más pequeño es más fiel y más largo (con `τ = 10⁻⁵` y `d = 0,4` hacen falta 1.458 pesos); más grande deja demasiado nivel y el contraste de raíz unitaria vuelve a fallar |
| `X̃_t` | El valor transformado | las de la serie, aunque no se interpreta como precio | Solo existe a partir de `t = K`; con series cortas y `d` pequeño el mordisco inicial es serio |
| `Σ ω_k` | La suma de los pesos truncados | adimensional | Mide cuánto nivel sobrevive: 0,136 con `d = 0,4` y `τ = 10⁻³`, y 0 exacto con `d = 1` |
:::

Con `0 < d < 1` los pesos alternan de signo y su valor absoluto decae despacio: el primero es 1,
el segundo `−d`, el tercero `−d(1−d)/2`… Esa cola larga es la memoria; la alternancia de signos es
lo que hace estacionaria la serie.

:::figura
fichero: fracdiff-memoria-y-nivel
pie: Arriba, la autocorrelación de la misma serie con tres órdenes: sin diferenciar no baja (no es estacionaria), `d = 1` cae dentro de la banda de ruido en el primer rezago (memoria tirada) y `d = 0,4` se queda en 0,192 a 25 rezagos, que es el compromiso que se busca. Abajo, la suma de los pesos truncados, que es el nivel que sobrevive: 0,136 con `d = 0,4` y 0 exacto con `d = 1`. El `d` que se elige es el menor que pasa el contraste, no el que más gana en el backtest.
fuente: figuras/diferenciacion-fraccional-1.py
:::

## Ejemplo

Recurrencia a mano para `d = 0,4`:

- `ω_0 = 1`.
- `ω_1 = −1 · (0,4 − 1 + 1) / 1 = −0,4`.
- `ω_2 = −(−0,4) · (0,4 − 2 + 1) / 2 = 0,4 · (−0,6) / 2 = −0,12`.
- `ω_3 = −(−0,12) · (0,4 − 3 + 1) / 3 = 0,12 · (−1,6) / 3 = −0,064`.
- `ω_4 = −(−0,064) · (0,4 − 4 + 1) / 4 = 0,064 · (−2,6) / 4 = −0,0416`.

Con `τ = 10⁻³` la cola llega hasta `K = 55`; con `d = 1` son dos pesos (`1, −1`) y con `d = 0` uno
solo (`1`). Es decir: cuanto más pequeña es `d`, más largo es el filtro y más observaciones
iniciales se pierden.

Aplicado a cinco cierres `100, 101, 99, 102, 103` con los cinco primeros pesos (`ω` de 1 a
−0,0416), el valor transformado en la última barra es
`1·103 − 0,4·102 − 0,12·99 − 0,064·101 − 0,0416·100 = 39,7`, mientras que la primera diferencia
en esa misma barra vale `103 − 102 = 1,0`. El 39,7 no significa nada por sí solo, pero su tamaño
delata lo que está pasando: la suma de esos cinco pesos es 0,374, así que el nivel del precio
entra en el valor transformado con un peso del 37 %. Con los 55 pesos la suma baja a 0,136, y con
`d = 1` a cero.

La tabla que hay que mirar para elegir `d` es la del compromiso: autocorrelación a distintos
rezagos (memoria que se conserva) frente a la desviación típica de la serie (signo de estar
diferenciando de más).

## Código

```python verificable
import numpy as np

def pesos_fracd(d, umbral=1e-3):
    """Pesos w_k de (1-B)^d, truncados cuando el valor absoluto baja del umbral."""
    w, k = [1.0], 1
    while True:
        siguiente = -w[-1] * (d - k + 1) / k
        if abs(siguiente) < umbral:
            break
        w.append(siguiente)
        k += 1
    return np.array(w)

for d in (0.0, 0.4, 1.0):
    w = pesos_fracd(d)
    print(f"d={d:.1f}  pesos {w.size:>3}  primeros {np.round(w[:5], 4).tolist()}")
# d=0.4 -> 55 pesos, los cinco primeros son [1.0, -0.4, -0.12, -0.064, -0.0416]
# d=1.0 -> 2 pesos, [1.0, -1.0]
```

:::claves
- La función construye una **lista** de Python y solo al final la convierte con `np.array(w)`. Es lo razonable aquí: una lista crece barata, mientras que un array de NumPy no se puede alargar sin copiarlo entero en cada `append`.
- La recurrencia usa `w[-1]`, el último peso calculado: los coeficientes se generan en cadena, cada uno a partir del anterior. Por eso no hace falta evaluar factoriales ni funciones gamma, y por eso un signo cambiado produce una serie de pesos que parece razonable y no lo es.
- En Python 3 la división `/` es siempre real, así que con `d = 0.4` los pesos salen en coma flotante sin convertir nada. Con `//` (división entera) el filtro sería otro distinto y el resultado no daría error: daría números.
- El bucle es `while True` y termina solo por la condición de truncamiento. Si el valor absoluto del peso no bajara (por ejemplo con un `d` negativo), el bucle no acabaría nunca; el guardia que falta es un límite para `k`.
- El peso que no llega al umbral **no se añade**: `w.size` es el número de pesos conservados, y ese mismo número es el que después hay que recortar al principio de la serie transformada. Si no se recortan esas filas, las fechas quedan desalineadas.
- Con `d = 0.0` el primer candidato vale `-1.0 * (0 - 1 + 1) / 1 = 0`, que es menor que el umbral, así que la función devuelve un único peso y la serie no se transforma. Es la comprobación rápida de que la recurrencia está bien escrita: `pesos_fracd(1.0)` debe dar dos pesos y `pesos_fracd(0.0)` uno.
:::

```python verificable
import numpy as np

def pesos_fracd(d, umbral=1e-3):
    w, k = [1.0], 1
    while True:
        s = -w[-1] * (d - k + 1) / k
        if abs(s) < umbral:
            break
        w.append(s)
        k += 1
    return np.array(w)

def acf(x, lag):
    x = x - x.mean()
    return float(np.dot(x[:-lag], x[lag:]) / np.dot(x, x))

rng = np.random.default_rng(0)
serie = np.cumsum(rng.normal(0.05, 1.0, size=800))   # paseo con deriva

# Al subir d la serie se vuelve estacionaria (el acf decae) pero pierde memoria (acf lejano).
print("  d   acf(1)  acf(5)  acf(25)  desviacion")
for d in (0.0, 0.2, 0.4, 0.6, 1.0):
    w = pesos_fracd(d)
    y = np.convolve(serie, w, "full")[w.size - 1:][-700:]
    print(f"{d:>4.1f}   {acf(y, 1):>6.3f}  {acf(y, 5):>6.3f}   {acf(y, 25):>6.3f}  "
          f"{y.std():>9.3f}")
# con d=1.0 el acf a 25 rezagos es 0.003; con d=0.4 todavia vale 0.192
```

## Errores típicos

- **Diferenciar siempre con `d = 1` y dar por hecho que es lo correcto.** Es estacionario, sí,
  pero destruye la memoria y con ella variables de nivel que pueden ser justamente la señal. Si tu
  modelo funciona con retornos, perfecto; si necesitabas el nivel, lo has tirado sin darte cuenta.
- **Elegir `d` por el resultado del backtest.** Probar 40 valores de `d` y quedarte con el que más
  gana es selección sobre ruido, y además convierte un parámetro que debería fijarse antes de
  mirar el rendimiento en otro grado de libertad. Elige `d` con el contraste de raíz unitaria y
  apúntalo.
- **Calcular los pesos con toda la muestra.** Aunque la transformación no mire el futuro
  (solo usa rezagos), la **elección** de `d` y del umbral `τ` sí se hace con datos. Esa decisión
  debe tomarse en el tramo de entrenamiento, y la validación hacerse después con ese `d` fijado.
  Si no, es [[sesgo-de-mirar-al-futuro|mirar al futuro]] por la puerta de atrás.
- **Truncar con un umbral demasiado alto.** Si te quedas con 5 pesos porque «total, el resto es
  pequeño», la suma de los pesos se queda en 0,37 y la serie transformada conserva mucho nivel:
  el contraste de raíz unitaria volverá a decirte que no es estacionaria. `τ` se elige mirando
  cuántos pesos necesitas para que el contraste pase, no por comodidad.
- **Truncar con un umbral demasiado bajo en series cortas.** Con `τ = 10⁻⁵` y `d = 0,4` hacen
  falta 1.458 pesos: con 1.500 observaciones te quedas sin serie. Cuanto más pequeño es `d`, más
  largo es el filtro y más datos hay que sacrificar al principio.
- **Desalinear los índices después de filtrar.** `X̃` empieza en `t = K`, no en `t = 0`. Si pegas
  la serie transformada a las etiquetas sin recortar las primeras `K` filas, estás mezclando
  fechas y el modelo aprende con el calendario torcido.

:::practica
enunciado: Con d = 0,5, calcula los pesos ω₁ a ω₃ con la recurrencia ω_k = −ω_{k−1} · (d − k + 1) / k y el valor transformado de la última barra de los cierres 100, 101, 102, 103.
pista: El cociente (d − k + 1) / k vale −0,5, −0,5 y −1,5 / 3 para k = 1, 2 y 3, y el signo de delante alterna.
solucion: ω₁ = −0,5; ω₂ = 0,5 · (−0,5) / 2 = −0,125; ω₃ = 0,125 · (−1,5) / 3 = −0,0625. Con ω₀ = 1, X̃ = 103 − 0,5 · 102 − 0,125 · 101 − 0,0625 · 100 = 33,125. Los cuatro pesos suman 0,3125: el filtro conserva un 31 % del nivel, mientras que la primera diferencia de esa barra, 103 − 102 = 1, no guarda nada.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el criterio correcto para elegir el orden de diferenciación `d`?
o: El valor de `d` que maximiza el rendimiento de la estrategia en el backtest
o: El menor `d` cuyo contraste de raíz unitaria rechace la no estacionariedad, porque es el que conserva más memoria
o: Siempre `d = 1`, porque es el único valor que garantiza estacionariedad
a: 2
e: El objetivo es el compromiso: estacionariedad garantizada con la máxima memoria retenida. Por eso se baja desde 1 hasta encontrar el primer valor que pasa el contraste. Elegirlo por el backtest convierte el parámetro en una selección sobre ruido, y `d = 1` es estacionario pero tira toda la memoria.
:::

:::quiz
p: Con `d = 0,4` y umbral `10⁻³` se conservan 55 pesos cuya suma es 0,136. ¿Qué implica ese 0,136?
o: Que el 13,6 % de las observaciones se pierden al principio de la serie
o: Que la serie transformada conserva un 13,6 % del nivel, y esa es exactamente la memoria que se ha decidido mantener
o: Que el error de la transformación es del 13,6 % y hay que reducir el umbral
a: 2
e: La suma de los pesos de la serie infinita es cero para cualquier `d` mayor que cero, y es lo que elimina el nivel. Al truncar queda un residuo: 0,136 para `d = 0,4` y 0 exactamente para `d = 1`. Ese residuo es la memoria conservada, no un error; si fuera un error, la solución sería bajar `τ`, lo que alargaría el filtro.
:::

:::trampa
Si tu contraste de estacionariedad sigue fallando con `d = 0,9`, el problema no es el orden de
diferenciación: mira si la serie tiene un cambio de tendencia, un salto por dividendo o un
periodo con datos repetidos. Ningún `d` arregla una serie mal construida.
:::
