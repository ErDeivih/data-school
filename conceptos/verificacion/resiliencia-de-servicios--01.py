# Un cortacircuitos, con el reloj inyectado para no tener que esperar de verdad.
class Cortacircuitos:
    def __init__(self, umbral_fallos=5, espera_s=2.0):
        self.umbral_fallos = umbral_fallos  # fallos consecutivos que lo abren
        self.espera_s = espera_s            # segundos que permanece abierto
        self.fallos = 0
        self.estado = "cerrado"
        self.abierto_hasta = 0.0

    def permite(self, ahora):
        # Al cumplirse la espera pasa a semiabierto: deja pasar UNA llamada de prueba.
        if self.estado == "abierto" and ahora >= self.abierto_hasta:
            self.estado = "semiabierto"
        return self.estado != "abierto"

    def registra(self, ok, ahora):
        if self.estado == "semiabierto":
            self.estado = "cerrado" if ok else "abierto"
            self.fallos = 0 if ok else self.umbral_fallos
            self.abierto_hasta = ahora + self.espera_s
            return
        if ok:
            self.fallos = 0
        else:
            self.fallos += 1
            if self.fallos >= self.umbral_fallos:
                self.estado = "abierto"
                self.abierto_hasta = ahora + self.espera_s

cb = Cortacircuitos()
for t in range(0, 9):
    if not cb.permite(t):
        print("t=%d  %-11s peticion rechazada sin llamar" % (t, cb.estado))
        continue
    ok = t >= 5                          # la dependencia se recupera en t=5
    cb.registra(ok, t)
    print("t=%d  %-11s llamada -> %s" % (t, cb.estado, "ok" if ok else "fallo"))
# -> t=4  abierto     llamada -> fallo
# -> t=5  abierto     peticion rechazada sin llamar
# -> t=6  cerrado     llamada -> ok
