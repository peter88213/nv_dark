"""Custom theme plugin for novelibre.

Applies the 'awdark' theme, if available. 

Requires Python 3.7+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_dark
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from pathlib import Path
from tkinter import messagebox
import webbrowser

from nvlib.gui.default_colors import DEFAULT_COLORS


class Plugin:
    VERSION = '@release'
    API_VERSION = '5.45'
    DESCRIPTION = 'Applies the tcl awdark theme, if available'
    URL = 'https://github.com/peter88213/nv_dark'

    HELP_URL = 'https://peter88213.github.io/nv_dark/help/'

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
        color_highlight='dark slate gray',
        color_inactive_bg='#394341',
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
        color_separator='black',
        color_stage='tomato',
        color_status_error_bg='red',
        color_status_error_fg='white',
        color_status_notification_bg='yellow',
        color_status_notification_fg='black',
        color_status_success_bg='green',
        color_status_success_fg='white',
        color_text_bg='#33393b',
        color_text_fg='light gray',
        color_unused='gray',
        color_xml_tag='cornflower blue',
    )

    def install(self, model, view, controller):
        """Install and apply the 'awdark' theme."""
        THEME_DIR = '.novx/themes'
        THEME_PACKAGE = 'awthemes'
        THEME = 'awdark'
        self._ui = view
        self._ctrl = controller

        # Load custom theme. Exceptions are caught by the application.
        homeDir = str(Path.home()).replace('\\', '/')
        themePath = f'{homeDir}/{THEME_DIR}'
        self._ui.root.tk.call(
            'lappend',
            'auto_path',
            f'{themePath}/{THEME_PACKAGE}',
        )
        self._ui.root.tk.call('package', 'require', THEME)
        self._ui.guiStyle.theme_use(THEME)

        # If the setup script has not already done so, adjust the colors.
        prefs = self._ctrl.get_preferences()
        colorsChanged = False
        for color in self.COLORS:
            if prefs[color] != self.COLORS[color]:
                prefs[color] = self.COLORS[color]
                colorsChanged = True
        if colorsChanged:
            messagebox.showinfo(
                'Dark theme installer',
                'Please restart novelibre now to apply changed colors.'
            )

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(
            label='nv_dark Online help',
            command=self.open_help,
        )

    def open_help(self):
        webbrowser.open(self.HELP_URL)

    def uninstall(self):
        """Reset the preferences to default colors."""
        prefs = self._ctrl.get_preferences()
        for color in DEFAULT_COLORS:
            prefs[color] = DEFAULT_COLORS[color]
