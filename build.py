#!/usr/bin/env python3
# Genera index.html desde looks.py y credits.json. Uso: python3 build.py
import html, json, os, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import looks
import temas
import registro
import resultados

# El nombre de la fiesta vive solo aca: cambiarlo y volver a correr el script.
TITULO = "Te canto las 40"

# Votación (Google Forms). Pasar a True cuando se abre la votación, correr build.py y republicar.
VOTACION_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfm4kTeIla4ivfnao4KStZRraC-1g7lKOuU_QkIVsyZbKxxtA/viewform"
VOTACION_ABIERTA = False

NIVELES = {1: "Con lo que tenés en casa", 2: "Comprando un par de cosas", 3: "Producción total"}
REGIONES = {"int": "Internacionales", "arg": "Nacionales"}
e = html.escape
creds = json.load(open(os.path.join(HERE, "credits.json"), encoding="utf-8"))
# 01-freddie.jpg -> freddie: el orden de looks.py no depende del numero del archivo
ARCHIVO = {c["file"][3:-4]: c["file"] for c in creds}

# Motivo dorado del flyer, redibujado en SVG.
ESTRELLA = "M0-43A43 43 0 0 0 43 0 43 43 0 0 0 0 43 43 43 0 0 0-43 0 43 43 0 0 0 0-43Z"


def patron(color="#c6a84f"):
    esquinas = "".join(f'<circle cx="{x}" cy="{y}" r="64" fill="#fff"/>' for x in (-72, 72) for y in (-72, 72))
    cruz = '<rect x="-4.2" y="-102" width="8.4" height="204"/><rect x="-102" y="-4.2" width="204" height="8.4"/>'
    aros = lambda radios: "".join(f'<circle r="{r}"/>' for r in radios)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-102 -102 204 204"><defs>'
        f'<mask id="c" maskUnits="userSpaceOnUse" x="-102" y="-102" width="204" height="204"><rect x="-102" y="-102" width="204" height="204" fill="#fff"/><g fill="#000">{cruz}</g></mask>'
        f'<mask id="l" maskUnits="userSpaceOnUse" x="-102" y="-102" width="204" height="204">{esquinas}<g fill="#000">{cruz}</g></mask>'
        f'</defs><g fill="none" stroke="{color}" stroke-width="4.3"><g mask="url(#c)">{aros([96, 87, 78, 69, 60])}</g><g mask="url(#l)">{aros([51, 42])}</g></g>'
        f'<path fill="{color}" d="{ESTRELLA}"/></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=,' ").replace('"', "%22")


PATRON = patron()


def estrellas(n):
    return '<svg class="st" aria-hidden="true"><use href="#estrella"/></svg>' * n


def slide(row):
    key, _, name, look, how, song, lvl, _r = row
    wide = key in looks.WIDE
    pos = f' style="object-position: {looks.ENCUADRE[key]}"' if key in looks.ENCUADRE else ""
    return f"""<article class="look" data-level="{lvl}">
  <img src="img/{ARCHIVO[key]}" alt="{e(name)}: {e(look)}" loading="lazy" width="{900 if wide else 576}" height="{600 if wide else 720}"{pos}>
  <h3>{e(name)}</h3>
  <p>{e(look)}</p>
  <p class="how">{e(how)}</p>
  <p class="song">Cantá: <b>{e(song)}</b></p>
  <p class="lvl">{estrellas(lvl)}{NIVELES[lvl]}</p>
</article>"""


FLECHA_I = '<svg viewBox="0 0 34 14" aria-hidden="true"><path d="M33 7H1M7 1 1 7l6 6"/></svg>'
FLECHA_D = '<svg viewBox="0 0 34 14" aria-hidden="true"><path d="M1 7h32M27 1l6 6-6 6"/></svg>'

secciones = []
for region, titulo in REGIONES.items():
    slides = [slide(r) for r in looks.L if r[7] == region]
    secciones.append(f"""<section class="car wrap" data-region="{region}" aria-label="{titulo}">
  <header class="car-top">
    <h2>{titulo}</h2>
    <div class="ctl">
      <span class="count" aria-live="off"></span>
      <button type="button" class="pause">Pausar</button>
      <button type="button" class="arrow prev" aria-label="Anterior en {titulo}">{FLECHA_I}</button>
      <button type="button" class="arrow next" aria-label="Siguiente en {titulo}">{FLECHA_D}</button>
    </div>
  </header>
  <div class="track" tabindex="0" aria-label="Looks {titulo}. Deslizá para ver más.">
{chr(10).join(slides)}
  </div>
</section>""")

def decada(anio):
    return next(k for k, _, desde, hasta in temas.DECADAS if desde <= anio <= hasta)


def boton_t(grupo, valor, texto):
    return f'<button type="button" class="tf" data-grupo="{grupo}" data-v="{valor}" aria-pressed="false">{e(texto)}</button>'


