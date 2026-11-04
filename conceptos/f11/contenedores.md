---
id: contenedores
titulo: Contenedores
fase: 11
nivel: intermedio
rutas: [de, alg]
prerequisitos: [entorno-python, docker-para-datos]
tags: [contenedores, despliegue, aislamiento, imagenes]
resumen: Un contenedor no es una máquina virtual pequeña: es un proceso normal con namespaces, límites de recursos y un sistema de ficheros montado por capas.
fuentes: ["Merkel (2014), 'Docker: Lightweight Linux Containers for Consistent Development and Deployment'", "Hightower, Burns, Beda (2017), 'Kubernetes: Up and Running'"]
---

## En una frase

Un contenedor es un proceso corriente del sistema operativo al que se le han tapado los ojos
(namespaces) y se le ha puesto un contador (cgroups), ejecutándose sobre un sistema de ficheros
formado por capas de solo lectura y una capa de escritura que se tira al terminar.

## La idea

Imagina un edificio de apartamentos. Todos comparten los cimientos, la fontanería y la
instalación eléctrica: eso es el **kernel** del sistema operativo. Cada apartamento tiene su
puerta con llave, su número y su contador de la luz: eso son los **namespaces** (lo que no
puedes ver) y los **cgroups** (lo que puedes consumir). Una máquina virtual, en cambio, es una
casa independiente: tiene sus propios cimientos, su propia caldera y su propio tejado, con el
gasto y el tiempo de construcción que eso implica.

De esa diferencia salen las consecuencias prácticas:

- **Arranque.** Una máquina virtual arranca un sistema operativo completo: del orden de
  decenas de segundos. Un contenedor arranca un proceso: del orden de décimas de segundo.
- **Tamaño.** Una imagen lleva el userland (bibliotecas, intérprete) pero no un kernel: cientos
  de megas frente a los gigabytes de un disco de máquina virtual.
- **Aislamiento.** Un contenedor es más débil. Comparte kernel: un fallo de seguridad en el
  kernel afecta a todos los contenedores de la máquina, y un contenedor `--privileged` o con
  el socket de Docker montado dentro es, en la práctica, root en el anfitrión. No es un
  límite de seguridad equivalente a una máquina virtual; es un límite operativo.
- **Kernel.** No puedes cambiar de kernel dentro de un contenedor ni ejecutar un kernel
  distinto al del anfitrión. El «sistema operativo» del contenedor es solo el conjunto de
  bibliotecas de usuario que lleva la imagen.

**Imágenes y capas.** Una imagen no es un fichero monolítico: es una lista ordenada de capas.
Cada instrucción de un `Dockerfile` que cambia el sistema de ficheros produce una capa nueva, y
cada capa se identifica por el hash de su contenido. Al arrancar un contenedor, el motor apila
esas capas y añade encima una capa de escritura: cuando el proceso modifica un fichero de una
capa inferior, se copia primero hacia arriba (eso es *copy-on-write*). Consecuencia directa:
**lo que escribas dentro del contenedor muere con el contenedor**. Los datos van en un
volumen, la configuración en variables de entorno y los registros a la salida estándar.

**Volúmenes y redes.** Un *bind mount* enlaza una ruta del anfitrión dentro del contenedor: es
rápido y cómodo en desarrollo, pero ata el contenedor a la estructura de directorios de esa
máquina. Un volumen con nombre lo gestiona el motor: es portable y sobrevive a la recreación
del contenedor. En redes, el modo puente por defecto da a cada contenedor su propia dirección
y sale al exterior por traducción de direcciones; dos contenedores no se ven por `localhost`,
se ven por el nombre que resuelve la red interna. El modo `host` no aísla nada: el proceso usa
directamente la red del anfitrión.

**El detalle que rompe despliegues: las señales.** Dentro del contenedor, el primer proceso es
el PID 1, y el PID 1 tiene un comportamiento especial: si no instala manejadores, las señales
que no maneja se ignoran. Si arrancas la aplicación con la forma de shell, el que queda como
PID 1 es `/bin/sh`, que no reenvía la señal a tu programa. Entonces el motor espera el tiempo
de gracia (10 segundos por defecto), manda `SIGKILL` y el contenedor muere con código 137, sin
cerrar conexiones ni volcar estado.

