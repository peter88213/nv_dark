"""nv_dark installer library module. 

Version @release

Copyright (c) 2025-2026 Peter Triesberger
For further information see https://github.com/peter88213/nv_dark
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from configparser import ConfigParser
import os
from pathlib import Path
from shutil import copy2
from shutil import copytree
import shutil
import sys
from tkinter import TkVersion
from tkinter import messagebox
import zipfile

from nv_dark import Plugin

PLUGIN = 'nv_dark.py'
VERSION = '@release'
THEME_DIR = 'themes'
THEME_PACKAGE = 'awthemes'

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


def restore_default_colors():
    print('Restoring novelibre default colors ...')
    homePath = str(Path.home()).replace('\\', '/')
    configFile = f'{homePath}/.novx/config/novx.ini'

    with open(configFile, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    newlines = []
    for line in lines:
        if not line.startswith('color_'):
            newlines.append(line)
    with open(configFile, 'w', encoding='utf-8') as f:
        f.write('\n'.join(newlines))
    print('Default colors successfully restored.')


def set_colors(iniFile):
    print(f'Setting up the dark mode colors ...\n')
    config = ConfigParser()
    config.read(iniFile, encoding='utf-8')
    for color in Plugin.COLORS:
        config['SETTINGS'][color] = Plugin.COLORS[color]
    with open(iniFile, 'w', encoding='utf-8') as f:
        config.write(f)


def handle_wrong_tk_version(pluginDir):
    if TkVersion < 9.0:
        return

    print(f'ERROR: Incompatible Tcl/Tk version: {TkVersion}')
    nvDarkPlugin = f'{pluginDir}/nv_dark.py'

    # Uninstall nv_dark, if any.
    if os.path.isfile(nvDarkPlugin):
        print('Uninstalling the nv_dark plugin ...')
        os.remove(nvDarkPlugin)
        restore_default_colors()

    print('\nInstallation cancelled.')
    input('Press ENTER to quit.')
    sys.exit()


def handle_incompatible_plugins(pluginDir):
    # Uninstall nv_themes, if any.
    nvThemesPlugin = f'{pluginDir}/nv_themes.py'
    if os.path.isfile(nvThemesPlugin):
        if not messagebox.askokcancel(
                'Incompatible plugin detected',
                'The "nv_themes" plugin will now be uninstalled.'
        ):
            sys.exit()

        os.remove(nvThemesPlugin)


def install(zipped):
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    print(f'*** Installing {PLUGIN} {VERSION} ***\n')
    homePath = str(Path.home()).replace('\\', '/')
    applicationDir = f'{homePath}/.novx'
    if os.path.isdir(applicationDir):
        shutil.rmtree(
            f'{applicationDir}/{THEME_DIR}/{THEME_PACKAGE}',
            ignore_errors=True
        )
        pluginDir = f'{applicationDir}/plugin'
        handle_wrong_tk_version(pluginDir)
        handle_incompatible_plugins(pluginDir)
        os.makedirs(pluginDir, exist_ok=True)

        # Install the plugin.
        print(f'Copying "{PLUGIN}" ...')
        copy_file(PLUGIN, pluginDir)

        # Install the themes.
        print('Installing the theme ...')
        copy_tree(THEME_DIR, applicationDir)

        # Install utility.
        copy_file('restore_default_colors.py', applicationDir)

        # Set up the dark mode colors
        set_colors(f'{applicationDir}/config/novx.ini')

        # Show a success message.
        print(
            f'\nSucessfully installed {PLUGIN} '
            f'at "{os.path.normpath(pluginDir)}".'
        )
    else:
        print(
            'ERROR: Cannot find a novelibre installation '
            f'at "{os.path.normpath(applicationDir)}".'
        )

    input('Press ENTER to quit.')


def main(zipped=True):
    try:
        install(zipped)
    except Exception as ex:
        print(str(ex))
        input('Press ENTER to quit.')

