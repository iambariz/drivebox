# DriveBox

![Build](https://github.com/iambariz/drivebox/actions/workflows/build.yml/badge.svg?branch=v1.1.0)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

> Take a screenshot. It's in your clipboard. That's it.

DriveBox is a lightweight PyQt5 desktop app that lives in your system tray. One click captures your screen — full or a selected region — uploads it to Google Drive, and copies a shareable link to your clipboard — instantly.

---

## Download

Grab the latest binary for your platform from the [Releases](https://github.com/iambariz/drivebox/releases) page — no Python required.

| Platform | File |
|----------|------|
| Linux    | `drivebox-linux` |
| Windows  | `drivebox-windows.exe` |
| macOS    | `drivebox-macos` |

---

## Features

- **One-click screenshots** — fullscreen capture with a single button or hotkey
- **Region capture** — drag-select a portion of the screen with `Ctrl+Shift+R`
- **Google Drive upload** — automatic upload with shareable link generation
- **Clipboard integration** — link is copied instantly, ready to paste
- **System tray** — runs quietly in the background, always accessible
- **Global hotkeys** — `Ctrl+Shift+S` (fullscreen) and `Ctrl+Shift+R` (region) trigger a capture from anywhere
- **Secure auth** — OAuth 2.0 with token caching, no passwords stored

---

## Getting Started

### 1. Get Google OAuth credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable the **Google Drive API**
3. Create **OAuth 2.0 credentials** (Desktop app type)
4. Download the JSON file

### 2. Configure

```bash
cp .env.dist .env
```

Edit `.env` and set the path to your credentials file:

```
DRIVEBOX_CLIENT_SECRETS=credentials/google-credentials.json
```

### 3. Run

```bash
python -m drivebox
```

On first launch, a browser window will open for Google sign-in. After that, the token is cached at `~/.drivebox/token.pickle`.

---

## Installation (from source)

```bash
git clone https://github.com/iambariz/drivebox.git
cd drivebox
pip install -e .
```

For development:

```bash
pip install -e .[dev]
```

---

## Development

### Commands

```bash
# Run
python -m drivebox

# Tests
.venv/bin/pytest tests/unit/ -v
.venv/bin/pytest tests/unit/ --cov=src/drivebox   # with coverage

# Lint & format
ruff check src/
ruff format src/

# Type check
mypy src/

# All pre-commit checks
pre-commit run --all-files
```

### Project Structure

```
src/drivebox/
├── actions.py      # Shared CaptureAction registry (tray menu, hotkeys, window)
├── auth/           # OAuth flow, token persistence, credential loading
├── capture/        # Capturer interface + per-mechanism handlers:
│                    #   QScreenCapturer (X11/Windows/macOS), WaylandPortalCapturer,
│                    #   factory.py (picks the right one), region_selector.py (drag-select UI)
├── clipboard/      # Clipboard manager
├── config/         # Settings, constants, env var names
├── drive/          # Google Drive upload + sharing
├── hotkeys/        # Global hotkey listener (pynput)
├── services/       # Orchestration (capture → upload → clipboard)
├── storage/        # Secure file I/O
├── ui/
│   ├── tray/       # System tray icon
│   └── windows/    # Main window + controls
└── __main__.py     # Entry point
```

### Data Flow

```
User action (tray menu / hotkey / window button)
  → ScreenshotService.take_and_upload_screenshot() / take_and_upload_region()
      ├─ get_capturer().capture_fullscreen() / capture_region()   → PNG bytes (or None if cancelled)
      ├─ DriveClient.upload_and_share()                            → shareable URL
      └─ ClipboardManager.copy(URL)
```

---

## Roadmap

- [x] Fullscreen screenshot + upload
- [x] System tray
- [x] Global hotkey
- [x] Area/region screenshot
- [ ] Desktop notifications
- [ ] Settings window
- [ ] Activity log
- [ ] Video/screen recording capture

---

## License

MIT
