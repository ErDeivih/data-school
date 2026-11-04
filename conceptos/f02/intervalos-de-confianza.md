---
id: intervalos-de-confianza
titulo: Intervalos de confianza
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [poblacion-y-muestra, teorema-central-del-limite, distribuciones-continuas]
tags: [inferencia, incertidumbre, estimacion]
resumen: El 95 % no es la probabilidad de que el parámetro caiga dentro: es la frecuencia con la que el procedimiento acierta si lo repites muchas veces.
fuentes: ["Neyman (1937), 'Outline of a Theory of Statistical Estimation Based on the Classical Theory of Probability'", "Morey et al. (2016), 'The Fallacy of Placing Confidence in Confidence Intervals'"]
---

## En una frase

Un intervalo de confianza del 95 % es una **regla** que, aplicada a muchas muestras distintas,
produce intervalos que contienen el parámetro en el 95 % de los casos; para el intervalo concreto
que tienes delante, el parámetro o está dentro o no lo está, y eso no se puede saber.

## La idea

El problema de fondo es que quieres decir un número pero no quieres mentir. «La altura media de los
españoles es 173,4 cm» es una afirmación demasiado rotunda para una muestra de 1.200 personas: si
hubieras medido otras 1.200, te habría salido 173,9 o 172,8. El intervalo de confianza es la forma
estándar de decir «173,4 cm, y con estos datos mi procedimiento acierta dentro de 1,2 cm en el
95 % de los casos».

La interpretación correcta sale de imaginar el experimento repetido. Supón que pudieras repetir
todo el estudio 10.000 veces, cada una con su muestra aleatoria, y que cada vez construyeras el
intervalo de la misma forma. Obtendrías 10.000 intervalos, todos centrados en sitios ligeramente
distintos y todos con la misma anchura. **El parámetro es fijo**; lo que varía es el intervalo. Si
el procedimiento es del 95 %, unos 9.500 de esos intervalos contendrán el parámetro y 500 no. Eso
es todo lo que dice el «95 %»: es una propiedad de la *receta*, no del intervalo que tienes en la
mano.

De ahí se sigue lo que **no** se puede decir: una vez calculado `[172,2 , 174,6]`, no hay ninguna
probabilidad asociada. O `μ` está ahí dentro (probabilidad 1) o no está (probabilidad 0).
Cualquier frase del estilo «hay un 95 % de probabilidad de que la media esté entre estos valores»
es incorrecta en la interpretación frecuentista, y es exactamente la frase que se lee en la mitad
de los informes. Para decir eso hace falta un enfoque bayesiano y un **intervalo creíble**, que es
otro objeto ([[estimacion-bayesiana-map]]).

Segunda pieza de la intuición: **de dónde sale la anchura**. La media muestral varía alrededor del
parámetro con desviación típica `σ/√n` —el error típico—, y el [[teorema-central-del-limite]] dice
que con `n` moderado esa variación es aproximadamente normal. Para cubrir el 95 % central de una
normal hay que alejarse 1,96 errores típicos a cada lado. De ahí la fórmula: `x̄ ± 1,96·σ/√n`. Los
tres ingredientes son los tres que se pueden manipular: la variabilidad de los datos (`σ`), el
tamaño de muestra (`n`) y el nivel de confianza (el 1,96).

Y de ahí sale la ley que más se usa en la práctica: **para reducir la anchura a la mitad, hay que
multiplicar la muestra por cuatro**. Porque el ancho va con `1/√n`, no con `1/n`. Duplicar la
muestra solo reduce el intervalo un 29 %. Es la razón de que conseguir precisión sea caro.

:::figura
fichero: intervalos-cobertura-y-anchura
pie: Cada línea verde es el intervalo del 95 % de un estudio distinto, todos con n = 20 y la misma receta: 5 de los 100 no llegan a μ, y ese 5 % es el fallo previsto por el diseño, no un error de cálculo. A la derecha, la anchura frente a n: pasar de 3,1 cm a 1,6 cm exige cuadruplicar la muestra, porque la anchura va con 1/√n y no con 1/n.
fuente: figuras/intervalos-de-confianza-1.py
:::

## Definición formal

