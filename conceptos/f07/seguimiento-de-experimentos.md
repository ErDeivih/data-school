---
id: seguimiento-de-experimentos
titulo: Seguimiento de experimentos
fase: 7
nivel: intermedio
rutas: [ds, alg]
prerequisitos: [pytorch-fundamentos, seleccion-de-hiperparametros]
tags: [mlops, experimentos, trazabilidad, semillas, comparacion]
resumen: Qué guardar de cada ejecución para poder comparar dos configuraciones sin fiarte de la memoria, y cómo saber si una mejora es real o es ruido entre semillas.
fuentes: ["Bouthillier et al. (2021), 'Accounting for Variance in Machine Learning Benchmarks'", "Breck et al. (2017), 'The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction'", "MLflow (2024), 'MLflow Tracking'"]
---

## En una frase

Una ejecución sin registro es una anécdota: el seguimiento convierte cada entrenamiento en una
fila con su contexto, para que compares configuraciones y no recuerdos.

## La idea

Un cuaderno de laboratorio no existe para recordar lo que salió bien, sino para poder volver a
montar el experimento. Sin él, la memoria reescribe la historia: la ejecución que te gustaba se
recuerda mejor de lo que fue y la que te fastidió se recuerda como un fallo del que ya no quedan
datos. Con cuarenta variantes en dos semanas, eso es todo lo que te queda.

El seguimiento resuelve tres cosas que se confunden y no son la misma:

- **Identidad.** Cada entrenamiento tiene un identificador, y con él su configuración completa,
  la versión del código y la versión de los datos. Si dos ejecuciones no se pueden distinguir por
  su registro, el registro no sirve.
- **Comparabilidad.** Solo se comparan ejecuciones con la misma partición de validación y la
  misma métrica. Un modelo evaluado sobre otro 20 % de los datos no es comparable con nada,
  aunque el número sea más bonito.
- **Incertidumbre.** La misma configuración con otra semilla da otro número. Sin varias semillas
  no puedes distinguir una mejora real del temblor de fondo, y esa es la decisión que vas a tener
  que tomar una y otra vez.

Ese último punto es el que separa un registro útil de una carpeta de ficheros. La semilla tiene
que ser un campo de primera clase, no una nota al margen: es lo que convierte una columna de
resultados en una distribución. Cuando dos configuraciones difieren en 0,008 y la dispersión
entre semillas es de 0,005, la diferencia existe; cuando difieren en 0,008 y la dispersión es de
0,02, lo único que has observado es qué semilla te tocó.

Qué guardar de cada ejecución:

1. **Identificador automático** y la fecha. Los nombres a mano («prueba_final_v2_definitivo») no
   son identificadores: no son únicos, no se ordenan y no dicen nada.
2. **La configuración entera**, incluidos los valores por defecto que no tocaste. Si el registro
   solo tiene los hiperparámetros que cambiaste, dos ejecuciones distintas comparten ficha.
3. **El código**: el commit, y si el árbol de trabajo estaba sucio.
4. **Los datos**: el hash del fichero o de la consulta, y qué partición se usó para validar.
5. **La semilla.**
6. **Las métricas por época**, no solo la final. La curva dice si el entrenamiento se quedó corto
   o si seguía mejorando cuando lo paraste; el número final no dice nada de eso.
7. **El estado**: completada, abortada o fallida. Tirar los fallos es un sesgo: pierdes el
   registro de lo que no funciona y lo repites dentro de un mes.
8. **Los artefactos**: los pesos del mejor punto, las muestras generadas, las figuras.

Lo que **no** se guarda: el conjunto de datos entero (se guarda su hash), las claves ni los
tokens, y los tensores intermedios de cada paso.

:::trampa
Elegir el mejor de cuarenta ejecuciones y presentarlo como el resultado es una selección sobre
ruido. El ganador de una comparación múltiple tiene una puntuación optimista por construcción, y
cuando repitas esa configuración no llegará a ese número. Si vas a quedarte con el máximo, mide
el máximo de un conjunto de semillas que no hayas usado para elegirlo.
:::

