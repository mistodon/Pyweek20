from __future__ import print_function, unicode_literals

import pyglet
import pyglet.gl as gl
from pyglet.window import key

from math import fmod

from .entity import Entity, Drawable, Datapawn, SpiritOfTheDrums, Camera
from .music import BeatClock

CONTROLS = {
    key.UP: "D",
    key.DOWN: "0",
    key.LEFT: "-",
    key.RIGHT: "1",
}


class GameScreen(pyglet.window.Window):
    GROUND_Y = 100

    def __init__(self):
        super().__init__(800, 450)
        gl.glClearColor(0.5,0.85,1.0,1.0)
        self.batch = pyglet.graphics.Batch()
        self.named_entities = {}
        self.clock = 0.0
        self.frames = 0

        def robot(x):
            return Entity(self, (x, self.GROUND_Y), components=[
                Drawable(image="datapawn.png", batch=self.batch),
                Datapawn()
                ])

        self.entities = [
            Entity(self, (400, 225), components=[Camera()]),
            robot(10),
            robot(40),
            robot(50),
            robot(80),
            Entity(self, (0,0), name="Spirit of the Drums", components=[SpiritOfTheDrums()]),
            ]
        for e in self.entities:
            if e.name:
                self.named_entities[e.name] = e

        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)
        self.command = []
        self.beatclock = BeatClock()
        self.beatclock.start()
        self.dispatch_event("on_start")

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        sym = CONTROLS.get(symbol)
        if sym:
            beat,error = self.beatclock.get_beat()
            status = "Good!"
            if error < -0.12:
                status = "Too Fast"
            elif error > 0.12:
                status = "Too Slow"
            #print("{0}  {1}".format(error, status))
            self.command.append(sym)
            if len(self.command) == 4:
                self.dispatch_event("on_drum_command", ''.join(self.command))
                print(self.command)
                self.command = []

    def tick(self, dt):
        self.clock += dt
        if self.frames == 10:
            self.clock = self.beatclock.player.time
        self.frames += 1
        self.dispatch_event("on_tick", dt)

    def on_draw(self):
        self.clear()
        self.draw_sky()
        self.draw_ground()
        self.batch.draw()
        self.draw_beat()

    def draw_sky(self):
        skystrip = (
            0, 450,   800, 450,
            0, self.GROUND_Y,   800, self.GROUND_Y
            )
        colors = (0.75,0.8,1.0,0.75,0.8,1.0,0.0,0.33,1.0,0.0,0.33,1.0)
        pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP,
            ("v2f", skystrip), ("c3f", colors))

    def draw_ground(self):
        groundstrip = (
            0, self.GROUND_Y,   800, self.GROUND_Y,
            0, self.GROUND_Y-20,   800, self.GROUND_Y-20,
            0,  0,   800,  0
            )
        colors = (1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0)
        pyglet.graphics.draw(6, pyglet.gl.GL_TRIANGLE_STRIP,
            ("v2f", groundstrip), ("c3f", colors))

    def draw_beat(self):
        if (self.frames < 11):
            return

        blength = self.beatclock.beat_length
        error = fmod(self.clock, blength) / blength
        beat = int(self.clock / blength)
        bar = self.clock / self.beatclock.bar_length
        playable = (bar % 2) == 1

        b = 10 - 8*error
        vertices = (
            0, 0,   b, b,   0, 450,   b, 450-b,
            800, 450,   800-b, 450-b,
            800, 0,   800-b, b,   0, 0,   b, b
            )
        colors = (0.8,1,0.8)*10
        pyglet.graphics.draw(10, pyglet.gl.GL_QUAD_STRIP,
            ("v2f", vertices), ("c3f", colors))

    def end_game(self, message="Victory!"):
        print(message)
        pyglet.app.quit()


GameScreen.register_event_type("on_tick")
GameScreen.register_event_type("on_start")
GameScreen.register_event_type("on_drum_command")