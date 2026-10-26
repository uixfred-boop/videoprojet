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
  domain: "votrenom.com",
  email: "hello@votrenom.com",

  // Les trois colonnes d'informations en haut de page
  header: [
    { label: "Basé en France", value: "Travaille partout" },
    { label: "Actuellement chez", value: "Studio", url: "https://example.com" },
    { label: "Disponibilité freelance", value: "Novembre 2026" },
  ],

  // Texte qui défile sous le nom dans la barre de navigation du bas
  roles: ["Creative Design Engineer", "Awwwards Stalker", "Product Builder", "Next.js Enthusiast"],
  // Vignette de la barre du bas (emoji, ou une image : { type: "image", src: "..." })
  avatar: "🤙🏼",

  hero: {
    top: ["Un", "Vraiment", "Bon"],
    title: ["Design", "Engineer"],
    scrollLeft: "Scrollez pour",
    scrollRight: "du bon contenu",
  },

  // Vidéo qui grandit au scroll sous le hero
  showreel: { type: "video", src: "", poster: "", label: "Showreel" },

  about: {
    label: "Moi",
    text: "Passionné par la rencontre du design et du code, je crée des expériences fluides et interactives qui ont du sens. Avec une attention portée au mouvement, à la performance et au détail, j'aide des marques ambitieuses du monde entier à donner vie à leurs produits numériques.",
    media: { type: "video", src: "", label: "Portrait" },
  },

  work: { title: "Work", year: "'26", seeAll: "Voir tout" },

  services: {
    label: "Services",
    intro: "En évolution à chaque brief et pensé pour l'impact, mon processus couvre le design, le développement et la stratégie de marque — pour aligner la vision et l'exécution et apporter clarté et caractère à chaque projet.",
    items: [
      {
        title: "Stratégie de marque",
        text: "Aider les marques à révéler leur raison d'être et leur singularité — et le plan pour la transmettre et gagner la fidélité de leurs clients.",
        tags: ["Recherche & Insights", "Stratégie de marque", "Étude concurrentielle", "Ton & Voix", "Naming & Copywriting", "Ateliers"],
        media: { type: "image", src: "", colors: ["#ff7a3d", "#2a0e04"] },
      },
      {
        title: "Design digital",
        text: "Concevoir des expériences numériques engageantes qui allient stratégie de marque, créativité et UX pour offrir des produits utiles et simples à utiliser.",
        tags: ["Identité visuelle", "Wireframing", "UI", "UX", "Web Design", "Product Design"],
        media: { type: "image", src: "", colors: ["#3fb6c9", "#0b2227"] },
      },
      {
        title: "Développement",
        text: "Construire des produits numériques qui réunissent design, technologie et stratégie pour des expériences utilisateur sans accroc.",
        tags: ["Front-end", "SEO", "Motion", "Animation", "WebGL", "CMS", "Bases de données"],
        media: { type: "image", src: "", colors: ["#9a9a9a", "#141414"] },
      },
    ],
  },

  // Logos : fichiers SVG dans assets/icons (source : simple-icons, licence CC0)
  stack: {
    title: ["Modern", "Tech Stack"],
    label: "Mes outils",
    top: [
      { name: "React", icon: "react", url: "https://react.dev" },
      { name: "Next.js", icon: "nextdotjs", url: "https://nextjs.org" },
      { name: "TypeScript", icon: "typescript", url: "https://www.typescriptlang.org" },
    ],
    bottom: [
      { name: "GSAP", icon: "greensock", url: "https://gsap.com" },
      { name: "Motion", icon: "framer", url: "https://motion.dev" },
      { name: "Tailwind CSS", icon: "tailwindcss", url: "https://tailwindcss.com" },
      { name: "Contentful", icon: "contentful", url: "https://www.contentful.com" },
      { name: "Supabase", icon: "supabase", url: "https://supabase.com" },
      { name: "Vercel", icon: "vercel", url: "https://vercel.com" },
      { name: "Figma", icon: "figma", url: "https://www.figma.com" },
    ],
  },

  // Tuiles du pied de page (la page « Work » et « Contact » sont ajoutées automatiquement)
  socials: [
    { label: "GitHub", url: "https://github.com/" },
    { label: "Instagram", url: "https://instagram.com/" },
    { label: "LinkedIn", url: "https://linkedin.com/" },
  ],

  workPage: { years: "[2022-2026]", title: "Selected Work" },
};

