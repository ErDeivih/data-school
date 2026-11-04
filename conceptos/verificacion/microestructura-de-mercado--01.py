# Recorrer el libro para saber a que precio se ejecuta de verdad una orden a mercado.
bids = [(100.00, 400), (99.99, 700), (99.98, 900), (99.97, 1500)]
asks = [(100.01, 300), (100.02, 600), (100.03, 1200), (100.04, 2000)]

bid, ask = bids[0][0], asks[0][0]
mid = (bid + ask) / 2
q_bid, q_ask = bids[0][1], asks[0][1]

print("spread            :", round(ask - bid, 4))            # -> 0.01
print("mid               :", round(mid, 4))                  # -> 100.005
print("spread en pb      :", round((ask - bid) / mid * 10000, 3))   # -> 1.0
print("desequilibrio     :", round((q_bid - q_ask) / (q_bid + q_ask), 4))   # -> 0.1429

def precio_medio_compra(Q, niveles):
    """Consume niveles de venta de arriba a abajo y devuelve (precio medio, sin ejecutar)."""
    resta, gastado = Q, 0.0
    for precio, cantidad in niveles:
        usa = min(resta, cantidad)
        gastado += usa * precio
        resta -= usa
        if resta == 0:
            break
    return gastado / (Q - resta), resta

medio, resto = precio_medio_compra(800, asks)
print("precio medio 800  :", round(medio, 5))     # -> 100.01625
print("impacto en euros  :", round(800 * (medio - ask), 2))   # -> 5.0
print("sin ejecutar 5000 :", precio_medio_compra(5000, asks)[1])   # -> 900
