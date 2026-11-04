---
id: entorno-python
titulo: Entorno de Python
fase: 3
nivel: básico
rutas: [de, ds, core]
prerequisitos: []
tags: [python, entorno, reproducibilidad]
resumen: Un intérprete concreto más las versiones exactas de sus librerías: aislarlo por proyecto y fijarlas es lo que hace que tu análisis se pueda repetir.
fuentes: ["Ramalho (2022), 'Fluent Python', 2.ª edición"]
---

## En una frase

Un entorno de Python es la pareja formada por un intérprete concreto y el conjunto de librerías que
ese intérprete ve; crear uno por proyecto y dejar escritas las versiones exactas es lo que permite
que el análisis de hoy se ejecute igual dentro de un año y en otro ordenador.

## La idea

Instalar librerías en el Python del sistema es como tener una sola cocina para todo el edificio:
cada vez que alguien necesita una olla distinta, se lía. El proyecto A necesita `pandas 2.x` porque
su código usa un comportamiento que cambió; el proyecto B necesita `pandas 3.x`. Con un intérprete
global compartido no pueden coexistir, y arreglar uno rompe el otro.

Hay una segunda razón, más grave: **el Python del sistema no es tuyo**. En Linux, la distribución
trae un Python que usan sus propias herramientas; en macOS, varias utilidades del sistema dependen
del Python instalado. Tocar sus librerías puede dejar la máquina en un estado del que cuesta salir.

Un **entorno virtual** resuelve las dos cosas. Al crear un entorno, Python copia (o enlaza) el
intérprete y le da su propia carpeta de librerías, aislada del resto. Cuando activas ese entorno,
las órdenes `python` y `pip` apuntan dentro de él; cuando lo desactivas, vuelven al sistema. No hay
magia: la activación solo cambia la variable `PATH`, y por eso en un servidor de integración nunca
se activa nada, se llama directamente a `.venv/bin/python`.

De ahí sale el error más común de todos: crear el entorno, olvidarse de activarlo e instalar con
`pip`. Ese `pip` pertenece al intérprete global, así que las librerías acaban fuera del proyecto y
el fallo no aparece hasta que ejecutas el script en otra máquina. La forma a prueba de balas es
llamar a `pip` **como módulo del intérprete que quieres usar**: `python -m pip install ...`.

El último ingrediente es dejar escrito qué necesita el proyecto, en dos niveles:

- **Declarar**: una lista de dependencias directas, en `requirements.txt` o en el bloque `[project]`
  de `pyproject.toml`. Dice «mi código necesita pandas y scikit-learn».
- **Fijar**: las versiones exactas, incluidas las **transitivas** (las que traen tus dependencias).
  Eso es un fichero de bloqueo (`lock`): `uv.lock`, `poetry.lock` o el resultado de `pip freeze`.

Fijar solo lo directo no basta. Si tu `requirements.txt` dice `pandas` a secas, mañana se instalará
otra versión; y si dice `pandas==3.0.6` pero numpy entra sin fijar, el entorno tampoco queda
determinado. Un análisis es reproducible si coinciden la versión menor de Python, las versiones de
todos los paquetes y, si hay extensiones compiladas, la plataforma.

## Definición formal

Un entorno de Python queda determinado por esta terna:

:::formula
Entorno = ( intérprete, versión de Python, { paquete : versión } )
:::

- **Intérprete** — el ejecutable que traduce y ejecuta el código. El de referencia es CPython, el
  que se instala desde python.org o el gestor del sistema.
- **`sys.prefix`** — la carpeta raíz del entorno activo. En un entorno virtual apunta a la carpeta
  del entorno; en el intérprete del sistema coincide con `sys.base_prefix`.
- **`site-packages`** — la carpeta dentro del entorno donde se instalan las distribuciones. Es lo
  que hace que dos entornos no se vean entre sí.
- **Distribución** — un paquete instalable con nombre, versión y metadatos. Se distribuye como
  *wheel* (binario ya compilado) o como *sdist* (código fuente que hay que compilar).
- **Especificador de versión** — la restricción que escribes: `==3.0.6` (exacta), `>=2.0,<3.0`
  (rango), `~=3.0` (compatible dentro de la misma versión mayor).
