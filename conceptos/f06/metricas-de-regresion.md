---
id: metricas-de-regresion
titulo: Métricas de regresión
fase: 6
nivel: básico
rutas: [core, ds]
prerequisitos: [medidas-de-centralidad, medidas-de-dispersion]
tags: [evaluacion, regresion, error, metricas]
resumen: MAE, MSE, RMSE, MAPE y R cuadrado: qué mide cada una, en qué unidades está y en qué casos engaña.
fuentes: ["Willmott y Matsuura (2005), 'Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance'", "Hyndman y Koehler (2006), 'Another look at measures of forecast accuracy'"]
---

## En una frase

Todas las métricas de regresión resumen la distancia entre lo que predijiste y lo que pasó, y se
diferencian en una sola decisión: si esa distancia se mide en unidades del objetivo (MAE, RMSE),
en porcentaje (MAPE) o contra lo que haría un predictor tonto (R²).

## La idea

Un modelo de precios de vivienda se equivoca en −8.000 € en un piso y en +8.000 € en otro. Si
sumas los errores, se cancelan y te sale cero: un modelo perfecto. Por eso las métricas que miden
el tamaño del error no usan los errores con su signo. Las tres familias son:

- **Valor absoluto (MAE):** cada error pesa lo que mide. Un error de 10.000 € pesa diez veces
  más que uno de 1.000 €. La métrica te habla en euros, que es lo que entiende tu jefe.
- **Cuadrado (MSE, RMSE):** un error de 10.000 € pesa cien veces más que uno de 1.000 €. Esto
  tiene una consecuencia enorme: el modelo que minimiza el error cuadrático se esfuerza por
  evitar los desastres y acepta muchos errores pequeños a cambio. Es lo que quieres si un fallo
  grande te arruina, y lo que no quieres si todos los errores valen lo mismo.
- **Relativo (MAPE):** mide el error como porcentaje del valor real. Así puedes comparar el
  error de predecir pisos de 100.000 € con el de predecir pisos de 900.000 €, pero castigas
  muchísimo más los errores en los valores pequeños.

El `RMSE` es simplemente la raíz del `MSE`, y sirve para volver a las unidades del objetivo: un
MSE de 160.000.000 en euros al cuadrado no dice nada; su raíz, 12.649 €, se lee de inmediato.
Esa es la razón de que casi todo el mundo reporte RMSE y no MSE, aunque el modelo se entrene
minimizando MSE.

Y luego está el `R²`, que no mide el error en absoluto: compara tu modelo contra el predictor
más tonto posible, que es decir siempre la media. Un `R² = 0` significa «igual que predecir la
media» y un `R²` negativo significa «peor que predecir la media», cosa que ocurre más de lo que
la gente cree. Su problema es que **siempre sube** al añadir variables, aunque sean ruido, y por
eso existe la versión ajustada.

:::figura
fichero: regresion-mae-y-rmse
pie: A la izquierda, las cinco viviendas del ejemplo: cada raya roja es un residuo y la diagonal es acertar. Los cuatro errores de 10 se compensan a la vista, pero el de 20 en la casa de 300 es el que decide: el MAE se queda en 12,0 y el RMSE sube a 12,6. A la derecha se ve por qué: con cuatro errores fijos de 1 y uno que crece, el MAE sube en línea recta y el RMSE se dispara al cuadrado (4,6 frente a 2,8 cuando el grande vale 10). Conclusión: elige la métrica antes de ver los resultados; si un fallo grande te arruina, es el RMSE, y si todos los errores te cuestan lo mismo, el MAE.
fuente: figuras/metricas-de-regresion-1.py
:::

## Definición formal

Con `n` observaciones, `yᵢ` el valor real, `ŷᵢ` el predicho y `eᵢ = yᵢ − ŷᵢ` el residuo:

:::formula
MAE = (1/n) · Σᵢ |eᵢ|              MSE = (1/n) · Σᵢ eᵢ²
:::

:::formula
RMSE = √MSE                        MAPE = (1/n) · Σᵢ |eᵢ / yᵢ|
:::

