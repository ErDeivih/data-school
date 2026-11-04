---
id: probabilidad-axiomas
titulo: Axiomas de probabilidad
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: []
tags: [probabilidad, fundamentos, conjuntos]
resumen: Espacio muestral, sucesos, unión e intersección: los tres axiomas de Kolmogorov y las reglas de suma que sostienen toda la estadística.
fuentes: ["Kolmogorov (1933), 'Grundbegriffe der Wahrscheinlichkeitsrechnung'"]
---

## En una frase

La probabilidad es una función que asigna a cada suceso un número entre 0 y 1, con la
probabilidad del suceso seguro igual a 1 y con la propiedad de que la probabilidad de varios
sucesos que no se solapan es la suma de sus probabilidades.

## La idea

Antes de calcular nada hay que decidir **qué puede pasar**. Lanzas un dado: los resultados
posibles son 1, 2, 3, 4, 5, 6. Ese conjunto de todo lo posible es el **espacio muestral**, y
cualquier subconjunto suyo (por ejemplo, «sale par» = {2, 4, 6}) es un **suceso**. Con ese
andamiaje, calcular probabilidades se reduce a contar y a combinar conjuntos: unir, intersecar,
complementar.

La parte que todo el mundo aprende a la fuerza es que **sumar probabilidades sin mirar si los
sucesos se solapan está mal**. Si en una clase el 60 % aprueba matemáticas y el 50 % aprueba
física, no puedes concluir que el 110 % aprueba alguna: hay alumnos que aprueban las dos, y esa
intersección se ha contado dos veces. La regla de la suma con corrección de solapamiento es la
herramienta más usada de todo el capítulo.

Los tres axiomas de Kolmogorov no dicen **cómo** asignar probabilidades (eso lo decide el modelo:
frecuencias, simetría, creencias). Solo imponen la coherencia mínima: que nada sea negativo, que
el total sea 1 y que las alternativas excluyentes se sumen. Casi todas las propiedades útiles
—la probabilidad del complementario, la regla de la suma, el principio de inclusión-exclusión—
se deducen de ahí en un par de líneas. Eso significa que si tu cálculo viola una de esas
propiedades, no es que esté «poco afinado»: es imposible.

## Definición formal

Sea `Ω` el **espacio muestral**: el conjunto de todos los resultados posibles de un experimento.
Un **suceso** `A` es un subconjunto de `Ω`.

Una función `P` que asigna un número real a cada suceso es una **probabilidad** si cumple los
tres axiomas:

:::formula
1) P(A) ≥ 0     2) P(Ω) = 1     3) P(A ∪ B) = P(A) + P(B) si A ∩ B = ∅
:::

- `Ω` — espacio muestral; `∅` — suceso imposible.
- `A ∪ B` — **unión**: ocurre `A`, o `B`, o los dos.
- `A ∩ B` — **intersección**: ocurren `A` y `B` a la vez.
- `A ∩ B = ∅` — sucesos **disjuntos** o mutuamente excluyentes: no pueden ocurrir juntos.
- El axioma 3 se extiende a cualquier colección numerable de sucesos disjuntos dos a dos.

De estos tres axiomas salen las reglas que se usan a diario:

- **Complementario:** `P(Aᶜ) = 1 − P(A)`, donde `Aᶜ` es «no ocurre A». Se deduce de que
  `A ∪ Aᶜ = Ω` y son disjuntos.
- **Suceso imposible:** `P(∅) = 0`. El recíproco no es cierto: un suceso de probabilidad cero
  puede ser posible (por ejemplo, que una variable continua valga exactamente 3).
- **Regla de la suma (inclusión-exclusión):**
  `P(A ∪ B) = P(A) + P(B) − P(A ∩ B)`. El término que se resta corrige el doble conteo.
- **Monotonía:** si `A ⊆ B`, entonces `P(A) ≤ P(B)`.
- **Cota:** `0 ≤ P(A) ≤ 1` para todo suceso.

Dos terminologías que conviene fijar: la **probabilidad conjunta** es `P(A ∩ B)` (los dos
sucesos a la vez) y la **probabilidad marginal** es `P(A)` (un suceso solo, sumando o integrando
sobre todo lo demás).

