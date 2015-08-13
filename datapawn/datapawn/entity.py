from __future__ import print_function, unicode_literals

import pyglet
from .vec import vec2


class Entity:
    def __init__(self, window, pos=vec2.zero(), rot=0.0, name=None, components=()):
        self.window = window
        self.pos = vec2(*pos)
        self.rot = rot
        self.name = name
        self.components = list(components)
        for c in components:
            c.attach(self)


class Component():
    def __init__(self):
        self.entity = None

    def attach(self, entity):
        self.entity = entity
        entity.window.push_handlers(self)


class Drawable(Component):
    def __init__(self, image, batch=None):
        super(Drawable, self).__init__()
        img = pyglet.resource.image(image)
        self.sprite = pyglet.sprite.Sprite(img, batch=batch)

    def on_tick(self, dt):
        self.sprite.position = self.entity.pos
        self.sprite.rotation = self.entity.rot


class Datapawn(Component):
    population = []     # leader is population[0]

    def __init__(self):
        super(Datapawn, self).__init__()
        self.dest = None
        self.emplaced = False
        Datapawn.population.append(self)

    def on_drum_command(self, command):
        # resolve scope
        if command[0] == "1" and not self.is_the_leader:
            return
        # act on command if scope includes me
        action = command[1:]
        if action == "DD1":
            self.dest = self.entity.pos[0] + 150.0

    def on_tick(self, dt):
        if self.dest is not None:
            x,y = self.entity.pos
            dx = -50*dt if self.dest < x else 50*dt
            newx = x + dx
            if (x < self.dest < newx) or (newx < self.dest < x):
                self.dest = None
            self.entity.pos = vec2(newx, y)

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
    def __init__(self, **kwargs):
        super(DrawableText, self).__init__()
        self.label = pyglet.text.Label(**kwargs)

    def on_draw(self):
        self.label.draw()
