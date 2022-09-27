#!/bin/bash

mkdir    exampledir
mkdir -p exampledir/a/b/d
mkdir -p exampledir/c/e

# Normal files
for FILE in \
      exampledir/file1.dat \
      exampledir/a/file5 \
      exampledir/a/b/file3 \
      exampledir/c/file13 \
	    exampledir/a/b/d/file8
do
cat <<EOF > $FILE
normal file: ${FILE}

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lobortis
cursus mi, quis sagittis mi venenatis et. Vivamus tortor nisl, blandit.
EOF

done

# Hard links
ln    exampledir/file1.dat exampledir/c/e/file15
ln    exampledir/file1.dat exampledir/a/file2.bin

# Symbolic link
ln -s ../../../c/file13 exampledir/a/b/d/file9

