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
    ("01-vsl-script-no", "vsl", "VSL-manus · 20 minutter"),
    ("02-pages-no", "sider", "Sidene · alle tilstander"),
    ("03-emails-no", "e-poster", "E-postene"),
    ("04-calendar-no", "kalender", "Romjulskalenderen · 8 luker"),
    ("05-live-qa-no", "live-qa", "Live Q&A · 11. desember"),
]
CSS = """
body{margin:0;background:#FAF9F6;color:#1f2a3d;font:17px/1.65 Inter,system-ui,sans-serif}
.top{position:sticky;top:0;background:#111a2b;padding:8px 16px;display:flex;flex-wrap:wrap;gap:6px}
.top a{display:inline-flex;align-items:center;min-height:36px;padding:4px 12px;border-radius:999px;color:#e6ebf4;text-decoration:none;border:1px solid rgba(255,255,255,.18);font-size:.85rem}
.top a.on{background:#8a7340;border-color:#8a7340}
main{max-width:820px;margin:0 auto;padding:32px 16px 80px}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;color:#274472;line-height:1.15}
h1{font-size:2.4rem}h2{font-size:1.8rem;margin-top:2em;border-top:1px solid #EDE7DB;padding-top:1em}h3{font-size:1.35rem}
blockquote{margin:1em 0;padding:4px 18px;border-left:3px solid #AB9461;background:#fff}
table{border-collapse:collapse;width:100%;background:#fff;font-size:.92rem;display:block;overflow-x:auto}
th,td{border-bottom:1px solid #EDE7DB;padding:8px 10px;text-align:left;vertical-align:top}
code{background:#f4efe5;padding:1px 5px;border-radius:4px}
mark{background:#ffe08a;padding:1px 4px;border-radius:4px}
.n{font-size:.85rem;color:#5d6a82;margin:0 0 24px}
"""


def page(slug, title, body, count):
    nav = '<a href="../">← Oversikt</a>' + "".join(
        f'<a href="{s}.html"{" class=on" if s == slug else ""}>{t.split(" ·")[0]}</a>' for _, s, t in DOCS)
    return f"""<!doctype html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>{title} · Black Week + jul 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><nav class="top">{nav}</nav><main>
<p class="n">Utkast til godkjenning. Gult merke = Maren må bekrefte ({count} steder).</p>
{body}</main></body></html>"""


OUT.mkdir(exist_ok=True)
for name, slug, title in DOCS:
    text = (SRC / f"{name}.md").read_text(encoding="utf-8")
    html = markdown.markdown(text, extensions=["tables", "sane_lists"])
    html, n = re.subn(r"\[Maren, bekreft:[^\]]*\]", lambda m: f"<mark>{m.group(0)}</mark>", html)
    (OUT / f"{slug}.html").write_text(page(slug, title, html, n), encoding="utf-8")
    print("ok", slug, n)