## Definición formal

**Capa.** Diferencia de sistema de ficheros respecto de la capa anterior, empaquetada y
identificada por el hash de su contenido.

- **Digest** — identidad inmutable de una imagen o de una capa. Dos construcciones con el mismo
  contenido tienen el mismo digest; con contenido distinto, distinto digest.
- **Etiqueta** (*tag*) — puntero mutable a un digest. `app:latest` hoy y mañana pueden ser
  imágenes distintas, y por eso no se usa en producción: se fija el digest.
- **Sistema de ficheros por capas** (*overlay*) — al leer, gana la capa más alta que tenga el
  fichero; al escribir, el fichero se copia a la capa de escritura y se modifica allí.

**Tamaño en disco de varias imágenes.** Con una capa base compartida `B` y capas propias de
cada imagen `C₁ … C_N`:

:::formula
tamaño_en_disco = B + Σ Cᵢ    mientras que    suma_de_imágenes = N · (B + C)
:::

El ahorro es lo que hace viable tener veinte servicios construidos sobre la misma base.

**Qué es un contenedor, exactamente.** Un proceso en ejecución con:

- **namespaces** — vistas aisladas de PID, montajes, red, nombre de máquina, IPC y usuarios.
- **cgroups** — límites y contabilidad de CPU, memoria, entrada/salida y número de procesos.
- **capacidades y `seccomp`** — qué llamadas al sistema y qué privilegios conserva.
- **rootfs** — las capas de la imagen más una capa de escritura efímera.

**Fallo por memoria.** Si el proceso supera el límite de memoria de su cgroup, el kernel lo
mata con `SIGKILL`; el motor lo reporta como código de salida **137 = 128 + 9**. No hay
excepción capturable ni volcado: el proceso simplemente desaparece.

## Ejemplo

Un `Dockerfile` de cuatro capas:

```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
```

Con números redondos de este ejemplo: capa base 150 MB, capa de dependencias 250 MB, código
2 MB. Total de la imagen: 402 MB.

- Reconstruyes cambiando solo `app.py`: se reutilizan 3 capas de 4 y solo se reconstruye la de
  2 MB. Quien haya puesto `COPY . .` antes del `pip install` no tiene esa suerte: cualquier
  cambio en el código invalida la instalación de dependencias y paga 250 MB de nuevo.
- Tienes ocho servicios con la misma base y 250 MB de capas propias cada uno. Si cada imagen
  guardara su copia de la base, ocuparían 3.200 MB; con capas compartidas ocupan 2.150 MB, un
  32,8 % menos.

:::figura
fichero: contenedores-capas-y-deduccion
pie: Arriba, las cuatro capas del `Dockerfile` del ejemplo y qué sobrevive a cada cambio. Al tocar solo el código, tres capas salen idénticas y se reutilizan (en verde); al cambiar el `pip install`, esa capa y todo lo que va detrás se reconstruyen (en rojo). Por eso el código va al final del `Dockerfile`: lo que cambia mucho se pone donde arrastra a pocos. Abajo, ocho servicios sobre la misma base: la suma de los tamaños de las imágenes son 3.200 MB, pero en disco solo hay 2.150 MB, porque una capa compartida se guarda una vez. Ese 32,8 % es lo que permite tener veinte servicios construidos sobre la misma base.
fuente: figuras/contenedores-1.py
:::

Y el contraste con la máquina virtual, en órdenes de magnitud: la misma aplicación en una
máquina virtual lleva un sistema operativo completo, arranca en decenas de segundos y consume
gigas de disco; en un contenedor arranca en décimas de segundo y ocupa lo que ocupan sus
capas. El precio es que comparte kernel y que su aislamiento no es el de una máquina.

## Código

