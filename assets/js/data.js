/* ==========================================================================
   CONTENU DU SITE
   --------------------------------------------------------------------------
   Tout le texte et tous les travaux sont ici : modifiez ce fichier pour
   personnaliser le portfolio sans toucher au HTML.

   Médias : chaque média accepte
     { type: "image", src: "assets/media/mon-image.jpg", alt: "..." }
     { type: "video", src: "assets/media/ma-video.mp4", poster: "..." }
   Sans `src`, un visuel de remplacement (dégradé) est affiché.
   ========================================================================== */

window.SITE = {
  name: "Votre Nom",
  firstName: "Votre",
  lastName: "Nom",
  role: "Creative Design Engineer",
  location: "Paris, FR",
  timezone: "Europe/Paris",
  availability: "Disponible pour freelance — Nov 2026",
  email: "hello@votrenom.com",
  intro:
    "Avec une attention portée au mouvement, à la performance et au détail, je donne vie à des produits numériques pour des marques ambitieuses partout dans le monde.",
  statement:
    "Je conçois et développe des expériences web où le design et le code ne font qu'un — des interfaces fluides, animées et pensées jusqu'au moindre pixel.",
  showreel: { type: "video", src: "", poster: "", label: "Showreel 2026" },
  socials: [
    { label: "Instagram", url: "https://instagram.com/" },
    { label: "X / Twitter", url: "https://x.com/" },
    { label: "LinkedIn", url: "https://linkedin.com/" },
    { label: "GitHub", url: "https://github.com/" },
  ],
  services: [
    {
      title: "Brand Design",
      text: "Identités visuelles, systèmes graphiques et direction artistique qui donnent une voix singulière à votre marque.",
      tags: ["Identité", "Direction artistique", "Guidelines"],
    },
    {
      title: "UX / UI Design",
      text: "Parcours utilisateurs, wireframes et interfaces pensés pour être clairs, accessibles et agréables à utiliser.",
      tags: ["Recherche", "Prototypage", "Design system"],
    },
    {
      title: "Web Development",
      text: "Sites et applications performants, construits avec des technologies modernes et une attention extrême au détail.",
      tags: ["Next.js", "WebGL", "CMS"],
    },
    {
      title: "Motion Design",
      text: "Animations, transitions et micro-interactions qui rendent chaque expérience vivante et mémorable.",
      tags: ["GSAP", "Vidéo", "Interactions"],
    },
  ],
  about: {
    bio: [
      "Je suis designer et développeur créatif basé à Paris. Depuis plusieurs années, j'accompagne des studios, des startups et des marques dans la création d'expériences numériques qui sortent du lot.",
      "Mon approche mêle direction artistique, motion et ingénierie front-end : je dessine les interfaces que je développe, ce qui me permet de préserver l'intention du design jusqu'à la mise en ligne.",
    ],
    experience: [
      { company: "Studio Exemple", role: "Design Engineer", period: "2024 — Présent" },
      { company: "Agence Exemple", role: "Creative Developer", period: "2022 — 2024" },
      { company: "Startup Exemple", role: "Front-end Developer", period: "2020 — 2022" },
      { company: "Freelance", role: "Designer & Développeur", period: "2018 — 2020" },
    ],
    recognitions: [
      { name: "Awwwards — Site of the Day", year: "2026" },
      { name: "CSS Design Awards — Website of the Day", year: "2025" },
      { name: "FWA — FWA of the Day", year: "2025" },
      { name: "Orpetron — Website of the Day", year: "2024" },
    ],
    clients: ["Client A", "Client B", "Client C", "Client D", "Client E", "Client F", "Client G", "Client H"],
  },
};

window.PROJECTS = [
  {
    slug: "projet-un",
    title: "Projet Un",
    category: "Product",
    year: "2026",
    client: "Client A",
    role: "Design & Développement",
    services: ["UX / UI", "Développement", "Motion"],
    url: "",
    colors: ["#ff5a1f", "#2b1a12"],
    summary: "Une plateforme produit repensée de A à Z, du système de design jusqu'aux animations de l'interface.",
    description: [
      "Remplacez ce texte par la description de votre projet : le contexte, le défi, la solution apportée et les résultats obtenus.",
      "Vous pouvez ajouter autant de paragraphes que nécessaire dans le tableau `description` du fichier assets/js/data.js.",
    ],
    cover: { type: "image", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }, { type: "video", src: "" }],
  },
  {
    slug: "projet-deux",
    title: "Projet Deux",
    category: "Website",
    year: "2026",
    client: "Client B",
    role: "Direction artistique & Développement",
    services: ["Direction artistique", "Développement", "WebGL"],
    url: "",
    colors: ["#5b6cff", "#0f1233"],
    summary: "Un site vitrine immersif mêlant 3D temps réel et transitions fluides.",
    description: [
      "Remplacez ce texte par la description de votre projet.",
    ],
    cover: { type: "image", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
  {
    slug: "projet-trois",
    title: "Projet Trois",
    category: "Brand",
    year: "2025",
    client: "Client C",
    role: "Identité visuelle",
    services: ["Branding", "Guidelines", "Motion"],
    url: "",
    colors: ["#d4ff3a", "#1c2208"],
    summary: "Une identité de marque complète, du logo au système d'animation.",
    description: ["Remplacez ce texte par la description de votre projet."],
    cover: { type: "image", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }, { type: "image", src: "" }],
  },
  {
    slug: "projet-quatre",
    title: "Projet Quatre",
    category: "Motion",
    year: "2025",
    client: "Client D",
    role: "Motion Design",
    services: ["Motion", "Vidéo", "Son"],
    url: "",
    colors: ["#ff3d7f", "#2a0b18"],
    summary: "Une campagne vidéo animée pour le lancement d'un nouveau produit.",
    description: ["Remplacez ce texte par la description de votre projet."],
    cover: { type: "video", src: "" },
    gallery: [{ type: "video", src: "" }, { type: "image", src: "" }],
  },
  {
    slug: "projet-cinq",
    title: "Projet Cinq",
    category: "E-commerce",
    year: "2024",
    client: "Client E",
    role: "Design & Développement",
    services: ["UX / UI", "Shopify", "Développement"],
    url: "",
    colors: ["#2fd5c4", "#08211f"],
    summary: "Une boutique en ligne rapide et élégante, pensée pour convertir.",
    description: ["Remplacez ce texte par la description de votre projet."],
    cover: { type: "image", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
  {
    slug: "projet-six",
    title: "Projet Six",
    category: "Website",
    year: "2024",
    client: "Client F",
    role: "Développement",
    services: ["Développement", "CMS", "Animations"],
    url: "",
    colors: ["#f2c14e", "#271d05"],
    summary: "Un site éditorial animé pour un studio d'architecture.",
    description: ["Remplacez ce texte par la description de votre projet."],
    cover: { type: "image", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
];
