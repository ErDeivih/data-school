# Lo que un p < 0,05 no te dice: la proporcion de hallazgos que son falsos.
# 200 candidatos, 20 con efecto real, potencia 80 %, alpha 5 %.
verdaderos, ruido = 20, 180
aciertos = 0.80 * verdaderos
falsos = 0.05 * ruido
hallazgos = aciertos + falsos

print(f"hallazgos con p < 0,05  {hallazgos:.0f}")          # -> 25
print(f"de ellos, falsos        {falsos:.0f}")            # -> 9
print(f"proporcion de falsos    {falsos / hallazgos:.0%}")  # -> 36%
