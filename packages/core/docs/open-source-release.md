# Open Source Release Notes

## GitHub Readiness

The repository includes GitHub Actions workflows for linting, tests, package builds, coverage
artifacts, Release Please versioning, GitHub releases, and GitHub Pages deployment.

Release builds derive the package version from the core release tag, build and test the
package, publish the same built distributions to PyPI, and attach release evidence to the
GitHub release object. The documentation footer receives the same core version.

The project license is MIT.
Project metadata already points to the GitHub repository.

Current GitHub documentation does not list a Python package registry under GitHub Packages.
For Python projects, the supported publishing path documented by GitHub Actions is PyPI,
with release artifacts attached to GitHub Releases.

## Current Release Status

The package is in Alpha. Release Please maintains independent versions and changelogs for the
core library and documentation site. Both packages are grouped into a single Release Please pull
request (`separate-pull-requests: false`) so that a PR touching both packages never produces two
competing release PRs. Merging the Release Please pull request creates the release tag and GitHub
release for each package that has pending changes. The release workflow may publish the core
package to PyPI when the protected `pypi` environment is configured.

PyPI trusted publishing must contain this exact publisher configuration:

- owner: `spmse`
- repository: `quickli`
- workflow: `release.yml`
- environment: `pypi`

The workflow grants `id-token: write` only to the release job and publishes with the official
PyPA action. A mismatch in any trusted-publisher field causes the upload step to fail before
PyPI accepts the package.

Governance files included:

- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

## Confirmed Release Facts

- Package name: `quickli`
- Stylized project name: `quiCkLI`
- License: MIT
- Repository: `https://github.com/spmse/quickli`
- Release trigger: merged Release Please pull requests on `main`
- Core package version: derived from the `quickli` release tag during the release build
- Documentation site: `https://spmse.github.io/quickli/`

## Maintainer Process

Release Please is configured in `release-please-config.json` and
`.release-please-manifest.json`. Release evidence is produced by
`.github/workflows/release.yml`.

All paths in this section are relative to the repository root.

### What the workflow actually does

1. A push to `main` runs Release Please, which creates or updates one grouped release PR.
   Core and documentation retain independent versions and changelogs.
2. Merging that PR lets Release Please create draft releases for components with pending
   changes. The configuration uses component tags such as `core-vX.Y.Z` and `docs-vX.Y.Z`.
   Use the generated tags; do not create an extra manual tag to start this workflow.
3. When Release Please reports a release, the evidence job checks out the released core SHA
   when available, otherwise the workflow SHA. It derives the core version from the tag,
   tests with coverage on Python 3.12, and builds source and wheel distributions.
4. If a core tag exists, the protected `pypi` job publishes those distributions to PyPI,
   uploads distributions and coverage evidence to the core GitHub release, then removes
   its draft status.
5. A separate documentation job typechecks and builds both locales, uploads the Pages
   artifact, and attaches evidence to a documentation release when a docs tag exists.
   The deploy job then publishes the artifact to GitHub Pages.

The workflow is triggered by pushes to `main`, not arbitrary tag pushes or a manual dispatch.
The evidence job uses the `pypi` environment even for a docs-only release, although the PyPI
upload is conditional on a core tag. Account for that environment's approval rules.

The documentation job passes the core tag as `QUICKLI_VERSION`, or `development` when
there is no core release in that run. Verify the displayed footer rather than assuming
the docs component version is the framework version.

## Release Preparation Checklist

This checklist is a preparation procedure, not authorization to publish or a claim that the
current checkout is release-ready. The maintainer chooses the version and approves release.

### 1. Confirm scope and compatibility

- Review configuration parsing, custom schemas/formats, initialization, automatic help,
  and the expanded guides against their specifications and tests.
- Describe the new `config`, `auto_init_config`, `init_config()`, and `auto_help` APIs in
  release notes. Include nested help and explicit alias/value preservation.
- Call out stricter configuration errors: JSON/YAML non-mapping roots no longer silently
  become `{}`, unsupported format identifiers are rejected, and file failures use `ConfigError`.
- Keep the alpha status visible. Do not promise 1.0 stability or select a patch/minor version
  solely from the phrase "stability release"; new public APIs affect that decision.
- Obtain user/maintainer acceptance before treating the work as complete.

### 2. Resolve packaging and documentation gates

