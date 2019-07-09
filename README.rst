=========================
Python Tuesday: Session 1
=========================

----------------------------------------------------------------
Getting your environment set up and ready for Python development
----------------------------------------------------------------

:date: 2019-08-05
:author: Gábor Nyers
:tags: python
:category: python_workshop
:summary: The things you need to get started with developing in Python
:licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/

.. sectnum::
   :start: 1
   :suffix: .
   :depth: 2

.. contents:: Contents:
   :depth: 2
   :backlinks: entry
   :local:

Agenda
======

Setting up of your own development Python environment

#. Tools and settings:

   - Python distribution(s): vanilla python.org, Anaconda
   - Editors / IDEs: How to set up: Vim, VSCode, Spyder

#. Get started with some simple use-cases:

   - Installing, using and creating Python modules
   - Set up virtual environments
   - Using popular modules solve a handful of frequently occurring use-cases

**Source**: https://github.com/gnyers/python-tuesday-01 ::

 git clone git@github.com:gnyers/python-tuesday-01.git



Python distributions
====================

**What is a Python distribution?**

A software collection made available by the Python project or some other
organization to execute Python programs. It contains a Python run-time
environment, the Python `Standard Library`_ and (optionally) additional Python
modules.

**How many Python distros are there?**

The Python Wiki lists more than a dozen of `Python distributions`_, though
several of the pages are unavailable.

.. _Python distributions: https://wiki.python.org/moin/PythonDistributions

We will be discussing the two most well-known Python distributions:

- The official `Python distro <#part-vanilla-python>`_, and
- The `Anaconda product <#part-anaconda>`_


.. _part-vanilla-python:

The official Python distribution
--------------------------------

The canonical Python run-time environment developed, managed and distributed
by the `Python Software Foundation`_ the official custodian of the Python
programming language, its reference implementation and the well-known Python
trademark. To find out more visit the website at `<http://python.org>`_.

.. _Python Software Foundation: https://www.python.org/psf/
.. _Python: https://python.org
.. _CLI interpreter: https://docs.python.org/3/tutorial/interpreter.html
.. _IDLE: https://docs.python.org/3/library/idle.html
.. _Standard Library: https://docs.python.org/3/library/
.. _pip: https://pypi.org/project/pip/

It contains:

- Python `CLI interpreter`_, which is used for both **running programs** and for
  **interactive** work.
- The IDLE_ GUI interpreter, which can be used for interactive work.
- Required (binary) libraries
- The Python `Standard Library`_, which is mostly written in Python, but lower
  level operating system related functions are written in C.
- The official documentation of this minor version

  - The Language Reference
  - Standard Library 
  - Official HOWTO's and Tutorials
  - C-API documentation (extending Python itself, OR extending an application
    with Python!)

The official Python distribution does **not** contain:

- An editor or IDE
- Python modules not part of the official `Standard Library`_, such as:

  - ``setuptools_``: library and CLI tools to create distributable packages of
    Python modules
  - pip_: library and CLI tools to install 3rd party modules from PyPI_


.. _part-anaconda:

anaconda.com: A more rich Python distro
---------------------------------------

.. _Anaconda: https://www.anaconda.com/distribution/
.. _Anaconda download: https://www.anaconda.com/distribution/#download-section
.. _Anaconda Pkg List: https://docs.anaconda.com/anaconda/packages/pkg-docs/
.. _Anaconda Navigator: https://docs.continuum.io/anaconda/navigator/
.. _Spyder: https://www.spyder-ide.org/
.. _Anaconda Docs: https://docs.anaconda.com/anaconda/
.. _Conda: https://conda.io/en/latest/
.. _Conda Cheat Sheet: https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html


The Anaconda_ distribution is made up of the official Python distro and a list
of 1500+ selected Python modules. This product is aimed mainly at data science
and scientific computing customers and is being developed and managed by
a commercial company. While the product itself is completely open source, the
company provides commercial services around it.

Anaconda_ contains the following major components:

- The official Python_ distribution (both v2 and v3)
- `Anaconda Navigator`_: a convenient GUI application to start 
  Anaconda applications, manage virtual environments and search for- and
  update  modules.
- Conda_ package manager (a more advanced version of ``pip``)
- Some 1500+ Python modules (see `Anaconda Pkg List`_), of which ~200 are
  automatically installed.
- Spyder_, an open source IDE (Integrated Development Environment) specializing
  in scientific use-cases.
- `Jupyter Notebooks`_ and the IPython_ interpreter
- etc...

.. _Jupyter Notebooks: https://jupyter.org/
.. _IPython: https://ipython.org/

