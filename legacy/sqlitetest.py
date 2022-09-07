import imp
import sqlite3
from enum import Enum
conn = sqlite3.connect('mysqlite2.db')
c = conn.cursor()


class Animal(Enum):
    dog = 1
    cat = 2
    lion = 3


x = Animal.cat
print(x.value)

print(Animal.cat)
