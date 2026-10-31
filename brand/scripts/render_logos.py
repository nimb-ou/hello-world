"""Render every logo SVG to PNG (transparent, 2x/1024) + favicon set + .ico."""
import glob, json, os, subprocess, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.normpath(os.path.join(HERE, "..", "logo"))
PNG = os.path.join(LOGO, "png")
os.makedirs(PNG, exist_ok=True)
jobs = []
for svg in sorted(glob.glob(os.path.join(LOGO, "svg", "*.svg"))):
    name = os.path.basename(svg)[:-4]
    if name.startswith("lore-app-icon"):
        jobs.append({"in": svg, "out": os.path.join(PNG, name + ".png"), "width": 1024, "height": 1024})
    elif name == "favicon":
        for s in (16, 32, 48, 180, 192, 512):
            jobs.append({"in": svg, "out": os.path.join(PNG, f"favicon-{s}.png"), "width": s, "height": s})
    elif "symbol" in name or "glyph" in name:
        jobs.append({"in": svg, "out": os.path.join(PNG, name + "-512.png"), "width": 512})
    else:
        jobs.append({"in": svg, "out": os.path.join(PNG, name + "-1600w.png"), "width": 1600})
for sheet in ("concepts", "construction", "clearspace", "misuse", "logo-overview"):
    jobs.append({"in": os.path.join(LOGO, sheet + ".svg"), "out": os.path.join(PNG, sheet + ".png")})
# app icon store sizes
for s in (180, 120, 87, 58):
    jobs.append({"in": os.path.join(LOGO, "svg", "lore-app-icon-1024.svg"), "out": os.path.join(PNG, f"app-icon-{s}.png"), "width": s, "height": s})
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    json.dump(jobs, fh)
subprocess.run(["node", os.path.join(HERE, "render.js"), "--batch", fh.name], check=True, cwd=HERE)
# apple-touch-icon must be opaque; app icons opaque by construction
imgs = [Image.open(os.path.join(PNG, f"favicon-{s}.png")).convert("RGBA") for s in (16, 32, 48)]
imgs[2].save(os.path.join(LOGO, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:2])
print("favicon.ico written")
