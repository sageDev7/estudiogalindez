"""Saca el fondo amarillo de logo-hd.png (logo real, 2048px) sin tocar el dibujo y arma las variantes.
- negro: tal cual (hexágono negro con balanza amarilla)          -> navbar amarillo, menú
- amarillo: para fondos oscuros (anillo y G amarillos; hexágono amarillo con balanza oscura)
Salidas en img/: logo[-amarillo].png (sello), monograma[-amarillo].png (hexágono | G), anillo-amarillo/negro.png
Uso: python _scripts/logo_png.py"""
from PIL import Image, ImageDraw, ImageChops
import os
D = os.path.join(os.path.dirname(__file__), '..')
src = Image.open(os.path.join(D, 'logo-hd.png')).convert('RGB')
W = src.width
alpha = src.convert('L').point(lambda v: max(0, min(255, int((200 - v) * 255 / 170))))
NEG, YEL, OSC = (0, 0, 0), (253, 215, 75), (14, 14, 13)

# hexágono: bbox de la mancha oscura a la izquierda del centro
zona = (int(W*.24), int(W*.38), int(W*.44), int(W*.62))
x0, y0, x1, y1 = alpha.crop(zona).point(lambda v: 255 if v > 200 else 0).getbbox()
x0 += zona[0]; x1 += zona[0]; y0 += zona[1]; y1 += zona[1]
cx, h, i = (x0 + x1) / 2, y1 - y0, 6
poly = [(cx, y0+i), (x1-i, y0+h/4+i/2), (x1-i, y1-h/4-i/2), (cx, y1-i), (x0+i, y1-h/4-i/2), (x0+i, y0+h/4+i/2)]
hexm = Image.new('L', src.size, 0); ImageDraw.Draw(hexm).polygon(poly, fill=255)

def variante(tinta, balanza):
    """tinta con el alpha del dibujo; dentro del hexágono, opaco (tinta donde era negro, balanza donde era amarillo)"""
    capa = Image.new('RGBA', src.size, tinta + (255,)); capa.putalpha(alpha)
    hexa = Image.composite(Image.new('RGBA', src.size, tinta + (255,)), Image.new('RGBA', src.size, balanza + (255,)), alpha)
    return Image.composite(hexa, capa, hexm)

def circulo(r, dentro=True):
    m = Image.new('L', src.size, 0 if dentro else 255)
    ImageDraw.Draw(m).ellipse((1024-r, 1024-r, 1024+r, 1024+r), fill=255 if dentro else 0)
    return m

negro, amarillo = variante(NEG, YEL), variante(YEL, OSC)
BB = negro.getbbox()  # mismo encuadre para sello y anillo (se superponen en el hero)
for nombre, img, m, w in [('logo.png', negro, None, 1200), ('logo-amarillo.png', amarillo, None, 1200),
                          ('monograma.png', negro, circulo(620), None), ('monograma-amarillo.png', amarillo, circulo(620), None),
                          ('anillo-amarillo.png', amarillo, circulo(640, False), 1200), ('anillo-negro.png', negro, circulo(640, False), 1200)]:
    if m is not None:
        t = Image.new('RGBA', src.size, (0, 0, 0, 0)); t.paste(img, (0, 0), ImageChops.multiply(m, img.getchannel('A'))); img = t
    img = img.crop(BB if nombre.startswith(('logo', 'anillo')) else img.getbbox())
    if w: img = img.resize((w, round(w * img.height / img.width)), Image.LANCZOS)
    img.save(os.path.join(D, 'img', nombre), optimize=True)
    print(nombre, img.size)
