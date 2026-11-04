---
id: instruccion-y-alineamiento
titulo: Instrucción y alineamiento
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [preentrenamiento-y-escalado, fine-tuning-y-lora, funciones-de-perdida]
tags: [llm, alineamiento, rlhf, preferencias]
resumen: Como se pasa de un modelo que solo continua texto a un asistente que obedece: ajuste sobre instrucciones, modelos de recompensa, RLHF y DPO.
fuentes: ["Ouyang et al. (2022), 'Training language models to follow instructions with human feedback'", "Rafailov et al. (2023), 'Direct Preference Optimization: Your Language Model is Secretly a Reward Model'"]
---

## En una frase

Un modelo preentrenado solo continúa texto; el alineamiento lo convierte en asistente en dos
pasos: enseñarle con ejemplos cómo se responde a una instrucción (SFT) y ajustarlo con
preferencias humanas sobre pares de respuestas (RLHF o DPO).

## La idea

Un modelo recién preentrenado es un continuador de documentos. Si le escribes
«¿Cuál es la capital de Francia?» seguido de salto de línea, puede contestar «¿Y la de
Italia?», porque en su corpus las preguntas de un examen aparecen en listas, no aisladas con su
respuesta. No es que no sepa la respuesta: es que no ha aprendido **qué se espera de él** en esa
situación. La tarea que optimizó era predecir el token siguiente de un texto cualquiera, y
continuar con otra pregunta es una predicción perfectamente razonable.

El alineamiento es el conjunto de técnicas que cambian ese comportamiento. Tiene tres capas:

**1. Ajuste supervisado sobre instrucciones (SFT).** Se recopilan miles o decenas de miles de
pares (instrucción, respuesta correcta) escritos o revisados por personas, y se hace ajuste fino
con ellos. Un detalle técnico que se pasa por alto y es decisivo: **la pérdida se calcula solo
sobre los tokens de la respuesta**. Lo que se enseña aquí es el formato, el tono, la longitud y
la estructura de una buena respuesta, además de cómo comportarse ante peticiones ambiguas. Lo
que **no** se consigue de forma fiable es inyectar conocimiento nuevo: para hechos concretos
conviene recuperarlos del contexto ([[rag-arquitectura|RAG]]).

**2. Aprendizaje a partir de preferencias.** Escribir la respuesta ideal es caro y a menudo
imposible de consensuar, pero **comparar dos respuestas es fácil**: «¿cuál de estas dos es
mejor?». Con esos pares se puede construir una señal de calidad sin definir la respuesta
perfecta. Hay dos caminos:

- **RLHF** (aprendizaje por refuerzo con retroalimentación humana): primero se entrena un
  **modelo de recompensa** que puntúa respuestas a partir de las comparaciones; después se
  optimiza el modelo de lenguaje para maximizar esa recompensa, con una penalización que le
  impide alejarse demasiado del modelo de partida.
- **DPO** (optimización directa de preferencias): se salta el modelo de recompensa y se escribe
  una pérdida que trabaja directamente sobre los pares preferido/descartado. Es más simple de
  implementar y de ajustar, y por eso se ha extendido tanto en la práctica.

**3. Seguridad y política.** Reglas explícitas, ejemplos de rechazo, críticas generadas por
otro modelo (retroalimentación por IA, RLAIF) y revisión humana de casos límite. Aquí aparece la
tensión central del campo: cuanto más se insiste en no responder a peticiones peligrosas, más
aumentan los **rechazos excesivos** a peticiones legítimas.

Y el problema de fondo de todo lo anterior: **una preferencia no es una verdad**. Los
anotadores, con prisa y sin ser expertos en el tema, tienden a preferir respuestas largas, bien
estructuradas y con tono seguro. Si optimizas contra esa señal, el modelo aprende a ser largo,
estructurado y seguro, independientemente de si acierta. Ese fenómeno se llama **explotación de
la recompensa** (reward hacking) y sus síntomas más conocidos son la verbosidad, la
**sicofancia** (dar la razón al usuario aunque se equivoque) y la seguridad mal calibrada.

