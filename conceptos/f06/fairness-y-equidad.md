---
id: fairness-y-equidad
titulo: Equidad y métricas de fairness
fase: 6
nivel: avanzado
rutas: [ds]
prerequisitos: [matriz-de-confusion, metricas-de-clasificacion, umbrales-y-coste]
tags: [equidad, sesgo, metricas, decision]
resumen: Paridad demográfica, igualdad de oportunidades y calibración por grupos: tres definiciones razonables de «justo» que no se pueden cumplir a la vez.
fuentes: ["Chouldechova (2017), 'Fair prediction with disparate impact: A study of bias in recidivism prediction instruments'", "Hardt, Price y Srebro (2016), 'Equality of Opportunity in Supervised Learning'", "Kleinberg, Mullainathan y Raghavan (2016), 'Inherent Trade-Offs in the Fair Determination of Risk Scores'"]
---

## En una frase

La equidad no es una propiedad del modelo, sino de cómo reparte sus errores entre grupos, y hay
varias formas razonables de medirla que resultan incompatibles entre sí.

## La idea

Un sistema decide a quién se llama a una entrevista, a quién se concede un crédito o a quién se le
hace una revisión adicional. Todos esos modelos tienen una variable protegida cerca: el grupo al que
pertenece la persona. «Que sea justo» significa al menos cuatro cosas distintas, y conviene saber
cuál pides:

1. **Mismo porcentaje de seleccionados.** Que del grupo A salga seleccionado el mismo porcentaje de
   gente que del grupo B. Es la **paridad demográfica** y es lo que mira casi todo el mundo, porque
   se calcula en una línea. No mira si la persona lo merecía: solo cuenta cabezas seleccionadas.
2. **Misma exhaustividad entre los que valían.** De los que de verdad eran aptos, que se seleccione
   el mismo porcentaje en cada grupo. Es la **igualdad de oportunidades**, y es la definición
   razonable cuando importa no dejar fuera a nadie que lo merecía.
3. **Los mismos errores en los dos sentidos.** Igual exhaustividad *y* las mismas falsas alarmas en
   cada grupo. Es la **igualdad de odds**: un grupo no puede llevarse más señalados injustamente.
4. **Que la puntuación signifique lo mismo.** Un 0,7 tiene que querer decir 70 % en los dos grupos:
   es la **calibración por grupos** ([[calibracion]]) o paridad predictiva.

Aquí llega el resultado incómodo, y es un teorema, no una opinión: si la prevalencia real es
distinta en los dos grupos y el modelo no es perfecto, **no se pueden cumplir a la vez la
calibración por grupos y la igualdad de odds**. Cualquier herramienta que se anuncie como «justa»
está eligiendo una definición y callando las demás.

El caso que hizo famoso esto fue la discusión pública de 2016 sobre una herramienta de predicción de
reincidencia usada en Estados Unidos: las dos partes usaban los mismos datos y discutían sin
entenderse, porque una medía falsas alarmas por grupo y la otra, calibración dentro de cada nivel de
riesgo. Ninguna mentía; hablaban de definiciones distintas de justicia.

Dos consecuencias prácticas antes de tocar nada:

- **Borrar la variable protegida no arregla nada.** El modelo la reconstruye con variables
  correlacionadas: código postal, centro de estudios, tipo de dispositivo, patrón de gasto. Si no
  mides por grupo, no ves la disparidad; solo has dejado de mirar ([[importancia-de-variables]]).
- **La equidad no sale gratis.** Igualar tasas de selección suele exigir decidir distinto a dos
  personas idénticas que solo se diferencian en el grupo, y sube las falsas alarmas de uno de los
  grupos. Eso tiene coste real y hay que decirlo en voz alta ([[umbrales-y-coste]]).

## Definición formal

Con `A` el grupo, `Y` el resultado real y `Ŷ` la decisión del modelo:

:::formula
Paridad demográfica:  P(Ŷ = 1 | A = a) igual para todo grupo a
:::

:::formula
Igualdad de oportunidades:  P(Ŷ = 1 | Y = 1, A = a) igual para todo grupo a
:::

:::formula
Igualdad de odds:  la anterior y además P(Ŷ = 1 | Y = 0, A = a) igual para todo grupo a
:::

:::formula
Paridad predictiva:  P(Y = 1 | Ŷ = 1, A = a) igual para todo grupo a
:::

- `A` — el grupo al que pertenece la persona: la variable protegida (sexo, origen, edad, barrio).
- `Y` — lo que de verdad pasó: si era apta, si pagó el crédito, si reincidió. Es la etiqueta.
- `Ŷ` — lo que decide el modelo al aplicar el umbral sobre la puntuación.
- `a` — un valor concreto de `A`. Las fórmulas dicen «igual para todo `a`»: se comparan los grupos
  dos a dos.
