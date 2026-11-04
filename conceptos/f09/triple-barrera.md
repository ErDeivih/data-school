---
id: triple-barrera
titulo: Etiquetado por triple barrera
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [retornos-logaritmicos, volatilidad-realizada, tick-data-y-ohlcv, sesgo-de-mirar-al-futuro]
tags: [etiquetado, validacion, lopez-de-prado, volatilidad]
resumen: Tres barreras (beneficio, pérdida y tiempo) deciden cuándo se cierra una operación y cuál es su etiqueta, sin usar información del futuro.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 3"]
---

## En una frase

Para cada operación se fijan tres barreras (un objetivo de beneficio, un stop de pérdida y una
fecha límite) y la etiqueta es simplemente cuál de las tres toca el precio primero: `+1` si toca
el objetivo, `-1` si toca el stop y `0` si se agota el tiempo.

## La idea

El etiquetado de manual es: mira el retorno de los próximos `h` días y pon `+1` si es positivo y
`-1` si es negativo. Es fácil de calcular y por eso se usa tanto, pero describe una estrategia
que nadie ejecuta. Nadie aguanta veinte días mirando la pantalla pase lo que pase: en algún
momento recoge beneficios o corta la pérdida. Si tu etiqueta no modela esa decisión, el modelo
aprende a predecir algo distinto de lo que vas a hacer con su predicción.

Hay un segundo problema, más sutil y más caro: un umbral fijo en porcentaje significa cosas
distintas según el régimen. Un movimiento del 3 % en un mes tranquilo es un acontecimiento; en
una semana de pánico es una mañana cualquiera. Con umbrales fijos, el modelo aprende a decir
«clase 0» en los periodos calmados y «clase extrema» en los violentos: no está aprendiendo a
predecir dirección, está aprendiendo a detectar volatilidad. Esa información ya la tienes sin
modelo. Por eso las barreras se ponen en unidades de volatilidad: `±1` volatilidad típica
significa lo mismo en 2017 que en marzo de 2020.

La tercera diferencia es la que casi todo el mundo pasa por alto: en el etiquetado a horizonte
fijo todas las observaciones se resuelven a la vez, `h` barras después de empezar. Aquí no. Una
operación puede cerrarse a las dos barras y otra agotar las veinte. Ese instante final, que
llamamos `t1`, permite después purgar el
entrenamiento, ponderar por unicidad y saber cuándo tu modelo podía saber algo. Sin ese intervalo,
dos observaciones que se solapan en el tiempo parecen independientes cuando en realidad están
mirando el mismo tramo de mercado. Un etiquetado
sin `t1` es un etiquetado del que no puedes defender su validación.

Y queda la propiedad que da nombre al método: la etiqueta depende del **camino**, no del destino.
Dos operaciones que acaban el día 20 con el mismo precio pueden tener etiquetas opuestas, porque
una pasó primero por el stop y la otra no. Eso no es un defecto: describe lo que le pasa a
tu cuenta. Si el precio te saca por el stop, el beneficio posterior ya no es tuyo.

:::nota
La triple barrera no es una estrategia, es una forma de etiquetar. No decide cuándo entrar: eso
viene de tus señales. Lo que decide es cuándo termina la observación y qué clase tiene.
:::

## Definición formal

Fijado un evento en la barra `t0`, se definen tres niveles a partir del precio de referencia
`P_t0` y de la volatilidad estimada en ese instante:

:::formula
arriba = P_t0 · (1 + pt · σ̂_t0)      abajo = P_t0 · (1 − sl · σ̂_t0)      vertical = t0 + h
:::

- `P_t0` — precio de referencia del evento (normalmente el cierre de la barra `t0`).
- `σ̂_t0` — volatilidad por barra en `t0`, estimada **solo con datos hasta `t0`**; lo habitual es
  la desviación típica exponencial de los retornos logarítmicos con una ventana tipo `span = 100`.
- `pt` — múltiplo de beneficio: cuántas volatilidades típicas deja correr el precio antes de
  recoger. `pt = 1` es el caso habitual.
- `sl` — múltiplo de pérdida: cuántas volatilidades típicas se aguantan antes de cortar.
- `h` — número de barras de la barrera vertical; es el tiempo máximo que la operación sigue viva.

La etiqueta y la fecha de resolución son:

:::formula
y = +1 si se toca arriba primero      y = −1 si se toca abajo primero      y = 0 si vence h
:::

- `y` — la etiqueta, una de tres clases: `+1`, `−1` o `0`.
- `t1` — la primera barra en la que se toca cualquiera de las tres barreras. Es la fecha en la
  que la etiqueta queda determinada y la que se usa para purgar, ponderar y medir.
