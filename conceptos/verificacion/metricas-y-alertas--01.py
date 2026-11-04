# --- inicio formula 1 ---
# De un SLO salen DOS presupuestos distintos y no son intercambiables.
slo = 0.999
ventana_dias = 30
rps = 10

error_permitido = 1 - slo
segundos_ventana = ventana_dias * 86400
eventos_totales = rps * segundos_ventana
# El presupuesto en tiempo es la fraccion del mes que puedes estar fallando: 0,001 * 30 dias.
minutos_presupuesto = error_permitido * ventana_dias * 24 * 60
# El presupuesto en peticiones es esa misma fraccion sobre el trafico.
peticiones_presupuesto = error_permitido * eventos_totales
# --- fin formula 1 ---

print("error permitido: %.4f" % error_permitido)               # -> 0.0010
print("eventos en la ventana:", eventos_totales)               # -> 25920000
print("presupuesto en minutos: %.1f" % minutos_presupuesto)    # -> 43.2
print("presupuesto en peticiones: %.0f" % peticiones_presupuesto)  # -> 25920
