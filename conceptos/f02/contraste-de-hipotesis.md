---
id: contraste-de-hipotesis
titulo: Contraste de hipótesis
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [poblacion-y-muestra, intervalos-de-confianza, distribuciones-continuas]
tags: [inferencia, decision, contraste]
resumen: Un procedimiento que fija de antemano qué resultado contarías como prueba contra la hipótesis nula, y decide si lo observado cae ahí.
fuentes: ["Neyman y Pearson (1933), 'On the Problem of the Most Efficient Tests of Statistical Hypotheses'", "Wasserstein y Lazar (2016), 'The ASA Statement on p-Values: Context, Process, and Purpose'"]
---

## En una frase

Un contraste de hipótesis es un juicio con las reglas escritas antes de ver los datos: se parte de
una hipótesis nula concreta, se calcula un estadístico y se decide si lo observado es demasiado
raro bajo esa hipótesis; «rechazar» significa «esto no cuadra con la nula», nunca «he demostrado
que la nula es falsa».

## La idea

Un juicio penal es el ejemplo que mejor funciona. El acusado llega con presunción de inocencia: esa
es la hipótesis nula, `H₀`. La acusación no tiene que demostrar la culpa «en general»; tiene que
presentar pruebas y el juez decide si son suficientes para tumbar la presunción. Y aquí está la
asimetría que se olvida: una absolución no declara inocente a nadie, solo dice que no hubo pruebas
suficientes. «No rechazar `H₀`» es exactamente eso.

Traducido a datos, la nula es una afirmación **precisa** sobre el mundo: «la media de esta pieza es
5,5 mm», «el fármaco y el placebo tienen la misma media», «esta moneda sale cara con probabilidad
0,5». Tiene que fijar un número o una igualdad, porque una nula del estilo «no hay diferencia» no
da nada que calcular. La alternativa es lo contrario de la nula, y se elige antes de mirar los
datos, no después de ver qué sale.

El segundo ingrediente es el estadístico de contraste: un número que resume los datos y cuya
distribución **conocemos si la nula es cierta**. La media muestral, una diferencia de medias, una
proporción o un estadístico chi-cuadrado sirven para esto. Con esa distribución se responde a la
única pregunta que el método sabe contestar: «si la nula fuera verdad, ¿qué probabilidad había de
ver algo al menos tan extremo como lo que he observado?». Si esa probabilidad es pequeña tienes dos
explicaciones posibles: o la nula es falsa, o te ha tocado una muestra rara. El contraste se queda
con la primera cuando la segunda es muy improbable ([[p-valor]]).

El tercer ingrediente es el nivel de significación `α`, y no lo elige el ordenador: lo eliges tú
antes de ver los datos. `α = 0,05` significa «acepto equivocarme un 5 % de las veces que la nula
sea cierta». Ese 5 % no es una ley de la naturaleza, es un umbral, y moverlo cambia las
conclusiones sin tocar los datos ([[errores-tipo-i-ii-y-potencia]]).

Por eso el orden de las operaciones es lo que sostiene todo: primero la hipótesis, después `α`,
después el estadístico, y solo al final los datos. Cambiar la alternativa o el umbral una vez visto
el resultado convierte el contraste en un trámite decorativo en lugar de evidencia.

## Definición formal

Sea `X = (X₁, …, Xₙ)` una muestra aleatoria y `θ` el parámetro de interés (una media, una
diferencia de medias, una proporción).

- `H₀` — hipótesis nula: `θ = θ₀`, un valor concreto. Se asume cierta mientras no haya pruebas en
  contra.
- `H₁` — hipótesis alternativa: lo contrario de `H₀`. Puede ser bilateral (`θ ≠ θ₀`) o unilateral
  (`θ > θ₀` o `θ < θ₀`).
- `T(X)` — estadístico de contraste: función de los datos cuya distribución bajo `H₀` se conoce.
- `α` — nivel de significación: la probabilidad máxima de rechazar `H₀` cuando `H₀` es cierta.
- `R` — región crítica: el conjunto de valores de `T` para los que se rechaza, elegido de modo que
  `P(T ∈ R | H₀) = α`.
- `p` — el p-valor: `P(T al menos tan extremo como el observado | H₀)`.
- `β` — probabilidad de error de tipo II: no rechazar cuando `H₀` es falsa.
- `x̄`, `μ₀`, `s`, `n` — media muestral, valor de la media bajo `H₀`, cuasi-desviación típica
  muestral y tamaño de la muestra.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `H₀` | Hipótesis nula: un valor concreto del parámetro (`θ = θ₀`) | las del parámetro | No es una magnitud que suba o baje, es la afirmación que se pone a prueba. Cuanto más lejos esté `θ₀` de la realidad, más fácil resulta rechazarla |