- **Missing package README:** `packages/core/pyproject.toml` specifies `readme = "README.md"`,
  but `packages/core/README.md` is absent. Builds can succeed with a warning and an incomplete
  project description. Before publishing, choose either a package-local README included in
  the source distribution or an existing package-local document referenced by the metadata.
  A local README improves package discovery but needs maintenance; reusing a document
  avoids duplication but must still read well on PyPI. Rebuild and inspect both archives.
- Ensure installation examples distinguish released PyPI packages from the current source
  checkout. Validate new APIs against the release candidate, not an older installed version.
- Review generated English pages, locale fallback, navigation, code blocks, and admonitions.
  A successful site build does not execute Python snippets.
- Treat the PyInstaller and Docker recipes as guides until their actual artifacts have been
  built and smoke-tested. They are not artifacts produced by the framework release workflow.

### 3. Run validation on the release candidate

From `packages/core`, in an activated environment with the existing development dependencies:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest --cov=quickli --cov-report=term-missing --cov-report=xml --cov-fail-under=80
python -m build --sdist --wheel
```

Run the unit suite on Python 3.12, 3.13, and 3.14. CI's Python matrix is conditional on
source/test changes, so do not treat a skipped matrix on a documentation-only release PR as
fresh compatibility evidence. The release evidence job itself tests Python 3.12.

From the repository root with Node.js 24 and the pinned pnpm version:

```bash
corepack pnpm install --frozen-lockfile
corepack pnpm --filter quickli-docs typecheck
corepack pnpm --filter quickli-docs build
```

Then verify the distributable, not just an editable installation:

1. Inspect wheel metadata and the source archive for the approved version, MIT license,
   dependencies, and complete project description.
2. Install the wheel in a clean virtual environment outside the checkout.
3. Exercise root/command/nested `--help` and `-h`, then verify successful output, stderr,
   and nonzero error exits through `Application.main()`.
4. Initialize custom YAML and JSON configurations, edit them, and confirm reinitialization
   preserves the changes. Check invalid syntax and schema errors.
5. Exercise the logging/console-script example. If binary/container distribution is claimed,
   build and test those artifacts on each promised target platform too.
6. Review security results, dependency advisories, and secret scans for the release candidate.

For example, after building, replace the wheel placeholder with the actual generated filename:

```bash
python -m venv /tmp/quickli-release-check
/tmp/quickli-release-check/bin/python -m pip install \
  "packages/core/dist/quickli-<version>-py3-none-any.whl"
```

These are POSIX commands run from the repository root. Quote the wheel path after substituting
the version; on Windows, use the virtual environment's `Scripts/python.exe`.
Do not install an unexpanded placeholder.

### 4. Review the generated release PR and publishing configuration

1. Merge accepted implementation/documentation changes using conventional commits.
   Use `feat(docs):` or `fix(docs):` for documentation changes intended to trigger a docs
   release; bare `docs:` changes do not trigger one.
2. Inspect the grouped Release Please PR: core metadata, package JSON files, manifest,
   component changelogs, proposed versions, and compatibility notes must agree.
   Do not hand-bump versions in this preparation work.
3. Confirm repository Actions permissions allow Release Please to create PRs/releases and
   that the protected `pypi` environment has its intended reviewers and branch rules.
4. Verify the trusted publisher fields listed above and that GitHub Pages is configured
   for GitHub Actions deployment. Never commit a PyPI token as a workaround.
5. Obtain release approval, then merge the generated release PR and monitor its workflow.

### 5. Verify publication and keep evidence

1. Confirm PyPI contains the intended core version and that its distributions match the
   tested release artifacts; verify hashes and inspect the rendered project description.
2. Check component GitHub releases are no longer drafts and contain their expected evidence.
3. Install `quickli==<approved-version>` from PyPI into a fresh environment and repeat the
   key initialization/help smoke tests. Substitute the approved version before running.
4. Check the deployed documentation, guide links, locale behavior, and framework version.
5. Record validation evidence and known limitations in the release notes before announcing.

If publication fails partway through, inspect the failing job and existing PyPI/GitHub state
before retrying. The workflow uses `skip-existing: true`; an existing PyPI version is immutable.
Do not delete/recreate release tags or reuse a published version for changed distributions.
A changed package needs a new approved version; a transient failure may only need a retry
after the cause is understood.
