from __future__ import annotations
import typing as ty

import os
import glob
from pathlib import Path

from hicon.core.typing import PathArgType
from hicon.core.constants import HICON_JSON_FILE_SUFFIX


def iter_source_paths(path: ty.Optional[PathArgType] = None) -> ty.Generator[Path]:
    if path is None:
        path = os.getcwd()

    parts = Path(path).parts
    search_dir = Path()

    for part in parts:
        search_dir /= part

        dir_source_paths = glob.glob(str(search_dir / ("*" + HICON_JSON_FILE_SUFFIX)))

        for source_path in dir_source_paths:
            yield Path(source_path)


def get_source_paths(path: ty.Optional[PathArgType] = None) -> list[Path]:
    return list(iter_source_paths(path))
