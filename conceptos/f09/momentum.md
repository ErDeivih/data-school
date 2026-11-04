---
id: momentum
titulo: Momentum
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [retornos-logaritmicos, autocorrelacion-acf-pacf, volatilidad-realizada]
tags: [momentum, tendencia, factores, senales]
resumen: Comprar lo que sube funciona en la muestra y duele en la racha: momentum 12-1, por qué se salta el último mes y por qué sus caídas son tan violentas.
fuentes: ["Jegadeesh y Titman (1993), 'Returns to Buying Winners and Selling Losers'", "Asness, Moskowitz y Pedersen (2013), 'Value and Momentum Everywhere'"]
---

## En una frase

El momentum dice que los activos que mejor lo han hecho en los últimos doce meses —saltando
el mes más reciente— tienden a seguir haciéndolo mejor durante unos meses, y que los peores
siguen peor.

## La idea

Estás en una cola de embarque y ves que una cola avanza más rápido que la otra. Cambiarte a
la que avanza no es adivinar el futuro: es aprovechar una diferencia que ya está ocurriendo y
que, por lo general, tarda en corregirse. Momentum es eso: no predice el giro, se sube a lo
que ya se está moviendo. Y funciona porque la información se difunde despacio: cuando una
empresa mejora sus resultados, el mercado no lo incorpora todo el primer día, lo va asimilando
durante semanas o meses.

Hay dos versiones que conviene no mezclar nunca:

- **Momentum de sección cruzada** (el clásico): cada mes ordenas un universo de activos por su
  rentabilidad de los últimos doce meses y compras el decil ganador mientras vendes el
  perdedor. Es una apuesta **relativa**: da igual si el mercado sube o baja.
- **Momentum de serie temporal** (trend following, el mundo de los gestores sistemáticos de
  futuros): miras cada activo por separado y te pones largo si su tendencia es positiva y
  corto si es negativa. Es una apuesta **absoluta** y por eso suele dar refugio en las caídas
  largas, cuando la sección cruzada lo pasa mal.

Momentum tiene una virtud y un defecto, y ambos son grandes. La virtud: es el factor que
mejor se ha replicado fuera de muestra, en acciones, bonos, divisas y materias primas. El
defecto: sus caídas son las peores que verás en una estrategia de factores. El motivo es
mecánico. Momentum va corto en lo que ha caído mucho, y esos son precisamente los activos
más castigados, los más endeudados, los que más suben cuando el pánico termina y el mercado
rebota con violencia. En un rebote fuerte desde un suelo, la pata corta se dispara hacia
arriba y la estrategia pierde justo cuando todo lo demás gana. Los episodios documentados de
estas «momentum crashes» coinciden con rebotes de mercado tras caídas profundas.

## Definición formal

Para un universo de `N` activos y un mes de rebalanceo `t`, el momentum de sección cruzada
de cada activo es:

:::formula
MOM_i,t = Π (1 + r_i,t−k) − 1, con k = 1, 2, …, 12
:::

- `r_i,t−k` — retorno del activo `i` en el mes `t − k` (en tanto por uno, o su logaritmo, si
  trabajas con [[retornos-logaritmicos|retornos logarítmicos]]).
- `k = 0` **se excluye**: `r_i,t` es el mes en curso y no entra en el producto. Los doce
  factores del producto son los doce meses anteriores al mes en curso, y de ahí el nombre
  «12-1»: doce meses de formación, uno de espera.
- Con `N` activos ordenados por `MOM`, la cartera es: largo igual ponderado en el decil
  superior, corto igual ponderado en el decil inferior, rebalanceada cada mes.

La versión de serie temporal es más simple todavía:

:::formula
señal_i,t = signo( Π (1 + r_i,t−k) ), con k = 1, 2, …, 12
:::

`signo(·)` vale +1 si el producto es mayor que 1 y −1 si es menor. La posición es +1 o −1
sobre el activo, habitualmente escalada por volatilidad para que todos los activos aporten
riesgo parecido.