```python verificable
import hashlib

def huellas(lineas):
    """Cada capa depende de la anterior: cambiar una linea invalida las siguientes."""
    anterior, salida = "inicio", []
    for linea in lineas:
        # El hash encadena el contenido de la linea CON el de la capa anterior: por eso una
        # capa no se identifica sola, se identifica dentro de la cadena que la precede.
        anterior = hashlib.sha256((anterior + linea).encode()).hexdigest()[:6]
        salida.append(anterior)
    return salida

base = ["FROM python:3.12-slim",
        "COPY requirements.txt .",
        "RUN pip install -r requirements.txt",
        "COPY app.py ."]

# Cambia solo el codigo de la aplicacion
otro_codigo = base[:3] + ["COPY app.py .  # version nueva"]
# Cambian las dependencias: la capa del pip y todo lo que va detras
otras_dependencias = base[:2] + ["RUN pip install -r requirements.txt  # con numpy", base[3]]

# zip empareja capa con capa en orden y sum() cuenta las coincidencias: las reutilizadas.
reutilizadas_codigo = sum(a == b for a, b in zip(huellas(base), huellas(otro_codigo)))
reutilizadas_deps = sum(a == b for a, b in zip(huellas(base), huellas(otras_dependencias)))

print("al tocar solo el codigo se reutilizan:", reutilizadas_codigo, "de", len(base))   # -> 3 de 4
print("al tocar las dependencias se reutilizan:", reutilizadas_deps, "de", len(base))   # -> 2 de 4
```

:::claves
- El hash **no es el de una línea suelta**: es el de todo lo anterior más esa línea. Por eso una
  instrucción nueva invalida todas las que vienen detrás, y por eso el orden del `Dockerfile`
  decide cuánto se reconstruye. Cambiar `FROM` es reconstruir la imagen entera.
- `sum(a == b for a, b in zip(...))` cuenta coincidencias porque en Python `True` vale 1 y
  `False` vale 0. Es un idioma cómodo, pero si las dos listas no miden lo mismo `zip` se para en
  la más corta y el total sale corto **sin avisar**.
- El `[:6]` del final es solo para leerlo: un digest real son 64 caracteres hexadecimales.
  Recortarlo en un sistema de verdad provocaría colisiones de identidad entre capas distintas.
- Las dos listas comparadas no son «la imagen vieja y la nueva»: son la vieja y una **copia con
  una línea cambiada**. La segunda cambia además el número de líneas, y por eso el recuento no
  es simétrico entre los dos casos.
- `sin_dedup` es la **suma de los tamaños de las imágenes** y `con_dedup` lo que ocupa el disco
  cuando las capas compartidas se guardan una sola vez. Las dos cifras son correctas y miden
  cosas distintas: la primera engaña, la segunda es la que paga la factura.
- El ahorro depende de que las 8 imágenes compartan **la misma base literal**. Si cada servicio
  parte de una base distinta (o de una versión distinta de la misma), no hay nada que deduplicar
  y el 32,8 % desaparece.
:::

```python verificable
# Ocho servicios con la misma base: las capas compartidas se guardan una sola vez.
base_mb, capa_servicio_mb, servicios = 150, 250, 8

sin_dedup = servicios * (base_mb + capa_servicio_mb)      # suma de tamanos de imagen
con_dedup = base_mb + servicios * capa_servicio_mb        # lo que ocupa el disco de verdad

print("suma de tamanos de imagen:", sin_dedup, "MB")     # -> 3200 MB
print("bytes reales en disco:   ", con_dedup, "MB")      # -> 2150 MB
print(f"ahorro {100 * (1 - con_dedup / sin_dedup):.1f} %")   # -> 32.8 %
```

```text
# Bind mount: el directorio del anfitrion manda (desarrollo)
docker run --rm -v "$PWD:/app" -w /app python:3.12-slim python app.py

# Volumen con nombre: el motor lo gestiona y sobrevive al contenedor (produccion)
docker run -d --name api -p 8080:80 -v datos:/var/lib/api api:1.4.2@sha256:...

# Limites y reinicio: sin esto, un contenedor se come la maquina
docker run -d --memory 512m --cpus 1.5 --restart unless-stopped api:1.4.2
```