:::figura
fichero: axiomas-suma-con-solape
pie: En el panel izquierdo, las cien celdas son los casos posibles y cada una pesa 0,01: la zona verde pertenece a los dos sucesos a la vez, y por eso sumar 0,50 + 0,40 la cuenta dos veces. Fíjate en la barra de arriba del panel derecho: 0,90 es un número que ninguna probabilidad puede alcanzar, y esa es la señal de alarma. La corrección es restar el solape, que es justo la diferencia entre las dos barras.
fuente: figuras/probabilidad-axiomas-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Ω` | Espacio muestral: todos los resultados posibles | el conjunto de resultados | Si te dejas resultados fuera, todo lo que calcules encima deja de sumar 1 |
| `A`, `B` | Sucesos: subconjuntos de `Ω` | subconjuntos | Cuantos mas sucesos anadas a la union, mas pares de solapes hay que corregir |
| `P(A)` | Probabilidad del suceso `A` | adimensional, entre 0 y 1 | Nunca puede pasar de 1; si tu cuenta lo supera, has contado algo dos veces |
| `A ∪ B` | Union: ocurre `A`, o `B`, o los dos | subconjunto de `Ω` | Crece al crecer cualquiera de los dos sucesos, pero menos que la suma de los dos |
| `A ∩ B` | Intersección: ocurren los dos a la vez | subconjunto de `Ω` | Es el termino que se resta en la regla de la suma; si es vacio, la resta no hace falta |
| `Aᶜ` | Complementario: no ocurre `A` | subconjunto de `Ω` | `P(Aᶜ) = 1 − P(A)`: cuanto mas probable es `A`, menos lo es su contrario |
| `∅` | Suceso imposible | subconjunto vacio | `P(∅) = 0`, pero el reciproco no vale: con variables continuas hay sucesos posibles de probabilidad cero |
:::

## Ejemplo

En una universidad, el 50 % de los estudiantes aprueba Estadística (`E`), el 40 % aprueba
Programación (`P`) y el 20 % aprueba las dos.

- `P(E) = 0,50`, `P(P) = 0,40`, `P(E ∩ P) = 0,20`.
- Probabilidad de aprobar **al menos una**: `P(E ∪ P) = 0,50 + 0,40 − 0,20 = 0,70`. Sin restar
  la intersección habrías dicho 0,90: un error del 20 % de la población.
- Probabilidad de no aprobar ninguna: `1 − 0,70 = 0,30`.
- Probabilidad de aprobar Estadística pero no Programación:
  `P(E) − P(E ∩ P) = 0,50 − 0,20 = 0,30`.
- Comprobación de coherencia: las cuatro casillas de la tabla suman 1.

```
                 aprueba P   no aprueba P   total
aprueba E           0,20         0,30        0,50
no aprueba E        0,20         0,30        0,40
total               0,40         0,60        1,00
```

Un detalle que se ve en la tabla: los dos sucesos son **independientes**, porque
`0,50 · 0,40 = 0,20 = P(E ∩ P)`. Esa coincidencia no es casualidad en este ejemplo, y se estudia
en [[independencia-y-condicionamiento|independencia y condicionamiento]].

## Código

```python verificable
# 100 estudiantes. E = aprueba Estadística (50), P = aprueba Programación (40).
# La intersección son los índices 0-19 (20 estudiantes que aprueban las dos).
estadistica = set(range(0, 20)) | set(range(50, 80))
programacion = set(range(0, 20)) | set(range(80, 100))

p_e = len(estadistica) / 100
p_p = len(programacion) / 100
p_interseccion = len(estadistica & programacion) / 100
p_union = len(estadistica | programacion) / 100

