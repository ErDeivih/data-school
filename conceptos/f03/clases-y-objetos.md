---
id: clases-y-objetos
titulo: Clases y objetos
fase: 3
nivel: intermedio
rutas: [core, de, ds, alg]
prerequisitos: [tipos-y-estructuras-python, vistas-y-copias]
tags: [python, objetos, estado]
resumen: Una clase es el molde, cada objeto guarda su propio estado y self es cómo un método sabe sobre qué objeto trabaja.
fuentes: ["Ramalho (2022), 'Fluent Python', 2.ª edición", "Lutz (2013), 'Learning Python', 5.ª edición"]
---

## En una frase

Una clase es el molde donde escribes qué datos guarda un objeto y qué sabe hacer con ellos; cada
objeto fabricado con ese molde tiene sus propios valores, y `self` es la forma que tiene un método
de saber sobre cuál de ellos está trabajando.

## La idea

Piensa en un formulario en blanco. El formulario define qué casillas hay que rellenar —nombre,
fecha, importe— y qué trámites se pueden hacer con él: firmarlo, sellarlo, archivarlo. El
formulario en blanco no es ningún trámite concreto, es la plantilla. Cada formulario relleno sí:
tiene su nombre, su fecha y su importe, y firmar uno no cambia los demás.

Eso es exactamente una clase y eso son los objetos. La clase es el formulario en blanco; los
objetos son los formularios rellenos. Los datos que guarda cada objeto se llaman **atributos** y
las acciones que sabe hacer se llaman **métodos**.

Esto importa aunque no vayas a escribir clases propias, porque las librerías que usas te devuelven
objetos continuamente. Cuando escribes `df.groupby("ciudad")`, pandas no te devuelve una tabla: te
devuelve un objeto agrupador que además sabe calcular `.mean()`, `.sum()` o `.size()`. Cuando
escribes `fig.savefig("grafico.png")`, la figura es un objeto con su método. Una fecha tiene
`.strftime()`, una serie de pandas tiene `.rolling(7)`. Un método no es una función suelta que
recibe datos: es una acción pegada a unos datos concretos.

Y aquí aparece `self`, la palabra que más confunde al principio. Cuando escribes `ana.ingresar(50)`,
Python lo traduce internamente a `Cuenta.ingresar(ana, 50)`: el objeto va como primer argumento.
Por eso el primer parámetro de todo método se llama `self` y por eso vale exactamente el objeto que
recibe la llamada. No es una palabra mágica: es un parámetro más, con un nombre acordado. Si lo
olvidas al definir el método, Python pasa el objeto igualmente y te salta un `TypeError` que habla
de «argumentos posicionales» y que no menciona la palabra self por ningún lado.

La segunda idea es el **estado**. Una función pura recibe argumentos y devuelve un resultado sin
recordar nada; un objeto recuerda. `ana.ingresar(50)` no devuelve un saldo nuevo, cambia el saldo
que `ana` lleva dentro. Esa memoria es lo que hace útil a un objeto y también lo que hace que un
método pueda mentirte con un `return`: si el método muta y no devuelve nada, la llamada vale `None`
aunque el trabajo esté hecho.

De ahí sale la única trampa que de verdad cuesta cara: **dónde se crea el atributo**. Si escribes
`movimientos = []` en el cuerpo de la clase, esa lista se crea una sola vez, cuando Python lee la
clase, y todos los objetos la comparten: un `append` desde un objeto aparece en el otro. Si escribes
`self.movimientos = []` dentro de `__init__`, cada objeto que nace estrena su propia lista. La
diferencia entre esas dos líneas es la diferencia entre dos cuentas independientes y una lista
común que nadie pidió. Es el mismo problema de compartir que ya viste con las listas en
[[tipos-y-estructuras-python]] y con los nombres que apuntan al mismo objeto en [[vistas-y-copias]].

## Definición formal

- **Clase** — plantilla que declara los atributos y los métodos de un tipo de objeto.
- **Objeto** o **instancia** — valor concreto creado a partir de una clase. Se crea llamándola:
  `ana = Cuenta("Ana")`.
