import pyray
from raylib import FLAG_MSAA_4X_HINT

from source.data import CONFIG, COLORS
from source.camera import Camera
from source.vehicle import Vehicle


Vector = pyray.Vector3


class Framework:

    def __init__(self):

        self.running = False
        self.paused = False
        self.step = False

        pyray.set_config_flags(FLAG_MSAA_4X_HINT)
        pyray.init_window(CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT, CONFIG.TITLE)
        pyray.set_target_fps(CONFIG.FPS)

        self.camera = Camera()
        self.vehicle = Vehicle()

    def start(self):
        if not self.running:
            self.running = True
            self.loop()

    def reset(self):
        self.paused = False
        self.step = False

    def events(self):
        if pyray.window_should_close():
            self.running = False

    def update(self):
        self.camera.update(self.vehicle)

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(COLORS.WHITE)

        pyray.begin_mode_3d(self.camera.camera)
        self.vehicle.render()
        pyray.draw_grid(50, 10.0)
        pyray.end_mode_3d()
        pyray.end_drawing()

    def loop(self):
        while self.running:
            self.events()
            self.update()
            self.render()
