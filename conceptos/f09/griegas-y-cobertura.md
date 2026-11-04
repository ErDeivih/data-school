---
id: griegas-y-cobertura
titulo: Griegas y cobertura
fase: 9
nivel: experto
rutas: [quant]
prerequisitos: [valoracion-de-opciones, operaciones-matriciales, optimizacion-con-restricciones]
tags: [griegas, cobertura, riesgo]
resumen: Las derivadas del precio de una opción, y cómo se resuelve la cartera que deja la exposición a cero sin apostar a la dirección.
fuentes: ["Hull (2018), 'Options, Futures and Other Derivatives', cap. 19", "Taleb (1997), 'Dynamic Hedging'"]
---

## En una frase

Delta, gamma, vega, theta y rho miden cuánto cambia el precio de una opción cuando cambia una
sola cosa, y cubrir es elegir posiciones que sumen cero en esas derivadas a la vez.

## La idea

El precio de una opción se mueve por cinco motivos: el precio del subyacente, su curvatura, la
volatilidad, el paso del tiempo y los tipos. Cada uno tiene su derivada, y a esas derivadas se
les llama griegas porque se nombran con letras griegas. No son un adorno académico: son la lista
de riesgos que asume quien vende una opción.

La delta es la más conocida y la más engañosa. Una cartera con delta cero **no es una cartera sin
riesgo**: es una cartera que no gana ni pierde si el precio se mueve un poco. Si se mueve mucho,
la delta cambia —eso es la gamma— y la cobertura se descompone. Vender opciones y cubrir la delta
es, en la práctica, estar corto de gamma: ganas poco muchas veces y pierdes mucho de golpe cuando
el precio se mueve de verdad. Esa asimetría es la razón de que exista el oficio.

Cubrir varias sensibilidades a la vez es un problema de álgebra, no de intuición. Si tienes dos
riesgos (gamma y vega) y dos instrumentos de cobertura, necesitas que la combinación de ambos
anule las dos exposiciones: dos ecuaciones, dos incógnitas.

:::trampa
Cubrir con un solo instrumento cuando tienes dos riesgos deja el segundo intacto. Puedes anular la
gamma comprando calls y descubrir que has multiplicado la vega. El sistema hay que plantearlo
completo o no plantearlo.
:::

## Definición formal

Para una call con precio `C(S, σ, t, r)`:

:::formula
Δ = ∂C/∂S     Γ = ∂²C/∂S²     ν = ∂C/∂σ     Θ = ∂C/∂t     ρ = ∂C/∂r
:::

- `Δ` (delta) — cambio del precio de la opción por cada euro que se mueve el subyacente.
- `Γ` (gamma) — cambio de la delta por cada euro: la curvatura. Si es grande, la cobertura caduca
  rápido.
- `ν` (vega) — cambio por cada punto de volatilidad, normalmente expresado por punto porcentual.
- `Θ` (theta) — lo que pierde la opción por el paso del tiempo, con todo lo demás quieto.
- `ρ` (rho) — sensibilidad a los tipos; la menos importante a plazos cortos.

La cobertura con `n` instrumentos es un sistema lineal. Con dos instrumentos y dos sensibilidades:

:::formula
G · w = −e        w = G⁻¹ · (−e)
:::

- `G` — matriz de griegas por contrato: cada fila una sensibilidad (gamma, vega), cada columna un
  instrumento de cobertura.
- `w` — pesos a operar de cada instrumento, en contratos.
- `e` — exposición actual de la cartera en esas mismas sensibilidades, con su signo.

Resuelto el sistema, queda la delta, que se ajusta con el propio subyacente porque su delta es 1,
su gamma es 0 y su vega es 0:

:::formula
w_S = −( Δ_cartera + Σ w_i · Δ_i )
:::

**Cuándo el sistema no tiene solución.** Si el determinante de `G` es cero, los dos instrumentos
cubren lo mismo y no se pueden anular dos riesgos con uno. Si es casi cero, la solución existe
pero es enorme: pequeños errores en las griegas producen pesos absurdos. Eso se mide con el número
de condición y es la razón de que en la práctica se use una tercera opción o se regularice el
sistema en lugar de invertirlo tal cual.

## Ejemplo

Una cartera tiene exposición a gamma de 60 y a vega de 100 (en unidades por contrato). Hay dos
calls de cobertura: la A tiene gamma 2 y vega 10; la B tiene gamma 5 y vega 18.

El determinante es `2 · 18 − 5 · 10 = −14`. Resolviendo:

- `w_A = (18 · 60 − 5 · 100) / (−14) = (1080 − 500) / (−14) = −41,43` contratos.
- `w_B = (−10 · 60 + 2 · 100) / (−14) = (−600 + 200) / (−14) = +28,57` contratos.

El signo negativo no es un error: hay que **vender** 41,43 contratos de A y comprar 28,57 de B.
La comprobación es inmediata: `2 · (−41,43) + 5 · 28,57 = 60` de gamma y
`10 · (−41,43) + 18 · 28,57 = 100` de vega. Las dos quedan cubiertas.

Queda la delta. Si la cartera arrastra +12 de delta y las dos calls tienen delta 0,45 y 0,55:

