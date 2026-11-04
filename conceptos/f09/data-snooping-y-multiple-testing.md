---
id: data-snooping-y-multiple-testing
titulo: Data snooping y pruebas múltiples
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [p-valor, multiplicidad-y-fdr, contraste-de-hipotesis]
tags: [sesgo, contrastes, backtest, p-hacking]
resumen: Si pruebas muchas ideas y te quedas con la mejor, el resultado está sesgado: cuántos intentos hacen falta para que el azar parezca una estrategia rentable.
fuentes: ["White (2000), 'A Reality Check for Data Snooping'", "Benjamini y Hochberg (1995), 'Controlling the False Discovery Rate'"]
---

## En una frase

El **data snooping** es usar la misma muestra para buscar la idea y para confirmarla: si pruebas
muchas variantes y publicas la mejor, el número que publicas está sesgado al alza porque estás
informando de un máximo, no de una estimación.

## La idea

Imagina que repartes una moneda entre mil personas y cada una la lanza diez veces. Alguien sacará
diez caras. No has descubierto a nadie con poderes: has hecho mil experimentos y has enseñado el
mejor. Con una sola persona, sacar diez caras seguidas tiene una probabilidad de 1/1.024 y sería
una noticia. Con mil personas, la probabilidad de que **alguien** lo consiga es
`1 − (1 − 1/1.024)¹⁰⁰⁰ ≈ 62 %`. La rareza del resultado individual no cambia; lo que cambia es
cuántas veces lo has intentado.

En una investigación cuantitativa esto pasa constantemente y casi siempre sin mala intención:
pruebas la señal con tres ventanas, con dos umbrales, en cuatro mercados y con el stop en dos
niveles. Has hecho 48 backtests y te quedas con el mejor. El [[p-valor|p-valor]] de ese backtest
se calculó como si fuera el único que hiciste, y no lo fue.

La multiplicidad también entra por puertas menos evidentes:

- **La variable objetivo.** ¿Retorno a un día, a cinco, a veinte? Cada elección es un intento.
- **El universo.** Probar la idea en 30 acciones y quedarte con las 5 donde funciona es
  selección, no validación.
- **El periodo.** Empezar en 2010 o en 2015 cambia el resultado; elegir el que mejor queda es un
  intento más.
- **La métrica.** Sharpe, beneficio total, porcentaje de acierto, caída máxima. Si eliges la que
  sale bien, has probado varias.
- **Los intentos que no cuentas.** Los proyectos abandonados, las variantes que no llegaste a
  ejecutar del todo, las que un compañero probó antes. La literatura llama a esto el sesgo del
  cajón: solo se publica lo que funcionó.

El resultado es que un backtest con un aspecto espectacular puede no contener ninguna información.
Con 1.000 estrategias sin ninguna habilidad, cada una medida sobre 250 días, el mejor estadístico
`t` observado fue 3,14 en nuestra simulación, con un p-valor sin ajustar de 0,0017. Y el máximo
esperado por puro azar con 1.000 intentos es `√(2 · ln 1000) = 3,72`. Es decir: el «descubrimiento»
está **por debajo** de lo que produce el ruido cuando buscas mucho. El data snooping no es un matiz
estadístico: es la diferencia entre un resultado y una casualidad bien peinada.

Las defensas, en orden de eficacia:

1. **Cuenta los intentos y dilo.** No hay corrección posible sin saber cuántos tiros hiciste. Si no
   los llevas apuntados desde el principio, ya has perdido la cuenta.
2. **Guarda datos que no hayas mirado.** La única confirmación limpia es aplicar la idea a datos
   que no participaron en la búsqueda: un periodo posterior, otro mercado, otro universo. Esto es
   más valioso que cualquier corrección estadística.
3. **Corrige por multiplicidad** con Bonferroni, Holm o Benjamini-Hochberg, sabiendo que son
   conservadoras cuando los contrastes están correlacionados (y en finanzas lo están: todas las
   variantes se prueban sobre los mismos precios).
