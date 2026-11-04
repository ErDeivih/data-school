import contextlib

# Anidados: entran en orden y salen al reves (LIFO), pase lo que pase.
@contextlib.contextmanager
def etapa(nombre):
    print("entra", nombre)
    try:
        yield nombre.upper()        # lo que hay antes del yield es __enter__
    finally:
        print("sale", nombre)       # lo que hay despues es __exit__

with etapa("abrir fichero") as a, etapa("leer cabecera") as b:
    print("trabajando con", a, "y", b)
# -> entra abrir fichero / entra leer cabecera / trabajando con ABRIR FICHERO y LEER CABECERA
# -> sale leer cabecera / sale abrir fichero

# Sin try/finally, la limpieza que va despues del yield no se ejecuta si el cuerpo falla.
@contextlib.contextmanager
def sin_proteccion(nombre):
    print("tomo", nombre)
    yield nombre
    print("suelto", nombre)         # no se imprime si el cuerpo lanza

try:
    with sin_proteccion("recurso"):
        raise ValueError("falla el cuerpo")
except ValueError:
    pass
# -> tomo recurso   (y nunca "suelto recurso")
