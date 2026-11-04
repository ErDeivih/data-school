---
id: testing-con-pytest
titulo: Tests con pytest
fase: 3
nivel: intermedio
rutas: [de, ds, alg]
prerequisitos: [entorno-python, tipos-y-estructuras-python, pandas-fundamentos]
tags: [tests, pytest, calidad, pipeline, fixtures]
resumen: Fixtures, parametrización y cobertura: qué merece un test en un pipeline de datos y qué es una pérdida de tiempo disfrazada de rigor.
fuentes: ["Pytest documentation, 'pytest: helps you write better programs'", "Khorikov (2020), 'Unit Testing: Principles, Practices, and Patterns'"]
---

## En una frase

Un test es código que comprueba que otro código hace lo que dijiste, y en un pipeline de datos
no sirve para demostrar que tu función está bien: sirve para que el día que cambies algo te
enteres **antes** de que los datos malos lleguen a la tabla que lee el negocio.

## La idea

Una transformación típica: recibes un DataFrame de pedidos, quitas los que no tienen fecha y
conviertes los importes a euros. Funciona. Tres semanas después alguien añade una columna,
cambia el orden de dos líneas y los pedidos sin fecha dejan de filtrarse: el informe de ventas
cuenta un 4 % más de lo real y nadie lo nota hasta el cierre de mes.

Un test es esa comprobación escrita y automática. La gracia no es que el test sea listo, es que
se ejecuta en dos segundos y **se ejecuta siempre**, mientras que repasar el código a mano no lo
hace nadie. Escribir tests es cambiar «creo que esto funciona» por «esto funciona y si deja de
funcionar, el pipeline se para».

En datos hay tres tipos de comprobación y conviene no confundirlos:

1. **Tests de la lógica**: convierto importes a euros, ¿lo hace bien? Entradas pequeñas escritas
   a mano, resultado esperado. Son los tests normales de software y son los que de verdad
   protegen tu código.
2. **Tests de los datos**: la tabla de hoy tiene 0 filas, o una columna que debería ser única
   tiene duplicados. No prueban tu código, prueban los datos que te llegan. En pandas eso es una
   función de validación que se ejecuta al principio del pipeline y falla con un mensaje claro.
3. **Tests de contrato**: el productor promete que la columna `fecha` es un `date` no nulo y que
   `cliente_id` es único. Si no lo cumple, el pipeline debe parar en la puerta, no escribir
   basura hacia abajo.

`pytest` es la herramienta porque reduce una prueba a una función: cualquier función cuyo
nombre empiece por `test_`, en un fichero que empiece por `test_`, es un test. Se ejecuta con
`pytest` y él descubre, ejecuta y te dice qué falla. Sin clases, sin registro, sin `main`.

## Definición formal

El vocabulario de pytest, definido:

- **Test**: una función `def test_algo():` que usa `assert`. Si el `assert` falla, el test
  falla y pytest muestra los valores de las dos partes de la comparación.
- **`assert`**: la única forma de comprobar en pytest. `assert resultado == esperado`. Al fallar
  no hay que escribir mensajes a mano: pytest te enseña qué valía cada lado.
- **Fixture**: una función decorada con `@pytest.fixture` cuyo valor pytest inyecta en los
  tests que la piden por nombre. Sirve para preparar lo que comparten varios tests (un
  DataFrame, una conexión, un fichero temporal) y para desmontarlo al terminar.
- **Alcance de la fixture (`scope`)**: `"function"` (por defecto, se crea en cada test),
  `"module"`, `"session"`. Una fixture de sesión se construye una vez para toda la ejecución.
- **Parametrización**: `@pytest.mark.parametrize("entrada, esperado", [(...), (...)])` ejecuta
  el mismo test una vez por caso. Un fallo te dice **qué caso** falló, y añadir un caso es
  añadir una línea.
