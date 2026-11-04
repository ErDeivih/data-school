---
id: tests-no-parametricos
titulo: Tests no paramétricos
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, test-t, anova, medidas-de-centralidad]
tags: [inferencia, rangos, robustez, distribucion]
resumen: Mann-Whitney, Wilcoxon, Kruskal-Wallis y Kolmogorov-Smirnov: contrastar sin suponer una forma concreta para la distribución.
fuentes: ["Wilcoxon (1945), 'Individual Comparisons by Ranking Methods'", "Mann y Whitney (1947), 'On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other'", "Kruskal y Wallis (1952), 'Use of Ranks in One-Criterion Variance Analysis'"]
---

## En una frase

Los tests no paramétricos sustituyen los valores por su orden (o por su posición dentro de la
distribución empírica), de modo que un dato extremo no puede inflar la varianza ni romper el
supuesto de normalidad; a cambio, pierden algo de potencia cuando los datos sí son normales.

## La idea

El [[test-t]] divide la diferencia de medias entre una desviación típica. Esa desviación es su
punto débil: se calcula elevando al cuadrado las distancias, así que un único valor disparatado
la multiplica. Vuelve a mirar el ejemplo de esta página: un grupo tiene siete valores bajos y uno
de 100; la desviación típica del grupo se va a 34 y el test t no ve nada, aunque seis de los
siete valores del grupo estén por debajo del valor más pequeño del otro grupo.

La solución no paramétrica es tirar la magnitud y quedarse con el orden. Ordenas las 16
observaciones de los dos grupos juntas, les asignas los números 1 a 16 y comparas las sumas de
rangos. Un valor de 100 y un valor de 40 que sean ambos los mayores del conjunto reciben el mismo
rango: el test no se inmuta por lo lejos que estén.

**Ese cambio tiene un precio y una letra pequeña.** El precio es la potencia: si los datos son
normales, el test de rangos necesita alrededor de un 5 % más de observaciones para la misma
potencia (su eficiencia relativa asintótica frente al test t es `3/π ≈ 0,955`). La letra pequeña
es más importante: **el test de Mann-Whitney no es un test de medianas**. Contrasta si
`P(A > B) = 0,5`, es decir, si los valores de un grupo tienden a ser mayores que los del otro
(dominancia estocástica). Solo puedes leerlo como un test de medianas si aceptas que las dos
distribuciones tienen la misma forma y solo se diferencian en un desplazamiento.

El mapa de sustituciones:

- **Dos grupos independientes**: Mann-Whitney U (también llamado Wilcoxon rank-sum).
- **Dos medidas del mismo sujeto**: Wilcoxon de rangos con signo.
- **Tres o más grupos independientes**: Kruskal-Wallis (el equivalente del [[anova]]).
- **Tres o más medidas del mismo sujeto**: Friedman.
- **¿Son distintas las distribuciones completas?**: Kolmogorov-Smirnov, que compara las funciones
  de distribución empíricas y por eso detecta diferencias de forma, dispersión o colas, no solo
  de posición.
- **Cualquier estadístico, sin supuestos**: un [[remuestreo-y-permutacion|test de permutación]],
  que baraja las etiquetas y construye la distribución nula con tus propios datos.

## Definición formal

**Mann-Whitney.** Con `n₁` y `n₂` observaciones en cada grupo, se ordenan todas juntas y se
calcula `R₁`, la suma de los rangos del grupo 1:

:::formula
U₁ = R₁ − n₁·(n₁ + 1) / 2 ,   U₂ = n₁·n₂ − U₁ ,   U = min(U₁, U₂)
:::

- `R₁` — suma de los rangos asignados a las observaciones del grupo 1.
- `U₁` — número de parejas (grupo 1, grupo 2) en las que la del grupo 1 es mayor. `U₂` cuenta las
  contrarias, y `U₁ + U₂ = n₁·n₂`.
- Bajo la hipótesis nula, `U` tiene media `n₁·n₂/2` y varianza `n₁·n₂·(n₁+n₂+1)/12`. Con empates
  se usan rangos promedio y se corrige la varianza.
