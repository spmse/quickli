# Open Source Release Notes

## GitHub Readiness

The repository now includes GitHub Actions workflows for linting, tests, package builds,
coverage artifacts, and tag-based releases.

Tag-based releases now build and test the package, create the GitHub release object, and
only then publish the same built distributions to PyPI.

The project license is MIT.
Project metadata already points to the GitHub repository.

Current GitHub documentation does not list a Python package registry under GitHub Packages.
For Python projects, the supported publishing path documented by GitHub Actions is PyPI,
with release artifacts attached to GitHub Releases.

## Current Release Status

The package is in Alpha. The current release workflow is tag-driven: a `v*` tag runs the
release workflow and may publish to PyPI when the protected `pypi` environment is configured.
Release Please is approved future work and is not implemented here.

Governance files now included:

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

## Risk Notes

- Renaming the package after publication will be more expensive than it is now.
- Publishing before the plugin story is designed may create user expectations the project does not yet meet.

## Confirmed Release Facts

- Package name: `quickli`
- Stylized project name: `quiCkLI`
- License: MIT
- Repository: `https://github.com/spmse/quickli`
- Release trigger: Git tags matching `v*`

## Maintainer Process

The current release workflow is defined in `.github/workflows/release.yml`. Release Please is
approved future work and will require a separate implementation change.