- La **prevalencia** `π_a = P(Y = 1 | A = a)` es la proporción real de positivos en el grupo. No es
  una propiedad del modelo; es cómo está el mundo.
- `TPR_a` — exhaustividad dentro del grupo: qué fracción de los que valían fue seleccionada.
- `FPR_a` — falsas alarmas dentro del grupo: qué fracción de los que no valían fue seleccionada.

En la tabla escribo `/` donde la fórmula lleva la barra de condicionado, para no romper la tabla.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `A` | Grupo al que pertenece la persona (variable protegida) | categorías | Con más grupos, más comparaciones y más riesgo de encontrar una brecha por azar |
| `Y` | Resultado real, la etiqueta | 0 o 1 | Su media por grupo es la prevalencia `π_a`, el motor de todo el conflicto |
| `Ŷ` | Decisión del modelo con el umbral aplicado | 0 o 1 | Bajando el umbral sube `P(Ŷ = 1 / A = a)` en todos los grupos |
| `π_a` | Prevalencia real del grupo `a` | adimensional, de 0 a 1 | Con prevalencias distintas, la paridad demográfica y la igualdad de odds chocan |
| `TPR_a` | Exhaustividad del grupo: `P(Ŷ = 1 / Y = 1, A = a)` | adimensional | La igualdad de oportunidades pide que sea la misma en todos los grupos |
| `FPR_a` | Falsas alarmas del grupo: `P(Ŷ = 1 / Y = 0, A = a)` | adimensional | La igualdad de odds pide además que sea la misma |
| `P(Ŷ = 1 / A = a)` | Tasa de selección del grupo | adimensional | Es la que exige la paridad demográfica; también la más fácil de falsear con el umbral |
| brecha | Diferencia entre el grupo mayoritario y el minoritario | adimensional | Se reporta como brecha: 0,143 en tasa de selección, por ejemplo |
:::

:::figura
fichero: fairness-y-equidad-paridad-frente-a-oportunidad
pie: A la izquierda, las tasas de selección de un mismo modelo, con idénticas curvas de acierto y de falsa alarma en los dos grupos. Las dos curvas no se cruzan: con un corte único de 0,50 el grupo A selecciona al 40 % y el B al 25 %, y eso no se arregla con ningún umbral intermedio. La línea negra discontinua marca el 33 % que pide la paridad demográfica, y alcanzarlo exige un umbral de 0,56 para A y de 0,46 para B. El panel derecho enseña el precio: con esos umbrales la exhaustividad del grupo A cae al 90 % mientras la del B sube al 97 %, y las falsas alarmas se van al 24 % en B frente al 8 % en A. Cumplir la primera definición rompe las otras dos, y no por un defecto del modelo: es la aritmética de las prevalencias.
fuente: figuras/fairness-y-equidad-1.py
:::

## Ejemplo

Mil personas del grupo A, de las que 300 son aptas de verdad, y 500 del grupo B, con 60 aptas. El
modelo es el mismo para todos y acierta igual de bien: con el umbral 0,50 selecciona al 95 % de las
aptas y genera un 16 % de falsas alarmas en los dos grupos.

| Grupo | Aptas | De las aptas, seleccionadas | No aptas | Falsas alarmas | Tasa de selección |
| --- | --- | --- | --- | --- | --- |
| A | 300 | 286 | 700 | 111 | 39,7 % |
| B | 60 | 57 | 440 | 70 | 25,4 % |

- La brecha de paridad demográfica es de **14,3 puntos** (39,7 % frente a 25,4 %).
- La brecha de exhaustividad es de **0,3 puntos** (95,3 % frente a 95,0 %): no hay ninguna.
- La brecha de falsas alarmas es de **0,1 puntos**: tampoco.

Es decir, el modelo cumple la igualdad de oportunidades y la igualdad de odds, y falla la paridad
demográfica. Y no ha hecho nada malo: el grupo A tiene dos veces y media la prevalencia del B, así
que cualquier regla que trate igual a los dos entra más en A. Si el comité exige paridad demográfica y fija el
objetivo en el 33 % de seleccionados, los umbrales que la consiguen son **0,56 para A** y **0,46 para
B**, y entonces la exhaustividad pasa a ser 89,7 % en A y 97,4 % en B: la brecha salta a 7,7 puntos y
las falsas alarmas se van al 23,7 % en B. Cumplir una definición ha roto las otras dos, con el mismo
modelo. Eso es la imposibilidad, con números.

## Código

