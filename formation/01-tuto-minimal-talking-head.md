# Leçon 01 — Monter une vidéo « talking head » virale en style minimal (avec Claude)

**Source :** « How to Edit VIRAL Talking Head Videos Using ONLY Claude! (New Minimal Style) », Joseph | Video Editing, 31/10/2026, 21 min
https://youtu.be/g9xoKm5DEeU

**Ce que j'ai étudié :** la transcription intégrale (sous-titres anglais) et les chapitres.
**Ce que je n'ai pas pu voir :** les images. YouTube bloque le téléchargement de la vidéo depuis mon environnement cloud. Je connais donc le style par sa description, pas encore à l'œil.

---

## 1. L'idée centrale

On fait monter par Claude un short « éducatif premium » : style minimal, luxueux, artistique, très produit, qui rend accro. C'est le style d'Arthur Brooks, facturé environ 100 $ le Reel par les monteurs.
Outils : un abonnement Claude et **Remotion** (vidéo en code React). Aucun plugin payant.

> **Règle n°1 :** si tu ne sais pas ce qui fait un bon montage, l'IA ne te fera que de mauvais montages.
> Il faut d'abord comprendre le style en monteur, ensuite seulement le confier à l'IA.

---

## 2. Les 10 principes du style minimal

| # | Principe | Recette |
|---|----------|---------|
| 1 | **Sous-titres « cinématiques »** | 2 polices : une sans-serif simple pour le texte courant (Inter) et une serif ou script pour l'accent (Playfair Italic). Lignes de 5 mots maximum. Les mots importants sont en gras, gros, au centre. Les autres mots, plus petits, vont dans les espaces au-dessus ou en dessous. Pas de gabarit fixe : une logique de placement. |
| 2 | **B-roll + texte** | Le script est découpé en petits segments, avec un B-roll littéral par segment (« se battre » → un homme qui se bat). Traitement : texture papier légère, bords assombris (vignette) et légèrement flous pour guider l'œil. Le texte cinématique (principe 1) est posé dessus et décrit la scène. |
| 3 | **Peintures animées** | Une peinture classique qui illustre le propos. Texture peinture + papier rugueux pour la rendre « réelle ». Texte cinématique autour du sujet principal. Révélation par un court glissement de caméra. |
| 4 | **Ligne + texte** | Fond noir ou blanc texturé papier. Une ligne fine **bleu accent** mène au texte, est interrompue par lui, puis repart vers un texte lié. La caméra suit la ligne, et donc le fil de la pensée. |
| 5 | **Ligne + illustrations** | Même fond, même ligne, mais elle mène à des illustrations. Variantes : ligne horizontale avec point blanc qui marque l'objet, texte et illustration dessous ; zigzag avec panoramique qui révèle des objets des deux côtés (pour une progression en phases) ; ligne qui monte droit vers le sujet. |
| 6 | **Scène centrée sur le texte** | Fond blanc ou bleu, texture papier très rugueuse. Deux guillemets autour du centre, la phrase en texte cinématique au milieu. Simple et direct. |
| 7 | **Illustration centrale** | Une illustration de l'idée principale (une personne, un cerveau vu de dessus, un motif circulaire en traits fins, un profil). Rendu peint, rugueux, bruité. Elle occupe la moitié basse et déborde vers le milieu, avec des bords abstraits qui se fondent dans la scène. Texte autour. Une texture tissu rugueuse fait ressortir les personnages du fond. |
| 8 | **Illustration latérale + texte** | Même univers, mais l'illustration est sur un côté et le texte sur l'autre (par exemple un demi-cercle texturé tissu à gauche, avec du texte qui tourne autour). Sert à montrer **deux éléments à la fois**. |
| 9 | **Objet + texte** (rare) | Un seul objet de l'histoire, fond papier, texte autour, révélation « rugueuse ». |
| 10 | **Graphiques / stats** (rare) | Fond sombre uni texturé. Grille de lignes blanches fines et lumineuses. Une **boule bleue** trace la courbe et la caméra la suit. |

**Cohérence globale :** mêmes textures (papier, peinture, tissu), mêmes bords abstraits, même palette (noir, blanc, bleu accent), même typographie. C'est ce qui fait le « look ».

---

## 3. Former Claude à un style (méthode réutilisable pour n'importe quel style)

