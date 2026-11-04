---
id: code-review
titulo: Revisión de código
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [testing-piramide, git-avanzado]
tags: [revision, equipo, calidad, automatizacion]
resumen: Que mirar en una revisión, cómo comentar para que el cambio se haga y qué conviene delegar en la máquina antes de que un humano abra el diff.
fuentes: ["Fagan (1976), 'Design and code inspections to reduce errors in program development'", "Bacchelli y Bird (2013), 'Expectations, outcomes, and challenges of modern code review'", "McConnell (2004), 'Code Complete', 2.ª ed."]
---

## En una frase

La revisión de código es una conversación sobre un cambio concreto, con dos objetivos a la vez
—detectar lo que la máquina no puede detectar y repartir el conocimiento del código— y funciona
solo si el cambio es lo bastante pequeño para leerse entero.

## La idea

Antes de levantar un edificio se revisa el plano: es barato cambiar un muro de sitio sobre el
papel. Cuando la obra está hecha, mover ese muro cuesta cien veces más. La revisión de código
está en ese momento: el cambio existe, funciona y todavía es barato rehacerlo.

Conviene tener claro **qué no es** una revisión, porque es donde se va el tiempo:

- No es un linter. El formato, los imports sin usar, la longitud de línea o un tipo mal declarado
  los tiene que cazar la máquina en [[ci-cd|la integración continua]], antes de que nadie mire.
  Si gastas el ojo humano en eso, no te queda para lo demás.
- No es una prueba de inteligencia ni un examen del autor. Un comentario que empieza por «esto
  está mal porque…» y explica el porqué enseña; uno que dice «esto no me gusta» solo frena.
- No es el sitio para rediseñar el sistema. Si el cambio revela un problema de arquitectura, la
  conversación es otra y con más gente; en la revisión se decide si *este* cambio entra.

Lo que sí aporta una revisión, y ninguna herramienta automática da:

1. **Intención frente a implementación.** El código hace lo que el autor quiso, pero ¿era eso lo
   que hacía falta? El caso que falta, la condición de negocio que nadie escribió, el flujo de
   error que no se contempló.
2. **Nombres y modelo mental.** Una función llamada `procesar` que en realidad valida y guarda
   es una trampa para el siguiente que la lea.
3. **Acoplamiento y efectos colaterales.** Este cambio toca una tabla compartida por otros tres
   servicios; esta consulta se ejecuta dentro de un bucle; este campo se registra en un log y
   contiene un dato personal.
4. **Conocimiento del sistema.** Quien revisa aprende cómo está hecho; quien escribió recibe
   contexto que no tenía. Es el mecanismo más barato de formación que existe en un equipo.
5. **Convenciones.** Las decisiones pequeñas —cómo se manejan los errores, qué se registra— se
   acuerdan aquí, no en un documento que nadie lee.

Y una regla de tamaño: un cambio de más de cuatrocientas líneas no se revisa de verdad, se
aprueba. Cuando el diff es enorme, la atención se agota en las primeras pantallas y el resto pasa
con un «lo veo bien». Divide el cambio en trozos que se puedan leer de una sentada, cada uno con
su propósito.

## Definición formal

- **Inspección formal (Fagan, 1976).** Proceso con roles definidos —autor, moderador, lector,
  inspectores, escriba—, una lista de comprobación, una reunión y un seguimiento de los defectos.
  Su versión moderna y ligera es la revisión asíncrona en la herramienta, sin reunión y con pocos
  revisores.
- **Unidad de revisión.** El diff: un conjunto de cambios con un propósito declarado. Un diff con
  dos propósitos es dos revisiones, y se rechaza aunque los dos sean correctos.
- **Cambio mínimo coherente.** El diff más pequeño que consigue el propósito. Cada línea de más
  es una línea que hay que entender y que puede esconder un fallo.
- **Criterios de aceptación de una revisión.** Cuatro preguntas, en este orden:
  1. ¿Hace lo que dice que hace, y lo dice bien en la descripción?
  2. ¿Está probado de forma que un cambio futuro lo detecte, en el nivel de
     [[testing-piramide|la pirámide]] que le corresponde?
  3. ¿Es el cambio mínimo, o lleva dentro reformas que nadie pidió?
  4. ¿Lo entenderá alguien dentro de seis meses sin preguntarte?
- **Severidades de un comentario.** *Bloqueante* (no se integra hasta resolverse), *sugerencia*
  (mejoraría, decide el autor), *pregunta* (no entiendo esto, explícamelo) y *elogio* (esto está
  bien resuelto, y decirlo también es parte del trabajo). Marcar la severidad evita que una
  preferencia de estilo parezca un veto.
