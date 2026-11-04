---
id: rebalanceo
titulo: Rebalanceo
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [construccion-de-carteras, markowitz-y-frontera, retornos-logaritmicos]
tags: [cartera, costes, riesgo, disciplina]
resumen: Devolver la cartera a sus pesos objetivo, por calendario o por banda: cuánto cuesta de verdad y por qué es una decisión de riesgo y no de rentabilidad.
fuentes: ["Magill y Constantinides (1976), 'Portfolio Selection with Transactions Costs'", "Davis y Norman (1990), 'Portfolio Selection with Transaction Costs'"]
---

## En una frase

Rebalancear es volver a poner la cartera en los pesos que decidiste, vendiendo lo que se ha
ido hacia arriba y comprando lo que se ha quedado atrás, y la pregunta interesante no es si
hacerlo, sino cada cuánto y a qué coste.

## La idea

Una cartera 60/40 con 100.000 € empieza con 60.000 € en bolsa y 40.000 € en bonos. Si la bolsa
sube un 50 % en un año y los bonos se quedan igual, la cartera vale 130.000 € pero ya no es
60/40: son 90.000 € de bolsa sobre 130.000 €, un **69,2 %**. Has pasado de una cartera que
aguantabas a otra con más riesgo del que elegiste, sin tomar ninguna decisión. Ese es el
problema que resuelve el rebalanceo: sin él, tus pesos son el resultado de lo que mejor lo ha
hecho, no de lo que tú querías.

Rebalancear tiene una consecuencia incómoda: es **contrario por construcción**. Te obliga a
vender lo que sube y comprar lo que baja, que es justo lo que apetece menos. Si la bolsa lleva
tres años ganando, rebalancear te hace reducirla una y otra vez, y en una muestra con tendencia
fuerte habrás ganado algo menos que quien no hizo nada. Lo que compras a cambio es que el riesgo
de la cartera se mantenga donde lo pusiste: en el ejemplo, la volatilidad mensual baja del
1,53 % al 1,42 % y la caída máxima del 5,04 % al 4,26 %. El rebalanceo no promete más
rentabilidad; promete que la cartera siga siendo la tuya.

Hay dos formas de decidir cuándo hacerlo:

- **Por calendario.** Cada mes, cada trimestre o cada año, sin mirar cómo van los pesos. Es
  predecible, fácil de automatizar y fácil de explicar. Su defecto es que a veces mueve la
  cartera por moverla (un desvío de 0,3 puntos no merece una operación) y otras veces deja
  pasar meses con un desvío enorme.
- **Por banda o umbral.** Se define un desvío máximo tolerado (por ejemplo 5 puntos
  porcentuales en cualquier activo) y se actúa cuando se cruza. Se opera menos y se deja correr
  la tendencia, a cambio de que las fechas de operación sean irregulares y de tener que
  vigilarlo.

En los dos casos el coste se mide igual: por el **notional** que cambia de manos multiplicado por
el coste por unidad negociada (comisión más deslizamiento). Ese coste es más pequeño de lo que
la intuición sugiere: devolver la cartera del ejemplo a 60/40 mueve 12.000 € en cada lado y, a
5 puntos básicos por pata, cuesta **12 €** sobre 130.000 €, un 0,009 %. Un rebalanceo anual
cuesta eso una vez al año. Lo que sí se acumula es rebalancear muchas veces con bandas
diminutas, o rebalancear contra estimaciones que cambian todos los días.

Dos matices que cambian la práctica. El primero: si haces aportaciones periódicas, dirige el
dinero nuevo al activo que se ha quedado corto; es un rebalanceo con coste cero y sin vender
nada, lo que además evita el posible hecho fiscal de las ventas. El segundo: rebalancear **no**
es lo mismo que mantener la volatilidad objetivo. Si tu cartera es 60/40 y la volatilidad de la
bolsa se duplica, los pesos siguen igual y el riesgo de la cartera no: eso se corrige con
[[tamano-de-posicion]], que ajusta exposición según la volatilidad, no según los pesos.

