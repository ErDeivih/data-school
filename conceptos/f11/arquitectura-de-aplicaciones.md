---
id: arquitectura-de-aplicaciones
titulo: "Arquitectura de aplicaciones: capas, límites y dependencias"
fase: 11
nivel: intermedio
rutas: [alg]
prerequisitos: [principios-solid, patrones-de-diseno, sistemas-distribuidos-bases, testing-piramide]
tags: [arquitectura, capas, dependencias, diseno]
resumen: Qué puede importar a qué: la regla que evita que un cambio en la base de datos obligue a tocar la interfaz, y cómo se comprueba sin discusión.
fuentes: ["Martin (2017), 'Clean Architecture: A Craftsman's Guide to Software Structure and Design'", "Evans (2003), 'Domain-Driven Design: Tackling Complexity in the Heart of Software'", "Parnas (1972), 'On the Criteria To Be Used in Decomposing Systems into Modules'"]
---

## En una frase

La arquitectura de una aplicación es la lista de quién puede depender de quién, y casi todo lo
demás —capas, puertos, adaptadores— es una forma de que esa lista se pueda cumplir y se pueda
comprobar.

## La idea

Un programa que funciona tiene cero dependencias mal puestas por definición: funciona. El problema
aparece al cambiarlo. Si para leer un dato desde la interfaz llamas directamente al driver de la
base de datos, cualquier cambio de esquema te obliga a tocar la interfaz, y cualquier prueba de la
interfaz necesita una base de datos. El código compila, los tests tardan, y el siguiente que
llegue no sabe qué puede romper.

La arquitectura responde a una sola pregunta: **¿qué puede importar a qué?**. Las capas son la
forma más común de responderla, y la versión útil no es «presentación, negocio, datos», sino la
dirección de las flechas:

- El **dominio** es el corazón: reglas del negocio, entidades y casos de uso. No importa nada de
  la aplicación. Ni el framework web, ni el ORM, ni el cliente de la cola.
- Los **adaptadores** son los que hablan con el mundo: la base de datos, la API de pagos, el
  sistema de ficheros. Dependen del dominio, porque implementan interfaces que el dominio declara.
- La **composición** es donde se juntan: un único sitio que construye los objetos reales y los
  inyecta. Es el único punto que conoce a la vez el dominio y los adaptadores.

La clave es que la flecha de dependencia **apunta hacia dentro**: el adaptador conoce el dominio,
el dominio no conoce el adaptador. Eso se consigue con inversión de dependencias: el dominio
declara una interfaz (`Protocol` en Python, `interface` en otros lenguajes) y el adaptador la
implementa. Es [[principios-solid|el principio de inversión de dependencias]] aplicado a módulos
enteros en vez de a clases.

:::trampa
«Capas» no significa «carpetas». Un proyecto con `models/`, `services/` y `repositories/` puede
tener el dominio importando el ORM en la primera línea de `models/`, y entonces no hay capas: hay
tres carpetas con nombres de capa. Lo que define la capa es la dirección de los `import`, y eso se
comprueba con una herramienta, no con una convención escrita en el README.
:::

Los **límites** son la otra mitad. Un límite es una frontera donde el formato de los datos cambia:
fuera hablas con JSON y códigos HTTP, dentro hablas con tus entidades. Si no hay traducción en la
frontera, el JSON del proveedor de pagos acaba siendo el argumento de tus funciones de negocio, y
cambiarlo es tocar cuarenta ficheros. El límite se paga en una capa de mapeo y se cobra en que el
resto del sistema no sabe qué proveedor hay detrás.

La prueba de fuego de un límite bien puesto es sencilla: ¿puedes cambiar la implementación por
otra en los tests, sin arrancar la base de datos? Si para probar el caso de uso necesitas
PostgreSQL en marcha, el límite no existe. Y hay una consecuencia práctica que aparece en los
tests de integración: si el dominio no depende de nada, sus pruebas corren en milisegundos, y las
que sí necesitan infraestructura se quedan en las capas de arriba, que son las menos.

