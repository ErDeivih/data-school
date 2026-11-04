---
id: privacidad-y-gdpr
titulo: Privacidad y RGPD
fase: 11
nivel: avanzado
rutas: [alg, de]
prerequisitos: [kafka-y-colas, seguridad-owasp]
tags: [privacidad, rgpd, retencion, anonimizacion]
resumen: Base legal, minimización, derechos del interesado y retención: cómo se recogen datos personales en una analítica sin construir un problema legal ni técnico.
fuentes: ["Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, Reglamento General de Protección de Datos", "Agencia Espanola de Proteccion de Datos, 'Guia del Reglamento General de Proteccion de Datos'"]
---

## En una frase

El RGPD no prohíbe usar datos personales: obliga a saber **por qué** los tienes, a recoger
los mínimos, a no guardarlos más de lo necesario y a poder borrarlos cuando te lo pidan.

## La idea

Imagina que montas una analítica para saber cuánta gente usa cada pantalla de tu aplicación.
Lo primero que harías es guardar el identificador de usuario, la dirección IP, el modelo de
móvil y la ciudad, «por si acaso». Ese «por si acaso» es exactamente el problema: estás
recogiendo datos personales que no necesitas, con una finalidad que no has definido, y que
tendrás que proteger, declarar y borrar durante años.

La forma mental sana es la de una mudanza. Antes de meter algo en una caja te preguntas: ¿lo
voy a usar en la casa nueva? ¿cuánto tiempo me hace falta? ¿lo tiraré cuando caduque? Un
almacén de datos que no responde a esas tres preguntas se convierte en una nave industrial
llena de cajas que nadie puede abrir y que, legalmente, tienes que poder vaciar entera cuando
alguien lo pida.

Cuatro conceptos sostienen todo lo demás:

- **Dato personal.** Cualquier información sobre una persona identificada o identificable. No
  hace falta el nombre: la dirección IP, el identificador de publicidad del móvil, una cookie
  que te sigue entre sesiones y una matrícula lo son, porque permiten llegar a alguien. Y la
  definición es amplia a propósito: si combinando dos campos puedes señalar a una persona, esos
  campos son datos personales.
- **Categorías especiales.** Salud, origen étnico, opiniones políticas, religión, datos
  biométricos para identificar a alguien y orientación sexual. Están especialmente protegidos:
  para tratarlos necesitas una base específica, no vale el interés legítimo normal.
- **Base legal.** Todo tratamiento necesita una de las seis bases: consentimiento, ejecución
  de un contrato, obligación legal, interés vital, misión de interés público o interés
  legítimo. Elegir la base **es el primer paso**, no un trámite posterior: sin base, todo lo
  demás está mal.
- **Pseudonimizar no es anonimizar.** Si guardas `usuario_hash` pero conservas la tabla que
  mapea hash a correo, los datos siguen siendo personales y todas las obligaciones siguen en
  pie. Anonimizar de verdad significa que **nadie** en tu organización puede volver a la
  persona, ni siquiera con la tabla de correspondencia. Un dato anonimizado sale del ámbito del
  reglamento; uno pseudonimizado, no.

Los derechos del interesado son la parte que toca al ingeniero. Los principales: acceso
(saber qué tienes y por qué), rectificación, supresión («derecho al olvido»), limitación,
portabilidad, oposición y no ser objeto de decisiones totalmente automatizadas con efectos
significativos. En la práctica se traducen en tareas concretas: un endpoint que exporte todo
lo de un usuario, un procedimiento que borre de la base de datos **y** del lago **y** de las
copias de seguridad en un plazo razonable, y una forma de saber en qué tablas aparece un
usuario. La respuesta debe darse sin dilación indebida y, en general, dentro de un mes.

:::aviso
«Borrar» en un sistema de datos no es un `DELETE` en la tabla principal. Los datos viven en
réplicas, en el lago, en ficheros Parquet inmutables, en índices de búsqueda y en copias de
seguridad. Si no puedes enumerar dónde está un usuario, no puedes cumplir una supresión, así
que el diseño de linaje ([[catalogo-y-linaje]]) no es burocracia: es lo que hace posible el
borrado.
:::

## Definición formal

