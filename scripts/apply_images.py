"""Intègre les images clés choisies (data/selections/<videoId>.json) dans les fiches.

Sélection : {"fiche": "<chemin relatif>", "images": [{"frame": 12, "legende": "...", "crop": [x0, y0, x1, y1]}]}
(crop en fractions de l'image 1280x720, optionnel).
Sortie : img/<année>/<videoId>-<n>.jpg + section « ## Images clés » dans la fiche.
Usage : /tmp/simsfr/venv/bin/python scripts/apply_images.py   (nécessite Pillow)
"""
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FRAMES = ROOT / "data" / "frames"
SEL = ROOT / "data" / "selections"
IMG = ROOT / "img"


def mmss(t):
    t = int(float(t))
    return f"{t // 60}:{t % 60:02d}"


n_img = n_fiche = 0
for sp in sorted(SEL.glob("*.json")):
    vid = sp.stem
    sel = json.loads(sp.read_text(encoding="utf-8"))
    fiche = ROOT / sel["fiche"]
    if not fiche.exists():
        print("fiche introuvable", sel["fiche"]); continue
    year = re.search(r"SIMS (\d{4})", sel["fiche"]).group(1)
    times = (FRAMES / vid / "times.txt").read_text().split()
    out = IMG / year
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob(f"{vid}-*.jpg"):
        old.unlink()
    lines = []
    for k, im in enumerate(sel.get("images", [])[:4], 1):
        src = FRAMES / vid / f"f{int(im['frame']):03d}.jpg"
        if not src.exists():
            print("frame manquante", vid, im["frame"]); continue
        img = Image.open(src).convert("RGB")
        c = im.get("crop")
        if c and len(c) == 4 and 0 <= c[0] < c[2] <= 1 and 0 <= c[1] < c[3] <= 1:
            W, H = img.size
            img = img.crop((round(c[0] * W), round(c[1] * H), round(c[2] * W), round(c[3] * H)))
        img.thumbnail((1100, 1100))
        name = f"{vid}-{k}.jpg"
        img.save(out / name, quality=82, optimize=True, progressive=True)
        t = times[int(im["frame"]) - 1] if int(im["frame"]) - 1 < len(times) else "0"
        leg = im["legende"].replace("]", ")").replace("[", "(").strip()
        lines.append(f"![{leg}](../../img/{year}/{name}) [▶ {mmss(t)}](https://www.youtube.com/watch?v={vid}&t={int(float(t))}s)")
        n_img += 1
    txt = fiche.read_text(encoding="utf-8")
    txt = re.sub(r"\n## Images clés\n.*?(?=\n## |\n> \[!|\Z)", "\n", txt, flags=re.S)
    if lines:
        block = "\n## Images clés\n" + "\n".join(lines) + "\n"
        # Après « À retenir » si présent, sinon après l'abstract, sinon avant « Points clés ».
        m = re.search(r"> \[!success\][^\n]*\n(?:>[^\n]*\n)*", txt) or re.search(r"> \[!abstract\][^\n]*\n(?:>[^\n]*\n)*", txt)
        if m:
            txt = txt[:m.end()] + block + txt[m.end():]
        else:
            txt = txt.replace("\n## Points clés", block + "\n## Points clés", 1)
        n_fiche += 1
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    fiche.write_text(txt, encoding="utf-8")
print(f"{n_img} images dans {n_fiche} fiches")
