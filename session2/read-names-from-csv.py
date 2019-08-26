#!/usr/bin/env python3

import csv
with open('names.csv') as fh:
    csv_r = csv.reader(fh, dialect='excel', delimiter='|')
    data = list(csv_r)
print(data)