## Definición formal

**Pérdida del ajuste supervisado.** Sea `x` la instrucción (los tokens del enunciado) e
`y = (y₁ … y_R)` la respuesta. Con `R` tokens en la respuesta:

:::formula
L_SFT = −(1/R) · Σₜ₌₁ᴿ ln P(yₜ | x, y₁ … yₜ₋₁ ; θ)
:::

- `x` — tokens de la instrucción y del contexto.
- `yₜ` — el token `t` de la respuesta.
- `R` — número de tokens de la respuesta.
- `θ` — los parámetros que se ajustan.
- La suma **empieza en el primer token de la respuesta**, no en el primero de la instrucción. Si
  incluyes la instrucción en la pérdida, el modelo aprende a generar preguntas en vez de
  respuestas.

**Modelo de recompensa con preferencias (Bradley-Terry).** Con pares en los que `y_w` es la
respuesta preferida e `y_l` la descartada:

:::formula
P(y_w ≻ y_l | x) = σ( r(x, y_w) − r(x, y_l) )      σ(z) = 1 / (1 + e^(−z))
:::

- `r(x, y)` — la puntuación del modelo de recompensa para la respuesta `y` a la instrucción `x`.
- `σ` — la función logística, que convierte una diferencia de puntuaciones en una probabilidad
  entre 0 y 1.
- Si las dos respuestas reciben la misma puntuación, la probabilidad es 0,5: no hay preferencia.

**Objetivo de RLHF.** Se maximiza:

:::formula
E[ r(x, y) ] − β · KL( π_θ(y | x) ‖ π_ref(y | x) )
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `x` | La instrucción y su contexto: los tokens del enunciado | tokens | Alarga el prompt, no cambia el objetivo |
| `y` | La respuesta que genera el modelo que se está entrenando | tokens | Más tokens que puntuar: la recompensa se promedia sobre la secuencia |
| `R` | Tokens de la respuesta | tokens | Divide la suma de `L_SFT`: la pérdida es por token, no por respuesta |
| `r(x, y)` | Puntuación del modelo de recompensa | sin unidades, relativa | El objetivo sube, pero solo si el modelo no se aleja demasiado |
| `σ` | Función logística: convierte una diferencia en probabilidad | entre 0 y 1 | Con diferencias grandes se satura: la señal deja de crecer |
| `β` | Peso de la penalización por divergencia | adimensional | Más freno: el modelo aprende menos pero degenera menos. Con `β` pequeño se aleja mucho del lenguaje natural |
| `KL(· ‖ ·)` | Cuánto se ha separado el modelo entrenado del de referencia | neperios (nats), nunca negativa | El objetivo baja: es el precio que se paga por perseguir la recompensa |
| `π_θ` | El modelo que se entrena | distribución sobre tokens | Es lo único que cambia: `π_ref` está congelado |
| `y_w`, `y_l` | Respuesta preferida y descartada del par anotado | tokens | Importa la **diferencia** entre las dos, no el valor absoluto de cada una |
:::

- `E[·]` — esperanza sobre las respuestas `y` que genera el propio modelo que se está entrenando.
- `π_θ` — el modelo que se entrena; `π_ref` — el modelo de referencia (el de partida, congelado).
- `β` — el coeficiente de la penalización. Controla el intercambio entre obedecer a la
  recompensa y no degenerar: con `β` pequeño el modelo se aleja mucho del lenguaje natural; con
  `β` grande aprende poco.
- `KL(· ‖ ·)` — la divergencia de Kullback-Leibler, que mide cuánto se ha separado la
  distribución del modelo entrenado de la del modelo de referencia.

**Pérdida de DPO.** Con los log-ratios de cada respuesta respecto al modelo de referencia:

:::formula
L_DPO = − ln σ( β · [ (ln π_θ(y_w|x) − ln π_ref(y_w|x)) − (ln π_θ(y_l|x) − ln π_ref(y_l|x)) ] )
:::

- La expresión entre corchetes es el **margen**: cuánto ha subido la respuesta preferida menos
  cuánto ha subido la descartada, medido respecto al modelo base.
- La pérdida baja cuando el margen crece. Si la respuesta descartada sube más que la preferida,
  el margen se hace negativo y la pérdida crece.
- `β` cumple aquí un papel parecido al del RLHF: limita cuánto puede moverse el modelo respecto
  a la referencia.

:::figura
fichero: instruccion-dpo-y-freno-de-divergencia
pie: A la izquierda, la pérdida de DPO frente al margen. La curva es decreciente: cuanto más sube la respuesta preferida respecto a la descartada, menor es la pérdida. Los dos puntos marcan el caso del ejemplo, con margen +0,070 (pérdida 0,659) y con margen −0,070 (pérdida 0,729); en margen cero la pérdida vale siempre ln 2 ≈ 0,693, así que el modelo no gana nada por subir las dos respuestas a la vez. A la derecha, el freno de la divergencia: subir la recompensa de 1,2 a 1,8 pagando una KL de 20 deja el objetivo en 0,8, por debajo del 1,100 de partida. Ese es el mecanismo que evita que el modelo se aleje del lenguaje natural para exprimir la recompensa.
fuente: figuras/instruccion-y-alineamiento-1.py
:::

## Ejemplo

**Modelo de recompensa.** Con tres pares, aplicando `σ(r_w − r_l)`:

```
r ganadora +1.2  r perdedora +0.3  P(preferir) = 0.711
r ganadora +0.4  r perdedora +0.5  P(preferir) = 0.475
r ganadora +2.0  r perdedora -0.5  P(preferir) = 0.924
```

El segundo caso es el interesante: la respuesta marcada como preferida tiene **peor** puntuación
(0,4 frente a 0,5) y el modelo solo le da un 47,5 % de probabilidad de ser preferida. Eso no es
un error de la fórmula, es la señal que debe aprender: una preferencia humana concreta no tiene
por qué coincidir con la puntuación actual del modelo. El entrenamiento empuja `r` a subir en
las preferidas y bajar en las descartadas hasta que la probabilidad se acerque a 1.

**Penalización por divergencia.** Con recompensa 1,2, divergencia KL de 2,0 y `β = 0,05`, el
objetivo vale `1,2 − 0,05 · 2,0 = 1,100`. Es decir: de los 1,2 puntos de recompensa, 0,10 se
pagan por mantener el modelo cerca del original. Si el modelo encuentra una forma de subir la
recompensa a 1,8 a costa de una divergencia de 20, el objetivo se queda en 0,8: peor. Ahí está
el freno contra la explotación de la recompensa.

**Pérdida de DPO.** Con `β = 0,1` y log-ratios de +0,5 (preferida) y −0,2 (descartada):
margen 0,070 y pérdida 0,6588. Ahora mira los tres casos:

```
log-ratios (+0.5, -0.2)  margen +0.070  perdida 0.6588
log-ratios (+0.2, +0.9)  margen -0.070  perdida 0.7288
log-ratios (-0.3, -0.1)  margen -0.020  perdida 0.7032
```

En la segunda fila la respuesta descartada ha subido más que la preferida: margen negativo y
pérdida mayor. En la tercera las dos han bajado, pero la preferida ha bajado más: también
empeora. DPO no premia «subir mucho», premia **subir más la buena que la mala**.

## Código

