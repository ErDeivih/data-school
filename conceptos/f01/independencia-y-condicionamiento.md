---
id: independencia-y-condicionamiento
titulo: Independencia y condicionamiento
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [probabilidad-condicional, probabilidad-axiomas]
tags: [probabilidad, independencia, collider, causalidad]
resumen: Independencia, independencia condicional y la paradoja de Berkson: por qué dos variables sin relación pueden parecer asociadas al condicionar en una tercera.
fuentes: ["Pearl (2009), 'Causality: Models, Reasoning and Inference'", "Ross (2014), 'A First Course in Probability'"]
---

## En una frase

Dos sucesos son independientes si saber uno no cambia la probabilidad del otro, pero eso no
significa que sigan siendo independientes cuando condicionas en un tercer suceso: la
independencia condicional es una propiedad distinta y más frágil, y confundirlas produce
asociaciones que existen en los datos y no en el mundo.

## La idea

Independencia es la intuición más limpia de la probabilidad: lanzas una moneda y un dado, y lo
que salga en uno no te dice nada del otro. Formalmente, `P(A ∩ B) = P(A)·P(B)`, o lo que es lo
mismo, `P(A | B) = P(A)`: condicionar a `B` no mueve la probabilidad de `A`. Cuando esto falla,
la información fluye.

El problema es que la independencia **no es heredable**. Hay dos formas de romperla al
condicionar, y las dos aparecen constantemente en análisis de datos reales.

La primera es la del **confusor**: dos variables parecen relacionadas porque ambas dependen de
una tercera. El consumo de helado y los ahogamientos en la playa suben juntos, pero no porque
uno cause el otro: los dos suben con la temperatura. Si condicionas en la temperatura, la
asociación desaparece. Aquí condicionar **arregla** el problema.

La segunda es la contraria y mucho más traicionera: el **collider** o colisionador. Dos variables
que eran independientes pasan a estar asociadas **al condicionar** en un efecto común. Es la
paradoja de Berkson: en un hospital, la enfermedad A y la enfermedad B pueden parecer
relacionadas negativamente porque condicionas en «estar hospitalizado», que es consecuencia de
cualquiera de las dos. Si solo entran al hospital los enfermos graves, entre los hospitalizados
escasea la gente con las dos enfermedades y parece que una protege de la otra. La asociación es
real en la muestra y no existe en la población.

Esto tiene una consecuencia práctica enorme: **no se controla por todo lo que se tiene a mano**.
Meter una variable que es consecuencia del efecto (una variable posterior al tratamiento, un
resultado intermedio) crea asociaciones espurias. Pero se sigue haciendo, y suele ser el motivo
de que un análisis con «muchos controles» dé resultados que no se replican.

## Definición formal

Dos sucesos `A` y `B` con probabilidades positivas son **independientes** si:

:::formula
P(A ∩ B) = P(A) · P(B)     equivalente a     P(A | B) = P(A)
:::

- `A ∩ B` — ocurren los dos a la vez; `P(A | B)` — probabilidad de `A` sabiendo que ocurrió `B`.
- La equivalencia exige `P(B) > 0`; si `P(B) = 0` la segunda forma no está definida.

`A` y `B` son **condicionalmente independientes dado `C`** (se escribe `A ⫫ B | C`) si:

:::formula
P(A ∩ B | C) = P(A | C) · P(B | C)     para todo C con P(C) > 0
:::

- `C` — el suceso en el que condicionas; puede romper o crear la independencia.
- `⫫` — símbolo de independencia; `A ⫫ B | C` se lee «A es independiente de B dado C».

Las dos propiedades son **independientes entre sí**: hay parejas independientes que dejan de
serlo al condicionar (collider) y parejas dependientes que se vuelven independientes al
condicionar (confusor). Ninguna implica la otra.

:::parametros
| Simbolo | Que es | Unidades | Que le pasa al condicionar |
| --- | --- | --- | --- |
| `A`, `B` | Los dos sucesos cuya relación estudias | ninguna | Es lo que se mueve: pueden empezar siendo independientes y dejar de serlo |
| `A ∩ B` | Ocurren los dos a la vez | ninguna | Su probabilidad se divide entre `P(C)` al condicionar; si `C` es raro, el cociente se dispara |
| `P(A / B)` | Probabilidad de `A` sabiendo que ocurrio `B` | probabilidad, entre 0 y 1 | Igual a `P(A)` es la definición de independencia. Con `P(B) = 0` la expresión no esta definida y no se puede usar |
| `C` | El suceso en el que condicionas | ninguna | Confusor: puede hacer desaparecer una asociación real. Colisionador: puede crear una que no existe. Elegirlo mal es el error de fondo |
| `P(A / C)`, `P(B / C)` | Las dos condicionales por separado | probabilidad, entre 0 y 1 | Su producto es lo que hay que comparar con `P(A ∩ B / C)`; que cada una sea razonable no dice nada de la conjunta |
| `A independiente de B dado C` | Independencia condicional: la conjunta factoriza dentro de cada estrato | ninguna | Se decide antes de mirar los datos, con el grafo causal. Mirando la tabla solo se comprueba, y con muchos estratos siempre se encuentra algo |
| `r` de Pearson | Correlación lineal entre dos variables | adimensional, entre -1 y 1 | Vale 0 tanto si son independientes como si la relación es simetrica y no lineal. Un cero no demuestra nada por si solo |
:::

