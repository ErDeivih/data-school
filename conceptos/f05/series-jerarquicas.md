---
id: series-jerarquicas
titulo: Series jerárquicas y reconciliación
fase: 5
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, suavizado-exponencial, validacion-temporal]
tags: [series-temporales, pronostico, agregacion]
resumen: Predecir por separado el total, las tiendas y los productos da cifras que no suman; la reconciliación reparte el desajuste.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 11", "Wickramasuriya, Athanasopoulos y Hyndman (2019), 'Optimal forecast reconciliation for hierarchical and grouped time series'"]
---

## En una frase

Una serie jerárquica tiene varios niveles que se suman entre sí —país, tienda, producto—, y
reconciliar es ajustar los pronósticos de todos los niveles para que al sumarlos den exactamente
el total.

## La idea

Imagina una empresa de alimentación con dos tiendas. La directora comercial presupuesta el año por
país consultando a quien conoce el mercado nacional; cada jefe de tienda presupuesta lo suyo
mirando su histórico local; y el responsable de categoría hace lo propio producto a producto. Los
tres usan modelos distintos, con datos distintos y agregados en momentos distintos. El resultado es
que la suma de las dos tiendas da 1.240 miles de euros y el presupuesto nacional dice 1.200. Alguien
tiene que cuadrar esa diferencia a mano, en una hoja de cálculo, un viernes por la tarde.

Ese desajuste no es un error de nadie: es lo que pasa cuando pronosticas cada nivel por separado.
Y el problema tiene dos caras. Por un lado, la incoherencia es un problema de negocio: si producción
planifica con 1.240 y finanzas con 1.200, una de las dos decisiones es mala. Por otro, **la
incoherencia contiene información**: el nivel superior ve cosas que el inferior no (una campaña
nacional, un cambio de precio global) y el inferior ve cosas que el superior no (la competencia
que acaba de abrir en esa calle). En vez de tirar una de las dos versiones, se combinan.

Tres formas de hacerlo, de menos a más sofisticada:

1. **De abajo arriba (bottom-up).** Pronostica solo el nivel más fino y suma. Coherente por
   construcción y conserva el detalle, pero es el nivel con más ruido y más series: si tienes
   40.000 combinaciones producto-tienda, cada una con poco histórico, el error se acumula.
2. **De arriba abajo (top-down).** Pronostica el total y repártelo con las proporciones
   históricas de cada serie. Estable frente al ruido, pero las proporciones se congelan: si una
   tienda nueva crece al 30 % anual, seguirá recibiendo su cuota vieja.
3. **Reconciliación óptima.** Pronostica **todos** los niveles, mide con qué precisión acierta
   cada uno y reparte la corrección dando más peso a los niveles que históricamente aciertan más.
   Es la que usa la gente que se toma esto en serio, y en la práctica casi siempre gana a las dos
   anteriores.

El detalle importante es que reconciliar **cambia las predicciones, no solo las escalas**. El
número final del nivel nacional deja de ser el que dio su modelo y pasa a ser una mezcla ponderada
de lo que dijeron todos los niveles.

## Definición formal

Con `n` series en total (los nodos del árbol), el vector de pronósticos base es `ŷ`. La jerarquía
se escribe con una matriz de suma `S` que dice qué suma a qué:

:::formula
ŷ_reconciliado = S · (Sᵀ W⁻¹ S)⁻¹ Sᵀ W⁻¹ · ŷ = S · P · ŷ
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Número de series de la jerarquía (todos los niveles) | series | Más filas y columnas: la matriz crece al cuadrado |
| `m` | Número de series del nivel más fino (la base del árbol) | series | Más detalle, más ruido por serie y más coste de cómputo |
| `ŷ` | Vector de pronósticos base, uno por serie, cada uno de su modelo | las de la serie | Es la entrada: cuanto peor sea, peor sale la reconciliación |
| `S` | Matriz de suma (`n × m`): cada columna dice qué nodos agrega esa serie de base | 0 o 1 | No «sube»: si cambia el árbol, cambia `S` entera |
| `W` | Matriz de covarianzas de los errores de pronóstico de los `n` niveles | al cuadrado | Más peso para los niveles con más error: la corrección se aleja de ellos |
| `P` | Matriz de proyección: `(Sᵀ W⁻¹ S)⁻¹ Sᵀ W⁻¹`, de tamaño `m × n` | adimensional | — |
| `β` | Los `m` valores del nivel base ya reconciliados | las de la serie | — |
:::

Dos casos particulares que conviene reconocer:

- Si `W` es la identidad (todos los niveles igual de fiables), la proyección `P` es la de mínimos
  cuadrados ordinarios: reparte la corrección minimizando la suma de cuadrados de los ajustes.
- Si `W` es diagonal con la varianza de cada nivel, cada nivel se corrige en proporción a su
  fiabilidad: los niveles ruidosos se mueven mucho, los estables casi nada.

