---
id: umbrales-y-coste
titulo: Umbrales y coste del error
fase: 6
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [roc-auc, matriz-de-confusion, metricas-de-clasificacion]
tags: [decision, coste, umbral, negocio]
resumen: El 0,5 es una convención, no una decisión: el punto de corte correcto sale del coste real de cada falso positivo y cada falso negativo.
fuentes: ["Elkan (2001), 'The Foundations of Cost-Sensitive Learning'", "Hernández-Orallo, Flach y Ferri (2012), 'A unified view of performance metrics: translating threshold choice into expected classification loss'"]
---

## En una frase

Elegir un umbral es elegir cuántos falsos positivos estás dispuesto a pagar para reducir los
falsos negativos, y la respuesta solo la da el coste de cada error, no una regla del 0,5.

## La idea

Todos los clasificadores que devuelven una puntuación necesitan un punto de corte, y casi todo
el mundo usa 0,5 por costumbre. Ese número no significa nada. Viene de suponer que los dos
errores cuestan lo mismo, que es justo lo que casi nunca ocurre.

Piensa en una campaña para retener clientes. Llamar a alguien cuesta 5 € (el tiempo del agente).
Si ese cliente se iba a marchar y la llamada lo evita, salvas 150 € de margen. ¿A partir de qué
probabilidad de fuga merece la pena descolgar el teléfono? Si el modelo dice 0,04, la llamada
cuesta 5 € y el valor esperado de salvar al cliente es `0,04 · 150 = 6 €`: sale a cuenta. Con
0,5 estarías dejando marchar a muchísima gente rentable de salvar.

La regla es siempre la misma y se deduce en dos líneas. Si actúas sobre un caso cuya probabilidad
de ser positivo es `p`, pagas el coste del falso positivo con probabilidad `1 − p`; si no
actúas, pagas el coste del falso negativo con probabilidad `p`. Actúas cuando

```
(1 − p) · c_FP  ≤  p · c_FN        ->        p  ≥  c_FP / (c_FP + c_FN)
```

donde `c_FP` es lo que cuesta un falso positivo y `c_FN` lo que cuesta un falso negativo. Con
costes iguales sale 0,5, que es de donde viene la convención. Con `c_FP = 5` y `c_FN = 150`, el
umbral es `5/155 = 0,032`.

Hay un requisito que se olvida con frecuencia: **la fórmula necesita probabilidades
calibradas**. Si tu modelo dice 0,9 cuando la frecuencia real es 0,6, el umbral que calculas no
es el que aplicas. Sin [[calibracion]], la vía práctica es otra: barrer umbrales sobre un
conjunto de validación, calcular el coste total en cada uno y quedarte con el mínimo. Lo que
nunca vale es barrer umbrales sobre el conjunto de prueba: el umbral es una decisión más del
modelo y se elige antes de mirar el dato final.

Dos complicaciones que aparecen en cuanto el problema es real:

1. **El coste depende del caso.** Un fraude de 12 € y otro de 4.000 € no merecen el mismo
   umbral. Lo correcto no es un corte sobre la probabilidad, sino actuar cuando
   `p · importe > (1 − p) · c_FP`: un umbral efectivo distinto por caso. Un único 0,8 global es
   una simplificación cómoda y cara.
2. **La capacidad es finita.** Si solo hay dos analistas y pueden revisar 40 casos al día, no
   tienes un umbral: tienes un presupuesto. La regla pasa a ser «los 40 mejor puntuados», que es
   lo que se mide con [[metricas-de-ranking]].

## Definición formal

Sea `τ` el umbral, `FP(τ)` y `FN(τ)` los recuentos de la [[matriz-de-confusion]] al predecir
positivo todo lo que puntúa por encima de `τ`, y `N` el número de casos:

:::formula
Coste(τ) = c_FP · FP(τ) + c_FN · FN(τ)
:::

- `c_FP` — coste de un falso positivo, en la unidad que elijas (euros, minutos, clientes
  perdidos).
- `c_FN` — coste de un falso negativo, en la misma unidad.
- El **coste por caso** es `Coste(τ) / N`; sirve para comparar entre conjuntos de distinto
  tamaño y para decidir si el sistema merece la pena antes de construirlo.

Con probabilidades calibradas, el umbral que minimiza el coste esperado es:

:::formula
τ* = c_FP / (c_FP + c_FN)
:::

