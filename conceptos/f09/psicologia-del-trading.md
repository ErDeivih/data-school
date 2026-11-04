---
id: psicologia-del-trading
titulo: Psicología del trading
fase: 9
nivel: básico
rutas: [quant]
prerequisitos: [valor-esperado, maximo-drawdown]
tags: [disciplina, sesgos, rachas, proceso]
resumen: Por qué una racha de siete pérdidas no significa que el sistema esté roto: plan escrito, un tamaño que aguante y juzgar decisiones en vez de resultados.
fuentes: ["Kahneman (2011), 'Thinking, Fast and Slow'", "Duke (2018), 'Thinking in Bets'", "Douglas (2000), 'Trading in the Zone'"]
---

## En una frase

La parte psicológica del trading no consiste en aguantar mejor las pérdidas, sino en tener un plan
escrito antes de operar, un tamaño de posición que sobreviva a las rachas que van a llegar y la
costumbre de evaluar tus decisiones por el proceso y no por lo que pasó después.

## La idea

Un sistema que gana el 45 % de las veces es un sistema perfectamente normal. Con ese sistema,
en 200 operaciones, la probabilidad de que aparezca **al menos una racha de 5 pérdidas seguidas
es del 99,4 %**; la de una racha de 7 es del 75,6 %, y hay casi un 20 % de probabilidad de
encadenar 10. Si haces 1.000 operaciones, la probabilidad de ver 10 pérdidas seguidas sube al
68,2 %. Es decir: la racha que te va a hacer dudar de todo no es un fallo del sistema ni una
señal de que el mercado ha cambiado. Es la forma que tiene el azar de repartirse, y estaba en el
guion desde el primer día.

Ahí empieza el problema real. La racha de siete pérdidas llega, y la reacción natural es una de
estas dos: cambiar el sistema (justo cuando no hay evidencia de que esté roto, porque la muestra
es demasiado corta para distinguir «roto» de «mala racha»), o subir el tamaño para recuperar lo
perdido. La segunda es la que arruina cuentas. Diez pérdidas seguidas con riesgo fijo de 1R
cuestan 10R; las mismas diez pérdidas duplicando el tamaño después de la tercera cuestan **257R**.
Con una esperanza de 0,35R por operación, 257R es más de lo que ese sistema gana en 700
operaciones.

Hay dos sesgos que explican casi todo lo demás. El primero es la **aversión a la pérdida**: una
pérdida duele más de lo que satisface una ganancia del mismo tamaño, y de ahí salen cerrar las
ganadoras demasiado pronto, aguantar las perdedoras, mover el stop y operar de más para recuperar.
El segundo es juzgar las decisiones por el resultado: una decisión correcta puede perder y una
mala puede ganar, así que aprender de esa casualidad es aprender lo contrario de lo que conviene.
Los angloparlantes lo llaman *resulting*.

Lo que funciona no es motivación, son reglas que no dependan del ánimo: escribir el plan antes de
la sesión (qué opera, cuándo entra, cuándo sale, cuánto arriesga y qué pasa si pierde tres
seguidas), medir en R y no en euros, anotar en un registro **si cumpliste el plan** —eso es lo que
controlas— y poner un límite de pérdida diaria que apague la sesión. Y una idea que ordena todo:
el sistema importa más que la idea. Una idea sin tamaño ni reglas de salida no es operable, y una
idea mediocre con buen control de riesgo sigue viva el tiempo suficiente para mejorarla.

## Definición formal

- **R** — la unidad de riesgo de una operación: lo que pierdes si la operación sale mal. Todo se
  mide en múltiplos de R, no en euros, para que las operaciones sean comparables entre sí y para
  que el tamaño no distorsione el análisis.
- **p** — proporción de operaciones ganadoras. **G** — ganancia media de una operación ganadora,
  en R. **P** — pérdida media de una operación perdedora, en R (habitualmente 1).
