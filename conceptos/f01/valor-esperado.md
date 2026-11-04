---
id: valor-esperado
titulo: Valor esperado
fase: 1
nivel: básico
rutas: [core, ds, quant]
prerequisitos: [variable-aleatoria, probabilidad-axiomas]
tags: [probabilidad, media, fundamentos]
resumen: La media teórica de una variable aleatoria, por qué se suma tan fácilmente y por qué E[X·Y] no es E[X]·E[Y] salvo que sean independientes.
fuentes: ["Casella y Berger (2002), 'Statistical Inference'", "Ross (2014), 'Introduction to Probability Models'"]
---

## En una frase

El valor esperado es la media que obtendrías si repitieras el experimento infinitas veces:
pondera cada valor posible por la probabilidad de que ocurra.

## La idea

Una aseguradora no sabe si tu casa se va a quemar. Sabe que, entre cien mil clientes como tú,
se queman unas pocas cada año y que la indemnización media por cliente es de 240 €. Con ese
número fija la prima. Nadie sabe qué pasará con tu casa; la empresa solo necesita el promedio
sobre muchísimos casos, y ese promedio es el **valor esperado**.

Tres consecuencias que se aprenden tarde y se olvidan pronto:

1. **No tiene por qué ser un valor posible.** El valor esperado de un dado de seis caras es
   3,5, y nunca sale 3,5. Es un centro de gravedad, no un pronóstico.
2. **Suma de maravilla.** El valor esperado de una suma es siempre la suma de los valores
   esperados: `E[X + Y] = E[X] + E[Y]`, sin pedir independencia ni nada parecido. Por eso se
   pueden sumar los beneficios esperados de diez líneas de negocio y tener el total.
3. **Multiplicar no.** `E[X · Y]` solo es igual a `E[X] · E[Y]` cuando las variables son
   independientes (o, más en general, cuando su covarianza es cero). Si `Y` crece cuando crece
   `X`, el producto esperado es mayor que el producto de las esperanzas, y esa diferencia
   tiene nombre: covarianza, que es el concepto siguiente de esta fase.

La trampa mental es decidir con la esperanza y nada más. Un juego con esperanza positiva puede
arruinarte si la varianza es enorme y no tienes colchón, y una estrategia con esperanza
positiva pequeña puede ser excelente si casi nunca pierde. La esperanza ordena alternativas
solo cuando el riesgo es comparable; para lo demás hacen falta
[[varianza-y-desviacion|la varianza]] y las medidas de riesgo.

## Definición formal

Para una variable aleatoria `X`:

- **Caso discreto:** `E[X] = Σₓ x · p(x)`, donde `p(x) = P(X = x)` es la función de masa y la
  suma recorre todos los valores del soporte.
- **Caso continuo:** `E[X] = ∫ x · f(x) dx`, con `f` la función de densidad, integrando en
  toda la recta real.

En los dos casos `E[X]` es un promedio ponderado por probabilidad, y por eso cumple
`mín(x) ≤ E[X] ≤ máx(x)`. Se usa también la notación `μ` o `μ_X` para la esperanza de `X`.

:::figura
fichero: esperado-centro-y-producto
pie: A la izquierda, la masa de un dado y su centro de gravedad: E[X] = 3,5 cae entre dos barras y no es un valor que el dado pueda dar. A la derecha, la misma variable multiplicada por si misma: la barra gris es E[X] por E[Y] y la azul es E[X por Y]. La diferencia entre las dos, 2,9167, es exactamente la covarianza, que aquí es la varianza del dado.
fuente: figuras/valor-esperado-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `X` | La variable aleatoria cuya media teorica quieres | las de sus valores | Desplazar todos los valores desplaza `E[X]` lo mismo: `E[X + c] = E[X] + c` |
| `x` | Cada valor del soporte por el que suma la formula | las de `X` | Es el índice de la suma, no un mando. Aparece obligatoriamente en el ejemplo: `np.arange(1, 7)` |
| `p(x)` | Función de masa: el peso de cada valor | probabilidad, entre 0 y 1 | Los pesos tienen que sumar 1. Repartirlos de otra forma mantiene `E[X]` acotado entre el mínimo y el maximo de `x` |
| `f(x)` | Función de densidad en el caso continuo | inversa de las unidades de `X` | Desplazar la densidad hacia la derecha sube `E[X]`; ensancharla sin moverla no lo cambia, solo cambia la varianza |
| `E[X]`, `mu` | El valor esperado y su notación habitual | las de `X` | Es el centro de gravedad: siempre cae entre el mínimo y el maximo, y no tiene por qué ser un valor posible (3,5 con un dado) |
| `E[X*Y]` | Media del producto de dos variables | producto de las unidades de las dos | Solo coincide con `E[X] * E[Y]` si la covarianza es cero. Si la dependencia es positiva, `E[X*Y]` es mayor |
| `a`, `b`, `c` | Constantes de la linealidad | las de `X` e `Y` | Escalan y desplazan la esperanza directamente: `E[aX + bY + c] = aE[X] + bE[Y] + c`. No hace falta independencia para esto |
| `g` | Una función cualquiera aplicada a `X` | la que devuelva `g` | Con LOTUS se promedia `g(x)`, no se aplica `g` a la media. Si `g` es convexa, `E[g(X)]` es mayor o igual que `g(E[X])` |
:::

