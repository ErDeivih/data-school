---
id: ab-testing
titulo: Tests A/B
fase: 2
nivel: intermedio
rutas: [ds, de]
prerequisitos: [contraste-de-hipotesis, p-valor, test-t, tamano-muestral, errores-tipo-i-ii-y-potencia]
tags: [experimentacion, producto, aleatorizacion, metricas]
resumen: Un experimento aleatorizado con métrica decidida de antemano, duración calculada y reglas de parada fijadas antes de mirar los datos.
fuentes: ["Kohavi, Tang y Xu (2020), 'Trustworthy Online Controlled Experiments'"]
---

## En una frase

Un test A/B es un experimento en el que repartes unidades al azar entre dos o más variantes y
comparas una métrica decidida de antemano; la aleatorización es lo que hace que las diferencias
que veas se puedan atribuir a la variante y no a quién cayó en cada grupo.

## La idea

La alternativa al test A/B es comparar antes y después, o comparar con los que no usaron la
función. Las dos cosas fallan por el mismo motivo: los grupos no son comparables. Los usuarios que
usan una función nueva son distintos —más activos, más curiosos, más antiguos— de los que no la
usan, y esa diferencia se mezcla con el efecto que quieres medir. Es el problema de los
[[confusores-y-dag|confusores]] en su versión más práctica.

La aleatorización arregla esto de raíz. Si asignas el tratamiento con una moneda, los dos grupos
se parecen **en todo**, incluido lo que no has medido ni sabes que existe, y las diferencias que
queden son atribuibles a la variante (con un margen de error que cuantifica el
[[p-valor]]). Ese es todo el valor del método, y por eso se destruye tan fácilmente: basta con
romper la aleatorización para volver al punto de partida.

Un experimento honesto se decide **antes** de lanzarlo. Como mínimo:

1. **La métrica principal**, una sola. Puede ser conversión, ingresos por usuario, retención a 7
   días. Si eliges la métrica después de ver los resultados, no tienes un test, tienes una
   búsqueda.
2. **Las métricas de guardarraíl** que no deben empeorar: latencia, tasa de error, ingresos,
   tickets de soporte. Un aumento de conversión que se paga con el doble de latencia no es una
   mejora.
3. **El efecto mínimo detectable** (MDE): la diferencia más pequeña que justificaría implementar
   el cambio. De ahí sale el tamaño muestral, y de ahí la duración.
4. **La regla de parada**, fijada de antemano. Lo normal es «analizar cuando se alcance `n`», no
   «mirar todos los días a ver qué tal».

Dos advertencias que se subestiman siempre:

- **El efecto de novedad.** En la primera semana, los usuarios reaccionan al cambio en sí
  (curiosidad, o al contrario, resistencia al cambio). El efecto medido en los primeros días no es
  el efecto a largo plazo. Un experimento que dura cuatro días mide, en buena parte, novedad.
- **La interferencia.** Si los usuarios del grupo de control se relacionan con los del grupo de
  tratamiento (mercados, redes sociales, equipos que comparten una cola), el control deja de ser
  un control limpio. Ahí la aleatorización por usuario no basta: hay que aleatorizar por
  conglomerado (ciudad, mercado, equipo) y asumir menos potencia.

## Definición formal

Para una métrica binaria (convierte o no), con tasa base `p₀` y efecto mínimo detectable `δ` en
puntos absolutos, el número de unidades por rama es:

:::formula
n = 2 · (z₁₋α/₂ + z₁₋β)² · p₀ · (1 − p₀) / δ²
:::

- `p₀` — tasa base de la métrica en el grupo de control (por ejemplo 0,12).
- `δ` — MDE en la misma escala que `p₀` (por ejemplo 0,01, un punto porcentual).
- `α` — probabilidad de falso positivo aceptada; `z₁₋α/₂` es el cuantil normal (1,96 con α = 0,05).
- `1 − β` — potencia; `z₁₋β` es el cuantil normal (0,84 con potencia del 80 %).
- `n` — unidades por rama; el total es `2n` con dos ramas.

