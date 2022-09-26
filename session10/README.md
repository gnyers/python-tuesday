---
title: Solving practical problems with Python - Part 2
author: Gábor Nyers <python-tuesday@trebut.nl>
date: 2022-09-18
licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/
---
 
<link rel="stylesheet" href="../assets/css/styles.css">



# Abstract

The [`profiler`][profiler] program from the [previous session][session09] performs its
main function but lacks almost all software engineering practices that makes a program
robust enough for general use. In this session we will implement a number of these
necessary features, like the ability to control the program's behavior with 
[**CLI arguments**](#add-cli-arguments) and provide 
[**logging**](#add-logging).
We will also solve the [**challenge**](#solve-the-challenge) described at the end of the
previous session.

**Audience**: This session -- like the previous one -- is meant for the novice Python programmer
You may code along or just focus on how to approach the problem and build a solution.



# Recap of the `profiler` program

For more information on its features see the [previous session][session09].

1. Goal: recursively analyze the content of a directory
1. Print information about:

   1. the number of filesystem objects, e.g.: files, directories, symbolic- and hard
      links; and
   1. the disk space used by all the above elements

   See [Example output](#example-output)

1. The source code of [`profiler`][profiler] lists a few of shortcomings of the
   implementation:

   ~~~markdown
   **Challenge:**
   
   The method used to calculate the `total_disk_usage` does not take hardlinks
   into account.
   
   (1) Why?
   (2) Based on the `distict_files` dictionary, you could correct the
       value of `total_disk_usage` to calculate the **exact** disk usage. How?
   ~~~


## Example output: 

~~~bash
$ ./profiler exampledir 
--- Statistics of directory: exampledir
Number of errors encountered while processing 0
   
The number of dirs: 6
The number of non-dirs (i.e.: files, hard- and symlinks): 8
The number of symlinks: 1
The number of hardlinks: 3
Used disk space: 524 bytes
Which of the hardlinks point to the same file? 
  exampledir/file1.dat, exampledir/a/file2.bin, exampledir/c/e/file15 : 7 bytes
~~~

The content of the `exampledir` directory is the following:

~~~bash
$ tree -F exampledir/
exampledir/
├── a/
│   ├── b/
│   │   ├── d/                              #     + symbolic link
│   │   │   ├── file8                       #     | (ie.: special file
│   │   │   └── file9 -> ../../../c/file13  #  <--+  pointing to a path)
│   │   └── file3                           #  
│   ├── file2.bin                           #  <--+ hard links
│   └── file5                               #     | (ie.: different names
├── c/                                      #     |  point to the same
│   ├── e/                                  #     |  content, which is 
│   │   └── file15                          #  <--+  stored only once
│   └── file13                              #     |  on disk)
└── file1.dat                               #  <--+
~~~



# Solve the challenge


## The problem with the disk usage calculation

Currently the total disk usage is being calculated with this
[list-comprehension][list-comprehension] expression:

~~~python
total_disk_usage = sum([ attrs.get('disk_usage',0)
                         for path,attrs in data.items()
                         if attrs['isdir']
                       ])
~~~

**Why** is this expression incorrect?

:  In the calculation of the total disk usage above expression will disregard the fact
   that [hard links][hard-link] are *just names* pointing to the same [**inode**][inode]
   (i.e.: file content).

     Instead of counting the size **only once**, the current expression adds the file's
     size to the total for **every** hardlink, i.e.: `file2.bin`, `file15` and `file1.dat`


## Calculate the correct total usage

The **Solution**:

:  We need an auxiliary data structure that contains the inodes of **all** non-directory
   filesystem objects. The calculation should only take into account the sizes of those
   inodes mentioned here.

     **NOTE**: See [profiler.1](profiler.1) for the implemented solution!
   
     1. the auxiliary data structure could be either:

        -  a `set`, e.g:

           ~~~python
           deduped_non_dir_inodes = { attrs['inode']
                                      for path, attrs in data.items() 
                                      if not attrs['isdir'] }
           # deduped_non_dir_inodes:
           # {217065955, 40485989, 40485993, 298461643, 40485982, 40485983}
           ~~~

        -  or a `dict`, e.g.:

           ~~~python
           deduped_non_dir_inodes = { attrs['inode']:path 
                                      for path, attrs in data.items()
                                      if not attrs['isdir'] } 
           # deduped_non_dir_inodes:
           # { 40485993: '../session09/exampledir/c/e/file15',
           #   40485989: '../session09/exampledir/a/file5',
           #   217065955: '../session09/exampledir/a/b/file3',
           #   40485982: '../session09/exampledir/a/b/d/file9',
           #   40485983: '../session09/exampledir/a/b/d/file8',
           #   298461643: '../session09/exampledir/c/file13' }
           ~~~

        The `dict` option is more suitable for this case, because we already have the
        dictionary `data`.  
        The keys of which are the filesystem objects' `path`. So by combining the two,
        we can easily retrieve the `size` of each unique non-directory `inode`:

        ~~~python
        >>> deduped_non_dir_inodes[217065955]
        '../session09/exampledir/a/b/file3'

        >>> data['../session09/exampledir/a/b/file3']['size']
        153
        ~~~

     1. modify the expression that calculates the total disk usage:

           ~~~python
           deduped_non_dir_inodes = {attrs['inode']: path      
                                     for path, attrs in data.items()
                                     if not attrs['isdir'] }
           total_disk_usage_corrected = sum([ data[path]['size']
                             for inode,path in deduped_non_dir_inodes.items()])
           ~~~

        **NOTE**: that the calculation now loops through the auxiliary data structure
        `deduped_non_dir_inodes`.


**NOTE**: See [profiler.1](profiler.1) for the implemented solution!



**Incorrect solution**:

:  It could be argued that the original expression needs only to be slightly modified and
   extended with a simple check `attrs['refcount'] < 2`, e.g.:

     ~~~python
     # Incorrect solution:
     total_disk_usage = sum([ attrs['size']
                              for path,attrs in data.items()
                              if not attrs['isdir'] 
                                 and attrs['refcount'] < 2 ])  # <-- check of refcount
     ~~~
     
     **Why** is this incorrect:
     
     -  Most importantly: above expression will disregard **all** hard-links and will not
        count the size of **any** them! For the correct calculation of the total disk
        usage the size of **every inode** needs to be added **exactly once**!

     -  Also: there could be multiple **different**  hard-links in the directory structure.
     
        In this case `attrs['refcount']` only indicates that this filesystem object is a
        hard-link. It **does not** tells which [inode][inode] is being referenced by the
        current element.



# Add CLI arguments

## Introduction to CLI arguments

Since the session is meant for the novice programmer, let's recap the purpose and usage of
command-line (CLI) arguments.

- **Primary purpose** of CLI arguments:<br>
  From the early days of operating systems, CLI arguments are used to control a program's
  behavior by enumerating the required parameters on the command line.

- These arguments need to be interpreted (i.e.: "parsed") by the program **immediately**
  after start in order for it to configure its run-time parameters.


### The anatomy of a command

~~~bash
# <--(1)->   <-----------(2)---------------------->
#            <-----------(3)--------->
#            <--(a)-->   <----(b)---->
#                        <--(i)--|---<-(ii)-
#                                        <---(4)-->

  profiler   --verbose   --format=json   exampledir

#       ->(5)<-     ->(5)<-         ->(5)<-
#
~~~

**Where**:

1. the name of the command being executed

2. all the arguments separated by spaces that will be passed by the OS to 
   the program (1);

   in Python the CLI arguments are available in the `sys.argv` (of type `list`)

3. the CLI options for the program

   3.a) the GNU-style **long-named option** `--verbose` that represents a boolean
        recognizable by the double dash prefix and the lack of a value

   3.b) the long-named **option** with a **value**: `--format=json` representing a
        key/value pair:

      i. the name of the option: `--format`, and
      i. its value: `json`

4. a positional argument, usually representing the main input for the program

5. at least a single space character to separate the elements of the command


### Different styles of CLI arguments

1. "Unix-style" options: `-s -vvv -l prog.log`, or it's equivalents: `-v 3 -a`, 
   `-l prog.log -dv3`

1. "GNU-style" or "long-named" options: `--log prog.log --verbose=3 --all` 

1. "Windows-style" arguments: `/a /l prog.log /v`


### Complexity

A few examples to illustrate the complexity of CLI argument parsing:

-  the options and arguments may be specified in any order: `-a -v` or `-v -a`

-  each option separated `-a -v` or compacted form `-av`

-  options may have an optional value, e.g.: `--debug 3` (increase debug level to 3,
   instead of 1)

-  the same run-time parameter may have a "short" (`-l prog.log`) and "long" 
   (`--log prog.log`) name; with- or without the `=` sign: `--log=prog`

-  dealing with corner-cases, e.g.:

   -  distinction between an option's **value** and a **positional argument**, e.g.:
      `... --output json ...`
      (is `json` a value to the option `--output` **or** is it a positional argument?)

   -  passing a special character as a value to an option, e.g.: `cut -d "-"`

   -  delete the file with an unusual name, e.g.: `--somefile`

      typically solved by the introduction of a "sentinel" token, e.g.:
      `rm -- --somefile`, where `--` indicates that after it there are
      no more options, only positional arguments.


## Python libraries to deal with argument parsing

Because of the complexity outlined above, it is rarely a good idea to spend any effort
writing your own CLI parser. Python already provides a wealth of readily available and
high-quality libraries that will fit your needs.

An additional benefit is that most of these libraries will not only **parse** the CLI
arguments, but will perform **argument validation**.

A few examples of validation:

- `--log=prog.file`: will check whether or not the file `prog.file` is writeable?
- `--age=32`: will only accept positive integers in the range 0-120 as option value
- `--fqdn=www.example.com`: does the value match the notation of a "fully qualified domain
  name"?
- `--color=red`: verify that the value is one of a limited number of choices, e.g.: red,
  green or blue


A few useful Python libraries for CLI argument parsing:

1. [`argparse`][py-stdlib-argparse]: a modern implementation that is part of the 
   [Python Standard Library][py-stdlib]

   For additional examples see also the [Argparse tutorial][py-howto-argparse].

1. [`getopt`][py-stdlib-getopt]: the legacy argument parser of the 
   [Standard Library][py-stdlib], very similar to the standard argument parsing function
   `getopt` provided by both the GlibC library and the `bash` shell.

1. [`docopt`][py-doctopt]: an excellent 3rd-party library that allows the declaration of
   the CLI parsing features just by **describing** them using the documentation notation
   rules. (see this [example and demo](http://try.docopt.org/))

1. "Command Line Interface Creation Kit" or [`click`][py-click]: a fully featured
   3rd-party library for developing sophisticated command-line oriented applications.


## Implementation of a simple CLI parser with `argparse`

### The requirements

1. [require a single **mandatory** positional argument called `DIR`, that is
   interpreted as a directory's path to be analyzed]{ #req-1 }

2. [verify that the path in `DIR` exists and be a directory]{ #req-2 }

3. [provide a description of above options and arguments if the program is invoked with the
   `--help` or `-h` options.]{ #req-3 }

### Demo code

The following example demonstrates the usage of the [`argparse`][py-stdlib-argparse]
module.

~~~python
{% include("argparse-demo.py") %}
~~~
See also: [argparse-demo.py](argparse-demo.py)


### Verify the requirements:

1. single positional argument `DIR`, must point to a directory:

   Executing the program without any arguments will not work:

   ~~~bash
   $ ./argparse-demo.py 
   usage: argparse-demo.py [-h] DIR
   argparse-demo.py: error: the following arguments are required: DIR
   ~~~

2. `DIR` **MUST**:

   exist:

   ~~~bash
   $ ./argparse-demo.py /path/to/non-existing/dir
   usage: argparse-demo.py [-h] DIR
   argparse-demo.py: error: argument DIR: /path/to/non-existing/dir is not a directory
   ~~~

   be a directory:

   ~~~bash
   $ ./argparse-demo.py /etc/hosts
   usage: argparse-demo.py [-h] DIR
   argparse-demo.py: error: argument DIR: /etc/hosts is not a directory
   ~~~

3. Program description:

   ~~~bash
   $ ./argparse-demo.py --help
   usage: argparse-demo.py [-h] DIR

   Simple argparse demo for the `profiler` program

   positional arguments:
     DIR         path to directory to analyze

   optional arguments:
     -h, --help  show this help message and exit

   That's all folks!
   ~~~


### Actual implementation for `profiler`

**NOTE**: See [profiler.2](profiler.2) for the implemented solution!


**Demo 1**: wrong arguments

~~~bash
$ ./profiler.2 /path/to/non-existent/dir
usage: profiler.2 [-h] DIR
profiler.2: error: argument DIR: /path/to/non-existent/dir is not a directory
~~~

**Demo 2**: help function

~~~bash
$ ./profiler.2  -h
usage: profiler.2 [-h] DIR

Recursively analyze a directory structure and provide some stats about the
disk space usage of the entire content, the number of files, directories, hard-
en symlinks.

Usage:

  ./profiler exampledir

Example output of a simple directory structure:

  --- Statistics of directory: exampledir/
  Number of errors encountered while processing 0

  The number of dirs: 6
  The number of non-dirs (i.e.: files, hard- and symlinks): 8
  The number of symlinks: 1
  The number of hardlinks: 3
  Used disk space: 524 bytes
  Which of the hardlinks point to the same file?
    exampledir/file1.dat, exampledir/a/file2.bin, exampledir/c/e/file15 : 7 bytes

positional arguments:
  DIR         path to directory to analyze

optional arguments:
  -h, --help  show this help message and exit

That's all folks!
~~~


**NOTE**: See [profiler.2](profiler.2) for the implemented solution!




# Add logging

## Introduction to logging

**Purpose** of logging:<br>
To be able to follow the working of a program or identify malfunctions, it needs to **emit
information** about its **internal state**.

**NOTE**: 

1. While sometimes used as a synonym, **debugging** means something different: it involves
   some external tool (i.e.: a *debugger*), that will be actively used by (usually) a
   developer to **extract** ad-hoc information from the application in real time. 

1. Logging, on the other hand, is done by the application itself during run-time. It emits
   predetermined messages at predetermined points of its flow.

1. To be able to **control** the type and amount of log messages, some additional logic
   needs to be implemented by the program.


## Python libraries to deal with logging

 A few common ways of logging:

1. using the 
   [`print()`](https://docs.python.org/3/library/functions.html#print)
   function (or its variant:
   [`pprint()`](https://docs.python.org/3/library/pprint.html), 
   "p" as in "pretty-print")

1. the [`logging`][py-stdlib-logging] module in the [Python Standard Library][py-stdlib]

   The [logging`][py-stdlib-logging] module provides numerous sophisticated features, e.g.:

   - multiple logging sources, each with its own configurable threshold to suppress or
     allow messages and own (set of) handlers

   - customizable [handlers](https://docs.python.org/3/library/logging.handlers.html)
     which deliver log messages, e.g. to the console, a file, a local or remote syslog
     server, etc..

   - sophisticated
     [filters](https://docs.python.org/3/library/logging.html#filter-objects) to allow or
     supress messages based on customizible criteria (source, handler, time of day,
     etc...)

   - customizable
     [formatters](https://docs.python.org/3/library/logging.html#formatter-objects)
     to control how a log message is being presented. (see also: 
     [log attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes))


## Implementation of basic logging functions

The built-in [`logging`][py-stdlib-logging] module is feature-rich, robust and
well-tested. `logging` has borrowed many ideas from the
[log4j](https://logging.apache.org/log4j/2.x/) product. 


**NOTE**: See [profiler.3](profiler.3) for the implemented solution!


### The requirements

1. Provide the following log messages:

   1. In case of an exception during the analysis of the directory structure emit an
      `error` message (meaning: the level *error* as defined in
      [`logging`][py-stdlib-logging]).

   2. Emit an `info` message when entering a directory to be processed. The message should
      mention the number of objects that have been analyzed so far.

   3. Each message should record the current timestamp (formatted in the ISO notation,
      e.g.: "2022-09-27T19:00:00"), error level and the message

2. The program should be able to log to the terminal (default) or a file.


3. Add the following CLI options to 

 `-l` or `--loglev` CLI option that will configure the threshold when to suppress
   or emit a message

   **NOTE**: the `logging` module has 5 different 
   [predefined levels](https://docs.python.org/3/library/logging.html#logging-levels) 
   to distinguish between the *urgency* of a message: `DEBUG`, `INFO`, `WARNING`, `ERROR`
   and `CRITICAL`


### Demo code

A **basic** logging [example][py-howto-logging]:

~~~python
{% include("logging-demo.py") %}
~~~
See also: [logging-demo.py](logging-demo.py)

**Example output**:

~~~bash
$ ./logging-demo.py
2022-09-27T02:04:38CEST WARNING (logging-demo:25) This is an WARNING level message
2022-09-27T02:04:38CEST ERROR (logging-demo:26) This is an ERROR level message
2022-09-27T02:04:38CEST CRITICAL (logging-demo:27) This is a CRITICAL level message
~~~

**NOTE**:

1. the `DEBUG` and `INFO` messages has been suppressed because of the provided `loglev`
   attribute in `basicConfig()`

1. the timestamp is displayed in the format as stated in requirement 1.3


### Actual implementation for `profiler`

**NOTE**: See [profiler.3](profiler.3) for the implemented solution!


### Verify requirements

1. support the CLI options `--loglev` and `--logfile`:

   ~~~bash
   $ ./profiler.3 --help
   ...
   positional arguments:
     DIR                   path to directory to analyze

   optional arguments:
     -h, --help            show this help message and exit
     --loglev {debug,info,warning,error,critical}
                           required log level (default: warning)
     --logfile LOGFILE     output the logs to this file (default: stderr)

   That's all folks!
   ~~~

1. Provide info messages when entering a directory **and** change the amount of emitted
   information with the `--loglev` option:

   ~~~bash
   $ ./profiler.3 --loglev=info  ../session09/exampledir/

   2022-09-27T19:48:53CEST INFO (profiler:127) Entering directory: ../session09/exampledir/
   2022-09-27T19:48:53CEST INFO (profiler:127) Entering directory: ../session09/exampledir/a
   2022-09-27T19:48:53CEST INFO (profiler:127) Entering directory: ../session09/exampledir/a/b
   2022-09-27T19:48:53CEST INFO (profiler:127) Entering directory: ../session09/exampledir/a/b/d
   2022-09-27T19:48:53CEST INFO (profiler:127) Entering directory: ../session09/exampledir/c
   2022-09-27T19:48:53CEST INFO (profiler:127) Entering directory: ../session09/exampledir/c/e
   --- Statistics of directory: ../session09/exampledir/
   Number of errors encountered while processing 0
   ...
   ~~~

1. Log to the terminal or a file:

   ~~~bash
   $ ./profiler.3 --loglev=info --logfile=profiler.3.log  ../session09/exampledir/
   --- Statistics of directory: ../session09/exampledir/
   Number of errors encountered while processing 0

   The number of dirs: 6
   The number of non-dirs (i.e.: files, hard- and symlinks): 8
   The number of symlinks: 1
   The number of hardlinks: 3
   Used disk space: 524 bytes
   Used disk space (corrected): 510 bytes
   Which of the hardlinks point to the same file?
     ../session09/exampledir/file1.dat, ../session09/exampledir/a/file2.bin, ../session09/exampledir/c/e/file15 : 7 bytes
   ~~~

   **NOTE**:

   1. Command same as above plus the `--logfile=profiler.log` option. Notice that there
      are no log messages (e.g.: "... INFO ...")

   1. The file `profiler.3.log` **does** contain those log messages:

      ~~~bash
      $ head -3 profiler.3.log  
      2022-09-27T19:51:04CEST INFO (profiler:127) Entering directory: ../session09/exampledir/
      2022-09-27T19:51:04CEST INFO (profiler:127) Entering directory: ../session09/exampledir/a
      2022-09-27T19:51:04CEST INFO (profiler:127) Entering directory: ../session09/exampledir/a/b
      ~~~

**NOTE**: See [profiler.3](profiler.3) for the implemented solution!





<!-- Links -->
[session09]: ../session09/README.md
[profiler]: ../session09/profiler
[hard-link]: https://en.wikipedia.org/wiki/Hard_link
[inode]: https://en.wikipedia.org/wiki/Inode
[list-comprehension]: https://pythongeeks.org/list-comprehensions-in-python/
[py-stdlib]: https://docs.python.org/3/library/
[py-stdlib-argparse]: https://docs.python.org/3/library/argparse.html
[py-stdlib-getopt]: https://docs.python.org/3/library/getopt.html
[py-howto-argparse]: https://docs.python.org/3/howto/argparse.html
[py-doctopt]: http://docopt.org/
[py-click]: https://click.palletsprojects.com/parameters/
[py-stdlib-logging]: https://docs.python.org/3/library/logging.html
[py-howto-logging]: https://docs.python.org/3/howto/logging.html

<script src="../assets/js/script.js" defer></script>

<!--
vim: filetype=markdown spelllang=en,nl spell foldmethod=marker lbr nolist ruler
vim: tw=90 wrap showbreak=… shiftwidth=3 tabstop=3 softtabstop=3 expandtab
-->
