---
id: test-t
titulo: Test t
fase: 2
nivel: intermedio
rutas: [ds, core]
prerequisitos: [contraste-de-hipotesis, p-valor, distribuciones-continuas, tamano-del-efecto]
tags: [inferencia, medias, comparacion, supuestos]
resumen: Comparar una media con un valor de referencia o dos medias entre sí, eligiendo bien la variante y respetando los supuestos.
fuentes: ["Student (1908), 'The Probable Error of a Mean'", "Welch (1947), 'The Generalization of Student's Problem when Several Different Population Variances are Involved'"]
---

## En una frase

El test t compara una media con un valor de referencia, o dos medias entre sí, dividiendo la
diferencia por su error típico: cuanto mayor sea la diferencia respecto al ruido de la muestra,
menos creíble es que se deba al azar.

## La idea

Tienes 9 llamadas de un centro de atención y el manual promete una media de 240 segundos. Tu
media es 237,7. ¿Está el centro cumpliendo, o esa diferencia de 2,3 segundos es simple
variabilidad entre llamadas?

La pregunta se responde comparando la diferencia con **lo que esa diferencia suele valer por
azar**. Si mides 9 llamadas y entre ellas hay mucha variación (unas de 180 s y otras de 300 s),
una diferencia de 2,3 segundos no dice nada: tu estimación de la media es imprecisa. Si todas
las llamadas duran entre 236 y 239, esa misma diferencia de 2,3 segundos es muy informativa.

Eso es exactamente lo que hace el test t: construye una regla del tipo «diferencia dividida
entre su error típico» y compara el resultado con la distribución t de Student, que es la
distribución de ese cociente cuando la hipótesis nula es cierta y los datos son normales. El
error típico es `s / √n`: baja cuando la muestra crece, y por eso con más datos el mismo efecto
se vuelve más fácil de detectar. Ese es el enlace con el [[tamano-del-efecto]]: el test mezcla
magnitud y cantidad de información.

Hay tres variantes y elegir mal es el error más común:

1. **Una muestra**: comparas la media de un grupo con un valor fijo (240 s, 100 puntos, cero).
2. **Dos muestras independientes**: comparas dos grupos distintos de sujetos.
3. **Dos muestras apareadas**: comparas dos medidas del *mismo* sujeto (antes y después), o
   parejas emparejadas a propósito (gemelos, misma tienda, mismo día).

La tercera no es un capricho. Si mides a las mismas 8 personas antes y después, la variabilidad
entre personas desaparece al restar, y el test se vuelve muchísimo más sensible. Usar la versión
independiente con datos apareados es tirar potencia a la basura y, además, violar el supuesto de
independencia.

:::figura
fichero: test-t-pareado-frente-a-independiente
pie: A la izquierda, los ocho empleados medidos antes y después: cada uno baja entre 6 y 11 s, así que la caída se repite en los ocho y la media cae 8,4 s, mientras que entre personas hay 12 s de diferencia. Esa variabilidad ajena al efecto es la que se cancela al restar. A la derecha se ve la consecuencia: los mismos datos dan un intervalo de ±1,4 s para la diferencia (apareado, el cero queda fuera, p ≈ 0,000002) o de ±12,9 s (independiente, el cero queda dentro, p = 0,19). Compara los dos anchos antes de elegir la variante del test: la elección, no los datos, decide la conclusión.
fuente: figuras/test-t-1.py
:::

## Definición formal

Para una muestra de tamaño `n`, media `x̄` y desviación típica muestral `s` (con `n−1` en el
denominador), frente a un valor de referencia `μ₀`:

:::formula
t = (x̄ − μ₀) / (s / √n) ,   grados de libertad = n − 1
:::

