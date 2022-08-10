# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\svyat\\PycharmProjects\\UA_Server\\Convertor_DA_UA.py'],
             pathex=['C:\\Users\\svyat\\PycharmProjects\\UA_Server'],
             binaries=[],
             datas=[],
             hiddenimports=['win32timezone'],
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
          name='Convertor_DA_UA',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='C:\\Users\\svyat\\OPC_DA_Allan Bredly\\Для установщика\\Gazprom-symbol.ico')