- `[t0, t1]` — el intervalo que ocupa la observación. Dos observaciones con intervalos que se
  solapan no son independientes, y eso abre [[sample-weights|el problema de los pesos]] y
  [[purged-kfold|la purga]].

Dos convenciones que hay que decidir y documentar:

1. **Dentro de la barra.** Si en la misma barra el máximo toca arriba y el mínimo toca abajo, con
   datos de barras no puedes saber el orden. La opción prudente es asignar `−1` (asumir que el
   stop se ejecutó primero) y decirlo en el informe. La optimista infla todos los resultados.
2. **En la barrera vertical.** Puedes asignar `0` a la clase intermedia o usar el signo del
   retorno acumulado hasta `t1`. Elegir una u otra cambia la proporción de clases, así que
   decídelo antes de mirar resultados.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P_t0` | Precio de referencia del evento, normalmente el cierre de la barra `t0` | precio | Mueve las tres barreras a la vez: los niveles son proporciones suyas, así que en un activo de 500 el mismo `pt` son más euros por acción |
| `σ̂_t0` | Volatilidad por barra estimada **solo con datos hasta `t0`** | tanto por uno por barra | Ensancha las dos barreras y con ellas la clase `0`: con barreras de una σ diaria y `h = 20`, el precio casi siempre toca una de las dos antes de que venza el plazo |
| `pt` | Múltiplo de beneficio: cuántas volatilidades deja correr el precio | volatilidades | Alarga la barrera de arriba: el objetivo se toca menos veces, pero cada acierto es mayor. Subirlo también dispara la clase `−1`, que sigue a una sigma |
| `sl` | Múltiplo de pérdida antes de cortar | volatilidades | Acerca el stop: más etiquetas `−1` y menos `+1`. Con `pt = 2` y `sl = 1` el problema se desbalancea por aritmética, no por un fallo del método |
| `h` | Barrera vertical: barras que la operación sigue viva | barras | Cuanto más largo, más operaciones se resuelven por precio y menos por tiempo; pero si `σ̂` es diaria y `h` de veinte días, un ancho de una sigma es el movimiento de un día, no el de veinte |
| `t1` | Primera barra en la que se toca cualquiera de las tres barreras | índice de barra | Define el intervalo `[t0, t1]` de la observación. Sin `t1` no hay purga ni pesos por unicidad: el modelo se valida sobre datos que se solapan |
| `y` | Etiqueta: `+1` si gana el objetivo, `−1` si gana el stop, `0` si vence el tiempo | clase | La proporción de cada clase la fijan `pt`, `sl` y `h`, así que se decide antes de mirar resultados. Si `0` se lleva el 80 %, casi siempre es `h` corta respecto al ancho de las barreras |
:::

:::figura
fichero: triple-barrera-camino-y-reparto-de-clases
pie: A la izquierda, la propiedad que da nombre al método: dos caminos que acaban en 104 (+4 %) reciben etiquetas opuestas porque el segundo pasó antes por el stop, y esa operación ya estaba cerrada cuando llegó el beneficio. A la derecha, el reparto de clases de 1 300 eventos simulados con `pt = sl = 1`: con barreras de una sigma diaria, la clase `0` no aparece ni una vez y el etiquetado se reduce a un signo; escalando las barreras por `√h` vuelve el 26 % de observaciones que agotan el plazo, que son información y no ruido.
fuente: figuras/triple-barrera-1.py
:::

## Ejemplo

Doce cierres y una volatilidad estimada de `σ̂ = 0,02` (un 2 % por barra), con `pt = sl = 1` y
`h = 6`:

```
100,0  100,5  101,2  102,4  101,8  99,9  98,6  99,4  100,7  101,5  102,9  103,4
```

- Evento en la barra 0: `P_t0 = 100,0` → barreras en 102,00 y 98,00. Las barras 1 y 2 cierran en
  100,5 y 101,2; la barra 3 cierra en 102,4, que supera 102,00 → etiqueta `+1` con `t1 = 3`.
- Evento en la barra 4: `P_t0 = 101,8` → barreras en 103,84 y 99,76. La barra 5 cierra en 99,9
  (aguanta) y la barra 6 en 98,6, por debajo de 99,76 → etiqueta `−1` con `t1 = 6`.
- Repitiendo el cálculo en todas las barras y contando las clases: 5 etiquetas `+1`, 3 etiquetas
  `−1` y 3 veces se agota el tiempo. La barrera vertical se lleva un tercio de la
  muestra, y esas observaciones son información, no ruido que se pueda tirar.

La dependencia del camino se ve con dos series que acaban en el mismo sitio, `100 → 104` en cinco
barras, con barreras en 102 y 98:

- Camino A: 100,0 → 101,0 → 102,5 → 103,2 → 104,0. Toca 102,5 en la barra 2 → `+1`.
- Camino B: 100,0 → 99,0 → 97,5 → 101,0 → 104,0. Toca 97,5 en la barra 2 → `−1`.

Mismo retorno final, `+4 %` en los dos casos, etiquetas opuestas. Cualquier etiqueta que mire
solo el precio final está tirando la información que decide si la operación te dejó seguir
operando o te sacó de la mesa.

## Código

```python verificable
import numpy as np

