---
id: principios-solid
titulo: Principios SOLID
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [tipos-y-estructuras-python, tipado-y-linters]
tags: [diseno, poo, mantenibilidad, interfaces]
resumen: Cinco reglas sobre dónde poner las fronteras del código para que añadir algo nuevo no obligue a repasar todo lo que ya funcionaba.
fuentes: ["Martin (2002), 'Agile Software Development: Principles, Patterns, and Practices'", "Liskov (1987), 'Data Abstraction and Hierarchy'", "Meyer (1988), 'Object-Oriented Software Construction'"]
---

## En una frase

SOLID son cinco principios sobre responsabilidades, extensiones, sustituciones,
interfaces y dependencias, y todos persiguen lo mismo: que un cambio concreto obligue a tocar
el menor número de sitios posible.

## La idea

Piensa en una cocina pequeña donde la misma persona compra, cocina, sirve y cobra. Funciona
mientras no cambie nada. El día que el menú cambia, esa persona tiene que interrumpirlo todo:
no hay forma de cambiar la compra sin tocar el servicio. Una cocina con puestos separados
—compras, partida, sala— permite cambiar el menú de la partida sin reescribir las facturas.

En software el problema es idéntico, y la medida del dolor es muy concreta: **cuántos ficheros
tienes que abrir y tocar para un cambio**. Si añadir una forma de pago obliga a modificar la
clase que calcula impuestos, la que genera el PDF y la que escribe en la base de datos, el
cambio no es pequeño: es pequeño el requisito y enorme el trabajo. SOLID es el conjunto de
reglas que la industria fue acumulando para reducir ese radio de explosión.

Los cinco, en corto:

- **S — Responsabilidad única (SRP).** Cada módulo responde ante un solo tipo de usuario o de
  cambio. Si dos equipos distintos pueden pedir modificaciones a la misma clase por motivos
  distintos, esa clase tiene dos responsabilidades.
- **O — Abierto y cerrado (OCP).** Debe poder añadirse comportamiento nuevo sin editar el
  código que ya funciona: se añade una implementación más, no otro `elif`.
- **L — Sustitución de Liskov (LSP).** Si tienes una función que acepta un tipo base, debe
  funcionar igual con cualquier subtipo. Un subtipo que rompe una promesa del padre no es un
  subtipo, es un impostor.
- **I — Segregación de interfaces (ISP).** Nadie debería verse obligado a depender de métodos
  que no usa. Mejor cinco interfaces pequeñas que una con veinte métodos.
- **D — Inversión de dependencias (DIP).** El código de alto nivel no debe depender de detalles
  (una base de datos, una API); ambos deben depender de una abstracción que el de alto nivel
  define.

El aviso que casi nunca se da: **esto no es una religión**. Aplicado a un script de 80 líneas,
SOLID produce veinte clases y una fábrica para instanciarlas. El criterio no es «cumplo los
cinco», es «este cambio concreto se ha vuelto más barato». Y tampoco es un fin en sí mismo: es
la preparación que hace posible [[refactorizacion|refactorizar]] sin miedo y el terreno donde
encajan [[patrones-de-diseno|los patrones de diseño]].

## Definición formal

- **SRP.** Un módulo `M` cumple SRP si todos sus consumidores que pueden pedir un cambio
  pertenecen a un mismo actor. Señal de violación: al describir la clase necesitas la palabra
  «y» («calcula la nómina **y** la manda por correo»). Medida práctica: número de motivos
  independientes de cambio.
- **OCP.** El módulo es abierto a extensión y cerrado a modificación: existe una abstracción
  `A` estable y el comportamiento nuevo se introduce con una implementación `C` nueva de `A`,
  sin editar el código cliente que usa `A`.
- **LSP (Liskov, 1987).** Si `S` es subtipo de `T`, para todo predicado `P` demostrable sobre
  objetos de tipo `T`, `P` debe ser demostrable sobre objetos de tipo `S`. En la práctica, con
  los contratos de Meyer: un subtipo **no puede reforzar precondiciones** (no puede exigir
  más), **no puede debilitar postcondiciones** (no puede prometer menos) y **debe preservar las
  invariantes** del padre.
- **ISP.** Un cliente `K` no debe depender de ningún método de la interfaz `I` que no invoque.
  La interfaz se parte hasta que cada cliente use todos los métodos de la suya.
- **DIP.** `A → I ← B`: el módulo de alto nivel `A` y el de bajo nivel `B` dependen ambos de la
  abstracción `I`, y `I` la declara quien la necesita, no quien la implementa.

Un indicador útil: **acoplamiento aferente y eferente**. Cuantos módulos dependen de este
(coste de cambiarlo) y de cuántos depende (lo que arrastra si cambia).

## Ejemplo

Una tienda aplica tres políticas de descuento. Sin OCP, el cálculo es una cadena:

```text
if tipo == "ninguno":    total = base
elif tipo == "diez":     total = base * 0.90
elif tipo == "dos_por_uno": total = base if base <= 20 else 20 + (base - 20) / 2
```

Añadir «rebaja del 30 % los martes» significa editar esa cadena… y las dos copias más que
existen en el generador de facturas y en el panel de administración. Con una abstracción
`Descuento` y un mapa de políticas, añadir una política es escribir una clase nueva y registrar
su nombre: los tres sitios que la usaban no se tocan.

Con un pedido de 48,00 €:

- política «ninguno»: 48,00 €
- política «diez»: 48,00 · 0,90 = 43,20 €
- política «dos_por_uno»: 20 + (48 − 20) / 2 = 20 + 14 = 34,00 €

Y el ejemplo de LSP, que es el mismo problema con otra cara: un `Rectangulo` con ancho y alto
independientes promete que `area() == ancho · alto`. Un `Cuadrado` que herede de él y mantenga
los dos lados iguales rompe la promesa en cuanto alguien llama a `set_ancho(5)` y luego
`set_alto(4)`: un rectángulo da 20 y el cuadrado da 16. No es un fallo de la aritmética, es que
el cuadrado no es un rectángulo *con ese contrato*.

:::figura
fichero: principios-solid-promesa-y-radio
pie: A la izquierda, el caso de Liskov medido: el cliente fija 5 de ancho y 4 de alto, y el padre promete 20. El rectángulo cumple; el cuadrado, que mantiene los lados iguales, devuelve 16 y no lanza ningún error, así que el fallo no se ve ejecutando: se ve comparando el resultado con el contrato. A la derecha, el radio del cambio al añadir la política «rebaja del 30 % los martes»: con la cadena de `if/elif` hay que abrir y editar tres sitios —el cálculo, el generador de facturas y el panel de administración—; con una abstracción `Descuento`, ninguno: se añade una clase y se registra su nombre. Ese número, cuántos ficheros tocas, es la medida práctica de si SOLID está sirviendo para algo en ese código.
fuente: figuras/principios-solid-1.py
:::

## Código

```python verificable
# Abierto y cerrado: anadir una politica no toca el codigo que calcula el total.
class Descuento:
    def importe(self, base):
        raise NotImplementedError     # la clase base no calcula nada: es solo el contrato

class SinDescuento(Descuento):
    def importe(self, base):
        return base

class DiezPorCiento(Descuento):
    def importe(self, base):
        return base * 0.90

class DosPorUno(Descuento):
    def importe(self, base):
        # los primeros 20 euros se pagan enteros; lo que pasa de 20, a mitad de precio
        return base if base <= 20 else 20 + (base - 20) / 2

def total(base, descuento):
    # no hay ningun if sobre el tipo: se llama al mismo metodo y cada clase hace lo suyo
    return round(descuento.importe(base), 2)      # round(x, 2) devuelve un float con dos decimales

print(total(48.0, SinDescuento()))     # -> 48.0
print(total(48.0, DiezPorCiento()))    # -> 43.2
print(total(48.0, DosPorUno()))        # -> 34.0
```

:::claves
- `DiezPorCiento()` se pasa **con paréntesis**: lo que viaja a `total` es una instancia, no la clase. Sin los paréntesis, `descuento.importe(base)` fallaría porque estarías llamando al método sobre la clase y `self` sería el propio `base`.
- La clase base `Descuento` no calcula nada: su método solo lanza `NotImplementedError`. Python no obliga a implementarlo, así que el fallo aparece **al llamar**, no al crear el objeto. Un `return 0` en su lugar sería peor: el total saldría mal y nadie se enteraría. Para que salte antes se usa `abc.ABC` con `@abstractmethod`.
- `total` no comprueba el tipo de `descuento` ni tiene un `if` por política: llama al mismo método y cada clase responde lo suyo. Eso es lo que hace que añadir una política nueva no toque esta función, y es el objetivo entero de OCP.
- `round(x, 2)` devuelve un `float`, no un `Decimal`, y usa redondeo al par más cercano: `round(2.675, 2)` da `2.67` y no `2.68`, porque 2.675 no se puede representar exactamente en binario. Para dinero se trabaja en céntimos enteros o con `decimal.Decimal`.
- En el cuadrado, `super().__init__(lado, lado)` ejecuta el constructor del padre y le pasa los dos lados iguales. `self.ancho = self.alto = valor` es una **asignación encadenada**: asigna el mismo valor a los dos atributos, y por eso `set_ancho` deja de respetar el alto que hubiera puesto el cliente.
- `area_tras_ajustes` no comprueba el tipo y acepta cualquier subtipo: esa es exactamente la promesa de LSP. Con el cuadrado devuelve 16 en vez de 20 y **no lanza ningún error**, así que la violación no se detecta ejecutando: se detecta comparando el resultado con el contrato del padre. La prueba que la delata es pasar el subtipo por los **mismos casos** que el padre; si el test se escribe dos veces —una por clase, esperando lo que cada una devuelve—, el fallo queda tapado y el test del cuadrado pasa en verde.
:::