```python verificable
import numpy as np

# Mismo modelo en los dos grupos. Cada fila: [aciertos, falsos negativos, falsas alarmas, rechazos correctos]
a = np.array([286, 14, 111, 589])      # grupo A: 1.000 personas, 300 aptas de verdad
b = np.array([57, 3, 70, 370])         # grupo B:   500 personas,  60 aptas de verdad


def tasas(x):
    tp, fn, fp, tn = x
    return (tp + fp) / x.sum(), tp / (tp + fn), fp / (fp + tn)


sel_a, tpr_a, fpr_a = tasas(a)
sel_b, tpr_b, fpr_b = tasas(b)
print(f"tasa de seleccion  A {sel_a:.3f}  B {sel_b:.3f}  brecha {abs(sel_a - sel_b):.3f}")
print(f"exhaustividad      A {tpr_a:.3f}  B {tpr_b:.3f}  brecha {abs(tpr_a - tpr_b):.3f}")
print(f"falsas alarmas     A {fpr_a:.3f}  B {fpr_b:.3f}  brecha {abs(fpr_a - fpr_b):.3f}")
# -> tasa de seleccion  A 0.397  B 0.254  brecha 0.143
# -> exhaustividad      A 0.953  B 0.950  brecha 0.003
# -> falsas alarmas     A 0.159  B 0.159  brecha 0.001
```

:::claves
- `tasas` devuelve una **tupla** de tres floats y no toca el array de entrada. Si en lugar de un array escribieras los cuatro recuentos como columnas de un DataFrame, esta misma función tendría que cambiar: aquí el desempaquetado `tp, fn, fp, tn = x` funciona porque `x` tiene exactamente cuatro elementos.
- El orden de la contingencia importa y no lo comprueba nadie: si intercambias falsos negativos y falsas alarmas, `tp / (tp + fn)` sigue dando un número plausible y el diagnóstico entero se invierte sin ningún error.
- Las denominaciones son las que producen las trampas: `tp / (tp + fn)` divide entre los positivos reales del grupo (exhaustividad), y `fp / (fp + tn)` entre los negativos reales (falsas alarmas). Confundir el denominador es el error más común al calcular fairness a mano.
- `x.sum()` sobre el array suma los cuatro recuentos y da el tamaño del grupo: 1.000 y 500. Sirve para la tasa de selección, pero **no** para las otras dos tasas, que llevan su propio denominador.
- Con estos datos, la brecha de exhaustividad es 0,003 y la de falsas alarmas 0,001: las dos caben dentro del ruido de una muestra de este tamaño. Sin un [[intervalos-de-confianza|intervalo de confianza]] no puedes afirmar que el modelo trate mejor o peor a un grupo en esos dos aspectos, solo que la tasa de selección difiere, que es una diferencia aritmética y no estadística.
:::

```python verificable
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

# Mismo modelo en los dos grupos; lo unico que cambia es la prevalencia real.
mu_pos, mu_neg, sd = 0.75, 0.35, 0.15
pi_a, pi_b = 0.30, 0.12


def seleccion(umbral, pi):
    tpr = 1.0 - norm.cdf((umbral - mu_pos) / sd)      # exhaustividad del grupo
    fpr = 1.0 - norm.cdf((umbral - mu_neg) / sd)      # falsas alarmas del grupo
    return pi * tpr + (1.0 - pi) * fpr


# Objetivo de paridad demografica: la misma tasa de seleccion en los dos grupos.
objetivo = 0.5 * (seleccion(0.50, pi_a) + seleccion(0.50, pi_b))
u_a = brentq(lambda u: seleccion(u, pi_a) - objetivo, 0.0, 1.0)
u_b = brentq(lambda u: seleccion(u, pi_b) - objetivo, 0.0, 1.0)
exhaustividad = lambda u: 1.0 - norm.cdf((u - mu_pos) / sd)

print(f"objetivo {objetivo:.3f}  umbral A {u_a:.2f}  umbral B {u_b:.2f}")
print(f"exhaustividad A {exhaustividad(u_a):.3f}  B {exhaustividad(u_b):.3f}")
# -> objetivo 0.325  umbral A 0.56  umbral B 0.46
# -> exhaustividad A 0.897  B 0.974
```

## Errores típicos

- **Mirar solo la exactitud global.** Con prevalencias distintas, un modelo que no selecciona a
  nadie del grupo minoritario puede tener una exactitud altísima, porque la mayoría de ese grupo no
  era apta. Sin métricas por grupo no ves nada ([[metricas-de-clasificacion]]).
- **Elegir la métrica de equidad después de ver los resultados.** Con cuatro definiciones y varios
  umbrales, siempre habrá una que salga bien. Fija la métrica y el umbral antes de medir, y reporta
  las demás como diagnóstico, no como titular.
- **Confundir disparidad con discriminación.** Una diferencia entre grupos no dice nada de la causa:
  puede venir de una variable legítima que se reparte de forma desigual
  ([[causalidad-vs-correlacion]], [[confusores-y-dag]]). Para atribuir causa hacen falta métodos
  causales, no una tabla de contingencia.
