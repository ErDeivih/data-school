# Ley de la probabilidad total con las dos máquinas de la fábrica.
p_m1, p_m2 = 0.70, 0.30
p_def_m1, p_def_m2 = 0.02, 0.05

p_defectuosa = p_m1 * p_def_m1 + p_m2 * p_def_m2
aporte_m1 = p_m1 * p_def_m1
aporte_m2 = p_m2 * p_def_m2

print("P(defectuosa)      ", round(p_defectuosa, 4))       # salida: 0.029
print("aporta la maquina 1", round(aporte_m1, 4))          # salida: 0.014
print("aporta la maquina 2", round(aporte_m2, 4))          # salida: 0.015
print("promedio ingenuo   ", round((p_def_m1 + p_def_m2) / 2, 4))  # salida: 0.035
