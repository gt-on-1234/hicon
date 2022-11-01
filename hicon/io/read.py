from __future__ import annotations
import typing as ty

import json
from pathlib import Path

from hicon.core.typing import PathArgType


def read_json_file(path: PathArgType) -> dict[str, ty.Any]:
    with open(str(path)) as file:
        data = json.load(file)

    if isinstance(data, str):
        data = json.loads(data)

    return data


def read_json_files(
    paths: list[PathArgType],
) -> tuple[dict[str, ty.Any], dict[str, Path]]:
    data = {}
    sources = {}

    for path in paths:
        new_data = read_json_file(path)

        for key, value in new_data.items():
            data[key] = value
            sources[key] = Path(path)

    return data, sources