Sea `X = (X₁, …, Xₙ)` una muestra aleatoria de una población con media `μ` y varianza `σ²`, y sea
`x̄` la media muestral.

- `μ` — el parámetro a estimar: la media poblacional. Es fijo y desconocido.
- `x̄` — la media muestral, que es aleatoria.
- `σ` — desviación típica poblacional. Si se conoce, se usa; si no, se sustituye por `s`, la
  desviación típica muestral.
- `α` — el nivel de significación: la probabilidad de que el intervalo **no** cubra el parámetro.
  Con confianza del 95 %, `α = 0,05`.
- `z_{1−α/2}` — el cuantil `1 − α/2` de una normal estándar. Para el 95 %, `z_{0,975} = 1,96`.
- `t_{n−1, 1−α/2}` — el mismo cuantil pero de una `t` de Student con `n − 1` grados de libertad. Se
  usa cuando `σ` se estima con `s`.
- `ET = σ/√n` — **error típico** de la media muestral.

Los tres intervalos que se usan de verdad:

:::formula
σ conocida:      x̄ ± z_{1−α/2} · σ/√n
:::

:::formula
σ estimada:      x̄ ± t_{n−1, 1−α/2} · s/√n
:::

:::formula
Proporción:      p̂ ± z_{1−α/2} · √( p̂(1 − p̂) / n )
:::

La definición rigurosa de «confianza» es esta: un intervalo `[L(X), U(X)]` tiene nivel de confianza
`1 − α` si

:::formula
P( L(X) ≤ μ ≤ U(X) ) = 1 − α   para todo μ
:::

Fíjate en que la probabilidad se toma sobre `X`, es decir sobre **todas las muestras posibles**, no
sobre `μ`. La cobertura tiene que cumplirse para todo valor de `μ`, no solo para el verdadero: esa
es la condición que hace que la receta sea válida antes de ver los datos.

Cuatro consecuencias que se deducen de la fórmula y se olvidan:

1. **El intervalo es simétrico solo si la distribución es simétrica.** Con `σ` conocida y media,
   sí. Para una proporción cercana a 0 o a 1, los métodos exactos (Clopper-Pearson, Wilson) dan
   intervalos asimétricos y más honestos.
2. **La `t` ensancha el intervalo con muestras pequeñas.** Con `n = 8` grados de libertad 7,
   `t = 2,365` en vez de 1,96: un 21 % más de anchura. Con `n = 100`, `t ≈ 1,984`: casi idéntico.
3. **La cobertura es una propiedad previa a los datos.** Una vez calculado el intervalo, ya no hay
   probabilidad que valga.
4. **Un intervalo que no cubre cero no es lo mismo que un contraste con `p < 0,05`… salvo que lo
   es.** Para el caso de dos medias y el mismo `α` bilateral, el intervalo de la diferencia excluye
   cero exactamente cuando el [[contraste-de-hipotesis]] rechaza. Son la misma información con dos
   formatos.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `μ` | Media poblacional: el parámetro que se quiere estimar | las de `X` | Es fijo y desconocido, así que no sube ni baja. No tiene distribución: o está dentro del intervalo o no, y por eso no se puede decir «hay un 95 % de que esté aquí» |
| `x̄` | Media muestral | las de `X` | Es lo único aleatorio del intervalo: cambia de una muestra a otra con desviación típica `σ/√n`. El intervalo se construye centrado en ella |
| `σ` | Desviación típica poblacional | las de `X` | Es el numerador del error típico: el doble de dispersión, el doble de anchura. Casi nunca se conoce, y cuando se sustituye por `s` hay que cambiar `z` por `t` |
| `s` | Cuasi-desviación típica muestral (`ddof = 1`) | las de `X` | Sustituye a `σ`. Es aleatoria, y esa incertidumbre añadida es exactamente lo que compensa la `t`: con 8 datos ensancha el intervalo un 21 % |
| `n` | Tamaño de la muestra | observaciones | La anchura va con `1/√n`: para dividirla por dos hay que cuadruplicar `n`, y duplicarla solo la reduce un 29 %. Con `n` grande la `t` converge a 1,96 y deja de importar |
| `α` | Nivel de significación: probabilidad de no cubrir | proporción | Si sube, el cuantil baja y el intervalo se estrecha, pero falla más: `α = 0,05` da 1,96 y `α = 0,10` da 1,645. Bajarlo a 0 exigiría un intervalo infinito |
| `z_{1−α/2}` | Cuantil de la normal estándar | — | 1,96 para el 95 %. Usarlo con `s` y pocos datos estrecha el intervalo y la cobertura real cae del 95 % al 91 % aproximadamente: con `n < 30`, usa la `t` |
| `t_{n−1, 1−α/2}` | Cuantil de la `t` de Student con `n − 1` grados de libertad | — | Con 7 grados de libertad vale 2,365 y con 99 vale 1,984: baja al crecer `n` y se pega a 1,96. Es el precio de haber estimado `σ` con `s` |
| `ET = σ/√n` | Error típico de la media muestral | las de `X` | Es la semianchura sin el cuantil: con `σ = 8` y `n = 20` vale 1,79 cm. Es lo que se reduce al aumentar la muestra, antes de multiplicar por el cuantil |
:::

