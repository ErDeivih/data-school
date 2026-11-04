---
id: curva-de-tipos-y-descuento
titulo: Curva de tipos y descuento
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [notacion-matematica, retornos-logaritmicos, varianza-y-desviacion]
tags: [tipos, descuento, valoracion, renta-fija]
resumen: Por qué el tipo de interés depende del plazo, qué es el factor de descuento y cómo un punto de tipos mueve mucho más un bono a diez años que uno a dos.
fuentes: ["Fabozzi (2015), 'Bond Markets, Analysis and Strategies'", "Hull (2018), 'Options, Futures and Other Derivatives'"]
---

## En una frase

La curva de tipos es el tipo de interés para cada plazo, el factor de descuento convierte un euro
futuro en su valor de hoy, y de ahí sale todo lo demás: un punto porcentual de subida mueve un
0,96 % un bono a un año y un 9,21 % uno a diez.

## La idea

Mil euros dentro de un año no valen mil euros hoy. Y mil euros dentro de diez años valen bastante
menos. Lo segundo es lo que casi nadie tiene interiorizado, y es justo lo que decide si una
inversión o un proyecto sale o no sale.

La razón es que el dinero se puede prestar. Si hoy tienes 1.000 € y los prestas a un año al 3 %,
mañana tienes 1.030 €. Al revés: si alguien te promete 1.000 € dentro de un año, hoy te valen
970,87 €, porque 970,87 € colocados al 3 % se convierten exactamente en 1.000 €. Ese «cuánto valen
hoy» es el **descuento**, y el número por el que multiplicas (0,97087) es el **factor de
descuento**.

**Y aquí viene la primera sorpresa: no hay un tipo de interés. Hay uno por plazo.** Mira lo que
paga el mercado por el dinero inmovilizado:

| Plazo | Tipo | Lo que sugiere |
| --- | --- | --- |
| 1 año | 2,50 % | Esperar un año se paga poco |
| 2 años | 2,80 % | Por dos años, algo más |
| 5 años | 3,20 % | Hay que compensar más incertidumbre |
| 10 años | 3,60 % | Diez años sin tocar el dinero tiene su precio |

Esa tabla es una **curva de tipos**: el tipo que el mercado pide hoy para cada plazo. Normalmente
sube, porque prestar a más plazo es más arriesgado (inflación futura, impagos, tipos que se muevan
en tu contra) y por eso exige más compensación. Pero no siempre sube: cuando el mercado espera una
recesión y bajadas de tipos, la curva se **invierte** y el plazo largo paga menos que el corto.

Cuando en las demás páginas de esta fase se habla «del tipo sin riesgo», se está usando una
simplificación cómoda: un solo número para todos los plazos. Funciona bien para ejemplos de
retornos diarios o mensuales, donde el numerito se cancela. **Se rompe en cuanto valoras algo a
varios años**, y ahí es donde aparece el error caro.

**La segunda sorpresa: lo que mueve el precio no es el nivel del tipo, es su cambio multiplicado
por el plazo.** Un tipo que sube del 3 % al 4 % es un punto porcentual, el mismo para todos. Pero
el precio de un pago a un año cae un 0,96 % y el de un pago a diez años cae un 9,21 %. Nueve veces
y media más, con el mismo movimiento de tipos. Esa es la razón por la que la deuda a largo plazo
asusta: no se equivoca más, pero cada error cuesta mucho más.

## Definición formal

**Tipo al contado (spot).** El tipo anual `z_t` que el mercado aplica hoy a un único pago dentro
de `t` años, con capitalización compuesta anual. Se lee de la curva.

**Factor de descuento.** El valor hoy de un euro pagadero dentro de `t` años:

:::formula
DF(t) = 1 / (1 + z_t)^t
:::

Con capitalización semestral (la convención habitual en bonos), el denominador es
`(1 + z_t / 2)^(2t)`; con capitalización continua, `DF(t) = e^(−z_t · t)`. Las tres expresiones son
la misma idea y dan números distintos: **la convención hay que decirla, porque no hay una única
correcta**.

**Valor actual.** Con una lista de flujos `C_1, C_2, …, C_n` en los instantes `t_1, …, t_n`:

:::formula
VA = Σ C_i · DF(t_i)
:::

**Precio de un bono.** Es el caso particular en que los flujos son los cupones y el nominal. Un
bono que paga cupón `c` (en tanto por uno del nominal) y devuelve el nominal `N` a `n` años:

:::formula
P = N · ( Σ c · DF(t_i) + DF(n) )
:::

