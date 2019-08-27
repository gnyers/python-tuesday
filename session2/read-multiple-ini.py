#!/usr/bin/env pythone

import configparser
ini = configparser.ConfigParser()
ini.optionxform = str               # make sure to preserve case!
files_read = ini.read(['servers.ini', 'user.ini'])
cfg = { section:dict(ini[section])
        for section in ini.sections() + ['DEFAULT'] }
print(cfg)