```python verificable
import numpy as np

# Modelo de recompensa de Bradley-Terry: sigma(r_ganadora - r_perdedora)
sigma = lambda z: 1 / (1 + np.exp(-z))   # funcion logistica: lleva cualquier diferencia a [0, 1]

pares = [(1.2, 0.3), (0.4, 0.5), (2.0, -0.5)]
for rw, rl in pares:                     # desempaqueta cada tupla en las dos puntuaciones
    print(f"r ganadora {rw:+.1f}  r perdedora {rl:+.1f}  P(preferir) = {sigma(rw - rl):.3f}")
# -> 0.711, 0.475 y 0.924 en las tres lineas

# En RLHF el objetivo es recompensa menos una penalizacion por alejarse del modelo base
recompensa, kl, beta = 1.2, 2.0, 0.05
print(f"objetivo {recompensa - beta * kl:.3f}  (recompensa {recompensa} menos {beta * kl:.2f} de KL)")
# -> objetivo 1.100  (recompensa 1.2 menos 0.10 de KL)
```

:::claves
- `sigma` es una **función lambda**, no un método: se asigna a un nombre y se llama igual que cualquier función, pero no tiene `def` ni documentación. Si necesitas depurarla, cambia a `def` y pon un `print` dentro.
- `np.exp(-z)` con `z` muy grande no desborda hacia `nan` de forma silenciosa, pero con `z = -1000` el resultado es 0 y `sigma` devuelve exactamente 1,0: la fórmula se **satura** y deja de distinguir entre diferencias de 50 y de 1000. Por eso un modelo de recompensa con puntuaciones muy dispares apenas recibe señal.
- `rw - rl` usa las puntuaciones **relativas**: sumar 10 a las dos no cambia nada. Si entrenaras con puntuaciones absolutas en vez de con pares, el modelo aprendería a inflar todas por igual.
- `(1.2, 0.3)` es una **tupla**, no una lista: no se puede modificar después. `for rw, rl in pares` la desempaqueta en dos variables; si la tupla tuviera tres elementos, el bucle fallaría con `ValueError`.
- `{rw:+.1f}` imprime el signo **siempre** (`+1.2`, `-0.5`), que aquí es lo que hace legible la tabla. Sin el `+` se pierde la pista de si la puntuación era positiva o negativa.
- En el segundo bloque, `margen = beta * (log_ratio_w - log_ratio_l)` deja fuera los logaritmos porque ya vienen calculados como **log-ratios** (diferencia de log-probabilidades). Si le pasaras probabilidades en crudo, el resultado no tendría nada que ver.
- `-np.log(sigma(margen))` es la pérdida: como `sigma` está entre 0 y 1, su logaritmo es negativo y el signo menos lo hace positivo. Si `margen` se hiciera muy negativo, `sigma` tiende a 0 y la pérdida crece sin límite: el modelo paga caro empeorar la respuesta preferida.
:::

```python verificable
import numpy as np

# Perdida DPO: -ln sigma(beta * [(ln pi_w - ln ref_w) - (ln pi_l - ln ref_l)])
sigma = lambda z: 1 / (1 + np.exp(-z))

beta = 0.1
log_ratio_w, log_ratio_l = 0.5, -0.2        # cuanto ha subido cada respuesta respecto al modelo base

margen = beta * (log_ratio_w - log_ratio_l)   # margen ya escalado por beta, como en la formula
print(f"margen {margen:+.3f}  perdida {-np.log(sigma(margen)):.4f}")   # -> margen +0.070  perdida 0.6588

# Si la respuesta peor sube mas que la buena, el margen se vuelve negativo y la perdida crece
for lw, ll in [(0.5, -0.2), (0.2, 0.9), (-0.3, -0.1)]:
    m = beta * (lw - ll)      # el mismo calculo que arriba, con los tres pares del ejemplo
    print(f"log-ratios ({lw:+.1f}, {ll:+.1f})  margen {m:+.3f}  perdida {-np.log(sigma(m)):.4f}")
# -> margenes +0.070, -0.070 y -0.020 con perdidas 0.6588, 0.7288 y 0.7032
```

