---
id: tamano-de-posicion
titulo: Tamaño de posición
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [volatilidad-realizada, criterio-de-kelly, riesgo-de-ruina]
tags: [posicion, volatilidad, riesgo, cartera]
resumen: Cuantas unidades abres por idea: riesgo fijo, volatilidad objetivo y límites por correlación, la decisión que convierte una señal en resultados.
fuentes: ["Vince (1990), 'Portfolio Management Formulas'", "Thorp (1997), 'The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market'"]
---

## En una frase

El tamaño de posición decide cuántas unidades abres por idea, y es la palanca que convierte una
señal con ventaja en una cuenta que crece o en una cuenta que desaparece: la dirección la pone
el sistema, el tamaño lo pones tú.

## La idea

Una señal te dice si comprar o vender. No te dice cuánto. Y esa segunda decisión tiene más
impacto sobre el resultado que la primera: dos personas con exactamente el mismo sistema, las
mismas entradas y las mismas salidas, pueden acabar una con el doble de capital y la otra
fuera del mercado. Lo único que las diferencia es cuánto arriesgaban en cada operación.

Hay tres familias de métodos y conviene conocer las tres:

**Riesgo fijo por operación.** Decides que si salta el stop pierdes como mucho un `r` por ciento
del capital (típicamente entre el 0,5 % y el 2 %) y calculas las unidades a partir de la
distancia al stop. Es el método más extendido porque hace que todas las operaciones pesen lo
mismo en tu cuenta. Pero tiene un efecto secundario que casi nadie tiene presente: **controla el
riesgo, no la exposición**. El mismo 1 % de riesgo con un stop al 2 % compra el doble de
nocional que con un stop al 4 %. Tu apalancamiento lo decide la distancia al stop, no tu
convicción.

**Volatilidad objetivo (vol targeting).** En vez de igualar el riesgo teórico de cada operación,
igualas la volatilidad que cada posición aporta a la cartera: `peso = volatilidad objetivo /
volatilidad del activo`. Un activo que se mueve un 30 % anual recibe la mitad de peso que uno
que se mueve un 15 %. Así, un día malo de cualquiera de los dos te cuesta parecido.

**Kelly fraccional.** Calculas la fracción de [[criterio-de-kelly]] y usas la mitad o un cuarto.
Es el puente entre la teoría (¿cuánto maximiza el crecimiento?) y la práctica (¿cuánto puedo
estimar de verdad?).

A cualquiera de los tres hay que añadirle la pieza que falta: **los límites**. Una posición
individual nunca debería poder arruinarte (tope por activo), y diez posiciones que se mueven
juntas no son diez apuestas (tope por bloque correlacionado). La diversificación no la decide el
número de posiciones, la decide la correlación entre ellas.

## Definición formal

**Riesgo fijo.** Sea `C` el capital de la cuenta, `r` la fracción de capital que aceptas perder
si salta el stop, `P_entrada` el precio de entrada, `P_stop` el precio del stop y `v` el valor
monetario de un punto de movimiento por unidad. El número de unidades `Q` es:

:::formula
Q = (C · r) / ( |P_entrada − P_stop| · v )
:::

- `C` — capital actual de la cuenta.
- `r` — riesgo por operación en tanto por uno (0,01 es un 1 %).
- `P_entrada`, `P_stop` — precios de entrada y de stop.
- `v` — valor de un punto por unidad (1 para acciones, el multiplicador del contrato para
  futuros y CFDs).
- `Q` — número de unidades o contratos.

De ahí salen dos cantidades que conviene vigilar siempre:

:::formula
Nocional = Q · P_entrada          Apalancamiento = Nocional / C
:::

**Volatilidad objetivo.** Si quieres que la posición aporte una volatilidad `σ_obj` y el activo
tiene volatilidad `σ_i` (ambas anualizadas y en la misma escala):

:::formula
peso_i = σ_obj / σ_i
:::

**Volatilidad de la cartera.** Con `N` posiciones del mismo tamaño, todas con volatilidad `σ` y
correlación media por pares `ρ`:

:::formula
σ_p = σ · √( 1/N + ρ · (N − 1) / N )
:::

- `σ` — volatilidad anualizada de cada posición.
- `ρ` — correlación media entre todos los pares de posiciones.
- `N` — número de posiciones.

