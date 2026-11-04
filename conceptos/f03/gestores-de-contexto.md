---
id: gestores-de-contexto
titulo: Gestores de contexto y liberación de recursos
fase: 3
nivel: intermedio
rutas: [core, de]
prerequisitos: [funciones-y-modulos, errores-y-depuracion]
tags: [python, recursos, limpieza, ficheros]
resumen: El bloque with garantiza que el recurso se suelte al salir, aunque el cuerpo falle a mitad, y evita que un proceso largo se quede sin descriptores ni conexiones.
fuentes: ["Ramalho (2022), 'Fluent Python', 2ª ed., cap. 18", "Python Software Foundation, 'The Python Language Reference: The with statement'", "Lutz (2013), 'Learning Python', cap. 34"]
---

## En una frase

Un gestor de contexto es el objeto que se encarga de soltar el recurso al salir del bloque
`with`, tanto si el cuerpo termina bien como si revienta a mitad.

## La idea

Un proceso de datos abre un fichero por cada fichero que encuentra en una carpeta: 1.200
fragmentos Parquet de una partición diaria. El código abre, lee, transforma y cierra, y funciona
durante meses. Un día, un fragmento llega corrupto y la lectura lanza una excepción justo entre
el `open` y el `close`. El `close` no se ejecuta —nadie lo va a ejecutar, porque la excepción se
lleva por delante el resto de la función—, el pipeline muere y el fichero queda abierto. Si eso
pasa con uno da igual; si pasa con doscientos, el proceso agota los descriptores de fichero
(el límite típico en Linux es 1.024 por proceso) y a partir de ahí **cualquier** `open` falla,
incluso los que no tienen nada que ver. El traceback señala el `open` número 1.025 y no el
`close` que nunca ocurrió, así que el mensaje te manda al sitio equivocado.

La solución pasa por hacer imposible olvidarlo, no por acordarse de cerrar. El bloque `with` es azúcar
sobre el `try`/`finally` que escribirías a mano, con una diferencia que importa: no se puede
saltar el `finally` por descuido ni equivocarse de indentación. El objeto que va después de
`with` implementa dos métodos:

- **`__enter__`** adquiere el recurso y devuelve lo que se asigna a la variable (`as r`). Puede
  ser el propio objeto o algo distinto: `open()` devuelve el fichero; un gestor de conexiones
  puede devolver una conexión del fondo.
- **`__exit__`** lo suelta. Se ejecuta **siempre** que `__enter__` haya terminado bien: al salir
  del bloque, al hacer `return`, al propagarse una excepción o al saltar un `break`. Recibe tres
  argumentos con la excepción (tipo, valor y traza) o tres `None` si todo fue bien, y su valor de
  retorno decide si la excepción sigue su curso: `None` o `False` la dejan pasar, cualquier cosa
  que evalúe a verdadero **la absorbe**.

Ese último detalle es el arma de doble filo. Devolver `True` está pensado para gestores que
quieren convertir un error en algo controlado, pero si lo haces sin querer —por ejemplo
`return self.cerrar()`, donde `cerrar()` devuelve `True` cuando todo va bien— el error
desaparece sin ruido: el programa continúa como si nada y el fallo reaparece más tarde, lejos y
disfrazado. Por eso conviene devolver `False` explícitamente en lugar de dejar que el valor de
retorno de un cierre accidental decida por ti.

Con varios bloques anidados, el orden es el de una pila: **el último que entra es el primero que
sale**. La razón es que así el recurso interno se suelta antes que el
externo. Si cierras el fichero antes que el lector que lo envuelve, el lector seguirá pidiendo
datos a un fichero cerrado.