usados = {g for *_, gs in temas.T for g in gs.split()}
assert usados <= set(temas.GENEROS), usados - set(temas.GENEROS)
filtros_temas = [
    ("Origen", "".join(boton_t("o", k, v) for k, v in REGIONES.items())),
    ("Género", "".join(boton_t("g", k, v) for k, v in temas.GENEROS.items())),
    ("Década", "".join(boton_t("d", k, v) for k, v, *_ in temas.DECADAS)),
]
filtros_temas_html = "\n".join(
    f'<div class="tf-fila"><p class="tf-tit">{t}</p><div class="tf-ops">{b}</div></div>' for t, b in filtros_temas
)
lista_html = "".join(
    f'<li data-o="{o}" data-g="{g}" data-d="{decada(y)}"><b>{e(t)}</b><span>{e(a)} · {y}</span></li>'
    for a, t, o, y, g in temas.T
)
total_temas = len(temas.T)
fuentes_html = "\n".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for t, u in temas.FUENTES)


votar_hero = f'<a class="cta-votar" href="{e(VOTACION_URL)}" target="_blank" rel="noopener"><svg class="st" aria-hidden="true"><use href="#estrella"/></svg>Votá a los ganadores<svg class="st" aria-hidden="true"><use href="#estrella"/></svg></a>' if VOTACION_ABIERTA else ""
votar_nav = f'<a class="ir-votar" href="{e(VOTACION_URL)}" target="_blank" rel="noopener">Votá</a>' if VOTACION_ABIERTA else ""


def ranking_html():
    filas, previo, pos = [], None, 0
    for i, (n, c) in enumerate(registro.ranking(), 1):
        if c != previo:
            pos, previo = i, c
        podio = ' class="podio"' if pos <= 3 else ""
        filas.append(f'<li{podio}><span class="pos">{pos}</span><b>{e(n)}</b><span class="c">{c} {"tema" if c == 1 else "temas"}</span></li>')
    return "".join(filas)


n_full = sum(1 for f in registro.NOCHE if f[1] == [registro.FULL])
setlist_html = "".join(f'<li><b>{e(f[0])}</b><span>{e(registro.quienes(f))}</span></li>' for f in registro.NOCHE)
noche_html = f"""<section id="noche" class="bloque bloque-noche" aria-labelledby="noche-tit"><div class="wrap">
  <header class="bloque-top">
    <p class="kicker">La noche del 9 de noviembre</p>
    <h2 id="noche-tit">El registro (in)completo.</h2>
    <p>{len(registro.NOCHE)} temas en una noche, en el orden en que sonaron.</p>
  </header>
  <ol class="setlist">{setlist_html}</ol>
  <div class="rank">
    <h3 class="sub">Quién cantó más</h3>
    <ol>{ranking_html()}</ol>
    <p class="nota">Los {n_full} temas con toda la banda no suman acá.</p>
  </div>
</div></section>"""


MEDALLAS = [("oro", "Oro"), ("plata", "Plata"), ("bronce", "Bronce")]


def podio(cat, puestos):
    filas = "".join(
        f'<li class="{clase}"><span class="medalla" aria-label="{texto}">{i}</span>'
        f'<span class="quien"><b>{e(nombre)}</b>{f"<span>{e(det)}</span>" if det else ""}</span></li>'
        for i, ((clase, texto), (nombre, det)) in enumerate(zip(MEDALLAS, puestos), 1)
    )
    nombre_cat = cat.removeprefix("Mejor ")
    return f'<article class="podio-cat"><h3><small>Mejor</small>{e(nombre_cat[0].upper() + nombre_cat[1:])}</h3><ol>{filas}</ol></article>'


ganadores_html = f"""<section id="ganadores" class="bloque ganadores wrap" aria-labelledby="ganadores-tit">
  <header class="bloque-top">
    <p class="kicker">La votación</p>
    <h2 id="ganadores-tit">El medallero.</h2>
    <p>Votaron {resultados.VOTANTES} personas. Oro, plata y bronce en cada categoría.</p>
  </header>
  <div class="podios">{"".join(podio(c, p) for c, p in resultados.MEDALLERO)}</div>
</section>"""


def credito(c):
    enlace = c["page"] or c["url"]
    return f'<li><a href="{e(enlace)}">{e(c["name"])}</a></li>' if enlace else f'<li>{e(c["name"])}</li>'


credit_rows = "\n".join(credito(c) for c in creds)

def boton(grupo, valor, texto, marca=""):
    return f'<button type="button" class="f" data-grupo="{grupo}" data-v="{valor}" aria-pressed="false">{marca}{texto}</button>'


filters = (
    '<button type="button" class="f on" data-grupo="todos" aria-pressed="true">Todos</button>'
    + '<span class="grupo">' + "".join(boton("region", k, v) for k, v in REGIONES.items()) + "</span>"
    + '<span class="grupo">' + "".join(boton("nivel", k, v, estrellas(k)) for k, v in NIVELES.items()) + "</span>"
)

page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(TITULO)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Pacifico&display=swap" rel="stylesheet">
<style>
/* El flyer final hecho pagina: pizarra que baja a naranja y a noche, motivo dorado arriba y abajo,
   palo seco muy gruesa y apretada, y el script del Karaoke como unico gesto. Un solo tema, a proposito. */
