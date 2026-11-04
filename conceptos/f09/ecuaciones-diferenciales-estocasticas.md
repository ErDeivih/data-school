---
id: ecuaciones-diferenciales-estocasticas
titulo: Ecuaciones diferenciales estocásticas
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [movimiento-browniano, derivadas-y-reglas, integrales]
tags: [sde, euler-maruyama, simulacion]
resumen: Cómo se escribe un modelo de precio como deriva más ruido, y cómo se simula sin que el paso temporal mienta sobre la incertidumbre.
fuentes: ["Kloeden y Platen (1992), 'Numerical Solution of Stochastic Differential Equations'", "Øksendal (2003), 'Stochastic Differential Equations'"]
---

## En una frase

Una ecuación diferencial estocástica describe el cambio de una variable como una parte
predecible (deriva) más una parte aleatoria (difusión), y se simula avanzando por pasos con un
ruido que escala con la raíz del paso.

## La idea

Un modelo de precio necesita dos cosas a la vez: una tendencia y un temblor. La tendencia es
determinista y pequeña; el temblor es aleatorio y, en cada intervalo, del orden de la raíz del
tiempo transcurrido. Esa raíz es la que rompe la intuición de quien viene del cálculo normal: al
dividir el tiempo en trozos más finos, el ruido de cada trozo no se reduce en la misma proporción.

De ahí sale el esquema de Euler-Maruyama, que es la versión estocástica del método de Euler: en
cada paso sumas la deriva multiplicada por el paso y el ruido multiplicado por la **raíz** del
paso. Con pocos pasos el resultado se separa de la solución verdadera; con muchos se acerca, pero
el error no baja igual de rápido que en una ecuación ordinaria.

Casi ninguna EDE tiene solución cerrada. La del movimiento browniano geométrico la tiene, y por
eso se usa como banco de pruebas: puedes comparar lo que simula tu esquema con lo que dice la
fórmula exacta. Si tu simulador no reproduce la fórmula exacta en ese caso, no está listo para
simular los que no la tienen.

:::aviso
En una EDE el error se mide de dos formas. El **error fuerte** compara trayectorias: la misma
secuencia de números aleatorios, el esquema contra la solución exacta. El **error débil** compara
medias y varianzas de muchas trayectorias. Un esquema puede ser bueno en media y malo trayectoria
a trayectoria, o al revés. Para valorar opciones importa el débil; para simular un camino concreto,
el fuerte.
:::

## Definición formal

Una EDE de Itô se escribe:

:::formula
dX_t = a(X_t, t) dt + b(X_t, t) dW_t
:::

- `a(X, t)` — deriva: el cambio esperado por unidad de tiempo.
- `b(X, t)` — difusión: la sensibilidad al ruido, en unidades de `X` por raíz de tiempo.
- `W_t` — el movimiento browniano de [[movimiento-browniano]].
- `dt` — incremento de tiempo; `dW_t` — su incremento aleatorio, con varianza `dt`.

El esquema de Euler-Maruyama discretiza el intervalo en `n` pasos de tamaño `Δt`:

:::formula
X_{k+1} = X_k + a(X_k, t_k)·Δt + b(X_k, t_k)·√Δt·Z_k        Z_k ~ N(0, 1)
:::

El error fuerte es de orden `Δt^½`: dividir el paso por 4 reduce el error a la mitad, no a la
cuarta parte. El error débil es de orden `Δt`: dividir por 4 lo reduce a la cuarta parte. Esa
diferencia de exponentes es la razón de que simular bien una trayectoria sea mucho más caro que
estimar una media.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `a` | Deriva del proceso | unidades de X por unidad de tiempo | Empuja todas las trayectorias en la misma dirección y no cambia su dispersión |
| `b` | Difusión | unidades de X por raíz de tiempo | Abre el abanico de trayectorias; en el GBM es `σ·X`, así que crece con el nivel |
| `Δt` | Tamaño del paso | años o fracción | Pasos grandes sesgan la simulación y pueden hacer que el proceso cruce cero |
| `n` | Número de pasos | pasos | Sube el coste de forma lineal y el error baja como `1/√n` en fuerte y `1/n` en débil |
:::

## Ejemplo

GBM con `S₀ = 100`, `μ = 0,05`, `σ = 0,25`, cuatro pasos de `Δt = 0,25` y `Z = (0,3; −1,1; 0,2; 0,8)`.

Primer paso: `100 + 0,05 · 100 · 0,25 + 0,25 · 100 · 0,5 · 0,3 = 100 + 1,25 + 3,75 = 105,0`.

El segundo paso parte de 105,0: `105,0 + 0,05 · 105 · 0,25 + 0,25 · 105 · 0,5 · (−1,1) = 105,0 +
1,31 − 14,44 = 91,87`.

Fíjate en el factor 0,5: es `√0,25`. Si hubieras usado `0,25` en vez de `0,5`, el ruido del
segundo paso habría sido `−7,22` en lugar de `−14,44` y la trayectoria habría quedado mucho más
suave de lo que el modelo dice.

## Código

