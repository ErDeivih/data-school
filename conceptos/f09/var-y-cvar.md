---
id: var-y-cvar
titulo: VaR y CVaR
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [cuantiles-y-percentiles, metricas-de-riesgo, maximo-drawdown]
tags: [riesgo, colas, cuantiles, cartera]
resumen: El VaR pone el umbral de pérdida que no se supera con cierta probabilidad y el CVaR mide la pérdida media cuando ese umbral se rompe.
fuentes: ["Jorion (2006), 'Value at Risk: The New Benchmark for Managing Financial Risk'", "Rockafellar y Uryasev (2000), 'Optimization of Conditional Value-at-Risk'"]
---

## En una frase

El VaR (value at risk) es la pérdida que no vas a superar en el 95 % de los días, y el CVaR
(conditional value at risk) es la pérdida media de ese 5 % de días en los que sí la superas: el
primero marca el umbral, el segundo describe lo que hay detrás.

## La idea

Piensa en el dique que protege una ciudad de las inundaciones. Puedes construir un muro que
aguante el 95 % de las crecidas y llamarlo «seguro». La pregunta que ese número no responde es:
cuando el agua pase por encima, ¿cuánto va a entrar? Un muro puede quedarse corto por diez
centímetros o por tres metros, y el destrozo no se parece en nada. El VaR es la altura del muro;
el CVaR es cuánto se inunda la ciudad cuando el muro falla.

Esa diferencia importa porque el VaR es un **cuantil**, y un cuantil solo mira dónde está la
frontera, no la forma de lo que queda fuera. Dos carteras pueden tener el mismo VaR
al 95 % y comportarse de forma opuesta en el peor 5 % de los escenarios: una pierde un poco más
que el umbral y la otra se hunde. Si tu límite de riesgo es un VaR, las dos pasan el filtro y
solo una te va a hacer daño.

Hay un segundo problema, más técnico y más importante de lo que parece: el VaR **no es
subaditivo**. Eso significa que puede ocurrir que la suma de los VaR de dos posiciones
separadas sea menor que el VaR de la cartera que las contiene. Un regulador que exigiera capital
por el VaR estaría, en ciertos casos, castigando la diversificación, que es lo
contrario de lo que quiere.

El CVaR sí es subaditivo, y por eso los marcos de riesgo modernos lo
prefieren cuando pueden elegir.

En la práctica el VaR se calcula de tres formas: **histórico** (ordenar las pérdidas observadas
y cortar por el cuantil), **paramétrico** (suponer una distribución, casi siempre normal) y por
**simulación** ([[simulacion-de-monte-carlo]]). Cada una tiene su trampa, y la peor es la
paramétrica: suponer normalidad en series financieras recorta justo la parte de la distribución
que estás intentando medir.

## Definición formal

Sea `R` el retorno de la cartera en un periodo y `L = −R` la pérdida, definida de forma que sea
positiva cuando pierdes. Sea `α` el nivel de confianza (0,95 o 0,99 habitualmente) y `1 − α` la
probabilidad de la cola.

:::formula
VaR_α = inf { l : P(L ≤ l) ≥ α }
:::

:::formula
CVaR_α = media de L sobre el peor (1 − α) de la distribución
:::

- `L` — pérdida del periodo, en euros o en tanto por uno. Positiva cuando la cartera baja.
- `α` — nivel de confianza. `VaR_0,95` es el cuantil 95 % de las pérdidas.
- `1 − α` — tamaño de la cola. Con `α = 0,95` es el 5 % de los peores escenarios.
- `VaR_α` — umbral de pérdida: el valor que solo superan el `(1 − α)` de los casos.
- `CVaR_α` — pérdida esperada **condicionada** a superar el umbral. Se llama también expected
  shortfall. Para distribuciones continuas coincide con `E[L tal que L ≥ VaR_α]`; con
  distribuciones discretas hay que repartir la masa del escalón, y para eso sirve la fórmula de
  Rockafellar y Uryasev:

