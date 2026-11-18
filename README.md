<img src="assets/icon.svg" width="64" height="64" alt="">

# Archive sims

Created in [T3 Code](https://t3.codes).

## Contenu

- `fiches/` : fiches résumé des congrès SIMS, au format Obsidian et rangées par année. Le point d'entrée est `00 - Congrès SIMS - Accueil.md`.
  - 2017 Genou : 35 fiches
  - 2019 Hanche : 42 fiches
  - 2022 Main et poignet : 40 fiches
  - 2024 Pied et cheville : 40 fiches
- Chaque fiche : orateur lu sur les diapos, « L'essentiel » + « À retenir », images clés légendées avec lien vers l'instant de la vidéo.
- `img/<année>/` : images clés (diapos recadrées, contrôlées pour l'anonymisation).
- `data/` (non versionné) : liste des vidéos, transcriptions, diapos extraites (`frames/`) et sélections d'images (`selections/`).
- `scripts/build_index.py` : régénère les index et vérifie les liens.
- `scripts/apply_images.py` : recadre les images choisies dans `data/selections/` et les insère dans les fiches (nécessite Pillow).

## Web-app

https://mrthomaslef.github.io/archive-sims/ (PWA hors-ligne, référencée sur le Tapp Store)

Après modification des fiches :

```bash
python3 scripts/build_index.py && python3 scripts/build_web.py
```
