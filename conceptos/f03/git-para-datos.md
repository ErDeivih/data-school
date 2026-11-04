---
id: git-para-datos
titulo: Git para datos
fase: 3
nivel: básico
rutas: [core, de, alg]
prerequisitos: [entorno-python, ficheros-y-encoding]
tags: [git, versionado, reproducibilidad, gitignore]
resumen: Ramas, commits y conflictos aplicados a un proyecto de datos, y por qué los ficheros de datos en crudo no se versionan en git.
fuentes: ["Chacon y Straub (2014), 'Pro Git'", "PEP 8, 'Style Guide for Python Code'"]
---

## En una frase

Git guarda la **historia de tu código**, no tus datos: versiona los scripts, las consultas y la
configuración que producen el resultado, y deja fuera los ficheros grandes y regenerables, que
git no sabe diffear y engordan el repositorio para siempre.

## La idea

Imagina que trabajas en un informe mensual. Tienes tres cosas en la mesa:

1. **La receta**: el script que lee los datos, los limpia y calcula las cifras.
2. **Los ingredientes**: el CSV de 800 MB con las transacciones del mes.
3. **El resultado**: un gráfico y una tabla de cinco números.

Git está hecho para la receta. Guarda cada cambio que haces en el script, permite volver a
cualquier versión anterior, deja que dos personas trabajen a la vez y avisa cuando las dos
tocan la misma línea. Eso es exactamente lo que quieres: saber *cómo* se calculó cada cifra.

Con los ingredientes no funciona. Git guarda una copia completa de cada versión del fichero
(comprimida, pero completa): subir el CSV de cada mes son 800 MB al mes, para siempre, y el
repositorio tarda minutos en clonarse. Además, git no puede combinar dos CSV: si dos personas
tocan el mismo fichero, el conflicto es el fichero entero, no una línea. La primera regla, y la
más importante: **los datos en crudo no se versionan; se guardan donde toca y se referencian
por su hash**.

La tercera pieza es la que casi nadie cuida y la que más disgustos da: **el resultado tiene que
salir de la receta**. Si el número del informe lo escribiste a mano en un documento, no hay
historia que valga: el día que cambia el dato, nadie sabe de dónde salía. En un proyecto de
datos, un commit decente contiene el script, la consulta y, si acaso, la tabla de cifras
generada por el script.

Y un malentendido que conviene desmontar ya: **una rama no es una carpeta de copias**. Es una
línea de historia que se puede fusionar. En datos se usan pocas ramas y bien nombradas:
`main` con lo que funciona, y una rama por cambio de cierta entidad. Veinte ramas abiertas
durante seis meses son veinte fusiones que nadie quiere hacer.

## Definición formal

El vocabulario, aplicado a datos:

- **Repositorio:** la carpeta `.git`, que contiene todos los objetos (versiones de ficheros) y
  las referencias. Se crea con `git init`.
- **Área de trabajo (working tree):** los ficheros que ves. **Índice (staging):** la foto que
  vas a confirmar con el siguiente commit. **HEAD:** el commit en el que estás.
- **Commit:** una foto del proyecto en un instante, identificada por un hash del contenido
  completo. Git clásico usa SHA-1 (40 caracteres hexadecimales) y el formato nuevo, SHA-256; en
  los dos casos, dos commits distintos no pueden tener el mismo hash.
- **Rama:** un puntero móvil a un commit. `main` es la convención actual para la rama
  principal (antes `master`).
- **Fusión (merge):** unir dos líneas de historia. Si las dos han cambiado la misma zona del
  mismo fichero, git no adivina y marca un **conflicto** que resuelves tú.
- **`.gitignore`:** un fichero con patrones de rutas que git debe ignorar. Los `*` y `?` son
  comodines; `datos/` ignora un directorio entero; `*.parquet` ignora todos los ficheros con
  esa extensión; una línea que empieza por `!` reabre una excepción.
- **`.gitattributes`:** reglas por tipo de fichero. Aquí se marcan los binarios y, muy
  importante en datos, se fuerza el salto de línea: `*.csv text eol=lf` evita que un fichero
  cambie solo porque alguien lo abrió en Windows.
