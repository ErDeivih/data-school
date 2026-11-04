import pandas as pd

UMBRAL = 0.20        # mas alla de esto, el lote no se escribe

def revisar(lote):
    """Devuelve (buenos, rechazados) con el motivo de cada rechazo."""
    motivos = []
    for _, f in lote.iterrows():
        fallos = []
        if not f["unidades"] > 0:
            fallos.append("unidades no positivas")
        if pd.isna(f["precio"]) or f["precio"] <= 0:
            fallos.append("precio vacio o no positivo")
        if "@" not in str(f["email"]):
            fallos.append("email sin arroba")
        motivos.append("; ".join(fallos))
    lote = lote.assign(motivo=motivos)
    return lote[lote["motivo"] == ""], lote[lote["motivo"] != ""]

def procesar(nombre, lote):
    buenos, malos = revisar(lote)
    tasa = len(malos) / len(lote)
    print(f"{nombre}: {len(malos)} rechazados de {len(lote)} ({tasa:.1%})")
    if tasa > UMBRAL:
        print("  -> por encima del umbral: 0 filas escritas y el pipeline se para")
    else:
        print("  -> por debajo del umbral:", len(buenos), "filas a la tabla y", len(malos), "a cuarentena")
    return buenos, malos

sucio = pd.DataFrame({
    "pedido_id": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
    "unidades": [2, 1, -3, 4, 0, 7, 2, 5],
    "precio": [10.0, 5.0, 20.0, None, 8.0, 12.0, 9.0, 0.0],
    "email": ["a@x.es", "b@x.es", "c@x.es", "d@x.es", "sin-arroba", "f@x.es", "g@x.es", "h@x.es"],
})
normal = pd.DataFrame({
    "pedido_id": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
    "unidades": [2, 1, 3, 4, 1, 7, 2, 5],
    "precio": [10.0, 5.0, 20.0, None, 8.0, 12.0, 9.0, 1.0],
    "email": ["a@x.es", "b@x.es", "c@x.es", "d@x.es", "e@x.es", "f@x.es", "g@x.es", "h@x.es"],
})

procesar("tanda sucia", sucio)
print()
buenos, malos = procesar("tanda normal", normal)
print(malos[["pedido_id", "motivo"]].to_string(index=False))
