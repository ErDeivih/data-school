# La misma carga a distintas frecuencias: cuanto cuesta la frescura.
eventos_por_hora = 10_800_000        # 3.000 eventos por segundo
coste_arranque = 0.05                # euros por ejecucion del trabajo
coste_por_evento = 0.0000004         # euros por evento (0,40 EUR por millon)

variable = eventos_por_hora * coste_por_evento
print(f"{'frecuencia':>12} {'latencia':>9} {'coste/h':>8}")
for nombre, f in [("cada hora", 1), ("cada 15 min", 4), ("cada 5 min", 12), ("cada minuto", 60)]:
    print(f"{nombre:>12} {60 / f:>7.0f} m {f * coste_arranque + variable:>7.2f} EUR")

print("coste variable por hora:", round(variable, 2))   # -> coste variable por hora: 4.32
print("arranques al dia a 1 min:", 60 * 24)             # -> arranques al dia a 1 min: 1440
