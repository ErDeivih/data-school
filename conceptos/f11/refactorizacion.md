---
id: refactorizacion
titulo: Refactorización
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [testing-piramide, tdd, principios-solid]
tags: [refactorizacion, testing, deuda-tecnica, diseno]
resumen: Cambiar la forma del código sin cambiar lo que hace: pasos pequeños, olores que dicen dónde mirar y una red de pruebas que lo hace seguro.
fuentes: ["Fowler (2018), 'Refactoring: Improving the Design of Existing Code', 2.ª ed.", "Feathers (2004), 'Working Effectively with Legacy Code'", "Cunningham (1992), 'The WyCash Portfolio Management System'"]
---

## En una frase

Refactorizar es cambiar la estructura interna del código sin cambiar lo que hace por fuera, en
pasos pequeños y con la suite en verde: la deuda técnica se paga a plazos, no con una
reescritura de seis meses.

## La idea

Puedes ordenar la cocina mientras sigues dando servicio, o cerrar el restaurante dos semanas
para reformarla. Lo segundo siempre parece más limpio y casi siempre sale mal: pierdes clientes
y, cuando vuelves, descubres que el horno nuevo no encaja donde estaba el viejo. Refactorizar es
lo primero: mover un cajón cada vez, con la cocina funcionando.

La regla que hace que esto funcione tiene nombre y es de Fowler: **dos sombreros**. O llevas el
sombrero de añadir funcionalidad, o el de refactorizar, pero no los dos a la vez. Con un solo
sombrero, cuando una prueba se pone en rojo sabes qué has roto. Con los dos puestos,
un fallo puede venir del cambio de comportamiento o del cambio de estructura, y empiezas a
depurar a ciegas. Por eso los dos trabajos van en commits separados.

¿Cuándo se refactoriza? Casi nunca «cuando haya tiempo», que es nunca. Se hace:

- **Justo antes de añadir algo.** Si el cambio que te han pedido es difícil de meter, primero
  reordena el código hasta que el cambio sea fácil, y luego hazlo. La preparación se paga sola.
- **Cuando hueles algo concreto.** Fowler catalogó los *olores*: función larga, clase grande,
  código duplicado, lista de parámetros interminable, el mismo `switch` repetido en tres sitios,
  una clase que solo tiene datos y ninguna lógica, comentarios que explican *qué* hace el código
  en lugar de *por qué*. Un olor es una señal de que ahí hay algo que va a doler, no un error.
- **Al revisar código ajeno** en una [[code-review|revisión]], si el arreglo es pequeño y está
  cubierto por pruebas.
- **Cuando no entiendes lo que lees.** Reescribirlo con nombres claros no es perder el tiempo:
  es la forma de que la próxima persona (tú, dentro de tres meses) no vuelva a pagar ese peaje.

La deuda técnica es la metáfora que Ward Cunningham usó para explicar esto: entregar código con
un diseño que no es el ideal es como pedir un préstamo, y los intereses se pagan en cada cambio
posterior. La metáfora se ha deformado hasta significar «código malo que otro escribió», pero la
idea original es más útil: la deuda se contrae a propósito, se sabe qué se debe y se devuelve.
Un refactor sin objetivo —«esto quedaría más bonito con interfaces»— contrata deuda nueva en vez de
pagar la vieja.

## Definición formal

**Refactorización** (definición de Fowler): un cambio en la estructura interna del software que
lo hace más fácil de entender y más barato de modificar **sin cambiar su comportamiento
observable**.

- **Comportamiento observable:** lo que un consumidor del código puede detectar: el valor
  devuelto, las excepciones que lanza, el estado que modifica, los efectos externos que provoca
  y el orden en que los provoca. El rendimiento queda fuera de esta definición: una
  refactorización puede hacer el código más lento o más rápido, y por eso hay que medir después.
- **Invariante del refactor:** para toda entrada del dominio, la salida y los efectos son
  idénticos antes y después. Si algo cambia, ya no hay refactorización: hay un cambio de
  comportamiento disfrazado, y va en otro commit.
- **Red de seguridad:** el conjunto de pruebas que detecta los cambios de comportamiento. Sin
  ella, la refactorización es una apuesta, no una técnica. Si el código no tiene pruebas, el
  primer paso son pruebas de caracterización y solo después se toca.
- **Paso pequeño:** cada paso deja la suite en verde y el sistema desplegable. La grandeza del
  método está en que nunca estás a medio camino de nada.

Los refactorings tienen nombre, y nombrarlos sirve para comunicarse: *extraer función*,
*renombrar*, *mover*, *inline*, *introducir objeto de parámetro*, *reemplazar condicional por
polimorfismo*, *separar en fases*, *encapsular campo*. «Voy a extraer el cálculo del IVA a su
función» es una frase que cualquiera entiende y que cabe en un mensaje.

