---
id: indicadores-tecnicos
titulo: Indicadores técnicos
fase: 9
nivel: básico
rutas: [quant]
prerequisitos: [tick-data-y-ohlcv, retornos-logaritmicos]
tags: [indicadores, rsi, medias]
resumen: Qué calcula de verdad cada indicador clásico, para qué sirve y por qué optimizar sus parámetros sobre el histórico es la forma más rápida de engañarte.
fuentes: ["Wilder (1978), 'New Concepts in Technical Trading Systems'", "Murphy (1999), 'Technical Analysis of the Financial Markets'"]
---

## En una frase

Un indicador técnico es una transformación de la serie de precios: no añade información que no
estuviera ahí, solo la hace visible de otra forma.

## La idea

Un indicador no predice. Toma precios que ya ocurrieron y los combina para responder preguntas
del tipo «¿cuánto se ha movido últimamente?», «¿las subidas recientes son mayores que las bajadas?»
o «¿el precio está por encima de su media?». Esas preguntas son legítimas y a veces útiles como
variables de un modelo. Lo que no son es una fuente de información nueva.

Hay tres familias. Las **medias** suavizan y comparan el presente con el pasado. Los
**osciladores** como el RSI normalizan la fuerza relativa de subidas y bajadas en una escala de 0
a 100. Las **medidas de rango** como el ATR cuantifican cuánto se mueve el precio, sin dirección.

El peligro no está en usarlos, está en ajustarlos. Un indicador tiene parámetros —periodos,
umbrales— y si los eliges mirando qué combinación habría ganado en el histórico, encontrarás una
que gana siempre. Eso no es una estrategia: es una descripción del pasado con el número de
decimales suficientes para parecer causal.

:::trampa
Optimizar el periodo de una media sobre los mismos datos con los que luego evalúas es
[[data-snooping-y-multiple-testing]] en estado puro. Con 20 periodos probados, la probabilidad de
encontrar uno que bata al mercado por azar es alta. Si no reservas un tramo que no hayas mirado
para elegir el periodo, el resultado es ruido con buena presentación.
:::

## Definición formal

Con cierres `P_t` y un periodo `n`:

:::formula
SMA_n(t) = ( P_t + P_{t−1} + … + P_{t−n+1} ) / n
:::

:::formula
RSI_n = 100 − 100 / ( 1 + RS )        RS = media de subidas / media de bajadas en n periodos
:::

- `SMA_n` — media móvil simple: el precio medio de las últimas `n` observaciones.
- `EMA_n` — media exponencial, con peso `α = 2/(n+1)`; reacciona más rápido que la simple.
- `RS` — cociente entre la magnitud media de las subidas y la de las bajadas.
- `RSI` — oscilador entre 0 y 100; por encima de 70 se lee como «sobrecomprado» y por debajo de 30
  como «sobrevendido», con toda la arbitrariedad que tienen esos umbrales.
- `ATR_n` — media del rango verdadero: el máximo entre alto−bajo, alto−cierre previo y
  cierre previo−bajo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Periodo del indicador | barras | Alarga la memoria: suaviza más, reacciona más tarde y reduce las señales falsas |
| `RS` | Cociente de subidas frente a bajadas | adimensional | Sube el RSI hacia 100; con muchas subidas seguidas el indicador se satura |
| `RSI` | Oscilador normalizado | 0 a 100 | Por encima de 70 indica racha de subidas; no dice que vaya a bajar |
| `ATR` | Rango medio del periodo | unidades de precio | Sube con la volatilidad; sirve para dimensionar stops en unidades comparables |
:::

## Ejemplo

Cierres `10, 11, 10, 12` con `n = 3`.

- Media simple: `(11 + 10 + 12) / 3 = 11`.
- Cambios: `+1, −1, +2`. Media de subidas: `(1 + 0 + 2)/3 = 1`. Media de bajadas: `(0 + 1 + 0)/3 =
  0,333`.
- `RS = 1 / 0,333 = 3`, y `RSI = 100 − 100/4 = 75`.

Setenta y cinco significa «las subidas recientes pesan tres veces más que las bajadas», ni más ni
menos. Que eso sea una señal de venta es una convención, no una consecuencia matemática.

## Código

```python verificable
import pandas as pd

serie = pd.Series([10, 11, 10, 12, 11, 13, 12, 14])

sma3 = serie.rolling(3).mean()
delta = serie.diff()
subidas = delta.clip(lower=0).rolling(3).mean()
bajadas = (-delta.clip(upper=0)).rolling(3).mean()
rsi3 = 100 - 100 / (1 + subidas / bajadas)

print(f"sma3 ultimo {sma3.iloc[-1]:.2f}")   # -> sma3 ultimo 13.00
print(f"rsi3 ultimo {rsi3.iloc[-1]:.2f}")   # -> rsi3 ultimo 80.00
```

