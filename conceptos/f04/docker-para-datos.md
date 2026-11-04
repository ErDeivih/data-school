---
id: docker-para-datos
titulo: Docker para datos
fase: 4
nivel: intermedio
rutas: [de, ds]
prerequisitos: [entorno-python, ciclo-de-vida-del-dato]
tags: [docker, contenedores, reproducibilidad, entornos]
resumen: Una imagen empaqueta tu código con sus librerías y sus versiones exactas, para que el mismo trabajo se ejecute igual en tu portátil y en el servidor.
fuentes: ["Documentación oficial de Docker, 'Dockerfile reference'"]
---

## En una frase

Docker construye una **imagen** (una plantilla de solo lectura con el sistema, las librerías y
tu código congelados) y cada vez que la ejecutas arranca un **contenedor** idéntico, así que
«en mi máquina funcionaba» deja de ser una excusa y pasa a ser un hecho comprobable.

## La idea

El problema que resuelve Docker no es de informática, es de arqueología. Tu análisis funciona
porque en tu portátil hay pandas 2.2.3, una librería del sistema que instalaste hace un año sin
recordarlo y una variable de entorno que pusiste en marzo. En el servidor no hay nada de eso, y
la semana que viene tu portátil tampoco será el mismo. Docker convierte esa suma accidental de
circunstancias en un fichero de texto que se puede leer y reconstruir.

La analogía útil es la de una tarta de capas congelada. Cada instrucción del `Dockerfile`
—instalar dependencias, copiar código— añade una capa inmutable a la imagen. Docker guarda cada
capa y, si no cambia, la reutiliza: por eso el orden de las instrucciones decide si reconstruir
tarda 45 segundos o ninguno. Un contenedor es esa tarta con una capa de escritura fina encima:
todo lo que el proceso escribe en el sistema de ficheros vive ahí y desaparece cuando el
contenedor se destruye, que es lo que pasa de forma normal y rutinaria.

**Un contenedor no es una máquina virtual.** Comparte el kernel del anfitrión, así que no
arranca un sistema operativo entero: arranca en milisegundos y su tamaño es el de tus
dependencias, no el de un disco. A cambio, el aislamiento es más fino que el de una máquina
virtual, y eso importa para lo que viene después: en [[kubernetes-basico]] orquestas muchos de
estos contenedores.

Tres cosas que conviene tener claras desde el principio:

- **Los datos no van dentro de la imagen.** Si copias un CSV de 2 GB, la imagen pesa 2 GB, cada
  servidor que la descargue arrastra esos 2 GB y, peor, los datos quedan congelados en la
  versión del día que construiste. Los datos van en un **volumen** o, mejor todavía, fuera del
  contenedor: en un almacén de objetos o en una base de datos.
- **La imagen se identifica por su digest, no por su etiqueta.** `python:3.12-slim` es una
  etiqueta que se puede mover; el digest `sha256:…` es el contenido. Si de verdad necesitas
  reproducibilidad, fija el digest.
- **Un proceso por contenedor.** Si tu contenedor arranca un *supervisor* con tres servicios,
  has reconstruido una máquina virtual pequeña y has perdido lo bueno del modelo.

## Definición formal

Un `Dockerfile` es una receta declarativa. Estas son las instrucciones que se usan de verdad en
un proyecto de datos:

| Instrucción | Qué hace | Crea capa |
| --- | --- | --- |
| `FROM` | Elige la imagen base y arranca la construcción | Sí |
| `RUN` | Ejecuta un comando durante la construcción (instalar, compilar) | Sí |
| `COPY` | Copia ficheros del contexto de construcción a la imagen | Sí |
| `WORKDIR` | Fija el directorio de trabajo de las instrucciones siguientes | No |
| `ENV` | Define una variable de entorno que existirá en el contenedor | No |
| `ARG` | Variable disponible solo durante la construcción | No |
| `USER` | Usuario con el que correrá el proceso | No |
| `EXPOSE` | Documenta el puerto; no lo publica | No |
| `CMD` | Comando por defecto, sustituible desde la línea de órdenes | No |
| `ENTRYPOINT` | Comando fijo del contenedor; `CMD` pasa a ser sus argumentos | No |

La regla de la caché es la única que hay que memorizar:

:::formula
capa k cambia ⇒ se rehacen k, k+1, …, n
:::

Es decir: **lo que cambia a menudo va al final**. Tu código cambia a diario y tus dependencias
casi nunca, así que el fichero de dependencias se copia primero y el código después.

Otras dos definiciones que se confunden:

- **Volumen**: almacenamiento gestionado por Docker que sobrevive al contenedor. Se declara con
  `-v nombre:/ruta` o en el bloque `volumes:` de un fichero de composición. Un *bind mount*
  (`-v /ruta/del/anfitrion:/ruta`) monta una carpeta tuya; úsalo para desarrollar, no en
  producción.
- **Red**: los contenedores de una misma red definida por el usuario se ven entre ellos por el
  nombre del servicio, no por IP. Publicar un puerto con `-p 8888:8888` es lo que permite
  entrar desde fuera; sin `-p`, el puerto solo existe dentro de la red.

## Ejemplo

Dos `Dockerfile` que instalan lo mismo. La diferencia es el orden de dos líneas:

```dockerfile
# Mal orden: el codigo va antes que las dependencias
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "pipeline"]

# Buen orden: primero lo que casi nunca cambia
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python", "-m", "pipeline"]
```

