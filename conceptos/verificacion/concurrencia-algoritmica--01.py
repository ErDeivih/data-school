import threading

# Intercalado forzado con eventos: el "lost update" se reproduce siempre, no por suerte.
contador = [0]
ha_leido = threading.Event()
puede_escribir = threading.Event()

def hilo_a():
    valor = contador[0]           # A lee 0
    ha_leido.set()                # avisa de que ya ha leido
    puede_escribir.wait()         # y espera a que B escriba
    contador[0] = valor + 1       # A escribe 1: pisa el 1 que dejo B

def hilo_b():
    ha_leido.wait()
    contador[0] = contador[0] + 1     # B lee 0 y escribe 1
    puede_escribir.set()

a = threading.Thread(target=hilo_a)
b = threading.Thread(target=hilo_b)
a.start(); b.start(); a.join(); b.join()

print("incrementos pedidos:", 2)                        # -> 2
print("valor final:", contador[0])                      # -> 1
print("se ha perdido un incremento:", contador[0] != 2)  # -> True