- El estimador del desplazamiento que acompaña al test es el de Hodges-Lehmann: la mediana de
  todas las diferencias por parejas entre los dos grupos.

**Wilcoxon de rangos con signo.** Con `n` diferencias apareadas `dᵢ`: se descartan los ceros, se
ordenan los valores absolutos `dᵢ` y se suman los rangos de las diferencias positivas:

:::formula
W⁺ = Σ { rango(dᵢ) : dᵢ > 0 } ,   E[W⁺] = n·(n+1)/4 bajo H₀
:::

Si las diferencias son simétricas alrededor de cero, `W⁺` se parece a `n(n+1)/4`. Un `W⁺` muy
pequeño o muy grande indica desplazamiento.

**Kruskal-Wallis.** Con `k` grupos, `N` el total y `R̄ᵢ` el rango medio del grupo `i`:

:::formula
H = (12 / (N·(N+1))) · Σᵢ nᵢ · (R̄ᵢ − (N+1)/2)²  ,   gl = k − 1
:::

**Kolmogorov-Smirnov.** Con `F₁` y `F₂` las funciones de distribución empíricas:

:::formula
D = supₓ |F₁(x) − F₂(x)|
:::

`D` es la mayor separación vertical entre las dos escaleras acumuladas. El p-valor se obtiene de
la distribución de Kolmogorov, y con pocos datos conviene el cálculo exacto.

:::figura
fichero: tests-no-parametricos-media-rota-y-rangos
pie: A la izquierda están los dos grupos del ejemplo: el único valor de 100 dispara la desviación del grupo A a 34 y el test t de Welch da p = 0,55, así que la diferencia desaparece aunque siete de los ocho valores de A estén por debajo de todos los de B. A la derecha, los mismos datos ordenados por rangos: si el 100 valiera un millón, el test de Mann-Whitney no se enteraría, porque solo mira el orden y no la distancia. La conclusión es que el precio de esa robustez es no poder leer el resultado como una diferencia de medias.
fuente: figuras/tests-no-parametricos-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `U` | El menor de los dos recuentos de parejas ganadas, `min(U1, U2)` | parejas, entre 0 y `n1·n2` | Es el resultado de la formula. Cerca de `n1·n2/2` significa que los dos grupos se mezclan; en los extremos (0 o el maximo), un grupo domina al otro. No lleva la escala de los datos: `U` es el mismo si el valor mas alto vale 100 o un millon |
| `n1`, `n2` | Observaciones de cada grupo | observaciones | Agrandan la rejilla de parejas `n1·n2` y estrechan la distribución nula, así que detectan diferencias mas pequeñas. Con `n1` y `n2` muy desiguales el test sigue valiendo, pero la potencia la manda el grupo pequeño |
| `R1` | Suma de los rangos del grupo 1 | rangos (1 a `n1+n2`) | Es el dato bruto del que sale `U`. Sube cuando los valores del grupo 1 son grandes; un único valor extremo solo puede subir `R1` hasta el rango maximo, que es exactamente la protección que buscas |
| `W+` | Suma de los rangos de las diferencias positivas (Wilcoxon apareado) | rangos | Bajo la hipotesis nula tiende a `n(n+1)/4`. Muy por debajo o muy por encima indica desplazamiento; los ceros se descartan y `n` baja, lo que cambia el valor esperado |
| `H` | Estadistico de Kruskal-Wallis, el equivalente de `F` sobre rangos | adimensional | Sube cuando los rangos medios de los grupos se alejan del rango medio global. Se compara con una chi-cuadrado de `k - 1` grados de libertad, no con una F |
| `D` | Mayor separación vertical entre las dos funciones de distribución empiricas (KS) | probabilidad, de 0 a 1 | Sube cuando las distribuciones difieren en forma, dispersión o colas, no solo en posición. Un `D` significativo puede convivir con medianas iguales: KS no es un test de medianas |
| `p` | Probabilidad de que el azar produzca un estadístico tan extremo como el tuyo | probabilidad, de 0 a 1 | Baja con la separación entre grupos y sube con los empates. Ojo: `method="auto"` de SciPy elige el calculo exacto y `method="asymptotic"` lo fuerza a la normal, y los dos dan p-valores distintos |
:::

