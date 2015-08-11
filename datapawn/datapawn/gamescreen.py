import pyglet
import pyglet.gl as gl

from datapawn.entity import Entity, Drawable


class GameScreen(pyglet.window.Window):
    GROUND_Y = 50

    def __init__(self):
        super().__init__(800, 450)
        gl.glClearColor(0.5,0.85,1.0,1.0)
        self.batch = pyglet.graphics.Batch()

        self.entities = [
            Entity((10, self.GROUND_Y),
                Drawable(image="datapawn.png", batch=self.batch))
            ]

        pyglet.clock.schedule_interval(self.on_tick, 1.0/60.0)

    def on_tick(self, dt):
        for e in self.entities:
            for c in e.components:
                c.tick(dt)

    def on_draw(self):
        self.clear()
        self.draw_ground()
        self.batch.draw()

    def draw_ground(self):
        groundstrip = (
            0, self.GROUND_Y,   800, self.GROUND_Y,
            0, self.GROUND_Y-20,   800, self.GROUND_Y-20,
            0,  0,   800,  0
            )
        colors = (1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0)
        pyglet.graphics.draw(6, pyglet.gl.GL_TRIANGLE_STRIP,
            ("v2f", groundstrip), ("c3f", colors))