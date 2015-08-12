import pyglet
from .gamescreen import GameScreen


def main():
    pyglet.resource.path = ["data", "data/images", "data/experiments"]
    pyglet.resource.reindex()

    gs = GameScreen()
    pyglet.app.run()
