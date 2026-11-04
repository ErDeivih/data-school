import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Enero: el esquema original. Marzo: el mismo esquema mas una columna nueva.
enero = pd.DataFrame({"id": [1, 2], "importe": [10.5, 20.0]})
marzo = pd.DataFrame({"id": [3], "importe": [7.25], "canal": ["web"]})

# El productor no reescribe el fichero viejo: escribe el nuevo con una columna mas.
pq.write_table(pa.Table.from_pandas(enero, preserve_index=False), "enero.parquet")
pq.write_table(pa.Table.from_pandas(marzo, preserve_index=False), "marzo.parquet")

print("columnas de enero:", pq.read_schema("enero.parquet").names)
print("columnas de marzo:", pq.read_schema("marzo.parquet").names)
# La columna nueva no existe en lo ya escrito: no aparece sola al leer un fichero suelto.
try:
    pq.read_table("enero.parquet").column("canal")
except KeyError as exc:
    print("enero.parquet no trae canal:", type(exc).__name__)

# Al unir esquemas distintos, pandas decide por version: o rellena con nulo o se queja.
try:
    print("pandas concatena con nulos:", pd.concat([enero, marzo], ignore_index=True)
          .to_dict(orient="list"))
except Exception as exc:
    print("pandas no concatena:", type(exc).__name__)
# -> columnas de enero: ['id', 'importe']
# -> columnas de marzo: ['id', 'importe', 'canal']
# -> enero.parquet no trae canal: KeyError
# -> pandas concatena con nulos: {'id': [1, 2, 3], 'importe': [10.5, 20.0, 7.25], 'canal': [nan, nan, 'web']}

# Arrow si garantiza el relleno: unir por nombre y poner nulo donde falta la columna.
unido = pa.concat_tables([pa.Table.from_pandas(enero, preserve_index=False),
                          pa.Table.from_pandas(marzo, preserve_index=False)],
                         promote_options="default")
print("arrow si puede:", unido.to_pydict())
# -> arrow si puede: {'id': [1, 2, 3], 'importe': [10.5, 20.0, 7.25], 'canal': [None, None, 'web']}
