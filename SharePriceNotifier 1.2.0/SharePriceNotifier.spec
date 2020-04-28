# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Scripts\\SharePriceNotifier.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\ShareMarketStuff\\Share_Price_Notifier\\SharePriceNotifier 1.2.0'],
             binaries=[],
             datas=[],
             hiddenimports=['DataScrapper', 'User_Inputs', 'Operations', 'SaveLogs', 'requests', 'json', 'bs4', 'os', 'time', 'win10toast', 'pkg_resources.py2_warn'],
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
          name='SharePriceNotifier',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Includes\\Stocks Icon.ico')
