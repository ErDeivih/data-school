# Cuenta de parametros de un modelo tipo transformer, capa por capa.
# Se supone que la proyeccion de salida reutiliza la matriz de entrada (pesos atados).
vocab, d, capas, contexto = 50257, 768, 12, 1024   # asignacion multiple: cuatro variables de golpe

embed = vocab * d
posiciones = contexto * d
por_capa = 4 * d * d + 8 * d * d + 4 * d   # atencion + MLP (d -> 4d -> d) + dos LayerNorm

total = embed + posiciones + capas * por_capa   # suma de los tres bloques
print(f"embedding            {embed:,}")        # -> 38,597,376
print(f"posiciones           {posiciones:,}")   # -> 786,432
print(f"atencion + MLP       {por_capa:,} por capa")   # -> 7,080,960 por capa
print(f"total                {total:,}")        # -> 124,355,328

# La atencion y el MLP crecen con d al cuadrado: duplicar d cuadruplica esa parte
print("factor al duplicar d:", 12 * (2 * d) ** 2 // (12 * d ** 2))   # -> 4
