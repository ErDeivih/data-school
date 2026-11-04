---
id: tamano-del-efecto
titulo: Tamaño del efecto
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, p-valor, medidas-de-dispersion]
tags: [inferencia, efecto, practica, d-cohen]
resumen: Cuanto de grande es una diferencia, en una unidad que no depende de cuántos datos tengas; la d de Cohen y la diferencia relativa.
fuentes: ["Cohen (1988), 'Statistical Power Analysis for the Behavioral Sciences'", "Cumming (2012), 'Understanding the New Statistics'"]
---

## En una frase

El tamaño del efecto responde a «¿cuánto?» en una unidad que no cambia al añadir datos; el
p-valor responde solo a «¿es difícil de explicar por puro azar?», y esa respuesta depende
enteramente de cuántas observaciones hayas medido.

## La idea

Imagina que quieres saber si una pastilla adelgaza. Mides a 20 personas y pierden 200 gramos de
media. El [[p-valor]] sale 0,6 y concluyes: «no hay efecto». Mides a 200.000 personas y pierden
los mismos 200 gramos. Ahora el p-valor sale 0,0001 y publicas: «la pastilla funciona». En los
dos casos la pastilla hace exactamente lo mismo: 200 gramos.

Ese es el problema: **el p-valor mezcla dos cosas distintas**, el tamaño real de la diferencia y
cuánta información tienes. Con suficientes datos, cualquier diferencia, por minúscula que sea,
acaba siendo «estadísticamente significativa». Y con pocos datos, una diferencia enorme puede no
serlo. La pregunta que de verdad importa —«¿esto es lo bastante grande como para que me
importe?»— no la contesta el p-valor. La contesta el tamaño del efecto.

Hay dos familias de medidas y conviene tenerlas separadas en la cabeza:

- **Estandarizadas**: la diferencia dividida entre una medida de dispersión (`d` de Cohen, `r`,
  odds ratio). No tienen unidades y por eso se pueden comparar entre estudios.
- **En bruto o relativas**: la diferencia en su unidad original (3,2 kg, 4,1 puntos) o como
  porcentaje («un 9 % más de conversión»). Son las que se usan para decidir.

Las dos hacen falta. La estandarizada te dice si el efecto es grande para el fenómeno; la bruta
te dice si es grande para tu decisión. Un `d` de 0,2 en una intervención sobre el sueño puede
dar igual, y un `d` de 0,2 en mortalidad neonatal es enorme.

:::figura
fichero: efecto-mismo-d-distinta-muestra
pie: A la izquierda, el mismo efecto real (`d = 0,55`, línea azul discontinua) estimado con 8 personas por grupo y con 200: con 8 la estimación cae a 0,08 y su intervalo va de −0,90 a 1,06, así que cruza el cero y no puedes descartar que no haya efecto; con 200 se queda en 0,55 con un margen de ±0,20. A la derecha, el p-valor del mismo estudio al crecer la muestra: la curva azul cruza el umbral del 5 % en unas 27 personas por grupo y la discontinua morada, con un efecto más pequeño (`d = 0,20` en vez de 0,55), no lo cruza hasta unas 193, siete veces más muestra. La conclusión es que la `d` no se mueve en ningún punto del eje: lo único que cambia es cuánta información tienes para demostrarla.
fuente: figuras/tamano-del-efecto-1.py
:::

## Definición formal

Para dos grupos independientes con medias `x̄₁` y `x̄₂`:

:::formula
d = (x̄₁ − x̄₂) / s_p ,   s_p = √[ ((n₁−1)·s₁² + (n₂−1)·s₂²) / (n₁+n₂−2) ]
:::

