---
id: sortino-y-calmar
titulo: Sortino y Calmar
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [metricas-de-riesgo, ratio-de-sharpe, maximo-drawdown]
tags: [riesgo, metricas, drawdown, cartera]
resumen: Dos correcciones al ratio de Sharpe: penalizar solo la volatilidad que duele y medir la rentabilidad contra la peor caída que has sufrido.
fuentes: ["Sortino y Price (1994), 'Performance Measurement in a Downside Risk Framework'", "Young (1991), 'Calmar Ratio: A Smoother Tool'", "Bacon (2008), 'Practical Portfolio Performance Measurement and Attribution'"]
---

## En una frase

El ratio de Sortino divide el exceso de rentabilidad entre la desviación de los retornos que
quedan por debajo del objetivo, y el de Calmar divide la rentabilidad anualizada entre la caída
máxima: los dos nacen de la misma queja contra el Sharpe, que castiga igual el temblor que te
enriquece y el que te arruina.

## La idea

Imagina que evalúas a dos conductores por la variación de su velocidad. Uno frena y acelera sin
parar en un atasco; el otro mantiene una velocidad alta y estable, con un par de frenazos fuertes
en curvas. Si penalizas toda variación por igual, el segundo sale peor valorado, y sin embargo es
el que llegó antes y el que conducía con margen. El Sharpe hace exactamente eso con las
estrategias: mete en la misma bolsa los meses de +8 % y los meses de −8 %, cuando lo que te quita
el sueño son los segundos.

El **Sortino** corrige eso. En lugar de dividir entre la volatilidad de todos los retornos, divide
entre la **desviación bajista**: solo cuenta los retornos que quedan por debajo de un objetivo
`T` que tú eliges. Y no es una corrección cosmética: en una estrategia con retornos asimétricos
—pocas pérdidas grandes y muchas ganancias pequeñas, o al contrario— el Sharpe y el Sortino
pueden contar historias opuestas. Cuando el Sortino es mucho mayor que el Sharpe, la estrategia
tiene volatilidad sobre todo hacia arriba. Cuando es menor, el problema está en las caídas.

El **Calmar** ataca otra cosa. Al inversor que aguanta una estrategia no le preocupa tanto la
desviación típica como el peor tramo que va a tener que vivir: si la cuenta cae un 40 % y tarda
dos años en recuperarse, da igual que la volatilidad mensual sea del 3 %. El Calmar pone el
rendimiento anualizado en el numerador y la caída máxima en el denominador, y responde a la
pregunta «¿cuánto gano por cada punto de caída que he soportado?». Su antecesor, el ratio MAR,
usaba la misma idea con el objetivo puesto en la peor caída.

Los dos tienen el mismo defecto de fondo y conviene decirlo antes de usarlos: **dependen mucho
más de la muestra que el Sharpe**. El Sortino se apoya solo en los periodos malos, así que si en
tu histórico hay pocos, la estimación es ruidosa. El Calmar se apoya en **una sola** caída, la
mayor, y esa caída puede ser un accidente irrepetible o el aviso de lo que viene. Con dos años de
datos, el Calmar es una anécdota; con veinte, empieza a ser una medida.

## Definición formal

Sea `r_1 … r_n` la serie de retornos y `T` el objetivo (MAR, *minimum acceptable return*): la
rentabilidad mínima que aceptas, en la misma frecuencia que los retornos.

:::formula
Sortino = (r̄ − T) / DD_T          DD_T = √( Σ min(r_i − T, 0)² / n )
:::

:::formula
Calmar = retorno anualizado / MDD
:::

- `r_i` — retorno del periodo `i`, en tanto por uno.
- `r̄` — media de los retornos del periodo.
- `T` — objetivo. Con `T = 0` se penalizan solo los periodos en pérdidas; con `T` igual al tipo
  libre de riesgo, se exige batir a ese tipo.
- `DD_T` — desviación bajista: raíz de la media de los cuadrados de las desviaciones negativas
  respecto a `T`. **Los periodos buenos entran en la suma con un cero**, es decir, cuentan en el
  denominador `n`. Es la convención coherente con la definición de desviación típica, y la que
  usa el artículo original.
