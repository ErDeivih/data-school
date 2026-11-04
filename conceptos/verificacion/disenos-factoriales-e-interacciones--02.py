import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

datos = pd.DataFrame({
    "rendimiento": [52, 54, 50, 60, 62, 58, 58, 60, 56, 51, 53, 49],
    "temperatura": ["baja"] * 6 + ["alta"] * 6,
    "catalizador": ["antiguo", "antiguo", "antiguo", "nuevo", "nuevo", "nuevo"] * 2,
})
modelo = smf.ols("rendimiento ~ C(temperatura) * C(catalizador)", data=datos).fit()

# Con codificacion de tratamiento cada coeficiente es un salto respecto a la celda de referencia,
# asi que el signo depende de que nivel se tome como base. La interaccion es +15 con esta base.
print(modelo.params.round(2).to_dict())
# -> {'Intercept': 58.0, 'C(temperatura)[T.baja]': -6.0, 'C(catalizador)[T.nuevo]': -7.0,
#     'C(temperatura)[T.baja]:C(catalizador)[T.nuevo]': 15.0}

# Una ANOVA con el termino de interaccion da una fila por efecto; aqui la interaccion es la senal.
print(smf.ols("rendimiento ~ C(temperatura) * C(catalizador)", data=datos).fit().rsquared.round(3),
      len(modelo.resid), float((modelo.resid ** 2).sum()))
# -> 0.846 12 32.0
