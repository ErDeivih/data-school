---
id: tamano-muestral
titulo: Cálculo de tamaño muestral
fase: 2
nivel: intermedio
rutas: [ds, de]
prerequisitos: [errores-tipo-i-ii-y-potencia, intervalos-de-confianza, test-t, tamano-del-efecto]
tags: [inferencia, potencia, diseno, experimentos]
resumen: Cuantas observaciones necesitas para detectar el efecto que te importa, y por qué calcularlo después de ver los datos no sirve de nada.
fuentes: ["Cohen (1988), 'Statistical Power Analysis for the Behavioral Sciences'", "Chow, Shao, Wang y Lokhnygina (2017), 'Sample Size Calculations in Clinical Research'"]
---

## En una frase

El tamaño muestral se calcula fijando de antemano el efecto que quieres ser capaz de detectar, el
riesgo de falso positivo que aceptas y la potencia que quieres, y despejando cuántas observaciones
hacen falta para cumplir las tres cosas a la vez.

## La idea

Un contraste de hipótesis tiene cuatro piezas y solo puedes elegir tres:

1. El **nivel de significación** `α`: la probabilidad de declarar un efecto que no existe.
2. La **potencia** `1 − β`: la probabilidad de detectar un efecto que sí existe, del tamaño que
   hayas decidido.
3. El **tamaño del efecto** que quieres detectar, `δ`.
4. El **tamaño de muestra** `n`.

En un análisis normal fijas `α` en 0,05 y te quedas con lo que salga. En un diseño, en cambio,
fijas `α`, decides la potencia que necesitas (0,80 es la convención, 0,90 si el estudio es caro) y
declaras el efecto mínimo que te interesaría detectar. Entonces despejas `n`. Eso es todo el
cálculo, y su dificultad no está en la fórmula sino en la tercera pieza: **decidir qué efecto te
importa**.

Ese número, el **efecto mínimo detectable** (MDE), es una decisión de negocio, no estadística. Si
una campaña de marketing solo se paga sola a partir de un 2 % más de conversión, no tiene sentido
diseñar un estudio para detectar un 0,1 %: o no cambias nada, o diseñas para el 2 %. Y al revés,
si declaras un MDE demasiado optimista, el estudio acabará con un resultado no concluyente y
habrás gastado el presupuesto en aprender nada.

La relación entre `n` y `δ` es cuadrática y es la que se lleva los sustos: **para detectar la mitad
de efecto necesitas cuatro veces más muestra**. Detectar un 1 % en lugar de un 2 % no cuesta el
doble, cuesta el cuádruple.

Dos cosas que conviene tener claras desde el principio:

- **La potencia calculada a posteriori no sirve.** Si ya tienes los datos, la «potencia observada»
  con el efecto estimado es una función monótona del p-valor: no añade información ninguna. Si te
  preocupa la potencia, se calcula antes, con el MDE.
- **El efecto del piloto está sesgado al alza.** Si estimas `δ` con un estudio de 12 personas, ese
  estudio solo se publicó porque salió grande. Usar ese valor para dimensionar el estudio
  definitivo te deja corto casi siempre. Es el mismo sesgo de selección que aparece con las
  [[multiplicidad-y-fdr|comparaciones múltiples]].

## Definición formal

Para comparar dos medias con un test bilateral, el número de observaciones **por grupo** es:

:::formula
n = 2 · (z₁₋α/₂ + z₁₋β)² · σ² / δ²
:::

- `α` — riesgo de falso positivo que aceptas; `z₁₋α/₂` es su cuantil normal (1,96 si α = 0,05).
- `1 − β` — potencia; `z₁₋β` es su cuantil (0,842 si la potencia es 0,80). Un `β` de 0,20 es la
  probabilidad de no detectar un efecto que existe.
- `σ` — desviación típica de la variable de respuesta, estimada de datos previos o de la
  literatura.
- `δ` — diferencia de medias que quieres ser capaz de detectar.
- `n` — unidades por grupo.

