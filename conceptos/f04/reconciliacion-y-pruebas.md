---
id: reconciliacion-y-pruebas
titulo: Reconciliación y pruebas de datos
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [dbt-y-transformacion, calidad-y-slas, sql-agregaciones-y-group-by]
tags: [calidad, pruebas, auditoria, control]
resumen: Cuadrar el origen con el destino, escribir pruebas que fallen solas y guardar los recuentos para saber si el dato de hoy se parece al de siempre.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering'", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 12"]
---

## En una frase

Reconciliar es demostrar con números que lo que hay en el destino es lo que debería haber llegado del
origen: recuentos, sumas de control y pruebas que hacen fallar el pipeline antes de que el error
llegue al informe.

## La idea

Es el arqueo de caja de una tienda al cerrar. Cuentas los billetes que hay (el destino) y los
comparas con lo que dice el TPV (el origen). No basta con que la caja «parezca» bien: hay que cuadrar
la cifra y, cuando no cuadra, saber cuánto falta, de qué día y por qué. Un pipeline sin
reconciliación es una caja que nadie cuenta nunca.

Hay tres preguntas detrás, de la más fácil a la más difícil:

1. **¿Están todas las filas?** Un recuento por partición y por tabla. Es el control más barato y el
   que antes detecta un fallo de carga.
2. **¿Están bien los valores?** Sumas de control: el total de un importe, el mínimo, el máximo, el
   número de nulos y el número de claves distintas. Si el recuento cuadra y la suma no, el problema
   está en la transformación, no en la carga.
3. **¿Significa lo mismo?** El grano, las categorías y las unidades. Un recuento perfecto con las
   fechas en otra zona horaria sigue siendo un dato equivocado.

Las pruebas se escriben una vez y se ejecutan en cada carga. En [[dbt-y-transformacion|dbt]] se
declaran en el YAML del modelo (`not_null`, `unique`, `relationships`, `accepted_values`) o como
**pruebas singulares**: ficheros de SQL dentro de `tests/` que devuelven las filas que fallan. Si
devuelven cero filas, la prueba pasa. Ese detalle cuesta al principio: la prueba no comprueba que el
dato esté bien, comprueba que **no hay filas malas**. Y `dbt test` termina con un código de salida
distinto de cero cuando algo falla, que es lo que engancha la prueba al orquestador para no dejar
pasar el modelo siguiente ([[orquestacion-y-dag]]).

No todo se compara igual:

- **Recuentos:** exactos dentro de una misma partición. Una fila que falta es una fila que falta.
- **Importes y medias:** con tolerancia, porque el redondeo y los números en coma flotante hacen que
  la diferencia casi nunca sea exactamente cero.
- **Contra el histórico:** la comparación que más enseña. «Hoy han entrado 1 248 700 filas» no dice
  nada; «hoy han entrado un 12 % menos que el mismo día de la semana pasada» salta a la vista. Esa
  es la base de la [[observabilidad-de-datos]].

Y todo esto se guarda. Una tabla de auditoría con una fila por ejecución y modelo —partición,
recuento, suma, nulos, claves distintas, instante y versión del código— sirve para tres cosas:
detectar la anomalía antes de que la sufra el negocio, demostrar qué había en el almacén el día que
se publicó un informe, y acotar el reproceso cuando toca repetirlo ([[backfill-y-reproceso]]).

:::trampa
Una tolerancia ancha convierte un problema real en un número verde. Si pactas el 2 % en filas,
puedes perder 24 000 filas de un millón sin que nada se queje, y el informe saldrá igual de
convencido. La tolerancia se pone sobre lo que el negocio admite perder y se revisa cuando cambia el
volumen, no al revés.
:::

## Definición formal

Para cada valor de control tienes el del origen `O` y el del destino `D`. La diferencia relativa y la
condición de fallo son:

:::formula
d = (D − O) / O     ·     la prueba falla si |d| > ε
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `O` | Valor de control medido en el origen: recuento, suma de importe, claves distintas | filas, euros o unidades | Si sube, la misma diferencia absoluta pesa menos: por eso todo se compara en relativo |
| `D` | El mismo valor medido en el destino | igual que `O` | Si sube por encima de `O`, sospecha de duplicados o de una unión que multiplica filas |
| `d` | Diferencia relativa entre destino y origen | tanto por uno o porcentaje | Es la cifra que se compara con la tolerancia, y su signo dice de qué lado falta |
| `ε` | Tolerancia pactada con el negocio | tanto por uno | Al subir, menos falsas alarmas y más errores reales que pasan sin que nadie mire |
| `N` | Número de filas del control | filas | En recuentos de la misma partición debería exigirse `ε = 0`; la tolerancia va en la variación contra el histórico |
| `huérfanas` | Claves del destino que no existen en la dimensión con la que se cruza | filas | Si sube, los informes pierden filas al cruzar y los totales bajan sin ningún error visible |
| `corte` | Instante hasta el que se comparan origen y destino | fecha y hora | Cuanto más cerca de ahora, menos tiempo ha tenido el origen para terminar y más diferencias falsas aparecen |
| `severidad` | Qué hace la prueba cuando falla: avisar o parar | `warn` o `error` | Si todo es `error`, el pipeline se para por ruido; si todo es `warn`, nadie mira nunca |
:::

