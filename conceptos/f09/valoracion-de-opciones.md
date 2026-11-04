---
id: valoracion-de-opciones
titulo: Valoración de opciones
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [movimiento-browniano, valor-esperado, curva-de-tipos-y-descuento]
tags: [opciones, black-scholes, derivados]
resumen: Por qué una opción tiene un precio único aunque nadie sepa a dónde va el activo: replicación, medida neutral al riesgo y la fórmula de Black-Scholes.
fuentes: ["Black y Scholes (1973), 'The Pricing of Options and Corporate Liabilities'", "Bachelier (1900), 'Théorie de la spéculation'"]
---

## En una frase

El precio de una opción no sale de adivinar a dónde va el activo, sino de construir una cartera
que copie su pago y obligar a que las dos cosas cuesten lo mismo.

## La idea

Una opción es un derecho, no una obligación: pagas hoy por poder comprar (call) o vender (put)
algo a un precio fijado (el *strike*) antes de una fecha (el vencimiento). Su pago final es
`max(S_T − K, 0)` en la call y `max(K − S_T, 0)` en la put. Nunca es negativo, y ahí está el
problema: algo que nunca vale menos de cero y a veces vale mucho tiene un precio, y ese precio no
puede salir de la media de sus pagos, porque la media de una distribución que no conoces no es un
número.

La idea de Black, Scholes y Merton es distinta y es la que cambió las finanzas: **si puedes
fabricar el pago de la opción comprando y vendiendo el activo subyacente, entonces la opción vale
lo que cuesta fabricarla**. Nadie necesita saber si el activo va a subir. Basta con que exista una
cartera —una cantidad de acciones y efectivo que se va ajustando— cuyo valor final sea el mismo
que el de la opción. Si dos cosas dan lo mismo en el futuro, hoy tienen que costar lo mismo; si
no, hay arbitraje.

El truco técnico es el **cambio de medida**. En vez de descontar los pagos con la probabilidad
real (que exige conocer la deriva `μ`, que nadie conoce), se valoran con una probabilidad
artificial —la medida neutral al riesgo— en la que todos los activos rinden el tipo sin riesgo.
El resultado es que `μ` desaparece de la fórmula. Eso desconcierta al principio: el precio de una
opción no depende de si crees que la acción va a subir. Depende de la volatilidad, del plazo, del
strike y de los tipos. La dirección ya está dentro del precio del activo.

:::aviso
Que `μ` no aparezca no significa que la dirección dé igual para ganar dinero: significa que la
dirección ya está cobrada en el precio del subyacente. Si compras una call porque crees que sube,
estás apostando a que subirá **más de lo que el mercado descuenta**, no a que suba.
:::

## Definición formal

Para una call europea sobre un activo que no paga dividendos, con `S₀` el precio actual, `K` el
strike, `r` el tipo sin riesgo, `σ` la volatilidad y `T` el plazo en años:

:::formula
C = S₀ · Φ(d₁) − K · e^(−rT) · Φ(d₂)
:::

:::formula
d₁ = ( ln(S₀/K) + (r + σ²/2)·T ) / (σ·√T)        d₂ = d₁ − σ·√T
:::

- `Φ(·)` — función de distribución de la normal estándar: la probabilidad de que una normal típica
  quede por debajo de ese valor.
- `d₁`, `d₂` — distancias estandarizadas al strike; `d₂` es, en la medida neutral al riesgo, la
  probabilidad de acabar dentro del dinero.
- `e^(−rT)` — factor de descuento: lo que vale hoy un euro seguro dentro de `T` años, que es
  exactamente lo que mide [[curva-de-tipos-y-descuento]].

La **paridad put-call** no es una fórmula aparte, es una identidad que tiene que cumplirse siempre
porque si no hay arbitraje:

:::formula
C − P = S₀ − K · e^(−rT)
:::

Si la paridad no se cumple, puedes comprar lo barato, vender lo caro y quedarte con la diferencia
sin riesgo. Por eso se usa como test: cualquier implementación que la viole tiene un error.

**El modelo de Bachelier (1900)** es el mismo razonamiento con un browniano aritmético en vez de
geométrico: el precio sigue una normal en lugar de una lognormal. Sigue usándose para tipos de
interés y para volatilidad normal, precisamente porque en esos mercados el nivel puede ser
negativo. La estructura —replicación, medida neutral, esperanza descontada— es idéntica; cambia la
distribución.

## Ejemplo

`S₀ = 100`, `K = 100`, `r = 3 %`, `σ = 25 %`, `T = 1`.

- `d₁ = (ln 1 + (0,03 + 0,03125)) / 0,25 = 0,06125 / 0,25 = 0,245`.
- `d₂ = 0,245 − 0,25 = −0,005`.
- `Φ(0,245) = 0,5968` y `Φ(−0,005) = 0,4980`.
- `C = 100 · 0,5968 − 100 · 0,9704 · 0,4980 = 59,68 − 48,33 = 11,35`.
- Por paridad: `P = 11,35 − 100 + 97,04 = 8,39`.

Fíjate en que `d₂` es prácticamente cero: la probabilidad neutral al riesgo de acabar dentro del
dinero es del 49,8 %, casi una moneda. La call vale 11,35 porque, aunque la mitad de las veces
acabe sin valor, las veces que acaba dentro lo hace con recorrido. Esa asimetría es todo el
negocio de una opción.