## Definición formal

Sea una cartera con `n` activos, valor total `V` y valor `Vᵢ` en el activo `i`.

- `wᵢ = Vᵢ / V` — peso actual del activo `i`. Se cumple `Σ wᵢ = 1`.
- `wᵢ*` — peso objetivo, el que decidiste (por ejemplo 0,60 y 0,40).
- `dᵢ = wᵢ − wᵢ*` — desvío del activo `i` respecto a su objetivo.
- **Regla de calendario:** rebalancear cuando `t` es múltiplo de `k` periodos.
- **Regla de banda:** rebalancear cuando `maxᵢ |dᵢ| > b`, con `b` la banda en tanto por uno
  (0,05 son 5 puntos porcentuales).
- `T = ½ Σᵢ |wᵢ* − wᵢ|` — **turnover** en una dirección: la fracción del valor de la cartera que
  cambia de manos si se vuelve al objetivo exacto. El factor ½ evita contar dos veces la misma
  operación (lo que se vende de un activo se compra en otro).
- `c` — coste por unidad negociada, en tanto por uno: comisión, diferencial y deslizamiento.
  Para acciones líquidas, unos pocos puntos básicos por operación es un orden de magnitud
  razonable; para activos ilíquidos puede ser un porcentaje entero.
- **Coste del rebalanceo:** `coste = T · V · c`.

Tres consecuencias que se deducen de esas definiciones:

1. **El coste es proporcional al desvío, no al número de activos.** Rebalancear una cartera que
   se ha desviado 1 punto cuesta una quinta parte que rebalancear una que se ha desviado 5.
2. **Los desvíos crecen con la raíz del tiempo, no linealmente.** La diferencia de pesos entre
   dos activos se comporta como un paseo aleatorio cuya escala crece con `σ · √t`, donde `σ` es
   la volatilidad de la diferencia de retornos. Cruzar una banda `b` tarda, en orden de
   magnitud, un tiempo proporcional a `(b/σ)²`. Por eso doblar la banda no tarda el doble:
   tarda unas cuatro veces más. Es la razón de que las bandas anchas operen tan poco.
3. **El rebalanceo del objetivo exacto no es óptimo con costes.** Si cada operación cuesta,
   conviene una zona muerta alrededor del objetivo en lugar de un punto. En los modelos clásicos
   de control con coste proporcional, el ancho de esa zona crece con el coste (de forma lenta,
   aproximadamente con su raíz cúbica) y con la volatilidad.

:::figura
fichero: rebalanceo-deriva-y-bandas
pie: A la izquierda, el peso de la bolsa en una cartera 60/40 a lo largo de cinco años. En azul, sin tocar nada: el peso se va solo hasta el 53 % y nadie ha tomado esa decisión. En naranja, la misma cartera con una banda de 5 puntos: solo se opera al cruzar la línea roja y cada operación (los puntos) devuelve el peso al 60 %; en cinco años se operó dos veces. A la derecha, cuántos rebalanceos hacen falta según el ancho de la banda, en escala logarítmica: la referencia de puntos baja con pendiente −2, es decir, doblar la banda tarda unas cuatro veces más en cruzarse, y por eso las bandas anchas operan tan poco.
fuente: figuras/rebalanceo-1.py
:::

## Ejemplo

La cartera del principio, con números redondos: 60.000 € en bolsa y 40.000 € en bonos; la bolsa
sube un 50 %, los bonos no se mueven.

- Valor total: 90.000 + 40.000 = **130.000 €**.
- Peso de la bolsa: 90.000 / 130.000 = **0,6923**, es decir un desvío de **9,2 puntos** sobre el
  60 % objetivo.
- Para volver al 60 % hay que dejar 0,60 · 130.000 = 78.000 € en bolsa: se venden 12.000 € de
  bolsa y se compran 12.000 € de bonos.
- Coste a 5 puntos básicos por pata: 12.000 · 0,0005 + 12.000 · 0,0005 = **12 €**, el 0,0092 %
  de la cartera.

