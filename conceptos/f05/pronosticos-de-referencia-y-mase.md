---
id: pronosticos-de-referencia-y-mase
titulo: Pronósticos de referencia y MASE
fase: 5
nivel: básico
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, metricas-de-regresion]
tags: [series-temporales, pronostico, metricas, referencia]
resumen: El naive, el naive estacional y la deriva son el listón que hay que batir antes de creerse un modelo, y el MASE es la métrica que pone ese listón en 1.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', caps. 3 y 5", "Hyndman y Koehler (2006), 'Another look at measures of forecast accuracy'", "Makridakis et al. (1982), 'The accuracy of extrapolation (time series) methods'"]
---

## En una frase

Antes de creerte un modelo, tienes que batir a los tres pronósticos de referencia (repetir el
último dato, repetir el mismo periodo del año pasado y seguir la recta), y el **MASE** es la
métrica que pone ese listón en 1.

## La idea

Imagina que apuestas quién gana una carrera y solo hay dos corredores: tu modelo, con sus
ecuaciones, y un tipo que dice «mañana hará lo mismo que hoy». Si gana el tipo, tu modelo no vale
para nada por muy bonito que sea. Ese tipo tiene nombre: el **método de referencia** (en inglés,
*benchmark*), y hay tres versiones que se usan siempre.

- **Naive (ingenuo).** El pronóstico es el último valor observado. Es lo mejor que se puede hacer
  cuando la serie es un paseo aleatorio, como un precio de bolsa.
- **Naive estacional.** El pronóstico es el valor del mismo periodo del ciclo anterior: para marzo
  de 2027, lo que pasó en marzo de 2026. Con un patrón anual fuerte, este es el rival a batir.
- **Deriva (drift).** Se traza la recta entre el primer valor y el último y se prolonga. Sirve
  cuando la serie sube o baja de forma constante y no tiene estacionalidad.

El rival correcto **depende del horizonte**: a un paso el naive es durísimo, porque la serie
todavía está cerca del último dato; a doce pasos repite un valor viejo y cualquier serie con ciclo
anual se le escapa, así que ahí el rival es el naive estacional. Comparar tu modelo de doce pasos
con el naive a un paso es hacer trampa.

Y queda el problema de la métrica. Si tu MAE es 12,9 euros, ¿es bueno o malo? Depende de si la
serie vende 15 o 15.000 euros al mes. El MAPE lo arregla dividiendo entre el valor real, pero se
dispara con valores pequeños y **no existe** si alguno es cero, que en ventas es lo más normal.

Para eso está el **MASE** (*mean absolute scaled error*), que divide el error medio entre el error
que comete el propio ingenuo dentro de la muestra. No tiene unidades y se lee de un vistazo:
**MASE = 1** significa que tu modelo empata con el ingenuo, o sea, que no ha aportado nada; **por
debajo de 1** lo bate; y un **8** significa que tu error es ocho veces el suyo. El **sMAPE** es la
otra métrica relativa de los informes: también está libre de escala y acotada entre 0 % y 200 %,
pero es **asimétrica** (pasarse un 50 % cuesta 40 % y quedarse un 50 % corto cuesta 66,7 %, con el
mismo error absoluto) y no trae referencia incorporada, así que un 4,7 % no te dice si es bueno.

## Definición formal

Con la serie `y_1, …, y_T`, el periodo estacional `m` (12 con datos mensuales, 1 si no hay
estacionalidad) y el horizonte `h`:

:::formula
ingenuo:  ŷ_{T+h} = y_T          estacional:  ŷ_{T+h} = y_{T+h−m}          deriva:  ŷ_{T+h} = y_T + h · (y_T − y_1)/(T − 1)
:::

- `T` — último instante observado.
- `h` — cuántos pasos hacia delante se pronostica. Con `h = 1` se pronostica el mes siguiente.
- `m` — el periodo del ciclo (12 en datos mensuales, 4 en trimestrales, 7 en diarios semanales).
- `y_{T+h−m}` — el valor del mismo punto del ciclo anterior. Con datos mensuales (`m = 12`) y
  `h = 3`, es `y_{T−9}`: el dato de hace nueve meses, que cae en el mismo mes del año que el que
  estás pronosticando.

