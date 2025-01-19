# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_cpp.py'],
    pathex=[],
    binaries=[('E:/Dev/Projects/speech-to-text/Release/build_cpu/ggml.dll', 'Release/build_cpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_cpu/whisper.dll', 'Release/build_cpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_cpu/ggml-cpu.dll', 'Release/build_cpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_cpu/ggml-base.dll', 'Release/build_cpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_cpu/whisper-server-cpu.exe', 'Release/build_cpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_cpu/models/ggml-large-v3-turbo-q8_0.bin', 'Release/build_cpu/models/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/models/ggml-large-v3-turbo-q8_0.bin', 'Release/build_gpu/models/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/whisper-server-gpu.exe', 'Release/build_gpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/ggml-cuda.dll', 'Release/build_gpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/ggml-base.dll', 'Release/build_gpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/ggml-cpu.dll', 'Release/build_gpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/whisper.dll', 'Release/build_gpu/'), ('E:/Dev/Projects/speech-to-text/Release/build_gpu/ggml.dll', 'Release/build_gpu/')],
    datas=[('E:/Dev/Projects/speech-to-text/ffmpeg', 'ffmpeg')],
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
