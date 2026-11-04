---
id: gobierno-y-privacidad
titulo: Gobierno y privacidad del dato
fase: 4
nivel: avanzado
rutas: [de, ds]
prerequisitos: [calidad-de-datos, catalogo-y-linaje, ciclo-de-vida-del-dato]
tags: [gobierno, privacidad, rgpd, linaje]
resumen: Quien responde de cada dato, cuánto tiempo se guarda, con qué base jurídica y cómo se borra: gobierno y privacidad son diseño, no un trámite final.
fuentes: ["Parlamento Europeo y Consejo (2016), 'Reglamento (UE) 2016/679 (RGPD)'", "Sweeney (2002), 'k-anonymity: a model for protecting privacy'"]
---

## En una frase

Gobernar el dato es saber en todo momento quién responde de él, para qué se puede usar, cuánto
tiempo se conserva y cómo se borra cuando toca; la privacidad no es quitar el nombre de una
columna, es impedir que alguien pueda volver a identificar a una persona cruzando datos.

## La idea

Piensa en un hospital. Cada historia clínica tiene un **responsable** (el servicio que la
mantiene), una **finalidad** (diagnóstico, no publicidad), un **plazo de conservación** (cinco
años, no para siempre), un **registro de accesos** (quién la ha mirado y cuándo) y un
procedimiento de **rectificación y borrado** cuando el paciente lo pide o cuando la ley lo
exige. Nada de eso funciona si se decide al final: son decisiones de diseño que se toman antes
de guardar el primer registro.

En datos pasa exactamente igual, y hay cinco preguntas que un sistema de datos serio debe poder
responder sin abrir un Excel:

1. **¿De quién es este dato?** Un equipo con nombre y apellidos profesionales, no «el área de
   datos». Sin dueño no hay quien corrija ni quien decida.
2. **¿Para qué se puede usar?** La finalidad. Un dato recogido para gestionar un pedido no se
   puede usar para perfilado publicitario sin una base jurídica distinta.
3. **¿Cuánto tiempo se guarda?** El plazo, con una fecha concreta y una tarea que lo ejecute.
   «Indefinidamente por si acaso» es una infracción, no prudencia.
4. **¿Quién lo ha visto y por dónde ha pasado?** Trazabilidad y linaje
   ([[catalogo-y-linaje|catálogo y linaje]]).
5. **¿Cómo se borra?** Y aquí está la pregunta que rompe arquitecturas: un lago de datos
   inmutable y un borrado a petición parecen incompatibles, y hay que resolverlo **antes** de
   montarlo.

La distinción que casi todo el mundo confunde y que hay que grabar a fuego:

- **Seudonimizar** es cambiar el nombre por un alias, guardando aparte la tabla que permite
  volver al original. Los datos siguen siendo **personales** y les aplica la normativa entera.
  Es una medida de seguridad, no una excusa.
- **Anonimizar** es hacer **irreversible** la reidentificación, incluso cruzando con otras
  fuentes y con medios razonables. Solo entonces el dato sale del ámbito de la protección de
  datos. La palabra clave es «irreversible», y demostrarlo es mucho más difícil de lo que
  parece.

Y el enemigo real no es el nombre en una columna: son los **cuasi-identificadores**. El código
postal, la fecha de nacimiento exacta, el sexo, el centro de trabajo. Por separado no
identifican a nadie; combinados, identifican a casi todo el mundo, porque hay muchos menos
registros que combinaciones posibles. Ese es el hallazgo que sostiene todo el campo: en una
población, la mayoría de las combinaciones de (código postal, fecha de nacimiento, sexo) son
únicas.

## Definición formal

- **Dato personal:** toda información sobre una persona física identificada o identificable. Es
  identificable si se puede llegar a ella por un identificador directo (nombre, DNI, correo) o
  por una combinación de cuasi-identificadores.
- **Seudonimización:** sustitución de identificadores directos por alias, conservando la
  correspondencia `alias → identidad`. El dato sigue siendo personal.
- **Anonimización:** transformación irreversible que impide la reidentificación. El resultado no
  es un dato personal.