## Ejemplo

Grupo A: `1 2 3 4 5 6 7 100`. Grupo B: `20 21 22 23 24 25 26 27`.

- Medias: A = 128/8 = **16,00** y B = 188/8 = **23,50**. A gana por medias... pero solo por el
  valor 100. Sin él, la media de A sería 28/7 = 4,0.
- Desviación de A: **34,0**; la de B: **2,45**. El test t de Welch da `t` = −0,62 y
  **p ≈ 0,55**: no ve nada.
- Rangos: los siete valores pequeños de A ocupan los rangos 1 a 7, los de B los rangos 8 a 15 y
  el 100 el rango 16. Así que `R₁` = 1 + 2 + … + 7 + 16 = **44**.
- `U₁` = 44 − 8·9/2 = 44 − 36 = **8**; `U₂` = 64 − 8 = 56.
- Con `U` = 8, el p-valor exacto es **0,0104**. Hay evidencia clara de que B tiende a valores
  mayores que A.
- Tamaño del efecto: de las 64 parejas (A, B), 56 tienen el valor de B por encima → probabilidad
  de superioridad **0,875**. El desplazamiento de Hodges-Lehmann es **+19,0** (B menos A).

Y el caso apareado, 12 servidores medidos antes y después de un cambio de configuración, con las
diferencias (después − antes): `-8 -6 -7 -9 -5 -8 -6 -7 -9 -5 -6 +30`.

- Media de las diferencias: **−3,83**, desviación **10,74**.
- Test t apareado: `t` = 1,24, **p ≈ 0,24**. El único valor de +30 se lleva toda la varianza.
- Wilcoxon de rangos con signo: 11 diferencias negativas y una positiva, `W⁺` = 12 →
  **p ≈ 0,034**. La conclusión cambia por completo.

## Código

```python verificable
import numpy as np
from scipy import stats

# A tiene valores tipicos mas bajos, pero un unico valor extremo destroza su varianza.
a = np.array([1, 2, 3, 4, 5, 6, 7, 100])
b = np.array([20, 21, 22, 23, 24, 25, 26, 27])

t, p_t = stats.ttest_ind(a, b, equal_var=False)
u, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")

print(f"t de Welch {t:+.2f}  p {p_t:.4f}")   # -> t de Welch -0.62  p 0.5533
print(f"U {u:.1f}  p exacta {p_u:.4f}")     # -> U 8.0  p exacta 0.0104

# Probabilidad de superioridad y desplazamiento de Hodges-Lehmann.
pares = (b[:, None] - a[None, :]).ravel()
print(f"P(B > A) {(b[:, None] > a[None, :]).mean():.3f}")   # -> P(B > A) 0.875
print(f"desplazamiento {np.median(pares):+.1f}")            # -> desplazamiento +19.0
```

