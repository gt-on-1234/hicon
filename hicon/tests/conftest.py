from __future__ import annotations
import typing as ty

import pytest
from tempfile import TemporaryDirectory


@pytest.fixture
def temp_directory() -> TemporaryDirectory:
    return TemporaryDirectory()


@pytest.fixture
def data_with_all_dtypes() -> dict[str, ty.Any]:
    return {"a": 1, "b": 2.3, "c": [10, 11], "d": None, "e": {"A": 1, "B": 2}}
