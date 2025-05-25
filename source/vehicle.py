import pyray
from pyray import Vector3 as Vector, Vector4 as Quaternion

from source.data import CONFIG, COLORS, VEHICLE


class Vehicle:

    def __init__(self):
        self.position = Vector()
        self.orientation = Quaternion()

        self.length = VEHICLE.FRONT_LENGTH + VEHICLE.REAR_LENGTH
        self.width = (VEHICLE.FRONT_TRACK + VEHICLE.REAR_TRACK) / 2.0
        self.height = VEHICLE.CHASSIS_HEIGHT

    def update(self):
        pass

    def render(self):
        pyray.draw_cube(self.position, self.width, self.height, self.length, COLORS.RED)
        pyray.draw_cube_wires(self.position, self.width, self.height, self.length, COLORS.BLACK)