:::figura
fichero: tamano-muestral-curva-y-conglomerados
pie: A la izquierda, unidades por grupo frente al efecto estandarizado, con los tres puntos del ejemplo: 6,2 segundos (52,2), 3,1 (205,9) y 1,55 (820,6). La curva es la fórmula entera y lo que enseña es que cada vez que divides el efecto por dos la muestra se multiplica por cuatro: 52 personas no pueden detectar 1,55 segundos, y eso no se arregla analizando mejor. A la derecha, el efecto de diseño que se olvida siempre: con tiendas de 20 usuarios y ρ = 0,05 vale 1,95, así que los 53 por grupo del cálculo limpio pasan a 103. Es el mismo estudio y casi el doble de presupuesto.
fuente: figuras/tamano-muestral-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Observaciones necesarias por grupo | observaciones | Es el resultado de la formula. Se redondea SIEMPRE hacia arriba y nunca a la baja: 52,2 son 53, no 52. Ademas es el mínimo para la potencia que pediste, no un objetivo que se pueda analizar antes de alcanzar |
| `delta` | Diferencia de medias que quieres ser capaz de detectar (MDE) | las de la variable | Es la palanca que manda: `n` va con `1/delta^2`. Partirlo por la mitad cuadruplica la muestra, y fijarlo mirando el presupuesto en vez del negocio es la trampa circular que describe la página |
| `sigma` | Desviación típica de la respuesta | las de la variable | Entra al cuadrado en la versión de medias: duplicar la variabilidad duplica la gente necesaria. Se estima de datos previos, y si la estimación es optimista el estudio sale infrapotenciado |
| `d` | Efecto estandarizado `delta / sigma` | adimensional | Es la versión que se usa en `statsmodels`: `solve_power(effect_size=d, ...)`. Pasarle `delta` en segundos en vez de `d` no da error, da un número absurdo. La regla de andar por casa es `n ≈ 16/d^2` por grupo con alpha 0,05 y potencia 0,80 |
| `p` | Tasa esperada cuando la métrica es una proporción | tanto por uno | Sustituye a `sigma^2` por `p(1-p)`, que vale como maximo 0,25 en `p = 0,5`. Cuanto mas cerca de 0 o de 1 este la tasa, menos gente hace falta para el mismo delta absoluto |
| `alpha` | Riesgo de falso positivo aceptado | probabilidad | Baja a traves de `z_(1-alpha/2)`: pasar de 0,05 a 0,01 sube ese cuantil de 1,96 a 2,58 y engorda `n`. Usar una cola para «ganar» potencia solo es legitimo si se decide antes de ver los datos |
| `1 - beta` | Potencia | probabilidad | `z_(1-beta)` vale 0,842 con 0,80 y 1,282 con 0,90: subir la potencia cuesta un 34 % mas de muestra con los demas números fijos. La potencia calculada después, con el efecto observado, es una función monotona del p-valor y no informa |
| `r` | Fracción de unidades que se espera perder | tanto por uno | Divide: se recluta `n / (1 - r)`. Con un 15 % de abandonos el factor es 1/0,85 = 1,176, un 17,6 % mas. Un 20 % de perdidas sobre 200 sujetos deja 160 y el estudio pierde la potencia que creia tener |
| `DEFF` | Efecto de diseño por conglomerados: `1 + (m - 1)·rho` | multiplicador, mayor o igual que 1 | Nunca baja de 1: si rho es 0 vuelve a 1 y no hay penalización. Con `m = 20` y `rho = 0,05` vale 1,95 y casi duplica el presupuesto. Ignorarlo es la causa habitual de que un ensayo por conglomerados acabe sin potencia |
| `rho` | Correlación intraclase: cuanto se parecen las unidades del mismo grupo | adimensional, de 0 a 1 | Es el parámetro que decide el encarecimiento por conglomerados. Cuanto mas alto, mas se parece la gente de la misma tienda o el mismo equipo y menos información aporta cada unidad extra |
| `m` | Unidades por conglomerado | unidades | Multiplica el efecto de diseño a traves de `(m - 1)`: pasar de tiendas de 20 a tiendas de 50 con el mismo rho lleva el DEFF de 1,95 a 3,45. Conviene usar conglomerados pequeños y muchos |
:::