:::figura
fichero: momentum-quintiles-y-desplome
pie: A la izquierda, la cartera de juguete ordenada por la señal 12-1: las dos curvas parten de 1 euro y se separan, un +20 % para el decil ganador y un −72 % para el perdedor. Lo que cobra la estrategia es esa distancia, no la subida de uno de los dos. A la derecha, la misma cartera larga-corta mes a mes: crece, pero tres veces se hunde alrededor de un 16 % en dos meses. Esos tramos sombreados son los rebotes desde un suelo, justo cuando los valores que lleva en corto son los que más suben.
fuente: figuras/momentum-1.py
:::

Dos detalles que deciden si el backtest es real o es fantasía:

1. **El momento de la decisión.** La señal se calcula con los precios del cierre del último
   día del mes `t`. La operación se ejecuta al día siguiente (o al precio de apertura). Si
   usas el cierre del propio mes `t + 1` para decidir, tienes
   [[sesgo-de-mirar-al-futuro|mirar al futuro]].
2. **El giro que implica.** Cada mes la composición de los deciles cambia y hay que recolocar
   posiciones. El momentum de doce meses con rebalanceo mensual tiene un giro alto, y en el
   decil de perdedores parte de los activos son caros o imposibles de vender en corto.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `MOM_i,t` | La rentabilidad acumulada del activo `i` en la ventana de formación: la señal | tanto por uno por ventana | Es lo que se ordena, no lo que se gana. Dos activos con el mismo `MOM` pueden tener recorridos muy distintos, y el `MOM` de un activo muy volátil se mueve mucho más de un mes a otro |
| `r_i,t−k` | Retorno del activo `i` en el mes `t − k`, en tanto por uno | tanto por uno por mes | Entran los doce meses anteriores. Cuanto más atrás va el retardo, menos pesa en la práctica en el producto (cada factor multiplica), pero un mes extremo dentro de la ventana arrastra el acumulado durante once meses más |
| `k` | El retardo de la ventana de formación: `k = 1, 2, …, 12` | meses | Cuanto mayor es la ventana, más lenta es la señal y menos giro genera, pero también más se mezclan regímenes distintos. Con `k` arrancando en 0 en lugar de 1 metes el mes en curso y aparecen los problemas del ejemplo |
| `N` | Número de activos del universo | activos | Con pocos activos los deciles son grupos diminutos y el resultado depende de dos o tres nombres; con muchos, la cartera se acerca a un factor pero el coste de operar los extremos crece |
| `signo(·)` | La función que convierte el acumulado en +1 o −1 para la versión de serie temporal | adimensional, ±1 | Es una función escalón: no distingue entre un acumulado de +0,1 % y uno de +50 %. Si quieres graduar la exposición, hay que sustituirla por el propio acumulado normalizado o escalarlo por volatilidad |
| Ventana de la señal (12-1) | Los doce meses de formación saltando el mes en curso | meses | Es el parámetro que más cambia el resultado y el que se elige mirando el histórico con más frecuencia. Alargar la ventana reduce el giro y retrasa la señal; acortarla la acerca a la reversión de corto plazo, que va en sentido contrario |
| Escalado por volatilidad | Dividir la posición por la volatilidad estimada del activo | adimensional | Sin él, el activo más nervioso del universo manda en el resultado y la cartera es en realidad una apuesta a su volatilidad. Divide la posición por la desviación típica, así que un activo con la mitad de volatilidad lleva el doble de peso |
| Coste por rebalanceo | El coste de girar la cartera cada mes (comisión, diferencial, impacto) | tanto por uno del nominal girado | Cada mes cambia la composición de los deciles y se paga por ello. Con 43 operaciones al año en un par de docenas de nombres, unos pocos puntos básicos por operación pueden llevarse la mitad de la prima |
:::

## Ejemplo

