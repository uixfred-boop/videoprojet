---
name: montage-minimal-premium
description: Monter un short vertical (Reels/TikTok/Shorts 9:16) dans le style « minimal premium » appris sur les 5 vidéos de référence de l'utilisateur. Deux formats couverts, talking head avec sous-titres éditoriaux ou essai visuel en voix off. Palette bleu électrique, blanc et noir, sous-titres mot à mot avec mot clé géant, peintures, schémas au trait, B-roll ciné. À utiliser dès qu'il faut planifier, construire (Remotion), réviser ou critiquer un montage short pour l'utilisateur.
---

# Montage minimal premium (short 9:16)

Ce skill est la synthèse de l'analyse image par image et mot par mot de 5 vidéos de référence fournies par l'utilisateur.
Dossier source : https://drive.google.com/drive/folders/1_pcFU4IViEQySzPt2RGFNZIaUTGYweaF

- Le détail scène par scène est dans `references/analyse-scene-par-scene.md`.
- Les images clés sont dans `references/images/` ; la vue d'ensemble est `references/bibliotheque-visuelle.jpg`.
- Les planches image par image (une image toutes les 0,5 s) sont dans `references/planches/`.
- Les transcriptions horodatées au mot sont dans `references/transcripts/`.

| Réf | Durée | Format | Coupes franches | Plan moyen | Débit |
|-----|-------|--------|-----------------|------------|-------|
| REF01 | 47 s | Talking head créateur + motion design UI | 6 (le reste en transitions animées) | ~2,5 s (visuel) | 231 mots/min |
| REF02 | 110 s | Essai visuel voix off (sans visage) | 50 | 2,2 s | 179 mots/min |
| REF03 | 111 s | Essai visuel voix off (sans visage) | 63 | 1,7 s | 188 mots/min |
| REF04 | 54 s | Talking head interview (podcast) | 15 | 3,3 s | 214 mots/min |
| REF05 | 80 s | Talking head interview (face cam) | 34 | 2,3 s | 223 mots/min |

---

## 1. L'ADN du style en 10 règles

1. **Le texte est le design.** Pas de cadre, de bandeau ni d'ombre lourde : de la typo pure, bien composée.
2. **Un mot clé géant, des mots satellites minuscules.** Rapport de taille d'environ 4 pour 1. C'est la signature.
3. **Deux familles de caractères en tension** : une sans-serif neutre (Inter) et une serif éditoriale (droite condensée ou italique).
4. **Trois couleurs** : bleu électrique, blanc cassé et noir. Le rouge n'apparaît qu'en accent rare (douleur, danger).
5. **Une idée = un visuel**, avec changement de visuel à chaque proposition du script.
6. **Tout est synchronisé à l'attaque du mot**, à la milliseconde : les coupes comme les apparitions de texte.
7. **Calme et précis** : pas de rebond, de tremblement, de transitions gadget ni d'emoji. Les mouvements sont lents ; l'énergie vient du rythme des coupes et du texte.
8. **Image noble** : B-roll ciné étalonné (grain, tons chauds ou désaturés), peintures classiques, archives N&B, schémas au trait fin.
9. **Profondeur douce** : halos bleus flous, grain, coins arrondis, légère poussée de caméra sur les images fixes.
10. **Zéro temps mort** : premier mot à 0,00 s, aucun blanc de plus de 0,8 s, et une musique de fond continue.

---

## 2. Les deux formats

### Format A : talking head premium (REF01, REF04, REF05)
- L'A-roll occupe **50 à 65 %** du temps, avec les sous-titres éditoriaux (§4) en permanence.
- Les inserts durent **0,7 à 2,5 s** : peintures, B-roll ciné, extraits de films, plein écran typo bleu ou blanc.
- Un passage sur le visage dure **2 à 6 s**. Un punch-in (recadrage serré de 110 à 125 %) sert à appuyer une phrase forte.
- Variante créateur (REF01) : l'A-roll **se réduit en carte arrondie** flottante sur fond clair (#E8F2F7). Autour : motion design UI (barre de recherche, carrousel 3D, orbite de cartes, cartes produit avec halo).

### Format B : essai visuel en voix off (REF02, REF03)
- Aucun visage : chaque phrase porte son propre visuel.
- Un changement de visuel toutes les **1,7 à 2,2 s** en moyenne.
- Alternance permanente : fond bleu (typo), fond blanc (schéma ou typo), B-roll ciné, illustration, fond noir (carte vidéo ou objet lumineux).
- Le texte est souvent la seule chose à l'écran : le sous-titre devient le visuel.

