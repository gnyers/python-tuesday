#!/usr/bin/env python3

import configparser

cfg = configparser.ConfigParser()
cfg.optionxform = str               # make sure to preserve case!

# add the DEFAULT section
cfg['DEFAULT'] = {'ServerAliveInterval': 45,
                  'Compression': 'yes',
                  'CompressionLevel': 9,
                  'ForwardX11': 'yes'}

# add a new section
cfg['bitbucket.org'] = {}
cfg['bitbucket.org']['User'] = 'hg'

# another new section
cfg['topsecret.server.com'] = {}
topsecret = cfg['topsecret.server.com']
topsecret['Port'] = '50022'
topsecret['ForwardX11'] = 'no'

with open('servers.ini', 'wt') as fh:
   cfg.write(fh)