En analítica, el mecanismo técnico que más se usa se llama **k-anonimato**. Un conjunto de
datos es `k`-anónimo respecto a un grupo de **cuasi-identificadores** (los campos que, sin ser
el nombre, permiten acotar a quién pertenece una fila: código postal, fecha de nacimiento,
sexo) si cada combinación de valores de esos campos aparece al menos `k` veces.

Formalmente, sea `Q` el conjunto de cuasi-identificadores y `n(q)` el número de filas con la
combinación `q`:

:::formula
k-anonimato ⟺ para todo q, n(q) ≥ k
:::

Símbolos: `q` es una combinación concreta de valores de los cuasi-identificadores (por ejemplo
`CP=28001, nacimiento=1980-03-02`); `n(q)` es cuántas filas comparten esa combinación; `k` es
el umbral mínimo exigido (2, 5, 10, según la sensibilidad).

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `q` | Una combinación concreta de cuasi-identificadores (`CP=28001, nacimiento=1980-03-02`) | valores de esos campos | Cuantos más campos entren en `q`, más estrecho es el grupo y más fácil es incumplir el umbral |
| `n(q)` | Cuántas filas comparten esa combinación | filas | El grupo es más grande y cuesta más señalar a una persona concreta dentro de él |
| `k` | Umbral mínimo de filas por grupo que exige la política | filas | Más privacidad y menos utilidad: hay que generalizar más o suprimir filas, y cada celda publicada mezcla a más gente |
| `Q` | El conjunto de cuasi-identificadores que se eligen, los campos que acotan a quién pertenece la fila | lista de columnas | Cada campo nuevo multiplica las combinaciones posibles y baja `n(q)`; olvidarse del código postal es el fallo típico |
| `1/k` | Probabilidad máxima de señalar a una persona concreta dentro de su grupo | tanto por uno | Con `k = 5` es 0,2; con `k = 1` es 1, y entonces la fila publicada identifica a alguien directamente |
:::

Dentro de un grupo de tamaño `k`, la probabilidad de señalar a una persona concreta es como
mucho `1/k`. Con `k = 1` estás publicando filas que identifican a alguien directamente. Con
`k = 5`, cada fila comparte sus cuasi-identificadores con otras cuatro.

Tres precisiones que evitan malentendidos:

1. El k-anonimato **no basta**. Si todas las filas del grupo tienen la misma enfermedad, saber
   que alguien está en ese grupo ya revela la enfermedad: eso lo cubre la **l-diversidad**
   (que cada grupo tenga al menos `l` valores distintos del atributo sensible).
2. Los cuasi-identificadores **se eligen**, no vienen dados. Elegir mal (olvidar el código
   postal) es el fallo típico.
3. Generalizar (quedarse con los dos primeros dígitos del código postal, o con el año en vez
   del día) reduce la precisión y sube `k`. Todo anonimato es un intercambio entre utilidad y
   privacidad.

## Ejemplo

Cuatro eventos de analítica con el código postal y la fecha de nacimiento exacta:

```
usuario  cp     nacimiento
u1       28001  1980-03-02
u2       28001  1980-03-02
u3       28001  1991-07-15
u4       28013  1975-11-30
```

- Combinaciones distintas de `(cp, nacimiento)`: **3**.
- Grupos con al menos 2 filas: **1** (el de `28001` y `1980-03-02`, que tiene 2 usuarios).
- Filas que quedan en grupos de tamaño 1: **2** (u3 y u4).

Con `k = 2` esos dos registros no se pueden publicar tal cual: cada uno identifica a una sola
persona. La corrección habitual es generalizar. Guardando solo el año en lugar de la fecha
completa, los grupos pasan a ser `(28001, 1980)` con 2 filas, `(28001, 1991)` con 1 y
`(28013, 1975)` con 1: **no se ha arreglado ninguno de los dos**, porque u3 y u4 siguen siendo
los únicos de su combinación (lo único que ha cambiado es la etiqueta del grupo). El
k-anonimato no se consigue apretando un botón; hay que iterar sobre qué campos se generalizan y
cuánto: subir del día al año no bastó aquí, y el siguiente paso sería quedarse con la provincia
o con un tramo de edad.

