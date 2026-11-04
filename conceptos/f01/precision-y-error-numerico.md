---
id: precision-y-error-numerico
titulo: Precisión y error numérico
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [notacion-matematica]
tags: [numerico, floats, redondeo, dinero]
resumen: Los números con decimales no se guardan exactos, así que 0,1 + 0,2 no da 0,3. Por eso se compara con tolerancia, se acumula con cuidado y el dinero se lleva en Decimal.
fuentes: ["Goldberg (1991), 'What Every Computer Scientist Should Know About Floating-Point Arithmetic'", "Higham (2002), 'Accuracy and Stability of Numerical Algorithms'"]
---

## En una frase

Un ordenador guarda los decimales en binario y con un número fijo de cifras, así que casi ninguno
es exacto: `0.1 + 0.2` no da `0.3`. Compara con tolerancia, no acumules a lo bruto y lleva el dinero
en `Decimal`.

## La idea

Coge una calculadora de diez dígitos y escribe 1/3: sale 0,3333333333, que no es un tercio. Multiplica
por 3 y te da 0,9999999999, no 1. El error no es un fallo de la calculadora: es que un tercio no
cabe en diez cifras decimales, y en algún sitio hay que cortar.

En un ordenador pasa lo mismo, con una diferencia que sorprende a todo el mundo: **corta en base
2, no en base 10**. Un `float` de doble precisión guarda 64 bits, de los que 53 son de mantisa, es
decir unas 15 o 17 cifras decimales significativas. El número 0,1 en binario es una fracción
periódica infinita (0,00011001100110011…), así que se guarda con un pelín de más o de menos. Y como
todos los números que escribes con decimales pasan por ese recorte, el error está ahí desde el
principio, no aparece después.

Lo que se deduce de eso, y que hay que tener presente en cada cálculo:

1. **Comparar con `==` no sirve.** `0.1 + 0.2 == 0.3` es falso. Dos caminos distintos para el mismo
   número casi nunca dan el mismo bit. Se compara con una tolerancia que decidas tú.
2. **El error se acumula al sumar.** Cada suma redondea al flotante más cercano, y si sumas muchos
   valores pequeños el error crece. El gráfico de la figura lo enseña: sumando 0,1 cien mil veces,
   el error absoluto llega a 1,9 · 10⁻⁸.
3. **El hueco entre números no es constante.** Alrededor de 1 es 2,22 · 10⁻¹⁶, pero alrededor de
   10¹⁶ vale 2: por encima de 2⁵³ = 9.007.199.254.740.992 los enteros van de dos en dos y sumar 1
   no cambia nada. No es un redondeo agresivo: ese número no existe en la recta de los `float`.
4. **Restar dos números casi iguales destroza la precisión.** Si dos medidas valen 1,000000001 y
   1,000000000, su diferencia arrastra el error de las dos. Calcular la varianza con la fórmula
   `E[X²] − E[X]²` es el ejemplo clásico: con datos grandes y poco dispersos puede dar un número
   negativo.

¿Y el dinero? Un céntimo sobre mil euros es una cifra que se tiene que poder leer y repetir, así que
los importes se llevan en `Decimal` (que guarda los decimales que le escribes, siempre que se los
pases como texto) o en céntimos enteros, con un modo de redondeo elegido a propósito. El `round()`
de Python no redondea como se enseña en el colegio: mira el binario que hay debajo, y además
desempata hacia el número par. Su sitio es presentar un resultado, no calcular lo que se factura.
Para analizar, `float` está bien y se redondea al final; lo que no se hace nunca es redondear en
cada paso.

:::figura
fichero: precision-error-al-sumar
pie: Izquierda: el error absoluto de ir sumando 0,1 una y otra vez, en escala logarítmica. Crece con el número de sumandos y la línea roja marca el hueco entre 1 y el número siguiente (2⁻⁵²); los saltos hacia abajo son los cambios de exponente, donde el resultado se recoloca. Derecha: el hueco entre dos números representables se duplica con cada exponente, así que a partir de 2⁵³ = 9,0 · 10¹⁵ los enteros van de dos en dos y sumar 1 no cambia nada.
fuente: figuras/precision-y-error-numerico-1.py
:::

## Definición formal

El error de una operación se mide de dos formas. Con `x` el valor exacto y `x̂` el que has calculado:

:::formula
error_absoluto = /x − x̂/          error_relativo = /x − x̂/ ÷ /x/
:::

(donde `/z/` es el valor absoluto de `z`). El absoluto se mide en las unidades del dato; el relativo
es adimensional, y es el que sirve para comparar precisiones.

El límite de precisión de la doble precisión es el **épsilon de máquina**:

