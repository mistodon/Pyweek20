import pyglet
import pyglet.gl as gl
from pyglet.window import key

from datapawn.entity import Entity, Drawable, Datapawn

CONTROLS = {
    key.UP: "D",
    key.DOWN: "0",
    key.LEFT: "-",
    key.RIGHT: "1",
}

class GameScreen(pyglet.window.Window):
    GROUND_Y = 50

    def __init__(self):
        super().__init__(800, 450)
        gl.glClearColor(0.5,0.85,1.0,1.0)
        self.batch = pyglet.graphics.Batch()
        self.named_entities = {}

        self.entities = [
            Entity(self, (10, self.GROUND_Y), name="Robot0", components=[
                Drawable(image="datapawn.png", batch=self.batch),
                Datapawn()
                ])
            ]
        for e in self.entities:
            if e.name:
                self.named_entities[e.name] = e

        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)
        self.command = []

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        sym = CONTROLS.get(symbol)
        if sym:
            self.command.append(sym)
            if len(self.command) == 4:
                self.dispatch_event("on_drum_command", self.command)
                self.command = []

    def tick(self, dt):
        self.dispatch_event("on_tick", dt)
        robot0 = self.named_entities["Robot0"]
        if robot0.pos[0] > 750:
            print("Victory!")
            pyglet.app.exit()

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

GameScreen.register_event_type("on_tick")
GameScreen.register_event_type("on_drum_command")