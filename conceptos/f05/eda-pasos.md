---
id: eda-pasos
titulo: Análisis exploratorio: el método
fase: 5
nivel: básico
rutas: [core, ds, de]
prerequisitos: [perfilado-de-datos, calidad-de-datos, pandas-fundamentos]
tags: [eda, exploracion, calidad, metodo]
resumen: Una rutina ordenada para conocer un dataset antes de modelarlo: qué es una fila, qué falta, qué rangos son posibles, cómo se distribuye y con qué se relaciona.
fuentes: ["Tukey (1977), 'Exploratory Data Analysis'"]
---

## En una frase

El análisis exploratorio es una lista de comprobaciones baratas, hechas **en orden**, que
convierte un fichero desconocido en un conjunto de datos del que te fías y sobre el que sabes
qué preguntas tienen sentido.

## La idea

Abres un dataset nuevo y lo primero que apetece es entrenar un modelo. Es el orden equivocado: un
modelo sobre datos mal entendidos te devuelve una métrica bonita y una conclusión falsa. El
análisis exploratorio es el reconocimiento del terreno antes de construir.

El orden importa porque cada paso barato evita un problema caro. Si no sabes qué representa una
fila, cualquier número que calcules después puede estar contando dos veces lo mismo. Si no sabes
qué significan los nulos, los vas a rellenar mal. Si no has mirado la forma de una variable,
vas a resumir con la media una distribución que tiene dos picos, y la media caerá justo en el
hueco entre ambos, donde no hay nadie.

La rutina tiene siete pasos, y los cuatro primeros son de una sola línea de código:

1. **Forma.** Cuántas filas y cuántas columnas. Un dataset de 300 filas no admite las mismas
   conclusiones que uno de 3 millones.
2. **Grano.** ¿Qué representa **una fila**? Un pedido, una línea de pedido, un cliente por día.
   Sin esto, todo lo demás es interpretable de varias maneras.
3. **Tipos y nulos.** Qué columnas son numéricas, de texto o fechas; cuántos valores faltan y
   en qué columnas se concentran.
4. **Rangos.** Mínimo, máximo y valores imposibles: edades negativas, fechas de 1900, importes
   de cero.
5. **Distribuciones.** La forma de cada variable numérica: simétrica, sesgada, bimodal, con
   ceros de más.
6. **Relaciones.** Cómo se mueven las variables entre sí: correlaciones, tablas cruzadas,
   medias por grupo.
7. **Rarezas.** Categorías que aparecen una sola vez, duplicados inesperados, valores
   centinela como −1 o 9999, cambios de comportamiento en el tiempo.

Los pasos 1 a 4 son mecánicos y se automatizan con [[perfilado-de-datos]]. Los pasos 5 a 7
requieren mirar y pensar: ahí es donde aparecen los hallazgos que cambian el proyecto.

:::truco
Escribe las conclusiones de cada paso en un documento mientras exploras, con la cifra concreta.
«La columna `importe` tiene 12,5 % de nulos, y el único cae en un pedido web». Dentro de dos semanas no
recordarás si el 12 % era de nulos o de descuentos, y volver a averiguarlo cuesta otra hora.
:::

## Definición formal

Cada paso tiene una pregunta y una comprobación concreta:

| Paso | Pregunta | Comprobación |
| --- | --- | --- |
| Forma | ¿Cuánto hay? | Número de filas y columnas |
| Grano | ¿Qué es una fila? | La clave candidata es única: contar filas y contar claves distintas |
| Tipos y nulos | ¿Qué falta? | Proporción de nulos por columna y por grupo |
| Rangos | ¿Qué es imposible? | Mínimo y máximo de cada numérica y de cada fecha |
| Distribuciones | ¿Qué forma tiene? | Histograma, asimetría, cuantiles |
| Relaciones | ¿Qué se mueve junto? | Matriz de correlación, medias por categoría |
| Rarezas | ¿Qué no encaja? | Frecuencias de categorías, valores centinela, series temporales |

La comprobación del grano es la más importante y la más olvidada, y tiene una forma exacta:

:::formula
si nº de filas = nº de valores distintos de la clave candidata, la clave identifica la fila
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `nº de filas` | Cuántas filas tiene la tabla | filas | Si supera el número de claves distintas, la clave candidata no identifica la fila: o el grano es otro o hay filas repetidas, y cualquier suma hecha así está inflada |
| `nº de valores distintos de la clave` | Cuántos valores únicos tiene la columna que crees que identifica la fila | valores distintos | Si baja respecto al número de filas, cada clave aparece en varias filas: es el aviso de que hay que mirar los duplicados antes de seguir |
| `clave candidata` | La columna o combinación que debería ser única: `pedido_id`, o `pedido_id` más `línea` | — | Si se elige mal, la comprobación pasa igual y el error no se detecta: la igualdad solo prueba algo con la clave correcta |
| `nº de filas tras la unión` | Cuántas filas quedan después de un `merge` | filas | Si crece respecto a la tabla de partida, la unión ha multiplicado registros; el ticket medio y el total quedan mal sin lanzar ningún error |
:::

