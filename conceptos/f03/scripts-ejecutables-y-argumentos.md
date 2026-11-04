---
id: scripts-ejecutables-y-argumentos
titulo: Scripts ejecutables y argumentos
fase: 3
nivel: básico
rutas: [core, de, ds]
prerequisitos: [entorno-python, funciones-y-modulos]
tags: [cli, argparse, pathlib, automatizacion]
resumen: De notebook a herramienta: leer los datos por argumentos con argparse, construir las rutas con pathlib y salir con código distinto de cero cuando algo falla.
fuentes: ["Python Software Foundation, 'argparse — Parser for command-line options, arguments and sub-commands' (documentación oficial)", "Python Software Foundation, 'pathlib — Object-oriented filesystem paths' (documentación oficial)"]
---

## En una frase

Un script ejecutable es un programa que recibe sus datos por argumentos en vez de tenerlos
escritos dentro, construye las rutas en vez de clavarlas y termina con un **código de salida**
que dice si ha funcionado; es lo que permite que otra persona, o un planificador, lo lance sin
abrir el editor.

## La idea

Un [[notebooks-vs-scripts|notebook]] es tú delante del teclado: miras, cambias, vuelves a
ejecutar. Un script es una máquina con un botón. Alguien —o algo— pulsa el botón a las tres de la
mañana, sin nadie mirando la pantalla, y necesita saber dos cosas: cómo decirle **qué** tiene que
procesar y cómo enterarse de si salió bien.

Esas dos cosas son las que cambian cuando pasas de analizar a automatizar:

1. **Los datos entran por argumentos.** Si el mes a resumir está escrito dentro del fichero, para
   cambiar de mes hay que editar código, guardarlo y volver a desplegarlo. Con
   `--mes 2026-02` el mismo fichero sirve para todos los meses, y el planificador solo cambia un
   texto.
2. **Las rutas se construyen.** `C:\Users\David\proyecto\datos\ventas.csv` funciona en tu
   portátil y falla en el contenedor de Linux, en la máquina de tu compañero y en el servidor de
   producción. Se construye desde una base: `Path("datos") / "ventas" / f"{mes}.csv"`.
3. **El código de salida es el único canal que ve quien te lanza.** Un planificador como
   [[orquestacion-y-dag|Airflow]], un `cron` o Docker no leen lo que imprimes: miran el número con
   el que termina el proceso. `0` significa «bien» y cualquier otro número significa «mal». Un
   script que imprime `"ERROR: no encuentro el fichero"` y termina con `0` deja el pipeline en
   verde y el informe vacío, y eso puede tardar semanas en detectarse.

`argparse` es la biblioteca estándar que resuelve el punto 1 sin que escribas analizador de
cadenas: declaras los argumentos, y ella te da `--help`, la conversión de tipos, los valores por
defecto, los mensajes de error y el código de salida `2`. `pathlib` resuelve el punto 2 con un
objeto `Path` al que le puedes preguntar si existe, qué extensión tiene o cuál es su carpeta
padre. Y el código de salida sale de `sys.exit()` o de `raise SystemExit(...)`, que son la misma
cosa escrita de dos maneras.

## Definición formal

Un programa de línea de órdenes tiene la forma `programa [opciones] argumentos`, donde las
opciones llevan `--` delante y su valor detrás (`--mes 2026-02`) y los argumentos posicionales
van sueltos (`ventas.csv`). Python te los entrega en `sys.argv`, una lista de **cadenas** cuya
posición `0` es el nombre del propio programa.

El contrato del código de salida, que es una convención del sistema operativo y no de Python:

:::formula
salida = 0  ⇒  éxito        salida ≠ 0  ⇒  el paso ha fallado
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `salida` | Número con el que termina el proceso; es lo único que mira el planificador | Entero de 0 a 255 | En cuanto deja de ser 0, el paso se marca en rojo y no se lanzan los que dependían de él |
| `0` | Todo fue bien | código | No representa un fallo: es el valor de éxito, y cualquier otro se lee como error |
| `1` | Fallo del propio script; una excepción no capturada también termina con 1 | código | Es el fallo genérico, el que sí merece un reintento porque puede ser transitorio |
| `2` | Error de uso: falta un argumento, el tipo no cuadra o el valor no está entre las opciones | código | Lo devuelve `argparse` solo, y significa «me has llamado mal»: reintentar lo mismo fallará igual |
| `126` y `127` | El shell no llegó a ejecutar el script: 126 sin permiso de ejecución, 127 no encontró el programa o el intérprete | código | A partir de 126 el fallo ya no es del script: mira permisos, la ruta y el `PATH` |
| `sys.argv` | Argumentos tal cual llegan, todos cadenas, con el nombre del programa en la posición 0 | cadenas | Cuantos más haya, más validaciones a mano; `argparse` existe justo para no hacerlas |
:::

