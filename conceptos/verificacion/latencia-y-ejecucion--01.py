# Presupuesto de latencia: cuanto del edge se come un retardo concreto
precio = 100.00
edge_bps = 5.0                       # ventaja esperada, en puntos basicos
deriva_por_ms = 0.00005 / 10         # el precio se mueve 0,05 pb por milisegundo

edge = precio * edge_bps / 10000     # ventaja en EUR por accion

for latencia_ms in (1, 5, 20, 100):
    adverso = precio * deriva_por_ms * latencia_ms
    queda = 100 * (1 - adverso / edge)
    print(f"{latencia_ms:>4} ms: coste adverso {adverso:.4f} EUR de {edge:.4f} EUR de edge, queda {queda:.1f} %")
# ->    1 ms: coste adverso 0.0005 EUR de 0.0500 EUR de edge, queda 99.0 %
# ->    5 ms: coste adverso 0.0025 EUR de 0.0500 EUR de edge, queda 95.0 %
# ->   20 ms: coste adverso 0.0100 EUR de 0.0500 EUR de edge, queda 80.0 %
# ->  100 ms: coste adverso 0.0500 EUR de 0.0500 EUR de edge, queda 0.0 %
