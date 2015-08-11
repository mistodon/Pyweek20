import pyglet


class Entity:
    def __init__(self, pos, *components):
        self.pos = pos
        self.components = components
        for c in components:
            c.entity = self

class Component:
    def __init__(self):
        self.entity = None

class Drawable(Component):
    def __init__(self, image, batch=None):
        super().__init__()
        img = pyglet.resource.image(image)
        self.sprite = pyglet.sprite.Sprite(img, batch=batch)

    def tick(self, dt):
        self.sprite.set_position(*self.entity.pos)