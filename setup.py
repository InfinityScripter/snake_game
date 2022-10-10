from setuptools import setup

APP = ['main.py']
DATA_FILES = ['dreams.mp3', 'bonus.wav', 'game-over.wav', 'logo.png']
OPTIONS = {
    'packages': ['pygame', 'pygame_menu'],
    'argv_emulation': True

}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'pygame', 'pygame_menu'],
)
