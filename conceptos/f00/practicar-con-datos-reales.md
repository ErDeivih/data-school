---
id: practicar-con-datos-reales
titulo: Practicar con datos reales
fase: 0
nivel: básico
rutas: [core, ds]
prerequisitos: [hacer-preguntas-buenas]
tags: [practica, proyectos, portfolio, datos]
resumen: Los datasets de juguete vienen limpios y con el problema ya resuelto. Practica con datos sucios y de verdad, y termina el proyecto: eso es lo que se puede enseñar.
fuentes: ["Wickham (2014), 'Tidy Data'"]
---

## En una frase

Aprender con datasets de juguete es como aprender a cocinar en una cocina de juguete: los datos
llegan limpios, con las variables ya elegidas y la pregunta ya decidida. Practica con datos
sucios, grandes y reales, y termina lo que empiezas.

## La idea

Coge cualquier dataset de manual: viene sin nulos, con los tipos correctos, con la variable
objetivo ya marcada y con el problema formulado por otra persona. Todo lo difícil —entender qué
significa una fila, decidir qué hacer con los huecos, dudar de una columna— ya está hecho. Por eso
se avanza tan rápido y por eso se aprende tan poco.

En el trabajo real, la mayor parte del esfuerzo está justo en esa parte previa. Y la segunda
diferencia es el final: un análisis que no termina en una conclusión escrita no existe para nadie.
De ahí la afirmación incómoda de este concepto: **un proyecto terminado y documentado dice más de
ti que veinte certificados**, porque un certificado acredita que asististe y un
[[portfolio-y-proyectos|portfolio]] deja que cualquiera compruebe qué sabes hacer.

De dónde sacar datos, por tipo y con su trampa:

| Fuente | Qué tiene | La trampa |
| --- | --- | --- |
| Estadística oficial (INE, Eurostat, Banco Mundial) | series largas y metadatos decentes | vienen agregados, con notas metodológicas que hay que leer |
| Repositorios de ML (UCI, Kaggle, OpenML) | tablas listas para modelar, con objetivo | muchos están tan trabajados que el resultado ya es el esperado |
| Datos abiertos de ciudades | transporte, tráfico, aire, con grano fino | los códigos y las categorías cambian entre años |
| APIs públicas | clima, tipos de cambio, vuelos: datos frescos | límites de peticiones, claves y formatos que cambian |
| Tus propios datos | gastos, entrenamientos, sensores de casa | son pequeños: hacen falta meses para ver algo |
| Datos de tu trabajo, con permiso | lo más parecido al trabajo real | privacidad: anonimiza antes de sacarlos de su sitio |

Tres niveles de práctica, en este orden: **reproducir** un análisis ajeno paso a paso (sirve para
aprender herramientas), **responder** una pregunta propia con una métrica y un criterio, y
**construir** un proyecto completo —ingesta, limpieza, análisis, conclusión y README— que otra
persona pueda ejecutar desde cero. El tercero es el único que enseña el oficio entero.

## Definición formal

Un dataset sirve para practicar si cumple estas propiedades, y conviene comprobarlas **antes** de
empezar con un [[perfilado-de-datos|perfilado rápido]]:

- **granularidad** — qué representa una fila. Si no lo sabes, cualquier agregación que hagas es
  una apuesta.
- **cobertura** — qué periodo y qué subconjunto del mundo cubre, y qué falta.
- **tamaño** — suficiente para que aparezcan casos raros, no tanto que no puedas abrirlo.
- **suciedad** — nulos, duplicados, tipos mezclados, categorías escritas de tres formas: lo que
  mide la [[calidad-de-datos|calidad de datos]].
- **documentación** — diccionario de variables. Sin él se paga en horas lo que se ahorra en
  descargas.
- **licencia y condiciones de uso** — qué puedes publicar y qué no.
- **actualización** — si es una foto fija o un flujo que se refresca.

Y un **proyecto terminado** es el que cumple tres condiciones: se ejecuta desde cero siguiendo el
README, responde a una pregunta escrita antes de mirar los datos, y declara sus límites. Si te
falta la tercera, el proyecto parece una promesa de marketing.

## Ejemplo

Dos proyectos candidatos para el primer fin de semana:

| Tarea | A: alquiler por distrito | B: retrasos de vuelos |
| --- | --- | --- |
| Descargar y leer el diccionario | 1,5 h | 1 h |
| Limpiar y unir fuentes | 2 h | 6 h |
| Análisis y gráficos | 3 h | 3 h |
| README y conclusión | 2 h | 2 h |
| **Total** | **8,5 h** | **12 h** |

Empieza por el A. Con menos horas de fontanería practicas lo mismo —descargar, perfilar, limpiar,
agrupar, graficar y escribir— y llegas al final, que es la parte que casi nadie alcanza. El B
enseña a unir fuentes con códigos que no cuadran, que es una habilidad valiosa, pero mejor como
segundo proyecto, cuando ya has terminado uno y sabes cuánto cuesta el último 20 %.

Regla de oro: **los datos en crudo no se tocan**. Guarda el fichero original en una carpeta de solo
lectura, escribe el código que lo transforma y sigue las reglas de [[git-para-datos|Git para
datos]]: se versiona el código, no los datos. Así, cuando un número no cuadre, siempre puedes
volver al principio.

## Código

