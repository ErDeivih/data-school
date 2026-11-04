---
id: monitorizacion-de-drift
titulo: Deriva de datos y de concepto
fase: 4
nivel: avanzado
rutas: [de, ds, quant]
prerequisitos: [calidad-de-datos, observabilidad-de-datos, mlops-y-cicd-de-modelos]
tags: [drift, monitorizacion, produccion, mlops]
resumen: Un modelo solo vale para la distribución con la que se entrenó; la deriva es el aviso de que el mundo cambió y la métrica de negocio todavía no se ha enterado.
fuentes: ["Gama, Žliobaitė et al. (2014), 'A survey on concept drift adaptation'"]
---

## En una frase

Un modelo aprende una relación que solo es cierta para los datos con los que se entrenó, y la
monitorización de deriva comprueba cada día si esa relación sigue siendo cierta, para avisar
mucho antes de que el fallo aparezca en la métrica de negocio.

## La idea

Piensa en un mapa de carreteras de 2015. El mapa no se ha equivocado: describía bien el
terreno cuando se dibujó. Lo que ha cambiado es el terreno, porque han abierto una
circunvalación. Un modelo en producción es ese mapa: la exactitud que mediste el día del
despliegue era real, y a los ocho meses puede estar dando vueltas por una rotonda que ya no
existe.

Hay tres formas distintas de que eso pase, y confundirlas lleva a la solución equivocada:

1. **Deriva de datos** (*covariate shift*): cambia la distribución de las entradas, `P(X)`,
   pero la relación entre entradas y objetivo sigue igual. Ejemplo: tu modelo de demanda se
   entrenó con un 70 % de tráfico móvil y ahora es el 92 %. La relación «más clics, más
   pedidos» no ha cambiado, pero las variables que miden la sesión se comportan distinto.
2. **Deriva de concepto**: cambia la relación `P(y|X)`; el mismo cliente con los mismos datos
   ahora se comporta de otra forma. Ejemplo: un cambio de política de devoluciones hace que
   clientes con el mismo historial devuelvan el doble.
3. **Deriva de la etiqueta** (*prior shift*): cambia la proporción de positivos aunque las
   entradas se comporten igual. Ejemplo: la tasa de fraude pasa del 0,4 % al 1,1 % porque han
   entrado a atacarte desde otro país.

El problema práctico es que la métrica de negocio llega tarde por diseño. Una conversión se
sabe en días, un impago a 90 días, una recaída de un paciente en meses. Si esperas a esa
métrica para reaccionar, has estado sirviendo predicciones malas todo ese tiempo. La deriva se
mide en las entradas y en las predicciones, que están disponibles al instante.

Dos advertencias antes de seguir. La primera: **no toda desviación es deriva**. Un pico de
tráfico el Black Friday mueve todas las distribuciones y no significa que el modelo esté roto;
por eso la comparación se hace contra una referencia estable y, si el negocio tiene
estacionalidad, contra el mismo periodo del año anterior. La segunda: la deriva es una señal,
no un diagnóstico. Detectar que una variable se movió no te dice si el modelo ha dejado de
acertar; para eso necesitas etiquetas, aunque sean de una muestra pequeña y revisada a mano.

## Definición formal

Se divide la variable en `k` intervalos (bins) y se comparan las proporciones de la
**referencia** `p` (la distribución del entrenamiento) con las de la **ventana actual** `q`:

:::formula
PSI = Σᵢ (qᵢ − pᵢ) · ln(qᵢ / pᵢ)
:::

:::formula
KL(q ‖ p) = Σᵢ qᵢ · ln(qᵢ / pᵢ)
:::

:::formula
KS = supₓ |Fq(x) − Fp(x)|
:::

- `pᵢ` — proporción de observaciones de la referencia que caen en el bin `i`.
- `qᵢ` — la misma proporción, calculada con los datos de la ventana actual.
- `k` — número de bins; los cortes se fijan **con la referencia** y no se recalculan.
- `Σᵢ` — suma sobre los `k` bins; `ln` es el logaritmo natural.
- `PSI` — *population stability index*. Es la diferencia simetrizada entre las dos
  distribuciones discretizadas; vale 0 si son idénticas y crece al separarse.
- `KL(q ‖ p)` — divergencia de Kullback-Leibler de `q` respecto a `p`. **No es simétrica**:
  `KL(q‖p) ≠ KL(p‖q)`, así que hay que decir siempre en qué orden se calcula.
- `Fp` y `Fq` — funciones de distribución empíricas (proporción de valores menores o iguales
  que `x`) de la referencia y de la actual; `supₓ` es el máximo sobre todos los valores de `x`.
- `KS` — estadístico de Kolmogorov-Smirnov: la mayor separación vertical entre las dos curvas.
  Va de 0 a 1 y no depende de cómo hayas hecho los bins, por eso se usa con variables continuas.