- **Esperanza (o expectativa) por operación:** `E = p · G − (1 − p) · P`. Es el
  [[valor-esperado]]: lo que ganas de media por operación si repites el sistema. Con `p = 0,45`,
  `G = 2` y `P = 1`: `E = 0,45 · 2 − 0,55 · 1 = 0,35R`.
- **Racha** — `k` pérdidas consecutivas. La probabilidad de que aparezca al menos una racha de
  longitud `k` en `n` operaciones se calcula con una recurrencia sobre el estado «racha actual» y
  «ya ha aparecido»; no depende de la estrategia, solo de `p` y de `n`.
- **Resultado esperado de `n` operaciones:** `n · E`. Con `n = 200` y `E = 0,35R`: `70R`. Es una
  media, no una promesa: la dispersión alrededor de ese número es grande y hace falta una muestra
  larga para distinguir una esperanza positiva de cero (es la [[ley-de-los-grandes-numeros]]).
- **Drawdown** — la caída desde el máximo de la curva de resultados, medida en R. Lo que aguantas
  psicológicamente no es el resultado final, es la profundidad y la duración de esa caída; ver
  [[maximo-drawdown]].
- **Plan de trading** — conjunto de reglas escritas antes de operar, con estos campos: mercado,
  horario, condición de entrada, condición de salida, riesgo por operación, máximo de pérdidas al
  día y qué hacer tras una racha de pérdidas. Sin tamaño de posición, no es un plan: es una
  opinión.
- **Tilt** (o «calentón») — estado en el que se opera para recuperar lo perdido en vez de ejecutar
  el plan. Se detecta por señales concretas: subir el tamaño, saltarse la entrada escrita, no
  cerrar la plataforma.

:::figura
fichero: psicologia-rachas-y-doblar
pie: A la izquierda, la probabilidad de que aparezca al menos una racha de k pérdidas seguidas con un sistema que pierde el 55 % de las veces. Con 200 operaciones (azul), el 76 % de las series contiene una racha de 7: no es un sistema roto, es lo que cabe esperar. Con 1.000 operaciones (morado), dos de cada tres series encadenan 10 pérdidas. A la derecha, lo que cuesta esa misma racha: con riesgo fijo de 1R, diez pérdidas son 10R (la línea que sube despacio); duplicando el tamaño a partir de la cuarta, la misma racha cuesta 257R, por encima de los 70R que el sistema espera ganar en todo el año.
fuente: figuras/psicologia-del-trading-1.py
:::

## Ejemplo

Sistema con un 45 % de aciertos, ganancia de 2R y pérdida de 1R. En 200 operaciones se esperan
90 ganadoras y 110 perdedoras, con un resultado esperado de 200 · 0,35 = **70R**.

- Una racha de 5 pérdidas seguidas no basta para cubrir el resultado: son 5R, el 7 % de los 70R.
  La probabilidad de que ocurra en 200 operaciones es del 99,4 %.
- Una racha de 10 pérdidas son 10R, el 14 % del resultado esperado, y aparece con probabilidad
  del 19,9 % en 200 operaciones y del 68,2 % en 1.000.
- Si en esa racha de 10 hubieras duplicado el tamaño a partir de la cuarta pérdida, el coste
  habría sido de 257R, tres veces y media el resultado esperado de todo el año.

La conclusión no es «ignora las pérdidas»: ver 10 pérdidas seguidas no te dice nada del sistema,
mientras que subir el tamaño tras perder tres dice mucho sobre tu probabilidad de arruinarte
([[riesgo-de-ruina]]).

## Código

```python verificable
# Probabilidad de al menos una racha de k perdidas en n operaciones.
def prob_racha(n, k, p_perder):
    estados = {(0, False): 1.0}          # (racha actual, ya ha aparecido una racha de k)
    for _ in range(n):
        nuevo = {}
        for (racha, hubo), prob in estados.items():
            for pierde, p in ((True, p_perder), (False, 1 - p_perder)):
                nr = racha + 1 if pierde else 0
                clave = (min(nr, k), hubo or nr >= k)
                nuevo[clave] = nuevo.get(clave, 0.0) + prob * p
        estados = nuevo
    return sum(pr for (r, h), pr in estados.items() if h)

for k in (5, 7, 10, 12):
    print(f"racha de {k:>2} perdidas en 200 ops: {prob_racha(200, k, 0.55):>6.1%}   "
          f"en 1000 ops: {prob_racha(1000, k, 0.55):>6.1%}")
```

