---
id: multiplicidad-y-fdr
titulo: Multiplicidad y FDR
fase: 2
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [p-valor, contraste-de-hipotesis, errores-tipo-i-ii-y-potencia, tamano-del-efecto]
tags: [inferencia, multiplicidad, fdr, bonferroni]
resumen: Comparar cien métricas a la vez dispara los falsos positivos; Bonferroni controla el error en familia y Benjamini-Hochberg la proporción de falsos.
fuentes: ["Benjamini y Hochberg (1995), 'Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing'", "Holm (1979), 'A Simple Sequentially Rejective Multiple Test Procedure'"]
---

## En una frase

Cuando contrastas muchas hipótesis a la vez, la probabilidad de encontrar al menos un falso
positivo crece muy deprisa; Bonferroni la mantiene por debajo de `α` a costa de perder potencia,
y Benjamini-Hochberg controla en su lugar la proporción esperada de falsos entre los hallazgos
que declaras.

## La idea

Imagina que pruebas 100 ideas de trading, o 100 métricas de producto, o 20.000 genes, y que
**ninguna de ellas funciona de verdad**. Cada contraste individual tiene un 5 % de dar un falso
positivo, así que esperarías unos 5 hallazgos «significativos» por puro azar. Y la probabilidad de
que aparezca al menos uno no es del 5 %: es

`1 − 0,95¹⁰⁰ = 0,9941`, prácticamente la certeza.

Ese es el problema de la multiplicidad. No es un matiz teórico: es la explicación de una parte
enorme de los resultados que no se replican. La primera vez que ves un p-valor de 0,03 en una
tabla de 200 correlaciones, hay que asumir que lo más probable es que sea ruido.

Hay dos formas de arreglarlo y hay que elegir con cuidado, porque controlan cosas distintas:

- **FWER** (*family-wise error rate*): la probabilidad de cometer **al menos un** falso positivo
  en toda la familia. Es lo que controla Bonferroni. Es un criterio duro: si haces 20.000 tests,
  mantener el FWER en el 5 % obliga a un umbral de 0,0000025 por test y no sobrevive casi nada.
- **FDR** (*false discovery rate*): la **proporción esperada de falsos** entre las hipótesis que
  rechazas. Es lo que controla Benjamini-Hochberg. Un FDR del 5 % significa: de cada 100
  hallazgos que declaro, unos 5 serán falsos de media. Es un criterio muchísimo más útil cuando
  estás haciendo un cribado exploratorio y esperas que una parte de los hallazgos sea real.

La regla práctica: si un solo falso positivo te arruina el análisis (un ensayo clínico
confirmatorio, una decisión irreversible), controla el FWER. Si estás filtrando candidatos para
seguir investigándolos, controla el FDR.

Hay una tercera fuente de multiplicidad, más silenciosa que las tablas de p-valores: **las
decisiones que tomas después de mirar los datos**. Probar tres definiciones de «usuario activo»,
quitar los outliers que estropean la gráfica, cambiar la ventana temporal, añadir una covariable y
volver a mirar. Cada una de esas bifurcaciones es un contraste implícito, y ninguna aparece en tu
lista de tests. Ese es el mecanismo del p-hacking, y no se corrige con ninguna fórmula: se corrige
decidiendo el análisis antes de ver los datos.

## Definición formal

Planteas `m` hipótesis nulas, de las cuales `m₀` son verdaderas. Tras aplicar tus contrastes al
nivel `α`, llamas `R` al número de hipótesis rechazadas y `V` al número de rechazos que eran
falsos positivos. Entonces:

:::formula
FWER = P(V ≥ 1) ,   FDR = E[ V / max(R, 1) ]
:::

- `m` — número de contrastes de la familia.
- `m₀` — cuántas de las hipótesis nulas son de verdad ciertas (nunca lo sabes).
- `R` — rechazos observados; `V` — rechazos que son errores.
- `max(R, 1)` — evita dividir entre cero cuando no rechazas nada; en ese caso el cociente se
  define como 0.

**Bonferroni.** Rechaza la hipótesis `i` si:

:::formula
pᵢ ≤ α / m
:::

