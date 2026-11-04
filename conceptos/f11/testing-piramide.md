---
id: testing-piramide
titulo: La pirámide de pruebas
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [testing-con-pytest]
tags: [testing, calidad, integracion, coste]
resumen: Muchas pruebas unitarias rápidas, algunas de integración y muy pocas de extremo a extremo: la proporción que mantiene la suite útil y a la vez soportable.
fuentes: ["Cohn (2009), 'Succeeding with Agile: Software Development Using Scrum'", "Meszaros (2007), 'xUnit Test Patterns: Refactoring Test Code'", "Humble y Farley (2010), 'Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation'"]
---

## En una frase

La pirámide de pruebas dice que conviene tener muchas pruebas unitarias baratas en la base,
menos de integración en el medio y muy pocas de extremo a extremo en la punta, porque cada
nivel hacia arriba cuesta más de escribir, más de ejecutar y, sobre todo, más de diagnosticar.

## La idea

Una fábrica de coches no desmonta el vehículo entero para comprobar cada tornillo, ni se fía
solo de la prueba de conducción final. Comprueba piezas cuando las fabrica, conjuntos cuando
los monta y el coche completo al final. Cada nivel cuesta más y descubre menos por euro
invertido, así que hay pocos del último.

Con el software pasa lo mismo, y el coste crece en tres frentes a la vez:

1. **Escribir.** Una prueba unitaria son cinco líneas. Una de extremo a extremo necesita
   levantar el sistema, datos de partida, una sesión, selectores de la interfaz y una limpieza
   al terminar.
2. **Ejecutar.** Una unitaria tarda milisegundos; una de extremo a extremo, entre segundos y
   minutos. Si tu suite tarda veinte minutos, deja de ejecutarse antes de cada subida, y una
   suite que no se ejecuta no protege nada. Esto conecta directamente con
   [[ci-cd]]: la suite es el freno del despliegue.
3. **Diagnosticar.** Cuando falla una unitaria, sabes qué función y qué caso. Cuando falla una
   de extremo a extremo, sabes que «el flujo de compra no funciona» y te toca investigar en
   logs y trazas.

Los tres niveles, en corto:

- **Unitaria.** Ejercita una unidad de comportamiento con todas las dependencias externas
  sustituidas: sin red, sin disco, sin base de datos, sin depender del reloj ni del azar. Debe
  poder ejecutarse en cualquier orden y tantas veces como haga falta.
- **Integración.** Ejercita la colaboración de dos o más componentes reales: la consulta contra
  una base de datos de verdad, la serialización y deserialización, el contrato del endpoint.
  Es donde aparecen los fallos que la unitaria no puede ver porque sustituyó justo la pieza que
  estaba mal.
- **Extremo a extremo.** Ejercita el sistema desplegado tal como lo usa una persona, desde
  fuera. Verifica el cableado completo, y es la única que detecta que faltaba una variable de
  entorno o que el contenedor nuevo no arranca.

Hay formas alternativas a la pirámide. En aplicaciones con mucha interfaz se habla del
**trofeo**: menos unitarias puras y más integración, porque gran parte de los fallos vive en el
pegamento entre componentes. En un proyecto de datos o de machine learning, la forma se
distorsiona aún más: la lógica suele ser poca y el riesgo está en el esquema, en la
distribución y en los datos de entrada. Lo que no cambia es la idea de fondo: **que la prueba
más barata capaz de detectar el fallo sea la que lo detecte**.

Y un matiz que se olvida: la suite no existe para demostrar que el código funciona hoy, sino
para poder cambiar el código mañana. Ese es el vínculo con [[refactorizacion]] y con [[tdd]]:
sin pruebas rápidas y fiables, refactorizar es apostar.

## Definición formal

Sea una suite `S` con `n_u` unitarias, `n_i` de integración y `n_e` de extremo a extremo, con
duraciones medias `t_u`, `t_i` y `t_e`. El tiempo de la suite es:

:::formula
T = n_u · t_u + n_i · t_i + n_e · t_e
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T` | El tiempo total de la suite: lo que tardas en saber si el cambio rompió algo | s | Sube con cualquiera de los tres niveles; decide si la suite llega a ejecutarse |
| `n_u` | Número de pruebas unitarias | pruebas | Sube `T` muy poco (2 ms cada una), así que se pueden tener miles |
| `t_u` | Duración media de una unitaria | s | Es el multiplicador del nivel barato: cada milisegundo aquí se multiplica por `n_u` |
| `n_i` | Número de pruebas de integración | pruebas | Sube `T` de forma apreciable: cada una toca base de datos, ficheros o red |
| `t_i` | Duración media de una de integración | s | Dos o tres órdenes de magnitud por encima de `t_u` |
| `n_e` | Número de pruebas de extremo a extremo | pruebas | Es el término que domina: pocas unidades cambian `T` en minutos |
| `t_e` | Duración media de un flujo completo | s | El más caro por prueba; bajarlo de 12 s a 3 s permite cuatro veces más flujos |
:::

La pirámide no dice nada de `T` directamente: dice que `n_e` debe ser pequeño porque `t_e` es
dos o tres órdenes de magnitud mayor que `t_u`, y que `n_u` puede ser grande porque su coste
marginal es mínimo.

Visto en números, la suma de la fórmula se reparte de forma muy desigual: el 99 % de las pruebas
se lleva un tercio del tiempo y el 1 % restante se lleva los otros dos tercios.

:::figura
fichero: testing-piramide-reparto-del-tiempo
pie: Izquierda, lo que aporta cada nivel al tiempo total de la suite de 145,6 s: las 800 unitarias suman 1,6 s (el 1 % del tiempo) mientras las 8 pruebas de extremo a extremo suman 96 s (el 66 %). Derecha, el mismo reparto en dos barras apiladas: el 99 % de las pruebas vive en la base y solo consume un tercio del tiempo, así que la proporción de la pirámide no la fija la elegancia, la fija `t_e`. Mover una prueba de la punta a la base es la única forma barata de acortar `T`.
fuente: figuras/testing-piramide-1.py
:::

Términos que conviene usar con precisión:

- **Doble de prueba (test double).** Cualquier objeto que sustituye a una dependencia real.
  Meszaros distingue cinco: **dummy** (solo rellena un parámetro), **stub** (devuelve respuestas
  prefijadas), **spy** (además registra cómo se le llamó), **mock** (viene con las expectativas
  programadas y falla si no se cumplen) y **fake** (una implementación simplificada de verdad,
  como un repositorio en memoria).
- **Fixture.** El estado previo que necesita una prueba: datos, conexión, fichero temporal.
  Debe crearse y destruirse por prueba, no compartirse entre ellas.
- **Prueba inestable (flaky).** Pasa y falla sin que cambie el código. Casi siempre por orden de
  ejecución, estado compartido, reloj, azar o esperas fijas. Es el enemigo número uno: cuando
  aparece una, el equipo empieza a relanzar en lugar de leer.
- **Cobertura de líneas y de ramas.** Porcentaje de líneas o de ramas ejecutadas por la suite.
  Mide ejecución, no verificación: una prueba sin `assert` sube la cobertura igual.
- **Criterio de aceptación.** Qué tiene que ser verdad para dar la tarea por terminada. Es la
  lista de la que salen los casos, empezando por el caso normal y siguiendo por los bordes.

## Ejemplo

Suite con 800 unitarias de 2 ms, 120 de integración de 400 ms y 8 de extremo a extremo de 12 s:

- unitarias: 800 · 0,002 = **1,6 s**
- integración: 120 · 0,4 = **48 s**
- extremo a extremo: 8 · 12 = **96 s**
- total: **145,6 s** (unos 2 minutos y medio)

Las 920 pruebas que no son de extremo a extremo son el 99,1 % de la suite y consumen un tercio
del tiempo; las 8 de extremo a extremo (el 0,86 %) se llevan los otros dos tercios. Ahora el
mismo sistema con la proporción invertida —pocas unitarias y muchas de extremo a extremo, el
«cono de helado»—: 20 unitarias, 60 de integración y 200 flujos completos. Solo los flujos
cuestan 200 · 12 = **2.400 s**, cuarenta minutos. Nadie ejecuta eso antes de subir un cambio, y
la consecuencia práctica es que las pruebas se ejecutan… cuando ya se ha roto producción.

Fíjate en que los números absolutos importan menos que la proporción. Si consigues bajar la
prueba de extremo a extremo de 12 s a 3 s, puedes tener cuatro veces más sin que la suite se
vuelva inútil; pero seguirá siendo el nivel más caro por prueba.

## Código

```python verificable
# La aritmetica de la piramide: donde se va el tiempo de una suite.
# Las dos claves coinciden: un nombre que falte aqui da KeyError al calcular los segundos.
duraciones = {"unitaria": 0.002, "integracion": 0.400, "e2e": 12.0}
cantidades = {"unitaria": 800, "integracion": 120, "e2e": 8}

