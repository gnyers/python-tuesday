======================================
Working with Data Part 1: Spreadsheets
======================================

-------------------------
Python Tuesday: Session 3
-------------------------

:date: 2019-09-24
:author: Gábor Nyers
:tags: python
:category: python_workshop
:summary: Reading and writing data to spreadsheets
:licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/


.. sectnum::
   :start: 1
   :suffix: .
   :depth: 2

.. contents:: Table of contents
   :depth: 2
   :backlinks: entry
   :local:


Introduction: Working with data Part 1: Spreadsheets
====================================================

Spreadsheets and databases permeate our business lives. Databases usually
contain structured data and often we use use dedicated applications to
interact with them. Spreadsheets are used to do ad-hoc processing or simply to
compensate for missing features of aforementioned applications.

This is Part 1 of a (potentially) series of sessions where we will focus on
how Python can be useful when dealing with spreadsheets. Our goal is to
live-code a simple Python application to read from- and write data to
spreadsheets.

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

This session's material
-----------------------

Visit this page: https://github.com/gnyers/python-tuesday/tree/master/session3

OR

Check out the Git repo:

.. code:: shell

   cd $PROJECTDIR
   git clone git@github.com:gnyers/python-tuesday.git

To follow along with the instructions please open the README.html in your
browser:

.. code:: shell

   firefox $PROJECTDIR/python-tuesday/session3/README.html


Requirements
------------

The code of this workshop has been tested with:

- Python v3.6 and
- the following modules that are not part of the Python Standard Library:

  - ``openpyxl``: module to read/write Excel 2010 workbooks (OOXML format)
  - ``ptpython``: a very conveniant Python interactive shell with support for
    in-line sytax highlighting, command completion and improved code editing
  
  To install these modules execute:

  .. code:: shell

     pip install --user -r requirements.txt


Working with Spreadsheets
=========================

.. contents:: Chapter contents
   :depth: 3
   :backlinks: entry
   :local:

This chapter will discuss the basics of working with Excel ``.xlsx`` files.


Python modules to deal with spreadsheets
----------------------------------------

Python provides numerous modules to deal with both Excel and LibreCalc
spreadsheets. Because LibreOffice support Python as macro language, users have
much more advanced capabilities. (See for more: [libreoffice_automation]_)

Therefore, in this workshop our focus is on dealing with Excel spreadsheets.
For this we have different options as wel: (Source: [PythonExcel]_)

- openpyxl: The recommended package for reading and writing Excel 2010 files
  (ie: .xlsx)

- xlsxwriter:  An alternative package for writing data, formatting information
  and, in particular, charts in the Excel 2010 format (ie: .xlsx)

- xlrd: This package is for reading data and formatting information from older
  Excel files (ie: .xls)

- xlwt: This package is for writing data and formatting information to older
  Excel files (ie: .xls)


Writing data to a spreadsheet
-----------------------------

Create a workbook
^^^^^^^^^^^^^^^^^

Following the openpyxl Tutorial ([openpyxl_tutorial]_) let's create
a spreadsheet in Excel 2010 format:

.. code:: python
   :number-lines: 1

   >>> import openpyxl
   >>> wb = openpyxl.Workbook()           # create a new workbook
   >>> ws1 = wb.active                    # get the active sheet
   >>> ws1.title = "MySheet"              # rename the current sheet

Create a new worksheet:

.. code:: python
   :number-lines: 5

   >>> ws2 = wb.create_sheet('TimeReg', 0)          # create a new sheet
   >>> ws2.sheet_properties.tabColor = "aa00bb"     # change tab color
   >>> ws1.sheet_properties.tabColor = "00bbaa"     # change the other sheet's color
   >>> wb.save('sandbox/test00.xlsx')               # save the workbook to file

..
   Resize a window with `xdotool`:
    sleep 2 && xdotool getactivewindow windowsize $(xdotool getwindowfocus) 720 400
   
   Screenshot with `xfce-screenshot`:
    sleep 2 && xfce4-screenshooter --window --save test-xlsx-01.png

The sheet now should look something like this:

.. figure:: images/test00-xlsx-01.png
   :target: sandbox/test00.xlsx
   :alt: A simple workbook created by openpyxl
   :align: center

   The spreadsheet created by the ``openpyxl`` module. Note the color of the
   worksheets.

Add data
^^^^^^^^

Now let's put some data into the sheet "TimeReg":

