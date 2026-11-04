import pandas as pd

# Dos origenes en monedas distintas: sin convertir no se pueden sumar
crm = pd.DataFrame({"pais": ["ES", "FR"], "importe": [1200.0, 800.0], "moneda": ["EUR", "USD"]})
facturacion = pd.DataFrame({"pais": ["ES"], "importe": [300.0], "moneda": ["EUR"]})
todos = pd.concat([crm, facturacion], ignore_index=True)

# El tipo de cambio se guarda con la carga: sin el, el numero de manana no se puede reproducir
fx = {"EUR": 1.0, "USD": 0.92}
en_euros = todos.assign(eur=todos.importe * todos.moneda.map(fx))

print("suma sin convertir:", round(todos.importe.sum(), 2))        # -> suma sin convertir: 2300.0
print("suma integrada en euros:", round(en_euros.eur.sum(), 2))    # -> suma integrada en euros: 2236.0
print("filas del hecho:", len(en_euros))                          # -> filas del hecho: 3