total = 0.0
# items() da pares (clave, valor): se recorren las dos tablas a la vez sin usar indices.
for capa, n in cantidades.items():
    segundos = n * duraciones[capa]
    total += segundos
    # El formato va en la f-string: <12 alinea a la izquierda, >4 a la derecha, .1f un decimal.
    print(f"{capa:<12} {n:>4} pruebas {segundos:>8.1f} s")

total_pruebas = sum(cantidades.values())       # sum sobre los valores, no sobre las claves
tiempo_e2e = cantidades["e2e"] * duraciones["e2e"]
print(f"total de la suite: {total:.1f} s")                            # -> total de la suite: 145.6 s
# .3% multiplica por 100 y anade el signo: 0.00862 se imprime como 0.862%.
print(f"e2e: {cantidades['e2e'] / total_pruebas:.3%} de las pruebas")  # -> e2e: 0.862% de las pruebas
print(f"e2e: {tiempo_e2e / total:.0%} del tiempo")                     # -> e2e: 66% del tiempo
```

:::claves
- Las dos tablas se recorren **por la misma clave**. `cantidades.items()` da pares
  `(capa, n)` y dentro se busca `duraciones[capa]`: un nombre que falte o esté mal escrito
  no se ignora, lanza `KeyError` y la suite entera del ejemplo no se ejecuta.
- `total += segundos` acumula en una variable que hay que haber inicializado **antes** del
  bucle (`total = 0.0`). Sin esa línea, el primer `+=` falla con `NameError`.
- El formato `f"{x:.3%}"` multiplica por cien y añade el signo: `0.00862` sale como
  `0.862%`, no como `0.009%`. Es la fuente número uno de porcentajes mal calculados a mano.
- El tiempo **no** es proporcional al número de pruebas: 8 pruebas de 12 s pesan más que 800
  de 2 ms. Por eso bajar la duración de una prueba de e2e cambia más la suite que añadir
  unitarias.
- `unittest` descubre los métodos por el **nombre**: `test_` al principio. Un método llamado
  `comprobar_iva` no se ejecuta nunca y la suite sigue diciendo «OK» con cero pruebas.
- `resultado.failures` es una lista, no un booleano: `len(...) == 0` significa que todo pasó.
  Comprobar `if resultado.failures` funciona, pero imprimir la lista entera te da el motivo.
:::

```python verificable
import unittest

def precio_con_iva(base, tipo=0.21):
    return round(base * (1 + tipo), 2)

class TestPrecio(unittest.TestCase):
    # Metodos que empiezan por test_: el cargador los encuentra por convencion, sin registro.
    def test_iva_general(self):
        self.assertEqual(precio_con_iva(100), 121.0)
    def test_tipo_reducido(self):
        self.assertEqual(precio_con_iva(100, 0.10), 110.0)
    def test_redondeo_a_dos_decimales(self):
        # 9.99 · 1.21 = 12.0879: sin el round serian 12.09 solo por como imprime Python.
        self.assertEqual(precio_con_iva(9.99), 12.09)