Convenciones habituales en la industria para el PSI: por debajo de **0,10** se considera
estable; entre **0,10 y 0,25**, cambio moderado que conviene investigar; por encima de
**0,25**, cambio importante. Son umbrales de trabajo, no verdades matemáticas: dos variables
con el mismo PSI pueden importar muy distinto según cuánto pesen en el modelo.

Tres detalles que se pasan por alto:

- El `KS` viene con un p-valor, y ese p-valor **depende del tamaño de muestra**. Con 200 000
  filas, una diferencia de 0,08 (irrelevante) da p ≈ 0. Mira el estadístico, no el p-valor.
- `KL` no tiene tope: puede ser 0,02 o 3,5. Solo se compara contra la misma referencia y la
  misma discretización.
- Si `qᵢ = 0` y `pᵢ > 0`, el logaritmo se va a infinito. Se agrupa ese bin con un vecino o se
  añade una pseudo-cuenta, y se documenta.

## Ejemplo

Una variable con cuatro bins. La referencia sale del entrenamiento y la actual de los últimos
30 días de producción:

| Bin | Referencia p | Actual q | (q − p) · ln(q / p) |
| --- | --- | --- | --- |
| 1 | 0,40 | 0,25 | 0,0705 |
| 2 | 0,30 | 0,30 | 0,0000 |
| 3 | 0,20 | 0,25 | 0,0112 |
| 4 | 0,10 | 0,20 | 0,0693 |

Sumando la última columna, `PSI = 0,1510`: cambio moderado según la convención anterior. El
peso se reparte entre el primer bin, que ha perdido 15 puntos, y el cuarto, que los ha ganado.
Eso ya te dice dónde mirar: la variable se ha desplazado hacia arriba.

Si calculas las dos KL con los mismos números salen `KL(q‖p) = 0,0769` y `KL(p‖q) = 0,0741`.
Son parecidas porque las distribuciones se parecen, pero **no son iguales**, y con
distribuciones muy distintas la diferencia entre ambos órdenes se dispara.

Y aquí está el caso que ningún PSI detecta. Imagina 2 000 observaciones con la misma `x`
(media 0, desviación 1) en entrenamiento y en producción. En entrenamiento el objetivo era
`y = 2x + ruido` y el modelo aprendió una pendiente de 1,983; en producción el mundo cambió a
`y = −2x + ruido`. La correlación entre `x` y `y` pasó de **+0,894** a **−0,897**, las
entradas son idénticas y el error cuadrático medio subió de **0,99 a 16,93**. La deriva de
datos es exactamente cero y el modelo está inservible: es deriva de concepto.

## Código

```python verificable
import numpy as np

# Proporciones por bin: la referencia fija los cortes, la actual se compara contra ella
ref = np.array([0.40, 0.30, 0.20, 0.10])
act = np.array([0.25, 0.30, 0.25, 0.20])

psi = ((act - ref) * np.log(act / ref)).sum()          # simetrizado: da igual el orden
kl_act_ref = (act * np.log(act / ref)).sum()           # KL(actual || referencia)
kl_ref_act = (ref * np.log(ref / act)).sum()           # KL(referencia || actual)

print(f"PSI           {psi:.4f}")     # -> 0.1510
print(f"KL(act||ref)  {kl_act_ref:.4f}")  # -> 0.0769
print(f"KL(ref||act)  {kl_ref_act:.4f}")  # -> 0.0741
```

```python verificable
import numpy as np

# Deriva de concepto: las entradas son las mismas, la regla que genera y ha cambiado.
rng = np.random.default_rng(0)
x = rng.normal(0.0, 1.0, size=2000)
y_train = 2.0 * x + rng.normal(0.0, 1.0, size=2000)
y_prod = -2.0 * x + rng.normal(0.0, 1.0, size=2000)

pendiente = float(np.polyfit(x, y_train, 1)[0])        # lo que aprendio el modelo
mse_train = float(((y_train - pendiente * x) ** 2).mean())
mse_prod = float(((y_prod - pendiente * x) ** 2).mean())

print("corr en entrenamiento:", round(float(np.corrcoef(x, y_train)[0, 1]), 3))  # -> 0.894
print("corr en produccion:   ", round(float(np.corrcoef(x, y_prod)[0, 1]), 3))   # -> -0.897
print("MSE en entrenamiento: ", round(mse_train, 2))                             # -> 0.99
print("MSE en produccion:    ", round(mse_prod, 2))                              # -> 16.93
```

