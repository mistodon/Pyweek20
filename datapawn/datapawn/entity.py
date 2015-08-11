import pyglet


class Entity:
    def __init__(self, window, pos, name=None, components=[]):
        self.window = window
        self.pos = pos
        self.name = name
        self.components = components
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
        self.sprite.set_position(*self.entity.pos)

class Datapawn(Component):
    def __init__(self):
        super().__init__()
        self.dest = None

    def on_drum_command(self, command):
        if command == ["D", "D", "D", "1"]:
            self.dest = self.entity.pos[0] + 100

    def on_tick(self, dt):
        if self.dest is not None:
            x,y = self.entity.pos
            dx = -50*dt if self.dest < x else 50*dt
            newx = x + dx
            if (x < self.dest < newx) or (newx < self.dest < x):
                self.dest = None
            self.entity.pos = (newx, y)