El error de cada pronóstico es `e_t = y_t − ŷ_t`. Entonces:

:::formula
MASE = media(|e_t|) / [ (1/(T − m)) · Σ_{t=m+1}^{T} |y_t − y_{t−m}| ]
:::

- El **numerador** es el error absoluto medio del método que estás evaluando.
- El **denominador** es el error absoluto medio del ingenuo estacional medido **dentro de la
  muestra**. Es la escala: no depende de las unidades de la serie.
- Si `m = 1`, el denominador es exactamente el error del ingenuo simple, y por eso el MASE del
  propio ingenuo vale **1,0 exacto**: es una identidad, no una coincidencia.

:::formula
sMAPE = (1/n) · Σ 2 · |e_t| / (|y_t| + |ŷ_t|)
:::

- Es adimensional y está entre 0 y 2 (multiplicado por 100, entre 0 % y 200 %).
- Se calcula sobre los `n` pronósticos evaluados, no sobre toda la serie.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `h` | Horizonte: cuántos pasos hacia delante se pronostica | pasos (meses, días) | El error de cualquier método crece con `h`, y el del ingenuo crece más deprisa que el de un buen modelo. Comparar dos métodos con horizontes distintos invalida la comparación |
| `m` | Periodo del ciclo estacional | pasos (entero) | Es el `m` del denominador del MASE. Si lo pones mal (1 en una serie mensual), la escala sale mucho menor, el MASE se infla y un modelo bueno parece malo |
| `e_t` | Error del pronóstico para el instante `t`: observado menos pronosticado | las de la serie | Su media con signo detecta el sesgo (si es muy negativa, el modelo se queda corto); su media en valor absoluto es el numerador del MASE |
| `media(abs(e_t))` | Error absoluto medio del método evaluado: la media de los errores en valor absoluto | las de la serie | Es el numerador. Un valor de 5 euros no dice nada hasta que lo divides entre la escala del ingenuo |
| Denominador del MASE | Error absoluto medio del ingenuo estacional dentro de la muestra | las de la serie | Es lo que hace la métrica comparable entre series. Si vale 0 (serie constante), el MASE es infinito y hay que usar otra cosa |
| `MASE` | Error del método, medido en «ingenuos» | adimensional | Por debajo de 1 el método bate al ingenuo; por encima, no. Es la única de estas métricas con una referencia incorporada |
| `sMAPE` | Error relativo simetrizado | adimensional (×100 se lee en %) | Al ser relativo, se dispara si `y_t` y `ŷ_t` son pequeños y del mismo signo. No tiene versión con referencia: un 0,05 no sabes si es bueno |
:::

## Ejemplo

Una serie mensual de 4 años (48 meses) con un ciclo anual de amplitud 20 y una deriva suave de
0,5 al mes. Se usan los 3 primeros años para mirar y el último para juzgar. La escala del MASE,
calculada sobre el entrenamiento, es **7,328**: eso es lo que falla el naive estacional dentro de
la muestra. Con los 12 pronósticos del último año:

| Método | MAE | MASE | sMAPE |
| --- | --- | --- | --- |
| Ingenuo (plano en el último dato) | 12,913 | 1,762 | 0,108 |
| Naive estacional (copia el año anterior) | 5,466 | 0,746 | 0,047 |
| Deriva (prolonga la recta) | 12,807 | 1,748 | 0,107 |

Solo el naive estacional baja de 1, y lo hace con holgura (0,746), así que **cualquier modelo que
se precie tiene que bajar de ahí**. El ingenuo y la deriva fallan casi el doble, porque los dos
ignoran el ciclo anual: la deriva acierta la tendencia y se equivoca con todos los meses, y el
ingenuo se equivoca además con la tendencia.

Fíjate en que el sMAPE da 0,047 para el ganador y no hay forma de saber si eso es bueno, porque la
serie vale en torno a 100. El MASE, en cambio, dice «la mitad de lo que falla el ingenuo», que es
una frase con sentido.

Y una comprobación que conviene hacer una vez: con la serie `3, 5, 4, 6, 8, 7, 9`, el denominador
del MASE es `(2+1+2+2+1+2)/6 = 1,6667`, exactamente el error absoluto medio del ingenuo. Por eso
el MASE del ingenuo vale `1,6667 / 1,6667 = 1,0`. Siempre.

