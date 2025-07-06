"""nv_dark installer library module. 

Version @release

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_dark
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from configparser import ConfigParser
import os
from pathlib import Path
from shutil import copy2
from shutil import copytree
import sys
from tkinter import messagebox
import zipfile

from nv_dark import Plugin

try:
    import tkinter as tk
except ModuleNotFoundError:
    print(
        (
            'The tkinter module is missing. '
            'Please install the tk support package for your python3 version.'
        )
    )
    sys.exit(1)

PLUGIN = 'nv_dark.py'
VERSION = ' @release'
THEMES_PATH = 'themes/'

root = tk.Tk()
processInfo = tk.Label(root, text='')
message = []

pyz = os.path.dirname(__file__)


def extract_file(sourceFile, targetDir):
    with zipfile.ZipFile(pyz) as z:
        z.extract(sourceFile, targetDir)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def set_colors(iniFile):
    output(f'Setting up the dark mode colors ...\n')
    config = ConfigParser()
    config.read(iniFile, encoding='utf-8')
    for color in Plugin.COLORS:
        config['SETTINGS'][color] = Plugin.COLORS[color]
    with open(iniFile, 'w', encoding='utf-8') as f:
        config.write(f)


def main(zipped=True):
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.title('Setup')
    output(f'*** Installing {PLUGIN}{VERSION} ***\n')
    header = tk.Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Install the plugin.
    homePath = str(Path.home()).replace('\\', '/')
    applicationDir = f'{homePath}/.novx'
    if os.path.isdir(applicationDir):
        pluginDir = f'{applicationDir}/plugin'
        os.makedirs(pluginDir, exist_ok=True)

        # Uninstall nv_themes, if any.
        nvThemesPlugin = f'{pluginDir}/nv_themes.py'
        if os.path.isfile(nvThemesPlugin):
            if not messagebox.askokcancel(
                    'Incompatible plugin detected',
                    'The "nv_themes" plugin will now be uninstalled.'
            ):
                sys.exit()

            os.remove(nvThemesPlugin)

        output(f'Copying "{PLUGIN}" ...')
        copy_file(PLUGIN, pluginDir)

        # Install the themes.
        copy_tree('themes', applicationDir)

        # Install utility.
        copy_file('restore_default_colors.py', applicationDir)

        # Set up the dark mode colors
        set_colors(f'{applicationDir}/config/novx.ini')

        # Show a success message.
        output(
            (
                f'Sucessfully installed "{PLUGIN}" '
                f'at "{os.path.normpath(pluginDir)}".'
            )
        )
    else:
        output(
            (
                'ERROR: Cannot find a novelibre installation '
                f'at "{os.path.normpath(applicationDir)}".'
            )
        )
    root.quitButton = tk.Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
