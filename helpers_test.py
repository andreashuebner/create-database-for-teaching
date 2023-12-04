import pytest

from helpers import load_file_content

from unittest import mock

class TestLoadFileContent:
    def test_read_exiting_file(self):
        with mock.patch('builtins.open', mock.mock_open(read_data='Andreas Huebner\nPeter Panzer')):
            file_content = load_file_content('path')
            assert(file_content == 'Andreas Huebner\nPeter Panzer' )
