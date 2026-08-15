# Contributing

## Before opening a PR

- Branch off `master`, named `fix/...` or `feat/...` depending on the change.
- Run `pre-commit run --all-files` (or just `git commit` — the hooks run automatically) — ruff, mypy, bandit, detect-secrets, and the unit tests all need to pass locally before you push.
- **If your PR changes anything in `src/`, add an entry to `CHANGELOG.md` under `[Unreleased]`.** This is enforced in CI (`changelog-check` job in `test.yml`) — a PR touching `src/` without a matching `CHANGELOG.md` change will fail the check.
  - Use the existing `### Added` / `### Fixed` / `### Changed` sub-headings under `[Unreleased]`.
  - Write it for a reader who wasn't in the PR discussion — plain description of the user-visible or architectural change, not a commit-message recap.
- If the change affects anything the README documents — features, project structure, data flow, setup steps, the roadmap checklist — update `README.md` in the same PR. This isn't CI-enforced (too easy for the check to be wrong about what "counts"), but treat it as required, not optional.

## Versioning and releases

`pyproject.toml`'s `version` field and git tags (`vX.Y.Z`) only change **at release time**, not per-PR. Between releases, `pyproject.toml` stays fixed and `CHANGELOG.md`'s `[Unreleased]` section accumulates entries from merged PRs.

When it's actually time to cut a release:

1. Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md`, and add a fresh empty `## [Unreleased]` above it.
2. Bump `version` in `pyproject.toml` to match.
3. If `README.md`'s Build badge is pinned to a specific tag (`?branch=vX.Y.Z`), update it to the new version.
4. Commit, push to `master`.
5. `git tag vX.Y.Z && git push origin vX.Y.Z` — this triggers `build.yml`, which builds all three platform binaries and publishes the GitHub Release automatically.
6. Verify the release actually works before considering it done — download and run the binaries, at least on whichever platforms you have access to. A green CI run only proves the binaries *built*, not that they work (this bit us once: v1.0.0's Windows/macOS binaries built successfully but couldn't actually take a screenshot).

## Why enforce this

Two real incidents drove these rules:
- `CHANGELOG.md` drifted so far from git history that it described features (region capture, desktop notifications, screen recording) as already shipped in versions where they didn't exist yet — reconciling it required cross-referencing raw commit history from scratch.
- The README's `Data Flow` and `Project Structure` sections kept referencing deleted classes (`ScreenCapture`, `ScreenshotService`) for multiple PRs after they were removed, because nothing forced a docs pass alongside the code change.

The CHANGELOG check is CI-enforced because it's mechanically checkable (did this file change, yes or no). The README expectation isn't automated, because "did the docs actually get updated *correctly*" isn't something a diff check can verify — that part still relies on the PR author (and reviewer) actually doing it.
