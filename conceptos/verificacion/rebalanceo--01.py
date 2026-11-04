# El desvio se ve con un solo movimiento grande: la bolsa sube un 50 %.
v_eq, v_bd = 60000.0, 40000.0
v_eq *= 1.50
total = v_eq + v_bd
print("valor de la cartera:", total)                                            # -> valor de la cartera: 130000.0
print("peso de la bolsa:", round(v_eq / total, 4))                              # -> peso de la bolsa: 0.6923
print("desvio en puntos porcentuales:", round(100 * (v_eq / total - 0.60), 1))  # -> desvio en puntos porcentuales: 9.2
print("notional que cambia de manos:", abs(0.60 * total - v_eq))                # -> notional que cambia de manos: 12000.0
coste = abs(0.60 * total - v_eq) * 0.0005 * 2                                   # 5 pb por cada pata
print("coste del rebalanceo:", coste)                                           # -> coste del rebalanceo: 12.0
print("en porcentaje de la cartera:", round(100 * coste / total, 4))            # -> en porcentaje de la cartera: 0.0092
