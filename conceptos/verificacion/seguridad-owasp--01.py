import sqlite3

con = sqlite3.connect(":memory:")        # base en RAM: no crea fichero y se pierde al terminar
con.execute("CREATE TABLE usuarios (email TEXT, rol TEXT)")
con.execute("INSERT INTO usuarios VALUES ('ana@ejemplo.es', 'admin')")

# MAL: la consulta se construye pegando el texto que llega del usuario.
email = "x' OR '1'='1"                   # la comilla suelta cierra el literal de la consulta
mala = f"SELECT email, rol FROM usuarios WHERE email = '{email}'"   # el dato acaba dentro del SQL
print("concatenando:", len(con.execute(mala).fetchall()), "filas (esperabamos 0)")

# BIEN: el valor viaja como parametro y el motor lo trata como dato, no como SQL.
buena = "SELECT email, rol FROM usuarios WHERE email = ?"
print("con parametro:", len(con.execute(buena, (email,)).fetchall()), "filas")
print("usuario real  :", con.execute(buena, ("ana@ejemplo.es",)).fetchall())   # la coma hace la tupla