4. **Usa contraste por remuestreo** cuando la dependencia importa: el Reality Check de White y el
   test SPA de Hansen comparan la mejor estrategia contra una distribución nula generada
   remuestreando, preservando la correlación entre estrategias. En la misma familia está
   [[sharpe-deflactado|el Sharpe deflactado]], que ajusta directamente el Sharpe por el número de
   intentos y por la forma de la distribución.

:::trampa
Corregir el p-valor y después seguir eligiendo es inútil. Si aplicas Bonferroni a los 48 backtests
pero luego te quedas con el mejor de los 48 y lo presentas como si fuera el único que pasó el
filtro, no has corregido nada: has movido el problema de sitio.
:::

## Definición formal

Con `m` contrastes simultáneos y un nivel de significación `α` por contraste, la probabilidad de
cometer al menos un falso positivo (la **tasa de error por familia**, FWER) es:

:::formula
FWER = P(al menos un falso positivo) = 1 − (1 − α)^m ≈ m · α        E[max Z] ≈ √(2 · ln m)
:::

- `m` — número de contrastes o de configuraciones probadas. Es un dato que hay que contar a mano.
- `α` — nivel de significación de cada contraste por separado (0,05 es lo habitual).
- `Z` — estadístico estandarizado de cada contraste (el `t` de un Sharpe, por ejemplo).
- `E[max Z]` — máximo esperado de `m` estadísticos independientes bajo la hipótesis nula: crece
  con `√(ln m)`, despacio pero sin techo. Con 10 intentos vale 2,15; con 1.000, 3,72.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `m` | El número de contrastes o de variantes probadas | contrastes | Es el dato que hay que contar a mano, e incluye las variantes abandonadas y los cambios de periodo, universo y métrica; de él dependen todas las correcciones |
| `α` | El nivel de significación de cada contraste por separado | probabilidad (0,05 es lo habitual) | Al subirlo pasan más contrastes sin corregir y la probabilidad de algún falso positivo crece aún más deprisa |
| `FWER` | La probabilidad de cometer al menos un falso positivo entre todos los contrastes | entre 0 y 1 | Crece como `1 − (1 − α)^m`: con 20 contrastes vale 0,64 y con 1.000, 0,994 |
| `Z` | El estadístico estandarizado de cada contraste (el `t` de un Sharpe, por ejemplo) | adimensional | Es lo que se compara con los umbrales; con muchos intentos hay que contrastarlo con el máximo que produce el azar, no con el 2 de un contraste único |
| `E[max Z]` | El máximo esperado de `m` estadísticos independientes bajo la hipótesis nula | adimensional | Crece como `√(2 · ln m)`, despacio y sin techo: 2,15 con 10 intentos y 3,72 con 1.000 |
| `p_i` | El p-valor del contraste `i` | entre 0 y 1 | Es lo que se compara con los umbrales corregidos; sin corregir, el p-valor de la variante elegida entre muchas no es el que calculaste |
| `α / m` | El umbral de Bonferroni para cada contraste | probabilidad | Al crecer `m` se hace diminuto: con 1.000 pruebas exige `p ≤ 0,00005`, que equivale a un `t` de 4,06 |
| `α · i / m` | El umbral de Benjamini-Hochberg para el p-valor que ocupa el puesto `i` | probabilidad | Es más permisivo que Bonferroni a propósito: controla la proporción esperada de falsos descubrimientos, no la probabilidad de que exista alguno |
:::

Las dos correcciones clásicas, con criterios distintos:

- **Bonferroni:** se rechaza el contraste `i` si `p_i ≤ α / m`. Controla la FWER (la probabilidad
  de **algún** falso positivo) y es muy conservador cuando los contrastes están correlacionados.
  Holm es una versión secuencial que controla lo mismo y siempre rechaza al menos tanto.
