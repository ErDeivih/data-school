---
id: errores-tipo-i-ii-y-potencia
titulo: Errores tipo I y II, potencia
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, p-valor, distribuciones-continuas]
tags: [potencia, error-tipo-i, tamano-muestral]
resumen: Todo contraste falla de dos maneras: falsa alarma o incendio sin alarma; la potencia mide la segunda y se decide antes de recoger los datos.
fuentes: ["Cohen (1988), 'Statistical Power Analysis for the Behavioral Sciences'", "Neyman y Pearson (1933), 'On the Problem of the Most Efficient Tests of Statistical Hypotheses'"]
---

## En una frase

Un contraste puede equivocarse de dos formas: rechazar algo que era cierto (error de tipo I, la
falsa alarma) o no detectar algo que era falso (error de tipo II, el incendio sin alarma); la
potencia es la probabilidad de evitar el segundo y depende del tamaño del efecto, de la dispersión
y, sobre todo, del tamaño de la muestra.

## La idea

Piensa en un detector de humo. Si lo haces muy sensible, pitará cada vez que fríes bacon: eso es un
error de tipo I, una falsa alarma. Si lo haces muy insensible, no pitará hasta que el fuego sea
grande: eso es un error de tipo II, y es el que mata. No puedes reducir los dos a la vez con el
mismo detector; solo puedes mejorar el detector (mejor sensor, más información). En estadística,
«mejorar el detector» se llama aumentar la muestra, reducir el ruido de medición o medir una
variable más informativa.

La asimetría es la misma que en el contraste de hipótesis: la hipótesis nula es la presunción de
inocencia y `α` lo difícil que es condenar a un inocente. Si exiges pruebas abrumadoras (`α` muy
pequeño), dejarás libres a muchos culpables: subes `β`. Si condenas con cualquier indicio, subes los
inocentes condenados. El umbral es una decisión sobre qué error te duele más, y por eso no existe
un `α` universalmente correcto.

Lo que casi nadie interioriza es que **`β` no lo eliges tú**. `α` es una decisión, pero la
probabilidad de no detectar un efecto real es una consecuencia de cuatro cosas: `α`, el tamaño de la
muestra, la dispersión de los datos y el tamaño del efecto. Si diseñas un estudio con 25
observaciones y mucha dispersión, tu detector es sordo, y no lo sabrás hasta que calcules la
potencia.

Y eso tiene una consecuencia cruel que explica media crisis de replicación: en un estudio con poca
potencia, los pocos resultados que alcanzan significación son precisamente aquellos en los que el
azar empujó la estimación hacia arriba. El efecto publicado está inflado y el siguiente estudio,
con el mismo diseño, no lo encuentra.

Se llama maldición del ganador, y no es un fallo de nadie en
particular: es aritmética.

La regla práctica: antes de recoger datos, decide qué diferencia mínima te importa (no la que
esperas, la que te cambiaría la decisión), estima la dispersión y calcula cuánta muestra necesitas
para detectarla con una potencia razonable. Si no puedes pagar esa muestra, sabes de antemano que tu
estudio no puede responder a la pregunta.

:::figura
fichero: potencia-solape-y-muestra-necesaria
pie: A la izquierda están las dos distribuciones que el contraste tiene que separar con n = 25: la nula y la alternativa quedan tan pegadas que la zona de rechazo (en rojo, α = 0,05) solo recorta el 23,9 % de la curva del efecto real, y el 76,1 % restante se queda dentro. A la derecha, la potencia frente al número de piezas: la curva sube con la raíz de n y cruza el 80 % en n = 126, y con un efecto la mitad de grande (Δ = 0,125) ese mismo cruce se iría a unas 502 piezas por grupo. La lectura práctica es que el detector se elige antes de recoger datos, y aquí se ve cuánto cuesta.
fuente: figuras/errores-tipo-i-ii-y-potencia-1.py
:::

## Definición formal

Las cuatro situaciones posibles, con `H₀` la hipótesis nula:

| | H₀ cierta | H₀ falsa |
| --- | --- | --- |
| No rechazar H₀ | acierto, probabilidad 1 − α | error de tipo II, probabilidad β |
| Rechazar H₀ | error de tipo I, probabilidad α | acierto, probabilidad 1 − β |

- `α` — probabilidad de error de tipo I: rechazar `H₀` cuando es cierta. La fijas tú.
- `β` — probabilidad de error de tipo II: no rechazar `H₀` cuando es falsa. No la fijas: se calcula.
- `1 − β` — **potencia**: probabilidad de detectar un efecto que existe.
- `μ₀`, `μ₁` — media bajo la nula y media real bajo la alternativa.
- `σ` — desviación típica de las observaciones (se supone conocida en las fórmulas de abajo).
- `n` — número de observaciones.
- `Δ = /μ₁ − μ₀/ / σ` — tamaño del efecto estandarizado: cuántas desviaciones típicas separan las
  dos medias ([[tamano-del-efecto]]).
