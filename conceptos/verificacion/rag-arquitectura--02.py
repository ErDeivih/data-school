# Techo de un pipeline de RAG: la generacion no puede arreglar lo que no se recupero.
# Los dos porcentajes son supuestos del ejemplo, no resultados medidos.
recall_20 = 0.92      # el fragmento correcto esta entre los 20 recuperados
rerank_5 = 0.85       # el reordenador lo mantiene en el top-5
print(f"techo del sistema {recall_20 * rerank_5:.2f}")     # -> 0.78

# Coste en prompt segun cuantos fragmentos se envian al modelo
por_fragmento = 400   # tokens medios por fragmento
print(f"20 fragmentos -> {20 * por_fragmento} tokens")     # -> 8000 tokens
print(f" 5 fragmentos -> {5 * por_fragmento} tokens")      # -> 2000 tokens
