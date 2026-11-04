# Un gestor escrito a mano: __enter__ entrega el recurso y __exit__ lo suelta siempre.
class Pool:
    def __init__(self, nombre):
        self.nombre = nombre
        self.prestado = False

    def __enter__(self):
        self.prestado = True
        print("presto", self.nombre)
        return self

    def __exit__(self, tipo, valor, traza):
        self.prestado = False
        print("devuelvo", self.nombre)
        return False        # False: si habia excepcion, sigue su curso

pool = Pool("conexion")
try:
    with pool as p:
        print("dentro: prestado =", p.prestado)
        raise ValueError("consulta mal escrita")
except ValueError as e:
    print("la excepcion llego fuera:", e)
print("fuera: prestado =", pool.prestado)
# -> presto conexion
# -> dentro: prestado = True
# -> devuelvo conexion
# -> la excepcion llego fuera: consulta mal escrita
# -> fuera: prestado = False
