---
id: patrones-de-diseno
titulo: Patrones de diseño
fase: 11
nivel: avanzado
rutas: [alg]
prerequisitos: [principios-solid, tipos-y-estructuras-python]
tags: [diseno, arquitectura, vocabulario, acoplamiento]
resumen: Estrategia, fábrica, observador y repositorio: nombres cortos para problemas de diseño que ya se han resuelto mil veces, con sus consecuencias.
fuentes: ["Gamma, Helm, Johnson y Vlissides (1994), 'Design Patterns: Elements of Reusable Object-Oriented Software'", "Fowler (2002), 'Patterns of Enterprise Application Architecture'", "Evans (2003), 'Domain-Driven Design: Tackling Complexity in the Heart of Software'"]
---

## En una frase

Un patrón de diseño es el nombre de una solución repetida a un problema de diseño, junto con
sus consecuencias: sirve para decidir antes de escribir y para entenderse después, no para
rellenar carpetas de clases.

## La idea

En ajedrez, «horquilla» y «clavada» no son jugadas concretas: son nombres de situaciones que se
repiten, y cada uno trae implícito qué se gana y qué se arriesga. Decir «esto es una horquilla»
ahorra veinte frases y evita que el otro tenga que reconstruir la idea desde cero. Los patrones
de diseño hacen eso mismo con el software.

El catálogo clásico es el de Gamma, Helm, Johnson y Vlissides (1994), que recogieron 23
patrones y los agruparon en tres familias: **creacionales** (cómo se construyen los objetos),
**estructurales** (cómo se componen) y **de comportamiento** (cómo colaboran). Después llegaron
los patrones de aplicación empresarial: repositorio, unidad de trabajo, mapeador de datos,
capa anticorrupción. No son álgebra: son observaciones sobre código que ya se había escrito
muchas veces y que funcionaba.

Cuatro que aparecen cada semana:

1. **Estrategia.** Hay varias formas de hacer lo mismo —calcular un envío, una comisión, un
   descuento— y no quieres una cadena de condicionales que crece con cada variante. Se define
   una interfaz con un método y el algoritmo se inyecta desde fuera. El contexto deja de saber
   *cómo* se calcula.
2. **Fábrica.** Decidir qué clase concreta construir tiene que estar en un solo sitio: leer la
   extensión de un fichero para elegir el lector, o el motor configurado para elegir el conector
   de base de datos. Un `if` en la fábrica es aceptable; el mismo `if` repartido en diez sitios,
   no.
3. **Observador.** Un objeto cambia de estado y avisa a quien se haya suscrito, sin conocer a
   nadie en concreto. Es lo que hay detrás de los eventos de un pedido que disparan correo,
   inventario y analítica. Desacopla de verdad, y a la vez es una de las formas más rápidas de
   hacer que un flujo sea difícil de seguir: la llamada ya no está en el código, está en una
   lista.
4. **Repositorio.** El dominio pide «dame el pedido 42» y no sabe si detrás hay PostgreSQL, un
   fichero o una lista en memoria. La interfaz imita a una colección; la persistencia se queda
   fuera. Su precio es conocido: si la interfaz devuelve objetos del ORM o filtros del motor,
   ya no oculta nada y solo añade una capa.

La regla de oro: **el patrón se elige por el problema, no el problema por el patrón.** Un
patrón aplicado donde no hay problema es deuda técnica disfrazada de elegancia, y el caso más
caro es el Singleton usado como variable global con nombre bonito.

## Definición formal

Un patrón se describe con cuatro elementos: **nombre**, **problema** (cuándo aplica),
**solución** (la estructura y sus participantes) y **consecuencias** (lo que ganas y lo que
pagas). Sin el cuarto, no es un patrón: es una receta.

- **Estrategia.** Una interfaz `E` con una operación `ejecutar(entrada)`, `n` implementaciones
  intercambiables y un contexto `C` que recibe una `E` y delega en ella. El contexto no conoce
  la implementación; el cliente elige. Cumple el principio de abierto y cerrado de
  [[principios-solid]]: añadir una variante es añadir una implementación.
