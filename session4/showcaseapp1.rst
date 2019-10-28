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


Usage
-----

Create a new database: ::

 $ ./timesheet.py --database timesheet.db create 
 Are you sure to delete all existing data? [y/N] y

Check the database file ``timesheet.db``: ::

 $ file timesheet.db
 timesheet.db: SQLite 3.x database, last written using SQLite version 3028000

Check the tables in the database: ::

 $ sqlite3 timesheet.db <<< .tables
 bookings  projects  users

Create a few new users: ::

 ./timesheet.py --database timesheet.db add-user -f John -s Doe -e jdoe@example.com
 New user added, id=1
 $ ./timesheet.py --database timesheet.db add-user -f Jane -s Brown -e jane.brown@example.com
 New user added, id=2
 $ ./timesheet.py --database timesheet.db add-user -f Frank -s Green -e frankg@example.com
 New user added, id=3
 $ ./timesheet.py --database timesheet.db add-user -f Eileen -s Smith -e eileeng@example.com
 New user added, id=4
 $ ./timesheet.py --database timesheet.db add-user -f George -s Moss -e moss@example.com
 New user added, id=5

Dump data from ``users`` as CSV and with headers: ::

 $ ./timesheet.py --database timesheet.db dump-table  --headers  -f csv  users
 id;fname;sname;email
 1;John;Doe;jdoe@example.com
 2;Jane;Brown;jane.brown@example.com
 3;Frank;Green;frankg@example.com
 4;Eileen;Smith;eileeng@example.com
 5;George;Moss;moss@example.com

Add a few projects: ::

 $ ./timesheet.py --database timesheet.db add-project --name "Project Roadrunner @ACMECo"
 New project added, id=1
 $ ./timesheet.py --database timesheet.db add-project --name "Webshop Implementation @ACMECo"
 New project added, id=2
 $ ./timesheet.py --database timesheet.db add-project --name "Security Audit @ACMECo"
 New project added, id=3

Dump data from ``projects``: ::

 $ ./timesheet.py --database timesheet.db dump-table projects
 1 "Project Roadrunner @ACMECo"
 2 "Webshop Implementation @ACMECo"
 3 "Security Audit @ACMECo"

Add a few bookings for user "Eileen Smith" (user ID: 4) for the projects
"Webshop Implementation @ACMECo" (project ID: 2) and
"Project Roadrunner @ACMECo" (project ID: 1): ::

 $ ./timesheet.py --database timesheet.db add-booking -u 4 -p 2 -d 2019-09-02 \
                  --hours 8 --remarks 'Landingpage design'
 New booking added, id=1
 $ ./timesheet.py --database timesheet.db add-booking -u 4 -p 2 -d 2019-09-03 \
                  --hours 6 --remarks 'Landingpage design'
 New booking added, id=2
 $ ./timesheet.py --database timesheet.db add-booking --user 4 --project 1 \
                   --date 2019-09-03 --hours 2 --remarks 'Requirement analysis'
 New booking added, id=3
 $ ./timesheet.py --database timesheet.db add-booking --user 4 --project 4 \
                  --date 2019-09-04 --hours 8 --remarks 'Verify inventory'
 New booking added, id=4
 $ ./timesheet.py --database timesheet.db add-booking --user=4 --project=1 \
                  --date=2019-09-05 --hours=2 --remarks='Planning review'
 New booking added, id=5

Dump data from ``bookings`` table as CSV, incl. headers. Note that the dump
contains data from multiple tables (using SQL ``JOIN`` s): ::

 $ ./timesheet.py --database timesheet.db dump-table --format=csv  --headers bookings
 booking_id;user_id;user_fname;user_sname;project_id;project_name;booking_date;booking_hours;booking_remarks
 1;4;Eileen;Smith;2;Webshop Implementation @ACMECo;2019-09-02;8;Landingpage design
 2;4;Eileen;Smith;2;Webshop Implementation @ACMECo;2019-09-03;6;Landingpage design
 3;4;Eileen;Smith;1;Project Roadrunner @ACMECo;2019-09-03;2;Requirement analysis
 5;4;Eileen;Smith;1;Project Roadrunner @ACMECo;2019-09-05;2;Planning review


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

  With ~60 lines of code (LoC) this is the largest function in this program.
  Parsing, interpreting and verifying CLI arguments is a complicated task,
  which is entirely taken care of by the ``argparse`` module from the Python
  Standard Library.

  The return value of this function is an object, which contains the function
  that needs to be executed and the validated input. The last line of the
  program ``arguments.func(connection, arguments)``, which 

  - will invoke the required function, stored in the `` arguments.func``
    attribute,
  - with all the collected input, i.e.: the other attributes of the
    ``arguments`` object. (e.g.: ``.first_name``, ``.surname``, ``.email``
    etc..)

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
- ``add_new_project``: add a new project record to the ``projects`` table
- ``add_new_booking``: add a new booking record tot the ``bookings`` table


.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
