class Cuenta:
    def __init__(self, titular, saldo=0.0):
        self.titular = titular          # atributo de instancia: cada objeto tiene el suyo
        self.saldo = saldo

    def ingresar(self, cantidad):
        self.saldo += cantidad          # modifica ESTE objeto y no devuelve nada
        return None


ana = Cuenta("Ana", 100.0)
luis = Cuenta("Luis", 100.0)

devuelto = ana.ingresar(50.0)
print("lo que devuelve ingresar:", devuelto)                    # -> None
print("saldo de ana:", ana.saldo, " saldo de luis:", luis.saldo)  # -> 150.0 y 100.0
print("la clase de ana:", type(ana).__name__)                   # -> Cuenta
