---
id: ratio-de-sharpe
titulo: Ratio de Sharpe
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [retornos-logaritmicos, varianza-y-desviacion, valor-esperado, z-score-y-estandarizacion]
tags: [riesgo, metricas, cartera, backtest]
resumen: Exceso de rentabilidad por unidad de volatilidad asumida; la métrica más citada del trading y la más fácil de inflar sin querer.
fuentes: ["Sharpe (1966), 'Mutual Fund Performance'", "Sharpe (1994), 'The Sharpe Ratio'"]
---

## En una frase

El ratio de Sharpe divide lo que ganas por encima del activo libre de riesgo entre la
volatilidad que has soportado para conseguirlo: convierte «gané un 30 %» en «gané un 30 %
moviéndome como si hubiera ganado un 10 %».

## La idea

Dos estrategias ganan un 20 % anual. La primera lo hace con meses de +1,5 % casi siempre
iguales; la segunda alterna meses de +18 % y de −15 %. Cualquiera preferiría la primera, y
sin embargo el beneficio es idéntico. Lo que falta en esa comparación es el **precio
emocional y financiero del camino**: la segunda te puede dejar fuera de juego en el peor
momento (una retirada, un margen, una llamada del bróker) aunque acabe el año igual.

Sharpe resuelve eso: mide cuánto rendimiento obtienes por cada unidad de temblor. El
«temblor» se mide con la desviación típica de los retornos, y el rendimiento que cuenta no
es el total, sino el que supera a lo que te habría dado el dinero sin riesgo (letras del
tesoro, tipo de depósito). Si tu estrategia gana exactamente lo mismo que el activo sin
riesgo, su Sharpe es 0: has asumido riesgo a cambio de nada.

Hay una interpretación que ayuda mucho: **el Sharpe es una señal contra su propio ruido**. Un
Sharpe de 2 quiere decir que la media del exceso de rentabilidad pesa el doble que su
desviación típica en la muestra; no dice nada sobre la probabilidad de que ese exceso sea
cierto. Para eso está el error típico del estimador (`1/√n`, ver más abajo): con 12 meses un
Sharpe de 2 sigue siendo compatible con el cero, y por eso los valores altos sostenidos en
muestras cortas son casi siempre un error de cálculo o una casualidad.

:::figura
fichero: sharpe-caminos-y-ruido
pie: A la izquierda, dos estrategias que acaban en el mismo capital: la azul se mueve un 1,7 % al mes (Sharpe anual 2,3) y la roja un 8,7 % para llegar exactamente al mismo sitio (Sharpe 0,6). El beneficio no las distingue; el Sharpe sí. A la derecha, 4.000 simulaciones de una estrategia **sin ninguna ventaja**: con 12 meses, uno de cada cuarenta intentos da un Sharpe de 2,2 o más, así que un número alto con pocas observaciones no demuestra nada.
fuente: figuras/ratio-de-sharpe-1.py
:::

## Definición formal

:::formula
Sharpe = (E[R − Rf]) / σ(R − Rf) ≈ (R̄ − R̄f) / σ_R
:::

- `R` — retorno de la estrategia en cada periodo (diario, mensual…).
- `Rf` — retorno del activo libre de riesgo en el mismo periodo.
- `R − Rf` — exceso de retorno; es lo que se premia por asumir riesgo.
- `E[·]` — esperanza matemática, que en la práctica se estima con la media.
- `σ` — desviación típica del exceso de retorno: la volatilidad.
- `R̄`, `σ_R` — media y desviación típica muestrales.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `R` | Retorno de la estrategia en un periodo (un día, un mes) | tanto por uno, en la frecuencia que elijas | Sube la media `R̄` y el Sharpe sube con ella. Ojo: cambiar la frecuencia con la que mides (mensual en vez de diario) sube el Sharpe sin que la estrategia haya mejorado nada |
| `Rf` | Lo que da el activo sin riesgo en ese mismo periodo | tanto por uno, **misma frecuencia** que `R` | Si sube, el numerador baja y el Sharpe cae. Restar un 3 % anual a retornos mensuales es el error clásico: son 0,25 % al mes, y el exceso sale doce veces mayor de lo que es |
| `R − Rf` | El exceso de retorno: lo que se te paga por asumir riesgo | tanto por uno | Es el numerador. Si es cero o negativo, el ratio no tiene sentido económico aunque salga un número: asumiste riesgo a cambio de nada |
| `E[·]` | La esperanza matemática del exceso | — | En la práctica se sustituye por la media muestral `R̄`, así que el Sharpe que publicas es una estimación con su error, no el valor verdadero |
| `σ` | La desviación típica del exceso: la volatilidad | tanto por uno | Es el denominador: si sube, el Sharpe baja. Medirla con pocos datos o con precios suavizados de activos ilíquidos la deja corta y el Sharpe sale inflado |
| `n` | Número de observaciones que sostienen la media y la desviación | periodos | No aparece en la fórmula y decide si el número significa algo: el error típico va como `1/√n`. Con 12 meses el intervalo de confianza incluye el cero; con 240 se estrecha |
| `√252` (o `√12`) | Factor de anualización: días de bolsa o meses del año | adimensional | Anualiza multiplicando por la raíz, no elevando al cuadrado ni multiplicando por 252. Solo vale si los periodos son independientes; con volatilidad agrupada, el Sharpe anual sale optimista |
:::

