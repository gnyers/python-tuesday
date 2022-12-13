#!/usr/bin/env python3

'''Jinja2 pre-processor

Render a Jinja2 template using data provided in a JSON, YAML or CSV file and
in the CLI arguments.
'''

__author__ = 'Gábor Nyers'
__version__ = '0.1.0'
__license__ = 'CC BY-NC 4.0'

# imports of modules in Standard Library
import json
import os
import pathlib
import sys
from datetime import datetime
from pprint import pprint
# imports of 3rd-party modules
import yaml
import jinja2 as j2     # load Jinja2 module, refer to its content as "j2.*"


def parseargs(cmdline=sys.argv[1:].copy(),       # for safety use a copy of argv
              description=__doc__,               # module docstring as help text
              epilog=''):
    '''Parse CLI arguments
    '''
    import argparse

    def paramlist(param):
        'Return a list of 2 elements, split on "="'
        ret = [p.strip() for p in param.split('=', 1)]
        if len(ret) != 2:
            msg = f'\n\tNeed "name=value" pair, got: "{param}"'
            raise argparse.ArgumentTypeError(msg)
        return ret

    p = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    p.add_argument('-D', '--debug',
                   action='store_true',
                   help='Dump the data that would be passed to '
                   'the template')
    p.add_argument('-d', '--data-file',
                   type=pathlib.Path,
                   default=None,
                   help='file containing the data, '
                   'will be passed to template as variable "data"')
    p.add_argument('-p', '--params',
                   metavar='name=value',
                   type=paramlist,
                   nargs='*',
                   help='additional parameters, will be passed to '
                   'template as variable "params", in the form of a dict')
    template_dirs_def = os.environ.get('J2PP_PATH', '.').split(':')
    p.add_argument('-T', '--template-dirs',
                   type=pathlib.Path,
                   nargs='+',
                   default=template_dirs_def,
                   help='Template directories (default: the value of env. '
                   f'variable "J2PP_PATH" or "."; now: {template_dirs_def})')
    p.add_argument('-o', '--output',
                   type=pathlib.Path,
                   default=sys.stdout,
                   help='Write the output to this file (default: STDOUT)')
    p.add_argument('template',
                   type=pathlib.Path,
                   nargs='?',
                   default=sys.stdin,
                   help='Template file (default: STDIN)')

    args = p.parse_args(cmdline)                 # parse all args!
    if args.params:                              # if provided,
        args.params = dict(args.params)          # convert params to dict
    return args


def load_data_json(data_file):
    'Load JSON data'
    data = json.loads(data_file.read_text())      # load json file content
    return data


def load_data_yaml(data_file):
    'Load YAML data'
    data = yaml.load(data_file.read_text(),       # load json file content
                     Loader=yaml.SafeLoader)
    return data


def load_data_csv(data_file, delimiter=','):
    'Load CSV data'
    import csv
    data_i = csv.DictReader(open(data_file),
                            delimiter=delimiter)
    data = [dict(row) for row in data_i]          # convert csv data to list
    return {'csv': data}                          # need data as dict


def load_data(data_file, **kwargs):
    '''Load the data from `data_file`
    '''
    # a dispath dict is much more elegant than  a lengthy if-elif-else
    # construct
    loaders = {
        # 'extension': 'loader' function
        '.json': load_data_json,
        '.yaml': load_data_yaml,
        '.yml': load_data_yaml,
        '.csv': load_data_csv,
    }
    try:
        # get the loader function based on the data_file's extension
        loader = loaders.get(data_file.suffix,
                             load_data_json)     # default loader, if no match

        # execute loader function with the data_file, also pass on any
        # additional keyword arguments, e.g.: "delimiter" for the CSV format
        data = loader(data_file=data_file, **kwargs)
    except Exception as e:
        print(e, file=sys.stderr)
        print(f'File "{data_file}" could not be loaded', file=sys.stderr)
        sys.exit(10)
    return data


def render_template(*, template, template_dirs, **data):
    '''Render Jinja2 template based on passed data
    '''
    try:
        if isinstance(template, pathlib.Path):  # if Path obj.
            template = template.open()          # create file descriptor of it

        tmpl = j2.Template(template.read(),     # template as str
                           undefined=j2.StrictUndefined)   # fail if template
                                                # variable names are undefined
        loader = j2.FileSystemLoader(template_dirs)
        tmpl.environment.loader = loader

        out = tmpl.render(                      # pass variables to template
            template=template,                  # - template value
            template_dirs=template_dirs,        # - template_dirs value
            **data,                             # - all other provided data
        )
    except j2.exceptions.TemplateError as e:
        msg = '*** Template ERROR:'
        print(msg, e, file=sys.stderr)          # print error message
        sys.exit(10)                            # exit program w/ code
    except Exception as e:
        msg = '*** ERROR:'
        print(msg, e, file=sys.stderr)          # print error message
        sys.exit(20)                            # exit program w/ code

    return out


def main():
    '''Immediate code if module is run directly, instead of being imported
    '''
    args = parseargs()                      # parse CLI arguments

    if args.data_file:                      # if provided, load data from file
        data = load_data(data_file=args.data_file)
    else:
        data = {}                           # or set it to empty dict

    all_data = dict(                        # data to pass to template:
        now=datetime.now(),                 # - current timestamp
        data=data,                          # - all data from data-file
        **args.__dict__,                    # - all CLI args to template
    )
    if data:                                # if provided, add the unpacked
        all_data.update(**data)             # data from the --data file

    if args.params:                         # if provided, add the data from
        all_data.update(**args.params)      # the CLI --param options

    if args.debug:                          # handle the --debug CLI param
        pprint(all_data)                    # dump all data as it would be
        sys.exit(0)                         # passed to template and exit.

    out = render_template(**all_data)       # render the template

    if isinstance(args.output, pathlib.Path):
        fh = open(args.output, 'w')         # open output file for writing
    else:
        fh = args.output                    # stdout, i.e.: a file handler

    fh.write(out)                           # write generated content to file

    return 0                                # main successfull exit code 0


if __name__ == '__main__':
    sys.exit(main())