- `n` — número de observaciones. `Σᵢ` — suma sobre todas ellas.
- El `MAE` está en las unidades del objetivo (euros, grados, unidades vendidas).
- El `MSE` está en esas unidades **al cuadrado**, y por eso casi nunca se interpreta directo.
- El `RMSE` vuelve a las unidades originales. Se cumple siempre `RMSE ≥ MAE`, y solo son iguales
  si todos los errores tienen el mismo tamaño.
- El `MAPE` es adimensional; multiplicado por 100 se lee en porcentaje. Es indefinido si algún
  `yᵢ` vale cero, y se dispara si algún `yᵢ` es muy pequeño.

:::formula
R² = 1 − SS_res / SS_tot,  con SS_res = Σᵢ eᵢ²  y  SS_tot = Σᵢ (yᵢ − ȳ)²
:::

:::formula
R²_ajustado = 1 − (1 − R²) · (n − 1) / (n − k − 1)
:::

- `ȳ` — la media de los valores reales; `SS_tot` es la variabilidad total del objetivo.
- `SS_res` — la parte que tu modelo no explica. Si es mayor que `SS_tot`, el `R²` sale negativo.
- `k` — número de variables explicativas del modelo. El `R²_ajustado` resta un poco por cada
  variable añadida, así que solo sube si la variable nueva aporta más de lo que cuesta.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de observaciones | casos | Estabiliza las métricas: con pocos datos el R² sale optimista por construcción |
| `yᵢ` | El valor real de la observación `i` | las del objetivo (€, grados, unidades) | Es el dato: si crece la escala del objetivo, crecen el MAE y el RMSE con ella |
| `ŷᵢ` | El valor que predijo el modelo | las del objetivo | Se aleja del real en la dirección que el modelo se equivoca |
| `eᵢ` | El residuo con signo, `yᵢ − ŷᵢ` | las del objetivo | Si su media no está cerca de 0, el modelo sobreestima o subestima de forma sistemática |
| `MAE` | Media del valor absoluto de los residuos | las del objetivo | Sube en proporción a cualquier error, sea grande o pequeño |
| `MSE` | Media de los residuos al cuadrado | las del objetivo, al cuadrado | Sube mucho más deprisa que el MAE cuando el error grande crece |
| `RMSE` | La raíz del MSE, para volver a las unidades del objetivo | las del objetivo | Sube más rápido que el MAE; siempre `RMSE ≥ MAE` |
| `MAPE` | Media del error en proporción al valor real | adimensional (×100 se lee en %) | Se dispara si algún `yᵢ` es pequeño, y no existe si alguno vale 0 |
| `ȳ` | La media de los valores reales | las del objetivo | Aumenta la variabilidad total del objetivo; no depende del modelo |
| `SS_res` | Suma de los residuos al cuadrado | al cuadrado | Es lo que el modelo no explica: cuanto más alto, peor R² |
| `SS_tot` | Suma de las desviaciones de cada real respecto a su media | al cuadrado | Es la variabilidad total; si `SS_res` la supera, el R² sale negativo |
| `R²` | Proporción de la variabilidad del objetivo que explica el modelo | adimensional, entre −∞ y 1 | Sube al añadir variables aunque sean ruido puro |
| `R²_ajustado` | El R² penalizado por el número de variables | adimensional | Sube solo si la variable nueva aporta más de lo que cuesta |
| `k` | Número de variables explicativas | variables | Baja el R² ajustado; con `k ≥ n − 1` la fórmula deja de tener sentido |
:::

## Ejemplo

Cinco viviendas, precio real y predicción en miles de euros:

```
real  100  150  200  250  300
pred  110  140  210  240  320
```

Los residuos son `−10, +10, −10, +10, −20` (real menos predicción):

- `MAE = (10 + 10 + 10 + 10 + 20) / 5 = 60 / 5 = 12,0` mil euros.
- `MSE = (100 + 100 + 100 + 100 + 400) / 5 = 800 / 5 = 160`.
- `RMSE = √160 = 12,649` mil euros. Fíjate en que el RMSE (12,649) es mayor que el MAE (12,0)
  porque el error de 20 pesa mucho más al cuadrado.