```python verificable
import io
import pandas as pd

# Los datos van escritos aqui, pero el patron es el mismo con un CSV de 2 GB: antes
# de analizar nada, mira tipos, duplicados, nulos y rangos.
crudo = """ciudad,anyo,precio_m2,operaciones
Madrid,2023,4200,185
Madrid,2024,4380,171
Valencia,2023,1980,96
Valencia,2024,,88
Sevilla,2023,1750,54
Sevilla,2023,1750,54
"""
df = pd.read_csv(io.StringIO(crudo))

print(df.dtypes.to_string())
print("filas:", len(df), "| duplicadas:", int(df.duplicated().sum()))   # -> 6 | 1
print("nulos:", df.isna().sum().to_dict())        # -> solo precio_m2, con 1 nulo
print(df.groupby("ciudad")["precio_m2"].median().to_string())   # -> Madrid 4290, Sevilla 1750, Valencia 1980
```

```python verificable
import pandas as pd

# Un duplicado no cambia la mediana y si infla las sumas: comprueba el grano antes
# de agregar. Aqui hay dos filas identicas de Sevilla.
df = pd.DataFrame({"ciudad": ["Sevilla"] * 3 + ["Madrid"],
                   "operaciones": [54, 54, 61, 185]})
limpio = df.drop_duplicates()

print("suma con duplicado :", int(df["operaciones"].sum()))         # -> 354
print("suma tras deduplicar:", int(limpio["operaciones"].sum()))    # -> 300
print(limpio.groupby("ciudad")["operaciones"].sum().to_dict())      # -> Madrid 185, Sevilla 115
```

## Errores típicos

- **Encadenar tutoriales sin escribir tu propio análisis.** Ver a otra persona resolver un caso no
  entrena las decisiones. Coge el mismo dataset y responde a una pregunta distinta de la del
  tutorial.
- **Modificar el fichero original.** Si reescribes el CSV a mano, pierdes la posibilidad de
  reproducir el análisis y de detectar tu propio error. Original intacto, transformación en código.
- **Subir datos con información personal a un repositorio público.** Nombres, correos, direcciones
  o identificadores, aunque parezcan inofensivos, son
  [[privacidad-y-gdpr|datos personales]]. Anonimiza antes de sacar nada de su sitio.
- **Mirar los datos antes de decidir la pregunta.** Si empiezas explorando sin criterio, acabas con
  ocho gráficos y ninguna conclusión; es el camino más corto a un análisis que no responde a nada.
- **Coleccionar certificados en lugar de proyectos.** Un certificado no se puede inspeccionar. Un
  repositorio con un README claro sí: enseña la pregunta, el método, el resultado y lo que no
  sabes.
- **Abandonar al 80 %.** El proyecto sin README y sin conclusión no existe para nadie, ni para ti
  dentro de tres meses. Media hora de escritura es lo que convierte el trabajo en algo enseñable.

## Comprueba que lo sabes

:::quiz
p: ¿Qué le falta a un análisis que acaba con ocho gráficos y ninguna conclusión escrita?
o: Más gráficos, para cubrir todos los ángulos
o: Una pregunta decidida antes de mirar los datos y un criterio para decidir qué se concluye
o: Un modelo de machine learning
a: 2
e: Sin una pregunta previa ni un criterio, la exploración no termina: siempre queda algo por mirar. La conclusión escrita, con sus límites, es lo que convierte el trabajo en un resultado utilizable. Un modelo no es requisito de nada.
:::

:::quiz
p: ¿Cuándo puedes decir que un proyecto de datos está terminado?
o: Cuando el código funciona en tu portátil y tienes los gráficos en pantalla
o: Cuando otra persona puede ejecutarlo desde cero siguiendo el README, entiende la pregunta, el resultado y los límites
o: Cuando lo has subido a un repositorio, aunque no tenga documentación
a: 2
e: «Funciona en mi portátil» no es reproducibilidad, y un repositorio sin README es un montón de ficheros. Lo que hace útil un proyecto es que la pregunta, el resultado y sus límites estén escritos y que los pasos se puedan repetir.
:::

:::practica
enunciado: Elige un dataset público de estadística oficial con granularidad de municipio y año, y plantea un proyecto que puedas terminar en una tarde. Escribe la pregunta, la métrica y el criterio de decisión antes de descargar nada.
pista: Empieza por lo que cabe en una tarde: un fichero, una pregunta, un gráfico honesto y un README.
solucion: Una pregunta posible: «¿La renta media por municipio de mi provincia creció más entre 2019 y 2022 en los municipios de menos de 5.000 habitantes que en los de más de 20.000?». Unidad: municipio-año. Métrica: variación porcentual de la renta media en el periodo. Comparación: dos grupos de tamaño de municipio. Criterio: si la diferencia supera 3 puntos, merece la pena mirar la composición por edad antes de contar nada. El proyecto termina con un README que incluye la pregunta, de dónde salen los datos, cómo se ejecuta, el resultado y sus límites (municipios que cambiaron de denominación, años con revisión metodológica).
:::

:::trampa
El primer proyecto siempre se sobreestima. Si crees que necesitas tres fuentes, un modelo y un
cuadro de mando interactivo, no lo vas a terminar. Un fichero, una pregunta y una conclusión
escrita enseñan más que un esqueleto de proyecto ambicioso abandonado a la mitad.
:::
