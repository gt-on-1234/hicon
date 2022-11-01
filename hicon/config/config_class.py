from __future__ import annotations
import typing as ty

from dataclasses import asdict, fields, dataclass

from hicon.core.constants import HICON_JSON_FILE_SUFFIX

from hicon.core.typing import (
    MultiFileReaderType,
    MultiFileWriterType,
    PathArgType,
    SourcePathGetterType,
    FieldParserType,
    FieldEncoderType,
    FieldDecoderType,
)


class _Defaults(ty.Protocol):
    multi_file_reader: MultiFileReaderType
    multi_file_writer: MultiFileWriterType
    source_path_getter: SourcePathGetterType


# Value is set automatically in hicon/__init__.py to
# decouple from the defaults.py module itself.
defaults: _Defaults


@ty.runtime_checkable
class _ConfigFieldType(ty.Protocol):
    parser: FieldParserType
    encoder: FieldEncoderType
    decoder: FieldDecoderType


# def _set_new_attribute(cls: ty.Type, name: str, value: ty.Any) -> None:
#     if not hasattr(cls, name):
#         setattr(cls, name, value)


def config_class(
    cls: ty.Optional[ty.Type] = None,
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    match_args: bool = True,
    kw_only: bool = False,
    slots: bool = False,
    file_suffix: str = HICON_JSON_FILE_SUFFIX,
    multi_file_reader: ty.Optional[MultiFileReaderType] = None,
    multi_file_writer: ty.Optional[MultiFileWriterType] = None,
    source_path_getter: ty.Optional[SourcePathGetterType] = None,
):
    if multi_file_reader is None:
        multi_file_reader = defaults.multi_file_reader

    if multi_file_writer is None:
        multi_file_writer = defaults.multi_file_writer

    if source_path_getter is None:
        source_path_getter = defaults.source_path_getter

    def from_files(cls_, path: ty.Optional[PathArgType] = None):
        source_paths = source_path_getter(path)
        data, field_sources = multi_file_reader(source_paths)

        for key, field in cls_.__dataclass_fields__.items():
            if isinstance(field, _ConfigFieldType):
                data[key] = field.decoder(data[key])

        instance = cls_(**data)
        instance.field_sources = field_sources

        return instance

    def update_source_files(self) -> None:
        data = asdict(self)

        for key, field in self.__dataclass_fields__.items():
            if isinstance(field, _ConfigFieldType):
                data[key] = field.encoder(data[key])

        multi_file_writer(data, self.field_sources)

    def __setattr__(self, name: str, value: ty.Any) -> None:
        field_ = self.__dataclass_fields__.get(name)

        if isinstance(field_, _ConfigFieldType):
            value = field_.parser(value)

        super(self.__class__, self).__setattr__(name, value)

    data_class_wrapper = dataclass(
        init=init,
        repr=repr,
        eq=eq,
        order=order,
        unsafe_hash=unsafe_hash,
        frozen=frozen,
        match_args=match_args,
        kw_only=kw_only,
        slots=slots,
    )

    data_class = data_class_wrapper(cls)

    if not hasattr(data_class, "FILE_SUFFIX"):
        data_class.FILE_SUFFIX = file_suffix

    if not hasattr(data_class, "from_files"):
        data_class.from_files = classmethod(from_files)

    if not hasattr(data_class, "update_source_files"):
        data_class.update_source_files = update_source_files

    if not hasattr(data_class, "setattr"):
        data_class.__setattr__ = __setattr__

    return data_class
