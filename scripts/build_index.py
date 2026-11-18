"""Génère les index par année (SIMS AAAA - Index.md) et l'accueil, puis vérifie les wikilinks."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "fiches"
THEMES = {}
fiches = {}
for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
    m = re.match(r"SIMS (\d{4}) - (.+)", d.name)
    if not m:
        continue
    year, theme = m.groups()
    THEMES[year] = (theme, d)
    for f in sorted(d.glob("*.md")):
        if f.stem.endswith("- Index"):
            continue
        txt = f.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", txt, re.M)
        orateur = re.search(r'^orateur:\s*"?(.*?)"?\s*$', txt, re.M)
        duree = re.search(r"^duree:\s*(\d+)", txt, re.M)
        video = re.search(r"^video:\s*(\S+)", txt, re.M)
        resume = re.search(r"> \[!abstract\][^\n]*\n> (.+)", txt)
        fiches.setdefault(year, []).append({
            "stem": f.stem,
            "titre": h1.group(1).strip() if h1 else f.stem,
            "orateur": orateur.group(1) if orateur else "",
            "duree": duree.group(1) if duree else "",
            "video": video.group(1) if video else "",
            "resume": resume.group(1).replace("**", "").strip() if resume else "",
        })

def cell(s):
    return s.replace("|", "\\|")

for year, (theme, d) in THEMES.items():
    L = fiches.get(year, [])
    lines = [
        "---", f"tags: [sims, congres-sims, index]", f"congres: SIMS {year}",
        f"theme: {theme}", "statut: index", "---", "",
        f"# SIMS {year} - {theme}", "",
        f"> [!info] {len(L)} fiches résumé, générées depuis les vidéos archivées sur la chaîne YouTube (transcriptions automatiques).",
        "", "Retour : [[00 - Congrès SIMS - Accueil]]", "",
        "| Communication | Orateur | En une phrase | Vidéo |", "|---|---|---|---|",
    ]
    for x in L:
        vid = f"[▶ {x['duree']} min]({x['video']})" if x["video"] else ""
        lines.append(f"| [[{x['stem']}]] | {cell(x['orateur'])} | {cell(x['resume'])} | {vid} |")
    (d / f"SIMS {year} - Index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

home = [
    "---", "tags: [sims, congres-sims, accueil]", "statut: index", "---", "",
    "# Congrès SIMS - Fiches résumé par année", "",
    "Société d'Imagerie Musculo-Squelettique : fiches tirées des vidéos archivées (privées) de la chaîne YouTube.", "",
    "| Année | Thème | Fiches |", "|---|---|---|",
]
for year in sorted(THEMES):
    theme, _ = THEMES[year]
    home.append(f"| **{year}** | [[SIMS {year} - Index\\|{theme}]] | {len(fiches.get(year, []))} |")
home += ["", "> [!WARNING] Fiches issues de sous-titres automatiques : vérifier sur la vidéo tout chiffre, seuil ou nom propre avant de le citer.", ""]
(ROOT / "00 - Congrès SIMS - Accueil.md").write_text("\n".join(home) + "\n", encoding="utf-8")

# Vérification des wikilinks
names = {p.stem for p in ROOT.rglob("*.md")}
broken = []
for p in ROOT.rglob("*.md"):
    if p.name == "_MODELE.md":
        continue
    for link in re.findall(r"\[\[([^\]|#\\]+)", p.read_text(encoding="utf-8")):
        if link.strip() not in names:
            broken.append((p.relative_to(ROOT), link))
print({y: len(v) for y, v in sorted(fiches.items())}, "total", sum(map(len, fiches.values())))
print("liens cassés:", len(broken))
for b in broken:
    print("  ", *b)
