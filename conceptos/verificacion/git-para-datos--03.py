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
