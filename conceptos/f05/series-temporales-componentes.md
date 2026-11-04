---
id: series-temporales-componentes
titulo: Componentes de una serie temporal
fase: 5
nivel: básico
rutas: [ds, quant, de]
prerequisitos: [notacion-matematica, medidas-de-centralidad]
tags: [series-temporales, tendencia, estacionalidad]
resumen: Toda serie temporal se lee como suma de una tendencia, un patrón que se repite, ciclos largos y ruido; separarlos es el primer paso para pronosticar.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice'", "Cleveland et al. (1990), 'STL: A Seasonal-Trend Decomposition Procedure Based on Loess'"]
---

## En una frase

Una serie temporal es un valor medido a lo largo del tiempo, y casi siempre se puede leer como
la mezcla de cuatro cosas: una dirección de fondo, un patrón que se repite cada cierto periodo,
oscilaciones largas e irregulares y puro azar.

## La idea

Piensa en las ventas diarias de una panadería. Si las dibujas durante tres años verás varias
cosas a la vez. Las ventas suben poco a poco porque el barrio crece: eso es la **tendencia**.
Los sábados se vende mucho más y los lunes menos, y eso se repite cada semana: eso es la
**estacionalidad**. Hubo un año en el que todo el barrio vendió menos por una obra larga en la
calle, y eso no se repite cada semana ni cada año: eso es un **ciclo**. Y luego está el ruido:
un día llueve, otro hay un partido, otro se estropea el horno.

Cada componente tiene una naturaleza distinta y se trata de forma distinta:

- **Tendencia.** La dirección de largo plazo: se estima con medias móviles o suavizados y es lo
  que se extrapola al pronosticar. No tiene por qué ser una recta.
- **Estacionalidad.** Un patrón que se repite con un **periodo fijo y conocido**: el día de la
  semana, el mes, la hora. Como el periodo es fijo, se aprende de los ciclos anteriores.
- **Ciclo.** Oscilaciones largas y **sin periodo fijo**: la economía, una moda. No se pueden
  predecir repitiendo lo anterior: no sabes cuándo empiezan ni cuánto duran.
- **Ruido (o residuo).** Lo que queda al quitar todo lo demás. No es basura: si tiene
  estructura, te has dejado un componente sin extraer.

¿Y si la serie no tiene alguno de ellos? Eso también es información: las temperaturas tienen
estacionalidad anual y ninguna tendencia, y un precio de acción es casi todo residuo.

La otra decisión es cómo se combinan: si la amplitud del patrón crece con el nivel (el sábado
vende un 50 % más cuando la base es mayor), es **multiplicativa**; si la amplitud se mantiene
(200 barras más cada sábado), es **aditiva**. Un logaritmo convierte el primer caso en el
segundo.

## Definición formal

Sea `y_t` el valor observado en el periodo `t`. El **modelo aditivo** descompone la serie así:

:::formula
y_t = T_t + S_t + C_t + e_t          ·          y_t = T_t · S_t · C_t · e_t   (multiplicativo)
:::

- `y_t` — el valor observado en el periodo `t`.
- `T_t` — la tendencia: el nivel de fondo de la serie en `t`.
- `S_t` — la estacionalidad: el efecto del periodo dentro del ciclo, con periodo `m` fijo (por
  ejemplo `m = 12` para meses o `m = 7` para días de la semana). Se repite, así que
  `S_t ≈ S_{t−m}`.
- `C_t` — el ciclo: oscilación de periodo largo y variable. Muchas veces se agrupa con la
  tendencia y se habla de «componente tendencia-ciclo».
- `e_t` — el residuo o error: lo que no explican los demás.

Tres propiedades que se usan a diario:

1. **La estacionalidad aditiva suma cero dentro de un ciclo completo:** `Σ S_t = 0` sobre los `m`
   periodos. Si al estimarla no suma cero, has metido parte de la tendencia dentro del patrón.
2. **El logaritmo convierte el producto en suma:** `ln(y_t) = ln(T_t) + ln(S_t) + ln(C_t) + ln(e_t)`.
   Por eso, ante una serie multiplicativa, se trabaja con el logaritmo y se vuelve atrás al
   final.