- `x̄₁`, `x̄₂` — media de cada grupo.
- `n₁`, `n₂` — número de observaciones de cada grupo.
- `s₁²`, `s₂²` — varianza muestral de cada grupo (con `n−1` en el denominador).
- `s_p` — desviación típica combinada (*pooled*): la dispersión común estimada a partir de los
  dos grupos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x̄₁ − x̄₂` | Diferencia de medias en su unidad original | las de la variable (kg, puntos, segundos) | Es el efecto bruto, el que se traduce a una decisión. Sube → el efecto importa más en la práctica, y no depende de cuántos datos tengas |
| `d` | Tamaño del efecto estandarizado: la diferencia dividida entre `s_p` | desviaciones típicas (adimensional) | Sube → el efecto es grande comparado con la dispersión. No depende de `n`, así que es comparable entre estudios |
| `s_p` | Desviación típica combinada de los dos grupos | las de la variable | Sube → la `d` baja con el mismo efecto bruto. Solo tiene sentido si las dos desviaciones son parecidas; con una el triple que la otra, mezcla diferencia de medias con diferencia de dispersión |
| `n₁`, `n₂` | Número de observaciones de cada grupo | observaciones | Suben → la `d` **no** cambia, pero su intervalo se estrecha y el p-valor baja. Con 8 por grupo, el intervalo de la `d` va de −0,90 a 1,06 aunque el efecto real sea 0,55 |
| `s₁²`, `s₂²` | Varianzas muestrales, con `n − 1` en el denominador | las de la variable al cuadrado | Suben → `s_p` sube y la `d` baja. Ojo con `ddof`: NumPy divide entre n por defecto, pandas entre n − 1 |
| `g` | La `d` corregida de Hedges | desviaciones típicas | Es algo menor que `d`: con 10 personas por grupo el factor es 0,958, y la corrección se desvanece al crecer `n`. Existe porque la `d` sobreestima el efecto en muestras pequeñas |
| `t = d · √(n/2)` | El estadístico del test t con grupos del mismo tamaño | adimensional | Sube con la `d` y con la raíz de `n`: por eso el p-valor mezcla el tamaño del efecto con la cantidad de datos, que es justo lo que la `d` evita |
| `RR = p₁ / p₂` | Riesgo relativo: cociente de dos proporciones | tanto por uno | «Reduce el riesgo a la mitad» suena igual con 2 % → 1 % que con 40 % → 20 %, y no es lo mismo para decidir. Siempre con la diferencia absoluta al lado |
| `ARR = p₁ − p₂` | Diferencia absoluta de riesgos | puntos porcentuales | Es la que informa de la magnitud real. Su inversa, el NNT, dice cuántas personas hay que tratar para evitar un evento |
:::

La corrección de Hedges para muestras pequeñas encoge ligeramente el valor, porque `d` tiende a
sobreestimar el efecto cuando `n` es bajo:

:::formula
g = d · (1 − 3 / (4·(n₁+n₂) − 9))
:::

La relación con el estadístico del [[test-t]] para grupos del mismo tamaño es directa, y es la
clave de por qué el p-valor depende de `n`:

:::formula
t = d · √(n/2)   ⇒   d = t · √(2/n)
:::

Otras medidas que aparecen según el tipo de variable de respuesta:

- **Diferencia relativa**: `(x̄₁ − x̄₂) / x̄₂`. Se expresa en porcentaje.
- **Riesgo relativo (RR)**: `p₁ / p₂`, cociente de dos proporciones.
- **Diferencia absoluta de riesgos (ARR)**: `p₁ − p₂`, en puntos porcentuales.
- **NNT**: `1 / ARR`. Número de personas que hay que tratar para evitar un evento.
- **V de Cramér**: medida estandarizada para tablas de contingencia, se ve en
  [[chi-cuadrado]].

Las convenciones de Cohen (0,2 pequeño, 0,5 medio, 0,8 grande) son una regla de andar por casa
de las ciencias sociales, no una ley. En tu dominio el umbral de relevancia lo fija el coste de
equivocarse.

## Ejemplo

Un programa de formación se evalúa con una prueba de 100 puntos. En una muestra de 10 personas
por grupo:

- Grupo control: media 68,4 puntos, desviación típica 11,2.
- Grupo tratado: media 74,6 puntos, desviación típica 11,2.

El efecto estandarizado es el mismo en los dos escenarios que vienen ahora, porque solo depende
de las medias y de `s_p`:

- `s_p` = 11,2 (las dos varianzas son iguales).
- `d` = (74,6 − 68,4) / 11,2 = 6,2 / 11,2 = **0,55**. Un efecto mediano según las convenciones.
- Diferencia relativa: 6,2 / 68,4 = **9,1 %**.

Ahora el p-valor con `n = 10` por grupo:

- Error típico de la diferencia: `11,2 · √(2/10)` = 5,01.
- `t` = 6,2 / 5,01 = 1,24, con 18 grados de libertad → **p ≈ 0,23**.

No es significativo. Y con `n = 100` por grupo, usando exactamente las mismas medias y la misma
desviación:

- Error típico: `11,2 · √(2/100)` = 1,58.
- `t` = 6,2 / 1,58 = 3,91, con 198 grados de libertad → **p ≈ 0,0001**.

Mismo `d` = 0,55 en los dos casos. Lo único que ha cambiado es cuántos datos tenías. El primer
estudio no demuestra que no haya efecto: demuestra que con 10 personas por grupo no puedes
distinguirlo del ruido.

## Código

```python verificable
import numpy as np
from scipy import stats

