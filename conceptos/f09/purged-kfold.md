---
id: purged-kfold
titulo: K-fold con purga y embargo
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [validacion-cruzada, triple-barrera, autocorrelacion-acf-pacf, fuga-de-datos]
tags: [validacion, backtest, lopez-de-prado, series-temporales]
resumen: Validación cruzada adaptada a etiquetas que solapan en el tiempo: quita del entrenamiento todo lo que toca al conjunto de prueba y deja un margen de embargo.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', caps. 7 y 12"]
---

## En una frase

La validación cruzada normal mezcla el futuro con el pasado; la purga elimina del
entrenamiento todas las observaciones cuya etiqueta se solapa en el tiempo con el conjunto de
prueba, y el embargo elimina además las que van justo después, porque sus variables todavía
contienen información del periodo de prueba.

## La idea

En un problema de machine learning de manual, cada fila es independiente: saber el precio de
la vivienda A no te dice nada de la vivienda B, y por eso puedes barajar las filas y hacer
K-fold tranquilamente.

En finanzas no ocurre eso. Dos motivos concretos:

1. **Las etiquetas solapan.** Si marcas una operación con [[triple-barrera|triple barrera]]
   empezando el 1 de marzo y su barrera temporal es 20 días, esa etiqueta no se cierra hasta
   el 21 de marzo. Si otra operación empieza el 10 de marzo, las dos etiquetas comparten 11
   días de precios. Son observaciones que se pisan. Si una cae en entrenamiento y la otra en
   prueba, el modelo está viendo en parte el mismo tramo de mercado que luego se le pide
   predecir: no está generalizando, está recordando.
2. **Las variables tienen memoria.** Aunque las etiquetas no solaparan, indicadores como una
   media móvil de 50 días del 22 de marzo contienen los precios del 1 al 21 de marzo. Un
   periodo de prueba que empieza justo después del entrenamiento comparte información a
   través de esas ventanas. Ese residuo se corta dejando un hueco: el **embargo**.

Por eso el esquema es: se divide el tiempo en pliegues consecutivos (no barajados), y para
cada pliegue de prueba se **purga** del entrenamiento todo lo que solape con él y se
**embarga** un tramo posterior. El resultado es una estimación más pesimista y mucho más
honesta: sigue siendo validación cruzada, pero con las fugas cerradas.

El precio es que se pierden datos de entrenamiento (típicamente entre un 10 % y un 40 % según
el horizonte de las etiquetas). Es un precio que se paga a gusto: un modelo con menos datos y
una estimación verdadera vale más que uno con todos los datos y una estimación inflada.

## Definición formal

Sean `N` observaciones etiquetadas, cada una con su intervalo temporal `[t0ᵢ, t1ᵢ)`: `t0ᵢ` es
el instante en que la observación empieza a formarse y `t1ᵢ` el instante en que su etiqueta
queda determinada. Sean `k` pliegues consecutivos.

Para el pliegue de prueba `j`, con `T_j = [min t0ᵢ , max t1ᵢ)` sobre las observaciones del
pliegue:

- **Conjunto de prueba:** las observaciones del pliegue `j`.
- **Purga:** se eliminan del entrenamiento todas las observaciones `i` con
  `[t0ᵢ, t1ᵢ) ∩ T_j ≠ ∅`. Es decir, se van las que solapan con la ventana de prueba, estén
  antes o después.
- **Embargo:** con `h` la fracción de embargo, se eliminan además las observaciones `i` con
  `t0ᵢ > max t1 (pliegue j)` y `t0ᵢ ≤ max t1 (pliegue j) + h · N`. Es un hueco ciego después
  del pliegue, proporcional al horizonte de las variables.

