---
id: metricas-de-ranking
titulo: Métricas de ranking
fase: 6
nivel: avanzado
rutas: [ds, alg]
prerequisitos: [roc-auc, metricas-de-clasificacion]
tags: [ranking, recuperacion, evaluacion, orden]
resumen: Precision@k, recall@k, MAP, MRR y NDCG: cómo se evalúa un sistema cuando lo que importa es el orden y solo se mira la parte de arriba.
fuentes: ["Järvelin y Kekäläinen (2002), 'Cumulated gain-based evaluation of IR techniques'", "Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval', cap. 8"]
---

## En una frase

Cuando el resultado es una lista ordenada y el usuario solo mira las primeras posiciones, la
calidad se mide sobre esa lista —aciertos en el top k, posición del primer acierto y ganancia
acumulada— y no con la exactitud de un clasificador.

## La idea

Un buscador devuelve 10 resultados. Un filtro de spam decide sí o no. Los dos son «modelos», y
no se evalúan igual. En el filtro, cada caso tiene su etiqueta y el orden no significa nada. En
el buscador, el orden **es** el producto: los mismos 10 documentos con el relevante en la
posición 1 y en la posición 10 son resultados comerciales opuestos.

Tres hechos separan este problema del de [[metricas-de-clasificacion]]:

1. **No hay verdaderos negativos observables.** El catálogo tiene un millón de documentos y tú
   solo has anotado la relevancia de los que decidiste mostrar. No puedes contar los aciertos
   «negativos» porque no sabes qué había debajo. La exactitud y la especificidad no tienen
   sentido aquí, y el AUC responde a otra pregunta: ordenar bien una pareja de relevante y no
   relevante, sin fijarse en si los aciertos están arriba.
2. **Solo importa la cabeza.** El usuario mira los tres primeros resultados; el analista revisa
   las 40 alertas que caben en su turno. Fallar en la posición 200 es irrelevante.
3. **El orden de los aciertos importa.** Tener tres relevantes en las posiciones 1, 2 y 3 no
   vale lo mismo que tenerlos en 8, 9 y 10, y las métricas de ranking lo reflejan con un
   **descuento por posición**.

De ahí salen las familias de métricas. Las de **corte** (`precision@k`, `recall@k`) miran solo
los primeros `k` puestos. Las **basadas en la posición del acierto** (`MRR`) se fijan en lo
pronto que aparece el primero. Las que **acumulan ganancia** (`MAP`, `NDCG`) recorren toda la
lista sumando aciertos ponderados por lo arriba que están. Y para relevancia **graduada** —no
todo lo relevante lo es igual: un documento perfecto no vale lo mismo que uno aceptable— la
única de la familia que lo aprovecha de forma estándar es `NDCG`.

## Definición formal

Para una consulta `q` con una lista ordenada de `k` resultados y una relevancia
`rel(i) ∈ {0, 1}` (binaria) o `rel(i) ∈ {0, 1, 2, 3}` (graduada) para el resultado en la
posición `i`:

:::formula
Precision@k = (nº de relevantes entre las k primeras) / k
:::

:::formula
Recall@k = (nº de relevantes entre las k primeras) / (nº total de relevantes)
:::

- `Precision@k` mide la pureza de la cabeza; `Recall@k`, cuánto del total has alcanzado. Con un
  catálogo grande y un `k` pequeño, el `recall@k` es necesariamente bajo y no sirve para
  comparar sistemas con distinto número de relevantes.
- `R` — el número total de relevantes de la consulta. Si `R = 0`, la consulta no se puede
  evaluar con estas métricas y se excluye del promedio.

La **precisión media** de una consulta resume la curva de `Precision@k` en los puntos donde
aparece un relevante:

:::formula
AP = (1/R) · Σᵢ [rel(i) = 1] · Precision@i          MAP = (1/Q) · Σ_q AP(q)
:::

- `Q` — número de consultas evaluadas. `MAP` es la media de las `AP`, y da el mismo peso a cada
  consulta por muy distinto que sea su número de relevantes.
- `AP` está pensada para relevancia binaria; con relevancia graduada se usa `NDCG`.

El **rango recíproco** mira solo el primer acierto, y su media sobre consultas es `MRR`:

:::formula
RR(q) = 1 / (posición del primer relevante)          MRR = (1/Q) · Σ_q RR(q)
:::

Si no hay ningún relevante en la lista, `RR = 0`. `MRR` es la métrica adecuada cuando el usuario
necesita **una** respuesta buena («¿cuál es la capital de…?»), no una lista completa.