Dentro del script, el código se escribe con `sys.exit(n)` o con `raise SystemExit(n)`. Si el
argumento es un texto en vez de un número —`sys.exit("no encuentro el fichero")`— Python lo
imprime en la salida de error y sale con código `1`.

## Ejemplo

Este es el mismo script lanzado de cinco maneras distintas. El script se llama
`resumen_ventas.py` y su salida depende del caso:

| Orden | Código | Qué ve quien lo lanza |
| --- | --- | --- |
| `python resumen_ventas.py datos/ventas.csv --mes 2026-01 --limite 3` | 0 | Las 3 primeras filas del resumen por la salida estándar |
| `python resumen_ventas.py datos/ventas.csv --limite 0` | 2 | Aviso de que el límite tiene que ser positivo, en la salida de error |
| `python resumen_ventas.py datos/ventas.csv --limite tres` | 2 | Uso del programa y `invalid int value: 'tres'`, impreso por `argparse` |
| `python resumen_ventas.py` | 2 | Uso del programa y `the following arguments are required: entrada` |
| `python resumen_ventas.py datos/noexiste.csv` | 1 | `no encuentro datos/noexiste.csv`, en la salida de error |

Fíjate en la diferencia entre las dos últimas. El código `2` dice «no me has llamado bien»:
reintentar exactamente la misma orden dará exactamente el mismo error, así que el planificador no
debe reintentar. El código `1` dice «me has llamado bien, pero el mundo no está como esperaba»:
puede que el fichero llegue cinco minutos tarde, así que ahí sí tiene sentido un reintento. Esa
distinción, que parece un detalle, es la que decide si un pipeline se recupera solo o se queda
parado toda la noche.

Y el error que cuesta un fin de semana: si el script envuelve la lectura del fichero en un
`try`/`except`, imprime `"aviso: no hay datos"` y sigue con un DataFrame vacío, termina con `0`.
El planificador pinta el paso en verde, los siguientes pasos también, y el cuadro de mando se
publica vacío. Durante doce días nadie lo nota, porque no hay ningún error en ningún sitio.

## Código

```python verificable
import argparse

def construir_parser():
    """Declara los argumentos que acepta el script: nombre, tipo y valor por defecto."""
    p = argparse.ArgumentParser(description="Resume un CSV de ventas")
    p.add_argument("entrada", help="ruta del CSV de entrada")
    p.add_argument("--mes", default="2026-01", help="mes a resumir, en formato AAAA-MM")
    p.add_argument("--limite", type=int, default=100, help="filas maximas a imprimir")
    p.add_argument("--modo", choices=["rapido", "exacto"], default="rapido")
    return p

# parse_args con una lista lee esa lista en vez de sys.argv: asi el ejemplo es comprobable
# sin lanzar el script desde la terminal.
args = construir_parser().parse_args(["datos/ventas.csv", "--limite", "250"])
print("entrada:", args.entrada)                        # -> entrada: datos/ventas.csv
print("mes sin decirlo:", args.mes)                    # -> mes sin decirlo: 2026-01
print("limite:", args.limite)                          # -> limite: 250
print("tipo de limite:", type(args.limite).__name__)   # -> tipo de limite: int
print("modo:", args.modo)                              # -> modo: rapido
```

```python verificable
import argparse
import contextlib
import io

p = argparse.ArgumentParser(prog="resumen_ventas.py")
p.add_argument("entrada")
p.add_argument("--limite", type=int, default=100)

# argparse escribe el aviso de uso en la salida de error y termina con SystemExit. Aqui se
# guarda ese aviso en un buffer solo para que la salida del ejemplo se lea de un tiron.
ruido, codigos = io.StringIO(), []
with contextlib.redirect_stderr(ruido):
    for orden in (["--limite", "tres", "datos.csv"], []):
        try:
            p.parse_args(orden)
        except SystemExit as e:
            codigos.append(e.code)      # argparse no devuelve un error: sale del programa

print("codigo con un tipo que no cuadra:", codigos[0])       # -> codigo con un tipo que no cuadra: 2
print("codigo sin el argumento obligatorio:", codigos[1])    # -> codigo sin el argumento obligatorio: 2
print("el usuario ve un aviso:", "error:" in ruido.getvalue())   # -> el usuario ve un aviso: True
print("SystemExit no lo captura 'except Exception':", not issubclass(SystemExit, Exception))
# -> SystemExit no lo captura 'except Exception': True
```

