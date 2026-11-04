---
id: reglas-de-asociacion
titulo: Reglas de asociación
fase: 6
nivel: intermedio
rutas: [de, ds]
prerequisitos: [probabilidad-condicional, sql-agregaciones-y-group-by]
tags: [cesta, apriori, soporte, retail]
resumen: Convertir millones de tickets en reglas del tipo «quien compra pan compra mantequilla», con el lift como único número que distingue un hallazgo de una obviedad.
fuentes: ["Agrawal, Imielinski y Swami (1993), 'Mining Association Rules between Sets of Items in Large Databases'", "Han, Pei y Yin (2000), 'Mining Frequent Patterns without Candidate Generation'"]
---

## En una frase

Las reglas de asociación buscan combinaciones de artículos que aparecen juntos en las cestas más
de lo que cabría esperar por azar, y lo resumen con tres números: soporte (cuánto aparece),
confianza (qué proporción de las veces que está A también está B) y lift (cuánto más de lo
normal).

## La idea

Todo el mundo conoce el ejemplo del pañal y la cerveza: un estudio de cestas de la compra
encontró que los padres que compraban pañales compraban cerveza el viernes por la noche. Sea
verdad o leyenda urbana, el ejemplo describe la promesa de estas reglas y también su trampa: una
regla puede ser cierta y completamente inútil. Si el 60 % de los clientes compra cerveza, que el
70 % de los que compran pañales la compre es casi nada; si solo la compra el 8 % del total, ese
70 % es un hallazgo.

De ahí los tres números y por qué hacen falta los tres:

- **Soporte**: qué parte de las cestas contiene el conjunto. Un soporte del 0,1 % puede ser
  interesante o puede ser tan raro que solo sean cuatro tickets de un mismo barrio.
- **Confianza**: de las cestas con A, cuántas llevan B. Es una [[probabilidad-condicional]]: la
  probabilidad de B entre las cestas que llevan A. Alta confianza significa que la regla acierta
  mucho, no que sea útil.
- **Lift**: cuántas veces más probable es B entre los que compran A que en el total. Un lift de
  1 es independencia pura, por debajo de 1 los artículos se repelen (quien compra pan compra
  menos leche de lo normal) y por encima de 1 hay asociación positiva.

El algoritmo clásico, **Apriori**, explota una propiedad sencilla: si un conjunto de tres
artículos es frecuente, sus tres pares también lo son. Y al revés, si un par no llega al soporte
mínimo, ningún conjunto que lo contenga puede llegar. Así se poda el espacio de combinaciones
(cada artículo nuevo multiplica las posibilidades) en lugar de probarlas todas. **FP-Growth**
evita generar candidatos: comprime la base de datos en un árbol y lo recorre.

Un aviso que ahorra disgustos: en un supermercado con 20.000 referencias, el número de pares
posibles es de 200 millones. Apriori no los enumera todos, pero sigue siendo sensible al umbral
de soporte: bajarlo un poco puede multiplicar el tiempo de cómputo por diez.

## Definición formal

Sea `T` el conjunto de cestas (cada una, un conjunto de artículos) y `|T|` el número de cestas.
Para un conjunto de artículos `X`:

:::formula
soporte(X) = |{ t ∈ T : X ⊆ t }| / |T|
:::

- `X ⊆ t` — el conjunto `X` está contenido en la cesta `t`.
- `soporte(X)` — la fracción de cestas que contienen todos los artículos de `X`. Se le llama
  también *frecuencia relativa*.

Para una regla `A → B`, con `A` y `B` conjuntos disjuntos de artículos:

:::formula
soporte(A → B) = soporte(A ∪ B)
:::

:::formula
confianza(A → B) = soporte(A ∪ B) / soporte(A) = P(B | A)
:::

:::formula
lift(A → B) = confianza(A → B) / soporte(B) = soporte(A ∪ B) / ( soporte(A) · soporte(B) )
:::

- `confianza` — proporción de cestas con `A` que también tienen `B`. **No es simétrica**:
  `confianza(A → B)` y `confianza(B → A)` son distintas salvo casualidad.