**Extensión a variables aleatorias.** Para variables, `X ⫫ Y` significa que su función de
distribución conjunta factoriza: `F(x, y) = F_X(x)·F_Y(y)`. De ahí se deduce que
`Cov(X, Y) = 0` y `Corr(X, Y) = 0`. **El recíproco es falso**: correlación cero no implica
independencia, porque la correlación solo detecta relación lineal. Un ejemplo clásico es
`X` uniforme en `{−1, 0, 1}` e `Y = X²`: son dependientes (`Y` está determinado por `X`) y su
correlación es cero.

:::figura
fichero: independencia-condicionar-cambia-la-relacion
pie: Los tres paneles usan los mismos datos generados. En el primero, helados y ahogamientos parecen ir juntos; en el segundo, al mirar dentro de cada grupo de temperatura, la relación casi desaparece: la asociación venia del confusor. En el tercero pasa lo contrario, dos enfermedades independientes (r cerca de cero) muestran r = -0,89 entre los ingresados solo por haber condicionado en un efecto comun. Compara los dos ultimos paneles antes de decidir que variables controlar.
fuente: figuras/independencia-y-condicionamiento-1.py
:::

## Ejemplo

**Independencia.** Lanzas una moneda y un dado, 120 veces. Con 60 caras y 60 cruces, y cada cara
del dado 20 veces repartidas a partes iguales entre cara y cruz:

```
                 cara   cruz   total
sale 6            10     10      20
no sale 6         50     50     100
total             60     60     120
```

- `P(6) = 20/120 = 1/6`.
- `P(cara) = 60/120 = 1/2`.
- `P(6 y cara) = 10/120 = 1/12 = (1/6)·(1/2)`. Independientes.
- `P(6 | cara) = 10/60 = 1/6 = P(6)`. Condicionar no mueve nada.

**Independencia condicional.** Tres sucesos con partición equiprobable de 8 casos:
`A` = el primer bit es 1, `B` = el segundo bit es 1, `C` = los dos bits son iguales (es decir,
`C` es verdadero si `A = B`).

- `P(A) = 4/8 = 0,5`, `P(B) = 0,5`, `P(A ∩ B) = 2/8 = 0,25 = 0,5·0,5`. `A` y `B` son
  independientes.
- `P(A | C) = 1/2` y `P(B | C) = 1/2`, pero `P(A ∩ B | C) = P(A = B = 1) / P(C) = (1/4)/(1/2) = 0,5`.
- Como `0,5 ≠ 0,5 · 0,5 = 0,25`, `A` y `B` **no** son condicionalmente independientes dado `C`.
  Saber que el primer bit es 1 y que los dos son iguales te dice que el segundo también: la
  información fluye a través del colisionador `C`.

**Paradoja de Berkson, con números.** Dos enfermedades independientes en la población, cada una
con `P(A) = P(B) = 0,10`, y un criterio de ingreso hospitalario que es «tener A o tener B»
(probabilidad de ingreso condicional del 100 % en esos casos y 0 en el resto).

- En la población, `P(A ∩ B) = 0,10 · 0,10 = 0,01` y `P(A | B) = 0,10`.
- `P(ingreso) = 1 − 0,90 · 0,90 = 0,19`.
- Entre los ingresados, `P(A ∩ B | ingreso) = 0,01 / 0,19 = 0,0526`, mientras que
  `P(A | ingreso) · P(B | ingreso) = (0,10/0,19) · (0,10/0,19) = 0,5263 · 0,5263 = 0,277`. Como
  `0,0526 ≠ 0,277`, las dos enfermedades **dejan de ser independientes** en la muestra del
  hospital.
- Y en la dirección que despista: `P(A | B, ingreso) = 0,10` frente a `P(A | ingreso) = 0,5263`.
  Entre los ingresados, tener la enfermedad B reduce la frecuencia de A. La asociación negativa
  es un artefacto de haber condicionado en un efecto común.

## Código

