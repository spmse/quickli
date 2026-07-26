import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'quiCkLI',
  tagline: 'A minimal Python framework for building command-line interfaces.',
  favicon: 'img/favicon.ico',

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

  // i18n — English is the default; additional locales can be added here later.
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        // Docs and blog are disabled until content is added.
        docs: false,
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

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
        src: 'img/logo.svg',
      },
      items: [
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
      copyright: `Copyright © ${new Date().getFullYear()} quiCkLI contributors. Built with Docusaurus.`,
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