3. **Una media móvil de longitud igual al periodo elimina la estacionalidad:** promediar 12
   meses consecutivos promedia un ciclo entero y `S_t` se cancela.

Para estimar el patrón estacional hacen falta **al menos dos ciclos completos**, y con dos la
estimación es frágil. Con tres o más se puede comprobar que el patrón es estable. Esa es la razón
por la que no se puede hablar de estacionalidad anual con 14 meses de datos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `y_t` | El valor observado en el periodo `t` | las de la serie | Es el dato; todo lo demás son piezas que se estiman a partir de él |
| `T_t` | La tendencia: el nivel de fondo | las de la serie | Si crece, la serie tiene dirección. Extrapolarla lejos es la apuesta más arriesgada: describe el pasado, no garantiza el futuro |
| `S_t` | La estacionalidad: el efecto del periodo dentro del ciclo | las de la serie (aditiva) o % del nivel (multiplicativa) | Cuanto mayor sea su amplitud, más se repite la serie dentro de cada ciclo y menos informa el último valor suelto. Con un periodo `m` mal elegido, parte de la estacionalidad se queda dentro de `T_t` |
| `m` | La longitud del ciclo estacional (7 días, 12 meses) | periodos | No es un parámetro que se estime: se decide. Si no divides la serie entre al menos 2 ciclos completos, `S_t` es una casualidad; con 3 o más puedes comprobar que el patrón aguanta |
| `C_t` | El ciclo: oscilación larga y sin periodo fijo | las de la serie | No se puede aprender repitiendo el pasado, porque no sabes cuándo empieza ni cuánto dura. Casi siempre se agrupa con la tendencia |
| `e_t` | El residuo: lo que no explican los demás | las de la serie | Si en vez de ruido blanco tiene rachas o picos, todavía queda estructura sin extraer y el pronóstico puede mejorar |
| `Σ S_t` | La suma de los efectos estacionales de un ciclo completo | las de la serie | En el modelo aditivo tiene que valer cero; si sale distinta de cero, has metido tendencia (o nivel) dentro del patrón |
:::

:::figura
fichero: series-temporales-tendencia-y-patron
pie: Arriba, tres años de ventas diarias: la serie sube y además tiene ritmo semanal, y las dos cosas se ven a la vez. Abajo a la izquierda, promediar 365 días consecutivos cancela el patrón semanal y el anual, y lo que queda es la dirección de fondo. Abajo a la derecha, los doce efectos estacionales, que suman cero: una serie con 14 meses solo cubre un año y dos meses, así que no hay con qué comparar y ese patrón no se puede estimar.
fuente: figuras/series-temporales-componentes-1.py
:::

:::figura
fichero: series-temporales-aditiva-y-multiplicativa
pie: La misma serie con la misma proporción de fin de semana, montada de las dos maneras. En la aditiva la brecha entre sábado y lunes no cambia aunque la panadería crezca; en la multiplicativa crece con el nivel. Si descompones de forma aditiva una serie que en realidad es multiplicativa, esa brecha que crece se queda dentro del residuo y el residuo sale con forma. El logaritmo la devuelve al caso aditivo.
fuente: figuras/series-temporales-componentes-1.py
:::

## Ejemplo

24 meses de una serie construida a mano, con los tres componentes conocidos:

```
tendencia       T_t = 100 + 2·t          (sube 2 cada mes)
estacionalidad  S_t = 10 · sen(2π·t/12)  (un ciclo al año)
ruido           e_t = +1, −1, +1, −1, …
```

Algunos valores de la serie, `y_t = T_t + S_t + e_t`:

- Mes 0: `100 + 0 + 1` = **101,0**.
- Mes 3: `106 + 10 − 1` = **115,0** (el seno vale 1 en el mes 3).
- Mes 6: `112 + 0 + 1` = **113,0** (el seno vale 0).
- Mes 12: `124 + 0 + 1` = **125,0** (se repite el patrón del mes 0, pero 24 más arriba).

