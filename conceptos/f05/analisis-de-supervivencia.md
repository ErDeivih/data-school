---
id: analisis-de-supervivencia
titulo: Análisis de supervivencia
fase: 5
nivel: experto
rutas: [ds, quant]
prerequisitos: [variable-aleatoria, distribuciones-continuas, maxima-verosimilitud]
tags: [supervivencia, censura, kaplan-meier, cox]
resumen: Modelar el tiempo hasta un evento cuando muchos casos aún no lo han sufrido: función de supervivencia, Kaplan-Meier, log-rank y riesgos proporcionales.
fuentes: ["Kaplan y Meier (1958), 'Nonparametric Estimation from Incomplete Observations'", "Cox (1972), 'Regression Models and Life-Tables'", "Klein y Moeschberger (2003), 'Survival Analysis: Techniques for Censored and Truncated Data'"]
---

## En una frase

El análisis de supervivencia estudia cuánto tarda en ocurrir un evento (una baja, un impago, un
fallo) aprovechando también los casos en los que el evento todavía no ha ocurrido, que no son datos
perdidos sino información incompleta pero útil.

## La idea

Tienes 5.000 clientes y quieres estimar cuánto tiempo permanecen de alta. De 1.200 que se han dado de
baja conoces la fecha exacta. De los otros 3.800 solo sabes que llevan `x` meses sin irse: el reloj
sigue corriendo. Si descartas a esos 3.800 y calculas la media de los 1.200, respondes a la pregunta
«¿cuánto tardan en irse los que se van?», que es distinta de «¿cuánto dura un cliente?». La media
saldrá demasiado baja, porque has borrado precisamente a los que aguantan.

El análisis de supervivencia resuelve esto tratando la información incompleta como lo que es. Un
cliente que lleva 8 meses sin irse aporta un dato muy concreto: su tiempo hasta la baja es **mayor
que 8**. Eso se llama **censura por la derecha**, y entra en las fórmulas como una condición, no
como un hueco. La analogía del maratón: cuando se retira el cronómetro, los corredores que siguen en
la calle no tienen tiempo final, pero tienes una cota inferior de su tiempo.

La segunda idea, más sutil, es que casi nunca interesa el riesgo acumulado: interesa el **riesgo
instantáneo de los que siguen expuestos**. Si dos grupos tienen la misma proporción de bajas al
cabo de un año, pero uno las concentra en el primer mes y el otro las reparte, no son iguales. Esa
tasa instantánea es el *hazard* `h(t)`, y es lo que modela la regresión de Cox.

:::figura
fichero: supervivencia-kaplan-meier-y-censura
pie: A la izquierda, la curva de Kaplan-Meier del ejemplo: las marcas verticales son las censuras, y cada una **no** baja la curva, solo saca al sujeto del denominador de los pasos siguientes. A la derecha, los dos grupos: control y tratamiento llegan al mes 40 con S = 0,27 y 0,25, pero el contraste de log-rank da chi² = 1,85 (p = 0,174), así que con 24 sujetos la separación es compatible con el efecto nulo. Conclusión: mira la curva para entender el fenómeno y el contraste para decidir si el dato lo sostiene.
fuente: figuras/analisis-de-supervivencia-1.py
:::

Los tres usos más frecuentes fuera de la medicina son: tiempo hasta la baja de un cliente (*churn*),
tiempo hasta el impago de un préstamo y tiempo hasta el fallo de una máquina. También aparece en
trading: la duración de una operación abierta es una variable de supervivencia, con la peculiaridad
de que hay dos formas de «morir» (salida por objetivo y salida por stop), lo que se llama riesgos en
competencia.

## Definición formal

Sea `T` la variable aleatoria «tiempo hasta el evento», no negativa, con función de densidad `f(t)` y
función de distribución `F(t) = P(T ≤ t)`.

- **Función de supervivencia:** `S(t) = P(T > t) = 1 − F(t)`. Probabilidad de seguir sin evento
  después de `t`. Es decreciente, vale 1 en `t = 0` y tiende a 0.
