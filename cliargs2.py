#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
p = argparse.ArgumentParser()
p.add_argument('-n', '--name',
               type=str,
               required=False,
               default='John Doe',
               help='Your name')
p.add_argument('-a', '--age',
               type=int,
               required=False,
               default=99,
               help='Your age')
args = p.parse_args()
print('Name:', args.name)
print('Age :', args.age)