# this file: j2_01.py

import jinja2 as j2     # load Jinja2 module, refer to its content as "j2.*"

template = '''
The list of kids and the show they appear:
{%- for character in kids %}
- {{ character }} appears in the show "{{ kids[character] }}".
{%- endfor %}
'''.strip()             # remove newlines from begin and end

kids = {
    "Chris": "Family Guy",
    "Pebbles": "The Flintstones",
    "Bart": "The Simpsons"
}
j2_tmpl = j2.Template(template)
out = j2_tmpl.render(kids=kids)
print(out)
