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


class ColumnVector(npa):
    """
    A column vector in 3D space.
    """
    def __init__(self, x: float, y: float, z: float):
        self[0] = x
        self[1] = y
        self[2] = z
        self[3] = 1

    def __new__(cls, x: float, y: float, z: float):
        obj = super(ColumnVector, cls).__new__(cls, (4,), np.float64)

        return obj

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __matmul__(self, other):
        return self @ other


class ThreeDObject:
    """
    A 3D object in 3D space.

    Args:
        threeDObject_name: The name of the 3D object.
    """
    def __init__(self, threeDObject_name: str = None):
        self.ref = None
        self.threeDObject_name = threeDObject_name if threeDObject_name else "unnamed_3D_object"

    def __str__(self):
        return self.threeDObject_name

    def __repr__(self):
        return self.threeDObject_name

    def __enter__(self):
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ref = bpy.context.object

        if self.threeDObject_name:
            # Rename the object
            self.ref.name = self.threeDObject_name

            # Display the name
            self.ref.show_name = True

        bpy.ops.object.select_all(action='DESELECT')

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


class Point(ColumnVector, ThreeDObject):
    """
    A point in 3D space.

    It inherits from the ColumnVector class and the ThreeDObject class.

    Args:
        x: The x coordinate of the point. (ColumnVector class)
        y: The y coordinate of the point. (ColumnVector class)
        z: The z coordinate of the point. (ColumnVector class)
        threeDObject_name: The name of the point. (ThreeDObject class)
    """
    def __init__(self, x: float, y: float, z: float, threeDObject_name: str = None, _type="PLAIN_AXES", radius=.25):
        ColumnVector.__init__(self, x, y, z)
        ThreeDObject.__init__(self, threeDObject_name)

        self.type = _type
        self.radius = radius

    def __new__(cls, x: float, y: float, z: float, threeDObject_name: str = None, _type="PLAIN_AXES"):
        obj = super(Point, cls).__new__(cls, x, y, z)

        return obj

    def __str__(self):
        name = f'"{self.threeDObject_name}"' if self.threeDObject_name else "Unnamed"
        return f"Point<{name}>({self[0]}, {self[1]}, {self[2]})"

    # def __repr__(self):
    #     """
    #     Return a string representation of the point.
    #     It uses threeDObject_name argument from it's ThreeDObject parent class.
    #
    #     Returns:
    #         (str): The string representation of the point.
    #
    #     Examples:
    #         >>> Point(1, 2, 3, "point_1")
    #         Point<"point_1">(1, 2, 3)
    #     """
    #     return self.__str__()

    def place(self):
        """
        Place the point in the scene.

        Returns:
            None
        """
        with self:
            bpy.ops.object.empty_add(
                type=self.type,
                radius=self.radius,
                location=(self[:-1]),
            )

    def update(self, _point=None):
        """
        Update the point in the scene AND the point's coordinates.

        Returns:
            None
        """
        if _point.any():
            self[0], self[1], self[2] = _point[0], _point[1], _point[2]
            self.ref.location = _point[:-1]

    def angle_between(self, axis: str = 'x') -> float:
        """
        Calculate the angle between the origin and the point along the specified axis.

        Args:
            axis: A string specifying the axis ('x', 'y', or 'z').

        Returns:
            angle: The angle in degrees between the origin and the point along the specified axis.
        """
        if axis not in ['x', 'y', 'z']:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")

        if axis == 'x':
            angle = np.degrees(np.arctan(self[1] / self[0]))

        elif axis == 'y':
            angle = np.degrees(np.arctan(self[0] / self[1]))
        else:  # axis == 'z'
            angle = np.degrees(np.arctan(
                np.sqrt(self[0] ** 2 + self[1] ** 2) / self[2]
            ))

        return 0 if np.isnan(angle) else angle

    def translation(self, c_vector: ColumnVector):
        """
        Translate the point by a column vector.

        Args:
            c_vector: The column vector to translate the point by.

        Returns:
            None
        """
        translation_matrix = np.identity(4)
        translation_matrix[0][3] = c_vector[0]
        translation_matrix[1][3] = c_vector[1]
        translation_matrix[2][3] = c_vector[2]

        final_matrix = translation_matrix @ np.array(self)

        self.update(final_matrix)

    def scaling(self, c_vector: ColumnVector):
        """
        Homothety the point by a column vector.

        Args:
            c_vector: The column vector to homothety the point by.

        Returns:
            None
        """
        homothety_matrix = np.identity(4)
        homothety_matrix[0][0] = c_vector[0]
        homothety_matrix[1][1] = c_vector[1]
        homothety_matrix[2][2] = c_vector[2]

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