:::figura
fichero: seguimiento-solape-y-semillas
pie: A la izquierda, dos configuraciones de la misma red, cinco semillas cada una, dibujadas como la media por época con una banda de dos desviaciones. Las bandas se solapan durante todo el entrenamiento: si solo hubieras lanzado una ejecución de cada una, la conclusión habría dependido de qué semilla te tocara, y las dos historias que se pueden contar con esos mismos diez números son opuestas. La comparación se hace entre medias con su dispersión, no entre curvas sueltas. A la derecha, el presupuesto que hace falta para declarar una mejora: el número de semillas por configuración crece con el cuadrado de la relación entre la dispersión y el efecto que quieres detectar, así que doblar el ruido multiplica por cuatro el cómputo. La línea de puntos marca las cinco semillas habituales, que solo bastan para efectos grandes.
fuente: figuras/seguimiento-de-experimentos-1.py
:::

## Definición formal

Sea `M(r)` la métrica principal de la ejecución `r`, medida siempre sobre la misma partición de
validación. Para una configuración `A` con `k` semillas, `M̄_A` es la media y `s_A` su desviación
típica. El contraste entre dos configuraciones es:

:::formula
Δ = M̄_A − M̄_B          EE(Δ) = s · √(2 / k)          mejora creíble si /Δ/ > 2 · EE(Δ)
:::

donde `s` es la desviación típica agrupada de las dos configuraciones y `EE(Δ)` el error típico
de la diferencia. El factor 2 es la convención habitual de «dos errores típicos», que deja fuera
aproximadamente el 95 % de las diferencias que produce el azar cuando no hay efecto.

Despejando, el número de semillas que hace falta para detectar una mejora de tamaño `δ` con esa
misma dispersión es:

:::formula
k ≥ 8 · (s / δ)²
:::

La consecuencia práctica es incómoda: el esfuerzo crece con el **cuadrado** de la relación entre
el ruido y el efecto. Si la dispersión entre semillas es el doble de la mejora que buscas,
necesitas 32 semillas; si es cuatro veces mayor, 128.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `M(r)` | Métrica principal de una ejecución, sobre una partición fija | las de la métrica (exactitud, F1, pérdida) | Es la unidad de comparación. Si cambia de definición entre ejecuciones, toda la tabla deja de tener sentido: por eso la métrica principal se fija antes de empezar |
| `M̄` | Media de la métrica sobre las semillas de una configuración | las de `M` | Es la cifra que se compara, y solo es interpretable junto a su dispersión. Una media de 0,853 con `s = 0,005` sobre 5 semillas admite cualquier valor entre 0,83 y 0,87 |
| `s` | Desviación típica entre semillas de la misma configuración | las de `M` | Sube con la capacidad del modelo, con menos datos y con menos épocas. Es el ruido de fondo del problema, y no se reduce cambiando de hiperparámetro: se reduce entrenando varias semillas y promediando, o midiendo con más datos de validación |
| `k` | Número de semillas distintas de una misma configuración | recuento | Al subir, el error típico de la media baja como `1/√k`: pasar de 1 a 4 semillas reduce el ruido a la mitad, y de 4 a 16 otra vez a la mitad. Es la palanca más aburrida y la más eficaz |
| `Δ` | Diferencia observada entre las medias de dos configuraciones | las de `M` | Es lo que quieres declarar. Su signo importa menos que su tamaño comparado con `2 · EE(Δ)`: por debajo de ese listón, el signo cambia si repites el experimento con otras semillas |
| `EE(Δ)` | Error típico de la diferencia de dos medias independientes | las de `M` | Baja al subir `k` y sube con `s`. Es el listón contra el que se mide `Δ`; se calcula con la dispersión **entre semillas**, no con el error de validación de una sola ejecución |
| `δ` | Mejora mínima que te interesa detectar | las de `M` | Es una decisión de negocio, no estadística: si medio punto de exactitud no cambia ninguna decisión, no gastes 128 semillas en detectarlo. Al subir `δ`, el número de semillas necesario cae con su cuadrado |
:::

## Ejemplo

Dos configuraciones de la misma red, cinco semillas cada una, misma partición de validación:

```
config      count    mean     std
lr-1e-3         5  0.8450  0.0052
lr-3e-4         5  0.8532  0.0037
mejor de cada configuracion:
  lr-1e-3  semilla 1  ->  0.851
  lr-3e-4  semilla 3  ->  0.858
```

La diferencia de medias es 0,0082 y el error típico de la diferencia vale
`0,0045 · √(2/5) = 0,0029`, así que el listón de dos errores típicos es 0,0057. La mejora pasa el
listón: `lr-3e-4` es mejor, aunque la banda de una configuración se solape con la de la otra.