```python verificable
# Grid 2 x 2 x 2 determinista: A = primer bit, B = segundo bit, C = "los bits son iguales".
casos = [(a, b) for a in (0, 1) for b in (0, 1)]      # 4 combinaciones equiprobables
n = len(casos)

P = lambda pred: sum(1 for c in casos if pred(*c)) / n

p_a = P(lambda a, b: a == 1)
p_b = P(lambda a, b: b == 1)
p_ab = P(lambda a, b: a == 1 and b == 1)
p_c = P(lambda a, b: a == b)
p_ab_c = P(lambda a, b: a == 1 and b == 1 and a == b) / p_c
p_a_c = P(lambda a, b: a == 1 and a == b) / p_c
p_b_c = P(lambda a, b: b == 1 and a == b) / p_c

print("P(A)             ", p_a)                # salida: 0.5
print("P(A y B)         ", p_ab)               # salida: 0.25
print("P(A)*P(B)        ", p_a * p_b)          # salida: 0.25  -> independientes
print("P(A y B dado C)  ", p_ab_c)             # salida: 0.5
print("P(A|C)*P(B|C)    ", p_a_c * p_b_c)      # salida: 0.25  -> no cond. independientes
```
:::claves
- `P = lambda pred: sum(1 for c in casos if pred(*c)) / n` no estima ninguna probabilidad: cuenta casos y divide. La parte que enganna es `pred(*c)`, que desempaqueta cada pareja `(a, b)` en los dos argumentos de la lambda. Si cambiaras `casos` por tuplas de tres elementos, esa misma línea seguiria funcionando y las lambdas de abajo no.
- `pred(*c)` dentro de un generador devuelve lo que devuelva el predicado. Aqui son comparaciones (`a == 1`), que dan `True` o `False`, y `sum` los cuenta como 1 y 0 porque en Python `bool` es una subclase de `int`. Ese detalle es el que permite escribir la cuenta sin un `if`.
- Cuidado con `and` en esos predicados: no devuelve `True` ni `False`, devuelve el ultimo operando evaluado. Funciona porque se usa dentro de un `if`, pero `x = a == 1 and b == 1` puede guardar `False` en vez del valor que esperas si lo encadenas con números.
- `p_c` se calcula una vez y se reutiliza como denominador en las tres líneas siguientes. Si se recalculara en cada línea con otra condición, los tres números dejarian de ser comparables y la conclusión de que no hay independencia condicional sería casualidad.
- En el bloque de NumPy, `np.corrcoef(X, Y)` devuelve una **matriz 2x2**, no un número: `[0, 1]` y `[1, 0]` son la correlación (la matriz es simetrica) y `[0, 0]` y `[1, 1]` valen 1 siempre. Casi todos los errores con esta función son un índice mal puesto.
- `np.mean((X - X.mean()) * (Y - Y.mean()))` es la covarianza con divisor `n`, mientras que `np.cov` usa `n - 1` por defecto. Con estos tres puntos, `X` e `Y` simetricos, las dos dan 0; con datos reales darian números distintos y el de `np.cov` sería el de la muestra.
- `itertools.product([0, 1], [0, 1])` genera las cuatro combinaciones en orden: `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`. El orden importa si luego indexas la lista por posición en vez de buscar por valor.
:::


```python verificable
import numpy as np

# Correlacion cero NO implica independencia: Y = X^2 con X simetrica.
X = np.array([-1.0, 0.0, 1.0])
Y = X**2

cov = float(np.mean((X - X.mean()) * (Y - Y.mean())))
corr = float(np.corrcoef(X, Y)[0, 1])

print("X            ", X.tolist())              # salida: [-1.0, 0.0, 1.0]
print("Y = X^2      ", Y.tolist())              # salida: [1.0, 0.0, 1.0]
print("covarianza   ", round(cov, 4))           # salida: 0.0
print("correlacion  ", round(corr, 4))          # salida: 0.0
print("pero Y depende de X:", bool(np.allclose(Y, X**2)))  # salida: True
```

```python verificable
import itertools

# Paradoja de Berkson: dos enfermedades independientes que dejan de serlo al condicionar
# en el ingreso, que es consecuencia de cualquiera de las dos.
p_enfermedad = 0.10
filas = []
for a, b in itertools.product([0, 1], [0, 1]):
    p = (p_enfermedad if a else 1 - p_enfermedad) * (p_enfermedad if b else 1 - p_enfermedad)
    filas.append((a, b, p))                  # (tiene A, tiene B, probabilidad conjunta)

p_ingreso = sum(p for a, b, p in filas if a or b)
p_a_dado_ingreso = sum(p for a, b, p in filas if a) / p_ingreso
p_ab_dado_ingreso = sum(p for a, b, p in filas if a and b) / p_ingreso

print("P(ingreso)        ", round(p_ingreso, 4))                 # salida: 0.19
print("P(A y B | ingreso)", round(p_ab_dado_ingreso, 4))        # salida: 0.0526
print("P(A|ing)*P(B|ing)", round(p_a_dado_ingreso**2, 4))       # salida: 0.277
print("son independientes:", bool(abs(p_ab_dado_ingreso - p_a_dado_ingreso**2) < 1e-9))  # salida: False
```

