#!/usr/bin/env python3

import csv

# The CSV data
names='''
name|full_name|group|gendergroup|agegroup
fred|Fred Flintstone|flintstones|m|adults
wilma|Wilma Flintstone|flintstones|f|adults
pebbles|Pebbles Flintstone|flintstones|f|kids
'''

# convert the ``names`` str to a list of lists
data = names.strip()           # remove white-space chars from both ends
data = data.split('\n')        # split ``str`` into lines, returns a ``list``
data = [ line.split('|') for line in data ]  # split all rows into its fields

# the ``data`` variable now points to a list object, each of whose element
# is a list:
# data = [
#   ['name', 'full_name', 'group', 'gendergroup', 'agegroup'],
#   ['fred', 'Fred Flintstone', 'flintstones', 'm', 'adults'],
#   ['wilma', 'Wilma Flintstone', 'flintstones', 'f', 'adults'],
#   ['pebbles', 'Pebbles Flintstone', 'flintstones', 'f', 'kids']
# ]

# Now let's write this out to the file ``names.csv``
with open('names.csv', 'wt') as fh:
   csv_w = csv.writer(fh, dialect='excel', delimiter='|')
   csv_w.writerows(data)