- **Benjamini-Hochberg (FDR):** se ordenan los p-valores de menor a mayor y se busca el mayor `i`
  tal que `p_(i) ≤ α · i / m`; se rechazan los `i` primeros. Controla la **proporción esperada de
  falsos descubrimientos** entre los rechazados, no la probabilidad de que exista alguno. Es el
  criterio adecuado cuando estás cribando muchas ideas y puedes tolerar que algunas sean falsas.

Sobre la corrección hay una decisión que casi nunca se explicita: estás corrigiendo por `m`
intentos, pero tus intentos no son independientes. Bonferroni sobre 1.000 variantes de la misma
señal es absurdamente severo, y el p-valor sin corregir es absurdamente optimista. Ninguno de los
dos extremos es correcto, y de ahí que en series temporales se prefiera el remuestreo, que estima
la distribución del máximo conservando la correlación entre estrategias.

:::figura
fichero: snooping-maximo-por-azar
pie: Arriba, la probabilidad de encontrar al menos un falso positivo según cuántas variantes pruebes: con 20 es del 64 % y con 1.000 prácticamente del 100 %, sin que ninguna tenga habilidad. Abajo, el estadístico de 1.000 estrategias que son puro ruido: la mejor da `t = 3,14`, por debajo del máximo esperado por azar con 1.000 intentos (3,72) y muy por debajo del umbral que exigiría Bonferroni (4,06). Un resultado así no aporta evidencia a favor de nada.
fuente: figuras/data-snooping-y-multiple-testing-1.py
:::

## Ejemplo

Veinte p-valores de veinte variantes de una misma idea, en orden creciente: 0,0001; 0,0008;
0,0021; 0,0043; 0,0067; 0,0091; 0,0122; 0,0180; 0,0245; 0,0301; 0,0410; 0,0520; 0,0680; 0,0900;
0,1200; 0,1800; 0,2400; 0,3100; 0,4500; 0,6200.

- **Sin ajustar**, con `α = 0,05`: once p-valores por debajo del umbral. «Once señales
  significativas» suena a hallazgo.
- **Bonferroni**: el umbral pasa a `0,05 / 20 = 0,0025` y solo sobreviven tres.
- **Benjamini-Hochberg**: se compara cada p-valor ordenado con `0,05 · i / 20`. El octavo
  (0,0180) cumple `0,0180 ≤ 0,05 · 8 / 20 = 0,0200`, y el noveno (0,0245) no cumple
  `0,0245 ≤ 0,0225`. Así que se rechazan los ocho primeros.

Tres cifras para los mismos datos: 11, 3 y 8. La diferencia entre ellas no es estadística
avanzada, es decidir qué error estás dispuesto a tolerar. Si buscas ideas para explorar después,
8 es razonable. Si vas a publicar «esta señal funciona», 3 es más defendible.

Y el caso de la simulación, que es el que más escuece: 1.000 estrategias sin ninguna habilidad,
250 días cada una. La mejor da `t = 3,14`, con un p-valor sin ajustar de 0,0017. El máximo
esperado por azar es 3,72 y el umbral que exige Bonferroni para 1.000 pruebas es 4,06. La
conclusión no es que la estrategia sea mala: es que este experimento no aporta ninguna evidencia a
su favor.

## Código

```python verificable
import numpy as np

p = np.array([0.0001, 0.0008, 0.0021, 0.0043, 0.0067, 0.0091, 0.0122, 0.0180,
              0.0245, 0.0301, 0.0410, 0.0520, 0.0680, 0.0900, 0.1200, 0.1800,
              0.2400, 0.3100, 0.4500, 0.6200])
alfa, m = 0.05, p.size

# Bonferroni: umbral por contraste alfa/m. Benjamini-Hochberg: se compara el
# p-valor ordenado i con alfa*i/m y se rechazan los i primeros que cumplen.
orden = np.argsort(p)
pasa = p[orden] <= alfa * np.arange(1, m + 1) / m
k_max = (np.max(np.where(pasa)[0]) + 1) if pasa.any() else 0

print(f"m={m} contrastes, alfa={alfa}")                          # -> 20 y 0.05
print(f"sin ajustar: {int((p <= alfa).sum())}")                  # -> 11
print(f"Bonferroni : {int((p <= alfa / m).sum())}")              # -> 3
print(f"Benjamini-Hochberg: {k_max}")                            # -> 8
```