- **Función de riesgo (*hazard*):** `h(t) = f(t) / S(t)`. Es la tasa instantánea de evento entre los
  que siguen en observación en `t`; no es una probabilidad (puede superar 1 si se mide en unidades
  grandes), es una tasa por unidad de tiempo.
- **Riesgo acumulado:** `H(t) = ∫₀ᵗ h(u) du = −ln S(t)`.
- **Censura por la derecha:** para cada sujeto `i` se observa `(t_i, δ_i)`, donde `t_i` es el tiempo
  observado y `δ_i = 1` si el evento ocurrió en `t_i`, `δ_i = 0` si la observación se censuró ahí.
  El supuesto que hace válido todo lo demás es que la censura es **no informativa**: quien se censura
  en `t` tiene el mismo riesgo futuro que quien sigue, dadas las covariables. Cuando se postula una
  forma concreta para `S(t)` (exponencial, Weibull, lognormal) se habla de modelos paramétricos y se
  usan las [[distribuciones-continuas|distribuciones continuas]] de siempre.

**Estimador de Kaplan-Meier.** Con los tiempos de evento ordenados `t_1 < t_2 < …`, sea `d_i` el
número de eventos en `t_i` y `n_i` el número de sujetos en riesgo justo antes de `t_i`:

:::formula
S(t) = Π_{t_i ≤ t} ( 1 − d_i / n_i )
:::

- `d_i` — cuántos eventos ocurren exactamente en `t_i`. Los empates se tratan como un solo paso.
- `n_i` — cuántos sujetos siguen en observación en `t_i`, incluidos los que se censuran en ese mismo
  instante (se consideran en riesgo hasta justo después).
- La **mediana de supervivencia** es el menor `t` con `S(t) ≤ 0,5`. Se usa en vez de la media porque
  con censura alta la media no está identificada.

**Contraste de log-rank.** Para comparar dos curvas, en cada tiempo de evento se construye la tabla
2×2 de grupo contra evento. Sea `O` el número observado de eventos en el grupo 1 y `E` el esperado
si el grupo no importara:

:::formula
E = Σ_i d_i · n_{1i} / n_i          χ² = (O − E)² / V
:::

- `n_{1i}` — sujetos del grupo 1 en riesgo en `t_i`; `V` — la varianza hipergeométrica del recuento,
  `Σ_i d_i · (n_{1i}/n_i) · (1 − n_{1i}/n_i) · (n_i − d_i)/(n_i − 1)`.
- Bajo la hipótesis nula, `χ²` se distribuye aproximadamente como una ji-cuadrado con 1 grado de
  libertad.

**Modelo de riesgos proporcionales de Cox.** Con covariables `x` y coeficientes `β`:

:::formula
h(t | x) = h₀(t) · exp(βᵀx)
:::

- `h₀(t)` — el riesgo base, común a todos, que **no se especifica**: queda sin modelar.
- `β` — el efecto de cada covariable sobre el logaritmo del riesgo. La razón de riesgos
  (*hazard ratio*) de un aumento de una unidad en `x_j` es `HR_j = exp(β_j)`.
- Los `β` se estiman maximizando la **verosimilitud parcial**, que compara en cada tiempo de evento
  al que falla con todos los que seguían en riesgo:

:::formula
L(β) = Π_{i : δ_i = 1} exp(βᵀx_i) / Σ_{j ∈ R(t_i)} exp(βᵀx_j)
:::

- `R(t_i)` — el conjunto en riesgo en `t_i`. El riesgo base desaparece de la expresión, y eso es lo
  que hace al modelo semiparamétrico.