- **Git LFS:** una extensión que guarda los ficheros grandes fuera del repositorio y deja un
  puntero dentro. Útil para un modelo o un binario pequeño, pero **no** es la solución para
  un CSV que cambia cada día.

Que se versiona y qué no, en una tabla mental:

- **Sí:** scripts, `notebooks` limpios sin salidas, consultas `.sql`, `requirements.txt` o
  `pyproject.toml`, ficheros de configuración sin secretos, tests, documentación, esquemas.
- **No:** datos en crudo, datos intermedios, ficheros Parquet, modelos entrenados, `venv/`,
  `__pycache__/`, `.env`, credenciales, ficheros con datos personales.
- **Casos límite:** un CSV de 200 líneas con la tabla de referencia de provincias **sí** se
  versiona (es pequeño, cambia poco y el diff es legible); un Parquet de 800 MB **no**.

## Ejemplo

Dos ficheros con el mismo contenido dan el mismo hash; un solo carácter distinto da un hash
completamente distinto:

```text
fichero A:      2024-01-05,1.50
fichero B:      2024-01-05,1.50      (mismo contenido)
hash(A) = hash(B)                    -> git lo guarda una sola vez

fichero C:      2024-01-05,1.50
fichero D:      2024-01-05,1,50
hash(C) != hash(D)                   -> git guarda DOS objetos completos
```

Esto explica por qué cambiar una coma en un CSV de 800 MB hace que git guarde otros 800 MB
comprimidos: no compara línea a línea para almacenar, guarda el objeto entero. Con código eso no
importa (los ficheros son de kilobytes); con datos, es la ruina del repositorio.

Otro caso concreto, el del `.gitignore`. Con estas líneas:

```text
datos/
*.parquet
.env
!datos/referencia.csv
```

- `ventas.parquet` → ignorado.
- `datos/ventas.csv` → ignorado.
- `.env` → ignorado.
- `datos/referencia.csv` → **también** ignorado, aunque la última línea intenta rescatarlo. Git
  no desciende dentro de un directorio ignorado, así que ningún `!` que apunte a algo de dentro
  tiene efecto.

Para que la excepción funcione hay que ignorar **el contenido** y no la carpeta:

```text
datos/*
!datos/referencia.csv
```

Con esta versión, `datos/ventas.csv` sigue ignorado y `datos/referencia.csv` sí entra. Se
comprueba con `git check-ignore -v datos/referencia.csv`, que dice qué línea del `.gitignore`
ha decidido.

## Código

```python verificable
# Por que un solo caracter en un CSV cambia el objeto que guarda git:
# el identificador es el hash del CONTENIDO completo, no un diff.
import hashlib

def hash_fichero(contenido: str) -> str:
    return hashlib.sha256(contenido.encode("utf-8")).hexdigest()

a = "2024-01-05,1.50\n2024-01-06,2.00\n"
b = "2024-01-05,1.50\n2024-01-06,2.00\n"          # mismo contenido
c = "2024-01-05,1.50\n2024-01-06,2,00\n"          # una coma en vez de un punto

print("A y B iguales:", hash_fichero(a) == hash_fichero(b))
print("A y C iguales:", hash_fichero(a) == hash_fichero(c))
print("prefijo de A:", hash_fichero(a)[:12])
print("prefijo de C:", hash_fichero(c)[:12])
print("caracteres distintos:", sum(1 for x, y in zip(a, c) if x != y))
```

```python verificable
# Cuanto pesa de mas el CSV frente al Parquet: el motivo de no versionar datos.
import io
import pandas as pd

filas = 5000
df = pd.DataFrame({
    "id": range(filas),
    "fecha": pd.date_range("2024-01-01", periods=filas, freq="h"),
    "cliente": [f"C{i % 500:03d}" for i in range(filas)],
    "importe": [round(10 + (i % 97) * 1.5, 2) for i in range(filas)],
})

csv_bytes = df.to_csv(index=False).encode("utf-8")
buffer = io.BytesIO()
df.to_parquet(buffer, compression="zstd")
parquet_bytes = buffer.getvalue()

print("filas:", len(df))
print("CSV     :", len(csv_bytes), "bytes")
print("Parquet :", len(parquet_bytes), "bytes")
print("factor  :", round(len(csv_bytes) / len(parquet_bytes), 1))
```