La **ganancia acumulada descontada** es la métrica que aprovecha la relevancia graduada:

:::formula
DCG@k = Σᵢ₌₁ᵏ (2^rel(i) − 1) / log₂(i + 1)          NDCG@k = DCG@k / IDCG@k
:::

- `2^rel(i) − 1` — la ganancia del resultado: con relevancia 0, 1, 2 y 3 vale 0, 1, 3 y 7. La
  ganancia crece de forma exponencial a propósito: pasar de «aceptable» a «perfecto» vale más
  que pasar de «nada» a «aceptable».
- `log₂(i + 1)` — el descuento por posición. La posición 1 no se descuenta (`log₂2 = 1`), la 2
  divide entre 1,585, la 10 entre 3,459.
- `IDCG@k` — el DCG de la lista ideal, con los mismos resultados ordenados de mejor a peor. Es
  la normalización que permite comparar consultas con distinto número de relevantes.
- `NDCG@k` vale 1 en la lista perfecta y 0 si ninguna ganancia es positiva. Si las ganancias son
  no negativas, `NDCG` siempre está en `[0, 1]`.

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `k` | Cuantos resultados de la cabeza se evaluan | posiciones | La precision@k baja (entran documentos peores) y el recall@k sube (alcanzas mas del total) |
| `rel(i)` | Relevancia del resultado en la posición `i` | 0/1 o grados 0 a 3 | La ganancia de esa posición crece: con `2^rel − 1` pasa de 0 a 1, 3 y 7 |
| `R` | Numero total de relevantes de la consulta | documentos | El recall@k baja con el mismo `k`: hay mas que encontrar y la cabeza no da para tanto |
| `Q` | Numero de consultas promediadas | consultas | MAP y MRR se estabilizan, pero cada consulta pesa menos: una consulta rara deja de mandar |
| `i` | Posición en la lista, empezando en 1 | posiciones | El descuento `1 / log₂(i + 1)` se hace menor: el mismo acierto vale menos cuanto mas abajo esta |
| `NDCG@k` | DCG dividido entre el DCG ideal | tanto por uno, de 0 a 1 | Mas cerca de 1, la lista se parece al orden perfecto; no dice nada del resto del catalogo |
:::

## Ejemplo

Dos consultas, con relevancia binaria (1 = relevante) en listas de 5 posiciones:

```
consulta A   1  0  1  0  1
consulta B   0  1  0  0  0
```

- `Precision@3` de A = 2/3 = 0,667. `Recall@3` de A = 2/3 = 0,667 (hay 3 relevantes en total).
- `AP(A)`: en la posición 1, precisión 1; en la 3, 2/3; en la 5, 3/5. Media:
  `(1 + 0,667 + 0,6) / 3 = 0,7556`.
- `AP(B)`: solo un relevante, en la posición 2, con precisión 1/2. `AP(B) = 0,5`.
- `MAP = (0,7556 + 0,5) / 2 = 0,6278`.
- `MRR`: A acierta en la posición 1 (`1/1`), B en la 2 (`1/2`). `MRR = 0,75`.

Y con relevancia graduada, para una lista con grados `[3, 2, 0, 1]` frente al orden ideal
`[3, 2, 1, 0]`:

```
DCG  = 7/1 + 3/1,585 + 0/2 + 1/2,322 = 7 + 1,893 + 0 + 0,431 = 9,3235
IDCG = 7/1 + 3/1,585 + 1/2 + 0/2,322 = 7 + 1,893 + 0,5 + 0     = 9,3928
NDCG = 9,3235 / 9,3928 = 0,9926
```

Ese 0,9926 dice que la lista está casi en el orden ideal. La misma lista con los grados
`[0, 1, 3, 2]` baja a `0,5774`: los mismos cuatro documentos, la mitad de bien ordenados. Ese
es el punto de `NDCG`: castiga mover un resultado perfecto de la primera posición a la tercera.

:::figura
fichero: metricas-de-ranking-corte-y-orden
pie: El panel izquierdo muestra por qué el corte `k` decide lo que mides: la precisión de la consulta A baja al abrir el corte (cada vez entran documentos peores) mientras su recall sube hasta 1 en la posición 8, y la consulta B, con un solo acierto en la posición 2 sobre 18 relevantes, nunca pasa de un recall bajo. El panel central da la misma lista ordenada de tres maneras y compara las tres familias: MAP y NDCG castigan el hundimiento y el MRR solo mira dónde está el primer acierto. El derecho acumula ganancia con descuento por posición: la curva ideal marca el techo y el hueco entre esa curva y la real, dividido entre la ideal, es el NDCG. Si tu métrica no distingue los tres órdenes del centro, no está midiendo el ranking.
fuente: figuras/metricas-de-ranking-1.py
:::