Y la comparación de políticas sobre 60 meses de una cartera 60/40, con coste de 10 puntos
básicos por unidad de notional negociado:

| Política | Valor final | Volatilidad mensual | Caída máxima | Rebalanceos | Coste total |
| --- | --- | --- | --- | --- | --- |
| Sin rebalancear | 143.979 € | 1,53 % | 5,04 % | 0 | 0 € |
| Anual | 142.149 € | 1,42 % | 4,26 % | 5 | 12,64 € |
| Banda de 5 puntos | 142.942 € | 1,42 % | 4,04 % | 2 | 14,48 € |

La lectura correcta no es «rebalancear cuesta dinero»: el coste es de 12 € sobre 143.000 € y lo
que cambia de verdad es la volatilidad y la caída máxima. La cartera anual acaba con 1.830 €
menos que la que no se tocó, y eso es el precio de haber vendido bolsa durante una racha
alcista; con otra muestra, el signo se invierte. El coste de las comisiones es un detalle al
lado de la decisión de riesgo.

## Código

```python verificable
# El desvio se ve con un solo movimiento grande: la bolsa sube un 50 %.
v_eq, v_bd = 60000.0, 40000.0
v_eq *= 1.50
total = v_eq + v_bd
print("valor de la cartera:", total)                                            # -> valor de la cartera: 130000.0
print("peso de la bolsa:", round(v_eq / total, 4))                              # -> peso de la bolsa: 0.6923
print("desvio en puntos porcentuales:", round(100 * (v_eq / total - 0.60), 1))  # -> desvio en puntos porcentuales: 9.2
print("notional que cambia de manos:", abs(0.60 * total - v_eq))                # -> notional que cambia de manos: 12000.0
coste = abs(0.60 * total - v_eq) * 0.0005 * 2                                   # 5 pb por cada pata
print("coste del rebalanceo:", coste)                                           # -> coste del rebalanceo: 12.0
print("en porcentaje de la cartera:", round(100 * coste / total, 4))            # -> en porcentaje de la cartera: 0.0092
```

:::claves
- `v_eq *= 1.50` modifica el número **en el sitio**: en Python los floats son inmutables, así que lo que cambia es el nombre `v_eq`, no el valor `60000.0`. Parece una tontería, pero si esa variable fuera una fila de un DataFrame estarías escribiendo en el original.
- `abs(0.60 * total - v_eq)` es el notional que cambia de manos **a un lado**: lo que se vende de bolsa se compra de bonos, así que el coste total lleva un factor 2. Olvidarlo deja el coste a la mitad.
- `statistics.stdev` divide entre `n − 1` (igual que `np.var(ddof=1)`), pero `statistics.pstdev` y `np.var()` a secas dividen entre `n`. Con 60 meses la diferencia es del 1,7 % en volatilidad; con 12 meses, del 4,5 %.
- `politica == "anual" and t % 12 == 11` opera al **final** del mes 11 de cada año. Si lo cambias a `t % 12 == 0`, rebalanceas en enero de cada año: el número de operaciones no cambia, pero el valor final sí, y no por una razón de fondo.
- El coste se resta del total **antes** de recolocar los pesos (`total -= negociado * coste`). Si lo restas después, estás repartiendo un dinero que ya no tienes y la cartera se queda con más valor del real; el error es pequeño pero crece con el número de rebalanceos.
:::