**Tipo interno de rentabilidad (TIR).** Es el tipo único `y` que hace que el valor actual iguale al
precio de mercado. Es la operación inversa: en vez de descontar con la curva, se busca el tipo que
cuadra el precio.

:::formula
P = Σ C_i / (1 + y)^(t_i)
:::

**Tipo a plazo (forward).** El tipo que el mercado implica entre dos plazos, con los dos tipos al
contado ya conocidos:

:::formula
(1 + f_1,2) = (1 + z_2)^2 / (1 + z_1)
:::

Con `z_1 = 2,50 %` y `z_2 = 2,80 %`: `f = 1,028² / 1,025 − 1 = 3,10 %`. Si el mercado no esperara
ninguna subida, el forward sería igual al tipo a un año; el 3,10 % dice que el mercado ya está
poniendo en precio esa subida.

**Sensibilidad: duración.** Para un bono con cupones, la duración de Macaulay `D` es el plazo medio
ponderado de sus flujos:

:::formula
D = Σ t_i · VA(C_i) / P        y        ΔP / P ≈ − D_mod · Δy        con D_mod = D / (1 + y)
:::

Para un bono cupón cero (un solo pago al final), `D` es exactamente el plazo. Por eso un cero a
10 años con una subida de un punto pierde alrededor de un 9,1 %, y uno a 1 año, un 0,97 %.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `z_t` | Tipo al contado para el plazo `t`: el tipo de un pago único dentro de `t` años | % anual | Sube el `DF(t)` en el denominador, así que el valor actual **baja**. La relación es inversa y no lineal: el mismo punto de subida duele más cuanto mayor es `t` |
| `t` | Plazo hasta el pago, en años | años | Al subir, el descuento es más agresivo y el flujo vale menos. También sube la sensibilidad del precio: el efecto crece más rápido que el plazo |
| `DF(t)` | Factor de descuento: el valor hoy de un euro que se paga dentro de `t` años | adimensional, entre 0 y 1 | Es el multiplicador que convierte flujos futuros en valor de hoy. Con tipos positivos siempre es menor que 1 y baja al alargar `t` |
| `C_i` | Flujo de caja del instante `i`: un cupón, un dividendo, un retorno esperado | dinero | Es el numerador del valor actual: sube el valor en línea recta. Un flujo lejano y grande pesa menos que uno cercano del mismo tamaño |
| `VA` | Valor actual: la suma de los flujos descontados | dinero | Es lo que se compara con el precio. Si el `VA` supera al precio, hay valor; si no, se está pagando de más |
| `y` (TIR) | El tipo único que iguala los flujos descontados con el precio de mercado | % anual | Sube cuando el precio baja. Es un resumen cómodo que **supone reinvertir todos los cupones a ese mismo tipo**, cosa que casi nunca pasa |
| `D_mod` | Duración modificada: cuánto cambia el precio por un punto de tipo | años | Es la sensibilidad. Un bono a 10 años con `D_mod` de 8,6 pierde un 8,6 % por cada punto que suba el tipo; uno a 2 años con `D_mod` de 1,9 pierde un 1,9 % |
| Convención | Cómo se capitaliza: anual, semestral o continua | — | No es un detalle: a 10 años al 6 %, anual da 0,5584 y semestral 0,5537. Un 0,8 % de diferencia en el precio, gratis, por escribir la convención de otra forma |
:::

## Ejemplo

Curva de tipos de contado:

| Plazo | 1 año | 2 años | 5 años | 10 años |
| --- | --- | --- | --- | --- |
| Tipo `z_t` | 2,50 % | 2,80 % | 3,20 % | 3,60 % |

**Precio de un bono a 5 años**, nominal 1.000 €, cupón anual del 3 % (30 €), con la curva:

| Año | Flujo | `z_t` | `DF(t)` | Valor actual |
| --- | --- | --- | --- | --- |
| 1 | 30 € | 2,50 % | 0,9756 | 29,27 € |
| 2 | 30 € | 2,80 % | 0,9463 | 28,39 € |
| 3 | 30 € | 3,00 % | 0,9151 | 27,45 € |
| 4 | 30 € | 3,20 % | 0,8817 | 26,45 € |
| 5 | 1.030 € | 3,60 % | 0,8379 | 863,05 € |
| | | | **Total** | **974,61 €** |

Con un único tipo del 3 % para todo (la simplificación habitual) el resultado sería 1.000,00 €
justo, porque el cupón coincide con el tipo. La curva da **974,61 €**, un **2,6 % menos**: esa
diferencia es el error que se comete al usar un solo tipo en algo que dura cinco años. Y fíjate en
dónde está el peso: el último flujo aporta el 88,6 % del valor, así que el tipo a 5 años manda
mucho más que los otros cuatro.

