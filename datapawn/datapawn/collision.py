from __future__ import print_function, unicode_literals

import pyglet
from .vec import vec2
from .entity import Component


class Collider(Component):
    shape = None
    all_colliders = []

    def __init__(self, layermask=0):
        super(Collider, self).__init__()
        Collider.all_colliders.append(self)
        self.layermask = layermask

    def on_die(self):
        Collider.all_colliders.remove(self)
 
    def overlaps(self, other):
        return False

    def test_overlap(self, multiple=False, mask=0, displacement=vec2.zero()):
        oldpos = self.entity.pos
        self.entity.pos += displacement
        result = [] if multiple else None
        for other in Collider.all_colliders:
            if other is self:
                continue
            if mask & other.layermask == 0:
                continue
            if self.overlaps(other):
                if multiple:
                    result.append(other)
                else:
                    result = other
                    break
        self.entity.pos = oldpos
        return result

    @classmethod
    def circle_circle_overlap(cls, a, b):
        dist_sq = (a.entity.pos - b.entity.pos).magSq
        r_sq = (a.radius + b.radius) ** 2
        return dist_sq < r_sq

    @classmethod
    def rect_rect_overlap(cls, a, b):
        ax,ay = a.entity.pos
        aw,ah = a.width, a.height
        bx,by = b.entity.pos
        bw,bh = b.width, b.height
        return (ax < bx+bw and ax+aw > bx and ay < by+bh and ay+ah > by)

    @classmethod
    def circle_rect_overlap(cls, a, b):
        rx,ry = b.entity.pos
        rw,rh = b.width, b.height
        cx,cy = cpos = a.entity.pos
        rad2 = a.radius * a.radius
        if (rx < cx < rx+rw) and (ry < cy < ry+rh):
            return True
        corners = [(rx,ry), (rx+rw,ry), (rx+rw,ry+rh), (rx,ry+rh)]
        edges = [(corners[i], corners[(i+1)%4]) for i in range(4)]
        for p,q in edges:
            disp = (cpos - q)
            edge = (p - q)
            proj = disp.proj_coefficient(edge)
            proj = min(max(0, proj), 1)
            closest = cpos - (q + edge*proj)
            if (closest.magSq < rad2):
                return True
        return False

class CircleCollider(Collider):
    shape = "circle"

    def __init__(self, radius, layermask=0):
        super(CircleCollider, self).__init__(layermask)
        self.radius = radius

    def overlaps(self, other):
        if other.shape == "circle":
            return Collider.circle_circle_overlap(self, other)
        elif other.shape == "rect":
            return Collider.circle_rect_overlap(self, other)
        return False

class RectCollider(Collider):
    shape = "rect"

    def __init__(self, width, height, layermask=0):
        super(RectCollider, self).__init__(layermask)
        self.width = width
        self.height = height

    def overlaps(self, other):
        if other.shape == "circle":
            return Collider.circle_rect_overlap(other, self)
        elif other.shape == "rect":
            return Collider.rect_rect_overlap(self, other)
        return False