1. **Collecter** environ 20 vidéos de référence parmi les plus soignées du style.
2. **Décortiquer en monteur** : pour chaque scène réussie, se demander pourquoi cette scène, ce design, ces couleurs, ces effets, cette animation.
3. **Planche d'inspiration** (Figma) : capturer chaque scène qui plaît, soit environ 130 visuels.
4. **Classer** les visuels dans les 10 principes, puis disséquer chaque catégorie : polices, couleurs, tailles, motifs.
5. **Donner à Claude** les 20 vidéos et la planche, avec ce prompt :
   - transcription mot à mot et analyse image par image de chaque vidéo ;
   - étudier 3 choses : **(a)** où tombent les animations par rapport au script, **(b)** de quoi se compose le design, **(c)** la logique d'animation (durées, ressenti) ;
   - utiliser la planche pour comprendre le design.
6. **Résultat** : un *skill* qui documente tailles, mise en page, textures, formes et couleurs, plus une **bibliothèque d'environ 225 animations** extraites (dossiers avec designs de référence et planches d'images clés).

> Les vidéos apprennent la **logique** (quand et pourquoi). La planche apprend le **design** (à quoi ça ressemble).

---

## 4. Monter un short : le pipeline

| Étape | Qui | Durée observée |
|-------|-----|----------------|
| 1. Rush brut → transcription mot à mot **à la milliseconde** et suppression des silences en gardant **30 ms de marge** | Claude | ~15 min (avec l'étape 2) |
| 2. **Document de planification** : script à droite, et à gauche, scène par scène, des designs recommandés tirés de la bibliothèque, avec un champ de notes | Claude | (inclus) |
| 3. **Plan de montage** : choisir le design de chaque scène | **Humain** (étape la plus importante) | ~15 min |
| 4. Liste d'assets et collecte : peintures (Wikipedia/Wikimedia), stock (Pexels), photos, polices Google Fonts | Claude | — |
| 5. Construction : sous-titres A-roll, puis chaque scène dans Remotion, puis rendu de la V1 | Claude | ~60 min |
| 6. **Révisions** : la V1 n'est qu'à 60-70 %. Retours précis et numérotés | Humain → Claude | ~10 min |
| 7. **Sound design** calé sur les références : musique cinématique, clics sur le texte, « surligneur » sur les graphiques, whooshs sur les transitions | Claude | ~15 min |
| 8. Rendu final | Claude | ~2 h au total |

> **Ne jamais laisser l'IA planifier seule** : elle n'est pas assez créative au premier jet. Une consigne paresseuse donne un résultat paresseux.

### Exemples de retours de révision (bon format)
1. Le design du texte de la scène 1 n'est pas bon, et le mot « psychology » doit apparaître dans la même scène.
2. Coupe brutale entre deux animations.
3. Texture peinture trop lourde, et elle ne suit pas l'animation.
4. Mauvaise coupe à la seconde 24.
5. La spirale doit rester plus longtemps à l'écran.
6. Il manque les guillemets sur la scène de texte finale.

---

## 5. La logique éditoriale (le vrai savoir-faire)

Tirée du plan de montage de l'exemple (« les 4 schémas de carrière ») :

- **Ouverture sur l'A-roll et les sous-titres** : le spectateur se connecte d'abord à la personne.
- **Premier visuel = accroche forte** (la courbe qui monte d'une marche à chaque « up »).
- **Quand il ANNONCE une nouvelle idée, on reste sur son visage. Quand il la DÉCRIT, on la MONTRE.**
- On peut **basculer en cours de phrase** : A-roll sur la première moitié, puis l'animation (une longue ligne plate pour « lent et régulier »).
- Visuel **adapté au type de propos** :
  - une personne évoquée → *character callout* ;
  - un concept abstrait (une spirale) → illustration centrale ;
  - une action ou une émotion (« tout reprendre de zéro ») → B-roll ;
  - une anecdote personnelle → *object callout* avec ses photos ;
  - plusieurs options ou un cycle → illustration avec un cercle qui fait défiler les choix ;
  - la grande thèse avec mots-clés (« calling, agility, courage ») → ligne + texte qui traverse les mots ;
  - la phrase de conclusion → scène texte avec guillemets.
- **Équilibre et rythme** : alterner les types de scènes pour que la vidéo reste fluide et agréable.

---

## 6. Ce que j'en retiens pour notre collaboration

- Mon rôle : exécuter le pipeline (transcription, coupes, plan proposé, assets, construction Remotion, révisions, sound design, rendu).
- Ton rôle : la direction artistique, c'est-à-dire valider ou corriger le plan scène par scène, puis faire des retours précis.
- Mon environnement le permet : Node 22 (Remotion), ffmpeg, 4 CPU / 15 Go de RAM. Pas de GPU : les rendus seront plus lents.
- Pour reproduire ce niveau, il me faudra **mes propres références** : les vidéos ou captures du style que tu vises, et idéalement ta planche d'inspiration. Ce sont elles qui me feront passer de « je connais la théorie » à « je sais le faire ».