:::formula
CVaR_α = mín over t de [ t + (1 / (1 − α)) · E[ (L − t)⁺ ] ]
:::

donde `(L − t)⁺` es `L − t` cuando es positivo y 0 en caso contrario. Ese mínimo se alcanza en
`t = VaR_α`, y tenerlo en forma de optimización es lo que permite meter el CVaR en un problema
de asignación de cartera.

**Versión paramétrica.** Si supones que `L` sigue una normal de media `μ` y desviación típica
`σ`:

:::formula
VaR_α = μ + z_α · σ        CVaR_α = μ + σ · φ(z_α) / (1 − α)
:::

- `z_α` — cuantil `α` de la normal tipificada: 1,645 para el 95 % y 2,326 para el 99 %.
- `φ` — función de densidad de la normal tipificada, `φ(x) = exp(−x²/2) / √(2π)`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `L` | Pérdida del periodo: el retorno cambiado de signo, positiva cuando la cartera baja | tanto por uno o euros, positiva en pérdida | Si mides la pérdida en negativo, todo el cálculo se da la vuelta: el cuantil 95 % pasaría a ser el mejor 5 % de los días |
| `α` | Nivel de confianza del VaR | tanto por uno (0,95 o 0,99) | Mueve el umbral hacia la cola y encarece el capital. En una normal, pasar del 95 % al 99 % multiplica el VaR por 1,41, no por 1,04 |
| `1 − α` | Probabilidad de la cola: la fracción de días que quedan por encima del umbral | tanto por uno (0,05 o 0,01) | Es el dato que hay que dar siempre junto al número, porque «VaR al 5 %» y «VaR al 95 %» se usan para lo mismo y significan lo contrario |
| `VaR_α` | Umbral de pérdida que solo supera el `(1 − α)` de los casos | las mismas que `L` | Al ser un cuantil no se mueve si cambias un día dentro de la cola, y sí mucho si mueves el peor: es la parte manipulable de la medida |
| `CVaR_α` | Pérdida media de todo lo que queda por encima del umbral (expected shortfall) | las mismas que `L` | Siempre es mayor o igual que el VaR, y la distancia entre los dos es lo que pesa la cola: en una normal un 25 %, con colas gruesas mucho más |
| `z_α` | Cuantil `α` de la normal tipificada: 1,645 para el 95 % y 2,326 para el 99 % | adimensional | Solo sirve si `L` es normal. Con colas gruesas el VaR paramétrico subestima justo los días que importan |
| `φ(x)` | Densidad de la normal tipificada, `exp(−x²/2) / √(2π)` | adimensional | Entra en el CVaR paramétrico como `σ · φ(z_α) / (1 − α)`. Confundir `φ` con la función de distribución `Φ` da un CVaR sin sentido |
| `N` | Número de observaciones del histórico con el que se calcula el VaR histórico | observaciones | Con `N` pequeño el cuantil es inestable: 250 días dan una cola de 13 datos y añadir o quitar uno mueve el VaR varios puntos |
:::

:::trampa
«VaR al 5 %» y «VaR al 95 %» se usan en la práctica para lo mismo, pero significan cosas
opuestas si no se dice si el número es el nivel de confianza o la probabilidad de la cola. Deja
siempre claro qué estás reportando: «VaR del 95 % de confianza, es decir, el 5 % de los peores
días».
:::

:::figura
fichero: var-y-cvar-umbral-y-cola
pie: A la izquierda, dos carteras construidas para tener el **mismo VaR** al 95 %: la azul con retornos normales y la naranja con colas gruesas. El umbral es el mismo (1,97 % del capital en las dos), pero el CVaR no: 2,47 % frente a 3,26 %, un 32 % más de pérdida media en el 5 % peor de los días. Fíjate en que toda la diferencia vive a la derecha de la línea roja: el VaR es ciego a lo que pasa ahí. A la derecha está el ejemplo de los dos bonos: sumar los VaR de las posiciones sueltas da 0 € y la cartera tiene 100 €, así que juntar riesgos empeora el VaR; con el CVaR ocurre lo contrario, porque 160 € (las dos sueltas) supera los 103 € de la cartera. Esa es la razón de que los marcos de riesgo modernos prefieran el CVaR.
fuente: figuras/var-y-cvar-1.py
:::

