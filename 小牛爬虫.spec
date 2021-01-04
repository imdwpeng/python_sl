# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['index.py'],
             pathex=['/Users/dwp/github/python_sl'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='小牛爬虫',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='ox.ico')
app = BUNDLE(exe,
             name='小牛爬虫.app',
             icon='ox.ico',
             bundle_identifier=None)