:::claves
- `stats.mannwhitneyu` devuelve un objeto `MannwhitneyuResult`, no una tupla; se lee con `.statistic` y `.pvalue`. El desempaquetado `u, p_u = ...` funciona, pero si algún día la función devuelve un campo más, ese desempaquetado revienta. Y el `U` que devuelve es `min(U₁, U₂)`, no el del primer argumento: aquí `n1·n2 = 64` y devuelve 8, no 56. Da igual el orden en que pases los grupos; lo que **no** da igual es citar el 56 como si fuera el estadístico.
- `alternative` vale `"two-sided"` **solo porque está escrito**. El valor por defecto de SciPy también es `"two-sided"`, pero escribirlo es lo que evita que alguien crea que un p-valor de una cola es el bilateral. Con `alternative="less"` este mismo ejemplo da p = 0,0052, exactamente la mitad.
- `method` decide el p-valor y no está en la llamada: SciPy usa `"auto"`, que elige el cálculo exacto en muestras pequeñas sin empates y la aproximación normal en el resto. Con `n = 8` por grupo, forzar `method="asymptotic"` da 0,0136 en vez del 0,0104 que se cita en la página. Si publicas el p-valor, publica también con qué método salió.
- `b[:, None] - a[None, :]` construye la matriz de 8×8 diferencias por parejas con *broadcasting*: `b[:, None]` es (8, 1) y `a[None, :]` es (1, 8), y NumPy los estira. `.ravel()` la aplana a 64 valores. Si te olvidas de uno de los dos `None`, la resta sale elemento a elemento y te da 8 diferencias en vez de 64, sin ningún error.
- `(b[:, None] > a[None, :])` no compara valores absolutos, compara posiciones: devuelve un array de `True`/`False` y `.mean()` lo convierte en la proporción de parejas en las que gana B, porque `True` es 1. Es exactamente `U₂ / (n1·n2)`, la probabilidad de superioridad: 56/64 = 0,875.
- `stats.rankdata` devuelve `float64` aunque los rangos sean enteros: los empates se reparten con medias (dos empates en el puesto 2 y 3 dan 2,5 a cada uno). Eso es la corrección de empates que menciona la página, y es la razón por la que `R₁` puede salir con decimales y `U` no ser entero.
:::

```python verificable
import numpy as np
from scipy import stats

# Doce pares antes/despues: once mejoran un poco y uno empeora muchisimo.
antes = np.array([210, 195, 230, 205, 220, 200, 215, 225, 199, 231, 208, 222], float)
cambios = np.array([-8, -6, -7, -9, -5, -8, -6, -7, -9, -5, -6, 30], float)

tp, p_t = stats.ttest_rel(antes, antes + cambios)
w, p_w = stats.wilcoxon(antes, antes + cambios)

print(f"t apareado  {tp:+.2f}  p {p_t:.4f}")   # -> t apareado  +1.24  p 0.2422
print(f"Wilcoxon    W {w:.1f}  p {p_w:.4f}")  # -> Wilcoxon    W 12.0  p 0.0342
print(f"mejoran {(cambios < 0).sum()} de {cambios.size}")  # -> mejoran 11 de 12
```

## Errores típicos

- **Decir que Mann-Whitney compara medianas.** Solo es un test de medianas si las dos
  distribuciones tienen la misma forma. Si una es más dispersa o más asimétrica, lo que contrasta
  es la dominancia estocástica, y una diferencia significativa puede convivir con medianas
  iguales. Si quieres comparar medianas, dilo como supuesto y compruébalo, o usa un test de
  permutación sobre la diferencia de medianas.
- **Usar la aproximación normal con pocos datos o con muchos empates.** SciPy elige el método
  exacto por defecto en muchos casos, pero si fuerzas `method="asymptotic"` con `n = 8` el
  p-valor cambia (0,0104 exacto frente a 0,0136 aproximado en el ejemplo). Con muestras pequeñas,
  pide el exacto.
- **Ignorar los empates.** Los empates se resuelven con rangos promedio y la varianza necesita
  corrección; sin ella el p-valor se queda corto. Con datos muy discretos (escalas de 1 a 5) los
  empates son la norma, no la excepción.
- **Confundir el test apareado con el independiente.** Wilcoxon de rangos con signo es para pares
  (mismo sujeto o pareja emparejada); Mann-Whitney es para grupos independientes. Intercambiarlos
  invalida el p-valor.
- **Usar Kolmogorov-Smirnov para comparar medianas.** KS es sensible a cualquier diferencia entre
  las distribuciones —forma, dispersión, colas— y eso está bien si eso es lo que preguntas. Si lo
  que quieres es «¿cuál es más grande?», usa Mann-Whitney.
- **Creer que «no paramétrico» significa «sin supuestos».** Sí los tiene: independencia (o
  simetría de las diferencias, en Wilcoxon), y para leer medianas, igualdad de forma. Lo que no
  supone es una familia de distribuciones concreta.