## Ejemplo

Un cuadro de control de una carga diaria:

| Control | Origen | Destino | Diferencia | Relativa |
| --- | --- | --- | --- | --- |
| Filas (líneas de pedido) | 1 250 000 | 1 248 700 | −1 300 | −0,104 % |
| Importe | 4 200 000,00 € | 4 199 100,00 € | −900,00 € | −0,0214 % |
| Clientes distintos | 318 400 | 318 400 | 0 | 0 % |

Con una tolerancia del 0,2 % en filas, esta carga **pasa**. Y sin embargo faltan 1 300 líneas de
pedido. Los clientes cuadran, así que no se ha perdido ninguna carga entera, y el importe que falta es
pequeño comparado con las filas: 900 € entre 1 300 líneas son 0,69 € por línea, importes de artículo
suelto, así que no es un error de valores: son filas que no llegaron. Por eso el recuento se compara
por partición y con el histórico, no contra un porcentaje global: la tolerancia dice cuánto puede
perder el negocio, no cuánto puedes dejar de mirar.

:::figura
fichero: reconciliacion-tolerancia-y-dias
pie: A la izquierda, los dos recuentos día a día: las barras se separan justo en los días que hay que investigar, y en el resto el destino sigue al origen. A la derecha, la diferencia relativa de cada día frente a la banda de tolerancia, aquí del 0,5 % (la del ejemplo de arriba es otra: la banda la pacta el negocio, no es un número fijo). El día 9 se sale de la escala con un 5,2 % de menos y el día 12 se queda a 0,05 puntos del límite: esos dos son los que enseñan algo, porque el resto de días no aporta información.
fuente: figuras/reconciliacion-y-pruebas-1.py
:::

## Código

```python verificable
import pandas as pd

origen = pd.DataFrame({
    "id": range(1, 8),
    "importe": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0],
    "fecha": ["2024-03-29", "2024-03-29", "2024-03-30", "2024-03-30", "2024-03-30",
              "2024-03-31", "2024-03-31"],
})
# El destino perdio las dos filas del 31: un filtro de fecha con la zona horaria mal puesta
destino = origen[origen.fecha != "2024-03-31"].copy()

filas = len(origen) - len(destino)
euros = origen.importe.sum() - destino.importe.sum()
print(f"faltan {filas} filas y {euros:.2f} euros")                        # -> faltan 2 filas y 130.00 euros
print(f"relativo en filas: {100 * filas / len(origen):.1f} %")           # -> relativo en filas: 28.6 %
print("ids que no llegaron:", sorted(set(origen.id) - set(destino.id)))   # -> ids que no llegaron: [6, 7]
```

:::claves
- `origen[origen.fecha != "2024-03-31"]` filtra y devuelve un DataFrame **nuevo**: el `origen`
  original no se toca, así que `len(origen)` sigue siendo 7 aunque el destino tenga 5. El `.copy()`
  deja explícito que trabajas sobre una copia, sin depender de lo que pandas decida por dentro.
- `origen.importe.sum()` se salta los `NaN` en silencio. Si un nulo significa «no se sabe», esa suma
  es una mentira cómoda: cuenta los nulos en otro control y compara también ese número.
- `euros == 0` con números en coma flotante falla por redondeo: 0,1 + 0,2 no da 0,3. En importes se
  compara contra una tolerancia o se trabaja en céntimos enteros.
- `len(df)` cuenta filas y `df.id.nunique()` cuenta identificadores distintos. Mismo recuento con
  menos claves distintas significa duplicados: 1 248 700 filas con 1 248 000 ids son 700 repetidos.
- `set(origen.id) - set(destino.id)` es la diferencia de conjuntos, y pierde el orden: de ahí el
  `sorted()`. Con millones de filas esto no se hace en Python, se hace con un `LEFT JOIN` que filtra
  los nulos en el motor.
- El `:.1f` de la f-string redondea **solo al imprimir**: 28,571 % se ve como 28,6 %, pero el valor
  que comparas con la tolerancia sigue siendo el exacto.
:::

Como prueba singular de dbt, la misma idea escrita para que la ejecute el orquestador:

```sql ilustrativo
-- Prueba singular: devuelve las filas que fallan; cero filas significan que pasa
select f.id_pedido
from {{ ref('fct_pedidos') }} f
left join {{ ref('dim_cliente') }} c on f.id_cliente = c.id_cliente
where c.id_cliente is null
```

## Errores típicos

- **Confundir «el pipeline terminó sin error» con «los datos están bien».** Un trabajo en verde con
  la mitad de las filas es el fallo más común y el más caro: nadie mira hasta que el informe lleva
  dos semanas mal.
- **Comparar solo el total.** 1 300 filas de menos en una partición y 1 300 duplicadas en otra dan el
  mismo recuento global, con dos errores dentro. El control se hace por partición, y luego se suma.
- **Poner tolerancia a los recuentos.** Los recuentos son exactos. La tolerancia va en importes, en
  medias y en la variación contra el histórico, no en «cuántas filas me faltan hoy».
- **Medir origen y destino en instantes distintos.** Si el origen sigue cargando mientras cuentas, la
  diferencia es un artefacto del reloj y no un error. Fija un corte: una partición cerrada o una foto
  del origen ([[calidad-y-slas]]).
- **Escribir pruebas que fijan el número exacto esperado.** «Tienen que ser 1 000 filas» se pone rojo
  el día que el negocio crece y alguien lo desactiva para seguir trabajando. Comprueba invariantes
  (no hay nulos, no hay claves repetidas, no hay huérfanas) o compara contra el histórico.
- **Dejar un test en rojo.** Un test que falla y nadie mira enseña a ignorarlos todos. Cada prueba
  necesita severidad, dueño y un aviso que llegue a una persona concreta.

:::practica
enunciado: Comparas origen y destino de una carga. El origen tiene 1 250 000 filas y 4 200 000,00 € de importe; el destino, 1 248 700 filas y 4 199 100,00 €, con los mismos 318 400 clientes distintos. Calcula las diferencias relativas, decide si pasan una tolerancia del 0,2 % y di qué investigas primero.
pista: La diferencia relativa es (destino − origen) partido por origen, y conviene mirar el importe que falta por cada fila que falta.
solucion: En filas, (1 248 700 − 1 250 000) / 1 250 000 = −0,104 %. En importe, (4 199 100 − 4 200 000) / 4 200 000 = −0,0214 %. Las dos caben dentro del 0,2 %, así que la prueba pasa; pero que falten 1 300 filas es un hecho, no un redondeo. Como los clientes distintos cuadran, no se ha perdido ninguna carga completa, y el importe que falta entre las filas que faltan da 900 / 1 300 = 0,69 € por fila, un importe de artículo suelto: no es un error de valores. Lo primero que investigas es el recuento por partición (por día o por hora) para ver si las 1 300 se concentran en una sola, después un anti-join de claves para listarlas, y antes de dar el dato por bueno compruebas si el origen había terminado de cargar cuando tomaste la medida.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué comprueba de verdad una prueba singular de dbt escrita como una consulta SQL?
o: Que el dato transformado es correcto y completo
o: Que la consulta no devuelve ninguna fila, es decir, que no hay filas malas
o: Que el modelo tiene el mismo número de filas que la ejecución anterior
a: 2
e: Una prueba singular devuelve las filas que fallan y pasa cuando el resultado está vacío. No demuestra que los datos sean correctos ni completos: demuestra que no encuentra el problema que la consulta describe. Por eso las pruebas se escriben sobre invariantes concretas y no sobre «todo está bien».
:::

:::quiz
p: El recuento de filas del destino coincide con el del origen, pero la suma del importe es un 3 % menor. ¿Qué miras?
o: La carga, porque se han perdido filas por el camino
o: La transformación, porque las filas están y los valores no cuadran
o: Nada, si el recuento cuadra la carga está bien
a: 2
e: Si las filas cuadran y la suma no, el problema está en cómo se calculó o se convirtió el importe: redondeos, tipos, un filtro dentro del cálculo o una división mal hecha. Un problema de carga habría movido también el recuento. Y dar por bueno el dato solo porque el recuento cuadra es justo lo que este control evita.
:::

:::quiz
p: ¿Cuál de estas comparaciones es la más útil para detectar un problema el mismo día que ocurre?
o: La diferencia relativa entre origen y destino con una tolerancia del 0,2 %
o: El recuento de hoy comparado con el del mismo día de la semana pasada
o: El número exacto de filas que debería tener la tabla cada día
a: 2
e: La comparación con el histórico detecta caídas y picos que ninguna tolerancia fija ve, porque el volumen cambia por día de la semana y por estación. Un número exacto esperado se rompe en cuanto el negocio crece, y una tolerancia global puede tapar la pérdida de una partición entera.
:::
