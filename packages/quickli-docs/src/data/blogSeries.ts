export type BlogSeriesArticle = {
  slug: string;
  title: string;
  titleDe: string;
  position: number;
};

export type BlogSeries = {
  id: string;
  title: string;
  titleDe: string;
  description: string;
  descriptionDe: string;
  category: string;
  categoryDe: string;
  articles: BlogSeriesArticle[];
};

export const blogSeries: BlogSeries[] = [
  {
    id: 'getting-started',
    title: 'Getting Started with quiCkLI',
    titleDe: 'Erste Schritte mit quiCkLI',
    description: 'A practical path from your first command to a multi-command application.',
    descriptionDe: 'Ein praktischer Weg vom ersten Befehl zur Multi-Command-Anwendung.',
    category: 'Getting Started',
    categoryDe: 'Erste Schritte',
    articles: [
      {
        slug: 'quickli-tutorial-01-hello-world',
        title: 'Your First Command-Line Application',
        titleDe: 'Deine erste Kommandozeilenanwendung',
        position: 1,
      },
      {
        slug: 'quickli-tutorial-02-file-tools',
        title: 'Reading Files and Validating Input',
        titleDe: 'Dateien lesen und Eingaben validieren',
        position: 2,
      },
      {
        slug: 'quickli-tutorial-03-multi-command-cli',
        title: 'Multi-Command Applications',
        titleDe: 'Multi-Command-Anwendungen',
        position: 3,
      },
    ],
  },
  {
    id: 'building-quickli',
    title: 'Building quiCkLI',
    titleDe: 'quiCkLI entwickeln',
    description: 'The motivation, audience, and development lessons behind the project.',
    descriptionDe: 'Motivation, Zielgruppe und Erkenntnisse aus der Entwicklung des Projekts.',
    category: 'Building quiCkLI',
    categoryDe: 'quiCkLI entwickeln',
    articles: [
      {
        slug: 'building-quickli-01-motivation',
        title: 'Why I Started a Minimal CLI Framework',
        titleDe: 'Warum ich ein minimales CLI-Framework gestartet habe',
        position: 1,
      },
      {
        slug: 'building-quickli-02-target-audience',
        title: 'Who Is This Framework For?',
        titleDe: 'Für wen ist dieses Framework gedacht?',
        position: 2,
      },
    ],
  },
];
