# Open Source Release Notes

## GitHub Readiness

The repository includes GitHub Actions workflows for linting, tests, package builds, coverage
artifacts, Release Please versioning, GitHub releases, and GitHub Pages deployment.

Tag-based releases now build and test the package, create the GitHub release object, and
only then publish the same built distributions to PyPI.

The project license is MIT.
Project metadata already points to the GitHub repository.

Current GitHub documentation does not list a Python package registry under GitHub Packages.
For Python projects, the supported publishing path documented by GitHub Actions is PyPI,
with release artifacts attached to GitHub Releases.

## Current Release Status

The package is in Alpha. Release Please maintains independent versions and changelogs for the
core library and documentation site. Merging a Release Please pull request creates the release
tag and GitHub release. The release workflow may publish the core package to PyPI when the
protected `pypi` environment is configured.

Governance files now included:

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

## Risk Notes

- Renaming the package after publication will be more expensive than it is now.
- Publishing before the plugin story is designed may create user expectations the project
	does not yet meet.

## Confirmed Release Facts

- Package name: `quickli`
- Stylized project name: `quiCkLI`
- License: MIT
- Repository: `https://github.com/spmse/quickli`
- Release trigger: merged Release Please pull requests on `main`
- Documentation site: `https://spmse.github.io/quickli/`

## Maintainer Process

Release Please is configured in `release-please-config.json` and
`.release-please-manifest.json`. Release evidence is produced by
`.github/workflows/release-please.yml`.