| Olor | Por qué duele | Refactorización típica |
| --- | --- | --- |
| Función larga | No se puede probar ni nombrar en una frase | Extraer función, separar en fases |
| Código duplicado | Un cambio hay que hacerlo en N sitios y siempre se olvida uno | Extraer función o clase |
| El mismo condicional repetido | Añadir un caso obliga a tocar cinco ficheros | Reemplazar condicional por polimorfismo o por tabla |
| Lista larga de parámetros | El orden se confunde y crece sin control | Introducir objeto de parámetro |
| Clase de datos sin lógica | La lógica vive fuera y se duplica | Mover método a la clase que tiene los datos |
| Comentario que explica el qué | El nombre no dice lo que hace | Renombrar y extraer |

## Ejemplo

Una función que calcula el total de una factura: suma las líneas y aplica un 5 % de descuento si
el bruto pasa de 100 €. La versión «nueva» hace lo mismo con `sum`, un generador y una expresión
condicional; el interés no está en que sea más corta, sino en que el descuento tiene nombre y la suma no
se puede romper al añadir líneas.

Tres facturas para comprobar que no se ha movido nada:

- 3 unidades a 10,00 €: bruto 30,00 € → no pasa de 100 € → **30,00 €**
- 4 unidades a 25,50 € y 2 a 0,90 €: bruto 102,00 + 1,80 = 103,80 € → 103,80 · 0,95 = **98,61 €**
- 1 unidad a 100,00 €: bruto exactamente 100,00 €, que **no** es mayor que 100 → **100,00 €**

Ese tercer caso es el que rompe las refactorizaciones descuidadas: cambiar `total > 100` por
`total >= 100` es un cambio de comportamiento de un carácter, y sin la prueba nadie lo nota
hasta que un cliente reclama 5 céntimos.

:::figura
fichero: refactorizacion-mismo-resultado
pie: Izquierda, las tres facturas del ejemplo con las dos versiones: 30,00 €, 98,61 € y 100,00 €, idénticas una al lado de la otra. Esa coincidencia es la red de seguridad, y la comprueba el `assert` del código. Derecha, el error de un carácter: la curva con `>` y la curva con `>=` solo se separan en un punto, el del bruto de 100,00 € exactos, donde la versión descuidada cobra 95,00 €. Un solo punto distinto en toda la recta, y sin una prueba que lo visite no lo ve nadie.
fuente: figuras/refactorizacion-1.py
:::

El segundo ejemplo es el condicional convertido en tabla: cuatro tarifas y un valor por defecto.
Las dos versiones devuelven lo mismo para los cuatro casos, y la versión con tabla no necesita
una prueba por rama: basta comprobar la tabla y el valor por defecto.

## Código

```python verificable
# Comprobar que el resultado no cambia es la red de seguridad de cualquier refactor.
def total_viejo(lineas):
    total = 0
    for linea in lineas:
        # Cada linea es un diccionario: se suma precio por cantidad, no los dos campos.
        total = total + linea["precio"] * linea["cantidad"]
    if total > 100:
        total = total * 0.95        # el estricto importa: 100,00 exactos NO llevan descuento
    return round(total, 2)

def total_nuevo(lineas):
    # Expresion generadora dentro de sum: recorre y multiplica sin crear una lista en medio.
    bruto = sum(linea["precio"] * linea["cantidad"] for linea in lineas)
    # Condicional en linea (A if condicion else B): el descuento tiene nombre, bruto.
    return round(bruto * 0.95 if bruto > 100 else bruto, 2)

facturas = [
    [{"precio": 10.0, "cantidad": 3}],
    [{"precio": 25.5, "cantidad": 4}, {"precio": 0.9, "cantidad": 2}],
    [{"precio": 100.0, "cantidad": 1}],
]
# enumerate con start=1 numera las facturas desde 1: el mensaje de error habla de la 1, no de la 0.
for numero, factura in enumerate(facturas, start=1):
    viejo, nuevo = total_viejo(factura), total_nuevo(factura)
    assert viejo == nuevo, f"el refactor cambio el resultado en la factura {numero}"
    print(f"factura {numero}: {viejo:.2f}")

# all() sobre un generador: True si las dos versiones coinciden en todas las facturas.
identicos = all(total_viejo(f) == total_nuevo(f) for f in facturas)
print("resultados identicos:", identicos)          # -> True
```

:::claves
- El `assert` compara la salida de las dos versiones **para la misma entrada**: eso es la
  invariante del refactor escrita como código. Si una factura diera distinto, el programa se
  pararía ahí, antes de imprimir nada.
- `sum(generador)` no crea ninguna lista intermedia: recorre las líneas y va acumulando. La
  versión vieja hacía lo mismo con un bucle y una variable, así que el resultado es idéntico,
  pero ya no hay un acumulador que se pueda olvidar de inicializar.
- El `if total > 100` es **estricto**, y esa es justo la línea que rompen los refactors
  descuidados. Con `>=`, la factura de 100,00 € exactos pasa de 100,00 a 95,00: un cambio de
  comportamiento con un solo carácter de diferencia.
- `all(...)` corta en cuanto encuentra un `False` y no sigue mirando el resto; aquí solo resume
  el veredicto del `assert` de dentro, que es el que dice en qué factura concreta falló. Y para
  que esa comparación signifique algo, las dos versiones tienen que **recibir los mismos datos y
  no tocarlos**: si una ordenara la lista al pasar, la segunda llamada vería otra cosa.
