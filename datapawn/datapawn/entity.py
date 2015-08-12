from __future__ import print_function, unicode_literals

import pyglet
from .vec import vec2
import random


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
        super().__init__()
        img = pyglet.resource.image(image)
        self.sprite = pyglet.sprite.Sprite(img, batch=batch)

    def on_tick(self, dt):
        self.sprite.position = self.entity.pos
        self.sprite.rotation = self.entity.rot


class Datapawn(Component):
    population = []
    selected_leader = None

    def __init__(self):
        super().__init__()
        self.dest = None
        self.selected = False
        self.emplaced = False
        Datapawn.population.append(self)

    def on_drum_command(self, command):
        # resolve scope
        if command[0] == "1" and not self.selected:
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

    def die(self):
        try:
            Datapawn.population.remove(self)
            if Datapawn.selected_leader is self:
                Datapawn.selected_leader = None
        except ValueError:
            pass

    @staticmethod
    def select_a_leader():
        old_leader = Datapawn.selected_leader
        new_leader = None
        if old_leader:
            old_leader.selected = False # maybe remove leader component?
        population = Datapawn.population
        if old_leader:
            try:
                leader_pos = population.index(old_leader)
                new_leader = population[(leader_pos + 1) % len(population)]
            except ValueError:
                old_leader = None
        if not old_leader and population:
            new_leader = random.choice(population)

        if new_leader:
            new_leader.selected = True  # maybe add a leader component or something?
        Datapawn.selected_leader = new_leader