Cinco activos (numerados del 0 al 4, como en el código) y trece meses de retornos. El mes 13
es el mes en curso, el que se salta. Las rentabilidades acumuladas de los doce meses
anteriores son:

```
activo 0:  0,2311     activo 3:  0,2803
activo 1:  0,1604     activo 4:  0,1265
activo 2: -0,0105
```

Ordenando de mejor a peor: 3, 0, 1, 4, 2. Con cinco activos, la cartera de juguete compra el
3 y vende el 2.

Ahora incluye el mes en curso y mira lo que pasa. El activo 1 se deja un 6 % ese mes, así que
su acumulado cae del 16,04 % al 9,08 % y baja del tercer puesto al cuarto: el activo 4 lo
adelanta. Y el activo 2, que era el peor con un −1,05 %, pasa a +2,91 %. En la versión
«12-0», sin saltarse nada, el activo 2 sigue siendo el último de la lista, pero su momentum
ya es positivo: la señal te está contando algo muy distinto sobre él, y encima te deja corto
en un activo que acaba de girar. Saltarse el último mes no es un capricho: es quitar de la
señal un componente que va en sentido contrario.

Ese componente contrario se puede medir. En una serie con tendencia persistente y un rebote de
corto plazo, la correlación entre el retorno de los doce meses y el mes siguiente es
**+0,125**, mientras que la del último mes con el siguiente es **−0,219**. El pasado reciente
apunta hacia atrás, el pasado lejano apunta hacia delante.

## Código

```python verificable
import numpy as np

# 5 activos, 13 retornos mensuales en tanto por uno; el ultimo es el mes en curso
r = np.array([
    [0.02, 0.01, 0.03, 0.02, 0.01, 0.02, 0.01, 0.02, 0.03, 0.01, 0.02, 0.01,  0.01],
    [0.01, 0.02, 0.00, 0.01, 0.02, 0.01, 0.02, 0.00, 0.01, 0.02, 0.01, 0.02, -0.06],
    [-0.01, 0.00, 0.01, -0.02, 0.00, 0.01, -0.01, 0.00, 0.01, -0.01, 0.00, 0.01, 0.04],
    [0.03, 0.02, 0.01, 0.02, 0.03, 0.01, 0.02, 0.03, 0.01, 0.02, 0.03, 0.02, 0.00],
    [0.00, 0.01, 0.02, 0.01, 0.00, 0.01, 0.02, 0.01, 0.00, 0.01, 0.02, 0.01,  0.00],
])

mom_12_1 = np.prod(1 + r[:, :12], axis=1) - 1     # 12 meses, saltando el ultimo
mom_total = np.prod(1 + r, axis=1) - 1            # incluyendo el mes en curso

print("momentum 12-1   ", np.round(mom_12_1, 4))
print("con el ultimo   ", np.round(mom_total, 4))
print("orden 12-1  (mejor a peor)", np.argsort(-mom_12_1))
print("orden total (mejor a peor)", np.argsort(-mom_total))
# -> momentum 12-1    [ 0.2311  0.1604 -0.0105  0.2803  0.1265]
# -> con el ultimo    [0.2434 0.0908 0.0291 0.2803 0.1265]
# -> orden 12-1  (mejor a peor) [3 0 1 4 2]
# -> orden total (mejor a peor) [3 0 4 1 2]
```

