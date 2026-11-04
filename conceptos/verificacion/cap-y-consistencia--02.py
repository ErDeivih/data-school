# Lectura en una replica que va por detras del lider: la garantia de sesion lo evita.
escritura_ms, retraso_replica_ms = 100, 400

for t in (50, 150, 300, 450, 700):
    # La replica ha aplicado todo lo anterior a (t - retraso): la comparacion devuelve un bool.
    visible = t - retraso_replica_ms >= escritura_ms
    print(f"t={t:>4} ms  la replica ya ve la escritura: {visible}")

print("la escritura se ve a partir de:", escritura_ms + retraso_replica_ms, "ms")   # -> 500 ms