## Ejemplo

Ocho medidas de una pieza, en milímetros: 5,2 · 4,8 · 6,1 · 5,5 · 4,9 · 5,8 · 5,0 · 6,3.

- Media: 5,450 mm. Desviación típica muestral: `s = 0,568` mm.
- Error típico: `0,568/√8 = 0,201` mm.
- Con `n − 1 = 7` grados de libertad, `t_{0,975} = 2,365`. Semianchura: `2,365 · 0,201 = 0,475`.
- Intervalo del 95 %: `[4,975 , 5,925]`. Casi un milímetro de anchura para estimar una pieza que
  se supone de 5,5 mm: con ocho medidas, esa es la precisión que hay.

Y ahora la comprobación de qué significa el 95 %. Simulando 5.000 estudios, cada uno con 20
observaciones de una población con media 170 y desviación 8, y construyendo en cada uno el intervalo
`x̄ ± 1,96·8/√20`:

- Anchura de cada intervalo: 7,01. Es constante, porque `σ` se supone conocida.
- Cobertura empírica: **0,948**, es decir 94,8 % de los intervalos contuvieron la media real.

Que salga 0,948 y no 0,950 es ruido de Monte Carlo: con 5.000 réplicas, la desviación típica de esa
proporción es `√(0,95·0,05/5000) ≈ 0,003`, así que 0,948 está a unos dos tercios de error típico. El
procedimiento funciona: el 95 % describe **la proporción de intervalos que aciertan**, exactamente
como dice la definición.

Y un detalle importante: en esa simulación, un 5 % de los intervalos falla. No porque el cálculo
esté mal, sino porque el azar produce de vez en cuando muestras raras. Un intervalo que falla es
parte del diseño, no un error.

## Código

```python verificable
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)

# Muestra de 20 alturas: media 166,7 y desviacion 6,62
muestra = np.array([160, 158, 171, 165, 175, 162, 168, 155, 180, 166,
                    164, 172, 159, 170, 167, 161, 173, 163, 169, 176], dtype=float)
print(f"media muestral  {muestra.mean():.1f}")   # -> 166.7
print(f"desv muestral   {muestra.std(ddof=1):.2f}")  # -> 6.62

# Repetimos el experimento 5000 veces: en cada uno cogemos 20 personas de una
# poblacion con media 170 y desviacion 8, y construimos el intervalo al 95 %.
media_real, desv_real, n, reps = 170.0, 8.0, 20, 5000
semiancho = stats.norm.ppf(0.975) * desv_real / np.sqrt(n)   # sigma conocida
cubren = 0
for _ in range(reps):
    x = rng.normal(media_real, desv_real, size=n)
    cubren += (x.mean() - semiancho <= media_real <= x.mean() + semiancho)

print(f"cobertura empirica {cubren / reps:.3f}")   # -> 0.948
print(f"anchura del intervalo {2 * semiancho:.2f}")  # -> 7.01
```

Ese bucle es la definición de la página ejecutada: se repite el estudio, se construye el intervalo
igual cada vez y se cuenta cuántos aciertan.