Para una proporción se sustituye `σ²` por `p·(1 − p)`, con `p` la tasa esperada:

:::formula
n = 2 · (z₁₋α/₂ + z₁₋β)² · p · (1 − p) / δ²
:::

Regla de andar por casa con α = 0,05 y potencia 0,80: `2 · (1,96 + 0,842)² = 15,7`, así que
`n ≈ 16 · σ² / δ²` por grupo, es decir `n ≈ 16 / d²` con `d = δ/σ`.

**Ajustes que se olvidan siempre.**

- **Abandonos**: si esperas perder una fracción `r` de las unidades, recluta
  `n / (1 − r)`. Con un 15 % de abandonos, un 17,6 % más.
- **Diseño por conglomerados**: si las unidades vienen en grupos (aulas, tiendas, equipos) con
  correlación intraclase `ρ` y `m` unidades por grupo, el tamaño efectivo se multiplica por el
  **efecto de diseño**:

:::formula
DEFF = 1 + (m − 1) · ρ
:::

Con `m = 20` y `ρ = 0,05`, `DEFF = 1,95`: necesitas casi el doble de unidades que en un diseño
individual. En encuestas y ensayos por conglomerados, esto es la diferencia entre un estudio
potente y uno inútil.

## Ejemplo

Quieres detectar una diferencia de tiempo de proceso entre dos métodos. Por datos previos sabes que
la desviación típica es 11,2 segundos. Con α = 0,05 y potencia del 80 %, el número de unidades por
grupo para tres efectos distintos:

```text
delta (s)   d = delta/11,2   n por grupo
   6,2          0,554            52,2
   3,1          0,277           205,9
   1,55         0,138           820,6
```

Dos lecturas importantes:

- **La mitad de efecto, el cuádruple de muestra.** Pasar de 6,2 a 3,1 segundos multiplica por 4 la
  muestra necesaria, y volver a dividir el efecto por dos la multiplica otra vez por 4.
- **El mismo estudio no puede detectarlo todo.** Con 52 personas por grupo, un efecto de 1,55
  segundos es invisible: aunque exista, el estudio acabará con p > 0,05 y la conclusión será «no
  hemos encontrado evidencia», que no es lo mismo que «no existe».

Añadiendo los ajustes al escenario de 6,2 segundos: redondeas a **53 por grupo**, y si esperas un
15 % de abandonos reclutas 53 / 0,85 = **63 por grupo**. Si además asignas por tiendas de 20
usuarios con `ρ = 0,05`, el efecto de diseño es 1,95 y necesitas 53 · 1,95 = **103 por grupo**:
casi el doble de lo que decía la fórmula limpia.

## Código

```python verificable
from statsmodels.stats.power import TTestIndPower

# Cuanta muestra hace falta para detectar distintos efectos con desviacion 11,2.
analisis = TTestIndPower()
for delta in (6.2, 3.1, 1.55):
    n = analisis.solve_power(effect_size=delta / 11.2, alpha=0.05, power=0.80, ratio=1.0)
    print(f"delta {delta:>5.2f}  d {delta / 11.2:.3f}  n por grupo {n:>7.1f}")
    # -> delta  6.20  d 0.554  n por grupo    52.2
    # -> delta  3.10  d 0.277  n por grupo   205.9
    # -> delta  1.55  d 0.138  n por grupo   820.6
```

