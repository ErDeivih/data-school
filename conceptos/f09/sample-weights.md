---
id: sample-weights
titulo: Pesos de muestra
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [triple-barrera, validacion-cruzada, autocorrelacion-acf-pacf]
tags: [etiquetado, pesos, lopez-de-prado, solapamiento]
resumen: Con etiquetas que se solapan, varias observaciones cuentan la misma información: pesarlas por su unicidad evita que el modelo cuente el mismo tramo varias veces.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 4"]
---

## En una frase

Si dos operaciones comparten días de mercado, no son dos observaciones independientes: el peso
por **unicidad** mide cuánta información exclusiva aporta cada una y reparte el peso para que
cada tramo de precios cuente una sola vez.

## La idea

Imagina una encuesta en la que la misma persona vota cinco veces porque pasa por la mesa cinco
veces. El recuento es incorrecto, y no por maldad de nadie: el procedimiento no impide que un
mismo dato entre varias veces. En el etiquetado financiero pasa exactamente eso.

Con [[triple-barrera|etiquetas de triple barrera]], cada operación ocupa un intervalo de barras.
Si lanzas 100 operaciones con `h = 20` barras sobre 300 barras de histórico, en cualquier momento
hay unas siete operaciones vivas a la vez. Las 100 observaciones no son 100 trozos de mercado
distintos: son 300 barras contadas siete veces de media. El modelo ve el mismo día siete veces, y
como consecuencia:

- **Sobrepondera los periodos con muchas operaciones abiertas.** Y esos periodos no son
  aleatorios: suelen ser los de volatilidad alta, cuando las señales se disparan. El modelo
  aprende de la crisis mucho más de lo que la crisis pesa en el histórico.
- **Reporta una confianza falsa.** Con 100 filas, la fórmula habitual del error típico diría que
  tienes 100 observaciones. En realidad tienes muchas menos, así que los intervalos de confianza
  son más estrechos de lo que deberían y las diferencias parecen más sólidas.
- **Rompe el supuesto de independencia** en el que se apoyan el [[validacion-cruzada|K-fold]] y
  casi cualquier contraste.

La solución es tan simple como razonable: en lugar de contar cada observación como 1, cuenta cada
observación por lo que aporta de exclusiva. Una etiqueta que vive sola en su tramo de mercado vale
1; una que comparte todos sus días con otras cinco vale aproximadamente 1/6. Después se
normaliza para que la suma de pesos siga siendo el número de observaciones y no cambie la escala
de la función de pérdida.

Este peso se puede multiplicar por otros dos que suelen hacer falta:

- **Decaimiento temporal:** en finanzas, el mercado de hace ocho años se parece poco al de hoy.
  Un peso lineal que baja de 1 en la observación más reciente a casi 0 en la más antigua evita
  que el modelo viva del pasado remoto. El precio es que el modelo se adapta más rápido y también
  olvida más rápido.
- **Equilibrio de clases:** si la clase `−1` es el 20 % de las observaciones, dividir el peso de
  cada clase por su frecuencia total (y reescalar) hace que las tres clases pesen lo mismo sin
  duplicar ni borrar filas. Es la alternativa a `class_weight` cuando ya tienes pesos puestos.

:::nota
Los pesos arreglan la *redundancia* (cuántas veces cuenta cada tramo), no la *dependencia en la
validación*. Un conjunto de validación que solapa con el de entrenamiento sigue estando mal aunque
uses pesos perfectos: para eso está [[purged-kfold|la purga con embargo]].
:::

## Definición formal

Sean `n` observaciones, cada una con su intervalo de vida `[t0ᵢ, t1ᵢ)` medido en barras, y sea
`1{·}` la función indicadora (vale 1 si la condición se cumple y 0 si no).

:::formula
c_t = Σᵢ 1{ t ∈ [t0ᵢ, t1ᵢ) }        ūᵢ = (1 / mᵢ) · Σ_{t ∈ Tᵢ} 1 / c_t
:::

- `c_t` — **concurrencia** en la barra `t`: cuántas etiquetas están vivas en ese instante.
- `Tᵢ` — el conjunto de barras que ocupa la observación `i`, y `mᵢ` su número de barras.
- `ūᵢ` — **unicidad media** de la observación `i`: la media de `1 / c_t` a lo largo de su vida.
  Está siempre entre 0 y 1, y vale 1 solo si la etiqueta nunca coincidió con otra.

