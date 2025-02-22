"""This module contains unit tests for the ShortVector2d class."""

import math
import struct

import pytest  # type: ignore

from vector2d import ShortVector2d, Vector2d


class TestShortVector2d:
    """Test suite for the ShortVector2d class.

    Methods:
        - test_constructor: Tests the constructor of ShortVector2d.
        - test_typecode: Tests that ShortVector2d uses single-precision float typecode.
        - test_memory_usage: Tests that ShortVector2d uses less memory than Vector2d.
        - test_bytes_roundtrip: Tests serialization and deserialization of ShortVector2d.
        - test_precision_differences: Tests the precision differences between Vector2d and ShortVector2d.
        - test_inheritance: Tests that ShortVector2d properly inherits Vector2d methods.
        - test_mixed_operations: Tests operations between ShortVector2d and Vector2d instances.
    """

    def test_constructor(self):
        """Test ShortVector2d constructor."""
        v = ShortVector2d(3, 4)
        assert v.x == 3.0
        assert v.y == 4.0
        assert isinstance(v, Vector2d)  # Should be instance of both classes
        assert isinstance(v, ShortVector2d)

    def test_typecode(self):
        """Test that ShortVector2d uses single-precision float typecode."""
        assert ShortVector2d.typecode == 'f'
        v = ShortVector2d(3, 4)
        assert bytes(v)[0] == ord('f')  # First byte should be typecode 'f'

    def test_memory_usage(self):
        """Test that ShortVector2d uses less memory than Vector2d."""
        # Create serialized bytes for both classes with same values
        sv = ShortVector2d(3.14159, 2.71828)
        sv_bytes = bytes(sv)

        v = Vector2d(3.14159, 2.71828)
        v_bytes = bytes(v)

        # Short vector should use less bytes (4 bytes per float vs 8 bytes)
        assert len(sv_bytes) < len(v_bytes)
        assert (
            len(sv_bytes) == 1 + 2 * 4
        )  # 1 byte typecode + 2 floats × 4 bytes
        assert (
            len(v_bytes) == 1 + 2 * 8
        )  # 1 byte typecode + 2 doubles × 8 bytes

    def test_bytes_roundtrip(self):
        """Test serialization and deserialization."""
        sv1 = ShortVector2d(3.14, 2.71)
        sv_bytes = bytes(sv1)
        sv2 = ShortVector2d.frombytes(sv_bytes)

        # Values should be approximately equal (accounting for float precision)
        assert math.isclose(sv1.x, sv2.x, rel_tol=1e-6)
        assert math.isclose(sv1.y, sv2.y, rel_tol=1e-6)

    def test_precision_differences(self):
        """Test the precision differences between Vector2d and ShortVector2d."""
        # A value that requires more precision than single float can provide
        precise_value = (
            1.12345678901234  # More digits than single precision can handle
        )

        sv = ShortVector2d(precise_value, precise_value)
        v = Vector2d(precise_value, precise_value)

        # Recreate from bytes to force conversion through array typecode
        sv_bytes = bytes(sv)
        sv2 = ShortVector2d.frombytes(sv_bytes)

        v_bytes = bytes(v)
        v2 = Vector2d.frombytes(v_bytes)

        # The double-precision version should preserve more decimal places
        # than the single-precision version
        assert v2.x != sv2.x

        # We can check the actual precision by unpacking the bytes
        sv_x_bytes = sv_bytes[1:5]  # First 4 bytes after typecode
        v_x_bytes = v_bytes[1:9]  # First 8 bytes after typecode

        sv_x = struct.unpack('f', sv_x_bytes)[0]
        v_x = struct.unpack('d', v_x_bytes)[0]

        # Double precision should be closer to the original value
        assert abs(v_x - precise_value) < abs(sv_x - precise_value)

    def test_inheritance(self):
        """Test that ShortVector2d properly inherits Vector2d methods."""
        sv = ShortVector2d(3, 4)

        # Test inherited methods
        assert abs(sv) == 5.0
        assert sv.angle() == math.atan2(4, 3)
        assert format(sv, '.2fp') == '<5.00, 0.93>'
        assert repr(sv) == 'ShortVector2d(3.0, 4.0)'

        # Test __slots__
        assert not hasattr(sv, '__dict__')
        with pytest.raises(AttributeError):
            sv.arbitrary = 42

    def test_mixed_operations(self):
        """Test operations between ShortVector2d and Vector2d instances."""
        sv = ShortVector2d(3, 4)
        v = Vector2d(1, 2)

        # Test equality comparison
        assert sv != v
        assert ShortVector2d(1, 2) == v

        # Test in collections
        d = {sv: 'short_vector'}
        assert ShortVector2d(3, 4) in d