- **Dependencia transitiva** — la que no escribes tú, sino tus dependencias.

:::formula
Reproducible ⟺ misma versión menor de Python y todas las versiones fijadas con ==
:::

«Versión menor» significa `3.12` frente a `3.13`: los binarios compilados para una no funcionan en
la otra, así que la versión de Python forma parte de la receta igual que las librerías. Y la
igualdad de la fórmula es exigente a propósito: cualquier `>=` deja una decisión abierta que se
resolverá de forma distinta el día que alguien instale.

## Ejemplo

Un `requirements.txt` de cinco líneas:

```text
numpy==2.5.2
pandas==3.0.6
scipy>=1.18,<2.0
scikit-learn==1.5.2
requests
```

- Tres líneas fijan la versión exacta con `==`: instalarán siempre lo mismo.
- Una línea fija un rango: hoy resolverá a una versión y dentro de un año, a otra.
- Una línea no dice nada: `requests` significa «la última que haya», que puede ser cualquier cosa.

Solo la primera categoría hace reproducible el entorno, y solo si además las dependencias
transitivas están fijadas: para eso se usa un fichero de bloqueo, que se genera una vez, se guarda
en el repositorio y se instala a partir de él. Un truco práctico: guarda el hash del fichero de
dependencias junto al resultado del análisis, y podrás decir con qué se generó cada tabla.

Los comandos del día a día, en Windows y en Linux:

```bash
# crear el entorno dentro del proyecto (una sola vez)
python -m venv .venv

# activarlo
.venv\Scripts\activate            # Windows (PowerShell: .venv\Scripts\Activate.ps1)
source .venv/bin/activate         # Linux y macOS

# instalar desde el fichero de dependencias, siempre como modulo del interprete
python -m pip install -r requirements.txt

# comprobar a que interprete estas apuntando
python -c "import sys; print(sys.executable)"
```

Y la estructura que genera, con el entorno dentro de la carpeta del proyecto:

```text
mi-analisis/
    .venv/                  entorno aislado: no se versiona ni se copia
        Scripts/            en Windows: python.exe, pip.exe, activate
        Lib/site-packages/  aqui caen las librerias instaladas
    requirements.txt        lo que declaro
    analisis.py             mi codigo
```

Con `uv`, un instalador y resolvedor mucho más rápido que `pip`, el flujo es el mismo pero con
menos pasos: `uv venv` crea el entorno, `uv pip install -r requirements.txt` instala, `uv lock`
genera el fichero de bloqueo y `uv sync` deja el entorno exactamente como dice el bloqueo. La idea
que hay que llevarse no es la herramienta, sino la separación entre **declarar** lo que necesitas y
**fijar** lo que acabó instalándose.

## Código

```python verificable
import re

requisitos = """numpy==2.5.2
pandas==3.0.6
scipy>=1.18,<2.0
scikit-learn==1.5.2
requests
"""

lineas = [l.strip() for l in requisitos.strip().splitlines()]
fijadas = [l for l in lineas if "==" in l]
rangos = [l for l in lineas if "==" not in l and re.search(r"[<>~]=", l)]
sueltas = [l for l in lineas if l not in fijadas and l not in rangos]

print(f"lineas en el fichero  {len(lineas)}")   # -> 5
print(f"con version exacta    {len(fijadas)}")  # -> 3
print(f"con rango             {len(rangos)}")   # -> 1
print(f"sin restriccion       {len(sueltas)}")  # -> 1
```

```python verificable
import hashlib

requisitos = "numpy==2.5.2\npandas==3.0.6\nscipy>=1.18,<2.0\nscikit-learn==1.5.2\nrequests\n"
# El mismo fichero con un solo caracter cambiado en el rango de scipy
cambiado = requisitos.replace(">=1.18", ">=1.19")

def huella(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

print(f"huella original       {huella(requisitos)[:16]}")   # -> 4be22d82cce0b8c4
print(f"huella con un cambio  {huella(cambiado)[:16]}")     # -> 0c46a8447de41818
print(f"coinciden             {huella(requisitos) == huella(cambiado)}")  # -> False
```

Esa es la razón de guardar el hash: dos entornos con ficheros de dependencias distintos se
distinguen en un vistazo, aunque el cambio sea un solo dígito.

