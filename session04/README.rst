==============================================================
Working with Data Part 2: Introduction to Relational Databases
==============================================================

-------------------------
Python Tuesday: Session 4
-------------------------

:date: 2019-10-13
:author: Gábor Nyers
:tags: python
:category: python_workshop
:summary: Reading from and writing data to databases
:licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/

.. sectnum::
   :start: 1
   :suffix: .
   :depth: 2

.. contents:: Contents:
   :depth: 2
   :backlinks: entry
   :local:



Introduction
============

The topic of this workshop is to examine the many ways how we can interact
with **relational databases** from Python.

Relational databases are used for:

- **data storage abstraction**: Clear separation of application code and
  data for purposes of: concurrent access, performance, security etc...
- **structured data storage**: Relational database software enforces
  a predefined structure of the data (schema)
- **data storage and retrieval**: Relational databases typically use the
  "Structured Query Language" (see [SQLLang]_) to store and retrieve data from
  the database. SQL is a programming language with an English-like vocabulary.


Preparations
============

Earlier sessions
----------------

As we will build upon the previous topics, you might want to review the
earlier sessions:

- session 1: Getting your environment set up and ready for Python development
  https://github.com/gnyers/python-tuesday/tree/master/session1

- session 2: Working with text files and file formats
  https://github.com/gnyers/python-tuesday/tree/master/session2

- session 3: Working with data, part 1: spreadsheets
  https://github.com/gnyers/python-tuesday/tree/master/session3

This session's material
-----------------------

Visit this page: https://github.com/gnyers/python-tuesday/tree/master/session4

OR

Check out the Git repo:

.. code:: shell

   cd $PROJECTDIR
   git clone git@github.com:gnyers/python-tuesday.git

To follow along with the instructions please open the README.html in your
browser:

.. code:: shell

   firefox $PROJECTDIR/python-tuesday/session4/README.html

Requirements
------------

The code of this workshop has been tested with:

- Python v3.6 and
- the following modules that are not part of the Python Standard Library:

  - ``sqlite3``: module to read/write SQLite databases
  - ``ptpython``: a very convenient Python interactive shell with support for
    in-line sytax highlighting, command completion and improved code editing

  To install these modules execute:

  .. code:: shell

     pip install --user -r requirements.txt

Useful tools
------------

The following tools can help to deal with databases:

- Python DB CLI tools: ``litecli`` (SQLite), ``mycli`` (MariaDB) and ``pgcli``
  (PostgreSQL)

  To install these modules execute:

  .. code:: shell

     pip install --user -r requirements-dbcli.txt

- DBeaver: an open source GUI database tool for multiple databases:
  https://dbeaver.io/

- DBDesigner: an on-line database schema design tool
  https://www.dbdesigner.net/

The scope
=========

Like in most other programming languages, databases are a huge topic in Python
as well. So we'll need to restrict our scope.

Topics inside of the scope
--------------------------

- Working with relational databases, such as: SQLite, MariaDB / MySQL and
  PostgreSQL
- Required Python modules
- Connecting to a Database
- Create a database
- Create a table
- Insert data
- Query information
- Update data
- Delete data

Topics outside of the scope
---------------------------

The following topics are assumed to be known:

- Introduction to SQL (see [SQLLang]_)
- Discussion of the [ACID]_ considerations
- DB management basics using [MariaDB]_ or [PostgreSQL]_

These topics are related to databases, but not discussed in this session:

- Object-Relational Mapping (ORM) software, such as [SQLAlchemy]_,
  [DjangoORM]_, [PeeweeORM]_
- NoSQL databases, such as MongoDB, Redis


Concepts
========

Access to databases via DB API driver
-------------------------------------

Similar to other programming languages and applications, accessing databases
from Python will require some middleware. The different layers when accessing
a database:

