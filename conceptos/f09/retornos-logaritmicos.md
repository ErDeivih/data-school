---
id: retornos-logaritmicos
titulo: Retornos logarítmicos
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [medidas-de-dispersion, escalado-y-transformacion, estacionariedad]
tags: [series-temporales, rentabilidad, precios]
resumen: Mide la variación proporcional de un precio, se suma en el tiempo y se anualiza sin trucos, por eso es la unidad de trabajo de casi todo modelo financiero.
fuentes: ["Campbell, Lo y MacKinlay (1997), 'The Econometrics of Financial Markets'", "Tsay (2010), 'Analysis of Financial Time Series'"]
---

## En una frase

El retorno logarítmico de un periodo es ln(P_t / P_{t−1}): mide la variación proporcional
del precio y, a diferencia del retorno simple, los retornos logarítmicos de periodos
consecutivos **se suman** para dar el retorno del periodo completo.

## La idea

El retorno simple, `R_t = (P_t − P_{t−1}) / P_{t−1}`, es lo primero que uno calcula y
responde bien a la pregunta «¿cuánto ha subido esto?». Su problema aparece al encadenar
periodos. Si un activo sube un 10 % y después baja un 10 %, no vuelve al punto de partida:
100 → 110 → 99. El retorno de los dos periodos juntos no es 0 %, es −1 %, porque los
retornos simples no se suman, se **multiplican**: (1 + 0,10) · (1 − 0,10) − 1 = −0,01. Para
saber cuánto has ganado en 250 sesiones tienes que multiplicar 250 factores, y la media de
esos retornos no te da el retorno del periodo.

:::figura
fichero: retornos-log-aditivos-y-error
pie: Arriba, tres formas de acumular el mismo histórico: la suma de log-retornos cae exactamente encima del producto de los factores, mientras que sumar los porcentajes se separa. Abajo, la simetría que solo tienen los logaritmos: un +20 % seguido de un −20 % devuelve el precio al mismo sitio si se mide en logaritmos, y deja el capital un 4 % por debajo si se mide en porcentajes. Mira primero la separación entre las dos líneas verdes y naranjas de arriba: eso es el error que cometes al sumar porcentajes.
fuente: figuras/retornos-logaritmicos-1.py
:::

Los retornos logarítmicos arreglan exactamente eso. Como

ln(P_t / P_{t−1}) = ln P_t − ln P_{t−1}

la suma de los retornos logarítmicos de varios periodos encadena los términos intermedios y
se cancela sola: `ln P₁ − ln P₀ + ln P₂ − ln P₁ + …` deja únicamente `ln P_T − ln P₀`. A eso
se le llama suma telescópica, y es la razón de que los logaritmos sean la unidad de trabajo
natural para todo lo que se acumula en el tiempo: sumar retornos diarios para obtener el
anual, sumar retornos para obtener el de una cartera a lo largo de un mes, o promediar la
rentabilidad de un periodo sin ponderaciones raras.

La segunda propiedad útil es la simetría. Un retorno logarítmico de −5 % seguido de uno de
+5 % devuelve **exactamente** al precio inicial (la suma es cero). Con retornos simples no:
tras perder un 5 % necesitas ganar un 5,263 % para recuperar, y ese desequilibrio se acumula
en cada racha.

Ahora la advertencia, que es la mitad de este concepto. Los logaritmos son aditivos **en el
tiempo**, pero no **entre activos**. El retorno de una cartera es la media ponderada de los
retornos *simples* de sus componentes, no de los logarítmicos. Con dos activos al 50 % que
hacen +10 % y −10 %, la cartera queda plana (0 %), mientras que la media de los logaritmos es
−0,50 %. Si calculas el retorno de una cartera promediando logaritmos, te sale un número
ligeramente negativo que no corresponde a ninguna cuenta real.

Como bonus, trabajar con logaritmos encaja con el supuesto estadístico más usado en finanzas:
si el log-precio sigue un paseo aleatorio con innovaciones normales, el precio es lognormal
(nunca negativo, con cola larga hacia arriba) y los retornos logarítmicos son, por
construcción, la variable que se supone normal. Ese supuesto es una aproximación —los
retornos reales tienen colas más gordas que la normal y cierta asimetría—, pero es la
aproximación sobre la que están construidos el movimiento browniano geométrico, [[garch-volatilidad|los
modelos GARCH]] y casi toda la teoría de carteras.

## Definición formal