## Código

```python verificable
import numpy as np

# Serie mensual sintetica: 4 anos, ciclo anual fuerte (amplitud 20) y deriva suave (0,5 al mes).
azar = np.random.default_rng(3)
t = np.arange(48)
y = 100 + 0.5 * t + 20 * np.sin(2 * np.pi * t / 12) + azar.normal(0, 4, 48)

entrena, prueba = y[:36], y[36:]        # 3 anos para mirar, 1 ano para juzgar
h = np.arange(1, 13)                    # horizonte: de 1 a 12 meses por delante

# Los tres pronosticos de referencia para el ano que falta:
ingenuo = np.repeat(entrena[-1], 12)                                        # plano
estacional = entrena[-12:]                                                  # copia el ano anterior
deriva = entrena[-1] + h * (entrena[-1] - entrena[0]) / (len(entrena) - 1)  # sigue la recta

escala = np.abs(entrena[12:] - entrena[:-12]).mean()   # lo que falla el estacional en muestra
print("escala del MASE:", round(escala, 3))            # -> escala del MASE: 7.328
for nombre, f in (("ingenuo", ingenuo), ("estacional", estacional), ("deriva", deriva)):
    e = prueba - f
    mae, smape = np.abs(e).mean(), (2 * np.abs(e) / (np.abs(prueba) + np.abs(f))).mean()
    print(f"{nombre:11s} MAE {mae:6.3f}  MASE {mae / escala:5.3f}  sMAPE {smape:5.3f}")
# -> ingenuo     MAE 12.913  MASE 1.762  sMAPE 0.108
# -> estacional  MAE  5.466  MASE 0.746  sMAPE 0.047
# -> deriva     MAE 12.807  MASE 1.748  sMAPE 0.107
```

:::claves
- `entrena[:-12]` tiene 24 elementos y `prueba` tiene 12, así que `entrena[-12:]` (el año anterior completo) encaja con `prueba` punto por punto. Es la forma de escribir el naive estacional sin bucles: desplazar el array doce posiciones.
- `np.repeat(entrena[-1], 12)` construye un array de doce copias del último valor. Con `[entrena[-1]] * 12` sale una lista de Python, y aunque el `print` se vea igual, `prueba - lista` funciona por casualidad y `lista.mean()` fallaría con `AttributeError`.
- La escala se calcula **solo con el tramo de entrenamiento** (`entrena`), nunca con `prueba`. Si la calcularas con todo, estarías usando el futuro para normalizar el error y el MASE saldría artificialmente pequeño.
- `f"{nombre:11s}"` alinea los nombres a la izquierda en once caracteres para que las columnas queden rectas. `:6.3f` deja tres decimales y reserva seis caracteres; sin ese ancho, los números bailan de una fila a otra.
- El sMAPE se calcula con `np.abs(prueba) + np.abs(f)` en el denominador, no con `prueba + f`. Con valores negativos, la suma sin valor absoluto puede anularse y el sMAPE se va a infinito sin avisar.
- `azar.normal(0, 4, 48)` añade ruido, así que los números exactos dependen de la semilla. Con `default_rng(3)` salen los de los comentarios; cambiar la semilla cambia las cifras pero no el orden de los métodos.
:::

```python verificable
import numpy as np

# Una serie sencilla para ver de donde sale el 1 del MASE.
y = np.array([3.0, 5.0, 4.0, 6.0, 8.0, 7.0, 9.0])
escala = np.abs(y[1:] - y[:-1]).mean()          # lo que falla el ingenuo en muestra
error = y[1:] - y[:-1]                          # el error del ingenuo, uno a uno
print("escala", round(escala, 4))               # -> escala 1.6667
print("MASE del ingenuo", round(np.abs(error).mean() / escala, 4))
# -> MASE del ingenuo 1.0

# El sMAPE no es simetrico: pasarse y quedarse corto no cuestan lo mismo.
real, alto, bajo = 30.0, 45.0, 15.0
print("sMAPE si me paso:", round(2 * abs(real - alto) / (abs(real) + abs(alto)), 4))
# -> sMAPE si me paso: 0.4
print("sMAPE si me quedo corto:", round(2 * abs(real - bajo) / (abs(real) + abs(bajo)), 4))
# -> sMAPE si me quedo corto: 0.6667

# El MAPE no existe si un valor real es cero; el MASE si.
real = np.array([0.0, 4.0, 6.0, 5.0, 7.0])      # un mes sin ventas
pred = np.array([3.0, 0.0, 4.0, 6.0, 5.0])      # el pronostico ingenuo: el mes anterior
with np.errstate(divide="ignore"):              # dividir entre cero da inf, no una excepcion
    print("MAPE con un cero:", np.abs((real - pred) / real).mean())   # -> inf
print("denominador del MASE:", round(np.abs(real[1:] - real[:-1]).mean(), 3))
# -> denominador del MASE: 2.25
```