:::claves
- `analisis.solve_power(effect_size=..., alpha=..., power=..., ratio=1.0)` devuelve el valor del parámetro que **no** le has dado. Si le pasas `nobs1` en vez de dejar `power` sin especificar, te devuelve la potencia (0,806 con `nobs1=53`) en lugar de la muestra, y ese número no da error: parece un resultado. Aquí se omite `nobs1` a propósito, que es lo que hace que despeje `n`.
- El nombre del argumento es `effect_size` y no `delta` ni `d`: es el efecto **estandarizado**. Pasarle `6.2` en vez de `6.2 / 11.2` no lanza una excepción: statsmodels avisa con un `ConvergenceWarning` por stderr y devuelve `nan`. El `nan` se imprime sin más si no compruebas el resultado, y un `nan` formateado con `:.1f` sale como `nan` en medio de la tabla.
- `solve_power` devuelve un `float` redondeado por statsmodels, no un entero: 52,2 no es un número de personas. La página redondea a 53 hacia arriba en el bloque siguiente y lo dice. `int(n)` sobre 52,2 da 52 y trunca, así que el estudio quedaría por debajo de la potencia prometida.
- El `for delta in (6.2, 3.1, 1.55)` reutiliza la misma instancia de `TTestIndPower` para las tres llamadas. Es correcto y barato, pero conviene saber que el objeto no guarda estado: `solve_power` es una función pura sobre sus argumentos, así que cambiar `ratio` entre iteraciones no contamina la siguiente.
- En el segundo bloque, `np.ceil(n / (1 - abandono))` es una función de NumPy y devuelve `np.float64`, no un entero: por eso el `print` lleva `:.0f`. Si lo usaras para indexar o para `range()`, necesitarías `int(...)`. Y el `ceil` está aplicado **antes** de multiplicar por el DEFF: el orden correcto es ajustar por pérdidas y luego por diseño, porque las dos penalizaciones se acumulan sobre el total.
- `deff = 1 + (m - 1) * rho` con `m = 20` y `rho = 0.05` da 1,95, un número que crece linealmente con `m` cuando `rho` es fijo. Con `rho = 0` la fórmula devuelve 1 sin ninguna rama especial; si te olvidaras del `1 +`, el DEFF valdría 0,95 y **reduciría** la muestra justo cuando hay que aumentarla.
:::

```python verificable
import numpy as np

n = 53                       # el calculo anterior redondeado hacia arriba
abandono = 0.15              # esperamos perder un 15 % de los sujetos

print(f"reclutar por grupo {np.ceil(n / (1 - abandono)):.0f}")   # -> reclutar por grupo 63

# Diseno por conglomerados: 20 usuarios por tienda y correlacion intraclase 0,05.
m, rho = 20, 0.05
deff = 1 + (m - 1) * rho
print(f"efecto de diseno {deff:.2f}  n necesario {n * deff:.0f}")
# -> efecto de diseno 1.95  n necesario 103
```

## Errores típicos

- **Calcular la potencia a posteriori con el efecto observado.** Es una transformación del
  p-valor: si el resultado no es significativo, la «potencia observada» saldrá baja por
  construcción. No sirve para justificar ni para rescatar un estudio.
- **Sacar `δ` de un piloto diminuto.** El efecto del piloto está sobreestimado porque solo viste
  el que salió grande. Dimensiona con el efecto mínimo que te interese por razones de negocio, no
  con el que viste en 12 casos.
- **Olvidar los abandonos y los datos incompletos.** Un 20 % de pérdidas sobre 200 sujetos te deja
  160, y el estudio pierde la potencia que creías tener. Recluta `n / (1 − r)`.
- **Ignorar el diseño por conglomerados.** Añadir una `DEFF` de 2 no es un detalle: es duplicar el
  presupuesto. Si no la aplicas, el estudio sale infrapotenciado.
- **Usar una cola para «ganar» potencia sin justificarlo.** Reduce el tamaño necesario, pero solo
  es legítimo si de verdad solo te interesa una dirección y lo decides antes de ver los datos.
- **Redondear a la baja y analizar antes de tiempo.** El cálculo da un mínimo, no un objetivo
  aproximado. Si el número sale 52,2, usa 53 por grupo.
