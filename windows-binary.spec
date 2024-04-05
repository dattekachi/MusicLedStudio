# -*- mode: python ; coding: utf-8 -*-
import os
from hiddenimports import hiddenimports
from mls.consts import PROJECT_VERSION
spec_root = os.path.abspath(SPECPATH)

venv_root = os.path.abspath(os.path.join(SPECPATH, '..'))
block_cipher = None
print(venv_root)
# Remove the mls.env file if it exists
os.remove("mls.env") if os.path.exists("mls.env") else None

# Get environment variables
github_ref = os.getenv('GITHUB_REF')
github_sha_value = os.getenv('GITHUB_SHA')

# Initialize variables
variables = [f"GITHUB_SHA = {github_sha_value}"]
SHOW_CONSOLE = False

# Check if this is a release
if github_ref and 'refs/tags/' in github_ref:
    # cleanup github_ref to remove /refs/tags/v and leave just the version
    github_ref_cleaned = github_ref.replace('refs/tags/v', '')
    assert PROJECT_VERSION == github_ref_cleaned, "Version and Tag do not match - aborting release."
    variables.append('IS_RELEASE = true')
    SHOW_CONSOLE = False
else:
    variables.append('IS_RELEASE = false')

# Write to mls.env file
with open('mls.env', 'a') as file:
    file.write('\n'.join(variables))
a = Analysis([f'{spec_root}\\mls\\__main__.py'],
             pathex=[f'{spec_root}', f'{spec_root}\\mls'],
             binaries=[],
             datas=[(f'{spec_root}/mls_frontend', 'mls_frontend/'), (f'{spec_root}/mls/', 'mls/'), (f'{spec_root}/mls_assets', 'mls_assets/'),(f'{spec_root}/mls_assets/tray.png','.'), (f'{spec_root}/mls.env','.')],
             hiddenimports=hiddenimports,
             hookspath=[f'{venv_root}\\lib\\site-packages\\pyupdater\\hooks'],
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
          name='MusicLedStudio',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=SHOW_CONSOLE,
          icon=f'{spec_root}\\mls_assets\\discord.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='MusicLedStudio')

# Cleanup mls.env
os.remove("mls.env")