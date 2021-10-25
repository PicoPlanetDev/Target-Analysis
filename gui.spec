# -*- mode: python ; coding: utf-8 -*-

# This spec file is used to generate a Windows executable for Target Analysis.
# Make sure to set pathex to the correct path to the directory containing Target Analysis.
# The path is currently set for my machine, which will likey be different for you.
# I set the folder name to 'Target-Analysis - Copy' because I just make a copy of the source folder and Windows names it like that.

# To build this spec file, run the following command: 'pyinstaller gui.spec'
# The built data will be inside the folder 'dist/TargetAnalysis'
# For user frienldlyness, I hide all folders and files that are not needed inside that directory that the user doesn't need to interact with.

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
          name='TargetAnalysis',
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
