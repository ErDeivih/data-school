class Almacen:
    """Sujeto observable: no conoce a nadie en concreto, solo avisa."""
    def __init__(self):
        self._suscriptores = []
        self.existencias = {}

    def suscribir(self, funcion):
        self._suscriptores.append(funcion)      # guarda la funcion, no su resultado

    def recibir(self, producto, unidades):
        # get con valor por defecto: el producto nuevo entra con 0 en vez de dar KeyError.
        self.existencias[producto] = self.existencias.get(producto, 0) + unidades
        total = self.existencias[producto]
        # Aviso a todos; el sujeto no sabe que hace ninguno ni en que orden importa.
        for funcion in self._suscriptores:
            funcion(producto, total)

eventos = []

def registrar(producto, total):
    # append devuelve None: aqui el valor no importa, lo que cuenta es el efecto.
    eventos.append(f"log: {producto} llega a {total}")

def avisar_a_compras(producto, total):
    # Cada suscriptor decide si le afecta; el almacen no lo consulta antes.
    if total < 5:
        eventos.append(f"pedir mas {producto}")

almacen = Almacen()
almacen.suscribir(registrar)          # se pasan las funciones sin parentesis
almacen.suscribir(avisar_a_compras)
almacen.recibir("tornillos", 3)       # 3 < 5: avisan los dos suscriptores
almacen.recibir("tornillos", 4)       # total 7: solo registra el primero

for evento in eventos:
    print(evento)
print("avisos emitidos:", len(eventos))    # -> 3