/* --------------------------------------------------------------------------
   PROJETS
   - Les deux premiers apparaissent sur la page d'accueil.
   - `tags` : texte qui défile sur la carte.
   - `preview` : vidéo affichée au survol de la carte.
   - `gallery` : un média = pleine largeur, un tableau de deux médias = deux colonnes.
   -------------------------------------------------------------------------- */
window.PROJECTS = [
  {
    slug: "projet-un",
    title: "Projet Un",
    category: "Portfolio",
    year: "2026",
    colors: ["#f2a3c4", "#2b1520"],
    icon: null,
    tags: ["Direction artistique", "Ton & Voix", "UI", "UX", "Next.js", "Tailwind CSS", "GSAP", "Motion", "Lenis", "Vercel"],
    services: ["Direction artistique", "Ton & Voix", "UI", "UX", "Développement"],
    summary: "Remplacez ce texte par le résumé de votre projet : le client, le contexte, l'objectif et votre rôle.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [
      { type: "image", src: "" },
      { type: "video", src: "" },
      [{ type: "image", src: "" }, { type: "image", src: "" }],
      { type: "image", src: "" },
    ],
  },
  {
    slug: "projet-deux",
    title: "Projet Deux",
    category: "Product",
    year: "2026",
    colors: ["#f5d90a", "#2a2500"],
    icon: null,
    tags: ["Direction artistique", "Naming & Copywriting", "Brand Design", "Stratégie", "UX", "UI", "Web Design", "Product Design"],
    services: ["Direction artistique", "Naming", "Brand Design", "Stratégie", "UX", "UI", "Web Design"],
    summary: "Remplacez ce texte par le résumé de votre projet : le client, le contexte, l'objectif et votre rôle.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [
      { type: "image", src: "" },
      { type: "image", src: "" },
      [{ type: "image", src: "" }, { type: "image", src: "" }],
      { type: "video", src: "" },
    ],
  },
  {
    slug: "projet-trois",
    title: "Projet Trois",
    category: "Services",
    year: "2025",
    colors: ["#e8442c", "#250805"],
    icon: null,
    tags: ["Web Design", "Next.js", "Tailwind CSS", "GSAP", "Motion", "Lenis", "Contentful", "Vercel", "Shopify API"],
    services: ["Web Design", "Développement", "Motion"],
    summary: "Remplacez ce texte par le résumé de votre projet.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, [{ type: "image", src: "" }, { type: "image", src: "" }]],
  },
  {
    slug: "projet-quatre",
    title: "Projet Quatre",
    category: "Product",
    year: "2025",
    colors: ["#2fb5a5", "#04201d"],
    icon: null,
    tags: ["Étude concurrentielle", "Ton & Voix", "Ateliers", "Stratégie", "UX", "UI", "Web Design", "Responsive"],
    services: ["Stratégie", "UX", "UI", "Web Design"],
    summary: "Remplacez ce texte par le résumé de votre projet.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
  {
    slug: "projet-cinq",
    title: "Projet Cinq",
    category: "Portfolio",
    year: "2024",
    colors: ["#ff5a5a", "#2a0909"],
    icon: null,
    tags: ["Web Design", "Next.js", "Tailwind CSS", "GSAP", "Lenis", "Contentful", "Vercel", "Direction artistique"],
    services: ["Direction artistique", "Web Design", "Développement"],
    summary: "Remplacez ce texte par le résumé de votre projet.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, [{ type: "image", src: "" }, { type: "image", src: "" }]],
  },
  {
    slug: "projet-six",
    title: "Projet Six",
    category: "Showcase",
    year: "2023",
    colors: ["#b8c4cc", "#14181b"],
    icon: null,
    tags: ["Supabase", "Vercel", "Web Design", "Responsive", "Next.js", "Tailwind CSS", "GSAP"],
    services: ["Web Design", "Développement", "Base de données"],
    summary: "Remplacez ce texte par le résumé de votre projet.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
];