:::formula
r_t = ln(P_t / P_{t−1}) = ln P_t − ln P_{t−1}
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `r_t` | Retorno logarítmico del periodo `t` | tanto por uno (0,05 = 5 %) | Es la unidad de trabajo: se suma en el tiempo sin ajustes, pero **no** se promedia entre activos |
| `R_t` | Retorno simple del mismo periodo | tanto por uno | Con movimientos pequeños vale casi lo mismo que `r_t`; al 50 % la diferencia ya es de nueve puntos porcentuales |
| `P_t` | Precio (o valor de la cartera) al final del periodo | EUR o índice | Un precio que se dobla no sube «un 100 %» en logaritmo, sube 0,693: la escala se comprime hacia arriba |
| `P_{t−1}` | Precio al final del periodo anterior | EUR o índice | Es el denominador: un precio muy pequeño en el pasado hace que `r_t` se dispare, y si es cero el logaritmo no existe |
| `ln` | Logaritmo natural, en base `e ≈ 2,71828` | adimensional | En finanzas es siempre el natural. Cambiar de base solo reescala el resultado y rompe la aditividad, que es justo lo que se busca |
| `T` | Número de periodos por año (252 sesiones, 12 meses, 52 semanas) | periodos | Multiplica el **log**-retorno medio, no el porcentaje: para tener la rentabilidad anual hay que aplicarle la exponencial |
| `r̄` | Media de los retornos logarítmicos de un periodo | tanto por uno | Es aditiva y promediable en el tiempo, a diferencia de los retornos simples, que hay que componer |
| `R_anual` | Retorno anual efectivo, lo que de verdad gana el capital | % anual | Llega por `exp(T · r̄) − 1`. Leer `T · r̄` como si ya fuera el porcentaje anual subestima, y el error crece con el nivel de retorno |
| `σ_periodo` | Desviación típica de los retornos logarítmicos de un periodo | tanto por uno o % | Es la base de la volatilidad: para agregarla en el tiempo se multiplica por `√T`, nunca por `T` |
| `σ_anual` | Su equivalente anual, con periodos independientes | % anual | Con retornos correlacionados, `σ_periodo · √T` se queda corta: el supuesto de independencia no es inocente |
:::

- `P_t` — precio (o valor de la cartera) al final del periodo `t`; `P_{t−1}`, al final del
  periodo anterior.
- `ln` — logaritmo natural, en base `e ≈ 2,71828`. En finanzas siempre es el natural; un
  logaritmo en otra base solo cambia la escala y estropea las propiedades de abajo.
- `r_t` — retorno logarítmico del periodo `t`, en tanto por uno (0,05 es un 5 %).
- `R_t = (P_t − P_{t−1}) / P_{t−1}` — retorno simple del mismo periodo.
- Relación entre ambos: `r_t = ln(1 + R_t)`, y deshaciendo, `R_t = exp(r_t) − 1`.

**Aditividad temporal.** Para cualquier número de periodos consecutivos:

:::formula
r_{1:T} = Σ_{t=1}^{T} r_t = ln(P_T / P_0)
:::

donde `P_0` es el precio al inicio del primer periodo y `P_T` al final del último. Esto no es
una aproximación: es exacto.

**Anualización.** Con `T` periodos por año (252 sesiones, 12 meses, 52 semanas) y `r̄` la
media de los retornos logarítmicos por periodo:

:::formula
R_anual = exp(T · r̄) − 1          σ_anual = σ_periodo · √T
:::

- `R_anual` — retorno anual efectivo (lo que de verdad gana el capital en un año).
- `σ_periodo` — desviación típica de los retornos logarítmicos de un periodo.
- `σ_anual` — su equivalente anual, bajo el supuesto de que los periodos son independientes.
- La exponencial es imprescindible: multiplicar la media logarítmica por 252 da un
  **log-retorno** anual, no un porcentaje anual.

**Aproximación para movimientos pequeños.** Desarrollando el logaritmo:

:::formula
r = ln(1 + R) ≈ R − R² / 2
:::

Con `R = 0,01` (un 1 %), la diferencia entre `R` y `r` es de cinco milésimas de punto
porcentual, medio punto básico; con `R = 0,10`, `r` vale 0,095310 y la diferencia es de 0,47
puntos porcentuales, casi medio punto; con `R = 0,50`, `r` vale 0,405465 y la diferencia supera
los nueve puntos.

## Ejemplo

Cuatro precios de cierre consecutivos: 100, 105, 99 y 104.

| Periodo | Precio | Retorno simple | Retorno logarítmico |
| --- | --- | --- | --- |
| 1 | 100 a 105 | +5,000000 % | +4,879016 % |
| 2 | 105 a 99 | −5,714286 % | −5,884052 % |
| 3 | 99 a 104 | +5,050505 % | +4,927088 % |
| Total | 100 a 104 | +4,336219 % si se suman | +3,922052 % |

Los tres números que hay que mirar:

