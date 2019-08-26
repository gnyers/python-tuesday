=========================
Python Tuesday: Session 2
=========================

-----------------------------------
Working with files and file formats
-----------------------------------

:date: 2019-08-27
:author: Gábor Nyers
:tags: python
:category: python_workshop
:summary: A demonstration of reading and writing information to files in
          different formats
:licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/

.. sectnum::
   :start: 1
   :suffix: .
   :depth: 2

**Agenda**

.. contents::
   :depth: 2
   :backlinks: entry
   :local:

**Prep**

- Get Material:
  URL: https://github.com/gnyers/python-tuesday/session2

  .. code:: shell

     git clone git@github.com:gnyers/python-tuesday.git


The fundametals: writing to and reading from files
==================================================

First: Open the file
--------------------

Before being able to access any file Python needs to open it.

#. The absolute minimum:

   (Example as executed in an interactive Python session or Python REPL)

   .. code:: python

      >>> # open the file 'names.txt' for reading, assume a text file
      >>> fh = open('names.txt')
      >>>

   What this means:

   - ``fh``: will be the variable pointing to a new *file handler* object which
     is the result of the ``open()`` function
   - ``open()``: function will create a new file handler object to the
     ``names.txt`` file
   - (allow read-only access to the file, because of missing second optional
     *mode* argument)

#. Open a file for writing only, for example to write some data to a new file:

   .. code:: python

      >>> # open the file 'names.txt' for writing
      >>> fh = open('names.txt', 'wt')
      >>>

   The above instruction will perform the same as above, except for the
   following:

   - ``"wt"``: an optional argument for the ``open()`` function called the
     *mode* string. This is a series of letter codes each with its specific
     meaning as to how Python should request access to the file.

      - ``"w"`` request write-only access, create the file or truncate its
        content, if it already exists
      - ``"t"`` interpret the file's content as Unicode text

     See also: [pydoc_open]_) for other letters and their meaning

#. The *mode* string governs **how** the file is accessed:

   Depending on the use-case we may want to access a file in many different
   ways:

   #. Load a configuration file: read-only, read once, content as text
   #. Export a CSV file: write-only, write once, content as text
   #. Read a picture from a PNG file: read-only, read once, binary content
   #. Append a new record to a log file: write-only, append to the end of
      a file (without overwriting the rest!), content as text
   #. Modify 3 records in a big database file: read and write multiple times,
      seek to a different positions within the file, binary content

Be careful when opening a file for writing!
-------------------------------------------

#. The dangers of the ``"w"`` or ``"w+"`` mode:

   The letter codes ``"w"`` and ``"w+"`` in the ``open()`` functions *mode*
   string will both instruct Python to truncate an existing file. That is: all
   existing content will be lost and may be only be recovered from an existing
   backup.

#. Depending on your use case it may be safer to use the ``"x"`` (or its
   variant ``"x+"``) letter code instead. In this case, if the given file
   exists, Python will throw an exception:

   .. code:: python
      :number-lines: 1

      >>> fh = open('names.txt', 'xt')
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      FileExistsError: [Errno 17] File exists: 'names.txt'
      >>>

   This *mode* is the only safe way to handle files


Create a new file with a list of names
--------------------------------------

Suppose we have the following list of names and want to write them to a file
one name per line:

   Hayley Peter Chris Stan Brian Lois Marge Stewie Francine Meg

.. code:: python
   :number-lines: 1
   :name: write-names-as-txt.py

   #!/usr/bin/env python3
   names = 'Hayley Peter Barney Stan Brian Lois Marge Stewie Francine Wilma'

   fh = open('names.txt', 'wt')        # create empty file with name "names.txt"
   names_l = names.split()             # split long ``str`` into a ``list``
   for name in names_l:                # loop through the list of names
       fh.write(name + '\n')           # write current name + '\n' (new line)
   fh.close()                          # close file

So, what has happened here:

- **line 1**: special "Shebang_" line, instructing the OS what interpreter to
  execute this file with
- **line 2**: create a new ``str`` object containing the names and bind the
  ``names`` variable to it
