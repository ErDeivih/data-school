---
id: simulacion-de-monte-carlo
titulo: Simulación de Monte Carlo
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [variable-aleatoria, bootstrap, maximo-drawdown]
tags: [simulacion, incertidumbre, bootstrap, backtest]
resumen: En vez de mirar la única curva que te dio el backtest, generas miles de curvas alternativas a partir de tus resultados y miras el abanico completo.
fuentes: ["Metropolis y Ulam (1949), 'The Monte Carlo Method'", "Efron y Tibshirani (1993), 'An Introduction to the Bootstrap'"]
---

## En una frase

La simulación de Monte Carlo genera miles de versiones alternativas de tu histórico para que
veas el abanico de resultados posibles —y sobre todo el abanico de caídas posibles— en lugar de
la única curva que te tocó.

## La idea

Un backtest es **una** trayectoria de entre muchísimas. Las mismas diez operaciones, en otro
orden, dan el mismo resultado final y una curva completamente distinta. Y si el futuro se
parece a tu muestra pero no es exactamente tu muestra, el resultado también cambia. Monte Carlo
ataca las dos preguntas:

- **¿Y si las operaciones hubieran venido en otro orden?** Esto se responde barajando tu propia
  secuencia, sin cambiar el conjunto de resultados. El total no se mueve (multiplicar es
  conmutativo) pero el [[maximo-drawdown]] sí, y a veces muchísimo.
- **¿Y si el futuro fuera otra muestra parecida a mi histórico?** Esto se responde
  remuestreando con reemplazo, que es lo que hace el [[bootstrap]]: sacas operaciones de tu
  histórico al azar, tantas como tenías, y algunas salen repetidas y otras no salen.

La tercera vía es suponer un modelo (por ejemplo, retornos normales con una media y una
desviación estimadas) y simular desde ahí. Es la más rápida y la más peligrosa, porque el modelo
decide las colas y las colas son justo lo que quieres medir.

Lo que Monte Carlo **no** hace es darte información nueva. No predice el futuro ni convierte una
muestra mala en buena: reordena y reexpresa la incertidumbre que ya estaba en tus datos. Si tu
histórico es de tres años tranquilos, las mil curvas que generes también serán tranquilas. Es
una herramienta para dejar de engañarte con un solo número, no una bola de cristal.

Aun así, cambia decisiones. Un backtest que dice «+12 % y caída máxima del 2 %» invita a
arrancar mañana. El mismo backtest con la distribución completa dice «+12 % de mediana, 11 % de
probabilidad de acabar en pérdidas y una caída máxima que en el percentil 95 llega al 7,9 %».
Con eso ya puedes decidir si el tamaño de tu posición es razonable.

## Definición formal

Tienes `N` resultados observados `r₁, …, r_N` (en múltiplos de `R`, es decir, en unidades de lo
que arriesgas por operación) y una fracción de riesgo `r` por operación. La curva de capital de
una réplica es:

:::formula
C_k = C_0 · ∏ (1 + r · r*_j)   para j = 1 … N
:::

- `N` — número de operaciones del histórico.
- `r` — fracción del capital que arriesgas en cada operación (por ejemplo, 0,02).
- `r*_j` — resultado remuestreado de la operación `j`, en múltiplos de `R`.
- `C_0` — capital inicial; `C_k` — capital tras `k` operaciones.
- `B` — número de réplicas simuladas (miles o decenas de miles).
- `T` — el estadístico que te interesa: resultado final, caída máxima, duración, etc.

**Remuestreo con reemplazo (bootstrap):** cada `r*_j` se extrae de forma independiente y con la
misma probabilidad `1/N` de entre los `N` valores observados. Repitiendo `B` veces obtienes `B`
valores de `T`, y con ellos una distribución empírica.

**Permutación (barajado):** se extrae una permutación aleatoria de los índices sin reemplazo. El
conjunto de resultados es el mismo, así que `T` solo cambia si depende del orden.

