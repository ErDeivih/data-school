# Buscar en texto plano es lo unico que encuentra una nota que no recuerdas haber escrito.
# Fijate en la segunda busqueda: la nota existe, pero con otras palabras, y no aparece.
notas = [
    ("bom-en-la-primera-columna",
     "El nombre de la primera columna sale con caracteres raros: el CSV empieza con BOM. Abrir con utf-8-sig."),
    ("leer-400-csv-tarda-9-minutos",
     "Leer 400 CSV tardaba 9 minutos; el mismo dato en Parquet, 12 segundos."),
    ("nulos-en-el-join",
     "LEFT JOIN en SQL: los nulos del lado derecho no son ceros al sumar."),
]

def buscar(notas, consulta):
    c = consulta.lower()
    return [titulo for titulo, texto in notas if c in texto.lower() or c in titulo]

print("buscar 'bom'      :", buscar(notas, "bom"))
print("buscar 'va lento' :", buscar(notas, "va lento"))
print("buscar 'tarda'    :", buscar(notas, "tarda"))
