import json

import pytest

from action import __main__


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

        with pytest.raises(OSError):
            __main__.convert_config(long_list_as_json)
