import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('main.py', base=base)
]

setup(name='your_app_name',
      version='1.0',
      description='your_app_description',
        options={
        "build_exe": {
            "packages": ["numpy", "cv2", ],  # 必要なパッケージ   # 同梱するファイル
        }
    },
      executables=executables
      )