Entre el mes 0 y el mes 12 la estacionalidad y el ruido son idénticos, y la serie sube justo 24,
que son 12 meses por 2 de tendencia. Y al restar `S_t` y `e_t` reaparece `T_t` exacta.

Suavizar cambia la foto: la serie original tiene una desviación típica de **13,16** y la media
móvil de 12 meses, **7,79**. Esa diferencia era estacionalidad y ruido, no dirección de fondo.

## Código

```python verificable
import numpy as np

# 24 meses construidos a mano: tendencia + estacionalidad anual + ruido que alterna.
meses = np.arange(24)
tendencia = 100 + 2.0 * meses
estacionalidad = 10 * np.sin(2 * np.pi * meses / 12)   # un ciclo completo cada 12 meses
ruido = np.array([1.0, -1.0] * 12)

serie = tendencia + estacionalidad + ruido

print(f"mes 0  {serie[0]:.1f}")    # -> 101.0
print(f"mes 3  {serie[3]:.1f}")    # -> 115.0
print(f"mes 6  {serie[6]:.1f}")    # -> 113.0
print(f"mes 12 {serie[12]:.1f}")   # -> 125.0

# La descomposicion aditiva se deshace restando: la tendencia vuelve exacta.
print(f"tendencia recuperada {np.allclose(serie - estacionalidad - ruido, tendencia)}")  # -> True
```

```python verificable
import numpy as np

meses = np.arange(24)
serie = 100 + 2.0 * meses + 10 * np.sin(2 * np.pi * meses / 12) + np.array([1.0, -1.0] * 12)

# Promediar 12 meses promedia un ciclo entero: la estacionalidad se cancela.
media_movil = np.convolve(serie, np.ones(12) / 12, mode="valid")

print(f"desviacion de la serie       {serie.std(ddof=1):.2f}")        # -> 13.16
print(f"desviacion de la media movil {media_movil.std(ddof=1):.2f}")  # -> 7.79
```

:::claves
- `np.convolve(serie, np.ones(12) / 12, mode="valid")` **no** devuelve 24 valores: devuelve 13. La media móvil solo existe donde la ventana cabe entera, así que las 11 primeras posiciones desaparecen y la serie se acorta. Los dos `.std()` del ejemplo se calculan sobre longitudes distintas y no son directamente comparables.
- `np.ones(12) / 12` es el kernel: un promedio móvil es una convolución con una ventana de unos dividida por su longitud. Si escribes `np.ones(12)` sin dividir, el resultado sale multiplicado por 12. Y el kernel va en el orden correcto para promediar, pero si lo inviertes (`np.ones(12)[::-1]`) el resultado es el mismo porque es simétrico; con un kernel asimétrico, no.
- `.std()` de NumPy usa `ddof=0` por defecto (divide entre `n`), mientras que `.std()` de una `Series` de pandas usa `ddof=1` (divide entre `n − 1`). Por eso el ejemplo escribe `ddof=1` a mano: sin él, los 13,16 y 7,79 salen algo menores. Es la diferencia entre el portal y lo que devuelve pandas por defecto.
- `np.array([1.0, -1.0] * 12)` construye 24 valores alternando: es una lista de Python multiplicada, no una función de NumPy. Si en vez de 12 escribieras 11, la serie tendría 22 valores y `tendencia + estacionalidad + ruido` fallaría con un error de formas (broadcasting), no con un aviso.
- `np.allclose(serie - estacionalidad - ruido, tendencia)` compara con tolerancia, no con `==`. La razón es que `10 * np.sin(2 * np.pi * meses / 12)` no da exactamente 0 en el mes 6 (da del orden de `1e-15`), así que una comparación exacta devolvería `False` y te haría buscar un error que no existe.
- La serie del ejemplo es determinista a propósito: el ruido `±1` está escrito a mano y no se sortea. Al no haber semilla, el resultado es siempre el mismo, y por eso este bloque puede ser `verificable` con la desviación típica escrita en el comentario.
:::

## Errores típicos

- **Llamar estacionalidad a un ciclo.** La estacionalidad tiene periodo fijo y conocido (semana,
  año); un ciclo económico no. Si intentas pronosticar un ciclo repitiendo el pasado reciente,
  fallas: no sabes cuándo empieza ni cuánto dura. La estacionalidad sí se puede aprender.
