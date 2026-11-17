"""Render the Norwegian campaign copy (Markdown in the private maren-project repo) into review pages.

Run: python3 build_copy.py   (needs the `markdown` package)
Reads  ~/maren-project/copy/09-black-week-christmas/no/*.md
Writes copy/<name>.html next to this file. [Maren, bekreft: ...] markers are highlighted.
"""
import re
from pathlib import Path

import markdown

SRC = Path.home() / "maren-project/copy/09-black-week-christmas/no"
OUT = Path(__file__).resolve().parent / "copy"
DOCS = [
    ("00-plan-no", "plan", "Kampanjeplan · Julen 2026"),
    ("01-vsl-script-no", "vsl", "VSL-manus · 20 minutter"),
    ("02-pages-no", "sider", "Sidene · alle tilstander"),
    ("03-emails-no", "e-poster", "E-postene"),
    ("04-calendar-no", "kalender", "Romjulskalenderen · 8 luker"),
    ("05-live-qa-no", "live-qa", "Live Q&A · 26. november og 10. desember"),
    ("06-sms-no", "sms", "SMS · 12 meldinger"),
    (str(Path.home() / "maren-project/docs/build-instructions-round-1"), "build", "Build · runde 1"),
]
CSS = """
:root{--navy:#274472;--navy-dd:#142340;--gold:#AB9461;--gold-d:#8a7340;--gold-l:#d8c79c;--cream:#f4efe5;--bg:#FAF9F6;--sand:#EDE7DB;--ink:#1f2a3d;--slate:#5d6a82}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--navy)}a:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.bar{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid var(--sand);padding:8px 16px;display:flex;flex-wrap:wrap;gap:2px;align-items:center}
.bar a{display:inline-flex;align-items:center;min-height:44px;padding:0 10px;border-radius:8px;color:var(--slate);text-decoration:none;font-size:.92rem}
.bar a:hover{color:var(--navy);background:var(--cream)}
.bar a.on{color:var(--navy);font-weight:600;box-shadow:inset 0 -2px 0 var(--gold)}
.hd{background:var(--bg);color:var(--slate);padding:40px 16px 8px}
.hd div{max-width:1120px;margin:0 auto}
.hd small{display:block;font-size:.74rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#74602f;margin-bottom:10px}
.hd h1{font:600 clamp(2.2rem,6vw,3.2rem)/1.1 'Cormorant Garamond',Georgia,serif;color:var(--navy);margin:0 0 10px}
.hd p{margin:0;max-width:620px}
.hd mark{background:#ffe08a;color:var(--ink);padding:0 5px;border-radius:4px}
.lay{max-width:1120px;margin:0 auto;padding:40px 16px 96px;display:grid;gap:40px}
@media(min-width:1000px){.lay{grid-template-columns:240px minmax(0,1fr)}.toc{position:sticky;top:72px;align-self:start;max-height:calc(100vh - 96px);overflow:auto}}
.toc{font-size:.88rem}
.toc b{display:block;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--slate);margin-bottom:8px}
.toc ul{list-style:none;margin:0;padding:0}.toc ul ul{display:none}
.toc a{display:block;padding:6px 10px;border-left:2px solid var(--sand);color:var(--slate);text-decoration:none}
.toc a:hover{color:var(--navy);border-color:var(--gold)}
article{max-width:720px;min-width:0}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;color:var(--navy);line-height:1.15}
article h1{font-size:2.2rem;margin-top:0}
article h2{font-size:1.9rem;margin:2.2em 0 .6em;padding-top:1.2em;border-top:1px solid var(--sand);scroll-margin-top:72px}
article h3{font-size:1.4rem;margin:1.8em 0 .4em;scroll-margin-top:72px}
blockquote{margin:1.2em 0;padding:14px 20px;border-left:3px solid var(--gold);background:#fff;border-radius:0 14px 14px 0}
blockquote p{margin:.4em 0}
table{border-collapse:collapse;width:100%;background:#fff;font-size:.9rem;display:block;overflow-x:auto;border-radius:12px;border:1px solid var(--sand)}
th,td{border-bottom:1px solid var(--sand);padding:10px 12px;text-align:left;vertical-align:top}
th{background:var(--cream);color:var(--navy)}
code{background:var(--cream);padding:1px 6px;border-radius:5px;font-size:.88em}
hr{border:0;border-top:1px solid var(--sand);margin:2em 0}
mark{background:#ffe08a;padding:1px 4px;border-radius:4px}
"""


def page(slug, title, body, toc, count):
    nav = '<a href="../" style="font:600 1.2rem Cormorant Garamond,Georgia,serif;color:#274472;margin-right:8px">Det lille pusterommet · Julen 2026</a>' + "".join(
        f'<a href="{s}.html"{" class=on" if s == slug else ""}>{t.split(" ·")[0]}</a>' for _, s, t in DOCS)
    return f"""<!doctype html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>{title} · Jul 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}body{{font-variant-numeric:lining-nums}}</style></head><body><nav class="bar" aria-label="Dokumenter">{nav}</nav>
<header class="hd"><div><small>Jul 2026 · til godkjenning</small><h1>{title}</h1><p>Utkast. <mark>Gult</mark> betyr at Maren må bekrefte noe ({count} steder).</p></div></header>
<div class="lay"><nav class="toc" aria-label="Innhold"><b>Innhold</b>{toc}</nav><article>{body}</article></div></body></html>"""


OUT.mkdir(exist_ok=True)
for name, slug, title in DOCS:
    text = (Path(f"{name}.md") if name.startswith("/") else SRC / f"{name}.md").read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"])
    html = md.convert(text)
    toc = md.toc
    html, n = re.subn(r"\[Maren, bekreft:[^\]]*\]", lambda m: f"<mark>{m.group(0)}</mark>", html)
    (OUT / f"{slug}.html").write_text(page(slug, title, html, toc, n), encoding="utf-8")
    print("ok", slug, n)
