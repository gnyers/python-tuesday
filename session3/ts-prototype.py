#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Demonstration of working with spreadsheets

1. Worksheet management of a given spreadsheet:

   1. list the sheets
      CLI args: --list-sheets WORKBOOK
   2. add sheet
      CLI args: --addsheet SHEETNAME WORKBOOK

2. Data management:

   1. dump the data on a sheet to the stdout or a given output file as text
      CLI args: --dump SHEETNAME WORKBOOK
   2. append provided CSV data at the end of a sheet
      CLI args: --append CSVRECORD --sheet SHEETNAME WORKBOOK

3. CLI Interface: as described above
'''

### Import modules
import sys
import os.path

### Constants

HEADER_ROW = 5                         # sheet headers are assumed in this row

### Function(s) for CLI arg. parsing

def parseargs(cmdline=sys.argv[1:], known_args_only=False):
    pass

### Functions implementing requirements

def list_sheets(workbook):
    ''' List the sheets in *workbok*
    '''
    pass

def add_sheet(workbook, name, index=0):
    ''' Create new sheet with *name* in *workbook* at position *index*
    '''
    pass

def append_data(sheet, data):
    ''' Append *data* after the last record in sheet
    '''
    pass

def dump_data(sheet, fd=sys.stdout):
    ''' Dump all data of *sheet* to file-descriptor *fd*
    '''
    pass

### main starts here
if __name__ == '__main__':
    args = parseargs()


