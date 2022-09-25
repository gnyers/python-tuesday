=========================
Python Tuesday: Session 2
=========================

----------------------------------------
Working with text files and file formats
----------------------------------------

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

   .. code:: pycon

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

   .. code:: pycon

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

   .. code:: pycon
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

   .. code:: pycon

      >>> fh = open('names.txt')
      >>> content = fh.read()
      >>> type(content)
      <class 'str'>
      >>> content
      'Hayley\nPeter\nBarney\nStan\nBrian\nLois\nMarge\nStewie\nFrancine\nWilma\n'

   The file's content is now in a ``str`` object, which when printed produces
   to following output:

   .. code:: pycon

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

   .. code:: pycon

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

   .. code:: pycon

      >>> line
      'Wilma\n'
      >>> fh.close()                   # close the file

   Additionally, the ``print()`` function automatically prints a ``"\n"``
   character, resulting in double spaced printout.

   The following is a solution, where the ``end=''`` argument instructs the
   ``print()`` function to print an empty ``str`` at the end of the line:

   .. code:: pycon

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
Library's" ``csv`` (see [pydoc_csv]_) module.

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


Read data from a CSV files
--------------------------

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

The *INI* format (see [INI_format]_) is capable of representing information
organized in a tree structure, which lends itself well for its main use case:
configuration files. Besides that the *INI* format can also be used for data
exchange.

Similarly to the *CSV* format despite of lacking an official standard, it has
been in use for decades and as a result has a multitude of (slightly
inconsistent) implementations.

In terms of the format's details, the content is divided into sections, which
in turn is a listing of properties and their associated values.

Python has an implementation in the "Python Standard Library" in the module
``configparser`` (see [pydoc_configparser]_).

In Python terminology, while the *CSV* format is well-suited for storing
``list``-like data, the *INI* format is a good choice for storing
``dict``-like data.

In this section we will be working with the data represented by the following
``dict`` object:

   .. code:: python

      names = {
                'kids': {
                          'Chris': 'Family Guy',
                          'Pebbles': 'The Flintstones',
                          'Bart': 'The Simpsons'
                        },
                'adults': {
                            'Fred': 'The Flintstones',
                            'Betty': 'The Flintstones',
                            'Homer': 'The Simpsons',
                            'Lois': 'Family Guy'
                          },
                'other': { 'Klaus': 'American Dad',
                           'Brian': 'Family Guy',
                           'Roger': 'American Dad'
                         }
              }

Writing data to INI file
------------------------

The following is one of the simplest solution to export to an INI file:

.. code:: python
   :number-lines: 1
   :name: write-names-as-ini.py

   #!/usr/bin/env python3

   import configparser

   names = {
             'kids': {
                       'Chris': 'Family Guy',
                       'Pebbles': 'The Flintstones',
                       'Bart': 'The Simpsons'
                     },
             'adults': {
                         'Fred': 'The Flintstones',
                         'Betty': 'The Flintstones',
                         'Homer': 'The Simpsons',
                         'Lois': 'Family Guy'
                       },
             'other': { 'Klaus': 'American Dad',
                        'Brian': 'Family Guy',
                        'Roger': 'American Dad'
                      }
           }
   ini = configparser.ConfigParser()
   ini.update(names)
   with open('names.ini', 'wt') as fh:
      ini.write(fh)

When executing this example, it creates the ``names.ini`` file with  the
following content:

.. code-block:: ini

   [kids]
   chris = Family Guy
   pebbles = The Flintstones
   bart = The Simpsons

   [adults]
   fred = The Flintstones
   betty = The Flintstones
   homer = The Simpsons
   lois = Family Guy

   [other]
   klaus = American Dad
   brian = Family Guy
   roger = American Dad

Note the lower-case key names (e.g.: 'chris', 'pebbles' etc...). This is the
default behavior of the ``ConfigParser`` class, since the original
implementation of the ``configparser`` module tried to adhere the *INI* format
used on Windows. Windows is case-insensitive, hence the class' default
behavior.