:::trampa
`with conexion:` **no cierra la conexión**. En `sqlite3`, en `psycopg2` y en la mayoría de los
clientes de bases de datos, ese `with` es un gestor de **transacción**: confirma al salir bien y
deshace al salir mal, pero la conexión sigue abierta y vuelve a estar disponible. Si lo usas como
si cerrara, cada ejecución del pipeline deja una conexión viva hasta que el servidor rechaza
nuevas conexiones. Para cerrar de verdad hay que envolver la conexión en un gestor propio o usar
`contextlib.closing`.
:::

## Definición formal

Un gestor de contexto es cualquier objeto con `__enter__` y `__exit__`. La equivalencia exacta
del bloque es esta:

:::formula
with G as r:  C   ≡   r = G.__enter__() ;  try:  C  finally:  G.__exit__(None, None, None)
:::

Y cuando el cuerpo lanza una excepción `E`, el gestor recibe sus tres datos y su valor de
retorno decide el destino del error:

:::formula
__exit__(E.tipo, E, E.traza) devuelve True  ⇒  E se absorbe;  False o None  ⇒  E se propaga
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube / cambia… |
| --- | --- | --- | --- |
| `G` | El gestor de contexto: el objeto que va después de `with` | no aplica | Si `__enter__` falla, `__exit__` **no** se llama y lo que se hubiera adquirido a medias se queda suelto |
| `r` | Lo que `__enter__` devuelve y se asigna con `as` | el recurso que sea | Si `__enter__` devuelve `None` (olvidar el `return self`), `as r` deja `None` y el cuerpo falla al primer uso |
| `C` | El cuerpo del bloque: el código que usa el recurso | no aplica | Cuanto más largo, más probable es una salida por excepción o por `return`, y más vale que la liberación no dependa de ti |
| `E.tipo`, `E`, `E.traza` | Clase, instancia y traza de la excepción que salió de `C` | no aplica | Si `C` no falla, los tres llegan como `None`: el mismo `__exit__` sirve para los dos caminos |
| valor devuelto por `__exit__` | Si la excepción se absorbe o se propaga | booleano | Si pasa de `False` a `True`, el error deja de verse: es la diferencia entre un fallo ruidoso y un descuadre silencioso |
:::

Una precisión que se pasa por alto: `__exit__` se llama **una vez por cada `__enter__` que haya
terminado bien**. Si la excepción ocurre dentro de `__enter__` —por ejemplo, al abrir el fichero
número 1.025— el `__exit__` correspondiente no se ejecuta, porque nunca hubo nada que soltar. Por
eso la adquisición tiene que ser atómica: o consigues todo el recurso o no tocas nada.

## Ejemplo

Tres bloques anidados que abren un fichero, leen la cabecera y validan las filas, y una excepción
en la validación. Lo que se imprime, en orden:

```
entra abrir fichero
entra leer cabecera
entra validar filas
sale validar filas      <- la excepción no impide la salida
sale leer cabecera
sale abrir fichero
```

La pila se vacía de dentro hacia fuera, y da igual por dónde se salga: `return`, `break` o
excepción. Si el mismo código se escribe con `open(...)` a mano y un `close()` al final del
bloque, la salida por excepción se salta el `close` y el fichero queda abierto. Con 1.200
fragmentos por tanda, el proceso falla en el 1.025 con `OSError: Too many open files`, que es un
mensaje que habla del síntoma y no de la causa.

El segundo caso es el que más cuesta encontrar, así que conviene mirarlo despacio. Dos
funciones constructoras de contexto, una sin `try`/`finally` alrededor del `yield` y otra con él,
y un cuerpo que lanza una excepción:

```
tomo recurso            <- mal: se anuncia la limpieza
tomo recurso            <- bien
suelto recurso          <- solo el bien limpia
```

La primera no imprime su «suelto recurso»: cuando el cuerpo revienta, `contextlib` vuelve a
lanzar la excepción **dentro** del generador, en el punto del `yield`, y el código que hay
después de esa línea no llega a ejecutarse. La limpieza no vive en el cuerpo del bloque, sino en
el código que va después del `yield`; y sin envolver ese `yield` en un `try`/`finally`, ese código
solo corre cuando el cuerpo termina bien.