```python verificable
# Que se cuela en el repositorio y que no: comprobar el .gitignore antes de subir.
import fnmatch

candidatos = [
    "scripts/limpieza.py",
    "ventas.parquet",
    "datos/ventas.csv",
    "datos/referencia.csv",
    ".env",
]

def ignorado(ruta: str, patrones: list[str]) -> bool:
    """Modelo de .gitignore. La regla que importa aqui: si una carpeta queda excluida,
    git no baja a mirar dentro, asi que ningun ! sobre un fichero de dentro la reabre."""
    partes = ruta.split("/")
    for i in range(1, len(partes)):          # ¿hay alguna carpeta padre excluida?
        padre = "/".join(partes[:i])
        for patron in patrones:
            if not patron.startswith("!") and patron.rstrip("/") == padre:
                return True
    estado = False
    for patron in patrones:                  # patrones de fichero: gana el ultimo que encaja
        excepto = patron.startswith("!")
        limpio = patron.lstrip("!").rstrip("/")
        if fnmatch.fnmatch(ruta, limpio):
            estado = not excepto
    return estado

por_carpeta = ["datos/", "*.parquet", ".env", "!datos/referencia.csv"]
por_contenido = ["datos/*", "!datos/referencia.csv"]

for ruta in candidatos:
    print(f"{'IGNORADO' if ignorado(ruta, por_carpeta) else 'SUBE   '}  {ruta}")

print("referencia.csv con 'datos/':",
      "IGNORADO" if ignorado("datos/referencia.csv", por_carpeta) else "SUBE")
print("referencia.csv con 'datos/*':",
      "IGNORADO" if ignorado("datos/referencia.csv", por_contenido) else "SUBE")
```

```text
# .gitignore de un proyecto de datos: ignora el contenido, no la carpeta
datos/*
!datos/referencia.csv          # este si: es pequeno y cambia poco
*.parquet
*.csv                          # ojo: esto ignora tambien referencia.csv
.env
.venv/
__pycache__/
*.ipynb_checkpoints/

# Los datos se guardan FUERA y se referencian por su hash
# datos/ventas-2024-01.parquet   sha256=4f9a...d21
```

```bash ilustrativo
# Flujo diario, con las comprobaciones que evitan el 90 % de los sustos.
git status                       # que he tocado
git diff                         # que he cambiado exactamente
git check-ignore -v ventas.parquet   # por que (no) se ignora
git add scripts/limpieza.py      # anado el codigo, no los datos
git commit -m "Normaliza importes a euros antes de agregar"
git log --oneline --stat -3      # que ha entrado en los ultimos commits

# Un fichero grande que ya esta en el historial NO se arregla con rm:
# sigue ocupando sitio en todos los commits. Hay que reescribir la historia
# (git filter-repo) y avisar a todo el equipo antes de hacerlo.
```

## Errores típicos

- **Subir los datos en crudo al repositorio.** El repositorio crece para siempre, clonarlo pasa
  a tardar minutos y git no puede fusionar dos versiones del fichero. Los datos van a
  almacenamiento de objetos o a una carpeta compartida, y en el repositorio se guarda el script
  que los descarga más su hash para saber qué versión se usó.
- **Confiar en `.gitignore` para un fichero que ya está en el historial.** Si `ventas.csv` ya se
  confirmó alguna vez, añadirlo al `.gitignore` no lo saca: git solo ignora lo que no sigue. Hay
  que `git rm --cached ventas.csv` (que lo quita del seguimiento, no del disco) y hacer commit.
  Y si el fichero tiene datos sensibles, además hay que reescribir el historial.
- **Poner un secreto en el código y arreglarlo borrándolo después.** Una clave de API escrita en
  un script y borrada en el commit siguiente sigue estando en el historial, recuperable con un
  `git log -p`. Los secretos van en variables de entorno o en un gestor de secretos, y `.env`
  va en el `.gitignore` **desde el primer commit**.
- **Un commit con el mensaje «cambios».** Dentro de dos meses, cuando algo deje de cuadrar, la
  historia es lo único que te dirá por qué se cambió una fórmula. Un mensaje que explique el
  **porqué** («redondea a céntimos antes de sumar para cuadrar con el proveedor») vale más que
  veinte commits con «arreglos varios».