Dos condiciones que no se pueden saltar: los pliegues son **consecutivos y sin barajar**, y
la purga se aplica **en los dos sentidos** (hacia atrás y hacia delante), porque el problema
no es solo el futuro filtrándose al pasado, sino también un pliegue de prueba que se apoya en
etiquetas que aún no habían terminado cuando empezó.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | El número de observaciones etiquetadas | filas | No cambia el esquema, pero con horizontes de etiqueta largos respecto a `N` el entrenamiento se queda sin datos y la purga no es el problema |
| `t0ᵢ` | El instante en que la observación `i` empieza a formarse | índice temporal | Si se adelanta respecto a la información que existía de verdad, es mirar al futuro y ninguna purga lo arregla |
| `t1ᵢ` | El instante en que la etiqueta de `i` queda determinada | índice temporal | Un horizonte más largo ensancha la ventana de purga: se caen más etiquetas del entrenamiento |
| `k` | El número de pliegues consecutivos | pliegues | Más pliegues dejan menos datos en cada uno y la purga pesa relativamente más; 5 o 6 es lo habitual |
| `T_j` | La ventana del pliegue de prueba `j`: de `min t0` a `max t1` de sus observaciones | intervalo temporal | Se ensancha con el horizonte de las etiquetas, no con el número de filas del pliegue |
| `h` | La fracción de embargo: el hueco ciego que se deja después del pliegue | fracción del total | Con `h = 0` sigue abierta la fuga de las *variables* (medias móviles, volatilidad); un 1-2 % es el punto de partida razonable |
| purga | Se eliminan del entrenamiento todas las etiquetas cuyo intervalo toca `T_j` | observaciones | Se aplica en los dos sentidos: purgar solo hacia atrás deja la mitad de la fuga |
| embargo | Se eliminan además las que empiezan justo después de `T_j` | observaciones | Crece con `h`; con `h` grande el conjunto de entrenamiento se queda corto |
:::

:::figura
fichero: purgado-purga-y-embargo
pie: Arriba, un K-fold de manual sobre 100 etiquetas que duran 10 barras: en rojo, las 20 que el modelo usaría para entrenar y que comparten precios con la ventana de prueba (la franja azul). Abajo, el mismo corte con purga y embargo: esas 20 salen, más 2 del hueco ciego, y ninguna de las 58 que quedan toca un solo día de la prueba. Se entrena con menos datos, pero la estimación deja de estar inflada.
fuente: figuras/purged-kfold-1.py
:::

## Ejemplo

100 observaciones con etiquetas que duran 10 pasos: la observación `i` ocupa `[i, i+10)`. Con
5 pliegues consecutivos, el pliegue de prueba es el tercero, de índices 40 a 59.

- `min t0 = 40`, `max t1 = 59 + 10 = 69`. La ventana de prueba es `[40, 69)`.
- **Sin purga:** entrenan 80 observaciones, pero 20 de ellas (de la 30 a la 69) comparten precios
  con la prueba. Una cuarta parte del entrenamiento está contaminado.
- **Con purga:** se caen las observaciones con `[i, i+10) ∩ [40, 69) ≠ ∅`, es decir de
  `i = 30` a `i = 68` → se eliminan 39 observaciones y quedan 41 de entrenamiento.
- **Con embargo del 2 %** sobre el recorrido total de las etiquetas (109 pasos, no 100): se caen
  además `i = 70`, `71` y `72`. Entrenamiento final: 38 observaciones.

Menos de la mitad de los datos, pero ninguna observación comparte una sola barra de precios
con el conjunto de prueba. El código de abajo imprime esa cuenta pliegue a pliegue: 58 de
entrenamiento para el tercer pliegue, con 22 observaciones tiradas entre purga y embargo.

## Código