- **Atributo de instancia** — dato guardado dentro de un objeto concreto (`self.saldo`). Cada
  instancia tiene el suyo.
- **Atributo de clase** — dato definido en el cuerpo de la clase, fuera de `__init__`. Existe una
  sola vez y todos los objetos lo ven.
- **Método** — función definida dentro de la clase. Su primer parámetro es la instancia que recibe
  la llamada.
- **`__init__`** — método especial que Python ejecuta al crear el objeto, para dejarlo con sus
  atributos iniciales.
- **`self`** — nombre del primer parámetro de un método: dentro del método vale el objeto que
  recibe la llamada.
- **`isinstance(objeto, Clase)`** — comprueba si el objeto se creó con esa clase (o con una que
  hereda de ella).

La llamada con punto y la llamada a la clase son la misma cosa:

:::formula
objeto.método(a)   ≡   Clase.método(objeto, a)
:::

:::parametros
| Símbolo | Qué es | Unidades | Qué pasa al cambiarlo |
| --- | --- | --- | --- |
| `Clase` | El molde: declara atributos y métodos | — | Un método nuevo lo tienen todos los objetos creados a partir de ahí |
| `objeto` | Una instancia concreta, como `ana` | — | Cada objeto nuevo estrena sus propios atributos de instancia |
| `self` | Primer parámetro del método; vale el objeto que recibe la llamada | — | Si lo quitas de la definición, la llamada falla con `TypeError` |
| `atributo` | Dato guardado en el objeto, como `self.saldo` | las del dato | Reasignarlo cambia solo ese objeto |
| `atributo de clase` | Dato declarado en el cuerpo de la clase | las del dato | Si es mutable, todos los objetos ven el mismo valor y se pisan |
| `a` | Argumento que le pasas al método, como `cantidad` | las del argumento | El método decide qué hacer con él: sumarlo, validarlo o ignorarlo |
| valor devuelto | Lo que el método entrega con `return` | las del resultado | Sin `return` es `None`, aunque el objeto haya cambiado por dentro |
:::

## Ejemplo

Dos cuentas con el mismo saldo inicial y un ingreso de 50 euros a la primera:

- `ana = Cuenta("Ana", 100.0)` y `luis = Cuenta("Luis", 100.0)`.
- `ana.ingresar(50.0)` deja el saldo de `ana` en **150,0** y el de `luis` en **100,0**: son dos
  atributos distintos, guardados en dos objetos distintos.
- `devuelto = ana.ingresar(50.0)` deja `devuelto` en `None` y el saldo de `ana` en **200,0**. El
  método hizo su trabajo, pero no devolvió nada: asignar su resultado es quedarse con `None`.

Ahora el caso que decide si has entendido los atributos. Seis días de ingresos:

```
ana:  10   0  25   5   0  15      total 55
luis:  0  20   0  10  30   0      total 60
```

- Con `movimientos = []` en el cuerpo de la clase, hay **una sola lista** y cada uno ve los
  ingresos del otro: los dos objetos acaban con **115** acumulados, y
  `ana.movimientos is luis.movimientos` es `True`.
- Con `self.movimientos = []` dentro de `__init__`, cada uno acumula lo suyo: `ana` acaba en
  **55** y `luis` en **60**.

:::figura
fichero: clases-y-objetos-atributo-compartido
pie: En el panel izquierdo las dos líneas se superponen exactamente, y esa es la señal de alarma: no hay dos listas, hay una que los dos objetos comparten, así que el saldo de Ana incluye los ingresos de Luis y acaba en 115 en vez de 55. En el derecho, con la lista creada en __init__, cada objeto sigue su propia curva y los totales son los que deberían ser. Si un gráfico de dos objetos que deberían ser independientes da una sola línea, el atributo está donde no debe.
fuente: figuras/clases-y-objetos-1.py
:::

## Código