.. class:: style2

   +-------------+------------------------------------+
   | Client side | Python Application                 |
   |             +------------------+-----------------+
   |             | DB-API driver    | Pure Python     |
   |             | (e.g. sqlite3,   | DB-API driver   |
   |             | mysql-connect)   |                 |
   |             +------------------+ (e.g.: PyMySQL) |
   |             | Native DB-API    |                 |
   |             | Driver           |                 |
   +-------------+------------------+-----------------+
   | Server side | Database Software (RDBMS)          |
   +-------------+------------------------------------+

This middleware needs to implement the specifications of DB API, which is
described in [PEP249]_. In general the responsibilities are the following:

- establishing a connection either through network, socket or some other
  mechanism.
- executing SQL statements
- fetching the results

Usually the Python database drivers are wrappers around existing (mostly C)
libraries. There are, however, a few exceptions that are completely written in
Python (e.g. PyMySQL)

The Python Wiki (see [PySupportedDBs]_) provides an overview of the database
products that have a Python database driver. A few examples: IBM DB2, Firebird
(and Interbase), Informix, Ingres, MariaDB / MySQL, Oracle, PostgreSQL, MaxDB,
Microsoft SQL Server, Microsoft Access, Sybase,

Database Cursor
---------------

A database cursor represents the results of some SQL transaction, which can be
fetched and manipulated from Python.

**Note:** a cursor is a snapshot of the state of the database at the end of
aforementioned SQL transaction. In case of multiuser/multithreaded database
products (i.e. the majority) this snapshot may not be up-to-date anymore, as
the consequence of the [ACID]_ requirements.


Working with SQL databases
==========================


The generic steps to interact with a SQL database
-------------------------------------------------

#. `Connect to the database <#connect-to-a-db>`_ using a DB API
   compatible driver

#. `Create a cursor object <#create-a-cursor>`_

#. `Construct a SQL statement <#construct-sql>`_

   The statement is often constructed by combining a template and some data,
   which is either provided by a user or acquired by Python some other way

#. Execute the SQL statement

   Submit the SQL statement to the database through the cursor object's
   ``.execute()`` method. The result is a cursor object.

#. Process the results by iterating through the cursor.


.. _connect-to-a-db:

Connect to a database
---------------------

SQlite
^^^^^^

Connect to a SQLite database represented by the file ``test.db``:

.. code:: python
   :number-lines: 1
   :class: python-interactive

   >>> import sqlite3
   >>>
   >>> conn1 = sqlite3.connect('test.db')

- **line 1:** load the ``sqlite3`` module
- **line 3:** create a connection object to the SQLite database in file
  ``test.db``

  **Note:** if the ``test.db`` database will be created automatically as an
  empty database if it did not exist.


MariaDB / MySQL
^^^^^^^^^^^^^^^

The below steps assume that the database server already has the user
``pyuser`` and the database ``pydb``. The ``pyuser`` has full privileges in
the ``pydb`` database.

The ``req-mariadb.sql`` script will create these requirements on the
database server:

.. code:: shell

   mysql -u root < req-mariadb.sql

To connect to a MariaDB database, we need a bit more information:

.. code:: python
   :number-lines: 1
   :class: python-interactive

   >>> import pymysql
   >>>
   >>> conn2 = pymysql.connect(host='localhost',
   ...                         db='pydb',
   ...                         user='pyuser',
   ...                         password='password')

- **line 1:** load the ``pymysql`` ([PyMySQL]_) module
- **line 3:** create a connection object to the MariaDB instance as user
  ``pyuser`` with the password ``password`` on the local system on the default
  port (3306) and using the usual defaults. Use the ``pydb`` database.

  For a complete list of arguments to the ``.connect()`` method see
  ``help(pymysql.connections.Connection)``


PostgreSQL
^^^^^^^^^^

The below steps assume that the database server already has the user
``pyuser`` and the database ``pydb``. The ``pyuser`` has full privileges in
the ``pydb`` database.

The ``req-postgresql.sql`` script will create these requirements on the
database server:

.. code:: shell

   sudo postgres psql < req-postgresql.sql