**El mismo bono con un punto más de tipos.** Si toda la curva sube un punto (1 año al 3,50 %,
5 años al 4,60 %), el valor pasa a 931,53 €: una caída del **4,42 %**. La duración de Macaulay del
bono con la curva es 4,71 años, así que `D_mod = 4,71 / 1,036 = 4,55` y la aproximación
`−4,55 · 1 % = −4,55 %` se queda algo larga frente al −4,42 % real: la duración es una aproximación
lineal de una curva que no lo es ([[convexidad]]). Sirve para saber el orden de magnitud, no para
clavar el precio.

**Y ahora la comparación que importa.** Dos bonos cupón cero, uno a 2 años y otro a 10, con la
subida de un punto en toda la curva:

- El de 2 años: `DF` pasa de 0,9426 a 0,9246, el precio cae de 942,60 € a 924,56 €: **−1,91 %**.
- El de 10 años: `DF` pasa de 0,7441 a 0,6756, el precio cae de 744,09 € a 675,56 €: **−9,21 %**.

Un movimiento idéntico de tipos y muy distinto dolor. Si en vez de una subida de un punto en toda
la curva se moviera solo el extremo corto, el de 10 años casi ni se enteraría: por eso los gestores
no miran «el tipo», miran **qué tramo** de la curva se ha movido.

:::figura
fichero: curva-tipos-y-descuento
pie: Izquierda, la curva de tipos de la tabla: el tipo al contado sube del 2,50 % a un año al 3,60 % a diez, porque prestar más tiempo exige más compensación. El factor de descuento a diez años es 0,7021: un euro de dentro de diez años vale hoy 70 céntimos. Derecha, el mismo punto de subida en toda la curva (del 3 % al 4 %) sobre bonos cupón cero de distintos vencimientos: a un año apenas se nota (0,96 % de caída) y a diez se lleva el 9,21 %, casi diez veces más. A veinte años, el 17,57 %.
fuente: figuras/curva-de-tipos-y-descuento-1.py
:::

## Código

```python verificable
# --- inicio formula 1 ---
# Valorar un bono con la curva entera, no con un tipo unico. La diferencia es el error que se comete.
plazos = [1, 2, 3, 4, 5]
tipos = [0.025, 0.028, 0.030, 0.032, 0.036]   # tipos al contado, uno por plazo
cupon, nominal = 30.0, 1000.0

# Un bono cupon cero tiene un solo flujo al final; con cupones, uno por ano y el nominal en el ultimo.
flujos = [cupon] * (len(plazos) - 1) + [cupon + nominal]
# El factor de descuento se calcula plazo a plazo: exponente entero, no interpolacion.
descuentos = [1 / (1 + z) ** t for t, z in zip(plazos, tipos)]
valores = [c * d for c, d in zip(flujos, descuentos)]
precio_curva = sum(valores)
# Con un unico tipo del 3 % el bono vale exactamente el nominal: el cupon coincide con el tipo.
precio_plano = sum(c / 1.03 ** t for t, c in zip(plazos, flujos))
# --- fin formula 1 ---

for t, z, d, v in zip(plazos, tipos, descuentos, valores):
    print("ano %2d  z %.3f  DF %.4f  VA %8.2f" % (t, z, d, v))
print("precio con la curva:  %.2f" % precio_curva)     # -> 974.61
print("precio con el 3 %%:    %.2f" % precio_plano)     # -> 1000.00
print("error por simplificar: %.2f %%" % (100 * (precio_plano / precio_curva - 1)))  # -> 2.60 %
```

:::claves
- `[cupon] * (len(plazos) - 1) + [cupon + nominal]` construye la lista de flujos: repetir una lista
  con `*` **no copia los elementos**, repite la referencia; con números inmutables da igual, con
  listas dentro sería un problema clásico.
- `zip(plazos, tipos)` empareja las dos listas y se para en la más corta, sin avisar: si te falta
  un tipo, el bono se valora con menos flujos y el precio sale mal **sin dar ningún error**.
- El factor de descuento usa `**t` con `t` entero. Si los plazos fueran años y medio, ese exponente
  tiene que ser fraccionario (1,5) y entonces la convención de capitalización deja de ser un detalle:
  anual, semestral y continua dan números distintos.
- `1 / (1 + z) ** t` lleva el paréntesis alrededor de `1 + z` a propósito. `1 + z ** t` calcula
  primero la potencia y luego suma el 1, y el resultado es un disparate silencioso.
- Los flujos se guardan en una lista y se multiplican por su descuento uno a uno. Vectorizar con
  NumPy sería más rápido, pero con cinco flujos la diferencia es de microsegundos y así se ve de
  dónde sale cada número.
