import numpy as np

# Cola del 5 % de un historico de 250 dias: las 13 mayores perdidas diarias de una
# cartera de 100 000 EUR, escritas en euros.
cola = np.array([1250, 1400, 1500, 1650, 1800, 2000, 2200,
                 2500, 2700, 3000, 3400, 3900, 4800], dtype=float)
capital = 100_000

var95 = cola.min()          # umbral: la menor de las perdidas de la cola
cvar95 = cola.mean()        # perdida media de todo lo que queda por encima

print(f"cola {cola.size} de 250 dias")                # -> cola 13 de 250 dias
print(f"VaR  95% {var95:7.0f} EUR {var95 / capital:.2%}")     # -> 1250 EUR  1.25%
print(f"CVaR 95% {cvar95:7.0f} EUR {cvar95 / capital:.2%}")   # -> 2469 EUR  2.47%
print(f"CVaR / VaR {cvar95 / var95:.2f}")             # -> 1.98