Tocas una línea de `pipeline.py` y vuelves a construir. En la primera versión, el `COPY . /app`
cambia, así que la caché se rompe ahí y **vuelve a instalar todas las dependencias**. En la
segunda, el `COPY requirements.txt` no ha cambiado, la capa de `pip install` se reutiliza y solo
se recopia el código. Si suponemos que instalar tarda 45 segundos y copiar el código 0, la
diferencia por construcción es de 45 segundos a cero; multiplicado por las veinte
construcciones de una tarde, es la diferencia entre trabajar y esperar.

El tamaño sigue la misma aritmética de suma. Si la base pesa 120 MB y la capa de dependencias
240 MB, la imagen ronda los 360 MB. Si además copias una carpeta de datos de 2 GB, la imagen
pasa a 2,4 GB: cada `docker pull` en cada servidor mueve 2,4 GB y cada versión nueva del código
duplica ese tráfico si no reutilizas capas.

## Código

```python verificable
# Cada instruccion del Dockerfile es una capa cacheada. Cambiar una capa obliga a
# rehacer esa y todas las posteriores; las anteriores se reutilizan.
def segundos_rehechos(capas, coste, capa_tocada):
    return sum(coste[c] for c in capas[capas.index(capa_tocada):])

coste = {
    "FROM python:3.12-slim": 2,
    "COPY requirements.txt": 0,
    "RUN pip install -r requirements.txt": 45,
    "COPY . /app": 0,
}

malo = ["FROM python:3.12-slim", "COPY . /app", "RUN pip install -r requirements.txt"]
bueno = ["FROM python:3.12-slim", "COPY requirements.txt",
         "RUN pip install -r requirements.txt", "COPY . /app"]

# Tocas un fichero .py: la unica capa que cambia de contenido es el COPY del codigo
print("mal orden: ", segundos_rehechos(malo, coste, "COPY . /app"), "s")   # -> 45 s
print("buen orden:", segundos_rehechos(bueno, coste, "COPY . /app"), "s")  # -> 0 s
```

```dockerfile
# Construccion en dos etapas: la etapa de compilacion no llega a la imagen final.
FROM python:3.12-slim AS compilacion
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/instalado -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=compilacion /instalado /usr/local
COPY . /app
RUN useradd --create-home analista
USER analista
EXPOSE 8000
CMD ["python", "-m", "pipeline"]
```

```bash
# El contexto de construccion excluye lo que no debe entrar en la imagen
printf '__pycache__/\n.venv/\n.git/\n*.parquet\n.env\n' > .dockerignore

docker build -t analitica/pipeline:1.4.0 .
docker run --rm -v "$PWD/datos:/datos:ro" analitica/pipeline:1.4.0
docker run --rm -p 8000:8000 analitica/pipeline:1.4.0
```

## Errores típicos

- **Copiar los datos dentro de la imagen.** Es el error más caro y el más frecuente: la imagen
  engorda, los *pull* se vuelven lentos y los datos se congelan en la versión del día que
  construiste. Monta un volumen de solo lectura o lee del almacén de objetos.
- **Usar la etiqueta `latest`.** El mismo `Dockerfile` construido hoy y dentro de un mes da
  imágenes distintas, y no hay forma de saber cuál corría cuando el informe salió mal. Fija
  versiones (`pandas==2.2.3`) y, en producción, el digest.
- **`COPY . .` sin `.dockerignore`.** Mete `.git`, el entorno virtual, `__pycache__` y a veces
  un `.env` con credenciales. Además invalida la caché cada vez que cambia cualquier fichero,
  incluidos los datos.
- **Ejecutar como root.** Es la opción por defecto y casi nunca la que quieres. Crea un
  usuario sin privilegios y cámbialo con `USER`; el contenedor comparte kernel con el
  anfitrión y no es una frontera tan gruesa como una máquina virtual.
- **Escribir resultados en el sistema de ficheros del contenedor.** Si el pipeline guarda el
  Parquet de salida en `/app/resultados` y no has montado nada, ese fichero desaparece al
  recrear el contenedor. Escribe en un volumen o súbelo a almacenamiento de objetos.
- **Meter varios servicios en un contenedor.** Un orquestador de procesos dentro del contenedor
  rompe el modelo: no puedes escalar solo el que va lento ni reiniciar uno sin tumbar el otro.
  Sepáralos y conéctalos por la red.

## Comprueba que lo sabes

:::quiz
p: ¿Por qué el orden de las instrucciones del Dockerfile afecta al tiempo de construcción?
o: Porque las instrucciones de abajo se ejecutan con más privilegios
o: Porque Docker reutiliza las capas que no han cambiado y, al cambiar una, rehace esa y todas las posteriores
o: Porque `RUN` siempre es más lento que `COPY`
a: 2
e: Cada instrucción que toca el sistema de ficheros crea una capa cacheada. Si el código se copia antes de instalar las dependencias, cualquier cambio en el código invalida también la capa de instalación. Poniendo el código al final, la instalación se reutiliza.
:::

:::quiz
p: Un compañero guarda el resultado del pipeline en `/app/salida.csv` y desaparece cada pocas horas. ¿Qué está pasando?
o: Que el contenedor se recrea y borra su capa de escritura, porque no hay ningún volumen montado en esa ruta
o: Que el disco del servidor está lleno
o: Que hay que ejecutar el contenedor como root para poder escribir
a: 1
e: La capa de escritura de un contenedor es efímera: muere con él. Los datos que deben sobrevivir van en un volumen o fuera del contenedor. Ejecutar como root no arregla nada: el fichero se escribe igual, simplemente se pierde al recrear.
:::

:::aviso
Una imagen no es una copia de seguridad y un volumen no es un *backup*. Si el volumen vive en el
mismo disco que el contenedor, un fallo de disco se lleva los dos. Los datos que importan
necesitan copia fuera de la máquina.
:::