- El supuesto de **riesgos proporcionales** es que el cociente entre los riesgos de dos sujetos es
  constante en el tiempo. Todo el modelo cae si eso no se cumple.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T` | El tiempo hasta el evento, que es lo que se quiere modelar | tiempo (meses, días) | No es un parámetro que se mueva: es la variable respuesta. Con seguimientos cortos, su cola no se observa y la media deja de estar identificada |
| `S(t)` | Probabilidad de seguir sin evento después de `t` | adimensional, entre 0 y 1 | Es 1 en `t = 0` y solo puede bajar: cada evento la multiplica por un factor menor que 1. Si sube en algún tramo, el cálculo está mal |
| `h(t)` | La tasa instantánea de evento entre los que siguen en observación | eventos por unidad de tiempo | Más riesgo instantáneo significa caída más rápida de `S(t)`. No es una probabilidad: puede pasar de 1 si el tiempo se mide en unidades grandes |
| `d_i` | Eventos que ocurren exactamente en `t_i` | sujetos (recuento) | Cada evento extra multiplica la curva por un factor más pequeño: el escalón de ese instante es más grande. Con empates, un solo `β` de Cox promedia peor |
| `n_i` | Sujetos en riesgo justo antes de `t_i`, censurados incluidos | sujetos (recuento) | Un denominador mayor acerca el factor `(1 − d_i/n_i)` a 1: cada evento pesa menos. Es el mecanismo por el que la censura importa, porque encoge `n_i` en los pasos siguientes |
| `δ_i` | Indicador: 1 si el evento ocurrió, 0 si la observación se censuró | 0 o 1 | Cambia la fila de sitio: los `δ_i = 1` contribuyen a la curva y a la verosimilitud parcial; los `δ_i = 0` solo reducen `n_i`. Meterlos como eventos sesga `S(t)` a la baja |
| `β` | El efecto de cada covariable sobre el logaritmo del riesgo | logaritmo de razón de riesgos | Con `β > 0` la covariable aumenta el riesgo; con `β < 0` lo reduce. Se estima maximizando la verosimilitud **parcial**, porque `h₀(t)` se cancela |
| `h₀(t)` | El riesgo base, común a todos los sujetos | eventos por unidad de tiempo | No se estima y por eso el modelo es semiparamétrico. Su forma decide el efecto sobre `S(t)` a un plazo concreto, aunque deje `β` intacto |
| `HR_j = exp(β_j)` | La razón de riesgos por una unidad más de `x_j` | adimensional, mayor que 0 | `HR = 1` es efecto nulo, `HR = 0,49` es la mitad de riesgo instantáneo en cada instante. No se lee como probabilidad ni como «la mitad de bajas»: eso depende del riesgo base |
| `V` | La varianza hipergeométrica del recuento de eventos | eventos, al cuadrado | Aparece en el denominador de `χ²`: con pocos eventos por grupo, `V` es grande y el contraste pierde potencia. Por eso un log-rank con 24 sujetos y 16 eventos apenas distingue |
:::

## Ejemplo

Quince sujetos seguidos durante 15 meses. Ocho sufren el evento y siete se censuran. La tabla de
Kaplan-Meier se construye paso a paso:

```text
t   en riesgo   eventos   S(t)
1      15          1      0,9333
2      14          1      0,8667
3      13          1      0,8000
5      10          1      0,7200
6       9          1      0,6400
7       8          1      0,5600
10      5          1      0,4480
12      3          1      0,2987
```

- En `t = 3` hay dos observaciones (una con evento y otra censurada) y las dos cuentan como «en
  riesgo»: por eso `n = 13` y no 12.
- Entre `t = 7` y `t = 10` salen tres sujetos del conjunto en riesgo —el que sufrió el evento de
  `t = 7` y dos censuras, en `t = 8` y `t = 9`—, así que el denominador cae de 8 a 5 y el escalón
  de ese paso es mucho más grande (de 0,56 a 0,448) que el anterior.
- La mediana es **10 meses**: es el primer tiempo con `S(t) ≤ 0,5`.
- Si ignoras la censura y calculas `1 − 8/15 = 0,4667`, estás mezclando dos cosas: ese número sería
  la proporción de eventos si todos hubieran sido seguidos hasta el final, y aquí siete no lo
  fueron. Kaplan-Meier da 0,2987, bastante menos.

## Código

```python verificable
import numpy as np