- **Métricas honestas.** Tamaño del diff en líneas, tiempo hasta la primera respuesta y tiempo
  hasta la integración. El número de comentarios no mide calidad: una revisión con veinte
  comentarios de formato es peor que una con dos de fondo.

## Ejemplo

Un cambio que toca tres ficheros: 320 líneas en el módulo de pagos, 140 en sus pruebas y 12 en el
registro de cambios. Total, 472 líneas. Con un límite de 400, ese cambio no debería pedirse como
una sola revisión: el bloque de pagos se separa (por ejemplo, extraer primero la función de
redondeo con sus pruebas, y después el cambio de comportamiento).

El límite no es un capricho administrativo: es dónde se agota la atención de quien revisa. Con
472 líneas, las 12 últimas del registro de cambios quedan fuera de lo que alguien va a mirar de
verdad.

:::figura
fichero: code-review-tamano-del-diff
pie: Izquierda, la composición del diff: 320 líneas de `src/pagos.py`, 140 de sus pruebas y 12 del registro de cambios, con el límite de 400 marcado en rojo. Todo lo que pasa de esa raya se aprueba sin leer. Derecha, las tres formas de pedir lo mismo: de una vez (472 líneas, por encima del límite), partido en dos y partido en tres, donde ningún trozo llega a 400. Partir el cambio no es burocracia: es lo que hace que la revisión ocurra.
fuente: figuras/code-review-1.py
:::

Y el otro ejemplo: un fragmento que llega a revisión con dos defectos clásicos que la máquina
debería haber marcado antes —un argumento por defecto mutable en la línea 2 y un `except` sin
tipo en la línea 9—. Cuando el CI avisa de eso, quien revisa puede dedicar su atención a la
pregunta que de verdad importa: «¿qué pasa aquí si el fichero no existe, y por qué se devuelve
`None` en vez de propagar el error?».

## Código

```python verificable
import ast

# Lo que la maquina puede cazar sola: asi el ojo humano se gasta en otra cosa.
# El codigo a revisar va como texto dentro de la cadena: no se ejecuta, solo se analiza.
CODIGO = '''
def anade(item, lista=[]):
    lista.append(item)
    return lista

def lee(ruta):
    try:
        return open(ruta).read()
    except:
        return None
'''

def avisos(fuente):
    encontrados = []
    # ast.parse construye el arbol de sintaxis; walk lo recorre entero, en cualquier orden.
    for nodo in ast.walk(ast.parse(fuente)):
        if isinstance(nodo, ast.FunctionDef):
            # args.defaults son solo los valores por defecto de los parametros.
            for defecto in nodo.args.defaults:
                # List, Dict y Set se crean UNA vez, al definir la funcion, y se comparten.
                if isinstance(defecto, (ast.List, ast.Dict, ast.Set)):
                    encontrados.append(f"linea {nodo.lineno}: argumento por defecto mutable en {nodo.name}")
        # Un except sin tipo es ExceptHandler con type None: se traga cualquier error.
        if isinstance(nodo, ast.ExceptHandler) and nodo.type is None:
            encontrados.append(f"linea {nodo.lineno}: except sin tipo de excepcion")
    return encontrados

for aviso in avisos(CODIGO):
    print(aviso)
# Se vuelve a analizar la cadena entera: la funcion no guarda nada entre llamadas.
print("avisos:", len(avisos(CODIGO)))     # -> 2
```

:::claves
- `ast.parse` **no ejecuta nada**: convierte texto en un árbol. Ese código con `lista=[]` y
  `except:` nunca se llama, y aun así el análisis encuentra los dos defectos.
- `ast.walk` recorre todos los nodos sin importar el orden, así que los avisos salen en orden
  de aparición en el árbol, no en el orden en que los escribirías tú a mano.
- El defecto del argumento mutable no es que la lista esté vacía, es que **se crea una sola
  vez**, al definir la función, y se comparte entre todas las llamadas: la segunda llamada
  recibe lo que dejó la primera.
- `nodo.args.defaults` son solo los valores por defecto de los últimos parámetros, y
  `nodo.args.kw_defaults` los de los que van detrás de un `*`. Si miras solo `defaults`, un
  `def f(*, lista=[])` se te escapa.
- Un `except:` sin tipo es `ExceptHandler` con `type is None`; captura también `KeyboardInterrupt`
  y los errores de programación, así que el `return None` de arriba convierte un fallo en un
  valor válido y nadie se entera.
- `len(avisos(CODIGO))` vuelve a analizar la cadena entera: nada se guarda en caché entre
  llamadas. Aquí da igual porque son cuatro líneas, pero con un proyecto real se analiza una
  vez y se reutiliza el árbol.
