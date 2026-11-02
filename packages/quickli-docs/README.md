# quickli-docs

Documentation site for [quiCkLI](https://github.com/spmse/quickli), the minimal Python CLI framework.

Built with [Docusaurus](https://docusaurus.io/) and deployed to [GitHub Pages](https://spmse.github.io/quickli/).

## Development

Use Node.js 24 and the pnpm version pinned in the root `package.json`.
From the repository root:

```sh
corepack pnpm install --frozen-lockfile
corepack pnpm --filter quickli-docs start
```

Or from this directory:

```sh
pnpm install
pnpm start
```

## Build

From the repository root, check TypeScript and build both configured locales:

```sh
corepack pnpm --filter quickli-docs typecheck
corepack pnpm --filter quickli-docs build
```

## Deploy

The release workflow builds the site and deploys its artifact to GitHub Pages after Release
Please creates component releases. A local build does not publish the site.
The configured `pnpm deploy` script invokes Docusaurus directly; it is not the normal
release path. Follow the
[maintainer release checklist](../core/docs/open-source-release.md#release-preparation-checklist)
instead of deploying manually during release preparation.

## Content entry points

- [Getting started](docs/getting-started.md): installation, first CLI, and automatic help.
- [Configuration](docs/concepts/config.md): JSON/YAML/TOML, schemas, and initialization.
- [Implementation guides](docs/guides/index.md): runnable examples, logging integration,
  console scripts, binary packaging, and containerization.
- [Stability outline](docs/roadmap.md): scope and remaining release gates.

The site follows the source checkout, which may contain unreleased APIs. Use an editable
core installation when validating new examples. A successful Docusaurus build checks site
generation and links, not Python execution or the optional PyInstaller/Docker artifacts.

## Configuration highlights

- **i18n**: English as default locale; additional locales can be added to `docusaurus.config.ts`.
- **Mermaid**: Diagram support is enabled via `@docusaurus/theme-mermaid`.
- **Syntax highlighting**: Python, Shell (`bash`), PowerShell, HCL, Docker (container), and YAML (Kubernetes) are enabled in addition to the Docusaurus defaults.
- **AI discoverability**: `static/robots.txt` allows crawling of the documentation site and
  `static/llms.txt` provides a machine-readable project summary with links back to the
  canonical repository documentation and specifications.
