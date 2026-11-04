# Leer el libro y calcular lo que de verdad cuesta una orden a mercado.
bids = [(50.00, 1200), (49.99, 3000), (49.98, 6000), (49.97, 9000)]
asks = [(50.01, 900), (50.02, 2500), (50.03, 4000), (50.04, 8000)]

bid, ask = bids[0][0], asks[0][0]
mid = (bid + ask) / 2

# Un solo nivel frente a tres: el desequilibrio cambia segun la profundidad mirada.
q_b1 = sum(q for _, q in bids[:1]); q_a1 = sum(q for _, q in asks[:1])
q_b3 = sum(q for _, q in bids[:3]); q_a3 = sum(q for _, q in asks[:3])

print("spread en pb :", round((ask - bid) / mid * 10000, 2))              # -> 2.0
print("imbalance 1  :", round((q_b1 - q_a1) / (q_b1 + q_a1), 4))          # -> 0.1429
print("imbalance 3  :", round((q_b3 - q_a3) / (q_b3 + q_a3), 4))          # -> 0.1591

def ejecutar(Q, niveles):
    """Recorre los niveles de arriba abajo: precio medio y cantidad sin ejecutar."""
    resta, gastado = Q, 0.0
    for precio, cantidad in niveles:
        usa = min(resta, cantidad)
        gastado += usa * precio
        resta -= usa
        if resta == 0:
            break
    ejecutado = Q - resta
    return gastado / ejecutado, resta

medio, resto = ejecutar(10000, asks)
print("precio medio :", round(medio, 4))                    # -> 50.0283
print("impacto en pb:", round((medio - ask) / mid * 10000, 2))   # -> 3.66
print("sin ejecutar :", resto)                              # -> 0