En la práctica `W` no se conoce y se estima con los residuos del histórico. La variante que usa
`W` estimada a partir de los residuos se llama **MinT** (*minimum trace*) y es la opción por
defecto en las librerías serias.

La **coherencia** se comprueba siempre igual: aplica `S` a tu vector final y compara con el nivel
superior. Si `S · ŷ_final` no reproduce exactamente los nodos agregados, la reconciliación no se
ha aplicado.

:::figura
fichero: series-jerarquicas-niveles-y-reconciliacion
pie: A la izquierda, los pronósticos base de dos tiendas suman 1.240 mientras el modelo nacional dice 1.200: los dos modelos son razonables y el descuadre es de 40. A la derecha, tras reconciliar, el nacional se queda como estaba y son las tiendas las que absorben el ajuste; la grande se lleva más corrección porque el reparto es proporcional.
fuente: figuras/series-jerarquicas-1.py
:::

## Ejemplo

Dos tiendas y un total nacional. Los modelos base dicen:

- Tienda A: **720** miles de euros.
- Tienda B: **520** miles.
- Total nacional (su propio modelo): **1.200** miles.

La suma de las tiendas es 1.240, que no cuadra. Reconciliación **proporcional al pronóstico base**
(la versión más simple de de-arriba-abajo):

- Peso de A: 720 / 1.240 = 0,5806. Peso de B: 520 / 1.240 = 0,4194.
- A corregida: 1.200 · 0,5806 = **696,8**.
- B corregida: 1.200 · 0,4194 = **503,2**.
- Comprobación: 696,8 + 503,2 = 1.200. Cuadra.

Fíjate en lo que ha pasado: A baja 23,2 y B baja 16,8. La corrección se ha repartido en
proporción al tamaño, así que la tienda grande absorbe más del ajuste. Eso es una decisión, no una
ley: si supieras que el modelo de B es mucho peor que el de A, querrías que B absorbiera casi todo
el ajuste. Eso es exactamente lo que hace `W` en la fórmula de arriba.

## Código

```python verificable
import numpy as np

# Serie mensual de dos tiendas y del total, para la que solo tenemos el pronostico,
# no el dato real. Lo que se comprueba aqui es la aritmetica de la reconciliacion.
base = np.array([1200.0, 720.0, 520.0])          # [total, tienda A, tienda B]
S = np.array([[1.0, 1.0],                        # el total es A + B
              [1.0, 0.0],
              [0.0, 1.0]])

print(f"suma de las tiendas {base[1] + base[2]:.1f}   total declarado {base[0]:.1f}")  # -> 1240.0 y 1200.0

# Reconciliacion proporcional: reparte el total segun el peso de cada tienda en la base
peso = base[1:] / base[1:].sum()
reconciliado = S @ (peso * base[0])
print(f"pesos {np.round(peso, 4)}")               # -> [0.5806 0.4194]
print(f"reconciliado {np.round(reconciliado, 1)}")  # -> [1200.  696.8 503.2]
print(f"desajuste tras cuadrar {base[1] + base[2] - base[0]:.1f} -> pendiente")  # -> 40.0
print(f"suma final {reconciliado[1] + reconciliado[2]:.1f}")  # -> 1200.0
```

:::claves
- `base[1:]` es una **vista**, no una copia: si escribieras dentro de ella (`base[1:][0] = 1`), cambiarías `base` también. `peso`, en cambio, es un array **nuevo**, porque la división `base[1:] / base[1:].sum()` copia: escribir en `peso` no toca `base`.
- La `@` es multiplicación de matrices, no producto elemento a elemento. `base[1:] * base[0]` sería otra cosa (multiplicaría cada tienda por el total); para multiplicar elemento a elemento en NumPy se usa `*`, y para matrices `@`.
- `S @ (peso * base[0])` funciona porque `S` es de 3×2 y el vector de dentro tiene 2 elementos: el resultado son las tres series (total, A, B) ya coherentes. Si el nivel base tuviera 3 tiendas, `S` tendría que ser 4×3.
- `np.round(peso, 4)` **devuelve un array nuevo**: no redondea `peso` en el sitio. Con `peso.round(4)` pasa lo mismo (devuelve copia); solo `peso.round(4, out=peso)` modificaría el original.
- Los pesos suman 1 por construcción (`base[1:].sum()` es el denominador). Si añades una tercera tienda con pronóstico 0, su peso es 0 y se queda fuera de todo el reparto: la reconciliación no puede «inventar» ventas donde el modelo base no las ve.
- Truco de dibujo que muerde: en matplotlib, `numeros(ax)` fija el formato de los ejes y **borra las etiquetas de texto** que hayas puesto antes (`ax.set_xticks([0, 1], ["tienda A", "tienda B"])` se convierte en «0» y «1»). Si el eje lleva nombres y no cifras, vuelve a fijar las etiquetas *después* de `numeros(ax)`, o formatea solo el eje vertical.
:::

## Errores típicos