`12 + (−41,43 · 0,45) + (28,57 · 0,55) = 12 − 18,64 + 15,71 = +9,07`.

Para dejarla en cero hay que vender 9,07 acciones. Y ese es el punto: la cobertura de las griegas
no es un número, es una posición que hay que recalcular cada vez que el precio o la volatilidad
se mueven.

## Código

```python verificable
import numpy as np

# Dos calls de cobertura: columnas = A y B; filas = gamma y vega por contrato
G = np.array([[2.0, 5.0],
              [10.0, 18.0]])
exposicion = np.array([60.0, 100.0])      # gamma y vega que hay que neutralizar
delats = np.array([0.45, 0.55])           # delta de cada call
delta_cartera = 12.0

w = np.linalg.solve(G, exposicion)

print(f"pesos {w[0]:.2f} {w[1]:.2f}")                                  # -> pesos -41.43 28.57
print(f"gamma cubierta {G[0] @ w:.2f} vega cubierta {G[1] @ w:.2f}")    # -> gamma cubierta 60.00 vega cubierta 100.00
print(f"delta residual {delta_cartera + w @ delats:+.2f}")              # -> delta residual +9.07
print(f"spot {-delta_cartera - w @ delats:+.2f} acciones")              # -> spot -9.07 acciones
print(f"condicion {np.linalg.cond(G):.2f}")                             # -> condicion 32.33
```

Las dos primeras líneas confirman que el sistema está bien resuelto. La tercera dice que aún hay
delta, y la cuarta es la operación de spot que la lleva a cero: un número negativo significa
vender.

:::claves
- `np.linalg.solve(G, exposicion)` resuelve el sistema sin invertir la matriz. `inv(G) @ b` da lo
  mismo en papel y peor en coma flotante: más error y más operaciones.
- `w @ delats` es el producto escalar entre pesos y deltas, la aportación total de las opciones a
  la delta. Sin él, el «delta residual» es solo el de la cartera original y la cobertura parece
  terminada cuando no lo está.
- `np.linalg.cond(G)` mide cuánto amplifica el sistema un error de entrada. Por debajo de 100 el
  sistema es cómodo; por encima de 1000, un error del 0,1 % en las griegas puede mover los pesos
  un 100 %.
- Los pesos salen en **contratos**, no en euros. El multiplicador del contrato se aplica después,
  y olvidarlo es un factor 100 que no avisa.
- El signo se lee, no se corrige a mano: un peso negativo es una venta. Cambiar el signo «porque
  no puede ser» invierte la cobertura y la convierte en una apuesta al doble.
:::

## Errores típicos

- **Cubrir una vez y olvidarse.** La cobertura es dinámica: cada movimiento del precio cambia la
  delta y cada cambio de volatilidad cambia la vega. Una cobertura estática es una foto de un
  instante, no una posición.
- **Ignorar la gamma cruzada.** Al resolver el sistema, cada instrumento aporta a todas las
  sensibilidades. Mirar solo la diagonal de `G` y repartir «lo que toca» funciona por casualidad
  y falla cuando los instrumentos no son simétricos.
- **Rebalancear cada minuto.** Cada rebalanceo paga horquilla y comisiones. Existe un óptimo entre
  cubrir demasiado pronto y demasiado tarde, y depende de la gamma y del coste por operación, no
  del gusto.
- **Creer que delta-neutral es «sin riesgo».** Neutralizar la primera derivada deja la segunda y
  la tercera. Un libro delta-neutral puede perder mucho en un día de movimiento grande.
- **Mezclar unidades.** Vega por acción, vega por contrato y vega por punto porcentual son tres
  números distintos. Un factor 100 de diferencia no lanza ningún error.
- **Confundir cobertura con predicción.** Cubrir no es acertar la dirección; es quitarse una
  exposición y quedarse con otra. El libro sigue teniendo riesgo, solo que otro.

## Comprueba que lo sabes

:::quiz
p: Con dos instrumentos de cobertura y dos sensibilidades, ¿qué significa que el determinante de la matriz de griegas sea cero?
o: Que los dos instrumentos cubren exactamente lo mismo y no se pueden anular dos riesgos con ellos
o: Que la cartera ya está cubierta y no hay que operar
o: Que las griegas son cero y el sistema está resuelto
a: 1
e: Determinante cero significa que las columnas son linealmente dependientes: los dos instrumentos aportan la misma combinación de gamma y vega. El sistema no tiene solución única y hay que añadir un tercer instrumento o cambiar la cobertura.
:::

:::quiz
p: Una cartera delta-neutral pierde dinero en un día en que el subyacente se mueve un 8 %. ¿Qué griega explica la pérdida?
o: La gamma: al moverse mucho el precio, la delta cambia y la cobertura deja de ser neutral
o: La rho: los tipos se movieron con el precio
o: Ninguna: una cartera delta-neutral no puede perder
a: 1
e: La delta solo es válida para movimientos pequeños. Con un movimiento grande, la curvatura (gamma) hace que la exposición cambie y la posición quede descubierta. Delta-neutral protege de un movimiento infinitesimal, no de un hueco.
:::