:::claves
- `muestra.std(ddof=1)` divide entre `n − 1`; sin el `ddof=1` NumPy divide entre `n` y devuelve 6,45 en vez de 6,62. El intervalo sale entonces más estrecho de lo que debe, y el error no da ningún aviso.
- `cubren += (x.mean() - semiancho <= media_real <= x.mean() + semiancho)` funciona porque los tres operandos son escalares: la comparación encadenada de Python es equivalente a dos comparaciones unidas por `and`. Con arrays de NumPy esa misma línea lanzaría «truth value of an array is ambiguous», y habría que escribir `np.all(...)`.
- El booleano `True` suma como 1, así que `cubren` acaba siendo un entero y `cubren / reps` un `float`. Si lo inicializaras como `cubren = []` y le hicieras `append`, el resultado sería el mismo y el conteo final necesitaría un `sum`: no es más claro, solo más largo.
- El bucle llama a `rng.normal` 5.000 veces y recalcula `x.mean()` dos veces por réplica. Vectorizarlo con `rng.normal(media_real, desv_real, size=(reps, n)).mean(axis=1)` da exactamente lo mismo mucho más rápido, pero deja de leerse la definición: repetir el estudio y contar los aciertos.
- `stats.norm.ppf(0.975)` vale 1,959964, y el código usa ese valor en lugar del 1,96 redondeado. La diferencia en la anchura es de una milésima, pero conviene saber de dónde sale el número: es el cuantil que deja 2,5 % en cada cola.
- `semiancho` es una constante porque `σ` se supone conocida: los 5.000 intervalos tienen la misma anchura y solo cambian de centro. Si estimaras `σ` con `s` en cada réplica, las anchuras también variarían, el cociente ya no sería normal y el 95 % dejaría de ser exacto con `n` pequeño.
:::

```python verificable
import numpy as np
from scipy import stats

# Una sola muestra: el intervalo no es un intervalo de probabilidad
datos = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
n = datos.size
media, desv = datos.mean(), datos.std(ddof=1)
error_tipico = desv / np.sqrt(n)
t = stats.t.ppf(0.975, df=n - 1)          # cuantil 97,5 % de una t con 7 gl

print(f"media           {media:.3f}")       # -> 5.450
print(f"error tipico    {error_tipico:.3f}")  # -> 0.201
print(f"t critico       {t:.3f}")            # -> 2.365
print(f"IC 95 %         [{media - t * error_tipico:.3f}, {media + t * error_tipico:.3f}]")  # -> [4.975, 5.925]
```

Compara el `t` crítico, 2,365, con el 1,96 de la normal: con ocho observaciones hay que ensanchar
el intervalo un 21 % para compensar que `s` es una estimación ruidosa de `σ`. Ese es el precio de
no conocer la varianza poblacional, y se va difuminando con `n`: con 50 grados de libertad el
cuantil ya es 2,009 y con 99 es 1,984.

```python ilustrativo
# Como se encoge el intervalo al crecer la muestra: anchura proporcional a 1/sqrt(n)
#   con n = 100:  anchura 2 * 1,96 * s / 10
#   con n = 400:  anchura 2 * 1,96 * s / 20   (la mitad, con 4 veces mas datos)
# Para partir la anchura por 2 hay que multiplicar la muestra por 4, siempre.
```
## Errores típicos

- **Decir «hay un 95 % de probabilidad de que `μ` esté en `[5,009 , 5,891]`».** Es el error más
  repetido de la estadística aplicada. El parámetro es fijo: o está o no está. El 95 % es la
  frecuencia de acierto del procedimiento, no una probabilidad sobre este intervalo.
- **Interpretar el intervalo como el rango del 95 % de los datos.** No es eso. El intervalo de
  confianza es sobre la **media**, y con `n` grande se estrecha hasta casi un punto. El rango que
  contiene el 95 % de las observaciones se estima con los cuantiles 2,5 % y 97,5 % y tiene un
  ancho que **no** depende de `n` ([[cuantiles-y-percentiles]]).
- **Usar `σ/√n` con `s` y el cuantil normal cuando `n` es pequeño.** Con `n = 8` y `z = 1,96` el
  intervalo sale un 21 % más estrecho de lo que debe, y su cobertura real baja del 95 % al 91 %
  aproximadamente. Con `n < 30` usa la `t`.