Connect to a PostgreSQL database:

.. code:: python
   :number-lines: 1
   :class: python-interactive

   >>> import psycopg2
   >>>
   >>> conn3 = psycopg2.connect(host='localhost',     # doctest: +SKIP
   ...                           database='pydb',
   ...                           user='pyuser',
   ...                           password='password')


.. _create-a-cursor:

Create a cursor object
----------------------

The cursor object will be used to submit SQL statements to the database and
retrieve the results.

Use of multiple cursor objects through the same connection is possible, but
keep in mind that the result of the same query may be different. This is
a consequence of the fact that cursors are different point-in-time snapshot of
the database.

Note the similarities in dealing with different databases! This is due to the
fact that the drivers implemented according the [PEP249]_ specifications.

SQLite
^^^^^^

.. code:: python
   :number-lines: 4
   :class: python-interactive

   >>> cur1 = conn1.cursor()
   >>> [ attr                          # new element of the list
   ...   for attr in dir(cur1)         # loop through the attributes of `cur1`
   ...   if not attr.startswith('__')  # only if attr does not start with '__'
   ... ]                               #     doctest:+NORMALIZE_WHITESPACE
   ['arraysize', 'close', 'connection', 'description', 'execute',
   'executemany', 'executescript', 'fetchall', 'fetchmany', 'fetchone',
   'lastrowid', 'row_factory', 'rowcount', 'setinputsizes', 'setoutputsize']

- **line 4:** create a cursor object, which can be used to submit SQL
  statements to the database
- **line 5:** get list of attributes of the cursor object:

  - data attributes: ``.arraysize``, ``.description``, ``.lastrowid``,
    ``.rowfactory``, ``.rowcount``
  - methods: ``.close()``, ``.execute()``, ``.executemany()``,
    ``.executescript()``, ``.fetchall()``, ``fetchmany()``, ``fetchone()``,
    ``.setinputsizes()``, ``.setoutputsize()``


MariaDB / MySQL
^^^^^^^^^^^^^^^

.. code:: python
   :number-lines: 7
   :class: python-interactive

   >>> cur2 = conn2.cursor()
   >>> [ attr 
   ...   for attr in dir(cur2)
   ...   if not attr.startswith('__')
   ... ]                               # doctest: +NORMALIZE_WHITESPACE
   ['DataError', 'DatabaseError', 'Error', 'IntegrityError', 'InterfaceError',
   'InternalError', 'NotSupportedError', 'OperationalError',
   'ProgrammingError', 'Warning', '_check_executed', '_clear_result',
   '_conv_row', '_defer_warnings', '_do_execute_many', '_do_get_result',
   '_ensure_bytes', '_escape_args', '_executed', '_get_db', '_nextset',
   '_query', '_result', '_rows', '_show_warnings', '_warnings_handled',
   'arraysize', 'callproc', 'close', 'connection', 'description', 'execute',
   'executemany', 'fetchall', 'fetchmany', 'fetchone', 'max_stmt_length',
   'mogrify', 'nextset', 'rowcount', 'rownumber', 'scroll', 'setinputsizes',
   'setoutputsizes']


- **line 7:** create a cursor object
- **line 8:** get a list of attributes of the cursor object.

  **Note:** that on a MariaDB cursor there much more attributes, but there are
  a few that are the same, i.e.: those that are specified by [PEP249]_


.. _construct-sql:

Construct the SQL Statement
---------------------------

Relational database products use the SQL language to query or change the data.
So this is what Python applications will need to do as well.

.. note:: direct SQL statements vs. ORM

   Python programmers often use an Object-Relational-Mapper (ORM) to interact
   with a database. In this approach the application programmer writes Python
   code and the ORM layer translates the instructions to SQL statements.

   In this session we're focusing on how to using SQL statements directly,
   which has the following pro's and con's:

   Benefits:

   - Since SQL is often understood by programmers, there is no need to learn
     the (otherwise non-trivial) ORM layer.
   - Database queries and transactions can be optimized by knowledgeable
     database administrators, who don't need to know Python.

   Drawbacks:

   - SQL dialects, i.e.: databases usually employ some extended version of
     SQL.  Changing an application to support a different or an additional
     database product may cost significant effort.
   - Maintaining or changing application functions may require additional
     database expertise.