- **`pytest.raises(Excepcion)`**: comprueba que el código lanza lo que debe lanzar. Sin esto
  acabas con un `except Exception: pass` que se traga los errores de verdad.
- **Cobertura**: porcentaje de líneas (o ramas con `--cov-branch`) ejecutadas por los tests. Es
  una medida de lo que **no** se ha probado, no de lo bien probado que está. Un 100 % de
  cobertura con asserts vacíos existe.

La anatomía de un test de calidad, en tres pasos: prepara el dato de entrada, ejecuta la
función, compara con lo que esperabas (y con lo que esperabas que **no** pasara).

:::formula
test:  entrada conocida → función → salida esperada
:::

En notación compacta, un test afirma que para todo `x` de un conjunto de casos se cumple
`f(x) = y`. Si esa afirmación se rompe, el test falla. Nada más: no hay magia, solo una
igualdad comprobada automáticamente.

## Ejemplo

Una función que quita pedidos sin fecha y pasa los importes de céntimos a euros:

```text
entrada: [{"id": 1, "centimos": 1050, "fecha": "2024-01-05"},
          {"id": 2, "centimos": 999,  "fecha": None},
          {"id": 3, "centimos": 0,    "fecha": "2024-01-06"}]

salida:  [{"id": 1, "euros": 10.5},
          {"id": 3, "euros": 0.0}]
```

Cuatro comprobaciones que cubren lo que importa:

1. Se elimina el pedido sin fecha: quedan 2 de 3 filas.
2. La conversión es exacta para valores con decimales: 1050 céntimos son 10,5 euros, no 10,49
   (aquí es donde aparece el error de redondeo si divides con enteros).
3. El cero se conserva: un pedido de 0 euros es un pedido, no un dato ausente. Si lo tratas
   como nulo, lo pierdes.
4. Un precio negativo lanza un error en vez de colarse. Es el caso que nadie prueba y el que
   aparece en producción.

El cuarto es el que separa un test útil de un test decorativo: **probar los caminos de error
importa más que probar el camino feliz**, porque el camino feliz ya lo has ejecutado a mano
mientras desarrollabas.

## Código

```python verificable
# La misma idea que un test de pytest, con asserts que se ejecutan de verdad aqui.
import pandas as pd

def limpia_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    """Quita pedidos sin fecha, rechaza importes negativos y pasa centimos a euros."""
    if (df["centimos"] < 0).any():
        raise ValueError("hay importes negativos en el lote")
    limpio = df.dropna(subset=["fecha"]).copy()
    limpio["euros"] = limpio["centimos"] / 100
    return limpio[["id", "euros"]]

entrada = pd.DataFrame({
    "id": [1, 2, 3],
    "centimos": [1050, 999, 0],
    "fecha": ["2024-01-05", None, "2024-01-06"],
})

salida = limpia_pedidos(entrada)

assert len(salida) == 2                      # el pedido sin fecha se cae
assert salida["euros"].iloc[0] == 10.5       # 1050 centimos son 10.5 euros exactos
assert salida["euros"].iloc[1] == 0.0        # un pedido de cero euros no es un nulo
assert list(salida["id"]) == [1, 3]

print("filas de entrada:", len(entrada))
print("filas de salida :", len(salida))
print("euros:", salida["euros"].tolist())
```

```python verificable
# Probar el camino de error: la parte que casi nadie escribe.
import pandas as pd

def limpia_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    if (df["centimos"] < 0).any():
        raise ValueError("hay importes negativos en el lote")
    return df.dropna(subset=["fecha"]).copy()

malo = pd.DataFrame({"id": [1], "centimos": [-100], "fecha": ["2024-01-05"]})

try:
    limpia_pedidos(malo)
    print("ERROR: deberia haber lanzado ValueError")
except ValueError as exc:
    print("lanza ValueError:", str(exc))
```