Con los ocho cierres del ejemplo, la media de 3 vale `(13 + 12 + 14)/3 = 13` y el RSI está en 80:
las dos últimas subidas pesan cuatro veces más que la bajada intermedia.

:::claves
- `serie.rolling(3).mean()` devuelve NaN en las dos primeras filas porque no hay tres datos. Si
  rellenas esos NaN con cero, la media del inicio se hunde y las señales de arranque son falsas.
- `serie.diff()` da el cambio respecto a la fila anterior. La primera fila es NaN, y ese NaN se
  propaga a las ventanas: es correcto, no es un fallo.
- `delta.clip(lower=0)` deja las subidas y convierte las bajadas en cero; `-delta.clip(upper=0)`
  hace lo simétrico con las bajadas. Es la forma de separar los dos lados sin bucles.
- `rolling(3).mean()` sobre las subidas y sobre las bajadas es la media de Wilder simplificada
  (Wilder usa un suavizado exponencial). Para practicar sirve; para replicar el RSI clásico hay
  que usar su suavizado.
- `1 + subidas / bajadas` puede dividir por cero si no hay ninguna bajada en la ventana. El
  resultado sería infinito y el RSI 100; conviene tratarlo antes de operar con él.
:::

## Errores típicos

- **Optimizar el periodo sobre todo el histórico.** Eliges el que mejor habría funcionado y luego
  lo presentas como si lo hubieras elegido antes. Reserva siempre un tramo final sin mirar.
- **Usar el RSI como señal de compra o venta sin horizonte.** «Sobrecomprado» no significa «va a
  bajar»: significa que las subidas recientes dominan. En tendencias fuertes el RSI puede quedarse
  alto semanas.
- **Encadenar cinco indicadores y creer que se confirman.** Todos salen de los mismos precios, así
  que están correlacionados por construcción. La aparente confirmación es redundancia.
- **Olvidar que el indicador usa precios ya conocidos.** No hay información del futuro en una
  media móvil; si tu backtest obtiene resultados espectaculares, busca el desplazamiento de la
  ventana antes de celebrar.
- **Comparar indicadores entre activos de volatilidad distinta.** Un RSI de 80 en un activo tranquilo
  y en uno que se mueve un 5 % al día no significan lo mismo.
- **Ignorar los costes al pasar de indicador a estrategia.** Un cruce de medias puede funcionar en
  el papel y morir con la horquilla, como cualquier señal de alta frecuencia.

:::practica
enunciado: Con cierres 20, 21, 19, 22, 24 y n = 3, calcula la media simple y el RSI al final, e interpreta el resultado sin decir si hay que comprar o vender.
pista: Separa los cambios en subidas y bajadas antes de promediar.
solucion: SMA3 = (22 + 24 + 19)/3 = 21,67 (las tres últimas son 19, 22, 24). Cambios: +1, −2, +3, +2. En la última ventana: subidas (0 + 3 + 2)/3 = 1,67; bajadas (2 + 0 + 0)/3 = 0,67; RS = 2,5; RSI = 71,4. Interpretación: las subidas recientes pesan 2,5 veces más que las bajadas, y el precio está por encima de su media de 3. Nada de eso dice qué pasará.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué información añade un RSI a la serie de cierres de la que sale?
o: Ninguna nueva: reformula la serie para que la comparación entre subidas y bajadas sea legible
o: Añade la probabilidad de que el precio suba
o: Añade el volumen que hay detrás de cada movimiento
a: 1
e: El RSI es una función determinista de los cierres. No incorpora volumen, ni probabilidad, ni información externa. Su utilidad está en que resume una comparación que a ojo cuesta hacer, no en que descubra algo oculto.
:::

:::quiz
p: Pruebas 30 combinaciones de periodos y eliges la que mejor habría funcionado en 5 años de datos. ¿Qué has hecho?
o: Buscar en el pasado hasta encontrar una combinación favorecida por el azar
o: Validar la estrategia con 30 escenarios distintos
o: Nada relevante, porque los periodos no afectan al resultado
a: 1
e: Cada combinación es una prueba más y el máximo de 30 resultados ruidosos parece bueno por construcción. Es data snooping. Sin una muestra reservada que no hayas usado para elegir, el resultado no es evidencia.
:::