- **Reconciliar solo el nivel donde duele.** Cuadrar el total nacional y dejar las tiendas
  descuadradas mueve el problema un piso más abajo: el almacén sigue comprando con un número que
  no existe.
- **Usar el histórico para calcular los pesos de reparto sin ventana temporal.** Si calculas la
  cuota de cada tienda con todo el histórico, una tienda que abrió hace seis meses sale con una
  cuota ridícula para siempre. Los pesos se estiman con una ventana reciente, igual que cualquier
  otra cosa en [[validacion-temporal|validación temporal]].
- **Reconciliar y luego medir el error contra el dato original con la misma métrica que antes.** La
  reconciliación mueve todas las predicciones, así que sube el error de algunos niveles y baja el
  de otros. Lo que mejora es el error **agregado y jerárquico**, y hay que medirlo así
  ([[metricas-de-regresion]]).
- **Confundir reconciliación con reparto de la diferencia.** Restar el desajuste a partes iguales
  entre todas las series es una reconciliación, sí, pero la peor posible: ignora por completo qué
  modelo es más fiable en cada nivel.
- **Olvidar las jerarquías cruzadas.** Si la jerarquía es producto × tienda × canal, un producto
  puede descomponerse de dos formas a la vez (por canal o por tienda). Las dos restricciones se
  meten en la misma `S`; reconciliar solo una deja la otra rota.
- **Creer que más niveles siempre es mejor.** Cada nivel añade series y parámetros a `W`. Con
  jerarquías muy anchas y poco histórico, estimar `W` es tan ruidoso que la reconciliación óptima
  pierde frente a la de abajo arriba. Empieza por la versión simple.

:::practica
enunciado: Tienes los pronósticos base para el total nacional (2.000), la tienda A (1.100) y la tienda B (1.050). Reconcilia de arriba abajo repartiendo el total en proporción al pronóstico base de cada tienda, y di qué tienda absorbe más ajuste y por qué.
pista: El peso de cada tienda es su pronóstico base dividido entre la suma de ambos pronósticos base.
solucion: La suma base es 1.100 + 1.050 = 2.150. El peso de A es 1.100 / 2.150 = 0,5116 y el de B es 1.050 / 2.150 = 0,4884. Con el total reconciliado: A recibe 2.000 · 0,5116 = 1.023,3 y B recibe 2.000 · 0,4884 = 976,7. Comprobación: 1.023,3 + 976,7 = 2.000. El ajuste total es 2.150 − 2.000 = 150, y A absorbe 76,7 frente a los 73,3 de B: absorbe más porque su pronóstico base es mayor. Con reconciliación óptima, si el modelo de B tuviera mucho más error histórico que el de A, B absorbería casi todo el ajuste.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué garantiza exactamente la reconciliación de una serie jerárquica?
o: Que el pronóstico de cada nivel sea más preciso que el del nivel de al lado
o: Que al sumar los niveles inferiores se reproduzca exactamente el valor del nivel agregado
o: Que todos los niveles usen el mismo modelo y las mismas variables
a: 2
e: La reconciliación es una restricción aritmética: los números cuadran. La precisión suele mejorar de rebote, sobre todo en los niveles altos, pero no está garantizada para un nivel concreto; y no obliga a usar un solo modelo, precisamente lo contrario: parte de que cada nivel tiene su propio pronóstico base.
:::

:::quiz
p: Pronosticas de abajo arriba 40.000 combinaciones producto-tienda y sumas. ¿Cuál es el principal riesgo?
o: Que la suma sea incoherente con el nivel nacional
o: Que el ruido de 40.000 series con poco histórico se acumule y el total sea peor que el de un modelo nacional
o: Que la matriz de proyección P no exista
a: 2
e: De abajo arriba la coherencia está garantizada por construcción: sumas y ya cuadra. El problema es el error. Cada serie base tiene poco histórico y mucho ruido; al sumarlas, los sesgos se suman y el total puede quedar peor que un modelo entrenado directamente sobre el total. Por eso la reconciliación óptima usa los dos.
:::

:::quiz
p: ¿Qué papel juega la matriz W en la reconciliación óptima?
o: Decide cuánto se corrige cada nivel según la fiabilidad de su pronóstico base
o: Es la matriz que define qué series suman a cuáles
o: Sirve para reordenar las series de menor a mayor
a: 1
e: La estructura de la jerarquía está en la matriz de suma S, con ceros y unos. W es la matriz de covarianzas de los errores: los niveles con más error reciben correcciones mayores, y los que aciertan más apenas se mueven. Confundir S con W es el malentendido más común de esta fórmula.
:::

:::trampa
La reconciliación reparte el desajuste, no lo elimina. Si tu modelo nacional va 40 miles por encima de la suma de las tiendas, después de reconciliar seguirás teniendo un error de 40 respecto a la realidad; solo que ahora el error está repartido y todas las áreas de la empresa usan la misma cifra. Reconciliar arregla la coherencia, no la precisión.
:::