El peso final se normaliza para que su suma sea `n`:

:::formula
wᵢ = ūᵢ · n / Σⱼ ūⱼ        Σᵢ wᵢ = n
:::

- `wᵢ` — el peso que se pasa al modelo (`sample_weight` en scikit-learn, `weight` en LightGBM).
- `n` — número de observaciones; sin este factor, los pesos redimensionarían la pérdida y
  cambiarían el efecto de la regularización.
- `Σᵢ ūᵢ` — la **información efectiva** de la muestra: cuántas observaciones independientes
  equivalen a tus `n` filas solapadas. Es un número que conviene mirar siempre; si sale mucho
  menor que `n`, tu muestra es más pequeña de lo que crees.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `c_t` | La concurrencia: cuántas etiquetas están vivas en la barra `t` | número de etiquetas | Sube cuando las operaciones duran más o se disparan juntas, y cada etiqueta pasa a pesar menos |
| `Tᵢ` | El conjunto de barras que ocupa la observación `i` | barras | No se elige a mano: lo fija el horizonte de la etiqueta |
| `mᵢ` | Cuántas barras dura la observación `i` | barras | Un horizonte más largo reparte el peso entre más barras y baja la unicidad de todas |
| `ūᵢ` | La unicidad media de la observación `i` | entre 0 y 1 | Vale 1 si la etiqueta vive sola; baja hacia `1/c` cuando comparte barras, y nunca puede pasar de 1 |
| `wᵢ` | El peso que se pasa al modelo (`sample_weight`, `weight`) | adimensional | Con decaimiento y equilibrio de clases el máximo puede quedar 30 veces por encima del mínimo: mira la distribución antes de entrenar |
| `n` | El número de observaciones | filas | Sin este factor en la normalización los pesos suman 1 y la regularización pesa distinto: cambia el modelo, no solo la escala |
| `Σⱼ ūⱼ` | La información efectiva de la muestra | observaciones equivalentes | Si sale muy por debajo de `n`, tienes menos muestra de la que crees (2.000 operaciones con unicidad media 0,15 son unas 300) |
:::

Con decaimiento temporal y equilibrio de clases, el peso compuesto es el producto de los tres
factores, renormalizado al final. El orden da igual; lo que no da igual es no documentarlo.

:::figura
fichero: pesos-unicidad-solapamiento
pie: Cada barra azul es la vida de una etiqueta sobre el mismo calendario de barras, con su unicidad media y su peso final. Abajo, la concurrencia: donde la línea llega a 5, esa barra de precios entra cinco veces en el modelo, y cada etiqueta solo cobra 1/5 por ella. La suma de unicidades, 2,24, es la información efectiva: seis filas valen menos de lo que valdrían dos observaciones y media independientes.
fuente: figuras/sample-weights-1.py
:::

## Ejemplo

Cuatro etiquetas sobre 12 barras: `A` ocupa las barras 0 a 4, `B` las barras 2 a 6, `C` las
barras 6 a 8 y `D` las barras 8 a 11. La concurrencia por barra es:

```
barra        0  1  2  3  4  5  6  7  8  9 10 11
c_t          1  1  2  2  2  1  2  1  2  1  1  1
```

El detalle del cálculo y los pesos:

| Etiqueta | Barras | Concurrencia en sus barras | Unicidad |
| --- | --- | --- | --- |
| A | 0 a 4 | 1, 1, 2, 2, 2 | 0,700 |
| B | 2 a 6 | 2, 2, 2, 1, 2 | 0,600 |
| C | 6 a 8 | 2, 1, 2 | 0,667 |
| D | 8 a 11 | 2, 1, 1, 1 | 0,875 |

- Para `A`: `ū = (1/1 + 1/1 + 1/2 + 1/2 + 1/2) / 5 = 3,5 / 5 = 0,700`.
- Para `B`: `ū = (1/2 + 1/2 + 1/2 + 1/1 + 1/2) / 5 = 3,0 / 5 = 0,600`.
- Suma de unicidades: 2,842. Esa es la información efectiva: las cuatro etiquetas valen menos que
  tres observaciones independientes.
- Pesos normalizados: `A = 0,700 · 4 / 2,842 = 0,985`, `B = 0,845`, `C = 0,938`, `D = 1,232`.
  Suman 4, así que la escala de la pérdida no cambia.

