---
id: volatility-drag
titulo: Volatility drag
fase: 9
nivel: intermedio
rutas: [quant, core]
prerequisitos: [retornos-logaritmicos, varianza-y-desviacion, ratio-de-sharpe]
tags: [volatilidad, rentabilidad, apalancamiento]
resumen: Por qué dos carteras con la misma media acaban en sitios distintos, y cómo la volatilidad se come el interés compuesto aunque el activo no baje.
fuentes: ["Hull (2018), 'Options, Futures and Other Derivatives'", "Thorp (2017), 'A Man for All Markets'"]
---

## En una frase

La rentabilidad que de verdad acumulas es, aproximadamente, la media menos la mitad de la
varianza: subir la volatilidad sin subir la media te empobrece aunque el activo acabe donde
empezó.

## La idea

Un activo que un mes sube un 10 % y al siguiente cae un 10 % no vuelve a su sitio: acaba un 1 %
por debajo, porque `1,10 · 0,90 = 0,99`. La media aritmética de los dos meses es cero, y sin
embargo has perdido dinero.

La razón es que la riqueza se compone multiplicando, no sumando. Y multiplicar castiga la
dispersión: hace falta una subida mayor que la caída para compensarla, porque la subida se aplica
sobre un capital menor. Con un −50 % necesitas un +100 % para volver; con un −80 %, un +400 %.

Ese hueco entre la media aritmética y la tasa que de verdad acumulas es el arrastre de
volatilidad, y crece con el cuadrado de la volatilidad. No es un detalle de segundo orden: en
carteras con volatilidad alta puede comerse varios puntos al año. Es la razón de que un activo
apalancado al 2x no rinda el doble a largo plazo, y de que la volatilidad importe incluso cuando
la media no cambia.

:::aviso
El arrastre no es una pérdida que ocurre «en el camino» y se recupera al final. Es una propiedad
de la composición: la riqueza final es el producto de los factores y por eso depende de la
dispersión, no solo del promedio. Se puede medir, se puede estimar y se puede gestionar con el
tamaño de posición, pero no se puede «esperar a que vuelva».
:::

## Definición formal

Para retornos por periodo `r₁, …, r_T`, la riqueza final es `∏(1 + r_t)`. Su tasa de crecimiento
por periodo es:

:::formula
g = (1/T) · Σ ln(1 + r_t)  ≈  E[r] − σ²/2
:::

- `g` — tasa de crecimiento geométrico: lo que de verdad acumula el capital por periodo.
- `E[r]` — media aritmética de los retornos.
- `σ²` — varianza de los retornos en el mismo periodo.
- La aproximación es buena con retornos pequeños y se rompe con saltos grandes.

La forma exacta no es una aproximación: la media del logaritmo es `g`, y la relación con la media
aritmética es una desigualdad (Jensen) que siempre va en el mismo sentido: `g ≤ ln(1 + E[r])`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `E[r]` | Media aritmética de los retornos del periodo | tanto por uno | Sube `g` en la misma cantidad; es la parte «de verdad» del rendimiento |
| `σ` | Volatilidad de los retornos del periodo | tanto por uno | Baja `g` con el cuadrado: doblar la volatilidad cuadruplica el arrastre |
| `σ²/2` | Arrastre por periodo | tanto por uno | Es el precio de la dispersión; con `σ = 0,20` anual son 2 puntos al año |
| `T` | Número de periodos | periodos | Alarga el efecto: el arrastre se acumula multiplicativamente, no se diluye |
:::

## Ejemplo

Dos periodos con `+10 %` y `−10 %`: media aritmética 0; riqueza `1,10 · 0,90 = 0,99`; tasa
geométrica `−1 %` en dos periodos. Con `±20 %`: media 0 y `1,20 · 0,80 = 0,96`, un `−4 %`.

Con la fórmula, el arrastre esperado por periodo sería `σ²/2`. Para `σ = 0,20` anual, `0,04/2 =
0,02`: dos puntos al año. Si tu cartera rinde un 8 % de media con esa volatilidad, la tasa que
acumulas ronda el 6 %, y en 20 años la diferencia es de más del 45 % de riqueza.

## Código

```python verificable
import numpy as np

# 10.000 carteras de 10 anos, retorno mensual con media 8 % anual y volatilidad 25 % anual
rng = np.random.default_rng(5)
mensual = rng.normal(0.08 / 12, 0.25 / np.sqrt(12), (10_000, 120))
riqueza = np.prod(1 + mensual, axis=1)

print(f"media aritmetica mensual {mensual.mean():.4f}")    # -> media aritmetica mensual 0.0067
print(f"media log mensual {np.log1p(mensual).mean():.4f}")  # -> media log mensual 0.0041
print(f"mitad varianza {-0.5 * (0.25 / np.sqrt(12)) ** 2:.4f}")  # -> mitad varianza -0.0026
print(f"riqueza mediana {np.median(riqueza):.4f}")          # -> riqueza mediana 1.6520
print(f"riqueza media {riqueza.mean():.4f}")                # -> riqueza media 2.2326
print(f"tasa anualizada {np.median(riqueza) ** (1 / 10) - 1:.4f}")  # -> tasa anualizada 0.0515
print(f"exp(mu)-1 {np.exp(0.08) - 1:.4f}")                  # -> exp(mu)-1 0.0833
```

