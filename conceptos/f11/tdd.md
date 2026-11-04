---
id: tdd
titulo: Desarrollo guiado por pruebas
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [testing-con-pytest, testing-piramide]
tags: [testing, diseno, refactorizacion, ciclo]
resumen: Rojo, verde, refactor: escribir la prueba antes que el código convierte el diseño en una decisión consciente y el ritmo en minutos en vez de días.
fuentes: ["Beck (2002), 'Test-Driven Development: By Example'", "Beck (1999), 'Extreme Programming Explained: Embrace Change'", "Feathers (2004), 'Working Effectively with Legacy Code'"]
---

## En una frase

TDD es un ciclo de tres pasos —escribir una prueba que falle, escribir el mínimo código para que
pase, limpiar el código— repetido en pasos de uno a cinco minutos, de forma que nunca pases más
de unos minutos sin saber si lo que hiciste funciona.

## La idea

Cuando cocinas para diez personas no pruebas la salsa al final, cuando ya está todo emplatado.
La pruebas cada pocos minutos, y si algo va mal lo corriges entonces, no cuando ya no hay
remedio. La diferencia no es la salsa: es la longitud del bucle de realimentación.

TDD es eso aplicado al código. En lugar de escribir doscientas líneas, ejecutar y depurar un
error que puede estar en cualquiera de ellas, escribes una prueba que describe un trozo pequeño
de comportamiento, la ves fallar, escribes lo mínimo para que pase y repites. Cada vuelta dura
minutos y cada vuelta termina con la suite entera en verde.

Lo contraintuitivo es lo siguiente: **el objetivo de TDD no son las pruebas**. Las pruebas son
el subproducto. El objetivo es el diseño. Si escribir la prueba de una función es un infierno
—porque necesita media aplicación levantada, porque toca seis objetos globales, porque devuelve
un `DataFrame` de catorce columnas— eso no es un problema de la prueba: es información sobre el
diseño. TDD te obliga a mirar esa información en el momento en el que arreglarla cuesta diez
minutos, en vez de tres semanas después.

Las tres leyes que suelen citarse resumen el mecanismo:

1. No escribas código de producción hasta tener una prueba que falle.
2. No escribas más prueba de la que basta para fallar; que no compile o que falte la función ya
   cuenta como fallo.
3. No escribas más código del necesario para que la prueba pase.

La tercera ley es la que más cuesta cumplir, y es la que aporta el beneficio: prohíbe el código
«por si acaso». El ciclo es:

- **Rojo.** Escribe la prueba y ejecútala. Tiene que fallar, y por el motivo correcto: lo que
  debe fallar es la aserción, no un `import` mal escrito ni una coma. Si pasa a la primera, o la
  prueba no comprueba nada o el comportamiento ya existía.
- **Verde.** Escribe lo mínimo para pasar, aunque sea feo. Vale devolver un valor fijo escrito a
  mano: se llama *falsificar* y es legítimo, porque el caso siguiente te obligará a generalizar.
  Lo que no vale es escribir la generalización que crees que necesitarás.
- **Refactor.** Con la suite en verde, limpia duplicación, cambia nombres y extrae funciones.
  Esta parte es literalmente [[refactorizacion]], y solo es segura porque tienes la red puesta.

**Cuándo no aplicarlo.** TDD no es una obligación moral y hay situaciones donde estorba:
código de exploración donde todavía no sabes qué quieres (escribe el prototipo, tíralo y hazlo
en serio con pruebas), prototipos visuales, cuadernos de análisis de datos y scripts de un solo
uso. Y sobre código heredado sin una sola prueba, la primera tarea no es TDD: es escribir
pruebas de caracterización que fijen el comportamiento actual antes de tocar nada, para no
cambiar dos cosas a la vez.

## Definición formal

Sea `P` el conjunto de pruebas de la suite, `n` su número y `f` el número de las que fallan. La
invariante del ciclo se enuncia así: **en todo momento, `f ≤ 1`**, y la única prueba que puede
estar en rojo es la que acabas de escribir. Si `f ≥ 2` has salido del ciclo y estás depurando.

- **Prueba que falla por el motivo correcto.** El fallo debe ser una aserción incumplida, no un
  error de compilación, de importación o de sintaxis. En la práctica, en un lenguaje interpretado
  se admite el error de nombre como primer rojo (la función aún no existe), pero la segunda
  ejecución en rojo ya debe ser por la aserción.
