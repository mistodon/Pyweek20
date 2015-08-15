from __future__ import print_function, unicode_literals

import pyglet
from pyglet.window import key
import pyglet.gl as gl

from math import fmod, floor

from .entity import Entity, SpiritOfTheDrums, Camera, Datapawn, Obstacle
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

    def __init__(self, pygame=False):
        super(GameScreen, self).__init__(800, 450, caption="Datapawn")
        gl.glClearColor(0.5,0.85,1.0,1.0)
        self.batch = batch = pyglet.graphics.Batch()
        self.named_entities = {}
        self.clock = 0.0
        self.frames = 0
        self.ended = False

        drumsfx = [
            ("D", "header_burst.mp3"),
            ("0", "zero2.wav"),
            ("1", "one2.wav"),
            ("-", "minus2.wav")]
        self.drumsfx = {sym: pyglet.resource.media(f, streaming=False)
                        for sym, f in drumsfx}

        self.entities = [
            Entity(self, (400, 225), components=[Camera()]),
            Entity(self, (0,0), name="Spirit of the Drums", components=[SpiritOfTheDrums()]),
            prefabs.moonlight(self, -200, self.GROUND_Y, batch),
            prefabs.robot(self, 60, self.GROUND_Y, batch),
            prefabs.robot(self, 90, self.GROUND_Y, batch),
            prefabs.robot(self, 100, self.GROUND_Y, batch),
            prefabs.robot(self, 130, self.GROUND_Y, batch),
            prefabs.obstacle(self, 500, self.GROUND_Y, batch, "block.png", 76, 76),
            prefabs.ground_text(self, 1000, batch, "This is a test"),
            prefabs.scenery(self, 300, self.GROUND_Y, batch, "bigtree.png", 6, loop=300*5),
            prefabs.scenery(self, 400, self.GROUND_Y, batch, "weetree.png", 5, 0.75, loop=300*7),
            prefabs.scenery(self, 700, self.GROUND_Y, batch, "bigtree.png", 6, loop=300*11),
            prefabs.scenery(self, 900, self.GROUND_Y, batch, "weetree.png", 5, 0.75, loop=300*13),
            prefabs.scenery(self, 40, 300, batch, "moon.png", 2, 0.0),
            prefabs.obstacle(self, 1500, self.GROUND_Y, batch, "goldblock.png", 76, 76, hp=5, victory=True)
            ]
        for e in self.entities:
            if e.name:
                self.named_entities[e.name] = e

        pyglet.clock.schedule_interval(self.tick, 1.0/60.0)
        self.command = ["*","*","*","*"]
        self.last_beat = 4
        self.beatclock = BeatClock(pygame=pygame)
        self.beatclock.start()
        self.dispatch_event("on_start")

    def on_key_press(self, symbol, modifiers):
        super(GameScreen, self).on_key_press(symbol, modifiers)
        if self.ended:
            return
        sym = CONTROLS.get(symbol)
        if sym:
            beat = self.current_beat(rounds=True)
            self.command[beat] = sym
            self.drumsfx[sym].play()
            if beat == 3:
                self.dispatch_event("on_drum_command", ''.join(self.command))

    def tick(self, dt):
        if self.ended:
            return
        self.clock += dt
        if self.frames % 60 == 0:
            self.clock = self.beatclock.player.time
        self.frames += 1
        beat = self.current_beat(rounds=True)
        if self.last_beat > 0 and beat == 0:
            self.command = ["*","*","*","*"]
        self.clean_out_your_dead()
        self.dispatch_event("on_tick", dt)
        if len(Datapawn.population) == 0:
            self.end_game("Game over...")

    def clean_out_your_dead(self):
        deads = []
        for e in self.entities:
            if e.dead:
                for c in e.components.values():
                    c.on_die()
                    if isinstance(c, Obstacle) and c.victory:
                        self.end_game("Victory!")
                deads.append(e)
        for e in deads:
            self.entities.remove(e)

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
            colors = (1.0,1.0,0.4)*10
        else:
            colors = (0.6,0.6,0.6)*10
        pyglet.graphics.draw(10, pyglet.gl.GL_QUAD_STRIP,
            ("v2f", vertices), ("c3f", colors))

    def end_game(self, message="Victory!"):
        print(message)
        self.entities.append(prefabs.sky_text(self, self.width // 2, self.height // 2, self.batch, message, 80))
        self.ended = True

    def current_beat(self, rounds=False):
        f = round if rounds else floor
        return int(f(self.clock / self.beatclock.beat_length) % self.beatclock.beats_per_bar)

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