---
id: sesgo-de-supervivencia
titulo: Sesgo de supervivencia
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [sesgo-de-mirar-al-futuro, retornos-logaritmicos]
tags: [sesgo, backtest, datos, validacion]
resumen: Analizar solo los fondos, acciones o exchanges que siguen vivos y tomar ese grupo como si fuera el mercado entero: la media que sale nunca existió.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 7", "Elton, Gruber y Blake (1996), 'Survivorship Bias and Mutual Fund Performance'"]
---

## En una frase

Hay sesgo de supervivencia cuando sacas conclusiones de un grupo que ha llegado hasta hoy
—fondos que siguen abiertos, empresas que aún cotizan, exchanges que no han quebrado— y lo
tratas como si fuera una muestra representativa del mercado.

## La idea

Quieres saber cuánto gana un fondo de inversión. Abres una base de datos de fondos, filtras los
que tienen diez años de historia y calculas la rentabilidad media. El número sale bonito. El
problema es que esa base de datos solo contiene fondos que **existen hoy**, y un fondo no
desaparece al azar: desaparece cuando va mal. Se liquida, se fusiona con otro o simplemente deja
de reportar. Los malos se van, los buenos se quedan, y tú has medido a los que se quedaron.

Es el mismo error que preguntar por la estatura media de la población encuestando en la puerta
de un club de baloncesto: has seleccionado la muestra por el propio resultado que querías medir.

El mecanismo tiene tres versiones que conviene no mezclar, porque las tres se arreglan de forma
distinta:

1. **Desaparición.** El miembro sale del universo porque muere: el fondo se cierra, la empresa
   quiebra, el exchange deja de operar. Tu base de datos de hoy solo tiene a los vivos.
2. **Relleno hacia atrás (backfill).** Un fondo entra en la base de datos cuando le conviene,
   normalmente después de un buen año, y en ese momento entrega su historial anterior. Los años
   malos de arranque están en el fichero que te llega, pero no en el universo que existía
   entonces: cuando calculas la rentabilidad media «de los fondos de 2015» estás incluyendo
   fondos que en 2015 no aparecían por ninguna parte.
3. **Universo reconstruido con la lista de hoy.** Haces un backtest comprando «las empresas del
   índice» y usas la lista actual de componentes. Las que quebraron o fueron expulsadas del
   índice no aparecen. Has comprado, a toro pasado, exactamente las que aguantaron.

Los tres tienen el mismo efecto: la muestra queda elegida por el resultado. Y el sesgo es
**asimétrico**: casi siempre infla la rentabilidad, porque lo que desaparece es lo que iba mal.
Por eso una estrategia de «invertir en las mejores empresas del sector» siempre parece
funcionar mejor de lo que funcionó.

:::figura
fichero: sesgo-de-supervivencia-los-que-faltan
pie: Los fondos que se caen de la base de datos se concentran en la zona mala, así que la muestra que queda está desplazada hacia arriba. A la derecha se ve la otra cara: cuanto más selectiva es la muestra, más se infla la media, y solo desaparece el sesgo si no desaparece nadie.
fuente: figuras/sesgo-de-supervivencia-1.py
:::

La corrección se llama universo **punto en punto**: para cada fecha, qué miembros existían y
estaban en el índice ese día, con sus precios de entonces y sin historial añadido después. Eso
exige bases de datos que conserven a los muertos, y en muchos casos no las tienes. Cuando no las
tienes, la conclusión honesta no es «mi backtest está corregido», sino «mi backtest es una cota
superior optimista y no sé de cuánto».

## Definición formal

Sea una cohorte de `N` miembros en el instante inicial `t0` y `r_i` la rentabilidad media anual
del miembro `i`. Sea `S` el conjunto de miembros que siguen existiendo en el instante `T`, con
`S = |S|` elementos. Lo que calculas con la base de datos es:

:::formula
media_observada = (1 / S) · Σ_{i ∈ S} r_i
:::