- **k-anonimato:** una tabla liberada cumple k-anonimato si, para cada combinación de
  cuasi-identificadores presente, hay **al menos `k`** registros. Con `k = 1` cada fila es única
  y se puede enlazar; con `k = 3`, quien mire una fila sabe que es una de tres personas.
- **l-diversidad:** además de agrupar en `k`, el atributo sensible (diagnóstico, salario) debe
  tener al menos `l` valores distintos dentro de cada grupo; si no, todos comparten el mismo
  secreto y el grupo no protege nada.
- **Retención:** plazo máximo de conservación por categoría de dato, con la acción asociada
  (borrar, anonimizar o archivar) y su ejecución automática.
- **Crypto-shredding:** cifrar los datos personales con una clave por sujeto y destruir esa
  clave para «borrar» sin tocar el histórico. El borrado real se convierte en la destrucción de
  un secreto.

:::formula
k-anonimato: min sobre cada combinación de cuasi-identificadores del nº de filas ≥ k
reidentificación: nº de registros ÷ nº de combinaciones únicas de cuasi-identificadores
:::

## Ejemplo

Ocho registros extraídos de una base de clientes «anonimizada»: solo llevan un identificador
interno, el código postal, la edad y el sexo. Al lado, un censo público del mismo municipio con
los mismos tres campos y los nombres.

- Cruzando por (código postal, edad, sexo), los **8 de 8** registros tienen **un único candidato**
  posible. La tabla, que no contiene ni un solo nombre, está completamente reidentificada.
- El k-anonimato de esas combinaciones es **1**: cada grupo tiene una sola fila.
- Generalizando a provincia y sexo se llega a **k = 3**, que es un valor aceptable, pero el precio
  es que se ha destruido la edad y la localidad: ya no puedes analizar por barrio ni por franja
  de edad. Ese es el compromiso real entre privacidad y utilidad, y no se puede evitar: se elige.

El segundo ejemplo es el de la seudonimización con hash. Un identificador de cinco dígitos tiene
**90.000 valores posibles**: se prueban todos en una fracción de segundo y el hash sin sal se
revierte por fuerza bruta. Con una **sal secreta**, el mismo valor produce otro hash y la
enumeración ya no sirve... siempre que la sal no esté guardada junto a los datos, en cuyo caso
has vuelto al punto de partida con un paso extra.

## Código

```python verificable
import pandas as pd

# Dataset "anonimizado": sin nombre, pero con cuasi-identificadores.
anonimo = pd.DataFrame({
    "id":   range(1, 9),
    "cp":   ["28001", "28001", "28001", "28013", "28013", "28013", "28040", "28040"],
    "edad": [34, 41, 29, 35, 52, 47, 61, 34],
    "sexo": ["M", "M", "F", "F", "F", "M", "F", "F"],
})

# Un censo publico del mismo municipio con los mismos tres campos.
censo = pd.DataFrame({
    "cp": anonimo["cp"], "edad": anonimo["edad"], "sexo": anonimo["sexo"],
    "nombre": ["Ana", "Luis", "Marta", "Pablo", "Sara", "Hugo", "Elena", "Nuria"],
})

unido = anonimo.merge(censo, on=["cp", "edad", "sexo"], how="left")
candidatos = unido.groupby("id")["nombre"].nunique()
print("registros con un unico candidato:", int((candidatos == 1).sum()), "de", len(candidatos))  # -> registros con un unico candidato: 8 de 8

# k-anonimato: tamano del grupo mas pequeno de cada combinacion de cuasi-identificadores.
grupos = anonimo.groupby(["cp", "edad", "sexo"]).size()
print("k sin generalizar:", int(grupos.min()))    # -> k sin generalizar: 1

# Generalizando a provincia y sexo se llega a k=3, a costa de perder edad y localidad.
grupos2 = anonimo.assign(prov=anonimo["cp"].str[:2]).groupby(["prov", "sexo"]).size()
print("k por provincia y sexo:", int(grupos2.min()))    # -> k por provincia y sexo: 3
```

