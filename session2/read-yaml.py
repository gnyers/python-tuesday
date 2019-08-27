#!/usr/bin/env pythone

import sys
import yaml
import pprint as pp

try:
   fh = open(sys.argv[1])
   data = yaml.load(fh)
except IndexError:
   print('I need an argument: YAML file name')
   sys.exit(1)
except FileNotFoundError:
   print('File "{}" is not found!'.format(sys.argv[1]))
   sys.exit(2)
except yaml.parser.ParserError:
   msg = 'The file {} does not appear to be a valid YAML file!'
   print(msg.format(sys.argv[1]))
pp.pprint(data)