- En `tasa_nueva`, `TASAS.get(tipo, POR_DEFECTO)` devuelve el defecto en vez de lanzar
  `KeyError`; si usaras `TASAS[tipo]`, el tipo «desconocida» reventaría la prueba. Y
  `len(TASAS) + 1` cuenta el defecto, que no está en la tabla.
- La tabla no reduce las ramas de verdad: las convierte en **datos**. Añadir una tarifa es
  añadir una fila, y el valor por defecto sigue siendo uno solo, en un solo sitio.
:::

```python verificable
# Reemplazar condicionales anidados por una tabla: mismo resultado, menos ramas que probar.
def tasa_vieja(tipo):
    # Cadena de elif: cada rama es un camino que hay que probar por separado.
    if tipo == "basica":
        return 0.04
    elif tipo == "plus":
        return 0.02
    elif tipo == "premium":
        return 0.01
    else:
        return 0.06                 # el else final es el valor por defecto

TASAS = {"basica": 0.04, "plus": 0.02, "premium": 0.01}
POR_DEFECTO = 0.06                  # mismo numero que el else, pero ahora con nombre

def tasa_nueva(tipo):
    # get con segundo argumento: devuelve el valor por defecto en vez de dar KeyError.
    return TASAS.get(tipo, POR_DEFECTO)

for tipo in ["basica", "plus", "premium", "desconocida"]:
    # La prueba compara las dos versiones para cada tipo, incluido el que no esta en la tabla.
    assert tasa_vieja(tipo) == tasa_nueva(tipo), f"difieren en {tipo}"
    print(f"{tipo:<12} {tasa_nueva(tipo):.2f}")

# +1 porque tambien se comprueba el tipo de fuera de la tabla (el valor por defecto).
print("tipos comprobados:", len(TASAS) + 1)        # -> 4
```

## Errores típicos

- **Refactorizar sin pruebas.** Es el error que convierte una mejora en una regresión silenciosa.
  Si no hay red, el orden correcto es: escribir pruebas de caracterización sobre el
  comportamiento actual, verlas en verde, y solo entonces mover código.
- **Mezclar refactor y funcionalidad en el mismo commit.** El sombrero doble. Cuando algo falla,
  no sabes qué de los dos cambios lo rompió, y en la revisión nadie puede distinguir lo que
  cambió de forma de lo que cambió de fondo. Dos commits, siempre.
- **La reescritura total como refactorización.** Reescribir un módulo entero «aprovechando» no es
  refactorizar: es un proyecto con su propio riesgo, y durante semanas no hay versión
  desplegable. La refactorización se caracteriza por no dejar nunca el sistema roto.
- **Cambiar el comportamiento y llamarlo refactorización.** Renombrar una variable está bien;
  aprovechar para arreglar el redondeo y llamarlo «limpieza» mete un cambio funcional sin
  revisión. Si cambia lo que sale, es otra cosa.
- **Refactorizar código que nadie va a tocar.** El beneficio de un refactor es hacer más baratos
  los cambios futuros. En un módulo congelado que funciona y no va a evolucionar, el coste es
  real y el beneficio, cero. Se documenta y se deja quieto.
- **Basar la decisión en la cobertura.** Un 90 % de cobertura con pruebas que solo ejecutan
  líneas no detecta un cambio de comportamiento. Antes de un refactor delicado, comprueba que las
  pruebas de esa zona tienen aserciones que de verdad comparan resultados.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estos cambios NO es una refactorización?
o: Extraer el cálculo del IVA a una función propia
o: Cambiar `total > 100` por `total >= 100` porque parece más correcto
o: Renombrar la variable `t` a `total_factura`
a: 2
e: Cambiar la comparación altera la salida para el caso de exactamente 100, así que es un cambio de comportamiento. Los otros dos dejan intacto lo que el código devuelve. El signo es justo el tipo de cambio que se cuela cuando se refactoriza sin pruebas.
:::

:::quiz
p: ¿Por qué Fowler insiste en no llevar los dos sombreros a la vez?
o: Porque cansa demasiado
o: Porque si algo se rompe no puedes saber si fue el cambio de estructura o el de comportamiento
o: Porque el sistema de control de versiones no lo permite
a: 2
e: Con un solo tipo de cambio por paso, un fallo es inequívoco y la bisección es trivial. Mezclados, cada fallo obliga a distinguir dos causas posibles, que es exactamente el trabajo que el ciclo corto venía a eliminar.
:::

:::quiz
p: Tienes que refactorizar un módulo de 600 líneas sin ninguna prueba. ¿Cuál es el orden correcto?
o: Mover el código primero, porque las pruebas se escriben más rápido sobre el diseño nuevo
o: Escribir pruebas de caracterización del comportamiento actual, y refactorizar después
o: Refactorizar y ejecutar el sistema a mano al final
a: 2
e: Las pruebas de caracterización convierten el comportamiento actual —aunque sea feo— en un contrato verificable. Sin ellas, cada movimiento es irreversible: no hay forma de saber si has cambiado algo. El sistema a mano no cubre los casos raros y no queda registrado.
:::