- **Guardar el notebook con las salidas dentro.** Cada reejecución reescribe el fichero entero
  (las imágenes van en base64) y el `diff` es ilegible, así que la revisión de cambios deja de
  tener sentido. Se ejecuta sin guardar salidas o se versiona el `.py` generado.
- **Resolver un conflicto quedándose con una de las dos versiones enteras.** En un conflicto
  real, las dos partes del fichero aportan cosas: hay que leer los dos bloques, decidir qué se
  queda y **ejecutar el código** después. Elegir «la mía» porque suena mejor es la forma más
  rápida de perder el arreglo del compañero.

:::trampa
Un `git add .` mete todo lo que no esté ignorado, incluido el CSV de 2 GB que acabas de
descargar y el `.env` con la contraseña de la base de datos. Usa `git status` antes de cada
commit y añade ficheros por su nombre. Recuperar un secreto ya subido no es borrar el fichero:
es rotar la credencial, porque en un repositorio compartido hay que suponer que ya lo ha visto
alguien.
:::

## Comprueba que lo sabes

:::quiz
p: Añades `datos/` a tu `.gitignore` y `git status` sigue mostrando `datos/ventas.csv` como pendiente. ¿Por qué?
o: Porque el `.gitignore` tiene un error de sintaxis
o: Porque ese fichero ya estaba en el historial: git solo ignora los ficheros que no sigue, así que hay que quitarlo del seguimiento con `git rm --cached`
o: Porque hay que hacer commit del `.gitignore` antes de que funcione
a: 2
e: El `.gitignore` solo afecta a ficheros sin seguimiento. Si el CSV se confirmó en algún commit anterior, seguirá apareciendo y hay que quitarlo del índice con `git rm --cached datos/ventas.csv`, que lo borra del seguimiento pero lo deja en el disco. Además, si contiene datos sensibles, quedará en el historial hasta que se reescriba.
:::

:::quiz
p: ¿Cuál de estos ficheros sí tiene sentido versionar en git?
o: El Parquet de 800 MB con las transacciones del mes
o: El script que lo genera y el fichero de requisitos con las versiones de las librerías
o: La carpeta `.venv/` completa para que el entorno sea idéntico en todos los equipos
a: 2
e: Los scripts y la lista de dependencias son pequeños, cambian a menudo y su historia explica cómo se obtuvo cada resultado: eso es justo lo que git hace bien. Los datos grandes no se pueden fusionar y engordan el repositorio para siempre. El entorno virtual se recrea a partir de los requisitos con una orden, y guardarlo añade miles de ficheros con rutas absolutas que no sirven en otra máquina.
:::

:::practica
enunciado: Un compañero ha subido por error un CSV de 300 MB con datos de clientes (nombre, correo y teléfono). El commit está a tres commits de distancia del actual. Enumera los pasos para arreglarlo, en orden, y di qué es urgente y qué puede esperar.
pista: Distingue entre lo que hay que corregir en el código, lo que hay que corregir en el historial y lo que hay que corregir fuera de git.
solucion: Primero lo urgente, que es la exposición de datos personales: hay que tratar los datos como comprometidos y actuar sobre el sistema de origen (rotar cualquier credencial que apareciera en el repositorio, notificar según el procedimiento de protección de datos de la organización y decidir si el dato debía estar ahí). En paralelo, lo técnico: (1) `git rm --cached` del fichero y añadirlo al `.gitignore`, para que no vuelva a entrar; (2) como el fichero está en commits anteriores, hay que reescribir el historial con `git filter-repo` (o BFG) para purgarlo de todos los commits, y no basta con un commit que lo borre, porque el objeto sigue accesible; (3) avisar a todo el equipo de que la historia se ha reescrito y que hay que volver a clonar, porque los hashes de los commits cambian; (4) forzar la actualización de la rama en el remoto y, si el repositorio es público o compartido con terceros, considerar los datos filtrados definitivamente. Lo que puede esperar es la limpieza de los datos: mover el CSV al almacenamiento correcto, dejar constancia en el README de dónde viven los datos y por qué hash se identifican, y añadir una comprobación previa al push (un gancho o una regla de integración continua) que rechace ficheros por encima de cierto tamaño.
:::