- `soporte(B)` — la probabilidad de `B` sin condiciones, que es la referencia del azar.
- `lift = 1` significa que `A` y `B` son independientes; `lift > 1`, que aparecen juntos más de
  lo esperado; `lift < 1`, menos.
- Otras medidas habituales: `leverage = soporte(A∪B) − soporte(A)·soporte(B)` (la diferencia en
  puntos porcentuales) y `convicción = (1 − soporte(B)) / (1 − confianza)`, que se dispara al
  infinito cuando la confianza llega a 1.

El flujo de Apriori en tres pasos: (1) contar los artículos individuales y quedarse con los que
superan el soporte mínimo; (2) combinar los frecuentes de tamaño `k` para proponer candidatos de
tamaño `k+1` y podar los que contienen algún subconjunto no frecuente; (3) repetir hasta que no
queden candidatos. Después, de cada conjunto frecuente se extraen las reglas que superan la
confianza mínima.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T` | Conjunto de cestas (tickets) con el que se calcula todo | cestas | Con más cestas, los mismos soportes se estiman con menos ruido: una regla del 0,1 % deja de depender de cuatro tickets sueltos |
| `soporte(X)` | Fracción de cestas que contienen todos los artículos de `X` | proporción (0-1) | La regla describe a más gente, pero también es más fácil que sea una obviedad: los artículos muy populares tienen soporte alto por definición |
| `soporte(A → B)` | Soporte del conjunto `A ∪ B` | proporción (0-1) | Es la cobertura de la regla: sube cuando los dos artículos se compran juntos, sin decir nada todavía de si la relación es real |
| `confianza(A → B)` | Proporción de cestas con `A` que también llevan `B` | proporción (0-1) | Acierta más veces, pero **no** implica que la regla valga más: si `B` ya era frecuente, la confianza alta es puro reflejo de su popularidad |
| `lift(A → B)` | Veces que `B` es más probable entre las cestas con `A` que en el total | adimensional | Por encima de 1 hay asociación positiva, 1 es independencia y por debajo de 1 los artículos se repelen. Es el único de los tres que compara con el azar |
| `leverage` | Diferencia en puntos entre el soporte conjunto y el esperado por azar | proporción (0-1) | Mide lo mismo que el lift pero en puntos porcentuales: sube cuando la regla aporta sobre la independencia, y no se dispara con soportes diminutos |
| `convicción` | Cuántas veces más probable es que `A` aparezca sin `B` de lo que fallaría la regla | adimensional | Al subir la confianza hacia 1, la convicción se dispara hacia infinito: es la medida más inestable de las cuatro |
| `soporte mínimo` | Umbral por debajo del cual un conjunto no se considera frecuente | proporción (0-1) | **Bajarlo multiplica los conjuntos frecuentes** y el tiempo de cómputo: en el ejemplo de la figura, de 0,010 a 0,002 pasa de 260 a 2 479 pares |
| `confianza mínima` | Umbral para quedarse con una regla de un conjunto frecuente | proporción (0-1) | Subirlo deja menos reglas y más fiables una a una, pero sesga el resultado hacia los artículos populares: es el filtro que hay que mirar al final, no el primero |
:::

## Ejemplo

Mil tickets de supermercado. Pan en 200 (el 20 %), mantequilla en 100 (el 10 %) y las dos cosas
en 80 (el 8 %). La regla `pan → mantequilla`:

- Soporte: `80 / 1000 = 0,080`. Un 8 % de las cestas llevan las dos cosas.
- Confianza: `80 / 200 = 0,400`. De cada 100 clientes que compran pan, 40 compran mantequilla.
- Lift: `0,400 / 0,100 = 4,00`. Comprar pan multiplica por cuatro la probabilidad de llevarse
  mantequilla. La regla es real.

Contrasta con dos casos que enseñan más que el anterior:

- **Confianza alta, lift bajo.** Café en 600 tickets (60 %), azúcar en 500 (50 %) y juntos en 400
  (40 %). La confianza de `café → azúcar` es `400 / 600 = 0,667`, altísima. Pero el lift es
  `0,667 / 0,500 = 1,33`: quien compra café ya tenía un 50 % de probabilidad de comprar azúcar
  sin saber nada de él. La regla añade poco. Si ordenas por confianza, esta regla te tapa a la
  del pan.
- **Lift por debajo de 1.** Pan en 200, leche en 300 y juntos en 30. La confianza de
  `pan → leche` es `30 / 200 = 0,15` y el lift `0,15 / 0,30 = 0,50`: entre los que compran pan,
  la leche es **la mitad** de probable que en el conjunto. Hay una asociación negativa, y eso
  también es un hallazgo (suele indicar productos sustitutivos o perfiles de cliente distintos).

Regla práctica para leer el resultado: filtra primero por soporte mínimo (para que la regla
describa a mucha gente), ordena después por lift (para que no sea obvia) y mira la confianza
solo al final, para saber con qué frecuencia acierta.

:::figura
fichero: reglas-soporte-confianza-lift
pie: El panel izquierdo compara cada regla con lo que ya pasaba sin ella: la barra naranja es la probabilidad de B en el conjunto y la azul, la de B entre las cestas que llevan A. El lift es el cociente entre las dos, y ahí se ve lo que la confianza sola esconde. Café → azúcar acierta el 66,7 % de las veces, pero solo multiplica por 1,33 una probabilidad que ya era del 50 %; pan → mantequilla acierta menos (40 %) y multiplica por 4. Y en pan → leche la confianza cae por debajo del azar (0,15 frente a 0,30), con un lift de 0,5 que también es un hallazgo: indica productos sustitutivos o perfiles de cliente distintos. Ordenar por confianza pondría la regla del café la primera y taparía las otras dos. El panel derecho explica el otro mando, el soporte mínimo: en 20 000 cestas simuladas de 300 artículos, bajarlo de 0,010 a 0,002 multiplica los pares frecuentes de 260 a 2 479 y se acerca al techo de todos los pares posibles. Bajar el umbral no encuentra cosas mejores: encuentra lo mismo más el ruido, y a un coste que crece mucho más deprisa que el número de reglas útiles.
fuente: figuras/reglas-de-asociacion-1.py
:::

## Código

```python verificable
import numpy as np

