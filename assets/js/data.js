/* ==========================================================================
   SITE CONTENT
   --------------------------------------------------------------------------
   Every text and every project lives here: edit this file to customise the
   portfolio without touching the HTML.

   Media: each media entry accepts
     { type: "image", src: "assets/media/my-image.jpg", alt: "..." }
     { type: "video", src: "assets/media/my-video.mp4", poster: "..." }
   Without `src`, a placeholder gradient is shown instead.
   ========================================================================== */

window.SITE = {
  name: "Your Name",
  domain: "yourname.com",
  email: "hello@yourname.com",
  title: "Design Engineer",

  // The three info columns at the top of the page
  header: [
    { label: "US Based", value: "Working globally" },
    { label: "Building at", value: "Company", url: "https://example.com" },
    { label: "Freelance availability", value: "September 2025" },
  ],

  // Text scrolling under the name in the bottom dock
  roles: ["Creative Design Engineer", "Awwwards Stalker", "Product Builder", "Next.js Enthusiast"],
  // Dock thumbnail and contact button emoji (or an image: { type: "image", src: "..." })
  avatar: "🤙🏼",

  hero: {
    top: ["A", "Seriously", "Good"],
    title: ["Design", "Engineer"],
    scrollLeft: "Scroll for",
    scrollRight: "cool sh*t",
  },

  // Video that grows on scroll below the hero
  showreel: { type: "video", src: "", poster: "", label: "Showreel" },

  about: {
    label: "Myself",
    text: "Passionate about merging design and engineering, I craft smooth, interactive experiences with purpose. With a focus on motion, performance, and detail, I help bring digital products to life for forward-thinking brands around the world.",
    media: { type: "video", src: "", label: "Portrait" },
  },

  work: { title: "Work", year: "'25", seeAll: "See all" },

  services: {
    label: "Services",
    intro: "Evolving with every brief and built for impact, my process spans design, development, and brand strategy—aligning vision with execution to bring clarity and edge to every project.",
    items: [
      {
        title: "Brand Strategy",
        text: "Helping others uncover their brand's purpose and uniqueness – and the game plan to deliver it to win their customers' devotion.",
        tags: ["Research & Insights", "Brand Strategy", "Competitive Study", "Voice & Tone", "Naming & Copywriting", "Workshops"],
        media: { type: "image", src: "", colors: ["#ff7a3d", "#2a0e04"] },
      },
      {
        title: "Digital Design",
        text: "Designing engaging digital experiences that combine brand strategy and creativity with UX insights to deliver functionality and ease of use.",
        tags: ["Identity Design", "Wireframing", "UI", "UX", "Web Design", "Product Design"],
        media: { type: "image", src: "", colors: ["#3fb6c9", "#0b2227"] },
      },
      {
        title: "Development",
        text: "Building digital products that combine design, technology, and business strategy to deliver seamless user experiences.",
        tags: ["Frontend Development", "SEO", "Motion", "Animation", "WebGL", "CMS Development", "Databases"],
        media: { type: "image", src: "", colors: ["#9a9a9a", "#141414"] },
      },
    ],
  },

  // Logos: SVG files in assets/icons (from simple-icons, CC0 license)
  stack: {
    title: ["Modern", "Tech Stack"],
    label: "Professional at",
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

  // Footer tiles (the "Work" and "Contact" tiles are added automatically)
  socials: [
    { label: "Github", url: "https://github.com/" },
    { label: "Instagram", url: "https://instagram.com/" },
    { label: "LinkedIn", url: "https://linkedin.com/" },
  ],

  workPage: { years: "[2022-2025]", title: "Selected Work" },
};

/* --------------------------------------------------------------------------
   PROJECTS
   - The first two are featured on the home page.
   - `tags`: text scrolling on the card.
   - `preview`: video revealed when hovering the card.
   - `gallery`: one media = full width, an array of two media = two columns.
   -------------------------------------------------------------------------- */
window.PROJECTS = [
  {
    slug: "project-one",
    title: "Project One",
    category: "Portfolio",
    year: "2025",
    colors: ["#f2a3c4", "#2b1520"],
    icon: null,
    tags: ["Art Direction", "Voice & Tone", "UI", "UX", "Next.js", "Tailwind CSS", "GSAP", "Motion", "Matter.js", "Lenis", "Vercel"],
    services: ["Art Direction", "Voice & Tone", "UI", "UX", "Development"],
    summary: "Replace this text with your project summary: the client, the context, the goal and your role.",
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
    slug: "project-two",
    title: "Project Two",
    category: "Product",
    year: "2025",
    colors: ["#f5d90a", "#2a2500"],
    icon: null,
    tags: ["Art Direction", "Naming & Copywriting", "Voice & Tone", "Brand Design", "Strategy", "UX", "UI", "Web Design", "Product Design", "Media Production"],
    services: ["Art Direction", "Naming & Copywriting", "Voice & Tone", "Brand Design", "Strategy", "UX", "UI", "Web Design", "Product Design", "Media Production"],
    summary: "Replace this text with your project summary: the client, the context, the goal and your role.",
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
    slug: "project-three",
    title: "Project Three",
    category: "Services",
    year: "2024",
    colors: ["#e8442c", "#250805"],
    icon: null,
    tags: ["Web Design", "Next.js", "Tailwind CSS", "GSAP", "Motion", "Lenis", "Contentful", "Vercel", "Shopify API"],
    services: ["Web Design", "Development", "Motion"],
    summary: "Replace this text with your project summary.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, [{ type: "image", src: "" }, { type: "image", src: "" }]],
  },
  {
    slug: "project-four",
    title: "Project Four",
    category: "Product",
    year: "2024",
    colors: ["#2fb5a5", "#04201d"],
    icon: null,
    tags: ["Competitive Study", "Voice & Tone", "Workshops", "Strategy", "UX", "UI", "Web Design", "Responsive Design"],
    services: ["Strategy", "UX", "UI", "Web Design"],
    summary: "Replace this text with your project summary.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
  {
    slug: "project-five",
    title: "Project Five",
    category: "Portfolio",
    year: "2024",
    colors: ["#ff5a5a", "#2a0909"],
    icon: null,
    tags: ["Web Design", "Next.js", "Tailwind CSS", "GSAP", "Lenis", "Contentful", "Vercel", "Art Direction"],
    services: ["Art Direction", "Web Design", "Development"],
    summary: "Replace this text with your project summary.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, [{ type: "image", src: "" }, { type: "image", src: "" }]],
  },
  {
    slug: "project-six",
    title: "Project Six",
    category: "Showcase",
    year: "2023",
    colors: ["#b8c4cc", "#14181b"],
    icon: null,
    tags: ["Supabase", "Vercel", "Web Design", "Responsive Design", "Next.js", "Tailwind CSS", "GSAP"],
    services: ["Web Design", "Development", "Databases"],
    summary: "Replace this text with your project summary.",
    cover: { type: "image", src: "" },
    preview: { type: "video", src: "" },
    gallery: [{ type: "image", src: "" }, { type: "image", src: "" }],
  },
];
