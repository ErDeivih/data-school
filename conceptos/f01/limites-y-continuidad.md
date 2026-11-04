---
id: limites-y-continuidad
titulo: Límites y continuidad
fase: 1
nivel: básico
rutas: [core]
prerequisitos: [notacion-matematica]
tags: [calculo, limites, continuidad, funciones]
resumen: El límite describe a dónde se acerca una función sin necesidad de llegar; la continuidad exige además que el valor de la función esté ahí.
fuentes: ["Stewart (2015), 'Calculus: Early Transcendentals'", "Spivak (2008), 'Calculus'"]
---

## En una frase

El **límite** de una función en un punto es el valor al que se acercan sus resultados cuando la
variable se acerca a ese punto, sin importar si la función está definida allí; la función es
**continua** en el punto si además está definida y su valor coincide con ese límite, es decir,
si no hay ningún salto.

## La idea

Vas en coche hacia una ciudad y te quedas en la gasolinera de la entrada: te acercabas a ella,
aunque no hayas entrado. El límite es eso, el sitio hacia el que ibas; que la entrada esté
cortada no cambia el destino. Matemáticamente, `lim f(x)` cuando `x → a` describe el
comportamiento de `f` **cerca** de `a`, y no dice nada sobre `f(a)`.

La continuidad añade la segunda pieza: además de acercarse a un valor, la función **tiene** ese
valor en el punto, y se puede dibujar sin levantar el lápiz. Casi todas las funciones que usarás
en un modelo (sumas, potencias, exponenciales, logaritmos en su dominio) son continuas, y esa es
la buena noticia. La mala es que hay excepciones: una función definida a trozos (un umbral, un
[[z-score-y-estandarizacion|indicador]] que vale 0 o 1, una penalización por tramos) puede dar
saltos, y en el salto el [[derivadas-y-reglas|gradiente]] no existe y el optimizador se atasca.

¿Por qué es esto lo primero del cálculo? Porque las dos ideas centrales se definen como
límites. La derivada es el límite de un cociente, `(f(a + h) − f(a)) / h` cuando `h → 0`, y ahí
el numerador y el denominador tienden a cero a la vez. La integral es el límite de una suma de
rectángulos cuando su ancho tiende a cero (ver [[integrales|integrales]]). Y hay una
consecuencia muy práctica: si una función continua cambia de signo, en algún punto intermedio
vale cero, que es lo que sostiene la búsqueda de raíces por bisección.

## Definición formal

**Límite.** Se escribe `lim_{x→a} f(x) = L` si se puede hacer que `f(x)` esté tan cerca de `L`
como se quiera sin más que tomar `x` suficientemente cerca de `a`, pero distinto de `a`. Con
las letras griegas habituales: para todo `ε > 0` existe un `δ > 0` tal que si la distancia
entre `x` y `a` es menor que `δ` y `x ≠ a`, entonces la distancia entre `f(x)` y `L` es menor
que `ε`.

- `a` — el punto al que se acerca la variable (puede ser un número o infinito).
- `L` — el valor límite; si `f` se dispara sin techo, se dice que el límite es `+∞`.
- `ε` (épsilon) — la tolerancia de cercanía que exiges en la salida.
- `δ` (delta) — la cercanía en la entrada que necesitas para conseguirla.
- El `0 <` de `x ≠ a` es la clave: el límite **no mira** el valor en el punto.

**Límites laterales.** `lim_{x→a⁻}` es el límite por la izquierda (valores menores que `a`) y
`lim_{x→a⁺}` por la derecha. El límite normal existe si y solo si los dos laterales existen y
son iguales. Este es el criterio que se usa para detectar saltos.

**Continuidad en `a`.** `f` es continua en `a` si se cumplen las tres condiciones: `f(a)` está
definida; existe `lim_{x→a} f(x)`; y ambos coinciden. Si `f` es continua en todos los puntos de
un intervalo, es continua en el intervalo.

**Tipos de discontinuidad.** *Evitable* (el límite existe pero `f(a)` no está definida o no
coincide); *de salto* (los laterales existen, pero son distintos); *infinita* (el límite se va
a infinito, como `1/x` en `x = 0`).

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `a` | El punto al que se acerca la variable (o `±∞`) | las de la entrada | No es un parámetro del resultado: cambiarlo cambia el problema entero. El límite se calcula punto a punto |
| `L` | El valor al que se acercan las salidas | las de la salida | No es una cota que se ajuste: o los valores se acercan a él o el límite no existe |
| `ε` | La tolerancia de cercanía que exiges en la salida | las de la salida | Al hacerla más pequeña, la exigencia aumenta: si el límite existe siempre se puede cumplir, y si no existe no hay `δ` que valga |
| `δ` | La cercanía en la entrada que necesitas para lograrlo | las de la entrada | No es único: si un `δ` sirve, cualquiera más pequeño también. Su tamaño depende de `ε` y del punto |
| `x` | La variable de entrada | las de la entrada | Debe acercarse a `a` **sin llegar**: el `0 <` de `abs(x − a) < δ` es lo que hace que el valor `f(a)` no importe |
:::

