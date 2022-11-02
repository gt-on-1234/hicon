from __future__ import annotations
import typing as ty

import pytest
from datetime import datetime

from hicon.core.typing import SterilizedType
from hicon.translate import parse_value, encode_value, decode_value


@pytest.mark.parametrize(
    ["value_in", "expected_value_out"],
    [
        (1, 1),
        (2.2, 2.2),
        ("Hello", "Hello"),
        ("2022-11-01 20:04:52.1", datetime(2022, 11, 1, 20, 4, 52, 100000)),
    ],
)
def test_parse_value(value_in: ty.Any, expected_value_out: ty.Any):
    assert parse_value(value_in) == expected_value_out


@pytest.mark.parametrize(
    ["value_in", "expected_value_out"],
    [
        (1, 1),
        (2.2, 2.2),
        ("Hello", "Hello"),
        (True, True),
        (False, False),
        ({"a": [1]}, {"a": [1]}),
        (datetime(2022, 11, 1, 20, 4, 52, 100000), "2022-11-01 20:04:52.100000"),
    ],
)
def test_encode_value(value_in: ty.Any, expected_value_out: SterilizedType):
    assert encode_value(value_in) == expected_value_out


@pytest.mark.xfail(raises=NotImplementedError)
def test_encode_unsupported_value():
    class C:
        pass

    encode_value(C())


@pytest.mark.parametrize(
    ["value_in", "expected_value_out"],
    [
        (1, 1),
        (2.2, 2.2),
        ("Hello", "Hello"),
        (True, True),
        (False, False),
        ({"a": [1]}, {"a": [1]}),
        ("2022-11-01 20:04:52.100000", datetime(2022, 11, 1, 20, 4, 52, 100000)),
    ],
)
def test_decode_value(value_in: SterilizedType, expected_value_out: ty.Any):
    assert decode_value(value_in) == expected_value_out