| `H₁` | Alternativa: `θ ≠ θ₀` (bilateral) o `θ > θ₀` / `θ < θ₀` (unilateral) | las del parámetro | Pasar de bilateral a unilateral cuando el resultado apunta en una dirección divide el p-valor por dos sin tocar los datos: es la vía rápida al falso positivo |
| `T(X)` | Estadístico de contraste (una t, una diferencia de medias, un chi-cuadrado) | adimensional si es un cociente | Cuanto más se aleja de su valor esperado bajo `H₀`, más evidencia hay en contra. Su escala depende de n, así que no se compara con un umbral fijo |
| `α` | Nivel de significación: probabilidad máxima de rechazar con `H₀` cierta | tanto por uno | Bajarlo de 0,05 a 0,01 mueve el umbral de 2,365 a 3,499 con 7 grados de libertad: se rechaza menos, tanto lo falso como lo cierto |
| `R` | Región crítica: los valores de `T` que llevan al rechazo | las de `T` | Se elige de modo que, bajo `H₀`, la probabilidad de caer dentro sea exactamente α. Y se elige antes de ver el estadístico |
| `p` | Probabilidad de un resultado al menos tan extremo como el observado, si `H₀` es cierta | entre 0 y 1 | Se rechaza cuando `p ≤ α`. Un p grande no demuestra `H₀`: solo dice que estos datos no la contradicen |
| `β` | Probabilidad de no rechazar cuando `H₀` es falsa | tanto por uno | No la eliges tú: se calcula. Con 8 piezas y un descentrado real de 0,3 mm vale 0,75, así que el contraste solo lo detectaría una de cada cuatro veces |
| `x̄ − μ₀` | Distancia entre la media observada y el valor nulo | las de la variable (mm) | Es el numerador de la t. Una diferencia grande con mucho ruido no es evidencia: hay que dividirla por el error típico |
| `s` | Cuasi-desviación típica muestral, con `n − 1` en el denominador | las de la variable | Sube → el error típico sube y la t baja. Con `ddof=0` sale algo menor (0,531 frente a 0,568) y la t sale algo mayor |
| `n` | Tamaño de la muestra | observaciones | Sube → el error típico baja con `√n` y la misma diferencia se vuelve significativa. Es la palanca que domina todo el contraste |
:::

:::formula
Se rechaza H₀ si  p-valor ≤ α
:::

:::formula
T = (x̄ − μ₀) / (s / √n)      con      T ~ t_{n−1}   bajo H₀
:::

Tres consecuencias que se deducen de ahí y se olvidan continuamente:

1. **El contraste bilateral y el intervalo de confianza son el mismo objeto.** Para una media, se
   rechaza `H₀: μ = μ₀` al 5 % exactamente cuando el intervalo del 95 % no contiene `μ₀`. No son dos
   análisis: son dos formatos de la misma información ([[intervalos-de-confianza]]).
2. **El p-valor no mide el tamaño del efecto.** Con `n` enorme, una diferencia de 0,01 mm sale
   significativa. Significativo quiere decir «es difícil explicarlo por azar», no «es importante»
   ([[tamano-del-efecto]]).
3. **Los supuestos forman parte del contraste.** La `t` de arriba supone observaciones
   independientes y, con `n` pequeño, una población aproximadamente normal. Si las ocho piezas se
   midieron el mismo día con el mismo operario, el contraste no es válido por muy pequeño que salga
   el p-valor.

:::figura
fichero: contraste-region-critica-y-su-intervalo
pie: A la izquierda, la distribución que tendría la t si la máquina estuviera centrada y, en rojo, el 5 % repartido en las dos colas: la zona en la que se rechaza. La t observada, −0,249, se queda en el centro, así que no hay rechazo. A la derecha está el mismo juicio en milímetros: el intervalo del 95 % de la media va de 4,975 a 5,925, contiene a 5,500 (p = 0,811) y deja fuera a 6,000 (p = 0,029). Mira los dos paneles juntos: son la misma información con dos formatos, no dos análisis distintos.
fuente: figuras/contraste-de-hipotesis-1.py
:::

## Ejemplo

Ocho piezas medidas con un micrómetro, en milímetros:

```
5,2  4,8  6,1  5,5  4,9  5,8  5,0  6,3
```

La tolerancia nominal es 5,5 mm. ¿Hay evidencia de que la máquina esté descentrada?