- `Φ` — función de distribución de la normal estándar; `z_{1−α/2}` es su cuantil `1 − α/2`, que
  vale 1,96 para `α = 0,05` bilateral.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `α` | Probabilidad de error de tipo I: rechazar con `H₀` cierta (la falsa alarma) | tanto por uno | Lo fijas tú. Bajarlo de 0,05 a 0,01 mueve el umbral a 2,58 y deja la potencia en 0,092 con n = 25: se rechaza menos, tanto lo falso como lo cierto |
| `β` | Probabilidad de error de tipo II: no detectar un efecto que existe (el incendio sin alarma) | tanto por uno | No la eliges: sale de α, n, σ y del efecto. Aquí vale 0,761 con n = 25 y 0,199 con n = 126 |
| `1 − β` | **Potencia**: probabilidad de detectar el efecto | tanto por uno | Sube con `Δ`, con `α` y con `n` (como su raíz); baja con `σ`. Por debajo de 0,80 el estudio apenas puede responder a la pregunta que se le hace |
| `μ₀`, `μ₁` | Media bajo la nula y media real bajo la alternativa | las de la variable (mm) | Lo que pesa es su diferencia: si el efecto real es la mitad, la muestra necesaria se multiplica por cuatro |
| `σ` | Desviación típica de las observaciones (supuesta conocida) | las de la variable | Sube → la potencia baja, porque el ruido tapa el efecto. Duplicar `σ` equivale a dividir `n` entre cuatro |
| `Δ = /μ₁ − μ₀/ / σ` | Tamaño del efecto estandarizado | desviaciones típicas | Sube → la potencia sube deprisa: la separación entre las dos curvas es `Δ·√n`, y aquí vale 1,25 |
| `n` | Número de observaciones | observaciones | Sube → la potencia sube con su raíz: doblar la separación cuesta cuatro veces más piezas, y pasar del 80 % al 90 % cuesta un 34 % más |
| `z_{1−α/2}` | Cuantil `1 − α/2` de la normal estándar (1,96 con α = 0,05 bilateral) | desviaciones típicas | Sube al bajar `α` y se **resta** en la fórmula: exigir más evidencia cuesta potencia |
| `Φ` | Función de distribución de la normal estándar | adimensional | Convierte la separación `Δ·√n − z` en una probabilidad entre 0 y 1; es el paso final de las dos fórmulas |
:::

Para un contraste bilateral de una media con `σ` conocida, la potencia es aproximadamente:

:::formula
Potencia ≈ Φ( Δ·√n − z_{1−α/2} )
:::

Y despejando `n`, la muestra que hace falta para una potencia objetivo:

:::formula
n ≈ ( z_{1−α/2} + z_{1−β} )² · σ² / (μ₁ − μ₀)²
:::

Tres lecturas directas de esas fórmulas:

1. **La potencia crece con `√n`.** Para duplicar la separación entre la distribución nula y la
   alternativa hay que cuadruplicar la muestra. Detectar efectos pequeños es carísimo.
2. **La potencia crece con `Δ` y decrece con `σ`.** Un efecto grande y un ruido pequeño son
   equivalentes a muchos datos, y las tres cosas cuestan dinero, así que se elige la más barata.
3. **Bajar `α` cuesta potencia.** Pasar de 0,05 a 0,01 con la misma `n` reduce la potencia, porque
   desplazas el umbral y la cola de la alternativa pierde masa.

## Ejemplo

Una máquina llena piezas de 5,5 mm. Por calibraciones anteriores sabes que `σ = 8` mm. Te importa
detectar un descentrado de 2 mm (`Δ = 2/8 = 0,25` desviaciones típicas) con `α = 0,05` bilateral.

Con 25 piezas:

- `Δ·√n = 0,25 · 5 = 1,25`.
- `Potencia ≈ Φ(1,25 − 1,96) = Φ(−0,71) = 0,239`.

Es decir: si la máquina estuviera descentrada 2 mm, este estudio lo detectaría **una de cada cuatro
veces**. Tres de cada cuatro veces concluirías «no hay evidencia de descentrado» con una máquina
averiada.

Con 126 piezas:

- `Δ·√n = 0,25 · 11,225 = 2,806`.
- `Potencia ≈ Φ(2,806 − 1,96) = Φ(0,846) = 0,801`.