:::formula
ε = 2⁻⁵² ≈ 2,22 · 10⁻¹⁶
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `ε` | Épsilon de máquina: el hueco entre 1 y el siguiente número representable | adimensional | Cada operación puede dejar un error del orden de `ε` por el tamaño del resultado |
| `x` | El valor exacto, el que daría la aritmética de papel | las de la variable | Es la referencia; si no puedes calcularlo, usa una tolerancia y di por qué |
| `x̂` | El valor que calculas, con sus redondeos | las de la variable | Es lo que tienes de verdad: la diferencia con `x` es tu error |
| `error_absoluto` | Cuánto te desvías, en las unidades del dato | las de la variable | Con magnitudes grandes crece aunque la precisión relativa no empeore |
| `error_relativo` | El error dividido entre el valor | adimensional, o en % | Es el que decide si el error importa: 1 euro sobre 10 es mucho, sobre un millón nada |
| `tol` | La tolerancia con la que declaras dos números iguales | las de la variable o adimensional | Si la subes demasiado, cualquier par de números se vuelve «igual»: hay que justificarla |
:::

## Ejemplo

Cuatro comprobaciones con números pequeños, todas ejecutables a mano:

- `0,1 + 0,2` da **0,30000000000000004**. El error absoluto es 5,55 · 10⁻¹⁷: invisible en un
  informe y letal en una comparación con `==`.
- Sumar 0,1 diez veces con un bucle da **0,9999999999999999** en lugar de 1. El error absoluto es
  1,11 · 10⁻¹⁶, justo medio épsilon. En una cifra sola no importa nada; el mecanismo que lo produce
  es el mismo que desvía la suma de cien mil valores en 1,9 · 10⁻⁸.
- `1e16 + 1 == 1e16` es **True**. A esa altura el hueco entre números es 2, así que el 1 cae en
  tierra de nadie y se pierde. Es el motivo de que sumar cantidades muy distintas pida otro método.
- Tres líneas de factura de 0,1, 0,2 y 0,3 € suman en `float` **0,6000000000000001**, y
  `round(2.675, 2)` da **2,67** en vez de 2,68. Para facturar eso no es aceptable; para analizar,
  da igual.

## Código

```python verificable
import math

# La suma mas famosa de la informatica: 0,1 y 0,2 no se guardan exactos, y el
# resultado se redondea al flotante mas cercano.
print(f"0.1 + 0.2          {0.1 + 0.2}")            # -> 0.30000000000000004
print(f"igual que 0.3      {0.1 + 0.2 == 0.3}")     # -> False
print(f"diferencia         {0.1 + 0.2 - 0.3:.2e}")  # -> 5.55e-17
print(f"con tolerancia     {math.isclose(0.1 + 0.2, 0.3)}")   # -> True
print(f"epsilon maquina    {2.0 ** -52:.2e}")       # -> 2.22e-16
```

```python verificable
import math

# Acumular en un float: cada suma vuelve a redondear sobre un total que crece.
acumulado = 0.0
for _ in range(10):
    acumulado += 0.1
print(f"diez veces 0,1     {acumulado}")            # -> 0.9999999999999999
print(f"error absoluto     {acumulado - 1.0:.2e}")  # -> -1.11e-16

# Con magnitudes muy distintas, el sumando pequeno desaparece sin avisar.
ingenuo = 0.0
for valor in [1e16] + [1.0] * 10:
    ingenuo += valor
print(f"suma ingenua       {ingenuo:.0f}")          # -> 10000000000000000
print(f"math.fsum          {math.fsum([1e16] + [1.0] * 10):.0f}")   # -> 10000000000000010
```

```python verificable
from decimal import Decimal, ROUND_HALF_UP

# round() trabaja sobre el binario de debajo y desempata hacia el numero par:
# 2,675 se guarda como 2,67499..., y 0,5 queda justo en medio.
print(f"round(2.675, 2)     {round(2.675, 2)}")      # -> 2.67
print(f"round(0.5) round(1.5)  {round(0.5)} {round(1.5)}")   # -> 0 2

# Decimal respeta los decimales que le escribes y deja elegir el redondeo.
factura = Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(f"Decimal HALF_UP     {factura}")               # -> 2.68

# Tres lineas de factura tampoco suman exacto en coma flotante.
total = 0.0
for precio in [0.1, 0.2, 0.3]:
    total += precio
print(f"total en float      {total}")                 # -> 0.6000000000000001
print(f"total en Decimal    {sum(Decimal(str(p)) for p in [0.1, 0.2, 0.3])}")   # -> 0.6
```

:::claves
- `0.1 + 0.2 == 0.3` es `False` en cualquier lenguaje que use el estándar IEEE 754 de doble
  precisión. No es un fallo de Python y no se arregla con otra librería de cálculo básico.