- Media muestral: `x̄ = 43,6 / 8 = 5,450` mm.
- Cuasi-desviación típica: `s = 0,568` mm.
- Error típico de la media: `s/√n = 0,568 / 2,828 = 0,2009`.
- Estadístico: `t = (5,450 − 5,500) / 0,2009 = −0,249`.
- Región crítica bilateral al 5 % con 7 grados de libertad: `|t| > 2,365`.
- Como `0,249 < 2,365`, **no se rechaza** `H₀`. El p-valor es 0,811.

La lectura correcta: con ocho piezas y esta dispersión, una desviación de 0,05 mm es
indistinguible del ruido. La lectura incorrecta: «la máquina está bien». No tienes evidencia de que
esté mal, y eso no es lo mismo. Si el descentrado real fuera de 0,3 mm, este contraste tendría una
potencia ridícula y casi nunca lo detectaría.

La misma maquinaria aplicada a una moneda da el resultado contrario: 15 caras en 20 lanzamientos sí
es evidencia contra «la moneda es justa», porque ahí el efecto (0,75 frente a 0,5) es enorme en
relación con la dispersión de solo 20 tiradas.

## Código

```python verificable
import numpy as np
from scipy import stats

# Ocho piezas medidas; la tolerancia nominal es 5,5 mm
piezas = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
mu0 = 5.5

# t de Student para una media: compara x_barra con mu0 usando el error tipico
t, p = stats.ttest_1samp(piezas, popmean=mu0)

print(f"media muestral    {piezas.mean():.3f}")       # -> 5.450
print(f"desv muestral     {piezas.std(ddof=1):.3f}")  # -> 0.568
print(f"estadistico t     {t:.3f}")                   # -> -0.249
print(f"p-valor           {p:.3f}")                   # -> 0.811
print("decision:", "rechazar" if p <= 0.05 else "no rechazar")  # -> no rechazar
```

:::claves
- `stats.ttest_1samp(piezas, popmean=mu0)` devuelve un resultado con nombre, así que `t, p = ...` funciona por el orden de sus dos campos (`statistic` y `pvalue`). Escríbelos explícitos (`res = ...; res.pvalue`) si no quieres depender de ese orden.
- `popmean` es el valor de la media bajo `H₀`, **no** la media de tus datos. Confundirlos hace que el contraste compare la muestra consigo misma y devuelva t = 0.
- El p-valor que devuelve `ttest_1samp` es **bilateral** por defecto; para una cola hay que pasar `alternative="greater"` o `"less"`. Sin ese argumento, un resultado con dirección esperada sale con el doble de p del que crees.
- `piezas.std(ddof=1)` divide entre `n − 1` = 7 y da 0,568. `np.std` por defecto usaría `ddof=0` (divide entre 8) y daría 0,531: la t pasaría de −0,249 a −0,266. SciPy usa internamente `n − 1`, así que la cuenta a mano solo coincide si escribes `ddof=1`.
- `stats.t.ppf(0.975, df=n - 1)` es la inversa de la función de distribución, y el orden de los argumentos importa: primero el cuantil, después los grados de libertad. `ppf` invierte `cdf` y `sf` da la cola derecha (`1 - cdf`); intercambiar el orden no da ningún error, devuelve un número sin sentido.
- `print("decision:", "rechazar" if p <= 0.05 else "no rechazar")` compara con `<=`, no con `<`: la diferencia solo aparece cuando el p-valor vale exactamente 0,05, que con datos reales no ocurre. El peligro de verdad está al imprimir: un p = 0,0499 redondeado a tres decimales se lee «0.050» y parece que no se rechaza, así que la decisión debe salir de la variable `p`, nunca del texto formateado.
:::

```python verificable
import numpy as np
from scipy import stats

# El contraste bilateral y el IC del 95 % responden lo mismo:
# se rechaza H0: mu = mu0 justo cuando mu0 se queda fuera del intervalo.
piezas = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
n = piezas.size
error = piezas.std(ddof=1) / np.sqrt(n)
t_crit = stats.t.ppf(0.975, df=n - 1)          # cuantil 97,5 % de una t con 7 gl
bajo, alto = piezas.mean() - t_crit * error, piezas.mean() + t_crit * error

print(f"IC 95 % de la media: [{bajo:.3f}, {alto:.3f}]")   # -> [4.975, 5.925]
for mu0 in (5.5, 6.0):
    p = stats.ttest_1samp(piezas, popmean=mu0).pvalue
    print(f"mu0 = {mu0}  p = {p:.3f}  dentro del IC = {bajo <= mu0 <= alto}")
# -> mu0 = 5.5  p = 0.811  dentro del IC = True
# -> mu0 = 6.0  p = 0.029  dentro del IC = False
```

El segundo bloque es la comprobación de que las dos herramientas son la misma: cuando `μ₀` vale 6,0
el intervalo se queda corto (su extremo superior es 5,925) y el contraste rechaza; cuando vale 5,5
está dentro y no rechaza.

