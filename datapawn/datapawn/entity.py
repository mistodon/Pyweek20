from __future__ import print_function, unicode_literals

import pyglet
from .vec import vec2
import random


def sgn(x):
    if x == 0:
        return 0
    return -1 if x < 0 else 1


class Entity:
    def __init__(self, window, pos=vec2.zero(), rot=0.0, name=None, components=()):
        self.window = window
        self.pos = vec2(*pos)
        self.rot = rot
        self.name = name
        self.components = list(components)
        for c in components:
            c.attach(self)


class Component(object):
    def __init__(self):
        self.entity = None

    def attach(self, entity):
        self.entity = entity
        entity.window.push_handlers(self)


class Camera(Component):
    active = None
    leftmargin = 100

    def __init__(self):
        super(Camera, self).__init__()
        self.__class__.active = self
        self.foci = []
        self.centrevec = vec2(0, 0)
    
    def on_start(self):
        self.centrevec = vec2(*self.entity.window.get_size()) * 0.5

    def add_focus(self, entity):
        self.foci.append(entity)

    def remove_focus(self, entity):
        self.foci.remove(entity)

    def on_tick(self, dt):
        if self.foci:
            minx = sorted(e.pos.x for e in self.foci)[0] - self.leftmargin
            destx = minx + self.centrevec.x
            x, y = self.entity.pos
            t = 0.1
            newx = x*(1-t) + destx*t
            self.entity.pos = vec2(newx, y)

    @property
    def offset(self):
        return self.centrevec - self.entity.pos


class Drawable(Component):
    layers = {}

    def __init__(self, image, batch=None, layer=8, parallax=1.0, loop=None):
        super(Drawable, self).__init__()
        img = pyglet.resource.image(image)
        self.sprite = pyglet.sprite.Sprite(
            img, batch=batch, group=Drawable.get_layer(layer), subpixel=True)
        self.parallax = parallax
        self.loop = loop

    def on_tick(self, dt):
        drawpos = self.entity.pos + (Camera.active.offset*self.parallax)
        if self.loop:
            x,y = drawpos
            while x < -200:
                x += self.loop
            while x > 800:
                x -= self.loop
            drawpos = vec2(x,y)
        self.sprite.position = drawpos
        self.sprite.rotation = self.entity.rot

    @classmethod
    def get_layer(cls, index):
        if index in cls.layers:
            return cls.layers[index]
        layer = pyglet.graphics.OrderedGroup(index)
        cls.layers[index] = layer
        return layer

class Datapawn(Component):
    population = []     # leader is population[0]
    MAXSPEED = 96.0
    STOP_DIST = 32.0
    BASE_SPEED = 20.0

    def __init__(self):
        super(Datapawn, self).__init__()
        self.move_interval = None
        self.emplaced = False
        # Slight randomness to give them personality
        self.maxspeed = self.MAXSPEED * random.randrange(90, 110) * 0.01
        self.stop_dist = self.STOP_DIST * random.randrange(90, 110) * 0.01
        self.base_speed = self.BASE_SPEED * random.randrange(90, 110) * 0.01
        Datapawn.population.append(self)

    def on_start(self):
        Camera.active.add_focus(self.entity)

    def on_drum_command(self, command):
        # resolve scope
        cmd0 = command[0]
        leader = self.is_the_leader
        if (cmd0 == "1" and not leader) or (cmd0 == "0" and leader):
            return
        # act on command if scope includes me
        action = command[1:]
        if action == "DD1":
            self.move_interval = (self.entity.pos[0], self.entity.pos[0] + 150.0)
        elif action == "DD-":
            self.move_interval = (self.entity.pos[0], self.entity.pos[0] - 150.0)

    def on_tick(self, dt):
        if self.move_interval is not None:
            self.move(dt)

    def move(self, dt):
        a, b = self.move_interval
        dist = b-a
        direction = sgn(dist)
        dist = abs(dist)
        moved = abs(self.entity.pos[0]-a)
        if moved >= dist:
            self.move_interval = None
        if moved < self.stop_dist:
            speed = moved/self.stop_dist * self.maxspeed + self.base_speed
        elif moved > dist - self.stop_dist:
            speed = (dist-moved)/self.stop_dist * self.maxspeed
        else:
            speed = self.maxspeed
        self.entity.pos += vec2(speed*dt*direction, 0)

    @property
    def is_the_leader(self):
        return Datapawn.population[0] is self

    def die(self):
        try:
            Datapawn.population.remove(self)
        except ValueError:
            pass

    @staticmethod
    def cycle_leader():
        popn = Datapawn.population
        if popn:
            popn.append(popn.pop(0))


class SpiritOfTheDrums(Component):
    """
    Handles high-level commands on the entire population of Datapawns that can't be
    done easily on an individual basis
    """
    def on_drum_command(self, command):
        # resolve scope
        if command[0] != "D":
            return
        action = command[1:]
        if action == "D01":
            Datapawn.cycle_leader()


class DrawableText(Component):
    def __init__(self, world=False, **kwargs):
        super(DrawableText, self).__init__()
        self.world = world
        self.x = kwargs['x']
        self.label = pyglet.text.Label(**kwargs)

    def on_draw(self):
        if self.world:
            self.label.x = self.x + Camera.active.offset.x
        self.label.draw()