**Error de Monte Carlo.** La media de las `B` réplicas es en sí misma una estimación, con error
típico `s_T / √B`, donde `s_T` es la desviación típica de `T` entre réplicas. Con `B = 20.000`
ese error es pequeño, pero conviene mirarlo: si el error de Monte Carlo es del mismo tamaño que
la incertidumbre que estás midiendo, has simulado poco.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | Número de operaciones del histórico que se remuestrea | operaciones | Es el tamaño de la muestra de la que sale todo: con 10 operaciones el abanico es enorme y con 1.000 se estrecha. Monte Carlo no añade información, así que `N` bajo da muchas réplicas de una muestra pobre |
| `r` | Fracción del capital que arriesgas en cada operación | tanto por uno (0,02 es un 2 %) | Multiplica cada resultado antes de componer: doblar `r` dobla el resultado final en unidades de `R`, pero mucho más que dobla la caída máxima. Es la palanca que separa dos backtests con las mismas operaciones |
| `r*_j` | Resultado remuestreado de la operación `j`, en múltiplos de `R` | múltiplos de `R` | En el bootstrap puede repetirse y en el barajado no. Un `r*` de +3 saliendo cinco veces cambia el total; con el mismo conjunto barajado, el total es inmutable |
| `C_k` | Capital después de `k` operaciones | euros o base 1 | Se compone multiplicando, no sumando: por eso el orden no cambia el valor final y por eso un −100 % no se recupera con un +100 % |
| `B` | Número de réplicas simuladas | réplicas | Baja el error de Monte Carlo como `1/√B`: para dividirlo por dos hacen falta cuatro veces más réplicas. Por encima de 20.000 el error ya suele ser menor que la incertidumbre que estás midiendo |
| `T` | El estadístico que te interesa de cada réplica: resultado final, caída máxima o duración | lo que corresponda | Es lo que se mira al final y lo que decide la conclusión. La media de `T` sin su percentil 5 es media información: la otra mitad está en la dispersión |
| `s_T` | Desviación típica de `T` entre las `B` réplicas | las mismas que `T` | Fija el error de Monte Carlo `s_T/√B`. Si es del orden de lo que quieres medir, has simulado poco o el sistema tiene demasiada varianza para distinguir nada |
:::

:::trampa
Barajar y remuestrear no son lo mismo y responden a preguntas distintas. Barajar conserva
exactamente tus operaciones y solo cambia el orden: sirve para el drawdown. Remuestrear con
reemplazo cambia el conjunto y puede repetir la peor operación cinco veces: sirve para el
resultado final, y es más pesimista en las colas. Si mezclas las dos y lo llamas «Monte Carlo»,
no sabrás qué pregunta estás respondiendo.
:::

:::figura
fichero: monte-carlo-barajar-y-remuestrear
pie: A la izquierda están las mismas diez operaciones en 400 de los 20.000 órdenes posibles, con el orden que te tocó en azul: todas las curvas acaban exactamente en el mismo punto, +12,22 %, porque el capital final es un producto y la multiplicación es conmutativa. Lo que sí cambia es el camino: este orden concreto cayó un 2,04 % desde su máximo y la mediana de los 20.000 órdenes es del 3,96 %. Tu backtest salió más suave de lo normal por pura suerte con el orden. A la derecha, el remuestreo **con reemplazo** sí mueve el total: la mediana sigue en +12,22 %, pero el 5 % peor acaba por debajo de −2,38 % y las barras rojas son los mundos que terminan en pérdidas. Barajar responde «¿y si el orden hubiera sido otro?»; remuestrear responde «¿y si el histórico hubiera sido otro parecido?».
fuente: figuras/simulacion-de-monte-carlo-1.py
:::

## Ejemplo

Diez operaciones de un sistema, en múltiplos de `R`:

```
+2   +1   -1   +3   -1   +1   -1   +2   -1   +1     (suma = +6R)
```

Con un 2 % de riesgo por operación, la secuencia tal como ocurrió da:

- Resultado final: **+12,22 %**.
- Caída máxima: **2,04 %**.

Ahora remuestreamos con reemplazo 20.000 veces:

- Mediana del resultado final: **+12,22 %**. El bootstrap reproduce la muestra, así que el centro
  apenas se mueve.
- Percentil 5 del resultado: **−2,38 %**. Es decir, en el 5 % de los mundos simulados acabas el
  año en pérdidas.
- Probabilidad de acabar en pérdidas: **11,27 %**.
- Caída máxima mediana: **3,96 %**. Percentil 95 de la caída: **7,87 %**.

Y si solo barajamos el orden, 20.000 veces:

- El resultado final es siempre **+12,2218 %**, exactamente el mismo, porque el producto no
  depende del orden.
- Tu orden real tenía una caída del 2,04 %; la mediana de los 20.000 órdenes es del 3,96 % y el
  peor llega al 7,76 %. Tu backtest salió **más suave de lo normal**, simplemente por suerte con
  el orden.

Esa última frase es la razón de existir de esta técnica: un backtest concreto siempre parece
mejor o peor de lo que es, y Monte Carlo te dice cuánto.

## Código