:::claves
- `np.argsort(p)` devuelve los **índices** que ordenarían el array, no los valores ordenados: para ver los p-valores ordenados hay que escribir `p[orden]`. Mezclar las dos cosas no da error, da otro número.
- Los umbrales de Benjamini-Hochberg son `alfa * np.arange(1, m + 1) / m`. Ese `1` inicial es lo que hace que el primer puesto se compare con `α/m` y no con cero; es un desplazamiento de un elemento que cambia cuántos se rechazan.
- `np.where(pasa)[0]` es la versión de NumPy de «dónde es verdad»: devuelve una tupla con un array de posiciones dentro, de ahí el `[0]`. Y `np.max(...) + 1` traduce la posición a número de rechazados porque los índices empiezan en 0.
- Si ninguna posición cumple la condición, `np.max` de un array vacío lanza un error; el `if pasa.any() else 0` no es cosmética, es lo que evita que el caso «no hay nada significativo» reviente el programa.
- En BH hay que quedarse con el **mayor** puesto que cumple `p_(i) ≤ α · i / m` y rechazar todos los anteriores. Si el puesto 3 falla y el 4 cumple, se rechazan los cuatro primeros; parar en el primer fallo daría una respuesta distinta.
- `int((p <= alfa).sum())` compara el array con un escalar elemento a elemento y suma los `True`, que es el recuento sin ajustar. No hace falta ninguna librería de contrastes: `statsmodels` haría lo mismo con `multipletests(p, alpha=0.05, method="fdr_bh")`, pero los umbrales son aritmética de tres líneas y conviene verlos.
:::

```python verificable
import numpy as np
from statistics import NormalDist

Z = NormalDist()
rng = np.random.default_rng(0)
m, n = 1000, 250        # 1000 estrategias sin alpha, 250 dias cada una
r = rng.normal(0.0, 0.01, size=(m, n))
t = r.mean(axis=1) / (r.std(axis=1, ddof=1) / np.sqrt(n))
mejor = float(t.max())

print(f"mejor t de {m} estrategias sin alpha: {mejor:.2f}")      # -> 3.14
print(f"p-valor sin ajustar: {2 * (1 - Z.cdf(mejor)):.5f}")      # -> 0.00169
print(f"t esperado del maximo por azar: {np.sqrt(2 * np.log(m)):.2f}")   # -> 3.72
print(f"t exigido por Bonferroni: {Z.inv_cdf(1 - 0.025 / m):.2f}")       # -> 4.06
```

## Errores típicos

- **No contar los intentos.** Las correcciones necesitan el número de pruebas, y ese número incluye
  las variantes abandonadas, los cambios de periodo, de universo y de métrica. Si solo cuentas las
  que llegaron al final, estás corrigiendo por una fracción del sesgo.
- **Aplicar Bonferroni a contrastes muy correlacionados y concluir que «no hay nada».**
  Mil variantes de la misma señal se mueven casi juntas; el umbral de Bonferroni castiga la
  redundancia como si fueran mil experimentos independientes. Con dependencia fuerte, remuestreo.
- **Elegir la métrica después de ver los resultados.** Si pruebas Sharpe y porcentaje de acierto y
  publicas el que sale significativo, has duplicado los intentos sin decirlo. La métrica se fija
  antes.
- **Confundir significación con rentabilidad.** Un resultado puede ser estadísticamente sólido y
  económicamente irrelevante después de comisiones y deslizamiento, o al revés. Son dos preguntas
  y necesitan dos respuestas ([[tamano-del-efecto|tamaño del efecto]] y
  [[slippage-y-comisiones|costes]]).
