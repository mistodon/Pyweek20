#! /usr/bin/env python3
"""
Load a music file and play it. Print timing relative to the nearest beat when a key is pressed.
"""
from __future__ import print_function, unicode_literals

import argparse

from .monkey import patch

import pyglet
import time


patch()


class MusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.player = pyglet.media.Player()

    def play(self):
        self.music = pyglet.media.load(self.filename, streaming=True)
        self.player.queue(self.music)
        self.player.play()

    @property
    def time(self):
        return self.player.time

    @property
    def playing(self):
        return self.player.playing


class PyGameMusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        import pygame
        self.mixer = pygame.mixer
        if not self.mixer.get_init():
            self.mixer.init()

    def play(self):
        self.mixer.music.load(self.filename)
        self.mixer.music.play()

    @property
    def playing(self):
        return self.mixer.music.get_busy()

    @property
    def time(self):
        return self.mixer.music.get_pos() / 1000.0    # pygame is ms, pyglet is seconds


class BeatTester:
    def __init__(self, args):
        self.win = pyglet.window.Window(400, 400)
        self.player = PyGameMusicPlayer(args.music) if args.pygame_audio else MusicPlayer(args.music)
        self.beats_per_minute = args.bpm
        self.offset_from_start = args.offset
        self.beats_per_bar = args.bar
        self.beat_length = 60.0 / self.beats_per_minute
        self.bar_length = self.beats_per_bar * self.beat_length
        self.win.push_handlers(self.on_key_press)
        self.calibration_times = []

    def start(self):
        self.player.play()

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
            if symbol == pyglet.window.key.C:
                self.calibration_times.append(music_time)
                if len(self.calibration_times) == 2:
                    diff = (self.calibration_times[1] - self.calibration_times[0])
                    guess_bpm = 60.0 / diff
                    print("Approx {0:.3f} bpm, {1:.3f}s".format(guess_bpm, diff))
                    self.calibration_times[:1] = []
        else:
            print("Not Playing")


def main():
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add("--bpm", type=int, default=120, help="beats per minute of music")
    add("--bar", type=int, default=4, help="beats in a bar")
    add("--offset", type=float, default=0.0, help="time to first beat in music file")
    add("--pygame-audio", action="store_true", default=False)
    add("music", help="path to music file")

    args = ap.parse_args()
    if args.pygame_audio:
        import pygame
        pygame.init()
    tester = BeatTester(args)
    tester.start()
    pyglet.app.run()

if __name__ == '__main__':
    main()