```python verificable
import numpy as np

# 10 operaciones en multiplos de R (lo que arriesgas en cada una) de un sistema ya probado
rs = np.array([2.0, 1.0, -1.0, 3.0, -1.0, 1.0, -1.0, 2.0, -1.0, 1.0])
riesgo = 0.02                                 # 2 % del capital por operacion

original = np.cumprod(1 + riesgo * rs)
picos = np.maximum.accumulate(original)
print(f"total de la muestra {rs.sum():+.0f}R")                                  # -> +6R
print(f"resultado del orden real {original[-1] - 1:+.2%}")                     # -> +12.22%
print(f"caida del orden real {((picos - original) / picos).max():.2%}")        # -> 2.04%

# Monte Carlo: remuestreamos con reemplazo para ver el abanico de resultados.
rng = np.random.default_rng(0)
muestras = rng.choice(rs, size=(20_000, rs.size), replace=True)
curvas = np.cumprod(1 + riesgo * muestras, axis=1)
picos = np.maximum.accumulate(curvas, axis=1)
dd = ((picos - curvas) / picos).max(axis=1)
final = curvas[:, -1] - 1

print(f"mediana final {np.median(final):+.2%}")            # -> +12.22%
print(f"percentil 5   {np.percentile(final, 5):+.2%}")     # -> -2.38%
print(f"caida mediana {np.median(dd):.2%}")                # -> 3.96%
print(f"caida p95     {np.percentile(dd, 95):.2%}")        # -> 7.87%
print(f"acaba en perdidas {(final < 0).mean():.2%}")       # -> 11.27%
```

:::claves
- `np.cumprod(..., axis=1)` compone **dentro de cada fila**, que es una réplica. Sin el `axis=1` la función aplana la matriz entera y devuelve un vector largo: no salta ningún error, pero los drawdowns dejan de significar nada. Es el fallo más silencioso de todo el bloque.
- `np.maximum.accumulate(curva)` devuelve el máximo **hasta cada punto**, que es el pico contra el que se mide la caída. Cambiarlo por `curva.max()` da el máximo de toda la serie en todas las posiciones y el drawdown sale mal.
- `replace=True` es lo que distingue el bootstrap del barajado. Con `replace=False`, `rng.choice` devuelve una permutación y el resultado final sería idéntico en las 20.000 réplicas: el panel derecho de la figura se quedaría en una sola barra.
- `size=(20_000, rs.size)` fija dos cosas a la vez: cuántas réplicas y cuántas operaciones por réplica. Si pones solo `size=10` obtienes diez números sueltos y el `axis=1` de la línea siguiente revienta; si inviertes las dos cifras, simulas 10 réplicas de 20.000 operaciones.
- `curvas[:, -1] - 1` convierte el capital en rentabilidad. Sin el `- 1` el número que se imprime es 1,1222, que parece un 112 % y es un multiplicador. El `- 1` es la diferencia entre informar y desinformar.
- `np.median(final)` y `np.percentile(final, 5)` no son la media: la mediana te dice dónde está el centro y el percentil 5, dónde está la cola. La media de un producto de factores está dominada por los pocos caminos que se disparan y describe a casi nadie.
:::

```python verificable
import numpy as np

# Barajar solo cambia el orden, no el conjunto: el total no se mueve nunca.
rs = np.array([2.0, 1.0, -1.0, 3.0, -1.0, 1.0, -1.0, 2.0, -1.0, 1.0])
rng = np.random.default_rng(1)

def caida_maxima(curva):
    picos = np.maximum.accumulate(curva)
    return float(((picos - curva) / picos).max())

original = np.cumprod(1 + 0.02 * rs)
dds = [caida_maxima(np.cumprod(1 + 0.02 * rng.permutation(rs))) for _ in range(20_000)]

print(f"total original  {original[-1] - 1:+.4%}")      # -> +12.2218%
print(f"caida real      {caida_maxima(original):.2%}")  # -> 2.04%
print(f"caida mediana   {np.median(dds):.2%}")          # -> 3.96%
print(f"peor de 20.000  {np.max(dds):.2%}")             # -> 7.76%
```

```python ilustrativo
import numpy as np

# Version con modelo: en vez de remuestrear, suponemos una distribucion.
# Aqui se ve el peligro: las colas las decide el supuesto, no los datos.
rng = np.random.default_rng(0)
mu_mensual, sigma_mensual, meses = 0.008, 0.05, 120
retornos = rng.normal(mu_mensual, sigma_mensual, size=(20_000, meses))
curvas = np.cumprod(1 + retornos, axis=1)

# Una t de Student con los mismos dos primeros momentos tiene colas mas gruesas.
retornos_t = mu_mensual + sigma_mensual * rng.standard_t(df=4, size=(20_000, meses)) / np.sqrt(2)
curvas_t = np.cumprod(1 + retornos_t, axis=1)

for nombre, c in (("normal", curvas), ("t de Student", curvas_t)):
    picos = np.maximum.accumulate(c, axis=1)
    dd = ((picos - c) / picos).max(axis=1)
    print(nombre, "caida maxima p99", np.percentile(dd, 99))
```