Se demuestra con la desigualdad de la unión: `P(∪ᵢ Aᵢ) ≤ Σᵢ P(Aᵢ) = m · (α/m) = α`. Es válido con
cualquier estructura de dependencia, y por eso es tan usado y tan conservador: en cuanto los tests
están correlacionados (y casi siempre lo están), el umbral real es más estricto de lo necesario.

**Holm (step-down).** Ordena los p-valores `p₍₁₎ ≤ p₍₂₎ ≤ … ≤ p₍ₘ₎`. Busca el menor `k` tal que

:::formula
p₍ₖ₎ > α / (m − k + 1)
:::

y rechaza las `k − 1` primeras. Controla el FWER igual que Bonferroni pero siempre rechaza al
menos tanto, así que no hay ninguna razón para preferir Bonferroni sobre Holm.

**Benjamini-Hochberg (step-up).** Con los mismos p-valores ordenados, busca el **mayor** `k` tal
que:

:::formula
p₍ₖ₎ ≤ (k / m) · α
:::

y rechaza todas las hipótesis hasta `k`. Es decir, cada p-valor se compara con una fracción
creciente del nivel: el más pequeño contra `α/m`, el segundo contra `2α/m`, y así hasta el mayor,
que se compara contra `α`. Controla el FDR en `α` si los tests son independientes o cumplen una
dependencia positiva razonable. Para dependencia arbitraria existe la variante de
Benjamini-Yekutieli, que sustituye `α` por `α / Σᵢ(1/i)` y es bastante más conservadora.

El **q-valor** de una hipótesis es el FDR más pequeño al que esa hipótesis sería rechazada; en la
práctica es el p-valor ajustado por BH, y es la cifra que se publica.

:::figura
fichero: multiplicidad-umbrales-y-fwer
pie: A la izquierda, cada p-valor ordenado se compara con dos listones: la recta creciente k·α/m de Benjamini-Hochberg y la recta plana α/m = 0,005 de Bonferroni. Los círculos verdes marcan los cuatro hallazgos que declara BH (corta en el cuarto, porque el quinto p = 0,031 supera su umbral de 0,025) y el círculo rojo, el único que sobrevive a Bonferroni. A la derecha, la probabilidad de colar al menos un falso positivo cuando todas las hipótesis son ciertas: pasa del 5 % con una prueba al 99,4 % con cien. Lo que hay que llevarse es que ambas correcciones usan los mismos p-valores y solo cambian el listón, y que el problema no es de un test, es de la familia entera.
fuente: figuras/multiplicidad-y-fdr-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `m` | Numero de contrastes de la familia | contrastes | Es el divisor de Bonferroni y el que fija la pendiente de BH: al subir, los umbrales se hacen mas estrictos y sobreviven menos hallazgos. Elegir `m` a posteriori (corregir por los 10 p mas pequeños habiendo mirado 100) deja el FDR real en el 50 %, no en el 5 % |
| `m0` | Cuantas de las hipotesis nulas son de verdad ciertas | contrastes | Nunca lo sabes y por eso se estima. Si `m0` es mucho menor que `m` (casi todo tiene efecto real), las correcciones son demasiado conservadoras y te quedas corto declarando hallazgos |
| `R` | Hipotesis rechazadas: los hallazgos que declaras | hallazgos | Sube cuando bajas el liston. El FDR se define sobre lo que declaras, no sobre lo que miraste: por eso BH con `R = 0` no tiene denominador y el cociente se define como 0 |
| `V` | Rechazos que eran falsos positivos | hallazgos | Es lo que no ves nunca. Bonferroni limita `P(V >= 1)`; BH limita la media de `V / max(R, 1)`. Es la diferencia entre prometer que casi no habra ningun falso positivo y prometer que una fracción conocida de tus hallazgos lo será |
| `alpha` | Nivel que controlas | probabilidad | Con Bonferroni es el FWER; con BH es el FDR. El mismo 0,05 significa cosas muy distintas: en el ejemplo, 1 hallazgo frente a 4. Bajarlo reduce los falsos positivos y aumenta los falsos negativos |
| `p_i` | El p-valor de cada contraste | probabilidad, de 0 a 1 | Un p-valor mas pequeño entra antes en la lista ordenada. Lo que decide no es su valor suelto sino su puesto `k`: el mismo 0,019 se rechaza en el puesto 4 y no se rechazaria en el puesto 20 |
| `k` | Puesto que ocupa un p-valor al ordenarlos | posición | Sube el umbral de BH (`k·alpha/m`) y no toca el de Bonferroni. Por eso BH es un procedimiento *step-up*: busca el mayor `k` que cumple y rechaza todo lo anterior, aunque algunos de esos p-valores no cumplieran su propio umbral |
| `q` | q-valor: el FDR mas pequeño al que esa hipotesis se rechaza | probabilidad, de 0 a 1 | Es el p-valor ajustado que se publica. Nunca es menor que el p-valor original, y no es una probabilidad condicional por hallazgo: es el FDR de un procedimiento, no la probabilidad de que un hallazgo concreto sea falso |
:::

