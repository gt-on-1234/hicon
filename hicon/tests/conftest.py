from __future__ import annotations

import json
import typing as ty

import pytest
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from tempfile import TemporaryDirectory

from hicon import config_field
from hicon.core.constants import HICON_JSON_FILE_SUFFIX


@pytest.fixture
def temp_directory() -> TemporaryDirectory:
    return TemporaryDirectory()


@pytest.fixture
def data_with_all_dtypes() -> dict[str, ty.Any]:
    return {"a": 1, "b": 2.3, "c": [10, 11], "d": None, "e": {"A": 1, "B": 2}}


@pytest.fixture
def base_class() -> ty.Type:
    class _BaseClass:
        a: int
        b: float = -2.3
        c: datetime = datetime(2020, 10, 1)
        d: list = config_field(default_factory=list, parser=list)
        e: frozenset = config_field(
            default=frozenset(),
            parser=lambda x: frozenset(i for i in x if i >= 0),
            encoder=list,
        )

    return _BaseClass


@dataclass
class TempFiles:
    config_file1: Path
    config_file2: Path
    config_file3: Path
    temp_directory: TemporaryDirectory

    def __post_init__(self):
        for path in [self.config_file1, self.config_file2, self.config_file3]:
            for parent in reversed(path.parents):
                if not parent.exists():
                    parent.mkdir()


@pytest.fixture
def temp_files() -> TempFiles:
    temp_dir = TemporaryDirectory()
    temp_dir_path = Path(temp_dir.name)

    files = TempFiles(
        config_file1=(temp_dir_path / "test").with_suffix(HICON_JSON_FILE_SUFFIX),
        config_file2=(temp_dir_path / "folder" / "test").with_suffix(
            HICON_JSON_FILE_SUFFIX
        ),
        config_file3=(temp_dir_path / "folder" / "folder" / "test").with_suffix(
            HICON_JSON_FILE_SUFFIX
        ),
        temp_directory=temp_dir,
    )

    json.dump(dict(a=1, e=[1, 3]), open(str(files.config_file1), "w"))
    json.dump(dict(c="2020-10-01 00:00:00.0"), open(str(files.config_file2), "w"))
    json.dump(dict(a=2, d=(-1, -2)), open(str(files.config_file3), "w"))

    return files
