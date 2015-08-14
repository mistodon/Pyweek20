from .entity import *


def robot(window, x, y, batch):
    return Entity(window, (x, window.GROUND_Y), components=[
        Drawable(image="datapawn.png", batch=batch),
        Datapawn()
        ])


def scenery(window, x, y, batch, image, layer=8, parallax=1.0, loop=None):
    d = Drawable(image=image, batch=batch, layer=layer,
                 parallax=parallax, loop=loop)
    return Entity(window, (x, y), components=[d])


def ground_text(window, x, batch, text, font_scale=0.9, font_name="Courier"):
    y = window.GROUND_Y * 0.5
    d = DrawableText(text=text, x=x, world=True, font_name=font_name,
                     font_size=window.GROUND_Y * font_scale,
                     y=y, batch=batch,
                     anchor_x='center', anchor_y='center')
    return Entity(window, (x, y), components=[d])