With the following slight modification we can preserve the upper-case letters:

.. _cartooncharacters:

.. code:: python
   :number-lines: 1
   :name: write-names-as-ini-preserve-case.py

   #!/usr/bin/env python3

   import configparser

   names = {
             'kids': {
                       'Chris': 'Family Guy',
                       'Pebbles': 'The Flintstones',
                       'Bart': 'The Simpsons'
                     },
             'adults': {
                         'Fred': 'The Flintstones',
                         'Betty': 'The Flintstones',
                         'Homer': 'The Simpsons',
                         'Lois': 'Family Guy'
                       },
             'other': { 'Klaus': 'American Dad',
                        'Brian': 'Family Guy',
                        'Roger': 'American Dad'
                      }
           }
   ini = configparser.ConfigParser()
   ini.optionxform = str               # make sure to preserve case!
   ini.update(names)
   with open('names-case-preserved.ini', 'wt') as fh:
      ini.write(fh)

A few details of this improved version:

- **line 3:** load the ``configparser`` module
- **line 22:** create a new ``ConfigParser`` object
- **line 23:** make sure to preserve upper- and lower-cases in both section-
  and key names!
- **line 24:** copy the data from the ``names`` dictionary object
- **line 25:** open the output file  (as a reminder: see [pep343]_ for more
  information on using context managers)
- **line 26:** write the data to the output file

Reading data from INI files
---------------------------

As usual, we'll try to read in the data from the file we just created.


.. _readinifile:

.. code:: python
   :number-lines: 1
   :name: read-names-from-ini.py

   #!/usr/bin/env pythone

   import configparser
   ini = configparser.ConfigParser()
   ini.optionxform = str               # make sure to preserve case!
   files_read = ini.read(['names-case-preserved.ini'])
   names = { section:dict(ini[section]) for section in ini.sections() }
   print(names)

So let's unpack what has happened here:

- **lines 3, 4 and 5:** load the ``configparser`` module, create a new
  ``ConfigParser`` object and make sure it preserves upper- and lower-case
  letters ; same as in the previous example
- **line 5:** the ``.read()`` method is an interesting one... it is capable of
  reading, parsing and merging multiple *INI* files in one go.

  As its argument we provide a collection (in this case a ``list``) of
  strings, which will be interpreted by the method as file names. The
  ``.read()`` method will try to read and parse them.

  The names of all successfully processed files will be provided as the
  elements of the ``list`` object it returns.

  **Very convenient!**

- **line 6:** this is where we convert the ``ConfigParser`` object to
  a ``dict``. This is not required, since we can access the data in the
  ``ini`` object as well. However for an easy comparison with what we've
  started it is convenient to see the data as a ``dict``

  The conversion is done using a "dictionary comprehension" (see [pep274]_),
  which is a convenient shorthand for a full-blown ``for`` loop.

  To unpack its working we could write the instruction up in a way which
  better indicates the details:

  .. code:: python

     names = {
      section                          # key of the new element is the section name
      :                                # required syntax
      dict(ini[section])               # value is the converted ``Section``
                                       # object to a ``dict``
      for section in ini.sections()    # loop through each section name
     }

- **line 7:** display the data

When we execute this program we see the following:

