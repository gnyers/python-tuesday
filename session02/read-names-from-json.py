#!/usr/bin/env pythone

import json
with open('names.json') as fh:
   names = json.load(fh)
   print(names)