---
id: catalogo-y-linaje
titulo: Catálogo y linaje
fase: 4
nivel: intermedio
rutas: [de, core]
prerequisitos: [data-warehouse]
tags: [gobierno, metadatos, linaje, descubrimiento]
resumen: El catálogo dice qué datos existen y de quién son; el linaje dice de dónde vienen y qué se rompe al cambiarlos, columna a columna.
fuentes: ["Dehghani (2022), 'Data Mesh'", "Reis & Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

El catálogo responde «¿qué datos tengo, quién los usa y qué significan?» y el linaje responde
«¿de dónde sale este número y qué se rompe si cambio aquello?».

## La idea

En una empresa mediana hay 800 tablas y nadie sabe qué son 300 de ellas. Cuando alguien pregunta
«¿este `ingresos_netos` incluye devoluciones?», la respuesta es un hilo de mensajes que acaba en
«pregúntale a Marta, que se fue en marzo». Ese es el problema que resuelven el catálogo y el
linaje, y es un problema de tiempo: cada pregunta sin respuesta cuesta media hora de tres
personas.

**Catálogo.** Un inventario con metadatos por conjunto de datos: nombre, descripción, dueño,
esquema, grano (una fila por pedido, por pedido y línea, por día), clasificación —¿contiene datos
personales?—, frescura, resultados de calidad y quién lo consulta. Lo que lo hace útil no es la
cantidad de campos, sino que tenga **dueño** y **grano**: sin dueño no hay a quién preguntar, y
sin grano cualquier suma que hagas encima puede estar contando doble.

**Linaje.** El grafo dirigido de «esto se construye a partir de aquello». En las herramientas
modernas es a nivel de **columna**, no sólo de tabla, y eso cambia lo que se puede responder. Dos
usos, que son las dos direcciones del grafo:

- **Impacto (hacia abajo).** Si borro o cambio `clientes.email`, ¿qué se rompe? Son todos los
  descendientes: tablas, vistas, informes y extractos. Se calcula recorriendo el grafo desde el
  nodo.
- **Origen (hacia arriba).** Este informe dice que el margen cayó un 3 %; ¿de qué tablas y de qué
  fuentes sale ese número? Son los ascendientes. Sin eso, depurar una cifra es arqueología.

Hay tres formas de obtener el linaje, y conviene saber cuál tienes:

1. **Declarado.** Lo escribe una persona en un fichero o en una herramienta. Se queda obsoleto la
   primera semana que alguien tiene prisa.
2. **Inferido del SQL.** Un analizador lee los `FROM`, `JOIN` y `SELECT` de los modelos. dbt lo
   hace de serie con `ref()` (ver [[dbt-y-transformacion]]), y es el enfoque que mejor relación
   tiene entre coste y fiabilidad. Su punto débil es el SQL generado dinámicamente con cadenas de
   texto: ahí no hay nada que analizar.
3. **Observado en tiempo de ejecución.** Qué leyó y qué escribió cada trabajo, según el plan de
   ejecución o los registros de acceso. Es el más fiable y el más caro de montar.

Un grafo de linaje es un **DAG**: dirigido y sin ciclos. Si aparece un ciclo, o el modelo está mal
o el analizador se ha equivocado. Detectar el ciclo es en sí mismo una prueba de calidad, y
además es obligatorio: con un ciclo, «todo lo que depende de esta columna» devuelve media empresa.

:::trampa
El catálogo mantenido a mano se desactualiza en dos semanas y a partir de ahí es peor que no
tenerlo, porque la gente confía en él. Los metadatos técnicos —esquema, columnas, tamaños— se
extraen del sistema (`information_schema`, el manifiesto del proyecto, el plan de ejecución). Lo
que hay que escribir a mano es sólo lo que una máquina no puede adivinar: descripción de negocio,
grano, dueño y clasificación.
:::

## Definición formal

Un linaje a nivel de tabla es un grafo `G = (V, E)`:

- `V` — los nodos. En linaje de tabla, cada nodo es una tabla, una vista, un fichero o un modelo;
  en linaje de columna, cada nodo es un par `(tabla, columna)`. Las cifras de esta ficha (480
  tablas, 1.930 aristas, 23 nodos afectados) son de linaje de tabla: el impacto de
  `clientes.email` se calcula sobre el grafo de columna y se agrega por tabla para contarlo.
- `E` — las aristas dirigidas. `u → v` significa «`v` se construye leyendo `u`». La dirección va
  del origen al destino, igual que el flujo del dato.

Sobre ese grafo se definen las dos consultas que se usan a diario. El **impacto** de un nodo `u`
es el conjunto de todos los nodos alcanzables desde él:

:::formula
impacto(u) = { v ∈ V : existe un camino de u a v }
:::

Y el **origen** de un nodo `v` es el conjunto de nodos desde los que se puede llegar a él:

:::formula
origen(v) = { u ∈ V : existe un camino de u a v }
:::

Símbolos:

- `u`, `v` — nodos del grafo (tablas, o pares de tabla y columna).
- `camino` — una secuencia de aristas dirigidas consecutivas. Si el grafo tiene un ciclo, el
  conjunto deja de ser finito y útil.
- `V`, `E` — el conjunto de nodos y el de aristas.

Dos propiedades que hay que poder comprobar en cualquier catálogo con linaje:

:::formula
G es acíclico   y   todo nodo de V tiene un dueño asignado
:::

## Ejemplo

Un almacén con **480 tablas** y **1.930 aristas** de linaje. La columna `clientes.email` está
clasificada como dato personal. Su impacto se calcula sobre el grafo de columnas y se agrega por
tabla: son **23 tablas afectadas en 4 saltos**:

| Capa | Nodos afectados |
| --- | --- |
| Vistas de staging | 6 |
| Tablas intermedias | 9 |
| Tablas de consumo | 5 |
| Extractos enviados a terceros | 3 |
| Total | 23 |

Con ese dato, la pregunta «¿dónde está el correo de mis clientes?» se responde en un minuto en
lugar de convertirse en un proyecto de tres semanas. Y para una petición de borrado por
protección de datos, la lista de sitios donde hay que borrar sale del mismo grafo (ver
[[gobierno-y-privacidad]]).

El detalle que sorprende a todo el mundo la primera vez: de esas 23 tablas, **12 usan `SELECT *`**.
Eso significa que no se puede saber por el SQL si consumen `email` o no, y por tanto el impacto
real tiene que comprobarse nodo a nodo. El `SELECT *` destruye el linaje de columna, y es una
razón técnica —no estética— para no usarlo en modelos de producción.

## Código

```python verificable
# Linaje a nivel de tabla: cada nodo apunta a los que se construyen a partir de el.
linaje = {
    "raw_clientes": ["stg_clientes"],
    "stg_clientes": ["dim_cliente", "int_pedidos"],
    "raw_pedidos":  ["int_pedidos"],
    "int_pedidos":  ["fact_ventas"],
    "dim_cliente":  ["fact_ventas"],
    "fact_ventas":  ["informe_margen"],
}

def recorrer(inicio, grafo):
    """Nodos alcanzables desde 'inicio', sin repetir. Es el impacto o el origen."""
    vistos, pila = set(), [inicio]
    while pila:
        nodo = pila.pop()
        for siguiente in grafo.get(nodo, []):
            if siguiente not in vistos:
                vistos.add(siguiente)
                pila.append(siguiente)
    return vistos

# Hacia abajo: que se rompe si cambio raw_clientes.
print("impacto:", sorted(recorrer("raw_clientes", linaje)))
# -> impacto: ['dim_cliente', 'fact_ventas', 'informe_margen', 'int_pedidos', 'stg_clientes']
print("nodos afectados:", len(recorrer("raw_clientes", linaje)))   # -> nodos afectados: 5

# Hacia arriba: de donde sale el informe. Se recorre el grafo con las aristas invertidas.
inverso = {}
for origen, destinos in linaje.items():
    for destino in destinos:
        inverso.setdefault(destino, []).append(origen)
print("origenes:", sorted(recorrer("informe_margen", inverso)))
# -> origenes: ['dim_cliente', 'fact_ventas', 'int_pedidos', 'raw_clientes', 'raw_pedidos', 'stg_clientes']
```

```python verificable
# Auditoria del catalogo: un listado sin dueno ni descripcion no responde a nada.
catalogo = [
    {"tabla": "fact_ventas", "dueno": "equipo-ventas", "descripcion": True,  "pii": False},
    {"tabla": "dim_cliente", "dueno": "equipo-crm",    "descripcion": True,  "pii": True},
    {"tabla": "tmp_extract", "dueno": None,            "descripcion": False, "pii": True},
    {"tabla": "int_pedidos", "dueno": "equipo-ventas", "descripcion": False, "pii": False},
]

print("sin dueno:", [t["tabla"] for t in catalogo if not t["dueno"]])
# -> sin dueno: ['tmp_extract']
print("sin descripcion:", [t["tabla"] for t in catalogo if not t["descripcion"]])
# -> sin descripcion: ['tmp_extract', 'int_pedidos']
print("con datos personales y sin dueno:", [t["tabla"] for t in catalogo if t["pii"] and not t["dueno"]])
# -> con datos personales y sin dueno: ['tmp_extract']
```

## Errores típicos

- **Mantener el catálogo a mano.** Se desactualiza en cuanto alguien crea una tabla un viernes.
  Los metadatos técnicos se extraen del sistema; a mano se escriben sólo el grano, el dueño, la
  descripción de negocio y la clasificación.
- **Linaje sólo a nivel de tabla.** Nueve de cada diez incidentes son de una columna concreta.
  Sin nivel de columna, «qué se rompe si cambio esto» devuelve la tabla entera y no sirve para
  decidir.
- **Confundir catálogo con diccionario de datos.** Un listado de columnas con su tipo, sin dueño,
  sin grano y sin descripción de negocio, no responde a ninguna pregunta real. Es un volcado de
  `information_schema`, no un catálogo.
- **Clasificar los datos personales a posteriori.** La clasificación forma parte del contrato con
  el consumidor ([[contratos-de-datos]]), no de una auditoría anual. Si se añade después, ya hay
  correos de clientes copiados en sitios que nadie controla.
- **Creer que el linaje declarado es el real.** Lo que la gente escribe en la documentación y lo
  que el trabajo lee de verdad divergen el mismo día en que se escribe la documentación. El
  linaje útil es el que se deduce del código o de la ejecución.
- **No comprobar que el grafo es acíclico.** Un ciclo convierte el cálculo de impacto en una lista
  interminable y suele indicar un modelo recursivo mal montado o un analizador que se ha liado
  con el SQL dinámico.

## Comprueba que lo sabes

:::quiz
p: Quieres saber qué informes se romperían si eliminas la columna `email` de la tabla de clientes. ¿En qué dirección recorres el linaje?
o: Hacia arriba, siguiendo los orígenes de la columna
o: Hacia abajo, siguiendo todos los nodos que se construyen a partir de ella
o: En las dos direcciones, porque el linaje no es dirigido
a: 2
e: El impacto de un cambio se calcula con los descendientes: todo lo que lee esa columna directa o indirectamente. Hacia arriba se responde la pregunta contraria, de dónde sale un número que ya está mal. El linaje es dirigido, del origen al destino, y esa dirección es la que hace que las dos preguntas sean distintas.
:::

:::quiz
p: ¿Por qué un `SELECT *` en los modelos de producción estropea el linaje de columna?
o: Porque es más lento que enumerar las columnas
o: Porque el análisis estático no puede saber qué columnas consume realmente el modelo
o: Porque cambia el orden de las columnas en la tabla de salida
a: 2
e: Con `SELECT *` el analizador sólo ve «todas las columnas»: si añades una columna al origen, el modelo la arrastra sin que nadie lo haya decidido, y al revés, no se puede saber si una columna concreta se usa. El impacto real hay que comprobarlo nodo a nodo, que es justo lo que el linaje evitaba.
:::

:::nota
El catálogo y el linaje se alimentan de lo mismo: los metadatos que genera el propio pipeline. Si
tu proyecto de transformación ya declara dependencias (como `ref()` en dbt) y extrae los esquemas,
el 80 % del catálogo sale gratis. Lo que no sale gratis, y es lo que de verdad se usa, es el
dueño, el grano y la descripción de negocio.
:::
