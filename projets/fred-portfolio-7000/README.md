# Projet : Fred, le portfolio à 7 000 $

- Source : https://drive.google.com/file/d/1s6D3pUyTjJg2vSj9AW04ISj2yNFMDDVA (16:9, 4 min 58, déjà montée, sous-titres incrustés en bas).
- Le rush n'est pas versionné : il pèse 189 Mo.
- Plan interactif à valider : https://claude.ai/artifact/EH4bsLsQU5zSvFCfD1pMmf

## Fichiers
- `transcript/script_propre.txt` : le texte exact, reconstruit par OCR des sous-titres incrustés et vérifié à l'image.
- `transcript/mots_alignes.json` : ce texte calé au mot sur la voix (faster-whisper large-v3 ; 75 % des mots ancrés, le reste interpolé).
- `transcript/phrases_horodatees.txt` : vue par phrase.
- `plan/plan.json` : les 6 shorts proposés, leurs segments et les options de scène (identifiants du skill montage-minimal-premium).

## Contraintes du rush
- Visage en très gros plan, centré vers x≈940 (il bouge parfois à gauche, vers 52-58 s).
- Sous-titres d'origine incrustés vers y≈930-1060 : à recadrer hors champ.
- Le visage n'est disponible qu'environ 49 % du temps ; le reste est du motion design (38 %) ou des captures d'écran du site (13 %).
- Silence ou musique seule entre 158,7 s et 176,2 s.