## Ejemplo

Diez métricas comparadas a la vez, con sus p-valores ordenados y los umbrales de BH:

```text
k   p ordenado   umbral BH (k*0,05/10)   Bonferroni (0,005)
1      0,001            0,005                  rechaza
2      0,009            0,010                  no
3      0,011            0,015                  no
4      0,019            0,020                  no
5      0,031            0,025                  no
6      0,048            0,030                  no
7      0,120            0,035                  no
8      0,340            0,040                  no
9      0,510            0,045                  no
10     0,880            0,050                  no
```

- Bonferroni: solo el p = 0,001 baja de 0,005 → **1 hallazgo**.
- BH: el mayor `k` que cumple `p₍ₖ₎ ≤ k·0,05/10` es `k = 4` (0,019 ≤ 0,020; el quinto ya no:
  0,031 > 0,025) → **4 hallazgos**, con un FDR esperado del 5 %.

Ninguno de los dos está «mal»: Bonferroni te promete que la probabilidad de haber colado algún
falso positivo es como mucho del 5 %; BH te promete que, de los cuatro hallazgos, en media 0,2
serán falsos. Son promesas distintas y la segunda suele ser la que quieres cuando exploras.

El caso extremo, con 100 métricas que **no dependen de nada**:

```text
p < 0,05 sin corregir: 6 de 100
p < 0,05/100:          0
p < 0,05/10:           1
```

Las seis primeras son ruido puro. Y fíjate en la tercera línea: si solo declaras los diez
p-valores más pequeños como «tu familia» y corriges por 10, uno sobrevive y te lo crees. Ese es
el truco más común para esquivar la corrección.

## Código

```python verificable
import numpy as np

# Diez p-valores de diez metricas medidas sobre el mismo experimento.
p = np.array([0.001, 0.009, 0.011, 0.019, 0.031, 0.048, 0.120, 0.340, 0.510, 0.880])
m, alfa = p.size, 0.05

ordenados = np.sort(p)
umbral_bh = np.arange(1, m + 1) / m * alfa          # k * alfa / m
pasa = ordenados <= umbral_bh
k = int(np.max(np.where(pasa)[0]) + 1) if pasa.any() else 0

print(f"Bonferroni sobreviven {int((p <= alfa / m).sum())} con umbral {alfa / m:.4f}")
# -> Bonferroni sobreviven 1 con umbral 0.0050
print(f"BH sobreviven {k} con umbral {umbral_bh[k - 1]:.4f}")
# -> BH sobreviven 4 con umbral 0.0200
```

