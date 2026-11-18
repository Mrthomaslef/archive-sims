"""Convertit les fiches Markdown en données pour la web-app (app/fiches.json + app/embedded_data.js)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FICHES = ROOT / "fiches"
OUT = ROOT / "app"
OUT.mkdir(exist_ok=True)


def front(txt):
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    meta, body = {}, txt
    if m:
        body = txt[m.end():]
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    return meta, body


congres = []
for d in sorted(p for p in FICHES.iterdir() if p.is_dir()):
    m = re.match(r"SIMS (\d{4}) - (.+)", d.name)
    if not m:
        continue
    year, theme = m.groups()
    items = []
    for f in sorted(d.glob("*.md"), key=lambda p: p.stem.lower()):
        if f.stem.endswith("- Index"):
            continue
        meta, body = front(f.read_text(encoding="utf-8"))
        h1 = re.search(r"^# (.+)$", body, re.M)
        resume = re.search(r"> \[!abstract\][^\n]*\n> (.+)", body)
        body = re.sub(r"^# .+\n+", "", body.lstrip(), count=1)
        # La section « Liens » est remplacée par la navigation de l'app ; on garde les « Voir aussi ».
        voir = re.findall(r"\[\[([^\]|]+)", body.split("## Liens")[-1]) if "## Liens" in body else []
        body = body.split("## Liens")[0].rstrip()
        doublon = re.findall(r"https://www\.youtube\.com/watch\?v=[\w-]+", meta.get("video", "") + " " + " ".join(re.findall(r"Doublon[^\n]*", f.read_text(encoding="utf-8"))))
        tags = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]
        items.append({
            "id": f"{year}-{len(items) + 1:02d}",
            "slug": f.stem,
            "titre": h1.group(1).strip() if h1 else f.stem,
            "orateur": meta.get("orateur", ""),
            "duree": meta.get("duree", ""),
            "video": meta.get("video", "").split()[0] if meta.get("video") else "",
            "videos": list(dict.fromkeys(doublon)),
            "resume": resume.group(1).strip() if resume else "",
            "tags": [t for t in tags if t not in ("sims", "congres-sims")],
            "voir": [v for v in voir if not v.endswith("- Index")],
            "md": body,
        })
    congres.append({"annee": year, "theme": theme, "fiches": items})

data = {"titre": "Archive SIMS", "congres": congres, "total": sum(len(c["fiches"]) for c in congres)}
(OUT / "fiches.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
(OUT / "embedded_data.js").write_text("window.SIMS_DATA=" + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
print({c["annee"]: len(c["fiches"]) for c in congres}, "total", data["total"])