- **Fábrica.** Una función `f: Clave → Producto` que concentra la construcción. Los clientes
  dependen de la clave y del producto, nunca de los nombres de las clases concretas. La
  inversión de dependencias se apoya en ella.
- **Observador.** Un sujeto mantiene una colección de observadores y, al cambiar su estado,
  invoca una operación de cada uno. El acoplamiento es de una sola dirección: el sujeto no
  conoce a los observadores, los observadores sí conocen la interfaz del sujeto si quieren
  consultar el estado. Dos decisiones que hay que fijar por escrito: el **orden** de
  notificación (habitualmente no definido) y qué ocurre si un observador lanza una excepción
  (habitualmente detiene a los siguientes).
- **Repositorio.** Una interfaz con operaciones de colección sobre objetos de dominio
  (`añadir`, `obtener_por_id`, `buscar(criterio)`), implementada en la capa de infraestructura.
  La unidad de trabajo agrupa varios cambios para confirmarlos o descartarlos juntos.

Y la lista negra, porque también se nombra: **antipatrón**. Objeto dios, clase con 3.000
líneas; dependencia circular entre paquetes; `catch` vacío que se traga el error; copiar y pegar
en lugar de extraer. Ponerles nombre es la mitad de la cura.

## Ejemplo

Un pedido de 2,5 kg con tres tarifas de envío, donde la estrategia es la función de cálculo:

- tarifa «estandar»: 3,50 + 0,80 · 2,5 = 3,50 + 2,00 = **5,50 €**
- tarifa «express»: 9,00 + 2,00 · 2,5 = 9,00 + 5,00 = **14,00 €**
- tarifa «gratis»: **0,00 €**

La fábrica es el diccionario que traduce el nombre de la tarifa a la función. Añadir «envío
nocturno» es escribir una función y una entrada; la función que calcula el coste total no se
toca.

Cada tarifa es una recta con su pendiente, así que el coste crece con el peso a un ritmo distinto
en cada una. La fórmula de cualquiera de ellas es `coste = c_fija + c_kg · peso`, y el reparto de
símbolos es este:

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `peso` | Lo que pesa el pedido: el único dato que ven todas las estrategias | kg | Sube el coste en todas las tarifas de pago; en `gratis` no cambia nada |
| `c_fija` | La cuota de salida de la tarifa (3,50 en estandar, 9,00 en express) | € | Sube el coste con el mismo peso; no depende del pedido |
| `c_kg` | Lo que se cobra por kilo (0,80 en estandar, 2,00 en express) | €/kg | Sube el coste, y más rápido en express: adelanta el cruce con estandar |
| `coste` | Lo que se cobra por el envío, ya redondeado a dos decimales | € | Sube con el peso y con cualquiera de los dos coeficientes |
| `tarifa` | La función elegida por nombre; el precio todavía no está calculado | función | Cambia de recta, no de valor: por eso hay que llamarla después |
:::

Dibujar las tres rectas es la forma más rápida de ver por qué el algoritmo tiene que ser un dato
y no un `if`:

:::figura
fichero: patrones-de-diseno-estrategia
pie: Izquierda, el coste de las tres tarifas según el peso del pedido: «gratis» es la horizontal del cero y las dos de pago no se cruzan, porque «express» tiene la cuota fija y el precio por kilo más altos y sale más cara en todo el rango de pesos. Derecha, los dos casos que se calculan a mano: a 2,5 kg la gratis cuesta 0,00 €, la estandar 5,50 € y la express 14,00 €; a 6 kg, 0,00 €, 8,30 € y 21,00 €. Lo que el peso cambia no es cuál es la más barata, sino cuánto cuestan las otras dos. La conclusión es que el contexto no puede decidir la tarifa: solo puede recibirla.
fuente: figuras/patrones-de-diseno-1.py
:::

Para el observador, un almacén que recibe tornillos: con la primera entrada de 3 unidades, sus
dos suscriptores reaccionan (uno escribe en el registro, el otro avisa de que hay que reponer
porque el total es menor que 5). Con la segunda entrada, el total llega a 7 y solo reacciona el
registro. Tres avisos en total, y el almacén no sabe qué hacen sus suscriptores.