```python verificable
import numpy as np
from scipy import stats

# El p-valor del KS no dice si la diferencia importa: depende sobre todo del tamano.
rng = np.random.default_rng(11)
for n in (50, 5000, 200000):
    referencia = rng.normal(0.0, 1.0, size=n)
    actual = rng.normal(0.2, 1.0, size=n)   # mismo desplazamiento en los tres casos
    ks = stats.ks_2samp(referencia, actual)
    print(f"n={n:>6}  KS {ks.statistic:.3f}  p {ks.pvalue:.4f}")
```

```text
n=    50  KS 0.280  p 0.0392
n=  5000  KS 0.090  p 0.0000
n=200000  KS 0.085  p 0.0000
```

## Errores típicos

- **Vigilar solo la métrica de negocio.** Es la señal más fiable y la más lenta: un impago
  tarda 90 días. Cuando la métrica cae, llevas un trimestre sirviendo predicciones malas.
- **Reentrenar en automático con los datos ya derivados.** Si la deriva es de concepto y las
  etiquetas nuevas son fiables, reentrenar es lo correcto. Si lo que cambió fue la definición
  de la etiqueta (devoluciones, fraude confirmado, criterio del revisor), reentrenar aprende
  el error y lo consolida. Antes de automatizar un reentrenamiento, define quién valida la
  etiqueta.
- **Recalcular los cortes de los bins con los datos de producción.** El PSI deja de ser
  comparable con el histórico y siempre saldrá pequeño. Los cortes se congelan con la
  referencia; si necesitas bins nuevos, recalcula también la referencia y dilo.
- **Dejar un bin a cero.** `ln(0/p)` es infinito y el PSI sale `inf` o `nan`. Agrupa el bin
  raro con su vecino o añade una pseudo-cuenta pequeña, y documenta cuál de las dos cosas
  hiciste.
- **Mirar las 400 variables por igual.** La deriva importa donde el modelo pesa. Ordena por
  contribución al modelo (importancia, coeficientes) y vigila primero esas; una variable con
  PSI de 0,4 que aporta el 0,5 % casi nunca explica un fallo.
- **Confundir deriva con un incidente de datos.** Si un campo pasa de un 2 % de nulos al
  100 %, eso no es el mundo cambiando: es la ingesta rota. Eso lo caza
  [[observabilidad-de-datos]] y [[calidad-y-slas]], no un test de distribución.

## Comprueba que lo sabes

:::quiz
p: La distribución de tus variables de entrada es idéntica a la del entrenamiento, pero el error del modelo se ha multiplicado por 17. ¿Qué está pasando?
o: Deriva de datos, porque las entradas siempre acaban moviéndose
o: Deriva de concepto, porque ha cambiado la relación entre entradas y objetivo
o: Nada: si las entradas no cambian, el modelo no puede degradarse
a: 2
e: La deriva de datos se mide en P(X) y aquí no hay ninguna. Lo que cambió es P(y), la regla que asocia entradas y objetivo, y eso no lo ve ningún test sobre las entradas: hace falta comparar predicciones contra etiquetas reales, aunque sean de una muestra revisada a mano.
:::

:::quiz
p: Con 200 000 filas, tu test KS da un estadístico de 0,085 y un p-valor de 0,0000. ¿Cómo lo interpretas?
o: Cambio importante: el p-valor es minúsculo
o: Cambio pequeño: el estadístico es la magnitud del efecto y el p-valor solo dice que la muestra es grande
o: No se puede interpretar sin saber la media de la variable
a: 2
e: Con muestras grandes, cualquier diferencia mínima da un p-valor casi nulo, así que el p-valor deja de ser informativo. El estadístico KS sí mide el tamaño del efecto, y 0,085 es una separación máxima del 8,5 % entre las dos curvas acumuladas: pequeño.
:::

:::trampa
Poner una alerta que dispare el reentrenamiento con solo superar un PSI de 0,25 es la forma más
rápida de reentrenar todos los días con datos peores que los del modelo actual. La alerta debe
abrir una investigación, no ejecutar un pipeline: primero mira qué variable se movió, si el
cambio es estacional y si tienes etiquetas frescas con las que medir.
:::

:::practica
enunciado: Una variable tiene referencia [0,50, 0,30, 0,20] y actual [0,30, 0,30, 0,40] en tres bins. Calcula el PSI y decide si abres una investigación.
pista: Aplica PSI = suma de (q − p) por el logaritmo natural de q/p en cada bin.
solucion: Bin 1: (0,30 − 0,50) · ln(0,30/0,50) = (−0,20) · (−0,5108) = 0,1022. Bin 2: 0. Bin 3: (0,40 − 0,20) · ln(0,40/0,20) = 0,20 · 0,6931 = 0,1386. PSI = 0,2408, justo por debajo del umbral de 0,25 pero en la banda de cambio moderado: sí se investiga, empezando por la cola alta, que es la que ha doblado su peso.
:::