## Definición formal

Un sistema con `n` módulos es un grafo dirigido de dependencias. Con `M` el conjunto de módulos y
`D` el conjunto de pares ordenados, el principio de arquitectura en capas se escribe así:

:::formula
para todo (a, b) en D:  nivel(a) > nivel(b)        y        D no contiene ciclos
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `M` | Conjunto de módulos del sistema | módulos | Más piezas que entender; por encima de unas decenas, los límites hay que declararlos explícitamente o se difuminan |
| `D` | Conjunto de dependencias: pares (a, b) donde a importa a b | pares | Más acoplamiento: cada arista es un motivo por el que un cambio en b obliga a revisar a |
| `nivel(m)` | Altura del módulo en la jerarquía de capas | entero | Un módulo de nivel alto puede usar los de nivel bajo; al revés se rompe la regla |
| `fan_in(m)` | Cuántos módulos dependen de m | módulos | Un fan-in alto significa que m es interfaz pública de facto: cambiarlo rompe a muchos |
| `fan_out(m)` | De cuántos módulos depende m | módulos | Un fan-out alto significa que m hace demasiadas cosas; es el módulo que hay que partir |
| `profundidad` | Número de niveles distintos en el grafo | capas | Más capas separan más responsabilidades y añaden más código de paso y más mapeos |
| `ciclo` | Camino que sale de un módulo y vuelve a él siguiendo las flechas | camino | Su presencia anula toda la jerarquía: sin orden topológico no hay capas, solo un grupo de módulos acoplados |
| `violación` | Arista que incumple la regla de nivel declarada | aristas | Es la deuda de arquitectura que hay que pagar antes de tocar nada de esa zona |

:::

La condición de ciclo se detecta descomponiendo el grafo en sus **componentes fuertemente conexas**
(CFC): un conjunto de nodos donde cada uno puede alcanzar a todos los demás. Si un módulo está
solo en su CFC, no participa en ningún ciclo; si comparte CFC con otros, todos ellos forman un
ciclo y hay que romperlo.

:::formula
CFC = { C ⊆ M : para todo u, v en C, u alcanza a v y v alcanza a u }
:::

- `C` — una componente fuertemente conexa. Su tamaño es la medida del acoplamiento mutuo: un `C`
  de un solo elemento quiere decir que ese módulo puede ordenarse sin ambigüedad.
- La salida del algoritmo da las CFC en **orden topológico inverso**: si `C1` aparece antes que
  `C2`, entonces `C1` no depende de `C2`. Ese orden es la lista de capas del sistema, calculada en
  lugar de dibujada a mano.
- `profundidad` del sistema es el número de CFC en la cadena más larga, y el orden topológico
  admite varias soluciones válidas: no hay una jerarquía única, hay una familia de ellas.

Los límites, en esta notación, son aristas que además cruzan un cambio de formato. Un límite bien
puesto es una arista que va de un adaptador a una interfaz del dominio, y en la interfaz no
aparece ningún tipo del exterior: ni el modelo del ORM, ni el diccionario del JSON, ni el objeto
de conexión.

## Ejemplo

Un servicio con cinco módulos y estas dependencias, leídas de los `import` reales:

| Módulo | Importa a |
| --- | --- |
| `dominio` | nada |
| `adaptador` | `dominio` |
| `servicio` | `dominio`, `informe` |
| `informe` | `dominio` |
| `composicion` | `servicio`, `adaptador` |

Si alguien añade una línea en `dominio` que importa `adaptador` —«es solo para reutilizar el
cliente de la base de datos»—, las CFC pasan de cinco bloques sueltos a uno solo: `dominio`,
`adaptador`, `servicio`, `informe` y `composicion` quedan mutuamente alcanzables y ya no hay
ninguna jerarquía que respetar. El síntoma llega tarde y disfrazado: los tests unitarios del
dominio empiezan a necesitar la base de datos.

