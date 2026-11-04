import pandas as pd

aciertos = pd.Series([5, 6, 4, 5, 6, 4, 5, 3, 4, 3])

print(f"acumulada {aciertos.expanding().mean().iloc[-1]:.2f}")   # -> acumulada 4.50
print(f"ventana 3 {aciertos.rolling(3).mean().iloc[-1]:.2f}")     # -> ventana 3 3.33
print(f"ventana 5 {aciertos.rolling(5).mean().iloc[-1]:.2f}")     # -> ventana 5 3.80

print(aciertos.rolling(3).mean().round(2).tail(4).to_string(index=False))