tickets = 1000
pan, mantequilla, pan_y_mantequilla = 200, 100, 80
leche, pan_y_leche, cafe, azucar, cafe_y_azucar = 300, 30, 600, 500, 400

def regla(n_xy, n_x, n_y, total):
    """n_xy: cestas con los dos; n_x: con el antecedente; n_y: con el consecuente."""
    soporte = n_xy / total
    confianza = n_xy / n_x
    lift = confianza / (n_y / total)         # compara con el azar, no con el antecedente
    return soporte, confianza, lift

for nombre, args in [("pan -> mantequilla", (pan_y_mantequilla, pan, mantequilla, tickets)),
                     ("cafe -> azucar", (cafe_y_azucar, cafe, azucar, tickets)),
                     ("pan -> leche", (pan_y_leche, pan, leche, tickets))]:
    s, c, l = regla(*args)                   # *args reparte la tupla en los cuatro argumentos
    print(f"{nombre:18s} soporte {s:.3f}  confianza {c:.3f}  lift {l:.3f}")
# -> pan -> mantequilla soporte 0.080  confianza 0.400  lift 4.000
# -> cafe -> azucar     soporte 0.400  confianza 0.667  lift 1.333
# -> pan -> leche       soporte 0.030  confianza 0.150  lift 0.500
```

:::claves
- `regla()` devuelve una **tupla** de tres números y el bucle la desempaqueta con
  `s, c, l = regla(*args)`. El `*args` reparte la tupla de argumentos en los cuatro parámetros.
  Si en lugar de desempaquetar guardas el retorno entero, `s` valdría `(0.08, 0.4, 4.0)` y el
  formato `{s:.3f}` fallaría con un error de tipo, no con un número raro.
- `lift = confianza / (n_y / total)` divide entre el **soporte de B**, no entre otra confianza. Es
  la diferencia entre «acierta mucho» y «aporta algo». Y es simétrico: `lift(A → B)` y
  `lift(B → A)` valen lo mismo, porque se calculan con el mismo par; la confianza no lo es, y por
  eso dos reglas con el mismo lift pueden tener confianzas muy distintas (0,667 y 0,15 en el
  ejemplo).
- `f"{nombre:18s} soporte {s:.3f}"` alinea el nombre a 18 caracteres y redondea a tres decimales
  **solo al imprimir**: el número guardado conserva todos los decimales. Comparar dos lifts por lo
  que se ve en pantalla es comparar redondeos.
- En el bloque SQL, `count(DISTINCT ticket)` no es lo mismo que `count(*)`: un ticket con el mismo
  artículo repetido contaría dos veces y el soporte saldría inflado. La condición
  `a.articulo < b.articulo` hace dos cosas a la vez: evita contar cada par dos veces (una por cada
  orden) y elimina el par de un artículo consigo mismo.
- `JOIN total ON true` es un producto cruzado deliberado contra una tabla de una sola fila: sirve
  para tener el total de tickets disponible en cada fila. Con más de una fila en `total`, cada par
  se multiplicaría por el número de filas.
- `par.n_par * 1.0 / item_x.n_item` multiplica por 1.0 para forzar la división decimal. En SQL,
  dividir un entero entre un entero puede dar un entero: sin ese truco, un soporte de 0,08 se
  quedaría en 0 y la regla desaparecería del informe.
:::

El segundo bloque hace lo mismo en SQL, que es como se calcula de verdad: contando cestas
distintas, no filas, porque un ticket con el mismo artículo repetido no debe contar dos veces.

```sql verificable
-- Cesta de la compra: tickets resumidos y asociaciones entre pares de articulos.
CREATE TABLE tickets AS
SELECT * FROM (VALUES
    (1, 'pan'), (1, 'mantequilla'), (1, 'leche'),
    (2, 'pan'), (2, 'mantequilla'),
    (3, 'pan'), (3, 'leche'),
    (4, 'pan'), (4, 'mantequilla'),
    (5, 'leche'), (5, 'cafe')
) AS t(ticket, articulo);

