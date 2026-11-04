"""_medir.py — mide solapes de texto en una figura sin mirarla a ojo.

Uso:
    python figuras/_medir.py figuras\\coste-y-latencia-1.py

Ejecuta el script de la figura con la escritura de ficheros interceptada y, sobre la figura
ya construida, saca la caja de cada texto visible y avisa de los pares que se pisan:

  * SOLAPE : dos textos se cruzan (esto es lo que rompe la figura).
  * FUERA  : un texto se sale del lienzo (se corta al exportar).
  * INVADE : un texto se apoya en el panel de otro eje sin caber dentro del suyo.

Los textos rotados (el rotulo vertical del eje y) quedan fuera de la comparación por parejas.
"""

import importlib.util
import io
import sys
import warnings
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.text import Text

RAIZ = Path(__file__).resolve().parent.parent


def rot_of(t):
    return abs(t.get_rotation() or 0) % 180


def etiqueta(t):
    s = t.get_text().replace("\n", " / ")
    return s if len(s) <= 58 else s[:55] + "..."


def medir(script):
    ruta = Path(script)
    if not ruta.is_absolute():
        ruta = RAIZ / ruta

    capturadas = []
    original = matplotlib.figure.Figure.savefig

    def falso_savefig(self, *a, **k):
        if self not in capturadas:
            capturadas.append(self)

    matplotlib.figure.Figure.savefig = falso_savefig
    import comun
    comun.guardar = lambda fig, nombre: capturadas.append(fig)
    buf = io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location("figura_medida", ruta)
        mod = importlib.util.module_from_spec(spec)
        with warnings.catch_warnings(), redirect_stdout(buf):
            warnings.simplefilter("ignore")
            spec.loader.exec_module(mod)
    finally:
        matplotlib.figure.Figure.savefig = original

    if not capturadas:
        print("La figura no llamo a guardar(): nada que medir.")
        return 1

    solapes = 0
    fuera = 0
    for i, fig in enumerate(capturadas):
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        ancho, alto = fig.canvas.get_width_height()
        ejes = list(fig.axes)
        cajas_ejes = [(ax, ax.get_window_extent(r)) for ax in ejes]

        textos = []
        for t in fig.findobj(Text):
            if not t.get_visible() or not (t.get_text() or "").strip():
                continue
            try:
                # En una anotacion, get_window_extent y get_tightbbox incluyen el parche de
                # la flecha y devuelven una caja enorme. Se mide el texto como Text puro.
                import copy
                c = copy.copy(t)
                if type(c) is not Text:
                    c.__class__ = Text
                b = c.get_window_extent(renderer=r)
            except Exception:
                continue
            if b is None or b.width <= 0 or b.height <= 0:
                continue
            textos.append((t, b, rot_of(t)))

        print("=" * 78)
        print(f"Figura {i + 1}/{len(capturadas)}: {ancho}x{alto} px, {len(ejes)} ejes, "
              f"{len(textos)} textos medidos")

        for t, c, _ in textos:
            if c.x0 < -0.5 or c.y0 < -0.5 or c.x1 > ancho + 0.5 or c.y1 > alto + 0.5:
                fuera += 1
                print(f"  FUERA   [{c.x0:7.1f},{c.y0:7.1f} -> {c.x1:7.1f},{c.y1:7.1f}] "
                      f"«{etiqueta(t)}»")

        # --- textos que una linea o una barra atraviesa ------------------------
        # Una anotacion puede no pisar a otro texto y aun asi quedar ilegible porque la
        # curva le pasa por encima. Aqui se compara la caja del texto con las lineas y
        # parches del eje al que pertenece.
        from matplotlib.lines import Line2D
        from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
        for t, c, _ in textos:
            ax = t.axes
            if ax is None:
                continue
            for art in ax.get_children():
                if isinstance(art, FancyArrowPatch):
                    continue      # la flecha de una anotacion apunta a su curva a proposito
                if isinstance(art, Line2D):
                    pts = art.get_xydata()
                    if len(pts) < 2:
                        continue
                    px = ax.transData.transform(pts)
                    cruces = 0
                    for k in range(len(px) - 1):
                        x0, y0 = px[k]
                        x1, y1 = px[k + 1]
                        pasos = max(2, int(max(abs(x1 - x0), abs(y1 - y0)) / 2))
                        for s in range(pasos + 1):
                            f = s / pasos
                            xi = x0 + (x1 - x0) * f
                            yi = y0 + (y1 - y0) * f
                            if c.x0 - 1 <= xi <= c.x1 + 1 and c.y0 - 1 <= yi <= c.y1 + 1:
                                cruces += 1
                    if cruces > 3:
                        solapes += 1
                        print(f"  LINEA   {cruces:4d} puntos de una linea dentro de "
                              f"«{etiqueta(t)}»")
                elif isinstance(art, (Rectangle, FancyBboxPatch)) and art.get_visible():
                    from matplotlib.legend import Legend
                    if art is ax.patch:
                        continue
                    if any(art is lg.get_frame() for lg in ax.get_children()
                           if isinstance(lg, Legend)):
                        continue          # el texto de la leyenda vive dentro de su caja
                    b = art.get_window_extent(r)
                    dx = min(c.x1, b.x1) - max(c.x0, b.x0)
                    dy = min(c.y1, b.y1) - max(c.y0, b.y0)
                    if dx > 3 and dy > 3 and b.width > 4 and b.height > 4:
                        solapes += 1
                        print(f"  BARRA   x{dx:5.1f} y{dy:5.1f} dentro de «{etiqueta(t)}»")

        rectos = [(t, c) for t, c, rot in textos if rot == 0]
        for a in range(len(rectos)):
            ta, ca = rectos[a]
            for b in range(a + 1, len(rectos)):
                tb, cb = rectos[b]
                dx = min(ca.x1, cb.x1) - max(ca.x0, cb.x0)
                dy = min(ca.y1, cb.y1) - max(ca.y0, cb.y0)
                if dx > 1.0 and dy > 1.0:
                    solapes += 1
                    print(f"  SOLAPE  x{dx:5.1f} y{dy:5.1f}  «{etiqueta(ta)}»  <->  «{etiqueta(tb)}»")

        for t, c, _ in textos:
            for ax, cb in cajas_ejes:
                if c.x1 < cb.x0 or c.x0 > cb.x1 or c.y1 < cb.y0 or c.y0 > cb.y1:
                    continue
                dentro = (c.x0 >= cb.x0 - 0.5 and c.x1 <= cb.x1 + 0.5
                          and c.y0 >= cb.y0 - 0.5 and c.y1 <= cb.y1 + 0.5)
                # Solo cuenta si el texto pertenece a OTRO eje: los avisos del propio eje
                # (ticks que se meten bajo el marco) se ven en la comparacion por parejas.
                if not dentro and t.axes is not ax:
                    solapes += 1
                    print(f"  INVADE  dx{min(c.x1, cb.x1) - max(c.x0, cb.x0):5.1f} "
                          f"«{etiqueta(t)}» sobre el panel de otro eje")

    print("=" * 78)
    print(f"TOTAL: {solapes} solapes/invasiones, {fuera} textos fuera del lienzo")
    return 0


if __name__ == "__main__":
    sys.exit(medir(sys.argv[1]))