# Tiempo observado en meses y si el evento ocurrio (1) o la observacion se censuro (0)
tiempo = np.array([1, 2, 3, 3, 5, 6, 7, 8, 10, 12, 4, 9, 11, 13, 15], dtype=float)
evento = np.array([1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0])

# Kaplan-Meier: en cada tiempo con evento, S se multiplica por (1 - d/n)
S, pasos = 1.0, []
for t in np.unique(tiempo[evento == 1]):
    en_riesgo = int((tiempo >= t).sum())                 # siguen en observacion en t
    casos = int(((tiempo == t) & (evento == 1)).sum())   # eventos en t
    S *= 1 - casos / en_riesgo
    pasos.append((t, en_riesgo, casos, S))

print("  ".join("t=%.0f n=%d d=%d S=%.4f" % p for p in pasos))
# -> t=1 n=15 d=1 S=0.9333  t=2 n=14 d=1 S=0.8667  t=3 n=13 d=1 S=0.8000  t=5 n=10 d=1 S=0.7200  t=6 n=9 d=1 S=0.6400  t=7 n=8 d=1 S=0.5600  t=10 n=5 d=1 S=0.4480  t=12 n=3 d=1 S=0.2987
print("supervivencia al final %.4f" % S)                     # -> supervivencia al final 0.2987
print("1 - eventos/total %.4f" % (1 - evento.sum() / evento.size))   # -> 1 - eventos/total 0.4667
print("mediana %.0f" % next(t for t, _, _, s in pasos if s <= 0.5))  # -> mediana 10
```

:::claves
- `tiempo >= t` es una comparación de array que devuelve un array de `True`/`False`, y `.sum()` los cuenta como 1 y 0. Por eso `int((tiempo >= t).sum())` es el número de sujetos en riesgo: no hay ningún bucle contando.
- `np.unique(tiempo[evento == 1])` da los tiempos con **evento**, ordenados y sin repetir. Si dentro del bucle recorrieras todos los tiempos observados en vez de solo esos, multiplicarías `S` también en los instantes de censura y la curva bajaría donde no debe. Ese es el error clásico al escribir Kaplan-Meier a mano.
- El paréntesis importa: `(tiempo == t) & (evento == 1)` combina dos condiciones elemento a elemento. En NumPy `and` no sirve (evalúa el array entero como un solo booleano y lanza un error): hay que usar `&`, cada condición entre paréntesis y `np.sum` en lugar de `sum` si quieres velocidad.
- `S` se va multiplicando paso a paso, así que va **acumulando** el error: es el producto de muchos factores, no una resta. Una errata en un solo `n_i` contamina todos los escalones posteriores, y no hay forma de detectarlo mirando solo el resultado final.
- `1 - evento.sum() / evento.size` es la cuenta ingenua, la que trata las censuras como si no existieran, y da 0,4667 frente al 0,2987 de Kaplan-Meier. Compáralas: si tu curva «a mano» coincide con la cuenta ingenua, has ignorado la censura.
- `next(t for t, _, _, s in pasos if s <= 0.5)` devuelve la primera `t` que cumple la condición: la mediana. Lanza `StopIteration` si la curva nunca baja de 0,5, y eso no es un fallo del código, es que con el seguimiento disponible la mediana **no está alcanzada**.
:::

```python verificable
import numpy as np
from math import erfc, sqrt

# 24 sujetos: 0 = control, 1 = tratamiento (12 en cada grupo)
tiempo = np.array([3, 5, 6, 8, 9, 11, 13, 15, 18, 21, 25, 30,
                   7, 10, 12, 16, 19, 22, 24, 27, 29, 33, 36, 40], dtype=float)
evento = np.array([1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                   1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0])
grupo = np.array([0] * 12 + [1] * 12, dtype=float)