- `MAPE = (0,10 + 0,0667 + 0,05 + 0,04 + 0,0667) / 5 = 0,0647`, es decir, un 6,47 % de error
  medio relativo. El mismo error absoluto de 10 pesa un 10 % sobre la vivienda de 100 y un 4 %
  sobre la de 250.
- `SS_tot = 10000 + 2500 + 0 + 2500 + 10000 = 25.000` y `SS_res = 800`, así que
  `R² = 1 − 800/25.000 = 0,968`: el modelo explica el 96,8 % de la variabilidad de los precios.

Ese 0,968 impresiona, y conviene mirarlo con calma: con cinco casas y precios que ya venían
ordenados, casi cualquier recta da un `R²` alto. Con `k = 3` variables y `n = 5`, el R² ajustado
baja a `1 − 0,032 · 4/1 = 0,872`: cada variable nueva cuesta caro cuando hay pocos datos.

## Código

```python verificable
import numpy as np

# Cinco viviendas: precio real y prediccion, en miles de euros
real = np.array([100.0, 150.0, 200.0, 250.0, 300.0])
pred = np.array([110.0, 140.0, 210.0, 240.0, 320.0])

error = real - pred                      # residuos con signo
# .mean() de un array de NumPy divide entre n (no entre n-1): para un error medio es lo
# que se quiere. np.abs se aplica elemento a elemento antes de promediar.
mae = np.abs(error).mean()
rmse = np.sqrt((error ** 2).mean())      # error ** 2 tambien es elemento a elemento
# Aqui se divide cada error entre SU valor real, y solo despues se promedian los cocientes.
mape = (np.abs(error) / real).mean()
# SS_res = suma de los residuos al cuadrado; SS_tot = variabilidad respecto a la media.
r2 = 1 - (error ** 2).sum() / ((real - real.mean()) ** 2).sum()

print(f"MAE  {mae:.4f}")    # -> 12.0000
print(f"MSE  {(error ** 2).mean():.4f}")   # -> 160.0000
print(f"RMSE {rmse:.4f}")   # -> 12.6491
print(f"MAPE {mape:.4f}")   # -> 0.0647
print(f"R2   {r2:.4f}")     # -> 0.9680
```

:::claves
- `real - pred` resta **elemento a elemento** y devuelve un array nuevo: no toca ni `real` ni `pred`. El residuo conserva el signo, y el signo solo se pierde al aplicar `np.abs` o al elevar al cuadrado.
- `.mean()` de un array de NumPy divide entre `n`, no entre `n − 1` (su `ddof` es 0). Para una media de errores es justo lo que quieres, pero si copias esa llamada para una varianza te sale un número más pequeño que el de `pandas`, que usa `ddof=1`.
- `error ** 2` eleva al cuadrado cada elemento, no multiplica el array por sí mismo de otra forma. `np.sqrt` del resultado devuelve el RMSE ya en las unidades del objetivo, porque el cuadrado se deshace.
- `(np.abs(error) / real)` divide cada error entre el valor real **de esa misma fila**. Por eso el MAPE no es una media de errores absolutos: un error de 10 pesa un 10 % sobre la casa de 100 y un 4 % sobre la de 250.
- `real.mean()` dentro del `SS_tot` se calcula una sola vez y se resta a los cinco valores: es una resta con difusión (*broadcasting*), no un bucle.
- `np.full(5, 50.0)` del segundo bloque construye un array de cinco 50.0 con el tipo que le digas. Sirve para fabricar a mano el predictor constante que hace falta para ver un R² negativo; `np.zeros` y `np.ones` son los mismos primos de esta familia.
:::

```python verificable
import numpy as np

# Un unico error grande dispara el RMSE y apenas mueve el MAE
errores = np.array([1.0, 1.0, 1.0, 1.0, 10.0])
print(f"MAE  {np.abs(errores).mean():.3f}")            # -> 2.800
print(f"RMSE {np.sqrt((errores ** 2).mean()):.3f}")    # -> 4.561

# El R2 puede ser negativo: aqui el modelo predice 50 para todo y la serie va de 10 a 50
real = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
# np.full(5, 50.0) es un array de cinco 50.0: el «predictor constante» mas tonto posible.
pred = np.full(5, 50.0)
r2 = 1 - ((real - pred) ** 2).sum() / ((real - real.mean()) ** 2).sum()
print(f"R2 de un predictor constante {r2:.1f}")        # -> -2.0
```

