# DriveBox

DriveBox is a cross‑platform screenshot and screen recording app with hotkey support, Google Drive upload, and system tray integration.

- 📸 Take fullscreen or region screenshots
- 🎥 Record your screen with ffmpeg
- ☁️ Upload automatically to Google Drive
- 🔑 Global hotkeys for quick actions
- 🖥️ System tray menu for easy access
- 🔔 Desktop notifications with shareable links

---

## 🚀 Features

- **Screenshots**
  - Fullscreen (`Ctrl+Alt+X`)
  - Region (`Ctrl+Alt+R`)
- **Screen Recording**
  - Start recording (`Ctrl+Alt+S`)
  - Stop & upload (`Ctrl+Alt+E`)
- **Clipboard Integration**
  - Upload links are automatically copied
- **Notifications**
  - Desktop notifications with custom icon
- **System Tray**
  - Quick access to all actions

---

## 📦 Installation (Development)

Clone the repo and install in editable mode:

```bash
git clone https://github.com/yourusername/drivebox.git
cd drivebox
pip install -e .
```

### Download ffmpeg

DriveBox requires **ffmpeg** for screen recording.
Run the helper script to download the correct binary for your OS:

```bash
python scripts/download_ffmpeg.py
```

This will place `ffmpeg` inside `drivebox/resources/ffmpeg/`.

---

## ▶️ Running the App

After installing:

```bash
drivebox
```

Or run directly:

```bash
python -m drivebox.main
```

---

## 🧪 Running Tests

We use `pytest` for testing:

```bash
pytest -v
```

---

## 📦 Building Executable (PyInstaller)

To build a standalone executable:

```bash
pyinstaller main.spec
```

The output will be in `dist/drivebox/`:

- `drivebox.exe` (Windows)
- `drivebox` (Linux/Mac)

The build includes:
- `resources/icon.png`
- `resources/ffmpeg/`

---

## ⚙️ Hotkeys

| Action                | Default Hotkey   |
|-----------------------|------------------|
| Fullscreen Screenshot | `Ctrl+Alt+X`     |
| Region Screenshot     | `Ctrl+Alt+R`     |
| Start Recording       | `Ctrl+Alt+S`     |
| Stop Recording        | `Ctrl+Alt+E`     |

Hotkeys can be changed in the **Options** window.

---

## 🛠️ Development Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Download ffmpeg:
   ```bash
   python scripts/download_ffmpeg.py
   ```
4. Run the app:
   ```bash
   drivebox
   ```

---