```python verificable
import statistics

# Series propias con un generador congruencial, para que el ejemplo no dependa
# de la version de la libreria ni de la semilla de un generador ajeno.
def uniformes(n, semilla=12345):
    x, salida = semilla, []
    for _ in range(n):
        x = (1103515245 * x + 12345) % (2 ** 31)
        salida.append(x / 2 ** 31)
    return salida

u = uniformes(120)
r_eq = [0.008 + 0.045 * (2 * x - 1) for x in u[:60]]   # bolsa: en torno al 0,8 % mensual
r_bd = [0.002 + 0.006 * (2 * x - 1) for x in u[60:]]   # bonos: en torno al 0,2 % mensual

def simular(politica, umbral=0.05, coste=0.001):
    v_eq, v_bd, ops, pagado = 60000.0, 40000.0, 0, 0.0
    pico, caida, retornos = 100000.0, 0.0, []
    for t in range(60):
        inicio = v_eq + v_bd
        v_eq *= (1 + r_eq[t])
        v_bd *= (1 + r_bd[t])
        total = v_eq + v_bd
        if (politica == "anual" and t % 12 == 11) or \
           (politica == "umbral" and abs(v_eq / total - 0.60) >= umbral):
            negociado = abs(0.60 * total - v_eq)       # notional que cambia de manos
            total -= negociado * coste                 # el coste sale de la cartera
            v_eq, v_bd = 0.60 * total, 0.40 * total
            ops += 1
            pagado += negociado * coste
        retornos.append((v_eq + v_bd) / inicio - 1)
        pico = max(pico, v_eq + v_bd)
        caida = max(caida, 1 - (v_eq + v_bd) / pico)
    return v_eq + v_bd, retornos, caida, ops, pagado

print(f"{'politica':>16} {'valor final':>12} {'vol mensual':>12} {'caida max':>10} {'ops':>5} {'coste':>8}")
for politica, nombre in (("nada", "sin rebalancear"), ("anual", "anual"), ("umbral", "umbral 5 pp")):
    valor, rets, caida, ops, pagado = simular(politica)
    print(f"{nombre:>16} {valor:>12,.0f} {statistics.stdev(rets):>12.4f} {caida:>10.4f} {ops:>5} {pagado:>8.2f}")
```

```python ilustrativo
# Rebalancear con dinero nuevo: si aportas cada mes, dirige la aportacion al
# activo que se ha quedado corto. Es la forma mas barata de rebalancear.
aportacion = 500.0
w_objetivo = {"bolsa": 0.60, "bonos": 0.40}
valor = {"bolsa": 90000.0, "bonos": 40000.0}
total = sum(valor.values()) + aportacion
corto = min(valor, key=lambda a: valor[a] / total - w_objetivo[a])
valor[corto] += aportacion          # sin vender nada: no hay comision de venta ni plusvalia
print(f"la aportacion va a {corto}, el activo mas alejado por debajo de su objetivo")
```

## Errores típicos

- **Confundir rebalanceo con timing.** Rebalancear no predice nada: no dice que la bolsa vaya a
  bajar, dice que tu cartera se ha desviado de lo que decidiste. Si lo usas como señal de
  entrada o salida, estás haciendo otra cosa y con otra justificación.
- **No rebalancear nunca «para dejar correr los ganadores».** En el ejemplo, un año bueno lleva
  la cartera del 60 % al 69,2 % de bolsa. Diez años así y tienes una cartera de renta variable
  con un apellido. El riesgo que asumes deja de ser el que elegiste, y la caída máxima también.
- **Rebalancear con demasiada frecuencia y bandas minúsculas.** Una banda de 1 punto sobre una
  cartera que se mueve un 4 % al mes se cruza casi cada mes: pagas comisión y deslizamiento por
  ruido, y encima vendes para volver a comprar lo mismo. Las bandas útiles se miden en puntos
  porcentuales, no en décimas.
- **Mirar solo la comisión del bróker.** El coste real incluye el diferencial, el deslizamiento
  (más grande en activos pequeños o en momentos de estrés) y el posible hecho fiscal de vender
  con ganancias. Con un 0,5 % de coste por operación, un rebalanceo trimestral se come un 2 %
  anual de la cartera, que es más que la mayoría de las ventajas que crees estar capturando.
- **Rebalancear vendiendo cuando tienes aportaciones periódicas.** Si entra dinero nuevo cada
  mes, el rebalanceo puede hacerse entero con ese flujo: cero ventas, cero comisiones de venta.
  Es el mismo resultado sin coste.