def log_verosimilitud_parcial(beta):
    """Suma de log(exp(b*x_i) / suma de exp(b*x_j) sobre el conjunto en riesgo)."""
    total = 0.0
    for i in np.where(evento == 1)[0]:
        en_riesgo = tiempo >= tiempo[i]
        total += beta * grupo[i] - np.log(np.exp(beta * grupo[en_riesgo]).sum())
    return total

# El riesgo base no aparece: se maximiza la parcial en una rejilla, sin derivadas
rejilla = np.arange(-3.0, 3.0001, 0.001)
valores = np.array([log_verosimilitud_parcial(b) for b in rejilla])
beta = rejilla[valores.argmax()]
estadistico = 2 * (valores.max() - log_verosimilitud_parcial(0.0))
p = erfc(sqrt(estadistico / 2))     # ji-cuadrado con 1 grado de libertad = cola de una normal

print("beta estimado %.3f" % beta)                        # -> beta estimado -0.708
print("razon de riesgos exp(beta) %.3f" % np.exp(beta))   # -> razon de riesgos exp(beta) 0.493
print("log-verosimilitud nula %.3f" % log_verosimilitud_parcial(0.0))
# -> log-verosimilitud nula -41.559
print("log-verosimilitud max %.3f" % valores.max())       # -> log-verosimilitud max -40.670
print("estadistico LR %.2f  p = %.4f" % (estadistico, p)) # -> estadistico LR 1.78  p = 0.1824

# Log-rank: observados frente a esperados en el grupo 1, tiempo a tiempo
obs = esp = var = 0.0
for t in np.unique(tiempo[evento == 1]):
    riesgo = tiempo >= t
    n, n1 = riesgo.sum(), (riesgo & (grupo == 1)).sum()
    d = ((tiempo == t) & (evento == 1)).sum()
    d1 = ((tiempo == t) & (evento == 1) & (grupo == 1)).sum()
    obs += d1
    esp += d * n1 / n
    var += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
chi2 = (obs - esp) ** 2 / var
print("log-rank observados %.1f esperados %.1f chi2 %.2f p = %.4f"
      % (obs, esp, chi2, erfc(sqrt(chi2 / 2))))