```python verificable
# Regla de unicidad sobre los datos: el test de contrato mas barato que existe.
import pandas as pd

pedidos = pd.DataFrame({
    "pedido_id": [10, 11, 11, 12],
    "cliente_id": [1, 2, 2, 3],
    "importe": [10.0, 20.0, 20.0, 5.0],
})

duplicados = int(pedidos["pedido_id"].duplicated().sum())
nulos_clave = int(pedidos["pedido_id"].isna().sum())

print("filas:", len(pedidos))
print("pedido_id duplicados:", duplicados)
print("claves nulas:", nulos_clave)

if duplicados or nulos_clave:
    print("el pipeline debe parar aqui antes de agregar nada")
```

```python ilustrativo
# Fichero tests/test_limpia_pedidos.py — el mismo analisis, ahora con pytest.
import sqlite3

import pandas as pd
import pytest

from pipeline.limpieza import limpia_pedidos


# Una fixture: los datos compartidos se construyen una vez y se inyectan por nombre.
@pytest.fixture
def pedidos_crudos():
    return pd.DataFrame({
        "id": [1, 2, 3],
        "centimos": [1050, 999, 0],
        "fecha": ["2024-01-05", None, "2024-01-06"],
    })


def test_descarta_los_pedidos_sin_fecha(pedidos_crudos):
    assert len(limpia_pedidos(pedidos_crudos)) == 2


# Parametrizar: un caso por linea, y el fallo dice cual.
@pytest.mark.parametrize("centimos, euros", [(1050, 10.5), (0, 0.0), (1, 0.01), (99999, 999.99)])
def test_conversion_exacta(centimos, euros):
    df = pd.DataFrame({"id": [1], "centimos": [centimos], "fecha": ["2024-01-05"]})
    assert limpia_pedidos(df)["euros"].iloc[0] == euros


def test_rechaza_importes_negativos():
    df = pd.DataFrame({"id": [1], "centimos": [-1], "fecha": ["2024-01-05"]})
    with pytest.raises(ValueError, match="negativos"):
        limpia_pedidos(df)


# La conexion tambien es una fixture: si no estuviera declarada, pytest no ejecutaria el test,
# abortaria con «fixture 'conexion' not found». El alcance de modulo la abre una sola vez.
@pytest.fixture(scope="module")
def conexion():
    con = sqlite3.connect(":memory:")
    con.execute("create table pedidos (id integer)")
    con.executemany("insert into pedidos values (?)", [(1,), (2,)])
    yield con
    con.close()


# Un test de datos, no de codigo: se ejecuta contra la tabla real de cada dia.
def test_contrato_de_la_tabla_de_pedidos(conexion):
    filas = conexion.execute("select count(*) from pedidos").fetchone()[0]
    assert filas > 0, "la tabla de pedidos llego vacia"
```

```text
$ pytest -q
.......                                                                  [100%]
7 passed in 0.12s

$ pytest --cov=pipeline --cov-report=term-missing
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
pipeline/limpieza.py           14      2    86%   21-22
---------------------------------------------------------
TOTAL                          14      2    86%

# Las lineas 21-22 son el camino de error: el test que falta esta ahi.
```

## Errores típicos

- **Perseguir el 100 % de cobertura.** La cobertura mide líneas ejecutadas, no casos
  comprobados: un test que llama a la función y no compara nada sube el porcentaje sin proteger
  nada. Es más útil mirar las líneas rojas del informe (`Missing`) y preguntarse si ahí hay
  lógica que importa.
- **Tests que dependen del orden o de datos externos.** Un test que lee un CSV del escritorio,
  llama a una API o depende de que otro test se haya ejecutado antes no es un test: es una
  lotería. Los datos de entrada se escriben dentro del test o se construyen en una fixture.
- **Comparar DataFrames con `==`.** `df1 == df2` devuelve una tabla de booleanos, no un booleano,
  así que el `assert` no comprueba lo que parece: pandas lanza
  `ValueError: The truth value of a DataFrame is ambiguous` en vez de decirte si son iguales. Usa
  `pandas.testing.assert_frame_equal(df1, df2)`, que compara valores, tipos e índice y te dice
  exactamente qué columna y qué fila difieren.
