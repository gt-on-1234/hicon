"""
hicon.

Create, use, edit and manage hierarchical configurations files with Python.
"""

__version__ = "0.1.2"
__author__ = "Oscar Nuki"

from .defaults import Defaults
from .core import constants, typing
from .config.config_class import config_class
from .config.config_field import ConfigField, config_field

from .io import (
    read_json_file,
    read_json_files,
    write_json_file,
    write_json_files,
    iter_source_paths,
    get_source_paths,
)

from .translate import (
    parse_value,
    encode_value,
    decode_value,
)


defaults = Defaults(
    single_file_reader=read_json_file,
    multi_file_reader=read_json_files,
    single_file_writer=write_json_file,
    multi_file_writer=write_json_files,
    source_path_iterator=iter_source_paths,
    source_path_getter=get_source_paths,
    field_parser=parse_value,
    field_encoder=encode_value,
    field_decoder=decode_value,
)


def _use_hicon_modules() -> None:
    """Update the settings in the required modules"""
    from .config import config_class as config_class_module

    config_class_module.defaults = defaults
    config_class_module.config_field_type = ConfigField

    from .config import config_field as config_field_module

    config_field_module.defaults = defaults


_use_hicon_modules()

__all__ = [
    "constants",
    "typing",
    "config_class",
    "config_field",
    "ConfigField",
    "read_json_file",
    "read_json_files",
    "write_json_file",
    "write_json_files",
    "iter_source_paths",
    "get_source_paths",
    "parse_value",
    "encode_value",
    "decode_value",
    "defaults",
    "__version__",
    "__author__",
]
