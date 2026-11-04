# La sensibilidad y la especificidad se quedan igual; la precision se hunde.
sensibilidad, especificidad = 0.85, 0.925
falso_positivo = 1 - especificidad

def vpp(prevalencia):
    """Valor predictivo positivo: la precision que se ve con esa prevalencia."""
    return (sensibilidad * prevalencia) / (
        sensibilidad * prevalencia + falso_positivo * (1 - prevalencia)
    )

print(f"prevalencia 0.200 -> VPP {vpp(0.20):.4f}")    # -> 0.7391
print(f"prevalencia 0.020 -> VPP {vpp(0.02):.4f}")    # -> 0.1878
print(f"prevalencia 0.005 -> VPP {vpp(0.005):.4f}")   # -> 0.0539
