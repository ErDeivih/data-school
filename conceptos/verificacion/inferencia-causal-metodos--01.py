# Diferencias en diferencias: dos grupos medidos antes y despues
trat_antes, trat_despues = 20.0, 26.0
ctrl_antes, ctrl_despues = 10.0, 12.0

did = (trat_despues - trat_antes) - (ctrl_despues - ctrl_antes)
print(f"cambio del grupo tratado  {trat_despues - trat_antes:+.1f}")   # -> +6.0
print(f"cambio del grupo control  {ctrl_despues - ctrl_antes:+.1f}")  # -> +2.0
print(f"efecto DiD                {did:+.1f}")                         # -> +4.0

# Variables instrumentales: estimador de Wald = forma reducida / primera etapa
primera_etapa, forma_reducida = 0.30, 90.0
print(f"LATE                      {forma_reducida / primera_etapa:.0f}")  # -> 300