WITH total AS (SELECT count(DISTINCT ticket) AS n FROM tickets),
     item AS (SELECT articulo, count(DISTINCT ticket) AS n_item FROM tickets GROUP BY articulo),
     par AS (
        SELECT a.articulo AS x, b.articulo AS y, count(DISTINCT a.ticket) AS n_par
        FROM tickets a
        JOIN tickets b ON a.ticket = b.ticket AND a.articulo < b.articulo  -- el < quita el par repetido
        GROUP BY a.articulo, b.articulo
     )
SELECT par.x, par.y,
       round(par.n_par / total.n, 3) AS soporte,
       round(par.n_par * 1.0 / item_x.n_item, 3) AS confianza,
       round((par.n_par * 1.0 / item_x.n_item) / (item_y.n_item * 1.0 / total.n), 3) AS lift
FROM par
JOIN total ON true
JOIN item AS item_x ON item_x.articulo = par.x
JOIN item AS item_y ON item_y.articulo = par.y
ORDER BY lift DESC;
```

Con esos cinco tickets sale `mantequilla → pan` con confianza 1,0 y lift 1,25, y
`leche → mantequilla` con lift 0,556: el mismo cálculo que el bloque de Python, pero sobre la
tabla en lugar de sobre números escritos a mano.

## Errores típicos

- **Confundir la confianza con la dirección de la regla.** `pan → mantequilla` con confianza 0,4
  no dice que el 40 % de los clientes compre pan: dice que el 40 % de los que compran pan
  compran mantequilla. Las cestas con pan son 200 de 1000; el 40 % de esas 200 son 80.
- **Ordenar por confianza y quedarse con el top 10.** Es la forma más rápida de llenar el
  informe de reglas obvias sobre artículos populares. Ordena por lift y usa la confianza como
  filtro secundario.
- **Bajar el soporte mínimo «para no perder nada».** El número de conjuntos frecuentes crece de
  forma explosiva: pasar de 0,01 a 0,001 puede multiplicar por cien el tiempo y generar millones
  de reglas. Empieza alto, mira el resultado y baja solo si hace falta.
- **Ignorar el tamaño de la cesta.** Un ticket con 60 artículos genera casi dos mil pares y
  contamina el análisis con un cliente que quizá fue una compra de empresa. Filtra cestas
  absurdamente grandes o analiza por separado.
- **Descubrir las reglas y evaluarlas en el mismo periodo, olvidando la multiplicidad.** Las
  reglas de las rebajas de julio no valen para noviembre: descubre con tres meses y valida con el
  mes siguiente. Y si evalúas 50.000 reglas, las 20 mejores por lift incluirán varias
  casualidades, porque con tantas pruebas el azar produce lifts altos solo. Exige un soporte
  mínimo decente y comprueba la estabilidad en periodos distintos.
- **Usar reglas para decidir precios sin mirar la causalidad.** Que la gente compre pan y
  mantequilla a la vez no significa que subir el pan aumente la venta de mantequilla. Para eso
  hacen falta experimentos, como en cualquier pregunta causal.

:::practica
enunciado: En 5.000 tickets, el yogur aparece en 500, la fruta en 1.500 y los dos juntos en 300. Calcula soporte, confianza y lift de yogur → fruta y de fruta → yogur, y decide cuál de las dos reglas reportas.
pista: La confianza divide el soporte conjunto entre el soporte del antecedente; el lift lo divide después entre el soporte del consecuente.
solucion: Soporte conjunto = 300 / 5000 = 0,06. yogur → fruta: confianza = 300 / 500 = 0,60 y lift = 0,60 / 0,30 = 2,00. fruta → yogur: confianza = 300 / 1500 = 0,20 y lift = 0,20 / 0,10 = 2,00. El lift coincide porque es simétrico; la confianza no. Si quieres la regla que acierta más veces, reporta yogur → fruta (0,60 frente a 0,20), asumiendo que cubre menos cestas.
:::

## Comprueba que lo sabes

:::quiz
p: El 20 % de las cestas llevan pan, el 10 % mantequilla y el 8 % las dos. ¿Cuál es el lift de la regla pan → mantequilla?
o: 4,00
o: 0,40
o: 0,08
a: 1
e: La confianza es 0,08 / 0,20 = 0,40 y el lift es 0,40 / 0,10 = 4,00, es decir, cuatro veces más probable que por azar. El 0,40 es la confianza (solo la mitad del cálculo) y 0,08 es el soporte de la regla.
:::

:::quiz
p: Una regla tiene confianza 0,90 y lift 1,02. ¿Cómo se interpreta?
o: Es una regla excelente: acierta el 90 % de las veces
o: El consecuente es tan frecuente que la regla no aporta casi nada sobre el azar
o: El lift está mal calculado, porque una confianza tan alta implica un lift alto
a: 2
e: Un lift de 1,02 significa independencia práctica: el consecuente ya aparecía en el 88 % de las cestas. La confianza alta solo refleja que el artículo B es popular. Las dos medidas miden cosas distintas y no se implican la una a la otra.
:::

:::quiz
p: ¿Por qué Apriori no necesita evaluar todos los conjuntos de artículos posibles?
o: Porque usa la propiedad de que todo subconjunto de un conjunto frecuente también es frecuente, y descarta los candidatos que contienen un subconjunto raro
o: Porque los conjuntos de más de tres artículos no se consideran
o: Porque muestrea un 10 % de los tickets y generaliza
a: 1
e: Esa monotonía permite podar: si un par no llega al soporte mínimo, ningún conjunto mayor que lo contenga puede llegar. Apriori no limita el tamaño a tres ni muestrea los datos: recorre los tickets completos, y justamente por eso el umbral de soporte decide cuánto tarda.
:::

:::truco
Antes de lanzar Apriori sobre millones de tickets, agrega: en lugar de analizar la cesta
individual, analiza productos que se compran juntos por cliente en un mes. Reduce el ruido, el
número de filas y hace que las reglas hablen de hábitos en vez de coincidencias de un día.
:::
