# Presupuesto de parametros: W (d x k) frente a B (d x r) y A (r x k).
for d, k, nombre in ((768, 768, "atencion"), (768, 3072, "MLP")):
    completo = d * k
    for r in (4, 8, 16):
        lora = r * (d + k)              # B y A juntas
        print(f"{nombre:>8} {d}x{k}  r={r:>2}  completo={completo:>8}"
              f"  LoRA={lora:>6}  {lora / completo:.4%}")
# El formato :.4% multiplica por 100 y anade el signo de porcentaje; no es lo mismo que
# :.4f, que daria 0.0208 en vez de 2.0833%.
# -> atencion 768x768  r= 4  completo=  589824  LoRA=  6144  1.0417%
# -> atencion 768x768  r= 8  completo=  589824  LoRA= 12288  2.0833%
# -> atencion 768x768  r=16  completo=  589824  LoRA= 24576  4.1667%
# ->      MLP 768x3072  r= 4  completo= 2359296  LoRA= 15360  0.6510%
# ->      MLP 768x3072  r= 8  completo= 2359296  LoRA= 30720  1.3021%
# ->      MLP 768x3072  r=16  completo= 2359296  LoRA= 61440  2.6042%
