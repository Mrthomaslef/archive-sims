<img src="assets/icon.svg" width="64" height="64" alt="">

# Archive sims

Created in [T3 Code](https://t3.codes).

## Contenu

- `fiches/` : fiches résumé des congrès SIMS, au format Obsidian et rangées par année. Le point d'entrée est `00 - Congrès SIMS - Accueil.md`.
  - 2017 Genou : 35 fiches
  - 2019 Hanche : 42 fiches
  - 2022 Main et poignet : 40 fiches
  - 2024 Pied et cheville : 40 fiches
- `data/videos.json` : liste des vidéos de la chaîne, extraite de YouTube Studio.
- `data/lots/` : répartition des vidéos par congrès.
- `data/transcripts/` : sous-titres automatiques, non versionnés.
- `scripts/build_index.py` : régénère les index et vérifie les liens.

## Web-app

https://mrthomaslef.github.io/archive-sims/ (PWA hors-ligne, référencée sur le Tapp Store)

Après modification des fiches :

```bash
python3 scripts/build_index.py && python3 scripts/build_web.py
```
