# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_cpp.py'],
    pathex=[],
    binaries=[('E:/Dev/Projects/speech-to-text/Release/whisper-server.exe', 'Release/')],
    datas=[('E:/Dev/Projects/speech-to-text/Release/models/ggml-large-v3.bin', 'Release/models/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Bg-Audio-Transcriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Bg-Audio-Transcriber',
)