:::claves
- `np.prod(1 + r[:, :12], axis=1)` compone los doce meses **a lo largo de las columnas** (`axis=1`), una fila por activo. Con `axis=0` multiplicarías hacia abajo, mes a mes, y obtendrías un solo número por columna: el resultado seguiría siendo un array, así que el `print` no fallaría, pero el orden de los activos sería absurdo. Es el error de `axis` más frecuente con datos en matriz.
- El corte `r[:, :12]` **excluye la última columna**, que es el mes en curso. Es la diferencia entre momentum 12-1 y 12-0, y está escrita como un índice, no como una decisión: si el array creciera a 14 columnas, `:12` seguiría tomando los doce primeros, que es lo correcto, mientras que `r[:, :-1]` tomaría trece. Con datos que cambian de longitud, `:-1` es más seguro; con ventanas fijas, `:12` es más explícito.
- `1 + r` **no modifica `r`**: crea un array nuevo, y lo mismo hace `np.prod`. Eso no es una garantía general de NumPy, sino de esta operación concreta: `r[:, :12]` es una **vista**, no una copia, así que un `r[:, :12] *= 2` cambiaría los datos originales y el segundo cálculo (`mom_total`) ya no mediría lo que crees. Cuando dudes, `.copy()`.
- `np.argsort(-mom_12_1)` devuelve los **índices** ordenados de menor a mayor, y el signo menos invierte el orden para que el mejor quede primero. No es `np.sort`, que devolvería los valores sin decirte a qué activo pertenecen. Ese `-` solo funciona con números: con etiquetas de texto habría que usar `np.argsort(mom)[::-1]`.
- Compara las dos listas de índices: `[3 0 1 4 2]` y `[3 0 4 1 2]`. Cambian solo por el último mes, pero ese intercambio es de medio universo: el activo 4 pasa de cuarto a tercero y el activo 1 cae. Si la cartera comprara el primero y vendiera el último, la pata corta también cambia de nombre, y la señal te está contando algo distinto sobre el mismo activo.
- En el segundo bloque, `rebote[1:] -= 2.0 * u[:-1]` escribe **en el propio array** `rebote`, por eso se construyó con `u.copy()` una línea antes: sin esa copia, la resta modificaría `u` y el ruido original quedaría destruido para el resto del cálculo.
- `np.corrcoef(ult12, futuro)[0, 1]` devuelve una **matriz** de correlaciones, no un número: hay que indexar la posición `[0, 1]` para sacar el coeficiente entre las dos series. Además, `ult12` y `futuro` tienen que medir lo mismo: aquí cuadran porque los dos rangos se construyeron a mano (`r[12:]` y `range(12, n)`), y un desplazamiento de una posición cambiaría la correlación sin lanzar ningún error.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(1)
n = 600
x = np.zeros(n)                       # deriva persistente: lo que captura el momentum
for t in range(1, n):
    x[t] = 0.85 * x[t - 1] + rng.normal(0, 0.012)
u = rng.normal(0, 0.02, n)
rebote = u.copy()
rebote[1:] -= 2.0 * u[:-1]            # reversion de corto plazo, exagerada a proposito
r = x + rebote

futuro = r[12:]
ult12 = np.array([r[i - 12:i].sum() for i in range(12, n)])
ult1 = r[11:-1]

