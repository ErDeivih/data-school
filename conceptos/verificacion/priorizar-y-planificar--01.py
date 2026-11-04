import pandas as pd

# Cuatro iniciativas: el coste del retraso son cuatro componentes que se suman,
# y el tamano (o la duracion) dividen. Todo en unidades relativas, como se hace de verdad.
iniciativas = pd.DataFrame({
    "iniciativa": ["arreglar el cobro", "informes nuevos", "migrar la base", "buscador"],
    "valor_negocio": [8, 5, 3, 5],
    "criticidad_temporal": [5, 0, 1, 0],
    "riesgo": [3, 1, 5, 0],
    "habilitacion": [2, 1, 3, 1],
    "tamano": [2, 5, 8, 3],
    "duracion_semanas": [1, 3, 10, 4],
})
componentes = ["valor_negocio", "criticidad_temporal", "riesgo", "habilitacion"]
iniciativas["coste_retraso"] = iniciativas[componentes].sum(axis=1)

# WSJF mide el coste de la cola (divide por tamano); CD3, el coste del reloj (por duracion).
iniciativas["wsjf"] = (iniciativas.coste_retraso / iniciativas.tamano).round(2)
iniciativas["cd3"] = (iniciativas.coste_retraso / iniciativas.duracion_semanas).round(2)
print(iniciativas[["iniciativa", "coste_retraso", "tamano", "wsjf", "cd3"]].to_string(index=False))
print("por WSJF:", list(iniciativas.sort_values("wsjf", ascending=False).iniciativa))
# -> por WSJF: ['arreglar el cobro', 'buscador', 'migrar la base', 'informes nuevos']
print("por CD3: ", list(iniciativas.sort_values("cd3", ascending=False).iniciativa))
# -> por CD3:  ['arreglar el cobro', 'informes nuevos', 'buscador', 'migrar la base']