.. code:: python
   :number-lines: 9
   
   ### Get a sheet by its name
   >>> ws_tr = wb['TimeReg']

   ### Fill the first row with some data
   >>> for i in range(1, 11):
   ...     ws_tr.cell(row=1, column=i, value='Col{}'.format(i))
   ...
   ...                                    # doctest: +ELLIPSIS
   <Cell 'TimeReg'.A1>
   <Cell 'TimeReg'.B1>
   <Cell 'TimeReg'.C1>
   ...

   ### Save the workbook to file
   >>> wb.save('sandbox/test01.xlsx') 

The sheet now should look something like this:

.. figure:: images/test01-xlsx-01.png
   :target: sandbox/test01.xlsx
   :alt: Workbook with some data
   :align: center

   The "TimeReg" sheet now has some data.

Load data from a CSV file
^^^^^^^^^^^^^^^^^^^^^^^^^

Let's load the data from the ``names.csv`` file into our sheet. The content of
the file is as follows:

.. include:: ../session2/names.csv
   :number-lines: 1
   :code: ini

The code:

.. code:: python
   :number-lines: 20
 
   ### We'll read from a csv file
   >>> import csv
   >>> with open('../session2/names.csv') as fh:
   ...     data = list(csv.reader(fh, delimiter='|'))
   
   ### Add a new sheet 'Names' to load the data into
   >>> ws3 = wb.create_sheet('Names')

   ### Activate the new sheet when the workbook loads
   >>> wb.active = ws3
  
   ### Add data to sheet
   >>> for row in data: ws3.append(row)
   ...                                    # doctest: +ELLIPSIS

   ### Save the workbook to file
   >>> wb.save('sandbox/test02.xlsx') 

The result:

.. figure:: images/test02-xlsx-01.png
   :target: sandbox/test02.xlsx
   :alt: Workbook with some data
   :align: center

   The 'Names' sheet now contains the CSV data. Note: multiple columns appear
   as too narrow; this is 


Add formatting
^^^^^^^^^^^^^^

Formatting of cells can be done either directly or by applying a style. In
general using styles is preferable.

.. code:: python
   :number-lines: 37

   >>> from openpyxl.styles import NamedStyle, Font, Border
   >>> from openpyxl.styles.borders import Side
   >>> h1 = openpyxl.styles.NamedStyle(name='h1')

   ### Font style: bold, 18pt "Arial" of a nice color;
   >>> h1.font = Font('Arial', sz=18, b=True, color='aa00bb')

   ### Border style: 
   >>> b_med = Side(color='aa00bb', border_style='medium' )
   >>> h1.border = Border(bottom=b_med)

   ### Apply the style to the 1st row
   ### Note: numbering of cells starts with 1!
   >>> for i in range(1, 6):
   ...     ws3.cell(row=1, column=i).style = h1
   ...                                    # doctest: +ELLIPSIS
   >>> wb.save('sandbox/test05.xlsx')     # save the workbook to file

This will result in the following: 

.. figure:: images/test05-xlsx-01.png
   :target: sandbox/test05.xlsx
   :alt: Custom sytle
   :align: center

   The first row of the "TimeReg" sheet has the custom style "h1". Note that
   graphical design is not a primary concern at this point ;-)


Add comment
^^^^^^^^^^^

Comments can contain useful auxiliary information about a cell, such as
instructions to the user or ways to verify the correctness of the data.

.. code:: python
   :number-lines: 8

   >>> from openpyxl.comments import Comment
   >>> ws3['A1'].comment = Comment('Data imported from ``names.csv``', 'John Doe')
   >>> wb.save('sandbox/test06.xlsx')     # save the workbook to file

.. figure:: images/test06-xlsx-01.png
   :target: sandbox/test06.xlsx
   :alt: Comment added to cell "A1"
   :align: center

   The cell "A1" now contains a comment


Reading data from a spreadsheet
-------------------------------

Getting totals
^^^^^^^^^^^^^^

Our goal is to calculate the total number of billable and non-billable hours
based on the data of the following timesheet:

.. figure:: images/timesheet-xlsx-01.png
   :target: sandbox/timesheet.xlsx
   :alt: Comment added to cell "A1"
   :align: center

   Example timesheet containing data

First let's load the data from the spreadsheet:
*(Please type the following in an interactive Python session)*

