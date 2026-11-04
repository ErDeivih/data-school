# En coma flotante, "acercarse" no es llegar: los numeros reales no se representan exactos.
print("0.1 + 0.2 - 0.3:", 0.1 + 0.2 - 0.3)                        # -> 5.551115123125783e-17
print("en notacion cientifica:", format(0.1 + 0.2 - 0.3, ".2e"))  # -> 5.55e-17
print("es exactamente cero:", 0.1 + 0.2 - 0.3 == 0.0)             # -> False
