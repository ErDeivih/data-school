---
id: matriz-de-confusion
titulo: Matriz de confusión
fase: 6
nivel: básico
rutas: [core, ds]
prerequisitos: [train-val-test]
tags: [evaluacion, clasificacion, diagnosticos]
resumen: La tabla de cuatro casillas que cuenta aciertos y errores de un clasificador binario, y el punto de partida de casi toda métrica.
fuentes: ["Provost, Fawcett y Kohavi (1998), 'The Case Against Accuracy Estimation for Comparing Induction Algorithms'"]
---

## En una frase

La matriz de confusión cuenta cuántos casos caen en cada combinación de «lo que era» y «lo que
el modelo dijo que era», y es la única vista de un clasificador que no oculta información.

## La idea

Un detector de humo tiene dos formas de fallar. Puede sonar por el vapor de la ducha: molesto,
pero nadie se muere. O puede quedarse callado en un incendio: silencioso y catastrófico. Si
solo te doy un número («el detector acierta el 99 % de las veces»), no sabes cuál de los dos
fallos te está tocando sufrir.

La matriz de confusión es simplemente la tabla que separa esos dos fallos. Filas: lo que era
de verdad. Columnas: lo que dijo el modelo. Cada celda es un recuento. Con esos cuatro
números ya se puede calcular cualquier métrica de clasificación —[[metricas-de-clasificacion]]
no es más que aritmética sobre esta tabla—, y además se ve de un vistazo el tipo de error que
domina.

La convención habitual, y la que usa `scikit-learn`, es **filas = clase real, columnas = clase
predicha**. Esto importa más de lo que parece: si lees la tabla girada, interpretas los falsos
positivos como falsos negativos y sacas la conclusión contraria. Con clases desbalanceadas la
matriz es además la primera cosa que hay que mirar, porque un modelo que acierta el 98 % puede
estar acertando solo la clase mayoritaria. Ese fenómeno tiene nombre: la **paradoja de la
exactitud**.

Con más de dos clases, la matriz crece a `k × k` y la diagonal sigue siendo los aciertos, pero
los errores ya no son uno: cada celda fuera de la diagonal es un par concreto de confusión
(«predijo gato cuando era perro»). Ahí es donde se descubre si el modelo falla de forma
razonable o está mezclando dos clases que no tienen nada que ver.

## Definición formal

Para un problema binario con clase positiva (la que te interesa detectar) y negativa:

| | Predicho positivo | Predicho negativo |
| --- | --- | --- |
| Real positivo | VP (verdadero positivo) | FN (falso negativo) |
| Real negativo | FP (falso positivo) | VN (verdadero negativo) |

- `VP` — el modelo dijo positivo y era positivo. El acierto que buscabas.
- `FN` — el modelo dijo negativo y era positivo. Lo que se te escapó.
- `FP` — el modelo dijo positivo y era negativo. La falsa alarma.
- `VN` — el modelo dijo negativo y era negativo.

Los cuatro suman el total de casos evaluados. De aquí salen:

- `Sensibilidad = VP / (VP + FN)`: de todos los positivos reales, cuántos detectas.
- `Especificidad = VN / (VN + FP)`: de todos los negativos reales, cuántos dejas en paz.
- `Precisión o valor predictivo positivo = VP / (VP + FP)`: de todas tus alertas, cuántas eran
  reales.
- `Exactitud = (VP + VN) / (VP + FP + FN + VN)`.

Las dos primeras son **propiedades del modelo**: si el modelo no cambia y el umbral tampoco,
valen lo mismo en cualquier población. La precisión no: depende de la **prevalencia**
(la proporción de positivos reales en la población donde lo aplicas), y por eso un test
excelente en un hospital puede ser inútil en un cribado masivo.

:::figura
fichero: confusion-matriz-y-prevalencia
pie: A la izquierda, los cuatro recuentos del ejemplo con sus márgenes: sensibilidad y especificidad son cocientes dentro de una fila, y la precisión mezcla las dos. A la derecha, el mismo test sobre 20.000 casos con un 20 % de enfermos y con un 0,5 %: los aciertos de la diagonal apenas se mueven, pero la precisión pasa de 0,74 a 0,054 porque las 1.492 falsas alarmas se cuentan contra 85 aciertos. La conclusión práctica es que una matriz sin la prevalencia al lado no dice si el test sirve: el modelo no empeoró, cambió el terreno.
fuente: figuras/matriz-de-confusion-1.py
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `VP` | Positivos reales que el modelo acertó | casos | Suben la sensibilidad y la precisión |
| `FN` | Positivos reales que el modelo dejó pasar | casos | Baja la sensibilidad, `VP / (VP + FN)`: son los casos perdidos |
| `FP` | Falsas alarmas: negativos marcados como positivos | casos | Bajan la precisión y la especificidad; la sensibilidad no se toca |
| `VN` | Negativos que el modelo dejó en paz | casos | Sube la especificidad; la precisión no se toca |
| `N` | Total de casos evaluados (`VP + FN + FP + VN`) | casos | Ninguna tasa cambia por sí sola: lo que crece es el número absoluto de errores |
| `π` | Prevalencia: proporción de positivos reales en la población donde aplicas el test | adimensional, entre 0 y 1 | Sube la precisión mucho, y no mueve ni la sensibilidad ni la especificidad |
| `τ` | Umbral: la puntuación a partir de la cual el modelo dice «positivo» | las de la puntuación | Bajan los FP y suben los FN: la precisión sube y la sensibilidad cae |
:::

