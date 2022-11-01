from __future__ import annotations
import typing as ty

import json
from pathlib import Path

from hicon.core.typing import PathArgType


def write_json_file(data: dict[str, ty.Any], path: PathArgType) -> None:
    with open(str(path), "w") as file:
        json.dump(data, file)


def write_json_files(data: dict[str, ty.Any], sources: dict[str, PathArgType]) -> None:
    unique_sources = {Path(source) for source in sources.values()}

    for source in unique_sources:
        source_data = {
            key: data[key] for key in sources if Path(sources[key]) == source
        }

        write_json_file(source_data, source)
