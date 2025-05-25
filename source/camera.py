import pyray
from pyray import Vector3 as Vector, Vector4 as Quaternion
from raylib import CAMERA_PERSPECTIVE


class Camera:

    def __init__(self):
        self._camera = pyray.Camera3D()

        self._camera.position=Vector(4.0, 4.0, 4.0)
        self._camera.target=Vector(0.0, 1.0, 0.0)
        self._camera.up=Vector(0.0, 1.0, 0.0)
        self._camera.fovy=45.0
        self._camera.projection=CAMERA_PERSPECTIVE

    @property
    def camera(self):
        return self._camera

    def update(self, vehicle):
        rotation = pyray.quaternion_to_matrix(vehicle.orientation)

        distance = 6
        height = 2

        # Get back and up vectors from rotation matrix
        forward = pyray.Vector3(rotation.m2, rotation.m6, rotation.m10)  # Z axis
        up = pyray.Vector3(rotation.m1, rotation.m5, rotation.m9)  # Y axis

        # Normalize just in case
        forward = pyray.vector3_normalize(forward)
        up = pyray.vector3_normalize(up)

        # Offset from vehicle position: back and up
        offset = pyray.vector3_scale(forward, -distance)
        offset = pyray.vector3_add(offset, pyray.vector3_scale(up, height))

        self._camera.position = pyray.vector3_add(vehicle.position, offset)
        self._camera.target = vehicle.position