def determine_common_axis(_point_1: Point, _point_2: Point, _point_3: Point) -> str:
    """
    Determine the common axis between the three points.

    Args:
        _point_1: The first point.
        _point_2: The second point.
        _point_3: The third point.

    Returns:
        axis: The common axis between the three points.
    """
    if _point_1[0] == _point_2[0] == _point_3[0]:
        axis = 'x'
    elif _point_1[1] == _point_2[1] == _point_3[1]:
        axis = 'y'
    elif _point_1[2] == _point_2[2] == _point_3[2]:
        axis = 'z'
    else:
        raise ValueError("The three points don't have a common axis.")

    return axis


class Edge(ThreeDObject):
    """
    An edge in 3D space.
    The edge is represented by two points.
    The first point should be the closest to the origin.
    The third point should be the furthest from the origin.

    The angle between the first point and the second point should be
    the one between the x-axis and line passing through the first point
    and the second point.

    The angle between the first point and the third point should be
    the one between the y-axis and line passing through the first point
    and the third point.

    The angle between the first point and the fourth point should be
    the one between the z-axis and line passing through the first point
    and the fourth point.

    Args:
        _point_1: The first point of the edge.
        _point_2: The second point of the edge.
        _point_3: The third point of the edge.
        _point_4: The fourth point of the edge.
        threeDObject_name: The name of the edge.
    """
    def __init__(
            self,
            _point_1: Point, _point_2: Point, _point_3: Point, _point_4: Point,
            threeDObject_name: str = None
    ):
        super().__init__(threeDObject_name)
        self.points = [_point_1, _point_2, _point_3, _point_4]
        self.plane_ref = None  # Store a reference to the plane object

    def __enter__(self):
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ref = bpy.context.object

        if self.threeDObject_name:
            # Rename the object
            self.ref.name = self.threeDObject_name

            # Display the name
            self.ref.show_name = True

        bpy.ops.object.select_all(action='DESELECT')

    def keyframe_insert(self, frame: int, _property: str = "location"):
        """
        Insert a keyframe.

        Args:
            frame: The frame to insert the keyframe at.
            _property: The property to insert the keyframe for.

        Returns:
            None
        """
        if self.ref:
            self.ref.keyframe_insert(data_path=_property, frame=frame, index=-1)

    def place(self):
        """
        Place the edge in the scene.

        Returns:
            None
        """
        with self:
            # The location is the middle of the two points
            # hence the primitive_plane_add() function location argument
            # is the middle of the two points
            final_location = (self.points[3] + self.points[0]) / 2

            needed_rotation = determine_common_axis(*self.points[:3])

            if needed_rotation == 'z':
                final_rotation = (0, 0, 0)
            elif needed_rotation == 'y':
                final_rotation = (np.radians(90), 0, 0)
            else:  # needed_rotation == 'x'
                final_rotation = (0, np.radians(90), 0)

            bpy.ops.mesh.primitive_plane_add(
                size=1,
                location=final_location[:-1],
                rotation=final_rotation,
            )

    def update(self, _points: list[Point] = None):
        """
        Update the edge in the scene.

        Returns:
            None
        """
        print(f"Updating {self.threeDObject_name}")

        if _points:
            print(f"Updating {self.threeDObject_name} with {_points}")
            self.points = _points

        # Update the plane object using the stored reference
        if self.ref:
            print(f"Updating {self.threeDObject_name} plane_ref")
            final_location = (self.points[3] + self.points[0]) / 2
            self.ref.location = final_location[:-1]


