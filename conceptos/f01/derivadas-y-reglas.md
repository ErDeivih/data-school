---
id: derivadas-y-reglas
titulo: Derivadas y reglas de derivación
fase: 1
nivel: básico
rutas: [core, ds, quant]
prerequisitos: [limites-y-continuidad]
tags: [calculo, derivadas, optimizacion, marginal]
resumen: La derivada es la pendiente de la recta tangente; las reglas de producto, cociente y cadena permiten derivar sin volver al límite cada vez.
fuentes: ["Stewart (2015), 'Calculus: Early Transcendentals'", "Deisenroth, Faisal y Ong (2020), 'Mathematics for Machine Learning'"]
---

## En una frase

La **derivada** de una función en un punto es la pendiente de la recta tangente en ese punto,
es decir, cuánto cambia la salida por cada unidad de cambio en la entrada; las **reglas de
derivación** son los atajos que permiten calcularla sin repetir el límite cada vez.

## La idea

El cuentakilómetros de un coche mide la distancia total; el velocímetro mide a qué ritmo
cambia esa distancia. Si has recorrido 120 km en 2 horas, tu velocidad **media** ha sido de
60 km/h, pero eso no te dice si en un momento concreto ibas a 30 o a 130. La derivada es el
velocímetro: el cambio instantáneo, medido en un instante tan pequeño como quieras.

Se calcula con un truco de dos pasos. Primero, el **cociente incremental**: recorres un poco
más (de `x` a `x + h`), miras cuánto ha cambiado la función y divides entre `h`. Eso es la
velocidad media en ese trocito. Después encoges `h` hasta cero, y lo que queda es la velocidad
instantánea. Ese «después encoges `h`» es exactamente el [[limites-y-continuidad|límite]] del
cociente, y por eso la derivada se define como un límite.

Con la derivada a mano se pueden hacer tres cosas que usarás constantemente:

1. **Encontrar óptimos.** En un máximo o un mínimo la recta tangente es horizontal, así que
   `f'(x) = 0`. Es el mecanismo de todos los métodos de optimización, y la base del
   [[derivadas-parciales-y-gradiente|gradiente]] y del descenso de gradiente.
2. **Leer un marginal.** En economía y en negocio, la derivada del ingreso respecto al precio
   dice cuánto ganas por subir el precio una unidad. No es una metáfora: es literalmente la
   derivada.
3. **Aproximar.** Para cambios pequeños, `f(x + h) ≈ f(x) + f'(x)·h`. Esto es la
   **linealización**, y es lo que hace que un modelo lineal funcione bien cerca del punto de
   trabajo.

La otra pieza importante es la segunda derivada: mide cómo cambia la pendiente, es decir, la
curvatura. Si es positiva, la función se curva hacia arriba (convexa) y el punto crítico es un
mínimo; si es negativa, se curva hacia abajo y es un máximo.

## Definición formal

La derivada de `f` en el punto `a` es el límite del cociente incremental:

:::formula
f'(a) = lim_{h→0} ( f(a + h) − f(a) ) / h
:::

- `f` — la función que se deriva; debe estar definida alrededor de `a`.
- `a` — el punto donde se mide el cambio instantáneo.
- `h` — el incremento en la entrada; el límite se toma cuando tiende a cero.
- `f'(a)` — la derivada. También se escribe `df/dx` evaluada en `a`.
- Si el límite existe, `f` es **derivable** en `a`. Ser derivable implica ser continua, pero no
  al revés (el valor absoluto de `x` es continuo en 0 y no derivable allí).

:::figura
fichero: derivadas-tangente-y-paso
pie: A la izquierda, la parábola y tres rectas secantes trazadas desde el punto `x = 2` con pasos cada vez más pequeños: 1, 0,5 y 0,1. Sus pendientes son 13, 11,5 y 10,3, y se van pegando a la tangente, que tiene pendiente exactamente 10. Ese es el límite. A la derecha está la trampa que aparece al hacerlo con el ordenador: el error de la fórmula baja mientras `h` se encoge, toca fondo cerca de `h = 10⁻⁸` y luego **sube** otra vez porque restar dos números casi iguales pierde dígitos. Encoger `h` no siempre mejora el resultado.
fuente: figuras/derivadas-y-reglas-1.py
:::

**Reglas de derivación** (con `c` una constante, `f` y `g` derivables):

| función | derivada | comentario |
| --- | --- | --- |
| c | 0 | una constante no cambia |
| xⁿ | n · xⁿ⁻¹ | válida para cualquier exponente real |
| f + g | f' + g' | la derivada reparte sumas |
| c · f | c · f' | las constantes salen fuera |
| f · g | f' · g + f · g' | regla del producto: dos términos |
| f / g | (f' · g − f · g') / g² | regla del cociente; el orden importa |
| f(g(x)) | f'(g(x)) · g'(x) | regla de la cadena |
| eˣ | eˣ | la exponencial es su propia derivada |
| ln x | 1 / x | definida para x mayor que 0 |