- `x̄` — media de la muestra.
- `μ₀` — valor de referencia de la hipótesis nula.
- `s` — desviación típica muestral.
- `n` — número de observaciones independientes.
- `s / √n` — error típico de la media: cuánto varía `x̄` de muestra a muestra.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x̄` | Media de la muestra | las de la variable (segundos, puntos) | No decide nada por sí sola: lo que se contrasta es `x̄ − μ₀`, su distancia al valor de referencia |
| `μ₀` | Valor de referencia de la hipótesis nula | las de la variable | Es el listón. Acercarlo a la media muestral hace el rechazo más difícil; alejarlo, más fácil |
| `s` | Desviación típica muestral, con `n − 1` en el denominador | las de la variable | Sube → el error típico sube y la t baja. Aquí se nota el `ddof`: con las nueve llamadas, `ddof=0` da 7,79 en vez de 8,26 |
| `n` | Número de observaciones **independientes** | observaciones | Sube → el error típico baja con `√n`. Cuidado: 40.000 registros de 900 usuarios no son 40.000 observaciones |
| `s / √n` | Error típico de la media | las de la variable | Es la unidad con la que se mide la diferencia. Con nueve llamadas vale 2,75 s, así que una diferencia de 2,3 s es menos de un error típico |
| `gl = n − 1` | Grados de libertad del contraste de una muestra | observaciones | Suben con `n` y acercan la t a la normal: con 7 gl el valor crítico es 2,37 y con 100 gl, 1,98 |
| `s_p` | Desviación combinada de los dos grupos (versión de Student) | las de la variable | Solo vale si las varianzas son parecidas; es lo que usa `ttest_ind` con `equal_var=True`, su valor por defecto |
| `t` | La diferencia dividida entre su error típico | adimensional | Su signo depende de en qué orden restes; su tamaño es la evidencia. Con los mismos datos, el apareado da 14,06 y el independiente 1,39 |
| `dᵢ = xᵢ − yᵢ` | Diferencia de cada par, en el test apareado | las de la variable | El contraste se hace sobre su media. Si las diferencias tienen mucha dispersión propia, el apareado pierde su ventaja |
:::

Para dos muestras independientes, la versión clásica (*pooled*, de Student) usa una desviación
combinada:

:::formula
t = (x̄₁ − x̄₂) / (s_p · √(1/n₁ + 1/n₂)) ,   gl = n₁ + n₂ − 2
:::

con `s_p² = ((n₁−1)·s₁² + (n₂−1)·s₂²) / (n₁+n₂−2)`. Esta versión **supone varianzas iguales**.
La versión de Welch no lo supone y usa:

:::formula
t = (x̄₁ − x̄₂) / √(s₁²/n₁ + s₂²/n₂)
:::

con grados de libertad calculados por la fórmula de Welch-Satterthwaite (un número decimal, no
un entero). Welch es la opción por defecto sensata: cuando las varianzas son iguales da casi lo
mismo, y cuando no lo son protege el error de tipo I. En `scipy`, `ttest_ind` usa la versión de
Student salvo que pidas `equal_var=False`.

Para datos apareados, se calcula la diferencia `dᵢ = xᵢ − yᵢ` de cada par y se hace un test de
una muestra sobre esas diferencias con `μ₀ = 0`.

**Supuestos:** observaciones independientes entre sí, y normalidad de la media (o de las
diferencias). Con `n` grande el [[teorema-central-del-limite]] salva la normalidad; con `n`
pequeño y colas muy gordas, el test t no controla bien el error de tipo I y conviene un
[[tests-no-parametricos|test de permutación o de rangos]].

## Ejemplo

Nueve llamadas, en segundos:

```text
231  245  238  226  250  242  235  228  244
```

- Media: 2139 / 9 = **237,67 s**.
- Desviación típica: **8,26 s**.
- Error típico: 8,26 / √9 = 2,75.
- `t` = (237,67 − 240) / 2,75 = **−0,85**, con 8 grados de libertad.
- p-valor bilateral ≈ **0,42**.

No hay evidencia de que la media se aleje de 240. Y fíjate en que el signo de `t` es negativo:
solo indica que la media muestral está por debajo de 240.

Ahora el caso apareado, ocho empleados medidos antes y después de una formación:

```text
antes:    210  195  230  205  220  200  215  225
después:  200  188  219  197  214  191  208  216
diferencias: -10  -7  -11  -8  -6  -9  -7  -9
```

- Diferencia media: **−8,375 s**.
- Desviación típica de las diferencias: **1,685 s**.
- Apareado: `t` = −8,375 / (1,685/√8) = **−14,06**, con 7 grados de libertad → **p ≈ 0,000002**.
- Independiente (Welch), tratando los dos conjuntos como si fueran personas distintas:
  `t` = 1,39, con unos 14 grados de libertad → **p ≈ 0,19**.

El mismo dato, dos conclusiones opuestas. La razón es que las personas difieren mucho entre sí
(desviaciones de 12,2 y 11,8 s) y esa variabilidad ajena al efecto se cancela al restar.

## Código

```python verificable
import numpy as np
from scipy import stats

