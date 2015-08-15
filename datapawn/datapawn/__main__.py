import argparse
import pyglet


def main():
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add("--pygame-audio", action="store_true", default=False)
    args = ap.parse_args()
    pyglet.resource.path = ["data", "data/images", "data/experiments", "data/sfx"]
    pyglet.resource.reindex()

    from .gamescreen import GameScreen
    gs = GameScreen(pygame=args.pygame_audio)
    pyglet.app.run()