- `math.isclose(a, b)` compara con `rel_tol=1e-09` por defecto, mientras que `np.isclose` usa
  `rtol=1e-05` y `atol=1e-08`. Dos funciones con el mismo nombre y criterios distintos: elige la
  tuya y escribe la tolerancia a mano.
- `round()` de Python redondea al par más cercano y opera sobre el binario: `round(2.675, 2)` da
  2.67 y `round(2.5)` da 2. Sirve para presentar, no para facturar.
- `Decimal(0.1)` no arregla nada: guarda el binario completo del `float`
  (0,1000000000000000055511151231257827…). Hay que construirlo desde texto, `Decimal("0.1")`.
- `math.fsum` redondea una sola vez al final, así que da el resultado más cercano posible; el bucle
  a mano va redondeando en cada paso. `sum()` incorpora una compensación parecida desde Python 3.12.
- `np.float32` tiene 24 bits de mantisa (unas 7 cifras) y `np.float64` los mismos 53 que el `float`
  de Python. Acumular en `float32` ahorra memoria y pierde precisión mucho antes.
:::

## Errores típicos

- **Comparar `float` con `==`, sobre todo en pruebas.** `assert precio == 0.3` falla sin que nada
  esté mal. Usa `math.isclose` o `pytest.approx` y escribe la tolerancia que aceptas.
- **Redondear en cada paso de un cálculo.** El error de cada redondeo se suma al siguiente y el
  resultado final puede desviarse mucho. Redondea una vez, al presentar.
- **Llevar dinero en `float`.** Los importes se facturan y se repiten: van en `Decimal` o en
  céntimos enteros, con el modo de redondeo elegido y escrito.
- **Calcular la varianza como `E[X²] − E[X]²` con números grandes.** Es una resta de dos cantidades
  casi iguales, y la cancelación se come las cifras buenas. Usa `np.var` o el método de dos pasadas.
- **Creer que `round()` redondea como en el colegio.** `round(2.675, 2)` da 2.67, y `round(0.5)` da
  0. Si el redondeo tiene consecuencias legales o contables, hay que decirlo explícitamente.
- **Confundir precisión con exactitud.** Un número con quince decimales puede estar mal: la
  precisión dice cuántas cifras arrastras, no si son las correctas. Es la diferencia entre medir con
  una balanza fina y medir la cosa equivocada.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué `0.1 + 0.2` no da exactamente `0.3`?
o: Porque Python tiene un error de redondeo en la suma de decimales
o: Porque 0,1 y 0,2 no tienen representación exacta en binario, y la suma se redondea al flotante más cercano
o: Porque 0,3 tampoco se puede representar y el resultado se queda sin redondear
a: 2
e: El problema está en la representación: en base 2, 0,1 es una fracción periódica infinita que se corta al guardarla. La suma de dos valores ya redondeados vuelve a redondearse, y el resultado cae a un bit de 0,3. No es un error de Python: pasa igual en cualquier lenguaje con doble precisión IEEE 754.
:::

:::quiz
p: En una prueba automática quieres comprobar que un cálculo da 0,3. ¿Qué escribes?
o: `assert resultado == 0.3`
o: `assert math.isclose(resultado, 0.3, rel_tol=1e-09)`, fijando la tolerancia que aceptas
o: `assert str(resultado) == "0.3"`
a: 2
e: La comparación exacta falla por un bit de diferencia y el texto puede cambiar de formato con la versión. La comparación con tolerancia es la que expresa lo que quieres: «se parecen lo suficiente», con el margen escrito en el código y no escondido.
:::

:::practica
enunciado: Suma 10.000 importes de 0,01 € con un bucle en `float`. ¿Cuánto se desvía del valor exacto, que son 100,00 €? Compruébalo también con `math.fsum` y con `Decimal`, y decide qué usarías para facturar.
pista: Escribe el bucle a mano, sin `sum()`, para ver el efecto de ir acumulando; y compara con el valor exacto antes de redondear nada.
solucion: El bucle a mano da 100,00000000001425, es decir 1,425 · 10⁻¹¹ € de más (unas catorce billonésimas de céntimo). `math.fsum([0.01] * 10000)` da 100.0 exacto, y sumar `Decimal("0.01")` diez mil veces da 100.00. Para facturar, `Decimal` (o céntimos enteros) con el modo de redondeo escrito; para analizar, `float` con `fsum` cuando la precisión importe, redondeando solo al presentar. El error de esta suma es diminuto, pero el mismo mecanismo con millones de operaciones deja de serlo.
:::

:::trampa
El error no se ve porque casi nunca importa: 1,9 · 10⁻⁸ sobre una suma de 10.000 es invisible. Se
vuelve visible de golpe en tres sitios: al comparar con `==`, al facturar céntimos y al restar dos
números casi iguales. Si tu código hace alguna de las tres cosas, la tolerancia y el redondeo tienen
que estar escritos, no supuestos.
:::
