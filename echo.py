#!/usr/bin/env python
'''A simple program to echo back all its CLI arguments
'''

import sys
answer = ' '.join(sys.argv[1:])
answer = answer.title()
print(answer)