- **Ignorar la dependencia entre observaciones.** La fórmula `σ/√n` supone independencia. Si mides
  20 veces la misma pieza o encuestas a 20 personas del mismo hogar, la muestra efectiva es menor y
  el intervalo real es más ancho. Es la causa número uno de intervalos falsamente estrechos en
  datos reales.
- **Aplicar la fórmula normal a una proporción extrema.** Con `p̂ = 0,02` y `n = 50`, el intervalo
  normal da un límite inferior negativo. Usa Wilson o Clopper-Pearson, que respetan `[0, 1]`.
- **Comparar dos grupos por si sus intervalos se solapan.** Dos intervalos del 95 % pueden solaparse
  y la diferencia ser significativa al 5 %. Para comparar, calcula el intervalo de la **diferencia**,
  no compares los dos por separado.

:::trampa
«El intervalo del 95 % cubre el 95 % de los datos» y «hay un 95 % de probabilidad de que el
verdadero valor esté dentro» son las dos frases que hay que dejar de decir. La primera confunde el
intervalo de la media con el de los datos; la segunda confunde la confianza frecuentista con una
probabilidad posterior. Si quieres la segunda frase, calcula un intervalo creíble bayesiano y
podrás decirla sin mentir.
:::

:::practica
enunciado: Con 25 medidas de una pieza, la media es 12,4 mm y la cuasi-desviación típica 2,0 mm. Con el cuantil t de 24 grados de libertad igual a 2,064, calcula el intervalo de confianza del 95 % y cuántas medidas hacen falta para reducir el error típico a la mitad.
pista: Primero el error típico s/√n; la semianchura es el cuantil t multiplicado por ese error típico. El error típico va con 1/√n.
solucion: Error típico: 2,0/√25 = 0,400 mm. Semianchura: 2,064 · 0,400 = 0,826 mm. IC 95 %: [12,4 − 0,83 ; 12,4 + 0,83] = [11,57 ; 13,23]. Para bajar el error típico de 0,400 a 0,200 hay que cuadruplicar la muestra: n = 100. Conclusión: el intervalo da una precisión de más o menos 0,83 mm, y doblarla cuesta cuatro veces más medidas.
:::

## Comprueba que lo sabes

:::quiz
p: Construyes un intervalo de confianza del 95 % para una media y obtienes [10,2 , 12,8]. ¿Qué significa exactamente el 95 %?
o: Que hay un 95 % de probabilidad de que la media poblacional esté entre 10,2 y 12,8
o: Que si repitieras el estudio muchas veces y construyeras el intervalo igual cada vez, el 95 % de esos intervalos contendría la media poblacional
o: Que el 95 % de las observaciones de la población están entre 10,2 y 12,8
a: 2
e: La confianza es una propiedad del procedimiento, definida sobre todas las muestras posibles. Una vez calculado el intervalo ya no hay probabilidad sobre μ, que es fijo. Y no es un rango de datos: para eso se usan los cuantiles 2,5 % y 97,5 %, cuyo ancho no depende de n.
:::

:::quiz
p: Tienes un intervalo del 95 % de anchura 4 unidades con n = 100. ¿Cuántas observaciones necesitas para que la anchura sea 2?
o: 200, porque la anchura es proporcional a 1/n
o: 400, porque la anchura es proporcional a 1/√n
o: 800, porque hay que compensar el cuantil t
a: 2
e: La anchura va con 1/√n: para dividirla por dos hay que multiplicar n por cuatro. Duplicar la muestra solo reduce el intervalo un 29 %, y el cuantil t deja de importar en cuanto n pasa de 50.
:::

:::quiz
p: Con 8 observaciones, el cuantil t es 2,365 frente a 1,96 de la normal. ¿Por qué se usa t?
o: Porque la media muestral no es insesgada con muestras pequeñas
o: Porque al estimar σ con s se añade incertidumbre, y la t lo compensa ensanchando el intervalo
o: Porque con n menor que 30 la distribución de los datos deja de ser normal
a: 2
e: La media muestral siempre es insesgada. El problema es que s varía de una muestra a otra, y el cociente (x̄ − μ)/(s/√n) no sigue una normal sino una t de Student. Con n = 8 grados de libertad 7, y el cuantil 2,365 da un intervalo un 21 % más ancho: sin él, la cobertura real cae por debajo del 95 %.
:::
