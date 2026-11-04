# Con altas constantes la base no crece sin fin: converge a altas / churn.
def base_estable(altas_mes, churn):
    return altas_mes / churn

altas, margen_mensual = 4000, 4.0
for churn in (0.08, 0.06, 0.05):
    print("churn %.0f %% -> base estable %.0f usuarios, LTV %.0f EUR"
          % (100 * churn, base_estable(altas, churn), margen_mensual / churn))
# -> churn 6 % -> base estable 66667 usuarios, LTV 67 EUR
# -> churn 5 % -> base estable 80000 usuarios, LTV 80 EUR

# Un punto de churn vale lo mismo que subir las altas un 20 %.
print("subir altas un 20 %:", round(base_estable(altas * 1.2, 0.06)))  # -> 80000
print("bajar el churn a 5 %:", round(base_estable(altas, 0.05)))       # -> 80000

# Quick ratio: cuanto entra por cada uno que se va. Por debajo de 1, la base se encoge.
for nuevos, recuperados, bajas in ((4000, 800, 2000), (3000, 300, 3300)):
    print("quick ratio %.2f" % ((nuevos + recuperados) / bajas))
# -> quick ratio 2.40
# -> quick ratio 1.00
