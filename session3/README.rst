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

   git clone git@github.com:gnyers/python-tuesday.git


Install required modules
------------------------

This session uses several modules that are not part of the Python Stadard
Library. To install these modules execute:

.. code:: shell

   pip install --user -r requirements.txt


Working with Spreadsheets
=========================

.. contents:: Chapter contents
   :depth: 3
   :backlinks: entry
   :local:

Python modules
--------------

.

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

Add some data
^^^^^^^^^^^^^

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

   The 'Names' sheet now contains the CSV data.


Add some formatting
^^^^^^^^^^^^^^^^^^^

Formatting of cells can be done either directly or by applying a style. In
general using styles is preferable.

.. code:: python
   :number-lines: 37

   >>> from openpyxl.styles import NamedStyle, Font, Border
   >>> from openpyxl.styles.borders import Side
   >>> h1 = openpyxl.styles.NamedStyle(name='h1')

   ### Font style: bold, 18pt "Arial" of a nice color
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

   The first row of the "TimeReg" sheet has the custom style "h1"


Add comment
^^^^^^^^^^^

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


Showcase Application: Time sheet
================================

Requirements
------------



References
==========

.. [pymod_openpyxl] OpenPyXL is a Python library to read/write Excel 2010
   xlsx/xlsm/xltx/xltm files
   https://openpyxl.readthedocs.io/

.. [openpyxl_tutorial] 
   https://openpyxl.readthedocs.io/en/stable/tutorial.html


.. vim: filetype=rst tw=78 foldmethod=marker foldcolumn=3 wrap lbr nolist
.. vim: spelllang=en,nl spell showbreak=… ruler