# Dos grupos con media 68,4 y 74,6 y desviacion 11,2 exactas: la d no cambia,
# solo cambia cuanta informacion tenemos para demostrarla.
def grupo(n, media, sd):
    z = np.arange(n) - (n - 1) / 2               # simetrico alrededor de cero
    return media + sd * z / np.sqrt((z**2).sum() / (n - 1))

for n in (10, 100):
    control = grupo(n, 68.4, 11.2)
    tratado = grupo(n, 74.6, 11.2)
    sp = np.sqrt((control.var(ddof=1) + tratado.var(ddof=1)) / 2)
    t, p = stats.ttest_ind(tratado, control)
    print(f"n={n:>3}  d={6.2 / sp:.2f}  t={t:+.2f}  p={p:.4f}")
    # -> n= 10  d=0.55  t=+1.24  p=0.2317
    # -> n=100  d=0.55  t=+3.91  p=0.0001
```

:::claves
- `control.var(ddof=1)` es la **cuasi**-varianza; `np.var` usa `ddof=0` por defecto y con n = 10 la diferencia es de un 11 %, más que suficiente para mover la `d` en la segunda cifra. pandas, en cambio, usa `ddof=1` por defecto: la misma columna da números distintos según la librería con la que la resumas.
- `grupo(n, media, sd)` no sortea nada: construye datos simétricos con `np.arange` y los escala con `np.sqrt((z**2).sum() / (n - 1))` para que la cuasi-desviación valga exactamente `sd`. Si dividieras entre `n`, la desviación real sería menor y la `d` dejaría de ser 0,55 en las dos filas.
- `stats.ttest_ind(tratado, control)` devuelve el estadístico y el p-valor; el orden de los argumentos cambia el **signo** de `t` (+1,24 aquí) pero no el p-valor. Y `equal_var=True` es el valor por defecto: es la versión de Student, no la de Welch.
- `sp = np.sqrt((control.var(ddof=1) + tratado.var(ddof=1)) / 2)` solo vale con grupos del mismo tamaño. Con tamaños distintos hay que ponderar por `n − 1`, como hace `d_con_intervalo` en el bloque siguiente; si no, la `d` sale mal y nada te avisa.
- SciPy no devuelve la `d` ni su error típico: `ttest_ind` da el estadístico y el p-valor, y la `d` hay que construirla a mano. Ese es el motivo de que cada artículo que la publica tenga que decir cómo la calculó.
- La `d` del `print` usa un `6.2` escrito a mano (la resta 74,6 − 68,4). Si cambias las medias en la llamada a `grupo`, el 6,2 no se entera y la `d` impresa deja de corresponder a los datos. La resta hay que hacerla con las medias de verdad: `tratado.mean() - control.mean()`.
:::

```python verificable
import numpy as np

# La d es una estimacion: con pocos datos su intervalo de confianza es enorme.
# Error tipico aproximado de d: raiz(1/n1 + 1/n2 + d^2 / (2*(n1+n2))).
def d_con_intervalo(a, b):
    n1, n2 = a.size, b.size
    sp = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    d = (a.mean() - b.mean()) / sp
    ee = np.sqrt(1 / n1 + 1 / n2 + d**2 / (2 * (n1 + n2)))
    return d, 1.96 * ee

rng = np.random.default_rng(3)                   # el efecto real de la simulacion es d = 0.55
for n in (8, 200):
    a = rng.normal(0.55, 1.0, n)
    b = rng.normal(0.00, 1.0, n)
    d, margen = d_con_intervalo(a, b)
    print(f"n={n:>4}  d={d:+.2f}  IC95% [{d - margen:+.2f}, {d + margen:+.2f}]")
    # -> n=   8  d=+0.08  IC95% [-0.90, +1.06]
    # -> n= 200  d=+0.55  IC95% [+0.35, +0.75]
