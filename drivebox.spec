# -*- mode: python ; coding: utf-8 -*-

import sys
import tomllib
from pathlib import Path

block_cipher = None


def _resolve_icon() -> str | None:
    """Pick the CI-generated platform icon, falling back to no icon for local builds."""
    build_dir = Path("build")
    if sys.platform == "win32":
        icon_path = build_dir / "icon.ico"
    elif sys.platform == "darwin":
        icon_path = build_dir / "icon.icns"
    else:
        icon_path = Path("src/drivebox/resources/icons/tray_icon.png")
    return str(icon_path) if icon_path.exists() else None


def _write_windows_version_file() -> str | None:
    """Windows version resource, shown in the .exe's Properties > Details."""
    if sys.platform != "win32":
        return None

    project = tomllib.loads(Path("pyproject.toml").read_text())["project"]
    version = project["version"]
    numbers = tuple(int(part) for part in version.split(".")[:3]) + (0,)
    publisher = project["authors"][0]["name"]

    version_file = Path("build") / "version_info.txt"
    version_file.parent.mkdir(exist_ok=True)
    version_file.write_text(
        f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={numbers}, prodvers={numbers}, mask=0x3f, flags=0x0,
                    OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', '{publisher}'),
      StringStruct('FileDescription', 'DriveBox screenshot uploader'),
      StringStruct('FileVersion', '{version}'),
      StringStruct('InternalName', 'drivebox'),
      StringStruct('LegalCopyright', 'MIT License, {publisher}'),
      StringStruct('OriginalFilename', 'drivebox.exe'),
      StringStruct('ProductName', 'DriveBox'),
      StringStruct('ProductVersion', '{version}')])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    )
    return str(version_file)


a = Analysis(
    ["src/drivebox/__main__.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("src/drivebox/resources/icons/tray_icon.png", "drivebox/resources/icons"),
        ("src/drivebox/resources/icons/logo_alt.png", "drivebox/resources/icons"),
    ],
    hiddenimports=[
        "drivebox",
        "drivebox.app",
        "drivebox.auth",
        "drivebox.auth.services",
        "drivebox.auth.credential_loaders",
        "drivebox.auth.token_storage",
        "drivebox.capture",
        "drivebox.clipboard",
        "drivebox.config",
        "drivebox.drive",
        "drivebox.hotkeys",
        "drivebox.services",
        "drivebox.storage",
        "drivebox.ui",
        "drivebox.ui.tray",
        "drivebox.ui.windows",
        "drivebox.ui.windows.components",
        "googleapiclient",
        "google.auth",
        "google.oauth2",
        "google_auth_oauthlib",
        "pynput",
        "pyperclip",
        "keyring",
        "dotenv",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="drivebox",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # UPX triggers antivirus false positives
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No terminal window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_resolve_icon(),
    version=_write_windows_version_file(),
)