```python verificable
import numpy as np

# GBM: un camino con Euler-Maruyama y el mismo camino con la solucion exacta
rng = np.random.default_rng(3)
mu, sigma, s0, T, n = 0.05, 0.25, 100.0, 1.0, 1000
dt = T / n
z = rng.standard_normal(n)

s = s0
for paso in range(n):
    s = s + mu * s * dt + sigma * s * np.sqrt(dt) * z[paso]

exacto = s0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * np.sqrt(dt) * z.sum())

print(f"euler {s:.4f}")                                   # -> euler 138.0540
print(f"exacto {exacto:.4f}")                             # -> exacto 138.1202
print(f"error {abs(s - exacto):.4f}")                     # -> error 0.0662
print(f"error relativo {abs(s - exacto) / exacto:.4%}")   # -> error relativo 0.0479%
```

Con 1.000 pasos el error relativo es del 0,05 %, que es lo que se espera de un esquema de orden
medio. Si el error fuera del 5 %, el sospechoso sería la raíz del paso.

:::claves
- `sigma * s * np.sqrt(dt)` aplica la difusión al nivel actual: es lo que hace que el proceso sea
  multiplicativo. Sin la `s`, el modelo se vuelve aditivo y deja de ser un precio.
- `z.sum()` suma los 1.000 números aleatorios. La solución exacta usa la suma del browniano
  acumulado en `T`, no un número nuevo: por eso se compara el mismo camino.
- `mu - 0.5 * sigma ** 2` aparece solo en la solución exacta, porque viene del lema de Itô. En el
  bucle no se resta nada: la resta es una propiedad de la solución, no del esquema.
- El bucle es vectorizable, pero aquí se escribe paso a paso a propósito: cada iteración usa el
  valor actualizado, así que no se puede lanzar de golpe sin una recurrencia.
- `rng.standard_normal(n)` fija la semilla al principio. Cambiar la semilla cambia el camino y no
  invalida la comparación, porque las dos ramas usan el mismo `z`.
:::

## Errores típicos

- **Usar `Δt` en el término de difusión.** Es el error que más veces aparece en el código de
  alguien que empieza: el modelo se vuelve menos ruidoso cuanto más fino es el paso, que es
  exactamente lo contrario de lo que pasa.
- **Elegir pasos tan grandes que el proceso cruza cero.** En un GBM la difusión es proporcional al
  nivel, pero con `Δt` grande el salto puede ser mayor que el precio y el siguiente paso parte de
  un número negativo.
- **Confundir la deriva con la rentabilidad esperada.** En el GBM, la media del nivel crece como
  `μ`, pero la del logaritmo crece como `μ − σ²/2`. Si comparas tu simulación con la fórmula
  equivocada, concluirás que el esquema está mal cuando el error es tuyo.
- **Creer que el orden fuerte y el débil son el mismo número.** Un esquema de orden débil 1 puede
  tener orden fuerte ½. Si tu conclusión depende de trayectorias concretas, necesitas el fuerte.
- **Simular una sola trayectoria y sacar conclusiones.** Una trayectoria es un sorteo. Para
  valorar, estimar una probabilidad o medir un riesgo hacen falta muchas, y el error de la
  estimación baja con la raíz del número de réplicas.
- **Usar Euler-Maruyama para un modelo con saltos.** Si el proceso tiene saltos, la discretización
  necesita un término de Poisson y el esquema cambia. Reutilizar el de difusión pura omite justo
  lo que se quería modelar.

:::practica
enunciado: Con S₀ = 50, μ = 0,02, σ = 0,4 y dos pasos de 0,5 años, y Z = (1,0; −0,5), calcula la trayectoria del GBM con Euler-Maruyama.
pista: En cada paso, la difusión lleva √0,5 = 0,7071, no 0,5.
solucion: Paso 1: 50 + 0,02·50·0,5 + 0,4·50·0,7071·1,0 = 50 + 0,5 + 14,14 = 64,64. Paso 2: 64,64 + 0,02·64,64·0,5 + 0,4·64,64·0,7071·(−0,5) = 64,64 + 0,65 − 9,14 = 56,15. Con √0,5 mal puesto en 0,5, el segundo paso restaría 6,46 en vez de 9,14.
:::

## Comprueba que lo sabes

:::quiz
p: Reduces el paso Δt a la cuarta parte. ¿Qué le pasa al término de ruido de cada paso?
o: Se multiplica por ½, porque el ruido escala con la raíz del paso
o: Se divide por 4, igual que el paso
o: No cambia, porque el ruido no depende del paso
a: 1
e: El término de difusión lleva √Δt. Si Δt pasa a ser ¼, su raíz pasa a ser ½. Dividirlo por 4 haría que la simulación dependiera del número de pasos elegido, que es un error de modelo.
:::

:::quiz
p: ¿Para qué sirve comparar un esquema numérico con la solución exacta del GBM?
o: Para medir el error del esquema en un caso donde se conoce la respuesta, antes de usarlo en modelos que no la tienen
o: Porque el GBM es más realista que los demás modelos
o: Para elegir la semilla del generador aleatorio
a: 1
e: La solución cerrada del GBM es un banco de pruebas: permite medir el error fuerte y débil del esquema contra una verdad conocida. No dice nada sobre qué modelo se parece más al mercado.
:::