Con `k` clases, la matriz es `k × k` y la diagonal son los aciertos. Dos formas de normalizarla,
y eligen cosas distintas: dividir por la suma de la fila da la sensibilidad de cada clase
(útil si las clases tienen tamaños distintos), y dividir por la suma de la columna da la
precisión de cada clase.

## Ejemplo

200 pacientes, 40 con la enfermedad. El test detecta 34 de los 40 enfermos y da 12 falsas
alarmas entre los 160 sanos:

- `VP = 34`, `FN = 6`, `FP = 12`, `VN = 148`. Comprobación: 34 + 6 + 12 + 148 = 200.
- Sensibilidad = 34 / 40 = **0,85**.
- Especificidad = 148 / 160 = **0,925**.
- Precisión = 34 / (34 + 12) = 34 / 46 = **0,739**. Casi uno de cada cuatro positivos es falso.
- Exactitud = (34 + 148) / 200 = **0,91**.

Ahora cambia la población y no el test. Si aplicas el mismo test a una población donde solo 1 de
cada 200 personas está enferma (prevalencia 0,005), la sensibilidad y la especificidad siguen
siendo 0,85 y 0,925, pero entre 199 sanos esperas unas `0,075 · 199 ≈ 15` falsas alarmas frente
a 0,85 aciertos: la precisión cae a `0,85 / (0,85 + 15) = 0,054`. La matriz lo habría dejado
claro antes de llevarse la sorpresa.

## Código

```python verificable
# 200 pacientes: 40 enfermos. El test detecta 34 y da 12 falsas alarmas.
# Cada caso es una pareja (real, predicho) con 1 = positivo; contar es construir la matriz.
# [(1, 1)] * 34 repite la MISMA tupla 34 veces. Con tuplas da igual porque son inmutables,
# pero con listas, [[0, 0]] * 3 deja tres filas enlazadas y cambiar una cambia las tres.
casos = [(1, 1)] * 34 + [(1, 0)] * 6 + [(0, 1)] * 12 + [(0, 0)] * 148

# sum(1 for ...) es una expresion generadora: recorre y suma sin construir una lista
# intermedia en memoria, que con un millon de casos se nota.
vp = sum(1 for real, pred in casos if real == 1 and pred == 1)
fn = sum(1 for real, pred in casos if real == 1 and pred == 0)
fp = sum(1 for real, pred in casos if real == 0 and pred == 1)
vn = sum(1 for real, pred in casos if real == 0 and pred == 0)

# En Python 3, vp / (vp + fn) es una division real aunque los dos sean enteros: da 0.85.
print(f"VP {vp}  FN {fn}  FP {fp}  VN {vn}")       # -> VP 34  FN 6  FP 12  VN 148
print(f"sensibilidad {vp / (vp + fn):.3f}")        # -> 0.850
print(f"especificidad {vn / (vn + fp):.3f}")       # -> 0.925
print(f"precision    {vp / (vp + fp):.3f}")        # -> 0.739
print(f"suma de la matriz {vp + fn + fp + vn}")    # -> 200

# sklearn.metrics.confusion_matrix devuelve esta misma tabla como array 2x2, con las
# filas = clase real y las columnas = clase predicha: con labels=[0, 1], [[VN, FP], [FN, VP]].
```

:::claves
- `[(1, 1)] * 34` no crea 34 tuplas distintas: repite la misma. Con tuplas es inofensivo (no se pueden modificar), pero el mismo truco con listas, `[[0, 0]] * 3`, deja las tres filas enlazadas: escribir en una escribe en las tres.
- `sum(1 for real, pred in casos if ...)` es una **expresión generadora**: cuenta sin construir ninguna lista intermedia. `sum([...])` daría el mismo número gastando memoria de más.
- Comparar con `real == 1 and pred == 1` y no con `real and pred`: con etiquetas 0/1 las dos cosas coinciden, pero si algún día usas −1 y +1 (lo habitual en una máquina de vectores), `and` daría verdadero para (−1, −1) y contarías como acierto justo lo contrario.
- En Python 3, `vp / (vp + fn)` es una **división real** aunque los dos sean enteros: da 0,85 y no 0. Si vienes de Python 2, ahí ese mismo código devolvía 0 y todo el cálculo salía a cero.
- `confusion_matrix` de `scikit-learn` devuelve un `np.array` de 2 × 2 (no un DataFrame y no guarda los nombres de las etiquetas): con `labels=[0, 1]` —o con etiquetas booleanas, que sklearn ordena como `[False, True]`— el orden es `[[VN, FP], [FN, VP]]`. Si lo imprimes sin mirar el orden de las etiquetas, lees los falsos positivos como falsos negativos.
- La función `vpp(prevalencia)` del segundo bloque no recibe la sensibilidad ni la especificidad: las toma del ámbito de fuera. Si cambias `sensibilidad` arriba, `vpp` devuelve otra cosa sin que hayas tocado la función.
:::