- **Regla de la cadena:** se desarrolla en [[regla-de-la-cadena|regla de la cadena]]. Es la
  pieza que hace posible la retropropagación de una red neuronal.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `f` | La función que se deriva | las de la salida | No es un parámetro: cambiarla cambia el problema. Lo que importa es que esté definida alrededor de `a` |
| `a` | El punto donde se mide el cambio instantáneo | las de la entrada | Al moverlo cambia la pendiente aunque la función sea la misma: `f'(2)` y `f'(3)` son números distintos |
| `h` | El incremento de la entrada en el cociente incremental | las de la entrada | Al encogerlo, la secante se pega a la tangente y el resultado se acerca al valor exacto; pero por debajo de `10⁻⁸` el redondeo de la resta domina y el error vuelve a crecer |
| `f'` | La derivada, también escrita `df/dx` | salida por unidad de entrada | Es un número, no una función: dice cuánto sube la salida por cada unidad que sube la entrada |
| `f''` | La segunda derivada: la curvatura | salida por unidad de entrada al cuadrado | Si en un punto crítico es positiva hay un mínimo; si es negativa, un máximo; si es cero, el criterio no decide y hay que mirar más allá |
:::
- **Punto crítico:** donde `f'(x) = 0` o donde la derivada no existe. No todos son óptimos:
  también puede ser un punto de inflexión.
- **Criterio de la segunda derivada:** si `f'(a) = 0` y `f''(a) > 0`, hay un mínimo local; si
  `f''(a) < 0`, un máximo local; si `f''(a) = 0`, el criterio no decide.
- **Derivadas de orden superior:** `f''` es la derivada de `f'`, y mide curvatura y aceleración.

## Ejemplo

**Pendiente paso a paso.** `f(x) = 3x² − 2x + 1`. Aplicando las reglas: `f'(x) = 6x − 2`, así
que `f'(2) = 10`. Comprobación numérica con el cociente incremental en `x = 2`:

- Con `h = 0,1`: `(f(2,1) − f(2)) / 0,1 = 10,3`.
- Con `h = 0,01`: `10,03`.
- Con `h = 0,001`: `10,003`.

Se acerca a 10, que es el valor exacto. El cociente incremental es una aproximación; el límite
es el valor real.

**Un caso de negocio con regla del producto.** Una empresa vende a precio `p` y su demanda es
`D(p) = 100 − 2p` unidades. El ingreso es `R(p) = p · D(p) = p · (100 − 2p) = 100p − 2p²`.
Derivando: `R'(p) = 100 − 4p`. El ingreso marginal en `p = 20` es `100 − 80 = 20`: subir el
precio un euro más aportaría 20 euros de ingreso. Igualando a cero, `100 − 4p = 0` da `p = 25`,
y `R(25) = 2500 − 1250 = 1250`. Como `R''(p) = −4 < 0`, es un máximo: a partir de 25 €, subir
el precio reduce el ingreso.

**Curvatura.** `f(x) = (x − 3)²` tiene `f'(x) = 2(x − 3)`, que se anula en `x = 3`, y
`f''(x) = 2 > 0`, así que `x = 3` es un mínimo. Empezando en `x = 0` y dando pasos en la
dirección contraria al gradiente con tasa `0,1`, tras 20 pasos se llega a `x ≈ 2,9654`, muy
cerca del mínimo.

## Código

```python verificable
def f(x):
    return 3 * x ** 2 - 2 * x + 1

def pendiente_numerica(x, h):
    return (f(x + h) - f(x)) / h

# Al reducir h, el cociente incremental se acerca a la derivada exacta, que vale 10.
print("h=0.1   :", round(pendiente_numerica(2, 0.1), 4))     # -> 10.3
print("h=0.01  :", round(pendiente_numerica(2, 0.01), 4))    # -> 10.03
print("h=0.001 :", round(pendiente_numerica(2, 0.001), 4))   # -> 10.003
print("exacta  :", 6 * 2 - 2)                                # -> 10

# Con h demasiado pequeno la resta pierde precision y la aproximacion empeora.
print("h=1e-13 :", round(pendiente_numerica(2, 1e-13), 6))   # -> 9.983125
```

:::claves
- `(f(x + h) - f(x)) / h` es una **diferencia hacia delante**: usa el punto de la derecha y el de partida. Tiene un error de orden `h`, mientras que la diferencia central `(f(x + h) - f(x - h)) / (2h)` tiene error de orden `h²` y da muchos más dígitos correctos con el mismo esfuerzo.
- En Python 3 la barra `/` **siempre** devuelve decimal: `(f(2.1) - f(2.0)) / 0.1` da `10.300000000000011` y no `10`. El `round(..., 4)` solo tapa los décimos de cola que arrastra la resta; el error de la fórmula sigue ahí, debajo.
- Con `h = 1e-13` el resultado empeora (`9.983125`) porque `f(2 + h) - f(2)` es la resta de dos números que coinciden en sus primeros 13 dígitos. Un `float` de 64 bits guarda unos 16 dígitos significativos: los que se comen la resta se pierden para siempre.
- `pendiente_numerica` recibe `h` como argumento y por eso se puede recorrer un rango de `h` y comparar errores. Si `h` estuviera escrito dentro de la función, ese experimento habría que reescribirlo entero para cada valor.
- El descenso de gradiente del segundo bloque lleva tres números que deciden todo: `0.1` es la tasa de aprendizaje, `2 * (x - 3)` es la derivada escrita a mano y `20` son las iteraciones. Solo se cambia la derivada si se cambia la función; nada en el bucle comprueba si el resultado es correcto.
- Con tasa `0.1` el método se acerca al mínimo pero **no lo pisa nunca**: se queda en `x ≈ 2.9654`. Con tasa `1.0` oscilaría sin converger y con `2.0` se alejaría. La tasa no es un detalle de estilo: por encima de `2 / f''(x)` el método diverge.
:::