## Código

```python verificable
# Estrategia: el algoritmo se inyecta y el contexto no sabe cual es.
# Las tres funciones tienen la misma firma (un peso, un numero): por eso son intercambiables.
def envio_estandar(peso): return 3.50 + 0.80 * peso    # cuota fija + precio por kilo
def envio_express(peso):  return 9.00 + 2.00 * peso    # misma forma, otros numeros
def envio_gratis(peso):   return 0.0                   # ignora el argumento: misma firma igual

# Fabrica: un solo sitio traduce la clave externa a la estrategia concreta.
# Ojo: el diccionario guarda FUNCIONES (sin parentesis), no el resultado de llamarlas.
TARIFAS = {"estandar": envio_estandar, "express": envio_express, "gratis": envio_gratis}

def tarifa(nombre):
    # Devuelve la funcion, no el precio: comprobar antes evita un KeyError poco claro.
    if nombre not in TARIFAS:
        raise ValueError(f"tarifa desconocida: {nombre}")
    return TARIFAS[nombre]

def coste_envio(peso, nombre):
    # Doble llamada: tarifa(nombre) da la funcion y (peso) la ejecuta con el peso.
    return round(tarifa(nombre)(peso), 2)

print("estandar 2.5 kg:", coste_envio(2.5, "estandar"))   # -> 5.5
print("express  2.5 kg:", coste_envio(2.5, "express"))    # -> 14.0
print("gratis   2.5 kg:", coste_envio(2.5, "gratis"))     # -> 0.0
```

:::claves
- La fábrica devuelve una **función**, no un número. `tarifa("express")` es un objeto
  llamable; si te olvidas de los paréntesis al usarlo, no hay error: te llevas la función
  a casa y el fallo aparece más tarde, al intentar operar con ella.
- En Python las funciones son valores: se guardan en un diccionario sin paréntesis. Si
  escribieras `{"express": envio_express(peso)}`, se ejecutaría **al construir el
  diccionario**, antes de que exista ningún `peso`, y el módulo fallaría al importarse.
- `coste_envio` encadena dos llamadas en una línea (`tarifa(nombre)(peso)`): la primera
  elige el algoritmo, la segunda lo ejecuta. Se lee de dentro hacia fuera.
- El orden de los argumentos es el de la firma: `coste_envio(2.5, "estandar")` es peso y
  luego nombre. Al revés no da un resultado raro: lanza `ValueError`.
- `round` aplica redondeo al par (bancario): `round(2.675, 2)` da `2.67`, no `2.68`. Para
  un precio grande apenas se nota; para cuadrar céntimos con Hacienda, sí.
- Añadir «envío nocturno» es una función más y una entrada más en el diccionario: la
  función que cobra no se toca. Eso es el principio de abierto y cerrado en la práctica.
:::

```python verificable
class Almacen:
    """Sujeto observable: no conoce a nadie en concreto, solo avisa."""
    def __init__(self):
        self._suscriptores = []
        self.existencias = {}

    def suscribir(self, funcion):
        self._suscriptores.append(funcion)      # guarda la funcion, no su resultado

    def recibir(self, producto, unidades):
        # get con valor por defecto: el producto nuevo entra con 0 en vez de dar KeyError.
        self.existencias[producto] = self.existencias.get(producto, 0) + unidades
        total = self.existencias[producto]
        # Aviso a todos; el sujeto no sabe que hace ninguno ni en que orden importa.
        for funcion in self._suscriptores:
            funcion(producto, total)

eventos = []

def registrar(producto, total):
    # append devuelve None: aqui el valor no importa, lo que cuenta es el efecto.
    eventos.append(f"log: {producto} llega a {total}")

def avisar_a_compras(producto, total):
    # Cada suscriptor decide si le afecta; el almacen no lo consulta antes.
    if total < 5:
        eventos.append(f"pedir mas {producto}")

almacen = Almacen()
almacen.suscribir(registrar)          # se pasan las funciones sin parentesis
almacen.suscribir(avisar_a_compras)
almacen.recibir("tornillos", 3)       # 3 < 5: avisan los dos suscriptores
almacen.recibir("tornillos", 4)       # total 7: solo registra el primero

for evento in eventos:
    print(evento)
print("avisos emitidos:", len(eventos))    # -> 3
```

