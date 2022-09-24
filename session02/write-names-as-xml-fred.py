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