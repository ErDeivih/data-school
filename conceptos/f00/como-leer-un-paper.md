---
id: como-leer-un-paper
titulo: Cómo leer un paper
fase: 0
nivel: intermedio
rutas: [core, ds]
prerequisitos: [como-estudiar, hacer-preguntas-buenas]
tags: [papers, lectura, investigacion, metodo]
resumen: Tres pasadas de coste creciente, saber cuándo abandonar y mirar la tabla de resultados antes que las matemáticas: leer un paper es un presupuesto.
fuentes: ["Keshav (2007), 'How to Read a Paper'"]
---

## En una frase

Un paper no se lee como un libro: se le dan tres pasadas de coste creciente, y solo se paga la
tercera si la segunda ha merecido la pena. La mayoría de los papers se abandonan en la primera, y
eso es un éxito del método, no un fracaso tuyo.

## La idea

Piensa en visitar un piso. Primero lo miras desde la calle: ¿está en la zona que quieres? Cinco
minutos y ya sabes si conviene subir. Después lo recorres por dentro: distribución, luz,
ruidos. Y solo si vas a comprarlo llamas al fontanero para que revise la instalación.

Keshav describió en 2007 el **método de las tres pasadas**: primero un filtro de cinco minutos
para decidir si el paper te interesa, después una hora para entender qué hace y con qué evidencia,
y solo en unos pocos papers al año una tarde entera para reproducir el razonamiento y cuestionar
cada supuesto. El coste y el criterio de salida de cada pasada están en la tabla de abajo.

Sobre las matemáticas, una regla que ahorra horas: **no se leen como un texto, se interrogan**.
¿Qué entra? ¿Qué sale? ¿Qué se supone?

Si una demostración no cambia lo que vas a hacer, sáltala
en la segunda pasada. Y apunta cada símbolo que aparezca sin definir: muchas veces el paper no lo
define porque lo hereda de otro, y ahí está la mitad de tu confusión.

Abandonar es parte del método. Señales claras: tras la primera pasada no sabes qué aporta; la
evaluación no permite distinguir el método del ruido; los datos no son accesibles y el método
depende de ellos; o el propio paper no define su métrica principal. Con 40 papers delante, el
recurso escaso es tu hora, no los papers.

## Definición formal

El método, con su coste y su criterio de salida:

| Pasada | Tiempo | Qué lees | Sales con |
| --- | --- | --- | --- |
| 1 | 5-10 min | título, resumen, introducción, títulos, conclusiones, figuras | qué problema resuelve y qué aporta |
| 2 | 30-60 min | cuerpo completo y tablas en detalle | un resumen con la evidencia y una lista de dudas |
| 3 | 2-5 h | demostraciones, apéndices, código | puedes reimplementarlo y decir qué supuestos son frágiles |

**Regla de parada:** pasa a la pasada siguiente solo si puedes escribir tres frases: (a) qué
problema resuelve, (b) qué hace distinto de lo anterior, (c) qué evidencia lo sostiene. Si (c) no
te sale, no es tu matemática la que falla: el paper no lo demuestra bien, o no lo has mirado. Y si sí lo demuestra, lo que falló fue el tiempo que le dedicaste, que también conviene apuntar.

Vocabulario que aparece en cualquier sección de resultados:

- **baseline** — el método de referencia contra el que se compara. Si es débil, la mejora no dice
  casi nada.
- **ablación** — repetir el experimento quitando una pieza para ver cuánto aporta esa pieza.
- **semilla** — el número que fija la aleatoriedad. Un solo resultado, sin semillas ni dispersión,
  es una anécdota.
- **barra de error** — el rango de incertidumbre de una cifra. Sin ella, dos números que difieren
  en la tercera decimal son indistinguibles.
- **prepublicación (preprint)** — manuscrito colgado antes de pasar revisión por pares. Puede ser
  buenísimo, pero nadie lo ha filtrado.
- **tamaño del efecto** — cuánto mejora, en unidades que signifiquen algo. La significancia solo
  dice que no es cero.

Y las seis preguntas que hay que hacerle siempre a la tabla de resultados: ¿cuál es el baseline y
es razonable?; ¿qué datos y qué partición, y se tocó el conjunto de prueba?; ¿cuántas semillas y
con qué dispersión?; ¿de qué parte del método viene la mejora (hay ablación)?; ¿la comparación se
hizo en igualdad de condiciones?; ¿puede haber fuga de datos?

## Ejemplo

Un paper imaginario reporta una exactitud media de 0,9116 con 5 semillas frente a 0,9052 del
baseline. Los números están inventados a propósito; la cuenta es la que hay que hacer siempre.

| Método | Exactitud por semilla | Media |
| --- | --- | --- |
| Propuesto | 0,911 · 0,918 · 0,905 · 0,915 · 0,909 | 0,9116 |
| Baseline | 0,906 · 0,902 · 0,911 · 0,899 · 0,908 | 0,9052 |

