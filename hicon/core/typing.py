from __future__ import annotations
import typing as ty

import os
from pathlib import Path

PathArgType = ty.Union[os.PathLike, str]

SingleFileReaderType = ty.Callable[[PathArgType], dict[str, ty.Any]]

MultiFileReaderType = ty.Callable[
    [list[PathArgType]], tuple[dict[str, ty.Any], dict[str, Path]]
]

SingleFileWriterType = ty.Callable[[dict[str, ty.Any], PathArgType], None]
MultiFileWriterType = ty.Callable[[dict[str, ty.Any], dict[str, PathArgType]], None]

SourcePathIteratorType = ty.Callable[
    [ty.Optional[PathArgType]], ty.Iterator[PathArgType]
]

SourcePathGetterType = ty.Callable[[ty.Optional[PathArgType]], list[PathArgType]]

SterilizedType = ty.Union[str, int, float, bool, None, list, dict, tuple]

FieldParserType = ty.Callable[[ty.Any], ty.Any]
FieldEncoderType = ty.Callable[[ty.Any], SterilizedType]
FieldDecoderType = ty.Callable[[SterilizedType], ty.Any]