Para una métrica continua, la misma estructura con la varianza en lugar de `p₀(1 − p₀)`:

:::formula
n = 2 · (z₁₋α/₂ + z₁₋β)² · σ² / δ²
:::

La **duración** sale de dividir el total entre el tráfico diario elegible, y luego se redondea
hacia arriba hasta semanas completas, porque el comportamiento depende del día de la semana.

:::figura
fichero: ab-testing-muestra-y-mirar-cada-dia
pie: En el panel izquierdo, la muestra necesaria por rama según el efecto mínimo detectable que fijes: el punto rojo es el MDE de un punto porcentual del ejemplo, y la curva deja claro que partir el efecto por la mitad multiplica la muestra por cuatro, no por dos. En el derecho, 20.000 experimentos simulados en los que las dos ramas convierten exactamente igual: si mirases el resultado cada día y cortaras al primer día que el p baja de 0,05, el error de tipo I llegaría al 22 % en vez del 5 % que prometiste. La consecuencia práctica es que la duración se fija antes y no se toca.
fuente: figuras/ab-testing-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Unidades necesarias por rama | usuarios o visitas | Es el resultado de la formula. Cuadruplica cuando el efecto que quieres detectar se reduce a la mitad, y el total con dos ramas es `2n`: 16.577 por rama son 33.154 unidades y 16,6 dias del trafico del ejemplo |
| `p0` | Tasa base de la métrica en el control | tanto por uno | Sube la varianza de una métrica binaria, `p0(1-p0)`, hasta el maximo en 0,5 y luego la baja. Una base del 50 % es la situación mas cara de medir; con la misma base y el mismo MDE absoluto, cerca de 0 o de 1 hace falta menos gente |
| `delta` | Efecto mínimo detectable, en puntos absolutos | los de la métrica | Es la palanca mas fuerte: `n` va con `1/delta^2`. Pasar de 1 a 0,5 puntos porcentuales cuadruplica la muestra, y por eso el MDE es una decisión de negocio que se toma antes de mirar datos |
| `alpha` | Riesgo de falso positivo que aceptas | probabilidad | Entra en `z_(1-alpha/2)`: bajarlo de 0,05 a 0,01 sube ese cuantil de 1,96 a 2,58 y engorda `n` casi un 50 % con los demas números del ejemplo. Es el precio de exigir mas evidencia, y no dice nada de la potencia |
| `1 - beta` | Potencia: probabilidad de detectar un efecto del tamaño `delta` | probabilidad | `z_(1-beta)` pasa de 0,842 con potencia 0,80 a 1,282 con 0,90: subir la potencia diez puntos cuesta un 34 % mas de muestra (16.577 → 22.192 por rama con los demas números del ejemplo). Se decide antes de lanzar, y la potencia calculada a posteriori con el efecto observado no vale para nada |
| `sigma` | Desviación típica de la métrica continua | las de la métrica | Solo aparece en la versión continua, donde sustituye a `p0(1-p0)`. `n` va con `sigma^2`: duplicar la variabilidad del proceso duplica, otra vez, la gente necesaria |
| `z_(1-alpha/2)`, `z_(1-beta)` | Cuantiles de la normal estandar | adimensionales | No son parámetros que se elijan: se despejan de `alpha` y de la potencia. Copiarlos a mano de una tabla y equivocarse de columna es un clasico: 1,645 es para una cola, no para un contraste bilateral |
| `chi2` | Estadistico del chequeo de reparto (SRM): `suma (O_i - E_i)^2 / E_i` | adimensional | Se compara con una chi-cuadrado de `ramas - 1` grados de libertad, nunca con el p-valor de la métrica. Un `chi2` alto con p por debajo de 0,001 significa que la asignación esta rota y la métrica no se lee |
:::