.. code:: shell

   python3 read-names-from-ini.py

   {'kids': {'Chris': 'Family Guy', 'Pebbles': 'The Flintstones', 'Bart': 'The
   Simpsons'}, 'adults': {'Fred': 'The Flintstones', 'Betty': 'The
   Flintstones', 'Homer': 'The Simpsons', 'Lois': 'Family Guy'}, 'other':
   {'Klaus': 'American Dad', 'Brian': 'Family Guy', 'Roger': 'American Dad'}}

Writing configuration data to INI files
---------------------------------------

Using the *INI* format for configuration data is not significantly different
and most of the differences arise from conventions after decades of use.

Create a new configuration file based on the example at
https://docs.python.org/3/library/configparser.html#quick-start

.. code:: python
   :number-lines: 1
   :name: write-cfg-as-ini.py

   #!/usr/bin/env python3

   import configparser

   cfg = configparser.ConfigParser()
   cfg.optionxform = str               # make sure to preserve case!

   # add the DEFAULT section
   cfg['DEFAULT'] = {'ServerAliveInterval': 45,
                     'Compression': 'yes',
                     'CompressionLevel': 9,
                     'ForwardX11': 'yes'}

   # add a new section
   cfg['bitbucket.org'] = {}
   cfg['bitbucket.org']['User'] = 'hg'

   # another new section
   cfg['topsecret.server.com'] = {}
   topsecret = cfg['topsecret.server.com']
   topsecret['Port'] = '50022'
   topsecret['ForwardX11'] = 'no'

   with open('servers.ini', 'wt') as fh:
      cfg.write(fh)

This creates the following *INI* file:

.. _serversini:

.. code-block:: ini
   :name: servers.ini

   [DEFAULT]
   ServerAliveInterval = 45
   Compression = yes
   CompressionLevel = 9
   ForwardX11 = yes

   [bitbucket.org]
   User = hg

   [topsecret.server.com]
   Port = 50022
   ForwardX11 = no


More advanced use-case: Merging of multiple configuration files
---------------------------------------------------------------

Suppose that for the reason of separating out concerns, we have decided to
split up our configuration information into the following 2 files:

- ``servers.ini`` from the `earlier example <#serversini>`_, containing
  generic server related configuration, and
- ``user.ini`` containing the specific preferences of a user as follows:

.. code-block:: ini
   :name: user.ini

   [DEFAULT]
   ServerAliveInterval = 200
   ForwardX11 = no

   [www.example.com]
   User = jdoe

A slightly modified version of our `earlier *INI* reader example
<#readinifile>`_ will read and merge both the ``servers.ini``

.. code:: python
   :number-lines: 1
   :name: read-multiple-ini.py

   #!/usr/bin/env pythone

   import configparser
   ini = configparser.ConfigParser()
   ini.optionxform = str               # make sure to preserve case!
   files_read = ini.read(['servers.ini', 'user.ini'])
   cfg = { section:dict(ini[section]) 
           for section in ini.sections() + ['DEFAULT'] }
   print(cfg)

This program produces the following output (slightly re-formatted for
readability):

.. code:: shell

   python3 -i read-multiple-ini.py

   {
     'bitbucket.org': {
        'User': 'hg', 'ServerAliveInterval': '200', 'Compression': 'yes',
        'CompressionLevel': '9', 'ForwardX11': 'no'},
     'topsecret.server.com': {
        'Port': '50022', 'ForwardX11': 'no', 'ServerAliveInterval': '200',
        'Compression': 'yes', 'CompressionLevel': '9'},
     'www.example.com': {
        'User': 'jdoe', 'ServerAliveInterval': '200', 'Compression': 'yes',
        'CompressionLevel': '9', 'ForwardX11': 'no'},
     'DEFAULT': {
        'ServerAliveInterval': '200', 'Compression': 'yes',
        'CompressionLevel': '9', 'ForwardX11': 'no'}
   }

Note that some of the entries defined in ``servers.ini`` are overwritten by
the matching entries in ``user.ini`` and there is also a new section:

- changes in the ``[DEFAULT]`` section:

  - value change of ``ServerAliveInterval``: ``45`` -> ``200``
  - value change of ``ForwardX11``: ``yes`` -> ``no``

- new section ``www.example.com``


More advanced use-case: Interpolation of configuration files
------------------------------------------------------------

For more information see the following section of the ``configparser``
module's documentation:

https://docs.python.org/3/library/configparser.html#interpolation-of-values


Working with JSON files
=======================

The *JSON* file format (see [JSON]_) is an ECMA open standard well-suited for
exchanging tree-like data in a human-readable text format. *JSON* is widely
used for storing both configuration information and actual data.


JSON support in Python
----------------------

The "Python Standard Library" provides out-of-the-box *JSON* support in the
``json`` modules.


Writing data to JSON file
-------------------------

Let's take the `cartoon characters data <#cartooncharacters>`_  from the
``names`` dictionary of our earlier example and export it to a *JSON* file:

.. code:: python
   :number-lines: 1
   :name: write-names-as-json.py

   #!/usr/bin/env python3

   import json

   names = {
             'kids': {
                       'Chris': 'Family Guy',
                       'Pebbles': 'The Flintstones',
                       'Bart': 'The Simpsons'
                     },
             'adults': {
                         'Fred': 'The Flintstones',
                         'Betty': 'The Flintstones',
                         'Homer': 'The Simpsons',
                         'Lois': 'Family Guy'
                       },
             'other': { 'Klaus': 'American Dad',
                        'Brian': 'Family Guy',
                        'Roger': 'American Dad'
                      }
           }
   with open('names.json', 'wt') as fh:
      json.dump(names, fh)

Focusing on the new instructions:

- **line 3:** load the ``json`` module
- **line 23:** the ``json.dump()`` takes 2 arguments: the data structure
  (usually as a ``dict``) and a file-handler

The program produces the ``"names.json"`` file with the following content
(re-formatted for readability):

.. code-block:: json
   :name: names.json

   {
     "kids": {
       "Chris": "Family Guy",
       "Pebbles": "The Flintstones",
       "Bart": "The Simpsons"
     },
     "adults": {
       "Fred": "The Flintstones",
       "Betty": "The Flintstones",
       "Homer": "The Simpsons",
       "Lois": "Family Guy"
     },
     "other": {
       "Klaus": "American Dad",
       "Brian": "Family Guy",
       "Roger": "American Dad"
     }
   }

Note the striking similarities in the syntax of the *JSON* format and the
actual Python syntax of dictionaries! Almost exactly the same.

Reading data from JSON files
----------------------------

Loading a *JSON* file is fairly trivial with Python's  ``json`` module:

.. code:: python
   :number-lines: 1
   :name: read-names-from-json.py

   #!/usr/bin/env pythone

   import json
   with open('names.json') as fh:
      names = json.load(fh)
      print(names)

Output (re-formatted):

.. code:: shell

   python3 read-names-from-json.py

   {
     'kids': {
       'Chris': 'Family Guy', 'Pebbles': 'The Flintstones', 
       'Bart': 'The Simpsons'
     },
     'adults': {
       'Fred': 'The Flintstones', 'Betty': 'The Flintstones', 
       'Homer': 'The Simpsons', 'Lois': 'Family Guy'
     },
     'other': {
       'Klaus': 'American Dad', 'Brian': 'Family Guy', 'Roger': 'American Dad'
     }
   }

Working with YAML files
=======================

In terms of purpose the [YAML]_ format is quite similar to *JSON*, except for
two aspects:

- its improved readability
- provides richer data serialization capabilities

One of the most notable usage for of the *YAML* format in the Python ecosystem
is the [Ansible]_ configuration management solution.

YAML support in Python
----------------------

Currently the "Python Standard Library" does not have *YAML* support.
Fortunately there are multiple 3rd party modules, which can be easy installed
using the ``pip`` package management tool.

Perhaps the most popular solution is provided by the [PyYAML]_ project. To
install the module execute:

.. code:: shell

   pip install pyyaml

Writing data to a YAML file
---------------------------

Re-using the cartoon characters `data <#cartooncharacters>`_ we can export the
``names`` dictionary with the following simple code:

.. code:: python
   :number-lines: 1
   :name: write-names-as-yaml.py

   #!/usr/bin/env python3

   import yaml

   names = {
             'kids': {
                       'Chris': 'Family Guy',
                       'Pebbles': 'The Flintstones',
                       'Bart': 'The Simpsons'
                     },
             'adults': {
                         'Fred': 'The Flintstones',
                         'Betty': 'The Flintstones',
                         'Homer': 'The Simpsons',
                         'Lois': 'Family Guy'
                       },
             'other': { 'Klaus': 'American Dad',
                        'Brian': 'Family Guy',
                        'Roger': 'American Dad'
                      }
           }
   with open('names.yaml', 'wt') as fh:
      yaml.dump(names, fh)

Focusing on the new instructions:

- **line 3:** load the ``yaml`` module
- **line 23:** the ``yaml.dump()`` takes 2 arguments: the data structure
  (usually as a ``dict``) and a file-handler

The program produces the ``"names.yaml"`` file with the following content
(re-formatted for readability):

.. code-block:: yaml
   :name: names.yaml

   adults: {Betty: The Flintstones, Fred: The Flintstones, Homer: The Simpsons, Lois: Family Guy}
   kids: {Bart: The Simpsons, Chris: Family Guy, Pebbles: The Flintstones}
   other: {Brian: Family Guy, Klaus: American Dad, Roger: American Dad}

More advanced YAML use-case
---------------------------

The *YAML* specifications (see [YAML_specs]_) contain various simple, yet informative examples
about the more advanced capabilities of the format.

.. code-block:: yaml
   :name: invoice.yaml

   ---
   invoice: 34843
   date   : 2001-01-23
   bill-to: &id001
       given  : Chris
       family : Dumars
       address:
           lines: |
               458 Walkman Dr.
               Suite #292
           city    : Royal Oak
           state   : MI
           postal  : 48046
   ship-to: *id001
   product:
       - sku         : BL394D
         quantity    : 4
         description : Basketball
         price       : 450.00
       - sku         : BL4438H
         quantity    : 1
         description : Super Hoop
         price       : 2392.00
   tax  : 251.42
   total: 4443.52
   comments:
       Late afternoon is best.
       Backup contact is Nancy
       Billsmer @ 338-4338.


Reading data from a YAML files
------------------------------

Let's create our usual program to read the current format, but with a few 
additional features: 

#. Instead of hard-coding the data file's name in the program, require the
   data file's  name as an CLI argument
#. Using the ``pprint`` (pretty-print) module display the data in a more
   readable format
#. Try to handle errors

.. code:: python
   :number-lines: 1
   :name: read-yaml.py

   #!/usr/bin/env pythone

   import sys
   import yaml
   import pprint as pp

   try:
      fh = open(sys.argv[1])
      data = yaml.load(fh)
   except IndexError:
      print('I need an argument: YAML file name')
      sys.exit(1)
   except FileNotFoundError:
      print('File "{}" is not found!'.format(sys.argv[1]))
      sys.exit(2)
   except yaml.parser.ParserError:
      msg = 'The file {} does not appear to be a valid YAML file!'
      print(msg.format(sys.argv[1]))
   pp.pprint(data)


Working with XML files
======================

The eXtensible Markup Language (XML) format is has been the workhorse of data
exchange in the last two decades. Because of its flexibility and the rich
ecosystem XML is still an often used format, especially in enterprise
applications. The format is best suited for the representation of tree-like
data structures. XML also provides standards and tools for the verification of
the data based on schema.

Following is a first simple example of our cartoon characters data in as XML:

.. _examplexml:

.. code-block:: xml
   :name: names-fred-orig.xml

   <character id="1000"fname="Fred" sname="Flintstone">
     <appeared_in>The Flintstones</appeared_in>
     <relations>
       <relation character_id="1001" type="child">
       <relation character_id="1002" type="spouse">
     </relations>
   </character>

XML support in Python
---------------------

Python has rich XML support in the form of multiple XML related modules and
projects. The two main reason for the lack of a single implementation are on
the one hand the huge scope and functionality of XML, and different
implementations with overlapping functionality.
Out of the many a few of these XML implementations also have made it to the
"Python Standard Library". (see for more [pydoc_markup_tools]_)

In our example we'll be using the ``lxml`` module, which is currently
a popular choice.  (see for more [lxml]_) This module is a wrapper around the
``libxml2`` and ``libxslt`` libraries, both written in C. (see also:
http://www.xmlsoft.org/)

Execute the following to install the ``lxml`` module:

.. code:: shell

   pip install lxml

**NOTE:** The installation of ``lxml`` require a working C compiler, which may
be an issue, especially for Windows users. Please visit the "Installing
``lxml``" page ([lxml_install]_) which provides a link to the "unofficial
Windows binaries".


Writing XML data
----------------

Working with XML is significantly more complex than the previously discussed
formats. To get acquainted with the API let's follow the "``lxml`` Tutorial" (see
[lxml_tutorial]_) and try to code the `above <#examplexml>`_ example manually
in an interactive Python session:

.. code:: pycon
   :number-lines: 1

   >>> from lxml import etree
   >>> root = etree.Element('character', attrib={'id': '1000', 'fname': 'Fred', 'sname': 'Flintstone'})

At this point the ``root`` variable is bound to an object, which represents an
XML node. Let's see how the data is organized:

.. code:: pycon
   :number-lines: 3

   >>> type(root)                      # the object's type
   <type 'lxml.etree._Element'>
   >>> root.tag                        # the XML tag of this node
   'character'
   >>> root.attrib                     # the XML attributes of the node
   {'fname': 'Fred', 'id': '1000', 'sname': 'Flintstone'}

The string representation of this node:

.. code:: pycon
   :number-lines: 9

   >>> etree.tostring(root)
   b'<character fname="Fred" id="1000" sname="Flintstone"/>'

**WARNING:** Notice the ``b`` prefix in the result of the ``tostring()``
function: the returned object is of type ``bytes`` (and not ``str``)! If we
were to attempt to write this to a file which has been opened in text mode
(e.g.: "``open( 'somename.xml', 'wt')``"), we would get an Exception!

The simple rule here is: ``bytes`` objects can be written to binary files
(i.e.: mode "``wb``") and ``str`` objects to text files (i.e.: mode "``wt``")

For a ``str`` result we need to decode the ``tostring()`` function's result:

.. code:: pycon
   :number-lines: 11

   >>> etree.tostring(root).decode()
   '<character fname="Fred" id="1000" sname="Flintstone"/>'

Next, we add two child nodes representing the ``appeared_in`` and the
``relations`` tags and check the XML output:

.. code:: pycon
   :number-lines: 13

   >>> a = etree.Element('appeared_in') # create a new node
   >>> b = etree.Element('relations')   # another new node
   >>> root.append(a)                   # add the ``a`` node to root
   >>> root.append(b)                   # add the ``b`` node to root

   >>> ### Check the XML representation of ``root``
   >>> print(etree.tostring(root, pretty_print=True).decode())
   <character fname="Fred" id="1000" sname="Flintstone">
     <appeared_in/>
     <relations/>
   </character>

   >>>

The ``root`` element is an container object, which currently holds 2 objects.
The API makes it possible to treat ``root`` as if it was a ``list``.

.. code:: pycon
   :number-lines: 26

   >>> root[0].tag                     # element lookup with similar to ``list``
   'appeared_in'
   >>> len(root)                       # the ``len()`` works correctly
   2

   ### with ``for`` we can iterate through the elements
   >>> for node in root:
   ...     print(node.tag, node.attrib)
   ... 
   appeared_in {}
   relations {}
   >>>

Let's add the missing pieces:

.. code:: pycon
   :number-lines: 38

   ### Add the cartoon title to the ``appeared_in`` tag
   >>> root[0].text = 'The Flintstones'
   >>> print(etree.tostring(root, pretty_print=True).decode())
   ### Show changes in XML representation
   <character fname="Fred" id="1000" sname="Flintstone">
     <appeared_in>The Flintstones</appeared_in>
     <relations/>
   </character>

   ### Add first relation
   >>> r1 = etree.Element('relation', attrib={'character_id': '1002', 'type': 'spouse'})
   ### index 1 is the earlier ``relations`` node. Add ``r1`` node to this
   >>> root[1].append(r1)
   ### Show XML representation
   >>> print(etree.tostring(root, pretty_print=True).decode())
   <character fname="Fred" id="1000" sname="Flintstone">
     <appeared_in>The Flintstones</appeared_in>
     <relations>
       <relation character_id="1002" type="spouse"/>
     </relations>
   </character>

   ### Add second relation
   >>> r2 = etree.Element('relation', attrib={'character_id': '1001', 'type': 'child'})
   >>> root[1].append(r2)
   ### Show XML representation
   >>> print(etree.tostring(root, pretty_print=True).decode())
   <character fname="Fred" id="1000" sname="Flintstone">
     <appeared_in>The Flintstones</appeared_in>
     <relations>
       <relation character_id="1002" type="spouse"/>
       <relation character_id="1001" type="child"/>
     </relations>
   </character>

At this point we can export the data in XML format:

.. code:: pycon
   :number-lines: 72

   >>> fh = open('names-fred-written.xml', 'wt')
   >>> fh.write(etree.tostring(root, pretty_print=True).decode())
   198
   >>> fh.close()

The content of the ``names-fred-written.xml`` file looks like this:

.. code-block:: xml

   <character fname="Fred" id="1000" sname="Flintstone">
     <appeared_in>The Flintstones</appeared_in>
     <relations>
       <relation character_id="1002" type="spouse"/>
       <relation character_id="1001" type="child"/>
     </relations>
   </character>

To summarize the above interactive session, let's put the essential bits into
a single Python program:

.. code:: python
   :number-lines: 1
   :name: write-names-as-xml-fred.py

   #!/usr/bin/env python3
   from lxml import etree
   root = etree.Element('character',
                        attrib={'id': '1000',
                                'fname': 'Fred',
                                'sname': 'Flintstone'})
   a = etree.Element('appeared_in') # create a new node
   b = etree.Element('relations')   # another new node
   root.append(a)                   # add the ``a`` node to root
   root.append(b)                   # add the ``b`` node to root
   root[0].text = 'The Flintstones' # add title in node ``appeared_in``
   r1 = etree.Element('relation', attrib={'character_id': '1002',
                                          'type': 'spouse'})
   root[1].append(r1)
   r2 = etree.Element('relation', attrib={'character_id': '1001',
                                          'type': 'child'})
   root[1].append(r2)

   with open('names-fred-written.xml', 'wt') as fh:
       fh.write(etree.tostring(root, pretty_print=True).decode())


Reading data from an XML file
-----------------------------

Using our previous example, let's try re-create the ``root`` object from the
XML file:

.. code:: pycon
   :number-lines: 1

   >>> fh = open('names-fred-written.xml')
   >>> root = etree.fromstring(fh.read())

- **line 1:** open the XML file in ``read-only`` and ``text`` mode, because of
  implied ``"wt"`` mode string
- **line 2:** the step in the order as they are executed:

  - ``fh.read()`` method will read the entire content of the file into
    a ``str``
  - ``etree.fromstring()`` function will convert this string to an instance of
    ``lxml.etree._Element``, i.e.: the Python object representing the XML
    content

At this point the object bound to the ``root`` variable contains all
information from the file. Using a ``for`` loop we can iterate through the
elements:

.. code:: pycon
   :number-lines: 3

   >>> for node in root:
   ...     tmpl.format(node.tag, len(node), node.text, node.attrib)
   ...
   'appeared_in          0     The Flintstones      {}'
   'relations            2     \n                    {}'

To summarize:

.. code:: python
   :number-lines: 1
   :name: read-names-from-xml.py

   #!/usr/bin/env python3
   from lxml import etree

   fh = open('names-fred-written.xml')
   root = etree.fromstring(fh.read())
   for node in root:
       tmpl.format(node.tag, len(node), node.text, node.attrib)

For large XML files this approach may be less efficient, since all the
processing is done in the Python interpreter. A more efficient way would be to
outsource the bulk of the work the underlying ``libxml2`` and ``libxstl``
libraries (see http://www.xmlsoft.org/), which we will consider next.


Processing XML data in Python
-----------------------------

Because the data that can be stored in XML format, can be large in terms of
both complexity and amount, processing is usually a non-trivial task. The
``lxml`` FAQ (see [lxml_faq]_) lists several considerations when processing
XML data. Dealing with large XML files can be more efficient using the
[xpath]_ technology, especially if we are only interested in certain parts.

Using an XPath search string return all nodes with the ``relation`` tag. The
parsing and searching is done in the C library, instead of Python, so it's the
performance is optimal:

.. code:: pycon
   :number-lines: 1

   >>> root.findall(".//relation")
   [<Element relation at 0x7f923f495888>, <Element relation at 0x7f923f46b7c8>]

As above, except loop through all the ``relation`` node(s) and show their
attributes.

.. code:: pycon
   :number-lines: 1

   >>> for e in root.findall(".//relation"): print(e.attrib)
   ...
   {'character_id': '1002', 'type': 'spouse'}
   {'character_id': '1001', 'type': 'child'}

The following XPath search string will limit the results to ``relation`` nodes
which have a ``type`` attribute with the value ``spouse``.

.. code:: pycon
   :number-lines: 1

   >>> for e in root.findall('.//relation[@type="spouse"]'):
   ...     print(e.attrib)
   ...
   {'character_id': '1002', 'type': 'spouse'}
   >>>


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

.. [INI_format] The INI file format is an informal standard for configuration
   files capable of representing tree-structure like information.
   See: https://en.wikipedia.org/wiki/INI_file

.. [pydoc_configparser] The ``configparser`` module implements the INI
   configuration file format.
   See https://docs.python.org/3/library/configparser.html

.. [pep274] Dictionary Comprehensions
   https://www.python.org/dev/peps/pep-0274/

.. [JSON] JSON is a language-independent data format. It was derived from
   JavaScript, but many modern programming languages include code to generate
   and parse JSON-format data.
   https://en.wikipedia.org/wiki/JSON

.. [YAML] YAML is a human-readable data-serialization language. It is commonly
   used for configuration files, but could be used in many applications where
   data is being stored or transmitted
   https://en.wikipedia.org/wiki/YAML

.. [Ansible] Ansible is an open-source software provisioning, configuration
   management, and application-deployment tool.
   https://en.wikipedia.org/wiki/Ansible_(software)

.. [PyYAML] PyYAML is a full-featured YAML framework for the Python
   programming language.
   https://pyyaml.org/

.. [YAML_specs] Full length examples of YAML
   https://yaml.org/spec/1.2/spec.html#id2761803

.. [lxml_install] https://lxml.de/installation.html

.. [lxml_tutorial] A brief overview of lxml's concepts
   https://lxml.de/tutorial.html

.. [pydoc_markup_tools] The Python Standard Library's Structured Markup
   Processing Tools
   https://docs.python.org/3/library/markup.html

.. [lxml] The ``lxml`` XML toolkit is a Pythonic binding for the C libraries
   libxml2 and libxslt.  It provides a the feature completeness of the
   C libraries with a mostly compatible API to the well-known ElementTree API
   from the Python Standard Library.

.. [lxml_faq] The lxml Frequently Asked Questions
   https://lxml.de/FAQ.html

.. [xpath] The XPath language provides the ability to navigate around in XML
   documents, selecting nodes by a variety of criteria.

   For more see:

   - XPath in Wikipedia: https://en.wikipedia.org/wiki/XPath
   - XML and XPath tutorials over at w3school:

     - https://www.w3schools.com/xml/xml_xpath.asp
     - https://www.w3schools.com/xml/xpath_intro.asp

.. _pydoc open: https://docs.python.org/3/library/functions.html#open
.. _pydoc unicode: https://docs.python.org/3/howto/unicode.html


.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
