# Reconciliacion de una caida de pedidos en dos efectos: trafico y conversion.
ses_antes, ped_antes = 210_000, 12_400
ses_ahora, ped_ahora = 208_000, 11_900

conv_antes, conv_ahora = ped_antes / ses_antes, ped_ahora / ses_ahora
# Pedidos que habria habido si solo hubiera cambiado el trafico.
ped_solo_trafico = ses_ahora * conv_antes

print(f"conversion {conv_antes:.2%} -> {conv_ahora:.2%}")
print(f"pedidos {ped_antes} -> {ped_ahora} ({ped_ahora - ped_antes:+d})")
print(f"efecto trafico {ped_solo_trafico - ped_antes:+.0f}  efecto conversion {ped_ahora - ped_solo_trafico:+.0f}")
