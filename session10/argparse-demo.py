#!/usr/bin/env python3

'''Simple argparse demo for the `profiler` program
'''

import argparse
import sys
from os.path import isdir

def valid_dir(dirname):
    ''' a validator function for directory names

    returns: `dirname` if directory exists and is indeed a directory
    raises: argparse.ArgumentTypeError dirname
    '''
    if isdir(dirname):                     # is dirname a valid directory?
        return dirname                     # return dirname as is
    else:                                  # do not accept an invalid dir
        raise argparse.ArgumentTypeError(f'{dirname} is not a directory')

def parseargs(cmdline=sys.argv[1:],        # parse either CLI args or a string
              known_args_only=False,       # fail if unknown args?
              description=__doc__,         # --help begins with the docstring
              epilog="That's all folks!"   # --help ends with this string
    ):
    ''' CLI argument parser
    '''

    p = argparse.ArgumentParser(           # get an ArgumentParser instance
          formatter_class=argparse.RawTextHelpFormatter,
          description=description,
          epilog=epilog
    )

    p.add_argument('dirname',              # name of this argument
                   metavar='DIR',          # --help will show this as arg name
                   type=valid_dir,         # validator function
                   help='path to directory to analyze')  # purpose of this arg
    if known_args_only:
        return p.parse_known_args(cmdline)[0] # want only known args
    else:
        return p.parse_args(cmdline)       # parse all args!

args = parseargs()                         # begin of the prg, lets parse args!

# **NOTE**: the received CLI arguments will be available through the whole
# program. To access any values refer to the appropriate attribute of the
# `args` object, e.g.: `args.dirname`

# Show the received info:
print(f'''
Received directory name from CLI arguments: {args.dirname}

''')

# The rest of the program's code goes here;