**Chequeo de reparto (SRM, *sample ratio mismatch*).** Antes de mirar la métrica, comprueba que el
reparto es el que diseñaste. Con `O` los tamaños observados y `E` los esperados:

:::formula
χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ  ,   gl = ramas − 1
:::

Un SRM con p < 0,001 es una señal de alarma: el sistema de asignación, el filtrado de bots o la
instrumentación están rompiendo el experimento. Si hay SRM, la métrica no se interpreta.

**Sobre el «mirar todos los días».** Cada vez que miras y decides parar si el p baja de 0,05,
gastas `α`. Con muchas miradas, el error de tipo I real se dispara muy por encima del 5 %. Si
necesitas monitorizar, usa un contraste secuencial que reparta `α` entre las miradas, o fija la
duración y no la toques.

## Ejemplo

Una tienda con 2.000 visitas diarias elegibles. La conversión base es del 12 % y decides que merece
la pena implementar un cambio si sube al menos **1 punto porcentual** (hasta el 13 %; en términos
relativos, un 8,3 % más).

- `z₁₋α/₂` = 1,96 con α = 0,05; `z₁₋β` = 0,842 con potencia del 80 %.
- `n` = 2 · (1,96 + 0,842)² · 0,12 · 0,88 / 0,01² = **16.577 unidades por rama**.
- Total: **33.154**, es decir, **16,6 días** de tráfico a 2.000 visitas diarias.
- Redondeando a semanas completas: **3 semanas** (21 días), unas 42.000 unidades.

Y el chequeo de reparto antes de mirar nada. Esperabas 10.000 y 10.000 unidades y llegaron 10.180
y 9.820:

- `χ²` = 180²/10.000 + 180²/10.000 = **6,48** con 1 grado de libertad → **p ≈ 0,011**.
- La proporción observada es 0,509, no 0,500.

Un desvío del 1,8 % en el reparto con esta muestra ya es sospechoso. Con un p tan bajo, lo
razonable es **no leer la métrica** y buscar la causa: ¿se filtraron los bots de una rama? ¿el
enrutado perdía un 1 % de peticiones? ¿el evento de exposición no se registra igual en las dos?

## Código

```python verificable
import numpy as np
from scipy import stats

# Cuantas unidades hacen falta para detectar un punto porcentual sobre una base del 12 %.
p0, mde, alfa, potencia = 0.12, 0.01, 0.05, 0.80
z_a = stats.norm.ppf(1 - alfa / 2)
z_b = stats.norm.ppf(potencia)
n = 2 * (z_a + z_b) ** 2 * p0 * (1 - p0) / mde ** 2

print(f"z_alfa {z_a:.3f}  z_beta {z_b:.3f}")     # -> z_alfa 1.960  z_beta 0.842
print(f"n por rama {n:.0f}")                     # -> n por rama 16577
print(f"dias a 2000 visitas/dia {2 * n / 2000:.1f}")  # -> dias a 2000 visitas/dia 16.6
```