:::

```python verificable
# Medir el diff antes de pedir revision: un cambio enorme no se lee, se aprueba.
diffs = {"src/pagos.py": 320, "tests/test_pagos.py": 140, "CHANGELOG.md": 12}
LIMITE = 400                    # en mayusculas por convencion: es una constante, no un dato

total = sum(diffs.values())     # values(), no el diccionario: sumar las claves daria un error
for fichero, lineas in diffs.items():
    print(f"{fichero:<22} {lineas:>4} lineas")

print("lineas cambiadas:", total)                 # -> 472
print("dentro del limite:", total <= LIMITE)      # -> False
# max con key: compara por el valor (las lineas) y devuelve la clave (el nombre del fichero).
print("mayor bloque:", max(diffs, key=diffs.get)) # -> src/pagos.py
```

```text
Un comentario util tiene tres partes: que, por que y que hacer.

Mal:   "Esto no me gusta."
Bien:  "Aqui se devuelve None si el fichero no existe (que). El que llama no
        distingue ese caso de un fichero vacio (por que). Propongo lanzar
        FileNotFoundError y dejar que la capa de arriba decida (que hacer)."
```

## Errores típicos

- **Revisar el estilo a mano.** Discutir comillas, sangría o longitud de línea en un comentario
  es gastar el recurso caro en lo barato. Eso lo resuelve un formateador automático una vez, y
  nadie vuelve a hablar del tema.
- **Aprobar un diff de mil líneas sin leerlo.** El «lo veo bien» en un cambio enorme es una
  aprobación sin revisión, y suele ser donde se cuelan los fallos. Si el autor no puede partirlo,
  ayúdale a partirlo: es parte del trabajo de revisar.
- **Comentar solo lo que está mal.** Una revisión que nunca dice «esto está bien» enseña a la
  gente a temerla. Señalar una buena decisión —una prueba que cubre el caso raro, un nombre que
  aclara el dominio— fija esa práctica en el equipo.
- **Confundir preferencia con defecto.** «Yo lo habría hecho con un `for`» no es un fallo. Marca
  la severidad: si es una sugerencia, dilo, y deja que el autor decida sin sentirse bloqueado.
- **Dejar la revisión parada dos días.** El coste de una revisión no es el tiempo de quien la
  hace, es el tiempo que el autor espera con el trabajo a medias y el conflicto que se acumula en
  su rama. Responde pronto, aunque sea para decir «hoy no puedo».
- **Pedir cambios que nadie ha pedido.** Aprovechar la revisión para renombrar medio módulo o
  reformatear ficheros enteros mezcla el propósito real con ruido: el diff deja de ser legible y
  el `git bisect` futuro señala un commit que cambió 4.000 líneas. Las reformas van en su propia
  revisión.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál de estas cosas NO debería ocupar el tiempo de una revisión humana?
o: Detectar que falta el caso en el que el pago se queda a medias
o: Señalar que una línea tiene 92 caracteres y comillas dobles en vez de simples
o: Preguntar por qué una consulta se ejecuta dentro de un bucle
a: 2
e: El formato y el estilo los comprueba un formateador en el CI, de forma automática y sin discusión. Lo que solo ve una persona es el caso que falta, la intención que no coincide con la implementación y los efectos colaterales como la consulta dentro del bucle.
:::

:::quiz
p: Llega un diff de 900 líneas que toca la lógica de facturación, sus pruebas y tres ficheros de configuración. ¿Qué es lo más útil que puedes hacer?
o: Aprobarlo para no bloquear al autor, que ya lo ha probado
o: Pedir que se separe en cambios con un propósito cada uno, y revisar el primero
o: Revisarlo entero de una vez, aunque tardes tres horas
a: 2
e: Un diff de ese tamaño no se revisa de verdad: la atención se agota y el final se aprueba por cansancio. Partirlo reduce el riesgo, hace la revisión posible y deja un historial donde el `git bisect` y el `revert` sirven para algo.
:::

:::quiz
p: Un compañero comenta «yo esto lo haría con un `for` en vez de un generador». ¿Cómo se interpreta?
o: Es un bloqueo: hay que reescribirlo antes de integrar
o: Es una sugerencia de estilo: el autor decide, y conviene que el comentario diga que no es bloqueante
o: Es una petición del responsable técnico y hay que obedecerla
a: 2
e: Sin marcar la severidad, cualquier comentario parece un veto y la revisión se convierte en una negociación desgastante. Distinguir bloqueante, sugerencia, pregunta y elogio es lo que permite discutir el fondo sin frenar cambios correctos.
:::
