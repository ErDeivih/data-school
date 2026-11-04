import numpy as np

# Modelo de coste por GB y mes: almacen fijo + precio por operacion de lectura.
# Cifras de ejemplo en unidades relativas: la forma de las curvas es lo que se traslada
# a cualquier proveedor, no los numeros exactos.
almacen = {"caliente": 1.00, "frio": 0.50, "archivo": 0.20}
lectura = {"caliente": 0.0005, "frio": 0.005, "archivo": 0.020}

# Cuantas lecturas al mes hacen que dejar de usar la clase caliente salga a cuenta:
# se igualan los dos costes y se despeja n.
cruce1 = (almacen["caliente"] - almacen["frio"]) / (lectura["frio"] - lectura["caliente"])
cruce2 = (almacen["frio"] - almacen["archivo"]) / (lectura["archivo"] - lectura["frio"])
print(f"caliente = frio a las {cruce1:.0f} lecturas por GB al mes")   # -> 111
print(f"frio = archivo a las {cruce2:.0f} lecturas por GB al mes")    # -> 20

for n in (10, 200, 5000):
    coste = {k: almacen[k] + lectura[k] * n for k in almacen}
    print(f"{n:>5} lecturas/GB  " + "  ".join(f"{k} {v:.2f}" for k, v in coste.items())
          + f"  -> {min(coste, key=coste.get)}")
# -> 10 lecturas/GB  caliente 1.00  frio 0.55  archivo 0.40  -> archivo
# -> 200 lecturas/GB  caliente 1.10  frio 1.50  archivo 4.20  -> caliente
# -> 5000 lecturas/GB  caliente 3.50  frio 25.50  archivo 100.20  -> caliente
