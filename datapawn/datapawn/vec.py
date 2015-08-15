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

    def proj_coefficient(self, other):
        if other.is_zero:
            return 0
        return self.dot(other) / other.dot(other)

    def proj(self, other):
        return other * self.proj_coefficient(other)

    @property
    def magSq(self):
        return self.dot(self)

    @property
    def mag(self):
        return sqrt(self.magSq)

    @property
    def normalized(self):
        if self.is_zero:
            return vec2(0,0)
        return self / self.mag

    @property
    def is_zero(self):
        return self.x == self.y == 0
    
    
    @staticmethod
    def zero():
        return vec2(0.0, 0.0)

    @staticmethod
    def one():
        return vec2(1.0, 1.0)