```python verificable
import sys
from pathlib import Path

def resumen(entrada: Path, limite: int) -> int:
    """Devuelve el codigo de salida: 0 bien, 2 mal uso, 1 fallo del entorno."""
    if limite <= 0:
        print("--limite tiene que ser positivo", file=sys.stderr)
        return 2                        # lo he llamado mal: reintentar no arregla nada
    if not entrada.exists():
        print(f"no encuentro {entrada}", file=sys.stderr)
        return 1                        # puede ser transitorio: aqui si tiene sentido reintentar
    return 0

# La ruta se construye; no se escribe ninguna ruta absoluta de esta maquina.
ruta = Path("datos") / "ventas" / "2026-01.csv"
print("la ruta por partes:", ruta.parts)      # -> la ruta por partes: ('datos', 'ventas', '2026-01.csv')
print("solo el nombre:", ruta.name)           # -> solo el nombre: 2026-01.csv
print("sin extension:", ruta.stem)            # -> sin extension: 2026-01
print("cambiando la extension:", ruta.with_suffix(".parquet").name)
# -> cambiando la extension: 2026-01.parquet
print("codigo con limite 0:", resumen(ruta, 0))                    # -> codigo con limite 0: 2
print("codigo con un fichero que no existe:", resumen(ruta, 10))   # -> codigo con un fichero que no existe: 1
print("el planificador solo mira si es cero:", resumen(ruta, 10) != 0)
# -> el planificador solo mira si es cero: True
```

```text
resumen_ventas.py — el esqueleto, con el codigo al final en su sitio

  import argparse
  from pathlib import Path

  def main(argv: list[str]) -> int:
      args = construir_parser().parse_args(argv)
      ...                                   # el trabajo de verdad
      return 0                              # y 1 o 2 cuando algo va mal

  if __name__ == "__main__":                # solo si lanzan el fichero, no si lo importan
      raise SystemExit(main(sys.argv[1:]))

  La terminal solo ve el numero:
    python resumen_ventas.py datos/ventas.csv    ->  0   y el planificador sigue
    python resumen_ventas.py datos/noexiste.csv  ->  1   y el planificador reintenta
    python resumen_ventas.py                     ->  2   y el planificador te avisa
```

:::claves
- `parse_args()` sin argumento lee `sys.argv[1:]`, y todo llega como **cadena**: sin `type=int`, `args.limite` es `"250"` y `args.limite > 3` lanza `TypeError`.
- `argparse` no devuelve un error de uso: llama a `sys.exit(2)`, que lanza `SystemExit`. Como `SystemExit` hereda de `BaseException` y no de `Exception`, tu `except Exception` no lo captura y el mensaje de uso llega al usuario como debe.
- `--help` termina con código `0`, no con `2`: pedir ayuda no es un error. Un `except SystemExit` que trate todo igual convertiría la ayuda en un fallo.
- `default` se aplica solo si el argumento no aparece; `action="store_true"` convierte `--cache` en un booleano que vale `False` si no lo pasas, y **no acepta** `--cache False`.
- `Path("datos") / "x.csv"` no toca el disco: solo construye el objeto. Quien mira el disco es `.exists()` o `.is_file()`, y quien escribe es `.write_text()` o `.mkdir()`. Para enseñar una ruta en una respuesta usa `.parts`, `.name` o `as_posix()`: `str(ruta)` en Windows sale con barras invertidas.
- La barra de `/` solo funciona si el lado izquierdo es un `Path`: `"datos" / "x.csv"` lanza `TypeError`. Con cadenas, la herramienta es `os.path.join`.
- `if __name__ == "__main__":` es lo que permite que un test haga `import resumen_ventas` sin que se ejecute todo el trabajo.
:::

## Errores típicos

- **Clavar la ruta absoluta de tu máquina.** `r"C:\Users\David\datos\ventas.csv"` funciona hoy y
  falla en cuanto el script se ejecuta en otro sitio. Si necesitas una referencia absoluta, la
  única legítima es la carpeta del propio fichero: `Path(__file__).parent`.
- **Capturar la excepción y terminar bien.** Un `except Exception: print("algo falló")` sin
  `sys.exit(1)` deja el pipeline en verde con datos incompletos. Si el paso no puede cumplir su
  contrato, tiene que decirlo con el código de salida, no con un mensaje.
- **Leer `sys.argv` a mano.** Sin `argparse` no hay `--help`, no hay conversión de tipos y las
  posiciones se rompen en cuanto alguien añade un argumento en medio. Además, los índices
  empiezan en `1` porque `sys.argv[0]` es el nombre del programa.
- **Escribir la salida en el directorio actual.** `df.to_csv("resultado.csv")` escribe donde el
  planificador tenga su directorio de trabajo, que casi nunca es donde tú estabas. La ruta de
  salida se pasa por argumento o se construye a partir de una base conocida, y la carpeta se crea
  antes con `.mkdir(parents=True, exist_ok=True)`.