## Ejemplo

**Ejemplo 1: VaR histórico.** Una cartera de 100.000 € tiene 250 días de histórico. El 5 % de
250 son 12,5 días, así que la cola son las 13 mayores pérdidas diarias:

```
1.250  1.400  1.500  1.650  1.800  2.000  2.200
2.500  2.700  3.000  3.400  3.900  4.800   (en euros)
```

- **VaR al 95 %:** el umbral es **1.250 €**, la menor de las trece pérdidas de la cola, que es
  el 1,25 % del capital. Todo lo que queda por encima de ese umbral es el 5 % peor de los días.
- **CVaR al 95 %:** la media de las 13, **2.469 €**, el 2,47 % del capital.
- El CVaR es **1,98 veces** el VaR. Toda esa diferencia es información que el VaR se guarda para
  sí mismo.

**Ejemplo 2: el VaR no es subaditivo.** Dos bonos con un 4 % de probabilidad de impago cada uno,
100 € de pérdida si impagan y 100 € invertidos en cada uno, con impagos independientes:

- Un bono suelto: la probabilidad de perder algo es del 4 %, que es **menos** que el 5 % de la
  cola, así que el cuantil 95 % de la pérdida es **0 €**.
- Los dos bonos juntos: la probabilidad de que impague al menos uno es
  1 − 0,96² = 7,84 %, que ya supera el 5 %, así que el cuantil 95 % es **100 €**.
- Suma de los VaR individuales: 0 €. VaR conjunto: 100 €. **0 < 100**, y ahí tienes la violación
  de la subaditividad.
- Con el CVaR coherente (media del peor 5 %): 80 € para un bono suelto y 103,20 € para la
  cartera. La suma, 160 €, es mayor que 103,20 €: el CVaR premia la diversificación, el VaR la
  castiga.

## Código

```python verificable
import numpy as np

# Cola del 5 % de un historico de 250 dias: las 13 mayores perdidas diarias de una
# cartera de 100 000 EUR, escritas en euros.
cola = np.array([1250, 1400, 1500, 1650, 1800, 2000, 2200,
                 2500, 2700, 3000, 3400, 3900, 4800], dtype=float)
capital = 100_000

var95 = cola.min()          # umbral: la menor de las perdidas de la cola
cvar95 = cola.mean()        # perdida media de todo lo que queda por encima

print(f"cola {cola.size} de 250 dias")                # -> cola 13 de 250 dias
print(f"VaR  95% {var95:7.0f} EUR {var95 / capital:.2%}")     # -> 1250 EUR  1.25%
print(f"CVaR 95% {cvar95:7.0f} EUR {cvar95 / capital:.2%}")   # -> 2469 EUR  2.47%
print(f"CVaR / VaR {cvar95 / var95:.2f}")             # -> 1.98
```

:::claves
- `cola.min()` da el VaR porque la cola son las peores pérdidas y el umbral es la menor de ellas. Da igual que el array esté escrito de menor a mayor: `.min()` no depende del orden. Cambiarlo por `cola.mean()` te da el CVaR, un número un 98 % más alto, y el código seguiría funcionando sin avisar.
- El tamaño de la cola se decide **antes** de escribir los números: el 5 % de 250 días son 12,5 observaciones, y como no se pueden partir se toman 13. Con 12, el VaR sería 1.400 € en vez de 1.250 €. La longitud del array es el resultado de esa decisión, no al revés.
- `f"{var95 / capital:.2%}"` ya multiplica por 100: el `%` del formato lo hace. Escribir `f"{100 * var95 / capital:.2%}"` no da un error, da 125 %.
- `capital = 100_000` con guion bajo es el mismo número que `100000`; en Python los guiones son solo para leerlo mejor y puedes agrupar como quieras. Lo que sí importa es que los números del array sean `float`: con enteros, `cola.mean()` sigue dando decimales, pero una división entre enteros en otro sitio no.
- `cola.mean()` divide entre 13, no entre 250: el CVaR es la media **de la cola**, no la pérdida media diaria. Cambiar el denominador es el error que convierte una cifra de riesgo en una cifra de nada.
:::