## Errores típicos

- **Guardar datos dentro del contenedor.** La capa de escritura es efímera: al recrear el
  contenedor desaparece todo. Los datos persistentes van en un volumen y el estado en un
  servicio externo.
- **Desplegar con `latest`.** La etiqueta es un puntero móvil: dos despliegues con la misma
  etiqueta pueden ejecutar código distinto, y no hay forma de saber qué versión está en
  producción. Fija el digest de la imagen.
- **Construir una imagen distinta por entorno.** Si el entorno se cuece dentro de la imagen,
  lo que pruebas no es lo que despliegas. Construye una vez y cambia solo la configuración
  ([[secretos-y-configuracion]]).
- **Usar la forma de shell en `CMD` y perder las señales.** `CMD python app.py` arranca un
  intérprete de shell como PID 1 que no reenvía `SIGTERM`; el contenedor agota los 10 segundos
  de gracia y muere con 137. Usa la forma de lista, `CMD ["python", "app.py"]`, y maneja la
  señal para cerrar limpio.
- **Creer que el contenedor es una frontera de seguridad.** Comparte kernel, y montar el socket
  de Docker o ejecutar `--privileged` equivale a dar root en el anfitrión. Como frontera real,
  usa una máquina virtual o un entorno con kernel propio.
- **Limitar la memoria sin avisar a la aplicación.** Un límite de 512 MB con una caché interna
  de 1 GB o una JVM mal dimensionada acaba en `SIGKILL` y código 137, sin mensaje de error.
  Configura la memoria de la aplicación a partir del límite del contenedor.
- **Confundir `EXPOSE` con publicar el puerto.** `EXPOSE` solo documenta; el puerto se publica
  al ejecutar, y el orden es `-p puerto_del_anfitrion:puerto_del_contenedor`.

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la diferencia esencial entre un contenedor y una máquina virtual?
o: El contenedor no puede ejecutar código compilado, solo intérpretes
o: El contenedor comparte el kernel del anfitrión y aísla procesos con namespaces y cgroups; la máquina virtual ejecuta su propio kernel sobre hardware virtualizado
o: El contenedor guarda sus datos en disco y la máquina virtual en memoria
a: 2
e: El contenedor no virtualiza hardware: es un proceso más del anfitrión con la vista tapada y un contador de consumo. Por eso arranca en décimas de segundo y ocupa menos, y por eso su aislamiento es más débil. La máquina virtual paga un kernel completo a cambio de una frontera más fuerte.
:::

:::quiz
p: Escribes un fichero de resultados en `/app/salida.csv` dentro de un contenedor y lo eliminas con `docker rm`. ¿Qué pasa con el fichero?
o: Se pierde: estaba en la capa de escritura, que se destruye con el contenedor
o: Se conserva en la imagen original
o: Se mueve automáticamente a un volumen anónimo
a: 1
e: La capa de escritura es efímera y muere con el contenedor. Para conservar datos hay que montar un volumen (con nombre) o un bind mount, y para intercambiar ficheros pequeños basta con copiarlos fuera con `docker cp`.
:::

:::quiz
p: Un contenedor termina con código de salida 137 justo cuando llega más tráfico. ¿Qué es lo más probable?
o: Un error de sintaxis en el código de la aplicación
o: Que el proceso fue matado con `SIGKILL`, típicamente por superar el límite de memoria del cgroup
o: Que la imagen tiene la etiqueta equivocada
a: 2
e: 137 = 128 + 9, y la señal 9 es `SIGKILL`: el proceso no pudo capturarla ni despedirse. Las causas habituales son exceder el límite de memoria del contenedor o agotar el tiempo de gracia tras un `SIGTERM` que nadie atendió. Un error de aplicación daría un código distinto y dejaría rastro en los registros.
:::

:::aviso
El modo `host` de red y los contenedores privilegiados resuelven problemas muy concretos de
rendimiento o de acceso a dispositivos, pero eliminan justo lo que hace útil a un contenedor.
Si tu aplicación «solo funciona» así, casi siempre hay un problema de configuración debajo.
:::