:::claves
- `y[1:] - y[:-1]` es la diferencia de un paso para toda la serie, y su media en valor absoluto es el denominador del MASE con `m = 1`. Es el mismo número que el error del ingenuo **en muestra**, y de ahí sale el 1,0 exacto.
- `np.abs(error).mean()` es el MAE. Si en vez de `abs` usaras `error.mean()`, obtendrías el **sesgo** (el error medio con signo): cerca de cero significa que los errores positivos y negativos se compensan, no que el modelo sea bueno.
- `np.errstate(divide="ignore")` silencia el aviso de NumPy al dividir entre cero, pero el resultado sigue siendo `inf`. Silenciar el aviso no arregla la métrica: lo que hay que hacer es no usar MAPE con ceros.
- `2 * abs(...) / (abs(real) + abs(alto))` es la versión simétrica. Compara el 0,4 de pasarse 15 con el 0,6667 de quedarse 15 corto: mismo error absoluto, distinto castigo. Por eso, si reportas sMAPE, di si el sesgo es al alza o a la baja.
- La media del MASE del bloque anterior se hace sobre doce errores, y el denominador sobre 24 diferencias. No pasa nada: el MASE es un cociente de medias, no una media de cocientes.
:::

:::figura
fichero: pronosticos-de-referencia-y-mase
pie: A la izquierda, la serie mensual de 4 años con los tres pronósticos de referencia para el último año, que es el tramo que se juzga (a la derecha de la línea de puntos). El ingenuo repite el último dato y se queda plano; el naive estacional copia el año anterior y por eso reproduce el ciclo; la deriva prolonga la recta y se salta la estacionalidad por completo. A la derecha, el MASE de cada uno, con la línea en 1: solo el naive estacional baja del listón, con 0,746. Los otros dos se quedan en 1,762 y 1,748, casi el doble. Ese 1 es la frontera entre «mi modelo aporta algo» y «mi modelo no vale para nada», y es la primera comparación que hay que hacer antes de mirar ninguna otra cosa.
fuente: figuras/pronosticos-de-referencia-y-mase-1.py
:::

## Errores típicos

- **Reportar MAE o RMSE sin escala.** Un MAE de 12,9 puede ser excelente en una serie que vende
  millones o desastroso en una que vende 20. Añade siempre el MASE, o al menos el MAE del ingenuo
  al lado.
- **Usar MAPE con valores pequeños o ceros.** Si un mes se vendió 0, el MAPE es infinito, y si se
  vendió 2 con pronóstico 4, ese mes aporta un 100 % de error y arrastra la media. El MASE aguanta
  los dos casos porque su denominador es una media de diferencias.
- **Comparar métodos con horizontes distintos.** El MASE de un pronóstico a un paso y el de uno a
  doce pasos no son comparables: el segundo es mayor casi siempre, incluso para un modelo mejor.
  Fija el horizonte y evalúa a todos los métodos en el mismo.
- **Calcular la escala con `m` equivocado.** En una serie mensual con estacionalidad, el
  denominador lleva `m = 12`; con `m = 1` la escala sale más pequeña, el MASE se infla y puedes
  rechazar un modelo que era bueno. Confirma el periodo con la
  [[autocorrelacion-acf-pacf|ACF]] antes de decidir.
- **Confundir «bate al ingenuo» con «sirve para el negocio».** Un MASE de 0,95 bate al ingenuo por
  muy poco y puede no compensar el coste de mantener el modelo. La métrica descarta; la decisión la
  toma el [[metricas-de-regresion|coste del error]] en euros.
