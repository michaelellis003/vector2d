"""A module defining the Vector2d using single-precision floats.

This module contains the ShortVector2d class, which inherits from Vector2d
and provides the same functionality but uses single-precision floats for
storage. This can be useful in scenarios where memory usage is a concern.

Classes:
    ShortVector2d: A 2-dimensional vector class with single-precision float
                    storage.

Usage Example:
    >>> v1 = ShortVector2d(1.0, 2.0)
    >>> v2 = ShortVector2d(3.0, 4.0)
    >>> v1 + v2
    ShortVector2d(4.0, 6.0)
"""

from .vector2d import Vector2d


class ShortVector2d(Vector2d):
    """A short 2-dimensional vector class that inherits from Vector2d.

    This class is a lightweight version of Vector2d with the same functionality
    but using single-precision floats.

    __slots__ = () is declared to ensure instances of this subclass will have
    no __dict__ attribute, like the base class, saving memory.

    Attributes:
        typecode (str): The type code used for array representation, set to 'f'
                        for single-precision floats.
    """

    __slots__ = ()
    typecode = 'f'