- **Creer que rebalancear entre activos muy correlacionados diversifica.** Si dos activos se
  mueven juntos, intercambiar pesos entre ellos no cambia el riesgo de la cartera. Mira la
  [[covarianza-y-correlacion|correlación]] antes de construir una regla que solo mueve ruido.

:::practica
enunciado: Una cartera 70/30 vale 125.000 €, con 87.500 € en bolsa y 37.500 € en bonos. La bolsa cae un 10 % y los bonos no se mueven. Calcula el peso resultante de la bolsa, el notional que hay que mover y el coste a 6 puntos básicos por pata.
pista: Recalcula el valor de cada pata y el total; compara la bolsa con el 70 % del total nuevo.
solucion: La bolsa pasa a 87.500 · 0,90 = 78.750 € y el total a 116.250 €. Su peso es 78.750 / 116.250 = 0,6774, un desvío de 2,26 puntos por debajo del 70 %. Para volver al objetivo hay que tener 0,70 · 116.250 = 81.375 € en bolsa: se compran 2.625 € y se venden 2.625 € de bonos. El coste es 2.625 · 0,0006 · 2 = 3,15 €, un 0,0027 % de la cartera.
:::

## Comprueba que lo sabes

:::quiz
p: Una cartera 60/40 empieza con 100.000 € y la bolsa sube un 50 % mientras los bonos no se mueven. ¿Qué hay que hacer para volver al 60/40 y cuánto cuesta a 5 puntos básicos por pata?
o: Comprar 12.000 € de bolsa; cuesta 6 €
o: Vender 12.000 € de bolsa y comprar 12.000 € de bonos; cuesta 12 €
o: Vender 9.200 € de bolsa; cuesta 4,60 €
a: 2
e: La cartera vale 130.000 € y la bolsa pesa 90.000 (el 69,2 %). Para volver al 60 % hay que dejar 78.000 € en bolsa, así que se venden 12.000 € y se compran 12.000 € de bonos. A 5 puntos básicos por pata, son 6 € por cada lado, 12 € en total: el 0,0092 % de la cartera.
:::

:::quiz
p: ¿Por qué una banda de rebalanceo más ancha reduce tanto el número de operaciones?
o: Porque el desvío entre pesos crece como la raíz del tiempo, así que el tiempo hasta cruzar la banda crece con el cuadrado de su ancho
o: Porque las bandas anchas solo se revisan una vez al año
o: Porque con bandas anchas se dejan de pagar comisiones
a: 1
e: El desvío se comporta como un paseo aleatorio que escala con la raíz del tiempo, y el tiempo de primer cruce crece con el cuadrado del ancho de la banda. Doblar la banda tarda unas cuatro veces más en cruzarse. Las comisiones se siguen pagando cuando se opera; lo que baja es el número de operaciones.
:::

:::quiz
p: ¿Qué afirmación describe mejor el efecto de rebalancear una cartera 60/40 durante una racha alcista de la bolsa?
o: Aumenta la rentabilidad, porque compra barato y vende caro
o: Suele reducir algo la rentabilidad final y a cambio mantiene el riesgo en el nivel elegido
o: No tiene ningún efecto sobre la rentabilidad ni sobre el riesgo
a: 2
e: Al vender bolsa durante una subida, la cartera deja de capturar parte de esa subida: en el ejemplo acaba con 1.830 € menos. A cambio, la volatilidad mensual baja del 1,53 % al 1,42 % y la caída máxima del 5,04 % al 4,26 %. El signo del efecto sobre la rentabilidad depende de la muestra; el efecto sobre el riesgo es el que buscas.
:::

:::truco
Antes de elegir la frecuencia, calcula cuántas veces habrías operado en los últimos años con esa
regla y multiplica por tu coste real por operación. Si el número que sale te parece pequeño,
adelante; si te obliga a operar casi todos los meses, usa una banda. Y si aportas dinero con
regularidad, empieza por rebalancear con las aportaciones.
:::