Esa igualdad se comprueba **antes y después de cada unión** de tablas. Una unión que no conserva
el número de filas ha multiplicado registros, y cualquier suma posterior está inflada.

:::figura
fichero: eda-pasos-grano-y-ticket-medio
pie: A la izquierda, la comprobación del grano sobre ocho líneas de pedido: `pedido_id` tiene 5 valores distintos y `cliente_id` solo 4, mientras que `pedido_id + linea` tiene 8, las mismas que filas. A la derecha, el ticket medio que sale con cada clave candidata: 13,75 €, 8,59 € y 17,19 €, tres números plausibles de la misma tabla. Solo la clave que identifica la fila devuelve la media de verdad, 68,75 € entre 8 líneas; los otros dos son falsos y ninguna librería avisa.
fuente: figuras/eda-pasos-1.py
:::

## Ejemplo

Ocho filas de pedidos:

```
pedido_id  cliente_id  importe  canal   fecha
1          10          19.90    web     2024-01-02
2          10          45.00    app     2024-01-02
3          11          12.50    web     2024-01-03
4          12          (nulo)   web     2024-01-03
5          12          78.20    app     2024-01-04
6          12          33.00    web     2024-01-05
7          13           9.99    tienda  2024-01-05
8          13         120.00    web     2024-01-09
```

- **Forma**: 8 filas y 5 columnas.
- **Grano**: 8 pedidos distintos y 8 filas, así que una fila es un pedido. Si hubiera 6 pedidos
  distintos en 8 filas, habría duplicados y habría que investigar cuáles.
- **Nulos**: 1 de 8 en `importe`, el 12,5 %. Está en el pedido 4, que es del canal web. Un solo
  nulo no se arregla «rellenando con la media» sin preguntar antes qué pasó.
- **Rangos**: el importe mínimo es 9,99 y el máximo 120,00. Ninguno es negativo ni cero, así que
  no hay devoluciones mal codificadas.
- **Distribuciones**: con 8 valores no se puede hablar de forma. Con 8 000 sí, y entonces habría
  que mirar si el importe tiene cola larga.
- **Relaciones**: el cliente 12 aparece en tres pedidos y suma 111,20 (uno de ellos sin
  importe), el 35 % de la facturación de la semana, que son 318,59 en total. Un cliente
  concentra un tercio del resultado y conviene saberlo antes de sacar conclusiones.
- **Rarezas**: el canal `tienda` aparece una sola vez. Con una sola observación no se puede
  comparar canales, y sin embargo mucha gente lo hace.

## Código

```python verificable
import pandas as pd

# Ocho pedidos: el dataset minimo para recorrer los cuatro primeros pasos del metodo
pedidos = pd.DataFrame({
    "pedido_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "cliente_id": [10, 10, 11, 12, 12, 12, 13, 13],
    "importe": [19.9, 45.0, 12.5, None, 78.2, 33.0, 9.99, 120.0],
    "canal": ["web", "app", "web", "web", "app", "web", "tienda", "web"],
    "fecha": ["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03",
              "2024-01-04", "2024-01-05", "2024-01-05", "2024-01-09"],
})

print("filas, columnas:", pedidos.shape)                       # -> (8, 5)
print("pedidos distintos:", pedidos["pedido_id"].nunique())    # -> 8
print("nulos en importe:", int(pedidos["importe"].isna().sum()))  # -> 1
print("canales distintos:", pedidos["canal"].nunique())        # -> 3
print("importe minimo:", pedidos["importe"].min())             # -> 9.99
```

:::claves
- `pedidos.shape` es una **tupla** `(8, 5)`, no una lista: se puede desempaquetar (`filas, columnas = pedidos.shape`) y no se puede modificar. Y no es lo mismo que `len(pedidos)`, que da 8 (las filas), ni que `pedidos.size`, que da 40 (las celdas).
- El `None` de la lista de importes se convierte en `NaN` al construir el DataFrame, y por eso la columna entera pasa a ser `float64` aunque los demás valores sean enteros. Un solo hueco cambia el tipo de la columna y con él los decimales que se ven al imprimir. En el texto de la página ese hueco se escribe «(nulo)», pero dentro de pandas es `NaN`.
- `pedidos["importe"].min()` devuelve 9,99 **aunque haya un nulo**, porque pandas se salta los huecos. Y `np.min(pedidos["importe"])` da lo mismo, 9,99: NumPy ve que le han pasado una `Series`, encuentra su método `min` y lo usa. Para que salga `nan` hay que convertir antes a array: `np.min(pedidos["importe"].to_numpy())`. La misma pregunta con dos respuestas según el tipo que tengas en la mano, así que mira de dónde viene el dato antes de creerte el número.
- `pedidos["canal"].nunique()` cuenta valores distintos y no cuenta los nulos, y `value_counts()` los excluye salvo que se pida `dropna=False`. Ese detalle es el que hace que un canal lleno de huecos parezca pequeño justo en el paso de rarezas.
- La columna `fecha` son **cadenas de texto**, no fechas: `min()` y `max()` ordenan alfabéticamente y con el formato ISO `2024-01-02` coinciden por casualidad con el orden temporal. En cuanto el formato sea `02/01/2024`, el «mínimo» pasa a ser otra fecha y nada avisa: para el paso de rangos hay que convertir con `pd.to_datetime`.
- Para la misma columna, `isna().sum()` da 1, `count()` da 7 (los no nulos) y `size` da 8 (las celdas). Son tres números distintos y elegir el equivocado cambia el porcentaje de nulos que se apunta en el informe.
:::

