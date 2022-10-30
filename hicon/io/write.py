from __future__ import annotations
import typing as ty

import json
from pathlib import Path

from hicon.core.typing import EncoderArgType, PathArgType


class _JSONEncoder(json.JSONEncoder):
    def default(self, o: ty.Any) -> ty.Any:
        return super().default(o)


def write_json_file(
    data: dict[str, ty.Any], path: PathArgType, encoder: EncoderArgType = _JSONEncoder
) -> None:
    with open(str(path), "w") as file:
        json.dump(data, file, cls=encoder)


def write_json_files(
    data: dict[str, ty.Any],
    sources: dict[str, PathArgType],
    encoder: EncoderArgType = _JSONEncoder,
) -> None:
    unique_sources = {Path(source) for source in sources.values()}

    for source in unique_sources:
        source_data = {
            key: data[key] for key in sources if Path(sources[key]) == source
        }

        write_json_file(source_data, source, encoder=encoder)