**Propiedades útiles.** La suma, el producto, el cociente (con denominador no nulo) y la
composición de funciones continuas son continuas. **Teorema de Bolzano o del valor
intermedio:** si `f` es continua en `[a, b]` y `f(a)` y `f(b)` tienen signos opuestos, existe
al menos un `c` en `(a, b)` con `f(c) = 0`. **Teorema de Weierstrass:** una función continua en
un intervalo cerrado y acotado alcanza su máximo y su mínimo.

:::figura
fichero: limites-hueco-y-salto
pie: Arriba, la función `(x² − 1)/(x − 1)`: en `x = 1` hay un hueco (el punto rojo, donde la función no existe) y a su alrededor los valores se pegan a 2 por los dos lados. Ese es el límite, y no cambia porque el punto esté cortado. Abajo, la función signo: los dos laterales existen y valen −1 y +1, pero como no coinciden el límite no existe. Comparar los dos paneles es la diferencia entre discontinuidad evitable y de salto.
fuente: figuras/limites-y-continuidad-1.py
:::

## Ejemplo

**Discontinuidad evitable.** `f(x) = (x² − 1) / (x − 1)`. En `x = 1` sale `0/0`, así que `f(1)`
no está definida. Pero factorizando, `x² − 1 = (x − 1)(x + 1)`, y para `x ≠ 1` la función
equivale a `x + 1`. Valores concretos:

| x | 0,9 | 0,99 | 1,01 | 1,1 |
| --- | --- | --- | --- | --- |
| f(x) | 1,9 | 1,99 | 2,01 | 2,1 |

El límite es 2, y el hueco está solo en `x = 1`. Es evitable porque bastaría definir `f(1) = 2`
para que la función fuera continua.

**Discontinuidad de salto.** `g(x) = −1` si `x < 0`, `g(0) = 0` y `g(x) = 1` si `x > 0` (la
función signo). Por la izquierda el límite es `−1`; por la derecha, `+1`. Como no coinciden,
`lim_{x→0} g(x)` **no existe**: no hay ningún número al que se acerque por los dos lados.

**Discontinuidad infinita.** `h(x) = 1/x` en `x = 0`: por la derecha crece sin límite y por la
izquierda decrece sin límite. No es un salto finito; la recta `x = 0` es una asíntota vertical.

**Dónde sí se puede aplicar Bolzano.** `f(x) = x³ − x − 2` es continua en todo `ℝ`, con
`f(1) = −2` y `f(2) = 4`: cambia de signo, así que hay una raíz en `(1, 2)`. Bisecando se llega
a `x ≈ 1,52138`.

## Código

```python verificable
def f(x):
    return (x ** 2 - 1) / (x - 1)

# En x = 1 hay 0/0: la funcion no esta definida, pero los valores se acercan a 2.
print("f(0.9) :", round(f(0.9), 3))     # -> 1.9
print("f(0.99):", round(f(0.99), 3))    # -> 1.99
print("f(1.01):", round(f(1.01), 3))    # -> 2.01
print("f(1.1) :", round(f(1.1), 3))     # -> 2.1

# La funcion signo: los laterales existen pero no coinciden, asi que no hay limite.
def g(x):
    return -1.0 if x < 0 else (0.0 if x == 0 else 1.0)

print("lateral izquierdo:", g(-0.001))   # -> -1.0
print("lateral derecho  :", g(0.001))    # -> 1.0
print("valor en el punto:", g(0.0))      # -> 0.0
```

:::claves
- `(x ** 2 - 1) / (x - 1)` usa **una sola barra**, que en Python 3 siempre da un número decimal; con `//` se quedaría con la parte entera y el ejemplo daría `1.0` en lugar de `1.9`. La diferencia importa aquí porque todo el ejercicio va de acercarse a 2, no a 1.
- En `x = 1` esta función **lanza** una excepción, no devuelve un `nan`: Python no aplica la aritmética de punto flotante de IEEE a la división entre cero de `float`, y `f(1)` termina con `ZeroDivisionError: float division by zero`. NumPy sí se comporta al estilo IEEE: `np.float64(1) / 0` da `inf`, `0 / 0` da `nan` y en los dos casos emite un aviso.
- `return -1.0 if x < 0 else (0.0 if x == 0 else 1.0)` es una **expresión condicional encadenada**: si `x` es negativo devuelve `-1.0`; si no, evalúa el segundo `if`; y si tampoco, `1.0`. En `x = 0` la primera comparación es falsa y la segunda verdadera, así que devuelve `0.0`.
- Esa función y `np.sign` coinciden en los tres tramos, pero `np.sign` trabaja sobre arrays y devuelve un array, mientras que esta devuelve un `float` de Python. Mezclarlas en una comparación funciona, y luego sorprende cuando una es vectorial y la otra no.
- El bucle de bisección parte el intervalo en dos **60 veces**: cada vuelta gana un bit de precisión y con 60 rondas el error baja por debajo de `10⁻¹⁸`. No hay criterio de parada: si te equivocas de signo en la comparación `f(mid) < 0`, el bucle converge igual a la otra raíz, sin avisar.
- `round((lo + hi) / 2, 6)` redondea a 6 decimales **para imprimir**, no para calcular: el número que queda en `lo` y `hi` conserva toda su precisión. Si usaras el valor redondeado dentro del bucle, la bisección se atascaría antes de tiempo.
:::