Con el grafo sano, en cambio, el orden topológico sale solo y confirma la intuición:

| Paso | Módulo | Qué significa |
| --- | --- | --- |
| 1 | `dominio` | No depende de nada: puede construirse y probarse aislado |
| 2 | `informe` | Solo necesita el dominio |
| 3 | `adaptador` | Solo necesita el dominio |
| 4 | `servicio` | Necesita dominio e informe, ya construidos |
| 5 | `composicion` | Necesita todo lo anterior: es el último en construirse |

Fíjate en que `nivel(dominio) < nivel(servicio)` en el sentido de la fórmula: el nivel bajo es el
que no depende de nada. Las capas no se declaran antes de escribir el código; se **calculan** a
partir de él. Y en cuanto se calculan, se pueden pasar a una comprobación automática dentro de la
integración continua, que es lo único que impide que la arquitectura se erosione con el tiempo.

## Código

```python verificable
# Detectar el ciclo: componentes fuertemente conexas (algoritmo de Tarjan, iterativo)
dependencias = {
    "dominio": [],
    "informe": ["dominio"],
    "adaptador": ["dominio"],
    "servicio": ["dominio", "informe"],
    "composicion": ["servicio", "adaptador", "informe"],
}

indice, pila, en_pila, componentes = 0, [], set(), []
orden, bajo, visto = {}, {}, set()

for origen in dependencias:
    if origen in visto:
        continue
    trabajo = [(origen, 0)]
    while trabajo:
        nodo, siguiente = trabajo.pop()
        if siguiente == 0:                     # primera vez que se visita el nodo
            visto.add(nodo)
            orden[nodo] = bajo[nodo] = indice
            indice += 1
            pila.append(nodo)
            en_pila.add(nodo)
        hijos = dependencias[nodo]
        if siguiente < len(hijos):
            trabajo.append((nodo, siguiente + 1))
            hijo = hijos[siguiente]
            if hijo not in visto:
                trabajo.append((hijo, 0))       # se visita al hijo y se vuelve a este nodo
            elif hijo in en_pila:
                bajo[nodo] = min(bajo[nodo], orden[hijo])
        else:                                   # el nodo ya no tiene hijos pendientes
            if bajo[nodo] == orden[nodo]:
                componente = []
                while True:
                    salido = pila.pop()
                    en_pila.discard(salido)
                    componente.append(salido)
                    if salido == nodo:
                        break
                componentes.append(sorted(componente))
print("componentes (de hojas a raices):", componentes)
# -> componentes (de hojas a raices): [['dominio'], ['informe'], ['adaptador'], ['servicio'], ['composicion']]
ciclos = [c for c in componentes if len(c) > 1]
print("ciclos:", len(ciclos), " - modulos aislados:", sum(len(c) == 1 for c in componentes))
# -> ciclos: 0  - modulos aislados: 5
```

:::claves
- El resultado sale en **orden topológico inverso**: `dominio` aparece primero porque no depende
  de nadie, y `composicion` al final porque depende de todo. Ese orden es la jerarquía de capas
  del sistema, calculada en lugar de dibujada.
- La pila `trabajo` sustituye a la recursión. La versión recursiva del algoritmo es más corta y
  revienta con una pila de más de mil llamadas: en un grafo de imports real, eso pasa.
- `bajo[nodo]` guarda el índice más pequeño alcanzable desde el nodo, y `orden[nodo]` el instante
  en que se visitó. Un nodo abre componente cuando los dos coinciden, que es cuando ya no queda
  ningún camino de vuelta hacia arriba.
- `en_pila` evita contar como ciclo una arista que apunta a un nodo ya cerrado: solo las aristas
  hacia nodos que siguen abiertos bajan el `bajo`.
- `componentes` sale en orden de cierre, no alfabético. Por eso `['dominio']` va antes que
  `['informe']`, aunque alfabéticamente sea al revés: el orden es información, no presentación.
