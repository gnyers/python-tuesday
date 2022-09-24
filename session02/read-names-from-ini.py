#!/usr/bin/env pythone

import configparser
ini = configparser.ConfigParser()
ini.optionxform = str               # make sure to preserve case!
files_read = ini.read(['names-case-preserved.ini'])
names = { section:dict(ini[section]) for section in ini.sections() }
print(names)