precios = np.array([100.0, 100.5, 101.2, 102.4, 101.8,
                    99.9, 98.6, 99.4, 100.7, 101.5, 102.9, 103.4])
sigma = 0.02                  # volatilidad por barra (2 %), estimada solo con el pasado
pt, sl, h = 1.0, 1.0, 6       # multiplos de beneficio, de perdida y barrera vertical

def etiqueta_triple_barrera(precios, t0, sigma, pt, sl, h):
    """Devuelve la etiqueta y la barra en que queda determinada, t1."""
    p0 = precios[t0]
    arriba, abajo = p0 * (1 + pt * sigma), p0 * (1 - sl * sigma)
    for t in range(t0 + 1, min(t0 + h + 1, precios.size)):
        if precios[t] >= arriba:
            return 1, t
        if precios[t] <= abajo:
            return -1, t
    return 0, min(t0 + h, precios.size - 1)

# Dos eventos del mismo tramo: el de la barra 0 acaba en el objetivo y el de la 4 en el stop.
for t0 in (0, 4):
    etq, t1 = etiqueta_triple_barrera(precios, t0, sigma, pt, sl, h)
    print(f"t0={t0}  p0={precios[t0]:.1f}  barreras [{precios[t0]*(1-sl*sigma):.2f}, "
          f"{precios[t0]*(1+pt*sigma):.2f}]  etiqueta {etq:+d}  t1={t1}")

etiquetas = [etiqueta_triple_barrera(precios, t0, sigma, pt, sl, h)[0]
             for t0 in range(precios.size - 1)]
print("reparto de etiquetas:",
      {k: etiquetas.count(k) for k in (-1, 0, 1)})   # -> {-1: 3, 0: 3, 1: 5}
```

:::claves
- `arriba, abajo = p0 * (1 + pt * sigma), p0 * (1 - sl * sigma)` fija niveles **absolutos** de precio a partir de `p0`. Si en vez de eso guardas los múltiplos y comparas retornos, el bucle se llena de divisiones; aquí se calcula una vez y se compara precio contra precio.
- `min(t0 + h + 1, precios.size)` es el tope de la barrera vertical **y** del array: sin el `min`, el último evento de la serie lanzaría un `IndexError`. La barrera vertical es `t0 + h`, y el `+1` es porque el rango de Python no incluye el final.
- `precios[t] >= arriba` y `precios[t] <= abajo` comparan cierres, no máximos y mínimos de la barra. Con una barra que perfora el stop y recupera, la etiqueta sale más optimista que lo que habrías vivido; si tienes OHLC, la decisión de qué mirar cambia el resultado.
- El `for` recorre las barras en orden y devuelve en cuanto toca una: la etiqueta la decide la **primera** barrera, y solo el orden de las comparaciones importa si en la misma barra se tocan las dos. Cambiar el `if` de arriba por el de abajo invierte esa prioridad en los casos ambiguos.
- `range(precios.size - 1)` deja fuera el último precio: un evento abierto en la última barra no tiene ninguna barra futura que mirar y su `t1` sería inventado. Ese evento no se etiqueta, se descarta.
- El segundo bloque reutiliza `primera_barrera` para mostrar la dependencia del camino: las dos series acaban en `104.0`, así que el retorno final es idéntico y la etiqueta sale `+1` en una y `−1` en la otra. Cualquier etiqueta basada en `precios[-1] - precios[0]` habría dado el mismo valor a las dos.
:::

```python verificable
import numpy as np

# Dos caminos con el mismo destino y etiquetas opuestas: la etiqueta depende del recorrido.
camino_a = np.array([100.0, 101.0, 102.5, 103.2, 104.0])
camino_b = np.array([100.0, 99.0, 97.5, 101.0, 104.0])
arriba, abajo = 100 * 1.02, 100 * 0.98

def primera_barrera(camino, arriba, abajo):
    for i in range(1, camino.size):
        if camino[i] >= arriba:
            return i, 1
        if camino[i] <= abajo:
            return i, -1
    return camino.size - 1, 0

# Los dos caminos acaban en 104 (+4 %), pero la primera barrera es distinta en cada uno.
for nombre, c in (("A", camino_a), ("B", camino_b)):
    i, etq = primera_barrera(c, arriba, abajo)
    print(f"camino {nombre}: retorno final {c[-1]/c[0]-1:+.1%}  "
          f"primera barrera en t={i}  etiqueta {etq:+d}")
