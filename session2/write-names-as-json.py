#!/usr/bin/env python3

import json

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
with open('names.json', 'wt') as fh:
   json.dump(names, fh)