## Errores típicos

- **Creer que Monte Carlo predice el futuro.** No añade información: reexpresa la incertidumbre
  de tu muestra. Si la muestra es mala, las 20.000 réplicas también lo son. Solo cambia la
  forma de contarlo.
- **Cambiar solo el orden y llamarlo simulación completa.** Barajar responde a «¿y si el orden
  hubiera sido otro?», que es una pregunta útil pero limitada: el total final es idéntico
  siempre. Si quieres explorar resultados finales, remuestrea con reemplazo.
- **Suponer independencia cuando tus resultados están autocorrelacionados.** Si las operaciones
  van en rachas (porque el régimen manda, como en [[regimenes-de-mercado]]), remuestrear
  operaciones sueltas destruye esa estructura y **subestima** las caídas. Para eso se remuestrean
  bloques, no operaciones individuales.
- **Simular con una normal y creerte la cola.** Una normal genera muy pocos extremos; la
  diferencia en el percentil 99 del drawdown entre una normal y una t de Student con la misma
  varianza es enorme. Si la cola importa, simula con colas gruesas o con datos reales.
- **Reportar la media y no la dispersión.** «El resultado esperado es +12 %» es la mitad de la
  información. La otra mitad es el percentil 5, la probabilidad de acabar en pérdidas y la
  distribución de la caída máxima.
- **Hacer Monte Carlo sobre la muestra donde elegiste la estrategia.** Si escogiste las 10
  operaciones porque eran las mejores de un backtest más largo, el sesgo se propaga intacto a
  las 20.000 réplicas. Monte Carlo no arregla el sesgo de selección
  ([[data-snooping-y-multiple-testing]]).

:::practica
enunciado: Un sistema arriesga el 2 % del capital por operación y su histórico en múltiplos de R es +1, +2, −1, −1, +3. Calcula el resultado final y la caída máxima. Después reordena a +1, +2, +3, −1, −1 y comprueba qué estadístico cambia y cuál no.
pista: Multiplica los factores 1 + 0,02 · r en orden y compara cada capital con el máximo alcanzado hasta ahí.
solucion: Los factores son 1,02 · 1,04 · 0,98 · 0,98 · 1,06 = 1,07992, luego el resultado es +7,99 %. El capital pasa por 1,02, 1,0608, 1,03958, 1,01879 y 1,07992; el máximo antes de la caída es 1,0608, así que la caída máxima es 1 − 1,01879 / 1,0608 = 3,96 %. Con el orden reordenado el final es idéntico, +7,99 %, y la caída también, 3,96 %: barajar mueve el camino, no siempre el drawdown.
:::

## Comprueba que lo sabes

:::quiz
p: Barajas 20.000 veces las diez operaciones de un backtest. ¿Qué cambia y qué no?
o: Cambia el resultado final y también la caída máxima
o: No cambia el resultado final —el producto no depende del orden— pero sí cambia la caída máxima
o: No cambia nada, porque son las mismas operaciones
a: 2
e: El capital final es un producto de factores y la multiplicación es conmutativa, así que el total es idéntico en las 20.000 réplicas. La curva, en cambio, es distinta en cada orden, y con ella la caída máxima y su duración.
:::

:::quiz
p: ¿Qué diferencia hay entre remuestrear con reemplazo y barajar sin reemplazo?
o: El remuestreo puede repetir operaciones y por eso cambia el resultado final; el barajado conserva el conjunto exacto y solo cambia el orden
o: El barajado es más lento y por eso es más fiable
o: Son lo mismo, solo cambia la semilla del generador aleatorio
a: 1
e: Con reemplazo, la peor operación puede aparecer tres veces en una réplica y ninguna en otra, así que el total se mueve. Sin reemplazo, cada operación aparece exactamente una vez y el total queda fijado. Son dos preguntas distintas y hay que elegir la que corresponda.
:::

:::quiz
p: Tu histórico tiene un drawdown máximo del 3 % y la simulación por barajado da una mediana del 6 % con un percentil 95 del 12 %. ¿Qué conclusión es correcta?
o: Que el backtest tuvo suerte con el orden y que la caída típica de este sistema es mayor de lo que sugiere el único número que viste
o: Que la simulación se ha equivocado, porque el drawdown real fue del 3 %
o: Que el sistema tiene un drawdown garantizado del 12 %
a: 1
e: El 3 % es una de las muchas caídas posibles y resultó ser de las suaves. La mediana del 6 % describe mejor el comportamiento esperable. Nada garantiza el 12 %: es un percentil, no un máximo, y la muestra sigue siendo la misma de siempre.
:::
