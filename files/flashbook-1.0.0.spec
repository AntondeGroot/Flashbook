# -*- mode: python -*-

block_cipher = None


a = Analysis(['flashbook-1.0.0.py'],
             pathex=['C:\\Users\\Anton\\.spyder-py3\\Flashbook Flashcard\\Final'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='flashbook-1.0.0',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='book.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='flashbook-1.0.0')