## Errores típicos

- **Esperar que el SFT inyecte conocimiento factual.** El ajuste sobre instrucciones cambia el
  comportamiento (formato, tono, seguimiento de la tarea); para hechos concretos y cambiantes,
  el camino es dárselos en el contexto o hacer ajuste fino de dominio con datos suficientes. Con
  pocos ejemplos, lo que consigues es que el modelo invente con más seguridad.
- **Calcular la pérdida también sobre los tokens de la instrucción.** El modelo aprende a
  generar preguntas parecidas a las del conjunto de entrenamiento en lugar de respuestas. Hay
  que enmascarar la instrucción y promediar solo sobre la respuesta.
- **Premiar la longitud y el tono seguro.** Los anotadores prefieren respuestas largas y
  estructuradas; si optimizas esa señal sin corregirla, obtienes un modelo verboso y sicofante
  que da la razón al usuario. Se mitiga con instrucciones explícitas de anotación, control de
  longitud y datos de preferencia donde la respuesta corta y correcta gane a la larga y hueca.
- **Olvidar la penalización por divergencia.** Sin ella, el modelo se aleja del lenguaje
  natural y de todo lo aprendido para exprimir la recompensa: aparecen respuestas repetitivas,
  listas interminables o texto degenerado con puntuación altísima.
- **Evaluar con el mismo juez con el que entrenaste.** Si usas el modelo de recompensa (o un
  juez automático) para medir, estás midiendo lo que ese modelo prefiere, no lo que es correcto.
  La evaluación de un modelo alineado necesita datos reservados y revisión humana, además de
  [[evaluacion-de-llms|jueces independientes]] contrastados.
- **Sobreentrenar la capa de seguridad.** Un modelo que rechaza peticiones legítimas es tan
  inútil como uno que responde a todo. Mide por separado falsos positivos y falsos negativos del
  rechazo, y revisa los casos límite con personas del dominio.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un modelo base no responde bien a una pregunta directa?
o: Porque no tiene suficientes parámetros para recordar la respuesta
o: Porque solo aprendió a continuar texto: responder a una instrucción aislada no es la tarea que optimizó
o: Porque le falta una base de datos de hechos
a: 2
e: El preentrenamiento optimiza la predicción del siguiente token sobre documentos. Continuar una pregunta con otra pregunta es una predicción razonable en ese contexto. El SFT le enseña el formato y el comportamiento esperados, no le añade un almacén de hechos.
:::

:::quiz
p: En la pérdida del ajuste supervisado, ¿sobre qué tokens se calcula?
o: Sobre todos los tokens de la secuencia, instrucción incluida
o: Solo sobre los tokens de la respuesta
o: Solo sobre el último token de la respuesta
a: 2
e: Si incluyes la instrucción, el modelo aprende a producir instrucciones parecidas. La pérdida se calcula sobre la respuesta (a veces solo sobre partes concretas de ella) y se promedia por el número de tokens de esa respuesta.
:::

:::quiz
p: ¿Para qué sirve la penalización KL en el objetivo de RLHF?
o: Para que el modelo no se aleje demasiado del modelo de referencia mientras persigue la recompensa
o: Para acelerar el entrenamiento del modelo de recompensa
o: Para garantizar que las respuestas sean más cortas
a: 1
e: La recompensa es una aproximación imperfecta de lo que queremos. Sin freno, el modelo encuentra el punto donde la recompensa es máxima aunque el texto sea degenerado. La divergencia KL contra el modelo de referencia limita cuánto puede moverse la distribución, con `beta` como mando del intercambio.
:::

:::aviso
Preferencia no es corrección. Un conjunto de preferencias recoge lo que un grupo de personas, en
unas condiciones concretas, eligió entre dos opciones. Si en tu caso de uso lo que importa es la
exactitud factual, mide exactitud factual: entrena y evalúa con eso, aunque sea más caro de
anotar.
:::
