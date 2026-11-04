import sys
import threading
import time

sys.setswitchinterval(1e-6)     # cambios de hilo frecuentes: la carrera se ve antes

class Contador:
    def __init__(self):
        self.valor = 0
        self.lock = threading.Lock()

    def sin_bloqueo(self):
        actual = self.valor            # leer
        # sleep(0) no cambia el valor: solo pide al sistema que cambie de hilo, y ahi se cuela
        time.sleep(0)                  # el hilo puede perder el turno justo aqui
        self.valor = actual + 1        # escribir: la suma del otro hilo se ha perdido

    def con_bloqueo(self):
        with self.lock:                # el candado se suelta al salir, aunque salte una excepcion
            actual = self.valor
            time.sleep(0)              # dentro del candado, nadie mas puede leer a medias
            self.valor = actual + 1

def lanzar(metodo, veces=500):
    for _ in range(veces // 4):                                       # 125 tandas de 4 hilos
        hilos = [threading.Thread(target=metodo) for _ in range(4)]   # hilos nuevos cada vez
        for h in hilos:
            h.start()                   # start arranca; no espera a que el hilo acabe
        for h in hilos:
            h.join()                    # join si espera: sin el, se contarian hilos a medias

contador = Contador()
lanzar(contador.sin_bloqueo)
print("esperado 500, conseguido:", contador.valor, "(carrera: se pierden sumas)")

contador = Contador()
lanzar(contador.con_bloqueo)
print("con bloqueo, conseguido:", contador.valor)     # -> 500