```python verificable
class Cuenta:
    def __init__(self, titular, saldo=0.0):
        self.titular = titular          # atributo de instancia: cada objeto tiene el suyo
        self.saldo = saldo

    def ingresar(self, cantidad):
        self.saldo += cantidad          # modifica ESTE objeto y no devuelve nada
        return None


ana = Cuenta("Ana", 100.0)
luis = Cuenta("Luis", 100.0)

devuelto = ana.ingresar(50.0)
print("lo que devuelve ingresar:", devuelto)                    # -> None
print("saldo de ana:", ana.saldo, " saldo de luis:", luis.saldo)  # -> 150.0 y 100.0
print("la clase de ana:", type(ana).__name__)                   # -> Cuenta
```

:::claves
- `ana.ingresar(50.0)` devuelve `None`, no el saldo nuevo: el método muta el objeto y no tiene `return`. Si escribes `saldo = ana.ingresar(50.0)`, te quedas con `None` y el ingreso ya está hecho igualmente. Es el mismo estilo que `lista.append(x)`, que también cambia la lista y devuelve `None`.
- `ana` y `luis` son dos objetos distintos: `self.saldo += cantidad` modifica el atributo del objeto que recibe la llamada, y por eso el saldo de `luis` sigue en 100,0. Nada se comparte entre ellos salvo lo que esté declarado en el cuerpo de la clase.
- `self.titular = titular` **crea** el atributo en ese momento. Hasta que se ejecuta esa línea, `ana.titular` no existe: si te equivocas de nombre y escribes `self.titualr`, Python no avisa al definir la clase, solo falla más tarde con un `AttributeError`.
- `type(ana).__name__` da la clase del objeto como texto (`Cuenta`), mientras que `type(ana)` da la clase en sí. `isinstance(ana, Cuenta)` responde `True` y es lo que se usa para comprobar tipos.
- `saldo=0.0` en la firma de `__init__` es un valor por defecto, igual que en cualquier función: `Cuenta("Ana")` funciona y empieza en 0,0. Los valores por defecto se evalúan una sola vez al leer la clase, así que un valor mutable ahí (una lista) se compartiría entre todos los objetos y entre todas las llamadas.
:::

```python verificable
class CuentaMala:
    movimientos = []                 # atributo de CLASE: una sola lista para todos

    def __init__(self, titular):
        self.titular = titular

    def ingresar(self, cantidad):
        self.movimientos.append(cantidad)   # busca la lista en la clase, no la crea


class CuentaBuena:
    def __init__(self, titular):
        self.movimientos = []        # cada objeto estrena la suya

    def ingresar(self, cantidad):
        self.movimientos.append(cantidad)


a, b = CuentaMala("Ana"), CuentaMala("Luis")
a.ingresar(30)
b.ingresar(10)
print("mala - lista de a:", a.movimientos, " lista de b:", b.movimientos)  # -> [30, 10] y [30, 10]
print("mala - es la misma lista:", a.movimientos is b.movimientos)          # -> True

c, d = CuentaBuena("Ana"), CuentaBuena("Luis")
c.ingresar(30)
d.ingresar(10)
print("buena - lista de c:", c.movimientos, " lista de d:", d.movimientos)  # -> [30] y [10]
print("buena - es la misma lista:", c.movimientos is d.movimientos)         # -> False
```

## Errores típicos

- **Olvidar `self` en la definición de un método.** `def ingresar(cantidad):` parece razonable,
  pero Python llama siempre con el objeto delante y responde
  `TypeError: ingresar() takes 1 positional argument but 2 were given`. El mensaje cuenta los
  argumentos, no menciona `self`; si ves «2 were given» en un método de un solo parámetro, es esto.
- **Declarar una lista o un diccionario en el cuerpo de la clase.** `movimientos = []` fuera de
  `__init__` se crea una vez y lo comparten todas las instancias. Empieza a fallar lejos de su
  causa, cuando un objeto tiene datos del otro. Los atributos mutables van siempre dentro de
  `__init__`, con `self.`.
- **Asignar el resultado de un método que muta.** `ana = ana.ingresar(50)` deja `ana` valiendo
  `None` y pierdes el objeto. Mira la firma: si el método no tiene `return`, no esperes un valor.