```python verificable
import numpy as np

def purged_kfold(n_splits, t0, t1, embargo=0.0):
    """Divide en pliegues consecutivos y devuelve (train, test) con purga y embargo.

    t0, t1: arrays con el inicio y el fin de la etiqueta de cada observacion.
    embargo: fraccion del total de observaciones que se deja ciego tras el pliegue.
    """
    t0, t1 = np.asarray(t0, float), np.asarray(t1, float)
    assert np.all(t1 >= t0), "cada etiqueta debe terminar despues de empezar"
    n = t0.size
    pliegues = np.array_split(np.arange(n), n_splits)
    span = t1.max() - t0.min()

    for prueba in pliegues:
        inicio, fin = t0[prueba].min(), t1[prueba].max()

        # Purga: fuera cualquier etiqueta cuyo intervalo toque la ventana de prueba.
        solapa = (t1 >= inicio) & (t0 <= fin)

        # Embargo: fuera tambien el tramo inmediatamente posterior al pliegue.
        embargadas = (t0 > fin) & (t0 <= fin + embargo * span)

        entrenamiento = np.arange(n)[~solapa & ~embargadas]
        yield entrenamiento, prueba

# 100 observaciones cuyas etiquetas duran 10 pasos
n = 100
t0 = np.arange(n)
t1 = t0 + 10

for i, (train, test) in enumerate(purged_kfold(5, t0, t1, embargo=0.02)):
    print(f"pliegue {i}: prueba {test.size:>3}  train {train.size:>3}  "
          f"(purga+embargo quitan {n - test.size - train.size:>3})")
```

:::claves
- `np.asarray(t0, float)` acepta listas, tuplas o arrays y devuelve un array de NumPy sin copiar si ya lo era, forzando el tipo a coma flotante. El tipo importa: con enteros, el embargo por una fracción de la muestra se redondearía de otra manera.
- `np.array_split(np.arange(n), n_splits)` parte los índices en trozos **consecutivos y sin barajar**, que es de lo que depende todo el razonamiento; si `n` no es divisible entre `n_splits`, los primeros pliegues se llevan un elemento más. Un `KFold(shuffle=True)` de scikit-learn rompería justo esto.
- La purga es una sola condición sobre los dos extremos, `(t1 >= inicio) & (t0 <= fin)`. El `&` es el Y de NumPy elemento a elemento (`and` sobre arrays da error) y la máscara marca **también las propias filas de prueba**, porque cada etiqueta de prueba solapa con su ventana. Por eso `~solapa` quita de golpe la prueba y sus vecinas, y `test` se devuelve aparte sin filtrar.
- `arange(n)[~solapa & ~embargadas]` es indexación booleana: devuelve los índices que cumplen la condición, no los valores. Si se te olvida el `~`, devuelves exactamente las etiquetas que querías quitar, y el error no salta: sale un entrenamiento más pequeño y silencioso.
- El embargo del código mide la fracción sobre `span = t1.max() - t0.min()`, que con etiquetas de 10 barras vale 109 y no 100; el texto lo escribe como `h · N`. La diferencia se nota: con `h = 0,02` el corte cae en 69 + 2,18 y se caen tres filas (70, 71 y 72), no dos. Con horizontes largos la distancia crece: la fracción de embargo no es lo mismo que un número fijo de filas.
- `purged_kfold` es un **generador** (`yield`): no calcula ningún pliegue hasta que el bucle lo pide, y si el consumidor se detiene a la mitad los demás no llegan a construirse. Cada `train` que devuelve es un array nuevo; si hay que reutilizarlos todos, hay que guardarlos en una lista.
:::

```python verificable
import numpy as np

# Cuanto se contamina un K-fold normal: la comprobacion que justifica la purga.
n = 100
t0 = np.arange(n)
t1 = t0 + 10
prueba = np.arange(40, 60)                      # tercer pliegue de 5
inicio, fin = t0[prueba].min(), t1[prueba].max()

train_normal = np.setdiff1d(np.arange(n), prueba)          # K-fold clasico
contaminado = train_normal[(t1[train_normal] >= inicio) & (t0[train_normal] <= fin)]

print(f"ventana de prueba      [{inicio}, {fin})")
print(f"train clasico          {train_normal.size} observaciones")
print(f"de ellas contaminadas  {contaminado.size}  ({contaminado.size / train_normal.size:.0%})")
print(f"primera y ultima       {contaminado.min()} .. {contaminado.max()}")
```

## Errores típicos

- **Barajar antes de dividir.** Si usas `KFold(shuffle=True)` con series temporales, la purga
  ya no tiene sentido: has destruido el orden del que depende todo el razonamiento. Los
  pliegues son consecutivos siempre.