Esta fórmula es la que explica por qué diversificar tiene un límite: cuando `N` crece, el primer
término desaparece y queda `σ · √ρ`. Con `ρ = 0,7`, por muchas posiciones que añadas la
volatilidad de la cartera no baja del 84 % de la de una sola posición.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `C` | Capital actual de la cuenta | euros | Es el numerador del riesgo en euros: doblar la cuenta dobla el tamaño de cada posición si mantienes el mismo `r`. Y cambia solo: el capital de hoy no es el de la operación anterior |
| `r` | Riesgo por operación: lo que aceptas perder si salta el stop | tanto por uno (0,01 es un 1 %) | Es la palanca que gobierna el riesgo de ruina, y en la fórmula es lineal. Pasar del 1 % al 2 % no cambia el número de unidades por dos: cambia el riesgo asumido, que es otra cosa |
| `P_entrada`, `P_stop` | Precios de entrada y de stop | euros por unidad | Lo que importa es la **distancia** entre los dos, no el nivel. Acercar el stop reduce la distancia y multiplica las unidades: con el mismo 1 % de riesgo, el nocional se dispara |
| `v` | Valor monetario de un punto de movimiento por unidad | euros por punto y unidad | Vale 1 en acciones y el multiplicador del contrato en futuros y CFD. Olvidarlo en un futuro multiplica o divide el tamaño por el multiplicador, y el riesgo real deja de ser el que creías |
| `Q` | Número de unidades o contratos que abres | unidades o contratos | Sale con decimales y el mercado exige lotes enteros. Redondear hacia arriba cambia el riesgo real más de lo que lo cambia cualquier ajuste fino del modelo |
| `Nocional` | `Q · P_entrada`: el valor de mercado de la posición | euros | Es la exposición, no el riesgo. Con el mismo 1 % de riesgo, un stop lejano da la mitad de nocional y un stop cercano el doble: el apalancamiento lo decide la distancia al stop |
| `Apalancamiento` | `Nocional / C`: cuántas veces tu capital está en el mercado | veces | Es lo que convierte un hueco de apertura en una pérdida mayor que la prevista. El stop puede saltarse y cuanto mayor sea el nocional, más duele |
| `σ_obj` | Volatilidad que quieres que aporte cada posición | anualizada, tanto por uno | Sube el peso de todos los activos por igual: es una decisión de riesgo de cartera, no de convicción sobre un activo concreto |
| `σ_i` | Volatilidad del activo `i` | anualizada, tanto por uno | Entra en el denominador del peso: un activo que se mueve el doble recibe la mitad de peso. Estimarla con una ventana tranquila deja el riesgo real al doble de lo que crees |
| `ρ` | Correlación media entre todos los pares de posiciones | adimensional, entre −1 y 1 | Es el suelo de la diversificación: con `N` grande la volatilidad tiende a `σ·√ρ`. Con `ρ = 0,7` ese suelo es el 84 % de la volatilidad de una sola posición, y por muchas que añadas no baja de ahí |
:::

## Ejemplo

Cuenta de 50.000 €, riesgo del 1 % por idea (500 €) y entrada a 100 €:

| Stop | Unidades | Nocional | Apalancamiento |
| --- | --- | --- | --- |
| 98 € (−2 %) | 250 | 25.000 € | 50 % |
| 96 € (−4 %) | 125 | 12.500 € | 25 % |
| 90 € (−10 %) | 50 | 5.000 € | 10 % |

Los tres casos arriesgan lo mismo si el stop se respeta: 500 €, el 1 %. Pero el primero compra
cinco veces más que el tercero. Y recuerda que los stops se saltan: un hueco de apertura puede
hacer que la pérdida real sea bastante mayor que el 1 % previsto, y cuanto mayor sea el
nocional, más duele ese hueco.

**Volatilidad objetivo.** Si tu objetivo es una volatilidad del 12 % anual:

- Un activo con un 30 % de volatilidad recibe un peso de 12/30 = **0,40**.
- Un activo con un 15 % recibe 12/15 = **0,80**.

Ahora la parte incómoda. Cartera con 10 posiciones iguales, cada una con un 25 % de volatilidad
anual, y distintos niveles de correlación media:

| N | ρ = 0,0 | ρ = 0,3 | ρ = 0,7 |
| --- | --- | --- | --- |
| 1 | 25,00 % | 25,00 % | 25,00 % |
| 5 | 11,18 % | 16,58 % | 21,79 % |
| 10 | 7,91 % | 15,21 % | 21,36 % |
| 20 | 5,59 % | 14,47 % | 21,14 % |

Con correlación cero, pasar de 1 a 20 posiciones baja la volatilidad de la cartera del 25 % al
5,59 %: diversificación de verdad. Con correlación 0,7, pasar de 5 a 20 posiciones apenas mueve
la aguja (del 21,79 % al 21,14 %). En la práctica, cuando el mercado se pone feo, las
correlaciones suben hacia 1 y la diversificación que creías tener desaparece justo cuando la
necesitas.

