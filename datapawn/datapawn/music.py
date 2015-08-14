import pyglet

from math import floor

# Change this to some music you actually have.
TRACK = "Smashdance.wav"

class MusicPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.player = pyglet.media.Player()

    def play(self):
        try:
            self.music = pyglet.resource.media(self.filename, streaming=True)
            self.player.queue(self.music)
            self.player.eos_action = pyglet.media.Player.EOS_LOOP
            self.player.play()
        except pyglet.resource.ResourceNotFoundException:
            pass

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
        try:
            self.mixer.music.load(self.filename)
            self.mixer.music.play()
        except Exception:   # TODO find out which one
            pass

    @property
    def playing(self):
        return self.mixer.music.get_busy()

    @property
    def time(self):
        return self.mixer.music.get_pos() / 1000.0    # pygame is ms, pyglet is seconds


class BeatClock:
    def __init__(self, pygame=False):
        self.player = PyGameMusicPlayer(TRACK) if pygame else MusicPlayer(TRACK)
        self.bpm = 120.0
        self.offset = 0.0
        self.beats_per_bar = 4
        self.beat_length = 60.0 / self.bpm
        self.bar_length = self.beats_per_bar * self.beat_length

    def start(self):
        self.player.play()

    def get_beat(self, round_down=False):
        if self.player.playing:
            music_time = self.player.time - self.offset
            bar_pos = music_time % self.bar_length
            roundfunc = floor if round_down else round
            nearest_beat = roundfunc(bar_pos / self.beat_length)
            if nearest_beat >= self.beats_per_bar:
                nearest_beat -= self.beats_per_bar
            error = bar_pos - (self.beat_length * nearest_beat)
            return (nearest_beat, error)
        else:
            return None