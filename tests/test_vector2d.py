"""This module contains unit tests for the Vector2d class."""

import math

import pytest  # type: ignore

from vector2d import Vector2d


class TestVector2d:
    """A test suite for the Vector2d class.

    Methods:
        - test_constructor: Test Vector2d constructor with various inputs.
        - test_immutability: Test that Vector2d objects are immutable.
        - test_iter: Test iteration unpacking.
        - test_repr: Test string representation via repr().
        - test_str: Test string representation via str().
        - test_bytes: Test bytes conversion.
        - test_eq: Test equality comparisons.
        - test_abs: Test absolute value (magnitude).
        - test_bool: Test boolean value.
        - test_hash: Test hash functionality.
        - test_angle: Test angle calculation.
        - test_format: Test custom formatting.
        - test_match_args: Test that the object has __match_args__ for pattern matching.
        - test_slots: Test that the class uses __slots__ and has no __dict__.
    """

    def test_constructor(self):
        """Test Vector2d constructor with various inputs."""
        v = Vector2d(3, 4)
        assert v.x == 3.0
        assert v.y == 4.0

        # Test with floats
        v = Vector2d(3.5, 4.2)
        assert v.x == 3.5
        assert v.y == 4.2

        # Test with string conversions
        v = Vector2d('3', '4')
        assert v.x == 3.0
        assert v.y == 4.0

        # Test constructor with invalid input
        with pytest.raises(ValueError):
            Vector2d('three', 'four')

    def test_immutability(self):
        """Test that Vector2d objects are immutable."""
        v = Vector2d(3, 4)
        with pytest.raises(AttributeError):
            v.x = 7
        with pytest.raises(AttributeError):
            v.y = 9

    def test_iter(self):
        """Test iteration unpacking."""
        v = Vector2d(3, 4)
        x, y = v
        assert x == 3.0
        assert y == 4.0

        # Test conversion to tuple via iteration
        t = tuple(v)
        assert t == (3.0, 4.0)

    def test_repr(self):
        """Test string representation via repr()."""
        v = Vector2d(3, 4)
        assert repr(v) == 'Vector2d(3.0, 4.0)'

        # Make sure eval works on the repr result
        v2 = eval(repr(v))
        assert isinstance(v2, Vector2d)
        assert v.x == v2.x and v.y == v2.y

    def test_str(self):
        """Test string representation via str()."""
        v = Vector2d(3, 4)
        assert str(v) == '(3.0, 4.0)'

    def test_bytes(self):
        """Test bytes conversion."""
        v = Vector2d(3, 4)
        b = bytes(v)
        # First byte is typecode 'd', followed by 3.0 and 4.0 as doubles
        assert b[0] == ord('d')

        # Test round-trip conversion
        v2 = Vector2d.frombytes(b)
        assert v.x == v2.x and v.y == v2.y

    def test_eq(self):
        """Test equality comparisons."""
        v1 = Vector2d(3, 4)
        v2 = Vector2d(3, 4)
        v3 = Vector2d(5, 6)

        assert v1 == v2
        assert v1 != v3

        # Test equality with other iterables
        assert v1 == (3.0, 4.0)
        assert v1 == [3.0, 4.0]

    def test_abs(self):
        """Test absolute value (magnitude)."""
        v = Vector2d(3, 4)
        assert abs(v) == 5.0

        v = Vector2d(0, 0)
        assert abs(v) == 0.0

    def test_bool(self):
        """Test boolean value."""
        v1 = Vector2d(3, 4)
        v2 = Vector2d(0, 0)

        assert bool(v1) is True
        assert bool(v2) is False

    def test_hash(self):
        """Test hash functionality."""
        v1 = Vector2d(3, 4)
        v2 = Vector2d(3, 4)
        v3 = Vector2d(3.01, 4)

        # Same values should have same hash
        assert hash(v1) == hash(v2)

        # Different values should have different hash (not guaranteed but highly likely)
        assert hash(v1) != hash(v3)

        # Test as dictionary key
        d = {v1: 'vector1'}
        assert d[v2] == 'vector1'

        # Test in set
        s = {v1, v2, v3}
        assert len(s) == 2  # v1 and v2 should be considered the same element

    def test_angle(self):
        """Test angle calculation."""
        # Horizontal vector (0 degrees/radians)
        v = Vector2d(1, 0)
        assert v.angle() == 0.0

        # Vertical vector (90 degrees/pi/2 radians)
        v = Vector2d(0, 1)
        assert math.isclose(v.angle(), math.pi / 2)

        # 45 degree vector
        v = Vector2d(1, 1)
        assert math.isclose(v.angle(), math.pi / 4)

        # Test in different quadrants
        v = Vector2d(-1, 0)  # 180 degrees
        assert math.isclose(v.angle(), math.pi)

        v = Vector2d(0, -1)  # 270 degrees
        assert math.isclose(v.angle(), -math.pi / 2)

    def test_format(self):
        """Test custom formatting."""
        v = Vector2d(1, 0)

        # Default format (Cartesian)
        assert format(v) == '(1.0, 0.0)'

        # Polar format
        polar = format(v, 'p')
        assert polar == '<1.0, 0.0>'

        # Test with precision formatting
        v = Vector2d(1, 1)
        assert format(v, '.2f') == '(1.00, 1.00)'
        assert (
            format(v, '.2fp') == '<1.41, 0.79>'
        )  # Magnitude ~1.414, angle ~0.785

    def test_match_args(self):
        """Test that the object has __match_args__ for pattern matching."""
        _ = Vector2d(3, 4)
        assert hasattr(Vector2d, '__match_args__')
        assert Vector2d.__match_args__ == ('x', 'y')

        # Simple pattern matching function to test
        def match_vector(v):
            match v:
                case Vector2d(0, 0):
                    return 'null'
                case Vector2d(0, _):
                    return 'vertical'
                case Vector2d(_, 0):
                    return 'horizontal'
                case Vector2d(x, y) if x == y:
                    return 'diagonal'
                case _:
                    return 'other'

        assert match_vector(Vector2d(0, 0)) == 'null'
        assert match_vector(Vector2d(0, 5)) == 'vertical'
        assert match_vector(Vector2d(5, 0)) == 'horizontal'
        assert match_vector(Vector2d(3, 3)) == 'diagonal'
        assert match_vector(Vector2d(3, 4)) == 'other'

    def test_slots(self):
        """Test that the class uses __slots__ and has no __dict__."""
        v = Vector2d(3, 4)
        assert not hasattr(v, '__dict__')

        # Should have __slots__ attribute
        assert hasattr(Vector2d, '__slots__')

        # Cannot add arbitrary attributes
        with pytest.raises(AttributeError):
            v.custom_attr = 'cannot add this'