:::figura
fichero: posicion-riesgo-fijo-y-correlacion
pie: A la izquierda, la cuenta de 50.000 € con un 1 % de riesgo: la línea roja es lo que arriesgas (500 €) y es idéntica en las tres columnas, pero el nocional comprado pasa del 50 % al 25 % y al 10 % solo por mover el stop del 2 % al 4 % y al 10 %. La primera operación compra cinco veces más que la tercera sin arriesgar un euro más: **el riesgo lo pones tú, la exposición la pone la distancia al stop**. A la derecha, la volatilidad de una cartera de posiciones iguales según cuántas tengas y cuánto se muevan juntas: con correlación 0 baja del 25 % al 5,59 % al pasar de 1 a 20 posiciones, mientras que con correlación 0,7 se queda en el 20,92 % y añadir posiciones ya no sirve de nada. Las rayas de puntos son esos suelos, `σ·√ρ`, el techo real de la diversificación.
fuente: figuras/tamano-de-posicion-1.py
:::

## Código

```python verificable
capital, riesgo = 50_000.0, 0.01        # 50 000 EUR y 1 % de riesgo por idea
entrada = 100.0

print(f"riesgo en euros {capital * riesgo:.0f}")     # -> riesgo en euros 500
for stop in (98.0, 96.0, 90.0):
    titulos = (capital * riesgo) / (entrada - stop)
    nocional = titulos * entrada
    print(f"stop {stop:>5.1f}  titulos {titulos:>6.1f}  nocional {nocional:>8.0f}  {nocional / capital:>6.1%}")
# -> stop  98.0  titulos  250.0  nocional    25000   50.0%
# -> stop  90.0  titulos   50.0  nocional     5000   10.0%
```

:::claves
- `entrada - stop` está en euros por título, no en porcentaje. La fórmula divide el riesgo en euros entre esa distancia, así que restar dos porcentajes da un número de títulos absurdo (2 en vez de 250) sin lanzar ningún error. El `v` de la fórmula vale 1 aquí porque son acciones; en un futuro hay que multiplicar la distancia por el multiplicador del contrato.
- El numerador `capital * riesgo` es el mismo en las tres vueltas del bucle: los 500 € no cambian. Lo único que cambia es el divisor, y por eso el nocional pasa del 50 % al 10 %. Es la comprobación rápida de que has entendido la diferencia entre riesgo y exposición.
- `titulos` sale con decimales (62,5 en el ejemplo de la página). El mercado exige lotes enteros, así que el número que de verdad abres no es el que calcula la fórmula: redondear hacia arriba sube el riesgo real, y con cuentas pequeñas ese redondeo pesa más que cualquier ajuste del modelo.
- La función no comprueba que el stop esté por debajo de la entrada. Si lo pones por encima (una posición corta), la distancia sale negativa y el número de títulos también, sin ningún aviso: el resultado es un tamaño con el signo cambiado, que es justo lo contrario de lo que querías.
- `{nocional / capital:>6.1%}` ya multiplica por 100: el `%` del formato lo hace. La trampa clásica es escribir `100 * nocional / capital` con `%`, que imprime 5000 %.
- `capital` es un `float` porque se escribió `50_000.0`. Con `50_000` a secas el riesgo en euros seguiría siendo decimal, pero cualquier división entera posterior cambiaría de resultado según la versión de Python y el tipo de los operandos.
:::

```python verificable
import numpy as np

# Volatilidad de una cartera con N posiciones iguales, volatilidad sigma y
# correlacion media rho entre todos los pares.
sigma = 0.25
print("  N     rho=0.0    rho=0.3    rho=0.7")
for n in (1, 5, 10, 20):
    fila = [sigma * np.sqrt(1 / n + rho * (n - 1) / n) for rho in (0.0, 0.3, 0.7)]
    print(f"{n:>3}  " + "  ".join(f"{v:>9.2%}" for v in fila))
# ->   1     25.00%     25.00%     25.00%
# ->  10      7.91%     15.21%     21.36%
```

```python ilustrativo
import pandas as pd

# Volatilidad objetivo sobre datos reales: se estima la volatilidad de cada activo
# con una ventana movil y se reparte el riesgo en consecuencia.
precios = pd.read_parquet("precios_diarios.parquet")       # datos externos
retornos = precios.pct_change()

vol_anual = retornos.rolling(60).std() * (252 ** 0.5)      # ventana de 60 dias
vol_objetivo = 0.10

# Nunca conviene recalcular el peso a diario: cada ajuste cuesta comision y slippage.
pesos = (vol_objetivo / vol_anual).clip(upper=1.0).iloc[-1]
pesos = pesos / pesos.sum()
print(pesos.round(3))
```

## Errores típicos

- **Confundir riesgo con tamaño.** «Arriesgo un 1 % en todas las operaciones» no significa que
  todas las posiciones sean iguales: con stops lejanos abres posiciones mucho mayores. Si dos
  ideas tienen stops de distinta amplitud, el riesgo es el mismo y la exposición no.