- `n` — número de observaciones. Con la convención alternativa, el denominador es solo el número
  de periodos por debajo de `T`, `k`, y el resultado sale sistemáticamente **más bajo**, porque
  `k < n` y por tanto la desviación bajista es mayor. Las dos convenciones circulan; usa una,
  dilo y no compares números calculados con la otra.
- `MDD` — caída máxima: la mayor caída porcentual desde un pico de la curva de capital hasta el
  mínimo anterior a recuperarlo ([[maximo-drawdown]]).
- `retorno anualizado` — la rentabilidad del periodo llevada a un año:
  `(C_final / C_inicial)^(1 / años) − 1`. Si el periodo es más corto que un año, anualizar
  multiplica el ruido de la muestra.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `r_i` | El retorno del periodo `i` | tanto por uno | No es una palanca: es lo que mides. Solo los que quedan por debajo de `T` entran en la desviación bajista, y los buenos entran con un cero |
| `r̄` | La media de los retornos del periodo | tanto por uno | Es el numerador del Sortino: cada periodo bueno lo sube y el ratio con él. Un único mes muy bueno puede sostener todo el número |
| `T` | El objetivo (MAR): la rentabilidad mínima que aceptas | tanto por uno, **misma frecuencia** que `r_i` | Al subirlo, más periodos quedan por debajo del objetivo, la desviación bajista crece y el Sortino baja. Restar un 3 % anual a retornos mensuales es un error de doce veces |
| `DD_T` | La desviación bajista: la raíz de la media de los cuadrados de las desviaciones negativas respecto a `T` | tanto por uno | Es el denominador, y depende de entre cuánto dividas: con `n` sale 0,0220 y el Sortino 0,79; con `k` sale 0,0381 y el ratio 0,45 |
| `n` | Número total de observaciones | periodos | En la convención original el denominador es `√(Σ/n)`, así que añadir periodos buenos lo baja y el Sortino **sube**: más meses tranquilos mejoran el ratio sin que haya pasado nada |
| `k` | Número de periodos por debajo de `T` | periodos | Es la convención alternativa. Como `k < n`, la desviación bajista es mayor y el ratio sale más bajo: con los mismos datos, 0,45 en vez de 0,79. Elige una convención, dilo y no compares números calculados con la otra |
| `MDD` | La caída máxima de la curva de capital | tanto por uno | Es el denominador del Calmar y se apoya en **una sola** caída. Cuanto más larga sea la ventana, más probable es encontrar una caída peor y más bajo sale el Calmar |
| Retorno anualizado | La rentabilidad del periodo llevada a un año: `(C_final / C_inicial)^(1/años) − 1` | tanto por uno al año | Es el numerador del Calmar. Si el periodo es más corto que un año, anualizar multiplica el ruido: con seis meses, el número depende mucho de dónde cortes |
| `√12` (o `√252`) | El factor de anualización del Sortino | adimensional | Igual que en el Sharpe, escala con la raíz del número de periodos por año y supone independencia entre ellos. Con volatilidad agrupada, la cifra anualizada es una convención, no un dato |
:::

**Anualización del Sortino.** Igual que el Sharpe, escala con la raíz del número de periodos por
año: `Sortino_anual ≈ Sortino_mensual · √12` con retornos mensuales, y `· √252` con diarios. Ese
factor supone independencia entre periodos, y en finanzas ese supuesto es falso: la volatilidad
se agrupa, y por eso la cifra anualizada de una serie corta es más una convención que un dato.

La diferencia entre los dos denominadores, en una frase: el Sharpe mide cuánto te mueves, el
Sortino cuánto te mueves **a la baja**, y el Calmar cuánto llegaste a caer de verdad.

:::figura
fichero: sortino-convencion-y-ventana
pie: A la izquierda, la misma serie de seis meses con tres ratios: Sharpe 0,51, Sortino dividiendo la desviación bajista entre los seis meses (0,79) y el mismo Sortino dividiendo entre los dos meses malos (0,45). Lo único que cambia es entre cuánto se divide, y el orden respecto al Sharpe se invierte. A la derecha, la misma estrategia con dos ventanas: la caída del 19 % vive en los primeros doce meses, así que el Calmar pasa de 0,61 a 3,39 según desde dónde empieces a medir.
fuente: figuras/sortino-y-calmar-1.py
:::