---

## 3. La charte (tokens de design)

**Sortie** : 1080×1920, 30 fps. Les références sont en 720×1280, donc toutes les mesures ci-dessous sont ramenées à 1080 de large.

### Couleurs (mesurées dans les vidéos)
| Token | Hex | Usage |
|-------|-----|-------|
| `blue` | **#0047FF** (plage #0036EC à #0053FD) | Fonds pleins, boîte de surlignage, mots accent sur blanc, lignes épaisses |
| `blue-sky` | #0A83EF / #1782FD | Variante plus claire (REF02) : fond « respiration », ligne épaisse |
| `blue-night` | #064B90 | Fond uni sombre (REF01) |
| `halo` | #7698F4, en dégradé radial vers transparent | Halos flous derrière les objets et silhouettes |
| `paper` | **#FBF8FC** (variante #F7F8F7) | Fond blanc cassé, jamais un blanc pur |
| `ice` | #E8F2F7 | Fond clair bleuté du format créateur (REF01) |
| `ink` | **#141115** (ou noir pur #010000) | Fonds noirs, texte sur blanc |
| `red` | ~#C8102E | Accent très rare (douleur, danger, émotion négative) |

### Typographies (équivalents gratuits sur Google Fonts)
| Rôle | Police | Usage observé |
|------|--------|---------------|
| **Sans** | **Inter** (SemiBold à Black), interlettrage -2 à -4 % | Mots satellites, sous-titres de base, mots clés « choc » en Black |
| **Serif droite condensée** | **Instrument Serif**, ou Newsreader Display SemiBold resserré | Mots clés des essais visuels (« basically », « wrong », « PANAS », « mistake ») |
| **Serif italique** | **Playfair Display SemiBold Italic**, ou Instrument Serif Italic | Mots émotionnels ou abstraits en A-roll (« eliminate », « depression », « purpose ») |
| **Script** (REF01 uniquement) | **Great Vibes** ou Pinyon Script | Mots d'élégance ou connecteurs (« The », « Thing », « Professional ») |

### Tailles, pour une largeur de 1080
- Mot clé : **110 à 190 px**. Mot clé A-roll : 90 à 130 px. Mot géant « choc » : jusqu'à 220 px.
- Satellites : **28 à 40 px**. Bloc A-roll sans mot clé : 46 à 56 px en SemiBold ou Bold.
- Interlignage du lockup très serré (0,85 à 0,95). Les satellites touchent presque le mot clé.

### Matières et effets
- **Grain** léger sur tout (bruit animé, 3 à 6 % d'opacité). Le fond bleu de REF03 a une texture papier ou aquarelle.
- **Halo** : dégradé radial `halo` → transparent, flou de 60 à 120 px, derrière silhouettes, cercles et méditant.
- **Cartes vidéo** : coins arrondis à environ 3 % de la largeur (~32 px), ombre ou halo bleu doux, posées sur noir ou sur `ice`.
- **Illustrations** : silhouettes noires « rugueuses » (bord poudreux, aérographe), personnages plats anguleux, têtes texturées (peinture granuleuse beige et cerveau bleu), corps 3D lumineux bleu et cyan.
- **Traits fins** de 1 à 2 px (blanc sur bleu, gris ou noir sur blanc) : cercles, arcs, grilles d'architecte, lignes de cote, constellations de points reliés.

---

## 4. Le moteur de sous-titres (la signature n°1)

1. **Mot à mot** : chaque mot apparaît **au début exact de sa prononciation**, pas avant.
2. **Blocs de 1 à 6 mots** formant une unité de sens. Le bloc reste affiché, chaque nouveau mot s'y ajoute, puis le bloc est **remplacé net** (coupe) par le suivant.
3. **Lockup** : par bloc, **un mot clé (deux au maximum)** en grand. Les satellites s'y accrochent : ce qui précède en petit au-dessus ou à gauche, ce qui suit en petit en dessous ou à droite.
   Exemple : `Explosion of` / **depression** / `and anxiety`.
4. **Choix du mot clé** : le mot qui porte le sens ou l'émotion (nom fort, adjectif, verbe d'action, chiffre). Jamais un mot outil.
5. **Style du mot clé selon le registre** :
   - émotion, abstraction, spiritualité → **serif italique** (« happiness », « teacher », « meaning ») ;
   - choc, fait, impératif → **Inter Black** (« possible », « bored », « ways », « through ») ;
   - concept titre en essai visuel → **serif droite condensée** (« opposites. », « survival. ») ;
   - citation → serif géante entre **guillemets typographiques** « “ ” ».
