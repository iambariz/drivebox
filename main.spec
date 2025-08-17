# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['drivebox/main.py'],   # entry point
    pathex=[],
    binaries=[],
    datas=[
    ('drivebox/resources/icon.png', 'resources'),
    ('drivebox/resources/ffmpeg/*', 'resources/ffmpeg'),
    ('credentials.json', '.'),   #only for dev builds - Todo: Change it before release
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='drivebox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='drivebox'   #folder name inside dist/
)