## Ejemplo

Seis retornos mensuales: `0,03`, `−0,02`, `0,04`, `−0,05`, `0,01`, `0,02`. La media es `0,005`
(0,5 % mensual) y la volatilidad mensual es `0,0339`.

Con `T = 0`:

- Desviación bajista sumando sobre las seis observaciones (`n = 6`): las desviaciones negativas
  son `−0,02` y `−0,05`; sus cuadrados suman `0,0029`; divididos entre 6 y con la raíz, queda
  `0,0220`. Sortino mensual: `0,005 / 0,0220 = 0,227`; anualizado, `0,227 · √12 = 0,79`.
- Desviación bajista dividiendo solo entre las dos observaciones negativas (`k = 2`): raíz de
  `0,0029 / 2 = 0,0381`. Sortino mensual: `0,131`; anualizado, `0,45`.
- El Sharpe anual de la misma serie es `0,51`. Fíjate en el orden: con la convención coherente
  (la de `n`), el Sortino `0,79` es bastante mayor que el Sharpe `0,51`, porque la volatilidad de
  esta serie está repartida de forma parecida entre subidas y bajadas pero la media es positiva.
  Con la otra convención sale `0,45`, **por debajo** del Sharpe, y las conclusiones que sacarías
  serían las contrarias.

Para el Calmar, la curva de capital de esa serie va de 100 a 102,74. El pico es 104,98, el mínimo
posterior 99,73, así que la caída máxima es del `5,00 %`. La rentabilidad anualizada es
`1,0274² − 1 = 5,56 %`. Calmar: `5,56 / 5,00 = 1,11`.

Ese 1,11 significa «gano algo más de un punto por cada punto de caída máxima». Suena razonable y
no significa nada, porque el denominador se apoya en una única caída de seis meses. La prueba es
inmediata: sobre una serie de dos años que empieza con una caída del 19,04 % y sigue con doce
meses tranquilos, el Calmar sale `0,61` con la serie completa y `3,39` con los últimos doce meses
—ahí la caída máxima del tramo es del 1,50 %—, como muestra el segundo bloque de código. Un ratio
que se mueve con la ventana que eliges es una descripción, no una propiedad de la estrategia.

## Código

```python verificable
import numpy as np

r = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])
objetivo = 0.0                                   # T: rentabilidad minima aceptable, mensual
exceso = r - objetivo

vol_total = exceso.std(ddof=1)
bajista_n = np.sqrt((np.minimum(exceso, 0) ** 2).sum() / exceso.size)      # divide entre n
bajista_k = np.sqrt((np.minimum(exceso, 0) ** 2).sum() / (exceso < 0).sum())  # entre negativos
raiz = np.sqrt(12)

print(f"volatilidad         {vol_total:.4f}")                       # -> 0.0339
print(f"bajista (n = {exceso.size})    {bajista_n:.4f}")            # -> 0.0220
print(f"bajista (k = {(exceso < 0).sum()})    {bajista_k:.4f}")      # -> 0.0381
print(f"Sharpe anual        {exceso.mean() / vol_total * raiz:.2f}")        # -> 0.51
print(f"Sortino anual / n   {exceso.mean() / bajista_n * raiz:.2f}")         # -> 0.79
print(f"Sortino anual / k   {exceso.mean() / bajista_k * raiz:.2f}")         # -> 0.45
```