:::claves
- El diccionario `estados` guarda probabilidades que **suman 1** en todo momento. Lo que se acumula en el estado «ya apareció» no vuelve a salir nunca: si al mover las probabilidades de un paso al siguiente esa masa se reparte también hacia atrás, los números se salen de 1 sin que Python se queje (no hay ninguna comprobación de que sea una probabilidad).
- `clave = (min(nr, k), hubo or nr >= k)`: el `min` es lo que hace que la racha larga se quede en `k`. Sin él, el diccionario crecería con rachas de cualquier longitud y el cálculo sería más lento sin cambiar el resultado.
- El formato `.1%` imprime `99.4%` para 0,994 y `19.9%` para 0,199. Cuidado al copiar esos números a la prosa del portal, donde se escriben «99,4 %» y «19,9 %»: la coma y el espacio son cosa del texto, no del código.
- `p_perder` es la probabilidad de **perder** (0,55), no la de acertar (0,45). Cambiar una por otra da una serie de rachas mucho más corta y el resultado sigue pareciendo razonable: es el error silencioso más caro de este bloque.
- `sum(pierde * 2 ** i for i in range(1, 8))` construye la escalera 2 + 4 + … + 128 = 254 y, sumados los 3R de las tres primeras, da 257R. Si el rango fuera `range(1, 7)` te dejarías la última pérdida y el número saldría más pequeño sin avisar.
:::

```python verificable
# La esperanza y el coste de una racha, todo en unidades de R.
p, gana, pierde = 0.45, 2.0, 1.0
esperanza = p * gana - (1 - p) * pierde
print("esperanza por operacion:", round(esperanza, 2), "R")     # -> esperanza por operacion: 0.35 R
print("en 200 operaciones:", round(200 * esperanza, 1), "R")    # -> en 200 operaciones: 70.0 R
print("diez perdidas seguidas:", 10 * pierde, "R")              # -> diez perdidas seguidas: 10.0 R
doblada = 3 * pierde + sum(pierde * 2 ** i for i in range(1, 8))   # duplicar tras la tercera
print("la misma racha doblando el tamano:", doblada, "R")       # -> la misma racha doblando el tamano: 257.0 R
```

```text
Plantilla de diario de operaciones (una fila por operacion):

fecha | hora | mercado | entrada | salida | R obtenido | segui el plan | nota
------+------+---------+---------+--------+------------+---------------+------
      |      |         |         |        |            | si/no         |

Lo que se revisa cada semana no es el R total, son las columnas de la derecha:
cuantas operaciones se saltaron el plan y que estaban haciendo mal esas entradas.
```

## Errores típicos

- **Cambiar el sistema después de una racha de pérdidas.** Con un 45 % de aciertos, una racha de
  7 pérdidas es lo esperable en tres de cada cuatro series de 200 operaciones. Cambiar el sistema
  ahí es reaccionar al ruido: para saber si está roto hacen falta datos, no dolor.
- **Subir el tamaño para recuperar.** Ya has visto el número: 257R en lugar de 10R en la misma
  racha. Es la forma más rápida de convertir una racha normal en el final de la cuenta, y suele
  ir acompañada de saltarse las entradas escritas.
- **Juzgar la decisión por el resultado.** Una entrada perfecta puede perder y una mala puede
  ganar. Si refuerzas lo que hiciste solo porque salió bien, acabarás copiando tus errores.
  Evalúa dos cosas por separado: cumplimiento del plan y resultado.
- **Mover el stop o no cerrar la pérdida.** Es la aversión a la pérdida en acción: la pérdida
  flotante no duele igual que la realizada, aunque sea la misma pérdida. El stop se decide antes
  de entrar y no se toca, salvo para reducirlo.