Y ahí está la trampa que el registro evita. El **peor** resultado de `lr-3e-4` (0,849) es peor
que el **mejor** de `lr-1e-3` (0,851). Con una sola ejecución de cada una, la conclusión habría
dependido de qué semilla te tocara, y las dos historias que se pueden contar con estos mismos
diez números son opuestas. La tabla de medias y desviaciones no es un adorno: es lo que decide.

Si la mejora que te interesa detectar fuera de 0,004 en vez de 0,008, con `s = 0,0045` harían
falta `8 · (0,0045/0,004)² = 10,3`, es decir **11 semillas** por configuración en lugar de 5. Pasar
de la intuición «probé un par de veces» a un presupuesto de cómputo razonado es justo lo que
permite el registro.

## Código

```python verificable
import pandas as pd

# Cada fila es una ejecucion: la configuracion, la semilla y la metrica de validacion
runs = pd.DataFrame([
    {"config": "lr-1e-3", "semilla": 0, "val_acc": 0.842},
    {"config": "lr-1e-3", "semilla": 1, "val_acc": 0.851},
    {"config": "lr-1e-3", "semilla": 2, "val_acc": 0.838},
    {"config": "lr-1e-3", "semilla": 3, "val_acc": 0.849},
    {"config": "lr-1e-3", "semilla": 4, "val_acc": 0.845},
    {"config": "lr-3e-4", "semilla": 0, "val_acc": 0.851},
    {"config": "lr-3e-4", "semilla": 1, "val_acc": 0.856},
    {"config": "lr-3e-4", "semilla": 2, "val_acc": 0.849},
    {"config": "lr-3e-4", "semilla": 3, "val_acc": 0.858},
    {"config": "lr-3e-4", "semilla": 4, "val_acc": 0.852},
])

resumen = runs.groupby("config")["val_acc"].agg(["count", "mean", "std"])
for config, fila in resumen.iterrows():
    print(f"{config}: {int(fila['count'])} ejecuciones, media {fila['mean']:.4f}, "
          f"desviacion {fila['std']:.4f}")
# -> lr-1e-3: 5 ejecuciones, media 0.8450, desviacion 0.0052
# -> lr-3e-4: 5 ejecuciones, media 0.8532, desviacion 0.0037
print("mejor de cada configuracion:")
print(runs.loc[runs.groupby("config")["val_acc"].idxmax(), ["config", "semilla", "val_acc"]].to_string(index=False))
```

:::claves
- `groupby("config")` seguido de `agg(["count", "mean", "std"])` devuelve un DataFrame con el índice puesto en `config`, no una columna. Si luego quieres mezclarlo con otra tabla, hace falta `reset_index()`.
- `std()` de pandas usa `ddof=1` por defecto, es decir divide entre `n − 1`. Con 5 semillas eso importa: `np.std` sin argumentos dividiría entre 5 y daría una desviación menor, justo en la dirección que hace parecer más fiable lo que no lo es.
- El `std` de un grupo de una sola fila sale `NaN`, no 0. Un registro con muchas configuraciones probadas una sola vez produce una tabla llena de `NaN`, y ese es exactamente el diagnóstico: no hay dispersión que medir porque no hay repeticiones.
- `runs.loc[runs.groupby("config")["val_acc"].idxmax(), [...]]` localiza la fila del máximo por grupo. `idxmax` devuelve **posiciones de índice**, no posiciones 0..n; si el DataFrame tuviera un índice personalizado, el `loc` seguiría funcionando y un `iloc` con esos números no.
- `.to_string(index=False)` evita que se imprima el índice de pandas. Es cosmético, pero copiar la salida de un `print` de DataFrame a un informe sin quitar el índice es una fuente inagotable de columnas fantasma.
- Fíjate en que la tabla completa son diez números, y que la conclusión («`lr-3e-4` es mejor») no se puede leer en ninguno de ellos por separado: sale de la media y de la desviación juntas.
:::

```python verificable
import numpy as np

a = np.array([0.842, 0.851, 0.838, 0.849, 0.845])   # configuracion A, una fila por semilla
b = np.array([0.851, 0.856, 0.849, 0.858, 0.852])   # configuracion B, las mismas semillas

# Dispersion agrupada: el ruido entre semillas que comparten las dos configuraciones
s = np.sqrt((a.std(ddof=1) ** 2 + b.std(ddof=1) ** 2) / 2)
delta = b.mean() - a.mean()
ee = s * np.sqrt(2 / len(a))                        # error tipico de la diferencia de medias

print(f"medias          {a.mean():.4f}  y  {b.mean():.4f}")   # -> 0.8450  y  0.8532
print(f"dispersion s    {s:.4f}")                             # -> 0.0045
print(f"diferencia      {delta:.4f}")                         # -> 0.0082
print(f"2 x ee(delta)   {2 * ee:.4f}")                        # -> 0.0057
print(f"mejora creible  {bool(abs(delta) > 2 * ee)}")         # -> True
print(f"semillas para detectar delta=0,004 con esa s: {int(np.ceil(8 * (s / 0.004) ** 2))}")   # -> 11
```