- **Igualar métricas con umbrales distintos y no contarlo.** Cumple la paridad demográfica, pero
  decide distinto a dos personas idénticas que solo se diferencian en el grupo. Puede ser lo
  correcto y puede ser ilegal, según el caso: es una decisión que se documenta, no un detalle de
  implementación.
- **Medir grupos pequeños y creerse la brecha.** Con 60 personas en el grupo minoritario, una
  diferencia de cinco puntos es ruido de muestreo. Sin intervalo de confianza o bootstrap, estás
  mirando azar y llamándolo sesgo.
- **Optimizar la métrica de equidad y olvidar el coste.** Subir la exhaustividad de un grupo bajando
  su umbral sube sus falsas alarmas, y esas falsas alarmas son personas señaladas injustamente. La
  equidad se elige junto al coste, no en lugar de él ([[umbrales-y-coste]]).

:::practica
enunciado: Un modelo sobre 200 personas. Grupo A: 100 personas, 40 aptas, de las que selecciona 32, y 12 falsas alarmas. Grupo B: 100 personas, 20 aptas, de las que selecciona 14, y 10 falsas alarmas. Calcula las tres métricas por grupo y di qué definiciones de equidad fallan.
pista: Exhaustividad es seleccionadas entre las aptas; falsas alarmas es seleccionados entre los no aptos; tasa de selección es todos los seleccionados entre el total del grupo.
solucion: Grupo A: exhaustividad 32/40 = 0,80; falsas alarmas 12/60 = 0,20; tasa de selección (32+12)/100 = 0,44. Grupo B: exhaustividad 14/20 = 0,70; falsas alarmas 10/80 = 0,125; tasa de selección (14+10)/100 = 0,24. Las brechas son 0,20 en selección, 0,10 en exhaustividad y 0,075 en falsas alarmas: fallan las tres definiciones a la vez. Es el caso peor, y el más habitual cuando el modelo se entrenó sin mirar los grupos.
:::

## Comprueba que lo sabes

:::quiz
p: El grupo A tiene prevalencia 30 % y el B 12 %, y el modelo acierta igual de bien en los dos. ¿Qué pasa con la paridad demográfica y con la igualdad de oportunidades?
o: Las dos se cumplen, porque el modelo es igual de bueno en los dos grupos
o: La igualdad de oportunidades se cumple y la paridad demográfica no, porque la tasa de selección arrastra la prevalencia
o: Ninguna de las dos se cumple, porque las prevalencias son distintas
a: 2
e: Si las curvas de acierto y de falsa alarma son las mismas, las tasas condicionadas al resultado real coinciden, y eso es exactamente la igualdad de oportunidades. La tasa de selección mezcla aciertos y falsas alarmas y hereda la prevalencia, así que el grupo con más positivos reales entra más: la paridad demográfica falla sin que nadie haya hecho nada mal.
:::

:::quiz
p: ¿Por qué no se pueden cumplir a la vez la calibración por grupos y la igualdad de odds cuando las prevalencias difieren?
o: Porque nunca hay datos suficientes para medir las dos cosas
o: Porque una puntuación calibrada en dos grupos con distinta prevalencia obliga a tasas de falsas alarmas distintas, y la igualdad de odds pide que sean iguales
o: Porque la calibración solo se puede medir en el grupo mayoritario
a: 2
e: Es un resultado matemático, demostrado por varios autores en 2016 de forma independiente: con prevalencias distintas y un modelo imperfecto, exigir calibración por grupos e igualdad de odds a la vez es imposible salvo en casos degenerados. No se arregla con más datos ni con un modelo mejor.
:::

:::quiz
p: Un equipo baja el umbral solo para el grupo B hasta que las dos tasas de selección coinciden. ¿Qué ha conseguido?
o: Cumplir la paridad demográfica a costa de romper la igualdad de oportunidades y subir las falsas alarmas del grupo B
o: Cumplir todas las definiciones de equidad a la vez
o: Nada, porque el umbral no cambia las tasas de selección
a: 1
e: Bajar el umbral en un grupo sube su tasa de selección y con ella su exhaustividad y sus falsas alarmas, así que la igualdad de odds se rompe por el otro lado. Y aparece un problema nuevo: dos personas idénticas reciben decisiones distintas según el grupo al que pertenecen.
:::

:::trampa
Un informe con la frase «el modelo no usa la variable protegida, así que es justo» no ha medido
nada. La variable se reconstruye con correlacionadas, y la disparidad aparece igual. La única prueba
de equidad es medir las métricas por grupo sobre datos que el modelo no haya visto, y decir cuál de
las definiciones estás cumpliendo y cuál estás sacrificando.
:::