:::figura
fichero: privacidad-k-anonimato
pie: A la izquierda, los cuatro usuarios del ejemplo agrupados por (código postal, nacimiento): los grupos tienen 2, 1 y 1 filas, y generalizar la fecha al año los deja igual de pequeños, con dos personas solas en su combinación. A la derecha, las tres salidas posibles con k = 2 y lo que cuesta cada una: publicar tal cual deja k = 1 y esas dos personas quedan identificadas; suprimir las dos filas únicas cumple k = 2 publicando la mitad de los datos; y agregarlo todo cumple de sobra, pero deja una sola fila con la que ya no se aprende nada. El k-anonimato no se consigue apretando un botón: se elige qué se sacrifica.
fuente: figuras/privacidad-y-gdpr-1.py
:::

## Código

```python verificable
import pandas as pd

# Cada fila es un usuario identificable por codigo postal y fecha de nacimiento exacta.
eventos = pd.DataFrame({
    "usuario":    ["u1", "u2", "u3", "u4"],
    "cp":         ["28001", "28001", "28001", "28013"],
    "nacimiento": ["1980-03-02", "1980-03-02", "1991-07-15", "1975-11-30"],
})

# k-anonimato: cada combinacion de cuasi-identificadores debe aparecer al menos k veces.
conteo = eventos.groupby(["cp", "nacimiento"]).size()   # Serie con los grupos como indice
k = 2
print("combinaciones distintas:", len(conteo))          # len cuenta grupos, no filas
print("grupos con al menos", k, "filas:", int((conteo >= k).sum()), "de", len(conteo))   # True vale 1
print("filas en grupos pequenos:", int(eventos.shape[0] - conteo[conteo >= k].sum()))

# Generalizar la fecha al ano sube el tamano de los grupos.
generalizado = eventos.assign(anio=eventos.nacimiento.str.slice(0, 4))   # copia: no toca eventos
print("grupos por (cp, anio):", generalizado.groupby(["cp", "anio"]).size().to_dict())
```

:::claves
- `.groupby([...]).size()` devuelve una **Series**, no un DataFrame: el índice son los grupos (aquí un `MultiIndex` de dos niveles) y el valor, cuántas filas tiene cada uno. No hay ninguna columna de conteo que puedas ordenar.
- `len(conteo)` cuenta **grupos**, no filas: con cuatro usuarios repartidos en tres combinaciones distintas devuelve 3.
- `conteo >= k` es una Series de booleanos y `.sum()` la suma como 1 y 0, así que cuenta los grupos que cumplen. `conteo[conteo >= k].sum()` da las filas de esos grupos y la resta con `eventos.shape[0]` deja las que están en grupos pequeños. El `int(...)` de esas líneas solo convierte el entero de NumPy en un `int` de Python para no arrastrar su tipo.
- `.assign(anio=...)` devuelve un **DataFrame nuevo** con la columna añadida; `eventos` se queda con sus tres columnas. Para modificar el original hay que asignar: `eventos["anio"] = ...`.
- `.str.slice(0, 4)` solo existe en columnas de texto y corta por caracteres: de `"1980-03-02"` saca `"1980"`. Con una columna de tipo fecha (`datetime64`) no hay `.str` y se usa `.dt.year`.
- `.size().to_dict()` con dos claves de agrupación produce claves **tupla**, `("28001", "1980")`, no cadenas: al buscar un grupo hay que pasar la tupla entera.
:::

```sql verificable
CREATE TABLE eventos (id INTEGER, usuario VARCHAR, tipo VARCHAR, fecha DATE);

INSERT INTO eventos VALUES
  (1, 'u1', 'visita', DATE '2024-01-10'),
  (2, 'u1', 'compra', DATE '2024-02-02'),
  (3, 'u2', 'compra', DATE '2026-01-05');

-- Politica de retencion: los eventos de analitica se borran a los 24 meses.
DELETE FROM eventos WHERE fecha < DATE '2026-01-01';

SELECT usuario, count(*) AS eventos_conservados FROM eventos GROUP BY usuario ORDER BY usuario;
```

```text
usuario  eventos_conservados
u2       1
```

## Errores típicos