:::claves
- `a.std(ddof=1)` es imprescindible: con `ddof=0` (el valor por defecto de NumPy) la dispersión sale más pequeña y el listón de decisión baja, con lo que declararías mejoras que no lo son. pandas y NumPy no coinciden en este valor por defecto, y ese es el error de copiar y pegar entre los dos.
- La dispersión se **agrupa** en lugar de usar solo la de una configuración: con `k` pequeño, la desviación de un grupo de cinco tiene mucho error de muestreo. Promediar las varianzas de las dos usa toda la información disponible; la raíz del promedio de las varianzas es la desviación agrupada.
- `ee = s * np.sqrt(2 / len(a))` es el error típico de una **diferencia**. El `√2` aparece porque la diferencia de dos medias independientes suma sus varianzas: `Var(A − B) = Var(A) + Var(B)`. Si te olvidas del 2, el listón baja un 29 % y empiezas a creerte el ruido.
- El listón es `2 · ee`, no `ee`. Con `ee` solo estarías exigiendo una desviación típica de separación, que el azar produce a menudo.
- `int(np.ceil(8 * (s / 0.004) ** 2))` redondea hacia arriba: el número de semillas es entero y quedarse corto invalida el cálculo. Sale 11, no 10,3.
- Fíjate en que el denominador 0,004 es una decisión tuya: es la mejora mínima que te importa. Si nadie va a actuar distinto con menos de un punto de exactitud, el cálculo debe usar 0,01 y el presupuesto se divide por seis.
:::

```python ilustrativo
import mlflow

# El registro tiene que ser automatico: si depende de que te acuerdes, no se hace
mlflow.set_experiment("deteccion-de-fraude")

with mlflow.start_run(run_name="lr-3e-4-semilla-0"):
    mlflow.log_params({
        "lr": 3e-4, "batch_size": 64, "epochs": 30, "semilla": 0,
        "git_commit": "a1b2c3d", "datos_sha256": "9f2c41e0", "particion": "fold-2-de-5",
    })
    for epoca in range(30):
        mlflow.log_metrics({"val_loss": val_loss, "val_acc": val_acc}, step=epoca)
    mlflow.log_metric("val_acc_final", val_acc)
    mlflow.log_artifact("checkpoints/mejor.pt")
```

:::claves
- La configuración se registra **entera**, incluidos `batch_size` y `epochs`, que no se tocaron en esta tanda. Dos ejecuciones con la misma ficha tienen que ser la misma ejecución; si el registro solo guarda lo que cambiaste, el día que alguien cambie el valor por defecto de la librería tendrás dos ejecuciones indistinguibles con resultados distintos.
- `datos_sha256` y `particion` van juntos: el hash dice qué datos, la partición dice qué trozo se usó para validar. Sin lo segundo, dos ejecuciones con el mismo hash pueden estar midiendo sobre conjuntos distintos y la comparación es falsa.
- `log_metrics(..., step=epoca)` guarda la serie, no solo el final. Es lo que después permite ver que una ejecución se quedó corta o que ya había convergido, y es la diferencia entre un registro y un marcador.
- `git_commit` es un campo de texto libre y por eso es fácil guardarlo mal: si el árbol de trabajo tenía cambios sin confirmar, el hash apunta a un código que no es el que se ejecutó. Lo honesto es guardar el hash **y** un indicador de árbol sucio.
- Nada de esto guarda el modelo entrenado ni los datos: `log_artifact` se lleva el checkpoint y el hash cubre los datos. Registrar el dataset completo en cada ejecución multiplica el almacenamiento sin añadir información.
:::

## Errores típicos

- **Registrar solo la métrica final.** Sin la curva por época no sabes si la ejecución se quedó
  corta, si divergió al final o si el mejor punto estaba en la época 12. El número final
  esconde las tres cosas.
- **Nombrar las ejecuciones a mano.** «Prueba buena», «prueba buena 2». En una semana no sabrás
  qué cambió entre ellas, y dos nombres distintos pueden ser la misma configuración repetida.
