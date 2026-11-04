import pandas as pd

s = pd.Series([10.0, 30.0], index=pd.to_datetime(["2024-01-01", "2024-01-05"]))

print(s.asfreq("D").tolist())            # -> [10.0, nan, nan, nan, 30.0]
print(s.asfreq("D").index.freq)          # -> <Day>
print(s.resample("D").sum().tolist())    # -> [10.0, 0.0, 0.0, 0.0, 30.0]
print(s.loc["2024-01-01":"2024-01-02"].tolist())   # -> [10.0]  trocear por texto

# asfreq cambia la rejilla y DESCARTA lo que no cae en ella: aqui se pierden los tres datos
meses = pd.Series([1.0, 2.0, 3.0],
                  index=pd.to_datetime(["2024-01-05", "2024-02-10", "2024-03-20"]))
print(meses.asfreq("MS").tolist())       # -> [nan, nan]

# Una frecuencia anclada al calendario da las mismas etiquetas a dos series distintas...
primera = pd.Series(1.0, index=pd.date_range("2024-01-01", periods=10, freq="D"))
segunda = pd.Series(1.0, index=pd.date_range("2024-01-03", periods=10, freq="D"))
print([d.strftime("%m-%d") for d in primera.resample("W").sum().index])   # -> ['01-07', '01-14']
print([d.strftime("%m-%d") for d in segunda.resample("W").sum().index])   # -> ['01-07', '01-14']
# ...pero una de varios dias empieza a contar en el primer dato de cada serie
print([d.strftime("%m-%d") for d in primera.resample("7D").sum().index])  # -> ['01-01', '01-08']
print([d.strftime("%m-%d") for d in segunda.resample("7D").sum().index])  # -> ['01-03', '01-10']
