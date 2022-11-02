from __future__ import annotations
import typing as ty

from datetime import datetime

from hicon import config_class


def test_create_new_config_class(base_class):
    cls = config_class(base_class)
    instance = cls(a=1, c="2020-10-01 00:00:00.0", d=(1, 2, 3), e={0, 1, -2})

    assert instance.a == 1
    assert instance.b == -2.3
    assert instance.c == datetime(2020, 10, 1)
    assert instance.d == [1, 2, 3]
    assert instance.e == frozenset({0, 1})


def test_create_new_config_class_with_options(base_class):
    cls = config_class(repr=False)(base_class)
    instance = cls(a=1)
    assert repr(instance).startswith("<")


def test_from_files(temp_files, base_class):
    cls = config_class(base_class)
    instance = cls.from_files(temp_files.config_file3)

    assert instance.a == 2
    assert instance.b == -2.3
    assert instance.c == datetime(2020, 10, 1)
    assert instance.d == [-1, -2]
    assert instance.e == frozenset({1, 3})


def test_update_source_files(temp_files, base_class):
    cls = config_class(base_class)
    instance = cls.from_files(temp_files.config_file3)

    instance.a = 3
    instance.c = datetime(2020, 11, 1)
    instance.update_source_files()
    new_instance = cls.from_files(temp_files.config_file3)

    assert new_instance.a == 3
    assert new_instance.c == datetime(2020, 11, 1)