Further links to get started with Anaconda:

- `Anaconda download`_ page
- `Anaconda Docs`_
- `Conda Cheat Sheet`_

Which Python distribution to choose?
------------------------------------

Depending on you specific case there might be server consideration when
selecting a Python distribution:

- Download and Install size:

  - The official Python_ distribution is a few 10s of MB
  - The default installation of Anaconda_ is easily 10x that

- What kind of applications will you be developing:

  - For Scientific or data science scenario's Anaconda_ is well suited,
    because it provides most of the modules you'll need.
  - For generic Python development the official Python_ distribution is a good
    fit.

- The level of your Programming/Python knowledge:

  - To have everything work and get things done while needing to invest the
    least in Python knowledge, the Anaconda_ distribution provides a kind of
    one-stop-shop experience.

  - For more experience developers learning the details of the vanilla Python_
    environment is valuable knowledge.

Selecting and Setting-up an Editor/IDE
======================================

.. _VIM: https://vim.org
.. _Emacs: https://www.gnu.org/software/emacs/
.. _Geany: https://www.geany.org/
.. _Sublime: https://www.sublimetext.com/
.. _Atom: https://atom.io/
.. _VSCode: https://code.visualstudio.com/
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _PyDev: https://www.pydev.org/
.. _VisualStudio: https://visualstudio.microsoft.com/vs/

One of the most important tool when you developing software is the actual
application which you use to edit your code. This application goes by
different names, such as an "editor" or an "IDE" (Integrated Development
Environment). The difference between an editor and an IDE has to do with the
level of specialization the tool offers for the language.


- Generic editors, such as: VIM_ (**) or Emacs_ (**)
- Light-weight IDEs: Spyder_ (**), Sublime_ (*), Atom_ (**), Geany_ (**)
- Heavy-duty development environments, like: PyCharm_ (*), Eclipse's PyDev_ (**) or
  VisualStudio_ (*)

- Honorable mention: `Jupyter Notebooks`_ (**)

where:

- (*): Proprietary product
- (**): Open source project


A few important considerations for editor/IDE selection
-------------------------------------------------------

- Support for the Python syntax and best practices, i.e.: ``<Tab>`` to
  4x``<Space>`` coversion, auto-indentation

- Syntax Highlighting: colorize the code with multiple colors, which highlight
  different parts of the code, e.g.: comment, strings, reserved words
- Tab completion
- Variable overview: list of names of already defined variables, functions and
  class names.
- Snippets: inserting small pieces of often used code with a few key-strokes
- Automatically perform static code analytics: verify code quality with tools
  such as pep8_, pylint_, pyflakes_ , black_, mypy_

  Things as: unused, unrecognized or mistyped variables, usage of <Space>s,
  un-imported modules, etc...
- Terminal support, i.e.: ability to run the program being developed and watch
  its output
- Support for virtual environments (related to previous point)
- Is it possible to use your coding tool in a production environment?
- Support for refactoring: consistently renaming variables, function- or class
  names throughout a code base

.. _pep8: https://pypi.org/project/pep8/
.. _pylint: https://github.com/PyCQA/pylint
.. _pyflakes: https://github.com/pyflakes/pyflakes/
.. _black: https://github.com/python/black
.. _mypy: https://github.com/python/mypy

Resources on selection of an editor/IDE
---------------------------------------

- "Python IDEs and Code Editors (Guide)"
  https://realpython.com/python-ides-code-editors-guide/
- "Which Python static analysis tools should I use?"
  https://www.codacy.com/blog/which-python-static-analysis-tools-should-i-use/

Checklist: Getting started with Visual Code
-------------------------------------------

.. _Python extension for VSCode: https://marketplace.visualstudio.com/items?itemName=ms-python.python

Based on the "Getting Started with Python in VS Code" article above.

#. Download and install VSCode from https://code.visualstudio.com/Download
#. Install the "`Python extension for VSCode`_" by Microsoft using
   the built-in package manager
#. Select your Python interpreter: 

   #. Activate the Command Palette with the keystroke ``<Ctrl>+<Shift>+P``
   #. Start typing "Select Python Interpreter", which should automatically
      discover the installed Python run-time.
#. Create a new ``helloworld`` application and run it by right-clicking on the
   code and selecting the "Run Python File in Terminal"

Further read:

- "Getting Started with Python in VS Code"
  https://code.visualstudio.com/docs/python/python-tutorial

Checklist: Getting started with VIM
-----------------------------------

.. _Vundle: https://github.com/VundleVim/Vundle.vim

