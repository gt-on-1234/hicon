from __future__ import annotations
import typing as ty

from dataclasses import dataclass

from hicon.core.typing import (
    SingleFileReaderType,
    MultiFileReaderType,
    SingleFileWriterType,
    MultiFileWriterType,
    SourcePathIteratorType,
    SourcePathGetterType,
    FieldParserType,
    FieldEncoderType,
    FieldDecoderType,
)


@dataclass
class Defaults:
    """
    Store default values used across the package
    """

    # io
    single_file_reader: SingleFileReaderType
    multi_file_reader: MultiFileReaderType
    single_file_writer: SingleFileWriterType
    multi_file_writer: MultiFileWriterType
    source_path_iterator: SourcePathIteratorType
    source_path_getter: SourcePathGetterType

    # translation
    field_parser: FieldParserType
    field_encoder: FieldEncoderType
    field_decoder: FieldDecoderType
