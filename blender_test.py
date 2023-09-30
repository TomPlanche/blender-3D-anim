"""
The goal of this file is to represent a simple cube
in blender using python.
It will be represented by points and edges.
"""
import bpy
from bpy import context
import numpy as np
import builtins as __builtin__

npa = np.ndarray


def console_print(*args, **kwargs) -> None:
    """
    Print to the console.

    Args:
        *args: The arguments to print.
        **kwargs: The keyword arguments to print.

    Returns:
        None
    """
    for a in context.screen.areas:
        if a.type == 'CONSOLE':
            c = {'area': a, 'space_data': a.spaces.active, 'region': a.regions[-1], 'window': context.window,
                 'screen': context.screen}
            s = " ".join([str(arg) for arg in args])
            for line in s.split("\n"):
                bpy.ops.console.scrollback_append(c, text=line)


def print(*args, **kwargs):
    """Console print() function."""

    console_print(*args, **kwargs)  # to py consoles
    __builtin__.print(*args, **kwargs)  # to system console


class Vector(npa):
    """
    A vector in 3D space.
    """
    def __init__(self, x: float, y: float, z: float):
        self[0] = x
        self[1] = y
        self[2] = z
        self[3] = 1

    def __new__(cls, x: float, y: float, z: float):
        obj = super(Vector, cls).__new__(cls, (4,), np.float64)

        return obj

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __matmul__(self, other):
        return self @ other


class ThreeDObject:
    """
    A 3D object in 3D space.
    """
    def __init__(self, name: str = None):
        self.ref = None
        self.name = name

    def keyframe_insert(self, frame: int, _property: str = "location"):
        """
        Insert a keyframe.

        Args:
            frame: The frame to insert the keyframe at.
            _property: The property to insert the keyframe for.

        Returns:
            None
        """
        self.ref.keyframe_insert(data_path=_property, frame=frame, index=-1)

    def __enter__(self):
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ref = bpy.context.object

        if self.name:
            # Rename the object
            self.ref.name = self.name

            # Display the name
            self.ref.show_name = True

        bpy.ops.object.select_all(action='DESELECT')


class Point(Vector, ThreeDObject):
    """
    A point in 3D space.

    It inherits from the Vector class and the ThreeDObject class.

    Args:
        x: The x coordinate of the point. (Vector class)
        y: The y coordinate of the point. (Vector class)
        z: The z coordinate of the point. (Vector class)
        name: The name of the point. (ThreeDObject class)
    """
    def __init__(self, x: float, y: float, z: float, name: str = None):
        super().__init__(x, y, z)
        ThreeDObject.__init__(self, name=name)

    def __new__(cls, x: float, y: float, z: float, name: str = None):
        obj = super(Point, cls).__new__(cls, x, y, z)

        return obj

    def place(self):
        """
        Place the point in the scene.

        Returns:
            None
        """
        with self:
            bpy.ops.object.empty_add(location=(self[:-1]))

    def update(self, _point=None):
        """
        Update the point in the scene AND the point's coordinates.

        Returns:
            None
        """
        if _point.any():
            self[0], self[1], self[2] = _point[0], _point[1], _point[2]
            self.ref.location = _point[:-1]

    def translation(self, vector: Vector):
        """
        Translate the point by a vector.

        Args:
            vector: The vector to translate the point by.

        Returns:
            None
        """
        translation_matrix = np.identity(4)
        translation_matrix[0][3] = vector[0]
        translation_matrix[1][3] = vector[1]
        translation_matrix[2][3] = vector[2]

        final_matrix = translation_matrix @ np.array(self)

        self.update(final_matrix)

    def homohety(self, vector: Vector):
        """
        Homothety the point by a vector.

        Args:
            vector: The vector to homothety the point by.

        Returns:
            None
        """
        homothety_matrix = np.identity(4)
        homothety_matrix[0][0] = vector[0]
        homothety_matrix[1][1] = vector[1]
        homothety_matrix[2][2] = vector[2]

        final_matrix = homothety_matrix @ np.array(self)

        self.update(final_matrix)

    def rotation_x(self, angle: float):
        """
        Rotate the point around the x-axis.

        Args:
            angle: The angle to rotate the point by.

        Returns:
            None
        """
        angle = np.radians(angle)

        rotation_matrix = np.identity(4)
        rotation_matrix[1][1] = np.cos(angle)
        rotation_matrix[1][2] = -np.sin(angle)
        rotation_matrix[2][1] = np.sin(angle)
        rotation_matrix[2][2] = np.cos(angle)

        final_matrix = rotation_matrix @ np.array(self)

        self.update(final_matrix)

    def rotation_y(self, angle: float):
        """
        Rotate the point around the y-axis.

        Args:
            angle: The angle to rotate the point by.

        Returns:
            None
        """
        angle = np.radians(angle)

        rotation_matrix = np.identity(4)
        rotation_matrix[0][0] = np.cos(angle)
        rotation_matrix[0][2] = np.sin(angle)
        rotation_matrix[2][0] = -np.sin(angle)
        rotation_matrix[2][2] = np.cos(angle)

        final_matrix = rotation_matrix @ np.array(self)

        self.update(final_matrix)

    def rotation_z(self, angle: float):
        """
        Rotate the point around the z-axis.

        Args:
            angle: The angle to rotate the point by in degrees.

        Returns:
            None
        """
        angle = np.radians(angle)

        rotation_matrix = np.identity(4)
        rotation_matrix[0][0] = np.cos(angle)
        rotation_matrix[0][1] = -np.sin(angle)
        rotation_matrix[1][0] = np.sin(angle)
        rotation_matrix[1][1] = np.cos(angle)

        final_matrix = rotation_matrix @ np.array(self)

        self.update(final_matrix)


