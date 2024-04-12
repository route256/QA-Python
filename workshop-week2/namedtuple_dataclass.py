from collections import namedtuple
from dataclasses import dataclass


TheCat = namedtuple("TheCat", ["name", "age", "type"])

Murzik = TheCat(name="Murzik", age=10, type="Pers")

print(Murzik)
print(Murzik.name)
print(Murzik.age)

# Murzik.age = 11


@dataclass(frozen=True)
class TheCatClass:
    name: str
    age: int
    type: str


Persik = TheCatClass("Persik", 15, 'Siam')
print(Persik.name)
print(Persik.age)

# Persik.age = 16
print(Persik.age)