:::claves
- `np.minimum(exceso, 0)` es la pieza que convierte la volatilidad total en bajista: devuelve un array del mismo tamaño con todo lo positivo cambiado por cero. Tiene que ser `np.minimum`, porque el `min()` de Python compara el array entero con 0 y falla con un error de ambigüedad.
- `(exceso < 0).sum()` cuenta los meses malos porque un array de booleanos se suma como unos y ceros. `exceso.size` (los 6) y `(exceso < 0).sum()` (los 2) son exactamente la `n` y la `k` de las dos convenciones: cambiar una por otra es lo único que separa 0,79 de 0,45.
- El `** 2` antes de `.sum()` no es decorativo: las desviaciones que sobreviven a `np.minimum` son todas negativas, así que sin elevar al cuadrado la suma sale negativa y `np.sqrt` devuelve `nan` con un aviso en lugar de un error. Ese `nan` se propaga a todas las métricas que calcules después.
- `exceso.size` y `len(exceso)` coinciden aquí, pero con un array de dos dimensiones `len()` devuelve solo la primera: `.size` es el total de elementos, que es lo que quieres en el denominador.
- `raiz = np.sqrt(12)` se guarda en una variable y se multiplica: el factor de anualización **multiplica**, no eleva. Si en vez de `* raiz` escribieras `** 2`, el Sortino anual pasaría de 0,79 a 0,006 sin que nada avise.
- Si la muestra no tiene ningún mes negativo, `(exceso < 0).sum()` vale 0 y la división devuelve `inf` con un aviso (el tercer bloque de la página lo enseña). Un `inf` en una tabla de ratios no es un Sortino enorme: es un denominador que no existe, y lo honesto es decir que el ratio no está definido.
:::

```python verificable
import numpy as np

# La misma estrategia con dos ventanas: el Calmar cambia porque la caida cambia.
r = np.array([0.05, 0.04, -0.12, -0.08, 0.06, 0.05, 0.03, 0.04, 0.02, 0.03, 0.04, 0.03,
              0.005, 0.01, -0.015, 0.005, 0.01, 0.005, 0.005, 0.00, 0.01, 0.005, 0.005, 0.005])


def calmar(x):
    capital = np.cumprod(1 + x)       # arranca en 1: es el factor de crecimiento
    picos = np.maximum.accumulate(capital)
    mdd = float(((picos - capital) / picos).max())
    anual = float(capital[-1] ** (12 / x.size) - 1)
    return anual, mdd, anual / mdd


for etiqueta, tramo in (("24 meses", r), ("ultimos 12", r[-12:])):
    anual, mdd, ratio = calmar(tramo)
    print(f"{etiqueta:<12} anual {anual:+.2%}  caida {mdd:.2%}  Calmar {ratio:.2f}")
# -> 24 meses     anual +11.65%  caida 19.04%  Calmar 0.61
# -> ultimos 12   anual +5.09%  caida 1.50%  Calmar 3.39
```

```python verificable
import numpy as np

# Sortino sin retornos negativos en la muestra: el denominador es cero.
r = np.array([0.01, 0.02, 0.03, 0.01])
bajista = np.sqrt((np.minimum(r, 0) ** 2).sum() / r.size)

print(f"bajista {bajista:.4f}")     # -> 0.0000
print(f"Sortino {np.inf if bajista == 0 else r.mean() / bajista:.2f}")   # -> inf
print("sin meses malos el ratio no es enorme: es indefinido")
```

## Errores típicos

- **Dividir la desviación bajista entre el número de periodos malos.** Es la variante que más se
  ve en hojas de cálculo y en herramientas de producto, y cambia el número de forma notable: con
  `k` el denominador es mayor y el ratio baja. En el ejemplo, pasa de `0,79` a `0,45`, un 43 %
  menos. Elige la convención de la definición original (dividir entre `n`) y di cuál usas cuando
  compares con un número ajeno.
- **Mezclar el objetivo `T` con una frecuencia distinta.** Si tus retornos son mensuales, `T`
  tiene que ser mensual. Restar un 3 % anual a retornos mensuales hunde la media y dispara el
  Sortino en cualquier dirección: un 3 % anual es un 0,25 % mensual, doce veces menos.
- **Presumir de Sortino con pocos meses malos.** Si en tu muestra solo hay tres meses negativos,
  la desviación bajista se apoya en tres números. Un Sortino de 3 con esa base es ruido, no
  evidencia: mira el Sharpe, el número de observaciones y el intervalo de confianza.
- **Comparar Calmar calculado con ventanas distintas.** El Calmar depende de la peor caída del
  tramo que elijas, así que la misma estrategia da `0,61` con 24 meses y `3,39` con los últimos
  12. La definición original usa los últimos 36 meses; si usas otra, escríbela.
- **Creer que el Calmar mide el riesgo de ruina.** Un Calmar alto con apalancamiento alto es una
  estrategia que aún no ha vivido su primera racha larga. La caída máxima histórica no es una
  cota: es la mayor que ha ocurrido. Mira el apalancamiento y el
  [[tamano-de-posicion|tamaño de posición]] junto al ratio, y el [[riesgo-de-ruina|riesgo de
  ruina]] si vas a operar con dinero prestado.
