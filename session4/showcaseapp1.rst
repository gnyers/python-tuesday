Showcase Application: Time sheet
================================

.. contents:: Contents:
   :depth: 2
   :backlinks: entry
   :local:

Features
--------

The time sheet application should be able to:

#. create a new time sheet database with a given schema
#. connect to an existing database
#. insert records in the tables ``users``, ``projects`` and ``bookings``, the
   values are provided on the command line, e.g.:

   - users:

   .. code:: shell
      :class: code

      ./timesheet.py --database /tmp/test.db add-user -f 'Fred' \
                     --surname 'Flintstone' -e 'fred.flintstone@bedrock.com'

   - projects:

   .. code:: shell
      :class: code

      ./timesheet.py --database /tmp/test.db add-project -n 'Slace Co. Crane Operator'

   - bookings: 

   .. code:: shell
      :class: code

      ./timesheet.py --database /tmp/test.db dump-table -H -f csv bookings

#. dump all records from the tables.
#. support (only) the SQLite database


Implementation decisions
------------------------

A few considerations with regards to the implementation:

#.  To keep the implementation simple:

    - limit error-checking and helpful suggestions to users
    - limit the capabilities of the program

#. Each action will be implemented by function

#. Make use of the ``argparse`` module to:

   - read and interpret CLI arguments
   - define the appropriate function to be executed

Implementation highlights
-------------------------

Usage example
^^^^^^^^^^^^^

The main help function of the ``timesheet.py`` application:

.. code:: shell
   :number-lines: 1
   :class: shell-code

   ./timesheet.py  -h
   usage: timesheet.py [-h] -d DATABASE
                       {create,verify,dump-table,add-user,add-project,add-booking}
                       ...

   positional arguments:
     {create,verify,dump-table,add-user,add-project,add-booking}
                           Commands
       create              Create the required schema
       verify              Verify if the required tables exist is correct
       dump-table          Dump table contents
       add-user            Add user record
       add-project         Add project record
       add-booking         Add booking record

   optional arguments:
     -h, --help            show this help message and exit
     -d DATABASE, --database DATABASE
                           The SQLite database

To get the function-specific help, execute the function with the ``-h`` or
``--help`` argument:

.. code:: shell
   :number-lines: 1
   :class: shell-code

   ./timesheet.py  add-booking -h
   usage: timesheet.py add-booking [-h] [-u USER] [-p PROJECT] [-d DATE]
                                   [-H HOURS] [-r REMARKS]

   optional arguments:
     -h, --help            show this help message and exit
     -u USER, --user USER  User ID
     -p PROJECT, --project PROJECT
                           Project ID
     -d DATE, --date DATE  The date of the booking (ISO format 2019-01-20)
     -H HOURS, --hours HOURS
                           The date of the booking
     -r REMARKS, --remarks REMARKS
                           A custom remark for this booking

The functions implemented
^^^^^^^^^^^^^^^^^^^^^^^^^

- ``parseargs``: CLI argument parsing function
- ``dbconnect``: create a connection object to a database
- ``sql_exec``: a generic SQL execution function, this function is used to run
  the appropriate SQL statement, that stands for a particular action, e.g.:
  add user, add project record, dump table data etc...
- ``create_schema``: create a blank SQLite database with the provided name
- ``dump_table``: a generic table data dumper function, supporting the TXT and
  CSV formats
- ``verify_tables``: a simple verification of the database validity by
  checking whether or not all the tables are there
- ``add_new_user``: add a new user record to the ``users`` table
- ``add_new_project``: add a new project record
- ``add_new_booking``: add a new booking record


.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