:::claves
- `stats.norm.ppf(potencia)` se lleva la **potencia**, no `beta`: `ppf(0.80)` es 0,842, que es el cuantil que buscas. Escribir `stats.norm.ppf(1 - potencia)` da −0,842, y como el cuantil va **sumado** a `z_a` dentro del paréntesis al cuadrado, el resultado encoge en vez de crecer. El número sale plausible, que es lo peor: da 2.641 por rama en vez de 16.577.
- `stats.norm.ppf(1 - alfa / 2)` es bilateral. Para un contraste de una cola sería `ppf(1 - alfa)`, es decir 1,645 con α = 0,05, y eso reduce la muestra un 21 %. Las dos fórmulas son correctas según el diseño, pero mezclarlas es un error de planteamiento, no de tecleo.
- `n` sale como `np.float64` con decimales (16576,83) porque los cuantiles son continuos. Redondear **hacia arriba** y no hacia abajo es una decisión: 16.576 no cumple la potencia prometida, y la página redondea luego a semanas completas por el patrón semanal. `int(n)` trunca y `np.ceil(n)` redondea arriba; no son lo mismo.
- `2 * n / 2000` convierte unidades por rama en días: el total es `2n` y se divide entre el tráfico diario **elegible**, no entre el tráfico total. Si la métrica solo se mide en un 60 % de las visitas, ese 2.000 baja y los 16,6 días suben en la misma proporción. La fórmula no lo sabe: lo pones tú.
- `stats.chisquare(observado, esperado)` devuelve un objeto `Power_divergenceResult`, no una tupla: de ahí que las dos líneas del bloque usen `.statistic` y `.pvalue` en vez de desempaquetar. El mismo objeto se obtiene de `stats.power_divergence`, que es la función que hace el trabajo; `chisquare` es el envoltorio con la corrección de que las dos sumas tienen que cuadrar. Como en el SRM esperado y observado suman lo mismo, invertir los dos argumentos apenas cambia el número (6,4800 frente a 6,4821), y ese parecido es una trampa: con esperados no uniformes la diferencia deja de ser cosmética.
- `observado[0] / observado.sum()` da 0,5090: la proporción observada, no la esperada. El SRM no se juzga por la proporción (0,509 parece casi 0,5) sino por el p-valor, porque con 20.000 unidades una desviación del 1,8 % es incompatible con una moneda justa. Mirar el porcentaje y no el contraste es el error de lectura más común de este chequeo.
:::

```python verificable
import numpy as np
from scipy import stats

# Chequeo de SRM: esperaba 50/50 y llego esto. Hay que investigar antes de leer la metrica.
observado = np.array([10180, 9820])
esperado = np.array([10000, 10000])
chi2, p = stats.chisquare(observado, esperado)

print(f"chi2 {chi2:.2f}  p {p:.4f}")                        # -> chi2 6.48  p 0.0109
print(f"proporcion observada {observado[0] / observado.sum():.4f}")
# -> proporcion observada 0.5090
```

## Errores típicos

- **Parar el experimento en cuanto el p-valor cruza 0,05.** Es el error más caro y el más
  frecuente: mirar cada día y cortar cuando sale bien infla el error de tipo I muy por encima del
  5 %. Si necesitas monitorizar, usa un contraste secuencial con `α` repartido.
- **Analizar por sesiones o por impresiones cuando aleatorizaste por usuario.** La misma persona
  aparece muchas veces y sus visitas no son independientes: los errores típicos se quedan cortos y
  el p-valor sale demasiado pequeño. Analiza en la unidad en la que aleatorizaste.
- **Ignorar un SRM.** Si el reparto no es el diseñado, el experimento está roto. Da igual lo
  bonito que sea el resultado de la métrica: no se interpreta.
- **Correr menos de una semana completa.** El comportamiento del lunes no es el del sábado. Un
  test de tres días confunde el efecto con el patrón semanal.
- **Cambiar la métrica principal después de ver los resultados.** Si la de conversión no salió y
  la de clics sí, la de clics pasa a ser «la que importaba». Eso es
  [[multiplicidad-y-fdr|multiplicidad]] disfrazada.
- **No definir guardarraíles.** Una variante puede mejorar la conversión y empeorar la latencia,
  los errores o los reembolsos. Si no los miras, no los ves.
- **Confundir significación con relevancia.** Con millones de usuarios, una mejora de 0,02 puntos
  porcentuales sale significativa y no paga ni una hora de desarrollo. Compara el efecto estimado
  con el MDE que fijaste.
- **Generalizar desde usuarios nuevos.** Si el experimento solo cubre a quien llega por primera
  vez, el efecto de novedad domina y la extrapolación a los usuarios habituales es un salto sin
  base.