**Anualización.** Si mides retornos diarios y supones independencia entre días:

:::formula
Sharpe_anual ≈ Sharpe_diario · √252
:::

El 252 son los días de bolsa de un año, y el `√` viene de que la varianza de una suma de
variables independientes suma varianzas: multiplicar la desviación típica diaria por `√252`
da la anual. Con retornos mensuales se usa `√12`. **Este supuesto de independencia es falso**
en la práctica (la volatilidad se agrupa), y de ahí sale media parte de los abusos que se
cuentan más abajo.

## Ejemplo

Doce retornos mensuales de una estrategia, en tanto por uno:

```
0,02  0,03  -0,01  0,04  0,01  0,02  -0,02  0,03  0,00  0,02  0,01  0,01
```

- Media mensual: 0,0133 (el 1,33 %).
- Desviación típica mensual: 0,0172 (el 1,72 %).
- Supongamos un activo libre de riesgo al 0,2 % mensual.
- Sharpe mensual: (0,0133 − 0,002) / 0,0172 = **0,66**.
- Sharpe anualizado: 0,66 · √12 = **2,28**.

Un 2,3 con doce observaciones no significa nada: la incertidumbre del propio Sharpe es
enorme con tan pocos datos (el error típico de un Sharpe mensual estimado con 12 meses ronda
±0,3, y anualizado pasa de ±1). Antes de presumir de Sharpe hay que mirar **cuántas
observaciones** lo sostienen.

## Código

```python verificable
import numpy as np

retornos = np.array([0.02, 0.03, -0.01, 0.04, 0.01, 0.02,
                     -0.02, 0.03, 0.00, 0.02, 0.01, 0.01])
rf_mensual = 0.002

exceso = retornos - rf_mensual
sharpe_mensual = exceso.mean() / exceso.std(ddof=1)   # ddof=1: estimamos la media
sharpe_anual = sharpe_mensual * np.sqrt(12)

print(f"media mensual   {retornos.mean():.4f}")        # -> 0.0133
print(f"volatilidad     {retornos.std(ddof=1):.4f}")   # -> 0.0172
print(f"Sharpe mensual  {sharpe_mensual:.2f}")         # -> 0.66
print(f"Sharpe anual    {sharpe_anual:.2f}")           # -> 2.28
```

:::claves
- `retornos - rf_mensual` resta un escalar a **todos** los elementos del array (radiodifusión): no hace falta un bucle ni un `for`, y el resultado es un array nuevo; el original no se toca.
- `exceso.std(ddof=1)` divide entre `n − 1`, que es lo correcto cuando la serie es una muestra y no la población entera. NumPy usa `ddof=0` por defecto y pandas `ddof=1`: con los mismos 12 datos el Sharpe cambia un 4 o un 5 %, y ese es el número que acabas publicando.
- La desviación se toma del **exceso** (`exceso.std`), no de los retornos. Con un `rf` constante las dos son idénticas, porque restar una constante no cambia la dispersión; el día que `rf` cambie periodo a periodo dejan de coincidir y el Sharpe se mueve sin que la estrategia cambie.
- `np.sqrt(12)` va **fuera** del cociente y multiplica: el Sharpe mensual se anualiza con la raíz de 12, no con 12. El `√` sale de que la varianza de una suma de variables independientes suma varianzas. Con retornos diarios el factor sería `np.sqrt(252)`.
- Si todos los retornos de la muestra fuesen iguales, `exceso.std(ddof=1)` valdría 0 y la división daría `inf` acompañado de un aviso de NumPy, no de un error que te pare el programa. Un `inf` en una tabla de métricas significa «esta serie no tiene variación», no «Sharpe perfecto».
- Mezclar unidades rompe la cuenta sin dar ningún error: si escribes los retornos en porcentaje (`2, 3, -1`) y dejas `rf_mensual = 0.002` en tanto por uno, el exceso sale mal y el Sharpe, absurdo. Como el ratio es invariante de escala, el fallo no se ve mirando solo el resultado.
:::

