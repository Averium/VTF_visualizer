import pyray
from mpl_toolkits.mplot3d.proj3d import transform
from pyray import Vector3 as Vector, Vector4 as Quaternion

from source.data import CONFIG, COLORS, VEHICLE


class Vehicle:

    def __init__(self):
        self.position = Vector(0.0, 0.0, VEHICLE.WHEEL_RADIUS * 2.0)
        self.orientation = Quaternion(0.0, 0.0, 1.0, 0.0)

        self.length = VEHICLE.FRONT_LENGTH + VEHICLE.REAR_LENGTH + VEHICLE.WHEEL_RADIUS * 2.0
        self.width = (VEHICLE.FRONT_TRACK + VEHICLE.REAR_TRACK) / 2.0
        self.height = VEHICLE.CHASSIS_HEIGHT
        self.shift = (VEHICLE.FRONT_LENGTH - VEHICLE.REAR_LENGTH) / 2.0

        self.r_fl = Vector(+ VEHICLE.FRONT_LENGTH, + VEHICLE.FRONT_TRACK / 2.0, - VEHICLE.WHEEL_RADIUS - VEHICLE.SUSPENSION_LENGTH)
        self.r_fr = Vector(+ VEHICLE.FRONT_LENGTH, - VEHICLE.FRONT_TRACK / 2.0, - VEHICLE.WHEEL_RADIUS - VEHICLE.SUSPENSION_LENGTH)
        self.r_rl = Vector(- VEHICLE.REAR_LENGTH, + VEHICLE.REAR_TRACK / 2.0, - VEHICLE.WHEEL_RADIUS - VEHICLE.SUSPENSION_LENGTH)
        self.r_rr = Vector(- VEHICLE.REAR_LENGTH, - VEHICLE.REAR_TRACK / 2.0, - VEHICLE.WHEEL_RADIUS - VEHICLE.SUSPENSION_LENGTH)

    def update(self, position, orientation):
        self.position = position
        self.orientation = orientation

    def render(self):
        shift = Vector((VEHICLE.FRONT_LENGTH - VEHICLE.REAR_LENGTH) / 2.0, 0, 0)
        position = pyray.vector3_add(self.position, shift)

        rotation = pyray.quaternion_to_matrix(self.orientation)
        translation = pyray.matrix_translate(position.x, position.y, position.z)

        cube_mesh = pyray.gen_mesh_cube(self.length, self.width, self.height)
        cube_model = pyray.load_model_from_mesh(cube_mesh)
        cube_model.transform = pyray.matrix_multiply(rotation, translation)

        pyray.draw_model(cube_model, Vector(0.0, 0.0, 0.0), 1, COLORS.GREY)

        for vector in (): #(self.r_fl, self.r_fr, self.r_rl, self.r_rr):
            spindle_direction = pyray.vector3_normalize(Vector(0.0, -vector.y, 0.0))
            spindle_vector = pyray.vector3_scale(spindle_direction, 0.15)
            corner_position = pyray.vector3_add(self.position, vector)

            wheel_left_end = pyray.vector3_add(corner_position, spindle_vector)
            wheel_right_end = pyray.vector3_subtract(corner_position, spindle_vector)

            pyray.draw_cylinder_ex(wheel_left_end, wheel_right_end, VEHICLE.WHEEL_RADIUS, VEHICLE.WHEEL_RADIUS, 16, COLORS.BLACK)
            pyray.draw_cylinder_wires_ex(wheel_left_end, wheel_right_end, VEHICLE.WHEEL_RADIUS, VEHICLE.WHEEL_RADIUS, 16, COLORS.GREY)