- **Elegir entre Sharpe, Sortino y Calmar según cuál sale mejor.** Son tres formas de mirar la
  misma serie; quedarte con la que favorece tu estrategia es una prueba múltiple encubierta
  ([[data-snooping-y-multiple-testing]]). Publica los tres, o elige uno **antes** de ver los
  resultados y explica por qué.

:::practica
enunciado: Seis retornos mensuales: 0,03, −0,02, 0,02, −0,04, 0,02, 0,00. Con T = 0, calcula el Sortino mensual dividiendo la desviación bajista entre n = 6 y entre k = 2, y compáralo con el Sharpe mensual.
pista: Los cuadrados de las desviaciones negativas suman 0,0020; lo único que cambia es entre cuánto divides.
solucion: Media: 0,0017. Con n: √(0,0020 / 6) = 0,0183, Sortino 0,0017 / 0,0183 = 0,09. Con k = 2: √(0,0020 / 2) = 0,0316, Sortino 0,05. El Sharpe mensual es 0,0017 / 0,0271 = 0,06. Conclusión: el Sortino con n supera al Sharpe, pero dividiendo entre los dos meses malos baja por debajo; la convención mueve el resultado de 0,09 a 0,05 sin tocar la estrategia.
:::

## Comprueba que lo sabes

:::quiz
p: Una estrategia tiene Sharpe anual 0,9 y Sortino anual 1,6 calculados sobre la misma serie. ¿Qué lectura es razonable?
o: Que la volatilidad está concentrada en las subidas: los periodos malos son menos profundos o menos frecuentes que los buenos
o: Que el Sortino está mal calculado, porque siempre es menor que el Sharpe
o: Que la estrategia tiene una caída máxima del 1,6 %
a: 1
e: El Sharpe usa toda la volatilidad y el Sortino solo la de los periodos por debajo del objetivo. Si el segundo es bastante mayor, la mayor parte del movimiento está del lado bueno. No hay ninguna regla que obligue al Sortino a ser menor que el Sharpe, ni el Sortino es una caída máxima: es un cociente.
:::

:::quiz
p: ¿Por qué el Calmar de la misma estrategia cambia tanto al pasar de 24 meses a los últimos 12?
o: Porque el denominador es la peor caída del tramo elegido y la caída grande quedó fuera de la ventana corta
o: Porque el retorno anualizado se calcula con la media aritmética y cambia con el número de datos
o: Porque el Calmar se recalcula automáticamente con la inflación
a: 1
e: El Calmar depende de una única observación, la caída máxima, así que la ventana temporal lo domina. En el ejemplo, la caída del 19,04 % vive en los primeros doce meses y desaparece de la ventana corta, así que el ratio pasa de 0,61 a 3,39. El retorno anualizado se compone a partir de la curva de capital, no es una media aritmética, y la inflación no entra en la fórmula.
:::

:::quiz
p: Con `T = 0` y una muestra de cuatro meses todos positivos, ¿cuánto vale el Sortino?
o: No está definido: la desviación bajista es cero y el cociente se va a infinito
o: Vale 4, porque hay cuatro meses y ninguno es negativo
o: Vale lo mismo que el Sharpe, porque no hay pérdidas que penalizar
a: 1
e: Si no hay ninguna desviación negativa respecto al objetivo, el denominador es cero y el ratio no existe. Ese caso no es un éxito: es la señal de que la muestra es demasiado corta o demasiado benigna para medir riesgo bajista. El Sharpe, en cambio, sí se puede calcular, porque la volatilidad total nunca es cero si los retornos varían.
:::

:::nota
Sortino y Calmar no sustituyen al Sharpe: lo completan. El Sharpe es la métrica más comparable
entre estrategias y entre personas, precisamente porque sus supuestos son rígidos. Usa el Sortino
cuando sospeches asimetría y el Calmar cuando lo que te importa es el peor tramo que vas a tener
que aguantar. Y en los tres casos, mira la serie de retornos antes que el número: una curva de
capital enseña en tres segundos lo que un ratio esconde durante meses.
:::
