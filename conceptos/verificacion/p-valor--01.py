from scipy import stats

# 15 caras en 20 lanzamientos: cuanto de raro es si la moneda fuera justa
dos_colas = stats.binomtest(15, 20, p=0.5, alternative="two-sided")
una_cola = stats.binomtest(15, 20, p=0.5, alternative="greater")

print(f"p bilateral  {dos_colas.pvalue:.4f}")   # -> 0.0414
print(f"p unilateral {una_cola.pvalue:.4f}")    # -> 0.0207
print(f"casos con 15 o mas caras: {stats.binom.sf(14, 20, 0.5) * 2**20:.0f} de {2**20}")  # -> 21700 de 1048576