- **Triangulación.** Cuando no sabes cómo generalizar, añade un segundo caso con números
  distintos; la implementación más simple que pasa los dos casos es, casi siempre, la
  generalización correcta.
- **Prueba de caracterización.** Prueba escrita sobre código existente que no tiene pruebas, cuyo
  único fin es fijar el comportamiento actual. No afirma que ese comportamiento sea el
  deseado: afirma que es el que hay, para detectar cambios accidentales.
- **Refactorización.** Cambio de la estructura del código que no altera su comportamiento
  observable. En TDD se hace siempre con la suite en verde y en pasos pequeños.

## Ejemplo

Una función `es_bisiesto(anio)`, construida caso a caso. La columna «implementación mínima» es
lo que escribirías en verde, y la última es la que sobrevive al refactor:

```text
caso nuevo (rojo)          implementacion minima (verde)
2024 -> True               return True
2023 -> False              return anio % 4 == 0
1900 -> False              return anio % 4 == 0 and anio % 100 != 0
2000 -> True               return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
```

Fíjate en el cuarto caso: con la regla de los tres primeros, 2000 daría `False`, y la prueba lo
caza. Esa es la razón de que el caso raro se escriba *antes* de la implementación general: si
escribes la fórmula completa de memoria y después añades las pruebas, la prueba del año 2000
pasa por casualidad y no demuestra nada.

Otro ejemplo de triangulación, con un descuento por volumen: la primera prueba dice que 10
unidades cuestan 9,00 € y la implementación mínima es devolver 9,00. La segunda dice que 20
unidades cuestan 16,00 €, y ahí ya no hay valor fijo que valga: aparece la regla real (un 10 %
hasta 10 unidades y un 20 % a partir de 11). Dos casos con números distintos han forzado la
generalización, sin escribir código especulativo.

## Código

```python verificable
# El ciclo rojo-verde escrito como script: primero la expectativa, luego la funcion.
def es_bisiesto(anio):
    # Los dos divisores cuentan: 1900 es divisible por 4 y por 100, asi que no es bisiesto.
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

casos = [(2024, True), (2023, False), (1900, False), (2000, True)]
# Desempaquetado de la tupla en el for: cada vuelta deja anio y esperado ya separados.
for anio, esperado in casos:
    obtenido = es_bisiesto(anio)
    # is compara con el True/False de verdad; == daria por bueno un 1 y ocultaria un fallo.
    assert obtenido is esperado, f"falla {anio}: esperaba {esperado} y da {obtenido}"
    print(f"{anio}: {obtenido}")

print("casos comprobados:", len(casos))     # -> 4
```

:::claves
- El `assert` solo comprueba; no imprime nada cuando pasa. Si el caso 2000 fallara, el
  programa se detendría ahí y los casos siguientes no llegarían a ejecutarse.
- `assert obtenido is esperado` compara identidad con el `True`/`False` de verdad. Con `==`,
  un `1` o un `1.0` pasarían como si fueran `True` y la prueba mentiría.
- La expresión del año bisiesto se lee de fuera hacia dentro: primero `% 4`, y ese resultado
  se combina con el paréntesis. `and` tiene más prioridad que `or`, de ahí los paréntesis.
- El reloj se **inyecta** como argumento. Si `es_fin_de_semana` llamara a `date.today()`, la
  prueba daría un resultado distinto cada día y no se podría comprobar el lunes.
- `weekday()` empieza en 0 el lunes, así que el fin de semana es `>= 5`. Con `isoweekday()`
  el domingo es 7 y la misma comparación sería incorrecta.
- En el fichero de pytest, `@pytest.mark.parametrize` genera **una prueba por fila**: cuatro
  casos, cuatro resultados independientes en el informe, no un solo test que los recorre.
:::

```python verificable
from datetime import date

# Inyectar la dependencia hace el codigo comprobable sin red, sin reloj real y sin base de datos.
class RelojFijo:
    def __init__(self, dia):
        self._dia = dia                 # el guion bajo es solo una convencion: "no lo toques"
    def hoy(self):
        return self._dia                # siempre el mismo dia: la prueba es determinista

def es_fin_de_semana(reloj):
    # weekday() cuenta desde 0 el lunes: sabado es 5 y domingo 6, de ahi el >= 5.
    return reloj.hoy().weekday() >= 5

# La funcion no llama a date.today(): recibe el dia desde fuera, y eso la hace testeable.
print(es_fin_de_semana(RelojFijo(date(2024, 3, 9))))     # -> True
print(es_fin_de_semana(RelojFijo(date(2024, 3, 11))))    # -> False
```

