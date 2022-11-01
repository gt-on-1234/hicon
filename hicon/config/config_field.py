from __future__ import annotations
import typing as ty

from dataclasses import Field, MISSING

from hicon.core.typing import (
    FieldParserType,
    FieldEncoderType,
    FieldDecoderType,
)


class _Defaults(ty.Protocol):
    field_parser: FieldParserType
    field_encoder: FieldEncoderType
    field_decoder: FieldDecoderType


# Value is set automatically in hicon/__init__.py to
# decouple from the defaults.py module itself.
defaults: _Defaults


class ConfigField(Field):
    __slots__ = (*Field.__slots__, "parser", "encoder", "decoder")

    def __init__(
        self,
        default: ty.Any,
        default_factory: ty.Callable[[], ty.Any],
        init: bool,
        repr: bool,
        hash: ty.Optional[bool],
        compare: bool,
        metadata: ty.Optional[dict],
        kw_only: ty.Optional[bool],
        parser: FieldParserType,
        encoder: FieldEncoderType,
        decoder: FieldDecoderType,
    ):
        super().__init__(
            default=default,
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata,
            kw_only=kw_only,
        )

        self.parser: FieldParserType = parser
        self.encoder: FieldEncoderType = encoder
        self.decoder: FieldDecoderType = decoder


def config_field(
    *,
    default: ty.Any = MISSING,
    default_factory: ty.Callable[[], ty.Any] = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: ty.Optional[bool] = None,
    compare: bool = True,
    metadata: ty.Optional[dict] = None,
    kw_only: ty.Optional[bool] = MISSING,
    parser: ty.Optional[FieldParserType] = None,
    encoder: ty.Optional[FieldEncoderType] = None,
    decoder: ty.Optional[FieldDecoderType] = None,
):
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")

    if parser is None:
        parser = defaults.field_parser

    if encoder is None:
        encoder = defaults.field_encoder

    if decoder is None:
        decoder = defaults.field_decoder

    return ConfigField(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
        parser=parser,
        encoder=encoder,
        decoder=decoder,
    )
