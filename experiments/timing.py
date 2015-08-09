#! /usr/bin/env python3
"""
Load a music file and play it. Print timing relative to the nearest beat when a key is pressed.
"""

import argparse

from .monkey import patch
import pyglet
import time


patch()


class BeatTester:
    def __init__(self, args):
        self.win = pyglet.window.Window(400, 400)
        self.player = pyglet.media.Player()
        self.music = pyglet.media.load(args.music, streaming=True)
        self.beats_per_minute = args.bpm
        self.offset_from_start = args.offset
        self.beats_per_bar = args.bar
        self.beat_length = 60.0 / self.beats_per_minute
        self.bar_length = self.beats_per_bar * self.beat_length
        self.clock_time_start = None
        self.win.push_handlers(self.on_key_press)

    def start(self):
        print(pyglet.media.get_audio_driver().__class__.__name__)
        self.player.queue(self.music)
        self.player.play()
        self.clock_time_start = time.time()

    def on_key_press(self, symbol, modifiers):
        """
        :param symbol: key code
        :param modifiers: shifts and such
        :return:
        """
        if self.player.playing:
            music_time = self.player.time - self.offset_from_start
            bar_position = music_time % self.bar_length
            nearest_beat = round(bar_position / self.beat_length)
            if nearest_beat >= self.beats_per_bar:
                nearest_beat -= self.beats_per_bar
            error = bar_position - (self.beat_length * nearest_beat)
            print("Beat {0}{1:+.3f}s ".format(nearest_beat + 1, error))
        else:
            print("Not Playing")


def main():
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add("--bpm", type=int, default=120, help="beats per minute of music")
    add("--bar", type=int, default=4, help="beats in a bar")
    add("--offset", type=float, default=0.0, help="time to first beat in music file")
    add("music", help="path to music file")

    pyglet.options['audio'] = ('openal', 'pulse')
    args = ap.parse_args()
    tester = BeatTester(args)
    tester.start()
    pyglet.app.run()

if __name__ == '__main__':
    main()