print("P(E)             ", p_e)                                # salida: 0.5
print("P(P)             ", p_p)                                # salida: 0.4
print("P(E y P)         ", p_interseccion)                     # salida: 0.2
print("P(E o P)         ", p_union)                            # salida: 0.7
print("sumar sin restar ", p_e + p_p)                          # salida: 0.9
print("regla de la suma ", round(p_e + p_p - p_interseccion, 10))  # salida: 0.7
```

:::claves
- Los conjuntos se construyen con `set(range(0, 20)) | set(range(50, 80))`. La barra vertical no es «o lógico» aquí: es el operador de **union** de conjuntos, y `&` es la **intersección**. Cambiar `|` por `&` daria el suceso contrario al que quieres.
- `range(0, 100, 4)` en el segundo bloque lleva un tercer argumento: el paso. Genera `0, 4, 8, …, 96`, es decir 25 elementos. Sin ese 4 tendrias los 100 índices y `P(C)` sería 1 en vez de 0,25.
- Dividir entre 100 con la barra normal produce un `float` aunque el resultado sea entero: `len(estadistica) / 100` da `0.5`, no `0`. Con `//` obtendrias `0` y el ejemplo entero se caeria sin avisar.
- La resta `p_e + p_p - p_interseccion` se redondea a 10 decimales porque la suma en coma flotante deja un residuo del orden de `1e-17`. Ese residuo es la razón de comparar con tolerancia y no con `==` cuando compruebas el axioma 2.
- El error que ilustra el bloque no es un fallo del código sino de la formula: `p_e + p_p` vale 0,9 y ese número no es «la probabilidad de algo». Los estudiantes que aprueban las dos asignaturas están dentro de los dos conjuntos y se cuentan dos veces.
- En el bloque de inclusion-exclusion, `p(A & B & C)` es la intersección **triple**, que entra sumando al final. Si te olvidas de ella, con tres sucesos el resultado sale 0,75 en vez de 0,81: la formula corta sobreestima la union.
:::

```python verificable
# Regla de la suma con tres sucesos: inclusion-exclusion completa.
A = set(range(0, 50))        # P(A) = 0.50
B = set(range(25, 75))       # P(B) = 0.50
C = set(range(0, 100, 4))    # P(C) = 0.25

p = lambda s: len(s) / 100
union = p(A | B | C)
suma_simple = p(A) + p(B) + p(C)
inclusion_exclusion = suma_simple - p(A & B) - p(A & C) - p(B & C) + p(A & B & C)

print("P(A o B o C)          ", union)                          # salida: 0.81
print("A y B independientes  ", bool(abs(p(A & B) - p(A) * p(B)) < 1e-12))  # salida: True
print("suma de los tres      ", round(suma_simple, 4))          # salida: 1.25
print("suma - parejas        ", round(suma_simple - p(A & B) - p(A & C) - p(B & C), 4))  # salida: 0.75
print("inclusion-exclusion   ", round(inclusion_exclusion, 10))  # salida: 0.81
print("interseccion triple   ", round(p(A & B & C), 4))         # salida: 0.06
```

```python verificable
import numpy as np

# Tres axiomas, tres comprobaciones con un dado simulado de forma determinista.
caras = np.arange(1, 7)
p = np.full(6, 1 / 6)

print("axioma 1, todas >= 0 :", bool(np.all(p >= 0)))                 # salida: True
print("axioma 2, suma = 1   :", round(float(p.sum()), 12))            # salida: 1.0

par = caras % 2 == 0                 # {2, 4, 6}
multiplo_de_3 = caras % 3 == 0       # {3, 6}
p_par = float(p[par].sum())
p_mult3 = float(p[multiplo_de_3].sum())
p_ambos = float(p[par & multiplo_de_3].sum())

print("P(par)               :", round(p_par, 4))                      # salida: 0.5
print("P(multiplo de 3)     :", round(p_mult3, 4))                    # salida: 0.3333
print("P(par y multiplo 3)  :", round(p_ambos, 4))                    # salida: 0.1667
print("P(par o multiplo 3)  :", round(p_par + p_mult3 - p_ambos, 4))   # salida: 0.6667
print("complementario       :", round(1 - p_par, 4))                  # salida: 0.5
```

## Errores típicos

- **Sumar probabilidades de sucesos que se solapan.** `P(A ∪ B) = P(A) + P(B)` solo vale si
  `A ∩ B = ∅`. En cualquier otro caso hay que restar la intersección o el resultado puede pasar
  de 1, que es la señal de alarma evidente.