:::

```python verificable
# --- inicio formula 2 ---
# Lo mismo con una subida de un punto en toda la curva: el error no es lineal.
flujos = [30.0, 30.0, 30.0, 30.0, 1030.0]

def precio(tipos, flujos):
    # Descuenta cada flujo con SU tipo: es lo unico que distingue la curva del tipo unico.
    return sum(c / (1 + z) ** (i + 1) for i, (c, z) in enumerate(zip(flujos, tipos)))

base = [0.025, 0.028, 0.030, 0.032, 0.036]
subida = [z + 0.01 for z in base]
# --- fin formula 2 ---

print("antes   %.2f" % precio(base, flujos))    # -> 974.61
print("despues %.2f" % precio(subida, flujos))  # -> 931.53
print("caida   %.2f %%" % (100 * (precio(subida, flujos) / precio(base, flujos) - 1)))  # -> -4.42 %
# La duracion de Macaulay del bono con la curva es 4,71 anos, luego D_mod = 4,55: la aproximacion
# lineal -4,55 % se queda algo larga frente al -4,42 % real. Esa curvatura es la convexidad.
```

```python verificable
# --- inicio formula 3 ---
# Por que el mismo punto de tipos duele ocho veces mas a 10 anos que a 1: el cero.
def cero(z, t):
    # Bono cupon cero a t anos: un unico pago de 1.000 en t. El DF y el precio son lo mismo.
    return 1000.0 / (1 + z) ** t

z_actual, z_nuevo = 0.03, 0.04
for t in (1, 2, 5, 10):
    antes, despues = cero(z_actual, t), cero(z_nuevo, t)
    # El DF se imprime con el tipo viejo: es el valor de hoy de un euro, no del pago de 1.000.
    print("plazo %2d  DF %.4f  precio %8.2f  caida %6.2f %%"
          % (t, 1 / (1 + z_actual) ** t, antes, 100 * (despues / antes - 1)))
# --- fin formula 3 ---
# -> plazo  1  DF 0.9709  precio   970.87  caida  -0.96 %
# -> plazo  2  DF 0.9426  precio   942.60  caida  -1.91 %
# -> plazo  5  DF 0.8626  precio   862.61  caida  -4.72 %
# -> plazo 10  DF 0.7441  precio   744.09  caida  -9.21 %
```

## Errores típicos

- **Usar un único tipo sin riesgo para descontar flujos de plazos distintos.** Es la simplificación
  que se hace en toda esta fase y es cómoda para retornos diarios, pero en cuanto valoras algo a
  cinco o diez años el error es del 2 % o más, y siempre en la misma dirección. Si hay una curva,
  se usa la curva.
- **Confundir descuento con inflación.** Descontar no es «quitar la inflación»: es reconocer que el
  dinero tiene un precio por el paso del tiempo. El tipo nominal ya lleva la inflación esperada
  dentro; el tipo real es el que la descuenta aparte. Y hay tipos negativos, así que el
  razonamiento «el descuento siempre resta» no es una ley física.
- **No decir la convención de capitalización.** Anual, semestral y continua dan números distintos:
  a 10 años y al 6 %, los factores son 0,5584, 0,5537 y 0,5488. Comparar dos precios calculados con
  convenciones distintas es comparar dos cosas que no son la misma.
- **Creer que la duración es una predicción exacta.** `ΔP ≈ −D_mod · Δy` es una aproximación
  lineal. Con un punto de subida se queda corta o larga, y con dos puntos el error se dispara:
  para eso está la convexidad.
- **Olvidar que la sensibilidad crece con el plazo, no con el cupón.** Un bono a 10 años con cupón
  alto cae menos que un cero a 10 años, pero sigue cayendo mucho más que uno a 2 años. Comparar
  «rentabilidad» de bonos de plazos distintos sin mirar la duración es comparar manzanas con peras.
- **Descontar con tipos anuales y flujos mensuales.** Si el flujo está a 6 meses, el exponente es
  0,5 y el tipo tiene que estar en la misma base temporal. Mezclar un tipo anual con un exponente
  en meses convierte un 3 % en un 36 %.
- **Leer la TIR como la rentabilidad que vas a obtener.** La TIR supone que reinviertes todos los
  cupones al mismo tipo hasta el vencimiento. Si los tipos bajan, tu rentabilidad real es menor.
  La TIR sirve para comparar bonos, no para prometer resultados.