- **Elegirlo siempre «por seguridad».** Con datos normales pierdes alrededor de un 5 % de
  eficiencia. Con datos muy asimétricos o con outliers, en cambio, ganas mucho. La elección
  depende de lo que veas en los datos, no de la costumbre.

:::practica
enunciado: Dos proveedores de tornillos, con resistencias A = 3, 5, 6, 8, 9 y B = 10, 12, 13, 15, 20. Ordena las diez juntas y calcula U, la probabilidad de superioridad y el p-valor exacto.
pista: Los rangos 1 a 5 son de A y los 6 a 10 de B; U₁ descuenta de la suma de rangos lo que le tocaría por azar.
solucion: R₁ = 1 + 2 + 3 + 4 + 5 = 15, así que U₁ = 15 − 5·6/2 = 0 y U₂ = 25 − 0 = 25. U = 0: ningún par tiene un valor de A por encima de uno de B, y la probabilidad de superioridad es 25/25 = 1. Solo 1 de los C(10,5) = 252 repartos es tan extremo, luego p = 2/252 ≈ 0,008: los proveedores no son intercambiables.
:::

## Comprueba que lo sabes

:::quiz
p: Un grupo tiene los valores 1 2 3 4 5 6 7 100 y el otro 20 21 22 23 24 25 26 27. El test t de Welch da p = 0,55 y Mann-Whitney da p = 0,010. ¿Qué ha pasado?
o: Mann-Whitney está mal, porque las medias son 16,0 y 23,5 y esa diferencia no puede ser significativa
o: La varianza del primer grupo la infla el valor 100, y el test t pierde toda la potencia; el test de rangos no usa magnitudes
o: El test t es más potente que Mann-Whitney siempre, así que el p pequeño es un artefacto
a: 2
e: La desviación del primer grupo sube a 34 por un único dato. Como el test t divide por esa desviación, la diferencia de medias queda enterrada. Mann-Whitney solo mira el orden y ve que siete de los ocho valores del grupo A están por debajo de todos los de B. Ninguno de los dos está mal: miden cosas distintas.
:::

:::quiz
p: Vas a comparar la satisfacción (escala ordinal de 1 a 5) de tres grupos de clientes independientes. ¿Qué test encaja mejor?
o: Un [[anova]] de una vía sobre las puntuaciones 1 a 5
o: Kruskal-Wallis, porque la variable es ordinal y hay muchos empates
o: Un test de Kolmogorov-Smirnov entre los tres pares de grupos
a: 2
e: Con una escala ordinal de 5 puntos, las distancias entre categorías no significan lo mismo y los empates son masivos: la F del ANOVA se apoya en supuestos que no se sostienen. Kruskal-Wallis trabaja con rangos y maneja los empates con corrección. KS responde a otra pregunta (distribuciones completas) y además no está pensado para tres grupos a la vez.
:::

:::quiz
p: El test de Wilcoxon de rangos con signo da W+ = 12 con 12 pares y p = 0,034, mientras el t apareado da p = 0,24. ¿Cuál es la lectura honesta?
o: Wilcoxon es el bueno y el t apareado está equivocado
o: Los dos son válidos y responden a preguntas ligeramente distintas: Wilcoxon dice que las diferencias son mayoritariamente negativas; el t apareado está dominado por un único valor extremo
o: Hay que quedarse con el p más pequeño porque es el que tiene más potencia
a: 2
e: Wilcoxon contrasta si la mediana de las diferencias es cero (bajo simetría), y 11 de 12 diferencias son negativas: eso es información real. El t apareado reparte el peso del valor +30 por toda la varianza y pierde la señal. Quedarse con el p más pequeño sin declarar el criterio es p-hacking.
:::

:::trampa
Un test de rangos no arregla un mal diseño. Si los grupos no son comparables (porque la gente
eligió el tratamiento), el p-valor sigue siendo tan engañoso como el de un test t: la aleatoriedad
del contraste no sustituye a la aleatoriedad de la asignación. Eso es
[[causalidad-vs-correlacion]].
:::
