import pyglet

class GameScreen(pyglet.window.Window):
    def __init__(self):
        super().__init__(800,450)

    def on_draw(self):
        self.clear()
        self.draw_ground()

    def draw_ground(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_TRIANGLE_STRIP,
                             ("v2f", (0,50,0,30,800,50,800,30)),
                             ("c4f", (1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0)))
