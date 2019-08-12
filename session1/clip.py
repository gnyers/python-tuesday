#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clipboard

# Put a string on the clipboard
clipboard.copy('Beautiful is better than ugly.')

print('Retrieve the content of the clipboard:\n', clipboard.paste())