```sql verificable
-- El grano importa: sumar por la clave equivocada multiplica los totales.
CREATE TABLE lineas(pedido_id INTEGER, linea INTEGER, importe DOUBLE);
INSERT INTO lineas VALUES (1,1,10.0),(1,2,5.5),(2,1,20.0),(3,1,7.25);

SELECT count(*) AS filas,
       round(sum(importe), 2) AS total_lineas,
       count(DISTINCT pedido_id) AS pedidos,
       round(sum(importe) / count(DISTINCT pedido_id), 2) AS ticket_medio
FROM lineas;
```

```text
filas | total_lineas | pedidos | ticket_medio
4     | 42.75        | 3       | 14.25
```

## Errores típicos

- **Empezar por el modelo.** Un `fit` sobre datos sin explorar da una métrica y ninguna
  explicación. Las dos horas de exploración ahorran dos días de depurar un resultado absurdo.
- **No comprobar el grano antes de unir tablas.** Es el error más caro de todo el análisis: un
  `merge` que duplica filas infla todas las sumas y nadie lo nota hasta que el informe no
  cuadra. Cuenta filas antes y después, siempre.
- **Resumir con la media una variable bimodal o muy sesgada.** Si la distribución tiene dos
  picos, la media cae en el valle y no describe a ningún caso. Mira el histograma y usa
  [[medidas-de-centralidad|mediana y cuantiles]].
- **Rellenar nulos con cero sin preguntar qué significan.** En `importe`, un nulo puede ser un
  pedido no facturado; en `peso`, un dato no medido. Rellenar con cero inventa un dato y sesga
  cualquier media a la baja.
- **Mirar las columnas de una en una y no las relaciones.** La suma de dos variables sin sentido
  por separado puede tener todo el sentido: un importe y un descuento que se compensan.
- **Confundir un cruce con una causa.** Que los clientes de `app` gasten más no significa que la
  app haga gastar más: puede que la app la usen los clientes más fieles. Eso es
  [[causalidad-vs-correlacion]], y se resuelve con un experimento, no con una tabla cruzada.

:::practica
enunciado: Tienes 400 pedidos: 160 del canal web y 240 del canal tienda. Faltan 36 importes: 2 en web y 34 en tienda. Calcula la tasa de nulos global y por canal y decide si imputar con la media global es defendible.
pista: Compara la proporción de nulos dentro de cada canal: si el hueco se concentra en un grupo, rellenar con la media general mete ese grupo donde no toca.
solucion: Global: 36 / 400 = 9,0 %. Web: 2 / 160 = 1,25 %. Tienda: 34 / 240 = 14,2 %. La ausencia se concentra en tienda, más de diez veces la de web, así que no es MCAR. Imputar con la media global mezcla dos grupos distintos y sesga la comparación entre canales: investiga antes qué significa el hueco y, si imputas, hazlo por canal y deja la marca de ausencia.
:::

## Comprueba que lo sabes

:::quiz
p: Un dataset tiene 8 filas y 6 valores distintos en la columna `pedido_id`. ¿Qué concluyes?
o: Que la columna `pedido_id` identifica cada fila
o: Que hay pedidos repetidos en varias filas y el grano no es «un pedido por fila»
o: Que faltan dos pedidos en los datos
a: 2
e: Si la clave candidata tiene menos valores distintos que filas, hay duplicados: o el grano es otro (varias líneas por pedido) o hay filas repetidas por un error de carga. Antes de sumar nada hay que averiguar cuál de las dos cosas es.
:::

:::quiz
p: La columna `importe` tiene un 12,5 % de nulos. ¿Cuál es el primer paso correcto?
o: Rellenarlos con la media para no perder filas
o: Borrar esas filas y seguir
o: Mirar en qué filas y en qué grupos aparecen los nulos antes de decidir nada
a: 3
e: Un nulo no es un valor neutro: puede significar «no se facturó», «no se midió» o «no aplica». Si se concentran en un canal o en un periodo, borrarlos sesga el resultado. Primero se describe el patrón de ausencia y después se decide entre imputar, marcar o excluir.
:::

:::nota
El análisis exploratorio no termina cuando empiezas a modelar. Cada vez que un gráfico o una
métrica te sorprende, vuelves a él: comprobar el grano y los rangos de la variable sospechosa
resuelve la mitad de las sorpresas.
:::
