#!/usr/bin/env python3
# Imagen de vista previa para compartir el link (WhatsApp, etc.). Uso: python3 og.py -> og.jpg (1200x630)
import base64, contextlib, io, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import build  # motivo dorado del flyer
FOTO = "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(HERE, "img/fiesta.jpg"), "rb").read()).decode()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1200, 630

html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&family=Pacifico&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: {W}px; height: {H}px; overflow: hidden; }}
body {{ position: relative; color: #fff; font-family: "Outfit", sans-serif;
  background: linear-gradient(180deg, #7f9295 0%, #5f6e72 30%, #4c4e4d 55%, #5a3a2c 80%, #642810 100%); }}
.foto {{ position: absolute; top: 0; right: 0; width: 600px; height: 100%; object-fit: cover; object-position: center 45%;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,.6) 22%, #000 50%); }}
.motivo {{ position: absolute; left: 0; width: 720px; bottom: 0; height: 150px; opacity: .45;
  background: url("{build.PATRON}") left top / 170px repeat-x; -webkit-mask-image: linear-gradient(0deg, #000, transparent), linear-gradient(90deg, #000 70%, transparent); -webkit-mask-composite: source-in; }}
.texto {{ position: absolute; left: 64px; top: 64px; width: 640px; }}
h1 {{ font-weight: 800; font-size: 112px; line-height: .95; letter-spacing: -.045em; text-shadow: 0 6px 30px rgba(23,14,9,.35); }}
.y {{ display: block; margin-top: 18px; font: 400 64px/1.3 "Pacifico", cursive; color: #ecd27c; transform: rotate(-3deg); transform-origin: left center; }}
.bajada {{ margin-top: 18px; font-weight: 600; font-size: 30px; line-height: 1.3; max-width: 17em; }}
</style></head><body>
<img class="foto" src="{FOTO}" alt="">
<div class="motivo"></div>
<div class="texto">
  <h1>Te canto<br>las 40.</h1>
  <span class="y">Y fueron 41.</span>
  <p class="bajada">El medallero, el registro de la noche y los looks.</p>
</div>
</body></html>"""

src = os.path.join(HERE, ".og.html")
png = os.path.join(HERE, ".og.png")
out = os.path.join(HERE, "og.jpg")
open(src, "w", encoding="utf-8").write(html)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                "--virtual-time-budget=6000", f"--window-size={W},{H}", f"--screenshot={png}", "file://" + src],
               check=True, capture_output=True)
subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", png, "--out", out], check=True, capture_output=True)
os.remove(src)
os.remove(png)
print(out, os.path.getsize(out), "bytes")
