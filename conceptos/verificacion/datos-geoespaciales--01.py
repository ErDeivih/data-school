import numpy as np

R = 6371.0088   # radio medio de la Tierra en kilometros


def haversine(lat1, lon1, lat2, lon2):
    """Distancia en km sobre la esfera; latitudes y longitudes en grados."""
    f1, f2 = np.radians(lat1), np.radians(lat2)
    df, dl = f2 - f1, np.radians(lon2 - lon1)
    a = np.sin(df / 2) ** 2 + np.cos(f1) * np.cos(f2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def plano(lat1, lon1, lat2, lon2):
    """Version tramposa: trata los grados como kilometros fijos."""
    dy, dx = (lat2 - lat1) * 111.32, (lon2 - lon1) * 111.32
    return float(np.hypot(dx, dy))


for nombre, p1, p2 in (("Madrid-Barcelona", (40.4168, -3.7038), (41.3874, 2.1686)),
                       ("Helsinki-Oslo", (60.1699, 24.9384), (59.9139, 10.7522))):
    real = float(haversine(*p1, *p2))
    mal = plano(*p1, *p2)
    print(f"{nombre:>16}  real {real:7.1f} km  plano {mal:7.1f} km"
          f"  error {100 * (mal / real - 1):5.1f} %")
# -> Madrid-Barcelona  real   505.1 km  plano   662.6 km  error  31.2 %
# ->    Helsinki-Oslo  real   786.7 km  plano  1579.5 km  error 100.8 %
