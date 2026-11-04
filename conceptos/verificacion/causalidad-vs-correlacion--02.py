import numpy as np

# x e y no se causan entre si: los dos son consecuencia de z (el confusor).
rng = np.random.default_rng(0)
z = rng.normal(size=2000)
x = z + rng.normal(size=2000)
y = z + rng.normal(size=2000)

print(f"correlacion bruta       {np.corrcoef(x, y)[0, 1]:+.2f}")
# -> correlacion bruta       +0.49

# Al quitar de cada variable la parte explicada por z, la relacion desaparece.
sobra_x = x - np.polyval(np.polyfit(z, x, 1), z)
sobra_y = y - np.polyval(np.polyfit(z, y, 1), z)
print(f"correlacion quitando z  {np.corrcoef(sobra_x, sobra_y)[0, 1]:+.2f}")
# -> correlacion quitando z  -0.02
