from __future__ import annotations
import typing as ty

from datetime import datetime
from functools import singledispatch

from hicon.core.typing import SterilizedType
from hicon.core.constants import DATETIME_FORMAT


@singledispatch
def parse_value(value: ty.Any) -> ty.Any:
    return value


@parse_value.register(str)
def _(value: str) -> ty.Union[str, datetime]:
    try:
        return datetime.strptime(value, DATETIME_FORMAT)
    except ValueError:
        return value


@singledispatch
def encode_value(value: ty.Any) -> SterilizedType:
    if isinstance(value, SterilizedType):
        return value

    raise NotImplementedError(
        f"Default encoder cannot encode values of type {type(value)}. "
        f"Please specify a custom encoder."
    )


@encode_value.register(datetime)
def _(value: datetime) -> str:
    return value.strftime(DATETIME_FORMAT)


@singledispatch
def decode_value(value: SterilizedType) -> ty.Any:
    return value


@decode_value.register(str)
def _(value: str) -> ty.Union[str, datetime]:
    return parse_value(value)
