# 3D matrix transformation modeling/animation exercise.

> The purpose of this exercise is to model and animate 2D transformations. Having already done this part [here](https://github.com/TomPlanche/2D_vector_translations), I decided to try it in 3D using [Blender](https://www.blender.org/).

## 1. TODOs
- [x] Create utility functions
  - [x] `console_print`:
    
    Function that prints a message in the blender console.
  - [x] `print`:

    Overload of the `print` function that prints in the console and in the blender console.
- [ ] Create classes.
  - [x] `ColumnVector`:

    Inherit from `numpy.array` and represents a 3d homogeneous column vector.
    - [x] `__init__`
    - [x] `__new__`:
      
        Overload of the `__new__` function to make sure the vector is a column vector.
    - [x] `__eq__`
    - [x] `__matmul__`:
      
        Overload of the `@` operator to make matrix multiplication.
  - [x] `ThreeDObject`:
    
      This class represents a 3D object and makes the connection between my code and Blender.
    - [x] `keyframe_insert(frame, _property)`:
      
        Function that inserts a keyframe for the object's desired property at the desired frame.
    - [x] `__enter__`:
      
        Function that is called when entering a `with` statement. It deselects all objects in blender.
    - [x] `__exit__`:
      
        Function that is called when exiting a `with` statement. It selects the object.
  - [x] `Point`:

    Inherits from `ColumnVector` and `ThreeDObject`. Represents a point in 3D space.
    - [x] `__init__`:
      
      The point can be initialized with a  `name`.
      It initializes both the `ColumnVector` and `ThreeDObject` classes and itseslf.
    - [x] `__new__`:
      
      Overload of the `__new__` function to make sure the point is a `Point`
    - [x] `place`:
        
        Function that places the point at the desired position in Blender.
    - [x] `update`:
      
      Function that updates the point's position in Blender.
    - [x] `angle_between(axis)`:
      
      Function that returns the angle created by the point, the origin and the axis.
    - [x] `translation(translation_vector)`:
      
      Function that translates the point by the desired vector.
    - [x] `scaling(scaling_vector)`:
      
      Function that scales the point by the desired vector.
    - [x] `rotation_x(angle)`:
      
      Function that rotates the point around the x axis by the desired angle.
    - [x] `rotation_y(angle)`:
      
      Function that rotates the point around the y axis by the desired angle.
    - [x] `rotation_z(angle)`:
      
      Function that rotates the point around the z axis by the desired angle.
    - [x] `determine_common_axis(point_1, point_2, point_3)`:
      
      Function that determines the common axis of the three points.
  - [x] `Edge`:
    
    Inherits from `ThreeDObject`. Represents an edge in 3D space.
    - [x] `__init__`:
      
      The edge can be initialized with a `name`.
      It initializes both the `ColumnVector` and `ThreeDObject` classes and itseslf.
    - [x] `place`:
      
      Function that places the edge at the desired position in Blender.
    - [x] `update`:
      
      Function that updates the edge's position in Blender.
  - [ ] `Cube`:
    
    Inherits from `ThreeDObject`. Represents a cube in 3D space.
- [ ] Animation
  - [x] Points animation
  - [ ] Edges animation
  - [ ] Cube animation
