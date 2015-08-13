from .entity import *


def robot(window, x, y, batch):
    return Entity(window, (x, window.GROUND_Y), components=[
        Drawable(image="datapawn.png", batch=batch),
        Datapawn()
        ])

def scenery(window, x, y, batch, image, layer=8, parallax=1.0, loop=None):
    d = Drawable(image=image, batch=batch,
        layer=layer, parallax=parallax, loop=loop)
    return Entity(window, (x, y), components=[d])