- Si `c_FN` es mucho mayor que `c_FP` (dejar pasar un fraude grave), `τ*` tiende a 0: actúas
  ante la mínima sospecha.
- Si `c_FP` domina (molestar a un cliente es carísimo), `τ*` tiende a 1: solo actúas con
  evidencia abrumadora.
- Con `c_FP = c_FN`, `τ* = 0,5`. Es el único caso en que la convención acierta.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `c_FP` | Lo que te cuesta un falso positivo: una alerta que no era nada | la unidad de coste que elijas (€, minutos, clientes) | Sube el umbral óptimo `τ*`: te vuelves más exigente antes de actuar |
| `c_FN` | Lo que te cuesta un falso negativo: el caso que se te escapó | la misma unidad que `c_FP` | Baja el umbral óptimo: actúas ante la mínima sospecha |
| `FP(τ)`, `FN(τ)` | Los recuentos de la matriz al predecir positivo todo lo que supera `τ` | casos | Cada `FP` suma `c_FP` al coste y cada `FN` suma `c_FN` |
| `Coste(τ)` | La suma de los dos errores, cada uno ponderado por lo que cuesta | la unidad de coste | No «sube» solo: es lo que se minimiza barriendo `τ` |
| `N` | Número de casos evaluados | casos | El coste total crece en proporción; el coste por caso no cambia |
| `τ` | Umbral de decisión | las de la puntuación | Sube: menos `FP` y más `FN`, y al revés al bajarlo |
| `τ*` | El umbral que minimiza el coste esperado, si las probabilidades están calibradas | adimensional, entre 0 y 1 | Sube si sube `c_FP` o si baja `c_FN`; con los dos iguales vale 0,5 |
| `c_rev` | Lo que cuesta revisar un caso a mano, la tercera acción posible | la unidad de coste | Si baja, compensa revisar más casos y el umbral único pierde parte de su valor |
:::

La **curva de coste** dibuja `Coste(τ) / N` frente a la probabilidad umbral, con una recta
diagonal de referencia que representa al clasificador que no discrimina. Su utilidad es doble:
localiza el mínimo y enseña cuánto se pierde por no elegir bien (el coste de la indecisión).

:::figura
fichero: umbral-curva-de-coste
pie: A la izquierda, el coste total frente al umbral sobre 2.001 casos cuyas etiquetas se generaron a partir de su propia probabilidad (por eso el modelo está calibrado, que es el supuesto de la fórmula). La curva tiene un único mínimo en 0,015 con 2.862 €, justo donde cae la línea del umbral teórico, y a partir de ahí crece: en el 0,5 de la convención el coste se multiplica por diecinueve. A la derecha, de dónde sale ese número: cuanto más caro es el falso negativo respecto a la falsa alarma, más se acerca el corte a cero, y solo empata a 0,5 cuando los dos errores cuestan lo mismo. Conclusión: barre umbrales sobre validación y quédate con el mínimo; el 0,5 solo es correcto si los dos errores te cuestan igual.
fuente: figuras/umbrales-y-coste-1.py
:::

Tercera posibilidad, la **abstención**: añadir una acción intermedia («revisar a mano») con su
propio coste `c_rev`, y decidir positivo, negativo o revisar según cuál de los tres esperados sea
menor. Es lo que hacen los sistemas de fraude con una cola de revisión humana, y suele batir
cualquier umbral único.

## Ejemplo

Doce alertas de fraude ordenadas por puntuación, con `c_FP = 3 €` (bloquear una compra legítima y
disculparse) y `c_FN = 200 €` (el importe del fraude):

```
puntuacion  0,97  0,91  0,88  0,72  0,65  0,61  0,44  0,39  0,30  0,25  0,12  0,04
era fraude     s     n     n     s     n     s     n     n     n     s     n     n
```

Barriendo umbrales:

| Umbral | Alertas | FP | FN | Coste |
| --- | --- | --- | --- | --- |
| 0,95 | 1 | 0 | 3 | 600 € |
| 0,75 | 3 | 2 | 3 | 606 € |
| 0,50 | 6 | 3 | 1 | 209 € |
| 0,25 | 10 | 6 | 0 | 18 € |
| 0,00 | 12 | 8 | 0 | 24 € |