```python verificable
# f es continua y cambia de signo en [1, 2]: Bolzano garantiza una raiz dentro.
def f(x):
    return x ** 3 - x - 2

print("f(1):", f(1.0))   # -> -2.0
print("f(2):", f(2.0))   # -> 4.0

lo, hi = 1.0, 2.0
for _ in range(60):
    mid = (lo + hi) / 2
    if f(mid) < 0:
        lo = mid
    else:
        hi = mid
print("raiz aproximada:", round((lo + hi) / 2, 6))   # -> 1.52138
```

```python verificable
# En coma flotante, "acercarse" no es llegar: los numeros reales no se representan exactos.
print("0.1 + 0.2 - 0.3:", 0.1 + 0.2 - 0.3)                        # -> 5.551115123125783e-17
print("en notacion cientifica:", format(0.1 + 0.2 - 0.3, ".2e"))  # -> 5.55e-17
print("es exactamente cero:", 0.1 + 0.2 - 0.3 == 0.0)             # -> False
```

## Errores típicos

- **Creer que el límite exige que la función esté definida en el punto.** Es justo al contrario: el caso interesante es cuando no lo está, como `(x² − 1) / (x − 1)` en `x = 1`, donde el límite vale 2.
- **Sustituir, obtener `0/0` y echar mano de L'Hôpital a ciegas.** `0/0` es una **indeterminación**: el resultado puede ser cualquier cosa, así que primero factoriza y simplifica. Y L'Hôpital solo se aplica a `0/0` o a `∞/∞`; usarlo con `2/3` o con `1/0` da un resultado sin sentido.
- **Mirar solo un lado.** Con funciones definidas a trozos, con umbrales, con valores absolutos o con `ReLU` el límite puede no existir aunque los dos laterales existan por separado. Comprueba siempre los dos.
- **Confundir continuo con suave o derivable.** La función valor absoluto de `x` es continua en `x = 0` y no es derivable allí: tiene un pico. Continuidad es «no hay salto», no «no hay esquina».
- **Creer que una función continua alcanza su máximo en cualquier intervalo.** Weierstrass pide intervalo **cerrado y acotado**. `f(x) = x` en el intervalo abierto `(0, 1)` es continua y no alcanza ni el 0 ni el 1.
- **Confundir «límite finito cuando `x` crece» con «la función se vuelve constante».** `1/x` tiende a 0 cuando `x → +∞`, y nunca vale 0.

:::practica
enunciado: La tarifa de un parking es f(t) = 2t si t < 3 y f(t) = 5 + 2t si t ≥ 3, con t en horas. ¿Es continua en t = 3? Y para h(x) = (x² − 4) / (x − 2), ¿qué valor hay que darle a h(2) para que sea continua?
pista: Mira los dos límites laterales en el punto conflictivo.
solucion: En t = 3 el lateral izquierdo vale 6 y el derecho 11: no coinciden, hay un salto y f no es continua. En h, factorizando, x² − 4 = (x − 2)(x + 2), así que para x ≠ 2 vale x + 2 y el límite es 4; definiendo h(2) = 4 la discontinuidad es evitable.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué se puede decir de f(x) = (x² − 1) / (x − 1) en x = 1?
o: El límite vale 2 aunque f(1) no esté definida: la discontinuidad es evitable
o: El límite no existe porque la función no está definida en el punto
o: El límite es 0 porque el numerador se anula
a: 1
e: Factorizando, para x ≠ 1 la función es x + 1, cuyos valores se acercan a 2 por ambos lados. El límite no necesita que f(1) exista; si definiéramos f(1) = 2, la función sería continua. Que el numerador se anule no implica que el límite sea 0: también se anula el denominador.
:::

:::quiz
p: Una función definida a trozos vale 0 para x < 0 y 3 para x mayor o igual que 0. ¿Qué pasa en x = 0?
o: El límite por la izquierda es 0 y por la derecha 3, así que el límite no existe y hay un salto
o: El límite es 1,5 porque es el punto medio entre los dos valores
o: El límite existe y vale 3, porque ese es el valor de la función en 0
a: 1
e: El límite existe solo si los dos laterales coinciden; aquí valen 0 y 3. El punto medio no es un límite de nada, y el valor de la función en el punto no arregla el salto: la función no es continua allí.
:::
