# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['appCode/DefaultIDE.py'],
    pathex=[],
    binaries=[('./compiler/Default', '.'), ('/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13', '.'), ('/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload', '.'), ('/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages', '.'), ('/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/setuptools/_vendor', '.')],
    datas=[],
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
    a.binaries,
    a.datas,
    [],
    name='DefaultIDE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='DefaultIDE.app',
    icon=None,
    bundle_identifier=None,
)