- **Purgar solo hacia atrás.** El solapamiento es simétrico: las etiquetas que empiezan
  dentro de la ventana de prueba también comparten información con ella. `t1 >= inicio` es
  tan necesario como `t0 <= fin`.
- **Embargo del 0 % «porque ya he purgado».** La purga corta el solapamiento de *etiquetas*;
  el embargo corta el de *variables* (medias móviles, volatilidad realizada, rezagos). Son dos
  fugas distintas. Un embargo del 1-2 % del total es un punto de partida razonable.
- **Usar la purga para elegir hiperparámetros y luego reportar el mismo resultado como
  rendimiento.** La validación cruzada, purgada o no, sirve para *elegir*. El rendimiento se
  estima después, con [[validacion-temporal|walk-forward]] o con datos que no hayas tocado.
  Y si has probado muchas configuraciones, aplica [[sharpe-deflactado|el ajuste por pruebas
  múltiples]].
- **Olvidar los pesos por unicidad.** Con etiquetas solapadas, dos observaciones casi
  idénticas cuentan doble. Purgar reduce el problema, pero [[sample-weights|los pesos por
  unicidad]] lo corrigen de verdad.
- **Creer que la purga arregla un mal etiquetado.** Si tu etiqueta usa información que no
  estaba disponible en `t0`, ninguna purga te salva: eso es
  [[sesgo-de-mirar-al-futuro|mirar al futuro]] en el propio etiquetado.

:::practica
enunciado: Tienes 240 observaciones con etiquetas que duran 30 barras: la observación i ocupa [i, i+30). Con 6 pliegues consecutivos de 40 y un embargo del 2,5 %, ¿cuántas observaciones quedan para entrenar cuando el pliegue de prueba es el cuarto, índices 120 a 159?
pista: La ventana de prueba es [120, 189). Se purga toda etiqueta que empiece antes de 189 y no haya terminado al arrancar la prueba; el embargo va justo después.
solucion: Sin purga entrenan 200. La ventana de prueba es [120, 190). Se purga la etiqueta [i, i+30) que toque esa ventana: i de 90 a 188, 99 observaciones, de las que 40 son la prueba, así que salen 59 y el entrenamiento baja a 141. El embargo es el 2,5 % del recorrido total de las etiquetas (269 pasos, no 240), unas 6,7 barras, y elimina i = 190 a 195. Entrenamiento final: 135 observaciones, ninguna de las cuales comparte una barra con la prueba.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia hay entre purgar y embargar?
o: La purga quita del entrenamiento las etiquetas que solapan con la prueba; el embargo quita además un tramo posterior cuyas variables contienen información de la prueba
o: La purga se aplica a las variables y el embargo a las etiquetas
o: Son dos nombres de la misma operación según el número de pliegues
a: 1
e: Son dos fugas distintas: la de etiquetas solapadas (purga) y la de variables con memoria que miran hacia atrás (embargo). El embargo es un hueco adicional después del pliegue, proporcional al horizonte de las variables.
:::

:::quiz
p: Con 100 observaciones cuyas etiquetas duran 10 pasos y un pliegue de prueba de 20 observaciones (índices 40 a 59), ¿por qué se eliminan unas 38 del entrenamiento?
o: Porque el entrenamiento debe ser siempre más pequeño que la prueba
o: Porque toda etiqueta que empieza entre el índice 30 y el 68 comparte días de precios con la ventana de prueba [40, 69), y el embargo quita además las tres siguientes
o: Porque el embargo por defecto es del 38 %
a: 2
e: Una etiqueta que empieza en 30 no termina hasta 40, justo cuando arranca la prueba; una que empieza en 68 llega hasta 78 y solapa con el final. Todas ellas comparten tramo de mercado con el conjunto de prueba y por eso no pueden usarse para entrenar.
:::

:::aviso
Purgar y embargar reduce el tamaño del entrenamiento de forma notable con horizontes largos.
Si tu horizonte de etiqueta es muy largo respecto al total de datos, el esquema se queda sin
datos y la conclusión correcta no es relajar la purga, sino aceptar que no tienes muestra
suficiente para ese horizonte.
:::