```python verificable
# El caso clasico de violacion de Liskov: el cuadrado que hereda del rectangulo.
class Rectangulo:
    def __init__(self, ancho, alto):
        self.ancho, self.alto = ancho, alto
    def set_ancho(self, valor): self.ancho = valor
    def set_alto(self, valor):  self.alto = valor
    def area(self): return self.ancho * self.alto

class Cuadrado(Rectangulo):
    def __init__(self, lado):
        super().__init__(lado, lado)      # super() llama al constructor del padre con los dos lados iguales
    def set_ancho(self, valor): self.ancho = self.alto = valor   # mantiene el cuadrado...
    def set_alto(self, valor):  self.ancho = self.alto = valor   # ...y rompe al padre

def area_tras_ajustes(rect):
    """Invariante del padre: tras fijar 5 de ancho y 4 de alto, el area es 20."""
    # no comprueba el tipo: acepta cualquier subtipo, que es justo lo que promete LSP
    rect.set_ancho(5)
    rect.set_alto(4)
    return rect.area()

print("rectangulo 2x3:", area_tras_ajustes(Rectangulo(2, 3)))   # -> 20
print("cuadrado de lado 2:", area_tras_ajustes(Cuadrado(2)))    # -> 16
```

## Errores típicos

- **Leer SRP como «una clase por función».** El resultado es un enjambre de clases anémicas
  que solo envuelven un método. SRP habla de un actor al que responder, no de una clase por
  cada verbo. Si dos comportamientos cambian siempre juntos y por el mismo motivo, van juntos.
- **Confundir OCP con «no se toca el código».** OCP no prohíbe cambiar código: dice que añadir
  una variante nueva no debería obligar a editar lo que ya está probado. Si el requisito cambia
  de verdad, se cambia el código y se ejecutan los tests.
- **Usar herencia para reutilizar en vez de para sustituir.** Heredar de una clase solo para
  reaprovechar dos métodos es la vía rápida a violar LSP. Si lo que quieres es reutilizar
  comportamiento, casi siempre quieres composición: tener un objeto dentro, no ser su hijo.
- **Interfaces gigantes.** Una interfaz con veinte métodos obliga a cada implementación a
  rellenar quince con `raise NotImplementedError`, y a cada test a construir un doble enorme.
  Parte la interfaz por cliente.
- **Invertir dependencias donde no hay nada que invertir.** Envolver `math.sqrt` detrás de una
  interfaz y una fábrica no aporta flexibilidad: aporta dos ficheros más. La inversión se paga
  cuando hay algo que de verdad quieres poder cambiar (una base de datos, un reloj, una API
  externa) o cuando necesitas sustituirlo en un test.
- **Confundir inyección de dependencias con un marco de trabajo.** Inyectar es pasar la
  dependencia como argumento del constructor. Un contenedor con anotaciones es una forma de
  automatizar esa inyección, no un requisito: para tres dependencias, el constructor a mano se
  lee mejor.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la señal práctica de que una clase viola el principio de responsabilidad única?
o: Que tiene más de veinte métodos
o: Que dos equipos con motivos distintos necesitan modificarla, y al describirla hace falta la palabra «y»
o: Que importa módulos de más de un paquete
a: 2
e: SRP se define por actores que pueden pedir cambios, no por contar métodos ni importaciones. Un contador de líneas no distingue una clase con una responsabilidad grande de una con tres pequeñas; la lista de quién pide cambios, sí.
:::

:::quiz
p: ¿Por qué el cuadrado que hereda del rectángulo rompe el principio de sustitución?
o: Porque un cuadrado no tiene área
o: Porque mantener los lados iguales cambia la promesa del padre: fijar el alto ya no deja el ancho como estaba
o: Porque Python no admite herencia múltiple
a: 2
e: El cliente del padre da por hecho que ancho y alto son independientes. El subtipo refuerza la invariante (los lados son iguales) y con ello invalida la postcondición que el cliente esperaba. La solución habitual es no heredar: dos tipos con la misma interfaz de solo lectura.
:::

:::quiz
p: Tienes un servicio que lee de PostgreSQL y quieres probarlo sin base de datos. ¿Qué propone la inversión de dependencias?
o: Que el servicio dependa de una abstracción de repositorio que en producción implementa PostgreSQL y en el test un doble en memoria
o: Que el test levante una base de datos real para no cambiar nada
o: Que el servicio detecte si está en un test y cambie de comportamiento
a: 1
e: El módulo de alto nivel declara la interfaz que necesita y los detalles se conectan por fuera. Levantar una base real es integración, no una prueba unitaria, y detectar el entorno dentro del servicio mete lógica de test en producción.
:::
