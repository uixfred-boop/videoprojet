# Portfolio

Site portfolio statique (HTML / CSS / JS) qui reproduit la structure et les animations de [itsjay.us](https://www.itsjay.us/), **sans la page « Lab »**.
Animations : GSAP + ScrollTrigger, smooth scroll : Lenis (fichiers inclus dans `assets/vendor`, aucune installation requise).

## Pages

| Fichier | Contenu |
| --- | --- |
| `index.html` | Loader 0→100, hero « Design Engineer », showreel qui grandit au scroll (et suit la souris), « Moi », 2 projets mis en avant, services, « Modern Tech Stack » + logos, footer en tuiles |
| `work.html` | « Selected Work » : tous les projets en cartes |
| `project.html?p=<slug>` | Étude de cas : titre, année, services, résumé, galerie d'images / vidéos |

Sur toutes les pages : en-tête d'infos + bouton « Me contacter », barre de navigation flottante en bas (menu Home / Work), footer.

## Modifier le contenu

Tout se trouve dans **`assets/js/data.js`** :

- `SITE` : nom, domaine, email, infos de l'en-tête, rôles qui défilent, textes du hero, showreel, « Moi », services, outils, réseaux.
- `PROJECTS` : la liste des travaux (les deux premiers sont affichés sur l'accueil).

Chaque projet : `slug` (URL), `title`, `category`, `year`, `colors` (dégradé de remplacement), `tags` (texte défilant sur la carte), `services`, `summary`, `cover` (image de la carte), `preview` (vidéo au survol de la carte) et `gallery`.

Médias (images ou vidéos) à placer par exemple dans `assets/media/` :

```js
cover: { type: "image", src: "assets/media/projet-un/cover.jpg" },
preview: { type: "video", src: "assets/media/projet-un/preview.mp4" },
gallery: [
  { type: "video", src: "assets/media/projet-un/film.mp4", poster: "assets/media/projet-un/poster.jpg" }, // pleine largeur
  [ { type: "image", src: "assets/media/projet-un/01.jpg" }, { type: "image", src: "assets/media/projet-un/02.jpg" } ], // deux colonnes
],
```

Tant qu'un média n'a pas de `src`, un dégradé aux couleurs du projet s'affiche à la place.

Logos des outils : fichiers SVG de `assets/icons/` (issus de [simple-icons](https://simpleicons.org), licence CC0). Des logos vidéo sont déjà inclus (Premiere Pro, After Effects, DaVinci Resolve, Blender, Cinema 4D, Photoshop, Illustrator) : il suffit de mettre leur nom dans `SITE.stack`.

Polices : Inter Tight et Doto (Google Fonts), en remplacement des polices commerciales du site d'origine.

## Lancer en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```
