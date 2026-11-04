import pandas as pd

# La misma variable calculada por dos caminos: es el sesgo que busca el feature store.
pedidos = pd.DataFrame({
    "cliente": [1, 1, 1, 2, 2, 2, 3],
    "importe": [20.0, 40.0, 100.0, 10.0, 50.0, 90.0, 15.0],
    "estado":  ["ok", "ok", "devuelto", "ok", "ok", "ok", "ok"],
})

# Offline (dbt, para entrenar): media de todos los pedidos, devueltos incluidos.
offline = pedidos.groupby("cliente")["importe"].mean()
# Online (el servicio): filtra los devueltos, que es lo que hace el negocio.
online = pedidos[pedidos["estado"] == "ok"].groupby("cliente")["importe"].mean()

comparacion = pd.DataFrame({"offline": offline, "online": online})
# El denominador es el valor servido, en valor absoluto y con un suelo para no dividir por cero:
# es la misma formula que la definicion de arriba.
comparacion["desviacion"] = ((comparacion["offline"] - comparacion["online"]).abs()
                             / comparacion["online"].abs().clip(lower=1e-9))
print("clientes con desviacion > 1 %:", int((comparacion["desviacion"] > 0.01).sum()))  # -> 1
print(f"desviacion del cliente 1: {comparacion.loc[1, 'desviacion']:.1%}")              # -> 77.8%