y lo que querías calcular era:

:::formula
media_real = (1 / N) · Σ_{i ∈ U₀} r_i
:::

- `N` — número de miembros en el universo inicial `U₀`: fondos, empresas, exchanges.
- `T` — instante final del estudio. Todo lo que ocurre entre `t0` y `T` decide quién llega.
- `S` — subconjunto de `U₀` que sigue vivo en `T`. Es la muestra que ves.
- `r_i` — rentabilidad media anual del miembro `i`, en tanto por uno.
- `p_i` — probabilidad de que el miembro `i` siga existiendo en `T`. Es una función
  **decreciente** de `r_i`: cuanto peor lo hace, más probable es que desaparezca.
- **Sesgo** = `media_observada − media_real`. Es positivo siempre que `p_i` decrezca con `r_i`,
  y su tamaño depende de lo fuerte que sea esa relación y de cuánta dispersión haya en `r_i`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `N` | Miembros del universo inicial `U₀`: fondos, empresas, exchanges | recuento | Con `N` mayor y la misma tasa de desaparición, el sesgo no baja: lo que lo mueve no es el tamaño, sino qué parte se queda |
| `S` | Miembros que siguen existiendo en `T`, la muestra que ves | recuento | Cuanto menor es `S` respecto a `N`, más selectiva es la muestra y más se infla `media_observada`: en el ejemplo, quedarse con el 60 % ya desplaza la media más de siete puntos |
| `T` | Instante final del estudio | fecha | Con `T` más lejano hay más tiempo para que desaparezcan los malos, así que la fracción que sobrevive baja y el sesgo crece |
| `r_i` | Rentabilidad media anual del miembro `i` | tanto por uno o % anual | Es lo que se intenta medir. Su dispersión manda: con todos los miembros parecidos, descontar a los malos apenas cambia la media |
| `p_i` | Probabilidad de que el miembro `i` siga existiendo en `T` | probabilidad (0 a 1) | No se puede estimar con los datos que tienes, porque los de `p_i` bajo son justo los que no aparecen. Cuanto más rápido caiga con `r_i`, mayor el sesgo |
| `media_observada − media_real` | El sesgo | puntos porcentuales al año | Es la corrección que no puedes calcular desde dentro de la muestra: solo la resuelven datos externos que conserven a los desaparecidos |
:::

El detalle que lo hace peligroso: `p_i` **no se puede estimar** con los datos que tienes, porque
los miembros con `p_i` bajo son precisamente los que no aparecen. No hay forma de calcular la
corrección desde dentro de la muestra; la corrección solo puede venir de datos externos que
conserven a los desaparecidos.

El backfill es la misma fórmula con otro índice temporal: el universo `U₀` que reconstruyes con
la base de datos de `T` contiene miembros que no existían en `t0`, así que `N` está inflado y
`S` está sesgado hacia los que decidieron reportar después de ganar.

## Ejemplo

Diez fondos arrancan el mismo año. Diez años después, seis siguen abiertos y cuatro se cerraron.
Estas son sus rentabilidades medias anuales, en porcentaje:

```
siguen abiertos:   8    6   10    4    7    9
cerraron:        -20  -12   -8  -15
```

- Media de los que siguen abiertos: (8 + 6 + 10 + 4 + 7 + 9) / 6 = 44 / 6 = **7,33 %**.
- Media de la cohorte completa: (44 − 55) / 10 = −11 / 10 = **−1,10 %**.
- Diferencia: **8,43 puntos porcentuales al año**, y con cambio de signo: la muestra viva dice
  «este sector gana dinero» y la cohorte entera decía «este sector pierde dinero».

Fíjate en que no hace falta ninguna estafa: basta con que la base de datos de la que tiras solo
tenga a los seis vivos. Nadie ha borrado nada; simplemente, los cuatro que cerraron ya no
reportan.