- **Suma de los retornos logarítmicos:** 4,879016 − 5,884052 + 4,927088 = **3,922052 %**.
- **Comprobación:** ln(104 / 100) = 3,922052 %. Coincide al séptimo decimal. La suma funciona.
- **Producto de los factores simples:** 1,05 · 0,9428571 · 1,0505051 = 1,04, es decir un
  **+4 %** exacto. Correcto, pero fíjate en que la suma de los retornos simples (4,336219 %)
  no da ese 4 %: si hubieras sumado, te habrías equivocado en 0,34 puntos porcentuales en
  solo tres periodos.

Si esos tres retornos fueran diarios y se repitieran durante un año con la misma media, el
log-retorno anual sería `0,039221 · 252 = 9,88`: un 988 %, absurdo para una sesión media real.
Con una media diaria realista de 0,0004, el log-retorno anual es `0,0004 · 252 = 0,1008` y el
retorno efectivo `exp(0,1008) − 1 = 0,1061`, un **10,61 %**. Ahí está la trampa: el producto
`0,1008` es un log-retorno, y leerlo directamente como «un 10,08 %» subestima la ganancia real
en medio punto.

## Código

```python verificable
import numpy as np

precios = np.array([100.0, 105.0, 99.0, 104.0])
log_ret = np.diff(np.log(precios))         # ln(P_t) - ln(P_t-1): se suman en el tiempo
simple = np.diff(precios) / precios[:-1]   # (P_t - P_t-1) / P_t-1: se multiplican

print(f"log del periodo 1  {log_ret[0]:+.6f}")       # -> +0.048790
print(f"log del periodo 2  {log_ret[1]:+.6f}")       # -> -0.058841
print(f"log del periodo 3  {log_ret[2]:+.6f}")       # -> +0.049271
print(f"suma de los logs   {log_ret.sum():+.6f}")    # -> +0.039221
print(f"ln(104/100)        {np.log(precios[-1] / precios[0]):+.6f}")  # -> +0.039221
print(f"suma de simples    {simple.sum():+.6f}")     # -> +0.043362
```

:::claves
- `np.diff` devuelve un array **una posición más corto** que su entrada, y por eso `log_ret[2]` es el retorno del tercer periodo y no del cuarto. Si lo comparas con la lista de precios, los índices están desplazados uno.
- `precios[:-1]` no es `precios`: es una **vista** de todos los precios menos el último, la que hace que el cociente tenga tantos elementos como diferencias. Sin ese recorte, `simple` saldría con una posición de más y llena de valores basura.
- `np.log(precios)` se calcula elemento a elemento y devuelve un array nuevo; no modifica `precios`. Los componentes son logaritmos **naturales**, no decimales: `np.log10` existe y daría otro número completamente distinto.
- `log_ret.sum()` y `ln(precios[-1] / precios[0])` dan el mismo resultado por la suma telescópica; si no coinciden al sexto decimal, casi siempre es porque uno de los dos precios es de otro periodo.
- `simple.sum()` da 0,043362 y el resultado real es 0,04: sumar retornos simples **sobreestima**. La diferencia no es un error de redondeo, es la razón por la que existe este concepto.
- En el segundo bloque, `(pesos * simples).sum()` pondera los retornos simples y da 0,0000, mientras que `(pesos * np.log1p(simples)).sum()` da −0,0050. `np.log1p(x)` calcula `ln(1 + x)` con más precisión que `np.log(1 + x)` cuando `x` es diminuto, y aquí es la línea que demuestra que los logaritmos no se reparten entre activos.
:::

```python verificable
import numpy as np

# La aproximacion ln(1+r) ~ r - r^2/2 solo vale para retornos pequenos:
# al 50 % el error es de tres centesimas, no de una millonesima.
for r in (0.001, 0.01, 0.10, 0.50):
    error = r - r * r / 2 - np.log1p(r)
    print(f"r={r:>5.1%}  ln(1+r)={np.log1p(r):+.6f}  error de la aproximacion {error:+.2e}")

# En el tiempo los logs se suman; entre activos NO: la cartera promedia simples.
pesos = np.array([0.5, 0.5])
simples = np.array([0.10, -0.10])
print(f"cartera con simples {(pesos * simples).sum():+.4f}")              # -> +0.0000
print(f"media de los logs   {(pesos * np.log1p(simples)).sum():+.4f}")   # -> -0.0050
```

## Errores típicos

- **Sumar retornos simples en el tiempo.** Un +10 % y un −10 % no se cancelan: dejan −1 %. Si
  quieres el retorno acumulado, multiplica los factores `(1 + R_t)` o suma logaritmos, nunca
  sumes retornos simples.
