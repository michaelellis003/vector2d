"""This module provides a class to represent 2-dimensional vectors.

The bulk of this code is from chapter 11
of the 2nd edition of Fluent Python by Luciano Ramalho.

Classes:
    Vector2d: A class to represent a 2-dimensional vector.

Usage Example:
    >>> v1 = Vector2d(3, 4)
    >>> v2 = Vector2d(1, 2)
    >>> v1 + v2
    Vector2d(4.0, 6.0)
    >>> abs(v1)
    5.0
    >>> format(v1, 'p')
    '<5.0, 0.9272952180016122>'
"""

import math
from array import array
from collections.abc import Iterable, Iterator
from typing import Any


class Vector2d:
    """A class to represent a 2-dimensional vector.

    This class provides a comprehensive implementation of a 2D vector,
    supporting various operations and features such as hashability,
    positional pattern matching, and efficient memory usage with __slots__.

    The class currently does not support any mathematical operations like
    addition, subtraction, scalar multiplication, dot product, or cross
    product, etc. These can be added as needed.

    Features:
        Hashability:
            Hashability allows instances of Vector2d to be used as keys in
            dictionaries and stored in sets. This is achieved by implementing
            the __hash__ method.

    Example:
                >>> v1 = Vector2d(3, 4)
                >>> v2 = Vector2d(3, 4)
                >>> hash(v1) == hash(v2)
                True
                >>> {v1: 'vector1'}[v2]
                'vector1'

        Positional Pattern Matching:
            Positional pattern matching allows instances of Vector2d to be
            matched in patterns using their positional attributes. This is
            enabled by the __match_args__ attribute.

    Example:
                >>> def match_vector(v):
                ...     match v:
                ...         case Vector2d(0, 0):
                ...             print(f'{v!r} is null')
                ...         case Vector2d(0):
                ...             print(f'{v!r} is vertical')
                ...         case Vector2d(_, 0):
                ...             print(f'{v!r} is horizontal')
                ...         case Vector2d(x, y) if x == y:
                ...             print(f'{v!r} is diagonal')
                ...         case _:
                ...             print(f'{v!r} is awesome')

        __slots__:
            The __slots__ attribute is used to declare data members
            (like __x and __y) and prevents the creation of __dict__ for each
            instance, saving memory.

    Attributes:
        typecode (str): A class attribute used when converting Vector2d
            instances to/from bytes.
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.

    Methods:
        __init__(x, y):
            Initializes a 2D vector with x and y coordinates.
        x:
            Gets the x-coordinate of the vector.
        y:
            Gets the y-coordinate of the vector.
        __hash__():
            Returns a hash value for the vector, making it hashable.
        __iter__():
            Returns an iterator over the x and y coordinates.
        __repr__():
            Returns a string representation of the vector for debugging.
        __str__():
            Returns a string representation of the vector for users.
        __bytes__():
            Returns a bytes object representing the vector.
        __eq__(other):
            Checks if two vectors are equal.
        __abs__():
            Returns the magnitude of the vector.
        __bool__():
            Returns the truth value of the vector.
        __format__(format_spec):
            Formats the vector according to the given format specification.
        angle():
            Calculates the angle of the vector in radians.
        frombytes(octets):
            Creates a Vector2d instance from a bytes object.
    """

    typecode = 'd'

    # Without __match_args__ the Vector2d instances are compatible with with
    # keyword class patterns but not positional patterns. Adding
    # __match_args__ makes Vector2d compatible with postional pattern matching
    __match_args__ = ('x', 'y')

    # __slots__ is a class attribute that can save memory by predefining the
    # attributes of a class. By default, Python stores the attributes of each
    # instance in a dict named __dict__. This is convenient, but it consumes
    # a lot of memory because dictionaries are memory-inefficient. But if you
    # predefine a class atribute __slots__  holding a sequence of attribute
    # names, Python will use an alternative storage model for the instance
    # attributes. The attributes named in __slots__ are stored in a hidden-
    # array or references that use less memory than a dictionary.
    __slots__ = ('__x', '__y')

    def __init__(self, x: float, y: float) -> None:
        """Initialize a 2D vector with x and y coordinates.

        Converting x and y to float in __init__ catches bugs early. The x and y
        coordinates are private.

        Args:
            x (float or int): The x-coordinate of the vector.
            y (float or int): The y-coordinate of the vector.

        Raises:
            ValueError: If x or y cannot be converted to float.
        """
        self.__x = float(x)
        self.__y = float(y)

    @property  # property decorator marks the getter method of a property.
    def x(self) -> float:
        """Gets the x-coordinate of the vector.

        Returns:
            float: The x-coordinate of the vector.
        """
        return self.__x

    @property
    def y(self) -> float:
        """Gets the y-coordinate of the vector.

        Returns:
            float: The y-coordinate of the vector.
        """
        return self.__y

    def __hash__(self) -> int:
        """Return a hash value for the vector.

        __hash__ supports hashability. Vector2d is also immutable to support
        hashability. It is not reuqired to make the class immutable to be
        hashable, but the value of a hashable object should not change, so it
        is a good idea to make it immutable.

        Returns:
            int: The hash value of the vector.
        """
        return hash((self.x, self.y))

    def __iter__(self) -> Iterator[float]:
        """Return an iterator over the x and y coordinates.

        __iter__ makes a Vector2d iterable; this is what makes unpacking work
        (e.g., x, y = my_vector).

        Yields:
            int or float: The x and y coordinates of the vector.
        """
        return (i for i in (self.x, self.y))

    def __repr__(self) -> str:
        """Return a string representation of the vector.

        __repr__ builds a string by interpolating the components with {!r} to
        get their repr; because Vector2d is iterable, *self feeds the x and y
        components to format.

        __repr__ supports repr(). Returns a string representing the object as
        a developer wants to see it. It's what you get when the Python console
        or debugger shows an object.

        Returns:
            str: A string representation of the vector.
        """
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self) -> str:
        """Return a string representation of the vector.

        __str__ supports str(). Returns a string representing the object as
        a user wants to see it. It's what you get when you print an object.

        Returns:
            str: A string representation of the vector.
        """
        return str(tuple(self))

    def __bytes__(self) -> bytes:
        """Return a bytes object representing the vector.

        __bytes__ is analogous to __str__. It is called by bytes() to get the
        object represented as a byte string. In this method the typecode is
        creates a bytes representation of the vector's typecode by converting
        its ASCII value using ord() and then wrapping it in a bytes object.
        For example, bytes([ord('d')]) returns b'd' when printed to the
        console. The method then it appends the binary representation of the
        underlying array data by calling bytes() on the array. The end result
        is a bytes object of the array data prefixed by the typecode.

        Returns:
            bytes: A binary representation of the vector.
        """
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, other: Any) -> bool:
        """Check if two vectors are equal.

        __eq__ supports equality testing. It is called by the == operator. It
        compares the components of the two Vector2d objects. This
        implementation is efficient because it only compares the x and y
        attributes of the objects.

        WARNING: This implementation also returns True when comparing a
        Vector2d tto other iterables holding the same numeric values. For
        example, Vector2d(1.1, 2.2) == [1.1, 2.2] returns True.

        Args:
            other (Vector2d): The vector to compare to.

        Returns:
            bool: True if the vectors are equal, False otherwise.
        """
        if not isinstance(other, Iterable):
            return NotImplemented
        return tuple(self) == tuple(other)

    def __abs__(self) -> float:
        """Return the magnitude of the vector.

        __abs__ supports the abs() function. It calculates the magnitude of
        the vector using the Pythagorean theorem.

        Returns:
            float: The magnitude of the vector.
        """
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        """Return the truth value of the vector.

        __bool__ supports truth testing. It returns False if the magnitude of
        the vector is zero, True otherwise.

        Returns:
            bool: True if the vector is not the zero vector, False otherwise.
        """
        return bool(abs(self))

    def __format__(self, format_spec='') -> str:
        """Format the vector according to the given format specification.

        Args:
            format_spec (str): The format specification. If it ends with 'p',
                the vector will be formatted as polar coordinates.
                Otherwise, it will be formatted as Cartesian coordinates.

        Returns:
            str: The formatted string representation of the vector.
        """
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self  # unpack x and y from self
            outer_fmt = '({}, {})'

        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(*components)

    def angle(self) -> float:
        """Calculate the angle of the vector in radians.

        This method returns the angle between the positive x-axis and the
        vector represented by this instance. The angle is measured in radians
        and is calculated using the arctangent of the y-coordinate divided by
        the x-coordinate.

        Returns:
            float: The angle of the vector in radians.
        """
        return math.atan2(self.y, self.x)

    # classmethod decorator modifies the method so that it can be called on
    # the class.
    @classmethod
    def frombytes(cls, octets: bytes) -> 'Vector2d':
        """Create a Vector2d instance from a bytes object.

        This class method is used to deserialize a bytes object back into a
        Vector2d instance. It extracts the typecode from the first byte and
        then reads the remaining bytes as an array of the specified typecode.

        The `memoryview` class is a shared-memory sequence type that lets you
        handle slices of arrays without copying bytes. It allows you to share
        memory between data-structures without first copying. This is very
        important for large datasets.

        The `memoryview.cast` method lets you change the way the bytes are
        read or written as units without moving bits around.

        Args:
            octets (bytes): A bytes object containing the serialized vector.

        Returns:
            Vector2d: A new Vector2d instance created from the bytes object.
        """
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)  # type: ignore
        return cls(*memv)