El mínimo está en 0,25, no en 0,5: el umbral de la convención cuesta 209 € y el elegido por
coste, 18 €. Casi doce veces menos, con el mismo modelo. Con 0,00 también se capturan los cuatro
fraudes, pero cada alerta de más cuesta 3 € y ya no compensa.

La fórmula teórica dice `τ* = 3/203 = 0,0148`, que está cerca de 0,00 y no de 0,25. La
diferencia es informativa: este modelo no está calibrado y, sobre todo, sus puntuaciones no
están repartidas como si lo estuvieran. En la práctica el barrido empírico manda; la fórmula
sirve para entender la dirección del ajuste y para detectar cuándo tu umbral elegido está a
años luz del que dictan los costes.

## Código

```python verificable
import numpy as np

# Doce alertas ordenadas por puntuacion. y = 1 si el caso era realmente un fraude.
y = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0])
score = np.array([0.97, 0.91, 0.88, 0.72, 0.65, 0.61,
                  0.44, 0.39, 0.30, 0.25, 0.12, 0.04])

c_fp, c_fn = 3.0, 200.0   # bloquear una compra legitima / dejar pasar un fraude

for umbral in (0.95, 0.75, 0.50, 0.25, 0.00):
    pred = score >= umbral
    # Con arrays se usa & y no `and`; los parentesis de cada comparacion son obligatorios.
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    # :>2 y :>6.0f son anchos de campo: alinean a la derecha en 2 y 6 caracteres para que
    # las columnas de la salida queden a plomo. No redondean los calculos, solo el texto.
    print(f"umbral {umbral:.2f}  alertas {int(pred.sum()):>2}  "
          f"FP {fp:>2}  FN {fn:>2}  coste {c_fp * fp + c_fn * fn:>6.0f}")
```

:::claves
- `pred = score >= umbral` es una **máscara booleana**, no una lista de casos: `int(pred.sum())` cuenta cuántos han pasado el corte porque `True` vale 1 al sumar.
- Ojo con `y == 0` y `(pred == 1)`: comparar con 1 una máscara que ya es booleana funciona, pero lo que se está contando de verdad es `pred & (y == 0)`. Si las etiquetas fueran texto («fraude»/«no»), esa comparación cambiaría de sentido y habría que reescribirla.
- El umbral 0,00 marca todo: con `>=`, un caso con puntuación exactamente 0,00 también entra. Ese detalle decide si el último caso de la lista se marca o no, y con él la última fila de la tabla.
- `rng.random(p.size) < p` del segundo bloque **fabrica las etiquetas a partir de la propia probabilidad**: cada caso es positivo con probabilidad `p`, así que el modelo está calibrado por construcción. Es la forma de comprobar la fórmula teórica sin depender de un modelo real.
- `~pred` es la negación de una máscara booleana (`~`), no `not pred`: `not` sobre un array lanza «the truth value of an array is ambiguous».
- `np.argmin(costes)` devuelve la **posición** del mínimo, no el valor: por eso el umbral empírico se lee con `umbrales[int(np.argmin(costes))]`. Confundir posición y valor es el error clásico con `argmin` y `argmax`.
:::

```python verificable
import numpy as np

# Con probabilidades calibradas el minimo teorico es c_fp / (c_fp + c_fn).
# Lo comprobamos generando las etiquetas a partir de la propia probabilidad.
rng = np.random.default_rng(7)
p = np.linspace(0.0, 1.0, 2001)
# Cada caso sale positivo con probabilidad p: ese es el modelo perfectamente calibrado.
# .astype(float) deja las etiquetas en 0.0 y 1.0 para que las comparaciones sean numericas.
y = (rng.random(p.size) < p).astype(float)

c_fp, c_fn = 3.0, 200.0
umbrales = np.linspace(0.0, 0.60, 121)
costes = []
for t in umbrales:
    pred = p >= t
    fp = int((pred & (y == 0)).sum())
    fn = int((~pred & (y == 1)).sum())      # ~pred es la mascara contraria, no `not pred`
    costes.append(c_fp * fp + c_fn * fn)

print(f"umbral teorico  {c_fp / (c_fp + c_fn):.4f}")               # -> 0.0148
# argmin da la POSICION del minimo: hay que indexar umbrales con ella para ver el valor.
print(f"umbral empirico {float(umbrales[int(np.argmin(costes))]):.4f}")  # -> 0.0150
print(f"coste minimo    {min(costes):.0f} EUR")                   # -> 2862 EUR
```

