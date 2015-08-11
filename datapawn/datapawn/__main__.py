import pyglet
from datapawn.gamescreen import GameScreen

def main():
    pyglet.resource.path = ["data", "data/images"]
    pyglet.resource.reindex()

    gs = GameScreen()
    pyglet.app.run()
