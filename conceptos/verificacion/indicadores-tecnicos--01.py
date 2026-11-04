import pandas as pd

serie = pd.Series([10, 11, 10, 12, 11, 13, 12, 14])

sma3 = serie.rolling(3).mean()
delta = serie.diff()
subidas = delta.clip(lower=0).rolling(3).mean()
bajadas = (-delta.clip(upper=0)).rolling(3).mean()
rsi3 = 100 - 100 / (1 + subidas / bajadas)

print(f"sma3 ultimo {sma3.iloc[-1]:.2f}")   # -> sma3 ultimo 13.00
print(f"rsi3 ultimo {rsi3.iloc[-1]:.2f}")   # -> rsi3 ultimo 80.00