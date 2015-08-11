from collections import namedtuple
from math import sqrt

class vec2(namedtuple("vec2", ["x","y"])):

    def __add__(self, other):
        return vec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return vec2(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        if hasattr(other, "__len__"):
            return vec2(self.x*other.x, self.y*other.y)
        return vec2(self.x*other, self.y*other)

    def __div__(self, other):
        if hasattr(other, "__len__"):
            return vec2(self.x/other.x, self.y/other.y)
        return vec2(self.x/other, self.y/other)

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    @property
    def magSq(self):
        return self.dot(self)

    @property
    def mag(self):
        return sqrt(self.magSq)

    @property
    def normalized(self):
        return self / self.mag
    
    @staticmethod
    def zero():
        return vec2(0.0, 0.0)

    @staticmethod
    def one():
        return vec2(1.0, 1.0)