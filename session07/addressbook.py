from dataclasses import dataclass, field
from typing import List
from collections import Counter

@dataclass
class Person:
    fname: str = ''
    sname: str = ''
    gender: str = ''
    email: str = ''

    def __getitem__(self, item):
       res = getattr(self, item)
       return res

@dataclass
class Addressbook:
    name: str = 'My Addressbook'
    _items: List[Person] = field(default_factory=list, init=False)

    def __iter__(self):
        return iter(self._items)

    def add(self, person):
        self._items.append(person)

    def __len__(self):
        return len(self._items)

fred = Person(fname='Fred', sname='Flintstone', gender='m',
          email='fred@bedrock.place')
wilma = Person(fname='Wilma', sname='Flintstone', gender='f',
           email='wilma@bedrock.place')
ab = Addressbook(name='The Flintstones')
ab.add(fred)
ab.add(wilma)

gender_data_iterator = map(lambda v: v['gender'], ab)

res = Counter(gender_data_iterator)
print(res)
