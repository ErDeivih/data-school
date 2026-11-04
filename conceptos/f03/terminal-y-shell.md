---
id: terminal-y-shell
titulo: Terminal y shell
fase: 3
nivel: básico
rutas: [core, de, alg]
prerequisitos: [entorno-python, ficheros-y-encoding]
tags: [shell, bash, automatizacion]
resumen: Pipes, permisos, códigos de salida y cron: la herramienta con la que se depura un pipeline cuando algo falla a las tres de la mañana.
fuentes: ["Shotts (2019), 'The Linux Command Line'", "Robbins y Beebe (2005), 'Classic Shell Scripting'"]
---

## En una frase

El shell es el pegamento del sistema: une programas pequeños con tuberías, y su sintaxis es la
que usa el orquestador, el contenedor y el servidor donde vive tu pipeline.

## La idea

Un pipeline de datos no falla en el cuaderno: falla en una máquina sin pantalla, a una hora
incómoda, y se investiga con cuatro comandos. Quien no sabe shell depende de que otro le ejecute
las cosas; quien sabe, mira, corta y arregla.

La idea central es la **tubería**: cada programa hace una cosa, lee de la entrada estándar y
escribe en la salida estándar, y el siguiente recibe lo anterior. `grep` filtra, `sort` ordena,
`awk` corta columnas, `wc` cuenta. Ninguno sabe nada de los demás y juntos resuelven en una línea
lo que en Python son treinta.

La segunda idea es que **todo comando termina con un código**: cero si fue bien, distinto de cero
si falló. Ese número es el que decide si un DAG marca la tarea como fallida o si un `&&` encadena
el siguiente paso. Ignorarlo es la causa número uno de pipelines que «funcionan» y producen datos
vacíos.

:::trampa
`rm -rf $CARPETA` sin comillas borra cosas que no esperas si la variable está vacía o lleva
espacios. Con `set -u` el script aborta cuando usa una variable sin definir, y con
`set -euo pipefail` aborta al primer error, trata las variables no definidas como error y propaga
los fallos dentro de una tubería. Ese `pipefail` es la diferencia entre enterarte y no enterarte.
:::

## Definición formal

Un shell encadena procesos con tres canales y un contrato de salida:

:::formula
comando  [stdin 0] → [stdout 1] → [stderr 2]        exit 0 = éxito, otro = fallo
:::

- **stdin (0)** — de dónde lee el programa; por defecto, el teclado.
- **stdout (1)** — dónde escribe el resultado; por defecto, la pantalla.
- **stderr (2)** — dónde escribe los errores; separado para que un `>` no se lleve los mensajes.
- **`|`** — conecta el stdout de uno con el stdin del siguiente.
- **`>` y `>>`** — redirigen stdout a un fichero, truncando o añadiendo.
- **`2>&1`** — manda stderr al mismo sitio que stdout; imprescindible para guardar un log completo.
- **Código de salida** — `$?` lo guarda; `&&` ejecuta lo siguiente solo si fue cero.

Los permisos se leen en tres tríos —propietario, grupo, otros— y cada trío suma lectura (4),
escritura (2) y ejecución (1). `chmod 640` deja lectura y escritura al dueño, lectura al grupo y
nada a los demás.

## Ejemplo

Buscar los ficheros Parquet más grandes de un lago, contar cuántos hay por tabla y quedarse con
las tres tablas con más ficheros:

```text
$ find /lago -name "*.parquet" -size +100M -print0 \
    | xargs -0 du -h \
    | sort -rh | head -5
   1,2G  /lago/ventas/fecha=2026-01-01/part-000.parquet
   980M  /lago/ventas/fecha=2026-01-02/part-000.parquet
   ...
```

Tres piezas: `-print0` y `xargs -0` se comunican con bytes nulos, así que un nombre con espacios
no rompe nada; `du -h` da tamaños legibles; `sort -rh` ordena de mayor a menor entendiendo `1,2G`.

Y una línea de `cron` que lanza el proceso cada día a las 3:15 y guarda el log con la fecha:

```text
15 3 * * *  cd /srv/pipeline && ./cargar.sh >> /var/log/carga-$(date +\%F).log 2>&1
```

## Código

```text
Receta mínima de un script que no miente:

  #!/usr/bin/env bash
  set -euo pipefail              # aborta al primer fallo, variable sin definir o pipe roto
  cd "$(dirname "$0")"           # rutas relativas al script, no al directorio desde el que se llama
  LOG=/var/log/carga.log

  echo "[$(date -Is)] empieza" >> "$LOG"
  if ! ./ingesta.py >> "$LOG" 2>&1; then
      echo "[$(date -Is)] fallo la ingesta" >> "$LOG"
      exit 1
  fi
  echo "[$(date -Is)] termina" >> "$LOG"
```

Comprobar después:

```text
$ bash -n cargar.sh              # sintaxis, sin ejecutar
$ shellcheck cargar.sh           # el analizador que encuentra el 90 % de los fallos tontos
$ echo $?                        # 0 si el comando anterior fue bien
```

## Errores típicos

- **No mirar el código de salida.** Un comando que falla y sigue adelante produce un fichero
  vacío que parece un resultado. Usa `set -e` o comprueba `$?` explícitamente.
- **Parsear la salida de `ls`.** Los nombres con espacios y saltos de línea lo rompen. Usa `find`
  con `-print0` o globs del propio shell.
- **Redirigir solo stdout.** El error se queda en la pantalla y el log miente por omisión. Añade
  `2>&1`.
- **Variables sin comillas.** `"$VAR"` siempre; sin comillas, un espacio convierte un argumento en
  dos y un vacío borra el argumento.
- **`cron` sin rutas absolutas ni entorno.** `cron` no carga tu `.bashrc`: usa rutas completas, fija
  el `PATH` y registra lo que pasa, o el trabajo fallará en silencio cada noche.
- **Permisos `777` para salir del paso.** Deja el sistema abierto a cualquiera. Si algo necesita
  más permisos, el problema es el usuario, no el fichero.

:::practica
enunciado: Tienes un log de 4 GB y quieres las 10 IPs que más aparecen. Escribe la tubería y explica por qué no usas un script de Python.
pista: Cada línea empieza por la IP; `cut`, `sort`, `uniq -c` y `sort -rn`.
solucion: `cut -d" " -f1 access.log | sort | uniq -c | sort -rn | head -10`. No hace falta Python: son cuatro programas que ya existen, leen en streaming y no cargan 4 GB en memoria. Python sería razonable si hubiera que parsear JSON o aplicar reglas.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace `set -euo pipefail` en un script?
o: Abortar al primer error, tratar variables sin definir como error y propagar fallos dentro de una tubería
o: Activar el modo verboso y guardar un log
o: Ejecutar el script en segundo plano
a: 1
e: `-e` aborta al fallar un comando, `-u` da error si usas una variable vacía, `-o pipefail` hace que la tubería falle si falla cualquiera de sus partes. Sin lo tercero, `comando | head` puede devolver éxito aunque `comando` haya muerto.
:::

:::quiz
p: ¿Por qué se separa stderr de stdout?
o: Para poder guardar el resultado limpio en un fichero sin mezclarlo con los mensajes de error
o: Porque stderr es más lento
o: Porque stdout no admite errores
a: 1
e: Si un proceso escribe avisos y errores por stdout, el fichero de salida se contamina y el siguiente paso de la tubería recibe basura. Separarlos permite redirigir cada uno a su sitio y juntarlos solo cuando quieres un log completo.
:::
