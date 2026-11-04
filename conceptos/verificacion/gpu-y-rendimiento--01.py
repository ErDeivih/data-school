# Cuentas de pizarra: el tamano del lote decide si el nucleo calcula o espera.
B, D_in, D_out = 64, 1024, 4096
flops = 2 * B * D_in * D_out
bytes_pesos = D_in * D_out * 4                # float32: 4 bytes por parametro

print(f"FLOPs           {flops / 1e9:.3f} GFLOP")            # -> 0.537 GFLOP
# 2**20 vale 1048576: esto son MiB (potencias de 1024) y no MB (potencias de 1000)
print(f"pesos          {bytes_pesos / 2**20:.1f} MiB")       # -> 16.0 MiB
print(f"intensidad     {flops / bytes_pesos:.1f} FLOP/byte")  # -> 32.0 FLOP/byte

# Con lote de 1 se leen los mismos pesos y se hace 64 veces menos calculo.
print(f"lote  1: {2 * 1 * D_in * D_out / bytes_pesos:.2f} FLOP/byte")   # -> 0.50 FLOP/byte
print(f"lote 64: {2 * 64 * D_in * D_out / bytes_pesos:.2f} FLOP/byte")  # -> 32.00 FLOP/byte
