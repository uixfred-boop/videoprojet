# Portfolio

Site portfolio statique (HTML / CSS / JS) inspiré de [itsjay.us](https://www.itsjay.us/), sans la page « Lab ».
Animations : GSAP + ScrollTrigger, smooth scroll : Lenis (fichiers inclus dans `assets/vendor`, aucune installation requise).

## Pages

| Fichier | Contenu |
| --- | --- |
| `index.html` | Preloader, hero (nom géant), showreel, Selected Work (aperçu au survol), à propos, services, clients, footer contact |
| `work.html` | Tous les projets, filtres par catégorie, vue liste / grille |
| `about.html` | Bio, portrait, services, expérience, récompenses, clients |
| `project.html?p=<slug>` | Étude de cas : méta, cover, description, galerie, projet suivant |

Le header (nom, disponibilité, heure locale, navigation) et le footer sont générés automatiquement sur chaque page.

## Modifier le contenu

Tout se trouve dans **`assets/js/data.js`** :

- `SITE` : nom, rôle, ville, fuseau horaire, email, réseaux, textes, services, bio, expérience, récompenses, clients, showreel.
- `PROJECTS` : la liste des travaux. Chaque projet a un `slug` (utilisé dans l'URL), un titre, une catégorie, une année, une description, une `cover` et une `gallery`.

Médias (images ou vidéos) à placer par exemple dans `assets/media/` :

```js
cover: { type: "image", src: "assets/media/projet-un/cover.jpg" },
gallery: [
  { type: "video", src: "assets/media/projet-un/demo.mp4", poster: "assets/media/projet-un/poster.jpg" },
  { type: "image", src: "assets/media/projet-un/01.jpg", alt: "Écran d'accueil" },
],
```

Tant qu'un média n'a pas de `src`, un dégradé aux couleurs du projet (`colors`) s'affiche à la place.

## Lancer en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```