print("corr(12 meses, mes siguiente)   %+.3f" % np.corrcoef(ult12, futuro)[0, 1])
print("corr(ultimo mes, mes siguiente) %+.3f" % np.corrcoef(ult1, futuro)[0, 1])
# -> corr(12 meses, mes siguiente)   +0.125
# -> corr(ultimo mes, mes siguiente) -0.219
```

El segundo bloque explica el primer bloque: la parte persistente de la rentabilidad predice
el mes siguiente y el rebote transitorio predice lo contrario. La reversión de corto plazo
está exagerada a propósito para que se vea; en datos reales es más débil, pero sigue ahí.

## Errores típicos

- **No saltarse el último mes.** Es el error más común y el más caro: metes el rebote de corto
  plazo en la señal y tu cartera compra justo después de un pico. El ejemplo de arriba
  muestra cómo cambia la pata corta solo por incluir ese mes.
- **Rebalancear con datos del propio periodo de operación.** Decidir el día 31 con el cierre
  del día 31 y ejecutar al cierre del día 31 no es operar, es leer el periódico de mañana.
  Separa siempre el instante de decisión del de ejecución.
- **Ignorar el giro.** Momentum rota la cartera cada mes, y en los deciles extremos la
  composición cambia mucho. Si tu backtest no cobra [[slippage-y-comisiones|comisiones ni
  diferencial]] en cada rebalanceo, la mitad de la rentabilidad que ves es polvo.
- **Creer que la peor racha es una racha normal.** Momentum pierde mucho y muy rápido cuando
  el mercado rebota tras una caída profunda, porque la pata corta es la que más sube.
  Dimensiona la posición contando con esa cola, no con la volatilidad media.
- **Confundir momentum de sección cruzada con trend following.** Se parecen en el nombre y se
  comportan distinto: el de sección cruzada es relativo y sufre en los rebotes; el de serie
  temporal es absoluto y suele proteger en las caídas largas. Si los mezclas en un backtest
  sin separarlos, no sabrás qué estás midiendo.
- **Presumir de rentabilidad sin descontar la exposición al mercado.** Una versión solo-larga
  de momentum es, en buena parte, beta de mercado con otro nombre. Compara siempre contra la
  cartera larga-corta, que es la que aísla el efecto.

:::trampa
Un backtest de momentum con Sharpe alto suele tener una de estas tres cosas: mirada al
futuro en el rebalanceo, universo con [[sesgo-de-supervivencia|sesgo de supervivencia]]
(solo las acciones que hoy existen) o costes de transacción puestos a cero. Las tres inflan
el resultado y las tres se detectan mirando el código, no la curva.
:::

:::practica
enunciado: Tres activos. Doce meses anteriores: A +18 %, B +22 %, C +8 %. Mes en curso: A −7 %, B +1 %, C +6 %. Aplica la regla 12-1, di qué compras y qué vendes y cómo cambia el orden si incluyes ese mes.
pista: La señal 12-1 ignora el último mes; encadena los dos periodos multiplicando para ver el efecto.
solucion: Orden 12-1: B (22 %), A (18 %), C (8 %): compras B, vendes C. Metiendo el mes en curso, cada acumulado es el producto de los dos periodos: A 1,18 · 0,93 = 1,0974 (+9,74 %), B 1,22 · 1,01 = 1,2322 (+23,22 %), C 1,08 · 1,06 = 1,1448 (+14,48 %). El orden pasa a B, C, A: A cae al último puesto y C, la pata corta, adelanta a A, que es el rebote que descarta la señal 12-1.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la definición estándar de momentum salta el mes más reciente?
o: Porque los datos del último mes todavía no están disponibles cuando se opera
o: Porque el último mes contiene un rebote de corto plazo que va en dirección contraria a la tendencia
o: Porque doce meses es el máximo que permite la regulación de fondos
a: 2
e: Los datos del último mes sí están disponibles al decidir, y por eso el problema no es de información. Lo que ocurre es que en el muy corto plazo domina la reversión: los activos que acaban de subir tienden a devolver parte de esa subida en las semanas siguientes. Incluir ese mes mete ruido con el signo cambiado.
:::

:::quiz
p: Una estrategia de momentum gana un 15 % anual y de repente pierde un 25 % en dos meses. ¿Qué explicación es más plausible?
o: Que el modelo se ha roto para siempre y hay que abandonarlo
o: Que el mercado ha rebotado con fuerza desde una caída profunda y su pata corta es la que más ha subido
o: Que ha fallado el cálculo del z-score del diferencial
a: 2
e: Es el patrón clásico de las momentum crashes: la estrategia va corta en los activos más castigados y esos son los que rebotan con más violencia al final del pánico. El z-score del diferencial pertenece al mundo de [[pairs-trading|el trading de pares]], no a este.
:::

:::aviso
Momentum y [[reversion-a-la-media|reversión a la media]] no son opiniones enfrentadas sobre
el mismo horizonte: son efectos que aparecen en escalas distintas. La reversión manda en días
o semanas, y el momentum en meses. Una estrategia que mezcle los dos sin separar los
horizontes acabará con las dos señales cancelándose.
:::
