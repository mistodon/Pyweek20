from __future__ import print_function, unicode_literals

import pyglet
import pyglet.gl as gl
from pyglet.window import key

from math import fmod, floor

from .entity import Entity, SpiritOfTheDrums, Camera
from .music import BeatClock
from . import prefabs

CONTROLS = {
    key.UP: "D",
    key.DOWN: "0",
    key.LEFT: "-",
    key.RIGHT: "1",
}


class GameScreen(pyglet.window.Window):
    GROUND_Y = 100

    def __init__(self):
        super(GameScreen, self).__init__(800, 450, caption="Datapawn")
        gl.glClearColor(0.5,0.85,1.0,1.0)
        self.batch = batch = pyglet.graphics.Batch()
        self.named_entities = {}
        self.clock = 0.0
        self.frames = 0

        self.entities = [
            Entity(self, (400, 225), components=[Camera()]),
            prefabs.robot(self, 10, self.GROUND_Y, batch),
            prefabs.robot(self, 40, self.GROUND_Y, batch),
            prefabs.robot(self, 50, self.GROUND_Y, batch),
            prefabs.robot(self, 80, self.GROUND_Y, batch),
            Entity(self, (0,0), name="Spirit of the Drums", components=[SpiritOfTheDrums()]),
            prefabs.ground_text(self, 1000, batch, "This is a test"),
            prefabs.scenery(self, 300, self.GROUND_Y, batch, "bigtree.png", 7, loop=300*5),
            prefabs.scenery(self, 400, self.GROUND_Y, batch, "weetree.png", 6, 0.75, loop=300*7),
            prefabs.scenery(self, 700, self.GROUND_Y, batch, "bigtree.png", 7, loop=300*11),
            prefabs.scenery(self, 900, self.GROUND_Y, batch, "weetree.png", 6, 0.75, loop=300*13),
            ]
        for e in self.entities:
            if e.name:
                self.named_entities[e.name] = e

        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)
        self.command = ["*","*","*","*"]
        self.beatclock = BeatClock()
        self.beatclock.start()
        self.dispatch_event("on_start")

    def on_key_press(self, symbol, modifiers):
        super(GameScreen, self).on_key_press(symbol, modifiers)
        sym = CONTROLS.get(symbol)
        if sym:
            beat = self.current_beat(rounds=True)
            self.command[beat] = sym
            if beat == 3:
                self.dispatch_event("on_drum_command", ''.join(self.command))
                print(self.command)
                self.command = ["*","*","*","*"]

    def tick(self, dt):
        self.clock += dt
        if self.frames % 60 == 0:
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
        blength = self.beatclock.beat_length
        error = fmod(self.clock, blength) / blength
        beat = self.current_beat()
        bar = self.current_bar()
        playable = self.this_bar_playable()

        if bar < 2:
            return

        b = 10 - 8*error
        if not playable:
            b //= 2
        vertices = (
            0, 0,   b, b,   0, 450,   b, 450-b,
            800, 450,   800-b, 450-b,
            800, 0,   800-b, b,   0, 0,   b, b
            )
        if playable:
            colors = (1,1,1)*10
        elif beat == self.beatclock.beats_per_bar - 1 and bar >= 2:
            colors = (1.0,1.0,0.8)*10
        else:
            colors = (0.6,0.6,0.6)*10
        pyglet.graphics.draw(10, pyglet.gl.GL_QUAD_STRIP,
            ("v2f", vertices), ("c3f", colors))

    def end_game(self, message="Victory!"):
        print(message)
        pyglet.app.quit()

    def current_beat(self, rounds=False):
        f = round if rounds else floor
        return f(self.clock / self.beatclock.beat_length) % self.beatclock.beats_per_bar

    def current_bar(self, rounds=False):
        f = round if rounds else floor
        return f(self.clock / self.beatclock.bar_length)

    def this_bar_playable(self, rounds=False):
        bar = self.current_bar(rounds=rounds)
        if bar < 3:
            return False
        return (bar % 2) == 1

GameScreen.register_event_type("on_tick")
GameScreen.register_event_type("on_start")
GameScreen.register_event_type("on_drum_command")