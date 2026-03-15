# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No terminal window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