- **Probar solo el camino feliz.** El caso con el dato vacío, el nulo, el cero, el negativo y el
  duplicado es donde vive el fallo de producción. Probar que 2 + 2 son 4 es gratis y no aporta.
- **Tests que comprueban la implementación y no el resultado.** Si el test afirma «se llama a
  esta función auxiliar dos veces», cualquier refactor lo rompe aunque el resultado sea correcto.
  Se comprueba la salida para una entrada dada, no cómo se llega a ella.
- **Escribir los tests al final, con prisa, solo para el informe.** Un test escrito a posteriori
  suele reproducir el mismo malentendido que el código. Los tests de los casos límite se piensan
  antes de escribir la función, y son los que te obligan a decidir qué hacer con el nulo.

:::truco
No hace falta pytest para empezar: un fichero con asserts al final del módulo ya detecta
regresiones y no depende de nada. Cuando el proyecto crece, migrar esos asserts a funciones
`test_` es cuestión de minutos, y ya tienes el hábito. Lo que no se puede automatizar es
acordarse de ejecutarlos: eso es lo que aporta pytest y su integración con
[[git-para-datos|los ganchos de git]] o con la integración continua.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Para qué sirve una fixture de pytest?
o: Para ejecutar los tests más rápido ignorando los que fallan
o: Para preparar los datos o recursos que comparten varios tests e inyectarlos por nombre
o: Para medir el porcentaje de líneas cubiertas
a: 2
e: Una fixture es una función que prepara algo (un DataFrame, una conexión, un fichero temporal) y que pytest pasa como argumento a los tests que la piden por nombre; también se encarga de la limpieza al terminar. Saltarse un test concreto es `--deselect` o `-k`, y la cobertura la mide `pytest-cov`.
:::

:::quiz
p: Tu test compara dos DataFrames con `assert df1 == df2`. ¿Qué está mal?
o: Nada, es la forma correcta de comparar DataFrames
o: Que la comparación no devuelve un booleano sino un DataFrame de booleanos, así que en vez de comparar los datos salta `ValueError: The truth value of a DataFrame is ambiguous`
o: Que hay que convertir antes los DataFrames a listas
a: 2
e: `df1 == df2` compara celda a celda y devuelve una tabla de True y False; al evaluar esa tabla como condición, pandas no sabe qué contestar y lanza `ValueError: The truth value of a DataFrame is ambiguous`. Hay que usar `pandas.testing.assert_frame_equal`, que compara valores, tipos e índice y muestra la primera diferencia.
:::

:::practica
enunciado: Tienes una función que calcula el ingreso mensual por cliente a partir de una tabla de pedidos. Enumera los cuatro tests que escribirías primero y explica por qué esos y no otros.
pista: Piensa en qué casos de los datos, no del código, romperían el informe sin que nadie se diera cuenta.
solucion: (1) Un cliente sin pedidos debe aparecer con ingreso cero o no aparecer, según lo que hayas decidido: ese caso define si el informe suma 0 o pierde clientes. (2) Un pedido con importe negativo (una devolución) no debe restar silenciosamente si el negocio espera el importe bruto; hay que fijar el comportamiento. (3) Dos pedidos del mismo día para el mismo cliente deben agregarse, no duplicar la fila ni perder uno. (4) Un pedido sin fecha o con fecha fuera del mes analizado no debe caer en el mes equivocado. Los cuatro son casos de datos que se dan en producción y que no lanzan ninguna excepción: producen un número plausible y equivocado, que es el peor fallo posible. Un test que compruebe que la suma de dos importes conocidos da el total esperado también vale, pero es el que menos aporta, porque ese camino lo has verificado a mano al escribirlo.
:::
