# Esquema evolutivo: un fichero nuevo anade una columna y los antiguos se leen con nulo
ficheros = {
    "f_antiguo": [{"id": 1, "ciudad": "Madrid"}, {"id": 2, "ciudad": "Sevilla"}],
    "f_nuevo": [{"id": 3, "ciudad": "Bilbao", "segmento": "premium"}],
}
columnas = ["id", "ciudad", "segmento"]      # el esquema de la tabla, no el de cada fichero

filas = [{c: fila.get(c) for c in columnas} for contenido in ficheros.values() for fila in contenido]
print("filas leidas:", len(filas))                                          # -> filas leidas: 3
print("filas sin segmento:", sum(f["segmento"] is None for f in filas))     # -> filas sin segmento: 2
print("columnas del esquema:", ",".join(columnas))                          # -> columnas del esquema: id,ciudad,segmento
