---
id: teorema-central-del-limite
titulo: Teorema central del límite
fase: 1
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [ley-de-los-grandes-numeros, varianza-y-desviacion, distribuciones-continuas]
tags: [probabilidad, inferencia, normal]
resumen: Por qué la media de casi cualquier cosa se distribuye como una normal, de dónde sale el error típico y cuándo la aproximación deja de servir.
fuentes: ["Casella y Berger (2002), 'Statistical Inference'", "Billingsley (1995), 'Probability and Measure'"]
---

## En una frase

La media de muchas variables independientes se distribuye aproximadamente como una normal,
sea cual sea la forma de la distribución original, y de ahí salen el error típico y los
intervalos de confianza.

## La idea

¿Por qué la normal aparece en tantos sitios? Porque casi todo lo que medimos es una **suma**.
El error de un instrumento es la suma de pequeñas imperfecciones; la altura de una persona es
la suma de muchísimos efectos genéticos y ambientales; el tiempo total de un pedido es la suma
de tiempos de cada paso. El teorema central del límite dice que, cuando sumas muchos efectos
independientes y ninguno domina sobre los demás, el resultado se parece a una normal.

Conviene fijar bien qué es lo que se vuelve normal: **no los datos, sino la media**. Si mides
el tiempo entre fallos de un servidor, esa variable es exponencial y sigue siendo exponencial
por mucho que midas un millón de fallos. Lo que se vuelve normal es la distribución de la
**media** de muchas observaciones.

La consecuencia práctica es enorme y explica media estadística aplicada:

- Puedes hacer inferencia sobre una media sin saber la distribución original, siempre que tengas
  suficientes datos independientes.
- La dispersión de la media alrededor de `μ` es `σ/√n`, el **error típico**, y de ahí salen los
  intervalos de confianza y los contrastes.
- La suma también es aproximadamente normal, con media `n·μ` y varianza `n·σ²`.

Y ahora los límites, que es donde se cometen los errores caros. El teorema pide independencia
(o dependencia muy débil) y varianza finita. La pregunta «¿a partir de qué `n`?» no tiene una
respuesta universal: depende de lo asimétrica y de lo gorda que sea la cola de la distribución
original. Con una exponencial, `n = 30` ya da una aproximación decente en el centro; con datos
de ingresos o con cuentas de clics, que son mucho más asimétricos, `n = 30` se queda corto y
hacen falta cientos o miles. Y con varianza infinita (colas tan gordas que la media no tiene
desviación típica finita) el teorema no se aplica: la media estandarizada no converge a una
normal, y usar `σ/√n` da intervalos que no cubren lo que dicen cubrir.

## Definición formal

Sean `X₁, …, Xₙ` variables **iid** con media `μ` y varianza finita `σ²`, y sea
`X̄ₙ = (1/n)·Σᵢ Xᵢ` la media muestral. Entonces:

:::formula
√n · (X̄ₙ − μ) / σ  →  N(0, 1)   cuando n → ∞
:::

La flecha `→` significa **convergencia en distribución**: la función de distribución de la
expresión de la izquierda se acerca a la de la normal estándar. De forma equivalente y más
práctica:

:::formula
X̄ₙ ≈ N(μ, σ²/n)   y   Σᵢ Xᵢ ≈ N(n·μ, n·σ²)
:::

- `X̄ₙ` — media de las `n` observaciones; `Σᵢ Xᵢ` — su suma.
- `μ` — esperanza de cada observación; `σ²` — su varianza; `n` el tamaño de la muestra.
- `σ/√n` — **error típico** de la media, que es su desviación típica.
- `N(0, 1)` — normal estándar, de media 0 y varianza 1.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de observaciones independientes que se promedian | observaciones | El error típico baja como `1/√n` y la aproximación a la normal mejora; no cambia la forma de los datos originales |
| `μ` | La esperanza de cada observación | las de `X` | Centra la distribución de la media; el intervalo de confianza se desplaza con ella |
| `σ²` | La varianza de cada observación | las de `X`, al cuadrado | La media muestral se dispersa con `σ`, no con `σ²`; el margen del intervalo crece en la misma proporción |
| `X̄ₙ` | La media de las `n` observaciones | las de `X` | Es la variable que se vuelve normal; su desviación es `σ/√n`, no `σ` |
| `σ/√n` | El error típico de la media | las de `X` | Es la unidad del intervalo: `x̄ ± 1,96 · σ/√n` para el 95 % con `σ` conocida |
| `E[X − μ]³/σ³` | La asimetría de la distribución original | adimensional | Cuanto mayor es, más datos hacen falta para que la normal valga en las colas: el error de aproximación va como `1/√n` y empeora con ella |
:::

Dos figuras para las dos afirmaciones del teorema: la primera, que la media se vuelve normal
aunque los datos no lo sean; la segunda, que la aproximación se rompe antes en las colas.