La versión de backfill es todavía más silenciosa. Imagina que un fondo con doce años de historia
empezó a reportar en su octavo año, justo después de encadenar dos años buenos. En la base de
datos aparece con doce años de rentabilidades, y tú lo cuentas como parte del universo desde el
primer día. Su primera etapa, la mala, entra en tus estadísticas sin haber estado nunca en tu
universo de decisión.

## Código

```python verificable
import numpy as np

vivos = np.array([8.0, 6.0, 10.0, 4.0, 7.0, 9.0])
muertos = np.array([-20.0, -12.0, -8.0, -15.0])
cohorte = np.concatenate([vivos, muertos])

print(f"media de los vivos   {vivos.mean():+.2f} %")        # -> +7.33 %
print(f"media de la cohorte  {cohorte.mean():+.2f} %")      # -> -1.10 %
print(f"sesgo                {vivos.mean() - cohorte.mean():+.2f} pp")  # -> +8.43 pp
print(f"fondos que faltan    {muertos.size} de {cohorte.size}")          # -> 4 de 10
```

:::claves
- `np.concatenate([vivos, muertos])` devuelve un array **nuevo**: los dos originales no se tocan.
  Si en vez de eso haces `vivos.append(...)` sobre un array de NumPy, no existe ese método con esa
  semántica: para añadir a un array se usa `np.append`, y además devuelve copia.
- `.mean()` sobre un array de NumPy siempre da `float`; no hay parámetro `ddof` que ajustar porque
  la media no lo necesita. Donde sí muerde es en `.std(ddof=1)`: NumPy usa `ddof=0` por defecto y
  pandas `1`, y esa diferencia es la que hace que dos desviaciones «iguales» no coincidan.
- `muertos.size` y `cohorte.size` son **enteros**; `vivos.mean()` es un `float`. La resta
  `vivos.mean() - cohorte.mean()` es float. Si en algún momento mezclas un array de `int` con una
  división (`/`), NumPy promociona a `float64` sin avisar, y eso cambia lo que imprime `:.2f`.
- La f-string `{vivos.mean():+.2f}` pone el signo **siempre**, también en los positivos: por eso
  sale `+7.33` y no `7.33`. Quitar el `+` cambia los tres números de golpe.
- El sesgo está calculado como `vivos.mean() - cohorte.mean()`, y **ese orden importa**: al revés
  sale el mismo número con el signo contrario, y el comentario `# -> +8.43 pp` dejaría de ser cierto.
- Este bloque es una resta de dos medias, no una corrección. Ninguna línea estima `p_i`: no se
  puede, porque los fondos con `p_i` bajo no están en `muertos`, simplemente no están.
:::

```python verificable
import numpy as np

# El mecanismo, no el caso concreto: la probabilidad de seguir vivo baja con el resultado.
rng = np.random.default_rng(0)
n = 2000
resultado = rng.normal(0.02, 0.15, size=n)          # rentabilidad real de cada fondo
# Supervivencia: cuanta peor es la rentabilidad, menos probable es seguir en la base de datos.
prob_vivir = 1.0 / (1.0 + np.exp(-(resultado + 0.02) / 0.05))
vive = rng.random(n) < prob_vivir

print(f"fondos simulados        {n}")                       # -> 2000
print(f"supervivientes          {int(vive.sum())}")          # -> 1178
print(f"media real              {resultado.mean():+.4f}")    # -> +0.0158
print(f"media de supervivientes {resultado[vive].mean():+.4f}")  # -> +0.1027
print(f"sesgo al alza           {resultado[vive].mean() - resultado.mean():+.4f}")  # -> +0.0869
```

## Errores típicos

- **Usar la lista de hoy para un backtest de ayer.** Comprar los componentes actuales de un
  índice y simular veinte años hacia atrás es seleccionar a los ganadores sabiendo quiénes
  ganaron. Si no tienes la composición histórica con fechas de entrada y salida, dilo.
