---
id: notebooks-vs-scripts
titulo: Notebooks frente a scripts
fase: 3
nivel: básico
rutas: [core, ds, de]
prerequisitos: [entorno-python, tipos-y-estructuras-python]
tags: [jupyter, reproducibilidad, estado, herramientas]
resumen: Cuándo usar un notebook y cuándo un script, por qué el estado oculto arruina la reproducibilidad y cómo saber si tu análisis se puede repetir.
fuentes: ["Pimentel et al. (2019), 'A Large-Scale Study About Quality and Reproducibility of Jupyter Notebooks'", "Rule et al. (2019), 'Ten Simple Rules for Reproducible Research in Jupyter Notebooks'"]
---

## En una frase

Un notebook es un cuaderno de laboratorio para explorar y mirar resultados; un script es una
receta que se ejecuta de arriba abajo y da siempre lo mismo. El problema no es ninguno de los
dos: es no saber cuál toca.

## La idea

Imagina que estás cocinando algo nuevo. Pruebas, corriges el punto de sal, añades un poco de
pimienta, vuelves a probar. Eso es un notebook: cada celda es un cucharazo, ves el resultado al
instante y decides el siguiente paso con los ojos. Es la mejor herramienta que existe para
**explorar**, y por eso casi todo el análisis de datos empieza ahí.

Ahora imagina que tienes que servir ese plato 300 veces al día, siempre igual, y que si un día
sale mal alguien tiene que poder averiguar por qué. Ya no sirve «un poco de sal a ojo»: hace
falta una receta escrita, con cantidades y un orden. Eso es un script.

El problema aparece cuando se mezclan. En un notebook **tú eliges el orden** en que se ejecutan
las celdas, y el fichero guarda el orden en que están escritas, que puede ser distinto. Nada
impide definir una variable en la celda 5 y usarla en la celda 2: en el fichero eso se lee en
el orden contrario, y al reiniciar el kernel la celda 2 falla. A esto se le llama **estado
oculto**, y es la causa número uno de que un análisis no se pueda reproducir.

Un ejemplo diminuto para verlo. Si en la celda 1 escribes `datos = [3, 1, 2]` y en la celda 2
escribes `datos.sort(); print(datos)`, el resultado depende de si la primera se ejecutó antes.
En el fichero siempre se lee en el mismo orden; en la sesión, no. Al día siguiente ejecutas de
arriba abajo y sale lo mismo que el fichero dice, pero lo que apuntaste en tus conclusiones
salió del orden inverso.

La buena noticia es que la solución es mecánica, no artesanal:

1. **Reinicia el kernel y ejecuta todo** antes de dar un análisis por bueno. Si el resultado no
   sale, el análisis estaba roto aunque las celdas de abajo dieran el número correcto.
2. **Los números se imprimen, no se copian a mano** en el texto. Un «la media es 3,2» escrito a
   mano deja de ser cierto en cuanto cambias el filtro de arriba.
3. **Cuando algo funciona, se convierte en script** y se le pasa un test
   ([[testing-con-pytest|con pytest]]), no se deja como una celda que hay que recordar pulsar.

## Definición formal

Un notebook es un fichero JSON con una lista ordenada de celdas. Cada celda tiene un tipo y, si
se ha ejecutado, un contador:

- `cell_type`: `"code"`, `"markdown"` o `"raw"`.
- `source`: las líneas de la celda. En el formato actual es una lista de cadenas.
- `execution_count`: el número de orden **real** de ejecución dentro de la sesión. Vale `null`
  si la celda nunca se ha ejecutado.
- `outputs`: lo que la celda imprimió la última vez que se ejecutó. **Se guarda en el
  fichero**, y por eso un notebook con salidas puede pesar megas y mostrar resultados de una
  sesión anterior.
- `metadata.kernelspec`: qué kernel (intérprete) hay que usar para ejecutarlo.

De ahí salen dos definiciones que conviene tener claras:

- **Estado oculto:** diferencia entre lo que el fichero dice, en orden, y lo que hace falta para
  que las celdas produzcan las salidas guardadas. Se detecta comparando las celdas con
  `execution_count` no nulo contra su posición en el fichero: si los números no van en orden
  creciente, algo se ejecutó fuera de sitio.
- **Reproducible:** ejecutar el notebook entero, desde un kernel limpio, produce las mismas
  salidas. Un análisis que solo funciona si ejecutas «la celda 7 antes que la 3» no es
  reproducible, es una sesión que se perdió.