- **line 4**: (re-)create new empty file with the name "names.txt"
  (Remember: an existing file's data will be deleted!)
- **line 5**: split-up the long ``str`` object into multiple shorter ``str``
  and gather them into a new ``list`` object.
  Because the ``.split()`` method didn't received an argument, by default the
  splitting will occur at the any of the following characters: ' ' (space),
  '\t' (tab) and '\n' (new line)
- **line 6**: loop through the elements of the ``names_l`` list object one
  element  at a time. In each iteration the current element is bound to
  the ``name`` variable
- **line 7**: in each iteration write a ``str`` containing the current name
  and a ``"\n"`` (new line) character to the file represented by the ``fh``
  *file handler* object; in our case the ``names.txt`` file.

  This line will be executed for each element of the ``names_l`` list, i.e.:
  10 times.
- **line 8**: close the file


.. _Shebang: https://en.wikipedia.org/wiki/Shebang_(Unix)


Read the file with the names
----------------------------

Now that we have created the ``names.txt`` file let's read the data. We have
more than one way to do this:

#. The simplest way to read the content of the file is to read the whole
   content into memory, such as:

   .. code:: python

      >>> fh = open('names.txt')
      >>> content = fh.read()
      >>> type(content)
      <class 'str'>
      >>> content
      'Hayley\nPeter\nBarney\nStan\nBrian\nLois\nMarge\nStewie\nFrancine\nWilma\n'

   The file's content is now in a ``str`` object, which when printed produces
   to following output:

   .. code:: python

      >>> print(content)
      Hayley
      Peter
      Barney
      Stan
      Brian
      Lois
      Marge
      Stewie
      Francine
      Wilma
      >>> fh.close()

#. More often than not we want to read text files line-by-line:

   .. code:: python

      >>> fh = open('names.txt')
      >>> for line in fh:
      ...     print(line)              # doctest: +ELLIPSIS
      Hayley

      Peter

      Barney

      Stan

   Please note the double spaced output! This is the consequence of the
   default behaviors. On the one hand when reading a line, the *file handler*
   leaves the ``"\n"`` (new line) character intact at the end of the line.
   Verify this by typing the ``line`` variable, which still contains the
   last line:

   .. code:: python

      >>> line
      'Wilma\n'
      >>> fh.close()                   # close the file

   Additionally, the ``print()`` function automatically prints a ``"\n"``
   character, resulting in double spaced printout.

   The following is a solution, where the ``end=''`` argument instructs the
   ``print()`` function to print an empty ``str`` at the end of the line:

   .. code:: python

      >>> fh = open('names.txt')
      >>> for line in fh:
      ...     print(line, end='')
      ... 
      Hayley
      Peter
      Barney
      Stan
      Brian
      Lois
      Marge
      Stewie
      Francine
      Wilma

In addition to (or in place of) the above interactive commands, we can collect
these instructions into a Python program file:

.. code:: python
   :number-lines: 1
   :name: read-names-from-txt.py

   #!/usr/bin/env python3

   fh = open('names.txt')
   for line in fh:
       print(line, end='')

The program may be executed directly from your IDE or by entering the
following in a terminal:

.. code:: shell

   python3 read-names-from-txt.py


A word about Unicode and encoding
---------------------------------

The encoding of text files becomes a concern once we want to read and write
text files  with non-ASCII characters, i.e.: letters and symbols which are not
used in the English writing system. (see [ASCII1967]_). Here are a few
examples:

- international characters: Français, Español, Português, Plattdüütsch,
  ελληνική, Русский, שפה עברית, հայոց լեզու, 普通話
- emoticons: ☺(grinning face) ☹(sad face)
- and symbols: ❄(snowflake) ✌(V sign) €(euro sign) ⚕(medicine) ☮(peace sign)

The multitude (dozens!) of character pages and encoding standards used to make
working with -- and especially exchanging -- textual data outside English
speaking countries a daunting challenge. The solution has been gradually
implemented came about in de first decade of the '00s with the widespread
adoption of the Unicode standard (see [Unicode2001]_).

In Python 3 the built-in ``str`` datatype (and a few others) has been
re-implemented and strings are now 100% handled as [Unicode2001]_. Data
interchange -- i.e.: reading and writing text data -- now typically works to
a degree that users hardly notice it's there.

**Important takeaway:**

When exchanging textual data, such as reading from or writing to a file,
as a programmer you need to indicate to Python that it should handle the
data as text. This requires a few additional steps before writing or after
reading, which Python will take care of automatically, such as: 

- encoding, i.e.: converting from the ``str`` datatype to raw data and
- decoding, i.e.: converting from raw binary data to the ``str`` type

In our earlier examples we did this using the ``"t"`` letter code in the
``open()`` function.

Summary
-------

At this point we have covered the fundamental of reading and writing text
files. The rest of the session we will spend on the most popular formats which
are used to store data in text files.


Working with CSV files
======================

The *CSV* format (see [CSVformat]_) is a frequently used, application and
platform independent format to exchange tabular data. A typical example:

.. code::
   :number-lines: 1

   name|full_name|group|gendergroup|agegroup
   fred|Fred Flintstone|flintstones|m|adults
   wilma|Wilma Flintstone|flintstones|f|adults
   pebbles|Pebbles Flintstone|flintstones|f|kids

This data represents the following table:

.. csv-table:: Cartoon characters
   :widths: 10, 20, 10, 5, 10
   :header-rows: 1
   :delim: |

   name|full_name|group|gendergroup|agegroup
   fred|Fred Flintstone|flintstones|m|adults
   wilma|Wilma Flintstone|flintstones|f|adults
   pebbles|Pebbles Flintstone|flintstones|f|kids

A few noteworthy points about the above example:

- the first row contains the names of the columns
- the delimiter is the '|' (vertical bar) character
- the data consist of 3 rows and 5 columns
- the strings are not quoted

In Python there are at least a handful of ways and modules to process *CSV*
files. We will focus here on the most obvious one: the "Python Standard
Library's" ``csv`` (see [pydoc_csv]) module.

Create a CSV file
-----------------

Let's take the above example and create a *CSV* file from it.

.. code:: python
   :number-lines: 1
   :name: write-names-as-csv.py

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

The ``csv`` module's "Dialects and Formatting Parameters" section (see
[pydoc_csv_formatting]_) provides more information about additional bells and
whistles when exporting data to *CSV*, e.g.:

