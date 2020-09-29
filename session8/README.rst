.. Fancy RST roles, needs rst2html-fancy.css

.. role:: tst
   :class: test
.. role:: file(code)
.. role:: dir(code)
.. role:: key(code)
.. role:: cmd(code)
.. role:: url(code)

.. role:: var(code)
.. role:: type(code)
.. role:: func(code)
.. role:: class(code)
.. role:: mod(code)

.. role:: git(code)
.. role:: commit(code)
.. role:: tag(code)
.. role:: bug(code)

.. role:: app(code)
.. role:: user(code)
.. role:: dottedline(code)
.. role:: verticalspace(code)


.. Abbreviations
.. =============

.. |ANSWER| replace:: **Answer/Solution:**

.. |GIT| replace:: :app:`Git`
.. |PYTHON| replace:: :app:`Python`


.. |DOTTEDLINE| replace:: :dottedline:`✎`




================================================================================
Creating classes easily with the ``dataclasses`` module
================================================================================

--------------------------------------------------------------------------------
Python Tuesday: Session 8
--------------------------------------------------------------------------------

:date: 2020-09-29
:author: Gábor Nyers
:tags: python
:category: python_workshop
:summary: The Iterator protocol and its practical uses
:licence: CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/

.. sectnum::
   :start: 1
   :suffix: .
   :depth: 2

.. contents:: Contents:
   :depth: 2
   :backlinks: entry
   :local:

Abstract
================================================================================

The ``dataclasses`` module introduced in Python 3.7. This relatively new
addition to the Python Standard Library provides an easy and standardized way
to create new classes to represent data types required for applications. This
module is similar in purpose to the `collections` module's `namedtuple` class,
but with much more capabilities.



Agenda
================================================================================

- Introduction
- Simple use cases

Introduction
================================================================================


What is it?
--------------------------------------------------------------------------------

The ``dataclasses`` module is a modern code-generator that is part of the
Standard Library of Python 3.7 and above.

Side-step: Code generators (and why should you care?)

  In general people use code generators to **easily** create larger pieces of
  program code **based on specifications**.

  A comparison can be made between:

  - carefully hand-crafted code by an expert programmer, which is
    purpose-built, optimized, maintainable and perfectly fits the given
    use-case, versus

  - a "good enough" solution, where code is being generated automatically
    based on a few parameters. These components fit the typical use-case well
    most of the time and it can be maintained with reasonable effort by
    non-experts.

  Good code generators have an added value because they allow beginner- or
  intermediate programmers to quickly create "good-enough" components.


What is it good for?
--------------------------------------------------------------------------------

Simplifies the creation of Python classes that can be created using
a compact notation, yet observe current best-practices.


Typically ``classes`` are used for two purposes:

- to keep different pieces of data together (data-holder)
- classes to focus on "business-logic"


Example with ``dataclasses``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Declare a new class: ::

 >>> from dataclasses import dataclass
 >>> @dataclass
 ... class Contact:
 ...     fname: str
 ...     sname: str
 ...     email: str

Create a new instance: ::

 >>> jdoe = Contact('John', 'Doe', 1980)

Show the new instance: (notice the nice ``__repr__()`` method?) ::

 >>> jdoe
 Contact(fname='John', sname='Doe', birthyear=1980)

Compare two instances that are equal: ::

 >>> jdoe2 = Contact('John', 'Doe', 1980)
 >>> jdoe == jdoe2
 True

Compare two instances that are not equal: ::

 >>> jdoe3 = Contact('John', 'Doe', 1983)
 >>> jdoe == jdoe3
 False


Example without ``dataclasses``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The equivalent code for the above would be: ::

 >>> class Contact:
 ...     def __init__(self, fname, sname, email):
 ...         self.fname = fname
 ...         self.sname = sname
 ...         self.email = email
 ...     def __repr__(self):
 ...         tmpl = "Contact(fname='{}', sname='{}', email='{}')"
 ...         return tmpl.format(self.fname,
 ...                            self.sname,
 ...                            self.email)
 ...     def __eq__(self, other):
 ...         if other.__class__ is not self.__class__:
 ...             return NotImplemented
 ...         return (self.fname, self.sname, self.email) == \
 ...                (other.fname, other.sname, other.email)