```python verificable
# Descenso de gradiente sobre f(x) = (x - 3)^2, cuyo minimo esta en x = 3.
x = 0.0
for _ in range(20):
    x = x - 0.1 * 2 * (x - 3)   # 0.1 es la tasa de aprendizaje; 2(x-3) es la derivada

print("x tras 20 pasos:", round(x, 6))            # -> 2.965412
print("valor de f(x)  :", round((x - 3) ** 2, 10))   # -> 0.0011963052
```

## Errores típicos

- **Derivar un producto como producto de derivadas.** `(f · g)'` **no** es `f' · g'`. Con `f = x` y `g = x` sería `1 · 1 = 1`, cuando la derivada de `x²` es `2x`. Hay que usar `f'g + fg'`.
- **Olvidar la regla de la cadena.** La derivada de `e^{2x}` es `2e^{2x}`, no `e^{2x}`; la de `(x² + 1)⁵` es `5(x² + 1)⁴ · 2x`. Si dentro hay una función, hay un factor extra.
- **Confundir la derivada con la función dividida por la variable.** `f'(x)` no es `f(x) / x`. Para `f(x) = x²`, `f(2)/2 = 2` y `f'(2) = 4`; coinciden por casualidad en ese ejemplo y en casi ningún otro.
- **Creer que `f'(x) = 0` significa mínimo.** Puede ser un máximo, un punto de inflexión o una meseta. Mira la segunda derivada o el signo de `f'` a ambos lados.
- **Ignorar el dominio.** `1/x` no se puede derivar en `x = 0` (no está definida), `√x` no lo es para `x < 0` y `ln x` solo para `x > 0`. Derivar fuera del dominio produce expresiones que parecen válidas y no lo son.
- **Usar diferencias finitas con un `h` demasiado pequeño.** Al restar dos números casi iguales se pierde precisión: con `h = 10⁻¹³` el ejemplo da `9,983125` en lugar de acercarse más a 10. Para derivadas numéricas se usa una diferencia central y un `h` del orden de `10⁻⁵` a `10⁻⁸`.

:::practica
enunciado: Con la demanda D(p) = 120 − 3p, escribe el ingreso R(p) = p · D(p), calcula el ingreso marginal en p = 15 y decide qué precio lo maximiza. Comprueba después la pendiente de f(x) = x³ en x = 2 con el cociente incremental y h = 0,1.
pista: Multiplica antes de derivar y usa la regla de la potencia término a término.
solucion: R(p) = 120p − 3p², luego R'(p) = 120 − 6p; en p = 15 vale 30, así que subir el precio un euro aporta 30 euros. El máximo está donde R' = 0, en p = 20, con R(20) = 1200, y R'' = −6 < 0 confirma el máximo. Para f(x) = x³, f'(x) = 3x² y f'(2) = 12; el cociente da (2,1³ − 2³)/0,1 = (9,261 − 8)/0,1 = 12,61, una aproximación por encima.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la derivada de f(x) = 3x² − 2x + 1 en x = 2?
o: 10, porque f'(x) = 6x − 2 y 6·2 − 2 = 10
o: 9, porque f(2) = 9
o: 13, porque hay que sumar el valor de la función y el de la pendiente
a: 1
e: La regla de la potencia da 6x para el primer término y −2 para el segundo, así que f'(x) = 6x − 2 y f'(2) = 10. f(2) = 9 es el valor de la función, no la pendiente; y la derivada no se suma al valor de la función.
:::

:::quiz
p: ¿Por qué la derivada de e^{2x} es 2e^{2x} y no e^{2x}?
o: Porque la regla de la cadena obliga a multiplicar por la derivada de la función interior, que es 2
o: Porque la derivada de la exponencial siempre añade un factor igual al exponente
o: Porque e^{2x} se puede escribir como 2e^{x}
a: 1
e: Al ser una composición f(g(x)) con f = eˣ y g = 2x, su derivada es e^{2x} · 2. La regla de la cadena es general: la derivada de e^{kx} es k·e^{kx}. Las otras dos opciones son falsas: e^{2x} no es 2e^{x}, y la exponencial no genera factores por sí sola.
:::

:::truco
Antes de derivar un cociente, pregúntate si puedes reescribirlo como potencia: `1/x²` es
`x⁻²`, y su derivada es `−2x⁻³`, sin regla del cociente. La mitad de los errores de signo en
una regla del cociente desaparecen reescribiendo primero.
:::
