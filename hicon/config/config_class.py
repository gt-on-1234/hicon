from __future__ import annotations
import typing as ty

from dataclasses import asdict, dataclass, Field

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

    @classmethod
    def from_field(cls, field: Field) -> _ConfigFieldType:
        ...


# Value is set automatically in hicon/__init__.py to
# decouple from the config_field.py module itself.
config_field_type: _ConfigFieldType


def _process_class(
    cls: ty.Type = None,
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

        for key_, field_ in cls_.__dataclass_fields__.items():
            if key_ not in data:
                continue

            if isinstance(field, _ConfigFieldType):
                data[key_] = field_.decoder(data[key_])

        instance = cls_(**data)
        instance.field_sources = field_sources

        return instance

    def update_source_files(self) -> None:
        data = vars(self)

        for key_, field_ in self.__dataclass_fields__.items():
            if key_ not in data:
                continue

            if isinstance(field_, _ConfigFieldType):
                data[key_] = field_.encoder(data[key_])

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
    data_class_fields = data_class.__dataclass_fields__

    for key, field in data_class_fields.items():
        data_class_fields[key] = config_field_type.from_field(field)

    if not hasattr(data_class, "FILE_SUFFIX"):
        data_class.FILE_SUFFIX = file_suffix

    if not hasattr(data_class, "from_files"):
        data_class.from_files = classmethod(from_files)

    if not hasattr(data_class, "update_source_files"):
        data_class.update_source_files = update_source_files

    if not hasattr(data_class, "setattr"):
        data_class.__setattr__ = __setattr__

    return data_class


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
    def wrapper(cls_) -> ty.Type:
        return _process_class(
            cls=cls_,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            match_args=match_args,
            kw_only=kw_only,
            slots=slots,
            file_suffix=file_suffix,
            multi_file_reader=multi_file_reader,
            multi_file_writer=multi_file_writer,
            source_path_getter=source_path_getter,
        )

    if cls is None:
        return wrapper

    return wrapper(cls)
