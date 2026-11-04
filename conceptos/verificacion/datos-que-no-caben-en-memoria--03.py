import os
import tempfile

import polars as pl
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

with tempfile.TemporaryDirectory() as carpeta:
    # Dos ficheros Parquet, como los dejaria un proceso que escribe por lotes
    for i in range(2):
        tabla = pa.table({"ciudad": ["ES"] * 3 + ["FR"] * 2,
                          "importe": [1.0, 2.0, 3.0, 4.0, 5.0]})
        pq.write_table(tabla, os.path.join(carpeta, f"parte-{i}.parquet"))

    # pyarrow.dataset: el filtro se evalua en el lector y los lotes se piden de uno en uno
    conjunto = ds.dataset(carpeta, format="parquet")
    print(conjunto.count_rows(filter=ds.field("importe") > 2))   # -> 6
    print([l.num_rows for l in conjunto.scanner(batch_size=3).to_batches()])
    # -> [3, 2, 3, 2]  el tamano de lote se aplica a cada fichero por separado

    # Polars: scan_parquet no lee nada hasta que se pide el resultado
    perezoso = pl.scan_parquet(os.path.join(carpeta, "*.parquet"))
    print(type(perezoso).__name__)                              # -> LazyFrame
    print(perezoso.group_by("ciudad").agg(pl.col("importe").sum()).sort("ciudad")
          .collect(engine="streaming").to_dict(as_series=False))
    # -> {'ciudad': ['ES', 'FR'], 'importe': [12.0, 18.0]}
    try:
        perezoso.collect(streaming=True)                        # en Polars 2.x ya no existe
    except Exception as e:
        print(type(e).__name__)                                 # -> ArgumentRemovedError
