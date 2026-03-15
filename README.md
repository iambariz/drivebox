# DriveBox

DriveBox is a PyQt5 desktop app that captures screenshots, uploads them to Google Drive, and copies a shareable link to your clipboard. It lives in the system tray.

- Take a fullscreen screenshot with one click
- Upload automatically to Google Drive
- Shareable link copied to clipboard instantly
- System tray integration for quick access

---

## Requirements

- Python 3.9+
- A Google OAuth client secrets JSON file

---

## Installation

```bash
git clone https://github.com/yourusername/drivebox.git
cd drivebox
pip install -e .
```

For development (includes linting, testing tools):

```bash
pip install -e .[dev]
```

---

## Configuration

Copy `.env.dist` to `.env` and set `DRIVEBOX_CLIENT_SECRETS` to the path of your Google OAuth client secrets JSON:

```bash
cp .env.dist .env
# Edit .env and set DRIVEBOX_CLIENT_SECRETS=credentials/google-credentials.json
```

On first run, a browser window will open for Google OAuth. The token is cached at `~/.drivebox/token.pickle` for future sessions.

---

## Running

```bash
python -m drivebox
```

---

## Development

### Lint & format

```bash
ruff check src/
ruff format src/
```

### Type check

```bash
mypy src/
```

### Tests

```bash
pytest -v
pytest --cov=src/drivebox   # with coverage (threshold: 80%)
```

### Pre-commit checks

```bash
pre-commit run --all-files
```

---

## Project Structure

```
src/drivebox/
├── auth/           # OAuth flow, token persistence, credential loading
├── capture/        # PIL-based fullscreen screenshot capture
├── clipboard/      # Pyperclip wrapper
├── config/         # Settings, constants, env var names
├── drive/          # Google Drive upload + sharing
├── services/       # Orchestration (screenshot → upload → clipboard)
├── storage/        # Secure file I/O
├── ui/
│   ├── tray/       # System tray icon
│   └── windows/    # Main window + controls
└── __main__.py     # Entry point
```