- **Abrir sin `encoding="utf-8"`.** En Windows el valor por defecto no es UTF-8: un CSV con
  tildes se lee mal o revienta con `UnicodeDecodeError`, y el mismo script funciona en Linux.
  `open(ruta, encoding="utf-8")` y `df.to_csv(ruta, encoding="utf-8")`, siempre.
- **Mezclar los mensajes con el resultado.** Si el paso devuelve datos por la salida estándar,
  cualquier `print("voy por la fila 40")` los contamina. Los avisos y el progreso van a la salida
  de error (`file=sys.stderr`) o al registro del sistema, nunca a `stdout`.

:::trampa
Un `try`/`except` que se come `SystemExit` o un `return` sin código al final del `main` convierten
cualquier fallo en un éxito silencioso. La comprobación que lo pilla es de una línea: lanza el
script con un dato malo a propósito y mira el código con `echo $?` en Linux o `echo $LASTEXITCODE`
en PowerShell. Si sale `0`, el pipeline entero es mentira.
:::

:::practica
enunciado: Escribe el `argparse` de un script `cuenta.py` que reciba un CSV por argumento posicional `entrada`, una opción `--columna` con valor por defecto `"importe"`, y `--limite` entero con valor por defecto 10. Además, el `main` tiene que devolver 2 si el límite no es positivo, 1 si el fichero no existe y 0 si todo va bien. Di qué código de salida da cada uno de estos lanzamientos: `cuenta.py datos.csv`, `cuenta.py datos.csv --limite 5`, `cuenta.py datos.csv --limite 0`.
pista: Declara los argumentos con `add_argument` y usa `p.parse_args(argv)` dentro de `main`, no en el momento de construir el parser, para que un test pueda pasarle su propia lista.
solucion: El parser lleva `add_argument("entrada")`, `add_argument("--columna", default="importe")` y `add_argument("--limite", type=int, default=10)`. `main` comprueba primero el límite (devuelve 2 si es menor o igual que cero), después `Path(entrada).exists()` (devuelve 1 si no está) y al final hace el trabajo y devuelve 0. Los códigos: `cuenta.py datos.csv` da 0 si el fichero existe (columna `importe`, límite 10); `cuenta.py datos.csv --limite 5` da 0 (límite 5); `cuenta.py datos.csv --limite 0` da 2, porque el límite no es positivo, y ese 2 le dice al planificador que reintentar la misma orden es inútil. Si el fichero no existe, los dos primeros dan 1.
:::

## Comprueba que lo sabes

:::quiz
p: Tu script detecta que el fichero de entrada no existe, imprime el aviso, deja un DataFrame vacío y termina sin llamar a `sys.exit`. ¿Qué pasa en el pipeline?
o: El paso se marca como fallido, porque el aviso aparece en el registro
o: El paso se marca como correcto, porque el código de salida es 0, y los pasos siguientes se ejecutan con datos vacíos
o: El planificador lanza el paso otra vez automáticamente hasta que el fichero aparezca
a: 2
e: El planificador no lee los mensajes: solo mira el código de salida, y sin `sys.exit` ese código es 0. Por eso el fallo es invisible y los pasos siguientes se ejecutan con datos vacíos. El aviso en el registro no lo salva nadie, y el reintento automático tampoco existe si el paso consta como correcto.
:::

:::quiz
p: ¿Para qué sirve escribir `type=int` en un `add_argument`?
o: Para que el valor sea obligatorio
o: Para que `argparse` convierta la cadena a entero y, si no puede, avise y salga con código 2
o: Para que el entero se imprima sin decimales
a: 2
e: Lo que llega por la línea de órdenes son cadenas, siempre. `type=int` se encarga de la conversión y, cuando el texto no es un entero, escribe el error de uso y termina con código 2. La obligatoriedad se declara con `required=True`, y el formato al imprimir no tiene nada que ver con `argparse`.
:::

:::quiz
p: Un compañero lanza tu script en un contenedor de Linux y falla al abrir el fichero, aunque en tu portátil va bien. ¿Cuál es la causa más probable?
o: Que falta instalar pandas en el contenedor
o: Que la ruta del fichero está escrita a mano con la forma de Windows y no existe en ese contenedor
o: Que Linux no admite la biblioteca `pathlib`
a: 2
e: Una ruta absoluta de Windows como `C:\Users\David\datos\ventas.csv` no existe en Linux, y además la barra invertida se interpreta como carácter de escape. La solución es pasar la ruta por argumento o construirla con `pathlib` desde una base relativa al proyecto. `pathlib` es biblioteca estándar y funciona igual en los dos sistemas.
:::
