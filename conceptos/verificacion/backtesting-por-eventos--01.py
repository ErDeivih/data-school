# Cola y ejecucion parcial: la diferencia entre "toco el precio" y "me ejecutan".
cola_por_delante = 300
orden = 500
ejecutado = 0
cola = cola_por_delante

for venta in (400, 250):          # volumen que llega contra nuestro nivel de precio
    consume_cola = min(cola, venta)
    cola -= consume_cola
    disponible = venta - consume_cola
    llena = min(orden - ejecutado, disponible)
    ejecutado += llena
    print(f"venta de {venta:>3} -> cola delante {cola:>3}  ejecutado {ejecutado:>3} de {orden}")
# -> venta de 400 -> cola delante   0  ejecutado 100 de 500
# -> venta de 250 -> cola delante   0  ejecutado 350 de 500

print(f"parcial: {ejecutado} de {orden} ({ejecutado / orden:.0%})")   # -> parcial: 350 de 500 (70%)