# Tiempo de atencion (segundos) de 9 llamadas; el manual promete 240 s de media.
tiempos = np.array([231, 245, 238, 226, 250, 242, 235, 228, 244])
t, p = stats.ttest_1samp(tiempos, popmean=240)

print(f"media  {tiempos.mean():.2f}")                             # -> media  237.67
print(f"t {t:.3f}  df {tiempos.size - 1}  p {p:.4f}")            # -> t -0.847  df 8  p 0.4214
```

:::claves
- `stats.ttest_1samp(tiempos, popmean=240)` devuelve un resultado con nombre cuyos dos campos son `statistic` y `pvalue`: `t, p = ...` funciona por ese orden, no porque los nombres importen. Los grados de libertad **no** vienen en el resultado; hay que calcularlos aparte (`tiempos.size - 1`).
- `popmean` es el valor de la media bajo `H₀`, no la media de tus datos, y no tiene valor por defecto: sin él la llamada falla en vez de adivinar. Es el sitio donde más gente se equivoca al pasar de la fórmula al código.
- El p-valor que devuelve es bilateral. Para contrastar una dirección hay que pasar `alternative="greater"` o `"less"`; sin ese argumento, un resultado que iba en la dirección esperada sale con el doble de p del que le corresponde.
- `tiempos.mean()` funciona igual con un array de enteros (devuelve un flotante), pero `.size` es un atributo de numpy y no una función. Si `tiempos` fuera una lista de Python, `ttest_1samp` la aceptaría igual y en cambio `.size` daría `AttributeError` justo en la línea del `print`.
- El signo de `t` (−0,847) solo dice que la media muestral (237,67) queda por debajo de 240: no es un error ni indica un efecto mayor. En un contraste de dos muestras, intercambiar el orden de los argumentos cambia el signo y deja el p-valor intacto.
- `f"t {t:.3f}"` redondea a tres decimales, y el redondeo esconde los ceros: un estadístico de 1e-16 se imprime como `0.000` y parece un cero exacto. Si esa distinción importa, se compara con `abs(t) < 1e-12` en el código, nunca mirando el texto formateado.
:::

```python verificable
import numpy as np
from scipy import stats

# Las mismas 8 personas medidas antes y despues: los datos estan apareados.
antes = np.array([210, 195, 230, 205, 220, 200, 215, 225], float)
despues = np.array([200, 188, 219, 197, 214, 191, 208, 216], float)

tp, pp = stats.ttest_rel(antes, despues)
ti, pi = stats.ttest_ind(antes, despues, equal_var=False)   # Welch, por si acaso

