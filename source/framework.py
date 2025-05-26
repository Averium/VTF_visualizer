from os import listdir
from os.path import splitext, join

import pyray
from pyray import Vector3 as Vector, Vector4 as Quaternion
from raylib import FLAG_MSAA_4X_HINT, LOG_ERROR, KEY_P, KEY_SPACE, KEY_R
from scipy.io import loadmat
from sympy.codegen.cnodes import static

from source.data import CONFIG, COLORS, PATH
from source.camera import Camera
from source.file import MatFile
from source.vehicle import Vehicle
from source.log import Log
from source.scheduler import Scheduler


class Framework:

    def __init__(self):

        self.running = False
        self.paused = False
        self.step = False

        pyray.set_trace_log_level(LOG_ERROR)
        pyray.set_config_flags(FLAG_MSAA_4X_HINT)
        pyray.init_window(CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT, CONFIG.TITLE)
        pyray.set_target_fps(CONFIG.FPS)

        self.scheduler = Scheduler(CONFIG.SIMULATION_SPEED, CONFIG.DOWN_SAMPLING)
        self.camera = Camera()
        self.vehicle = Vehicle()

        self.sim_data = {}
        self.load_data(PATH.DATA)

        time = self.sim_data["data"]["data"][:, 0]
        data = self.sim_data["data"]["data"][:, 1:]

        self.scheduler.start(time, data)

    def start(self):
        if not self.running:
            self.running = True
            self.loop()

    def reset(self):
        self.paused = False
        self.step = False

    @staticmethod
    def draw_grid(size, spacing):
        half = (size * spacing) / 2.0

        for i in range(size + 1):
            offset = -half + i * spacing

            pyray.draw_line_3d(Vector(offset, -half, 0.0), Vector(offset, half, 0.0), COLORS.GREY)
            pyray.draw_line_3d(Vector(-half, offset, 0.0), Vector(half, offset, 0.0), COLORS.GREY)

    def load_data(self, folder):
        Log.info(f"Attempting to load .mat files from folder: [{folder}].")

        for index, filename in enumerate(listdir(folder)):
            name, extension = splitext(filename)
            if extension == MatFile.EXTENSION:
                self.sim_data[name] = loadmat(join(folder, f"{name}{extension}"))
                Log.info(f"Data from {name}{extension} successfully loaded.")

    def events(self):
        if pyray.window_should_close():
            self.running = False

        if pyray.is_key_pressed(KEY_R):
            self.reset()
        if pyray.is_key_pressed(KEY_P):
            self.paused = not self.paused
        if pyray.is_key_pressed(KEY_SPACE):
            self.step = True

    def update(self):
        if not self.paused or self.step:
            self.camera.update(self.vehicle)
            self.scheduler.update()
            self.step = False

            # w, x, y, z - x, y, z
            data = self.scheduler.value

            if data is not None:
                position = Vector(data[4], data[5], data[6])
                orientation = Quaternion(data[1], data[2], data[3], data[0])

                self.vehicle.update(position, orientation)

    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(COLORS.WHITE)

        pyray.begin_mode_3d(self.camera.camera)
        self.vehicle.render()
        self.draw_grid(CONFIG.GRID_SIZE, CONFIG.GRID_SPACING)

        pyray.end_mode_3d()
        pyray.end_drawing()

    def loop(self):
        while self.running:
            self.events()
            self.update()
            self.render()
