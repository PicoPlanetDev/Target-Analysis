# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['gui.pyw'],
             pathex=['D:\\Libraries\\Documents\\GitHub\\Target-Analysis - Copy'],
             binaries=[],
             datas=[
                 ("assets/*", "assets"),
                 ("assets/sun-valley/*", "assets/sun-valley"),
                 ("assets/sun-valley/theme/*", "assets/sun-valley/theme"),
                 ("assets/sun-valley/theme/dark/*", "assets/sun-valley/theme/dark"),
                 ("assets/sun-valley/theme/light/*", "assets/sun-valley/theme/light"),
                 ("data/.gitkeep", "data"),
                 ("help/*", "help"),
                 ("images/*", "images"),
                 ("images/output/.gitkeep", "images/output"),
                 ("./*.md", ".")],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon="assets/icon.ico",
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='TargetAnalysis')