```

Con 8 personas por grupo la estimación puede caer en 0,08 aunque el efecto real sea 0,55, y el
intervalo va de −0,90 a +1,06: cabe casi cualquier cosa. Con 200 por grupo el intervalo se
estrecha a `[+0,35, +0,75]`.


## Errores típicos

- **Confundir «significativo» con «importante».** Con `n` grande, una diferencia de 0,02 puntos
  en una escala de 100 sale con p < 0,001. Informa siempre del efecto con su intervalo, no solo
  del p-valor.
- **Reportar el p-valor y ninguna medida del efecto.** Un p-valor no se puede comparar entre
  estudios ni traducir a una decisión; una `d` o una diferencia en su unidad, sí.
- **Usar `d` de Cohen con varianzas muy distintas.** `s_p` solo tiene sentido si las dos
  desviaciones son parecidas; si no, `d` mezcla la diferencia de medias con la diferencia de
  dispersión. En ese caso informa la diferencia bruta con su intervalo o la probabilidad de
  superioridad.
- **Tratar los umbrales 0,2 / 0,5 / 0,8 como leyes.** Son convenciones de un campo concreto.
  Un efecto que en educación es pequeño puede ser enorme en publicidad, y al revés.
- **Elegir la escala que más luce.** «Reduce el riesgo a la mitad» (2 % → 1 %) y «mejora un
  punto porcentual» describen el mismo dato. Decide la escala antes de ver los resultados y no
  cambies según lo que te convenga.
- **Calcular el efecto en la misma muestra donde elegiste la mejor de 50 variantes.** El valor
  que sobrevive a una selección está sesgado al alza. Es el problema que corrige
  [[multiplicidad-y-fdr]].
- **Comparar `d` entre estudios con diseños distintos.** La `d` de un experimento controlado y
  la de un estudio observacional con grupos ya existentes no miden lo mismo.

:::practica
enunciado: Un cambio de proceso baja el tiempo medio de 240 s a 228 s, con desviación combinada de 30 s y 25 observaciones por grupo. Calcula la d de Cohen, la diferencia relativa y el estadístico t con t = d·√(n/2). Con t crítico 2,01, ¿se rechaza la nula?
pista: La d divide la diferencia de medias entre la desviación combinada, y el estadístico t sale de multiplicar la d por la raíz de n/2.
solucion: Diferencia: 240 − 228 = 12 s. d = 12/30 = 0,40, un efecto pequeño-medio. Diferencia relativa: 12/240 = 5 %. Estadístico: t = 0,40 · √(25/2) = 0,40 · 3,536 = 1,41. Como 1,41 < 2,01, no se rechaza la nula (p ≈ 0,16). Conclusión: el efecto de 12 s es real y moderado, pero con 25 por grupo no se distingue del ruido.
:::

## Comprueba que lo sabes

:::quiz
p: Un estudio con 200.000 usuarios encuentra que la nueva versión mejora la conversión en 0,02 puntos porcentuales con p < 0,001. ¿Qué conclusión es correcta?
o: La mejora es real e importante, porque el p-valor es muy pequeño
o: La mejora es detectable pero su tamaño (0,02 puntos) puede no compensar el coste de implementarla
o: No se puede decir nada, porque el p-valor no sirve para nada
a: 2
e: Un p-valor pequeño con muchísimos datos solo dice que la diferencia es difícil de atribuir al azar. El tamaño del efecto es el que decide si merece la pena: 0,02 puntos porcentuales son dos conversiones de cada 10.000. El p-valor sí sirve, pero no para juzgar magnitud.
:::

:::quiz
p: Dos grupos tienen medias 68,4 y 74,6 y desviación típica combinada 11,2. ¿Cuánto vale la d de Cohen?
o: 6,2, porque es la diferencia de medias
o: 0,55, porque es 6,2 dividido entre 11,2
o: 0,091, porque es 6,2 dividido entre 68,4
a: 2
e: La d divide la diferencia de medias entre la desviación típica combinada: 6,2 / 11,2 = 0,55. La primera opción es la diferencia bruta, y la tercera es la diferencia relativa dividida entre la media del control (9,1 %), que es otra medida distinta.
:::

:::quiz
p: Con el mismo efecto real (d = 0,55) y 10 personas por grupo obtienes p = 0,23. ¿Qué significa?
o: Que no hay efecto, porque no es significativo
o: Que con esa muestra no puedes distinguir el efecto del ruido, aunque el efecto estimado sea de 0,55
o: Que el efecto real es cero y lo que has visto es azar
a: 2
e: No rechazar la hipótesis nula no es aceptarla: solo dice que la evidencia disponible es compatible con el efecto cero. Con 10 personas por grupo la potencia para detectar d = 0,55 es baja, así que el resultado era esperable. Para eso está el [[tamano-muestral|cálculo del tamaño muestral]].
:::

:::trampa
Un resultado «no significativo» con una muestra diminuta se cita a menudo como «se demostró que
no hay efecto». No se demostró nada. Si vas a informar de una ausencia de efecto, da el tamaño
del efecto observado y el intervalo de confianza: si el intervalo va de −0,3 a +0,9, tu estudio
es compatible con casi cualquier cosa.
:::
