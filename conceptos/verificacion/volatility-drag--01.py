import numpy as np

# 10.000 carteras de 10 anos, retorno mensual con media 8 % anual y volatilidad 25 % anual
rng = np.random.default_rng(5)
mensual = rng.normal(0.08 / 12, 0.25 / np.sqrt(12), (10_000, 120))
riqueza = np.prod(1 + mensual, axis=1)

print(f"media aritmetica mensual {mensual.mean():.4f}")    # -> media aritmetica mensual 0.0067
print(f"media log mensual {np.log1p(mensual).mean():.4f}")  # -> media log mensual 0.0041
print(f"mitad varianza {-0.5 * (0.25 / np.sqrt(12)) ** 2:.4f}")  # -> mitad varianza -0.0026
print(f"riqueza mediana {np.median(riqueza):.4f}")          # -> riqueza mediana 1.6520
print(f"riqueza media {riqueza.mean():.4f}")                # -> riqueza media 2.2326
print(f"tasa anualizada {np.median(riqueza) ** (1 / 10) - 1:.4f}")  # -> tasa anualizada 0.0515
print(f"exp(mu)-1 {np.exp(0.08) - 1:.4f}")                  # -> exp(mu)-1 0.0833