- **Fijar el tamaño en euros y olvidar la volatilidad.** Comprar siempre 10.000 € del activo que
  sea mezcla un activo que se mueve un 5 % con otro que se mueve un 60 %. El segundo domina
  todos los resultados de la cartera.
- **Tratar posiciones correlacionadas como independientes.** Diez acciones de bancos no son diez
  apuestas, son una apuesta con diez nombres. Necesitas un tope por bloque correlacionado,
  además del tope por activo.
- **Recalcular el tamaño constantemente.** Ajustar el peso cada día multiplica las comisiones y
  el deslizamiento ([[slippage-y-comisiones]]) para capturar una mejora de riesgo mínima. Fija
  una frecuencia de reajuste y respétala. Y cuidado con los mínimos operativos: la fórmula puede
  dar 137 acciones y tu mercado exigir múltiplos de 100, así que con cuentas pequeñas el redondeo
  cambia el riesgo real de cada operación mucho más que el ajuste fino del modelo.
- **Subir el tamaño cuando la idea te gusta más.** Ese es el error que más caro sale: el exceso
  de confianza se concentra justo en las operaciones peor analizadas. Si el sistema dice 1 %,
  son 1 %.
- **Medir la volatilidad con datos de un régimen tranquilo.** Una ventana de 60 días en un
  mercado en calma estima la mitad de la volatilidad real de la siguiente crisis, así que tu
  «volatilidad objetivo» te deja con el doble de riesgo del que crees.

:::practica
enunciado: Tienes 25.000 € y arriesgas el 0,8 % por idea. Entras a 40 € con el stop en 38 € y en otro valor con el stop en 36,80 €. Calcula las unidades, el nocional y el apalancamiento de cada caso.
pista: Primero el riesgo en euros; después divide entre la distancia al stop.
solucion: El riesgo es 25.000 · 0,008 = 200 €. Con el stop a 38 € la distancia es 2 €: Q = 200 / 2 = 100 unidades, nocional 4.000 €, un 16 % del capital. Con el stop a 36,80 € la distancia es 3,20 €: Q = 200 / 3,20 = 62,5 unidades, nocional 2.500 €, un 10 %. Los dos pierden 200 € si salta el stop, pero el primero compra un 60 % más: el riesgo es idéntico y la exposición no.
:::

## Comprueba que lo sabes

:::quiz
p: Con 50.000 € de capital y un 1 % de riesgo por operación, ¿qué pasa si mueves el stop del 4 % al 2 % de distancia de la entrada?
o: El número de unidades se reduce a la mitad
o: El número de unidades se duplica y el nocional pasa del 25 % al 50 % del capital
o: No cambia nada, porque el riesgo sigue siendo el 1 %
a: 2
e: La cantidad arriesgada es fija (500 €), así que al reducir a la mitad la distancia al stop necesitas el doble de unidades: 125 pasan a 250 y el nocional sube de 12.500 € a 25.000 €. El riesgo sigue siendo el 1 %, pero la exposición se ha duplicado.
:::

:::quiz
p: Tienes 20 posiciones de la misma volatilidad con una correlación media de 0,7. ¿Por qué la volatilidad de la cartera no baja mucho respecto a tener solo 5?
o: Porque la fórmula tiende a σ·√ρ cuando N crece, y con ρ = 0,7 ese suelo es el 84 % de la volatilidad de una sola posición
o: Porque veinte posiciones siempre tienen más volatilidad que cinco
o: Porque la correlación no influye en la volatilidad de la cartera
a: 1
e: En σ_p = σ·√(1/N + ρ(N−1)/N), al crecer N el primer término desaparece y queda σ·√ρ. Con ρ = 0,7 eso es 0,837·σ. Pasar de 5 a 20 posiciones lleva la volatilidad del 21,79 % al 21,14 %: casi nada. La correlación es el límite real de la diversificación.
:::

:::quiz
p: ¿Para qué sirve un tope por bloque correlacionado y no solo un tope por activo?
o: Para limitar el riesgo agregado de posiciones que en la práctica son la misma apuesta
o: Para pagar menos comisiones
o: Para poder abrir más posiciones del mismo sector sin pasarse del límite por activo
a: 1
e: El tope por activo evita que una sola posición te arruine; el tope por bloque evita que diez posiciones que se mueven juntas sumen, de hecho, una posición enorme. Los dos son necesarios y miden cosas distintas.
:::

:::aviso
Cualquier método de tamaño asume que el stop se ejecuta en el precio previsto. En un hueco de
apertura o en un activo poco líquido, la pérdida real puede ser dos o tres veces la prevista.
Cuanto mayor sea el nocional, más se nota esa diferencia, y por eso el tope de exposición importa
tanto como el cálculo del riesgo.
:::