```python verificable
import numpy as np

p = 0.04                                   # probabilidad de impago de cada bono
perdida = 100.0                            # EUR que se pierden si impaga

def var_cvar(perdidas, probs, cola=0.05):
    """VaR y CVaR coherente: media del peor `cola` de la distribucion."""
    orden = np.argsort(-perdidas)
    pe, pr = perdidas[orden], probs[orden]
    var = pe[np.searchsorted(np.cumsum(pr), cola)]   # umbral del peor 5 %
    resto, cvar = cola, 0.0
    for perdida_i, peso in zip(pe, pr):              # masa parcial en el escalon
        toma = min(peso, resto)
        cvar += toma * perdida_i
        resto -= toma
    return var, cvar / cola

un_bono = var_cvar(np.array([0.0, perdida]), np.array([1 - p, p]))
dos_bonos = var_cvar(np.array([0.0, perdida, 2 * perdida]),
                     np.array([(1 - p) ** 2, 2 * p * (1 - p), p ** 2]))

print(f"VaR  95%  un bono {un_bono[0]:6.0f}  los dos {dos_bonos[0]:6.0f}")
# -> VaR  95%  un bono      0  los dos    100
print(f"CVaR 95%  un bono {un_bono[1]:6.2f}  los dos {dos_bonos[1]:6.2f}")
# -> CVaR 95%  un bono  80.00  los dos 103.20
print(f"suma de VaR  {2 * un_bono[0]:.0f} < {dos_bonos[0]:.0f} conjunto")
# -> suma de VaR  0 < 100 conjunto
print(f"suma de CVaR {2 * un_bono[1]:.2f} >= {dos_bonos[1]:.2f} conjunto")
# -> suma de CVaR 160.00 >= 103.20 conjunto
```

```python verificable
import numpy as np

# Version parametrica: cartera de 100 000 EUR con volatilidad diaria del 1,2 % y media 0.
capital, sigma_diaria = 100_000, 0.012
z = 1.6448536269514722                    # cuantil 95 % de la normal tipificada
phi = np.exp(-z ** 2 / 2) / np.sqrt(2 * np.pi)

var95 = z * sigma_diaria * capital
cvar95 = phi / 0.05 * sigma_diaria * capital
print(f"VaR  95% {var95:7.0f} EUR {z * sigma_diaria:.2%}")          # -> 1974 EUR  1.97%
print(f"CVaR 95% {cvar95:7.0f} EUR {phi / 0.05 * sigma_diaria:.2%}")  # -> 2475 EUR  2.48%
print(f"CVaR / VaR {cvar95 / var95:.2f}")                            # -> 1.25
```

## Errores típicos

- **Leer el VaR como pérdida máxima.** No lo es: es el umbral que se supera con probabilidad
  `1 − α`. Un VaR del 95 % de 2.000 € se rompe uno de cada veinte días, y en una racha mala eso
  son varios días en un mes.
- **Quedarse con el VaR e ignorar el CVaR.** Dos carteras con el mismo VaR pueden tener colas
  incomparables. Si solo reportas uno, reporta el CVaR: contiene al VaR y no se puede manipular
  tan fácilmente.
