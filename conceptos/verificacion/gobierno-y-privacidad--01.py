import pandas as pd

# Dataset "anonimizado": sin nombre, pero con cuasi-identificadores.
anonimo = pd.DataFrame({
    "id":   range(1, 9),
    "cp":   ["28001", "28001", "28001", "28013", "28013", "28013", "28040", "28040"],
    "edad": [34, 41, 29, 35, 52, 47, 61, 34],
    "sexo": ["M", "M", "F", "F", "F", "M", "F", "F"],
})

# Un censo publico del mismo municipio con los mismos tres campos.
censo = pd.DataFrame({
    "cp": anonimo["cp"], "edad": anonimo["edad"], "sexo": anonimo["sexo"],
    "nombre": ["Ana", "Luis", "Marta", "Pablo", "Sara", "Hugo", "Elena", "Nuria"],
})

unido = anonimo.merge(censo, on=["cp", "edad", "sexo"], how="left")
candidatos = unido.groupby("id")["nombre"].nunique()
print("registros con un unico candidato:", int((candidatos == 1).sum()), "de", len(candidatos))  # -> registros con un unico candidato: 8 de 8

# k-anonimato: tamano del grupo mas pequeno de cada combinacion de cuasi-identificadores.
grupos = anonimo.groupby(["cp", "edad", "sexo"]).size()
print("k sin generalizar:", int(grupos.min()))    # -> k sin generalizar: 1

# Generalizando a provincia y sexo se llega a k=3, a costa de perder edad y localidad.
grupos2 = anonimo.assign(prov=anonimo["cp"].str[:2]).groupby(["prov", "sexo"]).size()
print("k por provincia y sexo:", int(grupos2.min()))    # -> k por provincia y sexo: 3