:::

```python verificable
# La misma deteccion, con la arista prohibida y envuelta en una funcion para poder repetirla
def componentes_fuertemente_conexas(grafo):
    """Devuelve las CFC del grafo, de hojas a raices (Tarjan iterativo)."""
    indice, pila, en_pila, salida = 0, [], set(), []
    orden, bajo, visto = {}, {}, set()
    for origen in grafo:
        if origen in visto:
            continue
        trabajo = [(origen, 0)]
        while trabajo:
            nodo, siguiente = trabajo.pop()
            if siguiente == 0:
                visto.add(nodo)
                orden[nodo] = bajo[nodo] = indice
                indice += 1
                pila.append(nodo)
                en_pila.add(nodo)
            hijos = grafo[nodo]
            if siguiente < len(hijos):
                trabajo.append((nodo, siguiente + 1))
                hijo = hijos[siguiente]
                if hijo not in visto:
                    trabajo.append((hijo, 0))
                elif hijo in en_pila:
                    bajo[nodo] = min(bajo[nodo], orden[hijo])
            else:
                if bajo[nodo] == orden[nodo]:
                    componente = []
                    while True:
                        salido = pila.pop()
                        en_pila.discard(salido)
                        componente.append(salido)
                        if salido == nodo:
                            break
                    salida.append(sorted(componente))
    return salida

sano = {
    "dominio": [],
    "informe": ["dominio"],
    "adaptador": ["dominio"],
    "servicio": ["dominio", "informe"],
    "composicion": ["servicio", "adaptador"],
}
enfermo = dict(sano, dominio=["adaptador"])    # el dominio reutiliza el cliente de la base de datos

for nombre, grafo in (("sano", sano), ("con la arista prohibida", enfermo)):
    componentes = sorted(componentes_fuertemente_conexas(grafo), key=len)
    ciclos = [c for c in componentes if len(c) > 1]
    print(f"{nombre}: {len(ciclos)} ciclo(s) -> {ciclos}")
# -> sano: 0 ciclo(s) -> []
# -> con la arista prohibida: 1 ciclo(s) -> [['adaptador', 'dominio']]
print("el ciclo arrastra a:", sorted({modulo for ciclo in ciclos for modulo in ciclo}))
# -> el ciclo arrastra a: ['adaptador', 'dominio']
```

:::claves
- El cambio entre los dos grafos es **una línea**: `dict(sano, dominio=["adaptador"])` copia el
  diccionario y solo pisa esa clave. Por eso conviene que la función reciba el grafo como
  argumento en vez de leerlo de una variable global: se puede comparar el antes y el después.
- Las componentes se ordenan con `key=len` solo para presentarlas: el orden que devuelve Tarjan
  es el topológico y ese sí tiene significado. Reordenar para imprimir está bien; usarlo para
  decidir las capas, no.
- En el grafo enfermo, `informe`, `servicio` y `composicion` siguen siendo componentes sueltas:
  el ciclo solo se lleva a los dos módulos que se importan mutuamente. Eso acota el trabajo de
  arreglo a una arista, y es exactamente lo que hay que evitar cuando la deuda se extiende.
- La regla que se lleva a integración continua sale de aquí sin discusión: si
  `componentes_fuertemente_conexas` devuelve alguna componente de más de un módulo, el build
  falla. La arquitectura deja de ser una opinión y pasa a ser una comprobación.
:::