:::claves
- `np.where(pasa)` sobre un array **booleano de una dimensión** devuelve una tupla con un array de índices, por eso hay que añadirle `[0]`. Sobre una matriz devolvería dos arrays (filas y columnas) y ese `[0]` te daría solo las filas: si algún día `pasa` es 2D, el cálculo del corte sale mal sin ningún error.
- El `+ 1` de `int(np.max(np.where(pasa)[0]) + 1)` convierte un índice (que empieza en 0) en un número de hallazgos, pero existe una forma más corta y menos frágil de contar la misma cosa: `pasa.sum()`, que aquí también da 4. Y con `pasa.sum()` no hace falta la guarda `if pasa.any()`: sumar un array vacío de `False` da 0.
- Esa guarda **es imprescindible**: si ningún p-valor baja del umbral, `np.where(pasa)[0]` es un array vacío y `np.max` de un array vacío lanza un error. El `else 0` no es estilo: es que BH con cero hallazgos es un resultado normal cuando tienes 20.000 contrastes.
- BH es un procedimiento *step-up* y eso se lee en la línea: se busca el **mayor** `k` que cumple (`np.max`), no el primero, y se rechaza **todo** hasta ahí. En este ejemplo los cuatro primeros p-valores cumplen su propio umbral (0,001 ≤ 0,005, 0,009 ≤ 0,010, 0,011 ≤ 0,015 y 0,019 ≤ 0,020), así que el corte coincide con el del primer fallo. La diferencia entre las dos lecturas aparece cuando un p-valor intermedio no cumple el suyo y uno posterior sí: entonces ese intermedio también se declara, y buscar el primer `k` que falla es un error de lectura del procedimiento, no de código.
- `umbral_bh[k - 1]` usa el índice del último que cumple, que es exactamente `k` en notación de matemáticas: `k` hallazgos, índice `k − 1` en un array de Python. Si pones `umbral_bh[k]` imprimes el umbral del siguiente, que es un número más grande y más bonito, y por eso el error pasa desapercibido.
- Cuidado con `np.diff` si lo aplicas a estos p-valores: `np.diff` devuelve **un elemento menos** que el array original (9 en vez de 10) y eso desalinea los umbrales con los p-valores. Para calcular el corte hay que trabajar con `np.sort(p)` y `np.arange(1, m + 1)`, que sí tienen la misma longitud.
:::

```python verificable
import numpy as np

# Cien metricas que NO dependen de nada: los p-valores son uniformes por construccion.
rng = np.random.default_rng(0)
p = rng.uniform(0, 1, 100)

print(f"p < 0.05 sin corregir: {(p < 0.05).sum()}")        # -> p < 0.05 sin corregir: 6
print(f"p < 0.05/100:          {(p < 0.05 / 100).sum()}")  # -> p < 0.05/100:          0
print(f"p < 0.05/10:           {(p < 0.05 / 10).sum()}")   # -> p < 0.05/10:           1
print(f"FWER con 100 tests:    {1 - 0.95**100:.4f}")       # -> FWER con 100 tests:    0.9941
```

## Errores típicos

- **No corregir nada cuando has probado 40 subgrupos y publicas el que salió.** Es el caso más
  frecuente en analítica de producto: «los usuarios de Android mayores de 45 en Cataluña mejoran
  un 12 %». Con 40 subgrupos, alguno sale por azar casi seguro.
- **Corregir por el número equivocado de contrastes.** La familia no son «los 10 p-valores más
  pequeños que he mirado», son **todos** los contrastes que hiciste. Si probaste 100 y corriges
  por 10, el FDR real es del 50 %, no del 5 %.
- **Usar Bonferroni para un cribado masivo.** Con 20.000 genes y un umbral de 0,0000025 no
  sobrevive nada, ni siquiera efectos reales. Ahí el FDR es la herramienta correcta.
- **Interpretar el FDR como «el 5 % de mis hallazgos son falsos».** Es el **valor esperado** de la
  proporción de falsos entre los rechazados, y bajo supuestos de independencia o dependencia
  positiva. No es una garantía sobre tu lista concreta ni una probabilidad condicional por
  hallazgo.
- **Aplicar BH con tests fuertemente dependientes sin comprobarlo.** Si la dependencia puede ser
  arbitraria, la variante de Benjamini-Yekutieli mantiene el control a costa de potencia.
- **Confundir FWER con FDR al citar el resultado.** «Controlo el error al 5 %» significa cosas
  distintas con cada método, y la diferencia es enorme: en el ejemplo, 1 hallazgo frente a 4.
- **Corregir por multiplicidad y no por el resto del proceso.** Si además elegiste el mejor de 300
  modelos por validación cruzada, ese sesgo de selección es otra multiplicidad que ninguna
  corrección de p-valores arregla. Es lo mismo que ocurre al elegir hiperparámetros y reportar el
  resultado como si fuera nuevo.