- **Recoger todo «por si acaso».** Guardar el `user_agent` completo, la IP sin truncar y la
  ciudad «por si algún día hacen falta» multiplica el riesgo y las obligaciones sin aportar
  nada hoy. Minimiza: cada campo tiene que tener una finalidad escrita.
- **Llamar anónimo a lo pseudónimo.** Un `hash` del correo con la tabla de correspondencia
  guardada en otro sitio sigue siendo dato personal. Y un `hash` sin sal de un dato con pocas
  combinaciones (un teléfono, un DNI) se revierte con una tabla precalculada en segundos.
- **Confundir consentimiento con base legal universal.** Para ejecutar un contrato no necesitas
  consentimiento; para analítica de interés legítimo, a veces tampoco. Pedir consentimiento
  cuando no hace falta es tan mala práctica como no pedirlo cuando hace falta, porque lo
  desvirtúa y genera registros que no puedes defender.
- **No tener retención definida.** «Lo guardamos todo indefinidamente» es el estado por
  defecto de casi todos los lagos de datos y es indefendible: significa que tienes datos
  personales cuyo fin ya se cumplió. Define plazos por tabla y automatiza el borrado.
- **Olvidar las copias de seguridad y los terceros.** La supresión debe alcanzar los *backups*
  (con el enfoque de restaurar, borrar y volver a respaldar, o dejando que caduquen) y a los
  proveedores que reciben los datos. Sin un contrato de encargado del tratamiento, esa cesión
  es irregular.
- **Publicar tablas «agregadas» que en realidad no lo están.** Una tabla con conteos por
  código postal y edad, con celdas de valor 1, es un listado de personas con nombre y
  apellidos cambiados por coordenadas. Aplica `k` antes de publicar, no después de la queja.

:::trampa
Guardar el identificador de publicidad del móvil «porque lo da el sistema» es guardar un dato
personal con el que se te puede rastrear entre aplicaciones, y en muchos casos exige
consentimiento previo del sistema operativo. Lo mismo con la IP: se considera dato personal, y
truncarla (quedarse con los tres primeros octetos) o dejar de guardarla es una decisión que hay
que tomar a propósito, no por omisión.
:::

## Comprueba que lo sabes

:::quiz
p: Guardas un hash del correo de cada usuario y la tabla que relaciona hash y correo en otra base de datos. ¿Son datos personales?
o: No, porque lo que circula por el sistema es un hash irreversible
o: Sí, porque mientras alguien pueda volver al correo con la tabla de correspondencia, los datos son personales
o: Solo si el hash tiene menos de 256 bits
a: 2
e: La pseudonimización reduce el riesgo pero no saca los datos del ámbito del reglamento: siguen siendo personales y hay que atender acceso, supresión y retención. Solo la anonimización real (imposible de revertir por nadie) los excluye, y el tamaño del hash es irrelevante para esa distinción.
:::

:::quiz
p: Publicas una tabla de altas por código postal y año de nacimiento, y una celda tiene valor 1. ¿Cuál es el problema?
o: Ninguno: la tabla solo tiene conteos, y un conteo no es un dato personal
o: Que ese registro no es k-anónimo: quien conozca unos pocos datos de esa persona puede deducir que se dio de alta
o: Que los conteos con valor 1 suelen ser errores de datos y hay que borrarlos
a: 2
e: Los cuasi-identificadores son precisamente los que permiten acotar hasta una sola persona, y un grupo de tamaño 1 equivale a publicar la fila original. Se corrige generalizando (quedarse con el año, agrupar códigos postales) hasta que cada celda agrupe al menos k personas.
:::

:::quiz
p: Un usuario pide que borres sus datos. ¿Basta con borrar su fila en la tabla de usuarios?
o: Sí, con eso desaparece del sistema
o: No: hay que borrar o anonimizar también sus datos en el lago, los índices y las copias de seguridad
o: Solo si el usuario no ha comprado nada en los últimos doce meses
a: 2
e: Un mismo usuario aparece en muchas tablas, ficheros y sistemas, y la supresión debe alcanzarlos todos (a las copias de seguridad se les aplica la política de caducidad o un reproceso controlado). Sin linaje y sin un mapa de dónde vive cada dato, la supresión se queda a medias, y eso es un incumplimiento.
:::