- **Descomponer de forma aditiva una serie multiplicativa.** Si la amplitud del patrón crece con
  el nivel, el modelo aditivo deja esa amplitud metida en el residuo y el residuo sale con
  forma. Toma logaritmos primero, o usa una descomposición multiplicativa.
- **Extrapolar la tendencia como si fuera una ley.** Una recta ajustada a 24 meses proyectada a 5
  años es casi siempre una fantasía. La tendencia sirve para describir el pasado, no para
  garantizar el futuro.
- **Declarar estacionalidad con menos de dos ciclos.** Con 14 meses no puedes distinguir un
  patrón anual de una casualidad. Necesitas al menos dos ciclos completos para estimarla y tres
  para creértela; con menos, di que no hay datos suficientes.
- **Confundir efectos de calendario con estacionalidad.** Semana Santa, los festivos que caen en
  distinto mes cada año y los días laborables del mes no son un patrón fijo: hay que corregirlos
  aparte, o el «patrón» cambia cada año.
- **Ignorar un cambio de estructura.** Una huelga, una pandemia o un cambio en la forma de medir
  rompen la serie. Si no lo detectas, la tendencia estimada es un promedio de dos mundos
  distintos y no describe ninguno.
- **Tomar el residuo como ruido puro.** Si el residuo muestra rachas, picos o
  [[autocorrelacion-acf-pacf|autocorrelación]], todavía queda estructura por explicar: el
  pronóstico puede mejorar.

:::practica
enunciado: Una serie mensual sigue y = 80 + 3·t + S + e, con estacionalidad aditiva de periodo 12 y efectos 10, 8, 4, 0, −4, −8, −10, −8, −4, 0, 4 y 8. Comprueba que suman cero y, con ruido nulo, calcula el valor del mes 0, el del mes 12 y cuánto sube la serie en esos doce meses.
pista: El patrón estacional es idéntico en el mes 0 y en el mes 12.
solucion: La suma de los doce efectos es 0, así que no hay tendencia escondida en el patrón. Mes 0: 80 + 3·0 + 10 = 90. Mes 12: 80 + 3·12 + 10 = 126. La serie sube 126 − 90 = 36, que son exactamente 12 meses por 3 de tendencia; el patrón se repite y no aporta nada a la subida.
:::

## Comprueba que lo sabes

:::quiz
p: Las ventas de una tienda suben cada año y además son más altas todos los diciembres. ¿Cómo se llaman esos dos efectos?
o: Tendencia el crecimiento anual y estacionalidad el patrón de diciembre
o: Estacionalidad el crecimiento anual y ciclo el patrón de diciembre
o: Los dos son estacionalidad, porque se repiten cada año
a: 1
e: La tendencia es la dirección de fondo, que aquí crece año tras año. La estacionalidad es el patrón que se repite con un periodo fijo, en este caso 12 meses. Un ciclo tendría una duración variable y no se podría aprender repitiendo el pasado.
:::

:::quiz
p: Una serie mensual de 14 meses no muestra un patrón claro al comparar meses entre años. ¿Qué conclusión es razonable?
o: Que no hay estacionalidad en esa serie
o: Que no hay datos suficientes para estimarla: hacen falta al menos dos ciclos completos y lo ideal son tres
o: Que hay que usar una descomposición multiplicativa en vez de aditiva
a: 2
e: Con 14 meses solo tienes un año y dos meses, así que no puedes comparar un mismo mes en dos años distintos. La ausencia de patrón visible no prueba que no exista. El tipo de descomposición es otra decisión, que se toma mirando si la amplitud crece con el nivel.
:::

:::truco
Antes de elegir un modelo de pronóstico, dibuja la serie y responde por escrito a tres
preguntas: ¿hay dirección de fondo?, ¿hay un patrón que se repite y con qué periodo?, ¿la
amplitud de ese patrón crece cuando la serie crece? Las tres respuestas deciden si necesitas
[[descomposicion-stl|descomposición]], logaritmos y qué familia de modelos tiene sentido.
:::
