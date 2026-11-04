import numpy as np

vivos = np.array([8.0, 6.0, 10.0, 4.0, 7.0, 9.0])
muertos = np.array([-20.0, -12.0, -8.0, -15.0])
cohorte = np.concatenate([vivos, muertos])

print(f"media de los vivos   {vivos.mean():+.2f} %")        # -> +7.33 %
print(f"media de la cohorte  {cohorte.mean():+.2f} %")      # -> -1.10 %
print(f"sesgo                {vivos.mean() - cohorte.mean():+.2f} pp")  # -> +8.43 pp
print(f"fondos que faltan    {muertos.size} de {cohorte.size}")          # -> 4 de 10
