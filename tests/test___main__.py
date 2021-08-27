import argparse
import json
from unittest import mock

import pytest

from action import __main__

VALID_JSON = '{"key": "value"}'
VALID_JSON_AS_DICT = {"key": "value"}
INVALID_JSON = "{'key': 'value'}"  # JSON doesn't like single quotes


class TestConvertConfig:
    def test_with_long_json_string(self):
        # We generate a long JSON string representing an array of zeros. (The function
        # that we're testing doesn't validate the configuration; it just deserializes
        # the configuration.) For n zeros, the array has 3n characters: n for each zero,
        # n-1 for each comma, n-1 for each space, and 2 for the brackets. "Long", for
        # modern file systems, seems to mean longer than 255 characters/bytes.
        # Conveniently, 255 / 3 = 85.
        n = 86
        long_list = [0] * n
        long_list_as_json = json.dumps(long_list)
        assert len(long_list_as_json) == 3 * n
        assert __main__.convert_config(long_list_as_json) == long_list

    @mock.patch("action.__main__.Path.exists", side_effect=OSError())
    def test_raises_oserror(self, mocked):
        # Test that the function doesn't catch all instances of OSError.
        with pytest.raises(OSError):
            __main__.convert_config("config.json")

    def test_with_path_to_valid_json(self, tmp_path):
        path = tmp_path / "config.json"
        with path.open("w", encoding="utf8") as f:
            f.write(VALID_JSON)

        assert __main__.convert_config(path.as_posix()) == VALID_JSON_AS_DICT

    def test_with_path_to_invalid_json(self, tmp_path):
        path = tmp_path / "config.json"
        with path.open("w", encoding="utf8") as f:
            f.write(INVALID_JSON)

        with pytest.raises(argparse.ArgumentTypeError):
            __main__.convert_config(path.as_posix())

    def test_with_valid_json(self):
        assert __main__.convert_config(VALID_JSON) == VALID_JSON_AS_DICT

    def test_with_invalid_json(self):
        with pytest.raises(argparse.ArgumentTypeError):
            __main__.convert_config(INVALID_JSON)