class Cube(ThreeDObject):
    """
    Cube in 3D space.

    Args:
        _points: The points of the cube. The points must be in the following order:
            0: (0, 0, 0)
            1: (1, 0, 0)
            2: (0, 1, 0)
            3: (1, 1, 0)
            4: (0, 0, 1)
            5: (1, 0, 1)
            6: (0, 1, 1)
            7: (1, 1, 1)
        name: The name of the cube.
    """
    def __init__(self, _points: list[Point], name: str = None):
        super().__init__(name)
        self.points = _points
        self.size = (points[-1] - points[0])[0]

    def place(self):
        """
        Place the cube in the scene.

        Returns:
            None
        """
        with self:
            # Place the cube, the origin of the cube is at the center of the cube
            # so, we need to translate it by half of the size of the cube
            origin = (self.points[0] + self.points[-1]) / 2
            bpy.ops.mesh.primitive_cube_add(
                size=self.size,
                location=origin[:-1],
            )

    def update(self, _points: list[Point] = None):
        """
        Update the cube in the scene.

        Returns:
            None
        """
        if _points:
            print("Updating the cube's points")
            self.points = _points

        # update the cube's reference
        origin = (self.points[0] + self.points[-1]) / 2

        self.ref.location = origin[:-1]


# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

points = [
    Point(0, 0, 0, "p_1"),
    Point(1, 0, 0, "p_2"),
    Point(0, 1, 0, "p_3"),
    Point(1, 1, 0, "p_4"),
    Point(0, 0, 1, "p_5"),
    Point(1, 0, 1, "p_6"),
    Point(0, 1, 1, "p_7"),
    Point(1, 1, 1, "p_8")
]

DESIRED_FPS = 24
PADDING_FRAMES = 2 * DESIRED_FPS  # 2 seconds
ANIMATION_FRAMES = 5 * DESIRED_FPS  # 5 seconds

Z_ANGLE = 90  # degrees
DEGREES_PER_SECOND = 30
ANGLE_ANIMATION_FRAMES = Z_ANGLE // DEGREES_PER_SECOND * DESIRED_FPS

ANIM_1_END = ANIMATION_FRAMES + PADDING_FRAMES
ANIM_2_START = ANIM_1_END + PADDING_FRAMES
ANIM_2_END = ANIM_2_START + Z_ANGLE // DEGREES_PER_SECOND * DESIRED_FPS

TOTAL_FRAMES = ANIM_2_END + PADDING_FRAMES


for point in points:
    point.place()

    point.keyframe_insert(PADDING_FRAMES)
    point.translation(Vector(0, 0, 2))
    point.keyframe_insert(ANIM_1_END)

    # Animate the cube rotating around the z-axis
    for i in range(1, ANGLE_ANIMATION_FRAMES + 1):
        point.keyframe_insert(ANIM_2_START + i)
        point.rotation_z(Z_ANGLE / ANGLE_ANIMATION_FRAMES)


bpy.context.scene.frame_end = TOTAL_FRAMES
