from __future__ import annotations
import typing as ty

from hicon.core.typing import SterilizedType


def parse_value(value: ty.Any) -> ty.Any:
    return value


def encode_value(value: ty.Any) -> SterilizedType:
    if isinstance(value, SterilizedType):
        return value

    raise NotImplementedError(
        f"Default encoder cannot encode values of type {type(value)}. "
        f"Please specify a custom encoder."
    )


def decode_value(value: SterilizedType) -> ty.Any:
    return value