:::figura
fichero: gestores-contexto-orden-de-salida
pie: A la izquierda, la altura de la escalera es el número de bloques with abiertos: la línea sube al entrar en cada uno y baja al salir, siempre en orden inverso, y la raya roja marca el punto donde el cuerpo lanza una excepción, que no cambia nada del descenso. A la derecha, las cuatro combinaciones posibles entre lo que hace el cuerpo y lo que devuelve __exit__: las tres primeras sueltan el recurso y dejan pasar el error; la cuarta, en rojo, lo suelta pero se traga la excepción, y ese error desaparecido es el que reaparece tres semanas después en otro sitio.
fuente: figuras/gestores-de-contexto-1.py
:::

## Código

```python verificable
# Un gestor escrito a mano: __enter__ entrega el recurso y __exit__ lo suelta siempre.
class Pool:
    def __init__(self, nombre):
        self.nombre = nombre
        self.prestado = False

    def __enter__(self):
        self.prestado = True
        print("presto", self.nombre)
        return self

    def __exit__(self, tipo, valor, traza):
        self.prestado = False
        print("devuelvo", self.nombre)
        return False        # False: si habia excepcion, sigue su curso

pool = Pool("conexion")
try:
    with pool as p:
        print("dentro: prestado =", p.prestado)
        raise ValueError("consulta mal escrita")
except ValueError as e:
    print("la excepcion llego fuera:", e)
print("fuera: prestado =", pool.prestado)
# -> presto conexion
# -> dentro: prestado = True
# -> devuelvo conexion
# -> la excepcion llego fuera: consulta mal escrita
# -> fuera: prestado = False
```

```python verificable
import contextlib

# Anidados: entran en orden y salen al reves (LIFO), pase lo que pase.
@contextlib.contextmanager
def etapa(nombre):
    print("entra", nombre)
    try:
        yield nombre.upper()        # lo que hay antes del yield es __enter__
    finally:
        print("sale", nombre)       # lo que hay despues es __exit__

with etapa("abrir fichero") as a, etapa("leer cabecera") as b:
    print("trabajando con", a, "y", b)
# -> entra abrir fichero / entra leer cabecera / trabajando con ABRIR FICHERO y LEER CABECERA
# -> sale leer cabecera / sale abrir fichero

# Sin try/finally, la limpieza que va despues del yield no se ejecuta si el cuerpo falla.
@contextlib.contextmanager
def sin_proteccion(nombre):
    print("tomo", nombre)
    yield nombre
    print("suelto", nombre)         # no se imprime si el cuerpo lanza

try:
    with sin_proteccion("recurso"):
        raise ValueError("falla el cuerpo")
except ValueError:
    pass
# -> tomo recurso   (y nunca "suelto recurso")
```

```python verificable
import sqlite3

# with conexion: es una TRANSACCION, no un cierre. La conexion sigue viva al salir.
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pedidos (id INTEGER)")

with con:                                   # confirma al salir sin excepcion
    con.execute("INSERT INTO pedidos VALUES (1)")

try:
    with con:                               # deshace al salir con excepcion
        con.execute("INSERT INTO pedidos VALUES (2)")
        raise ValueError("el lote venia mal")
except ValueError:
    pass

print("filas confirmadas:", con.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0])
# -> 1
print("la conexion sigue abierta:", con.execute("SELECT 1").fetchone()[0])
# -> 1
con.close()                                 # cerrar es cosa tuya, no del with
```

## Errores típicos

- **Fiarse de `with conexion:` para cerrar la conexión.** Es un gestor de transacción: confirma o
  deshace, y la conexión vuelve al fondo. En un servicio que atiende peticiones, el fondo se
  agota y el servidor empieza a rechazar conexiones nuevas. Envuelve la conexión en un gestor
  propio que la cierre, o usa `contextlib.closing`.