- **Analizar «los fondos con diez años de historia» y llamarlo «el sector».** Esa frase describe
  a los supervivientes, no al sector. El sector incluye a los que se cerraron por el camino.
- **Tratar la ausencia de datos como ausencia de suceso.** Que una empresa no esté en tu CSV no
  significa que no existiera: significa que desapareció, y casi siempre por un mal motivo.
- **Ignorar el backfill.** Un fondo que entra en la base de datos hoy con su historial completo
  contamina todas tus medias hacia atrás. La solución es usar solo las observaciones que
  existían en cada fecha, no el fichero final.
- **Creer que este sesgo no afecta a mercados jóvenes.** En cripto, los exchanges que quebraron
  no están en los datasets de precios, y los tokens muertos desaparecen de los listados. La
  lista de pares que cotizan hoy es una lista de supervivientes.
- **Confundirlo con [[sesgo-de-mirar-al-futuro]] y creer que corregir uno corrige el otro.** Son
  fugas distintas: la de información (una variable que no existía el día de la decisión) y la de
  selección (un universo que no existía el día de la decisión). Puedes tener las dos, una o
  ninguna, y se arreglan por separado.

:::practica
enunciado: Doce fondos arrancan el mismo año. Diez años después siguen siete, con rentabilidades medias anuales del 10, 6, 12, 4, 8, 14 y 2 %; los cinco que cerraron dieron −25, −15, −12, −10 y −6 %. Calcula la media que ve la base de datos, la real y el sesgo.
pista: La base de datos solo contiene a los siete vivos; la media real usa los doce, incluidos los que cerraron.
solucion: Vivos: (10 + 6 + 12 + 4 + 8 + 14 + 2) / 7 = 56 / 7 = 8,00 %. Cohorte completa: (56 − 68) / 12 = −12 / 12 = −1,00 %. El sesgo es 8,00 − (−1,00) = 9,00 puntos porcentuales al año, y cambia el signo: la muestra viva dice que el sector gana y la cohorte entera, que pierde. Han desaparecido 5 de 12 fondos, un 42 %.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la rentabilidad media de los fondos que siguen abiertos hoy está sesgada al alza?
o: Porque los fondos que van mal tienden a cerrarse o dejar de reportar, así que desaparecen de la muestra
o: Porque las gestoras inflan los datos de rentabilidad que publican
o: Porque los fondos buenos cobran comisiones más bajas
a: 1
e: La muestra se selecciona sola por el resultado: la probabilidad de seguir existiendo disminuye cuando la rentabilidad es mala. Los datos publicados pueden tener otros errores, pero el sesgo de supervivencia no necesita ninguna mentira: basta con que los malos no estén. Las comisiones afectan a la rentabilidad neta, no a la composición de la muestra.
:::

:::quiz
p: Un fondo con doce años de historia entra en tu base de datos en su octavo año, tras dos años buenos. ¿Qué problema introduce?
o: Sesgo de backfill: incluyes hacia atrás un fondo que no estaba en el universo de entonces, y encima suele llegar después de haber ganado
o: Ninguno, porque los doce años de rentabilidad son datos reales
o: Solo un problema de duplicados si el fondo cambió de nombre
a: 1
e: Que el dato sea real no lo convierte en parte del universo que estás reconstruyendo. El fondo decide reportar cuando le interesa, y ese momento correlaciona con su rendimiento reciente: los años malos de arranque entran en tus medias sin haber estado nunca en tu conjunto de decisión. Es un sesgo de selección, no de calidad del dato.
:::

:::trampa
Un backtest de un universo de acciones que da un rendimiento excelente suele tener, antes o
después, esta comprobación pendiente: ¿cuántas de las empresas de tu lista quebraron, fueron
absorbidas o salieron del índice durante el periodo? Si no lo sabes, tu resultado es una cota
superior. Y cuanto más largo es el periodo y más pequeño el universo, más grande es la cota.
:::
