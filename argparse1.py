#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
p = argparse.ArgumentParser()
p.add_argument('-n', '--name',
               type=int,
               required=False,
               default=0,
               help='An integer number')
args = p.parse_args()
