#!/usr/bin/env python3
names = 'Hayley Peter Barney Stan Brian Lois Marge Stewie Francine Wilma'

fh = open('names.txt', 'wt')        # create empty file with name "names.txt"
names_l = names.split()             # split long ``str`` into a ``list``
for name in names_l:                # loop through the list of names
    fh.write(name + '\n')           # write current name + '\n' (new line)
fh.close()                          # close file