# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Google Drive upload now runs on a single-worker background queue (`QThreadPool`, `CaptureUploadService` + `UploadJob`) instead of blocking the UI thread — the window stays responsive during slow uploads

### Changed
- Removed `ScreenshotService` — capture (main thread) and upload+clipboard (worker thread) are now decoupled, so `CaptureUploadService` owns orchestration instead of one class doing both synchronously

### Process
- Added `CONTRIBUTING.md` and a CI check (`changelog-check` in `test.yml`) requiring a `CHANGELOG.md` entry on any PR touching `src/`; versioning/release process documented (version bumps only happen at release time, not per-PR)

## [1.1.0] - 2026-08-10

### Added
- Region (partial) screenshot capture — drag-to-select overlay on X11/Windows/macOS via a custom Qt selector, native compositor picker on Wayland via xdg-desktop-portal's interactive `Screenshot` call
- `Capturer` interface (`capture/base.py`) with one handler per capture mechanism (`QScreenCapturer`, `WaylandPortalCapturer`), selected at runtime by `capture/factory.py`
- Shared `CAPTURE_ACTIONS` registry (`actions.py`) driving the tray menu, global hotkeys, and window buttons from a single source instead of duplicated per-action wiring
- App icon (`.ico`/`.icns`) generated at build time and embedded in Windows/macOS release binaries

### Fixed
- Fullscreen capture returning solid black under Wayland — now routes through xdg-desktop-portal instead of `QScreen.grabWindow()`, which reads X11's root window and is never filled with real pixels for arbitrary clients under Wayland's compositor model
- Screenshot capture was Linux/X11-only (`ffmpeg x11grab`) despite the release pipeline building and shipping Windows/macOS binaries that could never actually take a screenshot — replaced with Qt's cross-platform `QScreen.grabWindow()`
- Missing `python-dotenv` dependency — imported in `__main__.py` but never declared in `pyproject.toml`

### Changed
- CI now runs `ruff`, `mypy`, and `bandit` in addition to `pytest` (previously only tests ran, so lint/type/security issues went uncaught)
- Removed empty `adapters/`, `ports/`, `domain/` scaffolding — unused hexagonal-architecture directories with no implementation
- Removed redundant `requirements.txt` and the `pipreqs-generate` pre-commit hook — `pyproject.toml` and `requirements-lock.txt` are the real dependency source of truth

## [1.0.0] - 2026-03-15

Full rewrite of the original prototype (see `0.1.0-beta` below) onto its current architecture.

### Added
- OAuth 2.0 sign-in with cached tokens; credentials loaded from keyring, `DRIVEBOX_CLIENT_SECRETS` env var, or a local file, in that order
- Google Drive upload with shareable link generation
- Fullscreen screenshot capture, clipboard copy
- System tray icon with an auth-aware context menu
- Global hotkey (`Ctrl+Shift+S`)
- PyInstaller packaging and a GitHub Actions build/release pipeline
- Unit test suite with pre-commit hooks (ruff, mypy)

## [0.1.0-beta] - 2025-07-15

Initial prototype.

### Added
- Screen capture via `mss`, upload to Google Drive, clipboard copy
- System tray with a configurable hotkey and an options window
- Basic desktop notifications
- Early attempt at region/area screenshot capture (Wayland support noted as unresolved at the time)

### Known issues
- Screen recording via ffmpeg was started but not completed