```python verificable
import hashlib

def pseudo(valor, sal=""):
    # Un hash truncado a 12 caracteres basta como alias, pero no protege nada por si solo.
    return hashlib.sha256((sal + valor).encode()).hexdigest()[:12]

# Un identificador de 5 digitos tiene 90.000 valores: se enumeran todos.
objetivo = pseudo("34521")
recuperado = next(v for v in range(10_000, 100_000) if pseudo(str(v)) == objetivo)
print("recuperado del hash sin sal:", recuperado)     # -> recuperado del hash sin sal: 34521

# Con sal secreta el mismo valor produce otro hash, y la sal no puede vivir con los datos.
print("mismo valor con sal:", pseudo("34521", sal="s3cr3t0-a1"))   # -> mismo valor con sal: 72ceabaf4ad3
```

## Errores típicos

- **Creer que quitar el nombre es anonimizar.** Con cuasi-identificadores, ocho registros sin
  nombre se reidentifican al 100 % con un censo público. Antes de publicar, mide el
  k-anonimato de las combinaciones que liberas.
- **Hashear sin sal valores de baja entropía.** Un DNI, un teléfono o una fecha de nacimiento se
  enumeran en segundos. El hash sin sal no es anonimización: es un alias determinista que
  además facilita agrupar a la misma persona entre tablas.
- **Guardar la sal (o la tabla de correspondencias) junto a los datos seudonimizados.** Si el
  alias y la clave para deshacerlo viven en el mismo sistema y con los mismos permisos, la
  seudonimización solo aporta trabajo.
- **Replicar PII en el entorno de analítica «porque hace falta para el join».** Casi siempre se
  puede unir por un alias con la tabla de identidad en un sistema aparte y con permisos
  distintos. Cada copia de PII multiplica los sitios donde hay que borrar y donde hay que
  auditar.
- **Confundir retención con prudencia.** «No borres nada por si acaso» es conservar datos
  personales más tiempo del necesario, y eso es precisamente lo contrario de lo que pide la
  normativa. Define el plazo por categoría y automatiza la acción.
- **Descubrir el conflicto entre lago inmutable y derecho de supresión después de montarlo.** Un
  lago append-only sin borrado por clave ni crypto-shredding no puede cumplir una supresión
  individual sin reescribir el histórico entero. Decide la estrategia antes: borrado por clave
  en el formato de tabla ([[lakehouse-y-table-formats|Delta, Iceberg o Hudi]]) o cifrado por
  sujeto con destrucción de clave.

## Comprueba que lo sabes

:::quiz
p: Publicas una tabla sin nombres, con código postal, edad y sexo. ¿Es anónima?
o: Sí, porque no contiene ningún identificador directo
o: No necesariamente: si esas combinaciones son únicas en la población, cualquiera puede reidentificar cruzando con un censo público
o: Sí, siempre que el código postal tenga más de cinco dígitos
a: 2
e: La anonimización depende de la irreversibilidad, no de la ausencia de nombres. Los cuasi-identificadores combinados identifican a mucha gente porque hay muchas más combinaciones posibles que personas en una zona concreta. Se mide con k-anonimato y l-diversidad.
:::

:::quiz
p: Sustituyes el DNI de tus clientes por el SHA-256 del DNI y publicas la tabla. ¿Qué has conseguido?
o: Anonimizar los datos, porque un hash no se puede revertir
o: Solo seudonimizar con un alias determinista; como el espacio de DNIs es pequeño, se enumera y se recupera el valor original
o: Nada en absoluto, porque el hash siempre se puede invertir matemáticamente
a: 2
e: Un hash no es reversible matemáticamente, pero sí enumerable cuando el conjunto de entradas posibles es pequeño: los DNIs, teléfonos y fechas de nacimiento se prueban en segundos. Con sal secreta y bien custodiada mejora la situación, pero el dato sigue siendo personal.
:::

:::aviso
Todo esto es orientación técnica, no asesoramiento jurídico: la base jurídica concreta, los
plazos y los procedimientos dependen de la normativa aplicable y de cada organización. Lo que sí
es responsabilidad de ingeniería es **poder demostrar** qué datos tienes, de dónde vinieron,
quién los ha visto y qué se ha borrado. Si eso requiere tres semanas de trabajo manual, no
tienes gobierno del dato: tienes documentación desactualizada.
:::