```python verificable
# El limite que hace probable el dominio: dos adaptadores, el mismo caso de uso, cero base de datos
from typing import Protocol

class Reloj(Protocol):
    def hoy(self) -> str: ...

class RepositorioSuscripciones(Protocol):
    def buscar(self, cliente: str) -> dict: ...

class ServicioDeCobro:
    def __init__(self, repositorio: RepositorioSuscripciones, reloj: Reloj):
        self.repositorio = repositorio        # el dominio no sabe de donde vienen los datos
        self.reloj = reloj

    def a_cobrar(self, cliente: str) -> bool:
        suscripcion = self.repositorio.buscar(cliente)
        return suscripcion["activa"] and suscripcion["vence"] <= self.reloj.hoy()

class RepositorioDePrueba:                     # adaptador en memoria, para los tests
    def __init__(self, datos):
        self.datos = datos

    def buscar(self, cliente):
        return self.datos[cliente]

class RelojFijo:
    def __init__(self, fecha):
        self.fecha = fecha

    def hoy(self):
        return self.fecha

datos = {"ana": {"activa": True, "vence": "2026-10-01"},
         "luis": {"activa": False, "vence": "2026-01-01"}}
servicio = ServicioDeCobro(RepositorioDePrueba(datos), RelojFijo("2026-10-15"))
print("ana:", servicio.a_cobrar("ana"), " luis:", servicio.a_cobrar("luis"))
# -> ana: True  luis: False
```

:::claves
- La clase `ServicioDeCobro` no importa nada de infraestructura: recibe objetos que cumplen
  `Protocol`. La comprobación es **estructural**, no por herencia, así que `RepositorioDePrueba`
  no necesita declarar que implementa la interfaz: le basta con tener el método `buscar` con la
  firma correcta.
- `RelojFijo` existe para que el test no dependa de la fecha del día. Un caso de uso que llama a
  `datetime.now()` por dentro es imposible de probar en el límite del mes, y ese es justo el
  límite que interesa probar.
- El diccionario que devuelve `buscar` es el formato de la frontera. Aquí son dos claves, pero si
  en vez de un `dict` el repositorio devolviese el objeto del ORM, el dominio quedaría atado a
  ese ORM: el límite estaría mal puesto aunque el código funcione.
- `Protocol` de `typing` no crea ninguna clase base ni comprueba nada en tiempo de ejecución: los
  errores de firma los ve el analizador estático, no Python. Es una interfaz para el que lee y
  para el `mypy`, no un mecanismo de despacho.
- El servicio **no** guarda copia del repositorio ni del reloj: guarda las referencias que le
  pasan. Por eso la composición es el único sitio donde se decide qué implementación se usa, y
  cambiarla no toca ni una línea del dominio.
:::

```text
Fronteras, en orden de lo que cuesta cruzar mal la linea
frontera                | que cruza                 | que NO debe cruzar
HTTP / interfaz         | JSON, codigos de estado   | entidades del dominio hacia el cliente
casos de uso            | entidades, comandos       | objetos de conexion, sesiones de ORM
persistencia            | filas, documentos         | logica de negocio en SQL o en triggers
terceros (pagos, correo)| peticiones y respuestas   | el modelo del proveedor en el dominio
cola / mensajeria       | mensajes con version      | el esquema interno serializado tal cual
```

## Errores típicos

- **Confundir carpetas con capas.** Tener `models/`, `services/` y `repositories/` no garantiza
  nada si `models/` importa el ORM. La comprobación es leer los `import`, y se puede automatizar:
  si la regla no se comprueba en integración continua, se rompe en el tercer mes.
- **Poner la lógica de negocio en el controlador o en SQL.** Es el atajo que parece ahorrar una
  capa y termina duplicando la regla: una vez en la consulta y otra en el servicio. Cuando las dos
  versiones se separan, nadie sabe cuál es la buena.
- **Devolver el objeto del ORM desde el repositorio.** El dominio acaba llamando a métodos de
  carga diferida y disparando consultas sin saberlo. El límite está para traducir, y traducir
  incluye no dejar pasar el tipo de fuera.
- **Inyectar el contenedor en vez de las dependencias.** Una clase que recibe el contenedor y pide
  lo que necesita por dentro esconde sus dependencias reales: el grafo deja de ser analizable y
  los tests tienen que montar medio sistema para probar una función.