Ahora el detector funciona. ¿De dónde sale 126? De la fórmula de tamaño muestral:

- Para potencia 0,80, `z_{1−β} = 0,8416`: `n = (1,96 + 0,8416)² · 64 / 4 = 125,6 → 126`.
- Para potencia 0,90, `z_{1−β} = 1,2816`: `n = (1,96 + 1,2816)² · 64 / 4 = 168,1 → 169`.

Pasar del 80 % al 90 % de potencia cuesta un 34 % más de muestra para el mismo efecto. Nadie dijo
que la potencia fuera barata.

## Código

```python verificable
import numpy as np
from scipy import stats

sigma, delta, alpha = 8.0, 2.0, 0.05     # desviacion conocida y efecto que importa
z_alfa = stats.norm.ppf(1 - alpha / 2)    # 1,96 para el 5 % bilateral

def potencia(n):
    # Separacion entre la nula y la alternativa, medida en errores tipicos
    return stats.norm.cdf(delta * np.sqrt(n) / sigma - z_alfa)

def muestra_necesaria(potencia_objetivo):
    z_beta = stats.norm.ppf(potencia_objetivo)
    return int(np.ceil((z_alfa + z_beta) ** 2 * sigma**2 / delta**2))

for n in (25, 126):
    print(f"n = {n:>3}  potencia {potencia(n):.3f}")
# -> n =  25  potencia 0.239
# -> n = 126  potencia 0.801

print(f"n para potencia 0,80: {muestra_necesaria(0.80)}")   # -> 126
print(f"n para potencia 0,90: {muestra_necesaria(0.90)}")   # -> 169
```

:::claves
- `stats.norm.ppf(1 - alpha / 2)` es la inversa de `cdf`, y el `1 - alpha/2` es lo que codifica el contraste bilateral. Si escribieras `norm.ppf(1 - alpha)` obtendrías 1,645, el umbral unilateral, y la potencia saldría 0,347 en lugar de 0,239: un número equivocado sin ningún aviso.
- Las funciones `potencia` y `muestra_necesaria` leen `delta`, `sigma` y `z_alfa` cuando se llaman, no cuando se definen. Reasignar `sigma` después de definirlas cambia el resultado; y si asignaras `sigma = ...` dentro de la función sin `global`, Python la tomaría por local y lanzaría `UnboundLocalError`.
- `int(np.ceil(...))` hace dos cosas a la vez: redondea **hacia arriba** porque la fórmula es una aproximación (125,6 pasa a 126, mientras que con `round()` un caso de 125,4 se quedaría en 125 y el estudio nacería sin la potencia pedida) y convierte el `np.float64` que devuelve `np.ceil` en un entero de Python, que es lo que necesitan `range()` y los índices.
- `stats.norm.cdf(separacion - z_alfa)` acumula por la izquierda, que es lo que hace falta: la potencia es el área de la alternativa que cae **por encima** del umbral. Con `stats.norm.sf(...)` obtendrías el complementario, 0,761, que es justo `β`.
- `def potencia(n)` y el bucle `for n in (25, 126)` usan el mismo nombre `n`, y no pasa nada: el parámetro vive dentro de la función. Lo que sí engaña es que `potencia` no modifica nada de fuera; es una función pura y se puede llamar tantas veces como haga falta sin efectos laterales.
- `f"n = {n:>3}  potencia {potencia(n):.3f}"` usa `:>3` para alinear a la derecha en tres caracteres: 25 y 126 ocupan lo mismo y las dos líneas de salida quedan pegadas. Y `:.3f` redondea a tres decimales (0,239 y 0,801), no al número entero de casos.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(7)
sigma, delta, reps = 8.0, 2.0, 20000

# Simulacion: la maquina esta descentrada 2 mm. Contamos cuantas veces el
# contraste con sigma conocida lo detecta, para n = 25 y para n = 126.
for n in (25, 126):
    medias = rng.normal(delta, sigma / np.sqrt(n), size=reps)
    z = medias / (sigma / np.sqrt(n))          # estadistico z con mu0 = 0
    detectado = np.mean(np.abs(z) > 1.96)
    print(f"n = {n:>3}  potencia simulada {detectado:.3f}")