## Código

```python verificable
import math
from scipy.stats import norm

S0, K, r, sigma, T = 100.0, 100.0, 0.03, 0.25, 1.0

d1 = (math.log(S0 / K) + (r + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)
call = S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
put = call - S0 + K * math.exp(-r * T)

print(f"d1 {d1:.4f} d2 {d2:.4f}")                      # -> d1 0.2450 d2 -0.0050
print(f"call {call:.2f} put {put:.2f}")                # -> call 11.35 put 8.39
print(f"paridad {call - put - S0 + K * math.exp(-r * T):+.10f}")  # -> paridad +0.0000000000
```

La última línea imprime cero con diez decimales: es la comprobación de que la implementación
resuelve la misma ecuación que el modelo. Si sale distinto de cero, el error está en la fórmula o
en los signos, no en el mercado.

:::claves
- `norm.cdf(d2)` es una probabilidad acumulada, no una densidad. Cambiarlo por `norm.pdf` da un
  número positivo y plausible que no significa nada: el tipo de error que sobrevive a una
  revisión rápida.
- `math.exp(-r * T)` descuenta el strike, no el resultado. Si descuentas la call entera estás
  valorando un pago que ocurre hoy con un tipo que corresponde a mañana.
- `math.log(S0 / K)` usa logaritmo natural. Con logaritmo decimal, `d1` cambia de escala y el
  precio se va a cero sin lanzar ningún error.
- `sigma` va en tanto por uno anual (0,25, no 25). Si le pasas 25, la call vale prácticamente
  `S₀` y parece que el modelo «se ha vuelto loco».
- `put = call - S0 + K * math.exp(-r * T)` despeja la put de la paridad en vez de repetir la
  fórmula. Al hacerlo así, la paridad se cumple por construcción y el test compara dos caminos
  distintos hacia el mismo número.
:::

## Errores típicos

- **Meter la rentabilidad esperada del activo en la fórmula.** No aparece, y no es un olvido: está
  absorbida por el precio actual. Si tu implementación tiene un parámetro `mu`, no estás valorando
  una opción, estás simulando una apuesta.
- **Usar volatilidad diaria con plazo en años.** `σ` y `T` tienen que hablar el mismo idioma. La
  volatilidad diaria se anualiza multiplicando por √252.
- **Olvidar descontar el strike.** Con tipos al 3 % el error es pequeño y con tipos al 12 % deja
  de serlo. En plazos largos, el descuento es una parte grande del precio.
- **Interpretar el precio como probabilidad.** Una call de 11,35 no dice «hay un 11 % de que
  suba». El precio mezcla probabilidad, magnitud y descuento.
- **Comparar opciones con vencimientos distintos sin anualizar.** Una call a un mes y otra a un
  año no se comparan por su prima: se comparan por su volatilidad implícita.
- **Creer que la volatilidad implícita es la volatilidad futura.** Es la que el mercado cobra hoy,
  y contiene prima de riesgo y oferta y demanda. Que el modelo la llame volatilidad no la
  convierte en un pronóstico.

:::practica
enunciado: Con S₀ = 50, K = 55, r = 2 %, σ = 40 % y T = 0,5, calcula d₁ y d₂, decide si la call está dentro o fuera del dinero y comprueba la paridad con la put.
pista: d₁ mide la distancia al strike en desviaciones típicas del logaritmo; el signo de ln(S₀/K) manda.
solucion: ln(50/55) = −0,0953; (0,02 + 0,08) · 0,5 = 0,05; σ√T = 0,40 · 0,7071 = 0,2828. d₁ = (−0,0953 + 0,05) / 0,2828 = −0,160; d₂ = −0,160 − 0,2828 = −0,443. La call está fuera del dinero (S₀ < K) y vale C = 50 · 0,4364 − 55 · 0,9900 · 0,3289 = 21,82 − 17,91 = 3,91. La put por paridad: 3,91 − 50 + 54,45 = 8,36.
:::

## Comprueba que lo sabes

:::quiz
p: Si sube la volatilidad del activo, ¿qué les pasa a una call y a una put del mismo strike?
o: Suben las dos, porque una opción es un derecho y más volatilidad aumenta el valor de ese derecho
o: Sube la call y baja la put, porque son posiciones contrarias
o: No les pasa nada: la volatilidad ya está en el precio del subyacente
a: 1
e: El comprador de una opción tiene el derecho a ejercer solo si le conviene, así que la pérdida está acotada y la ganancia no. Más dispersión mejora las dos colas del derecho. Que suban las dos es la razón de que exista la cobertura de vega.
:::

:::quiz
p: ¿Por qué la rentabilidad esperada del activo no aparece en la fórmula de Black-Scholes?
o: Porque se cancela al construir la cartera replicante y valorar en la medida neutral al riesgo
o: Porque los modelos suponen que todos los activos suben lo mismo
o: Porque la fórmula es una aproximación y se olvidaron de incluirla
a: 1
e: Al formar la cartera que replica la opción, la deriva del activo se cancela entre la posición en acciones y la opción. Lo que queda se valora con la probabilidad artificial en la que todos los activos rinden el tipo sin riesgo. No es un olvido: es el resultado central del modelo.
:::