- **Confundir «no significativo» con «sin efecto».** Un estudio con potencia para detectar
  `d = 0,5` no dice nada sobre un efecto de `d = 0,1`. La conclusión correcta es «no tengo muestra
  para esto», no «no hay nada».
- **Elegir el MDE mirando qué tamaño muestral es asumible.** Es la trampa circular: primero se
  decide el efecto relevante y luego se busca el presupuesto, no al revés. Si no hay presupuesto,
  la respuesta honesta es «con este dinero no puedo responder a esta pregunta».

:::practica
enunciado: Una web convierte al 10 %. Diseñas un test A/B bilateral con α = 0,05 (z = 1,96) y potencia del 80 % (z = 0,842) para detectar una subida hasta el 13 %. Calcula cuántos usuarios necesitas por grupo y ajústalo con un 20 % de abandonos.
pista: Para proporciones se sustituye σ² por p·(1 − p) con la tasa esperada, y δ es la diferencia absoluta: 0,03.
solucion: n = 2 · (1,96 + 0,842)² · 0,10 · 0,90 / 0,03² = 2 · 7,851 · 0,09 / 0,0009 = 15,702 · 100 = 1570,2, es decir 1571 usuarios por grupo. Con un 20 % de abandonos reclutas 1571 / 0,80 = 1963,8, esto es 1964 por grupo. Redondear a la baja u olvidar las pérdidas deja el estudio sin la potencia prometida.
:::

## Comprueba que lo sabes

:::quiz
p: Con desviación típica 11,2, alpha = 0,05 y potencia del 80 %, necesitas 52,2 unidades por grupo para detectar 6,2 segundos. ¿Cuántas necesitas para detectar 3,1 segundos?
o: Unas 104, el doble
o: Unas 206, el cuádruple
o: Las mismas, porque la desviación típica no cambia
a: 2
e: El tamaño muestral depende de delta al cuadrado, así que dividir el efecto entre 2 multiplica la muestra por 4: 52,2 pasa a 205,9. Es la relación más importante que hay que interiorizar de este concepto, porque explica por qué los efectos pequeños son tan caros de demostrar.
:::

:::quiz
p: Un estudio ya terminado no ha salido significativo. Un compañero calcula la potencia «observada» con el efecto que salió y dice que era del 20 %, así que el estudio estaba infrapotenciado. ¿Qué hay de malo?
o: Nada, es la forma correcta de comprobar la potencia
o: Que la potencia observada con el efecto estimado es una función monótona del p-valor y no aporta información nueva; la potencia se calcula antes con el MDE
o: Que la potencia nunca puede ser del 20 %
a: 2
e: Si el resultado no es significativo, la potencia calculada con el efecto observado saldrá baja siempre, por construcción. No es un diagnóstico, es el mismo dato con otra forma. Lo que sí puedes hacer es reportar el intervalo de confianza del efecto y decir qué tamaños de efecto quedan descartados.
:::

:::quiz
p: Diseñas un estudio asignando tiendas completas al tratamiento, con 20 usuarios por tienda y una correlación intraclase de 0,05. La fórmula limpia daba 53 usuarios por grupo. ¿Qué usas?
o: 53, porque la correlación intraclase no afecta al tamaño muestral
o: 103, porque el efecto de diseño 1 + (20-1)·0,05 = 1,95 multiplica el tamaño necesario
o: 20, porque cada tienda ya es un grupo
a: 2
e: Las unidades de una misma tienda se parecen entre sí, así que aportan menos información que 20 usuarios independientes. El efecto de diseño cuantifica esa pérdida: 1,95, es decir, casi el doble de unidades. Ignorarlo es la causa habitual de que un ensayo por conglomerados acabe sin potencia.
:::

:::aviso
Si al calcular el tamaño muestral te sale un número que no puedes pagar, no recortes el número:
recorta la ambición. Cambia el MDE por uno mayor y di explícitamente que solo podrás detectar
efectos grandes. Un estudio infrapotenciado no es un estudio más barato, es un estudio que no
responde a la pregunta.
:::
