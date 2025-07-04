#!/usr/bin/python3
"""Restore the novelibre default colors.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_dark
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

print(
    (
        'Restoring novelibre default colors. '
        'Please make sure that novelibre is not running.'
    )
)
homePath = str(Path.home()).replace('\\', '/')
configFile = f'{homePath}/.novx/config/novx.ini'

with open(configFile, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')
newlines = []
for line in lines:
    if line.startswith('color_'):
        print(f'Restoring {line.split(" = ")[0]}')
    else:
        newlines.append(line)
with open(configFile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(newlines))
print('Default colors successfully restored.')

