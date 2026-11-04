import numpy as np

# Version parametrica: cartera de 100 000 EUR con volatilidad diaria del 1,2 % y media 0.
capital, sigma_diaria = 100_000, 0.012
z = 1.6448536269514722                    # cuantil 95 % de la normal tipificada
phi = np.exp(-z ** 2 / 2) / np.sqrt(2 * np.pi)

var95 = z * sigma_diaria * capital
cvar95 = phi / 0.05 * sigma_diaria * capital
print(f"VaR  95% {var95:7.0f} EUR {z * sigma_diaria:.2%}")          # -> 1974 EUR  1.97%
print(f"CVaR 95% {cvar95:7.0f} EUR {phi / 0.05 * sigma_diaria:.2%}")  # -> 2475 EUR  2.48%
print(f"CVaR / VaR {cvar95 / var95:.2f}")                            # -> 1.25