SQL statements are strings
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Example 1:** Simplest SQL example: as-is

.. code:: python
   :number-lines: 1
   :class: python-interactive

   >>> create_tbl_users = '''
   ... CREATE TABLE users (
   ...    id INT AUTO_INCREMENT,
   ...    fname VARCHAR(40),
   ...    sname VARCHAR(60),
   ...    email VARCHAR(255),
   ...    PRIMARY KEY (id)
   ... );'''


SQL statements with string formatting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Example 2:** Make table name configurable with string formatting

.. code:: python
   :number-lines: 1
   :class: python-interactive

   >>> tblname = 'users'
   >>> create_tbl_users = '''CREATE TABLE {table_name} (
   ...    id INT AUTO_INCREMENT,
   ...    fname VARCHAR(40),
   ...    sname VARCHAR(60),
   ...    email VARCHAR(255),
   ...    PRIMARY KEY (id)
   ... );'''.format(table_name=tblname)


   >>> print(create_tbl_users)         # doctest: +NORMALIZE_WHITESPACE
   CREATE TABLE users (
      id INT AUTO_INCREMENT,
      fname VARCHAR(40),
      sname VARCHAR(60),
      email VARCHAR(255),
      PRIMARY KEY (id)
   );

- **line 1:** the ``tblname`` variable will hold the name of the table
- **lines 2-8:** using the ``.format()`` string method replace the
  ``table_name`` placeholder with the value of the ``tblname`` variable
- **line 11:** show the constructed SQL statement


SQL statements with parameter substitution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the most important considerations when constructing a SQL statement is
security. Since most applications work with user provided data, which
ultimately will end up as part of a SQL query, care must be taken to sanitize
the user input. (see also: [SQLInjection]_)

Part of the DB-API specification for database drivers is to provide
a parameter substitution. This facility is meant to take care of verifying
user input, to avoid "SQL Injection"-type attacks.

The concept of parameter substitution is very similar to how string formatting
works in Python.  Parameter style options as defined by [PEP249]_ for
executing SQL statements. Drivers may implement one or more of the following
syntax:

- "qmark" ``?``: ``statement = "SELECT * FROM users WHERE name=?"``
- "numeric" ``:1``: ``statement = "SELECT * FROM users WHERE name=:1"``
- "named" ``:name``: ``statement = "SELECT * FROM users WHERE name=:name"``
- "format" ``%s``: ``statement = "SELECT * FROM users WHERE name=%s"``
- "pyformat" ``%(name)s``: ``statement = "SELECT * FROM users WHERE name=%(name)s"``


**Example 3:** SQL statement to add a new user:

.. code:: python
   :number-lines: 1
   :class: python-interactive

   >>> sql_add_user = '''
   ... INSERT INTO users (fname, sname, email)
   ... VALUES (?, ?, ?);
   ... '''
   >>> cur1.execute(sql_add_user, ['John', 'Doe', 'jdoe@example.com'])

- **line 1-4:** the variable ``sql_add_user`` will contain the parametrized
  SQL statement as a ``str`` value
- **line 3:** the question marks (``?``) are the placeholders, which will be
  substituted by the driver with the verified parameters.
- **line 5:** execute the SQL statement by providing the parametrized SQL
  statement **and** the actual values **separately**.


Database differences
====================

Even though the SQL language is fairly standardized, there are plenty of
differences between the actual SQL commands. This problem is very hard to
solve, because 

Example: get information about a table