## Errores típicos

- **Comparar métricas entre problemas distintos.** Un RMSE de 12 no significa lo mismo en euros
  que en miles de euros, y dos R² sobre conjuntos con distinta variabilidad tampoco son
  comparables porque el `SS_tot` cambia. Si necesitas comparar, usa una métrica relativa o
  normaliza el objetivo.
- **Reportar MSE porque es lo que optimiza el modelo.** Un MSE de 160 no dice nada a nadie.
  Reporta RMSE y, si el error no es simétrico, también MAE.
- **Usar MAPE con valores pequeños o ceros.** Si algún real vale 0, la métrica no existe; si hay
  valores de 0,5, un error de 0,5 es un 100 %. Y es asimétrica: subestimar está acotado por un
  100 %, sobreestimar no tiene tope.
- **Presumir de R² alto sin mirar el tamaño de la muestra.** Añadir variables sube el R² siempre.
  Con `n` pequeño y muchas variables, el R² es optimista por construcción: usa el ajustado y
  valida sobre datos nuevos.
- **Elegir la métrica después de ver los resultados.** MAE y RMSE ordenan los modelos de forma
  distinta y no hay uno «mejor»: elige según el problema. Si un error grande es catastrófico,
  RMSE; si todos los errores cuestan lo mismo, MAE. Decídelo antes de comparar.
- **Ignorar el sesgo medio.** MAE y RMSE no distinguen entre equivocarse mucho en unas filas y
  equivocarse siempre en la misma dirección. Calcula la media de los residuos con signo: si no
  está cerca de cero, tu modelo sobreestima o subestima de forma sistemática.

:::practica
enunciado: Cuatro viviendas con precio real 10, 20, 30 y 40 mil euros y predicción 12, 18, 33 y 37. Calcula MAE, RMSE y R².
pista: Saca los residuos con signo; MAE y RMSE se calculan sobre su valor absoluto y su cuadrado, y el R² compara los residuos al cuadrado con la variabilidad total respecto a la media.
solucion: Residuos: −2, +2, −3, +3. MAE = (2+2+3+3)/4 = 10/4 = 2,5 mil €. MSE = (4+4+9+9)/4 = 26/4 = 6,5, y RMSE = √6,5 = 2,55 mil €, mayor que el MAE porque los errores de 3 pesan más al cuadrado. La media real es 25, con SS_tot = 225+25+25+225 = 500 y SS_res = 26, así que R² = 1 − 26/500 = 0,948: explica el 94,8 % de la variabilidad.
:::

## Comprueba que lo sabes

:::quiz
p: Dos modelos tienen el mismo MAE pero uno tiene un RMSE mucho mayor. ¿Qué significa?
o: Que ese modelo tiene errores más desiguales, con algún caso muy mal predicho
o: Que ese modelo es peor en todos los casos
o: Que el RMSE está mal calculado, porque siempre debe coincidir con el MAE
a: 1
e: El RMSE eleva al cuadrado y por eso lo dominan los errores grandes. Con el mismo error medio absoluto, un RMSE mayor indica más dispersión en los errores. RMSE y MAE solo coinciden cuando todos los errores tienen el mismo tamaño.
:::

:::quiz
p: Un modelo obtiene R² = 0,98 sobre 20 viviendas con 8 variables explicativas. ¿Qué comprobación es más urgente?
o: Cambiar a una métrica relativa, porque el R² no sirve
o: Mirar el R² ajustado y validar en datos nuevos, porque con 20 casos y 8 variables el R² está inflado
o: Nada, un R² de 0,98 es un modelo excelente por definición
a: 2
e: El R² sube con cada variable añadida, aporte o no. Con 20 observaciones y 8 variables, el ajustado y, sobre todo, el error sobre datos que el modelo no ha visto, son la única prueba real.
:::
