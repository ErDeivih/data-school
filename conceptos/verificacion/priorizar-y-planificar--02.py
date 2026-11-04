# Ley de Little: el tiempo de ciclo no lo fija el esfuerzo, lo fija el trabajo en curso.
TERMINADOS = 3.5
for wip in (4, 6, 12, 20):
    print("WIP %2d -> tiempo de ciclo %.1f semanas" % (wip, wip / TERMINADOS))
# -> WIP 12 -> tiempo de ciclo 3.4 semanas
# -> WIP  6 -> tiempo de ciclo 1.7 semanas

# Utilizacion: la espera crece como rho/(1-rho), no como rho. Por eso el 100 % no existe.
for rho in (0.5, 0.7, 0.8, 0.9, 0.95):
    print("utilizacion %.0f %% -> espera %.1f veces el tiempo de servicio" % (100 * rho, rho / (1 - rho)))
# -> utilizacion 70 % -> espera 2.3 veces el tiempo de servicio
# -> utilizacion 95 % -> espera 19.0 veces el tiempo de servicio
