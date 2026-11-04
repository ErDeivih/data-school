import duckdb

con = duckdb.connect()
con.sql("""
    CREATE TABLE ventas (ciudad VARCHAR, importe DECIMAL(10,2));
    INSERT INTO ventas VALUES
        ('Madrid',  75.00), ('Madrid', 150.00),
        ('Sevilla', 25.00), ('Sevilla', 400.00),
        ('Bilbao',  30.00), ('Bilbao',  NULL);
""")

filas, con_importe, total, media = con.sql(
    "SELECT COUNT(*), COUNT(importe), SUM(importe), AVG(importe) FROM ventas"
).fetchone()

# COUNT(*) cuenta filas; los agregados de importe se saltan el nulo.
print(f"filas {filas}  con_importe {con_importe}  total {total}  media {media:.2f}")
# -> filas 6  con_importe 5  total 680.00  media 136.00

# La media por pedido (todos) no es la media por importe presente.
por_pedido = con.sql("SELECT ROUND(SUM(importe) / COUNT(*), 2) FROM ventas").fetchone()[0]
print(f"media por pedido {por_pedido}")   # -> media por pedido 113.33