# Carga y ejecuta la clase entera en una linea; verbosity=0 evita el ruido de cada punto.
resultado = unittest.TextTestRunner(verbosity=0).run(
    unittest.defaultTestLoader.loadTestsFromTestCase(TestPrecio))

# Tres comprobaciones sin base de datos, sin red y sin reloj: milisegundos.
print("pruebas ejecutadas:", resultado.testsRun)   # -> 3
print("fallos:", len(resultado.failures))          # -> 0
```

```text
Forma de la suite, de abajo arriba:

  /\        e2e          pocas, lentas, fragiles, detectan el cableado
 /  \       integracion  bastantes, reales, detectan contratos
/____\      unitarias   muchas, rapidas, deterministas, detectan logica
```

## Errores típicos

- **Usar la cobertura como objetivo.** Un 95 % de cobertura con pruebas sin aserciones no
  protege de nada. La cobertura sirve para encontrar zonas *no* ejecutadas nunca, no para
  aprobar un cambio. Si conviertes el porcentaje en un umbral obligatorio, la gente escribe
  pruebas que ejecutan líneas sin comprobar nada.
- **Probar la implementación en lugar del comportamiento.** Si una prueba comprueba que se
  llamó a un método interno concreto, se romperá en cuanto refactorices sin cambiar nada de
  fuera, y el equipo aprenderá a ignorar los fallos. Comprueba entradas y salidas, no el guion.
- **Meterlo todo en extremo a extremo.** Es la trampa del cono de helado: parece más real y es
  más lento y más difícil de diagnosticar. Reserva ese nivel para los flujos que justifican el
  coste: el camino del dinero, el alta de usuario, el arranque.
- **Compartir estado entre pruebas.** Base de datos que se queda con las filas de la prueba
  anterior, variable global modificada, fichero que no se borra. La suite pasa en tu portátil y
  falla en el servidor por el orden de ejecución.
- **Dejar una prueba inestable «para luego».** Al tercer relanzamiento, el equipo asume que los
  fallos de la suite son ruido y deja de mirarlos. Una prueba inestable se arregla, se aisla o
  se borra, pero no se tolera.
- **Confundir una prueba de integración con una unitaria con dobles.** Si sustituyes la base de
  datos, el `JOIN` que estaba mal no lo vas a ver nunca. Los dos niveles son necesarios: la
  unitaria te dice dónde, la de integración te dice si de verdad funciona junto.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la pirámide pone pocas pruebas de extremo a extremo?
o: Porque no detectan fallos reales
o: Porque cuestan mucho de escribir, ejecutar y diagnosticar, así que se reservan para los flujos críticos
o: Porque solo se pueden ejecutar en producción
a: 2
e: Las de extremo a extremo son las únicas que verifican el cableado completo, pero su coste por prueba es dos o tres órdenes de magnitud mayor. Si son la mayoría, la suite tarda tanto que deja de ejecutarse y entonces no protege nada.
:::

:::quiz
p: Una prueba comprueba que se llamó a un método interno del servicio con un argumento concreto. ¿Qué problema tiene?
o: Que es lenta
o: Que fija la implementación: cualquier refactorización que no cambie el comportamiento la rompe
o: Que no puede ejecutarse con pytest
a: 2
e: Es una prueba acoplada al cómo y no al qué. Al no cambiar el comportamiento observable, debería seguir pasando, pero falla; y los fallos falsos son los que enseñan al equipo a ignorar la suite.
:::

:::quiz
p: Una prueba falla una de cada cinco ejecuciones sin que nadie toque el código. ¿Qué se hace?
o: Relanzarla hasta que pase y seguir
o: Tratarla como un fallo: aislarla, arreglar la causa (orden, reloj, azar, esperas fijas) o eliminarla
o: Añadirle un `sleep` de cinco segundos al principio
a: 2
e: Una prueba inestable destruye la confianza en toda la suite: se deja de leer los fallos y el día que hay uno real se ignora. El `sleep` tapa el síntoma y hace la suite más lenta, que es el otro camino hacia que nadie la ejecute.
:::
