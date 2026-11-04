# Precios de ejemplo en euros por millon de tokens: cámbialos por los de tu proveedor.
PRECIO_ENTRADA = 3.0     # tokens de entrada que no estan en cache
PRECIO_CACHE = 0.30      # tokens de entrada que si estan en cache
PRECIO_SALIDA = 15.0     # tokens generados

def coste(entrada_nueva, entrada_cache, salida):
    # los precios son por MILLON de tokens: el / 1e6 deja el resultado en euros por consulta
    return (entrada_nueva * PRECIO_ENTRADA + entrada_cache * PRECIO_CACHE
            + salida * PRECIO_SALIDA) / 1e6

# el orden de la tupla manda: sistema, historial, documentos y salida, en ese orden
sistema, historial, documentos, respuesta = 3000, 12000, 120000, 300

# sin cache: todo el prompt (prefijo + documentos) se paga a precio de entrada
sin_cache = coste(sistema + historial + documentos, 0, respuesta)
# con cache: el prefijo estable va en la ranura de cache; los documentos, que cambian
# en cada pregunta, van en la de entrada nueva
con_cache = coste(documentos, sistema + historial, respuesta)
# recortado: el mismo prefijo con 30.000 tokens de documentos en vez de 120.000
recortado = coste(30000, sistema + historial, respuesta)

print(f"sin cache            {sin_cache:.4f} EUR")
print(f"con cache            {con_cache:.4f} EUR")
print(f"con cache y 30k docs {recortado:.4f} EUR")
print(f"ahorro de la cache   {(1 - con_cache / sin_cache) * 100:.0f} %")
print(f"1000 consultas al dia con cache: {con_cache * 1000 * 30:.0f} EUR al mes")