```python verificable
# La sensibilidad y la especificidad se quedan igual; la precision se hunde.
sensibilidad, especificidad = 0.85, 0.925
falso_positivo = 1 - especificidad

def vpp(prevalencia):
    """Valor predictivo positivo: la precision que se ve con esa prevalencia."""
    return (sensibilidad * prevalencia) / (
        sensibilidad * prevalencia + falso_positivo * (1 - prevalencia)
    )

print(f"prevalencia 0.200 -> VPP {vpp(0.20):.4f}")    # -> 0.7391
print(f"prevalencia 0.020 -> VPP {vpp(0.02):.4f}")    # -> 0.1878
print(f"prevalencia 0.005 -> VPP {vpp(0.005):.4f}")   # -> 0.0539
```

## Errores típicos

- **Leer la matriz girada.** Confundir filas con columnas convierte los falsos positivos en
  falsos negativos. Fija la convención al principio (filas = realidad) y comprueba que la
  diagonal es lo que crees.
- **Tratar FP y FN como si fueran lo mismo.** No lo son: uno molesta a un inocente y el otro
  deja pasar el caso que querías cazar. Antes de resumirlos en un solo número, pregúntate
  cuánto cuesta cada uno.
- **Mirar solo la diagonal.** La información está fuera de ella. Con 10.000 casos y 30 errores,
  saber si son 30 falsas alarmas o 30 casos perdidos cambia por completo la decisión.
- **Olvidar que la matriz es de un umbral concreto.** El mismo modelo con otro punto de corte
  da otra tabla. Si publicas una matriz, publica el umbral.
- **Comparar matrices sin normalizar con clases de distinto tamaño.** Con 900 negativos y 100
  positivos, la celda de VN domina la tabla y todo lo demás parece pequeño. Normaliza por
  filas para comparar sensibilidades.
- **Aplicar una precisión medida en un conjunto balanceado a una población donde el positivo
  es raro.** Es el error del ejemplo: el modelo no empeora, cambia el terreno. Recalcula la
  precisión con la prevalencia real de despliegue.

:::practica
enunciado: En 5.000 operaciones hay 100 fraudes. El detector lanza 250 alertas y 70 son fraude real. Construye la matriz, calcula sensibilidad, especificidad, precisión y exactitud, y di qué celda domina el error.
pista: Los falsos negativos son los fraudes no detectados y los falsos positivos, las alertas que no lo eran. Todo suma 5.000.
solucion: VP = 70, FN = 100 − 70 = 30, FP = 250 − 70 = 180 y VN = 4.900 − 180 = 4.720; la matriz suma 5.000. Sensibilidad = 70/100 = 0,70; especificidad = 4.720/4.900 = 0,963; precisión = 70/250 = 0,28; exactitud = 4.790/5.000 = 0,958. Domina el falso positivo: 180 alertas falsas frente a 30 fugas, seis veces más, y menos de una de cada tres alertas es fraude.
:::

## Comprueba que lo sabes

:::quiz
p: De 200 pacientes, 40 están enfermos. El test detecta a 34 y da 12 falsas alarmas entre los sanos. ¿Cuántos falsos negativos hay?
o: 6, porque son los 40 enfermos menos los 34 detectados
o: 12, las falsas alarmas
o: 148, los sanos bien clasificados
a: 1
e: El falso negativo es un positivo real que el modelo deja pasar: 40 − 34 = 6. Las 12 falsas alarmas son falsos positivos y los 148 son verdaderos negativos.
:::

:::quiz
p: El mismo test (sensibilidad 0,85 y especificidad 0,925) se aplica a una población donde la enfermedad es 100 veces más rara. ¿Qué cambia?
o: La sensibilidad y la especificidad bajan, porque hay menos enfermos
o: La precisión baja mucho, porque las falsas alarmas se cuentan contra muy pocos aciertos
o: Nada, porque la matriz de confusión no depende de la población
a: 2
e: Sensibilidad y especificidad son propiedades del test y no cambian con la prevalencia. La precisión es un cociente entre aciertos positivos y alertas totales: si los sanos son muchísimos más, las falsas alarmas crecen en número absoluto y la precisión se hunde.
:::

:::aviso
Una matriz de confusión de un modelo con fuga de datos puede ser espectacular y no significar
nada. Antes de celebrar la tabla, comprueba que las variables no contienen información del
futuro ni de la etiqueta, y que el conjunto de prueba es realmente de prueba.
:::
