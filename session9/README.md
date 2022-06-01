---
title: Solving practical problems with Python
author: Gábor Nyers <python-tuesday@trebut.nl>
date: 2022-05-03
licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/
---

<link rel="stylesheet" href="styles.css">

# Solving practical problems with Python


## Abstract

In this session we'll be focusing on solving simple problems while learning about the
language, its 
[**built-in data structures**](https://docs.python.org/3/library/stdtypes.html)
and a few functions provided by the 
[**Python Standard Library**](https://docs.python.org/3/library/index.html).

The chosen use-case is related to file management: we will be building a moderately
sophisticated program to analyze the content of a directory.  Our program should
recursively read the content of a directory and provide answers to questions such as: how
many directories, files, symbolic- and hard links are in the directory?

We will take a step-by-step approach and will make a few sidesteps to related topics of
interest.

This session is meant for the **novice** Python programmer; you may code along or just
focus on the explanation on how to approach the problem and build the solution.

### Disclaimer :-)

Sort of... The purpose of this session is to provide practical guidance for novice Python
programmers. The resulting code probably lacks most elementary software engineering
practices, such as tests and most error checking- and handling.

So you shouldn't use it directly on your production system or on a job
interview.


## Prerequisites

For more information about setting up a Python development environment please refer to the
this [earlier session](../session1/README.rst).

### Linux

**NOTE**: The actual installation depends on your Linux distribution (e.g.:
RedHat/CentOS/openSUSE or Debian/Ubuntu etc...) and -- in case of VSCode -- if your
preference of using a containerized application, such as provided by
[Flatpak](https://flatpak.org/) or [Snap](https://snapcraft.io/).

1. Install/verify the Python interpreter (usually installed by default)

   - RHEL/AlmaLinux/RockyLinux/CentOS: 
     install: `yum install python3`
   - openSUSE / SUSE: `zypper install python3`
   - Debian / Ubuntu: `apt install python3`

1. Install VSCode

   - With native package manager for above Linux distro's: 
     [VSCode download page](https://code.visualstudio.com/Download)
   - With [Flatpak](https://flathub.org/apps/details/com.visualstudio.code)
   - With [Snap](https://snapcraft.io/code) 

### Windows

Both Python and VScode can be installed from the Microsoft Store:

1. Install Python v3.9+:

   1. Press the `Win` key on you keyboard, which will pop-up both the "Start menu" and the
      "Type here to search" search box.
   1. Start typing: `microsoft store`, which will appear in the search box.
   1. Press the `Enter` key or click on the "Microsoft Store" icon to start the
      application.
   1. In the "Microsoft Store" application search for "`python`", which can be installed
      free of charge.
   
1. Install VSCode v1.67+:

   1. Still in the "Microsoft Store" application search for "`vscode`", which should
      return the "Visual Studio Code" application.
   1. This application can also be installed free of charge.

Alternatively, you can also download and install both applications with the usual
installation procedure:

1. Download Python v3.9+ installer from
   [this page](https://www.python.org/downloads/windows/). 

1. Download VSCode  v1.67+ installer from
   [this page](https://code.visualstudio.com/download/)


## Getting familiar with the Python interactive shell


### What is it?

The Python interactive shell or "**REPL**" 
(from **R**ead - **E**val - **P**rint - **L**oop) allows for:

1. Interactive execution of individual Python instructions

   Start the Python REPL from a shell (e.g.: Bash or PowerShell):

   ~~~bash
   $ python3 
   Python 3.6.12 (default, Dec 02 2020, 09:44:23) [GCC] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> 
   ~~~

   The obligatory "`Hello world!`" string:

   ~~~python
   >>> print('Hello World!')
   Hello World!
   >>>
   ~~~

   Assign a value to the variable `name` and show its value:

   ~~~python
   >>> name = 'Alice'
   >>> name
   'Alice'

   ~~~

   Import the JSON module and convert a JSON string:
   
   ~~~python
   >>> json_str = '{"name": "Alice", "email": "alice@example.com"}'
   >>> import json
   >>> data = json.loads(json_str)
   >>> data
   {'name': 'Alice', 'email': 'alice@example.com'}

   ~~~

1. Quick interactive composition of complex "one-liner" statements, e.g.:

   1. Get some user input and store it in the variable `email`:

      ~~~python
      >>> email = input('Please enter your name: ')
      Please enter your name: Alice White
      >>> email
      'Alice White'
      ~~~
 
   1. Lower-case the input string:

      ~~~python
      >>> email = input('Please enter your name: ') .lower()
      Please enter your name: Alice White
      >>> email
      'alice white'
      ~~~
 
   1. Lower-case the input string and replace the `space` characters with `_` (underscore)

      ~~~python
      >>> email = input('Please enter your name: ') .lower().replace(' ', '_')
      Please enter your name: Alice White
      >>> email
      'alice_white'
      ~~~
 
   1. Create an email address from a user provided name:

      ~~~python
      >>> email = input('Please enter your name: ') .lower().replace(' ', '_') + '@example.com'
      Please enter your name: Alice White
      >>> email
      'alice_white@example.com'
      ~~~

1. Using the built-in `help()` function to view the documentation of **any**
   object in memory:

   ~~~python
   >>> help(input)
   Help on built-in function input in module builtins:

   input(prompt=None, /)
       Read a string from standard input.  The trailing newline is stripped.
   ...

   >>> help(email)
   ~~~

   **NOTE**: press the "`q`" key to exit "`help()`".
 

## A few simple snippets for managing files


The following [Python][python] snippets are small building blocks that can be assembled
into more powerful programs.

   
### Snippets for navigating the file system

1. Get the current working directory:

   ~~~python
   import os                      # import the `os` module
   cwd = os.getcwd()              # The current working directory, e.g.
                                  # /home/tux/Documents 
   ~~~

   **NOTE**: 

   1. `import os`: the interpreter currently does not contain the required functionality
      to find out about the current working directory, so we'll need to load this from an
      external module (a.k.a.: library).
   1. Variable `cwd` will contain the returned value, which we can reuse later in our
      program.

1. Change the current working directory:
   
   ~~~python
   import os                      # just to be sure: import the `os` module
   os.chdir('/tmp')               # Set the current working directory to /tmp
   ~~~

   **NOTE**:

   1. The `import os` is only required once per program, but let's mention it again so
      that the snippet to be used stand-alone.
   1. `os.chdir()` always returns `None`, which we don't bother to "remember" in a
      variable, so the function call stands alone.


### Snippets for listing of a directory content

1. List the content of a directory, i.e.: **all** files, directories etc...:

   ~~~python
   import os
   files_cwd = os.listdir('.')    # the content of the current directory (see `getcwd()`)
   print(files_cwd[:4])           # e.g.: [ 'README.md', 'names.csv', 'subdir' ]
                                  # `[:4]` notation: show up to the 4th element

   files2 = os.listdir('/tmp')    # list the content of the `/tmp` directory (absolute
                                  # path!)
   files3 = os.listdir('subdir')  # the content of the `subdir` directory (relative path!)

   error = os.listdir('/tmp/*.py')  # ERROR!
   ~~~

   **NOTE**:
  
   1. The path of the directory can be referred to with absolute or relative notation.
   1. `os.listdir()` will only list the directory's content, **not that of subdirs**!
   1. The `files[:4]` will limit the output to the first 3 directory entries.
   1. Directory entries can be files, directories and other file system objects
   1. `os.listdir()` **does not allow wildcards**!

1. List the content using wildcards:

   ~~~python
   import glob
   py_files = glob.glob('/tmp/*.py')   # return all Python files in /tmp
   ~~~
  
   **NOTE**:

   1. The `py_files` will contain a list of strings, similar to the `os.listdir()`
      output.
   1. The wildcard syntax is similar to the `ls` or `dir` commands, e.g.:

      - `?`: match exactly 1 character, e.g.: `file?.bin` matches `file1.bin` or
        `fileA.txt`
      - `*`: match any number of characters (0 or many), e.g: `*` matches all files
      - `[a1X]`: match exactly 1 of the mentioned character, e.g.: `file[a1X].txt` will
        match files `filea.txt`, `file2.txt` and `fileX.txt`, but **not** `fileB.txt`


1. Emulate the `ls -1 /tmp/*.py` command:

   ~~~python
   import glob                         # load the module `glob`
   py_files = glob.glob('/tmp/*.py')   # store every Python files's name as a list
   for f in py_files:                  # for every file name in `py_files`...
       print(f)                        # ... print its name
   ~~~

   **NOTE**: 

   1. `glob.glob()` seems a bit redundant, but that's how the module is provided.
   1. `glob()` will store the matching filenames in a list. If no matching file found, the
      list is empty.
   

### Snippets to get types and attributes of files and directories

File system objects have several attributes, e.g.:

- **type**, such as: file, directory, symbolic links, sockets etc...
- **permissions**, e.g.: on Linux, MacOS X and other Unix-like OSs: readable, writeable or
  executable for owner, group-owner and others
- **timestamps**, e.g.: last -creation, -modification and -access
- etc...

1. Does `README.md` exists in the current working directory?

   A simple snippet showing how to build the existence check into an `if` construct:

   ~~~python
   import os.path as p                 # load os.path module, alias it to `p`
   fname = 'README.md'
   if p.exists(fname):
       print(f'"{fname}" exists!')
   else:
       print(f'"{fname}" DOES NOT exists!')
   ~~~
   
   **NOTE**:

   1. the `os.path.exists()` function will not differentiate between files, directories or
      other file system objects (e.g.: *symbolic links*)

1. Similar as above, but the code probes `README.md`'s type:

   ~~~python
   # We assume here that 'README.md' is a file in the current working directory

   import os.path as p                 # load os.path module, alias it to `p`
   fname = 'README.md'
   print(p.isfile(fname))              # is it a file? prints "True"
   print(p.isdir(fname))               # is it a directory? prints "False"
   print(p.islink(fname))              # is it a symbolic link? prints "False"
   ~~~

1. Get a file system object's attributes, such as: type, size, creation date:

   ~~~python
   import os

   fpath = 'exampledir/a/file2.bin'
   attrs = os.lstat(fpath)
   print(attrs.st_mtime)               # mod. time (sec. since epoch): 1653942544.7019486
   print(attrs.st_nlink)               # number of links to this inode: 3
   ~~~

   **NOTE**:

   Python also provides the `os.stat()` function, which - as opposed to `lstat()` will
   "follow" the link to its target and will report the attributes of the target objects.


### Snippets for manipulating paths

Sometimes you may need to manipulate the paths of files, e.g.:

1. Join several strings into a file path:

   ~~~python
   import os.path as p                 # load os.path module, alias it to `p`

   fpath = p.join('exampledir', 'a', 'file2.bin')    # 'exampledir/a/file1.dat'
   ~~~
   
1. Split a path into the directory path and the file name:

   ~~~python
   pieces = p.split(fpath)             # ('exampledir/a', 'file2.bin')
   
   # or in a more "Pythonic"-way using "tuple unpacking"
   dpath, fname = p.split(fpath)       # dpath='exampledir/a', fname='file1.dat'
   ~~~

1. Split the file's name and extension:

   ~~~python
   fname = 'file2.bin'

   # using the above "Pythonic" way 
   name, ext = p.splitext(fname)       # name='file2', ext='.bin'
   ~~~

   Or combining the `split()` and `splitext` functions:
   
   ~~~python
   fpath = 'exampledir/a/file2.bin')
   dirname, fname = p.split(fpath)     # ('exampledir/a/', 'file2.bin')
   name, ext = p.splitext(fname)       # name='file2', ext='.bin'
   ~~~
      

### Snippets for creating and deleting files and directories

1. Create a new subdirectory in the current working directory:

   ~~~python
   import os
   dname = 'demo'

   os.mkdir(dname)                     # the actual creation of the directory
   ~~~
  
1. Create the new empty file:

   ~~~python
   fname = 'emptyfile1'
   open(fname, 'w').close()            # the actual creation of the empty file
   ~~~

   **NOTE**: 
   
   1. The "`.`" (dot) is separating 2 different actions above, that will be executed in
      the following sequence:

      1. `open(fname, 'w')`: create a new, or **truncate** an existing file with the name
         `emptyfile1`, return an open **filedescriptor** to it.
      1. On the filedescriptor object invoke the `.close()` method, thus "releasing" this
         resource.

   1. The `'w'` character-code means: open for writing **and** create(/truncate!) the
      file. In case an existing file should remain, use `'x'` letter code.
      See [this table](https://docs.python.org/3/library/functions.html#open) for other
      options and their meaning.


1. Create a symbolic link:

   ~~~python
   import os
   fname = 'emptyfile1'                     # name of the file to link to
   dname = 'demo'                           # name of the dir to link to

   os.symlink(fname, 'symlink-to-'+fname)   # creates `symlink-to-emptyfile1`
   os.symlink(dname, 'symlink-to-'+dname)   # creates `symlink-to-demo`
   ~~~

   **NOTE**:
   
   1. On Windows creating a symbolic links is supported since Windows Vista.
   1. Beginning with Windows 10 symlinks can also be created without "Administrator"
      privileges.

1. Delete a file:

   ~~~python
   import os
   fname = 'emptyfile1'

   os.unlink(fname)                    # the actual deleting
   ~~~

1. Delete an **empty directory**; if not **yet** empty, must delete content first!:

   ~~~python
   import os
   dname = 'demo'

   os.rmdir(dname)                     # the actual deleting
   ~~~


## More advanced snippets

Let's now combine the above simple snippets and build a more advanced building blocks.


### Snippets for processing files

1. Create an overview list of files and directories:

   ~~~python
   import glob
   import os.path as p                 # import the module `os.path` as variable `p`
   files, dirs = [], []                # initialize 2 empty list objects

   fobjects = glob.glob('/tmp/[ab]*')  # every file or directory starting with "a" or "b"

   for f in fobjects:                  # loop through the elements of `fobjects`
       if p.isfile(f):
           files.append(f)             # if current item is a file, store its name in
                                       # the list `files`
       elif p.isdir(f):
           dirs.append(f)              # if item is a dir, store it in list `dirs`

   print('Files:', files)              # print out the list of files
   print('Directories:', dirs)         # ... and directories
   ~~~

   **NOTE**:
   
   1. To shorten the references to objects in a module, we can use an **alias**: 
      `import os.path as p`;
      
      In this case the objects in `os.path` can be prefixed simply with `p.`, such as
      `p.isfile()`, instead of `os.path.isfile()`.

   1. `files, dirs = [], []` is an example of **tuple packing and unpacking**; very
      practical to initialize multiple variables in a single line of code
   
1. Sort the files on size in ascending order (from small to large):

   ~~~python
   import glob
   import os

   def getsize(file):                                 # define a custom function, which
       '''Returns the file's size in bytes'''         # takes a file name as argument
       return os.stat(file).st_size                   # and returns its size.

   files = glob.glob('/tmp/*.jpg')                    # get a list of all JPG files
   files_bysize = sorted(files, key=getsize)          # sort by size in asc. order
   files_bysize_desc = sorted(files, key=getsize,     # same, but in desc. order
                              reverse=True)
   ~~~
  
   **NOTE**:
  
   1. The `getsize()` function simply returns the `file`'s size. 
   1. `os.stat()` function returns several file attributes, such as: size, timestamps
      of creation and modification, owner, etc... In this snippet the custom sorting
      function `getsize()` will return file's size.
   1. With a *sort function* `sorted()` can be instructed to perform the sorting
      based on an attribute or some criteria; in this case the sorting is done based
      on the file's size. <br/>
      See also the [Sorting HOWTO][sorting_howto].
   1. Specifying the `reverse=True` argument with the `sorted()` function, it will sort in
      descending order.

1. Create a ZIP archive from a list of files:

   ~~~python
   from zipfile import ZipFile              # load **only** the class (+dependencies)
   import glob

   files = glob.glob('/tmp/*.jpg')          # get a list of all JPG files
   zip = ZipFile(
            '/tmp/test-from-python.zip',    # ZIP file name
            mode='x')                       # open to write to, error if exists

   for f in files:                          # simple `for` loop to
       zip.write(f)                         # write all files from `files` to ZIP
   ~~~

   **NOTE**:

   1. `from zipfile import ZipFile` is an alternative to load **only parts** of a module
      into memory, instead of the whole thing.
   1. The last line is a shorthand for a `for` loop single instruction, that executes only
      a single instruction for each filename listed in `files`.


### Introducing `os.walk()`

The Standard Library's [`os.walk()`][os_walk] function will **recursively traverse a
directory hierarchy**. This is required by [Feature 1](#feature-1).

**Example**: To understand how the `os.walk()` function works, let's consider the
following directory hierarchy and code:

~~~bash
$ tree exampledir/
exampledir/
├── a
│   ├── b
│   │   ├── d
│   │   │   ├── file8
│   │   │   └── file9
│   │   └── file3
│   ├── file2.bin
│   └── file5
├── c
│   ├── e
│   │   └── file15
│   └── file13
└── file1.dat
~~~

Consider this simplistic demo of the `os.walk()` to illustrate its working:

~~~python
round = 0
for path,subdirs,files in os.walk('exampledir'):
    round += 1                              # increase counter
    print(f'--- Round {round} {"-"*20}')
    print(f'Current path    : {path}')
    print(f'Current subdirs : {subdirs}')
    print(f'Current files   : {files}')
~~~

The output of the above demo code on the directory `exampledir`:

~~~
--- Round 1 --------------------         :  exampledir/           <-- Round 1
Current path    : exampledir             :  ├── a                 <-- Round 2   
Current subdirs : ['a', 'c']             :  │   ├── b             <-- Round 3   
Current files   : ['file1.dat']          :  │   │   ├── d         <-- Round 4   
--- Round 2 --------------------         :  │   │   │   ├── file8
Current path    : exampledir/a           :  │   │   │   └── file9
Current subdirs : ['b']                  :  │   │   └── file3
Current files   : ['file5', 'file2.bin'] :  │   ├── file2.bin
--- Round 3 --------------------         :  │   └── file5
Current path    : exampledir/a/b         :  ├── c                 <-- Round 5
Current subdirs : ['d']                  :  │   ├── e             <-- Round 6
Current files   : ['file3']              :  │   │   └── file15
--- Round 4 --------------------         :  │   └── file13
Current path    : exampledir/a/b/d       :  └── file1.dat
Current subdirs : []                     :  
Current files   : ['file9', 'file8']
--- Round 5 --------------------
Current path    : exampledir/c
Current subdirs : ['e']
Current files   : ['file13']
--- Round 6 --------------------
Current path    : exampledir/c/e
Current subdirs : []
Current files   : ['file15']
~~~


**NOTE**:

The 2 fancy bits in the loop's declaration 
(`for path,subdirs,files in os.walk('exampledir'):`) are:


1. The expression `os.walk('exampledir')` will return a tuple in each round, e.g.:

   ~~~
   ('exampledir', ['a', 'c'], ['file1.dat'])
   ('exampledir/a', ['b'], ['file5', 'file2.bin'])
   ('exampledir/a/b', ['d'], ['file3'])
   ('exampledir/a/b/d', [], ['file9', 'file8'])
   ('exampledir/c', ['e'], ['file13'])
   ('exampledir/c/e', [], ['file15'])
   ~~~

   This `tuple` will always contain 3 elements:

   - 1st element (with index 0): current directory, that is being visited, e.g.:
     `exampledir/a`

   - 2nd element (index 1): a `list` of subdirectories in the current directory, e.g.: 
     `['b']` (list with a single element)

   - 3rd element (index 2): a `list` containing the file names that are located in the
     current directory, e.g.: `['file5', 'file2.bin']`
   
2. Using [**tuple unpacking**](https://www.w3schools.com/python/python_tuples_unpack.asp)
   the variables `path`, `subdirs` and `files` will be assigned the respective elements of
   the above tuples in each round, e.g.:

   ~~~
   path, subdirs, files = ('exampledir/a', ['b'], ['file5', 'file2.bin'])
   #  ^      ^      ^      \____________/  \___/  \____________________/ 
   #  |      |      |            |           |              |
   #  `------|------|------------'           |              |
   #         `------|------------------------'              |
   #                `---------------------------------------'
   #
   # After unpacking, the variables hold the following values:
   #
   print(path)                    # exampledir/a            (type: str)
   print(subdirs)                 # ['b']                   (type: list of str)
   print(files)                   # ['file5', 'file2.bin']  (type: list of str)
   ~~~
   

## Build an actual program from the snippets


### Features

##### Feature 1
Recursively analyze the content of a directory, which is provided as an argument.

##### Feature 2
Show the total number of files in the entire hierarchy.

##### Feature 3
Show the top 10 directories in terms of size or number of files in them.

See [this example implementation](profiler).

**NOTES**:

1. The program's main feature is to create the following `dict` data structure while
   analyzing the directory's content:

   ```
   {
     'exampledir/': {'disk_usage': 7, 'inode': 40539923, 'isdir': True, 'isfile': False, 
                     'issymlink': False, 'nr_of_nondirs': 1, 'refcount': 4, 'size': 41},
     'exampledir/a': {'disk_usage': 13, 'inode': 40539935, 'isdir': True, 'isfile': False,
                      'issymlink': False, 'nr_of_nondirs': 2, 'refcount': 3, 'size': 45},
     'exampledir/a/b': {'disk_usage': 153, 'inode': 217065954, 'isdir': True, 'isfile': False,
                        'issymlink': False, 'nr_of_nondirs': 1, 'refcount': 3, 'size': 28},
     'exampledir/a/b/d': {'disk_usage': 327, 'inode': 38206054, 'isdir': True, 'isfile': False,
                          'issymlink': False, 'nr_of_nondirs': 2, 'refcount': 2, 'size': 32},
     'exampledir/a/b/d/file8': {'inode': 40485983, 'isdir': False, 'isfile': True,
                                'issymlink': False, 'refcount': 1, 'size': 134},
     'exampledir/a/b/d/file9': {'inode': 298461643, 'isdir': False, 'isfile': True,
                                'issymlink': True, 'refcount': 1, 'size': 193},
     ...
   }
   ```

1. Based on the above data will all other conclusions be reached at the end of the
   program, such as:

   - number of directories,
   - number of non-dirs (i.e.: files, hard- and symlinks),
   - number of symlinks,
   - number of hardlinks,
   - the used disk space (in bytes)
   - which of the hardlinks point to the same file? 


<!--Links-->
[python]: https://python.org "The Python home page"
[sorting_howto]: https://docs.python.org/3/howto/sorting.html#key-functions "Sorting HOWTO"
[os_walk]: https://docs.python.org/3/library/os.html#os.walk "os.walk()"

<script src="script.js" defer></script>

<!--
vim: filetype=markdown spelllang=en,nl spell foldmethod=marker lbr nolist ruler
vim: tw=90 wrap showbreak=… shiftwidth=2 tabstop=2 softtabstop=2 expandtab
-->