# class Cube(ThreeDObject):
#     """
#     Cube in 3D space.
#
#     Args:
#         _points: The points of the cube. The points must be in the following order:
#             0: (0, 0, 0)
#             1: (1, 0, 0)
#             2: (0, 1, 0)
#             3: (1, 1, 0)
#             4: (0, 0, 1)
#             5: (1, 0, 1)
#             6: (0, 1, 1)
#             7: (1, 1, 1)
#         threeDObject_name: The name of the cube.
#     """
#     def __init__(self, _points: list[Point], threeDObject_name: str = None, solid: bool = False):
#         super().__init__(threeDObject_name)
#         self.points = _points
#         self.solid = solid
#
#         self.size = (_points[-1] - _points[0])[0]
#         self.edges = [
#             Edge(*_points[:4], threeDObject_name="edge_bottom"),
#             Edge(*_points[4:], threeDObject_name="edge_top"),
#             Edge(_points[0], _points[4], _points[2], _points[6], threeDObject_name="edge_y_1"),
#             Edge(_points[1], _points[5], _points[3], _points[7], threeDObject_name="edge_y_2"),
#             Edge(_points[0], _points[1], _points[4], _points[5], threeDObject_name="edge_x_1"),
#             Edge(_points[2], _points[3], _points[6], _points[7], threeDObject_name="edge_4"),
#         ]
#
#     def keyframe_insert(self, frame: int, _property: str = "location"):
#         """
#         Override the ThreeDObject class keyframe_insert() method.
#         Insert a keyframe.
#
#         Args:
#             frame: The frame to insert the keyframe at.
#             _property: The property to insert the keyframe for.
#
#         Returns:
#             None
#         """
#         if self.solid:
#             for edge in self.edges:
#                 edge.keyframe_insert(frame, _property)
#
#     def place(self):
#         """
#         Place the cube in the scene.
#
#         Returns:
#             None
#         """
#         if self.solid:
#             # Place the cube, the origin of the cube is at the center of the cube
#             # so, we need to translate it by half of the size of the cube
#             # origin = (self.points[0] + self.points[-1]) / 2
#             # bpy.ops.mesh.primitive_cube_add(
#             #     size=self.size,
#             #     location=origin[:-1],
#             # )
#
#             for edge in self.edges:
#                 edge.place()
#
#     def update(self, _points: list[Point] = None):
#         """
#         Update the cube in the scene.
#
#         Returns:
#             None
#         """
#         if _points:
#             self.points = _points
#             self.edges = [
#                 Edge(*_points[:4], threeDObject_name="edge_bottom"),
#                 Edge(*_points[4:], threeDObject_name="edge_top"),
#                 Edge(_points[0], _points[4], _points[2], _points[6], threeDObject_name="edge_y_1"),
#                 Edge(_points[1], _points[5], _points[3], _points[7], threeDObject_name="edge_y_2"),
#                 Edge(_points[0], _points[1], _points[4], _points[5], threeDObject_name="edge_x_1"),
#                 Edge(_points[2], _points[3], _points[6], _points[7], threeDObject_name="edge_4"),
#             ]
#
#         # update the cube's reference
#         if self.solid:
#             # Place the cube, the origin of the cube is at the center of the cube
#             # so, we need to translate it by half of the size of the cube
#             # origin = (self.points[0] + self.points[-1]) / 2
#             # bpy.ops.mesh.primitive_cube_add(
#             #     size=self.size,
#             #     location=origin[:-1],
#             # )
#
#             for edge in self.edges:
#                 edge.update()


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

ANIM_FRAMES = ANGLE_ANIMATION_FRAMES + 1

# Create the cube
# cube_1 = Cube(points, "cube_1", solid=True)
# cube_1.place()
# cube_1.keyframe_insert(PADDING_FRAMES)

for point in points:
    point.place()

    point.keyframe_insert(PADDING_FRAMES)
    point.translation(ColumnVector(0, 0, 2))
    point.keyframe_insert(ANIM_1_END)


# cube_1.update(points)
# cube_1.keyframe_insert(ANIM_1_END)

# Animate the cube rotating around the z-axis
#     for i in range(1, ANGLE_ANIMATION_FRAMES + 1):
#         point.keyframe_insert(ANIM_2_START + i)
#         point.rotation_z(Z_ANGLE / ANGLE_ANIMATION_FRAMES)


bpy.context.scene.frame_end = TOTAL_FRAMES

