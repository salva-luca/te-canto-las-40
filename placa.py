#!/usr/bin/env python3
# Placa "¿No sabés qué cantar? Escaneá" con el QR de la página. Uso: python3 placa.py
# Genera placa-pantalla.png (1920x1080) y placa-vertical.png (1080x1920) con Chrome headless.
import base64, contextlib, io, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import build  # reusa el motivo dorado del flyer
QR = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(HERE, "qr-pagina.jpg"), "rb").read()).decode()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FORMATOS = {
    "pantalla": (1920, 1080, "h"),
    "vertical": (1080, 1920, "v"),
}


def html(w, h, modo):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&family=Pacifico&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{ position: relative; color: #fff; font-family: "Outfit", sans-serif;
  background: linear-gradient(180deg, #7f9295 0%, #5f6e72 22%, #4c4e4d 42%, #5a3a2c 62%, #642810 80%, #170e09 100%); }}
.motivo {{ position: absolute; inset: 0; opacity: .55; background: url("{build.PATRON}") center top / {300 if modo == 'h' else 290}px repeat; }}
.motivo.arriba {{ -webkit-mask-image: linear-gradient(180deg, #000 0%, transparent {38 if modo == 'h' else 30}%); }}
.motivo.abajo {{ opacity: .35; -webkit-mask-image: linear-gradient(0deg, #000 0%, transparent {30 if modo == 'h' else 22}%); }}
.grano {{ position: absolute; inset: 0; opacity: .12; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E"); }}
.wrap {{ position: relative; height: 100%; display: flex; align-items: center; justify-content: center;
  {'gap: 120px; padding: 0 120px;' if modo == 'h' else 'flex-direction: column; gap: 70px; padding: 140px 80px;'} }}
.texto {{ {'flex: 0 1 900px;' if modo == 'h' else 'text-align: center;'} }}
.fiesta {{ font-weight: 800; font-size: {44 if modo == 'h' else 50}px; letter-spacing: -.03em; }}
h1 {{ margin-top: 18px; font-weight: 800; font-size: {150 if modo == 'h' else 150}px; line-height: .92; letter-spacing: -.045em;
  text-shadow: 0 6px 40px rgba(23, 14, 9, .35); }}
.esc {{ display: block; margin-top: {34 if modo == 'h' else 40}px; font: 400 {130 if modo == 'h' else 140}px/1.25 "Pacifico", cursive;
  color: #ecd27c; -webkit-text-stroke: .012em #ecd27c; transform: rotate(-4deg); transform-origin: {'left' if modo == 'h' else 'center'} center;
  text-shadow: 0 6px 30px rgba(23, 14, 9, .45); }}
.bajada {{ margin-top: {30 if modo == 'h' else 34}px; font-weight: 600; font-size: {38 if modo == 'h' else 42}px; line-height: 1.3; {'max-width: 20em;' if modo == 'h' else 'max-width: 18em; margin-left: auto; margin-right: auto;'} }}
.qr {{ flex: none; position: relative; width: {640 if modo == 'h' else 700}px; padding: 26px; background: #fff; border-radius: 34px;
  box-shadow: 0 30px 90px rgba(23, 14, 9, .55), 0 0 0 10px #c6a84f; }}
.qr img {{ display: block; width: 100%; height: auto; }}
</style></head><body>
<div class="motivo arriba"></div><div class="motivo abajo"></div><div class="grano"></div>
<div class="wrap">
  <div class="texto">
    <p class="fiesta">Te canto las 40.</p>
    <h1>¿No sabés<br>qué cantar?</h1>
    <span class="esc">Escaneá</span>
    <p class="bajada">Más de 200 temas para elegir por estilo y década, o uno al azar si no te decidís.</p>
  </div>
  <div class="qr"><img src="{QR}" alt="QR a la página"></div>
</div>
</body></html>"""


for nombre, (w, h, modo) in FORMATOS.items():
    src = os.path.join(HERE, f".placa-{nombre}.html")
    out = os.path.join(HERE, f"placa-{nombre}.png")
    open(src, "w", encoding="utf-8").write(html(w, h, modo))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=6000", f"--window-size={w},{h}", f"--screenshot={out}", "file://" + src],
                   check=True, capture_output=True)
    os.remove(src)
    print(out)