La lectura es clara: `D` vive tres de sus cuatro barras sin compañía y pesa un 23 % más que una
observación media; `B` comparte cuatro de sus cinco barras y pesa un 15 % menos. La diferencia no
es enorme porque el solapamiento tampoco lo es; con operaciones largas y frecuentes la horquilla
se dispara.

## Código

```python verificable
import numpy as np

t0 = np.array([0, 2, 6, 8])
t1 = np.array([5, 7, 9, 12])
n_barras = 12

# Concurrencia: cuantas etiquetas estan vivas en cada barra.
concurrencia = np.zeros(n_barras, dtype=int)
for a, b in zip(t0, t1):
    concurrencia[a:b] += 1
print("concurrencia por barra:", concurrencia.tolist())
# -> [1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1]

# Unicidad: media de 1/concurrencia a lo largo de la vida de cada etiqueta.
unicidad = np.array([np.mean(1.0 / concurrencia[a:b]) for a, b in zip(t0, t1)])
print("unicidad:", np.round(unicidad, 3).tolist())        # -> [0.7, 0.6, 0.667, 0.875]

# Se normaliza para que la suma de pesos siga siendo el numero de observaciones.
pesos = unicidad / unicidad.sum() * unicidad.size
print("pesos normalizados:", np.round(pesos, 3).tolist())  # -> [0.985, 0.845, 0.938, 1.232]
```

:::claves
- `concurrencia[a:b] += 1` funciona porque el corte de un array es una **vista**, no una copia: el trozo comparte memoria con `concurrencia` y el `+=` escribe dentro del array original. Con `concurrencia[a:b].copy()` el sumando se perdería en el aire y el conteo saldría todo a cero.
- El corte `a:b` **excluye** la barra `b`. Una etiqueta `[0, 5)` ocupa cinco barras, de la 0 a la 4, que es el mismo convenio con el que se construyen las etiquetas de [[triple-barrera|triple barrera]]. Cambiarlo por `a:b+1` añadiría una barra a cada etiqueta y la última se saldría del array.
- `np.zeros(n_barras, dtype=int)` fija el tipo: sin `dtype` el array sería de coma flotante y el conteo saldría como `1.0, 2.0`. Luego se compara e imprime sin avisar, así que el tipo se elige al crear el array, no después.
- `zip(t0, t1)` recorre las dos listas en paralelo y **se detiene en la más corta**. Si una lista tuviera un elemento de menos, la última etiqueta se procesaría con un final equivocado o no se procesaría, sin ningún error. La comprobación es una línea: `assert len(t0) == len(t1)`.
- `1.0 / concurrencia[a:b]` divide un número entre un array y devuelve un array de la misma forma; `np.mean` de ese array es la media de `1/c` a lo largo de toda la vida de la etiqueta. Con un trozo vacío (`a == b`) `np.mean` devuelve `nan` y un aviso, no una excepción.
- La normalización `unicidad / unicidad.sum() * unicidad.size` es la que deja `pesos.sum() == 4`. Si se omite el `* unicidad.size`, los pesos suman 1 y la pérdida cambia de escala, con lo que la regularización pesa lo que no debe y la comparación entre modelos deja de ser limpia. `np.round` no toca el array: devuelve uno nuevo.
:::

```python verificable
import numpy as np

# Cuanto baja la informacion efectiva al alargar las etiquetas: 100 eventos en 300 barras.
rng = np.random.default_rng(0)
n = 300
inicios = np.sort(rng.choice(n, size=100, replace=False))

print("largo  unicidad media  n efectivo")
for largo in (1, 5, 20):
    concurrencia = np.zeros(n)
    for a in inicios:
        concurrencia[a:min(a + largo, n)] += 1
    unicidad = np.array([np.mean(1.0 / concurrencia[a:min(a + largo, n)])
                         for a in inicios if min(a + largo, n) > a])
    print(f"{largo:>5}  {unicidad.mean():>14.3f}  {unicidad.sum():>10.1f}")
# con etiquetas de 20 barras, 100 operaciones valen como 15 independientes
```

## Errores típicos

- **Entrenar con pesos 1 y luego sorprenderse de que la validación cruzada dé resultados
  inestables.** Con etiquetas solapadas, el modelo repite información; los pesos son la parte
  fácil de arreglar. Si no los usas, al menos mide la unicidad media para saber cuánta muestra
  real tienes.