```text
El mismo caso, como fichero de pytest (rojo primero, verde despues):

# test_bisiesto.py
import pytest
from calendario import es_bisiesto

@pytest.mark.parametrize("anio, esperado", [
    (2024, True), (2023, False), (1900, False), (2000, True),
])
def test_bisiesto(anio, esperado):
    assert es_bisiesto(anio) is esperado
```

## Errores típicos

- **Escribir todas las pruebas al principio.** Es la tentación más común: «ya sé lo que tiene
  que hacer, escribo las doce pruebas y luego implemento». Al hacerlo pierdes el ciclo: no ves
  fallar cada caso por separado, no triangulas y acabas con una implementación grande que no
  sabes si es la mínima. Una prueba, un rojo, un verde.
- **No ver el rojo.** Si escribes la prueba y pasas directamente al código sin ejecutarla, no
  sabes si la prueba comprueba algo. Una prueba que no puede fallar (porque el `assert` está mal
  escrito, porque compara un objeto consigo mismo o porque no llega a ejecutarse) es peor que no
  tenerla: da confianza falsa.
- **Pasar de rojo a verde con la solución completa.** Escribir la fórmula general en el primer
  verde elimina la triangulación y con ella la garantía de que has entendido los casos. El
  código «feo» intermedio es parte del método, no una pérdida de tiempo.
- **Saltarse el refactor.** Sin el tercer paso, el código crece con duplicación y TDD se queda
  en «pruebas escritas antes», que es solo la mitad del beneficio. Además, el refactor es lo que
  mantiene el ritmo: si no limpias cada pocos minutos, la siguiente prueba es más difícil de
  escribir.
- **Confundir TDD con cobertura total.** TDD no exige probar cada línea. Exige que ninguna línea
  de producción se escriba sin una prueba que la pida. Una rama defensiva que nunca se ejecuta no
  necesita una prueba que la visite: necesita que decidas si existe.
- **Aplicarlo a un cuaderno de exploración.** Cuando estás mirando datos y no sabes qué vas a
  encontrar, escribir la prueba antes te bloquea. Explora en el cuaderno, decide qué función
  quieres, y hazla en un módulo con su prueba. Mezclar las dos cosas produce pruebas que
  comprueban el resultado del último `print`.

## Comprueba que lo sabes

:::quiz
p: Escribes una prueba, la ejecutas y pasa a la primera. ¿Qué haces?
o: Continuar con la siguiente prueba, ya está cubierto
o: Sospechar: o el comportamiento ya existía, o la prueba no comprueba lo que crees, así que hay que revisarla
o: Borrarla, porque una prueba que pasa no aporta nada
a: 2
e: En el ciclo, el primer rojo demuestra que la prueba es capaz de detectar el fallo. Si pasa sin haber escrito código, es que el comportamiento ya estaba (y entonces quizá sobraba trabajo previo) o que el `assert` no comprueba nada. La prueba hay que revisarla, no borrarla.
:::

:::quiz
p: ¿Qué es triangular en TDD?
o: Dividir la implementación en tres funciones
o: Añadir un segundo caso con números distintos para que un valor fijo deje de pasar y aparezca la regla general
o: Ejecutar la suite tres veces antes de cada commit
a: 2
e: La triangulación usa los casos como presión: con un solo caso, devolver un valor escrito a mano pasa; con dos casos distintos, la única forma de pasar es generalizar. Es el mecanismo que evita escribir la solución completa de golpe.
:::

:::quiz
p: Tienes que tocar una función de 400 líneas sin ninguna prueba. ¿Cuál es el primer paso sensato?
o: Reescribirla desde cero con TDD
o: Escribir pruebas de caracterización que fijen lo que hace hoy, y solo después cambiar
o: Cambiar y ver qué se rompe en producción
a: 2
e: Sin red, cualquier cambio mezcla dos cosas: lo que querías cambiar y lo que rompiste sin querer. Las pruebas de caracterización documentan el comportamiento actual —aunque sea feo— y convierten el cambio en algo verificable. Reescribir de cero pierde el conocimiento acumulado en esos casos raros.
:::