# -> n =  25  potencia simulada 0.237
# -> n = 126  potencia simulada 0.801
```

```python ilustrativo
# Con statsmodels el calculo es una linea, pero necesita los parametros
# del test (efecto, potencia, alpha, ratio de grupos) y no se ejecuta aqui:
#
#   from statsmodels.stats.power import TTestIndPower
#   TTestIndPower().solve_power(effect_size=0.25, power=0.80, alpha=0.05)
#
# Util para pruebas t de dos muestras, ANOVA, proporciones y correlaciones.
```

## Errores típicos

- **Calcular la potencia después de ver el resultado.** La «potencia observada» es una función
  monótona del p-valor: no aporta información nueva. La potencia se calcula en el diseño, cuando
  todavía puedes cambiar `n`.
- **Confundir `1 − p` con la potencia.** Un `p = 0,20` no significa «80 % de probabilidad de que no
  haya efecto», ni un `p = 0,80` que el estudio tuviera poca potencia. El p-valor y `β` miden cosas
  distintas y viven en condicionales opuestos.
- **Interpretar «no significativo» como «no hay efecto».** Con 25 piezas y `Δ = 0,25`, un resultado
  no significativo es lo más probable incluso con la máquina descentrada. Es ausencia de evidencia,
  no evidencia de ausencia ([[contraste-de-hipotesis]]).
- **Elegir `α = 0,05` y potencia 0,80 sin pensar en los costes.** En un cribado médico el coste de un
  falso negativo no se parece al de una falsa alarma; en un test A/B que mueve ingresos, tampoco.
  El 0,80 es una convención cómoda, no una ley ([[ab-testing]]).
- **Ignorar la multiplicidad al planificar.** Si vas a contrastar 20 métricas, tu `α` efectivo no es
  0,05 y la potencia de cada contraste tampoco. Hay que corregir antes de calcular la muestra
  ([[multiplicidad-y-fdr]]).
- **Usar el tamaño de efecto que esperas en lugar del que te importa.** Si calculas la muestra para
  un efecto de 5 mm porque es el que crees que hay, y resulta ser de 2 mm, tu estudio nace sin
  potencia. Diseña para la diferencia mínima relevante.

:::practica
enunciado: Una máquina llena piezas con σ = 5 mm y quieres detectar un descentrado de 1,5 mm con α = 0,05 bilateral. Calcula la potencia con 49 piezas y la muestra necesaria para llegar a 0,80 (z de 0,80 = 0,8416).
pista: El efecto estandarizado es Δ = 0,3 y la potencia es Φ(Δ·√n − 1,96). Para la muestra, despeja n = (z + z)² · σ² / Δ².
solucion: Δ = 1,5/5 = 0,30. Con n = 49: Δ·√n = 0,30 · 7 = 2,10 y la potencia es Φ(2,10 − 1,96) = Φ(0,14) = 0,556. Para potencia 0,80: n = (1,96 + 0,8416)² · 25/2,25 = 7,85 · 11,11 = 87,2, o sea 88 piezas. Conclusión: con 49 piezas el detector acierta poco más de la mitad de las veces y para el 80 % hace falta casi el doble de muestra.
:::

## Comprueba que lo sabes

:::quiz
p: Un estudio no encuentra diferencias significativas entre dos grupos. ¿Qué conclusión es defendible?
o: Que no existe diferencia entre los grupos
o: Que con esa muestra y esa dispersión no se ha detectado una diferencia de ese tamaño, y puede que el estudio no tuviera potencia para detectarla
o: Que el error de tipo I ha sido pequeño
a: 2
e: No rechazar no demuestra la nula: si la potencia era del 24 %, tres de cada cuatro veces no se detectaría un efecto real. La conclusión honesta incluye el tamaño de muestra y el efecto mínimo detectable. El error de tipo I es una propiedad del diseño, no un resultado del estudio.
:::

:::quiz
p: Duplicas el tamaño de muestra manteniendo todo lo demás igual. ¿Qué le pasa a la potencia?
o: Se duplica, porque la potencia es proporcional a n
o: Aumenta, pero menos que duplicarse, porque la separación entre nula y alternativa crece con √n
o: No cambia: la potencia depende solo del tamaño del efecto
a: 2
e: Lo que crece con √n es Δ·√n; duplicar n multiplica esa separación por 1,41. Para duplicar la separación hay que cuadruplicar la muestra. El tamaño del efecto y α también influyen, pero n forma parte de la fórmula.
:::

:::quiz
p: ¿Por qué en un estudio con poca potencia un hallazgo significativo suele exagerar el efecto real?
o: Porque los p-valores pequeños siempre vienen de errores de medición
o: Porque para alcanzar significación con poca potencia hace falta que el azar empuje la estimación hacia arriba, así que los resultados publicados están sesgados al alza
o: Porque la potencia baja aumenta α automáticamente
a: 2
e: Con poca potencia solo se detectan los casos afortunados, y esos son los que sobreestiman el efecto: es la maldición del ganador. α no cambia, lo fijas tú. Y no es cuestión de errores de medición, sino de selección sobre el azar.
:::