La diferencia entre las dos últimas líneas es el arrastre: un 8,33 % de media aritmética se
convierte en un 5,15 % de tasa mediana. Y la distancia entre la riqueza mediana (1,65) y la media
(2,23) dice lo mismo desde el otro lado: la media la sostienen unas pocas carteras que se
disparan.

:::claves
- `np.prod(1 + mensual, axis=1)` compone los 120 meses **de cada cartera**. Sin `axis=1` multiplica
  toda la matriz y devuelve un solo número, que no es la riqueza de nadie.
- `np.log1p(mensual)` calcula `ln(1 + r)` sin perder precisión cuando `r` es pequeño. Con
  `np.log(1 + mensual)` el resultado es casi idéntico, pero `log1p` es la forma correcta.
- La media del logaritmo es la tasa geométrica por periodo. `np.log1p(mensual).mean()` da 0,0041
  mensual, que anualizado con `× 12` es 0,049, coherente con el 5,15 % de la mediana.
- `** (1 / 10)` anualiza la riqueza de 10 años. Elevar a 1/10 no es lo mismo que dividir por 10:
  la primera es una tasa compuesta y la segunda una media simple.
- La mediana y la media de la riqueza no coinciden porque la distribución es asimétrica: la media
  la mueven las colas derechas. En una cartera real, la mediana describe mejor lo que le pasa a
  una persona.
:::

## Errores típicos

- **Comparar dos carteras por su media aritmética cuando tienen volatilidades distintas.** La de
  mayor volatilidad parece mejor y acumula menos. Compara tasas geométricas o, mejor, la riqueza
  final.
- **Mantener apalancamiento constante en un activo volátil.** Un 2x diario rinde menos del doble a
  largo plazo y puede perder dinero con el subyacente plano. El apalancamiento constante paga el
  arrastre todos los días.
- **Olvidar el coste de financiar el apalancamiento.** El arrastre es solo una parte: el tipo del
  préstamo se resta además, y con tipos altos se come el resto.
- **Extrapolar el interés compuesto a partir del retorno medio.** Si usas `E[r]` como tasa de
  crecimiento, sobreestimas la riqueza final y lo haces más cuanto más volátil sea la cartera.
- **Creer que el arrastre solo afecta a productos apalancados.** Afecta a cualquier cartera
  volátil, incluida una de acciones sin apalancar. Lo que pasa es que con volatilidad moderada es
  pequeño y fácil de ignorar hasta que deja de serlo.

:::practica
enunciado: Una cartera tiene una media anual del 10 % y una volatilidad del 35 %. Estima la tasa geométrica y calcula cuánta riqueza acumula en 15 años, comparándola con la que daría el 10 % compuesto.
pista: La tasa geométrica aproximada es la media menos σ²/2.
solucion: σ²/2 = 0,1225/2 = 0,0613. La tasa geométrica es 0,10 − 0,061 = 0,039, un 3,9 %. En 15 años, 1,039^15 = 1,77 veces el capital. Con el 10 % compuesto serían 1,10^15 = 4,18 veces. El arrastre se lleva más de la mitad de la riqueza, y eso con una cartera que «de media» gana un 10 %.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué cartera acumula más riqueza: una con 8 % de media y 10 % de volatilidad, o una con 9 % de media y 30 % de volatilidad?
o: La primera: su tasa geométrica es 7,5 % frente a 4,5 % de la segunda
o: La segunda, porque su media es mayor
o: Las dos igual, porque la media ya tiene en cuenta la volatilidad
a: 1
e: La primera pierde 0,10²/2 = 0,005, así que crece al 7,5 %. La segunda pierde 0,30²/2 = 0,045 y crece al 4,5 %. Un punto más de media no compensa veinte puntos más de volatilidad.
:::

:::quiz
p: Un activo sube un 50 % y luego cae un 50 %. ¿Dónde acaba?
o: En el 75 % del capital inicial, porque 1,5 · 0,5 = 0,75
o: Donde empezó, porque las dos variaciones se compensan
o: En el 100 %, porque la media aritmética es cero
a: 1
e: La riqueza se multiplica: 1,5 · 0,5 = 0,75, un −25 %. La media aritmética de +50 % y −50 % es cero, y por eso la media aritmética no sirve para describir lo que pasa con el capital.
:::