- **Devolver algo verdadero desde `__exit__` sin querer.** `return self.cerrar()` donde `cerrar()`
  devuelve `True` cuando todo fue bien convierte cualquier error del cuerpo en un silencio. El
  método debería devolver `False` o nada, y tragarse una excepción solo cuando absorberla sea
  justo el propósito del gestor.
- **Escribir `@contextmanager` sin `try`/`finally` alrededor del `yield`.** La limpieza se salta
  justo en el caso en el que más falta hace, el de la excepción. Todo lo que va después del
  `yield` tiene que estar dentro de un `finally`.
- **Sacar el recurso del bloque y usarlo después.** `with open(ruta) as f: return f` devuelve un
  fichero ya cerrado: la primera lectura falla con `ValueError: I/O operation on closed file`. Si
  necesitas devolver contenido, léelo dentro del bloque; si necesitas devolver el objeto, la
  propiedad tiene que ser de quien lo recibe.
- **Reutilizar un gestor que no es reentrante.** Un `with open(...)` no se puede volver a abrir
  donde se cerró, y un gestor que guarda estado en atributos de instancia (como el `Pool` del
  ejemplo) se rompe si dos bloques lo usan a la vez. Para compartir recursos entre bloques, un
  objeto nuevo por uso o un fondo de recursos que sí sepa atender a varios.
- **Confundir «soltar» con «guardar».** Un gestor de contexto limpia, pero no siempre confirma:
  en una transacción, salir del `with` con excepción normalmente significa deshacer, y eso es una
  decisión de negocio, no de sintaxis. Lee qué hace el `__exit__` del gestor que estás usando
  antes de darlo por hecho.

## Comprueba que lo sabes

:::quiz
p: ¿Cuándo se ejecuta el método __exit__ de un gestor de contexto?
o: Solo si el cuerpo del bloque termina sin excepciones
o: Siempre que __enter__ haya terminado bien, salga el cuerpo como salga
o: Solo si el cuerpo lanza una excepción que hay que deshacer
a: 2
e: El bloque with equivale a un try/finally, y el finally se ejecuta en los dos caminos: salida normal, return, break o excepción. La única excepción es que __enter__ falle: en ese caso no hubo nada que adquirir y __exit__ no se llama, por eso la adquisición tiene que ser atómica.
:::

:::quiz
p: Escribes un gestor con @contextlib.contextmanager y pones la limpieza después del yield, sin try/finally. ¿Qué pasa si el cuerpo del with lanza una excepción?
o: La limpieza se ejecuta igual, porque contextlib la garantiza
o: La limpieza no se ejecuta: la excepción se relanza dentro del generador, en el yield, y el código posterior se salta
o: La limpieza se ejecuta, pero después de que la excepción llegue al exterior
a: 2
e: contextlib no añade ningún finally por su cuenta: lanza la excepción dentro del generador en el punto del yield. Si no la capturas con try/finally, el generador termina ahí y el código que sigue al yield nunca corre. Por eso la limpieza de un @contextmanager va siempre en un finally.
:::

:::quiz
p: Un servicio abre conexiones con with conexion: en cada petición y a las tres horas el servidor de base de datos rechaza conexiones nuevas. ¿Qué está pasando?
o: El with de la conexión gestiona la transacción, no el cierre: cada petición deja la conexión abierta hasta agotar el fondo
o: El with cierra la conexión, pero el servidor tarda en enterarse y las cuenta como activas
o: El with hace COMMIT y eso abre una conexión nueva cada vez
a: 1
e: En los clientes de bases de datos, el gestor de contexto de una conexión suele confirmar o deshacer la transacción y devolver la conexión, no cerrarla. El número de conexiones vivas crece con las peticiones hasta el límite del servidor. La solución es un gestor propio que cierre de verdad, o un fondo de conexiones con su propio ciclo de vida.
:::
