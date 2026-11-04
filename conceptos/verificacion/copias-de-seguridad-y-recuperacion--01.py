# El plan de recuperacion son numeros, no una carpeta con ficheros.
tamano_gb, ancho_mb_s = 400, 120

minutos_copia = tamano_gb * 1024 / ancho_mb_s / 60
print("traer la copia completa: %.0f min" % minutos_copia)          # -> 57

# RTO: todo lo que pasa desde que se rompe hasta que el usuario vuelve.
fases = [("deteccion", 8), ("decision", 5), ("aprovisionar", 15),
         ("restaurar", minutos_copia), ("reproducir registros", 40),
         ("verificar", 25)]
for nombre, m in fases:
    print("  %-22s %5.0f min" % (nombre, m))
total = sum(m for _, m in fases)
print("RTO total: %.0f min (%.1f h)" % (total, total / 60))        # -> 150 min (2.5 h)

# RPO: cuanto dato se pierde con cada frecuencia de copia.
pedidos_dia = 3000
for rpo_min in (1440, 60, 15, 5):
    print("RPO %4d min -> hasta %6.1f pedidos perdidos" % (rpo_min, pedidos_dia * rpo_min / 1440))
# -> RPO 1440 min -> hasta 3000.0 pedidos perdidos
# -> RPO    5 min -> hasta   10.4 pedidos perdidos
