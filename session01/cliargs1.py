#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
p = argparse.ArgumentParser()
p.add_argument('-n', '--name',
               type=str,
               required=False,
               default='John Doe',
               help='Your name')
args = p.parse_args()