:::formula
ejecutar_todo(kernel_limpio) = salidas_guardadas   ⇒   reproducible
:::

La flecha de implicación resume la prueba: no hay que inspeccionar el código a ojo, hay que
reiniciar y ejecutar todo. Si el resultado coincide, da igual en qué orden se ejecutaron las
celdas aquel día.

## Ejemplo

Estas son las celdas de código de un notebook real, en el orden en que están escritas, con su
contador de ejecución:

```
celda 0:  execution_count = 3    cargar_ventas()          <- se ejecuto la ultima
celda 1:  execution_count = 1    ventas = cargar_ventas() <- se ejecuto la primera
celda 2:  execution_count = 2    print(ventas.head())     <- se ejecuto la segunda
```

Leído de arriba abajo, el notebook intenta usar resultados antes de calcularlos. Y sin embargo,
cuando lo abres, **se ven los resultados**: están guardados en `outputs` de la sesión anterior.
Ese es el engaño del estado oculto: el fichero parece funcionar y no funciona.

Como se detecta con números: hay 3 celdas, los contadores son [3, 1, 2]. Comparando cada
contador con la posición que le tocaría en el fichero (1, 2, 3) no coincide ninguno, así que las
tres celdas están fuera de sitio. Y el recorrido de los contadores no es creciente, porque el 3
va antes que el 1 y el 2. Con una línea de código lo compruebas y te ahorras publicar un análisis
que no se repite.

## Código

```python verificable
# Detector de estado oculto: compara el orden real de ejecucion con el orden del fichero.
celdas = [
    {"nombre": "cargar_ventas()", "execution_count": 3},
    {"nombre": "ventas = cargar_ventas()", "execution_count": 1},
    {"nombre": "print(ventas.head())", "execution_count": 2},
]

contadores = [c["execution_count"] for c in celdas]
escritas = [c["nombre"] for c in sorted(celdas, key=lambda c: c["execution_count"])]

print("celdas ejecutadas:", len(contadores))
print("contadores en orden creciente:", contadores == sorted(contadores))
print("empieza el fichero por:", celdas[0]["nombre"])
print("pero se ejecuto primero:", escritas[0])
print("celdas fuera de sitio:", sum(1 for i, c in enumerate(contadores) if c != i + 1))
```

```python verificable
# No hay que reejecutar el notebook para auditar el orden: basta leer los contadores.
import json

cuaderno = {
    "cells": [
        {"cell_type": "code", "execution_count": 2, "source": ["x = 1\n"]},
        {"cell_type": "markdown", "source": ["# Analisis\n"]},
        {"cell_type": "code", "execution_count": 1, "source": ["print(x)\n"]},
        {"cell_type": "code", "execution_count": None, "source": ["print('sin ejecutar')\n"]},
    ],
    "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"}},
}

crudo = json.dumps(cuaderno)
codigo = [c for c in cuaderno["cells"] if c["cell_type"] == "code"]
sin_ejecutar = [c for c in codigo if c["execution_count"] is None]

print("celdas totales:", len(cuaderno["cells"]))
print("celdas de codigo:", len(codigo))
print("sin ejecutar:", len(sin_ejecutar))
print("kernel:", cuaderno["metadata"]["kernelspec"]["name"])
print("el kernel no viaja en el codigo, solo el nombre:", '"import"' in crudo)
```

```python verificable
# Por que un notebook con salidas ensucia el control de versiones:
# las imagenes van dentro del JSON, en base64.
import json

def peso_aproximado(celdas_con_salida: int, kb_por_grafico: int = 120) -> int:
    """Kilobytes que ocupan las salidas guardadas de un notebook."""
    return celdas_con_salida * kb_por_grafico

print("10 graficos guardados:", peso_aproximado(10), "KB")
print("con 5 graficos:", peso_aproximado(5), "KB")
print("y cada reejecucion los reescribe enteros: True")

# La solucion no es borrar el notebook: es ejecutar sin guardar salidas
# (jupyter nbconvert --to notebook --execute) o versionar solo el .py generado.
```

## Errores típicos

- **Comparar resultados de dos notebooks sin reiniciar.** El clásico: cambias una constante,
  ejecutas dos celdas de abajo y comparas el número nuevo con el viejo. Puede que el número
  nuevo no incorpore el cambio, porque la celda que lo aplica está más arriba y no se ha
  ejecutado. Reinicia y ejecuta todo antes de comparar nada.