- **Lanzar varias variantes y comparar todas contra el control sin corregir.** Con 5 variantes
  son 5 comparaciones: corrige, o diseña el experimento para una sola pregunta.

## Comprueba que lo sabes

:::quiz
p: Vas a medir conversión (base 12 %) y decides que solo te interesa un cambio de al menos 1 punto porcentual. Con alpha = 0,05 y potencia del 80 %, ¿cuántas unidades necesitas por rama?
o: Unas 1.700, porque se redondea el efecto a dos cifras
o: Unas 16.600, porque el efecto es muy pequeño respecto a la variabilidad de una variable binaria
o: Depende solo del tráfico disponible, no del efecto
a: 2
e: La fórmula n = 2 (z_alfa + z_beta)^2 p0(1-p0)/delta^2 da 16.577 por rama. El tamaño muestral sale del efecto mínimo detectable: cuanto más pequeño es el efecto que quieres ver, más datos hacen falta, y crece con el cuadrado de la inversa de delta.
:::

:::quiz
p: El reparto esperado era 50/50 y observas 10.180 frente a 9.820 con p = 0,011 en el chequeo de SRM. ¿Qué haces?
o: Seguir adelante, porque el experimento tenía tráfico suficiente
o: Investigar el sistema de asignación y no interpretar la métrica hasta resolverlo
o: Meter el desequilibrio como covariable en el análisis final
a: 2
e: Un desequilibrio en el reparto indica que algo del sistema (filtrado de bots, enrutado, instrumentación) está rompiendo la aleatorización. Sin aleatorización el contraste pierde su interpretación causal, así que primero se arregla y luego se mide. Ajustar por el desequilibrio no recupera lo que se ha roto.
:::

:::quiz
p: Un test A/B da una mejora de conversión del 0,05 % relativo con p = 0,002 sobre 4 millones de usuarios. ¿Qué conclusión es sensata?
o: Es un resultado sólido: p muy pequeño y muestra enorme
o: Es un efecto real pero casi con seguridad irrelevante para la decisión, porque no llega al efecto mínimo detectable que fijaste
o: El p-valor está mal calculado con tanta muestra
a: 2
e: Con muestras enormes se detectan efectos minúsculos. El p-valor dice que la diferencia no es azar, no que importe. La pregunta la contesta el tamaño del efecto comparado con el MDE y con el coste de implementar el cambio.
:::

:::practica
enunciado: Un equipo quiere detectar un aumento de la retención semanal del 40 % al 42 % con alpha = 0,05 y potencia del 80 %. El servicio tiene 5.000 usuarios nuevos a la semana, repartidos a partes iguales entre las dos ramas. ¿Cuántas semanas debe durar el experimento como mínimo y por qué no basta con 4 días?
pista: Usa la fórmula de proporciones con p0 = 0,40 y delta = 0,02; luego divide el total entre 5.000 usuarios semanales y redondea a semanas completas.
solucion: n por rama = 2 (1,96 + 0,842)^2 x 0,40 x 0,60 / 0,02^2 = 2 x 7,849 x 0,24 / 0,0004 = 9.419 usuarios por rama, es decir 18.838 en total. Con 5.000 usuarios nuevos por semana, el total de ambas ramas avanza a 5.000 por semana, así que hacen falta 18.838 / 5.000 = 3,8 semanas: cuatro semanas completas. Cuatro días no bastan por dos motivos: no llegas a la muestra necesaria (tendrías unas 2.850 unidades, muy por debajo de 18.838) y además el comportamiento de retención depende del día de la semana, así que un tramo corto mezcla el efecto con el patrón semanal.
:::

:::trampa
Un test A/B que «casi salía» y al que le añades una semana más hasta que cruza el 0,05 no es un
test con más datos: es un test con el umbral elegido a posteriori. La regla de parada se decide
antes, y si no la decidiste, el p-valor que tienes ya no significa lo que crees.
:::
