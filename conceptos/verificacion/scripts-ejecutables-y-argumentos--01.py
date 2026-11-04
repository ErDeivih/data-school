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