- **Guardar solo los hiperparámetros que tocaste.** El resto de la configuración también define
  la ejecución. El síntoma es que dos ejecuciones con la misma ficha dan números distintos y no
  hay forma de saber por qué.
- **Comparar ejecuciones con distinta partición o distinta métrica.** El resultado es una tabla
  ordenada que no significa nada. La partición y la métrica son parte de la clave de comparación,
  no metadatos decorativos.
- **Descartar las ejecuciones fallidas.** El registro de lo que no funciona es la mitad del
  valor: evita que dentro de tres meses repitas el mismo camino muerto. Los fallos se registran
  con su estado, no se borran.
- **Elegir el mejor run de una tanda y quedarse con ese número.** Es una selección sobre ruido,
  el valor es optimista y no se reproduce. Si necesitas el máximo, calcula el máximo sobre
  semillas que no hayas usado para elegir la configuración.

:::practica
enunciado: Una configuración concreta da, con 6 semillas, una exactitud media de 0,882 y una desviación típica entre semillas de 0,009. Otra da 0,889 con la misma dispersión y también 6 semillas. ¿Puedes afirmar que la segunda es mejor? ¿Cuántas semillas harían falta para detectar una mejora de 0,005 con esa dispersión?
pista: Calcula el error típico de la diferencia con `s · √(2/k)` y compáralo con dos veces ese valor. Para el número de semillas, despeja `k ≥ 8 · (s/δ)²`.
solucion: La diferencia es 0,007. El error típico vale 0,009 · √(2/6) = 0,009 · 0,5774 = 0,0052, y el listón de dos errores típicos es 0,0104. Como 0,007 < 0,0104, no hay evidencia suficiente: las dos configuraciones son indistinguibles con estos datos. Para detectar 0,005 con s = 0,009 harían falta 8 · (0,009/0,005)² = 8 · 3,24 = 25,9, es decir 26 semillas por configuración. Alternativa razonable: si 0,005 no cambia ninguna decisión del negocio, deja de medirlo y quédate con la configuración más barata de entrenar.
:::

## Comprueba que lo sabes

:::quiz
p: Dos configuraciones dan 0,845 y 0,853, con una desviación típica entre semillas de 0,02 en ambas y cuatro semillas por configuración. ¿Qué concluyes?
o: Que la segunda es mejor, porque su media es más alta
o: Que no hay evidencia suficiente: la diferencia es menor que dos errores típicos de la diferencia
o: Que hay que repetir el experimento con más épocas para reducir la dispersión
a: 2
e: El error típico de la diferencia vale 0,02 · √(2/4) = 0,0141 y el listón de dos errores típicos es 0,028. La diferencia observada, 0,008, es mucho menor: cambiar las semillas puede dar el resultado contrario. Ni más épocas ni más capas arreglan eso; lo que hace falta son más semillas o un efecto más grande.
:::

:::quiz
p: ¿Por qué hay que guardar los hiperparámetros que no tocaste?
o: Porque dos ejecuciones con la misma ficha deben ser la misma ejecución, y el valor por defecto forma parte de la configuración
o: Porque ocupan poco y nunca está de más
o: Porque el servidor de seguimiento los exige para calcular la curva
a: 1
e: El registro sirve para distinguir ejecuciones. Si solo anotas lo que cambiaste, dos entrenamientos distintos comparten ficha y ningún análisis posterior puede separarlos. Además, los valores por defecto cambian entre versiones de la librería: la misma ficha puede describir dos cosas.
:::

:::quiz
p: Tienes 30 ejecuciones de 30 configuraciones distintas y eliges la de mayor exactitud en validación. ¿Qué problema tiene ese número?
o: Ninguno, es el mejor resultado observado
o: Que es el máximo de una comparación múltiple y está sesgado hacia arriba; no se reproducirá igual con otras semillas
o: Que hay que descontarle el error de validación del modelo
a: 2
e: El máximo de muchas mediciones ruidosas tiende a caer por encima del valor real de la mejor configuración: parte de lo que mide es suerte. La forma de comprobarlo es volver a entrenar la ganadora con semillas nuevas y ver si mantiene la marca.
:::

:::aviso
El registro no sustituye al criterio. Una tabla con cuatrocientas ejecuciones y una partición de
validación distinta en cada una es peor que tres ejecuciones comparables: da la ilusión de
evidencia sin permitir ninguna comparación. Antes de lanzar la primera tanda, fija la métrica
principal, la partición y el número de semillas.
:::