- **Promediar retornos logarítmicos entre activos para obtener el de la cartera.** El retorno
  de una cartera es `Σ wᵢ · Rᵢ` con retornos simples. Con logaritmos obtienes un número que no
  corresponde a ninguna cuenta; el error es pequeño con pesos y retornos pequeños, y deja de
  serlo en cuanto hay movimientos grandes o pesos concentrados.
- **Anualizar multiplicando la media logarítmica por 252 y llamarlo «rentabilidad anual».**
  Ese producto es un log-retorno: con una media diaria de 0,0004 da 0,1008, y la rentabilidad
  efectiva es `exp(0,1008) − 1 = 10,61 %`. Presentar el 10,08 % se queda corto, y el error
  crece con el nivel de retorno.
- **Usar precios sin ajustar.** Un desdoblamiento de acciones 2 a 1 produce un
  `ln(0,5) = −69,3 %` que nunca ocurrió. Con dividendos pasa lo mismo, en pequeño. Usa precios
  ajustados por splits y dividendos, o trabaja con [[tick-data-y-ohlcv|series ya ajustadas]].
- **Olvidar que `r` no tiene suelo.** Un retorno simple no baja de −100 %; un logaritmo sí
  puede valer −3 (precio dividido por 20). Si aplicas al logaritmo fórmulas pensadas para
  porcentajes acotados, comprueba los límites.
- **Presentar los retornos logarítmicos como si fueran porcentajes exactos.** Decir «hoy ha
  subido 0,0488, o sea un 4,88 %» es aceptable en el día a día, pero al 20 % la diferencia con
  el retorno simple es de más de un punto: conviene decir cuál de los dos estás usando.

:::practica
enunciado: Un fondo encadena 20 sesiones con un retorno logarítmico diario de +0,0123. Calcula el retorno simple acumulado del periodo y compáralo con el que saldría de sumar los 20 retornos simples diarios.
pista: Los logaritmos se suman en el tiempo; para volver a retorno simple hay que deshacer el logaritmo con la exponencial.
solucion: Logaritmo acumulado: 20 · 0,0123 = 0,246. Retorno simple: exp(0,246) − 1 = 0,2789, un 27,89 %. El retorno simple diario es exp(0,0123) − 1 = 0,012376, y sumarlo 20 veces da 0,2475, un 24,75 %. La suma se queda 3,14 puntos porcentuales corta porque el logaritmo crece menos que el simple y la diferencia se acumula periodo a periodo. Conclusión: para encadenar periodos, suma logaritmos y convierte el total con la exponencial.
:::

## Comprueba que lo sabes

:::quiz
p: Un activo pasa de 100 a 110 y después a 99. ¿Qué afirmación es correcta?
o: Los dos retornos simples suman 0 %, así que el activo ha vuelto al punto de partida
o: La suma de los retornos logarítmicos es ln(99/100), es decir un −1,005 %
o: La suma de los retornos logarítmicos es 0 % porque el precio final es 99 y el inicial 100
a: 2
e: Por la propiedad telescópica, sumar los logaritmos equivale a ln(P_final / P_inicial) = ln(0,99) = −1,005 %. Los retornos simples (+10 % y −10 %) suman 0 %, pero su producto es 1,10 · 0,90 = 0,99: eso es exactamente el −1 % que sí ha ocurrido.
:::

:::quiz
p: ¿Por qué el retorno de una cartera se calcula con retornos simples y no con logarítmicos?
o: Porque los logaritmos no están definidos para retornos negativos
o: Porque el valor de la cartera es la suma ponderada de los valores, y eso hace que el retorno sea media ponderada de simples
o: Porque los retornos logarítmicos solo se usan con divisas
a: 2
e: Si la cartera vale Σ wᵢ · Vᵢ, el retorno del conjunto es Σ wᵢ · Rᵢ con los retornos simples. Los logaritmos sí están definidos para retornos negativos (siempre que el precio sea positivo) y se usan en cualquier activo; lo que no hacen es repartirse linealmente entre componentes.
:::

:::quiz
p: Tienes 250 retornos logarítmicos diarios con media 0,0004. ¿Cuál es el retorno anual aproximado?
o: 0,0004 · 250 = 0,10, es decir un 10 %
o: exp(0,1) − 1 ≈ 10,52 %
o: 0,0004 · √250 ≈ 0,63 %
a: 2
e: Sumar 250 log-retornos da 0,1, que es un log-retorno anual; para pasarlo a rentabilidad efectiva hay que aplicar exp(0,1) − 1 = 10,52 %. Multiplicar por √250 confunde la escala de la volatilidad con la de la media.
:::

:::truco
Cuando compares periodos de distinta duración, pásalos siempre a la misma unidad con
`exp(T · r̄) − 1`. Y si solo vas a hacer medias, sumas y regresiones, quédate con el
logaritmo: es aditivo y no necesita ajustes.
:::