- **Confundir unión con intersección.** «O» es unión (basta uno) y «y» es intersección (hacen
  falta los dos). Leer «aprueba mates o física» como intersección es el fallo más frecuente en
  los enunciados con lenguaje natural.
- **Creer que probabilidad cero significa imposible.** Para variables continuas, la probabilidad
  de un valor concreto es cero y el suceso es perfectamente posible. Solo el suceso vacío es
  imposible.
- **Suponer que todos los resultados son equiprobables sin justificarlo.** Repartir `1/n` entre
  `n` resultados exige un argumento de simetría. Dos resultados posibles («llueve» / «no llueve»)
  no tienen probabilidad 0,5 cada uno: la moneda no está en el enunciado.
- **Definir mal el espacio muestral.** Si `Ω` no incluye todos los resultados posibles, las
  probabilidades no suman 1 y todo lo que construyas encima está mal. Empieza siempre enumerando
  los resultados.
- **Olvidar que la regla de inclusión-exclusión tiene más términos con tres sucesos.**
  `P(A ∪ B ∪ C) = P(A) + P(B) + P(C) − P(A∩B) − P(A∩C) − P(B∩C) + P(A∩B∩C)`. Quedarse en los tres
  primeros términos sobreestima la unión.

:::practica
enunciado: En un gimnasio con 500 socios, 275 hacen yoga, 200 hacen spinning y 75 practican las dos cosas. Calcula la probabilidad de que un socio elegido al azar no haga ninguna de las dos.
pista: Primero la union con la regla de la suma; el complementario sale de que todo el espacio suma 1.
solucion: P(Y ∪ S) = 275/500 + 200/500 − 75/500 = 0,55 + 0,40 − 0,15 = 0,80. Ninguna de las dos: 1 − 0,80 = 0,20, es decir 100 socios. Comprobación: 0,55 + 0,40 − 0,15 = 0,80 y 0,80 + 0,20 = 1. Sumar sin restar la intersección daria 0,95 y el resultado sería imposible.
:::

## Comprueba que lo sabes

:::quiz
p: En un grupo, el 60 % juega al fútbol, el 30 % juega al baloncesto y el 10 % juega a los dos. ¿Qué porcentaje juega al menos a uno?
o: 90 %
o: 80 %
o: 70 %
a: 2
e: Por la regla de la suma, 0,60 + 0,30 - 0,10 = 0,80. Sumar sin restar la intersección cuenta dos veces a quien practica ambos deportes y da 0,90, que es un resultado incorrecto.
:::

:::quiz
p: ¿Cuál de estas afirmaciones se deduce de los axiomas y cuál no?
o: P(A ∪ B) = P(A) + P(B) − P(A ∩ B) se deduce de los axiomas
o: P(A) = 0,5 para cualquier suceso A con dos resultados posibles
o: P(A ∩ B) = P(A) · P(B) siempre
a: 1
e: La regla de la suma se demuestra descomponiendo A ∪ B en tres trozos disjuntos. Que dos resultados sean equiprobables requiere un supuesto de simetría, y que la intersección se multiplique es la definición de independencia, que no se cumple siempre.
:::

:::quiz
p: Un suceso tiene probabilidad exactamente 0. ¿Qué se puede afirmar?
o: Que es imposible en todos los casos
o: Que es imposible si el espacio muestral es finito o numerable, pero puede ser posible con variables continuas
o: Que el experimento está mal diseñado
a: 2
e: Con un espacio muestral discreto, probabilidad cero implica que el suceso es vacío. Con una variable continua, cada valor concreto tiene probabilidad cero y sigue siendo un resultado posible: la densidad describe intervalos, no puntos.
:::

:::nota
Los axiomas no dicen de dónde salen los números. Un modelo frecuentista los obtiene contando
repeticiones; uno bayesiano, actualizando creencias. Discutir sobre probabilidades sin decir
qué modelo las genera es discutir sobre nada: los axiomas son las reglas del juego, no la
estrategia.
:::