- **Creer que pre-registrar elimina la multiplicidad.** La reduce muchísimo, pero el análisis
  sigue teniendo varias métricas y varios contrastes; el pre-registro lo que hace es fijar la
  familia de antemano.

## Comprueba que lo sabes

:::quiz
p: Pruebas 100 métricas, ninguna de ellas tiene efecto real, y usas alpha = 0,05 en cada una sin corregir. ¿Qué esperas?
o: Exactamente 0 falsos positivos, porque las métricas son independientes
o: Unos 5 falsos positivos de media, y una probabilidad cercana al 99 % de que haya al menos uno
o: Un 5 % de probabilidad de que aparezca al menos un falso positivo
a: 2
e: Cada test mantiene su 5 % individual, así que se esperan 0,05 x 100 = 5 falsos positivos. La probabilidad de al menos uno es 1 - 0,95^100 = 0,9941. El error clásico es confundir el 5 % por test con el 5 % de la familia.
:::

:::quiz
p: ¿Qué controla Benjamini-Hochberg que no controla Bonferroni?
o: La proporción esperada de falsos positivos entre las hipótesis rechazadas
o: La probabilidad de cometer al menos un falso positivo
o: La probabilidad de cometer un falso negativo
a: 1
e: BH controla el FDR, que es E[V/max(R,1)]: de cada 100 hallazgos declarados, cuántos son falsos de media. Bonferroni (y Holm) controlan el FWER, la probabilidad de al menos un falso positivo en toda la familia. Ninguno de los dos habla directamente de falsos negativos, aunque un umbral más estricto los aumenta.
:::

:::quiz
p: Diez p-valores ordenados son 0,001, 0,009, 0,011, 0,019, 0,031, 0,048, 0,12, 0,34, 0,51 y 0,88. ¿Cuántos rechaza BH con alpha = 0,05?
o: 1, porque ese es el resultado de Bonferroni
o: 4, porque el cuarto p-valor (0,019) sigue por debajo de su umbral (0,020) y el quinto ya no
o: 6, porque los seis primeros están por debajo de 0,05
a: 2
e: BH compara cada p-valor ordenado con k x 0,05/10. El cuarto umbral es 0,020 y 0,019 lo cumple; el quinto umbral es 0,025 y 0,031 no lo cumple, así que se corta en k = 4 y se rechazan esos cuatro. Comparar directamente con 0,05 ignora la corrección.
:::

:::practica
enunciado: Una empresa prueba 24 variantes de una página y mide conversión, tiempo en página y número de clics por sesión. Obtiene 72 p-valores y tres bajan de 0,05 (0,004, 0,021 y 0,043), todos en la misma variante y en la métrica de conversión. ¿Cuántos hallazgos declaras con Bonferroni y cuántos con BH al 5 %?
pista: Con m = 72, el umbral de Bonferroni es 0,05/72. Para BH, compara cada p-valor ordenado con k·0,05/72.
solucion: El umbral de Bonferroni es 0,05/72 = 0,000694 y ninguno de los tres p-valores baja de ahí, así que no declaras nada. Con BH, la lista ordenada empieza en 0,004, 0,021 y 0,043, y los umbrales para k = 1, 2 y 3 son 0,000694, 0,001389 y 0,002083: ninguno de los tres los cumple (0,004 > 0,000694, 0,021 > 0,001389, 0,043 > 0,002083). Tampoco lo cumplirían los k mayores, porque exigirían que casi todos los 72 p-valores fueran pequeños. La conclusión honesta es que, con 72 contrastes, esos tres resultados son compatibles con el azar. Además los tres están en la misma variante y la misma métrica, lo que indica que las métricas están correlacionadas y que la familia efectiva es menor que 72.
:::

:::trampa
Un p-valor de 0,03 entre 200 correlaciones no es un hallazgo: es exactamente lo que se espera por
azar (0,05 · 200 = 10). Antes de contar el resultado, cuenta cuántas cosas has mirado. Si no
llevas esa cuenta, ya has perdido.
:::