:::figura
fichero: tcl-media-normal-y-cola
pie: A la izquierda, la media de 1 dato conserva la forma de la exponencial y la de 30 ya es una campana; los datos originales siguen siendo exponenciales por muchos que añadas, lo que se vuelve normal es su media. A la derecha, los cuantiles de la media de 200 datos se pegan a la diagonal en el centro y se separan un poco en los extremos, mucho menos que una t de Student. Mira la zona central y la zona extrema por separado: si tu decisión depende del extremo, `n = 30` no basta.
fuente: figuras/teorema-central-del-limite-1.py
:::

**Cómo se usa.** Con `σ` conocida, un intervalo de confianza del 95 % para `μ` es
`x̄ ± 1,96 · σ/√n`. Si `σ` se estima con la muestra (`s`), se sustituye 1,96 por el cuantil de
la t de Student con `n − 1` grados de libertad: con pocos datos la diferencia es notable
(2,571 con 5 grados de libertad frente a 1,96).

**Precisión de la aproximación.** El error de la aproximación es del orden de
`E[|X − μ|³] / (σ³·√n)`: mejora con `√n` y empeora con la asimetría. Por eso una distribución
simétrica converge mucho antes que una con cola larga, y por eso el famoso «`n = 30`» es una
regla práctica y no un teorema.

## Ejemplo

Toma una exponencial de media 1, que es claramente asimétrica (su densidad cae de golpe desde
el 1 y arrastra una cola larga). Genera 4.000 muestras de tamaño 30 y mira la distribución de
las medias:

```
media de las medias  0,9967      (el valor teórico es 1)
error tipico         0,1851      (el teorico es 1/raiz de 30 = 0,1826)
dentro de 1 error    0,6825      (la normal predice 0,6827)
dentro de 2 errores  0,9527      (la normal predice 0,9545)
asimetria restante   0,4041      (la exponencial original tiene 2)
```

El centro de la distribución ya es indistinguible del de una normal, y los porcentajes dentro
de uno y dos errores típicos clavan los valores teóricos. La asimetría, en cambio, no ha
desaparecido: ha bajado de 2 a 0,4. Con `n = 30` la aproximación es buena en el centro y
regular en las colas; si tu decisión depende de la cola, necesitas más datos o un método que no
dependa del TCL.

**De dónde sale el error típico.** Si el tiempo de atención a un cliente tiene `σ = 12`
minutos y mides 100 clientes, la media tiene un error típico de `12/√100 = 1,2` minutos, y el
margen del 95 % es `1,96 · 1,2 = 2,352` minutos. Para bajarlo a la mitad (`0,6`) hacen falta
400 clientes, cuatro veces más.

## Código

```python verificable
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)

# La exponencial es muy asimetrica; la media de 30 ya se comporta como una normal.
muestras = rng.exponential(scale=1.0, size=(4000, 30))
medias = muestras.mean(axis=1)

print(f"media de las medias = {medias.mean():.4f}")                        # -> 0.9967
print(f"error tipico        = {medias.std(ddof=1):.4f}")                  # -> 0.1851
print(f"teorico 1/sqrt(30)  = {1 / np.sqrt(30):.4f}")                      # -> 0.1826
print(f"dentro de 1 error   = {(np.abs(medias - 1) < 1 / np.sqrt(30)).mean():.4f}")   # -> 0.6825
print(f"dentro de 2 errores = {(np.abs(medias - 1) < 2 / np.sqrt(30)).mean():.4f}")   # -> 0.9527
print(f"asimetria restante  = {stats.skew(medias, bias=False):.4f}")       # -> 0.4041
```

:::claves
- `rng.exponential(scale=1.0, size=(4000, 30))` genera una matriz de 4.000 muestras de 30 datos y `.mean(axis=1)` promedia cada fila. Con `axis=0` promediarías cada una de las 30 posiciones a lo largo de las 4.000 muestras: obtendrías 30 números que no son medias de nada útil, y la desviación de esos números saldría unas 12 veces menor (`1/√4000` frente a `1/√30`), porque cada uno promedia 4.000 datos en vez de 30.
- `scale` en `exponential` es la media (`1/λ`), no la tasa. `scale=1.0` es la exponencial de tasa 1; si el ejercicio hablara de una tasa de 2 habría que escribir `scale=0.5`.
- `medias.std(ddof=1)` mide la dispersión **de las 4.000 medias**, que es el error típico. No es la desviación de los datos originales (que vale 1): confundir las dos es el error de un orden de magnitud que denuncia la sección de errores típicos.
- `(np.abs(medias - 1) < 1 / np.sqrt(30)).mean()` compara contra el error típico **teórico** `1/√30`, no contra el estimado. Por eso el porcentaje que sale (0,6825) se puede comparar directamente con 0,6827 sin arrastrar el error de estimar `σ`.
- `stats.skew(medias, bias=False)` sigue dando 0,4041 después de promediar 30 datos: la simetría mejora pero no desaparece. Si el script imprimiera solo los porcentajes centrales, parecería que la normal ya es exacta; la asimetría restante es la que avisa de que en la cola no lo es.
- Cambiar `size=(4000, 30)` por `size=(4000, 200)` dejaría el error típico en `1/√200 = 0,0707` y la asimetría bajaría a la mitad aproximadamente: el mismo código sirve para ver que la convergencia es lenta y gradual, y por eso conviene dibujarla en vez de fiarse de una regla.
:::