- **Crear un ciclo «temporal» para reutilizar una función.** Es el error que destruye la jerarquía
  entera: en cuanto un módulo de abajo importa uno de arriba, las CFC se fusionan y ya no hay
  orden topológico. Se arregla moviendo la función compartida al módulo de abajo o a un módulo
  nuevo, nunca con un `import` dentro de una función.
- **Abstraer antes de tener dos implementaciones.** Una interfaz con una sola implementación y sin
  perspectiva de otra es una capa de paso que hay que mantener. La señal de que toca abstraer es
  el segundo adaptador, no la elegancia del diagrama.
- **Dibujar la arquitectura y no medirla.** Un diagrama de capas en la wiki no es verificable y
  envejece en semanas. El grafo de dependencias del código sí lo es: se extrae, se comprueba y se
  falla el build cuando aparece una arista prohibida.

:::practica
enunciado: Un equipo tiene un módulo `facturacion` que importa `pdf`, `correo` y `base_de_datos`, y `base_de_datos` importa a su vez `facturacion` para consultar los tipos de factura. Enumera los ciclos, propón un corte y di qué regla automática dejarías en integración continua.
pista: Pinta el grafo con tres nodos y sigue las flechas: hay más de un camino que vuelve al punto de partida. Después piensa en qué módulo es el que no debería depender de nadie.
solucion: Las flechas son `facturacion -> pdf`, `facturacion -> correo`, `facturacion -> base_de_datos` y `base_de_datos -> facturacion`, así que los cuatro módulos forman un único ciclo, no varios: cualquiera alcanza a los demás. El corte razonable es sacar los tipos de factura a un módulo `tipos` que no dependa de nadie, hacer que `facturacion` y `base_de_datos` importen `tipos`, y dejar la escritura en la base de datos detrás de una interfaz que `facturacion` declare y un adaptador implemente. La regla para la integración continua: extraer el grafo de importaciones en cada push, calcular las componentes fuertemente conexas y fallar el build si alguna tiene más de un módulo; además, comprobar que ningún módulo por debajo de un límite declarado importa a otro por encima.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa que la flecha de dependencia apunta hacia dentro en una arquitectura en capas?
o: Que el dominio importa los adaptadores y la interfaz importa el dominio
o: Que los adaptadores conocen el dominio, y el dominio no conoce a los adaptadores
o: Que todas las capas importan un módulo común de utilidades
a: 2
e: El dominio declara las interfaces que necesita y los adaptadores las implementan, así que la dependencia de compilación va del adaptador hacia dentro. Si el dominio importase el adaptador, el núcleo de negocio quedaría atado a la base de datos y a los tests de infraestructura. Un módulo de utilidades compartido por todas las capas no invierte nada: solo añade acoplamiento.
:::

:::quiz
p: Un módulo aparece solo en su propia componente fuertemente conexa. ¿Qué quiere decir?
o: Que no participa en ningún ciclo y se puede ordenar sin ambigüedad
o: Que no tiene ninguna dependencia de salida
o: Que nadie depende de él
a: 1
e: Una componente de un solo elemento significa que no hay camino que salga del módulo y vuelva a él. Puede tener dependencias de salida y puede recibir dependencias de otros: lo único que se sabe es que no está metido en un ciclo. Si además no tuviera ninguna arista de salida, sería una hoja del grafo, que es un caso más fuerte.
:::

:::quiz
p: ¿Cuál es la señal de que un límite entre capas está bien puesto?
o: Que existe una carpeta con el nombre de la capa
o: Que se puede sustituir la implementación por otra en las pruebas sin arrancar la infraestructura
o: Que la capa de arriba tiene más líneas de código que la de abajo
a: 2
e: Un límite bien puesto traduce el formato en la frontera, así que el caso de uso se puede probar con un adaptador en memoria y sin base de datos. La carpeta no dice nada: se puede tener `repositories/` y seguir importando el driver desde el dominio. El tamaño relativo de las capas tampoco indica nada sobre la dirección de las dependencias.
:::