# -> log-rank observados 8.0 esperados 10.5 chi2 1.85 p = 0.1740
```

## Errores típicos

- **Maltratar la censura.** Descartar a quien no ha sufrido el evento hunde la media y subestima la
  supervivencia: con censura alta, la media ni siquiera está identificada, así que usa la mediana y
  la curva. Y dar por buena la censura informativa es igual de grave: si los que se van del estudio
  son justo los de peor pronóstico, Kaplan-Meier está sesgado al alza y ninguna fórmula lo arregla.
- **Meter el tiempo como variable dependiente de una regresión lineal o logística.** Con una
  regresión lineal ignoras la censura y predices tiempos negativos; con una logística binaria
  conviertes «cuánto tarda» en «se fue o no», y eso depende de cuánto hayas esperado a cada sujeto,
  que es justo lo que varía. Para eso están Cox y los modelos paramétricos de supervivencia.
- **Leer la razón de riesgos como una probabilidad o como un efecto sobre la supervivencia.** Un
  `HR = 0,49` no significa «la mitad de bajas»: significa que, en cada instante, el riesgo
  instantáneo del grupo tratado es la mitad del de control. El efecto sobre `S(t)` a un año concreto
  depende del riesgo base y hay que calcularlo.
- **Dar por bueno el supuesto de riesgos proporcionales sin comprobarlo.** Si el efecto cambia con el
  tiempo (una intervención que aumenta el riesgo al principio y lo reduce después), un único `β`
  promedia cosas opuestas y oculta el fenómeno. Se comprueba con residuos de Schoenfeld o metiendo
  una interacción con el tiempo.
- **Definir mal el tiempo cero (sesgo de tiempo inmortal).** Si empiezas a contar desde que el sujeto
  recibe un tratamiento, y para recibirlo hay que seguir vivo hasta ese momento, el grupo tratado
  acumula supervivencia por construcción. El tiempo cero tiene que ser el mismo criterio para todos
  y situarse en el inicio del seguimiento.
- **Ignorar los empates y los riesgos en competencia.** Con muchos empates, la verosimilitud parcial
  con la aproximación de Breslow se queda corta y conviene el método exacto o el tiempo discreto. Y
  si hay dos eventos posibles (una operación que sale por objetivo o por stop), tratar uno como
  censura del otro cambia la pregunta: eso es un modelo de riesgos en competencia.

:::practica
enunciado: Diez sujetos con tiempos observados 2, 3, 3, 5, 6, 7, 9, 10, 12 y 14. Hay evento en t = 2, 3, 5, 6 y 9; el resto son censuras. Construye la Kaplan-Meier, da la mediana y compárala con 1 − 5/10.
pista: En cada tiempo con evento el denominador es cuántos siguen en observación; las censuras anteriores salen del riesgo pero no multiplican la curva.
solucion: En t = 2 hay 10 en riesgo y 1 evento: S = 1 − 1/10 = 0,9. En t = 3 quedan 9 y S = 0,9·(8/9) = 0,8. En t = 5 quedan 7 y S = 0,8·(6/7) = 0,6857. En t = 6 quedan 6: S = 0,6857·(5/6) = 0,5714. En t = 9 quedan 4: S = 0,5714·(3/4) = 0,4286. La mediana es 9 meses; ignorar la censura daría 0,5 y sobreestimaría la supervivencia.
:::

## Comprueba que lo sabes

:::quiz
p: Diez sujetos en observación. En el mes 4 hay dos bajas y en el mes 6 una censura. Con Kaplan-Meier, ¿qué se hace en el mes 6?
o: Se recalcula el denominador quitando al censurado y se deja la curva S(t) igual, sin escalón
o: Se multiplica S por (1 - 1/10) porque la censura también es un evento
o: Se ignora la censura y se sigue con los diez sujetos
a: 1
e: La censura no produce escalón: sale del conjunto en riesgo para los pasos siguientes, con lo que el denominador baja y los eventos posteriores pesan más. No es un evento (no multiplica a S) y tampoco se puede ignorar, porque seguir contando a alguien que ya no se observa infravalora los escalones siguientes.
:::

:::quiz
p: Estimas la duración media de un cliente descartando a los que aún no se han dado de baja. ¿Qué sesgo introduces?
o: Ninguno: los que no se han ido no aportan información sobre el tiempo hasta la baja
o: Subestimas la duración, porque te quedas con los que se van antes
o: Sobreestimas la duración, porque te quedas con los clientes más fieles
a: 2
e: Al borrar a los censurados eliminas a todos los que llevan mucho tiempo sin irse, así que la media queda dominada por las bajas tempranas: la duración estimada sale corta. Su información es una cota inferior del tiempo real, y Kaplan-Meier la aprovecha.
:::

:::quiz
p: En un modelo de Cox obtienes un hazard ratio de 0,49 para un tratamiento, con un estadístico de log-verosimilitud de 1,78. ¿Qué conclusión es correcta?
o: El tratamiento reduce el riesgo a la mitad y el resultado es significativo
o: El riesgo instantáneo estimado del grupo tratado es la mitad, pero con estos datos no se puede rechazar que el efecto sea nulo
o: El tratamiento reduce la supervivencia, porque 0,49 es menor que 1
a: 2
e: La razón de riesgos 0,49 apunta a la mitad de riesgo instantáneo, pero el contraste de razón de verosimilitud da 1,78, por debajo del valor crítico 3,84 de una ji-cuadrado con 1 grado de libertad (p = 0,18). Con 24 sujetos la estimación es compatible con el efecto nulo. Un HR menor que 1 indica menos riesgo, no menos supervivencia.
:::

:::nota
Con censura alta, la media de `T` no está identificada porque la cola de la distribución no se
observa. La mediana sí: solo necesita que la curva baje de 0,5, y si no lo hace se reporta «no
alcanzada» con el seguimiento disponible.
:::