```text
Repositorio: el dominio no ve el motor de base de datos.

class RepositorioPedidos(Protocol):
    def anadir(self, pedido: Pedido) -> None: ...
    def obtener_por_id(self, pedido_id: int) -> Pedido: ...
    def buscar_por_cliente(self, cliente_id: int) -> list[Pedido]: ...

class RepositorioPedidosSQL(RepositorioPedidos):   # infraestructura
    ...   # aqui viven el ORM, las consultas y las transacciones
```

## Errores típicos

- **Aplicar patrones por currículum.** Meter una fábrica abstracta, dos estrategias y un
  observador en un módulo de 300 líneas que solo tiene una variante. Cada indirección cuesta
  lectura; se paga cuando hay más de una implementación real o cuando se prevé una segunda con
  motivos.
- **Usar Singleton como variable global.** Se justifica con «solo debe haber una instancia» y
  acaba siendo estado compartido difícil de sustituir en un test. Si de verdad hay un solo
  objeto, créalo una vez en el arranque y pásalo como dependencia.
- **Fábrica para una única clase concreta.** Si la función solo hace `return LaClase()`, la
  indirección no compra nada. La fábrica se justifica cuando hay una decisión que centralizar.
- **Observadores que no se dan de baja.** El sujeto mantiene referencias a objetos que ya no
  importan: fuga de memoria clásica en interfaces gráficas y en procesos de larga vida. Y si un
  observador lanza una excepción, los siguientes no se notifican salvo que lo controles.
- **Repositorio que devuelve el ORM.** Un método que devuelve una consulta del motor o una
  entidad con anotaciones de persistencia deja el detalle fuera de la interfaz, así que ya no
  hay abstracción: hay una capa más que atravesar. Devuelve objetos del dominio y criterios
  propios.
- **Confundir el patrón con la biblioteca.** El patrón describe la estructura y las
  consecuencias; la biblioteca es una implementación concreta. «Usamos el patrón X, que viene en
  este marco de trabajo» no es una decisión de diseño, es una compra.

## Comprueba que lo sabes

:::quiz
p: ¿Cuándo compensa de verdad introducir una fábrica?
o: Siempre que se cree más de un objeto en el programa
o: Cuando hay una decisión sobre qué clase concreta construir que conviene tener en un solo sitio
o: Cuando la clase tiene más de diez líneas de constructor
a: 2
e: El valor de la fábrica es centralizar la decisión y que los clientes dejen de nombrar clases concretas. Si solo hay una implementación y ningún criterio que elegir, la función de fábrica es una llamada de más que no protege de nada.
:::

:::quiz
p: Un almacén notifica a tres suscriptores y el segundo lanza una excepción. ¿Qué hay que tener previsto?
o: Nada: el sujeto ya ha avisado a los demás porque la notificación es en paralelo
o: Si el sujeto no captura la excepción, los suscriptores siguientes no se notifican, así que hay que decidir y documentar ese comportamiento
o: Los suscriptores se ejecutan en orden alfabético, así que no se puede saber
a: 2
e: La notificación típica es un bucle secuencial: una excepción lo interrumpe. El orden de notificación suele estar indefinido y no depende del nombre, así que hay que decidir explícitamente si se aísla cada suscriptor, si se notifica en un orden concreto y si un fallo se propaga.
:::

:::quiz
p: «El dominio pide el pedido 42 y no sabe si viene de PostgreSQL o de un fichero». ¿Qué patrón describe eso?
o: Observador
o: Repositorio
o: Estrategia
a: 2
e: El repositorio presenta una interfaz con operaciones de colección sobre objetos del dominio y esconde la persistencia detrás. La estrategia cambia un algoritmo, y el observador reparte notificaciones; ninguno de los dos oculta el almacenamiento.
:::