VIM_ is famous (or infamous) of its steep learning curve, yet it still has
a huge number of users. So there must be something to it, right? Anyway,
regardless if you're an experienced VIM person, or just curious about the
fuss, this is how to get started with Python development in VIM. It is a more
involved process that getting started with VSCode, yet people seem to thing
it's worth the effort.

#. Download and Install VIM_
#. Install a plug-in manager for VIM, such as Vundle_
#. Follow one of the more detailed guides below.

Further read:

- "VIM and Python – A Match Made in Heaven"
  https://realpython.com/vim-and-python-a-match-made-in-heaven/
- Setting up VIM as an IDE for Python
  https://medium.com/@hanspinckaers/setting-up-vim-as-an-ide-for-python-773722142d1d


Python Modules
==============

Typically there are 3 types of modules you'll need to work with on a daily
bases:

- Modules of the `Standard Library`_
- Modules which are part of the application being developed
- 3rd party modules, e.g. available in PyPI_ or `Anaconda Repository`_.

The availability of the first two are trivial, but finding and installing 3rd
party modules is a concern.

Installing 3rd Party Python modules
-----------------------------------

.. _PyPI: https://pypi.python.org
.. _Anaconda Repository: https://repo.continuum.io/
.. _pipenv: https://docs.pipenv.org/en/latest/

There are several sources of to install Python modules from, such as:

- PyPI_: the Python Package Index, which is the official 3rd party repository.
  The site is managed by the `Python Software Foundation`_.
- `Anaconda Repository_`: the repository managed by Anaconda, the commercial
  entity behind the Python distro of the same name.

Tools to manage 3rd party modules:

- pip_: the de-facto module management tool.
- conda_: a much more sophisticated manager for modules developed primarily
  for the Anaconda_ Python distribution
- pipenv_: similarly sophisticated capabilities as conda_, but generic

Shared features:

- basic package management: searching, downloading, installing, up- and
  downgrading and removing of modules.
- support for the several different Python package formats (i.e.: the
  distributable, (usually) platform-independent archive containing stuff
  needed to install or compile a module

Differences:

- ``pipenv`` and ``conda`` can do everything ``pip`` can, with support of more
  sophisticated dependency management and security
- ``pipenv`` and ``conda`` manage Python virtual environments, ``pip`` does
  not.

Installing modules
^^^^^^^^^^^^^^^^^^

Let's install the ``requests`` module using ``pip``: ::

 $ pip install requests
 Collecting requests
   Downloading https://files.pythonhosted.org/packages/...
     100% |████████████████████████████████| 61kB 2.1MB/s
 Collecting idna<2.9,>=2.5 (from requests)
   Downloading https://files.pythonhosted.org/packages/...
     100% |████████████████████████████████| 61kB 4.0MB/s
 Collecting certifi>=2017.4.17 (from requests)
   Downloading https://files.pythonhosted.org/packages/...
     100% |████████████████████████████████| 163kB 1.9MB/s
 Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests)
   Downloading https://files.pythonhosted.org/packages/...
     100% |████████████████████████████████| 153kB 3.4MB/s
 Collecting chardet<3.1.0,>=3.0.2 (from requests)
   Downloading https://files.pythonhosted.org/packages/...
     100% |████████████████████████████████| 143kB 2.4MB/s
 Installing collected packages: idna, certifi, urllib3, chardet, requests
 Successfully installed certifi-2019.6.16 chardet-3.0.4 idna-2.8 requests-2.22.0 urllib3-1.25.3
 You are using pip version 9.0.3, however version 19.1.1 is available.
 You should consider upgrading via the 'pip install --upgrade pip' command.

What just happened:

- ``pip`` has downloaded the archive containing the ``requests`` module
- based on information in the archive, it then (recursively) downloaded all
  other required modules the current one depends on.
- once all required packages are downloaded it installed them
- thrown a warning about our outdated version of ``pip``

Get a list of installed modules: ::

 $ pip list
 certifi (2019.6.16)
 chardet (3.0.4)
 idna (2.8)
 pip (9.0.3)
 requests (2.22.0)
 setuptools (39.0.1)
 urllib3 (1.25.3)
 You are using pip version 9.0.3, however version 19.1.1 is available.
 You should consider upgrading via the 'pip install --upgrade pip' command.