## Errores típicos

- **Dar por hecho que independencia sobrevive al condicionamiento.** No sobrevive. Si condicionas
  en un efecto común (un collider), dos causas independientes se vuelven dependientes. Es el
  mecanismo detrás de la paradoja de Berkson y de muchos hallazgos que no se replican.
- **Interpretar correlación cero como independencia.** Solo descarta relación **lineal**. Con
  `Y = X²` la correlación es cero y la dependencia es total. Antes de afirmar independencia, mira
  el gráfico de dispersión.
- **Controlar por variables que son consecuencias del resultado.** Es el error opuesto a
  confundir: meter como «control» una variable posterior al tratamiento introduce sesgo en vez de
  quitarlo. Para saber qué controlar hay que dibujar el grafo causal
  ([[confusores-y-dag|confusores, mediadores y DAG]]).
- **Confundir independencia con sucesos disjuntos.** Si `A` y `B` son disjuntos y ambos tienen
  probabilidad positiva, son **dependientes** al máximo: saber que ocurrió uno descarta el otro.
  Disjunto no es independiente, es lo contrario.
- **Verificar la independencia solo con una tabla de contingencia global.** La independencia
  puede valer en el conjunto y fallar en subgrupos (o al revés). Es la **paradoja de Simpson**, y
  se detecta mirando los estratos, no solo el agregado.
- **Suponer independencia para multiplicar probabilidades sin justificarlo.** La regla
  `P(A ∩ B) = P(A)·P(B)` es una propiedad, no una definición universal. Con sucesos dependientes,
  ese producto da un número que no es ninguna probabilidad del experimento.

:::practica
enunciado: En una población, el 60 % lee prensa deportiva (A) y el 40 % va al gimnasio (B). Si condicionas a ser socio de un club (C), resulta P(A|C) = 0,6, P(B|C) = 0,4 y P(A ∩ B|C) = 0,25. Decide si A y B son condicionalmente independientes dado C.
pista: Compara la probabilidad conjunta condicionada con el producto de las dos condicionales.
solucion: El producto vale 0,6 · 0,4 = 0,24 y la conjunta condicionada 0,25. Como 0,25 no es 0,24, A y B no son condicionalmente independientes dado C: entre los socios hay una asociación leve que no existia en la población, el patron del colisionador. La diferencia es pequeña, así que el efecto es débil.
:::

## Comprueba que lo sabes

:::quiz
p: Dos sucesos A y B son independientes. ¿Qué se puede decir de su independencia condicional dado un tercer suceso C?
o: Que siguen siendo condicionalmente independientes, la independencia se hereda
o: Nada: pueden dejar de serlo (collider) o pueden pasar a serlo si antes no lo eran (confusor)
o: Que son dependientes dado C siempre
a: 2
e: La independencia marginal y la condicional son propiedades distintas. Condicionar en un efecto común de A y B las vuelve dependientes; condicionar en un confusor que las afecta a las dos puede volverlas independientes. Ninguna implica la otra.
:::

:::quiz
p: En un hospital se observa que los pacientes con la enfermedad A rara vez tienen la enfermedad B, aunque en la población general son independientes. ¿Cuál es la explicación más plausible?
o: Que A protege contra B
o: Que condicionar en estar hospitalizado (efecto común de A y B) crea una asociación negativa artificial
o: Que los datos del hospital están mal
a: 2
e: Es la paradoja de Berkson. Si ingresar depende de tener A o B, entre los ingresados la presencia de una enfermedad "explica" el ingreso y reduce la probabilidad relativa de la otra. La asociación existe en la muestra condicionada y no en la población.
:::

:::quiz
p: X toma valores -1, 0 y 1 con la misma probabilidad e Y = X². ¿Son independientes?
o: Sí, porque su correlación es cero
o: No: Y está completamente determinada por X, aunque la correlación sea cero
o: Solo son independientes si X no toma valores negativos
a: 2
e: La independencia exige que la distribución conjunta factorice, y aquí no lo hace: saber X determina Y. La correlación de Pearson solo mide relación lineal, y esta relación es cuadrática y simétrica, así que da cero. Es el ejemplo canónico de que correlación cero no es independencia.
:::

:::aviso
La independencia condicional no se puede comprobar mirando una tabla, porque hay infinitos
conjuntos en los que condicionar. Se decide **antes** de mirar los datos, con el grafo causal del
problema: qué causa qué y qué es consecuencia de qué. Elegir los controles después de ver qué
funciona es p-hacking con otro nombre.
:::
