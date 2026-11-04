# --- inicio formula 3 ---
# Cardinalidad: cada etiqueta MULTIPLICA las series, no las suma.
metricas_base = 20
endpoints, regiones, metodos = 5, 3, 4

sin_usuario = metricas_base * endpoints * regiones * metodos
con_cien_usuarios = sin_usuario * 100
con_cien_mil_usuarios = sin_usuario * 100_000
# --- fin formula 3 ---

print("series sin etiqueta de usuario:", sin_usuario)             # -> 1200
print("con 100 usuarios distintos:", con_cien_usuarios)           # -> 120000
print("con 100.000 usuarios:", f"{con_cien_mil_usuarios:,}")      # -> 120,000,000
print("factor de crecimiento:", con_cien_mil_usuarios // sin_usuario)  # -> 100000