## Errores típicos

- **Decir que «no rechazar» demuestra la nula.** Es el error más grave porque cambia decisiones
  reales: «el test no detectó diferencia, luego los grupos son iguales». Solo puedes decir que no
  tienes evidencia suficiente con ese tamaño de muestra.
- **Elegir la alternativa después de ver los datos.** Pasar de bilateral a unilateral cuando el
  resultado va en la dirección esperada divide el p-valor por dos sin justificación. La dirección se
  fija antes, y si no la tienes, usa siempre bilateral.
- **Usar `α = 0,05` por costumbre.** El umbral debería salir del coste relativo de cada error: si un
  falso positivo cuesta mil veces más que un falso negativo, `α = 0,05` es una barbaridad.
- **Mirar solo el p-valor.** Con `n = 500.000`, una diferencia de 0,3 puntos de satisfacción sale
  significativa y no le importa a nadie. Reporta tamaño del efecto e intervalo, no solo el p-valor
  ([[tamano-del-efecto]]).
- **Ignorar la dependencia entre observaciones.** Repetir la misma medición, encuestar a hermanos o
  medir la misma pieza cinco veces infla el `n` efectivo y hace que los contrastes sean demasiado
  optimistas. Es la causa número uno de falsos positivos en datos reales.
- **Elegir el contraste después de probar diez.** Cada prueba extra es una oportunidad de dar un
  falso positivo; si has probado varios, la corrección por comparaciones múltiples no es opcional
  ([[multiplicidad-y-fdr]]).

:::practica
enunciado: Cinco piezas nuevas miden 5,1 · 5,4 · 5,0 · 5,3 · 5,2 mm y la tolerancia nominal sigue siendo 5,5 mm. Contrasta si la máquina está descentrada con α = 0,05 bilateral, sabiendo que el cuantil t con 4 grados de libertad es 2,776.
pista: Calcula la media, la cuasi-desviación típica (divide la suma de cuadrados entre n − 1 = 4), el error típico y el estadístico (x̄ − μ₀)/(s/√n).
solucion: Media: 26,0/5 = 5,200 mm. Desviaciones: −0,1 · +0,2 · −0,2 · +0,1 · 0,0; suma de cuadrados 0,10; s² = 0,10/4 = 0,025 y s = 0,158. Error típico: 0,158/√5 = 0,0707. t = (5,200 − 5,500)/0,0707 = −4,24. Como 4,24 supera 2,776, se rechaza H₀ y hay evidencia de descentrado (p ≈ 0,013). Conclusión: con cinco piezas pero muy poca dispersión, un desvío de 0,3 mm sí se detecta.
:::

## Comprueba que lo sabes

:::quiz
p: Un contraste de la media de unas piezas da p = 0,31 con α = 0,05. ¿Qué has demostrado?
o: Que la media poblacional es exactamente la del valor nulo
o: Que no hay evidencia suficiente para rechazar el valor nulo con estos datos
o: Que el experimento estaba mal diseñado
a: 2
e: No rechazar solo significa que lo observado es compatible con la nula; con pocas observaciones y mucha dispersión, eso ocurre casi siempre. No demuestra que la nula sea cierta y tampoco implica que el diseño esté mal: puede que el efecto sea pequeño o que la muestra sea corta.
:::

:::quiz
p: Con 8 piezas, el intervalo de confianza del 95 % de la media es [4,975 , 5,925]. ¿Qué contraste rechaza el mismo conjunto de datos al mismo nivel?
o: Cualquiera cuyo valor nulo quede fuera de [4,975 , 5,925]
o: Solo el contraste contra el valor nulo que sea exactamente la media muestral
o: Ninguno: el intervalo y el contraste dan información distinta
a: 1
e: Para un contraste bilateral de una media, rechazar μ = μ₀ al 5 % equivale a que μ₀ quede fuera del intervalo del 95 %. Los dos objetos llevan exactamente la misma información con distinto formato: por eso 5,5 está dentro (p = 0,811) y 6,0 fuera (p = 0,029).
:::

:::quiz
p: ¿Por qué la hipótesis nula tiene que ser una afirmación precisa y no «no hay diferencia»?
o: Porque hay que conocer la distribución del estadístico bajo la nula para calcular el p-valor
o: Porque las revistas lo exigen así
o: Porque con una nula imprecisa el p-valor sale siempre mayor que 0,05
a: 1
e: El cálculo necesita la distribución del estadístico cuando la nula es cierta, y para eso hace falta un valor concreto del parámetro. Sin ese valor no hay región crítica ni p-valor que calcular. No es un requisito editorial ni tiene que ver con que el p-valor salga grande o pequeño.
:::
