from __future__ import annotations
import typing as ty

import json
from pathlib import Path

from hicon.io import read_json_file, read_json_files, write_json_file, write_json_files


def test_read_json_file(temp_directory, data_with_all_dtypes):
    path = temp_directory.name + "/test_json.json"

    with open(path, "w") as writer:
        expected = data_with_all_dtypes
        json.dump(expected, writer)

    actual = read_json_file(path=path)
    assert actual == expected


def test_read_json_files(temp_directory):
    configs = [
        {"a": 1, "b": [2]},
        {"c": "Hello"},
        {"a": 9},
    ]

    paths = []
    dir_path = Path(temp_directory.name)

    for i, config in enumerate(configs):
        path = dir_path / f"test_json_{i}.json"

        with open(path, "w") as writer:
            json.dump(config, writer)

        paths.append(path)

    expected_config = {"a": 9, "b": [2], "c": "Hello"}

    expected_sources = {
        "a": paths[2],
        "b": paths[0],
        "c": paths[1],
    }

    config, sources = read_json_files(paths)

    assert config == expected_config
    assert sources == expected_sources


def test_write_json_file(temp_directory, data_with_all_dtypes):
    path = temp_directory.name + "/test_json.json"
    expected = data_with_all_dtypes
    write_json_file(expected, path)
    actual = read_json_file(path=path)
    assert actual == expected


def test_write_json_files(temp_directory):
    dir_path = Path(temp_directory.name)

    data = {
        "a": 9,
        "b": [2],
        "c": "Hello",
        "d": "World",
    }

    sources = {
        "a": dir_path / "test_json_1.json",
        "b": dir_path / "test_json_2.json",
        "c": dir_path / "test_json_3.json",
        "d": dir_path / "test_json_3.json",
    }

    write_json_files(data, sources)

    assert read_json_file(sources["a"]) == {"a": 9}
    assert read_json_file(sources["b"]) == {"b": [2]}
    assert read_json_file(sources["c"]) == {"c": "Hello", "d": "World"}
