from __future__ import print_function, unicode_literals

import pyglet
from .vec import vec2
from .constants import MASK
import random
from math import sin


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
        self.components = {c.__class__.__name__: c for c in components}
        for c in components:
            c.attach(self)
        self.dead = False

    def die(self):
        self.dead = True

    def __getitem__(self, comp_name):
        return self.components.get(comp_name)


class Component(object):
    def __init__(self):
        self.entity = None

    def attach(self, entity):
        self.entity = entity
        entity.window.push_handlers(self)

    def on_die(self):
        pass

class SingletonComponent(Component):
    active = None

    def __init__(self):
        super(SingletonComponent, self).__init__()
        self.__class__.active = self


class Camera(SingletonComponent):
    leftmargin = -45
    rightmargin = 200

    def __init__(self):
        super(Camera, self).__init__()
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
            self.foci = [e for e in self.foci if not e.dead]
            minx = sorted(e.pos.x for e in self.foci)[0] - self.leftmargin
            maxx = sorted(e.pos.x for e in self.foci)[-1] + self.rightmargin
            mindest = minx + self.centrevec.x
            maxdest = maxx - self.centrevec.x
            destx = maxdest if mindest+400 < maxx else mindest
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

    def on_die(self):
        self.sprite.batch = None

    @classmethod
    def get_layer(cls, index):
        if index in cls.layers:
            return cls.layers[index]
        layer = pyglet.graphics.OrderedGroup(index)
        cls.layers[index] = layer
        return layer

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
        self.base_img = pyglet.resource.image("datapawn.png")
        self.attack_img = pyglet.resource.image("datapawn-attacking.png")
        self.attacking = False
        Datapawn.population.append(self)

    def on_start(self):
        Camera.active.add_focus(self.entity)

    def set_attacking(self, status):
        self.attacking = status
        sprite = self.entity["Drawable"].sprite
        sprite.image = self.attack_img if status else self.base_img

    def on_drum_command(self, command):
        self.set_attacking(False)
        # resolve scope
        cmd0 = command[0]
        leader = self.is_the_leader
        if (cmd0 == "1" and not leader) or (cmd0 == "0" and leader):
            return
        # act on command if scope includes me
        action = command[1:3]
        target = command[3]
        if action in("DD", "D-") and target == "1":
            dx = 150.0
            if action == "D-":
                self.set_attacking(True)
                dx = 100.0
            self.move_interval = (self.entity.pos[0], self.entity.pos[0] + dx)
        elif action == "DD" and target == "-":
            self.move_interval = (self.entity.pos[0], self.entity.pos[0] - 150.0)

    def on_tick(self, dt):
        if self.move_interval is not None:
            self.move(dt)
        ex = self.entity.pos.x
        deathx = Moonlight.active.entity.pos.x
        if ex - deathx <= 55:
            self.entity.die()

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
        delta = vec2(speed*dt*direction, 0)
        obstacle = self.entity["RectCollider"].test_overlap(
            mask=MASK["obstacle"],
            displacement=delta)
        if obstacle:
            x = self.entity.pos.x
            self.move_interval = (x, x + ((dist-moved)*-direction))
        else:
            self.entity.pos += delta

    @property
    def is_the_leader(self):
        return Datapawn.population[0] is self

    def on_die(self):
        try:
            Datapawn.population.remove(self)
        except ValueError:
            pass

    @staticmethod
    def cycle_leader():
        popn = Datapawn.population
        if popn:
            popn.append(popn.pop(0))

class Obstacle(Component):
    def __init__(self, hp, hitsounds={}, victory=False):
        super(Obstacle, self).__init__()
        self.hp = hp
        self.wiggletime = 0.0
        self.hitsounds = {key: pyglet.resource.media(f, streaming=False)
                          for key,f in hitsounds.items()}
        self.victory = victory

    def on_start(self):
        self.basepos = self.entity.pos

    def on_tick(self, dt):
        self.wiggletime = max(0, self.wiggletime-dt)
        if self.wiggletime > 0:
            dx = sin(self.wiggletime) * 10
            self.entity.pos = self.basepos + vec2(dx, 0)
        else:
            rect = self.entity["RectCollider"]
            circ = self.entity["CircleCollider"]
            collider = rect if rect else circ
            if collider:
                robot = collider.test_overlap(
                    mask=MASK["robot"], displacement=vec2(-5, 0))
                pawn = robot.entity["Datapawn"] if robot else None
                if pawn and pawn.attacking:
                    s = self.hitsounds.get("hit")
                    if s: s.play()
                    self.hp -= 1
                    self.wiggletime = 0.25
            if self.hp <= 0:
                self.entity.die()

    def on_die(self):
        s = self.hitsounds.get("die")
        if s:
            s.play()


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

class Moonlight(SingletonComponent):
    def __init__(self):
        super(Moonlight, self).__init__()
        self.speed = 16.0

    def on_start(self):
        Camera.active.add_focus(self.entity)

    def on_tick(self, dt):
        x,y = self.entity.pos
        x += self.speed *  dt
        self.entity.pos = vec2(x,y)