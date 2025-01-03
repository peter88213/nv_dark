"""Custom theme plugin for novelibre.

Applies the 'awdark' theme, if available. 

Installation: 

- Copy this file into the 'plugin' subdirectory of your novelibre installation folder 
  (e.g. ~/.novx/novelibre).
- Download the zipped tcl-awthemes package from https://sourceforge.net/projects/tcl-awthemes/
- Unpack the awthemes<version> folder and remove the version from the folder's name.
- Make sure there's a 'themes' subdirectory in your novelibre installation folder. 
- Put the 'awthemes' folder into the 'themes' directory.

The installation routine changes colors; this will take effect after a novelibre restart.
To restore the default colors after having uninstalled the plugin, close novelibre,
and delete the novx.ini file in the novelibre/config directory.

Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_dark
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path
from tkinter import messagebox


class Plugin:
    VERSION = '0.2.0'
    API_VERSION = '5.4'
    DESCRIPTION = 'Applies the tcl awdark theme, if available'
    URL = 'https://github.com/peter88213/nv_dark'

    THEME_DIR = '.novx/themes'
    THEME_PACKAGE = 'awthemes'
    THEME = 'awdark'
    COLORS = dict(
        color_1st_edit='DarkGoldenrod2',
        color_2nd_edit='DarkGoldenrod3',
        color_arc='plum',
        color_before_schedule='sea green',
        color_behind_schedule='tomato',
        color_chapter='chartreuse',
        color_comment_tag='wheat4',
        color_done='DarkGoldenrod4',
        color_draft='white',
        color_locked_bg='dim gray',
        color_locked_fg='light gray',
        color_major='SteelBlue1',
        color_minor='SteelBlue',
        color_modified_bg='goldenrod1',
        color_modified_fg='maroon',
        color_notes_bg='wheat4',
        color_notes_fg='white',
        color_on_schedule='white',
        color_outline='orchid2',
        color_stage='tomato',
        color_text_bg='#33393b',
        color_text_fg='light grey',
        color_unused='gray',)

    def install(self, model, view, controller):
        """Install and apply the 'awdark' theme."""
        self._ui = view
        self._ctrl = controller

        # Load custom theme. Exceptions are caught by the application.
        homeDir = str(Path.home()).replace('\\', '/')
        themePath = f'{homeDir}/{self.THEME_DIR}'
        self._ui.root.tk.call('lappend', 'auto_path', f'{themePath}/{self.THEME_PACKAGE}')
        self._ui.root.tk.call('package', 'require', self.THEME)
        self._ui.guiStyle.theme_use(self.THEME)

        # Adjust the colors. This will take effect after restart.
        # Note: The changes wil be stored in the novx.ini file
        #       in the novelibre/config directory.
        #       To restore the default colors, you will have to close novelibre
        #       and delete novx.ini.
        prefs = self._ctrl.get_preferences()
        colorsChanged = False
        for color in self.COLORS:
            if prefs[color] != self.COLORS[color]:
                prefs[color] = self.COLORS[color]
                colorsChanged = True
        if colorsChanged:
            messagebox.showinfo('Dark theme installer', 'Please restart novelibre now to apply changed colors.')