- **Usar una normal donde no la hay.** Con colas gruesas y asimetría, el VaR paramétrico
  subestima justo los días que importan. Es el motivo de que existan [[distribuciones-en-datos-reales]]
  y de que el VaR histórico y el simulado sean el estándar en la práctica.
- **Escalar el VaR diario a anual multiplicando por `√252`.** Ese factor sale de suponer
  normalidad e independencia, y las colas no escalan así. Un VaR anual calculado a partir del
  diario suele quedarse corto.
- **Elegir `α` después de ver los resultados.** Si pruebas 90 %, 95 % y 99 % y publicas el que
  deja la cifra más bonita, has hecho [[data-snooping-y-multiple-testing]] con el nivel de
  confianza. Fija `α` antes.
- **Calcular el VaR de la cartera como la suma de los VaR individuales.** No sirve: la suma de
  los VaR de las partes no acota el VaR del conjunto, ni por arriba ni por abajo. Solo coincidiría
  con correlación perfecta entre todas las posiciones, y el ejemplo de los dos bonos enseña que la
  desigualdad puede ir en el sentido contrario. Necesitas la distribución conjunta.

:::practica
enunciado: Una cartera de 200.000 € tiene 200 días de histórico y estas son las 10 mayores pérdidas diarias: 3.000, 4.500, 6.000, 8.000, 9.000, 10.000, 11.000, 12.000, 13.000 y 14.000 €. Calcula el VaR y el CVaR al 95 % en euros y en porcentaje del capital, y la relación entre ambos.
pista: La cola del 5 % de 200 días son las 10 peores pérdidas, y el VaR es la menor de ellas, no la media.
solucion: 0,05 · 200 = 10, así que la cola son esas diez pérdidas. El VaR al 95 % es la menor de la cola: 3.000 €, un 1,50 % del capital. El CVaR es su media: 90.500 / 10 = 9.050 €, un 4,53 % del capital. El CVaR es 9.050 / 3.000 = 3,02 veces el VaR, así que la cola pesa tres veces más que el umbral.
:::

## Comprueba que lo sabes

:::quiz
p: Una cartera tiene un VaR del 99 % de 5.000 € y un CVaR del 99 % de 9.000 €. ¿Qué significa?
o: Que la pérdida máxima posible es 9.000 €
o: Que en el peor 1 % de los días la pérdida media es 9.000 €, y el umbral a partir del cual se entra en ese 1 % es 5.000 €
o: Que en el 99 % de los días se pierde exactamente 9.000 €
a: 2
e: El VaR es el cuantil: el umbral que solo supera el 1 % de los días. El CVaR es la media de las pérdidas de ese 1 % restante. Ni uno es un máximo ni el otro es una pérdida frecuente.
:::

:::quiz
p: ¿Por qué se dice que el VaR no es una medida de riesgo «coherente»?
o: Porque no se puede calcular con datos históricos
o: Porque puede incumplir la subaditividad: el VaR de una cartera puede ser mayor que la suma de los VaR de sus partes
o: Porque siempre es menor que el CVaR
a: 2
e: La subaditividad exige que juntar dos riesgos nunca sea peor que sumarlos por separado, y el VaR la incumple en distribuciones con saltos, como muestra el ejemplo de los dos bonos. El CVaR sí la cumple. Que sea menor que el CVaR es normal y no tiene nada de incoherente.
:::

:::quiz
p: Con 250 días de histórico, ¿por qué la cola del 5 % son 13 observaciones y no 12,5?
o: Porque hay que redondear hacia arriba para que la cola cubra al menos el 5 % de los casos
o: Porque el VaR siempre se calcula con un número impar de datos
o: Porque las 12,5 observaciones se redondean al número par más cercano
a: 1
e: 0,05 · 250 = 12,5 y las observaciones son indivisibles: para que el conjunto cubra al menos el 5 % necesitas 13. Es el mismo detalle que aparece al calcular cualquier cuantil empírico con pocos datos, y explica por qué el VaR histórico de una muestra corta es tan inestable.
:::