- **Elegir el modelo y evaluarlo con los mismos datos.** Si pruebas veinte métodos y te quedas con
  el de menor MASE sobre el mismo tramo, ese MASE está sesgado a la baja. Guarda un tramo final
  para la comprobación, con la lógica de la [[validacion-temporal|validación temporal]].

:::truco
Un MASE por debajo de 1 en **muestra** no demuestra nada: muchos modelos con parámetros ajustados a
esos datos bajan de 1 sin esfuerzo. La prueba de fuego es el MASE fuera de muestra, sobre datos que
el modelo no ha visto. Y si el MASE fuera de muestra es mayor que 1, el pronóstico de referencia
habría hecho el trabajo mejor y más barato.
:::

:::practica
enunciado: Una serie trimestral de dos años: 10, 20, 30, 40, 12, 22, 33, 44. Calcula la escala del MASE con m = 4, el MASE del naive estacional y explica por qué sale ese número exacto.
pista: Con m = 4, el denominador se calcula con las diferencias entre cada trimestre del segundo año y el mismo trimestre del primero.
solucion: Las diferencias son |12 − 10| = 2, |22 − 20| = 2, |33 − 30| = 3 y |44 − 40| = 4, así que la escala es (2+2+3+4)/4 = 2,75. Los pronósticos del naive estacional son los cuatro trimestres del primer año, los errores son 2, 2, 3 y 4, y su media es 2,75. El MASE sale 2,75/2,75 = 1,0 exacto: el naive estacional es la referencia contra la que se mide, así que siempre empata consigo mismo. Que valga 1 no significa que sea bueno, significa que cualquier otro método tiene que bajar de ahí.
:::

## Comprueba que lo sabes

:::quiz
p: Un modelo tiene un MASE de 0,5 en el tramo de prueba. ¿Qué significa?
o: Que su error medio es la mitad del que comete el naive estacional en la muestra
o: Que acierta el 50 % de las veces
o: Que su error medio es la mitad que el de un modelo que repite el último dato
a: 1
e: El MASE divide el error absoluto medio del modelo entre el error absoluto medio del naive (estacional si hay estacionalidad, simple si no) medido dentro de la muestra. No es un porcentaje de aciertos: un 0,5 significa la mitad de error que el ingenuo, ni más ni menos.
:::

:::quiz
p: La demanda de un producto fue 0 un mes y 4 al siguiente. ¿Por qué el MAPE no sirve aquí y el MASE sí?
o: Porque el MAPE divide entre el valor real de cada mes, y ese cero lo convierte en infinito; el MASE divide entre una media de diferencias, que solo es cero si la serie es constante
o: Porque el MAPE solo funciona con números enteros
o: Porque el MASE no necesita el valor real, solo el pronóstico
a: 1
e: El MAPE es la media de los errores relativos, y cada error se divide entre el valor real de ese mes: un cero hace la métrica infinita. El MASE normaliza con una única escala calculada sobre toda la muestra, así que solo falla si todas las diferencias valen cero, es decir, si la serie es constante.
:::

:::quiz
p: Comparas dos modelos con series distintas: el A tiene MAE 40 y MASE 0,8, y el B tiene MAE 12 y MASE 1,4. ¿Cuál es mejor?
o: El B, porque tiene mucho menos error absoluto
o: El A, porque bate a su referencia y el B no
o: No se puede decir sin ver las series
a: 2
e: El MAE está en las unidades de cada serie, así que 40 en una serie grande puede ser mucho mejor que 12 en una serie pequeña. El MASE está normalizado con la propia referencia de cada serie, y por eso sí se puede comparar: 0,8 significa que el modelo A comete un 20 % menos de error que su ingenuo, mientras que el B comete un 40 % más que el suyo.
:::

:::nota
El MASE se pensó para errores a un paso: su escala se calcula con diferencias de un paso, así que
con un horizonte largo sale más alto y puede superar 1 aunque el modelo mejore al ingenuo en ese
horizonte. Si tu evaluación es a varios pasos, mírala junto al RMSSE (la misma idea con errores al
cuadrado), que penaliza más los fallos grandes y se comporta mejor con horizontes largos.
:::