**Propiedades.**

- **Linealidad:** `E[aX + bY + c] = a·E[X] + b·E[Y] + c`, con `a`, `b` y `c` constantes.
  Vale siempre, haya dependencia o no.
- **Producto:** `E[X·Y] = E[X]·E[Y]` si `X` e `Y` son independientes. En general,
  `E[X·Y] − E[X]·E[Y] = Cov(X, Y)`.
- **Función de una variable (LOTUS):** `E[g(X)] = Σₓ g(x)·p(x)` en discreto y
  `E[g(X)] = ∫ g(x)·f(x) dx` en continuo. No es `g(E[X])`: la función se aplica dentro, valor
  a valor, antes de promediar. Para `g(x) = x²` esto da `E[X²] ≥ (E[X])²`.
- **Existencia:** la suma o la integral tienen que converger en valor absoluto. Si no,
  la esperanza no existe, aunque la distribución esté perfectamente definida (le pasa a la
  distribución de Cauchy).

## Ejemplo

**Un dado.** `E[X] = (1 + 2 + 3 + 4 + 5 + 6)/6 = 21/6 = 3,5`.

**Un juego de feria.** Pagas 2 € por tirar un dado y recibes 5 € si sale un 6. Tu beneficio
neto es +3 € con probabilidad 1/6 y −2 € con probabilidad 5/6:

`E[beneficio] = 3 · (1/6) + (−2) · (5/6) = 0,5 − 1,6667 = −1,1667 €`.

Es decir, pierdes 1,17 € por tirada de media, unos 117 € cada cien tiradas. El juego es malo
aunque una de cada seis personas salga contenta de una tirada suelta.

**Linealidad.** Dos juegos distintos con `E[X₁] = 1` y `E[X₂] = 1` dan `E[X₁ + X₂] = 2`
aunque estén correlacionados. La linealidad no pide independencia.

**Producto.** Toma `X` = resultado de un dado e `Y = X`. Entonces
`E[X·Y] = E[X²] = 91/6 = 15,1667`, mientras que `E[X]·E[Y] = 3,5 · 3,5 = 12,25`. La
independencia no se cumple (son la misma variable) y el producto de esperanzas se queda corto.

## Código

```python verificable
import numpy as np

# X es el resultado de un dado; Y = X, asi que son perfectamente dependientes.
x = np.arange(1, 7, dtype=float)
y = x.copy()

print(f"E[X]     = {x.mean():.4f}")               # -> 3.5000
print(f"E[X*Y]   = {(x * y).mean():.4f}")         # -> 15.1667
print(f"E[X]E[Y] = {x.mean() * y.mean():.4f}")    # -> 12.2500

# La linealidad no necesita independencia: se comprueba valor a valor.
print(f"E[3X + 10] = {(3 * x + 10).mean():.4f}")  # -> 20.5000
print(f"3E[X] + 10 = {3 * x.mean() + 10:.4f}")    # -> 20.5000
```
:::claves
- En el primer bloque, `x` es un `np.array` de NumPy, no una lista. `x.mean()` es entonces un método del array y no una función de la libreria estandar: sobre una lista de Python no existe y tendrias que escribir `sum(x) / len(x)`.
- `y = x.copy()` hace una copia **independiente**. Si escribieras `y = x`, las dos variables serian el mismo objeto: cualquier cambio en una apareceria en la otra y el ejemplo perderia el sentido. Se comprueba con `y is x` (da `False` con `copy`) y con `np.shares_memory(x, y)`.
- `(x ** 2).mean()` y `(x * x).mean()` dan lo mismo, pero el orden de las operaciones sí importa: `x ** 2` se calcula elemento a elemento y **antes** de promediar. Escribir `x.mean() ** 2` es otra cosa —12,25 frente a 15,1667— y es justo el error que la página denuncia.
- En el segundo bloque, `probabilidades = np.array([1 / 6, 5 / 6])` usa división con barra. Con `1 // 6` en Python 3 obtendrias `0`, el array entero valdria 0 y la esperanza saldria 0,0000 sin ningun error. Es un fallo silencioso, no una excepción.
- `(beneficios * probabilidades).sum()` multiplica **posición a posición** y luego suma. Funciona porque los dos arrays tienen la misma longitud; con longitudes distintas NumPy lanza un `ValueError` (o emite un aviso si uno mide 1). El orden en que se emparejan los elementos es el del array, no el de tu cabeza.
- `100 * esperado` se imprime con `:.2f`, que redondea a dos decimales al mostrar. Si el resultado fuera a usarse en otro calculo, conviene no redondear nunca en el medio.
:::


