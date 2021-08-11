from dataclasses import dataclass


@dataclass
class A:
    a: str
    a2: str = ""

@dataclass
class B(A):
    b: str
    b2: str = ""

class C(B):
    pass

c = C(a='a', b='b')