- **Llevar la cuenta en euros.** En euros, cada operación parece distinta y no puedes comparar
  nada. En R, todas las operaciones son comparables, puedes medir tu esperanza y ves si el tamaño
  que usas es coherente con el resto del sistema.
- **Improvisar el tamaño en el momento.** Si el riesgo por operación no está escrito antes de la
  sesión, lo decidirá tu estado de ánimo, y tu estado de ánimo después de dos pérdidas no es el
  mismo que después de dos ganancias. El tamaño se decide en frío.

:::practica
enunciado: Un sistema acierta el 40 %, gana 2,5R por ganadora y pierde 1R. Calcula la esperanza por operación y el resultado esperado en 250 operaciones. Compara después el coste de una racha de 6 pérdidas con riesgo fijo de 1R y duplicando el tamaño desde la cuarta.
pista: La esperanza es p · G − (1 − p) · P; en la racha doblada, las tres primeras cuestan 1R y luego 2R, 4R y 8R.
solucion: E = 0,40 · 2,5 − 0,60 · 1 = 0,40R; en 250 operaciones, 100R. Con riesgo fijo, 6 pérdidas cuestan 6R, el 6 % del esperado. Duplicando desde la cuarta: 1 + 1 + 1 + 2 + 4 + 8 = 17R, casi el triple. Conclusión: la racha es normal y no dice nada del sistema; doblar el tamaño sí cambia el daño.
:::

## Comprueba que lo sabes

:::quiz
p: Un sistema gana el 45 % de las veces. ¿Qué significa que en 200 operaciones la probabilidad de una racha de 7 pérdidas sea del 75,6 %?
o: Que el sistema tiene un problema y hay que revisarlo
o: Que una racha de 7 pérdidas es un resultado esperable y no demuestra por sí sola que el sistema esté roto
o: Que la esperanza del sistema es negativa
a: 2
e: La racha es una propiedad de la secuencia de aciertos y fallos, no de la calidad de la estrategia: con un 45 % de aciertos y 200 operaciones, tres de cada cuatro series contienen una racha de 7. La esperanza puede ser perfectamente positiva (0,35R en el ejemplo) y la racha aparecer igual.
:::

:::quiz
p: ¿Por qué se mide el resultado en R y no en euros?
o: Porque en R no se pagan impuestos
o: Porque así todas las operaciones son comparables y el tamaño no distorsiona el análisis de la esperanza
o: Porque el bróker calcula las pérdidas en R y no en euros
a: 2
e: R es lo que arriesgas en cada operación, así que expresar el resultado en múltiplos de R permite comparar operaciones de tamaños distintos, sumar la esperanza y detectar si el tamaño usado es coherente. Sin eso, dos operaciones con cifras parecidas pueden estar arriesgando cantidades muy distintas.
:::

:::quiz
p: Después de tres pérdidas seguidas decides doblar el tamaño para recuperar. ¿Cuál es el problema aritmético?
o: Que la comisión se duplica, que es un coste asumible
o: Que si la racha continúa el coste crece exponencialmente: una racha de 10 pérdidas pasa de costar 10R a 257R
o: Ninguno, porque el sistema tiene esperanza positiva y antes o después recupera
a: 2
e: Doblar el tamaño después de cada pérdida convierte una racha en una progresión geométrica. Con 1R fijo, 10 pérdidas cuestan 10R; duplicando a partir de la cuarta, cuestan 257R, más de lo que el sistema gana en 700 operaciones. Que la esperanza sea positiva no protege de quedarse sin cuenta antes de que llegue.
:::

:::truco
Escribe el plan antes de abrir la plataforma y no lo cambies con la sesión en marcha: qué vas a
operar, cuándo entras, cuándo sales, cuánto arriesgas y qué haces tras tres pérdidas seguidas.
Y pon por escrito el máximo de pérdida diaria: cerrar la plataforma un mal día no es rendirse, es
la única regla que evita que un calentón se convierta en una cuenta cerrada.
:::
