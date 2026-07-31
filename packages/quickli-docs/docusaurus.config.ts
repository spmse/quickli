import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const coreProject = readFileSync(resolve(__dirname, '../core/pyproject.toml'), 'utf8');
const coreVersion = coreProject.match(/^version = "([^"]+)"$/m)?.[1] ?? 'unreleased';
const quickliVersion = process.env.QUICKLI_VERSION ?? coreVersion;
const socialImage = 'https://spmse.github.io/quickli/img/quickli-light.png';

const config: Config = {
  title: 'quiCkLI',
  tagline: 'A minimal Python framework for building command-line interfaces.',
  favicon: 'img/quickli-icon-light.svg',

  // Future flags — improve compatibility with the upcoming Docusaurus v4
  future: {
    v4: true,
  },

  // GitHub Pages deployment
  url: 'https://spmse.github.io',
  baseUrl: '/quickli/',
  organizationName: 'spmse',
  projectName: 'quickli',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  // Mermaid diagram support
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  themes: ['@docusaurus/theme-mermaid'],

  // i18n — English is the default; German is the first additional locale.
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
      de: {
        label: 'Deutsch',
        direction: 'ltr',
        htmlLang: 'de-DE',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
          showLastUpdateTime: true,
        },
        blog: {
          showReadingTime: true,
          blogTitle: 'Le quiCkLI Blog',
          blogDescription: 'News, guides, and deep dives from the quiCkLI project.',
          routeBasePath: 'blog',
          blogSidebarTitle: 'All Posts',
          blogSidebarCount: 'ALL',
          postsPerPage: 10,
          feedOptions: {
            type: ['rss', 'atom'],
            title: 'quiCkLI Blog',
            description: 'News, tutorials, and deep dives from the quiCkLI project.',
            copyright: `Copyright © ${new Date().getFullYear()} quiCkLI contributors.`,
          },
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: socialImage,

    metadata: [
      { name: 'keywords', content: 'quickli, python, cli, command-line, framework, tutorial, learning' },
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:image', content: socialImage },
      { name: 'twitter:description', content: 'A minimal Python framework for building command-line interfaces.' },
      { property: 'og:type', content: 'website' },
      { property: 'og:site_name', content: 'quiCkLI' },
      { property: 'og:image', content: socialImage },
    ],

    colorMode: {
      respectPrefersColorScheme: true,
    },

    // Mermaid theme tokens — can be customised per color mode.
    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
    },

    navbar: {
      title: 'quiCkLI',
      logo: {
        alt: 'quiCkLI logo',
        src: 'img/quickli-icon-light-transparent.png',
        srcDark: 'img/quickli-icon-dark-transparent.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/blog',
          label: 'Blog',
          position: 'left',
        },
        {
          to: '/blog/series',
          label: 'Blog series',
          position: 'left',
        },
        {
          href: 'https://github.com/spmse/quickli',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Project',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/spmse/quickli',
            },
            {
              label: 'Issues',
              href: 'https://github.com/spmse/quickli/issues',
            },
            {
              label: 'Changelog',
              href: 'https://github.com/spmse/quickli/releases',
            },
          ],
        },
      ],
      copyright: `quiCkLI ${quickliVersion} · Copyright © ${new Date().getFullYear()} quiCkLI contributors. Built with Docusaurus.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      // Additional language support beyond the Docusaurus defaults.
      // - python       → Python source code
      // - bash         → Shell scripts and terminal sessions
      // - powershell   → PowerShell scripts
      // - hcl          → HashiCorp Configuration Language (Terraform / OpenTofu)
      // - docker       → Dockerfiles and container definitions
      // - yaml         → YAML (Kubernetes manifests, Compose files, …)
      additionalLanguages: ['python', 'bash', 'powershell', 'hcl', 'docker', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