## Código

```python verificable
import numpy as np

# Dos consultas: 1 si el documento de esa posicion era relevante
consulta_a = np.array([1, 0, 1, 0, 1])
consulta_b = np.array([0, 1, 0, 0, 0])

def ap(rel):
    """Precision media: promedio de la precision en cada acierto."""
    aciertos, suma = 0, 0.0
    # start=1 porque la posicion de la lista empieza en 1: con start=0 el primer
    # acierto dividiria entre cero y Python lanzaria ZeroDivisionError.
    for i, r in enumerate(rel, start=1):
        if r == 1:
            aciertos += 1
            suma += aciertos / i
    return suma / rel.sum()      # numpy.int64: la division ya da float

print(f"precision@3 A {consulta_a[:3].sum() / 3:.4f}")                # -> 0.6667
print(f"recall@3 A    {consulta_a[:3].sum() / consulta_a.sum():.3f}") # -> 0.667
print(f"AP A {ap(consulta_a):.4f}  AP B {ap(consulta_b):.4f}")        # -> AP A 0.7556  AP B 0.5000
print(f"MAP {(ap(consulta_a) + ap(consulta_b)) / 2:.4f}")             # -> 0.6278
print(f"MRR {(1 / 1 + 1 / 2) / 2:.4f}")                               # -> 0.7500
```

:::claves
- `consulta_a[:3]` es una **vista** del array, no una copia, pero como solo la lees (`.sum()`)
  da igual. Lo que importa es que `[:3]` corta **antes** del índice 3: se queda con las
  posiciones 1, 2 y 3 contadas desde uno, que es justo lo que significa el `k` de la métrica.
- `consulta_a.sum()` suma los unos y los ceros, o sea que cuenta los relevantes: el recall se
  calcula dividiendo entre eso y no entre el número de documentos de la lista. Si la lista
  tuviera documentos no anotados, ese denominador sería mentira.
- `enumerate(rel, start=1)` es lo que hace que la posición empiece en 1 y no en 0. Con
  `start=0` la primera posición valdría `1/0` y Python lanzaría
  `ZeroDivisionError: division by zero` en vez de devolver un número: ese argumento no es
  decorativo, es la diferencia entre un número y un error.
- `if r == 1:` solo cuenta la relevancia binaria. Con grados (0, 1, 2, 3) esa condición ignora
  los aciertos parciales y el AP sale mas bajo de lo que debería: para relevancia graduada se
  usa la otra función, la del DCG.
- `suma / rel.sum()` divide entre **numpy.int64**, así que devuelve un `numpy.float64` y no un
  `float`. Se imprime igual, pero si el array fuera de enteros y la suma diera un valor exacto,
  seguirias teniendo coma flotante y errores de redondeo del orden de `1e-16`.
- En `dcg`, `np.arange(2, g.size + 2)` genera `2, 3, 4, …` porque el descuento de la posición
  `i` es `log₂(i + 1)`. Si empezara en 1, la primera posición se dividiría entre `log₂(1) = 0` y
  el DCG se iría a infinito (NumPy avisa con un `RuntimeWarning`), y la segunda pasaría de
  dividir entre 1,585 a dividir entre 1,0: el mismo código con otro orden.
- `sorted(bueno, reverse=True)` ordena los grados, no los documentos: el `IDCG` es el techo
  teorico con esos mismos grados. Si calcularas el ideal con grados distintos, el NDCG podría
  pasar de 1 y dejaria de ser una proporción.
:::

```python verificable
import numpy as np

# Relevancia graduada: 0 = nada, 1 = util, 2 = bueno, 3 = perfecto
def dcg(grados, k=None):
    g = np.asarray(grados[:k], dtype=float)
    # np.arange(2, ...) porque el descuento de la posicion i es log2(i + 1): la
    # primera posicion se divide entre log2(2) = 1, o sea que no se descuenta.
    descuento = 1.0 / np.log2(np.arange(2, g.size + 2))
    return float((((2 ** g) - 1) * descuento).sum())

bueno = [3, 2, 0, 1]
malo = [0, 1, 3, 2]
ideal = sorted(bueno, reverse=True)   # el mejor orden posible con esos mismos grados

print(f"DCG bueno {dcg(bueno):.4f}")                 # -> 9.3235
print(f"IDCG      {dcg(ideal):.4f}")                 # -> 9.3928
print(f"NDCG bueno {dcg(bueno) / dcg(ideal):.4f}")   # -> 0.9926
print(f"NDCG malo  {dcg(malo) / dcg(ideal):.4f}")    # -> 0.5774
print(f"DCG@2 bueno {dcg(bueno, k=2):.4f}")          # -> 8.8928
```

