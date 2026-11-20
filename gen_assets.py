"""Render OozAmp Neon Vat image assets for the PCSX2 custom.qss theme.

Outputs (in build/oozamp/): gel.jpg (window background, stretched by Qt),
pipe_*.png (checkbox indicators, 2x), radio_*.png, arrow_*.png.
"""
import io, os, random, sys
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = os.path.join(os.path.dirname(__file__), 'build', 'oozamp')
os.makedirs(OUT, exist_ok=True)

# ---------- gel pool (from gen_field recipe, no skulls) ----------
def gel_svg(W=1600, H=1000, seed=21):
    rnd = random.Random(seed)
    stops = [(0.05, 0.12, 0.0), (0.12, 0.25, 0.0), (0.12, 0.25, 0.0), (0.12, 0.25, 0.0), (0.30, 0.52, 0.0), (0.66, 0.92, 0.0)]
    R, G, B = (' '.join(f'{s[i]:.3f}' for s in stops) for i in range(3))
    sw = ''.join(f"<ellipse cx='{rnd.uniform(0,W):.0f}' cy='{rnd.uniform(0,H):.0f}' rx='{rnd.uniform(60,220):.0f}' ry='{rnd.uniform(50,170):.0f}' fill='#fff' opacity='{rnd.uniform(.25,.6):.2f}'/>" for _ in range(22))
    filt = (
        "<filter id='gel' x='0' y='0' width='100%' height='100%' color-interpolation-filters='sRGB'>"
        f"<feTurbulence type='fractalNoise' baseFrequency='.0032 .0042' numOctaves='3' seed='{seed}' result='n'/>"
        "<feGaussianBlur in='SourceGraphic' stdDeviation='38' result='sw'/>"
        "<feColorMatrix in='n' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.5 0 0 0 -.3' result='na'/>"
        "<feComposite in='na' in2='sw' operator='arithmetic' k2='1' k3='.4' result='h0'/>"
        "<feGaussianBlur in='h0' stdDeviation='7' result='hs'/>"
        f"<feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='1' seed='{seed+1}' result='g'/>"
        "<feColorMatrix in='g' type='matrix' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .022 0 0 0 0' result='ga'/>"
        "<feComposite in='hs' in2='ga' operator='arithmetic' k2='1' k3='1' k4='-.011' result='h'/>"
        "<feColorMatrix in='h' type='matrix' values='0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 1' result='hg'/>"
        f"<feComponentTransfer in='hg' result='col'><feFuncR type='table' tableValues='{R}'/><feFuncG type='table' tableValues='{G}'/>"
        f"<feFuncB type='table' tableValues='{B}'/><feFuncA type='linear' slope='0' intercept='1'/></feComponentTransfer>"
        "<feDiffuseLighting in='h' surfaceScale='16' diffuseConstant='1.05' lighting-color='#ffffff' result='diff'><feDistantLight azimuth='235' elevation='58'/></feDiffuseLighting>"
        "<feComposite in='col' in2='diff' operator='arithmetic' k1='1.3' result='shaded'/>"
        "<feSpecularLighting in='h' surfaceScale='16' specularConstant='.75' specularExponent='38' lighting-color='#f4ffcc' result='spec'><feDistantLight azimuth='235' elevation='34'/></feSpecularLighting>"
        "<feComposite in='spec' in2='shaded' operator='in' result='spec2'/>"
        "<feMerge><feMergeNode in='shaded'/><feMergeNode in='spec2'/></feMerge></filter>"
    )
    bub = []
    for _ in range(140):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([rnd.uniform(1, 2.2), rnd.uniform(1, 2.2), rnd.uniform(2.2, 4.5), rnd.uniform(4.5, 8)])
        bub.append(
            f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='rgba(16,40,0,.35)' stroke='rgba(240,255,170,.55)' stroke-width='{max(.6, r*.14):.2f}'/>"
            f"<circle cx='{x - r*.32:.1f}' cy='{y - r*.38:.1f}' r='{r*.22:.1f}' fill='#fbffe6' opacity='.85'/>")
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}'><defs>{filt}"
            "<linearGradient id='top' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='rgb(5,16,0)' stop-opacity='.55'/>"
            "<stop offset='.32' stop-color='rgb(5,16,0)' stop-opacity='.28'/><stop offset='.58' stop-color='rgb(5,16,0)' stop-opacity='0'/></linearGradient>"
            "<radialGradient id='glow' cx='130' cy='1040' r='560' gradientUnits='userSpaceOnUse'><stop offset='0' stop-color='rgb(214,255,0)' stop-opacity='.34'/>"
            "<stop offset='.45' stop-color='rgb(214,255,0)' stop-opacity='.12'/><stop offset='.75' stop-color='rgb(214,255,0)' stop-opacity='0'/></radialGradient></defs>"
            f"<rect width='{W}' height='{H}' fill='#000'/><g filter='url(#gel)'><rect width='{W}' height='{H}' fill='#000'/>{sw}</g>"
            f"{''.join(bub)}<rect width='{W}' height='{H}' fill='url(#top)'/><rect width='{W}' height='{H}' fill='url(#glow)'/></svg>")


