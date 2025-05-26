import pyray
from pyray import Vector3 as Vector, Vector4 as Quaternion
from raylib import CAMERA_PERSPECTIVE


class Camera:

    def __init__(self):
        self._camera = pyray.Camera3D()

        self._camera.position=Vector(4.0, 4.0, 4.0)
        self._camera.target=Vector(1.0, 0.0, 0.0)
        self._camera.up=Vector(0.0, 0.0, 1.0)
        self._camera.fovy=45.0
        self._camera.projection=CAMERA_PERSPECTIVE

    @property
    def camera(self):
        return self._camera

    def update(self, vehicle):
        rotation = pyray.matrix_transpose(pyray.quaternion_to_matrix(vehicle.orientation))

        distance = 8
        height = 3

        # Get back and up vectors from rotation matrix
        forward = Vector(rotation.m0, rotation.m4, rotation.m8)  # Z axis
        up = Vector(0.0, 0.0, 1.0)  # Y axis

        # Normalize just in case
        forward = pyray.vector3_normalize(forward)
        up = pyray.vector3_normalize(up)

        # Offset from vehicle position: back and up
        offset = pyray.vector3_scale(forward, -distance)
        offset = pyray.vector3_add(offset, pyray.vector3_scale(up, height))

        self._camera.position = pyray.vector3_add(vehicle.position, offset)
        self._camera.target = vehicle.position