```python verificable
import numpy as np

# Juego: pagas 2 EUR, ganas 5 EUR solo si sale un 6.
# Beneficio neto: +3 con probabilidad 1/6, -2 con probabilidad 5/6.
beneficios = np.array([3.0, -2.0])
probabilidades = np.array([1 / 6, 5 / 6])

esperado = (beneficios * probabilidades).sum()
print(f"E[beneficio] por tirada = {esperado:.4f} EUR")        # -> -1.1667
print(f"perdida esperada en 100 tiradas = {100 * esperado:.2f} EUR")  # -> -116.67

# Linealidad: sumar dos juegos independientes suma sus esperanzas.
otro = np.array([0.0, 8.0])
print(f"E[X1 + X2] = {(beneficios * probabilidades).sum() + (otro * np.array([0.9, 0.1])).sum():.4f}")  # -> -0.3667
```

## Errores típicos

- **Confundir valor esperado con valor más probable.** Con un dado, `E[X] = 3,5` y la moda son
  seis valores empatados. La esperanza es un centro de gravedad; la moda, el valor que más sale.
- **Multiplicar esperanzas sin comprobar la independencia.** `E[X·Y] = E[X]·E[Y]` es falso en
  general: con `Y = X`, da 15,1667 frente a 12,25. La diferencia es exactamente `Cov(X, Y)`, y
  en finanzas esa diferencia es casi todo el riesgo de una cartera.
- **Meter la función antes de la esperanza (o al revés).** `E[X²]` no es `(E[X])²`: 15,1667
  frente a 12,25 con un dado. La desigualdad de Jensen dice que para una función convexa,
  `E[g(X)] ≥ g(E[X])`, y la igualdad solo llega si `X` es constante.
- **Decidir solo con la esperanza.** Dos estrategias con el mismo beneficio esperado pueden
  tener riesgos incomparables; sin mirar la dispersión, la esperanza no ordena nada.
- **Creer que la linealidad exige independencia.** `E[X + Y] = E[X] + E[Y]` vale siempre. Lo que
  exige independencia es la varianza de la suma, no la esperanza.
- **Usar el valor esperado cuando no existe.** La media de una distribución de Cauchy no está
  definida, y la de un cociente de variables normales tampoco. Calcular la media muestral de
  esos datos y llamarla esperanza es un error de concepto, no de redondeo.

:::practica
enunciado: Una variable X toma los valores 1, 2 y 5 con probabilidades 0,5, 0,3 y 0,2. Calcula E[X] y E[X²] y comprueba que E[X²] no es (E[X])².
pista: E[X²] se calcula con LOTUS: eleva cada valor al cuadrado antes de ponderar.
solucion: E[X] = 1 · 0,5 + 2 · 0,3 + 5 · 0,2 = 0,5 + 0,6 + 1,0 = 2,1. E[X²] = 1 · 0,5 + 4 · 0,3 + 25 · 0,2 = 0,5 + 1,2 + 5,0 = 6,7. En cambio (E[X])² = 2,1² = 4,41. La diferencia, 2,29, es Var(X), que es positiva porque X no es constante.
:::

## Comprueba que lo sabes

:::quiz
p: Tiras un dado justo de seis caras. ¿Cuál es el valor esperado del resultado?
o: 3, porque es el valor central de la lista
o: 3,5, aunque nunca salga exactamente ese valor
o: 6, porque es el valor máximo posible
a: 2
e: La esperanza es el promedio ponderado por probabilidad: (1+2+3+4+5+6)/6 = 3,5. No tiene por qué ser un resultado posible; es el centro de gravedad de la distribución, no el valor más frecuente.
:::

:::quiz
p: X es el resultado de un dado e Y = X. ¿Cuánto vale E[X·Y]?
o: 12,25, el producto de las esperanzas
o: 15,1667, porque E[X²] = 91/6
o: 21, porque se suman los valores del dado
a: 2
e: Como Y es la misma variable que X, el producto es X², y su esperanza es (1+4+9+16+25+36)/6 = 91/6 = 15,1667. El producto de esperanzas (12,25) solo valdría si X e Y fueran independientes; la diferencia de 2,9167 es la covarianza, que aquí es la varianza de X.
:::

:::quiz
p: Pagas 2 € y ganas 5 € si sale un 6. ¿Qué dice el valor esperado?
o: Que pierdes 1,1667 € de media por tirada, así que el juego no te conviene
o: Que ganas, porque 5 € es más que 2 €
o: Que el juego es neutro, porque 5/6 ≈ 2/2
a: 1
e: El beneficio neto es +3 € con probabilidad 1/6 y −2 € con probabilidad 5/6: E = 0,5 − 1,6667 = −1,1667 €. Que el premio sea mayor que el precio no basta: hay que ponderar por la probabilidad de acertar.
:::