# ---------- sewer pipe checkbox (viewBox 28x40, mouth centred at y=20) ----------
STEEL = ("<radialGradient id='st' cx='14' cy='20' r='13.6' gradientUnits='userSpaceOnUse'>"
         "<stop offset='.66' stop-color='#11160d'/><stop offset='.72' stop-color='#3c4434'/><stop offset='.80' stop-color='#a7b29a'/>"
         "<stop offset='.86' stop-color='#d4dcc8'/><stop offset='.93' stop-color='#7c8670'/><stop offset='1' stop-color='#4a5240'/></radialGradient>"
         "<linearGradient id='lt' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#fff' stop-opacity='.28'/><stop offset='.55' stop-color='#fff' stop-opacity='0'/>"
         "<stop offset='1' stop-color='#000' stop-opacity='.3'/></linearGradient>"
         "<radialGradient id='tb' cx='14' cy='20' r='9.4' gradientUnits='userSpaceOnUse'><stop offset='0' stop-color='#000'/>"
         "<stop offset='.62' stop-color='#050a02'/><stop offset='1' stop-color='#1d2c12'/></radialGradient>"
         "<radialGradient id='bt' cx='.35' cy='.3' r='.8'><stop offset='0' stop-color='#eef2e4'/><stop offset='1' stop-color='#5d6652'/></radialGradient>"
         "<linearGradient id='ru' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#e8602c' stop-opacity='.9'/><stop offset='1' stop-color='#e8602c' stop-opacity='0'/></linearGradient>"
         "<radialGradient id='sl' cx='14' cy='22' r='11' gradientUnits='userSpaceOnUse'><stop offset='0' stop-color='#f0ff9a'/>"
         "<stop offset='.35' stop-color='#ccff00'/><stop offset='.8' stop-color='#8fd000'/><stop offset='1' stop-color='#5c9a00'/></radialGradient>"
         "<linearGradient id='dr' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#9ad600'/><stop offset='.45' stop-color='#e6ff70'/><stop offset='1' stop-color='#9ad600'/></linearGradient>"
         "<clipPath id='mouth'><circle cx='14' cy='20' r='9.2'/></clipPath>")