6. **Blocs sans mot clé** (« and that's », « for some people ») : petite taille uniforme, centrés, un à trois mots.
7. **Couleur** :
   - blanc sur image ou sur bleu ; noir (ou bleu) sur `paper` ;
   - **un seul mot accent bleu par écran au maximum** ;
   - sur A-roll, le mot arrive en gris (~50 %) puis passe au blanc.
8. **Boîte de surlignage bleue** (signature de REF05) : un rectangle `blue` derrière la phrase clé, texte blanc (souvent serif italique). À utiliser sur environ 1 bloc sur 6 ou 8, pour les phrases à retenir.
9. **Surligneur** (REF04) : une barre `blue` qui balaie derrière un seul mot, sur fond blanc.
10. **Position** :
    - A-roll : centré à **50-62 % de la hauteur** (poitrine), jamais sur le visage ;
    - plein écran : centré, ou dans le tiers haut quand un objet occupe le centre ;
    - sur B-roll : dans la zone la plus calme de l'image.
11. **Interdits** : contour, fond noir semi-transparent, emoji, plus de deux couleurs de texte, MAJUSCULES partout (sauf citation en petites capitales, ou texte géant défilant).

---

## 5. Catalogue de scènes

Chaque scène a un identifiant à réutiliser dans le plan de montage. Les images sont dans `references/images/`.

### A. A-roll (format A)
| ID | Scène | Quand | Recette | Image |
|----|-------|-------|---------|-------|
| A1 | Sous-titres lockup | Par défaut sur le visage | §4 | 01, 03 |
| A2 | Boîte de surlignage | Phrase à retenir, problème, chiffre | Wipe bleu gauche→droite et texte blanc | 02, 61 |
| A3 | Mot géant remplissage | Adjectif ou superlatif choc | Inter Black géant, gris→blanc de gauche à droite | 05 |
| A4 | Texte géant défilant | Impératif (« Be bored more ») | Capitales blanches énormes qui traversent le bas du cadre en ~1 s | 04 |
| A5 | Icônes 3D en verre | Énumération de 2 ou 3 notions | Losanges en verre avec icône et label, près des mains | 06 |
| A6 | A-roll → carte flottante | Bascule vers une démonstration | Réduction en carte arrondie avec halo, cartes satellites qui dérivent | 07 |
| A7 | Punch-in | Phrase forte, chute | Recadrage serré de 110 à 125 %, coupe sèche | — |

### B. Typo plein écran
| ID | Scène | Quand | Image |
|----|-------|-------|-------|
| B1 | Fond bleu + lockup blanc | Contradiction, conclusion, transition logique | 17 |
| B2 | Fond blanc + lockup noir ou bleu | Contre-pied court (« But that's wrong. ») | 18, 45, 60 |
| B3 | Citation géante avec guillemets | Question ou citation clé | 53 |
| B4 | Surligneur derrière un mot | Problème principal | 59 |
| B5 | Chiffre géant en dégradé (« 01 », « 1 ») | Liste numérotée, « une seule chose » | 62, 08 |
| B6 | Phrase qui défile horizontalement | Phrase relance | 13 |
| B7 | CTA final (« Comment "X" below… ») | Dernière scène | 38 |

### C. Images
| ID | Scène | Quand | Recette | Image |
|----|-------|-------|---------|-------|
| C1 | B-roll ciné + lockup | Émotion, vécu, action | Étalonnage chaud ou désaturé, grain, lockup blanc | 16, 57 |
| C2 | Vidéo en carte arrondie sur noir | Souvenir, passé, « la plupart des gens » | Carte à 85 % de la largeur, vintage | 23 |
| C3 | Extrait de film ou célébrité | Personnage, réaction, référence pop | Plein cadre, lockup | — |
| C4 | Archive N&B | Science, histoire, chercheurs | Plein cadre ou carte sur noir | — |
| C5 | Peinture classique + mot | Spiritualité, morale, sagesse | Plein cadre, push-in lent, mot serif italique ou boîte bleue | 63, 64 |
| C6 | Peinture révélée par papier déchiré | Basculement de sens | Version duotone bleu nuit, trou déchiré qui révèle la couleur | 56 |
| C7 | Rafale de peintures | Énumération (« purpose, meaning, coherence… ») | Une peinture par mot, 0,7 à 1 s chacune, boîte bleue | 64 |
| C8 | Citation en petites capitales sur B-roll | Texte ancien, verset | Petites capitales sans, mots clés en gras | 30 |

### D. Illustrations
| ID | Scène | Quand | Image |
|----|-------|-------|-------|
| D1 | Silhouettes rugueuses sur bleu texturé | Ouverture, condition humaine | 39 |
| D2 | Profil de tête texturé + cerveau bleu | Psychologie, pensée | 15 |
| D3 | Personnage plat anguleux (tête qui s'ouvre) | Hook, croyance commune | 14 |
| D4 | Silhouette bleue devant une lune blanche (sur noir) | Personne qui traverse quelque chose | 44 |
| D5 | Corps 3D lumineux avec éclat cyan | Douleur, choc émotionnel | 51 |
| D6 | Tête IRM bleue sur noir | Cerveau, intériorité | 36 |
| D7 | Photo N&B détourée sur blanc + texte bleu | Expérience vécue | 40 |
| D8 | Méditant + anneaux + halo | Calme, réglage intérieur | 32 |
| D9 | Personnage rugueux qui monte du bas + halo | « Je » qui se raconte | 42 |

### E. Schémas (fonds blanc, bleu ou noir, traits fins)
| ID | Scène | Pour exprimer | Image |
|----|-------|---------------|-------|
| E1 | **Ligne bleue épaisse qui serpente**, caméra qui suit | Parcours, poussée, enchaînement d'étapes | 27, 28, 43 |
| E2 | Ligne noire fine courbe + mot italique bleu | Croyance personnelle, nuance | 58 |
| E3 | Cercle fin qui se trace + 3 points ou labels | Liste de 3 bénéfices | 50, 37 |
| E4 | Cadran (bouton bleu + halo, mot fantôme derrière) | Concept unique (« dial ») | 24 |
| E5 | Quadrants ou grille 2×2 | Deux variables indépendantes | 22 |
| E6 | Camembert dans un anneau | Phases ou parts d'un tout | 48 |
| E7 | Venn à 3 cercles, intersection bleue | Trois piliers qui convergent | 55 |
| E8 | Spirale qui rétrécit en point | Rumination, question qui tourne | 52 |
| E9 | Labels en orbite autour d'une tête | Injonctions, pensées | 41 |
| E10 | Plan d'architecte (cadre fin, cotes, split) | Démonstration « scientifique » | 19 |
| E11 | Constellation de points reliés + objet 3D | Système, réseau | 31 |
| E12 | Frise fine + photos | Date, histoire, chercheurs | 20 |
| E13 | Grille et grands arcs + élément rouge | Biologie, danger | 46 |
| E14 | Orbe lumineux sur noir + cercle | Sentiment, état | 35 |

### F. Objets et preuves
| ID | Scène | Pour | Image |
|----|-------|------|-------|
| F1 | Document scientifique sur bleu + zoom dedans | Étude, preuve | 21 |
| F2 | Photos de l'orateur qui s'empilent sur bleu | Autorité, « je » | 33 |
| F3 | Capture de page web (offre) | Produit, abonnement | 54 |
| F4 | Collage de gravures ou papier vintage | Antiquité, textes sacrés | 25, 29 |
| F5 | Cerveau 3D chrome + collage IRM | Neurosciences | 49 |

### G. UI créateur (REF01)
| ID | Scène | Image |
|----|-------|-------|
| G1 | Barre de recherche sombre avec halo cyan, texte tapé | 09 |
| G2 | Carrousel 3D incurvé de cartes vidéo | 10 |
| G3 | Orbite de cartes autour d'un avatar rond + gros nombre fantôme | 11 |
| G4 | Cartes produit empilées avec halos colorés | 12 |
| G5 | Carte profil qui pivote en 3D et se pose | — |

---

## 6. Logique de placement : quel visuel sur quel bout de script

**Règle mère : couper sur l'attaque du mot qui ouvre une nouvelle proposition** (après une virgule ou un point), jamais au milieu d'un groupe de sens.

| Ce que dit le script | Visuel |
|----------------------|--------|
| Accroche, croyance commune (« Most people assume… », « The biggest mistake… ») | Illustration forte (D1, D3) ou A-roll + mot clé dès 0,3 s |
| Contre-pied (« But that's wrong. », « but it isn't. ») | **Typo plein écran courte** (B1 ou B2, 0,8 à 1,5 s), avec inversion du fond |
| Étude, chiffre, date, chercheurs | Archive (C4), document (F1), frise (E12), schéma (E5, E10) |
| Concept abstrait (systèmes, cadran, réseau) | Schéma minimal au trait (E3 à E11) |
| Émotion, souffrance, intime | B-roll ciné en gros plan (larmes, yeux, silhouettes), C1 ou C2 |
| Sagesse ancienne, religion, philosophie | Peinture (C5, C6), fresque, gravure (F4) |
| Énumération | Rafale, un visuel par item (C7), ou cercle avec points (E3), ou icônes (A5) |
| Il parle de lui (« I spent years… », « My negative dial… ») | Photos de lui (F2), personnage qui monte (D9) ou A-roll |
| Question rhétorique | Typo plein écran ou spirale (E8) ; « How? » en géant sur une image |
| Citation | Guillemets géants (B3) ou petites capitales sur B-roll (C8) |
| Impératif, conseil | A-roll punch-in, mot géant (A3) ou texte défilant (A4) |
| Référence générationnelle ou pop | Extrait de film connu (C3) |
| Offre, CTA | Capture produit (F3), puis écran final CTA (B7) |

**Rythme**
- Format B : un changement de visuel toutes les 1,7 à 2,2 s.
- Format A : une alternance visage/insert toutes les 2 à 3,5 s.
- **Jamais plus d'environ 6 s sans changement de plan.** Le texte change à chaque mot, l'œil a donc toujours du nouveau.

**Retour au visage (format A)**
On revient sur l'orateur pour les liaisons logiques (« So you need to… »), les « je », les conclusions et les mots d'humeur. On le quitte quand il **décrit** ou **cite** quelque chose.

**Alternance des fonds**
- Ne pas enchaîner deux scènes indépendantes sur le même fond.
- Cycle typique : image → bleu → blanc → image → noir…
- Exception : **une même scène qui évolue** sur plusieurs phrases. La ligne bleue continue, le cercle se déplace et le texte se réorganise.

**Fil visuel**
Un motif peut revenir pour faire rimer deux idées. Dans REF02, la ligne bleue de 40 s revient à 89 s sur « eliminate your happiness ».

**Ouverture et fin**
- Pas d'intro ni de logo.
- Fin : dernière phrase en typo pleine sur bleu, puis CTA (B7) ou fondu au noir en 0,5 à 1 s.

---

## 7. Logique d'animation (mesurée à 30 fps)

| Élément | Durée | Courbe / ressenti |
|---------|-------|-------------------|
| Mot qui apparaît, A-roll | **4 à 6 images (0,13-0,2 s)**, de gris ~50 % à blanc | ease-out doux, sans scale ni rebond |
| Mot qui apparaît, plein écran (format B) | **instantané (0-1 image)** à l'attaque du mot. Le lockup **se réorganise d'un coup** à l'arrivée du mot clé | sec, typographique |
| Changement de bloc de texte | coupe sèche | — |
| Boîte de surlignage bleue | balayage gauche→droite en **5-6 images (~0,2 s)** | ease-out (`cubic-bezier(.2,.8,.2,1)`) |
| Coupe de plan | ~95 % de coupes franches **sur l'attaque d'un mot** | — |
| Fondu | rare : fin vers noir 0,5-1 s, ou bleu → bleu clair en respiration | linéaire |
| Push-in sur image fixe (peinture, photo, illustration) | **+6 à 8 % d'échelle par seconde**, en continu pendant le plan | linéaire ou très léger ease |
| A-roll → carte flottante | **12-14 images (~0,45 s)**, puis dérive lente continue | ease-in-out, cartes satellites qui entrent par les bords en ~10 images |
| Ligne bleue épaisse | **10-12 images par arc**. La caméra suit la pointe ; le texte apparaît quand la ligne l'atteint | ease-in-out, fluide |
| Cercle fin qui se trace | 0,5 à 0,8 s ; les points ou labels arrivent un par un, chacun sur son mot | ease-out |
| Halo | croissance ou pulsation douce de 0,5 à 1 s | sinus |
| Photos qui s'empilent | une par mot, apparition ≤ 3 images (scale 95 → 100 %), rotation ±2-4° | sec |
| Texte géant défilant | traverse le cadre en ~1 s | linéaire |
| Rafale de peintures | 0,7 à 1 s par image, coupe sur chaque mot | sec |
| Texte tapé (barre de recherche) | ~1 caractère toutes les 1-2 images | linéaire |

**Ressenti global** : éditorial, posé, précis. Sont exclus :
- les secousses de caméra et le flou de mouvement exagéré ;
- les animations élastiques ou à rebond ;
- les rotations 3D gratuites (autorisées seulement pour l'UI de REF01) ;
- les glitchs, sauf une transition « data » rare et justifiée.

---

## 8. Son

- **Musique de fond continue**, ambient ou cinématique (piano, cordes, nappes). Il n'y a jamais de silence total.
- Mixage : la voix tourne autour de -15 à -19 dB (médiane) ; la musique est **8 à 11 dB plus bas** dans les respirations.
- **Bruitages discrets** : moins de 5 % des coupes portent un transitoire marqué. À utiliser :
  - souffles doux (whoosh léger) sur les grosses transitions (A-roll → carte, entrée d'un schéma) ;
  - micro-clics très bas sur l'UI et sur l'apparition de points ou d'icônes ;
  - léger crescendo vers le CTA.
  Pas de « boom » ni de bruitage cartoon.
- **Voix nette et serrée** : silences coupés (aucun blanc de plus de 0,3 à 0,8 s), garder environ **30 ms** de marge aux coupes. Débit visé : 180 à 230 mots/min.

*(Mesures audio automatiques, heuristiques : à confirmer à l'oreille sur un projet réel.)*

---

## 9. Pipeline de production

1. **Rush** : copie dans `projets/<nom>/rush/`.
2. **Transcription mot à mot** : faster-whisper avec `word_timestamps=True`. Décoder l'audio avec ffmpeg en 16 kHz mono float32 ; le loader PyAV de faster-whisper est incompatible ici.
3. **Coupe des silences** : garder 30 ms de marge et refaire les horodatages.
4. **Plan de montage** : un tableau à valider **par l'utilisateur** avant toute construction.

   | # | t début–fin | Texte du bloc | Mot(s) clé(s) | Style mot clé | Scène (ID §5) | Assets nécessaires | Note |
   |---|-------------|---------------|---------------|---------------|---------------|--------------------|------|

   Proposer 1 ou 2 options de scène par bloc, en respectant §6.
5. **Assets** : peintures du domaine public (Wikimedia Commons), B-roll libre (Pexels), polices Google Fonts. Lister ce qui manque et le demander à l'utilisateur.
6. **Construction Remotion** (1080×1920, 30 fps) :
   - sous-titres générés depuis le JSON des mots ;
   - une composition par type de scène, paramétrée ;
   - grain en overlay (SVG `feTurbulence` ou vidéo de grain) ;
   - lignes en SVG avec `strokeDashoffset` ;
   - halos en `radial-gradient` + `blur` ;
   - polices via `@remotion/google-fonts` (Inter, Instrument Serif, Playfair Display, Great Vibes).
7. **V1** : rendu et envoi. Elle sera à 60-70 % : demander des retours **numérotés**.
8. **Révisions**.
9. **Sound design** : musique et bruitages selon §8.
10. **Rendu final** : H.264, CRF 16-18, AAC 320 kbit/s.

---

## 10. Checklist qualité avant livraison

- [ ] Premier mot à 0,00 s, aucun blanc de plus de 0,8 s.
- [ ] Chaque coupe et chaque mot tombe sur l'attaque du mot (tolérance de 1 image).
- [ ] Chaque bloc de texte a au plus un ou deux mots clés, et le rapport de taille est d'environ 4 pour 1.
- [ ] Un seul mot accent bleu par écran au maximum.
- [ ] Aucun sous-titre sur un visage, ni dans les 15 % du bas (zone d'interface des plateformes).
- [ ] Pas plus d'environ 6 s sans changement de plan.
- [ ] Pas deux scènes indépendantes de suite sur le même fond.
- [ ] Palette respectée (bleu, blanc cassé, noir, rouge rare).
- [ ] Push-in lent sur toutes les images fixes.
- [ ] Musique continue, voix devant, bruitages discrets.
- [ ] Fin propre : CTA ou fondu au noir.

## 11. À ne jamais faire

- Sous-titres « karaoké » colorés, contours, ombres portées épaisses ou emoji.
- Plus de trois familles de caractères dans une vidéo.
- Transitions de banque d'effets (zoom-blur, glitch RGB, flash blanc, spin).
- B-roll stock « corporate » non étalonné : tout doit avoir un grain et une couleur cinéma.
- Laisser l'IA (moi) décider seule du plan : le plan se valide toujours avec l'utilisateur.