:root {{
  color-scheme: dark;
  --oro: #c6a84f;
  --oro-claro: #ecd27c;
  --noche: #170e09;
  --blanco: #fff;
  --sans: "Outfit", "Helvetica Neue", Arial, sans-serif;
  --script: "Pacifico", "Brush Script MT", cursive;
  --g: clamp(16px, 2vw, 28px);
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; background: var(--noche); overflow-x: clip; }}
body {{ overflow-x: clip; }}
body {{ margin: 0; min-height: 100vh; display: flex; flex-direction: column; color: var(--blanco); font: 400 1rem/1.42 var(--sans);
  background: linear-gradient(180deg, #7f9295 0, #5f6e72 280px, #4c4e4d min(760px, 40%), #5a3a2c 58%, #642810 78%, var(--noche) 100%); }}
a {{ color: inherit; }}
button {{ font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; }}
:focus-visible {{ outline: 2px solid var(--blanco); outline-offset: 3px; }}
main {{ flex: 1 0 auto; }}
.wrap {{ width: 100%; max-width: 1280px; margin: 0 auto; padding: 0 clamp(20px, 4vw, 56px); }}
.st {{ display: inline-block; width: .82em; height: .82em; fill: currentColor; vertical-align: -.06em; }}

.hero {{ position: relative; overflow: hidden; padding: clamp(26px, 3.2vw, 44px) 0 clamp(24px, 2.8vw, 38px); }}
.hero::before {{ content: ""; position: absolute; inset: 0; opacity: .6;
  background: url("{PATRON}") right top / clamp(150px, 15.5vw, 218px) repeat;
  -webkit-mask-image: linear-gradient(90deg, transparent 52%, #000 88%); mask-image: linear-gradient(90deg, transparent 52%, #000 88%); }}
.hero .wrap {{ position: relative; }}
.hero-foto {{ position: absolute; top: 0; right: 0; width: min(44%, 640px); height: 100%; object-fit: cover; object-position: center 45%;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, rgba(0, 0, 0, .6) 22%, #000 48%); mask-image: linear-gradient(90deg, transparent 0, rgba(0, 0, 0, .6) 22%, #000 48%); }}
.hero .bajada {{ max-width: min(66ch, 54%); }}
@media (min-width: 641px) {{ .hero::before {{ display: none; }} }}
.hero h1 {{ margin: 0; font-weight: 800; font-size: clamp(3rem, 8.2vw, 6.9rem); line-height: 1; letter-spacing: -.04em; }}
.dress {{ margin: clamp(12px, 1.4vw, 20px) 0 0; font-weight: 600; font-size: clamp(1.15rem, 1.9vw, 1.5rem); line-height: 1.2; }}
.bajada {{ max-width: 66ch; text-wrap: balance; margin: 4px 0 0; font-size: clamp(1rem, 1.25vw, 1.08rem); }}

.filtros {{ position: sticky; top: 0; z-index: 2; background: rgba(52, 54, 54, .9); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); }}
.filtros .wrap {{ display: flex; align-items: center; gap: 8px clamp(14px, 1.6vw, 22px); padding-top: 15px; padding-bottom: 15px; }}
.f-tit {{ flex: none; margin: 0; font-weight: 800; font-size: 1rem; letter-spacing: -.01em; }}
.opciones {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px clamp(12px, 1.4vw, 20px); }}
.grupo {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.f {{ padding: 6px 12px 5px; border: 1px solid rgba(255, 255, 255, .45); border-radius: 99px; font-weight: 600; font-size: .9rem; white-space: nowrap; }}
.f .st {{ color: var(--oro-claro); margin-right: 1px; }}
.f .st:last-of-type {{ margin-right: 6px; }}
.f:hover {{ border-color: var(--oro-claro); color: var(--oro-claro); }}
.f.on, .f.on:hover {{ background: var(--oro-claro); border-color: var(--oro-claro); color: var(--noche); }}
.f.on .st {{ color: var(--noche); }}
.vacio {{ padding-top: 40px; margin-bottom: 0; }}
.vacio[hidden] {{ display: none; }}

.car {{ padding-top: clamp(30px, 4vw, 54px); }}
.filtros + .vacio + .car {{ padding-top: clamp(22px, 3vw, 36px); }}
.car[hidden] {{ display: none; }}
.car-top {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 2px 22px; margin-bottom: clamp(12px, 1.6vw, 20px); }}
.car-top h2 {{ margin: 0; font: 400 clamp(2.1rem, 3.8vw, 3.1rem)/1.3 var(--script); -webkit-text-stroke: .01em var(--blanco); transform: rotate(-2.5deg); transform-origin: left center; }}
.ctl {{ display: flex; align-items: center; gap: clamp(12px, 1.6vw, 20px); font-weight: 600; font-size: .92rem; }}
.count {{ font-variant-numeric: tabular-nums; }}
.pause {{ text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; min-width: 3.6em; text-align: left; }}
.arrow {{ display: inline-flex; padding: 8px 2px; }}
.arrow svg {{ display: block; width: 34px; height: 14px; fill: none; stroke: var(--blanco); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
.arrow:hover svg {{ stroke: var(--oro-claro); }}

.track {{ container-type: inline-size; display: flex; gap: var(--g); position: relative;
  overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; padding-bottom: 4px; }}
.track::-webkit-scrollbar {{ display: none; }}
@media (hover: hover) and (pointer: fine) {{ .track {{ cursor: grab; }} }}
.track.drag {{ cursor: grabbing; scroll-snap-type: none; user-select: none; }}
.look {{ flex: 0 0 calc((100cqw - 3 * var(--g)) / 4); min-width: 0; scroll-snap-align: start; }}
.look[hidden] {{ display: none; }}
.look img {{ display: block; width: 100%; height: calc((100cqw - 3 * var(--g)) / 4 * 1.25); object-fit: cover; }}
.look h3 {{ margin: 12px 0 4px; font-weight: 800; font-size: 1.28rem; line-height: 1.12; letter-spacing: -.02em; }}
.look p {{ margin: 0 0 6px; font-size: .95rem; line-height: 1.36; }}
.look .song {{ color: var(--oro-claro); }}
.look .song b {{ font-weight: 600; }}
.look .lvl {{ margin: 8px 0 0; font-size: .86rem; }}
.look .lvl .st {{ color: var(--oro-claro); margin-right: 1px; }}
.look .lvl .st:last-of-type {{ margin-right: 6px; }}

.cta {{ display: inline-flex; align-items: center; gap: 10px; margin-top: clamp(16px, 2vw, 24px); padding: 10px 18px 9px; border-radius: 99px;
  background: var(--oro-claro); color: var(--noche); font-weight: 800; font-size: 1.02rem; text-decoration: none; letter-spacing: -.01em; }}
.cta svg {{ width: 11px; height: 16px; fill: none; stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }}
.cta:hover {{ background: var(--blanco); }}
.ctas {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: clamp(22px, 2.6vw, 32px); }}
.ctas .cta {{ margin-top: 0; }}
.cta-votar {{ display: inline-flex; align-items: center; gap: 14px; padding: clamp(15px, 1.6vw, 20px) clamp(24px, 2.6vw, 36px); border-radius: 99px;
  background: var(--oro-claro); color: var(--noche); font-weight: 800; font-size: clamp(1.2rem, 2vw, 1.6rem); letter-spacing: -.02em; text-decoration: none;
  box-shadow: 0 0 0 3px var(--noche), 0 0 0 5px var(--oro-claro), 0 12px 36px rgba(23, 14, 9, .45); animation: brillo 2.4s ease-in-out infinite; }}
.cta-votar .st {{ width: .8em; height: .8em; }}
.cta-votar:hover {{ background: var(--blanco); animation: none; }}
@keyframes brillo {{ 0%, 100% {{ box-shadow: 0 0 0 3px var(--noche), 0 0 0 5px var(--oro-claro), 0 12px 36px rgba(23, 14, 9, .45); }}
  50% {{ box-shadow: 0 0 0 3px var(--noche), 0 0 0 5px var(--oro-claro), 0 0 46px 10px rgba(236, 210, 124, .55); }} }}
@media (prefers-reduced-motion: reduce) {{ .cta-votar {{ animation: none; }} }}
.ir-votar {{ flex: none; padding: 5px 13px 4px; border-radius: 99px; background: var(--blanco); color: var(--noche); font-weight: 800; font-size: .9rem; text-decoration: none; }}
.ir-votar:hover {{ background: var(--oro-claro); }}
.ir-temas {{ flex: none; margin-left: auto; font-weight: 600; font-size: .92rem; white-space: nowrap; color: var(--oro-claro);
  text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; }}
.ir-temas:hover {{ color: var(--blanco); }}

.temas {{ scroll-margin-top: 20px; }}
.tf-filtros {{ display: grid; grid-template-columns: minmax(0, 1fr); gap: 10px; margin: clamp(16px, 2vw, 24px) 0 clamp(14px, 1.8vw, 20px); }}
.tf-fila {{ display: flex; align-items: center; gap: 8px 14px; }}
.tf-tit {{ flex: none; width: 4.6em; margin: 0; font-weight: 800; font-size: .95rem; }}
.tf-ops {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.tf {{ padding: 6px 13px 5px; border: 1px solid rgba(255, 255, 255, .45); border-radius: 99px; font-weight: 600; font-size: .9rem; white-space: nowrap; }}
.tf:hover {{ border-color: var(--oro-claro); color: var(--oro-claro); }}
.tf[aria-pressed="true"], .tf[aria-pressed="true"]:hover {{ background: var(--oro-claro); border-color: var(--oro-claro); color: var(--noche); }}
.tf-cuenta {{ display: flex; align-items: baseline; gap: 16px; margin: 0 0 10px; font-weight: 600; font-size: .92rem; }}
.tf-cuenta .n {{ color: var(--oro-claro); font-variant-numeric: tabular-nums; margin-right: -.6em; }}
.tf-cuenta .n::after {{ content: " "; }}
.tf-limpiar {{ text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; font-weight: 600; }}
.tf-limpiar[hidden], .tf-vacio[hidden] {{ display: none; }}
.tf-vacio {{ margin: 8px 0 0; }}
.lista li[hidden] {{ display: none; }}
.lista {{ list-style: none; margin: 0; padding: 0; counter-reset: n; columns: 3 250px; column-gap: clamp(20px, 3vw, 44px); }}
.lista li {{ counter-increment: n; break-inside: avoid; display: grid; grid-template-columns: 2.7em 1fr; padding: 10px 0 11px; border-top: 1px solid rgba(255, 255, 255, .18); }}
.lista li::before {{ content: counter(n); grid-row: span 2; color: var(--oro-claro); font-weight: 600; font-size: .86rem; font-variant-numeric: tabular-nums; padding-top: .2em; }}
.lista b {{ font-weight: 800; font-size: 1.08rem; line-height: 1.2; letter-spacing: -.01em; }}
.lista span {{ font-size: .9rem; opacity: .82; }}
.lista li.elegido {{ scroll-margin: 90px; }}
.lista li.elegido b {{ color: var(--oro-claro); }}
.azar {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 18px; margin: 0 0 clamp(18px, 2.2vw, 26px); }}
.tirar {{ padding: 8px 16px 7px; border: 1px solid var(--oro-claro); border-radius: 99px; font-weight: 600; color: var(--oro-claro); }}
.tirar:hover {{ background: var(--oro-claro); color: var(--noche); }}
.sorteo {{ margin: 0; font-weight: 600; }}
.sorteo b {{ color: var(--oro-claro); }}
.pie ol.fuentes {{ columns: 2 260px; }}

.bloque-top {{ margin-bottom: clamp(20px, 2.6vw, 34px); }}
.bloque-top .kicker {{ margin: 0 0 10px; color: var(--oro-claro); font-weight: 800; font-size: .82rem; letter-spacing: .16em; text-transform: uppercase; }}
.bloque-top h2 {{ margin: 0; font-weight: 800; font-size: clamp(2.7rem, 6.4vw, 5rem); line-height: .96; letter-spacing: -.045em; }}
.bloque-top p:not(.kicker) {{ max-width: 62ch; margin: 12px 0 0; font-size: clamp(1rem, 1.25vw, 1.08rem); }}
.divisor {{ height: clamp(110px, 13vw, 170px); margin: clamp(40px, 5vw, 70px) 0; opacity: .55;
  background: url("{PATRON}") center / clamp(150px, 15.5vw, 218px) repeat-x;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 18%, #000 82%, transparent); mask-image: linear-gradient(90deg, transparent, #000 18%, #000 82%, transparent); }}
.bloque-noche {{ background: rgba(23, 14, 9, .32); padding: clamp(40px, 5vw, 70px) 0 clamp(44px, 5.5vw, 76px); border-top: 1px solid rgba(236, 210, 124, .35); border-bottom: 1px solid rgba(236, 210, 124, .35); }}
.sub {{ margin: clamp(36px, 4.5vw, 56px) 0 14px; font: 400 clamp(1.9rem, 3.2vw, 2.6rem)/1.3 var(--script); -webkit-text-stroke: .01em var(--blanco); transform: rotate(-2.5deg); transform-origin: left center; }}
.bloque-noche ol {{ list-style: none; margin: 0; padding: 0; }}
.rank ol {{ columns: 4 210px; column-gap: clamp(20px, 3vw, 40px); }}
.rank li {{ break-inside: avoid; display: grid; grid-template-columns: 2em 1fr auto; align-items: baseline; gap: 8px; padding: 7px 0 8px; border-top: 1px solid rgba(255, 255, 255, .18); }}
.rank .pos {{ color: var(--oro-claro); font-weight: 600; font-size: .9rem; font-variant-numeric: tabular-nums; }}
.rank b {{ font-weight: 800; font-size: 1.05rem; }}
.rank .c {{ font-size: .9rem; opacity: .82; font-variant-numeric: tabular-nums; }}
.rank .podio b {{ color: var(--oro-claro); font-size: 1.2rem; }}
.rank .nota {{ margin: 10px 0 0; font-size: .85rem; opacity: .8; }}
.setlist {{ counter-reset: s; columns: 3 250px; column-gap: clamp(20px, 3vw, 40px); }}
.setlist li {{ counter-increment: s; break-inside: avoid; display: grid; grid-template-columns: 2.2em 1fr; padding: 7px 0 8px; border-top: 1px solid rgba(255, 255, 255, .18); }}
.setlist li::before {{ content: counter(s); grid-row: span 2; color: var(--oro-claro); font-weight: 600; font-size: .86rem; font-variant-numeric: tabular-nums; padding-top: .15em; }}
.setlist b {{ font-weight: 800; font-size: 1rem; line-height: 1.2; }}
.setlist span {{ font-size: .88rem; opacity: .82; }}

.ganadores {{ scroll-margin-top: 20px; padding-top: clamp(40px, 5vw, 70px); }}
.podios {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: clamp(14px, 1.8vw, 22px); }}
.podio-cat {{ padding: clamp(18px, 2vw, 24px); border: 1px solid rgba(236, 210, 124, .45); border-radius: 18px; background: rgba(23, 14, 9, .28); }}
.podio-cat h3 {{ margin: 0 0 14px; white-space: nowrap; font: 400 1.55rem/1.3 var(--script); -webkit-text-stroke: .01em var(--blanco); transform: rotate(-2.5deg); transform-origin: left center; }}
.podio-cat h3 small {{ display: block; margin-bottom: 2px; font: 800 .72rem/1 var(--sans); letter-spacing: .16em; text-transform: uppercase; color: var(--oro-claro); -webkit-text-stroke: 0; }}
.podio-cat ol {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }}
.podio-cat li {{ display: grid; grid-template-columns: auto 1fr; gap: 12px; align-items: center; }}
.medalla {{ display: grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; font-weight: 800; font-size: .95rem; color: var(--noche);
  box-shadow: inset 0 -3px 0 rgba(0, 0, 0, .18), 0 0 0 2px rgba(255, 255, 255, .25); }}
.oro .medalla {{ width: 46px; height: 46px; font-size: 1.15rem; background: radial-gradient(circle at 35% 30%, #fff3c4, #ecd27c 45%, #b8913a); }}
.plata .medalla {{ background: radial-gradient(circle at 35% 30%, #ffffff, #d4d9dc 45%, #8e979c); }}
.bronce .medalla {{ background: radial-gradient(circle at 35% 30%, #f6d2b0, #cf8f5e 45%, #8c5230); }}
.quien b {{ display: block; font-weight: 800; font-size: 1.02rem; line-height: 1.2; letter-spacing: -.01em; }}
.oro .quien b {{ font-size: 1.3rem; color: var(--oro-claro); }}
.quien span {{ display: block; font-size: .88rem; opacity: .82; }}
@media (min-width: 1100px) {{
  .podios {{ grid-template-columns: repeat(5, minmax(0, 1fr)); }}
  .podio-cat {{ padding: 18px 16px; }}
  .podio-cat h3 {{ font-size: 1.32rem; }}
  .oro .quien b {{ font-size: 1.15rem; }}
  .quien b {{ font-size: .95rem; }}
}}

.pie {{ position: relative; margin-top: clamp(52px, 7vw, 90px); font-size: .86rem; overflow: hidden; }}
.pie .wrap {{ position: relative; z-index: 1; padding-bottom: clamp(70px, 9vw, 120px); }}
.pie::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: clamp(110px, 13vw, 170px); opacity: .5;
  background: url("{PATRON}") center top / clamp(150px, 15.5vw, 218px) repeat-x;
  -webkit-mask-image: linear-gradient(0deg, #000, transparent); mask-image: linear-gradient(0deg, #000, transparent); }}
.pie p {{ max-width: 72ch; margin: 0; }}
.pie summary {{ cursor: pointer; margin-top: 14px; font-weight: 600; }}
.pie ol {{ list-style: none; margin: 12px 0 0; padding: 0; columns: 4 150px; column-gap: 22px; }}
.pie li {{ break-inside: avoid; margin-bottom: 3px; }}

@media (max-width: 980px) {{
  .look {{ flex-basis: calc((100cqw - 2 * var(--g)) / 3); }}
  .look img {{ height: calc((100cqw - 2 * var(--g)) / 3 * 1.25); }}
}}
@media (max-width: 640px) {{
  .hero h1 {{ font-size: 13.4vw; }}
  .hero::before {{ opacity: .3; -webkit-mask-image: none; mask-image: none; }}
  .hero {{ padding-top: 0; }}
  .hero-foto {{ position: relative; display: block; width: 100%; height: 240px; margin-bottom: -40px; object-position: center 40%;
    -webkit-mask-image: linear-gradient(180deg, #000 55%, transparent); mask-image: linear-gradient(180deg, #000 55%, transparent); }}
  .hero .bajada {{ max-width: none; }}
  .filtros .wrap {{ flex-wrap: wrap; padding-top: 11px; padding-bottom: 11px; padding-right: 0; gap: 7px; }}
  .f-tit {{ font-size: .95rem; }}
  .opciones {{ flex-wrap: nowrap; width: 100%; overflow-x: auto; scrollbar-width: none; padding-right: 20px; }}
  .opciones::-webkit-scrollbar {{ display: none; }}
  .grupo {{ flex-wrap: nowrap; }}
  .f {{ flex: none; }}
  .ir-temas {{ order: 1; margin-left: auto; padding-right: 20px; }}
  .ir-votar {{ order: 1; margin-right: 20px; }}
  .opciones {{ order: 2; }}
  .tf-fila {{ flex-wrap: wrap; gap: 6px; margin-right: -20px; }}
  .tf-tit {{ width: auto; font-size: .9rem; }}
  .tf-ops {{ flex-wrap: nowrap; flex: 1 1 100%; min-width: 0; width: 100%; overflow-x: auto; scrollbar-width: none; padding-right: 20px; }}
  .tf-ops::-webkit-scrollbar {{ display: none; }}
  .tf {{ flex: none; }}
  .look {{ flex-basis: 74cqw; }}
  .look img {{ height: calc(74cqw * 1.25); }}
}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="estrella" viewBox="-43 -43 86 86"><path d="{ESTRELLA}"/></symbol></svg>
<header class="hero">
  <img class="hero-foto" src="img/fiesta.jpg" alt="La fiesta en pleno karaoke" width="1388" height="1400">
  <div class="wrap">
    <h1>{e(TITULO)}.</h1>
    <p class="dress">Y al final fueron {len(registro.NOCHE)}.</p>
    <p class="bajada">La noche estuvo a la altura del dresscode: looks espectaculares, {len(registro.NOCHE)} temas cantados (le ganamos al título) y hasta una visita de la policía, que tampoco se la quiso perder. Y ya votaron: acá están los ganadores.</p>
    <div class="ctas">{votar_hero}<a class="cta-votar" href="#ganadores"><svg class="st" aria-hidden="true"><use href="#estrella"/></svg>Ver el medallero<svg class="st" aria-hidden="true"><use href="#estrella"/></svg></a></div>
  </div>
</header>
<main>
{ganadores_html}
<div class="divisor" aria-hidden="true"></div>
{noche_html}
<div class="divisor" aria-hidden="true"></div>
<section id="looks" class="bloque" aria-labelledby="looks-tit">
<header class="bloque-top wrap">
  <p class="kicker">Para inspirarse</p>
  <h2 id="looks-tit">Ideas de looks.</h2>
  <p>{len(looks.L)} cantantes para armar el disfraz, del que se arma con lo que hay en casa a la producción total.</p>
</header>
<nav class="filtros" aria-label="Filtrar looks"><div class="wrap"><p class="f-tit">Filtrá los looks:</p><div class="opciones">{filters}</div><a class="ir-temas" href="#temas">¿Qué canto?</a>{votar_nav}</div></nav>
<p class="vacio wrap" hidden>No hay looks con esos filtros. Probá sacando alguno.</p>
{chr(10).join(secciones)}
</section>
<div class="divisor" aria-hidden="true"></div>
<section id="temas" class="bloque temas wrap" aria-labelledby="temas-tit">
  <header class="bloque-top">
    <p class="kicker">Para animarse</p>
    <h2 id="temas-tit">¿No sabés qué cantar?</h2>
    <p>{total_temas} temas que nunca fallan en un karaoke, sacados de listas de los más cantados, con muchos de acá. Combiná los filtros como quieras.</p>
  </header>
  <div class="tf-filtros" role="group" aria-label="Filtrar temas">
{filtros_temas_html}
  </div>
  <div class="azar">
    <button type="button" class="tirar">Tirame uno al azar</button>
    <p class="sorteo" aria-live="polite"></p>
  </div>
  <p class="tf-cuenta" aria-live="polite"><span class="n">{total_temas}</span> temas<button type="button" class="tf-limpiar" hidden>Sacar filtros</button></p>
  <ol class="lista">{lista_html}</ol>
  <p class="tf-vacio" hidden>No hay temas con esa combinación. Probá sacando algún filtro.</p>
</section>
</main>
<footer class="pie"><div class="wrap">
  <p>Página privada y sin fines comerciales, hecha solo para los invitados del cumple de Maru. Las fotos pertenecen a sus autores y se usan únicamente como referencia de vestuario. Si alguna es tuya y preferís que no esté, avisanos y la sacamos.</p>
  <details>
    <summary>De dónde salieron las fotos</summary>
    <ol>
{credit_rows}
    </ol>
  </details>
  <details>
    <summary>De dónde salieron los temas</summary>
    <ol class="fuentes">
{fuentes_html}
    </ol>
  </details>
</div></footer>
<script>
const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
const INTERVALO = 3600;
const carruseles = [...document.querySelectorAll('.car')].map((car, i) => {{
  const track = car.querySelector('.track');
  const count = car.querySelector('.count');
  const pauseBtn = car.querySelector('.pause');
  const st = {{ paused: quieto, hover: false, focus: false, visible: true, holdUntil: 0 }};
  const items = () => [...track.querySelectorAll('.look:not([hidden])')];
  const pos = el => el.offsetLeft;
  const actual = () => {{
    const list = items();
    let idx = 0;
    list.forEach((el, n) => {{ if (pos(el) <= track.scrollLeft + 4) idx = n; }});
    return {{ list, idx }};
  }};
  const pinta = () => {{ const {{ list, idx }} = actual(); count.textContent = list.length ? (idx + 1) + ' / ' + list.length : ''; }};
  const ir = left => track.scrollTo({{ left, behavior: quieto ? 'auto' : 'smooth' }});
  const alFinal = () => track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
  const sig = () => {{ const {{ list, idx }} = actual(); ir(alFinal() || idx >= list.length - 1 ? 0 : pos(list[idx + 1])); }};
  const ant = () => {{
    const {{ list, idx }} = actual();
    if (!list.length) return;
    ir(track.scrollLeft <= 4 ? track.scrollWidth : pos(list[idx - 1] || list[0]));
  }};
  const pinPausa = () => {{ pauseBtn.textContent = st.paused ? 'Seguir' : 'Pausar'; }};
  const espera = () => {{ st.holdUntil = Date.now() + 9000; }};
  car.querySelector('.next').addEventListener('click', () => {{ espera(); sig(); }});
  car.querySelector('.prev').addEventListener('click', () => {{ espera(); ant(); }});
  pauseBtn.addEventListener('click', () => {{ st.paused = !st.paused; pinPausa(); }});
  track.addEventListener('scroll', pinta, {{ passive: true }});
  track.addEventListener('pointerdown', espera, {{ passive: true }});
  // arrastre con mouse; con el dedo el navegador ya desliza solo
  let drag = null;
  let finSnap = 0;
  track.addEventListener('dragstart', e => e.preventDefault());
  track.addEventListener('pointerdown', e => {{
    if (e.pointerType !== 'mouse' || e.button !== 0) return;
    clearTimeout(finSnap);
    drag = {{ x: e.clientX, left: track.scrollLeft }};
    track.setPointerCapture(e.pointerId);
    track.classList.add('drag');
  }});
  track.addEventListener('pointermove', e => {{
    if (!drag) return;
    track.scrollLeft = drag.left - (e.clientX - drag.x);
    espera();
  }});
  const soltar = () => {{
    if (!drag) return;
    drag = null;
    espera();
    const cerca = items().reduce((a, b) => Math.abs(pos(b) - track.scrollLeft) < Math.abs(pos(a) - track.scrollLeft) ? b : a);
    ir(pos(cerca));
    finSnap = setTimeout(() => track.classList.remove('drag'), 500);
  }};
  track.addEventListener('pointerup', soltar);
  track.addEventListener('pointercancel', soltar);
  track.addEventListener('touchstart', espera, {{ passive: true }});
  track.addEventListener('wheel', espera, {{ passive: true }});
  track.addEventListener('pointerenter', e => {{ if (e.pointerType === 'mouse') st.hover = true; }});
  track.addEventListener('pointerleave', () => {{ st.hover = false; }});
  car.addEventListener('focusin', e => {{ st.focus = e.target.matches(':focus-visible'); }});
  car.addEventListener('focusout', () => {{ st.focus = false; }});
  track.addEventListener('keydown', e => {{
    if (e.key === 'ArrowRight') {{ e.preventDefault(); espera(); sig(); }}
    if (e.key === 'ArrowLeft') {{ e.preventDefault(); espera(); ant(); }}
  }});
  if ('IntersectionObserver' in window) {{
    new IntersectionObserver(es => {{ st.visible = es[0].isIntersecting; }}, {{ threshold: 0 }}).observe(car);
  }}
  setTimeout(() => setInterval(() => {{
    if (!st.paused && !st.hover && !st.focus && st.visible && !document.hidden && Date.now() > st.holdUntil) sig();
  }}, INTERVALO), i * 1200);
  pinPausa();
  pinta();
  return {{ car, track, items, pinta }};
}});
const btns = [...document.querySelectorAll('.f')];
const vacio = document.querySelector('.vacio');
const activos = {{ region: new Set(), nivel: new Set() }};
const aplicar = () => {{
  btns.forEach(b => {{
    const on = b.dataset.grupo === 'todos' ? !activos.region.size && !activos.nivel.size : activos[b.dataset.grupo].has(b.dataset.v);
    b.classList.toggle('on', on);
    b.setAttribute('aria-pressed', on);
  }});
  let hay = false;
  carruseles.forEach(c => {{
    c.track.querySelectorAll('.look').forEach(l => {{ l.hidden = activos.nivel.size > 0 && !activos.nivel.has(l.dataset.level); }});
    const ok = (!activos.region.size || activos.region.has(c.car.dataset.region)) && c.items().length > 0;
    c.car.hidden = !ok;
    hay = hay || ok;
    c.track.scrollLeft = 0;
    c.pinta();
  }});
  vacio.hidden = hay;
}};
btns.forEach(b => b.addEventListener('click', () => {{
  if (b.dataset.grupo === 'todos') {{
    activos.region.clear();
    activos.nivel.clear();
  }} else {{
    const set = activos[b.dataset.grupo];
    set.has(b.dataset.v) ? set.delete(b.dataset.v) : set.add(b.dataset.v);
  }}
  aplicar();
}}));
const tfBtns = [...document.querySelectorAll('.tf')];
const temasLi = [...document.querySelectorAll('.lista li')];
const sorteo = document.querySelector('.sorteo');
const cuentaN = document.querySelector('.tf-cuenta .n');
const limpiar = document.querySelector('.tf-limpiar');
const tfVacio = document.querySelector('.tf-vacio');
const tfAct = {{ o: new Set(), g: new Set(), d: new Set() }};
const filtrarTemas = () => {{
  tfBtns.forEach(b => b.setAttribute('aria-pressed', tfAct[b.dataset.grupo].has(b.dataset.v)));
  let n = 0;
  temasLi.forEach(li => {{
    const ok = (!tfAct.o.size || tfAct.o.has(li.dataset.o))
      && (!tfAct.g.size || li.dataset.g.split(' ').some(g => tfAct.g.has(g)))
      && (!tfAct.d.size || tfAct.d.has(li.dataset.d));
    li.hidden = !ok;
    li.classList.remove('elegido');
    if (ok) n++;
  }});
  cuentaN.textContent = n;
  limpiar.hidden = !(tfAct.o.size || tfAct.g.size || tfAct.d.size);
  tfVacio.hidden = n > 0;
  sorteo.textContent = '';
}};
tfBtns.forEach(b => b.addEventListener('click', () => {{
  const set = tfAct[b.dataset.grupo];
  set.has(b.dataset.v) ? set.delete(b.dataset.v) : set.add(b.dataset.v);
  filtrarTemas();
}}));
limpiar.addEventListener('click', () => {{ Object.values(tfAct).forEach(x => x.clear()); filtrarTemas(); }});
document.querySelector('.tirar').addEventListener('click', () => {{
  const visibles = temasLi.filter(li => !li.hidden);
  if (!visibles.length) return;
  const previo = visibles.find(li => li.classList.contains('elegido'));
  let li;
  do {{ li = visibles[Math.floor(Math.random() * visibles.length)]; }} while (visibles.length > 1 && li === previo);
  temasLi.forEach(x => x.classList.toggle('elegido', x === li));
  sorteo.innerHTML = 'Te toca: <b>' + li.querySelector('b').textContent + '</b>, de ' + li.querySelector('span').textContent.split(' · ')[0] + '.';
}});
</script>
</body>
</html>
"""
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print("ok", len(looks.L), "looks")
