# this file: j2_02.py

'''Render a Jinja2 template based on data

Usage:
        python3 j2_02.py TEMPLATEFILE DATAFILE

Where:
TEMPLATEFILE: path to the text file containing a valid Jinja2 teamplte
DATAFILE    : path to a JSON file containing the data
'''

import json
import sys
import jinja2 as j2     # load Jinja2 module, refer to its content as "j2.*"

TEMPLATE = open(sys.argv[1]).read()    # load template from file given as
                                       # 1st CLI argument
TEMPLATE = TEMPLATE.strip()            # remove newlines from begin and end

DATA = json.load(open(sys.argv[2]))    # load data from file given as
                                       # 2nd CLI argument

j2_tmpl = j2.Template(TEMPLATE)        # new Jinja2 template instance
out = j2_tmpl.render(**DATA)           # pass unpacked data (assuming dict)
print(out)