```

## Errores típicos

- **Etiquetar a horizonte fijo y llamarlo triple barrera.** Un `sign(retorno a 20 barras)` no
  tiene barreras ni `t1`, así que no describe ninguna regla de salida y no permite purgar nada.
  Si de verdad usas horizonte fijo, dilo: es otra cosa y tiene otras limitaciones.
- **Calcular `σ̂` con toda la muestra.** Si la volatilidad que fija las barreras se estima con
  datos posteriores a `t0`, las barreras ya saben que viene una crisis y la etiqueta se vuelve
  trivialmente predecible. Es [[sesgo-de-mirar-al-futuro|mirar al futuro]] en el paso más
  temprano del proceso, y contamina todo lo que venga después.
- **Usar solo cierres cuando tienes máximos y mínimos, o al revés.** Con cierres, una barra que
  perfora el stop y recupera no cuenta como stop y tu etiqueta es más optimista que la realidad.
  Con máximos y mínimos hay que decidir el orden intra-barra, y la decisión prudente es asumir lo
  malo.
- **Mezclar frecuencias entre `σ̂` y `h`.** Si `σ̂` es la volatilidad de una barra diaria y la
  barrera vertical son 20 días, un ancho de `1 · σ̂` es el movimiento típico de un día, no el de
  veinte. O escalas el ancho con `√h`, o aceptas conscientemente que la barrera de beneficio es
  muy estrecha respecto al plazo.
- **Fijar `pt` y `sl` iguales «por simetría» y no mirarlos más.** El cociente entre objetivo y
  stop, junto con la probabilidad de acierto, determina el valor esperado. Con `pt = 2` y
  `sl = 1` la clase `−1` se dispara y el problema se desbalancea; es
  la consecuencia aritmética de tu elección, no un fallo del método.
- **Guardar la etiqueta y tirar `t1`.** Sin el intervalo `[t0, t1]` no puedes purgar el
  entrenamiento ni ponderar por unicidad: acabarás con un modelo que se valida sobre datos que
  solapan y con métricas que no significan nada.

:::practica
enunciado: Cinco cierres: 50,0; 50,4; 49,3; 51,2; 52,0. Con una volatilidad por barra de 0,018, pt = sl = 1 y h = 4, etiqueta los eventos abiertos en las barras 0 y 1 y di qué barras ocupa cada observación.
pista: Las barreras son P_t0 · (1 ± σ̂) y gana la primera que toque un cierre; la observación va de t0 a t1.
solucion: Evento de la barra 0: P = 50,0, barreras 50,90 y 49,10. Las barras 1 y 2 aguantan y la barra 3 cierra en 51,2, por encima de 50,90: etiqueta +1 con t1 = 3. Evento de la barra 1: P = 50,4, barreras 51,31 y 49,49, y la barra 2 cierra en 49,3: etiqueta −1 con t1 = 2. Las dos observaciones se solapan en las barras 1 y 2 y duran distinto, cuatro barras frente a dos.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué las barreras se fijan en múltiplos de la volatilidad y no en porcentajes fijos?
o: Porque así el número de operaciones ganadoras y perdedoras queda equilibrado por construcción
o: Porque un mismo porcentaje significa un movimiento enorme en un régimen tranquilo y uno normal en uno violento, y la etiqueta acabaría midiendo volatilidad en vez de dirección
o: Porque la volatilidad es más fácil de estimar que el precio
a: 2
e: Con umbrales fijos, el modelo aprende a distinguir periodos calmados de periodos agitados, información que ya tenías sin modelo. Al escalar por volatilidad, un mismo múltiplo representa el mismo esfuerzo relativo en cualquier régimen. No equilibra las clases: eso depende de pt, de sl y de la deriva del activo.
:::

:::quiz
p: Dos eventos tienen el mismo retorno final del +4 % en cinco barras, pero uno tocó antes el stop. ¿Qué etiquetas reciben?
o: Las dos `+1`, porque el resultado final es el mismo
o: El primero `+1` y el segundo `−1`, porque la etiqueta la decide la primera barrera tocada
o: Las dos `0`, porque ninguna llegó a la barrera vertical
a: 2
e: La triple barrera etiqueta por el camino, no por el destino: si el precio pasó por el stop, la operación estaba cerrada cuando llegó el beneficio. Ese sesgo hacia lo que de verdad habrías vivido es justamente lo que aporta el método.
:::

:::trampa
Si al revisar tus etiquetas ves que la clase `0` es el 80 % de la muestra, casi siempre es la
barrera vertical mal calibrada: `h` demasiado corta respecto al ancho de las barreras. Alarga el
plazo o estrecha las barreras, pero decide antes de mirar el rendimiento del modelo.
:::