- lesser readability
- lots of "boilerplate" code: code that is necessary and usually simple but
  repetitive
- more opportunities for bugs to seep in


Who is it meant for?
--------------------------------------------------------------------------------

General purpose module intended for programmers of all skill-level who wish to
spend less time on "boilerplate" code (i.e.: the usual instance methods that
are required for most classes: ``__init__()``, ``__repr__()``, ``__eq__()``,
etc...


Availability?
--------------------------------------------------------------------------------

- Python v3.6 (backport, run ``pip install dataclasses``)
- Python v3.7 native


``dataclasses`` is modern
--------------------------------------------------------------------------------

The ``dataclasses`` module is using `type annotations
<https://docs.python.org/3/library/typing.html>`_ to provide type hints


Other similar modules
--------------------------------------------------------------------------------

- ``collections.NamedTuple`` of the Python Standard Library: a tuple, that
  bundles different pieced together, and have attributes ("names") to refer to
  these

- ``attrs`` 3rd party module: can be viewed as the inspiration for
  ``dataclasses``


Demonstration of ``dataclasses``
================================================================================


Attributes with default values
--------------------------------------------------------------------------------

Create a class that has a few attributes with default values: ::

 >>> from dataclasses import dataclass
 >>> @dataclass
 ... class Contact:
 ...     fname: str
 ...     sname: str = ''
 ...     email: str = ''


Create new instance and display it: ::

 >>> jdoe = Contact('John')

 >>> jdoe
 Contact(fname='John', sname='', email='')


- attribute ``fname`` is mandatory
- attributes ``sname`` and ``email`` have a default value, hence optional


Container class
--------------------------------------------------------------------------------

The following class:

- may contain elements (subclassed from ``List``), and
- has an attribute (``date_created``) with default value that is not a static
  value (or is it?)

::

 >>> from time import localtime
 >>> from dataclasses import dataclass
 >>> from typing import List

 >>> @dataclass
 ... class Addressbook(List):
 ...     name: str
 ...     owner: Contact = None
 ...     date_created: localtime =  localtime()

Test it: ::

 >>> ab = Addressbook('My Addressbook')

Let's add a few elements: ::

 >>> janedoe = Contact('Jane', 'Doe', 'jane.doe@example.com')
 >>> ab.extend([jdoe, janedoe])

 >>> ab
 Addressbook(name='MyAddressBook', owner=None, date_created=time.struct_time(tm_year=2020, tm_mon=9, tm_mday=25, tm_hour=13, tm_min=28, tm_sec=52, tm_wday=1, tm_yday=273, tm_isdst=1))

**Verify** that the attribute ``date_created`` is indeed dynamic:

Create a new ``Addressbook``: ::

 >>> ab2 = Addressbook('TestAB')
 >>> ab2
 Addressbook(name='TestAB', owner=None, date_created=time.struct_time(2020, 9, 26, 13, 49, 34, 997024))


**Conclusion**: the attribute ``date_created`` is the same for instances ``ab`` and
``ab2``! Conclusion: the ``localtime()`` value is generated **once** at the
time of the creation of the class, and not **every time**
a new instance is created!


Improved dynamic default values with a ``default_factory``
--------------------------------------------------------------------------------

Improve the above example with a truly dynamic default value: ::

 from time import localtime
 from dataclasses import dataclass, field
 from typing import List

 @dataclass
 class Addressbook(List):
     name: str
     owner: Contact = None
     date_created: localtime = field(default_factory=localtime)


**Verify**: ::

 >>> ab = Addressbook('MyAddressBook')
  Addressbook(name='MyAddressBook', owner=None, date_created=time.struct_time(2020, 9, 26, 14, 0, 44, 427232))


 >>> ab2 = Addressbook('TestAB')
 >>> ab2
 Addressbook(name='TestAB', owner=None, date_created=time.struct_time(2020, 9, 26, 14, 1, 2, 752333))

**Conclusion**:

The timestamps of ``ab`` and ``ab2`` are different!


Immutable classes
--------------------------------------------------------------------------------

Immutability is often a desired trait of an object in order to have certainty
that the data will not be changed when the object is passed on to e.g. some
function.

**Problem**:

The current implementation of ``Contact`` can be changed: ::

 >>> jdoe.fname = 'Jonny'
 >>> jdoe
 Contact(fname='Jonny', sname='Doe', email='jdoe@example.com'


**Solution**:

Update the definition of the class ``Contact`` to be immutable: ::

 >>>  @dataclass(frozen=True)
 ...  class Contact:
 ...      fname: str
 ...      sname: str = ''
 ...      email: str = ''


**Verify**: ::

 >>> jdoe
 Contact(fname='John', sname='Doe', email='jdoe@example.com')

 >>> jdoe.fname = 'Jonny'
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "<string>", line 3, in __setattr__
 dataclasses.FrozenInstanceError: cannot assign to field 'fname'


**Conclusion**:

Using the ``@dataclass(frozen=True)`` decorator, the class is immutable!


Sorting of objects
--------------------------------------------------------------------------------

In this example we'll see how ``dataclasses`` allow the sorting of objects.

**Problem**:

In an earlier example we added two ``Contact`` instances to our ``Addressbook``::

 >>> ab
 Addressbook(name='MyAddressBook', owner=None, date_created=time.struct_time(2020, 9, 26, 14, 0, 44, 427232))


Let's try to sort the address book: ::

 >>> sorted(ab)
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
 TypeError: '<' not supported between instances of 'Contact' and 'Contact'

The above error message informs that Python does not "know" how to determine
which of the instances of the ``Contact`` class is considered "larger" or
"smaller".

Normally Python provides the following four "magic methods" for a class to
implement:

- ``__lt__()``, used when comparing object, e.g.: ::

   jdoe < janedoe

  Python executes: ::

   Contact.__lt__(jdoe, janedoe)

- ``__le__()``, e.g.: ``jdoe <= janedoe``
- ``__gt__()``, e.g.: ``jdoe > janedoe``
- ``__ge__()``, e.g.: ``jdoe >= janedoe``


**Solution**:

Add the ``order=True`` argument to the decorator in order for ``dataclasses``
to implement the above "magic methods": ::

 >>>  @dataclass(frozen=True, order=True)
 ...  class Contact:
 ...      fname: str
 ...      sname: str = ''
 ...      email: str = ''


**Verify**: ::

  >>> ab
  Addressbook(name='MyAddressBook', owner=None, date_created=time.struct_time(2020, 9, 26, 13, 49, 34, 997024))


  >>> sorted(ab)
  [Contact(fname='Jane', sname='Doe', email='jane.doe@example.com'), Contact(fname='John', sname='Doe', email='jdoe@example.com')]


**Conclusion**:

Using the ``@dataclass(order=True)`` decorator, the instances of a class can
be "compared" amongst themselves.

**IMPORTANT**: The default comparison implemented by ``dataclass`` decorator
relies on tuple comparison, that is:

- take the data attributes of both the instances in the order that they have
  been declared, e.g.: ::

   Contact(fname='Jane', sname='Doe', email='jane.doe@example.com')
   Contact(fname='John', sname='Doe', email='jdoe@example.com')

- put them in a tuple, e.g.: ::

   ('Jane', 'Doe', 'jane.doe@example.com')

   ('John', 'Doe', 'jdoe@example.com')

- compare them: ::

   ('Jane', 'Doe', 'jane.doe@example.com') < ('John', 'Doe', 'jdoe@example.com')

In the above example the attribute ``fname`` will effectively determine the
sorting order.

In case other ordering is needed, the options are as follows:

- change the order of the attributes in the class definition, e.g. swap the
  ``fname`` and ``sname`` attributes: ::

   >>>  @dataclass(frozen=True, order=True)
   ...  class Contact:
   ...      sname: str
   ...      fname: str = ''
   ...      email: str = ''

- or implement the ``__lt__()`` (etc...) methods as desired: ::

   >>>  @dataclass(frozen=True)
   ...  class Contact:
   ...      fname: str
   ...      sname: str = ''
   ...      email: str = ''
   ...
   ...      def __lt__(self, other):
   ...         if other.__class__ is not self.__class__:
   ...             return NotImplemented
   ...          return self.sname < other.sname

  NOTE that in this case the ``order=True`` argument has no effect on the
  ``dataclass`` decorator's working.


Data serialization with ``asdict()`` and ``astuple()``
--------------------------------------------------------------------------------


The ``dataclasses`` module provides the functions ``asdict()`` and
``astuple``, which may be used to convert a ``dataclass`` object into
a ``dict`` or a ``tuple``. Using these functions it is easy to:

- *"export"* (*"serialize"*) an object to a file, or
- *"import"* (*"de-serialize"*) the content of a file and re-create the object


**Challenge**:

Implement a function to export an ``Addressbook`` instance complete with its
content in ``JSON`` format: ::

 '{"name": "MyAddressBook",
   "owner": null,
   "date_created": [2020, 9, 25, 13, 28, 52, 1, 273, 1],
   "_contacts": [
      {"fname": "John", "sname": "Doe", "email": "jdoe@example.com"},
      {"fname": "Jane", "sname": "Doe", "email": "jane.doe@example.com"}
   ]}'


**Problem**:

The relatively simple ``Contact`` class works well with both ``asdict()`` and
``astuple()``, the ``Addressbook`` class does not:

- ``Contact`` is OK:

  Import the functions ``asdict()`` and ``astuple``: ::

   >>> from dataclasses import asdict, astuple

  Object as ``dict``: ::

   >>> asdict(jdoe)
   {'fname': 'John', 'sname': 'Doe', 'email': 'jdoe@example.com'}

  Object as ``tuple``: ::

   >>> astuple(janedoe)
   ('Jane', 'Doe', 'jane.doe@example.com')

- ``Addressbook`` misses data: ::

   >>> asdict(ab)
   {'name': 'MyAddressBook', 'owner': None, 'date_created': time.struct_time(tm_year=2020, tm_mon=9, tm_mday=25, tm_hour=13, tm_min=28, tm_sec=52, tm_wday=1, tm_yday=273, tm_isdst=1)}

   >>> astuple(ab)
   ('MyAddressBook', None, time.struct_time(tm_year=2020, tm_mon=9, tm_mday=25, tm_hour=13, tm_min=28, tm_sec=52, tm_wday=1, tm_yday=273, tm_isdst=1))


**Solution**:

We need to create a custom function to export the content of an
``Addressbook`` instance as well: ::

 >>> import json
 >>> from dataclasses import asdict, astuple

 >>> def export_addressbook(ab):
 ...     d = asdict(ab)
 ...     d['_contacts'] = [ asdict(c) for c in ab ]
 ...     return json.dumps(d)




References
================================================================================

Web pages:

- PEP-557: Data Classes
  https://www.python.org/dev/peps/pep-0557/

- Data Classes development @GitHub:
  https://github.com/ericvsmith/dataclasses

- Typing
  https://docs.python.org/3/library/typing.html


Video's:

- Dataclasses: The code generator to end all code generators - PyCon 2018
  keynote, Raymond Hettinger
  https://www.youtube.com/watch?v=T-TwcmT6Rcw

- Data Classes in Python: Why They're Great, Tal Einat - PyCon IL 2019
  https://www.youtube.com/watch?v=Udz4jjd46ho

- Data Classes in Python 3.6 and beyond, Alexander Hultnér
  https://www.youtube.com/watch?v=nwjWOaxWMes




.. vim: filetype=rst textwidth=78 foldmethod=syntax foldcolumn=3 wrap
.. vim: linebreak ruler spell spelllang=en showbreak=… shiftwidth=3 tabstop=3
