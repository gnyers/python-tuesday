#!/usr/bin/env python3

import configparser

names = {
          'kids': {
                    'Chris': 'Family Guy',
                    'Pebbles': 'The Flintstones',
                    'Bart': 'The Simpsons'
                  },
          'adults': {
                      'Fred': 'The Flintstones',
                      'Betty': 'The Flintstones',
                      'Homer': 'The Simpsons',
                      'Lois': 'Family Guy'
                    },
          'other': { 'Klaus': 'American Dad',
                     'Brian': 'Family Guy',
                     'Roger': 'American Dad'
                   }
        }
ini = configparser.ConfigParser()
ini.optionxform = str               # make sure to preserve case!
ini.update(names)
with open('names-case-preserved.ini', 'wt') as fh:
   ini.write(fh)