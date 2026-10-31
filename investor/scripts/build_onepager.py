#!/usr/bin/env python3
"""Render investor/one-pager.md -> one-pager.html -> one-pager.pdf (Letter, 1 page) with Playwright.

pip install markdown playwright ; Chromium is taken from /opt/pw-browsers (override with CHROME=).
"""
import base64
import glob
import os
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "investor"
FONTS = ROOT / "brand/typography/fonts"


def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def chrome_path():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    c = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
    return c[-1] if c else None


md = (INV / "one-pager.md").read_text()
title_line, body = md.split("\n", 1)
body_html = markdown.markdown(body, extensions=["tables"])
logo = ROOT / "brand/logo/png/lore-lockup-horizontal-bone-1600w.png"
hero = INV / "assets/lineup.png"

css = f"""
@font-face {{ font-family: Fraunces; src: url(data:font/woff2;base64,{b64(FONTS/'fraunces-latin-full-normal.woff2')}) format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: Inter; src: url(data:font/woff2;base64,{b64(FONTS/'inter-latin-opsz-normal.woff2')}) format('woff2'); font-weight: 100 900; }}
:root {{ --ink:#14161A; --bone:#F3EEE6; --terra:#C4623A; --brass:#B8935A; --muted:#5A5D63; }}
@page {{ size: Letter; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background: var(--bone); color: var(--ink); font: 8.6pt/1.36 Inter, Arial, sans-serif; }}
header {{ background: var(--ink); color: var(--bone); padding: 18px 34px 14px; display:flex; align-items:center; gap: 22px; }}
header img.logo {{ height: 26px; }}
header h1 {{ font: 500 20pt/1.1 Fraunces, Georgia, serif; margin:0; flex:1; }}
header img.hero {{ height: 62px; border-radius: 4px; }}
main {{ padding: 10px 34px 8px; column-count: 2; column-gap: 26px; }}
h2 {{ font: 600 10.5pt/1.2 Fraunces, Georgia, serif; color: var(--terra); margin: 9px 0 3px; break-after: avoid; }}
p {{ margin: 0 0 5px; }}
ul {{ margin: 0 0 5px; padding-left: 15px; }}
li {{ margin-bottom: 2px; }}
table {{ border-collapse: collapse; width: 100%; margin: 3px 0 6px; font-size: 7.8pt; break-inside: avoid; }}
th {{ background: var(--ink); color: var(--bone); text-align:left; padding: 3px 5px; font-weight:600; }}
td {{ padding: 3px 5px; border-bottom: 1px solid #DDD5C8; }}
strong {{ font-weight: 650; }}
em {{ color: var(--muted); }}
main > p:first-child, main > p:nth-child(2) {{ column-span: all; }}
main > p:nth-child(2) {{ background: var(--terra); color: #fff; padding: 6px 10px; border-radius: 3px; font-size: 9.5pt; }}
"""
html = f"""<!doctype html><html><head><meta charset="utf-8"><title>LORE one-pager</title>
<style>{css}</style></head><body>
<header><img class="logo" src="data:image/png;base64,{b64(logo)}"><h1>Every street has a story.</h1>
{'<img class="hero" src="data:image/png;base64,' + b64(hero) + '">' if hero.exists() else ''}</header>
<main>{body_html}</main></body></html>"""
(INV / "one-pager.html").write_text(html)

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=chrome_path())
    pg = b.new_page()
    pg.set_content(html, wait_until="load")
    pg.pdf(path=str(INV / "one-pager.pdf"), format="Letter", print_background=True)
    pg.set_viewport_size({"width": 816, "height": 1056})
    pg.screenshot(path=str(INV / "render/one-pager.png"), full_page=True)
    b.close()
print("wrote one-pager.html, one-pager.pdf, render/one-pager.png")
