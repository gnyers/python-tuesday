#!/usr/bin/env python3

'''Simple logging demo for the `profiler` program
'''

import sys
import logging

# Define the message format
# see: https://docs.python.org/3/library/logging.html#logrecord-attributes
#
msgfmt = '%(asctime)s %(levelname)s '       # timestamp level
msgfmt += '(%(module)s:%(lineno)d) '        # module:line nr. where msg created
msgfmt += '%(message)s'                     # actual log message

logging.basicConfig(
          # filename='logging-demo.log',    # uncomment to log msgs to this file
          format=msgfmt,                    # message template
          level=logging.WARNING,            # suppress msgs below WARNING
          datefmt='%Y-%m-%dT%H:%M:%S%Z'     # e.g.: 2022-09-27T19:00:00CEST
          )

logging.debug('This is a DEBUG level message')
logging.info('This is an INFO level message')
logging.warning('This is an WARNING level message')
logging.error('This is an ERROR level message')
logging.critical('This is a CRITICAL level message')
