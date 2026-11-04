"""test-adf-kpss-1.py — las dos hipotesis nulas opuestas, las cuatro casillas que salen
de cruzarlas y el error de especificación que da la vuelta al veredicto. La figura de la
pagina de los tests de raiz unitaria."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

CRIT_ADF = {"1%": -3.43, "5%": -2.86, "10%": -2.57}
CRIT_KPSS = {"1%": 0.739, "5%": 0.463, "10%": 0.347}


def adf_stat(y, p=1, tendencia=False):
    """Estadistico t del coeficiente de y_{t-1} en la regresión de Dickey-Fuller."""
    dy = np.diff(y)
    X, objetivo = [], []
    for j in range(p, dy.size):
        fila = [y[j]]                                   # y_{t-1}
        if tendencia:
            fila.append(j + 1)                          # tendencia determinista
        fila.append(1.0)                                # constante
        fila += [dy[j - i] for i in range(1, p + 1)]    # retardos de la diferencia
        X.append(fila)
        objetivo.append(dy[j])
    X, d = np.array(X), np.array(objetivo)
    b, *_ = np.linalg.lstsq(X, d, rcond=None)
    resid = d - X @ b
    s2 = resid @ resid / (X.shape[0] - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    return b[0] / np.sqrt(cov[0, 0])


def kpss_stat(y, tendencia=False):
    """Estadistico LM: suma acumulada de residuos sobre la varianza de largo plazo."""
    T = y.size
    X = np.column_stack([np.ones(T), np.arange(1, T + 1)]) if tendencia else np.ones((T, 1))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    S = np.cumsum(e)
    nlags = int(4 * (T / 100) ** 0.25)                  # regla de Schwert
    s2 = (e @ e) / T
    for l in range(1, nlags + 1):
        s2 += 2 * (1 - l / (nlags + 1)) * (e[l:] @ e[:-l]) / T
    return (S @ S) / (T ** 2 * s2)


n = 300
t = np.arange(n)
ruido = azar.normal(0, 1, n)
paseo = np.cumsum(ruido)
paseo_deriva = np.cumsum(azar.normal(0.1, 1, n))
tendencia = 0.1 * t + azar.normal(0, 1, n)

series = [
    ("Solo ruido: estacionaria de verdad", ruido, AZUL, False),
    ("Paseo aleatorio: raiz unitaria", paseo, ROJO, False),
    ("Paseo con deriva: raiz unitaria y además sube", paseo_deriva, ROJO, False),
    ("Tendencia + ruido: estacionaria si se permite la tendencia", tendencia, NARANJA, True),
]

fig, ejes = plt.subplots(2, 2, figsize=(11.0, 7.6))

for eje, (titulo_panel, serie, color, con_tendencia) in zip(ejes.ravel(), series):
    a = adf_stat(serie)
    k = kpss_stat(serie)
    eje.plot(t, serie, color=color, linewidth=1.0)
    if con_tendencia:
        b, *_ = np.linalg.lstsq(np.column_stack([np.ones(n), t]), serie, rcond=None)
        eje.plot(t, b[0] + b[1] * t, color=MORADO, linewidth=1.4, linestyle="--")

    rechaza_adf = a < CRIT_ADF["5%"]          # mas negativo que el umbral
    rechaza_kpss = k > CRIT_KPSS["5%"]
    color_adf = VERDE if rechaza_adf else ROJO
    color_kpss = VERDE if not rechaza_kpss else ROJO
    eje.text(0.03, 0.99,
             "ADF " + f"{a:+.2f}".replace(".", ",") +
             "   umbral 5 % " + f"{CRIT_ADF['5%']:.2f}".replace(".", ",") +
             ("   rechaza" if rechaza_adf else "   no rechaza"),
             transform=eje.transAxes, fontsize=8.5, color=color_adf, va="top", family="monospace")
    eje.text(0.03, 0.91,
             "KPSS " + f"{k:.3f}".replace(".", ",") +
             "  umbral 5 %  " + f"{CRIT_KPSS['5%']:.3f}".replace(".", ",") +
             ("  rechaza" if rechaza_kpss else "  no rechaza"),
             transform=eje.transAxes, fontsize=8.5, color=color_kpss, va="top", family="monospace")

    if rechaza_adf and not rechaza_kpss:
        lectura, color_lectura = ("los dos coinciden: estacionaria, se modela el nivel", VERDE)
    elif not rechaza_adf and rechaza_kpss:
        lectura, color_lectura = ("los dos coinciden: hay raiz unitaria, hay que diferenciar", ROJO)
    elif not rechaza_adf and not rechaza_kpss:
        lectura, color_lectura = ("ninguno rechaza: no hay información suficiente", NARANJA)
    else:
        lectura, color_lectura = ("se contradicen: busca un cambio estructural", NARANJA)
    if not con_tendencia:
        eje.text(0.03, 0.06, lectura, transform=eje.transAxes, fontsize=8.5,
                 color=color_lectura, va="bottom")

    if con_tendencia:
        a2 = adf_stat(serie, tendencia=True)
        k2 = kpss_stat(serie, tendencia=True)
        eje.text(0.03, 0.70,
                 "sin tendencia, los dos rechazan la estacionariedad;\n"
                 "con tendencia, los dos coinciden: es estacionaria",
                 transform=eje.transAxes, fontsize=8.5, color=color_lectura, va="top")
        eje.text(0.03, 0.55,
                 "con tendencia:  ADF " + f"{a2:+.2f}".replace(".", ",") +
                 "   KPSS " + f"{k2:.3f}".replace(".", ",") + "   ->  estacionaria",
                 transform=eje.transAxes, fontsize=8.5, color=VERDE, va="top",
                 family="monospace")
        anotar(eje, "la linea morada es la tendencia que el\ncontraste con constante no ve",
               (150, b[0] + b[1] * 150), (0.42, 0.30), MORADO)

    eje.set_title(titulo_panel)

    eje.set_xlabel("dia")
    eje.set_ylabel("valor")
    rejilla(eje)
    numeros(eje)

guardar(fig, "adf-kpss-cuatro-casillas")