La diferencia es 0,0064. Con esa dispersión entre semillas (desviación típica de 0,0051 y 0,0048),
el error típico de la diferencia ronda 0,0031: la mejora son unos **2 errores típicos**. Eso es «puede que haya algo»,
no una revolución. Antes de cambiar tu sistema por este método, busca en el
paper si la diferencia se sostiene con más semillas y con otro conjunto de datos.

## Código

```python verificable
import numpy as np

# Numeros de ejemplo (inventados) para la cuenta que hay que hacer al leer
# cualquier tabla de resultados con semillas.
propuesto = np.array([0.911, 0.918, 0.905, 0.915, 0.909])
baseline = np.array([0.906, 0.902, 0.911, 0.899, 0.908])

def error_tipico(a):
    return a.std(ddof=1) / np.sqrt(a.size)      # incertidumbre de la media

diferencia = propuesto.mean() - baseline.mean()
ee = np.sqrt(error_tipico(propuesto) ** 2 + error_tipico(baseline) ** 2)

print(f"medias       {propuesto.mean():.4f} vs {baseline.mean():.4f}")
print(f"diferencia   {diferencia:+.4f}")
print(f"en errores tipicos {diferencia / ee:.2f}")   # -> 2.05: prometedor, no concluyente
```

```python verificable
import numpy as np

# Por que hay que mirar cuantos experimentos se probaron: si un paper prueba 20
# variantes y publica la mejor, el ganador puede salir de puro ruido.
rng = np.random.default_rng(0)
n, variantes = 30, 20
t = []
for _ in range(variantes):
    a = rng.normal(0.0, 1.0, n)
    b = rng.normal(0.0, 1.0, n)      # mismo proceso: no hay ninguna diferencia real
    t.append((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / n + b.var(ddof=1) / n))

print("t de la mejor de 20 variantes:", round(max(t), 2))   # -> 2.42
print("variantes con t > 2:", int(np.sum(np.abs(t) > 2)), "de", variantes)   # -> 4 de 20
```

## Errores típicos

- **Leerlo de principio a fin, en orden, y atascarte en una demostración.** Es el error que más
  tiempo cuesta. Resumen, figuras y conclusiones primero; el cuerpo, solo si el paper pasa el
  filtro; las demostraciones, solo si vas a usar el resultado.
- **Creerte el resumen sin mirar las tablas.** El resumen lo escribe quien quiere que lo cites. Las
  cifras reales, con su dispersión, están en la tabla.
- **Confundir «significativo» con «importante».** Un [[p-valor|p-valor]] pequeño con un efecto
  minúsculo es perfectamente posible: mira el [[tamano-del-efecto|tamaño del efecto]] y su
  intervalo.
- **Ignorar cuántas configuraciones se probaron.** Veinte variantes y publicar la mejor infla el
  resultado aunque el método no valga nada: es el problema de la
  [[multiplicidad-y-fdr|multiplicidad]]. Si no hay corrección, desconfía.
- **No mirar la partición de datos.** Si el conjunto de prueba se usó para elegir
  [[seleccion-de-hiperparametros|hiperparámetros]], el número que se reporta está inflado. Y si hay
  variables calculadas con datos futuros, la [[fuga-de-datos|fuga de datos]] hace magia.
- **Dar por revisado un preprint.** Estar en un repositorio público no es haber pasado revisión
  por pares.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es el objetivo de la primera pasada de un paper?
o: Entender todas las demostraciones matemáticas
o: Decidir en pocos minutos si el paper merece una lectura completa
o: Copiar la bibliografía para saber qué leer después
a: 2
e: La primera pasada es un filtro barato: título, resumen, introducción, títulos, conclusiones y figuras, para saber qué problema resuelve y qué aporta. Las demostraciones son material de la tercera pasada, y la bibliografía se consulta cuando ya has decidido que el paper te interesa.
:::

:::quiz
p: Un paper reporta 0,9116 frente a 0,9052 del baseline, con una desviación entre semillas de 0,005. ¿Qué conclusión es razonable?
o: El método nuevo es claramente superior y hay que adoptarlo
o: La diferencia es de unos dos errores típicos: es una señal débil que hay que confirmar con más semillas y otros datos
o: La diferencia es irrelevante porque no llega al 1 %
a: 2
e: Con cinco semillas y esa dispersión, el error típico de la diferencia es de unas tres milésimas, así que la mejora está a dos errores típicos de cero: prometedor, no demostrado. Descartarla por «menos del 1 %» también es un error: la relevancia depende de qué se mida, no de un porcentaje fijo.
:::

:::aviso
Leer papers cansa más que escribir código, y no se puede hacer ocho horas seguidas. Dos papers
bien leídos a la semana, con notas de media página cada uno, rinden mucho más que veinte
descargados y hojeados. Si no tomas notas, en un mes no recordarás ni de qué iban.
:::