print(f"pareado     t {tp:+.2f}  p {pp:.2e}")     # -> pareado     t +14.06  p 2.18e-06
print(f"independ.   t {ti:+.2f}  p {pi:.4f}")     # -> independ.   t +1.39  p 0.1854
print(f"sd entre personas {antes.std(ddof=1):.2f}")  # -> sd entre personas 12.25
```

## Errores típicos

- **Usar la versión de Student con varianzas muy distintas.** `ttest_ind` de SciPy usa
  `equal_var=True` por defecto. Si un grupo tiene el doble de dispersión que el otro y los
  tamaños son muy distintos, el p-valor puede quedarte corto o largo. Pasa `equal_var=False`
  (Welch) salvo que tengas una razón de peso para combinar varianzas.
- **Aplicar el test independiente a datos apareados.** Es el error del ejemplo: p = 0,19 frente
  a p = 0,000002. Si cada fila del segundo grupo es «la misma unidad» que una del primero, es
  `ttest_rel`.
- **Ignorar la dependencia por grupos.** Si tienes 40.000 registros de 900 usuarios, no tienes
  40.000 observaciones independientes. Los errores típicos salen demasiado pequeños y el p-valor
  demasiado optimista. Agrupa, promedia por usuario o usa errores agrupados.
- **Hacer muchos tests t en vez de un [[anova]].** Con 5 grupos, comparar todos los pares son 10
  tests y la probabilidad de al menos un falso positivo sube del 5 % al 40 %. Usa ANOVA y luego
  un post-hoc, o corrige por [[multiplicidad-y-fdr]].
- **Elegir la cola después de ver los datos.** Pasar de bilateral a unilateral cuando el
  resultado «casi» sale duplica el error de tipo I real. Decide la cola antes de mirar.
- **Interpretar «no rechazo» como «no hay diferencia».** Con 9 llamadas, el intervalo de
  confianza de la media es amplio: no haber detectado nada no es haber demostrado nada. Mira la
  potencia en [[tamano-muestral]].
- **Usarlo con variables que no son medias.** El test t es para medias (o para diferencias
  apareadas). Para proporciones, usa el test de proporciones o [[chi-cuadrado]]; para
  distribuciones completas, un test de rangos.

:::practica
enunciado: Seis tiendas registran sus ventas antes y después de cambiar el escaparate. Las diferencias (después − antes) son −4 · −6 · −5 · −7 · −3 · −5. Contrasta con un test t apareado si hubo efecto, con α = 0,05 y cuantil t (5 gl) de 2,571.
pista: Con datos apareados se contrasta la media de las diferencias dividida entre su error típico, con 5 grados de libertad.
solucion: Media de las diferencias: −30/6 = −5,000. Suma de cuadrados de las desviaciones: 10; s² = 10/5 = 2,000 y s = 1,414. Error típico: 1,414/√6 = 0,577. t = −5,000/0,577 = −8,66. En valor absoluto, 8,66 > 2,571, así que se rechaza la nula (p ≈ 0,0003). Conclusión: al aparear, la variabilidad entre tiendas se cancela y el efecto se detecta con solo seis pares.
:::

## Comprueba que lo sabes

:::quiz
p: Mides el tiempo de respuesta antes y después de un cambio en el mismo grupo de 20 servidores. ¿Qué test usas?
o: Un test t de dos muestras independientes con equal_var=False
o: Un test t de muestras apareadas sobre las diferencias de cada servidor
o: Un [[chi-cuadrado]] de independencia
a: 2
e: Cada servidor es su propio control, así que los datos están apareados: se calcula la diferencia antes-después de cada servidor y se contrasta si su media es cero. Usar la versión independiente ignora esa estructura y desperdicia potencia. El chi-cuadrado es para variables categóricas.
:::

:::quiz
p: Nueve llamadas dan una media de 237,67 s con desviación típica 8,26 s. ¿Cuánto vale el error típico de la media?
o: 8,26, porque es la desviación típica de la muestra
o: 2,75, porque es 8,26 dividido entre la raíz de 9
o: 0,92, porque es 8,26 dividido entre 9
a: 2
e: El error típico de la media es s/√n = 8,26/3 = 2,75. La desviación típica describe la dispersión de las llamadas individuales; el error típico describe la dispersión de la media estimada, y por eso encoge con √n. Dividir entre n sin raíz es un error habitual.
:::

:::quiz
p: Un test t de una muestra da t = −0,85 con 8 grados de libertad. ¿Qué indica el signo negativo?
o: Que el test está mal hecho, porque un estadístico t no puede ser negativo
o: Que la media muestral está por debajo del valor de referencia con el que se contrasta
o: Que la diferencia es grande pero en la dirección contraria a la hipótesis alternativa
a: 2
e: El signo solo refleja la dirección: x̄ − μ₀ es negativo, así que la media de la muestra queda por debajo de μ₀. Nada más. El tamaño del estadístico es lo que habla de la evidencia, y aquí el p-valor bilateral es 0,42.
:::

:::aviso
El test t es robusto a desviaciones moderadas de la normalidad, pero no a valores extremos en
muestras pequeñas. Con 8 o 10 observaciones y un dato que se escapa, el p-valor puede pasar de
0,60 a 0,01 por un único punto. Antes de mirar el p-valor, mira los datos.
:::
