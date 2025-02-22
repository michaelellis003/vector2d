"""This is the vector2d package.

This package provides two classes for working with 2-dimensional vectors:
- Vector2d: A class for standard 2D vectors.
- ShortVector2d: A class for 2D vectors with shorter representation.

Attributes:
    __all__ (list): A list of public objects of that module, as interpreted by
        `import *`.
"""

from .short_vector2d import ShortVector2d
from .vector2d import Vector2d

__all__ = ['Vector2d', 'ShortVector2d']