Now let's get rid of those annoying warnings about ``pip``'s version by
updating it: ::

 $ pip install --upgrade pip
 Cache entry deserialization failed, entry ignored
 Collecting pip
   Downloading https://files.pythonhosted.org/packages/.../pip-19.1.1-py2.py3-none-any.whl (1.4MB)
     100% |████████████████████████████████| 1.4MB 528kB/s 
 Installing collected packages: pip
   Found existing installation: pip 9.0.3
     Uninstalling pip-9.0.3:
       Successfully uninstalled pip-9.0.3
 Successfully installed pip-19.1.1

Warnings are gone; also note how the latest version presents the same
information as above: ::

 $ pip list
 Package    Version
 ---------- ---------
 certifi    2019.6.16
 chardet    3.0.4
 clipboard  0.0.4
 idna       2.8
 pip        19.1.1
 pyperclip  1.7.0
 requests   2.22.0
 setuptools 39.0.1
 urllib3    1.25.3



Python Virtual Environments
---------------------------

Python Virtual Environment:
    Used run conflicting Python applications, in terms of modules, module
    versions or even interpreter versions. For this reason they need to be
    isolated from one another. It is a best practice to develop each
    application in its own virtual environment.

Consider the following:

- A virtual environment (or **venv**) is very simple and very light-weight
  isolation mechanism to allow the use of conflicting modules or even
  different Python major (and minor) versions.
- Please note that this technique has nothing to do with virtualization (such
  as VMware, VirtualBox or KVM) nor containers create by such tools as
  ``LXC``, ``Docker`` or ``systemd-nspawn``.
- Python virtual environments are "just" a separate sets of directories and
  appropriate environment variables resulting in a separate Python run-time
  environment.
- If the same module is used in multiple ``venv``'s, it needs to be installed
  multiple times.


Create a virtual environment
----------------------------

A ``venv`` can be created manually or programmatically (i.e. from code).

To manually create a ``venv`` execute the following steps:

#. Create a directory which will be the ``root`` of the ``venv``. ::

    mkdir -p ~/.virtualenvs/devenv

#. Populate the ``root`` directory: ::

    python3 -m venv ~/.virtualenvs/devenv


Working with Virtual Environments
---------------------------------

Every time you want to use a ``venv`` you need to activate it either
interactively or as a batch process during the startup of an application.

Use a ``venv`` interactively or with VIM_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Activate the ``venv`` from a directory

   On Linux or MacOS X, if ``venv`` is installed in ``~/.virtualenvs/devenv``:
   ::

    source ~/.virtualenvs/devenv/bin/activate

   On Windows, from dir : ::

    C:/temp/devenv/bin/activate.bat

   This will change the prompt to show the name of the active Python ``venv``,
   e.g.: ::

    (devenv) user@host $

#. Above script will modify environmental variables such that when typing
   ``python``, the interpreter, the libraries and modules in the ``venv`` will
   be used.

   **Note:** These settings are temporary and only active in the current session!
   #If the session is closed, you'll need to re-activate.

#. Run your Python application the usual way: ::

    $ python myprogram.ph

   **Note:** you don't need to specify explicitly ``python3``, because the
   python interpreter of the ``venv`` will be the first the OS founds.

#. To de-activate the ``venv`` and restore the system-wide Python settings
   simply execute: ::

    deactivate

Further read:

- The Official Python tutorial "Virtual Environments and Packages"
  https://docs.python.org/3/tutorial/venv.html
- "Managing environments" - Anaconda documentation
  https://docs.anaconda.com/anaconda/navigator/tutorials/manage-environments/


Setup VSCode_ to use ``venv``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please note that VSCode_ will automatically discover Python environments of the
following types:

- system wide Python environments
- virtual environments located in any of the following special directories:

  - $HOME/.virtualenvs
  - $HOME/.pyenv
  - $HOME/Envs

In case you'd like to use an environment from a non-standard location use the
following steps:

#. Start VSCode
#. Open your project
#. Edit your settings by selecting ``File`` -> ``Preferences`` -> ``Settings``
   menus. This will open a new tab titled: "Settings"

   or hitting the ``<Ctrl> + ,`` (comma) keystroke

#. In the "Search" field type: ``venv`` and find the "Python: Venv Folder"
   parameter.
#. Add the parent folder containing the root of your virtual environment.

   For example: if you've created a virtual environment using: ::

    mkdir /tmp/myenv && python3 -m venv /tmp/myenv

   You will need to add the ``/tmp`` directory to the ``python.venvPath``
   VSCode parameter. (btw: this will be stored in the
   ``~/.config/Code/User/settings.json`` file.

#. After this select the correct environment using the Command Palette ->
   "Select Python Interpreter" action.

#. Restart any VSCode terminal to propagate these changes and use the correct
   interpreter when executing your Python code.






.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
