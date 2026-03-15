# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] — v1.0.0 (MVP, targeting merge to master)

### In Progress
- Desktop notifications ("Uploading…", "Link copied!", error states)
- Global hotkey (`Ctrl+Shift+S`) to trigger screenshot while app is backgrounded
- Polish: app icon, better error messages, loading states in UI
- Unit tests covering all services (80% coverage threshold)

---

## [Unreleased] — v2.0.0

### Planned
- Settings window: customisable hotkey, upload folder, default file permissions, auto-start on boot
- Permission controls: toggle public/private on upload, optional expiring links
- Folder management: create/select Drive folder, organise by date (`YYYY/MM/DD`)

---

## [Unreleased] — v3.0.0

### Planned
- Area selection with drag, crosshair cursor, and preview before upload
- Window capture: active window only, multi-monitor support
- Activity log: view history, re-copy links, delete from Drive, search
- Additional shortcuts: `Ctrl+Shift+A` (area), `Ctrl+Shift+W` (window)

---

## [Unreleased] — v4.0.0

### Planned
- Watch a local folder and auto-upload new files
- Sync deletions and conflict resolution

---

## [Unreleased] — v5.0.0

### Planned
- Full screen and area recording, audio toggle, stop/pause controls
- Post-processing: compression, format conversion, basic trim

---

## [0.2.0] — 2025 (v2 rework, pre-release)

### Added
- Full project rework under `master-v2` branch
- PyQt5 main window with login/logout auth controls
- Google OAuth flow with token caching (`~/.drivebox/token.pickle`)
- Credential loading chain: Keyring → `DRIVEBOX_CLIENT_SECRETS` env var → file
- Google Drive upload client with shareable link generation
- PIL-based fullscreen screenshot capture
- Clipboard manager (pyperclip wrapper)
- Screenshot service orchestrating capture → upload → clipboard copy
- System tray icon with context menu
- Auth-aware tray menu (items enabled/disabled based on login state)
- Global hotkey support (Linux)
- `.env` support via `python-dotenv`
- Secure file storage service (0o600 files, 0o700 dirs)
- Pre-commit hooks (ruff, mypy, large file check, private key detection)

---

## [0.1.0] — 2024 (initial version)

### Added
- Initial PyQt5 app with system tray
- Fullscreen and region screenshot capture
- Screen recording via ffmpeg
- Google Drive upload and shareable link
- Hotkey support with customisable bindings via settings window
- Desktop notifications
- PyInstaller build configuration
- GitHub Actions CI/CD pipeline