- ``quoting``: whether or not to quote strings
- ``escapechar``: how to escape characters in the data, which coincide with
  the ``delimiter`` character
- etc ...

Execute this program by entering:

.. code:: shell

   python3 write-names-as-csv.py

and verify the file it has produced:

.. code:: shell

   cat names.csv

   name|full_name|group|gendergroup|agegroup
   fred|Fred Flintstone|flintstones|m|adults
   wilma|Wilma Flintstone|flintstones|f|adults
   pebbles|Pebbles Flintstone|flintstones|f|kids


Read data from a CSV file
-------------------------

Now that we have an example *CSV* example, we can re-create the Python data
structure from the data:

.. code:: python
   :number-lines: 1
   :name: read-names-from-csv.py

   #!/usr/bin/env python3

   import csv
   with open('names.csv') as fh:
       csv_r = csv.reader(fh, dialect='excel', delimiter='|')
       data = list(csv_r)
   print(data)

The steps:

- **line 3:** load the ``csv`` module
- **line 4:** the ``with`` statement is an improved way of using (amongst
  others) the ``open()`` function, which will automatically close the file
  handler if Python is done with the code block (lines 5 and 6)

  For detailed information on this construct see the [pep343]_ or search for
  the term "python context manager".

- **line 5:** create a new CSV reader object with the specified details about
  the delimiter and CSV dialect
- **line 6:** convert the data represented by the CSV reader to a list object
- **line 7:** print out the data

Working with INI files
======================

TODO

Working with JSON files
=======================

TODO

Working with YAML files
=======================

TODO

Working with XML files
======================

TODO


References
==========

.. [pydoc_open] Documentation of the ``open()`` function
   https://docs.python.org/3/library/functions.html#open

.. [ASCII1967] ASCII codes represent text in computers, telecommunications
   equipment, and other devices. Most modern character-encoding schemes are based
   on ASCII, although they support many additional characters. 
   See: https://en.wikipedia.org/wiki/ASCII

.. [Unicode2001] Unicode is a computing industry standard for the consistent
   encoding, representation, and handling of text expressed in most of the
   world's writing systems.
   https://en.wikipedia.org/wiki/Unicode

.. [CSVformat] A CSV file stores tabular data (numbers and text) in plain
   text. Each line of the file is a data record. Each record consists of one
   or more fields, separated by commas (',') or other delimiter characters,
   such as semicolon (';'), colon (':'), bar ('|'), etc...
   https://en.wikipedia.org/wiki/Comma-separated_values

.. [pydoc_csv] Python Standard Library documentation, CSV module
   https://docs.python.org/3/library/csv.html

.. [pydoc_csv_formatting] ``csv`` module's Dialects and Formatting Parameters
   https://docs.python.org/3/library/csv.html#csv-fmt-params

.. [pep343] PEP 343 -- The "with" Statement
   https://www.python.org/dev/peps/pep-0343/

.. _pydoc open: https://docs.python.org/3/library/functions.html#open
.. _pydoc unicode: https://docs.python.org/3/howto/unicode.html


.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
