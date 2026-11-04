import pandas as pd

# Cada fila es un usuario identificable por codigo postal y fecha de nacimiento exacta.
eventos = pd.DataFrame({
    "usuario":    ["u1", "u2", "u3", "u4"],
    "cp":         ["28001", "28001", "28001", "28013"],
    "nacimiento": ["1980-03-02", "1980-03-02", "1991-07-15", "1975-11-30"],
})

# k-anonimato: cada combinacion de cuasi-identificadores debe aparecer al menos k veces.
conteo = eventos.groupby(["cp", "nacimiento"]).size()   # Serie con los grupos como indice
k = 2
print("combinaciones distintas:", len(conteo))          # len cuenta grupos, no filas
print("grupos con al menos", k, "filas:", int((conteo >= k).sum()), "de", len(conteo))   # True vale 1
print("filas en grupos pequenos:", int(eventos.shape[0] - conteo[conteo >= k].sum()))

# Generalizar la fecha al ano sube el tamano de los grupos.
generalizado = eventos.assign(anio=eventos.nacimiento.str.slice(0, 4))   # copia: no toca eventos
print("grupos por (cp, anio):", generalizado.groupby(["cp", "anio"]).size().to_dict())
