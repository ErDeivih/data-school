# Un robot con ventaja bruta que pierde dinero al poner los costes reales.
lotes = 0.10
unidades_por_lote = 100_000
valor_pip = lotes * unidades_por_lote * 0.0001          # en USD para este par

spread_pips = 1.2
comision_pips = 7.0 * lotes / valor_pip                 # 7 USD por lote, pasado a pips
slippage_pips = 0.5
objetivo, stop, acierto = 6.0, 6.0, 0.56

bruto = acierto * objetivo - (1 - acierto) * stop
coste_fijo = spread_pips + comision_pips
coste_desliz = (1 - acierto) * slippage_pips        # el stop se ejecuta a mercado
neto = bruto - coste_fijo - coste_desliz

print(f"valor del pip con {lotes:.2f} lotes: {valor_pip:.2f} USD")   # -> 1.00 USD
print(f"esperanza bruta: {bruto:+.2f} pips")                        # -> +0.72 pips
print(f"costes fijos:    {coste_fijo:.2f} pips")                    # -> 1.90 pips
print(f"esperanza neta:  {neto:+.2f} pips")                         # -> -1.40 pips