```python verificable
import numpy as np

# Error tipico y margen del 95 % para la media de un tiempo de atencion.
sigma, n = 12.0, 100
error_tipico = sigma / np.sqrt(n)
print(f"error tipico   = {error_tipico:.4f}")          # -> 1.2000
print(f"margen 95 %    = {1.96 * error_tipico:.4f}")   # -> 2.3520

# Cuadruplicar n divide el error tipico entre 2.
print(f"con n = 400    = {sigma / np.sqrt(400):.4f}")  # -> 0.6000
```

## Errores típicos

- **Creer que los datos se vuelven normales.** No: lo que se aproxima a una normal es la
  distribución de la **media**. Una muestra de 10.000 tiempos exponenciales sigue teniendo
  forma exponencial; su histograma no se acercará a una campana por muchos datos que añadas.
- **Aplicar la regla de `n = 30` a cualquier cosa.** La velocidad de convergencia depende de la
  asimetría y de las colas. Con distribuciones muy sesgadas (ingresos, importes de siniestros,
  conteos de clics) puede hacer falta un `n` mucho mayor, y con varianza infinita el teorema
  simplemente no se aplica.
- **Ignorar la dependencia.** En una serie temporal con autocorrelación, los datos no son
  independientes y la varianza de la media no es `σ²/n`. Usar `σ/√n` con esos datos produce
  intervalos demasiado estrechos y contrastes que rechazan demasiado a menudo.
- **Confundir la desviación típica de los datos con el error típico de la media.** `σ` describe
  cuánto varía una observación; `σ/√n` describe cuánto varía la media. Con 100 datos, el error
  típico es diez veces menor, y decir «la media es 30 ± 12» cuando toca «30 ± 1,2» es un error
  de un orden de magnitud.
- **Usar 1,96 con varianza estimada y pocos datos.** Si `σ` no se conoce y `n` es pequeño, toca
  la t de Student: con 6 observaciones el cuantil es 2,571, no 1,96. Ignorarlo estrecha el
  intervalo y aumenta los falsos positivos.
- **Pensar que el TCL arregla una muestra sesgada.** El teorema describe la variabilidad
  alrededor de la esperanza de **tu** distribución de muestreo. Si la muestra no es
  representativa, la media converge al valor equivocado con un intervalo de confianza
  impecable alrededor de ese error.

:::practica
enunciado: Una muestra de 64 pedidos da un tiempo medio de 42 minutos y una desviación típica muestral de 8 minutos. Calcula el intervalo de confianza del 95 % para la media y los pedidos necesarios para que el margen baje a 0,5 minutos.
pista: El margen es cuantil · σ/√n; para el tamaño necesario despeja n de esa igualdad y redondea hacia arriba.
solucion: Error típico = 8/√64 = 1,0 minuto, luego margen = 1,96 · 1,0 = 1,96 e intervalo [40,04; 43,96]. Para un margen de 0,5: n = (1,96 · 8 / 0,5)² = 31,36² ≈ 983,4, es decir 984 pedidos, unas 15 veces más que 64. Conclusión: reducir el margen a la cuarta parte cuesta quince veces más muestra, porque el error típico va con la raíz de n.
:::

## Comprueba que lo sabes

:::quiz
p: Mides tiempos de espera (distribución exponencial, muy asimétrica) con muestras de tamaño 30. ¿Qué afirma el teorema central del límite?
o: Que los tiempos de espera se distribuyen como una normal
o: Que la media de cada muestra de 30 se distribuye aproximadamente como una normal
o: Que la media muestral es exactamente igual a la media poblacional
a: 2
e: El TCL habla de la distribución de la media (o de la suma), no de la variable original, que sigue siendo exponencial. Con n = 30 la aproximación es buena en el centro pero la asimetría residual todavía se nota en las colas.
:::

:::quiz
p: El tiempo de atención tiene sigma = 12 minutos. Con 100 clientes, ¿cuál es el error típico de la media?
o: 12 minutos, porque no depende del tamaño de la muestra
o: 1,2 minutos, porque es sigma entre la raíz de 100
o: 0,12 minutos, porque es sigma entre 100
a: 2
e: El error típico es sigma/raíz de n = 12/10 = 1,2. Dividir entre n en lugar de entre su raíz subestima el error: harían falta 10.000 clientes, no 100, para bajarlo a 0,12.
:::

:::quiz
p: ¿Por qué el TCL no basta para usar 1,96 cuando estimas la varianza con 6 observaciones?
o: Porque con pocos datos el cuantil correcto es el de la t de Student, que es mayor
o: Porque el TCL solo vale para muestras mayores de 1.000
o: Porque la varianza muestral es siempre menor que la poblacional
a: 1
e: Al estimar sigma con la muestra se añade incertidumbre, y esa incertidumbre engorda las colas: con 5 grados de libertad el cuantil del 97,5 % es 2,571 en vez de 1,96. El TCL sigue siendo válido para la forma, pero el cuantil debe salir de la t.
:::