- **Normalizar los pesos de cualquier manera.** Si la suma no es `n`, el término de regularización
  pesa relativamente más (o menos) y la comparación entre modelos ajustados con y sin pesos deja
  de ser limpia. Normaliza siempre y escribe en el informe la suma antes y después.
- **Aplicar los pesos solo al ajuste.** Si mides la precisión o el área bajo la curva sobre el
  conjunto de validación contando cada fila como 1, estás premiando al modelo que acierta en las
  zonas de mucho solapamiento. Usa las mismas ponderaciones al medir, o mide sobre un conjunto
  purgado.
- **Confundir unicidad con importancia.** La unicidad mide redundancia, no relevancia. Una
  observación única pero ruidosa pesará 1, y una observación informativa rodeada de otras
  parecidas pesará 0,4. No es un sistema de importancia de variables ni de calidad de etiqueta.
- **Multiplicar pesos sin mirar el rango final.** Unicidad por decaimiento por equilibrio de clases
  puede dejar el peso máximo 30 veces por encima del mínimo. En ese caso el modelo se ajusta a
  cuatro filas y el resto es decorado. Mira la distribución de `w` antes de entrenar.
- **Creer que los pesos sustituyen a la purga.** Son problemas distintos: la unicidad corrige
  cuántas veces cuenta cada tramo durante el ajuste; la purga evita que el conjunto de prueba
  comparta información con el de entrenamiento. Necesitas las dos cosas.

:::practica
enunciado: Tres etiquetas sobre siete barras: A ocupa las barras 0 a 3, B las 1 a 5 y C las 3 a 6. Calcula la concurrencia por barra, la unicidad media de cada etiqueta y los pesos normalizados para que sumen 3.
pista: La concurrencia cuenta las etiquetas vivas por barra; la unicidad es la media de 1/c en la vida de la etiqueta; se normaliza con n entre la suma de unicidades.
solucion: Concurrencia por barra: 1, 2, 2, 3, 2, 2, 1. Unicidad: A = (1 + 0,5 + 0,5 + 0,333)/4 = 0,583; B = (0,5 + 0,5 + 0,333 + 0,5 + 0,5)/5 = 0,467; C = (0,333 + 0,5 + 0,5 + 1)/4 = 0,583. La suma, 1,633, es la información efectiva: tres etiquetas valen menos que dos. Pesos = unicidad · 3 / 1,633: A y C 1,071, B 0,857, y suman 3.
:::

## Comprueba que lo sabes

:::quiz
p: Dos etiquetas duran lo mismo. La primera comparte todos sus días con otras cinco etiquetas; la segunda vive sola. ¿Qué unicidad tienen aproximadamente?
o: Las dos 1, porque la unicidad no depende de las demás etiquetas
o: La primera alrededor de 1/6 y la segunda 1
o: La primera 6 y la segunda 1, porque hay que contar cuántas la acompañan
a: 2
e: La unicidad es la media de 1 partido por la concurrencia a lo largo de la vida de la etiqueta. Si siempre hay 6 etiquetas vivas a la vez, cada barra aporta 1/6 y la unicidad media es 1/6. Una etiqueta que nunca coincide con otra tiene concurrencia 1 en todas sus barras, así que su unicidad es 1. Nunca puede pasar de 1.
:::

:::quiz
p: En el ejemplo, la suma de las unicidades es 2,842 con cuatro etiquetas. ¿Qué significa ese número y para qué sirve?
o: Es el número de observaciones que hay que borrar para que la muestra sea independiente
o: Es la información efectiva: cuatro etiquetas solapadas aportan lo que aportarían menos de tres observaciones independientes
o: Es el peso medio que hay que dar a cada etiqueta, que en este caso es 0,71
a: 2
e: La suma de unicidades es la cantidad de información no redundante de la muestra. Sirve para saber cuánta muestra real tienes y para interpretar los errores típicos: con 2,842 en lugar de 4, la incertidumbre es mayor de lo que sugiere el número de filas. El peso medio ya normalizado es siempre 1, porque los pesos se reescalan para sumar n.
:::

:::trampa
Si tu backtest tiene 2.000 operaciones y la unicidad media sale 0,15, no tienes 2.000
observaciones: tienes unas 300. Cualquier intervalo de confianza calculado sobre 2.000 estará
entre dos y tres veces más ajustado de lo que debería, y eso sin contar el solapamiento del
conjunto de prueba.
:::