## Errores típicos

- **Instalar en el Python global.** `pip install` sin entorno, o con `sudo`, deja las librerías
  fuera del proyecto y puede romper herramientas del sistema operativo. Crea un entorno por
  proyecto, siempre.
- **Crear el entorno y no usarlo.** El fallo típico: `python -m venv .venv`, no activarlo, e instalar
  con `pip`. El script funciona en tu máquina porque hay una copia global de la librería y falla en
  cualquier otra. Comprueba con `python -c "import sys; print(sys.executable)"` que la ruta está
  dentro de `.venv`.
- **Fijar solo las dependencias directas.** `pandas==3.0.6` no fija la versión de numpy que pandas
  arrastra. Sin bloqueo, dos instalaciones de la misma receta pueden dar entornos distintos.
- **Versionar o copiar la carpeta del entorno.** `.venv/` contiene rutas absolutas en sus scripts de
  activación y binarios compilados para tu sistema; copiarla a otra máquina no funciona. Se
  versiona el fichero de dependencias, no el entorno, y `.venv/` va en `.gitignore`.
- **Confundir declarar con congelar.** `requirements.txt` escrito a mano declara; `pip freeze`
  congela **todo** lo que hay instalado, incluido lo que instalaste para probar y ya no usas. Son
  cosas distintas y mezclarlas ensucia el proyecto.
- **Mezclar intérpretes sin darte cuenta.** En Windows, `python` puede ser el alias de la Microsoft
  Store; en Linux, `python` puede no existir y ser `python3`. Ten claro cuál es, con su versión, y
  escríbelo en el README del proyecto.

:::practica
enunciado: Un `requirements.txt` tiene estas líneas: `numpy==2.5.2`, `pandas>=3.0`, `scipy`, `requests==2.32.3`. ¿Cuántas quedarán con la misma versión dentro de un año y cuántas no? Explica qué haría falta para que el fichero entero fuese reproducible.
pista: Distingue las líneas que llevan `==` de las que llevan un rango o ninguna restricción.
solucion: Con `==` hay dos: numpy y requests, que instalan siempre lo mismo. `pandas>=3.0` resuelve a versiones distintas según el día y `scipy` a la última publicada, así que ninguna de las dos queda determinada dentro de un año. Quedan 2 de 4. Para que las cuatro sean reproducibles hay que escribirlas todas con `==` y añadir un fichero de bloqueo con lo que finalmente se instaló.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Para qué sirve un entorno virtual?
o: Para que el código se ejecute más rápido
o: Para aislar las librerías de cada proyecto y no tocar el Python del sistema
o: Para poder usar Python sin instalarlo
a: 2
e: El entorno no cambia la velocidad ni sustituye al intérprete: copia o enlaza uno y le da su propia carpeta de librerías, de modo que dos proyectos con versiones incompatibles conviven y el Python del sistema no se toca. Sin él, instalar para un proyecto puede romper otro o romper herramientas del sistema.
:::

:::quiz
p: Tu requirements.txt dice pandas==3.0.6 y numpy sin fijar, pero numpy entra como dependencia de pandas. ¿Es reproducible ese entorno?
o: Sí, porque pandas está fijado con ==
o: No, porque las dependencias transitivas quedan libres y pueden resolverse a versiones distintas en cada instalación
o: Sí, siempre que uses el mismo sistema operativo
a: 2
e: Fijar solo lo directo deja abiertas las versiones que arrastran tus dependencias. Lo que determina el entorno es el conjunto completo de versiones instaladas, y para eso hace falta un fichero de bloqueo. El sistema operativo importa para los binarios, pero no resuelve el problema de las versiones.
:::

:::quiz
p: ¿Cuál es la forma segura de instalar una librería en el entorno del proyecto?
o: pip install libreria, después de activar el entorno
o: python -m pip install libreria, usando el intérprete del entorno
o: sudo pip install libreria
a: 2
e: Llamar a pip como módulo del intérprete garantiza que se instala en ese entorno aunque te hayas olvidado de activarlo, que es el fallo más frecuente. Activar y usar pip funciona, pero es frágil. Y sudo instala en el Python del sistema, justo lo que hay que evitar.
:::