```python verificable
import numpy as np

# El error típico del Sharpe: por qué 12 meses no bastan para presumir.
# Aproximación de Lo (2002): SE ≈ sqrt((1 + Sharpe²/2) / n)
def error_tipico_sharpe(retornos, rf=0.0):
    exceso = retornos - rf
    sr = exceso.mean() / exceso.std(ddof=1)
    return sr, np.sqrt((1 + sr**2 / 2) / exceso.size)

rng = np.random.default_rng(0)

# Misma estrategia "real" (Sharpe mensual 0,1), medida con 12 y con 240 meses
for n in (12, 60, 240):
    sr, se = error_tipico_sharpe(rng.normal(0.003, 0.03, size=n))
    print(f"n={n:>4}  Sharpe mensual {sr:+.2f}  error tipico ±{se:.2f}  anual {sr*np.sqrt(12):+.2f}")
```

## Errores típicos

- **Comparar Sharpes calculados a frecuencias distintas.** Un Sharpe «anual» calculado con
  datos diarios, con datos mensuales y con datos anuales da tres números distintos, porque el
  supuesto de independencia se rompe más cuanto más fina es la frecuencia. Si comparas, usa la
  misma frecuencia y dilo.
- **Inflarlo midiendo menos veces.** Con retornos mensuales en vez de diarios, el Sharpe sube
  sin que la estrategia haya mejorado: desaparece la autocorrelación negativa de corto plazo.
  Es la forma más común (y más involuntaria) de mentir con esta métrica.
- **Presumir de Sharpe con pocas observaciones.** Un Sharpe de 3 sobre 6 meses es
  indistinguible de ruido. Da siempre el número de periodos y, si puedes, un intervalo de
  confianza.
- **Aplicarlo a retornos muy asimétricos.** Sharpe penaliza igual la volatilidad buena y la
  mala: castiga las subidas tanto como las bajadas. Con estrategias de opciones o colas
  gruesas, [[sortino-y-calmar|el ratio de Sortino]] o el CVaR describen mejor la realidad.
- **Elegir la estrategia por su Sharpe en la misma muestra donde la escogiste.** Si pruebas
  500 ideas y publicas el Sharpe de la mejor, ese número está sesgado al alza. Es
  exactamente lo que corrige [[sharpe-deflactado|el Sharpe deflactado]].
- **Calcular el Sharpe sin restar el tipo sin riesgo.** Un 5 % anual cuando el depósito paga
  un 4,5 % no es una estrategia: es un depósito con más riesgo.

:::practica
enunciado: Una estrategia rinde un 12 % anual con una volatilidad anual del 8 %, y otra un 24 % con un 22 %. El depósito sin riesgo paga un 3 % y estás dispuesto a tolerar una volatilidad de cartera del 12 %. ¿Cuál eliges y cuánto apalancas la primera?
pista: Calcula los dos Sharpe y después reparte la volatilidad tolerada entre la de cada estrategia.
solucion: Sharpe de la primera: (12 − 3) / 8 = 1,13; de la segunda: (24 − 3) / 22 = 0,95. Gana la primera por unidad de riesgo. Escalada a tu tolerancia: 12 / 8 = 1,5 veces, con lo que rinde 3 + 1,5 · 9 = 16,5 % anual y no 12 %. Conclusión: el Sharpe decide cuál, el apalancamiento decide cuánto, y sin restricción de caída el número de Sharpe solo no basta.
:::

## Comprueba que lo sabes

:::quiz
p: Una estrategia tiene Sharpe mensual de 0,5. ¿Cuál es su Sharpe anualizado bajo el supuesto habitual?
o: 0,5 · 12 = 6,0
o: 0,5 · √12 ≈ 1,73
o: 0,5 / √12 ≈ 0,14
a: 2
e: El retorno escala con el tiempo (×12) y la volatilidad con su raíz (×√12), así que el cociente escala con √12. Multiplicar por 12 supone que no hay volatilidad; dividir convierte a frecuencia menor.
:::

:::quiz
p: ¿Por qué un Sharpe de 2,5 calculado con 10 operaciones no debe tomarse en serio?
o: Porque los Sharpes solo valen con datos diarios
o: Porque el error típico del estimador es enorme con tan pocas observaciones
o: Porque un Sharpe superior a 2 es matemáticamente imposible
a: 2
e: El Sharpe es una media dividida por una desviación típica estimada, y con pocas observaciones esa estimación es muy inestable: el intervalo de confianza incluye valores cercanos a cero. No hay nada imposible en un 2,5, simplemente no está demostrado.
:::

:::trampa
Si tu backtest da un Sharpe de 4, busca el error antes de celebrarlo. Los tres sospechosos
habituales: mirar al futuro en alguna variable, medir la volatilidad con datos
infravalorados (activos ilíquidos, precios de cierre suavizados) o haber probado muchas
variantes y quedarte con la mejor.
:::