- **Validar sobre los datos de la búsqueda.** Elegir la mejor variante y reportar su rendimiento en
  la misma muestra no es validar: es describir el máximo de la muestra. Sin datos apartados no hay
  confirmación posible.
- **Creer que el número de intentos es 1 porque solo has entrenado un modelo.** El modelo es uno,
  pero la arquitectura, las variables, el preprocesado y la etiqueta los has elegido tú mirando
  resultados intermedios. Todas esas decisiones son intentos.

:::practica
enunciado: Con α = 0,05 y estos diez p-valores ordenados de diez variantes de una señal —0,002; 0,008; 0,013; 0,019; 0,026; 0,032; 0,038; 0,045; 0,048; 0,300—, calcula cuántas declaras significativas sin ajustar, con Bonferroni y con Benjamini-Hochberg.
pista: Bonferroni compara cada p con α/m; Benjamini-Hochberg compara el p-valor del puesto i con α · i / m y se queda con el mayor i que cumpla.
solucion: Sin ajustar pasan las nueve primeras. Bonferroni exige p ≤ 0,05 / 10 = 0,005, así que solo sobrevive 0,002. En BH el umbral del puesto i es 0,005 · i: 0,002 ≤ 0,005; 0,008 ≤ 0,010; 0,013 ≤ 0,015; 0,019 ≤ 0,020; 0,026 > 0,025, y de ahí en adelante ninguna cumple. El mayor i válido es 4, así que se rechazan cuatro. Tres respuestas para los mismos datos: 9, 1 y 4.
:::

## Comprueba que lo sabes

:::quiz
p: Pruebas 20 variantes de una idea y ninguna tiene habilidad real. Con α = 0,05, ¿cuál es la probabilidad aproximada de encontrar al menos una «significativa»?
o: El 5 %, porque cada contraste tiene su propio 5 %
o: Alrededor del 64 %, porque 1 − 0,95^20 ≈ 0,64
o: El 100 %, porque con 20 intentos siempre sale algo
a: 2
e: Cada contraste mantiene su 5 % de falso positivo por separado, pero lo que te importa es la probabilidad de que aparezca alguno, que se acumula: 1 − (1 − 0,05)^20 ≈ 0,64. Con 100 contrastes, el 99,4 %. Por eso el p-valor de un contraste elegido entre muchos no es el p-valor que calculaste.
:::

:::quiz
p: Con 1.000 estrategias sin habilidad, la mejor da t = 3,14 (p = 0,0017). ¿Qué lectura es correcta?
o: La estrategia es prometedora porque el p-valor es muy pequeño
o: El resultado está por debajo del máximo que produce el azar con 1.000 intentos (3,72), así que no aporta evidencia
o: Hay que repetir la simulación con otra semilla hasta que el mejor t baje de 2
a: 2
e: El máximo esperado de 1.000 estadísticos nulos es aproximadamente √(2·ln 1000) = 3,72 y el umbral de Bonferroni es 4,06. Un máximo de 3,14 es un resultado corriente cuando se busca mucho: no hay nada que explicar. Repetir hasta que salga otra cosa es exactamente el comportamiento que genera el problema.
:::

:::quiz
p: ¿Cuándo es más apropiado el criterio de Benjamini-Hochberg que el de Bonferroni?
o: Cuando los contrastes son independientes y quieres garantizar cero falsos positivos
o: Cuando estás cribando muchas ideas y puedes tolerar una proporción conocida de falsos descubrimientos entre las que seleccionas
o: Cuando tienes menos de diez contrastes
a: 2
e: Bonferroni controla la probabilidad de que exista al menos un falso positivo, y por eso exige mucho a cada contraste. Benjamini-Hochberg controla la proporción esperada de falsos descubrimientos entre los rechazados, lo que da más potencia y encaja mejor en una fase exploratoria. Si de la lista solo vas a llevar una idea a producción, la FWER es el criterio conservador.
:::