.. code:: python
   :number-lines: 1

   ### load the ``openpyxl`` module
   >>> import openpyxl

   ### open the workbook
   >>> wb = openpyxl.load_workbook('sandbox/timesheet.xlsx')

   ### select the sheet containing the required data
   >>> ws = wb['TimeSheet']

   ### select the cells that contain the data; this obviously implies that you
   ### need to be familiar with the structure of the workbook
   >>> data_range = ws['A5:G40']

   ### let's retrieve the data with the following list comprehension
   >>> timesheet = [ [ cell.value  for cell in row  ]  for row in data_range ]
   >>> print(timesheet)                              # doctest: +ELLIPSIS
   [['Date', 'ProjectID', 'ActivityID', 'Billable Hours', 'Non-Billable Hours', 'RemarkPub', 'RemarkPriv'], [datetime.datetime(2019, 9, 1, 0, 0)...

We're now ready to calculate the total number of billable hours from the range
``'D5:D40'``:

.. code:: python
   :number-lines: 18

   ### select the cells which contain the billable hours
   >>> range_billable = ws['D5:D40']

   ### since the range is 2D data structure, we'll need a nested loop to
   ### process the data
   ###
   ### with the following list comprehension we create a list of hours
   >>> billable_hours = [ cell.value  for row in range_billable[1:]
   ...                                for cell in row if cell.value ]
   >>> print(billable_hours)
   [8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8, 5, 8, 8, 8, 8]

   ### the total of the billable hours
   >>> print(sum(billable_hours))
   156

In a similar manner, we'll calculate the total of non-billable hours based on
the data in the range ``'E5:E40'``:

.. code:: python
   :number-lines: 33

   >>> range_non_billable = ws['E5:E40']
   >>> non_billable_hours = [ cell.value  for row in range_non_billable[1:]
   ...                                    for cell in row if cell.value ]
   >>> print(non_billable_hours)
   [2, 3, 3, 3, 2, 2, 3, 3, 3, 2, 2, 3, 3, 3, 2, 2, 3, 3, 3, 2, 2]
   >>> total_non_billable = sum(non_billable_hours)
   >>> print(total_non_billable)
   54


Simple Analytics
^^^^^^^^^^^^^^^^

Suppose we're interested in the dates when the number of billable hours was
below 8:

.. code:: python
   :number-lines: 41

   >>> r = ws['A6:D40']

   ### Let's write up the query in a more understandable form
   ### NOTE: the <1>...<5> indicate the order in which Python executes the
   ###       statements
   >>> result = [
   ...  [ cell.value                   # <5> take the current cell's value
   ...    for cell in row[::3]         # <4> loop through the current row and 
   ...                                 #     take only elements w/ index 0 and 3
   ...  ]
   ...  for row in r                   # <1> loop through the data
   ...      if row[3].value            # <2> take only rows where the billable
   ...                                 #     hours are non-empty, and
   ...         and
   ...         row[3].value < 8        # <3> where the value is less than 8
   ... ]

   ### the ``result`` variable now points to a list of lists (2D list)
   ### of the days when the number of billable hours were < 8:
   >>> for d, h in result: print(d.strftime('%Y-%m-%d'), h)
   2019-09-03 5
   2019-09-10 5
   2019-09-17 5
   2019-09-24 5


Showcase Application: Time sheet
================================

Application Requirements
------------------------

#. Worksheet management of a given spreadsheet:

   #. list the sheets
   #. add sheet

#. Data management:

   #. dump the data on a sheet to the stdout
   #. append provided CSV data at the end of a sheet

#. CLI Interface: arguments as described above


Implementation prototype
------------------------

.. include:: ts-prototype.py
   :number-lines: 1
   :code: python


References
==========

.. [PythonExcel] http://www.python-excel.org/
.. [pymod_openpyxl] OpenPyXL is a Python library to read/write Excel 2010
   xlsx/xlsm/xltx/xltm files

   - source: https://bitbucket.org/openpyxl/openpyxl
   - documentation: https://openpyxl.readthedocs.io/
.. [openpyxl_tutorial] 
   https://openpyxl.readthedocs.io/en/stable/tutorial.html
.. [libreoffice_automation] Automate your office tasks with Python Macros
   http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html


.. vim: filetype=rst tw=78 foldmethod=marker foldcolumn=3 wrap lbr nolist
.. vim: spelllang=en,nl spell showbreak=… ruler
