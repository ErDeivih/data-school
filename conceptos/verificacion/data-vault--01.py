import hashlib
import pandas as pd

# Lo que manda el origen: una foto por carga, con la ciudad que el CRM conoce ese dia
origen = pd.DataFrame({
    "load_date": ["2024-01-10", "2024-03-02", "2024-06-15", "2024-09-01"],
    "id_cliente": [42, 42, 42, 42],
    "ciudad": ["Madrid", "Barcelona", "Barcelona", "Valencia"],
})

def hashdiff(fila):
    return hashlib.md5("|".join(str(v) for v in fila).encode()).hexdigest()[:8]

satelite = []
for _, fila in origen.iterrows():
    h = hashdiff([fila.id_cliente, fila.ciudad])
    if not satelite or h != satelite[-1]["hashdiff"]:    # solo inserta si algo cambio
        satelite.append({"load_date": fila.load_date, "ciudad": fila.ciudad, "hashdiff": h})

print("llegadas:", len(origen), " filas del satelite:", len(satelite))
# -> llegadas: 4  filas del satelite: 3
for f in satelite:
    print(f["load_date"], f["ciudad"], f["hashdiff"])
# -> 2024-01-10 Madrid a280015e
# -> 2024-03-02 Barcelona 39e607fe
# -> 2024-09-01 Valencia 375ab662