## Errores típicos

- **Dejar el umbral en 0,5 porque es el valor por defecto de la librería.** `predict()` te da la
  decisión de 0,5 y casi nunca es la tuya. Usa `predict_proba` y decide tú.
- **Aplicar `τ* = c_FP / (c_FP + c_FN)` sin comprobar sus dos supuestos.** La fórmula supone que
  `p` es una probabilidad real (si el modelo exagera la confianza en la zona alta, el umbral
  calculado te deja fuera la mitad de los casos) y que el coste es el mismo en todos los casos
  (con importes que van de 5 € a 5.000 €, el corte depende del importe: compara `p · importe` con
  `(1 − p) · c_FP`).
- **Elegir el umbral con el conjunto de prueba.** Es la forma más discreta de fuga de datos:
  parece que solo has tocado un número, pero ese número está ajustado al ruido del conjunto que
  luego usas para presumir de resultado. Elige el umbral en validación.
- **Optimizar el F1 en vez del coste.** F1 trata los dos errores como iguales. Si `c_FP` y
  `c_FN` difieren en un factor 50, maximizar F1 es optimizar una función de utilidad que no es
  la tuya, y la diferencia se mide en dinero.
- **Ignorar la capacidad de revisión y los empates.** Con 40 revisiones al día, el umbral
  «teórico» puede mandarte 300 casos que nadie va a mirar. Y si 500 candidatos comparten
  puntuación en la frontera del puesto 40, el orden que ponga tu código decide quién entra:
  fija un desempate explícito.
- **Trabajar con costes caducados.** El coste de una falsa alarma cambia con el precio del
  soporte y la paciencia del cliente. Si el umbral no se revisa, envejece.

:::practica
enunciado: Ocho alertas ordenadas por puntuación —0,90 0,80 0,70 0,60 0,50 0,40 0,30 0,20— con etiquetas sí, no, sí, no, no, sí, no, no. Una falsa alarma cuesta 20 € y un fraude no detectado, 180 €. Halla el coste con umbral 0,5 y con 0,3.
pista: Cuenta cuántas alertas dispara cada umbral y cuántos fraudes quedan fuera; el coste suma los dos errores ponderados, no los aciertos.
solucion: Con 0,5 se marcan las cinco primeras: 2 fraudes, 3 falsas alarmas y el fraude de 0,40 fuera. Coste = 3 · 20 + 1 · 180 = 240 €. Con 0,3 se marcan siete, con los 3 fraudes dentro y 4 falsas alarmas: 4 · 20 + 0 · 180 = 80 €. Bajar el corte ahorra 160 €, así que compensa el umbral bajo.
:::

## Comprueba que lo sabes

:::quiz
p: Retener a un cliente que se iba vale 150 € y una llamada cuesta 5 €. ¿Qué umbral de probabilidad de fuga usa la regla de coste esperado?
o: 0,5, porque es el punto neutro
o: 5 / 155, es decir, 0,032
o: 150 / 155, es decir, 0,968
a: 2
e: El umbral es c_FP / (c_FP + c_FN) = 5 / (5 + 150) = 0,032: llamas en cuanto la probabilidad de fuga supera el 3,2 %. La última opción sería el umbral si el error caro fuera llamar a quien no se iba, que es justo al revés.
:::

:::quiz
p: ¿Por qué el umbral que minimiza el coste no se elige sobre el conjunto de prueba?
o: Porque el conjunto de prueba es demasiado pequeño para estimar costes
o: Porque el umbral queda ajustado al ruido de ese conjunto y deja de ser una estimación honesta del rendimiento
o: Porque el coste solo se puede calcular sobre entrenamiento
a: 2
e: El umbral es un parámetro más del sistema. Elegirlo mirando el test contamina la evaluación igual que elegir el modelo mirando el test. Se elige sobre validación y se reporta el coste sobre el test, una sola vez.
:::

:::trampa
Un umbral bajo que captura casi todo suena bien hasta que sumas el coste de las falsas alarmas.
Con `c_FP = 3` y `c_FN = 200`, bajar el umbral de 0,25 a 0,00 en el ejemplo captura los mismos
fraudes y cuesta 6 € más. Y con `c_FP = 50`, la diferencia se dispara. Antes de presumir de
exhaustividad, multiplica.
:::