- **Dar por hecho que la curva sube.** Se invierte con frecuencia cuando el mercado espera
  recortes de tipos. Una estrategia que asume pendiente positiva se lleva un susto en la primera
  inversión, y encima suele coincidir con recesión y caídas en bolsa
  ([[regimenes-de-mercado]]).

## Comprueba que lo sabes

:::practica
enunciado: Con la curva 1 año 2,50 %, 2 años 2,80 %, 3 años 3,00 %, valora un bono a 3 años con nominal 1.000 € y cupón anual del 4 %. Después repite la valoración suponiendo que los tres flujos se descuentan al 3 % y explica la diferencia. Por último, calcula el tipo a plazo entre el año 1 y el año 2.
pista: El cupón del 4 % es 40 €. El factor de descuento de cada año usa su propio tipo; el tipo a plazo sale de dividir los factores acumulados.
solucion: Flujos: 40, 40 y 1.040. Factores: DF(1) = 1/1,025 = 0,97561; DF(2) = 1/1,028² = 0,94616; DF(3) = 1/1,03³ = 0,91514. Valor actual: 40 · 0,97561 + 40 · 0,94616 + 1.040 · 0,91514 = 39,02 + 37,85 + 951,75 = 1.028,62 €. Con un tipo único del 3 %: 40/1,03 + 40/1,03² + 1.040/1,03³ = 38,83 + 37,70 + 951,66 = 1.028,19 €. La diferencia es de solo 0,43 € (un 0,04 %) porque el cupón (4 %) está por encima de los tipos de la curva (2,5-3 %): el bono cotiza sobre la par y los flujos cercanos pesan poco. Con una curva más empinada o un plazo mayor, la diferencia crecería. Tipo a plazo año 1-2: (1,028² / 1,025) − 1 = 3,10 %.
:::

:::quiz
p: Un bono cupón cero a 10 años y otro a 2 años. Los tipos suben un punto en toda la curva. ¿Cuál cae más y por qué?
o: El de 2 años, porque le queda menos tiempo para recuperarse
o: El de 10 años, porque el descuento se aplica a un plazo mayor y su duración es mayor
o: Caen lo mismo: el movimiento de tipos es el mismo para los dos
a: 2
e: La caída porcentual depende del plazo a través de la duración: en un cupón cero, la duración es el propio plazo. El mismo punto de subida baja el precio un 0,96 % a un año y un 9,21 % a diez. Que el movimiento de tipos sea idéntico no implica que el efecto lo sea: la sensibilidad crece con el plazo.
:::

:::quiz
p: ¿Qué es el factor de descuento de un plazo t?
o: El tipo de interés que se aplica a ese plazo
o: El valor hoy de un euro que se cobra dentro de t años
o: La probabilidad de que el pago se produzca
a: 2
e: El factor de descuento es un multiplicador entre 0 y 1 que trae un euro futuro al presente: a 10 años y al 3,6 % vale 0,8379, o sea que un euro de dentro de diez años vale hoy 84 céntimos. El tipo es el dato de entrada; el factor, el resultado. No tiene nada que ver con la probabilidad de impago, que es otra cosa (el riesgo de crédito).
:::

:::quiz
p: Al valorar un bono a 5 años, ¿qué pasa si usas un único tipo del 3 % en vez de la curva de la página?
o: El precio sale 974,61 €, igual que con la curva
o: El precio sale 1.000,00 €, un 2,6 % más alto que con la curva
o: El precio sale más bajo, porque la curva tiene tipos más altos
a: 2
e: Con un tipo único igual al cupón (3 %), el bono vale exactamente el nominal: 1.000 €. Con la curva, que arranca en el 2,50 % y sube hasta el 3,60 %, el precio baja a 974,61 €. El error de simplificar es del 2,6 % en un bono a cinco años y siempre en la misma dirección si la curva es creciente.
:::

:::trampa
Una rentabilidad prometida de un bono se calcula con la TIR, y la TIR supone que reinviertes cada
cupón al mismo tipo hasta el vencimiento. Si los tipos bajan, tu rentabilidad real será menor que
la prometida, y si suben, mayor. Cuando veas «rentabilidad al vencimiento del 5 %», pregúntate con
qué tipos se reinvierten los cupones; la respuesta honesta es «con los que haya entonces».
:::

:::nota
En la práctica, la curva que se usa no es la de tipos de contado sino la de los bonos que cotizan,
y de ahí hay que **extraer** los tipos al contado. Eso se hace con un ajuste (Nelson-Siegel, splines)
y cada método da una curva ligeramente distinta. Es la razón de que dos mesas de un mismo banco
puedan valorar el mismo bono con cifras que difieren en céntimos, y no es un error de nadie: es que
la curva es una estimación, no un dato.
:::