- **Creer que `==` compara el contenido de dos objetos.** Sin definir `__eq__`, `Cuenta("Ana") ==
  Cuenta("Ana")` es `False`, porque compara identidad (si son el mismo objeto en memoria), igual
  que `is`. Para comparar por contenido hay que definir `__eq__` a mano.
- **Escribir `Cuenta.saldo`.** El atributo vive en el objeto, no en la clase: eso lanza
  `AttributeError`. La clase solo tiene los métodos y los atributos declarados en su cuerpo.
- **Cambiar los atributos desde fuera del objeto.** `ana.saldo = -500` funciona (nada lo impide) y
  rompe cualquier regla que el método `ingresar` estuviera manteniendo. Si el objeto tiene que
  cumplir una invariante, la comprobación va dentro del método y el código de fuera usa métodos.

:::practica
enunciado: Escribe una clase Sensor con un nombre y una lista de lecturas de temperatura, un método anade(temp) que guarde una lectura y un método media() que devuelva la media. Crea dos sensores, añade 20 y 22 al primero y 30 al segundo, e imprime la media de cada uno y si comparten la lista de lecturas.
pista: La lista tiene que nacer dentro de __init__ con self.lecturas = []; si la declaras en el cuerpo de la clase, los dos sensores compartirán la misma.
solucion: Con `def __init__(self, nombre): self.nombre = nombre; self.lecturas = []`, `def anade(self, temp): self.lecturas.append(temp)` y `def media(self): return sum(self.lecturas) / len(self.lecturas)`, la media del primer sensor es 21,0 y la del segundo 30,0, y `s1.lecturas is s2.lecturas` es False. Si la lista se hubiera declarado en el cuerpo de la clase, las dos medias serían 24,0 y la lista sería la misma para los dos.
:::

## Comprueba que lo sabes

:::quiz
p: Con `def ingresar(self, cantidad): self.saldo += cantidad`, ¿qué imprime `print(ana.ingresar(50))` si el saldo de ana era 100,0?
o: 150.0, porque el método devuelve el saldo actualizado
o: None, porque el método no tiene return aunque el saldo ya valga 150,0
o: Un error, porque no se puede imprimir el resultado de un método que modifica el objeto
a: 2
e: El método muta el atributo y no devuelve nada, así que la llamada vale None: el saldo de ana ya es 150,0, pero el valor que devuelve la expresión es None. Para ver el saldo hay que leer `ana.saldo` después de la llamada. Un método que muta y no devuelve nada no es un error: es el estilo de gran parte de la biblioteca estándar.
:::

:::quiz
p: Escribes `movimientos = []` en el cuerpo de la clase, fuera de `__init__`, y en un método haces `self.movimientos.append(x)`. ¿Qué ocurre con dos objetos de esa clase?
o: Cada objeto tiene su lista, porque `self` siempre crea un atributo nuevo
o: Los dos comparten la misma lista: el append de uno aparece en el otro
o: Da AttributeError, porque `movimientos` no está en `__init__`
a: 2
e: La lista se crea una sola vez, al leer la clase, y `self.movimientos` la encuentra en la clase porque el objeto no tiene una propia. Los dos objetos apuntan a la misma lista y los datos se mezclan. Escribir `self.movimientos = []` dentro de `__init__` crea una lista nueva por objeto, que es lo que se busca.
:::

:::quiz
p: ¿Por qué `df.groupby("ciudad").mean()` funciona sin pasar el DataFrame como argumento?
o: Porque `mean()` busca el último DataFrame que se haya creado
o: Porque `df` es el objeto que recibe la llamada y el método lo recibe como primer parámetro, su `self`
o: Porque `mean()` es una función global que pandas aplica a la variable `df`
a: 2
e: `df.groupby("ciudad")` devuelve un objeto agrupador, y sobre ese objeto se llama `mean()`. La llamada con punto pasa el objeto como primer argumento, exactamente igual que `Cuenta.ingresar(ana, 50)` equivale a `ana.ingresar(50)`. No hay ninguna variable global de por medio.
:::