- **Copiar a mano los resultados al texto.** «El modelo da un AUC de 0,87» escrito en una celda
  de markdown deja de ser cierto con el primer cambio de datos y nadie se entera. Imprímelo con
  `print()` o con un `f-string` en una celda de código, para que se recalcule.
- **Guardar el notebook con las salidas dentro.** Las imágenes van codificadas en base64 dentro
  del propio JSON: un cuaderno con diez gráficos engorda cientos de kilobytes y cada
  reejecución reescribe el fichero entero, así que el `git diff` es ilegible y no puedes revisar
  qué cambió de verdad. Ejecuta con `--execute` sin guardar salidas, o guarda el `.py`.
- **Un notebook que importa de otro notebook.** Las importaciones entre cuadernos con `%run` o
  con `importlib` son frágiles y dependen del directorio de trabajo. Si dos análisis comparten
  código, ese código va a un módulo `.py` con nombre, no a una celda que se copia y se pega.
- **Celdas que solo funcionan en un orden.** Definir en una celda y usar antes de definirla es
  un error que el notebook no detecta, porque nunca lo ejecuta entero. Un script lo detecta
  siempre: se ejecuta de arriba abajo o falla.
- **Dar por reproducido un análisis que necesita base de datos, rutas locales y una API.** El
  notebook depende del entorno. Un script con sus dependencias declaradas y
  [[entorno-python|un entorno reproducible]] es la única forma de que otra persona lo ejecute.

:::truco
Convierte la exploración en script en cuanto el análisis se estabilice, con
`jupyter nbconvert --to script analisis.ipynb`. A partir de ahí, el notebook solo sirve para
enseñar los resultados y el script es lo que se ejecuta. La regla práctica: si vas a repetir el
análisis más de dos veces, ya es un script.
:::

:::practica
enunciado: Tres celdas de código, en este orden de fichero: `print(resumen)`, `resumen = ventas.groupby("ciudad").sum()` y `ventas = cargar_ventas()`. Sus `execution_count` son 3, 2 y 1. ¿Qué falla al reiniciar el kernel y ejecutar todo de arriba abajo, y cuántas celdas estaban fuera de sitio?
pista: Compara cada contador con la posición que la celda ocupa en el fichero, no con el contador de la celda anterior.
solucion: Al ejecutar de arriba abajo, la primera celda usa `resumen`, que todavía no existe: `NameError`. Funcionó porque se ejecutó de abajo arriba: 1, 2 y 3. Comparando cada contador con su posición en el fichero (1, 2, 3), el 3 frente al 1 y el 1 frente al 3 no coinciden: dos celdas estaban fuera de sitio y la lista 3, 2, 1 no es creciente. Conclusión: no es reproducible hasta reordenar las celdas.
:::

## Comprueba que lo sabes

:::quiz
p: Abres un notebook y todas las celdas muestran resultados correctos. ¿Basta eso para darlo por reproducible?
o: Sí, si los resultados están ahí es que el análisis funciona
o: No: hay que reiniciar el kernel y ejecutar todo de arriba abajo, porque las salidas guardadas pueden venir de celdas ejecutadas en otro orden
o: No, pero basta con ejecutar la última celda para comprobarlo
a: 2
e: Las salidas están guardadas en el fichero y sobreviven al cierre del kernel, así que un notebook puede enseñar resultados que ya no se pueden volver a producir sin ejecutar las celdas en el orden en que se ejecutaron aquella vez. La prueba definitiva es reiniciar el kernel y usar «Ejecutar todo»: si sale lo mismo, es reproducible.
:::

:::quiz
p: ¿Cuál de estas tareas encaja mejor en un script que en un notebook?
o: Probar cinco transformaciones distintas de una variable para ver cuál queda mejor
o: Generar cada noche el informe de ventas a partir de la base de datos
o: Mirar los primeros registros de un fichero recién recibido
a: 2
e: Un proceso que se repite solo, sin nadie mirando y que debe dar siempre lo mismo, es un script (idealmente con un test que lo compruebe). Explorar transformaciones y mirar los primeros registros son tareas interactivas de un solo uso, y ahí el notebook es más rápido. La pregunta que decide es «¿lo voy a repetir sin mirar?».
:::

:::trampa
El botón «Reiniciar y ejecutar todo» no arregla el estado oculto: lo **revela**. Si al pulsarlo
todo falla o los números cambian, el notebook estaba mintiendo, y lo que hay que arreglar es el
orden de las celdas, no volver a ejecutar las de abajo hasta que se vea el número que uno
esperaba.
:::