def pipe(on, disabled=False):
    bolts = ''.join(f"<circle cx='{x}' cy='{y}' r='1.55' fill='url(#bt)' stroke='#20261a' stroke-width='.35'/>"
                    for x, y in [(5.7, 11.7), (22.3, 11.7), (5.7, 28.3), (22.3, 28.3)])
    body = ("<circle cx='14' cy='20' r='13.6' fill='url(#st)' stroke='#0d1209' stroke-width='.6'/>"
            "<circle cx='14' cy='20' r='13.6' fill='url(#lt)'/>"
            "<circle cx='14' cy='20' r='9.3' fill='url(#tb)' stroke='#000' stroke-width='.5'/>")
    rust = "<path d='M21.6 29.6 q.5 2.6 -.1 4.4 q-.6-1.6-.6-3.9z' fill='url(#ru)'/>"
    if on:
        inner = ("<g clip-path='url(#mouth)'><ellipse cx='14' cy='28.4' rx='10.8' ry='5.8' fill='url(#sl)'/>"
                 "<ellipse cx='12.4' cy='23.3' rx='4.2' ry='.7' fill='#fdffe0' opacity='.85'/></g>")
        spill = ("<path d='M12.1 28.2 C12.6 30 13 30.6 13.05 32.2 L13.1 34.6 C13.1 35.6 14.9 35.6 14.9 34.6 L14.95 32.2 C15 30.6 15.4 30 15.9 28.2 Z' fill='url(#dr)'/>"
                 "<ellipse cx='14' cy='36.4' rx='2.5' ry='2.9' fill='url(#sl)'/>"
                 "<ellipse cx='13.2' cy='35.4' rx='.7' ry='.9' fill='#fdffe0' opacity='.9'/>"
                 "<path d='M13.6 29.6 q.3 2 .1 4' stroke='#f6ffb8' stroke-width='.5' fill='none' opacity='.8'/>")
    else:
        inner = "<g clip-path='url(#mouth)'><ellipse cx='14' cy='28.6' rx='8' ry='3.4' fill='#8cbe00' opacity='.28'/></g>"
        spill = ''
    g = body + inner + bolts + rust + spill
    if disabled:
        g = f"<g opacity='.45' style='filter:saturate(.35)'>{g}</g>"
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='56' height='80' viewBox='0 0 28 40'><defs>{STEEL}</defs>{g}</svg>"


def radio(on, disabled=False):
    defs = ("<radialGradient id='gl' cx='.38' cy='.32' r='.75'><stop offset='0' stop-color='#3a5a14'/><stop offset='1' stop-color='#040a01'/></radialGradient>"
            "<radialGradient id='lm' cx='.38' cy='.32' r='.8'><stop offset='0' stop-color='#fbffe0'/><stop offset='.25' stop-color='#e4ff5a'/>"
            "<stop offset='.7' stop-color='#ccff00'/><stop offset='1' stop-color='#7ab800'/></radialGradient>")
    g = ("<circle cx='10' cy='10' r='8.6' fill='url(#gl)' stroke='#eeff2e' stroke-width='1.3'/>"
         "<ellipse cx='8' cy='6' rx='4.2' ry='2' fill='#fff' opacity='.18'/>")
    if on:
        g += ("<circle cx='10' cy='10' r='5.2' fill='url(#lm)'/>"
              "<ellipse cx='8.4' cy='8' rx='1.6' ry='1' fill='#fff' opacity='.9'/>")
    if disabled:
        g = f"<g opacity='.45'>{g}</g>"
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 20 20'><defs>{defs}</defs>{g}</svg>"


def arrow(d, color='#ccff00'):
    paths = {'down': 'M2 3l5 5 5-5', 'up': 'M2 8l5-5 5 5', 'right': 'M4 1.5l5 5-5 5', 'left': 'M9 1.5l-5 5 5 5'}
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='28' height='{26 if d in ('right','left') else 22}' "
            f"viewBox='0 0 14 {13 if d in ('right','left') else 11}'><path d='{paths[d]}' fill='none' stroke='{color}' "
            "stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/></svg>")


def main():
    jobs = {
        'pipe_off.png': pipe(False), 'pipe_on.png': pipe(True),
        'pipe_off_disabled.png': pipe(False, True), 'pipe_on_disabled.png': pipe(True, True),
        'radio_off.png': radio(False), 'radio_on.png': radio(True),
        'radio_off_disabled.png': radio(False, True), 'radio_on_disabled.png': radio(True, True),
        'arrow_down.png': arrow('down'), 'arrow_up.png': arrow('up'),
        'arrow_right.png': arrow('right'), 'arrow_left.png': arrow('left'),
        'arrow_down_dark.png': arrow('down', '#102400'),
    }
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = b.new_page()
        for name, svg in jobs.items():
            pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
            pg.locator('svg').screenshot(path=os.path.join(OUT, name), omit_background=True)
        pg.set_viewport_size({'width': 1600, 'height': 1000})
        pg.set_content(f"<html><body style='margin:0'>{gel_svg()}</body></html>")
        png = pg.locator('svg').screenshot()
        b.close()
    im = Image.open(io.BytesIO(png)).convert('RGB')
    im = Image.blend(im, Image.new('RGB', im.size, (24, 48, 0)), .58)
    im.save(os.path.join(OUT, 'gel.jpg'), quality=86, optimize=True)
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))


if __name__ == '__main__':
    main()