## Errores típicos

- **Evaluar con datos sesgados o incompletos.** Si tu catálogo tiene un millón de documentos y
  solo juzgaste 50, la métrica mide tu esfuerzo de anotación, no el sistema: los no anotados no
  son «no relevantes». Y si los juicios vienen de clics, el usuario pincha lo que está arriba
  porque está arriba. Anota una muestra aleatoria y corrige el sesgo de posición.
- **Usar exactitud, precisión o AUC de clasificación tal cual.** En ranking no hay verdaderos
  negativos observables y el orden forma parte del resultado. Con `precision@k` te refieres a la
  pureza de la cabeza, que es otra cosa que la precisión de un clasificador.
- **Comparar NDCG calculado con convenciones distintas.** Cambiar la ganancia (`2^rel − 1` frente
  a `rel`), el logaritmo o el `k` cambia el número. Fija la convención y publícala con el
  resultado.
- **Elegir mal la métrica según la forma del catálogo.** Con muchísimos relevantes por consulta,
  `recall@5` es siempre bajo y engaña; con una sola respuesta correcta, `MAP` diluye lo que
  importa y `MRR` lo captura mejor. Y como `MAP` da el mismo peso a cada consulta, una con un
  solo relevante puede dominar el promedio: reporta también cuántos relevantes tiene cada una.
- **Ajustar `k` o el número de resultados mirando el conjunto de prueba.** `k` es una decisión
  del sistema: se elige en validación, igual que un umbral ([[umbrales-y-coste]]).
- **No desempatar de forma explícita.** Si 300 candidatos comparten la misma puntuación en la
  frontera del puesto 10, el orden que devuelva tu código decide la métrica. Fija el desempate
  y documenta la regla.

:::practica
enunciado: Un buscador devuelve cinco resultados con relevancia, de arriba abajo: 0, 1, 0, 1, 1. Calcula Precision@3, el AP de la consulta y el RR.
pista: En cada acierto, la precisión es aciertos acumulados entre la posición; el AP promedia esas precisiones solo donde hay relevante y el RR mira solo el primero.
solucion: En las tres primeras posiciones solo hay un relevante: Precision@3 = 1/3 = 0,333. Las precisiones en cada acierto son 1/2 = 0,5 en la posición 2, 2/4 = 0,5 en la 4 y 3/5 = 0,6 en la 5. AP = (0,5 + 0,5 + 0,6)/3 = 1,6/3 = 0,533. El primer relevante está en la posición 2, así que RR = 1/2 = 0,5.
:::

## Comprueba que lo sabes

:::quiz
p: Dos listas tienen los tres documentos relevantes en el mismo conjunto de resultados, pero una los coloca en las posiciones 1, 2 y 3 y la otra en las 8, 9 y 10. ¿Qué métricas lo distinguen?
o: Precision@3 y recall@3, que serían iguales en las dos
o: NDCG y MAP, porque descuentan o ponderan según la posición
o: Ninguna, porque contienen los mismos aciertos
a: 2
e: Las métricas de corte miran solo las k primeras posiciones y pueden no ver la diferencia; las que acumulan ganancia con descuento por posición (NDCG) o que promedian la precisión en cada acierto (AP y MAP) sí la reflejan.
:::

:::quiz
p: El catálogo tiene un millón de documentos y solo has anotado la relevancia de los 50 que mostrabas. ¿Qué problema tiene el MAP que calcules con eso?
o: Ninguno, si el sistema mostró sus mejores 50 candidatos
o: Que los documentos no anotados se tratan como no relevantes, así que el resultado mide tu anotación y no la calidad del sistema
o: Que el MAP solo funciona con relevancia graduada
a: 2
e: La ausencia de anotación no es ausencia de relevancia. Con solo los mostrados anotados, el sistema siempre parece haber encontrado todo lo que había. La solución es anotar una muestra aleatoria del catálogo para tener una base con la que comparar.
:::

:::aviso
Estas métricas asumen que tienes juicios de relevancia fiables. En un sistema con
recomendaciones, esos juicios suelen venir de la interacción pasada, que está sesgada por lo que
el sistema ya mostraba. Es el bucle de realimentación: el modelo aprende de los datos que él
mismo generó y la métrica premia repetir lo de siempre.
:::
