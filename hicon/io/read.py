from __future__ import annotations
import typing as ty

import json
from pathlib import Path

from hicon.core.typing import DecoderArgType, PathArgType


def read_json_file(
    path: PathArgType, decoder: DecoderArgType = None
) -> dict[str, ty.Any]:
    if decoder is None:
        decoder = json.JSONDecoder

    with open(str(path)) as file:
        data = json.load(file, cls=decoder)

    if isinstance(data, str):
        data = json.loads(data)

    return data


def read_json_files(
    *paths: PathArgType, decoder: DecoderArgType = None
) -> tuple[dict[str, ty.Any], dict[str, Path]]:
    data = {}
    sources = {}

    for path in paths:
        new_data = read_json_file(path, decoder=decoder)

        for key, value in new_data.items():
            data[key] = value
            sources[key] = Path(path)

    return data, sources