- SQLite:

  .. code:: python
     :class: python-interactive

     >>> cur1 = conn1.cursor()         # doctest: +SKIP
     >>> res = cur1.execute('PRAGMA table_info("users");') # doctest: +SKIP
     >>> list(cur1)                    # doctest: +SKIP
     [(0, 'id', 'int auto_increment', 0, None, 1),
      (1, 'fname', 'varchar(40)', 0, None, 0),
      (2, 'sname', 'varchar(60)', 0, None, 0),
      (3, 'email', 'varchar(255)', 0, None, 0)]

- MariaDB:

  .. code:: python
     :class: python-interactive

     >>> cur2 = conn2.cursor()               # doctest: +SKIP
     >>> res = cur2.execute('DESC users;')   # doctest: +SKIP
     >>> list(cur2)                          # doctest: +SKIP
     [('id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'),
      ('fname', 'varchar(40)', 'YES', '', None, ''),
      ('sname', 'varchar(60)', 'YES', '', None, ''),
      ('email', 'varchar(255)', 'YES', '', None, '')]


Note the differences:

#. the actual statement to execute:

   - SQLite: 'PRAGMA table_info("users");'
   - MariaDB: 'DESC users;'

#. the output:

   - records are numbered by SQLite, not numbered by MariaDB
   - the data types: 'int' in SQLite vs. 'int(11) in MariaDB

Database-independent Python applications
========================================

Despite the standardized way of accessing databases in Python and the widely
used SQL language, true database-independence is difficult. The root of this
problem is the different SQL dialects used- and the different features
provided by database products.

As Python programmers we can choose to deal with the diversity of SQL dialects
in our code, but maintaining these differences is almost always too heavy
a burden.

The usual way to man a Python application database-independent is by
implementing an additional layer of abstraction in the form of an [ORM]_


Other useful HOWTOs and tutorials
=================================

#. Python PostgreSQL Tutorial Using Psycopg2
   https://pynative.com/python-postgresql-tutorial/

#. Getting Started with MySQL in Python
   https://www.datacamp.com/community/tutorials/mysql-python

#. Python MySQL Tutorial Using MySQL Connector
   https://pynative.com/python-mysql-tutorial/



.. include:: showcaseapp1.rst


References
==========

.. [RelationalModel] 
   https://en.wikipedia.org/wiki/Relational_model
.. [SQL] https://en.wikipedia.org/wiki/SQL
.. [ACID] The abreviation of the terms Atomicity, Consistency, Isolation and
   Durability, which are the required properties of a database software to
   guaranty transactional safety. (https://en.wikipedia.org/wiki/ACID)
.. [MariaDB] MariaDB is an open source relational database softare. MariaDB is
   a fork of the MySQL database software. https://mariadb.com/
.. [PyMySQL] A pure Python client library for the MariaDB/MySQL databases
.. [PostgreSQL] PostgreSQL, is a free and open-source relational database
   management system (RDBMS) emphasizing extensibility and technical standards
   compliance.  (https://www.postgresql.org/)
.. [ORM] Object-relational Mapper is a library which allows full access to
   (relational) databases without requiring to write SQL statements.
   (https://www.fullstackpython.com/object-relational-mappers-orms.html)
.. [SQLAlchemy] Perhaps the most popular Python ORM (https://www.sqlalchemy.org/)
.. [DjangoORM] The built-in ORM of the Django web development framework
.. [PeeweeORM] https://docs.peewee-orm.com/
.. [PySupportedDBs] https://wiki.python.org/moin/DatabaseInterfaces
.. [DBProgInPython] https://wiki.python.org/moin/DatabaseProgramming
.. [PEP249] Python Database API Specification v2.0
   (https://www.python.org/dev/peps/pep-0249/)
.. [SQLLang] https://en.wikipedia.org/wiki/SQL
.. [SQLInjection] SQL Injection attacks are one of the most frequently used
   hacking technique. See: https://www.w3schools.com/sql/sql_injection.asp and
   https://en.wikipedia.org/wiki/SQL_injection



.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
