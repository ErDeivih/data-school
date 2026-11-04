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
